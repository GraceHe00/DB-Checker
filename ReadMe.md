# DB Checker
This program indexes the Databricks workspace and network drives to:
1. Identify any notebook not saved to the network,
2. Save code to the network proper structure if it is missing,
3. Verify that the notebook in the Databricks workspace and the source file on the network are the same by calculating the Damerau–Levenshtein distance,
4. Check for author and checker signatures, and
5. Export an Excel workbook with links to both workspace and network locations of notebooks and files alongside other QRM information.

This assumes that support folder names are the same in Databricks, the S:, and P: drive. Also, while this can check through files in compressed zip folders, it will take significantly longer. This program can be run in the background while doing other work. It is advisable to run in a remote desktop to avoid accidentally exiting the program.

In order to run this program, pleasse see the [latest release](https://github.com/GraceHe00/DB-Checker/releases/latest) and download the `DB Checker.exe`. This is entirely run in Python, so you may also clone their repo. This program requires that the Databricks CLI is set up ([directions here](https://github.com/GraceHe00/DB-Checker/blob/20260715/lib/assets/docs/DBCLI.md)).

Additional options may be changed in config.ini ([additional information here](https://github.com/GraceHe00/DB-Checker/blob/20260715/lib/assets/docs/config.md)).

If you experience errors, please see the __Common Issues__ section below. If the issue persists, please submit an [issue](https://github.com/GraceHe00/DB-Checker/issues).<br />

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
## Download
* `download`: This is the toggle to download notebooks flagged as missing (_False_)
* `export_path`: This is the export location (_current working directory_)
* `create_file_structure`: If true, files will export to a subfolder with a file structure similar to the S drive ; else, files will export to export_path (_True_)
## Excel
* `one_file`: This is a toggle to save log as one file for all project codes. If false, a new Excel workbook will be generated for each project code (_True_)
* `open_file`: This is a toggle to open the Excel workbook after the program is done running (_True_)
  * Note: This only works if one_file is selected.
## QRM
* `check_similarity`: This will check if the notebook in the Databricks workspace and the source file on the network are the same for all _non-whitespace characters_. (_False_)
* `levenshtein`: This will check the [Damerau-Levenshtein distance](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance) between the notebook in the Databricks workspace and the source file on the network. It will return the normalized similarity of all _non-whitespace characters_. (_False_)
  * Note: This will overwrite the setting for check_similarity.
  * Warning: Because Damerau-Levenshtein runs in O(n^2) time, be prepared for this to take longer, especially if there are large differences between files.
* `threshold`: This is the minimum percent of similarity that a notebook needs to be considered OK. (_100_)
  * Note: This only works if levenshtein is selected.
* `check_signatures`: This will check for author and checker signatures. (_True_)

# Common Issues
- Databricks CLI not configured correctly.
  - Verify that your Databricks profile is configured by typing `databricks auth describe` in Windows PowerShell.
- Files being flagged as unable to read.
  - Most likely due to the title of the file containing a . or other character. This is currently being fixed.
- Files/folders are being skipped/flagged as scrap when they shouldn't be.
  - Verify that those files/folders in question do not contain a scrap indicator as a substring.
- The program stopped.
  - Try pressing the down arrow key a few times.
- Notebooks are being flagged as missing when they aren't actually missing.
  - Verify the spelling of the support folders including any prefixes.
