#  Shortest Path Classification algorithm

## Introduction

Suppose you have a dataset in which you know label of at least one – but not many more – label. Given this one labelled example, you want to classify all the other points in the dataset as either belonging to the class of that element, or the other class.

Suppose your data is composed of (feature) vectors in <img src="https://latex.codecogs.com/png.latex?\mathbb{R}^d" />  if you're not assuming anything about your data, and you're supposing the dataset is balanced, you might opt for the following classification rule: supposing you call known example's feature vector v, then compute the Euclidean distance of each element in the dataset and the vector v; the closer half is classified as the class of v, the farther half is classified as the other class.

[Detailed description]

[Local and Global elaboration]
## Installing

## Dependencies

In order to run the algorithm itself, you need the following (these are installed automatically with pip)

- numpy >= 1.19.2
- networkx >= 2.5

Additionally, to run the example provided in the GitHub repo, and all its constituent parts, you need

- beautifulsoup4 >= 4.10.0
- progressbar33 >= 2.4
- matplotlib >= 3.3.2