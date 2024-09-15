from flask import Flask, request, send_file, render_template_string, redirect, url_for, flash
import yt_dlp
import os
import io
import requests
from yt_dlp.utils import sanitize_filename  # Import sanitize function
import instaloader
import requests
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'  # Required for flashing messages

# Instaloader setup
loader = instaloader.Instaloader()

# Define the default download directory
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Home page (YouTube downloader)
@app.route('/')
@app.route('/youtube')
def youtube_page():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YouTube Video Downloader</title>
            <style>
                /* General styles for body with dark mode and purple gradient */
                body {
                    margin: 0;
                    padding: 0;
                    font-family: 'Roboto', sans-serif;
                    background: linear-gradient(135deg, #6A1B9A, #8E24AA);
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    text-align: center;
                }
                h1 {
                    font-size: 2.5em;
                    margin-bottom: 20px;
                }
                form {
                    background: rgba(0, 0, 0, 0.7);
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                }
                label, input, select {
                    font-size: 1.2em;
                }
                input[type="text"], select {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0 20px;
                    border: none;
                    border-radius: 5px;
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    transition: background 0.3s ease;
                }
                input[type="text"]:focus, select:focus {
                    background: rgba(255, 255, 255, 0.2);
                    outline: none;
                }
                button {
                    padding: 10px 20px;
                    font-size: 1.2em;
                    border: none;
                    border-radius: 5px;
                    background: #9C27B0;
                    color: white;
                    cursor: pointer;
                    transition: background 0.3s ease, transform 0.3s ease;
                }
                button:hover {
                    background: #AB47BC;
                    transform: translateY(-3px);
                }
                @media (max-width: 768px) {
                    h1 {
                        font-size: 2em;
                    }
                    form {
                        width: 90%;
                    }
                }

                nav {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    background: rgba(0, 0, 0, 0.6);
                    padding: 15px;
                    z-index: 100;
                }
                nav ul {
                    list-style: none;
                    margin: 0;
                    padding: 0;
                    display: flex;
                }
                nav ul li {
                    margin: 0 15px;
                }
                nav ul li a {
                    text-decoration: none;
                    color: white;
                    font-size: 1.2em;
                    padding: 8px 20px;
                    border-radius: 5px;
                    transition: background 0.3s ease;
                }
                nav ul li a.active {
                    background: #9C27B0;
                    color: #fff;
                }
                nav ul li a:hover {
                    background: #AB47BC;
                }
                select {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0 20px;
                    border: none;
                    border-radius: 5px;
                    background: rgba(255, 255, 255, 0.1); /* Background for the select box */
                    color: white; /* Text color */
                    transition: background 0.3s ease;
                }

                select:focus {
                    background: rgba(255, 255, 255, 0.2); /* Background on focus */
                    outline: none;
                }

                /* Set option text color in select dropdown */
                select option {
                    background: #6A1B9A; /* Dark background for options */
                    color: white; /* Text color for options */
                }

            </style>
        </head>
        <body>
            <nav>
                <ul>
                    <li><a href="{{ url_for('youtube_page') }}" class="active">YouTube</a></li>
                    <li><a href="{{ url_for('instagram_page') }}">Instagram</a></li>
                </ul>
            </nav>
            <div>
                <h1>YouTube Video Downloader</h1>
                <form action="/download" method="post">
                    <label for="video_url">YouTube Video URL:</label><br>
                    <input type="text" id="video_url" name="video_url" placeholder="Enter URL" required><br>
                    <label for="format">Choose format:</label><br>
                    <select id="format" name="format" required>
                        <option value="mp4">MP4 (Video)</option>
                        <option value="mp3">MP3 (Audio)</option>
                        <option value="wav">WAV (Audio)</option>
                    </select><br><br>
                    <button type="submit">Download</button>
                </form>
            </div>
        </body>
        </html>
    ''')

def login_to_instagram():
    username = "enter_your_username"
    password = "enter_your_password"
    try:
        loader.login(username, password)
    except Exception as e:
        print(f"Error logging in: {str(e)}")

# Instagram page (Instagram downloader)
@app.route('/instagram')
def instagram_page():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Instagram Downloader</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    font-family: 'Roboto', sans-serif;
                    background: linear-gradient(135deg, #6A1B9A, #8E24AA);
                    height: 100vh;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    color: white;
                    text-align: center;
                }
                h1 {
                    font-size: 2.5em;
                    margin-bottom: 20px;
                }
                form {
                    background: rgba(0, 0, 0, 0.7);
                    padding: 30px;
                    border-radius: 15px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                }
                label, input, select {
                    font-size: 1.2em;
                }
                input[type="text"], select {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0 20px;
                    border: none;
                    border-radius: 5px;
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    transition: background 0.3s ease;
                }
                input[type="text"]:focus, select:focus {
                    background: rgba(255, 255, 255, 0.2);
                    outline: none;
                }
                button {
                    padding: 10px 20px;
                    font-size: 1.2em;
                    border: none;
                    border-radius: 5px;
                    background: #9C27B0;
                    color: white;
                    cursor: pointer;
                    transition: background 0.3s ease, transform 0.3s ease;
                }
                button:hover {
                    background: #AB47BC;
                    transform: translateY(-3px);
                }
                @media (max-width: 768px) {
                    h1 {
                        font-size: 2em;
                    }
                    form {
                        width: 90%;
                    }
                }

                nav {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    display: flex;
                    justify-content: center;
                    background: rgba(0, 0, 0, 0.6);
                    padding: 15px;
                    z-index: 100;
                }
                nav ul {
                    list-style: none;
                    margin: 0;
                    padding: 0;
                    display: flex;
                }
                nav ul li {
                    margin: 0 15px;
                }
                nav ul li a {
                    text-decoration: none;
                    color: white;
                    font-size: 1.2em;
                    padding: 8px 20px;
                    border-radius: 5px;
                    transition: background 0.3s ease;
                }
                nav ul li a.active {
                    background: #9C27B0;
                    color: #fff;
                }
                nav ul li a:hover {
                    background: #AB47BC;
                }
                select {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0 20px;
                    border: none;
                    border-radius: 5px;
                    background: rgba(255, 255, 255, 0.1); /* Background for the select box */
                    color: white; /* Text color */
                    transition: background 0.3s ease;
                }

                select:focus {
                    background: rgba(255, 255, 255, 0.2); /* Background on focus */
                    outline: none;
                }

                /* Set option text color in select dropdown */
                select option {
                    background: #6A1B9A; /* Dark background for options */
                    color: white; /* Text color for options */
                }

            </style>
        </head>
        <body>
            <nav>
                <ul>
                    <li><a href="{{ url_for('youtube_page') }}">YouTube</a></li>
                    <li><a href="{{ url_for('instagram_page') }}" class="active">Instagram</a></li>
                </ul>
            </nav>
            <div>
                <h1>Instagram Downloader</h1>
                <form action="/download_instagram" method="post">
                    <label for="instagram_url">Instagram URL:</label><br>
                    <input type="text" id="instagram_url" name="instagram_url" placeholder="Enter URL" required><br>
                    <label for="type">Choose content type:</label><br>
                    <select id="type" name="type" required>
                        <option value="reels">Reels</option>
                        <! --<option value="stories">Stories</option>-->
                        <option value="posts">Posts</option>
                        <! --<option value="profile">Profile Picture</option>-->
                    </select><br><br>
                    <button type="submit">Download</button>
                </form>
            </div>
        </body>
        </html>
    ''')

