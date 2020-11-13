import csv
import json
import os, glob
from english_words import english_words_set
# from nltk.corpus import words
import nltk
def readfile(filename):
    data = []
    file = open(filename, 'r')
    while True: 
        # Get next line from file 
        line = file.readline() 
        if not line: 
            break
        currdata = json.loads(line)
        if "lang" in currdata:
            if currdata["lang"] == "en":
                data.append(currdata["text"])
    return data

def main():
    # unlabelled
    alldata = []
    os.chdir("./unlabeled_data")
    for eachfile in glob.glob("*.json"):
        alldata.extend(readfile(eachfile))
    
    for eachtweet in alldata:
        with open(r'saved_tweets.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([eachtweet])

    # labeled
    os.chdir("../labeled_data")
    tweets_texts = []
    tweets_keys = []
    for eachfile in glob.glob("*/*.txt"):
        keyfile = os.path.splitext(eachfile)[0] + ".key"
        tweets_texts.append(open(eachfile).read().splitlines()[0])
        keys = open(keyfile).read().splitlines()
        tweets_keys.append(keys)

    for i in range(0, len(tweets_texts)):
        with open(r'labeled_tweets.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([tweets_texts[i], tweets_keys[i]])

    word_list = nltk.corpus.words.words()
    os.chdir("..")
    f = open("all_words.txt", "w") 
    for eachword in word_list:
        f.write(eachword + "\n")
    f.close()

if __name__ == "__main__":
    main()
