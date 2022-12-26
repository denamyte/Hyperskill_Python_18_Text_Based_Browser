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
        full_name = os.path.join(self.folder, file_name)
        with open(full_name, 'w') as file:
            file.write(content)


class Previous:
    def __init__(self):
        self._stack: List[str] = []

    def add(self, name: str):
        if name:
            self._stack.append(name)

    def pop(self) -> str:
        if len(self._stack) <= 1:
            return ''
        self._stack.pop()
        return self._stack[-1]
