import os

def normalize_file_paths(file_paths):
    """Convert single path or list of paths to a list of normalized paths."""
    if isinstance(file_paths, str):
        return [os.path.normpath(file_paths)]
    return [os.path.normpath(path) for path in (file_paths or [])]
