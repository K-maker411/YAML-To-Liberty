import yaml
import numbers

class YamlToLibertyWriter:
  def __init__(self, yaml_file_read_stream):
    self.yaml_file = yaml.safe_load(yaml_file_read_stream)
    
  # ints, floats, or strings are simple because they're non-nested
  # TODO - is this bad design? Probably not a huge deal, but worth checking
  def is_simple_attribute(self, attr):
    return isinstance(attr, (numbers.Number, str))

  # list and dicts are complex
  # TODO - is this bad design? Probably not a huge deal, but worth checking
  def is_complex_attribute(self, attr):
    return isinstance(attr,  (list, dict))
  
  # "simple" is defined as non-list/dictionary/nested structure
  def get_simple_library_level_attributes(self):
    simple_attrs_string = ""
    for attr in self.yaml_file.get("library"):
      if self.is_simple_attribute(attr):
        # TODO - add code for this later
        pass
      else:
        return simple_attrs_string

  def get_full_library(self):
    full_lib = ""
    full_lib += "library(" + self.yaml_file.get("library").get("name") + ") {"
    # add the rest of the stuff here (in a while, crocodile)
    full_lib += "\n"
    return full_lib
    
    