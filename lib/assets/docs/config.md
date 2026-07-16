# Configuration in config.ini
This file will be automatically created with the default values on the first run of DB_checker.exe if it does not exist. If any variables are omitted or removed from the configuration file, the default values will be used for fallback. (_Default values in italics_)
## General
* `host_url`: This is your Databricks host URL; typically the first part of any DB notebook URL and was used to authenticate Databricks CLI (_https://adb-7405618167364399.19.azuredatabricks.net_)
* `workspace_path`: This is the Databricks workspace path that contains the project folders (_/Workspace/Shared/ILM_Project_Codes/_)
* `client_code`: This is the client code (_0032ILM_)
* `check_extensions`: This is the toggle to force matching extensions (most of the time notebooks are downloaded as SQL but DB might recognize the notebook as a PY file) (_False_)
## Scrap
* `contains`: Any notebook title or directory name containing any value in this comma-delimited list of terms or phrases will be skipped (_scrap,clone_)
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
  * _Warning: Because Damerau-Levenshtein runs in $`O(n^2)`$ time, be prepared for this to take longer, especially if there are large differences between files._
* `threshold`: This is the minimum percent of similarity that a notebook needs to be considered OK. (_100_)
  * Note: This only works if levenshtein is selected.
* `check_signatures`: This will check for author and checker signatures. (_True_)
