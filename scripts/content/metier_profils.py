# Voies Métier par profil (révision du 26/11/2026, demande de Thomas).
# Principe : la voie Métier n'enseigne pas le métier. Elle montre comment utiliser l'IA de façon
# optimale pour les tâches courantes de ce métier (prospection, proposition commerciale, présentation,
# synthèse, tableaux...). Chaque question porte sur la manière de se servir de l'assistant :
# ce qu'il faut lui donner, comment le guider, ce qu'il faut vérifier, ce qui ne doit pas lui être confié.
# Les notions communes à plusieurs métiers portent le même titre (le schéma des notions s'en sert).
# Le juriste garde me1 à me5 (metier.py). Pratique autorisée au poste (cadre 1), données fictives ou publiques.
from socle import mcq, tf, cloze, order, match

COMP = [["produire", "formuler"], ["produire", "verifier"], ["verifier", "dialoguer"], ["produire", "organiser"], ["organiser", "automatiser"]]

def step(pid, n, titre, duree, obj, notions, res, ex, quiz, drills):
  return {"id": f"{pid}{n}", "cote": f"M{n}", "titre": titre, "duree": duree, "comp": COMP[n - 1], "cadre": 1,
          "obj": obj, "notions": notions, "res": res, "ex": ex, "quiz": quiz, "drills": drills}

R_FLU = ["skfluency", "Cours AI Fluency : décrire la tâche, le ton et le format, puis évaluer la réponse."]
R_MS = ["msgenfr", "Microsoft, cours d'IA générative en français : rédaction et synthèse."]
R_101 = ["sk101", "Claude 101 : usages quotidiens, projets et instructions."]
R_OAI = ["oaiacad", "OpenAI Academy : projets et GPTs."]

# ---------- Notions communes (mêmes titres dans toutes les voies) ----------
N_CONTEXTE = lambda ex: ["Le contexte d'abord", "L'assistant ne connaît ni la SATT, ni votre interlocuteur, ni votre objectif. Donnez-les en tête de demande : " + ex + ". Une demande nue produit un texte générique qu'il faudra tout réécrire."]
N_PLAN = ["Le plan avant le texte", "Demandez d'abord un plan, corrigez-le, puis faites rédiger partie par partie. Corriger un plan de dix lignes prend une minute ; corriger un texte de deux pages construit sur un mauvais plan prend une heure."]
N_RELIRE = ["Relire comme l'auteur", "Le document part sous votre nom. Relisez les chiffres, les dates, les noms et chaque engagement : l'assistant ajoute volontiers une promesse, un délai ou un chiffre que personne n'a décidé."]
N_DONNEES = lambda ex: ["Données fictives ou publiques", "Dans un outil non validé par l'entreprise, on travaille sur des documents publics ou sur des versions fictives de même structure. " + ex + " ne va pas dans l'assistant, même sans les noms."]
N_TRAME = ["Trame de présentation", "Demandez un plan diapositive par diapositive : un titre qui affirme le message, trois idées au plus, le visuel suggéré, puis les notes de l'orateur. La mise en forme se fait ensuite dans l'outil de présentation de l'entreprise."]
N_TITRES = ["Titres affirmatifs", "Un titre comme « Marché » ne dit rien ; « Le marché visé croît de façon régulière » porte le message. Demandez explicitement des titres en forme de phrase, puis vérifiez que chacun est vrai."]
N_CONTRA = ["Contradicteur", "Avant de présenter, demandez à l'assistant les trois objections les plus solides contre votre message. Il est plus utile de les découvrir à votre bureau qu'en séance."]
N_CHIFFRES = ["Les chiffres se recalculent", "L'assistant met en forme et compare ; il calcule mal de tête. Demandez-lui la formule plutôt que le résultat, et recalculez chaque total dans le tableur."]
N_WEB = ["Recherche web activée", "Pour des entreprises, un marché ou une actualité, activez la recherche web et exigez un lien par information. Sans recherche, l'assistant répond de mémoire : données datées, entreprises disparues, chiffres inventés."]
N_SOURCE = ["Remonter à la source", "Ouvrez chaque lien fourni : la page peut ne pas dire ce que l'assistant lui attribue. Un chiffre se cite depuis sa source d'origine, jamais depuis la réponse de l'assistant."]
N_MANQUE = ["Demander ce qui manque", "Demandez aussi ce qui n'y est pas : l'information absente, la rubrique oubliée, la question laissée sans réponse. Une absence ne se voit pas à la lecture rapide."]
N_CITATIONS = ["Exiger les citations", "Pour toute extraction ou comparaison, demandez un tableau avec le passage exact pour chaque ligne. Vous vérifiez alors en quelques secondes, ligne par ligne, au lieu de relire tout le document."]

N_PROJETS = ["Projets et assistants personnalisés", "Claude (Projets), ChatGPT (Projets et GPTs), Copilot (agents), Le Chat (agents) et Gemini (Gems) enregistrent des instructions permanentes et des documents de référence. Une tâche que vous faites chaque semaine y gagne en régularité."]
N_INSTR = ["Instructions permanentes", "Rôle, public visé, format de sortie et règles : ne rien inventer, citer la source de chaque chiffre, signaler l'incertitude, ne rien promettre en votre nom. Testez-les sur trois cas fictifs avant de les adopter."]
N_REF = ["Documents de référence", "Modèles vierges, charte de rédaction, documents publics : seulement ce qui est validé pour cet usage, jamais un dossier en cours. Les connaissances d'un projet partagé sont visibles de ses membres."]
N_MESURE = ["Mesurer", "Notez pour une tâche le temps sans assistant, le temps avec, et les corrections nécessaires. Sans mesure, l'impression de gain trompe dans les deux sens."]
N_PARTAGE = ["Partager", "Une consigne qui marche se partage avec les collègues du même métier : fiche d'une page (usage, consigne, limites, exemple fictif). C'est ainsi qu'une équipe progresse au même rythme."]

