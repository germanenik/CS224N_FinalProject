# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from access.fairseq.main import fairseq_train_and_evaluate
from access.resources.prepare import prepare_wikilarge, prepare_turkcorpus
import random
import sys
import uuid
import os
from glob import glob
from shutil import rmtree

if __name__ == '__main__':
    while(True):
        orig_stdout = sys.stdout
        f = open(f'{uuid.uuid4()}.txt', 'w')
        sys.stdout = f
        print('Training a model from scratch')
        prepare_wikilarge()
        prepare_turkcorpus()
        random_kwargs = {
            'arch': 'transformer',
            'warmup_updates': 4000,
            'parametrization_budget': 256,
            'beam': random.randint(2, 10),
            'dataset': 'simplification',
            'dropout': random.random(),
            'fp16': False,
            'label_smoothing': random.random(),
            'lr': random.random() * (10.0 ** random.randint(-5, 0)),
            'lr_scheduler': 'fixed',
            'max_epoch': 100,
            'max_tokens': 5000,
            'metrics_coefs': [0, 1, 0],
            'optimizer': 'adam',
            'validations_before_sari_early_stopping': 10,
            'preprocessors_kwargs': {
                'LengthRatioPreprocessor': {
                    'target_ratio': random.random()  # Default initial value
                },
                'LevenshteinPreprocessor': {
                    'target_ratio': random.random()  # Default initial value
                },
                'WordRankRatioPreprocessor': {
                    'target_ratio': random.random()  # Default initial value
                },
                'DependencyTreeDepthRatioPreprocessor': {
                    'target_ratio': random.random()  # Default initial value
                },
                'SentencePiecePreprocessor': {
                    'vocab_size': 10000
                }
            }
        }
        kwargs = {
            'arch': 'transformer',
            'warmup_updates': 4000,
            'parametrization_budget': 256,
            'beam': 8,
            'dataset': 'simplification',
            'dropout': 0.93761351,
            'fp16': False,
            'label_smoothing': 0.55591264,
            'lr': 0.0000487,
            'lr_scheduler': 'fixed',
            'max_epoch': 100,
            'max_tokens': 5000,
            'metrics_coefs': [0, 1, 0],
            'optimizer': 'adam',
            'validations_before_sari_early_stopping': 10,
            'preprocessors_kwargs': {
                'LengthRatioPreprocessor': {
                    'target_ratio': 0.74780667
                },
                'LevenshteinPreprocessor': {
                    'target_ratio': 0.96770866
                },
                'WordRankRatioPreprocessor': {
                    'target_ratio': 0.48898006
                },
                'DependencyTreeDepthRatioPreprocessor': {
                    'target_ratio': 0.98223764
                },
                'SentencePiecePreprocessor': {
                    'vocab_size': 10000
                }
            }
        }
        try:
            fairseq_train_and_evaluate(**random_kwargs)
        except:
            print('this run failed.')
        sys.stdout = orig_stdout
        f.close()
        path = 'resources/datasets/'
        pattern = os.path.join(path, "_*")

        for item in glob(pattern):
            if not os.path.isdir(item):
                continue
            rmtree(item)
            print('removing', item)
