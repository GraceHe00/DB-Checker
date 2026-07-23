# classes
from halo import Halo # pyright: ignore[reportMissingTypeStubs]
from typing import List

def init() -> None:
    global version
    version = '1.9.0'
        
    global ext
    ext = {'SQL':'.sql','PYTHON':'.py','R':'.r'}

    global spinner
    spinner = Halo()

    # defined in config.ini file
    global host_url
    global workspace_path
    global client_code
    global client
    global check_ext
    global download
    global overwrite
    global export_path
    global create_file_structure
    global replace
    global one_file
    global open_file
    global check_similarity
    global levenshtein
    global check_signatures
    global scrap_contains
    global scrap_startswith
    global scrap_endswith

host_url: str 
workspace_path: str
client_code: str
client: str
check_ext: bool
download: bool
overwrite: bool
export_path: str
create_file_structure: bool
replace: bool
one_file: bool
open_file: bool
check_similarity: bool
levenshtein: bool
check_signatures: bool
scrap_contains: List[str]
scrap_startswith: List[str]
scrap_endswith: List[str]