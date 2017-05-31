import os
import networkx as nx
import matplotlib.pyplot as plt

lemma_freq = {}

GOOD_POS = ['A', 'S', 'V', 'ADV']


def read_texts():
    dirs = os.walk('05')    
    word_lists = []
    for dirr in dirs:
        files = dirr[2]
        for file in files:
            file_name  = dirr[0] + '/' + file
            print(file_name)
            f = open(file_name, 'r', encoding='utf-8')
            text = f.read()
            text = text.replace('{',' ').replace('}',' ').split()
            i = 1
            word_li = []
            for word in text:
                if i % 2 == 0:
                    w = word.split('=')
                    lemma = w[0]
                    if '?' not in lemma:
                        pos = w[1]
                    else:
                        pos = '??'
                    if pos in GOOD_POS:
                        word_li.append(lemma)
                        make_dic(lemma)
                i += 1
            word_lists.append(word_li)
    return word_lists


def make_dic(lemma):
    if lemma not in lemma_freq:
        lemma_freq[lemma] = 1
    else:
        lemma_freq[lemma] += 1


def make_graph():
    word_lists = read_texts()
    g = nx.Graph()
    for text in word_lists:
        i = 0
        len_t = len(text) - 1
        for word in text:
            if i < len_t:
                g.add_edge(word, text[i+1])
            if i < len_t - 1:
                g.add_edge(word, text[i+2])
            i += 1
    print('радиус - ' + str(nx.radius(g)))
    print('диаметр - ' + str(nx.diameter(g)))
    print('кол-во узлов - ' + str(g.number_of_nodes()))
    print('кол-во ребер - ' + str(g.number_of_edges()))
    print('плотность - ' + str(nx.density(g)))
    deg = nx.degree_centrality(g)
    nodes = []
    for node in sorted(deg, key=deg.get, reverse=True):
        nodes.append(node)
    sub_g = g.subgraph(nodes[:25])
    save_graph(sub_g, 'graph_25.png')
    save_graph(g, 'graph_all.png')


def save_graph(g, name):
    pos = nx.random_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color='blue', node_size=7)
    nx.draw_networkx_edges(g, pos, edge_color='yellow')
    nx.draw_networkx_labels(g, pos, font_size=7)
    plt.axis('off')
    plt.savefig(name)

if __name__ == '__main__':
    make_graph()  
