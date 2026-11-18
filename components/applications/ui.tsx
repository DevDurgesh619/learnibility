import Link from 'next/link';
import type { ReactNode } from 'react';
import { ExternalLink, Info } from 'lucide-react';
import { Badge, type BadgeProps } from '@/components/ui/badge';
import type { ApplicationStatus } from '@/lib/data/types';
import type { Sourced, University } from '@/lib/types';
import { uniPhoto } from '@/lib/media';
import { cn } from '@/lib/utils';
import type { FitBand } from './fit';
import { FIT_BAND_LABEL } from './fit';
import { STATUS_LABEL, daysLeftLabel, fmtDate } from './logic';

export const COUNTRY_NAME: Record<string, string> = { in: 'India', us: 'USA', uk: 'UK', ca: 'Canada', au: 'Australia' };

const FIT_TONE: Record<FitBand, BadgeProps['tone']> = { reach: 'danger', target: 'info', safe: 'success' };

export function FitBadge({ band, className }: { band: FitBand; className?: string }) {
  return <Badge tone={FIT_TONE[band]} className={className}>{FIT_BAND_LABEL[band]}</Badge>;
}

const STATUS_TONE: Record<ApplicationStatus, BadgeProps['tone']> = {
  shortlisted: 'neutral', collecting_documents: 'warning', in_review: 'info', submitted: 'brand', decision: 'success',
};

export function StatusBadge({ status }: { status: ApplicationStatus }) {
  return <Badge tone={STATUS_TONE[status]}>{STATUS_LABEL[status]}</Badge>;
}

export function DaysLeft({ days, className }: { days: number; className?: string }) {
  const tone = days < 0 ? 'text-danger-700' : days < 14 ? 'text-danger-600' : days < 30 ? 'text-warning-700' : 'text-muted';
  return <span className={cn('text-xs font-medium whitespace-nowrap', tone, className)}>{daysLeftLabel(days)}</span>;
}

const COUNTRY_TILE: Record<string, string> = {
  us: 'bg-sky-100 text-sky-800', uk: 'bg-rose-100 text-rose-800', ca: 'bg-red-100 text-red-800', au: 'bg-amber-100 text-amber-800', in: 'bg-emerald-100 text-emerald-800',
};

/** Square tile for a university: its campus photo when bundled, otherwise a monogram (no logos in the demo). */
export function UniMark({ uni, size = 'md' }: { uni: Pick<University, 'shortName' | 'country'> & { id?: string }; size?: 'sm' | 'md' | 'lg' }) {
  const dims = { sm: 'size-8 text-[11px]', md: 'size-10 text-xs', lg: 'size-14 text-base' }[size];
  const photo = uniPhoto(uni.id);
  if (photo) {
    // eslint-disable-next-line @next/next/no-img-element
    return <img src={photo.src} alt="" aria-hidden loading="lazy" className={cn('shrink-0 rounded-lg bg-surface-muted object-cover ring-1 ring-black/5', dims)} />;
  }
  const letters = uni.shortName.replace(/[^A-Za-z ]/g, '').split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]).join('').toUpperCase() || uni.shortName.slice(0, 2);
  return <span aria-hidden className={cn('inline-flex shrink-0 items-center justify-center rounded-lg font-bold', dims, COUNTRY_TILE[uni.country] ?? 'bg-surface-muted text-ink')}>{letters}</span>;
}

/** Photo credit for a campus image (author, licence, source), as the licence requires. */
export function PhotoCredit({ photo, className }: { photo: { author: string; license: string; licenseUrl?: string; sourceUrl: string }; className?: string }) {
  return (
    <a href={photo.sourceUrl} target="_blank" rel="noreferrer" className={cn('text-[10px] leading-none text-white/85 hover:text-white hover:underline', className)}>
      Photo: {photo.author} · {photo.license} · Wikimedia Commons
    </a>
  );
}

/** A catalogue fact with its source and "as of" date (brief: every fact shows both). */
export function SourcedFact<T>({ fact, children, className }: { fact: Sourced<T>; children?: ReactNode; className?: string }) {
  const title = `${fact.verified ? 'Verified' : 'Estimate'} · as of ${fmtDate(fact.asOf)}${fact.note ? ` · ${fact.note}` : ''}`;
  return (
    <span className={cn('inline-flex items-baseline gap-1', className)}>
      <span>{children ?? String(fact.value ?? '—')}</span>
      <a href={fact.sourceUrl} target="_blank" rel="noreferrer" title={title} aria-label={`Source: ${title}`} className="text-subtle hover:text-brand-600">
        <Info className="inline size-3" />
      </a>
    </span>
  );
}

export function SourceLine<T>({ fact }: { fact: Sourced<T> }) {
  let host = fact.sourceUrl;
  try {
    host = new URL(fact.sourceUrl).hostname.replace(/^www\./, '');
  } catch {}
  return (
    <p className="mt-1 text-[11px] leading-tight text-subtle">
      <a href={fact.sourceUrl} target="_blank" rel="noreferrer" className="hover:text-brand-600 hover:underline">{host}<ExternalLink className="ml-0.5 inline size-2.5" /></a>
      {' · '}as of {fmtDate(fact.asOf)}{fact.verified ? '' : ' · estimate'}
    </p>
  );
}

/** Underlined link tabs (PDF 6a/7a). Pass the active key. */
export function LinkTabs({ tabs, active, className }: { tabs: { key: string; label: ReactNode; href: string; external?: boolean }[]; active: string; className?: string }) {
  return (
    <nav className={cn('-mx-4 mb-6 overflow-x-auto border-b border-line px-4 sm:mx-0 sm:px-0', className)} aria-label="Sections">
      <ul className="flex min-w-max gap-1">
        {tabs.map((t) => {
          const on = t.key === active;
          return (
            <li key={t.key}>
              <Link
                href={t.href}
                aria-current={on ? 'page' : undefined}
                className={cn('inline-flex items-center gap-1 border-b-2 px-3 py-2.5 text-sm font-medium transition-colors', on ? 'border-brand-600 text-brand-700' : 'border-transparent text-muted hover:text-ink')}
              >
                {t.label}
                {t.external && <ExternalLink className="size-3" />}
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

export function money(amount: number, currency: string) {
  return new Intl.NumberFormat(currency === 'INR' ? 'en-IN' : 'en-US', { style: 'currency', currency, maximumFractionDigits: 0 }).format(amount);
}

export function lakh(inr: number) {
  if (inr >= 1_00_00_000) return `₹${(inr / 1_00_00_000).toFixed(1)} Cr`;
  if (inr >= 1_00_000) return `₹${(inr / 1_00_000).toFixed(1)} L`;
  return `₹${new Intl.NumberFormat('en-IN').format(inr)}`;
}

export function Pill({ children, className }: { children: ReactNode; className?: string }) {
  return <span className={cn('inline-flex items-center rounded-full border border-line bg-surface px-2.5 py-0.5 text-xs text-muted', className)}>{children}</span>;
}
