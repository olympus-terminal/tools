import sys

def break_sequence_into_lines(input_file, line_length=100):
  """
  Breaks a single-line sequence in a FASTA file into lines of a specified length.

  Args:
    input_file: The path to the input FASTA file.
    line_length: The desired length of each line (default is 100).
  """
  output_file = f"{input_file}.wrapped"
  with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    sequence = infile.read().strip()  # Read entire sequence as a single string
    for i in range(0, len(sequence), line_length):
      outfile.write(sequence[i:i+line_length] + "\n")

# Check if input file is provided as sys.argv[1]
if len(sys.argv) > 1:
  input_file = sys.argv[1]
  break_sequence_into_lines(input_file)
else:
  print("Error: Please provide the input FASTA file as a command-line argument.")
