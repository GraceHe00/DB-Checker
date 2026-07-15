# libraries
import os
from . import settings
import re
import subprocess

# classes
from typing import List
from zipfile import ZipFile

# methods
from .utils import scrap

class Notebook:
    def __init__(self, code: str, path: str, subpath: str, extension: str, url: str):
        """
        Represents a Databricks notebook

        Args:
            code (str):                 This is the project code associated with this notebook.
            path (str):                 This is the Databricks path from the Workspace of this notebook.
            subpath (str):              This is the Databricks path from the project code of this notebook.
            extension (str):            This is the associated extension of this notebook (likely either SQL or PY)
            url (str):                  This is the website link to the notebook on Databricks.

            source_path (str | None):   This is the directory path to the source file if it exists.
            zipped (bool | None):       This is whether the source file is in a zipped/compressed folder.
            downloaded (bool | None):   This is whether the source file has been downloaded by this program. If it is None, then it is not applicable because it was already saved to the network.
            qrm (bool | None):          This is whether this notebook has been reviewed.
            qrm_status (str):           This is a more granular breakdown of self.qrm, giving info on authors and reviewers.
        """
        self.code = code
        self.path = path
        self.subpath = subpath
        self.extension = extension
        self.url = url
        self.support = self.subpath.split('/')[0]
        self.name = self.subpath.split('/')[-1]
        self.scrap = scrap(self.name)
        
        self.source_path: str | None = None
        self.zipped: bool | None = None
        self.downloaded: bool | None = None
        self.qrm: bool | None = None
        self.qrm_status = 'Not reviewed'
    
    def __str__(self): return self.name
    
    def match_source_file(self, source_paths: List[str]) -> bool:
        """
        From a list of possible matching files, update self.source_file if names (and extensions) match

        Args:
            source_paths (List[str]):   This is the list of potential matching files' directory paths.
        """
        for s in source_paths:
            try:
                filename = s.split('/')[-1]
                file, extension = os.path.splitext(filename)
                if file == self.name and settings.check_ext and extension == self.extension:
                    self.source_path = s
                    self.zipped = '.zip' in self.source_path
                    return True
                elif file == self.name:
                    self.source_path = s
                    self.zipped = '.zip' in self.source_path
                    return True
                else: continue
            except: continue
        return False
    
    def download(self) -> str:
        """
        Download notebook
        """
        if settings.create_file_structure: export_dir = f'{settings.export_path}/{self.code}/5-Support_Files/{self.support}/Databricks_Programs'
        else: export_dir = f'{settings.export_path}'
        export_dir = export_dir.replace('\\','/')
        try:
            os.makedirs(export_dir,exist_ok=True)
            subprocess.run(['databricks','workspace','export-dir','--overwrite',self.path,f'{export_dir}/{self.name}'],capture_output=True,text=True)
            self.source_path = f'{export_dir}/{self.name}{self.extension}'
            self.zipped = False
            self.downloaded = True
            return self.source_path
        except:
            self.source_path = None
            self.downloaded = False
            return f'Error downloading {self.name} to {export_dir}'

    def get_lines(self, find: str, start: str = ':', end: str = '\n', ignore: str | None = None) -> List[str]:
        """
        Read a source file and attempt to return list of any text between two values

        Args:
            find (str):             string in a line that is trying to be found
            start (str):            return after this character (default: ':')
            end (str):              end after this character (default: '\n')
            ignore (str | None):    ignore a line if it contains this string, even if it is a match (default: None)
        """
        if self.source_path is None: return ['missing']
        matches: List[str] = []
        try:
            try:
                with open(self.source_path,mode='r',encoding='utf-8') as f:
                    matches = [line for line in f if find.lower() in line.lower()]
                    f.close()
            except:
                try:
                    if '.zip' in self.source_path:
                        z = self.source_path.split('.zip')
                        with ZipFile(z[0] + '.zip','r') as zd:
                            with zd.open(z[1][1:],'r') as zf:
                                content = zf.read().decode('utf-8').split('\n')
                                zf.close()
                        matches = [line for line in content if find.lower() in line.lower()]
                except: return ['zip']
            if ignore != None: matches = [m for m in matches if ignore.lower() in m.lower()]
            matches_trimmed = [m[m.find(start) + len(start):m.find(end)] for m in matches]
            matches_no_html = [re.sub(r'<(.*?)>',' ',m) for m in matches_trimmed]
            matches_no_special = [re.sub(r'[^a-zA-Z\s]','',m).strip() for m in matches_no_html]
            return [n for n in matches_no_special if n != '']
        except: return ['failed']

    def get_names(self) -> None:
        """
        Define authors and reviewers for a given source file
        """
        self.initial_author = self.get_lines('author')
        self.initial_checker = self.get_lines('checker')
        self.addl_auth = self.get_lines('author', ignore='initial')
        self.addl_check = self.get_lines('checker', ignore='initial')

        if len(self.addl_auth) + len(self.addl_check) == 0: self.subsequent = False
        else: self.subsequent = True
    
    def check_qrm(self) -> str:
        """
        Verify QRM status by checking authors and reviewers
        """
        self.get_names()
        if self.initial_author == ['failed']: self.qrm_status = 'Failed to read file'
        elif self.initial_author == ['zip']: self.qrm_status = 'Cannot read compressed file'
        elif self.initial_author == ['missing']:
            self.qrm_status = 'File not downloaded'
            self.qrm = False
        elif len(self.initial_author) == 0:
            self.qrm_status = 'No author'
            self.qrm = False
        elif len(self.initial_checker) == 0:
            self.qrm_status = f'No checker, last author: {self.initial_author[0]}'
            self.qrm = False
        elif self.subsequent and len(self.addl_auth) > len(self.addl_check):
            self.qrm_status = f'No subsequent checker, last subsequent author: {self.addl_auth[-1]}'
            self.qrm = False
        else:
            a = self.initial_author + self.addl_auth
            c = self.initial_checker + self.addl_check
            self.qrm = True
            self.qrm_status = f'OK. Last author & checker: {a[-1]} & {c[-1]}'
        return self.qrm_status
