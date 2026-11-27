# Étapes ajoutées au Socle le 27/11/2026 (spécification v0.2.1, section 5).
# Placées après so10 : aucune étape existante n'est verrouillée par leur ajout.
from socle import mcq, tf, cloze, order, match

SOCLE_PLUS = [
 {
  "id": "so11", "cote": "S11", "titre": "Obtenir le bon résultat en un minimum d'échanges", "duree": "45 min",
  "comp": ["formuler", "dialoguer"], "cadre": 1,
  "obj": ["Écrire un brief complet dès le premier message", "Montrer le résultat attendu plutôt que le décrire", "Faire écrire ou améliorer une consigne par l'assistant"],
  "notions": [
   ["Le brief complet", "Chaque aller-retour coûte du temps et des tokens. Donnez dès le premier message l'objectif, le lecteur, la matière, le format, les limites et ce qui fera dire que le résultat est réussi. Les questions liées se regroupent dans le même message."],
   ["Montrer le résultat attendu", "Un exemple de sortie ou un gabarit (« un tableau à trois colonnes : point, risque, action ») guide mieux qu'une longue description. Quand le format est délicat, trois à cinq exemples variés valent mieux qu'un seul."],
   ["Dire quoi faire, et pourquoi", "« Écris trois paragraphes suivis » fonctionne mieux que « pas de liste ». Donnez aussi la raison d'une contrainte (« le texte sera lu à voix haute en comité ») : l'assistant en tire des choix que vous n'aviez pas écrits."],
   ["Faire écrire la consigne", "Pour une tâche qui revient, demandez : « Écris la consigne que je devrais te donner pour obtenir [résultat] ; pose-moi d'abord tes questions. » Testez la consigne obtenue sur deux cas fictifs, puis rangez-la dans votre bibliothèque."],
   ["Choisir le mode et le modèle", "Un raisonnement long (comparer des options, analyser un document dense) gagne au mode de réflexion approfondie et à un effort élevé. Une reformulation ou un tri simple se contente d'un modèle léger et d'un effort bas, plus rapides et moins gourmands."],
   ["Enchaîner sans recommencer", "Appuyez-vous sur ce qui est déjà produit : « à partir du tableau ci-dessus, rédige le courriel ». Une tâche longue se découpe en étapes contrôlées plutôt qu'en une demande unique refaite trois fois."]
  ],
  "res": [["promptbp", "Anthropic : bonnes pratiques de rédaction des consignes (en anglais)."], ["usagebp", "Anthropic : brief complet et demandes groupées pour ménager ses limites (en anglais)."]],
  "ex": [
   {"t": "Reprenez une demande qui vous a coûté plusieurs allers-retours. Réécrivez-la en un seul message complet (objectif, lecteur, matière, format, limites, critère de réussite) et relancez-la dans une nouvelle conversation.", "c": "Le carnet indique le nombre d'échanges avant et après, et ce qui manquait au premier message."},
   {"t": "Demandez à l'assistant d'écrire la consigne d'une tâche récurrente de votre poste, après vous avoir posé ses questions. Testez-la sur deux cas fictifs.", "c": "La consigne est rangée dans votre bibliothèque avec les deux résultats de test."}
  ],
  "quiz": [
   mcq("Quel premier message réduit le plus les allers-retours ?", ["« Fais-moi une note sur ce sujet, je préciserai après »", "Objectif, lecteur, matière, format, limites et critère de réussite", "Une question courte, puis une correction à chaque réponse reçue", "Trois messages séparés : d'abord le contexte, ensuite la tâche, enfin le format"], 1, "Tout donner d'emblée évite les relances et les réponses à refaire."),
   mcq("Pour obtenir un tableau d'une forme précise, le plus efficace est de :", ["Écrire « fais un beau tableau clair »", "Montrer un exemple du tableau attendu", "Demander plusieurs versions et choisir la meilleure parmi elles", "Répéter la demande jusqu'à obtenir le bon format"], 1, "Un exemple de sortie montre ce qu'une description laisse dans le flou."),
   mcq("Laquelle de ces consignes dit quoi faire plutôt que quoi éviter ?", ["Pas de liste à puces, pas de titres", "Écris trois paragraphes suivis de cinq lignes", "Évite tout ce qui ressemble à une présentation", "Ne fais surtout pas un texte trop long ni trop court"], 1, "Une consigne positive décrit le résultat ; une interdiction laisse deviner ce qui est attendu."),
   mcq("Pourquoi donner la raison d'une contrainte ?", ["Pour que l'assistant en tire des choix cohérents", "Pour allonger la consigne et la rendre plus formelle", "Parce que l'assistant refuse une consigne sans justification", "Pour que la réponse cite la contrainte mot pour mot"], 0, "Connaître le but permet d'adapter ce que la consigne ne précise pas."),
   mcq("Vous voulez seulement reformuler un courriel court. Quel réglage convient ?", ["Recherche approfondie et effort maximal", "Modèle léger et effort bas", "Mode de réflexion approfondie, pour plus de sûreté", "Le modèle le plus puissant disponible, par principe"], 1, "Une tâche simple n'a pas besoin du raisonnement le plus long : elle va plus vite et consomme moins.")
  ],
  "drills": [
   tf("Une consigne écrite par l'assistant n'a pas besoin d'être testée.", False, "Une consigne se teste sur deux ou trois cas fictifs avant d'entrer dans la bibliothèque."),
   cloze("« À partir du tableau ___, rédige le courriel » évite de tout redemander.", ["ci-dessus", "vierge", "suivant"], 0, "Réutiliser la sortie précédente fait gagner un échange."),
   match("Associez chaque besoin au bon réflexe.", [["Format précis", "Montrer un exemple de sortie"], ["Tâche qui revient", "Faire écrire la consigne"], ["Raisonnement long", "Réflexion approfondie"], ["Reformulation simple", "Modèle léger, effort bas"]], "Chaque réflexe évite une relance."),
   order("Remettez dans l'ordre la préparation d'une consigne réutilisable.", ["Décrire le résultat attendu", "Faire poser ses questions à l'assistant", "Obtenir la consigne proposée", "La tester sur deux cas fictifs", "La ranger dans la bibliothèque"], "On teste avant de ranger."),
   tf("Quand le format est délicat, trois à cinq exemples variés guident mieux qu'un seul.", True, "Des exemples variés évitent que l'assistant imite un détail sans importance.")
  ]
 },
 {
  "id": "so12", "cote": "S12", "titre": "Gérer ses tokens et ses limites d'usage", "duree": "40 min",
  "comp": ["comprendre", "organiser"], "cadre": 1,
  "obj": ["Savoir ce qui consomme des tokens", "Distinguer limite d'usage et limite de longueur", "Organiser son travail pour consommer moins"],
  "notions": [
   ["Ce qui consomme", "La consommation dépend de la longueur de vos messages et des pièces jointes, de la longueur de la conversation, des outils utilisés (recherche web, recherche approfondie), du modèle choisi, du niveau d'effort, des documents créés et des tâches en plusieurs étapes."],
   ["Deux limites différentes", "La limite d'usage fixe ce que vous pouvez faire sur une période ; chez Claude, par exemple, une limite de session qui se renouvelle toutes les cinq heures et des plafonds hebdomadaires. La limite de longueur fixe la taille d'une conversation : c'est la fenêtre de contexte."],
   ["La conversation longue", "À chaque message, l'assistant reprend l'échange entier : une conversation très longue coûte de plus en plus. Quand elle approche de la limite, certains assistants la résument automatiquement, ce qui consomme encore davantage. Repartez d'une conversation neuve avec un résumé de reprise de quelques lignes."],
   ["Projets et documents de référence", "Un document placé une fois dans un projet est mis en cache : chez Claude, il compte moins à chaque réutilisation que s'il était joint de nouveau. Le cache expire après une période d'inactivité. Retirez les fichiers devenus inutiles et gardez des instructions de projet courtes."],
   ["Régler avant d'envoyer", "Pour une tâche simple, coupez la réflexion approfondie, baissez l'effort et désactivez la recherche web et les connecteurs dont la conversation n'a pas besoin. Ces outils consomment beaucoup de tokens."],
   ["Suivre sa consommation", "Les assistants affichent votre consommation dans leurs réglages (chez Claude : Paramètres, puis Usage ; le nom du menu varie selon l'outil). Un coup d'œil avant un travail long évite d'être coupé au milieu."]
  ],
  "res": [["limits", "Anthropic : fonctionnement des limites d'usage et de longueur (en anglais)."], ["usagebp", "Anthropic : bonnes pratiques pour ménager ses limites (en anglais)."]],
  "ex": [
   {"t": "Relevez votre consommation dans les réglages de l'assistant. Menez une même tâche fictive de deux façons : en continuant une longue conversation, puis dans une conversation neuve ouverte avec un résumé de reprise. Relevez la consommation après chaque essai.", "c": "Le carnet indique les deux relevés et la façon de faire que vous retenez."},
   {"t": "Rédigez votre résumé de reprise type : sujet, décisions prises, documents utiles, prochaine étape, format attendu. Cinq lignes au plus.", "c": "Le résumé est rangé dans votre bibliothèque et a servi au moins une fois."}
  ],
  "quiz": [
   mcq("Lequel de ces éléments pèse sur la consommation ?", ["La couleur du thème de l'application", "La longueur de la conversation en cours", "L'heure à laquelle vous écrivez votre message", "Le nombre de conversations déjà archivées"], 1, "Plus l'échange est long, plus chaque message coûte."),
   mcq("Quelle est la différence entre limite d'usage et limite de longueur ?", ["Aucune : ce sont deux noms pour la même chose", "La première porte sur une période, la seconde sur une conversation", "La première concerne les fichiers, la seconde les images jointes", "La première vaut pour les offres gratuites, la seconde pour les payantes"], 1, "La limite d'usage se renouvelle dans le temps ; la limite de longueur tient à la fenêtre de contexte."),
   mcq("Votre conversation est devenue très longue. Le bon réflexe :", ["Ouvrir une conversation neuve avec un résumé de reprise", "Recoller tous les documents pour lui rafraîchir la mémoire", "Passer au modèle le plus puissant pour tenir la longueur", "Continuer : une longue conversation améliore toujours les réponses"], 0, "Le résumé relu remplace l'historique et coûte bien moins cher."),
   mcq("Vous interrogez chaque semaine le même guide interne public. Le plus économe :", ["Le joindre à chaque nouvelle conversation", "Le placer une fois dans un projet", "Le recopier par morceaux dans plusieurs messages", "Le résumer de mémoire au début de chaque échange"], 1, "Le contenu d'un projet réutilisé compte moins que le même fichier joint à chaque fois."),
   mcq("Pour trier une liste de dix titres, que désactiver ?", ["Rien : tous les outils sont gratuits", "La réflexion approfondie et la recherche web", "Le correcteur orthographique de votre navigateur web", "L'historique des conversations précédentes"], 1, "Une tâche simple n'a besoin ni d'un long raisonnement ni d'une recherche.")
  ],
  "drills": [
   tf("Une conversation très longue coûte de plus en plus à chaque message.", True, "L'assistant reprend l'échange entier à chaque réponse."),
   cloze("Un document placé dans un projet est mis en ___ et compte moins quand on le réutilise.", ["cache", "quarantaine", "brouillon"], 0, "Chez Claude, le contenu d'un projet réutilisé compte moins dans les limites."),
   match("Associez chaque situation au bon réglage.", [["Tri simple", "Effort bas"], ["Analyse d'un document dense", "Réflexion approfondie"], ["Pas besoin d'actualité", "Recherche web coupée"], ["Guide consulté chaque semaine", "Document dans un projet"]], "Régler avant d'envoyer évite de consommer pour rien."),
   order("Remettez dans l'ordre une reprise économe.", ["Demander un résumé de la conversation", "Le relire et le corriger", "Ouvrir une conversation neuve", "Coller le résumé de reprise", "Poursuivre le travail"], "Le résumé relu remplace tout l'historique."),
   tf("Désactiver les connecteurs inutiles aide à ménager ses limites.", True, "Les outils et les connecteurs consomment beaucoup de tokens.")
  ]
 }
]
