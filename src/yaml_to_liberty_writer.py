import constants_yaml_to_liberty_writer
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

  # TODO - add support for this once initial cell and pin stuff is done
  # bus definition
  def get_type_lib_level_as_string(self):
    pass

  def get_lib_level_attributes_as_string(self):
    # this could be improved a bit by not having to check directly for which "complexity level" an attribute belongs to,
    # but it should work well for now
    full_string = ""
    library_level_yaml = self.yaml_file.get("library")
    lib_level_simple_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_STR)
    lib_level_default_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_STR)
    lib_level_scaling_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SCALING_ATTRIBUTES_STR)
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
      elif attr == constants_yaml_to_liberty_writer.CAPACITIVE_LOAD_UNIT:
        full_string += self.get_capacitive_load_unit_as_string() + "\n"
      elif attr == constants_yaml_to_liberty_writer.OPERATING_CONDITIONS:
        full_string += self.get_operating_conditions_as_string(self.yaml_file.get("library").get("operating_conditions")) + "\n"

    return full_string

  # NOTE - this is for a single cell, since that's how the actual .lib file is written
  # e.g. self.yaml_file.get("library").get("cells")[0], ..., self.yaml_file.get("library").get("cells")[i], ...
  # would be the input cell_dict
  def get_cell_simple_attributes_as_string(self, cell_dict):
    full_string = ""
    cell_group_simple_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.CELL_GROUP_SIMPLE_ATTRIBUTES_STR)
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
    pin_group_simple_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.PIN_GROUP_SIMPLE_ATTRIBUTES_STR)
    for attr in pin_dict:
      if attr in pin_group_simple_attributes_dict:
        full_string += self.get_string_from_attr_type(
            attr, pin_group_simple_attributes_dict, pin_dict)

    return full_string

  def get_statement_with_parens_string(self, statement, params_string):
    # convert params_string to str in case it's not already
    return statement + "(" + str(params_string) + ");"

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
    return attr == constants_yaml_to_liberty_writer.CELL_RISE or attr == constants_yaml_to_liberty_writer.CELL_FALL or attr == constants_yaml_to_liberty_writer.RISE_TRANSITION or attr == constants_yaml_to_liberty_writer.FALL_TRANSITION

  # TODO - must be modified later to add support for arrays/indices for cell rise/fall and rise/fall transition
  # TODO - need to also add support for the rest of the group attributes within timing group in pin group
  def get_timing_group_group_attribute_as_string(self, attr, timing_dict):
    if self.is_delay_attr(attr):
      return self.get_function_notation_string(
          attr,
          timing_dict.get(attr).get("cell_template"),
          self.get_statement_with_parens_string(
              "values",
              "\"" + str(timing_dict.get(attr).get("values")) + "\""),
          0)
    else:
      return ""

  # TODO - this is a very barebones function (no support for LUT), need to update later
  # works on individual timing, must do loop to go through all timing values
  def get_timing_in_pin_as_string(self, timing_dict):
    timing_string = ""
    timing_group_simple_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.TIMING_GROUP_SIMPLE_ATTRIBUTES_STR)
    timing_group_group_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.TIMING_GROUP_GROUP_ATTRIBUTES_STR)
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
    pin_group_simple_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.PIN_GROUP_SIMPLE_ATTRIBUTES_STR)
    for attr in pin_dict:
      if attr in pin_group_simple_attributes_dict:
        pin_string += self.get_string_from_attr_type(
            attr, pin_group_simple_attributes_dict, pin_dict)
      # if attr is a timing attr in pin group
      elif attr == constants_yaml_to_liberty_writer.TIMING:
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
    cell_group_simple_attributes_dict = self.attributes_provider.get_attributes(constants_yaml_to_liberty_writer.CELL_GROUP_SIMPLE_ATTRIBUTES_STR)
    for attr in cell_dict:
      if attr in cell_group_simple_attributes_dict:
        cell_string += self.get_string_from_attr_type(
            attr, cell_group_simple_attributes_dict, cell_dict)
      # if attr is a group attr in cell group
      elif attr == constants_yaml_to_liberty_writer.PIN:
        cell_string += self.get_all_pins_in_cell_as_string(cell_dict)
        

    cell_string = self.remove_blank_lines(cell_string)

    cell_func_notation = self.get_function_notation_string(
        "cell", cell_dict.get("name"), cell_string,
        0)

    return cell_func_notation
  
  def get_all_cells_in_library_as_string(self):
    full_string = ""
    for cell_dict in self.yaml_file.get("library").get("cells"):
      full_string += self.get_cell_as_string(cell_dict)

    return full_string
    

  def get_capacitive_load_unit_as_string(self):
    inside_parens_string = "\"" + str(self.yaml_file.get("library").get("capacitive_load_unit").get("value")) + "\",\"" + self.yaml_file.get("library").get("capacitive_load_unit").get("unit") + "\""
    return self.get_statement_with_parens_string("capacitive_load_unit", inside_parens_string) 

  def get_operating_conditions_as_string(self, operating_conditions_dict):
    inner_string = ""
    for attr in operating_conditions_dict:
      if attr == constants_yaml_to_liberty_writer.POWER_RAIL:
        # TODO - add support for this attribute later (unnecessary for now)
        continue
      # otherwise, simple attribute, so just get as string like normal
      elif attr != constants_yaml_to_liberty_writer.NAME:
        inner_string += self.get_string_attr_as_string(attr, operating_conditions_dict)

    
    return self.remove_blank_lines(self.get_function_notation_string("operating_conditions", self.yaml_file.get("library").get("operating_conditions").get("name"), inner_string, 0))
  
  def get_full_library_as_string(self):
    full_lib = ""
    full_lib += self.get_lib_level_attributes_as_string()
    full_lib += self.get_all_cells_in_library_as_string()
    # TODO - add more groups here as necessary, doesn't matter for now
    
    return self.remove_blank_lines(self.get_function_notation_string("library", self.yaml_file.get("library").get("name"), full_lib, 0))
