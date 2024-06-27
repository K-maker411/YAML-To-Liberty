import pytest
from pathlib import Path
from src.yaml_to_liberty_writer import YamlToLibertyWriter
from src import constants_yaml_to_liberty_writer
import yaml
from liberty.parser import parse_liberty
import dictdiffer

@pytest.fixture
def yaml_to_liberty_writer_simple_gscl45nm():
  return YamlToLibertyWriter()

@pytest.fixture
def simple_gscl45nm_dict(simple_gscl45nm_yaml_file):
  return yaml.safe_load(simple_gscl45nm_yaml_file)

def test_get_simple_attr_as_string(yaml_to_liberty_writer_simple_gscl45nm):
  attr_1 = "time_unit"
  attr_2 = "slew_upper_threshold_pct_rise"
  attr_3 = "current_unit"

  value_1 = "\"1ns\""
  value_2 = 80
  value_3 = "1uA"
  
  expected_1 = """time_unit : "1ns";\n"""
  expected_2 = """slew_upper_threshold_pct_rise : "80";\n"""
  expected_3 = """current_unit : "1uA";\n"""

  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_simple_attr_as_string(attr_1, value_1)) == repr(expected_1)
  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_simple_attr_as_string(attr_2, value_2)) == repr(expected_2)
  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_simple_attr_as_string(attr_3, value_3)) == repr(expected_3)

def test_get_complex_attr_as_string(yaml_to_liberty_writer_simple_gscl45nm):
  attr_1 = "index_1"
  attr_2 = "capacitive_load_unit"
  attr_3 = "values"
  
  value_1 = [1.0, 2.0, 3.0, 4.0, 5.0]
  value_2 = [1, "pf"]
  value_3 = [[0.007629, 0.007814, 0.008527, 0.011, 0.013036, 0.021415], [0.007847, 0.007969, 0.008127, 0.008954, 0.01012, 0.013793], [0.007598, 0.007574, 0.008075, 0.008447, 0.009083, 0.011614], [0.008148, 0.008291, 0.008042, 0.008235, 0.008524, 0.009792], [0.007902, 0.007896, 0.008061, 0.008321, 0.008456, 0.009447], [0.008154, 0.008144, 0.008174, 0.008374, 0.008494, 0.009334]]

  expected_1 = """index_1("1.0, 2.0, 3.0, 4.0, 5.0");\n"""
  expected_2 = """capacitive_load_unit(1, pf);\n"""
  expected_3 = """values("0.007629, 0.007814, 0.008527, 0.011, 0.01", "0.007847, 0.007969, 0.008127, 0.008954, 0.01012, 0.013793", "0.007598, 0.007574, 0.008075, 0.008447, 0.009083, 0.011614", "0.008148, 0.008291, 0.008042, 0.008235, 0.008524, 0.009792", "0.007902, 0.007896, 0.008061, 0.008321, 0.008456, 0.009447", "0.008154, 0.008144, 0.008174, 0.008374, 0.008494, 0.009334");"""

  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_complex_attr_as_string(attr_1, value_1)) == repr(expected_1)
  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_complex_attr_as_string(attr_2, value_2)) == repr(expected_2)
  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_complex_attr_as_string(attr_3, value_3) == repr(expected_3))

