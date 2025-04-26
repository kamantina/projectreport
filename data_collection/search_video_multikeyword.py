from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json


# Replace "YOUR_API_KEY" with the actual YouTube Data API key
api_key = "YOUR_API_KEY"
api_service_name = "youtube"
api_version = "v3"

youtube = build(api_service_name, api_version, developerKey=api_key)

# Function to search for videos with a given keyword
def search_videos(query, max_results=50, page_token=None):
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results,
        pageToken=page_token,
        order='viewCount',  # View Count from highest to lowest
        eventType='none',   # Exclude live broadcasts
        type='video'        # Ensure only videos are returned
    ).execute()

    print(f"Page info for query '{query}': {search_response.get('pageInfo')}")
    videos = search_response.get('items', []) 
    next_page_token = search_response.get('nextPageToken')

    return videos, next_page_token

# Function to save data to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Function to get video details
def get_video_details(video_ids):
    video_details = []
    for i in range(0, len(video_ids), 50):  # API allows max 50 IDs per request
        response = youtube.videos().list(
            part='snippet,contentDetails,statistics',
            id=','.join(video_ids[i:i+50])
        ).execute()
        video_details.extend(response['items'])
    return video_details

def main():

    # Define the list of keywords you want to search for
    queries = ['asmr ambient', 'ambient asmr', 'asmr environment', 'ambience asmr', 'asmr background']

    # Get the number of pages to fetch for each keyword
    max_pages = int(input("Enter the number of pages to fetch for each query: "))

    # Loop over each keyword to perform the search and save results
    for query in queries:
        page_token = None
        all_videos = []
        for _ in range(max_pages):
            results, page_token = search_videos(query, page_token=page_token)
            all_videos.extend(results)
            
            if not page_token:
                break
        
        # Create a filename with the query and max_pages
        filename = f"{query.replace(' ', '_')}_pages_{max_pages}.json"
        
        # Save all retrieved videos to a JSON file
        save_to_json(all_videos, filename)
        
        print(f"Retrieved {len(all_videos)} videos for query '{query}' and saved to '{filename}'")

    # Load all saved JSON files and combine video IDs
    all_video_ids = []

    for query in queries:
        loadfile = f"{query.replace(' ', '_')}_pages_{max_pages}.json"
        
        # Load the JSON file
        with open(loadfile, 'r') as file:
            data = json.load(file)
        
        # Extract video IDs
        video_ids = [item['id']['videoId'] for item in data if 'videoId' in item['id']]
        
        print(f"Extracted {len(video_ids)} video IDs from '{loadfile}'.")
        
        all_video_ids.extend(video_ids)

    # Remove duplicate video IDs
    unique_video_ids = list(set(all_video_ids))
    print(f"Total unique video IDs after removing duplicates: {len(unique_video_ids)}")

    # Fetch video details for unique video IDs
    video_details = get_video_details(unique_video_ids)
    print(f"Retrieved details for {len(video_details)} unique videos.")

    # Save combined video details to a JSON file
    details_filename = f"combined_videos_info.json"
    save_to_json(video_details, details_filename)
    print(f"Saved video details to '{details_filename}'.")

    # Save unique video IDs
    with open('unique_video_ids.txt', 'w') as file:
        for item in unique_video_ids:
            file.write(f"{item}\n")

if __name__ == "__main__":
    main()
