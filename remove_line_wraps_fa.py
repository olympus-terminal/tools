import sys

def remove_line_wrapping(input_file):
  """
  Removes line wrapping from a FASTA file.

  Args:
    input_file: The path to the input FASTA file.
  """
  output_file = f"{input_file}.unwrapped"  # Create output filename based on input
  with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    sequence = False
    for line in infile:
      # Check for header line
      if line.startswith('>'):
        outfile.write(line)
        sequence = True
      # Append sequence lines without newline
      elif sequence:
        outfile.write(line.strip())
      else:
        print("Warning: Unexpected line found before first sequence entry.")

# Check if input file is provided as sys.argv[1]
if len(sys.argv) > 1:
  input_file = sys.argv[1]
  remove_line_wrapping(input_file)
else:
  print("Error: Please provide the input FASTA file as a command-line argument.")
