"""Parser module."""

from typing import TextIO

from .graph import UndirectedGraph


def parse_file(graph: UndirectedGraph, file: TextIO):
    """Parse the file and add the edges to the graph."""
    lines = file.readlines()
    num_nodes = int(lines[0].strip())
    for i in range(1, num_nodes + 1):
        graph.add_node(i)
    line_index = 1
    for i in range(1, num_nodes + 1):
        for j in range(i + 1, num_nodes + 1):
            if line_index < len(lines):
                weight = float(lines[line_index].strip())
                if weight != -1:
                    graph.add_edge(i, j, weight=weight)
            line_index += 1
