/* Scraper v4 — deep package extractor: itinerary, inclusions, price, urls.
 * Modes: node deep.js test <url> [url2...]   |   node deep.js crawl   (uses seeds.txt)
 */
const puppeteer=require('puppeteer-core');
const fs=require('fs'),path=require('path');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const arr=x=>Array.isArray(x)?x:(x==null?[]:[x]);
const host=u=>{try{return new URL(u).hostname.replace(/^www\./,'');}catch{return'';}};
const homepage=u=>{try{const x=new URL(u);return x.origin;}catch{return'';}};
const GEO=/(pakistan|skardu|hunza|gilgit|naran|kaghan|fairy|deosai|baltistan|northern|chitral|swat|kalam|neelam|hushe|shimshal|khaplu|shigar|attabad|phander|shandur|kashmir|murree|nathia|kumrat)/i;
const DETAIL=/(\/t\/\d|\/tour\/|\/tours\/|\/trip\/|\/p\/|\/packages?\/)/i;
function flat(n,o=[]){if(Array.isArray(n)){n.forEach(x=>flat(x,o));return o;}if(n&&typeof n==='object'){o.push(n);if(n['@graph'])flat(n['@graph'],o);for(const k of ['offers','itemListElement','item'])if(n[k])flat(n[k],o);}return o;}
function schemaPrice(lds){
  for(const raw of lds){let d;try{d=JSON.parse(raw);}catch{continue;}
    for(const n of flat(d)){const o=n.offers?arr(n.offers)[0]:null;
      const p=(o&&(o.price||o.lowPrice))||n.price||'';const c=(o&&o.priceCurrency)||n.priceCurrency||'';
      if(p)return{price:String(p),currency:c};}}
  return{price:'',currency:''};
}
function extractItin(text){
  const t=text.replace(/\s+/g,' ');
  const ms=[...t.matchAll(/\bday\s*0?(\d{1,2})(?!\d)/gi)];
  const by={};
  for(let i=0;i<ms.length;i++){
    const day=+ms[i][1]; if(day<1||day>25) continue;
    const start=ms[i].index+ms[i][0].length;
    const end=i+1<ms.length?ms[i+1].index:Math.min(t.length,start+280);
    let txt=t.slice(start,end).replace(/^[\s:.\-–|)]+/,'').replace(/\s+/g,' ').trim().slice(0,240);
    if(txt.length>12 && (!by[day]||txt.length>by[day].length)) by[day]=txt;
  }
  return Object.keys(by).map(d=>({day:+d,txt:by[d]})).sort((a,b)=>a.day-b.day);
}
function extractList(text,startkw){
  const m=text.match(new RegExp('('+startkw+')\\s*[:\\-]?\\s*([^]{20,500}?)(exclusion|not included|exclude|price|book|day 1|itinerary|$)','i'));
  if(!m)return [];
  return m[2].split(/[••\n\|,]| - /).map(s=>s.replace(/\s+/g,' ').trim()).filter(s=>s.length>3&&s.length<80).slice(0,12);
}
async function extract(page,url){
  const d=await page.evaluate(()=>({
    ld:[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent),
    title:(document.querySelector('h1')?.innerText||document.title||'').trim().slice(0,140),
    text:(()=>{let c=document.body.cloneNode(true);c.querySelectorAll('script,style,noscript,nav,footer,header').forEach(e=>e.remove());return (c.textContent||'').replace(/\r/g,' ');})()}));
  const flatText=d.text.replace(/\s+/g,' ');
  const pr=schemaPrice(d.ld);
  const dm=flatText.match(/(\d{1,2})\s*days?(?:\s*[\/&\-]\s*(\d{1,2})\s*nights?)?/i);
  return {url, operator:host(url), operatorUrl:homepage(url),
    name:d.title, days:dm?dm[0]:'', price:pr.price, currency:pr.currency,
    itinerary:extractItin(d.text), includes:extractList(flatText,"inclusions?|includes?|what'?s included"),
    excludes:extractList(flatText,"exclusions?|excludes?|not included")};
}
async function getXml(u){try{const r=await fetch(u,{headers:{'User-Agent':UA},signal:AbortSignal.timeout(15000)});return r.ok?await r.text():'';}catch{return'';}}
const locs=x=>[...x.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/gi)].map(m=>m[1]);
async function sitemap(dom){
  for(const c of [`https://www.${dom}/sitemap_index.xml`,`https://${dom}/sitemap_index.xml`,`https://www.${dom}/sitemap.xml`,`https://${dom}/sitemap.xml`,`https://${dom}/wp-sitemap.xml`]){
    const xml=await getXml(c);if(!xml)continue;let urls=[];
    if(/<sitemapindex/i.test(xml)){for(const ch of locs(xml).slice(0,10)){urls.push(...locs(await getXml(ch)));}}else urls=locs(xml);
    if(urls.length)return [...new Set(urls)];}
  return [];
}
(async()=>{
  const mode=process.argv[2]||'crawl';
  const browser=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox','--disable-gpu']});
  const page=await browser.newPage();await page.setUserAgent(UA);
  const out=[];
  if(mode==='test'){
    for(const u of process.argv.slice(3)){
      try{await page.goto(u,{waitUntil:'networkidle2',timeout:45000});await sleep(700);const r=await extract(page,u);out.push(r);
        console.log(`\n● ${r.name} | ${r.days} | ${r.price} ${r.currency}`);
        console.log('  itinerary days:',r.itinerary.length);r.itinerary.slice(0,3).forEach(d=>console.log(`   D${d.day}: ${d.txt.slice(0,80)}`));
        console.log('  includes:',r.includes.slice(0,4).join(' | '));}
      catch(e){console.log('! '+u+' '+e.message.slice(0,40));}
    }
  } else {
    const seeds=fs.readFileSync('seeds.txt','utf8').split('\n').map(s=>s.trim()).filter(s=>s&&!s.startsWith('#'));
    for(const seed of seeds){
      const dom=host(seed);const mkt=/tourradar|bookmundi|findmyadventure/.test(dom);
      let targets=new Set();
      if(!mkt){const sm=await sitemap(dom);sm.filter(u=>host(u)===dom&&GEO.test(u)&&DETAIL.test(u)).forEach(u=>targets.add(u));}
      try{await page.goto(seed,{waitUntil:'networkidle2',timeout:45000});await sleep(600);
        const links=await page.$$eval('a[href]',a=>a.map(x=>x.href));
        links.filter(u=>host(u)===dom&&DETAIL.test(u)&&(mkt||GEO.test(u))).forEach(u=>targets.add(u));}catch(e){}
      const list=[...targets].slice(0,30);
      console.log(`● ${dom}: ${list.length} package pages`);
      for(const u of list){try{await page.goto(u,{waitUntil:'networkidle2',timeout:40000});await sleep(500);const r=await extract(page,u);
        if(r.itinerary.length||r.price){out.push(r);console.log(`  ✓ ${r.name.slice(0,42)} | ${r.days} | ${r.itinerary.length}d itin | ${r.price||'-'}`);}
        await sleep(700);}catch(e){console.log(`  ! ${u.slice(0,50)} ${e.message.slice(0,25)}`);}}
    }
  }
  await browser.close();
  if(mode!=='test'){fs.writeFileSync('packages-deep.json',JSON.stringify(out,null,2));console.log(`\n✅ ${out.length} packages, ${out.filter(p=>p.itinerary.length).length} with itineraries → packages-deep.json`);}
})().catch(e=>{console.error('FATAL',e.message);process.exit(1)});
