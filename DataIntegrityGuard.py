# DataIntegrityGuard.py
import inspect, sys, os, numpy as np, torch

def enforce_data_integrity():
    banned = [
        np.linspace, np.random.rand, np.random.randn,
        torch.rand, torch.randn
    ]
    caller = sys.argv[0]
    src = open(caller).read()

    # Allow explicit override for training only
    if "# ALLOW_SYNTHETIC_FOR_TRAINING" in src:
        return

    for func in banned:
        if func.__name__ in src:
            raise RuntimeError(
                f"🚫 Data Integrity Violation: {func.__name__} detected in {caller}.\n"
                "Synthetic data generation is strictly prohibited under Data Integrity Policy."
            )

def validate_input_source(path):
    if not isinstance(path, str) or not os.path.exists(path):
        raise ValueError(f"🚫 Invalid data source: {path} — must be a real file path.")
