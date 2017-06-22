# Maximum weight clique instances

[![DOI](https://zenodo.org/badge/95154389.svg)](https://zenodo.org/badge/latestdoi/95154389)

This repository of benchmark instances for the maximum weight clique problem
accompanies the paper _On Maximum Weight Clique Algorithms, and
How They Are Evaluated_ by Ciaran McCreesh, Patrick Prosser, Kyle Simpson and James
Trimble (CP 2017, forthcoming).

All graphs are in
[DIMACS (ASCII, undirected) format](http://dimacs.rutgers.edu/pub/challenge/graph/doc/ccformat.tex).
For example, a file with the following contents would represent a graph with four
vertices with weights 10, 11, 12, 13 and a single edge from the first vertex
to the second vertex.

    p edge 4 1
    n 1 10
    n 2 11
    n 3 12
    n 4 13
    e 1 2

We hope to add further sets of instances over time.  Please contact j.trimble.1@research.glasgow.ac.uk
if you have any suggestions.
