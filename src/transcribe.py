import subprocess

import numpy as np
from faster_whisper import WhisperModel

_model = None


def get_model():
    global _model
    if _model is None:
        _model = WhisperModel("tiny", device="cpu", compute_type="int8")
    return _model


def _decode_with_ffmpeg(audio_path: str, sr: int = 16000) -> np.ndarray:
    """Decode any audio file to mono float32 using the system ffmpeg.

    This bypasses PyAV's av.open(), which fails on some Python versions
    (e.g. 3.14) on Streamlit Cloud.
    """
    cmd = [
        "ffmpeg", "-nostdin", "-threads", "0",
        "-i", audio_path,
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", str(sr),
        "-",
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError("ffmpeg failed: " + result.stderr.decode(errors="ignore")[-500:])
    return np.frombuffer(result.stdout, np.int16).astype(np.float32) / 32768.0


def transcribe_audio(audio_path: str, language: str = "en") -> str:
    model = get_model()
    audio = _decode_with_ffmpeg(audio_path)
    if audio.size == 0:
        return ""
    segments, _ = model.transcribe(audio, language=language)
    return " ".join(s.text.strip() for s in segments if s.text.strip())
