const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
const p=await b.newPage();
for(const w of [1280,390]){
  await p.setViewport({width:w,height:900});
  await p.goto('file://'+process.argv[2],{waitUntil:'load'});
  const r=await p.evaluate(()=>{
    const g=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return {top:Math.round(r.top),bottom:Math.round(r.bottom),h:Math.round(r.height)};};
    return {nav:g('nav'),crumb:g('.art-crumb'),eyebrow:g('.article-eyebrow'),h1:g('.article-title'),meta:g('.article-meta'),navPos:getComputedStyle(document.querySelector('nav')).position,headPadTop:getComputedStyle(document.querySelector('.article-head')).paddingTop};
  });
  console.log(`\n--- width ${w} --- nav:${r.navPos}`);
  console.log('nav',r.nav,'| head padTop',r.headPadTop);
  console.log('crumb',r.crumb,'eyebrow',r.eyebrow);
  console.log('h1',r.h1,'meta',r.meta);
  if(r.nav&&r.crumb&&r.nav.bottom>r.crumb.top)console.log('⚠️ NAV OVERLAPS CRUMB by',r.nav.bottom-r.crumb.top,'px');
}
await b.close();
})();
