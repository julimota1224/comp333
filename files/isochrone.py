import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii


def plt_iso(plot_settings, eep_cfg, points):
    """
    Plot restricted isochrone segments corresponding to the
    same mass and age bounds used for evolutionary tracks.

    Inputs:
    - plot_settings:
        {
            "iso_directory": "...",
            "title": "...",
            "xlabel": "...",
            "ylabel": "...",
            "invert_xaxis": true
        }

    - eep_cfg:
        {
            "age_min": <float, years>,
            "age_max": <float, years>,
            "min_mass_code": "00105",
            "max_mass_code": "00108"
        }

    - points:
        list of star dictionaries with x, y, x_err, y_err
    """

    # Validate isochrone directory
    iso_dir = plot_settings.get("iso_directory")
    if iso_dir is None or not os.path.isdir(iso_dir):
        raise ValueError(f"[ERROR] Isochrone directory not found: {iso_dir}")

    print(f"[INFO] Using Isochrone directory: {iso_dir}")

    # Locate isochrone file
    iso_files = sorted(
        f for f in os.listdir(iso_dir)
        if f.endswith((".iso", ".iso.cmd"))
    )

    if not iso_files:
        raise RuntimeError("[ERROR] No isochrone files found.")

    filepath = os.path.join(iso_dir, iso_files[0])
    print(f"[INFO] Using Isochrone file: {iso_files[0]}")

    # Read data
    try:
        data = ascii.read(filepath)
    except Exception as e:
        raise RuntimeError(f"[ERROR] Failed to read isochrone file: {e}")

    # Extract columns
    ages = np.array(data['col2'])   # log10(age/yr)
    mass = np.array(data['col3'])   # initial stellar mass
    logT = np.array(data['col5'])
    logL = np.array(data['col7'])

    # Convert config values
    age_min = np.log10(eep_cfg["age_min"])
    age_max = np.log10(eep_cfg["age_max"])

    min_mass = float(eep_cfg["min_mass_code"]) / 100
    max_mass = float(eep_cfg["max_mass_code"]) / 100

    # Find closest available isochrone ages
    unique_ages = np.unique(ages)
    age_lo = unique_ages[np.argmin(np.abs(unique_ages - age_min))]
    age_hi = unique_ages[np.argmin(np.abs(unique_ages - age_max))]

    print(f"[INFO] Isochrone ages used: log(age) = {age_lo:.2f}, {age_hi:.2f}")

    # Plot restricted isochrone segments
    for age_val in (age_lo, age_hi):
        mask = (
            (ages == age_val) &
            (mass >= min_mass) &
            (mass <= max_mass)
        )

        plt.plot(
            logT[mask],
            logL[mask],
            '-',
            linewidth=2,
            label=f"Isochrone log(age)={age_val:.2f}"
        )

    # Plot user-specified stars
    for p in points:
        plt.errorbar(
            p["x"],
            p["y"],
            xerr=p.get("x_err"),
            yerr=p.get("y_err"),
            fmt='o',
            capsize=3,
            label=p["name"]
        )

    # Styling
    plt.xlabel(plot_settings.get("xlabel", "log(T_eff)"))
    plt.ylabel(plot_settings.get("ylabel", "log(L)"))
    plt.title(plot_settings.get("title", "HR Diagram"))
    plt.grid(True)

    if plot_settings.get("invert_xaxis", True):
        plt.gca().invert_xaxis()

    plt.legend()
    print("[INFO] Isochrone plotting complete.")