# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/13 10:17
# @author   :Mo
# @function :setup of nlp_xiaojiang
# @codes    :copy from https://github.com/TianWenQAQ/Kashgari/blob/master/setup.py

from setuptools import find_packages, setup
import pathlib

# Package meta-data.
NAME = 'augment'

'''
required = [
            'scikit-learn>=0.19.1',
            'fuzzywuzzy>=0.17.0',
            'openpyxl>=2.6.2',
            'xpinyin>=0.5.6',
            'gensim>=3.7.1',
            'jieba>=0.39',
            'xlrd>=1.2.0',
            'tensorflow>=1.8.0',
            'keras-bert>=0.41.0',
            'Keras>=2.2.0',
            'pandas>=0.23.0',
            'h5py>=2.7.1',
            'numpy>=1.16.1',
            'pyemd==0.5.1',
            'pathlib',
            'translate',
            'PyExecJS',
            'stanfordcorenlp',]
'''

setup(name=NAME,
        version='0.0.1',
        packages=find_packages(),
        include_package_data=True,
        # install_requires=required,
        )


if __name__ == "__main__":
    print("setup ok!")
