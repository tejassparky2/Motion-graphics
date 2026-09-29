// Render selected frames as PNGs for a quick visual check:  node scripts/stills.mjs out/stills 50 200 400
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';

const [outDir, ...frames] = process.argv.slice(2);
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const browserExecutable = process.env.REMOTION_BROWSER || null;
const composition = await selectComposition({serveUrl, id: 'MiniMeAd', browserExecutable});
for (const f of frames) {
  const output = path.join(outDir, `f${String(f).padStart(4, '0')}.png`);
  await renderStill({composition, serveUrl, output, frame: Number(f), browserExecutable, overwrite: true});
  console.log('wrote', output);
}
