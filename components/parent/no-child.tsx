import { Users } from 'lucide-react';
import { EmptyState } from '@/components/ui';

export function NoChild() {
  return (
    <EmptyState
      icon={<Users />}
      title="No child linked yet"
      description="When your child signs up and adds you as their parent, their progress, plan and timetable show up here."
    />
  );
}
