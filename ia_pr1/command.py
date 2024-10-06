"""Parser module."""

# this module is responsible for parsing the arguments and the input file

import argparse


def parse_args():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="Graph traversal")
    parser.add_argument(
        "--input",
        type=argparse.FileType("r"),
        required=True,
        help="Input file with the graph data",
    )
    parser.add_argument(
        "--output",
        type=argparse.FileType("w"),
        default="output.txt",
        help="Output file with the traversal data",
    )
    parser.add_argument(
        "--start",
        type=int,
        required=True,
        help="Starting vertex for the traversal",
    )
    parser.add_argument(
        "--end",
        type=int,
        required=True,
        help="Ending vertex for the traversal",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        required=True,
        choices=["dfs", "bfs"],
        help="Traversal algorithm",
    )
    return parser.parse_args()
