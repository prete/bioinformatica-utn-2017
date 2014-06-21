from Bio import Entrez

def fetch_accession(accession):
    print accession
    Entrez.email = "martinprete@gmail.com"
    handle = Entrez.efetch(db="nucleotide", id=accession, rettype="fasta", retmode="text")
    return handle.read()