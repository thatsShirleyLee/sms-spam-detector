from sentence_transformers import SentenceTransformer, util

# nltk.download('punkt')
# nltk.download('stopwords')
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.data import load
from nltk.stem import SnowballStemmer
from string import punctuation
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# 创建一些函数，处理西班牙语
stemmer_en = SnowballStemmer('english')


class Tokenizer:
    @staticmethod
    def stem_tokens(tokens, stemmer):
        stems = []
        for token in tokens:
            stems.append(stemmer.stem(token))
        return stems

    @staticmethod
    def tokenize_stem(text):
        text = ''.join([s for s in text if s not in Tokenizer.non_words])
        tokens = word_tokenize(text)
        tokens = Tokenizer.stem_tokens(tokens, stemmer_en)
        return tokens

    # 准备标点列表
    non_words = list(punctuation)
    non_words.extend(map(str, range(10)))
    # print("Symbols to be removed (%d):" % len(non_words), non_words)
    # 准备英语停顿词列表
    english_stopwords = stopwords.words('english')
    # print("Stop-words to be removed (%d):" % len(english_stopwords), english_stopwords)


class BertVectorizer:
    model = SentenceTransformer(
        'D:\GraduationDesign\sms-spam-detector\sentence-transformers\distiluse-base-multilingual-cased-v1')

    @staticmethod
    def fit_transform(data):
        print("\n\n使用BERT模型编码中... ")
        data_vecs = []
        for i, d in enumerate(data):
            data_vec = BertVectorizer.model.encode(d)
            data_vecs.append(data_vec)
            print(".", end="" if (i % 100 > 0) else ("%4d\n" % i))
        return np.array(data_vecs)
