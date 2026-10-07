#!/usr/bin/env python3
"""
Fabrique un fichier MP3 par mot anglais de words.json.

Lancé automatiquement par GitHub à chaque modification de words.json.
Les fichiers déjà présents ne sont pas refaits : seuls les nouveaux mots
coûtent du temps.
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

# Voix britannique. Mettre "com" pour l'accent américain, "com.au" pour l'australien.
TLD = "co.uk"


def slug(word):
    """Doit produire exactement le même résultat que la fonction slug() de index.html."""
    return re.sub(r"(^-|-$)", "", re.sub(r"[^a-z0-9]+", "-", word.lower()))


def spoken(word):
    """'to run' se prononce mieux que 'to run' lu tel quel ? On garde tel quel.
    En revanche on retire les articles anglais isolés en tête pour les noms,
    sauf s'ils font partie du sens."""
    return word


def main():
    with open(WORDS, encoding="utf-8") as f:
        data = json.load(f)

    words = []
    for level in data.values():
        for entry in level:
            words.append(entry["en"])

    # dédoublonnage en conservant l'ordre
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
            gTTS(spoken(word), lang="en", tld=TLD).save(path)
            made += 1
            print("voix créée : %s" % word)
            time.sleep(0.5)  # on reste poli avec le service
        except Exception as exc:  # noqa: BLE001
            failed.append((word, str(exc)))
            if os.path.exists(path) and os.path.getsize(path) == 0:
                os.remove(path)

    # ménage : on supprime les voix dont le mot a disparu de la liste
    wanted = {slug(w) + ".mp3" for w in unique}
    removed = 0
    for name in os.listdir(OUT):
        if name.endswith(".mp3") and name not in wanted:
            os.remove(os.path.join(OUT, name))
            removed += 1

    print(
        "\n%d voix créées, %d déjà présentes, %d supprimées, %d en échec"
        % (made, skipped, removed, len(failed))
    )
    for word, err in failed:
        print("  échec : %s -> %s" % (word, err[:120]))

    # Un échec isolé ne doit pas bloquer la publication : l'app retombe sur la
    # voix du téléphone pour ce mot-là. On n'échoue que si tout a échoué.
    if failed and made == 0 and skipped == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
