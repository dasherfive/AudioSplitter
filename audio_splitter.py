import os
import sys
import argparse
import logging
import shutil
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def check_ffmpeg():
    """Checks if ffmpeg is available. If not, tries to add known paths."""
    if shutil.which("ffmpeg"):
        return True
    
    # Common Winget install path pattern
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        winget_packages = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
        if winget_packages.exists():
            # Search for ffmpeg.exe in a depth-first manner to find the bin folder
            for path in winget_packages.rglob("ffmpeg.exe"):
                bin_dir = path.parent
                os.environ["PATH"] += os.pathsep + str(bin_dir)
                logging.info(f"[INFO] Added FFmpeg to PATH: {bin_dir}")
                return True
                
    return False

def process_file(file_path, args):
    try:
        logging.info(f"[INFO] Processing: {file_path.name}...")
        
        # Determine format
        file_ext = file_path.suffix.lower().replace('.', '')
        if file_ext not in ['mp3', 'wav', 'flac']:
            return # Should be filtered before, but safety check

        # Load Audio
        try:
            audio = AudioSegment.from_file(str(file_path), format=file_ext)
        except Exception as e:
            logging.error(f"[ERROR] File {file_path.name}: Failed to load. {e}")
            return

        # Split
        chunks = split_on_silence(
            audio,
            min_silence_len=args.min_silence_len,
            silence_thresh=args.silence_thresh,
            keep_silence=args.keep_silence
        )

        if len(chunks) < 2:
            logging.warning(f"[WARN] File {file_path.name}: 未偵測到足夠的靜音區段，跳過分割 (Chunks: {len(chunks)}).")
            return

        logging.info(f"[INFO] Found {len(chunks)} parts. Exporting...")

        # Create Output Directory
        output_dir = file_path.parent / file_path.stem
        try:
            output_dir.mkdir(exist_ok=True)
        except OSError as e:
            logging.error(f"[ERROR] Failed to create directory {output_dir}: {e}")
            return

        # Export
        for i, chunk in enumerate(chunks):
            # 01_filename.ext
            out_name = f"{i+1:02d}_{file_path.name}"
            out_path = output_dir / out_name
            
            try:
                chunk.export(out_path, format=file_ext)
            except Exception as e:
                 logging.error(f"[ERROR] Failed to export {out_name}: {e}")
        
        logging.info(f"[INFO] Done. Saved to {output_dir}")

    except Exception as e:
        logging.error(f"[ERROR] Unexpected error processing {file_path.name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Auto Audio Splitter")
    parser.add_argument("--input_dir", required=True, help="Target directory to scan")
    parser.add_argument("--silence_thresh", type=int, default=-40, help="Silence threshold in dBFS (default: -40)")
    parser.add_argument("--min_silence_len", type=int, default=1000, help="Minimum silence length in ms (default: 1000)")
    parser.add_argument("--keep_silence", type=int, default=500, help="Silence to keep in ms (default: 500)")
    
    args = parser.parse_args()

    # Check FFmpeg
    if not check_ffmpeg():
        logging.error("[FATAL] 未偵測到 ffmpeg，請確保已安裝並加入環境變數。")
        sys.exit(1)

    input_path = Path(args.input_dir)
    if not input_path.exists():
        logging.error(f"[FATAL] Input directory not found: {args.input_dir}")
        sys.exit(1)

    # Recursive scan
    audio_extensions = {'.mp3', '.wav', '.flac'}
    files = [p for p in input_path.rglob('*') if p.suffix.lower() in audio_extensions and p.is_file()]

    if not files:
        logging.warning(f"[WARN] No audio files found in {args.input_dir}")
        return

    logging.info(f"Found {len(files)} audio files in {args.input_dir}")

    for file_path in files:
        process_file(file_path, args)

if __name__ == "__main__":
    main()
