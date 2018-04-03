#!/usr/bin/env python3
"""
Tree output of ncbi taxonomy

ncbi - ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
"""
import io
import logging
import os
import urllib.request
import sys
import tarfile

from . import Tree, get_parser, setup_logging

NCBI = 'ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz'


def add_arguments(parser):
    parser.add_argument(
        '-L', '--level',
        metavar='',
        type=int,
        default=-1,
        help='max depth of the taxonomic tree')
    return parser


def main(args=sys.argv[1:]):
    parser = add_arguments(get_parser())
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
    root = Tree(nodes, names)[args.root]

    if args.ids:
        logging.info('pruning')
        ids = set(i.strip() for i in args.ids.split(','))
        root.prune(ids)

    root.write_tree(args.out, args.level)


if __name__ == '__main__':
    sys.exit(main())
