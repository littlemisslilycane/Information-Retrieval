import traceback
from math import log

from config import *
from utils.Utility import get_queries


class BM25RetrievalModel:

    def __init__(self):
        self.results_folder = BM25_RESULTS_FOLDER
        self.corpus_folder = CACM_CORPUS_FOLDER

        print(self.results_folder)
        self.b = BM25_B
        self.k1 = BM25_K1
        self.k2 = BM25_K2
        self.R = BM25_R
        self.relevant_info = BM25_RELEVANT_INFO
        self.query_freq = BM25_QUERY_FREQ
        self.average_doc_length = 0

        self.doc_term_freq_dict = {}
        self.queries_list = get_queries(PARSED_QUERIES_FILE)
        self.token_count = {}
        self.inverted_index_file = None
        self.inverted_index_data_dict = None

    def load_index_file(self):
        self.inverted_index_file = open(INVERTED_INDEX_FILE, "rb")
        self.inverted_index_data_dict = eval(self.inverted_index_file.read())

    def bm25_score_calculator(self, n, doc_length, term_freq):
        K = self.k1 * ((1 - self.b) + self.b * (float(doc_length) / float(self.average_doc_length)))
        formula_part_1 = ((self.relevant_info + 0.5) / (self.R - self.relevant_info + 0.5)) / (
                    (n - self.relevant_info + 0.5) / (
                        len(self.doc_term_freq_dict) - n - self.R + self.relevant_info + 0.5))
        formula_part_1 = log(formula_part_1)
        formula_part_2 = ((self.k1 + 1) * term_freq) / (K + term_freq)
        formula_part_3 = ((self.k2 + 1) * self.query_freq) / (self.k2 + self.query_freq)
        return formula_part_1 * formula_part_2 * formula_part_3

    def compute_doc_average_length(self):
        print('----------------- Computing Doc Average Length -----------------')
        try:
            total_term_count = 0
            for term_index in self.inverted_index_data_dict:
                for temp_doc_id in self.inverted_index_data_dict[term_index]:
                    doc_dict = self.inverted_index_data_dict[term_index]
                    for term_count in doc_dict:
                        total_term_count += int(doc_dict.get(term_count))
                        self.add_to_doc_term_dict(doc_dict, temp_doc_id, term_count)
            total_no_of_documents = len(self.doc_term_freq_dict)
            self.average_doc_length = float(total_term_count) / float(total_no_of_documents)
        except Exception as e:
            print("Exception in compute_doc_average_length", e)
            print(traceback.format_exc())

    def add_to_doc_term_dict(self, doc_dict, temp_doc_id, term_count):
        if temp_doc_id in self.doc_term_freq_dict:
            self.doc_term_freq_dict[temp_doc_id].append(doc_dict.get(term_count))
        else:
            self.doc_term_freq_dict[temp_doc_id] = [doc_dict.get(term_count)]

    def compute_rank(self):
        self.compute_doc_average_length()
        for i in range(1, len(self.queries_list) + 1):
            self.compute_doc_score(i, self.queries_list[i - 1])

    def compute_doc_score(self, query_id, query):
        print('----------------- Computing Rank for Query %s -----------------' % query_id)
        doc_tf_score = {}
        try:
            for term_index in query.split():
                if term_index in self.inverted_index_data_dict:
                    doc_dict = self.inverted_index_data_dict[term_index]
                    word_to_doc_id_n_freq = doc_dict
                    n = len(word_to_doc_id_n_freq)
                    for doc_id, term_freq in word_to_doc_id_n_freq.items():
                        doc_length = 0
                        for term_count in self.doc_term_freq_dict[doc_id]:
                            doc_length += term_count
                        bm25_score = self.bm25_score_calculator(n, doc_length, term_freq)
                        if doc_id not in doc_tf_score:
                            doc_tf_score[doc_id] = bm25_score
                        else:
                            doc_tf_score[doc_id] += bm25_score
            self.write_doc_score_to_file(query_id, doc_tf_score)
        except Exception as e:
            print("Exception in compute_doc_score", e)
            print(traceback.format_exc())
        return doc_tf_score

    def write_doc_score_to_file(self, query_id, doc_to_score):
        queries_results_file_name = self.results_folder + 'query_{}_rank_list.txt'.format(query_id)
        query_report_file = open(queries_results_file_name, 'w+')
        sorted_result_list = sorted(doc_to_score.items(), key=lambda kv: kv[1], reverse=True)

        for i in range(len(sorted_result_list[:NO_OF_SEARCH_RESULTS])):
            search_result = sorted_result_list[i]
            query_report_file.write(
                str(query_id) + " " + 'Q0' + " " + str(search_result[0]) + " " + str(i + 1) + " " + str(
                    search_result[1]) + " " + "BM25_IR_MODEL \n")

        query_report_file.close()
