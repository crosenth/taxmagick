#!/usr/bin/env python3
"""
lineages file

ncbi - ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
"""
import csv
import io
import logging
import os
import urllib.request
import sys
import tarfile

from . import Tree, get_parser, setup_logging


def add_arguments(parser):
    parser.add_argument(
        '--no-rank',
        action='store_true',
        help='include "no rank" nodes [False]')

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

    logging.info('building node tree')
    tree = Tree(nodes)

    logging.info('calculating ranks')
    rank_order = tree.root.rank_order()

    # reset root node for output
    root = tree[args.root]

    if args.ids:
        ids = set(i for i in args.ids.split(','))
        root.prune(keep=ids)

    ranks = root.ranks()
    output_ranks = [r for r in rank_order if r in ranks]
    out = csv.DictWriter(args.out, fieldnames=['tax_id'] + output_ranks)
    out.writeheader()
    root.write_lineage(out)


if __name__ == '__main__':
    sys.exit(main())
