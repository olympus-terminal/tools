# Command-Line Tools

General-purpose command-line utilities for data processing, file management, and system administration.

[![License](https://img.shields.io/github/license/olympus-terminal/tools)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/olympus-terminal/tools?style=social)](https://github.com/olympus-terminal/tools/stargazers)
[![Tools](https://img.shields.io/badge/tools-36-green.svg)](https://github.com/olympus-terminal/tools)

## Overview

A collection of practical command-line utilities for common tasks in data processing, file operations, and system management. These tools are designed to be simple, efficient, and composable with standard Unix workflows.

## Quick Start

```bash
# Clone repository
git clone https://github.com/olympus-terminal/tools.git
cd tools

# Make scripts executable
chmod +x *.sh *.py *.pl

# Add to PATH (optional)
export PATH="$PATH:$(pwd)"
```

## Tool Categories

### Data Processing

**break-to-100s.py** - Split data into chunks of 100 entries
```bash
python break-to-100s.py large_dataset.txt
```

**delim_to_tab_UTF8** - Convert any delimiter to tab-separated values
```bash
./delim_to_tab_UTF8 < data.csv > data.tsv
```

**only_alpha** - Extract only alphabetic characters from input
```bash
./only_alpha < mixed_text.txt > letters_only.txt
```

**get_IDs** - Extract IDs from formatted text
```bash
./get_IDs input_file.txt > ids.txt
```

### File Management

**move_large_files.sh** - Efficiently move large files with progress
```bash
./move_large_files.sh /source/dir /dest/dir "*.bam"
```

**osxrename.pl** - Perl-based batch file renaming (macOS compatible)
```bash
./osxrename.pl 's/old_pattern/new_pattern/g' *.txt
```

**filter_ckpts.sh** - Filter and manage checkpoint files
```bash
./filter_ckpts.sh checkpoints/ --keep-every 10
```

**opposite_day.sh** - Reverse file selection logic
```bash
./opposite_day.sh pattern files/
```

### Text & Document Processing

**pdf_to_txt_argv.py** - Convert PDF files to plain text
```bash
python pdf_to_txt_argv.py document.pdf output.txt
```

**mp3xtractr.py** - Extract metadata from MP3 files
```bash
python mp3xtractr.py music_library/ > metadata.csv
```

**neural_tts.py** - Text-to-speech synthesis utility
```bash
python neural_tts.py "Text to convert to speech" output.wav
```

### System Administration

**CatchAndSlot.sh** - Execute commands with proper error handling
```bash
./CatchAndSlot.sh long_running_command
```

**distribute_ex.sh** - Distribute files across multiple systems
```bash
./distribute_ex.sh file_list.txt server1 server2 server3
```

**clone_imprint_distribute** - Clone and distribute configurations
```bash
./clone_imprint_distribute template/ target_systems.txt
```

**download-update.sh** - Automated download and update script
```bash
./download-update.sh package_name
```

### Archive & Compression

**extract_zip_having_dups.sh** - Extract ZIP files with duplicate handling
```bash
./extract_zip_having_dups.sh archive.zip output_dir/
```

**force_unzip.sh** - Force extraction of damaged archives
```bash
./force_unzip.sh corrupted.zip output_dir/
```

### Data Transfer & Sync

**optimized_rsync.sh** - Rsync wrapper with optimization
```bash
./optimized_rsync.sh /source/dir/ user@host:/dest/dir/
```

### Bioinformatics

**getFromNCBI-gene.py** - Fetch gene data from NCBI
```bash
python getFromNCBI-gene.py gene_list.txt > gene_data.txt
```

**cid_make_unitigs** - Process unitigs from assembly
```bash
./cid_make_unitigs assembly.fa > unitigs.fa
```

**interleave.sh** - Interleave paired-end sequencing reads
```bash
./interleave.sh reads_R1.fq reads_R2.fq > interleaved.fq
```

**combine-ig-headers.sh** - Combine immunoglobulin sequence headers
```bash
./combine-ig-headers.sh sequences.fa > combined.fa
```

### String Processing

**awktag.sh** - AWK-based string tagging
```bash
./awktag.sh pattern input.txt
```

**betterthanbasename** - Enhanced basename functionality
```bash
./betterthanbasename /path/to/file.tar.gz .tar.gz
```

## Usage Examples

### Pipeline Processing
```bash
# Convert CSV to TSV, extract IDs, process in chunks
cat data.csv | \
  ./delim_to_tab_UTF8 | \
  ./get_IDs | \
  python break-to-100s.py
```

### Bulk File Operations
```bash
# Rename all files matching pattern
./osxrename.pl 's/IMG_/photo_/g' *.jpg

# Move large files with progress
./move_large_files.sh raw_data/ processed_data/ "*.fastq.gz"
```

### System Management
```bash
# Distribute configuration to multiple servers
./distribute_ex.sh config_files.txt web1 web2 web3

# Execute with error handling
./CatchAndSlot.sh ./critical_backup.sh
```

## Requirements

Most tools require only standard Unix utilities. Specific requirements:

- **Python scripts**: Python 3.6+
- **Perl scripts**: Perl 5.10+
- **C programs**: Compile with `gcc only_alpha.c -o only_alpha`

Python dependencies (if needed):
```bash
pip install beautifulsoup4 requests pdftotext
```

## Installation

```bash
# Clone repository
git clone https://github.com/olympus-terminal/tools.git
cd tools

# Make all scripts executable
find . -name "*.sh" -o -name "*.py" -o -name "*.pl" | xargs chmod +x

# Compile C programs
gcc only_alpha.c -o only_alpha

# Add to PATH
echo 'export PATH="$PATH:'$(pwd)'"' >> ~/.bashrc
source ~/.bashrc
```

## Contributing

Contributions welcome. Please:
1. Fork the repository
2. Create a feature branch
3. Add your tool with usage documentation
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contact

- Issues: [GitHub Issues](https://github.com/olympus-terminal/tools/issues)
- Author: [@olympus-terminal](https://github.com/olympus-terminal)
