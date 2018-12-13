A Classifier project - Find self-proclaimed authenticity experts in restaurant reviews

    This classifier determines if a review text is written by
    someone who has authentic cuisine experiences by living in the country or from the country.

    Although there are some hooks to handle different cuisines,
    for the initial phase, reviews for Japanese restaurants are used to do this classification.
    The classifier trained in reviews from a Japanese restaurant is looking
    for word pattern matches along with Entity Recognition tag. Phrases such
    as "lived in Japan" or "I am Japanese" should have a high probability for
    authenticity experts' reviews.

***How to run the script***

GitLab:
Using the .gitlab-ci.yml in this repository, you can run this in your gitlab environment by "run pipeline".


GitHub:
If you download this repository to your environment, then you can run the script by: 


pip install --upgrade nltk numpy spacy
python -m spacy download en
python cuisineExpClassify.py
