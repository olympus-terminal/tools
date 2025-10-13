# Claude Instructions

## Core Principles
- NEVER create scripts or figures using synthetic, simulated, or randomly generated data as a substitute for real experimental results.
## CRITICAL: Data Integrity Policy

**NEVER create scripts or figures using synthetic, simulated, or randomly generated data as a substitute for real experimental results.**

This includes:
- DO NOT use `np.random`, `torch.rand`, or similar functions to generate fake scientific data for publication figures
- DO NOT create "improved" or "cleaned up" visualizations based on summary statistics instead of raw data
- DO NOT reconstruct attribution patterns, gradients, or any analysis results from partial information
- DO NOT generate placeholder data for CAV analysis, uncertainty quantification, or any interpretability methods

**Acceptable uses of random functions:**
- Standard ML training operations (batch sampling, weight initialization, dropout)
- Statistical bootstrapping or resampling of real data
- Test cases clearly marked as synthetic for unit testing only

**If real data is unavailable:** Stop and request the actual data rather than generating synthetic alternatives.

- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary
- ALWAYS prefer editing existing files over creating new ones
- When creating a new file or program, add a timestamp to the filename
- Do not run programs on synthetic or subsampled data unless explicitly requested
- ALWAYS make sure new results files can be traced to the program that generated them

## Project-Specific Context
<!-- Add your project-specific instructions here -->

## Commands to Run
- When developing new scripts, be proactive about testing and debugging them - don't just say "should be ready!" you need to be sure - take your time to make sure it is legitimate

## Explaining Results

When asked to explain analysis results or figures:
1. Show the exact code/formula that generated the data FIRST
2. 2. Print actual numerical values (not descriptions)
3. State "I don't know" if uncertain - never rationalize unexpected results without verification
4. If explanation seems counterintuitive, verify against implementation before presenting



<!-- Add any lint/typecheck commands that should be run after code changes -->
<!-- Example: -->
<!-- npm run lint -->
<!-- npm run typecheck -->
