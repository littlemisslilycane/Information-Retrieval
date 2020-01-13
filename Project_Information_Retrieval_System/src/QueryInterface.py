# -*- coding: utf-8 -*-
#
from spellcheckerlib.spellchecker import *
from utils.Utility import *


class QueryInterface:
    def __init__(self):
        self.inverted_index_file = None
        self.inverted_index_data_dict = None
        self.parsed_queries_list = None
        self.erroneous_queries_list = None

        self.unindexed_data_file = None
        self.unindexed_data = None
        self.dictionary_data_set = None

    def load_data_files(self):
        self.inverted_index_file = open(INVERTED_INDEX_FILE, "rb")
        self.inverted_index_data_dict = eval(self.inverted_index_file.read())
        self.parsed_queries_list = get_queries(PARSED_QUERIES_FILE)

        self.unindexed_data_file = open(UNINDEXED_TXT_FILE, "rb")
        self.unindexed_data = self.unindexed_data_file.read()

    def generate_noisy_queries(self):
        print('---------------------------- Generating Noisy Queries -------------------------------')
        query_terms_list = []
        for query_sentence in self.parsed_queries_list:
            query_terms_list.append(query_sentence.split())

        error_query_list = []

        random_function_list = [swap_vowels, get_word_variants]

        for query in query_terms_list:
            no_of_errors_to_generate = int(len(query) * QUERY_ERROR_RATE)
            query_index = dict(enumerate(query))

            sorted_queries_index = sorted(query_index.keys())[:no_of_errors_to_generate]

            for pos in sorted_queries_index:
                term = query_index[pos]
                # calls either swap_vowels or get_word_variants function
                query_index[pos] = random.choice(random_function_list)(term)

            new_query = ""
            for key in sorted(query_index):
                new_query += query_index[key] + " "

            error_query_list.append(new_query)

        self.write_queries_to_file(error_query_list, ERRONEOUS_QUERIES_FILE)

    def initialize_dictionary(self):
        self.dictionary_data_set = {'NO SUGGESTION': 1}
        self.updated_dictionary(self.unindexed_data)
        self.erroneous_queries_list = get_queries(ERRONEOUS_QUERIES_FILE)
        for term in self.inverted_index_data_dict:
            self.dictionary_data_set[term] = self.get_term_frequency_in_doc(term)

    def updated_dictionary(self, text):
        for word in sentence_to_words(text):
            if word in self.dictionary_data_set:
                self.dictionary_data_set[word] += 1
            else:
                self.dictionary_data_set[word] = 1

    def get_term_frequency_in_doc(self, query_term):
        doc_term_frequency = 0
        if query_term in self.inverted_index_data_dict:
            doc_dict = self.inverted_index_data_dict[query_term]
            for doc_id in doc_dict:
                doc_term_frequency += doc_dict[doc_id]

        return doc_term_frequency

    def compute_and_suggest_new_queries(self):
        print('---------------------------- Started computing Noisy Queries -------------------------------')
        self.initialize_dictionary()
        for query_id in range(1, len(self.erroneous_queries_list) + 1):
            print('----------------- Processing Noisy Query %s -----------------' % query_id)
            query_sentence = self.erroneous_queries_list[query_id - 1]
            corrected_query_list = self.process_each_query(query_sentence)
            if len(corrected_query_list) == 0:
                corrected_query_list.append(query_sentence)
            self.write_queries_to_file(corrected_query_list[:NO_OF_QUERY_SUGGESTIONS], SUGGESTED_QUERIES_FILE.format(query_id))

    def process_each_query(self, query_sentence):
        new_queries = []
        query_terms_list = query_sentence.split()

        for query_term in query_terms_list:
            if query_term not in self.inverted_index_data_dict:
                suggested_words = self.get_suggestion(query_term, set(self.dictionary_data_set))
                correct_words = {query_term: [(x, self.dictionary_data_set[x]) for x in suggested_words]}
                new_queries = self.get_new_queries(query_term, query_sentence, new_queries, correct_words)
        return new_queries

    def get_new_queries(self, query_term, query_sentence, old_queries, correct_values):
        suggested_words = []
        for key, value in correct_values.items():
            sorted_result_list = sorted(value, key=lambda kv: kv[1], reverse=True)
            for suggestion in sorted_result_list:
                suggested_words.append(suggestion[0])

        new_queries = []
        previous_suggested_term = None
        for suggested_term in suggested_words:
            if 'NO SUGGESTION' not in suggested_term:
                if old_queries is None or len(old_queries) == 0:
                    new_query = query_sentence.replace(query_term, suggested_term)
                    new_queries = [new_query]
                    old_queries = [new_query]
                    previous_suggested_term = suggested_term
                else:
                    for query in old_queries:
                        if previous_suggested_term is not None:
                            query_term = previous_suggested_term
                        new_query = query.replace(query_term, suggested_term)
                        new_queries.append(new_query)
            else:
                print('NO SUGGESTION for', query_term)
        return new_queries

    def get_suggestion(self, new_word, words_dic):
        new_word = new_word.lower()
        print('get_suggestion', new_word)
        return ({new_word} & words_dic or
                set(vowelswaps(new_word)) & words_dic or
                set(variants(new_word)) & words_dic or
                set(double_variants(new_word)) & words_dic or
                {"NO SUGGESTION"})

    def write_queries_to_file(self, new_queries, file_name):
        query_report_file = open(file_name, 'w')
        for i in range(len(new_queries)):
            query_report_file.write(str(i + 1) + " " + str(new_queries[i]) + "\n")
        query_report_file.close()
