from difflib import SequenceMatcher
import preprocessor as p
import string
import spacy
import csv
import sys

##### return the most similar word in the dictionary #####
def find_similar(word):
	cur_max = 0
	cur_word = ''
	for w in dictionary:                                                                                                                                                                                                                                                                                                                                                                                                          
		score = SequenceMatcher(None, w, word).ratio() * 100
		if score > cur_max:
			cur_max = score
			cur_word = w
	return cur_word

##### setup dictionary #####
file = open('all_words.txt', 'r')
lines = file.readlines()

index = 0
dictionary = {}
for w in lines:
	dictionary[w.strip('\n')] = index
	index += 1

file.close()

twitter_dictionary = {}

processed = int(sys.argv[1])
limit = int(sys.argv[2])

# data cleaning -> https://pypi.org/project/tweet-preprocessor/
p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.RESERVED, p.OPT.EMOJI, p.OPT.SMILEY, p.OPT.NUMBER)

# different models -> https://spacy.io/models/en
nlp = spacy.load("en_core_web_sm")

with open('labeled_tweets.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')

	with open('twitter_dictionary.csv', "a") as dic:
		dic_writer = csv.writer(dic)

		i = 0

		for row in csv_reader:
			if i == limit:
				break

			if i < processed - 1:
				i = i + 1
				continue

			i = i + 1
			print('Start processing tweet NO.', i)

			tweet = row[0]
			keys = row[1]

			# print('original:', tweet)
			cleaned = p.clean(tweet)
			if len(cleaned) > 0:
				if cleaned[0] == ':':
					cleaned = cleaned[1:]

				# print('cleaned:', cleaned)

				dependency_tagged = nlp(cleaned)

				filename = 'processed-data-labeled/processed-labeled-tweet-' + str(i) + '.csv'
				
				with open(filename, "a") as file:
				    # https://spacy.io/usage/spacy-101#annotations-pos-deps
					writer = csv.writer(file)
					for token in dependency_tagged:

						if token.lemma_ != '-PRON-' and token.pos_ != 'SPACE' and token.text not in string.punctuation and token.text.isdigit() == False and token.pos_ != 'PUNCT' and token.pos_ != 'NUM' and token.pos_ != 'X':
							lower_case = token.lemma_.lower()
							word_index = 0
							
							if lower_case in dictionary:
								word_index = dictionary[lower_case]
								
							else:
								print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.is_stop)
								lower_case = find_similar(lower_case)
								if lower_case == '':
									print('############# unfound ############')
									continue
								word_index = dictionary[lower_case]
								print(lower_case, word_index)

							if lower_case not in twitter_dictionary:
								twitter_dictionary[lower_case] = word_index
								r = [lower_case, word_index]
								dic_writer.writerow(r)
							
							if token.text in keys:
								row = [token.text, token.lemma_, lower_case, word_index, token.pos_, token.dep_, token.is_stop, 1]

							else:
								row = [token.text, token.lemma_, lower_case, word_index, token.pos_, token.dep_, token.is_stop, 0]	
								
							writer.writerow(row)

						else:
							print('!!!!! invalid token !!!!!', token.text)
