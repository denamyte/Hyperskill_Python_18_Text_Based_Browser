import os
from typing import List


class Storage:
    def __init__(self, folder: str):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)

    def get_file_content(self, file_name: str) -> str:
        path = os.path.join(self.folder, file_name)
        if os.path.exists(path):
            with open(path, 'rt') as file:
                return ''.join(file.readlines())
        return ''

    def save_content(self, file_name: str, content: str):
        if not content:
            return
        short = file_name[:file_name.index('.')]
        full_name = os.path.join(self.folder, short)
        with open(full_name, 'w') as file:
            file.write(content)
