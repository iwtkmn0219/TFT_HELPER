BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
VIOLET = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"

def font(text: str, color: str) -> str:
    if color == "black":
        return BLACK + text + RESET
    if color == "red":
        return RED + text + RESET
    elif color == "green":
        return GREEN + text + RESET
    elif color == "yellow":
        return YELLOW + text + RESET
    elif color == "blue":
        return BLUE + text + RESET
    elif color == "violet":
        return VIOLET + text + RESET
    elif color == "cyan":
        return CYAN + text + RESET
    elif color == "white":
        return WHITE + text + RESET