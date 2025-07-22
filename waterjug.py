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
