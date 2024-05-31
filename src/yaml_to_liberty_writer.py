import yaml

class YamlToLibertyWriter:
  def __init__(self, yaml_file_read_stream, attributes_provider):
    self.yaml_file = yaml.safe_load(yaml_file_read_stream)
    self.attributes_provider = attributes_provider
  
  
  def get_simple_library_level_attributes_as_string(self):
    simple_attrs_string = ""
    # for every attribute on the library level in the yaml
    for attr in self.yaml_file.get("library"):
      # if the attribute is in the set of simple library-level attributes, add it to the string in the given format
      if attr in self.attributes_provider.get_library_level_simple_attributes():
        # TODO - pretty crude workaround, change this later so that we read from the json file containing
        # attribute names to type mappings and then use that to determine the type of the attribute
        # and thus whether to add quotes on either side when writing the value to the liberty file
        if isinstance(self.yaml_file.get("library").get(attr), str):
          simple_attrs_string += attr + " : \"" + self.yaml_file.get("library").get(attr) + "\";\n"
        else:
          simple_attrs_string += attr + " : " + str(self.yaml_file.get("library").get(attr)) + ";\n"
          
    return simple_attrs_string

  def get_full_library(self):
    full_lib = ""
    full_lib += "library(" + self.yaml_file.get("library").get("name") + ") {"
    # add the rest of the stuff here (in a while, crocodile)
    full_lib += "\n"
    return full_lib
    
    