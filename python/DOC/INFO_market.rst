Market Description
===================
​
​
The ``market.py`` file contains :meth:`market` class.
​
It's functions gets called by the ``CropwarModel`` and 
``Farmer`` in order to update the market each time step with the 
current amount in stock. 
​​

Market
-------

:meth:`market` implements a basic market model. Prices aggregate globally.
Another underlying assumption of this version is symmetric information for all market participants. 
This is important in price aggregation: if all agents know the other agents stocks, they can anticipate the market volume for each iteration
and hence infer the market prices. The transparency of stocks is incorporated via the function :meth:`market.Market._calc_global_stock`.
​
The global prices is determined as follows:

.. math::
    p_j = p_{j,0} \cdot \frac{D_j(p_{j-1})}{K + \sum_i s_i}
​

Here :math:`p_{j,0}` is the base price of commodity :math:`j`, :math:`D_j(p_j)` the demand and :math:`\sum_i s_j` the total stock available of crop :math:`j` across all farmers. 
The constant :math:`K` represents a residual stock of a commodity and is equal for all :math:`j`.
​

Supply and demand
------------------
In order to constitute a market, demand and supply need to be defined. Throughout the basic model we will use classical supply and demand functions.
​
The linear supply :math:`S_i(p_j)` of an agent :math:`i` for a commodity :math:`j` reads:
​

.. math::

    S_i(p_j) = A \left[ 1 + c_i \cdot p_j \right]

​
where :math:`A` is a surplus supply (willingness to supply for :math:`p_j=0`), :math:`p_j` the global commodity price and :math:`c_i` the slope of supply (which is connected to the inverse price elasticity of supply).
The supply function is implemented within :class:`market.Market.market_interaction`.
​
The demand for a commodity :math:`j` is globally defined as:
​

.. math::

    D_j(p_j) = \left( D_0 + at^2 \right) e^{-\alpha (p_j-p_{j,0})}
​

Where :math:`D_0` is a base demand, :math:`at^2` is a term representing population (and demand) growth as a function of time :math:`t`, :math:`p_j` is the price of crop :math:`j` at time :math:`t`, :math:`p_{j,0}` is the base price of crop :math:`j`, 
and :math:`\alpha` is a demand slope, representing the fact that less and less people will be able to afford expensive crops.
​

..  automodule:: market
    :members:
    :private-members: