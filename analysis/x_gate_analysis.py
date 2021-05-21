import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from git.Bakalaurinis.experiments.h_gate_experiment import prepare_h_gate_experiment
from git.Bakalaurinis.experiments.x_gate_experiment import prepare_x_gate_experiment
from git.Bakalaurinis.experiments.rotation_gate_experiments import prepare_rx_gate_experiment
from git.Bakalaurinis.simuliator.gates import np_gate, na_gate, gate_factory
from git.Bakalaurinis.simuliator.gates import X, I, rx_gate, rz_gate, ry_gate
from git.Bakalaurinis.analysis.analysis_tools import prepare_data, extract_most_probable_values, \
    plot_gate_results, count_distribution_between_gates, plot_single_gate_results
from git.Bakalaurinis.simuliator.translator import simulate_all
from git.Bakalaurinis.tools.excel_tools import get_excel_sheets

def x_gate_analysis():
    noise_quito_dic = {
        # 'M': gate_factory(ry_gate, 0.1913),
        # 'X': gate_factory(rx_gate, 0.503663),
        'M': gate_factory(ry_gate, 0.197125245579567),
        'X': gate_factory(rx_gate, 0.428607843137255),
    }

    noise_yorktown_dic = {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'X': gate_factory(rx_gate, 0.573896226415094),

        # 'M': gate_factory(rx_gate, 0.543),
        # 'X': gate_factory(rx_gate, 0.5950),
    }

    df_dic = prepare_data(quito_sheet='Sheet_quito_X',
                          yorktown_sheet='Sheet_yorktown_X',
                          local_sheet='Sheet_local_X',
                          experiment=prepare_x_gate_experiment,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    df = extract_most_probable_values(df_dic)
    print("------------", (df['Quito'].apply(np.array)).apply(np.linalg.norm))
    percent_diff = (df['Quito'].apply(np.array) - df['Sim_Quito'].apply(np.array)).apply(np.linalg.norm).mean()
    print("Quito percent_diff", percent_diff)
    percent_diff = (df['Yorktown'].apply(np.array) - df['Sim_Yorktown'].apply(np.array)).apply(np.linalg.norm).mean()
    print("Yorktown percent_diff", percent_diff)

    percent_diff = (df['Quito'].apply(np.array) - df['Qiskit'].apply(np.array)).apply(np.linalg.norm).mean()
    print("Quito percent_diff", percent_diff)

    percent_diff = (df['Yorktown'].apply(np.array) - df['Qiskit'].apply(np.array)).apply(np.linalg.norm).mean()
    print("Yorktown percent_diff", percent_diff)

    plot_gate_results(df, "X vartų triukšmai ir jų simuliacijos." )
    names_arr = ['Quito', 'Yorktown', 'Sim_Quito', 'Sim_Yorktown']
    df_dis = count_distribution_between_gates(df, names_arr)
    plot_single_gate_results(df_dis, "X vartų nuokrypiu vidurkiai")

# x_gate_analysis()

def h_gate_analysis_rx():
    noise_quito_dic = {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'H': gate_factory(rx_gate, 1.48866929133858),
    }

    noise_yorktown_dic = {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'H': gate_factory(rx_gate, 1.886),
    }

    df_dic = prepare_data(quito_sheet='Sheet_h_gate_quito',
                          yorktown_sheet='Sheet_h_gate_yorktown_Y',
                          local_sheet='Sheet_h_gate_local',
                          experiment=prepare_h_gate_experiment,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    df = extract_most_probable_values(df_dic)
    plot_gate_results(df, "H vartų eksperimento nuo labiausiai tikėtino rezultato")
    names_arr = ['Quito', 'Yorktown', 'My_Quito', 'My_Yorktown']
    df_dis = count_distribution_between_gates(df, names_arr)
    plot_single_gate_results(df_dis, "H vartų nuokrypiu vidurkiai")

# h_gate_analysis_rx()


def h_gate_analysis_ry():
    noise_quito_dic = {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'H': gate_factory(ry_gate, 2.99717391304345),
    }

    noise_yorktown_dic = {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'H': gate_factory(ry_gate, 2.95099999999998),
    }

    df_dic = prepare_data(quito_sheet='Sheet_h_gate_quito',
                          yorktown_sheet='Sheet_h_gate_yorktown_Y',
                          local_sheet='Sheet_h_gate_local',
                          experiment=prepare_h_gate_experiment,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    df = extract_most_probable_values(df_dic)
    plot_gate_results(df, "H vartų eksperimento nuo labiausiai tikėtino rezultato")
    names_arr = ['Quito', 'Yorktown', 'My_Quito', 'My_Yorktown']
    df_dis = count_distribution_between_gates(df, names_arr)
    plot_single_gate_results(df_dis, "H vartų nuokrypiu vidurkiai")

# h_gate_analysis_ry()
