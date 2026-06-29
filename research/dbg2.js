const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
const p=await b.newPage();
await p.goto(process.argv[2],{waitUntil:'networkidle2',timeout:45000});
await new Promise(r=>setTimeout(r,800));
const ctx=await p.evaluate(()=>{
  let c=document.body.cloneNode(true);c.querySelectorAll('script,style,noscript').forEach(e=>e.remove());
  const t=(c.textContent||'').replace(/\s+/g,' ');
  const out=[];const re=/day\s*0?\d{1,2}/gi;let m;
  while((m=re.exec(t))){out.push(t.slice(m.index,m.index+70));}
  return out;
});
ctx.forEach((s,i)=>console.log(i+1,'|',s));
await b.close();
})();
