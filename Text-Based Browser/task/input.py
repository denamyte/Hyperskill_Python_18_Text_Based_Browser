INVALID_URL = 'Invalid URL\n'


class IOChecker:
    @staticmethod
    def is_url(url: str) -> bool:
        return not url.startswith('.') and '.' in url

    @staticmethod
    def is_short(name: str):
        return '.' not in name

    @staticmethod
    def print_content_or_error(content: str = ''):
        print(content if content else INVALID_URL)
