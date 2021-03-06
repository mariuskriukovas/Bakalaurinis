import random
import numpy as np
import pandas as pd
from git.Bakalaurinis.analysis.analysis_tools import prepare_data, extract_most_probable_values, \
    plot_gate_results, count_distribution_between_gates, plot_single_gate_results
from git.Bakalaurinis.experiments.rotation_gate_experiments import prepare_rx_gate_experiment
from git.Bakalaurinis.simuliator.gates import gate_factory
from git.Bakalaurinis.simuliator.gates import ry_gate


def rx_noise(theta):
    if 0<= theta < np.pi/3:
       return random.uniform(0, -0.0136458975364205)
    if np.pi/3 <= theta < 2*np.pi/3:
       return random.uniform(-0.0136458975364205, -0.0575545879784532)
    if 2*np.pi/3 <= theta < 3*np.pi/3:
       return random.uniform(-0.0575545879784532, 0.174738087634757)
    if 3*np.pi/3 <= theta < 4*np.pi/3:
       return random.uniform(0.174738087634757, -0.408655577625011)
    if 4*np.pi/3 <= theta < 5*np.pi/3:
       return random.uniform(-0.408655577625011, -0.235673964109191)
    if 5*np.pi/3 <= theta <= 6*np.pi/3:
       return random.uniform(0.235673964109191,0.0123473931975008)
    return random.uniform(-0.2, 0.2)

def rx_gate_analysis():
    noise_quito_dic = {
        'M': gate_factory(ry_gate, 0.197125245579567),
        'NRx': rx_noise,
    }

    noise_yorktown_dic = {
        'M': gate_factory(ry_gate, 0.279535050537985),
    }

    df_dic = prepare_data(quito_sheet='Sheet_rx_gate_quito',
                          yorktown_sheet='Sheet_rx_gate_yorktown_Y',
                          local_sheet='Sheet_rx_gate_local',
                          experiment=prepare_rx_gate_experiment,
                          noise_quito_dic=noise_quito_dic,
                          noise_yorktown_dic=noise_yorktown_dic)

    df = extract_most_probable_values(df_dic)
    print(df)
    n_df = pd.DataFrame(data={'Quito': df['Quito'], 'Yorktown': df['Yorktown'], 'Qiskit': df['Qiskit']})
    n_df= n_df.loc[: 192]
    plot_gate_results(n_df, "RX vartų nuokrypiai nuo labiausiai tikėtinos būsenos")
    names_arr = ['Quito', 'Yorktown', 'Sim_Quito', 'Sim_Yorktown']
    df_dis = count_distribution_between_gates(df, names_arr)
    plot_single_gate_results(df_dis, "RX vartų nuokrypiu vidurkiai")

# rx_gate_analysis()

from git.Bakalaurinis.experiments.rotation_gate_experiments import prepare_rotation_experiment, init_rx_gates
import matplotlib.pyplot as plt
from git.Bakalaurinis.analysis.noise_interval_analysis import get_full_rotation_interval

def rx_gate_simple_analysis():
    def t():
        return prepare_rotation_experiment(init_rx_gates)
    df_dic = prepare_data(quito_sheet='Sheet_f_rx_gate_quito',
                          yorktown_sheet='Sheet_f_rx_gate_local',
                          local_sheet='Sheet_f_rx_gate_yorktown_Y',
                          experiment=t,
                          noise_quito_dic={},
                          noise_yorktown_dic={})

    # print(df_dic['Quito'].iloc[0])

    def plot_single_gate_results(df_result, title):
        my_colors = ['green', 'red', 'black', 'purple']
        pic = df_result.plot(title=title, kind='line', lw=1, fontsize=6,
                             color=my_colors,
                             use_index=True)

        plt.ylabel('Tikimybės $x_i$')
        plt.xlabel('Eksprimentai intervale $ \phi \in [-2\pi, 2\pi]$')
        plt.show()

    df = pd.DataFrame(data= {
        'Qiskit|00000⟩' : df_dic['Qiskit'].iloc[0],
        'Qiskit|11111⟩':df_dic['Qiskit'].iloc[31],
        'Yorktown|00000⟩':df_dic['Yorktown'].iloc[0],
        'Yorktown|11111⟩':df_dic['Yorktown'].iloc[31],
    })

    r_arr = get_full_rotation_interval()
    df['index'] = r_arr
    df = df.set_index('index')
    plot_single_gate_results(df, "RX vartų ekeperimento vizualizacija")


rx_gate_simple_analysis()