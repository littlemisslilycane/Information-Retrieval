from bs4 import BeautifulSoup
import urllib.request
import nltk
import os
import re
import string
import numpy as np
import matplotlib.pylab as pt
import operator


def get_file_name(filename):
    """
    Returns the title of the page from the URL to be used for saving
    :param filename:
    :return: filename to be used for storing HTML text
    """
    filename = filename.split('\n')[0]
    filename = filename.replace('/', '')
    return filename


def download_pages(download_to, text_file):
    """
    Downloads the articles for the URLs in BFS.txt
    :param download_to: Download Folder location
    :param text_file: Reference text file BFS.txt
    """
    with open(text_file) as f:
        for line in f:
            filename = line.split('/wiki/')[1]
            filename = get_file_name(filename)
            urllib.request.urlretrieve(line, download_to + '/' + filename + '.txt')


def tokenize(download_dir, case_folding, punctuation_handling, parsed_folder):
    """
    Parses and tokenizes the articles and generates a text file for it
    """
    nltk.download('punkt')
    directory = os.fsdecode(download_dir)
    words = ''
    for file in os.listdir(directory):
        docID = os.fsdecode(file)
        print(docID)
        filename = download_dir + '/' + docID
        with open(filename, encoding="utf-8") as cachedata:
            html_data = cachedata.read()

        soup = BeautifulSoup(html_data)
        content = ''

        # Parse text from the main content only
        for word in soup.find_all(['h3', 'p', 'h1']):
            content += word.text
        # Remove reference string like [1], [2], etc.
        content = re.sub('\[[^]]*\]', '', content)

        # Handle punctuation
        remove = string.punctuation
        remove = remove.replace("-", "")  # don't remove hyphens
        if punctuation_handling:
            content = re.sub("[" + re.escape(remove) + "]", "", content)

        # Store the parsed text in a text file
        parser_file = parsed_folder + '/' + docID
        tokens = nltk.word_tokenize(content)

        tokenized = ''
        for w in tokens:
            if w.isalnum() or w.__contains__('-'):  # Parses only alphanumeric
                if case_folding:  # Case folding
                    w = w.lower()
                tokenized += w.lower() + ' '

        # Write tokenized content to a new text file
        with open(parser_file, 'w', encoding="utf-8") as filetowrite:
            filetowrite.write(tokenized)


def generate_trigrams(parsed_dir):
    """
    Generates the trigrams for the corpus and plots frequency rank log log graph
    """

    directory = os.fsdecode(parsed_dir)
    words = ''
    trigrams = []

    # Dictionary to hold the trigrams and their frequencies
    trigram_dictionary = {}

    # Generate trigram for every article
    for file in os.listdir(directory):
        doc_id = os.fsdecode(file)
        print(doc_id)
        filename = parsed_dir + '/' + doc_id
        with open(filename, encoding="utf-8") as cachedata:
            content = cachedata.read()
            tokens = nltk.word_tokenize(content)

            for t in nltk.trigrams(tokens):
                if t in trigram_dictionary:
                    # If trigram is already present in the dictionary increase the frequency by 1
                    trigram_dictionary[t] += 1
                else:
                    trigram_dictionary[t] = 1

    ranks = np.array(np.arange(1, len(trigram_dictionary) + 1))
    y = sorted(trigram_dictionary.values(), reverse=True)
    y = np.array(y)

    # Print trigrams
    with open('Trigrams.txt', 'w+', encoding="utf-8") as f:
        for key, value in sorted(trigram_dictionary.items(), key=operator.itemgetter(1), reverse=True):
            f.write(str(key) + ' ' + str(value) + '\n')
    pt.loglog(ranks, y)
    pt.show()


CASE_FOLDING = True
PUNCTUATION_HANDLING = True
BFS_DOWNLOAD = 'BFS_Downloads'
BFS_PARSED = 'BFS_PARSED'
FOCUSED_DOWNLOAD = 'Focused_Download'

# Download the articles from BFS
# download_pages(BFS_DOWNLOAD, 'BFS.txt')

# Download articles for Focused
download_pages(FOCUSED_DOWNLOAD, 'Focused.txt')

# Parse and tokenize articles and generate them in text files
# tokenize(BFS_DOWNLOAD, CASE_FOLDING, PUNCTUATION_HANDLING, BFS_PARSED)

# Generate trigrams and plot frequency-rank graph
# generate_trigrams(BFS_PARSED)
