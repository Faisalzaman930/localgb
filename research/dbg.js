const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
const p=await b.newPage();
await p.goto(process.argv[2],{waitUntil:'networkidle2',timeout:45000});
await new Promise(r=>setTimeout(r,800));
const info=await p.evaluate(()=>{
  const t=document.body.textContent||'';
  const days=(t.match(/day\s*0?\d{1,2}/gi)||[]).length;
  // look for accordion/itinerary containers
  const sels=['.itinerary','.tour-itinerary','[class*=itinerar]','.accordion','.elementor-tab-title','.elementor-accordion','.day','[class*=day]'];
  const hits={};
  sels.forEach(s=>{try{hits[s]=document.querySelectorAll(s).length;}catch{}});
  // grab a chunk around 'itinerary'
  const i=t.toLowerCase().indexOf('itinerary');
  const chunk=i>=0?t.slice(i,i+600).replace(/\s+/g,' '):'(no itinerary kw)';
  return {len:t.length,days,hits,chunk};
});
console.log('textContent len:',info.len,'| "day" matches:',info.days);
console.log('container counts:',JSON.stringify(info.hits));
console.log('around "itinerary":',info.chunk);
await b.close();
})();
