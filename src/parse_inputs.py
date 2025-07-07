import os
import yaml
import re
from dataclasses import dataclass
from typing import List, Optional
from src.models.inputs import Inputs

def parse_inputs(inputs_file: str) -> Inputs:
    if not os.path.exists(inputs_file):
        raise FileNotFoundError(f"Inputs file {inputs_file} not found")
    inputs_dict = yaml.safe_load(open(inputs_file, 'r'))

    valid_source_connection_string = _is_valid_mongo_connection_string(inputs_dict.get('source_connection_string'))
    valid_destination_connection_string = _is_valid_mongo_connection_string(inputs_dict.get('destination_connection_string'))
    valid_source_database = isinstance(inputs_dict.get('source_database'), str) and inputs_dict['source_database'] and inputs_dict['source_database'] != ""
    valid_source_tier = isinstance(inputs_dict.get('source_tier'), str) and inputs_dict['source_tier'] and inputs_dict['source_tier'] != ""
    valid_destination_database = isinstance(inputs_dict.get('destination_database'), str) and inputs_dict['destination_database'] and inputs_dict['destination_database'] != ""
    valid_destination_tier = isinstance(inputs_dict.get('destination_tier'), str) and inputs_dict['destination_tier'] and inputs_dict['destination_tier'] != ""
    valid_data_directory = isinstance(inputs_dict.get('data_directory'), str) and inputs_dict['data_directory'] and inputs_dict['data_directory'] != ""

    inputs = Inputs(**inputs_dict)

    if (inputs.run_database_connection_test):
        if (not valid_source_connection_string):
            raise ValueError("Invalid source connection string")
        if (not valid_destination_connection_string):
            raise ValueError("Invalid destination connection string")
    elif (inputs.run_source_data_export):
        if (not valid_source_connection_string):
            raise ValueError("Invalid source connection string")
        if (not valid_source_database):
            raise ValueError("Invalid source database")
        if (not valid_source_tier):
            raise ValueError("Invalid source tier")
        if (not valid_data_directory):
            raise ValueError("Invalid data directory")
    elif (inputs.run_destination_data_backup):
        if (not valid_destination_connection_string):
            raise ValueError("Invalid destination connection string")
        if (not valid_destination_database):
            raise ValueError("Invalid destination database")
        if (not valid_destination_tier):
            raise ValueError("Invalid destination tier")
    elif (inputs.run_data_migration):
        if (not valid_data_directory):
            raise ValueError("Invalid data directory")
        if (not valid_destination_connection_string):
            raise ValueError("Invalid destination connection string")
        if (not valid_destination_database):
            raise ValueError("Invalid destination database")
        if (not valid_destination_tier):
            raise ValueError("Invalid destination tier")
    return inputs

def _is_valid_mongo_connection_string(connection_string: str):
    MONGO_REGEX = r"^mongodb:\/\/[^:]+:[^@]+@[^:\/]+(:\d+)?\/$"
    return re.match(MONGO_REGEX, connection_string) is not None
