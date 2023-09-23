import os
import requests
import logging
import sys
import tempfile
import shutil
from flask import Flask, request, jsonify, send_file
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError, UnsupportedMediaType
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger()

API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("No API_KEY set for Flask application")

def download_file(url, target_folder):
    local_filename = os.path.join(target_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

@app.route('/combine_audio_video', methods=['POST'])
@swag_from('swagger.yaml')
def combine_audio_video():
    if request.headers.get('API-Key') != API_KEY:
        raise Unauthorized("Invalid API Key")
    request_data = None
    if request.content_type == 'application/json':
        request_data = request.get_json()
    else:
        raise UnsupportedMediaType("Content type must be 'application/json'")
    if not request_data:
        raise BadRequest("Empty JSON received")
    if 'audio_url' not in request_data or 'video_url' not in request_data:
        raise BadRequest("Both audio and video URLs must be provided")

    audio_url = request_data['audio_url']
    video_url = request_data['video_url']

    temp_dir = tempfile.mkdtemp()
    try:
        logger.info(f"Temporary directory: {temp_dir}")

        audio_file = download_file(audio_url, temp_dir)
        video_file = download_file(video_url, temp_dir)

        audioclip = AudioFileClip(audio_file)
        videoclip = VideoFileClip(video_file)

        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip

        output_filename = os.path.join(temp_dir, "output.mp4")
        videoclip.write_videofile(output_filename)

        return send_file(output_filename, as_attachment=True, download_name="output.mp4")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise InternalServerError(f"An error occurred: {str(e)}")

    finally:
        shutil.rmtree(temp_dir)

@app.after_request
def after_request(response):
    logger.info('%s - %s - %s - %s - %s',
                request.remote_addr,
                request.method,
                request.scheme,
                request.full_path,
                response.status)
    if response.content_length == 0:
        logger.warning("No content returned in response")
    return response

if __name__ == '__main__':
    port = os.getenv('PORT', 8080)
    app.run(debug=True, host='0.0.0.0', port=int(port))
