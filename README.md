# NFTokenator - an easy-to-use, extensible, and customizable tool for generating NFTs.

### **Author**: Max Eisen

## Requirements
### Dependencies
- Python 3.7 or newer
- Pillow (PIL)
- IPython

### Setup 
- `traits.py` file with your defined traits, layers for each trait and each layer's weight in the form of:  
    ```
    traitList = ["background", "body", "shirt"...]

    background = ["Black And White", "Green And Blue"]
    background_weights = [50, 50]... # must add up to 100
    ```
  **NOTE**: The only required trait is `background` which will be used as the base for the token images.
- `assets` folder with all the possible layers for each trait in the form of:
    `assets > background > BlackAndWhite.png...`  
  **NOTE**: Folder and file names must match exactly with the `traits` file, aside from spaces in trait option names, which will be removed.

## Usage
1. Complete setup section (above)
1. Run `pip install -r requirements.txt`
1. Run `python3 generate.py`