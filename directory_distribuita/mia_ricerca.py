
    #TODO passare Pktid e poi cancellarlo passati i 300 secondi
    #TODO provare se funziona il ciclo
    listaRisultati = []
def my_research (self):

    stringa = raw_input("""Cosa vuoi cercare ??  : """)
    for i in range(100-len(stringa)) :
        stringa=stringa+" "
    #print stringa
    PKtid_send=random.randint(0,99999)
    TTLnoform = 4
    TTL= "%(#)02d" %{"#":int(TTLnoform)}
    #"QUER"[4B].PKtid[16B].IPP2P[15B].PP2P[5B].TTL[2B].Ricerca[20B]
    pacchetto="QUER"+str(PKtid_send)+myIp+myport+str(TTL)+stringa
    srcSocket = socket(AF_INET, SOCK_STREAM)
    try:

        for i in range(len(listaIpPeer)) :

            errore=srcSocket.connect_ex((listaIpPeer[i],myPort))
            if errore==0 :
                srcSocket.send(pacchetto)
                self.PKtid_send = PKtid
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
        PKtid_send = 0


    except Exception,ex :
        print ex