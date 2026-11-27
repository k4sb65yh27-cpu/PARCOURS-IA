// Préparation commune aux contrôles : premier lancement, profil juriste, assistant Claude.
module.exports = async function (p) {
  if (!(await p.getByRole('radiogroup', { name: 'Votre métier' }).count())) return;
  await p.getByRole('radio', { name: /Juriste/ }).click();
  await p.getByRole('button', { name: 'Continuer', exact: true }).click();
  await p.waitForTimeout(400);
  await p.getByRole('radio', { name: 'Claude', exact: true }).click();
  await p.getByRole('button', { name: /^(Commencer|Reprendre le parcours)$/ }).click();
  await p.waitForTimeout(600);
};
