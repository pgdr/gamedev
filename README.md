---
documentclass: memoir
fontsize: 14pt
title: Introduction to Graph Theory for Gamedevs
author: Pål Grønås Drange
date: Summer 2025
papersize:
  - a4
header-includes:
  - \usepackage{microtype}
  - \usepackage{newpx}
  - \usepackage{tcolorbox}
  - \usepackage{froufrou}
abstract: |

    This pamphlet serves two purposes.

    1. Introduce graph theory to teach concepts and graph structures for game
       developers, both programmers and artistic creators. This also entails
       the explanation of some algorithms, although all algorithms mentioned
       herein are relatively simple.

    2. Through structures, models, and problems from graph theory, inspire game
       creators about possible games, puzzles, and AI strategies. It may also
       explain what makes certain graph problems easy or hard.

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

In fact, since BFS (and as we will later see, Dijkstra's algorithm) finds the
shortest path from a specific _source_ to all other vertices (unless
specifically aborted once we reach our target, of course), we sometimes refer
to this problem as \textsc{Single Source Shortest Path}, or SSSP for short.



### Flood Filling

Flood filling algorithms can simulate water flooding on discrete 2D surfaces
embedded in 3D environments.  Imagine water pouring onto a terrain from a
specific aquifer point: the water naturally spreads outward, filling
neighboring lower or equal-height cells before progressively rising to higher
elevations.  Using BFS, the simulation accurately captures this spreading
behavior, incrementally marking cells as flooded while respecting the terrain's
topography.

By iteratively expanding the flooded region from the initial aquifer location,
developers can realistically model scenarios like rising water levels, dynamic
river flows, or inundation puzzles.  Such simulations not only enhance visual
realism but also open up compelling gameplay mechanics where players must
strategically manipulate terrain or barriers to direct water flow, protect
certain regions, or solve environmental puzzles involving flooding.




### Weighted graphs

When the "cost" of moving from one "cell" to another is not the same
everywhere; for example running in water or running uphill can be more
expensive, we need an algorithm that can deal with these costs.  BFS can
unfortunately not.

Dijkstra's algorithm is an SSSP (single source shortest path) algorithm that
works similarly to BFS, but instead
of a queue that we iterate through, we have a _priority queue_.  A priority
queue is a queue in which the First In First Out is replaced with "Most
Important Out".  That is, the order of insertion is irrelevant; when we pop
from the queue, we pop the one with highest priority (typically this is the one
with _lowest possible value_).

```python
import heapq

def dijkstra(G, s):
  dist = D(lambda: INF)  # distance from source
  visited = D(bool)      # visited = False
  dist[source] = 0       # starting point
  queue = [(0, source)]

  while queue:
    dv, v = heappop(queue)
    if dist[v] <= dv:
      continue

    for u in neighbors[v]:
      if dist[u] > dv + w(v, u)
        dist[u] = dv + w(v, u)
        heappush(queue, (dist[u], u)
```


## Puzzle Solving

It is not only in the literal sense that path finding algorithms are useful.
Consider Rubik's Cube, the 15-puzzle, or the classic Die Hard puzzle of filling
a 5 liter bucket with 4 liters of water using only 3 and 5 liter buckets.


### Water Jug Problem

Suppose, we want to help MacClane with his task of putting 4 liters of water in a 5 liter bucket using only one 3 and one 5 liter buckets.
Construct an abstract "state
space graph" where you have the node set as $(c_3, c_5)$ where $c_3 \in \{0, 1,
2, 3\}$ and $c_5 \in \{0, 1, 2, 3, 4, 5\}$.  Suppose that you have $c_3$ liters
of water in the small bucket and $c_5$ liters of water in the large bucket.
What can you do?  Fill one of them, i.e., the next states are $(3, c_5)$ or
$(c_3, 5)$.  Alternatively, you can empty one of them, i.e., the next states
are $(0, c_5$) or $(c_3, 0)$.  Finally, you can pour from one to the other
until either pourer becomes empty or the pouree becomes full: $(\max(c_5 - c_3,
0), \min(c_5 + c_3, 5))$, or the other way around.  How do we go from $(0,0)$ to
$(0, 4)$?  Simply run `bfs(G, (0,0))`.

\clearpage

