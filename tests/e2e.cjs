// Parcours complet à 375 px : captures et contrôles (débordement horizontal, erreurs console).
const { chromium } = require('playwright');
const out = process.argv[2], url = process.argv[3], scheme = process.argv[4] || 'light', profil = process.argv[5] || 'support';
// Premier lancement : choix du métier puis de l'assistant (profil en dernier argument, « support » par défaut).
async function onboarding(p, profil) {
  const noms = { juriste: 'Juriste', cdt: 'Chargé de transfert', brevet: 'Ingénieur brevet', support: 'Fonctions support et direction' };
  if (!(await p.getByRole('radiogroup', { name: 'Votre métier' }).count())) return;
  await p.getByRole('radio', { name: new RegExp(noms[profil]) }).click();
  await p.getByRole('button', { name: 'Continuer', exact: true }).click();
  await p.waitForTimeout(400);
  await p.getByRole('radio', { name: 'Claude', exact: true }).click();
  await p.getByRole('button', { name: /^(Commencer|Reprendre le parcours)$/ }).click();
  await p.waitForTimeout(500);
}

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 1, colorScheme: scheme, hasTouch: true });
  const p = await ctx.newPage();
  const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push(String(e)));
  const snap = async (n) => {
    await p.waitForTimeout(500);
    const sw = await p.evaluate(() => document.documentElement.scrollWidth);
    if (sw > 375) errs.push(`overflow ${n}: ${sw}`);
    await p.screenshot({ path: `${out}/${scheme}_${n}.png` });
  };
  await p.goto(url); await p.waitForTimeout(1200);
  await snap('00_onboarding');
  await onboarding(p, profil);
  await snap('01_home');
  // nœud courant -> tiroir
  await p.getByRole('button', { name: /à faire maintenant/ }).first().click();
  await snap('02_drawer');
  await p.getByRole('button', { name: /Lire les notions/ }).click();
  await snap('03_notions');
  for (let i = 0; i < 10; i++) { const f = p.getByRole('button', { name: "J'ai compris" }); if (await f.count()) { await f.click(); break; } await p.getByRole('button', { name: 'Suivante' }).click(); await p.waitForTimeout(350); }
  await p.waitForTimeout(600);
  await snap('04_home_after');
  // leçon
  await p.getByRole('button', { name: /à faire maintenant/ }).first().click();
  await p.waitForTimeout(400);
  await p.getByRole('button', { name: /^Commencer$/ }).click();
  await p.waitForTimeout(600);
  let shots = 0, seen = new Set();
  for (let k = 0; k < 30; k++) {
    const kind = (await p.locator('div.z-40 main p').first().innerText()).toLowerCase();
    // répondre : choisir le premier choix disponible
    if (kind.includes('associez')) {
      const n = await p.locator('div.z-40 main .grid-cols-2 > button').count();
      for (let i = 0; i < n / 2; i++) { await p.locator('div.z-40 main .grid-cols-2 > button').nth(i * 2).click(); await p.locator('div.z-40 main .grid-cols-2 > button').nth(i * 2 + 1).click(); }
    } else if (kind.includes('ordre')) {
      for (let i = 0; i < 8; i++) { const r = p.locator('[aria-label="Éléments à placer"] button'); if (!(await r.count())) break; await r.first().click(); await p.waitForTimeout(80); }
    } else {
      await p.locator('[data-key="1"]').first().click();
    }
    const tag = kind.split(' ')[0];
    if (!seen.has(tag) && shots < 6) { seen.add(tag); await snap(`05_q_${tag}`); }
    await p.getByRole('button', { name: 'Vérifier', exact: true }).click();
    if (shots < 6) { shots++; await snap(`06_fb_${k}`); }
    await p.getByRole('button', { name: 'Continuer', exact: true }).click();
    await p.waitForTimeout(450);
    if (await p.getByText(/Leçon terminée|Plus de vies/).count()) break;
  }
  await p.waitForTimeout(1500);
  await snap('07_end');
  await p.getByRole('button', { name: 'Continuer', exact: true }).click();
  await p.waitForTimeout(600);
  await snap('08_home_progress');
  for (const [t, n] of [['Réviser', '09_review'], ['Glossaire', '10_gloss'], ['Profil', '11_profile']]) {
    await p.getByRole('navigation').getByRole('button', { name: t }).click(); await snap(n);
  }
  await p.getByRole('navigation').getByRole('button', { name: 'Glossaire' }).click();
  await p.locator('[aria-pressed]').first().click(); await snap('12_gloss_flip');
  await p.getByRole('navigation').getByRole('button', { name: 'Parcours' }).click();
  await p.waitForTimeout(500);
  await p.getByRole('button', { name: /Étape S1 / }).first().click();
  await snap('13_guide');
  await p.getByRole('tab', { name: /Exercices/ }).click(); await snap('14_guide_ex');
  await p.getByRole('button', { name: 'Revenir au parcours' }).click(); await p.waitForTimeout(400);
  await p.getByRole('heading', { name: /^Voie Métier/ }).scrollIntoViewIfNeeded(); await p.mouse.wheel(0, -60); await snap('15_voie_metier');
  await p.getByRole('heading', { name: 'Voie Expert', exact: true }).scrollIntoViewIfNeeded(); await snap('16_voie_expert');
  await p.getByRole('button', { name: /Étape E2 / }).first().click(); await snap('17_guide_e2');
  await p.evaluate(() => document.querySelector('.z-30').scrollTo(0, 99999)); await snap('18_guide_tuteur');
  await p.getByRole('button', { name: 'Revenir au parcours' }).click(); await p.waitForTimeout(400);
  await p.getByRole('navigation').getByRole('button', { name: 'Réviser' }).click();
  await p.screenshot({ path: `${out}/${scheme}_19_review_full.png`, fullPage: true });
  await p.getByRole('navigation').getByRole('button', { name: 'Profil' }).click();
  await p.waitForTimeout(400);
  await p.screenshot({ path: `${out}/${scheme}_20_profile_full.png`, fullPage: true });
  console.log(JSON.stringify(errs));
  await b.close();
})();
