"""
JSON Storage Infrastructure
"""

import json
import os
from typing import List, Optional, Any


class JSONStorage:
    """Generic JSON file storage handler."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create file with empty array if it doesn't exist."""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path) if os.path.dirname(self.file_path) else '.', exist_ok=True)
            with open(self.file_path, 'w') as f:
                json.dump([], f)
    
    def read(self) -> List[dict]:
        """Read all records from the JSON file."""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def write(self, data: List[dict]):
        """Write all records to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def append(self, record: dict) -> dict:
        """Append a single record and return it."""
        records = self.read()
        records.append(record)
        self.write(records)
        return record
    
    def find_by(self, key: str, value: Any) -> Optional[dict]:
        """Find first record matching key/value."""
        records = self.read()
        for record in records:
            if record.get(key) == value:
                return record
        return None
    
    def find_all_by(self, key: str, value: Any) -> List[dict]:
        """Find all records matching key/value."""
        records = self.read()
        return [r for r in records if r.get(key) == value]
    
    def update(self, key: str, value: Any, updates: dict) -> bool:
        """Update first matching record. Returns True if found."""
        records = self.read()
        for i, record in enumerate(records):
            if record.get(key) == value:
                records[i].update(updates)
                self.write(records)
                return True
        return False
    
    def delete_by(self, key: str, value: Any) -> bool:
        """Delete first matching record. Returns True if found."""
        records = self.read()
        for i, record in enumerate(records):
            if record.get(key) == value:
                records.pop(i)
                self.write(records)
                return True
        return False
    
    def clear(self):
        """Clear all records."""
        self.write([])