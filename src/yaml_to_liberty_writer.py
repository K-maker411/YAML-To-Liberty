import constants_yaml_to_liberty_writer
import yaml
from liberty.types import EscapedString, Group


# converts from given YAML to Liberty .lib file
class YamlToLibertyWriter:

  # NOTE - this assumes that if seed_lib_file is provided, then open(seed_lib_file_path) has already been done,
  # and that the result of open(seed_lib_path) is being passed in
  def __init__(self, seed_lib_file=None):
    self.seed_lib_file = seed_lib_file

  # removes only completely blank lines from given string
  def remove_blank_lines(self, s):
    return "\n".join(line for line in s.splitlines() if line.strip())

  # gets simple, default, scaling, and complex attrs from group as dict
  def get_simple_and_complex_attrs_from_seed_group_as_dict(self, group_: Group):
    dict_ = {}
    for attr in group_.attributes:
      # complex attribute
      if isinstance(attr.value, list):
        dict_.update({attr.name: {"level_type": "complex", "vals": attr.value}})
      # simple, default, or scaling
      elif isinstance(attr.value, str):
        # remove double quotes around values if they exist
        dict_.update({attr.name: attr.value.replace('"', "")})
      elif isinstance(attr.value, EscapedString):
        dict_.update({attr.name: str(attr.value).replace('"', "")})
      else:
        dict_.update({attr.name: attr.value})

    return dict_

  '''
  def get_non_nested_group_attr_from_seed_as_dict(self, group_: Group):
    dict_ = {}
    for g in group_.groups:
      # if there are NO nested groups
      if len(g.groups) == 0:
        # there are no other groups in this group, so just process as normal
        group_as_dict = {"level_type": "group", "vals": {constants_yaml_to_liberty_writer.PARAM_INDICATOR_CHAR: }}
        dict_.update(self.get_simple_and_complex_attrs_from_seed_group_as_dict(g))
  '''   
      
  
  # Currently unused, but may be useful in the future
  # works for floats, bools, value_enums, anything else that doesn't use double quotes around the value (possibly others)
  def get_attr_as_string_basic(self, attr, dict_containing_attr):
    return attr + " : " + str(dict_containing_attr.get(attr)) + ";\n"

  # converts simple attribute to .lib-formatted string (with double quotes around value)
  def get_simple_attr_as_string(self, attr, value):
    # convert value to string if it isn't already
    value = str(value)
    # if the value already has quotes around it (e.g. from the liberty parser), don't add extra
    if (value[0] == "\"" and value[-1] == "\""):
      return attr + " : " + value + ";\n"

    # otherwise, return string with double quotes around the value
    return attr + " : \"" + value + "\";\n"

  # converts complex attribute to .lib-formatted string
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
      # check if value (given vals) is 2D array
      # (possibly crude check)
      if isinstance(value[0], list):
        full_string += " \\" + "\n"
        # if so, process both layers
        for index_1 in range(0, len(value)):
          full_string += "\""
          for index_2 in range(0, len(value[index_1])):
            if index_2 == len(value[index_1]) - 1:
              full_string += str(value[index_1][index_2])
            else:
              full_string += str(value[index_1][index_2]) + ", "

          if index_1 == len(value) - 1:
            full_string += "\");"
          else:
            full_string += "\", \\" + "\n"

      # for now, every complex attribute (except the above) will have quotes (this might change)
      # if not 2d array, do 1d array processing
      else:
        full_string += "\""
        for index in range(0, len(value)):
          if index == len(value) - 1:
            full_string += str(value[index]) + "\");"
          else:
            full_string += str(value[index]) + ", "
    return full_string + "\n"

  # does simple string to .lib string conversion and indents
  def handle_simple_attribute(self, attr_name, attr_value, accum_str,
                              num_indents):
    indents = " " * num_indents
    # this assumes that \n was already done on accum_str
    new_string = accum_str + indents + self.get_simple_attr_as_string(
        attr_name, attr_value)
    return new_string

  # converts complex attribute to .lib format
  def handle_complex_attribute(self, attr_name, attr_value, accum_str,
                               num_indents):
    indents = " " * num_indents
    # attr_value is list of values
    # this assumes that \n was already done on accum_str
    complex_attr_as_string = self.get_complex_attr_as_string(
        attr_name, attr_value)
    # every complex_attr_as_string gets a \n at the very end, so if there are more than 2 lines (meaning
    # more than one newline), then we know to do the indents (on each line)
    if len(complex_attr_as_string.splitlines()) > 2:
      return accum_str + "\n".join(
          indents + line
          for line in complex_attr_as_string.splitlines()) + "\n"
    else:
      # otherwise, one line complex attr, so just add indents before it
      return accum_str + indents + self.get_complex_attr_as_string(
          attr_name, attr_value)

  # handles list processing
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

  # handles dict processing
  def handle_dict(self, attr_name, dict_, accum_str, num_indents):
    indents = " " * num_indents

    # add to accum_str
    key_starting_with_param_indicator = [
        key for key in dict_ if key.startswith(
            constants_yaml_to_liberty_writer.PARAM_INDICATOR_CHAR)
    ]

    # if there is a key that starts with PARAM_INDICATOR_CHAR (currently $), then we need to put the value
    # associated with that key in the parens for that group (e.g. "gscl45nm" in library(gscl45nm))
    if len(key_starting_with_param_indicator) > 0:
      accum_str += indents + attr_name + "("
      for key in key_starting_with_param_indicator:
        # if there is a list of values associated with the key, then we need to handle that
        if isinstance(dict_[key], list):
          accum_str += "\""
          for index in range(0, len(dict_[key])):
            accum_str += str(dict_[key][index])
          accum_str += "\""
        else:
          accum_str += dict_.get(key) 
        accum_str += ", "
        
      # remove the extra ", " at the end
      accum_str = accum_str.removesuffix(", ")
      accum_str += ") {\n"
    # otherwise, just add the parens to indicate group (e.g. timing())
    else:
      accum_str += indents + attr_name + "() {\n"

    # key is attribute name, value is attribute value
    for key, value in dict_.items():
      # if value is a dict, then it is either group or complex attribute
      if isinstance(value, dict):
        if constants_yaml_to_liberty_writer.LEVEL_TYPE_STR in value and constants_yaml_to_liberty_writer.VALS_STR in value:
          # check if this is a group attribute
          if value.get(constants_yaml_to_liberty_writer.LEVEL_TYPE_STR
                       ) == constants_yaml_to_liberty_writer.GROUP_STR:
            vals = value.get(constants_yaml_to_liberty_writer.VALS_STR)
            # if vals is a list, call handle_list
            if isinstance(vals, list):
              # TODO - check if num_indents + 2 is necessary
              accum_str = self.handle_list(key, vals, accum_str,
                                           num_indents + 2)
            else:
              # if so, recursively call this function on the group attribute (using the vals of this group as the dict_)
              #print("recursively calling handle dict, key: " + key + ", value: " + str(value))
              accum_str = self.handle_dict(key, vals, accum_str,
                                           num_indents + 2)

          # otherwise, check if this is a complex attribute
          elif value.get(constants_yaml_to_liberty_writer.LEVEL_TYPE_STR
                         ) == constants_yaml_to_liberty_writer.COMPLEX_STR:
            vals = value.get(constants_yaml_to_liberty_writer.VALS_STR)
            accum_str = self.handle_complex_attribute(key, vals, accum_str,
                                                      num_indents + 2)
      # must be simple attribute
      else:
        #print("handling simple attribute: " + key)
        if not key.startswith(
            constants_yaml_to_liberty_writer.PARAM_INDICATOR_CHAR):
          accum_str = self.handle_simple_attribute(key, value, accum_str,
                                                   num_indents + 2)

    return accum_str + indents + "}\n"

  # master function - converts dict (from YAML) to .lib-formatted string
  def get_group_as_string_recursive(self, attr_name, dict_):
    accum_str = ""
    final_string = ""
    # checks if dict has a level-type key and a vals key (this should always be true for the inputted dict_)
    if constants_yaml_to_liberty_writer.LEVEL_TYPE_STR in dict_ and constants_yaml_to_liberty_writer.VALS_STR in dict_:
      vals_dict_or_list = dict_.get(constants_yaml_to_liberty_writer.VALS_STR)

      # if vals is a list (e.g. timing.vals), process as list
      if isinstance(vals_dict_or_list, list):
        final_string = self.handle_list(attr_name, vals_dict_or_list,
                                        accum_str, 0)
      # if vals is a dict (e.g. cell_rise.vals), process as dict
      elif isinstance(vals_dict_or_list, dict):
        final_string = self.handle_dict(attr_name, vals_dict_or_list,
                                        accum_str, 0)

    return self.remove_blank_lines(final_string)



  def seed_at_lib_level(self):
    # How do I do this? "Easiest" might be to convert the liberty-parser values 
    # to the dict format I set up for the YAML, then do lib-parser-dict.update(yaml_as_dict_)
    # 1. Simple/default/scaling are easy enough - just {attr_name: value} from lib-parser
    # 2. Complex is likely also not that difficult, since I've updated my YAML to use arrays for the values
    # 3. Groups are more challenging
    pass
