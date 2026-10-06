import zlib, random as r, socket as k, sys, time
PR, Tm = 5000,30

try:
    with open("countries.bin", "rb") as f:
        decompressed = zlib.decompress(f.read()).decode("utf-8")
    countries_set = {c.strip().lower() for c in decompressed.split("|") if c.strip()}
except FileNotFoundError:
    sys.exit("countries.bin not found.")

def available(letter,used):
    return [c for c in countries_set if c.startswith(letter) and c not in used]
def say(ps,m):
    for p in ps:
        try: p[1].sendall((m+"\n").encode())
        except: pass
def solo():
    used = set()
    while True:
        letter = input("Enter the starting letter:").strip().lower()
        if len(letter) == 1 and available(letter,used): break
        print("Pick a letter that has countries")
    print("\n ==== ATLAS ====\n")
    while True:
        try: guess = input(f"Enter a country starting with '{letter.upper()}':").strip().lower()
        except (KeyboardInterrupt, EOFError): print("\nGoodbye"); break
        if not guess.startswith(letter) or guess not in countries_set or guess in used:
            print("Invalid or used country. Try again."); continue
        used.add(guess); letter = guess[-1]
        candidates = available(letter,used)
        if not candidates: print("No more countries available. You win!"); break
        bot_guess = r.choice(candidates); used.add(bot_guess); letter = bot_guess[-1]
        print(f"Bot's turn: {bot_guess.title()}")
        if not available(letter,used): print("No more countries available. Bot wins!"); break

def host(n, t):
    s = k.socket(); s.setsockopt(k.SOL_SOCKET, k.SO_REUSEADDR, 1); s.bind(("", PR)); s.listen(n)
    players = []
    for i in range (n):
        c, _ = s.accept();
        players.append((f"Player {i+1}", c, c.makefile("r")))
        say(players, f"Player {i+1} has joined, ({i+1}/{n})")
    allp, used, i = players[:], set(), 0
    letter = r.choice(sorted({c[0] for c in countries_set}))
    while len(players) > 1:
        name, c, f = players[i]
        say(allp, f"\nIt's {name}'s turn. Current letter: '{letter.upper()}'")
        guess, end, why = None, time.time() + t, f"No countries left for '{letter.upper()}'"
        if available(letter, used):
            try:
                while not guess:
                    c.settimeout(max(.1, end - time.time()))
                    c.sendall(b">\n")
                    line = f.readline()
                    if not line: raise EOFError
                    g = line.strip().lower()
                    if g.startswith(letter) and g in countries_set and g not in used: guess = g
                    else: c.sendall(b"Invalid or used country. Try again.\n")
            except (EOFError, OSError):
                why = "timed out or left"
        if guess:
            used.add(guess); letter = guess[-1]
            say(allp, f"{name} guessed '{guess.title()}'")
            i +=1
        else:
            say(allp, f"{name} {why}. Eliminated.")
            players.pop(i)
            if not available(letter, used):
                letter = r.choice(sorted({c[0] for c in countries_set-used}))
        i %= len(players)
    say(allp, f"\n{players[0][0]} wins!")

def join(ip):
    s = k.create_connection((ip, PR), timeout=20)
    for line in s.makefile("r"):
        line = line.rstrip()
        if line != ">": print(line); continue
        try: s.sendall((input(">")+ "\n").encode())
        except (KeyboardInterrupt, EOFError): break
if __name__ == "__main__":
    a = sys.argv[1:]
    if a == ["solo"]: solo()
    elif a[:1] == ["host"] and 2 <= len(a) <= 3 and a[1] in ("3", "4", "5", "6") and (len(a) == 2 or a[2].isdigit() and int(a[2]) > 0):
        host(int(a[1]), int(a[2]) if len(a) == 3 else Tm)
    elif len(a) == 2 and a[0] == "join": join(a[1])
    else: print("usage: atlas.py solo | host <3-6> [seconds] | join <ip>")