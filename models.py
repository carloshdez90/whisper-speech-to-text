from pydantic import BaseModel


class Item(BaseModel):
    audio_source: str
