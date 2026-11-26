const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1587, height: 1122 }, deviceScaleFactor: 2 });
  await p.goto('file://' + __dirname + '/schema.html'); await p.waitForTimeout(500);
  const h = await p.evaluate(() => document.querySelector('.page').scrollHeight);
  console.log('hauteur', h);
  await p.screenshot({ path: __dirname + '/schema.png', fullPage: true });
  await p.pdf({ path: __dirname + '/schema.pdf', width: '420mm', height: Math.ceil(h / 1587 * 420 + 2) + 'mm', printBackground: true, pageRanges: '1' });
  await b.close();
})();
