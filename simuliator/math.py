import array_to_latex as a2l
import numpy as np
from numpy.linalg import inv
import functools
from scipy import stats


def convert_to_normal_matrix(m):
    v = []
    for t in m:
        tBegin = t[0]
        for i in range(1, len(t)):
            tBegin = np.concatenate((tBegin, t[i]), axis=1)
        v.append(tBegin)

    answer = v[0]
    for i in range(1, len(v)):
        answer = np.concatenate((answer, v[i]), axis=0)
    return answer

def tensor_mul(a, b):
    return np.kron(a,b)
    # tensor = np.tensordot(a, b, 0)
    # return convert_to_normal_matrix(tensor)



def tensor_arr(t_arr):
    return functools.reduce(lambda a, b: tensor_mul(a, b), t_arr)


def mul(a, b):
    return np.matmul(a, b)


def mul_arr(m_arr):
    return functools.reduce(lambda a, b: mul(a, b), m_arr)


def find_prob(v):
    p = []
    s = np.linalg.norm(v)
    # print("|psi| =",(s**2))
    for vi in v:
        si = np.linalg.norm(vi)
        pi = ((si ** 2) / (s ** 2))
        # print((si ** 2), "/", (s ** 2), "=", pi)
        p.append(pi)
    if np.abs(np.sum(p) - 1) > 0.000001:
        raise Exception("wrong probabilities")
    return p


def map_to_arr(v):
    return [v]


def to_ket(ket):
    return list(map(map_to_arr, ket))


def _ket_bra_zero():
    ket_zero = to_ket([1, 0])
    bra_zero = [1, 0]
    return np.outer(ket_zero, bra_zero)


def _ket_bra_one():
    ket_one = to_ket([0, 1])
    bra_one = [0, 1]
    return np.outer(ket_one, bra_one)


ket_bra_zero = _ket_bra_zero()
ket_bra_one = _ket_bra_one()


# I⊗|0⟩⟨0|+X⊗|1⟩⟨1|
def apply_two_qubit_gate(gate, n_qubits, c_qubit, x_qubit):
    qc_arr = []
    qx_arr = []

    I = np.array([
        [1, 0],
        [0, 1],
    ])

    for i in range(0, n_qubits):
        qc_arr.append(I)
        qx_arr.append(I)

    qc_arr[n_qubits - c_qubit - 1] = ket_bra_zero
    qx_arr[n_qubits - c_qubit - 1] = ket_bra_one

    qx_arr[n_qubits - x_qubit - 1] = gate.get_value()
    return np.add(tensor_arr(qc_arr), tensor_arr(qx_arr))


def count_linear_regresion(df, reversed_index = True):
    df = df.dropna()
    x = None
    if reversed_index:
        x = df.index.to_numpy()[::-1]
    else:
        x = df.index.to_numpy()
    y = df.to_numpy()
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err