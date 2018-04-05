# Taxmagick

Taxmagick was started as a command line visualization tool for the NCBI taxonomy.
I have begun adding support for common taxonomic requirement files for classification
tools like my alignment based classifier and Mothur. In the future 

# Installation

Taxmagick is written using Python 3 and should be installed using Python 3 or pip3.

```
pip3 taxmagick
```

or download and install and install using

```
python3 setup.py install
```

# Documentation

There are two commands in this package.  The first command is the `taxtree`
command that generates a text based taxonomic tree.  A user can choose
individual tax ids to visualize along with a top level root node.  If 
no root node is defined the ncbi top level root node is used.  If a 
subset of tax ids is not defined then the entire taxonomic tree is
output.  If no taxdmp.tar.gz file is specified then it will be downloaded automatically
and saved in the current directory.

An example using a couple Escherichia coli tax ids the output looks like
this

```
taxtree --root 131567 --ids 866789,481805 taxdump.tar.gz

|--- 131567 "cellular organisms" [no rank]
|    |--- 2 "Bacteria" [superkingdom]
|    |    |--- 1224 "Proteobacteria" [phylum]
|    |    |    |--- 1236 "Gammaproteobacteria" [class]
|    |    |    |    |--- 91347 "Enterobacterales" [order]
|    |    |    |    |    |--- 543 "Enterobacteriaceae" [family]
|    |    |    |    |    |    |--- 561 "Escherichia" [genus]
|    |    |    |    |    |    |    |--- 562 "Escherichia coli" [species]
|    |    |    |    |    |    |    |    |--- 498388 "Escherichia coli C" [no rank]
|    |    |    |    |    |    |    |    |    |--- 481805 "Escherichia coli ATCC 8739" [no rank]
|    |    |    |    |    |    |    |    |--- 866789 "Escherichia coli DSM 30083 = JCM 1649 = ATCC 11775" [no rank]
```

The second command is the lineages command that generates either a tax id
based lineage file in csv form or a tax name based lineage csv file.  The rank
order used in the header is determined by traversing the NCBI taxonomic data.
