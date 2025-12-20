import os
import requests
import tarfile
from .config_utils import load_config, ensure_config_dir_exists


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


def download_isochrone(vcrit=None):
    """
    vcrit : float (0.0 or 0.4)
    """
    if vcrit is None or not isinstance(vcrit, (int, float)):
        raise ValueError("download_isochrone(vcrit=...) requires numeric vcrit (e.g., 0.0 or 0.4).")

    config = load_config()
    ensure_config_dir_exists(config)
    download_dir = config["DOWNLOAD_DIR"]

    vvcrit = f"{float(vcrit):.1f}"
    filename = f"MIST_v1.2_vvcrit{vvcrit}_UBVRIplus.txz"
    local_path = os.path.join(download_dir, filename)

    base_name = filename.rsplit(".", 1)[0]
    if any(name.startswith(base_name) for name in os.listdir(download_dir)):
        print(f"Already exists → skipping {filename}\n")
        return

    url = f"{config['MIST_BASE_URL']}{filename}"
    print(f"Downloading Isochrone: {filename}")
    return _fetch_and_extract(url, local_path)
