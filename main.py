import os
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Directory where images and prompts will be saved
DOWNLOAD_DIR = './civitai_images'
# Number of parallel threads for downloading
MAX_WORKERS = 10

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Base URL for CivitAI API
BASE_URL = 'https://civitai.com/api/v1/images'

def download_images_with_prompts(model_id, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    # Request URL with the model ID and NSFW flag set to true
    url = f'{BASE_URL}?modelId={model_id}&limit=100&nsfw=true'
    
    image_data_list = []
    count = 0
    
    while url:
        print(f"Fetching from: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            break
        
        data = response.json()
        items = data.get('items', [])
        
        # Collect image URLs and prompts
        for item in items:
            image_url = item['url']
            prompt = item['meta']['prompt'] if 'meta' in item and 'prompt' in item['meta'] else "No prompt available"
            image_data_list.append((image_url, prompt, count))
            count += 1
        
        # Get the next page URL if available
        url = data.get('metadata', {}).get('nextPage', None)
    
    print(f"Downloading {len(image_data_list)} images and saving prompts...")
    download_images_parallel(image_data_list)
    print("All images and prompts downloaded.")

def download_images_parallel(image_data_list):
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_image_and_prompt, url, prompt, index) for url, prompt, index in image_data_list]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error downloading image or saving prompt: {e}")

def download_image_and_prompt(url, prompt, index):
    # Save image
    image_path = os.path.join(DOWNLOAD_DIR, f'{index}.jpg')
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded {image_path}")
    else:
        print(f"Failed to download image from {url}")

    # Save prompt as a text file
    prompt_path = os.path.join(DOWNLOAD_DIR, f'{index}.txt')
    with open(prompt_path, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f"Saved prompt to {prompt_path}")

if __name__ == "__main__":
    # Setting up argument parser
    parser = argparse.ArgumentParser(description="Download images and prompts from CivitAI model.")
    parser.add_argument('--api_key', type=str, required=True, help="Your CivitAI API key.")
    parser.add_argument('--model_id', type=str, required=True, help="The model ID from which to download images and prompts.")
    
    args = parser.parse_args()

    # Pass the API key and Model ID from the arguments
    download_images_with_prompts(args.model_id, args.api_key)
