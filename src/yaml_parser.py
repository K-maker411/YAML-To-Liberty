import logging
import yaml

logger = logging.getLogger("yaml_parser_logger")

# TODO - need to add checks for all fields individually (hoo boy) (not difficult, just really annoying)
class YamlParser:
    def __init__(self, yaml_file_read_stream, supported_library_level_attributes):
        self.loaded_yaml = yaml.safe_load(yaml_file_read_stream)
        # create a set from all of the supported library level attributes
        self.supported_library_level_attributes = {line.strip() for line in supported_library_level_attributes}
        # custom attributes in YAML that don't exist in .lib, but
        # are still allowed to exist (e.g. name is not a specific field in .lib because
        # it's provided in library("name"), but the way this is expressed in YAML is through a "name" key)
        self.supported_library_level_attributes.add("name")

    # TODO - test
    def check_library_level_attributes(self):
        # get all attributes at the library level (meaning not nested inside other attributes)
        library_level = self.loaded_yaml.get("library")
        # indicates if there's a field specified in yaml that's not in library-level supported attributes
        has_error = False
        # check every attribute on the library level in the yaml and check if its in the
        # file - if it's not, there's at least one error and thus we return false 
        # (however, we make sure to check every attribute and print it out)
        for attribute in library_level:
            #with open(self.supported_library_level_attributes_path, "r") as f:
            if attribute not in self.supported_library_level_attributes:
                has_error = True
                logging.error(f"'{attribute}' not in provided library-level supported attributes.")
                #print(f"'{attribute}' not in provided library-level supported attributes.")
        # if there's an error, return false, 
        # otherwise true (where true indicates success and false indicates failure)
        return not has_error

    # full check of everything
    # we will also check within each thing to make sure all values are valid 
    # (keep it modular)
    def is_formatted_correctly(self):
        return self.check_library_level_attributes()

    # gets value associated with key on lib level, returns none otherwise
    def get_value_from_key_lib_level(self, key):
        return self.loaded_yaml.get(key)






