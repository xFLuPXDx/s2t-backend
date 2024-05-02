from dotenv import dotenv_values
import googleapiclient.discovery

config = dotenv_values(".env")
YOUTUBE_API_KEY = config["YOUTUBE_API_KEY"]

youtube = googleapiclient.discovery.build("youtube","v3",developerKey=YOUTUBE_API_KEY)

def get_youtube_url(topic):
    request = youtube.search().list(
        part="snippet",
        type = "video",
        maxResults=1,
        order="relevance",
        q=topic,
        relevanceLanguage="en",
        videoDuration = "medium",
        safeSearch = "strict"
    )

    response = request.execute()

    return response["items"][0]["id"]["videoId"]