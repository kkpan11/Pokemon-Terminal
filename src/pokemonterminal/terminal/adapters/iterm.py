import os
import subprocess

from . import TerminalProvider as _TProv


class ItermProvider(_TProv):
    # OSA script that will change the terminal background image
    __osa_script_set = """tell application "iTerm2"
    \ttell current session of current window
    \t\tset background image to "{}"
    \tend tell
    end tell"""

    __osa_script_get = """tell application "iTerm2"
    \ttell current session of current window
    \t\treturn background image as text
    \tend tell
    end tell"""

    def is_compatible() -> bool:
        return "ITERM_PROFILE" in os.environ

    def __set_process(stream):
        proc = subprocess.Popen(["osascript"], stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        proc.stdin.write(stream)
        proc.communicate()
        proc.stdin.close()

    def __get_process(stream):
        proc = subprocess.Popen(["osascript"],
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.stdin.write(stream)
        path, err = proc.communicate()
        proc.stdin.close()
        return path

    def change_terminal(path: str):
        stdin = ItermProvider.__osa_script_set.format(path)
        ItermProvider.__set_process(str.encode(stdin))

    def get_image_file_number():
        stdin = ItermProvider.__osa_script_get.format()
        path = ItermProvider.__get_process(str.encode(stdin)).decode('utf-8')
        # The easiest check to see if we have a Pokemon as a background is checking for the presence of '/'
        if '/' in path:
            return path.split('/')[-1].split('.')[0]
        else:
            return 0

    def clear():
        stdin = ItermProvider.__osa_script_set.format("")
        ItermProvider.__set_process(str.encode(stdin))

    def __str__():
        return "iTerm 2"
