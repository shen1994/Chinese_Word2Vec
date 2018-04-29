# Chinese_Word2Vec

## 0.效果展示  
![image](https://github.com/shen1994/README/raw/master/images/Word2Vec.jpg)  

## 1. 字库链接  
* 私人云盘: 链接: <https://pan.baidu.com/s/1J3QoqZ8vi8senjG1wPWr9A> 密码: gakk  
* 字库网络路径: <http://sighan.cs.uchicago.edu/bakeoff2005/>  
* 路径: icwb2-data\training\pku_training.txt  

## 2. 操作流程  
* 根据词频制作词典,产生dict.txt文件  
`python word_to_dict.py`  
* 根据词典把语料重新编码,产生translate.txt文件  
`python word_to_process.py`  
* 训练样本,维度是128,大约在100000次loss趋于平缓  
`python train.py`  
* 加载训练完成的模型,生成相近的10个或更多的词  
`python match.py`  
* 参数说明:words = match(match_word=u"找", dict_name="dict.txt",embed_vec=embed_vec, k=10)  
@params[in]: match_word--->带匹配的词  
@params[in]: dict_name--->生成的字典文件  
@params[in]: embed_vec--->根据模型生成,字典中所有词对应的128维向量  
@params[in]: k--->相近的词的数目  
@params[out]: similar_words--->返回匹配的相近的词  

