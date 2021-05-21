from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

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


