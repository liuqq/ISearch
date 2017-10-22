class SearchComp:
    def __init__(self, graph_dic, nodes):
        self.father = []
        self.graph = graph_dic
        self.nodes = nodes

    def find_connected_cpn(self):
        ## ignore 0. root
        n = len(self.nodes)
        self.father = list(range(n))
        nodes_ids = list(self.graph.keys())
        for node in nodes_ids:
            if node == 0:
                continue
            for neighbor in self.graph.get(node):
                self.union(node, neighbor)

        res = {}
        for node in nodes_ids:
            if node == 0:
                continue
            if self.find(node) not in res:
                res[self.find(node)] = [node]
            else:
                res[self.find(node)].append(node)
        return res.values()

    def union(self, a, b):
        if self.find(a) != self.find(b):
            self.father[self.find(a)] = self.find(b)

    def find(self, a):
        if self.father[a] == a:
            return a
        self.father[a] = self.find(self.father[a])
        return self.father[a]

