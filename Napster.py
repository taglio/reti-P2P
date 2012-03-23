import socket
import sys
import hashlib
import threading
from risultati import ResultFile
import threadfile
import shutil

class PEER(object):
	def __init__(self):
	

		self.HOSTNAME = "10.42.43.1"
		self.PORT = 9994
		self.addr = (self.HOSTNAME,self.PORT)
		self.p2pPort = 7029
		self.resultfiles=[]
		self.file_con=[]
		
	def open_socket(self):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #create TCP
    		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    		self.sock.connect(self.addr)

	def md5_for_file_hex(self,fname, block_size=2**20):
    		f=open('/home/taglio/Scrivania/'+fname,'rb')
    		md5 = hashlib.md5()
    
    		while True:
        		data = f.read(block_size)
        		if not data:
        	    		break
        	md5.update(data)
    		return md5.hexdigest()

	def md5_for_file(self,fname, block_size=2**20):
    		f=open('/home/taglio/Scrivania/'+fname,'rb')
    		md5 = hashlib.md5()
    
    		while True:
        		data = f.read(block_size)
        		if not data:
        	    		break
        	md5.update(data)
    		return md5.digest()

#end function md5_for_file


   
	def login(self):
		#apro la socket
		self.open_socket()
		
		
		#leggo il mio ip e lo formatto adeguatamente per inviarlo alla directory

    		self.ip = self.sock.getsockname()[0]
    		ips_noform = self.ip.split(".")
    		ips1= '%(#)03d' %{"#":int(ips_noform[0])}  
    		ips2= '%(#)03d' %{"#":int(ips_noform[1])} 
    		ips3= '%(#)03d' %{"#":int(ips_noform[2])} 
    		ips4= '%(#)03d' %{"#":int(ips_noform[3])} 
		
		#apro la socket per i peer
	       	self.upload_for_peers = threadfile.P2P(self.ip, self.p2pPort)
            	self.upload_for_peers.start()

    		self.ip_to_send = ips1+"."+ips2+"."+ips3+"."+ips4
	
    		log = "LOGI"+self.ip_to_send+str(self.p2pPort)
    
		
    		print "invio: "+log
    		self.sock.send(log+"\n")
    
    		data = self.sock.recv(4)
    		if  data =="ALGI":
			print data
         		self.sessionID = self.sock.recv(16)
         
         		if self.sessionID == "0000000000000000":
	 			login = "no"
				return login
	 			self.sock.close()
			else : 
				login = "ok"
				return login
	
	        else : 
			login = "no"
			return login
		self.sock.close()

		
#add file
	def addfile(self,filename):

	    self.open_socket()

	    md5add =self.md5_for_file(filename) #calcolo md5 del file
	    print md5add
    	    file_condivisi = open('/home/taglio/Scrivania/file_condivisi.txt', 'wa')
	    file_condivisi.write(md5add+"\n")
            file_condivisi.write(filename+"\n")
	    file_condivisi.close()
	    fname= "%(#)0100s" %{"#" :filename}

	    addfile = "ADDF"+self.sessionID+md5add+fname

	    #invio pacchetto
	    print "invio: "+addfile
	    self.sock.send(addfile+"\n")
	    #ricevo ack AADD
	    ackadd = self.sock.recv(4)
	    if ackadd == "AADD":
		ncopy = self.sock.recv(3)
		if int(ncopy) < 1:
			print "errore nessun file presente, aggiungilo nuovamente"
			ack = "no"
			return ack
			
		else:
			ack = "ok"
			return ack
	    else:
	        print "non e' stato aggiunto il file!\n"
		ack="no"
		return ack

	    self.sock.close()

