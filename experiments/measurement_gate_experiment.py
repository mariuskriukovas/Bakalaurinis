import git.Bakalaurinis.tools.backend_service as back
from git.Bakalaurinis.tools.circ_fun import init_reg


def init_gates(n):
    q = init_reg(5)
    (qr, cr, qc) = q
    b_n = bin(n)[2:]
    print(b_n)
    for i, x in enumerate(reversed(b_n)):
        if x == '1':
            qc.measure(qr[i], cr[i])
    return (qr, cr, qc)


def prepare_measurement_gate_experiment():
    q_arr = []
    for i in range(0, 2 ** 5):
        q = init_gates(i)
        q_arr.append(q)
        # (qr, cr, qc) = q
        # tools.simulate_and_show_result(qc, title="test")
    return q_arr


def apply_measurement_gate_local_experiment():
    exp_arr = prepare_measurement_gate_experiment()
    back.simulate_local_all(exp_arr, "measurement_gate_local", "M")


def apply_measurement_gate_yorktown_experiment():
    exp_arr = prepare_measurement_gate_experiment()
    back.simulate_on_yorktown_all(exp_arr, "measurement_gate_ibmq_yorktown", "M")


def apply_measurement_gate_quito_experiment():
    exp_arr = prepare_measurement_gate_experiment()
    back.simulate_quito_all(exp_arr, "measurement_gate_ibmq_quito", "M")
