import os
import tempfile
import pytest
from src.parse_inputs import parse_inputs, Inputs

def write_yaml_file(data):
    import yaml
    fd, path = tempfile.mkstemp(suffix='.yaml')
    with os.fdopen(fd, 'w') as tmp:
        yaml.dump(data, tmp)
    return path

def test_valid_full_inputs():
    data = {
        'data_directory': 'data',
        'source_connection_string': 'mongodb://user:pass@host:27017/',
        'source_database': 'db',
        'source_tier': 'tier',
        'destination_connection_string': 'mongodb://user:pass@host:27017/',
        'destination_database': 'db2',
        'destination_tier': 'tier2',
        'exclude_collections': [],
        'flag_collections': [],
        'run_database_connection_test': False,
        'run_source_data_export': False,
        'run_destination_data_backup': False,
        'run_review_prompt': False,
        'run_data_migration': False,
    }
    path = write_yaml_file(data)
    result = parse_inputs(path)
    assert isinstance(result, Inputs)
    os.remove(path)

def test_invalid_source_connection_string():
    data = {
        'data_directory': 'data',
        'source_connection_string': 'invalid',
        'source_database': 'db',
        'source_tier': 'tier',
        'destination_connection_string': 'mongodb://user:pass@host:27017/',
        'destination_database': 'db2',
        'destination_tier': 'tier2',
        'exclude_collections': [],
        'flag_collections': [],
        'run_database_connection_test': True,
        'run_source_data_export': False,
        'run_destination_data_backup': False,
        'run_review_prompt': False,
        'run_data_migration': False,
    }
    path = write_yaml_file(data)
    with pytest.raises(ValueError, match="Invalid source connection string"):
        parse_inputs(path)
    os.remove(path)

def test_valid_source_data_export():
    data = {
        'data_directory': 'data',
        'source_connection_string': 'mongodb://user:pass@host:27017/',
        'source_database': 'db',
        'source_tier': 'tier',
        'destination_connection_string': 'mongodb://user:pass@host:27017/',
        'destination_database': '',
        'destination_tier': '',
        'exclude_collections': [],
        'flag_collections': [],
        'run_database_connection_test': False,
        'run_source_data_export': True,
        'run_destination_data_backup': False,
        'run_review_prompt': False,
        'run_data_migration': False,
    }
    path = write_yaml_file(data)
    result = parse_inputs(path)
    assert isinstance(result, Inputs)
    os.remove(path)

def test_invalid_data_directory():
    data = {
        'data_directory': '',
        'source_connection_string': 'mongodb://user:pass@host:27017/',
        'source_database': 'db',
        'source_tier': 'tier',
        'destination_connection_string': 'mongodb://user:pass@host:27017/',
        'destination_database': 'db2',
        'destination_tier': 'tier2',
        'exclude_collections': [],
        'flag_collections': [],
        'run_database_connection_test': False,
        'run_source_data_export': True,
        'run_destination_data_backup': False,
        'run_review_prompt': False,
        'run_data_migration': False,
    }
    path = write_yaml_file(data)
    with pytest.raises(ValueError, match="Invalid data directory"):
        parse_inputs(path)
    os.remove(path) 