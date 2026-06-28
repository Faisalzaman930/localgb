/* GB Guide — tour-package scraper
 * Renders operator sites with your installed Chrome (JS executes, so prices/
 * itineraries that plain HTTP misses are captured), finds package pages,
 * and extracts structured data to packages.csv / packages.json + raw HTML.
 *
 * Usage:
 *   1) put operator URLs (homepage or /tours listing) in seeds.txt, one per line
 *   2) node scrape.js
 * Edit CONFIG below (top-5 SERP operators go in EXCLUDE so they're skipped).
 */
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  chrome: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  seeds: 'seeds.txt',
  maxPagesPerSeed: 25,        // safety cap
  navTimeoutMs: 45000,
  politenessMs: 1200,         // delay between page loads
  // Domains to skip entirely (your top-5 SERP competitors). Substring match.
  EXCLUDE: ['apricottours', 'natureadventureclub'],
  // A link is treated as a package page if its URL matches this:
  pkgUrl: /(tour|package|trip|itinerar|skardu|hunza|gilgit|naran|fairy|deosai|kaghan|baltistan|northern)/i,
};

const UA = 'Mozilla/5.0 (Macintosh) GBGuideResearchBot/1.0';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const host = u => { try { return new URL(u).hostname.replace(/^www\./,''); } catch { return ''; } };
const slug = u => u.replace(/https?:\/\//,'').replace(/[^a-z0-9]+/gi,'_').slice(0,80);
const excluded = u => CONFIG.EXCLUDE.some(d => u.includes(d));

async function render(page, url) {
  await page.goto(url, { waitUntil: 'networkidle2', timeout: CONFIG.navTimeoutMs });
  await sleep(800);
  return page;
}

// Extract package signals from the current page.
async function extract(page, url) {
  return await page.evaluate((url) => {
    const text = document.body.innerText.replace(/\s+/g, ' ').trim();
    const title = (document.querySelector('h1')?.innerText || document.title || '').trim();
    const uniq = a => [...new Set(a)];
    const prices = uniq([...text.matchAll(/(?:Rs\.?|PKR|₨)\s?[0-9][0-9,]{3,}(?:\/-)?/gi)].map(m => m[0].trim())).slice(0, 12);
    const durations = uniq([...text.matchAll(/\b\d{1,2}\s*(?:days?|nights?)(?:\s*[\/&-]\s*\d{1,2}\s*(?:days?|nights?))?/gi)].map(m => m[0].trim())).slice(0, 8);
    // crude "includes" capture
    let includes = '';
    const m = text.match(/(includ[ei][^.]{0,400})/i);
    if (m) includes = m[1].trim().slice(0, 300);
    return { url, title: title.slice(0, 140), prices, durations, includes, words: text.split(' ').length };
  }, url);
}

(async () => {
  if (!fs.existsSync(CONFIG.seeds)) { console.error(`Create ${CONFIG.seeds} with operator URLs (one per line).`); process.exit(1); }
  const seeds = fs.readFileSync(CONFIG.seeds, 'utf8').split('\n').map(s => s.trim()).filter(s => s && !s.startsWith('#'));
  fs.mkdirSync('raw', { recursive: true });
  const browser = await puppeteer.launch({ executablePath: CONFIG.chrome, headless: 'new', args: ['--no-sandbox','--disable-gpu'] });
  const page = await browser.newPage();
  await page.setUserAgent(UA);
  const results = [];

  for (const seed of seeds) {
    if (excluded(seed)) { console.log(`SKIP (excluded): ${seed}`); continue; }
    const dom = host(seed);
    console.log(`\n● Seed: ${seed}`);
    let links = [];
    try {
      await render(page, seed);
      links = await page.$$eval('a[href]', as => as.map(a => a.href));
    } catch (e) { console.log(`  ! seed failed: ${e.message}`); continue; }
    // candidate package pages on the same domain
    let pkgs = [...new Set(links)].filter(u => host(u) === dom && CONFIG.pkgUrl.test(u) && !excluded(u));
    pkgs = pkgs.slice(0, CONFIG.maxPagesPerSeed);
    console.log(`  found ${pkgs.length} candidate package pages`);
    for (const u of pkgs) {
      try {
        await render(page, u);
        const data = await extract(page, u);
        data.operator = dom;
        const html = await page.content();
        fs.writeFileSync(path.join('raw', slug(u) + '.html'), html);
        results.push(data);
        console.log(`   ✓ ${data.title || u}  | ${data.durations.join(',')||'—'} | ${data.prices.join(',')||'no price'}`);
        await sleep(CONFIG.politenessMs);
      } catch (e) { console.log(`   ! ${u} → ${e.message}`); }
    }
  }
  await browser.close();

  fs.writeFileSync('packages.json', JSON.stringify(results, null, 2));
  const esc = s => `"${String(s||'').replace(/"/g,'""')}"`;
  const csv = ['operator,title,durations,prices,includes,url',
    ...results.map(r => [r.operator, r.title, r.durations.join(' / '), r.prices.join(' / '), r.includes, r.url].map(esc).join(','))].join('\n');
  fs.writeFileSync('packages.csv', csv);
  console.log(`\n✅ ${results.length} package pages → packages.csv, packages.json, raw/*.html`);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
