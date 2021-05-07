from git.Bakalaurinis.tools.circ_fun import init_reg, init_b_gates, measure_all
import git.Bakalaurinis.tools.backend_service as back
from itertools import permutations


def prepare_cx_gate_experiment(measure=False):
    qubits = list(range(0, 5))
    q_arr = []
    for com in permutations(qubits, 2):
        q = init_reg(5)
        (qr, cr, qc) = q
        (c_q, x_q) = com
        if measure:
            qc.x(qr[c_q])
        qc.cx(qr[c_q], qr[x_q])
        measure_all(q)
        q_arr.append(q)
    return q_arr


def apply_cx_gate_local_experiment_zero():
    exp_arr = prepare_cx_gate_experiment()
    back.simulate_local_all(exp_arr, "cx_gate_local_z", "cx_zero")


def apply_cx_gate_local_experiment_one():
    exp_arr = prepare_cx_gate_experiment(True)
    back.simulate_local_all(exp_arr, "cx_gate_local_o", "cx_one")


def apply_cx_gate_yorktown_experiment_zero():
    exp_arr = prepare_cx_gate_experiment()
    back.simulate_on_yorktown_all(exp_arr, "cx_gate_yorktown_z", "cx_zero")


def apply_cx_gate_yorktown_experiment_one():
    exp_arr = prepare_cx_gate_experiment(True)
    back.simulate_on_yorktown_all(exp_arr, "cx_gate_yorktown_o", "cx_one")


def apply_cx_gate_quito_experiment_zero():
    exp_arr = prepare_cx_gate_experiment()
    back.simulate_quito_all(exp_arr, "cx_gate_quito_z", "cx_zero")


def apply_cx_gate_quito_experiment_one():
    exp_arr = prepare_cx_gate_experiment(True)
    back.simulate_quito_all(exp_arr, "cx_gate_quito_o", "cx_one")
