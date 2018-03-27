#!/usr/bin/env python3
"""
Tree output of ncbi taxonomy

ncbi - ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
"""
import argparse
import io
import logging
import os
import pkg_resources
import urllib.request
import sys
import tarfile

NCBI = 'ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz'


class Node:
    def __init__(self, tax_id):
        self.tax_id = tax_id
        self.children = []

    def __repr__(self):
        return '{} "{}" [{}]'.format(self.tax_id, self.name, self.rank)

    def add_child(self, child):
        self.children.append(child)

    def write_tree(self, outfile, level, print_char='|___'):
        if level == 0:
            return

        outfile.write(print_char + str(self) + '\n')
        for c in self.children:
            c.write_tree(outfile, level-1, print_char='| ' + print_char)

    def set_name(self, name):
        self.name = name

    def set_rank(self, rank):
        self.rank = rank


def add_arguments(parser):
    parser.add_argument(
        'taxdmp',
        nargs='?',
        metavar='tar.gz',
        help='ncbi taxdmp.tar.gz')

    parser.add_argument(
        '-V', '--version',
        action='version',
        version=pkg_resources.get_distribution('taxmagick').version,
        help='Print the version number and exit.')

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
    log_parser.add_argument(
        '-q', '--quiet',
        action='store_const',
        dest='verbosity',
        const=0,
        help='Suppress output')

    parser.add_argument(
        '--name-class',
        default='scientific name',
        help='name class to use in tree [%(default)s]')
    parser.add_argument(
        '-L', '--level',
        metavar='',
        type=int,
        default=-1,
        help='max depth of the taxonomic tree')
    parser.add_argument(
        '--root',
        default='1',
        metavar='',
        help='root node id for output [%(default)s]')
    parser.add_argument(
        '--url',
        default=NCBI,
        help='[%(default)s]')
    parser.add_argument(
        '-o', '--out',
        metavar='',
        default=sys.stdout,
        type=argparse.FileType('w'),
        help='output tree')

    return parser


def build_tree(nodes, names, root):
    tree = {}

    for tax_id, parent_id, rank in nodes:
        if tax_id in tree:
            node = tree[tax_id]
        else:
            node = Node(tax_id)
            tree[tax_id] = node

        node.set_rank(rank)

        if tax_id == root:  # root has no parent
            continue

        if parent_id in tree:
            parent = tree[parent_id]
        else:
            parent = Node(parent_id)
            tree[parent_id] = parent

        parent.add_child(node)

    for tax_id, name in names:
        tree[tax_id].set_name(name)

    return tree[root]


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=__doc__)
    parser = add_arguments(parser)
    args = parser.parse_args(args)
    setup_logging(args)

    if args.taxdmp:
        tar = args.taxdmp
    else:
        logging.info('downloading ' + args.url)
        tar, headers = urllib.request.urlretrieve(
            args.url, os.path.basename(args.url))
        logging.debug(str(headers).strip())

    taxdmp = tarfile.open(name=tar, mode='r:gz')

    nodes = io.TextIOWrapper(taxdmp.extractfile('nodes.dmp'))
    nodes = (n.strip().replace('\t', '').split('|') for n in nodes)
    nodes = (n[:3] for n in nodes)  # tax_id,parent,rank

    names = io.TextIOWrapper(taxdmp.extractfile('names.dmp'))
    names = (n.strip().replace('\t', '').split('|') for n in names)
    names = (n for n in names if n[3] == args.name_class)
    names = (n[:2] for n in names)  # tax_id, name

    logging.info('building node tree')
    root = build_tree(nodes, names, args.root)
    root.write_tree(args.out, args.level)


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


if __name__ == '__main__':
    sys.exit(main())
