import pathlib
import sys
import os


# base dir
projectdir = str(pathlib.Path(os.path.abspath(__file__)).parent.parent)
sys.path.append(projectdir)
print(projectdir)

# stop_words_path
stop_words_path =  projectdir + '/Data/common_words/stopwords.txt'

# eda_gen_path
eda_gen_path = projectdir + '/Data/eda_gen/result.txt'



