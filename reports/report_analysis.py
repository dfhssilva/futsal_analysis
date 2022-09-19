import os
import sys
import getopt

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


if __name__ == "__main__":
    filename = parse_parameters(sys.argv)

    df = pd.read_excel(filename, skiprows=3, usecols=range(2,13))
    df = df.loc[:find_first_nan_row(df)-1]

    col_names = ["Perda de Bola", "Passe Errado", "Desarme", "Interceção de Passe", "Interceção de Remate", "Remate Efetuado", "Assistência", "Golos"]
    fig, axes = plt.subplots(2, 4, figsize=(19, 9))

    for ax, name in zip(axes.flat, col_names):
        data = df.sort_values(name, ascending=False)
        ax.bar(data["Nome completo"], data[name])
        ax.set_title(name)
        ax.tick_params(axis="x", rotation=45)

    plt.suptitle(f"Jogo {df['Data'].iloc[0]} - Atlético vs {df['Adversário'].iloc[0]}")
    plt.tight_layout()

    filename_no_extension, _ = os.path.splitext(filename)
    plt.savefig(filename_no_extension + ".png")