import gzip
import logging
try:
    import cPickle as pickle
except:
    import pickle

from interval_tree import IntervalTree

logger = logging.getLogger(__name__)

def build_gene_trees(infile, gene_db):
    """Build gene trees from the gene file"""
    gene_trees = {}
    chromosome_stops = {}
    with gzip.open(infile) as f:
        for line in f:
            if not line.startswith('#'):
                line = line.rstrip().split('\t')
                # print(line)
                # print(len(line))
                if len(line) >= 6:
                    chrom = line[0]
                    start = int(line[1])
                    stop = int(line[2])
                    hgnc_symbol = line[5]
                    if hgnc_symbol:
                        if chrom in gene_trees:
                            if not hgnc_symbol in gene_trees[chrom]:
                                gene_trees[chrom][hgnc_symbol] = [start, stop]
                        else:
                            gene_trees[chrom] = {}
                            gene_trees[chrom][hgnc_symbol] = [start, stop]
                        
                        if stop > chromosome_stops.get(chrom, 0):
                            chromosome_stops[chrom] = stop + 1
    
    #Prepare for interval tree
    interval_trees = {}
    for chromosome in gene_trees:
        for gene_symbol in gene_trees[chromosome]:
            start = gene_trees[chromosome][gene_symbol][0]
            stop = gene_trees[chromosome][gene_symbol][1]
            interval = [start, stop, gene_symbol]
            if chromosome in interval_trees:
                interval_trees[chromosome].append(interval)
            else:
                interval_trees[chromosome] = [interval]
    

    for chrom in gene_trees:
        interval_trees[chrom] = IntervalTree(
            interval_trees[chrom], 
            1, 
            chromosome_stops[chrom]
        )
    
    with open(gene_db, 'wb') as f:
        logger.info("Dumping gene database to {0}.".format(gene_db))
        pickle.dump(interval_trees, f)
        logger.debug("Dumping successful.")
    




            
