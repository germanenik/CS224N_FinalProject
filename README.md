# CS224N_FinalProject
legalese simplification

PreSumm repo: https://github.com/nlpyang/PreSumm <br /> 
Trials:
* Part0 -  dirty data, around 20 ToS?
* Full0 - all dirty data
* Clean0 - manually cleaned data, ~10 ToS
* Clean1 - repeat of clean0 but random split
* Clean2 - clean0 + algorithmically determined clean data, ~100 ToS (~2000 chunk files)
* Clean 3 - same as clean2 but with saved file breakdown 
* Clean 4 - same as clean3 but kept only a regex of characters

*** above trials were all trained on non-empty highlights ***

* Clean6 - clean3 but including empty highlights
* Clean aug6 - clean6 w 1,000 augmented data (on chunk0s) only in the training set
* Clean7 (in progress) - clean6 but with "blank" under each blank highlight instead of an empty string

ACCESS repo: https://github.com/facebookresearch/access
