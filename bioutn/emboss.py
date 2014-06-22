import sys
import os
from StringIO import StringIO
import re

def getorf(file_content):
    try:
        print("Ejecutando EMBOSS getorf")
        f = open('temp_fasta.fasta', 'w')
        f.write(file_content.read())
        f.close()
        os.system('getorf temp_fasta.fasta temp_orf.orf')
        print("Analisis de ORF finalizado")
        os.remove('temp_fasta.fasta')
        f = open('temp_orf.orf','r')
        orf = f.read()
        f.close()
        os.remove('temp_orf.orf')
        return orf
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def getmotifs(file_content):
    try:
        print("Ejecutando EMBOSS prosextract")
        f = open('temp_fasta.fasta', 'w')
        f.write(file_content.read())
        f.close()
        os.system('prosextract -prositedir prosite')
        print("prosextract finalizado")
        print("Analizando motifs")
        os.system("patmatmotifs temp_fasta.fasta temp_fasta.patmatmotifs")
        os.remove('temp_fasta.fasta')
        f = open('temp_fasta.patmatmotifs','r')
        motifs = f.read()
        f.close()
        os.remove('temp_fasta.patmatmotifs')
        return motifs
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def parse_orf(file_content):
    try:
        table_html = "<tbody>"
        row_template = "<tr> \
                            <td>{0}</td> \
                        </tr>"
        hits = re.findall("(\>.*)", file_content.read())
        for hit in hits:
            table_html += row_template.format( hit )
        table_html+= "</tbody>"
        return (table_html, len(hits))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise