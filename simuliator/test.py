import numpy as np
import git.Projektinis.tools.gates as g
from qiskit.aqua.components.reciprocals import LookupRotation
from qiskit.aqua.algorithms import HHL, NumPyLSsolver
from qiskit import Aer, transpile, assemble
import matplotlib.pyplot as plt
import git.Projektinis.tools.simulators as tools
import git.Projektinis.tools.functions as fun



import git.Bakalaurinis.experiments.hhl_functions as hhl_fun
import git.Bakalaurinis.tools.presentation_service as pr
from git.Bakalaurinis.simuliator.gates import X,I,H
from git.Bakalaurinis.simuliator.simuliator import Simuliator
from git.Bakalaurinis.simuliator.math import apply_two_qubit_gate



from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import git.Projektinis.tools.simulators as tools


def init_reg(n):
    qr = QuantumRegister(n, "qr")
    cr = ClassicalRegister(n, "cr")
    qc = QuantumCircuit(qr, cr)
    q = (qr, cr, qc)
    return q


def init_b_gates(n, q):
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.x(qr[i])


def measure_all(q):
    (qr, cr, qc) = q
    for i, x in enumerate(qr):
        qc.measure(x, cr[i])


def get_MOCK_circuit():
    q = init_reg(5)
    init_b_gates(5, q)
    measure_all(q)
    return q

C_gate = 0
X_gate = 1
N_qubits = 2

# q = init_reg(N_qubits)
# (qr, cr, qc) = q
# qc.cx(qr[C_gate],qr[X_gate])
# init_b_gates(3,q)
# init_b_gates(3,q)
# measure_all(q)

q = init_reg(3)
(qr, cr, qc) = q
init_b_gates(7,q)
qc.x(qr[2])
qc.cx(qr[0],qr[2])
# init_b_gates(3,q)
measure_all(q)
qc.draw(output='mpl')
tools.simulate_and_show_result(qc)

import git.Bakalaurinis.simuliator.translator as trans
simuliator = trans.QASMParser(qc.qasm()).get_simulator()
simuliator.show_circuit()
simuliator.show_results()

# A = np.abs(tools.simulate_unitary_matrix_df(qc))
# print(A)
# plt.show()
# B = apply_two_qubit_gate(X, N_qubits, C_gate, X_gate)
# print(B)
# print("N_qubits",N_qubits, "C = ",  C_gate, "X = ", X_gate)
# (a,b) = B.shape
# print("A == B", np.equal(A, B).sum() == (a*b))
# x = Simuliator(3)
# x.add_single_gates([(0, X),(1, X),(2, X)])
# x.add_single_gates([(2, X)])
# x.add_multi_gates(X,0,2)
# x.show_circuit()
# x.measure()
# x.show_results()

plt.show()