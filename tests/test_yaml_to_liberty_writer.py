import pytest
from pathlib import Path
from src.yaml_to_liberty_writer import YamlToLibertyWriter

YAML_WITH_SIMPLE_LIB_LEVEL_ATTRIBUTES_PATH = Path("tests/test_input_files/valid_lib_level_attributes.yaml").absolute()



@pytest.fixture
def yaml_with_simple_lib_level_attributes():
  with open(YAML_WITH_SIMPLE_LIB_LEVEL_ATTRIBUTES_PATH, 'r') as file:
    yield file

@pytest.fixture
def yaml_to_liberty_writer(yaml_with_simple_lib_level_attributes, attributes_provider):
  return YamlToLibertyWriter(yaml_with_simple_lib_level_attributes, attributes_provider)

def test_get_lib_level_attributes_as_string(yaml_to_liberty_writer):
  string_thing = yaml_to_liberty_writer.get_lib_level_attributes_as_string()
  print(f"String thing: {string_thing}")
  
  assert yaml_to_liberty_writer.get_lib_level_attributes_as_string() == "time_unit : \"1ns\";\nslew_upper_threshold_pct_rise : 80;\n"
  
  
  