import sys
import os
import argparse
import pandas as pd
import numpy as np


# usage statement and input descriptions
parser = argparse.ArgumentParser(
    description='Calculates the mean and stdev for each histone mark in each file using the output from \
                    the post-processed Skyline Export Report generated by pepmodseq2histonemod.\
                    Requires Total Area Fragment column and Condition annotations, see tutorial for details.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('histonemod_file', type=str,
                    help='the output from pepmodseq2histonemod, requires Sample Group and Total Area Fragment columns.')
parser.add_argument('--output_path', default=os.getcwd(), type=str,
                    help='specify an output path for the decoded result file')

# parse arguments from command line
args = parser.parse_args()
histonemod_file = args.histonemod_file
output_dir = args.output_path


##
## read input files: FASTA and Skyline Export Report with Peptide Modified Sequences
##

# read in Skyline Export Report with Peptide Modified Sequences
skyline_df = pd.read_csv(histonemod_file)

if 'Condition' in skyline_df.columns:
    pass
else:
    sys.exit('ERROR: Skyline export file must include Condition column.\n')

if 'Peptide Modified Sequence' in skyline_df.columns:
    pass
else:
    sys.exit('ERROR: Skyline export file must include Peptide Modified Sequence column.\n')

if 'Total Area Fragment' in skyline_df.columns:
    pass
else:
    sys.exit('ERROR: Skyline export file must include Total Area Fragment column.\n')

sys.stdout.write("Successfully imported data, calculating summary statistics now.\n")


groupby_cols = ['Condition', 'Peptide Modified Sequence']

# make sample group "groupings" for each non-unique histone mark
frag_mean = skyline_df.groupby(groupby_cols)['Total Area Fragment'].mean().reset_index()
frag_mean = frag_mean.rename(columns={'Total Area Fragment': 'Condition Mean'}); print(frag_mean.head())
frag_stdev = skyline_df.groupby(groupby_cols)['Total Area Fragment'].std().reset_index()
frag_stdev = frag_stdev.rename(columns={'Total Area Fragment': 'Condition Stdev'})

skyline_df = skyline_df.merge(frag_mean, on=['Condition', 'Peptide Modified Sequence'])
skyline_df = skyline_df.merge(frag_stdev, on=['Condition', 'Peptide Modified Sequence'])
print(skyline_df.tail())

#sys.exit()

out_file = os.path.splitext(histonemod_file)[0]

skyline_df.to_csv(path_or_buf=os.path.join(output_dir, (out_file+'_summarystats.csv')), index=False)

sys.stdout.write("Finished decoding modified peptide sequences.\n")
