import json, sys
sys.path.insert(0, '.')
from socle import SOCLE
from socle_plus import SOCLE_PLUS
from glossaire import GLOSS, THEMES
import revisions
from metier import METIER
from metier_profils import METIER_PROFILS
from profils import PROFILS, OV, DEFI_OV
from extra import *
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = '../../src/data/content.json'
# Contenu source figé avant les profils (étapes Expert et bonus, glossaire, sources) : relancer sans perdre le texte d'origine.
old = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'source_v2.json'))
B = {s['id']: s for s in old['STEPS']}
SRC = old['SRC']
SRC.update({
 "elements": {"n": "Elements of AI (en français)", "u": "https://www.elementsofai.fr/"},
 "cnil": {"n": "CNIL, intelligence artificielle", "u": "https://www.cnil.fr/fr/intelligence-artificielle"},
 "aiact": {"n": "AI Act, règlement (UE) 2024/1689 sur EUR-Lex", "u": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"},
 "promptdoc": {"n": "Anthropic, guide de rédaction des consignes", "u": "https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview"},
 "oaiacad": {"n": "OpenAI Academy", "u": "https://academy.openai.com/"},
 "judilibre": {"n": "Judilibre, Cour de cassation", "u": "https://www.courdecassation.fr/acces-rapide-judilibre"},
 "omnibus": {"n": "Commission européenne, entrée en vigueur de l'omnibus IA", "u": "https://digital-strategy.ec.europa.eu/fr/news/ai-omnibus-enters-force"},
 "espacenet": {"n": "Espacenet, Office européen des brevets", "u": "https://worldwide.espacenet.com/"},
 "oeb": {"n": "Office européen des brevets (OEB)", "u": "https://www.epo.org/fr"},
 "inpi": {"n": "INPI", "u": "https://www.inpi.fr/"},
 "insee": {"n": "INSEE", "u": "https://www.insee.fr/"},
 "hal": {"n": "HAL, archive ouverte", "u": "https://hal.science/"},
})
BLOC_S = {1: "Socle : prise en main", 5: "Socle : au quotidien", 9: "Socle : autonomie"}
steps = []
bloc = None
for i, s in enumerate(SOCLE + SOCLE_PLUS, 1):
  bloc = BLOC_S.get(i, bloc)
  steps.append({**s, "bloc": bloc, "voie": "socle"})
# Voie Métier : une série de cinq étapes par profil. Le juriste garde me1 à me5 (progressions conservées).
PBLOC = {p["id"]: p["bloc"] for p in PROFILS}
for s in METIER:
  steps.append({**s, "bloc": PBLOC["juriste"], "voie": "metier", "profil": "juriste"})
for pid, lst in METIER_PROFILS.items():
  for s in lst:
    steps.append({**s, "bloc": PBLOC[pid], "voie": "metier", "profil": pid})
for sid, cote, bl, cadre, comp in EXPERT_MAP:
  s = dict(XC) if sid == "xc" else dict(B[sid])
  s.update(cote=cote, bloc=bl, cadre=cadre, comp=comp, voie="bonus" if sid == "bonus" else "expert")
  steps.append(s)
# Notion de compte personnel reprise de l'ancienne étape 00.
e2 = next(s for s in steps if s['id'] == 's7')
if not any(n[0] == 'Compte personnel' for n in e2['notions']):
  e2['notions'].insert(0, ["Compte personnel", "Les étapes en cadre API se font avec un compte personnel (console du fournisseur, notebook Colab, GitHub), jamais avec un compte ou des données de l'entreprise."])
from fixes import FIX
for s in steps:
  for qi,q in enumerate(s['quiz']):
    if (s['id'],qi) in FIX:
      j,t=FIX[(s['id'],qi)]; assert j!=q['a']; q['o'][j]=t
# Neutralisation et variantes par profil (après FIX : les leurres corrigés font partie du texte d'origine).
PIDS = [p["id"] for p in PROFILS]
def getp(o, path):
  for k in path.split('.'): o = o[int(k)] if isinstance(o, list) else o[k]
  return o
def setp(o, path, v):
  ks = path.split('.')
  for k in ks[:-1]: o = o[int(k)] if isinstance(o, list) else o[k]
  last = ks[-1]
  if isinstance(o, list): o[int(last)] = v
  else: o[last] = v
BYID_ = {s['id']: s for s in steps}
for sid, paths in OV.items():
  s = BYID_[sid]
  pv = {}
  for path, var in paths.items():
    orig = json.loads(json.dumps(getp(s, path)))
    base = var["base"]
    if isinstance(base, dict) and isinstance(orig, dict) and path.startswith("ex."): base = {**orig, **base}
    setp(s, path, base)
    for p in PIDS:
      v = var.get(p, base) if (p != "juriste" or "juriste" in var) else orig
      if v is None: v = orig
      if isinstance(v, dict) and isinstance(orig, dict) and path.startswith("ex."): v = {**orig, **v}
      if v != base: pv.setdefault(p, {})[path] = v
  if pv: s["pv"] = pv
DBY = {d['id']: d for d in DEFIS}
for did, var in DEFI_OV.items():
  d = DBY[did]
  orig = {k: d[k] for k in d}
  base = {**orig, **var["base"]}
  d.update(base)
  pv = {}
  for p in PIDS:
    v = var.get(p, var["base"]) if (p != "juriste" or "juriste" in var) else orig
    if v is None: v = orig
    full = {**orig, **v}
    diff = {k: full[k] for k in full if full[k] != base.get(k)}
    if diff: pv[p] = diff
  if pv: d["pv"] = pv
# Révisions du 27/11/2026 : skills, étiquettes retirées, défis et exercices facultatifs.
revisions.apply(steps, DEFIS, NEWS, SRC, PIDS)
assert {x['step'] for x in GLOSS if x['step']} <= {s['id'] for s in steps}
used = {k for s in steps for k, _ in s['res']}
missing = used - SRC.keys()
assert not missing, missing
# Biais de longueur sur le contenu neuf
def quizzes(s):
  yield from s['quiz']
  for p, m in s.get('pv', {}).items():
    for path, v in m.items():
      if path.startswith('quiz.'): yield v
NEUF = lambda s: s['voie'] in ('socle','metier') or s['id']=='xc'
bias = [(s['id'], q['q'][:50]) for s in steps if NEUF(s) for q in quizzes(s)
        if all(len(q['o'][q['a']]) > len(o) for j, o in enumerate(q['o']) if j != q['a'])]
biasx = [(s['id'], q['q'][:50]) for s in steps if not NEUF(s) for q in quizzes(s)
        if all(len(q['o'][q['a']]) > len(o) for j, o in enumerate(q['o']) if j != q['a'])]
out = {"SRC": SRC, "STEPS": steps, "GLOSS": GLOSS, "GLOSS_THEMES": THEMES, "COMPS": COMPS, "LEVELS": LEVELS, "VOIES": VOIES,
       "CADRES": CADRES, "CADRE_NOTE": CADRE_NOTE, "DEFIS": DEFIS, "NEWS": NEWS, "PROFILS": PROFILS}
json.dump(out, open(P, 'w'), ensure_ascii=False, indent=1)
print(len(steps), 'étapes ; biais longueur (contenu neuf, variantes comprises) :', len(bias), 'sur', sum(1 for s in steps if NEUF(s) for _ in quizzes(s)))
for b in bias: print(' ', b)
print('biais longueur (Expert et bonus, variantes comprises) :', len(biasx), 'sur', sum(1 for s in steps if not NEUF(s) for _ in quizzes(s)))
