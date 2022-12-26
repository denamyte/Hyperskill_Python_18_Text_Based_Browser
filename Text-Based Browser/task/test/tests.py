from hstest.stage_test import *
import requests
import os
import shutil
from bs4 import BeautifulSoup
import sys

if sys.platform.startswith("win"):
    import _locale
    # pylint: disable=protected-access
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

names = {'bloomberg': 'bloomberg.com',
         'docs': 'docs.python.org',
         'nytimes': 'nytimes.com'
         }


class TextBasedBrowserTest(StageTest):

    def generate(self):

        dir_for_files = os.path.join(os.curdir, 'tb_tabs')
        return [
            TestCase(
                stdin='bloomberg.com\nexit',
                attach='bloomberg.com',
                args=[dir_for_files]
            ),
            TestCase(
                stdin='docs.python.org\nexit',
                attach='docs.python.org',
                args=[dir_for_files]
            ),
            TestCase(
                stdin='nytimescom\nexit',
                attach=None,
                args=[dir_for_files]
            ),
            TestCase(
                stdin='back\nexit',
                attach='back',
                args=['tb_tabs']
            ),
            TestCase(
                stdin='bloomberg.com\ndocs.python.org\nbloomberg\nexit',
                attach=('bloomberg.com', 'docs.python.org', 'bloomberg.com'),
                args=[dir_for_files]
            ),
            TestCase(
                stdin='bloomberg.com\ndocs.python.org\nback\nexit',
                attach=('bloomberg.com', 'docs.python.org', 'docs.python.org'),
                args=['tb_tabs']
            )
        ]

    def check_output(self, output_text: str, ideal_text: list, page_code: list, source: str):
        """
        :param output_text: the text from the user's file or from the console output
        :param ideal_text: the text from the web page (without HTML tags)
        :param page_code: the text from the web page with HTML tags
        :param source: the name of the file from which the user's text is taken or "console output" line
        :return: raises WrongAnswer if an HTML tag is found in the output_text
        or if a word from the ideal_text is not found in the output_text
        """
        for line in page_code:
            if line not in ideal_text and line in output_text:
                raise WrongAnswer(f"The following token is present in the {source} even though it's not expected "
                                  f"to be there:\n\'{line}\'\n"
                                  f"Make sure you get rid of all HTML tags.")
        output_text = ''.join(char for char in output_text if char.isalnum())
        for line in ideal_text:
            line_without_spaces = ''.join(char for char in line if char.isalnum())
            if line_without_spaces.strip() not in output_text:
                raise WrongAnswer(f"The following token is missing from the {source}:\n"
                                  f"\'{line}\'\n"
                                  f"Make sure you get all the text from the web page.")

    def _check_files(self, path_for_tabs: str, ideal_page: list, page_code: list, attach: str):
        """
        Helper which checks that browser saves visited url in files and
        provides access to them.

        :param path_for_tabs: directory which must contain saved tabs
        :param ideal_page: the text from the web page (without HTML tags)
        :param page_code: the text from the web page with HTML tags
        """

        path, dirs, filenames = next(os.walk(path_for_tabs))

        name = attach.split('.')[0]
        if name in filenames:
            print("found file: {}".format(name))
            with open(os.path.join(path_for_tabs, name), 'r', encoding='utf-8') as tab:
                try:
                    content = tab.read()
                except UnicodeDecodeError:
                    raise WrongAnswer('An error occurred while reading your saved tab. '
                                      'Perhaps you used the wrong encoding?')
                self.check_output(content, ideal_page, page_code, "file " + name)

        else:
            raise WrongAnswer(f"Couldn't find file with the name {name}.\n"
                              f"Make sure you saved the tab and named it correctly.")

    @staticmethod
    def get_page_and_code(url):
        """
        :param url: url link that the program is requested to open
        :return: list with strings of clean text and list of strings with text with HTML tags
        """

        url = f'https://{url}'
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/70.0.3538.77 Safari/537.36"
        try:
            page = requests.get(url, headers={'User-Agent': user_agent})
        except requests.exceptions.ConnectionError:
            raise WrongAnswer(f"An error occurred while tests tried to connect to the page {url}.\n"
                              f"Please try again a bit later.")
        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.find_all(['p', 'a', 'h1', 'h2', 'ul', 'ol', 'li'])
        text = []
        tagged_text = []
        for tag in tags:
            tag_text = tag.text.strip()
            if tag_text:
                text.append(tag_text)
            tag = str(tag)
            if tag.startswith('<'):
                tagged_text.append(tag)
        return text, tagged_text

    def check_correct_url(self, attach_0: str, path_for_tabs: str, reply):

        ideal_text, page_code = TextBasedBrowserTest.get_page_and_code(attach_0)
        self._check_files(path_for_tabs, ideal_text, page_code, attach_0)
        self.check_output(reply, ideal_text, page_code, "console output")

    def check(self, reply, attach):

        # Incorrect URL
        if attach is None:
            if 'invalid url' in reply.lower():
                return CheckResult.correct()
            else:
                return CheckResult.wrong('An invalid URL was input to your program.\n'
                                         'Your program should print \'Invalid URL\'.')

        if attach == 'back':
            if not reply:
                return CheckResult.correct()
            else:
                return CheckResult.wrong(f'There should be no output. But your program printed: {reply}')

        # Correct URL
        path_for_tabs = os.path.join(os.curdir, 'tb_tabs')

        if not os.path.isdir(path_for_tabs):
            return CheckResult.wrong("There is no directory for tabs")

        if isinstance(attach, tuple):
            for element in attach:
                attach_0 = element
                self.check_correct_url(attach_0, path_for_tabs, reply)

        elif isinstance(attach, str):
            attach_0 = attach
            self.check_correct_url(attach_0, path_for_tabs, reply)

        try:
            shutil.rmtree(path_for_tabs)
        except PermissionError:
            return CheckResult.wrong("Impossible to remove the directory for tabs. "
                                     "Perhaps you haven't closed some file?")

        return CheckResult.correct()


if __name__ == '__main__':
    TextBasedBrowserTest().run_tests()
