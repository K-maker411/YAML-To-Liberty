import json

# TODO - this class may need to stay as-is because it will provide the functionality of handling JSON with the type specifications
class AttributesProvider:
  def __init__(self, library_level_simple_attributes, library_level_scaling_attributes, library_level_default_attributes):
    # Current idea: pull these from the individual 
    self.library_level_simple_attributes = json.load(library_level_simple_attributes)
    self.library_level_default_attributes = json.load(library_level_default_attributes)
    self.library_level_scaling_attributes = json.load(library_level_scaling_attributes)
    

  def get_library_level_simple_attributes(self):
    return self.library_level_simple_attributes

  def get_library_level_scaling_attributes(self):
    return self.library_level_scaling_attributes

  def get_library_level_default_attributes(self):
    return self.library_level_default_attributes