def test_get_group_as_string_recursive(yaml_to_liberty_writer_simple_gscl45nm, simple_gscl45nm_dict):
  dict_1 = simple_gscl45nm_dict.get("library").get("vals").get("operating_conditions")

  dict_2 = simple_gscl45nm_dict.get("library").get("vals").get("cell").get("vals")[0].get("pin").get("vals")[1].get("timing")

  dict_3 = simple_gscl45nm_dict.get("library").get("vals").get("cell").get("vals")[0].get("pin")

  dict_4 = simple_gscl45nm_dict.get("library").get("vals").get("cell")

  dict_5 = simple_gscl45nm_dict.get("library")
  
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

  expected_3 = """pin(A) {
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
  internal_power() {
    rise_power(energy_template_6x6) {
      index_1("0.1, 0.5, 1.2, 3, 4, 5");
      index_2("0.06, 0.24, 0.48, 0.9, 1.2, 1.8");
      values( \\
      "0.007629, 0.007814, 0.008527, 0.011, 0.013036, 0.021415", \\
      "0.007847, 0.007969, 0.008127, 0.008954, 0.01012, 0.013793", \\
      "0.007598, 0.007574, 0.008075, 0.008447, 0.009083, 0.011614", \\
      "0.008148, 0.008291, 0.008042, 0.008235, 0.008524, 0.009792", \\
      "0.007902, 0.007896, 0.008061, 0.008321, 0.008456, 0.009447", \\
      "0.008154, 0.008144, 0.008174, 0.008374, 0.008494, 0.009334");
    }
  }
}"""

  expected_4 = """cell(BUFX2) {
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
    internal_power() {
      rise_power(energy_template_6x6) {
        index_1("0.1, 0.5, 1.2, 3, 4, 5");
        index_2("0.06, 0.24, 0.48, 0.9, 1.2, 1.8");
        values( \\
        "0.007629, 0.007814, 0.008527, 0.011, 0.013036, 0.021415", \\
        "0.007847, 0.007969, 0.008127, 0.008954, 0.01012, 0.013793", \\
        "0.007598, 0.007574, 0.008075, 0.008447, 0.009083, 0.011614", \\
        "0.008148, 0.008291, 0.008042, 0.008235, 0.008524, 0.009792", \\
        "0.007902, 0.007896, 0.008061, 0.008321, 0.008456, 0.009447", \\
        "0.008154, 0.008144, 0.008174, 0.008374, 0.008494, 0.009334");
      }
    }
  }
}
cell(BUFX1) {
  cell_footprint : "buf";
}"""

  expected_5 = """library(gscl45nm) {
  delay_model : "table_lookup";
  in_place_swap_mode : "match_footprint";
  time_unit : "1ns";
  voltage_unit : "1V";
  current_unit : "1uA";
  pulling_resistance_unit : "1kohm";
  leakage_power_unit : "1nW";
  capacitive_load_unit(1, pf);
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
      internal_power() {
        rise_power(energy_template_6x6) {
          index_1("0.1, 0.5, 1.2, 3, 4, 5");
          index_2("0.06, 0.24, 0.48, 0.9, 1.2, 1.8");
          values( \\
          "0.007629, 0.007814, 0.008527, 0.011, 0.013036, 0.021415", \\
          "0.007847, 0.007969, 0.008127, 0.008954, 0.01012, 0.013793", \\
          "0.007598, 0.007574, 0.008075, 0.008447, 0.009083, 0.011614", \\
          "0.008148, 0.008291, 0.008042, 0.008235, 0.008524, 0.009792", \\
          "0.007902, 0.007896, 0.008061, 0.008321, 0.008456, 0.009447", \\
          "0.008154, 0.008144, 0.008174, 0.008374, 0.008494, 0.009334");
        }
      }
    }
  }
  cell(BUFX1) {
    cell_footprint : "buf";
  }
}"""

  print("Expected: \n" + expected_1)
  print("Actual: \n" + yaml_to_liberty_writer_simple_gscl45nm.get_group_as_string_recursive("operating_conditions", dict_1))
  
  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_group_as_string_recursive("operating_conditions", dict_1)) == repr(expected_1)

  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_group_as_string_recursive("timing", dict_2)) == repr(expected_2)

  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_group_as_string_recursive("pin", dict_3)) == repr(expected_3)

  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_group_as_string_recursive("cell", dict_4)) == repr(expected_4)

  assert repr(yaml_to_liberty_writer_simple_gscl45nm.get_group_as_string_recursive("library", dict_5)) == repr(expected_5)
  

