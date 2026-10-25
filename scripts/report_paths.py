"""Portable display paths for reports; never change operational filesystem paths."""
from pathlib import Path


def report_path(path, root):
    """Describe a project file relatively; omit private external locations entirely."""
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return '[external location omitted]'
