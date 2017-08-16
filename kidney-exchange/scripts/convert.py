# This is from github.com/jamestrimble/kidney_solver

import sys

class WmdException(Exception):
    pass

if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
    print "Convert .wmd from standard input to combined .input and .ndds format."
else:
    n, m = [int(x) for x in sys.stdin.readline().split(",")]

    n_pairs = 0
    n_ndds = 0

    for i in range(n):
        s = sys.stdin.readline()
        if "Pair" in s:
            if n_ndds > 0:
                raise WmdException("Didn't expect a pair to appear after NDDs")
            n_pairs += 1
        else:
            n_ndds += 1


    pair_edges = [[] for _ in range(n_pairs)]
    ndd_edges = [[] for _ in range(n_ndds)]

    for i in range(m):
        src, tgt, wt = [int(x) for x in sys.stdin.readline().split(",")]
        if tgt < n_pairs:   # Discard edges to NDDs
            if src < n_pairs:
                pair_edges[src].append((tgt, wt))
            else:
                ndd_edges[src-n_pairs].append((tgt, wt))

    def write(n_agents, edges):
        n_edges = len([e for l in edges for e in l])
        print "{}\t{}".format(n_agents, n_edges)
        for i in range(n_agents):
            for edge in edges[i]:
                print "{}\t{}\t{}".format(i, edge[0], edge[1])
        print "-1\t-1\t-1"

    write(n_pairs, pair_edges)
    write(n_ndds, ndd_edges)
