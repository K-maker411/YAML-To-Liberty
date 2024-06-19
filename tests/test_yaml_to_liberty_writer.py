import pytest
from pathlib import Path
import difflib
from src.yaml_to_liberty_writer import YamlToLibertyWriter
from src import constants_yaml_to_liberty_writer

YAML_WITH_SIMPLE_LIB_LEVEL_ATTRIBUTES_PATH = Path(
    "tests/test_input_files/valid_lib_level_attributes.yaml").absolute()
gscl45nm_yaml_path = Path("tests/test_input_files/gscl45nm.yaml").absolute()

gscl45nm_lib_level_string_without_complex_and_group = '''delay_model : "table_lookup";
in_place_swap_mode : "match_footprint";
time_unit : "1ns";
voltage_unit : "1V";
current_unit : "1uA";
pulling_resistance_unit : "1kohm";
leakage_power_unit : "1nW";
slew_upper_threshold_pct_rise : "80";
slew_lower_threshold_pct_rise : "20";
slew_upper_threshold_pct_fall : "80";
slew_lower_threshold_pct_fall : "20";
input_threshold_pct_rise : "50";
input_threshold_pct_fall : "50";
output_threshold_pct_rise : "50";
output_threshold_pct_fall : "50";
nom_process : "1";
nom_voltage : "1.1";
nom_temperature : "27";
default_operating_conditions : "typical";
'''

gscl45nm_lib_level_attrs_string_with_complex_and_group = '''delay_model : "table_lookup";
in_place_swap_mode : "match_footprint";
time_unit : "1ns";
voltage_unit : "1V";
current_unit : "1uA";
pulling_resistance_unit : "1kohm";
leakage_power_unit : "1nW";
capacitive_load_unit("1","pf");
slew_upper_threshold_pct_rise : "80";
slew_lower_threshold_pct_rise : "20";
slew_upper_threshold_pct_fall : "80";
slew_lower_threshold_pct_fall : "20";
input_threshold_pct_rise : "50";
input_threshold_pct_fall : "50";
output_threshold_pct_rise : "50";
output_threshold_pct_fall : "50";
nom_process : "1";
nom_voltage : "1.1";
nom_temperature : "27";
operating_conditions(typical) {
  process : "1";
  voltage : "1.1";
  temperature : "27";
}
default_operating_conditions : "typical";
'''


