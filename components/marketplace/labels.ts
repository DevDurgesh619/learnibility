import type { HelpType, HomeworkPolicy, SessionFormat, SessionMode, TeachingStyle, TutorAudience, Weekday } from '@/lib/types/catalogue';

export const STYLE_LABEL: Record<TeachingStyle, string> = {
  concept_first: 'Concept-first', practice_first: 'Practice-first', socratic: 'Socratic', exam_focused: 'Exam-focused', project_based: 'Project-based',
};
export const FORMAT_LABEL: Record<SessionFormat, string> = { one_to_one: '1-on-1', group: 'Group' };
export const MODE_LABEL: Record<SessionMode, string> = { online: 'Online', offline: 'In person' };
export const HELP_LABEL: Record<HelpType, string> = {
  concept_learning: 'Concept learning', exam_prep: 'Exam prep', homework: 'Homework', skill_development: 'Skill development',
};
export const AUDIENCE_LABEL: Record<TutorAudience, string> = {
  school: 'School students', competitive_exam: 'Competitive exam', college: 'College', english_learners: 'English learners', career_learners: 'Career learners',
};
export const HOMEWORK_LABEL: Record<HomeworkPolicy, string> = { every_session: 'Every session', weekly: 'Weekly', on_request: 'On request' };

export const WEEKDAYS: Weekday[] = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'];
export const DAY_LABEL: Record<Weekday, string> = { mon: 'Mon', tue: 'Tue', wed: 'Wed', thu: 'Thu', fri: 'Fri', sat: 'Sat', sun: 'Sun' };

/** "maths" → "Maths", "social-science" → "Social science", "applied-maths" → "Applied maths". */
export function subjectLabel(slug: string): string {
  const special: Record<string, string> = { maths: 'Maths', 'applied-maths': 'Applied maths', 'computer-science': 'Computer science', informatics: 'Informatics', environmental: 'Environmental systems', 'legal-studies': 'Legal studies', 'political-science': 'Political science', 'social-science': 'Social science' };
  if (special[slug]) return special[slug];
  const s = slug.replace(/-/g, ' ');
  return s[0]!.toUpperCase() + s.slice(1);
}

export const BOARD_LABEL = { cbse: 'CBSE', cambridge: 'Cambridge', ib: 'IB' } as const;

/** "rotational-motion" → "Rotational motion". */
export function tagLabel(tag: string): string {
  const s = tag.replace(/-/g, ' ');
  return s[0]!.toUpperCase() + s.slice(1);
}

/** "16:00" → "4 pm", "16:30" → "4:30 pm". */
export function clockLabel(hhmm: string): string {
  const h = Number(hhmm.slice(0, 2));
  const m = hhmm.slice(3, 5);
  const ap = h >= 12 ? 'pm' : 'am';
  const h12 = h % 12 === 0 ? 12 : h % 12;
  return m === '00' ? `${h12} ${ap}` : `${h12}:${m} ${ap}`;
}
