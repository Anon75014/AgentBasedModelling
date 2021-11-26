from datetime import datetime
from json import dump, load
from os import sep

import numpy as np
import tianshou as ts
import torch
from tianshou.data import Batch
from tianshou.utils import TensorboardLogger
from torch import nn
from torch.utils.tensorboard import SummaryWriter

from RL_env import CropwarEnv
from helper_functions import DotDict, make_file_path, make_local_dir

print("hello, we power up the DQN machine... one moment ...")

"""Parameter variables"""
config_folder = make_local_dir("configs")

# Change the following 2 lines to reuse the "pars" of a previous config run
# use_configs = False means, that all the parameters of this file are used
# --.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--
# use_configs = "python\configs\dqn17_train_config.json"
use_configs = False
# --'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--


if use_configs:
    print(f"Info: Using config of file {use_configs}")
    file = open(use_configs)
    pars = DotDict(load(file)).pars
    pars.used_config_of = use_configs

else:
    print(f"Info: Using NEW config.")
    pars = DotDict(
        # --.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--.--
        # Change the following lines to tune the DQN and its training
        {
            "optim": {"lr": 1e-3},
            "policy": {
                "discount_factor": 0.9,
                "estimation_step": 1,
                "target_update_freq": 320,
                "train_epsilon": 0.1,
                "test_epsilon": 0.05,
            },
            "trainer": {
                "max_epoch": 1,
                "step_per_epoch": 10000,
                "step_per_collect": 10,
                "update_per_step": 0.1,
                "episode_per_test": 100,
                "batch_size": 64,
            },
            # --'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--'--
            "run_name": None,
            "used_config_of": None,
            "execution_time": None,
        }
    )

"""Setup Log Folder, generate new log Name, initialise Logger"""
log_folder_path = make_local_dir("log")
log_file_path, run_name = make_file_path(log_folder_path, "dqn")
pars.run_name = run_name
writer = SummaryWriter(log_file_path)
logger = TensorboardLogger(writer)
print("\n")

"""Initialise Environments"""
env = CropwarEnv()
train_envs = ts.env.DummyVectorEnv([lambda: CropwarEnv() for _ in range(10)])
test_envs = ts.env.DummyVectorEnv([lambda: CropwarEnv() for _ in range(100)])
state_shape = env.observation_space.shape or env.observation_space.n
action_shape = env.action_space.shape or env.action_space.n


class Net(nn.Module):
    """Define the neural network
    - Internally Tunable: amount of hidden layers, amount of nodes per layer
    Note: the second number of one layer must match the first of the next.
          this has to do with the matrix multiplications (linear algebra)
    """

    def __init__(self, state_shape, action_shape):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(np.prod(state_shape), 20),
            nn.ReLU(inplace=True),
            nn.Linear(20, 20),
            nn.ReLU(inplace=True),
            nn.Linear(20, np.prod(action_shape)),
        )

    def forward(self, obs, state=None, info={}):
        # default as online in the tianshou documentation
        if not isinstance(obs, torch.Tensor):
            obs = torch.tensor(obs, dtype=torch.float)
        batch = obs.shape[0]
        logits = self.model(obs.view(batch, -1))
        return logits, state


"""Initialise Network, Optimizer and Policy"""
net = Net(state_shape, action_shape)
optim = torch.optim.Adam(net.parameters(), lr=pars.optim.lr)

policy = ts.policy.DQNPolicy(
    net,
    optim,
    discount_factor=pars.policy.discount_factor,
    estimation_step=pars.policy.estimation_step,
    target_update_freq=pars.policy.target_update_freq,
)


"""Initialise Collectors for training and testing"""
train_collector = ts.data.Collector(
    policy, train_envs, ts.data.VectorReplayBuffer(20000, 10), exploration_noise=True
)
test_collector = ts.data.Collector(policy, test_envs, exploration_noise=True)

"""Train the network!"""
pars.execution_time = str(datetime.now())

result = ts.trainer.offpolicy_trainer(
    policy,
    train_collector,
    test_collector,
    max_epoch=pars.trainer.max_epoch,
    step_per_epoch=pars.trainer.step_per_epoch,
    step_per_collect=pars.trainer.step_per_collect,
    update_per_step=pars.trainer.update_per_step,
    episode_per_test=pars.trainer.episode_per_test,
    batch_size=pars.trainer.batch_size,
    train_fn=lambda epoch, env_step: policy.set_eps(pars.policy.train_epsilon),
    test_fn=lambda epoch, env_step: policy.set_eps(pars.policy.test_epsilon),
    stop_fn=lambda mean_rewards: mean_rewards >= env.reward_threshold,
    logger=logger,
)
print(f'Finished training! Use {result["duration"]}')
print(f"\nThe results of the training are:\n{result}\n")


"""Write the used parameters into the config file in config folder"""
infos = {"pars": dict(pars), "network": str(net), "model_parameters": env.model._info_dict()}

config_file_path = config_folder + sep + run_name + "_train_config.json"
with open(config_file_path, "w") as f:
    dump(infos, f)
    print(f"Info: Dumped config into {config_file_path}")
#%%
