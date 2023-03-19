import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import plotly.express as px

from utils import *


def calculate_trend(df, col):
    X = [i for i in range(0, df.index.shape[0])]
    X = np.reshape(X, (len(X), 1))
    y = df[col].values

    model = LinearRegression()
    model.fit(X, y)
    # Calculate trend
    trend = model.predict(X)
    return trend


if __name__ == "__main__":
    xlsx_files = list(filter(lambda x: x.endswith("xlsx"), os.listdir()))
    dfs = []
    for filename in xlsx_files:
        df = pd.read_excel(filename, usecols=range(2,14))
        date, opponent = get_date(df), get_opponent(df)
        df = extract_analysis_table(df)
        df["Data"], df["Oponente"] = date, opponent
        dfs.append(df)

    # Concatenate every dataframe
    df = pd.concat(dfs)
    
    # Groupby each game and sort by game
    df = df.groupby(["Data", "Oponente"]).sum().reset_index()
    df["Data"] = pd.to_datetime(df["Data"], format="%d-%m-%Y")
    df = df.sort_values("Data").reset_index(drop=True)

    # Create "Jogo" index column
    df["Jogo"] = df["Data"].astype(str) + " - " + df["Oponente"]
    df = df.set_index("Jogo").drop(columns=["Data", "Oponente"])

    fig = go.Figure()
    for col, color in zip(df.columns, px.colors.qualitative.Dark24):
        # Add data line
        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines+markers', name=col, line=dict(color=color)))
        # Add trend line
        trend = calculate_trend(df, col)
        fig.add_trace(go.Scatter(x=df.index, y=trend, showlegend=False, name=col+" - tendência", opacity=0.3, line=dict(dash='dash', color=color)))
    
    fig.update_layout(
        title="""Análise Evolutiva com linhas de tendência - duplo clique na legenda para isolares cada uma das estatísticas""",
        xaxis_title="Jogos",
        yaxis_title="Valor",
        legend_title="Estatísticas",
    )

    fig.write_html("Análise Evolutiva.html")
