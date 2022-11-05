from google.cloud import language_v1
import os
import requests
import yaml
import numpy as np

def sample_analyze_sentiment(text_content):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'PATH_TO_TOKEN'
    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"content": text_content, "type_": type_}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    return response.document_sentiment.score

def create_twitter_url(acc, tweets_cnt = 20):
    mrf = "max_results={}".format(tweets_cnt)
    q = "query=from:{}".format(acc)
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        mrf, q
    )
    return url

def get_cfg():
    with open("config.yaml") as file:
        return yaml.safe_load(file)

def get_twts(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()

def analyze_prsn(twitter_id):
    url = create_twitter_url(twitter_id)
    cfg = get_cfg()
    token = cfg["search_tweets_api"]["bearer_token"]
    twts = get_twts(token, url)
    twts_scores = []
    for twt in twts['data']:
        txt = twt['text']
        twts_scores.append(sample_analyze_sentiment(txt))
        # print(txt, sample_analyze_sentiment(txt))
    score = np.mean(twts_scores)
    std = np.std(twts_scores)
    result_score = 'neutral'
    if score > 0.25:
        result_score = 'positive'
    if score > 0.5:
        result_score = 'very positive'
    if score < -0.25:
        result_score = 'negative'
    if score < -0.5:
        result_score = 'very negative'
    stability = 'stable'
    if std > 0.25:
        stability = 'unstable'
    if std > 0.5:
        stability = 'unstable'
    return f'{result_score}_{stability}', score, std


result_score = analyze_prsn('elonmusk')
print(result_score)
# print(sample_analyze_sentiment('wanna die'))
# print(sample_analyze_sentiment('Life is beautiful'))