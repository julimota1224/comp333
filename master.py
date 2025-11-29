import json
import sys
import matplotlib.pyplot as plt

from comp333.files.config_utils import load_config, ensure_config_dir_exists
from comp333.files.download_eep import download_eep
from comp333.files.download_iso import download_isochrone
from comp333.files.isochrone import plt_iso
from comp333.files.evolutionary_track import plot_eep


# =====================================================================
# Run everything from run_config.json
# =====================================================================
def run_from_config(config):
    """
    Executes all tasks defined in run_config.json.

    Expected structure:

    {
        "eep_download": { "run": true, "vcrit": "A", "feh_index": 13 },
        "iso_download": { "run": true, "vcrit": "B" },
        "eep_plot": { "run": true },
        "iso_plot": { "run": true },
        "eep_plot_settings": {...},
        "plot_settings": {...},
        "points": [...]
    }
    """

    # ==========================================================
    # 1. EEPS DOWNLOAD
    # ==========================================================
    if config.get("eep_download", {}).get("run", False):
        print("\n[MASTER] Downloading EEP...")
        vcrit = config["eep_download"]["vcrit"]
        feh_index = config["eep_download"]["feh_index"]
        download_eep(vcrit_choice=vcrit, metallicity_index=feh_index)

    # ==========================================================
    # 2. ISOCHRONE DOWNLOAD
    # ==========================================================
    if config.get("iso_download", {}).get("run", False):
        print("\n[MASTER] Downloading isochrone...")
        vcrit = config["iso_download"]["vcrit"]
        download_isochrone(vcrit_choice=vcrit)

    # ==========================================================
    # 3. PLOT EEP AUTOMATICALLY
    # ==========================================================
    if config.get("eep_plot", {}).get("run", False):
        print("\n[MASTER] Plotting EEP curves...")
        eep_cfg = config.get("eep_plot_settings", {})
        plot_eep(eep_cfg)

    # ==========================================================
    # 4. PLOT ISOCHRONE AUTOMATICALLY
    # ==========================================================
    if config.get("iso_plot", {}).get("run", False):
        print("\n[MASTER] Plotting Isochrone...")
        iso_settings = config.get("iso_plot", {})
        points = config.get("points", [])
        plt_iso(iso_settings, points)

    # ==========================================================
    # 5. Show final plots
    # ==========================================================
    print("\n[MASTER] Displaying plots...")
    plt.show()


# =====================================================================
# ENTRY POINT
# =====================================================================
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m comp333.master <run_config.json>")
        return

    run_config_path = sys.argv[1]

    # Load main system config (DOWNLOAD_DIR, base URLs)
    system_cfg = load_config()
    ensure_config_dir_exists(system_cfg)

    # Load user-defined run_config.json
    try:
        with open(run_config_path, "r") as f:
            run_cfg = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load run_config file: {e}")
        return

    run_from_config(run_cfg)


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    main()
