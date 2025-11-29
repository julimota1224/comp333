import os
import requests
import tarfile
from .config_utils import load_config, save_config, ensure_config_dir_exists


def _get_feh_string(index):
    feh_map = {
        1: "m4.00",
        2: "m3.50",
        3: "m3.00",
        4: "m2.50",
        5: "m2.00",
        6: "m1.75",
        7: "m1.50",
        8: "m1.25",
        9: "m1.00",
        10: "m0.75",
        11: "m0.50",
        12: "m0.25",
        13: "p0.00",
        14: "p0.25",
        15: "p0.50",
    }
    return feh_map.get(index)


def _fetch_and_extract(url, local_path):
    print(f"Starting download: {url}")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        extract_dir = os.path.dirname(local_path)
        print(f"Extracting into: {extract_dir}")

        with tarfile.open(local_path, "r:xz") as tar:
            tar.extractall(path=extract_dir)

        os.remove(local_path)
        print("Done.\n")
        return True

    except Exception as e:
        print("ERROR:", e)
        return False


def _execute_download(config, filename, local_path):
    base_url = config["MIST_BASE_URL"]
    download_url = f"{base_url}{filename}"
    return _fetch_and_extract(download_url, local_path)


def download_eep(vcrit_choice=None, metallicity_index=None):
    """
    If args are provided: non-interactive (used by run_config.json)
    If args are None: interactive old menu
    """
    config = load_config()
    download_dir = config["DOWNLOAD_DIR"]

    ensure_config_dir_exists(config)

    interactive = (vcrit_choice is None or metallicity_index is None)

    if interactive:
        raise RuntimeError("Interactive mode disabled for JSON-driven workflow.")

    # Non-interactive mode VALIDATION
    if vcrit_choice not in ("A", "B"):
        raise ValueError("vcrit_choice must be 'A' or 'B'.")

    if not isinstance(metallicity_index, int):
        raise ValueError("metallicity_index must be an integer.")

    if not (1 <= metallicity_index <= 15):
        raise ValueError("metallicity_index must be 1–15.")

    vvcrit = "0.4" if vcrit_choice == "A" else "0.0"
    feh_code = _get_feh_string(metallicity_index)

    filename = f"MIST_v1.2_feh_{feh_code}_afe_p0.0_vvcrit{vvcrit}_EEPS.txz"
    local_path = os.path.join(download_dir, filename)

    base_name = filename.rsplit(".", 1)[0]

    if any(f.startswith(base_name) for f in os.listdir(download_dir)):
        print(f"Already exists → skipping {filename}\n")
        return

    print(f"Downloading: {filename}")
    return _execute_download(config, filename, local_path)