# Voie Socle : tout salarié, pratique autorisée au poste (assistant dans le navigateur).
# Rédaction neutre vis-à-vis de l'outil : Claude, ChatGPT, Copilot, Le Chat, Gemini.

def mcq(q, o, a, e): return {"q": q, "o": o, "a": a, "e": e}
def tf(q, a, e): return {"type": "tf", "q": q, "a": a, "e": e}
def cloze(q, o, a, e): return {"type": "cloze", "q": q, "o": o, "a": a, "e": e}
def order(q, items, e): return {"type": "order", "q": q, "items": items, "e": e}
def match(q, pairs, e): return {"type": "match", "q": q, "pairs": pairs, "e": e}

SOCLE = [
 {
  "id": "so1", "cote": "S1", "titre": "Comprendre l'assistant", "duree": "30 min",
  "comp": ["comprendre"], "cadre": 1,
  "obj": ["Expliquer comment un assistant produit sa réponse", "Reconnaître une hallucination", "Savoir ce que l'assistant ignore"],
  "notions": [
   ["Prédiction", "Un assistant comme Claude, ChatGPT, Copilot ou Le Chat repose sur un grand modèle de langage (LLM). Il produit sa réponse en prédisant, morceau après morceau, la suite la plus probable du texte. Il ne consulte pas une base de faits : il génère un texte plausible."],
   ["Token et contexte", "Le texte est découpé en tokens (mots courts, fragments, signes). La fenêtre de contexte est la quantité de texte que l'assistant prend en compte en une fois : vos consignes, les pièces jointes, l'historique et sa propre réponse. Au-delà, il oublie le début."],
   ["Date de coupure", "Le modèle ne connaît que ses données d'entraînement, arrêtées à une date. Un texte, un prix ou un événement postérieur lui est inconnu, sauf s'il fait une recherche web ou si vous lui fournissez le document."],
   ["Hallucination", "Réponse plausible, assurée et fausse : article de loi inventé, arrêt inexistant, chiffre erroné, citation attribuée à tort. Le ton assuré ne prouve rien. Toute référence se vérifie à la source."],
   ["Un outil, plusieurs marques", "Les assistants du marché fonctionnent sur le même principe. Les noms des fonctions changent d'un outil à l'autre et d'un mois à l'autre ; les réflexes de ce parcours restent valables quel que soit l'outil."]
  ],
  "res": [["skfluency", "Cours gratuit : le cadre des 4D (Delegation, Description, Discernment, Diligence), en anglais."], ["elements", "Elements of AI, en français : chapitres 1 et 2 pour situer l'IA."]],
  "ex": [
   {"t": "Dans votre assistant, sans recherche web, demandez le texte exact d'un article de loi précis (par exemple l'article L.611-11 du CPI). Comparez avec Légifrance.", "c": "Vous avez noté dans le carnet au moins un écart, ou constaté que la réponse était exacte et vérifiée."},
   {"t": "Demandez à votre assistant quelle est sa date de coupure et ce qu'il sait d'un événement de la semaine dernière.", "c": "Vous savez dire si votre assistant a fait une recherche web ou répondu de mémoire."}
  ],
  "quiz": [
   mcq("Comment un assistant produit-il sa réponse ?", ["Il recopie la page web la plus fiable", "Il prédit la suite de texte la plus probable", "Il interroge une base de faits validée", "Il assemble des réponses écrites par des experts"], 1, "Le modèle génère un texte plausible ; il ne consulte pas de base de faits par défaut."),
   mcq("La fenêtre de contexte désigne :", ["La durée de conservation de vos conversations", "Le nombre de questions autorisées par jour", "La quantité de texte prise en compte en une fois", "La zone de saisie visible à l'écran"], 2, "Consignes, pièces jointes, historique et réponse doivent tenir dans cette fenêtre."),
   mcq("L'assistant cite un arrêt avec date et numéro de pourvoi. Que faire ?", ["L'utiliser : le numéro précis prouve qu'il existe", "Lui demander s'il est certain de sa référence", "Le vérifier sur Judilibre ou Légifrance", "Le garder pour une note interne seulement"], 2, "Seule la source officielle établit l'existence et le contenu d'une décision."),
   mcq("Pourquoi l'assistant peut-il ignorer un décret paru le mois dernier ?", ["Il écarte les textes réglementaires", "Ses données s'arrêtent à une date de coupure", "Il ne lit que les textes en anglais", "Les décrets sont trop courts pour lui"], 1, "Sans recherche web ni document fourni, il ne connaît que ses données d'entraînement."),
   mcq("Vous passez de ChatGPT à Claude. Qu'est-ce qui reste valable ?", ["Les noms exacts des menus", "Les réflexes de consigne et de vérification", "Les mêmes limites de taille de fichier", "Le même historique de conversations"], 1, "Les fonctions changent de nom ; la méthode reste la même.")
  ],
  "drills": [
   tf("Un assistant consulte une base de faits avant de répondre.", False, "Il génère une suite de texte probable. Il ne consulte pas de base de faits par défaut."),
   cloze("Une réponse plausible, assurée et fausse s'appelle une ___.", ["hallucination", "injection", "coupure"], 0, "Le ton assuré ne garantit pas l'exactitude."),
   match("Associez chaque terme à sa définition.", [["Token", "Morceau de texte traité"], ["Fenêtre de contexte", "Texte pris en compte en une fois"], ["Date de coupure", "Fin des données d'entraînement"], ["Hallucination", "Réponse plausible mais fausse"]], "Ces quatre notions encadrent tout usage prudent."),
   tf("Demander à l'assistant s'il est sûr de sa citation vaut vérification.", False, "Il peut confirmer une erreur avec la même assurance. Seule la source vérifie."),
   cloze("Une très longue conversation peut faire ___ à l'assistant les consignes du début.", ["oublier", "traduire", "chiffrer"], 0, "Au-delà de la fenêtre de contexte, le début de l'échange n'est plus pris en compte.")
  ]
 },
 {
  "id": "so2", "cote": "S2", "titre": "Utiliser l'IA dans les règles", "duree": "30 min",
  "comp": ["proteger"], "cadre": 1,
  "obj": ["Savoir quelles données ne jamais saisir", "Connaître le cadre d'usage de votre entreprise", "Situer les règles qui s'appliquent (RGPD, secret, AI Act)"],
  "notions": [
   ["Ce qui ne sort pas", "Données personnelles, informations confidentielles de partenaires, secrets d'affaires, inventions non déposées, montants et conditions de négociation : rien de cela ne se saisit dans un outil d'IA non validé par l'entreprise. À la SATT, les données de dossiers restent sur le Nextcloud SATT."],
   ["Anonymiser ne suffit pas", "Remplacer un nom ne rend pas un document anonyme : le montant, la technologie, les dates et la structure suffisent souvent à reconnaître le dossier. Pour s'entraîner, on travaille sur des documents fictifs ou publics."],
   ["Le cadre de l'entreprise", "Chaque entreprise fixe ce qui est permis : quels outils, par quel accès, pour quelles données. Aujourd'hui à la SATT : les assistants s'utilisent dans le navigateur, sans logiciel de bureau, sans extension et sans outil de code. Ce cadre évolue ; l'application vous laisse le régler dans le profil."],
   ["Divulgation et nouveauté", "Saisir la description d'une invention non déposée dans un outil grand public peut être analysé comme une communication à un tiers, hors de tout engagement de confidentialité. Prudence absolue avant le dépôt."],
   ["Former les équipes", "L'AI Act (règlement (UE) 2024/1689) impose aux entreprises qui utilisent des systèmes d'IA de prendre des mesures de maîtrise de l'IA pour leur personnel (article 4). [Non vérifié] Depuis la modification de 2026 (Digital Omnibus), il s'agit d'une obligation de moyens adaptée aux rôles, et non plus d'un niveau suffisant à garantir."]
  ],
  "res": [["cnil", "CNIL : recommandations sur l'intelligence artificielle."], ["aiact", "Texte de l'AI Act sur EUR-Lex."]],
  "ex": [
   {"t": "Relisez la charte ou la note interne de votre entreprise sur l'usage de l'IA. Notez dans le carnet les outils permis, les données interdites et la personne à contacter en cas de doute.", "c": "Trois lignes claires dans le carnet. S'il n'existe pas de note, la question est posée à votre responsable."},
   {"t": "Constituez un dossier d'entraînement de cinq documents fictifs ou publics (modèle de NDA public, article de loi, courriel inventé, compte rendu fictif, tableau fictif).", "c": "Cinq documents prêts, aucun issu d'un dossier réel."}
  ],
  "quiz": [
   mcq("Vous voulez faire relire un NDA en cours de négociation. Quelle pratique est correcte ?", ["Le coller après avoir retiré le nom", "Travailler sur un NDA fictif de même structure", "Le déposer sur un Drive personnel d'abord", "Le coller en demandant la confidentialité"], 1, "Un document fictif de même structure permet de s'entraîner sans exposer le dossier."),
   mcq("Pourquoi retirer le nom de la contrepartie ne suffit-il pas ?", ["Les noms sont rétablis automatiquement", "Le contexte suffit souvent à reconnaître le dossier", "L'outil refuse les textes anonymisés", "Le nom figure aussi dans les métadonnées"], 1, "Montants, technologie, dates et structure identifient encore le dossier."),
   mcq("Qui fixe les outils d'IA permis dans l'entreprise ?", ["Chaque salarié selon son métier", "L'éditeur de l'outil d'IA", "L'entreprise, dans ses règles internes", "Le partenaire concerné par le dossier"], 2, "Le cadre d'usage est une décision de l'entreprise, qui peut évoluer."),
   mcq("Une invention n'est pas encore déposée. Peut-on la décrire à un assistant grand public ?", ["Oui, si l'on demande la confidentialité", "Oui, si la description reste courte", "Non, c'est une communication hors engagement", "Oui, si le compte est personnel"], 2, "Hors engagement de confidentialité, la communication fait courir un risque sur la nouveauté."),
   mcq("Selon l'article 4 de l'AI Act, l'entreprise qui utilise l'IA doit :", ["Interdire l'IA aux non-spécialistes", "Prendre des mesures de maîtrise de l'IA pour son personnel", "Déclarer chaque usage à la CNIL", "Certifier chaque salarié par un examen"], 1, "Il s'agit de mesures de formation et de sensibilisation adaptées aux rôles.")
  ],
  "drills": [
   tf("Remplacer le nom de la contrepartie suffit pour coller un contrat réel dans un outil non validé.", False, "Le contexte reste identifiant. On s'exerce sur des documents fictifs ou publics."),
   cloze("Les données de dossiers SATT restent sur le ___.", ["Drive personnel", "Nextcloud SATT", "compte GitHub"], 1, "Les données de dossiers ne quittent pas l'espace validé par l'entreprise."),
   match("Associez chaque situation à la bonne règle.", [["Contrat en négociation", "Version fictive pour s'exercer"], ["Article de loi", "Utilisable librement"], ["Invention non déposée", "Jamais dans un outil non validé"]], "Le niveau de risque dépend de la nature de l'information."),
   tf("Le cadre d'usage de l'IA dans l'entreprise peut évoluer avec le temps.", True, "Les outils et les accès permis changent ; il faut se tenir à la règle en vigueur."),
   order("Remettez dans l'ordre le réflexe avant de saisir un document.", ["Identifier la nature de l'information", "Vérifier ce que permet la règle interne", "Remplacer par un document fictif si besoin", "Saisir la demande dans l'assistant"], "On qualifie l'information avant de choisir l'outil et le support.")
  ]
 },
 {
  "id": "so3", "cote": "S3", "titre": "Formuler une demande claire", "duree": "40 min",
  "comp": ["formuler"], "cadre": 1,
  "obj": ["Donner contexte, tâche et format", "Préciser le destinataire et les limites", "Passer d'une demande vague à une demande exploitable"],
  "notions": [
   ["La règle du collègue", "Relisez votre demande comme si un collègue compétent, qui ne connaît pas le dossier, la recevait. S'il hésite sur ce que vous attendez, l'assistant hésitera aussi."],
   ["Les cinq éléments", "Contexte (qui vous êtes, pourquoi vous demandez), tâche (le verbe d'action), matière (le texte ou les faits), format (longueur, forme, tableau), limites (ce qu'il ne faut pas faire). Une demande solide les contient presque toujours."],
   ["Rôle", "Indiquer un rôle (« Agis comme juriste en transfert de technologie ») oriente le vocabulaire, l'angle et le niveau d'exigence. Le rôle ne remplace pas le contexte."],
   ["Exemple", "Faible : « Résume ce contrat. » Solide : « Je suis juriste dans une SATT. Résume le contrat fictif ci-dessous pour un chargé d'affaires non juriste : objet, durée, obligations de chaque partie, en huit lignes au plus, sans conseil juridique. »"],
   ["Délimiter les documents", "Quand la demande contient un texte à traiter, séparez-le de la consigne : entre guillemets, sous un intertitre « Texte : » ou entre balises <texte>…</texte>. L'assistant distingue ce qu'il doit faire de ce qu'il doit lire."]
  ],
  "res": [["promptdoc", "Guide de rédaction des consignes (documentation Anthropic, en anglais)."], ["oaiacad", "OpenAI Academy : ressources gratuites sur l'usage de ChatGPT (en anglais)."]],
  "ex": [
   {"t": "Prenez une demande vague que vous avez déjà faite (« fais-moi un mail », « résume ») et réécrivez-la avec les cinq éléments. Comparez les deux réponses.", "c": "Le carnet contient les deux versions et deux différences constatées."},
   {"t": "Posez la même question avec et sans rôle sur un sujet de votre métier.", "c": "Vous savez dire ce que le rôle a changé (vocabulaire, angle, précision)."}
  ],
  "quiz": [
   mcq("Laquelle de ces demandes est la plus exploitable ?", ["« Analyse ce contrat en détail »", "« Que penses-tu de ce contrat ? »", "« Liste les clauses de durée, article et citation, en tableau »", "« Fais au mieux, tu es expert »"], 2, "Tâche précise, matière identifiée, format défini."),
   mcq("Quel élément manque à : « Rédige un courriel de relance » ?", ["Le verbe d'action", "Le destinataire et le contexte", "La langue française", "La formule de politesse"], 1, "Sans destinataire ni contexte, l'assistant invente un cas générique."),
   mcq("À quoi sert d'indiquer un rôle ?", ["À agrandir la fenêtre de contexte", "À orienter vocabulaire et angle", "À supprimer les hallucinations", "À réduire le coût de la demande"], 1, "Le rôle oriente la réponse ; il ne garantit pas l'exactitude."),
   mcq("Pourquoi séparer le texte à traiter de la consigne ?", ["Pour que l'assistant les distingue", "Pour chiffrer le document", "Parce qu'il ne lit pas le texte brut", "Pour diviser le coût par deux"], 0, "La séparation évite de prendre une phrase du document pour une instruction."),
   mcq("La « règle du collègue » consiste à :", ["Faire valider chaque réponse par un collègue", "Relire la demande comme un collègue sans contexte", "Poser la question en équipe", "Copier la demande d'un collègue"], 1, "Si un collègue hésiterait, l'assistant hésitera aussi.")
  ],
  "drills": [
   match("Associez chaque élément de la demande à son exemple.", [["Contexte", "Je suis juriste dans une SATT"], ["Tâche", "Résume le contrat"], ["Format", "Huit lignes au plus"], ["Limite", "Sans conseil juridique"]], "Contexte, tâche, matière, format et limites font une demande solide."),
   tf("« Résume ce contrat » suffit pour obtenir une synthèse adaptée à un chargé d'affaires.", False, "Il manque le destinataire, l'angle, la longueur et les limites."),
   cloze("Un texte à traiter se place entre guillemets, sous un intertitre ou entre ___.", ["balises", "parenthèses vides", "émoticônes"], 0, "Les balises délimitent clairement la matière."),
   order("Remettez dans l'ordre la construction d'une demande.", ["Donner le contexte", "Énoncer la tâche", "Fournir le texte à traiter", "Préciser format et limites"], "Le lecteur comprend d'abord pourquoi, puis quoi, puis comment rendre la réponse."),
   tf("Le rôle remplace le contexte.", False, "Le rôle oriente le style ; seul le contexte dit ce que vous cherchez.")
  ]
 },
 {
  "id": "so4", "cote": "S4", "titre": "Dialoguer et affiner", "duree": "30 min",
  "comp": ["dialoguer"], "cadre": 1,
  "obj": ["Corriger une réponse au lieu de recommencer", "Faire poser des questions à l'assistant", "Savoir quand ouvrir une nouvelle conversation"],
  "notions": [
   ["Itérer", "La première réponse est un brouillon. Dites précisément ce qui ne va pas : « trop long, garde trois paragraphes », « ton trop familier », « tu as oublié la clause 7 ». Une correction ciblée vaut mieux qu'une nouvelle demande vague."],
   ["Faire questionner", "Pour une tâche complexe, demandez : « Avant de rédiger, pose-moi les questions dont tu as besoin. » L'assistant révèle les informations qui lui manquent au lieu de les inventer."],
   ["Proposer plusieurs versions", "Demander trois variantes (plus courte, plus ferme, plus diplomatique) aide à choisir et à comprendre les leviers de style."],
   ["Nouvelle conversation", "Changez de conversation quand le sujet change, quand l'échange devient très long ou quand l'assistant s'enferre dans une erreur. Reprenez alors l'essentiel en quelques lignes."],
   ["Faire critiquer", "Demandez à l'assistant de relire sa propre réponse selon des critères donnés (exactitude, ton, oubli), puis de la corriger. C'est utile, mais ne remplace pas votre relecture."]
  ],
  "res": [["skfluency", "Partie « Description » et « Discernment » du cours AI Fluency."]],
  "ex": [
   {"t": "Demandez un courriel fictif, puis améliorez-le en trois corrections ciblées sans jamais recommencer la demande.", "c": "Le carnet garde les trois corrections et la version finale."},
   {"t": "Sur une tâche de votre métier, commencez par « pose-moi d'abord tes questions ».", "c": "Vous avez noté au moins une information que vous auriez oublié de donner."}
  ],
  "quiz": [
   mcq("La réponse est trop longue et trop familière. Le meilleur réflexe :", ["Recommencer la demande depuis le début", "Demander « fais mieux »", "Dire « trois paragraphes, ton professionnel »", "Changer d'assistant"], 2, "Une correction précise s'applique au brouillon existant."),
   mcq("Pourquoi faire poser des questions à l'assistant avant une tâche complexe ?", ["Pour gagner du temps de saisie", "Pour qu'il révèle ce qui lui manque", "Pour tester ses connaissances", "Pour allonger sa réponse"], 1, "Il identifie les informations manquantes au lieu de les inventer."),
   mcq("Quand ouvrir une nouvelle conversation ?", ["À chaque nouvelle question, sans exception", "Quand le sujet change ou que l'échange s'enlise", "Jamais : l'historique aide toujours", "Seulement en fin de journée"], 1, "Un historique long ou erroné pèse sur les réponses suivantes."),
   mcq("Demander trois variantes d'un courriel sert surtout à :", ["Comparer et choisir le bon ton", "Contourner une limite de l'outil", "Obtenir une réponse sans erreur", "Remplir la fenêtre de contexte"], 0, "La comparaison montre les leviers de style."),
   mcq("L'auto-relecture par l'assistant :", ["Remplace votre relecture", "Aide, sans remplacer votre relecture", "Est inutile sur un texte court", "Garantit l'absence d'erreur"], 1, "Elle améliore souvent le texte, mais la responsabilité reste la vôtre.")
  ],
  "drills": [
   tf("Une correction ciblée donne en général un meilleur résultat qu'une nouvelle demande vague.", True, "L'assistant garde ce qui allait et corrige ce que vous signalez."),
   cloze("« Avant de rédiger, pose-moi les ___ dont tu as besoin. »", ["questions", "excuses", "sources"], 0, "Faire questionner révèle les informations manquantes."),
   order("Remettez dans l'ordre un cycle d'amélioration.", ["Lire le brouillon", "Nommer précisément le défaut", "Demander la correction", "Relire la nouvelle version"], "Chaque tour part d'un constat précis."),
   tf("Une conversation très longue améliore toujours la qualité des réponses.", False, "Au-delà d'un certain volume, le début est moins bien pris en compte et les erreurs s'accumulent."),
   match("Associez chaque situation à la bonne relance.", [["Ton trop sec", "Rends-le plus diplomatique"], ["Oubli d'un point", "Ajoute la clause 7"], ["Tâche floue", "Pose-moi d'abord tes questions"]], "Chaque défaut appelle une relance précise.")
  ]
 },
 {
  "id": "so5", "cote": "S5", "titre": "Travailler avec des documents", "duree": "40 min",
  "comp": ["produire", "formuler"], "cadre": 1,
  "obj": ["Joindre un document et cadrer ce qu'on en attend", "Extraire, résumer, comparer", "Connaître les limites de lecture"],
  "notions": [
   ["Joindre ou coller", "Les assistants acceptent des fichiers (PDF, Word, tableur) ou du texte collé. Un PDF scanné peut être mal lu : vérifiez sur un passage que le texte a bien été reconnu."],
   ["Extraire", "Demandez des champs précis : parties, durée, montant, droit applicable. Exigez la valeur « non mentionné » quand l'information manque, sinon l'assistant risque de la deviner."],
   ["Résumer pour quelqu'un", "Un résumé dépend de son lecteur : décideur, juriste, chercheur. Précisez-le, ainsi que la longueur et ce qui doit absolument y figurer."],
   ["Comparer", "Deux versions d'un même texte : demandez un tableau des différences, article par article, avec citation des deux versions. Contrôlez ensuite deux ou trois lignes vous-même."],
   ["Documents longs", "Placez le document avant la question. Sur un texte très long, l'assistant peut survoler certaines parties : demandez-lui de citer les passages sur lesquels il s'appuie."]
  ],
  "res": [["promptdoc", "Conseils sur les documents longs (documentation Anthropic, en anglais)."]],
  "ex": [
   {"t": "Avec un NDA public, faites extraire dans un tableau : parties, objet, durée, exceptions à la confidentialité, droit applicable, avec « non mentionné » si absent.", "c": "Le tableau est complet et vous avez vérifié deux cases sur le texte."},
   {"t": "Comparez deux versions d'un texte fictif que vous avez modifié vous-même (trois changements).", "c": "L'assistant retrouve les trois changements ; s'il en manque un, vous l'avez noté."}
  ],
  "quiz": [
   mcq("Le contrat ne mentionne pas le droit applicable. Que doit prévoir la demande ?", ["Rien, l'assistant le verra", "La valeur « non mentionné » si absent", "De le déduire de la nationalité des parties", "De retirer ce champ du tableau"], 1, "Sans cette consigne, l'assistant risque de combler le vide."),
   mcq("Un PDF scanné est joint. Premier réflexe ?", ["Vérifier qu'un passage a bien été lu", "Demander directement la synthèse", "Le convertir en image", "Le traduire en anglais"], 0, "La reconnaissance du texte peut être défaillante."),
   mcq("Un bon résumé commence par préciser :", ["Le nombre de mots exact", "Le lecteur et son besoin", "La police de caractères", "Le nom de l'auteur"], 1, "Un résumé pour un décideur n'est pas celui d'un juriste."),
   mcq("Pour comparer deux versions d'un contrat, la sortie la plus utile est :", ["Un avis général sur les évolutions", "Un tableau article par article avec citations", "Un résumé de la version finale", "La liste des articles inchangés"], 1, "Le tableau rend chaque différence vérifiable."),
   mcq("Sur un document très long, comment fiabiliser la réponse ?", ["Demander une réponse plus courte", "Exiger les passages cités à l'appui", "Augmenter le nombre de questions", "Joindre le document deux fois"], 1, "Les citations rendent la réponse contrôlable.")
  ],
  "drills": [
   tf("Un assistant lit toujours parfaitement un PDF scanné.", False, "La reconnaissance de texte peut échouer ; vérifiez un passage."),
   cloze("Pour un champ absent, exigez la valeur « ___ ».", ["non mentionné", "à déduire", "probable"], 0, "Sinon l'assistant risque de fabriquer l'information."),
   order("Remettez dans l'ordre une extraction fiable.", ["Joindre le document", "Lister les champs attendus", "Exiger « non mentionné » si absent", "Contrôler deux cases sur le texte"], "La vérification par sondage clôt toute extraction."),
   match("Associez le besoin à la bonne demande.", [["Décideur pressé", "Résumé de huit lignes"], ["Deux versions", "Tableau des différences"], ["Fiche contrat", "Extraction de champs"]], "La forme suit l'usage."),
   tf("Placer la question après un long document aide l'assistant.", True, "Document d'abord, question et consignes à la fin.")
  ]
 },
 {
  "id": "so6", "cote": "S6", "titre": "Vérifier et fiabiliser", "duree": "40 min",
  "comp": ["verifier"], "cadre": 1,
  "obj": ["Réduire les inventions par la consigne", "Utiliser la recherche web à bon escient", "Contrôler une référence juridique"],
  "notions": [
   ["Autoriser l'ignorance", "Écrivez : « Si l'information ne figure pas dans le document ou si tu n'es pas sûr, dis-le. » Sans cette autorisation, l'assistant tend à combler les vides."],
   ["Citer d'abord", "Demandez d'extraire mot pour mot les passages utiles, puis de répondre uniquement à partir d'eux. Chaque affirmation devient vérifiable."],
   ["Recherche web", "Quand l'assistant cherche sur le web, il indique ses sources. Ouvrez-les : une source citée peut ne pas dire ce que l'assistant affirme, ou dater. Préférez les sources officielles."],
   ["Références juridiques", "Article de code : Légifrance, version en vigueur. Jurisprudence : Judilibre ou Légifrance. Texte européen : EUR-Lex. Une référence non vérifiée ne sort jamais dans un document transmis."],
   ["Ce que vous signez", "L'assistant propose ; vous validez. Tout document qui part sous votre nom engage votre responsabilité, quelle que soit la part écrite par l'IA."]
  ],
  "res": [["legi", "Légifrance."], ["judilibre", "Judilibre, moteur de la Cour de cassation."]],
  "ex": [
   {"t": "Posez sur un NDA public une question dont la réponse n'y figure pas (montant d'une pénalité). Une fois sans, une fois avec « dis-le si ce n'est pas dans le texte ».", "c": "Vous avez constaté la différence et noté la meilleure formulation."},
   {"t": "Demandez avec recherche web les dernières évolutions d'un sujet de votre métier, puis ouvrez chaque source citée.", "c": "Pour chaque source : elle dit bien ce qui est affirmé, ou l'écart est noté."}
  ],
  "quiz": [
   mcq("Quelle consigne réduit le plus les réponses inventées sur un document ?", ["« Sois exhaustif et précis »", "« Réponds sans hésiter »", "« Si ce n'est pas dans le texte, dis-le »", "« Tu es le meilleur expert »"], 2, "Autoriser l'ignorance évite de combler les vides."),
   mcq("L'assistant donne trois sources web. Que faire ?", ["Les citer telles quelles", "Ouvrir chacune et vérifier ce qu'elle dit", "Garder la plus récente", "Demander trois autres sources"], 1, "Une source citée peut ne pas soutenir l'affirmation."),
   mcq("Où vérifier un article du Code de la propriété intellectuelle ?", ["Sur Légifrance, version en vigueur", "Dans la réponse d'un second assistant", "Sur un blog juridique récent", "Dans la mémoire de l'assistant"], 0, "La source officielle donne la rédaction en vigueur."),
   mcq("« Citer d'abord » signifie :", ["Commencer la réponse par une citation célèbre", "Extraire les passages puis répondre à partir d'eux", "Citer l'auteur de chaque document", "Mettre la question entre guillemets"], 1, "La réponse s'ancre dans le texte fourni."),
   mcq("Un courriel rédigé avec l'IA contient une erreur. Qui en répond ?", ["L'éditeur de l'outil", "La personne qui l'envoie", "Le service informatique", "Personne, c'est l'IA"], 1, "Ce qui part sous votre nom vous engage.")
  ],
  "drills": [
   tf("Une source citée par l'assistant confirme toujours ce qu'il affirme.", False, "Il faut ouvrir la source : elle peut dire autre chose ou dater."),
   match("Associez chaque référence à sa source officielle.", [["Article de code", "Légifrance"], ["Arrêt de cassation", "Judilibre"], ["Règlement européen", "EUR-Lex"]], "Chaque type de texte a sa base officielle."),
   cloze("Pour fiabiliser, demandez d'abord les ___ exactes, puis la réponse.", ["citations", "conclusions", "excuses"], 0, "Les citations rendent chaque affirmation vérifiable."),
   tf("Autoriser l'assistant à répondre « je ne sais pas » réduit les inventions.", True, "Sans cette autorisation, il tend à combler les vides."),
   order("Remettez dans l'ordre le contrôle d'une référence citée.", ["Relever la référence exacte", "Ouvrir la source officielle", "Comparer texte et version en vigueur", "Intégrer ou corriger"], "On isole la référence, puis on la confronte à la source.")
  ]
 },
 {
  "id": "so7", "cote": "S7", "titre": "Rédiger avec l'IA", "duree": "40 min",
  "comp": ["produire"], "cadre": 1,
  "obj": ["Faire rédiger dans votre style", "Réécrire, raccourcir, changer de ton", "Éviter l'écriture qui sonne « IA »"],
  "notions": [
   ["Donner son style", "Collez un ou deux textes que vous avez écrits et demandez de reprendre le ton, la longueur des phrases et les formules. Précisez vos interdits (formules creuses, listes à puces dans un courriel)."],
   ["Réécrire plutôt qu'écrire", "Le plus efficace est souvent d'écrire un premier jet rapide et de demander : « clarifie, raccourcis d'un tiers, garde mes idées ». Vous restez l'auteur du fond."],
   ["Les signes d'un texte IA", "Mots gonflés (crucial, essentiel, véritable), triples énumérations par réflexe, phrases d'accroche, « en conclusion », tirets longs, ton enthousiaste. Demandez explicitement de les éviter, puis relisez."],
   ["Courriels à un tiers", "Prose en paragraphes, une idée par paragraphe, sans liste à puces, dix lignes environ. Le détail va en pièce jointe."],
   ["Traduction", "L'assistant traduit bien les textes courants. Pour un contrat, faites vérifier les termes juridiques : un faux ami peut changer une obligation."]
  ],
  "res": [["skfluency", "Partie « Diligence » du cours AI Fluency."]],
  "ex": [
   {"t": "Donnez à l'assistant deux de vos courriels anonymisés ou fictifs, puis faites rédiger une relance fictive dans votre style.", "c": "La relance pourrait passer pour la vôtre après au plus deux retouches."},
   {"t": "Faites réécrire un paragraphe que vous trouvez lourd : « raccourcis d'un tiers, sans perdre d'information ».", "c": "Le texte est plus court et vous avez vérifié qu'aucune idée n'a disparu."}
  ],
  "quiz": [
   mcq("Comment obtenir un texte dans votre style ?", ["Demander « écris comme un humain »", "Fournir un ou deux de vos textes", "Utiliser une température élevée", "Changer de langue"], 1, "Des exemples réels transmettent le ton mieux qu'une consigne abstraite."),
   mcq("Lequel est un signe fréquent d'un texte généré ?", ["Des phrases de longueur variable", "Des énumérations en trois par réflexe", "Une idée par paragraphe", "Des chiffres précis et sourcés"], 1, "Le trio systématique est un tic d'écriture générée."),
   mcq("Pour un courriel à une contrepartie, la forme attendue est :", ["Une liste à puces détaillée", "Des paragraphes courts, une idée chacun", "Un tableau des points", "Des titres en gras"], 1, "La prose en paragraphes reste la norme pour un tiers."),
   mcq("Vous traduisez une clause de contrat. Que vérifier ?", ["La longueur de la traduction", "Les termes juridiques et faux amis", "La ponctuation seulement", "Le nombre de phrases"], 1, "Un faux ami peut changer la portée d'une obligation."),
   mcq("Quel usage garde le mieux la maîtrise du fond ?", ["Faire tout écrire puis signer", "Écrire un premier jet puis faire clarifier", "Demander plusieurs textes et en fusionner deux", "Copier un modèle trouvé en ligne"], 1, "Le fond reste le vôtre, l'assistant améliore la forme.")
  ],
  "drills": [
   tf("Fournir vos propres textes aide l'assistant à reprendre votre style.", True, "Les exemples réels transmettent ton et formules."),
   cloze("« Raccourcis d'un ___, sans perdre d'information. »", ["tiers", "titre", "tableau"], 0, "Une consigne chiffrée et une limite claire donnent un résultat contrôlable."),
   match("Associez chaque tic à sa correction.", [["« Il est crucial de »", "Dire le fait directement"], ["Trois exemples par réflexe", "Le nombre réel d'éléments"], ["« En conclusion »", "Supprimer, finir sur l'information"]], "Ces corrections rendent le texte plus naturel."),
   tf("Un courriel à un partenaire se rédige de préférence en liste à puces.", False, "Prose en paragraphes, une idée par paragraphe."),
   order("Remettez dans l'ordre une rédaction assistée.", ["Écrire un premier jet rapide", "Demander clarification et raccourci", "Relire et retoucher", "Envoyer sous votre responsabilité"], "Vous gardez le fond et la décision finale.")
  ]
 },
 {
  "id": "so8", "cote": "S8", "titre": "Analyser, raisonner, décider", "duree": "40 min",
  "comp": ["produire", "verifier"], "cadre": 1,
  "obj": ["Faire raisonner avant de conclure", "Guider par des exemples", "Découper une tâche longue en étapes"],
  "notions": [
   ["Raisonner d'abord", "Demandez d'exposer le raisonnement avant la conclusion. Écrit avant, il sert la réponse ; écrit après, il la justifie seulement. Certains assistants ont un mode « réflexion » qui le fait d'eux-mêmes."],
   ["Exemples", "Deux ou trois exemples résolus (entrée et résultat attendu) guident mieux qu'une longue explication. Variez-les : des exemples trop semblables sont imités trop fidèlement."],
   ["Découper", "Une tâche longue se traite en étapes : extraire, puis analyser, puis rédiger. Vous contrôlez le résultat de chaque étape avant la suivante."],
   ["Grille de décision", "Pour comparer des options, imposez les critères et leur poids, puis demandez un tableau et une recommandation argumentée. Vous gardez la décision."],
   ["Avocat du diable", "Demandez : « Quels sont les trois meilleurs arguments contre cette conclusion ? » Utile avant une réunion ou une négociation."]
  ],
  "res": [["dair", "Prompt Engineering Guide (DAIR.AI), en français partiellement."]],
  "ex": [
   {"t": "Faites classer dix clauses fictives en catégories (confidentialité, PI, durée, responsabilité) avec trois exemples variés dans la demande.", "c": "Au moins huit clauses sur dix sont bien classées ; les erreurs sont notées."},
   {"t": "Sur une décision fictive (choisir un prestataire), imposez trois critères pondérés et demandez le tableau, puis l'avocat du diable.", "c": "Le carnet garde la grille et l'argument contraire le plus utile."}
  ],
  "quiz": [
   mcq("Pourquoi demander le raisonnement avant la conclusion ?", ["Pour économiser des mots", "Pour que la conclusion s'appuie dessus", "Pour que le texte soit plus long", "L'ordre est indifférent"], 1, "Écrit avant, le raisonnement sert la réponse."),
   mcq("Quel est le risque d'exemples trop semblables ?", ["L'assistant les imite trop", "L'assistant refuse de répondre", "Le coût double", "Ils sont ignorés"], 0, "Variez les exemples et couvrez les cas limites."),
   mcq("Une tâche demande d'extraire, comparer puis rédiger. Meilleure approche ?", ["Tout demander en une fois", "Découper en étapes contrôlées", "Demander une réponse courte", "Changer d'assistant à chaque étape"], 1, "Chaque étape se vérifie avant la suivante."),
   mcq("Pour choisir entre trois options, vous imposez :", ["La conclusion attendue", "Les critères et leur poids", "La longueur de la réponse", "Le nom des options seulement"], 1, "La grille rend la recommandation discutable et vérifiable."),
   mcq("Dans un cas fictif, qui est co-titulaire d'une invention ?", ["Celui qui a financé la recherche", "Celui qui a apporté une contribution inventive", "Celui qui a fourni le matériel", "Celui qui a passé le plus de temps"], 1, "La co-titularité repose sur l'apport inventif, non sur les ressources.")
  ],
  "drills": [
   tf("Des exemples variés améliorent un classement fait par l'assistant.", True, "Ils couvrent les cas limites et évitent l'imitation servile."),
   order("Remettez dans l'ordre l'analyse d'un contrat en étapes.", ["Extraire les clauses", "Comparer à la trame de référence", "Rédiger la synthèse des écarts"], "Chaque étape utilise le résultat contrôlé de la précédente."),
   cloze("Demander les meilleurs arguments contre sa propre conclusion, c'est jouer l'___.", ["avocat du diable", "expert-comptable", "arbitre"], 0, "Le contre-argument prépare la discussion."),
   tf("Le raisonnement de l'assistant, écrit après sa conclusion, a la même utilité.", False, "Écrit après, il justifie une conclusion déjà prise."),
   match("Associez chaque technique à son usage.", [["Exemples résolus", "Classer selon un modèle"], ["Découpage", "Tâche longue"], ["Grille pondérée", "Comparer des options"]], "Chaque technique répond à un type de tâche.")
  ]
 },
 {
  "id": "so9", "cote": "S9", "titre": "Les fonctions avancées de votre assistant", "duree": "45 min",
  "comp": ["organiser"], "cadre": 1,
  "obj": ["Connaître les grandes familles de fonctions", "Utiliser instructions personnalisées et espaces de projet", "Savoir ce que fait la mémoire de l'assistant"],
  "notions": [
   ["Instructions personnalisées", "Un texte que l'assistant lit avant chaque conversation : votre métier, votre style, vos interdits. Il évite de répéter le contexte. Le nom varie selon l'outil (instructions personnalisées, préférences, profil)."],
   ["Espaces de projet", "Un espace regroupe des conversations, des documents de référence et des instructions propres à un sujet (par exemple « Projets » chez Claude ou ChatGPT, « GPT » personnalisé chez ChatGPT). Utile pour un gabarit maison réutilisé souvent. [Non vérifié] Les noms et limites évoluent ; la veille hebdomadaire les met à jour."],
   ["Mémoire", "Certains assistants retiennent des éléments d'une conversation à l'autre. Vérifiez ce qui est mémorisé, effacez ce qui ne doit pas l'être, et n'y laissez jamais d'information confidentielle."],
   ["Recherche approfondie", "Un mode qui enchaîne de nombreuses recherches web et rend un rapport sourcé en quelques minutes. Efficace pour un état des lieux ; les sources se vérifient comme toujours."],
   ["Création de documents", "Les assistants produisent aussi des tableaux, des pages, des schémas, des images ou des fichiers (Artifacts chez Claude, Canvas chez ChatGPT). Le résultat se relit comme tout livrable."]
  ],
  "res": [["sk101", "Claude 101 (Anthropic Academy), en anglais."], ["oaiacad", "OpenAI Academy (en anglais)."]],
  "ex": [
   {"t": "Rédigez vos instructions personnalisées : métier, destinataires habituels, style, trois interdits. Activez-les dans votre assistant si l'entreprise le permet.", "c": "Une nouvelle conversation reprend votre style sans que vous le rappeliez."},
   {"t": "Ouvrez les réglages de mémoire de votre assistant et notez ce qu'il retient de vous.", "c": "Vous savez consulter et effacer la mémoire."}
  ],
  "quiz": [
   mcq("À quoi servent les instructions personnalisées ?", ["À donner un contexte lu avant chaque conversation", "À accélérer la connexion", "À traduire l'interface", "À augmenter la limite de fichiers"], 0, "Elles évitent de répéter votre contexte à chaque fois."),
   mcq("Un espace de projet est surtout utile pour :", ["Une question isolée", "Un sujet récurrent avec documents de référence", "Changer de langue", "Partager son mot de passe"], 1, "Il regroupe instructions, documents et conversations d'un même sujet."),
   mcq("La mémoire de l'assistant contient une information confidentielle. Que faire ?", ["La laisser, elle est privée", "L'effacer et éviter de la saisir", "Changer de compte", "Demander à l'assistant de l'oublier en conversation"], 1, "Effacez depuis les réglages et ne saisissez pas ce type d'information."),
   mcq("La recherche approfondie rend un rapport sourcé. Ensuite ?", ["Le transmettre tel quel", "Vérifier les sources clés", "Le traduire", "Le raccourcir de moitié"], 1, "Les sources se vérifient, quel que soit le mode."),
   mcq("Pourquoi les noms de fonctions de ce chapitre sont-ils marqués comme évolutifs ?", ["Ils changent souvent selon les outils", "Ils sont secrets", "Ils sont réservés aux développeurs", "Ils n'existent qu'en anglais"], 0, "Les éditeurs renomment et modifient souvent leurs fonctions.")
  ],
  "drills": [
   match("Associez chaque fonction à son usage.", [["Instructions personnalisées", "Contexte permanent"], ["Espace de projet", "Sujet récurrent"], ["Recherche approfondie", "Rapport sourcé"], ["Mémoire", "Souvenirs entre conversations"]], "Les noms varient, les familles restent."),
   tf("La mémoire de l'assistant peut contenir des informations confidentielles sans risque.", False, "Ce qui est mémorisé doit être contrôlé et nettoyé."),
   cloze("Un espace qui regroupe documents et instructions d'un même sujet s'appelle un ___.", ["projet", "token", "prompt système"], 0, "Le nom exact dépend de l'outil."),
   tf("Un rapport de recherche approfondie n'a pas besoin d'être vérifié.", False, "Les sources se vérifient toujours."),
   order("Remettez dans l'ordre la mise en place d'un espace de projet.", ["Définir le sujet récurrent", "Rédiger ses instructions", "Ajouter les documents de référence autorisés", "Tester sur un cas fictif"], "Le test sur un cas fictif valide la configuration.")
  ]
 },
 {
  "id": "so10", "cote": "S10", "titre": "Votre méthode et votre bibliothèque", "duree": "45 min",
  "comp": ["organiser", "produire"], "cadre": 1,
  "obj": ["Constituer une bibliothèque de demandes réutilisables", "Choisir les tâches où l'IA fait gagner du temps", "Mesurer et partager ce qui marche"],
  "notions": [
   ["Gabarit", "Une demande qui marche se garde avec des variables : « Résume [DOCUMENT] pour [LECTEUR] en [N] lignes ». Rangez-la avec son usage, sa date et un exemple de résultat."],
   ["Bonnes tâches", "L'IA aide surtout pour : premier jet, reformulation, synthèse, extraction, comparaison, préparation de questions, relecture. Elle aide moins pour : décision finale, fait récent non sourcé, calcul critique non vérifié."],
   ["Mesurer le gain", "Notez le temps sans IA, le temps avec, et le nombre de retouches. Une tâche qui demande plus de corrections qu'elle n'en économise sort de la liste."],
   ["Partager", "Une bonne demande partagée profite à l'équipe. Partagez la demande et ses limites, jamais un document de dossier."],
   ["Rester à jour", "Les outils évoluent chaque semaine. Le parcours ajoute des nouveautés et des défis chaque semaine : quelques minutes suffisent pour garder la main."]
  ],
  "res": [["skfluency", "Synthèse du cadre des 4D (AI Fluency)."]],
  "ex": [
   {"t": "Rangez dans le carnet cinq demandes réutilisables, chacune avec variables, usage et limite.", "c": "Cinq gabarits utilisables par un collègue sans explication."},
   {"t": "Mesurez sur une tâche réelle autorisée le temps avec et sans assistant.", "c": "Le carnet indique les deux temps et le nombre de retouches."}
  ],
  "quiz": [
   mcq("Qu'est-ce qu'un bon gabarit ?", ["Une demande avec variables, usage et limite", "Une conversation archivée en entier", "Une réponse copiée dans un document", "Une liste de mots-clés"], 0, "Le gabarit se réutilise sur d'autres données."),
   mcq("Pour quelle tâche l'IA aide-t-elle le moins ?", ["Un premier jet de courriel", "La décision finale sur un dossier", "La synthèse d'un compte rendu", "La reformulation d'un paragraphe"], 1, "La décision reste humaine."),
   mcq("Une tâche demande plus de retouches qu'elle ne fait gagner. Conclusion ?", ["Augmenter la longueur de la demande", "La retirer de la liste des usages", "Changer d'assistant aussitôt", "La garder par principe"], 1, "On garde ce qui fait réellement gagner du temps."),
   mcq("Que peut-on partager avec l'équipe ?", ["La demande et ses limites", "Le document du dossier traité", "Son mot de passe d'outil", "L'historique complet du compte"], 0, "Les méthodes se partagent, pas les données."),
   mcq("Comment garder la main quand les outils changent ?", ["Attendre la prochaine formation", "Quelques minutes de nouveautés chaque semaine", "Tout réapprendre chaque mois", "Changer d'outil souvent"], 1, "La pratique régulière suffit à suivre l'évolution.")
  ],
  "drills": [
   cloze("« Résume [DOCUMENT] pour [LECTEUR] » est un ___ réutilisable.", ["gabarit", "token", "projet"], 0, "Les variables entre crochets se remplacent à chaque usage."),
   match("Associez chaque tâche à l'apport de l'IA.", [["Premier jet", "Gain de temps net"], ["Décision finale", "Reste humaine"], ["Fait récent", "À sourcer et vérifier"]], "L'IA prépare, vous décidez."),
   tf("Partager une bonne demande avec l'équipe expose les dossiers.", False, "On partage la méthode, jamais les documents."),
   order("Remettez dans l'ordre la vie d'un gabarit.", ["Réussir une demande", "La transformer avec des variables", "La ranger avec usage et limite", "La revoir quand l'outil change"], "Un gabarit se maintient."),
   tf("Mesurer le temps gagné aide à choisir les bons usages.", True, "La mesure distingue l'impression du gain réel.")
  ]
 }
]
