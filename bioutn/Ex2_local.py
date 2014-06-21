from Bio.Blast import NCBIWWW
from Bio.Blast.Applications import NcbiblastxCommandline

def Ex2Local():
    fasta_string = open("ls_orchid.fasta").read();
    blastx_cline = NcbiblastxCommandline(query="opuntia.fasta", db="nr", evalue=0.001,outfmt=5, out="opuntia.xml")
    stdout, stderr = blastx_cline()
    
Ex2Local()