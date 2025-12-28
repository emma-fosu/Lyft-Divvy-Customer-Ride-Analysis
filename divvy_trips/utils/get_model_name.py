from pathlib import Path
from .get_all_analyses_name import get_all_analyses_names

def get_model_name(file: str, directory: str = "analyses") -> str:
    analyses_file_names = get_all_analyses_names(directory)
    file = Path(file).stem
    try:
        analyses_file_names.index(file)
        return file
    except:
        return ""