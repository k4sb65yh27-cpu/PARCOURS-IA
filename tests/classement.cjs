// Classement (version serveur) : onglet masqué si désactivé, participation, nom en double refusé, retrait.
// Usage : servir le paquet serveur (php -S), puis node tests/classement.cjs <dossier> <url> light|dark on|off
const { chromium } = require('playwright');
const [out, url, theme = 'light', mode = 'on'] = process.argv.slice(2);
const res = { theme, mode, errs: [] };
const check = (n, ok) => { res[n] = ok; if (!ok) res.errs.push('échec : ' + n); };
const KEY = 'parcours-ia-juriste-v2';
// Noms propres à chaque exécution : plusieurs passages sur la même base ne se gênent pas.
const n = String(Date.now() % 100000);
const NA = 'Alice' + n, NB = 'Bruno' + n;
(async () => {
  const b = await chromium.launch();
  const dev = async (email, xp) => {
    const ctx = await b.newContext({ viewport: { width: 375, height: 812 }, colorScheme: theme, deviceScaleFactor: 1, serviceWorkers: 'block' });
    const day = new Date().toISOString().slice(0, 10);
    const root = { state: { updatedAt: 1, xp, streak: { count: 1, lastDay: day }, daily: { day, xp: 0, goal: 20 }, steps: {}, srs: {}, free: false, settings: { sound: false, haptics: false, cadre: 1, outil: 'Claude', profil: 'juriste' }, defis: {} }, notes: {}, answers: {}, plan: null, journal: null, tutor: null };
    await ctx.addInitScript(([k, v]) => { if (!localStorage.getItem('seeded')) { localStorage.setItem(k, v); localStorage.setItem('seeded', '1'); } }, [KEY, JSON.stringify(root)]);
    const p = await ctx.newPage();
    p.on('pageerror', e => res.errs.push(String(e)));
    await p.goto(url); await p.waitForTimeout(1200);
    await p.getByRole('navigation').getByRole('button', { name: 'Profil' }).click();
    await p.getByRole('button', { name: 'Première fois : créer un compte' }).click();
    await p.getByLabel('Courriel professionnel').fill(email);
    await p.getByLabel(/Mot de passe/).fill('motdepasse-assez-long');
    await p.getByRole('button', { name: 'Créer mon compte' }).click();
    await p.waitForTimeout(1800);
    return p;
  };
  // Lignes du classement de cette exécution (la base peut contenir des passages précédents ; les notifications sont exclues).
  const lignes = async (p) => (await p.locator('section', { hasText: 'Les dix premiers' }).locator('ol li').allInnerTexts()).filter(x => x.includes(n));
  const tab = (p) => p.getByRole('navigation').getByRole('button', { name: 'Classement' });
  const A = await dev(`alice.${Date.now()}@sattse.com`, 340);
  if (mode === 'off') {
    check('onglet_masque_si_desactive', await tab(A).count() === 0);
    await b.close(); console.log(JSON.stringify(res)); return;
  }
  check('onglet_present', await tab(A).count() === 1);
  await tab(A).click(); await A.waitForTimeout(800);
  await A.screenshot({ path: `${out}/classement_vide_${theme}.png`, fullPage: true });
  await A.getByLabel(/Nom affiché/).fill(NA);
  await A.getByRole('button', { name: 'Participer' }).click();
  await A.waitForTimeout(1200);
  check('participation_alice', await A.getByRole('button', { name: 'Me retirer' }).count() === 1);
  await A.getByRole('button', { name: 'Depuis le début', exact: true }).click();
  await A.waitForTimeout(800);
  check('alice_340_depuis_le_debut', await A.getByText('340 XP').count() > 0);
  const B = await dev(`bruno.${Date.now()}@sattse.com`, 90);
  await tab(B).click(); await B.waitForTimeout(600);
  await B.getByLabel(/Nom affiché/).fill(NA.toLowerCase());
  await B.getByRole('button', { name: 'Participer' }).click();
  await B.waitForTimeout(1000);
  check('nom_en_double_refuse', /déjà pris/.test(await B.getByRole('alert').innerText().catch(() => '')));
  await B.getByLabel(/Nom affiché/).fill(NB);
  await B.getByRole('button', { name: 'Participer' }).click();
  await B.waitForTimeout(1000);
  await B.getByRole('button', { name: 'Depuis le début', exact: true }).click();
  await B.waitForTimeout(800);
  const rows = await lignes(B);
  res.rows = rows;
  check('ordre_classement', rows.length === 2 && rows[0].includes(NA) && rows[1].includes(NB));
  check('semaine_part_de_zero', await (async () => { await B.getByRole('button', { name: 'Semaine', exact: true }).click(); await B.waitForTimeout(700); return (await lignes(B)).every(t => /\b0 XP/.test(t)); })());
  check('sans_defilement_horizontal', !(await B.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)));
  await B.getByRole('button', { name: 'Depuis le début', exact: true }).click(); await B.waitForTimeout(600);
  await B.screenshot({ path: `${out}/classement_${theme}.png`, fullPage: true });
  await A.getByRole('button', { name: 'Me retirer' }).click();
  await A.waitForTimeout(1000);
  await B.getByRole('button', { name: 'Mois', exact: true }).click(); await B.waitForTimeout(400);
  await B.getByRole('button', { name: 'Depuis le début', exact: true }).click(); await B.waitForTimeout(800);
  const rows2 = await lignes(B);
  check('retrait_effectif', rows2.length === 1 && rows2[0].includes(NB));
  check('mention_emulation', await B.getByText('Il n\'est utilisé pour aucune évaluation.').count() === 1);
  await b.close();
  console.log(JSON.stringify(res));
})();
