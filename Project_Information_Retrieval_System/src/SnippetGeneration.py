from utils.Utility import *
import bs4
import re
import string
import operator
import nltk

K = 5

document_title = {}


def get_top_k_document(query_id):
    doc_list = []
    with io.open(BM25_RESULTS_FOLDER + query_id + "_rank_list.txt", encoding="utf-8") as cache_data:
        doc_id = cache_data.readline().strip()
        doc_count = 1
        while doc_id != '' and doc_count <= K:
            doc_list.append(doc_id)
            doc_id = cache_data.readline().strip()
            doc_count += 1
    return doc_list


def parse_text(raw_text):
    soup = bs4.BeautifulSoup(raw_text)
    parsed = soup.get_text()
    parsed = re.sub('\[[^]]*\]', '', parsed)
    remove = string.punctuation
    remove = remove.replace("-", "")  # don't remove hyphens and periods
    remove = remove.replace(".", "")
    parsed = re.sub("[" + re.escape(remove) + "]", "", parsed)
    AM_index = parsed.rfind("AM")
    PM_index = parsed.rfind("PM")
    index = max(AM_index, PM_index)
    parsed = parsed[0:index + 2]
    return parsed


def get_sentences(document):
    global document_title
    sentences = []
    document = document.split(' ')[2]
    with io.open(CACM_DOCS_FOLDER + document + ".html", encoding="utf-8") as cache_data:
        doc_text = cache_data.read()
        document_title[document] = doc_text.split('<pre>')[1].split('\n\n\n')[1].split('\n\n')[0]
        doc_text = parse_text(doc_text).lower()
        doc_text = doc_text.replace('\n', ' ')
        sentences = doc_text.split('.')

    return sentences


def get_significant_words(query):
    significant_words = []
    common_words = get_common_words()
    words = nltk.word_tokenize(query)
    for term in words:
        if term not in significant_words and term not in common_words:
            significant_words.append(term)
    return significant_words


def significance_factor(sentences, significant_words):
    score = {}
    for sentence in sentences:
        sentence = sentence.strip()
        window_start = 0
        window_end = 0
        index = 1
        significant_count = 0

        for term in sentence.split(' '):
            if term in significant_words:
                significant_count += 1
                if window_start == 0:
                    window_start = 1
                    window_end = 1
                else:
                    window_end = index
            if window_start == 1:
                index += 1
        number_of_words = window_end - window_start + 1
        if number_of_words != 0 and significant_count != 0:
            score[sentence] = (significant_count ** 2) / number_of_words
    return score


def get_html_format(sentence, query):
    significant_words = get_significant_words(query)
    html_text = ''
    for term in sentence[0].split(' '):
        if term in significant_words:
            html_text += '<b>' + term + '</b> '
        else:
            html_text += term + ' '
    return html_text + '.'


def display_snippets(query, query_id, document, significance_score):
    with io.open(SNIPPET_RESULTS + query_id + '_results.html', 'a+', encoding="utf-8") as filetowrite:
        html_text = ''
        doc_id = document.split(' ')[2]
        html_text += '<b><u>' + doc_id + '</u></b><br />'
        html_text += '<b>' + document_title[doc_id] + '</b><br />'
        sentence_limit = 1
        for sentence in sorted(significance_score.items(), key=operator.itemgetter(1), reverse=True):
            html_text += get_html_format(sentence, query)
            sentence_limit += 1
            if sentence_limit > 3:
                break
        filetowrite.write(unicode(html_text + '<br />'))


def snippet_generation(queries):
    # Get the top K documents for each query to generate snippets
    for query_id, query in queries.items():
        document_list = get_top_k_document(query_id)
        for document in document_list:
            significance_score = {}
            sentences = get_sentences(document)
            significant_words = get_significant_words(query)
            significance_score = significance_factor(sentences, significant_words)
            display_snippets(query, query_id, document, significance_score)


def display_results():
    queries = get_queries_map(PARSED_QUERIES_FILE)
    snippet_generation(queries)



