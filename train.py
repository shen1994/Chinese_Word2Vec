# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 19:29:23 2018

@author: shen1994
"""

import argparse
import numpy as np
import tensorflow as tf

from word_to_generate import Word2Generate

parser = argparse.ArgumentParser()
parser.add_argument("--batch_size", help="batch size value", default=128, type=int)
parser.add_argument("--embedding_size", help="embedding size value", default=128, type=int)
parser.add_argument("--skip_window", help="skip window value", default=1, type=int)
parser.add_argument("--num_sampled", help="negative sample noise number value", default=64, type=int)
parser.add_argument("--vocab_num", help="vocabulary number value", default=50000, type=int)
parser.add_argument("--learning_rate", help="learning rate value", default=1.0, type=float)
parser.add_argument("--epoc_values", help="training epoc value", default=100001, type=int)

args = parser.parse_args()
batch_size = args.batch_size
embedding_size = args.embedding_size
skip_window = args.skip_window
num_sampled = args.num_sampled
vocab_num = args.vocab_num
learning_rate = args.learning_rate
epoc_values = args.epoc_values

if __name__ == "__main__":
    
    word_bag = Word2Generate.read_translate_file("translate.txt")
    
    graph = tf.Graph()
    
    with graph.as_default():
        train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
        train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
        
        with tf.device('/cpu:0'):
            embeddings = tf.Variable(tf.random_uniform([vocab_num, embedding_size], -1.0, 1.0))
            embed = tf.nn.embedding_lookup(embeddings, train_inputs)
            
            nce_weights = tf.Variable(
                        tf.truncated_normal([vocab_num, embedding_size], \
                                            stddev=1.0 / np.sqrt(embedding_size)))
            nce_biases = tf.Variable(tf.zeros([vocab_num]))
        
            loss = tf.reduce_mean(tf.nn.nce_loss(weights=nce_weights,
                                                 biases=nce_biases,
                                                 labels=train_labels,
                                                 inputs=embed,
                                                 num_sampled=num_sampled,
                                                 num_classes=vocab_num))
            
            optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)
            norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
            normalized_embeddings = tf.divide(embeddings, norm, name="embedding_vector")

        saver = tf.train.Saver(max_to_keep=2)
        init = tf.global_variables_initializer()    
        with tf.Session(graph=graph) as sess:
            init.run()
            
            average_loss = 0.
            step = 0
            for step in range(epoc_values):
                
                batch_inputs, batch_labels = Word2Generate.generate_batch(data=word_bag, 
                                                    batch_size=batch_size, 
                                                    skip_window=skip_window)
                _, loss_value = sess.run([optimizer, loss],
                                         feed_dict={train_inputs: batch_inputs, train_labels: batch_labels})
                average_loss += loss_value
                
                if step % 100 == 0 and step > 0:
                    average_loss /= 100.
                    print(step, ':', average_loss)
                    average_loss = 0
                    
                if step % 50000 == 0 and step >0:
                    saver.save(sess, 'ckpt/Word2Vec.ckpt', global_step = step)
                  