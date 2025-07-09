---
documentclass: memoir
fontsize: 14pt
title: Introduction to Graph Theory for Gamedevs
author: Pål Grønås Drange
date: Summer 2025
papersize:
  - a4paper
header-includes:
  - \usepackage{microtype}
  - \usepackage{newpx}
  - \usepackage{froufrou}
abstract: |

    This pamphlet serves to purposes.

    1. Introduce graph theory to teach concepts and graph structures for game
       developers, both programmers and artistic creators.  This also entails
       expositing some algorithms, although all algorithms mentioned herein are
       quite simple.

    2. Through structures, models, and problems from graph theory, give ideas to
       game creators about possible games, puzzles, and also AI (bot) strategies
       for games.  It also might explain what makes a certain graph problem easy or
       hard.

---

\tableofcontents

# Basic graph theory and representation

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
means length times (expected) speed, cheapest is perhaps sum of tolls.  In all
these cases, the weight of an edge is some non-negative value.  A road segment
cannot be a negative length, a speed limit is unlikely to be negative, and the
tolls on a road is likely non-negative (except someone has a crate of gold to
give you).  However, one can definitely imagine negative weights: Let the
weight of a road segment represent the energy used by an electric vehicle (EV)
to traverse it.  An EV uses a certain amount of energy to travel a segment,
depending on distance and slope.  If the road is steep downhill and the EV has
regenerative braking, it might actually _gain energy_, resulting in a
_negative_ net energy usage for that segment.  This means that if you want to
find a shortest path from $A$ to $B$ for an EV, you need to take into account
battery level and slope, and perhaps your path-finding algorithm needs to
handle negative weights---something we will see later that Dijkstra's algorithm
does not do.

\froufrou

Ultimately, a graph is therefore---mathematically, and in code---a tuple
consisting of the vertices $V$, the edges $E \subseteq V \times V$, sometimes a
weight function on vertices $w: V \to \mathbb{R}$, and a weight function on
edges $c: E \to \mathbb{R}$.  In code,

```python
G = (V, E, w)
```

## Representation and Prerequisites

When representing a graph in a computer program, we could go the easy way and
use two lists.  One list of nodes, $V$, and one list of edges $E$.  However, it
turns out that for many algorithmic purposes, this is too slow.  Instead we use
one of two ways of representing graphs that are _adjacency list_ or _adjacency
matrix_.

### Adjacency List

The simplest form of a graph represented in code is the adjacency list:

```python

G = [
     [b],        # a
     [a, c, e],  # b
     [b, d, f],  # c
     [c, f],     # d
     [b, f],     # e
     [c, d, e],  # f
]
```

### Adjacency Matrix



```python
G = [ # a  b  c  d  e  f
       [0, 1, 0, 0, 0, 0],  # a
       [1, 0, 1, 0, 1, 0],  # b
       [0, 1, 0, 1, 0, 1],  # c
       [0, 0, 1, 0, 0, 1],  # d
       [0, 1, 0, 0, 0, 1],  # e
       [0, 0, 1, 1, 1, 0],  # f
]
```

### Grid Representation

Sometimes we have a very small tile world, and it might make sense to represent
the entire graph as a simple list of characters.  Here, a `.` means an empty
space, whereas a `#` means an obstacle.  The `S` and `T` are the start and goal
of a maze.


```
####################
#T.#.#....#...#....S
##.###.##.###.##.###
#..##..#..##..#..##.
##..#.###....###....
##....###....###.###
##.######.###.##.###
#..##..#..##.....##.
#..#...#......#..#..
####################
```

In this maze, we are allowed to move `U`, `D`, `R`, and `L`, as long as we do
not enter an obstacle.  It is not hard to see that the following gives a path
from `S` to `T`.  We will see in the next section how to find this path
programatically.

```
####################
#To#.#oooo#...#.oooS
##o###o##o###.##o###
#.o##oo#.o##..#.o##.
##oo#o###o...###o...
##.ooo###o...###o###
##.######o###.##o###
#..##..#.o##ooooo##.
#..#...#.oooo.#..#..
####################
```


# Paths, Navigation, and the Art of Finding

## Path Finding and Mazes

Suppose that you have an AI who wants to travel from $A$ to $B$, or that _you_
want to travel from $A$ to $B$, and you want to highlight the path on the map.
In this case, we need to find a _path_, whatever that is, that (a) starts in
$A$, (b) ends in $B$, and is (c) as short as possible.  There are many path
finding algorithms, and they all serve different purposes.

To illustrate the simplicity of a path finding algorithm, here is DFS:

```python
def dfs(G, u, visited=None):
  if visited is None:
    visited = set()
  visited.add(u)
  for v in G[u]:
    if v not in visited:
      dfs(G, v, visited)
  return visited
```

The problem with DFS, however, is that it does not necessarily find the
_shortest_ path, only some path.  In addition, as it is now, it is recursive,
and that is something we want to avoid.  So instead of using DFS, we will use
BFS for our path finding.  Here is BFS, the simplest path finding algorithm
that finds (and returns) the shortest path from $s$ to _any other vertex_,
together with the distance.  The running time of BFS is $O(n+m)$, meaning
_linear time_, meaning that it essentially takes as long time to run BFS as it
takes to read the graph.

```python
from collections import deque

def bfs(G, s):
  visited = set()
  dist = {s: 0}
  parent = {s: None}
  queue = deque([s])
  while queue:
    u = queue.popleft()
    for v in G[u]:
      if v not in visited:
        visited.add(v)
        dist[v] = dist[u] + 1
        parent[v] = u
        queue.append(v)
  return dist, parent
```

