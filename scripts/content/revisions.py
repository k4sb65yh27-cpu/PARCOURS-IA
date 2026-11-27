# Révisions du 27/11/2026 (spécification v0.2.1, sections 6 et 7), appliquées après les variantes par profil.
# Chaque révision remplace une valeur à un chemin existant : identifiants, nombre de questions et
# indices d'exercices restent inchangés, donc les progressions restent valides.
from socle import mcq, tf, cloze, match

REGLE_SKILLS = "À ce stade, les skills relèvent de l'utilisation sur projets personnels ; l'ajout d'un skill nécessite de demander l'aval du RSI ou du référent IA."

SRC_PLUS = {
 "promptbp": {"n": "Anthropic, Prompting best practices", "u": "https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/be-clear-and-direct"},
 "usagebp": {"n": "Anthropic, Usage limit best practices", "u": "https://support.claude.com/en/articles/9797557-usage-limit-best-practices"},
 "limits": {"n": "Anthropic, How usage and length limits work", "u": "https://support.claude.com/en/articles/11647753-how-usage-and-length-limits-work"},
 "skillsuse": {"n": "Anthropic, Use skills in Claude", "u": "https://support.claude.com/en/articles/12512180-use-skills"},
 "oaiskills": {"n": "OpenAI, Skills in ChatGPT", "u": "https://help.openai.com/articles/20001066-skills-in-chatgpt"},
}

# (étape, chemin, valeur de base, {profil: valeur propre}) ; un profil absent reçoit la valeur de base.
REV = [
 # C3 : étiquettes retirées, affirmations reformulées
 ("s8", "notions.3", ["Découpage par unité de sens", "Pour un recueil de procédures ou de modèles, découpez par section plutôt que par page et attachez des métadonnées (type, version, statut) : chaque extrait retrouvé arrive complet et situé."],
  {"juriste": ["Découpage juridique", "Pour un clausier, découpez par clause plutôt que par page et attachez des métadonnées (type de clause, version, statut) : chaque extrait retrouvé arrive complet et situé."]}),
 ("s9", "notions.2", ["Workflow ou agent", "Quand les étapes sont connues d'avance (extraire, comparer, rédiger), un enchaînement fixe se contrôle plus facilement qu'un agent autonome et consomme moins d'appels."], {}),
 ("s10", "notions.2", ["Coût et complexité", "Plusieurs agents multiplient les appels, donc les tokens, et rendent les erreurs plus difficiles à localiser. Ils se justifient quand des sous-tâches sont indépendantes ou demandent des expertises distinctes."], {}),
 ("s11", "notions.3", ["Tokenisation BPE", "Le découpage en tokens est appris en fusionnant les paires de caractères les plus fréquentes. Le modèle voit donc des tokens et non des lettres, ce qui explique en partie ses erreurs quand il compte des lettres."], {}),
 ("xc", "notions.4", ["Pourquoi ce n'est pas au poste", "Ces outils accèdent aux fichiers, à la messagerie ou au réseau de l'entreprise. Leur déploiement suppose une décision sur la sécurité, la confidentialité et les contrats avec l'éditeur ; le cadre actuel de la SATT reste donc limité au navigateur. Sur un ordinateur personnel, avec un compte personnel et des fichiers fictifs, ils s'explorent sans risque pour l'entreprise."], {}),
 # C4 : réglage de température refusé par plusieurs modèles récents
 ("s7", "ex.2", {"t": "Lancer trois fois la même consigne rédactionnelle à température 0, puis à température 1, et comparer. Plusieurs modèles récents refusent ce réglage (documentation de l'API Claude) : vérifier d'abord que le modèle choisi l'accepte.", "c": "Différences notées dans le carnet."}, {}),
 # K3 et K4 : s9b, exemples officiels et projet personnel
 ("s9b", "notions.5", ["Exemple : les skills officiels d'Anthropic", "Anthropic publie des skills prêts à l'emploi, par exemple pour créer des documents Word, des classeurs Excel ou des présentations PowerPoint. Ils servent ici de modèles de structure : un nom, une description qui dit quand s'en servir, des instructions, parfois des scripts. " + REGLE_SKILLS], {}),
 ("s9b", "ex.0", {"t": "Sur un projet personnel, rédiger un SKILL.md pour une tâche fictive répétitive (par exemple la fiche de synthèse d'un document public), sans l'installer sur un compte professionnel.", "c": "Le fichier contient un nom, une description qui dit quand le déclencher, des étapes, un format de sortie et une règle de citation. Un test sur un document fictif est consigné dans le carnet."}, {}),
 # K5 : bonus, skills officiels et règle d'usage
 ("bonus", "notions.0", ["Skills officiels", "Anthropic fournit des skills pour créer des documents Word, des classeurs Excel et des présentations PowerPoint. Au poste, les exercices de cet atelier se font avec la création de documents intégrée à l'assistant ; les skills officiels s'essaient sur un projet personnel."], {}),
 ("bonus", "notions.1", ["Règle d'usage", REGLE_SKILLS + " Les skills publiés par des tiers ne servent pas d'exemple dans ce parcours."], {}),
 ("bonus", "quiz.0", mcq("Que permettent les skills officiels présentés dans cet atelier ?", ["Signer des documents à la place de leur auteur", "Accéder à de nouveaux modèles sans compte", "Créer des documents Word, Excel et PowerPoint", "Entraîner un modèle de langage sur vos données"], 2, "Anthropic les fournit pour produire des documents bureautiques."), {}),
 ("bonus", "quiz.1", mcq("Vous voulez ajouter un skill. Que faire d'abord ?", ["L'installer puis prévenir si quelqu'un pose la question", "Demander l'aval du RSI ou du référent IA", "Choisir le skill le plus téléchargé du moment", "Le tester sur un vrai dossier pour juger de son intérêt"], 1, REGLE_SKILLS), {}),
 ("bonus", "drills.2", match("Associez chaque skill officiel à ce qu'il produit.", [["Skill Word", "Document de traitement de texte"], ["Skill Excel", "Classeur avec formules"], ["Skill PowerPoint", "Présentation"]], "Ces trois skills sont fournis par Anthropic."), {}),
 ("bonus", "quiz.3", mcq("Quel dépôt réunit les skills officiels d'Anthropic ?", ["anthropics/courses, dépôt de cours archivé", "anthropics/skills", "Un dépôt personnel repéré sur un forum", "microsoft/autogen, dépôt d'un framework"], 1, "anthropics/skills est le dépôt officiel."), {}),
 ("bonus", "res", [["anthskills", "Dépôt officiel anthropics/skills : lire la structure d'un skill de document."], ["skillsuse", "Anthropic : activer et utiliser des skills (en anglais)."]], {}),
 ("s9b", "res", [["skskills", "« Introduction to Agent Skills » : construire, configurer et partager des skills dans Claude Code."], ["sksub", "« Introduction to subagents » (4 leçons)."], ["skcode", "« Claude Code in Action »."], ["anthskills", "Parcourir le dépôt officiel et lire deux skills."], ["skillsuse", "Anthropic : activer, déclencher et partager des skills (en anglais)."], ["modelblog", "Lire l'article en entier."]], {}),
]

