#%%
from copy import deepcopy

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

from main import run_full_simulation
from RL_env import CropwarEnv

name = "CropWar_PPO_vDezCanChange"


def run_trainer():
    """Train, Train, Train,...

    Train the Policy using many iterations using the PPO algorithm.py

    :return: a copy of the finally trained model.
    :rtype: SB3 model
    """
    global name
    # Parallel environments
    env = make_vec_env(CropwarEnv, n_envs=2)
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="python\log_ppo_vsTraders")
    model.learn(total_timesteps=1e5)

    model.save(name)
    print(
        f"Saved Model as {name}.\
         Rename this file if you like the results for permanent storage."
    )
    return deepcopy(model)


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
        run_full_simulation(use_ml_model=ml_model)


def evaluate():
    """evaluate the trained Reinforcement model."""
    global name

    print(f"Use previousely trained model.")
    try:
        ml_model = PPO.load(name)
        print(f"Loaded the mode {name}.")
    except:
        print("Could not find that file. Did you specify the right model name?")

    run_full_simulation(use_ml_model=ml_model)


if __name__ == "__main__":
    # run_trainer()
    # run_interactive()
    evaluate()
#%%
