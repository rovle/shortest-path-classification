import networkx as nx
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
from statistics import median
from itertools import combinations, product
from collections import namedtuple



class ShortestPathModel():
    def __init__(self, sim_function, ):
        self.sim_function = sim_function


    def fit(self, X):        
        X_enumerated = list(enumerate(X))

        nodes = namedtuple('node', 'index features')
        X_enumerated = [nodes(*t) for t in X_enumerated]

        self.graph = nx.Graph()
        for x_1, x_2 in combinations(X_enumerated, 2):
            similarity = self.sim_function(x_1.features,
                                            x_2.features)
            if similarity is not float('inf'):
                self.graph.add_edge(str(x_1.index), str(x_2.index),
                                weight=similarity)
        
        self.distances = single_source_dijkstra(self.graph, '0')[0]
        self.decision_boundary = median(self.distances.values())

        return self
        
    def fit_predict(self, X):
        self.fit(X)
        n_samples = len(X)
        predictions = [1 if self.distances(str(x)) > self.decision_boundary
                    else 0 for x in range(n_samples - 1)]
            

        pass

    def predict(self):
        pass