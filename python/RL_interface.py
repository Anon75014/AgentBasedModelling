#%%
from copy import deepcopy

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

from agents import *
from main import run_full_simulation
from ml_agents import *
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
        "MlpPolicy", env, verbose=1, tensorboard_log="python\log_ppo_vs_pretrained"
    )
    model.learn(total_timesteps=1e6)

    model.save(name)
    print(
        f"Saved Model as {name}.\
         Rename this file if you like the results for permanent storage."
    )
    return model


def run_interactive():
    """Interactively train and visualize the Reinforcement Training."""
    global name

    if int(input("Shall I train a new RL agent? 1:yes, 0:no")):
        ml_model = run_trainer()
    else:
        print(f"Use previousely trained model.")

        try:
            ml_model = PPO.load(name)
            print(f"Loaded the mode {name}.")
        except:
            print("Could not find that file. Did you specify the right model name?")

    print("done with model generation part...")
    if int(input("Do you want to see plots? 1:yes, 0:no")):
        training_parameters = {
            "farmers": {Trader: 3, Introvert: 0, ML_Expander: 1},
            "use_trained_model": ml_model,
        }
        run_full_simulation(custom_parameters=training_parameters)


def evaluate():
    """evaluate the trained Reinforcement model."""
    global name

    print(f"Use previousely trained model.")
    try:
        ml_model = PPO.load(name)
        print(f"Loaded the mode {name}.")
    except:
        print("Could not find that file. Did you specify the right model name?")
        raise FileNotFoundError

    evaluate_parameters = {
        "farmers": {Trader: 0, Introvert: 3, ML_Expander: 1},
        "use_trained_model": ml_model,
        "seed": 0,
    }
    run_full_simulation(custom_parameters=evaluate_parameters)


if __name__ == "__main__":
    # run_trainer()
    # run_interactive()
    evaluate()