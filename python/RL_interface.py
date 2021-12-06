#%%
from copy import deepcopy

import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

from agents import *
from main import run_full_simulation
from RL_agents import *
from RL_env import CropwarEnv

name = "CropWar_PPO_expanding_budgetreward"


def run_trainer():
    """Train, Train, Train,...

    Train the Policy using many iterations using the PPO algorithm.py

    :return: a copy of the finally trained model.
    :rtype: SB3 model
    """
    global name
    # Parallel environments
    env = make_vec_env(CropwarEnv, n_envs=8)
    model = PPO(
        "MlpPolicy", env, verbose=1, tensorboard_log="python\log_ppo"
    )
    model.learn(total_timesteps=1e6)

    model.save(name)
    print(
        f"Saved Model as {name}.\
         Rename this file if you like the results (for permanent storage)."
    )
    return model


def evaluate():
    """evaluate the trained Reinforcement model."""
    global name

    print(f"Use previousely trained model {name}.")
    try:
        ml_model = PPO.load(name)
        print(f"Loaded the model {name}.")
    except:
        print("Could not find that file. Did you specify the right model name (zip file)?")
        raise FileNotFoundError

    evaluate_parameters = {
        "farmers": {Trader: 0, Introvert: 3, ML_Expander: 1},
        "use_trained_model": ml_model,
        "seed": 0,
    }
    run_full_simulation(custom_parameters=evaluate_parameters)


if __name__ == "__main__":
    # run_trainer()
    evaluate()
