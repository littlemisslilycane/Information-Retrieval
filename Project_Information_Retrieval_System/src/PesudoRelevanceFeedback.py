import nltk
import operator
from utils.Utility import *

K = 10
ALPHA = 1
BETA = 0.75
DELTA = 0.15


def get_query_term_weight(query, inverted_index):
    query_term_weight = {}
    for term in query.split(" "):
        if term not in query_term_weight:
            query_term_weight[term] = 1
        else:
            query_term_weight[term] += 1
    for term in inverted_index:
        if term not in query_term_weight:
            query_term_weight[term] = 0
    return query_term_weight


def get_relevant_document_index(start, end, doc_list, inverted_index):
    doc_index = {}
    current_doc_list = []
    for i in range(start, end + 1):
        current_doc_list.append(doc_list[i - 1])

    for doc in current_doc_list:
        with io.open(CACM_CORPUS_FOLDER + '/' + doc + ".txt", encoding="utf-8") as cache_data:
            doc_text = cache_data.read()
        for term in doc_text.split(' '):
            if term in doc_index:
                doc_index[term] += 1
            else:
                doc_index[term] = 1

    for term in inverted_index:
        if term not in doc_index:
            doc_index[term] = 0

    return doc_index


def get_rocchio_score(q0, rel_dij, non_rel_dij, inverted_index):
    rochchio_scores = {}
    for term in inverted_index:
        initial_weight = q0[term] * ALPHA
        rel_weight = rel_dij[term] * BETA
        non_rel_weight = non_rel_dij[term] * DELTA
        rochchio_scores[term] = initial_weight + rel_weight - non_rel_weight
    return rochchio_scores


def print_enhanced_queries(query, scores):
    suggestion_count = 1
    enhanced_query = ''
    words = nltk.word_tokenize(query)
    for key, value in sorted(scores.items(), key=operator.itemgetter(1), reverse=True):
        if key not in words:
            enhanced_query += key + ' '
        suggestion_count += 1
        if suggestion_count == 20:
            break
    with io.open(STEM_PRF, 'a+', encoding="utf-8") as file_to_write:
        file_to_write.write(unicode(query + ' ' + enhanced_query + '\n'))


def get_enhanced_query(queries, inverted_index):
    for query_id, query in sorted(queries.items(), key=operator.itemgetter(1), reverse=True):
        query_term_frequency = get_query_term_weight(query, inverted_index)
        doc_list = get_doc_collection(query_id, BM25_RESULTS_FOLDER)
        relevant_document_index = get_relevant_document_index(1, K, doc_list, inverted_index)
        non_relevant_document_index = get_relevant_document_index(K + 1, doc_list.__len__(), doc_list, inverted_index)
        scores = get_rocchio_score(query_term_frequency, relevant_document_index, non_relevant_document_index,
                                   inverted_index)
        print_enhanced_queries(query, scores)


def pseudo_relevance_feedback():
    inverted_index = get_inverted_index()
    queries = get_queries_map(PARSED_QUERIES_FILE)
    get_enhanced_query(queries, inverted_index)
