import git.Bakalaurinis.simuliator.simuliator as sim
from git.Bakalaurinis.simuliator.gates import X, I, H, Z, Y, M, SimpleGate
from git.Bakalaurinis.simuliator.gates import rx_gate, ry_gate, rz_gate, u_gate, p_gate, u1_gate, u2_gate, u3_gate
import numpy as np
import pandas as pd
import re
import random
from git.Bakalaurinis.simuliator.chart_drawer import print_red, print_green


class QASMTranslator:
    def __init__(self, qasm_str, q_noise=None, q_map_dic=None):
        self.q_map_dic = q_map_dic
        self.qasm_str = qasm_str
        self.qasm_arr = qasm_str.split('\n')
        self.q_noise = q_noise

        self._n_q = None
        self._m_q = None
        self._simulator = None
        self._statements_arr = []

        self._qubits_in_use = {}

        if q_map_dic:
            self._qubit_map_dic = q_map_dic
        else:
            self._qubit_map_dic = {}

    def _search_in__statements_arr(self, pos):
        return [x for x, y in enumerate(self._statements_arr) if y[0] == pos]

    def _add_statement(self, q_statement):
        (pos, gate) = q_statement
        is_same_column = self._search_in__statements_arr(pos)
        if not is_same_column:
            self._statements_arr.append(q_statement)
        else:
            self._simulator.add_single_gates(self._statements_arr)
            self._statements_arr = []
            self._statements_arr.append(q_statement)

    def _parse_not_know(self, qasm_word_arr):
        raise Exception(f'Gate not know {str(qasm_word_arr)}')

    def _parse_include_statement(self, qasm_word_arr):
        statement = "include"

    def _parse_OPENQASM_statement(self, qasm_word_arr):
        statement = "OPENQASM"

    def _parse_square_bracket_content(self, q_str) -> [str]:
        return re.findall(r'\[(.*?)\]', q_str)

    def _parse_round_bracket_content(self, q_str) -> [str]:
        return re.findall(r'\((.*?)\)', q_str)

    def _map_to_int(self, q_str) -> [int]:
        return list(map(lambda x: int(x), q_str))

    def _parse_numbers(self, q_str) -> [int]:
        num = re.findall(r'[0-9]+', q_str)
        return list(map(lambda x: int(x), num))

    def _parse_qreg_statement(self, qasm_word_arr):
        self._n_q = self._extract_q_value(qasm_word_arr[1])

    def _parse_creg_statement(self, qasm_word_arr):
        # only all register measurement supported
        self._m_q = self._extract_q_value(qasm_word_arr[1])
        # print_red("self._m_q : " + str(self._m_q))
        if self._n_q != self._m_q:
            print_red("Using qubit maping : ")
            print_red(self._qubit_map_dic)
            self._m_q = len(self._qubit_map_dic)
            self._n_q = self._m_q
        self._simulator = sim.Simuliator(self._m_q, self.q_noise)
        for i in range(0, self._n_q):
            self._add_statement((i, I))

    def _extract_theta(self, qasm_word) -> float:
        theta = self._parse_round_bracket_content(qasm_word)[0]
        theta = theta.replace("pi", "np.pi")
        return float(eval(theta))

    def _extract_q_value(self, qasm_word) -> int:
        return int(self._parse_square_bracket_content(qasm_word)[0])

    def _extract_q(self, qasm_word) -> int:
        real_q_val = self._extract_q_value(qasm_word)
        if self.q_map_dic:
            # print_green(str(real_q_val) + " ----> " + str(self.q_map_dic[real_q_val]))
            return self.q_map_dic[real_q_val]
        else:
            # print_red(real_q_val)
            return real_q_val

    def _extract_two_q(self, qasm_word) -> (int, int):
        (q1, q2) = int(self._parse_square_bracket_content(qasm_word)[0]), \
                   int(self._parse_square_bracket_content(qasm_word)[1])

        if self.q_map_dic:
            # print_green(str(q1) + " ----> " + str(self.q_map_dic[q1]))
            # print_green(str(q2) + " ----> " + str(self.q_map_dic[q2]))
            return(self.q_map_dic[q1],self.q_map_dic[q2])
        else:
            # print_red(str(q1) + " ----> " + str(self.q_map_dic[q1]))
            # print_red(str(q2) + " ----> " + str(self.q_map_dic[q2]))
            return (q1, q2)

    def _extract_theta_and_q(self, qasm_word_arr) -> (float, int):
        return (self._extract_theta(qasm_word_arr[0]), self._extract_q(qasm_word_arr[1]))

    def _parse_ry_statement(self, qasm_word_arr):
        (theta, q) = self._extract_theta_and_q(qasm_word_arr)
        if self.q_noise and 'TRy' in self.q_noise.keys():
            theta += self.q_noise['TRy']
        if self.q_noise and 'NRy' in self.q_noise.keys():
            f = self.q_noise['NRy']
            theta += f(theta)
        ry = SimpleGate(ry_gate.get_adjusted_name(theta), ry_gate.get_value(theta))
        self._add_statement((q, ry))

    def _parse_rx_statement(self, qasm_word_arr):
        (theta, q) = self._extract_theta_and_q(qasm_word_arr)
        if self.q_noise and 'TRx' in self.q_noise.keys():
            theta += self.q_noise['TRx']
        if self.q_noise and 'NRx' in self.q_noise.keys():
            f = self.q_noise['NRx']
            # theta += random.uniform(a,b)
            theta += f(theta)

        rx = SimpleGate(rx_gate.get_adjusted_name(theta), rx_gate.get_value(theta))
        self._add_statement((q, rx))

    def _parse_rz_statement(self, qasm_word_arr):
        (theta, q) = self._extract_theta_and_q(qasm_word_arr)
        if self.q_noise and 'TRz' in self.q_noise.keys():
            theta += self.q_noise['TRz']
        if self.q_noise and 'NRz' in self.q_noise.keys():
            f = self.q_noise['NRz']
            theta += f(theta)
        rz = SimpleGate(rz_gate.get_adjusted_name(theta), rz_gate.get_value(theta))
        self._add_statement((q, rz))

    def _parse_barrier_statement(self, qasm_word_arr):
        # barrier in qiskit only for representation
        statement = "barrier"

    def _parse_p_statement(self, qasm_word_arr):
        # print(qasm_word_arr)
        (theta, q) = self._extract_theta_and_q(qasm_word_arr)
        if self.q_noise and 'TP' in self.q_noise.keys():
            theta += self.q_noise['TP']
        if self.q_noise and 'NP' in self.q_noise.keys():
            f = self.q_noise['NP']
            theta += f(theta)
        p = SimpleGate(p_gate.get_adjusted_name(theta), p_gate.get_value(theta))
        self._add_statement((q, p))

    # U1(λ)=eiλ/2RZ(λ)
    def _parse_u1_statement(self, qasm_word_arr):
        u_val = self._parse_round_bracket_content(qasm_word_arr[0])[0]
        u_val = u_val.replace("pi", "np.pi").split(",")
        lam = eval(u_val[0])

        # U1NOISE
        if self.q_noise and 'U1L' in self.q_noise.keys():
            f = self.q_noise['U1L']
            lam += f(lam)

        q = self._extract_q(qasm_word_arr[1])
        u = SimpleGate(u1_gate.get_adjusted_name(lam), u1_gate.get_value(lam))
        self._add_statement((q, u))

    # U2(ϕ,λ)=RZ(ϕ).RY(π2).RZ(λ)
    def _parse_u2_statement(self, qasm_word_arr):
        u_val = self._parse_round_bracket_content(qasm_word_arr[0])[0]
        u_val = u_val.replace("pi", "np.pi").split(",")
        phi = eval(u_val[0])
        lam = eval(u_val[1])

        # U2NOISE RZ phi
        if self.q_noise and 'U2P' in self.q_noise.keys():
            f = self.q_noise['U2P']
            phi += f(lam)

        # U2NOISE RZ lamb
        if self.q_noise and 'U2L' in self.q_noise.keys():
            f = self.q_noise['U2L']
            phi += f(lam)

        q = self._extract_q(qasm_word_arr[1])
        u = SimpleGate(u2_gate.get_adjusted_name((phi, lam)), u2_gate.get_value((phi, lam)))
        self._add_statement((q, u))

    # U3(θ,ϕ,λ)=RZ(ϕ)RX(−π/2)RZ(θ)RX(π/2)RZ(λ)
    def _parse_u3_statement(self, qasm_word_arr):
        u_val = self._parse_round_bracket_content(qasm_word_arr[0])[0]
        u_val = u_val.replace("pi", "np.pi").split(",")
        theta = eval(u_val[0])
        phi = eval(u_val[1])
        lam = eval(u_val[2])

        # U2NOISE RZ phi
        if self.q_noise and 'U3P' in self.q_noise.keys():
            f = self.q_noise['U3P']
            phi += f(lam)

        # U2NOISE RZ lamb
        if self.q_noise and 'U3L' in self.q_noise.keys():
            f = self.q_noise['U3L']
            phi += f(lam)

        # U2NOISE RZ thet
        if self.q_noise and 'U3T' in self.q_noise.keys():
            f = self.q_noise['U3T']
            phi += f(lam)

        # print("------------------------------------>", theta)
        # print("------------------------------------>", phi)
        # print("------------------------------------>", lam)
        q = self._extract_q(qasm_word_arr[1])
        u = SimpleGate(u3_gate.get_adjusted_name((theta, phi, lam)), u3_gate.get_value((theta, phi, lam)))
        # print("------------------------------------>", u.get_name())
        self._add_statement((q, u))

    def _parse_u_statement(self, qasm_word_arr):
        # print(qasm_word_arr)
        u_val = self._parse_round_bracket_content(qasm_word_arr[0])[0]
        u_val = u_val.replace("pi", "np.pi").split(",")
        theta = eval(u_val[0])
        phi = eval(u_val[1])
        lam = eval(u_val[2])
        q = self._extract_q(qasm_word_arr[1])
        u = SimpleGate(u_gate.get_adjusted_name((theta, phi, lam)), u_gate.get_value((theta, phi, lam)))
        self._add_statement((q, u))

    def _save_progress(self):
        if len(self._statements_arr) > 0:
            self._simulator.add_single_gates(self._statements_arr)
            self._statements_arr = []

    def _parse_cx_statement(self, qasm_word_arr):
        self._save_progress()
        (q_0, q_1) = self._extract_two_q(qasm_word_arr[1])
        self._simulator.add_multi_gates(X, q_0, q_1)

    def _parse_h_statement(self, qasm_word_arr):
        q = self._extract_q(qasm_word_arr[1])
        self._add_statement((q, H))

    def _parse_x_statement(self, qasm_word_arr):
        q = self._extract_q(qasm_word_arr[1])
        self._add_statement((q, X))

    def _parse_y_statement(self, qasm_word_arr):
        q = self._extract_q(qasm_word_arr[1])
        self._add_statement((q, Y))

    def _parse_z_statement(self, qasm_word_arr):
        q = self._extract_q(qasm_word_arr[1])
        self._add_statement((q, Z))

    def _parse_measure_statement(self, qasm_word_arr):
        q = self._extract_q(qasm_word_arr[1])
        self._add_statement((q, M))
        self._simulator.set_measurement(True)

    def _parse_qubit_map_statement(self, qasm_word_arr):
        q = self._extract_q_value(qasm_word_arr[1])
        m = self._extract_q_value(qasm_word_arr[3])
        self._qubit_map_dic[q] = m

    def _parse_dictionary(self):
        return {
            "OPENQASM": self._parse_OPENQASM_statement,
            "include": self._parse_include_statement,
            "qreg": self._parse_qreg_statement,
            "creg": self._parse_creg_statement,
            "barrier": self._parse_barrier_statement,
            "measure": self._parse_measure_statement,
            "cx": self._parse_cx_statement,
            "rx": self._parse_rx_statement,
            "ry": self._parse_ry_statement,
            "rz": self._parse_rz_statement,
            "x": self._parse_x_statement,
            "y": self._parse_y_statement,
            "z": self._parse_z_statement,
            "h": self._parse_h_statement,
            "p": self._parse_p_statement,
            "u1": self._parse_u1_statement,
            "u2": self._parse_u2_statement,
            "u3": self._parse_u3_statement,
            "u": self._parse_u_statement,
        }

    def _parse_qubit_map_dictionary(self):
        return {
            "measure": self._parse_qubit_map_statement,
            "cx": self._parse_multiple_qubit_map_statement,
        }

    def _parse_line_qasm(self, qasm_line):
        qasm_word_arr = qasm_line.split(' ')
        qasm_dic = self._parse_dictionary()
        for qasm_rule in qasm_dic.keys():
            if qasm_word_arr[0].find(qasm_rule) == 0:
                qasm_f = qasm_dic[qasm_rule]
                qasm_f(qasm_word_arr)
                return
        self._parse_not_know(qasm_word_arr)

    def parse_qasm(self):
        for i, qasm_line in enumerate(self.qasm_arr):
            # print(qasm_line)
            if not qasm_line.strip().isspace() and len(qasm_line) > 1:
                self._parse_line_qasm(qasm_line)

        if len(self._statements_arr) > 0:
            self._simulator.add_single_gates(self._statements_arr)

        self._simulator.measure()

    def _parse_single_qubit_map_statement(self, qasm_word_arr):
        m = re.search('q\[(.+?)\]', qasm_word_arr)
        if m:
            idx = int(m.group(1))
            self._qubits_in_use[idx] = 1

    def _parse_multiple_qubit_map_statement(self, qasm_word_arr):
        (q_0, q_1) = self._extract_two_q(qasm_word_arr[1])
        self._qubits_in_use[q_0] = 1
        self._qubits_in_use[q_1] = 1


    def _parse_qubit_map_line_qasm(self, qasm_line):
        qasm_word_arr = qasm_line.split(' ')
        qasm_dic = self._parse_qubit_map_dictionary()
        for qasm_rule in qasm_dic.keys():
            if qasm_word_arr[0].find(qasm_rule) == 0:
                qasm_f = qasm_dic[qasm_rule]
                qasm_f(qasm_word_arr)
                return
            else:
                self._parse_single_qubit_map_statement(qasm_line)

    def add_additional_qubits_if_necessary(self):
        for k in self._qubit_map_dic.keys():
            self._qubits_in_use.pop(k, None)

        max_key = max(self._qubit_map_dic, key=self._qubit_map_dic.get)
        max_value = self._qubit_map_dic[max_key]

        for i, k in enumerate(self._qubits_in_use.keys()):
            self._qubit_map_dic[k] = max_value + i + 1


    def _parse_qubit_map_qasm(self) -> dict:
        for i, qasm_line in enumerate(self.qasm_arr):
            if not qasm_line.strip().isspace() and len(qasm_line) > 1:
                self._parse_qubit_map_line_qasm(qasm_line)
        self.add_additional_qubits_if_necessary()
        return self._qubit_map_dic

    def get_simulator(self) -> sim.Simuliator:
        return self._simulator


