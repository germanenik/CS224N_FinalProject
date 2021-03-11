import os
import pandas as pd

df = pd.read_csv('hyperparams.csv')
df.drop('Unnamed: 0', inplace=True, axis=1)
df.drop('Stopped early?', inplace=True, axis=1)
dict_data = df.transpose().to_dict()

os.system('source venv/bin/activate')
for row in dict_data:
    os.system(f'python wandb_log.py {row}')