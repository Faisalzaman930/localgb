/* Operator ratings via Google Places API (New) — Text Search.
 * One call per operator → rating + review count + website + address.
 * Key is read from env GOOGLE_MAPS_KEY (never hard-coded / committed).
 * Usage: GOOGLE_MAPS_KEY=$(cat .key) node ratings.js
 */
const fs = require('fs');
const KEY = process.env.GOOGLE_MAPS_KEY;
if (!KEY) { console.error('Set GOOGLE_MAPS_KEY (e.g. GOOGLE_MAPS_KEY=$(cat .key) node ratings.js)'); process.exit(1); }
const ops = fs.readFileSync('operators.txt','utf8').split('\n').map(s=>s.trim()).filter(s=>s && !s.startsWith('#'));
const FIELDS = 'places.displayName,places.rating,places.userRatingCount,places.formattedAddress,places.id,places.websiteUri';
(async () => {
  const rows = [];
  for (const q of ops) {
    try {
      const r = await fetch('https://places.googleapis.com/v1/places:searchText', {
        method: 'POST',
        headers: { 'Content-Type':'application/json', 'X-Goog-Api-Key': KEY, 'X-Goog-FieldMask': FIELDS },
        body: JSON.stringify({ textQuery: q, regionCode: 'PK' }),
      });
      const j = await r.json();
      if (j.error) { console.log(`! API error: ${j.error.message}`); if(j.error.status==='PERMISSION_DENIED'){console.log('  → enable "Places API (New)" + check key restrictions'); process.exit(1);} continue; }
      const p = (j.places || [])[0];
      if (p) {
        rows.push({ query:q, name:p.displayName?.text||'', rating:p.rating||'', reviews:p.userRatingCount||'', site:p.websiteUri||'', addr:p.formattedAddress||'' });
        console.log(`  ★${p.rating||'-'} (${p.userRatingCount||0})  ${p.displayName?.text||q}`);
      } else { rows.push({query:q,name:'',rating:'',reviews:'',site:'',addr:''}); console.log(`  —  no match: ${q}`); }
    } catch(e){ console.log(`  ! ${q}: ${e.message}`); }
    await new Promise(r=>setTimeout(r,300));
  }
  const esc = s => `"${String(s||'').replace(/"/g,'""')}"`;
  fs.writeFileSync('ratings.csv', ['query,name,rating,reviews,site,addr',
    ...rows.map(r=>[r.query,r.name,r.rating,r.reviews,r.site,r.addr].map(esc).join(','))].join('\n'));
  console.log(`\n✅ ${rows.filter(r=>r.rating).length}/${rows.length} matched with ratings → ratings.csv`);
})();
