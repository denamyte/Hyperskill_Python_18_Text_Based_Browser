import requests

PROTOCOL = 'https://'


class Request:
    @staticmethod
    def get(url: str) -> str:
        if not url.startswith(PROTOCOL):
            url = PROTOCOL + url
        res = requests.get(url)
        return '' if not res else res.text
