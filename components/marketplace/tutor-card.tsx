import Link from 'next/link';
import { BadgeCheck, Sparkles } from 'lucide-react';
import { Avatar } from '@/components/ui/avatar';
import { Card } from '@/components/ui/card';
import { buttonVariants } from '@/components/ui/button';
import { formatInr } from '@/lib/format';
import type { Tutor } from '@/lib/types/catalogue';
import { FORMAT_LABEL, MODE_LABEL } from './labels';
import { Rating } from './rating';

/** Explore Tutors card: the three facts a student compares (rating, price, mode), plus the match reason when there is one. */
export function TutorCard({ tutor, reason, score, href, compact }: { tutor: Tutor; reason?: string; score?: number; href: string; compact?: boolean }) {
  return (
    <Card className="flex h-full flex-col p-4">
      <div className="flex items-start gap-3">
        <Avatar name={tutor.displayName} personId={tutor.id} size="lg" photo />
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-1.5">
            <Link href={href} className="truncate font-semibold text-ink hover:text-brand-700">{tutor.displayName}</Link>
            {tutor.verified && <BadgeCheck className="size-4 shrink-0 text-brand-600" aria-label="Verified" />}
          </div>
          <p className="line-clamp-2 text-xs text-muted">{tutor.headline}</p>
          <p className="mt-0.5 text-[11px] text-subtle">{tutor.city} · {tutor.yearsExperience} yrs teaching</p>
        </div>
        {score !== undefined && <span className="shrink-0 rounded-md bg-brand-50 px-1.5 py-0.5 text-xs font-semibold text-brand-700" title="How well this tutor matches your gaps, style, budget and free time">{Math.round(score)}% match</span>}
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-muted">
        <Rating value={tutor.rating} count={tutor.reviewsCount} />
        <span aria-hidden>·</span>
        <span className="text-ink">{formatInr(tutor.pricing.oneToOnePerHourInr)}/hr</span>
        <span aria-hidden>·</span>
        <span>{tutor.formats.map((f) => FORMAT_LABEL[f]).join(' & ')}</span>
        {!compact && <><span aria-hidden>·</span><span>{tutor.modes.map((m) => MODE_LABEL[m]).join(' & ')}</span></>}
      </div>
      {reason && (
        <p className="mt-3 flex gap-1.5 rounded-lg bg-brand-50/60 p-2 text-xs text-brand-800">
          <Sparkles className="mt-0.5 size-3.5 shrink-0" aria-hidden />
          <span>{reason}</span>
        </p>
      )}
      <div className="mt-auto flex items-center gap-2 pt-4">
        <Link href={href} className={buttonVariants({ variant: 'secondary', size: 'sm' })}>View</Link>
        {tutor.pricing.demoInr === 0 && <span className="text-xs text-success-700">Free {tutor.pricing.demoMinutes}-min demo</span>}
      </div>
    </Card>
  );
}
