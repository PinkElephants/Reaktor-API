import numpy as np
import json
import pandas as pd
import datetime
from dateutil.parser import parse



def process_music(json):
    data = pd.DataFrame([ {"played_at":parse(item['played_at']).date(),
                           "mode": item['track_statistic']['mode'],
                           "mode_confidence": item['track_statistic']['mode_confidence'],
                           "confident_major": item['track_statistic']['mode'] == 1 and item['track_statistic']['mode_confidence'] > 0.4,
                           "confident_minor": item['track_statistic']['mode'] == 0 and item['track_statistic']['mode_confidence'] > 0.4,
                           "unconfident": item['track_statistic']['mode_confidence'] < 0.4
                           } for item in json_file])


    confident_major = data.groupby(['played_at'])['confident_major'].sum().reset_index(name='sum')

    confident_minor = data.groupby(['played_at'])['confident_minor'].sum().reset_index(name='sum')

    unconfident = data.groupby(['played_at'])['unconfident'].sum().reset_index(name='sum')

    confident_major= confident_major.rename(columns={'sum':'major_sum'})
    confident_minor= confident_minor.rename(columns={'sum':'minor_sum'})
    unconfident= unconfident.rename(columns={'sum':'unconf_sum'})

    res = pd.concat([confident_major,confident_minor,unconfident], axis=1)
    res = res.loc[:,~res.columns.duplicated()]
    res['happyness_index'] = res['major_sum'] / (res['major_sum'] + res['minor_sum'] +res['unconf_sum'] + np.finfo(float).eps)
    res['sadness_indes'] = res['minor_sum'] / (res['major_sum'] + res['minor_sum'] +res['unconf_sum'] + np.finfo(float).eps)
    return res

with open('parsed_music.json') as f:
    json_file = json.load(f)

res = process_music(json)
print(res)
