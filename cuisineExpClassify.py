import sys
import nltk
import re
import spacy
import en_core_web_sm
import csv
import random

#Constants Defined 
EXPERT = "EXPT"
NOEXPERT = "NOEX"
DEFAULT_CUISINE = "japanese"

"""
Global Variables
These should be loaded up from some corpus.
For this project, define them here.
"""

# Lookup Table for country and naionality
country_dict = {} 

# Lookup Table for each country and its prominent cities
geo_words = {}

def load_country():
    """
    The following function loads up the country and nationality lookup table into a dictionary 
    """
    with open('./data/my_country_national.csv', 'rU', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            country_dict[row[1].lower()] = row[0].lower()

def load_geo_words():
    """
    The following function defines the lookup table for each country and its cities  into a dictionary. 
    For this project, just work with 'japanese' only
    """

    geo_words['japanese'] = ('japan', 'japanese', 'tokyo', 'osaka', 'yokohama', 'okinawa', 'kyoto', 'nara', 'harajuku', 'shibuya','ginza') 
    geo_words['chinese'] = ('china', 'beijing', 'shanghai', 'hong kong') 

def entity_features(raw, cuisine_type):
    """
    The following function defines the feature extraction for this classifier. 
    
    Use spaCy to do NLP using en_core_web_sm. It gives us easy token interface in moving around and checking the token types.
    NOTE: I took out token.pos_ checking as it was making this function overfitting.
    
    Check the entity type to see if the token contains a country or nationality.  
    If found, we are interested in 2 tokens left of the token to obeserve the patters such as:
    GPE -> VERB/ADP/GPE (e.g. live in Japan)
    NORP -> /PRON/VERB/GPE (e.g. I am Japanese)
    """

    nlp = en_core_web_sm.load()
    doc = nlp(raw)
    features={}
    for token in doc:
        if token.i > 1 and token.ent_type_ in ('GPE', 'NORP') and token.text.lower() in geo_words[cuisine_type]:
            features['contains({})'.format(doc[token.i-2].text + " "+ doc[token.i -1].text + " " + token.text)] = token.ent_type_
    return features


def classify_this(classifier, review_text, restaurant_category):
    """
    The following function calls the classifier to classify the text and print out the result 
    """
    found_features = {}
    found_features=entity_features(review_text, restaurant_category)
    if (classifier.classify(found_features) == EXPERT):
        print ("CLASSIFIED AS: written by Authenticity Expert's Review")
    else:
        print ("CLASSIFIED AS: written by Non-authenticity Expert's Review")
    print ("\n")

def classify_with_input(classifier, restaurant_category):
    #interactively classify input text 
    answer = 'n'
    print ("Do you want to try this classifier? (y/n)")
    answer = input()
    while answer == 'y':
        print ("Enter your review:") 
        input_review = input() 
        classify_this(classifier, input_review, restaurant_category)
        print ("Do you want to try this classifier? (y/n)")
        answer = input()


def main():
    """
    This classifier determines if a review text is written by 
    someone who has authentic cuisine experiences by living in the country
    or from the country. 
    
    Although there are some hooks to handle different cuisines, 
    for the initial phase, reviews for Japanese restaurants are used to do this classification.
    The classifier along with the training data is looking 
    for key word/word pattern matches in conjunction with Entity Recognition tag.
    Phrases such as "lived in Japan" or "I am Japanese" should have a high probability
    for the authenticity expert.
    """

    load_geo_words()
    if len(sys.argv) > 1:
        restaurant_category = str(sys.argv[1]).lower()
    else:
        restaurant_category = DEFAULT_CUISINE
    featuresets = []
    from os import listdir
    from os.path import isfile, join
    data_path_exp = './data/expert/'
    data_path_nonexp = './data/nonexpert/'
    onlyfiles = [f for f in listdir(data_path_exp) if isfile(join(data_path_exp, f))]
    for f in onlyfiles:
        with open(data_path_exp + f, 'rU', newline='', encoding='utf-8') as csvfile:
            reviews = csv.reader(csvfile, delimiter=',', quotechar='"')
            featuresets += [(entity_features(raw[1], restaurant_category), EXPERT) for raw in reviews]
        csvfile.close()
    onlyfiles = [f for f in listdir(data_path_nonexp) if isfile(join(data_path_nonexp, f))]
    for f in onlyfiles:
        with open(data_path_nonexp + f, 'rU', newline='', encoding='utf-8') as csvfile:
            reviews = csv.reader(csvfile, delimiter=',', quotechar='"')
            featuresets += [(entity_features(raw[1], restaurant_category), NOEXPERT) for raw in reviews]
        csvfile.close()
    random.shuffle(featuresets)
    size = int(len(featuresets) * 0.1)
    train_set, test_set  = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print("\nCLASSIFY ACCURACY:", nltk.classify.accuracy(classifier, test_set))
    print("\n")
    classifier.show_most_informative_features(5)

    #rate adjustment
    data_path_test = './data/test/'
    onlyfiles = [f for f in listdir(data_path_test) if isfile(join(data_path_test, f))]
    tagged_ratings = []
    for f in onlyfiles:
        with open(data_path_test + f, 'rU', newline='', encoding='utf-8') as csvfile:
            reviews = csv.reader(csvfile, delimiter=',', quotechar='"')
            for raw in reviews:
                found_features = {}
                found_features=entity_features(raw[1], restaurant_category)
                tagged_ratings.append((raw[2], classifier.classify(found_features)))
        csvfile.close()
    print ("\nRate adjustment using test data")
    print ("# of reviews:",len(tagged_ratings))
    num_reviews = len(tagged_ratings)  
    sum_rating = 0
    sum_exp_rating = 0
    num_exp = 0
    for elem in tagged_ratings:
        sum_rating += int(elem[0])
        if (elem[1] == EXPERT):
            sum_exp_rating += int(elem[0]) 
            num_exp += 1 
    print ("current star rating:", int(sum_rating/num_reviews))
    print ("star rating only by EXPERTS:", int(sum_exp_rating/num_exp))
    print ("star rating adjusted (EXP:NOEXP=7:3)",int(((sum_exp_rating/num_exp)*0.7) + (((sum_rating - sum_exp_rating)/(num_reviews-num_exp))*0.3)))

    #interactivly classify 

    print ("\nShowing how it classifies some text....")
    input_review = "This is a great place! I am Japanese and I used to eat this type of food."
    print ("\nREVIEW TEXT:", input_review)
    classify_this(classifier, input_review, restaurant_category)
    input2_review = "I love Japanese food! I can eat sushi everyday."
    print ("\nREVIEW TEXT:", input2_review)
    classify_this(classifier, input2_review, restaurant_category)
    input3_review = "Don't care for the food. Trust me - I used to live in Tokyo."
    print ("\nREVIEW TEXT:", input3_review)
    classify_this(classifier, input3_review, restaurant_category)

    classify_with_input(classifier, restaurant_category)

if __name__ == "__main__":
    main()
