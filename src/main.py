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
  parser.add_argument("-sl", "--seed_lib_attributes", type=pathlib.Path)
  args = parser.parse_args()

  try:
    with open(args.input_file_path, 'r') as input, \
         open(args.output_file_path, 'w') as output:
           
      y2l = YamlToLibertyWriter()
      dict_ = yaml.safe_load(input).get("library")
      library_str = y2l.get_group_as_string_recursive("library", dict_)
      output.write(library_str)
      print("Writing successful!")
  
  except IOError as e:
    print("IOError: " + str(e))
  except Exception as e:
    print("Exception: " + str(e))
          
if __name__ == "__main__":
  main()
