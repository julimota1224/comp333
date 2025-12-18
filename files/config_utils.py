import json
import os

# NOTE:
# This config.json is AUTO-GENERATED on first run.
# Users generally should NOT edit this file unless changing DOWNLOAD_DIR.

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def get_default_download_dir():
    """
    Return the default download directory:
    ~/MIST_Data
    """
    home_dir = os.path.expanduser("~")
    return os.path.join(home_dir, "MIST_Data")


def load_config():
    """
    Load system configuration from comp333/files/config.json.

    If the file does not exist, it is automatically created
    using safe, system-independent defaults.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    print(f"[INFO] config.json not found. Creating default configuration.")

    default_config = {
        "DOWNLOAD_DIR": get_default_download_dir(),
        "MIST_BASE_URL": "https://waps.cfa.harvard.edu/MIST/data/tarballs_v1.2/",
        "DEFAULT_EEPS_FILE": "",
        "DEFAULT_ISO_FILE": ""
    }

    save_config(default_config)
    return default_config


def save_config(config_data):
    """
    Save system configuration to comp333/files/config.json
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)
        print(f"[INFO] Configuration saved to {CONFIG_FILE}")
    except Exception as e:
        print(f"[ERROR] Failed to save configuration: {e}")


def ensure_config_dir_exists(config_data):
    """
    Ensure the DOWNLOAD_DIR exists; create it if missing.
    """
    download_dir = config_data.get("DOWNLOAD_DIR")

    if download_dir and not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir)
            print(f"[INFO] Created download directory: {download_dir}")
        except OSError as e:
            print(f"[ERROR] Could not create download directory {download_dir}: {e}")
            return False

    return True
