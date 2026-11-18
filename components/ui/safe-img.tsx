'use client';

import { useState, type ReactNode } from 'react';

/** <img> that swaps to a fallback if the image fails to load (e.g. a remote campus photo is unavailable). */
export function SafeImg({ src, alt, className, fallback, loading = 'lazy' }: { src: string; alt: string; className?: string; fallback: ReactNode; loading?: 'lazy' | 'eager' }) {
  const [failed, setFailed] = useState(false);
  if (failed) return <>{fallback}</>;
  // eslint-disable-next-line @next/next/no-img-element
  return <img src={src} alt={alt} className={className} loading={loading} decoding="async" onError={() => setFailed(true)} />;
}
