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
import warnings


def get_sheet_df(name):
    sheets = get_excel_sheets([name])
    return sheets[name]


QUITO_RX_SHEET_NAME = 'Sheet_f_rx_gate_quito_Aprox'
QUITO_RY_SHEET_NAME = 'Sheet_f_ry_gate_quito_Aprox5'
QUITO_RZ_SHEET_NAME = 'Sheet_f_rz_gate_quito_Aprox'
QUITO_P_SHEET_NAME = 'Sheet_f_p_gate_quito_Aprox'

QUITO_APROX_COFF = 0.05

YORKTOWN_RX_SHEET_NAME = 'Sheet_f_rx_gate_yorktown_Aprox'
YORKTOWN_RY_SHEET_NAME = 'Sheet_f_ry_gate_yorktown_Aprox2'
YORKTOWN_RZ_SHEET_NAME = 'Sheet_f_rz_gate_yorktown_Aprox1'
YORKTOWN_P_SHEET_NAME = 'Sheet_f_p_gate_yorktown_Aprox1'

YORKTOWN_APROX_COFF = 0.05


def get_full_rotation_interval(e = 0):
    x_axis = []
    # e = np.pi / 20
    # e = np.pi / 14
    theta = -1 * 2 * np.pi + e
    while theta < 2 * np.pi + e:
        print(theta)
        x_axis.append(theta)
        theta += np.pi / 20
    return x_axis


def get_poly_regression(x, y):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', np.RankWarning)
        return np.poly1d(np.polyfit(x, y, 30))


def f_quito_rx_noise():
    df_quito_rx = get_sheet_df(QUITO_RX_SHEET_NAME)
    x = get_full_rotation_interval()
    y = df_quito_rx[QUITO_APROX_COFF].to_numpy()
    p30 = get_poly_regression(x, y)
    return p30


def f_quito_ry_noise():
    df_quito_ry = get_sheet_df(QUITO_RY_SHEET_NAME)
    x = get_full_rotation_interval()
    y = df_quito_ry[QUITO_APROX_COFF].to_numpy()
    p30 = get_poly_regression(x, y)
    return p30


def f_quito_rz_noise():
    df_quito_rz = get_sheet_df(QUITO_RZ_SHEET_NAME)
    x = get_full_rotation_interval()
    y = df_quito_rz[QUITO_APROX_COFF].to_numpy()
    p30 = get_poly_regression(x, y)
    return p30


def f_quito_p_noise():
    df_quito_p = get_sheet_df(QUITO_P_SHEET_NAME)
    x = get_full_rotation_interval()
    y = df_quito_p[QUITO_APROX_COFF].to_numpy()
    p30 = get_poly_regression(x, y)
    return p30


# nepamenu gali reiketi perskaiciuoti jeigu labai blogai bus

def f_yorktown_rx_noise():
    df_rx = get_sheet_df(YORKTOWN_RX_SHEET_NAME)
    x = get_full_rotation_interval()
    y = df_rx[QUITO_APROX_COFF].to_numpy()
    p30 = get_poly_regression(x, y)
    return p30


def f_yorktown_ry_noise():
    df_ry = get_sheet_df(YORKTOWN_RY_SHEET_NAME)
    x = get_full_rotation_interval()
    y = df_ry[QUITO_APROX_COFF].to_numpy()
    p30 = get_poly_regression(x, y)
    return p30


def f_yorktown_rz_noise():
    df_rz = get_sheet_df(YORKTOWN_RZ_SHEET_NAME)
    x = get_full_rotation_interval()
    y = df_rz[QUITO_APROX_COFF].to_numpy()
    p30 = get_poly_regression(x, y)
    return p30


def f_yorktown_p_noise():
    df_p = get_sheet_df(YORKTOWN_P_SHEET_NAME)
    x = get_full_rotation_interval()
    y = df_p[QUITO_APROX_COFF].to_numpy()
    p30 = get_poly_regression(x, y)
    return p30


