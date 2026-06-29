/* Scraper v5 — deep package extractor: itinerary + inclusions/exclusions + meals
 * + payment policy + price + urls. node deep.js test <url>  |  node deep.js crawl
 */
const puppeteer=require('puppeteer-core');
const fs=require('fs');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const arr=x=>Array.isArray(x)?x:(x==null?[]:[x]);
const host=u=>{try{return new URL(u).hostname.replace(/^www\./,'');}catch{return'';}};
const homepage=u=>{try{return new URL(u).origin;}catch{return'';}};
const EXCLUDE=['apricottours','natureadventureclub','pakistantours'];   // top-3 SERP — never feature
const GEO=/(pakistan|skardu|hunza|gilgit|naran|kaghan|fairy|deosai|baltistan|northern|chitral|swat|kalam|neelam|hushe|shimshal|khaplu|shigar|attabad|phander|shandur|kashmir|murree|nathia|kumrat)/i;
const DETAIL=/(\/t\/\d|\/tour\/|\/tours\/|\/trip\/|\/p\/|\/packages?\/)/i;
function flat(n,o=[]){if(Array.isArray(n)){n.forEach(x=>flat(x,o));return o;}if(n&&typeof n==='object'){o.push(n);if(n['@graph'])flat(n['@graph'],o);for(const k of ['offers','itemListElement','item'])if(n[k])flat(n[k],o);}return o;}
function schemaPrice(lds){for(const raw of lds){let d;try{d=JSON.parse(raw);}catch{continue;}for(const n of flat(d)){const o=n.offers?arr(n.offers)[0]:null;const p=(o&&(o.price||o.lowPrice))||n.price||'';const c=(o&&o.priceCurrency)||n.priceCurrency||'';if(p)return{price:String(p),currency:c};}}return{price:'',currency:''};}
function extractItin(text){
  const t=text.replace(/\s+/g,' ');
  const ms=[...t.matchAll(/\bday\s*0?(\d{1,2})(?!\d)/gi)];
  const by={};
  for(let i=0;i<ms.length;i++){const day=+ms[i][1];if(day<1||day>25)continue;
    const start=ms[i].index+ms[i][0].length;const end=i+1<ms.length?ms[i+1].index:Math.min(t.length,start+280);
    let txt=t.slice(start,end).replace(/^[\s:.\-–|)]+/,'').replace(/\s+/g,' ').trim().slice(0,240);
    if(txt.length>12&&(!by[day]||txt.length>by[day].length))by[day]=txt;}
  return Object.keys(by).map(d=>({day:+d,txt:by[d]})).sort((a,b)=>a.day-b.day);
}
function section(t,startRe,endRe){
  const m=t.match(startRe); if(!m) return '';
  const from=m.index+m[0].length;
  const rest=t.slice(from, from+900);
  const e=rest.search(endRe);
  return (e>0?rest.slice(0,e):rest).replace(/\s+/g,' ').trim();
}
function bullets(s){return [...new Set(s.split(/[•·▪►|]|(?<=[a-z])\.(?=\s+[A-Z])|\n/).map(x=>x.replace(/\s+/g,' ').trim()).filter(x=>x.length>3&&x.length<90))].slice(0,12);}
async function extract(page,url){
  const d=await page.evaluate(()=>({
    ld:[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent),
    title:(document.querySelector('h1')?.innerText||document.title||'').trim().slice(0,140),
    text:(()=>{let c=document.body.cloneNode(true);c.querySelectorAll('script,style,noscript,nav,footer,header').forEach(e=>e.remove());return (c.textContent||'').replace(/\r/g,' ');})()}));
  const flatText=d.text.replace(/\s+/g,' ');
  const pr=schemaPrice(d.ld);
  const dm=flatText.match(/(\d{1,2})\s*days?(?:\s*[\/&\-]\s*(\d{1,2})\s*nights?)?/i);
  const incRaw=section(flatText,/(price includes?|tour includes?|package includes?|cost includes?|what'?s included|inclusions?)\s*[:\-]?/i,/(exclusion|not includ|what'?s not|excludes?|itinerary|\bday\s*0?1\b|payment|cancellation|book now)/i);
  const excRaw=section(flatText,/(exclusions?|not included|what'?s not included|excludes?)\s*[:\-]?/i,/(payment|cancellation|terms|policy|faq|note:|book now|itinerary|map\b)/i);
  const polRaw=section(flatText,/(payment policy|cancellation policy|booking policy|refund policy|advance payment|terms (and|&) conditions)\s*[:\-]?/i,/(faq|frequently asked|related|copyright|©)/i);
  const meals=[]; if(/breakfast/i.test(flatText))meals.push('breakfast'); if(/\blunch/i.test(flatText))meals.push('lunch'); if(/\bdinner/i.test(flatText))meals.push('dinner'); if(/full board/i.test(flatText))meals.push('full-board'); if(/half board/i.test(flatText))meals.push('half-board');
  const hotelHint = /(\d|three|four|five)\s*star/i.test(flatText)?(flatText.match(/(three|four|five|\d)\s*star[^.]{0,40}/i)||[''])[0].trim():'';
  return {url, operator:host(url), operatorUrl:homepage(url), name:d.title, days:dm?dm[0]:'',
    price:pr.price, currency:pr.currency, itinerary:extractItin(d.text),
    includes:bullets(incRaw), excludes:bullets(excRaw),
    meals:[...new Set(meals)].join(', '), hotelHint, policy:polRaw.slice(0,300)};
}
async function getXml(u){try{const r=await fetch(u,{headers:{'User-Agent':UA},signal:AbortSignal.timeout(15000)});return r.ok?await r.text():'';}catch{return'';}}
const locs=x=>[...x.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/gi)].map(m=>m[1]);
async function sitemap(dom){for(const c of [`https://www.${dom}/sitemap_index.xml`,`https://${dom}/sitemap_index.xml`,`https://www.${dom}/sitemap.xml`,`https://${dom}/sitemap.xml`,`https://${dom}/wp-sitemap.xml`]){const xml=await getXml(c);if(!xml)continue;let urls=[];if(/<sitemapindex/i.test(xml)){for(const ch of locs(xml).slice(0,10))urls.push(...locs(await getXml(ch)));}else urls=locs(xml);if(urls.length)return [...new Set(urls)];}return [];}
(async()=>{
  const mode=process.argv[2]||'crawl';
  const browser=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox','--disable-gpu']});
  const page=await browser.newPage();await page.setUserAgent(UA);
  const out=[];
  if(mode==='test'){
    for(const u of process.argv.slice(3)){try{await page.goto(u,{waitUntil:'networkidle2',timeout:45000});await sleep(700);const r=await extract(page,u);
      console.log(`\n● ${r.name} | ${r.days} | ${r.price} ${r.currency} | ${r.itinerary.length}d itin`);
      console.log('  meals:',r.meals||'-','| hotel:',r.hotelHint||'-');
      console.log('  includes:',r.includes.slice(0,5).join(' · ')||'-');
      console.log('  excludes:',r.excludes.slice(0,4).join(' · ')||'-');
      console.log('  policy:',(r.policy||'-').slice(0,120));}catch(e){console.log('!',e.message.slice(0,50));}}
  } else {
    const seeds=fs.readFileSync('seeds.txt','utf8').split('\n').map(s=>s.trim()).filter(s=>s&&!s.startsWith('#'));
    for(const seed of seeds){const dom=host(seed);if(EXCLUDE.some(d=>dom.includes(d))){console.log('SKIP',dom);continue;}
      let targets=new Set();const sm=await sitemap(dom);sm.filter(u=>host(u)===dom&&GEO.test(u)&&DETAIL.test(u)).forEach(u=>targets.add(u));
      try{await page.goto(seed,{waitUntil:'networkidle2',timeout:45000});await sleep(600);const links=await page.$$eval('a[href]',a=>a.map(x=>x.href));links.filter(u=>host(u)===dom&&DETAIL.test(u)&&GEO.test(u)).forEach(u=>targets.add(u));}catch(e){}
      const list=[...targets].slice(0,30);console.log(`● ${dom}: ${list.length} pages`);
      for(const u of list){try{await page.goto(u,{waitUntil:'networkidle2',timeout:40000});await sleep(500);const r=await extract(page,u);if(r.itinerary.length||r.price){out.push(r);console.log(`  ✓ ${r.name.slice(0,40)} | ${r.itinerary.length}d | ${r.price||'-'} | meals:${r.meals||'-'}`);}await sleep(700);}catch(e){console.log(`  ! ${u.slice(0,48)} ${e.message.slice(0,22)}`);}}
    }
  }
  await browser.close();
  if(mode!=='test'){fs.writeFileSync('packages-deep.json',JSON.stringify(out,null,2));console.log(`\n✅ ${out.length} pkgs | ${out.filter(p=>p.itinerary.length>=3).length} w/itinerary | ${out.filter(p=>p.includes.length).length} w/includes | ${out.filter(p=>p.meals).length} w/meals`);}
})().catch(e=>{console.error('FATAL',e.message);process.exit(1)});
