# from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
# from qiskit.visualization import plot_histogram
#
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

import git.Bakalaurinis.tools.backend_service as back
from git.Bakalaurinis.simuliator.translator import QASMTranslator
import pandas as pd

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


def prepare_x_gate_experiment():
    q_arr = []
    for i in range(0, 2 ** 5):
        q = init_reg(5)
        init_b_gates(i, q)
        measure_all(q)
        q_arr.append(q)
        # (qr, cr, qc) = q
        # tools.simulate_and_show_result(qc, title="test")
    return q_arr

def apply_x_gate_local_experiment():
    exp_arr = prepare_x_gate_experiment()
    back.simulate_local_all(exp_arr, "x_gate_local","BINARY")

def apply_x_gate_yorktown_experiment():
    exp_arr = prepare_x_gate_experiment()
    back.simulate_on_yorktown_all(exp_arr, "x_gate_ibmq_yorktown","BINARY")

def apply_x_gate_lima_experiment():
    exp_arr = prepare_x_gate_experiment()
    back.simulate_lima_all(exp_arr, "x_gate_ibmq_lima","BINARY")

q = init_reg(5)
(qr, cr, qc) = q
for i in range(0, 9):
    qc.x(qr[0])

measure_all(q)
# back.simulate_on_yorktown_all([q], "xx_10_gate_ibmq_yorktown", "xxx")

from git.Bakalaurinis.tools.transple import transpile_to_yorktown

print(transpile_to_yorktown(qc).qasm())

# apply_g_gate_experiment()
# apply_x_gate_lima_experiment()
# apply_x_gate_local_experiment()
# apply_x_gate_my_experiment()