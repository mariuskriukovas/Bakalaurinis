from git.Bakalaurinis.tools.excel_tools import get_excel_sheets
from git.Bakalaurinis.experiments.hhl_optimised import prepare_hhl_optimised_gate_experiment
from git.Bakalaurinis.simuliator.translator import simulate_all
from git.Bakalaurinis.simuliator.gates import np_gate, na_gate, gate_factory
from git.Bakalaurinis.simuliator.gates import X, I, rx_gate, rz_gate, ry_gate
from git.Bakalaurinis.simuliator.translator import simulate_one

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


def get_sheet_df(name):
    sheets = get_excel_sheets([name])
    return sheets[name]


def get_hhl_index():
    arr = []
    i = 0
    while i < 2 * np.pi:
        arr.append(i)
        i += 0.1
    return arr


def plot_hll_graphic_qiskit(df, title):
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df.plot(title=title, kind='line', lw=1, fontsize=6,
                  color=my_colors,
                  use_index=True)

    plt.show()


def smother_results(df_a, df_b):
    sum = df_a + df_b
    df_a = df_a / sum
    df_b = df_b / sum
    return df_a, df_b


def rotation_noise(theta, arr):
    while theta < 0:
        theta += 2 * np.pi

    if theta % np.pi < 0.1:
        return random.uniform(-1 * arr[0], arr[0])

    for i in range(len(arr) - 1):
        from_i = i * np.pi / 3
        to_i = (i + 1) * np.pi / 3
        print(from_i, " ", to_i)
        if from_i <= theta < to_i:
            return random.uniform(arr[i], arr[i + 1])

    return random.uniform(-1 * arr[0], arr[0])


def rx_noise(i):
    arr = [-0.013645898,
           -0.057554588,
           0.174738088,
           -0.408655578,
           -0.235673964,
           0.012347393,
           -0.02063659]
    return rotation_noise(i, arr)


def ry_noise(i):
    arr = [-0.388736915,
           -0.301037393,
           -0.275620766,
           -0.618625414,
           -0.155021223,
           -0.16215355,
           -0.378719374]
    return rotation_noise(i, arr)


def rz_noise(i):
    arr = [0.124224238,
           -0.847456865,
           -1.880796327,
           -1.880796327,
           2.033744165,
           1.192523755,
           0.140498261]
    return rotation_noise(i, arr)


def p_noise(i):
    arr = [0.078294582,
           -0.804375872,
           0.089249791,
           0.089249791,
           1.750768295,
           1.136874128,
           0.078919582]
    return rotation_noise(i, arr)


def just_noise(theta):
    if 0 <= theta < np.pi / 3:
        return random.uniform(0, -0.0136458975364205)
    if np.pi / 3 <= theta < 2 * np.pi / 3:
        return random.uniform(-0.0136458975364205, -0.0575545879784532)
    if 2 * np.pi / 3 <= theta < 3 * np.pi / 3:
        return random.uniform(-0.0575545879784532, 0.174738087634757)
    if 3 * np.pi / 3 <= theta < 4 * np.pi / 3:
        return random.uniform(0.174738087634757, -0.408655577625011)
    if 4 * np.pi / 3 <= theta < 5 * np.pi / 3:
        return random.uniform(-0.408655577625011, -0.235673964109191)
    if 5 * np.pi / 3 <= theta <= 6 * np.pi / 3:
        return random.uniform(0.235673964109191, 0.0123473931975008)
    return random.uniform(-0.2, 0.2)


#################################################################

def t_rx_noise(theta):
    while theta < 0:
        theta += 2 * np.pi

    if 0 <= theta < np.pi / 3:
        return random.uniform(-0.0136458975364205, -0.0575545879784532)
    if np.pi / 3 <= theta < 2 * np.pi / 3:
        return random.uniform(-0.0575545879784532, 0.174738087634757)
    if 2 * np.pi / 3 <= theta < 3 * np.pi / 3:
        return random.uniform(0.174738087634757, -0.408655577625011)
    if 3 * np.pi / 3 <= theta < 4 * np.pi / 3:
        return random.uniform(-0.408655577625011, -0.235673964109191)
    if 4 * np.pi / 3 <= theta < 5 * np.pi / 3:
        return random.uniform(-0.235673964109191, 0.0123473931975008)
    if 5 * np.pi / 3 <= theta <= 6 * np.pi / 3:
        return random.uniform(0.0123473931975008, -0.0206365901290871)
    return random.uniform(-0.2, 0.2)


def t_ry_noise(theta):
    if theta < 0:
        return 0
    if 0 <= theta < np.pi / 3:
        return random.uniform(-0.0136458975364205, -0.301037392819514)
    if np.pi / 3 <= theta < 2 * np.pi / 3:
        return random.uniform(-0.301037392819514, -0.275620766137173)
    if 2 * np.pi / 3 <= theta < 3 * np.pi / 3:
        return random.uniform(-0.275620766137173, -0.618625414317006)
    if 3 * np.pi / 3 <= theta < 4 * np.pi / 3:
        return random.uniform(-0.618625414317006, -0.15502122326441)
    if 4 * np.pi / 3 <= theta < 5 * np.pi / 3:
        return random.uniform(-0.15502122326441, -0.16215354996272)
    if 5 * np.pi / 3 <= theta <= 6 * np.pi / 3:
        return random.uniform(-0.16215354996272, -0.378719373514822)
    return random.uniform(-0.2, 0.2)


