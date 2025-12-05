# COMP333 Tracking Young Stars
Automated MIST Evolutionary Track & Isochrone Processing

## Coding Standards
For coding standards, please refer to our [Python Style Guide](StyleGuide.md).

## Creators
nalam309: Nadia Alam
xaviermkim: Xavier Kim
julimota1224: Julissa Mota

## Program Overview
Astronomers frequently rely on MESA Isochrones & Stellar Tracks (MIST) to compare stellar luminosities, temperatures, masses, and ages. However, downloading, extracting, parsing, and plotting these files manually is slow, error-prone, and dependent on remembering complex MIST naming conventions.

What the tool does:
- Downloads MIST evolutionary tracks (EEPS) and isochrones directly via HTTPS
- Extracts .txz archives and auto-detects extracted directories
- Loads and interpolates evolutionary tracks between masses
- Plots:
 - EEP curves
 - Interpolated mass curves
 - Isochrones at user-selected ages
 - HR diagrams with custom star points
 
Summary of major improvements:
- Removed Selenium entirely
- Removed the menu-based interface
- Replaced all interactivity with a clean configuration-driven workflow
- All user settings are stored in run_config.json
- Updated plotting style with cleaner formatting and optional filled interpolation regions
- Runs are fully reproducible and require no user input at runtime

## Installation

1. **Clone the Repository**:
Using VS Code:
Clone Git Repository → enter the repo URL

Or in terminal:
git clone <repo-url>
cd comp333

2. **Install Dependencies**:
pip install matplotlib astropy fastnumbers numpy requests

3. **Verify Python Version**:
You need Python 3.9 or newer.

Check with:
python3 --version

### How the Program Works:
The software uses two configuration files.

1. System Config (auto-generated): comp333/files/config.json

Created automatically on the first run.
It stores:
- The download directory (default: ~/MIST_Data)
- The MIST base URL
- Default filenames (if applicable)
- You normally do not need to edit this file.

2. User Run Config: run_config.json

This file controls:
- Whether to download EEPs
- Whether to download Isochrones
- v/vcrit values
- Metallicity
- Mass codes for EEP plotting
- Isochrone age to use
- HR diagram labels
- Custom stars with errors

A fully commented example template is included: run_config_template.jsonc

To create an editable copy:
cp run_config_template.jsonc run_config.json

## Running the Program
Run from the directory containing the comp333/ package:
python3 -m comp333.master comp333/run_config.json

The command will:
- Parse your run configuration
- Download missing EEPS files
- Download missing Isochrone files
- Extract .txz archives
- Identify all necessary extracted directories
- Generate:
 - Evolutionary track curves
 - Interpolated mass curves
 - Isochrone curve at the selected age
 - HR diagram with your custom star points

A matplotlib window will appear.
Close the window to return control to the terminal.

## Editing run_config.json
Below is a simplified sample structure:

{
  "eep_download": { "run": true, "vcrit": "0.4", "feh": -0.25 },

  "iso_download": { "run": true, "vcrit": "0.0" },

  "eep_plot": { "run": true },

  "eep_plot_settings": {
    "min_mass": 1.00,
    "max_mass": 5.00,
    "age_min": 1000000,
    "age_max": 30000000,
    "fill_between": true
  },

  "iso_plot": {
    "run": true,
    "iso_directory": "/Users/.../MIST_v1.2_vvcrit0.0_UBVRIplus",
    "age": 9.0
  },

  "points": [
    { "name": "Star 1", "x": 3.75, "y": 1.20, "x_err": 0.05, "y_err": 0.10 }
  ]
}

Everything is explicit.
There are no menus, prompts, or filename guessing.

## Output
The program produces:
- Evolutionary track curves
- Interpolated mass curves
- Isochrone curves at a chosen log(age)
- HR diagrams with proper axes and inverted temperature scale
- Optional star overlays with error bars

## Testing
Legacy tests from the original Selenium version are included:
- test_make_driver.py — tests WebDriver logic
- test_xpath_function.py — tests the metallicity index handling logic

Run them with:
python3 test_make_driver.py
python3 test_xpath_function.py

These tests are no longer essential for the new automated workflow but remain for historical completeness.

### Help for New Terminal Users
If you are new to command-line work, this guide may help:

The Terminal: First Steps & Useful Commands
https://realpython.com/terminal-commands/