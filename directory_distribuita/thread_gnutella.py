import socket # networking module
import sys
import threading
import time
import os
import hashlib

PKtidRicercati=[]
listaIpPeer=[]
listaRisultati=[]

class P2P(threading.Thread):

    def __init__(self, local_IP, P2P_port):

        threading.Thread.__init__(self)
        self.local_IP = local_IP
        self.P2P_port = P2P_port
        self.address=(self.local_IP,self.P2P_port)



    def run(self):

        self.peer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.peer.bind(self.address)
        self.peer.listen(100)

        while 1:


            (Peer_Client,IP_Client) = self.peer.accept()

            print "il client " + self.local_IP + " si e' connesso"

            peer = Handler(Peer_Client)
            peer.start()


class Handler(threading.Thread):


    def __init__(self, Peer_client):

        threading.Thread.__init__(self)
        self.connection=Peer_client


    def md5_for_file(self,fname, block_size=2**20):
        f=open('/home/taglio/Scrivania/'+fname,'rb')
        md5 = hashlib.md5()

        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
        f.close()
        return md5.digest()


    def  addPeer(self,ip,port):
        address=(ip,port)
        count = 0
        for i in range(len(listaIpPeer)):
            if listaIpPeer[i]== address:
                count = count + 1
        if count == 1:
            listaIpPeer.append(address)




    def run(self):

        print "Sono un thread che si occupa di un altro peer"

        chunk_dim = 128

        data = self.connection.recv(4)

        if data == "RETR":
            #receive RETR and search md5 of file from file_condivisi
            md5tofind = self.connection.recv(16)
            file_condivisi = open('/home/taglio/Scrivania/file_condivisi.txt', 'r')
            self.file_con=file_condivisi.readlines()
            for i in range(0,len(self.file_con)) :
                if self.md5_for_file(self.file_con[i].rstrip("\n")) == md5tofind:
                    self.nomefile=self.file_con[i]
            file_condivisi.close()




            #open the file, divide it in chunk
            try :
                file_to_send = open('/home/taglio/Scrivania/'+self.nomefile.rstrip("\n"), "rb")
            except Exception,expt:
                print "Error: %s" %expt + "\n"
                print "An error occured, file upload unavailable for peer \n"
            else :
                #number of chunk to send
                file_to_send.seek(0,2)
                tot_dim = file_to_send.tell()
                number_chunks = int(tot_dim // chunk_dim)
                resto = tot_dim % chunk_dim
                if resto != 0.0:
                    number_chunks+=1

                number_chunks_to = '%(#)06d' % {"#" : int(number_chunks)}
                file_to_send.seek(0,0)
                try :
                    chunk_sent = 0
                    self.connection.send("ARET" + number_chunks_to)
                    neof = 1
                    #send the file
                    while neof :
                        buff = file_to_send.read(chunk_dim)
                        neof = len(buff)
                        chunk_dim_to = '%(#)05d' % {"#" : len(buff)}
                        self.connection.send(chunk_dim_to + buff)
                        chunk_sent +=1
                        print "Sent " + str(chunk_sent)


                except EOFError:
                    print "You have read a EOF char"


                else :
                    print "End of upload of "+self.nomefile
                    file_to_send.close()

        if data=="QUER" :
            try:
                trovata=0
                #"QUER"[4B].PKtid[16B].IPP2P[15B].PP2P[5B].TTL[2B].Ricerca[20B]
                data = self.connection.recv(58)
                PKtid=data[:16]
                IPP2P=data[16:31]
                PP2P =data[31:36]
                TTL = data[36:38]
                search = data[38:58]
                #IPP2P è l'ip della macchina che ha effettuato la mia_ricerca
                if IPP2P==myIp :
                    #mi è stata inoltrata una richiesta che ho inviato io in precedenza. la ignoro
                    print "Ricerca partita da questa macchina: ignoro richiesta.. "
                else:
                    #self.addPeer(IPP2P,PP2P)
                    ipEId=IPP2P+PKtid
                    # ricercare all'interno del nostro database se abbiamo già fatto la mia_ricerca
                    for i in range(len(PKtidRicercati)) :
                        if ipEId==PKtidRicercati[i] :
                            trovata=1
                            print "Ricerca già effettuata in precendenza: ignoro richiesta .."

                    if trovata==0:
                        srcSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        PKtidRicercati.append(ipEId)
                        #TODO creare funzione di mia_ricerca in file condivisi e che se c'è invii il pacchetto di risposta
                        rt = ricerca_thread(search,IPP2P,PP2P,PKtid)
                        rt.start()
                        #propaga la query di mia_ricerca
                        if int(TTL)>1:
                        for i in range(len(listaIpPeer)) :
                            srcSocket.connect(listaIpPeer[i])
                            newTTL = int(TTL)-1
                            newTTLform= "%(#)02d" %{"#":int(newTTL)}
                            packet = "QUER"+PKtid+IPP2P+PP2P+str(newTTLform)+search
                            srcSocket.send(packet)
                        srcSocket.close()

            except Exception,ex :
                print ex

        if data=="AQUE" :
            try:
                #TODO passare il PKtid della ricerca in modo da verificarlo
                #"AQUE"[4B].PKtid[16B].IPP2P[15B].PP2P[5B].Filemd5[16B].Filename[100B]
                data = self.connection.recv(152)
                PKtid=data[:16]
                IPP2P=data[16:31]
                PP2P =data[31:36]
                Md5 = data[36:52]
                filename = data[52:152]
                trovato = False
                if (PKtid == self.PKtid_send):
                    for i in range(0,len(listaRisultati)):
                        rs = listaRisultati[i]
                        if (rs.Md5 == Md5) :
                            if (rs.ip == IPP2P) and (rs.port == PP2P):
                                print "ho già questo indirizzo associato a questo md5"
                                break
                            else :
                                self.num += 1
                                new=ResultFile(self.num,Md5,filename,IPP2P,PP2P)
                                listaRisultati.append(new)
                                trovato = True
                    if not trovato:
                        self.num +=1
                        new=ResultFile(self.num,Md5,filename,IPP2P,PP2P)
                        listaRisultati.append(new)
                else :
                    print "la ricerca non è stata effettuata da me"
            except Exception,ex :
                print ex

        if data=="NEAR" :
            try:
                #"NEAR"[4B].PKtid[16B].IPP2P[15B].PP2P[5B].TTL[2B]
                data = self.connection.recv(38)
                PKtid=data[:16]
                IPP2P=data[16:31]
                PP2P =data[31:36]
                TTL = data[36:38]
                nearAddr=(IPP2P,int(PP2P))
                self.addPeer(IPP2P,PP2P)
                nearSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ackForNear = "ANEA"+PKtid+myIp+myPort
                nearSocket.connect(nearAddr)
                nearSocket.send(ackForNear)
                #propaga al vicino
                if int(TTL)>1:
                    for i in range(len(listaIpPeer)) :
                        nearSocket.connect(listaIpPeer[i])
                        newTTL = int(TTL)-1
                        newTTLform= "%(#)02d" %{"#":int(newTTL)}
                        packet = "NEAR"+PKtid+IPP2P+PP2P+str(newTTLform)
                        nearSocket.send(packet)
                nearSocket.close()

            except Exception,ex :
                print ex


        if data=="ANEA":
            data=self.connection.recv(36)
            PKtid=data[:16]
            IPP2P=data[16:31]
            PP2P =data[31:36]
            self.addPeer(IPP2P,PP2P)

        self.connection.close()

