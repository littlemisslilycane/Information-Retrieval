import networkx as nx
import numpy as np
from fractions import Fraction
from numpy.linalg import norm
from scipy.sparse import csc_matrix
import operator


def page_rank(graph_file, lambda_value):
    G = nx.DiGraph()
    node_count = 1
    # Create initial nodes
    with open(graph_file + '.txt') as f:
        for line in f:
            G.node(line[0])
    with open(graph_file + '.txt') as f:
        for line in f:
            print(node_count)
            incoming_nodes = line.split(' ')
            current_node = incoming_nodes[0]
            i = 1
            while i < (incoming_nodes.__len__() - 1):
                G.add_edge(incoming_nodes[i], current_node)
                i = i + 1
            node_count = node_count + 1
    for item in G.nodes:
        for u, v, data in G.in_edges(item, data=True):
            G[u][v]['weight'] = 1 / len(G.edges(u))

    adj_matrix = nx.adjacency_matrix(G)
    print(adj_matrix.todense())

    lam_by_n = Fraction(lambda_value / G.__len__())
    probability_initial = Fraction(1 / G.__len__())
    probability_value = lam_by_n + ((1 - lambda_value) * probability_initial)

    I = np.zeros((1, G.__len__()))
    I[:] = probability_value
    R = I
    sum = 0
    loopcounter = 0
    l2_norm_list = []

    while True:

        R = lam_by_n + ((1 - lambda_value) * I.dot(nx.to_numpy_matrix(G)))
        l2_norm_value = norm(np.subtract(R, I))

        l2_norm_list.append(l2_norm_value)
        sum = np.sum(I)
        print('Sum', sum)
        I = R

        if l2_norm_value < 0.0005:
            loopcounter = loopcounter + 1

        if loopcounter == 4:
            break

    print(loopcounter)
    print('Printing Final Rank')
    print(np.matrix(R))
    page_rank_list = np.array(R)[0]
    for item in page_rank_list:
        print(item)
    print(G.__len__())
    print(len(page_rank_list))

    page_rank_dictionary = {}
    j = 0
    for item in G.nodes:
        page_rank_dictionary[item] = page_rank_list[j]
        j = j + 1

    with open('PageRank_' + graph_file + '.txt', 'w+', encoding="utf-8") as f:
        for key, value in sorted(page_rank_dictionary.items(), key=operator.itemgetter(1), reverse=True):
            f.write(str(key) + ' ' + str(value) + '\n')

    with open(graph_file + '_L2_Norm.txt', 'w+', encoding="utf-8") as f:
        for item in l2_norm_list:
            f.write(str(item) + '\n')


# Genrating page rank for Graph G1
page_rank('G1', 0.15)

# Generating page rank for Graph G2
page_rank('G2', 0.15)
