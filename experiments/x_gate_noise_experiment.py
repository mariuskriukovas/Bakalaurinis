import numpy as np
import pandas as pd

from git.Bakalaurinis.experiments.x_gate_experiment import prepare_x_gate_experiment
from git.Bakalaurinis.simuliator.gates import np_gate, na_gate, gate_factory
from git.Bakalaurinis.simuliator.gates import X, I, rx_gate, rz_gate, ry_gate
from git.Bakalaurinis.simuliator.translator import simulate_one
from git.Bakalaurinis.tools.excel_tools import write_to_excel, append_excel_sheets, get_excel_sheets
from git.Bakalaurinis.simuliator.chart_drawer import draw_simple_plot

BIG_EPSILON = 0.001


def find_best_value(min_value, max_value, epsilon, atol_val, experiment):
    i = min_value
    lover_bound = None
    upper_bound = None
    result = None
    while i < max_value:
        is_close = experiment(i, atol_val)
        # print("I = ", i)
        # print("close: DATA == EXPERIMENT", is_close)
        if is_close:
            lover_bound = i

        if not is_close and (lover_bound is not None):
            upper_bound = i

        if lover_bound and upper_bound:
            if epsilon <= BIG_EPSILON:
                # print("epsilon", epsilon)
                # print("lover_bound", lover_bound, "upper_bound", upper_bound, "i", i)
                return i
            else:
                # print("lover_bound", lover_bound, "upper_bound", upper_bound, "i", i)
                return find_best_value(lover_bound, upper_bound, epsilon / 10, atol_val / 1.01, experiment)
        i += epsilon


def experiment(real_value, test_gate, shape, i, atol_val):
    noise_dic = {
        'I': gate_factory(ry_gate, 0.1913),
        'X': gate_factory(rx_gate, i),
    }
    experiment_res = simulate_one(test_gate, noise_dic)
    # print("DATA", real_value.shape)
    # print("EXPERIMENT", experiment_res.shape)
    # print(np.isclose(real_value, experiment_res, atol=atol_val).sum() )
    is_close = np.isclose(real_value, experiment_res, atol=atol_val).sum() == shape
    return is_close


def execute_experiment(name):
    sheets = get_excel_sheets([name])
    DATA = sheets[name]
    experiments = prepare_x_gate_experiment()
    shape = DATA[0].shape

    atol_val = 0.01
    dic_val = {}
    while atol_val < 0.06:
        best_arr = []

        for i, d in enumerate(experiments):
            real_data = DATA[i].to_numpy()
            e = experiments[i]

            def current_experiment(i, atol_val):
                return experiment(real_data, e, shape, i, atol_val)

            best = find_best_value(
                min_value=0,
                max_value=2 * np.pi,
                epsilon=0.01,
                atol_val=atol_val,
                experiment=current_experiment)
            best_arr.append(best)
            print("i = ", i, "atol = ", atol_val, " Best ---> ", best)
            dic_val[atol_val] = best_arr

        atol_val += 0.01

    return pd.DataFrame(data=dic_val)


# df = execute_experiment(name='Sheet_quito_X')
# df = execute_experiment(name='Sheet_yorktown_X')
# append_excel_sheets(df_arr=[df],
#                     df_names=["Yorktown_X_Noise_aprox_test"])
# print(df.notnull().count(axis=1))
# print("Vidurkis : ", df.dropna().mean())
# draw_simple_plot(df.dropna())