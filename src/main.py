import argparse
from pathlib import Path
from yaml_to_liberty_writer import YamlToLibertyWriter
from attributes_provider import AttributesProvider
def main():  
  parser = argparse.ArgumentParser(
    prog='YAMLToLibertyWriter',
    description='Converts YAML information into Liberty format using existing Liberty file attributes.')
  
  # TODO - open attributes provider files using with, provide them to attributes provider,
  # get filename from command line input, parse and write!
  attrs_provider = AttributesProvider()
  # positional argument for filename
  parser.add_argument('filename')
  y2l = YamlToLibertyWriter()

if __name__ == "__main__":
  main()
