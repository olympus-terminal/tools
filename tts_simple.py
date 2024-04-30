import sys
import os
from gtts import gTTS
from playsound import playsound

def generate_mp3(input_filepath):
    # Read the input text from the file
    with open(input_filepath, 'r') as file:
        text = file.read()

    # Define the output file name by replacing '.txt' with '.mp3'
    output_filepath = input_filepath.replace('.txt', '.mp3')

    # Use gTTS to convert text to mp3 and save it
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_filepath)

    # Play the sound
   # playsound(output_filepath)

# Main function to check arguments and call generate_mp3 if appropriate
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script_name.py file_path")
    else:
        input_file = sys.argv[1]
        if not input_file.endswith('.txt'):
            print("Error: The input file should have a '.txt' extension")
        else:
            generate_mp3(input_file)
