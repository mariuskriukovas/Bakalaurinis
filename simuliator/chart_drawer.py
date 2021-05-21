import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from qiskit.visualization import plot_histogram


def draw_circuit_scheme(df, title=""):
    print(df)
    df_val = df.copy()

    for key in df.columns:
        df_val[key] = df[key].map(lambda x: ord(str(x)[0]))
    print(df_val)

    fig, ax = plt.subplots()
    sns.heatmap(df_val,ax=ax, annot=df, fmt='', cmap="YlGnBu")
    ax.set_title(title)

    ax.set_ylabel("Kubitai")
    ax.set_xlabel("Laikas  $t_{i}$")

    plt.show()


def draw_bar_chart(df, y_label="", title=""):
    df = df.T
    df = df.loc[:, (df != 0).any(axis=0)]  # remove zeros
    objects = df.columns
    y_pos = np.arange(len(objects))
    df.plot.bar(rot=0, color=['red'])
    # plt.xticks(y_pos, objects)
    # plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def draw_simple_plot(df, title = None):
    my_colors = ['blue', 'green', 'red', 'black', ]
    pic = df.plot(title=f'{title}', kind='line', lw=1, fontsize=6,
                  color=my_colors,
                  use_index=True)

    plt.show()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_red(string):
    string = str(string)
    print(bcolors.FAIL + string + bcolors.ENDC)

def print_green(string):
    string = str(string)
    print(bcolors.OKGREEN + string + bcolors.ENDC)


def plot_experiment_state(df, title=""):
    state_dict = {}
    e = 0.001
    longest = len("{0:b}".format(df.index[-1]))
    print(longest)
    repeats = "abc" * 3
    for col in df.index:
        if df[col] > e:
            bin = "{0:b}".format(col)
            add_zeros = "0" * (longest - len(bin))
            state_dict[f'|{add_zeros + bin}⟩'] = df[col]

    plot_histogram(state_dict, color="#4169e1", title=title)
    plt.show()