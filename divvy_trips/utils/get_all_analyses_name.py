from pathlib import Path


def get_all_analyses_names(directory: str = "analyses") -> list[str]:
    analyses_directory = Path(directory)

    files = [Path(file.name).stem for file in analyses_directory.glob("*.sql") if file.is_file()]
    return files