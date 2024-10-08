"""Graph module."""

import random

from .tree import Node


class UndirectedGraph:
    """Undirected Graph class."""

    def __init__(self):
        """Initialize the graph."""
        self.graph = {}
        self.edges = []
        self.weights = {}

    def get_nodes(self):
        """Return the nodes of the graph."""
        return list(self.graph.keys())

    def get_weight(self):
        """Return the weight of the graph."""
        return self.weights

    def get_neighbors(self, node):
        """Return the neighbors of the node."""
        return self.graph[node]

    def get_unvisited_neighbors(self, node, visited):
        """Return the unvisited neighbors of the node."""
        return [n for n in self.get_neighbors(node) if n not in visited]

    def get_edges(self):
        """Return the edges of the graph."""
        for node in self.graph:
            for neighbor in self.graph[node]:
                if (neighbor, node) not in self.edges:
                    self.edges.append((node, neighbor))
        return self.edges

    def add_edge(self, node1, node2, *, weight=1):
        """Add an edge to the graph."""
        if weight == -1:
            return
        self.graph.setdefault(node1, []).append(node2)
        self.graph.setdefault(node2, []).append(node1)
        self.weights[(node1, node2)] = self.weights[(node2, node1)] = weight

    def add_node(self, node):
        """Add a node to the graph."""
        if node not in self.graph:
            self.graph[node] = []

    def remove_edge(self, node1, node2):
        """Remove an edge from the graph."""
        self.edges.remove((node1, node2))
        self.graph[node1].remove(node2)
        self.graph[node2].remove(node1)
        del self.weights[(node1, node2)]
        del self.weights[(node2, node1)]

    def remove_node(self, node):
        """Remove a node from the graph."""
        del self.graph[node]
        for n in self.graph:
            if node in self.graph[n]:
                self.graph[n].remove(node)
                del self.weights[(node, n)]
                del self.weights[(n, node)]

    def path_cost(self, path):
        """Return the cost of the path."""
        return sum(
            self.weights.get((path[i], path[i + 1]), 0) for i in range(len(path) - 1)
        )

    def dfs(self, start, end):
        """Depth-first search using Node class."""
        tree_root = Node(start)
        generated = [tree_root.id]
        inspected = []
        stack = [tree_root]
        steps: list[dict[str, list]] = []
        steps.append(
            {
                "generated": generated.copy(),
                "inspected": inspected.copy(),
            }
        )
        current: Node = None
        while stack:
            current = stack.pop()
            inspected.append(current.id)
            if current.id == end:
                path = [ancestor.id for ancestor in current.node_path]
                cost = self.path_cost(path)
                steps.append(
                    {
                        "generated": generated.copy(),
                        "inspected": inspected.copy(),
                    }
                )
                return (path, cost, steps)
            new_generated = [
                neighbor
                for neighbor in self.get_neighbors(current.id)
                if neighbor not in [ancestor.id for ancestor in current.ancestors]
            ]
            generated.extend(new_generated)
            stack.extend(
                [
                    Node(successor, parent=current)
                    for successor in reversed(new_generated)
                ]
            )
            steps.append(
                {
                    "generated": generated.copy(),
                    "inspected": inspected.copy(),
                }
            )
        if current != end:
            print("The ending node was not found.")
            path = [ancestor.id for ancestor in current.node_path]
            return (path, -1, steps)
        return (path, cost, steps)

    def bfs(self, start, end):
        """Breadth-first search using Node class."""
        tree_root = Node(start)
        generated = [tree_root.id]
        inspected = []
        queue = [tree_root]
        steps: list[dict[str, list]] = []
        steps.append(
            {
                "generated": generated.copy(),
                "inspected": inspected.copy(),
            }
        )

        def node_cost(node):
            """Return the cost of the node."""
            path = [ancestor.id for ancestor in node.node_path]
            return self.path_cost(path)

        current = None
        while queue:
            if len(queue) == 1:
              current = queue.pop(0)
            else:
                node_costs = [(node, node_cost(node)) for node in queue]
                if random.choice([True, False]):
                    current, _ = min(node_costs, key=lambda x: x[1])
                else:
                    current, _ = max(node_costs, key=lambda x: x[1])
                queue.remove(current)
            inspected.append(current.id)
            if current.id == end:
                path = [ancestor.id for ancestor in current.node_path]
                cost = self.path_cost(path)
                steps.append(
                    {
                        "generated": generated.copy(),
                        "inspected": inspected.copy(),
                    }
                )
                return (path, cost, steps)
            new_generated = [
                neighbor
                for neighbor in self.get_neighbors(current.id)
                if neighbor not in [ancestor.id for ancestor in current.ancestors]
            ]
            generated.extend(new_generated)
            queue.extend(
                [Node(successor, parent=current) for successor in new_generated]
            )
            steps.append(
                {
                    "generated": generated.copy(),
                    "inspected": inspected.copy(),
                }
            )
        if current != end:
            print("The ending node was not found.")
            path = [ancestor.id for ancestor in current.node_path]
            return (path, -1, steps)
        return (path, cost, steps)
