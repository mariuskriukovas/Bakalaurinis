import numpy as np
import pandas as pd

from qiskit.visualization import plot_histogram
from git.Bakalaurinis.simuliator.chart_drawer import draw_bar_chart, draw_circuit_scheme, bcolors
from git.Bakalaurinis.simuliator.gates import I, C, SimpleGate
from git.Bakalaurinis.simuliator.math import tensor_arr, mul_arr, find_prob, apply_two_qubit_gate, \
    convert_to_normal_matrix


# Paisdaryti korektiskai veikianti simuliatoriu - done
# Prasitestuoti ant X vart kombinacijos
# Surasti buda konvertuoti is mano i quiskit
# Pradeti tytineti tikimybes


class Simuliator:
    def __init__(self, n, noise=None):
        self.n_qbits = n
        self.gates = []
        self._iteration = 0
        self.transition_matrix = None
        self.ket_zero = None
        self.final_state = None
        self.results = None
        self._tensors = []
        self._measurement = False

        self._noise = noise

        for i in range(0, n):
            self.gates.append([])

        # print(bcolors.FAIL, "init", "--->", self.n_qbits, bcolors.ENDC)

    @staticmethod
    def _rise_wring_gate_exeption(string):
        err_str = f'Wrong input gate {string}'
        raise Exception(err_str)

    @staticmethod
    def _search_in_gate_arr(g_arr, index):
        return [x for x, y in enumerate(g_arr) if y[0] == index]

    @staticmethod
    def _print_gate_arr(g_arr):
        return list(map(lambda xy: (xy[0], xy[1].get_name()), g_arr))

    def _append_gates(self, g_arr):
        for i in range(0, self.n_qbits):
            idx_arr = self._search_in_gate_arr(g_arr, i)
            len_idx_arr = len(idx_arr)

            # why quiskit is reverse ???
            reversed_i = self.n_qbits - i - 1
            if len_idx_arr == 0:
                self.gates[reversed_i].append(I)
            elif len_idx_arr == 1:
                idx = idx_arr[0]
                (_, gate) = g_arr[idx]
                self.gates[reversed_i].append(gate)
                del g_arr[idx]
            else:
                self._rise_wring_gate_exeption("more than one index")

        if len(g_arr) > 0:
            self._rise_wring_gate_exeption("still left")

    def add_multi_gates(self, gate, c_qubit, v_qubit):
        # print("add multi gate ", "--->", "C" + gate.get_name() + " c : " + str(c_qubit) + " v : " + str(v_qubit))
        # print("iteration ", "--->", self._iteration)
        full_name = "C" + str(gate.get_name())

        # if full_name in self._noise.keys():
        #     noisy_gate_name = "N" + full_name
        #     gate = SimpleGate(noisy_gate_name, mul_arr([gate.get_value(), self._noise[full_name].get_value()]))

        tensor = apply_two_qubit_gate(gate, self.n_qbits, c_qubit, v_qubit)

        g_arr = [(c_qubit, C), (v_qubit, gate)]
        self._append_gates(g_arr)

        self._tensors.append(tensor)

        if full_name in self._noise.keys():
            noisy_gate = self._noise[full_name]
            tensor = apply_two_qubit_gate(noisy_gate, self.n_qbits, c_qubit, v_qubit)
            self._tensors.append(tensor)
            # g_arr = [(c_qubit, C), (v_qubit, noisy_gate)]
            # self._append_gates(g_arr)

        self._iteration += 1

    def _apply_noise(self, g_arr):
        n_g_arr = []
        if self._noise is not None:
            for key in self._noise.keys():
                for g in g_arr:
                    (pos, gate) = g
                    if gate.get_name().find(key) == 0:
                        n_g_arr.append((pos, self._noise[key]))
        return n_g_arr

    def add_single_gates(self, g_arr):
        # print("add single gates ", "--->", self._print_gate_arr(g_arr))
        # print("iteration ", "--->", self._iteration)

        nois_copy = g_arr.copy()

        self._append_gates(g_arr)
        gates = []
        for i in range(0, self.n_qbits):
            gates.append(self.gates[i][self._iteration].get_value())
        self._tensors.append(tensor_arr(gates))
        self._iteration += 1

        noise_arr = self._apply_noise(nois_copy)
        if len(noise_arr) > 0:
            self.add_single_gates(noise_arr)

    def gates_to_df(self):
        dic = {}
        for i in range(0, self.n_qbits):
            dic[str(i)] = self.gates[i]
        df = pd.DataFrame(data=dic)
        return df

    def _count_transition_matrix(self):
        tensors = list(reversed(self._tensors))
        return mul_arr(tensors)

    def _get_zero_state_vector(self):
        zero = np.zeros(2 ** self.n_qbits)
        zero[0] = 1
        return list(map(lambda x: [x], zero))

    def set_measurement(self, measure):
        self._measurement = measure

    def measure(self):
        self.ket_zero = self._get_zero_state_vector()
        self.results = {}

        if not self._measurement:
            for i in range(0, len(self.ket_zero)):
                self.results[str(i)] = [self.ket_zero[i]]
            return

        self.transition_matrix = self._count_transition_matrix()
        self.final_state = mul_arr([self.transition_matrix, self.ket_zero])

        prob = find_prob(self.final_state)
        for i in range(0, len(prob)):
            self.results[str(i)] = [prob[i]]

    def get_results_as_dic(self) -> dict:
        return self.results

    def get_results(self) -> pd.DataFrame:
        return pd.DataFrame(data=self.results)


    def show_results_qiskit_graph(self, title="title"):
        new_dic = {}
        e = 0.000001
        for k in self.results.keys():
            state = self.results[k][0]
            if state > e:
                new_dic[k] = bytes((state * 1024))

        plot_histogram(new_dic, title=title)

    def show_circuit(self, title):
        len_cir = len(self.gates[0])
        dic = {}
        for i in range(0, len_cir):
            dic[str(i)] = []
            for j in range(0, self.n_qbits):
                dic[str(i)].append(self.gates[j][i].get_name())

        df = pd.DataFrame(data=dic)
        draw_circuit_scheme(df, title=title)
