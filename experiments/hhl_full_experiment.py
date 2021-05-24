import git.Bakalaurinis.tools.helper as tools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from git.Bakalaurinis.tools.transple import transpile_to_melbourne
from git.Bakalaurinis.experiments.hhl_alg import create_HHL_circuit
from git.Bakalaurinis.simuliator.translator import get_system_length, simulate_melburne_one
from git.Bakalaurinis.simuliator.gates import np_gate, na_gate, gate_factory
from git.Bakalaurinis.simuliator.gates import X, I, rx_gate, rz_gate, ry_gate
from git.Bakalaurinis.analysis.noise_interval_analysis import f_quito_rz_noise, f_quito_p_noise, f_quito_ry_noise, f_quito_rx_noise
import random
from git.Bakalaurinis.tools.presentation_service import write_results_to_excel


def execute_qiskit_simuliation(qc):
    # tools.simulate_and_show_result(qc, "")
    return tools.simulate_and_return_result(qc)
    # plt.show()

def transpile(qc):
    # qc_y.measure_all()
    return transpile_to_melbourne(qc)

def get_shortest_transpiled_circuit(matrix,vector, experiments = 10):
    shortest_qc = None
    shortest_len = None
    for i in range(0, experiments):
        qc = create_HHL_circuit(matrix, vector)
        qc = transpile(qc)
        return qc
        length = get_system_length(qc)
        if shortest_len is None or shortest_len < length:
            shortest_qc = qc
            shortest_len = length
    return shortest_qc

ADJUST_COFF = 10

def f_factory(f):
    def adjusted_f(psi):
        psi = psi % 2 * np.pi
        e = 0.1
        return random.uniform(-1* (1 / ADJUST_COFF) * f(psi), (1 / ADJUST_COFF) * f(psi))
    return adjusted_f


rx_q = f_quito_rx_noise()
ry_q = f_quito_ry_noise()
rz_q = f_quito_rz_noise()
p_q = f_quito_p_noise()

model = {
    'M': gate_factory(ry_gate, 0.197125245579567 / ADJUST_COFF),
    'CX': gate_factory(rx_gate, 0.4698968668407313 / 2 / ADJUST_COFF),
    'NRx': f_factory(rx_q),
    'NRy': f_factory(ry_q),
    'NRz': f_factory(rz_q),
    'NP': f_factory(p_q),
    'U1L': f_factory(rz_q),
    'U2F':  f_factory(rz_q),
    'U2L': f_factory(rz_q),
    'U3F': f_factory(rz_q),
    'U3T': f_factory(rz_q),
    'U3L': f_factory(rz_q),
}

averages = []

def generate_experiment():
    matrix = [[0, 0, 0, 1],
              [0, 0, 1, 0],
              [0, 1, 0, 0],
              [1, 0, 0, 0]]
    vector = [np.sin(np.random.rand()), np.cos(np.random.rand()),]

    qc = get_shortest_transpiled_circuit(matrix, vector)

    print("gylis ---- > ",  qc.depth() )
    print("cx skaicius ---- > ", qc.count_ops()['cx'])
    print("u3 skaicius ---- > ", qc.count_ops()['u3'])

    perfect = simulate_melburne_one(qc,{})
    real = simulate_melburne_one(qc,model)
    percent_diff = np.mean(np.linalg.norm((perfect - real)))
    print("vidurkis ------- > ", percent_diff)
    averages.append(percent_diff)

def execute():
    for i in range(0, 10):
        generate_experiment()
    print("visu vidurkis ------> ", np.mean(averages))


execute()
# e = 1.092e-2