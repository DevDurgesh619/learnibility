import type { Metadata } from 'next';
import { BookOpen, Clock, Target, TrendingUp } from 'lucide-react';
import { BarChart, RadarChart, TrendChart } from '@/components/charts';
import { Logo } from '@/components/shell/logo';
import {
  Avatar, Badge, BandBadge, Button, Card, CardBody, CardFooter, CardHeader, EmptyState, GapBadge, PageHeader, Progress,
  StatTile, Table, TBody, TD, TH, THead, TR, TierBadge,
} from '@/components/ui';
import { BANDS, GAP_CODES, TIERS } from '@/lib/types';

export const metadata: Metadata = { title: 'Design system · Learnibility' };

// Sample numbers for the gallery only.
const radar = [
  { axis: 'Rational numbers', you: 0.82, target: 0.8 },
  { axis: 'Linear equations', you: 0.64, target: 0.8 },
  { axis: 'Squares & roots', you: 0.48, target: 0.8 },
  { axis: 'Exponents', you: 0.71, target: 0.8 },
  { axis: 'Mensuration', you: 0.58, target: 0.8 },
  { axis: 'Data handling', you: 0.9, target: 0.8 },
];
const trend = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6'].map((x, i) => ({ x, lrs: 0.55 + i * 0.04, mci: 0.55 + i * 0.03 }));
const bars = [
  { x: 'Maths', learn: 6.5, master: 9.2 },
  { x: 'Science', learn: 4.1, master: 5.8 },
  { x: 'English', learn: 2.0, master: 3.1 },
];

export default function DesignPage() {
  return (
    <div className="mx-auto max-w-6xl p-6 sm:p-10">
      <div className="mb-8"><Logo /></div>
      <PageHeader eyebrow="Foundations" title="Design system" description="Components every screen uses. Import from @/components/ui, @/components/charts and @/components/shell." actions={<><Button variant="secondary">Secondary</Button><Button>Primary</Button></>} />

      <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatTile label="Learning rate (LRS)" value="0.79" delta={{ value: '+0.06', direction: 'up' }} hint="vs last month" icon={<TrendingUp />} />
        <StatTile label="Retention" value="89%" delta={{ value: '-3%', direction: 'down' }} icon={<BookOpen />} />
        <StatTile label="Open gaps" value="4" delta={{ value: '-2', direction: 'down', good: true }} icon={<Target />} />
        <StatTile label="Hours to close" value="7.5 h" hint="Average band" icon={<Clock />} />
      </section>

      <section className="mt-6 grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader title="Mastery radar" description="RadarChart: you vs target" />
          <CardBody><RadarChart data={radar} series={[{ key: 'you', label: 'You' }, { key: 'target', label: 'Target' }]} /></CardBody>
        </Card>
        <Card>
          <CardHeader title="Trend" description="TrendChart: LRS and calibration over 6 weeks" />
          <CardBody><TrendChart data={trend} series={[{ key: 'lrs', label: 'LRS' }, { key: 'mci', label: 'MCI' }]} target={{ value: 0.8, label: 'Target 0.80' }} /></CardBody>
        </Card>
        <Card>
          <CardHeader title="Bar chart" description="BarChart: hours to learn vs master" />
          <CardBody><BarChart data={bars} series={[{ key: 'learn', label: 'Learn' }, { key: 'master', label: 'Master' }]} format="hours" /></CardBody>
        </Card>
        <Card>
          <CardHeader title="Badges" description="Bands, gap codes and sensitivity tiers" />
          <CardBody className="flex flex-wrap gap-2">
            {BANDS.map((b) => <BandBadge key={b} band={b} />)}
            {GAP_CODES.map((g) => <GapBadge key={g} code={g} />)}
            {TIERS.map((t) => <TierBadge key={t} tier={t} />)}
            <Badge tone="brand">Brand</Badge><Badge tone="success">Done</Badge><Badge tone="danger">Overdue</Badge>
          </CardBody>
        </Card>
      </section>

      <section className="mt-6">
        <Card>
          <CardHeader title="Table" description="Table, THead, TBody, TR, TH, TD" />
          <Table className="mt-4">
            <THead><TR><TH>Student</TH><TH>Subtopic</TH><TH>Gap</TH><TH>Level</TH><TH className="w-48">Mastery</TH></TR></THead>
            <TBody>
              {[['Kabir Singh', 'Square roots by factorisation', 'G4', 0.62], ['Ishita Rao', 'Adding unlike fractions', 'G1', 0.31], ['Rohan Das', 'Linear equations in one variable', 'G10', 0.44]].map(([n, s, g, m]) => (
                <TR key={n as string}>
                  <TD><div className="flex items-center gap-2"><Avatar name={n as string} size="sm" />{n}</div></TD>
                  <TD>{s}</TD><TD><GapBadge code={g as 'G1'} /></TD><TD>L2</TD>
                  <TD><div className="flex items-center gap-2"><Progress value={m as number} tone={(m as number) < 0.4 ? 'danger' : 'warning'} /><span className="text-xs text-muted">{Math.round((m as number) * 100)}%</span></div></TD>
                </TR>
              ))}
            </TBody>
          </Table>
          <CardFooter><Button variant="link" size="sm" className="px-0">View all gaps</Button></CardFooter>
        </Card>
      </section>

      <section className="mt-6"><EmptyState title="No tests yet" description="Take the onboarding test to see your gaps, timetable and tutor matches." action={<Button>Start onboarding test</Button>} /></section>
    </div>
  );
}
