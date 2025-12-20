import json
import sys
import numpy as np
import matplotlib.pyplot as plt

from comp333.files.config_utils import load_config, ensure_config_dir_exists
from comp333.files.download_eep import download_eep
from comp333.files.download_iso import download_isochrone
from comp333.files.evolutionary_track import plot_eep
from comp333.files.isochrone import plt_iso



def run_from_config(cfg):
    # --- Downloads ---
    fehs = []
    eep_vcrit = None
    iso_vcrit = None

    if cfg.get("eep_download", {}).get("run"):
        eep_vcrit = cfg["eep_download"]["vcrit"]
        fehs = cfg["eep_download"]["feh"]
        if not isinstance(fehs, list):
            fehs = [fehs]
        for feh in fehs:
            download_eep(vcrit=eep_vcrit, feh=feh)

    if cfg.get("iso_download", {}).get("run"):
        iso_vcrit = cfg["iso_download"]["vcrit"]
        download_isochrone(iso_vcrit)

    # --- Plot EEPs (now supports multiple feh) ---
    eep_plot_cfg = dict(cfg["eep_plot_settings"])
    if fehs:
        eep_plot_cfg["feh_list"] = fehs
    if eep_vcrit is not None:
        eep_plot_cfg["vcrit"] = eep_vcrit

    eep_bounds = plot_eep(eep_plot_cfg)

    # --- Plot isochrones (now supports multiple feh) ---
    plot_cfg = dict(cfg["plot_settings"])
    if fehs:
        plot_cfg["feh_list"] = fehs
    if iso_vcrit is not None:
        plot_cfg["vcrit"] = iso_vcrit

    iso_bounds = plt_iso(
        plot_cfg,
        eep_bounds,
        cfg.get("points", [])
    )

    # Combined bounds if needed later
    all_x = np.concatenate([eep_bounds["x"], iso_bounds["x"]])
    all_y = np.concatenate([eep_bounds["y"], iso_bounds["y"]])

    # Use bounds from EEPs (low-mass focused)
    plt.xlim(*eep_bounds["xlim"])
    plt.ylim(*eep_bounds["ylim"])

    plt.xlabel(plot_cfg["xlabel"])
    plt.ylabel(plot_cfg["ylabel"])
    plt.title(plot_cfg["title"])
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 -m comp333.master <run_config.json>")
        return

    with open(sys.argv[1]) as f:
        cfg = json.load(f)

    ensure_config_dir_exists(load_config())
    run_from_config(cfg)


if __name__ == "__main__":
    main()
