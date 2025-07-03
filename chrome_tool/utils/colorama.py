from colorama import init, Back, Fore, Style


init()

def color_print(text: str, color: str=Fore.WHITE, bg: str=Back.BLACK, style: str=Style.NORMAL):
    print(style + color + bg + text + Style.RESET_ALL)