#remove file
	def rmfile(self,fname):
	    self.open_socket()

	    md5rem = self.md5_for_file(fname)
	    print md5rem 
	    md5rem_hex=self.md5_for_file_hex(fname)   
   	    file_condivisi = open('/home/taglio/Scrivania/file_condivisi.txt', 'r')
	    self.file_con=file_condivisi.readlines()
	    print self.file_con
   	    for i in range(0,len(self.file_con)) : 
		if self.file_con[i] == md5rem:
			del self.file_con[i]
			del self.file_con[i+1]
	    
	    filetemp=open('/home/taglio/Scrivania/file_condivisitemp.txt', 'w')
	    filetemp.writelines(self.file_con)
	    filetemp.close()
	    file_condivisi.close()
	    shutil.copyfile('/home/taglio/Scrivania/file_condivisitemp.txt','/home/taglio/Scrivania/file_condivisi.txt')
	    
	    removefile = "DELF"+self.sessionID+md5rem

	    print "invio: " +removefile
	    self.sock.send(removefile+"\n")

	    ackrem = self.sock.recv(4)
	    if ackrem == "ADEL":
		ncopy = self.sock.recv(3)
		print "numero di copie sul server:"+ncopy+"\n"
		ack = "ok"
		return ack	

		if nt(ncopy)<0:
			print "errore durante l'eliminazione\n"
			ack = "no"
			return ack
	    else:
		print"errore ack non ricevuto, riprovare"
		ack = "no"
		return ack

	    self.sock.close()

#logout
	def logout(self):
	    self.open_socket()

	    logout = "LOGO"+self.sessionID

	    print "invio: "+logout
	    self.sock.send(logout+"\n")

	    acklogout = self.sock.recv(4)
	    if acklogout == "ALGO":
		ndelete = self.sock.recv(3)
		print "numero di file cancellati"+ndelete+"\n"
		ack = "ok"
		return ack
		self.sock.close()
		self.upload_for_peers.stop=True
		self.upload_for_peers.peer.close()
	    else:
		print "errore ack, riprovare"
		ack = "no"
		return ack
		self.sock.close()

#search
	def find(self,search):

	    self.open_socket()
 	

	    self.resultfiles=[]
	    ricerca = "%(#)020s" %{"#":search} 
	    find = "FIND"+self.sessionID+ricerca

	    print "invio: "+find
	    self.sock.send(find+"\n")
    
	    ackfind = self.sock.recv(4)
	    if ackfind == "AFIN":
		nfile = self.sock.recv(3)
		print "Nome file  Numero copie "+nfile+"\t\t\t\t IP \t Porta"
		if int(nfile) == 0:
			print "nessun risultato per la ricerca"
		else:
		  for i in range(0,int(nfile)):
			self.infofile=[]
			self.infofile = self.sock.recv(119)
			filemd5=self.infofile[:16]
			filename=self.infofile[16:116]
			numbercp = self.infofile[116:119]
			print self.infofile[16:116]+"  "+self.infofile[116:119]
			for j in range(0,int(numbercp)):
				ipport = self.sock.recv(20)
				rs=ResultFile(filemd5,filename,ipport[:15],ipport[15:20])
				
			self.resultfiles.append(rs)
		  for i in range(0,len(self.resultfiles)):
			rs=self.resultfiles[i]
			print "%d %s %s:%s" %(i,rs.filename,rs.ip,rs.porta)
		return self.resultfiles
		self.sock.close()
	#download

	def download(self,i):
	    
            rs=self.resultfiles[int(i)]
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
	   		lenchunk = self.download.recv(5)
			print lenchunk
		    	chunk = self.download.recv(int(lenchunk)) 
		    	if not chunk: break
			ack = "ok"
			return ack
	    		f1.write(chunk)
	        f1.close()
	        self.download.close()
	    else: 
		print "errore nel download prova a scaricare di nuovo"
		ack = "no"
		return ack
	    self.open_socket()
	    ip_P2P_noform = self.ip_P2P.split(".")
	    ip_p2p1= "%(#)03d" %{"#":int(ips_P2P_noform[0])}  
	    ip_p2p2 ="%(#)03d" %{"#":int(ips_P2P_noform[1])} 
	    ip_p2p3 ="%(#)03d" %{"#":int(ips_P2P_noform[2])} 
	    ip_p2p4 ="%(#)03d" %{"#":int(ips_P2P_noform[3])} 
	    
	    IP_P2P = ip_p2p1 +"."+ ip_p2p2 +"."+ ip_p2p3 +"."+ ip_p2p4
	
	    PORTp2p = "%(#)05d" % {"#" : int(p2p_port)}
	    segnaladown = "RREG"+self.sessionID+self.md5down+IPp2p+PORTp2p
	    print "invio"+segnaladown
	    self.sock.send(segnaladown+"\n")
	 
	    acksegndown = self.sock.recv(4)
	    if acksegdown == "ARRE":
		ndown = self.sock.recv(5)
		print "numero di download:"+ ndown+"\n"
	    else:
		print "download not available"
	    self.sock.close()
