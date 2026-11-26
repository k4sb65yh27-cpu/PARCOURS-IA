const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const scheme of ['light', 'dark']) {
    const p = await b.newPage({ viewport: { width: 375, height: 812 }, colorScheme: scheme });
    await p.goto(process.argv[2]); await p.waitForTimeout(1000);
    await p.getByRole('navigation').getByRole('button', { name: 'Réviser' }).click();
    await p.waitForTimeout(1200);
    await p.screenshot({ path: `${process.argv[3]}/${scheme}_review.png`, fullPage: true });
    await p.getByText('Tous les défis, par compétence').click(); await p.waitForTimeout(500);
    const sw = await p.evaluate(() => document.documentElement.scrollWidth); console.log(scheme, 'scrollWidth', sw);
    await p.close();
  }
  await b.close();
})();
