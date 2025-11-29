import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii


def plt_iso(iso_settings, points):

    iso_dir = iso_settings.get("iso_directory")
    desired_age = iso_settings.get("age", 9.0)   # log(age/yr), default = 1e9 yr = 1 Gyr

    if iso_dir is None or not os.path.isdir(iso_dir):
        raise ValueError(f"[ERROR] Isochrone directory not found: {iso_dir}")

    print(f"[INFO] Using Isochrone directory: {iso_dir}")

    # find files
    iso_files = sorted([
        f for f in os.listdir(iso_dir)
        if f.endswith((".iso", ".iso.cmd", ".cmd", ".dat"))
    ])

    if not iso_files:
        raise RuntimeError("[ERROR] No isochrone files found.")

    chosen = iso_files[0]
    filepath = os.path.join(iso_dir, chosen)
    print(f"[INFO] Using Isochrone file: {chosen}")

    # read
    try:
        data = ascii.read(filepath)
    except Exception as e:
        raise RuntimeError(f"[ERROR] Failed to read {chosen}: {e}")

    # extract columns
    ages = np.array(data['col2'])      # log10(age)
    logT = np.array(data['col5'])
    logL = np.array(data['col7'])

    # find which rows correspond to the desired isochrone
    unique_ages = np.unique(ages)
    idx = np.argmin(np.abs(unique_ages - desired_age))
    chosen_age = unique_ages[idx]

    print(f"[INFO] Using isochrone age log10(age/yr) = {chosen_age}")

    mask = (ages == chosen_age)

    # plot
    plt.plot(logT[mask], logL[mask], '-', color='blue', label=f"Isochrone log(age)={chosen_age:.2f}")

    # plot stars
    for p in points:
        plt.errorbar(
            p["x"], p["y"],
            xerr=p["x_err"], yerr=p["y_err"],
            fmt='o', label=p["name"]
        )

    plt.xlabel("log(T_eff)")
    plt.ylabel("log(L)")
    plt.title("Isochrone")

    plt.grid(True)
    plt.legend()
    plt.gca().invert_xaxis()

    print("[INFO] Isochrone plot complete.")
