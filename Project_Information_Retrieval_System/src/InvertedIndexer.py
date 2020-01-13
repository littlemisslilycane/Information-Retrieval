import glob
import ntpath
import os
import traceback

from config import *


class InvertedIndexer:

    def __init__(self):
        self.inverted_index = {}
        self.n_gram_name = ''
        self.corpus_folder_path = CACM_CORPUS_FOLDER
        self.n_gram = 1
        self.doc_terms_count = {}

    def gen_inverted_index(self):
        print('---------------------------- Generating Inverted Index ---------------------------------')
        try:
            corpus_files_list = glob.glob(os.path.join(self.corpus_folder_path, '*.txt'))

            for corpus_file_path in corpus_files_list:
                corpus_file_name = ntpath.basename(corpus_file_path)
                corpus_doc_id = os.path.splitext(corpus_file_name)[0]

                with open(corpus_file_path, 'r') as temp_corpus_file:
                    corpus_file = temp_corpus_file.read()
                    self.gen_data_structure(corpus_file, corpus_doc_id, self.n_gram)

                temp_corpus_file.close()
            self.write_doc_terms_count_file()
            self.generate_term_freq()
        except Exception as gen_inverted_index_ex:
            print("Error in gen_inverted_index function : ", gen_inverted_index_ex)
            print(traceback.format_exc())

    def gen_data_structure(self, corpus_file, corpus_file_name, n_gram):
        print("Creating index for " + str(corpus_file_name))
        try:
            word_list = corpus_file.split()
            self.doc_terms_count[corpus_file_name] = len(word_list)

            # create data structure for the inverted index
            for i in range(len(word_list) - (n_gram - 1)):
                words = word_list[i]

                if words is not None and " " not in words:
                    if words not in self.inverted_index:
                        corpus_dict = {corpus_file_name: 1}
                        self.inverted_index[words] = corpus_dict
                    elif corpus_file_name in self.inverted_index[words]:
                        corpus_dict = self.inverted_index[words]
                        value = corpus_dict.get(corpus_file_name)
                        value += 1
                        corpus_dict[corpus_file_name] = value
                    else:
                        corpus_dict = {corpus_file_name: 1}
                        self.inverted_index[words].update(corpus_dict)
        except Exception as gen_data_structure_ex:
            print("Error in gen_data_structure function ", gen_data_structure_ex)

    def generate_term_freq(self):
        print('-------------------------------- Generating Term Frequency -----------------------------------')
        try:
            corpus_doc_freq = {}
            doc_term_frequency = {}

            for term_index in self.inverted_index:
                term_count = 0
                corpus_dict = self.inverted_index[term_index]
                corpus_doc_freq[term_index] = {}
                doc_dict = {}

                for temp_doc_id in corpus_dict:
                    doc_id = temp_doc_id

                    if doc_id not in doc_dict:
                        doc_dict[doc_id] = 0

                    doc_dict[doc_id] += corpus_dict.get(temp_doc_id)
                    term_count = doc_dict[doc_id]

                corpus_doc_freq[term_index] = doc_dict
                doc_term_frequency[term_index] = term_count

            sorted_term_freq_table = sorted(doc_term_frequency.items(), key=lambda kv: kv[1], reverse=True)

            self.write_inverted_index_file(corpus_doc_freq, sorted_term_freq_table)

        except Exception as generate_term_freq_ex:
            print("Error in generate_term_freq function!", generate_term_freq_ex)

    @staticmethod
    def write_inverted_index_file(corpus_doc_freq, sorted_term_freq_table):
        print('---------------------------- Creating Term Doc Frequency Files-------------------------------')
        try:
            inverted_doc = {}

            for freq_table_val in sorted_term_freq_table:
                inverted_doc[freq_table_val[0]] = corpus_doc_freq[freq_table_val[0]]

            inverted_index_file = open(INVERTED_INDEX_FILE, "w")
            inverted_index_file.write(str(inverted_doc))
            inverted_index_file.close()

        except Exception as create_term_doc_freq_files_ex:
            print("Error in write_inverted_index_file function!", create_term_doc_freq_files_ex)

    def write_doc_terms_count_file(self):
        try:
            doc_terms_count_file = open(DOC_TERMS_COUNT_FILE, "w")
            doc_terms_count_file.write(str(self.doc_terms_count))
            doc_terms_count_file.close()

        except Exception as create_term_doc_freq_files_ex:
            print("Error in write_doc_terms_count_file function!", create_term_doc_freq_files_ex)
