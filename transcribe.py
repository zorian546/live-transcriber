import argparse
from pathlib import Path

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
    print(f"selected input: {args.audio_path}")
    
if __name__=="__main__":
    main()