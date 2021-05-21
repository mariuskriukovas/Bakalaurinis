from git.Bakalaurinis.tools.presentation_service import write_results_to_excel
from git.Bakalaurinis.analysis.analysis_tools import noise_results, preaty_print, get_sheet
from git.Bakalaurinis.tools.excel_tools import append_excel_sheets

import pandas as pd

def write_hhl_gate_results():
    write_results_to_excel("hhl_ibmq_local", "HHL")
    write_results_to_excel("hhl_ibmq_quito", "HHL")
    write_results_to_excel("hhl_ibmq_yorktown_Y", "HHL")


def write_m_gate_results():
    write_results_to_excel("measurement_gate_local", "M")
    write_results_to_excel("measurement_gate_ibmq_yorktown_Y", "M")
    write_results_to_excel("measurement_gate_ibmq_quito", "M")

# write_m_gate_results()

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

def write_i_ry_gate_results():
    write_results_to_excel("i_ry_gate_local", "ry")
    write_results_to_excel("i_ry_gate_yorktown_Y", "ry")
    write_results_to_excel("i_ry_gate_quito", "ry")


def write_i_rz_gate_results():
    write_results_to_excel("i_rz_gate_local", "rz")
    write_results_to_excel("i_rz_gate_yorktown_Y", "rz")
    write_results_to_excel("i_rz_gate_quito", "rz")


def write_i_p_gate_results():
    write_results_to_excel("i_p_gate_local", "p")
    write_results_to_excel("i_p_gate_yorktown_Y", "p")
    write_results_to_excel("i_p_gate_quito", "p")

# write_i_p_gate_results()

def write_n_i_gate_results():
    # write_results_to_excel("n_r_gate_local", "nr")
    # write_results_to_excel("n_r_gate_quito", "nr")
    write_results_to_excel("n_r_gate_yorktown_Y", "nr")

# write_n_i_gate_results()

def write_f_rotation_gate_results():
    write_results_to_excel("f_rx_gate_quito", "rx")
    write_results_to_excel("f_rx_gate_yorktown_Y", "rx")
    write_results_to_excel("f_ry_gate_yorktown_Y", "ry")

# write_f_rotation_gate_results()

def join_sheets(df_i, df_n):
    new_names = {}
    for i in range(0, 40):
        new_names[i] = 40 + i
    df_i = df_i.rename(columns=new_names)
    df = pd.concat([df_n, df_i], axis=1)
    return df

def write_join_f_rotation_gate_results():
    # df_i = get_sheet("Sheet_i_ry_gate_quito")
    # df_n = get_sheet("Sheet_quito_n_i_ry")
    # df = join_sheets(df_i, df_n)
    # append_excel_sheets([df], ["f_ry_gate_quito"])

    df_i = get_sheet("Sheet_i_rz_gate_quito")
    df_n = get_sheet("Sheet_quito_n_i_rz")
    df = join_sheets(df_i, df_n)
    append_excel_sheets([df], ["f_rz_gate_quito"])

    df_i = get_sheet("Sheet_i_p_gate_quito")
    df_n = get_sheet("Sheet_quito_n_i_p")
    df = join_sheets(df_i, df_n)
    append_excel_sheets([df], ["f_p_gate_quito"])

# write_join_f_rotation_gate_results()