# COMP333 Tracking Young Stars
Automated MIST Evolutionary Track & Isochrone Processing


## Coding Standards
For coding standards, please refer to our [Python Style Guide](StyleGuide.md).


## Creators
- **nalam309: Nadia Alam**
- **xaviermkim: Xavier Kim**
- **julimota1224: Julissa Mota**


## Program Overview
Astronomers frequently rely on MESA Isochrones & Stellar Tracks (MIST) to compare stellar luminosities, temperatures, masses, and ages. However, downloading, extracting, parsing, and plotting these files manually is slow, error-prone, and dependent on remembering complex MIST naming conventions. This package automates the entire workflow.


## What the Tool Does
1. Downloads MIST evolutionary tracks (EEPS) and isochrones via HTTPS
2. Automatically extracts `.txz` archives and detects extracted directories
3. Loads evolutionary tracks and interpolates between stellar masses
4. Plots:
   - Evolutionary mass tracks
   - Interpolated mass tracks (when required)
   - Isochrones at selected stellar ages
   - HR diagrams with observational constraints

 
## Major Improvements Over the Original Version
- Removed Selenium and browser automation
- Removed menu-based, interactive input
- Replaced all runtime prompts with a configuration-driven workflow
- Supports plotting **multiple metallicities on the same HR diagram**
- Supports plotting **incomplete observational constraints**
- Uses continuous curves instead of marker-based tracks
- Uses physically motivated axis bounds to emphasize the low-mass regime
- Fully reproducible runs with no user input required at runtime


## Installation
### 1. Clone the Repository
Using VS Code:
Clone Git Repository → enter the repo URL

Or in terminal:
git clone <repo-url>
cd comp333

### 2. Install Dependencies
pip install matplotlib astropy fastnumbers numpy requests

### 3. Verify Python Version
You need Python 3.9 or newer.

Check with:
python3 --version

## Configuration Files
The software uses two configuration files.

### 1. System Configuration (auto-generated)
Location: comp333/files/config.json
This file stores machine-specific settings such as the download directory and MIST base URL. It is created automatically on first run and should not be committed to version control.

### 2. User Run Configuration
Location: run_config.json

This file controls:
- Which MIST files are downloaded
- Which metallicities are plotted
- Which stellar masses are plotted or interpolated
- Age ranges for evolutionary tracks
- Isochrone age ranges
- HR diagram labels
- Observational constraints
  
A fully commented example is provided in:
run_config_template.jsonc

Create your own editable configuration with:
cp run_config_template.jsonc run_config.json

## Running the Program
From the directory containing the comp333/ package:
python3 -m comp333.master run_config.json

The program will:
- Download missing MIST files
- Extract archives automatically
- Plot evolutionary tracks for each requested metallicity
- Plot isochrones for each requested metallicity and age
- Overlay observational constraints

## Interpreting Multi-Metallicity Plots
When multiple metallicities are provided:
- Each metallicity produces its own set of mass tracks
- Each metallicity produces its own set of isochrones
- Labels explicitly indicate [Fe/H] values
  
The total number of curves plotted is:
(# metallicities) × (# masses) + (# metallicities) × (# isochrone ages)

Users may reduce visual complexity by:
- Using a single metallicity
- Setting age_min == age_max to plot a single isochrone per metallicity

## Observational Constraints
The software supports incomplete data commonly found in the literature, including:
- Exact HR points
- Temperature-only constraints
- Luminosity-only constraints
- Rectangular uncertainty regions
Unsupported or malformed constraints are skipped with a warning rather than causing the program to fail.

## Output
The program produces HR diagrams with:
- Physically correct axis orientation
- Evolutionary and interpolated mass tracks
- Isochrones from tabulated stellar models
- Optional observational constraints

## Testing
Legacy tests from the original Selenium version are included:
- test_make_driver.py — tests WebDriver logic
- test_xpath_function.py — tests the metallicity index handling logic

Run them with:
python3 test_make_driver.py
python3 test_xpath_function.py

These tests are no longer essential for the new automated workflow but remain for historical completeness.

## Help for New Terminal Users
If you are new to command-line work, this guide may help:

The Terminal: First Steps & Useful Commands
https://realpython.com/terminal-commands/
