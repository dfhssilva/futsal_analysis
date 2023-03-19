import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import *

CURRENT_PLAYERS = [
    "Miguel L.", 
    "Tomás G.", 
    "João V.", 
    "Duarte G.", 
    "Vasco M.", 
    "André M.", 
    "Rodrigo P.", 
    "Marco F.", 
    "Rodrigo G.", 
    "Igor P.", 
    "Valter S.", 
    "David C.", 
    "Vasco S.", 
    "Óscar S.", 
    "Mário B."
]

sns.set_theme()

if __name__ == "__main__":
    xlsx_files = list(filter(lambda x: x.endswith("xlsx"), os.listdir()))
    dfs = []
    for filename in xlsx_files:
        df = pd.read_excel(filename, usecols=range(2,14))
        df = extract_analysis_table(df)
        dfs.append(df)

    # Concatenate every dataframe
    df = pd.concat(dfs)
    
    # Groupby each current player name
    df = df.loc[df["Nome completo"].isin(CURRENT_PLAYERS)]
    df = df.groupby("Nome completo").sum().replace(0, np.nan)

    fig, axes = plt.subplots(*define_axes_grid(COL_NAMES), figsize=(21, 9))

    for ax, name in zip(axes.flat, COL_NAMES):
        data = df.sort_values(name, ascending=False).reset_index()
        bar_plot = ax.bar(data["Nome completo"], data[name])
        # Set GR bars with a different color
        gr_indices = data.index[data["Nome completo"].isin(GR_NAMES)].tolist()
        for i in gr_indices:
            bar_plot[i].set_color("orange")
        ax.set_title(name)
        ax.tick_params(axis="x", rotation=90)

    remove_unused_axes(COL_NAMES, axes)
    plt.suptitle(f"Estatísticas agregadas {len(dfs)} jornadas campeonato")
    plt.tight_layout()

    plt.savefig("Estatísticas agregadas campeonato.png")
