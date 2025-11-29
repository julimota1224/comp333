import os
import math as m
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
from .config_utils import load_config

# =====================================================================
# Main plot function (fully automated, no input prompts)
# =====================================================================
def plot_eep(cfg):
    """
    cfg comes from run_config.json, containing:

    {
        "min_mass_code": "00100",
        "max_mass_code": "00500",
        "age_min": 1e6,
        "age_max": 3e7,
        "label_lower": "1.00 M⊙",
        "label_upper": "5.00 M⊙",
        "fill_between": true
    }
    """

    # -------------------------------------------------------------
    # 1. Load system config (download directory)
    # -------------------------------------------------------------
    system_cfg = load_config()
    download_dir = system_cfg.get("DOWNLOAD_DIR")

    if not os.path.isdir(download_dir):
        print(f"[ERROR] DOWNLOAD_DIR does not exist: {download_dir}")
        return

    # -------------------------------------------------------------
    # 2. Auto-detect extracted EEPS directory
    # -------------------------------------------------------------
    eep_dirs = [
        os.path.join(download_dir, d)
        for d in os.listdir(download_dir)
        if os.path.isdir(os.path.join(download_dir, d)) and d.endswith("_EEPS")
    ]

    if not eep_dirs:
        print(f"[ERROR] No extracted EEPS directories found in {download_dir}")
        print("Run eep_download first.")
        return

    path = eep_dirs[0]   # use the first match
    print(f"[INFO] Using EEPS directory: {path}")

    # -------------------------------------------------------------
    # 3. Extract list of files inside EEPS folder
    # -------------------------------------------------------------
    file_list = os.listdir(path)

    # Clean out README files
    mass_files = []
    for f in file_list:
        if f.endswith(".track.eep"):
            mass_files.append(f)

    # Sorted list for consistency
    mass_files = sorted(mass_files)

    # Convert file names (#####M.track.eep) → mass codes ##### (string)
    file_codes = [f[:5] for f in mass_files]

    # -------------------------------------------------------------
    # 4. Load user-specified settings from cfg
    # -------------------------------------------------------------
    min_code = cfg["min_mass_code"]
    max_code = cfg["max_mass_code"]
    age_min = float(cfg["age_min"])
    age_max = float(cfg["age_max"])
    label_lower = cfg["label_lower"]
    label_upper = cfg["label_upper"]
    fill_region = cfg.get("fill_between", False)

    # -------------------------------------------------------------
    # Helper function: load temperature + luminosity arrays
    # -------------------------------------------------------------
    def load_mass_track(mcode):
        fname = os.path.join(path, f"{mcode}M.track.eep")
        data = ascii.read(fname)
        logt = np.array(data['col12'])
        logl = np.array(data['col7'])
        age = np.array(data['col1'])
        return logt, logl, age

    # -------------------------------------------------------------
    # Function: restrict arrays to given age range
    # -------------------------------------------------------------
    def restrict_age(logt, logl, age):
        idx = np.where((age >= age_min) & (age <= age_max))
        return logt[idx], logl[idx]

    # -------------------------------------------------------------
    # Function: interpolate between two mass tracks
    # -------------------------------------------------------------
    def interpolate_mass(min_m, max_m, target_m, logt_min, logt_max, logl_min, logl_max):
        """
        Interpolates temperature + luminosity arrays between mass min_m and max_m
        to reach target mass target_m.
        """
        # Arrays must match in size
        while len(logt_min) > len(logt_max):
            logt_min = logt_min[1:]
        while len(logt_max) > len(logt_min):
            logt_max = logt_max[1:]

        while len(logl_min) > len(logl_max):
            logl_min = logl_min[1:]
        while len(logl_max) > len(logl_min):
            logl_max = logl_max[1:]

        # Number of interpolation steps
        m_min = float(min_m) / 100
        m_max = float(max_m) / 100
        m_target = float(target_m) / 100

        steps = int(round((m_max - m_min) / 0.01))
        idx_target = int(round((m_target - m_min) / 0.01))

        out_logt = []
        out_logl = []

        for i in range(len(logt_min)):
            t_vals = np.linspace(logt_min[i], logt_max[i], steps + 2)
            l_vals = np.linspace(logl_min[i], logl_max[i], steps + 2)
            out_logt.append(t_vals[idx_target])
            out_logl.append(l_vals[idx_target])

        return np.array(out_logt), np.array(out_logl)

    # -------------------------------------------------------------
    # 5. Compute LOWER curve (min mass curve)
    # -------------------------------------------------------------
    if min_code in file_codes:
        # Direct file exists
        logt, logl, age = load_mass_track(min_code)
        low_logt, low_logl = restrict_age(logt, logl, age)
    else:
        # Must interpolate
        # Find nearest lower + upper mass data files
        pos = 0
        while pos < len(file_codes) and file_codes[pos] < min_code:
            pos += 1
        upper_code = file_codes[pos]
        lower_code = file_codes[pos - 1]

        # Load both
        logt_low, logl_low, age_low = load_mass_track(lower_code)
        logt_high, logl_high, age_high = load_mass_track(upper_code)

        # Restrict both to the same age range
        logt_low, logl_low = restrict_age(logt_low, logl_low, age_low)
        logt_high, logl_high = restrict_age(logt_high, logl_high, age_high)

        # Interpolate to target min_code
        low_logt, low_logl = interpolate_mass(lower_code, upper_code, min_code,
                                              logt_low, logt_high, logl_low, logl_high)

    # -------------------------------------------------------------
    # 6. Compute UPPER curve (max mass curve)
    # -------------------------------------------------------------
    if max_code in file_codes:
        logt, logl, age = load_mass_track(max_code)
        high_logt, high_logl = restrict_age(logt, logl, age)
    else:
        pos = 0
        while pos < len(file_codes) and file_codes[pos] < max_code:
            pos += 1
        upper_code = file_codes[pos]
        lower_code = file_codes[pos - 1]

        # Load both
        logt_low, logl_low, age_low = load_mass_track(lower_code)
        logt_high, logl_high, age_high = load_mass_track(upper_code)

        # Restrict both
        logt_low, logl_low = restrict_age(logt_low, logl_low, age_low)
        logt_high, logl_high = restrict_age(logt_high, logl_high, age_high)

        # Interpolated curve
        high_logt, high_logl = interpolate_mass(lower_code, upper_code, max_code,
                                                logt_low, logt_high, logl_low, logl_high)

    # -------------------------------------------------------------
    # 7. Plotting
    # -------------------------------------------------------------
    plt.plot(low_logt, low_logl, 'x', label=label_lower)
    plt.plot(high_logt, high_logl, 'x', label=label_upper)

    if fill_region:
        plt.fill(
            np.append(low_logt, high_logt[::-1]),
            np.append(low_logl, high_logl[::-1]),
            'y', alpha=0.4
        )

    print(f"[INFO] Generated curves with {len(low_logt)} and {len(high_logt)} points.")

    return