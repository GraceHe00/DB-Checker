# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 10:45:49 2026

@author: Grace.Hedges
"""
print('Initializing libraries... Please wait.')

#%%libraries
import os
import configparser
import subprocess
import sys
from pathlib import Path
import glob
import zipfile
import openpyxl
from datetime import datetime

#%%init
ext = {'SQL':'.sql','PYTHON':'.py','R':'.r'}

#%%Close programs
def close_program(reason='') -> None:
    """
    Offer prompt and close program
    """
    print(f'{reason}\nThis program will now close.')
    os.system('pause')
    sys.exit()

#%%Verify Databricks CLI is installed
try: print(subprocess.run(['databricks','-v'],capture_output=True,text=True).stdout)
except: close_program('Databricks CLI not installed!\nPlease see ReadMe for more information to set up Databricks CLI.')

#%%config
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
        'one-file':'True'
    }

    if not os.path.isfile('config.ini'):
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    config.read('config.ini')
    host_url = config.get('General','host_URL')
    workspace_path = config.get('General','workspace_path')
    client_code = config.get('General','client_code')
    client = client_code[4:]
    check_ext = config.getboolean('General','check_extensions')
    download = config.getboolean('Download','download')
    export_path = config.get('Download','export_path')
    create_file_structure = config.getboolean('Download','create_file_structure')
    overwrite = config.get('Download','overwrite')
    one_file = config.getboolean('Excel','bulk')
    
    scrap_contains = [c.strip().lower() for c in config.get('Scrap','contains').split(',')]
    scrap_startswith = [c.strip().lower() for c in config.get('Scrap','startswith').split(',')]
    scrap_endswith = [c.strip().lower() for c in config.get('Scrap','endswith').split(',')]
    show_scrap = config.getboolean('Scrap','show')

    print('\nConfiguration options:')
    print(f'Checking extensions:\t{check_ext}')
    print(f'Scrap indicators:\n\tContains:\t{", ".join(scrap_contains)}\n\tStarts with:\t{", ".join(scrap_startswith)}\n\tEnds with:\t{", ".join(scrap_endswith)}')
    print(f'Download missing:\t{download}')
    if download:
        print(f'Download path:\t\t{export_path}')
        print(f'Create file structure:\t{create_file_structure}')
        print(f'Overwrite:\t\t{overwrite}')
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
            os.system('pause')
        else:
            print(f'Expecting Y or N, got {inp} instead')
            continue
#%%Scrap
def scrap(name: str) -> bool:
    """
    Check if a name contains a scrap indicator
    """
    for s in scrap_contains:
        if s in name.lower(): return True
        else: continue
    for s in scrap_startswith:
        if name.startswith(s): return True
        else: continue
    for s in scrap_endswith:
        if name.endswith(s): return True
        else: continue
    return False

#%%Project Code
class projectCode:
    def __init__(self,code):
        self.code = code
        self.s_drive = f'S:/Client_Projects/{client_code}/{self.code}/5-Support_Files'
        self.p_drive = f'P:/PHI/{client}/{self.code}/5-Support_Files'
        self.notebooks = []
        self.exist = Path(f'S:/Client_Projects/{client_code}/{self.code}').exists()
    
    def __str__(self):
        return self.code
    
    def get_files(self,directory: str) -> None:
        """
        Get all non-scrap files in a workspace for a given workspace diretory and add to self.notebooks list
        """
        for r in subprocess.run(['databricks','workspace','list',directory],capture_output=True,text=True).stdout.splitlines()[1:]:
            if r.split()[1] == 'NOTEBOOK':
                path = ' '.join(r.split()[3:])
                subpath = path.replace(main_path,'')[1:]
                extension = ext[r.split()[2]]
                url = f'{host_url}/editor/notebooks/{r.split()[0]}'
                if not scrap(path): self.notebooks.append(Notebook(self.code,path,subpath,extension,url))
            if r.split()[1] == 'DIRECTORY':
                name = ' '.join(r.split()[2:])
                if not scrap(name): dirs.append(name)
    
    def check_support(self,support) -> list:
        """
        Return all SQL, Python, and R files from S drive and P drive (if exists) for a given support
        """
        m = []
        for e in ext.values():
            m += [f.replace('\\','/') for f in glob.glob(f'{self.s_drive}/{support}/**/*{e}', recursive=True)]
            zip_files = [f.replace('\\','/') for f in glob.glob(f'{self.s_drive}/{support}/**/*.zip', recursive=True)]
            for zip_file in zip_files: m += [f'{zip_file}/{z.filename}' for z in zipfile.ZipFile(zip_file, 'r').infolist() if z.filename.endswith(e)]
            if Path(self.p_drive).exists():
                m += [f.replace('\\','/') for f in glob.glob(f'{self.p_drive}/{support}/**/*{e}', recursive=True)]
                zip_files = [f.replace('\\','/') for f in glob.glob(f'{self.p_drive}/{support}/**/*.zip', recursive=True)]
                for zip_file in zip_files: m += [f'{zip_file}/{z.filename}' for z in zipfile.ZipFile(zip_file, 'r').infolist() if z.filename.endswith(e)]
        return m
    
    def get_name(self) -> None:
        try:
            if self.exist:
                n = [f.replace('\\','/').split('/')[-1].split('.')[0] for f in glob.glob(f'S:/Client_Projects/{client_code}/{self.code}/*.txt')]
                n.remove('DO NOT STORE FILES IN THIS DIRECTORY')
                self.name = n[0]
            else: self.name = None
        except:
            self.name = None


#%%Notebook
class Notebook:
    def __init__(self,code,path,subpath,extension,url):
        self.code = code
        self.path = path
        self.subpath = subpath
        self.extension = extension
        self.url = url
        self.support = self.subpath.split('/')[0]
        self.name = self.subpath.split('/')[-1]
        self.scrap = scrap(self.name)
        
        self.source_path = 'MISSING'
        self.downloaded = False
        self.qrm = False
        self.qrm_status = 'Not reviewed'
    
    def __str__(self): return self.name
    
    def match_source_file(self,source_paths: list) -> bool:
        """
        From a list of possible matching files, update self.source_file if names (and extensios) match
        """
        for s in source_paths:
            try:
                file = s.split('/')[-1].split('.')[0]
                extension = '.' + s.split('/')[-1].split('.')[1]
                if file == self.name and check_ext and extension == self.extension:
                    self.source_path = s
                    return True
                elif file == self.name:
                    self.source_path = s
                    return True
                else: continue
            except: continue
        return False
    
    def download_missing(self) -> None:
        """
        Download notebook
        """
        try:
            if create_file_structure: export_dir = f'{export_path}/{self.code}/5-Support_Files/{self.support}/Databricks_Programs'
            else: export_dir = f'{export_path}'
            export_dir = export_dir.replace('\\','/')
            os.makedirs(export_dir,exist_ok=True)
            subprocess.run(['databricks','workspace','export-dir',self.path,f'{export_dir}/{self.name}'],capture_output=True,text=True)
            self.source_path = f'{export_dir}/{self.name}{self.extension}'
            self.downloaded = True
        except: print(f'Error downloading {self.name} to {export_dir}')

    
    def get_lines(self, find: str, start=':', end='\n') -> list:
        """
        Read a source file and attempt to return list of any text between two values
        """
        try:
            with open(self.source_path,mode='r',encoding='utf-8') as f:
                matches = [line for line in f if find.lower() in line.lower()]
                return [n for n in [m[m.find(start) + len(start):m.find(end)].strip() for m in matches] if n != '']
            f.close()
        except:
            try:
                with open(self.source_path,mode='r',encoding='ascii') as f:
                    matches = [line for line in f if find.lower() in line.lower()]
                    return [n for n in [m[m.find(start) + len(start):m.find(end)].strip() for m in matches] if n != '']
                f.close()
            except: return ['failed']

    def get_names(self) -> None:
        """
        Define authors and reviewers for a given source file
        """
        self.initial_author = self.get_lines('initial author',start=':**')
        self.initial_checker = self.get_lines('initial checker name')
        self.addl_auth = self.get_lines('change author')
        self.addl_check = self.get_lines('name of checker')
        if len(self.addl_auth) + len(self.addl_check) == 0: self.subsequent = False
        else: self.subsequent = True
    
    def check_qrm(self) -> str:
        """
        Verify QRM status by checking authors and reviewers
        """
        self.get_names()
        if self.initial_author == ['failed']: self.qrm_status = 'Failed to read file'
        elif len(self.initial_author) == 0: self.qrm_status = 'No author'
        elif len(self.initial_checker) == 0: self.qrm_status = f'No checker, last author: {self.initial_author[0]}'
        elif self.subsequent and len(self.addl_auth) > len(self.addl_check): self.qrm_status = f'No subsequent checker, last subsequent author: {self.addl_auth[-1]}'
        else:
            a = self.initial_author + self.addl_auth
            c = self.initial_checker + self.addl_check
            self.qrm = True
            self.qrm_status = f'OK. Last author & checker: {a[-1]} & {c[-1]}'
        return self.qrm_status
  
#%%Verify Databricks CLI is configured
host_info = subprocess.run(['databricks','auth','describe'],capture_output=True,text=True).stdout
h = host_info.split()[1]
if h == 'to': close_program(f'Databricks profile is not set up!\nconfig.ini:\t{host_url}\nPlease see ReadMe for more information to set up Databricks CLI.')
elif h != host_url: close_program(f'Databricks profile does not match config.ini!\nconfig.ini:\t{host_url}\nProfile:\t{h}\nPlease verify Databricks profile or config.ini to re-run.')
else: print(host_info)

#%%Define project code
project_codes = []
p = None
print('Enter FULL project codes to check. (Press [ENTER] between each entry. Leave blank and press [ENTER] to continue.)')
while p != '' or len(project_codes) == 0:
    p = input('>').upper().strip()
    if p != '': project_codes.append(projectCode(p))
project_codes = sorted([p for p in project_codes],key=lambda x: x.code)
print(f'Checking {[p.code for p in project_codes]}')

#%%Make workbook
def create_audit(wb_xlsx) -> None:
    wb_xlsx.create_sheet('Audit')
    wb_xlsx.remove(wb_xlsx['Sheet'])
    ws_xlsx = wb_xlsx['Audit']
    ws_xlsx.cell(1,1,'Run By:')
    ws_xlsx.cell(1,2,str(os.environ.get('USERNAME')))
    ws_xlsx.cell(2,1,'Workspace path:')
    ws_xlsx.cell(2,2,workspace_path)
    ws_xlsx.cell(3,1,'Force same extension:')
    ws_xlsx.cell(3,2,str(check_ext))
    ws_xlsx.cell(4,1,'Scrap identifiers:')
    ws_xlsx.cell(4,2,', '.join(scrap_contains + scrap_startswith + scrap_endswith))

def format_xlcols(wb):
    for sheets in wb.worksheets:
        for col in sheets.columns:
            max_length = 0
            column = col[0].column_letter # Get the column name
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            sheets.column_dimensions[column].width = adjusted_width

if one_file:
    wb = openpyxl.Workbook()
    create_audit(wb)

#%%         
for p in project_codes:
    if p.exist:
        p.get_name()
        try: print(f'\n{p.name}')
        except: print(f'\n{p.code}')

        #Pull Databricks files
        main_path = f'{workspace_path}{p}'
        dirs = [main_path]
        while len(dirs) != 0:
            p.get_files(dirs[0])
            dirs.remove(dirs[0])
            
        if len(p.notebooks) > 0:
            # Sort notebooks
            p.notebooks = sorted(p.notebooks,key=lambda x: (x.support, x.name))
            
            # Checking network drives
            for n in p.notebooks:
                print(f'{p.code.split("-")[-1]}-{n.subpath.replace('-',': ',1)}')
                n.match_source_file(p.check_support(n.support))
                if n.source_path == 'MISSING' and download: n.match_source_file([n.download_missing()])
                n.check_qrm()
                print(f'\tPath:\t{n.source_path}\n\tQRM:\t{n.qrm_status}')        
            
            # Project code
            if not one_file:
                wb = openpyxl.Workbook()
                create_audit(wb)
            
            wb.create_sheet(p.code)
            ws = wb[p.code]
            
            ws.cell(1,1,'Support')
            ws.cell(1,2,'Notebook Name')
            ws.cell(1,3,'QRM Status')
            ws.cell(1,4,'Now downloaded')
            ws.cell(1,5,'Source File')
            ws.cell(1,6,'Notebook URL')
            
            for i in range(2,len(p.notebooks)+2):
                ws.cell(i,1,p.notebooks[i-2].support)
                ws.cell(i,2,p.notebooks[i-2].name)
                if p.notebooks[i-2].qrm: q = 'OK.'
                else: q = p.notebooks[i-2].qrm_status
                ws.cell(i,3,q)
                ws.cell(i,4,int(p.notebooks[i-2].downloaded))
                ws.cell(i,5,p.notebooks[i-2].source_path)
                url_cell = ws.cell(i,6,p.notebooks[i-2].subpath)
                url_cell.hyperlink = p.notebooks[i-2].url
                url_cell.font = openpyxl.styles.Font(color="0000FF", underline="single")
            
            if not one_file:
                format_xlcols(wb)
                xlsx_file = f'DB_Check_{p.code}_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
                wb.save(xlsx_file)
                print(f'Saved {xlsx_file}')

        else:
            print(f'There are no Databricks notebooks without {", ".join(scrap_contains + scrap_startswith + scrap_endswith)}.')
            continue
    else:
        print(f'\nNo project with code {p.code} found.')
        continue

#%%save wb
if one_file:
    format_xlcols(wb)
    xlsx_file = f'DB_Check_{datetime.now().strftime("%Y%m%d%H%M%S")}.xlsx'
    wb.save(xlsx_file)
    print(f'\nOpening {xlsx_file}...')
    os.startfile(xlsx_file)
#%% End
close_program()