from pathlib import Path
import pytest
from src.attributes_provider import AttributesProvider
from src import constants_yaml_to_liberty_writer

LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_simple_attributes_to_types_mapping.json"
).absolute()
LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_default_attributes_to_types_mapping.json"
).absolute()
LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_scaling_attributes_to_types_mapping.json"
).absolute()
gscl45nm = Path("tests/test_input_files/gscl45nm.yaml").absolute()
simple_gscl45nm = Path(
    "tests/test_input_files/simple_gscl45nm.yaml").absolute()
CELL_GROUP_SIMPLE_ATTRIBUTES_PATH = Path(
    "supported_attributes/cell_group_simple_attributes_to_types_mapping.json"
).absolute()
PIN_GROUP_SIMPLE_ATTRIBUTES_PATH = Path(
    "supported_attributes/pin_group_simple_attributes_to_types_mapping.json"
).absolute()
TIMING_GROUP_SIMPLE_ATTRIBUTES_PATH = Path(
    "supported_attributes/timing_group_simple_attributes_to_types_mapping.json"
).absolute()
TIMING_GROUP_GROUP_ATTRIBUTES_PATH = Path(
    "supported_attributes/timing_group_group_attributes.json").absolute()
PIN_GROUP_GROUP_ATTRIBUTES_PATH = Path(
    "supported_attributes/pin_group_group_attributes.json").absolute()
SEED_TEST_GSCL45NM_LIB_PATH = Path(
    "tests/test_input_files/seed_test_gscl45nm.lib").absolute()
SEED_TEST_GSCL45NM_YAML_PATH = Path(
    "tests/test_input_files/seed_test_gscl45nm.yaml").absolute()


@pytest.fixture
def gscl45nm_yaml_file():
  with open(gscl45nm, 'r') as file:
    yield file


@pytest.fixture
def simple_gscl45nm_yaml_file():
  with open(simple_gscl45nm, 'r') as file:
    yield file


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
def cell_group_simple_attributes_file():
  with open(CELL_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def pin_group_simple_attributes_file():
  with open(PIN_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def timing_group_simple_attributes_file():
  with open(TIMING_GROUP_SIMPLE_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def timing_group_group_attributes_file():
  with open(TIMING_GROUP_GROUP_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def pin_group_group_attributes_file():
  with open(PIN_GROUP_GROUP_ATTRIBUTES_PATH, 'r') as file:
    yield file


@pytest.fixture
def attributes_provider(
    library_level_simple_attributes_file,
    library_level_default_attributes_file,
    library_level_scaling_attributes_file, cell_group_simple_attributes_file,
    pin_group_simple_attributes_file, timing_group_simple_attributes_file,
    timing_group_group_attributes_file, pin_group_group_attributes_file):
  attributes_dict = {
      constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_STR:
      library_level_simple_attributes_file,
      constants_yaml_to_liberty_writer.LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_STR:
      library_level_default_attributes_file,
      constants_yaml_to_liberty_writer.LIBRARY_LEVEL_SCALING_ATTRIBUTES_STR:
      library_level_scaling_attributes_file,
      constants_yaml_to_liberty_writer.CELL_GROUP_SIMPLE_ATTRIBUTES_STR:
      cell_group_simple_attributes_file,
      constants_yaml_to_liberty_writer.PIN_GROUP_SIMPLE_ATTRIBUTES_STR:
      pin_group_simple_attributes_file,
      constants_yaml_to_liberty_writer.TIMING_GROUP_SIMPLE_ATTRIBUTES_STR:
      timing_group_simple_attributes_file,
      constants_yaml_to_liberty_writer.TIMING_GROUP_GROUP_ATTRIBUTES_STR:
      timing_group_group_attributes_file,
      constants_yaml_to_liberty_writer.PIN_GROUP_GROUP_ATTRIBUTES_STR:
      pin_group_group_attributes_file
  }
  return AttributesProvider(attributes_dict)


@pytest.fixture
def seed_test_gscl45nm_lib_file():
  with open(SEED_TEST_GSCL45NM_LIB_PATH, 'r') as file:
    yield file


@pytest.fixture
def seed_test_gscl45nm_yaml_file():
  with open(SEED_TEST_GSCL45NM_YAML_PATH, 'r') as file:
    yield file
