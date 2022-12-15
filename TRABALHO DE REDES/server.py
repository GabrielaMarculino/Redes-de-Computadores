#Gabriela Marculino e Lincoln Amorim

import socket
import urllib3
import sys
import _thread
import argparse
import logging
import logging.handlers
import datetime

BUFLEN = 8192

class LRUCache(object):
    def __init__(self, tam):
        self.tam = tam
        self.cache = {}
        self.lru = {}
        self.expires = {}
        self.tm = 0

    def get(self, key):
        if key in self.cache:
            self.lru[key] = self.tm
            self.tm = self.tm + 1
            return self.cache[key]
        else:
            return -1

    def set(self, key, value):
        sizebytes = 0
        for i in self.cache:
            sizebytes += sys.getsizeof(self.cache[i])
        while (sizebytes + sys.getsizeof(value)) > self.tam:
            if sys.getsizeof(value) > self.tam:
                msg = str(_thread.get_native_id()) + "\tEVICT\t"+key+"\tCACHE FULL"
                logging.info(msg)
                exit(1)
            else:
                msg = str(_thread.get_native_id()) + "\tEVICT\t"+key+"\tCACHE FULL"
                logging.info(msg)
                old_key = min(self.lru.keys(), key=lambda k: self.lru[k])
                msg = str(_thread.get_native_id()) + "\tEVICT\t"+old_key+"\tEXPIRED"
                logging.info(msg)
                self.cache.pop(old_key)
                self.lru.pop(old_key)
                self.expires.pop(old_key)
            sizebytes = 0
            for i in self.cache:
              sizebytes += sys.getsizeof(self.cache[i])
        self.cache[key] = value
        self.lru[key] = self.tm
        tempo = datetime.datetime.now()
        tempo += datetime.timedelta(minutes=1)
        self.expires[key] = tempo
        self.tm = self.tm + 1

    def clean(self):
        self.cache = {}
        self.lru = {}
        self.expires = {}
        self.tm = 0

    def delete(self,key):
        self.cache.pop(key)
        self.lru.pop(key)
        self.expires.pop(key)

    def dump(self):
        msg = str(_thread.get_native_id()) + "\tDUMP\tDump Start"
        logging.info(msg)
        sizebytes = 0
        for i in self.cache:
            sizebytes += sys.getsizeof(self.cache[i])
        msg = str(_thread.get_native_id()) + "\tDUMP\tSize "+str(sizebytes/1024)
        logging.info(msg)
        for i in self.cache:
            sizebytes = sys.getsizeof(self.cache[i])
            msg = str(_thread.get_native_id()) + "\tDUMP\tfileid1\t"+str(sizebytes/1024)+"\t"+str(self.expires[i])+"\t"+i
            logging.info(msg)
        msg = str(_thread.get_native_id()) + "\tDUMP\tDump End"
        logging.info(msg)
        
    def dumpnotex(self):
        msg = str(_thread.get_native_id()) + "\tDUMP\tDump Start"
        logging.info(msg)
        timenow = datetime.datetime.now()
        sizebytes = 0
        for i in self.cache:
            timeexpiring = self.expires[i]
            if timenow < timeexpiring:
                sizebytes += sys.getsizeof(self.cache[i])
        msg = str(_thread.get_native_id()) + "\tDUMP\tSize "+str(sizebytes/1024)
        logging.info(msg)
        for i in self.cache:
            timeexpiring = self.expires[i]
            if timenow < timeexpiring:
                sizebytes = sys.getsizeof(self.cache[i])
                msg = str(_thread.get_native_id()) + "\tDUMP\tfileid1\t"+str(sizebytes/1024)+"\t"+str(self.expires[i])+"\t"+i
                logging.info(msg)
        msg = str(_thread.get_native_id()) + "\tDUMP\tDump End"
        logging.info(msg)
    
    def changesize(self,newsize):
      sizebytes = 0
      for i in self.cache:
        sizebytes += sys.getsizeof(self.cache[i])
      while newsize < sizebytes:
        old_key = min(self.lru.keys(), key=lambda k: self.lru[k])
        self.cache.pop(old_key)
        self.lru.pop(old_key)
        self.expires.pop(old_key)
        sizebytes = 0
        for i in self.cache:
          sizebytes += sys.getsizeof(self.cache[i])
      self.tam=newsize

    def expired(self, url):
      timenow = datetime.datetime.now()
      timeexpiring = self.expires[url]
      if timenow > timeexpiring:
        self.delete(url)
        return testcache("GET", url)
      else:
        return testcache("GET", url)


def testcache(met, url):
    global caching, tamcache, numhits, numfails
    http = urllib3.PoolManager()
    response = http.request(met, url)
    test = caching.get(url)

    if(test == -1):
        result = response.data
        test = caching.set(url, result)
        numfails += 1
        msg = str(_thread.get_native_id())+"\tADD\t"+url
        logging.info(msg)
        return result
    else:
        numhits += 1
        msg = str(_thread.get_native_id())+"\tHIT\t"+url
        logging.info(msg)
        return test


