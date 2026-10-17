from math import isfinite
import numpy as np 
class AudioBuffer:
    def __init__(self,sample_rate:int=16000,max_seconds:float=30.0)->None:
        if sample_rate<=0:
            raise ValueError("sample rate must be positive")
        if(not isfinite(max_seconds) or max_seconds*sample_rate<1):
            raise ValueError("Buffer capacity must be finite and contain atleast one sample")
        self.sample_rate=sample_rate
        self.max_samples=int(max_seconds*sample_rate)
        self.samples=np.empty(0,dtype=np.float32)
    def append(self,chunk)->None:
        chunk=np.asarray(chunk,dtype=np.float32)
        if chunk.ndim!=1:
            raise ValueError("Audio must be a 1 dimensional mono array")
        if not np.isfinite(chunk).all():
            raise ValueError("Audio samples must be finite")
        if self.samples.size+chunk.size>self.max_samples:
            raise BufferError("Buffer capacity exceeded")
        self.samples=np.concatenate((self.samples,chunk))
    @property
    def duration_seconds(self)->float:
        return self.samples.size/self.sample_rate
        
    