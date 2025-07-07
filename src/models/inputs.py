from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Inputs:
    data_directory: str
    source_connection_string: str
    source_database: str
    source_tier: str
    destination_connection_string: str
    destination_database: str
    destination_tier: str
    exclude_collections: Optional[List[str]] = None
    flag_collections: Optional[List[str]] = None
    run_database_connection_test: bool = True
    run_source_data_export: bool = True
    run_destination_data_backup: bool = True
    run_review_prompt: bool = True
    run_data_migration: bool = True 