# FIXME: add more checks and make this less hacky

import argparse
import sys
import json
from kep_h_pool import *
from optimality_criteria import *
import pool_reader

def find_ndd(pool, nhs_id):
    for ndd in pool.altruists:
        if ndd.nhs_id == nhs_id:
            return ndd

def find_patient(pool, nhs_id):
    for patient in pool.patients:
        if patient.nhs_id == nhs_id:
            return patient

def find_paired_donor(pool, nhs_id):
    for donor in pool.paired_donors:
        if donor.nhs_id == nhs_id:
            return donor

def find_pair(pool, token):
    comma_pos = token.find(",")
    patient_id = int(token[1:comma_pos])
    donor_id = int(token[comma_pos+1:-1])
    patient = find_patient(pool, patient_id)
    donor = find_paired_donor(pool, donor_id)
    return PatientDonorPair(patient, donor)

def ndd_has_edge_to_patient(ndd, patient):
    for edge in ndd.edges:
        if edge.target_patient == patient:
            return True
    return False

def check_chain(pool, tokens):
    ndd = find_ndd(pool, int(tokens[2]))
    pairs = [find_pair(pool, token) for token in tokens[3:]]
    n_backarcs = 1 if len(pairs)==2 else 0
    if ndd_has_edge_to_patient(ndd, pairs[-1].patient) and len(pairs)==2:
        n_backarcs += 1
    assert ndd_has_edge_to_patient(ndd, pairs[0].patient)
    for i in range(1,len(pairs)):
        pair1 = pairs[i-1]
        pair2 = pairs[i]
        assert pair1.donor.has_edge_to(pair2.patient)
        if pair2.donor.has_edge_to(pair1.patient) and len(pairs)==2:
            n_backarcs += 1
    print tokens[1], n_backarcs
    c = Chain(AltruistEdge(ndd, pairs[0].patient, 0), pairs, -1)
    print len(pairs), c.n_backarcs(), n_backarcs
    assert c.n_backarcs() == n_backarcs
    return n_backarcs

def check_cycle(pool, tokens):
    n_backarcs = 0
    pairs = [find_pair(pool, token) for token in tokens[2:]]
    for i in range(len(pairs)):
        pair1 = pairs[i-1]
        pair2 = pairs[i]
        assert pair1.donor.has_edge_to(pair2.patient)
        if pair2.donor.has_edge_to(pair1.patient) and len(pairs)==3:
            n_backarcs += 1
    print tokens[1], n_backarcs
    c = Cycle(pairs, -1)
    print len(pairs), c.n_backarcs(), n_backarcs
    assert c.n_backarcs() == n_backarcs
    return n_backarcs

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Hierarchical kidney-exchange optimisation")
    parser.add_argument("-f", "--file", help="Input file name", type=str,
                        required=True)
    args = parser.parse_args()

    if args.file.endswith(".json"):
        with open(args.file) as json_file:
            pool = pool_reader.read(json.load(json_file)["data"])
    else:
        print "Input file must be in JSON format"

    n_backarcs = 0

    for line in sys.stdin.readlines():
        tokens = line.strip().split()
        if tokens[2].isdigit():
            n_backarcs += check_chain(pool, tokens)
        else:
            n_backarcs += check_cycle(pool, tokens)

    print n_backarcs
