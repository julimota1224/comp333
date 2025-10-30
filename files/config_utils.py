import json
import os

CONFIG_FILE = 'config.json'

def get_default_download_dir():
    """
    Returns a system-independent default download directory:
    A folder named 'MIST_Data' inside the current user's home directory.
    This avoids permission issues tied to specific user paths.
    """
    # Uses '~' which expands to the current user's home directory (e.g., /Users/currentuser)
    home_dir = os.path.expanduser('~')
    
    # We create a sub-directory for the MIST data inside the home directory
    return os.path.join(home_dir, 'MIST_Data') 

def load_config():
    """
    Loads the configuration from config.json.
    Returns default settings if the file doesn't exist.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        # Fallback to a system-independent default
        print(f"Configuration file '{CONFIG_FILE}' not found. Using system default path.")
        
        # This new dictionary uses the generic path calculated above
        default_config = {
            "DOWNLOAD_DIR": get_default_download_dir(),
            "MIST_BASE_URL": "http://waps.cfa.harvard.edu/MIST/models/v1.2/",
            "DEFAULT_EEPS_FILE": "MIST_v1.2_feh_p0.00_afe_p0.0_vvcrit0.0_EEPS.txz",
            "DEFAULT_ISO_FILE": "MIST_v1.2_vvcrit0.4_UBVRIplus.txz"
        }
        # It's good practice to save this default config immediately
        save_config(default_config) 
        return default_config

def save_config(config_data):
    """
    Saves the current configuration dictionary to config.json.
    """
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"Configuration saved to {CONFIG_FILE}.")
    except Exception as e:
        print(f"Error saving configuration: {e}")

def ensure_config_dir_exists(config_data):
    """
    Checks if the DOWNLOAD_DIR specified in the config exists, and creates it if not.
    """
    download_dir = config_data.get("DOWNLOAD_DIR")
    if download_dir and not os.path.exists(download_dir):
        try:
            os.makedirs(download_dir)
            print(f"Created download directory: {download_dir}")
        except OSError as e:
            print(f"Failed to create download directory {download_dir}: {e}")
            return False
    return True