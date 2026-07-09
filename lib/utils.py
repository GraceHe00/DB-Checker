# libraries
import re
from . import settings
import sys

# classes
from datetime import datetime

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

def scrap(name: str) -> bool:
    """
    Check if a name contains a scrap indicator

    Args:
        name (str): name of the file to check if it is scrap
    """
    for s in settings.scrap_contains:
        if re.search(name.lower(), s): return True
        else: continue
    for s in settings.scrap_startswith:
        if name.lower().startswith(s): return True
        else: continue
    for s in settings.scrap_endswith:
        if name.lower().endswith(s): return True
        else: continue
    return False