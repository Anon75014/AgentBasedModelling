Market Description
===================


The ``market.py`` file contains ``market`` class.

It's functions get called by the ``CropwarModel`` and 
``Farmer`` in order to update the market each time step with the 
current amount in stock -> supply. 


Market
-------
```market.py``` implements a basic market model. Prices aggregate globally and demand remains a quantity independent of the market decisions.
Another underlying assumption of this version is symmetric information for all market participants. 
This is important in price aggregation: if all agents know the other agents stocks, they can anticipate the market volume for each iteration
and hence infer the market prices. The transparency of stocks is incorporated via the function :class:`market.Market._calc_global_stock`.

The p


Supply and demand
-------
In order to constitute a market, demand and supply need to be defined. Throughout the basic model we will use classical linear supply and demand functions.

The linear supply :math:`S_i(p_j)` of an agent :math:`i` for a commodity :math:`j` reads:

.. math::
  
    S_i(p_j) = A + c_i p_j


where :math:`A` is a surplus supply (willingness to supply for :math:`p_j=0`), :math:`p_j` the global commodity price and :math:`c_i` the slope of supply (which is connected to the inverse price elasticity of supply).
The supply function is implemented via :class:`market.Market._calc_global_supply`.

The linear demand for a commodity :math:`j` is globally defined as:

.. math::
    D_j(p_j) = d_j \cdot (B(p_j) + x_{random})

where :math:`B(p_j)` is a baseline demand, :math:`d_j` a demand shift and :math:`x_{random}\in [0,1]` a random variable. 

Since the market, i.e. the stock and supply of the agents, expands, the baseline demand :math:`B(p_j) = B + a \cdot S(p_j)` needs to increase proportionally to account for the expanding market. 
In each iteration the initial baseline :math:`B` is increased by a fraction :math:`a` of the global supply :math:`S_i(p_j)`.





.. automodule:: market
    :members:
    :private-members:
