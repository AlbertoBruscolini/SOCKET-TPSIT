import socket, random, sys

# Uso: python mettiti_alla_prova_es2.py [server_v | client_v | server_c | client_c | server_b | client_b]

VOCALI = set('aeiouAEIOU')
modo = sys.argv[1] if len(sys.argv) > 1 else ''

def crea_server():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('', 6789)); srv.listen(1)
    cli, _ = srv.accept(); srv.close()
    return cli, cli.makefile('r'), cli.makefile('wb')

def crea_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 6789))
    return s, s.makefile('r'), s.makefile('wb')

# ── Mettiti alla prova pag.188: vocali e consonanti ──────────────────────────
if modo == "server_v":
    print("SERVER Vocali in attesa...")
    cli, inp, out = crea_server()
    while True:
        riga = inp.readline().rstrip('\n')
        if not riga: break
        v   = sum(1 for c in riga if c in VOCALI)
        con = sum(1 for c in riga if c.isalpha() and c not in VOCALI)
        r = f"vocali={v} consonanti={con}"
        print("SERVER: " + r)
        out.write((r + '\n').encode()); out.flush()
    cli.close()

elif modo == "client_v":
    s, inp, out = crea_client()
    while True:
        frase = input("Inserisci frase: ")
        out.write((frase + '\n').encode()); out.flush()
        r = inp.readline().rstrip('\n'); print("Server: " + r)
        p = dict(x.split('=') for x in r.split())
        if int(p['consonanti']) and int(p['vocali']) == int(p['consonanti']) // 2:
            print("vocali == consonanti/2 → Fine!"); break
    s.close()

# ── Esercizio 1: Calcolatrice ─────────────────────────────────────────────────
elif modo == "server_c":
    print("SERVER Calcolatrice in attesa...")
    cli, inp, out = crea_server()
    while True:
        riga = inp.readline().rstrip('\n')
        if not riga or riga.upper() == 'FINE': break
        try:
            t = riga.split(); a, op, b = float(t[0]), t[1], float(t[2])
            res = {'+': a+b, '-': a-b, '*': a*b, '/': a/b if b else None}.get(op)
            r = str(res) if res is not None else "ERRORE: divisione per zero"
        except Exception:
            r = "ERRORE: usa il formato   num op num   (es: 3 + 5)"
        print("SERVER: " + r)
        out.write((r + '\n').encode()); out.flush()
    cli.close()

elif modo == "client_c":
    s, inp, out = crea_client()
    print("Calcolatrice  |  formato: 3 + 5  |  FINE per uscire")
    while True:
        riga = input("> ")
        out.write((riga + '\n').encode()); out.flush()
        if riga.upper() == 'FINE': break
        print("= " + inp.readline().rstrip('\n'))
    s.close()

# ── Esercizio 3: Bomba a orologeria ──────────────────────────────────────────
elif modo == "server_b":
    print("SERVER Bomba in attesa...")
    cli, inp, out = crea_server()
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

elif modo == "client_b":
    s, inp, out = crea_client()
    r = inp.readline().rstrip('\n')
    if 'BOOM' in r: print(r); s.close(); exit()
    miccia = int(r); print(f"CLIENT: miccia={miccia}")
    while True:
        miccia -= random.randint(1, 3)
        print(f"CLIENT: riduco a {miccia}")
        out.write((str(miccia) + '\n').encode()); out.flush()
        r = inp.readline().rstrip('\n')
        if 'BOOM' in r: print(r); break
        miccia = int(r); print(f"CLIENT: ricevuto miccia={miccia}")
    s.close()

else:
    print("Uso: python mettiti_alla_prova_es2.py [server_v|client_v|server_c|client_c|server_b|client_b]")