import socket
import sys
import hashlib
import threading
from risultati import ResultFile
import thread_gnutella
import shutil

class PEER(object):

    def __init__(self):

        """
          This method set the connection parameters, to allow other peer/directory to connect and communicate.
        """

        #IP address of the directory
        self.HOSTNAME = "192.168.1.100"
        #connection port to the directory
        self.PORT = 80
        self.addr = (self.HOSTNAME,self.PORT)
        #port that I make available to other peers for downloading
        self.p2pPort = 6120
        self.resultfiles=[]
        self.file_con=[]
        self.ip = self.sock.getsockname()[0]
        ips_noform = self.ip.split(".")
        ips1= '%(#)03d' %{"#":int(ips_noform[0])}
        ips2= '%(#)03d' %{"#":int(ips_noform[1])}
        ips3= '%(#)03d' %{"#":int(ips_noform[2])}
        ips4= '%(#)03d' %{"#":int(ips_noform[3])}
        self.my_Ip = ips1+"."+ips2+"."+ips3+"."+ips4
        #end of __init__ method



    def open_socket(self):

        """
          This method create a connection
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.connect(self.addr)
        #end of open_socket method


    def sockread(self, socket, numToRead):

        allread = socket.recv(numToRead)
        num = len(allread)

        while (num < numToRead):
            letti = socket.recv(numToRead - num)
            num = num + len(read)
            allread = allread + read

        return lettiTot
        #end of sockread method


    def md5_for_file(self,fname, block_size=2**20):

        """
        This method md5_for_file allows the user to get the md5 checksum of a file, given as parameter.
        """

        f=open('/home/taglio/Scrivania/'+fname,'rb')
        md5 = hashlib.md5()

        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
        f.close()
        return md5.digest()
        #end of md5_for_file method

    def download(self,i):

        """
          This method allows the user to make a download from another peer in the P2P network
        """

        #selected from keyboard file to download
        rs=self.listaRisultati[int(i)]
        #TODO se faccio così elimino tutti i risultati della ricerca,quindi guardare se può andare bene oppure no
        listaRisultati = []
        #create the connection for download the file
        self.downip=rs.ip
        self.downport=int(rs.porta)
        self.address=(self.downip,self.downport)
        self.download = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create TCP
        self.download.connect(self.address)

        self.md5down = rs.file_md5
        down = "RETR"+self.md5down
        f1 = open (rs.filename, 'a')
        print "invio: "+down
        self.download.send(down+"\n")
        print "ciao"
        ackdown = self.download.recv(4)
        if ackdown == "ARET":
            nchunk = self.download.recv(6)
            print "ARET"
            for i in range(1,int(nchunk)):
                lchunk = self.download.recv(5)
                lenchunk=lchunk.lstrip("0")
                print lenchunk
                chunk = self.sockread(self.download,int(lenchunk))
                if not chunk: break
                f1.write(chunk)
            f1.close()
            ack = "ok"
            return ack
            self.download.close()
        else:
            print "errore nel download prova a scaricare di nuovo"
            ack = "no"
            return ack
            self.download.close()

    #end of download method

    def my_research(self):

        stringa = raw_input("""Cosa vuoi cercare ??  : """)
        for i in range(100-len(stringa)) :
            stringa=stringa+" "
            #print stringa
        self.PKtid_send=random.randint(0,99999)#TODO mettere a posto il paktid
        TTLnoform = 4
        TTL= "%(#)02d" %{"#":int(TTLnoform)}
        #"QUER"[4B].PKtid[16B].IPP2P[15B].PP2P[5B].TTL[2B].Ricerca[20B]
        pacchetto="QUER"+str(self.PKtid_send)+myIp+myport+str(TTL)+stringa
        srcSocket = socket(AF_INET, SOCK_STREAM)
        try:

            for i in range(len(listaIpPeer)) :

                errore=srcSocket.connect_ex((listaIpPeer[i],myPort))
                if errore==0 :
                    srcSocket.send(pacchetto)
                    print "*** Attendi prego per 30 secondi mentre inoltro la ricerca ***"
                #saranno 30 secondi
            timeStart = time.time()
            time.sleep(30)
            print "**** Stampa Risultati ***** "
            dim = len(listaRisultati)
            firstloop = True
            while ((time.time()-timeStart) > 270 ):
                if firstloop:
                    for i in range(0,len(listaRisultati)):
                        rs=listaRisultati[i]
                        print "%d %s %s:%s" %(i,rs.filename,rs.ip,rs.port)
                    firstloop = False
                else :
                    if (len(listaRisultati)>dim):
                        count = len(listaRisultati)-dim
                        for i in range(0,count):
                            new = dim +i
                            rs=listaRisultati[new]
                            print "%d %s %s:%s" %(new,rs.filename,rs.ip,rs.port)
                        dim = len(listaRisultati)
            self.PKtid_send = 0


        except Exception,ex :
            print ex
