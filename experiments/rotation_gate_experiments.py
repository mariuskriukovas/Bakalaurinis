import numpy as np

import git.Bakalaurinis.tools.backend_service as back
from git.Bakalaurinis.tools.circ_fun import init_reg, measure_all


def init_rx_gates(n, theta, q):
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.rx(theta, qr[i])


def prepare_rx_gate_experiment():
    q_arr = []

    theta = 0
    while theta < 2 * np.pi:
        for i in range(0, 2 ** 5):
            q = init_reg(5)
            init_rx_gates(i, theta, q)
            measure_all(q)
            q_arr.append(q)
            # (qr, cr, qc) = q
            # tools.simulate_and_show_result(qc, title="test")
        theta += np.pi / 3
    return q_arr


def init_ry_gates(n, theta, q):
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.ry(theta, qr[i])


def init_rz_gates(n, theta, q):
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.h(qr[i])
            qc.rz(theta, qr[i])
            qc.h(qr[i])


def init_p_gates(n, theta, q):
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.h(qr[i])
            qc.p(theta, qr[i])
            qc.h(qr[i])


def prepare_rotation_experiment(experiment):
    q_arr = []
    theta = 0
    while theta < 2 * np.pi:
        for i in range(0, 2 ** 5):
            q = init_reg(5)
            experiment(i, theta, q)
            measure_all(q)
            q_arr.append(q)
            # (qr, cr, qc) = q
            # tools.simulate_and_show_result(qc, title="test")
        theta += np.pi / 3
    return q_arr


def apply_rotation_gate_local_experiment():
    exp_arr = prepare_rotation_experiment(init_ry_gates)
    back.simulate_local_all(exp_arr, "ry_gate_local", "ry")

    exp_arr = prepare_rotation_experiment(init_rz_gates)
    back.simulate_local_all(exp_arr, "rz_gate_local", "rz")

    exp_arr = prepare_rotation_experiment(init_p_gates)
    back.simulate_local_all(exp_arr, "p_gate_local", "p")


# apply_rotation_gate_local_experiment()

def apply_rotation_gate_yorktown_experiment():
    exp_arr = prepare_rotation_experiment(init_ry_gates)
    back.simulate_on_yorktown_all(exp_arr, "ry_gate_yorktown", "ry")

    exp_arr = prepare_rotation_experiment(init_rz_gates)
    back.simulate_on_yorktown_all(exp_arr, "rz_gate_yorktown", "rz")

    exp_arr = prepare_rotation_experiment(init_p_gates)
    back.simulate_on_yorktown_all(exp_arr, "p_gate_yorktown", "p")


# apply_rotation_gate_yorktown_experiment()

def apply_rotation_gate_quito_experiment():
    exp_arr = prepare_rotation_experiment(init_ry_gates)
    back.simulate_quito_all(exp_arr, "ry_gate_quito", "ry")

    exp_arr = prepare_rotation_experiment(init_rz_gates)
    back.simulate_quito_all(exp_arr, "rz_gate_quito", "rz")

    exp_arr = prepare_rotation_experiment(init_p_gates)
    back.simulate_quito_all(exp_arr, "p_gate_quito", "p")


# apply_rotation_gate_quito_experiment()

def apply_rx_gate_local_experiment():
    exp_arr = prepare_rx_gate_experiment()
    back.simulate_local_all(exp_arr, "rx_gate_local", "rx")


# apply_rx_gate_local_experiment()

def apply_rx_gate_yorktown_experiment():
    exp_arr = prepare_rx_gate_experiment()
    back.simulate_on_yorktown_all(exp_arr, "rx_gate_yorktown", "rx")


# apply_rx_gate_yorktown_experiment()

def apply_rx_gate_quito_experiment():
    exp_arr = prepare_rx_gate_experiment()
    back.simulate_quito_all(exp_arr, "rx_gate_quito", "rx")

# apply_rx_gate_quito_experiment()
