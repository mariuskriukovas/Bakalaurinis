import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

from git.Bakalaurinis.simuliator.chart_drawer import draw_simple_plot
from git.Bakalaurinis.simuliator.math import count_linear_regresion
from git.Bakalaurinis.tools.excel_tools import write_to_excel, append_excel_sheets, get_excel_sheets
from git.Bakalaurinis.analysis.analysis_tools import noise_results, preaty_print


def m_gate_analysis():
    m_yorktown = noise_results(name = 'Sheet_yorktown_M_Aprox')
    m_quito = noise_results(name = 'Sheet_quito_M_Aprox')

    print("m_yorktown su ry vartais", m_yorktown )
    print("m_quito su ry vartais", m_quito)

def x_gate_analysis():
    x_quito_M1 = noise_results(name = 'Sheet_quito_X_Aprox_M1')
    x_yorktown_M1 = noise_results(name = 'Sheet_yorktown_M_Aprox_M1')
    x_quito_M2 = noise_results(name = 'Sheet_quito_M_Aprox_M2')
    x_yorktown_M2 = noise_results(name = 'Sheet_yorktown_M_Aprox_M2')

    print("x_quito_M1 su rx vartais", x_quito_M1)
    print("x_yorktown_M1 su rx vartais", x_yorktown_M1 )
    print("x_quito_M2 su rx vartais", x_quito_M2)
    print("x_yorktown_M2 su rx vartais", x_yorktown_M2 )


def h_gate_analysis():
    m_yorktown_rx = noise_results(name='Sheet_yorktown_H_Aprox')
    m_quito_rx = noise_results(name='Sheet_quito_H_Aprox')

    m_yorktown_ry = noise_results(name='Sheet_yorktown_H_Aprox_ry')
    m_quito_ry = noise_results(name='Sheet_quito_H_Aprox_ry')

    print("h_yorktown su rx vartais: ")
    preaty_print(m_yorktown_rx)
    print("h_quito su rx vartais :")
    preaty_print(m_quito_rx)

    print("h_yorktown su ry vartais :")
    preaty_print(m_yorktown_ry)
    print("h_quito su ry vartais :")
    preaty_print(m_quito_ry)

# h_gate_analysis()


def rx_gate_analysis():
    quito_rx = noise_results(name='Sheet_quito_rx_Aprox_r', e=0.21 )
    print(quito_rx)
    yorktown_rx = noise_results(name='Sheet_yorktown_rx_Aprox_radians', e=0.21 )
    print(yorktown_rx)

# rx_gate_analysis()

def ry_gate_analysis():
    quito_ry = noise_results(name='Sheet_quito_ry_Aprox', e=0.21 )
    print(quito_ry)
    yorktown_ry = noise_results(name='Sheet_yorktown_ry_Aprox', e=0.21 )
    print(yorktown_ry)


def rz_gate_analysis():
    quito_rz = noise_results(name='Sheet_quito_rz_Aprox', e=0.21 )
    print(quito_rz)
    yorktown_rz = noise_results(name='Sheet_yorktown_rz_Aprox', e=0.21 )
    print(yorktown_rz)

def p_gate_analysis():
    quito_p = noise_results(name='Sheet_quito_p_Aprox', e=0.21 )
    print(quito_p)
    yorktown_p = noise_results(name='Sheet_yorktown_p_Aprox', e=0.21 )
    print(yorktown_p)

def cx_gate_analysis():
    quito_cx = noise_results(name='Sheet_quito_cx_o_Aprox', e=0.03 )
    print(quito_cx)
    yorktown_cx = noise_results(name='Sheet_yorktown_cx_o_Aprox', e=0.03 )
    print(yorktown_cx)


# p_gate_analysis()
