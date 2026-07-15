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
