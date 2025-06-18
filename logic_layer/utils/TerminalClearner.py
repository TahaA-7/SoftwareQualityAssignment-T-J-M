import os, sys

class TerminalCleaner():
    CLEAR = ""
    @classmethod
    def __detect_platform(cls):
        if sys.platform in ('linux', 'unix', 'macos', 'darwin'):
            CLEAR = 'clear'
        elif sys.platform in ('windows'):
            CLEAR = 'cls'

    @classmethod
    def clear_terminal(cls):
        cls.__detect_platform()
        os.system(cls.CLEAR)
