import os
import requests
import tarfile
from .config_utils import load_config, ensure_config_dir_exists


# Helpers

def _feh_to_code(feh):
    """
    Convert numeric [Fe/H] to MIST filename code.

    Examples:
    -0.25 → "m0.25"
     0.00 → "p0.00"
     0.50 → "p0.50"
    """
    sign = "p" if feh >= 0 else "m"
    return f"{sign}{abs(feh):.2f}"


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
        print(f"[ERROR] Failed to download or extract EEPS: {e}")
        return False


# Public API

def download_eep(vcrit=None, feh=None):
    """
    Download MIST evolutionary tracks (EEPS) using numeric parameters.

    Parameters
    ----------
    vcrit : float
        Stellar rotation fraction (e.g. 0.4 or 0.0)

    feh : float
        Metallicity [Fe/H] (e.g. -0.25, 0.00, +0.50)

    This function is fully non-interactive and intended
    for use with run_config.json.
    """

    # Validate inputs
    if vcrit is None or feh is None:
        raise ValueError("download_eep() requires numeric vcrit and feh.")

    if not isinstance(vcrit, (int, float)):
        raise ValueError("vcrit must be numeric (e.g., 0.4 or 0.0).")

    if not isinstance(feh, (int, float)):
        raise ValueError("feh must be numeric (e.g., -0.25 or 0.0).")

    # Load system configuration
    config = load_config()
    download_dir = config.get("DOWNLOAD_DIR")

    if not ensure_config_dir_exists(config):
        raise RuntimeError("Download directory could not be created.")

    # Construct filename
    feh_code = _feh_to_code(feh)
    vcrit_code = f"{vcrit:.1f}"

    filename = (
        f"MIST_v1.2_feh_{feh_code}_afe_p0.0_vvcrit{vcrit_code}_EEPS.txz"
    )
    local_path = os.path.join(download_dir, filename)
    base_name = filename.replace(".txz", "")

    # Skip if already extracted
    if any(f.startswith(base_name) for f in os.listdir(download_dir)):
        print(f"Already exists → skipping {filename}\n")
        return

    # Download and extract
    base_url = config.get("MIST_BASE_URL")
    url = f"{base_url}{filename}"

    print(f"Downloading: {filename}")
    _fetch_and_extract(url, local_path)
