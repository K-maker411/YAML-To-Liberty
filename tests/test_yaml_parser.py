from pathlib import Path
import pytest
from src.yaml_parser import YamlParser

VALID_LIB_LEVEL_ATTRIBUTES_PATH = Path(
    "tests/test_input_files/valid_lib_level_attributes.yaml").absolute()
INVALID_LIB_LEVEL_ATTRIBUTES_PATH = Path(
    "tests/test_input_files/invalid_lib_level_attributes.yaml").absolute()
LIB_LEVEL_SUPPORTED_ATTRIBUTES_PATH = Path(
    "supported_attributes/library_level.txt").absolute()


@pytest.fixture
def valid_lib_level_attributes_test_file():
    with open(VALID_LIB_LEVEL_ATTRIBUTES_PATH, 'r') as file:
        yield file


@pytest.fixture
def invalid_lib_level_attributes_test_file():
    with open(INVALID_LIB_LEVEL_ATTRIBUTES_PATH, 'r') as file:
        yield file


@pytest.fixture
def lib_level_supported_attributes_test_file():
    with open(LIB_LEVEL_SUPPORTED_ATTRIBUTES_PATH, 'r') as file:
        yield file


@pytest.fixture
def invalid_lib_level_attributes_yaml_parser(
        invalid_lib_level_attributes_test_file,
        lib_level_supported_attributes_test_file):
    return YamlParser(invalid_lib_level_attributes_test_file,
                      lib_level_supported_attributes_test_file)


@pytest.fixture
def valid_lib_level_attributes_yaml_parser(
        valid_lib_level_attributes_test_file,
        lib_level_supported_attributes_test_file):
    return YamlParser(valid_lib_level_attributes_test_file,
                      lib_level_supported_attributes_test_file)


# check_library_level_attributes() test - check that function returns true when yaml is valid and that there was no logging
def test_check_library_level_attributes_valid(
        valid_lib_level_attributes_yaml_parser, caplog):
    assert valid_lib_level_attributes_yaml_parser.check_library_level_attributes()
    assert not caplog.records

# check_library_level_attributes() test - check that function returns false when yaml is invalid and that there was logging 
def test_check_library_level_attributes_invalid(invalid_lib_level_attributes_yaml_parser, caplog):
    assert not invalid_lib_level_attributes_yaml_parser.check_library_level_attributes()
    found_error_message_1 = False
    found_error_message_2 = False
    for record in caplog.records:
        if record.levelname == "ERROR":
            if "'nom' not in provided library-level supported attributes." in record.message:
                found_error_message_1 = True
            elif "'slow_upper_threshold_pct_rise' not in provided library-level supported attributes." in record.message:
                found_error_message_2 = True

    assert found_error_message_1 and found_error_message_2

# TODO - add tests for this later (once more stuff is complete)
def test_check_library_level():
    pass
