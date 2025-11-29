# COMP333 Tracking Young Stars

## Coding Standards
For coding standards, please refer to our [Python Style Guide](StyleGuide.md).

## Creators
nalam309: Nadia Alam
xaviermkim: Xavier Kim
julimota1224: Julissa Mota

## Program Overview
This package automates scientific data handling for stellar evolution research using the MESA Isochrones & Stellar Tracks (MIST) database. It allows users to:

- Automatically download evolutionary tracks (EEPS) and isochrones
- Extract MIST .txz archives
- Plot evolutionary tracks, interpolated curves, and HR diagrams
- Overlay user-specified stars on an HR diagram
- Control all behavior through a single configuration file (run_config.json)

This version removes the old menu-style interface and replaces it with a clean, automated, config-driven workflow.

## Installation

1. **Clone the Repository**:
In VS Code:
Clone Git Repository → enter the repo URL

Or via terminal:
git clone <repo-url>
cd comp333

2. **Install Dependencies**:
pip install matplotlib astropy fastnumbers numpy

3. **Verify Python**:
You need:
Python 3.9+

Check with:
python3 --version

### How the program works:
The system is controlled by two configuration files:

1. System Config (auto-generated)： config.json

Created on the first run. It stores:

- download directory (~/MIST_Data)
- base URL for MIST tarballs
- default filenames (optional)

You do not need to modify this file.

2. User Run Config： run_config.json

This is your main script. It tells the program:

- What to download
- What to plot
- What ages/masses to use
- What stars to overlay
- Where the isochrone data is stored

You fully control the program by editing this file.

A commented example is included as:
run_config_template.jsonc

Copy it to create your own:
cp run_config_template.jsonc run_config.json

## Running the Program
From inside the directory containing the comp333/ folder:
python3 -m comp333.master run_config.json

The script will:
- Parse your run config
- Download missing MIST data
- Extract and validate files
- Plot evolutionary tracks
- Plot isochrones at your selected age
- Overlay any custom stars
- Show a final HR diagram

Close the matplotlib window to return control to the terminal.

## Testing
Two unit tests are available:
1. test_make_driver.py which tests WebDriver logic
2. test_xpath_function.py which tests XPath calculation for identifying metallicity index positions

Run tests with:
python3 test_make_driver.py
python3 test_xpath_function.py

### Help for New Terminal Users
If you are new to command-line interfaces, this quick guide is helpful:

The Terminal: First Steps & Useful Commands
https://realpython.com/terminal-commands/