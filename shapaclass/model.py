from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
import networkx as nx

from itertools import combinations, product
from collections import namedtuple
from statistics import median



class ShortestPathModel():
    """Implements the Shortest Path model.

    This class is an implemention of the shortest path model, enabling
    one to prepare data for it, fit it, and use it for prediction.

    You can read more about the model at <link>.

    Parameters
    ----------
    weight_fn : function
        Function which takes two arguments and returns
        a nonnegative number; serves as a function which
        computes the weights in our graph.
            
    Attributes
    ----------
    is_fit : bool
        Flag for whether the model has been fit already or not.
    
    current_sample : list
        In case the prepare_data function is used, this holds all
        the samples in the current dataset.

    labels : list
        In case the prepare_data function is used, this holds all
        the labels of the current dataset.

    n_of_labels : int
        In case the prepare_data function is used, this is the size
        of our dataset.

    is_data_prepared : bool
        Flag for whether the prepare_data function was called.

    graph : NetworkX Graph object
        The graph object containing all the information about the
        relations in the dataset.

    distances : list
        List of distances of shortest paths from the anchor element
        to every vertex of the graph / point in the dataset.

    decision_boundary : float
        Median of the distances; points are classified as belonging
        to the anchor class if below the decision_boundary, otherwise
        to the other class.
        
    accuracy_ : float in [0,1]
        If prepare_data was called, automatically compute and save
        the 
    """

    def __init__(self, weight_fn):
        self.weight_fn = weight_fn
        self.is_data_prepared = False
        
    def prepare_data(self, anchor_class, other_class):
        """
        Function to prepare the data in the case where you already have
        the anchor and other class separated. Therefore, this function is
        primarily meant for testing stuff on the datasets where you already
        know the answer.

        Parameters
        ----------
        anchor_class : list or array-like of shape (n_sample, n_features)
            The list-like of "positive" demos, of which the first element
            is going to be used as the anchor vertex in the algorithm.
        
        other_class : list or array-like of shape (n_sample, n_features)
            The list-like of "negative" demos.

        Returns
        -------
        self : object
            Returns an instance of self.
        """
        anchor_class, other_class = list(anchor_class), list(other_class) 
        self.current_sample = anchor_class + other_class
        self.labels = ( len(anchor_class) * [1] +
                        len(other_class) * [0] )
        self.n_of_labels = len(self.labels)
        self.is_data_prepared = True
        return self

    def resolve_data(self, X):
        """
        A helper function handling the case of data being prepared
        by the prepare_data function. It serves as a preprocesing of
        the input to the fit procedure -- since fit allows None in the
        case that data was previously prepared, one has to check for the
        status of these various ways of inputting the data.

        Parameters
        ----------
        X : list or array-like of shape (n_sample, n_features), default=None
            Either None or a container of the dataset.

        Returns
        -------
        X : list or array-like of shape (n_sample, n_features)
            X, unaltered if prepare_data has not been called.
        self.current_sample : list
            The data prepared by the prepare_data function.
        """
        if not self.is_data_prepared and X is None:
            raise ReferenceError("You have to supply data either through"
                                "through the prepare_data function or"
                                "directly passing it to fit!")
        elif self.is_data_prepared and X is not None:
            raise ReferenceError("You've already prepared data,"
                                "please call fit without any new data.")
        elif self.is_data_prepared:
            return self.current_sample
        else:
            return X


    def fit(self, X=None):
        """
        Function to fit the model to the data.

        The functions first uses the weight function to build a NetworkX
        graph, whereupon (if the graph is connected and not not empty)
        distances from the anchor element are computed, via the Dijkstra
        algorithm. That is used to compute the decision boundary.

        Parameters
        ----------
        X : list or array-like of shape (n_sample, n_features), default=None
            If None, then check whether the prepare_data functions has been
            called. If not, then it should be a list or an array-like which
            contains the data to be fit on.
            
        Returns
        -------
        self : object
        Returns an instance of self.         
        """
        X = self.resolve_data(X)

        X_enumerated = list(enumerate(X))

        nodes = namedtuple('node', 'index features')
        X_enumerated = [nodes(*t) for t in X_enumerated]

        self.graph = nx.Graph()
        for x_1, x_2 in combinations(X_enumerated, 2):
            weight = self.weight_fn(x_1.features,
                                    x_2.features)
            self.graph.add_edge(str(x_1.index), str(x_2.index),
                            weight=weight)

        if nx.is_empty(self.graph):
            raise Exception("The graph is empty. Please check whether your"
                            " weight function is well configured.")
        
        self.distances = single_source_dijkstra(self.graph, '0')[0]
        self.decision_boundary = median(self.distances.values())

        return self
        
    def fit_predict(self, X=None):
        """
        Function which first fits on the data (by calling .fit())
        and then computes the predictions and the accuracy (if
        labels are known because the prepare_data function has 
        been called) on the initial dataset.

        Parameters
        ----------
        X : list or array-like of shape (n_sample, n_features), default=None
            If None, then check whether the prepare_data functions has
            been called. If not, then it should be a list or an array-like
            which contains the data to be fit on.

        Returns
        -------
        self : objects
        Returns an instance of self.
        """
        self.fit(X)

        if self.is_data_prepared:
            n_samples = self.n_of_labels
        else:
            n_samples = len(X)

        self.predictions = \
                    [            
                    1 if (self.distances[str(x)] < self.decision_boundary)
                    else 0 for x in range(n_samples)
                    ]
        
        if self.is_data_prepared:
            n_of_hits = sum([1 if (self.labels[i] == self.predictions[i])
                                else 0
                                for i in range(len(self.labels))][1:])
            self.accuracy_ = n_of_hits / (len(self.labels) - 1)

        return self

    def predict(self, X, keep_new_nodes=False):
        """
        Function that predicts classes of a new dataset given to it.

        In particular, depending on whether the keep_new_nodes if True or
        False it might incorporate that new dataset into its graph, or it
        might not.

        Parameters
        ----------
        X : list or array-like of shape (n_sample, n_features), default=None
            A container for example to be classified.
        
        keep_new_nodes : boolean
            If True, leave the X in the model's graph, otherwise remove
            them.

        Returns
        -------
        self : objects
        Returns an instance of self.
        """
        try:
            self.graph
        except NameError:
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
            self.graph.remove_nodes_from([f'new_node_{num}'
                                            for num in range(num_X)])

        return predictions