# Utility functions for path manipulation

import os


def get_path(path):
    """Return the absolute path of the given path."""
    return os.path.abspath(path)


def get_parent(path):
    """Return the parent directory of the given path."""
    return os.path.dirname(path)


def get_filename(path):
    """Return the filename of the given path."""
    return os.path.basename(path)


def get_extension(path):
    """Return the extension of the given path."""
    return os.path.splitext(path)[1]


def get_root():
    """Return the absolute path of the app directory."""
    return get_parent(get_parent(get_path(__file__)))


def get_tmp():
    """Return the absolute path of the tmp directory."""
    return os.path.join(get_root(), "tmp")
