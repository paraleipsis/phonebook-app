import json

from typing import Optional, Mapping, Any


def httpize(
        d: Optional[Mapping]
) -> Optional[Mapping[str, Any]]:
    """
    Convert given dictionary to HTTP JSON-like format.

    :param d:
        Dict to convert.
    """

    if d is None:
        return None
    converted = {}
    for k, v in d.items():
        if isinstance(v, bool):
            v = "1" if v else "0"
        if not isinstance(v, str):
            v = json.dumps(v)
        converted[k] = v

    return converted
