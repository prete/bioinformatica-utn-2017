#modules
import sys
import os
from StringIO import StringIO
#biopython modules
from Bio import SearchIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline


def bastp_online(file_content):
    try:
        print("Consultando NCBI...")
        result_handle = NCBIWWW.qblast("blastp", "swissprot", file_content.getvalue())
        print("Respuesta a BLAST obtenida!")
        out_handle = result_handle.read()
        result_handle.close()
        return out_handle
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        
def bastp_local(file_content):
    try:
        f = open("local_blast_input.fasta","w")
        f.write(file_content.getvalue())
        f.close()
        cmd = NcbiblastpCommandline(query="local_blast_input.fasta", \
                        db="swissprot", outfmt=5, out="local_blast_output.xml")
        stdout, stderr= cmd()
        o = open("local_blast_output.xml")
        out_handle = o.read()
        o.close()
        #cleanup
        try:
            os.remove("local_blast_input.fasta")
            os.remove("local_blast_output.xml")
        except:
            print("no se pudo borrar temporales...")
        return out_handle
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise        

def parse_blast(file_content):
    try:
        table_html = "<tbody>"
        row_template = "<tr> \
                            <td>{0}</td> \
                            <td><button type=\"button\" class=\"btn btn-xs btn-primary\" \
                                    onclick=\"getAccession('{1}')\">{1}</button></td> \
                            <td>{2}</td> \
                            <td>{3}</td> \
                            <td>{4}</td>\
                        </tr>"
        blast_record = SearchIO.read(file_content, 'blast-xml')
        for hit, hsp in zip(blast_record.hits, blast_record.hsps):
            table_html += row_template.format( hit.id, hit.accession, hsp.bitscore, hit.seq_len, hit.description.replace(";","<br/>") )
        table_html+= "</tbody>"
        return (table_html, len(blast_record.hits), blast_record.description, blast_record.version, blast_record.target, blast_record.program)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
