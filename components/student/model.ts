/**
 * View-model types for the student daily loop (W2-S2): Home, Timetable, Inventory, Career, Sessions.
 * Pages build these in components/student/load.ts from lib/data reads and lib/engines; components only render them.
 */
import type { TimetableBlock } from '@/lib/engines';
import type { GapCode } from '@/lib/types';

export type StudentPlan = 'free' | 'counselling' | 'application_support' | 'full_package';

/** Plans that include a counsellor, so the student may request a timetable change (PDF 3a/3b). */
export const PLANS_WITH_COUNSELLOR: StudentPlan[] = ['counselling', 'application_support', 'full_package'];

export const PLAN_LABEL: Record<StudentPlan, string> = {
  free: 'Free',
  counselling: 'Counselling',
  application_support: 'Application Support',
  full_package: 'Full package',
};

export type MetricKey = 'learning-rate' | 'retention' | 'discipline' | 'task-completion';

export const METRICS: { key: MetricKey; label: string; how: string }[] = [
  {
    key: 'learning-rate',
    label: 'Learning rate',
    how: 'Your Learning Rate Score from tests: how much you gained, kept and could apply, per hour spent (ALR method).',
  },
  {
    key: 'retention',
    label: 'Retention',
    how: 'Marks on 7-day review questions ÷ marks when you first learned the topic.',
  },
  {
    key: 'discipline',
    label: 'Discipline',
    how: 'Study blocks you started on the planned day ÷ study blocks planned.',
  },
  {
    key: 'task-completion',
    label: 'Task completion',
    how: 'Tasks marked done ÷ tasks that were due, including homework and to-dos.',
  },
];

export interface MetricPoint { x: string; value: number | null }

export interface MetricSummary {
  key: MetricKey;
  label: string;
  /** 0 to 1, or null with `emptyReason` when there is no evidence yet. */
  value: number | null;
  /** Change vs last week, in points (0.04 = +4). */
  delta: number | null;
  emptyReason?: string;
}

export interface TaskItem {
  id: string;
  title: string;
  /** "Today 4:00 pm", "30 min" */
  meta?: string;
  kind: TimetableBlock['kind'] | 'homework' | 'todo' | 'application';
  done: boolean;
  href?: string;
  /** Tag shown at the end, e.g. "app" for application to-dos (PDF 2c). */
  tag?: string;
}

export interface SessionItem {
  id: string;
  personId: string;
  personName: string;
  role: 'counsellor' | 'tutor' | 'mentor';
  /** "Counsellor", "Maths tutor" */
  roleLabel: string;
  title: string;
  /** "Session 8", "Free demo" */
  label?: string;
  startUtc: string;
  endUtc: string;
  platform: string;
  topic?: string;
  status: 'scheduled' | 'completed' | 'missed' | 'cancelled';
  summary?: string;
}

export interface PersonCard {
  id: string;
  role: 'counsellor' | 'tutor' | 'mentor';
  name: string;
  /** "Main counsellor", "Maths", "Career" */
  focus: string;
  sinceUtc: string;
  sessionCount: number;
}

export interface TodoItem {
  id: string;
  fromPersonId: string;
  title: string;
  dueOn?: string;
  status: 'pending' | 'done' | 'removed';
}

export interface ApplicationCard {
  id: string;
  title: string;
  /** "Fall '27" */
  intake?: string;
  progress: number;
  deadlineUtc?: string;
  note: string;
  status: string;
  atRisk: boolean;
}

export interface NextActionView {
  title: string;
  reason: string;
  href?: string;
  cta: string;
  kind: string;
}

export interface GapView {
  id: string;
  subtopicId: string;
  title: string;
  subject: string;
  code: GapCode;
  hoursToClose: number;
  status: string;
}
