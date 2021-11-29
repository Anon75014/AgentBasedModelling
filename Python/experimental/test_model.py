# %%


import agentpy as ap
import seaborn as sns

""" THIS Document is used for understanding and experimenting with AGENTpy outside of cropwar. """


class Payer(ap.Agent):

    def setup(self):
        """ Initiate agent attributes."""
        self.grid = self.model.grid
        self.random = self.model.random

        # Set start budget
        self.budget = self.random.randint(50, 100)
        self.book = {}

    def pay(self):
        amount = self.random.randint(10, 20)
        self.budget -= amount
        self.book["b1"] = self.budget
        self.book["b2"] = self.budget/2


class MoneyWorld(ap.Model):
    """ An Agent-Based-Model to simulate the crop war of farmers."""
    # See documentation https://agentpy.readthedocs.io/en/latest/reference_grid.html#agentpy.Grid

    def setup(self):
        """ Setting parameters and model properties """
        # Create grid:
        self.grid = ap.Grid(self, (7, 6), track_empty=True)
        self.agents = ap.AgentList(self, 4, Payer)

        self.grid.add_agents(self.agents, positions=[
                             (5, 4), (5, 1), (1, 1), (1, 4)], random=False, empty=True)  # version 0
        print('Done: setup of grid.')

    def update(self):
        if self.t > self.p.t_end:       # model should stop after "t_end" steps
            self.stop()
        self.agents.pay()

    def step(self):
        # record these properties of the agents each step
        self.agents.record("budget")
        self.agents.record("book")

    def end(self):
        pass


parameters = {
    "t_end": 5
}

''' Create and run the model '''
model = MoneyWorld(parameters)  # create model instance
results = model.run()

print(f"The results are {results}.")
run_data = results.arrange_variables()
print(f"The rundata is \n{run_data}.")


sns.lineplot(data=run_data, x='t', y="budget", hue="obj_id")
# %%
