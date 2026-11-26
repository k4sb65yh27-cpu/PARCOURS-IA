// Contrôle des profils métier, de la confirmation de sortie et de la mascotte des exercices, à 375 px.
// Usage : npx vite preview, puis node tests/profils.cjs <dossier_captures> http://localhost:4173/ <light|dark>
// shortcut : Playwright de la machine, pas de dépendance du projet.
const { chromium } = require('playwright');
const fs = require('fs');
const out = process.argv[2], url = process.argv[3], scheme = process.argv[4] || 'light';
const content = JSON.parse(fs.readFileSync('src/data/content.json', 'utf8'));
const items = [];
for (const s of content.STEPS) {
  const add = (x, t) => items.push({ ...x, type: t || x.type, step: s.id });
  s.quiz.forEach((q) => add(q, 'mcq')); s.drills.forEach((d) => add(d));
  for (const m of Object.values(s.pv || {})) for (const [k, v] of Object.entries(m)) {
    if (k.startsWith('quiz.')) add(v, 'mcq'); else if (k.startsWith('drills.')) add(v);
  }
}
const find = (q) => items.find((i) => i.q === q) || items.find((i) => i.type === 'cloze' && q.startsWith(i.q.split(/_{2,}/)[0].trim()));
const S = 'div.z-40 main';
const fails = [], errs = [];
const ok = (c, msg) => { if (!c) fails.push(msg); };

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 375, height: 812 }, colorScheme: scheme, deviceScaleFactor: 2 });
  const p = await ctx.newPage();
  p.on('pageerror', (e) => errs.push(String(e)));
  const snap = async (n) => {
    await p.waitForTimeout(450);
    const w = await p.evaluate(() => document.documentElement.scrollWidth);
    ok(w <= 375, `${n} : débordement horizontal (${w} px)`);
    await p.screenshot({ path: `${out}/${scheme}_${n}.png` });
  };
  const inSession = async () => (await p.locator('div.z-40').count()) > 0;
  const dialog = () => p.getByRole('dialog');
  const question = async () => (await p.locator(`${S} h2`).first().innerText()).trim();
  const answer = async (good) => {
    const it = find(await question());
    if (!it) { fails.push('question introuvable : ' + (await question())); return null; }
    const btn = (t) => p.locator(`${S} button`, { hasText: t }).first();
    if (it.type === 'tf') await btn((it.a === good) ? 'Vrai' : 'Faux').click();
    else if (it.type === 'mcq' || it.type === 'cloze') await btn(it.o[good ? it.a : (it.a + 1) % it.o.length]).click();
    else if (it.type === 'order') { const seq = good ? it.items : [...it.items].reverse(); for (const t of seq) { await p.locator('[aria-label="Éléments à placer"] button', { hasText: t }).first().click(); await p.waitForTimeout(100); } }
    else if (it.type === 'match') { const n = it.pairs.length; for (let i = 0; i < n; i++) { await btn(it.pairs[i][0]).click(); await btn(it.pairs[good ? i : (i + 1) % n][1]).click(); } }
    return it;
  };
  const verify = async () => { await p.getByRole('button', { name: 'Vérifier', exact: true }).click(); await p.waitForTimeout(400); };
  const cont = async () => { await p.getByRole('button', { name: 'Continuer', exact: true }).click(); await p.waitForTimeout(450); };
  const startLesson = async (scope) => {
    await (scope || p).getByRole('button', { name: /^Leçon/ }).first().click();
    await p.waitForTimeout(400);
    await p.getByRole('button', { name: /^Commencer$/ }).click();
    await p.waitForTimeout(600);
  };

  // 1. Premier lancement
  await p.goto(url); await p.waitForTimeout(1200);
  ok(await p.getByRole('radiogroup', { name: 'Votre métier' }).count(), 'écran d’ouverture absent');
  ok(await p.getByRole('button', { name: 'Continuer', exact: true }).isDisabled(), 'Continuer actif sans métier choisi');
  await snap('p01_ouverture');
  await p.getByRole('radio', { name: /Chargé de transfert/ }).click();
  await snap('p02_ouverture_choix');
  await p.getByRole('button', { name: 'Continuer', exact: true }).click(); await p.waitForTimeout(400);
  await p.getByRole('radio', { name: 'Claude', exact: true }).click();
  await snap('p03_ouverture_assistant');
  await p.getByRole('button', { name: 'Commencer', exact: true }).click(); await p.waitForTimeout(700);
  ok(!(await p.getByRole('radiogroup', { name: 'Votre métier' }).count()), 'écran d’ouverture toujours affiché');
  await snap('p04_accueil');

  // 2. Sortie sans réponse : pas de confirmation
  await startLesson();
  await p.getByRole('button', { name: 'Quitter la séance' }).click(); await p.waitForTimeout(500);
  ok(!(await inSession()) && !(await dialog().count()), 'sortie sans réponse : la séance devrait se fermer directement');

  // 3. Mascotte et erreur
  await startLesson();
  ok(await p.locator(`${S} .bubble`).count(), 'bulle de la mascotte absente');
  await snap('p05_question_mascotte');
  await answer(false); await verify();
  ok(/1 vies|4 vies/.test(await p.locator('[aria-label$="vies"]').getAttribute('aria-label')), 'compteur de vies');
  await snap('p06_erreur_mascotte');
  await cont();

  // 4. Confirmation par la croix, Échap et le retour du navigateur
  await p.getByRole('button', { name: 'Quitter la séance' }).click(); await p.waitForTimeout(500);
  ok(await dialog().count(), 'croix : confirmation absente');
  await snap('p07_confirmation');
  await p.getByRole('button', { name: 'Continuer la leçon' }).click(); await p.waitForTimeout(1200);
  ok(!(await dialog().count()) && (await inSession()), 'Continuer la leçon : la séance devrait reprendre');
  await p.keyboard.press('Escape'); await p.waitForTimeout(500);
  ok(await dialog().count(), 'Échap : confirmation absente');
  await p.getByRole('button', { name: 'Continuer la leçon' }).click(); await p.waitForTimeout(500);
  await p.goBack(); await p.waitForTimeout(600);
  ok((await dialog().count()) && (await inSession()), 'retour : confirmation absente ou séance fermée');
  await snap('p08_confirmation_retour');
  await p.getByRole('button', { name: 'Continuer la leçon' }).click(); await p.waitForTimeout(500);

  // 5. Dernière vie : mascotte inquiète
  for (let i = 0; i < 3; i++) { await answer(false); await verify(); await cont(); }
  ok((await p.locator('[aria-label="1 vies"]').count()) > 0, 'dernière vie non atteinte');
  ok(/Dernière vie/.test(await p.locator(`${S} .bubble`).innerText()), 'bulle de dernière vie absente');
  await snap('p09_derniere_vie');
  await p.getByRole('button', { name: 'Quitter la séance' }).click(); await p.waitForTimeout(400);
  await p.getByRole('button', { name: 'Quitter', exact: true }).click(); await p.waitForTimeout(700);
  ok(!(await inSession()), 'Quitter : la séance devrait se fermer');
  // Le retour suivant ne doit pas rouvrir ni bloquer.
  ok(!(await dialog().count()), 'feuille restée ouverte après Quitter');

  // 6. Voie Métier du chargé de transfert (mode libre)
  await p.getByRole('navigation').getByRole('button', { name: 'Profil' }).click(); await p.waitForTimeout(400);
  await p.locator('[id="t-Mode libre"]').click(); await p.waitForTimeout(300);
  await p.getByRole('navigation').getByRole('button', { name: 'Parcours' }).click(); await p.waitForTimeout(500);
  const h = p.getByRole('heading', { name: /^Voie Métier/ });
  ok(/Chargé de transfert/.test(await h.innerText()), 'titre de la voie Métier : ' + (await h.innerText()));
  await h.scrollIntoViewIfNeeded(); await p.mouse.wheel(0, -60); await snap('p10_voie_metier_cdt');
  await startLesson(p.locator('section[aria-label="Bloc Métier : chargé de transfert"]'));
  const it = find(await question());
  ok(it && it.step === 'mt1', 'leçon M1 : question hors mt1 (' + (it && it.step) + ')');
  await snap('p11_lecon_metier_cdt');
  await p.getByRole('button', { name: 'Quitter la séance' }).click(); await p.waitForTimeout(400);

  // 7. Changement de profil dans Profil : ingénieur brevet
  await p.getByRole('navigation').getByRole('button', { name: 'Profil' }).click(); await p.waitForTimeout(400);
  await p.getByRole('radio', { name: /Ingénieur brevet/ }).click(); await p.waitForTimeout(400);
  await p.getByRole('radiogroup', { name: 'Votre métier' }).scrollIntoViewIfNeeded(); await snap('p12_profil_metier');
  await p.getByRole('navigation').getByRole('button', { name: 'Parcours' }).click(); await p.waitForTimeout(500);
  ok(/Ingénieur brevet/.test(await p.getByRole('heading', { name: /^Voie Métier/ }).innerText()), 'voie Métier non mise à jour');
  await p.getByRole('button', { name: /Étape S1 / }).first().click(); await p.waitForTimeout(400);
  await p.getByRole('tab', { name: /Exercices/ }).click(); await p.waitForTimeout(300);
  ok(/Espacenet/.test(await p.locator('.z-30').innerText()), 'S1 exercices : variante brevet absente');
  await snap('p13_s1_exercice_brevet');
  await p.getByRole('button', { name: 'Revenir au parcours' }).click(); await p.waitForTimeout(300);

  // 8. Progression d'avant les profils : juriste présélectionné
  const ctx2 = await b.newContext({ viewport: { width: 375, height: 812 }, colorScheme: scheme, deviceScaleFactor: 2 });
  await ctx2.addInitScript(() => {
    if (localStorage.getItem('parcours-ia-juriste-v2')) return;
    localStorage.setItem('parcours-ia-juriste-v2', JSON.stringify({ state: { xp: 320, steps: { so1: { passed: true, notions: true, lessons: 2 }, me1: { notions: true, lessons: 1 } }, settings: { sound: false, cadre: 1, outil: 'ChatGPT' } } }));
  });
  const q = await ctx2.newPage(); q.on('pageerror', (e) => errs.push(String(e)));
  await q.goto(url); await q.waitForTimeout(1200);
  ok((await q.getByRole('radio', { name: /^Juriste/ }).getAttribute('aria-checked')) === 'true', 'migration : juriste non présélectionné');
  await q.screenshot({ path: `${out}/${scheme}_p14_migration_juriste.png` });
  await q.getByRole('button', { name: 'Continuer', exact: true }).click(); await q.waitForTimeout(300);
  ok((await q.getByRole('radio', { name: 'ChatGPT' }).getAttribute('aria-checked')) === 'true', 'migration : assistant non repris');
  await q.getByRole('button', { name: 'Reprendre le parcours' }).click(); await q.waitForTimeout(600);
  ok(/Juriste/.test(await q.getByRole('heading', { name: /^Voie Métier/ }).innerText()), 'migration : voie Métier juriste absente');
  const xp = await q.evaluate(() => JSON.parse(localStorage.getItem('parcours-ia-juriste-v2')).state.xp);
  ok(xp === 320, 'migration : XP modifiés (' + xp + ')');

  console.log(JSON.stringify({ scheme, fails, errs }));
  await b.close();
})();
