import React from 'react';
import {interpolate, useCurrentFrame, Easing} from 'remotion';
import {filaments, theme} from '../config';
import {MiniFigure, colorsAtHeight} from './MiniFigure';
import {clamp} from './ui';
import timeline from '../timeline.json';

const TOOLS = [filaments.t1, filaments.t2, filaments.t3, filaments.t4];

/**
 * Stylised 4-toolhead tool-changer printer (illustration, not a product render).
 * Prints the Mini Me from the bottom up, swapping to the toolhead of each colour.
 */
export const Printer: React.FC<{width: number}> = ({width}) => {
  const frame = useCurrentFrame();
  const {start, end, swapEvery} = timeline.print;
  const W = 900;
  const H = 1000;
  const k = width / W;

  const raw = interpolate(frame, [start, end], [0, 1], clamp);
  const progress = Easing.inOut(Easing.sin)(raw);

  // figure placement inside printer
  const figW = 440;
  const figX = (W - figW) / 2;
  const figY = 250;
  const figH = figW * 1.5;
  // figure local y printed (viewBox 50..600)
  const localY = 600 - 550 * progress;
  const nozzleY = figY + (localY / 600) * figH;

  const printing = raw > 0 && raw < 1;
  const colors = colorsAtHeight(localY);
  const swapIndex = Math.floor(frame / swapEvery);
  const activeColor = printing ? colors[swapIndex % colors.length] : TOOLS[0].color;
  const activeTool = TOOLS.findIndex((t) => t.color === activeColor);
  const sinceSwap = frame % swapEvery;
  const swapFlash = printing ? interpolate(sinceSwap, [0, 4], [1, 0], clamp) : 0;

  // nozzle sweeps across the current layer
  const sweep = Math.sin(frame * 0.9) * 0.5 + 0.5;
  const layerHalf = 120 + 40 * Math.sin(localY / 40);
  const nozzleX = printing ? W / 2 - layerHalf + sweep * layerHalf * 2 : W / 2 + 250;
  const headY = printing ? nozzleY - 118 : 150;

  return (
    <svg viewBox={`0 0 ${W} ${H}`} width={W * k} height={H * k} style={{overflow: 'visible'}}>
      <defs>
        <linearGradient id="frameGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#3A3470" />
          <stop offset="1" stopColor="#221D4D" />
        </linearGradient>
        <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="rgba(255,255,255,0.10)" />
          <stop offset="0.5" stopColor="rgba(255,255,255,0.02)" />
          <stop offset="1" stopColor="rgba(255,255,255,0.07)" />
        </linearGradient>
        <radialGradient id="glow">
          <stop offset="0" stopColor={activeColor} stopOpacity={0.9} />
          <stop offset="1" stopColor={activeColor} stopOpacity={0} />
        </radialGradient>
      </defs>

      {/* frame */}
      <rect x={20} y={20} width={W - 40} height={H - 40} rx={48} fill="url(#frameGrad)" stroke="rgba(255,255,255,0.18)" strokeWidth={4} />
      <rect x={60} y={120} width={W - 120} height={H - 200} rx={26} fill="#120E30" />
      <rect x={60} y={120} width={W - 120} height={H - 200} rx={26} fill="url(#glass)" />

      {/* tool docks along the top */}
      {TOOLS.map((t, i) => {
        const x = 110 + i * 175;
        const docked = !printing || i !== activeTool;
        return (
          <g key={i}>
            <rect x={x} y={40} width={150} height={64} rx={16} fill="rgba(0,0,0,0.35)" stroke="rgba(255,255,255,0.15)" strokeWidth={2} />
            {docked && (
              <g>
                <rect x={x + 30} y={46} width={90} height={52} rx={12} fill="#E9E6FF" />
                <rect x={x + 30} y={46} width={90} height={14} rx={7} fill={t.color} />
              </g>
            )}
            <text x={x + 75} y={90} textAnchor="middle" fontFamily={theme.bodyFont} fontWeight={900} fontSize={22} fill={docked ? '#2A2550' : 'rgba(255,255,255,0.5)'}>
              {`T${i + 1}`}
            </text>
            {!docked && (
              <rect x={x - 6} y={34} width={162} height={76} rx={20} fill="none" stroke={theme.spark} strokeWidth={5} strokeDasharray="14 10" opacity={0.6 + 0.4 * swapFlash} />
            )}
          </g>
        );
      })}

      {/* build plate */}
      <rect x={130} y={figY + figH - 30} width={W - 260} height={26} rx={10} fill="#4A4380" />
      <rect x={130} y={figY + figH - 30} width={W - 260} height={8} rx={4} fill="#7C73C9" />

      {/* small prime tower (the U1 still uses a small one) */}
      {new Array(Math.floor(progress * 12)).fill(0).map((_, i) => (
        <rect key={i} x={700} y={figY + figH - 30 - (i + 1) * 9} width={46} height={9} fill={TOOLS[i % 4].color} />
      ))}

      {/* the figure being printed */}
      <g transform={`translate(${figX} ${figY})`}>
        <MiniFigure id="printfig" width={figW} print={progress} layerLines />
      </g>

      {/* gantry + active toolhead */}
      <rect x={70} y={headY + 20} width={W - 140} height={22} rx={11} fill="#8E86D8" opacity={0.9} />
      {printing && <circle cx={nozzleX} cy={nozzleY} r={40} fill="url(#glow)" />}
      <g transform={`translate(${nozzleX - 60} ${headY})`}>
        <rect x={0} y={0} width={120} height={96} rx={20} fill="#F1EEFF" />
        <rect x={0} y={0} width={120} height={24} rx={12} fill={activeColor} stroke="#FFFFFF" strokeWidth={3} />
        <rect x={10} y={30} width={100} height={8} rx={4} fill="rgba(0,0,0,0.12)" />
        <path d="M44 96 L76 96 L64 116 L56 116 Z" fill="#B8B2DA" />
        <text x={60} y={78} textAnchor="middle" fontFamily={theme.bodyFont} fontWeight={900} fontSize={26} fill="#2A2550">
          {`T${(activeTool < 0 ? 0 : activeTool) + 1}`}
        </text>
      </g>
      {printing && swapFlash > 0 && (
        <circle cx={nozzleX} cy={headY + 48} r={70 + (1 - swapFlash) * 50} fill="none" stroke={activeColor} strokeWidth={6} opacity={swapFlash} />
      )}
      {/* progress bar */}
      <rect x={110} y={H - 58} width={W - 220} height={16} rx={8} fill="rgba(255,255,255,0.12)" />
      <rect x={110} y={H - 58} width={(W - 220) * raw} height={16} rx={8} fill={theme.spark} />
    </svg>
  );
};