def assistant_de_poste(pid, titre, taches, ex1, ex2):
  return step(pid, 5, titre, "1 h",
   ["Configurer un projet pour une tâche récurrente du métier", "Mesurer le temps gagné et la qualité", "Partager la méthode avec l'équipe"],
   [N_PROJETS, N_INSTR, N_REF, N_MESURE, N_PARTAGE],
   [R_101, R_OAI],
   [
    {"t": "Créez un projet (ou équivalent) pour une tâche récurrente de votre poste, par exemple " + taches + " : instructions permanentes et un modèle vierge.", "c": "Trois essais sur des cas fictifs donnent un résultat de même qualité."},
    {"t": ex1, "c": "Les deux temps et le nombre de corrections sont notés dans le carnet."},
    {"t": ex2, "c": "Un collègue du même métier peut l'appliquer sans explication orale."}
   ],
   [
    mcq("À quoi servent les instructions permanentes d'un projet ?", ["À stocker durablement les dossiers en cours du service", "À appliquer les mêmes règles à chaque échange", "À agrandir la fenêtre de contexte", "À couper la recherche web"], 1, "Elles évitent de répéter rôle, format et règles à chaque demande."),
    mcq("Quels documents placer dans les connaissances d'un projet ?", ["Les dossiers en cours, pour gagner du temps", "Des modèles publics ou validés pour cet usage", "Les courriels reçus dans la semaine, triés par expéditeur", "Tous les fichiers du service sans tri"], 1, "Les connaissances sont lues à chaque échange et parfois partagées."),
    mcq("Avant d'adopter un assistant personnalisé, il faut :", ["Le partager tout de suite à toute l'équipe", "Le tester sur trois cas fictifs différents", "Lui donner un nom facile à retenir", "Activer toutes les options disponibles"], 1, "Plusieurs cas révèlent les consignes ambiguës."),
    mcq("Pourquoi mesurer le temps passé avec et sans assistant ?", ["Pour remplir un tableau de bord", "Parce que l'impression de gain peut tromper", "Parce que l'outil le demande", "Pour choisir l'offre d'abonnement la moins chère du marché"], 1, "La mesure tranche entre impression et réalité."),
    mcq("Quel format pour partager une méthode avec un collègue ?", ["Une capture d'écran de la conversation qui a bien marché", "Une fiche : usage, consigne, limites, exemple", "Un lien vers votre historique personnel", "Une explication orale en réunion"], 1, "La fiche se réutilise sans son auteur.")
   ],
   [
    tf("Les documents placés dans un projet partagé peuvent être vus par ses membres.", True, "D'où la règle : documents publics ou validés seulement."),
    cloze("Des consignes qui servent à chaque échange s'appellent des instructions ___.", ["permanentes", "cachées", "système"], 0, "Le terme varie selon l'outil ; le principe est le même."),
    match("Associez chaque outil à son nom de fonction.", [["Claude", "Projets"], ["ChatGPT", "GPTs"], ["Gemini", "Gems"]], "Les noms changent, la fonction est voisine."),
    order("Remettez dans l'ordre la mise en place d'un assistant de poste.", ["Choisir une tâche récurrente", "Écrire les instructions", "Tester sur trois cas fictifs", "Mesurer puis partager"], "Le partage vient après la preuve."),
    tf("Un gain de temps ressenti suffit pour généraliser une méthode.", False, "Sans mesure, l'impression trompe dans les deux sens.")
   ])

