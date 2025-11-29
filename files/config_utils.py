import json
import os

# ALWAYS store the config.json inside the comp333/files directory
CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')


def get_default_download_dir():
    """Return ~/MIST_Data"""
    home_dir = os.path.expanduser('~')
    return os.path.join(home_dir, 'MIST_Data')


def load_config():
    """Load config from comp333/files/config.json"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)

    print(f"Configuration file '{CONFIG_FILE}' not found. Using default values.")

    default_config = {
        "DOWNLOAD_DIR": get_default_download_dir(),
        "MIST_BASE_URL": "https://waps.cfa.harvard.edu/MIST/data/tarballs_v1.2/",
        "DEFAULT_EEPS_FILE": "",
        "DEFAULT_ISO_FILE": ""
    }

    save_config(default_config)
    return default_config


def save_config(config_data):
    """Save config into comp333/files/config.json"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"Configuration saved to {CONFIG_FILE}.")
    except Exception as e:
        print(f"Error saving configuration: {e}")


def ensure_config_dir_exists(config_data):
    """Ensure DOWNLOAD_DIR exists"""
    download_dir = config_data.get("DOWNLOAD_DIR")
    if download_dir and not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir)
            print(f"Created download directory: {download_dir}")
        except OSError as e:
            print(f"Failed to create download directory {download_dir}: {e}")
            return False
    return True