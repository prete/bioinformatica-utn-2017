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
                            <td>{1}</td> \
                            <td>{2}</td> \
                            <td>{3}</td> \
                            <td>{4}</td> \
                        </tr>"
        orf = file_content.read()
        hits = re.findall("(\>.*)", orf)
        for hit in hits:
            id_orf = re.search("\w+\.\d\_\d+", hit)
            index = re.search("\[.*\]", hit)
            desc = re.search(" (\w*( ))+\w+", hit)
            family = re.search("\,.*\,", hit)
            orf_type = re.search("\,( \w*)$", hit)
             
            table_html += row_template.format( id_orf.group(0), index.group(0), desc.group()[1:], family.group(0)[2:-1],  orf_type.group(0)[2:] )
        table_html+= "</tbody>"
        return (table_html, len(hits))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise