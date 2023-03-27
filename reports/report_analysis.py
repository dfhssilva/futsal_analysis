import os
import sys
import getopt

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import *


sns.set_theme()

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


if __name__ == "__main__":
    filename = parse_parameters(sys.argv)

    df = pd.read_excel(filename, usecols=range(2,14))
    date, opponent = get_date(df), get_opponent(df)
    df = extract_analysis_table(df)

    # Remove col_name if the corresponding column is empty
    for name in COL_NAMES:
        if df[name].isna().all():
            COL_NAMES.remove(name)
    fig, axes = plt.subplots(*define_axes_grid(COL_NAMES), figsize=(21, 9))

    for ax, name in zip(axes.flat, COL_NAMES):
        data = df.sort_values(name, ascending=False).reset_index()
        bar_plot = ax.bar(data["Nome completo"], data[name])
        # Set GR bars with a different color
        gr_indices = data.index[data["Nome completo"].isin(GR_NAMES)].tolist()
        for i in gr_indices:
            bar_plot[i].set_color("orange")
        ax.set_title(name)
        ax.tick_params(axis="x", rotation=45)

    remove_unused_axes(COL_NAMES, axes)
    plt.suptitle(f"Jogo {date} - Atlético vs {opponent}")
    plt.tight_layout()

    filename_no_extension, _ = os.path.splitext(filename)
    plt.savefig(filename_no_extension + ".png")
