# Profils métier (25/11/2026). Le contenu commun (Socle, Expert, Bonus, défis) est rédigé
# pour tout salarié ; un exemple propre à un métier est décliné en variantes par profil.
#
# OV[étape][chemin] = {"base": valeur neutre, "cdt": ..., "brevet": ..., "support": ...}
# Chemin : "titre", "obj.i", "notions.i", "ex.i", "quiz.i", "drills.i".
# Un profil absent reçoit la valeur de base. Le profil « juriste » reçoit le texte d'origine
# (écrit pour les juristes) sauf s'il est donné explicitement.
from socle import mcq, tf, cloze, order, match

PROFILS = [
 {"id": "juriste", "nom": "Juriste", "court": "Juriste", "desc": "L'IA pour les contrats, la recherche, les notes et les courriels.", "bloc": "Métier : juriste",
  "voie": "Utiliser l'IA dans les tâches du juriste : courriels et notes, lecture de contrats, recherche et veille, synthèses et supports, assistant de poste."},
 {"id": "cdt", "nom": "Chargé de transfert", "court": "Chargé de transfert", "desc": "L'IA pour la prospection, les propositions, la veille et les présentations.", "bloc": "Métier : chargé de transfert",
  "voie": "Utiliser l'IA dans les tâches du chargé de transfert : courriels de prospection, proposition cohérente avec le business plan, repérage de cibles et veille, présentations, assistant de poste."},
 {"id": "brevet", "nom": "Ingénieur brevet", "court": "Ingénieur brevet", "desc": "L'IA pour expliquer, comparer, préparer une recherche et présenter.", "bloc": "Métier : ingénieur brevet",
  "voie": "Utiliser l'IA dans les tâches de l'ingénieur brevet : expliquer un document publié, extraire et comparer avec citations, préparer une recherche, présenter à des non-spécialistes, assistant de poste."},
 {"id": "support", "nom": "Fonctions support et direction", "court": "Support et direction", "desc": "L'IA pour les courriers, les tableaux, les procédures et les supports.", "bloc": "Métier : support et direction",
  "voie": "Utiliser l'IA dans les tâches des fonctions support et de direction : courriers et comptes rendus, tableaux et chiffres, procédures, présentations et supports de CA, assistant de poste."},
]

def V(base, **kw):
  return {"base": base, **kw}

