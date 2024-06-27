#!/usr/bin/env python3

import argparse
import pathlib
from yaml_to_liberty_writer import YamlToLibertyWriter
#from src import constants_yaml_to_liberty_writer
from liberty.parser import parse_liberty
import yaml


def main():  
  parser = argparse.ArgumentParser(
    prog="YAMLToLibertyWriter",
    description="Converts YAML information into Liberty format using existing Liberty file attributes.")
  parser.add_argument("input_file_path", type=pathlib.Path)
  parser.add_argument("output_file_path", type=pathlib.Path)
  parser.add_argument("-sl", "--seed_lib_attributes_path", type=pathlib.Path)
  args = parser.parse_args()
    
  try:
    with open(args.input_file_path, 'r') as input, \
         open(args.output_file_path, 'w') as output:
           
      y2l = YamlToLibertyWriter()
      dict_ = yaml.safe_load(input).get("library")

      print("dict_ before seed stuff: \n" + str(dict_))
      if args.seed_lib_attributes_path:
        with open(args.seed_lib_attributes_path, 'r') as seed_lib_attributes_file:
          # this is the library as a group object
          seed_lib_attributes_parsed = parse_liberty(seed_lib_attributes_file.read())
          seed_lib_attributes_dict = y2l.get_non_nested_group_attr_from_seed_as_dict(seed_lib_attributes_parsed)
          print("seed lib attributes dict: \n" + str(seed_lib_attributes_dict))
          # we need to override the seed with the yaml (in case any overrides are necessary), and also
          # to add all the stuff from the 
          # limitation: if even one lu_table_template is specified in the yaml, it will override all of the lu_table_template in the seed (since the key itself is being replaced)
          #print("dict before update: \n" + str(dict_))
          seed_lib_attributes_dict.update(dict_["vals"])
          print("dict vals: \n" + str(dict_["vals"]))
          dict_["vals"].update(seed_lib_attributes_dict.copy()) 
          print("dict after update: \n" + str(dict_))
          #print("dict after update: \n" + str(dict_))
          

      print("dict just before get string: \n" + str(dict_))
      library_str = y2l.get_group_as_string_recursive("library", dict_)
      print("library_str: \n" + library_str)
      output.write(library_str)
      print("Writing successful!")
  
  except IOError as e:
    print("IOError: " + str(e))
  except Exception as e:
    print("Exception: " + str(e))
          
if __name__ == "__main__":
  main()
