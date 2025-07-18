import os
import json

class MetadataManager:
    def __init__(self, metadata_file):
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        """Loads metadata from file or initializes an empty list."""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                data = json.load(f)
                return data if isinstance(data, list) else [data]
        return []

    def has_hash(self, file_hash):
        """Checks if a file hash exists in metadata."""
        return any(entry['file_hash'] == file_hash for entry in self.metadata)

    def has_file_path(self, file_path):
        """Checks if a file path exists in metadata."""
        file_path = os.path.normpath(file_path)
        return any(os.path.normpath(entry['file_path']) == file_path for entry in self.metadata)

    def add_entry(self, file_path, file_hash):
        """Adds a new metadata entry."""
        self.metadata.append({
            'file_path': os.path.normpath(file_path),
            'file_hash': file_hash
        })

    def remove_by_hash(self, file_hash):
        """Removes metadata entries by file hash."""
        self.metadata = [entry for entry in self.metadata if entry['file_hash'] != file_hash]

    def save(self):
        """Saves metadata to file."""
        os.makedirs(os.path.dirname(self.metadata_file), exist_ok=True)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=4)