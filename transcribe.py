import argparse
from pathlib import Path
from av.error import FFmpegError
from faster_whisper import decode_audio

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
    
    
if __name__=="__main__":
    main()