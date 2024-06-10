import src.constants_yaml_to_liberty_writer
import yaml

# MOST IMPORTANTLY - don't obssess about making the code perfect on the first try, let's just get it working first! I can always go back and change stuff later to make it prettier :)

# hmmm I don't know what to do about structure, on one hand classes would get
# super annoying, but on the other hand, all of these functions being in this class might get crowded

# POTENTIAL SOLUTION: instead of class, what if each is a module and just provides related functionality?
# classes aren't very useful here since they will be singleton instances
# (it also probably would not be very difficult to alter the code to work with modules instead)


class YamlToLibertyWriter:

  def __init__(self, yaml_file_read_stream, attributes_provider):
    self.yaml_file = yaml.safe_load(yaml_file_read_stream)
    self.attributes_provider = attributes_provider

  def remove_blank_lines(self, s):
    return "\n".join(line for line in s.splitlines() if line.strip())

  # current idea: for non-complex and non-group attributes, go by type(s) (unless something special)
  # for complex and group, create a function for each and look at the types of the inputs and process them through the "get___as_string" functions to create one "big" string for each of those attributes

  # using dict_containing_attr allows us to make the two below methods generic (meaning it can be used on library level, but also within cell and pin groups)
  def get_string_attr_as_string(self, attr, dict_containing_attr):
    # return string with double quotes around the value
    return attr + " : \"" + str(dict_containing_attr.get(attr)) + "\";\n"

  # works for floats, bools, value_enums, anything else that doesn't use double quotes around the valuepossibly others
  def get_attr_as_string_basic(self, attr, dict_containing_attr):
    return attr + " : " + str(dict_containing_attr.get(attr)) + ";\n"

  # flow control function that gets the type from associated json file (including "level")
  def get_string_from_attr_type(self, attr, level_dict, dict_containing_attr):
    # type of attr in level will be a list of strings or booleans holding the potential types/values this attribute can have

    # UPDATE: for now, every value can be a string, so we can just return the string with double quotes
    return self.get_string_attr_as_string(attr, dict_containing_attr)
    '''
      # if the value at a given key is a list, that means the attribute can be one of several values (but NOT types)
      if isinstance(level_dict.get(attr), list):
        # for these, we can just return the attr value without quotes on either side
        return self.get_attr_as_string_basic(attr, dict_containing_attr)
      # if the value at a given key is a dict, that means the attribute has at least one possible type (but possibly more, e.g. name and name_list)
      elif isinstance(level_dict.get(attr), dict):
        # get list of types
        type_of_attr_in_level = level_dict.get(attr).get("type")
        # if no quotes or anything are required to be added, just return the value with the attribute name is the specified format
        if ("float" in type_of_attr_in_level
            or "trip_point_value" in type_of_attr_in_level
            or type_of_attr_in_level == [True, False]
            or "valueenum" in type_of_attr_in_level):
          return self.get_attr_as_string_basic(attr, dict_containing_attr)
  
        # TODO - edit this later, for now everything that's not a float (or float-like) on lib-level will be string
        else:
          return self.get_string_attr_as_string(attr, dict_containing_attr)
  
      # this case should never be called unless there's an error in the YAML - if so, just don't add anything to the string outside,
      # so return empty string here
      else:
        return ""
    '''

  # TODO - add support for this once initial cell and pin stuff is done
  # bus definition
  def get_type_lib_level_as_string(self):
    pass

  def get_lib_level_attributes_as_string(self):
    # this could be improved a bit by not having to check directly for which "complexity level" an attribute belongs to,
    # but it should work well for now
    full_string = ""
    library_level_yaml = self.yaml_file.get("library")
    lib_level_simple_attributes_dict = self.attributes_provider.get_library_level_simple_attributes(
    )
    lib_level_default_attributes_dict = self.attributes_provider.get_library_level_default_attributes(
    )
    lib_level_scaling_attributes_dict = self.attributes_provider.get_library_level_scaling_attributes(
    )
    for attr in library_level_yaml:
      # if attr is a simple attr in lib level
      if attr in lib_level_simple_attributes_dict:
        full_string += self.get_string_from_attr_type(
            attr, lib_level_simple_attributes_dict, library_level_yaml)
      # if attr is a default attr in lib level
      elif attr in lib_level_default_attributes_dict:
        full_string += self.get_string_from_attr_type(
            attr, lib_level_default_attributes_dict, library_level_yaml)
      # if attr is a scaling attr in lib level
      elif attr in lib_level_scaling_attributes_dict:
        full_string += self.get_string_from_attr_type(
            attr, lib_level_scaling_attributes_dict, library_level_yaml)

    return full_string

  # NOTE - this is for a single cell, since that's how the actual .lib file is written
  # e.g. self.yaml_file.get("library").get("cells")[0], ..., self.yaml_file.get("library").get("cells")[i], ...
  # would be the input cell_dict
  def get_cell_simple_attributes_as_string(self, cell_dict):
    full_string = ""
    cell_group_simple_attributes_dict = self.attributes_provider.get_cell_group_simple_attributes(
    )
    # go through all the attributes and process the simple ones
    for attr in cell_dict:
      print(f"current attr: {attr}")
      # this should always be the case
      if attr in cell_group_simple_attributes_dict:
        full_string += self.get_string_from_attr_type(
            attr, cell_group_simple_attributes_dict, cell_dict)

    return full_string

  # NOTE - this is for a single pin, since that's how the actual .lib file is written
  # e.g. self.yaml_file.get("library").get("cells")[0].get("pins")[0], ..., self.yaml_file.get("library").get("cells")[i].get("pins")[j], ...
  # would be the input pin_dict
  def get_pin_simple_attributes_as_string(self, pin_dict):
    full_string = ""
    pin_group_simple_attributes_dict = self.attributes_provider.get_pin_group_simple_attributes(
    )
    for attr in pin_dict:
      if attr in pin_group_simple_attributes_dict:
        full_string += self.get_string_from_attr_type(
            attr, pin_group_simple_attributes_dict, pin_dict)

    return full_string

  def get_statement_with_parens_string(self, statement, params_string):
    # convert params_string to str in case it's not already
    return statement + "(\"" + str(params_string) + "\");"

  # e.g. cell_rise(scalar) {}
  # TODO - fix spaces issue, need to adjust every line within inside_string before returning
  def get_function_notation_string(self, func_name, param_name, inside_string,
                                   num_spaces_for_indent):
    # split by line
    lines = inside_string.split("\n")
    # get actual spaces based on given input
    spaces = " " * num_spaces_for_indent
    # for every line in lines, add spaces to the beginning of the line
    # (also add two extra spaces to the beginning of the line to account for the indent required for the "function body")
    lines = [spaces + "  " + line for line in lines]
    # add spaces before func name, after the
    return spaces + func_name + "(" + param_name + ") {\n" + "\n".join(
        lines) + "\n" + spaces + "}\n"

  def is_delay_attr(self, attr):
    return attr == src.constants_yaml_to_liberty_writer.CELL_RISE or attr == src.constants_yaml_to_liberty_writer.CELL_FALL or attr == src.constants_yaml_to_liberty_writer.RISE_TRANSITION or attr == src.constants_yaml_to_liberty_writer.FALL_TRANSITION

  # TODO - must be modified later to add support for arrays/indices for cell rise/fall and rise/fall transition
  # TODO - need to also add support for the rest of the group attributes within timing group in pin group
  def get_timing_group_group_attribute_as_string(self, attr, timing_dict):
    if self.is_delay_attr(attr):
      return self.get_function_notation_string(
          attr,
          timing_dict.get(attr).get("cell_template"),
          self.get_statement_with_parens_string(
              "values",
              timing_dict.get(attr).get("values")),
          0)
    else:
      return ""

  # TODO - this is a very barebones function (no support for LUT), need to update later
  # works on individual timing, must do loop to go through all timing values
  def get_timing_in_pin_as_string(self, timing_dict):
    timing_string = ""
    timing_group_simple_attributes_dict = self.attributes_provider.get_timing_group_simple_attributes(
    )
    timing_group_group_attributes_dict = self.attributes_provider.get_timing_group_group_attributes(
    )
    for attr in timing_dict:
      if attr in timing_group_simple_attributes_dict:
        timing_string += self.get_string_from_attr_type(
            attr, timing_group_simple_attributes_dict, timing_dict)
      # if attr is a group attr in timing group
      elif attr in timing_group_group_attributes_dict:
        timing_string += self.get_timing_group_group_attribute_as_string(
            attr, timing_dict)

    return self.get_function_notation_string(
        "timing", "", timing_string,
        0)

  def get_pin_as_string(self, pin_dict):
    pin_string = ""
    pin_group_simple_attributes_dict = self.attributes_provider.get_pin_group_simple_attributes(
    )
    #pin_group_group_attributes_dict = self.attributes_provider.get_pin_group_group_attributes()
    for attr in pin_dict:
      if attr in pin_group_simple_attributes_dict:
        pin_string += self.get_string_from_attr_type(
            attr, pin_group_simple_attributes_dict, pin_dict)
      # if attr is a timing attr in pin group
      elif attr == src.constants_yaml_to_liberty_writer.TIMING:  #and self.is_delay_attr(attr):
        # add timing string to pin string
        for timing in pin_dict.get(attr):
          pin_string += self.get_timing_in_pin_as_string(timing)

    pin_string = self.remove_blank_lines(pin_string)

    pin_func_notation = self.get_function_notation_string(
        "pin", pin_dict.get("name"), pin_string,
        0)

    return pin_func_notation

  def get_all_pins_in_cell_as_string(self, cell_dict):
    full_string = ""
    for pin_dict in cell_dict.get("pins"):
      full_string += self.get_pin_as_string(pin_dict)

    return full_string

  def get_cell_as_string(self, cell_dict):
    cell_string = ""
    cell_group_simple_attributes_dict = self.attributes_provider.get_cell_group_simple_attributes(
    )
    for attr in cell_dict:
      if attr in cell_group_simple_attributes_dict:
        cell_string += self.get_string_from_attr_type(
            attr, cell_group_simple_attributes_dict, cell_dict)
      # if attr is a group attr in cell group
      elif attr == src.constants_yaml_to_liberty_writer.PIN:
        cell_string += self.get_all_pins_in_cell_as_string(cell_dict)
        

    cell_string = self.remove_blank_lines(cell_string)

    cell_func_notation = self.get_function_notation_string(
        "cell", cell_dict.get("name"), cell_string,
        0)

    return cell_func_notation
  
  def get_all_cells_in_library_as_string(self):
    full_string = ""
    

  def get_full_library_as_string(self):
    full_lib = ""
    full_lib += "library(" + self.yaml_file.get("library").get("name") + ") {"
    # add the rest of the stuff here (in a while, crocodile)
    full_lib += "\n"
    return full_lib
