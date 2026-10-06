# Atlas

A country word-chain game. Name a country that starts with the last letter of the previous one (India → Argentina → Austria...). No repeats. Play solo against a bot or with 3 to 6 friends over a network.

## Requirements

- Python 3
- `countries.bin` in the same folder as `atlas.py` (run `git pull` if it's missing)

## Play solo

```
python atlas.py solo
```

Pick a starting letter, then trade countries with the bot. If either side can't name a valid country, the other wins. Ctrl+C to quit.

## Play multiplayer

**1. One person hosts:**

```
python atlas.py host 4
```

The number is how many players (3 to 6). The game starts once exactly that many have joined. To set the time per turn (default 30 seconds), add it at the end:

```
python atlas.py host 4 45
```

**2. Everyone joins (including the host, in a second terminal):**

```
python atlas.py join <host-ip>
```

The host joins with `python atlas.py join 127.0.0.1`.

**3. Play.** The server announces whose turn it is and the letter to use. When you see `>`, type a country and press Enter.

## Rules

- A country must start with the current letter and can't be used twice.
- A wrong guess lets you retry, but the clock keeps running.
- You're eliminated if you run out of time, disconnect, or there are no countries left for your letter.
- If a letter runs out of countries, that player is eliminated and a new letter is picked.
- Eliminated players stay connected and watch the rest of the game.
- Last player standing wins.

## Networking

- The game uses port **5000**.
- Same Wi-Fi/LAN: players join with the host's local IP (e.g. `192.168.x.x`).
- Over the internet: port forwarding usually doesn't work behind CGNAT, so use something like Tailscale or ngrok (TCP) and share that address instead.
- If you're eliminated while stuck on the input prompt, you'll see the message after you press Enter.