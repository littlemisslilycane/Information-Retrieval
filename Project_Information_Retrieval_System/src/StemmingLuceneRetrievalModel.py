# -*- coding: utf-8 -*-
#
import glob
import ntpath
import os

from utils.Utility import *
import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, FieldType
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory

from config import CACM_CORPUS_FOLDER, CACM_CORPUS_LUCENE_INDEX_FOLDER, LUCENE_RESULTS_FOLDER, PARSED_QUERIES_FILE, \
    NO_OF_SEARCH_RESULTS


class StemmingLuceneRetrievalModel:

    def __init__(self):
        lucene.initVM()
        self.standard_analyzer = StandardAnalyzer()
        lucene_index_config = IndexWriterConfig(self.standard_analyzer)
        corpus_lucene_index_dir_path = Paths.get(CACM_CORPUS_LUCENE_INDEX_FOLDER)
        self.corpus_lucene_index_dir = SimpleFSDirectory(corpus_lucene_index_dir_path)
        self.lucene_index_writer = IndexWriter(self.corpus_lucene_index_dir, lucene_index_config)
        self.corpus_dir = STEMMED_CORPUS
        self.results_folder = LUCENE_RESULTS_FOLDER
        self.lucene_index_searcher = None

    def generate_corpus_index(self):
        print('-----------------Generating Corpus Lucene Index-----------------')
        corpus_files_list = glob.glob(os.path.join(self.corpus_dir, u'*.txt'))
        for corpus_file_path in corpus_files_list:
            corpus_file_name = ntpath.basename(corpus_file_path)
            corpus_file_name = os.path.splitext(corpus_file_name)[0]
            try:
                corpus_file = open(corpus_file_path)
                corpus_index_doc = self.add_corpus_file_to_index(corpus_file, corpus_file_name)
                self.lucene_index_writer.addDocument(corpus_index_doc)
            except Exception as indexEx:
                print("Error Indexing file:", indexEx, corpus_file_name)
        print('Total number of files indexed:', self.lucene_index_writer.numDocs())
        self.lucene_index_writer.close()

    @staticmethod
    def add_corpus_file_to_index(corpus_file, corpus_file_name):
        corpus_index_doc = Document()
        try:

            corpus_file_name_field = StringField("corpus_file_name", corpus_file_name, Field.Store.YES)

            content_field_type = FieldType()
            content_field_type.setTokenized(True)
            content_field_type.setStoreTermVectors(True)
            content_field_type.setStoreTermVectorOffsets(True)
            content_field_type.setStoreTermVectorPositions(True)
            content_field_type.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
            content_field_type.freeze()

            corpus_content_field = Field("corpus_content", corpus_file.read(), content_field_type)
            corpus_index_doc.add(corpus_file_name_field)
            corpus_index_doc.add(corpus_content_field)
            corpus_file.close()
        except Exception as ex:
            print("Error Adding file:", ex, corpus_file_name)
        return corpus_index_doc

    def compute_doc_score(self, query_term, no_of_results_to_fetch):
        lucene_query_parser = QueryParser("corpus_content", self.standard_analyzer)
        lucene_query = lucene_query_parser.parse(query_term)
        query_doc_score = self.lucene_index_searcher.search(lucene_query, no_of_results_to_fetch).scoreDocs
        return query_doc_score

    def process_queries(self):
        self.standard_analyzer = StandardAnalyzer()
        self.lucene_index_searcher = IndexSearcher(DirectoryReader.open(self.corpus_lucene_index_dir))
        print('-----------------Processing Queries-----------------')
        queries_doc = get_queries(STEM_QUERY_FILE)
        query_count = 1
        for query in queries_doc:
            try:
                query_id = query_count
                query_term = query[2:].replace("\n", "")
                print("Performing query search for:", query_id, query_term)

                query_doc_score = self.compute_doc_score(query_term, NO_OF_SEARCH_RESULTS)
                self.write_query_doc_score(query_doc_score, query_id)
                query_count += 1

            except Exception as e:
                print("Error query_doc:", e, query)

    def write_query_doc_score(self, query_doc_score, query_id):
        queries_results_file_name = self.results_folder + 'query_{}_rank_list.txt'.format(query_id)
        queried_results = open(queries_results_file_name, 'w+')

        for i in range(len(query_doc_score)):
            temp_doc = self.lucene_index_searcher.doc(query_doc_score[i].doc)
            queried_results.write(str(query_id) + " " + 'Q0' + " " + str(
                str(temp_doc.get("corpus_file_name").encode('utf-8')) + " " + str(i + 1) + " " + str(
                    query_doc_score[i].score) + " " + "LUCENE_IR_MODEL \n"))

        queried_results.close()
