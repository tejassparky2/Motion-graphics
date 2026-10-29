// The rat video's first 6.6 s (row 77, toxo_rat) remade in Remotion + GSAP, with the same voice, music and word
// times as the pycairo render, to compare the two side by side. Layout follows videos/toxo_rat.py.
import React, {useLayoutEffect, useRef} from 'react';
import {
  AbsoluteFill, Audio, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig,
} from 'remotion';
import {CameraMotionBlur} from '@remotion/motion-blur';
import {StrikeThrough} from '@remotion/rough-notation';
import gsap from 'gsap';
import {DrawSVGPlugin} from 'gsap/DrawSVGPlugin';
import {CustomEase} from 'gsap/CustomEase';
import {CustomWiggle} from 'gsap/CustomWiggle';
import data from './words.json';

gsap.registerPlugin(DrawSVGPlugin, CustomEase, CustomWiggle);
CustomWiggle.create('shiver', {wiggles: 8, type: 'easeOut'});

const OUTLINE = '#2b1d16';
const RED = '#ff2b2b';
const PINK = '#ffa8b8';
const GERM = '#7ae86a';

// ---- fonts (the channel's own TTFs): hold the render until they are in
const fontHandle = delayRender('fonts');
Promise.all(
  [['Anton', 'Anton-Regular.ttf'], ['Fredoka', 'Fredoka-Bold.ttf'], ['Luckiest Guy', 'LuckiestGuy-Regular.ttf']].map(
    ([family, file]) => new FontFace(family, `url(${staticFile('fonts/' + file)})`).load().then((f) => {
      (document.fonts as any).add(f);
    }),
  ),
).then(() => continueRender(fontHandle));

// ---- word times from the Python timeline
type Word = {beat: string; word: string; start: number; end: number};
const WORDS = data.words as Word[];
const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9']/g, '');
const at = (key: string, nth = 1, end = false) => {
  let seen = 0;
  for (const w of WORDS) {
    if (norm(w.word).startsWith(norm(key)) && ++seen === nth) return end ? w.end : w.start;
  }
  throw new Error(`no word ${key}`);
};

// 1-3 word caption chunks, broken at sentence ends (as motion/captions.py does)
const CHUNKS: Word[][] = [];
for (const w of WORDS) {
  const last = CHUNKS[CHUNKS.length - 1];
  if (!last || last.length >= 3 || /[.?!,]$/.test(last[last.length - 1].word)) CHUNKS.push([w]);
  else last.push(w);
}

const textStyle = (size: number, color: string, font: string, stroke: number): React.CSSProperties => ({
  fontFamily: font, fontSize: size, color, WebkitTextStroke: `${stroke}px #000`, paintOrder: 'stroke fill',
  textShadow: `${size * 0.03}px ${size * 0.06}px 0 rgba(0,0,0,0.6)`, lineHeight: 1, whiteSpace: 'nowrap',
});

// v1: GSAP only. v2 (RatHookFX): + Remotion's motion blur and a hand-drawn (rough-notation) strike-through.
export const RatHook: React.FC = () => (
  <AbsoluteFill>
    <Audio src={staticFile('rat_open.wav')} />
    <RatScene rough={false} />
  </AbsoluteFill>
);

export const RatHookFX: React.FC = () => (
  <AbsoluteFill>
    <Audio src={staticFile('rat_open.wav')} />
    <CameraMotionBlur samples={6} shutterAngle={180}>
      <RatScene rough />
    </CameraMotionBlur>
  </AbsoluteFill>
);

