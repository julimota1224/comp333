import os
import requests
import tarfile
from .config_utils import load_config, ensure_config_dir_exists


# Helpers

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
        print("Download + extraction complete.\n")
        return True

    except Exception as e:
        print(f"[ERROR] Isochrone download failed: {e}")
        return False


def _execute_download(config, filename, local_path):
    base_url = config.get("MIST_BASE_URL")
    url = f"{base_url}{filename}"
    return _fetch_and_extract(url, local_path)


# Public API

def download_isochrone(vcrit=None):
    """
    Download a MIST Isochrone archive using numeric vcrit.

    Parameters
    ----------
    vcrit : float
        Stellar rotation fraction (e.g. 0.0 or 0.4)

    Interactive (menu-based) mode is DISABLED.
    """

    # Validate input
    if vcrit is None:
        raise RuntimeError(
            "download_isochrone() requires numeric vcrit in run_config.json."
        )

    if not isinstance(vcrit, (int, float)):
        raise ValueError("vcrit must be numeric (e.g., 0.0 or 0.4).")

    # Load system configuration
    config = load_config()
    download_dir = config.get("DOWNLOAD_DIR")

    if not ensure_config_dir_exists(config):
        raise RuntimeError("Download directory could not be created.")

    # Construct filename
    vvcrit = f"{float(vcrit):.1f}"
    filename = f"MIST_v1.2_vvcrit{vvcrit}_UBVRIplus.txz"
    local_path = os.path.join(download_dir, filename)
    base_name = filename.replace(".txz", "")

    # Skip if already extracted
    try:
        already_exists = any(
            f.startswith(base_name) for f in os.listdir(download_dir)
        )
    except FileNotFoundError:
        already_exists = False

    if already_exists:
        print(
            f"Required isochrone directory already exists → skipping {filename}\n"
        )
        return

    # Download and extract
    print(f"Downloading Isochrone: {filename}")
    _execute_download(config, filename, local_path)