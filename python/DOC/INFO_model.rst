Model Structure
===============


The ``model`` contains a grid of ``cells`` and a specified amount of ``farmers`` which own some cells.
Below is a pseudo code version of the model class. The highlighted lines show the central update function, which steps all agents from `t -> t+1`. 
This is done by calling their ``self.farmers.pre_market_step()`` then the ``self.market.step()`` and next the ``self.farmers.post_market_step()``. 
After that, the river is refreshed: ``self.river.refresh_water_content()``.

Further information to the functions can be found in the API.

.. code-block:: Python
    :emphasize-lines: 67,68,69,71
    
    class CropwarModel(ap.Model):
        """AgentPy model used for simulation.
        An agent based model (ABM) to simulate competing farmers.
        """

        def setup(self):
            """Setting up of the ABM model."""

            """Setting random seed (for reproducibility)"""
            # ...

            """Setting parameters and model properties"""
            self.crop_shop = self.p.crop_shop
            self.water_row = sum(self.p.water_levels)  # <- index of center row
            self.river = River(water_content=self.p.river_content)
            # ...

            """ Create grid: """
            self.grid = ap.Grid(self, (n, m), track_empty=True)
            # ...

            """ Grid Iteration Functions """
            # ... lambda functions used for expansion

            """ Initialising Cells"""
            n_cells = m * n  # amount of cells (that can even be water)
            self.cells = ap.AgentDList(self, n_cells, Cell)
            # ...
            self.grid.add_agents(  #... CELLS  )

            # Set River Cells
            # ...

            """ Initialising Farmers"""
            # ...

            """ MARKET """
            self.market = Market( # ... market parameters  )
            # ... variables for the market

            """ MACHINE LEARNING """
            # ... set the Trainee, link him to the environment, ...

            """ Initialise Map (for GIF) Instances """
            if self.p.save_gif:
                # ...


        def generate_water_matrix(self) -> np.array:
            """
            Generates the hydration matrix.
            Generate the distribution of hydration cells throughout the map.
            """
            # ...
            return water_matrix

        def step(self):
            """Move model from t to t+1.

            Evolve the entire model by one time step:
            - Step all the farmers
            - Step the market
            - let farmers decide if they want to change crops/expand
            - refresh the river water content
            """

            self.farmers.pre_market_step()
            self.market.step()
            self.farmers.post_market_step()

            self.river.refresh_water_content()

        def update(self):
            """Update farmers and record farmer properties."""

            """Create sorted Budget array for """
            budgets = np.array(self.model.farmers.budget.copy())
            budgets.sort()
            self.sorted_budgets = budgets
            """Record the properties of the farmers each step."""
            self.farmers.update()
            self.farmers.record("budget")
            self.farmers.record( ... )
            
            if self.p.save_gif:
                # ... generate map at current time step

        def end(self):
            """Performs final action at the end."""
            self.cells.set_farmer_id()

            if self.p.save_gif:
                # ... safe map as gif

.. Warning:: The above is *pseudo code* and will not run like this.

Model
-----

.. automodule:: model
    :members:


Farmers 
-------

..  automodule:: agents
    :members:

Cells 
-----

..  autoclass:: agents_base.Cell
    :members:


