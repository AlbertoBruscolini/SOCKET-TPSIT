import socket, random, sys

VOCALI = set('aeiouAEIOU')

# --- Mettiti alla prova: vocali/consonanti ---
class ServerVocali:
    def avvia(self):
        srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('', 6789)); srv.listen(1)
        print("SERVER Vocali in attesa...")
        cli, _ = srv.accept(); srv.close()
        inp = cli.makefile('r'); out = cli.makefile('wb')
        while True:
            riga = inp.readline().rstrip('\n')
            if not riga: break
            v = sum(1 for c in riga if c in VOCALI)
            con = sum(1 for c in riga if c.isalpha() and c not in VOCALI)
            r = f"vocali={v} consonanti={con}"
            print("SERVER: " + r)
            out.write((r + '\n').encode()); out.flush()
        cli.close()

class ClientVocali:
    def avvia(self):
        s = socket.socket(); s.connect(("localhost", 6789))
        out = s.makefile('wb'); inp = s.makefile('r')
        while True:
            frase = input("Frase: ")
            out.write((frase + '\n').encode()); out.flush()
            r = inp.readline().rstrip('\n'); print("Server: " + r)
            p = dict(x.split('=') for x in r.split())
            if int(p['consonanti']) != 0 and int(p['vocali']) == int(p['consonanti']) // 2:
                print("Fine! vocali == consonanti/2"); break
        s.close()

# --- Esercizio 1: Calcolatrice ---
class ServerCalc:
    def avvia(self):
        srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('', 6789)); srv.listen(1)
        print("SERVER Calcolatrice in attesa...")
        cli, _ = srv.accept(); srv.close()
        inp = cli.makefile('r'); out = cli.makefile('wb')
        while True:
            riga = inp.readline().rstrip('\n')
            if not riga or riga.upper() == 'FINE': break
            try:
                t = riga.split(); a, op, b = float(t[0]), t[1], float(t[2])
                r = {'+': a+b, '-': a-b, '*': a*b, '/': a/b if b else None}.get(op)
                risposta = str(r) if r is not None else "ERRORE"
            except Exception:
                risposta = "ERRORE formato"
            out.write((risposta + '\n').encode()); out.flush()
        cli.close()

class ClientCalc:
    def avvia(self):
        s = socket.socket(); s.connect(("localhost", 6789))
        out = s.makefile('wb'); inp = s.makefile('r')
        print("Calcolatrice | formato: 3 + 5 | FINE per uscire")
        while True:
            riga = input("> ")
            out.write((riga + '\n').encode()); out.flush()
            if riga.upper() == 'FINE': break
            print("= " + inp.readline().rstrip('\n'))
        s.close()

# --- Esercizio 3: Bomba a orologeria ---
class ServerBomba:
    def avvia(self):
        srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('', 6789)); srv.listen(1)
        cli, _ = srv.accept(); srv.close()
        inp = cli.makefile('r'); out = cli.makefile('wb')
        miccia = random.randint(5, 15)
        print(f"SERVER: miccia iniziale = {miccia}")
        out.write((str(miccia) + '\n').encode()); out.flush()
        while True:
            miccia = int(inp.readline().rstrip('\n'))
            print(f"SERVER: ricevuto miccia={miccia}")
            if miccia <= 0:
                out.write(b'BOOM!\n'); out.flush(); print("BOOM!"); break
            miccia -= random.randint(1, 3)
            print(f"SERVER: riduco a {miccia}")
            out.write((str(miccia) + '\n').encode()); out.flush()
        cli.close()

class ClientBomba:
    def avvia(self):
        s = socket.socket(); s.connect(("localhost", 6789))
        out = s.makefile('wb'); inp = s.makefile('r')
        r = inp.readline().rstrip('\n')
        if 'BOOM' in r: print(r); s.close(); return
        miccia = int(r); print(f"CLIENT: miccia={miccia}")
        while True:
            miccia -= random.randint(1, 3)
            print(f"CLIENT: riduco a {miccia}")
            out.write((str(miccia) + '\n').encode()); out.flush()
            r = inp.readline().rstrip('\n')
            if 'BOOM' in r: print(r); break
            miccia = int(r); print(f"CLIENT: ricevuto miccia={miccia}")
        s.close()

# Uso: python mettiti_alla_prova_es2.py [server_v|client_v|server_c|client_c|server_b|client_b]
CLASSI = {
    "server_v": ServerVocali, "client_v": ClientVocali,
    "server_c": ServerCalc,   "client_c": ClientCalc,
    "server_b": ServerBomba,  "client_b": ClientBomba,
}
if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CLASSI:
        print("Uso: python mettiti_alla_prova_es2.py [" + "|".join(CLASSI) + "]")
    else:
        CLASSI[sys.argv[1]]().avvia()