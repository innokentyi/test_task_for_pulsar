from re import search

def split_file_to_path_and_format(path: str) -> tuple:
    match = search('(.*)\.(.*)', path)
    return match.group(1), match.group(2)
