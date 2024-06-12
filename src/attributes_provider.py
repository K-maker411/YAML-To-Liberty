import json


# TODO - this class may need to stay as-is because it will provide the functionality of handling JSON with the type specifications
class AttributesProvider:

  def __init__(self, attributes):
    # Current structure - attributes is dict of name: open(file_path_for_name, 'r') - this prevents
    # having to constantly modify the constructor and change a billion things, instead we can just add
    # new files to the dictionary in main and then just provide the newly-updated attributes dictionary like normal!
    self.attributes = {name: json.load(opened_file_path) for name, opened_file_path in attributes.items()}

  # e.g. get_attributes("library_level_simple_attributes") -> dictionary of library_level_simple_attributes
  def get_attributes(self, name):
    return self.attributes[name]
    '''
    # Current idea: pull these from the individual
    self.library_level_simple_attributes = json.load(
        library_level_simple_attributes)
    self.library_level_default_attributes = json.load(
        library_level_default_attributes)
    self.library_level_scaling_attributes = json.load(
        library_level_scaling_attributes)
    self.cell_group_simple_attributes = json.load(cell_group_simple_attributes)
    self.pin_group_simple_attributes = json.load(pin_group_simple_attributes)
    self.timing_group_simple_attributes = json.load(
        timing_group_simple_attributes)
    self.timing_group_group_attributes = json.load(
        timing_group_group_attributes)
    self.pin_group_group_attributes = json.load(pin_group_group_attributes)

  def get_library_level_simple_attributes(self):
    return self.library_level_simple_attributes

  def get_library_level_scaling_attributes(self):
    return self.library_level_scaling_attributes

  def get_library_level_default_attributes(self):
    return self.library_level_default_attributes

  def get_cell_group_simple_attributes(self):
    return self.cell_group_simple_attributes

  def get_pin_group_simple_attributes(self):
    return self.pin_group_simple_attributes

  def get_timing_group_simple_attributes(self):
    return self.timing_group_simple_attributes

  def get_timing_group_group_attributes(self):
    return self.timing_group_group_attributes

  def get_pin_group_group_attributes(self):
    return self.pin_group_group_attributes
  '''