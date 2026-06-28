/* GB Guide — tour-package scraper v3 (sitemap-fed, schema-first)
 * 1) pulls each site's XML sitemap (index→children) for tour-DETAIL URLs
 * 2) also follows on-page tour-detail links (marketplaces)
 * 3) renders each with Chrome, extracts JSON-LD (price + aggregateRating + duration)
 * Usage: node scrape.js   (URLs in seeds.txt)
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs'), path = require('path');
const CONFIG = {
  chrome: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  seeds: 'seeds.txt', maxPagesPerSeed: 22, navTimeoutMs: 45000, politenessMs: 900,
  EXCLUDE: ['apricottours','natureadventureclub'],
  geo: /(pakistan|skardu|hunza|gilgit|naran|kaghan|fairy|deosai|baltistan|northern|chitral|swat|kalam|neelam|hushe|shimshal|khaplu|shigar|attabad|phander|shandur|kashmir|murree|nathia)/i,
  // marketplace tour-detail URL patterns (already destination-scoped by the listing page)
  detail: /(\/t\/\d|\/tour\/|\/tours\/|\/trip\/|\/p\/|\/packages?\/)/i,
  marketplaces: ['tourradar.com','bookmundi.com'],
};
const UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const host=u=>{try{return new URL(u).hostname.replace(/^www\./,'');}catch{return'';}};
const slug=u=>u.replace(/https?:\/\//,'').replace(/[^a-z0-9]+/gi,'_').slice(0,90);
const excluded=u=>CONFIG.EXCLUDE.some(d=>u.includes(d));
const arr=x=>Array.isArray(x)?x:(x==null?[]:[x]);

async function getXml(url){
  try{const r=await fetch(url,{headers:{'User-Agent':UA},signal:AbortSignal.timeout(15000)});
    if(!r.ok) return ''; return await r.text();}catch{return'';}
}
function locs(xml){ return [...xml.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/gi)].map(m=>m[1]); }
async function sitemapUrls(dom){
  const cands=[`https://www.${dom}/sitemap_index.xml`,`https://${dom}/sitemap_index.xml`,
    `https://www.${dom}/sitemap.xml`,`https://${dom}/sitemap.xml`,`https://${dom}/wp-sitemap.xml`];
  let urls=[];
  for(const c of cands){
    const xml=await getXml(c); if(!xml) continue;
    const found=locs(xml);
    if(/<sitemapindex/i.test(xml)){ // index → fetch up to 8 child maps
      for(const child of found.slice(0,8)){
        const cx=await getXml(child); urls.push(...locs(cx));
      }
    } else urls.push(...found);
    if(urls.length) break;
  }
  return [...new Set(urls)];
}
// ---- schema parse ----
function flatten(n,out=[]){ if(Array.isArray(n)){n.forEach(x=>flatten(x,out));return out;}
  if(n&&typeof n==='object'){out.push(n); if(n['@graph'])flatten(n['@graph'],out);
    for(const k of ['itemListElement','item','offers','makesOffer','hasOfferCatalog','itemOffered']) if(n[k])flatten(n[k],out);} return out;}
const TYPES=/(Product|TouristTrip|Trip|Tour|Event|Service|Offer|Vacation)/i;
function price(n){const o=n.offers?arr(n.offers)[0]:n; if(!o)return{};
  return{price:o.price||o.lowPrice||(o.priceSpecification&&o.priceSpecification.price)||'',currency:o.priceCurrency||(o.priceSpecification&&o.priceSpecification.priceCurrency)||''};}
function parseSchema(raws,url,op){const rows=[];
  for(const raw of raws){let d;try{d=JSON.parse(raw);}catch{continue;}
    for(const n of flatten(d)){const t=arr(n['@type']).join(','); if(!TYPES.test(t))continue;
      const pr=price(n),ar=n.aggregateRating||{},name=(n.name||'').toString().trim();
      if(!name&&!pr.price&&!ar.ratingValue)continue;
      rows.push({operator:op,url,type:t,name:name.slice(0,120),price:pr.price,currency:pr.currency,
        rating:ar.ratingValue||'',reviews:ar.reviewCount||ar.ratingCount||'',duration:(n.duration||'').toString(),source:'schema'});}}
  return rows;}
function textRows(d,url,op){const u=a=>[...new Set(a)];
  const p=u([...d.text.matchAll(/(?:Rs\.?|PKR|₨|USD|\$)\s?[0-9][0-9,]{3,}/gi)].map(m=>m[0].trim())).slice(0,6);
  const dur=u([...d.text.matchAll(/\b\d{1,2}\s*(?:days?|nights?)\b/gi)].map(m=>m[0].trim())).slice(0,4);
  if(!p.length&&!dur.length)return[];
  return[{operator:op,url,type:'(text)',name:d.title,price:p.join(' / '),currency:'',rating:'',reviews:'',duration:dur.join(' / '),source:'text'}];}

async function render(page,url){await page.goto(url,{waitUntil:'networkidle2',timeout:CONFIG.navTimeoutMs});await sleep(700);}
async function pull(page){return await page.evaluate(()=>({
  ld:[...document.querySelectorAll('script[type="application/ld+json"]')].map(s=>s.textContent),
  title:(document.querySelector('h1')?.innerText||document.title||'').trim().slice(0,140),
  text:document.body.innerText.replace(/\s+/g,' ').trim(),
  links:[...document.querySelectorAll('a[href]')].map(a=>a.href)}));}

(async()=>{
  const seeds=fs.readFileSync(CONFIG.seeds,'utf8').split('\n').map(s=>s.trim()).filter(s=>s&&!s.startsWith('#'));
  fs.mkdirSync('raw',{recursive:true});
  const browser=await puppeteer.launch({executablePath:CONFIG.chrome,headless:'new',args:['--no-sandbox','--disable-gpu']});
  const page=await browser.newPage(); await page.setUserAgent(UA); await page.setExtraHTTPHeaders({'Accept-Language':'en-US,en;q=0.9'});
  const all=[];
  for(const seed of seeds){
    if(excluded(seed)){console.log(`SKIP ${seed}`);continue;}
    const dom=host(seed); const isMkt=CONFIG.marketplaces.some(m=>dom.includes(m));
    console.log(`\n● ${seed}  ${isMkt?'[marketplace]':'[operator]'}`);
    let targets=new Set();
    // A) sitemap (operators mainly)
    if(!isMkt){
      const sm=await sitemapUrls(dom);
      const hit=sm.filter(u=>host(u)===dom && CONFIG.geo.test(u) && CONFIG.detail.test(u) && !excluded(u));
      hit.forEach(u=>targets.add(u));
      console.log(`  sitemap: ${sm.length} urls → ${hit.length} GB tour pages`);
    }
    // B) seed page: schema + on-page detail links
    let d; try{await render(page,seed); d=await pull(page);}catch(e){console.log(`  ! seed: ${e.message.slice(0,40)}`);}
    if(d){
      let sc=parseSchema(d.ld,seed,dom); if(!sc.length)sc=textRows(d,seed,dom); all.push(...sc);
      const onpage=[...new Set(d.links)].filter(u=>host(u)===dom && CONFIG.detail.test(u) && !excluded(u) &&
        (isMkt? true : CONFIG.geo.test(u)));   // marketplace listing already PK-scoped
      onpage.forEach(u=>targets.add(u));
    }
    const list=[...targets].slice(0,CONFIG.maxPagesPerSeed);
    console.log(`  crawling ${list.length} detail pages`);
    for(const u of list){
      try{await render(page,u); const dd=await pull(page);
        let rows=parseSchema(dd.ld,u,dom); if(!rows.length)rows=textRows(dd,u,dom); all.push(...rows);
        const r=rows.find(x=>x.rating)||rows.find(x=>x.price)||rows[0];
        if(r)console.log(`   ✓ ${r.name.slice(0,40)} | ${r.price||'-'} ${r.currency||''} | ★${r.rating||'-'}(${r.reviews||'-'})`);
        await sleep(CONFIG.politenessMs);
      }catch(e){console.log(`   ! ${u.slice(0,55)} → ${e.message.slice(0,30)}`);}
    }
  }
  await browser.close();
  const seen=new Set(),uniq=[]; for(const r of all){const k=r.operator+'|'+r.name+'|'+r.price; if(!seen.has(k)){seen.add(k);uniq.push(r);}}
  fs.writeFileSync('packages.json',JSON.stringify(uniq,null,2));
  const esc=s=>`"${String(s||'').replace(/"/g,'""')}"`,cols=['operator','name','type','duration','price','currency','rating','reviews','source','url'];
  fs.writeFileSync('packages.csv',[cols.join(','),...uniq.map(r=>cols.map(c=>esc(r[c])).join(','))].join('\n'));
  const sc=uniq.filter(r=>r.source==='schema');
  console.log(`\n✅ ${uniq.length} rows | schema ${sc.length} | w/price ${sc.filter(r=>r.price).length} | w/RATING ${sc.filter(r=>r.rating).length} → packages.csv`);
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
