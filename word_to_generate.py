# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 17:06:24 2018

@author: shen1994
"""

import random
import collections
import numpy as np

class Word2Generate:
    
    __data_index = 0
    
    def __init__(self):
        pass
    
    @staticmethod
    def read_translate_file(file_name):
        word_bag = []
        
        with open(file_name, "r") as infile:
            for row in infile:
                row = row.strip()
                row = row.split()
                for word_index in row:
                    word_bag.append(int(word_index))
                    
        return word_bag
    
    @staticmethod
    def generate_batch(data, batch_size, skip_window):

        num_skips = 2 * skip_window
        
        assert batch_size % num_skips == 0
        
        batch = np.ndarray(shape=(batch_size), dtype=np.int32)
        labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
        
        # 为每个单词创建相关样本时会使用的单词数量，包括目标单词本身和他前后的单词
        span = 2 * skip_window + 1        
        buffer = collections.deque(maxlen = span)
        
        # 初始化buffer数组
        for _ in range(span):
            buffer.append(data[Word2Generate.__data_index])
            Word2Generate.__data_index = (Word2Generate.__data_index + 1) % len(data)
        
        for i in range(batch_size // num_skips):
            target = skip_window
            target_to_avoid = [skip_window] # 除目标词汇外，产生乱序的batch组合
            # 对于label，当前词前后乱序存放
            for j in range(num_skips):
                while target in target_to_avoid:
                    target = random.randint(0, span - 1)
                target_to_avoid.append(target)
                batch[i * num_skips + j] = buffer[skip_window]
                labels[i * num_skips + j, 0] = buffer[target]
            # 再次跟新
            buffer.append(data[Word2Generate.__data_index])
            Word2Generate.__data_index = (Word2Generate.__data_index + 1) % len(data)
            
        return batch, labels
    
if __name__ == "__main__":
    word_to_generate = Word2Generate()
    word_bag = word_to_generate.read_translate_file("translate.txt")
    batch, labels = word_to_generate.generate_batch(data=word_bag, 
                                                batch_size=8, 
                                                skip_window=1)
