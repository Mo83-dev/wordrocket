#!/usr/bin/env python3
"""
Fabrique un fichier MP3 par mot anglais de words.json.
"""

import json
import os
import re
import sys
import time

from gtts import gTTS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = os.path.join(ROOT, "words.json")
OUT = os.path.join(ROOT, "audio")

# Voix britannique. Mettre "com" pour l'accent américain.
TLD = "co.uk"


def slug(word):
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", word.lower()))


def main():
    with open(WORDS, encoding="utf-8") as f:
        data = json.load(f)

    words = []
    for level in data.values():
        for entry in level:
            words.append(entry["en"])

    seen = set()
    unique = [w for w in words if not (w in seen or seen.add(w))]

    os.makedirs(OUT, exist_ok=True)
    made, skipped, failed = 0, 0, []

    for word in unique:
        path = os.path.join(OUT, slug(word) + ".mp3")
        if os.path.exists(path) and os.path.getsize(path) > 0:
            skipped += 1
            continue
        try:
            gTTS(word, lang="en", tld=TLD).save(path)
            made += 1
            print("voix creee : %s" % word)
            time.sleep(0.5)
        except Exception as exc:
            failed.append((word, str(exc)))
            if os.path.exists(path) and os.path.getsize(path) == 0:
                os.remove(path)

    wanted = {slug(w) + ".mp3" for w in unique}
    removed = 0
    for name in os.listdir(OUT):
        if name.endswith(".mp3") and name not in wanted:
            os.remove(os.path.join(OUT, name))
            removed += 1

    print(
        "\n%d voix creees, %d deja presentes, %d supprimees, %d en echec"
        % (made, skipped, removed, len(failed))
    )
    for word, err in failed:
        print("  echec : %s -> %s" % (word, err[:120]))

    if failed and made == 0 and skipped == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