# K2 : notions ajoutées en fin de liste (aucun chemin existant ne bouge)
APPEND_NOTIONS = {
 "s9b": [
  ["Activer et déclencher", "Sur claude.ai, les skills se gèrent dans Customize > Skills : on active un skill fourni ou on téléverse le sien sous forme de dossier compressé. L'assistant charge un skill quand la demande correspond à sa description ; on peut aussi le choisir en tapant « / ». ChatGPT propose des skills sur ses offres Business, Enterprise et Edu, selon le même standard ouvert."],
  ["Skill, instructions ou projet", "Les instructions personnalisées valent pour toutes les conversations ; un projet regroupe les documents et les consignes d'un sujet ; un skill décrit une méthode réutilisable (étapes, format de sortie, contrôles) que l'assistant applique quand la tâche s'y prête."],
  ["Risques et règle d'usage", "Un skill peut contenir des scripts et des instructions que l'assistant suit. Anthropic cite deux risques principaux : l'injection de prompt et la fuite de données. " + REGLE_SKILLS],
 ],
}

# C1 : exercice facultatif dans l'étape 5 de chaque voie Métier (ajouté en fin de liste)
APPEND_EX = {
 "me5": {"t": "Facultatif : transformez la consigne de votre tâche la plus fréquente (par exemple la fiche d'identité d'un accord de confidentialité fictif) en gabarit de projet : instructions permanentes, format de sortie, deux exemples fictifs.", "c": "Le gabarit produit le même format sur deux cas fictifs.", "opt": True},
 "mt5": {"t": "Facultatif : transformez la consigne de votre tâche la plus fréquente (par exemple le premier courriel de prospection vers un industriel fictif) en gabarit de projet : instructions permanentes, format de sortie, deux exemples fictifs.", "c": "Le gabarit produit le même format sur deux cas fictifs.", "opt": True},
 "mb5": {"t": "Facultatif : transformez la consigne de votre tâche la plus fréquente (par exemple la note de synthèse d'un document publié) en gabarit de projet : instructions permanentes, format de sortie, deux exemples fictifs.", "c": "Le gabarit produit le même format sur deux cas fictifs.", "opt": True},
 "ms5": {"t": "Facultatif : transformez la consigne de votre tâche la plus fréquente (par exemple le compte rendu d'une réunion fictive) en gabarit de projet : instructions permanentes, format de sortie, deux exemples fictifs.", "c": "Le gabarit produit le même format sur deux cas fictifs.", "opt": True},
}

