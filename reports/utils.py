import re
import numpy as np
from math import ceil


COL_NAMES = ["Perda de Bola", "Passe Errado", "Desarme", "Interceção de Passe", "Interceção de Remate", "Remate", "Remate à Baliza", "Assistência", "Golos", "Defesas", "Linha de Passe"]
GR_NAMES = ["Vasco S.", "Mário B.", "Óscar S.", "Pedro R."]


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


def extract_analysis_table(df):
    df = skip_rows(df)
    df = df.replace("-", np.nan)
    df = df.loc[:find_first_nan_row(df)-1]
    return df


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


def find_first_nan_row(df):
    nan_ix = df.index[df.isna().all(axis=1)][0]
    return nan_ix


def skip_rows(df):
    df.columns = df.iloc[8]
    df = df.iloc[9:].reset_index(drop=True)
    return df
