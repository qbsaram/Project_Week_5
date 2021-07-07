from api_key import api_key
from apiclient.discovery import build
youtube = build("youtube", "v3", developerKey=api_key)


#function to get all videos from a channel

def get_all_videos(channel_id):
    '''
    Function to get all the videos from a channel
    Input: channel_id as string
    Output:
    '''
    res = youtube.channels().list(id=channel_id, part="contentDetails").execute()
    
    playlist_id = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    videos = []
    next_page_token = None

    while 1:
        res = youtube.playlistItems().list(playlistId=playlist_id, part="snippet", maxResults=50, pageToken=next_page_token).execute()

        videos += res["items"]
        next_page_token = res.get("nextPageToken")

        if next_page_token is None:
            break
    
    return videos



#function to get video information by video id
def get_video_information(video_id):   

    request_video = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id)
    response = request_video.execute()
    return response