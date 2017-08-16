import argparse
import sys
import json
from kep_h_pool import *
from optimality_criteria import *
from kep_h_pool_optimiser import PoolOptimiser
import pool_reader

def parse_shifts(input):
    return [int(s) for s in input.split(":")] + [0]

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Hierarchical kidney-exchange optimisation")
    parser.add_argument("-f", "--file", help="Input file name", type=str,
                        required=True)
    parser.add_argument("-c", "--criteria",
                        help="A colon-separated list of optimality criteria," +
                             "such as effective:size:3way:backarc:weight",
                        type=str,
                        required=True)
    parser.add_argument("-s", "--shifts",
                        help="A colon-separated list of bit-shifts" +
                             " specifying the width in bits of the last n-1 criterion-scores" +
                             " such as 7:6:7:36",
                        type=str,
                        required=True)
    parser.add_argument("-e", "--cycle",
                        help="Maximum cycle length",
                        type=int,
                        required=True)
    parser.add_argument("-n", "--chain",
                        help="Maximum chain length",
                        type=int,
                        required=True)
    parser.add_argument("-o", "--node-order",
                        help="Node order (0=default, 1=random, 2=score asc., 3=score desc., " +
                             "4=degree asc., 5=degree desc.)",
                        type=int,
                        default=0)
    parser.add_argument("-r", "--reduce-nodes",
                        help="Remove some nodes that can't be part of a solution",
                        action='store_true') 
    parser.add_argument("-i", "--invert-edges",
                        help="Create complement graph",
                        action='store_true') 
    args = parser.parse_args()

    opt_criteria = get_criteria(args.criteria)
    shifts = parse_shifts(args.shifts)

    if not args.file.endswith(".json"):
        print "Input file must be in JSON format"
    elif len(opt_criteria) != len(shifts):
        print "Length of shifts must be one less than length of optimality criteria."
    else:
        with open(args.file) as json_file:
            pool = pool_reader.read(json.load(json_file)["data"])
            pool_optimiser = PoolOptimiser(pool, opt_criteria, args.cycle, args.chain)
            pool_optimiser.solve(args.invert_edges, args.node_order, shifts)
