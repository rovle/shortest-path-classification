from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
import networkx as nx

from itertools import combinations, product
from collections import namedtuple
from statistics import median



class ShortestPathModel():
    def __init__(self, weight_fn, ):
        self.weight_fn = weight_fn
        self.has_been_fit = False

    def fit(self, X):        
        X_enumerated = list(enumerate(X))

        nodes = namedtuple('node', 'index features')
        X_enumerated = [nodes(*t) for t in X_enumerated]

        self.graph = nx.Graph()
        for x_1, x_2 in combinations(X_enumerated, 2):
            weight = self.weight_fn(x_1.features,
                                            x_2.features)
            if weight is not float('inf'):
                self.graph.add_edge(str(x_1.index), str(x_2.index),
                                weight=weight)
        
        self.distances = single_source_dijkstra(self.graph, '0')[0]
        self.decision_boundary = median(self.distances.values())

        self.has_been_fit = True
        return self
        
    def fit_predict(self, X):
        self.fit(X)
        n_samples = len(X)
        self.predictions_on_train_set = \
                    [            
                    1 if (self.distances[str(x)] < self.decision_boundary)
                    else 0 for x in range(n_samples)
                    ]
        
        return self

    def predict(self, X, keep_new_nodes=False):
        if not self.has_been_fit:
            raise ReferenceError("The model has not been fitted yet.")
        num_X = len(X)
        for new_node_num, old_node in product(range(num_X), self.graph.nodes):
            weight = self.weight_fn(X[new_node_num], old_node)
            if weight is not float('inf'):
                self.graph.add_edge(f"new_node_ {new_node_num}",
                                    old_node, weight)                                    )
        distances_new = single_source_dijkstra(self.graph,
                                                '0')[0][len(self.graph.nodes):]

        predictions = \
                    [            
                    1 if distances_new[x] < self.decision_boundary
                    else 0 for x in range(num_X)
                    ]
        
        if not keep_new_nodes:
            self.graph.remove_nodes_from([f'new_node_{num}' for num in range(num_X)])

        return predictions