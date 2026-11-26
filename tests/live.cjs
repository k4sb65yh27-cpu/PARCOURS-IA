const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const errs=[];
 const p = await (await b.newContext({viewport:{width:375,height:812}})).newPage();
 p.on('pageerror', e=>errs.push(String(e))); const bad=[]; p.on('response', r=>{ if(r.status()>=400) bad.push(r.status()+' '+r.url()) });
 await p.goto(process.argv[2]); await p.waitForTimeout(3000);
 const sw = await p.evaluate(()=>navigator.serviceWorker.getRegistrations().then(r=>r.length));
 console.log(JSON.stringify({title: await p.title(), h: (await p.locator('body').innerText()).slice(0,120), sw, errs, bad}));
 await p.screenshot({path:'live.png'}); await b.close(); })();
