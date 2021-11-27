Overview of CropWar
===================

Make a Simulation
-----------------

You can use the :py:func:``main.run_full_simulation()`` function in ``main.py`` to simulate an entire episode of the CropWar.

.. autofunction:: main.run_full_simulation
    :noindex:

Firstly the CropSortiment ``CropSortiment`` is initialised and crops are added.

.. autoclass:: crops.CropSortiment 

Then the parameters for the CropWar model are specified and the ``CropwarModel`` model is initialised.
This is based on AgentPy. The agentpy model is then run via the agentpy model-function ``model.run()``. Which performs ``t_end`` amount of cycles {}:

``setup()`` -> {``update()`` <-> ``step()``} -> ``end()``


.. autoclass:: model.CropwarModel

After that, a ``graph_class`` and ``map_class`` is initialised to present the result data from the run.
The graph class is used to show graphs of interesting parameters recorded during the model ``update()``.
The map_class is used to generate a pretty map of the CropWar to visualise the spatial distribution.

.. Hint:: If the parameter ``save_gif`` is ``True`` in the ``parameters = {...}`` then a gif of the temporal map evolution will be saved to ``\images\map.gif``
