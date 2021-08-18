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
        self.predictions_on_train_set = \
                    [            
                    1 if self.distances(str(x)) < self.decision_boundary
                    else 0 for x in range(n_samples - 1)
                    ]
        
        return self

    def predict(self, X, keep_new_nodes = False):
        if not self.distances:
            raise ReferenceError("The model has not been fitted yet.")
        num_X = len(X)
        for new_node_num, old_node in product(range(num_X), self.graph.nodes):
            similarity = self.sim_function(X[new_node_num], old_node)
            if similarity is float('inf'):
                continue
            self.graph.add_edge(f"new_node_ {new_node_num}",
                                            old_node,
                                            self.sim_function(X[new_node_num],
                                                                old_node)
                                            )
        distances_new = single_source_dijkstra(self.graph,
                                                '0')[0][len(self.graph.nodes):]

        predictions = \
                    [            
                    1 if distances_new[x] > self.decision_boundary
                    else 0 for x in range(num_X)
                    ]
        
        self.graph.remove_nodes_from([f'new_node_{num}' for num in range(num_X)])
        return predictions