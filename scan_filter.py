import string
import sys

# Windows size
WINDOW_SIZE = 100

# Get the input and output filenames from the command line arguments
input_filename = sys.argv[1]
output_filename = sys.argv[2]

# Read the file
with open(input_filename, 'r') as file:
    text = file.read()

# Remove punctuation
text = text.translate(str.maketrans('', '', string.punctuation))

# Iterate over each window of WINDOW_SIZE characters
new_text = ''
for i in range(0, len(text), WINDOW_SIZE):
    window = text[i:i+WINDOW_SIZE]

    # Count numeric and non-numeric characters
    numbers = sum(c.isdigit() for c in window)
    non_numbers = sum(c.isalpha() for c in window)

    # If less than 80% of the window is numbers,
    # include it in the new text
    if numbers < 0.8 * (numbers + non_numbers):
        new_text += window

# Write the result back to the file
with open(output_filename, 'w') as file:
    file.write(new_text)
