import requests
from bs4 import BeautifulSoup

PROTOCOL = 'https://'


class Request:
    @staticmethod
    def get(url: str) -> str:
        if not url.startswith(PROTOCOL):
            url = PROTOCOL + url
        res = requests.get(url)
        if not res:
            return ''
        content = res.content
        soup = BeautifulSoup(content, features='html.parser')

        text_list = []

        text = soup.get_text("\n", True)
        return text
