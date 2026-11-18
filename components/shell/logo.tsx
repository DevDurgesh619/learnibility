import Link from 'next/link';

/** Brand mark: an open book whose right page rises into a spark (learning that grows). */
export function LogoMark({ className = 'size-8' }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" className={className} aria-hidden>
      <defs>
        <linearGradient id="lb-g" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#6366f1" />
          <stop offset="1" stopColor="#4338ca" />
        </linearGradient>
      </defs>
      <rect width="32" height="32" rx="9" fill="url(#lb-g)" />
      <path d="M7 10.5c3-.9 6-.6 9 1.2v11.6c-3-1.8-6-2.1-9-1.2z" fill="#fff" opacity=".95" />
      <path d="M16 11.7c3-1.8 6-2.1 9-1.2v11.6c-3-.9-6-.6-9 1.2z" fill="#fff" opacity=".7" />
      <path d="M22.5 5.5l.9 2.1 2.1.9-2.1.9-.9 2.1-.9-2.1-2.1-.9 2.1-.9z" fill="#fde68a" />
    </svg>
  );
}

export function Logo({ href = '/' }: { href?: string }) {
  return (
    <Link href={href} className="flex items-center gap-2 font-semibold tracking-tight text-ink">
      <LogoMark />
      <span className="text-[17px]">Learn<span className="text-brand-600">ibility</span></span>
    </Link>
  );
}
