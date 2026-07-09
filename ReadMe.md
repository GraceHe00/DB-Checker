> Version 1.7.3
# DB Checker
Running 'DB_checker.exe' will compare Databricks to SQL, PY, and R files saved on the S: and P: drives and will output an *.xlsx file. This assumes that support folder names are the same in Databricks and the S:/P: drive. It can check through zip folders. This program takes significantly longer larger projects or projects that use a lot of zip folders. This program can run in the background while doing other work. To change settings, use config.ini.<br />
If you experience errors, please see the Common Issues section below. If the issue persists, please submit an [issue](https://github.com/GraceHe00/DB-Checker/issues) or [message me](https://teams.microsoft.com/l/chat/0/0?users=grace.hedges@milliman.com). <br />
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
* Additional resources (instructions for Azure are the same):
  * [Install or Update the Databricks CLI | Databricks on AWS](https://docs.databricks.com/aws/en/dev-tools/cli/install)
  * [Authentication for the Databricks CLI | Databricks on AWS](https://docs.databricks.com/aws/en/dev-tools/cli/authentication)
  * [Databricks REST API reference](https://docs.databricks.com/api/workspace/introduction)

# Configuration in config.ini
This file will be automatically created with the default values on the first run of DB_checker.exe if it does not exist. If any variables are omitted or removed from the configuration file, the default values will be used for fallback. (_Default values in italics_)
## General
* `host_url`: This is you Databricks host URL; typically the first part of any DB notebook URL and was used to authenticate Databricks CLI (_https://adb-7405618167364399.19.azuredatabricks.net_)
* `workspace_path`: This is the Databricks workspace path that contains the project folders (_/Workspace/Shared/ILM_Project_Codes/_)
* `client_code`: This is the client code (_0032ILM_)
* `check_extensions`: This is the toggle to force matching extensions (most of the time notebooks are downloaded as SQL but DB might recognize the notebook as a PY file) (_False_)
## Scrap
* `contains`: Any notebook title or directory name containing any value in this comma-delimited list of terms or phases will be skipped (_scrap,clone_)
* `startswith`: Any notebook title or directory name starting with any value in this comma-delimited list of terms or phrases will be skipped (_xx-,copy of_)
* `endswith`: Any notebook title or directory name ending with any value in this comma-delimited list of terms or phrases will be skipped (_\_tr,- copy_)
* `show`: not implemented (_False_)
## Download
* `download`: This is the toggle to download notebooks flagged as missing (_False_)
* `export_path`: This is the export location (_current working directory_)
* `create_file_structure`: If true, files will export to a subfolder with a file structure similar to the S drive ; else, files will export to export_path (_True_)
* `overwrite`: This is a toggle to overwrite existing files in the export location (_False_)
## Excel
* `one_file`: This is a toggle to save log as one file for all project codes. If false, a new Excel workbook will be generated for each project code (_True_)
* `open_file`: This is a toggle to open the Excel workbook after the program is done running (_True_)
  * Note: This only works if one_file is selected.

# Common Issues
- Databricks CLI not configured correctly.
  - Verify that your Databricks profile is configured by typing `databricks auth describe` in Windows PowerShell.
- Files being flagged as unable to read.
  - Most likely due to the title of the file containing a . or other character. This is currently being fixed.
- Files/folders are being skipped/flagged as scrap when they shouldn't be.
  - Verify that those files/folders in question do not contain a scrap indicator as a substring.
- The program stopped.
  - Try pressing the down arrow key a few times.
