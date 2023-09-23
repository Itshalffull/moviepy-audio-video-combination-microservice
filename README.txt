# MoviePy Audio-Video Combiner Microservice

## Overview
This microservice allows users to combine audio and video files using MoviePy. It provides an API that takes the URLs of an audio file and a video file, combines them, and returns the combined video file.

## API Call and Response
### Endpoint
`POST /combine_audio_video`

### Parameters
- `API-Key`: The API key for authorization provided in the header.
- `audio_url`: The URL of the audio file provided in the JSON body.
- `video_url`: The URL of the video file provided in the JSON body.

### Example
```
curl -X POST "http://localhost:8080/combine_audio_video" \
     -H "API-Key: YourAPIKey" \
     -H "Content-Type: application/json" \
     -d '{"audio_url": "http://example.com/audio.mp3", "video_url": "http://example.com/video.mp4"}'
```

### Response
The API returns the combined video file in `video/mp4` format.

## API Docs
You can access the API documentation at `http://localhost:8080/apidocs`.

## Authentication
The default authentication method is API Key authentication. The API Key needs to be included in the `API-Key` header of the request.

## Logging
The microservice uses Python's logging module to log information, warnings, and errors to stderr.

## Installation on Cloud Run
1. Build the Docker image and push it to Container Registry or another container image repository.
2. Deploy the image to Cloud Run.
3. Set the `API_KEY` environment variable in the Cloud Run service to your desired API key.

## Technical Details and Explanation
The microservice uses the MoviePy library to combine audio and video files. It downloads the files from the provided URLs, processes them using MoviePy to combine the audio and video, and then returns the processed file.

### Audio and Video Combination
The combination of audio and video is done using the `CompositeAudioClip` class of MoviePy. The audio from the audio file replaces the original audio of the video file.

### Parameters
- `audio_url`: URL of the audio file. It should be a string representing a valid URL.
- `video_url`: URL of the video file. It should be a string representing a valid URL.