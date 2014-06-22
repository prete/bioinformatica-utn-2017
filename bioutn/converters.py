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

#nucleotid gb -> protein fasta
def nucgb2protfasta(file_content):
    gb_records = SeqIO.parse(file_content, "genbank")
    protein_list = [ seq_to_seqrecord( DNA_to_protein(dna_record), dna_record.id ) for dna_record in gb_records]
    out_handle = StringIO()
    SeqIO.write(protein_list, out_handle, "fasta")
    return out_handle.getvalue()
    
#nucleotid fasta -> protein gb
def nucfasta2protgb(file_content):
    gb_records = SeqIO.parse(file_content, "fasta")
    protein_list = [ seq_to_seqrecord( DNA_to_protein(dna_record), dna_record.id ) for dna_record in gb_records]
    out_handle = StringIO()
    SeqIO.write(protein_list, out_handle, "genbank")
    return out_handle.getvalue()    
    
#gb -> fasta (sin traducir)
def gb2fasta(file_content):
    gb_records = SeqIO.parse(file_content, "genbank")
    SeqIO.write(protein_list, gb_records, "fasta")
    return out_handle.getvalue()
    
#fasta -> gb (sin traducir)
def fasta2gb(file_content):
    gb_records = SeqIO.parse(file_content, "fasta")
    SeqIO.write(protein_list, gb_records, "genbank")
    return out_handle.getvalue()    
