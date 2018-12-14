# Self-proclaimed Cuisine Expert Finder

!!!!!UNDER CONSTRUCTION!!!!!!!!!!
A Classifier project - Find self-proclaimed authenticity experts in restaurant reviews.

This classifier determines if a review text is written by someone who has authentic cuisine experiences by living in the cuisine's originating country or being a native of the country.

Using the text categorization technique with the help of Entity Recognition tagging, this classifier probabilistically
categorizes the text into written by Authenticity Expert or Non-authenticity Expert.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

GitLab:
Using the .gitlab-ci.yml in this repository, you can run this in your gitlab environment by "run pipeline."


GitHub:
If you download this repository to your environment, then you can run the script by:


```bash
pip install --upgrade nltk numpy spacy
```

## Usage

To run:

```python
python -m spacy download en
python cuisineExpClassify.py
```
It takes some time depending on your environment.

For instance, it took almost 4 minutes on my mac.
real	3m44.554s
user	3m47.480s
sys	0m22.853s

## Overview
cuisienExpertClassifier.py


## Implementation Notes
Although there are some hooks to handle different cuisines,
for the initial phase, reviews for Japanese restaurants are used to do this classification.
The classifier trained in reviews from a Japanese restaurant is looking for word pattern matches along with Entity Recognition tag. Phrases such as "lived in Japan" or "I am Japanese" should have a high probability of authenticity experts' reviews.
With sufficient detail so that others can have a basic understanding of your code for future extension or any further improvement.

## Usage
of the software including either documentation of usages of APIs or detailed instructions on how to install and run the software, whichever is applicable.

## Contribution
Produced for a class project by C. Miklasevich, an MCS-DS student at UIUC:1
