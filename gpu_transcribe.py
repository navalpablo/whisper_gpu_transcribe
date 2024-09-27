import logging
import sys
import os
import tkinter as tk
from tkinter import filedialog
import whisper
import torch
import subprocess

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Specify the path to FFmpeg executable
FFMPEG_PATH = r"C:\path\to\ffmpeg.exe"  # Update this path

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select MP4 file to transcribe",
        filetypes=[("MP4 files", "*.mp4")]
    )
    return file_path

def get_whisper_model():
    model_name = input('Indicate the Whisper model to download (default: small): ') or 'small'
    logging.info(f"Downloading Whisper model: {model_name}")
    return whisper.load_model(model_name, device="cuda")

def main():
    # Check for CUDA availability
    if not torch.cuda.is_available():
        logging.warning("CUDA is not available. Falling back to CPU.")
        device = "cpu"
    else:
        device = "cuda"
        logging.info(f"Using GPU: {torch.cuda.get_device_name(0)}")

    logging.info("Please select your MP4 file")
    file_path = select_file()
    
    if not file_path:
        logging.error("No file was selected")
        return

    logging.info(f"Selected file: {file_path}")

    model = get_whisper_model()

    logging.info("Transcribing the video")
    
    # Set the FFMPEG_BINARY environment variable
    os.environ["FFMPEG_BINARY"] = FFMPEG_PATH

    try:
        result = model.transcribe(file_path, fp16=False)  # Disable fp16 for now
        print("\nTranscription:")
        print(result["text"])

        # Save the transcription to a file
        output_file = os.path.splitext(file_path)[0] + "_transcription.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result["text"])
        logging.info(f"Transcription saved to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred during transcription: {str(e)}")
        logging.info("Attempting to run FFmpeg directly to check for issues...")
        try:
            subprocess.run([FFMPEG_PATH, "-version"], check=True, capture_output=True)
            logging.info("FFmpeg is working correctly. The issue might be with the input file or Whisper library.")
        except subprocess.CalledProcessError as ffmpeg_error:
            logging.error(f"FFmpeg error: {ffmpeg_error}")
        except FileNotFoundError:
            logging.error(f"FFmpeg not found at the specified path: {FFMPEG_PATH}")

if __name__ == "__main__":
    main()