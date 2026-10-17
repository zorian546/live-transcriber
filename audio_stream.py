from math import isfinite

def iter_audio_chunks(audio,sample_rate: int=16000,chunk_seconds:float=0.5):
    """Yields each chunks start time and audio samples."""
    if(sample_rate<=0):
        raise ValueError("sample rate must be positive")
    if (not isfinite(chunk_seconds) or sample_rate*chunk_seconds<1):
        raise ValueError("chunk duration must be finite and contain atleast one sample")
    
    chunk_samples=int((chunk_seconds*sample_rate))
    for start in range(0,len(audio),chunk_samples):
        yield(
            start/sample_rate,
            audio[start:start+chunk_samples],
        )