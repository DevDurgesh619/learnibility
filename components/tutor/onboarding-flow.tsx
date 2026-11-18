'use client';

import { useMemo, useState } from 'react';
import { ArrowLeft, BadgeCheck, Check, Sparkles, Upload, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardBody } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';
import { EXAMPLE_INTRO, extractProfile } from './extract';

/** Onboarding 1a-1h for the signed-in tutor. Publish posts everything to saveTutorPrefs; the server shows 1i. */
type Slot = { day: string; start: string; end: string };
export interface OnboardingSeed { name: string; city: string; availability: Slot[]; oneToOne: number; group: number | null; feeRate: number; identityDone: boolean }

const STEPS = ['About you', 'Teaching', 'Availability', 'Pricing', 'Verify', 'Publish'];
const AUD: [string, string][] = [['school', 'School students'], ['competitive_exam', 'Competitive exam'], ['college', 'College'], ['english_learners', 'English learners'], ['career_learners', 'Career learners']];
const HELP: [string, string][] = [['concept_learning', 'Concept learning'], ['exam_prep', 'Exam prep'], ['homework', 'Homework'], ['skill_development', 'Skill development']];
const STYLE: [string, string][] = [['concept_first', 'Concept-first'], ['practice_first', 'Practice-first'], ['socratic', 'Socratic'], ['exam_focused', 'Exam-focused'], ['project_based', 'Project-based']];
const DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
const BANDS = [{ k: 'm', l: '7–10', s: '07:00', e: '10:00' }, { k: 'd', l: '10–1', s: '10:00', e: '13:00' }, { k: 'a', l: '4–7', s: '16:00', e: '19:00' }, { k: 'e', l: '7–10', s: '19:00', e: '22:00' }];
const toMin = (x: string) => Number(x.slice(0, 2)) * 60 + Number(x.slice(3, 5));

function Chips({ options, value, onChange, single }: { options: [string, string][]; value: string[]; onChange: (v: string[]) => void; single?: boolean }) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map(([v, l]) => {
        const on = value.includes(v);
        return <button key={v} type="button" aria-pressed={on} onClick={() => onChange(single ? [v] : on ? value.filter((x) => x !== v) : [...value, v])} className={cn('rounded-full border px-3 py-1 text-sm', on ? 'border-brand-500 bg-brand-50 font-medium text-brand-700' : 'border-line bg-surface text-muted hover:text-ink')}>{l}</button>;
      })}
    </div>
  );
}

