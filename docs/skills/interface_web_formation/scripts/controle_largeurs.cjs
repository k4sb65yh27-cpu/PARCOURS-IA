// Contrôle de mise en page d'une interface web à plusieurs largeurs, en clair et en sombre.
// Usage : node controle_largeurs.cjs <url> <dossier_captures> [--largeurs 375,768,1024,1440] [--prep module.cjs]
// Le module --prep exporte une fonction async (page) qui amène l'application à l'écran à contrôler
// (accueil, choix d'un profil...). Mesures par capture :
//   - débordement : largeur de défilement supérieure à la fenêtre ;
//   - couverture : part de la largeur de la fenêtre occupée par du contenu visible dans le premier écran
//     (texte, image, SVG, champ, fond ou bordure visible ; les éléments pleine largeur sont exclus) ;
//   - cibles : éléments cliquables de moins de 44 px de côté (à 375 px seulement) ;
//   - erreurs : erreurs de console et exceptions de page.
// Ce sont des signaux à confirmer sur la capture, pas un verdict.
const { chromium } = require('playwright');
const path = require('path');

const args = process.argv.slice(2);
const url = args[0], out = args[1];
const opt = (k, d) => { const i = args.indexOf(k); return i > -1 ? args[i + 1] : d; };
const widths = opt('--largeurs', '375,768,1024,1440').split(',').map(Number);
const prep = opt('--prep', '') ? require(path.resolve(opt('--prep', ''))) : null;

function mesurer() {
  const vw = innerWidth, vh = innerHeight, iv = [];
  const visible = (el, cs) => {
    if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) return false;
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    const media = /^(IMG|SVG|CANVAS|VIDEO|INPUT|TEXTAREA|SELECT)$/i.test(el.tagName);
    const bg = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
    const bd = parseFloat(cs.borderTopWidth) + parseFloat(cs.borderLeftWidth) > 0 && cs.borderTopColor !== 'rgba(0, 0, 0, 0)';
    return hasText || media || bg || bd;
  };
  for (const el of document.body.querySelectorAll('*')) {
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2 || r.bottom < 0 || r.top > vh || r.width >= vw * 0.95) continue;
    if (!visible(el, getComputedStyle(el))) continue;
    iv.push([Math.max(0, r.left), Math.min(vw, r.right)]);
  }
  iv.sort((a, b) => a[0] - b[0]);
  let tot = 0, cur = null;
  for (const [a, b] of iv) { if (!cur || a > cur[1]) { if (cur) tot += cur[1] - cur[0]; cur = [a, b]; } else cur[1] = Math.max(cur[1], b); }
  if (cur) tot += cur[1] - cur[0];
  const petites = vw <= 400 ? [...document.querySelectorAll('button, a[href], [role=button], input, select')]
    .filter(e => { const r = e.getBoundingClientRect(); return r.width && r.height && (r.width < 44 || r.height < 44) && getComputedStyle(e).visibility !== 'hidden'; }).length : null;
  return { debord: document.documentElement.scrollWidth > vw ? document.documentElement.scrollWidth : 0, couverture: Math.round(100 * tot / vw), petites };
}

(async () => {
  const b = await chromium.launch();
  const res = [];
  for (const scheme of ['light', 'dark']) for (const w of widths) {
    const ctx = await b.newContext({ viewport: { width: w, height: w < 600 ? 812 : 900 }, colorScheme: scheme, hasTouch: w < 1024 });
    const p = await ctx.newPage(); const errs = [];
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto(url); await p.waitForTimeout(1000);
    if (prep) await prep(p);
    await p.waitForTimeout(600);
    const m = await p.evaluate(mesurer);
    await p.screenshot({ path: `${out}/${w}_${scheme}.png` });
    res.push({ largeur: w, theme: scheme, ...m, erreurs: errs.length });
    await ctx.close();
  }
  await b.close();
  console.table(res);
})();
