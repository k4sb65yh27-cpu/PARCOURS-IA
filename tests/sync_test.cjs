// Synchronisation par compte : appareil A (PC) progresse, appareil B (téléphone) se connecte et retrouve tout.
const { chromium } = require('playwright');
const url = process.argv[2], out = process.argv[3];
(async () => {
  const b = await chromium.launch();
  const errs = [];
  const dev = async (vp) => {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto(url); await p.waitForTimeout(1200);
    // Premier lancement : choix du métier puis de l'assistant (écran ajouté avec les profils, c0ebf10).
    if (await p.getByRole('radiogroup', { name: 'Votre métier' }).count()) {
      await p.getByRole('radio', { name: /Juriste/ }).click();
      await p.getByRole('button', { name: 'Continuer', exact: true }).click();
      await p.waitForTimeout(400);
      await p.getByRole('radio', { name: 'Claude', exact: true }).click();
      await p.getByRole('button', { name: /^(Commencer|Reprendre le parcours)$/ }).click();
      await p.waitForTimeout(500);
    }
    return p;
  };
  const profile = async (p) => { await p.getByRole('navigation').getByRole('button', { name: 'Profil' }).click(); await p.waitForTimeout(400); };
  // Appareil A : PC
  const A = await dev({ width: 1280, height: 800 });
  await A.screenshot({ path: `${out}/pc_parcours.png` });
  await profile(A);
  await A.getByRole('button', { name: 'Première fois : créer un compte' }).click();
  await A.getByLabel('Courriel professionnel').fill('test.juriste@sattse.com');
  await A.getByLabel(/Mot de passe/).fill('motdepasse-assez-long');
  await A.getByRole('button', { name: 'Créer mon compte' }).click();
  await A.waitForTimeout(1500);
  await A.getByText('Connecté').first().scrollIntoViewIfNeeded();
  await A.screenshot({ path: `${out}/pc_compte.png` });
  // Progression sur A : lire les notions de S1
  await A.getByRole('navigation').getByRole('button', { name: 'Parcours' }).click();
  await A.getByRole('button', { name: /à faire maintenant/ }).first().click();
  await A.getByRole('button', { name: /Lire les notions/ }).click();
  for (let i = 0; i < 10; i++) { const f = A.getByRole('button', { name: "J'ai compris" }); if (await f.count()) { await f.click(); break; } await A.getByRole('button', { name: 'Suivante' }).click(); await A.waitForTimeout(350); }
  await A.waitForTimeout(4000); // poussée différée de 2,5 s
  const xpA = await A.evaluate(() => JSON.parse(localStorage.getItem('parcours-ia-juriste-v2')).state.xp);
  // Appareil B : téléphone, connexion au même compte
  const B = await dev({ width: 375, height: 812 });
  await profile(B);
  await B.getByLabel('Courriel professionnel').fill('test.juriste@sattse.com');
  await B.getByLabel(/Mot de passe/).fill('motdepasse-assez-long');
  await B.getByRole('button', { name: 'Se connecter' }).click();
  await B.waitForTimeout(2000);
  const xpB = await B.evaluate(() => JSON.parse(localStorage.getItem('parcours-ia-juriste-v2')).state.xp);
  const notB = await B.evaluate(() => JSON.parse(localStorage.getItem('parcours-ia-juriste-v2')).state.steps.so1?.notions);
  await B.getByText('Connecté').first().scrollIntoViewIfNeeded();
  await B.screenshot({ path: `${out}/mobile_compte.png` });
  // Mauvais mot de passe
  const C = await dev({ width: 375, height: 812 });
  await profile(C);
  await C.getByLabel('Courriel professionnel').fill('test.juriste@sattse.com');
  await C.getByLabel(/Mot de passe/).fill('faux');
  await C.getByRole('button', { name: 'Se connecter' }).click();
  await C.waitForTimeout(1500);
  const alert = await C.getByRole('alert').innerText().catch(() => '');
  console.log(JSON.stringify({ xpA, xpB, notB, alert, errs }));
  await b.close();
})();
