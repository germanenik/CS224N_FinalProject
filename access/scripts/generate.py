# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import fileinput

from access.preprocessors import get_preprocessors
from access.resources.prepare import prepare_models
from access.simplifiers import get_fairseq_simplifier, get_preprocessed_simplifier
from access.text import word_tokenize
from access.utils.helpers import yield_lines, write_lines, get_temp_filepath, mute
from access.resources.paths import REPO_DIR


if __name__ == '__main__':
    # Usage: python generate.py < my_file.complex
    # Read from stdin
    source_filepath = get_temp_filepath()
    write_lines([word_tokenize(line) for line in fileinput.input()], source_filepath)
    # Load best model
    #best_model_dir = prepare_models() #test on default model
    best_model_dir = REPO_DIR / 'experiments/fairseq/local_1615780248144' #test on our model
    recommended_preprocessors_kwargs = {
        'LengthRatioPreprocessor': {'target_ratio': 0.7999999999999999},
        'LevenshteinPreprocessor': {'target_ratio': 0.42647234616101964},
        'WordRankRatioPreprocessor': {'target_ratio': 0.7999999999999999},
        'SentencePiecePreprocessor': {'vocab_size': 10000},
    }
    preprocessors = get_preprocessors(recommended_preprocessors_kwargs)
    simplifier = get_fairseq_simplifier(best_model_dir, beam=8)
    simplifier = get_preprocessed_simplifier(simplifier, preprocessors=preprocessors)
    # Simplify
    pred_filepath = get_temp_filepath()
    with mute():
        simplifier(source_filepath, pred_filepath)
    for line in yield_lines(pred_filepath):
        print(line)
