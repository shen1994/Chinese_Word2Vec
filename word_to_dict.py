# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 20:28:04 2018

@author: shen1994
"""

import re
import collections

class Word2Dict:
    vocabulary_number = 50000
    
    def __init__(self, vocabulary_number=50000):
        self.vocabulary_number = vocabulary_number
        
    def get_vocabulary_number(self):
        return self.vocabulary_number
        
    def read_data(self, file_name):
        row_index = 0
        word_bag = []
        with open(file_name, "r") as infile:
            for row in infile:
                row_index += 1
                row = row.strip()
                row_items = row.split()
                word_bag.append(row_items)
                
        return row_index, word_bag
        
    def data_filter(self, rows, data):
        word_bag = []

        # 过滤得到中文字符
        for i in range(rows):
            word_row = data[i]
            for j in range(len(word_row)):
                row_filter = re.match("^[\u4e00-\u9fa5]+$", word_row[j])
                if row_filter:
                    word_bag.append(row_filter.group(0))
        
        # 保证元素的唯一性
        #word_set = set(word_bag)

        return word_bag
        
    def word_count(self, word_bag, is_save=False):
        unknown_name = u"未知"
        count = [[unknown_name, -1]]
        count.extend(collections.Counter( \
                        word_bag).most_common(self.vocabulary_number))
        
        dictionary = dict()
        for word, _ in count:
            dictionary[word] = len(dictionary)
        
        reverse_dictionary = dict(zip( \
                                dictionary.values(), dictionary.keys()))
        reverse_dictionary[0] = unknown_name

        if is_save:
            dict_file_name = "dict.txt"
            
            dict_file = open(dict_file_name, "w+")
            dict_file.truncate()
            dict_file.close()
            dict_file = open(dict_file_name, "a", encoding="utf-8")
            
            sorted_keys = sorted(reverse_dictionary.keys())
            for i in range(len(sorted_keys)):
                word_key = sorted_keys[i]
                word_value = reverse_dictionary[word_key]
                dict_file.writelines(word_value + "  " + str(word_key) + "\n")
                
            dict_file.close()
            
        return count
                
        
if __name__ == "__main__":
    word_to_dict = Word2Dict(vocabulary_number=50000)
    rows, word_list = word_to_dict.read_data("pku_training.txt")
    word_bag = word_to_dict.data_filter(rows, word_list)
    count = word_to_dict.word_count(word_bag, is_save=True)
    