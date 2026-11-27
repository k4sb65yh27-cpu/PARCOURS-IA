# Parcours IA

Application d'auto-formation à l'usage des assistants d'IA (Claude, ChatGPT, Copilot, Le Chat, Gemini) pour tout salarié. Profil choisi à l'ouverture (juriste, chargé de transfert, ingénieur brevet, fonctions support et direction) : il fixe la voie Métier et les exemples. Chemin d'étapes en trois voies (Socle, Métier, Expert), leçons courtes avec vies, examens à 80 %, révision espacée (1, 2, 4, 8, 16 jours), défi du jour, actualité de la semaine, tuteur socratique à copier dans l'assistant, glossaire de 69 termes avec recherche et filtre par thème. Sur un serveur SATT, classement facultatif des points d'XP entre volontaires (désactivé par défaut, voir `server/GUIDE_INSTALLATION.md`). Mascotte : le symbole SATT Sud-Est. Installable (PWA) sur PC et téléphone, utilisable hors ligne.

- Version publique (GitHub Pages) : sans compte, la progression reste dans le navigateur ; export et import dans Profil.
- Version serveur SATT : avec `config.json` et l'API PHP de `server/`, la progression suit le compte sur tous les appareils. Voir `server/GUIDE_INSTALLATION.md` et `sh scripts/package-server.sh <sortie.zip>`.

Exercices sur documents fictifs ou publics uniquement.

## Développement

```bash
npm install
npm run dev      # serveur local
npm run build    # version de production dans dist/
```

Pile : React, Vite, Tailwind CSS, shadcn/ui, Magic UI (NumberTicker, Confetti, BlurFade), Motion, vite-plugin-pwa. Sons synthétisés avec Web Audio (`src/lib/sound.ts`). Contenu : sources dans `scripts/content/*.py` (`profils.py` pour les profils et les variantes par métier, `metier_profils.py` pour les voies Métier hors juriste, `source_v2.json` pour le texte d'origine des étapes Expert, `socle_plus.py` pour S11 et S12, `glossaire.py` pour le glossaire, `revisions.py` pour les révisions appliquées au texte figé : skills, défis, exercices facultatifs), `python3 scripts/content/build.py` régénère `src/data/content.json` et contrôle le biais de longueur des réponses ; `python3 scripts/check-profils.py` compte les termes juridiques visibles par profil. Référence de design : `DESIGN.md`.

Contrôle : `node scripts/check-lesson.cjs <dossier> http://localhost:4173/ src/data/content.json` joue une leçon sans faute et affiche les erreurs de page (tableau vide attendu).

## Publication

Le workflow `.github/workflows/pages.yml` publie `dist/` sur GitHub Pages à chaque envoi sur `main`. Dans les réglages du dépôt : Settings, Pages, Source : GitHub Actions.
