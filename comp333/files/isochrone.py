import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from astropy.io import ascii


def _feh_to_code(feh: float) -> str:
    sign = "p" if feh >= 0 else "m"
    return f"{sign}{abs(feh):.2f}"


def _vcrit_to_code(vcrit: float) -> str:
    return f"{float(vcrit):.1f}"


def _find_iso_file(iso_dir: str, feh: float, vcrit: float) -> str:
    """
    Find the specific .iso.cmd file for this metallicity and vcrit.
    Example filename:
      MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_UBVRIplus.iso.cmd
    """
    feh_code = _feh_to_code(float(feh))
    vv = _vcrit_to_code(float(vcrit))
    target = f"MIST_v1.2_feh_{feh_code}_afe_p0.0_vvcrit{vv}_UBVRIplus.iso.cmd"
    path = os.path.join(iso_dir, target)
    if os.path.isfile(path):
        return path

    # fallback: try any iso.cmd if exact match missing
    files = sorted(f for f in os.listdir(iso_dir) if f.endswith(".iso.cmd"))
    if not files:
        raise ValueError(f"No .iso.cmd files found in: {iso_dir}")
    return os.path.join(iso_dir, files[0])


def plt_iso(iso_cfg, eep_bounds, points):
    iso_dir = os.path.expanduser(iso_cfg["iso_directory"])
    age_min = float(iso_cfg["age_min"])
    age_max = float(iso_cfg["age_max"])

    feh_list = iso_cfg.get("feh_list", None)
    if feh_list is None:
        feh_list = [0.0]
    if not isinstance(feh_list, list):
        feh_list = [feh_list]

    vcrit = float(iso_cfg.get("vcrit", 0.0))

    if not os.path.isdir(iso_dir):
        raise ValueError(f"Isochrone directory not found: {iso_dir}")

    # Plot bounds from EEPs
    xmin, xmax = min(eep_bounds["x"]), max(eep_bounds["x"])
    ymin, ymax = min(eep_bounds["y"]), max(eep_bounds["y"])

    used_T = []
    used_L = []

    # --- Isochrones for each metallicity ---
    for feh in feh_list:
        iso_path = _find_iso_file(iso_dir, feh=float(feh), vcrit=vcrit)
        data = ascii.read(iso_path)

        ages = np.array(data["col2"])
        logT = np.array(data["col5"])
        logL = np.array(data["col7"])

        for age in [age_min, age_max]:
            unique_ages = np.unique(ages)
            chosen = unique_ages[np.argmin(np.abs(unique_ages - age))]
            m = (ages == chosen)

            T = logT[m]
            L = logL[m]

            # clip to EEP overlap region (keeps plot readable and scientifically relevant)
            mask = (T >= xmin) & (T <= xmax) & (L >= ymin) & (L <= ymax)
            if np.count_nonzero(mask) < 5:
                continue

            Tm = T[mask]
            Lm = L[mask]

            feh_tag = f"[Fe/H]={float(feh):+.2f}"
            plt.plot(
                Tm, Lm,
                "--", lw=1.6, alpha=0.85,
                label=f"Iso log(age)={chosen:.2f} ({feh_tag})"
            )

            used_T.append(Tm)
            used_L.append(Lm)

    # --- Flexible observational constraints ---
    ax = plt.gca()
    point_x_vals = []
    point_y_vals = []
    extra_x_extents = []
    extra_y_extents = []

    def _safe_label(p):
        return p.get("name", "Constraint")

    for p in points:
        name = _safe_label(p)

        # Helpers: safely read ranges
        x_range = p.get("x_range", None)
        y_range = p.get("y_range", None)

        # Normalize ranges if provided
        if x_range is not None:
            if not (isinstance(x_range, list) and len(x_range) == 2):
                print(f"[WARN] x_range must be [min, max]. Skipping: {p}")
                continue
            x0, x1 = float(x_range[0]), float(x_range[1])
            extra_x_extents.extend([x0, x1])

        if y_range is not None:
            if not (isinstance(y_range, list) and len(y_range) == 2):
                print(f"[WARN] y_range must be [min, max]. Skipping: {p}")
                continue
            y0, y1 = float(y_range[0]), float(y_range[1])
            extra_y_extents.extend([y0, y1])

        # Case 1: exact point (x,y)
        if "x" in p and "y" in p:
            x = float(p["x"])
            y = float(p["y"])
            plt.errorbar(
                x, y,
                xerr=p.get("x_err"),
                yerr=p.get("y_err"),
                fmt="o", ms=6,
                label=name
            )
            point_x_vals.append(x)
            point_y_vals.append(y)

        # Case 2: x + y_range (vertical uncertainty bar/band)
        elif "x" in p and y_range is not None:
            x = float(p["x"])
            ymid = 0.5 * (y0 + y1)
            yerr = [[ymid - y0], [y1 - ymid]]
            plt.errorbar(
                x, ymid,
                xerr=p.get("x_err"),
                yerr=yerr,
                fmt="o", ms=6,
                label=name
            )
            point_x_vals.append(x)
            point_y_vals.append(ymid)

        # Case 3: y + x_range (horizontal uncertainty bar/band)
        elif "y" in p and x_range is not None:
            y = float(p["y"])
            xmid = 0.5 * (x0 + x1)
            xerr = [[xmid - x0], [x1 - xmid]]
            plt.errorbar(
                xmid, y,
                xerr=xerr,
                yerr=p.get("y_err"),
                fmt="o", ms=6,
                label=name
            )
            point_x_vals.append(xmid)
            point_y_vals.append(y)

        # Case 4: x only (no y information) -> vertical line at x
        elif "x" in p and "y" not in p and y_range is None:
            x = float(p["x"])
            ax.axvline(x, alpha=0.25, linewidth=2.0, label=name)
            extra_x_extents.append(x)

        # Case 5: y only (no x information) -> horizontal line at y
        elif "y" in p and "x" not in p and x_range is None:
            y = float(p["y"])
            ax.axhline(y, alpha=0.25, linewidth=2.0, label=name)
            extra_y_extents.append(y)

        # Case 6: x_range only -> shaded vertical band spanning full y-range
        elif x_range is not None and "y" not in p and y_range is None:
            ax.axvspan(x0, x1, alpha=0.18, label=name)

        # Case 7: y_range only -> shaded horizontal band spanning full x-range
        elif y_range is not None and "x" not in p and x_range is None:
            ax.axhspan(y0, y1, alpha=0.18, label=name)

        # Case 8: x_range + y_range -> shaded rectangle region
        elif x_range is not None and y_range is not None and "x" not in p and "y" not in p:
            rect = Rectangle(
                (x0, y0),
                width=(x1 - x0),
                height=(y1 - y0),
                alpha=0.15
            )
            ax.add_patch(rect)
            # Add an invisible handle for legend labeling (matplotlib quirk)
            ax.plot([], [], alpha=0.0, label=name)

        else:
            print(f"[WARN] Skipping unsupported point specification: {p}")

    # Bounds returned for master scaling if desired
    all_x_parts = []
    all_y_parts = []

    if used_T:
        all_x_parts.append(np.concatenate(used_T))
    if point_x_vals:
        all_x_parts.append(np.array(point_x_vals))
    if extra_x_extents:
        all_x_parts.append(np.array(extra_x_extents))

    if used_L:
        all_y_parts.append(np.concatenate(used_L))
    if point_y_vals:
        all_y_parts.append(np.array(point_y_vals))
    if extra_y_extents:
        all_y_parts.append(np.array(extra_y_extents))

    all_x = np.concatenate(all_x_parts) if all_x_parts else np.array([xmin, xmax])
    all_y = np.concatenate(all_y_parts) if all_y_parts else np.array([ymin, ymax])

    return {
        "x": all_x,
        "y": all_y,
    }
