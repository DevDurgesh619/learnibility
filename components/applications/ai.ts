/**
 * Simulated AI for application support. Everything here is deterministic and rule-based so the demo is
 * repeatable without a model: the AI pre-pass on essays, the outline helper in the draft studio, and
 * action-item extraction from meeting notes ("meeting intelligence").
 */
import { wordCount } from './logic';

export interface AiComment {
  anchor: { start: number; end: number; quote: string };
  text: string;
  rule: string;
}

interface Sentence {
  start: number;
  end: number;
  text: string;
}

export function sentences(text: string): Sentence[] {
  const out: Sentence[] = [];
  const re = /[^.!?\n]+[.!?]*/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) {
    const raw = m[0];
    const lead = raw.length - raw.trimStart().length;
    const t = raw.trim();
    if (t.length < 3) continue;
    out.push({ start: m.index + lead, end: m.index + lead + t.length, text: t });
  }
  return out;
}

const CLICHE_OPENERS = [/^ever since/i, /^since (i was|childhood|my childhood)/i, /^from a young age/i, /^according to/i, /^(the )?(oxford|cambridge|merriam)[- ]webster/i, /^"/, /^what is /i, /^in today's world/i];
const VAGUE = [
  { re: /\bpassion(ate)?\b/i, text: 'Naming the passion does less than showing it. Swap this for one thing you did because of it.' },
  { re: /\b(very|really|extremely)\b/i, text: 'Intensifiers weaken the sentence. Cut the word or replace it with a specific detail.' },
  { re: /\b(always|never) been\b/i, text: 'Absolute claims are hard to believe. Anchor this in a specific time or moment.' },
  { re: /\b(many|various|several) (things|skills|experiences)\b/i, text: 'Vague plural. Name one of them and show what it taught you.' },
];
const REFLECTION = /\b(taught me|i learned|i learnt|i realised|i realized)\b/i;

/**
 * AI pre-pass: up to `limit` comments anchored to the text, most useful first.
 * `prompt` lets the pass check prompt-specific structure (UCAS three questions, "why this school").
 */
export function aiPrePass(text: string, prompt: string, wordLimit?: number, limit = 5): { comments: AiComment[]; summary: string } {
  const ss = sentences(text);
  const out: AiComment[] = [];
  const add = (s: { start: number; end: number }, t: string, rule: string, quoteLen = 90) => {
    if (out.some((c) => c.anchor.start === s.start)) return;
    const end = Math.min(s.end, s.start + quoteLen);
    out.push({ anchor: { start: s.start, end, quote: text.slice(s.start, end) }, text: t, rule });
  };

  const first = ss[0];
  if (first && CLICHE_OPENERS.some((r) => r.test(first.text))) {
    add(first, 'Admissions readers see this opening often. Start inside a specific moment instead, then zoom out.', 'opener');
  }
  for (const s of ss) {
    const n = wordCount(s.text);
    if (n > 38) add(s, `This sentence runs to ${n} words. Split it so each idea lands on its own.`, 'long_sentence');
  }
  for (const v of VAGUE) {
    for (const s of ss) {
      const m = s.text.match(v.re);
      if (m && m.index !== undefined) {
        const start = s.start + m.index;
        add({ start, end: start + m[0].length }, v.text, 'vague');
        break;
      }
    }
  }
  const refl = ss.find((s) => REFLECTION.test(s.text));
  if (refl) {
    const i = ss.indexOf(refl);
    const next = ss[i + 1]?.text ?? '';
    if (!/\b(for example|when|after|because|during)\b/i.test(refl.text + ' ' + next)) {
      add(refl, 'Good reflection. Back it with the concrete example that taught you this.', 'reflection_needs_example');
    }
  }
  if (/ucas/i.test(prompt) && !/\b(course|degree|study|studying)\b/i.test(text.slice(0, Math.max(400, Math.floor(text.length / 3))))) {
    if (first) add(first, 'UCAS readers want to know early why you chose this course. Say it within the first paragraph.', 'ucas_why_course');
  }
  if (/why (this|our)|why do you want/i.test(prompt) && !/\b(professor|programme|program|course|module|club|lab|centre|center)\b/i.test(text)) {
    const last = ss[ss.length - 1];
    if (last) add(last, 'A "why us" essay needs one detail only this university has: a module, lab, professor or society.', 'why_us_specific');
  }

  const words = wordCount(text);
  const parts: string[] = [`${words}${wordLimit ? ` of ${wordLimit}` : ''} words`];
  if (wordLimit && words > wordLimit) parts.push(`${words - wordLimit} over the limit`);
  else if (wordLimit && words < wordLimit * 0.7) parts.push('room to add one more example');
  const picked = out.slice(0, limit);
  parts.push(picked.length ? `${picked.length} suggestion${picked.length === 1 ? '' : 's'}` : 'no issues found');
  return { comments: picked, summary: parts.join(' · ') };
}

/** Draft studio: an outline for the prompt type. */
export function outlineFor(prompt: string, wordLimit?: number): { heading: string; points: string[] }[] {
  const w = wordLimit ?? 650;
  if (/ucas/i.test(prompt)) {
    return [
      { heading: `Why this course (about ${Math.round(w * 0.4)} words)`, points: ['The moment the subject became yours', 'What you want to understand next, in the subject\'s own terms'] },
      { heading: `How school has prepared you (about ${Math.round(w * 0.35)} words)`, points: ['One A level topic you went beyond, and how', 'A skill it built that the course needs'] },
      { heading: `Outside education (about ${Math.round(w * 0.25)} words)`, points: ['Work, competitions or projects linked to the course', 'What you did, what changed, what you learned'] },
    ];
  }
  if (/why (this|our)|why do you want/i.test(prompt)) {
    return [
      { heading: 'Your goal', points: ['What you want to study and why, in one or two sentences'] },
      { heading: 'Their fit', points: ['Two specifics only this university offers', 'How you would use each one'] },
      { heading: 'Your contribution', points: ['What you would add to the community'] },
    ];
  }
  return [
    { heading: 'Hook', points: ['Open inside a specific moment, not a definition or quote'] },
    { heading: 'Story', points: ['What happened, what you did, what was hard'] },
    { heading: 'Reflection', points: ['What changed in how you think', 'Where it points next'] },
  ];
}

/** Meeting intelligence: pull action items out of free-text notes. One item per action sentence. */
export function extractActionItems(notes: string, owner: string, today: string): { title: string; dueOn: string }[] {
  const items: { title: string; dueOn: string }[] = [];
  const lines = notes.split(/\n|(?<=[.;])\s+/).map((l) => l.replace(/^[-*•\d.)\s]+/, '').trim()).filter(Boolean);
  const verb = /^(to ?do:|action:|todo:)?\s*(send|upload|finish|complete|draft|write|ask|request|book|email|submit|revise|update|prepare|register|pay|share|read|call|shortlist|add|check)\b/i;
  const ownerRe = new RegExp(`^${owner}\\s+(will|to|should)\\s+`, 'i');
  for (const raw of lines) {
    let l = raw;
    if (ownerRe.test(l)) l = l.replace(ownerRe, '');
    if (!verb.test(l)) continue;
    l = l.replace(/^(to ?do:|action:|todo:)\s*/i, '');
    const due = parseDue(l, today);
    const title = l.replace(/\s*(by|before|on)\s+(\d{1,2}\s+\w{3,9}|tomorrow|friday|monday|tuesday|wednesday|thursday|saturday|sunday|next week)\.?$/i, '').replace(/[.;]$/, '');
    items.push({ title: title[0]!.toUpperCase() + title.slice(1), dueOn: due });
  }
  return items.slice(0, 8);
}

const MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
const DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];

function parseDue(l: string, today: string): string {
  const base = new Date(`${today}T00:00:00Z`);
  const add = (n: number) => new Date(base.getTime() + n * 86_400_000).toISOString().slice(0, 10);
  const m = l.match(/(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*/i);
  if (m) {
    const month = MONTHS.indexOf(m[2]!.toLowerCase());
    let year = base.getUTCFullYear();
    if (month < base.getUTCMonth()) year += 1;
    return `${year}-${String(month + 1).padStart(2, '0')}-${String(Number(m[1])).padStart(2, '0')}`;
  }
  if (/tomorrow/i.test(l)) return add(1);
  if (/next week/i.test(l)) return add(7);
  const d = DAYS.findIndex((x) => new RegExp(`\\b${x}\\b`, 'i').test(l));
  if (d >= 0) return add(((d - base.getUTCDay() + 7) % 7) || 7);
  return add(7);
}
