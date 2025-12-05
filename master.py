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

    Expected clean structure:

    {
        "eep_download": { "run": true, "vcrit": 0.4, "feh": -0.25 },
        "iso_download": { "run": true, "vcrit": 0.0 },
        "eep_plot": { "run": true },
        "iso_plot": { "run": true, "iso_directory": "...", "age": 9.0 },
        "eep_plot_settings": {...},
        "points": [...]
    }
    """

    # ==========================================================
    # 1. EEPS DOWNLOAD
    # ==========================================================
    eep_cfg = config.get("eep_download", {})
    if eep_cfg.get("run", False):
        print("\n[MASTER] Downloading EEP...")

        vcrit = eep_cfg.get("vcrit")
        feh = eep_cfg.get("feh")

        if vcrit is None or feh is None:
            raise ValueError(
                "[ERROR] run_config.json must include numeric 'vcrit' and 'feh' for eep_download."
            )

        download_eep(vcrit=vcrit, feh=feh)

    # ==========================================================
    # 2. ISOCHRONE DOWNLOAD
    # ==========================================================
    iso_cfg = config.get("iso_download", {})
    if iso_cfg.get("run", False):
        print("\n[MASTER] Downloading Isochrone...")

        vcrit = iso_cfg.get("vcrit")
        if vcrit is None:
            raise ValueError("[ERROR] run_config.json must include numeric 'vcrit' for iso_download.")

        download_isochrone(vcrit=vcrit)

    # ==========================================================
    # 3. PLOT EEP AUTOMATICALLY
    # ==========================================================
    if config.get("eep_plot", {}).get("run", False):
        print("\n[MASTER] Plotting EEP curves...")
        eep_plot_cfg = config.get("eep_plot_settings", {})
        plot_eep(eep_plot_cfg)

    # ==========================================================
    # 4. PLOT ISOCHRONE AUTOMATICALLY
    # ==========================================================
    if config.get("iso_plot", {}).get("run", False):
        print("\n[MASTER] Plotting Isochrone...")

        iso_settings = config.get("plot_settings", {})
        # iso_settings may also contain iso_directory, age, etc.

        points = config.get("points", [])
        plt_iso(iso_settings, points)

    # ==========================================================
    # 5. Display plots
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

    # Load system config (base URLs, download dir)
    system_cfg = load_config()
    ensure_config_dir_exists(system_cfg)

    # Load run_config.json
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
