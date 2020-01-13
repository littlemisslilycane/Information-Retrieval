import os
import math
import nltk
import operator
from nltk.util import ngrams
import collections

CORPUS = 'BFS_PARSED'
term_frequency = {}
positional_index = {}


# Task 1a, 1b and 1c
def get_index(n):
    """
    Generate inverted index for n grams and number of terms in each document.
    :param n: n gram value
    """
    print('Generating ' + str(n) + " grams")
    inverted_index = {}

    for file in [f for f in os.listdir(CORPUS) if f.endswith('.txt')]:
        term_count = 0
        docID = os.fsdecode(file).split('.txt')[0]
        print('Parsing ' + docID)
        filename = CORPUS + '/' + docID + '.txt'
        with open(filename, encoding="utf-8") as cachedata:
            f = cachedata.read()
            f = f.strip()
            n_grams = ngrams((f.split(" ")), n)
            for n_gram in n_grams:
                term = (' '.join(n_gram))
                term_count += 1
                if term not in inverted_index:
                    inverted_index[term] = {docID: 1}
                elif docID not in inverted_index[term]:
                    inverted_index[term].update({docID: 1})
                else:
                    inverted_index[term][docID] += 1
    return inverted_index


def number_of_terms_in_document():
    """
    Generate the list of documents and the number of terms in each of them.
    """
    print('Number of terms per document generating')
    number_of_terms_in_document = {}

    for file in [f for f in os.listdir(CORPUS) if f.endswith('.txt')]:
        term_count = 0
        docID = os.fsdecode(file).split('.txt')[0]
        print('Parsing ' + docID)
        filename = CORPUS + '/' + docID + '.txt'
        with open(filename, encoding="utf-8") as cachedata:
            f = cachedata.read()
            f = f.strip()
            n_grams = ngrams((f.split(" ")), 1)
            for n_gram in n_grams:
                term_count += 1
        number_of_terms_in_document[docID] = term_count
    with open('Number_of_terms_in_document.txt', 'w+', encoding="utf-8") as filetowrite:
        for key, value in sorted(number_of_terms_in_document.items(), key=operator.itemgetter(1), reverse=True):
            filetowrite.write(key + ":" + str(value) + "\n")

    print('Number of terms per document generated.')


def generate_inverted_index(n):
    inverted_index = get_index(n)
    # Write the inverted index to the file
    with open('Inverted_Index_' + str(n) + '_gram.txt', 'w+', encoding="utf-8") as filetowrite:
        for index in inverted_index:
            filetowrite.write(index + "->" + str(inverted_index[index]) + "\n")

    print('nGram inverted index completed.')


# Task 1d - Generate positional index for unigram
def positional_inverted_index():
    print('Positional index generation started completed')
    # Iterate through each file in the directory
    for file in [f for f in os.listdir(CORPUS) if f.endswith('.txt')]:
        term_count = 0
        docID = os.fsdecode(file).split('.txt')[0]
        print(docID)
        filename = CORPUS + '/' + docID + '.txt'
        with open(filename, encoding="utf-8") as cachedata:
            f = cachedata.read()
            for term in f.split():
                term_count += 1
                if term not in positional_index:
                    positional_index[term] = {docID: [term_count]}
                elif docID not in positional_index[term]:
                    positional_index[term].update({docID: [term_count]})
                else:
                    positional_index[term][docID].append(
                        term_count - positional_index[term][docID][-1])

    # Write the inverted index to the file
    with open('Positional_Index.txt', 'w+', encoding="utf-8") as filetowrite:
        for index in positional_index:
            filetowrite.write(index + ":" + str(positional_index[index]) + "\n")
    print('Positional index completed')


# Task 2a and 2b
def conjunctive_processing(term1, term2, k):
    """
    Retrieved a list of documents that contain the pair of terms within the proximity window k.
    :param term1: term1
    :param term2: term 2
    :param k: proximity window
    :return: list of documents containing both the term within the proximity window.
    """
    result_docs = []

    # Get the list of documents for the pair of terms
    lst1 = positional_index[term1.lower()]
    lst2 = positional_index[term2.lower()]

    # Get the list of documents which have both space and exploration and iterate through them
    common_docs = set(lst1).intersection(lst2)
    for doc in common_docs:
        lst1[doc].sort()
        positions_1 = lst1[doc]
        lst2[doc].sort()
        positions_2 = lst2[doc]
        i = 0
        j = 0
        iLen = positions_1.__len__()
        jLen = positions_2.__len__()
        icurrentPosition = 0
        jCurrentPosition = 0
        while i < iLen and j < jLen:
            if abs((positions_1[i] + icurrentPosition) - (positions_2[j] + jCurrentPosition)) <= k:
                result_docs.append(doc)
                break
            else:
                if (positions_1[i] + icurrentPosition) < (positions_2[j] + jCurrentPosition):
                    icurrentPosition = positions_1[i] + icurrentPosition
                    i = i + 1

                else:
                    jcurrentPosition = positions_2[j] + jCurrentPosition
                    j = j + 1

    print('List of documents for ' + term1 + ' and ' + term2 + ' generated for the window ' + str(k))
    with open(term1 + '_' + term2 + '_' + str(k) + '.txt', 'w+', encoding="utf-8") as filetowrite:
        for doc in result_docs:
            filetowrite.write(doc + "\n")


# Task 3
def get_term_frequency(n):
    inverted_index = {}
    inverted_index = get_index(n)
    term_frequency = {}
    """
    Generates the list of term and term frequency across the corpus.

    """
    total_count = 0
    print('Generating Term Frequency list')
    for term in inverted_index:
        for doc in inverted_index[term]:
            total_count += inverted_index[term][doc]
        term_frequency[term] = total_count
        total_count = 0

    with open('Term_Frequency_' + str(n) + '.txt', 'w+', encoding="utf-8") as filetowrite:
        for key, value in sorted(term_frequency.items(), key=operator.itemgetter(1), reverse=True):
            filetowrite.write(str(key) + '->' + str(value) + '\n')
    print('Term Frequency list generation complete')


def get_doc_frequency_table(n):
    inverted_index = get_index(n)
    doc_frequency_table = {}
    o = []
    docIDList = ''
    total_count = 0
    inverted_sorted = collections.OrderedDict(sorted(inverted_index.items()))
    with open('Document_Frequency_' + str(n) + '.txt', 'w+', encoding="utf-8") as filetowrite:
        for term in inverted_sorted:
            for doc in inverted_sorted[term]:
                total_count += 1
                docIDList = docIDList + doc + ','
            filetowrite.write(term + "->[" + docIDList + "] " + str(total_count) + "\n")
            doc_frequency_table[term] = math.log10(996 / total_count)
            total_count = 0
            docIDList = ''

    sorted_idf = sorted(doc_frequency_table.items(), key=lambda kv: kv[1])

    with open('idf_' + str(n) + '.txt', 'w+', encoding="utf-8") as filetowrite:
        for key, value in sorted_idf:
            filetowrite.write(key + "->" + str(value) + "\n")

    with open('StopList_Trigram.txt', 'w+', encoding="utf-8") as filetowrite:
        for key, value in sorted_idf:
            if value <=  0.6519063639730601:
                filetowrite.write(key + "\n")


generate_inverted_index(1)
generate_inverted_index(2)
generate_inverted_index(3)
number_of_terms_in_document()
positional_inverted_index()
conjunctive_processing('space', 'mission', 6)
conjunctive_processing('space', 'mission', 12)
conjunctive_processing('earth', 'orbit', 5)
conjunctive_processing('earth', 'orbit', 10)
get_term_frequency(1)
get_term_frequency(2)
get_term_frequency(3)
get_doc_frequency_table(1)
get_doc_frequency_table(2)
get_doc_frequency_table(3)
