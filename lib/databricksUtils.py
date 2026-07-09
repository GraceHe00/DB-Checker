# libraries
import subprocess

def version() -> str | None:
    """
    Returns Databricks CLI version; if CLI is not installed, then returns nothing
    """
    try: return subprocess.run(['databricks','-v'], capture_output=True, text=True).stdout
    except: return None

def host_info() -> str | None:
    """
    Returns host info
    """
    auth_info = subprocess.run(['databricks','auth','describe'],capture_output=True,text=True).stdout
    try:
        host_url = auth_info.split()[1]
        if host_url == 'to': return None
        else: return host_url
    except: return None