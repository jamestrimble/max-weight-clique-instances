from kep_h_pool import *

def read(data):
    pool = read_people(data)
    create_pairings_and_edges(data, pool)
    return pool

def read_people(data):
    pool = Pool()

    patient_ids_seen = set()  # The set of IDs of patients who have been created

    for id in data:
        dage = data[id]["dage"]
        is_altruistic = data[id].has_key("altruistic") and data[id]["altruistic"]
        if is_altruistic:
            altruist = Altruist(dage, int(id))
            pool.altruists.append(altruist)
        else:
            paired_donor = PairedDonor(dage, int(id))
            pool.paired_donors.append(paired_donor)
            for patient_id in data[id]["sources"]:
                if patient_id not in patient_ids_seen:
                    patient_ids_seen.add(patient_id)
                    patient = Patient(patient_id, len(pool.patients))
                    pool.patients.append(patient)

    return pool

def create_pairings_and_edges(data, pool):
    id_to_patient = {patient.nhs_id: patient for patient in pool.patients}
    id_to_donor = {donor.nhs_id: donor for donor in pool.paired_donors}
    id_to_altruist = {altruist.nhs_id: altruist for altruist in pool.altruists}

    # Create patient-donor pairs
    for id in data:
        if int(id) in id_to_donor:
            paired_donor = id_to_donor[int(id)]
            for source_id in data[id]["sources"]:
                patient = id_to_patient[source_id]
                pool.associate_patient_with_donor(patient, paired_donor)
        
    # Create edges from altruists and edges between patient-donor pairs
    for id in data:
        if int(id) in id_to_donor and data[id].has_key("matches"):
            paired_donor = id_to_donor[int(id)]
            for match in data[id]["matches"]:
                patient = id_to_patient[match["recipient"]]
                score = match["score"]
                dp_match = DonorPatientMatch(patient, score)
                paired_donor.edges_out.append(dp_match)
        
        elif int(id) in id_to_altruist:
            altruist = id_to_altruist[int(id)]
            if "matches" in data[id]:
                for match in data[id]["matches"]:
                    patient = id_to_patient[match["recipient"]]
                    score = match["score"]
                    altruist.edges.append(AltruistEdge(altruist, patient, score))

