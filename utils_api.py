#!/usr/bin/env python3

from monkeylearn import MonkeyLearn
import requests
import pickle
import json
import pandas as pd
import string, re
import os
APIKEY_MONKEYLEARN = os.environ.get('APIKEY_MONKEYLEARN')
APIKEY_NEWSAPI = os.environ.get('APIKEY_NEWSAPI')

def get_sentiment(phrase: str) -> dict:
    """
    Get sentiment on phrase from monkeylearn API.

    Result:
        label = str
        confidence = float
    """
    ml = MonkeyLearn(APIKEY_MONKEYLEARN)
    response = ml.classifiers.classify(
        model_id='cl_pi3C7JiL',
        data=[phrase],
        )
    classification = response.body[0]['classifications'][0]
    return {'label': classification.get('tag_name'),
            'confidence': classification.get('confidence')}


def get_news_headers(phrase: str,
                    key_from='2021-12-24',
                    key_pageSize='5',
                    ) -> dict:
    """
    Get a list of recent news on phrase from newsapi API.

    Result:
        articles = List( title = str,
                           url = str,
                          date = str )
    """
    url = 'https://newsapi.org/v2/everything'
    payload = {'from': key_from,
               'q': phrase,
               'pages': 1,
               'pageSize': key_pageSize,
               'sortBy': 'popularity',
               'apiKey': APIKEY_NEWSAPI,}
    r = requests.get(url, params=payload).json()
    res = {}
    res['articles'] = []
    articles = r.get('articles')
    for a in articles:
        date = a.get('publishedAt')
        title = a.get('title')
        url = a.get('url')
        res['articles'].append({'title': a.get('title'),
                                'url': a.get('url'),
                                'date': a.get('publishedAt')})

    return res


def get_factcheck(phrase: str, datadir='.') -> dict:
    """
    Get a list of relevant factchecked articles given request.

    Currently, uses Kaggle dataset and simply matches the similar
    entries to the string based on mutual set intersection measure.
    """

    def dist(a,b):
        c = set(b)
        return 2.*len(a.intersection(c)) / (len(a) + len(c))

    def clean_text(text):
        text = text.replace('’s','')
        text_nopunct = "".join([char.lower() for char in text if char not in string.punctuation])
        text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
        return text_no_doublespace

    res = {}
    dfs = dict(true=pd.read_csv(f'{datadir}/True.csv'),
               fake=pd.read_csv(f'{datadir}/Fake.csv'))
    for k in 'true fake'.split():
        res[k] = {}
        df = dfs[k]
        dmax = 0
        tidmax = 0
        set_phrase = set(clean_text(phrase).split())
        for tid,t in enumerate(df.title.iloc[:]):
            d = dist(set_phrase, clean_text(t).split())
            if (d > dmax):
                # print(set_phrase, t, d)
                tidmax = tid
                dmax = d
        res[k] = {'title': df.title.loc[tidmax], 'score': dmax}

    return res


def get_ml_analysis(phrase: str, datadir='.') -> dict:
    import nltk as nlp # Main Library for NLP
    from nltk.corpus import stopwords # stopwords
    from nltk.util import ngrams
    # nlp.download("stopwords")
    # nlp.download('omw-1.4')

    lemma=nlp.WordNetLemmatizer()
    def clean_text(text):
        text = text.replace('’s','')
        text_nopunct = "".join([char.lower() for char in text if char not in string.punctuation])
        text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
        return text_no_doublespace

    # def text_process(data):
    #     text_list=[]
    #     for text in data.text:
    #         text=re.sub("[^a-zA-Z]"," ",text) # extracting unnecesary characters
    #         text=text.lower() #makes characters lowercase
    #         text=nlp.word_tokenize(text) # splits all the words
    #         text=[word for word in text
    #                     if not word in set(stopwords.words("english"))] # extract stopwords
    #         text=[lemma.lemmatize(word) for word in text] # Lemmatisation
    #         text=" ".join(text)
    #         text_list.append(text)

    # return text_list
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    with open('countvectorizer.pkl', 'rb') as f:
        cv = pickle.load(f)

    # print(cv.get_feature_names())

    phrase_df = pd.DataFrame({'text': [phrase]})
    # print(phrase_df)
    # print(text_process(phrase_df))
    # print(phrase)
    # print(clean_text(phrase))

    res = model.predict(cv.transform([clean_text(phrase)])) #text_process(phrase_df)))

    return {'result': res[0]}