OV = {
 # ---------- Socle ----------
 "so1": {
  "notions.3": V(["Hallucination", "Réponse plausible, assurée et fausse : référence inventée, source qui n'existe pas, chiffre erroné, citation attribuée à tort. Le ton assuré ne prouve rien. Toute référence se vérifie à la source."]),
  "ex.0": V({"t": "Dans votre assistant, sans recherche web, demandez une information officielle précise que vous pouvez vérifier (par exemple le taux normal de TVA en France et le texte qui le fixe). Comparez avec le site officiel.", "c": "Vous avez noté dans le carnet au moins un écart, ou constaté que la réponse était exacte et vérifiée."},
   cdt={"t": "Dans votre assistant, sans recherche web, demandez le résumé d'une publication scientifique précise de votre domaine (titre, auteurs, revue, année). Comparez avec la notice sur HAL ou chez l'éditeur.", "c": "Vous avez noté dans le carnet au moins un écart, ou constaté que la réponse était exacte et vérifiée."},
   brevet={"t": "Dans votre assistant, sans recherche web, demandez le texte de la revendication 1 d'un brevet publié dont vous connaissez le numéro. Comparez avec Espacenet.", "c": "Vous avez noté dans le carnet au moins un écart, ou constaté que la réponse était exacte et vérifiée."}),
  "quiz.2": V(mcq("L'assistant cite une étude avec auteurs, revue et année. Que faire ?", ["L'utiliser : une référence aussi précise prouve qu'elle existe", "Lui demander s'il est certain de sa référence", "La retrouver à la source", "La garder pour une note interne seulement"], 2, "Seule la source établit l'existence et le contenu d'une référence."),
   brevet=mcq("L'assistant cite un brevet antérieur avec son numéro de publication. Que faire ?", ["L'utiliser : un numéro aussi précis prouve qu'il existe", "Lui demander s'il est certain de sa référence", "Le retrouver dans Espacenet", "Le garder pour une note interne seulement"], 2, "Seule la base officielle établit l'existence et le contenu d'un brevet.")),
  "quiz.3": V(mcq("Pourquoi l'assistant peut-il ignorer un texte officiel paru le mois dernier ?", ["Il écarte les textes officiels", "Ses données s'arrêtent à une date de coupure", "Il ne lit que les textes publiés en anglais ou en version consolidée", "Les textes récents sont trop courts pour lui"], 1, "Sans recherche web ni document fourni, il ne connaît que ses données d'entraînement.")),
 },
 "so2": {
  "ex.1": V({"t": "Constituez un dossier d'entraînement de cinq documents fictifs ou publics (rapport public, page d'un site officiel, courriel inventé, compte rendu fictif, tableau fictif).", "c": "Cinq documents prêts, aucun issu d'un dossier réel."},
   brevet={"t": "Constituez un dossier d'entraînement de cinq documents fictifs ou publics (deux brevets publiés, un article scientifique public, une revendication fictive, un courriel inventé).", "c": "Cinq documents prêts, aucun issu d'un dossier réel."},
   cdt={"t": "Constituez un dossier d'entraînement de cinq documents fictifs ou publics (déclaration d'invention fictive, publication scientifique publique, fiche technologie inventée, courriel fictif, tableau fictif).", "c": "Cinq documents prêts, aucun issu d'un dossier réel."}),
  "quiz.0": V(mcq("Vous voulez faire reformuler le compte rendu d'une réunion avec un partenaire. Quelle pratique est correcte ?", ["Le coller après avoir retiré les noms", "Travailler sur une version fictive de même structure", "Le déposer sur un Drive personnel d'abord", "Le coller en demandant à l'assistant de rester confidentiel"], 1, "Un document fictif de même structure permet de s'entraîner sans exposer le dossier."),
   cdt=mcq("Vous voulez faire structurer une déclaration d'invention reçue. Quelle pratique est correcte ?", ["La coller après avoir retiré les noms", "Travailler sur une déclaration fictive de même structure", "La déposer sur un Drive personnel d'abord", "La coller en demandant à l'assistant de rester confidentiel"], 1, "Une déclaration fictive de même structure permet de s'entraîner sans exposer l'invention."),
   brevet=mcq("Vous voulez faire relire un projet de demande de brevet. Quelle pratique est correcte ?", ["Le coller après avoir retiré les noms", "Travailler sur un texte fictif de même structure", "Le déposer sur un Drive personnel d'abord", "Le coller en demandant à l'assistant de rester confidentiel"], 1, "Un texte fictif de même structure permet de s'entraîner sans exposer l'invention.")),
  "drills.0": V(tf("Remplacer le nom du partenaire suffit pour coller un document de dossier réel dans un outil non validé.", False, "Le contexte reste identifiant. On s'exerce sur des documents fictifs ou publics.")),
  "drills.2": V(match("Associez chaque situation à la bonne règle.", [["Document de dossier en cours", "Version fictive pour s'exercer"], ["Texte officiel publié", "Utilisable librement"], ["Invention non déposée", "Jamais dans un outil non validé"]], "Le niveau de risque dépend de la nature de l'information."),
   brevet=match("Associez chaque situation à la bonne règle.", [["Projet de demande", "Version fictive pour s'exercer"], ["Brevet publié", "Utilisable librement"], ["Invention non déposée", "Jamais dans un outil non validé"]], "Le niveau de risque dépend de la nature de l'information.")),
 },
 "so3": {
  "notions.2": V(["Rôle", "Indiquer un rôle (« Agis comme assistant de direction d'un organisme de recherche ») oriente le vocabulaire, l'angle et le niveau d'exigence. Le rôle ne remplace pas le contexte."],
   cdt=["Rôle", "Indiquer un rôle (« Agis comme chargé de transfert de technologie ») oriente le vocabulaire, l'angle et le niveau d'exigence. Le rôle ne remplace pas le contexte."],
   brevet=["Rôle", "Indiquer un rôle (« Agis comme ingénieur brevet ») oriente le vocabulaire, l'angle et le niveau d'exigence. Le rôle ne remplace pas le contexte."]),
  "notions.3": V(["Exemple", "Faible : « Résume ce rapport. » Solide : « Je travaille à la direction d'une SATT. Résume le rapport fictif ci-dessous pour le conseil d'administration : faits marquants, chiffres clés, décisions à prendre, en huit lignes au plus, sans ajouter d'information. »"],
   cdt=["Exemple", "Faible : « Résume cette publication. » Solide : « Je suis chargé de transfert dans une SATT. Résume la publication publique ci-dessous pour un industriel non spécialiste : problème résolu, résultat, applications possibles, en huit lignes au plus, sans promettre de performance. »"],
   brevet=["Exemple", "Faible : « Résume ce brevet. » Solide : « Je suis ingénieur brevet dans une SATT. Résume le brevet publié ci-dessous pour un chargé de transfert : problème technique, solution, revendication 1 en termes simples, en huit lignes au plus, sans avis sur la validité. »"]),
  "quiz.0": V(mcq("Laquelle de ces demandes est la plus exploitable ?", ["« Analyse ce rapport en détail »", "« Que penses-tu de ce rapport ? »", "« Liste les échéances du rapport, avec la page, en tableau »", "« Tu es un expert reconnu de la gestion de projet : fais au mieux »"], 2, "Tâche précise, matière identifiée, format défini."),
   brevet=mcq("Laquelle de ces demandes est la plus exploitable ?", ["« Analyse ce brevet en détail »", "« Que penses-tu de ce brevet ? »", "« Liste les revendications indépendantes, en tableau »", "« Tu es un ingénieur brevet chevronné : fais au mieux, sans rien oublier »"], 2, "Tâche précise, matière identifiée, format défini."),
   cdt=mcq("Laquelle de ces demandes est la plus exploitable ?", ["« Analyse cette publication en détail »", "« Que penses-tu de cette publication ? »", "« Liste les applications citées, avec la page, en tableau »", "« Tu es un expert reconnu du transfert de technologie : fais au mieux »"], 2, "Tâche précise, matière identifiée, format défini.")),
  "drills.0": V(match("Associez chaque élément de la demande à son exemple.", [["Contexte", "Je travaille à la direction d'une SATT"], ["Tâche", "Résume le rapport"], ["Format", "Huit lignes au plus"], ["Limite", "Sans ajouter d'information"]], "Contexte, tâche, matière, format et limites font une demande solide."),
   cdt=match("Associez chaque élément de la demande à son exemple.", [["Contexte", "Je suis chargé de transfert"], ["Tâche", "Résume la publication"], ["Format", "Huit lignes au plus"], ["Limite", "Sans promettre de performance"]], "Contexte, tâche, matière, format et limites font une demande solide."),
   brevet=match("Associez chaque élément de la demande à son exemple.", [["Contexte", "Je suis ingénieur brevet"], ["Tâche", "Résume le brevet"], ["Format", "Huit lignes au plus"], ["Limite", "Sans avis sur la validité"]], "Contexte, tâche, matière, format et limites font une demande solide.")),
  "drills.1": V(tf("« Résume ce rapport » suffit pour obtenir une synthèse adaptée au conseil d'administration.", False, "Il manque le destinataire, l'angle, la longueur et les limites."),
   cdt=tf("« Résume cette publication » suffit pour obtenir une synthèse adaptée à un industriel.", False, "Il manque le destinataire, l'angle, la longueur et les limites."),
   brevet=tf("« Résume ce brevet » suffit pour obtenir une synthèse adaptée à un chargé de transfert.", False, "Il manque le destinataire, l'angle, la longueur et les limites.")),
 },
 "so4": {
  "notions.0": V(["Itérer", "La première réponse est un brouillon. Dites précisément ce qui ne va pas : « trop long, garde trois paragraphes », « ton trop familier », « tu as oublié le point 7 ». Une correction ciblée vaut mieux qu'une nouvelle demande vague."]),
  "drills.4": V(match("Associez chaque situation à la bonne relance.", [["Ton trop sec", "Rends-le plus diplomatique"], ["Oubli d'un point", "Ajoute le point 7"], ["Tâche floue", "Pose-moi d'abord tes questions"]], "Chaque défaut appelle une relance précise.")),
 },
 "so5": {
  "notions.1": V(["Extraire", "Demandez des champs précis : émetteur, date, montant, échéance, responsable. Exigez la valeur « non mentionné » quand l'information manque, sinon l'assistant risque de la deviner."],
   brevet=["Extraire", "Demandez des champs précis : déposant, inventeurs, date de priorité, classification, nombre de revendications. Exigez la valeur « non mentionné » quand l'information manque, sinon l'assistant risque de la deviner."]),
  "notions.2": V(["Résumer pour quelqu'un", "Un résumé dépend de son lecteur : décideur, spécialiste, partenaire, grand public. Précisez-le, ainsi que la longueur et ce qui doit absolument y figurer."]),
  "notions.3": V(["Comparer", "Deux versions d'un même texte : demandez un tableau des différences, paragraphe par paragraphe, avec citation des deux versions. Contrôlez ensuite deux ou trois lignes vous-même."]),
  "ex.0": V({"t": "Avec un document public (un appel à projets ou un rapport d'un organisme public), faites extraire dans un tableau : émetteur, objet, dates clés, montants, conditions, avec « non mentionné » si absent.", "c": "Le tableau est complet et vous avez vérifié deux cases sur le texte."},
   cdt={"t": "Avec un appel à projets public, faites extraire dans un tableau : financeur, objet, conditions d'éligibilité, montant, date limite, avec « non mentionné » si absent.", "c": "Le tableau est complet et vous avez vérifié deux cases sur le texte."},
   brevet={"t": "Avec un brevet publié, faites extraire dans un tableau : déposant, inventeurs, date de priorité, classification, nombre de revendications, avec « non mentionné » si absent.", "c": "Le tableau est complet et vous avez vérifié deux cases sur le texte."}),
  "quiz.0": V(mcq("Le document ne mentionne pas de date limite. Que doit prévoir la demande ?", ["Rien, l'assistant le verra", "La valeur « non mentionné » si absent", "De la déduire de la date de publication", "De retirer ce champ du tableau"], 1, "Sans cette consigne, l'assistant risque de combler le vide.")),
  "quiz.2": V(mcq("Un bon résumé commence par préciser :", ["Le nombre de mots exact à respecter", "Le lecteur et son besoin", "La police de caractères", "Le nom de l'auteur"], 1, "Un résumé pour un décideur n'est pas celui d'un spécialiste.")),
  "quiz.3": V(mcq("Pour comparer deux versions d'un document, la sortie la plus utile est :", ["Un avis général sur l'évolution entre les deux textes", "Un tableau point par point avec citations", "Un résumé de la version finale", "La liste des passages inchangés"], 1, "Le tableau rend chaque différence vérifiable.")),
  "drills.3": V(match("Associez le besoin à la bonne demande.", [["Décideur pressé", "Résumé de huit lignes"], ["Deux versions", "Tableau des différences"], ["Fiche de synthèse", "Extraction de champs"]], "La forme suit l'usage.")),
 },
 "so6": {
  "obj.2": V("Contrôler une référence à sa source", cdt="Contrôler une référence scientifique ou un chiffre de marché", brevet="Contrôler une référence de brevet"),
  "notions.3": V(["Sources officielles", "Texte officiel : Légifrance ou service-public.fr. Statistique : INSEE ou Eurostat. Publication scientifique : HAL ou l'éditeur. Brevet : Espacenet. Une référence non vérifiée ne sort jamais dans un document transmis."],
   cdt=["Sources scientifiques et économiques", "Publication : HAL, PubMed ou le site de l'éditeur. Entreprise : registres officiels et site de l'entreprise. Marché : l'étude d'origine, pas l'article qui la cite. Une référence non vérifiée ne sort jamais dans un document transmis."],
   brevet=["Sources brevets", "Document brevet : Espacenet ou la base de l'INPI. Statut d'une demande européenne : Registre européen des brevets. Littérature non brevet : HAL ou l'éditeur. Une référence non vérifiée ne sort jamais dans un document transmis."]),
  "ex.0": V({"t": "Posez sur un document public une question dont la réponse n'y figure pas (un chiffre absent). Une fois sans, une fois avec « dis-le si ce n'est pas dans le texte ».", "c": "Vous avez constaté la différence et noté la meilleure formulation."}),
  "quiz.2": V(mcq("Où vérifier un chiffre de l'INSEE cité par l'assistant ?", ["Sur le site de l'INSEE, dans la publication d'origine", "Dans la réponse d'un second assistant", "Sur un blog récent qui le reprend et le commente en détail", "Dans la mémoire de l'assistant"], 0, "La source officielle donne le chiffre exact et sa date."),
   cdt=mcq("Où vérifier le résultat d'une publication citée par l'assistant ?", ["Dans la publication, sur HAL ou chez l'éditeur", "Dans la réponse d'un second assistant", "Dans un communiqué de presse qui la reprend et la résume", "Dans la mémoire de l'assistant"], 0, "Seule la publication dit ce qu'elle a montré."),
   brevet=mcq("Où vérifier le statut d'un brevet européen cité par l'assistant ?", ["Dans le Registre européen des brevets", "Dans la réponse d'un second assistant", "Sur le site web du déposant, rubrique actualités", "Dans la mémoire de l'assistant"], 0, "Le registre donne le statut officiel.")),
  "drills.1": V(match("Associez chaque référence à sa source officielle.", [["Texte officiel", "Légifrance"], ["Statistique publique", "INSEE"], ["Règlement européen", "EUR-Lex"]], "Chaque type de source a sa base officielle."),
   cdt=match("Associez chaque référence à sa source officielle.", [["Publication scientifique", "HAL ou l'éditeur"], ["Brevet publié", "Espacenet"], ["Statistique publique", "INSEE"]], "Chaque type de source a sa base officielle."),
   brevet=match("Associez chaque référence à sa source officielle.", [["Brevet publié", "Espacenet"], ["Statut d'une demande européenne", "Registre européen des brevets"], ["Article scientifique", "HAL ou l'éditeur"]], "Chaque type de source a sa base officielle.")),
 },
 "so7": {
  "notions.4": V(["Traduction", "L'assistant traduit bien les textes courants. Pour un document qui engage (contrat, cahier des charges, revendication), faites vérifier les termes techniques : un faux ami peut changer le sens."]),
  "quiz.3": V(mcq("Vous traduisez un cahier des charges technique. Que vérifier ?", ["La longueur de la traduction par rapport à l'original", "Les termes techniques et faux amis", "La ponctuation seulement", "Le nombre de phrases"], 1, "Un faux ami peut changer le sens d'une exigence."),
   brevet=mcq("Vous traduisez une revendication. Que vérifier ?", ["La longueur de la traduction par rapport à l'original", "Chaque terme technique et les faux amis", "La ponctuation seulement", "Le nombre de phrases"], 1, "Un terme mal traduit peut changer la portée.")),
 },
 "so8": {
  "ex.0": V({"t": "Faites classer dix courriels fictifs en catégories (demande d'information, réclamation, relance, facture) avec trois exemples variés dans la demande.", "c": "Au moins huit courriels sur dix sont bien classés ; les erreurs sont notées."},
   cdt={"t": "Faites classer dix résumés fictifs de déclarations d'invention par domaine (santé, numérique, matériaux, énergie) avec trois exemples variés dans la demande.", "c": "Au moins huit résumés sur dix sont bien classés ; les erreurs sont notées."},
   brevet={"t": "Faites classer dix résumés de brevets fictifs par domaine technique avec trois exemples variés dans la demande.", "c": "Au moins huit résumés sur dix sont bien classés ; les erreurs sont notées."}),
  "drills.1": V(order("Remettez dans l'ordre l'analyse d'un document en étapes.", ["Extraire les points clés", "Comparer à la référence", "Rédiger la synthèse des écarts"], "Chaque étape utilise le résultat contrôlé de la précédente.")),
 },
 # ---------- Expert : exemples rendus génériques, le juriste garde les siens ----------
 "s6": {
  "notions.2": V(["Jeu de tests", "Inclure des cas faciles, des cas limites et des pièges (information absente, formulation ambiguë, format inhabituel)."]),
  "ex.1": V({"t": "Créer un tableur d'évaluation pour un classificateur de courriels : 20 courriels fictifs, colonnes « attendu », « obtenu », « correct ».", "c": "Taux de réussite calculé pour deux versions du prompt ; la meilleure est identifiée."}),
  "quiz.2": V(mcq("Quand recourir à un modèle « juge » ?", ["Pour classer des étiquettes à valeur unique, comme oui ou non", "Pour noter des réponses ouvertes selon une grille de critères", "Pour écrire à la place de l'utilisateur le prompt à tester", "Jamais : un modèle ne peut pas en évaluer un autre"], 1, "La grille doit reposer sur des critères observables.")),
  "drills.3": V(match("Associez chaque méthode de notation à son exemple.", [["Par code", "Vérifier qu'une date est au bon format"], ["Par modèle", "Un second modèle note la qualité"], ["Par humain", "Un expert du métier relit et note"]], "Trois façons de noter, avec des coûts et des biais différents.")),
  "drills.4": V(tf("Cas pratique : un jeu de tests de courriels doit contenir des courriels fictifs avec quelques pièges, par exemple une demande formulée de façon inhabituelle.", True, "Les cas difficiles révèlent les faiblesses d'un prompt.")),
 },
 "s7": {
  "notions.3": V(["Exemple", "<pre>import anthropic\nclient = anthropic.Anthropic()  # lit la clé dans l'environnement\nrep = client.messages.create(\n    model=\"[nom du modèle, voir la documentation]\",\n    max_tokens=500,\n    system=\"Tu classes des courriels de service.\",\n    messages=[{\"role\": \"user\", \"content\": \"Classe ce courriel : ...\"}])\nprint(rep.content[0].text)</pre>"]),
  "ex.1": V({"t": "Écrire une boucle qui envoie trois courriels fictifs au classificateur et affiche les résultats.", "c": "Trois étiquettes affichées, une par courriel."}),
  "quiz.3": V(mcq("Que fait ce code : for c in courriels: print(c) ?", ["Il supprime chaque courriel de la liste après l'avoir affiché", "Il compte le nombre de courriels contenus dans la liste", "Il trie les courriels par ordre alphabétique avant l'affichage", "Il affiche chaque élément de la liste, un par un"], 3, "La boucle for parcourt la liste.")),
  "drills.4": V(tf("Cas pratique : sans mise en cache du prompt, envoyer cent fois un long document fictif fait payer cent fois ses tokens d'entrée.", True, "Chaque appel facture ses tokens d'entrée et de sortie ; seule la mise en cache réduit le coût des parties répétées.")),
 },
 "s8": {
  "obj.2": V("Concevoir un RAG sur un corpus de documents"),
  "notions.3": V(["Découpage par unité de sens", "[Inférence] Pour un recueil de procédures ou de modèles, découper par section plutôt que par page, et attacher des métadonnées (type, version, statut) améliore la pertinence des extraits."]),
  "ex.2": V({"t": "Concevoir sur papier un RAG d'un recueil de procédures internes fictif : unité de découpage, métadonnées, cinq questions tests et la section attendue pour chacune.", "c": "Les cinq questions ont chacune une section cible identifiée."}),
  "quiz.4": V(mcq("Pour un recueil de procédures, quel découpage est le plus pertinent ?", ["Par page, quelle que soit la place des sections", "Par lettre, pour une recherche plus fine dans chaque passage", "Par section, avec des métadonnées (type, version)", "En un seul bloc, pour garder tout le contexte"], 2, "Une page peut couper une section en deux ou en mêler plusieurs.")),
  "drills.4": V(cloze("Cas pratique : pour un corpus de procédures fictives, découpez par ___ plutôt qu'en blocs arbitraires de caractères.", ["section", "caractère", "page imprimée"], 0, "Un découpage par unité de sens respecte la structure du document.")),
 },
 "s9": {
  "ex.2": V({"t": "Concevoir un agent fictif de préparation de comptes rendus : déclencheur, outils (lecture des notes, modèle de compte rendu, annuaire interne), actions interdites, points de validation humaine.", "c": "Au moins deux points de validation humaine ; aucun envoi externe automatique."}),
  "quiz.3": V(mcq("Où placer une validation humaine dans un agent qui prépare des documents ?", ["Nulle part : la validation humaine ralentit trop l'agent", "Une seule fois, au début de la tâche, pour approuver le plan général de l'agent", "Avant toute action irréversible ou externe : envoi, signature, dépôt", "Uniquement après une erreur signalée par l'agent lui-même"], 2, "Un envoi à un partenaire ne se rattrape pas.")),
  "drills.4": V(tf("Cas pratique : avant qu'un agent envoie un document à un partenaire extérieur, une validation humaine s'impose.", True, "Un envoi externe est irréversible : il demande un contrôle humain.")),
 },
 "s9b": {
  "ex.0": V({"t": "Rédiger un SKILL.md pour une tâche récurrente de votre poste (par exemple la fiche de synthèse d'un document type), testé sur des données fictives.", "c": "Le fichier contient un nom, une description qui dit quand le déclencher, des étapes, un format de sortie et une règle de citation. Un test sur un document fictif est consigné dans le carnet."}),
  "ex.2": V({"t": "Concevoir la répartition des modèles d'une chaîne de traitement de documents : extraction, analyse, relecture.", "c": "Un modèle est nommé par étape, avec une justification tirée de l'article et une règle d'escalade (auto-vérification, effort, modèle supérieur)."}),
  "quiz.5": V(mcq("À quel type de tâche l'article réserve-t-il les petits modèles ?", ["Celles qui demandent le plus de jugement d'expert", "Les décisions finales avant envoi au partenaire", "Celles dont l'erreur se repère facilement", "Les tâches sans relecture, pour gagner du temps"], 2, "Les petits modèles prennent les tâches dont l'erreur se voit vite ; le jugement reste sur le modèle principal.")),
  "drills.4": V(cloze("Cas pratique : dans une chaîne de traitement de documents, l'extraction des noms et des dates convient à ___.", ["Haiku 5.5", "Fable 5.2", "aucun modèle"], 0, "L'extraction est une tâche simple en volume dont l'erreur se repère facilement.")),
 },
 "s10": {
  "ex.2": V({"t": "Spécifier une équipe de trois agents pour la revue d'un dossier de projet fictif (analyse financière, analyse technique, relecture de style).", "c": "Pour chaque agent : rôle, objectif, livrable ; un critère d'arrêt ; un point de contrôle humain."}),
  "quiz.3": V(mcq("Principal inconvénient d'une équipe d'agents ?", ["Elle ne peut pas lire de documents volumineux comme un rapport", "Elle exige un GPU local pour chaque agent de l'équipe, même pour une tâche simple", "Plus d'appels, donc plus de coût, et des erreurs plus dures à localiser", "Elle est limitée à un seul fournisseur de modèles"], 2, "À réserver aux tâches qui le justifient.")),
  "drills.4": V(tf("Cas pratique : une équipe qui sépare recherche, analyse et recommandation se justifie si ces sous-tâches sont indépendantes.", True, "Le multi-agents se justifie par l'indépendance ou la spécialisation des sous-tâches.")),
 },
 "s11": {
  "drills.4": V(tf("Cas pratique : fournir un modèle de document dans le prompt revient à du fine-tuning.", False, "Le prompt n'altère pas les paramètres du modèle ; le fine-tuning, si.")),
 },
 "s12": {
  "notions.0": V(["Sujet", "Un assistant de pré-revue d'un document récurrent de votre poste : il reçoit le document, produit une fiche d'identité, relève les écarts par rapport à une trame de référence générique et cite chaque passage. Vous restez seul juge de la suite à donner."],
   cdt=["Sujet", "Un assistant de pré-analyse de déclarations d'invention : il reçoit une déclaration, produit une fiche structurée, relève les informations manquantes par rapport à une grille générique et cite chaque passage. Le chargé de transfert reste seul juge de la suite à donner."],
   brevet=["Sujet", "Un assistant de tri d'antériorités : il reçoit des abrégés de brevets publiés et une revendication fictive, indique pour chaque document les caractéristiques présentes avec citation et classe les documents. L'ingénieur brevet reste seul juge de la pertinence."],
   support=["Sujet", "Un assistant de préparation de comptes rendus : il reçoit des notes de réunion fictives, produit un compte rendu selon une trame de référence (décisions, actions, points ouverts) et signale chaque élément sans source dans les notes. Vous restez seul juge du texte diffusé."]),
  "notions.1": V(["Données", "Uniquement des documents fictifs ou publics. La trame de référence est une version générique, sans aucune donnée de dossier."]),
  "ex.2": V({"t": "Constituer 15 documents fictifs ou variantes avec les écarts attendus, et mesurer le taux de détection.", "c": "Au moins 80 % des écarts détectés, aucune citation inventée."}),
  "ex.3": V({"t": "Écrire le script Colab qui traite un dossier de fichiers et produit une fiche par document.", "c": "Exécution complète sans intervention manuelle."}),
  "quiz.0": V(mcq("Dans ce projet, qui arrête la suite à donner ?", ["L'assistant, une fois la trame de référence appliquée", "Un second modèle chargé de juger la sortie du premier", "Vous, l'assistant ne fait qu'une pré-revue", "Le destinataire, après relecture de la fiche produite"], 2, "L'outil prépare, vous décidez.")),
  "quiz.1": V(mcq("Quel indicateur fixe le seuil de réussite du projet ?", ["Le nombre de pages de synthèse produites pour chaque document", "Le temps de réponse moyen de l'assistant sur chacun des documents du jeu de test", "Le nombre d'outils connectés à l'assistant au total", "Le taux de détection des écarts sur 15 documents, sans citation inventée"], 3, "Une mesure objective, reproductible après chaque modification.")),
  "quiz.2": V(mcq("Quelles données utiliser pour développer et tester l'outil ?", ["Des documents fictifs ou publics et une trame générique", "Des documents en cours de traitement, rendus anonymes à la main", "Des documents récupérés sur le web sans vérification de licence", "Des documents d'autres SATT obtenus auprès de confrères"], 0, "Règle de confidentialité du parcours.")),
  "drills.0": V(tf("L'assistant de pré-revue décide seul de la suite à donner.", False, "Vous restez seul juge ; l'outil prépare et cite.")),
  "drills.2": V(order("Remettez dans l'ordre le traitement d'un document par l'assistant.", ["Charger le document fictif", "Extraire la fiche d'identité, avec citations", "Comparer la fiche à la trame, avec citations", "Vous remettre le résultat, vous décidez"], "Les citations accompagnent chaque étape ; la décision reste humaine.")),
  "drills.4": V(tf("Cas pratique : la trame de référence peut reprendre le contenu d'un dossier réel anonymisé.", False, "La trame reste générique, sans aucune donnée de dossier.")),
 },
 "bonus": {
  "quiz.0": V(mcq("Que produisent les skills spécialisés de cet atelier ?", ["Des documents prêts à signer, relus par un expert", "Des clés API pour accéder à de nouveaux modèles", "Des schémas, présentations et pages", "Des modèles de langage entraînés sur vos données"], 2, "Ils produisent des supports visuels à partir d'instructions.")),
  "drills.1": V(cloze("Une page de synthèse produite par un skill se ___ avant diffusion.", ["relit", "signe", "chiffre"], 0, "Le contenu reste sous la responsabilité de son auteur.")),
 },
}