def simulate_one(q, noise_dic=None) -> np.array:
    (qr, cr, qc) = q
    # print(qc.qasm())
    s = QASMTranslator(qc.qasm(), noise_dic)
    s.parse_qasm()
    s = s.get_simulator()
    s_dic = s.get_results_as_dic()
    s_arr = list(map(lambda k: s_dic[k][0], s_dic.keys()))
    return np.array(s_arr)

def get_system_length(qc):
    qubit_map = QASMTranslator(qc.qasm(), {})._parse_qubit_map_qasm()
    return len(qubit_map)

def simulate_melburne_one(qc, noise_dic=None) -> np.array:
    # print(qc.qasm())
    qubit_map = QASMTranslator(qc.qasm(), noise_dic)._parse_qubit_map_qasm()
    translator = QASMTranslator(qc.qasm(), noise_dic, qubit_map)
    translator.parse_qasm()
    s = translator.get_simulator()
    s_dic = s.get_results_as_dic()
    s_arr = list(map(lambda k: s_dic[k][0], s_dic.keys()))
    return np.array(s_arr)


def simulate_all(q_arr, noise_dic) -> pd.DataFrame:
    all_dic = {}
    for i, q in enumerate(q_arr):
        (qr, cr, qc) = q
        s = QASMTranslator(qc.qasm(), noise_dic)
        s.parse_qasm()
        s = s.get_simulator()
        s_dic = s.get_results_as_dic()
        s_arr = list(map(lambda k: s_dic[k][0], s_dic.keys()))
        all_dic[i] = s_arr
    df = pd.DataFrame(data=all_dic)
    return df
