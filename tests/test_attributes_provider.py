from pathlib import Path
import pytest
from src.attributes_provider import AttributesProvider

LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_simple_attributes.txt").absolute()

SIMPLE_ATTRIBUTES_LIST = {
    "bus_naming_style", "comment", "current_unit", "date", "delay_model",
    "em_temp_degradation_factor", "fpga_technology", "in_place_swap_mode",
    "input_threshold_pct_fall", "input_threshold_pct_rise",
    "leakage_power_unit", "nom_calc_mode", "nom_process", "nom_temperature",
    "nom_voltage", "output_threshold_pct_fall", "output_threshold_pct_rise",
    "piece_type", "power_model", "preferred_output_pad_slew_rate_control",
    "preferred_input_pad_voltage", "preferred_output_pad_voltage",
    "pulling_resistance_unit", "revision", "simulation",
    "slew_derate_from_library", "slew_lower_threshold_pct_fall",
    "slew_lower_threshold_pct_rise", "slew_upper_threshold_pct_fall",
    "slew_upper_threshold_pct_rise", "time_unit", "voltage_unit"
}

LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_default_attributes.txt").absolute()
LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_scaling_attributes.txt").absolute()


@pytest.fixture
def library_level_simple_attributes_file():
  with open(LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def library_level_default_attributes_file():
  with open(LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def library_level_scaling_attributes_file():
  with open(LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def attributes_provider(library_level_simple_attributes_file, library_level_default_attributes_file, library_level_scaling_attributes_file):
  return AttributesProvider(library_level_simple_attributes_file,
                            library_level_default_attributes_file,
                            library_level_scaling_attributes_file)


def test_get_library_level_simple_attributes(attributes_provider):
  assert attributes_provider.get_library_level_simple_attributes(
  ) == SIMPLE_ATTRIBUTES_LIST

# TODO - add tests for get_library_level_default_attributes and get_library_level_scaling_attributes