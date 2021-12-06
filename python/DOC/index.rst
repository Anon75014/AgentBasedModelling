.. CropWar documentation master file, created by
   sphinx-quickstart on Fri Nov 26 17:48:20 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CropWar's documentation!
===================================

Here you can find instructions on how to simulate the interactions of spatially and economically competing farmers : :guilabel:`The CropWar`


.. image:: img/map.gif
   :width: 255pt

.. image:: img/10.jpg
   :width: 255pt

.. image:: img/04.jpg
   :width: 255pt

.. image:: img/02.jpg
   :width: 255pt

.. image:: img/01.jpg
   :width: 510pt

.. image:: img/03.jpg
   :width: 510pt

.. image:: img/09.jpg
   :width: 255pt

.. image:: img/07.jpg
   :width: 255pt

.. image:: img/08.jpg
   :width: 255pt

.. image:: img/06.jpg
   :width: 255pt



Simulation Pseudo Code
----------------------

.. code-block:: Python

   """ Initialise the available crops """
   crop_shop = CropSortiment()
   crop_shop.add_crop(1, 1, 1)  
   crop_shop.add_crop(1, 2, 1)  

   parameters = {
      # ...
      # Parameters, specifing the model properties
      # ...

   }

   """ Create and run the model """
   model = CropwarModel(parameters)  
   results = model.run()

   """ Display the results using the Displayer Class """
   presenter = graph_class(results)
   presenter.crops()
   presenter.cellcount()
   presenter.stocks()
   presenter.budget()
   presenter.export()
   presenter.traits(model)

   """ Display the Map with the farmers """
   mapper = map_class(model)
   mapper.initialise_farmers()
   mapper.place_farmers()
   mapper.show()

   print(f"SEED: {model.p.seed}")

.. Tip:: Read through the documentation accessible in the sidebar to understand what happens behind the scenes. :)

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   overview

   INFO_model
   INFO_market
   INFO_crops
   INFO_weather


.. toctree::
   :maxdepth: 2
   :caption: Reinforcement Learning

   INFO_SB3 
   INFO_RL_env
   INFO_RL_agents

.. toctree::
   :maxdepth: 2
   :caption: Visualisation

   VIS_graphs
   VIS_map
   
.. toctree::
   :maxdepth: 2
   :caption: Documentation

   code/modules
   api



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