def prepare_df_index(df, f):
    r_arr = get_full_rotation_interval()
    df['index'] = r_arr
    df = df.set_index('index')
    df["f_noise"] = list(map(lambda x: f(x), r_arr))
    return df


def plot_quito_rx_noise():
    f = f_quito_rx_noise()
    df_quito_rx = get_sheet_df(QUITO_RX_SHEET_NAME)
    df_quito_rx = prepare_df_index(df_quito_rx, f)
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    df_quito_rx = df_quito_rx.rename(columns={"f_noise": "$f(\phi)$",
                                              0.03:"$\epsilon = 0.03$",
                                              0.04: "$\epsilon = 0.04$",
                                              0.05: "$\epsilon = 0.05$"
                                              })
    pic = df_quito_rx.plot(title="RX vartų triukšmo simuliacijos", kind='line', lw=1, fontsize=6,
                           color=my_colors,
                           use_index=True)

    plt.ylabel("$\phi$")
    plt.xlabel('Eksprimentai intervale $[-2\pi, 2\pi]$')
    plt.show()


def plot_quito_ry_noise():
    f = f_quito_ry_noise()
    df_quito_ry = get_sheet_df(QUITO_RY_SHEET_NAME)
    df_quito_ry = prepare_df_index(df_quito_ry, f)
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df_quito_ry.plot(title="plot_quito_ry_noise", kind='line', lw=1, fontsize=6,
                           color=my_colors,
                           use_index=True)


    plt.show()

plot_quito_rx_noise()
# plot_quito_ry_noise()

def plot_quito_rz_noise():
    f = f_quito_rz_noise()
    df_quito_rz = get_sheet_df(QUITO_RZ_SHEET_NAME)
    df_quito_rz = prepare_df_index(df_quito_rz, f)
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df_quito_rz.plot(title="Title", kind='line', lw=1, fontsize=6,
                           color=my_colors,
                           use_index=True)

    plt.show()

def plot_quito_p_noise():
    f = f_quito_p_noise()
    df_quito_rz = get_sheet_df(QUITO_P_SHEET_NAME)
    df_quito_rz = prepare_df_index(df_quito_rz, f)
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df_quito_rz.plot(title="Title", kind='line', lw=1, fontsize=6,
                           color=my_colors,
                           use_index=True)

    plt.show()


# plot_quito_p_noise()


def plot_yorktown_rx_noise():
    f = f_yorktown_rx_noise()
    df = get_sheet_df(YORKTOWN_RX_SHEET_NAME)
    df = prepare_df_index(df, f)
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df.plot(title="plot_yorktown_rx_noise", kind='line', lw=1, fontsize=6,
                  color=my_colors,
                  use_index=True)

    plt.show()

# plot_yorktown_rx_noise()

def plot_yorktown_ry_noise():
    f = f_yorktown_ry_noise()
    df = get_sheet_df(YORKTOWN_RY_SHEET_NAME)
    df = prepare_df_index(df, f)
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df.plot(title="plot_yorktown_ry_noise", kind='line', lw=1, fontsize=6,
                  color=my_colors,
                  use_index=True)

    plt.show()

# plot_yorktown_ry_noise()

def plot_yorktown_rz_noise():
    f = f_yorktown_rz_noise()
    df = get_sheet_df(YORKTOWN_RZ_SHEET_NAME)
    df = prepare_df_index(df, f)
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df.plot(title="plot_yorktown_rz_noise", kind='line', lw=1, fontsize=6,
                  color=my_colors,
                  use_index=True)

    plt.show()


def plot_yorktown_p_noise():
    f = f_yorktown_p_noise()
    df = get_sheet_df(YORKTOWN_P_SHEET_NAME)
    df = prepare_df_index(df, f)
    my_colors = ['blue', 'green', 'red', 'black', 'purple']
    pic = df.plot(title="plot_yorktown_p_noise", kind='line', lw=1, fontsize=6,
                  color=my_colors,
                  use_index=True)

    plt.show()
