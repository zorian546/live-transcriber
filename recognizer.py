from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment
class SpeechRecognizer:
    """Transcribe decoded,mono audio sampled at 16 KHz"""
    def __init__(self):
        self.model=WhisperModel(
            "Systran/faster-whisper-base.en",
            revision="3d3d5dee26484f91867d81cb899cfcf72b96be6c",
            device="cpu",
            compute_type="int8"
        )
    
    def transcribe(self,audio)->list[Segment]:
        segments,_=self.model.transcribe(
            audio,
            language="en",
            beam_size=5,
            word_timestamps=True,
            condition_on_previous_text=True
        )
        return list(segments)