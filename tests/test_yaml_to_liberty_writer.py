import pytest
from pathlib import Path
from src.yaml_to_liberty_writer import YamlToLibertyWriter

YAML_WITH_SIMPLE_LIB_LEVEL_ATTRIBUTES_PATH = Path("tests/test_input_files/valid_lib_level_attributes.yaml").absolute()
gscl45nm_yaml_path = Path("tests/test_input_files/gscl45nm.yaml").absolute()

gscl45nm_lib_level_string_without_complex_and_group = '''delay_model : table_lookup;
in_place_swap_mode : match_footprint;
time_unit : 1ns;
voltage_unit : 1V;
current_unit : 1uA;
pulling_resistance_unit : 1kohm;
leakage_power_unit : 1nW;
slew_upper_threshold_pct_rise : 80;
slew_lower_threshold_pct_rise : 20;
slew_upper_threshold_pct_fall : 80;
slew_lower_threshold_pct_fall : 20;
input_threshold_pct_rise : 50;
input_threshold_pct_fall : 50;
output_threshold_pct_rise : 50;
output_threshold_pct_fall : 50;
nom_process : 1;
nom_voltage : 1.1;
nom_temperature : 27;
default_operating_conditions : "typical";
'''


@pytest.fixture
def yaml_with_simple_lib_level_attributes():
  with open(YAML_WITH_SIMPLE_LIB_LEVEL_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def yaml_to_liberty_writer_simple_lib_level_attributes(yaml_with_simple_lib_level_attributes, attributes_provider):
  return YamlToLibertyWriter(yaml_with_simple_lib_level_attributes, attributes_provider)

@pytest.fixture
def yaml_to_liberty_writer_gscl45nm(gscl45nm_yaml_file, attributes_provider):
  return YamlToLibertyWriter(gscl45nm_yaml_file, attributes_provider)

def test_get_lib_level_attributes_as_string(yaml_to_liberty_writer_simple_lib_level_attributes, yaml_to_liberty_writer_gscl45nm):
  assert yaml_to_liberty_writer_simple_lib_level_attributes.get_lib_level_attributes_as_string() == "time_unit : 1ns;\nslew_upper_threshold_pct_rise : 80;\n"
  string_thing = yaml_to_liberty_writer_gscl45nm.get_lib_level_attributes_as_string()
  print(f"String thing: {string_thing}")
  assert yaml_to_liberty_writer_gscl45nm.get_lib_level_attributes_as_string() == gscl45nm_lib_level_string_without_complex_and_group

def test_get_cell_simple_attributes_as_string(yaml_to_liberty_writer_gscl45nm):
  first_cell = yaml_to_liberty_writer_gscl45nm.yaml_file.get("library").get("cells")[0]
  print(f"First cell: {first_cell}")
  assert yaml_to_liberty_writer_gscl45nm.get_cell_simple_attributes_as_string(first_cell) == "cell_footprint : \"buf\";\narea : 2.3465;\ncell_leakage_power : 19.7536;\n"

def test_get_pin_simple_attributes_as_string(yaml_to_liberty_writer_gscl45nm):
  first_pin = yaml_to_liberty_writer_gscl45nm.yaml_file.get("library").get("cells")[0].get("pins")[0]
  print(f"First pin: {first_pin}")
  assert yaml_to_liberty_writer_gscl45nm.get_pin_simple_attributes_as_string(first_pin) == "direction : input;\ncapacitance : 0.00153896;\nrise_capacitance : 0.00153896;\nfall_capacitance : 0.00150415;\n"