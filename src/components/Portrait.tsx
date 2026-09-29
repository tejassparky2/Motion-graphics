import React from 'react';
import {filaments} from '../config';

/** A simple "real proportions" portrait used as the customer's photo. */
export const Portrait: React.FC<{size: number; border?: number; rotate?: number; style?: React.CSSProperties}> = ({size, border = 14, rotate = 0, style}) => (
  <div
    style={{
      width: size,
      height: size * 1.16,
      background: '#fff',
      padding: border,
      paddingBottom: border * 4,
      borderRadius: 10,
      boxShadow: '0 30px 60px rgba(0,0,0,0.45)',
      transform: `rotate(${rotate}deg)`,
      ...style,
    }}
  >
    <svg viewBox="0 0 300 300" width="100%" height="100%" style={{display: 'block', borderRadius: 4}}>
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#8EC9FF" />
          <stop offset="1" stopColor="#FFD9A8" />
        </linearGradient>
      </defs>
      <rect width={300} height={300} fill="url(#sky)" />
      <circle cx={245} cy={60} r={26} fill="#FFF3C4" />
      <path d="M0 230 Q80 200 150 225 T300 215 L300 300 L0 300 Z" fill="#7FD69A" />
      {/* shoulders */}
      <path d="M50 300 Q60 222 150 214 Q240 222 250 300 Z" fill={filaments.t3.color} />
      <path d="M140 214 L150 250 L160 214 Z" fill={filaments.t2.color} />
      {/* neck */}
      <rect x={134} y={180} width={32} height={40} rx={10} fill="#E9B08A" />
      {/* head */}
      <ellipse cx={150} cy={140} rx={50} ry={62} fill={filaments.t2.color} />
      <ellipse cx={100} cy={146} rx={9} ry={14} fill={filaments.t2.color} />
      <ellipse cx={200} cy={146} rx={9} ry={14} fill={filaments.t2.color} />
      <path d="M98 132 C92 80 130 68 152 70 C186 70 212 92 202 134 C196 112 178 100 160 104 C140 108 120 104 108 112 C102 118 100 124 98 132 Z" fill={filaments.t1.color} />
      <circle cx={132} cy={140} r={5} fill={filaments.t1.color} />
      <circle cx={168} cy={140} r={5} fill={filaments.t1.color} />
      <path d="M126 128 Q132 124 140 127 M160 127 Q168 124 174 128" stroke={filaments.t1.color} strokeWidth={3} strokeLinecap="round" fill="none" />
      <path d="M135 170 Q150 182 165 170" stroke="#B5543F" strokeWidth={4} strokeLinecap="round" fill="none" />
    </svg>
  </div>
);
