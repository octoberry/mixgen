from apiclient.discovery import build
from server import app


DEVELOPER_KEY = app.config['YOUTUBE_API_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(query, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results,
        type='video'
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(dict(title=search_result["snippet"]["title"],
                               id=search_result["id"]["videoId"]))

    return videos
