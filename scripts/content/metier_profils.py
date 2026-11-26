# Voies Métier par profil (25/11/2026, demande de Thomas : un parcours par métier de la SATT).
# Le profil Juriste garde les étapes me1 à me5 (metier.py). Chaque voie compte cinq étapes,
# avec les mêmes compétences dans le même ordre, pour que la carte des compétences reste comparable.
# Pratique autorisée au poste (cadre 1), documents fictifs ou publics uniquement.
from socle import mcq, tf, cloze, order, match

COMP = [["produire", "formuler"], ["produire", "verifier"], ["verifier", "dialoguer"], ["produire", "organiser"], ["organiser", "automatiser"]]

def step(pid, n, titre, duree, obj, notions, res, ex, quiz, drills):
  return {"id": f"{pid}{n}", "cote": f"M{n}", "titre": titre, "duree": duree, "comp": COMP[n - 1], "cadre": 1,
          "obj": obj, "notions": notions, "res": res, "ex": ex, "quiz": quiz, "drills": drills}

# ---------- Chargé de transfert ----------
CDT = [
 step("mt", 1, "Courriels aux chercheurs et aux industriels", "40 min",
  ["Écrire à un chercheur ou à un industriel avec le bon registre", "Relancer sans froisser", "Ne rien promettre au nom de la SATT"],
  [
   ["Deux publics, deux registres", "Un chercheur attend de la précision sur le calendrier et sur ce que la SATT fera de son invention. Un industriel attend une proposition de valeur en trois lignes. Indiquez le destinataire et son attente dans la consigne : l'assistant ajuste le vocabulaire et la longueur."],
   ["Le premier contact industriel", "Demandez un courriel court : problème résolu, résultat obtenu, ce que vous proposez (un échange, une démonstration), sans détail technique confidentiel. Ce qui n'est pas publié ou protégé ne figure pas dans un premier courriel."],
   ["Relancer", "Donnez l'historique en termes neutres (date du premier envoi, réponse ou silence) et le ton voulu. Une relance réussie rappelle l'intérêt pour le destinataire, pas l'impatience de l'expéditeur."],
   ["Engagements", "L'assistant ajoute volontiers « nous pouvons financer », « exclusivité possible » ou un délai. Aucune de ces formules ne part sans décision. Relisez chaque phrase qui engage la SATT."],
   ["Matière d'entraînement", "Projet fictif, laboratoire imaginaire, société inventée. Une déclaration d'invention réelle ou le nom d'un industriel en discussion ne vont pas dans un outil non validé."]
  ],
  [["skfluency", "Module Description du cours AI Fluency : décrire la tâche, le ton et le format."], ["msgenfr", "Microsoft, cours d'IA générative en français : leçon sur la rédaction."]],
  [
   {"t": "Pour un projet fictif (un capteur imaginaire de qualité de l'eau), faites rédiger un premier courriel à un industriel inventé, en moins de 120 mots, sans détail technique non publié.", "c": "Le courriel tient en 120 mots ; aucune information confidentielle ni promesse n'y figure."},
   {"t": "Faites rédiger la relance d'un chercheur fictif qui n'a pas renvoyé les compléments de sa déclaration d'invention, en deux tons : cordial et pressant.", "c": "Vous savez quelle consigne a changé le ton."},
   {"t": "Facultatif : demandez la version anglaise du premier courriel et vérifiez les termes techniques.", "c": "Les termes techniques ont été relus par vous.", "opt": True}
  ],
  [
   mcq("Que met-on dans un premier courriel à un industriel ?", ["Le détail du procédé et les résultats non publiés", "Problème résolu, résultat et proposition d'échange", "Le calendrier interne de la SATT et le budget", "La copie de la déclaration d'invention reçue"], 1, "Le premier contact donne envie d'en savoir plus, sans rien divulguer."),
   mcq("L'assistant écrit « une licence exclusive est envisageable ». Que faire ?", ["La garder, elle rend l'offre attractive", "La retirer, sauf si c'est décidé", "La remplacer par « tout est négociable »", "Demander à l'assistant de la justifier"], 1, "Aucun engagement ne part sans décision."),
   mcq("Quelle information donner pour une bonne relance ?", ["Le nom du laboratoire et de l'inventeur", "Date du premier envoi, réponse et ton voulu", "Le texte complet de tous les échanges", "Votre avis personnel sur le destinataire"], 1, "L'historique neutre suffit à l'assistant."),
   mcq("Sur quoi s'entraîner à rédiger ces courriels ?", ["Un projet fictif et une société inventée", "Le dernier projet du portefeuille, sans les noms", "Une déclaration d'invention reçue cette semaine", "Le courriel d'un collègue sur un dossier en cours"], 0, "Le contexte d'un vrai projet reste identifiant, même sans les noms."),
   mcq("Avant l'envoi, la relecture prioritaire porte sur :", ["La longueur des paragraphes", "Les formules de politesse", "Les engagements, dates et informations techniques", "Le nombre de points d'exclamation"], 2, "Ce sont les éléments qui engagent la SATT ou divulguent l'invention.")
  ],
  [
   tf("Un premier courriel à un industriel peut détailler des résultats non publiés si le ton est prudent.", False, "Ce qui n'est ni publié ni protégé ne part pas dans un premier contact."),
   cloze("Un premier contact industriel met en avant le ___ résolu par la technologie.", ["problème", "budget", "laboratoire"], 0, "L'industriel cherche une solution à son problème."),
   match("Associez chaque destinataire à son attente.", [["Chercheur", "Calendrier et suite donnée"], ["Industriel", "Valeur en trois lignes"], ["Direction", "Décision à prendre"]], "Le registre se règle dans la consigne."),
   order("Remettez dans l'ordre la préparation d'une relance.", ["Résumer l'historique en termes neutres", "Choisir le ton", "Faire rédiger", "Relire chaque engagement"], "La relecture ferme la boucle."),
   tf("Une formule comme « nous pouvons financer la maturation » demande une décision préalable.", True, "Tout engagement au nom de la SATT doit avoir été décidé.")
  ]),
 step("mt", 2, "Analyser une déclaration d'invention", "50 min",
  ["Faire structurer une déclaration d'invention fictive", "Repérer ce qui manque pour décider", "Garder l'appréciation de valorisation"],
  [
   ["Structurer, pas juger", "L'assistant met en forme : problème technique, solution, résultats, état d'avancement, inventeurs et établissements, publications prévues. L'appréciation du potentiel et la décision d'investir restent celles du chargé de transfert et du comité."],
   ["Grille d'analyse", "Donnez votre grille : rubriques attendues, format (tableau rubrique, contenu, source dans le document, question à poser) et la consigne de citer le passage exact. Sans grille, la synthèse est générale et inégale."],
   ["Ce qui manque", "Demandez explicitement les informations absentes : date de publication prévue, résultats reproduits ou non, financement d'origine, autres établissements. Une absence ne se voit pas à la lecture rapide et conditionne souvent la suite."],
   ["Niveau de maturité", "L'échelle TRL (de 1, principe observé, à 9, système éprouvé en conditions réelles) aide à situer un projet. Faites justifier le niveau proposé par une phrase du document ; un TRL sans justification est une supposition."],
   ["Confidentialité", "Une déclaration d'invention décrit une invention non protégée. Elle ne va jamais dans un outil non validé, même sans les noms. On s'entraîne sur une déclaration fictive rédigée pour l'exercice."]
  ],
  [["skfluency", "Module Discernment : évaluer la production de l'assistant."], ["msgenfr", "Microsoft, IA générative en français : leçons sur la synthèse."]],
  [
   {"t": "Rédigez une déclaration d'invention fictive d'une demi-page (une colle biosourcée imaginaire). Faites-en produire une fiche structurée avec citation du passage pour chaque rubrique.", "c": "Chaque rubrique de la fiche renvoie à un passage du texte ; les écarts sont notés."},
   {"t": "Demandez la liste des informations manquantes pour présenter ce projet en comité.", "c": "Au moins trois absences pertinentes sont confirmées par votre lecture."},
   {"t": "Demandez un niveau TRL justifié par une phrase du document, puis contestez-le.", "c": "Vous savez dire si la justification tient."}
  ],
  [
   mcq("Dans l'analyse d'une déclaration d'invention, l'assistant sert à :", ["Décider si le projet mérite un investissement", "Structurer le contenu et signaler les manques", "Évaluer seul la brevetabilité de l'invention", "Remplacer l'entretien avec les inventeurs"], 1, "La décision reste au chargé de transfert et au comité."),
   mcq("Pourquoi exiger le passage cité pour chaque rubrique ?", ["Pour rendre la fiche plus longue", "Pour contrôler vite contre le texte", "Parce que l'assistant ne sait pas résumer", "Pour respecter le droit d'auteur"], 1, "La citation permet la vérification ligne par ligne."),
   mcq("L'assistant propose un TRL 6. Que lui demander ?", ["De confirmer qu'il est certain", "La phrase du document qui le justifie", "De proposer plutôt un TRL 8", "De retirer le TRL de la fiche"], 1, "Un niveau sans justification est une supposition."),
   mcq("Quelle question fait apparaître ce que la lecture rapide manque ?", ["Résume cette déclaration en cinq lignes", "Quelles informations manquent pour décider ?", "Cette invention est-elle prometteuse ?", "Traduis cette déclaration en anglais"], 1, "Une absence ne se voit pas ; il faut la demander."),
   mcq("Sur quel document s'exercer ?", ["La dernière déclaration reçue, noms masqués", "Une déclaration fictive écrite pour l'exercice", "Une ancienne déclaration d'un projet abandonné", "Une déclaration envoyée par un confrère"], 1, "Une invention réelle reste non protégée, même ancienne ou masquée.")
  ],
  [
   tf("Une déclaration d'invention réelle peut aller dans un outil non validé si les noms des inventeurs sont retirés.", False, "L'invention elle-même est l'information confidentielle."),
   cloze("Le niveau de maturité d'une technologie se situe sur l'échelle ___.", ["TRL", "CIB", "PCT"], 0, "Technology Readiness Level, de 1 à 9."),
   order("Remettez dans l'ordre l'analyse d'une déclaration.", ["Donner la grille de rubriques", "Faire structurer avec citations", "Demander ce qui manque", "Préparer les questions aux inventeurs"], "Les manques deviennent des questions."),
   match("Associez chaque rubrique à sa question.", [["Résultats", "Sont-ils reproduits ?"], ["Publications", "Une parution est-elle prévue ?"], ["Financement", "Qui a financé les travaux ?"]], "Chaque rubrique appelle une vérification."),
   tf("Un TRL proposé par l'assistant sans justification tirée du document reste une hypothèse.", True, "Faites-le justifier par une phrase du texte.")
  ]),
 step("mt", 3, "Veille, marché et partenaires", "45 min",
  ["Mener une recherche web contrôlée sur un marché", "Repérer des partenaires industriels potentiels", "Remonter à la source de chaque chiffre"],
  [
   ["Recherche web activée", "Pour un marché ou des entreprises, activez la recherche web et exigez les liens. Sans recherche, l'assistant répond de mémoire : chiffres datés, entreprises disparues, taille de marché inventée."],
   ["Chiffres de marché", "Un chiffre de marché circule souvent d'article en article sans source. Demandez l'étude d'origine, son éditeur et son année. Un chiffre sans source primaire ne va pas dans une fiche de comité."],
   ["Cartographie des acteurs", "Demandez un tableau des entreprises du secteur : activité, taille, implantation, lien vers le site. Vérifiez chaque ligne : une entreprise peut avoir été rachetée, avoir changé d'activité ou ne pas exister."],
   ["Veille récurrente", "Enregistrez une consigne de veille (sujet, sources préférées, période, format) et relancez-la chaque mois. La consigne enregistrée garde la méthode d'une fois sur l'autre."],
   ["Ce que la recherche ne dit pas", "L'assistant ne voit ni les bases payantes ni les échanges confidentiels du secteur. Une liste de partenaires produite par l'assistant est un point de départ, jamais une cible validée."]
  ],
  [["insee", "INSEE : statistiques publiques sur les entreprises et les secteurs."], ["espacenet", "Espacenet : repérer les déposants actifs d'un domaine technique."]],
  [
   {"t": "Avec la recherche web activée, faites établir la liste de dix entreprises françaises d'un secteur de votre choix (par exemple le traitement de l'eau), avec un lien par entreprise.", "c": "Vous avez ouvert au moins cinq liens ; les erreurs sont notées dans le carnet."},
   {"t": "Demandez la taille du marché de ce secteur, puis l'étude d'origine du chiffre.", "c": "Vous savez si le chiffre remonte à une source primaire identifiée."}
  ],
  [
   mcq("Pourquoi activer la recherche web pour une cartographie d'entreprises ?", ["Pour que la réponse soit plus longue", "Sans elle, l'assistant répond de mémoire", "Parce que l'outil refuse sinon de répondre", "Pour masquer les entreprises disparues"], 1, "La mémoire de l'assistant s'arrête à sa date de coupure."),
   mcq("Un article cite un marché de 2 milliards d'euros. Que faire ?", ["Le reprendre, il est publié", "Remonter à l'étude d'origine et à son année", "Le diviser par deux par prudence", "Demander à l'assistant s'il est exact"], 1, "Seule la source primaire se cite en comité."),
   mcq("La liste de partenaires proposée par l'assistant est :", ["Une cible validée à contacter", "Un point de départ à vérifier", "Une liste exhaustive du secteur", "Une source citable en comité"], 1, "L'assistant ne voit ni les bases payantes ni le contexte du secteur."),
   mcq("Comment rendre une veille mensuelle régulière ?", ["Reformuler la demande chaque mois", "Enregistrer une consigne de veille réutilisable", "Demander à l'assistant de s'en souvenir", "Changer d'assistant chaque mois"], 1, "La consigne enregistrée garde la méthode."),
   mcq("Quelle vérification prime sur une ligne de cartographie ?", ["La longueur de la description", "L'existence et l'activité actuelle de l'entreprise", "La couleur du logo", "Le nombre de salariés arrondi"], 1, "Rachats et changements d'activité sont fréquents.")
  ],
  [
   tf("Un chiffre de marché repris par plusieurs articles est forcément fiable.", False, "Il peut circuler sans source ; remontez à l'étude d'origine."),
   cloze("Avant de citer un chiffre, remontez à sa source ___.", ["primaire", "secondaire", "probable"], 0, "L'étude d'origine, avec son éditeur et son année."),
   order("Remettez dans l'ordre une cartographie fiable.", ["Activer la recherche web", "Demander un tableau avec liens", "Ouvrir chaque lien", "Corriger les lignes erronées"], "La vérification clôt la recherche."),
   match("Associez chaque besoin à la source à privilégier.", [["Déposants d'un domaine", "Espacenet"], ["Statistiques d'un secteur", "INSEE"], ["Activité d'une entreprise", "Son site et ses publications"]], "Chaque question a sa source."),
   tf("L'assistant voit les bases de données payantes auxquelles la SATT est abonnée.", False, "Il ne voit que le web public et ce que vous lui fournissez.")
  ]),
 step("mt", 4, "Fiches de valorisation et dossiers de comité", "45 min",
  ["Produire une fiche de présentation de technologie", "Préparer la trame d'un passage en comité", "Faire relire une recommandation"],
  [
   ["Fiche technologie", "Une fiche de présentation tient en une page : problème, solution, avantages, applications, état de la protection, contact. Demandez cette structure et une version non confidentielle, sans détail technique non publié."],
   ["Dossier de comité", "Le comité décide : demandez le plan objet, projet, marché, protection, budget, risques, recommandation. Sans plan, l'assistant raconte l'histoire du projet au lieu de préparer une décision."],
   ["Budget de maturation", "L'assistant met en forme un budget à partir de vos lignes ; il ne l'estime pas. Un montant proposé par l'assistant sans base est une invention. Vérifiez chaque total recopié."],
   ["Contradicteur", "Avant le comité, demandez les trois objections les plus fortes contre votre recommandation. Préparer la réponse vaut mieux que la découvrir en séance."],
   ["Supports", "Demandez une trame de diapositives à titres affirmatifs (« Le marché de la détection rapide croît », plutôt que « Marché »). La mise en forme se fait ensuite dans l'outil de l'entreprise."]
  ],
  [["msgenfr", "Microsoft, IA générative en français : leçons sur la synthèse."], ["sk101", "Claude 101 : usages quotidiens, en anglais."]],
  [
   {"t": "À partir du projet fictif de l'étape M2, faites produire une fiche de présentation non confidentielle d'une page.", "c": "La fiche ne contient rien qui ne figure dans une publication imaginaire de référence."},
   {"t": "Faites produire la trame d'un dossier de comité, puis les trois objections les plus fortes.", "c": "Chaque objection a une réponse dans le carnet."},
   {"t": "Facultatif : faites mettre en tableau un budget fictif de cinq lignes et contrôlez le total.", "c": "Le total a été recalculé par vous.", "opt": True}
  ],
  [
   mcq("Quelle structure pour une fiche de présentation de technologie ?", ["Historique complet du laboratoire", "Problème, solution, avantages, applications, protection", "Liste des inventeurs et de leurs publications", "Résumé chronologique des réunions"], 1, "Une page, lisible par un industriel."),
   mcq("L'assistant propose un budget de 150 000 € pour la maturation. Que faire ?", ["Le reprendre, l'ordre de grandeur est plausible", "Le refuser : le budget vient de vos lignes", "Le diviser en deux tranches égales", "Lui demander d'arrondir"], 1, "Un montant sans base est une invention."),
   mcq("Quel titre de diapositive est le plus utile en comité ?", ["Marché", "Le marché de la détection rapide croît", "Données", "Annexe 2"], 1, "Un titre affirmatif porte le message."),
   mcq("Pourquoi demander les objections avant le comité ?", ["Pour allonger le dossier", "Pour préparer les réponses", "Pour laisser l'assistant décider", "Pour remplacer l'avis du comité"], 1, "On découvre les objections avant la séance."),
   mcq("Que vérifier dans un tableau budgétaire mis en forme ?", ["La police du tableau", "Chaque montant recopié et le total", "La couleur des en-têtes", "Le nombre de colonnes"], 1, "Une erreur de recopie est fréquente et peu visible.")
  ],
  [
   tf("Une fiche de présentation destinée aux industriels peut reprendre les résultats non publiés.", False, "La version diffusée reste non confidentielle."),
   cloze("Le dossier de comité se termine par une ___.", ["recommandation", "bibliographie", "annexe"], 0, "Le comité vient pour décider."),
   match("Associez chaque document à sa consigne.", [["Fiche technologie", "Une page, non confidentielle"], ["Dossier de comité", "Plan orienté décision"], ["Support", "Titres affirmatifs"]], "Chaque format a sa consigne type."),
   order("Remettez dans l'ordre la préparation d'un comité.", ["Rédiger la recommandation", "Faire produire la trame", "Demander les objections", "Préparer les réponses"], "La recommandation guide le reste."),
   tf("Un total recalculé à la main protège d'une erreur de recopie de l'assistant.", True, "La vérification des chiffres reste humaine.")
  ]),
 step("mt", 5, "Votre assistant de chargé de transfert", "1 h",
  ["Configurer un projet pour une tâche récurrente de valorisation", "Mesurer le temps gagné", "Partager la méthode avec l'équipe"],
  [
   ["Projets et assistants personnalisés", "Claude (Projets), ChatGPT (Projets et GPTs), Copilot (agents), Le Chat (agents) et Gemini (Gems) enregistrent des instructions permanentes et des documents de référence. Les fiches technologie, les relances et les comptes rendus de comité s'y prêtent bien."],
   ["Instructions permanentes", "Rôle, public visé, format de sortie et règles : ne rien inventer, citer la source de chaque chiffre, signaler l'incertitude, ne rien promettre au nom de la SATT. Testez-les sur trois projets fictifs."],
   ["Documents de référence", "Modèles publics ou internes validés pour cet usage, jamais un dossier de projet. Les connaissances d'un projet partagé sont visibles de ses membres."],
   ["Mesurer", "Pour une tâche (une fiche technologie fictive), notez le temps sans assistant, le temps avec et les corrections nécessaires. Sans mesure, l'impression de gain trompe dans les deux sens."],
   ["Partager", "Une consigne qui marche se partage avec les autres chargés de transfert : fiche d'une page (usage, consigne, limites, exemple fictif)."]
  ],
  [["sk101", "Claude 101 : projets et instructions."], ["oaiacad", "OpenAI Academy : projets et GPTs."]],
  [
   {"t": "Créez un projet (ou équivalent) « Fiche technologie » : instructions permanentes et un modèle de fiche vierge.", "c": "Trois essais sur des projets fictifs donnent une fiche de même qualité."},
   {"t": "Mesurez la rédaction d'une fiche fictive sans et avec l'assistant.", "c": "Les deux temps et le nombre de corrections sont notés dans le carnet."},
   {"t": "Rédigez une fiche d'une page pour partager cette méthode.", "c": "Un collègue peut l'appliquer sans explication orale."}
  ],
  [
   mcq("Quelle règle mettre dans les instructions permanentes ?", ["Toujours proposer une licence exclusive", "Citer la source de chaque chiffre", "Écrire en anglais par défaut", "Répondre en une phrase"], 1, "La règle de source évite les chiffres inventés."),
   mcq("Quels documents placer dans les connaissances du projet ?", ["Les déclarations d'invention en cours", "Modèles publics ou validés pour cet usage", "Les courriels des industriels", "Les budgets des projets en cours"], 1, "Les connaissances sont lues à chaque échange et parfois partagées."),
   mcq("Avant d'adopter l'assistant, il faut :", ["Le partager à toute l'équipe", "Le tester sur trois projets fictifs", "Lui donner un nom accrocheur", "Activer toutes ses options"], 1, "Plusieurs cas révèlent les consignes ambiguës."),
   mcq("Pourquoi mesurer le temps passé ?", ["Pour remplir un tableau de bord", "Parce que l'impression de gain peut tromper", "Parce que l'outil l'exige", "Pour choisir le modèle le moins cher"], 1, "La mesure tranche entre impression et réalité."),
   mcq("Quel format pour partager la méthode ?", ["Une capture d'écran de conversation", "Une fiche : usage, consigne, limites, exemple", "Un lien vers votre historique", "Un message oral en réunion"], 1, "La fiche se réutilise sans son auteur.")
  ],
  [
   tf("Les documents placés dans un projet partagé peuvent être vus par ses membres.", True, "D'où la règle : documents publics ou validés seulement."),
   cloze("Les consignes appliquées à chaque échange s'appellent des instructions ___.", ["permanentes", "cachées", "système"], 0, "Le terme varie selon l'outil ; le principe est le même."),
   order("Remettez dans l'ordre la mise en place d'un assistant de poste.", ["Choisir une tâche récurrente", "Écrire les instructions", "Tester sur trois cas fictifs", "Mesurer puis partager"], "Le partage vient après la preuve."),
   match("Associez chaque outil à son nom de fonction.", [["Claude", "Projets"], ["ChatGPT", "GPTs"], ["Gemini", "Gems"]], "Les noms changent, la fonction est voisine."),
   tf("Un gain de temps ressenti suffit pour généraliser une méthode.", False, "Sans mesure, l'impression trompe dans les deux sens.")
  ]),
]

