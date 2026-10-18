from dataclasses import dataclass

@dataclass(frozen=True)
class TranscriptWord:
    start:float
    end:float
    text:str

def words_from_segments(segments)->list[TranscriptWord]:
    words=[]
    
    for segment in segments:
        if segment.words is None:
            raise ValueError("Transcription requires word timestamps")
        for word in segment.words:
            text=word.word.strip()
            
            if text:
                words.append(
                    TranscriptWord(word.start,word.end,text)
                )
    return words

def matching_prefix_length(
    previous:list[TranscriptWord],
    current:list[TranscriptWord]
)->int:
    matched=0
    for previous_word,current_word in zip(previous,current):
        if previous_word.text!=current_word.text:
            break
        matched+=1
        
    return matched

class TranscriptState:
    def __init__(self):
        self.committed:list[TranscriptWord]=[]
        self.provisional:list[TranscriptWord]=[]
        
    def update(self,words:list[TranscriptWord])->list[TranscriptWord]:
        committed_count=len(self.committed)
        
        if matching_prefix_length(self.committed,words)!=committed_count:
            raise ValueError("new transcripts conflicts with committed words")
        pending=words[committed_count:]
        matched=matching_prefix_length(self.provisional,pending)
        newly_committed=pending[:matched]
        self.committed.extend(newly_committed)
        self.provisional=pending[matched:]
        return newly_committed