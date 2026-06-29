const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36';
const EX=/gilgitbaltistanguide|apricottours|natureadventureclub|pakistantours\.|facebook|instagram|youtube|tripadvisor|tourradar|bookmundi|findmyadventure|getyourguide|viator|wikipedia|tripoto|google|bing|microsoft|booking\.com|daraz|olx|pinterest|linkedin|twitter|w3\.org|youtube|reddit|quora/i;
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox']});
const p=await b.newPage(); await p.setUserAgent(UA);
const queries=['skardu tour packages pakistan','hunza tour packages from islamabad','gilgit tour packages','naran kaghan tour packages','fairy meadows tour package pakistan'];
const hosts={};
for(const q of queries){
  try{
    await p.goto('https://www.bing.com/search?q='+encodeURIComponent(q),{waitUntil:'networkidle2',timeout:30000});
    await new Promise(r=>setTimeout(r,600));
    const links=await p.$$eval('li.b_algo h2 a, a[href]',as=>as.map(a=>a.href));
    for(const u of links){try{const h=new URL(u).hostname.replace(/^www\./,'');if(!EX.test(h)&&/\.(pk|com|net|org)$/.test(h))hosts[h]=(hosts[h]||0)+1;}catch{}}
  }catch(e){console.log('q fail',q,e.message.slice(0,30));}
}
const sorted=Object.entries(hosts).sort((a,b)=>b[1]-a[1]);
console.log('candidate operator domains:');
sorted.slice(0,25).forEach(([h,c])=>console.log(`  ${c}  ${h}`));
await b.close();
})();
