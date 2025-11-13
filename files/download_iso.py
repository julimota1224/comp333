import os
import requests 
import tarfile
from .config_utils import load_config, save_config, ensure_config_dir_exists

# Handles the actual download and extraction
def _fetch_and_extract(url, local_path):
    """
    Downloads the MIST Isochrone file (.txz) from the URL, extracts its 
    contents to the download directory, and removes the compressed archive.
    """
    print(f"Starting download from: {url}")
    
    try:
        # Download the compressed file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Download complete. File saved temporarily to: {local_path}")
        
        # Extract the file contents
        extract_dir = os.path.dirname(local_path) 
        print(f"Extracting contents to: {extract_dir}")
        
        with tarfile.open(local_path, 'r:xz') as tar:
            tar.extractall(path=extract_dir) 
            
        print("Extraction complete. Cleaning up compressed file.")
        
        # Clean up the compressed archive
        os.remove(local_path)
        
        return True

    except requests.exceptions.RequestException as e:
        print(f"Network Error during download. Check URL and connection: {e}")
        return False
    except tarfile.TarError as e:
        print(f"Extraction Error (Is the downloaded file a valid .txz archive?): {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during file processing: {e}")
        return False

# Handles the download URL construction
def _execute_download(config, filename, local_path):
    """
    Internal function to construct URL and execute the download.
    """
    base_url = config.get("MIST_BASE_URL")
    # Using the simplified path (BaseURL + Filename)
    folder = "" 
    download_url = f"{base_url}{folder}{filename}"

    print(f"Attempting download from: {download_url}")
    return _fetch_and_extract(download_url, local_path)


# Handles user interaction and configuration
def download_isochrone():
    """
    Handles downloading MIST Isochrone files with v/vcrit selection.
    """
    config = load_config()
    download_dir = config.get("DOWNLOAD_DIR")
    
    if not ensure_config_dir_exists(config):
        print("Cannot proceed without a valid download directory.")
        return

    print("\n--- Select Isochrone File ---")
    
    print("What Isochrone track would you like to download: ")
    print("A: v/vcrit = 0.4 (Default) ")
    print("B: v/vcrit = 0.0 ")

    user_input = input("Select A or B (case sensitive). ").strip()
    while user_input not in ["A", "B"]:
        user_input = input("Not a valid input, please select A or B. ").strip()

    # Construct Filename
    vvcrit = "0.4" if user_input == "A" else "0.0"
    
    # Filename pattern: MIST_v1.2_vvcrit0.4_UBVRIplus.txz (or vvcrit0.0)
    download_filename = f"MIST_v1.2_vvcrit{vvcrit}_UBVRIplus.txz"
    local_path = os.path.join(download_dir, download_filename)

    # Check for extracted files, not the temporary .txz archive.
    base_name = download_filename.rsplit('.', 1)[0]
    
    try:
        extracted_content_exists = any(f.startswith(base_name) for f in os.listdir(download_dir))
    except FileNotFoundError:
        extracted_content_exists = False

    if extracted_content_exists:
        print(f"\nRequired data for '{base_name}' already exists in: {download_dir}. Skipping download.")
        return
    
    # Final Prompt & Execution
    
    # Ask to save this as the new default
    save_default = input(f"\nSave '{download_filename}' as the new default Isochrone file? (Y/N): ").strip().lower()
    if save_default == 'y':
        config["DEFAULT_ISO_FILE"] = download_filename
        save_config(config)
        print("Configuration updated.")
        
    prompt = input(f"File is missing. Download '{download_filename}'? (Y/N): ").strip().lower()
    if prompt in ['y', '']:
        return _execute_download(config, download_filename, local_path)
    else:
        print("\nDownload aborted. Returning to main menu.")
        return