Bioninformática
==============

#Requerimientos
Python 2.7.x: http://www.python.org/

Biopython: http://biopython.org/

##Adicionales
BLAST+: http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download

swissprot db: ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/swissprot.gz

EMBOSS: http://emboss.sourceforge.net/

prosite db: ftp://ftp.expasy.org/databases/prosite/


#Uso
Iniciar el servidor
`>>>python server.py`

Ingresar en http://localhost:6666

#Navegacion del sitio

##Inicio
Resumen del trabajo con bases de datos biológicas

##Menu Conversores
Permite convertir entre diferentes formatos:
* GenBank -> FASTA (traducción de DNA/mRNA -> prot)
* GenBank -> FASTA (sin traducir)

##Menu BLAST
Permite realizar y analizar BLAST:
* Analizar BALST output
* Realizar un BLAST online (consultando en el NCBI)
* Realizar un BLAST local (usando `blastp` sobre db swissprot)

##Menu EMBOSS
Permite realizar analisis y visualizar resultados usando EMBOSS
* Analizar ORF
* Analizar Dominios
* Obtener ORF (usando `getorf`)
* Obtener Dominios (usando `patmatmotifs`)
