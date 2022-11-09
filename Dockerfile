FROM python:3.9.13-slim-bullseye

WORKDIR /app

COPY . /app/
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install git+https://github.com/openai/whisper.git && pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:80", "--workers", "4", "--keep-alive", "7200", "-t", "7200"]