import json, sys
sys.path.insert(0, '.')
from socle import SOCLE
from metier import METIER
from extra import *
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = '../../src/data/content.json'
old = json.load(open(sys.argv[1] if len(sys.argv) > 1 else P))
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
})
BLOC_S = {1: "Socle : prise en main", 5: "Socle : au quotidien", 9: "Socle : autonomie"}
steps = []
bloc = None
for i, s in enumerate(SOCLE, 1):
  bloc = BLOC_S.get(i, bloc)
  steps.append({**s, "bloc": bloc, "voie": "socle"})
for s in METIER:
  steps.append({**s, "bloc": "Métier : juriste SATT", "voie": "metier"})
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
used = {k for s in steps for k, _ in s['res']}
missing = used - SRC.keys()
assert not missing, missing
# Biais de longueur sur le contenu neuf
bias = [(s['id'], q['q'][:50]) for s in steps if s['voie'] in ('socle','metier') or s['id']=='xc' for q in s['quiz']
        if all(len(q['o'][q['a']]) > len(o) for j, o in enumerate(q['o']) if j != q['a'])]
out = {"SRC": SRC, "STEPS": steps, "GLOSS": old['GLOSS'], "COMPS": COMPS, "LEVELS": LEVELS, "VOIES": VOIES,
       "CADRES": CADRES, "CADRE_NOTE": CADRE_NOTE, "DEFIS": DEFIS, "NEWS": NEWS}
json.dump(out, open(P, 'w'), ensure_ascii=False, indent=1)
print(len(steps), 'étapes ; biais longueur (contenu neuf) :', len(bias), 'sur', sum(len(s['quiz']) for s in steps if s['voie'] in ('socle','metier') or s['id']=='xc'))
for b in bias: print(' ', b)
