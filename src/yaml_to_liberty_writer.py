import yaml

class YamlToLibertyWriter:
  def __init__(self, yaml_file_read_stream, attributes_provider):
    self.yaml_file = yaml.safe_load(yaml_file_read_stream)
    self.attributes_provider = attributes_provider
  
  def get_string_attr_as_string(self, attr):
    # we know the attr is a string, so return string with double quotes around it
    return attr + " : \"" + self.yaml_file.get("library").get(attr) + "\";\n"
  
  def get_float_attr_as_string(self, attr):
    return attr + " : " + str(self.yaml_file.get("library").get(attr)) + ";\n"

  # flow control function that gets the type from associated json file (including "level")
  def get_string_from_attr_type(self, attr, level_dict):
    type_of_attr_in_level = level_dict.get(attr).get("type")
    if (type_of_attr_in_level == "float"):
      return self.get_float_attr_as_string(attr)
    # TODO - edit this later, for now everything that's not a float will be string
    else:
      return self.get_string_attr_as_string(attr)
    

  def get_simple_library_level_attribute_as_string(self, attr):
    # if the attribute is in the set of simple, default, or scaling library-level attributes, get the string in the .lib format
    if attr in self.attributes_provider.get_library_level_simple_attributes():
      # TODO - pretty crude workaround, change this later so that we read from the json file containing
      # attribute names to type mappings and then use that to determine the type of the attribute
      # and thus whether to add quotes on either side when writing the value to the liberty file
      if isinstance(self.yaml_file.get("library").get(attr), str):
        # if type string, add quotes around value
        return attr + " : \"" + self.yaml_file.get("library").get(attr) + "\";\n"
      else:
        # otherwise, it's a number, so don't add quotes
        return attr + " : " + str(self.yaml_file.get("library").get(attr)) + ";\n"


  # TODO - is this function necessary? for now I'll keep it since it may come in handy with the default attributes
  # being able to have more sophisticated types than just strings and ints (as well as restrictions)
  def get_default_library_level_attribute_as_string(self, attr):
    if attr in self.attributes_provider.get_library_level_default_attributes():
      if isinstance(self.yaml_file.get("library").get(attr), str):
        # if type string, add quotes around value
       return attr + " : \"" + self.yaml_file.get("library").get(attr) + "\";\n"
      else:
        # otherwise, it's a number, so don't add quotes
        return attr + " : " + str(self.yaml_file.get("library").get(attr)) + ";\n"
        

  def get_scaling_library_level_attribute_as_string(self, attr):
    if attr
  
  def get_full_library(self):
    full_lib = ""
    full_lib += "library(" + self.yaml_file.get("library").get("name") + ") {"
    # add the rest of the stuff here (in a while, crocodile)
    full_lib += "\n"
    return full_lib
    
    