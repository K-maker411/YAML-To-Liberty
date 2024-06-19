from liberty.types import EscapedString
from src import constants_yaml_to_liberty_writer
import yaml
from liberty.parser import parse_liberty
# MOST IMPORTANTLY - don't obssess about making the code perfect on the first try, let's just get it working first! I can always go back and change stuff later to make it prettier :)

# hmmm I don't know what to do about structure, on one hand classes would get
# super annoying, but on the other hand, all of these functions being in this class might get crowded

# POTENTIAL SOLUTION: instead of class, what if each is a module and just provides related functionality?
# classes aren't very useful here since they will be singleton instances
# (it also probably would not be very difficult to alter the code to work with modules instead)

# TODO - if order is important, we can sort each dictionary according to the functional order, but that seems to also be alphabetically within each section (e.g. alphabetically in lib-level simple, then alphabetically in lib-level default, etc.) - for now, let's not worry too much about that
'''
def handle_dict(self, key_name, dictionary, current_string, num_spaces_for_indent):
  # Handle dictionary here...
  for attr, value in dictionary.items():
      if isinstance(value, dict):
          current_string += self.handle_dict(attr, value, current_string, num_spaces_for_indent + 2)
      elif isinstance(value, list):
          current_string += self.handle_list(attr, value, current_string, num_spaces_for_indent + 2)
      else:
          current_string += self.handle_value(attr, value, current_string, num_spaces_for_indent + 2)
  return current_string

def handle_list(self, key_name, list_, current_string, num_spaces_for_indent):
  # Handle list here...
  for index in range(0, len(list_)):
      item = list_[index]
      if isinstance(item, dict):
          current_string += self.handle_dict(key_name, item, current_string, num_spaces_for_indent)
      elif isinstance(item, list):
          current_string += self.handle_list(key_name, item, current_string, num_spaces_for_indent)
      else:
          current_string += self.handle_value(key_name, item, current_string, num_spaces_for_indent)
  return current_string

def handle_value(self, key_name, value, current_string, num_spaces_for_indent):
  # Handle single value here...
  return current_string
'''

