import pandas as pd
import wandb
import sys


if __name__ == "__main__":
    row = sys.argv[1]
    df = pd.read_csv('hyperparams.csv')
    df.drop('Unnamed: 0', inplace=True, axis=1)
    df.drop('Stopped early?', inplace=True, axis=1)
    dict_data = df.transpose().to_dict()


    # Pass your defaults to wandb.init
    wandb.init(config=dict_data[int(row)])
    config = wandb.config


    wandb.log(dict_data[int(row)])