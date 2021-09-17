import pandas as pd
import lzma
import json
metadata_file = './data/cog_metadata.csv.xz'
handle = lzma.open(metadata_file, 'rt')
df = pd.read_csv(handle)

alias_file = "./data/alias_key.json"
alias_dict = json.load(open(alias_file))

def expand_alias(input_string):
    if "." not in input_string:
        return input_string

    alias, rest = input_string.split('.', 1)

    if alias in alias_dict:
        if alias_dict[alias] == "":
            return alias + '.' + rest
        else:
            return alias_dict[alias] + '.' + rest
        

df['full_lineage'] = df['lineage'].apply(expand_alias)

df = df[(df['full_lineage']+".").str.startswith('B.1.617.2.')]

df = df[df['sample_date']>"2021-09-01"]

df = df.sample(frac=0.001)



alignment_file = "./data/cog_alignment.fasta.xz"
from Bio import SeqIO

reference_file = "./data/reference.fa"
reference = SeqIO.read(reference_file, "fasta")

ref_sequence = str(reference.seq)

for record in SeqIO.parse(lzma.open(alignment_file, 'rt'), 'fasta'):
    if record.id in df['sequence_name'].values:
        for index, residue in enumerate(list(record.seq)):
            if residue != ref_sequence[index] and residue !="N":
                print(record.id,index+1,residue)
