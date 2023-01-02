import requests
from bs4 import BeautifulSoup

PROTOCOL = 'https://'
# ALLOWED_TAGS = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'a', 'li']
ALLOWED_TAGS = ['p', *(f'h{i}' for i in range(1, 7)), 'a', 'ul', 'ol', 'li']


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
        tags = soup.find_all(True)
        for tag in tags:
            if tag.name in ALLOWED_TAGS and tag.string and tag.contents[0] == tag.string:
                text_list.append(str(tag.string))
        return '\n'.join(text_list)
