import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
from .config_utils import load_config


def _feh_to_code(feh: float) -> str:
    sign = "p" if feh >= 0 else "m"
    return f"{sign}{abs(feh):.2f}"


def _vcrit_to_code(vcrit: float) -> str:
    return f"{float(vcrit):.1f}"


def _find_eep_dir(download_dir: str, feh: float, vcrit: float) -> str:
    """
    Find extracted EEPS directory matching feh + vcrit.
    Example:
      MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.4_EEPS
    """
    feh_code = _feh_to_code(float(feh))
    vv = _vcrit_to_code(float(vcrit))

    target_suffix = f"feh_{feh_code}_afe_p0.0_vvcrit{vv}_EEPS"
    candidates = [
        os.path.join(download_dir, d)
        for d in os.listdir(download_dir)
        if d.endswith("_EEPS") and target_suffix in d
    ]
    if candidates:
        return sorted(candidates)[0]

    # fallback: any EEPS dir (for robustness), but only if nothing matches
    fallback = [
        os.path.join(download_dir, d)
        for d in os.listdir(download_dir)
        if d.endswith("_EEPS")
    ]
    if fallback:
        return sorted(fallback)[0]

    raise RuntimeError("No EEPS directory found. Run eep_download first.")


def plot_eep(cfg):
    """
    Plot two evolutionary tracks (min and max mass) for one or more metallicities.
    Returns bounds tuned to the low-mass regime across all plotted tracks.
    """

    system_cfg = load_config()
    download_dir = system_cfg["DOWNLOAD_DIR"]

    min_code = cfg["min_mass_code"]
    max_code = cfg["max_mass_code"]
    age_min = float(cfg["age_min"])
    age_max = float(cfg["age_max"])

    feh_list = cfg.get("feh_list", None)
    if feh_list is None:
        feh_list = [0.0]  # default if not provided
    if not isinstance(feh_list, list):
        feh_list = [feh_list]

    vcrit = float(cfg.get("vcrit", 0.4))

    label_low = cfg.get("label_lower", "Lower Mass Track")
    label_high = cfg.get("label_upper", "Upper Mass Track")

    all_T_accum = []
    all_L_accum = []

    def load_track(path, code):
        data = ascii.read(os.path.join(path, f"{code}M.track.eep"))
        return (
            np.array(data["col12"]),  # log(T_eff)
            np.array(data["col7"]),   # log(L)
            np.array(data["col1"]),   # age (years)
        )

    def restrict(logT, logL, age):
        m = (age >= age_min) & (age <= age_max)
        return logT[m], logL[m]

    def interpolate(target, low, high, low_vals, high_vals):
        if high == low:
            return low_vals
        w = (target - low) / (high - low)
        return low_vals * (1 - w) + high_vals * w

    def get_curve(path, codes, code):
        if code in codes:
            logT, logL, age = load_track(path, code)
            return restrict(logT, logL, age)

        idx = np.searchsorted(codes, code)
        if idx <= 0 or idx >= len(codes):
            raise ValueError(f"Requested mass code {code} is outside available EEPS range.")

        low_c, high_c = codes[idx - 1], codes[idx]

        low_T, low_L = restrict(*load_track(path, low_c))
        high_T, high_L = restrict(*load_track(path, high_c))

        n = min(len(low_T), len(high_T))
        low_T, low_L = low_T[:n], low_L[:n]
        high_T, high_L = high_T[:n], high_L[:n]

        target = float(code)
        low = float(low_c)
        high = float(high_c)

        logT = interpolate(target, low, high, low_T, high_T)
        logL = interpolate(target, low, high, low_L, high_L)
        return logT, logL

    for feh in feh_list:
        eep_path = _find_eep_dir(download_dir, feh=float(feh), vcrit=vcrit)
        print(f"[INFO] Using EEPS directory for [Fe/H]={feh:+.2f}: {eep_path}")

        files = sorted(f for f in os.listdir(eep_path) if f.endswith(".track.eep"))
        codes = sorted([f[:5] for f in files])

        low_T, low_L = get_curve(eep_path, codes, min_code)
        high_T, high_L = get_curve(eep_path, codes, max_code)

        # labels include metallicity so overlay is understandable
        feh_tag = f"[Fe/H]={float(feh):+.2f}"
        plt.plot(low_T, low_L, "-", lw=2.5, label=f"{label_low} ({feh_tag})")
        plt.plot(high_T, high_L, "-", lw=2.5, label=f"{label_high} ({feh_tag})")

        all_T_accum.append(low_T)
        all_T_accum.append(high_T)
        all_L_accum.append(low_L)
        all_L_accum.append(high_L)

    all_T = np.concatenate(all_T_accum) if all_T_accum else np.array([])
    all_L = np.concatenate(all_L_accum) if all_L_accum else np.array([])

    if all_T.size == 0 or all_L.size == 0:
        raise RuntimeError("No EEP data plotted; check your mass codes and age range.")

    # Low-mass focused bounds across all metallicities
    pad_T = 0.02 * (all_T.max() - all_T.min())
    pad_L = 0.08 * (all_L.max() - all_L.min())

    return {
        "x": all_T,
        "y": all_L,
        "xlim": (all_T.max() + pad_T, all_T.min() - pad_T),  # inverted axis convention handled by limits
        "ylim": (all_L.min() - pad_L, all_L.max() + pad_L),
    }
