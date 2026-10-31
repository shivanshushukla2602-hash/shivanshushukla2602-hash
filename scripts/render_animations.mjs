/** Rasterize original SVG frames through Chrome. No photo pixels are edited. */
import {chromium} from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(root,'preview/rendered-v2');fs.mkdirSync(output,{recursive:true});
const executablePath=process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const browser=await chromium.launch({executablePath,headless:true});
try{
 const page=await browser.newPage({deviceScaleFactor:1});
 for(const [name,width,height] of [['header',1200,510],['header-mobile',600,660],['lab',1200,450],['lab-mobile',600,620]]){
  await page.setViewportSize({width,height});
  for(let i=0;i<72;i++){
   const frame=String(i).padStart(3,'0');const svg=fs.readFileSync(path.join(root,'preview/frames-v2',`${name}-${frame}.svg`),'utf8');
   await page.setContent(`<!DOCTYPE html><html><head><style>html,body{margin:0;width:${width}px;height:${height}px;background:#070c1b}svg{display:block}</style></head><body>${svg}</body></html>`,{waitUntil:'load'});
   await page.screenshot({path:path.join(output,`${name}-${frame}.png`)});
  }
  console.log(`Rendered ${name}: 72 frames`);
 }
}finally{await browser.close()}
