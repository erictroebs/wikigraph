#!/usr/bin/env python
import logging
from functools import reduce

from wikigraph.cli.ArgumentParser import ArgumentParser
from wikigraph.graph.GraphBuilder import GraphBuilder
from wikigraph.graph.GraphDrawer import GraphDrawer
from wikigraph.wikipedia.Article import Article

# parse command line arguments
args = ArgumentParser()

url = args.add_slot_parameter(
    'url',
    'Wikipedia article',
    example='https://en.wikipedia.org/wiki/Elon_Musk'
)

verbose = args.add_named_parameter(
    ['v', 'verbose'],
    'set log level to info'
)
D = args.add_named_parameter(
    ['D', 'maximum-depth'],
    'maximum distance from start article',
    expects='number',
    default=10,
    parse=int
)
K = args.add_named_parameter(
    ['K', 'maximum-nodes'],
    'maximum nodes in graph',
    expects='number',
    default=500,
    parse=int
)
R = args.add_named_parameter(
    ['R', 'maximum-references'],
    'maximum references used per article',
    expects='number',
    parse=int
)
exclude = args.add_named_parameter(
    ['e', 'exclude'],
    'exclude article from result graph',
    expects='identifier'
)
png = args.add_named_parameter(
    'png',
    'save graph to given png file',
    expects='path'
)
pdf = args.add_named_parameter(
    'pdf',
    'save graph to given pdf file',
    expects='path'
)
highlight = args.add_named_parameter(
    ['h', 'highlight'],
    'highlight articles containing a given phrase',
    expects='keyword'
)
cache_directory = args.add_named_parameter(
    'cache',
    'directory to store downloaded HTML files in',
    expects='directory'
)
graph_properties = args.add_named_parameter(
    ['p', 'properties'],
    'print graph properties to stdout'
)
adjacency_matrix = args.add_named_parameter(
    ['m', 'matrix'],
    'print adjacency matrix to stdout'
)

args.parse()

# set logging
if verbose.value:
    logging.getLogger().setLevel(logging.INFO)

# create start article
article = Article.from_url(url.value, cache_directory=cache_directory.value)

# build graph
gp = GraphBuilder(K.value, D.value, maximum_references=R.value, exclude=exclude.value)
with gp:
    graph = gp.build_from(article)

# print some stats
if graph_properties.value:
    mindeg = graph.minimum_degree_node()
    print(f'minimum degree: {mindeg.degree} / article: {mindeg.article.unescaped_identifier}')

    maxdeg = graph.maximum_degree_node()
    print(f'maximum degree: {maxdeg.degree} / article: {maxdeg.article.unescaped_identifier}')

    print(f'density: {graph.density()}')

# print graph adjacency table
if adjacency_matrix.value:
    matrix = graph.adjacency()
    labels = graph.labels()
    label_length = list(map(lambda x: len(x) + 1, labels))
    max_label_length = reduce(max, label_length, 0)

    print(' '.ljust(max_label_length), end='')
    print(' | '.join(labels))

    for i in range(len(labels)):
        print(labels[i].ljust(max_label_length), end='')
        for k in range(len(labels)):
            print(str(matrix[i][k]).ljust(label_length[k] + 2), end='')
        print()

# draw graph
if png.value is not None:
    if not png.value.endswith('.png'):
        png.value += '.png'

    gd = GraphDrawer(graph, highlight=highlight.value)
    gd.save_to(png.value)

if pdf.value is not None:
    if not pdf.value.endswith('.pdf'):
        pdf.value += '.pdf'

    gd = GraphDrawer(graph, highlight=highlight.value)
    gd.save_to(pdf.value)
