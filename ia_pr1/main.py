"""Main module for the application."""

from .graph import UndirectedGraph


def main():
    """Entry point function for the application."""
    graph = UndirectedGraph()
    graph.parse_file("input.txt")
    graph.traverse(start=1, end=15, algorithm="dfs", output_file="output.txt")
