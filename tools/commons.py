from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field, conint
import os
import hashlib
import requests

class ServeReferenceAudio(BaseModel):
    audio: bytes
    text: str

class RoServeRefereceAudio(BaseModel):
    audio_url: str
    prompt_text: str

    def check_prompt_audio_url(self):
        md5_hash = hashlib.md5(self.audio_url.encode()).hexdigest()
        local_dir = "AudioSamples"
        os.makedirs(local_dir, exist_ok=True)
        file_path = os.path.join(local_dir, f"{md5_hash}.wav")
        if os.path.exists(file_path):
            return file_path
        # 如果文件不存在,下载并保存
        try:
            # 下载文件
            response = requests.get(self.audio_url)
            response.raise_for_status()  # 如果请求失败,将引发异常
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return file_path
        except Exception as e:
            print(f"下载或保存文件时发生错误: {e}")
            return None

class ServeTTSRequest(BaseModel):
    text: str
    chunk_length: Annotated[int, conint(ge=100, le=300, strict=True)] = 200
    # Audio format
    format: Literal["wav", "pcm", "mp3"] = "mp3"
    mp3_bitrate: Literal[64, 128, 192] = 128
    # References audios for in-context learning
    references: list[ServeReferenceAudio] = []
    # for rochat reference
    ro_references: Optional[RoServeRefereceAudio] = None
    # Reference id
    # For example, if you want use https://fish.audio/m/7f92f8afb8ec43bf81429cc1c9199cb1/
    # Just pass 7f92f8afb8ec43bf81429cc1c9199cb1
    reference_id: str | None = None
    # Normalize text for en & zh, this increase stability for numbers
    normalize: bool = True
    mp3_bitrate: Optional[int] = 64
    opus_bitrate: Optional[int] = -1000
    # Balance mode will reduce latency to 300ms, but may decrease stability
    latency: Literal["normal", "balanced"] = "normal"
    # not usually used below
    streaming: bool = False
    emotion: Optional[str] = None
    max_new_tokens: int = 1024
    top_p: Annotated[float, Field(ge=0.1, le=1.0, strict=True)] = 0.7
    repetition_penalty: Annotated[float, Field(ge=0.9, le=2.0, strict=True)] = 1.2
    temperature: Annotated[float, Field(ge=0.1, le=1.0, strict=True)] = 0.7
