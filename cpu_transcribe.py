import logging
import whisper
import sys
import os
import tkinter as tk
from tkinter import filedialog

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select MP4 file to transcribe",
        filetypes=[("MP4 files", "*.mp4")]
    )
    return file_path

def get_whisper_model():
    model_name = input('Indicate the Whisper model to download (default: small): ') or 'small'
    logging.info(f"Downloading Whisper model: {model_name}")
    return whisper.load_model(model_name)

def main():
    logging.info("Please select your MP4 file")
    file_path = select_file()
    
    if not file_path:
        logging.error("No file was selected")
        return

    logging.info(f"Selected file: {file_path}")

    model = get_whisper_model()

    logging.info("Transcribing the video")
    result = model.transcribe(file_path)

    print("\nTranscription:")
    print(result["text"])

    # Save the transcription to a file
    output_file = os.path.splitext(file_path)[0] + "_transcription.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])
    logging.info(f"Transcription saved to {output_file}")

if __name__ == "__main__":
    main()