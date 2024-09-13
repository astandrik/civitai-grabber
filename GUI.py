import os
import requests
from tkinter import Tk, Label, Entry, Button, StringVar, Text, Scrollbar, messagebox, ttk, BooleanVar, Checkbutton
from tkinter.constants import END, RIGHT, Y
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Directory where images and prompts will be saved
DOWNLOAD_DIR = './civitai_images'
MAX_WORKERS = 100  # Number of parallel threads for downloading

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

BASE_URL = 'https://civitai.com/api/v1/images'


def log_message(message):
    log_area.config(state="normal")
    log_area.insert(END, message + '\n')
    log_area.yview(END)
    log_area.config(state="disabled")


def update_progress(current, total):
    progress['value'] = (current / total) * 100
    progress_label.config(text=f"Progress: {current}/{total} images")


def download_images_with_prompts(api_key, model_id, save_prompts):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    url = f'{BASE_URL}?modelId={model_id}&limit=100&nsfw=true'
    image_data_list = []
    count = 0
    total_images = 0

    while url:
        log_message(f"Fetching from: {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            log_message(f"Error: Failed to retrieve data: {
                        response.status_code}")
            messagebox.showerror("Error", f"Failed to retrieve data: {
                                 response.status_code}")
            break

        data = response.json()
        items = data.get('items', [])

        for item in items:
            image_url = item['url']
            prompt = item['meta']['prompt'] if 'meta' in item and 'prompt' in item['meta'] else "No prompt available"
            if save_prompts:
                image_data_list.append((image_url, prompt, count))
            else:
                image_data_list.append((image_url, None, count))
            count += 1

        total_images += len(items)
        url = data.get('metadata', {}).get('nextPage', None)

    if total_images == 0:
        messagebox.showinfo("No Images", "No images found for this model.")
        return

    log_message(f"Downloading {total_images} images{
                ' and prompts' if save_prompts else ''}...")
    download_images_parallel(image_data_list, total_images, save_prompts)
    messagebox.showinfo("Success", "All images downloaded successfully!")


def download_images_parallel(image_data_list, total_images, save_prompts):
    completed = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_image_and_prompt, url, prompt, index, save_prompts)
                   for url, prompt, index in image_data_list]
        for future in as_completed(futures):
            try:
                future.result()
                completed += 1
                update_progress(completed, total_images)
            except Exception as e:
                log_message(f"Error downloading image or saving prompt: {e}")
                messagebox.showerror(
                    "Error", f"Error downloading image or saving prompt: {e}")


def download_image_and_prompt(url, prompt, index, save_prompts):
    image_path = os.path.join(DOWNLOAD_DIR, f'{index}.jpg')
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        log_message(f"Downloaded {image_path}")
    else:
        log_message(f"Failed to download image from {url}")

    if save_prompts and prompt is not None:
        prompt_path = os.path.join(DOWNLOAD_DIR, f'{index}.txt')
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        log_message(f"Saved prompt to {prompt_path}")

# GUI Function


def start_download():
    api_key = api_key_var.get()
    model_id = model_id_var.get()
    save_prompts = save_prompts_var.get()

    if not api_key or not model_id:
        messagebox.showerror(
            "Error", "Please enter both API Key and Model ID!")
        return

    # Reset progress bar and label
    progress['value'] = 0
    progress_label.config(text="Progress: 0/0 images")

    # Run the download task in a separate thread to keep the GUI responsive
    download_thread = threading.Thread(
        target=download_images_with_prompts, args=(api_key, model_id, save_prompts))
    download_thread.start()


# GUI Setup
root = Tk()
root.title("CivitAI Image Downloader")

# API Key input
Label(root, text="API Key:").grid(row=0, column=0, padx=10, pady=10)
api_key_var = StringVar()
Entry(root, textvariable=api_key_var, width=40).grid(
    row=0, column=1, padx=10, pady=10)

# Model ID input
Label(root, text="Model ID:").grid(row=1, column=0, padx=10, pady=10)
model_id_var = StringVar()
Entry(root, textvariable=model_id_var, width=40).grid(
    row=1, column=1, padx=10, pady=10)

# Checkbox for saving prompts
save_prompts_var = BooleanVar(value=True)  # Default is to save prompts
Checkbutton(root, text="Save Prompts", variable=save_prompts_var).grid(
    row=2, column=1, padx=10, pady=10, sticky='w')

# Download Button
Button(root, text="Download Images", command=start_download).grid(
    row=3, columnspan=2, pady=20)

# Progress Bar
progress = ttk.Progressbar(root, orient="horizontal",
                           length=300, mode="determinate")
progress.grid(row=4, column=0, columnspan=2, pady=10)
progress_label = Label(root, text="Progress: 0/0 images")
progress_label.grid(row=5, column=0, columnspan=2)

# Log Area
log_area = Text(root, height=10, width=60, state="disabled")
log_area.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Scrollbar for Log Area
scrollbar = Scrollbar(root, command=log_area.yview)
scrollbar.grid(row=6, column=2, sticky="nsew")
log_area['yscrollcommand'] = scrollbar.set

# Run the GUI loop
root.mainloop()
