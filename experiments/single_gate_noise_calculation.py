import numpy as np
import pandas as pd

from git.Bakalaurinis.simuliator.translator import simulate_one
from git.Bakalaurinis.tools.excel_tools import get_excel_sheets

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


def execute_experiment(name,
                       experiments,
                       noise_dictionary):
    sheets = get_excel_sheets([name])
    DATA = sheets[name]
    # experiments = prepare_experiment()
    shape = DATA[0].shape
    print(shape)
    atol_val = 0.01
    dic_val = {}
    while atol_val < 0.04:
        best_arr = []

        for i, d in enumerate(experiments):
            real_data = DATA[i].to_numpy()
            e = experiments[i]

            def current_experiment(i, atol_val):
                noise_dic = noise_dictionary(i)
                return np.isclose(real_data, simulate_one(e, noise_dic), atol=atol_val).sum() == shape

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


def execute_rotation_experiment(name,
                                experiments,
                                noise_dictionary):
    sheets = get_excel_sheets([name])
    DATA = sheets[name]
    # experiments = prepare_experiment()
    shape = DATA[0].shape
    print(shape)
    atol_val = 0.01
    dic_val = {}
    while atol_val < 0.04:
        best_arr = []

        for i, d in enumerate(experiments):
            real_data = DATA[i].to_numpy()
            e = experiments[i]

            best = None
            j = - (np.pi / 2)
            while j < (np.pi / 2):
                noise_dic = noise_dictionary(j)
                experiment_res = simulate_one(e, noise_dic)
                is_close = np.isclose(real_data, experiment_res, atol=atol_val).sum() == shape
                if is_close:
                    best = j
                    break
                j += 0.01
            best_arr.append(best)
            print("i = ", i, "atol = ", atol_val, " Best ---> ", best)
            dic_val[atol_val] = best_arr

        atol_val += 0.01

    return pd.DataFrame(data=dic_val)
