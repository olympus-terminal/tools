#!/usr/bin/env python3
import argparse
import os
import tempfile
from TTS.api import TTS
from pydub import AudioSegment

def txt_to_audio(input_file, output_file, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
    # Read the text from the input file.
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading {input_file}: {e}")
        return

    # Initialize the TTS model from Coqui TTS.
    try:
        tts = TTS(model_name=model_name)
    except Exception as e:
        print(f"Error initializing TTS model '{model_name}': {e}")
        return

    # Check the desired output format by its file extension.
    _, ext = os.path.splitext(output_file)
    if ext.lower() == ".mp3":
        # Create a temporary WAV file to generate the speech.
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav_name = temp_wav.name

        try:
            print("Generating speech (temporary WAV)...")
            tts.tts_to_file(text=text, file_path=temp_wav_name)
        except Exception as e:
            print(f"Error generating speech audio: {e}")
            os.remove(temp_wav_name)
            return

        # Convert the temporary WAV file to MP3.
        try:
            print("Converting WAV to MP3...")
            sound = AudioSegment.from_wav(temp_wav_name)
            sound.export(output_file, format="mp3")
            print(f"Success: Audio saved as {output_file}")
        except Exception as e:
            print(f"Error converting WAV to MP3: {e}")
        finally:
            os.remove(temp_wav_name)
    else:
        # If the output file is not MP3, we assume a WAV (or other) file is desired.
        try:
            print("Generating speech directly to output file...")
            tts.tts_to_file(text=text, file_path=output_file)
            print(f"Success: Audio saved as {output_file}")
        except Exception as e:
            print(f"Error generating speech audio: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a .txt file to an audio file (MP3/WAV) using Coqui TTS."
    )
    parser.add_argument("input_file", help="Path to the input text file (e.g., input.txt)")
    parser.add_argument("output_file", help="Path for the output audio file (e.g., output.mp3 or output.wav)")
    parser.add_argument("--model", default="tts_models/en/ljspeech/tacotron2-DDC",
                        help="Coqui TTS model to use (default: tts_models/en/ljspeech/tacotron2-DDC)")

    args = parser.parse_args()
    txt_to_audio(args.input_file, args.output_file, args.model)
