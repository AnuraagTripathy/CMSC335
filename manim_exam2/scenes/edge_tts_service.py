"""manim-voiceover SpeechService backed by edge-tts (free Microsoft neural voices)."""
import asyncio
import time
from pathlib import Path

import edge_tts
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService, initialize_speech_service


class EdgeTTSService(SpeechService):
    def __init__(self, voice="en-US-AndrewNeural", rate="+0%", **kwargs):
        initialize_speech_service(self, kwargs)
        self.voice, self.rate = voice, rate

    def generate_from_text(self, text, cache_dir=None, path=None, **kwargs):
        cache_dir = cache_dir or self.cache_dir
        input_text = remove_bookmarks(text)
        input_data = {"input_text": input_text, "service": "edge_tts", "voice": self.voice, "rate": self.rate}
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached
        audio_path = str(path) if path else self.get_audio_basename(input_data) + ".mp3"
        for attempt in range(10):  # the free endpoint occasionally drops a request; retry with backoff
            try:
                comm = edge_tts.Communicate(input_text, self.voice, rate=self.rate)
                asyncio.run(comm.save(str(Path(cache_dir) / audio_path)))
                break
            except (edge_tts.exceptions.NoAudioReceived, edge_tts.exceptions.WebSocketError, OSError):
                if attempt == 9:
                    raise
                time.sleep(min(30, 3 * (attempt + 1)))
        return {"input_text": text, "input_data": input_data, "original_audio": audio_path}
