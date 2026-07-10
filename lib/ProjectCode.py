# libraries
import glob
from . import settings
import subprocess
import zipfile

# classes
from pathlib import Path
from .Notebook import Notebook
from typing import List

# methods
from .utils import scrap

class ProjectCode:
    def __init__(self, code: str):
        """
        This represent a project.

        Args:
            code (str):                     This is the full project code.
            client_code (str):              This is the client code of this project.
            s_drive (str):                  This is the network S: drive path to the project folder.
            p_drive (str):                  This is the network P: drive path to the project folder. This may not exist.
            notebooks (List[Notebook]):     This is a list of all Databricks notebooks associated with this project code.
            exist (bool):                   This is whether the project exists and is not archived.

            name (str):                     This is the name of the project code (if it exists).
            supports (dict[str,List[str]]): This is a dictionary of support and its code support files.
        """
        self.code = code

        self.client_code = settings.client_code
        self.s_drive = f'S:/Client_Projects/{self.client_code}/{self.code}/5-Support_Files'
        self.p_drive = f'P:/PHI/{settings.client}/{self.code}/5-Support_Files'
        self.notebooks: List[Notebook] = []
        self.exist = Path(f'S:/Client_Projects/{self.client_code}/{self.code}').exists()

        self.name: str | None = None
        self.supports: dict[str,List[str]] = {}
    
    def __str__(self) -> str:
        self.get_name()
        if self.name is None: return self.code
        else: return self.name
    
    def get_files(self) -> List[Notebook]:
        """
        Get all non-scrap files in a workspace for a given workspace diretory and add to self.notebooks list
        """
        main_path = f'{settings.workspace_path}{self.code}'
        dirs = [main_path]
        while len(dirs) != 0:
            if scrap(dirs[0]):
                dirs.remove(dirs[0])
                continue
            settings.spinner.start(text=f'Indexing {dirs[0]}...') # pyright: ignore[reportUnknownMemberType]
            for r in subprocess.run(['databricks','workspace','list',dirs[0]],capture_output=True,text=True).stdout.splitlines()[1:]:
                try:
                    if r.split()[1] == 'DIRECTORY': dirs.append(' '.join(r.split()[2:]))
                except: pass
                try: 
                    path = ' '.join(r.split()[3:])
                    subpath = path.replace(main_path,'')[1:]
                    if r.split()[1] == 'NOTEBOOK':
                        if scrap(subpath): continue
                        extension = settings.ext[r.split()[2]]
                        url = f'{settings.host_url}/editor/notebooks/{r.split()[0]}'
                        self.notebooks.append(Notebook(self.code,path,subpath,extension,url))
                except: pass
            settings.spinner.stop() # pyright: ignore[reportUnknownMemberType]
            dirs.remove(dirs[0])
        return self.notebooks
        
    
    def check_support(self, support: str) -> List[str]:
        """
        Return all SQL, Python, and R files from S drive and P drive (if exists) for a given support

        Args:
            support (str):  This is the name of the support folder.
        """
        try: return self.supports[support]
        except:
            settings.spinner.start(f'Indexing {support}...') # pyright: ignore[reportUnknownMemberType]
            m: List[str] = []
            for e in settings.ext.values():
                m += [f.replace('\\','/') for f in glob.glob(f'{self.s_drive}/{support}/**/*{e}', recursive=True)]
                zip_files = [f.replace('\\','/') for f in glob.glob(f'{self.s_drive}/{support}/**/*.zip', recursive=True)]
                for zip_file in zip_files:
                    with zipfile.ZipFile(zip_file, 'r') as zf:
                        m += [f'{zip_file}/{z.filename}' for z in zf.infolist() if z.filename.endswith(e)]
                        zf.close()
                if Path(self.p_drive).exists():
                    m += [f.replace('\\','/') for f in glob.glob(f'{self.p_drive}/{support}/**/*{e}', recursive=True)]
                    zip_files = [f.replace('\\','/') for f in glob.glob(f'{self.p_drive}/{support}/**/*.zip', recursive=True)]
                    for zip_file in zip_files:
                        with zipfile.ZipFile(zip_file, 'r') as zf:
                            m += [f'{zip_file}/{z.filename}' for z in zf.infolist() if z.filename.endswith(e)]
                            zf.close()
            self.supports[support] = m
            settings.spinner.stop() # pyright: ignore[reportUnknownMemberType]
            return m
    
    def get_name(self) -> None:
        """
        Define name of project code
        """
        if not self.exist: self.name = None
        try:
            n = [f.replace('\\','/').split('/')[-1].split('.')[0] for f in glob.glob(f'S:/Client_Projects/{self.client_code}/{self.code}/*.txt')]
            n.remove('DO NOT STORE FILES IN THIS DIRECTORY')
            self.name = n[0]
        except: pass