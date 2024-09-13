# CivitAI Image and Prompt Downloader

This Python script allows users to download images and associated prompts from the CivitAI API for a specified model, with both a **command-line interface (CLI)** and a **graphical user interface (GUI)**.

## Features

- Download images and prompts for any model hosted on CivitAI.
- **CLI** for advanced users who prefer terminal-based operations.
- **GUI** for ease of use, with a progress bar and real-time logging.
- Images are saved in `.jpg` format and prompts in `.txt`.
- Multi-threading support for faster downloads, configurable in the script.

## Requirements

- Python 3.x
- Required libraries:
  - `requests`
  - `argparse` (for CLI)
  - `tkinter` (for GUI)
  - `concurrent.futures` (for multi-threading)

## Installation

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv ./venv
   source ./venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install requests argparse
   ```

3. **(Optiona) GUI**
    To install tinker that is used for interface 

    ### Installing Tkinter on Different Platforms

    #### 1. **Windows**
    Tkinter is pre-installed with Python on Windows. Verify by importing in Python:
    ```bash
    import tkinter
    ```
    If not installed, run:
    ```bash
    pip install tk
    ```

    #### 2. **macOS**
    Tkinter is generally pre-installed. If needed, install via Homebrew:
    ```bash
    brew install python-tk
    ```
    Or use pip:
    ```bash
    pip install tk
    ```

    #### 3. **Linux (Ubuntu/Debian)**
    Install Tkinter using:
    ```bash
    sudo apt-get install python3-tk
    ```

    #### 4. **Other Linux Distributions**
    For Fedora:
    ```bash
    sudo dnf install python3-tkinter
    ```
    For Arch Linux:
    ```bash
    sudo pacman -S tk
    ```

## Configuration

Before running the script, you need:
1. A valid API key from [CivitAI](https://civitai.com/).
2. The model ID of the model whose images you want to download.

These values are passed as command-line arguments in the CLI or entered directly in the GUI.

## Usage

### 1. Command-Line Interface (CLI)

#### Command-Line Arguments:

- `--api_key`: (Required) Your CivitAI API key.
- `--model_id`: (Required) The model ID for the images you wish to download.

#### Example:

To download images and prompts from a specific model:

```bash
python3 main.py --api_key <your_civitai_api_key> --model_id <your_model_id>
```

This command will:
- Download the images and associated prompts.
- Save them in the default directory: `./civitai_images/`.

### 2. Graphical User Interface (GUI)

For users who prefer a more interactive experience, the GUI provides a simple form to input the API key and model ID. It also includes:
- **Progress bar**: Displays real-time download progress.
- **Log area**: Shows a detailed log of downloads and errors.

#### To start the GUI:

```bash
python3 GUI.py
```

Once the window opens:
1. Enter your CivitAI API key.
2. Enter the model ID.
3. Click **Download Images**.

The images and prompts will be saved in the same `./civitai_images/` directory.

## Customization

- **Download Directory**: By default, the images and prompts are saved in the `./civitai_images` directory. You can modify the `DOWNLOAD_DIR` variable in the script to change the save location.
- **Multi-threading**: The script uses 10 concurrent threads by default for faster downloads. You can adjust the number of threads by modifying the `MAX_WORKERS` variable in the script.

## Notes

- **NSFW Images**: The script downloads NSFW images by default. You can control this by modifying the API request parameters in the script.
- Ensure that your API key is valid and you are adhering to [CivitAI's terms of service](https://civitai.com/terms).

## License

This project is licensed under the MIT License.
