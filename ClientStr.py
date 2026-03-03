import socket, sys

class ClientStr:
    def __init__(self):
        self.nome_server  = "localhost"
        self.porta_server = 6789
        self.miosocket    = None
        self.out_verso_server = None
        self.in_dal_server    = None

    def connetti(self):
        print("2 CLIENT partito in esecuzione ...")
        try:
            self.miosocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.miosocket.connect((self.nome_server, self.porta_server))
            self.out_verso_server = self.miosocket.makefile('wb')
            self.in_dal_server    = self.miosocket.makefile('r')
        except ConnectionRefusedError:
            print("Connection refused: connect")
            print("Errore durante la connessione!")
            sys.exit(1)

    def comunica(self):
        try:
            print("4 ... inserisci la stringa da trasmettere al server: ", end='')
            stringa_utente = input()
            print("5 ... invio la stringa al server e attendo ...")
            self.out_verso_server.write((stringa_utente + '\n').encode())
            self.out_verso_server.flush()
            stringa_ricevuta = self.in_dal_server.readline().rstrip('\n')
            print("8 ... risposta dal server +'" + stringa_ricevuta + "'")
            print("9 CLIENT: termina elaborazione e chiude connessione")
            self.miosocket.close()
        except Exception as e:
            print(str(e))
            sys.exit(1)

def main():
    c = ClientStr()
    c.connetti()
    c.comunica()

if __name__ == "__main__":
    main()