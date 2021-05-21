import matplotlib.pyplot as plt
from qiskit.test.mock import FakeYorktown, FakeMelbourne
from qiskit.visualization import plot_gate_map
from qiskit import transpile


def show_yorktown_gate_map():
    yorktown = FakeYorktown()
    plot_gate_map(yorktown)
    plt.show()

def transpile_to_yorktown(qc):
    yorktown = FakeYorktown()
    t_qc = transpile(qc, yorktown)
    return t_qc

def transpile_to_melbourne(qc):
    melbourne = FakeMelbourne()
    t_qc = transpile(qc, melbourne)
    return t_qc