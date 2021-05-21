import numpy as np
import pandas as pd

from git.Bakalaurinis.simuliator.translator import simulate_one
from git.Bakalaurinis.tools.excel_tools import get_excel_sheets

BIG_DELTA = 0.001
def find_best_value(min_value, max_value, delta_i, epsilon, experiment):
    i = min_value
    lover_bound = None
    upper_bound = None
    while i < max_value:
        is_close = experiment(i, epsilon)
        if is_close:
            lover_bound = i
        if not is_close and (lover_bound is not None):
            upper_bound = i
        if lover_bound and upper_bound:
            if delta_i <= BIG_DELTA:
                return i
            else:
                return find_best_value(lover_bound, upper_bound, delta_i / 10, epsilon / 1.01, experiment)
        i += delta_i


def execute_experiment(name,
                       experiments,
                       noise_dictionary):
    sheets = get_excel_sheets([name])
    DATA = sheets[name]
    # experiments = prepare_experiment()
    shape = DATA[0].shape
    print(shape)
    epsilon = 0.03
    dic_val = {}
    while epsilon < 0.06:
        best_arr = []

        for i, d in enumerate(experiments):
            real_data = DATA[i].to_numpy()
            e = experiments[i]

            def current_experiment(i, epsilon):
                noise_dic = noise_dictionary(i)
                return np.isclose(real_data, simulate_one(e, noise_dic), atol=epsilon).sum() == shape

            best = find_best_value(
                min_value=0,
                max_value=2 * np.pi,
                delta_i=0.01,
                epsilon=epsilon,
                experiment=current_experiment)
            best_arr.append(best)
            print("i = ", i, "atol = ", epsilon, " Best ---> ", best)
            dic_val[epsilon] = best_arr

        epsilon += 0.01

    return pd.DataFrame(data=dic_val)


def execute_rotation_experiment(name,
                                experiments,
                                noise_dictionary):
    sheets = get_excel_sheets([name])
    DATA = sheets[name]
    # experiments = prepare_experiment()
    shape = DATA[0].shape
    print(shape)
    epsilon = 0.03
    dic_val = {}
    while epsilon < 0.06:
        best_arr = []

        for i, d in enumerate(experiments):
            real_data = DATA[i].to_numpy()
            e = experiments[i]
            if i < 40:
                b_value = (np.pi)
            else:
                b_value = (np.pi) / 2
            best = None
            j = -b_value
            while j < b_value:
                noise_dic = noise_dictionary(j)
                experiment_res = simulate_one(e, noise_dic)
                is_close = np.isclose(real_data, experiment_res, atol=epsilon).sum() == shape
                if is_close:
                    best = j
                    break
                j += 0.01
            best_arr.append(best)
            print("i = ", i, "atol = ", epsilon, " Best ---> ", best)
            dic_val[epsilon] = best_arr

        epsilon += 0.01

    return pd.DataFrame(data=dic_val)
