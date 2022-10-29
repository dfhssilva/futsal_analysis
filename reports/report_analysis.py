import os
import sys
import getopt
import re
from math import ceil

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def parse_parameters(argv):
    arg_file = ""
    arg_help = "{0} -f <file>".format(argv[0])
    
    try:
        opts, _ = getopt.getopt(argv[1:], "hf:", ["help", "file="])
    except:
        print(arg_help)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-f", "--file"):
            arg_file = arg

    return arg_file

def find_first_nan_row(df):
    nan_ix = df.index[df.isna().all(axis=1)][0]
    return nan_ix


def define_axes_grid(col_names):
    num_rows = 1
    while True:
        num_cols = ceil(len(col_names)/num_rows)
        if num_cols > 4:
            num_rows += 1
        else:
            break

    return num_rows, num_cols


def remove_unused_axes(col_names, axes):
    grid_size = define_axes_grid(col_names)
    remainder = grid_size[0] * grid_size[1] - len(col_names)
    for ax in axes.flat[-remainder:]:
        ax.remove()


def skip_rows(df):
    df.columns = df.iloc[8]
    df = df.iloc[9:].reset_index(drop=True)
    return df


def get_date(df):
    date = df.iloc[6, 3]
    pattern = re.compile("Data: (.*)$")
    date = pattern.search(date).group(1)
    return date


def get_opponent(df):
    opponent = df.iloc[2, 3]
    pattern = re.compile("VS (.*)$")
    opponent = pattern.search(opponent).group(1)
    return opponent


if __name__ == "__main__":
    filename = parse_parameters(sys.argv)

    df = pd.read_excel(filename, usecols=range(2,14))
    date, opponent = get_date(df), get_opponent(df)
    df = skip_rows(df)
    df = df.replace("-", np.nan)
    df = df.loc[:find_first_nan_row(df)-1]
    col_names = ["Perda de Bola", "Passe Errado", "Desarme", "Interceção de Passe", "Interceção de Remate", "Remate", "Remate à Baliza", "Assistência", "Golos", "Defesas", "Linha de Passe"]
    gr_names = ["Vasco S.", "Pedro R.", "Óscar S."]

    # Remove col_name if the corresponding column is empty
    for name in col_names:
        if df[name].isna().all():
            col_names.remove(name)
    fig, axes = plt.subplots(*define_axes_grid(col_names), figsize=(21, 9))

    for ax, name in zip(axes.flat, col_names):
        data = df.sort_values(name, ascending=False).reset_index()
        bar_plot = ax.bar(data["Nome completo"], data[name])
        # Set GR bars with a different color
        gr_indices = data.index[data["Nome completo"].isin(gr_names)].tolist()
        for i in gr_indices:
            bar_plot[i].set_color("orange")
        ax.set_title(name)
        ax.tick_params(axis="x", rotation=45)

    remove_unused_axes(col_names, axes)
    plt.suptitle(f"Jogo {date} - Atlético vs {opponent}")
    plt.tight_layout()

    filename_no_extension, _ = os.path.splitext(filename)
    plt.savefig(filename_no_extension + ".png")
