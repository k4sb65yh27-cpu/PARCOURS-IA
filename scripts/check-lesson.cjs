// shortcut: utilise le Playwright installé sur la machine (pas de dépendance du projet) ; à passer en @playwright/test si une CI doit le lancer.
// Usage : npx vite preview, puis node scripts/check-lesson.cjs <dossier_captures> http://localhost:4173/ src/data/content.json
// Leçon réussie sans faute : vérifie le parcours heureux (confettis, série, fin de leçon).
const { chromium } = require('playwright');
const fs = require('fs');
const out = process.argv[2], url = process.argv[3], content = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));
const items = [];
for (const s of content.STEPS) { s.quiz.forEach(q => items.push({ ...q, type: 'mcq' })); s.drills.forEach(d => items.push(d)); }
const find = (q) => items.find(i => i.q === q);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 375, height: 812 } });
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  await p.goto(url); await p.waitForTimeout(1000);
  await p.getByRole('button', { name: /^Leçon/ }).first().click();
  await p.waitForTimeout(400);
  await p.getByRole('button', { name: /^Commencer$/ }).click();
  await p.waitForTimeout(600);
  const S = 'div.z-40 main';
  for (let k = 0; k < 15; k++) {
    const q = (await p.locator(`${S} h2`).first().innerText()).trim();
    let it = find(q) || items.find(i => i.type === 'cloze' && q.startsWith(i.q.split(/_{2,}/)[0].trim()));
    if (!it) { errs.push('introuvable: ' + q); break; }
    const btn = (t) => p.locator(`${S} button`, { hasText: t }).first();
    if (it.type === 'tf') await btn(it.a ? 'Vrai' : 'Faux').click();
    else if (it.type === 'mcq' || it.type === 'cloze') await btn(it.o[it.a]).click();
    else if (it.type === 'order') { for (const t of it.items) { await p.locator('[aria-label="Éléments à placer"] button', { hasText: t }).first().click(); await p.waitForTimeout(120); } }
    else if (it.type === 'match') { for (const [l, r] of it.pairs) { await btn(l).click(); await btn(r).click(); } }
    if (k === 3) await p.screenshot({ path: `${out}/win_q.png` });
    await p.getByRole('button', { name: 'Vérifier', exact: true }).click();
    await p.waitForTimeout(350);
    if (k === 4) await p.screenshot({ path: `${out}/win_combo.png` });
    await p.getByRole('button', { name: 'Continuer', exact: true }).click();
    await p.waitForTimeout(450);
    if (await p.getByText('Leçon terminée').count()) break;
  }
  await p.waitForTimeout(700);
  await p.screenshot({ path: `${out}/win_end_confetti.png` });
  await p.waitForTimeout(1600);
  await p.screenshot({ path: `${out}/win_end.png` });
  console.log(JSON.stringify(errs));
  await b.close();
})();
