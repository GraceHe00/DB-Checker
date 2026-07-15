# libraries
import os
from . import settings
import re
import subprocess

# classes
from typing import List
from zipfile import ZipFile

# methods
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
from .utils import scrap

class Notebook:
    def __init__(self, code: str, path: str, subpath: str, extension: str, url: str):
        """
        Represents a Databricks notebook

        Args:
            code (str):                  This is the project code associated with this notebook.
            path (str):                  This is the Databricks path from the Workspace of this notebook.
            subpath (str):               This is the Databricks path from the project code of this notebook.
            extension (str):             This is the associated extension of this notebook (likely either SQL or PY)
            url (str):                   This is the website link to the notebook on Databricks.

            source_path (str | None):    This is the directory path to the source file if it exists.
            zipped (bool | None):        This is whether the source file is in a zipped/compressed folder.
            downloaded (bool | None):    This is whether the source file has been downloaded by this program. If it is None, then it is not applicable because it was already saved to the network.
            local (str | None):          This is the content of the local source file.
            initial_author (List[str]):  This is a list of the initial authors.
            initial_checker (List[str]): This is a list of the initial checkers.
            addl_auth (List[str]):       This is a list of the subsequent authors.
            addl_check (List[str]):      This is a list of the subsequent checkers.
            signatures (str):            This is the most recent author and checker.
            similarity (float | None):   This is the similarity normalized Damerau-Levenshtein distance between the code in the workspace and the source file on the network.
            qrm (bool | None):           This is whether this notebook has been reviewed.
            
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
        self.local: str | None = None
        self.initial_author: List[str] = []
        self.initial_checker: List[str] = []
        self.addl_auth: List[str] = []
        self.addl_check: List[str] = []
        self.signatures = 'Not reviewed'
        self.similarity: float | None = None
        self.qrm: bool | None = None
    
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
    
    def __get_local__(self) -> None:
        """
        Read local source file
        """
        if self.source_path is None: return None
        if self.zipped:
            try:
                z = self.source_path.split('.zip')
                with ZipFile(z[0] + '.zip','r') as zd:
                    with zd.open(z[1][1:],'r') as zf:
                        self.local = zf.read().decode('utf-8')
                        zf.close()
            except: return None
        else:
            try:
                with open(self.source_path,mode='r',encoding='utf-8') as f:
                    self.local = f.read()
                    f.close()
            except: return None

    def __parse_lines__(self, find: str, start: str | None = ':', end: str | None = '\n', ignore: str | None = None) -> List[str]:
        """
        Read source file and attempt to return list of any text between two values

        Args:
            find (str):             string in a line that is trying to be found
            start (str | None):     return after this character (default: ':')
            end (str | None):       end after this character (default: '\n')
            ignore (str | None):    ignore a line if it contains this string, even if it is a match (default: None)
        """
        if self.local is None: return []
        content = self.local.split('\n')
        matches = [c for c in content if find.lower() in c.lower()]
        if ignore != None: matches = [m for m in matches if ignore.lower() not in m.lower()]
        matches_trimmed: List[str] = []
        for m in matches:
            if start is None or m.find(start) == -1: a = 0
            else: a = m.find(start) + len(start)
            if end is None or m.find(end) == -1: b = len(m)
            else: b = m.find(end)
            matches_trimmed.append(m[a:b])
        matches_no_html = [re.sub(r'<(.*?)>',' ',m) for m in matches_trimmed]
        matches_no_special = [re.sub(r'[^a-zA-Z\s]','',m).strip() for m in matches_no_html]
        return [n for n in matches_no_special if n != '']

    def __check_signatures__(self) -> None:
        """
        Define authors and reviewers for a given source file
        """
        if self.local is None: return None

        settings.spinner.start(f'Checking {self.name} for signatures...') # pyright: ignore[reportUnknownMemberType]

        self.initial_author = self.__parse_lines__('author')
        self.initial_checker = self.__parse_lines__('checker')
        self.addl_auth = self.__parse_lines__('author', ignore='initial')
        self.addl_check = self.__parse_lines__('checker', ignore='initial')

        subsequent = len(self.addl_auth) + len(self.addl_check) != 0

        if len(self.initial_author) == 0: self.signatures = 'No author'
        elif len(self.initial_checker) == 0: self.signatures = f'No checker, last author: {self.initial_author[0]}'
        elif subsequent and len(self.addl_auth) > len(self.addl_check): self.signatures = f'No subsequent checker, last subsequent author: {self.addl_auth[-1]}'
        else:
            a = self.initial_author + self.addl_auth
            c = self.initial_checker + self.addl_check
            self.signatures = f'OK. Last author & checker: {a[-1]} & {c[-1]}'
        
        settings.spinner.stop()
    
    def __check_similarity__(self) -> None:
        """
        Get normalized similarity based on Damerau-Levenshtein distance
        """
        if self.local is None: return None
        try: origin = subprocess.run(['databricks','workspace','export',self.path], capture_output=True, text=True, encoding='utf-8').stdout
        except: return None
        settings.spinner.start(f'Comparing {self.name}...') # pyright: ignore[reportUnknownMemberType]
        local_nsp = re.sub(r'\s','',self.local)
        origin_nsp = re.sub(r'\s','',origin)
        if settings.levenshtein: self.similarity = 1 - normalized_damerau_levenshtein_distance(local_nsp, origin_nsp)
        else: self.similarity = int(local_nsp == origin_nsp)
        settings.spinner.stop()
    
    def check_qrm(self, check_similarity: bool = True, check_signatures: bool = True) -> bool | None:
        """
        Verify QRM status by checking authors and reviewers
        """
        if self.source_path is None: return None
        if check_similarity or check_signatures:
            settings.spinner.start(f'Reading {self.name}...') # pyright: ignore[reportUnknownMemberType]
            self.__get_local__()
            settings.spinner.stop()
            if self.local is None: return None
            if check_similarity:
                self.__check_similarity__()
                if (self.qrm or self.qrm is None)and self.similarity is not None:
                    if settings.levenshtein: self.qrm = self.similarity >= settings.threshold
                    else: self.qrm = bool(self.similarity)
            if check_signatures:
                self.__check_signatures__()
                if self.qrm or self.qrm is None: self.qrm = self.signatures[:2] == 'OK'
            return self.qrm
        else: return None