def generate_id(data: dict) -> int:
    """
    Generate new ID for given dictionary.
    It takes last root key of dict and increment it
    or just return 1 if there is no data in dict.

    :param data:
        Dict to generate ID.
    """
    if data:
        new_id = int(sorted(data.keys())[-1]) + 1
        return new_id

    return 1
