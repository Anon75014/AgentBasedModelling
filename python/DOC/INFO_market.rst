Market Description
===================


The ``market.py`` file contains ``market`` class.

It's functions get called by the ``CropwarModel`` and 
``Farmer`` in order to update the market each time step with the 
current amount in stock -> supply. 


Market
-------
```market.py``` implements a basic market model. Prices aggregate globally and demand remains a quantity independent of the market decisions.


This is a test. Here is an equation:
:math:`X_{0:5} = (X_0, X_1, X_2, X_3, X_4)`.
Here is another:

.. math::
    :label: This is a label

    \nabla^2 f =
    \frac{1}{r^2} \frac{\partial}{\partial r}
    \left( r^2 \frac{\partial f}{\partial r} \right) +
    \frac{1}{r^2 \sin \theta} \frac{\partial f}{\partial \theta}
    \left( \sin \theta \, \frac{\partial f}{\partial \theta} \right) +
    \frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2}




.. automodule:: market
    :members:
    :private-members:
