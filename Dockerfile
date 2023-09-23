FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install ffmpeg and ImageMagick
RUN apt-get update &&     apt-get install -y ffmpeg imagemagick &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*

COPY app.py .
COPY swagger.yaml .

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-t", "2400", "app:app"]
