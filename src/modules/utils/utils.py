from typing import List, Mapping


def convert_obj_to_list(dict_of_dicts: dict) -> List[Mapping]:
    """
    Convert dict of dict to list of dict and
    add root keys of origin dict as ID field in each dict in list.
    """
    return [(lambda d: d.update(id=key) or d)(val) for (key, val) in dict_of_dicts.items()]


def filter_none_values(dictionary: dict) -> dict:
    """
    Delete keys with None values from dict.
    """
    return {key: value for key, value in dictionary.items() if value is not None}
