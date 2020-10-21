import requests
import json
import sys
import csv
import pandas as pd
import string
from itertools import chain
import re


def doubleDigit(num):
    if num < 10:
        return '0'+str(num)
    else:
        return str(num)


def main(v_id):

    if sys.version_info[0] == 2:
        reload(sys)
        sys.setdefaultencoding('utf-8')

    videoId = v_id
    clientId = ''  # c_id

    chat = []
    time = []
    user = []

    nextCursor = ''

    params = {}
    params['client_id'] = clientId

    i = 0

    while True:
        if i == 0:
            URL = 'https://api.twitch.tv/v5/videos/' + \
                videoId+'/comments?content_offset_seconds=0'
            i += 1
        else:
            URL = 'https://api.twitch.tv/v5/videos/'+videoId+'/comments?cursor='
            URL += nextCursor

        response = requests.get(URL, params=params)

        j = json.loads(response.text)

        for k in range(0, len(j["comments"])):
            tmp = []
            timer = j["comments"][k]["content_offset_seconds"]

            timeMinute = int(timer/60)

            # if timeMinute >= 60:
            #     timeHour = int(timeMinute/60)
            #     timeMinute %= 60
            # else:
            #     timeHour = int(timeMinute/60)

            timeSec = int(timer % 60)
            tmp.append(doubleDigit(timeMinute))
            # tmp.append(doubleDigit(timeHour)+':'+doubleDigit(timeMinute))
            # +':'+doubleDigit(timeSec))
            # user.append(j["comments"][k]["commenter"]["display_name"])
            tmp.append(j["comments"][k]["message"]["body"])
            time.append(tmp)

        if '_next' not in j:
            break

        nextCursor = j["_next"]

    # f = open(videoId+".csv", 'wt')
    with open(videoId+".csv", 'wt', newline='', encoding='utf-8')as f:
        w = csv.writer(f)
        w.writerow(['time', 'chat'])
        for i in time:
            w.writerows([i])
    data = pd.read_csv(videoId+".csv")
    tmp_data = data
    time_list = tmp_data.drop_duplicates("time", keep="first")[
        'time'].values.tolist()
    with open(videoId+'_result.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['time', 'mount'])
        for i in time_list:
            chat = "".join(list(chain(*data[data['time'].isin([i])].drop(
                'time', axis=1).values.tolist()))).lower()
            match_pattern = re.findall(r'[ㅋ]', chat)
            w.writerow([i, len(match_pattern)])


if __name__ == "__main__":
    main(sys.argv[1])
