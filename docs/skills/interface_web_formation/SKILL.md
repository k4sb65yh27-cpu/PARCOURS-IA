---
name: interface_web_formation
description: "Concevoir, adapter ou relire l'interface d'une application web de formation ou d'apprentissage gamifié (PWA type Duolingo, parcours d'étapes, quiz, révision espacée, glossaire, tableau de progression) pour qu'elle soit juste au téléphone, à la tablette et sur un grand écran de bureau. À utiliser dès qu'un écran de ce type est créé ou modifié, dès qu'on signale un affichage « comme un mobile étiré », de grands vides sur ordinateur, une navigation peu pratique au clavier ou à la souris, ou un aspect généré par IA, même si le mot « responsive » n'est pas employé. Synthèse de frontend-design, html-soigne, pages-html-sobres, animation-ludique-pwa et ui-ux-pro-max ; ne remplace pas la référence de design propre au projet (DESIGN.md)."
---

# Interface web de formation

Une application de formation se consulte au téléphone dans un couloir et sur un écran de 24 pouces au bureau. La même colonne de 576 px centrée dans 1920 px laisse 70 % de l'écran vide : l'apprenant ne voit ni son objectif du jour ni ce qui l'attend. Ce skill fixe la mise en page par largeur, le plancher de finition et le contrôle mesuré.

## 1. Ordre de priorité

1. La demande explicite de l'utilisateur.
2. La référence de design du projet (DESIGN.md, charte, jetons existants). Ne pas changer couleurs, polices, rayons ni relief déjà retenus.
3. Ce skill.

Une règle d'ici contredite par les niveaux 1 ou 2 cède. Le signaler en une ligne dans la livraison.

## 2. Mise en page par largeur

Principe : aux grandes largeurs, on ajoute des colonnes utiles, pas de la longueur de ligne. La mesure du texte reste entre 65 et 75 caractères ; ce qui grandit, c'est le nombre de zones.

| Largeur | Navigation | Zones | Remarques |
|---|---|---|---|
| moins de 768 px | barre d'état en haut, barre d'onglets en bas (5 onglets au plus) | une colonne, gouttière 16 px | action principale pleine largeur, au pouce |
| 768 à 1023 px | identique au mobile | une colonne plafonnée vers 640 px | les listes passent en deux colonnes si chaque élément reste lisible |
| 1024 à 1279 px | navigation latérale fixe (220 à 240 px), libellés visibles ; plus de barre du bas | navigation + contenu ; la barre d'état reste en haut du contenu | le contenu prend la largeur restante, plafonnée vers 960 px |
| 1280 px et plus | navigation latérale | navigation + contenu + colonne d'accompagnement (300 à 340 px) | la colonne de droite reprend ce que la barre d'état montrait, en plus complet |

Colonne d'accompagnement : ce que l'apprenant consulte souvent sans changer d'écran. Objectif du jour et sa jauge, série, XP, questions à revoir avec le bouton qui lance la révision, étape en cours avec le bouton qui la reprend. Les chiffres s'y lisent en liste à deux colonnes (libellé, valeur), jamais en cartes de statistiques alignées.

Par type d'écran, au-delà de 1024 px :
- Chemin d'étapes : reste une colonne centrée (le serpentin perd son sens au-delà de 600 px). L'espace gagné va aux colonnes latérales.
- Liste de consultation (glossaire, bibliothèque) : grille de deux colonnes, cartes alignées en haut ; recherche et filtres sur toute la largeur du contenu.
- Tableau de bord personnel (profil, révision) : panneaux répartis sur deux colonnes, titre de page sur toute la largeur.
- Séance (leçon, quiz, examen) et lecture de notions : plein écran, colonne étroite centrée, sans navigation. La concentration prime sur la densité.
- Feuilles et tiroirs ouverts du bas : sur bureau, largeur plafonnée (480 à 560 px) et centrés, pas étirés sur tout l'écran.

Éléments collants : une barre collante sous la barre d'état mobile se cale à `top: 0` dès que cette barre disparaît. Les colonnes latérales sont `position: sticky; top: 0; height: 100dvh` avec défilement interne si besoin.

## 3. Grammaire de l'apprentissage gamifié

