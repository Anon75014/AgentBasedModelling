Overview of CropWar
===================

Make a Simulation
-----------------

You can use the :func:`main.run_full_simulation()` function in the :mod:`main` file to simulate an entire episode of the CropWar.

.. 
    autofunction:: main.run_full_simulation
    :noindex:

A simulation begins with the initialisation of the :class:`crops.CropSortiment` to which some :class:`crops.Crop` are added.

.. 
    autoclass:: crops.CropSortiment 

Then the ``parameters`` for the CropWar model are specified and the :mod:`model` is initialised.
This is based on AgentPy. The agentpy model is then run via the agentpy model-function ``model.run()``. Which performs ``t_end`` amount of cycles {}:

``setup()`` -> {``update()`` <-> ``step()``} -> ``end()``


..
    autoclass:: model.CropwarModel

After that, a :mod:`graph_presenter` and :mod:`map_presenter` is initialised to present the result data from the run.
The :class:`graph_presenter.graph_class` is used to show graphs of interesting parameters recorded during the model :meth:`CropwarModel.update`.
The :class:`map_presenter.map_class` is used to generate a pretty map of the CropWar to visualise the spatial distribution.

.. Hint:: If the parameter ``save_gif`` is ``True`` in the ``parameters = {...}`` then a gif of the temporal map evolution will be saved to ``\images\map.gif``
