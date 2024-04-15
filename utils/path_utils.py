from pathlib import Path


def get_root_repo_path() -> Path:
    """Return Path to the root the repo"""
    return Path(__file__).parent.parent
