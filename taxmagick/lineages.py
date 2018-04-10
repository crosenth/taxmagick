#!/usr/bin/env python3
"""
lineages file

ncbi - ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
"""
import csv
import logging
import sys

from . import Tree, get_parser, setup_logging, get_data


def add_arguments(parser):
    # TODO: create no_rank=yes output
    lineage_parser = parser.add_argument_group(title='lineage options')
    lineage_parser.add_argument(
        '--names',
        action='store_true',
        help='include taxonomic names')
    lineage_parser.add_argument(
        '--no-rank-suffix',
        help='apply parent rank with suffix to "no rank" nodes')
    return parser


def main(args=sys.argv[1:]):
    parser = add_arguments(get_parser())
    args = parser.parse_args(args)
    setup_logging(args)
    nodes, names = get_data(args.taxdmp, args.url, args.name_class)
    logging.info('building node tree')
    tree = Tree(nodes, names if args.names else None)
    logging.info('calculating ranks')
    rank_order = tree.root.rank_order(args.no_rank_suffix)
    root = tree[args.root]  # reset root node for output
    if args.ids:
        logging.info('pruning')
        ids = set(i for i in args.ids.split(','))
        root.prune(keep=ids)
    ranks = root.ranks()
    output_ranks = [r for r in rank_order if r in ranks]
    out = csv.DictWriter(args.out, fieldnames=['tax_id'] + output_ranks)
    out.writeheader()
    root.write_lineage(out)


if __name__ == '__main__':
    sys.exit(main())
