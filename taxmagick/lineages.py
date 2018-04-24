#!/usr/bin/env python3
"""
Lineages file

ncbi - ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
"""
import csv
import logging
import sys

from . import Tree, get_parser, setup_logging, get_data


def add_arguments(parser):
    lineage_parser = parser.add_argument_group(title='lineage options')
    lineage_parser.add_argument(
        '--names',
        action='store_true',
        help='include taxonomic names')
    return parser


def main(args=sys.argv[1:]):
    parser = add_arguments(get_parser())
    args = parser.parse_args(args)
    setup_logging(args)
    nodes, names = get_data(args.taxdmp, args.url, args.name_class)
    logging.info('building node tree')
    tree = Tree(nodes, names if args.names else None)
    if args.no_rank_suffix is not None:
        logging.info('expanding "no rank"')
        tree.expand_ranks(args.no_rank_suffix)
    root = tree[args.root]  # reset root node for output
    if args.ids:
        logging.info('pruning')
        ids = set(i for i in args.ids.split(','))
        root.prune(keep=ids)
    ranks = root.ranks()
    output_ranks = [r for r in tree.ranks if r in ranks]
    out = csv.DictWriter(args.out, fieldnames=['tax_id'] + output_ranks)
    out.writeheader()
    logging.info('writing lineage')
    root.write_lineage(out)


if __name__ == '__main__':
    sys.exit(main())
