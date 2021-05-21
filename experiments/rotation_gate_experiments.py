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
    # print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.ry(theta, qr[i])


def init_rz_gates(n, theta, q):
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    # print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.h(qr[i])
            qc.rz(theta, qr[i])
            qc.h(qr[i])


def init_p_gates(n, theta, q):
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    # print(b_n)
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


def prepare_rotation_experiment_interval(experiment):
    q_arr = []
    theta = 0
    all_gates = 2 ** 5 - 1
    while theta < 2 * np.pi:
        q = init_reg(5)
        # print(theta)
        experiment(all_gates, theta, q)
        measure_all(q)
        q_arr.append(q)
        theta += np.pi / 20
    return q_arr


def prepare_n_rotation_experiment_interval(experiment):
    q_arr = []
    theta = -1 * 2 * np.pi
    all_gates = 2 ** 5 - 1
    while theta < 0:
        q = init_reg(5)
        # print(theta)
        experiment(all_gates, theta, q)
        measure_all(q)
        q_arr.append(q)
        theta += np.pi / 20
    return q_arr


def prepare_full_rotation_experiment_in_interval(init_gates):
    a = prepare_n_rotation_experiment_interval(init_gates)
    b = prepare_rotation_experiment_interval(init_gates)
    return np.concatenate([a, b])


# prepare_all_n_rotation_experiment_interval()

def apply_rx_full_quito_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_rx_gates)
    back.simulate_quito_all(exp_arr, "f_rx_gate_quito", "rx")


def apply_ry_full_quito_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_ry_gates)
    back.simulate_quito_all(exp_arr, "f_ry_gate_quito", "ry")


def apply_rz_full_quito_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_rz_gates)
    back.simulate_quito_all(exp_arr, "f_rz_gate_quito", "rz")


def apply_p_full_quito_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_p_gates)
    back.simulate_quito_all(exp_arr, "f_p_gate_quito", "p")


# ---------------------------------------------------------------------
# apply_rx_full_quito_experiment()

def apply_rx_full_yorktown_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_rx_gates)
    back.simulate_on_yorktown_all(exp_arr, "f_rx_gate_yorktown", "rx")


def apply_ry_full_yorktown_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_ry_gates)
    back.simulate_on_yorktown_all(exp_arr, "f_ry_gate_yorktown", "ry")

# apply_ry_full_yorktown_experiment()

def apply_rz_full_yorktown_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_rz_gates)
    back.simulate_on_yorktown_all(exp_arr, "f_rz_gate_yorktown", "rz")


def apply_p_full_yorktown_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_p_gates)
    back.simulate_on_yorktown_all(exp_arr, "f_p_gate_yorktown", "p")


# ---------------------------------------------------------------------

def apply_rx_full_local_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_rx_gates)
    back.simulate_local_all(exp_arr, "f_rx_gate_local", "rx")


def apply_ry_full_local_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_ry_gates)
    back.simulate_local_all(exp_arr, "f_ry_gate_local", "ry")


def apply_rz_full_local_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_rz_gates)
    back.simulate_local_all(exp_arr, "f_rz_gate_local", "rz")


def apply_p_full_local_experiment():
    exp_arr = prepare_full_rotation_experiment_in_interval(init_p_gates)
    back.simulate_local_all(exp_arr, "f_p_gate_local", "p")