# ---------- Ingénieur brevet ----------
BREVET = [
 step("mb", 1, "Résumer et expliquer un document brevet", "40 min",
  ["Faire résumer un brevet publié pour un non-spécialiste", "Expliquer une revendication en termes simples", "Écrire aux inventeurs avec le bon niveau technique"],
  [
   ["Le brevet publié, matière idéale", "Un brevet publié est public : c'est la meilleure matière d'entraînement. Copiez le texte depuis Espacenet ou la base de l'INPI et indiquez le lecteur visé : chargé de transfert, chercheur, direction."],
   ["Résumé utile", "Demandez : problème technique, solution, revendication 1 en termes simples, domaine d'application. Ajoutez « sans avis sur la validité ni sur la portée » : ces appréciations restent les vôtres."],
   ["Expliquer une revendication", "Faites découper la revendication en caractéristiques numérotées, chacune expliquée en une phrase. Comparez avec votre propre lecture : l'assistant peut fusionner deux caractéristiques ou en oublier une."],
   ["Écrire aux inventeurs", "Pour demander des compléments (modes de réalisation, résultats d'essais), donnez la liste des points et le niveau technique de l'inventeur. L'assistant structure ; vous vérifiez que chaque question est précise."],
   ["Limite", "Un document brevet non publié, un projet de demande ou une description reçue d'un inventeur ne vont jamais dans un outil non validé."]
  ],
  [["espacenet", "Espacenet : textes intégraux des brevets publiés."], ["inpi", "INPI : base des brevets français."]],
  [
   {"t": "Choisissez un brevet publié dans un domaine que vous connaissez. Faites-en produire un résumé de dix lignes pour un chargé de transfert, sans avis sur la validité.", "c": "Le résumé a été comparé au texte ; les écarts sont notés."},
   {"t": "Faites découper la revendication 1 en caractéristiques numérotées.", "c": "Le découpage correspond à votre propre lecture, ou vous savez où il diverge."},
   {"t": "Facultatif : faites rédiger un courriel fictif de demande de compléments à un inventeur imaginaire.", "c": "Chaque question du courriel appelle une réponse précise.", "opt": True}
  ],
  [
   mcq("Sur quel document s'entraîner à résumer un brevet ?", ["Un projet de demande avant dépôt", "Un brevet publié, copié depuis une base officielle", "La description reçue d'un inventeur", "Un rapport de recherche non publié"], 1, "Un brevet publié est public."),
   mcq("Que demander dans le résumé d'un brevet pour un non-spécialiste ?", ["Un avis sur la validité du brevet", "Problème, solution, revendication 1 en termes simples", "La liste complète des revendications dépendantes", "La traduction intégrale du texte"], 1, "L'avis sur la validité reste celui de l'ingénieur brevet."),
   mcq("Pourquoi découper une revendication en caractéristiques ?", ["Pour la rendre plus longue", "Pour vérifier qu'aucune caractéristique n'est oubliée", "Pour la traduire plus vite", "Pour changer sa portée"], 1, "Le découpage numéroté se contrôle point par point."),
   mcq("L'assistant ajoute « ce brevet est probablement valide ». Que faire ?", ["Le garder, c'est rassurant pour le lecteur", "Le retirer : l'appréciation vous revient", "Le remplacer par « très probablement valide »", "Lui demander un pourcentage de validité"], 1, "Validité et portée relèvent de votre analyse."),
   mcq("Avant d'envoyer un courriel de demande de compléments, vérifiez :", ["La présence d'une formule de politesse", "Que chaque question est précise", "La longueur des phrases", "Le nombre de paragraphes"], 1, "Une question vague appelle une réponse vague.")
  ],
  [
   tf("Une description d'invention reçue d'un inventeur peut aller dans un outil grand public si elle est courte.", False, "L'invention non déposée ne va jamais dans un outil non validé."),
   cloze("Pour vérifier un résumé, découpez la revendication en ___ numérotées.", ["caractéristiques", "pages", "figures"], 0, "Chaque caractéristique se contrôle."),
   match("Associez chaque lecteur au résumé adapté.", [["Chargé de transfert", "Problème, solution, applications"], ["Direction", "Enjeu en trois lignes"], ["Chercheur", "Lien avec ses travaux"]], "Le lecteur décide du contenu."),
   order("Remettez dans l'ordre l'explication d'une revendication.", ["Copier la revendication publiée", "Faire découper en caractéristiques", "Comparer à votre lecture", "Corriger les écarts"], "La comparaison clôt l'exercice."),
   tf("L'assistant peut fusionner deux caractéristiques d'une revendication sans le signaler.", True, "D'où la comparaison avec votre propre lecture.")
  ]),
 step("mb", 2, "Lire et comparer des revendications", "50 min",
  ["Comparer les revendications de deux brevets publiés", "Faire produire un tableau de caractéristiques", "Garder l'analyse de portée et de contrefaçon"],
  [
   ["Repérer, pas trancher", "L'assistant aligne rapidement les caractéristiques de deux revendications. L'appréciation de la portée, de la nouveauté ou d'un risque de contrefaçon reste celle de l'ingénieur brevet."],
   ["Tableau de caractéristiques", "Demandez un tableau : caractéristique, présente dans le document A (citation), présente dans le document B (citation), remarque. La citation exacte rend chaque ligne vérifiable."],
   ["Revendications indépendantes", "Demandez d'abord la liste des revendications indépendantes, puis le rattachement de chaque dépendante. Une erreur de rattachement fausse toute la lecture."],
   ["Ce qui n'est pas dit", "Demandez aussi les caractéristiques absentes du document comparé. Une absence ne se voit pas à la lecture rapide et c'est souvent elle qui compte."],
   ["Recouper", "Contrôlez au moins trois lignes du tableau sur le texte publié. Un mot remplacé par un synonyme (« fixé » pour « solidaire ») peut changer l'analyse."]
  ],
  [["espacenet", "Espacenet : textes intégraux et revendications."], ["skfluency", "Module Discernment : évaluer la production de l'assistant."]],
  [
   {"t": "Choisissez deux brevets publiés du même domaine. Faites produire un tableau des caractéristiques de leurs revendications 1, avec citations.", "c": "Trois lignes ont été vérifiées sur le texte publié ; les écarts sont notés."},
   {"t": "Demandez la liste des revendications indépendantes et le rattachement des dépendantes pour un des deux brevets.", "c": "Le rattachement est confirmé par votre lecture."},
   {"t": "Demandez les caractéristiques de A absentes de B.", "c": "Au moins une absence est confirmée par votre lecture."}
  ],
  [
   mcq("Dans une comparaison de revendications, le rôle de l'assistant est de :", ["Conclure sur un risque de contrefaçon", "Aligner les caractéristiques avec citations", "Décider de la nouveauté de l'invention", "Rédiger l'avis remis à la direction"], 1, "L'appréciation reste celle de l'ingénieur brevet."),
   mcq("Pourquoi exiger la citation exacte dans le tableau ?", ["Pour allonger le tableau", "Pour vérifier chaque ligne sur le texte", "Parce que l'assistant ne sait pas résumer", "Pour respecter la mise en page"], 1, "La citation rend le contrôle rapide."),
   mcq("Quelle étape vient en premier ?", ["Comparer toutes les revendications à la fois", "Lister les revendications indépendantes", "Résumer la description", "Traduire les revendications"], 1, "Le rattachement des dépendantes en découle."),
   mcq("« Fixé » devient « solidaire » dans le tableau. Pourquoi est-ce un problème ?", ["Ce n'en est pas un, ce sont des synonymes", "Un mot changé peut modifier l'analyse", "Parce que le tableau devient trop long", "Parce que la police change"], 1, "En brevets, le mot exact compte."),
   mcq("Quelle question fait apparaître ce qui manque ?", ["Résume ces deux brevets", "Quelles caractéristiques de A sont absentes de B ?", "Ces brevets se ressemblent-ils ?", "Traduis la revendication 1"], 1, "Une absence ne se voit pas ; il faut la demander.")
  ],
  [
   tf("Un tableau de caractéristiques produit par l'assistant peut fonder seul un avis de contrefaçon.", False, "L'avis repose sur l'analyse de l'ingénieur brevet."),
   cloze("Une revendication ___ ne renvoie à aucune autre revendication.", ["indépendante", "dépendante", "accessoire"], 0, "Les dépendantes s'y rattachent."),
   order("Remettez dans l'ordre une comparaison fiable.", ["Lister les revendications indépendantes", "Faire le tableau avec citations", "Demander les absences", "Vérifier trois lignes"], "La vérification par sondage clôt la comparaison."),
   match("Associez chaque demande à son intérêt.", [["Citation exacte", "Contrôle ligne par ligne"], ["Liste des absences", "Ce que la lecture rapide manque"], ["Rattachement", "Structure des revendications"]], "Chaque consigne a sa fonction."),
   tf("Remplacer un mot par un synonyme peut changer l'analyse d'une revendication.", True, "Le mot exact compte.")
  ]),
 step("mb", 3, "Recherche d'antériorités", "45 min",
  ["Préparer une stratégie de recherche avec l'assistant", "Interroger les bases officielles", "Vérifier chaque document cité"],
  [
   ["L'assistant ne remplace pas la base", "Les assistants inventent volontiers des numéros de brevet plausibles. Toute antériorité se retrouve dans Espacenet, Google Patents, Lens ou la base de l'INPI. Un numéro introuvable est une hallucination."],
   ["Préparer la requête", "L'assistant est utile en amont : mots-clés et synonymes, traductions anglaises et allemandes, codes de classification CIB ou CPC à explorer. Vous lancez ensuite la recherche dans la base."],
   ["Littérature non brevet", "Publications scientifiques, thèses, normes : demandez des pistes et des mots-clés, puis cherchez dans HAL ou chez l'éditeur. Une référence d'article fournie de mémoire se vérifie comme un numéro de brevet."],
   ["Lire un résultat", "Collez l'abrégé d'un document trouvé et demandez s'il contient chaque caractéristique de la revendication visée, avec citation. Vous concluez ; l'assistant pointe."],
   ["Confidentialité", "Décrire une invention non déposée dans un outil non validé expose l'invention. On s'exerce sur un objet technique banal ou sur un brevet déjà publié."]
  ],
  [["espacenet", "Espacenet : recherche par mots-clés et par classification."], ["hal", "HAL : archive ouverte des publications scientifiques."]],
  [
   {"t": "Pour un objet technique banal (un ouvre-bouteille à levier), faites proposer des mots-clés, synonymes, traductions et codes CPC. Lancez la recherche dans Espacenet.", "c": "Au moins un code proposé a été confirmé dans la classification ; les autres sont notés."},
   {"t": "Sans recherche web, demandez trois brevets antérieurs sur cet objet avec leur numéro. Cherchez chaque numéro dans Espacenet.", "c": "Vous savez combien de numéros existent et correspondent au sujet."}
  ],
  [
   mcq("L'assistant cite trois brevets antérieurs avec leur numéro. Que faire ?", ["Les citer, les numéros sont précis", "Les retrouver dans Espacenet ou une autre base", "Lui demander s'il en est certain", "Les garder pour un usage interne"], 1, "Un numéro plausible peut être inventé."),
   mcq("Où l'assistant est-il le plus utile dans une recherche d'antériorités ?", ["Pour conclure sur la nouveauté", "Pour préparer mots-clés, traductions et codes", "Pour remplacer la base de données", "Pour décider de déposer ou non"], 1, "La recherche elle-même se fait dans la base."),
   mcq("Comment traiter un code CPC proposé par l'assistant ?", ["L'utiliser tel quel", "Le vérifier dans la classification officielle", "Le remplacer par un code CIB", "L'ignorer, les codes sont inutiles"], 1, "Un code peut être mal attribué ou inexistant."),
   mcq("Sur quoi s'exercer à la recherche d'antériorités ?", ["L'invention qu'un laboratoire vient de déclarer", "Un objet banal ou un brevet déjà publié", "Un projet de demande à déposer le mois prochain", "La description d'un concurrent obtenue en réunion"], 1, "Une invention non déposée ne va pas dans un outil non validé."),
   mcq("Vous collez un abrégé trouvé. Que demander ?", ["Si le brevet visé est valide", "Si chaque caractéristique y figure, avec citation", "Un résumé en cinq lignes", "Une traduction en allemand"], 1, "L'assistant pointe, vous concluez.")
  ],
  [
   tf("Un numéro de brevet donné de mémoire par l'assistant est fiable s'il a le bon format.", False, "Le format ne prouve rien ; seule la base fait foi."),
   cloze("Les codes de classification des brevets les plus utilisés sont la CIB et la ___.", ["CPC", "TRL", "PCT"], 0, "Classification coopérative des brevets."),
   order("Remettez dans l'ordre une recherche d'antériorités.", ["Faire proposer mots-clés et codes", "Vérifier les codes", "Lancer la recherche dans la base", "Analyser les résultats avec citations"], "La base reste la source."),
   match("Associez chaque besoin à sa source.", [["Brevets publiés", "Espacenet"], ["Publications scientifiques", "HAL ou l'éditeur"], ["Classification", "Schéma CPC officiel"]], "Chaque document se vérifie à sa source."),
   tf("Décrire une invention non déposée dans un outil grand public expose l'invention.", True, "On s'exerce sur un objet banal ou un brevet publié.")
  ]),
 step("mb", 4, "Aide à la rédaction, sans exposer l'invention", "45 min",
  ["Utiliser l'assistant sur la forme sans lui confier l'invention", "Vérifier la cohérence d'un texte fictif", "Préparer une réponse à une notification sur un cas d'école"],
  [
   ["Ce qui reste hors de l'outil", "Un projet de demande décrit une invention non publiée. Tant qu'il n'est pas déposé, il ne va pas dans un outil non validé : une fuite peut nuire à la nouveauté et la confidentialité de l'outil n'est pas maîtrisée par l'entreprise."],
   ["Ce que l'on peut faire", "Travailler sur un texte fictif ou publié : vérifier la cohérence des références numériques, la base d'antécédence (« ledit », « le ») et l'emploi constant des termes. Ces contrôles de forme se transposent ensuite à la main."],
   ["Variantes de formulation", "Sur un exemple fictif, demandez plusieurs formulations d'une même caractéristique, plus large ou plus étroite, et l'effet de chacune. Le choix et sa justification restent les vôtres."],
   ["Notification d'examen", "Sur une notification publiée (le registre européen en contient), faites structurer les objections et les passages cités. La stratégie de réponse reste la vôtre."],
   ["Traduction", "L'assistant traduit bien la langue technique courante ; vérifiez chaque terme de revendication. Un terme mal traduit peut changer la portée."]
  ],
  [["oeb", "OEB : Registre européen des brevets et notifications publiées."], ["espacenet", "Espacenet : textes publiés servant de modèles."]],
  [
   {"t": "Rédigez une revendication fictive pour un objet banal, avec cinq références numériques. Demandez un contrôle de cohérence des références et de la base d'antécédence.", "c": "Les incohérences signalées ont été vérifiées par vous."},
   {"t": "Demandez trois formulations d'une caractéristique, de la plus large à la plus étroite, avec l'effet de chacune.", "c": "Vous savez laquelle vous retiendriez et pourquoi."},
   {"t": "Facultatif : sur une notification publiée dans le registre européen, faites lister les objections et les passages cités.", "c": "La liste a été comparée à la notification.", "opt": True}
  ],
  [
   mcq("Un projet de demande non déposée peut-il être collé dans un outil grand public ?", ["Oui, si les inventeurs ne sont pas nommés", "Non, il reste hors de tout outil non validé", "Oui, si l'outil promet la confidentialité", "Oui, pour un simple contrôle de forme"], 1, "L'invention non publiée reste hors de l'outil."),
   mcq("Quel contrôle confier à l'assistant sur un texte fictif ?", ["La décision de déposer", "La cohérence des références et des termes", "L'évaluation de l'activité inventive", "Le choix des pays de dépôt"], 1, "Les contrôles de forme se transposent ensuite."),
   mcq("Vous demandez trois formulations d'une caractéristique. Qui choisit ?", ["L'assistant, selon l'effet le plus favorable", "Vous, en justifiant votre choix", "Le déposant, sans justification", "Personne, on garde les trois"], 1, "La portée reste votre décision."),
   mcq("Sur quoi s'entraîner à analyser une notification d'examen ?", ["Une notification reçue cette semaine", "Une notification publiée au registre", "Un projet de réponse en cours", "Un échange avec l'examinateur"], 1, "Le registre européen publie des notifications."),
   mcq("Dans une traduction de revendication, la vérification prioritaire porte sur :", ["La ponctuation", "Chaque terme technique", "La longueur des phrases", "La mise en page"], 1, "Un terme mal traduit peut changer la portée.")
  ],
  [
   tf("Retirer le nom des inventeurs suffit pour soumettre un projet de demande à un outil non validé.", False, "C'est l'invention elle-même qu'il faut protéger."),
   cloze("« Ledit » renvoie à un élément déjà introduit : c'est la base d'___.", ["antécédence", "priorité", "classement"], 0, "Chaque élément est introduit avant d'être repris."),
   match("Associez chaque tâche au bon traitement.", [["Projet de demande réel", "Hors de l'outil"], ["Revendication fictive", "Contrôle de forme possible"], ["Notification publiée", "Structuration possible"]], "Le statut du document décide."),
   order("Remettez dans l'ordre l'usage sûr de l'assistant en rédaction.", ["Rédiger un exemple fictif", "Faire contrôler la forme", "Vérifier les signalements", "Appliquer la méthode à la main"], "L'invention réelle ne passe jamais par l'outil."),
   tf("Une formulation plus large d'une caractéristique peut changer la portée de la revendication.", True, "D'où le choix réservé à l'ingénieur brevet.")
  ]),
 step("mb", 5, "Suivi de portefeuille et assistant de poste", "1 h",
  ["Organiser un échéancier fictif", "Configurer un projet pour une tâche récurrente", "Mesurer et partager"],
  [
   ["Échéances", "Priorité (12 mois), entrée en phase nationale d'une demande internationale, annuités : l'assistant met en tableau les dates à partir de vos données fictives. Il ne remplace pas le logiciel de gestion du portefeuille ; chaque date calculée se vérifie."],
   ["Calcul de dates", "Demandez la règle appliquée pour chaque date (« date de dépôt + 12 mois ») et vérifiez-la. Une erreur de calcul sur une échéance ne se rattrape pas toujours."],
   ["Projets et assistants personnalisés", "Claude (Projets), ChatGPT (Projets et GPTs), Copilot, Le Chat et Gemini (Gems) enregistrent des instructions permanentes. Les résumés de brevets publiés et les courriels aux inventeurs s'y prêtent bien."],
   ["Instructions permanentes", "Rôle, lecteur, format et règles : citer le passage, ne donner aucun avis de validité, signaler l'incertitude, ne jamais inventer un numéro. Testez-les sur trois brevets publiés."],
   ["Mesurer et partager", "Notez le temps sans et avec l'assistant pour une tâche, puis partagez une fiche d'une page (usage, consigne, limites, exemple)."]
  ],
  [["sk101", "Claude 101 : projets et instructions."], ["oaiacad", "OpenAI Academy : projets et GPTs."]],
  [
   {"t": "À partir de trois dépôts fictifs (dates inventées), faites produire un échéancier avec la règle de calcul de chaque date.", "c": "Chaque date a été recalculée par vous."},
   {"t": "Créez un projet (ou équivalent) « Résumé de brevet » avec instructions permanentes, testé sur trois brevets publiés.", "c": "Les trois résumés sont de même qualité et sans avis de validité."},
   {"t": "Mesurez un résumé fait sans puis avec l'assistant, et rédigez une fiche de partage.", "c": "Les deux temps et la fiche sont dans le carnet."}
  ],
  [
   mcq("Quel délai de priorité appliquer pour une demande de brevet ?", ["6 mois", "12 mois", "18 mois", "24 mois"], 1, "Le délai de priorité d'un brevet est de 12 mois."),
   mcq("Que demander à l'assistant avec chaque échéance calculée ?", ["La couleur de la ligne", "La règle de calcul appliquée", "Le nom du logiciel utilisé", "Une échéance de secours"], 1, "La règle rend le calcul vérifiable."),
   mcq("L'échéancier produit par l'assistant :", ["Remplace le logiciel de gestion du portefeuille", "Se vérifie date par date", "Est fiable s'il est bien présenté", "Peut contenir les dossiers réels"], 1, "Une erreur d'échéance ne se rattrape pas toujours."),
   mcq("Quelle règle mettre dans les instructions permanentes ?", ["Donner un avis sur la validité", "Ne jamais inventer un numéro de brevet", "Toujours résumer en anglais", "Répondre en une phrase"], 1, "La règle évite les références plausibles et fausses."),
   mcq("Pourquoi mesurer le temps passé ?", ["Pour remplir un tableau de bord", "Parce que l'impression de gain peut tromper", "Parce que l'outil l'exige", "Pour choisir le modèle le moins cher"], 1, "La mesure tranche entre impression et réalité.")
  ],
  [
   tf("Un échéancier produit par l'assistant peut remplacer le logiciel de gestion du portefeuille.", False, "Il aide à présenter ; la source de vérité reste le logiciel."),
   cloze("Le délai de priorité d'une demande de brevet est de ___ mois.", ["12", "6", "30"], 0, "Il court à compter du premier dépôt."),
   order("Remettez dans l'ordre un échéancier fiable.", ["Saisir les dates fictives", "Demander chaque règle de calcul", "Recalculer les dates", "Corriger les écarts"], "Chaque date se vérifie."),
   match("Associez chaque outil à son nom de fonction.", [["Claude", "Projets"], ["ChatGPT", "GPTs"], ["Gemini", "Gems"]], "Les noms changent, la fonction est voisine."),
   tf("Une règle « ne jamais inventer de numéro » a sa place dans les instructions permanentes.", True, "Elle cible l'erreur la plus coûteuse.")
  ]),
]

