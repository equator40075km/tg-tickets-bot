from json import load
from typing import Union


MSGS_FILE = 'handlers/messages.json'


def load_json(path: str) -> Union[dict, None]:
    data = None
    with open(path) as jsonfile:
        data = load(jsonfile)

    return data


def load_messages() -> Union[dict, None]:
    return load_json(MSGS_FILE)
