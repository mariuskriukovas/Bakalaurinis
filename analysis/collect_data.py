from git.Bakalaurinis.tools.presentation_service import write_results_to_excel


def write_hhl_gate_results():
    write_results_to_excel("hhl_ibmq_local", "HHL")
    write_results_to_excel("hhl_ibmq_quito", "HHL")
    write_results_to_excel("hhl_ibmq_yorktown_Y", "HHL")


def write_m_gate_results():
    write_results_to_excel("measurement_gate_local", "M")
    write_results_to_excel("measurement_gate_ibmq_yorktown_Y", "M")
    write_results_to_excel("measurement_gate_ibmq_quito", "M")


def write_cx_gate_results():
    write_results_to_excel("cx_gate_local_o", "cx_one")
    write_results_to_excel("cx_gate_local_z", "cx_zero")
    write_results_to_excel("cx_gate_quito_o", "cx_one")
    write_results_to_excel("cx_gate_quito_z", "cx_zero")
    write_results_to_excel("cx_gate_yorktown_o_Y", "cx_one")
    write_results_to_excel("cx_gate_yorktown_z_Y", "cx_zero")


def write_h_gate_results():
    write_results_to_excel("h_gate_local", "H")
    write_results_to_excel("h_gate_yorktown_Y", "H")
    write_results_to_excel("h_gate_quito", "H")


def write_rx_gate_results():
    write_results_to_excel("rx_gate_local", "rx")
    write_results_to_excel("rx_gate_yorktown_Y", "rx")
    write_results_to_excel("rx_gate_quito", "rx")


def write_ry_gate_results():
    write_results_to_excel("ry_gate_local", "ry")
    write_results_to_excel("ry_gate_yorktown_Y", "ry")
    write_results_to_excel("ry_gate_quito", "ry")


def write_rz_gate_results():
    write_results_to_excel("rz_gate_local", "rz")
    write_results_to_excel("rz_gate_yorktown_Y", "rz")
    write_results_to_excel("rz_gate_quito", "rz")


def write_p_gate_results():
    write_results_to_excel("p_gate_local", "p")
    write_results_to_excel("p_gate_yorktown_Y", "p")
    write_results_to_excel("p_gate_quito", "p")
