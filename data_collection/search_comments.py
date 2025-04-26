from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os

# Replace "YOUR_API_KEY" with your actual YouTube Data API key
api_key = "YOUR_API_KEY" 
api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, developerKey=api_key)

# Function to save data to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to fetch all comments for a given video
def get_all_comments(video_id):
    comments = []
    page_token = None
    while True:
        try:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=100,
                pageToken=page_token
            )
            response = request.execute()
            comments.extend(response['items'])
            page_token = response.get('nextPageToken')
            if not page_token:
                break
        except HttpError as e:
            error_reason = e.error_details[0]['reason']
            if error_reason == 'commentsDisabled':
                print(f"Comments are disabled for video ID {video_id}. Skipping...")
                break
            else:
                raise e
    return comments

def main():

    # Load unique video IDs
    with open('unique_video_ids.txt', 'r') as file:
        unique_video_ids = [line.strip() for line in file]

    # Allow the user to choose the range of video IDs to retrieve comments from (in case you do not want to get all at a time)
    start_index = int(input(f"Enter the start index for comments (0 to {len(unique_video_ids)-1}): "))
    end_index = int(input(f"Enter the end index for comments ({start_index} to {len(unique_video_ids)-1}): "))

    # Define the directory to save JSON files
    output_dir = 'comments_json'

    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Fetch all comments for each selected video and save them
    for index, video_id in enumerate(unique_video_ids[start_index:end_index+1], start=start_index):
        comments = get_all_comments(video_id)
        comments_filename = os.path.join(output_dir, f"{index}_{video_id}_comments.json")
        save_to_json(comments, comments_filename)
        print(f"Saved comments for video ID {video_id} to '{comments_filename}'.")

if __name__ == "__main__":
    main()
