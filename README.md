# Word Rocket

Apprentissage de l'anglais pour deux joueurs, avec prononciation fiable.

## Mise en ligne, une fois pour toutes

1. Sur **github.com**, créer un dépôt public nommé `wordrocket`.
2. Déposer le contenu de ce dossier à la racine du dépôt (bouton **Add file → Upload files**,
   puis glisser tous les fichiers *et* les dossiers `tools` et `.github`).
3. Onglet **Settings → Pages** : dans *Source*, choisir **Deploy from a branch**,
   branche `main`, dossier `/ (root)`. Enregistrer.
4. Deux minutes plus tard, l'application est à l'adresse
   `https://<votre-nom>.github.io/wordrocket/`.
5. Sur l'iPhone, ouvrir cette adresse dans Safari, puis **Partager → Sur l'écran d'accueil**.

## Les voix

Elles se fabriquent toutes seules. Au premier dépôt des fichiers, GitHub lance la
génération : un MP3 par mot, déposé dans le dossier `audio/`. Comptez trois à quatre
minutes pour les deux cents mots. L'avancement est visible dans l'onglet **Actions**.

En attendant que les fichiers existent, l'application lit les mots avec la voix du
téléphone — c'est le comportement de secours, pas le comportement normal.

### Ajouter des mots

Ouvrir `words.json` sur GitHub, cliquer sur le crayon, ajouter une ligne :

```json
{"en": "a lighthouse", "fr": "un phare", "cat": "En ville"},
```

Enregistrer. Les voix des nouveaux mots sont fabriquées automatiquement dans la minute,
et les mots retirés voient leur fichier supprimé. Rien à installer, rien à lancer.

### Changer d'accent

Dans `tools/generate_audio.py`, la ligne `TLD = "co.uk"` donne l'accent britannique.
`"com"` donne l'américain, `"com.au"` l'australien. Après modification, lancer
**Actions → Fabriquer les voix → Run workflow**, puis supprimer le dossier `audio/`
pour forcer la refabrication complète.

## Les cinq modes

| Mode | Ce qu'il travaille |
|---|---|
| Entraînement | Dix mots, anglais → français et français → anglais en alternance |
| Oreille | Le mot est seulement entendu, jamais écrit |
| Chrono | Soixante secondes, le plus de mots possible |
| Paires | Mémoire et association des deux langues |
| Duel | Les deux joueurs alternent sur le même téléphone, chacun à son niveau |

## La révision espacée

Chaque mot progresse dans cinq cases. Une bonne réponse le fait monter d'une case et
repousse sa révision à 1, 3, 7 puis 16 jours. Une erreur le ramène à la première case.
L'application ne pose donc plus les mots déjà acquis, et fait revenir ceux qui vacillent :
c'est ce qui évite de tourner en rond.

Un mot est compté comme maîtrisé à partir de la quatrième case.

## Fichiers

```
index.html                     l'application
words.json                     la liste de mots (le seul fichier à modifier)
tools/generate_audio.py        fabrication des voix
.github/workflows/voix.yml     déclenchement automatique
audio/                         créé automatiquement
```
