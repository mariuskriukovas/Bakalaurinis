import numpy as np
from git.Bakalaurinis.simuliator.math import mul_arr

ROUND = 8

class Gate:
    def __init__(self, name, formula):
        self.name = name
        self.formula = formula

    def get_value(self, psi):
        return self.formula(psi)

    def get_adjusted_name(self, val):
        return str(self.name + "(" + str(val) + ")")

    def get_name(self):
        return self.name

    def print(self, psi=np.pi):
        print("<----------------------->")
        print(self.name)
        print(self.formula(psi))
        print("<----------------------->")


def init_rx_gate():
    def gate(psi):
        Rx = np.array([
            [np.round(np.cos(psi / 2), ROUND), (np.round(np.sin(psi / 2), ROUND)) * (-1j)], #LOX
            [(np.round(np.sin(psi / 2), ROUND)) * (-1j), np.round(np.cos(psi / 2), ROUND), ],
        ])
        return Rx

    return Gate('Rx', gate)


def init_ry_gate():
    def gate(psi):
        Ry = np.array([
            [np.round(np.cos(psi / 2), ROUND), np.round(-np.sin(psi / 2), ROUND), ],
            [np.round(np.sin(psi / 2), ROUND), np.round(np.cos(psi / 2), ROUND), ],
        ])
        return Ry

    return Gate('Ry', gate)


def init_rz_gate():
    def gate(psi):
        Rz = np.array([
            [np.round(np.exp(((psi / 2) * (-1j))), ROUND), 0, ],
            [0, np.round(np.exp(((psi / 2) * (1j))), ROUND)],
        ])
        return Rz

    return Gate("Rz", gate)


def init_p_gate():
    def gate(lamb):
        gt = np.array([
            [1, 0, ],
            [0, np.round(np.exp(((lamb) * (1j))), ROUND)],
        ])
        return gt

    return Gate("P", gate)


def init_N_amp_gate():
    def gate(lamb):
        gt = np.array([
            [0, 1],
            [0, 0],
        ])
        gt = np.sqrt(lamb) * gt
        return gt

    return Gate("Na", gate)


def init_N_phase_gate():
    def gate(lamb):
        gt = np.array([
            [1, 0],
            [0, -1],
        ])
        gt = np.sqrt(lamb) * gt
        return gt

    return Gate("Np", gate)


def init_N_x_gate():
    def gate(lamb):
        gt = np.array([
            [1, 0],
            [0, 1]
        ])
        gt = np.sqrt(lamb) * gt
        return gt

    return Gate("NX", gate)


def init_u_gate():
    def gate(par):
        (teta, fi, lamb) = par
        gt = np.array([
            [np.cos(teta / 2), -1 * np.round(np.exp(((lamb) * (1j))), ROUND) * np.sin(teta / 2), ],
            [np.round(np.exp(((fi) * (1j))), ROUND) * np.sin(teta / 2),
             np.round(np.exp(((fi + lamb) * (1j))), ROUND) * np.cos(teta / 2)],
        ])
        return gt

    return Gate("U", gate)


rx_gate = init_rx_gate()
ry_gate = init_ry_gate()
rz_gate = init_rz_gate()
p_gate = init_p_gate()


# U1(??)=ei??/2RZ(??)
def init_u1_gate():
    def gate(par):
        (lamb) = par
        gt = np.round(np.exp((((lamb) * (1j)) / 2)), ROUND) * rz_gate.get_value(lamb)
        # gt = np.array([
        #     [1, 0 ],
        #     [0 , np.round(np.exp(((lamb) * (1j))), ROUND)],
        # ])

        return gt

    return Gate("U1", gate)


def init_u2_gate():
    def gate(par):
        (fi, lamb) = par
        gt = mul_arr([
            rz_gate.get_value(fi),
            ry_gate.get_value(np.pi / 2),
            rz_gate.get_value(lamb)])

        # gt = (1/np.sqrt(2)) * np.array([
        #     [ 1 , -1 * np.round(np.exp(((lamb) * (1j))), ROUND)   ],
        #     [np.round(np.exp(((fi) * (1j))), ROUND) , np.round(np.exp(((fi + lamb) * (1j))), ROUND)],
        # ])

        return gt

    return Gate("U2", gate)


# U3(??,??,??)=RZ(??)RX(?????/2)RZ(??)RX(??/2)RZ(??)
def init_u3_gate():
    def gate(par):
        (teta, fi, lamb) = par
        # ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        gt = mul_arr([
            rz_gate.get_value(fi),
            rx_gate.get_value(-np.pi / 2),
            rz_gate.get_value(teta),
            rx_gate.get_value(np.pi / 2),
            rz_gate.get_value(lamb)]
        )

        # gt = np.array([
        #     [np.cos(teta / 2), -1 * np.round(np.exp(((lamb) * (1j))), ROUND) * np.sin(teta / 2), ],
        #     [np.round(np.exp(((fi) * (1j))), ROUND) * np.sin(teta / 2),
        #      np.round(np.exp(((fi + lamb) * (1j))), ROUND) * np.cos(teta / 2)],
        # ])

        return gt

    return Gate("U3", gate)


u_gate = init_u_gate()
u1_gate = init_u1_gate()
u2_gate = init_u2_gate()
u3_gate = init_u3_gate()

na_gate = init_N_amp_gate()
np_gate = init_N_phase_gate()
nx_gate = init_N_x_gate()


class SimpleGate:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def apply_noise(self, noise_gate):
        print(self.value)
        print(noise_gate.get_value())
        self.value = np.matmul(noise_gate.get_value(),
                               self.value)
        print(self.value)

    def print(self):
        print("<----------------------->")
        print(self.name)
        print(self.value)
        print("<----------------------->")


CZ = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, -1]
])

CZ = SimpleGate('CZ', CZ)

CXq0q1 = np.array([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0]
])

CXq0q1 = SimpleGate('CXq0q1', CXq0q1)

CXq1q0 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
])

CXq1q0 = SimpleGate('CXq1q0', CXq1q0)

I = np.array([
    [1, 0],
    [0, 1],
])

M = SimpleGate('M', I)
I = SimpleGate('I', I)
C = SimpleGate('C', I)

Z = np.array(
    [[1, 0],
     [0, -1]]
)

Z = SimpleGate('Z', Z)

X = np.array(
    [[0, 1],
     [1, 0]]
)

X = SimpleGate('X', X)

H = (1 / np.sqrt(2)) * np.array(
    [[1, 1],
     [1, -1]]
)

H = SimpleGate('H', H)

Y = np.array(
    [[0, -1j],
     [1j, 0]]
)

Y = SimpleGate('Y', Y)


def get_zero_ket(n):
    zero = np.array([1])
    for i in range(1, n):
        zero = np.append(zero, [0])
    return zero


def gate_factory(gate, value):
    return SimpleGate(f'Nois({gate.get_adjusted_name(value)})',
                      gate.get_value(value))
