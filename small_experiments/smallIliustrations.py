from git.Bakalaurinis.simuliator.simuliator import Simuliator
from git.Bakalaurinis.simuliator.gates import X, I, H, Z, Y, M, SimpleGate
from git.Bakalaurinis.simuliator.gates import rx_gate, ry_gate, get_zero_ket
from git.Bakalaurinis.simuliator.math import tensor_arr
from git.Bakalaurinis.simuliator.translator import simulate_all
from git.Bakalaurinis.experiments.x_gate_experiment import prepare_x_gate_experiment
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit_textbook.widgets import plot_bloch_vector_spherical
from git.Bakalaurinis.tools.transple import transpile_to_yorktown
from git.Bakalaurinis.simuliator.gates import np_gate, na_gate, gate_factory


import git.Projektinis.tools.simulators as tools
import git.Projektinis.tools.functions as funct

import numpy as np
import matplotlib.pyplot as plt


def vertical_iteration_example():
    simuliator = Simuliator(3)
    simuliator.add_single_gates([(0, X), (1, X), (2, X)])
    simuliator.measure()
    print(simuliator.get_results())
    simuliator.show_circuit("Vertikali topologija")
    plt.show()

def horizontal_iteration_example():
    simuliator = Simuliator(3)
    simuliator.add_single_gates([(0, X)])
    simuliator.add_single_gates([(0, X)])
    simuliator.add_single_gates([(0, X)])
    simuliator.measure()
    simuliator.show_circuit("Horizontali topologija")
    plt.show()

def test_circut():
    qr = QuantumRegister(3, "qr")
    cr = ClassicalRegister(3, "cr")
    qc = QuantumCircuit(qr, cr)
    qc.x(qr[0])
    qc.cx(qr[0], qr[1])
    qc.u1(np.pi/2, qr[0])
    qc.u2(np.pi/4, 2 * np.pi, qr[1])
    qc.u3(0, np.pi / 4, 2 * np.pi / 4, qr[2])
    qc.barrier()
    qc.measure(qr[0], cr[0])
    qc.measure(qr[1], cr[1])
    qc.measure(qr[2], cr[2])
    print(qc.qasm())
    qc.draw(output='mpl')
    tools.simulate_and_show_result(qc)
    plt.show()

def count_theta_and_fi(state_value):
    ket_zero = state_value[0]
    ket_one = state_value[1]
    theta = np.arccos(ket_zero)
    sin_fi = np.sin(theta)
    log_val = ket_one/sin_fi
    log = np.log(log_val)
    fi = log / 1j
    return (2 * theta, fi)



def prepare_scheme():
    qr = QuantumRegister(1, "qr")
    cr = ClassicalRegister(1, "cr")
    qc = QuantumCircuit(qr, cr)
    return (qr,cr,qc)

def zero_rotation():
    (qr, cr, qc) = prepare_scheme()
    # qc.measure(qr[0], cr[0])  # measure q[1] -> c[0];
    tools.simulate_bloch_sphere(qc, "|0>")

def x_rotation():
    (qr, cr, qc) = prepare_scheme()
    qc.x(qr[0])
    state_value = tools.simulate_state_value(qc)
    theta, fi = count_theta_and_fi(state_value)
    print( f' \Theta = {theta} \Phi = {fi}')
    # Paulio - X
    tools.simulate_bloch_sphere(qc, 'Paulio - X \n $\Theta =  \pi ; \Phi = 0 $')
    plt.show()

# x_rotation()

def h_rotation():
    (qr, cr, qc) = prepare_scheme()
    qc.h(qr[0])

    state_value = tools.simulate_state_value(qc)
    theta, fi = count_theta_and_fi(state_value)
    print(f' \Theta = {theta} \Phi = {fi}')
    # "Hadamardo - H"
    tools.simulate_bloch_sphere(qc, 'Hadamardo - H \n $\Theta = \\frac{\pi}{2} ; \Phi = 0$')
    plt.show()

# h_rotation()


def z_rotation():
    (qr, cr, qc) = prepare_scheme()

    qc.h(qr[0])
    qc.z(qr[0])
    qc.h(qr[0])

    state_value = tools.simulate_state_value(qc)
    funct.to_latex(state_value)
    # print(state_value)
    # theta, fi = count_theta_and_fi(state_value)
    # print( f' \Theta = {theta} \Phi = {fi}')

    tools.simulate_bloch_sphere(qc, 'H + Z \n $\Theta = \\frac{\pi}{2} ; \Phi = \pi$')
    plt.show()

# z_rotation()

def y_rotation():
    (qr, cr, qc) = prepare_scheme()

    qc.y(qr[0])

    state_value = tools.simulate_state_value(qc)
    theta, fi = count_theta_and_fi(state_value)
    print( f' \Theta = {theta} \Phi = {fi}')

    tools.simulate_bloch_sphere(qc, 'Y \n $\Theta = \pi ; \Phi = \\frac{\pi}{2}$')
    plt.show()

# y_rotation()

def double_check():
    # coords = [np.pi, 0, 1]  # [Theta, Phi, Radius] x
    # coords = [np.pi / 2, 0, 1]  # [Theta, Phi, Radius] h
    # coords = [np.pi / 2, np.pi, 1]  # [Theta, Phi, Radius] h + z
    coords = [np.pi, np.pi / 2, 1]  # [Theta, Phi, Radius] y
    plot_bloch_vector_spherical(coords)
    plt.show()

# double_check()

def cx_experiment():
    qr = QuantumRegister(5, "qr")
    cr = ClassicalRegister(5, "cr")
    qc = QuantumCircuit(qr, cr)

    qc.x(qr[0])
    qc.y(qr[0])
    qc.z(qr[0])

    qc.cx(qr[0], qr[4])
    qc.cx(qr[1], qr[4])
    qc.cx(qr[2], qr[4])
    qc.cx(qr[3], qr[4])

    # qc.cx(qr[0], qr[2])
    qc.draw(output='mpl')
    qc_y = transpile_to_yorktown(qc)
    qc_y.draw(output='mpl')
    plt.show()

# cx_experiment()
# zero_rotation()
# h_rotation()
# x_rotation()
# z_rotation()
# test_circut()
# vertical_iteration_example()
# horizontal_iteration_example()

def countRX_values():
    rx = []
    for i in range(0,5):
        rx.append(rx_gate.get_value(0.232))

    v = np.matmul(tensor_arr(rx), get_zero_ket(32))
    funct.to_latex(v)
    funct.printProb(v)


def countX_values():

    df = simulate_all([prepare_x_gate_experiment()[30]], {'M': gate_factory(ry_gate,0.1971252), 'X':gate_factory(rx_gate,0.46989686)})
    print(df)
    # funct.printProb(v)

countX_values()
# # countRX_values()