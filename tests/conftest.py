from pathlib import Path
import pytest
from src.attributes_provider import AttributesProvider

LIBRARY_LEVEL_SIMPLE_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_simple_attributes_to_types_mapping.json").absolute()
LIBRARY_LEVEL_DEFAULT_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_default_attributes_to_types_mapping.json").absolute()
LIBRARY_LEVEL_SCALING_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level_scaling_attributes_to_types_mapping.json").absolute()
gscl45nm = Path("tests/test_input_files/gscl45nm.yaml").absolute()

@pytest.fixture
def gscl45nm_yaml_file():
  with open(gscl45nm, 'r') as file:
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
def attributes_provider(library_level_simple_attributes_file, library_level_default_attributes_file, library_level_scaling_attributes_file):
  return AttributesProvider(library_level_simple_attributes_file,
                            library_level_default_attributes_file,
                            library_level_scaling_attributes_file)