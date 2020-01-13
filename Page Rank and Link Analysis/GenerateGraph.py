import networkx as nx
import nltk
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin


def get_file_name(filename):
    """
    Returns the title of the page from the URL to be used for saving
    :param filename:
    :return: filename to be used for storing HTML text
    """
    filename = filename.split('\n')[0]
    filename = filename.replace('/', '')
    return filename


def generate_graphs(text_file, download_directory, results_file):
    """
    Generate graph of web links given in the text file
    :param text_file: BFS or focused
    """
    #
    G = nx.DiGraph()
    url_dictionary = {}
    j = 0

    # For the URLs present in the text file create a node each and add them to the dictionary
    with open(text_file) as f:
        for line in f:
            title = line.split('/wiki/')
            url = line.split('\n')[0]
            filename = title[1]
            filename = get_file_name(filename)
            url_dictionary[filename] = url
            G.add_node(filename)

    i = 0
    # Extract links from every URL and check if they are present in the URL dictionary
    nltk.download('punkt')
    for t in url_dictionary:
        print(str(i) + ' ' + t)
        directory = os.fsdecode(download_directory)
        filename = download_directory + '/' + t + '.txt'

        with open(filename, encoding="utf-8") as cachedata:
            html_data = cachedata.read()
            soup = BeautifulSoup(html_data)
            links = soup.find_all('a', href=True)

        for link in links:
            link = link.get('href', '')
            link = urljoin('https://en.wikipedia.org/', link)

            # If link is present in URL dictionary create an edge between two nodes
            if link in url_dictionary.values() and link != url_dictionary[t]:
                title = link.split('/wiki/')
                filename = title[1]
                filename = get_file_name(filename)
                G.add_edge(t, filename)

        i = i + 1

    for t in url_dictionary:
        with open(results_file + '.txt', 'a', encoding="utf-8") as filetowrite:
            filetowrite.writelines(t + ' ')

            for u, v, data in G.in_edges(t, data=True):
                filetowrite.write(u + ' ')
                G[u][v]['weight'] = 1 / len(G.edges(u))
            filetowrite.write('\n')

    indegrees = [val for (node, val) in G.in_degree()]
    outdegrees = [val for (node, val) in G.out_degree()]
    max_indegree = max(indegrees)
    max_outdegree = max(outdegrees)

    print('Maximum Indegree :', max(indegrees))
    print('Maximum Outdegree: ', max(outdegrees))

    with open(results_file + '_Indegree.txt', 'w+', encoding="utf-8") as filetowrite:
        for node, val in sorted(G.in_degree, key=lambda x: x[1], reverse=True):
            filetowrite.write(str(node) + ' ' + str(val) + '\n')
    with open(results_file + '_Outdegree.txt', 'w+', encoding="utf-8") as filetowrite:
        for node, val in sorted(G.out_degree, key=lambda x: x[1], reverse=True):
            filetowrite.write(str(node) + ' ' + str(val) + '\n')


BFS_DOWNLOAD = 'BFS_Downloads'
BFS_RESULTS = 'G1'

FOCUSED_DOWNLOAD = 'Focused_Download'
FOCUSED_RESULTS = 'G2'

# Generate Graph for BFS
# generate_graphs('BFS.txt', BFS_DOWNLOAD, BFS_RESULTS)

# Generate for focused
generate_graphs('Focused.txt', FOCUSED_DOWNLOAD, FOCUSED_RESULTS)
