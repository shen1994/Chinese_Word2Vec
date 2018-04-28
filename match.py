# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 20:35:08 2018

@author: shen1994
"""

import os
import numpy as np
import tensorflow as tf

from word_to_process import Word2Process

is_save_vector = False

def match(match_word, dict_name, embed_vec, k):
    word_dict = Word2Process.get_dict(dict_name)
    reverse_dict = Word2Process.get_reverse_dict(word_dict)
    
    word_index = 0
    for word in word_dict:
        if match_word == word:
            word_index = word_dict[word]
    
    word_vector = embed_vec[word_index]

    dist_list = list()
    
    for vec in embed_vec:
        dist = np.sqrt(np.sum(np.square(word_vector - vec)))
        dist_list.append(dist)
        
    dist_index = np.argsort(dist_list)
    
    similar_words = list()
    
    for i in range(k):
        similar_index = dist_index[i]
        similar_words.append(reverse_dict[similar_index])
     
    similar_words[0] = match_word

    return similar_words
    
    

if __name__ == "__main__":

    saver = tf.train.import_meta_graph('ckpt/Word2Vec.ckpt-100000.meta')
        
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        
        saver.restore(sess, 'ckpt/Word2Vec.ckpt-100000')
        
        _embed_vec = tf.get_default_graph().get_tensor_by_name("embedding_vector:0")

        embed_vec = sess.run(_embed_vec)
    
    if is_save_vector:
        if os.path.exists("embedding_vector.txt"):
            os.remove("embedding_vector.txt")
            
        np.savetxt("embedding_vector.txt", embed_vec)
        
    words = match(match_word=u"上帝", dict_name="dict.txt",embed_vec=embed_vec, k=10)
    
    print(words)
    