import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame as df


class Displayer():
    """ Displayer Class to show the Agnetpy Run results. """

    def __init__(self, _results) -> None:
        """ 
        Parameters:
        -   _results: A pandas dataframe, containing the results of Model.run()
        """
        self.results = _results
        self.data = _results.arrange_variables()
        self.data = self.data.rename(columns={"obj_id": "Farmer ID"})
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

    def stocks(self):
        just_stock = df.from_records(self.data.stock)
        raw_stock_data = pd.concat(
            [self.data[["t", "Farmer ID"]], just_stock], axis=1)
        all_stock_data = raw_stock_data.melt(
            id_vars=['t', 'Farmer ID'], var_name='Crop', value_name='Amount')
        # melt source: https://pandas.pydata.org/docs/reference/api/pandas.melt.html
        # print(just_stock)

        g = sns.relplot(
            data=all_stock_data, x="t", y="Amount", col="Farmer ID", hue="Crop",
            kind="line")
        g.set_axis_labels("Time", "Amount in Stock")
        g.fig.suptitle('Stock Evolution', fontsize=14)
        g.fig.subplots_adjust(top=0.86)

    def crops(self):
        g = self.show_solo_line("crop_id")
        g.set(yticks=list(
            range(self.results.parameters.constants["amount_of_crops"])))
        g.set_axis_labels("Time", "Crop ID")
        g.fig.suptitle('Active Crop', fontsize=14)
        g.fig.subplots_adjust(top=0.86)

    def budget(self):
        self.new_plot("budget")
        self.show_evolution_line("budget")


"""
#Working with pandas:

import pandas as pd
from pandas import DataFrame as df

- create new dataframe: t7 = df(data=[10,20],columns=["bla"])
- join two together: df.join(t2,t3)
- Fill NA/NaN values: df.fillna(0)
- reset indices: t5.reset_index(drop=True,inplace=True)
"""
