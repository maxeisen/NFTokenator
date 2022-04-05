'''
NFTokenator - an easy-to-use, extensible, and customizable tool for generating NFTs.

Author: Max Eisen
Updated: April 5, 2022

Requirements:
- Python 3.7 or newer
- Pillow (PIL)
- 'traits.py' file with your defined traits, layers for each trait and each layer's weight in the form of:
  traitList = ["background", "body", "shirt"...]
  background = ["Black And White", "Green And Blue"]
  background_weights = [50, 50]... # must add up to 100
  NOTE: The only required trait is 'background' which will be used as the base for the token images.
- 'assets' folder with all the possible layers for each trait in the form of:
  assets > background > BlackAndWhite.png...
  NOTE: Folder and file names must match exactly with the 'traits' file, aside from spaces in trait option names, which will be removed.

Usage
1. Complete setup section (above)
2. Run `pip install -r requirements.txt`
3. Run `python3 generate.py`
'''

import traits
from PIL import Image
from validate import validateCharacter
import random
import math
import time
import os

allCharacters = []

# Walk assets folder to calculate maximum collection size
def getMaxCollectionSize(cwd='assets'):
  traitLayerCounts = []
  for subdir in os.listdir(cwd):
    if os.path.isdir(f'{cwd}/{subdir}'):
      traitLayerCounts.append(len([file for file in os.listdir(f'{cwd}/{subdir}')]))
    else:
      continue
  return(math.prod(traitLayerCounts))

maxCollectionSize = getMaxCollectionSize()

# Create the characters by randomly combining select traits according to defined weights
def createCharacter():
  character = {}
  for trait in traits.traitList:
    character[trait] = random.choices(traits.__dict__[trait], traits.__dict__[trait + "_weights"])[0]

  # Check that character does not exist and is valid
  if (character in allCharacters) or (not validateCharacter(character)):
    return createCharacter()
  else:
    return character

# Check if all characters are unique
def characterUniqueCheck(characterList):
    checked = list()
    return not any(i in checked or checked.append(i) for i in characterList)

# Generate and save a token image for a given character
def generateToken(character):
  print(f'\nGenerating token #{character["id"]}.')
  background = Image.open(f'./assets/background/{character["background"].replace(" ","")}.png').convert('RGBA')
  for key in character:
    if key == "background":
      composite = background
      continue
    elif key == "id":
      continue
    trait = Image.open(f'./assets/{key}/{character[key].replace(" ", "")}.png').convert('RGBA')
    composite = Image.alpha_composite(composite, trait)
  print(f'Token #{character["id"]} generated.')
  
  token = composite.convert('RGB')
  filename = str(character["id"]) + ".png"
  token.save("./tokens/" + filename)
  print(f'Token #{character["id"]} saved.')

def main():
  collectionSize = 0
  validCollectionSize = False

  # Prompting number of tokens to generate
  while (not validCollectionSize):
    try:
      print(f'The maximum size of this collection, based on provided assets, is {maxCollectionSize} tokens.')
      collectionSize = input("How many tokens would you like to generate? (Leave blank for maximum) ")
      if collectionSize == "":
        print(f'\n{maxCollectionSize} tokens will be generated.')
        collectionSize = maxCollectionSize
        validCollectionSize = True
      elif int(collectionSize) > maxCollectionSize:
        print(f'\nThis is greater than the maximum collection size. {maxCollectionSize} tokens will be generated.')
        time.sleep(2)
        collectionSize = maxCollectionSize
        validCollectionSize = True
      else:
        collectionSize = int(collectionSize)
        print(f'\n{collectionSize} tokens will be generated.')
        validCollectionSize = True
    except ValueError:
      print("\nPlease enter a valid number.")
      collectionSize = 0
      time.sleep(1)

  # Create defined number of characters
  for i in range(int(collectionSize)):
    character = createCharacter()
    allCharacters.append(character)

  # Check uniqueness of each character
  charactersUnique = characterUniqueCheck(allCharacters)
  print(f'\n{collectionSize} generated characters were found to be {"unique and valid. Generating tokens..." if charactersUnique else "not unique. Regenerating characters..."}.')
  time.sleep(2)

  # Assign unique id to each character
  if charactersUnique:
    i = 0
    for item in allCharacters:
        item["id"] = i
        i = i + 1

  # Generate token images for each character
  if not os.path.exists('./tokens'):
    os.mkdir(f'./tokens')
  try:
    for character in allCharacters:
      generateToken(character)
    print("\n\nAll tokens were successfully generated and saved to the 'tokens' folder. Enjoy!")
  except:
    print("\n\nAn error occurred while generating tokens. Please try again.")

if __name__ == "__main__":
  main()