```python
from collections import deque, namedtuple

def bfs(s):
  visited = set()
  dist = {s: 0}
  parent = {s: None}
  queue = deque([s])
  while queue:
    u = queue.popleft()
    for v in next_state(u):
      if v not in visited:
        visited.add(v)
        dist[v] = dist[u] + 1
        parent[v] = u
        queue.append(v)
  return dist, parent

Jugs = namedtuple("Jugs", "b3 b5")
START = Jugs(0, 0)
GOAL = Jugs(0, 4)

def next_state(state):
  yield Jugs(0, state.b5)
  yield Jugs(state.b3, 0)
  yield Jugs(3, state.b5)
  yield Jugs(state.b3, 5)
  yield Jugs(max(state.b3 - (5 - state.b5), 0),
             min(5, state.b3 + state.b5))
  yield Jugs(min(3, state.b3 + state.b5),
             max(state.b5 - (3 - state.b3), 0))

def is_goal(state):
  return state == GOAL

dist, parent = bfs(START)
current = GOAL
solution = [GOAL]
while (current := parent[current]) != START:
  solution.append(current)
solution.append(START)
for step, state in enumerate(reversed(solution)):
  print((1 + step), state)
```

\clearpage

The above code solves the Water Jug Problem and will print the steps needed to
take to achieve the solution.

```
1 Jugs(b3=0, b5=0)
2 Jugs(b3=0, b5=5)
3 Jugs(b3=3, b5=2)
4 Jugs(b3=0, b5=2)
5 Jugs(b3=2, b5=0)
6 Jugs(b3=2, b5=5)
7 Jugs(b3=3, b5=4)
8 Jugs(b3=0, b5=4)
```

### Other Puzzles

The 15-puzzle and the Rubik's cube are other examples of games where we can
represent the state space as a graph and use a search algorithm for finding the
shortest path.

### Exercise: Wolf, Goat, and Cabbage

The Wolf, Goat, and Cabbage problem is a classic river-crossing puzzle.  In
this scenario, a farmer needs to cross a river with a wolf, a goat, and a
cabbage.  The farmer has a small boat that can only carry himself and one of
the three items at a time.  The challenge lies in ensuring that the wolf does
not eat the goat when left alone together and the goat does not eat the cabbage
under the same conditions.  Here are the rules:

1. The farmer can take only one item at a time across the river.
2. If left alone, the wolf will eat the goat, and the goat will eat the cabbage.
3. The goal is to transport all three items across the river without any of them being eaten.

Using a similar approach as the Water Jug Problem, represent the state of the
game as a graph.  Define the states using a triplet notation $(F, W, G, C)$
where these take values 0 and 1, meaning start or opposite side:

- $F$ is the farmer's location (0 or 1)
- $W$ is the wolf's location (0 or 1)
- $G$ is the goat's location (0 or 1)
- $C$ is the cabbage's location (0 or 1)

Once you have your implementation, demonstrate that you can reach the goal
state $(1, 1, 1, 1)$ starting from $(0, 0, 0, 0)$ and list the steps taken to
do so.



## Informed Search

Dijkstra's algorithm works well for graphs with non-negative distances, but in
some cases, it explores an excessively large part of the graph.  We will now
look at an algorithm called $A^*$ that uses a _heuristic_ to "steer" the
direction of the search.  It is simply Dijkstra's algorithm, but with a small
estimation of remaining distance.  However, contrary to Dijkstra's algorithm,
we necessarily terminate when we discover $t$, so this is _not_ an SSSP.

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

Graphs with negative edge weights introduce new complexities into pathfinding
algorithms.  While typical graph traversal problems---like roads or
paths---naturally have non-negative weights (distance, cost, or time), negative
weights can represent scenarios like energy regeneration in electric vehicles
traveling downhill.  Here, the EV actually gains energy, making the edge weight
negative.  This fundamentally alters the nature of shortest-path calculations.

Algorithms like Dijkstra's, which rely on non-negative edge weights, fail to
handle negative distances correctly because they assume that visiting a node
once guarantees the shortest path to it.  With negative edges, previously
computed paths may need constant revising, potentially leading to incorrect
results.  Thus, we require specialized algorithms such as the Bellman--Ford or
Johnson's algorithms that can accommodate negative weights and correctly
compute shortest paths even when negative cycles are present.

Interestingly, negative cycles---loops with a negative total weight---can
themselves become part of the gameplay mechanics.  For instance, players might
exploit negative cycles strategically to replenish energy or accumulate
resources, introducing intriguing tactical considerations into game design.

