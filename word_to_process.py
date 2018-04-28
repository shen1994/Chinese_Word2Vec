# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 10:20:07 2018

@author: shen1994
"""

import re

class Word2Process:
    def __init__(self):
        pass

    @staticmethod    
    def get_dict(dict_name):
        row_index = 0
        word_dict = dict()
        with open(dict_name, "r", encoding="utf-8") as infile:
            for row in infile:
                row_index += 1
                row = row.strip()
                row = row.split()
                if row:
                    word_dict[row[0]] = int(row[1])
                              
        return word_dict

    @staticmethod
    def get_reverse_dict(word_dict):
        reverse_dict = dict(zip(word_dict.values(), word_dict.keys()))
        return reverse_dict
        
 
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
                    
        return word_bag
                    
    def build_dataset(self, file_name, dict_name):
        rows, word_list = self.read_data(file_name)
        word_bag = self.data_filter(rows, word_list)
        
        word_dict = Word2Process.get_dict(dict_name)
        
        data = list()
        for word in word_bag:
            if word in word_dict:
                index = word_dict[word]
            else:
                index = 0
            data.append(index)
            
        return data
        
    def save_dataset(self, file_name, dict_name, save_name):
        """
        @params[out]: save_name为写入的输出名
        """
        rows, word_list = self.read_data(file_name)
        
        word_bag = []
        for i in range(rows):
            row_list = []
            word_row = word_list[i]
            for j in range(len(word_row)):
                row_filter = re.match("^[\u4e00-\u9fa5]+$", word_row[j])
                if row_filter:
                    row_list.append(row_filter.group(0))
            if row_list:
                word_bag.append(row_list)
                
        with open(save_name, "w+") as infile:
            infile.truncate()
        
        word_dict = Word2Process.get_dict(dict_name)
        
        with open(save_name, "w") as infile:
            for bag_row in word_bag:
                row_list = []
                for word in bag_row:
                    if word in word_dict:
                        index = word_dict[word]
                    else:
                        index = 0
                    row_list.append(index)
                    
                for row_index in row_list:
                    infile.writelines(str(row_index))
                    infile.writelines("  ")
                    
                infile.writelines("\n")       
                
    
if __name__ == "__main__":
    word_to_process = Word2Process()
    data = word_to_process.build_dataset("pku_training.txt", "dict.txt")
    word_to_process.save_dataset("pku_training.txt", "dict.txt", "translate.txt")
    