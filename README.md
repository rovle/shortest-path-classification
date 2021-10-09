#  Shortest Path Classification algorithm

## Introduction

Suppose you have a dataset in which you know label of at least one – but not many more – label. Given this one labelled example, you want to classify all the other points in the dataset as either belonging to the class of that element, or the other class.

Suppose your data is composed of (feature) vectors in <img src="https://latex.codecogs.com/png.latex?\mathbb{R}^d" />  if you're not assuming anything about your data, and you're supposing the dataset is balanced, you might opt for the following classification rule: supposing you call known example's feature vector v, then compute the Euclidean distance of each element in the dataset and the vector v; the closer half is classified as the class of v, the farther half is classified as the other class.

That is not the case that is particularly interesting to solve, but consider now a similar problem: a dataset to which you have a reasonable metric in mind, but most elements are incomparable. (You can think of a metric whose domain has been extended with positive infinity.) What is, then, the intuitive counterpart of the above algorithm?

The answer that this repo proposes is to turn the dataset into a graph where each data point is a node, and the edges between them either have a finite positive weight if two data points are comparable; otherwise infinite weight (which is basically equivalent to them not being connected, but it is slighlty more convenient to put infinite weight to avoid cumbersome situations when the graph ends up unconnected). Then, find the shortest path from our known example to each of other data point; classify the closer half (in terms of the weight of the shortest path) to the known example's class, the farther half to the other class.

### Local-global relationship

One of the reasons why I went to the trouble of implementing this model – besides the _"because it was there"_ reason – is because I find it aesthetically pleasing how the model recovers _global information_ from purely _local relationships_. This is something that seems somewhat absent in the rest of the machine learning (except in the trivial sense of models being trained on batches of data, etc.), so it seemed at least worth investigating. If you also find it aesthetically pleasing, see [List of Local to Global principles](https://math.stackexchange.com/questions/34053/list-of-local-to-global-principles). (I don't know of a really nice writeup of local-to-global principles that's not just about the number theoretical one, but, maybe one day–)

### Demo

When I originally conceived this algorithm, I had tried it out on a set of my own Facebook messages – I had a bunch that were in Croatian and a bunch that were in English, so I taught the model to differentiate between them. Since I would rather not share my personal Facebook messages, the demonstration which I put in this repo is that of the model learning to differentiate between languages in the [European Parliamentary Proceedings dataset](https://www.statmt.org/europarl/). As you can see in the demo/languages.ipynb, the model does really well, approaching very close to 100% in a lot of language pairs and/or hyperparameter settings.

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
