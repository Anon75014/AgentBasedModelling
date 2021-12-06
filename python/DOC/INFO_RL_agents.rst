
RL Agents
--------------

Similarly to the deterministic agents, we defined a reinforcement learning agent. It is also a subclass of the 
``Base_Farmer`` and thus inherits all the necssary functions to interact with the model.

The big difference is, that if he is in ``ACTIVE_TRAINING = True``, the ``self.planned_action`` will be set by the neural network ahead of the ``pre_market_step`` of the model.
Thus he can be operated from the ``model.py`` in exactly the same manner as the deterministic agents.

If ``ACTIVE_TRAINING = False`` and a ``use_trained_model`` loaded, 
it will evaluate the current observation of the environment with a trained model and set the ``self.planned_action`` similary as in active training, but with a pretrained model.


.. automodule:: RL_agents
    :members: