# Flask Video and Audio Downloader

This is a Flask-based web application that allows users to download videos and audio from YouTube, as well as media from Instagram. 

## Features

- **YouTube Downloader**: Download videos or extract audio from YouTube in various formats (MP4, MP3, WAV).
- **Instagram Downloader**: Download posts, reels, and profile pictures from Instagram.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/ayushsalunkhe/youtube-and-instagram-downloader.git
    cd youtube-and-instagram-downloader
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

    Replace `your_instagram_username` and `your_instagram_password` with your Instagram credentials.

## Usage

1. Start the Flask development server:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/` for the YouTube downloader or `http://127.0.0.1:5000/instagram` for the Instagram downloader.

3. **YouTube Downloader**:
    - Enter the YouTube video URL.
    - Choose the format (MP4, MP3, WAV).
    - Click "Download".

4. **Instagram Downloader**:
    - Enter the Instagram post, reel URL.
    - Choose the content type (Posts, Reels).
    - Click "Download".

## Requirements

To ensure you have all necessary packages, create a `requirements.txt` file with:

```bash
pip freeze > requirements.txt
