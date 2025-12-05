import os
import requests
import tarfile
from .config_utils import load_config, ensure_config_dir_exists


# ---------------------------------------------------------------
# Helper: download + extract
# ---------------------------------------------------------------
def _fetch_and_extract(url, local_path):
    print(f"Starting download: {url}")

    try:
        # Download file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        extract_dir = os.path.dirname(local_path)
        print(f"Extracting into: {extract_dir}")

        # Extract .txz archive
        with tarfile.open(local_path, "r:xz") as tar:
            tar.extractall(path=extract_dir)

        os.remove(local_path)
        print("Download + extraction complete.\n")
        return True

    except Exception as e:
        print(f"[ERROR] Isochrone download failed: {e}")
        return False


# ---------------------------------------------------------------
# Helper: construct URL + download
# ---------------------------------------------------------------
def _execute_download(config, filename, local_path):
    base_url = config["MIST_BASE_URL"]
    url = f"{base_url}{filename}"
    return _fetch_and_extract(url, local_path)


# ---------------------------------------------------------------
# MAIN FUNCTION (non-interactive ONLY)
#
# vcrit must be numeric (0.0 or 0.4)
#
# ---------------------------------------------------------------
def download_isochrone(vcrit=None):
    """
    Download a MIST Isochrone archive based on numeric vcrit.
    Example:
        vcrit = 0.0   → MIST_v1.2_vvcrit0.0_UBVRIplus.txz
        vcrit = 0.4   → MIST_v1.2_vvcrit0.4_UBVRIplus.txz

    Interactive (menu-based) mode is DISABLED.
    """

    config = load_config()
    download_dir = config["DOWNLOAD_DIR"]

    ensure_config_dir_exists(config)

    # ---------------------------------------------------------
    # Validate inputs
    # ---------------------------------------------------------
    if vcrit is None:
        raise RuntimeError(
            "Interactive mode is disabled. You must specify vcrit in run_config.json."
        )

    if not isinstance(vcrit, (float, int)):
        raise ValueError("vcrit must be numeric (e.g., 0.0 or 0.4).")

    vvcrit = f"{float(vcrit):.1f}"   # Convert to string formatted like "0.0"

    # ---------------------------------------------------------
    # Build filename
    # ---------------------------------------------------------
    filename = f"MIST_v1.2_vvcrit{vvcrit}_UBVRIplus.txz"
    local_path = os.path.join(download_dir, filename)
    base_name = filename.rsplit(".", 1)[0]

    # Detect if already extracted (directory matching prefix exists)
    try:
        existing = any(f.startswith(base_name) for f in os.listdir(download_dir))
    except FileNotFoundError:
        existing = False

    if existing:
        print(
            f"Required isochrone directory already exists → skipping {filename}\n"
        )
        return

    # ---------------------------------------------------------
    # Perform download
    # ---------------------------------------------------------
    print(f"Downloading Isochrone: {filename}")
    return _execute_download(config, filename, local_path)
