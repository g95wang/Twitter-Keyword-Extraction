import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue as PQ

directory = [os.getcwd() + '/new_processed-data-labeled', os.getcwd() + '/processed-data-unlabeled']

text = 0
lemma = 1
dic_word = 2
word_index = 3
pos = 4
dep = 5
stop = 6
label = 7

doc_with_term = {} # term -> number of documents with term t in it
total_num_of_doc = 0 # total number of documents

def build_dic(cwds):
	global doc_with_term
	global total_num_of_doc

	occ_in_this_doc = {} # term -> number of times term t appears in a document

	for cwd in cwds:

		for filename in os.listdir(cwd):
			
			if filename != None and filename[0] != 'p':
				continue

			with open(os.path.join(cwd, filename), 'r') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')

				for row in csv_reader:
					if row[dic_word] not in occ_in_this_doc:
						occ_in_this_doc[row[dic_word]] = 1
					else:
						occ_in_this_doc[row[dic_word]] += 1

				for k in occ_in_this_doc:
					if k not in doc_with_term:
						doc_with_term[k] = 1
					else:
						doc_with_term[k] += 1

				total_num_of_doc += 1
				occ_in_this_doc.clear()

	return doc_with_term, total_num_of_doc

def calc_tfidf(cwd, filename, threshold):
	global doc_with_term
	global total_num_of_doc

	tp = 0
	fp = 0
	fn = 0
	tn = 0
	
	occ_in_this_doc = {}
	keywords = set()

	with open(os.path.join(cwd, filename), 'r') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')

			for row in csv_reader:
				if row[dic_word] not in occ_in_this_doc:
					occ_in_this_doc[row[dic_word]] = 1
				else:
					occ_in_this_doc[row[dic_word]] += 1

				if row[label] == '1':
					keywords.add(row[lemma].lower())

			word_count = sum(occ_in_this_doc.values())

			scores = []

			for k in occ_in_this_doc:
				tf = occ_in_this_doc[k]/word_count
				idf = math.log(total_num_of_doc/doc_with_term[k])
				tfidf = tf * idf

				# print(tfidf)
				
				if tfidf > threshold:
					if k in keywords:
						tp += 1
					else:
						fp += 1
				else:
					if k in keywords:
						fn += 1
					else:
						tn += 1

			occ_in_this_doc.clear()
			keywords.clear()

	precision = 0
	recall = 0

	if tp+fp != 0:
		precision = tp/(tp+fp) * word_count

	if tp+fn != 0:
		recall = tp/(tp+fn) * word_count

	return precision, recall, word_count


def cross_validation(thresholds):
	precisions = []
	recalls = []
	fscores = []

	for threshold in thresholds:
		# print("#####", threshold)
		i = 0
		precision = 0
		recall = 0
		word_count = 0
		
		for filename in os.listdir(directory[0]):

			if filename != None and filename[0] != 'p':
					continue

			if i < 900:
				i += 1
				continue

			i += 1

			p, r, w = calc_tfidf(directory[0], filename, threshold)

			# print(i, p, r, w)

			precision += p
			recall += r
			word_count += w

		precision = precision/word_count
		recall = recall/word_count

		precisions.append(precision)
		recalls.append(recall)

		if precision == 0 and recall != 0:
			fscores.append(2/(1/recall))
		elif precision != 0 and recall == 0:
			fscores.append(2/(1/precision))
		elif precision == 0 and recall == 0:
			fscores.append(0)
		else:
			fscores.append(2/(1/recall + 1/precision))

	max_index = np.argmax(np.asarray(fscores))
	print('precision:', precisions[max_index])
	print('recall:', recalls[max_index])
	print('fscore:', fscores[max_index])
	print('threshold:', thresholds[max_index])
	return precisions, recalls, fscores


def plot(thresholds, precisions, recalls, fscores):
	plt.plot(thresholds, precisions, 'r')
	plt.plot(thresholds, recalls, 'b')
	plt.plot(thresholds, fscores, 'g')
		
	plt.xlabel('thresholds')
	plt.ylabel('score')
	plt.legend(['precisions', 'recalls', 'fscores'], loc='upper left')
	plt.savefig('tfidf.svg', format = 'svg')


thresholds = np.arange(0.1, 1, 0.001)
doc_with_term, total_num_of_doc = build_dic(directory)
precisions, recalls, fscores = cross_validation(thresholds)
plot(thresholds, precisions, recalls, fscores) 
