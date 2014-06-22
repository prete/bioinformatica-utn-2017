from os import curdir, sep, path
import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from socket import gethostname
import bioutn

class RequestHandler(BaseHTTPRequestHandler):

    # HEAD handler
    def do_HEAD(self):
        self.write_headers()
    ###########################################################################

    # GET handler
    def do_GET(self):
        try:
            if self.path == "/":
                f = open(curdir + sep + "views" + sep +"index.html")
            elif self.path.endswith(".html"):
                f = open(curdir + sep + "views" + sep + self.path)
            else:
                f = open(curdir + sep + self.path)
            self.write_headers()
            self.wfile.write(f.read())
            f.close()
        except IOError:
            self.send_error(404,'Error : %s' % self.path)
    ###########################################################################

    # POST handler
    def do_POST(self):
        try:
            if self.path=="/conversor/gb2fasta":
                self.convertir_gb2fasta()
            elif self.path=="/blast/p/online":
                self.blast_online()
            elif self.path=="/blast/p/local":
                self.blast_local()                
            elif self.path=="/blast/report":
                self.blast_report()
            elif self.path=="/accession":
                self.get_accession()
            else:
                self.send_error(404,'Error : %s' % self.path)
        except IOError:
            self.send_error(500,'Error : %s' % self.path)
    ###########################################################################

    # custom headers
    def write_headers(self):
        self.send_response(200)
        if self.path.endswith(".css"):
            self.send_header('Content-type','text/css')
        elif self.path.endswith(".js"):
            self.send_header('Content-type','text/javascript')
        else:
            self.send_header('Content-type','text/html')
        self.end_headers()
    ###########################################################################

    #obtener los parametros del request
    def get_PARAMS(self):
        try:
            form_fields = cgi.FieldStorage(fp=self.rfile,\
                                        headers=self.headers, \
                                        environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            return form_fields
        except:
            return {}
    ###########################################################################

    #Genbank a FASTA
    def convertir_gb2fasta(self):
        params = self.get_PARAMS()
        output = bioutn.gb2fasta(params['input_file'].file)
        file_name, file_extension = path.splitext(params['input_file'].filename)
        self.send_response(200)
        self.send_header('Content-type','application/fasta')
        self.send_header('Content-Disposition','attachment; filename=' + file_name + '.fasta')
        self.end_headers()
        self.wfile.write(output)
    ###########################################################################

    #BLASTP online contra el NCBI
    def blast_online(self):
        params = self.get_PARAMS()
        output = bioutn.bastp_online(params['input_file'].file)
        print output
        file_name, file_extension = path.splitext(params['input_file'].filename)
        self.send_response(200)
        self.send_header('Content-type','application/xml')
        self.send_header('Content-Disposition','attachment; filename=' + file_name + '_BLAST.xml')
        self.end_headers()
        self.wfile.write(output)
    ###########################################################################
    
    #BLASTP local
    def blast_local(self):
        params = self.get_PARAMS()
        output = bioutn.bastp_local(params['input_file'].file)
        file_name, file_extension = path.splitext(params['input_file'].filename)
        self.send_response(200)
        self.send_header('Content-type','application/xml')
        self.send_header('Content-Disposition','attachment; filename=' + file_name + '_BLAST.xml')
        self.end_headers()
        self.wfile.write(output)
    ###########################################################################
    
    #parseo de archivo BLAST
    def blast_report(self):
        params = self.get_PARAMS()
        table, hits, desc, version, target, program = bioutn.parse_blast(params['input_file'].file)
        f = open(curdir + sep + "views" + sep + "blast_result.html")
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        template = f.read();
        output = template.decode('utf-8') \
                        .replace("<<BLAST-RESULT-TABLE>>",table) \
                        .replace("<<BLAST-HITS>>", str(hits))\
                        .replace("<<BLAST-DESCRIPTION>>", desc)\
                        .replace("<<BLAST-VERSION>>", version)\
                        .replace("<<BLAST-TARGET>>", target) \
                        .replace("<<BLAST-PROGRAM>>", program)
        self.wfile.write(output.encode('utf-8'))
    ###########################################################################

    #busco el accession
    def get_accession(self):
        a = self.get_PARAMS()['accession'].value
        output = bioutn.fetch_accession(a)
        self.send_response(200)
        self.send_header('Content-type','application/fasta')
        self.send_header('Content-Disposition','attachment; filename=' + a + '.fasta')
        self.end_headers()
        self.wfile.write(output)
    ###########################################################################

# main
try:
    port = 6666
    server = HTTPServer(('', port), RequestHandler)
    print('=====================')
    print('Servidor inciado!')
    print('Ingrese a http://localhost:%d para acceder.' % port)
    print('Presione <ctrl+C> una o dos veces para salir.')
    print('=====================')
    server.serve_forever()
except KeyboardInterrupt:
    print('\n')
    print('<ctrl+C> recibido, cerrando el servidor.')
    server.socket.close()
