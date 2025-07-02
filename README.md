# Introduction to Graph Theory for Gamedevs

## Abstract

This pamphlet serves to purposes.

1. Introduce graph theory to teach concepts and graph structures for game
   developers, both programmers and artistic creators.  This also entails
   expositing some algorithms, although all algorithms mentioned herein are
   quite simple.

2. Through structures, models, and problems from graph theory, give ideas to
   game creators about possible games, puzzles, and also AI (bot) strategies
   for games.  It also might explain what makes a certain graph problem easy or
   hard.


## Basic graph theory and representation

A graph is a mathematical object where we have objects (abstractly called nodes
or vertices) and relations between them.  If two objects, e.g. $v_1$ and $v_2$
have a relation, we say that $v_1$ and $v_2$ have an _edge_.  Sometimes this
relationship is abstract, as in "they live in the same city", "they went to the
same school", and sometimes it's more concrete, $v_1$ and $v_2$ are
intersections and $e$ is a road segment that goes directly between $v_1$ and
$v_2$.

We will be completely abstract and say that we have a _set_ of _nodes_ and a
set of _edges_, and that is it.

[picture of graphs]

Often the edges, i.e. relationships, are _symmetric_.  That means that if $v_1,
v_2$ is an edge, then necessarily $v_2 v_1$ is an edge.  For example consider
that $v_1$ and $v_2$ are friends, or live in the same street, went to the same
school, or that there is a trail in the woods from $v_1$ to $v_2$.  But
sometimes it's not symmetric.  Just because Jack follows Jill on some social
site, it's not necessarily the case that Jill follows Jack.  Furthermore, just
because you can drive from $v_1$ to $v_2$ doesn't mean that you can go the
other way, as in _one-way streets_ (or; you can, it's just not guaranteed to be
legal).  An edge can mean that $v_1$ is the mother of $v_2$.  Is $v_2$ the
mother of $v_1$, then? Certainly not.

We call graphs that are inherently asymmetric _directed graphs_.

Some times, we would like to put some _values_, often referred to as _weights_
or _costs_, on our objects or edges.  Suppose that you have a road network, and
you want to know what the length, speed limits, or perhaps tolls, are on roads
(or all).  Then we say that we have a _weighted graph_, and each edge $e =
(v_1, v_2)$ has an edge cost $c(e)$.  If you have an _unweighted graph_, it's
the same as assuming that $c(e)= 1$ for all edges.

If you want to go from $A$ to $B$ in your road network, you might want to find
a route that is _shortest_, _fastest_, or _cheapest_.  Short means length, fast
means length times (expected) speed, cheapest is perhaps sum of tolls.

Heck, maybe you can go the wrong way in a one-way street provided that the
expectation that you get fined is low enough!

### Representation and prerequisites

When representing a graph in a computer program, we could go the easy way and
use two lists.  One list of nodes, $V$, and one list of edges $E$.  However, it
turns out that for many algorithmic purposes, this is too slow.  Instead we use
one of two ways of representing graphs that are _adjacency list_ or _adjacency
matrix_.

#### Adjacency list

#### Adjacency matrix

#### Data structures?

* Fibonacchi heap, priority queue?
* Union find for MST?

## Paths, navigation, and the art of finding

Covered in this section:

* Problems
  * Path finding and mazes
  * flood-filling
  * puzzle solving (rubik, 15-puzzle, die hard water)
  * planar $\sqrt n$ portals and highways
  * APSP
* Algorithms
  * BFS
  * Dijkstra's
  * $A^*$
  * Bidirectional search
  * Floyd--Warshall
  * Bellman--Ford, Johnson's algorithm

## Global navigation

* Problems
  * No-Lift Pencil Drawing
  * TSP
  * Ticket 2 Ride
* Algorithms
  * Euler walks
  * TSP
  * Longest path

## Cutting and flowing

* Problems
  * Matching (assignment)
  * Min s-t-Cut
  * Max flow
  * Disjoint Paths
  * Vertex and edge capacities, Undirected to directed
  * Min-cost max flow
  * Max-weight perfect matching
  * Circulation with demand
* Algorithms
  * Ford--Fulkerson / Edmonds--Karp
  * The Hungarian Method
  * Suurballe

## Covering, hitting, packing

* Problems
  * R-B-Dom Set, Vertex Cover, Tower defense
  * War defense, cutting-off
  * Independent set (scattering)
* Algorithms
  * VC appx
  * VC for bipartite graph
  * reduction rules


## Drawing and partitioning and clustering

* Problems
  * Graph drawing
  * Cluster editing
  * Community detection
  * Clique (?)
  * MST (connectivity and clustering)
  * Steiner tree
  * Centrality measures
  * Cascading and fire fighting, disease propagation
* Algorithms
  * Spring layout
  * Louvain and LCA
  * Betweenness, Page rank

## Geometric embeddings

* Problems
  * Regions from fences (Planar dual)
  * Convex hull ??
* Algorithms
  * Explain that `left of` (not well known) gives rise to
    * planar dual (rotation system)
    * convex hull (and convex polygon containment)
    * line intersection
    * triangle and polygon containment

### Interval graphs

* Problems
  * Interval scheduling (chromatic number)
  * Interval partitioning (clique)
  * Cops & robbers
  * Rabbit hunting
* Algorithms
  * Greedy algorithms for interval scheduling and coloring

### Dynamic graphs

Explain that **this changes everything**.

Many graphs are temporal and dynamic, and algorithms here ... tough stuff
