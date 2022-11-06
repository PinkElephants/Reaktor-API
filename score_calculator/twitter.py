from google.cloud import language_v1
import os
import requests
import yaml
import numpy as np
from dateutil.parser import parse
import pandas as pd
import string
import re

def sample_analyze_sentiment(text_content):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''
    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"content": text_content, "type_": type_}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    return {"magnitude":response.document_sentiment.magnitude,"score":response.document_sentiment.score}
    # return response.document_sentiment.score


def create_twitter_url(acc, tweets_cnt = 20, pagination_token=None):
    mrf = "max_results={}".format(tweets_cnt)
    q = "query=from:{}".format(acc)
    # url = "https://api.twitter.com/2/tweets/search/recent?{}&{}&exclude".format(
    #     mrf, q
    # )

    url = f"https://api.twitter.com/2/users/{acc}/tweets/?exclude=retweets&tweet.fields=created_at&start_time=2022-11-01T00:00:00Z"
    if pagination_token is not None:
        url += f'&pagination_token={pagination_token}'
    return url

def get_cfg():
    with open("config.yaml") as file:
        return yaml.safe_load(file)

def get_twts(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()

def analyze_prsn(twitter_id):
    cfg = get_cfg()
    token = cfg["search_tweets_api"]["bearer_token"]
    elon = get_twts(token, f'https://api.twitter.com/2/users/by/username/{twitter_id}')
    url = create_twitter_url(elon['data']['id'], 50)
    twts_res = get_twts(token, url)
    twts = twts_res['data']

    page_token = None
    if 'next_token' in  twts_res['meta'].keys():
        page_token = twts_res['meta']['next_token']

    # count = twts_res['meta']['result_count']
    while page_token:
        url = create_twitter_url(elon['data']['id'], 50, page_token)
        twts_res = get_twts(token, url)

        page_token = None
        if 'next_token' in twts_res['meta'].keys():
            page_token = twts_res['meta']['next_token']
        twts += twts_res['data']

    twts_prepared = []
    for twt in twts:
        txt = twt['text']
        date = twt['created_at']
        twts_prepared.append({"text":txt, "date_time":parse(date), "date":parse(date).date()})
        # twts_scores.append(sample_analyze_sentiment(txt))
        # print(txt, sample_analyze_sentiment(txt))
    df = pd.DataFrame.from_dict(twts_prepared)
    df['long_text'] = df.groupby(['date'])['text'].transform(lambda x: ','.join(x))
    res = df[['date', 'long_text']].drop_duplicates().to_numpy()
    # res = df[['date','text']].to_numpy()
    scores = {}
    for date,text in res:
        if date not in scores.keys():
            scores[date] = []
        sent = sample_analyze_sentiment(text)
        scores[date] = sent

        # sanitized = text.translate(str.maketrans('', '', string.punctuation))
        # sanitized = re.sub(' +', ' ', sanitized)
        # norm = len(sanitized.split(' '))
        # sent['magnitude_normalized'] = sent['magnitude']
        # scores[date].append(sent)
    res_final = {}
    for k,v in scores.items():
        # score = np.mean(v)
        # std = np.std(v)
        score = v['score']
        mag = v['magnitude']
        while mag > 1:
            mag = mag/10

        score_final = np.clip((score - mag), -1.,1.)
        res_final[k] = {"score":score,"magnitude":mag,"score_final":score_final}

    return res_final
    # score = np.mean(twts_scores)
    # std = np.std(twts_scores)
    # result_score = 'neutral'
    # if score > 0.25:
    #     result_score = 'positive'
    # if score > 0.5:
    #     result_score = 'very positive'
    # if score < -0.25:
    #     result_score = 'negative'
    # if score < -0.5:
    #     result_score = 'very negative'
    # stability = 'stable'
    # if std > 0.25:
    #     stability = 'unstable'
    # if std > 0.5:
    #     stability = 'unstable'
    #
    # return f'{result_score}_{stability}', score, std


if '__name__' == 'main':
    result_score = analyze_prsn('elonmusk')
    print(result_score)
# print(sample_analyze_sentiment('wanna die'))
# print(sample_analyze_sentiment('Life is beautiful'))