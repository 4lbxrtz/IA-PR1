"""Search tree module that represents the tree generated during graph traversal."""


class Node:
    """Class representing a node in the search tree."""

    def __init__(self, id, parent=None):
        self.id = id  # Node ID
        self.parent = parent  # Parent Node (None for root)
        self.children = []

    @property
    def ancestors(self):
        """Return the list of ancestors for this node."""
        ancestors = []
        current = self
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    @property
    def neighbors(self):
        """Return the list of neighbors for this node."""
        neighbors = []
        current = self
        while current:
            neighbors.extend(current.children)
            current = current.parent
        return neighbors

    @property
    def node_path(self):
        """Return the path from the root to this node."""
        path = []
        current = self
        while current:
            path.insert(0, current)  # Insert at the beginning to reverse the path
            current = current.parent
        return path

    def prevent_cycle(self, node):
        """Check if adding the given node would create a cycle in the tree."""
        current = self
        while current:
            if current.id == node.id:
                return True
            current = current.parent
        return False
