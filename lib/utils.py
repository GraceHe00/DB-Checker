from datetime import datetime
import sys

def log(exception: str, message: str = str(datetime.now())) -> bool:
    """
    Writes errors to a log

    Args:
        exception (str):    Excpetion message
        message (str):      Any additional information to write (default: current time)
    """
    try:
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n{exception}\n\n')
            file.close()
        return True
    except: return False


def close_program(message: str = '', pause: bool = False) -> None:
    """
    Prints message and closes program (can toggle user pause)

    Args:
        message (str):  Message to display before closing (default: '')
        pause (bool):   Prompt user pause before closing (default: True)
    """
    print(f'\n{message}')
    if pause: input('Press [ENTER] to close...')
    sys.exit()