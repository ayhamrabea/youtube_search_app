from django.shortcuts import render  , redirect
import requests
from project import settings
from isodate import parse_duration       # لتحةيل الوقت

def index(request):

    videos = []

    if request.method == "POST" :
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KET,
            'maxResults' : 9,
            'type' : 'video'
        }
        
        r = requests.get(search_url , params=search_params)
        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])
        

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')



        video_params = {
            'key' : settings.YOUTUBE_DATA_API_KET,
            'part' : 'snippet,contentDetails',
            'id' : ','.join(video_ids),
            'maxResults' : 9,
        }

        r = requests.get(video_url , params=video_params)
        results = r.json()['items']
        
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'time' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'img' : result['snippet']['thumbnails']['high']['url'],
                'url' : 'https://www.youtube.com/watch?v=' + result["id"]
            }

            videos.append(video_data)

    context = {
        'videos' : videos
    }

    return render(request,'index.html' , context)
