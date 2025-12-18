import json
import sys
import matplotlib.pyplot as plt

from comp333.files.config_utils import load_config, ensure_config_dir_exists
from comp333.files.download_eep import download_eep
from comp333.files.download_iso import download_isochrone
from comp333.files.isochrone import plt_iso
from comp333.files.evolutionary_track import plot_eep


# Run everything from run_config.json
def run_from_config(config):
    """
    Executes all tasks defined in run_config.json.

    Expected structure:

    {
        "eep_download": {
            "run": true,
            "vcrit": 0.4,
            "feh": [-0.25, 0.0]
        },
        "iso_download": {
            "run": true,
            "vcrit": 0.0
        },
        "eep_plot": { "run": true },
        "iso_plot": { "run": true },
        "eep_plot_settings": {...},
        "plot_settings": {...},
        "points": [...]
    }
    """

    # 1. EEP downloads
    eep_cfg = config.get("eep_download", {})
    if eep_cfg.get("run", False):
        print("\n[MASTER] Downloading EEP files...")

        vcrit = eep_cfg.get("vcrit")
        feh_vals = eep_cfg.get("feh")

        if vcrit is None or feh_vals is None:
            raise ValueError(
                "[ERROR] eep_download requires numeric 'vcrit' and 'feh'."
            )

        # Allow feh to be a single value or a list
        if not isinstance(feh_vals, list):
            feh_vals = [feh_vals]

        for feh in feh_vals:
            download_eep(vcrit=vcrit, feh=feh)

    # 2. Isochrone download
    iso_dl_cfg = config.get("iso_download", {})
    if iso_dl_cfg.get("run", False):
        print("\n[MASTER] Downloading Isochrone files...")

        vcrit = iso_dl_cfg.get("vcrit")
        if vcrit is None:
            raise ValueError(
                "[ERROR] iso_download requires numeric 'vcrit'."
            )

        download_isochrone(vcrit=vcrit)

    # 3. Plot evolutionary tracks
    if config.get("eep_plot", {}).get("run", False):
        print("\n[MASTER] Plotting evolutionary tracks...")
        eep_plot_cfg = config.get("eep_plot_settings", {})
        plot_eep(eep_plot_cfg)

    # 4. Plot isochrone segments + stars
    if config.get("iso_plot", {}).get("run", False):
        print("\n[MASTER] Plotting isochrone segments...")

        plot_settings = config.get("plot_settings", {})
        points = config.get("points", [])

        plt_iso(plot_settings, points)

    # 5. Display final figure
    print("\n[MASTER] Displaying plots...")
    plt.show()


# Entry Point
def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m comp333.master <run_config.json>")
        return

    run_config_path = sys.argv[1]

    # Load system configuration
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


# Main
if __name__ == "__main__":
    main()