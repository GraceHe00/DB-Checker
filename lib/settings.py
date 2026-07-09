def init() -> None:
    global version
    with open('ReadMe.md','r') as f:
        version = f.read()[10:15]
    f.close()
        
    global ext
    ext = {'SQL':'.sql','PYTHON':'.py','R':'.r'}

    # initialized in config.ini file
    global host_url
    global workspace_path
    global client_code
    global client
    global check_ext
    global download
    global export_path
    global create_file_structure
    global overwrite
    global one_file
    global open_file
    global scrap_contains
    global scrap_startswith
    global scrap_endswith
    global show_scrap