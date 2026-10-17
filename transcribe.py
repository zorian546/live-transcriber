import argparse
from pathlib import Path
from av.error import FFmpegError
from faster_whisper import WhisperModel,decode_audio
from time import perf_counter

def main()->None:
    parser=argparse.ArgumentParser(
        description="Transcribe a local audio file "
    )
    parser.add_argument(
        "audio_path",
        type=Path,
        help="Path to audio recording "
    )
    args=parser.parse_args()
    if not args.audio_path.is_file():
        parser.error(f"file not found: {args.audio_path}")
    try:
        audio=decode_audio(
            str(args.audio_path),
            sampling_rate=16000
        )
    except (FFmpegError,ValueError,IndexError,OSError) as error:
        parser.error(f"cannot decode audio: {error}")
        
    if audio.size==0:
        parser.error("the input contains no audio samples")
    print(f"audio decoded successfully: {audio.size} samples")
    
    print("loading speech model....")
    model_started=perf_counter()
    model=WhisperModel(
        "Systran/faster-whisper-base.en",
        revision="3d3d5dee26484f91867d81cb899cfcf72b96be6c",
        device="cpu",
        compute_type="int8"
    )
    model_seconds=perf_counter()-model_started
    print("Transcribing")
    transcription_started=perf_counter()
    segments,_=model.transcribe(
        audio,
        language="en",
        beam_size=5,
        word_timestamps=True,
        condition_on_previous_text=True
    )    
    segments=list(segments)
    transcription_seconds=perf_counter()-transcription_started
    
    found_text=False
    for segment in segments:
        text=segment.text.strip()
        if text:
            found_text=True
            print(
                f"[{segment.start: .2f}s-{segment.end: .2f}s] "
                f"{text}"
            )
    if not found_text:
        print("no speech recognized.")
    audio_seconds=audio.size/16000
    rtf=transcription_seconds/audio_seconds
    print(f"Audio duration: {audio_seconds:.2f}s")
    print(f"Model setup: {model_seconds:.2f}s")
    print(f"Transcription: {transcription_seconds:.2f}s")
    print(f"Offline real-time factor: {rtf:.3f}")
    
if __name__=="__main__":
    main()