# Voie Métier : cas d'usage d'un juriste de SATT, transposables à tout poste de bureau.
# Pratique autorisée au poste, sur documents fictifs ou publics.
from socle import mcq, tf, cloze, order, match

METIER = [
 {
  "id": "me1", "cote": "M1", "titre": "Courriels et notes internes", "duree": "40 min",
  "comp": ["produire", "formuler"], "cadre": 1,
  "obj": ["Rédiger un courriel juste du premier coup", "Adapter le ton au destinataire", "Transformer des notes brutes en note interne"],
  "notions": [
   ["Le brouillon d'abord", "Donnez à l'assistant vos idées en vrac : destinataire, objectif, points à faire passer, ce qui ne doit pas être dit. Il structure ; vous gardez la main sur le fond et sur chaque engagement pris au nom de l'entreprise."],
   ["Le ton se règle", "Précisez le registre attendu : chercheur à rassurer, partenaire industriel à relancer, direction à informer. « Ferme et courtois, sans formule d'excuse » produit un résultat très différent de « chaleureux ». Donnez un ancien courriel fictif comme modèle de ton si besoin."],
   ["Note interne", "Une note se construit autour de la décision attendue : objet, contexte, analyse, options, recommandation. Demandez ce plan explicitement ; sinon l'assistant raconte au lieu de conclure."],
   ["Relire comme l'auteur", "Le courriel part sous votre nom. Relisez les dates, les noms, les montants et chaque promesse. L'assistant ajoute volontiers une formule (« nous reviendrons vers vous sous 48 h ») que personne n'a décidée."],
   ["Réponse à un courriel reçu", "Collez le courriel reçu, s'il ne contient pas de données de dossier, ou résumez-le en termes neutres. Indiquez votre position, puis demandez une réponse point par point. Vérifiez qu'aucune question du correspondant n'est restée sans réponse."]
  ],
  "res": [["skfluency", "Module Description du cours AI Fluency : décrire la tâche, le ton et le format."], ["msgenfr", "Microsoft, cours d'IA générative en français : leçon sur la rédaction."]],
  "ex": [
   {"t": "À partir de cinq lignes de notes fictives (réunion avec un laboratoire sur un projet de maturation imaginaire), faites produire un courriel de suivi, puis une version deux fois plus courte.", "c": "Les deux versions sont dans le carnet ; aucune promesse non décidée n'y figure."},
   {"t": "Faites rédiger une relance d'un partenaire fictif qui n'a pas renvoyé un accord signé, en trois tons : neutre, ferme, très ferme.", "c": "Vous savez quelle consigne a changé le ton à chaque fois."},
   {"t": "Facultatif : transformez une page de notes fictives en note interne avec recommandation.", "c": "La recommandation figure en tête et tient en trois lignes.", "opt": True}
  ],
  "quiz": [
   mcq("Que doit contenir votre demande pour un courriel de relance ?", ["Uniquement l'adresse du destinataire", "Destinataire, objectif, points et ton", "Le dossier complet en pièce jointe", "Une liste de formules de politesse"], 1, "Avec ces quatre éléments, le premier jet est presque toujours utilisable."),
   mcq("L'assistant ajoute « nous vous répondrons sous 48 h ». Que faire ?", ["Le laisser, c'est une formule usuelle", "Le retirer sauf si ce délai est décidé", "Le remplacer par une semaine", "Demander à l'assistant de le justifier"], 1, "Tout engagement envoyé sous votre nom doit avoir été décidé."),
   mcq("Quel plan demander pour une note interne ?", ["Chronologie complète des échanges", "Objet, contexte, analyse, options, recommandation", "Questions puis réponses dans l'ordre reçu", "Un paragraphe unique, sans titres"], 1, "La note sert une décision : elle doit conclure."),
   mcq("Comment obtenir le ton d'un service sans le décrire longuement ?", ["Fournir un ancien courriel fictif comme modèle", "Demander un ton professionnel", "Écrire la consigne en majuscules", "Changer d'assistant"], 0, "Un exemple de ton vaut souvent mieux qu'une description."),
   mcq("Avant d'envoyer la réponse rédigée, la vérification prioritaire est :", ["Le nombre de paragraphes", "La présence d'une formule de politesse", "Dates, noms, montants et promesses", "La longueur des phrases"], 2, "Ce sont les éléments qui engagent et que l'assistant peut altérer.")
  ],
  "drills": [
   tf("Un courriel rédigé par l'assistant peut partir sans relecture s'il est bien écrit.", False, "Il part sous votre nom : dates, noms, montants et promesses se relisent."),
   cloze("Pour un ton précis, le plus efficace est souvent de fournir un ___.", ["exemple", "glossaire", "sommaire"], 0, "Un modèle de ton guide mieux qu'un adjectif."),
   order("Remettez dans l'ordre le plan d'une note interne.", ["Objet", "Contexte", "Analyse et options", "Recommandation"], "En pratique, la recommandation peut aussi être annoncée en tête."),
   match("Associez chaque destinataire au ton le plus adapté.", [["Chercheur inquiet", "Rassurant et précis"], ["Partenaire en retard", "Ferme et courtois"], ["Direction", "Bref et orienté décision"]], "Le ton se règle dans la consigne."),
   tf("Préciser ce qui ne doit pas être dit fait partie d'une bonne consigne de courriel.", True, "Les limites évitent les formulations maladroites ou les engagements implicites.")
  ]
 },
 {
  "id": "me2", "cote": "M2", "titre": "Lire et comparer des contrats", "duree": "50 min",
  "comp": ["produire", "verifier"], "cadre": 1,
  "obj": ["Faire repérer les clauses d'un contrat public ou fictif", "Comparer deux versions", "Préparer une pré-revue sans déléguer l'avis juridique"],
  "notions": [
   ["Repérer, pas trancher", "L'assistant est rapide pour localiser : durée, confidentialité, propriété des résultats, exclusivité, responsabilité, loi applicable. L'appréciation du risque et la position à tenir restent celles du juriste."],
   ["Grille de lecture", "Donnez votre grille : liste des clauses à trouver, format attendu (tableau clause, article, extrait, remarque) et consigne de citer le texte exact. Sans grille, la lecture est générale et inégale."],
   ["Comparer deux versions", "Demandez un tableau des différences article par article, avec citation des deux rédactions. Vérifiez ensuite avec la comparaison de votre traitement de texte : l'assistant peut manquer une virgule qui change le sens."],
   ["Ce qui manque", "Demandez aussi ce qui n'y est pas : absence de clause de non-sollicitation, de durée de survie de la confidentialité, de limitation de responsabilité. Une clause absente ne se voit pas à la lecture rapide."],
   ["Documents d'entraînement", "Modèles publics (NDA type, accord de consortium type, contrats de licence publiés par des universités ou des organismes publics) ou contrats fictifs rédigés pour l'exercice. Jamais un contrat de dossier réel dans un outil non validé."]
  ],
  "res": [["legi", "Légifrance : textes de référence (Code civil, CPI) pour vérifier les renvois."], ["skfluency", "Module Discernment : évaluer la production de l'assistant."]],
  "ex": [
   {"t": "Sur un NDA type public, faites produire un tableau des clauses (objet, durée, exclusions, restitution, loi applicable) avec citation exacte.", "c": "Chaque ligne du tableau a été vérifiée contre le texte ; les écarts sont notés."},
   {"t": "Modifiez vous-même trois points d'une copie du NDA (durée, exclusion, juridiction). Demandez la comparaison des deux versions.", "c": "L'assistant a trouvé les trois modifications, ou vous savez laquelle il a manquée."},
   {"t": "Demandez la liste des clauses habituelles absentes du NDA type.", "c": "Au moins une absence pertinente est confirmée par votre propre lecture."}
  ],
  "quiz": [
   mcq("Dans une pré-revue, quel est le rôle de l'assistant ?", ["Donner la position finale à tenir", "Localiser et extraire les clauses", "Valider la conformité du contrat", "Signer à la place du juriste"], 1, "L'appréciation et la décision restent humaines."),
   mcq("Pourquoi exiger la citation exacte des clauses ?", ["Pour allonger le tableau", "Pour vérifier vite contre le texte", "Parce que l'assistant ne sait pas résumer", "Pour éviter les droits d'auteur"], 1, "La citation permet le contrôle ligne par ligne."),
   mcq("Comment fiabiliser une comparaison de versions ?", ["La faire deux fois de suite", "Demander une comparaison plus détaillée", "Recouper avec l'outil de comparaison du traitement de texte", "Comparer à la mémoire de l'assistant"], 2, "L'outil déterministe détecte chaque caractère modifié."),
   mcq("Quelle question fait apparaître ce que la lecture rapide manque ?", ["Résume ce contrat en cinq lignes", "Quelles clauses habituelles sont absentes ?", "Ce contrat est-il bien rédigé ?", "Traduis ce contrat en anglais"], 1, "Une absence ne se voit pas ; il faut la demander."),
   mcq("Sur quel document s'entraîner à la pré-revue ?", ["Le dernier NDA reçu d'un partenaire", "Un NDA réel dont le nom est masqué", "Un modèle public ou un contrat fictif", "Un contrat signé de plus de cinq ans"], 2, "Un contrat de dossier, même ancien ou masqué, ne va pas dans un outil non validé.")
  ],
  "drills": [
   tf("L'assistant peut donner la position à tenir dans une négociation à la place du juriste.", False, "Il aide à repérer et à formuler ; la position relève du juriste."),
   cloze("Pour une pré-revue exploitable, donnez à l'assistant votre ___ de lecture.", ["grille", "signature", "facture"], 0, "Liste des clauses, format et citation exacte."),
   order("Remettez dans l'ordre une pré-revue assistée.", ["Choisir un document fictif ou public", "Donner la grille de lecture", "Vérifier chaque ligne contre le texte", "Rédiger votre propre appréciation"], "La vérification précède toujours l'appréciation."),
   match("Associez chaque demande à son intérêt.", [["Citation exacte", "Contrôle rapide"], ["Clauses absentes", "Voir ce qui manque"], ["Tableau des différences", "Comparer deux versions"]], "Chaque consigne répond à un risque de lecture."),
   tf("Une comparaison faite par l'assistant peut manquer une modification d'un seul mot.", True, "D'où le recoupement avec un outil de comparaison.")
  ]
 },
 {
  "id": "me3", "cote": "M3", "titre": "Recherche et veille", "duree": "45 min",
  "comp": ["verifier", "dialoguer"], "cadre": 1,
  "obj": ["Utiliser la recherche web de l'assistant avec méthode", "Distinguer source primaire et commentaire", "Organiser une veille régulière"],
  "notions": [
   ["Deux modes", "Sans recherche web, l'assistant répond de mémoire. Avec la recherche web activée, il cite des pages consultées. Vérifiez quel mode a servi avant de vous fier à une date ou à un texte récent."],
   ["Source primaire", "Le texte officiel (Légifrance, EUR-Lex, Judilibre, INPI, OEB) fait foi. Un article de blog, un communiqué ou une synthèse d'assistant sont des commentaires : utiles pour s'orienter, insuffisants pour citer."],
   ["Ouvrir les liens", "Ouvrez chaque lien cité. Il arrive qu'une page existe mais ne dise pas ce que l'assistant lui attribue, ou qu'elle porte sur une version antérieure du texte."],
   ["Recherche approfondie", "Plusieurs assistants proposent un mode de recherche longue (« deep research » ou équivalent) qui lit des dizaines de sources et rédige un rapport. Pratique pour un état des lieux ; à vérifier comme le reste, et sans y mettre d'élément de dossier."],
   ["Veille", "Une veille utile tient en une consigne réutilisable : périmètre, sources prioritaires, période, format (titre, date, source, une phrase d'impact). Relancez-la chaque semaine dans un projet ou une conversation dédiée."]
  ],
  "res": [["legi", "Légifrance : source primaire du droit français."], ["judilibre", "Judilibre : décisions de la Cour de cassation et des juridictions judiciaires."]],
  "ex": [
   {"t": "Avec la recherche web activée, demandez les dernières évolutions d'un thème public (par exemple la réforme du crédit d'impôt recherche). Ouvrez chaque lien.", "c": "Pour chaque source, vous avez noté : primaire ou commentaire, et si elle dit bien ce qui est affirmé."},
   {"t": "Rédigez une consigne de veille hebdomadaire sur un sujet de votre métier et testez-la.", "c": "La consigne est enregistrée dans le carnet et produit une liste datée et sourcée."}
  ],
  "quiz": [
   mcq("L'assistant donne une date récente sans lien. Que supposer ?", ["Qu'il a consulté une source fiable", "Qu'il a peut-être répondu de mémoire", "Que la date est forcément exacte", "Qu'il a lu le Journal officiel"], 1, "Sans source affichée, la réponse vient peut-être de ses données d'entraînement."),
   mcq("Quelle source fait foi pour citer un article du CPI ?", ["Un blog de cabinet", "Le résumé de l'assistant", "Légifrance", "Une encyclopédie en ligne"], 2, "Le texte officiel est la source primaire."),
   mcq("Un lien cité existe bien. Est-ce suffisant ?", ["Oui, le lien prouve l'affirmation", "Non, la page doit dire ce qui est affirmé", "Oui, si le site est officiel", "Non, il faut trois liens minimum"], 1, "L'existence du lien ne prouve pas le contenu attribué."),
   mcq("Une recherche approfondie de l'assistant sert surtout à :", ["Remplacer la vérification", "Dresser un état des lieux à vérifier", "Rédiger un avis signé", "Analyser un dossier confidentiel"], 1, "Le rapport oriente ; il se vérifie comme toute réponse."),
   mcq("Que doit préciser une consigne de veille réutilisable ?", ["Le nom de l'assistant utilisé", "Périmètre, sources, période et format", "Le nombre de mots maximal seulement", "La liste des destinataires de la veille"], 1, "Ces quatre paramètres rendent la veille comparable d'une semaine à l'autre.")
  ],
  "drills": [
   tf("Un communiqué de presse est une source primaire pour citer un texte de loi.", False, "Le texte officiel fait foi ; le communiqué est un commentaire."),
   cloze("Avant de citer, ouvrez chaque ___ fourni par l'assistant.", ["lien", "onglet", "menu"], 0, "La page peut ne pas dire ce qui lui est attribué."),
   match("Classez chaque source.", [["Légifrance", "Source primaire"], ["Article de blog", "Commentaire"], ["Synthèse de l'assistant", "Point de départ à vérifier"]], "Seule la source primaire se cite."),
   order("Remettez dans l'ordre une recherche fiable.", ["Activer la recherche web", "Lire la réponse et ses sources", "Ouvrir chaque lien", "Remonter au texte officiel"], "La remontée à la source primaire clôt la recherche."),
   tf("Une consigne de veille enregistrée se relance chaque semaine sans tout réécrire.", True, "C'est le principe de la bibliothèque de consignes.")
  ]
 },
 {
  "id": "me4", "cote": "M4", "titre": "Synthèses, comptes rendus et supports", "duree": "45 min",
  "comp": ["produire", "organiser"], "cadre": 1,
  "obj": ["Produire un compte rendu à partir de notes", "Résumer un long document public", "Préparer la trame d'un support de présentation"],
  "notions": [
   ["Compte rendu", "À partir de notes brutes (jamais d'enregistrement d'une réunion confidentielle dans un outil non validé), demandez : décisions, actions avec responsable et échéance, points ouverts. Le reste est secondaire."],
   ["Résumé fidèle", "Fixez la longueur, le public et ce qui doit absolument figurer. Demandez de signaler ce qui a été omis. Un résumé élégant peut gommer une réserve ou une condition."],
   ["Tableaux", "L'assistant transforme un texte en tableau (échéancier, comparatif, matrice de risques) et inversement. Demandez les colonnes voulues ; vérifiez les chiffres recopiés."],
   ["Trame de présentation", "Demandez un plan diapositive par diapositive : titre affirmatif, trois idées au plus, visuel suggéré. La mise en forme se fait ensuite dans l'outil de présentation de l'entreprise."],
   ["Visuels", "Selon l'outil, l'assistant peut produire un schéma, un graphique ou une image. Un schéma de flux (parties, droits, échéances) se vérifie comme un texte : une flèche dans le mauvais sens est une erreur de fond."]
  ],
  "res": [["msgenfr", "Microsoft, IA générative en français : leçons sur la synthèse."], ["sk101", "Claude 101 : usages quotidiens, en anglais."]],
  "ex": [
   {"t": "À partir de notes fictives d'une réunion de comité, faites produire un compte rendu décisions, actions, points ouverts.", "c": "Chaque action a un responsable et une échéance ; rien n'a été inventé."},
   {"t": "Résumez en 200 mots un rapport public (par exemple un rapport de la Cour des comptes) et demandez ce qui a été omis.", "c": "Vous avez vérifié au moins une omission signalée dans le texte source."},
   {"t": "Facultatif : faites produire la trame d'une présentation de dix diapositives sur un sujet fictif.", "c": "Chaque titre est une phrase affirmative.", "opt": True}
  ],
  "quiz": [
   mcq("Quelles rubriques sont prioritaires dans un compte rendu ?", ["Liste des présents et horaires", "Décisions, actions et points ouverts", "Résumé chronologique des échanges", "Citations exactes de chaque intervenant"], 1, "Ce sont les éléments sur lesquels on agit."),
   mcq("Comment limiter le risque d'un résumé infidèle ?", ["Demander un résumé plus long", "Demander ce qui a été omis", "Demander un résumé en anglais", "Demander un résumé en points"], 1, "La liste des omissions rend les choix de l'assistant visibles."),
   mcq("Quel titre de diapositive est le plus utile ?", ["Contexte", "Résultats", "Le projet doit entrer en maturation", "Annexe 1"], 2, "Un titre affirmatif porte le message."),
   mcq("Peut-on transcrire une réunion confidentielle avec un outil grand public ?", ["Oui, si le fichier est supprimé après", "Non, sauf outil validé par l'entreprise", "Oui, si personne n'est nommé", "Oui, si la réunion dure moins d'une heure"], 1, "Le contenu reste confidentiel quel que soit le format."),
   mcq("L'assistant produit un schéma des flux de droits. Que vérifier ?", ["Les couleurs", "Le sens de chaque flèche et chaque partie", "La police de caractères", "La taille de l'image"], 1, "Une erreur sur un schéma est une erreur de fond.")
  ],
  "drills": [
   tf("Un résumé bien écrit est forcément fidèle.", False, "Il peut gommer une réserve ou une condition. Demandez les omissions."),
   cloze("Dans un compte rendu, chaque action a un responsable et une ___.", ["échéance", "couleur", "signature"], 0, "Sinon l'action ne sera pas suivie."),
   match("Associez chaque besoin à la consigne utile.", [["Compte rendu", "Décisions, actions, points ouverts"], ["Résumé", "Longueur, public, omissions"], ["Présentation", "Titres affirmatifs"]], "Chaque format a sa consigne type."),
   order("Remettez dans l'ordre la préparation d'un support.", ["Fixer le message principal", "Demander la trame", "Corriger les titres", "Mettre en forme dans l'outil interne"], "Le message précède la forme."),
   tf("Les chiffres recopiés dans un tableau par l'assistant se vérifient.", True, "Une erreur de recopie est fréquente et peu visible.")
  ]
 },
 {
  "id": "me5", "cote": "M5", "titre": "Votre assistant de poste", "duree": "1 h",
  "comp": ["organiser", "automatiser"], "cadre": 1,
  "obj": ["Configurer un projet ou un assistant personnalisé pour une tâche récurrente", "Mesurer le temps gagné et la qualité", "Partager une méthode avec l'équipe"],
  "notions": [
   ["Projets et assistants personnalisés", "Claude (Projets), ChatGPT (Projets et GPTs), Copilot (agents), Le Chat (agents) et Gemini (Gems) permettent d'enregistrer des instructions permanentes et des documents de référence. Une tâche récurrente y gagne en régularité."],
   ["Instructions permanentes", "Rôle, contexte du service, format de sortie, règles (citer la source, signaler l'incertitude, ne jamais inventer une référence). Testez-les sur trois cas fictifs avant de les adopter."],
   ["Documents de référence", "Seuls des documents publics ou validés pour cet usage : modèles publics, guides internes non confidentiels si la règle de l'entreprise le permet. Les connaissances d'un projet partagé sont visibles de ses membres."],
   ["Mesurer", "Notez pour une tâche : temps sans assistant, temps avec, corrections nécessaires. Sans mesure, l'impression de gain trompe dans les deux sens."],
   ["Partager", "Une consigne qui marche se partage : fiche d'une page (usage, consigne, limites, exemple fictif). C'est ainsi qu'une équipe progresse au même rythme."]
  ],
  "res": [["sk101", "Claude 101 : projets et instructions."], ["oaiacad", "OpenAI Academy : projets et GPTs."]],
  "ex": [
   {"t": "Créez un projet (ou équivalent) pour une tâche récurrente de votre poste : instructions permanentes et un document de référence public.", "c": "Trois essais sur des cas fictifs donnent un résultat de même qualité."},
   {"t": "Mesurez une tâche réelle faite sans données de dossier (par exemple la rédaction d'une relance générique) : temps sans et avec assistant.", "c": "Les deux temps et le nombre de corrections sont notés dans le carnet."},
   {"t": "Rédigez une fiche d'une page pour partager cette méthode avec un collègue.", "c": "Un collègue peut l'appliquer sans explication orale."}
  ],
  "quiz": [
   mcq("À quoi servent les instructions permanentes d'un projet ?", ["À stocker les dossiers clients", "À appliquer les mêmes règles à chaque échange", "À augmenter la fenêtre de contexte", "À désactiver la recherche web"], 1, "Elles évitent de répéter rôle, format et règles."),
   mcq("Quels documents placer dans les connaissances d'un projet ?", ["Les contrats en cours", "Documents publics ou validés pour cet usage", "Les courriels de la semaine", "Tous les fichiers du service"], 1, "Les connaissances sont lues à chaque échange et parfois partagées."),
   mcq("Avant d'adopter un assistant personnalisé, il faut :", ["Le partager à tout le service", "Le tester sur trois cas fictifs", "Lui donner un nom précis", "Activer toutes ses options"], 1, "Un test sur plusieurs cas révèle les consignes ambiguës."),
   mcq("Pourquoi mesurer le temps passé avec et sans assistant ?", ["Pour remplir un tableau de bord", "Parce que l'impression de gain peut tromper", "Parce que l'outil l'exige", "Pour choisir le modèle le moins cher"], 1, "La mesure tranche entre impression et réalité."),
   mcq("Quel format pour partager une méthode ?", ["Une capture d'écran de conversation", "Une fiche : usage, consigne, limites, exemple", "Un lien vers votre historique", "Un message oral en réunion"], 1, "La fiche se réutilise sans son auteur.")
  ],
  "drills": [
   tf("Les documents placés dans un projet partagé peuvent être vus par ses membres.", True, "D'où la règle : documents publics ou validés seulement."),
   cloze("Des consignes qui servent à chaque échange s'appellent des instructions ___.", ["permanentes", "cachées", "système"], 0, "Le terme varie selon l'outil ; le principe est le même."),
   match("Associez chaque outil à son nom de fonction.", [["Claude", "Projets"], ["ChatGPT", "GPTs"], ["Gemini", "Gems"]], "Les noms changent, la fonction est voisine."),
   order("Remettez dans l'ordre la mise en place d'un assistant de poste.", ["Choisir une tâche récurrente", "Écrire les instructions", "Tester sur trois cas fictifs", "Mesurer puis partager"], "Le partage vient après la preuve."),
   tf("Un gain de temps ressenti suffit pour généraliser une méthode.", False, "Sans mesure, l'impression trompe dans les deux sens.")
  ]
 }
]