def t_rz_noise(theta):
    if theta < 0:
        return 0
    if 0 <= theta < np.pi / 3:
        return random.uniform(0.124224238366198, -0.847456864602296)
    if np.pi / 3 <= theta < 2 * np.pi / 3:
        return random.uniform(-0.847456864602296, -1.88079632679498)
    if 2 * np.pi / 3 <= theta < 3 * np.pi / 3:
        return random.uniform(-1.88079632679498, -1.88079632679498)  # cia gali blgai
    if 3 * np.pi / 3 <= theta < 4 * np.pi / 3:
        return random.uniform(-1.88079632679498, 2.03374416456088)
    if 4 * np.pi / 3 <= theta < 5 * np.pi / 3:
        return random.uniform(2.03374416456088, 1.19252375475454)
    if 5 * np.pi / 3 <= theta <= 6 * np.pi / 3:
        return random.uniform(1.19252375475454, 0.140498261426351)
    return random.uniform(-0.2, 0.2)


def t_p_noise(theta):
    if theta < 0:
        return 0
    if 0 <= theta < np.pi / 3:
        return random.uniform(0.0782945822960138, -0.804375872249441)
    if np.pi / 3 <= theta < 2 * np.pi / 3:
        return random.uniform(-0.804375872249441, 0.0892497912951646)
    if 2 * np.pi / 3 <= theta < 3 * np.pi / 3:
        return random.uniform(0.0892497912951646, 0.0892497912951646)  # cia gali blgai
    if 3 * np.pi / 3 <= theta < 4 * np.pi / 3:
        return random.uniform(0.0892497912951646, 1.75076829473927)
    if 4 * np.pi / 3 <= theta < 5 * np.pi / 3:
        return random.uniform(1.75076829473927, 1.13687412775056)
    if 5 * np.pi / 3 <= theta <= 6 * np.pi / 3:
        return random.uniform(1.13687412775056, 0.0789195822960138)
    return random.uniform(-0.2, 0.2)


#################################################################


from git.Bakalaurinis.analysis.noise_interval_analysis import f_quito_p_noise, f_quito_ry_noise, f_quito_rz_noise
from git.Bakalaurinis.analysis.noise_interval_analysis import f_yorktown_p_noise, f_yorktown_ry_noise, f_yorktown_rz_noise

# important to count only one time
rz_q = f_quito_rz_noise()
ry_q = f_quito_ry_noise()
p_q = f_quito_p_noise()
#
# rz_y = f_yorktown_rz_noise()
# ry_y = f_yorktown_ry_noise()
# p_y = f_yorktown_p_noise()

def f_factory(f):
    def adjusted_f(psi):
        psi = psi % 2 * np.pi
        e = 0.1
        return random.uniform(-1* (1 + e) * f(psi), (1 + e) *  f(psi))
        # return  f(psi)

    return adjusted_f



def get_quito_state_values():
    # sheets = get_excel_sheets(['Sheet_local_HHL', 'Sheet_hhl_ibmq_quito', 'Sheet_hhl_ibmq_yorktown_Y'])
    sheets = get_excel_sheets(['Sheet_hhl_ibmq_quito'])
    df = sheets['Sheet_hhl_ibmq_quito']
    df = pd.DataFrame(data={"ket{1100}": df.iloc[12], "ket{1101}": df.iloc[13]})
    df['index'] = get_hhl_index()
    return df.set_index('index')

def get_yorktown_state_values():
    sheets = get_excel_sheets(['Sheet_hhl_ibmq_yorktown_Y'])
    df = sheets['Sheet_hhl_ibmq_yorktown_Y']
    df = pd.DataFrame(data={"ket{1100}": df.iloc[12], "ket{1101}": df.iloc[13]})
    df['index'] = get_hhl_index()
    return df.set_index('index')


def get_mine_state_values(dic):
    exp_arr = prepare_hhl_optimised_gate_experiment()
    df_my_simulator = simulate_all(exp_arr, dic)
    df_my_simulator = pd.DataFrame(data={"ket{1100}": df_my_simulator.iloc[12], "ket{1101}": df_my_simulator.iloc[13]})
    df_my_simulator['index'] = get_hhl_index()
    return df_my_simulator.set_index('index')


def plot_hhl_quito_states():
    df = get_quito_state_values()
    plot_hll_graphic_qiskit(df, "plot_hhl_quito_states")


# plot_hhl_quito_states()

