import traits

# Implement custom validation logic here
def validateCharacter(character):
  for trait in traits.traitList:
    if character[trait] == "":
      return False

  return True