import numpy as np
from qiskit.aqua.components.eigs import EigsQPE
from qiskit.aqua.operators import MatrixOperator
from qiskit.circuit.library import QFT
from qiskit.quantum_info import state_fidelity


def create_eigs(matrix, num_auxiliary, num_time_slices, negative_evals):
    ne_qfts = [None, None]
    if negative_evals:
        num_auxiliary += 1
        ne_qfts = [QFT(num_auxiliary - 1), QFT(num_auxiliary - 1).inverse()]

    return EigsQPE(MatrixOperator(matrix=matrix),
                   QFT(num_auxiliary).inverse(),
                   num_time_slices=num_time_slices,
                   num_ancillae=num_auxiliary,
                   expansion_mode='suzuki',
                   expansion_order=2,
                   evo_time=None,  # This is t, can set to: np.pi*3/4
                   negative_evals=negative_evals,
                   ne_qfts=ne_qfts)



def fidelity(hhl, ref):
    solution_hhl_normed = hhl / np.linalg.norm(hhl)
    solution_ref_normed = ref / np.linalg.norm(ref)
    fidelity = state_fidelity(solution_hhl_normed, solution_ref_normed)
    print("Fidelity:\t\t %f" % fidelity)



class Converter:
    def __init__(self, state_vector,
                 _reciprocal,
                 _num_q,
                 _truncate_hermitian,
                 _truncate_powerdim,
                 _original_dimension,
                 matrix,
                 vector):
        self.sv = state_vector
        self._reciprocal = _reciprocal
        self._num_q = _num_q
        self._truncate_hermitian = _truncate_hermitian
        self._truncate_powerdim = _truncate_powerdim
        self._original_dimension = _original_dimension
        self._matrix = matrix
        self._vector = vector


    def _resize_vector(self, vec: np.ndarray) -> np.ndarray:
        if self._truncate_hermitian:
            half_dim = int(vec.shape[0] / 2)
            vec = vec[:half_dim]
        if self._truncate_powerdim:
            vec = vec[:self._original_dimension]
        return vec


    def _resize_matrix(self, matrix: np.ndarray) -> np.ndarray:
        if self._truncate_hermitian:
            full_dim = matrix.shape[0]
            half_dim = int(full_dim / 2)
            new_matrix = np.ndarray(shape=(half_dim, half_dim), dtype=complex)
            new_matrix[:, :] = matrix[0:half_dim, half_dim:full_dim]
            matrix = new_matrix
        if self._truncate_powerdim:
            new_matrix = \
                np.ndarray(shape=(self._original_dimension, self._original_dimension),
                           dtype=complex)
            new_matrix[:, :] = matrix[:self._original_dimension, :self._original_dimension]
            matrix = new_matrix
        return matrix


    def _hhl_results(self, vec: np.ndarray) -> None:
        print("mano : vec", "----->", vec)

        # --------------------------------------
        # sitas nekorektiskai
        # --------------------------------------

        res_vec = self._resize_vector(vec)
        in_vec = self._resize_vector(self._vector)
        matrix = self._resize_matrix(self._matrix)
        output = res_vec
        # Rescaling the output vector to the real solution vector
        tmp_vec = matrix.dot(res_vec)
        f1 = np.linalg.norm(in_vec) / np.linalg.norm(tmp_vec)
        # "-1+1" to fix angle error for -0.-0.j
        f2 = sum(np.angle(in_vec * tmp_vec.conj() - 1 + 1)) / (np.log2(matrix.shape[0]))
        solution = f1 * res_vec * np.exp(-1j * f2)
        print("mano : solution", "----->" , solution)

    def do_magic(self):
        vec = self._reciprocal.sv_to_resvec(self.sv, self._num_q)
        probability_result = np.real(self._resize_vector(vec).dot(self._resize_vector(vec).conj()))
        print("mano: probability_result" , " ---> " , probability_result)
        vec = vec / np.linalg.norm(vec)
        self._hhl_results(vec)

