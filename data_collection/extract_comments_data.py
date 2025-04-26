import json
import pandas as pd
import os

# Function to extract comments from a JSON file
def extract_comments_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    comments_data = []
    for item in data:
        video_id = item['snippet']['videoId']
        top_comment = item['snippet']['topLevelComment']
        top_comment_id = top_comment['id']
        top_comment_like_count = top_comment['snippet']['likeCount']
        top_comment_text = top_comment['snippet']['textOriginal']
        
        # Add top comment
        comments_data.append({
            'videoId': video_id,
            'commentId': top_comment_id,
            'likeCount': top_comment_like_count,
            'isTopComment': 1,
            'isReply': 0,
            'parentId': None,
            'textOriginal': top_comment_text
        })
        
        # Add replies if any
        if 'replies' in item:
            for reply in item['replies']['comments']:
                reply_id = reply['id']
                reply_like_count = reply['snippet']['likeCount']
                reply_text = reply['snippet']['textOriginal']
                comments_data.append({
                    'videoId': video_id,
                    'commentId': reply_id,
                    'likeCount': reply_like_count,
                    'isTopComment': 0,
                    'isReply': 1,
                    'parentId': top_comment_id,
                    'textOriginal': reply_text
                })
    
    return comments_data

def main():

    # Directory containing the JSON files
    directory = 'comments_json'

    # List to hold all comments data
    all_comments_data = []

    # Iterate over each JSON file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            comments_data = extract_comments_from_file(file_path)
            all_comments_data.extend(comments_data)

    # Convert to a DataFrame
    df = pd.DataFrame(all_comments_data)

    # Save to a CSV file (Define the file name)
    df.to_csv('[file_name].csv', index=False)

    print("The comments have been successfully extracted and saved.")

if __name__ == "__main__":
    main()
