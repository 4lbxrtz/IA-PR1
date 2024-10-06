"""Main module for the application."""

from .utils import run


def main():
    """Entry point function for the application."""
    try:
        run()
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
