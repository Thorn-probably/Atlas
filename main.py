import zlib
import random as r
import sys

try:
    with open("countries.bin", "rb") as f:
        compressed = f.read()
    decompressed = zlib.decompress(compressed).decode("utf-8")
    countries_set = {c.strip().lower() for c in decompressed.split("|") if c.strip()}
except FileNotFoundError:
    print("countries.bin not found, please run git pull to get the latest version of it")
    sys.exit(1)

used = set()

while True:
    letter = input("Enter the starting letter: ").lower().strip()
    if len(letter) != 1 or not letter.isalpha():
        print("Enter a single letter.")
        continue
    if not any(c.startswith(letter) for c in countries_set):
        print(f"No countries start with {letter.upper()}. Pick another letter.")
        continue
    break

print("\n ===== ATLAS ===== \n")
print(f"first letter is {letter.upper()}, press ctrl+c to exit")

while True:
    try:
        guess = input(f"Enter a country starting with {letter.upper()}: ").lower().strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting the program. Goodbye!")
        break
    if not guess.startswith(letter):
        print(f" {guess.title()} does not start with {letter.upper()}. Try again.")
        continue
    if guess not in countries_set:
        print(f" {guess.title()} is not a valid country. Try again.")
        continue
    if guess in used:
        print(f" You have already guessed {guess.title()}. Try again.")
        continue
    used.add(guess)
    letter = guess[-1]
    #bot
    candidates = [c for c in countries_set if c.startswith(letter) and c not in used]
    if not candidates:
        print(f" I can't think of any country starting with {letter.upper()}. You win!")
        break
    bot_guess = r.choice(candidates)
    print(f" I choose {bot_guess.title()}. Your turn!")
    used.add(bot_guess)
    letter = bot_guess[-1]
    player_candidates = [c for c in countries_set if c.startswith(letter) and c not in used]
    if not player_candidates:
        print(f" There is no valid country starting with {letter.upper()}. I win!")
        break