import whisper
from urllib.request import Request
from fastapi import FastAPI, Request, HTTPException
from models import Item
from utils import get_image_from_url


def initialize():
    app = FastAPI()
    model = whisper.load_model("medium")

    return app, model


app, model = initialize()


@app.post('/speech-to-text')
def text_similarity(request: Request, item: Item):
    """ 
    Get speech to text
    """
    # validate if responses are empty
    if item.audio_source == '':
        raise HTTPException(
            status_code=400, detail="Invalid responses provided, the responses mustn't be empty")
    filename = get_image_from_url(item.audio_source)

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    return {"text": result.text, "lang_detected": max(probs, key=probs.get)}
