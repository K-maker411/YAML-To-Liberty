import argparse
from .yaml_to_liberty_writer import YamlToLibertyWriter
from .attributes_provider import AttributesProvider
from . import constants_yaml_to_liberty_writer

def main():  
  parser = argparse.ArgumentParser(
    prog='YAMLToLibertyWriter',
    description='Converts YAML information into Liberty format using existing Liberty file attributes.')
  parser.add_argument('input_file_path')
  parser.add_argument("output_file_path")
  args = parser.parse_args()

  try:
    with open(constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH, 'r') as f1, \
         open(constants_yaml_to_liberty_writer.LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH, 'r') as f2, \
         open(constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH, 'r') as f3, \
         open(constants_yaml_to_liberty_writer.CELL_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as f4, \
         open(constants_yaml_to_liberty_writer.PIN_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as f5, \
         open(constants_yaml_to_liberty_writer.PIN_GROUP_GROUP_ATTRIBUTES_PATH, 'r') as f6, \
         open(constants_yaml_to_liberty_writer.TIMING_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as f7, \
         open(constants_yaml_to_liberty_writer.TIMING_GROUP_GROUP_ATTRIBUTES_PATH, 'r') as f8, \
         open(args.input_file_path, 'r') as input, \
         open(args.output_file_path, 'w') as output:
           
      attributes_dict = {
         constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_STR: f1,       
         constants_yaml_to_liberty_writer.LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_STR: f2,
         constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SCALING_ATTRIBUTES_STR: f3,
         constants_yaml_to_liberty_writer.CELL_GROUP_SIMPLE_ATTRIBUTES_STR: f4,
         constants_yaml_to_liberty_writer.PIN_GROUP_SIMPLE_ATTRIBUTES_STR: f5,
         constants_yaml_to_liberty_writer.TIMING_GROUP_SIMPLE_ATTRIBUTES_STR: f7,
         constants_yaml_to_liberty_writer.TIMING_GROUP_GROUP_ATTRIBUTES_STR: f8,
         constants_yaml_to_liberty_writer.PIN_GROUP_GROUP_ATTRIBUTES_STR: f6
      }
      # open attributes provider files using with, provide them to attributes provider,
      # get filename from command line input, parse and write!
      attrs_provider = AttributesProvider(attributes_dict)
      y2l = YamlToLibertyWriter(input, attrs_provider)
      library_str = y2l.get_full_library_as_string()
      output.write(library_str)
  
  except IOError as e:
    print("IOError: " + str(e))
  except Exception as e:
    print("Exception: " + str(e))
          
if __name__ == "__main__":
  main()
