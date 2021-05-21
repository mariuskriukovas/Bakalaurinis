import git.Projektinis.tools.simulators as tools
import matplotlib.pyplot as plt
from git.Bakalaurinis.tools.transple import transpile_to_melbourne
from git.Bakalaurinis.experiments.hhl_alg import create_HHL_circuit
from git.Bakalaurinis.simuliator.translator import get_system_length, simulate_melburne_one


def execute_qiskit_simuliation(qc):
    tools.simulate_and_show_result(qc, "")
    # plt.show()

def transpile(qc):
    # qc_y.measure_all()
    return transpile_to_melbourne(qc)

def get_shortest_transpiled_circuit(matrix,vector, experiments = 10):
    shortest_qc = None
    shortest_len = None
    for i in range(0, experiments):
        qc = create_HHL_circuit(matrix, vector)
        return qc
        qc = transpile(qc)
        length = get_system_length(qc)
        if shortest_len is None or shortest_len > length:
            shortest_qc = qc
            shortest_len = length
    return shortest_qc


# matrix = [[0, 0, 0, 1],
#           [0, 0, 1, 0],
#           [0, 1, 0, 0],
#           [1, 0, 0, 0]]

matrix = [[0.5, 0, 0, 0],
          [0, 0.5, 0, 0],
          [0, 0, 0.5, 0],
          [0, 0, 0, 0.5]]


vector = [1,  1, 1, 1]

qc = get_shortest_transpiled_circuit(matrix, vector)
print(qc.qasm())
# execute_qiskit_simuliation(qc)
# print(qc_y.qasm())
# # qc_y.draw(output='mpl')
#
# from git.Bakalaurinis.simuliator.gates import np_gate, na_gate, gate_factory
# from git.Bakalaurinis.simuliator.gates import X, I, rx_gate, rz_gate, ry_gate
#
# simulate_melburne_one(qc, {
#     'M': gate_factory(ry_gate, 0.1737),
#     'CX': gate_factory(rx_gate,  0.4698968668407313/100),
#     # 'NRy': f_factory(ry_q),
#     # 'NRz': f_factory(rz_q),
#     # 'NP': f_factory(p_q),
#     })
# plt.show()


# # e = 1.092e-2
# # print(e)