def test_get_simple_and_complex_attrs_from_seed_group_as_dict(yaml_to_liberty_writer_simple_gscl45nm, seed_test_gscl45nm_lib_file):
  seed_test_gscl45nm_lib_file_dict = yaml_to_liberty_writer_simple_gscl45nm.get_simple_and_complex_attrs_from_seed_group_as_dict(parse_liberty(seed_test_gscl45nm_lib_file.read()))

  expected = {"delay_model": "table_lookup", "in_place_swap_mode": "match_footprint", "time_unit": "1ns", "voltage_unit": "1V", "current_unit": "1uA", "pulling_resistance_unit": "1kohm", "leakage_power_unit": "1nW", "capacitive_load_unit": {"level_type": "complex", "vals": [1, "pf"]}, "slew_upper_threshold_pct_rise": 80, "slew_lower_threshold_pct_rise": 20, "slew_upper_threshold_pct_fall": 80, "slew_lower_threshold_pct_fall": 20, "input_threshold_pct_rise": 50, "input_threshold_pct_fall": 50, "output_threshold_pct_rise": 50, "output_threshold_pct_fall": 50, "nom_process": 1, "nom_voltage": 1.1, "nom_temperature": 27, "default_operating_conditions": "typical"}

  print("Actual: \n" + str(seed_test_gscl45nm_lib_file_dict))
  print("Expected: \n" + str(expected))
  
  assert seed_test_gscl45nm_lib_file_dict == expected

def test_get_non_nested_group_attr_from_seed_as_dict(yaml_to_liberty_writer_simple_gscl45nm, seed_test_gscl45nm_lib_file):
  seed_test_gscl45nm_lib_file_dict = yaml_to_liberty_writer_simple_gscl45nm.get_non_nested_group_attr_from_seed_as_dict(parse_liberty(seed_test_gscl45nm_lib_file.read()))

  expected = {"delay_model": "table_lookup", "in_place_swap_mode": "match_footprint", "time_unit": "1ns", "voltage_unit": "1V", "current_unit": "1uA", "pulling_resistance_unit": "1kohm", "leakage_power_unit": "1nW", "capacitive_load_unit": {"level_type": "complex", "vals": [1, "pf"]}, "slew_upper_threshold_pct_rise": 80, "slew_lower_threshold_pct_rise": 20, "slew_upper_threshold_pct_fall": 80, "slew_lower_threshold_pct_fall": 20, "input_threshold_pct_rise": 50, "input_threshold_pct_fall": 50, "output_threshold_pct_rise": 50, "output_threshold_pct_fall": 50, "nom_process": 1, "nom_voltage": 1.1, "nom_temperature": 27, "default_operating_conditions": "typical", 
              "operating_conditions": 
              {"level_type": "group", "vals": {"$0": "typical", "process": 1, "voltage": 1.1, "temperature": 27}}, 
              "lu_table_template": 
              {"level_type": "group", "vals": 
               [
                 {"$0": "delay_template_4x5", "variable_1": "total_output_net_capacitance", "variable_2": "input_net_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0"]}},
                 
                 {"$0": "delay_template_5x1", "variable_1": "input_net_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0"]}},
                 
                 {"$0": "delay_template_6x1", "variable_1": "input_net_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},
                 
                 {"$0": "delay_template_6x6", "variable_1": "total_output_net_capacitance", "variable_2": "input_net_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},
                 
                 {"$0": "hold_template_3x6", "variable_1": "related_pin_transition", "variable_2": "constrained_pin_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},

                 {"$0": "recovery_template_3x6", "variable_1": "related_pin_transition", "variable_2": "constrained_pin_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},

                 {"$0": "recovery_template_6x6", "variable_1": "related_pin_transition", "variable_2": "constrained_pin_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},

                 {"$0": "removal_template_3x6", "variable_1": "related_pin_transition", "variable_2": "constrained_pin_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},

                 {"$0": "setup_template_3x6", "variable_1": "related_pin_transition", "variable_2": "constrained_pin_transition", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},
               ]},
             
             "power_lut_template": 
             {"level_type": "group", "vals": 
              [
                {"$0": "energy_template_4x5", "variable_1": "total_output_net_capacitance", "variable_2": "input_transition_time", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0"]}},
                
                {"$0": "energy_template_6x6", "variable_1": "total_output_net_capacitance", "variable_2": "input_transition_time", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}, "index_2": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},
              
                {"$0": "passive_energy_template_5x1", "variable_1": "input_transition_time", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0"]}},
                
                {"$0": "passive_energy_template_6x1", "variable_1": "input_transition_time", "index_1": {"level_type": "complex", "vals": ["1000.0, 1001.0, 1002.0, 1003.0, 1004.0, 1005.0"]}},
                
              ]}}
  print("Expected: \n" + str(expected))
  print("Actual: \n" + str(seed_test_gscl45nm_lib_file_dict))
  assert seed_test_gscl45nm_lib_file_dict == expected

  