"""Search tree module that represents the tree generated during graph traversal."""


class SearchTree:
    """Search Tree class."""

    def __init__(self):
        """Initialize the search tree."""
        self.tree = {}
        self.path_costs = {}

    def add_node(self, parent, node, *, cost=1):
        """Add a node to the search tree."""
        if parent not in self.tree:
            self.tree[parent] = []
        self.tree[parent].append(node)
        if (parent, node) not in self.path_costs:
            self.path_costs[(parent, node)] = []
        self.path_costs[(parent, node)].append(cost)

    def get_neighbors(self, node):
        """Return the neighbors of the node."""
        return self.tree.get(node, [])

    def get_ancestors(self, node):
        """Return the ancestors of the node."""
        ancestors = []
        current = node
        while True:
            parent = next(
                (p for p, children in self.tree.items() if current in children), None
            )
            if parent is None:
                break
            ancestors.append(parent)
            current = parent
        return ancestors

    def get_cost(self, parent, node):
        """Return the cost of the edge between the parent and the node."""
        return self.path_costs.get((parent, node), None)

    def reconstruct_path(self, start, end):
        """Reconstruct the path from start to end."""
        path = []
        current = end
        total_cost = 0
        while current is not None and current != start:
            path.insert(0, current)
            previous = None
            for parent, child in self.tree.items():
                if current in child:
                    previous = parent
                    break
            if previous is not None:
                total_cost += self.get_cost(previous, current)
            current = previous
        path.insert(0, start)
        return path, total_cost

    def __repr__(self) -> str:
        """Return the string representation of the search tree."""
        return f"Search tree: {self.tree}\nPath costs: {self.path_costs}"

    def log_tree(self, output):
        """Log the current state of the search tree."""
        output.write(f"--- Search tree---\n")
        for parent, children in self.tree.items():
            children_str = ", ".join(map(str, children))
            output.write(f"{parent}: {children_str}\n")
            for child in children:
                output.write(
                    f"{parent} --> {child} (cost: {self.path_costs[(parent, child)]})\n"
                )
            output.write("\n")
            output.write(f"Ancestors of {parent}: {self.get_ancestors(parent)}\n\n")
        output.write(f"--- End of Search tree ---\n")

    def get_min_cost(self, parent, node):
        """Return the minimum cost of the node."""
        return min(self.path_costs.get(parent, node), [], default=None)

    def get_max_cost(self, parent, node):
        """Return the maximum cost of the node."""
        return max(self.path_costs.get(parent, node), [], default=None)

    def update_weight(self, parent, node, new_weight):
        """Update the weight of the edge between the parent and the node."""
        self.path_costs[(parent, node)] = new_weight
        self.path_costs[(node, parent)] = new_weight

    def detect_cycle(self, parent, node):
        """Detect a cycle in the search tree."""
        if parent == node:
            return True
        current = parent
        while current is not None:
            if current == node:
                return True
            current = next(
                (p for p, children in self.tree.items() if current in children), None
            )
        return False
