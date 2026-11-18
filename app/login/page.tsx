import type { Metadata } from 'next';
import { ArrowRight } from 'lucide-react';
import { Logo } from '@/components/shell/logo';
import { Avatar } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { personasByRole } from '@/lib/data/personas';
import { ROLE_LABEL } from '@/lib/nav';
import { ROLES, type PersonaSummary } from '@/lib/types';
import { loginAs } from './actions';

export const metadata: Metadata = { title: 'Log in as · Learnibility' };

const BOARD_LABEL = { cbse: 'CBSE', cambridge: 'Cambridge', ib: 'IB' } as const;

function meta(p: PersonaSummary) {
  if (p.role !== 'student') return null;
  const parts = [p.grade ? `Grade ${p.grade}` : null, p.programme ?? (p.board ? BOARD_LABEL[p.board] : null)];
  return parts.filter(Boolean).join(' · ');
}

export default function LoginPage() {
  const groups = personasByRole();
  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[minmax(320px,420px)_1fr]">
      <aside className="flex flex-col justify-between bg-brand-700 p-8 text-white lg:sticky lg:top-0 lg:h-screen">
        <div className="[&_a]:text-white [&_a>span:first-child]:bg-white [&_a>span:first-child]:text-brand-700">
          <Logo />
        </div>
        <div className="my-10 lg:my-0">
          <h1 className="text-3xl font-semibold tracking-tight">One verified record for every learner.</h1>
          <p className="mt-3 text-brand-100">
            Assessments, gaps, timetables, tutors, careers and applications, all driven by the same student record and seen
            through the eyes of each person around the student.
          </p>
        </div>
        <div className="text-sm text-brand-200">
          <p>Demo: pick anyone to log in as them. No passwords; all people and data are fictional.</p>
          <a href="/demo" className="mt-2 inline-block font-medium text-white underline underline-offset-4">Open the guided demo</a>
        </div>
      </aside>

      <main className="mx-auto w-full max-w-5xl p-6 sm:p-10">
        <h2 className="text-2xl font-semibold tracking-tight">Log in as</h2>
        <p className="mt-1 text-sm text-muted">Each persona shows a different part of Learnibility.</p>

        <div className="mt-8 flex flex-col gap-10">
          {ROLES.filter((r) => groups.has(r)).map((role) => (
            <section key={role} aria-labelledby={`role-${role}`}>
              <h3 id={`role-${role}`} className="mb-3 text-xs font-semibold uppercase tracking-wide text-subtle">
                {ROLE_LABEL[role]}s
              </h3>
              <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
                {groups.get(role)!.map((p) => (
                  <form key={p.id} action={loginAs}>
                    <input type="hidden" name="personaId" value={p.id} />
                    <button
                      type="submit"
                      className="group flex h-full w-full flex-col gap-3 rounded-[var(--radius-card)] border border-line bg-surface p-4 text-left shadow-[var(--shadow-card)] transition hover:border-brand-300 hover:shadow-md focus-visible:border-brand-500"
                    >
                      <div className="flex items-center gap-3">
                        <Avatar name={p.name} src={p.avatar} />
                        <div className="min-w-0">
                          <p className="truncate font-medium text-ink">{p.name}</p>
                          {meta(p) && <p className="truncate text-xs text-muted">{meta(p)}</p>}
                        </div>
                        <ArrowRight className="ml-auto size-4 text-subtle transition group-hover:translate-x-0.5 group-hover:text-brand-600" />
                      </div>
                      <p className="text-sm text-muted">{p.story}</p>
                      {p.role === 'student' && p.stream && p.stream !== 'none' && (
                        <Badge tone="brand" className="self-start capitalize">{p.stream}</Badge>
                      )}
                    </button>
                  </form>
                ))}
              </div>
            </section>
          ))}
        </div>
      </main>
    </div>
  );
}
