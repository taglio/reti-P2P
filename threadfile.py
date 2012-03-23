import socket # networking module
import sys
import threading
import time
import os


class P2P(threading.Thread):

    def __init__(self, local_IP, P2P_port):


        threading.Thread.__init__(self)
	self.stop = False
        self.local_IP = local_IP
        self.P2P_port = P2P_port
	self.address=(self.local_IP,self.P2P_port)
	
    def run(self):

       

        # Metto a disposizione una porta per il peer to peer
        self.peer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	self.peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.peer.bind(self.address)
        self.peer.listen(100) #socket per chi vorra' fare download da me

        while 1:

            # entro nel while con la socket ("peer_socket") gia' in listen
            # voglio far partire un thread per ogni accept che ricevo

            (Peer_Client,IP_Client) = self.peer.accept() # la accept restituisce la nuova socket del client connesso, e il suo indirizzo

            print "il client " + self.local_IP + " si e' connesso"

            peer = Handler(Peer_Client,IP_Client)
            peer.start()


class Handler(threading.Thread):


    def __init__(self, Peer_client, address_client):

        threading.Thread.__init__(self)

        # info sul peer che si connette, magari servono
        self.Peer_client = Peer_client
        self.address_client = address_client
       

    def filesize(self, filename):

        ### calcolo della dimensione del file

        F = open(filename,'r')
        F.seek(0,2)
        dim = F.tell()
        F.seek(0,0)
        F.close()
        return dim

    def run(self):

        print "Sono un thread che si occupa di un altro peer"

        chunk_dim = 128 # specifica la dimensione in byte del chunk (fix)

        # mi metto in receive della string "RETR"
        download = self.Peer_client.recv(4)
        if download == "RETR":
            print "ok, mi hai chiesto il file, controllo l'md5"

            md5tofind = self.Peer_client.recv(16)
	    
            # ricerca della corrispondenza
	    file_condivisi = open('/home/taglio/Scrivania/file_condivisi.txt', 'r')
	    self.file_con=file_condivisi.readlines()
   	    for i in range(0,len(self.file_con)) : 
		if self.file_con[i] == md5rem:
			self.nomefile=self.file_con[i+1]
	    file_condivisi.close()
            
	    

            # dividere il file in chuncks

            try :
                file_to_send = open(self.nomefile, "rb")
            except Exception,expt:
                print "Error: %s" %expt + "\n"
                print "An error occured, file upload unavailable for peer \n"
            else :
		file_to_send.seek(0,2)
        	tot_dim = file_to_send.tell()
                number_chunks = int(tot_dim // chunk_dim) #risultato intero della divisione
                resto = tot_dim % chunk_dim #eventuale resto della divisione
                if resto != 0.0:
                    number_chunks+=1

                number_chunks_to = '%(#)06d' % {"#" : int(number_chunks)}
                file_to_send.seek(0,0) #sposto la testina di lettura ad inizio file
                try :
                    chunk_sent = 0
                    self.Peer_client.send("ARET" + number_chunks_to)
		    neof = 1
                    while neof :
			buff = file_to_sent.read(chunk_dim) 
			neof = len(buff)
                        chunk_dim_to = '%(#)05d' % {"#" : len(buff)}
                        self.Peer_client.send(chunk_dim_to + buff)
                        chunk_sent +=1
                        print "Sent " + chunk_sent  
                      
                        
                except EOFError:
                    print "You have read a EOF char"
                except ConnException:
                    print "Your friend is a bad peer, and a bad developer!\n"

                else :
                    print "End of upload to of "+filename
                    file_to_send.close()
        else:
            print "ack parsing failed, for RETR\n"
	self.Peer_client.close()
        
