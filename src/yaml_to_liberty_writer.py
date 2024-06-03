import yaml

# MOST IMPORTANTLY - don't obssess about making the code perfect on the first try, let's just get it working first! I
# can always go back and change stuff later to make it prettier :)

class YamlToLibertyWriter:
  def __init__(self, yaml_file_read_stream, attributes_provider):
    self.yaml_file = yaml.safe_load(yaml_file_read_stream)
    self.attributes_provider = attributes_provider

  # current idea: for non-complex and non-group attributes, go by type(s) (unless something special)
  # for complex and group, create a function for each and look at the types of the inputs and process them through the "get___as_string" functions to create one "big" string for each of those attributes
  
  
  def get_string_attr_as_string(self, attr):
    # we know the attr is a string, so return string with double quotes around it
    return attr + " : \"" + self.yaml_file.get("library").get(attr) + "\";\n"

  # works for floats, bools, value_enums, anything else that doesn't use double quotes around the valuepossibly others
  def get_attr_as_string_basic(self, attr):
    return attr + " : " + str(self.yaml_file.get("library").get(attr)) + ";\n"
  
  # flow control function that gets the type from associated json file (including "level")
  def get_string_from_attr_type(self, attr, level_dict):
    # type of attr in level will be a list of strings or booleans holding the potential types/values this attribute can have

    # if the value at a given key is a list, that means the attribute can be one of several values (but NOT types)
    if isinstance(level_dict.get(attr), list):
      # for these, we can just return the attr value without quotes on either side
      return self.get_attr_as_string_basic(attr)
    # if the value at a given key is a dict, that means the attribute has at least one possible type (but possibly more, e.g. name and name_list)
    elif isinstance(level_dict.get(attr), dict):
      # get list of types
      type_of_attr_in_level = level_dict.get(attr).get("type")
      # if no quotes or anything are required to be added, just return the value with the attribute name is the specified format
      if ("float" in type_of_attr_in_level or "trip_point_value" in type_of_attr_in_level or type_of_attr_in_level == [True, False] or "valueenum" in type_of_attr_in_level):
        return self.get_attr_as_string_basic(attr)
        
      # TODO - edit this later, for now everything that's not a float (or float-like) on lib-level will be string
      else:
        return self.get_string_attr_as_string(attr)
        
    # this case should never be called unless there's an error in the YAML - if so, just don't add anything to the string outside,
    # so return empty string here
    else:
      return ""

  def get_lib_level_attributes_as_string(self):
    # this could be improved a bit by not having to check directly for which "complexity level" an attribute belongs to,
    # but it should work well for now
    full_string = ""
    library_level_yaml = self.yaml_file.get("library")
    lib_level_simple_attributes_dict = self.attributes_provider.get_library_level_simple_attributes()
    lib_level_default_attributes_dict = self.attributes_provider.get_library_level_default_attributes()
    lib_level_scaling_attributes_dict = self.attributes_provider.get_library_level_scaling_attributes()
    for attr in library_level_yaml:
      # if attr is a simple attr in lib level
      if attr in lib_level_simple_attributes_dict:
        full_string += self.get_string_from_attr_type(attr, lib_level_simple_attributes_dict)
      # if attr is a default attr in lib level
      elif attr in lib_level_default_attributes_dict: 
        full_string += self.get_string_from_attr_type(attr, lib_level_default_attributes_dict)
      # if attr is a scaling attr in lib level
      elif attr in lib_level_scaling_attributes_dict:
        full_string += self.get_string_from_attr_type(attr, lib_level_scaling_attributes_dict)
        
    return full_string
  
  def get_full_library(self):
    full_lib = ""
    full_lib += "library(" + self.yaml_file.get("library").get("name") + ") {"
    # add the rest of the stuff here (in a while, crocodile)
    full_lib += "\n"
    return full_lib
    
    