# ---------- Chargé de transfert ----------
CDT = [
 step("mt", 1, "Courriels de prospection avec l'IA", "40 min",
  ["Faire rédiger un premier courriel de prospection personnalisé", "Adapter le message à chaque cible sans tout réécrire", "Garder la main sur ce qui est dit et promis"],
  [
   N_CONTEXTE("la technologie en trois lignes publiques, l'entreprise visée, ce que vous attendez d'elle (un échange, une démonstration) et ce qui ne doit pas être dit"),
   ["Personnaliser sans recopier", "Donnez une base commune, puis pour chaque cible deux ou trois faits publics (son activité, un produit, une actualité trouvée en recherche web). Demandez une variante par cible : le message change d'accroche, pas de fond."],
   ["Le ton se règle", "Précisez le registre et la longueur : « cent mots, courtois et direct, sans superlatif ». Un ancien courriel fictif qui a bien marché vaut souvent mieux qu'une description du ton voulu."],
   N_RELIRE,
   N_DONNEES("Une déclaration d'invention, un résultat non publié ou le nom d'un industriel en discussion")
  ],
  [R_FLU, R_MS],
  [
   {"t": "Pour une technologie fictive (un capteur imaginaire de qualité de l'eau), faites rédiger un courriel de prospection de cent mots à partir de trois lignes de description publique.", "c": "Le courriel tient en cent mots ; aucune information non publique ni promesse n'y figure."},
   {"t": "Donnez deux entreprises fictives avec deux faits chacune et demandez une variante du courriel par entreprise.", "c": "Seule l'accroche change ; vous savez quelle consigne l'a permis."},
   {"t": "Facultatif : faites rédiger une relance à quinze jours, en deux tons.", "c": "Vous savez quel ton vous enverriez et pourquoi.", "opt": True}
  ],
  [
   mcq("Que donner à l'assistant avant de demander un courriel de prospection ?", ["Uniquement le nom de l'entreprise visée", "Technologie publique, cible, attente et limites", "La déclaration d'invention complète du projet", "Une liste de formules de politesse à utiliser"], 1, "Avec ces éléments, le premier jet est presque toujours utilisable."),
   mcq("Comment obtenir une version par cible sans tout réécrire ?", ["Recommencer une conversation pour chaque cible", "Donner une base commune et des faits propres à chaque cible", "Demander dix variantes au hasard et choisir", "Changer d'assistant pour chaque entreprise"], 1, "Le fond reste commun ; l'accroche s'appuie sur des faits de la cible."),
   mcq("L'assistant écrit « nous pouvons vous accorder une exclusivité ». Que faire ?", ["Garder la phrase, elle rend l'offre attractive", "La retirer, sauf si c'est décidé", "La remplacer par « tout est négociable »", "Demander à l'assistant de la justifier"], 1, "Aucun engagement ne part sans décision."),
   mcq("Quelle information ne doit jamais aller dans l'assistant non validé ?", ["Le nom public de l'entreprise visée", "Un résultat technique non publié", "La longueur souhaitée du courriel", "Le ton attendu pour la relance"], 1, "Ce qui n'est ni publié ni protégé reste hors de l'outil."),
   mcq("Comment régler le ton le plus sûrement ?", ["Fournir un ancien courriel fictif comme modèle", "Écrire la consigne en majuscules", "Demander un ton « professionnel »", "Laisser l'assistant choisir seul"], 0, "Un exemple guide mieux qu'un adjectif.")
  ],
  [
   tf("Un courriel de prospection rédigé par l'assistant peut partir sans relecture s'il est bien écrit.", False, "Il part sous votre nom : faits, chiffres et promesses se relisent."),
   cloze("Pour personnaliser un courriel, donnez à l'assistant des faits ___ sur chaque cible.", ["publics", "supposés", "confidentiels"], 0, "Des faits vérifiables, trouvés en recherche web par exemple."),
   order("Remettez dans l'ordre la préparation d'une campagne de prospection.", ["Écrire la base commune", "Ajouter les faits de chaque cible", "Faire rédiger les variantes", "Relire chaque engagement"], "La relecture ferme la boucle."),
   match("Associez chaque consigne à son effet.", [["Cent mots", "Longueur maîtrisée"], ["Ancien courriel fictif", "Ton reproduit"], ["Ce qui ne doit pas être dit", "Pas de fuite ni de promesse"]], "Chaque consigne règle un défaut précis."),
   tf("Préciser ce qui ne doit pas être dit fait partie d'une bonne consigne.", True, "Les limites évitent les promesses implicites et les fuites.")
  ]),
 step("mt", 2, "Proposition commerciale cohérente avec le business plan", "50 min",
  ["Faire structurer une proposition à partir d'un business plan fictif", "Faire vérifier la cohérence des chiffres entre les deux documents", "Garder la décision sur les conditions proposées"],
  [
   N_PLAN,
   ["Cohérence avec le business plan", "Donnez les deux documents et demandez un tableau : chaque chiffre de la proposition, la ligne du business plan qui le justifie, et « non trouvé » s'il n'y en a pas. Les écarts sautent aux yeux, et les chiffres orphelins aussi."],
   N_CHIFFRES,
   N_MANQUE,
   N_DONNEES("Un business plan réel, des conditions financières en négociation ou le nom d'un partenaire")
  ],
  [R_FLU, R_MS],
  [
   {"t": "Rédigez un business plan fictif d'une demi-page (cinq lignes de chiffres). Faites produire le plan d'une proposition commerciale, corrigez-le, puis faites rédiger.", "c": "Le plan a été corrigé avant la rédaction ; vous savez ce que vous avez changé."},
   {"t": "Demandez le tableau de correspondance entre chaque chiffre de la proposition et le business plan.", "c": "Chaque ligne a été vérifiée ; au moins un chiffre orphelin ou un écart a été trouvé, ou vous avez constaté qu'il n'y en avait pas."},
   {"t": "Demandez ce qui manque à la proposition pour qu'un industriel puisse décider.", "c": "Au moins une absence pertinente est confirmée par votre lecture."}
  ],
  [
   mcq("Par quoi commencer une proposition commerciale avec l'assistant ?", ["Demander directement le texte complet", "Faire produire puis corriger un plan", "Lui demander de fixer les prix", "Lui donner le dossier du partenaire"], 1, "Un plan se corrige en une minute ; un texte construit sur un mauvais plan, en une heure."),
   mcq("Comment faire vérifier la cohérence avec le business plan ?", ["Demander si les deux documents sont cohérents", "Un tableau chiffre par chiffre, avec la ligne qui le justifie", "Relire les deux documents l'un après l'autre", "Résumer les deux documents en cinq lignes"], 1, "Le tableau rend chaque écart visible et vérifiable."),
   mcq("L'assistant calcule un total de 412 000 €. Que faire ?", ["Le reprendre, l'ordre de grandeur est plausible", "Recalculer dans le tableur", "Demander à l'assistant s'il est sûr", "Arrondir à 400 000 €"], 1, "Il calcule mal de tête : la formule et le tableur font foi."),
   mcq("Que signifie « non trouvé » dans le tableau de correspondance ?", ["Un chiffre de la proposition sans appui dans le business plan", "Une erreur de l'assistant à ignorer", "Un chiffre confidentiel à retirer du document", "Une ligne du business plan à supprimer"], 0, "Un chiffre orphelin doit être justifié ou retiré."),
   mcq("Qui décide des conditions proposées à l'industriel ?", ["L'assistant, d'après le business plan", "Vous et votre hiérarchie", "Le premier relecteur venu", "L'industriel, après lecture"], 1, "L'assistant structure et vérifie ; la décision reste humaine.")
  ],
  [
   tf("Demander « ces deux documents sont-ils cohérents ? » suffit à vérifier une proposition.", False, "Exigez un tableau chiffre par chiffre, sinon la réponse reste générale."),
   cloze("Un chiffre de la proposition sans appui dans le business plan est un chiffre ___.", ["orphelin", "arrondi", "confidentiel"], 0, "Il doit être justifié ou retiré."),
   order("Remettez dans l'ordre la préparation d'une proposition.", ["Faire produire le plan", "Corriger le plan", "Faire rédiger partie par partie", "Vérifier les chiffres avec le tableau"], "La vérification chiffrée clôt le travail."),
   match("Associez chaque demande à son intérêt.", [["Tableau de correspondance", "Écarts visibles"], ["Ce qui manque", "Absences repérées"], ["Formule plutôt que résultat", "Calcul vérifiable"]], "Chaque demande vise un risque précis."),
   tf("Un total calculé par l'assistant se recalcule dans le tableur.", True, "Une erreur de calcul est fréquente et peu visible.")
  ]),
 step("mt", 3, "Repérer des cibles et suivre un marché", "45 min",
  ["Mener une recherche web contrôlée sur un secteur", "Construire une liste de cibles vérifiée", "Mettre en place une veille récurrente"],
  [
   N_WEB,
   N_SOURCE,
   ["Une liste à vérifier", "Demandez un tableau des entreprises (activité, taille, implantation, lien). Vérifiez chaque ligne : une entreprise peut avoir été rachetée, avoir changé d'activité ou ne pas exister. La liste est un point de départ, jamais une cible validée."],
   ["Veille récurrente", "Enregistrez une consigne de veille (sujet, sources préférées, période, format) et relancez-la chaque mois. La consigne enregistrée garde la méthode d'une fois sur l'autre."],
   ["Dialoguer pour affiner", "La première liste est large. Resserrez par relances ciblées : « seulement les PME », « seulement celles qui ont déjà acheté une licence », « classe par proximité avec notre technologie, en justifiant »."]
  ],
  [R_FLU, R_101],
  [
   {"t": "Avec la recherche web activée, faites établir la liste de dix entreprises d'un secteur de votre choix, avec un lien par entreprise.", "c": "Vous avez ouvert au moins cinq liens ; les erreurs sont notées dans le carnet."},
   {"t": "Resserrez la liste par deux relances, puis demandez un classement justifié.", "c": "Vous savez dire quelle relance a le plus amélioré la liste."},
   {"t": "Facultatif : écrivez une consigne de veille mensuelle et enregistrez-la.", "c": "La consigne est dans votre bibliothèque.", "opt": True}
  ],
  [
   mcq("Pourquoi activer la recherche web pour une liste d'entreprises ?", ["Pour obtenir une réponse plus longue", "Sans elle, l'assistant répond de mémoire", "Parce que l'outil refuse sinon de répondre", "Pour masquer les entreprises disparues"], 1, "Sa mémoire s'arrête à une date de coupure."),
   mcq("Un article cité par l'assistant donne la taille d'un marché. Que faire ?", ["La reprendre telle quelle", "Remonter à l'étude d'origine et à son année", "La diviser par deux par prudence", "Demander à l'assistant si elle est exacte"], 1, "Seule la source d'origine se cite."),
   mcq("La liste d'entreprises produite par l'assistant est :", ["Une cible validée à contacter", "Un point de départ à vérifier", "Une liste complète du secteur", "Une source citable en comité"], 1, "Chaque ligne se vérifie avant usage."),
   mcq("Comment resserrer une liste trop large ?", ["Recommencer la même demande", "Relancer avec un critère précis à chaque fois", "Demander une liste plus longue", "Changer d'assistant"], 1, "Une relance ciblée vaut mieux qu'une nouvelle demande vague."),
   mcq("Comment rendre une veille mensuelle régulière ?", ["Reformuler la demande chaque mois", "Enregistrer une consigne de veille réutilisable", "Demander à l'assistant de s'en souvenir", "Changer d'assistant chaque mois"], 1, "La consigne enregistrée garde la méthode.")
  ],
  [
   tf("Un chiffre repris par plusieurs articles est forcément fiable.", False, "Il peut circuler sans source ; remontez à l'origine."),
   cloze("Avant de citer une information, ouvrez chaque ___ fourni par l'assistant.", ["lien", "onglet", "menu"], 0, "La page peut ne pas dire ce qui lui est attribué."),
   order("Remettez dans l'ordre une recherche de cibles fiable.", ["Activer la recherche web", "Demander un tableau avec liens", "Ouvrir chaque lien", "Resserrer par relances"], "La vérification précède l'affinage."),
   match("Associez chaque relance à son effet.", [["Seulement les PME", "Liste resserrée"], ["Classe en justifiant", "Priorités explicites"], ["Un lien par ligne", "Vérification possible"]], "Chaque relance précise la demande."),
   tf("L'assistant voit les bases de données payantes auxquelles la SATT est abonnée.", False, "Il ne voit que le web public et ce que vous lui fournissez.")
  ]),
 step("mt", 4, "Présentations pour comités et industriels", "45 min",
  ["Faire produire une trame de présentation", "Obtenir des titres qui portent le message", "Préparer les objections avant la séance"],
  [
   N_CONTEXTE("le public (comité d'investissement, industriel, laboratoire), la décision attendue, la durée et les chiffres validés"),
   N_TRAME,
   N_TITRES,
   N_CONTRA,
   N_CHIFFRES
  ],
  [R_MS, R_101],
  [
   {"t": "Pour un projet fictif, faites produire la trame d'une présentation de huit diapositives à un comité, avec titres affirmatifs et notes de l'orateur.", "c": "Chaque titre est une phrase vraie ; aucun chiffre n'a été inventé."},
   {"t": "Demandez la version de la même trame pour un industriel, en six diapositives.", "c": "Vous savez ce qui a changé entre les deux publics."},
   {"t": "Demandez les trois objections les plus solides contre votre recommandation.", "c": "Chaque objection a une réponse dans le carnet."}
  ],
  [
   mcq("Que donner à l'assistant avant de demander une trame ?", ["Le titre de la présentation seulement", "Public, décision attendue, durée et chiffres validés", "Le dossier complet du projet", "Une présentation d'un concurrent"], 1, "Le public et la décision attendue structurent tout le reste."),
   mcq("Quel titre de diapositive est le plus utile ?", ["Marché", "Le marché visé croît de façon régulière", "Données", "Annexe 2"], 1, "Un titre affirmatif porte le message."),
   mcq("L'assistant propose un chiffre de marché pour illustrer une diapositive. Que faire ?", ["Le garder s'il paraît plausible", "Le remplacer par un chiffre sourcé que vous avez vérifié", "L'arrondir pour qu'il paraisse moins précis", "Le déplacer dans une annexe"], 1, "Un chiffre sans source est une invention."),
   mcq("Pourquoi demander les objections avant la séance ?", ["Pour allonger la présentation", "Pour préparer les réponses", "Pour laisser l'assistant décider", "Pour remplacer l'avis du comité"], 1, "On les découvre à son bureau plutôt qu'en séance."),
   mcq("Où se fait la mise en forme finale ?", ["Dans l'assistant, diapositive par diapositive", "Dans l'outil de présentation de l'entreprise", "Dans un logiciel de dessin", "Dans le courriel d'envoi"], 1, "L'assistant prépare le fond et la trame.")
  ],
  [
   tf("Un titre de diapositive doit nommer le thème plutôt qu'affirmer un message.", False, "Le titre affirmatif dit ce que la diapositive démontre."),
   cloze("Avant une séance, faites jouer à l'assistant le rôle de ___.", ["contradicteur", "secrétaire", "traducteur"], 0, "Les objections se préparent à l'avance."),
   order("Remettez dans l'ordre la préparation d'une présentation.", ["Fixer le message et le public", "Faire produire la trame", "Vérifier titres et chiffres", "Préparer les objections"], "Le message précède la forme."),
   match("Associez chaque public à la consigne utile.", [["Comité", "Décision attendue en tête"], ["Industriel", "Valeur pour lui en premier"], ["Laboratoire", "Suite donnée à ses travaux"]], "Le public règle l'angle de la trame."),
   tf("Les notes de l'orateur peuvent être préparées avec l'assistant.", True, "Elles se relisent comme le reste.")
  ]),
 assistant_de_poste("mt", "Votre assistant de chargé de transfert", "les courriels de prospection ou les trames de comité",
  "Mesurez la préparation d'un courriel de prospection fictif sans puis avec l'assistant.",
  "Rédigez une fiche d'une page pour partager cette méthode avec les autres chargés de transfert."),
]

