// Runtime render checks with a minimal DOM stub; not a substitute for browser visual QA.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const elements=new Map();function element(k){if(!elements.has(k))elements.set(k,{innerHTML:'',textContent:'',value:'',hidden:false,focus(){},setSelectionRange(){}});return elements.get(k)}
const ctx={window:{},document:{querySelector:element,documentElement:{},querySelectorAll:()=>[],addEventListener(){}},location:{search:''},URLSearchParams,history:{pushState(a,b,url){ctx.location.search=url}},console};vm.createContext(ctx);
for(const f of ['data.js','content.js','app.js'])vm.runInContext(fs.readFileSync(__dirname+'/'+f,'utf8'),ctx);
function run(s){return vm.runInContext(s,ctx)}
assert.equal(run('filtered().length'),500);assert.equal((element('#tbody').innerHTML.match(/<tr>/g)||[]).length,500);
for(const category of ['conventional','alternative','one_sided','unresolved']){run(`update({q:'',cat:'${category}',checked:'',eg:'',zg:''})`);let n=run('filtered().length');assert.equal(n,run(`D.filter(r=>r.category==='${category}').length`));assert.equal(run("count(filtered(),'en_generic').reduce((a,x)=>a+x[1],0)"),n);assert.equal(run("count(filtered(),'category').reduce((a,x)=>a+x[1],0)"),n)}
run("update({cat:'',checked:'yes'})");assert.equal(run('filtered().length'),50);assert.equal((element('#tbody').innerHTML.match(/<tr>/g)||[]).length,50);
run("update({checked:'',q:'ROAD'})");assert(run('filtered().length')>0);assert(run("filtered().every(r=>(r.source_text+' '+r.target_text).toLowerCase().includes('road'))"));
run("update({q:'',eg:'ROAD',zg:'道'})");assert(run("filtered().every(r=>r.en_generic==='ROAD'&&r.zh_generic==='道')"));let n=run('filtered().length');run('read();render()');assert.equal(run('filtered().length'),n);
for(const page of ['report','codebook','ai'])for(const lang of ['en','zh','zh-Hans']){run(`update({page:'${page}',lang:'${lang}'})`);assert(element('#document').innerHTML.length>500)}
console.log('PASS: 500 records, category counts, 50 human-checked records, search, paired filtering, URL restoration, all three language variants. Browser visual QA not available.');
