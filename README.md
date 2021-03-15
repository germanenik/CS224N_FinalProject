# CS224N_FinalProject
legalese simplification

PreSumm repo: https://github.com/nlpyang/PreSumm
Trials:
Part0 -  dirty data, around 20 ToS?
Full0 - all dirty data
Clean0 - manually cleaned data, ~10 ToS
Clean1 - repeat of clean0 but random split
Clean2 - clean0 + algorithmically determined clean data, ~100 ToS (~2000 chunk files)
Clean 3 - same as clean2 but with saved file breakdown 
Clean 4 - same as clean3 but kept only a regex of characters

Clean aug1 - clean 3 w 1,000 augmented (on chunk0s) data only in the training set
Clean aug2 - clean 3 w 10,000 augmented data  (on chunk0s) only in the training set
Clean aug3 - clean 3 w 10,000 augmented data (on all chunks) only in the training set

*** above trials were all trained on non-empty highlights ***

Clean5 - clean3 but with min tat len of 0
Clean aug4 - clean 3 w 10,000 augmented data  (on chunk0s) only in the training set and tat Len of 0
Clean aug5 - clean 3 w 1,000 augmented data  (on chunk0s) only in the training set and tat Len of 0

ACCESS repo: https://github.com/facebookresearch/access
