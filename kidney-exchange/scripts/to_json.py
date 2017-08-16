import sys
import json

class WmdException(Exception):
    pass

def assert_next_line_contains_minus_ones():
    a, b, c = [int(x) for x in sys.stdin.readline().strip().split()]
    if not a==b==c==-1:
        raise WmdException("Missing line of -1s")

if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
    print "Convert .wmd from standard input to combined .input and .ndds format."
else:
    n_pairs, m1 = [int(x) for x in sys.stdin.readline().strip().split()]
    edges_from_pairs = [[] for i in range(n_pairs)]
    for i in range(m1):
        src, tgt, wt = [int(x) for x in sys.stdin.readline().strip().split()]
        edges_from_pairs[src].append(tgt)

    assert_next_line_contains_minus_ones()

    n_ndds, m2 = [int(x) for x in sys.stdin.readline().strip().split()]
    edges_from_ndds = [[] for i in range(n_ndds)]
    for i in range(m2):
        src, tgt, wt = [int(x) for x in sys.stdin.readline().strip().split()]
        edges_from_ndds[src].append(tgt)

    assert_next_line_contains_minus_ones()

    pair_id = [i+1 for i in range(n_pairs)]
    ndd_id = [i+100001 for i in range(n_ndds)]

    pair_data = {str(pair_id[i]):
            {"sources": [pair_id[i]],
                "dage": 50,
                "matches": [{"recipient": pair_id[tgt], "score": 1} for tgt in edges_from_pairs[i]]}
            for i in range(n_pairs)}
    ndd_data = {str(ndd_id[i]):
            {"altruistic": True,
                "dage": 50,
                "matches": [{"recipient": pair_id[tgt], "score": 1} for tgt in edges_from_ndds[i]]}
            for i in range(n_ndds)}

    all_data = {}
    all_data.update(pair_data)
    all_data.update(ndd_data)
    for k, v in all_data.items():
        if not v["matches"]:
            del v["matches"]
    
    print json.dumps({"data": all_data})
