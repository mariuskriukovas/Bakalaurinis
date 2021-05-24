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

    print(df_dic['Quito'].max())

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

    percent_diff = (df['Sim_Quito'].apply(np.array) - df['Qiskit'].apply(np.array)).apply(np.linalg.norm).mean()
    print("SimQuito percent_diff", percent_diff)

    percent_diff = (df['Sim_Yorktown'].apply(np.array) - df['Qiskit'].apply(np.array)).apply(np.linalg.norm).mean()
    print("SimYorktown percent_diff", percent_diff)

    plot_gate_results(df, "X vartų triukšmai ir jų simuliacijos." )
    names_arr = ['Quito', 'Yorktown', 'Sim_Quito', 'Sim_Yorktown']
    df_dis = count_distribution_between_gates(df, names_arr)
    plot_single_gate_results(df_dis, "X vartų nuokrypiu vidurkiai")

# x_gate_analysis()

def x_noise_simpe():
    noise_quito_dic = {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'X': gate_factory(rx_gate, 0.428607843137255),
    }
    noise_yorktown_dic = {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'X': gate_factory(rx_gate, 0.573896226415094),
    }

    df_dic = prepare_data(quito_sheet='Sheet_quito_X',
                          yorktown_sheet='Sheet_yorktown_X',
                          local_sheet='Sheet_local_X',
                          experiment=prepare_x_gate_experiment,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    df = pd.DataFrame(data={"val": list(range(0,32)),
                            "QuitoMax": df_dic['Quito'].max(),
                            "YorktownMax": df_dic['Yorktown'].max(),
                            "QiskitMax": df_dic['Qiskit'].max(),
                            })

    # df_dic['Quito'][1].to_numpy()
    np.transpose(df_dic['Quito'][0].apply(np.array))
    # print( ().apply(np.linalg.norm)).sum() )
    arr = (df_dic['Quito'][0].to_numpy())
    arr = np.transpose(arr)
    print("norma", np.linalg.norm(arr))

    df = pd.DataFrame(data={
        'Quito':  df['QuitoMax'],
        'Yorktown': df['YorktownMax'],
        'Qiskit':  df['QiskitMax']
    })

    def plot_single_gate_results(df_result, title):
        my_colors = ['green', 'red', 'black', 'purple']
        pic = df_result.plot(title=title, kind='line', lw=1, fontsize=6,
                             color=my_colors,
                             use_index=True)

        plt.ylabel('$c_i$')
        plt.xlabel('Eksperimentai $i$')
        plt.show()

    plot_single_gate_results(df, "X vartų ekeperimento vizualizacija")

# x_noise_simpe()

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

from git.Bakalaurinis.experiments.measurement_gate_experiment import prepare_measurement_gate_experiment
from git.Bakalaurinis.experiments.x_gate_experiment import prepare_x_gate_experiment
from git.Bakalaurinis.experiments.h_gate_experiment import prepare_h_gate_experiment
from git.Bakalaurinis.experiments.cx_experiment import prepare_cx_gate_experiment


def single_m_analysis():
    noise_quito_dic={
        'M': gate_factory(ry_gate, 0.197125245579567),
    }
    noise_yorktown_dic={
        'M': gate_factory(ry_gate, 0.279535050537985)
    }
    df_dic = prepare_data(quito_sheet='Sheet_quito_M',
                          yorktown_sheet='Sheet_yorktown_M',
                          local_sheet='Sheet_measurement_gate_local',
                          experiment=prepare_measurement_gate_experiment,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    print("Qiskit", "Quito", (df_dic['Qiskit'] - df_dic['Quito']).apply(np.linalg.norm).mean())
    print("Qiskit", "Yorktown", (df_dic['Qiskit'] - df_dic['Yorktown']).apply(np.linalg.norm).mean())

    print("Qiskit", "Sim_Quito",(df_dic['Qiskit'].drop(columns=[0])- df_dic['Sim_Quito'].drop(columns=[0])).apply(np.linalg.norm).mean())
    print("Qiskit", "Sim_Yorktown", (df_dic['Qiskit'].drop(columns=[0]) - df_dic['Sim_Yorktown'].drop(columns=[0])).apply(np.linalg.norm).mean())


def single_x_analysis():
    noise_quito_dic={
        'M': gate_factory(ry_gate, 0.197125245579567),
        'X': gate_factory(rx_gate, 0.428607843137255),
    }
    noise_yorktown_dic={
        'M': gate_factory(ry_gate, 0.279535050537985),
        'X': gate_factory(rx_gate, 0.573896226415094),
    }

    df_dic = prepare_data(quito_sheet='Sheet_quito_X',
                          yorktown_sheet='Sheet_yorktown_X',
                          local_sheet='Sheet_local_X',
                          experiment=prepare_x_gate_experiment,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    print("Qiskit", "Quito", (df_dic['Qiskit'] - df_dic['Quito']).apply(np.linalg.norm).mean())
    print("Qiskit", "Yorktown", (df_dic['Qiskit'] - df_dic['Yorktown']).apply(np.linalg.norm).mean())

    print("Qiskit", "Sim_Quito",(df_dic['Qiskit'] - df_dic['Sim_Quito']).apply(np.linalg.norm).mean())
    print("Qiskit", "Sim_Yorktown", (df_dic['Qiskit'] - df_dic['Sim_Yorktown']).apply(np.linalg.norm).mean())

def single_h_analysis():
    noise_quito_dic={
        'M': gate_factory(ry_gate, 0.197125245579567),
        'H': gate_factory(ry_gate, 3.0619239645489422),
    }
    noise_yorktown_dic={
        'M': gate_factory(ry_gate, 0.279535050537985),
        'H': gate_factory(ry_gate, 3.1743848797250),
    }

    df_dic = prepare_data(quito_sheet='Sheet_h_gate_quito',
                          yorktown_sheet='Sheet_h_gate_yorktown_Y',
                          local_sheet='Sheet_h_gate_local',
                          experiment=prepare_h_gate_experiment,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    print("Qiskit", "Quito", (df_dic['Qiskit'] - df_dic['Quito']).apply(np.linalg.norm).mean())
    print("Qiskit", "Yorktown", (df_dic['Qiskit'] - df_dic['Yorktown']).apply(np.linalg.norm).mean())

    print("Qiskit", "Sim_Quito",(df_dic['Qiskit'] - df_dic['Sim_Quito']).apply(np.linalg.norm).mean())
    print("Qiskit", "Sim_Yorktown", (df_dic['Qiskit'] - df_dic['Sim_Yorktown']).apply(np.linalg.norm).mean())


# single_h_analysis()



def single_cx_analysis():
    noise_quito_dic={
        'M': gate_factory(ry_gate, 0.197125245579567),
        'X': gate_factory(rx_gate, 0.428607843137255),
        'CX': gate_factory(rx_gate, 0.4698968668407313),
    }
    noise_yorktown_dic={
        'M': gate_factory(ry_gate, 0.279535050537985),
        'X': gate_factory(rx_gate, 0.573896226415094),
        'CX': gate_factory(rx_gate, 0.682),
    }
    def mm():
       return prepare_cx_gate_experiment(True)
    df_dic = prepare_data(quito_sheet='Sheet_cx_gate_quito_o',
                          yorktown_sheet='Sheet_cx_gate_yorktown_o_Y',
                          local_sheet='Sheet_cx_gate_local_o',
                          experiment=mm,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    print("Qiskit", "Quito", (df_dic['Qiskit'] - df_dic['Quito']).apply(np.linalg.norm).mean())
    print("Qiskit", "Yorktown", (df_dic['Qiskit'] - df_dic['Yorktown']).apply(np.linalg.norm).mean())

    print("Qiskit", "Sim_Quito",(df_dic['Qiskit'] - df_dic['Sim_Quito']).apply(np.linalg.norm).mean())
    print("Qiskit", "Sim_Yorktown", (df_dic['Qiskit'] - df_dic['Sim_Yorktown']).apply(np.linalg.norm).mean())

single_cx_analysis()