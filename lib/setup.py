import configparser
import os

from . import settings

def setup() -> None:
    """
    Set up the configuration for DB Checker
    """
    setup = False
    while not setup:
        config = configparser.ConfigParser()

        config['General'] = {
            'host_URL':'https://adb-7405618167364399.19.azuredatabricks.net',
            'scrap_indicators':'scrap,xx-,clone',
            'workspace_path':'/Workspace/Shared/ILM_Project_Codes/',
            'client_code': '0032ILM',
            'check_extensions':'False'
        }
        config['Scrap'] = {
            'contains':'scrap,clone',
            'startswith':'xx-,copy of',
            'endswith':'_tr,- copy',
            'show':'False'
        }
        config['Download'] = {
            'download':'False',
            'export_path':os.getcwd(),
            'create_file_structure':'True',
            'overwrite':'False',
        }
        config['Excel'] = {
            'one_file':'True',
            'open_file':'True'
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
        settings.overwrite = config.get('Download','overwrite')
        settings.one_file = config.getboolean('Excel','one_file')
        settings.open_file = config.getboolean('Excel','open_file')
        
        settings.scrap_contains = [c.strip().lower() for c in config.get('Scrap','contains').split(',')]
        settings.scrap_startswith = [c.strip().lower() for c in config.get('Scrap','startswith').split(',')]
        settings.scrap_endswith = [c.strip().lower() for c in config.get('Scrap','endswith').split(',')]
        settings.show_scrap = config.getboolean('Scrap','show')

        print('\nCONFIGURATION OPTIONS:')
        print(f'Checking extensions:\t{settings.check_ext}')
        print(f'Scrap indicators:\n\tContains:\t{", ".join(settings.scrap_contains)}\n\tStarts with:\t{", ".join(settings.scrap_startswith)}\n\tEnds with:\t{", ".join(settings.scrap_endswith)}')
        print(f'Save as one file:\t{settings.one_file}')
        print(f'Download missing:\t{settings.download}')
        if settings.download:
            print(f'Download path:\t\t{settings.export_path}')
            print(f'Create file structure:\t{settings.create_file_structure}')
            print(f'Overwrite:\t\t{settings.overwrite}')
        print('\nAre these configuration settings correct? [Y] Yes or [N]')
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