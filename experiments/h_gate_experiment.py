import git.Bakalaurinis.tools.backend_service as back
from git.Bakalaurinis.tools.circ_fun import init_reg, measure_all


def init_h_gates(n, q):
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.h(qr[i])


def prepare_h_gate_experiment():
    q_arr = []
    for i in range(0, 2 ** 5):
        q = init_reg(5)
        init_h_gates(i, q)
        measure_all(q)
        q_arr.append(q)
        # (qr, cr, qc) = q
        # tools.simulate_and_show_result(qc, title="test")
    return q_arr


def apply_h_gate_local_experiment():
    exp_arr = prepare_h_gate_experiment()
    back.simulate_local_all(exp_arr, "h_gate_local", "H")


def apply_h_gate_yorktown_experiment():
    exp_arr = prepare_h_gate_experiment()
    back.simulate_on_yorktown_all(exp_arr, "h_gate_yorktown", "H")


def apply_h_gate_quito_experiment():
    exp_arr = prepare_h_gate_experiment()
    back.simulate_quito_all(exp_arr, "h_gate_quito", "H")
