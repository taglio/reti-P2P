import socket,sys,time
from Napster import PEER
from Tkinter import * #interfaccia grafica
import threadfile
peer=PEER()
class Menu_Login:
    def __init__(self,master):

        frame = Frame(master, height=300, width=500)
        frame.pack_propagate(0)
        frame.pack()
	
        def My_Button_Click():
			global Login
			self.StatusLogin["text"] = peer.login() #qui ci mettero' la funzione per il login
			
			

			if self.StatusLogin["text"] != "ok":
				self.StatusLogin["text"] = "Login non effettuato, riprova"
				Login = False
			else : 
				Login = True
				self.StatusLogin["text"] = "Login effettuato, chiudere la finestra per passare al menu' principale"
				#master.destroy()
				
        self.Login = Button(frame, height=5, width=20, text="LOGIN", command=My_Button_Click)
        self.Login.pack()
        self.Login.place(x=150, y=40)
        

        self.StatusLogin = Label(frame, text="...")
        self.StatusLogin.pack({"expand":"yes", "fill":"x"})
        #self.StatusLogin.place(x=150, y=200)
        
        
        

root = Tk()

menu_login = Menu_Login(root)

root.mainloop()




class Menu:

	def __init__(self, master):
		
		self.resultfiles=[]
		frame = Frame(master, height=700, width=500) #serve per contenere altri oggetti
		frame.pack_propagate(0) 
		frame.pack()

		def My_Button_Click_Add():
			self.Status["text"] = peer.addfile(self.name.get()) 
			if self.Status["text"] == "ok":
				self.Status["text"] = "file aggiunto con successo"
			else : 				
				self.Status["text"] = "Errore nell'aggiunta del file"	

		def My_Button_Click_Remove():
			self.Status["text"] = peer.rmfile(self.name.get()) 
			if self.Status["text"] == "ok":
				self.Status["text"] = "aggiunta effettuata con successo, chiudere la finestra per passare al menu' principale"
			else : 
				self.Status["text"] = "aggiunta non effettuata, riprova"

		def My_Button_Click_Logout():
			self.Status["text"] = peer.logout() 
			if self.Status["text"] == "ok":
				self.Status["text"] = "logout effettuata con successo, si e' disconnessi"
			else : 
				self.Status["text"] = "logout non riuscito, riprova"

		def My_Button_Click_Search():
			self.resultfiles = peer.find(self.name.get()) 
			for i in range(0,len(self.resultfiles)):
				rs=self.resultfiles[i]
				self.Status["text"] = "%d %s %s:%s" %(i,rs.filename.lstrip(" "),rs.ip,rs.porta) 
			
		def My_Button_Click_Download():
			self.Status["text"] = peer.download(self.name.get()) 
			if self.Status["text"] == "ok":
				self.Status["text"] = "download effettuato con successo, chiudere la finestra per passare al menu' principale"
			else : 
				self.Status["text"] = "download non effettuata, riprova"
			
			
			
			
			
		self.name = StringVar()
		

		self.testo = Label(frame, height=3, text="SELEZIONA LA FUNZIONE DESIDERATA:", fg="red", font=("ubuntu-title",16))
		self.testo.pack()
		self.testo.grid(columnspan=3)	
			 
		self.MyInputBox = Entry(frame, textvariable=self.name)
		self.MyInputBox.pack()
		self.MyInputBox.grid(rowspan=4, column=1)

		self.aggiunta = Button(frame, height=3, width=20, text="ADD", command=My_Button_Click_Add)
		self.aggiunta.pack()
		self.aggiunta.grid(row=1, column=0)

		self.Status = Label(frame)
		self.Status.pack({"expand":"yes", "fill":"x"})
		self.Status.grid(row=2, column=2)

		self.rimozione = Button(frame, height=3, width=20, text="REMOVE",command=My_Button_Click_Remove)
		self.rimozione.pack()
		self.rimozione.grid(row=3, column=0)

		self.ricerca = Button(frame, height=3, width=20, text="SEARCH", command=My_Button_Click_Search)
		self.ricerca.pack()
		self.ricerca.grid(row=2, column=0)

		self.download = Button(frame, height=3, width=20, text="DOWNLOAD", command=My_Button_Click_Download)
		self.download.pack()
		self.download.grid(row=4, column=0)

		self.logout = Button(frame, height=3, width=20, text="LOGOUT", command=My_Button_Click_Logout)
		self.logout.pack()
		self.logout.grid(row=5, column=0)

		self.chiudi = Button(frame, height=3, width=20, text="CLOSE", command=frame.quit)
		self.chiudi.pack()
		self.chiudi.grid(row=5, column=2)




root = Tk()

menu = Menu(root)

root.mainloop()

if __name__ == "__main__":
	
	ciao=Menu_Login()
	if Login == True:
		tuamamma=Menu()
	


