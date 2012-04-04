import socket,sys,time
from gnutella import PEER
#imports needed for the GUI
from Tkinter import *
import thread_gnutella
#TODO bisogna fare una specie di login che permetta di far partire la socket in ascolto
peer=PEER()
class Menu_Login:
    def __init__(self,master):

        """
          This method create the master frame, the first window for the Login, button and the label.
        """

        frame = Frame(master, height=300, width=500)
        frame.pack_propagate(0)
        frame.pack()

        def My_Button_Click():

            """
                This method defines the actions to make if key Login is pressed
            """

            global Login
            Login = False

            #call to login method
            self.StatusLogin["text"] = peer.login()
            if self.StatusLogin["text"] != "ok":
                Login = False
                self.StatusLogin["text"] = "Login non effettuato, riprova"
            else :
                Login = True
                self.StatusLogin["text"] = "Login effettuato, chiudere la finestra per passare al menu' principale"


            self.Login = Button(frame, height=5, width=20, text="LOGIN", command=My_Button_Click)
            self.Login.pack()
            self.Login.place(x=150, y=40)

            #create a Label widget as a child to the root window
            self.StatusLogin = Label(frame, text="...")
            self.StatusLogin.pack({"expand":"yes", "fill":"x"})

    #create an ordinary window
root = Tk()

menu_login = Menu_Login(root)

#TKinter event loop, the program will stay in the event loop until we close the window
root.mainloop()


class Menu:

    def __init__(self, master):

        """
          This method create the second window and all elements within it.
          """
        if Login == True:
            self.resultfiles=[]
            frame = Frame(master, height=700, width=500)
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
                self.Status["text"] = "file rimosso con successo"
            else :
                self.Status["text"] = "Errore nella rimozione del file"

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
                self.Status["text"] = "%d %s %s:%s" %(i,rs.filename.strip(" "),rs.ip,rs.porta)

        def My_Button_Click_Download():

            child_pid = os.fork() #TODO mettere a posto il figlio
            if child_pid==0:
                print "Sono il figlio che fa il downloadl"
                signal.signal(signal.SIGINT, signal.SIG_DFL)
                downloadFile(fileScelto,stringa)
                os._exit(0)	#Uscita del figlio.
            self.Status["text"] = peer.download(self.name.get())
            if self.Status["text"] == "ok":
                self.Status["text"] = "download effettuato con successo"
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






root = Tk()

menu = Menu(root)

root.mainloop()





