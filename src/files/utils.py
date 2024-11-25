import os
from uuid import uuid4


def make_unique_filename(filename: str) -> str:
    split_name = os.path.splitext(filename)

    original_name = split_name[0]
    file_extension = split_name[-1]

    return f"{uuid4()}-{original_name}{file_extension}"
