#  Shortest Path Classification algorithm

Suppose you want to classify a set of messages written in two languages, but you have no labeled examples, only a bunch of messages from both of those language. You could take one message, see which language it is, and then classifty those messages "similar" to it as that language, and those "dissimilar" as the other.
But defining similarity for general pairs of strings in languages might be a bit of a daunting task. One can, e.g., define a similarity as a function of how many words two strings share, but then many string become incomparable.

That's where this algorithm comes in play. Given a dataset $\mathcal{D}$ and a metric $\mathrm{d} : \mathcal{D} \to [0, +\infty]$ (note that this metric can [assume infinity](https://math.stackexchange.com/a/399759)), one forms a graph between points, with an edge between points $x_1$ and $x_2$ existing iff $\mathrm{d}(x_1, x_2)$ is finite. Then one takes one example which they can classify, and finds shortest weighted path between it and all other points in the dataset; classifying them with respect to weight of the path between the known example and them.

### Demo

In the demo/ folder, I test the model's ability to classify between pairs of languages in the [European Parliamentary Proceedings dataset](https://www.statmt.org/europarl/). The model approaches 100% in a lot of language pairs and/or hyperparameter settings.

In order to run the demo/languages.ipynb notebook yourself, you have to first call the scripts which download and prepare the dataset. You need to execute these two scripts in this order:
1. demo/dataset_utils/get_dataset.py
2. demo/dataset_utils/extract_language_text.py

## Installing

Just run

```
pip install shapaclass
```
Or alternatively, clone this repository. If you want to run the demo, you will have to clone the repository because only the algorithm part is on PiPy.

## Dependencies

In order to run the algorithm itself, you need the following (these are installed automatically with pip)

- NumPy (>= 1.19.2)
- NetworkX (>= 2.5)

Additionally, to run the example provided in the GitHub repo, and all its constituent parts, you need

- BeautifulSoup4 (>= 4.10.0)
- ProgressBar33 (>= 2.4)
- Matplotlib (>= 3.3.2)
