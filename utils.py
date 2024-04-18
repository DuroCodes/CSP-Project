import os
from typing import Callable


def clear_screen():
    "Uses `cls` on Windows and `clear` on Unix to clear the screen"
    os.system('cls' if os.name == 'nt' else 'clear')


def prompt(
    prompt: str,
    case_sensitive=False,
    parser: Callable[[str], bool] = lambda _: True,
    error_message="Invalid response, please try again.",
    retry=True,
    clear=True
) -> str:
    """
    Parses user input, if parser is True, the response is returned.

    Parameters:
        `prompt (str)`: The prompt to display to the user
        `case_sensitive (bool)`: Whether the input should be case sensitive or not
        `parser (Callable[[str], bool])`: A function that parses the user's input
        `error_message (str)`: The error message to display if the parser returns False
        `retry (bool)`: Whether to retry if the parser returns False
        `clear (bool)`: Whether to clear the screen before retrying
    """
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


class Colors:
    reset = '\033[0m'
    red = '\033[31m'
    blue = '\033[34m'

def color(text: str, color: str):
    return f"{color}{text}{Colors.reset}"
