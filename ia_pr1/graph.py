"""Graph module."""


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
        if node1 not in self.graph and node2 not in self.graph:
            self.edges.append((node1, node2))
        if node1 not in self.graph:
            self.graph[node1] = []
        if node2 not in self.graph:
            self.graph[node2] = []
        self.graph[node1].append(node2)
        self.graph[node2].append(node1)
        self.weights[(node1, node2)] = weight
        self.weights[(node2, node1)] = weight

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

    def reconstruct_path(self, end, predesessor):
        """Reconstruct the path from start to end."""
        path = []
        current = end
        total_cost = 0
        while current is not None:
            path.insert(0, current)
            previous = predesessor[current]
            if previous is not None:
                total_cost += self.weights[(previous, current)]
            current = previous
        return path, total_cost

    def log_neighbors(self, node, log):
        """Log the neighbors of the current node."""
        neighbors = self.get_neighbors(node)
        log.append(neighbors.copy())

    def get_unvisited_neighbors(self, node, visited):
        """Return the unvisited neighbors of the node."""
        return [n for n in self.get_neighbors(node) if n not in visited]

    def dfs(self, start, end, visited=None, output_file="output.txt"):
        """Depth-first search."""
        stack = [start]
        generated = [start]
        inspected = []
        predecessor = {start: None}
        visited = {start: True}
        iteration = 1
        self.log_iteration(iteration, generated.copy(), inspected.copy(), output_file)
        while stack:
            current = stack.pop()
            visited[current] = True
            inspected.append(current)
            if current == end:
                path, cost = self.reconstruct_path(end, predecessor)
                iteration += 1
                self.log_iteration(
                    iteration, generated.copy(), inspected.copy(), output_file
                )
                return {
                    "path": path,
                    "cost": cost,
                }
            unvisited_neighbors = self.get_unvisited_neighbors(current, visited)
            for neighbor in unvisited_neighbors:
                stack.append(neighbor)
                generated.append(neighbor)
                predecessor[neighbor] = current
            iteration += 1
            self.log_iteration(
                iteration, generated.copy(), inspected.copy(), output_file
            )
        return {
            "path": [],
            "cost": 0,
        }

    def bfs(self, start, end, visited=None, output_file="output.txt"):
        """Breadth-first search."""
        queue = [start]
        generated = [start]
        inspected = []
        predecessor = {start: None}
        visited = {start: True}
        iteration = 1
        self.log_iteration(iteration, generated.copy(), inspected.copy(), output_file)
        while queue:
            current = queue.pop(0)
            inspected.append(current)
            if current == end:
                path, cost = self.reconstruct_path(end, predecessor)
                iteration += 1
                self.log_iteration(
                    iteration, generated.copy(), inspected.copy(), output_file
                )
                return {
                    "path": path,
                    "cost": cost,
                }
            unvisited_neighbors = self.get_unvisited_neighbors(current, visited)
            for neighbor in unvisited_neighbors:
                queue.append(neighbor)
                generated.append(neighbor)
                visited[neighbor] = True
                predecessor[neighbor] = current
            iteration += 1
            self.log_iteration(
                iteration, generated.copy(), inspected.copy(), output_file
            )
        return {
            "path": [],
            "cost": 0,
        }

    def traverse(self, start, end, output_file, algorithm="dfs"):
        """Traverse the graph."""
        output_file.write(f"--------------------------------\n")
        output_file.write(f"Number of nodes: {len(self.get_nodes())}\n")
        output_file.write(f"Number of edges: {len(self.get_edges())}\n")
        output_file.write(f"Origin vertex: {start}\n")
        output_file.write(f"Destination vertex: {end}\n")
        output_file.write(f"--------------------------------\n")
        if algorithm == "dfs":
            result = self.dfs(start, end, output_file=output_file)
        elif algorithm == "bfs":
            result = self.bfs(start, end, output_file=output_file)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
        output_file.write(f"--------------------------------\n")
        output_file.write(f"Path: {' - '.join(map(str, result['path']))}\n")
        output_file.write(f"--------------------------------\n")
        output_file.write(f"Cost: {result['cost']}\n")
        output_file.write(f"--------------------------------\n")

    def parse_file(self, file):
        """Parse the file and add the edges to the graph."""
        lines = file.readlines()
        num_nodes = int(lines[0].strip())
        for i in range(1, num_nodes + 1):
            self.add_node(i)
        line_index = 1
        for i in range(1, num_nodes + 1):
            for j in range(i + 1, num_nodes + 1):
                if line_index < len(lines):
                    weight = float(lines[line_index].strip())
                    if weight != -1:
                        self.add_edge(i, j, weight=weight)
                line_index += 1

    def log_iteration(self, iteration, generated, inspected, output_file):
        """Log the iteration to the output file."""
        output_file.write(f"--------------------------------\n")
        output_file.write(f"Iteration: {iteration}\n")
        output_file.write(f"Generated: {', '.join(map(str, generated))}\n")
        output_file.write(
            f"Inspected: {', '.join(map(str, inspected))}\n"
            if inspected
            else "Inspected: -\n"
        )
