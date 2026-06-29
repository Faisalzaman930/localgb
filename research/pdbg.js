const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
const p=await b.newPage();
await p.goto(process.argv[2],{waitUntil:'networkidle2',timeout:45000});
await new Promise(r=>setTimeout(r,800));
const r=await p.evaluate(()=>{
  let c=document.body.cloneNode(true);c.querySelectorAll('script,style,noscript,nav,footer,header').forEach(e=>e.remove());
  const t=(c.textContent||'').replace(/\s+/g,' ');
  const prices=[...t.matchAll(/(?:Rs\.?|PKR|₨|price)[\s:]*[0-9][0-9,]{2,}/gi)].map(m=>t.slice(Math.max(0,m.index-15),m.index+30)).slice(0,8);
  // also raw numbers near 'price'
  const pi=t.toLowerCase().indexOf('price');
  return {prices, pricectx: pi>=0?t.slice(pi-10,pi+120):'(no price word)', lds:[...document.querySelectorAll('script[type="application/ld+json"]')].length};
})
console.log('price matches:',r.prices);
console.log('around "price":',r.pricectx);
console.log('jsonld blocks:',r.lds);
await b.close();
})();