```python
def floyd_warshall(G):
  dist = [[INFTY for _ in range(n)] for _ in range(n)]
  for u in nodes:
    dist[u][u] = 0
    for v, w in G[u]:
      dist[u][v] = w
      next_node[u][v] = v

  for k in nodes:
    for i in nodes:
      for j in nodes:
        if dist[i][k] + dist[k][j] < dist[i][j]:
          dist[i][j] = dist[i][k] + dist[k][j]
          next_node[i][j] = next_node[i][k]

  for u in nodes:
    if dist[u][u] < 0:
      raise ValueError("Graph contains a negative-weight cycle")

  return dist, next_node
```


Alternatively, 

```python
def bellman_ford(G, s):
  dist = {v: float("inf") for v in G}
  dist[s] = 0
  parent = {v: None for v in G}
  n = len(G)

  # Relax edges up to n-1 times
  for _ in range(n - 1):
    updated = False
    for u in G:
      for v, w in G[u]:
        if dist[u] + w < dist[v]:
          dist[v] = dist[u] + w
          parent[v] = u
          updated = True
    if not updated:
      break

  # Check for negative-weight cycles
  for u in G:
    for v, w in G[u]:
      if dist[u] + w < dist[v]:
        raise ValueError("Graph contains a negative-weight cycle")

  return dist, parent
```

## Bidirectional search

We saw that BFS can be used to solve puzzles such as the *Wolf, Goat, and
Cabbage* problem and the *Water Jug* problem.  However, the nodes explored
grows exponentially in the depth; If the *branching factor* is $b$ and the
_distance_ from the start to the goal is $d$, the total number of nodes
explored is $d^b$.

There is a way to drastically reduce the number of explored nodes, however.
Imagine that the search is a circle, and the number of nodes explored is the
_area_ of the circle.  Then the area is $\pi d^2$, where $d$ is distance from
start to goal.  If we *instead* search from the start node and the goal node
*simultaneously*, and abort the search once the two searches intersect, you can
visualize this as _two circles_ with radius $d/2$.  The area of two circles
with half the radius is much smaller than the area of one large circle with the
full radius (by quadratic order).

The same reasoning holds in our case, but where the quadratic improvement
becomes a (potentially) exponential improvement.  If the (and this is a **big
if**) _branching factor_ is the same in both directions, then we expore $2
(d/2)^b$ nodes instead, which is $2 \frac{d^b}{2^b}$, i.e., it shaves off an
exponential fraction.

\paragraph{Reverse branching factor.}  So what is the _reverse branching
factor_ for different cases?  In the *Rubik's cube* problem, it is the same if
we go back or forth.  In each state we have 12 possible move, and it doesn't
matter if we go forwards or backwards; if we want to move from the goal state
to the start state, we have the same possible moves.  The same holds for the
*15-puzzle* problem.  In each case, we can move the blank N/S/E/W, i.e., the
branching factor is 4 both forwards and backwards.  Also in (undirected) graph
searching, the backwards is the same as the forwards; It is the _degree_ of the
vertex $\deg(v)$.

However, for the Water-Jug problem the approach breaks down.  Suppose that you
are in a state, e.g. $(0,0)$.  In the forwards direction we have 6 potential
moves always.  However, in the reverse direction, we must ask: *where did we
come from* to reach $(0,0)$.  And it turns out that there are many more
possibilities: the previous *move* could have been to empty the first jug.
However, then the previous state could have been any of $(k, 0)$ for $1 \leq k
\leq 5$.  The same for the second jug, $(0,k)$.  The problem becomes much worse
if we say that the capacities for the jugs are, say, 17 and 43.  In the
forwards direction we still only have 6 possibilities:

$$ a\to 0\quad b\to 0\quad a\to b\quad b\to a\quad \infty \to a\quad \infty \to b. $$

\paragraph{Exercise:} How many moves does it take to get to state `Jugs(b17=0,
b43=4)` if your bottles are of capacities 17 and 43.  How many nodes are
explored in BFS versus bidirectional search?

\paragraph{Exercise:} Implement bidirectional search for the 15 puzzle.
Compare the number of explored nodes with $A^*$.

\paragraph{Exercise:} Suppose you are at $x$ and $y$.  Your potential moves are
always $(x+y, x)$ and $(y, x+y)$.  Write an algorithm for finding out if there
is a path from $(1,1)$ to $(a,b)$.





## Future Reading

* Problems
  * Randomly pick $\sqrt n$ nodes $P$ as _portals_ (keyword: transit nodes,
    distance oracle, highways) and compute the APSP for $P$.
  * Distance oracle for planar graphs
  * APSP
* Algorithms
  * Bidirectional search
  * Johnson's algorithm


# Global Navigation

