from math import log

from utils.Utility import *


class QueryLMJMSRetrievalModel:
    def __init__(self):
        self.results_folder = QUERY_LM_JM_RESULTS_FOLDER
        self.inverted_index_file = None
        self.inverted_index_data_dict = None
        self.doc_terms_count_file = None
        self.doc_terms_count_dict = None
        self.queries_list = None
        self.qlm_scores = {}
        self.q_lambda = 0.7
        self.corpus_len = 0

    def load_data_files(self):
        self.inverted_index_file = open(INVERTED_INDEX_FILE, "rb")
        self.inverted_index_data_dict = eval(self.inverted_index_file.read())
        self.doc_terms_count_file = open(DOC_TERMS_COUNT_FILE, "rb")
        self.doc_terms_count_dict = eval(self.doc_terms_count_file.read())
        self.queries_list = get_queries(PARSED_QUERIES_FILE)
        self.corpus_len = sum(self.doc_terms_count_dict.values())

    def compute_ql_score(self, tf, ctf, D_doc_length, C_total_doc_length):
        a = (1 - self.q_lambda) * (tf / D_doc_length)
        b = self.q_lambda * (ctf / C_total_doc_length)
        score = log(1 + (a + b))
        return score

    def compute_rank(self):
        for query_id in range(1, len(self.queries_list) + 1):
            qlm_score_list = self.calculate_score(query_id, self.queries_list[query_id - 1])
            self.write_doc_score_to_file(query_id, qlm_score_list)

    def calculate_score(self, query_id, query_sentence):
        print('----------------- Computing QLM Score for Query %s -----------------' % query_id)
        qlm_score_list = {}

        for term in query_sentence.split():
            if term in self.inverted_index_data_dict:
                for doc_id in self.inverted_index_data_dict[term]:
                    temp_doc_dict = self.inverted_index_data_dict[term]
                    doc_term_frequency = self.get_term_frequency_in_doc(term)
                    if doc_id not in qlm_score_list:
                        qlm_score_list[doc_id] = self.compute_ql_score(temp_doc_dict[doc_id], doc_term_frequency,self.doc_terms_count_dict[doc_id], self.corpus_len)
                    else:
                        qlm_score_list[doc_id] += self.compute_ql_score(temp_doc_dict[doc_id], doc_term_frequency,self.doc_terms_count_dict[doc_id], self.corpus_len)
                        doc_term_frequency,self.doc_terms_count_dict[doc_id]

        return qlm_score_list

    def get_term_frequency_in_doc(self, query_term):
        doc_term_frequency = 0.0
        if query_term in self.inverted_index_data_dict:
            doc_dict = self.inverted_index_data_dict[query_term]
            for items in doc_dict:
                doc_term_frequency += doc_dict[items]
        return doc_term_frequency

    def write_doc_score_to_file(self, query_id, doc_to_score):
        queries_results_file_name = self.results_folder + 'query_{}_rank_list.txt'.format(query_id)
        query_report_file = open(queries_results_file_name, 'w+')
        sorted_result_list = sorted(doc_to_score.items(), key=lambda kv: kv[1], reverse=True)
        for i in range(len(sorted_result_list[:NO_OF_SEARCH_RESULTS])):
            search_result = sorted_result_list[i]
            query_report_file.write(str(query_id) + " " + 'Q0' + " " + str(search_result[0]) + " " + str(i + 1) + " " + str(search_result[1]) + " " + "QUERY_LM_JM_SMOOTHED_IR_MODEL \n")
        query_report_file.close()
