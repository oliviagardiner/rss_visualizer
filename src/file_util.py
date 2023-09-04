#!/usr/bin/python3

import os
from pathlib import Path
from dotenv import load_dotenv

class FileUtil():
    ABS_PATH = os.path.dirname(__file__)

    def __init__(self) -> None:
        load_dotenv()

    def get_gen_path(self, subdir: str) -> str:
        if os.getenv('ABS_PATH') == 'true':
            return os.path.join(
                self.ABS_PATH, os.getenv('GEN_DIR') + subdir)
        else:
            return os.getenv('GEN_DIR') + subdir
    
    def make_gen_path(self, subdir: str) -> str:
        path = self.get_gen_path(subdir)
        Path(path).mkdir(parents = True, exist_ok = True)
        return path