# Download video or audio for YouTube
@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['video_url']
    format_type = request.form['format']

    download_dir = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'restrictfilenames': True,  # Prevent special characters
    }

    if format_type == 'mp4':
        ydl_opts.update({
            'format': 'bestvideo+bestaudio',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        })
    elif format_type == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    elif format_type == 'wav':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info_dict)

            if format_type in ['mp3', 'wav']:
                file_path = file_path.rsplit('.', 1)[0] + f'.{format_type}'

            if os.path.exists(file_path):
                flash(f"Download successful: {os.path.basename(file_path)}")
                return send_file(file_path, download_name=os.path.basename(file_path), as_attachment=True)
            else:
                flash("Error: File not found.")
                return redirect(url_for('youtube_page'))

    except Exception as e:
        flash(f"Error occurred: {str(e)}")
        return redirect(url_for('youtube_page'))

# Download for Instagram (Reels, Stories, Posts)
@app.route('/download_instagram', methods=['POST'])
def download_instagram():
    instagram_url = request.form['instagram_url']
    content_type = request.form['type']

    try:
        # Login to Instagram before fetching content (for stories)
        login_to_instagram()

        if content_type == 'profile':
            username = instagram_url.split('/')[-2]
            profile = instaloader.Profile.from_username(loader.context, username)
            profile_pic_url = profile.profile_pic_url_hd

            response = requests.get(profile_pic_url)
            if response.status_code == 200:
                return send_file(io.BytesIO(response.content), download_name='profile_picture.jpg', as_attachment=True)
            else:
                flash("Error: Unable to fetch profile picture.")
                return redirect(url_for('instagram_page'))

        elif content_type == 'posts':
            shortcode = instagram_url.split('/')[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            media_url = post.url  # Can be either an image or video URL
            
            response = requests.get(media_url)
            if response.status_code == 200:
                # Force the file to be downloaded as JPG regardless of the original extension
                return send_file(io.BytesIO(response.content), download_name='post.jpg', as_attachment=True)
            else:
                flash("Error: Unable to fetch post.")
                return redirect(url_for('instagram_page'))

        elif content_type == 'stories':
            username = instagram_url.split('/')[-2]
            profile = instaloader.Profile.from_username(loader.context, username)
            
            # Fetch the latest stories
            stories = loader.get_stories(userids=[profile.userid])
            for story in stories:
                for item in story.get_items():
                    media_url = item.url
                    response = requests.get(media_url)
                    if response.status_code == 200:
                        return send_file(io.BytesIO(response.content), download_name='story.mp4', as_attachment=True)
            flash("No stories found or unable to fetch stories.")
            return redirect(url_for('instagram_page'))

        elif content_type == 'reels':
            shortcode = instagram_url.split('/')[-2]
            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            if post.is_video:
                media_url = post.video_url
                response = requests.get(media_url)
                if response.status_code == 200:
                    return send_file(io.BytesIO(response.content), download_name='reel.mp4', as_attachment=True)
            else:
                flash("The URL provided does not point to a video reel.")
                return redirect(url_for('instagram_page'))

    except Exception as e:
        flash(f"Error occurred: {str(e)}")
        return redirect(url_for('instagram_page'))

if __name__ == '__main__':
    app.run(debug=True)