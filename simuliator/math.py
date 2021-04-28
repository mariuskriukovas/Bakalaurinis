import array_to_latex as a2l
import numpy as np
from numpy.linalg import inv
import functools
from git.Bakalaurinis.simuliator.gates import X, I, H, Z
import ibm.myMath.fun as fun  # todo del


# todo kazkas lagina su vartais


# todo make more efection
def tensor_mul(a, b):
    tensor = np.tensordot(a, b, 0)
    v = []
    for t in tensor:
        tBegin = t[0]
        for i in range(1, len(t)):
            tBegin = np.concatenate((tBegin, t[i]), axis=1)
        v.append(tBegin)

    answer = v[0]
    for i in range(1, len(v)):
        answer = np.concatenate((answer, v[i]), axis=0)
    return answer


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


def _bra_ket_zero():
    ket_zero = fun.to_ket([1, 0])
    bra_zero = [1, 0]
    return np.outer(ket_zero, bra_zero)


def _bra_ket_one():
    ket_one = fun.to_ket([0, 1])
    bra_one = [0, 1]
    return np.outer(ket_one, bra_one)


bra_ket_zero = _bra_ket_zero()
bra_ket_one = _bra_ket_one()


# I⊗|0⟩⟨0|+X⊗|1⟩⟨1|
def apply_two_qubit_gate(gate, n_qubits, c_qubit, x_qubit):
    zero_state_arr = []
    one_state_arr = []

    for i in range(0, n_qubits):
        zero_state_arr.append(I.get_value())
        one_state_arr.append(I.get_value())

    gate_pos = n_qubits - x_qubit - 1

    zero_state_arr[n_qubits - c_qubit - 1] = bra_ket_zero
    one_state_arr[n_qubits - c_qubit - 1] = bra_ket_one

    one_state_arr[gate_pos] = gate.get_value()

    tensor_zero_state = tensor_arr(zero_state_arr)
    tensor_one_state = tensor_arr(one_state_arr)
    return np.add(tensor_zero_state, tensor_one_state)


# todo remove
# # 1 2
# # i_tensor_zero = fun.tensor_all([I.get_value(), bra_ket_zero, I.get_value()])
# # ii_tensor_zero = fun.tensor_all([X.get_value(), bra_ket_one, I.get_value(),])
#
# # 0 1
# # i_tensor_zero = fun.tensor_all([I.get_value(), I.get_value(), bra_ket_zero])
# # ii_tensor_zero = fun.tensor_all([I.get_value(),X.get_value(), bra_ket_one])
# # 0 2
# # i_tensor_zero = fun.tensor_all([I.get_value(), I.get_value(), bra_ket_zero])
# # ii_tensor_zero = fun.tensor_all([X.get_value(), I.get_value(), bra_ket_one])