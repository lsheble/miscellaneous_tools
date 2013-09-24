CSV-to-GraphML-DiGraphs
=======================

Simple script to process a csv file to return a graphML file for bimodal / bipartitie graphs.

This version used to prepare TMT document-topic matrix output from the Stanford TMT 
(http://nlp.stanford.edu/software/tmt/tmt-0.4/) to which additional document-related fields were added (from WOS S/SCI
records and content analysis) in order to open in Gephi.

If using Gephi, it's helpful to specify that a graphML file is being opened in Gephi - otherwise, double check 
what was imported.
 
Calling/Usage:	

python csv_to_graphML.py <infile> <outfile>
 
 		helpful to use ".graphML" suffix on outfile name for gephi import
   