In the previous chapter, we saw problems where we wanted to find a path
from one node in a graph to another, i.e., the fewest number of edges to
connect one vertex to another.  All of the problems in the previous
chapter are "easy", in the sense that they have an "efficient
algorithm".  An _efficient algorithm_ is something we have defined to be
an algorithm with a _polynomial running time_.  We will in this chapter
see some problems that don't necessarily have such efficient
algorithms.

We mentioned that the shortest path is the problem of finding the fewest
possible number of edges connecting $A$ to $B$.  What about the
following: consider a road network where in each node, there is a house,
except in one node, there is a power station.  You want to put up
electric wires along (some of) the roads so that every house is
connected to the power station, and you want to use as little wiring as
possible.  In other words: find the fewest possible number of roads such
that _all nodes_ are connected.  Surprisingly, perhaps, this problem has
an efficient algorithm.

## Trees In Our Graphs

The aforementioned problem is called \textsc{Minimum Spanning Tree} (MST).
You are given a graph, preferably with weights, and you want to find a
_spanning tree_ in the graph, that is a _tree_ that contains all edges.
And out of all possible spanning trees, you want to find one which is as
cheap as possible.  There are two famous algorithms for this problem,
Prim's algorithm, which is Dijkstra's algorithm with simply this
modification.

```diff
15,16c15,16
<       if dist[u] > dv + w(v, u)
<         dist[u] = dv + w(v, u)
---
>       if dist[u] > w(v, u)
>         dist[u] = w(v, u)
```

Hence, we will focus on _Kruskal's algorithm_ for computing a _minimum
spanning tree_, because it introduces a very nifty data structure:
Union--Find.


```python
def find(u):
  if comp[u] == u:
    return u
  else:
    parent = find(u)
    comp[u] = parent  # "memoize"
    return parent

def union(u, v):
  r1 = find(u)
  r2 = find(v)
  comp[r1] = r2
```

## Steiner Tree: Non-Full Spanning Trees

We now come to the first problem in this pamphlet that we cannot see a
polynomial time algorithm for, even though ... in a sense ... it sounds simpler
than the previous problem.

Suppose you have the same road network as above, with a power station and
houses, but now not every node is a house, there are just houses in some of the
nodes.  Meaning that you have _fewer_ houses than before.  The problem,
however, is the same: Find the minimum network (in terms of electric cabling)
possible that connects all houses to the power station.


## Travelling Sale

If you are standing on a location $A$ and want to reach a location $B$, we know
what to do; shortest path.  However, what if you want to visit not one but two
locations?  Well, either $ABC$ or $ACB$.  What if three locations?  Well,
either one of $ABCD, ABDC, ACBD, ACDB, ADBC, ADCB$.  This set doesn't only grow
_exponentially_, it grows _super-exponentially_: Like $n^n$, which is something
like $n^{\log_2 n}$.

There is, however, an algorithm that solves the problem in time $2^nn^2$.


### Hamiltonian Path

### Travelling Salesman

### Longest Path

In \textsc{Ticket 2 Ride}, the winning criterion is who has built the longest path.
This is in fact an NP-hard problem!  The game developers ask us to, after the game has been completed, to solve a problem known to need exponential time!  The audacity ...


## Euler Tour, or: Bridges of Königsberg

A problem very similar to the Hamiltonian Cycle problem is: What if you don't
visit every _node_ exactly once, but ever _edge_ exactly once.  Surprisingly,
this is solvable with a trivial check.  Graph theory was invented in 1736 when
mathematician Leonhard Euler presented the solution to the famous problem of
the seven bridges of Königsberg.

Arranging domino tiles can be modeled by an Eulerian path, where each tile
represents an edge and each face value corresponds to a vertex in the graph.
To successfully create a continuous path using the tiles, one must ensure that
the graph formed by the dominoes adheres to specific conditions: either all
vertices have an even degree, allowing for a closed loop, or exactly two
vertices have an odd degree, permitting a path.

This concept extends beyond dominoes into various game mechanics, such as
drawing a figure without lifting your pencil from the paper.

Yet a third game possibility: In each hallway there is a door and once you pass
through a door you get a bucket of gold and the door closes shut forever (with
you on the other side).  Can you collect all the gold?


### The algorithms:

Two cases: Either you start and end in the same node.  Then you enter and exit
each vertex the same number of times, hence check all degrees are even.

Or you start and end in different nodes: Exactly two nodes have odd degree.

That's it.

```python

def euler(G, v):
  while G[v]:
    u = G[v][0]
    G.remove(u, v)
    euler(G, u)
    yield v

```


# Cutting and Flowing

