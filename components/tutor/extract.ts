/**
 * Onboarding 1b to 1c: reads a tutor's free-text intro into profile chips. Pre-written rules (no live model):
 * subjects, class range, exams, topic strengths, years of experience, qualifications and languages.
 */
export interface Extracted {
  subjects: string[]; grades: number[]; exams: string[]; topics: string[]; years: number | null; qualifications: string[]; languages: string[];
  audiences: string[]; helpTypes: string[]; styles: string[];
}

const SUBJECTS: [RegExp, string][] = [
  [/\bmath(s|ematics)?\b/i, 'Mathematics'], [/\bphysics\b/i, 'Physics'], [/\bchemistry\b/i, 'Chemistry'], [/\bbiology\b/i, 'Biology'],
  [/\bscience\b/i, 'Science'], [/\beconomics\b/i, 'Economics'], [/\baccount(s|ancy|ing)\b/i, 'Accountancy'], [/\bbusiness\b/i, 'Business Studies'],
  [/\bhistory\b/i, 'History'], [/\bgeography\b/i, 'Geography'], [/\bpolitic(s|al science)\b/i, 'Political Science'], [/\benglish\b/i, 'English'],
  [/\bcomputer science\b|\bcoding\b|\bprogramming\b/i, 'Computer Science'],
];
const EXAMS: [RegExp, string][] = [[/\bjee\b/i, 'JEE'], [/\bneet\b/i, 'NEET'], [/\bigcse\b/i, 'IGCSE'], [/\bib\b|\binternational baccalaureate\b/i, 'IB'], [/\bboards?\b/i, 'Board exams'], [/\bsat\b/i, 'SAT'], [/\bcuet\b/i, 'CUET'], [/\bolympiad/i, 'Olympiad']];
const TOPICS = ['algebra', 'calculus', 'geometry', 'trigonometry', 'probability', 'statistics', 'mechanics', 'electrostatics', 'optics', 'thermodynamics', 'organic chemistry', 'physical chemistry', 'genetics', 'microeconomics', 'macroeconomics', 'essay writing', 'grammar', 'coordinate geometry', 'vectors', 'matrices'];
const LANGS = ['English', 'Hindi', 'Tamil', 'Telugu', 'Marathi', 'Bengali', 'Kannada', 'Gujarati', 'Malayalam', 'Punjabi'];
const QUALS: [RegExp, string][] = [[/\bb\.?\s?sc\b/i, 'B.Sc'], [/\bm\.?\s?sc\b/i, 'M.Sc'], [/\bb\.?\s?ed\b/i, 'B.Ed'], [/\bb\.?\s?tech\b/i, 'B.Tech'], [/\biit\b/i, 'IIT graduate'], [/\bph\.?\s?d\b/i, 'PhD'], [/\bm\.?\s?a\b/i, 'M.A'], [/\bca\b/i, 'Chartered Accountant']];

export function extractProfile(text: string): Extracted {
  const t = ` ${text} `;
  // "in English" is the medium, not a subject, unless they say they teach English.
  const englishAsMedium = /\bin english\b/i.test(t) && !/\bteach(ing)?\s+english\b/i.test(t);
  const subjects = SUBJECTS.filter(([re, n]) => re.test(t) && !(n === 'English' && englishAsMedium)).map(([, n]) => n);
  const grades = new Set<number>();
  for (const m of t.matchAll(/(?:class(?:es)?|grades?|std\.?)\s*(\d{1,2})\s*(?:(?:[-–—]|to|and|&)\s*(\d{1,2}))?/gi)) {
    const a = Number(m[1]); const b = m[2] ? Number(m[2]) : a;
    for (let g = Math.min(a, b); g <= Math.max(a, b) && g <= 12; g++) if (g >= 1) grades.add(g);
  }
  const exams = EXAMS.filter(([re]) => re.test(t)).map(([, n]) => n);
  const topics = TOPICS.filter((x) => new RegExp(`\\b${x}\\b`, 'i').test(t)).map((x) => x.replace(/\b\w/g, (c) => c.toUpperCase()));
  const y = t.match(/(\d{1,2})\+?\s*(?:years?|yrs?)/i);
  const languages = LANGS.filter((l) => new RegExp(`\\b${l}\\b`, 'i').test(t) && !(l === 'English' && subjects.includes('English') && !/\bin english\b|english and|, english/i.test(t)));
  const audiences = [/school|class|grade|board/i.test(t) && 'school', exams.some((e) => ['JEE', 'NEET', 'SAT', 'CUET', 'Olympiad'].includes(e)) && 'competitive_exam', /college|university|undergrad/i.test(t) && 'college'].filter(Boolean) as string[];
  const helpTypes = [/concept|understand|basics|fundamentals|good at/i.test(t) && 'concept_learning', exams.length && 'exam_prep', /homework|assignment/i.test(t) && 'homework'].filter(Boolean) as string[];
  const styles = [/concept|basics|fundamentals|why/i.test(t) && 'concept_first', /practice|problems|drill/i.test(t) && 'practice_first', /question|socratic/i.test(t) && 'socratic', exams.length && 'exam_focused'].filter(Boolean) as string[];
  return { subjects, grades: [...grades].sort((a, b) => a - b), exams, topics, years: y ? Number(y[1]) : null, qualifications: QUALS.filter(([re]) => re.test(t)).map(([, n]) => n), languages, audiences, helpTypes, styles };
}

export const EXAMPLE_INTRO = "I've been teaching mathematics for 6 years. I mostly teach Class 9–12 students preparing for JEE. I'm particularly good at algebra and calculus.";
