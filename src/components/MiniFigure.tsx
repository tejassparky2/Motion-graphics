import React from 'react';
import {filaments} from '../config';

export type FigureLook = {
  kind?: 'person' | 'dog';
  skin?: string;
  hair?: string;
  shirt?: string;
  pants?: string;
  shoes?: string;
  base?: string;
  hairStyle?: 'short' | 'long' | 'bun' | 'curly';
  glasses?: boolean;
  beard?: boolean;
  bolt?: boolean; // little brand spark on the shirt
};

type Props = {
  id: string; // unique per instance (used for clip paths)
  look?: FigureLook;
  width: number;
  /** 0..1 – how much of the figure is printed (from the bottom). 1 = finished. */
  print?: number;
  /** Show faint FDM layer lines on the printed part. */
  layerLines?: boolean;
  /** 0..1 raise the right arm to wave. */
  wave?: number;
  /** Blink amount 0..1 */
  blink?: number;
  style?: React.CSSProperties;
};

const F = filaments;

export const defaultLook: Required<FigureLook> = {
  kind: 'person',
  skin: F.t2.color,
  hair: F.t1.color,
  shirt: F.t3.color,
  pants: F.t1.color,
  shoes: F.t4.color,
  base: F.t1.color,
  hairStyle: 'short',
  glasses: false,
  beard: false,
  bolt: true,
};

const shade = (hex: string, amt: number) => {
  const n = parseInt(hex.slice(1), 16);
  const c = (v: number) => Math.max(0, Math.min(255, Math.round(v + amt * 255)));
  const r = c((n >> 16) & 255);
  const g = c((n >> 8) & 255);
  const b = c(n & 255);
  return `rgb(${r},${g},${b})`;
};

const Base: React.FC<{color: string}> = ({color}) => (
  <g>
    <path d="M70 548 L70 572 A130 26 0 0 0 330 572 L330 548 Z" fill={shade(color, -0.06)} />
    <path d="M70 560 A130 26 0 0 0 330 560" stroke={F.t4.color} strokeWidth={5} fill="none" />
    <ellipse cx={200} cy={548} rx={130} ry={26} fill={shade(color, 0.08)} />
  </g>
);

