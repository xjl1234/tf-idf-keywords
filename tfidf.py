# encoding=utf-8
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import math


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def get_corpus(path):
	corpus_list = []
	files_list = os.listdir(path)
	for cur_filename in files_list:
		f = open(str(path + "/" + cur_filename), 'rb')
		cur_file = f.read()
		cur_file = cur_file.decode()
		cur_file = cur_file.split(" ")
		corpus_list.append(cur_file)
		f.close()
	return corpus_list, files_list


#计算词频
def get_if(content):
	word_dic ={}
	words_list = content.split(" ")
	for word in words_list:
		if word in word_dic:
			word_dic[word] = word_dic[word]+1
		else:
			word_dic[word] = 1
	# for key in word_dic:
	# 	print(key,word_dic[key])
	return word_dic


#计算tfidf
def get_tfidf(word_dic, corpus):
	word_idf = {}
	word_tfidf = {}
	num_corpus = len(corpus)
	count = 0
	num_files = 0
	for cur_corpus in corpus:
		num_files = num_files + len(cur_corpus)
		for line in cur_corpus:
			for word in word_dic:
				if word in line:
					if word in word_idf:
						word_idf[word] = word_idf[word] + 1
					else:
						word_idf[word] = 1
	for key, value in word_dic.items():
		if key != " ":
			if key not in word_idf:
				temp_idf = 0
			else:
				temp_idf = word_idf[key]
			temp = num_files/(temp_idf+1)
			temp_log = math.log(temp)
			word_tfidf[key] = value * temp_log
	values_list = sorted(word_tfidf.items(), key=lambda item: item[1], reverse=True)
	return values_list

f1 = open('原文.txt', 'rb')
for line in f1:
	line = line.decode()
	txt_cut = jieba.cut(line)
	stopWords_dic = open('stopwords.dat', 'rb')
	stopWords_content = stopWords_dic.read()
	stopWords_content = stopWords_content.decode()
	stopWords_list = stopWords_content.splitlines()
	outstr = ''
	for word in txt_cut:
	    if word not in stopWords_list:
	        outstr += word
	        outstr += " "
	word_dic = get_if(outstr)
	with open('corpus.txt', 'r', encoding='utf-8') as f3:
	    res3 = f3.readlines()
	with open('en_corpus.txt', 'r', encoding='utf-8') as f4:
	    res4 = f4.readlines()
	corpus = [res3, res4]
	valuelist_tfidf = get_tfidf(word_dic, corpus)
	with open ('keyword.txt', 'a+') as f:
		for i in range(0, 10):
			str = '"' + valuelist_tfidf[i][0] + '"' + ','
			f.write(str)
		f.write('\n')








