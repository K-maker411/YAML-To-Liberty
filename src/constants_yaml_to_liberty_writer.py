from pathlib import Path

CELL_RISE = "cell_rise"
CELL_FALL = "cell_fall"
RISE_TRANSITION = "rise_transition"
FALL_TRANSITION = "fall_transition"
VALUES_STRING = "values(\"{}\")"
TIMING = "timings"
PIN = "pins"
CELL = "cells"
POWER_RAIL = "power_rail"
NAME = "name"
CAPACITIVE_LOAD_UNIT = "capacitive_load_unit"
OPERATING_CONDITIONS = "operating_conditions"

LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH = Path("supported_attributes/library_level_simple_attributes_to_types_mapping.json").absolute()
LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH = Path("supported_attributes/library_level_simple_attributes_to_types_mapping.json").absolute()
LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH = Path("supported_attributes/library_level_scaling_attributes_to_types_mapping.json").absolute()
CELL_GROUP_SIMPLE_ATTRIBUTES_PATH = Path("supported_attributes/cell_group_simple_attributes_to_types_mapping.json").absolute()
PIN_GROUP_SIMPLE_ATTRIBUTES_PATH = Path("supported_attributes/pin_group_simple_attributes_to_types_mapping.json").absolute()
TIMING_GROUP_SIMPLE_ATTRIBUTES_PATH = Path("supported_attributes/timing_group_simple_attributes_to_types_mapping.json").absolute()
TIMING_GROUP_GROUP_ATTRIBUTES_PATH = Path("supported_attributes/timing_group_group_attributes.json").absolute()
PIN_GROUP_GROUP_ATTRIBUTES_PATH = Path("supported_attributes/pin_group_group_attributes.json").absolute()

INSIDE_LIBRARY_NUM_SPACES = 2
INSIDE_CELL_GROUP_NUM_SPACES = 4
INSIDE_PIN_GROUP_NUM_SPACES = 6
INSIDE_TIMING_GROUP_NUM_SPACES = 8