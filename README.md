CSV-to-GraphML-DiGraphs
=======================

Simple script to process a csv file to return a graphML file for bimodal / bipartitie graph.

Used for TMT document-topic matrix output from the Stanford TMT (http://nlp.stanford.edu/software/tmt/tmt-0.4/), 
that has WOS record fields and content analysis fields manually added in & prepare these for opening
in Gephi. If using Gephi, it's helpful to specify that a graphML file is being opened in Gephi - otherwise,
double check what was imported.
 
Calling/Usage:	python csv_to_graphML.py <infile> <outfile>
 
 		helpful to use ".graphML" prefix to outfile name for gephi import
    Note: When opening in gephi, specify that a 'graphML' file is being imported.
