import os
import json

directory = r'.'
for filename in os.listdir(directory):
    if filename.endswith(".txt") and filename != 'requirements.txt':
        fp = open(filename)
        data_for_file = None
        last_scores = None
        last_loss_data = dict()
        run_failed = False
        recommended_kwargs = None
        for i, line in enumerate(fp):
            if i == 3 and line.startswith('kwargs'):
                line = line.replace('\'', '"')[len('kwargs='):]
                line = line.replace('False', '"False"')
                data_for_file = json.loads(line)
            elif line.startswith('ts_scores'):
                line = line.replace('\'', '"')[len('ts_scores='):]
                last_scores = json.loads(line)
            elif line.startswith('scores'):
                line = line.replace('\'', '"')[len('scores='):]
                last_scores = json.loads(line)
                last_scores["BLEU"] = last_scores['bleu']
                last_scores["SARI"] = last_scores['sari_legacy']
                last_scores["FKGL"] = last_scores['fkgl']
            elif line.startswith('| epoch'):
                vals = line.split('|')
                for val in vals:
                    if val:
                        info = val.strip().split(' ')
                        last_loss_data[info[0]] = info[1]
            elif line.startswith('this run failed.'):
                run_failed = True
            elif line.startswith('recommended_preprocessors_kwargs'):
                line = line.replace('\'', '"')[len('recommended_preprocessors_kwargs='):]
                recommended_kwargs = json.loads(line)
        if last_scores:
            print_string = (f'{run_failed},'
                f'{last_scores["BLEU"]},'
                f'{last_scores["SARI"]},'
                f'{last_scores["FKGL"]},'
                f'{last_loss_data["loss"]},'
                f'{last_loss_data["nll_loss"]},'
                f'{data_for_file["warmup_updates"]},'
                f'{data_for_file["parametrization_budget"]},'
                f'{data_for_file["beam"]},'
                f'{data_for_file["dropout"]},'
                f'{data_for_file["fp16"]},'
                f'{data_for_file["label_smoothing"]},'
                f'{data_for_file["lr"]},'
                f'{data_for_file["lr_scheduler"]},'
                f'{data_for_file["max_epoch"]},'
                f'{data_for_file["max_tokens"]},'
                f'{data_for_file["optimizer"]},'
                f'{data_for_file["preprocessors_kwargs"]["LengthRatioPreprocessor"]["target_ratio"]},'
                f'{data_for_file["preprocessors_kwargs"]["LevenshteinPreprocessor"]["target_ratio"]},'
                f'{data_for_file["preprocessors_kwargs"]["WordRankRatioPreprocessor"]["target_ratio"]},'
                f'{data_for_file["preprocessors_kwargs"]["DependencyTreeDepthRatioPreprocessor"]["target_ratio"]},')
            if recommended_kwargs:
                print_string += (
                    f'{recommended_kwargs["LengthRatioPreprocessor"]["target_ratio"]},'
                    f'{recommended_kwargs["LevenshteinPreprocessor"]["target_ratio"]},'
                    f'{recommended_kwargs["WordRankRatioPreprocessor"]["target_ratio"]},'
                    f'{recommended_kwargs["DependencyTreeDepthRatioPreprocessor"]["target_ratio"]},'
                )
            print(print_string)
        fp.close()
        if run_failed and not last_scores:
            os.remove(filename)
    else:
        continue