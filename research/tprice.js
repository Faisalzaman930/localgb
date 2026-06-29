const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
const p=await b.newPage();
for(const u of process.argv.slice(2)){
  try{
    await p.goto(u,{waitUntil:'networkidle2',timeout:45000}); await new Promise(r=>setTimeout(r,800));
    const t=await p.evaluate(()=>{let c=document.body.cloneNode(true);c.querySelectorAll('script,style,noscript,nav,footer,header').forEach(e=>e.remove());return (c.textContent||'').replace(/\s+/g,' ');});
    const m=[...t.matchAll(/(from|starting|price)[^.]{0,8}?(US\$|USD|Rs\.?|PKR|₨|\$|€)\s?[0-9][0-9,]{2,}/gi)].map(x=>x[0].slice(0,40)).slice(0,4);
    const any=[...t.matchAll(/(US\$|USD|\$|€|Rs|PKR)\s?[0-9][0-9,]{2,}/g)].map(x=>x[0]).slice(0,6);
    console.log('\n'+u.split('/').slice(-2)[0]);
    console.log('  from/starting price:', m.length?m:'(none)');
    console.log('  any currency match:', any.length?any:'(none)');
  }catch(e){console.log('!',e.message.slice(0,40));}
}
await b.close();
})();
