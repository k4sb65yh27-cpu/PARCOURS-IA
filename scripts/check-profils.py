# Contrôle : termes juridiques visibles par profil, après application des variantes.
# Usage : python3 scripts/check-profils.py
import json, re, copy
c = json.load(open('src/data/content.json'))
T = re.compile(r"juriste|contrat|clause|cassation|\barrêt\b|jurisprudence|Légifrance|Judilibre|\bNDA\b|avocat|juridique|tribunal|code civil|\bCPI\b|pourvoi", re.I)
def setp(o, path, v):
  ks = path.split('.')
  for k in ks[:-1]: o = o[int(k)] if isinstance(o, list) else o[k]
  if isinstance(o, list): o[int(ks[-1])] = v
  else: o[ks[-1]] = v
for p in [x['id'] for x in c['PROFILS']]:
  tot = 0; det = []
  for s in c['STEPS']:
    if s['voie'] == 'metier' and s.get('profil') != p: continue
    s2 = copy.deepcopy(s)
    for path, v in s.get('pv', {}).get(p, {}).items(): setp(s2, path, v)
    txt = json.dumps({k: s2[k] for k in ('titre', 'obj', 'notions', 'ex', 'quiz', 'drills')}, ensure_ascii=False)
    n = len(T.findall(txt)); tot += n
    if n: det.append(f"{s['cote']}:{n}")
  d = 0
  for x in c['DEFIS']:
    x2 = {**x, **x.get('pv', {}).get(p, {})}; x2.pop('pv', None)
    d += len(T.findall(json.dumps(x2, ensure_ascii=False)))
  print(f"{p:8} étapes {tot:3}  défis {d:2}  ", ' '.join(det))
