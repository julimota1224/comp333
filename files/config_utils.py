import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def get_default_download_dir():
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, "MIST_Data")


def save_config(config_data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)
    print(f"[INFO] Configuration saved to {CONFIG_FILE}")


def load_config():
    """
    Loads comp333/files/config.json.
    If missing, creates it with defaults (portable for new users).
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    print("[INFO] config.json not found. Creating default configuration.")
    default_config = {
        "DOWNLOAD_DIR": get_default_download_dir(),
        "MIST_BASE_URL": "https://waps.cfa.harvard.edu/MIST/data/tarballs_v1.2/",
        "DEFAULT_EEPS_FILE": "",
        "DEFAULT_ISO_FILE": ""
    }
    save_config(default_config)
    return default_config


def ensure_config_dir_exists(config_data):
    download_dir = config_data.get("DOWNLOAD_DIR")
    if not download_dir:
        return False

    # Expand ~
    download_dir = os.path.expanduser(download_dir)
    config_data["DOWNLOAD_DIR"] = download_dir

    if not os.path.exists(download_dir):
        os.makedirs(download_dir, exist_ok=True)
        print(f"[INFO] Created download directory: {download_dir}")
    return True
