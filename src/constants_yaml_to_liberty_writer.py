from pathlib import Path

LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH = Path("supported_attributes/library_level_simple_attributes_to_types_mapping.json").absolute()
LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH = Path("supported_attributes/library_level_simple_attributes_to_types_mapping.json").absolute()
LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH = Path("supported_attributes/library_level_scaling_attributes_to_types_mapping.json").absolute()
CELL_GROUP_SIMPLE_ATTRIBUTES_PATH = Path("supported_attributes/cell_group_simple_attributes_to_types_mapping.json").absolute()
PIN_GROUP_SIMPLE_ATTRIBUTES_PATH = Path("supported_attributes/pin_group_simple_attributes_to_types_mapping.json").absolute()
TIMING_GROUP_SIMPLE_ATTRIBUTES_PATH = Path("supported_attributes/timing_group_simple_attributes_to_types_mapping.json").absolute()
TIMING_GROUP_GROUP_ATTRIBUTES_PATH = Path("supported_attributes/timing_group_group_attributes.json").absolute()
PIN_GROUP_GROUP_ATTRIBUTES_PATH = Path("supported_attributes/pin_group_group_attributes.json").absolute()

# these are the names that go into the keys for the attributes dict in AttributesProvider
LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_STR = "library_level_simple_attributes"
LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_STR = "library_level_default_attributes"
LIBRARY_LEVEL_SCALING_ATTRIBUTES_STR = "library_level_scaling_attributes"
CELL_GROUP_SIMPLE_ATTRIBUTES_STR = "cell_group_simple_attributes"
PIN_GROUP_SIMPLE_ATTRIBUTES_STR = "pin_group_simple_attributes"
TIMING_GROUP_SIMPLE_ATTRIBUTES_STR = "timing_group_simple_attributes"
TIMING_GROUP_GROUP_ATTRIBUTES_STR = "timing_group_group_attributes"
PIN_GROUP_GROUP_ATTRIBUTES_STR = "pin_group_group_attributes"

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

LEVEL_TYPE_STR = "level_type"
VALS_STR = "vals"
GROUP_STR = "group"
COMPLEX_STR = "complex"

PARAM_INDICATOR_CHAR = "$"

INSIDE_LIBRARY_NUM_SPACES = 2
INSIDE_CELL_GROUP_NUM_SPACES = 4
INSIDE_PIN_GROUP_NUM_SPACES = 6
INSIDE_TIMING_GROUP_NUM_SPACES = 8