def plot_hhl_quito_values():
    df = get_quito_state_values()
    df["ket{1100}"], df["ket{1101}"] = smother_results(df["ket{1100}"], df["ket{1101}"])
    plot_hll_graphic_qiskit(df, "plot_hhl_quito_values")


# plot_hhl_quito_values()

def get_quito_best_noise_results():
    return {
        'M': gate_factory(ry_gate, 0.1737),
         'CX': gate_factory(rx_gate,  0.4698968668407313/2),
        'NRy': f_factory(ry_q),
        'NRz': f_factory(rz_q),
        'NP': f_factory(p_q),
    }

def get_yorktown_best_noise_results():
    return {
        'M': gate_factory(ry_gate, 0.279535050537985),
        'CX': gate_factory(rx_gate, 0.772639097744361/2),
        # 'NRy': f_factory(ry_q),
        # 'NRz': f_factory(rz_y),
        # 'NP': f_factory(p_y),
    }

def get_quito_terrible_noise_results():
    return {
        'M': gate_factory(ry_gate, 0.1737),
        # 'H': gate_factory(rx_gate, 1.48866929133858),
        'CX': gate_factory(rx_gate, 0.561310344827586),
        'NRy': t_ry_noise,
        'NRz':t_rz_noise,
        'NP':t_p_noise,
    }

def get_no_noise_results():
    return {}


def plot_hhl_quito_and_mine_states_comparison():
    df_perfect = get_mine_state_values(get_no_noise_results())
    df_my_simulator = get_mine_state_values(get_quito_best_noise_results())
    df_quito = get_quito_state_values()
    df = pd.DataFrame(data={"Mine ket{1100}": df_my_simulator['ket{1100}'], "Quito ket{1100}": df_quito['ket{1100}']})
    plot_hll_graphic_qiskit(df, "plot_hhl_quito_and_mine_states_comparison  ket{1100}")
    percent_diff = (df['Mine ket{1100}'].apply(np.array) - df['Quito ket{1100}'].apply(np.array)).apply(np.linalg.norm).mean()
    print("ket{1100} percent_diff", percent_diff * 100)

    percent_diff = (df['Mine ket{1100}'].apply(np.array) - df_perfect['ket{1100}'].apply(np.array)).apply(np.linalg.norm).mean()
    print("ket{1100} percent_diff with perfect", percent_diff * 100)

    percent_diff = (df['Quito ket{1100}'].apply(np.array) - df_perfect['ket{1100}'].apply(np.array)).apply(np.linalg.norm).mean()
    print("ket{1100} Quito percent_diff with perfect", percent_diff * 100)


    df = pd.DataFrame(data={"Mine ket{1101}": df_my_simulator['ket{1101}'], "Quito ket{1101}": df_quito['ket{1101}']})
    plot_hll_graphic_qiskit(df, "plot_hhl_quito_and_mine_states_comparison  ket{1101}")
    percent_diff = (df['Mine ket{1101}'].apply(np.array) - df['Quito ket{1101}'].apply(np.array)).apply(np.linalg.norm).mean()
    print("ket{1101} percent_diff", percent_diff * 100)


#################################################################
#################################################################
#################################################################


def plot_hhl_yorktown_states():
    df = get_yorktown_state_values()
    plot_hll_graphic_qiskit(df, "plot_hhl_yorktown_states")


def plot_hhl_yorktown_values():
    df = get_yorktown_state_values()
    df["ket{1100}"], df["ket{1101}"] = smother_results(df["ket{1100}"], df["ket{1101}"])
    plot_hll_graphic_qiskit(df, "plot_hhl_yorktown_values")

def plot_hhl_yorktown_and_mine_states_comparison():
    df_my_simulator = get_mine_state_values(get_no_noise_results())
    # df_perfect = get_mine_state_values(get_yorktown_best_noise_results())
    df_quito = get_yorktown_state_values()

    df = pd.DataFrame(data={"Mine ket{1100}": df_my_simulator['ket{1100}'], "Yorktown ket{1100}": df_quito['ket{1100}']})
    plot_hll_graphic_qiskit(df, "plot_hhl_yorktown_and_mine_states_comparison  ket{1100}")
    percent_diff = (df['Mine ket{1100}'].apply(np.array) - df['Yorktown ket{1100}'].apply(np.array)).apply(np.linalg.norm).mean()
    print("ket{1100} percent_diff", percent_diff * 100)

    df = pd.DataFrame(data={"Mine ket{1101}": df_my_simulator['ket{1101}'], "Yorktown ket{1101}": df_quito['ket{1101}']})
    plot_hll_graphic_qiskit(df, "plot_hhl_yorktown_and_mine_states_comparison  ket{1101}")
    percent_diff = (df['Mine ket{1101}'].apply(np.array) - df['Yorktown ket{1101}'].apply(np.array)).apply(np.linalg.norm).mean()
    print("ket{1101} percent_diff", percent_diff * 100)


def execute_experiments():
    plot_hhl_quito_and_mine_states_comparison()
    # plot_hhl_yorktown_and_mine_states_comparison()

# execute_experiments()