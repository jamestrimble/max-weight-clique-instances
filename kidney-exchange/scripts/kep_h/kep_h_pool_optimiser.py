import sys
import random
import optimality_criteria

class OptimisationException(Exception):
    pass

class PoolOptimiser(object):
    EPSILON = 1e-7

    def __init__(self, pool, opt_criteria, max_cycle, max_chain):
        self.opt_criteria = opt_criteria
        self.pool = pool
        self.cycles = pool.find_cycles(max_cycle)
        self.chains = pool.find_chains(max_chain)

    def add_clique(self, adj_mat, node_ids):
        for i in range(len(node_ids) - 1):
            for j in range(i+1, len(node_ids)):
                x = node_ids[i]
                y = node_ids[j]
                adj_mat[x][y] = True
                adj_mat[y][x] = True

    def calc_hier_score(self, item, bit_shifts, score_accessor):
        val = 0
        for oc, bit_shift in zip(self.opt_criteria, bit_shifts):
            assert oc.sense == 'MAX'
            if isinstance(oc, optimality_criteria.MaxWeight):
                val += int(round(score_accessor(oc, item) * 100000))
            else:
                val += int(round(score_accessor(oc, item)))
            val <<= bit_shift
        return val

    def solve(self, invert_edges, node_order, bit_shifts):
        # param node_order: 0=default, 1=random, 2=score ascending, 3=score descending
        #                   4=degree asc., 5=degree desc.
        
        print "c Node order {}".format(node_order)
        print "c Bit shifts {}".format(":".join(str(s) for s in bit_shifts[:-1]))

        patients = self.pool.patients
        paired_donors = self.pool.paired_donors
        altruists = self.pool.altruists

#        for c in self.cycles:
#            print c.index, "   ", " ".join(str(pdp.patient.index) for pdp in c.pd_pairs)

        chain_node_ids = range(len(self.chains))
        cycle_node_ids = [len(chain_node_ids) + i for i in range(len(self.cycles))]
        unused_ndd_node_ids = [len(chain_node_ids) + len(cycle_node_ids) + i for i in range(len(altruists))]
        num_nodes = len(chain_node_ids) + len(cycle_node_ids) + len(unused_ndd_node_ids)
        #print chain_node_ids
        #print cycle_node_ids
        #print unused_ndd_node_ids

        # We'll use "node" to denote a vertex in our MWIS instance
        # Nodes have zero-based indices, but we'll print them out using 1-based indexing
        patient_to_nodes = {patient: [] for patient in patients}
        paired_donor_to_node = {donor: [] for donor in paired_donors}
        ndd_to_node = {ndd: [] for ndd in altruists}

        # Each element of hier_scores will be the full hierarchy of scores for a node, compressed
        # into a single int
        hier_scores = [0] * num_nodes

        descriptions = [] # A description of each node, for printing in the comments

        for c, node_id in zip(self.chains, chain_node_ids):
            for pd_pair in c.pd_pairs:
                patient_to_nodes[pd_pair.patient].append(node_id)
                paired_donor_to_node[pd_pair.donor].append(node_id)
            ndd_to_node[c.altruist_edge.altruist].append(node_id)
            hier_scores[node_id] = self.calc_hier_score(
                    c, bit_shifts, lambda oc, c: oc.chain_val(c))
            descriptions.append("{} {}".format(
                    c.altruist_edge.altruist.nhs_id,
                    " ".join("({},{})".format(pd_pair.patient.nhs_id, pd_pair.donor.nhs_id)
                                              for pd_pair in c.pd_pairs)))

        for c, node_id in zip(self.cycles, cycle_node_ids):
            for pd_pair in c.pd_pairs:
                patient_to_nodes[pd_pair.patient].append(node_id)
                paired_donor_to_node[pd_pair.donor].append(node_id)
            hier_scores[node_id] = self.calc_hier_score(
                    c, bit_shifts, lambda oc, c: oc.cycle_val(c))
            descriptions.append(" ".join("({},{})".format(
                    pd_pair.patient.nhs_id, pd_pair.donor.nhs_id) for pd_pair in c.pd_pairs))

        for ndd, node_id in zip(altruists, unused_ndd_node_ids):
            ndd_to_node[ndd].append(node_id)
            hier_scores[node_id] = self.calc_hier_score(
                    ndd, bit_shifts, lambda oc, ndd: oc.altruist_val(ndd))
            descriptions.append(str(ndd.nhs_id))

        adj_mat = [[False]*num_nodes for i in range(num_nodes)]
        
        for d in [patient_to_nodes, paired_donor_to_node, ndd_to_node]:
            for key, val in d.iteritems():
                self.add_clique(adj_mat, val)

        if node_order in [1, 2, 3, 4, 5]:
            if node_order == 1:
                order = range(num_nodes)
                random.shuffle(order)
            elif node_order == 2:
                order = sorted(range(num_nodes), key=lambda i: hier_scores[i])
            elif node_order == 3:
                order = sorted(range(num_nodes), key=lambda i: hier_scores[i], reverse=True)
            elif node_order == 4:
                order = sorted(range(num_nodes), key=lambda i: sum(adj_mat[i]))
            elif node_order == 5:
                order = sorted(range(num_nodes), key=lambda i: sum(adj_mat[i]), reverse=True)
            hier_scores = [hier_scores[i] for i in order]
            adj_mat = [[adj_mat[i][j] for j in order] for i in order]
            descriptions = [descriptions[i] for i in order]

        if num_nodes < 30:
            print "c Adjacency matrix"
            for row in adj_mat:
                print "c " + " ".join("X" if x else "." for x in row)

        for i, desc in enumerate(descriptions):
            print "c {} {}".format(i+1, desc)

        if invert_edges:
            print "p edge {} {}".format(num_nodes,
                (num_nodes*num_nodes - num_nodes) / 2 - sum(sum(row) for row in adj_mat) / 2)
        else:
            print "p edge {} {}".format(num_nodes, sum(sum(row) for row in adj_mat) / 2)

        for i in range(num_nodes-1):
            for j in range(i+1, num_nodes):
                edge_exists = adj_mat[i][j]
                if invert_edges:
                    edge_exists = not edge_exists
                if edge_exists:
                    print "e", i+1, j+1

        for i, score in enumerate(hier_scores):
            print "n", i+1, score

