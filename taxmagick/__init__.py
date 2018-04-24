#!/usr/bin/env python3
"""
"""
import argparse
import io
import logging
import os
import pkg_resources
import tarfile
import urllib.request
import sys

NCBI = 'ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz'
ROOT = 'root'


class Node:
    def __init__(self, tax_id):
        self.tax_id = tax_id
        self.children = []
        self.name = ''

    def __rank_tree__(self, parent_rank, lineages={}):
        '''Creates a dictionary of sets with keys being ranks pointing
        to a set of parent ranks via tree traversal.
        '''
        if self.rank != 'no rank' and self.rank != parent_rank:
            if self.rank in lineages:
                lineages[self.rank].add(parent_rank)
            else:
                lineages[self.rank] = set()
            parent_rank = self.rank
        for c in self.children:
            c.__rank_tree__(parent_rank, lineages)
        return lineages

    def __repr__(self):
        return '{} "{}" [{}]'.format(self.tax_id, self.name, self.rank)

    def add_child(self, child):
        self.children.append(child)

    def expand_no_ranks(self, suffix, ranks, parent=ROOT):
        if self.rank == 'no rank':
            self.rank = parent + suffix
            if self.rank not in ranks:
                ranks.insert(ranks.index(parent) + 1, self.rank)
        for c in self.children:
            c.expand_no_ranks(suffix, ranks, self.rank)

    def prune(self, keep):
        cut = self.tax_id not in keep
        for c in list(self.children):
            if c.prune(keep):
                self.children.remove(c)
            else:
                cut = False
        return cut

    def ranks(self, ranks=set()):
        ranks.add(self.rank)
        for c in self.children:
            c.ranks(ranks)
        return ranks

    def write_lineage(self, outfile, lineage={}):
        '''Write csv file of taxonomic lineages

        Args:
            outfile (DictWriter): Output file
            lineage (dict): Dictionary of parent lineage

        Returns:
            None
        '''
        if self.rank in outfile.fieldnames:
            lineage.update({self.rank: self.name or self.tax_id})
            outfile.writerow({'tax_id': self.tax_id, **lineage})
        for c in self.children:
            c.write_lineage(outfile, lineage.copy())

    def write_tree(self, outfile, level, print_char='|--- '):
        if level != 0:
            outfile.write(print_char + str(self) + '\n')
            for c in self.children:
                c.write_tree(outfile, level-1, print_char='|    ' + print_char)


class Tree(dict):
    '''
    Builds and returns all the nodes as a dictionary object
    '''
    def __init__(self, nodes, names=None):
        for tax_id, parent_id, rank in nodes:
            if tax_id in self:
                node = self[tax_id]
            else:
                node = Node(tax_id)
                self[tax_id] = node

            node.rank = rank

            if tax_id == parent_id:  # top node, no parent
                self.root = node
                continue

            if parent_id in self:
                parent = self[parent_id]
            else:
                parent = Node(parent_id)
                self[parent_id] = parent

            parent.add_child(node)

        if names is not None:
            for tax_id, name in names:
                self[tax_id].name = name

        self.ranks = self.__ranks__()

    def __ranks__(self):
        '''
        Determines rank order
        '''
        lineages = self.root.__rank_tree__(self.root.rank)
        for l in lineages.values():
            l.discard(self.root.rank)
        ranks = []
        if self.root.rank != 'no rank':
            ranks.append(self.root.rank)
        while lineages:
            next_rank = sorted(lineages, key=lambda x: len(lineages[x]))[0]
            ranks.append(next_rank)
            del lineages[next_rank]
            for v in lineages.values():
                v.discard(next_rank)
        return ranks

    def expand_ranks(self, suffix):
        self.root.rank = ROOT
        self.ranks.insert(0, ROOT)
        self.root.expand_no_ranks(suffix, self.ranks)


def get_data(taxdmp, url, name_class):
    if taxdmp is not None:
        tar = taxdmp
    else:
        logging.info('downloading ' + url)
        tar, headers = urllib.request.urlretrieve(
            url, os.path.basename(url))
        logging.debug(str(headers).strip())
    taxdmp = tarfile.open(name=tar, mode='r:gz')
    nodes = io.TextIOWrapper(taxdmp.extractfile('nodes.dmp'))
    nodes = (n.strip().replace('\t', '').split('|') for n in nodes)
    nodes = (n[:3] for n in nodes)  # tax_id,parent,rank
    names = io.TextIOWrapper(taxdmp.extractfile('names.dmp'))
    names = (n.strip().replace('\t', '').split('|') for n in names)
    names = (n for n in names if n[3] == name_class)
    names = (n[:2] for n in names)  # tax_id,name
    return nodes, names


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'taxdmp',
        nargs='?',
        help='ncbi taxdmp.tar.gz')
    parser.add_argument(
        '--name-class',
        metavar='',
        default='scientific name',
        help='name class to use in tree [%(default)s]')
    parser.add_argument(
        '--url',
        metavar='',
        default=NCBI,
        help='[%(default)s]')
    parser.add_argument(
        '-V', '--version',
        action='version',
        version=pkg_resources.get_distribution('taxmagick').version,
        help='Print the version number and exit.')
    parser.add_argument(
        '--no-rank-suffix',
        help='apply parent rank with suffix to "no rank" nodes')
    log_parser = parser.add_argument_group(title='logging')
    log_parser.add_argument(
        '-l', '--log',
        metavar='FILE',
        type=argparse.FileType('a'),
        default=sys.stdout,
        help='Send logging to a file')
    log_parser.add_argument(
        '-v', '--verbose',
        action='count',
        dest='verbosity',
        default=0,
        help='Increase verbosity of screen output '
             '(eg, -v is verbose, -vv more so)')
    tree_parser = parser.add_argument_group(title='tree options')
    tree_parser.add_argument(
        '--ids',
        metavar='',
        help='prune tree around these tax ids')
    tree_parser.add_argument(
        '--root',
        default='1',
        metavar='',
        help='root node tax id for output [%(default)s]')
    parser.add_argument(
        '-o', '--out',
        metavar='',
        default=sys.stdout,
        type=argparse.FileType('w'),
        help='output tree')
    return parser


def setup_logging(namespace):
    loglevel = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }.get(namespace.verbosity, logging.DEBUG)
    if namespace.verbosity > 1:
        logformat = '%(levelname)s taxtree %(message)s'
    else:
        logformat = 'taxtree %(message)s'
    logging.basicConfig(stream=namespace.log, format=logformat, level=loglevel)
