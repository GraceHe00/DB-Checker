# libraries
import configparser
import os
import requests
from . import settings

def check_version(owner: str, repo: str, timeout: int = 10) -> None:
    """
    Checks if the version running is the latest version on GitHub

    Args:
        owner (str):    Username of GitHub repository owner
        repo (str):     Name of GitHub repository
        timeout (int):  Seconds until request timeout (default = 10)
    """
    try:
        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/releases/latest', timeout=timeout)
        response.raise_for_status()
        data = response.json()
        latest_version = data.get('tag_name').replace('v','')
        if latest_version > settings.version:
            print(f'WARNING! This version is out of date.\nPlease go to:\nhttps://github.com/{owner}/{repo}/releases/latest\nfor the latest release.')
            input('Press [ENTER] to continue anyways...')
    except: pass

def setup_config() -> None:
    """
    Set up the configuration for DB Checker
    """
    setup = False
    while not setup:

        config = configparser.ConfigParser()
        config['General'] = {
            'host_URL':'https://adb-7405618167364399.19.azuredatabricks.net',
            'workspace_path':'/Workspace/Shared/ILM_Project_Codes/',
            'client_code': '0032ILM',
            'check_extensions':'False'
        }
        config['Scrap'] = {
            'contains':'scrap,clone',
            'startswith':'xx-,copy of',
            'endswith':'_tr,- copy'
        }
        config['Download'] = {
            'download':'False',
            'export_path':os.getcwd(),
            'create_file_structure':'True'
        }
        config['Excel'] = {
            'one_file':'True',
            'open_file':'True'
        }
        config['QRM'] = {
            'check_similarity':'False',
            'threshold':'100',
            'check_signatures':'True'
        }

        if not os.path.isfile('config.ini'):
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        config.read('config.ini')

        settings.host_url = config.get('General','host_URL')
        settings.workspace_path = config.get('General','workspace_path')
        settings.client_code = config.get('General','client_code')
        settings.client = settings.client_code[4:]
        settings.check_ext = config.getboolean('General','check_extensions')
        settings.download = config.getboolean('Download','download')
        settings.export_path = config.get('Download','export_path')
        settings.create_file_structure = config.getboolean('Download','create_file_structure')
        settings.one_file = config.getboolean('Excel','one_file')
        settings.open_file = config.getboolean('Excel','open_file')
        settings.check_similarity = config.getboolean('QRM','check_similarity')
        settings.threshold = float(int(config.get('QRM','threshold')) / 100)
        settings.check_signatures = config.getboolean('QRM','check_signatures')
        settings.scrap_contains = [c.strip().lower() for c in config.get('Scrap','contains').split(',') if c.strip() != '']
        settings.scrap_startswith = [c.strip().lower() for c in config.get('Scrap','startswith').split(',') if c.strip() != '']
        settings.scrap_endswith = [c.strip().lower() for c in config.get('Scrap','endswith').split(',') if c.strip() != '']

        print('\nCONFIGURATION OPTIONS:')
        print(f'Checking extensions:\t{settings.check_ext}')
        print(f'Scrap indicators:\n\tContains:\t{", ".join(settings.scrap_contains)}\n\tStarts with:\t{", ".join(settings.scrap_startswith)}\n\tEnds with:\t{", ".join(settings.scrap_endswith)}')
        print(f'Save as one file:\t{settings.one_file}')
        print(f'Download missing:\t{settings.download}')
        if settings.download:
            print(f'Download path:\t\t{settings.export_path}')
            print(f'Create file structure:\t{settings.create_file_structure}')
        print(f'Check differences:\t{settings.check_similarity}')
        if settings.check_similarity: print(f'Similarity threshold:\t{settings.threshold}')
        print(f'Check signatures:\t{settings.check_signatures}')
        print('\nAre these configuration settings correct? [Y] Yes or [N] No')
        valid_answer = False
        while not valid_answer:
            inp = input('>').upper()
            if inp == 'Y':
                valid_answer = True
                setup = True
            elif inp == 'N':
                valid_answer = True
                print(f'Please update {os.getcwd()}\\config.ini.')
                input('Press [ENTER] to continue...')
            else:
                print(f'Expecting Y or N, got {inp} instead')
                continue
    print()