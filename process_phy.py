import os
import shutil
from Bio import SeqIO

for fi in os.listdir(os.getcwd()):
    if not fi.endswith('.phy'):
        continue
    new_fi = fi.replace(" ", "")
    ids, seqs = [], []
    try:
        with open(fi) as input_handle:
            for record in SeqIO.parse(fi, 'phylip'):
                ids.append(record.id)
                seqs.append(record.seq)
    except ValueError:
        pass

    os.remove(fi)
    with open(new_fi, 'w+') as output_handle:
        for num, recs in enumerate(zip(ids, seqs)):
            if not num:
                output_handle.write("     {}     {}\n".format(len(ids), len(recs[1])))
            output_handle.write("{}     {}\n".format(*recs))
