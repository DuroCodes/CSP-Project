import os
from typing import Callable


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt(prompt: str, case_sensitive=False, parser: Callable[[str], bool] = lambda _: True, error_message="Invalid response, please try again.", retry=True, clear=True):
    while True:
        response = input(prompt)
        if not case_sensitive:
            response = response.lower()
        if parser(response):
            return response
        if retry:
            if clear:
                clear_screen()
            print(error_message)
        else:
            return response


class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


def color(text: str, color: str):
    return f"{color}{text}{colors.reset}"
