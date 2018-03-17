import json
import requests
from api_key import api_key

def get_list():
    """
    Returns a list of all the songs needed to display with correct added fields
    """
    # replace below with this to get from subsplash api
    songs = get_json_youtube_from_subsplash()
    # songs = get_youtube_samples()
    list_of_songs = []
    for item in songs['_embedded']['media-items']:
        print(item)
        duration, views = get_duration_and_views(item['youtube_url'])
        item['duration'] = format_duration(duration)
        item['views'] = views
        list_of_songs.append(item)

    return sorted(list_of_songs, key=lambda song: song['reach'], reverse=True)

def get_json_youtube_from_subsplash():
    """
    Takes care of getting all of the youtube videos from subsplash
    """
    url = 'https://challenge.subsplash.net'
    headers = {'X-Sap-Auth': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlN2U5NDhlOC0xMzA3LTRhNDktOTkzZS1jZDQwMGIyNDBiNzMiLCJpYXQiOjE1MTc0NDMyMDB9.cCnoZDiDA1wZDw2jrbRgpwWvtA5nHHaDaUKLl1fAXAY'}
    r = requests.get(url, headers=headers)
    return r.json()

def get_duration_and_views(url):
    """
    Used to get the title and duration of a youtube video given a video id.
    """
    x = url.split('https://www.youtube.com/watch?v=')
    if len(x) < 13:
        video_id = x
    else:
        return '5H23M33S', 1000000
    payload = {'id': video_id, 'part': 'contentDetails,statistics,snippet', 'key': api_key}
    l = requests.Session().get('https://www.googleapis.com/youtube/v3/videos', params=payload)
    resp_dict = json.loads(l.content)
    print(resp_dict)
    duration = resp_dict['items'][0]['contentDetails']['duration'].lstrip('PT')
    views = resp_dict['items'][0]['statistics']['viewCount']

    return duration, views

def format_duration(duration):
    """
    In order to change the duration from 5H23M15S to 5:23:15
    Needs to fill with 00 in case it's missing.  i.e. a youtube video that is exactly 1 hour long will have 1H only.  
    """
    output = []
    if 'H' in duration:
        hours, duration = duration.split('H')
        output.append('%02d' % int(hours[0]))
    else:
        output.append('00')
    if 'M' in duration:
        minutes, duration = duration.split('M')
        output.append('%02d' % int(minutes[0]))
    else:
        output.append('00')
    if 'S' in duration:
        seconds = duration.split('S')
        output.append('%02d' % int(seconds[0]))
    else:
        output.append('00')
    return output
