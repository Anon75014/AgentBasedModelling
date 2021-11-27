#%%
from copy import deepcopy

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

from main import run_full_simulation
from RL_env import CropwarEnv


def run_trainer():
    """Train, Train, Train,...

    Train the Policy using many iterations using the PPO algorithm.py
    
    :return: a copy of the finally trained model.
    :rtype: SB3 model
    """

    # Parallel environments
    env = make_vec_env(CropwarEnv, n_envs=10)
    #%%
    model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="python\log_ppo")
    model.learn(total_timesteps=100000)

    model.save("CropWar_PPO")
    print(
        "Saved Model as CropWar_PPO.\
         Rename this file if you like the results for permanent storage."
    )
    return deepcopy(model)


def run_interactive():
    """Interactively train and visualize the Reinforcement Training."""
    if int(input("Shall I train a new RL agent? 1:yes, 0:no")):
        ml_model = run_trainer()
    else:
        print(f"Use previousely trained model.")

        try:
            ml_model = PPO.load("CropWar_PPO_converging11_100ksteps")
        except:
            print("Could not find that file. Did you specify the right model name?")

    if int(input("Do you want to see plots? 1:yes, 0:no")):
        run_full_simulation(use_ml_model=ml_model)


if __name__ == "__main__":
    run_trainer()


#%%
