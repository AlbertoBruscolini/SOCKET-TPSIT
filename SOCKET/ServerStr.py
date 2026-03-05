import socket

# ES2 - ServerStr.py  (pag. 186-187)

# --- attendi ---
print("1 SERVER partito in esecuzione ...")
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 6789))
    server.listen(1)
    client, _ = server.accept()
    server.close()                          # chiude per inibire altri client
    inDalClient    = client.makefile('r')
    outVersoClient = client.makefile('wb')
except Exception as e:
    print(str(e))
    print("Errore durante l'istanza del server!")
    exit(1)

# --- comunica ---
try:
    print("3 benvenuto client, scrivi una frase e la trasformo in maiuscolo. Attendo ...")

    stringaRicevuta = inDalClient.readline().rstrip('\n')
    print("6 ricevuta la stringa dal cliente : " + stringaRicevuta)

    stringaModificata = stringaRicevuta.upper()
    print("7 invio la stringa modificata al client ...")
    outVersoClient.write((stringaModificata + '\n').encode())
    outVersoClient.flush()

    print("9 SERVER: fine elaborazione ... buona notte!")
    client.close()

except Exception as e:
    print(str(e))
    print("Errore durante la comunicazione!")
    exit(1)