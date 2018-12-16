# Cuisine Authenticity Expert Finder
This classifier was created for a class project of my text analysis class.

It classifies restaurant reviews into two categories: text written by a cuisine authenticity expert (EXPT) and text written by a non cuisine-authenticity expert (NOEX).

Definition of the "cuisine authenticity" expert is a person who has lived or traveled to the country of the particular cuisine or a native to the country. Furthermore, this background/nationality information can be found in their restaurant reviews from the public web. Thus, the "cuisine authenticity" experts are self-proclaimed within their reviews.

NOTE: for the initial version, the supported cuisine type is Japanese only.

Please see the Overview and Implementation sections for details.

## Installation

Download the project from git as follows:

```bash
git clone https://github.com/cmik2/cuisine-expert-class.git
cd cuisine-expert-class 
```

Next, using [pip](https://pip.pypa.io/en/stable/) to install the required packages as follows:

```bash
pip install --upgrade nltk numpy spacy
```

If the installation failed due file/directory permission, you may want to do the following command instead:

```bash
sudo pip install --upgrade nltk numpy spacy
```

## Usage

To run:

First load the spaCy module by:

```python
python -m spacy download en
```
Then you can run the classifier as follows:
```python
python cuisineExpClassify.py
```
It takes some time depending on your environment.

For instance, it took almost 6 minutes on my mac.

Then you will see the output similar to the one below, showing:

1. classify accuracy
2. Rate adjuments example based on the test data in ./data/test weighted in the 7:3 ration between EXPT and NOEX
3. Examples of the text classification
4. Interactive session to take input and classfiy it

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
## Overview

### Motivation and Goal of this project:
When choosing restaurants, I always rely on Yelp ratings. The most ratings are helpful; however, when it comes to my native country's food, some of the highly rated restaurants are not quite authentic enough for my native palate. For Yelp users who seek true authentic cuisine experiences, I hope to provide different ratings or adjusted ratings based on the self-proclaimed experts in consideration of the cuisine authenticity.

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

the data input format is in CSV. Each review is in the following format: 


"reviewer name","review text","star rating" 


First, I tried to use Yelp's academic dataset for the reviews. However, the review data is so voluminous and is a mixture of all the business categories. I needed more controlled sample data. Thus I decided to extract restaurant reviews from the web using parse_hub.com to create my sample data. A target restaurant is a popular Japanese restaurant serving Sushi.

Analyzing the data from the web, I noticed that many reviewers were commenting about the authenticities of the food but none of them mentioned their background or nationalities, my criteria for this classification. Thus, I needed to interject my qualifying phrases to create the sample data.

Although I scraped 700 records from the web, I only used 340 records to train the classifier. It was too time-consuming to create the samples for 700 records and made the python script run for more than more than 10 minutes for the amount. 

### Tool choices:
To categorize the reviews, I need Part of Speech to tokenize the self-proclaimed phrases and Entity Recognition information (e.g., Japan, Japanese). To do so, I use:

spaCy -- parsing of text using the Natural Language Processing (NLP) approach to tokenize the text with POS and Entity Recognition tagging

nltk -- modeling classifier and train the data

Initially, nltk was the only choice for NPL. However, after feeding through raw
texts from my sample data, I found that:

1. Simple tokens had wrong Entity Recognition Tag.
2. nltk's POS tags were too extensive. Instead of having 5 different verb tags based on its use, all I needed is just one tag for "VERB".

After researching in the other NLP options, I decided to use spaCY for the NLP parsing of the text.
With one function call, it can parse and tag POS and ER. POS Tags are simple "VERB",  "ADP", and such. I can access tokens by simple index.

### Feature Extraction
Logic: if token is either GTE or NORP for the particular cuisine, make annotation as ((token.left).left) + token.left + token

After many iterative processes in adjusting sample data and feature extraction annotations/tagging, I ended up with the simple logic above.

When finding tokens with Entity Recognition tags such as GTE (tagged for Japan)  or NORP (tagged for Japanese), I was looking for phrases like "live in Japan" by checking POS patterns of Verb +
Preposition + GTE token. With typical programming attitude to strive for 100% code coverage, I was even
qualifying/defining what the preposition should be. This mentality caused overfitting issues during the classification, and it could not classify beyond "live in Japan".  After resolving the overfitted issue, the classifier started to show accuracy between 0.7 and 0.9. It shows the training model behavior: more sample data, better the accuracy. 

### Future implementation and extension
1. Although there is a hook to support different cuisines, it must include corpus to define the appropriate countries of the cuisines and their cities.

2. I need to investigate if we have enough self-proclaimed authenticity experts in the production environment. If not, the overall ratings remain the same without reflecting authenticity consideration.  

## Contribution
Produced for a class project by C. Miklasevich, an MCS-DS student at UIUC
