import socket, sys

class ServerStr:
    def __init__(self):
        self.server = None
        self.client = None
        self.in_dal_client    = None
        self.out_verso_client = None

    def attendi(self):
        print("1 SERVER partito in esecuzione ...")
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(('', 6789))
            self.server.listen(1)
            self.client, _ = self.server.accept()
            self.server.close()   # chiude per inibire altri client (Unicast)
            self.in_dal_client    = self.client.makefile('r')
            self.out_verso_client = self.client.makefile('wb')
        except Exception as e:
            print(str(e))
            sys.exit(1)

    def comunica(self):
        try:
            print("3 benvenuto client, scrivi una frase e la trasformo in maiuscolo. Attendo ...")
            stringa = self.in_dal_client.readline().rstrip('\n')
            print("6 ricevuta la stringa dal cliente : " + stringa)
            modificata = stringa.upper()
            print("7 invio la stringa modificata al client ...")
            self.out_verso_client.write((modificata + '\n').encode())
            self.out_verso_client.flush()
            print("9 SERVER: fine elaborazione ... buona notte!")
            self.client.close()
        except Exception as e:
            print(str(e))
            sys.exit(1)

def main():
    s = ServerStr()
    s.attendi()
    s.comunica()

if __name__ == "__main__":
    main()