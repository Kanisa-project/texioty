import os
import glob
import requests
from dotenv import load_dotenv

load_dotenv()


def check_file_exists(path: str) -> bool:
    """Use glob to check if a file exists."""
    if glob.glob(path):
        return True
    return False

def project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def asset_path(*parts: str) -> str:
    return os.path.join(project_root(), "..", "assets", *parts)

def output_root() -> str:
    """
    Root folder for generated/output files. Adjust as needed.
    """
    return os.path.join(project_root(), "filesOutput")

def input_root() -> str:
    """
    Root folder for input files, such as fonts, sounds or images. Adjust as needed.
    """
    return os.path.join(project_root(), "..", "filesInput")

def output_path(*parts: str) -> str:
    """
    Build a path inside the output directory.
    """
    return os.path.join(output_root(), *parts)

def ensure_parent_dir(file_path: str) -> str:
    """
    Ensure the parent directory of file_path exists. Return the original file_path.
    """
    parent = os.path.dirname(file_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    return file_path

def safe_filename(name: str, replacement: str = "_") -> str:
    """
    Sanitize a filename or path segment by replacing common invalid characters.
    Keeps it simple and cross-platform friendly.
    """
    invalid = '<>:"/\\|?*\n\r\t'
    return "".join((c if c not in invalid else replacement) for c in name).strip()

def get_stock_price(ticker):
    url = f"https://api.api-ninjas.com/v1/stockprice?ticker={ticker}"
    response = requests.get(url, headers={"X-Api-Key": os.getenv("API_NINJAS")})
    data = response.json()
    return data