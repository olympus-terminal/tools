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

**NEVER fabricate metadata or annotations:**
     DO NOT invent PFAM/protein domain functional descriptions
     DO NOT make up gene names, GO terms, or pathway annotations
     DO NOT guess or infer biological functions without verified source data
     If annotation data is not in a local file or successfully retrieved from an API, state "annotation not available" rather than fabricating one
     When fetching external data (e.g., InterPro API), only report what was actually returned - never fill in gaps with plausible-sounding information

  ## CRITICAL: No Methodology Demonstrations with Hardcoded Values

  **NEVER create scripts that simulate analysis by hardcoding results.**

  This deceptive pattern includes:
  - Functions that accept data parameters but return predetermined values
  - Scripts that load real files but ignore them, outputting hardcoded results
  - "Placeholder" implementations that print fake statistics/p-values/correlations
  - Code that appears to iterate over data but uses fixed loop outputs
  - Any result that doesn't trace directly back to actual computation on input data

  **Red flag patterns to AVOID:**
  ```python
  # BAD: Looks like analysis but values are hardcoded
  def analyze_correlation(data):
      # ... some code that touches data ...
      return {"r": 0.73, "p": 0.002}  # ← hardcoded, not computed

  # BAD: Loading file but ignoring it
  df = pd.read_csv(real_file)
  results = [0.85, 0.72, 0.91, 0.68]  # ← where did these come from?

  # BAD: "Demonstration" that fabricates output
  print(f"Significant associations: 47 (FDR < 0.05)")  # ← not computed

  Every numerical result in output MUST be traceable to:
  1. A computation performed on loaded data, OR
  2. A value read directly from an input file

  If implementation is incomplete: Return errors, raise exceptions, or explicitly state "NOT IMPLEMENTED" - never return plausible-looking fake values.

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

 ```

Zero Tolerance:

Any detected use of placeholder or synthetic data in analysis triggers a critical policy violation and must be escalated for review.


## Core Principles

- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary
- ALWAYS prefer editing existing files over creating new ones
- When creating a new file or program, add a timestamp to the filename (format: YYYYMMDD_HHMMSS) - make certain that new output files from developed programs will not override each other
- Do not run programs on synthetic or subsampled data unless explicitly requested
- ALWAYS make sure new results files can be traced to the program that generated them
- **NEVER write "expected results" or predictions about what analysis outcomes should be** - this creates confirmation bias and confuses future agents who may mistake predictions for actual findings
 


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
