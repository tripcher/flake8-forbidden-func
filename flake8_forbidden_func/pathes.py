from __future__ import annotations


def convert_python_filepath_to_importable(filepath: str) -> str:
    return filepath[:-3].replace('/', '.')
