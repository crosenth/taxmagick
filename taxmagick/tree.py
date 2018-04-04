#!/usr/bin/env python3
"""
Tree output of ncbi taxonomy

ncbi - ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
"""
import logging
import sys

from . import Tree, get_parser, setup_logging, get_data

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
    logging.info('building node tree')
    nodes, names = get_data(args.taxdmp, args.url, args.name_class)
    root = Tree(nodes, names)[args.root]
    if args.ids:
        logging.info('pruning')
        ids = set(i.strip() for i in args.ids.split(','))
        root.prune(ids)
    root.write_tree(args.out, args.level)


if __name__ == '__main__':
    sys.exit(main())