function Editable({ label, items, onChange, placeholder }: { label: string; items: string[]; onChange: (v: string[]) => void; placeholder: string }) {
  const [draft, setDraft] = useState('');
  return (
    <div className="grid gap-2 border-b border-line py-3 sm:grid-cols-[140px_1fr] sm:items-center">
      <p className="text-sm text-muted">{label}</p>
      <div className="flex flex-wrap items-center gap-2">
        {items.map((x) => <span key={x} className="inline-flex items-center gap-1 rounded-full bg-brand-50 px-2.5 py-1 text-sm text-brand-700">{x}<button type="button" aria-label={`Remove ${x}`} onClick={() => onChange(items.filter((y) => y !== x))}><X className="size-3" /></button></span>)}
        <input value={draft} onChange={(e) => setDraft(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter' && draft.trim()) { e.preventDefault(); onChange([...items, draft.trim()]); setDraft(''); } }} placeholder={items.length ? '+ add' : placeholder} aria-label={`Add ${label}`} className={cn('min-w-32 flex-1 rounded-lg px-2 py-1 text-sm text-ink', items.length ? 'border border-transparent' : 'border border-warning-600/40 bg-warning-50/50')} />
      </div>
    </div>
  );
}

export function OnboardingFlow({ seed, action }: { seed: OnboardingSeed; action: (d: FormData) => void }) {
  const [step, setStep] = useState(0);
  const [intro, setIntro] = useState('');
  const [name, setName] = useState(seed.name);
  const [city, setCity] = useState(seed.city);
  const x = useMemo(() => extractProfile(intro || EXAMPLE_INTRO), [intro]);
  const [subjects, setSubjects] = useState<string[]>([]);
  const [levels, setLevels] = useState<string[]>([]);
  const [expertise, setExpertise] = useState<string[]>([]);
  const [years, setYears] = useState<string[]>([]);
  const [quals, setQuals] = useState<string[]>([]);
  const [langs, setLangs] = useState<string[]>([]);
  const [aud, setAud] = useState<string[]>([]);
  const [help, setHelp] = useState<string[]>([]);
  const [style, setStyle] = useState<string[]>([]);
  const [format, setFormat] = useState<string[]>(['one_to_one', 'group']);
  const [mode, setMode] = useState<string[]>(['online']);
  const [homework, setHomework] = useState<string[]>(['every_session']);
  const [cells, setCells] = useState<string[]>(() => DAYS.flatMap((d) => BANDS.filter((b) => seed.availability.some((a) => a.day === d && toMin(a.start) <= toMin(b.s) && toMin(a.end) >= toMin(b.e))).map((b) => `${d}:${b.k}`)));
  const [maxDay, setMaxDay] = useState(4);
  const [rate, setRate] = useState(seed.oneToOne);
  const [group, setGroup] = useState<number | ''>(seed.group ?? '');
  const [demoFree, setDemoFree] = useState(true);
  const [uploaded, setUploaded] = useState<Record<string, boolean>>({ identity: seed.identityDone });

  const readIntro = () => {
    setSubjects(x.subjects); setLevels(x.grades.length ? [`Class ${x.grades[0]}${x.grades.length > 1 ? `–${x.grades.at(-1)}` : ''}`] : []);
    setExpertise([...x.exams.map((e) => `${e} prep`), ...x.topics]); setYears(x.years ? [`${x.years} years`] : []); setQuals(x.qualifications); setLangs(x.languages);
    setAud(x.audiences); setHelp(x.helpTypes); setStyle(x.styles.slice(0, 2));
    setStep(2);
  };
  const ideal = `${levels[0] ?? 'School'} students${x.exams.length ? ` preparing for ${x.exams.join(', ')}` : ''} who need ${style.includes('concept_first') ? 'concept-first' : style.includes('practice_first') ? 'practice-heavy' : 'patient'} help with ${(x.topics.length ? x.topics : subjects).slice(0, 3).join(' and ') || 'their subject'}.`;
  const filled = [subjects.length, levels.length, expertise.length, years.length, quals.length, langs.length, intro.length > 40, uploaded.identity, uploaded.qualification].filter(Boolean).length;
  const strength = Math.round(40 + (filled / 9) * 55);
  const slots = DAYS.flatMap((d) => BANDS.filter((b) => cells.includes(`${d}:${b.k}`)).map((b) => ({ day: d, start: b.s, end: b.e })));
  const net = (v: number) => `₹${(v - Math.round(v * seed.feeRate)).toLocaleString('en-IN')}`;
  const stepIdx = step <= 2 ? 0 : step - 2;
  const nav = (back: number, next: () => void, label = 'Continue', disabled = false) => (
    <div className="flex items-center justify-between border-t border-line pt-4">
      <Button type="button" variant="ghost" onClick={() => setStep(back)}><ArrowLeft />Back</Button>
      <Button type="button" onClick={next} disabled={disabled}>{label}</Button>
    </div>
  );

  return (
    <div className="mx-auto max-w-3xl">
      {step > 0 && (
        <ol className="mb-6 grid grid-cols-3 gap-2 text-xs sm:grid-cols-6">
          {STEPS.map((s, i) => <li key={s} className={cn('rounded-md border px-2 py-1.5 text-center', i === stepIdx ? 'border-brand-500 bg-brand-50 font-medium text-brand-700' : i < stepIdx ? 'border-line text-ink' : 'border-line text-subtle')}>{i < stepIdx && <Check className="mr-1 inline size-3" />}{i + 1} {s}</li>)}
        </ol>
      )}
      <Card><CardBody className="space-y-5">
        {step === 0 && (
          <div className="py-6 text-center">
            <h1 className="text-2xl font-semibold text-ink">Set up your tutor profile</h1>
            <p className="mx-auto mt-2 max-w-lg text-sm text-muted">About 5 minutes. We match you with students whose gaps fit your strengths, and tell you what each one needs before every session.</p>
            <ol className="mx-auto mt-6 flex max-w-xl flex-wrap justify-center gap-2 text-sm text-muted">{STEPS.map((s, i) => <li key={s} className="rounded-full bg-surface-muted px-3 py-1">{i + 1} {s}</li>)}</ol>
            <Button type="button" className="mt-6" size="lg" onClick={() => setStep(1)}>Start</Button>
            <p className="mt-2 text-xs text-subtle">You can save and come back any time.</p>
          </div>
        )}
        {step === 1 && (
          <>
            <div><h2 className="text-xl font-semibold text-ink">Tell us about yourself as a teacher</h2><p className="text-sm text-muted">Write like you&apos;d introduce yourself to a parent. We&apos;ll fill in your profile from it.</p></div>
            <textarea value={intro} onChange={(e) => setIntro(e.target.value)} rows={5} placeholder={EXAMPLE_INTRO} aria-label="About you" className="w-full rounded-lg border border-line bg-surface p-3 text-sm text-ink focus:border-brand-400 focus:outline-none" />
            {!intro && <button type="button" onClick={() => setIntro(EXAMPLE_INTRO)} className="text-sm font-medium text-brand-700 hover:underline">Use the example text</button>}
            <div className="grid gap-3 sm:grid-cols-2">
              <label className="text-sm text-muted">Full name<input value={name} onChange={(e) => setName(e.target.value)} className="mt-1 h-10 w-full rounded-lg border border-line px-3 text-ink" /></label>
              <label className="text-sm text-muted">City<input value={city} onChange={(e) => setCity(e.target.value)} className="mt-1 h-10 w-full rounded-lg border border-line px-3 text-ink" /></label>
            </div>
            <div className="flex items-center justify-between border-t border-line pt-4">
              <button type="button" onClick={() => { setIntro(''); setStep(2); }} className="text-sm text-muted hover:text-ink">Prefer a form instead?</button>
              <Button type="button" onClick={readIntro} disabled={intro.trim().length < 20}><Sparkles />Continue</Button>
            </div>
          </>
        )}
        {step === 2 && (
          <>
            <div><h2 className="text-xl font-semibold text-ink">Here&apos;s what we understood</h2><p className="text-sm text-muted">Tap anything to fix it. Empty fields are the only ones we still need.</p></div>
            <div>
              <Editable label="Subjects" items={subjects} onChange={setSubjects} placeholder="e.g. Mathematics" />
              <Editable label="Levels" items={levels} onChange={setLevels} placeholder="e.g. Class 9–12" />
              <Editable label="Expertise" items={expertise} onChange={setExpertise} placeholder="e.g. Algebra" />
              <Editable label="Experience" items={years} onChange={setYears} placeholder="e.g. 6 years" />
              <Editable label="Qualifications" items={quals} onChange={setQuals} placeholder="e.g. B.Sc Maths, B.Ed" />
              <Editable label="Languages" items={langs} onChange={setLangs} placeholder="English, Hindi…" />
            </div>
            {nav(1, () => setStep(3), 'Looks right, continue', !subjects.length)}
          </>
        )}
        {step === 3 && (
          <>
            <h2 className="text-xl font-semibold text-ink">How do you like to teach?</h2>
            <div className="space-y-2"><p className="text-sm font-medium text-ink">Who do you teach best?</p><Chips options={AUD} value={aud} onChange={setAud} /></div>
            <div className="space-y-2"><p className="text-sm font-medium text-ink">What kind of help?</p><Chips options={HELP} value={help} onChange={setHelp} /></div>
            <div className="space-y-2"><p className="text-sm font-medium text-ink">Your style</p><Chips options={STYLE} value={style} onChange={setStyle} /></div>
            <div className="flex flex-wrap gap-6">
              <div className="space-y-2"><p className="text-sm text-muted">Format</p><Chips options={[['one_to_one', '1:1'], ['group', 'Group']]} value={format} onChange={setFormat} /></div>
              <div className="space-y-2"><p className="text-sm text-muted">Mode</p><Chips options={[['online', 'Online'], ['offline', 'Offline']]} value={mode} onChange={setMode} /></div>
              <div className="space-y-2"><p className="text-sm text-muted">Homework</p><Chips single options={[['every_session', 'Every session'], ['weekly', 'Weekly'], ['on_request', 'On request']]} value={homework} onChange={setHomework} /></div>
            </div>
            <div className="rounded-lg bg-brand-50/60 p-3 text-sm"><p className="font-medium text-ink">Your ideal student</p><p className="text-muted">{ideal}</p></div>
            {nav(2, () => setStep(4), 'Continue', !aud.length || !style.length)}
          </>
        )}
        {step === 4 && (
          <>
            <div><h2 className="text-xl font-semibold text-ink">When can students book you?</h2><p className="text-sm text-muted">Tap slots. You can change this any time from Profile.</p></div>
            <div className="overflow-x-auto"><table className="w-full min-w-[420px] text-sm"><thead><tr><th />{DAYS.map((d) => <th key={d} className="pb-2 font-medium capitalize text-muted">{d}</th>)}</tr></thead>
              <tbody>{BANDS.map((b) => <tr key={b.k}><th className="pr-2 text-left font-normal text-muted">{b.l}</th>{DAYS.map((d) => { const k = `${d}:${b.k}`; const on = cells.includes(k); return <td key={d} className="p-1"><button type="button" aria-pressed={on} aria-label={`${d} ${b.l}`} onClick={() => setCells(on ? cells.filter((c) => c !== k) : [...cells, k])} className={cn('flex h-9 w-full items-center justify-center rounded-md border', on ? 'border-brand-400 bg-brand-50 text-brand-700' : 'border-line')}>{on && <Check className="size-4" />}</button></td>; })}</tr>)}</tbody></table></div>
            <div className="flex flex-wrap gap-4 text-sm text-muted"><span>Session length 60 min</span><span>Time zone IST</span><label className="flex items-center gap-2">Max sessions / day<input type="number" min={1} max={10} value={maxDay} onChange={(e) => setMaxDay(Number(e.target.value) || 1)} className="h-8 w-16 rounded-md border border-line px-2 text-ink" /></label></div>
            {nav(3, () => setStep(5), 'Continue', !cells.length)}
          </>
        )}
        {step === 5 && (
          <>
            <div><h2 className="text-xl font-semibold text-ink">Set your rates</h2><p className="text-sm text-muted">Tutors like you ({subjects[0] ?? 'your subject'}{x.exams[0] ? ` · ${x.exams[0]}` : ''}{years[0] ? ` · ${years[0]}` : ''}) charge ₹600–₹1,000 / hr on Learnibility. Sample prices for the demo.</p></div>
            <label className="flex items-center gap-2 text-sm text-ink">1:1 session ₹<input type="number" min={0} step={50} value={rate} onChange={(e) => setRate(Number(e.target.value) || 0)} className="h-9 w-28 rounded-lg border border-line px-2" /> / hr</label>
            <label className="flex items-center gap-2 text-sm text-ink">Group ₹<input type="number" min={0} step={50} value={group} onChange={(e) => setGroup(e.target.value ? Number(e.target.value) : '')} placeholder="—" className="h-9 w-28 rounded-lg border border-line px-2" /> / student / hr</label>
            <label className="flex items-center gap-2 text-sm text-ink"><input type="checkbox" checked={demoFree} onChange={(e) => setDemoFree(e.target.checked)} className="accent-brand-600" />Free 30-min demo</label>
            <p className="rounded-lg bg-surface-muted p-3 text-sm text-muted">You receive {net(rate)} per 1:1 hour after the platform fee ({Math.round(seed.feeRate * 100)}%). Payouts weekly; details in Earnings.</p>
            {nav(4, () => setStep(6))}
          </>
        )}
        {step === 6 && (
          <>
            <div><h2 className="text-xl font-semibold text-ink">Verify your profile</h2><p className="text-sm text-muted">Verified tutors get a badge and 3× more demo requests. Documents are never shown to students.</p></div>
            {[['identity', 'Identity', 'Aadhaar / passport'], ['qualification', 'Highest qualification', 'Degree certificate'], ['experience', 'Experience proof', 'Optional · letter, payslip, LinkedIn']].map(([k, l, d]) => (
              <div key={k} className="flex items-center justify-between rounded-lg border border-line p-3">
                <div><p className="text-sm font-medium text-ink">{l}</p><p className="text-xs text-muted">{d}</p></div>
                {uploaded[k!] ? <span className="inline-flex items-center gap-1 text-sm text-success-700"><Check className="size-4" />Uploaded</span> : <Button type="button" size="sm" variant="secondary" onClick={() => setUploaded({ ...uploaded, [k!]: true })}><Upload />Upload</Button>}
              </div>
            ))}
            <div className="flex items-center justify-between border-t border-line pt-4">
              <Button type="button" variant="ghost" onClick={() => setStep(5)}><ArrowLeft />Back</Button>
              <div className="flex gap-2"><Button type="button" variant="secondary" onClick={() => setStep(7)}>Do this later</Button><Button type="button" onClick={() => setStep(7)}>Continue</Button></div>
            </div>
          </>
        )}
        {step === 7 && (
          <form action={action} className="space-y-5">
            <input type="hidden" name="back" value="/tutor/onboarding?step=done" />
            <input type="hidden" name="patch" value={JSON.stringify({
              headline: `${subjects.join(', ')}${levels[0] ? ` · ${levels[0]}` : ''}${x.exams.length ? ` · ${x.exams.join(', ')}` : ''}${years[0] ? ` · ${years[0]}` : ''}`,
              ...(intro ? { bio: intro } : {}), idealStudent: ideal, audiences: aud, helpTypes: help, teachingStyles: style, formats: format, modes: mode, homework: homework[0],
              availability: slots, maxSessionsPerDay: maxDay, pricing: { oneToOnePerHourInr: rate, groupPerStudentPerHourInr: group === '' ? null : group, demoInr: demoFree ? 0 : 200 }, onboarded: true,
            })} />
            <div className="flex flex-wrap items-center justify-between gap-3"><div className="w-56"><p className="mb-1 text-sm text-ink">Your profile is {strength}% complete</p><Progress value={strength} /></div><Button type="submit">Publish profile</Button></div>
            <div className="rounded-lg border border-line p-4">
              <p className="flex items-center gap-2 font-semibold text-ink">{name}{uploaded.identity && uploaded.qualification && <span className="inline-flex items-center gap-1 text-sm font-normal text-brand-700"><BadgeCheck className="size-4" />Verified</span>}</p>
              <p className="text-sm text-muted">{[subjects.join(', '), levels[0], x.exams.join(', '), years[0], city, langs.join(', ')].filter(Boolean).join(' · ')}</p>
              <div className="mt-2 flex flex-wrap gap-1.5">{[...x.topics, ...style.map((s) => STYLE.find(([k]) => k === s)?.[1] ?? s)].map((t) => <span key={t} className="rounded-full bg-surface-muted px-2 py-0.5 text-xs text-muted">{t}</span>)}</div>
              <p className="mt-2 text-sm text-ink">₹{rate.toLocaleString('en-IN')} / hr{demoFree ? ' · Free demo' : ''}</p>
            </div>
            <div className="text-sm"><p className="font-medium text-ink">To reach 100%</p><ul className="mt-1 list-inside list-disc text-muted"><li>Add a photo</li>{intro.length <= 40 && <li>Write a 2-line intro</li>}{!quals.length && <li>Qualifications</li>}{!uploaded.qualification && <li>Upload your qualification</li>}</ul></div>
            <p className="text-xs text-subtle">This is how students see you in Explore Tutors.</p>
            <Button type="button" variant="ghost" onClick={() => setStep(6)}><ArrowLeft />Back</Button>
          </form>
        )}
      </CardBody></Card>
    </div>
  );
}