# ---------- Ingénieur brevet ----------
BREVET = [
 step("mb", 1, "Expliquer un document publié avec l'IA", "40 min",
  ["Faire résumer un document publié pour un lecteur précis", "Faire reformuler un passage technique sans en changer le sens", "Garder pour soi toute appréciation de fond"],
  [
   N_CONTEXTE("le lecteur (chargé de transfert, chercheur, direction), ce qu'il doit comprendre, la longueur et ce qui doit absolument figurer"),
   ["Résumer pour quelqu'un", "Un même document donne des résumés très différents selon le lecteur. Demandez-en deux, pour deux lecteurs, et comparez : vous verrez ce que la consigne change."],
   ["Ce que l'assistant ne tranche pas", "Ajoutez à la consigne « sans avis sur la portée ni sur la validité » : l'assistant ajoute volontiers une appréciation. Ces appréciations restent celles de l'ingénieur brevet."],
   N_CITATIONS,
   N_DONNEES("Un projet de demande, une description reçue d'un inventeur ou un document non publié")
  ],
  [R_FLU, ["espacenet", "Espacenet : documents publiés pour s'exercer."]],
  [
   {"t": "Choisissez un brevet publié dans un domaine que vous connaissez. Faites-en produire deux résumés de dix lignes : pour un chargé de transfert, puis pour la direction.", "c": "Vous savez ce que la consigne de lecteur a changé ; les deux résumés ont été comparés au texte."},
   {"t": "Faites reformuler un passage technique en langage courant, avec la citation de chaque phrase d'origine.", "c": "Chaque reformulation a été vérifiée contre sa citation."},
   {"t": "Facultatif : faites rédiger un courriel fictif de demande de compléments à un inventeur imaginaire.", "c": "Chaque question du courriel appelle une réponse précise.", "opt": True}
  ],
  [
   mcq("Sur quel document s'exercer à résumer avec l'assistant ?", ["Un projet de demande avant dépôt", "Un document publié, copié depuis une base officielle", "La description reçue d'un inventeur", "Un rapport interne non publié"], 1, "Un document publié est public."),
   mcq("Qu'est-ce qui change le plus un résumé produit par l'assistant ?", ["La police du document source", "Le lecteur indiqué dans la consigne", "La longueur du document source", "L'heure de la demande"], 1, "Le lecteur décide de ce qui est retenu."),
   mcq("L'assistant ajoute « ce brevet semble solide ». Que faire ?", ["Le garder, c'est rassurant pour le lecteur", "Le retirer et préciser la limite dans la consigne", "Le remplacer par « très solide »", "Lui demander un pourcentage"], 1, "L'appréciation de fond reste la vôtre."),
   mcq("Pourquoi demander la citation de chaque phrase reformulée ?", ["Pour allonger le texte", "Pour vérifier que le sens n'a pas changé", "Pour respecter la mise en page", "Pour traduire plus vite"], 1, "La citation rend la vérification rapide."),
   mcq("Avant d'envoyer un résumé à la direction, la vérification prioritaire porte sur :", ["La présence d'une formule de politesse", "La fidélité au document et l'absence d'avis ajouté", "La longueur des phrases", "Le nombre de paragraphes"], 1, "C'est là que l'assistant peut dériver.")
  ],
  [
   tf("Une description d'invention reçue d'un inventeur peut aller dans un outil grand public si elle est courte.", False, "Ce qui n'est pas publié reste hors de l'outil."),
   cloze("Pour vérifier une reformulation, exigez la ___ de chaque phrase d'origine.", ["citation", "traduction", "date"], 0, "La comparaison se fait alors en quelques secondes."),
   match("Associez chaque lecteur à la consigne adaptée.", [["Chargé de transfert", "Problème, solution, applications"], ["Direction", "Enjeu en trois lignes"], ["Chercheur", "Lien avec ses travaux"]], "Le lecteur décide du contenu."),
   order("Remettez dans l'ordre la préparation d'un résumé fiable.", ["Copier le document publié", "Indiquer lecteur et limites", "Faire résumer avec citations", "Vérifier contre le texte"], "La vérification clôt l'exercice."),
   tf("Préciser « sans avis sur la validité » évite que l'assistant n'ajoute une appréciation.", True, "Il en ajoute volontiers sans consigne contraire.")
  ]),
 step("mb", 2, "Extraire et comparer avec citations", "50 min",
  ["Faire extraire des informations d'un document publié dans un tableau", "Faire comparer deux documents publiés", "Contrôler vite ce que l'assistant a produit"],
  [
   N_CITATIONS,
   ["La valeur « non mentionné »", "Demandez des champs précis et la valeur « non mentionné » quand l'information manque. Sans cette consigne, l'assistant risque de combler le vide avec une valeur plausible."],
   N_MANQUE,
   ["Recouper au hasard", "Contrôlez au moins trois lignes du tableau sur le texte, choisies au hasard. Un mot remplacé par un synonyme peut changer le sens d'une phrase technique."],
   N_DONNEES("Un document non publié ou un projet en cours")
  ],
  [R_FLU, ["espacenet", "Espacenet : documents publiés pour s'exercer."]],
  [
   {"t": "Sur un document publié, faites extraire dans un tableau des champs de votre choix, avec citation et « non mentionné » si absent.", "c": "Trois lignes ont été vérifiées sur le texte ; les écarts sont notés."},
   {"t": "Faites comparer deux documents publiés du même domaine, ligne par ligne, avec citations.", "c": "Au moins une différence relevée a été confirmée par votre lecture."},
   {"t": "Demandez ce qui figure dans l'un et pas dans l'autre.", "c": "Au moins une absence est confirmée par votre lecture."}
  ],
  [
   mcq("Pourquoi exiger la citation exacte dans un tableau d'extraction ?", ["Pour allonger le tableau", "Pour vérifier chaque ligne sur le texte", "Parce que l'assistant ne sait pas résumer", "Pour respecter la mise en page"], 1, "La citation rend le contrôle rapide."),
   mcq("Le document ne contient pas un des champs demandés. Que prévoir dans la consigne ?", ["Rien, l'assistant le verra", "La valeur « non mentionné » si absent", "De le déduire du reste du texte", "De retirer ce champ du tableau"], 1, "Sinon l'assistant risque de deviner."),
   mcq("Quelle question fait apparaître ce que la lecture rapide manque ?", ["Résume ces deux documents", "Qu'est-ce qui figure dans l'un et pas dans l'autre ?", "Ces documents se ressemblent-ils ?", "Traduis le premier document"], 1, "Une absence ne se voit pas ; il faut la demander."),
   mcq("Comment contrôler un tableau de vingt lignes produit par l'assistant ?", ["Lui demander s'il est sûr de chaque ligne", "Vérifier au moins trois lignes au hasard sur le texte", "Le relire sans ouvrir le document", "Le faire refaire par un second assistant"], 1, "Le sondage révèle les erreurs systématiques."),
   mcq("Qui tire les conclusions d'une comparaison ?", ["L'assistant, qui a tout lu", "Vous, à partir du tableau vérifié", "Un second modèle chargé de juger", "Le destinataire du tableau"], 1, "L'assistant aligne ; vous concluez.")
  ],
  [
   tf("Un tableau produit par l'assistant peut fonder seul une conclusion technique.", False, "Il se vérifie, puis vous concluez."),
   cloze("Quand une information manque, exigez la valeur « non ___ ».", ["mentionné", "confidentiel", "traduit"], 0, "Sinon l'assistant comble le vide."),
   order("Remettez dans l'ordre une comparaison fiable.", ["Choisir les champs", "Faire le tableau avec citations", "Demander les absences", "Vérifier trois lignes au hasard"], "La vérification par sondage clôt la comparaison."),
   match("Associez chaque consigne à son intérêt.", [["Citation exacte", "Contrôle ligne par ligne"], ["Non mentionné", "Pas de valeur devinée"], ["Ce qui manque", "Absences visibles"]], "Chaque consigne vise un risque précis."),
   tf("Remplacer un mot par un synonyme peut changer le sens d'une phrase technique.", True, "D'où la vérification sur le texte.")
  ]),
 step("mb", 3, "Préparer une recherche avec l'IA", "45 min",
  ["Faire proposer mots-clés, synonymes et traductions", "Garder la base officielle comme seule source", "Repérer les références inventées"],
  [
   ["L'assistant prépare, la base répond", "L'assistant est utile en amont : mots-clés, synonymes, traductions, formulations de requête. La recherche elle-même se fait dans la base officielle (Espacenet, base de l'INPI, Lens, Google Patents)."],
   ["Numéros à vérifier", "Sans recherche web, les assistants inventent volontiers des références plausibles : numéros, titres, auteurs. Toute référence se retrouve dans la base ; un numéro introuvable est une hallucination."],
   N_SOURCE,
   ["Dialoguer pour affiner", "Les premiers mots-clés sont larges. Relancez : « plus technique », « termes utilisés dans les années 2000 », « équivalents allemands ». Chaque relance ajoute des pistes que vous testez dans la base."],
   N_DONNEES("Une invention non déposée")
  ],
  [["espacenet", "Espacenet : recherche par mots-clés et par classification."], ["hal", "HAL : archive ouverte des publications scientifiques."]],
  [
   {"t": "Pour un objet technique banal (un ouvre-bouteille à levier), faites proposer des mots-clés, synonymes et traductions, puis lancez la recherche dans Espacenet.", "c": "Vous savez quels mots-clés ont donné des résultats pertinents."},
   {"t": "Sans recherche web, demandez trois références sur cet objet avec leur numéro. Cherchez chaque numéro dans la base.", "c": "Vous savez combien de références existent et correspondent au sujet."}
  ],
  [
   mcq("L'assistant donne trois références avec leur numéro. Que faire ?", ["Les citer, les numéros sont précis", "Les retrouver une par une dans la base", "Lui demander s'il en est certain", "Les garder pour un usage interne"], 1, "Un numéro plausible peut être inventé."),
   mcq("Où l'assistant est-il le plus utile dans une recherche ?", ["Pour conclure sur ce qui existe déjà", "Pour préparer mots-clés, synonymes et traductions", "Pour remplacer la base de données", "Pour décider de la suite à donner"], 1, "La recherche elle-même se fait dans la base."),
   mcq("Comment élargir une liste de mots-clés trop pauvre ?", ["Recommencer la même demande", "Relancer avec un angle précis à chaque fois", "Demander une liste dix fois plus longue", "Changer d'assistant"], 1, "Chaque relance ciblée ajoute des pistes."),
   mcq("Sur quoi s'exercer à préparer une recherche ?", ["L'invention qu'un laboratoire vient de déclarer", "Un objet banal ou un document déjà publié", "Un projet de demande à déposer bientôt", "Une description obtenue en réunion"], 1, "Une invention non déposée reste hors de l'outil."),
   mcq("Un numéro donné par l'assistant est introuvable dans la base. C'est :", ["Une erreur de la base", "Probablement une référence inventée", "Un document confidentiel", "Une traduction ratée"], 1, "Un numéro introuvable est à traiter comme une hallucination.")
  ],
  [
   tf("Un numéro donné de mémoire par l'assistant est fiable s'il a le bon format.", False, "Le format ne prouve rien ; seule la base fait foi."),
   cloze("La recherche elle-même se fait dans la ___ officielle.", ["base", "messagerie", "conversation"], 0, "L'assistant prépare, la base répond."),
   order("Remettez dans l'ordre une recherche préparée avec l'IA.", ["Faire proposer les mots-clés", "Affiner par relances", "Lancer la recherche dans la base", "Vérifier chaque référence"], "La base reste la source."),
   match("Associez chaque tâche à qui la fait.", [["Proposer des synonymes", "L'assistant"], ["Trouver les documents", "La base officielle"], ["Juger la pertinence", "L'ingénieur brevet"]], "Chacun son rôle."),
   tf("Décrire une invention non déposée dans un outil grand public expose l'invention.", True, "On s'exerce sur un objet banal ou un document publié.")
  ]),
 step("mb", 4, "Présentations et notes pour non-spécialistes", "45 min",
  ["Faire produire une trame de présentation sur un sujet technique", "Rendre un sujet technique lisible pour la direction ou un comité", "Vérifier que la simplification n'a rien faussé"],
  [
   N_CONTEXTE("le public, ce qu'il doit retenir ou décider, la durée et les informations publiques ou validées à utiliser"),
   N_TRAME,
   N_TITRES,
   ["Simplifier sans fausser", "Demandez une analogie ou un exemple concret, puis vérifiez qu'il ne dit rien de faux. Une image parlante mais inexacte se retient mieux que la réalité."],
   N_CONTRA
  ],
  [R_MS, R_101],
  [
   {"t": "Faites produire la trame d'une présentation de six diapositives expliquant un sujet technique public à la direction.", "c": "Chaque titre est une phrase vraie ; chaque simplification a été vérifiée."},
   {"t": "Demandez deux analogies pour une notion technique et choisissez celle qui ne fausse rien.", "c": "Vous savez dire pourquoi l'autre analogie était trompeuse."},
   {"t": "Facultatif : demandez les trois questions qu'un administrateur poserait.", "c": "Chaque question a une réponse dans le carnet.", "opt": True}
  ],
  [
   mcq("Que donner à l'assistant avant de demander une trame ?", ["Le titre de la présentation seulement", "Public, message à retenir, durée et informations validées", "Le dossier technique complet", "Une présentation d'un autre service"], 1, "Le public et le message structurent tout le reste."),
   mcq("L'assistant propose une analogie parlante. Que vérifier ?", ["Qu'elle est courte", "Qu'elle ne dit rien de faux", "Qu'elle fait sourire", "Qu'elle est originale"], 1, "Une image inexacte se retient mieux que la réalité."),
   mcq("Quel titre de diapositive est le plus utile ?", ["Contexte technique", "Le procédé réduit la consommation d'énergie", "Résultats", "Annexe 1"], 1, "Un titre affirmatif porte le message."),
   mcq("Pourquoi faire jouer le contradicteur à l'assistant ?", ["Pour allonger la présentation", "Pour préparer les réponses aux questions", "Pour remplacer la relecture", "Pour choisir les couleurs"], 1, "Les objections se préparent à l'avance."),
   mcq("Où se fait la mise en forme finale ?", ["Dans l'assistant", "Dans l'outil de présentation de l'entreprise", "Dans un logiciel de dessin", "Dans le courriel d'envoi"], 1, "L'assistant prépare le fond et la trame.")
  ],
  [
   tf("Une analogie claire est forcément juste.", False, "Clarté et exactitude se vérifient séparément."),
   cloze("Un titre de diapositive ___ dit ce que la diapositive démontre.", ["affirmatif", "court", "numéroté"], 0, "« Le procédé réduit la consommation » plutôt que « Résultats »."),
   order("Remettez dans l'ordre la préparation d'une présentation technique.", ["Fixer le public et le message", "Faire produire la trame", "Vérifier chaque simplification", "Préparer les questions"], "Le message précède la forme."),
   match("Associez chaque demande à son intérêt.", [["Titres affirmatifs", "Message lisible"], ["Analogie vérifiée", "Compréhension sans erreur"], ["Contradicteur", "Questions anticipées"]], "Chaque demande vise un besoin précis."),
   tf("Les notes de l'orateur peuvent être préparées avec l'assistant.", True, "Elles se relisent comme le reste.")
  ]),
 assistant_de_poste("mb", "Votre assistant d'ingénieur brevet", "les résumés de documents publiés ou les préparations de recherche",
  "Mesurez le résumé d'un document publié sans puis avec l'assistant.",
  "Rédigez une fiche d'une page pour partager cette méthode avec les autres ingénieurs brevet."),
]

