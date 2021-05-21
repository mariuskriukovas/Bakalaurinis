import numpy as np
from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
import matplotlib.pyplot as plt
from qiskit.aqua.algorithms import HHL, NumPyLSsolver
import git.Projektinis.tools.simulators as tools
import git.Bakalaurinis.tools.backend_service as back
from git.Bakalaurinis.simuliator.translator import  simulate_one, QASMTranslator

# theta -- Angle defining |b>
# a -- Matrix diagonal
# b -- Matrix off-diagonal

def optimized_hhl_circuit(a, b, theta):
    t = 2  # This is not optimal; As an exercise, set this to the
    # value that will get the best results. See section 8 for solution.

    nqubits = 4  # Total number of qubits
    nb = 1  # Number of qubits representing the solution
    nl = 2  # Number of qubits representing the eigenvalues

    a_matrix = [[a, b], [b, a]]
    b_matrix = [np.cos(theta), np.sin(theta)]
    print("A = ", a_matrix)
    print("B = ", b_matrix)

    # Initialise the quantum and classical registers
    # Create a Quantum Circuit

    qr = QuantumRegister(nqubits, "qr")
    cr = ClassicalRegister(nqubits, "cr")
    qc = QuantumCircuit(qr, cr)

    qrb = qr[0:nb]
    qrl = qr[nb:nb + nl]
    qra = qr[nb + nl:nb + nl + 1]

    # State preparation.
    qc.ry(2 * theta, qrb[0])

    qc.barrier()

    # QPE with e^{iAt}
    for qu in qrl:
        qc.h(qu)

    qc.p(a * t, qrl[0])
    qc.p(a * t * 2, qrl[1])
    qc.u(b * t, -np.pi / 2, np.pi / 2, qrb[0])

    qc.barrier()

    # Controlled e^{iAt} on \lambda_{1}:
    params = b * t

    qc.p(np.pi / 2, qrb[0])
    qc.cx(qrl[0], qrb[0])
    qc.ry(params, qrb[0])
    qc.cx(qrl[0], qrb[0])
    qc.ry(-params, qrb[0])
    qc.p(3 * np.pi / 2, qrb[0])

    qc.barrier()
    # Controlled e^{2iAt} on \lambda_{2}:
    params = b * t * 2

    qc.p(np.pi / 2, qrb[0])
    qc.cx(qrl[1], qrb[0])
    qc.ry(params, qrb[0])
    qc.cx(qrl[1], qrb[0])
    qc.ry(-params, qrb[0])
    qc.p(3 * np.pi / 2, qrb[0])

    qc.barrier()
    # Inverse QFT
    qc.h(qrl[1])
    qc.rz(-np.pi / 4, qrl[1])
    qc.cx(qrl[0], qrl[1])
    qc.rz(np.pi / 4, qrl[1])
    qc.cx(qrl[0], qrl[1])
    qc.rz(-np.pi / 4, qrl[0])
    qc.h(qrl[0])

    qc.barrier()
    # Eigenvalue rotation
    t1 = (-np.pi + np.pi / 3 - 2 * np.arcsin(1 / 3)) / 4
    t2 = (-np.pi - np.pi / 3 + 2 * np.arcsin(1 / 3)) / 4
    t3 = (np.pi - np.pi / 3 - 2 * np.arcsin(1 / 3)) / 4
    t4 = (np.pi + np.pi / 3 + 2 * np.arcsin(1 / 3)) / 4

    qc.cx(qrl[1], qra[0])
    qc.ry(t1, qra[0])
    qc.cx(qrl[0], qra[0])
    qc.ry(t2, qra[0])
    qc.cx(qrl[1], qra[0])
    qc.ry(t3, qra[0])
    qc.cx(qrl[0], qra[0])
    qc.ry(t4, qra[0])

    for i, x in enumerate(qr):
        qc.measure(x, cr[i])

    return (qr, cr, qc)

# Vartai kuriuos reikia istestuoti
# Ry
# U
# H
# P
# CX
# RZ

def classical_hhl_solver(a, b, theta):
    a_matrix = [[a, b], [b, a]]
    b_matrix = [np.cos(theta), np.sin(theta)]
    result_ref = NumPyLSsolver(a_matrix, b_matrix).run()
    result = np.round(result_ref['solution'], 4)
    print("Solution:\t", result)
    return result


# as example
# qc = optimized_hhl_circuit(a = 1,
#                            b = 0,
#                            theta = 0)
# classical_hhl_solver(a = 1,
#                      b = 0,
#                      theta = 0)

def prepare_hhl_optimised_gate_experiment():
    q_arr = []
    i = 0
    while i < 2 * np.pi:
        q_arr.append(
            optimized_hhl_circuit(a=1,
                                  b=0,
                                  theta=i)
        )
        i += 0.1
    return q_arr


# q_arr = prepare_hhl_optimised_gate_experiment()
# (qr, cr, qc) = q_arr[0]
# s = QASMTranslator(qc.qasm()).get_simulator()
# s.show_results()
# qc.draw(output='mpl')
# tools.simulate_and_show_result(qc, f'a = {str(1)} b = {str(0)} theta = {str(0)}')
# plt.show()

def apply_hhl_optimised_local_experiment():
    exp_arr = prepare_hhl_optimised_gate_experiment()
    back.simulate_local_all(exp_arr, "hhl_local_parallel_test", "HHL")


def apply_hhl_optimised_yorktown_experiment():
    exp_arr = prepare_hhl_optimised_gate_experiment()
    back.simulate_on_yorktown_all(exp_arr, "hhl_ibmq_yorktown", "HHL")


def apply_hhl_optimised_quito_experiment():
    exp_arr = prepare_hhl_optimised_gate_experiment()
    back.simulate_quito_all(exp_arr, "hhl_ibmq_quito", "HHL")

# apply_hhl_optimised_local_experiment()
# apply_hhl_optimised_quito_experiment()
# apply_hhl_optimised_yorktown_experiment()