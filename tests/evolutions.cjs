// Évolutions du 27/11/2026 : progression antérieure conservée, avis « Nouveautés », leçon S11 sans faute, glossaire.
// Usage : npx vite preview, puis node tests/evolutions.cjs <dossier> http://localhost:4173/ light|dark <profil>
const { chromium } = require('playwright');
const fs = require('fs');
const [out, url, theme = 'light', profil = 'juriste', cible = 'so11'] = process.argv.slice(2);
// cible so12 : S11 déjà validée, l'avis Nouveautés ne s'affiche plus et S12 devient l'étape courante.
const content = JSON.parse(fs.readFileSync('src/data/content.json', 'utf8'));
const items = [];
for (const s of content.STEPS) {
  s.quiz.forEach(q => items.push({ ...q, type: 'mcq' })); s.drills.forEach(d => items.push(d));
  for (const m of Object.values(s.pv || {})) for (const [k, v] of Object.entries(m)) {
    if (k.startsWith('quiz.')) items.push({ ...v, type: 'mcq' }); else if (k.startsWith('drills.')) items.push(v);
  }
}
const find = (q) => items.find(i => i.q === q) || items.find(i => i.type === 'cloze' && q.startsWith(i.q.split(/_{2,}/)[0].trim()));
// Progression d'avant l'ajout : S1 à S10 validées (examen réussi, exercices faits).
const day = new Date().toISOString().slice(0, 10);
const steps = {};
for (const s of content.STEPS.filter(s => s.voie === 'socle' && s.id !== 'so12' && (cible === 'so12' || s.id !== 'so11')))
  steps[s.id] = { ex: Object.fromEntries(s.ex.map((_, i) => [i, true])), best: 100, passed: true, date: day, lessons: 2, xpEx: {}, perfect: false, val: true, notions: true };
