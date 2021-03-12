import wandb
import pandas as pd

if __name__ == '__main__':
	df = pd.read_csv("Hyperparameter Tuning - Sheet1.csv", encoding='utf-8-sig')
	# 1. Start a W&B run
	wandb.init(project='224N-legalese', entity='hazh')

	# 2. Save model inputs and hyperparameters
	config = wandb.config
	config.learning_rate = 0.01

	# Model training here

	# 3. Log metrics over time to visualize performance
	wandb.log({"loss": loss})
	    