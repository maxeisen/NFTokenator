'''
NFTokenator - an easy-to-use, extensible, and customizable tool for generating NFTs.

Author: Max Eisen
Updated: May 27, 2022

Requirements:
- Python 3.7 or newer
- Pillow (PIL)
- Progress
- NumPy
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
from progress.bar import IncrementalBar
import numpy
from validate import validateCharacter
import random
import json
import time
import re
import os

allCharacters = []

# Prompting for project name
PROJECT_NAME = re.sub(r'[\W_]+', '', input("Enter a name for your NFT project: ").replace(" ", ""))

# Walk assets folder to calculate maximum collection size
def getMaxCollectionSize(cwd='assets'):
  traitLayerCounts = []
  for subdir in os.listdir(cwd):
    if os.path.isdir(f'{cwd}/{subdir}'):
      traitLayerCounts.append(len([file for file in os.listdir(f'{cwd}/{subdir}')]))
    else:
      continue
  return(numpy.prod(traitLayerCounts))

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

# Count total number of each trait option
def countTraits():
  traitCounts = {}
  for trait in traits.traitList:
    currentTraitCount = {}
    for character in allCharacters:
      if character[trait] in currentTraitCount:
        currentTraitCount[character[trait]] += 1
      else:
        currentTraitCount[character[trait]] = 1
    traitCounts[trait] = currentTraitCount
  try:
    with open(f'./{PROJECT_NAME}_files/rarities.json', 'w') as outfile:
      json.dump(traitCounts, outfile, indent=4, sort_keys=False)
    print(f'\nRarities written to {PROJECT_NAME}_files/rarities.json\n')
  except:
    print("\nAn error occurred while writing the rarities file.")

# Generate and save a token image for a given character
def generateToken(character):
  # print(f'\nGenerating token #{character["id"]}.')
  background = Image.open(f'./assets/background/{character["background"].replace(" ","")}.png').convert('RGBA')
  for key in character:
    if key == "background":
      composite = background
      continue
    elif key == "id":
      continue
    trait = Image.open(f'./assets/{key}/{character[key].replace(" ", "")}.png').convert('RGBA')
    composite = Image.alpha_composite(composite, trait)
  # print(f'Token #{character["id"]} generated.')
  
  token = composite.convert('RGB')
  filename = PROJECT_NAME + "_" + str(character["id"]) + ".png"
  token.save(f'./{PROJECT_NAME}_files/tokens/{filename}')
  # print(f'Token #{character["id"]} saved.')

class ProgressBar(IncrementalBar):
    suffix = 'Estimated time remaining: %(custom_eta)s'
    @property
    def custom_eta(self):
      return (str(self.eta//60)+' minutes') if (self.eta > 60) else (str(self.eta)+' seconds')

def main():
  collectionSize = 0
  validCollectionSize = False

  # Prompting number of tokens to generate
  while (not validCollectionSize):
    try:
      print(f'\nThe maximum size of this collection, based on provided assets, is {maxCollectionSize} tokens.')
      collectionSize = input("How many tokens would you like to generate? (Leave blank for maximum) ")
      if (collectionSize == "") or (int(collectionSize) == maxCollectionSize):
        print(f'\n{maxCollectionSize} tokens will be generated.')
        print("\nWARNING: This ignores rarities and will generate every possible combination for the collection.")
        print("It also may take a long time.")
        print("Press ctrl+c to cancel.")
        time.sleep(8)
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
    except:
      print("\n\nScript has stopped. Please try again.")
      exit()

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

  # Create project directories
  if not os.path.exists(f'./{PROJECT_NAME}_files'):
    os.mkdir(f'./{PROJECT_NAME}_files')
  if not os.path.exists(f'./{PROJECT_NAME}_files/tokens'):
    os.mkdir(f'./{PROJECT_NAME}_files/tokens')

  # Write trait counts to rarities JSON file
  countTraits()
  
  # Generate tokens for each character
  try:
    bar = ProgressBar('Generating token %(index)d/%(max)d', max=collectionSize)
    for character in allCharacters:
      generateToken(character)
      bar.next()
    bar.finish()
    print(f'\n\nAll {collectionSize} tokens were successfully generated and saved to the \'{PROJECT_NAME}_files/tokens\' folder. Enjoy!\n')
  except:
    print("\n\nAn error occurred while generating tokens. Please try again.")

if __name__ == "__main__":
  main()
