import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
from .config_utils import load_config


# Plot evolutionary tracks (EEP) using run_config.json only
def plot_eep(cfg):
    """
    Plot lower and upper evolutionary tracks with optional interpolation.

    cfg structure (from run_config.json):

    {
        "min_mass_code": "00105",
        "max_mass_code": "00108",
        "age_min": 1e6,
        "age_max": 3e7,
        "label_lower": "1.05 M⊙",
        "label_upper": "1.08 M⊙",
        "fill_between": true
    }
    """

    # 1. Load system config
    system_cfg = load_config()
    download_dir = system_cfg.get("DOWNLOAD_DIR")

    if not os.path.isdir(download_dir):
        raise RuntimeError(f"[ERROR] DOWNLOAD_DIR does not exist: {download_dir}")

    # 2. Find extracted EEPS directory
    eep_dirs = [
        os.path.join(download_dir, d)
        for d in os.listdir(download_dir)
        if d.endswith("_EEPS") and os.path.isdir(os.path.join(download_dir, d))
    ]

    if not eep_dirs:
        raise RuntimeError("[ERROR] No extracted EEPS directories found.")

    path = eep_dirs[0]
    print(f"[INFO] Using EEPS directory: {path}")

    # 3. Identify available mass tracks
    files = sorted(f for f in os.listdir(path) if f.endswith(".track.eep"))
    file_codes = [f[:5] for f in files]

    # 4. Load config parameters
    min_code = cfg["min_mass_code"]
    max_code = cfg["max_mass_code"]
    age_min = float(cfg["age_min"])
    age_max = float(cfg["age_max"])
    label_lower = cfg["label_lower"]
    label_upper = cfg["label_upper"]
    fill_region = cfg.get("fill_between", False)

    # Helpers
    def load_track(code):
        data = ascii.read(os.path.join(path, f"{code}M.track.eep"))
        return (
            np.array(data["col12"]),  # logT
            np.array(data["col7"]),   # logL
            np.array(data["col1"])    # age
        )

    def restrict_by_age(logT, logL, age):
        mask = (age >= age_min) & (age <= age_max)
        return logT[mask], logL[mask]

    def interpolate(code_lo, code_hi, code_target, logT_lo, logT_hi, logL_lo, logL_hi):
        # Match array sizes
        n = min(len(logT_lo), len(logT_hi))
        logT_lo, logT_hi = logT_lo[:n], logT_hi[:n]
        logL_lo, logL_hi = logL_lo[:n], logL_hi[:n]

        m_lo = float(code_lo) / 100
        m_hi = float(code_hi) / 100
        m_t = float(code_target) / 100

        frac = (m_t - m_lo) / (m_hi - m_lo)

        logT = logT_lo + frac * (logT_hi - logT_lo)
        logL = logL_lo + frac * (logL_hi - logL_lo)

        return logT, logL

    # 5. Compute LOWER curve
    if min_code in file_codes:
        logT, logL, age = load_track(min_code)
        low_T, low_L = restrict_by_age(logT, logL, age)
    else:
        idx = next(i for i, c in enumerate(file_codes) if c > min_code)
        lo, hi = file_codes[idx - 1], file_codes[idx]

        logT_lo, logL_lo, age_lo = load_track(lo)
        logT_hi, logL_hi, age_hi = load_track(hi)

        logT_lo, logL_lo = restrict_by_age(logT_lo, logL_lo, age_lo)
        logT_hi, logL_hi = restrict_by_age(logT_hi, logL_hi, age_hi)

        low_T, low_L = interpolate(lo, hi, min_code, logT_lo, logT_hi, logL_lo, logL_hi)

    # 6. Compute UPPER curve
    if max_code in file_codes:
        logT, logL, age = load_track(max_code)
        high_T, high_L = restrict_by_age(logT, logL, age)
    else:
        idx = next(i for i, c in enumerate(file_codes) if c > max_code)
        lo, hi = file_codes[idx - 1], file_codes[idx]

        logT_lo, logL_lo, age_lo = load_track(lo)
        logT_hi, logL_hi, age_hi = load_track(hi)

        logT_lo, logL_lo = restrict_by_age(logT_lo, logL_lo, age_lo)
        logT_hi, logL_hi = restrict_by_age(logT_hi, logL_hi, age_hi)

        high_T, high_L = interpolate(lo, hi, max_code, logT_lo, logT_hi, logL_lo, logL_hi)

    # 7. Plot
    plt.plot(low_T, low_L, '-', linewidth=2, label=label_lower)
    plt.plot(high_T, high_L, '-', linewidth=2, label=label_upper)

    if fill_region:
        plt.fill(
            np.concatenate([low_T, high_T[::-1]]),
            np.concatenate([low_L, high_L[::-1]]),
            alpha=0.3
        )

    print(f"[INFO] Generated EEP curves with {len(low_T)} and {len(high_T)} points.")
