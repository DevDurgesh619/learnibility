import Link from 'next/link';
import { Briefcase, Clock, GraduationCap, ListPlus, Route } from 'lucide-react';
import { assignSkillTask } from '@/lib/actions/mentor';
import { mentorContext } from '@/components/mentor/context';
import { MenteeSwitcher } from '@/components/mentor/mentee-switcher';
import { careersToPlan, skillPlanFor } from '@/components/mentor/skill-plan';
import { Notice } from '@/components/parent/notice';
import { Badge, Button, Card, CardBody, CardHeader, EmptyState, PageHeader, StatTile, Table, TBody, TD, TH, THead, TR } from '@/components/ui';
import { addDaysLocal, demoToday, getCareer, listResources } from '@/lib/data';
import { formatHours, formatInr } from '@/lib/format';
import { cn } from '@/lib/utils';

export default async function SkillPlans({ searchParams }: { searchParams: Promise<Record<string, string | string[] | undefined>> }) {
  const sp = await searchParams;
  const { mentees, mentee } = await mentorContext(searchParams);
  if (!mentee) return (<><PageHeader eyebrow="Mentor" title="Skill plans" /><EmptyState title="No mentees yet" /></>);
  const id = mentee.student.id;
  const careers = careersToPlan(id);
  const careerId = (typeof sp.career === 'string' && careers.some((c) => c.careerId === sp.career) ? sp.career : careers[0]?.careerId) ?? '';
  const plan = careerId ? skillPlanFor(id, careerId) : undefined;
  const career = careerId ? getCareer(careerId) : undefined;
  const res = new Map(listResources().map((r) => [r.id, r]));
  const assigned = typeof sp.assigned === 'string' ? sp.assigned : undefined;
  const lines = (plan?.skills ?? []).filter((l) => l.levelsToClimb > 0).sort((a, b) => Number(b.importance === 'core') - Number(a.importance === 'core') || b.hours - a.hours);

  return (
    <>
      <PageHeader eyebrow="Mentor" title="Skill plans" description="The skill gap for each career a mentee is weighing, with a free route and a paid route." />
      <MenteeSwitcher mentees={mentees} selectedId={id} basePath="/mentor/skill-plans" />
      {assigned && <Notice>Added to {mentee.student.firstName}&apos;s tasks.</Notice>}

      {!careers.length ? (
        <EmptyState icon={<Briefcase />} title={`${mentee.student.firstName} has no careers shortlisted`} description="Once they run Career Fit or shortlist a career, the skill plan shows here." />
      ) : (
        <>
          <nav aria-label="Careers" className="mb-6 flex flex-wrap gap-2">
            {careers.map((c) => (
              <Link key={c.careerId} href={`/mentor/skill-plans?${new URLSearchParams({ mentee: id, career: c.careerId })}`}
                className={cn('rounded-full border px-3 py-1.5 text-sm', c.careerId === careerId ? 'border-brand-300 bg-brand-50 font-medium text-brand-700' : 'border-line bg-surface text-muted hover:text-ink')}>
                {c.title}{c.score !== undefined && <span className="ml-1.5 text-xs text-subtle">fit {Math.round(c.score)}</span>}
              </Link>
            ))}
          </nav>
          {!plan ? <EmptyState title="No plan for this career" /> : (
            <>
              <section className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
                <StatTile label="Skills to build" value={lines.length} icon={<ListPlus />} hint={`${lines.filter((l) => l.importance === 'core').length} core`} />
                <StatTile label="Free route" value={formatHours(plan.free.hours)} icon={<Clock />} hint={`About ${plan.free.months} months at 5 h a week · ₹0`} />
                <StatTile label="Paid route" value={formatHours(plan.paid.hours)} icon={<Route />} hint={`About ${plan.paid.months} months · ${formatInr(plan.paid.inr)}`} />
                <StatTile label="Fastest pathway" value={plan.pathways.length ? `${Math.min(...plan.pathways.map((p) => p.yearsToEntry))} yrs` : '—'} icon={<GraduationCap />} hint="To first job" />
              </section>
              {career && <p className="mb-6 max-w-3xl text-sm text-muted">{career.summary}</p>}

              <Card className="mb-6">
                <CardHeader title="Skill gap" description="Current level to target level, 0 to 5" />
                {lines.length ? (
                  <div className="overflow-x-auto">
                    <Table className="mt-4 min-w-[760px]">
                      <THead><TR><TH>Skill</TH><TH>Level</TH><TH>Hours</TH><TH>Free route</TH><TH>Paid route</TH><TH /></TR></THead>
                      <TBody>{lines.map((l) => {
                        const free = l.freeRoute.resourceIds.map((r) => res.get(r)).filter(Boolean)[0];
                        const paid = l.paidRoute.resourceId ? res.get(l.paidRoute.resourceId) : undefined;
                        return (
                          <TR key={l.skillId} className={l.skillId === assigned ? 'bg-success-50' : undefined}>
                            <TD><p className="font-medium text-ink">{l.name}</p><Badge tone={l.importance === 'core' ? 'brand' : 'neutral'}>{l.importance}</Badge></TD>
                            <TD className="whitespace-nowrap">{l.currentLevel} → {l.targetLevel}</TD>
                            <TD>{formatHours(l.hours)}</TD>
                            <TD className="max-w-[14rem]"><p className="truncate text-ink">{free?.title ?? 'Self-practice'}</p><p className="text-xs text-muted">{free?.provider ?? ''} · ₹0</p></TD>
                            <TD className="max-w-[14rem]"><p className="truncate text-ink">{paid?.title ?? 'Tutor support'}</p><p className="text-xs text-muted">{formatHours(l.paidRoute.hours)} · {formatInr(l.paidRoute.inr)}</p></TD>
                            <TD>
                              <form action={assignSkillTask}>
                                <input type="hidden" name="learnerId" value={id} /><input type="hidden" name="careerId" value={careerId} /><input type="hidden" name="skillId" value={l.skillId} />
                                <input type="hidden" name="title" value={`Start ${l.name}${free ? `: ${free.title}` : ''}`} />
                                <input type="hidden" name="detail" value={`Skill plan for ${career?.title ?? careerId}. Level ${l.currentLevel} to ${l.targetLevel}, about ${formatHours(l.hours)}.`} />
                                <input type="hidden" name="due" value={addDaysLocal(demoToday(), 7)} />
                                <Button size="sm" variant="secondary" type="submit">Add as task</Button>
                              </form>
                            </TD>
                          </TR>
                        );
                      })}</TBody>
                    </Table>
                  </div>
                ) : <CardBody><EmptyState className="border-0" title="No skill gaps" description="Every skill for this career is already at its target level." /></CardBody>}
              </Card>

              <Card>
                <CardHeader title="Pathways" description="Degrees and routes into the career" />
                <CardBody className="grid gap-4 pt-3 md:grid-cols-2">
                  {plan.pathways.length ? plan.pathways.map((p) => (
                    <div key={p.id} className="rounded-lg border border-line p-4">
                      <div className="flex items-start justify-between gap-2"><p className="font-medium text-ink">{p.label}</p><Badge>{p.region}</Badge></div>
                      <p className="mt-1 text-sm text-muted">{p.yearsToEntry} years to entry{p.examIds.length ? ` · exams: ${p.examIds.join(', ')}` : ''}</p>
                      <p className="mt-1 text-sm text-muted">Cost about {formatInr(p.costInr.typical)} ({formatInr(p.costInr.low)}–{formatInr(p.costInr.high)}){p.examPrepHours ? ` · exam prep ${formatHours(p.examPrepHours)}` : ''}</p>
                    </div>
                  )) : <p className="text-sm text-muted">No pathways listed.</p>}
                </CardBody>
              </Card>
            </>
          )}
        </>
      )}
    </>
  );
}
