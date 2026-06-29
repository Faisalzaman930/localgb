const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
const p=await b.newPage();
for(const w of [1280,390]){
  await p.setViewport({width:w,height:900});
  await p.goto(process.argv[2],{waitUntil:'networkidle2'});
  const r=await p.evaluate(()=>{
    const g=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return {top:Math.round(r.top),bottom:Math.round(r.bottom)};};
    const nav=document.querySelector('nav');
    return {navPos:getComputedStyle(nav).position,navH:Math.round(nav.getBoundingClientRect().height),
      navlinks:getComputedStyle(document.querySelector('.nav-links')).display,
      crumb:g('.art-crumb'),h1:g('.article-title'),headPad:getComputedStyle(document.querySelector('.article-head')).paddingTop};
  });
  console.log(`w${w}: nav ${r.navPos} h${r.navH} | links:${r.navlinks} | headPad ${r.headPad} | crumb.top ${r.crumb?.top} h1.top ${r.h1?.top}`);
}
await b.close();
})();