const Person: React.FC<{look: Required<FigureLook>; wave: number; blink: number}> = ({look, wave, blink}) => {
  const armAngle = -20 - wave * 115; // degrees, pivot at shoulder
  const eyeRy = 26 * (1 - blink * 0.9);
  return (
    <g>
      {/* back hair (long / bun) */}
      {look.hairStyle === 'long' && (
        <path d="M66 200 C56 300 60 380 92 410 C120 420 150 400 150 370 L150 210 Z M334 200 C344 300 340 380 308 410 C280 420 250 400 250 370 L250 210 Z" fill={look.hair} />
      )}
      {look.hairStyle === 'bun' && <circle cx={200} cy={72} r={46} fill={look.hair} />}

      {/* shoes */}
      <ellipse cx={163} cy={532} rx={34} ry={16} fill={look.shoes} />
      <ellipse cx={237} cy={532} rx={34} ry={16} fill={look.shoes} />
      {/* legs */}
      <rect x={140} y={430} width={48} height={100} rx={18} fill={look.pants} />
      <rect x={212} y={430} width={48} height={100} rx={18} fill={look.pants} />
      {/* left arm */}
      <path d="M150 360 Q118 392 112 432" stroke={look.shirt} strokeWidth={36} strokeLinecap="round" fill="none" />
      <circle cx={110} cy={444} r={19} fill={look.skin} />
      {/* torso */}
      <path d="M138 338 Q200 318 262 338 L278 452 Q200 474 122 452 Z" fill={look.shirt} />
      {look.bolt && <path d="M206 372 L184 410 L200 410 L192 440 L220 398 L204 398 L214 372 Z" fill={F.t1.color} />}
      {/* right arm (waves) */}
      <g transform={`rotate(${armAngle} 250 356)`}>
        <path d="M250 356 L250 432" stroke={look.shirt} strokeWidth={36} strokeLinecap="round" fill="none" />
        <circle cx={250} cy={446} r={19} fill={look.skin} />
      </g>
      {/* ears */}
      <circle cx={66} cy={222} r={22} fill={look.skin} />
      <circle cx={334} cy={222} r={22} fill={look.skin} />
      {/* head */}
      <circle cx={200} cy={206} r={138} fill={look.skin} />
      {/* beard */}
      {look.beard && (
        <path d="M86 250 C92 330 150 350 200 350 C250 350 308 330 314 250 C290 290 260 300 200 302 C140 300 110 290 86 250 Z" fill={look.hair} />
      )}
      {/* front hair */}
      {look.hairStyle === 'curly' ? (
        <g fill={look.hair}>
          {[
            [78, 170, 40], [110, 120, 44], [160, 88, 46], [220, 82, 48], [280, 108, 44], [318, 160, 40],
            [140, 130, 34], [250, 128, 34], [200, 120, 36],
          ].map(([x, y, r], i) => (
            <circle key={i} cx={x} cy={y} r={r} />
          ))}
        </g>
      ) : (
        <path
          d="M62 222 C50 110 130 58 205 62 C290 62 356 116 338 222 C326 186 304 160 276 150 C262 170 236 180 206 176 C214 164 216 152 214 140 C188 166 146 176 112 172 C92 186 74 202 62 222 Z"
          fill={look.hair}
        />
      )}
      {/* eyebrows */}
      <path d="M126 186 Q148 176 170 184" stroke={look.hair} strokeWidth={8} strokeLinecap="round" fill="none" />
      <path d="M230 184 Q252 176 274 186" stroke={look.hair} strokeWidth={8} strokeLinecap="round" fill="none" />
      {/* eyes */}
      <ellipse cx={148} cy={232} rx={20} ry={eyeRy} fill={F.t1.color} />
      <ellipse cx={252} cy={232} rx={20} ry={eyeRy} fill={F.t1.color} />
      {blink < 0.5 && (
        <>
          <circle cx={156} cy={221} r={7} fill="#FFFFFF" />
          <circle cx={260} cy={221} r={7} fill="#FFFFFF" />
        </>
      )}
      {look.glasses && (
        <g stroke={F.t1.color} strokeWidth={7} fill="none">
          <circle cx={148} cy={232} r={40} />
          <circle cx={252} cy={232} r={40} />
          <path d="M188 228 Q200 220 212 228" />
        </g>
      )}
      {/* cheeks */}
      <ellipse cx={116} cy={276} rx={22} ry={12} fill={F.t4.color} opacity={0.55} />
      <ellipse cx={284} cy={276} rx={22} ry={12} fill={F.t4.color} opacity={0.55} />
      {/* smile */}
      <path d="M176 284 Q200 316 224 284 Z" fill={F.t4.color} stroke={F.t1.color} strokeWidth={6} strokeLinejoin="round" />
    </g>
  );
};

