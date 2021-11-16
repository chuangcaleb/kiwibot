# Global Chat
colors = {
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'grey': '\033[90m',
    'white': '\033[97m',
    'end': '\033[0m',
}


def green(message):
    return f"{colors['green']}{message}{colors['end']}"


def yellow(message):
    return f"{colors['yellow']}{message}{colors['end']}"


def red(message):
    return f"{colors['red']}{message}{colors['end']}"


def grey(message):
    return f"{colors['grey']}{message}{colors['end']}"


def white(message):
    return f"{colors['white']}{message}{colors['end']}"


def docbot_says(message):
    print()
    for string in message:
        print(green(f"[Doc] {string}"))


def user_says():
    print()
    return input("> ")