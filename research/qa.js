const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
const p=await b.newPage();
for(const slug of ['hunza','gilgit-baltistan','skardu']){
  for(const w of [1280,390]){
    await p.setViewport({width:w,height:900});
    await p.goto('http://localhost:8767/tours/'+slug+'/index.html',{waitUntil:'networkidle2'});
    const r=await p.evaluate(()=>{
      const navB=document.querySelector('nav').getBoundingClientRect().bottom;
      const crumb=document.querySelector('.art-crumb')?.getBoundingClientRect().top;
      const sw=document.documentElement.scrollWidth, cw=document.documentElement.clientWidth;
      // any element wider than viewport (horizontal overflow)?
      let over=[];document.querySelectorAll('.article *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width>cw+2)over.push(e.className||e.tagName);});
      return {navOverlap: crumb!=null && navB>crumb, hOverflow: sw>cw+2, overEls:[...new Set(over)].slice(0,4)};
    });
    console.log(`${slug} @${w}: navOverlap=${r.navOverlap} hScroll=${r.hOverflow} ${r.overEls.length?'overflow:'+r.overEls.join(','):''}`);
  }
}
await b.close();
})();
