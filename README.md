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
command that generates a text based taxonomic tree.  With both commands 
the user can choose individual tax ids to visualize along with a top level 
root node.  If the `--root` node is not specified then the ncbi top level root 
node (tax id 1) is used.  If a subset of tax ids is not defined then the entire 
taxonomic tree is output.  If no taxdmp.tar.gz file is specified then it will be 
downloaded automatically and saved in the current directory.

A taxtree example using Escherichia coli (tax id 562) and Amanita muscaria (41956) the 
output looks like this

```
taxtree --root 131567 --ids 562,41956 taxdump.tar.gz

|--- 131567 "cellular organisms" [no rank]
|    |--- 2 "Bacteria" [superkingdom]
|    |    |--- 1224 "Proteobacteria" [phylum]
|    |    |    |--- 1236 "Gammaproteobacteria" [class]
|    |    |    |    |--- 91347 "Enterobacterales" [order]
|    |    |    |    |    |--- 543 "Enterobacteriaceae" [family]
|    |    |    |    |    |    |--- 561 "Escherichia" [genus]
|    |    |    |    |    |    |    |--- 562 "Escherichia coli" [species]
|    |--- 2759 "Eukaryota" [superkingdom]
|    |    |--- 33154 "Opisthokonta" [no rank]
|    |    |    |--- 4751 "Fungi" [kingdom]
|    |    |    |    |--- 451864 "Dikarya" [subkingdom]
|    |    |    |    |    |--- 5204 "Basidiomycota" [phylum]
|    |    |    |    |    |    |--- 5302 "Agaricomycotina" [subphylum]
|    |    |    |    |    |    |    |--- 155619 "Agaricomycetes" [class]
|    |    |    |    |    |    |    |    |--- 452333 "Agaricomycetidae" [subclass]
|    |    |    |    |    |    |    |    |    |--- 5338 "Agaricales" [order]
|    |    |    |    |    |    |    |    |    |    |--- 41954 "Amanitaceae" [family]
|    |    |    |    |    |    |    |    |    |    |    |--- 41955 "Amanita" [genus]
|    |    |    |    |    |    |    |    |    |    |    |    |--- 41956 "Amanita muscaria" [species]
```

By default `--name-class "scientific name"` is used for taxonomic names.

The second `lineages` command generates either a tax id based lineage file in 
csv form or a tax name based lineage csv file.  The rank order used in the 
header is determined by traversing the NCBI taxonomic data.

```
lineages --root 131567 --ids 562,41956 taxdump.tar.gz

tax_id,superkingdom,kingdom,subkingdom,phylum,subphylum,class,subclass,order,family,genus,species
2,2,,,,,,,,,,
1224,2,,,1224,,,,,,,
1236,2,,,1224,,1236,,,,,
91347,2,,,1224,,1236,,91347,,,
543,2,,,1224,,1236,,91347,543,,
561,2,,,1224,,1236,,91347,543,561,
562,2,,,1224,,1236,,91347,543,561,562
2759,2759,,,,,,,,,,
4751,2759,4751,,,,,,,,,
451864,2759,4751,451864,,,,,,,,
5204,2759,4751,451864,5204,,,,,,,
5302,2759,4751,451864,5204,5302,,,,,,
155619,2759,4751,451864,5204,5302,155619,,,,,
452333,2759,4751,451864,5204,5302,155619,452333,,,,
5338,2759,4751,451864,5204,5302,155619,452333,5338,,,
41954,2759,4751,451864,5204,5302,155619,452333,5338,41954,,
41955,2759,4751,451864,5204,5302,155619,452333,5338,41954,41955,
41956,2759,4751,451864,5204,5302,155619,452333,5338,41954,41955,41956
```
And if `--names` is specified then the `--name-class` will be used instead of tax id.

```
lineages --root 131567 --ids 562,41956 taxdump.tar.gz

d,superkingdom,kingdom,subkingdom,phylum,subphylum,class,subclass,order,family,genus,species
2,Bacteria,,,,,,,,,,
1224,Bacteria,,,Proteobacteria,,,,,,,
1236,Bacteria,,,Proteobacteria,,Gammaproteobacteria,,,,,
91347,Bacteria,,,Proteobacteria,,Gammaproteobacteria,,Enterobacterales,,,
543,Bacteria,,,Proteobacteria,,Gammaproteobacteria,,Enterobacterales,Enterobacteriaceae,,
561,Bacteria,,,Proteobacteria,,Gammaproteobacteria,,Enterobacterales,Enterobacteriaceae,Escherichia,
562,Bacteria,,,Proteobacteria,,Gammaproteobacteria,,Enterobacterales,Enterobacteriaceae,Escherichia,Escherichia coli
2759,Eukaryota,,,,,,,,,,
4751,Eukaryota,Fungi,,,,,,,,,
451864,Eukaryota,Fungi,Dikarya,,,,,,,,
5204,Eukaryota,Fungi,Dikarya,Basidiomycota,,,,,,,
5302,Eukaryota,Fungi,Dikarya,Basidiomycota,Agaricomycotina,,,,,,
155619,Eukaryota,Fungi,Dikarya,Basidiomycota,Agaricomycotina,Agaricomycetes,,,,,
452333,Eukaryota,Fungi,Dikarya,Basidiomycota,Agaricomycotina,Agaricomycetes,Agaricomycetidae,,,,
5338,Eukaryota,Fungi,Dikarya,Basidiomycota,Agaricomycotina,Agaricomycetes,Agaricomycetidae,Agaricales,,,
41954,Eukaryota,Fungi,Dikarya,Basidiomycota,Agaricomycotina,Agaricomycetes,Agaricomycetidae,Agaricales,Amanitaceae,,
41955,Eukaryota,Fungi,Dikarya,Basidiomycota,Agaricomycotina,Agaricomycetes,Agaricomycetidae,Agaricales,Amanitaceae,Amanita,
41956,Eukaryota,Fungi,Dikarya,Basidiomycota,Agaricomycotina,Agaricomycetes,Agaricomycetidae,Agaricales,Amanitaceae,Amanita,Amanita muscaria
```

Both commands are fast and memory efficient to run.

# Contact

Please email [me](https://github.com/crosenth) by email for requests or concerns about current or
future taxonomic outputs.
