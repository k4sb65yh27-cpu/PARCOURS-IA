# Parcours IA du juriste

Application d'auto-formation à l'IA générative pour un juriste en propriété intellectuelle : chemin d'étapes, leçons courtes avec vies, examens à 80 %, révision espacée (Leitner 1, 2, 4, 8, 16 jours), série journalière, sons et animations. Installable (PWA) et utilisable hors ligne.

La progression reste dans le navigateur. L'écran Profil permet de l'exporter et de l'importer (le fichier de la version claude.ai est accepté). Le tuteur IA et le coach hebdomadaire restent dans la version claude.ai.

Exercices sur documents fictifs ou publics uniquement.

## Développement

```bash
npm install
npm run dev      # serveur local
npm run build    # version de production dans dist/
```

Pile : React, Vite, Tailwind CSS, shadcn/ui, Magic UI (NumberTicker, Confetti, BlurFade), Motion, vite-plugin-pwa. Sons synthétisés avec Web Audio (`src/lib/sound.ts`). Contenu dans `src/data/content.json`. Référence de design : `DESIGN.md`.

## Publication

Le workflow `.github/workflows/pages.yml` publie `dist/` sur GitHub Pages à chaque envoi sur `main`. Dans les réglages du dépôt : Settings, Pages, Source : GitHub Actions.
