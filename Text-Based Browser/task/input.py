# INCORRECT_URL = 'Error: Incorrect URL\n'
INVALID_URL = 'Invalid URL\n'


class IOChecker:
    def __init__(self):
        pass

    @staticmethod
    def is_url(url: str) -> bool:
        return not url.startswith('.') and '.' in url

    @staticmethod
    def is_short(name: str):
        return '.' not in name

    @staticmethod
    def print_content_or_error(content: str = ''):
        print(content if content else INVALID_URL)