const RatScene: React.FC<{rough: boolean}> = ({rough}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const root = useRef<HTMLDivElement>(null);
  const tl = useRef<gsap.core.Timeline | null>(null);

  // Build one paused GSAP timeline, then seek it to the current frame on every render: deterministic frames.
  useLayoutEffect(() => {
    const q = gsap.utils.selector(root);
    const cam = {z: 1, fx: 360, fy: 640};
    const camEl = q('#cam')[0];
    const setCam = () => camEl.setAttribute('transform',
      `translate(360 640) scale(${cam.z}) translate(${-cam.fx} ${-cam.fy})`);
    const tail = {sw: 0};
    const setTail = () => q('.tail').forEach((p: Element) =>
      p.setAttribute('d', `M-80,-30 Q-160,${-10 + tail.sw} -232,${-40 - tail.sw}`));
    const zoom = at('Something');
    const r1end = WORDS.filter((w) => w.beat === 'r1').slice(-1)[0].end;

    // gsap.context scopes every selector string to this copy of the scene (motion blur renders several copies)
    const ctx = gsap.context(() => {
    const m = gsap.timeline({paused: true, defaults: {ease: 'power2.out'}});
    // camera: slow push-in, then a fast zoom into the rat's head on "Something inside it"
    m.to(cam, {z: 1.04, duration: zoom, ease: 'none', onUpdate: setCam}, 0)
      .to(cam, {z: 1.9, fx: 330, fy: 690, duration: 0.6, ease: 'power3.inOut', onUpdate: setCam}, zoom);
    // the rat walks in, legs and tail going, then stops at the end of the girl's line
    m.fromTo('#rat', {x: 130}, {x: 250, duration: r1end, ease: 'power1.inOut'}, 0)
      .fromTo('#legF', {x: -14}, {x: 14, duration: 0.22, ease: 'sine.inOut', yoyo: true, repeat: Math.floor(r1end / 0.22)}, 0)
      .fromTo('#legB', {x: 14}, {x: -14, duration: 0.22, ease: 'sine.inOut', yoyo: true, repeat: Math.floor(r1end / 0.22)}, 0)
      .fromTo('#ratBody', {y: 0}, {y: -4, duration: 0.11, ease: 'sine.inOut', yoyo: true, repeat: Math.floor(r1end / 0.11)}, 0)
      .fromTo(tail, {sw: -12}, {sw: 12, duration: 0.5, ease: 'sine.inOut', yoyo: true, repeat: 13, onUpdate: setTail}, 0)
      .to('#whiskers', {rotation: 6, svgOrigin: '166 -44', duration: 0.4, ease: 'shiver'}, at('cat'))
      .to('#whiskers', {rotation: 6, svgOrigin: '166 -44', duration: 0.4, ease: 'shiver'}, at('eat'));
    // the germ lights up in its head and pulses
    m.fromTo('#glow', {scale: 0, opacity: 0, svgOrigin: '100 -64'},
      {scale: 1, opacity: 1, duration: 0.7, ease: 'elastic.out(1, 0.45)'}, zoom + 0.3)
      .to('#glow', {scale: 1.15, svgOrigin: '100 -64', duration: 0.15, yoyo: true, repeat: 7, ease: 'sine.inOut'}, zoom + 1.0);
    // the cat's eyes: blink, pupils widen when the girl says "cat", narrow on "eat"
    m.to('#eyes', {scaleY: 0.08, svgOrigin: '0 0', duration: 0.08, yoyo: true, repeat: 1}, 1.0)
      .to('.pupil', {attr: {rx: 15}, duration: 0.35, ease: 'back.out(3)'}, at('cat'))
      .to('#eyes', {scaleY: 0.08, svgOrigin: '0 0', duration: 0.08, yoyo: true, repeat: 1}, 4.6)
      .to('#eyes', {scaleY: 0.5, svgOrigin: '0 0', duration: 0.25}, at('eat'))
      .to('.pupil', {attr: {rx: 4}, duration: 0.25}, at('eat'));
    // hook: AFRAID pops in letter by letter on "straight", struck through on "brave", then shivers; gone after it
    m.fromTo('.big', {scale: 0, y: 50, rotation: -12}, {scale: 1, y: 0, rotation: 0, duration: 0.45,
      ease: 'back.out(2.6)', stagger: 0.04}, at('straight'))
    if (q('#strike').length) m.fromTo('#strike', {drawSVG: '0%'}, {drawSVG: '100%', duration: 0.28, ease: 'power3.in'}, at('brave'));
    m.to('#bigRow', {x: 8, duration: 0.5, ease: 'shiver'}, at('brave') + 0.28)
      .to('#hook', {opacity: 0, y: -30, duration: 0.25, ease: 'power2.in'}, at('brave', 1, true) + 0.3);
    // "IT WANTS THIS" tag
    m.fromTo('#want', {scale: 0, rotation: -20}, {scale: 1, rotation: -4, duration: 0.6, ease: 'elastic.out(1, 0.5)'},
      at('eat'));
    tl.current = m;
    }, root);
    return () => ctx.revert();
  }, []);

  useLayoutEffect(() => {
    tl.current?.seek(t, false);
  }, [t]);

  // captions: React, straight from the word times
  const chunk = CHUNKS.find((c, i) => {
    const next = CHUNKS[i + 1];
    const stop = next && next[0].start - c[c.length - 1].end < 0.5 ? next[0].start : c[c.length - 1].end + 0.25;
    return t >= c[0].start - 0.02 && t < stop;
  });
  const pop = chunk ? spring({frame: frame - Math.round(chunk[0].start * fps), fps, config: {damping: 11, mass: 0.5}}) : 0;
  const chip = Math.min(1, Math.max(0, (t - 0.3) / 0.25)) * (t < 2.4 ? 1 : Math.max(0, 1 - (t - 2.4) / 0.25));

  return (
    <AbsoluteFill ref={root} style={{background: '#f0e4cc'}}>
      <svg width={720} height={1280} viewBox="0 0 720 1280" style={{position: 'absolute'}}>
        <defs>
          <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#f6ecd8" /><stop offset="1" stopColor="#e6d8bc" />
          </linearGradient>
          <radialGradient id="centre"><stop offset="0" stopColor="#fff" stopOpacity="0.22" /><stop offset="1" stopColor="#fff" stopOpacity="0" /></radialGradient>
          <radialGradient id="patch"><stop offset="0" stopColor="#141019" stopOpacity="0.92" /><stop offset="0.6" stopColor="#141019" stopOpacity="0.6" /><stop offset="1" stopColor="#141019" stopOpacity="0" /></radialGradient>
          <radialGradient id="body" cx="0.42" cy="0.3" r="0.8"><stop offset="0" stopColor="#d6d2da" /><stop offset="1" stopColor="#86828c" /></radialGradient>
          <radialGradient id="head" cx="0.5" cy="0.35" r="0.8"><stop offset="0" stopColor="#dedae2" /><stop offset="1" stopColor="#9a96a0" /></radialGradient>
          <radialGradient id="germGlow"><stop offset="0" stopColor="#8aff6a" stopOpacity="0.7" /><stop offset="1" stopColor="#8aff6a" stopOpacity="0" /></radialGradient>
          <radialGradient id="eyeFill" cx="0.5" cy="0.4"><stop offset="0" stopColor="#fff07a" /><stop offset="1" stopColor="#ffb21a" /></radialGradient>
          <radialGradient id="vig" r="0.75"><stop offset="0.55" stopColor="#000" stopOpacity="0" /><stop offset="1" stopColor="#000" stopOpacity="0.32" /></radialGradient>
          <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7" /></filter>
        </defs>
        <rect width="720" height="1280" fill="url(#bg)" />
        <ellipse cx="360" cy="614" rx="420" ry="420" fill="url(#centre)" />
        <g id="cam">
          <g transform="translate(590 560)">
            <ellipse rx="230" ry="170" fill="url(#patch)" />
            <g id="eyes">
              {[-60, 60].map((ex) => (
                <g key={ex} transform={`translate(${ex} 0)`}>
                  <path d="M-46,0 C-20,-38 20,-38 46,0 C20,38 -20,38 -46,0Z" fill="url(#eyeFill)" stroke={OUTLINE} strokeWidth={4} />
                  <ellipse className="pupil" rx="7" ry="30" fill="#111" />
                  <circle cx="-14" cy="-12" r="5" fill="#fff" opacity="0.85" />
                </g>
              ))}
            </g>
          </g>
          <g id="rat" transform="translate(130 800)">
            <g transform="scale(1.45)">
              <ellipse cx="0" cy="4" rx="120" ry="12" fill="#000" opacity="0.16" filter="url(#soft)" />
              <path className="tail" d="M-80,-30 Q-160,-10 -232,-40" fill="none" stroke={OUTLINE} strokeWidth={17} strokeLinecap="round" />
              <path className="tail" d="M-80,-30 Q-160,-10 -232,-40" fill="none" stroke={PINK} strokeWidth={9} strokeLinecap="round" />
              <ellipse id="legB" cx="-50" cy="-8" rx="26" ry="13" fill={PINK} stroke={OUTLINE} strokeWidth={4} />
              <ellipse id="legF" cx="52" cy="-8" rx="26" ry="13" fill={PINK} stroke={OUTLINE} strokeWidth={4} />
              <g id="ratBody">
                <ellipse cx="-5" cy="-55" rx="100" ry="56" fill="url(#body)" stroke={OUTLINE} strokeWidth={6} />
                <path d="M-70,-82 C-40,-100 10,-104 40,-96" fill="none" stroke="#fff" strokeOpacity="0.35" strokeWidth={8} strokeLinecap="round" />
                <path d="M50,-96 C85,-100 140,-82 170,-60 C186,-50 182,-38 165,-33 C140,-26 92,-24 58,-30 C40,-40 38,-88 50,-96Z"
                  fill="url(#head)" stroke={OUTLINE} strokeWidth={6} strokeLinejoin="round" />
                <ellipse cx="80" cy="-102" rx="28" ry="32" fill="#b0acb6" stroke={OUTLINE} strokeWidth={5} />
                <ellipse cx="82" cy="-99" rx="16" ry="20" fill={PINK} />
                <g id="glow" opacity="0">
                  <circle cx="100" cy="-64" r="60" fill="url(#germGlow)" />
                  <ellipse cx="100" cy="-64" rx="13" ry="8" transform="rotate(28 100 -64)" fill={GERM} stroke={OUTLINE} strokeWidth={3} />
                </g>
                <ellipse cx="128" cy="-68" rx="9" ry="10" fill="#1b1b1f" />
                <circle cx="131" cy="-72" r="3" fill="#fff" />
                <ellipse cx="180" cy="-47" rx="9" ry="8" fill={PINK} stroke={OUTLINE} strokeWidth={3} />
                <g id="whiskers">
                  {[-1, 0, 1].map((k) => (
                    <line key={k} x1="166" y1="-44" x2="220" y2={-48 + k * 13} stroke={OUTLINE} strokeWidth={2.5} strokeLinecap="round" />
                  ))}
                </g>
              </g>
            </g>
          </g>
        </g>
        <rect width="720" height="1280" fill="url(#vig)" />
      </svg>

      {/* series chip */}
      <div style={{position: 'absolute', left: 36, top: 34, transform: `scale(${chip})`, transformOrigin: 'left center',
        background: 'rgba(18,18,26,0.72)', borderRadius: 21, padding: '6px 17px', color: '#fff',
        fontFamily: 'Fredoka', fontSize: 26}}>Interestingly Strange</div>

      {/* two-tier hook */}
      <div id="hook" style={{position: 'absolute', top: 152, width: 720, textAlign: 'center'}}>
        <div style={textStyle(46, '#fff', 'Anton', 6)}>THIS RAT IS NOT</div>
        <div id="bigRow" style={{position: 'relative', marginTop: 4, display: 'inline-block'}}>
          {rough ? (
            <StrikeThrough color={RED} strokeWidth={13} iterations={2} seed={4}
              progress={interpolate(t, [at('brave'), at('brave') + 0.35], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}>
              {'AFRAID'.split('').map((c, i) => (
                <span key={i} className="big" style={{...textStyle(150, RED, 'Anton', 18), display: 'inline-block',
                  transform: 'scale(0)'}}>{c}</span>
              ))}
            </StrikeThrough>
          ) : 'AFRAID'.split('').map((c, i) => (
            <span key={i} className="big" style={{...textStyle(150, RED, 'Anton', 18), display: 'inline-block',
              transform: 'scale(0)'}}>{c}</span>
          ))}
          {!rough && <svg width="560" height="200" viewBox="0 0 560 200" style={{position: 'absolute', left: '50%', top: 0,
            marginLeft: -280, overflow: 'visible'}}>
            <path id="strike" d="M20,112 L540,84" stroke={RED} strokeWidth={17} strokeLinecap="round" fill="none"
              style={{filter: 'drop-shadow(0 3px 0 rgba(0,0,0,0.5))'}} />
          </svg>}
        </div>
      </div>

      {/* "IT WANTS THIS" */}
      <div id="want" style={{position: 'absolute', top: 430, width: 720, textAlign: 'center', transform: 'scale(0)'}}>
        <span style={textStyle(44, RED, 'Luckiest Guy', 9)}>IT WANTS THIS</span>
      </div>

      {/* captions */}
      {chunk && (
        <div style={{position: 'absolute', top: 852, width: 720, textAlign: 'center',
          transform: `scale(${0.6 + 0.4 * pop})`}}>
          {chunk.map((w, i) => (
            <span key={i} style={{...textStyle(58, t >= w.start ? '#ffd84d' : '#fff', 'Fredoka', 11),
              margin: '0 8px'}}>{w.word}</span>
          ))}
        </div>
      )}
    </AbsoluteFill>
  );
};