def _d(id, comp, cadre, titre, consigne, critere):
  return {"id": id, "comp": comp, "cadre": cadre, "titre": titre, "consigne": consigne, "critere": critere}

# C2 : huit défis (aucun ne demande d'installer un skill)
DEFIS_PLUS = [
 _d("d25", "formuler", 1, "Le brief en un message", "Je vais te demander [tâche]. Avant de répondre, dis-moi quelles informations manquent à ma demande pour que tu puisses la traiter en une seule réponse : objectif, lecteur, matière, format, limites, critère de réussite.", "Vous avez réécrit la demande en un message et obtenu un résultat utilisable sans relance."),
 _d("d26", "formuler", 1, "Montrer plutôt que décrire", "Voici un exemple du résultat que j'attends : [collez un exemple fictif]. Produis le même type de résultat pour [nouveau cas fictif], en respectant la structure de l'exemple.", "Le résultat reprend la structure sans recopier le contenu de l'exemple."),
 _d("d27", "formuler", 1, "La consigne écrite par l'assistant", "Écris la consigne que je devrais te donner pour obtenir [résultat] sur une tâche fictive. Pose-moi d'abord tes questions, puis propose la consigne avec ses zones à compléter entre crochets.", "La consigne a été testée sur deux cas fictifs et rangée dans votre bibliothèque."),
 _d("d28", "organiser", 1, "Résumé de reprise", "Résume cette conversation en cinq lignes pour que je puisse la poursuivre dans une conversation neuve : sujet, décisions, documents utiles, prochaine étape, format attendu.", "La conversation neuve repart du résumé sans perte d'information utile."),
 _d("d29", "organiser", 1, "Relevé de consommation", "Réponds à cette question générale sans faire de recherche web : [question sans actualité].", "Vous avez relevé votre consommation dans les réglages avant et après, avec puis sans recherche web, et noté l'écart dans le carnet."),
 _d("d30", "organiser", 1, "Demandes groupées", "Voici trois demandes liées sur le même document fictif : [demande 1], [demande 2], [demande 3]. Traite-les dans une seule réponse, une section par demande.", "Une seule réponse couvre les trois demandes : deux échanges évités."),
 _d("d31", "dialoguer", 1, "Enchaîner sur la sortie", "À partir du tableau que tu viens de produire, rédige le courriel de synthèse pour [destinataire fictif], en laissant de côté les lignes sans enjeu.", "Le courriel reprend le tableau sans que vous ayez recollé la matière."),
 _d("d32", "dialoguer", 1, "Le bon réglage", "Je vais te confier deux tâches : [reformulation courte] et [comparaison de deux documents fictifs]. Pour chacune, dis-moi quel mode, quel modèle et quel niveau d'effort conviennent, et pourquoi.", "Vous avez appliqué le réglage proposé et constaté la différence de temps de réponse."),
]

# Point 5 : statut des brèves sans crochets
NEWS_STATUT = {"[Non vérifié] source secondaire": "source secondaire, non vérifiée"}


def _setp(o, path, v):
  ks = path.split('.')
  for k in ks[:-1]: o = o[int(k)] if isinstance(o, list) else o[k]
  last = ks[-1]
  if isinstance(o, list): o[int(last)] = v
  else: o[last] = v


def apply(steps, defis, news, src, pids):
  by = {s['id']: s for s in steps}
  for sid, path, base, per in REV:
    s = by[sid]
    _setp(s, path, base)
    pv = s.get('pv', {})
    for p in list(pv):
      pv[p].pop(path, None)
      if not pv[p]: del pv[p]
    for p, v in per.items():
      if v != base: pv.setdefault(p, {})[path] = v
    if pv: s['pv'] = pv
    else: s.pop('pv', None)
  for sid, lst in APPEND_NOTIONS.items():
    by[sid]['notions'].extend(lst)
  for sid, e in APPEND_EX.items():
    by[sid]['ex'].append(e)
  known = {d['id'] for d in defis}
  defis.extend(d for d in DEFIS_PLUS if d['id'] not in known)
  for n in news:
    for it in n['items']:
      it['statut'] = NEWS_STATUT.get(it['statut'], it['statut'])
  src.update(SRC_PLUS)
  # Sources des skills tiers retirés (point ouvert 4) : supprimées si plus aucune étape ne les cite.
  used = {k for s in steps for k, _ in s['res']}
  for k in ['socratic', 'archdiag', 'huashu', 'guizang', 'hallmark', 'impeccable']:
    if k not in used: src.pop(k, None)
