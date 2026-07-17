print('Initializing libraries... Please wait.', end='\r')

#%% IMPORT
# libraries
import lib.databricksUtils as db
import openpyxl
import os
import lib.settings as settings
import lib.setup as setup
import lib.utils as utils
import lib.xlsUtils as xl

# classes
from datetime import datetime
from typing import List
from pathlib import Path
from lib.ProjectCode import ProjectCode

#%% INITIALIZATION
# define start
start_time = datetime.now()
time_signature = start_time.strftime("%Y%m%d%H%M%S")
settings.init()

# print version
print(f'DB Checker                            ')
print(f'v{settings.version}')

setup.check_version('GraceHe00','DB-Checker')
setup.setup_config()

# Databricks CLI verification
cli_version = db.version()
if cli_version is None: utils.close_program('Databricks CLI not installed!\nPlease see ReadMe for more information to set up Databricks CLI.')

host_url = db.host_info()
if host_url is None: utils.close_program(f'Databricks profile is not set up!\nconfig.ini:\t{settings.host_url}\nPlease see ReadMe for more information to set up Databricks CLI.')
elif host_url != settings.host_url: utils.close_program(f'Databricks profile does not match config.ini!\nconfig.ini:\t{settings.host_url}\nProfile:\t{host_url}\nPlease verify Databricks profile or config.ini to re-run.')
else: print(f'{cli_version}{host_url}\n')

#%% START
# get project codes
project_codes: List[ProjectCode] = []
p: str | None = None
print('Enter FULL project codes to check. (Press [ENTER] between each entry. Leave blank and press [ENTER] to continue.)')
while p != '' or len(project_codes) == 0:
    p = input('>').upper().strip()
    if p != '': project_codes.append(ProjectCode(p))
project_codes = sorted([p for p in project_codes],key=lambda x: x.code)
print(f'Checking {[p.code for p in project_codes]}\n')

wb: openpyxl.Workbook | None = None

#%% ITERATE
for project in project_codes:
    if project.exist:
        # print project name (or code)
        print(f'\n{project}')

        # get all Databricks notebooks
        project.get_files()
            
        if len(project.notebooks) > 0:
            # sort notebook by support and name
            project.notebooks = sorted(project.notebooks, key=lambda x: (x.support, x.name))
            
            # check network drives
            for n in project.notebooks:
                print(f'{project.code.split("-")[-1]}-{n.subpath.replace("-",": ",1)}')
                n.match_source_file(project.check_support(n.support))
                if n.source_path is None and settings.download:
                    if settings.create_file_structure: export_path = f'{settings.export_path}/{project.code}/5-Support_Files/{n.support}/Databricks_Programs'
                    else: export_path = f'{settings.export_path}'
                    n.download(export_path.replace('\\','/'))
                n.check_qrm(check_similarity=settings.check_similarity, check_signatures=settings.check_signatures)
                print(f'\tPath:\t{n.source_path}')        
                if settings.levenshtein and n.similarity is not None: print(f'\tMatch:\t{round(n.similarity * 100, 2)}%')
                elif settings.check_similarity and n.similarity is not None: print(f'\tMatch:\t{bool(n.similarity)}')
                if settings.check_signatures: print(f'\tQRM:\t{n.signatures}')
            
            # write data to workbook
            if wb is None: wb = xl.create_workbook()
            wb.create_sheet(project.code)
            ws = wb[project.code]
            xl.write_headers(ws)
            xl.write_data(ws, project.notebooks)

            # format and save workbook if doing multiple files
            if not settings.one_file:
                xl.fit_columns(wb)
                xlsx_file = f'DB_Check_{project.code}_{time_signature}.xlsx'
                xl.save(wb, xlsx_file)
                wb = None
            
            # update ReadMe for downloads
            if settings.download and settings.create_file_structure:
                if Path(f'{settings.export_path}/{project.code}').exists():
                    with open(f'{settings.export_path}/{project.code}/ReadMe.txt','a') as readme:
                        xlsx_path = os.getcwd()
                        if settings.one_file: xlsx_path += f'\\DB_Check_{time_signature}.xlsx'
                        else: xlsx_path = f'\\DB_Check_{project.code}_{time_signature}.xlsx'
                        readme.write(f'DB_Checker {settings.version} ran by {os.environ.get("USERNAME")} at {start_time.strftime("%H:%M")} on {start_time.strftime("%B %d, %Y")}.\nSee {xlsx_path} for more information.\n\n')
                    readme.close()

        else:
            # no notebooks found
            print(f'There are no Databricks notebooks without {", ".join(settings.scrap_contains + settings.scrap_startswith + settings.scrap_endswith)}.')
            continue
    else:
        # no project code found
        print(f'\nNo project with code {project.code} found.')
        continue

# format and save workbook if doing a singular file and open if settings.open_file
if wb is not None:
    xl.fit_columns(wb)
    xlsx_file = f'DB_Check_{time_signature}.xlsx'
    xl.save(wb, xlsx_file)
    if settings.open_file:
        print(f'\nOpening {xlsx_file}...')
        os.startfile(xlsx_file)

#%% END
utils.close_program(f'Runtime:\t{datetime.now() - start_time}')