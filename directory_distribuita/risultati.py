
class ResultFile(object):
	def __init__(self,num,Md5,filename,ip,port):
		self.Md5=Md5
		self.filename=filename
		self.ip=ip
        self.num=num
        self.port=port


class List(object):
    def __init__(self,IP,filename):
        self.IP=IP
        self.filename=filename
	