@pytest.fixture
def yaml_with_simple_lib_level_attributes():
  with open(YAML_WITH_SIMPLE_LIB_LEVEL_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def yaml_to_liberty_writer_simple_lib_level_attributes(
    yaml_with_simple_lib_level_attributes, attributes_provider):
  return YamlToLibertyWriter(yaml_with_simple_lib_level_attributes,
                             attributes_provider)


@pytest.fixture
def yaml_to_liberty_writer_gscl45nm(gscl45nm_yaml_file, attributes_provider):
  return YamlToLibertyWriter(gscl45nm_yaml_file, attributes_provider)


@pytest.fixture
def yaml_to_liberty_writer_simple_gscl45nm(simple_gscl45nm_yaml_file,
                                           attributes_provider):
  return YamlToLibertyWriter(simple_gscl45nm_yaml_file, attributes_provider)


@pytest.fixture
def yaml_to_liberty_writer_simple_gscl45nm_with_seed_lib(
    seed_test_gscl45nm_yaml_file, seed_test_gscl45nm_lib_file,
    attributes_provider):
  return YamlToLibertyWriter(seed_test_gscl45nm_yaml_file, attributes_provider,
                             seed_test_gscl45nm_lib_file)

@pytest.fixture
def yaml_to_liberty_writer_simple_gscl45nm_take_2(
    simple_gscl45nm_take_2_yaml_file, attributes_provider):
  return YamlToLibertyWriter(simple_gscl45nm_take_2_yaml_file, attributes_provider)


def test_get_lib_level_attributes_as_string(
    yaml_to_liberty_writer_simple_lib_level_attributes,
    yaml_to_liberty_writer_gscl45nm,
    yaml_to_liberty_writer_simple_gscl45nm_with_seed_lib):
  assert yaml_to_liberty_writer_simple_lib_level_attributes.get_lib_level_attributes_as_string(
  ) == "time_unit : \"1ns\";\nslew_upper_threshold_pct_rise : \"80\";\n"
  
  #assert repr(
      #yaml_to_liberty_writer_gscl45nm.get_lib_level_attributes_as_string(
      #)) == repr(gscl45nm_lib_level_attrs_string_with_complex_and_group)

  # tests both seeding and override behavior
  # seeding tested through slew_thresholds not being in yaml and values from seed .lib being used
  # override behavior tested through nom_temperature being in yaml and its value is used (28) rather than the value provided in the seed .lib (27)
  expected_2 = """delay_model : "table_lookup";
in_place_swap_mode : "match_footprint";
time_unit : "1ns";
voltage_unit : "1V";
current_unit : "1uA";
pulling_resistance_unit : "1kohm";
leakage_power_unit : "1nW";
capacitive_load_unit("1","pf");
slew_upper_threshold_pct_rise : "80";
slew_lower_threshold_pct_rise : "20";
slew_upper_threshold_pct_fall : "80";
slew_lower_threshold_pct_fall : "20";
input_threshold_pct_rise : "50";
input_threshold_pct_fall : "50";
output_threshold_pct_rise : "50";
output_threshold_pct_fall : "50";
nom_process : "1";
nom_voltage : "1.1";
nom_temperature : "28";
operating_conditions(typical) {
  process : "1";
  voltage : "1.1";
  temperature : "27";
}
default_operating_conditions : "typical";
"""

  print("expected_2: \n" + expected_2)
  print("actual_2: \n" + yaml_to_liberty_writer_simple_gscl45nm_with_seed_lib.get_lib_level_attributes_as_string())
  assert repr(expected_2) == repr(yaml_to_liberty_writer_simple_gscl45nm_with_seed_lib.get_lib_level_attributes_as_string())


def test_get_cell_simple_attributes_as_string(yaml_to_liberty_writer_gscl45nm):
  first_cell = yaml_to_liberty_writer_gscl45nm.yaml_file.get("library").get(
      "cells")[0]
  print(f"First cell: {first_cell}")
  assert yaml_to_liberty_writer_gscl45nm.get_cell_simple_attributes_as_string(
      first_cell
  ) == "cell_footprint : \"buf\";\narea : \"2.3465\";\ncell_leakage_power : \"19.7536\";\n"


def test_get_pin_simple_attributes_as_string(yaml_to_liberty_writer_gscl45nm):
  first_pin = yaml_to_liberty_writer_gscl45nm.yaml_file.get("library").get(
      "cells")[0].get("pins")[0]
  assert yaml_to_liberty_writer_gscl45nm.get_pin_simple_attributes_as_string(
      first_pin
  ) == "direction : \"input\";\ncapacitance : \"0.00153896\";\nrise_capacitance : \"0.00153896\";\nfall_capacitance : \"0.00150415\";\n"


def test_get_function_notation_string(yaml_to_liberty_writer_gscl45nm):
  first_string = "        cell_rise(scalar) {\n          values(\"0.0\");\n        }\n"
  assert yaml_to_liberty_writer_gscl45nm.get_function_notation_string(
      "cell_rise", "scalar", "values(\"0.0\");",
      constants_yaml_to_liberty_writer.INSIDE_TIMING_GROUP_NUM_SPACES
  ) == first_string


def test_get_timing_group_group_attribute_as_string(
    yaml_to_liberty_writer_simple_gscl45nm):
  timing_dict = yaml_to_liberty_writer_simple_gscl45nm.yaml_file.get(
      "library").get("cells")[0].get("pins")[1].get("timings")[0]

  print("Timing dict:\n", timing_dict)

  first_string = """rise_transition(scalar) {
  values(\"0.0\");
}
"""
  print("First string:\n" + first_string)
  print("Func call output:\n" + yaml_to_liberty_writer_simple_gscl45nm.
        get_timing_group_group_attribute_as_string("rise_transition",
                                                   timing_dict))
  assert yaml_to_liberty_writer_simple_gscl45nm.get_timing_group_group_attribute_as_string(
      "rise_transition", timing_dict) == first_string


def test_get_pin_as_string(yaml_to_liberty_writer_simple_gscl45nm):
  pin_A_dict = yaml_to_liberty_writer_simple_gscl45nm.yaml_file.get(
      "library").get("cells")[0].get("pins")[0]

  pin_Y_dict = yaml_to_liberty_writer_simple_gscl45nm.yaml_file.get(
      "library").get("cells")[0].get("pins")[1]

  pin_A_string = """pin(A) {
  direction : "input";
  capacitance : "0.00153896";
  rise_capacitance : "0.00153896";
  fall_capacitance : "0.00150415";
}
"""

  pin_Y_string = """pin(Y) {
  direction : "output";
  capacitance : "0";
  rise_capacitance : "0";
  fall_capacitance : "0";
  max_capacitance : "0.518678";
  function : "A";
  timing() {
    related_pin : "A";
    timing_sense : "positive_unate";
    cell_rise(scalar) {
      values("0.0");
    }
    rise_transition(scalar) {
      values("0.0");
    }
    cell_fall(scalar) {
      values("0.0");
    }
    fall_transition(scalar) {
      values("0.0");
    }
  }
}
"""
  print("String: \n" + pin_Y_string)
  print("Func: \n" +
        yaml_to_liberty_writer_simple_gscl45nm.get_pin_as_string(pin_Y_dict))

  assert repr(
      yaml_to_liberty_writer_simple_gscl45nm.get_pin_as_string(
          pin_A_dict)) == repr(pin_A_string)

  assert repr(
      yaml_to_liberty_writer_simple_gscl45nm.get_pin_as_string(
          pin_Y_dict)) == repr(pin_Y_string)


def test_get_all_pins_in_cell_as_string(
    yaml_to_liberty_writer_simple_gscl45nm):
  first_cell_dict = yaml_to_liberty_writer_simple_gscl45nm.yaml_file.get(
      "library").get("cells")[0]

  pins_in_first_cell_string = """pin(A) {
  direction : "input";
  capacitance : "0.00153896";
  rise_capacitance : "0.00153896";
  fall_capacitance : "0.00150415";
}
pin(Y) {
  direction : "output";
  capacitance : "0";
  rise_capacitance : "0";
  fall_capacitance : "0";
  max_capacitance : "0.518678";
  function : "A";
  timing() {
    related_pin : "A";
    timing_sense : "positive_unate";
    cell_rise(scalar) {
      values("0.0");
    }
    rise_transition(scalar) {
      values("0.0");
    }
    cell_fall(scalar) {
      values("0.0");
    }
    fall_transition(scalar) {
      values("0.0");
    }
  }
}
"""

  print("String: \n" + pins_in_first_cell_string)
  print("Func: \n" +
        yaml_to_liberty_writer_simple_gscl45nm.get_all_pins_in_cell_as_string(
            first_cell_dict))
  assert repr(
      yaml_to_liberty_writer_simple_gscl45nm.get_all_pins_in_cell_as_string(
          first_cell_dict)) == repr(pins_in_first_cell_string)


def test_get_cell_as_string(yaml_to_liberty_writer_simple_gscl45nm):
  first_cell_dict = yaml_to_liberty_writer_simple_gscl45nm.yaml_file.get(
      "library").get("cells")[0]
  first_cell_string = """cell(BUFX2) {
  cell_footprint : "buf";
  area : "2.3465";
  cell_leakage_power : "19.7536";
  pin(A) {
    direction : "input";
    capacitance : "0.00153896";
    rise_capacitance : "0.00153896";
    fall_capacitance : "0.00150415";
  }
  pin(Y) {
    direction : "output";
    capacitance : "0";
    rise_capacitance : "0";
    fall_capacitance : "0";
    max_capacitance : "0.518678";
    function : "A";
    timing() {
      related_pin : "A";
      timing_sense : "positive_unate";
      cell_rise(scalar) {
        values("0.0");
      }
      rise_transition(scalar) {
        values("0.0");
      }
      cell_fall(scalar) {
        values("0.0");
      }
      fall_transition(scalar) {
        values("0.0");
      }
    }
  }
}
"""
  print("String: \n" + first_cell_string)
  print("Func: \n" + yaml_to_liberty_writer_simple_gscl45nm.get_cell_as_string(
      first_cell_dict))
  assert repr(
      yaml_to_liberty_writer_simple_gscl45nm.get_cell_as_string(
          first_cell_dict)) == repr(first_cell_string)


def test_get_all_cells_in_library_as_string(
    yaml_to_liberty_writer_simple_gscl45nm):
  all_cells_string = """cell(BUFX2) {
  cell_footprint : "buf";
  area : "2.3465";
  cell_leakage_power : "19.7536";
  pin(A) {
    direction : "input";
    capacitance : "0.00153896";
    rise_capacitance : "0.00153896";
    fall_capacitance : "0.00150415";
  }
  pin(Y) {
    direction : "output";
    capacitance : "0";
    rise_capacitance : "0";
    fall_capacitance : "0";
    max_capacitance : "0.518678";
    function : "A";
    timing() {
      related_pin : "A";
      timing_sense : "positive_unate";
      cell_rise(scalar) {
        values("0.0");
      }
      rise_transition(scalar) {
        values("0.0");
      }
      cell_fall(scalar) {
        values("0.0");
      }
      fall_transition(scalar) {
        values("0.0");
      }
    }
  }
}
cell(BUFX1) {
  cell_footprint : "buf";
}
"""
  assert repr(yaml_to_liberty_writer_simple_gscl45nm.
              get_all_cells_in_library_as_string()) == repr(all_cells_string)


def test_get_capacitive_load_unit_as_string(
    yaml_to_liberty_writer_simple_gscl45nm):
  expected_str = """capacitive_load_unit("1","pf");"""
  assert repr(yaml_to_liberty_writer_simple_gscl45nm.
              get_capacitive_load_unit_as_string()) == repr(expected_str)


def test_get_operating_conditions_as_string(
    yaml_to_liberty_writer_simple_gscl45nm):
  operating_conditons_dict = yaml_to_liberty_writer_simple_gscl45nm.yaml_file.get(
      "library").get("operating_conditions")
  expected_str = """operating_conditions(typical) {
  process : "1";
  voltage : "1.1";
  temperature : "27";
}"""

  print("expected: \n" + expected_str)
  print("actual: \n" + yaml_to_liberty_writer_simple_gscl45nm.
        get_operating_conditions_as_string(operating_conditons_dict))
  assert repr(
      yaml_to_liberty_writer_simple_gscl45nm.
      get_operating_conditions_as_string(operating_conditons_dict)) == repr(
          expected_str)


def test_get_full_library_as_string(yaml_to_liberty_writer_simple_gscl45nm):
  expected_str = """library(gsc145nm) {
  delay_model : "table_lookup";
  in_place_swap_mode : "match_footprint";
  time_unit : "1ns";
  voltage_unit : "1V";
  current_unit : "1uA";
  pulling_resistance_unit : "1kohm";
  leakage_power_unit : "1nW";
  capacitive_load_unit("1","pf");
  slew_upper_threshold_pct_rise : "80";
  slew_lower_threshold_pct_rise : "20";
  slew_upper_threshold_pct_fall : "80";
  slew_lower_threshold_pct_fall : "20";
  input_threshold_pct_rise : "50";
  input_threshold_pct_fall : "50";
  output_threshold_pct_rise : "50";
  output_threshold_pct_fall : "50";
  nom_process : "1";
  nom_voltage : "1.1";
  nom_temperature : "27";
  operating_conditions(typical) {
    process : "1";
    voltage : "1.1";
    temperature : "27";
  }
  default_operating_conditions : "typical";
  cell(BUFX2) {
    cell_footprint : "buf";
    area : "2.3465";
    cell_leakage_power : "19.7536";
    pin(A) {
      direction : "input";
      capacitance : "0.00153896";
      rise_capacitance : "0.00153896";
      fall_capacitance : "0.00150415";
    }
    pin(Y) {
      direction : "output";
      capacitance : "0";
      rise_capacitance : "0";
      fall_capacitance : "0";
      max_capacitance : "0.518678";
      function : "A";
      timing() {
        related_pin : "A";
        timing_sense : "positive_unate";
        cell_rise(scalar) {
          values("0.0");
        }
        rise_transition(scalar) {
          values("0.0");
        }
        cell_fall(scalar) {
          values("0.0");
        }
        fall_transition(scalar) {
          values("0.0");
        }
      }
    }
  }
  cell(BUFX1) {
    cell_footprint : "buf";
  }
}"""
  print("Expected: \n" + expected_str)
  print("\nActual: \n" +
        yaml_to_liberty_writer_simple_gscl45nm.get_full_library_as_string())

  assert repr(expected_str) == repr(
      yaml_to_liberty_writer_simple_gscl45nm.get_full_library_as_string())


def test_get_lib_level_attributes_dict_from_seed_lib_file(
    yaml_to_liberty_writer_simple_gscl45nm_with_seed_lib):
  expected = {
      "delay_model": "table_lookup",
      "in_place_swap_mode": "match_footprint",
      "time_unit": "1ns",
      "voltage_unit": "1V",
      "current_unit": "1uA",
      "pulling_resistance_unit": "1kohm",
      "leakage_power_unit": "1nW",
      "slew_upper_threshold_pct_rise": 80,
      "slew_lower_threshold_pct_rise": 20,
      "slew_upper_threshold_pct_fall": 80,
      "slew_lower_threshold_pct_fall": 20,
      "input_threshold_pct_rise": 50,
      "output_threshold_pct_rise": 50,
      "nom_process": 1,
      "nom_voltage": 1.1,
      "nom_temperature": 27,
      "default_operating_conditions": "typical"
  }
  lib_level_attributes_dict = yaml_to_liberty_writer_simple_gscl45nm_with_seed_lib.get_lib_level_attributes_dict_from_seed_lib_file(
  )

  print("lib level attrs dict: \n" + str(lib_level_attributes_dict))

  assert expected == lib_level_attributes_dict


def test_get_complex_attr_as_string(yaml_to_liberty_writer_simple_gscl45nm_take_2):
  cap_load_unit_attr_dict = yaml_to_liberty_writer_simple_gscl45nm_take_2.yaml_file.get(
      "library").get(constants_yaml_to_liberty_writer.CAPACITIVE_LOAD_UNIT)

  index_1_dict = yaml_to_liberty_writer_simple_gscl45nm_take_2.yaml_file.get(
    "library").get("cell")[0].get("pin")[1].get("internal_power")[0].get("rise_power").get("index_1")
  
  expected_str_1 = "capacitive_load_unit(1, pf);"
  expected_str_2 = "index_1(\"0.1, 0.5, 1.2, 3, 4, 5\");"

  print("expected: \n" + expected_str_1)
  print("actual: \n" + (yaml_to_liberty_writer_simple_gscl45nm_take_2.get_complex_attr_as_string(constants_yaml_to_liberty_writer.CAPACITIVE_LOAD_UNIT, cap_load_unit_attr_dict)))
  assert repr(yaml_to_liberty_writer_simple_gscl45nm_take_2.get_complex_attr_as_string(constants_yaml_to_liberty_writer.CAPACITIVE_LOAD_UNIT, cap_load_unit_attr_dict)) == repr(expected_str_1)

  assert repr(yaml_to_liberty_writer_simple_gscl45nm_take_2.get_complex_attr_as_string("index_1", index_1_dict)) == repr(expected_str_2)

def test_get_dict_as_string_recursive(yaml_to_liberty_writer_simple_gscl45nm_take_2):
  operating_conditions_dict = yaml_to_liberty_writer_simple_gscl45nm_take_2.yaml_file.get("library").get("operating_conditions")

  timing_dict = yaml_to_liberty_writer_simple_gscl45nm_take_2.yaml_file.get("library").get("cell")[0].get("pin")[1].get("timing")
  
  expected_1 = """operating_conditions(typical) {
  process : "1";
  voltage : "1.1";
  temperature : "27";
}"""

  expected_2 = """timing() {
  related_pin : "A";
  timing_sense : "positive_unate";
  cell_rise(scalar) {
    values("0.0");
  }
  rise_transition(scalar) {
    values("0.0");
  }
  cell_fall(scalar) {
    values("0.0");
  }
  fall_transition(scalar) {
    values("0.0");
  }
}"""
  assert repr(yaml_to_liberty_writer_simple_gscl45nm_take_2.get_dict_as_string_recursive("operating_conditions", operating_conditions_dict)) == repr(expected_1)

  print("expected: \n" + expected_2)
  print("dict: \n" + str(timing_dict))
  print("actual: \n" + yaml_to_liberty_writer_simple_gscl45nm_take_2.get_dict_as_string_recursive("timing", timing_dict))
  
  assert repr(yaml_to_liberty_writer_simple_gscl45nm_take_2.get_dict_as_string_recursive("timing", timing_dict)) == repr(expected_2)



  