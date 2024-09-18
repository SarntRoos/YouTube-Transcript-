import os
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, TooManyRequests

# Function to extract video ID from the URL
def extract_video_id(video_url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.match(pattern, video_url)
    if match:
        return match.group(1)
    else:
        print("Invalid YouTube URL. Please enter a valid URL.")
        return None

# Function to get the transcript using the video ID
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except TranscriptsDisabled:
        print(f"Transcripts are disabled for video ID: {video_id}.")
        return None
    except TooManyRequests:
        print("Too many requests have been made to YouTube. Please wait and try again later.")
        return None
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {str(e)}")
        return None

# Function to validate the folder name
def is_valid_folder_name(folder):
    # Check for illegal characters in folder names for different operating systems
    if re.search(r'[<>:"/\\|?*]', folder):
        print("Invalid folder name. Please avoid using special characters.")
        return False
    return True

# Main function to prompt the user for input and run the program
def main():
    video_url = input("Enter the YouTube video URL: ")
    folder = input("Enter the folder name to save the JSON file: ")

    # Extract video ID from the URL
    video_id = extract_video_id(video_url)
    if video_id is None:
        return

    # Check if folder name is valid
    if not is_valid_folder_name(folder):
        return

    # Get transcript
    transcript = get_transcript(video_id)
    if transcript is None:
        return

    # Save transcript to JSON file
    save_to_json(transcript, folder, video_id)

# Function to iterate through the json file to extract the text from the transcript and save it as a new json making it easier to read
def save_to_json(transcript, folder, file_name):
    if not os.path.exists(folder):
        os.makedirs(folder)

    file_path = os.path.join(folder, f"{file_name}.json")
    if os.path.exists(file_path):
        overwrite = input(f"File {file_path} already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Aborted saving the transcript.")
            return

    # Concatenate all the "text" fields to make the transcript like a story/book format
    readable_transcript = " ".join([item["text"] for item in transcript])

    # Save the result into the JSON file in a more readable format
    with open(file_path, 'w') as json_file:
        json.dump({"transcript": readable_transcript}, json_file, indent=4)

    print(f"Transcript saved to {file_path}")


if __name__ == "__main__":
    main()
