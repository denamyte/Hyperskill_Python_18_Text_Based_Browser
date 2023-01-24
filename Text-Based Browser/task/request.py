import requests
from bs4 import BeautifulSoup
from colorama import Fore

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

        for elem in soup.body.descendants:
            if elem and elem.name and elem.name == 'a':
                elem.string = "".join([Fore.BLUE, elem.get_text(), Fore.RESET])

        return soup.get_text()
