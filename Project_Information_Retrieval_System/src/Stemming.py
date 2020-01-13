from nltk import PorterStemmer
from nltk import word_tokenize
import itertools
import operator
from utils.Utility import *

inverted_index = {}
stem_classes = {}


def get_dice_coefficient(pair):
    a = pair[0]
    b = pair[1]
    # find n(a) - number of documents containing a
    da = inverted_index[a].keys()
    na = da.__len__()
    # find n(b) - number of documents containing b
    db = inverted_index[b].keys()
    nb = db.__len__()
    common_documents = set(da) - set(db)
    nab = common_documents.__len__()
    if nab != 0 and (na != 0 or nb != 0):
        coefficient = (2 * nab) / (na + nb)
    else:
        coefficient = 0
    return coefficient


# Generate stem classes for the corpus
def generate_stem_classes(inverted_index):
    stemmer = PorterStemmer()
    stem_classes = {}
    for term in inverted_index:
        stem = stemmer.stem(term)
        if stem != term:
            if stem not in stem_classes:
                stem_classes[stem] = {term}
            else:
                stem_classes.get(stem).add(term)
    return stem_classes


# Print the new queries expansion terms
def write_enhanced_query(new_queries, query):
    enhanced_query = ''
    words = word_tokenize(query)
    for term in words:
        if term.strip() != '':
            enhanced_query += term + ' '
            for new_query in new_queries[term]:
                enhanced_query += new_query + ' '
    with io.open(STEM_ENHANCED, 'a+', encoding="utf-8") as filetowrite:
        filetowrite.write(unicode(enhanced_query + '\n'))


def query_expansion(queries, stem_classes):
    for query in queries:
        new_queries = {}
        stemmer = PorterStemmer()
        words = word_tokenize(query)
        words = list(set(words))
        for word in words:
            stem = stemmer.stem(word)
            if stem in stem_classes:
                new_queries[word] = stem_classes[stem]
                association_pairs = itertools.combinations(new_queries[word], 2)
                association_metric = {}
                for pair in list(association_pairs):
                    association_metric[pair] = get_dice_coefficient(pair)
                # Eliminate pairs which have no association
                refined_classes = []
                for key, value in sorted(association_metric.items(), key=operator.itemgetter(1), reverse=True):
                    if value != 0:
                        refined_classes.append(key[0])
                        refined_classes.append(key[1])
                refined_classes = list(set(refined_classes))
                if word in refined_classes: refined_classes.remove(word)
                new_queries[word] = refined_classes
            else:
                new_queries[word] = {}
        write_enhanced_query(new_queries, query)


def query_time_stemming():
    global inverted_index
    inverted_index = get_inverted_index()
    global stem_classes
    stem_classes = generate_stem_classes(inverted_index)
    queries = get_queries(PARSED_QUERIES_FILE)
    query_expansion(queries, stem_classes)
