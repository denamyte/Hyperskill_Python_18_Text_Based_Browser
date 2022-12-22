from sys import argv
from sites import SITES
from storage import Storage
from input import IOChecker


def main():
    if len(argv) != 2:
        return
    storage = Storage(argv[1])
    io_checker = IOChecker()

    while True:
        content, cmd = '', input()

        if cmd == 'exit':
            break

        if io_checker.is_short(cmd):
            content = storage.get_file_content(cmd)
        elif io_checker.is_url(cmd):
            content = SITES.get(cmd)
            storage.save_content(cmd, content)

        io_checker.print_content_or_error(content)


if __name__ == '__main__':
    main()