class YamlToLibertyWriter:

  # NOTE - this assumes that if seed_lib_file is provided, then open(seed_lib_file_path) has already been done,
  # and that the result of open(seed_lib_path) is being passed in
  def __init__(self,
               yaml_file_read_stream,
               attributes_provider,
               seed_lib_file=None):
    self.yaml_file = yaml.safe_load(yaml_file_read_stream)
    self.attributes_provider = attributes_provider
    self.seed_lib_file = seed_lib_file

  def remove_blank_lines(self, s):
    return "\n".join(line for line in s.splitlines() if line.strip())

  # current idea: for non-complex and non-group attributes, go by type(s) (unless something special)
  # for complex and group, create a function for each and look at the types of the inputs and process them through the "get___as_string" functions to create one "big" string for each of those attributes

  # using dict_containing_attr allows us to make the two below methods generic (meaning it can be used on library level, but also within cell and pin groups)
  def get_string_attr_as_string(self, attr, dict_containing_attr):

    value_as_str = str(dict_containing_attr.get(attr))

    # if the value already has quotes around it (e.g. from the liberty parser), don't add extra
    if (value_as_str[0] == "\"" and value_as_str[-1] == "\""):
      return attr + " : " + value_as_str + ";\n"
      
    # otherwise, return string with double quotes around the value
    return attr + " : \"" + value_as_str + "\";\n"

  # works for floats, bools, value_enums, anything else that doesn't use double quotes around the valuepossibly others
  def get_attr_as_string_basic(self, attr, dict_containing_attr):
    return attr + " : " + str(dict_containing_attr.get(attr)) + ";\n"

  # flow control function that gets the type from associated json file (including "level")
  def get_string_from_attr_type(self, attr, level_dict, dict_containing_attr):
    # type of attr in level will be a list of strings or booleans holding the potential types/values this attribute can have

    # UPDATE: for now, every value can be a string, so we can just return the string with double quotes
    return self.get_string_attr_as_string(attr, dict_containing_attr)



  # interesting idea that might work:
  # main func and helper func, helper func takes in string and dict
  # helper func goes through key-value pairs in dict and adds simple/default/scaling attributes to string, checks for complex attribute in aggregate json file containing every complex attribute name and adds it to string (need to figure out how to do that part)
  # if a group attribute is found, call the function recursively using the current string as the string param and this new group attribute as the dict param
  # go through it in the exact same way, and this should automatically take care of nested groups (e.g. inside library, there are cells, and inside a cell, there are pins, inside pins, there are timing groups, etc.)

  # idea for complex attributes - why not specify them in arrays in the json to act like tuples?


  def get_simple_attr_as_string(self, attr, value):
    # convert value to string if it isn't already
    value = str(value)
    # if the value already has quotes around it (e.g. from the liberty parser), don't add extra
    if (value[0] == "\"" and value[-1] == "\""):
      return attr + " : " + value + ";\n"

    # otherwise, return string with double quotes around the value
    return attr + " : \"" + value + "\";\n"
      
  # here, value is a list
  def get_complex_attr_as_string(self, attr, value):
    full_string = attr + "("

    # this one doesn't use quotes for whatever reason
    if attr == constants_yaml_to_liberty_writer.CAPACITIVE_LOAD_UNIT:
      for index in range(0, len(value)):
        if index == len(value) - 1:
          full_string += str(value[index]) + ");"
        else:
          full_string += str(value[index]) + ", "
      
    else:
      # for now, every complex attribute (except the above) will have quotes (this might change)
      full_string += "\""
      for index in range(0, len(value)):
        if index == len(value) - 1:
          full_string += str(value[index]) + "\");"
        else:
          full_string += str(value[index]) + ", "
          
    return full_string + "\n"

  # does simple string to lib string conversion and indents
  def handle_simple_attribute(self, attr_name, attr_value, accum_str, num_indents):
    indents = " " * num_indents
    # this assumes that \n was already done on accum_str
    new_string = accum_str + indents + self.get_simple_attr_as_string(attr_name, attr_value)
    return new_string

  # converts complex attribute to lib format
  def handle_complex_attribute(self, attr_name, attr_value, accum_str, num_indents):
    indents = " " * num_indents
    # attr_value is list of values
    # this assumes that \n was already done on accum_str
    new_string = accum_str + indents + self.get_complex_attr_as_string(attr_name, attr_value)
    return new_string
  
  def handle_list(self, attr_name, list_, accum_str, num_indents):
    for index in range(0, len(list_)):
      item = list_[index]
      # if the item in the list is a dict
      if isinstance(item, dict):
        # lists themselves don't exist in .lib the way they do in the YAML specification,
        # so we need to plug in the given attr_name into the handle_dict method because
        # we are on a list of dicts (e.g. cell in YAML has a list of cells, and when we get the first one in this function,
        # we are on a cell dict, thus we plug in attr_name, which was cell)
        accum_str = self.handle_dict(attr_name, item, accum_str, num_indents)

    return accum_str
        

  def handle_dict(self, attr_name, dict_, accum_str, num_indents):
    indents = " " * num_indents
    # add to accum_str
    key_starting_with_param_indicator = [key for key in dict_.keys() if key.startswith(constants_yaml_to_liberty_writer.PARAM_INDICATOR_CHAR)]
    if len(key_starting_with_param_indicator) > 0:
      accum_str += indents + attr_name + "(" + dict_.get(key_starting_with_param_indicator[0]) + ") {\n"
    else:
      accum_str += indents + attr_name + "() {\n"
    # key is attribute name, value is attribute value
    for key, value in dict_.items():
      #print("key: " + key)
      #print("value: " + str(value))
      #print("is value a dict: " + str(isinstance(value, dict)))
      if isinstance(value, dict):
        
        if constants_yaml_to_liberty_writer.LEVEL_TYPE_STR in value and constants_yaml_to_liberty_writer.VALS_STR in value:
          # check if this is a group attribute
          #print("is value a group attribute: " + str(value.get(constants_yaml_to_liberty_writer.LEVEL_TYPE_STR) == constants_yaml_to_liberty_writer.GROUP_STR))
          if value.get(constants_yaml_to_liberty_writer.LEVEL_TYPE_STR) == constants_yaml_to_liberty_writer.GROUP_STR:
            # add to accum_str
            # TODO - figure out how to put the stuff in parentheses later
            # TODO - is this even correct? all guesswork for now, we shall see
            #print("adding to accum_str (inside if isinstnace value dict in handle dict): " + indents + attr_name + "() {\n")
            #accum_str += indents + "  " + attr_name + "() {\n"
            vals = value.get(constants_yaml_to_liberty_writer.VALS_STR)
            # if vals is a list, call handle_list
            if isinstance(vals, list):
              # TODO - check if num_indents + 2 is necessary
              accum_str = self.handle_list(key, vals, accum_str, num_indents + 2)
            else:
              # if so, recursively call this function on the group attribute (using the vals of this group as the dict_)
              #print("recursively calling handle dict, key: " + key + ", value: " + str(value))
              accum_str = self.handle_dict(key, vals, accum_str, num_indents + 2)
            
          # otherwise, check if this is a complex attribute
          elif value.get(constants_yaml_to_liberty_writer.LEVEL_TYPE_STR) == constants_yaml_to_liberty_writer.COMPLEX_STR:
            vals = value.get(constants_yaml_to_liberty_writer.VALS_STR)
            accum_str = self.handle_complex_attribute(key, vals, accum_str, num_indents + 2)
      # must be simple attribute
      else:
        #print("handling simple attribute: " + key)
        if not key.startswith(constants_yaml_to_liberty_writer.PARAM_INDICATOR_CHAR):
          accum_str = self.handle_simple_attribute(key, value, accum_str, num_indents + 2)
        
    return accum_str + indents + "}\n"


  
  def get_group_as_string_recursive(self, attr_name, dict_):
    accum_str = ""
    final_string = ""
    # this should always be true
    if constants_yaml_to_liberty_writer.LEVEL_TYPE_STR in dict_ and constants_yaml_to_liberty_writer.VALS_STR in dict_:
      vals_dict_or_list = dict_.get(constants_yaml_to_liberty_writer.VALS_STR)
      #print("vals dict or list: ", str(vals_dict_or_list))
      # if vals is a list (e.g. timing.vals), process as list
      if isinstance(vals_dict_or_list, list):
        final_string = self.handle_list(attr_name, vals_dict_or_list, accum_str, 0)
      # if vals is a dict (e.g. cell_rise.vals), process as dict
      elif isinstance(vals_dict_or_list, dict):
        #print("entering handle dict")
        final_string = self.handle_dict(attr_name, vals_dict_or_list, accum_str, 0)

    return self.remove_blank_lines(final_string)
  
    
  
  # TODO - add support for this once initial cell and pin stuff is done
  # bus definition
  def get_type_lib_level_as_string(self):
    pass

  def get_lib_level_attributes_dict_from_seed_lib_file(self):
    # if there is no seed lib file, exit function and don't do anything (might need to change this to return something other than empty dict, but we'll see)
    if self.seed_lib_file is None:
      return {}

    # NOTE - this only works for simple, default, and scaling attributes right now - need to figure out how to handle seeding with complex and group attributes
    seed_library = parse_liberty(self.seed_lib_file.read())
    self.seed_lib_file.seek(0)
    lib_level_attrs_dict = {}
    # for every (non-complex, non-group) attribute in the seed library, add it to the lib_level_attrs_dict
    for attr in seed_library.attributes:
      # EscapedString is a type used by liberty parser for things like voltage_unit, etc.
      if isinstance(attr.value, (str, float, int, EscapedString)):
        lib_level_attrs_dict.update({attr.name: attr.value})
    # TODO - add separate loop here for seed_library.groups (if that's even possible)
    # IDEA (to be implemented soon?): loop through all complex and group attributes in the seed library, but if they are complex/group, the dict entry will be {"name": null} - this way, we can check if the complex/group attribute has been defined in the YAML, and if not, we can use the value associated with this one as the default value for the complex/group attribute in the new .lib file (seeding complete)

    # HOWEVER, how would I deal with this when there are multiple group attributes with the same name (namely power_lut_template)?
    return lib_level_attrs_dict

  def get_lib_level_attribute_as_string(self, attr, library_level_yaml,
                                        lib_level_simple_attributes_dict,
                                        lib_level_default_attributes_dict,
                                        lib_level_scaling_attributes_dict):
    # if attr is a simple attr in lib level
    if attr in lib_level_simple_attributes_dict:
      return self.get_string_from_attr_type(attr,
                                            lib_level_simple_attributes_dict,
                                            library_level_yaml)
    # if attr is a default attr in lib level
    elif attr in lib_level_default_attributes_dict:
      return self.get_string_from_attr_type(attr,
                                            lib_level_default_attributes_dict,
                                            library_level_yaml)
    # if attr is a scaling attr in lib level
    elif attr in lib_level_scaling_attributes_dict:
      return self.get_string_from_attr_type(attr,
                                            lib_level_scaling_attributes_dict,
                                            library_level_yaml)
    # TODO - currently, when the .lib is used to seed one of these group/complex attributes,
    # it doesn't actually use that value because the liberty-parser uses different formatting
    # for the attributes than this program does - eventually, we need to convert each of the 
    # group/complex attributes from the seed .lib in the liberty-parser-extracted format to the same format as I'm using for any of this to work
    elif attr == constants_yaml_to_liberty_writer.CAPACITIVE_LOAD_UNIT:
      return self.get_capacitive_load_unit_as_string() + "\n"
    elif attr == constants_yaml_to_liberty_writer.OPERATING_CONDITIONS:
      return self.get_operating_conditions_as_string(
          self.yaml_file.get("library").get("operating_conditions")) + "\n"
    else:
      return ""

  # returns the combined dictionary of seed and yaml values
  # if the seed value is provided for a key, then if the yaml value does not exist, {attribute_name: value_from_seed_lib} will be added to dict - otherwise, {attribute_name: value_from_yaml} will be added
  def get_lib_level_attributes_combined_dict(self):
    library_level_dict = self.yaml_file.get("library")
    lib_level_simple_attributes_dict = self.attributes_provider.get_attributes(
      constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_STR)
    lib_level_default_attributes_dict = self.attributes_provider.get_attributes(
      constants_yaml_to_liberty_writer.LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_STR)
    lib_level_scaling_attributes_dict = self.attributes_provider.get_attributes(
      constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SCALING_ATTRIBUTES_STR)

    # unpack all three dicts into new one
    combined_attributes_dict = {**lib_level_simple_attributes_dict, **lib_level_default_attributes_dict, **lib_level_scaling_attributes_dict}

    
    # for every attribute in the seed library, add it to a new dict 
     
    
    
  
  def get_lib_level_attributes_as_string(self):
    # this could be improved a bit by not having to check directly for which "complexity level" an attribute belongs to,
    # but it should work well for now
    full_string = ""
    library_level_yaml = self.yaml_file.get("library")
    lib_level_simple_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_STR)
    lib_level_default_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_STR)
    lib_level_scaling_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SCALING_ATTRIBUTES_STR)
    # NEW - adding seed file support
    # NOTE - recent python versions make dicts preserve insertion order by default, so we can loop as-is
    seed_lib_file_dict = self.get_lib_level_attributes_dict_from_seed_lib_file(
    )

    # set of attrs that have already been added to the full string
    added_attrs = set()
    
    for attr in seed_lib_file_dict:
      # if the attribute has NOT been defined in the yaml file, we use the value in the seed .lib file
      # (seeding behavior)
      if attr not in library_level_yaml:
        print(f"{attr} not in yaml file, adding from seed file")
        full_string += self.get_lib_level_attribute_as_string(
            attr, seed_lib_file_dict, lib_level_simple_attributes_dict,
            lib_level_default_attributes_dict,
            lib_level_scaling_attributes_dict)
        added_attrs.add(attr)

      # if the attribute has been defined in the yaml, we use the value in the yaml file and add the attribute to the added_attrs set
      # this is done so that yaml order is preserved, but it also prevents the attribute from being added to the string twice
      else:
        print(f"{attr} in yaml file, adding from yaml file")
        full_string += self.get_lib_level_attribute_as_string(
            attr, library_level_yaml, lib_level_simple_attributes_dict,
            lib_level_default_attributes_dict,
            lib_level_scaling_attributes_dict)
        added_attrs.add(attr)

      # otherwise, the attribute HAS been defined in the yaml file, so we use the value in the yaml file instead (override behavior)

    for attr in library_level_yaml:
      if attr not in added_attrs:
        print(f"{attr} in yaml file, adding from yaml file (2nd pass)" )
        full_string += self.get_lib_level_attribute_as_string(
            attr, library_level_yaml, lib_level_simple_attributes_dict,
            lib_level_default_attributes_dict, lib_level_scaling_attributes_dict)
  
    return full_string

  # NOTE - this is for a single cell, since that's how the actual .lib file is written
  # e.g. self.yaml_file.get("library").get("cells")[0], ..., self.yaml_file.get("library").get("cells")[i], ...
  # would be the input cell_dict
  def get_cell_simple_attributes_as_string(self, cell_dict):
    full_string = ""
    cell_group_simple_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.CELL_GROUP_SIMPLE_ATTRIBUTES_STR)
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
    pin_group_simple_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.PIN_GROUP_SIMPLE_ATTRIBUTES_STR)
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
              "\"" + str(timing_dict.get(attr).get("values")) + "\""), 0)
    else:
      return ""

  # TODO - this is a very barebones function (no support for LUT), need to update later
  # works on individual timing, must do loop to go through all timing values
  def get_timing_in_pin_as_string(self, timing_dict):
    timing_string = ""
    timing_group_simple_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.TIMING_GROUP_SIMPLE_ATTRIBUTES_STR)
    timing_group_group_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.TIMING_GROUP_GROUP_ATTRIBUTES_STR)
    for attr in timing_dict:
      if attr in timing_group_simple_attributes_dict:
        timing_string += self.get_string_from_attr_type(
            attr, timing_group_simple_attributes_dict, timing_dict)
      # if attr is a group attr in timing group
      elif attr in timing_group_group_attributes_dict:
        timing_string += self.get_timing_group_group_attribute_as_string(
            attr, timing_dict)

    return self.get_function_notation_string("timing", "", timing_string, 0)

  def get_pin_as_string(self, pin_dict):
    pin_string = ""
    pin_group_simple_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.PIN_GROUP_SIMPLE_ATTRIBUTES_STR)
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
        "pin", pin_dict.get("name"), pin_string, 0)

    return pin_func_notation

  def get_all_pins_in_cell_as_string(self, cell_dict):
    full_string = ""
    for pin_dict in cell_dict.get("pins"):
      full_string += self.get_pin_as_string(pin_dict)

    return full_string

  def get_cell_as_string(self, cell_dict):
    cell_string = ""
    cell_group_simple_attributes_dict = self.attributes_provider.get_attributes(
        constants_yaml_to_liberty_writer.CELL_GROUP_SIMPLE_ATTRIBUTES_STR)
    for attr in cell_dict:
      if attr in cell_group_simple_attributes_dict:
        cell_string += self.get_string_from_attr_type(
            attr, cell_group_simple_attributes_dict, cell_dict)
      # if attr is a group attr in cell group
      elif attr == constants_yaml_to_liberty_writer.PIN:
        cell_string += self.get_all_pins_in_cell_as_string(cell_dict)

    cell_string = self.remove_blank_lines(cell_string)

    cell_func_notation = self.get_function_notation_string(
        "cell", cell_dict.get("name"), cell_string, 0)

    return cell_func_notation

  def get_all_cells_in_library_as_string(self):
    full_string = ""
    for cell_dict in self.yaml_file.get("library").get("cells"):
      full_string += self.get_cell_as_string(cell_dict)

    return full_string

  def get_capacitive_load_unit_as_string(self):
    inside_parens_string = "\"" + str(
        self.yaml_file.get("library").get("capacitive_load_unit").get(
            "value")) + "\",\"" + self.yaml_file.get("library").get(
                "capacitive_load_unit").get("unit") + "\""
    return self.get_statement_with_parens_string("capacitive_load_unit",
                                                 inside_parens_string)

  def get_operating_conditions_as_string(self, operating_conditions_dict):
    inner_string = ""
    for attr in operating_conditions_dict:
      if attr == constants_yaml_to_liberty_writer.POWER_RAIL:
        # TODO - add support for this attribute later (unnecessary for now)
        continue
      # otherwise, simple attribute, so just get as string like normal
      elif attr != constants_yaml_to_liberty_writer.NAME:
        inner_string += self.get_string_attr_as_string(
            attr, operating_conditions_dict)

    return self.remove_blank_lines(
        self.get_function_notation_string(
            "operating_conditions",
            self.yaml_file.get("library").get("operating_conditions").get(
                "name"), inner_string, 0))

  def get_full_library_as_string(self):
    full_lib = ""
    full_lib += self.get_lib_level_attributes_as_string()
    full_lib += self.get_all_cells_in_library_as_string()
    # TODO - add more groups here as necessary, doesn't matter for now

    return self.remove_blank_lines(
        self.get_function_notation_string(
            "library",
            self.yaml_file.get("library").get("name"), full_lib, 0))
