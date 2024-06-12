import argparse
from yaml_to_liberty_writer import YamlToLibertyWriter
from attributes_provider import AttributesProvider
from constants_yaml_to_liberty_writer import LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH, LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH, LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH, CELL_GROUP_SIMPLE_ATTRIBUTES_PATH, PIN_GROUP_SIMPLE_ATTRIBUTES_PATH, PIN_GROUP_GROUP_ATTRIBUTES_PATH, TIMING_GROUP_SIMPLE_ATTRIBUTES_PATH, TIMING_GROUP_GROUP_ATTRIBUTES_PATH

def main():  
  parser = argparse.ArgumentParser(
    prog='YAMLToLibertyWriter',
    description='Converts YAML information into Liberty format using existing Liberty file attributes.')
  parser.add_argument('input_file_path')
  parser.add_argument("output_file_path")
  args = parser.parse_args()

  try:
    with open(LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH, 'r') as f1, \
         open(LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH, 'r') as f2, \
         open(LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH, 'r') as f3, \
         open(CELL_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as f4, \
         open(PIN_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as f5, \
         open(PIN_GROUP_GROUP_ATTRIBUTES_PATH, 'r') as f6, \
         open(TIMING_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as f7, \
         open(TIMING_GROUP_GROUP_ATTRIBUTES_PATH, 'r') as f8, \
         open(args.input_file_path, 'r') as input, \
         open(args.output_file_path, 'w') as output:
      # open attributes provider files using with, provide them to attributes provider,
      # get filename from command line input, parse and write!
      attrs_provider = AttributesProvider(f1, f3, f2, f4, f5, f7, f8, f6)
      y2l = YamlToLibertyWriter(input, attrs_provider)
      library_str = y2l.get_full_library_as_string()
      output.write(library_str)
  
  except IOError as e:
    print("IOError: " + str(e))
  except Exception as e:
    print("Exception: " + str(e))
          
if __name__ == "__main__":
  main()