In this chapter, we will discuss a fundamental graph theory concept.

Let $G = (V, E, c)$ be a _weighted and directed_ graph, where $c: E \to
\mathbb{N}$ denotes the _capacity_ of each edge, whatever capacity means.  In
this section, we will refer to $(G, s, t)$ as a _flow network_, and to confuse
us a bit, we will compute the _network flow_ of the given _flow network_.

Intuitively, the _flow_ of a network is easy to understand.  Suppose that you
put a garden hose with _infinite_ water pressure and stick it into $s$, and you
see poke a hole in $t$, to see how much water comes out of $t$ (per time unit).

If the capacity of an edge $e = (u,v)$ is $c(e) = 3$, that means that $3$ units
of flow per time unit can go through $e$.  For simplicity: $3$ liters of waters
per second, i.e., $c(e) \ell/s$.  How many $\ell/s$ comes out of $t$?  This is
the \textsc{Maximum Flow} problem.

\begin{tcolorbox}[title=Theory]

Menger's theorem says that the number of disjoint paths from $s$ to $t$ is
equal to the number of edges we have to remove to cut $s$ from $t$.

\end{tcolorbox}

## Minimum Cut

Suppose you have a tower defense like game, where the enemy sends units from
some source towards your castle in an intricate road network.  You can put up
turrets that kill all enemies passing a certain point in the road network.
Where should you put turrets so that no enemy unit can reach your castle?
Here we can also add different costs to the turrets positions (e.g. it's
expensive on grass and cheap on gravel).
This problem is called the \textsc{Minimum $s$-$t$-Cut} problem.

Let $G = (V, E)$ be a graph and $s$ and $t$ two vertices.  Which edges should
you remove from the graph such that you disconnect $s$ from $t$?

Menger's theorem, and the so-called Max Flow--Min Cut theorem states that the
maximum $s$-$t$-flow value is exactly the same as the minimum $s$-$t$-cut
value, and we can find the cut by running and algorithm for maximum flow.

The algorithm is quite simple, but at the same time not very intuitive.  We are
not diving into the reason why it works here, but just state that a simple
greedy approach does not work, but that what is needed is to construct a
_residual graph_ that we actually can run a greedy-ish algorithm on.  The
entire algorithm can be summarized in these few lines:

```python
def maxflow(graph, s, t):
  flow = 0
  while P := bfs(graph, s, t):
    bottleneck = min(graph.F[v][u] for (v, u) in edges(P))
    print(P, bottleneck)
    if bottleneck == 0:
      return flow
    flow += bottleneck
    for i in range(1, len(P)):
      v, u = P[i - 1], P[i]
      graph.F[v][u] -= bottleneck
      graph.F[u][v] += bottleneck
  return flow
```

If we run the above algorithm on our Tower Defense graph, and then run a BFS
from $s$ in the remaining graph, we will get the left hand side of the minimum
cut; Simply place turrets on all edges that leave this set; this will be
optimal, even in the weighted setting.

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


# What Now?

In this final chapter, we see some things that we didn't get to cover due to
space or scope, but that nevertheless might be interesting to be aware of.

## Dynamic Graphs

Dynamic graphs extend the static model by allowing changes to the graph
structure over time, including the addition or removal of vertices and edges.
This characteristic is crucial for modeling real-world scenarios such as social
networks, traffic systems, and game environments, where the relationships
between entities evolve.

Traditional algorithms designed for static graphs often struggle in these
settings, as their assumptions about fixed structures can lead to
inefficiencies or inaccuracies when applied to dynamic data.  As a result,
dynamic graph algorithms must adapt to continually accommodate updates,
enabling developers to maintain performance while responding to fluid gaming
environments.


## Online Algorithms

Online algorithms are essential for scenarios where data arrives in a
sequential manner, and decisions must be made without knowledge of future
input.  This is particularly relevant in gaming, where an AI may need to
respond to player actions in real-time without the luxury of hindsight.  These
algorithms process information on the fly, making greedy choices based on the
current state of the game.  While such strategies can yield efficient results,
they often cannot guarantee optimal solutions; however, they can provide
acceptable approximations quickly.

Understanding the principles behind online algorithms allows game developers to
create more responsive and engaging gaming experiences, as they can design
systems that treat each player interaction as a new opportunity to adjust
strategies dynamically.


# Notes

\pagebreak

\phantom{page intentionally left blank}

\pagebreak

\phantom{page intentionally left blank}


\pagebreak

\phantom{page intentionally left blank}


\pagebreak

\phantom{page intentionally left blank}
