""" Presentation File for the Results of the  CropWar Simulation. """

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas import DataFrame as df


class graph_class():
    """ Displayer Class to show the Agnetpy Run results. """

    def __init__(self, _results) -> None:
        """ 
        Parameters:
        -   _results: A pandas dataframe, containing the results of Model.run()
        """
        self.results = _results
        self.data = _results.arrange_variables()
        self.data = self.data.rename(columns={"obj_id": "Farmer ID"})
        self.stock_data = self.preprocess_data()
        self.data.drop(columns=['stock'], inplace=True)

        self.titles = {
            "budget": "Budget Evolution",
            "crop_id": "Active Crops",
            "stock": "Stock Evolution"
        }
        self.y_labels = {
            "budget": "Budget",
            "crop_id": "Active Crop ID",
            "stock": "Stock Units"
        }
        self._stock_data = None
        print("OK: initialised Displayer instance")

    def new_plot(self, _parameter):
        """ Basic properties for a new plot. """
        fig = plt.figure()

        plt.title(self.titles[_parameter])
        plt.xlabel("Time Steps")
        plt.ylabel(self.y_labels[_parameter])

    def show_evolution_bar(self, _parameter):
        sns.catplot(data=self.data, kind="bar", x='t',
                    y=_parameter, hue="Farmer ID")

    def show_evolution_line(self, _parameter):
        sns.set_theme(style="whitegrid")
        sns.lineplot(data=self.data, x='t', y=_parameter, hue="Farmer ID")

    def show_evolution_scatter(self, _parameter):
        sns.set_theme(style="whitegrid")
        sns.scatterplot(data=self.data, x='t', y=_parameter, hue="Farmer ID")

    def show_solo_line(self, _parameter):
        g = sns.relplot(
            data=self.data, x="t", y=_parameter, col="Farmer ID",
            kind="line")

        return g

    ''' SPECIFIC FUNCTIONS '''

    def preprocess_data(self):
        """ Convert the results-pandas-series to a dataframe without dictionaries """

        _stock_as_df = df.from_records(self.data.stock)
        _stock_data_raw = pd.concat(
            [self.data[["t", "Farmer ID"]], _stock_as_df], axis=1)
        _stock_data = _stock_data_raw.melt(
            id_vars=['t', 'Farmer ID'], var_name='Crop', value_name='Amount')
        # melt source: https://pandas.pydata.org/docs/reference/api/pandas.melt.html

        return _stock_data

    def stocks(self):
        ''' Plot the stock evolution for all the farmers seperately. '''
        g = sns.relplot(
            data=self.stock_data, x="t", y="Amount", col="Farmer ID", hue="Crop",
            kind="line")
        g.set_axis_labels("Time", "Amount in Stock")
        g.fig.suptitle('Stock Evolution', fontsize=14)
        g.fig.subplots_adjust(top=0.86)

    def crops(self):
        """ Plot crop_id evolution for the different farmers. """
        g = self.show_solo_line("crop_id")
        g.set(yticks=list(
            range(self.results.parameters.constants["amount_of_crops"])))
        g.set_axis_labels("Time", "Crop ID")
        g.fig.suptitle('Active Crop', fontsize=14)
        g.fig.subplots_adjust(top=0.86)

    def budget(self):
        """ Plot budget data """
        self.new_plot("budget")
        self.show_evolution_line("budget")

    def export(self):
        """ Export Stockdata and Budget&Crop_id data to two .csv files for plotting in Latex. """
        self.stock_data.to_csv("stock_results.csv")
        self.data.to_csv("data.csv")
