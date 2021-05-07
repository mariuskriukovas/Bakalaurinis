import git.Bakalaurinis.tools.backend_service as back
from git.Bakalaurinis.tools.circ_fun import init_reg, init_b_gates, measure_all


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
    back.simulate_local_all(exp_arr, "x_gate_local", "BINARY")


def apply_x_gate_yorktown_experiment():
    exp_arr = prepare_x_gate_experiment()
    back.simulate_on_yorktown_all(exp_arr, "x_gate_ibmq_yorktown", "BINARY")


def apply_x_gate_lima_experiment():
    exp_arr = prepare_x_gate_experiment()
    back.simulate_lima_all(exp_arr, "x_gate_ibmq_lima", "BINARY")
