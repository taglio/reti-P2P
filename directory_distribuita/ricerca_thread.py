import socket
import sys
import hashlib
import threading
import os
import re

class ricerca_thread(threading.Thread):

    def __init__ (self,stringToSearch,IPP2P,PP2P,PKtid):

        threading.Thread.__init__(self)
        self.stringToSearch=stringToSearch
        self.IPP2P=IPP2P
        self.PP2P=PP2P
        self.PKtid=PKtid
        self.file_search=[]

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

    def search_file(self,stringToSearch):
        for entry in os.listdir('/home/taglio/Scrivania'):
            if re.match(".*"+stringToSearch+".*" ,entry):
                print entry
                self.file_search.append(entry)
        return self.file_search



    def run(self):


        self.file_search=self.search_file(self.stringToSearch)
		
        
        if len(self.file_search)>0:
        
            for i in range(int(len(self.file_search))):

                try :
                    filemd5=self.md5_for_file(self.file_search[i])
					filename = "%(#)0100s" %{"#":self.file_search[i]}
					packet="AQUE"+PKtid+myIP+myport+filemd5+filename
					print "** mando pacchetto: " + pacchetto
					ack_search = socket(AF_INET, SOCK_STREAM)
					errore=ack_search.connect_ex((self.IPP2P,self.PP2P))
					if errore==0 :
                    	ack_search.send(packet)

                    
                except Exception,ex:
                    print ex

            
   

               
