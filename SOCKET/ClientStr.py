import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 5000))

messaggio = input("Inserisci messaggio: ")
s.send(messaggio.encode())

risposta = s.recv(1024).decode()
print("Risposta:", risposta)

s.close()
