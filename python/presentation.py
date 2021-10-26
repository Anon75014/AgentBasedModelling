import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame as df

def display_evolution_bar(_data,_parameter):
    fig = plt.figure()
    sns.catplot(data = _data, kind="bar", x='t', y=_parameter, hue="obj_id")
    plt.xlabel("Time Steps")
    plt.ylabel(_parameter)


def display_evolution_line(_data,_parameter):
    sns.set_theme(style="whitegrid")

    fig = plt.figure()
    sns.lineplot(data = _data, x='t', y=_parameter, hue="obj_id")
    plt.xlabel("Time Steps")
    plt.ylabel(_parameter)

def display_solo_line(_data,_parameter):
    sns.relplot(
    data=_data, x="t", y=_parameter, col="obj_id",
    kind="line")

def display_stocks(_run_data):
    just_stock = df.from_records(_run_data.stock)
    raw_stock_data = pd.concat([_run_data[["t","obj_id"]], just_stock], axis=1)
    all_stock_data = raw_stock_data.melt(id_vars=['t','obj_id'],var_name='Crop', value_name='Amount')    
    print(just_stock)
    
    fig = plt.figure()
    sns.relplot(
    data=all_stock_data, x="t", y="Amount", col="obj_id", hue="Crop",
    kind="line")
    fig.show()
    # melt source: https://pandas.pydata.org/docs/reference/api/pandas.melt.html
