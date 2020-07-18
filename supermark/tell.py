from colorama import init, Fore, Style
init(autoreset=True)

LOG_VERBOSE = True

def tell(message, level='info', chunk=None):
    # Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
    # Style: DIM, NORMAL, BRIGHT, RESET_ALL
    if chunk is not None:
        message = '{} line {}: {}'.format(chunk.path, chunk.start_line_number, message)
    if level == 'info':
        if LOG_VERBOSE:
            print(Fore.GREEN + Style.BRIGHT +  ' - ' + Style.RESET_ALL + message)
    elif level == 'warn':
        print(Fore.YELLOW + Style.BRIGHT +  ' - ' + Style.RESET_ALL + message)
    else:
        print(Fore.RED + Style.BRIGHT +  ' - ' + Style.NORMAL + message)