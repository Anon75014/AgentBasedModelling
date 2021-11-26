#%%
import os.path as path
from os import mkdir, listdir

import numpy as np
import tianshou as ts
from tianshou.data.batch import Batch
import torch
from tianshou.utils import TensorboardLogger
from torch import nn
from torch.utils.tensorboard import SummaryWriter

from tst_DQN_env import TestEnv
import gym

print("hello, we power up the Test DQN machine... one moment ...")

"""Setup Log Folder and generate new log Name"""
try:
    dirname = path.dirname(path.abspath(__file__))
    print(dirname)
    log_path = dirname + "\\log"
    mkdir(log_path)
except OSError as error:
    print(f"Folder exists already, so: {error}")


dir_list = listdir(log_path)
print(dir_list)
for i in range(1000):
    if "dqn" + str(i) not in dir_list:
        logfile_path = log_path + "/dqn" + str(i)
        break
writer = SummaryWriter(logfile_path)
logger = TensorboardLogger(writer)


"""Initialise Environments"""
# torch.cuda.set_device("cuda:0")

# OPEN AI Gym
env = TestEnv()
train_envs = ts.env.DummyVectorEnv([lambda: TestEnv() for _ in range(10)])
test_envs = ts.env.DummyVectorEnv([lambda: TestEnv() for _ in range(100)])

# env = gym.make("CartPole-v0")
# train_envs = ts.env.DummyVectorEnv([lambda: gym.make('CartPole-v0') for _ in range(10)])
# test_envs = ts.env.DummyVectorEnv([lambda: gym.make('CartPole-v0') for _ in range(100)])


class Net(nn.Module):
    def __init__(self, state_shape, action_shape):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(np.prod(state_shape), 20),
            # linear means fully connected. all combinations of inputs are considered!!! so its good
            nn.ReLU(inplace=True),  # or tanh or whatever try&error
            nn.Linear(20, 20),
            # linear means fully connected. all combinations of inputs are considered!!! so its good
            nn.ReLU(inplace=True),  # or tanh or whatever try&error
            # convolution layers: spatial dependence (vector) things close together have spatial correlation
            nn.Linear(20, np.prod(action_shape)),
        )

    def forward(self, obs, state=None, info={}):
        if not isinstance(obs, torch.Tensor):
            # print(obs)
            obs = torch.tensor(obs, dtype=torch.float)
        batch = obs.shape[0]
        logits = self.model(obs.view(batch, -1))
        return logits, state


state_shape = env.observation_space.shape or env.observation_space.n
action_shape = env.action_space.shape or env.action_space.n

net = Net(state_shape, action_shape)
optim = torch.optim.Adam(net.parameters(), lr=1e-2)

policy = ts.policy.DQNPolicy(
    net, optim, discount_factor=0, estimation_step=1, target_update_freq=320
)

train_collector = ts.data.Collector(
    policy, train_envs, ts.data.VectorReplayBuffer(20000, 10), exploration_noise=True
)
test_collector = ts.data.Collector(policy, test_envs, exploration_noise=True)

# train_collector.collect(n_step = 10)

result = ts.trainer.offpolicy_trainer(
    policy,
    train_collector,
    test_collector,
    max_epoch=2,
    step_per_epoch=10000,
    step_per_collect=10,
    update_per_step=0.01,
    episode_per_test=100,
    batch_size=64,
    train_fn=lambda epoch, env_step: policy.set_eps(0.3),
    test_fn=lambda epoch, env_step: policy.set_eps(0.05),
    stop_fn=lambda mean_rewards: mean_rewards >= env.reward_threshold,
    logger=logger,
)  # early stopping
print(f'Finished training! Use {result["duration"]}')

#%%

# policy.eval()

# #%%
# Obs = Batch({"obs": np.array([20, 20]), "info": {}, "done": False})
# # %%
# policy.forward(Obs)