Suppose that you have a map, and your player is in the spawn area, and wants to
find a route to the bomb site.  As long as your world has, for each coordinate,
a list of "neighboring cells", you can plug that directly into the `bfs`
routine above, where $G[u]$ means the neighboring cells of $u$.  The return
value, i.e., when we write

```python
dist, parent = bfs(world, current_location)
```

\noindent is the distance and a form of linked list leading from each vertex to
a vertex closer to the start.

### Flood Filling

This algorithm can also be used as a flood filling algorithm.


### Weighted graphs

When the "cost" of moving from one "cell" to another is not the same
everywhere; for example running in water or running uphill can be more
expensive, we need an algorithm that can deal with these costs.  BFS can
unfortunately not.

Dijkstra's algorithm is an algorithm that works similarly to BFS, but instead
of a queue that we iterate through, we have a _priority queue_.  A priority
queue is a queue in which the First In First Out is replaced with "Most
Important Out".  That is, the order of insertion is irrelevant; when we pop
from the queue, we pop the one with highest priority (typically this is the one
with _lowest possible value_).

```python
import heapq

def dijkstra(G, s):
  dist = {s: 0}
  parent = {s: None}
  visited = set()
  heap = [(0, s)]

  while heap:
    d, u = heapq.heappop(heap)
    if u in visited:
      continue
    visited.add(u)
    for v, w in G[u]:
      if v not in dist or d + w < dist[v]:
        dist[v] = d + w
        parent[v] = u
        heapq.heappush(heap, (dist[v], v))

  return dist, parent
```


## Puzzle Solving

It is not only in the literal sense that path finding algorithms are useful.
Consider Rubik's Cube, the 15-puzzle, or the classic Die Hard puzzle of filling
a 5 liter bucket with 4 liters of water using only 3 and 5 liter buckets.

Suppose, we want to help MacClane with his task.  Construct an abstract "state
space graph" where you have the node set as $(c_3, c_5)$ where $c_3 \in \{0, 1,
2, 3\}$ and $c_5 \in \{0, 1, 2, 3, 4, 5\}$.  Suppose that you have $c_3$ liters
of water in the small bucket and $c_5$ liters of water in the large bucket.
What can you do?  Fill one of them, i.e., the next states are $(3, c_5)$ or
$(c_3, 5)$.  Alternatively, you can empty one of them, i.e., the next states
are $(0, c_5$) or $(c_3, 0)$.  Finally, you can pour from one to the other
until either pourer becomes empty or the pouree becomes full: $(\max(c_5 - c_3,
0), \min(c_5 + c_3, 5)$, or the other way around.  How do we go from $(0,0)$ to
$(0, 4)$?  Simply run `bfs(G, (0,0))`.

However, running the 15-puzzle with BFS might take longer than necessary.  An
algorithm $A^*$ is cool.  It is simply Dijkstra's algorithm, but with a small
estimation of remaining distance.

```python
import heapq


def astar(G, s, t, h):
  dist = {s: 0}
  parent = {s: None}
  heap = [(h(s), s)]

  while heap:
    _, u = heapq.heappop(heap)
    if u == t:
      break
    for v, w in G[u]:
      alt = dist[u] + w
      if v not in dist or alt < dist[v]:
        dist[v] = alt
        parent[v] = u
        heapq.heappush(heap, (alt + h(v), v))

  return dist, parent
```


## Negative Distances

As mentioned above, suppose the energy usage for an EV is negative in certain
steep downhill segments.



## --- NOTES ---

Covered in this section:

* Problems
  * planar $\sqrt n$ portals (distance oracle) and highways
  * APSP
* Algorithms
  * Bidirectional search
  * Floyd--Warshall
  * Bellman--Ford, Johnson's algorithm

# Global navigation

* Problems
  * No-Lift Pencil Drawing
  * TSP
  * Ticket 2 Ride
* Algorithms
  * Euler walks
  * TSP
  * Longest path

# Cutting and flowing

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

# Covering, Hitting, and Packing

* Problems
  * R-B-Dom Set, Vertex Cover, Tower defense
  * War defense, cutting-off
  * Independent set (scattering)
* Algorithms
  * VC appx
  * VC for bipartite graph
  * reduction rules


# Drawing, Partitioning, and Clustering

* Problems
  * Graph drawing
  * Cluster editing
  * Community detection
  * Clique (?)
  * MST (connectivity and clustering)
    * Union--find
  * Steiner tree
  * Centrality measures
  * Cascading and fire fighting, disease propagation
* Algorithms
  * Spring layout
  * Louvain and LCA
  * Betweenness, Page rank

# Geometric Embeddings

* Problems
  * Regions from fences (Planar dual)
  * Convex hull ??
* Algorithms
  * Explain that `left of` (not well known) gives rise to
    * planar dual (rotation system)
    * convex hull (and convex polygon containment)
    * line intersection
    * triangle and polygon containment

## Interval Graphs

* Problems
  * Interval scheduling (chromatic number)
  * Interval partitioning (clique)
  * Cops & robbers
  * Rabbit hunting
* Algorithms
  * Greedy algorithms for interval scheduling and coloring


# What now?

## Dynamic graphs

Explain that **this changes everything**.

Many graphs are temporal and dynamic, and algorithms here ... tough stuff
