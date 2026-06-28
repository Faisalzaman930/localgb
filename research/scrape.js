/* GB Guide — tour-package scraper (schema-first)
 * Renders pages with installed Chrome, then extracts machine-readable JSON-LD
 * structured data (Product/Trip/Offer/AggregateRating) for accurate prices,
 * currencies, ratings and review counts. Falls back to text regex.
 *
 * Usage: put URLs in seeds.txt (one per line) → node scrape.js
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs'), path = require('path');

const CONFIG = {
  chrome: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  seeds: 'seeds.txt',
  maxPagesPerSeed: 18,
  navTimeoutMs: 45000,
  politenessMs: 1100,
  EXCLUDE: ['apricottours', 'natureadventureclub'],
  // must reference a Pakistan/GB destination, so marketplaces don't drag in England/Vietnam tours
  pkgUrl: /(pakistan|skardu|hunza|gilgit|naran|kaghan|fairy|deosai|baltistan|northern.?area|chitral|swat|kalam|neelam|hushe|shimshal|khaplu|shigar|attabad|phander|shandur|kashmir|murree|nathia)/i,
};
const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const host = u => { try { return new URL(u).hostname.replace(/^www\./,''); } catch { return ''; } };
const slug = u => u.replace(/https?:\/\//,'').replace(/[^a-z0-9]+/gi,'_').slice(0,90);
const excluded = u => CONFIG.EXCLUDE.some(d => u.includes(d));
const arr = x => Array.isArray(x) ? x : (x == null ? [] : [x]);

// Walk arbitrary JSON-LD (handles @graph, arrays, nesting) → flat node list.
function flatten(node, out=[]) {
  if (Array.isArray(node)) { node.forEach(n => flatten(n, out)); return out; }
  if (node && typeof node === 'object') {
    out.push(node);
    if (node['@graph']) flatten(node['@graph'], out);
    for (const k of ['itemListElement','item','offers','makesOffer','hasOfferCatalog','itemOffered'])
      if (node[k]) flatten(node[k], out);
  }
  return out;
}
const TYPES = /(Product|TouristTrip|Trip|Tour|Event|Service|Offer|Vacation)/i;
function pickPrice(n) {
  const o = n.offers ? arr(n.offers)[0] : n;
  if (!o) return {};
  return {
    price: o.price || o.lowPrice || (o.priceSpecification && (o.priceSpecification.price)) || '',
    priceHigh: o.highPrice || '',
    currency: o.priceCurrency || (o.priceSpecification && o.priceSpecification.priceCurrency) || '',
  };
}
function parseSchema(rawArr, url, operator) {
  const rows = [];
  for (const raw of rawArr) {
    let data; try { data = JSON.parse(raw); } catch { continue; }
    for (const n of flatten(data)) {
      const type = arr(n['@type']).join(',');
      if (!TYPES.test(type)) continue;
      const pr = pickPrice(n);
      const ar = n.aggregateRating || {};
      const name = (n.name || '').toString().trim();
      if (!name && !pr.price && !ar.ratingValue) continue;
      rows.push({
        operator, url, type,
        name: name.slice(0, 120),
        price: pr.price, priceHigh: pr.priceHigh, currency: pr.currency,
        rating: ar.ratingValue || '', reviews: ar.reviewCount || ar.ratingCount || '',
        duration: (n.duration || '').toString(),
        source: 'schema',
      });
    }
  }
  return rows;
}

async function render(page, url) {
  await page.goto(url, { waitUntil: 'networkidle2', timeout: CONFIG.navTimeoutMs });
  await sleep(700);
}
async function pull(page) {
  return await page.evaluate(() => ({
    ld: [...document.querySelectorAll('script[type="application/ld+json"]')].map(s => s.textContent),
    title: (document.querySelector('h1')?.innerText || document.title || '').trim().slice(0,140),
    text: document.body.innerText.replace(/\s+/g,' ').trim(),
    links: [...document.querySelectorAll('a[href]')].map(a => a.href),
  }));
}
function textRows(p, url, operator) {
  const uniq = a => [...new Set(a)];
  const prices = uniq([...p.text.matchAll(/(?:Rs\.?|PKR|₨|USD|\$)\s?[0-9][0-9,]{3,}/gi)].map(m=>m[0].trim())).slice(0,6);
  const dur = uniq([...p.text.matchAll(/\b\d{1,2}\s*(?:days?|nights?)\b/gi)].map(m=>m[0].trim())).slice(0,4);
  if (!prices.length && !dur.length) return [];
  return [{ operator, url, type:'(text)', name:p.title, price:prices.join(' / '), priceHigh:'', currency:'',
            rating:'', reviews:'', duration:dur.join(' / '), source:'text' }];
}

(async () => {
  const seeds = fs.readFileSync(CONFIG.seeds,'utf8').split('\n').map(s=>s.trim()).filter(s=>s && !s.startsWith('#'));
  fs.mkdirSync('raw',{recursive:true});
  const browser = await puppeteer.launch({ executablePath: CONFIG.chrome, headless:'new', args:['--no-sandbox','--disable-gpu'] });
  const page = await browser.newPage();
  await page.setUserAgent(UA);
  await page.setExtraHTTPHeaders({ 'Accept-Language':'en-US,en;q=0.9' });
  const all = [];

  for (const seed of seeds) {
    if (excluded(seed)) { console.log(`SKIP ${seed}`); continue; }
    const dom = host(seed);
    console.log(`\n● ${seed}`);
    let p;
    try { await render(page, seed); p = await pull(page); }
    catch(e){ console.log(`  ! seed failed: ${e.message}`); continue; }
    // schema from the listing/seed page itself (often has many tours)
    let sc = parseSchema(p.ld, seed, dom);
    if (!sc.length) sc = textRows(p, seed, dom);
    all.push(...sc);
    fs.writeFileSync(path.join('raw', slug(seed)+'.html'), p.ld.join('\n\n---LD---\n\n') || '(no ld)');
    let pkgs = [...new Set(p.links)].filter(u => host(u)===dom && CONFIG.pkgUrl.test(u) && !excluded(u)).slice(0, CONFIG.maxPagesPerSeed);
    console.log(`  schema on seed: ${sc.length} | crawling ${pkgs.length} pages`);
    for (const u of pkgs) {
      try {
        await render(page, u); const d = await pull(page);
        let rows = parseSchema(d.ld, u, dom);
        if (!rows.length) rows = textRows(d, u, dom);
        all.push(...rows);
        const withP = rows.filter(r=>r.price||r.rating);
        if (withP.length) console.log(`   ✓ ${withP[0].name.slice(0,42)} | ${withP[0].price||''}${withP[0].currency? ' '+withP[0].currency:''} | ★${withP[0].rating||'-'}(${withP[0].reviews||'-'})`);
        await sleep(CONFIG.politenessMs);
      } catch(e){ console.log(`   ! ${u.slice(0,60)} → ${e.message.slice(0,40)}`); }
    }
  }
  await browser.close();

  // dedupe by operator+name+price
  const seen=new Set(), uniq=[];
  for (const r of all){ const k=r.operator+'|'+r.name+'|'+r.price; if(!seen.has(k)){seen.add(k);uniq.push(r);} }
  fs.writeFileSync('packages.json', JSON.stringify(uniq,null,2));
  const esc=s=>`"${String(s||'').replace(/"/g,'""')}"`;
  const cols=['operator','name','type','duration','price','priceHigh','currency','rating','reviews','source','url'];
  fs.writeFileSync('packages.csv', [cols.join(','), ...uniq.map(r=>cols.map(c=>esc(r[c])).join(','))].join('\n'));
  const schemaRows=uniq.filter(r=>r.source==='schema');
  console.log(`\n✅ ${uniq.length} rows (${schemaRows.length} from schema, ${schemaRows.filter(r=>r.price).length} with price, ${schemaRows.filter(r=>r.rating).length} with rating) → packages.csv`);
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
