from nlp_utils.text_tools import load_word2vec_model
from conf.path_config import word2_vec_path
from nlp_utils.text_tools import is_total_english
from nlp_utils.text_tools import is_total_number
from conf.path_config import stop_words_path
from nlp_utils.text_tools import jieba_cut
from conf.path_config import eda_gen_path
from random import shuffle
import synonyms
import random


random.seed(1234)


# 停用词列表，默认使用hanlp停用词表
f_stop = open(stop_words_path, "r", encoding="utf-8")
stop_words = []
for stop_word in f_stop.readlines():
    stop_words.append(stop_word.strip())

def get_syn_by_synonyms(word):
    if not is_total_english(word.strip()):
        return synonyms.nearby(word)[0]
    else:
        return word

def sr(words, n, key_words):
    """
      同义词替换,替换一个语句中的n个单词为其同义词
    """
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stop_words]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        sim_synonyms = get_syn_by_synonyms(random_word)
        if len(sim_synonyms) >= 1 and random_word not in key_words and not is_total_english(random_word) and not is_total_number(random_word):
            synonym = random.choice(sim_synonyms)
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break
    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')
    return new_words


def add_word(new_words, key_words):
    """
      在list上随机插入一个同义词
    """
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words) - 1)]
        if random_word not in key_words and not is_total_english(random_word) and not is_total_number(random_word):
            synonyms = get_syn_by_synonyms(random_word)
            counter += 1
        if counter >= 10:
            return
    random_synonym = random.choice(synonyms)
    random_idx = random.randint(0, len(new_words) - 1)
    new_words.insert(random_idx, random_synonym)

def ri(words, n, key_words):
    """
      随机插入, 随机在语句中插入n个词
    """
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words, key_words)
    return new_words

def swap_word(new_words):
    """
        随机交换，随机交换两个词语
    """
    random_idx_1 = random.randint(0, len(new_words) - 1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words) - 1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
    return new_words

def rs(words, n):
    """
      随机交换，随机交换两个词语n次数
    """
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    return new_words

def rd(words, p, key_words):
    """
      随机删除,以概率p删除语句中的词
    """
    if len(words) == 1:
        return words

    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p or word in key_words:
            new_words.append(word)

    if len(new_words) == 0:
        rand_int = random.randint(0, len(words) - 1)
        return [words[rand_int]]

    return new_words


def sentence_replace_whitespace(sentences):
    """
      去除空格
    """
    sentences_new = []
    for sentence in sentences:
        sentence_replace = sentence.replace(" ", "").strip()
        sentences_new.append(sentence_replace + "\n")
    return sentences_new


def eda(sentence, alpha=0.1, num_aug=3, key_words=[], eda_method='sr'):
    # EDA函数，可选同义词替换、插入词汇、交换词语顺序、删除词语
    seg_list = jieba_cut(sentence)
    seg_list = " ".join(seg_list)
    words = list(seg_list.split())
    tot_words = len(words)

    results = []
    alpha_n = max(1, int(alpha * tot_words)) * 2

    # 同义词替换sr
    if eda_method == 'sr' :
        for _ in range(num_aug * 2):
            temp = sr(words, alpha_n, key_words)
            results.append(''.join(temp))

    # 随机插入ri
    if eda_method == 'ri' :
        for _ in range(num_aug * 2):
            temp = ri(words, alpha_n, key_words)
            results.append(''.join(temp))

    # 随机交换rs
    if eda_method == 'rs' :
        for _ in range(num_aug * 2):
            temp = rs(words, alpha_n)
            results.append(''.join(temp))

    # 随机删除rd
    if eda_method == 'rd' :
        for _ in range(num_aug * 2):
            temp = rd(words, alpha, key_words)
            results.append(''.join(temp))

    results = list(set(results))
    shuffle(results)

    if len(results) > num_aug:
        results = results[0:num_aug]
    # augmented_sentences.append(seg_list)
    return results


if __name__ == "__main__":
    while True:
        print('输入: ')
        sen = input()
        syn = []
        syn.append(eda(sentence=sen,eda_method='sr',num_aug = 5))
        syn.append(eda(sentence=sen,eda_method='ri',num_aug = 5))
        syn.append(eda(sentence=sen,eda_method='rs',num_aug = 5))
        syn.append(eda(sentence=sen,eda_method='rd',num_aug = 5))
        print(syn)
        with open(eda_gen_path, 'w') as f:
            for sen in syn :
                f.write(sen)
