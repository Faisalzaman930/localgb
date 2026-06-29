const puppeteer=require('puppeteer-core');
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const ops=['pakistantravelplaces.com','narankaghantours.com','baltistantours.com','hunzaadventuretours.com','atp.com.pk','pakistanguidedtours.com','hunzaexplorers.com'];
const paths=['/','/reviews/','/testimonials/','/about/','/about-us/','/reviews','/testimonials'];
const arr=x=>Array.isArray(x)?x:(x==null?[]:[x]);
function flat(n,o=[]){if(Array.isArray(n)){n.forEach(x=>flat(x,o));return o;}if(n&&typeof n==='object'){o.push(n);if(n['@graph'])flat(n['@graph'],o);}return o;}
(async()=>{
const b=await puppeteer.launch({executablePath:CHROME,headless:'new',args:['--no-sandbox','--disable-gpu']});
const p=await b.newPage();await p.setUserAgent('Mozilla/5.0 Chrome/126');
for(const dom of ops){
  let found=null;
  for(const path of paths){
    const url='https://www.'+dom+path;
    try{
      await p.goto(url,{waitUntil:'domcontentloaded',timeout:25000});
      await new Promise(r=>setTimeout(r,600));
      const lds=await p.$$eval('script[type="application/ld+json"]',ss=>ss.map(s=>s.textContent));
      for(const raw of lds){let d;try{d=JSON.parse(raw);}catch{continue;}
        for(const n of flat(d)){
          const ar=n.aggregateRating;
          if(ar&&(ar.ratingValue||ar.ratingCount||ar.reviewCount)){found={url,rating:ar.ratingValue,count:ar.reviewCount||ar.ratingCount,type:arr(n['@type']).join(',')};break;}
        }
        if(found)break;
      }
    }catch(e){}
    if(found)break;
  }
  console.log(found? `  ★ ${found.rating} (${found.count})  ${dom}  [${found.type}]  ${found.url}` : `  —  no rating schema  ${dom}`);
}
await b.close();
})().catch(e=>{console.error(e.message);process.exit(1)});
