# About
Running 'DB_checker.exe' will compare Databricks to SQL, PY, and R files saved on the S: and P: drives and will output an *.xlsx file. This assumes that support folder names are the same in Databricks and the S:/P: drive. It can check through zip folders. This program takes significantly longer larger projects or projects that use a lot of zip folders. This program can run in the background while doing other work. To change settings, use config.ini.<br />
_This program cannot verify the QRM status of files in zip folders._

# Databricks CLI Configuration
1. open Windows PowerShell
2. run `winget search databricks`
2. accept the Miscrosoft TOS if prompted
4. run `winget install Databricks.DatabricksCLI`
5. exit Windows PowerShell
6. open Windows PowerShell
7. run `databricks auth login --host https://adb-7405618167364399.19.azuredatabricks.net/`
   - This is for the [ws-databricks-indy-indianapolis-centralus-213 workspace](https://adb-7405618167364399.19.azuredatabricks.net/); for other workspaces, use their host url.
9. name the Databricks profile or press [ENTER] to skip
10. authenticate your Databricks account in the browser
* Additional resource: [Install or Update the Databricks CLI | Databricks on AWS](https://docs.databricks.com/aws/en/dev-tools/cli/install)
  * Instructions for Azure are the same.
 
# Files Included
## config.ini
This file will be automatically created with the default values on the first run of DB_checker.exe if it does not exist. If any variables are omitted or removed from the configuration file, the default values will be used for fallback. (_Default values in italics_)
### General
* `host_url`: This is you Databricks host URL; typically the first part of any DB notebook URL and was used to authenticate Databricks CLI (_https://adb-7405618167364399.19.azuredatabricks.net_)
* `scrap-indicators`: This is a comma-delimited list of terms or phrases to ignore; any file OR folder that contains that text will be skipped when parsing Databricks files/folders; not case-sensitive (_scrap,xx-,clone_)
* `workspace_path`: This is the Databricks workspace path that contains the project folders (_/Workspace/Shared/ILM_Project_Codes/_)
* `client_code`: This is the client code (_0032ILM_)
* `check_extensions`: This is the toggle to force matching extensions (most of the time notebooks are downloaded as SQL but DB might recognize the notebook as a PY file) (_False_)
### Download
* `download`: This is the toggle to download notebooks flagged as missing (_False_)
* `export_path`: This is the export location (_current working directory_)
* `create_file_structure`: If true, files will export to {export_path}\{project code}\{5-Support_Files}\{Support Folder}\{Databricks Programs}; else, files will export to export_path (_True_)
* `overwrite`: This is a toggle to overwrite existing files in the export location (_False_)

## main.py
This is the logic used to build the *.exe file.

## exe_config.json
This is used to create the *.exe file for [autopytoexe](https://pypi.org/project/auto-py-to-exe/). 'main.py' is the logic used to build the *.exe file based on values in 'exe_config.json.'