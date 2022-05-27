'''
These are example traits and their weights, in the required format for the generator.
Customize these however you please, but make sure there is at least a 'background' trait defined, as the generator will not work without it.

To use this file for the generator, remove 'example_' from the filename.
'''

traitList = ["background", "body", "face"] # This should be in the order you want the layers to be placed, starting with background

background = ["Light Blue Sample", "Purple Sample", "RGB Sample"]
background_weights = [40, 40, 20]

body = ["Black and Green Sample", "Pink and Brown Sample", "Yellow Sample"]
body_weights = [10, 30, 60]

face = ["Grey Mischievous Sample", "Lavender Angry Sample", "Red Apathetic Sample"]
face_weights = [40, 35, 25]