const root = { state: { updatedAt: 1, xp: 2400, streak: { count: 1, lastDay: day }, daily: { day, xp: 0, goal: 20 }, steps, srs: {}, free: false, settings: { sound: false, haptics: false, cadre: 1, outil: 'Claude', profil }, defis: {} }, notes: {}, answers: {}, plan: null, journal: null, tutor: null };
const res = { profil, theme, errs: [] };
const check = (name, ok) => { res[name] = ok; if (!ok) res.errs.push('échec : ' + name); };
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 375, height: 812 }, colorScheme: theme, deviceScaleFactor: 1 });
  await ctx.addInitScript(([k, v]) => { if (!localStorage.getItem('seeded')) { localStorage.setItem(k, v); localStorage.setItem('seeded', '1'); } }, ['parcours-ia-juriste-v2', JSON.stringify(root)]);
  const p = await ctx.newPage();
  p.on('pageerror', e => res.errs.push(String(e)));
  await p.goto(url); await p.waitForTimeout(1200);
  const scrollX = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  check('pas_de_defilement_horizontal_parcours', !scrollX);
  // Avis Nouveautés
  const nv = p.getByRole('region', { name: 'Nouveautés' });
  check('avis_nouveautes_attendu', await nv.count() === (cible === 'so11' ? 1 : 0));
  await p.evaluate(() => window.scrollTo(0, 0));
  await p.screenshot({ path: `${out}/nouveautes_${cible}_${profil}_${theme}.png` });
  // Étape courante : S11
  const cur = p.getByRole('button', { name: /à faire maintenant/ }).first();
  await cur.scrollIntoViewIfNeeded();
  await p.screenshot({ path: `${out}/s11_courante_${cible}_${profil}_${theme}.png` });
  const before = await p.evaluate(() => JSON.parse(localStorage.getItem('parcours-ia-juriste-v2')).state.steps);
  check('progression_conservee', ['so1', 'so5', 'so10'].every(k => before[k]?.passed));
  if (cible === 'so11') await nv.getByRole('button', { name: 'Compris' }).click();
  await p.reload(); await p.waitForTimeout(1000);
  check('avis_masque_apres_compris', await p.getByRole('region', { name: 'Nouveautés' }).count() === 0);
  // Leçon S11 : notions puis leçon, réponses justes
  await p.getByRole('button', { name: /Notions, à faire maintenant/ }).first().click().catch(() => {});
  await p.waitForTimeout(500);
  const lire = p.getByRole('button', { name: /Lire les notions/ });
  if (await lire.count()) {
    await lire.click();
    for (let i = 0; i < 10; i++) { const f = p.getByRole('button', { name: "J'ai compris" }); if (await f.count()) { await f.click(); break; } await p.getByRole('button', { name: 'Suivante' }).click(); await p.waitForTimeout(250); }
    await p.waitForTimeout(800);
  }
  const titreNotions = await p.evaluate((c) => JSON.parse(localStorage.getItem('parcours-ia-juriste-v2')).state.steps[c]?.notions, cible);
  check('notions_s11_lues', !!titreNotions);
  await p.getByRole('button', { name: /Leçon, à faire maintenant/ }).first().click();
  await p.waitForTimeout(400);
  await p.getByRole('button', { name: /^Commencer$/ }).click();
  await p.waitForTimeout(600);
  const S = 'div.z-40 main';
  for (let k = 0; k < 15; k++) {
    const q = (await p.locator(`${S} h2`).first().innerText()).trim();
    const it = find(q);
    if (!it) { res.errs.push('introuvable : ' + q); break; }
    const btn = (t) => p.locator(`${S} button`, { hasText: t }).first();
    if (it.type === 'tf') await btn(it.a ? 'Vrai' : 'Faux').click();
    else if (it.type === 'mcq' || it.type === 'cloze') await btn(it.o[it.a]).click();
    else if (it.type === 'order') { for (const t of it.items) { await p.locator('[aria-label="Éléments à placer"] button', { hasText: t }).first().click(); await p.waitForTimeout(100); } }
    else if (it.type === 'match') { for (const [l, r] of it.pairs) { await btn(l).click(); await btn(r).click(); } }
    if (k === 1) await p.screenshot({ path: `${out}/s11_question_${cible}_${profil}_${theme}.png` });
    await p.getByRole('button', { name: 'Vérifier', exact: true }).click();
    await p.waitForTimeout(300);
    await p.getByRole('button', { name: 'Continuer', exact: true }).click();
    await p.waitForTimeout(400);
    if (await p.getByText('Leçon terminée').count()) break;
  }
  check('lecon_s11_terminee', await p.getByText('Leçon terminée').count() > 0);
  const so11 = await p.evaluate((c) => JSON.parse(localStorage.getItem('parcours-ia-juriste-v2')).state.steps[c], cible);
  check('lecon_s11_comptee', (so11?.lessons || 0) >= 1);
  await p.keyboard.press('Escape'); await p.waitForTimeout(400);
  const fermer = p.getByRole('button', { name: /^(Continuer|Fermer|Terminer)$/ });
  if (await fermer.count()) { await fermer.first().click(); await p.waitForTimeout(400); }
  // Glossaire
  await p.getByRole('navigation').getByRole('button', { name: 'Glossaire' }).click();
  await p.waitForTimeout(500);
  check('glossaire_69_termes', await p.getByText('69 termes', { exact: false }).count() > 0);
  check('glossaire_sans_defilement_horizontal', !(await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)));
  await p.screenshot({ path: `${out}/glossaire_${cible}_${profil}_${theme}.png` });
  await p.getByLabel('Rechercher').fill('tokens');
  await p.waitForTimeout(250);
  const n = await p.locator('main li, li').filter({ has: p.locator('button[aria-expanded]') }).count();
  check('recherche_filtre', n > 0 && n < 69);
  await p.getByLabel('Rechercher').fill('');
  await p.getByRole('button', { name: 'Tokens et limites', exact: true }).click();
  await p.waitForTimeout(250);
  const n2 = await p.locator('li').filter({ has: p.locator('button[aria-expanded]') }).count();
  check('filtre_theme_6', n2 === 6);
  await p.getByRole('button', { name: 'Tous', exact: true }).click();
  await p.getByLabel('Rechercher').fill('Skill');
  await p.getByRole('button', { name: /^Skill/ }).first().click();
  await p.waitForTimeout(300);
  check('regle_skills_affichee', await p.getByText("l'aval du RSI ou du référent IA", { exact: false }).count() > 0);
  await p.screenshot({ path: `${out}/glossaire_skill_${cible}_${profil}_${theme}.png` });
  await p.getByRole('button', { name: /^Voir l'étape/ }).first().click();
  await p.waitForTimeout(600);
  check('lien_vers_etape', await p.getByText('E5', { exact: false }).count() > 0);
  await b.close();
  console.log(JSON.stringify(res));
})();
