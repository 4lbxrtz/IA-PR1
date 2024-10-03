"""Main module for the application."""

from .graph import UndirectedGraph
from .parser import parse_args


def main():
    """Entry point function for the application."""
    args = parse_args()
    graph = UndirectedGraph()
    graph.parse_file(args.input)
    graph.traverse(
        start=args.start,
        end=args.end,
        algorithm=args.algorithm,
        output_file=args.output,
    )