const Dog: React.FC<{blink: number}> = ({blink}) => {
  const tan = '#E3A869';
  const brown = '#8A5A3B';
  const cream = '#F8E6CC';
  const eyeR = 15 * (1 - blink * 0.85);
  return (
    <g>
      <ellipse cx={200} cy={458} rx={104} ry={80} fill={tan} />
      <ellipse cx={200} cy={478} rx={60} ry={52} fill={cream} />
      <ellipse cx={150} cy={530} rx={30} ry={16} fill={tan} />
      <ellipse cx={250} cy={530} rx={30} ry={16} fill={tan} />
      <path d="M298 452 Q350 420 340 380" stroke={tan} strokeWidth={22} strokeLinecap="round" fill="none" />
      <ellipse cx={104} cy={262} rx={40} ry={78} fill={brown} transform="rotate(18 104 262)" />
      <ellipse cx={296} cy={262} rx={40} ry={78} fill={brown} transform="rotate(-18 296 262)" />
      <circle cx={200} cy={280} r={112} fill={tan} />
      <ellipse cx={200} cy={330} rx={56} ry={40} fill={cream} />
      <ellipse cx={200} cy={308} rx={18} ry={12} fill={F.t1.color} />
      <path d="M200 320 L200 340 M180 340 Q200 356 220 340" stroke={F.t1.color} strokeWidth={6} strokeLinecap="round" fill="none" />
      <ellipse cx={200} cy={356} rx={12} ry={14} fill={F.t4.color} />
      <ellipse cx={156} cy={262} rx={15} ry={eyeR} fill={F.t1.color} />
      <ellipse cx={244} cy={262} rx={15} ry={eyeR} fill={F.t1.color} />
      {blink < 0.5 && (
        <>
          <circle cx={161} cy={255} r={5} fill="#fff" />
          <circle cx={249} cy={255} r={5} fill="#fff" />
        </>
      )}
      <path d="M150 390 Q200 410 250 390" stroke={F.t4.color} strokeWidth={14} strokeLinecap="round" fill="none" />
      <circle cx={200} cy={410} r={11} fill={F.t3.color} />
    </g>
  );
};

/** Chibi "Mini Me" figurine – big head, big eyes (baby-schema proportions). */
export const MiniFigure: React.FC<Props> = ({id, look, width, print = 1, layerLines = false, wave = 0, blink = 0, style}) => {
  const L = {...defaultLook, ...look};
  const top = 50;
  const bottom = 600;
  const printY = bottom - (bottom - top) * Math.max(0, Math.min(1, print));
  const body = L.kind === 'dog' ? <Dog blink={blink} /> : <Person look={L} wave={wave} blink={blink} />;
  const full = (
    <g>
      <Base color={L.base} />
      {body}
    </g>
  );
  return (
    <svg viewBox="0 0 400 600" width={width} height={width * 1.5} style={{overflow: 'visible', ...style}}>
      <defs>
        <clipPath id={`${id}-done`}>
          <rect x={-50} y={printY} width={500} height={700} />
        </clipPath>
        <clipPath id={`${id}-todo`}>
          <rect x={-50} y={-100} width={500} height={printY + 100} />
        </clipPath>
        <pattern id={`${id}-layers`} width={8} height={5} patternUnits="userSpaceOnUse">
          <rect width={8} height={1.4} fill="rgba(0,0,0,0.13)" />
        </pattern>
        <mask id={`${id}-mask`}>
          <g style={{filter: 'brightness(0) invert(1)'}}>{full}</g>
        </mask>
      </defs>
      {print < 1 && (
        <g clipPath={`url(#${id}-todo)`} opacity={0.22} style={{filter: 'grayscale(1) brightness(1.8)'}}>
          {full}
        </g>
      )}
      <g clipPath={print < 1 ? `url(#${id}-done)` : undefined}>
        {full}
        {layerLines && <rect x={0} y={0} width={400} height={600} fill={`url(#${id}-layers)`} mask={`url(#${id}-mask)`} />}
      </g>
    </svg>
  );
};

/** Which filament colours exist at a given height of the default figure (for tool-swap animation). */
export const colorsAtHeight = (y: number): string[] => {
  if (y > 540) return [F.t1.color, F.t4.color]; // base + stripe
  if (y > 515) return [F.t4.color, F.t1.color]; // shoes + legs
  if (y > 452) return [F.t1.color, F.t2.color]; // legs + hands
  if (y > 340) return [F.t3.color, F.t2.color, F.t1.color]; // shirt, hands, bolt
  if (y > 250) return [F.t2.color, F.t4.color, F.t1.color]; // face, cheeks, mouth
  if (y > 170) return [F.t2.color, F.t1.color]; // face, eyes, hair sides
  return [F.t1.color, F.t2.color]; // hair
};
