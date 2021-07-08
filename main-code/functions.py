from api_key import api_key
from apiclient.discovery import build
import pandas as pd

#access to youtube api
youtube = build("youtube", "v3", developerKey=api_key)


#function to get all videos from a channel

def get_all_videos(channel_id):
    '''
    Function to get all the videos from a channel
    Input: channel_id as string
    Output: json with all the videos of the channel (video id)
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

#function to get the information about all the videos from a channel, by using the channel json
def get_all_videos_information(videos_json):
    
    all_videos_information = []
    for video in range(len(videos_json)):
        video_id = videos_json[video]["snippet"]["resourceId"]["videoId"]
        video_information = get_video_information(video_id)
        all_videos_information.append(video_information)

    return all_videos_information


#function to extract the essential information from the information and make a df

def extract_essential_information(all_videos_json):
    video_statistics = {}
    video_publication_date = {}
    video_titles = {}

    for i in range(len(all_videos_json)):
        statistics = all_videos_json[i]["items"][0]["statistics"]
        video_statistics[i] = statistics

    for i in range(len(all_videos_json)):
        publication_date = all_videos_json[i]["items"][0]["snippet"]["publishedAt"]
        video_publication_date[i] = publication_date

    for i in range(len(all_videos_json)):
        title = all_videos_json[i]["items"][0]["snippet"]["title"]
        video_titles[i] = title

    df_test = pd.DataFrame(video_statistics)
    video_statistics_df = df_test.transpose()

    series = pd.Series(video_publication_date)
    publication_date_df = series.to_frame(name="publication_date")

    series2 = pd.Series(video_titles)
    titles_df = series2.to_frame(name="title")

    videos_df = pd.concat([titles_df, publication_date_df, video_statistics_df],axis=1)

    return videos_df