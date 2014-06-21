from Bio import SeqIO
from StringIO import StringIO
from Bio.SeqRecord import *
from Bio.Seq import *
import os

#traduce DNA a Proteina
def DNA_to_protein(dna):
    return dna.seq.translate()

#crea un SeqRecord a partir de un Seq
def seq_to_seqrecord(seq, id):
    return SeqRecord(seq = seq, \
        id = id, \
        description = id+' translated to Protein'
    )

#gb2fasta
def gb2fasta(file_content):
    gb_records = SeqIO.parse(file_content, "genbank")
    protein_list = [ seq_to_seqrecord( DNA_to_protein(dna_record), dna_record.id ) for dna_record in gb_records]
    out_handle = StringIO()
    SeqIO.write(protein_list, out_handle, "fasta")
    return out_handle.getvalue()