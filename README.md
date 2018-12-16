# Cuisine Authenticity Expert Finder
This classifier was created for a class project of my text analysis class.

It classifies restaurant reviews into two categories: text written by a cuisine authenticity expert (EXPT) and text written by a non cuisine-authenticity expert (NOEX).

For this project, the definition of the "cuisine authenticity" expert is a person who has lived or traveled to the country of the particular cuisine or a native of the country -- anyone who has first-hand experience in the cuisine. Furthermore, this background/nationality information comes from their restaurant reviews on the public web. Thus, the "cuisine authenticity" experts are self-proclaimed within their reviews.

NOTE: for the initial version, the supported cuisine type is Japanese only.

Please see the Overview and Implementation sections for details.

## Installation

NOTE: The information below applies to the Mac OS environment. Adjust it to your environment as needed. 

Download the project from git as follows:

```bash
git clone https://github.com/cmik2/cuisine-expert-class.git
cd cuisine-expert-class 
```

Next, using [pip](https://pip.pypa.io/en/stable/) to install the required packages as follows:

```bash
pip install --upgrade nltk numpy spacy
```

If the installation failed due to file/directory permissions, you may want to do the following command instead:

```bash
sudo pip install --upgrade nltk numpy spacy
```

## Usage

To run:

First, load spaCy's English module shown below. This may not be required but, in some environment (i.e., gitlab), you need this step: 

```python
python -m spacy download en
```
Then you can run the classifier as follows:
```python
python cuisineExpClassify.py
```
It takes a few minutes before you see any display. For instance, it took almost 10 minutes on my mac.

Then you will see the following information:
1. classify accuracy
2. Rate adjuments example based on the test data in ./data/test weighted in the 7:3 ration between EXPT and NOEX
3. Examples of the text classification
4. Interactive session to take input and classfiy it



Below is the sample output:

```python
CLASSIFY ACCURACY: 0.9411764705882353


Most Informative Features
 contains(live in Japan) = 'GPE'            EXPT : NOEX   =      7.2 : 1.0
contains(am not Japanese) = 'NORP'           EXPT : NOEX   =      3.1 : 1.0
contains(! Great Japanese) = 'NORP'           EXPT : NOEX   =      3.1 : 1.0
 contains(back to Japan) = None             NOEX : EXPT   =      1.1 : 1.0
 contains(back in Japan) = None             NOEX : EXPT   =      1.0 : 1.0

Rate adjustment using test data
# of reviews: 20
current star rating: 4
star rating only by EXPERTS: 2
star rating adjusted (EXP:NOEXP=7:3) 3

Showing how it classifies some text....

REVIEW TEXT: This is a great place! I am Japanese and I used to eat this type of food.
CLASSIFIED AS: written by Authenticity Expert's Review



REVIEW TEXT: I love Japanese food! I can eat sushi everyday.
CLASSIFIED AS: written by Non-authenticity Expert's Review



REVIEW TEXT: Don't care for the food. Trust me - I used to live in Tokyo.
CLASSIFIED AS: written by Authenticity Expert's Review


Do you want to try this classifier? (y/n)
n
```

According to the displayed classifying samples, try typing your text to see how it classify your text your text. After each text input, type 'y' to continue or 'n' to quit the script. 

## Overview

### Motivation and Goal of this project:
When choosing restaurants, I always rely on Yelp ratings. The most ratings are helpful; however, when it comes to my native country's food, some of the highly rated restaurants are not quite authentic enough for my native palate. For Yelp users who seek true authentic cuisine experiences, I hope to provide different ratings or adjusted ratings based on the reviewers who have the first-hand experience in the cuisine. These reviewers are referred as the self-proclaimed Cuisine Authenticity experts in this project.

## Implementation Notes

### Approach:
This is a text categorization problem. I need to define a feature extractor looking for certain qualifying phrases and train the classifier with the sample data.

### Qualifying Phrases (i.e. matching patterns):
Generally speaking, restaurant reviewers' background and ethnicities are not publicly shared due to the policies of review-providing companies. However, some reviewers willingly comment about their background to establish their credentials as a "cuisine-authenticity" expert. This classifier is looking for the self-proclaiming phrases such as:

"I used to live in Tokyo and go to sushi places a lot. ....This place has awesome sushi!"

"I am Japanese. I can tell when I see good Japanese food.

"I have visted Japan many times. I can tell when I see good Japanese food.


With this approach, I define the feature extraction function for this classifier.

### Data Sampling and Traing Data:

Two sets of sample data are under the installation directory:


data/expert      -- Sample Expert Reviews

data/nonexpert   -- Sample Non-expert Reviews 



These data sets are created sololy for the purpose of this project. Please don't use them outside of this classifier.

The data input format is in CSV. Each review is in the following format: 


"reviewer name","review text","star rating" 


First, I tried to use Yelp's academic dataset for the reviews. However, the review data is so voluminous and is a mixture of all the business categories. I needed more controlled sample data. Thus I decided to extract restaurant reviews from the web using parse_hub.com to create my sample data. A target restaurant is a popular Japanese restaurant.

Analyzing the data from the web, I noticed that many reviewers were commenting about the authenticities of the food but none of them mentioned their background or nationalities, my criteria for this classification. Thus, I needed to interject my qualifying phrases into the raw data to create the sample data.

Although I scraped 700 records from the web, I only used 340 records to train the classifier. It was too time-consuming to create the samples for 700 records and made the python script run for more than more than 10 minutes for the amount. 

### Tool choices:
To categorize the reviews, I need Natural Language Processing(NLP) utilities to obtain Part of Speech(POS) to tokenize the self-proclaimed phrases and Entity Recognition(ER) information (e.g., Japan, Japanese). To do so, I use:

spaCy -- to parse and tokenize the text to tag each token with lexical POS and ER information

nltk -- modeling classifier and train the data

Initially, nltk was the only choice for NLP. However, after feeding through raw
texts from my sample data, I found that:

1. Simple tokens had wrong Entity Recognition tag in nltk. (e.g., "Hello" was tagged as country)
2. nltk's POS tags were too extensive. Instead of having 5 different verb tags based on its use, all I needed was just "VERB".

After some researching, I decided to use spaCY for the NLP parsing.  With one function call, spaCy can parse and tag POS and ER. POS Tags are simple tag such as  "VERB" and  "ADP". Also I can access tokens easily by simple index.

### Feature Extraction

The logic of the feature extractor is as follows:


if token is either GTE or NORP for the particular cuisine, make annotation as ((token.left).left) + token.left + token


After many iterative processes in adjusting sample data and feature extraction annotations/tagging, I ended up with the simple logic above.

When finding tokens with the ER tags such as GTE (a tag for countries and cities like "Japan")  or NORP (a tag for nationality like "Japanese"), I was looking for phrases like "live in Japan" by checking POS patterns of Verb + Preposition + GTE token. With typical programming attitude to strive for 100% code coverage, I was even qualifying/defining what the preposition should be. This mentality caused overfitting issues during the classification, and it could not classify beyond "live in Japan".  After resolving the overfitted issue, the classifier started to show accuracy between 0.7 and 0.9. It shows the training model behavior: more sample data, better the accuracy. 

### Future implementation and extension
1. Although there is a hook to support different cuisines, it must include corpus to define the appropriate countries of the cuisines and their cities.

2. More rubost input interface for feeding data. Currently it takes CSV files with 3 double-quoted fields (i.e., reviewer, text, and rating) separated by comma. 

3. I need to investigate if we have enough self-proclaimed authenticity experts in the production environment. If not, the overall ratings remain the same without reflecting authenticity consideration.  

## Contribution
Produced for a class project by C. Miklasevich, an MCS-DS student at UIUC
