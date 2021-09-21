
alignment_file = "./data/cog_alignment.fasta.xz"
import pandas as pd
import lzma
import json
from Bio import SeqIO


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



df.to_csv("processed_metadata.csv")


reference_file = "./data/reference.fa"
reference = SeqIO.read(reference_file, "fasta")


ref_sequence = str(reference.seq)

for record in SeqIO.parse(lzma.open(alignment_file, 'rt'), 'fasta'):
        index = 21846-1
        residue = str(record.seq)[index]
        print(record.id,index+1,residue)