# ---------- Fonctions support et direction ----------
SUPPORT = [
 step("ms", 1, "Courriers, comptes rendus et notes", "40 min",
  ["Faire rédiger courriers et courriels au bon ton", "Transformer des notes en compte rendu", "Faire produire une note orientée décision"],
  [
   N_CONTEXTE("le destinataire, l'objectif, les points à faire passer et ce qui ne doit pas être dit"),
   ["Le ton se règle", "Précisez le registre et la longueur : administrateur à informer, partenaire institutionnel à remercier, prestataire à relancer. Un ancien courrier fictif comme modèle de ton guide mieux qu'un adjectif."],
   ["Compte rendu", "À partir de notes brutes (jamais l'enregistrement d'une réunion confidentielle dans un outil non validé), demandez : décisions, actions avec responsable et échéance, points ouverts. Le reste est secondaire."],
   ["Note de direction", "Une note se construit autour de la décision attendue : objet, contexte, options, recommandation. Demandez ce plan explicitement ; sinon l'assistant raconte au lieu de conclure."],
   N_RELIRE
  ],
  [R_FLU, R_MS],
  [
   {"t": "À partir de cinq lignes de notes fictives d'une réunion, faites produire un compte rendu : décisions, actions, points ouverts.", "c": "Chaque action a un responsable et une échéance ; rien n'a été inventé."},
   {"t": "Faites rédiger un courrier de remerciement à un partenaire institutionnel fictif, en deux tons.", "c": "Vous savez quelle consigne a changé le ton."},
   {"t": "Facultatif : faites rédiger une note de direction fictive (choix entre deux prestataires) avec recommandation en tête.", "c": "La recommandation tient en trois lignes.", "opt": True}
  ],
  [
   mcq("Que doit contenir la demande pour un compte rendu ?", ["Les notes brutes et la structure attendue", "L'enregistrement audio de la réunion", "La liste des présents uniquement", "Une formule de politesse"], 0, "Notes et structure suffisent ; l'enregistrement d'une réunion confidentielle reste hors de l'outil."),
   mcq("L'assistant ajoute « la direction vous recevra sous huit jours ». Que faire ?", ["Le laisser, c'est une formule usuelle", "Le retirer sauf si c'est décidé", "Le remplacer par quinze jours", "Demander à l'assistant de le justifier"], 1, "Tout engagement envoyé au nom de la direction doit avoir été décidé."),
   mcq("Quel plan demander pour une note de direction ?", ["La chronologie complète des échanges", "Objet, contexte, options, recommandation", "Les questions puis les réponses", "Un paragraphe unique, sans titres"], 1, "La note sert une décision : elle doit conclure."),
   mcq("Comment obtenir le ton de la maison sans le décrire longuement ?", ["Fournir un ancien courrier fictif comme modèle", "Demander un ton « professionnel »", "Écrire la consigne en majuscules", "Changer d'assistant"], 0, "Un exemple guide mieux qu'un adjectif."),
   mcq("Avant l'envoi, la vérification prioritaire porte sur :", ["Le nombre de paragraphes", "La présence d'une formule de politesse", "Dates, noms, montants et engagements", "La longueur des phrases"], 2, "Ce sont les éléments qui engagent.")
  ],
  [
   tf("Un courrier rédigé par l'assistant peut partir sans relecture s'il est bien écrit.", False, "Il part en votre nom : dates, noms, montants et promesses se relisent."),
   cloze("Dans un compte rendu, chaque action a un responsable et une ___.", ["échéance", "couleur", "signature"], 0, "Sinon l'action ne sera pas suivie."),
   order("Remettez dans l'ordre la rédaction d'une note de direction.", ["Fixer la décision attendue", "Faire produire le plan", "Faire rédiger", "Relire chaque engagement"], "La décision attendue structure le reste."),
   match("Associez chaque destinataire au ton adapté.", [["Administrateur", "Bref et orienté décision"], ["Partenaire institutionnel", "Protocolaire"], ["Prestataire en retard", "Ferme et courtois"]], "Le ton se règle dans la consigne."),
   tf("Préciser ce qui ne doit pas être dit fait partie d'une bonne consigne.", True, "Les limites évitent les formulations maladroites.")
  ]),
 step("ms", 2, "Tableaux et chiffres avec l'IA", "50 min",
  ["Faire écrire et expliquer une formule de tableur", "Faire analyser un tableau fictif", "Vérifier chaque chiffre produit"],
  [
   ["Formules de tableur", "Décrivez le tableau (colonnes, ligne d'en-tête, ce que vous voulez calculer) et demandez la formule avec son explication. Testez-la sur trois lignes dont vous connaissez le résultat."],
   ["Analyser un tableau", "Sur un tableau fictif ou public, demandez les écarts, les tendances et les anomalies, avec la ligne concernée. L'assistant peut mal lire une colonne : vérifiez chaque constat sur le tableau."],
   N_CHIFFRES,
   ["Commenter des chiffres", "Demandez un commentaire de trois phrases : le fait principal, l'écart notable, la question à poser. Le commentaire se vérifie chiffre par chiffre."],
   N_DONNEES("Une donnée de paie, un budget nominatif ou un relevé bancaire")
  ],
  [R_FLU, ["insee", "INSEE : tableaux publics pour s'exercer."]],
  [
   {"t": "Créez un tableau fictif de dix lignes (dépenses par mois et par poste). Demandez la formule du total par poste et celle de l'évolution en pourcentage.", "c": "Les deux formules donnent le bon résultat sur trois lignes contrôlées."},
   {"t": "Collez le tableau et demandez trois constats avec la ligne concernée.", "c": "Chaque constat a été vérifié sur le tableau."},
   {"t": "Demandez un commentaire de trois phrases pour un comité de direction.", "c": "Chaque chiffre du commentaire figure dans le tableau."}
  ],
  [
   mcq("Comment fiabiliser une formule proposée par l'assistant ?", ["La copier dans tout le classeur", "La tester sur des lignes au résultat connu", "Lui demander si elle est juste", "Choisir la plus longue"], 1, "Un test sur des cas connus révèle l'erreur."),
   mcq("L'assistant annonce une hausse de 12 % calculée de tête. Que faire ?", ["La reprendre telle quelle", "Recalculer dans le tableur", "Arrondir à 10 %", "Demander une seconde estimation"], 1, "Un calcul de tête peut être faux."),
   mcq("Quelles données utiliser pour s'exercer ?", ["La paie du mois dernier", "Un tableau fictif ou des données publiques", "Le budget nominatif d'un projet", "Les relevés bancaires de la société"], 1, "Les données personnelles et financières internes restent hors de l'outil."),
   mcq("Un bon commentaire de tableau donne :", ["Tous les chiffres du tableau", "Le fait principal, l'écart notable, la question à poser", "Une conclusion sans chiffres", "Une prévision pour l'année suivante"], 1, "Trois phrases, chacune vérifiable."),
   mcq("L'assistant signale une anomalie en ligne 7. Que faire ?", ["La corriger sans regarder", "Vérifier la ligne 7 dans le tableau", "Supprimer la ligne", "Ignorer le signalement"], 1, "L'assistant peut mal lire une colonne.")
  ],
  [
   tf("Un pourcentage calculé de tête par l'assistant est fiable s'il est présenté avec assurance.", False, "Recalculez dans le tableur."),
   cloze("Une formule se teste sur des lignes dont on connaît le ___.", ["résultat", "titre", "format"], 0, "Le cas connu révèle l'erreur."),
   order("Remettez dans l'ordre l'analyse d'un tableau.", ["Décrire les colonnes", "Demander les constats avec la ligne", "Vérifier chaque constat", "Rédiger le commentaire"], "La vérification précède le commentaire."),
   match("Associez chaque donnée à la règle.", [["Paie", "Jamais dans l'outil"], ["Tableau fictif", "Utilisable"], ["Données publiques", "Utilisables"]], "La nature de la donnée décide."),
   tf("Demander la formule plutôt que le résultat rend le calcul vérifiable.", True, "Le tableur calcule ; vous contrôlez.")
  ]),
 step("ms", 3, "Procédures et documents de référence", "45 min",
  ["Faire structurer une procédure à partir de notes", "Faire comparer deux versions d'un document", "Faire repérer les manques avant une diffusion"],
  [
   N_PLAN,
   ["Structurer une procédure", "Donnez les étapes en vrac, les acteurs et les documents utilisés. Demandez une procédure avec objet, responsabilités et étapes numérotées. Vous validez chaque étape avec les personnes qui la pratiquent."],
   ["Comparer deux versions", "Demandez un tableau des différences paragraphe par paragraphe, avec citation des deux rédactions. Recoupez avec la comparaison de votre traitement de texte, qui voit chaque caractère modifié."],
   N_MANQUE,
   ["Questions d'un relecteur", "Demandez à l'assistant les questions qu'un relecteur exigeant poserait sur le document. Celles auxquelles vous n'avez pas de réponse révèlent les manques."]
  ],
  [R_FLU, R_MS],
  [
   {"t": "Décrivez en vrac une procédure fictive (réception et enregistrement d'une demande de congés). Faites-la structurer.", "c": "Chaque étape a un acteur ; rien n'a été inventé."},
   {"t": "Demandez les questions qu'un relecteur exigeant poserait sur cette procédure.", "c": "Au moins une question révèle un manque réel."},
   {"t": "Modifiez trois points d'une copie et demandez la comparaison des deux versions.", "c": "Les trois modifications ont été trouvées, ou vous savez laquelle manque."}
  ],
  [
   mcq("Que fournir pour faire structurer une procédure ?", ["Le titre seul", "Étapes, acteurs et documents utilisés", "L'organigramme complet de l'entreprise", "Une procédure d'une autre entreprise"], 1, "L'assistant structure ce que vous lui donnez."),
   mcq("Comment fiabiliser une comparaison de versions ?", ["La refaire deux fois", "La recouper avec l'outil de comparaison du traitement de texte", "Demander plus de détails", "Comparer à la mémoire de l'assistant"], 1, "L'outil de comparaison voit chaque modification."),
   mcq("Quelle question fait apparaître les manques d'un document ?", ["Résume ce document", "Quelles questions poserait un relecteur exigeant ?", "Ce document est-il bon ?", "Traduis ce document"], 1, "Les questions sans réponse révèlent les manques."),
   mcq("Qui valide les étapes d'une procédure rédigée avec l'assistant ?", ["L'assistant lui-même", "Les personnes qui pratiquent la procédure", "Le premier lecteur venu", "Personne, elle est cohérente"], 1, "La procédure décrit une pratique réelle."),
   mcq("Par quoi commencer un document de plusieurs pages ?", ["Faire rédiger tout le document d'un coup", "Faire produire puis corriger un plan", "Choisir la police et les couleurs", "Écrire la conclusion"], 1, "Un plan se corrige vite ; un long texte, non.")
  ],
  [
   tf("Une procédure bien structurée par l'assistant peut être diffusée sans validation par ceux qui la pratiquent.", False, "Elle décrit une pratique réelle : ceux qui la font la valident."),
   cloze("Avant un long document, faites produire puis corriger un ___.", ["plan", "résumé", "titre"], 0, "Le plan se corrige en une minute."),
   order("Remettez dans l'ordre la rédaction d'une procédure.", ["Lister les étapes en vrac", "Faire structurer", "Faire poser les questions d'un relecteur", "Valider avec les acteurs"], "La validation humaine clôt la rédaction."),
   match("Associez chaque besoin à la consigne.", [["Procédure", "Objet, responsabilités, étapes"], ["Comparaison", "Tableau avec citations"], ["Relecture", "Questions d'un relecteur"]], "Chaque besoin a sa consigne type."),
   tf("L'outil de comparaison du traitement de texte complète utilement la comparaison faite par l'assistant.", True, "Il voit chaque caractère modifié.")
  ]),
 step("ms", 4, "Présentations et supports de conseil d'administration", "45 min",
  ["Faire produire une trame de présentation", "Obtenir des titres qui portent le message", "N'utiliser que des chiffres validés"],
  [
   N_CONTEXTE("le public (conseil d'administration, comité, équipe), la décision attendue, la durée et les chiffres validés"),
   N_TRAME,
   N_TITRES,
   N_CHIFFRES,
   N_CONTRA
  ],
  [R_MS, R_101],
  [
   {"t": "Faites produire la trame d'un support de huit diapositives sur un sujet fictif, avec titres affirmatifs et notes de l'orateur.", "c": "Chaque titre est une phrase vraie ; aucun chiffre n'a été inventé."},
   {"t": "Demandez les trois questions les plus probables d'un administrateur.", "c": "Chaque question a une réponse dans le carnet."},
   {"t": "Facultatif : faites rédiger un projet de relevé de décisions à partir de notes fictives.", "c": "Chaque décision correspond à une ligne des notes.", "opt": True}
  ],
  [
   mcq("Que donner à l'assistant avant de demander une trame ?", ["Le titre seulement", "Public, décision attendue, durée et chiffres validés", "Les comptes complets de l'entreprise", "Le support de l'an dernier en entier"], 1, "Le public et la décision attendue structurent tout le reste."),
   mcq("D'où viennent les chiffres d'un support de conseil d'administration ?", ["De l'assistant, qui les estime", "De vos tableaux validés", "D'un article de presse", "De la mémoire de l'assistant"], 1, "Un chiffre proposé par l'assistant sans base est une invention."),
   mcq("Quel titre de diapositive est le plus utile ?", ["Budget", "Le budget de l'année est tenu", "Chiffres", "Annexe 3"], 1, "Un titre affirmatif porte le message."),
   mcq("Pourquoi demander les questions probables d'un administrateur ?", ["Pour allonger le support", "Pour préparer les réponses", "Pour laisser l'assistant répondre en séance", "Pour remplacer la relecture"], 1, "On les découvre à son bureau plutôt qu'en séance."),
   mcq("Où se fait la mise en forme finale ?", ["Dans l'assistant", "Dans l'outil de présentation de l'entreprise", "Dans un logiciel de dessin", "Dans le courriel d'envoi"], 1, "L'assistant prépare le fond et la trame.")
  ],
  [
   tf("Un chiffre proposé par l'assistant peut aller dans un support s'il paraît plausible.", False, "Seuls les chiffres de vos tableaux validés y vont."),
   cloze("Un titre de diapositive ___ dit ce que la diapositive démontre.", ["affirmatif", "court", "numéroté"], 0, "« Le budget est tenu » plutôt que « Budget »."),
   order("Remettez dans l'ordre la préparation d'un support.", ["Fixer le message principal", "Faire produire la trame", "Insérer les chiffres validés", "Préparer les questions"], "Le message précède la forme."),
   match("Associez chaque demande à son intérêt.", [["Titres affirmatifs", "Message lisible"], ["Chiffres validés", "Aucune invention"], ["Questions probables", "Séance préparée"]], "Chaque demande vise un risque précis."),
   tf("Les notes de l'orateur peuvent être préparées avec l'assistant.", True, "Elles se relisent comme le reste.")
  ]),
 assistant_de_poste("ms", "Votre assistant de poste", "les comptes rendus, les courriers types ou les commentaires de tableaux",
  "Mesurez une tâche faite sans données internes (un courrier type) sans puis avec l'assistant.",
  "Rédigez une fiche d'une page pour partager cette méthode avec un collègue."),
]

METIER_PROFILS = {"cdt": CDT, "brevet": BREVET, "support": SUPPORT}
