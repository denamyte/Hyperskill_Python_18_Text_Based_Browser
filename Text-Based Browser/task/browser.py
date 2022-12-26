from sys import argv
from storage import Storage, Previous
from utils import Utils
from request import Request
INVALID_URL = 'Invalid URL\n'


def main():
    if len(argv) != 2:
        return
    storage = Storage(argv[1])
    utils = Utils()
    request = Request()
    prev = Previous()

    while True:
        content, cmd = '', input()

        if cmd == 'exit':
            break

        if cmd == 'back':
            short = prev.pop()
            if not short:
                continue
            content = storage.get_file_content(short)

        if utils.is_url(cmd):
            short = utils.make_short(cmd)
            content = storage.get_file_content(short)
            if not content:
                content = request.get(cmd)
                if content:
                    storage.save_content(short, content)
            if content:
                prev.add(short)

        print(content if content else INVALID_URL)


if __name__ == '__main__':
    main()
