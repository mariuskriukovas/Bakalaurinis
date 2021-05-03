import git.Bakalaurinis.simuliator.simuliator as sim
from git.Bakalaurinis.simuliator.gates import X, I, H, Z, Y, SimpleGate
from git.Bakalaurinis.simuliator.gates import rx_gate, ry_gate, rz_gate, u_gate, p_gate
import numpy as np
import pandas as pd
import re


class QASMTranslator:
    def __init__(self, qasm_str, q_noise = None):
        self.qasm_str = qasm_str
        self.qasm_arr = qasm_str.split('\n')
        self.q_noise = q_noise

        self._n_q = None
        self._simulator = None
        self._statements_arr = []
        self._measured = False

        self._parse_qasm()

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
        self._n_q = int(self._parse_square_bracket_content(qasm_word_arr[1])[0])
        self._simulator = sim.Simuliator(self._n_q, self.q_noise)

    def _parse_creg_statement(self, qasm_word_arr):
        # only all register measurement supported
        for i in range(0, self._n_q):
            self._add_statement((i, I))

    def _extract_theta(self, qasm_word) -> float:
        theta = self._parse_round_bracket_content(qasm_word)[0]
        theta = theta.replace("pi", "np.pi")
        return float(eval(theta))

    def _extract_q(self, qasm_word) -> int:
        return int(self._parse_square_bracket_content(qasm_word)[0])

    def _extract_two_q(self, qasm_word) -> (int, int):
        return int(self._parse_square_bracket_content(qasm_word)[0]), \
               int(self._parse_square_bracket_content(qasm_word)[1])

    def _extract_theta_and_q(self, qasm_word_arr) -> (float, int):
        return (self._extract_theta(qasm_word_arr[0]), self._extract_q(qasm_word_arr[1]))

    def _parse_ry_statement(self, qasm_word_arr):
        (theta, q) = self._extract_theta_and_q(qasm_word_arr)
        ry = SimpleGate(ry_gate.get_adjusted_name(theta), ry_gate.get_value(theta))
        self._add_statement((q, ry))

    def _parse_rx_statement(self, qasm_word_arr):
        (theta, q) = self._extract_theta_and_q(qasm_word_arr)
        rx = SimpleGate(rx_gate.get_adjusted_name(theta), rx_gate.get_value(theta))
        self._add_statement((q, rx))

    def _parse_rz_statement(self, qasm_word_arr):
        (theta, q) = self._extract_theta_and_q(qasm_word_arr)
        rz = SimpleGate(rz_gate.get_adjusted_name(theta), rz_gate.get_value(theta))
        self._add_statement((q, rz))

    def _parse_barrier_statement(self, qasm_word_arr):
        # barrier in qiskit only for representation
        statement = "barrier"

    def _parse_p_statement(self, qasm_word_arr):
        print(qasm_word_arr)
        (theta, q) = self._extract_theta_and_q(qasm_word_arr)
        p = SimpleGate(p_gate.get_adjusted_name(theta), p_gate.get_value(theta))
        self._add_statement((q, p))

    def _parse_u_statement(self, qasm_word_arr):
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
        # only all register measurement supported
        if not self._measured:
            self._measured = True

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
            "u": self._parse_u_statement,
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

    def _parse_qasm(self):
        for i, qasm_line in enumerate(self.qasm_arr):
            if not qasm_line.strip().isspace() and len(qasm_line) > 1:
                self._parse_line_qasm(qasm_line)

        if len(self._statements_arr) > 0:
            self._simulator.add_single_gates(self._statements_arr)

        if self._measured:
            self._simulator.measure()

    def get_simulator(self) -> sim.Simuliator:
        return self._simulator


def simulate_one(q, noise_dic = None) -> np.array:
    (qr, cr, qc) = q
    s = QASMTranslator(qc.qasm(), noise_dic).get_simulator()
    s_dic = s.get_results_as_dic()
    s_arr = list(map(lambda k: s_dic[k][0], s_dic.keys()))
    return np.array(s_arr)


def simulate_all(q_arr, noise_dic) -> pd.DataFrame:
    all_dic = {}
    for i, q in enumerate(q_arr):
        (qr, cr, qc) = q
        s = QASMTranslator(qc.qasm(), noise_dic).get_simulator()
        s_dic = s.get_results_as_dic()
        s_arr = list(map(lambda k: s_dic[k][0],  s_dic.keys()))
        all_dic[i] = s_arr
    df = pd.DataFrame(data=all_dic)
    return df