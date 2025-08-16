import networkx as nx
def euler(G, v):
  while G[v]:
    u = next(iter(G[v]))
    G.remove_edge(u, v)
    yield from euler(G, u)
  yield v

G = nx.Graph()
e = "ab ag bc be bg cd de ef eg fh hg"
for u, v in e.split():
  G.add_edge(u, v)

print(" ".join(list(euler(G, "a"))))
