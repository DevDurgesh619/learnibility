'use client';
import { useEffect, useState } from 'react';

/** Elapsed call time for the live view (5d); starts when the page opens. */
export function LiveTimer() {
  const [sec, setSec] = useState(0);
  useEffect(() => { const t = setInterval(() => setSec((x) => x + 1), 1000); return () => clearInterval(t); }, []);
  const p = (n: number) => String(n).padStart(2, '0');
  return <span className="tabular-nums">{p(Math.floor(sec / 3600))}:{p(Math.floor(sec / 60) % 60)}:{p(sec % 60)}</span>;
}
