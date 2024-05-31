# TODO - this class doesn't need to exist separately - including it as part of YamlParser would make 
# more sense and keep the code simpler
class AttributesProvider:
  def __init__(self, library_level_simple_attributes, library_level_scaling_attributes, library_level_default_attributes):
    # Current idea: these will be individual sets, since the order will be based on what the YAML has
    self.library_level_simple_attributes = {line.strip() for line in library_level_simple_attributes}
    self.library_level_scaling_attributes = {line.strip() for line in library_level_scaling_attributes}
    self.library_level_default_attributes = {line.strip() for line in library_level_default_attributes}

  def get_library_level_simple_attributes(self):
    return self.library_level_simple_attributes

  def get_library_level_scaling_attributes(self):
    return self.library_level_scaling_attributes

  def get_library_level_default_attributes(self):
    return self.library_level_default_attributes