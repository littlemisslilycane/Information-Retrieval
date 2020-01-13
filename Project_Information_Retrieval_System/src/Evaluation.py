from utils.Utility import *
from config import *
import operator
from prettytable import PrettyTable


def get_rel_documents():
    rel_doc_list = {}

    with io.open(RELEVANT_DOC_INFO, encoding="utf-8") as cache_data:
        line = cache_data.readline()
        while line.strip() != '':
            line = line.split(' ')
            query_id = 'query_' + line[0]
            document_id = line[2]
            if query_id in rel_doc_list.keys():
                rel_doc_list[query_id].append(document_id)
            else:
                rel_doc_list[query_id] = []
                rel_doc_list[query_id].append(document_id)
            line = cache_data.readline()
    return rel_doc_list


def get_doc_id(formatted_data):
    return formatted_data.split(' ')[2]


def get_top_100_documents(result, query_id):
    top_100_doc_list = []
    with io.open(result + query_id + "_rank_list.txt", encoding="utf-8") as cache_data:
        line = cache_data.readline().strip()
        while line != '':
            documentID = get_doc_id(line)
            top_100_doc_list.append(documentID)
            line = cache_data.readline().strip()
    return top_100_doc_list


def get_rel_non_rel_list(top100, rel_list):
    rel_non_rel_map = {}
    for document in top100:
        if not rel_list:
            rel_non_rel_map[document] = "NON-REL"
        else:
            if document in rel_list:
                rel_non_rel_map[document] = "REL"
            else:
                rel_non_rel_map[document] = "NON-REL"
    return rel_non_rel_map


def reciprocal_rank(rel_non_rel_list, top_100_rank_list):
    first_rel_index = 1.0
    rel_present = False
    for document in top_100_rank_list:
        if rel_non_rel_list[document] == "REL":
            rel_present = True
            break
        first_rel_index += 1.0
    if rel_present:
        reciprocalrank = 1.0 / first_rel_index
    else:
        reciprocalrank = 0.0
    return reciprocalrank


def main(result):
    # Get the list of queries
    queries = get_queries_map(PARSED_QUERIES_FILE)

    # Get the list of relevant documents for each query
    rel_doc_list = get_rel_documents()

    # total number of queries
    total_number_of_queries = queries.__len__()
    sum_precision = 0.0
    sum_reciprocal_rank = 0.0

    for query_id, query in sorted(queries.items(), key=operator.itemgetter(1), reverse=True):
        with io.open(BM25_EVALUATION + query_id + ".txt", "a+", encoding="utf-8") as write_output:
            write_output.write(unicode(query_id + ": " + query + "\n"))
            table = PrettyTable(["RANK", "REL/NONREL", "PRECISION", "RECALL"])
            result_docs = {}
            result_docs = get_top_100_documents(result, query_id)
            query_result_top_100 = result_docs

            rel_non_rel_map = {}
            if query_id not in rel_doc_list:
                rel_doc_list[query_id] = []
            rel_non_rel_map = get_rel_non_rel_list(query_result_top_100, rel_doc_list[query_id])

            no_of_rel_doc = rel_doc_list[query_id].__len__()

            reciprocalrank = reciprocal_rank(rel_non_rel_map, query_result_top_100)
            sum_reciprocal_rank += reciprocalrank

            # Find the number of relevant documents that the query has produced
            rel_count = 0.0
            current_precision_map = {}
            current_recall_map = {}
            relevance_precisions = []
            precision = 0.0
            rank = 1
            for doc_id in query_result_top_100:
                if rel_non_rel_map[doc_id] == "REL":
                    rel_count += 1.0
                current_precision = rel_count / rank
                current_precision_map[rank] = current_precision
                if no_of_rel_doc == 0:
                    current_recall = 0
                else:
                    current_recall = rel_count / no_of_rel_doc
                current_recall_map[rank] = current_recall

                if rel_non_rel_map[doc_id] == "REL":
                    relevance_precisions.append(current_precision)

                if relevance_precisions.__len__() != 0:
                    precision = sum(relevance_precisions) / len(relevance_precisions)

                table.add_row([rank, rel_non_rel_map[doc_id], current_precision_map[rank], current_recall_map[rank]])

                if rank == 5:
                    with io.open(BM25_EVALUATION + query_id + "_PK5.txt", "a+", encoding="utf-8") as write_output1:
                        write_output1.write(
                            unicode("P@K = 5: " + str(current_precision_map[rank]) + "\n"))
                if rank == 20:
                    with io.open(BM25_EVALUATION + query_id + "_PK20.txt", "a+", encoding="utf-8") as write_output1:
                        write_output1.write(
                            unicode("P@K = 20: " + str(current_precision_map[rank]) + "\n"))
                rank += 1
            write_output.write(unicode(str(table)))

        sum_precision += precision
    with io.open(BM25_EVALUATION + query_id + "_MAP_MRR.txt", "a+", encoding="utf-8") as write_output:
        write_output.write(unicode("MAP: " + str(float(sum_precision / total_number_of_queries)) + "\n"))
        write_output.write(unicode("MRR: " + str(float(sum_reciprocal_rank / total_number_of_queries)) + "\n"))
    print(float(sum_precision / total_number_of_queries))
    print(float(sum_reciprocal_rank / total_number_of_queries))