# Défis : mêmes identifiants (les défis relevés restent acquis), consigne déclinée par profil.
DEFI_OV = {
 "d02": V({"consigne": "Donne trois chiffres officiels récents sur la recherche publique en France (par exemple la dépense intérieure de recherche et développement), avec la source exacte de chacun.", "critere": "Les trois chiffres ont été retrouvés à la source citée ; les écarts sont notés."},
   cdt={"consigne": "Cite trois publications scientifiques récentes sur [domaine d'un projet fictif], avec auteurs, revue et année.", "critere": "Chaque publication a été retrouvée sur HAL ou chez l'éditeur ; les références inventées sont notées."},
   brevet={"consigne": "Cite trois articles de la Convention sur le brevet européen relatifs à la brevetabilité, avec leur numéro et une phrase de contenu.", "critere": "Les trois articles ont été vérifiés sur le site de l'OEB ; les écarts sont notés."}),
 "d04": V({"consigne": "Explique ce qu'est une SATT et ce que recouvre le transfert de technologie à une personne qui découvre le secteur.", "critere": "Après trois relances ciblées (plus court, un exemple, une analogie), la réponse est utilisable telle quelle."}, cdt=None, brevet=None),
 "d08": V({"titre": "Ce qui manque", "consigne": "Voici un document type public : [collez un modèle public, par exemple une procédure ou un formulaire]. Liste les rubriques habituelles qui en sont absentes et explique ce que chaque absence peut poser comme problème.", "critere": "Au moins une absence est confirmée par votre lecture."},
   cdt={"consigne": "Voici une fiche de présentation de technologie fictive : [fiche]. Liste les informations qu'un industriel attendrait et qui manquent.", "critere": "Au moins une absence est confirmée par votre lecture."},
   brevet={"consigne": "Voici le résumé d'une invention fictive : [résumé]. Liste les informations qui manquent pour préparer une demande de brevet (problème technique, modes de réalisation, résultats d'essais).", "critere": "Au moins une absence est confirmée par votre lecture."}),
 "d11": V({"consigne": "Voici ma position sur un cas fictif : [position]. Joue la personne qui n'est pas d'accord et donne-moi les trois objections les plus solides."}),
 "d12": V({"consigne": "Posez la même question précise à deux assistants différents (par exemple Claude et ChatGPT) : « Qu'est-ce que la révision espacée et pourquoi aide-t-elle à mémoriser ? »"},
   cdt={"consigne": "Posez la même question précise à deux assistants différents (par exemple Claude et ChatGPT) : « Quels sont les niveaux de maturité technologique (TRL) et que recouvre chacun ? »"},
   brevet=None),
 "d13": V({"consigne": "Compare sous forme de tableau le compte rendu, le relevé de décisions et la note de synthèse : objectif, longueur, lecteur, contenu attendu. Signale tes incertitudes."},
   cdt=None,
   brevet={"consigne": "Compare sous forme de tableau le dépôt français, la demande européenne et la demande internationale (PCT) : procédure, délais, étendue territoriale. Signale tes incertitudes."}),
 "d14": V({"consigne": "Avec la recherche web activée : quelles sont les trois dernières publications de l'INSEE sur l'activité ou l'emploi en France ? Donne la date et le titre de chacune.", "critere": "Chaque publication a été retrouvée sur le site de l'INSEE."},
   cdt={"consigne": "Avec la recherche web activée : quels appels à projets publics de soutien à l'innovation sont ouverts ce mois-ci ? Donne la date limite et la page officielle de chacun.", "critere": "Chaque appel a été retrouvé sur la page du financeur ; les appels clos sont notés."},
   brevet={"consigne": "Avec la recherche web activée : quelles sont les dernières modifications des règles ou des taxes de l'OEB ? Donne la date et la référence officielle de chacune.", "critere": "Chaque modification a été retrouvée sur le site de l'OEB."}),
 "d16": V({"consigne": "Voici deux exemples de courriels classés « urgent » et « peut attendre » : [exemples fictifs]. Classe de la même façon ces trois nouveaux courriels : [courriels fictifs]."},
   cdt={"consigne": "Voici deux exemples de déclarations d'invention fictives classées « à approfondir » et « à classer » : [exemples fictifs]. Classe de la même façon ces trois nouvelles déclarations fictives : [résumés]."},
   brevet={"consigne": "Voici deux exemples d'abrégés classés « pertinent » et « hors sujet » pour une revendication fictive : [exemples]. Classe de la même façon ces trois nouveaux abrégés publiés : [abrégés]."}),
 "d21": V({"consigne": "Sur un compte personnel, créez une clé d'API et faites un premier appel depuis un notebook avec une consigne de classification de courriels fictifs."}),
}
