#!/usr/bin/python3

import os
from dotenv import load_dotenv

class EnvUtil():
    def __init__(self) -> None:
        load_dotenv()

    def parse_config_to_list(config: str, separator: str = ',') -> list:
        configlist = str(os.getenv(config))

        return configlist.split(separator)
