from pathlib import Path
import pytest
from src import constants_yaml_to_liberty_writer

SEED_TEST_GSCL45NM_LIB_PATH = Path(
    "tests/test_input_files/seed_test_gscl45nm.lib").absolute()
SIMPLE_GSCL45NM_YAML_PATH = Path("tests/test_input_files/simple_gscl45nm.yaml")


@pytest.fixture
def seed_test_gscl45nm_lib_file():
  with open(SEED_TEST_GSCL45NM_LIB_PATH, 'r') as file:
    yield file

@pytest.fixture
def simple_gscl45nm_yaml_file():
  with open(SIMPLE_GSCL45NM_YAML_PATH, 'r') as file:
    yield file