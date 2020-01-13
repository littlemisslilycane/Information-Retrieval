# -*- coding: utf-8 -*-
#
from BM25RetrievalModel import BM25RetrievalModel
from StemmedBM25RetrievalModel import StemmedBM25RetrievalModel
from InvertedIndexer import InvertedIndexer
from LuceneRetrievalModel import LuceneRetrievalModel
from StemmingLuceneRetrievalModel import StemmingLuceneRetrievalModel
from PesudoRelevanceFeedback import pseudo_relevance_feedback
from QueryInterface import QueryInterface
from QueryLMJMSRetrievalModel import QueryLMJMSRetrievalModel
from SnippetGeneration import display_results
from Stemming import query_time_stemming
from TFIDFRetrievalModel import TFIDFRetrievalModel
from utils.CACMParser import CACMParser
from utils.Utility import *


class CACMSearchEngine:
    def __init__(self):
        initialize_project()

    def parse_cacm(self):
        print('---------------------------- Started parsing cacm file -------------------------------')
        cacm_parser = CACMParser()
        cacm_parser.build_cacm_corpus()
        cacm_parser.parse_queries()

    def start_indexing_corpus(self):
        print('---------------------------- Started indexing corpus -------------------------------')
        inverted_indexer = InvertedIndexer()
        inverted_indexer.gen_inverted_index()

    def compute_bm25_ir(self):
        print('---------------------------- Started computing BM25 -------------------------------')
        bm25_retrieval_model = BM25RetrievalModel()
        bm25_retrieval_model.load_index_file()
        bm25_retrieval_model.compute_rank()

    def compute_lucene_ir(self):
        print('---------------------------- Started computing LUCENE -------------------------------')
        clean_lucene_index()  # cleaning up old index if any to avoid duplicate
        lucene_retrieval_model = LuceneRetrievalModel()
        lucene_retrieval_model.generate_corpus_index()
        lucene_retrieval_model.process_queries()

    def compute_lucene_for_stemmed(self):
        print('---------------------------- Started computing LUCENE for Stemmed -------------------------------')
        clean_lucene_index()  # cleaning up old index if any to avoid duplicate
        lucene_retrieval_model = StemmingLuceneRetrievalModel()
        lucene_retrieval_model.generate_corpus_index()
        lucene_retrieval_model.process_queries()

    def compute_tfidf_ir(self):
        print('---------------------------- Started computing TFIDF based IR -------------------------------')
        tfidf_retrieval_model = TFIDFRetrievalModel()
        tfidf_retrieval_model.load_data_files()
        tfidf_retrieval_model.compute_rank()

    def compute_query_lm_jms_ir(self):
        print(
            '---------------------------- Started computing Query Likelihood (JM Smoothed) based IR -------------------------------')
        query_lm_jms_retrieval_model = QueryLMJMSRetrievalModel()
        query_lm_jms_retrieval_model.load_data_files()
        query_lm_jms_retrieval_model.compute_rank()

    def query_expansion_stemming(self):
        print(
            '---------------------------- Start query expansion technique using query time stemming -------------------------------')
        query_time_stemming()

    def pseudo_relevance_feedbacks(self):
        print(
            '---------------------------- Start query expansion technique using pseudo_relevance_feedback ------------------------')
        pseudo_relevance_feedback()

    def generate_noisy_queries(self):
        print('---------------------------- Started Generating Noisy Queries -------------------------------')
        query_interface = QueryInterface()
        query_interface.load_data_files()
        query_interface.generate_noisy_queries()

    def compute_spell_check(self):
        print('---------------------------- Started computing Queries Spell Checker -------------------------------')
        query_interface = QueryInterface()
        query_interface.load_data_files()
        query_interface.compute_and_suggest_new_queries()

    def snippet(self):
        print('---------------------------- Phase_2 Snippet generation -------------------------------')
        display_results()

    def stopping(self):
        print('---------------------------- remove_stop_words_from_query -------------------------------')
        remove_stop_words_from_query(CACM_PARSED_QUERIES_FILE)

    def stemming(self):
        print('---------------------------- stemming -------------------------------')
        bm25_retrieval_model = StemmedBM25RetrievalModel()
        bm25_retrieval_model.load_index_file()
        bm25_retrieval_model.compute_rank()


if __name__ == '__main__':
    cacm_search = CACMSearchEngine()
    # cacm_search.parse_cacm()
    # cacm_search.start_indexing_corpus()
    # cacm_search.compute_tfidf_ir()
    # cacm_search.compute_query_lm_jms_ir()
    # cacm_search.compute_lucene_ir()
    # cacm_search.compute_bm25_ir()
    # cacm_search.query_expansion_stemming()
    # cacm_search.pseudo_relevance_feedbacks()
    # cacm_search.generate_noisy_queries()
    # cacm_search.compute_spell_check()
    # cacm_search.snippet()
    # cacm_search.stopping()
    # cacm_search.stemming()
    # cacm_search.compute_lucene_for_stemmed()
