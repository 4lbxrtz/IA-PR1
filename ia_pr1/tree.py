"""Search tree module that represents the tree generated during graph traversal."""


class Node:
    """Class representing a node in the search tree."""

    def __init__(self, id: int, parent=None):
        self.id = id
        self.parent = parent
        self.children = []

    @property
    def ancestors(self) -> list:
        """Return the list of ancestors for this node."""
        ancestors = []
        current = self
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    @property
    def neighbors(self) -> list:
        """Return the list of neighbors for this node."""
        neighbors = []
        current = self
        while current:
            neighbors.extend(current.children)
            current = current.parent
        return neighbors

    @property
    def node_path(self) -> list:
        """Return the path from the root to this node."""
        path = []
        current = self
        while current:
            path.insert(0, current)  # Insert at the beginning to reverse the path
            current = current.parent
        return path
