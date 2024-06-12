
LIB_LEVEL_SIMPLE_ATTRIBUTES_LIST = {
  "bus_naming_style": {"type": ["string"]},
  "comment": {"type": ["string"]},
  "current_unit": {"type": ["valueenum"]},
  "date": {"type": ["date"]},
  "delay_model": {"type": ["valueenum"]},
  "em_temp_degradation_factor": {"type": ["float"]},
  "fpga_technology": {"type": ["fpga_technology_name_string"]},
  "in_place_swap_mode": {"type": ["valueenum"]},
  "input_threshold_pct_fall": {"type": ["trip_point_value"]},
  "input_threshold_pct_rise": {"type": ["trip_point_value"]},
  "leakage_power_unit": {"type": ["valueenum"]},
  "nom_calc_mode": {"type": ["nameid"]},
  "nom_process": {"type": ["float"]},
  "nom_temperature": {"type": ["float"]},
  "nom_voltage": {"type": ["float"]},
  "output_threshold_pct_fall": {"type": ["trip_point_value"]},
  "output_threshold_pct_rise": {"type": ["trip_point_value"]},
  "piece_type": {"type": ["valueenum"]},
  "power_model": {"type": ["table_lookup", "polynomial"]},
  "preferred_output_pad_slew_rate_control": {"type": ["valueenum"]},
  "preferred_input_pad_voltage": {"type": ["string"]},
  "preferred_output_pad_voltage": {"type": ["string"]},
  "pulling_resistance_unit": ["1ohm", "10ohm", "100ohm", "1kohm"],
  "revision": {"type": ["float", "string"]},
  "simulation": [True, False],
  "slew_derate_from_library": {"type": ["derate_value"]},
  "slew_lower_threshold_pct_fall": {"type": ["trip_point_value"]},
  "slew_lower_threshold_pct_rise": {"type": ["trip_point_value"]},
  "slew_upper_threshold_pct_fall": {"type": ["trip_point_value"]},
  "slew_upper_threshold_pct_rise": {"type": ["trip_point_value"]},
  "time_unit": ["1ps", "10ps", "100ps", "1ns"],
  "voltage_unit": ["1mV", "10mV", "100mV", "1V"]
}

CELL_GROUP_SIMPLE_ATTRIBUTES_LIST = {
  "area": {"type": ["float"]},
  "auxiliary_pad_cell": [True, False],
  "base_name": {"type": ["string"]},
  "bus_naming_style": {"type": ["string"]},
  "cell_footprint": {"type": ["string"]},
  "cell_leakage_power": {"type": ["float"]},
  "clock_gating_integrated_cell": {"type": ["string"]},
  "contention_condition": {"type": ["string"]},
  "dont_fault": ["sa0", "sa1", "sa01"],
  "dont_touch": [True, False],
  "dont_use": [True, False],
  "driver_type": {"type": ["string"]},
  "edif_name": {"type": ["string"]},
  "em_temp_degradation_factor": {"type": ["float"]},
  "fpga_domain_style": {"type": ["string"]},
  "geometry_print": {"type": ["string"]},
  "handle_negative_constraint": [True, False],
  "interface_timing": [True, False],
  "io_type": {"type": ["string"]},
  "is_clock_gating_cell": [True, False],
  "map_only": [True, False],
  "pad_cell": [True, False],
  "pad_type": {"type": ["string"]},
  "power_cell_type": {"type": ["string"]},
  "preferred": [True, False],
  "scaling_factors": {"type": ["string"]},
  "single_bit_degenerate": {"type": ["string"]},
  "slew_type": {"type": ["string"]},
  "timing_model_type": {"type": ["string"]},
  "use_for_size_only": [True, False],
  "vhdl_name": {"type": ["string"]}
}



def test_get_library_level_simple_attributes(attributes_provider):
  pass
  #assert attributes_provider.get_library_level_simple_attributes(
  #) == LIB_LEVEL_SIMPLE_ATTRIBUTES_LIST

def test_get_cell_group_simple_attributes(attributes_provider):
  pass
  #assert attributes_provider.get_cell_group_simple_attributes(
  #) == CELL_GROUP_SIMPLE_ATTRIBUTES_LIST
  
  
# TODO - add tests for get_library_level_default_attributes and get_library_level_scaling_attributes