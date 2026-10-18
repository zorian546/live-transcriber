import argparse
from pathlib import Path
from av.error import FFmpegError
from faster_whisper import decode_audio
from recognizer import SpeechRecognizer
from time import perf_counter
from replay import iter_replay_updates

def main()->None:
    parser=argparse.ArgumentParser(
        description="Transcribe a local audio file "
    )
    parser.add_argument(
        "audio_path",
        type=Path,
        help="Path to audio recording "
    )
    parser.add_argument(
        "--replay",
        action="store_true",
        help="Show provisional transcript snapshots from accumulated audio"
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
    if args.replay and audio.size>30*16000:
        parser.error("Replay currently supports at most 30 seconds")
    
    print("loading speech model....")
    model_started=perf_counter()
    recognizer=SpeechRecognizer()
    model_seconds=perf_counter()-model_started
    if args.replay:
        print(f"Model setup: {model_seconds:.2f}s")
        
        for audio_seconds,segments in iter_replay_updates(audio,recognizer):
            text=" ".join(segment.text.strip() for segment in segments if segment.text.strip())
            print(f"\n[Provisional-{audio_seconds:.2f}s received]")
            print(text or "(no speech recognized)")
        return
    print("Transcribing")
    transcription_started=perf_counter()
    segments=recognizer.transcribe(audio)
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