# controle das threads
def controlt(c):
    global caching, numpedidos
    # recebe o request
    msg = ""
    req = ""
    req = c.recv(BUFLEN).decode()
    reqsplit = req.split()

    if len(reqsplit) == 1:
        c.send(b'Incomplete Request')
        c.close()
        exit()

    reqsplit[1] = reqsplit[1].lower()

    if not("http://" in reqsplit[1]) and not("ADMIN" in reqsplit):
        reqsplit[1] = "http://"+reqsplit[1]

    if "HTTP/1.1" in reqsplit and not("ADMIN" in reqsplit):
        reqsplit[0] = "GET"

    if "ADMIN" in reqsplit:
        reqsplit[1] = reqsplit[1].upper()
    numpedidos += 1
    # trata o request
    match reqsplit[0]:
        case "GET":
            if "if-modified-since" in reqsplit:
                try:
                    c.send(caching.expired(reqsplit[1]))
                except:
                    c.send(b'404 Not Found')
            else:
                try:
                    c.send(testcache(reqsplit[0], reqsplit[1]))
                except:
                    c.send(b'404 Not Found')
        case "ADMIN":
            match reqsplit[1]:
                case "FLUSH":
                    msg = str(_thread.get_native_id())+"\tFLUSH\tRequested"
                    logging.info(msg)
                    caching.clean()
                    c.send(b'200 HTTP OK')
                case "DELETE":
                    try:
                        caching.delete(reqsplit[2])
                    except:
                        c.send(b'404 Not Found')
                        c.close()
                        exit()
                    c.send(b'200 HTTP OK')
                case "INFO":
                    match reqsplit[2]:  # TODO
                        case "0":  # salva tamanho atual e lista de objetos do cache
                            caching.dump()
                            c.send(b'200 HTTP OK')
                        case "1":  # salva os não-expirados (igual o 0)
                            caching.dumpnotex()
                            c.send(b'200 HTTP OK')
                        case "2":  # mostra as estatísticas
                            sizebytes = 0
                            for i in caching.cache:
                                sizebytes += sys.getsizeof(caching.cache[i])
                            msg = str(_thread.get_native_id()) + "\tNúmero Total de Pedidos:\t"+str(numpedidos)
                            logging.info(msg)
                            msg = str(_thread.get_native_id()) + "\tNúmero Total de Hits:\t"+str(numhits)
                            logging.info(msg)
                            msg = str(_thread.get_native_id()) + "\tNúmero Total de Fails:\t"+str(numfails)
                            logging.info(msg)
                            try:
                                msg = str(_thread.get_native_id())+"\tTamanho Médio das Páginas em Cache:\t"+str((sizebytes/numfails)/1024)
                                logging.info(msg)
                            except:
                                msg = str(_thread.get_native_id())+"\t0 Páginas em Cache"
                                logging.info(msg)
                            c.send(b'200 HTTP OK')
                        case other:
                            c.send(b'Error 501 Not Implemented!')
                case "CHANGE":
                    msg = str(_thread.get_native_id())+"\tCHSIZE\told: " +str(caching.tam/1024)+"\tnew: "+reqsplit[2]
                    logging.info(msg)
                    caching.changesize(int(reqsplit[2])*1024)
                    c.send(b'200 HTTP OK')
                case other:
                    c.send(b'Error 501 Not Implemented!')
        case other:
            c.send(b'Error 501 Not Implemented!')
    i = 0
    # fecha a conexao com o cliente
    c.close()


######################main###########################
parser = argparse.ArgumentParser(
    prog='python3', usage='%(prog)s path [options]')
parser.add_argument('-c', type=int, help="tamanho do cache em kb")
parser.add_argument('-p', type=int, help="numero do port", required=True)
parser.add_argument('-l', type=str, help="nome do arquivo de log")

argv = parser.parse_args()

port = argv.p

if not(argv.c == None):
    tamcache = argv.c*1024
    print("Tamanho do cache definido como:", tamcache)
else:
    tamcache = 500*1024
    print("Tamanho do cache definido como:", tamcache)
if not(argv.l == None):
    nomelog = argv.l
else:
    nomelog = "log.txt"
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[
                    logging.FileHandler(nomelog, mode="w"), logging.StreamHandler()])

caching = LRUCache(tam=tamcache)

# cria o socket
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind(('', port, 0, 0))
except socket.error:
    print("Erro no bind da porta:", port)
    sys.exit(-1)
print("Port definido como:", port)

# coloca o socket em listen
s.listen(1)
print("Socket is listening")
numpedidos = 0
numhits = 0
numfails = 0
# loop
while True:
    # abre a conexao com o cliente
    c, addr = s.accept()
    msg = 'Got connection from ' + str(addr)
    logging.info(msg)
    _thread.start_new_thread(controlt, (c,))