import nltk
import re
import spacy
import en_core_web_sm
import csv
import random


country_dict = {} 
geo_words = {}
def load_country():
    with open('./data/my_country_national.csv', 'rU', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            country_dict[row[1].lower()] = row[0].lower()

def load_geo_words():
    geo_words['japanese'] = ('japan', 'japanese', 'tokyo', 'osaka', 'yokohama', 'okinawa', 'kyoto', 'nara', 'harajuku', 'shibuya','ginza') 

def entity_features(raw, cuisine_type):
    nlp = en_core_web_sm.load()
    doc = nlp(raw)
    features={}
    for token in doc:
        if token.ent_type_ == 'GPE':
            if token.i > 1 and token.text.lower() in geo_words[cuisine_type] and doc[token.i - 1].pos_ == 'ADP' and doc[token.i-2].pos_=='VERB':
                features['contains({})'.format(doc[token.i-2].text + " "+ doc[token.i -1].text + " " + token.text)] = True
        elif token.ent_type_ == 'NORP':
            if token.i > 1 and token.text.lower() in geo_words[cuisine_type] and (doc[token.i - 1].pos_ == "VERB" and doc[token.i-2].pos_ == "PRON") and (doc[token.i -
            1].text.lower() in ("'re", "are", "'m", "am") and doc[token.i-2].text.lower() in ("i", "we")):
                features['contains({})'.format(doc[token.i-2].text + " "+ doc[token.i -1].text + " " + token.text)] = True
        else:
            features['contains({})'.format(token.text)] = False 
    return features

def main():
    load_geo_words()
    restaurant_category = "Japanese".lower()
    featuresets = []
    from os import listdir
    from os.path import isfile, join
    data_path_exp = './data/expert/'
    data_path_nonexp = './data/nonexpert/'
    onlyfiles = [f for f in listdir(data_path_exp) if isfile(join(data_path_exp, f))]
    for f in onlyfiles:
        with open(data_path_exp + f, 'rU', newline='', encoding='utf-8') as csvfile:
            reviews = csv.reader(csvfile, delimiter=',', quotechar='"')
            featuresets += [(entity_features(raw[1], restaurant_category), "EXPT") for raw in reviews]
        csvfile.close()
    onlyfiles = [f for f in listdir(data_path_nonexp) if isfile(join(data_path_nonexp, f))]
    for f in onlyfiles:
        with open(data_path_nonexp + f, 'rU', newline='', encoding='utf-8') as csvfile:
            reviews = csv.reader(csvfile, delimiter=',', quotechar='"')
            featuresets += [(entity_features(raw[1], restaurant_category), "NOEX") for raw in reviews]
        csvfile.close()
    random.shuffle(featuresets)
    size = int(len(featuresets) * 0.1)
    train_set, test_set  = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("accuracy:", nltk.classify.accuracy(classifier, test_set))
    classifier.show_most_informative_features(5)

if __name__ == "__main__":
    main()
