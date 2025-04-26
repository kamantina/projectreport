import json
import pandas as pd
import os


def load_video_data(input_file):
       
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data

def process_video_info(data):

    # Extract the relevant information
    video_data = []
    for video in data:
        video_info = {
            'videoId': video['id'],
            'title': video['snippet']['title'],
            'description': video['snippet']['description'],
            'publishedAt': video['snippet']['publishedAt'],
            'tags': ', '.join(video['snippet'].get('tags', [])),  # list item
            'default_'
            'viewCount': video['statistics'].get('viewCount', 'N/A'),
            'likeCount': video['statistics'].get('likeCount', 'N/A'),
            'commentCount': video['statistics'].get('commentCount', 'N/A'),
            'duration':video['contentDetails'].get('duration', 'N/A')
        }
        video_data.append(video_info)

    return video_data

def main():

    # Define the file name for input and output 
    input_json = 'combined_videos_info.json'
    output_csv = 'video_metadata.csv'

    # Load data
    raw_data = load_video_data(input_json)

    # Get video data
    video_data = process_video_info(raw_data)

    # Convert to a DataFrame
    df = pd.DataFrame(video_data)

    # # List of video IDs to be filtered out (if any)
    # non_english_ids = [list]

    # # Filter out videos with IDs in the non-english list (if any)
    # df = df[~df['videoId'].isin(non_english_ids)]

    # # Extract video IDs and save to a text file (if needed)
    # video_ids = df['videoId'].tolist()
    # with open('filtered_video_ids.txt', 'w') as f:
    #     for video_id in video_ids:
    #         f.write(f"{video_id}\n")

    # Save to a CSV file (change the file name where necessary)
    df.to_csv('[video_file_name].csv', index=False)

if __name__ == "__main__":
    main()

