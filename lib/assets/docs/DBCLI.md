# Databricks CLI Configuration
1. open Windows PowerShell
2. run `winget search databricks`<br /><img title='winget search databricks' src='img/winget_search_databricks.png' />
2. accept the Miscrosoft TOS if prompted
4. run `winget install Databricks.DatabricksCLI`
5. exit Windows PowerShell
6. open Windows PowerShell
7. run `databricks auth login --host https://adb-7405618167364399.19.azuredatabricks.net/`
   - This is for the [ws-databricks-indy-indianapolis-centralus-213 workspace](https://adb-7405618167364399.19.azuredatabricks.net/); for other workspaces, use their host url.
9. name the Databricks profile or press [ENTER] to skip<br /><img title='Databricks profile configured' src='img/databricks_auth_login.png' />
10. authenticate your Databricks account in the browser
* Additional resources (instructions for Azure are the same):
  * [Install or Update the Databricks CLI | Databricks on AWS](https://docs.databricks.com/aws/en/dev-tools/cli/install)
  * [Authentication for the Databricks CLI | Databricks on AWS](https://docs.databricks.com/aws/en/dev-tools/cli/authentication)
  * [Databricks REST API reference](https://docs.databricks.com/api/workspace/introduction)

You can verify that you have set up the profile correctly by running `databricks auth describe`. It should look similar to this:
<br /><img title='Databricks profile detail' src='img/databricks_auth_describe.png' />