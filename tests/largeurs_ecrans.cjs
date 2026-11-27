// Captures des écrans principaux aux largeurs bureau (Réviser, Glossaire, Profil, tiroir d'un nœud, notions).
// Usage : node tests/largeurs_ecrans.cjs <dossier> <url> <largeur> <light|dark>
const { chromium } = require('playwright');
const prep = require('./prep_juriste.cjs');
const [out, url, w, scheme] = [process.argv[2], process.argv[3], +process.argv[4], process.argv[5] || 'light'];
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: w, height: 900 }, colorScheme: scheme });
  const p = await ctx.newPage(); const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push(String(e)));
  await p.goto(url); await p.waitForTimeout(1000); await prep(p);
  const nav = () => p.getByRole('navigation', { name: 'Navigation principale' });
  const shot = async (n) => { await p.waitForTimeout(600); const sw = await p.evaluate(() => document.documentElement.scrollWidth); if (sw > w) errs.push(`débordement ${n}: ${sw}`); await p.screenshot({ path: `${out}/${w}_${scheme}_${n}.png` }); };
  for (const [t, n] of [['Réviser', 'reviser'], ['Glossaire', 'glossaire'], ['Profil', 'profil']]) { await nav().getByRole('button', { name: new RegExp('^' + t) }).click(); await shot(n); }
  await p.getByRole('textbox').first().isVisible().catch(() => {});
  await nav().getByRole('button', { name: /^Glossaire/ }).click(); await p.waitForTimeout(400);
  await p.getByRole('button', { name: /Token/ }).first().click(); await shot('glossaire_ouvert');
  await nav().getByRole('button', { name: /^Parcours/ }).click(); await p.waitForTimeout(500);
  await p.getByRole('button', { name: /Notions/ }).first().click(); await shot('tiroir');
  await p.keyboard.press('Escape'); await p.waitForTimeout(400);
  console.log(w, scheme, 'erreurs :', JSON.stringify(errs));
  await b.close();
})();
