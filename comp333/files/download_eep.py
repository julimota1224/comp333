import os
import requests
import tarfile
from .config_utils import load_config, ensure_config_dir_exists


def _feh_to_code(feh: float) -> str:
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
        print("ERROR:", e)
        return False


def download_eep(vcrit=None, feh=None):
    """
    vcrit : float (0.0 or 0.4)
    feh   : float (e.g., -0.25, 0.00, +0.50)
    """
    if vcrit is None or feh is None:
        raise ValueError("download_eep() requires numeric vcrit and feh.")

    if not isinstance(vcrit, (int, float)):
        raise ValueError("vcrit must be numeric (e.g., 0.4 or 0.0).")
    if not isinstance(feh, (int, float)):
        raise ValueError("feh must be numeric (e.g., -0.25 or 0.0).")

    config = load_config()
    ensure_config_dir_exists(config)
    download_dir = config["DOWNLOAD_DIR"]

    feh_code = _feh_to_code(float(feh))
    vcrit_code = f"{float(vcrit):.1f}"

    filename = f"MIST_v1.2_feh_{feh_code}_afe_p0.0_vvcrit{vcrit_code}_EEPS.txz"
    local_path = os.path.join(download_dir, filename)
    base_name = filename.replace(".txz", "")

    # Skip if already extracted
    if os.path.isdir(os.path.join(download_dir, base_name)):
        print(f"Already exists → skipping {filename}\n")
        return

    # Some extractions might not be a single directory; prefix check helps.
    if any(name.startswith(base_name) for name in os.listdir(download_dir)):
        print(f"Already exists → skipping {filename}\n")
        return

    url = f"{config['MIST_BASE_URL']}{filename}"
    print(f"Downloading: {filename}")
    return _fetch_and_extract(url, local_path)
