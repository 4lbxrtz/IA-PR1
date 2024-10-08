"""Utils Module."""

from typing import TextIO

from .command import parse_args
from .graph import UndirectedGraph
from .parser import parse_file

DIVIDER = "-" * 40 + "\n"


def calculate_path_cost(graph: UndirectedGraph, path: list):
    """Calculate the cost of the path."""
    cost = 0
    for i in range(len(path) - 1):
        cost += graph.weights[(path[i], path[i + 1])]
    return cost


def traverse(graph: UndirectedGraph, start: int, end: int, algorithm: str ="dfs"):
    """Traverse the graph."""
    if algorithm == "dfs":
        result: tuple[list, int, list] = graph.dfs(start, end)
    elif algorithm == "bfs":
        result: tuple[list, int, list] = graph.bfs(start, end)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    return result


def print_result(
    graph: UndirectedGraph,
    start: int,
    end: int,
    result: tuple[list, int, list],
    output_file: TextIO,
):
    """Print the result to the output file."""
    path, cost, steps = result
    output_file.write(DIVIDER)
    output_file.write(f"Number of nodes: {len(graph.get_nodes())}\n")
    output_file.write(f"Number of edges: {len(graph.get_edges())}\n")
    output_file.write(f"Origin vertex: {start}\n")
    output_file.write(f"Destination vertex: {end}\n")
    output_file.write(DIVIDER)
    for i, step in enumerate(steps):
        output_file.write(f"Iteration: {i+1}:\n")
        output_file.write(f"Generated: {', '.join(map(str, step['generated']))}\n")
        output_file.write(
            f"Inspected: {', '.join(map(str, step['inspected']))}\n"
            if step["inspected"]
            else "Inspected: -\n"
        )
        output_file.write(DIVIDER)
    output_file.write(f"Path: {' - '.join(map(str, path))}\n")
    output_file.write(DIVIDER)
    output_file.write(f"Cost: {cost}\n")
    output_file.write(DIVIDER)

def run():
    """Run the application."""
    args = parse_args()
    graph = UndirectedGraph()
    parse_file(graph, args.input)
    if args.start not in graph.get_nodes():
        raise ValueError(f"Node {args.start} not in the graph")
    if args.end not in graph.get_nodes():
        raise ValueError(f"Node {args.end} not in the graph")
    result = traverse(graph, args.start, args.end, args.algorithm)
    print_result(
        graph=graph,
        start=args.start,
        end=args.end,
        result=result,
        output_file=args.output,
    )
