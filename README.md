# bioblend_history_update
A python script to extract fastq and fastq.gz urls of histories from Galaxy

This code takes three required and one optional inputs:

1- required: workflow_name *

2- required: Galaxy_url **

3- required: Galaxy_APIkey ***

4- optional: Galaxy_url_write ****

The code generates a txt file as the output file. The txt file contains:
history_name, history_id, fastq url of Read 1, fastq url of Read 2, fastq.gz Read 1, fastq.gz Read2.

### dependencies:

It needs bioblend package (pip install bioblend)

### Pre-assumption:

The code assumes history names are in the following format:

WorkflowName_SequencerRunNumber-SampleID.VersionOfAnalysis.

For example: paired_002-121-3456.002

### More information about code inputs
*Histories in Galaxy are showing results of sample analysis by a specific workflow. In here we are asking to output fastq and fastq.gz urls of histories which specific worflow is used for analysis.

**Instance of Galaxy we are intrested to look into.

***API key of the Galaxy account holder to access histories.

****If the the url we need to wirte in the output is different than the address we give as Galaxy_url.
Somestimes explicit port number needs to be added to URL or, http needs to be used instead of https to access Galaxy from a  server. 

