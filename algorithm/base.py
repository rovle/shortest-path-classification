from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
import networkx as nx

from itertools import combinations, product
from collections import namedtuple
from statistics import median



class ShortestPathModel():
    def __init__(self, weight_fn, ):
        """
        Class for the Shortest Path model.

            Parameters
            ----------
            weight_fn : function which takes two arguments and returns
                        a nonnegative number


        """
        self.weight_fn = weight_fn
        self.has_been_fit = False
        
    def prepare_data(self, anchor_class, other_class):
        """
        Function to prepare the data in the case where you already have
        the anchor and other class separated. Therefore, this function is
        primarily meant for testing stuff on the datasets where you already
        know the answer.

            Parameters
            ----------
            anchor_class : list or array-like of shape (n_sample, n_features)
                The list-like of "positive" examples, of which the first element
                is going to be used as the anchor vertex in the algorithm.
            
            other_class : list or array-like of shape (n_sample, n_features)
                The list-like of "negative" examples.
        """
        anchor_class, other_class = list(anchor_class), list(other_class) 
        self.current_sample = anchor_class + other_class
        self.labels = ( len(anchor_class) * [1] +
                        len(other_class) * [0] )
        self.n_of_labels = len(self.labels)
        self.data_prepared = True

    def fit(self, X=None):
        """
        Function to fit the model to the data.

            Parameters
            ----------
            X : list or array-like of shape (n_sample, n_features), default=None
                If None, then check whether the prepare_data functions has been called.
                If not, then it should be a list or an array-like which contains the data
                to be fit on.
             
            Returns
            -------
            self            
        """
        if not self.data_prepared and not X:
            raise ReferenceError("You have to supply data either through prepare_data function or directly passing it to fit!")
        if self.data_prepared and X:
            raise ReferenceError("You've already prepared data, please call fit without any new data.")
        if self.data_prepared:
            X = self.current_sample
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
        
    def fit_predict(self, X=None):
        """
        Function which first fits on the data (by calling .fit()) and
        then computes the predictions and the accuracy (if labels are known
        because the prepare_data function has been called) on the initial dataset.

            Parameters
            ----------
            X : list or array-like of shape (n_sample, n_features), default=None
                If None, then check whether the prepare_data functions has been called.
                If not, then it should be a list or an array-like which contains the data
                to be fit on.

        """
        self.fit(X)
        if self.data_prepared:
            n_samples = self.n_of_labels
        else:
            n_samples = len(X)
        self.predictions = \
                    [            
                    1 if (self.distances[str(x)] < self.decision_boundary)
                    else 0 for x in range(n_samples)
                    ]
        
        if self.data_prepared:
            n_of_hits = sum([1 if (self.labels[i] == self.predictions[i])
                                else 0
                                for i in range(len(self.labels))][1:])
            self.accuracy_ = n_of_hits / (len(self.labels) - 1)

        return self

    def predict(self, X, keep_new_nodes=False):
        """
        Function to predict the labels once the model has already been fit.

            Parameters
            ----------
            
        """
        if not self.has_been_fit:
            raise ReferenceError("The model has not been fitted yet.")
        num_X = len(X)
        for new_node_num, old_node in product(range(num_X), self.graph.nodes):
            weight = self.weight_fn(X[new_node_num], old_node)
            if weight is not float('inf'):
                self.graph.add_edge(f"new_node_ {new_node_num}",
                                    old_node, weight)
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