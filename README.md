Here is an updated `README.md` that reflects the changes in your code, including the usage of command-line arguments:

```markdown
# CivitAI Image and Prompt Downloader

This Python script downloads images and their associated prompts from the CivitAI API for a specified model. It fetches images and saves both the images and prompts locally.

## Features
- Downloads images from the CivitAI API using a specified model ID.
- Saves images as `.jpg` and corresponding prompts as `.txt` files.
- Utilizes multi-threading for faster downloads (configurable via command-line arguments).

## Requirements
- Python 3.x
- `requests` library

## Installation

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv ./venv
   source ./venv/bin/activate
   ```

2. **Create a working directory:**
   ```bash
   mkdir civitai
   cd civitai
   ```

3. **Install required dependencies:**
   ```bash
   pip3 install requests
   pip3 install argparse
   ```

## Configuration

Before running the script, you will need:
1. A valid API key from [CivitAI](https://civitai.com/).
2. The model ID from which you want to download images.

These values are passed as command-line arguments when you run the script.

## Usage

### Command-line Arguments
- `--api_key`: (Required) Your CivitAI API key.
- `--model_id`: (Required) The model ID for the images you wish to download.

To run the script, execute the following command:

```bash
python3 main.py --api_key <your_civitai_api_key> --model_id <your_model_id>
```

### Example

```bash
python3 main.py --api_key abc123 --model_id 456def
```

The script will:
- Fetch image URLs and associated prompts from the CivitAI API.
- Save the images as `.jpg` files in the `./civitai_images/` directory.
- Save the prompts as `.txt` files in the same directory.

## Customization

- **Download Directory**: By default, images and prompts are saved in the `./civitai_images` directory. You can change this by modifying the `DOWNLOAD_DIR` variable in the script.
- **Maximum Concurrent Threads**: The script uses 10 threads by default for parallel downloads. You can adjust this by modifying the `MAX_WORKERS` variable in the script.

## Notes
- The script includes NSFW images by default. You can modify this behavior by adjusting the API request URL parameters.
- Ensure that your API key is valid and you are adhering to CivitAI's terms of service.

## License
This project is licensed under the MIT License.
```

This updated `README.md` includes instructions on how to run the script with the new argument parsing functionality, making it easier for users to provide their API key and model ID at runtime.