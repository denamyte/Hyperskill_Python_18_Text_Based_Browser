from request import PROTOCOL


class Utils:
    @staticmethod
    def is_url(url: str) -> bool:
        return not url.startswith('.') and '.' in url

    @staticmethod
    def make_short(url: str) -> str:
        if url.startswith(PROTOCOL):
            url = url[len(PROTOCOL):]
        url = url[:url.index('.')]
        return url
