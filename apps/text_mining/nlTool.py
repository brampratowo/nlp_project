import re
from collections import Counter
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import math
import numpy


class SimilarityHelper(object):
    def cosine_similarity(vec1, vec2):
        vec1 = list(vec1)
        vec2 = list(vec2)
        dot_prod = 0
        for i, v in enumerate(vec1):
            dot_prod += v * vec2[i]
        mag_1 = math.sqrt(sum([x**2 for x in vec1]))
        mag_2 = math.sqrt(sum([x**2 for x in vec2]))
        return dot_prod / (mag_1 * mag_2)

    def euclidean_distance(vec1, vec2):
        sVec1 = numpy.array(vec1)
        sVec2 = numpy.array(vec2)
        return numpy.linalg.norm(sVec1 - sVec2)

    def stemmingSentence(word):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        output = stemmer.stem(word)
        return output

    def getSinonim(word, mydict):
        if word in mydict.keys():
            return mydict[word]["sinonim"]
        else:
            return []


class SpellingCheckerHelper(object):
    def words(text):
        return re.findall(r"\w+", text.lower())

    @classmethod
    def correction(self, word, WORDS):
        return {word: self.candidates(word, WORDS)}

    @classmethod
    def candidates(self, word, WORDS):
        # "Generate possible spelling corrections for word."
        return (
            self.known([word], WORDS)
            or self.known(self.edits1(word), WORDS)
            or self.known(self.edits2(word), WORDS)
            or [word]
        )

    @classmethod
    def known(self, words, WORDS):
        # "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in WORDS)

    @classmethod
    def edits1(self, word):
        # "All edits that are one edit away from `word`."
        letters = "abcdefghijklmnopqrstuvwxyz"
        separates = []

        # [('', 'kemarin'), ('k', 'emarin'), ('ke', 'marin'), dst]
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

        # ['emarin', 'kmarin', 'kearin', dst]
        deletes = [L + R[1:] for L, R in splits if R]

        # ['ekmarin', 'kmearin', 'keamrin', dst]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]

        # ['aemarin', 'bemarin', 'cemarin', dst]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]

        # ['akemarin', 'bkemarin', 'ckemarin', dst]
        inserts = [L + c + R for L, R in splits for c in letters]

        for L, R in splits:
            separates.append(L)
            separates.append(R)
            
        return set(separates + deletes + transposes + replaces + inserts)

    @classmethod
    def edits2(self, word):
        # "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


class SearchDocHelper(object):
    @classmethod
    def word_count(self, query):
        counts = dict()
        words = query.lower().split()
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        return counts

    @classmethod
    def termFrequency(self, term, document):
        normalizeDocument = document.lower().split()
        return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))

    @classmethod
    def inverseDocumentFrequency(self, word, documents, key_column):
        count = 0
        for doc in documents:
            if word.lower() in doc[key_column].lower().split():
                count += 1
        if count > 0:
            return 1.0 + math.log(float(len(documents)) / count)
        else:
            return 1.0

    @classmethod
    def tf_idf(self, query, document, documents, key_column):
        tf = self.termFrequency(query, document)
        idf = self.inverseDocumentFrequency(query, documents, key_column)
        return tf * idf

    @classmethod
    def generateVectors(self, query, documents, key_column):
        tf_idf_matrix = numpy.zeros((len(query.split()), len(documents)))
        for i, word in enumerate(query.lower().split()):
            idf = self.inverseDocumentFrequency(word, documents, key_column)
            for j, doc in enumerate(documents):
                tf_idf_matrix[i][j] = idf * self.termFrequency(word, doc[key_column])
        return tf_idf_matrix

    @classmethod
    def build_query_vector(self, query, documents, key_column):
        count = self.word_count(query)
        vector = numpy.zeros((len(count), 1))
        for i, word in enumerate(query.lower().split()):
            vector[i] = (
                float(count[word])
                / len(count)
                * self.inverseDocumentFrequency(word, documents, key_column)
            )
        return vector

    @classmethod
    def consine_similarity(self, doc, v1, v2):
        lin = float(numpy.linalg.norm(v1) * numpy.linalg.norm(v2))
        if lin > 0:
            return numpy.dot(v1, v2) / float(
                numpy.linalg.norm(v1) * numpy.linalg.norm(v2)
            )
        else:
            return [[0]]

    @classmethod
    def compute_relevance(self, query, documents, key_column):
        tf_idf_matrix = self.generateVectors(query, documents, key_column)
        query_vector = self.build_query_vector(query, documents, key_column)
        data_list_result = []
        for i, doc in enumerate(documents):
            similarity = self.consine_similarity(
                doc, tf_idf_matrix[:, i].reshape(1, len(tf_idf_matrix)), query_vector
            )
            doc["Similarity"] = similarity[0][0]
            data_list_result.append(doc)
        data_list_result.sort(key=lambda x: x["Similarity"], reverse=True)
        return data_list_result
