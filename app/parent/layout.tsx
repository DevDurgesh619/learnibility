import type { ReactNode } from 'react';
import { RoleLayout } from '@/components/shell/role-layout';

export default function Layout({ children }: { children: ReactNode }) {
  return <RoleLayout role="parent">{children}</RoleLayout>;
}
