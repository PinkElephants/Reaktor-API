import numpy as np
from twitter import analyze_prsn
from music import process_music
import json
import pandas as pd


def get_score(twit, music):
    score_twit = twit['score_final']
    music_sad = music['sadness_indes']
    music_happy = music['happyness_index']
    score = 0.8 +score_twit * 0.5 + (music_happy-music_sad)*0.5
    score = np.clip(score,0.,1.)
    return score*100

person_scores = analyze_prsn('elonmusk')

with open('parsed_music.json') as f:
    json_file = json.load(f)
musics = process_music(json_file)


result_scores = {}

for played,hap,sad in musics[['played_at','happyness_index','sadness_indes']].to_numpy():
    music = {'played_at':played,'happyness_index':hap,'sadness_indes':sad}
    twittor = None
    if music['played_at'] in person_scores.keys():
        twittor = person_scores[music['played_at']]
    result_scores[played.isoformat()] = get_score(twittor,music)

with open('result_scores.json', 'w') as fp:
    json.dump(result_scores, fp)
# result = pd.DataFrame.from_dict(result_scores)
# result.to_csv('result_score.csv')