- Une seule couleur d'action par écran ; la couleur de récompense est réservée aux gains (XP, série, objectif atteint).
- Bouton en relief (bordure inférieure plus foncée écrasée au toucher), sans ombre colorée ni halo.
- Retour de réponse en 150 à 250 ms : bandeau de correction qui monte du bas ; erreur par une secousse courte, jamais un clignotement. Le rouge et le vert ne portent jamais seuls l'information : icône et libellé en plus.
- Une célébration par écran (fin de leçon, déblocage), 1,5 s au plus, interruptible.
- Sons synthétisés, courts, désactivables d'un geste visible dès la première séance.
- Progression montrée comme un objet (chemin, jauge, boîte de révision), pas décrite en paragraphes.

## 4. Plancher de finition

Accessibilité et interaction
- `<button>` pour une action, `<a>` pour une navigation ; onglets de navigation avec `aria-current="page"` ; une seule navigation principale active à la fois dans l'arbre d'accessibilité (l'autre est masquée par `display: none`, pas seulement visuellement).
- Focus visible partout (`:focus-visible`), jamais retiré sans remplacement. Au bureau, tout se fait au clavier : ordre de tabulation navigation, contenu, colonne de droite.
- Cibles de 44 px au moins en tactile ; au bureau, états de survol sur tout ce qui est cliquable, sans dépendre du survol pour comprendre.
- Mises à jour annoncées (`aria-live="polite"`) : score, nombre de résultats d'une recherche.
- Contraste 4,5:1 pour le texte courant, 3:1 pour le grand texte, vérifié en clair et en sombre.

Typographie française
- Espace insécable avant `: ; ! ?` et dans les ensembles (`10 000 XP`, `S 12` si le projet l'écrit ainsi), guillemets « », apostrophe ’, points de suspension en un caractère.
- `text-wrap: balance` sur les titres, chiffres tabulaires dans les compteurs et listes de valeurs.
- Casse de phrase partout ; pas de capitales espacées pour décorer (sauf si la référence du projet les impose, par exemple sur les boutons en relief).

Mouvement
- Animer `transform` et `opacity` ; jamais `transition: all`.
- Tout est coupé sous `prefers-reduced-motion: reduce`.
- Pas d'apparition section par section au défilement.

PWA
- Premier écran sous 250 ko de JavaScript compressé quand c'est possible ; bibliothèques lourdes chargées à la demande.
- Hors connexion : le dernier état reçu reste lisible et daté.

## 5. Interdits (aspect généré par IA)

- Police Inter par défaut, dégradés décoratifs (violet surtout), boutons lumineux ou à bordure animée.
- Titre serif avec un mot en italique ; un mot isolé en couleur dans un titre.
- Quatre cartes de statistiques côte à côte (ni trois, ni cinq pour contourner).
- Grille de cartes identiques « icône, titre, trois lignes » comme ossature d'écran.
- Emoji ou glyphe Unicode comme icône ; une seule famille d'icônes, trait uniforme, `currentColor`.
- Chiffre, témoignage ou exemple inventé : ce qui manque reste `[à compléter]`.

## 6. Méthode

1. Lire la référence de design du projet et le composant de mise en page racine (souvent `App`).
2. Mesurer avant : `node scripts/controle_largeurs.cjs <url> <dossier> --largeurs 375,768,1024,1280,1440,1920 [--prep prep.cjs]`. Noter la couverture du premier écran par largeur.
3. Modifier la mise en page racine d'abord (navigation latérale, colonne de droite, plafonds), puis écran par écran avec des classes conditionnées à la largeur. Ne pas toucher au rendu mobile sauf défaut constaté : les tests mobiles existants doivent rester verts.
4. Mesurer après, avec les mêmes largeurs, et regarder chaque capture. Cibles indicatives : aucun débordement, aucune erreur, couverture d'au moins 70 % du premier écran à 1280 px et plus, rendu à 375 px inchangé.
5. Relancer les tests du projet (parcours mobile, profils, synchronisation).
6. Livrer avec : tableau avant et après, captures, liste de ce qui n'a pas été vérifié (navigateurs autres que Chromium, écrans tactiles réels, lecteur d'écran).

La couverture mesure l'occupation horizontale du premier écran, pas la qualité. Une page à 90 % peut être confuse : la capture tranche.

## Références

- `references/sources.md` : les cinq skills sources, ce qui en est repris, licences.
- `scripts/controle_largeurs.cjs` : captures et mesures (débordement, couverture, cibles, erreurs) en clair et en sombre.
