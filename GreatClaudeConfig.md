# Claude Instructions

## CRITICAL: Data Integrity Policy

**NEVER create scripts, figures, or result files using synthetic, simulated, or randomly generated data as a substitute for real experimental results.**

This includes:
- DO NOT use `np.random`, `torch.rand`, or 'np.linspace()' for dummy importance values or similar functions to generate fake scientific data for publication figures
- DO NOT create "improved" or "cleaned up" visualizations based on summary statistics instead of raw data
- DO NOT reconstruct attribution patterns, gradients, or any analysis results from partial information
- DO NOT generate placeholder data for CAV analysis, uncertainty quantification, or any interpretability methods

**Acceptable uses of random functions:**
- Standard ML training operations (batch sampling, weight initialization, dropout)
- Statistical bootstrapping or resampling of real data
- Test cases clearly marked as synthetic for unit testing only

**If real data is unavailable:** Stop and request the actual data rather than generating synthetic alternatives.

## Data Integrity Enforcement

Purpose:
Ensure no analysis, visualization, or interpretability step can proceed if synthetic or placeholder data is generated, intentionally or unintentionally.

Implementation Steps:

Runtime Guard:

Every analysis, plotting, or interpretability script must import and call:

from DataIntegrityGuard import enforce_data_integrity
enforce_data_integrity()


at the very beginning of execution.

What the guard does:

Scans the active script for forbidden functions or modules, including:

np.linspace, np.random.*, torch.rand*, random.*, faker.*, synthetic*


Aborts immediately with a clear error message if any are detected.

Allows exceptions only when the script header contains:

# ALLOW_SYNTHETIC_FOR_TRAINING


and when the context is confirmed to be model training or bootstrapping.

Figure/Analysis Input Validation:

All data passed to visualization or metrics functions must originate from real files, not in-memory arrays or lists.

Example:

validate_input_source(input_path)


where validate_input_source checks for a valid, existing file.

Provenance Logging (Mandatory):

Every output file (figures, metrics, CSVs) must contain a header or metadata block:

# Provenance:
#   Script: /abs/path/to/script.py
#   Input:  /abs/path/to/data.tsv
#   Date:   YYYY-MM-DD HH:MM:SS
#   Integrity Check: PASSED


Testing the Guard:

A unit test (test_data_integrity.py) must be included in the repository.

Example:

def test_no_fake_data():
    import pytest, numpy as np
    from DataIntegrityGuard import enforce_data_integrity
    with pytest.raises(RuntimeError):
        np.linspace(0, 1, 10)


Zero Tolerance:

Any detected use of placeholder or synthetic data in analysis triggers a critical policy violation and must be escalated for review.


## Core Principles

- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary
- ALWAYS prefer editing existing files over creating new ones
- When creating a new file or program, add a timestamp to the filename (format: YYYYMMDD_HHMMSS) - make certain that new output files from developed programs will not override each other
- Do not run programs on synthetic or subsampled data unless explicitly requested
- ALWAYS make sure new results files can be traced to the program that generated them

## Memory-Efficient Coding


**ALWAYS prioritize memory-efficient implementations by default:**

- **Stream large files** line-by-line or in chunks instead of loading entire files into memory
- **Use generators and iterators** instead of loading full datasets into lists/arrays
- **Process data in batches** when dealing with multi-million line files
- **Clean up variables** with `del` when large objects are no longer needed
- **Use appropriate data structures** (e.g., numpy arrays vs lists, pandas chunking)
- **Estimate memory usage** before loading data (file size × parsing overhead)
- **Profile memory consumption** for scripts handling >1M lines or >1GB files

**Common patterns to AVOID:**
- `lines = file.readlines()` for large files → use `for line in file:`
- `data = [process(x) for x in huge_list]` → use generators or chunk processing
- Loading entire genome files into memory when only sequential access is needed

**When to override:** If explicitly told to run on a bigmem node or high-memory system, or if memory-intensive approach is specifically requested

## Script Development & Testing

**Before running scripts on full datasets:**
- Test on small subsets of data first to verify correctness
- Estimate and report expected runtime for large operations
- Check if output files already exist before recomputing
- Use existing tools/libraries when available rather than reimplementing

**When developing new scripts:**
- Be proactive about testing and debugging - don't just say "should be ready!" you need to be sure - take your time to make sure it is legitimate
- Include logging of key parameters and software versions in script headers
- Document data provenance (input file paths, dates, versions) in outputs
- Add error handling for common edge cases (empty files, missing columns, etc.)

## Explaining Results
ALWAYS GIVE REALPATHs of created files
When asked to explain analysis results or figures:
1. Show the exact code/formula that generated the data FIRST
2. Print actual numerical values (not descriptions)
3. State "I don't know" if uncertain - never rationalize unexpected results without verification
4. If explanation seems counterintuitive, verify against implementation before presenting

## visualizations

1. REFER TO FIGURE_PROTOCOL.MD for visualization rules i.e., creating figures, graphics, etc.
2. View any generated graphics to ensure adherence to FIGURE_PROTOCOL.md, especially regarding text overlapping with other figure elements
