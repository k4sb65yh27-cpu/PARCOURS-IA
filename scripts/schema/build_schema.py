# Schéma des notions par voie Métier : notions communes et propres à chaque métier.
import json, html
c = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__file__), '../../src/data/content.json')))
P = [('juriste', 'Juriste'), ('cdt', 'Chargé de transfert'), ('brevet', 'Ingénieur brevet'), ('support', 'Support et direction')]
# Équivalences pour la voie juriste, rédigée avant les autres (même savoir-faire, autre titre).
EQ = {"Le brouillon d'abord": "Le contexte d'abord", "Ce qui manque": "Demander ce qui manque", "Documents d'entraînement": "Données fictives ou publiques",
      "Deux modes": "Recherche web activée", "Source primaire": "Remonter à la source", "Ouvrir les liens": "Remonter à la source",
      "Veille": "Veille récurrente", "Résumé fidèle": "Résumer pour quelqu'un", "Note interne": "Note de direction", "Grille de lecture": "Exiger les citations"}
LABEL = {"Note de direction": "Note orientée décision"}
FAM = [
 ("Rédiger", ["Le contexte d'abord", "Le plan avant le texte", "Le ton se règle", "Personnaliser sans recopier", "Note de direction", "Compte rendu", "Réponse à un courriel reçu", "Résumer pour quelqu'un", "Ce que l'assistant ne tranche pas", "Simplifier sans fausser"]),
 ("Vérifier", ["Relire comme l'auteur", "Exiger les citations", "La valeur « non mentionné »", "Demander ce qui manque", "Recouper au hasard", "Comparer deux versions", "Cohérence avec le business plan", "Questions d'un relecteur", "Repérer, pas trancher"]),
 ("Rechercher", ["Recherche web activée", "Remonter à la source", "Une liste à vérifier", "Dialoguer pour affiner", "Veille récurrente", "Recherche approfondie", "L'assistant prépare, la base répond", "Numéros à vérifier"]),
 ("Présenter", ["Trame de présentation", "Titres affirmatifs", "Contradicteur", "Visuels"]),
 ("Chiffres et tableaux", ["Les chiffres se recalculent", "Formules de tableur", "Analyser un tableau", "Commenter des chiffres", "Tableaux"]),
 ("Structurer", ["Structurer une procédure"]),
 ("Protéger", ["Données fictives ou publiques"]),
 ("Organiser", ["Projets et assistants personnalisés", "Instructions permanentes", "Documents de référence", "Mesurer", "Partager"]),
]
seen = {}   # notion -> profil -> [cotes]
steps = {}
for s in c['STEPS']:
  if s['voie'] != 'metier': continue
  steps.setdefault(s['profil'], []).append((s['cote'], s['titre']))
  for t, _ in s['notions']:
    k = EQ.get(t, t)
    l = seen.setdefault(k, {}).setdefault(s['profil'], [])
    if s['cote'] not in l: l.append(s['cote'])
known = {n for _, l in FAM for n in l}
missing = set(seen) - known
assert not missing, missing
rows = []
for fam, lst in FAM:
  items = [n for n in lst if n in seen]
  items.sort(key=lambda n: -len(seen[n]))
  rows.append((fam, items))
socle = [(s['cote'], s['titre']) for s in c['STEPS'] if s['voie'] == 'socle']
expert = [(s['cote'], s['titre']) for s in c['STEPS'] if s['voie'] == 'expert']
e = html.escape
n4 = sum(1 for n in seen if len(seen[n]) == 4); nspec = sum(1 for n in seen if len(seen[n]) == 1)

