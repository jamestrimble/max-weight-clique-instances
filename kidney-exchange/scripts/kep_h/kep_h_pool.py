from collections import namedtuple

class Pool(object):
    def __init__(self):
        self.patients = []
        self.paired_donors = []
        self.altruists = []

    def associate_patient_with_donor(self, patient, paired_donor):
        patient.paired_donors.append(paired_donor)
        paired_donor.paired_patients.append(patient)

    def find_cycles(self, max_length):
        cycles = []
        for patient in self.patients:
            for donor in patient.paired_donors:
                p_d_pair = PatientDonorPair(patient, donor)
                self._cycle(max_length, [p_d_pair], cycles)
        return cycles

    def _cycle(self, max_length, current_list, cycles):
        last_pd_pair = current_list[-1]
        first_patient = current_list[0].patient
        if last_pd_pair.donor.has_edge_to(first_patient):
            cycles.append(Cycle(current_list[:], len(cycles)+1))
        if len(current_list) < max_length:
            for edge in last_pd_pair.donor.edges_out:
                patient = edge.target_patient
                if patient.index > first_patient.index and not patient.is_in(current_list):
                    for donor in patient.paired_donors:
                        if not donor.is_in(current_list):
                            pd_pair = PatientDonorPair(patient, donor)
                            current_list.append(pd_pair)
                            self._cycle(max_length, current_list, cycles)
                            del current_list[-1]

    def find_chains(self, max_length):
        if max_length==0:
            return []
        chains = []
        for altruist in self.altruists:
            for edge in altruist.edges:
                patient = edge.target_patient
                for paired_donor in patient.paired_donors:
                    pd_pair = PatientDonorPair(patient, paired_donor)
                    self._chain(edge, max_length, [pd_pair], chains)
        return chains

    def _chain(self, altruist_edge, max_length, pd_pairs, chains):
        chains.append(Chain(altruist_edge, pd_pairs[:], len(chains)+1))
        if len(pd_pairs) < max_length:
            for edge in pd_pairs[-1].donor.edges_out:
                patient = edge.target_patient
                if not patient.is_in(pd_pairs):
                    for donor in patient.paired_donors:
                        if not donor.is_in(pd_pairs):
                            pd_pair = PatientDonorPair(patient, donor)
                            pd_pairs.append(pd_pair)
                            self._chain(altruist_edge, max_length, pd_pairs, chains)
                            del pd_pairs[-1]

class Cycle(object):
    def __init__(self, pd_pairs, index):
        self.pd_pairs = pd_pairs
        self.index = index

    def n_transplants(self):
        return len(self.pd_pairs)

    def n_backarcs(self):
        if self.n_transplants() < 3:
            return 0
        n_backarcs_ = 0
        for i in range(len(self.pd_pairs)):
            if self.pd_pairs[i].patient.has_backarc_to(self.pd_pairs[i-1].patient):
                n_backarcs_ += 1
        return n_backarcs_

    def weight(self, weight_fun):
        weight_ = 0
        for i in range(0, len(self.pd_pairs)):
            pair1 = self.pd_pairs[i-1]
            pair2 = self.pd_pairs[i]
            edge = pair1.donor.get_edge_to(pair2.patient)
            weight_ += weight_fun(edge.score, pair1.donor.dage, pair2.donor.dage)
        return weight_

    def __str__(self):
        retval = "["
        for i, pd_pair in enumerate(self.pd_pairs):
            if i>0: 
                retval += " "
            retval += "%d(%d)" % (pd_pair.patient.nhs_id, pd_pair.donor.nhs_id)
        retval += "]"
        return retval

class Chain(object):
    def __init__(self, altruist_edge, pd_pairs, index):
        self.altruist_edge = altruist_edge
        self.pd_pairs = pd_pairs
        self.index = index
    
    def n_transplants(self):
        return len(self.pd_pairs) + 1

    def n_backarcs(self):
        if self.n_transplants() < 3:
            return 0
        n_backarcs_ = 1
        for i in range(1, len(self.pd_pairs)):
            if self.pd_pairs[i].patient.has_backarc_to(self.pd_pairs[i-1].patient):
                n_backarcs_ += 1
        final_patient = self.pd_pairs[-1].patient
        for edge in self.altruist_edge.altruist.edges:
            if edge.target_patient == final_patient:
                n_backarcs_ += 1
                break
        return n_backarcs_

    def __str__(self):
        retval = "[(%d)" % (self.altruist_edge.altruist.nhs_id,)
        for pd_pair in self.pd_pairs:
            retval += " %d(%d)" % (pd_pair.patient.nhs_id, pd_pair.donor.nhs_id)
        retval += "]"
        return retval

    def weight(self, weight_fun):
        weight_ = weight_fun(self.altruist_edge.score, self.altruist_edge.altruist.dage,
                             self.pd_pairs[0].donor.dage)
        for i in range(1, len(self.pd_pairs)):
            pair1 = self.pd_pairs[i-1]
            pair2 = self.pd_pairs[i]
            edge = pair1.donor.get_edge_to(pair2.patient)
            weight_ += weight_fun(edge.score, pair1.donor.dage, pair2.donor.dage)
        return weight_

class Altruist(object):
    def __init__(self, dage, nhs_id):
        self.edges = []
        self.dage = dage
        self.nhs_id = nhs_id

    def __str__(self):
        return "altruist " + str(self.nhs_id)

class AltruistEdge(object):
    def __init__(self, altruist, target_patient, score):
        self.altruist = altruist
        self.target_patient = target_patient
        self.score = score

class PairedDonor(object):
    def __init__(self, dage, nhs_id):
        self.paired_patients = []
        self.edges_out = []
        self.dage = dage
        self.nhs_id = nhs_id

    def is_in(self, pd_pairs):
        "Is this donor in the passed list of patient-donor pairs?"
        for pd_pair in pd_pairs:
            if pd_pair.donor==self:
                return True
        return False

    def has_edge_to(self, patient):
        return self.get_edge_to(patient) is not None

    def get_edge_to(self, patient):
        for edge in self.edges_out:
            if patient == edge.target_patient:
                return edge
        return None

class Patient(object):
    def __init__(self, nhs_id, index):
        self.paired_donors = []
        self.nhs_id = nhs_id
        self.index = index

    def is_in(self, pd_pairs):
        "Is this patient in the passed list of patient-donor pairs?"
        for pd_pair in pd_pairs:
            if pd_pair.patient==self:
                return True
        return False

    def has_backarc_to(self, other_patient):
        for paired_donor in self.paired_donors:
            for edge in paired_donor.edges_out:
                if edge.target_patient == other_patient:
                    return True
        return False

PatientDonorPair = namedtuple('PatientDonorPair', ['patient', 'donor'])

DonorPatientMatch = namedtuple('DonorPatientMatch', ['target_patient', 'score'])

