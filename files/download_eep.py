import os
import requests 
import tarfile
from .config_utils import load_config, save_config, ensure_config_dir_exists

def _get_feh_string(index):
    # Maps the user's index (1-15)
    feh_map = {
        1: 'm4.00', 2: 'm3.50', 3: 'm3.00',
        4: 'm2.50', 5: 'm2.00', 6: 'm1.75',
        7: 'm1.50', 8: 'm1.25', 9: 'm1.00',
        10: 'm0.75', 11: 'm0.50', 12: 'm0.25',
        13: 'p0.00', 14: 'p0.25', 15: 'p0.50',
    }
    return feh_map.get(index, None)

# Handles the actual download and extraction
def _fetch_and_extract(url, local_path):
    """
    Downloads the MIST EEPS file (.txz) from the URL, extracts its 
    contents to the download directory, and removes the compressed archive.
    """
    print(f"Starting download from: {url}")
    
    try:
        # 1. Download the compressed file
        response = requests.get(url, stream=True)
        response.raise_for_status() # Catches 4xx/5xx errors
def test_xpath_index(vcrit_choice, metallicity_index):
    """Helper function to test calculation of XPath index.
    
    Arguments:
        vcrit_choice: 'A' or 'B' (v/vcrit value)
        metallicity_index: int from 1-15 for A, 1-16 for B ([Fe/H] selection)
    
    Returns:
        int: XPath index for the download link
    
    Raises:
        ValueError: if inputs are invalid
    """
    # Validate vcrit_choice first
    if vcrit_choice not in ('A', 'B'):
        raise ValueError(f"vcrit_choice must be 'A' or 'B', got {vcrit_choice}")
    
    # Validate metallicity_index type
    if not isinstance(metallicity_index, int):
        raise ValueError(f"metallicity_index must be an integer, got {type(metallicity_index).__name__}")
    
    # Validate metallicity_index is positive
    if metallicity_index < 1:
        raise ValueError(f"metallicity_index must be at least 1, got {metallicity_index}")
    
    # Get the appropriate array and validate range
    if vcrit_choice == "A":
        array = [54,55,56,57,58,59,60,61,62,63,64,65,66,67,68]
        if metallicity_index > 15:
            raise ValueError(f"metallicity_index for vcrit 'A' must be 1-15, got {metallicity_index}")
    else:  # vcrit_choice == "B"
        array = [69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84]
        if metallicity_index > 16:
            raise ValueError(f"metallicity_index for vcrit 'B' must be 1-16, got {metallicity_index}")
    
    return int(array[metallicity_index - 1])

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Download complete. File saved temporarily to: {local_path}")
        
        # 2. Extract the file contents
        # Extracts to the parent directory (the DOWNLOAD_DIR)
        extract_dir = os.path.dirname(local_path) 
        print(f"Extracting contents to: {extract_dir}")
        
        # Use 'r:xz' for tar archive compressed with xz
        with tarfile.open(local_path, 'r:xz') as tar:
            tar.extractall(path=extract_dir) 
            
        print("Extraction complete. Cleaning up compressed file.")
        
        # 3. Clean up the compressed archive
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

# Handles user interaction and configuration
def download_eep():
    """
    Handles downloading MIST EEPS files with a customizable menu.
    """
    config = load_config()
    download_dir = config.get("DOWNLOAD_DIR")
    
    if not ensure_config_dir_exists(config):
        print("Cannot proceed without a valid download directory.")
        return

    # Custom File Selection Menu
    print("\n--- Select Custom EEPS File ---")
    
    # Rotation Selection
    print("What evolutionary track would you like to download: ")
    print("A: v/vcrit = 0.4 ")
    print("B: v/vcrit = 0.0 ")
    
    user_input1 = input("Select A or B (case sensitive). ").strip()
    while user_input1 not in ["A", "B"]:
        user_input1 = input("Not a valid input, please select A or B. ").strip()
        
    # Metallicity Selection
    print("\nWhat [Fe/H] would you like: ")
    print("1. [Fe/H] = -4.00 \t 2. [Fe/H] = -3.50 \t 3. [Fe/H] = -3.00")
    print("4. [Fe/H] = -2.50 \t 5. [Fe/H] = -2.00 \t 6. [Fe/H] = -1.75")
    print("7. [Fe/H] = -1.50 \t 8. [Fe/H] = -1.25 \t 9. [Fe/H] = -1.00")
    print("10. [Fe/H] = -0.75 \t 11. [Fe/H] = -0.50 \t 12. [Fe/H] = -0.25")
    print("13. [Fe/H] = +0.00 \t 14. [Fe/H] = +0.25 \t 15. [Fe/H] = +0.50")
    
    try:
        user_input2 = int(input("Select a valid number index (1-15) for [Fe/H]: ").strip())
        while user_input2 not in range(1, 16):
            user_input2 = int(input("Not a valid input, try again. Select a valid number index (1-15) for [Fe/H]: ").strip())
    except ValueError:
        print("Invalid input. Returning to main menu.")
        return

    # Construct Filename and Check Existence
    vvcrit = "0.4" if user_input1 == "A" else "0.0"
    feh_code = _get_feh_string(user_input2)
    download_filename = f"MIST_v1.2_feh_{feh_code}_afe_p0.0_vvcrit{vvcrit}_EEPS.txz"
    local_path = os.path.join(download_dir, download_filename)
    
    # We check if the extracted content exists, not the deleted .txz archive.
    base_name = download_filename.rsplit('.', 1)[0]
    
    # Check if a file or directory that starts with the base name exists in the download directory
    # This assumes the extracted data starts with the compressed file's name (without the extension).
    try:
        extracted_content_exists = any(f.startswith(base_name) for f in os.listdir(download_dir))
    except FileNotFoundError:
        # Should be caught by ensure_config_dir_exists, but defensive check
        extracted_content_exists = False 

    if extracted_content_exists:
        print(f"\nRequired data for '{base_name}' already exists in: {download_dir}. Skipping download.")
        return
        
    # Final Prompt (Only if file is missing)
    
    # Ask to save this as the new default
    save_default = input(f"\nSave '{download_filename}' as the new default EEPS file? (Y/N): ").strip().lower()
    if save_default == 'y':
        config["DEFAULT_EEPS_FILE"] = download_filename
        save_config(config)
        print("Configuration updated.")
        
    prompt = input(f"File is missing. Download '{download_filename}'? (Y/N): ").strip().lower()
    if prompt in ['y', '']:
        return _execute_download(config, download_filename, local_path)
    else:
        print("\nDownload aborted. Returning to main menu.")
        return


def _execute_download(config, filename, local_path):
    """
    Constructs the download URL using the proven direct tarballs path.
    """
    base_url = config.get("MIST_BASE_URL")
    
    # No extra folder logic needed! The URL is now simply BaseURL + Filename
    folder = "" 

    download_url = f"{base_url}{folder}{filename}" 
    print(f"Attempting download from: {download_url}")
    
    return _fetch_and_extract(download_url, local_path)