css = '''
@font-face{font-family:N;src:url(../../node_modules/@fontsource/nunito/files/nunito-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:N;src:url(../../node_modules/@fontsource/nunito/files/nunito-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:N;src:url(../../node_modules/@fontsource/nunito/files/nunito-latin-800-normal.woff2);font-weight:800}

*{box-sizing:border-box}
body{margin:0;font-family:N,"DejaVu Sans",sans-serif;color:#19171c;background:#f3f6f8}
.page{width:1587px;min-height:1122px;padding:44px 52px 40px;position:relative}
h1{margin:0;font-size:34px;font-weight:800;letter-spacing:-.01em}
.lead{margin:8px 0 0;font-size:16px;color:#56616a;max-width:1180px;line-height:1.45}
.cols{display:grid;grid-template-columns:330px 1fr;gap:28px;margin-top:26px}
.side{display:grid;gap:16px;align-content:start}
.box{background:#fff;border:1px solid #d5dee5;border-radius:10px;padding:16px 18px}
.box h2{margin:0 0 4px;font-size:15px;font-weight:800;color:#00698c}
.box p{margin:0 0 10px;font-size:13px;color:#56616a;line-height:1.4}
.box ol{margin:0;padding:0;list-style:none;display:grid;gap:3px;font-size:13px;line-height:1.35}
.box li span{display:inline-block;width:34px;font-weight:800;color:#00698c}
table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid #d5dee5;border-radius:10px;overflow:hidden;font-size:13.5px}
th,td{padding:5px 10px;border-bottom:1px solid #e9eef2;text-align:left;vertical-align:middle}
thead th{background:#e9eef2;font-size:13px;font-weight:800;vertical-align:top}
thead th small{display:block;font-weight:600;color:#56616a;font-size:11.5px;line-height:1.35;margin-top:4px}
td.c,th.c{text-align:center;width:150px}
tr.fam td{background:#f7f9fb;font-weight:800;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#00698c;padding-top:9px}
.dot{display:inline-block;min-width:38px;padding:2px 8px;border-radius:99px;background:#0084af;color:#fff;font-weight:800;font-size:12px}
.dot.one{background:#fed442;color:#19171c}
.n{font-weight:600}
.cnt{font-size:12px;color:#56616a;text-align:center}
.legend{display:flex;gap:22px;align-items:center;margin-top:14px;font-size:13px;color:#56616a}
.foot{margin-top:16px;font-size:12px;color:#56616a;line-height:1.45;max-width:1180px}
.band{position:absolute;left:0;right:0;bottom:0;height:10px;background:#fed442}
'''
def th(pid, nom):
  st = ''.join(f'{e(cote)} {e(t)}<br>' for cote, t in steps[pid])
  return f'<th class="c">{e(nom)}<small>{st}</small></th>'
body = []
for fam, items in rows:
  if not items: continue
  body.append(f'<tr class="fam"><td colspan="6">{e(fam)}</td></tr>')
  for n in items:
    cells = ''
    k = len(seen[n])
    for pid, _ in P:
      v = seen[n].get(pid)
      cells += f'<td class="c">{"<span class=\"dot" + (" one" if k == 1 else "") + "\">" + e(" ".join(v)) + "</span>" if v else ""}</td>'
    body.append(f'<tr><td class="n">{e(LABEL.get(n, n))}</td>{cells}<td class="cnt">{k} sur 4</td></tr>')
page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="page">
<h1>Parcours IA : notions vues dans chaque voie Métier</h1>
<p class="lead">La voie Métier n'enseigne pas le métier : elle montre comment utiliser l'IA dans ses tâches courantes. Le tableau indique, pour chaque savoir-faire, les métiers et les étapes où il est vu. Première version établie sans recueil des besoins de chaque métier ; à faire valider par un représentant de chaque métier et à compléter par mises à jour.</p>
<div class="cols"><div class="side">
<div class="box"><h2>Socle, commun à tous</h2><p>Dix étapes suivies quel que soit le métier. Les exemples s'adaptent au métier choisi.</p><ol>{''.join(f'<li><span>{e(a)}</span>{e(b)}</li>' for a,b in socle)}</ol></div>
<div class="box"><h2>Expert, commun à tous</h2><p>Neuf étapes facultatives, en partie au-delà de la pratique autorisée au poste.</p><ol>{''.join(f'<li><span>{e(a)}</span>{e(b)}</li>' for a,b in expert)}</ol></div>
</div><div>
<table><thead><tr><th>Savoir-faire IA de la voie Métier</th>{''.join(th(p, n) for p, n in P)}<th class="c" style="width:80px">Métiers</th></tr></thead><tbody>{''.join(body)}</tbody></table>
<div class="legend"><span><span class="dot">M1</span> vu dans plusieurs métiers, à l'étape indiquée</span><span><span class="dot one">M2</span> propre à un seul métier</span><span>{n4} savoir-faire communs aux quatre métiers, {nspec} propres à un seul</span></div>
<p class="foot">Source : contenu de l'application Parcours IA (version du 26/11/2026, dépôt PARCOURS-IA). Les notions de la voie juriste, rédigées en premier, sont rattachées au savoir-faire équivalent des autres voies quand elles portent le même enseignement sous un autre titre. Exercices pratiqués sur des données fictives ou publiques.</p>
</div></div><div class="band"></div></div></body></html>'''
open(__import__('os').path.join(__import__('os').path.dirname(__file__), 'schema.html'), 'w').write(page)
print(len(seen), 'savoir-faire ;', n4, 'communs aux 4 ;', nspec, 'propres à un seul')
