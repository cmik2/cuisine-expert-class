# Cuisine Authenticity Expert Finder
This classifier is an outcome of a text analysis class project.

It classifies restaurant reviews in text format into two categories: text written by an authenticity expert (EXPT) and by a non-authenticity expert
(NOEX).

Using the text categorization technique with the help of Entity Recognition tagging, this classifier probabilistically categorizes the text into EXPT and NOEX.

NOTE: fot the initial version, the supported cuisine type is Japanese only.

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

For instance, it took almost 4 minutes on my mac.

real	3m44.554s *separate paragraph*
user	3m47.480s*separate paragraph*
sys	0m22.853s

## Overview

### Motivation of this project:
When choosing restaurants, I always rely on Yelp ratings. The most ratings are helpful; however, when it comes to my
native country's food, I had more misses than hits in the restaurant selection.  Some highly rated restaurants cannot
deliver the essential elements of the cuisine right. I don't want people to think that this is quintessential of my
country's cuisine through these restaurants. On the same note,  when I choose restaurants specialized in a specific
cuisine, I want reviews and ratings by the people who know about the cuisine. When looking for a good Dim Sum place, I
would like to hear from someone from Hong Kong telling us if the restaurant serves decent Dim Sum. If we have ratings by people who can judge the cuisine's authenticity, it helps us foodies and cuisine-adventure seekers in restaurant selections.

### Goal of this project:
Initially, my goal was to adjust the ratings of the cuisine restaurants based on reviewers who have the authenticity experience with the cuisine. However, during the data design and analysis phase, I discovered that there were no reviewers who reveal their background and ethnicity in 1000 reviews of my target restaurants, leaving me no rating adjustment necessary.  Thus, my project remains in classification only, no rate adjustments.

## Implementation Notes

### Approach:
This is a text categorization problem. I need to define a feature extractor looking for certain qualifying phrases and train the classifier with the sample data.

### Qualifying Phrases:
Generally speaking, restaurant reviewers' background and ethnicities are not publicly shared due to the policies of review-providing companies. However, some reviewers willingly comment about their background to establish their credentials as a "cuisine-authenticity" expert. This classifier is looking for the self-proclaiming phrases such as:

"I used to live in Tokyo and go to sushi places a lot. ....This place has awesome sushi!"*separate paragraph*
"I am Japanese. I can tell when I see good Japanese food."*separate paragraph*

With this approach, I define the feature extraction function for this classifier.

### Data Sampling and Traing Data:

Two sets of sample data are under the installation directory:

data/expert      -- Sample Expert Reviews*separate paragraph*
data/nonexpert   -- Sample Non-expert Reviews *separate paragraph*

These data sets are created sololy for the purpose of this project. Please don't use them outside of this classifier.

First, I tried to use Yelp's academic dataset for the reviews. However, the review data is so voluminous and is a mixture of all the business categories. I needed more controlled sample data. Thus I decided to extract restaurant reviews from the web using parse_hub.com to create my sample data. A target restaurant is a popular Japanese restaurant serving Sushi.

Analyzing the data from the web, I noticed that many reviewers were commenting about the authenticities of the food but none of them mentioned their background or nationalities, my criteria for this classification.

Questions raised during the analysis -  Is it merely that we don't have enough people traveled to Japan or from Japan? This restaurant is in the area where we have a good number of Japanese communities and business hubs for many companies with business in Japan. We should have many people who can be an authenticity expert. Perhaps, do we have differences in reviewers' behaviors based on cuisines and types of foods?  Would reviewers want to comment more about background experience depending on the cuisine such as Chinese food, Mexican food over Japanese food? How about Dim Sum over Sushi or Ramen?

If we don't have enough reviewers self-proclaiming their background and ethnicities, there is no validity for this classification. This needs to be studied separately. For this project, I add the self-proclaiming phrases into the sample data to move on to the implementation phase.

### Tool choices:
To categorize the reviews, I need Part of Speech to tokenize the self-proclaimed phrases and Entity Recognition information (e.g., Japan, Japanese). To do so, I use:

spaCy -- parsing of text using the Natural Language Processing (NLP) approach to tokenize the text with POS and Entity Recognition tagging

nltk -- modeling classifier and train the data

Initially, nltk was the only choice for NPL. However, after feeding through raw
texts from my sample data, I found that:

1. Simple tokens had wrong Entity Recognition Tag GTE/NORP.
2. nltk's POS tags were too extensive. Instead of having 5 different verb tags based on its use, all I needed is just one tag for "VERB".

After researching in the other NLP options, I decided to use spaCY for the NLP parsing of the text.
With one function call, it can parse and tag POS and ER. POS Tags are simple "VERB",  "ADP", and such. I can access tokens by simple index.

### Feature Extraction
Logic: if token is either GTE or NORP for the particular cuisine, make annotation as ((token.left).left) + token.left + token

After many iterative processes in adjusting sample data and feature extraction annotations/tagging, I ended up with the simple logic above.

When encountering a GTE or NORP token, I was looking for phrases like "live in Japan" by checking POS patterns of Verb +
Preposition + GTE token. With typical programming attitude to strive for 100% code coverage, I was even qualifying/defining what the preposition should be. This mentality caused overfitting issues during the classification, and it could not classify beyond "live in Japan".  After resolving the overfitted issue, the classifier started to show accuracy between 0.7 and 0.9. It could be trained better with more sample data.

### Future implementation and extension
Although there is a hook to support different cuisines, it must include corpus to define the appropriate countries of the cuisines and their cities. 

If there are enough self-proclaimed authenticity experts data-mined in the reviews, we can use this classifier to adjust restaurant ratings weighing their ratings.

## Contribution
Produced for a class project by C. Miklasevich, an MCS-DS student at UIUC:1