# ---------- Fonctions support et direction ----------
SUPPORT = [
 step("ms", 1, "Courriers, agendas et organisation", "40 min",
  ["Rédiger courriers et courriels de direction", "Préparer un ordre du jour et une invitation", "Organiser une semaine chargée"],
  [
   ["Le brouillon d'abord", "Donnez à l'assistant les idées en vrac : destinataire, objectif, points à faire passer, ce qui ne doit pas être dit. Il structure ; vous gardez la main sur le fond et sur chaque engagement."],
   ["Le ton se règle", "Précisez le registre : administrateur à informer, partenaire institutionnel à remercier, prestataire à relancer. Donnez un ancien courrier fictif comme modèle de ton si besoin."],
   ["Ordre du jour et invitation", "Donnez l'objet de la réunion, la durée, les décisions attendues et les participants par fonction. Demandez un ordre du jour minuté et une invitation de cinq lignes."],
   ["Organiser une semaine", "Listez vos tâches avec leur durée estimée et leur échéance ; demandez un plan par jour avec les priorités. L'assistant ne voit pas votre agenda dans le navigateur : vous lui donnez les créneaux libres."],
   ["Relire comme l'auteur", "Le courrier part sous le nom de la direction. Relisez dates, noms, montants et chaque promesse : l'assistant ajoute volontiers une formule que personne n'a décidée."]
  ],
  [["skfluency", "Module Description du cours AI Fluency : décrire la tâche, le ton et le format."], ["msgenfr", "Microsoft, cours d'IA générative en français : leçon sur la rédaction."]],
  [
   {"t": "À partir de cinq lignes de notes fictives, faites rédiger un courriel d'invitation à un comité, puis l'ordre du jour minuté.", "c": "L'ordre du jour tient dans la durée prévue ; aucune décision n'a été inventée."},
   {"t": "Faites rédiger un courrier de remerciement à un partenaire institutionnel fictif, en deux tons : protocolaire et chaleureux.", "c": "Vous savez quelle consigne a changé le ton."},
   {"t": "Facultatif : listez dix tâches fictives avec durées et échéances, et demandez un plan de semaine.", "c": "Le plan respecte les échéances et les créneaux que vous avez donnés.", "opt": True}
  ],
  [
   mcq("Que doit contenir la demande pour un ordre du jour ?", ["Uniquement la date de la réunion", "Objet, durée, décisions attendues et participants", "Le compte rendu de la réunion précédente en entier", "Une liste de formules de politesse"], 1, "Avec ces éléments, l'ordre du jour est presque toujours utilisable."),
   mcq("L'assistant ajoute « la direction vous recevra sous huit jours ». Que faire ?", ["Le laisser, c'est une formule usuelle", "Le retirer sauf si c'est décidé", "Le remplacer par quinze jours", "Demander à l'assistant de le justifier"], 1, "Tout engagement envoyé au nom de la direction doit avoir été décidé."),
   mcq("Pour planifier votre semaine, l'assistant du navigateur :", ["Lit votre agenda automatiquement", "Travaille sur les créneaux que vous lui donnez", "Réserve les salles à votre place", "Envoie les invitations seul"], 1, "Dans le navigateur, il ne voit que ce que vous lui fournissez."),
   mcq("Comment obtenir le ton de la maison sans le décrire longuement ?", ["Fournir un ancien courrier fictif comme modèle", "Demander un ton professionnel", "Écrire la consigne en majuscules", "Changer d'assistant"], 0, "Un exemple de ton vaut souvent mieux qu'une description."),
   mcq("Avant l'envoi, la vérification prioritaire porte sur :", ["Le nombre de paragraphes", "La présence d'une formule de politesse", "Dates, noms, montants et engagements", "La longueur des phrases"], 2, "Ce sont les éléments qui engagent.")
  ],
  [
   tf("Un courrier rédigé par l'assistant peut partir sans relecture s'il est bien écrit.", False, "Il part au nom de la direction : dates, noms, montants et promesses se relisent."),
   cloze("Pour un ton précis, le plus efficace est souvent de fournir un ___.", ["exemple", "glossaire", "sommaire"], 0, "Un modèle de ton guide mieux qu'un adjectif."),
   order("Remettez dans l'ordre la préparation d'une réunion.", ["Fixer les décisions attendues", "Faire rédiger l'ordre du jour", "Faire rédiger l'invitation", "Relire et envoyer"], "Les décisions attendues structurent le reste."),
   match("Associez chaque destinataire au ton adapté.", [["Administrateur", "Bref et orienté décision"], ["Partenaire institutionnel", "Protocolaire"], ["Prestataire en retard", "Ferme et courtois"]], "Le ton se règle dans la consigne."),
   tf("L'assistant utilisé dans le navigateur ne voit pas votre agenda.", True, "Vous lui donnez les créneaux et les contraintes.")
  ]),
 step("ms", 2, "Tableaux et chiffres", "50 min",
  ["Faire écrire et expliquer une formule de tableur", "Faire analyser un tableau fictif", "Vérifier chaque chiffre produit"],
  [
   ["Formules de tableur", "Décrivez le tableau (colonnes, ligne d'en-tête, ce que vous voulez calculer) et demandez la formule avec son explication. Testez-la sur trois lignes dont vous connaissez le résultat."],
   ["Analyser un tableau", "Sur un tableau fictif ou public, demandez les écarts, les tendances et les anomalies, avec la ligne concernée. L'assistant peut mal lire une colonne : vérifiez chaque constat sur le tableau."],
   ["Les calculs de l'assistant", "Un assistant qui calcule de tête peut se tromper sur une somme ou un pourcentage. Pour un résultat chiffré, demandez la formule à appliquer dans le tableur, ou l'usage de son outil de calcul s'il en dispose, et recalculez."],
   ["Données à ne pas saisir", "Salaires, données personnelles, comptes bancaires, budgets nominatifs de projets en cours : jamais dans un outil non validé. On s'exerce sur des tableaux fictifs ou des comptes publics."],
   ["Présenter des chiffres", "Demandez un commentaire de trois phrases sur un tableau : le fait principal, l'écart notable, la question à poser. Le commentaire se vérifie chiffre par chiffre."]
  ],
  [["insee", "INSEE : tableaux publics pour s'exercer."], ["skfluency", "Module Discernment : évaluer la production de l'assistant."]],
  [
   {"t": "Créez un tableau fictif de dix lignes (dépenses par mois et par poste). Demandez la formule du total par poste et celle de l'évolution en pourcentage.", "c": "Les deux formules donnent le bon résultat sur trois lignes contrôlées."},
   {"t": "Collez le tableau et demandez trois constats avec la ligne concernée.", "c": "Chaque constat a été vérifié sur le tableau."},
   {"t": "Demandez un commentaire de trois phrases pour un comité de direction.", "c": "Chaque chiffre du commentaire figure dans le tableau."}
  ],
  [
   mcq("Comment fiabiliser une formule proposée par l'assistant ?", ["La copier dans tout le classeur", "La tester sur des lignes au résultat connu", "Lui demander si elle est juste", "Choisir la plus longue"], 1, "Un test sur des cas connus révèle l'erreur."),
   mcq("L'assistant annonce une hausse de 12 % calculée de tête. Que faire ?", ["La reprendre telle quelle", "Recalculer dans le tableur", "Arrondir à 10 %", "Demander une deuxième estimation"], 1, "Un calcul de tête peut être faux."),
   mcq("Quelles données utiliser pour s'exercer ?", ["La paie du mois dernier", "Un tableau fictif ou des comptes publics", "Le budget nominatif d'un projet en cours", "Les relevés bancaires de la société"], 1, "Les données personnelles et financières internes restent hors de l'outil."),
   mcq("Un bon commentaire de tableau donne :", ["Tous les chiffres du tableau", "Le fait principal, l'écart notable, la question à poser", "Une conclusion sans chiffres", "Une prévision pour l'année suivante"], 1, "Trois phrases, chacune vérifiable."),
   mcq("L'assistant signale une anomalie en ligne 7. Que faire ?", ["La corriger sans regarder", "Vérifier la ligne 7 dans le tableau", "Supprimer la ligne", "Ignorer le signalement"], 1, "L'assistant peut mal lire une colonne.")
  ],
  [
   tf("Un pourcentage calculé de tête par l'assistant est fiable s'il est présenté avec assurance.", False, "Recalculez dans le tableur."),
   cloze("Une formule se teste sur des lignes dont on connaît le ___.", ["résultat", "titre", "format"], 0, "Le cas connu révèle l'erreur."),
   order("Remettez dans l'ordre l'analyse d'un tableau.", ["Décrire les colonnes", "Demander les constats avec la ligne", "Vérifier chaque constat", "Rédiger le commentaire"], "La vérification précède le commentaire."),
   match("Associez chaque donnée à la règle.", [["Salaires", "Jamais dans l'outil"], ["Tableau fictif", "Utilisable"], ["Comptes publics", "Utilisables"]], "La nature de la donnée décide."),
   tf("Demander la formule plutôt que le résultat rend le calcul vérifiable.", True, "Le tableur calcule ; vous contrôlez.")
  ]),
 step("ms", 3, "Procédures et documents qualité", "45 min",
  ["Faire structurer une procédure à partir de notes", "Comparer deux versions d'un document", "Vérifier une exigence à sa source"],
  [
   ["Structurer une procédure", "Donnez les étapes en vrac, les acteurs et les documents utilisés. Demandez une procédure avec objet, domaine d'application, responsabilités, étapes numérotées et enregistrements. Vous validez chaque étape avec les personnes qui la pratiquent."],
   ["Logigramme", "Demandez un logigramme en texte (étape, acteur, décision, suite) que vous reportez ensuite dans votre outil. Une flèche dans le mauvais sens est une erreur de fond."],
   ["Comparer deux versions", "Demandez un tableau des différences paragraphe par paragraphe, avec citation des deux rédactions. Recoupez avec la comparaison de votre traitement de texte."],
   ["Exigences de norme", "L'assistant cite volontiers une clause de norme de mémoire, parfois fausse. Une exigence se vérifie dans le texte de la norme dont vous disposez, jamais dans la réponse de l'assistant."],
   ["Dialoguer pour clarifier", "Demandez à l'assistant de vous poser les questions qu'un auditeur poserait sur la procédure. Les réponses que vous n'avez pas révèlent les manques."]
  ],
  [["skfluency", "Module Discernment : évaluer la production de l'assistant."], ["msgenfr", "Microsoft, IA générative en français : leçons sur la synthèse."]],
  [
   {"t": "Décrivez en vrac une procédure fictive (réception et enregistrement d'une demande de congés). Faites-la structurer.", "c": "Chaque étape a un acteur ; rien n'a été inventé."},
   {"t": "Demandez les questions qu'un auditeur poserait sur cette procédure.", "c": "Au moins une question révèle un manque réel."},
   {"t": "Modifiez trois points d'une copie et demandez la comparaison des deux versions.", "c": "Les trois modifications ont été trouvées, ou vous savez laquelle manque."}
  ],
  [
   mcq("Que fournir pour structurer une procédure ?", ["Le titre seul", "Étapes, acteurs et documents utilisés", "La norme complète", "L'organigramme de l'entreprise"], 1, "L'assistant structure ce que vous lui donnez."),
   mcq("L'assistant cite une clause de norme de mémoire. Que faire ?", ["La reprendre, la numérotation semble exacte", "La vérifier dans le texte de la norme", "Lui demander s'il est sûr", "La reformuler"], 1, "Seul le texte de la norme fait foi."),
   mcq("Comment fiabiliser une comparaison de versions ?", ["La refaire deux fois", "La recouper avec l'outil de comparaison", "Demander plus de détails", "Comparer à la mémoire de l'assistant"], 1, "L'outil déterministe voit chaque modification."),
   mcq("Quelle question fait apparaître les manques d'une procédure ?", ["Résume cette procédure", "Quelles questions un auditeur poserait-il ?", "Cette procédure est-elle bonne ?", "Traduis cette procédure"], 1, "Les questions sans réponse révèlent les manques."),
   mcq("Qui valide les étapes d'une procédure rédigée avec l'assistant ?", ["L'assistant lui-même", "Les personnes qui pratiquent la procédure", "Le premier lecteur venu", "Personne, elle est cohérente"], 1, "La procédure décrit une pratique réelle.")
  ],
  [
   tf("Une exigence de norme citée par l'assistant de mémoire peut être reprise dans un document qualité.", False, "Elle se vérifie dans le texte de la norme."),
   cloze("Un schéma qui enchaîne étapes, acteurs et décisions s'appelle un ___.", ["logigramme", "organigramme", "calendrier"], 0, "Il se vérifie comme un texte."),
   order("Remettez dans l'ordre la rédaction d'une procédure.", ["Lister les étapes en vrac", "Faire structurer", "Faire poser les questions d'auditeur", "Valider avec les acteurs"], "La validation humaine clôt la rédaction."),
   match("Associez chaque besoin à la consigne.", [["Procédure", "Objet, responsabilités, étapes"], ["Comparaison", "Tableau avec citations"], ["Audit à blanc", "Questions d'auditeur"]], "Chaque besoin a sa consigne type."),
   tf("Une flèche inversée dans un logigramme est une erreur de fond.", True, "Elle change l'ordre ou le responsable.")
  ]),
 step("ms", 4, "Comptes rendus, notes de direction et supports de CA", "45 min",
  ["Produire un compte rendu à partir de notes", "Rédiger une note de direction orientée décision", "Préparer la trame d'un support de conseil d'administration"],
  [
   ["Compte rendu", "À partir de notes brutes (jamais l'enregistrement d'une réunion confidentielle dans un outil non validé), demandez : décisions, actions avec responsable et échéance, points ouverts. Le reste est secondaire."],
   ["Note de direction", "Une note se construit autour de la décision attendue : objet, contexte, options, recommandation. Demandez ce plan explicitement ; sinon l'assistant raconte au lieu de conclure."],
   ["Résumé fidèle", "Fixez la longueur, le public et ce qui doit figurer. Demandez ce qui a été omis : un résumé élégant peut gommer une réserve ou une condition."],
   ["Support de CA", "Demandez une trame diapositive par diapositive : titre affirmatif, trois idées au plus, visuel suggéré. Les chiffres viennent de vos tableaux, jamais de l'assistant."],
   ["Délibérations", "Un projet de délibération ou de procès-verbal se relit mot à mot : une décision mal formulée engage l'entreprise. L'assistant propose une forme ; la formulation retenue est validée par qui de droit."]
  ],
  [["msgenfr", "Microsoft, IA générative en français : leçons sur la synthèse."], ["sk101", "Claude 101 : usages quotidiens, en anglais."]],
  [
   {"t": "À partir de notes fictives d'un comité de direction, faites produire un compte rendu décisions, actions, points ouverts.", "c": "Chaque action a un responsable et une échéance ; rien n'a été inventé."},
   {"t": "Faites rédiger une note de direction fictive (choix entre deux prestataires) avec recommandation en tête.", "c": "La recommandation tient en trois lignes."},
   {"t": "Facultatif : faites produire la trame d'un support de conseil d'administration de huit diapositives sur un sujet fictif.", "c": "Chaque titre est une phrase affirmative ; aucun chiffre n'a été inventé.", "opt": True}
  ],
  [
   mcq("Quelles rubriques sont prioritaires dans un compte rendu ?", ["Liste des présents et horaires", "Décisions, actions et points ouverts", "Résumé chronologique des échanges", "Citations exactes de chaque intervenant"], 1, "Ce sont les éléments sur lesquels on agit."),
   mcq("Quel plan demander pour une note de direction ?", ["Chronologie complète des échanges", "Objet, contexte, options, recommandation", "Questions puis réponses dans l'ordre reçu", "Un paragraphe unique, sans titres"], 1, "La note sert une décision : elle doit conclure."),
   mcq("D'où viennent les chiffres d'un support de CA ?", ["De l'assistant, qui les estime", "De vos tableaux validés", "D'un article de presse", "De la mémoire de l'assistant"], 1, "Un chiffre proposé par l'assistant sans base est une invention."),
   mcq("Peut-on transcrire une réunion confidentielle avec un outil grand public ?", ["Oui, si le fichier est supprimé après", "Non, sauf outil validé par l'entreprise", "Oui, si personne n'est nommé", "Oui, si la réunion dure moins d'une heure"], 1, "Le contenu reste confidentiel quel que soit le format."),
   mcq("Comment limiter le risque d'un résumé infidèle ?", ["Demander un résumé plus long", "Demander ce qui a été omis", "Demander un résumé en anglais", "Demander un résumé en points"], 1, "La liste des omissions rend les choix visibles.")
  ],
  [
   tf("Un résumé bien écrit est forcément fidèle.", False, "Il peut gommer une réserve ou une condition. Demandez les omissions."),
   cloze("Dans un compte rendu, chaque action a un responsable et une ___.", ["échéance", "couleur", "signature"], 0, "Sinon l'action ne sera pas suivie."),
   match("Associez chaque document à la consigne utile.", [["Compte rendu", "Décisions, actions, points ouverts"], ["Note de direction", "Recommandation en tête"], ["Support de CA", "Titres affirmatifs"]], "Chaque format a sa consigne type."),
   order("Remettez dans l'ordre la préparation d'un support de CA.", ["Fixer le message principal", "Demander la trame", "Insérer les chiffres validés", "Mettre en forme dans l'outil interne"], "Le message précède la forme."),
   tf("Un projet de délibération rédigé avec l'assistant se relit mot à mot.", True, "Une décision mal formulée engage l'entreprise.")
  ]),
 step("ms", 5, "Votre assistant de poste", "1 h",
  ["Configurer un projet pour une tâche récurrente", "Mesurer le temps gagné et la qualité", "Partager une méthode avec l'équipe"],
  [
   ["Projets et assistants personnalisés", "Claude (Projets), ChatGPT (Projets et GPTs), Copilot (agents), Le Chat (agents) et Gemini (Gems) enregistrent des instructions permanentes et des documents de référence. Comptes rendus, courriers types et commentaires de tableaux s'y prêtent bien."],
   ["Instructions permanentes", "Rôle, contexte du service, format de sortie, règles : ne rien inventer, signaler l'incertitude, ne jamais proposer un chiffre sans source. Testez-les sur trois cas fictifs avant de les adopter."],
   ["Documents de référence", "Seuls des documents publics ou validés pour cet usage : charte de rédaction, modèles vierges. Les connaissances d'un projet partagé sont visibles de ses membres."],
   ["Mesurer", "Notez pour une tâche : temps sans assistant, temps avec, corrections nécessaires. Sans mesure, l'impression de gain trompe dans les deux sens."],
   ["Partager", "Une consigne qui marche se partage : fiche d'une page (usage, consigne, limites, exemple fictif)."]
  ],
  [["sk101", "Claude 101 : projets et instructions."], ["oaiacad", "OpenAI Academy : projets et GPTs."]],
  [
   {"t": "Créez un projet (ou équivalent) pour une tâche récurrente de votre poste : instructions permanentes et un modèle vierge.", "c": "Trois essais sur des cas fictifs donnent un résultat de même qualité."},
   {"t": "Mesurez une tâche faite sans données internes (un courrier type) : temps sans et avec assistant.", "c": "Les deux temps et le nombre de corrections sont notés dans le carnet."},
   {"t": "Rédigez une fiche d'une page pour partager cette méthode avec un collègue.", "c": "Un collègue peut l'appliquer sans explication orale."}
  ],
  [
   mcq("À quoi servent les instructions permanentes d'un projet ?", ["À stocker les fichiers du service", "À appliquer les mêmes règles à chaque échange", "À augmenter la fenêtre de contexte", "À désactiver la recherche web"], 1, "Elles évitent de répéter rôle, format et règles."),
   mcq("Quels documents placer dans les connaissances d'un projet ?", ["Les tableaux de paie", "Documents publics ou validés pour cet usage", "Les courriels de la semaine", "Tous les fichiers du service"], 1, "Les connaissances sont lues à chaque échange et parfois partagées."),
   mcq("Avant d'adopter un assistant personnalisé, il faut :", ["Le partager à tout le service", "Le tester sur trois cas fictifs", "Lui donner un nom précis", "Activer toutes ses options"], 1, "Un test sur plusieurs cas révèle les consignes ambiguës."),
   mcq("Pourquoi mesurer le temps passé avec et sans assistant ?", ["Pour remplir un tableau de bord", "Parce que l'impression de gain peut tromper", "Parce que l'outil l'exige", "Pour choisir le modèle le moins cher"], 1, "La mesure tranche entre impression et réalité."),
   mcq("Quel format pour partager une méthode ?", ["Une capture d'écran de conversation", "Une fiche : usage, consigne, limites, exemple", "Un lien vers votre historique", "Un message oral en réunion"], 1, "La fiche se réutilise sans son auteur.")
  ],
  [
   tf("Les documents placés dans un projet partagé peuvent être vus par ses membres.", True, "D'où la règle : documents publics ou validés seulement."),
   cloze("Des consignes qui servent à chaque échange s'appellent des instructions ___.", ["permanentes", "cachées", "système"], 0, "Le terme varie selon l'outil ; le principe est le même."),
   match("Associez chaque outil à son nom de fonction.", [["Claude", "Projets"], ["ChatGPT", "GPTs"], ["Gemini", "Gems"]], "Les noms changent, la fonction est voisine."),
   order("Remettez dans l'ordre la mise en place d'un assistant de poste.", ["Choisir une tâche récurrente", "Écrire les instructions", "Tester sur trois cas fictifs", "Mesurer puis partager"], "Le partage vient après la preuve."),
   tf("Un gain de temps ressenti suffit pour généraliser une méthode.", False, "Sans mesure, l'impression trompe dans les deux sens.")
  ]),
]

METIER_PROFILS = {"cdt": CDT, "brevet": BREVET, "support": SUPPORT}
