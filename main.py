import time
import json
from requests import post as POST
from requests import get as GET

with open('config.json') as json_file:
	config = json.load(json_file)

API_KEY = config['key']
CHANNEL_ID = config['id']
CHANNEL_NAME = config['name']
WEBHOOK_URL = config['webhook']
VIDEO_ENDPOINT = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=1'
THUMBNAIL_ENDPOINT = f'https://www.googleapis.com/youtube/v3/channels?part=snippet&id={CHANNEL_ID}&key={API_KEY}'

def data(ENDPOINT):
	response = GET(ENDPOINT)
	return response.json()

def send(payload):
    response = POST(WEBHOOK_URL, json=payload)
	
def main():
    while True:
        recent_title = data(VIDEO_ENDPOINT)['items'][0]['snippet']['title']
        
        with open('recent_title.txt', 'w') as file:
            file.write(recent_title)
        with open('recent_title.txt', 'r') as file:
            recent_title = file.read()

        time.sleep(599.5)

        videoData = data(VIDEO_ENDPOINT)
        thumbnailData = data(THUMBNAIL_ENDPOINT)

        new_title = videoData['items'][0]['snippet']['title']
        channel_name = videoData['items'][0]['snippet']['channelTitle']
        channel_url = f"https://www.youtube.com/user/{CHANNEL_ID if CHANNEL_NAME == '' else CHANNEL_NAME}"
        post_date = videoData['items'][0]['snippet']['publishedAt']
        video_url = f"https://www.youtube.com/watch?v={videoData['items'][0]['id']['videoId']}"
        video_thumbnail = videoData['items'][0]['snippet']['thumbnails']['high']['url']
        channel_icon = thumbnailData['items'][0]['snippet']['thumbnails']['high']['url']

        if new_title != recent_title:
            payload = {
		  "embeds": [
			{
			  "title": channel_name,
			  "description": f"Posted on {post_date}",
			  "url": channel_url,
			  "color": 16711680,
			  "fields": [
				{
				  "name": new_title,
				  "value": f"> {video_url}"
				}
			  ],
			  "author": {
				"name": "A Ram9™ Application",
				"url": "https://www.github.com/",
				"icon_url": "https://tinyimg.io/i/PO91QCh.png"
			  },
			  "footer": {
				"text": f"Tracking {channel_name} Posts",
				"icon_url": "https://artofselfdiscovery.com.au/wp-content/uploads/2020/04/thankyou-gif.gif"
			  },
			  "image": {
				"url": video_thumbnail
			  },
			  "thumbnail": {
				"url": channel_icon
			  }
			}
		  ],
		  "username": "Youtube Video Notifier",
		  "avatar_url": "https://tinyimg.io/i/A9l3tLC.png"
		}
        send(payload)
        print(f'[+] New Video Uploaded From {(channel_name).capitalize()}!')

if __name__ == "__main__":
    main()
