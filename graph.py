from collections import defaultdict
import heapq

INF = 1E4


class Graph:
    def __init__(self, undirected=False):
        self.graph = defaultdict(dict)  # dictionary containing adjacency List
        self.V = set()
        self.undirected = undirected

    def add_edge(self, u, v, w):
        if self.undirected:
            self.graph[u][v] = w
            self.graph[v][u] = w
        else:
            self.graph[u][v] = w
        self.V.add(u)
        self.V.add(v)

    def print_graph(self):
        print(self.graph)

    def bfs(self, src):
        # Time complexity O(E+V)
        # Space complexity O(V)
        stack = [src]
        visited = dict()
        bfs_order = []
        for i in self.V:
            visited[i] = 0
        while stack:
            cur = stack.pop(0)
            bfs_order.append(cur)
            visited[cur] = 1
            for i in self.graph[cur]:
                if not visited[i]:
                    stack.append(i)
            visited[cur] = 2
        return bfs_order

    def _dfs_visit(self, graph, v, visited, topological_sort, dfs_order):
        visited[v] = 1
        dfs_order.append(v)
        for i in graph[v]:
            if visited[i] == 1:
                self.dag = 0
            if not visited[i]:
                visited, topological_sort, dfs_order = self._dfs_visit(
                    graph, i, visited, topological_sort, dfs_order)
        visited[v] = 2
        topological_sort.insert(0, v)
        return visited, topological_sort, dfs_order

    # Time complexity O(E+V)
    def dfs(self):
        visited = dict()
        dfs_order = []
        topological_sort = []
        self.dag = 1
        for i in self.V:
            visited[i] = 0
        for i in self.V:
            if not visited[i]:
                visited, topological_sort, dfs_order = self._dfs_visit(
                    self.graph, i, visited, topological_sort, dfs_order)
        return topological_sort, dfs_order

    def mst_kruskal(self):
        # time complexity O(ElogV).
        mst_set = dict()  # for each node in the graph, the set it belongs to.
        node_sets = dict()  # for each set, the list of all the nodes.
        mst_parent = defaultdict(list)  # The parent of each node.

        for i in self.V:
            mst_set[i] = i
            node_sets[i] = [i]
        self.E = []
        for i in self.graph:
            for j in self.graph[i]:
                self.E.append((self.graph[i][j], i, j))
        self.E.sort()
        total_weight = 0
        for e in self.E:
            old_set = mst_set[e[2]]
            new_set = mst_set[e[1]]
            if old_set != new_set:
                for i in node_sets[old_set]:
                    mst_set[i] = new_set
                    node_sets[new_set].append(i)
                del node_sets[old_set]
                mst_parent[e[2]].append(e[1])
                total_weight += e[0]
        return mst_parent, total_weight

    def _exchange(self, nums, i, j):
        tmp = nums[i]
        nums[i] = nums[j]
        nums[j] = tmp

    def mst_prim(self):
        src = 1
        h = []
        mst_tree = self._initialize_single_source(src)
        visited = [src]
        for i in self.graph[src]:
            heapq.heappush(h, (self.graph[src][i], src, i))
        total_weight = 0
        while h:
            weight, parent, cur = heapq.heappop(h)
            if cur not in visited:
                mst_tree[cur]['parent'] = parent
                visited.append(cur)
                total_weight += weight
                for i in self.graph[cur]:
                    if i not in visited:
                        heapq.heappush(h, (self.graph[cur][i], cur, i))
        return mst_tree, total_weight

    def _initialize_single_source(self, src):
        shortest_path = defaultdict(dict)
        for i in self.V:
            shortest_path[i]['weight'] = INF
            shortest_path[i]['parent'] = None
        shortest_path[src]['weight'] = 0
        return shortest_path

    def _relax(self, start, end):
        if self.graph[start][end] + self.shortest_path[start]['weight'] < self.shortest_path[end]['weight']:
            self.shortest_path[end]['weight'] = self.graph[start][end] + \
                self.shortest_path[start]['weight']
            self.shortest_path[end]['parent'] = start

    def shortest_path_bellman_ford(self, src):
        # Complexity Bellman_ford O(VE)
        # Complexity Bellman_ford DAG O(V+E)
        # TO-DO: determine if it is a DAG
        self.shortest_path = self._initialize_single_source(src)
        if self.dag:
            topological_sort, _ = self.dfs()
            for i in topological_sort:
                for v in self.graph[i]:
                    self._relax(i, v)
        else:
            for i in self.V:
                for start in self.graph:
                    for end in self.graph[start]:
                        self._relax(start, end)

        print('Shortest path with Bellman-ford algorithm.')
        print(self.shortest_path)

    def shortest_path_dijkstra(self, src):
        # Time complexity: O(VlogV+E)
        self.shortest_path = self._initialize_single_source(src)
        h = []
        visited = []
        for i in self.V:
            heapq.heappush(h, (self.shortest_path[i]['weight'], i))
        while h:
            weight, cur = heapq.heappop(h)
            visited.append(cur)
            for i in self.graph[cur]:
                if i not in visited:
                    h.remove((self.shortest_path[i]['weight'], i))
                    self._relax(cur, i)
                    heapq.heappush(h, (self.shortest_path[i]['weight'], i))
        print('Shortest path with Dijktra algorithm')
        print(self.shortest_path)

    def _transpose(self, graph):
        graph_transposed = defaultdict(dict)
        for i in self.graph:
            for j in self.graph[i]:
                graph_transposed[j][i] = self.graph[i][j]
        return graph_transposed

    def strongly_connected_component(self):
        topological_sort, _ = self.dfs()
        graph_transposed = self._transpose(self.graph)
        visited = dict()
        for i in self.V:
            visited[i] = 0
        cnt = 0
        for i in topological_sort:
            if not visited[i]:
                visited, topological_sort_node, _ = self._dfs_visit(
                    graph_transposed, i, visited, [], [])
                print('Nodes in strongly connected component %d:' % cnt)
                print(topological_sort_node)
                cnt += 1
