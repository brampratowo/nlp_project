# Program to measure the similarity between
# two sentences using cosine similarity.

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from .helper import HelperFunction
from .helper import SetEncoder
from .nlTool import SimilarityHelper
from .nlTool import SpellingCheckerHelper
from .nlTool import SearchDocHelper
from collections import Counter
import os.path
import json
from enum import Enum
from nlp_project import settings


class TextMiningEnum(Enum):
    COSINE_SIMILARITY = 1
    EUCLIDEAN_DISTANCE = 2


class LanguageTool:
    @classmethod
    def getValueSimilarity(
        self, textAnswering, textComparing, text_mining_type: TextMiningEnum
    ):
        # tokenization
        aswering_token = word_tokenize(textAnswering.lower())
        comparing_token = word_tokenize(textComparing.lower())

        # load kata sambung bahasa indonesia
        sw = stopwords.words("indonesian")

        # menghilangkan stopword
        # melakukan stemming (merubah menjadi kata dasar tanpa imbuhan)
        answering_set = {
            SimilarityHelper.stemmingSentence(w) for w in aswering_token if not w in sw
        }
        comparing_set = {
            SimilarityHelper.stemmingSentence(w) for w in comparing_token if not w in sw
        }

        # membuka kamus sebagai basis data sinonim/padanan kata
        synonym_dict = HelperFunction.loadJsonFile(
            os.path.join(settings.BASE_DIR, os.path.normpath("static/data/sinonim_antonim_bahasa.json"))
        )

        # mencari sinonim / padanan kata
        comp_synonym_list_temp = []
        for comp_word in comparing_set:
            comp_synonym_list_temp.append(
                {comp_word: SimilarityHelper.getSinonim(comp_word, synonym_dict)}
            )

        comp_json_data = json.dumps(comp_synonym_list_temp)
        for data in json.loads(comp_json_data):
            for key in data.keys():
                if key not in answering_set:
                    for syn in data[key]:
                        if syn in answering_set:
                            comparing_set.discard(key)
                            comparing_set.add(syn)

        # form a set containing keywords of both strings
        l1 = []
        l2 = []
        uniqueWords = answering_set.union(comparing_set)
        for w in uniqueWords:
            if w in answering_set:
                l1.append(1)  # create a vector
            else:
                l1.append(0)
            if w in comparing_set:
                l2.append(1)
            else:
                l2.append(0)

        # cosine or  formula
        if text_mining_type == TextMiningEnum.COSINE_SIMILARITY:
            return SimilarityHelper.cosine_similarity(l1, l2)
        if text_mining_type == TextMiningEnum.EUCLIDEAN_DISTANCE:
            return SimilarityHelper.euclidean_distance(l1, l2)

    @classmethod
    def spellChecker(self, sentence):
        WORDS = Counter(
            SpellingCheckerHelper.words(
                HelperFunction.loadTextFile(
                    os.path.join(settings.BASE_DIR, os.path.normpath("static/data/kamus-kbbi.txt"))
                )
            )
        )

        sentence_token = word_tokenize(sentence.lower())
        listCorrection = []
        word_list = [word for word in sentence_token if word.isalnum()]
        
        for word in word_list:
            listCorrection.append(SpellingCheckerHelper.correction(word, WORDS))

        return SetEncoder().encode(listCorrection)

    @classmethod
    def searchDocumentRanking(self, query, documents, key_column):
        unique_query = ' '.join(set(query.split(' ')))
        data_result_all = SearchDocHelper.compute_relevance(unique_query, documents, key_column)
        data_result_similar = [data for data in data_result_all if data["Similarity"] > 0]
        return data_result_similar[:100]
