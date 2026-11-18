import { cva, type VariantProps } from 'class-variance-authority';
import type { HTMLAttributes } from 'react';
import { cn } from '@/lib/utils';
import type { Band, GapCode, Tier } from '@/lib/types';

export const badgeVariants = cva('inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-medium ring-1 ring-inset', {
  variants: {
    tone: {
      neutral: 'bg-surface-muted text-muted ring-line',
      brand: 'bg-brand-50 text-brand-700 ring-brand-200',
      success: 'bg-success-50 text-success-700 ring-success-600/20',
      warning: 'bg-warning-50 text-warning-700 ring-warning-600/20',
      danger: 'bg-danger-50 text-danger-700 ring-danger-600/20',
      info: 'bg-info-50 text-info-600 ring-info-600/20',
    },
  },
  defaultVariants: { tone: 'neutral' },
});

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, tone, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ tone }), className)} {...props} />;
}

export const LEVEL_LABEL = ['L0 No recall', 'L1 Recalls', 'L2 Explains', 'L3 Routine only', 'L4 Nearly there', 'L5 Mastered'] as const;

export const BAND_LABEL: Record<Band, string> = {
  below_avg: 'Below average', average: 'Average', above_avg: 'Above average', excellent: 'Excellent',
};
const BAND_TONE: Record<Band, BadgeProps['tone']> = {
  below_avg: 'danger', average: 'warning', above_avg: 'info', excellent: 'success',
};

export function BandBadge({ band }: { band: Band }) {
  return <Badge tone={BAND_TONE[band]}>{BAND_LABEL[band]}</Badge>;
}

/** Short names from the class 8 maths workbook, sheet Gap Diagnosis. */
export const GAP_LABEL: Record<GapCode, string> = {
  G1: 'Prerequisite', G2: 'Conceptual', G3: 'Procedural', G4: 'Careless', G5: 'Transfer',
  G6: 'Retention', G7: 'Language', G8: 'Time pressure', G9: 'Calibration', G10: 'Engagement',
};

export function GapBadge({ code }: { code: GapCode }) {
  return <Badge tone="warning" title={GAP_LABEL[code]}>{code} · {GAP_LABEL[code]}</Badge>;
}

const TIER_LABEL: Record<Tier, string> = { T1: 'Standard', T2: 'Elevated', T3: 'Sensitive health', C: 'Consent' };
const TIER_TONE: Record<Tier, BadgeProps['tone']> = { T1: 'neutral', T2: 'warning', T3: 'danger', C: 'info' };

export function TierBadge({ tier }: { tier: Tier }) {
  return <Badge tone={TIER_TONE[tier]}>{tier} · {TIER_LABEL[tier]}</Badge>;
}
