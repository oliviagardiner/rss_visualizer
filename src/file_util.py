#!/usr/bin/python3

import os
from pathlib import Path
from dotenv import load_dotenv

class FileUtil():
    ABS_PATH = os.path.dirname(__file__)

    def __init__(self) -> None:
        load_dotenv()

    def get_abs_path(self, path: str) -> str:
        return os.path.abspath(os.path.join(
            self.ABS_PATH, '../' + path))

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
    
    def save_to_path(self, data, path: str) -> None:
        handler = open(path, 'wb')
        handler.write(data)

    def save_to_path_utf8(self, data, path: str) -> None:
        try:
            handler = open(path, 'x', encoding='utf-8')
        except FileExistsError as err:
            handler = open(path, 'w', encoding='utf-8')
        finally:
            handler.write(data)
            handler.close()
