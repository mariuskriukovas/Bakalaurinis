import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_multivector, circuit_drawer
from qiskit.visualization import plot_histogram

import numpy as np
import pandas as pd
import re

from git.Bakalaurinis.tools.IO_service import read_filenames, read_results
from git.Bakalaurinis.tools.excel_tools import append_excel_sheets


def filename_sort_key(filename):
    return int(re.split('[_.]', filename)[-2])


def get_result(dir_name, key):
    res = []

    file_names = sorted(read_filenames(dir_name, key), key=filename_sort_key)
    print(file_names)
    for f in file_names:
        res.append({
            'name': f,
            'result': read_results(dir_name, f)
        })
    return res


# print(get_result("test","test"))

def convert_result_to_np_arr(result):
    counts = result.get_counts()
    keys = list(counts.keys())
    arr_len = 2 ** len(keys[0])
    arr = np.zeros(arr_len)
    for k in keys:
        idx = int(k, 2)
        arr[idx] = counts[k]
    return arr


def convert_results_to_df(result_arr):
    data = {}
    for i, r in enumerate(result_arr):
        data[i] = convert_result_to_np_arr(r)
    return pd.DataFrame(data=data)


def parse_results(r_arr):
    r_arr = list(map(lambda r: r['result'], r_arr))
    df = convert_results_to_df(r_arr) / 1024
    return df


def write_results_to_excel(name, file_name):
    local = parse_results(get_result(name, file_name))
    # print(local)
    df_arr = [local,]
    name_arr = [name,]
    append_excel_sheets(df_arr, name_arr)

def draw_circuit(q, title=""):
    (qr, cr, qc) = q
    circuit_drawer(qc, output='mpl')
    plt.title(title)
    plt.show()


# do with mocks

def draw_result_graphic(result, title=""):
    plot_histogram(result.get_counts(), title=title)
    plt.show()
    return result


def draw_sphere(result, title):
    plot_bloch_multivector(result)
    # plot_bloch_multivector(out_state, title=title)
    # plt.title(title)
    plt.show()
