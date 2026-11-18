import { Badge } from '@/components/ui/badge';
import type { Booking } from '@/lib/data/types';

const MAP: Record<Booking['status'], { label: string; tone: 'neutral' | 'brand' | 'success' | 'warning' | 'danger' | 'info' }> = {
  requested: { label: 'Waiting for tutor', tone: 'warning' },
  accepted: { label: 'Confirmed', tone: 'success' },
  active: { label: 'Active', tone: 'brand' },
  completed: { label: 'Completed', tone: 'neutral' },
  declined: { label: 'Declined', tone: 'danger' },
  cancelled: { label: 'Cancelled', tone: 'neutral' },
};

export function BookingStatusBadge({ status }: { status: Booking['status'] }) {
  const m = MAP[status];
  return <Badge tone={m.tone}>{m.label}</Badge>;
}
