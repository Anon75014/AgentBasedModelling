"""
Presentation file for the results of the CropWar simulation.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas import DataFrame as df
from tabulate import tabulate

from model import CropwarModel


class graph_class:
    """
    Displayer Class to show the Agnetpy Run results.
    """

    def __init__(self, model: CropwarModel, _results) -> None:
        """
        :param model: CropWar model that should be graphed
        :type model: CropwarModel
        :param _results: A pandas dataframe, containing the results of `model.run()`
        """
        self.model = model
        self.results = _results
        self.data = _results.arrange_variables()
        self.data = self.data.rename(columns={"obj_id": "Farmer ID"})
        self.stock_data = self.preprocess_data()
        self.data.drop(columns=["stock"], inplace=True)

        self.titles = {
            "budget": "Budget Evolution",
            "crop_id": "Active Crops",
            "stock": "Stock Evolution",
            "cellcount": "Evolution of Cells per Farmer",
            "buy_cell_threash": "Buy Threashold",
            "prices": "Crop Prices",
            "demand": "Crop Demand",
            "supply": "Crop Supply",
            "global_stock": "Global Crop Stock",
        }
        self.y_labels = {
            "budget": "Budget",
            "crop_id": "Active Crop ID",
            "stock": "Stock Units",
            "cellcount": "Amount of Cells",
            "buy_cell_threash": r"Parameter $\in [0,1]}$",
            "prices": "Price",
            "demand": "Demand in Stock Units",
            "supply": "Supply in Stock Units",
            "global_stock": "Stock Units",
        }
        self._stock_data = None
        print("OK: initialised Displayer instance")

    def new_plot(self, _parameter):
        """
        Basic properties for a new plot.
        """
        fig = plt.figure()

        plt.title(self.titles[_parameter])
        plt.xlabel("Time Steps")
        plt.ylabel(self.y_labels[_parameter])

    def show_evolution_bar(self, _parameter):
        sns.catplot(data=self.data, kind="bar", x="t", y=_parameter, hue="Farmer ID")

    def show_evolution_line(self, _parameter):
        sns.set_theme(style="whitegrid")
        sns.lineplot(data=self.data, x="t", y=_parameter, hue="Farmer ID")

    def show_evolution_scatter(self, _parameter):
        sns.set_theme(style="whitegrid")
        sns.scatterplot(data=self.data, x="t", y=_parameter, hue="Farmer ID")

    def show_solo_line(self, _parameter):
        g = sns.relplot(
            data=self.data, x="t", y=_parameter, col="Farmer ID", kind="line"
        )

        return g

    """ SPECIFIC FUNCTIONS """

    def preprocess_data(self):
        """
        Convert the results-pd-series to a dataframe w/out dictionaries
        """

        _stock_as_df = df.from_records(self.data.stock)
        _stock_data_raw = pd.concat(
            [self.data[["t", "Farmer ID"]], _stock_as_df], axis=1
        )
        _stock_data = _stock_data_raw.melt(
            id_vars=["t", "Farmer ID"], var_name="Crop", value_name="Amount"
        )
        # source: https://pandas.pydata.org/docs/reference/api/pandas.melt.html

        return _stock_data

    def stocks(self):
        """
        Plot the stock evolution for all the farmers seperately.
        """
        g = sns.relplot(
            data=self.stock_data,
            x="t",
            y="Amount",
            col="Farmer ID",
            hue="Crop",
            kind="line",
        )
        g.set_axis_labels("Time", "Amount in Stock")
        g.fig.suptitle("Stock Evolution", fontsize=14)
        g.fig.subplots_adjust(top=0.86)

    def crops(self):
        """
        Plot crop_id evolution for the different farmers.
        """
        g = self.show_solo_line("crop_id")
        g.set(yticks=list(range(self.results.parameters.constants["amount_of_crops"])))
        g.set_axis_labels("Time", "Crop ID")
        g.fig.suptitle("Active Crop", fontsize=14)
        g.fig.subplots_adjust(top=0.86)

    def budget(self):
        """
        Plot budget data
        """
        self.new_plot("budget")
        self.show_evolution_line("budget")

    def cellcount(self):
        """
        Cellcount data
        """
        self.new_plot("cellcount")
        self.show_evolution_line("cellcount")

    def traits(self, model):
        """
        Personality traits
        """
        fig, ax = plt.subplots()
        trait_data = list(model.farmers.buy_cell_threash)
        farmer_ids = list(model.farmers.id)
        rects1 = ax.bar(farmer_ids, trait_data)
        ax.set_ylabel("Buy threashold")
        ax.set_xlabel("Farmer ID")
        ax.bar_label(rects1, padding=3, fmt="%.2f")
        ax.set_xticks(farmer_ids)
        ax.set_title("Buy Threashold for the farmers")

    def prices(self):
        """Presents the evolution of the Market-influenced crop prices.
        """
        print(f"prices have so many pars: {len(self.model.price_history)}")
        prices_df = pd.DataFrame(self.model.price_history)
        self.new_plot("prices")
        sns.lineplot(data = prices_df)
        prices_df.to_csv('exported_prices.csv')

    def demand(self):
        """
        Presents the evolution of the Market-influenced crop demand.
        """
        print(f"demand have so many pars: {len(self.model.demand_history)}")
        demand_df = pd.DataFrame(self.model.demand_history)
        self.new_plot("demand")
        sns.lineplot(data = demand_df)
        demand_df.to_csv('exported_demand.csv')

    def supply(self):
        """Presents the evolution of the Market-influenced crop supply.
        """
        print(f"supply have so many pars: {len(self.model.supply_history)}")
        supply_df = pd.DataFrame(self.model.supply_history)
        self.new_plot("supply")
        sns.lineplot(data = supply_df)
        supply_df.to_csv('exported_supply.csv')

    def global_stock(self):
        """
        Presents the evolution of the Market-influenced crop global stock.
        """
        print(f"global_stock have so many pars: {len(self.model.global_stock_history)}")
        global_stock_df = pd.DataFrame(self.model.global_stock_history)
        self.new_plot("global_stock")
        sns.lineplot(data = global_stock_df)
        global_stock_df.to_csv('exported_global_stock.csv')


    def personalities(self):
        """
        Show Personality database

        Pretty print a table into the Console with ID, Farmer Types and Buy threashold
        """

        ids = self.model.farmers.id
        types = self.model.farmers.type
        buy_vals = [round(val,3) for val in self.model.farmers.buy_cell_threash]

        data = {
            "IDs": ids,
            "Farmer type": types,
            "Buy Threashold\n(rounded)": buy_vals,
        }
        # source : https://pypi.org/project/tabulate/
        print(tabulate(data, headers="keys",tablefmt="fancy_grid",numalign='center',stralign='center'))

    def export_budget(self):
        """
        Export the relevant data for plotting in LaTeX
        """
        budget_df = df.pivot(self.data, index="t", columns="Farmer ID", values="budget")
        budget_df.to_csv("exported_budget.csv")

    def export_cellcount(self):
        """
        Export the relevant data for plotting in LaTeX
        """
        cellcount_df = df.pivot(
            self.data, index="t", columns="Farmer ID", values="cellcount"
        )
        cellcount_df.to_csv("exported_cellcount.csv")

    def export_stock(self):
        """
        Export the relevant data for plotting in LaTeX
        """
        stock_df = df.pivot(
            self.stock_data, index="t", columns=["Crop", "Farmer ID"], values="Amount"
        )
        stock_df.to_csv("exported_stock.csv")

    def export(self):
        """
        Export stock data and budget, `crop_id` data to two `.csv` files for
        plotting in LaTex.
        """
        # self.stock_data.to_csv("stock_results.csv")
        self.data.to_csv("data.csv")
        self.export_budget()
        self.export_cellcount()
        self.export_stock()
