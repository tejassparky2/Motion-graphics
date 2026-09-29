import '@fontsource/fredoka/500.css';
import '@fontsource/fredoka/600.css';
import '@fontsource/fredoka/700.css';
import '@fontsource/nunito/700.css';
import '@fontsource/nunito/800.css';
import '@fontsource/nunito/900.css';
import {continueRender, delayRender} from 'remotion';

const handle = delayRender('Loading fonts');
const faces = ['500 40px Fredoka', '600 40px Fredoka', '700 40px Fredoka', '700 40px Nunito', '800 40px Nunito', '900 40px Nunito'];
Promise.all(faces.map((f) => document.fonts.load(f)))
  .then(() => document.fonts.ready)
  .then(() => continueRender(handle))
  .catch(() => continueRender(handle));
