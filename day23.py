from collections import defaultdict
import re 

def bron_kerbosch(graph, r=set(), p=None, x=set()):
    if p is None:
        p = set(graph.keys())

    if not p and not x:
        yield r
    else:
        u = next(iter(p | x))  # Choose a pivot vertex
        for v in p - graph[u]:
            yield from bron_kerbosch(graph, r | {v}, p & graph[v], x & graph[v])
            p.remove(v)
            x.add(v)

def find_largest_complete_subgraph(graph):
    cliques = list(bron_kerbosch(graph))
    return max(cliques, key=len)

m = re.compile(r"(..)-(..)")

mapping = defaultdict(set)

with open("inputs/day23.txt") as f:
    for l in f: 
        (g1,g2) = m.match(l.strip()).groups()
        mapping[g1].add(g2)
        mapping[g2].add(g1)

sets = set()
networks = []
for k,v in mapping.items():
    if len(v) < 2:
        continue

    p = list(v)
    for (i,p1) in enumerate(p):
        for p2 in p[i+1:]:
            if p1 == p2 or p1 == k or p2 == k:
                continue

            if p2 in mapping[p1]: 
                connections = [k,p1,p2]
                connections.sort()
                sets.add(tuple(connections))
 


def has_t(connections: tuple[str,str,str]) -> bool:
    if connections[0][0] == 't':
        return True 

    if connections[1][0] == 't':
        return True
    
    if connections[2][0] == 't':
        return True
    
    return False

filtered = [s for s in sets if has_t(s)]
print(len(filtered))

n = list(find_largest_complete_subgraph(mapping))
n.sort()
print(",".join(n))

