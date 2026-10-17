from audio_buffer import AudioBuffer
from audio_stream import iter_audio_chunks

def iter_replay_updates(audio,recognizer):
    """Yield(audio duration,segments ) for mono audio at 16KHz"""
    buffer=AudioBuffer()
    update_samples=2*buffer.sample_rate
    last_processed_samples=0
    
    if len(audio)==0:
        raise ValueError("Replay requires non empty audio")
    if len(audio)>buffer.max_samples:
        raise ValueError("Replay currently supports at most 30 seconds")
    for _,chunk in iter_audio_chunks(audio):
        buffer.append(chunk)
        
        if buffer.samples.size-last_processed_samples>=update_samples:
            segments=recognizer.transcribe(buffer.samples)
            last_processed_samples=buffer.samples.size
            yield buffer.duration_seconds,segments
            
    if buffer.samples.size>last_processed_samples:
        segments=recognizer.transcribe(buffer.samples)
        yield buffer.duration_seconds,segments