# COMP333 Tracking Young Stars

## Coding Standards

For coding standards, please refer to our [Python Style Guide](StyleGuide.md).

## Creators
nalam309: Nadia Alam

xaviermkim: Xavier Kim

julimota1224: Julissa Mota

## Program Overview
A Python-based software package to compare measured stellar properties of luminosity, temperature, and mass with astrophysical models from the MIST databases, and this would result in plotting results on an HR diagram.

The program is capable of:
- Downloading a real MIST dataset automatically using Selenium
- Extracting and visualizing stellar evolutionary track and isochrone data
- Run a dummy demonstration of the data
- Guide users through each step interactively using a terminal-line menu. 

## User Guide

    Before you begin:
    - Make sure you have Python 3 and pip installed and up to date.
      You can check this by running "python 3--version" and "python 3 -m pip install --upgrade pip"
    - If you are new to using the terminal or command line see: 
     [The Terminal: First Steps and Useful Commands]([(https://realpython.com/terminal-commands/]))
    for a quick walkthrough of cloning repositories, navigating directories, and running programs.
    - The program currently requires Google Chrome for automation. If you don't have it installed you can download it here: 
    https://www.google.com/chrome/dr/download/?brand=FKPE&ds_kid=11256481&gclsrc=aw.ds&gad_source=1&gad_campaignid=19930262352&gbraid=0AAAAAoY3CA5BjQIZOa2txPljSN1NX2hfR&gclid=Cj0KCQiAq7HIBhDoARIsAOATDxDr5nNOYgU0xY9lAJVL2bBd3QyHYKrIcOcoyvgjc2WAsLyaT6dxRUgaAghUEALw_wcB
    
    
    1. Clone the Repository: Clone the main repository to your local machine. 
    Open up VS Code, click on "Clone Git Repository", and enter the repository's URL. 
    
    2. Install all required packages: matplotlib, astropy, fastnumbers. 
    You can do this by running in your terminal in bash the 
    following command: "pip install matplotlib astropy fastnumbers"
    
    3. Run the Script: Once you are on the Feature-1 branch, run the program by entering:
    python3 master.py
    You can now use the package as usual, testing Option 1 (EEPS) and Option 2 (Isochrone) downloads. 
    You should notice the files are downloaded much faster, and the new menus automatically construct the correct file
    names.
        
    You will see the following menu:
    1. Download evolutionary track files
    2. Download isochrone files
    3. Input data for evolutionary track curves
    4. Input data for isochrone curves
    5. Plot all
    6. Quit

    Each option guides you through a short sequence of user inputs to simulate data handling:
    Option 1: Demonstrates how evolutionary tracks would be downloaded
    Option 2: Demonstrates how isochrone files would be downloaded
    Option 3: Simulates entering data for evolutionary track plotting
    Option 4: Simulates entering data for isochrone plotting. 
    Option 5: Creates a combined plot of both data sets
    Option 6: Exits the program

    * It should be noted that in this skeletal version of the code, no real data or files are required.
    When the program asks for an absolute path (i.e, in option 3 or 4). 
    Entering any valid path (e.g., /Users/test/dummy.txz) 
    will allow the code to run through the program and sufficiently show you an example of a graph. 
    Additionally, the "download" options simulate the download process rather than saving actual files; 
    files are not yet saved locally, and future versions will store downloaded data more efficiently. 

    Option Exploration:
    Option 1: Downloading evolutionary track files
    *After following the initial installation steps
    1.  Type 1  and press Enter.
    2. Follow on-screen prompts: Which evolutionary track do you wish to download    
    and the index for what Fe/H you would like?
    3. When the download is completed, a message will be printed that states the 
    following: "Link clicked; check your downloads folder/browser for the file
    
    Option 2: Downloading isochorone files
    *After following the initial installation steps
    1. Type 2 and press Enter.
    2. Follow on-screen prompts: Which Isochrone track would you like to download?
    3. When the download is completed, a message will be printed that states that
    "Isochrone link clicked; check your browser/downloads settings. 
    
    Option 3: Inputting data for evolutionary track curves
    *After following the initial installation steps
    1. Type 3 and press Enter
    2. Follow on-screen prompts; Enter the absolute path to your downloaded evolutionary track file, 
    input the minimum eep mass curve you want to highlight, and input the maximum eep mass curve you want to highlight
    3. Once the program verifies the dummy plot (no real file path is required), a  plot will appear.
    
    Option 4: Inputting data for isochrone curves
    *After following the initial installation steps
    1. Type 4 and press enter
    2. Follow the onscreen prompts: Choose a metallicity value [Fe/H] from a numbered list (1–15), 
    enter minimum age, maximum age, minimum mass, and maximum mass.
    3. A  plot will appear. 
    
    Option 5: Plotting all data
    *After following the initial installation steps
    1. Type 5 and press Enter
    2. The program will simulate combining the previously entered evolutionary track and isochrone data. 
    3. Follow on-screen prompts: Effective temperature, the error for effective     temperature, biometric 
    luminosity of the star, the error for biometric luminosity, name for the point, graph title, x label, y label. 
    3. A plot will appear. 
    Note: After viewing the plot, the program closes automatically instead of returning to the menu.
    To continue, re-run: "python3 master.py"

    Option 6: Quit
    Ends the program 





    

