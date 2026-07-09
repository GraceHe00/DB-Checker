# classes
from typing import List

def init() -> None:
    global version
    with open('ReadMe.md','r') as f:
        version = f.read()[10:15]
    f.close()
        
    global ext
    ext = {'SQL':'.sql','PYTHON':'.py','R':'.r'}

    # defined in config.ini file
    global host_url
    global workspace_path
    global client_code
    global client
    global check_ext
    global download
    global export_path
    global create_file_structure
    global one_file
    global open_file
    global scrap_contains
    global scrap_startswith
    global scrap_endswith

host_url: str 
workspace_path: str
client_code: str
client: str
check_ext: bool
download: bool
export_path: str
create_file_structure: str
one_file: bool
open_file: bool
scrap_contains: List[str]
scrap_startswith: List[str]
scrap_endswith: List[str]