Crops Description
==================


The ``crops.py`` file contains ``CropSortiment`` and ``Crop`` class.

It's functions get called by the ``CropwarModel`` in order to 
initialise a sortiment of crops. The ``Farmer`` can buy those and 
plant them on his cells. 

The source for the detailed information about the crops is in ``crop_model.py``.

``in the present study FAO-based model has been adopted to make the crop harvest yield realistic. 
`for this purpose, several factors for four different crops (winter wheat, barley, maize, and beans) are implemented
to create realistic crop yield under water stress. To do this, drought scenario factors have been used to model the agent reactions
under severe conditions. The used factors are maximum harvest yield is an important factor that is used to calculate the actual crop harvest yield.
The maximum harvest yield is based on empirical data under different climate conditions. Water consumption illustrates how each stage of crop development will decrease under the water stress situation.
Crops IDs are:  1 for winter wheat, 2 for barley, 3 for maize, 4 for beans
 

Crop Model
-----------

.. autoclass:: crops.Crop
    :members:
    :private-members:

