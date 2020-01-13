# -*- coding: utf-8 -*-
#
import math

from utils.Utility import *


class TFIDFRetrievalModel:
    def __init__(self):
        self.results_folder = TF_IDF_RESULTS_FOLDER
        self.inverted_index_file = None
        self.inverted_index_data_dict = None
        self.doc_terms_count_file = None
        self.doc_terms_count_dict = None
        self.queries_list = None
        self.corpus_tf_idf_scores_dict = {}

    def load_data_files(self):
        self.inverted_index_file = open(INVERTED_INDEX_FILE, "rb")
        self.inverted_index_data_dict = eval(self.inverted_index_file.read())
        self.doc_terms_count_file = open(DOC_TERMS_COUNT_FILE, "rb")
        self.doc_terms_count_dict = eval(self.doc_terms_count_file.read())
        self.queries_list = get_queries(PARSED_QUERIES_FILE)

    def tfidf_score_calculator(self):
        print('----------------- Computing TF-IDF Score for each term -----------------')
        no_of_docs = get_total_docs_in_corpus()

        for word in self.inverted_index_data_dict:
            self.corpus_tf_idf_scores_dict[word] = {}
            for doc_id in self.inverted_index_data_dict[word]:
                tf = float(self.inverted_index_data_dict[word][doc_id]) / float(self.doc_terms_count_dict[doc_id])
                idf = 1.0 + (math.log(no_of_docs / (len(self.inverted_index_data_dict[word]) + 1.0)))
                self.corpus_tf_idf_scores_dict[word][doc_id] = tf * idf

    def compute_rank(self):
        self.tfidf_score_calculator()

        for query_id in range(1, len(self.queries_list) + 1):
            print('----------------- Computing Rank for Query %s -----------------' % query_id)
            query_list = self.compute_query_term_frequency(self.queries_list[query_id - 1])
            score_list = self.compute_doc_score(query_list)
            self.write_doc_score_to_file(query_id, score_list)

    def compute_doc_score(self, query_list):
        doc_score_list = {}
        for query_term in query_list:
            for doc_id in query_list[query_term]:
                if doc_id not in doc_score_list:
                    doc_tf = 0
                    for word in query_list:
                        if doc_id in query_list[word].keys():
                            doc_tf += query_list[word][doc_id]
                    doc_score_list[doc_id] = doc_tf
        return doc_score_list

    def compute_query_term_frequency(self, query_sentence):
        query_list = {}
        for query_term in query_sentence.split():
            if query_term not in self.corpus_tf_idf_scores_dict:
                query_list[query_term] = {}
            else:
                query_list[query_term] = self.corpus_tf_idf_scores_dict[query_term]
        return query_list

    def write_doc_score_to_file(self, query_id, doc_to_score):
        queries_results_file_name = self.results_folder + 'query_{}_rank_list.txt'.format(query_id)
        query_report_file = open(queries_results_file_name, 'w+')
        sorted_result_list = sorted(doc_to_score.items(), key=lambda kv: kv[1], reverse=True)
        for i in range(len(sorted_result_list[:NO_OF_SEARCH_RESULTS])):
            search_result = sorted_result_list[i]
            query_report_file.write(str(query_id) + " " + 'Q0' + " " + str(search_result[0]) + " " + str(i + 1) + " " + str(search_result[1]) + " " + "TF_IDF_IR_MODEL \n")
        query_report_file.close()
