import type { Role } from './types';

/** Icon keys map to lucide icons in components/shell/nav-icon.tsx. */
export type NavIcon =
  | 'home' | 'calendar' | 'folder' | 'users' | 'graduation' | 'clipboard' | 'compass' | 'video' | 'chart' | 'wallet'
  | 'briefcase' | 'message' | 'shield' | 'layers' | 'send' | 'grid' | 'user' | 'list' | 'alert' | 'file' | 'clock' | 'star';

export interface NavItem {
  /** URL segment under the role, '' for the role home. */
  slug: string;
  label: string;
  icon: NavIcon;
  /** One line shown on the placeholder until the screen is built. */
  blurb: string;
}

/** Sidebars from the blueprint, section "Role screens and flows". */
export const NAV: Record<Role, NavItem[]> = {
  student: [
    { slug: '', label: 'Home', icon: 'home', blurb: "Today's tasks, progress and your next best action." },
    { slug: 'timetable', label: 'Timetable', icon: 'calendar', blurb: 'Your week, re-planned after every test and missed task.' },
    { slug: 'inventory', label: 'My Inventory', icon: 'folder', blurb: 'Academics, activities, application documents and your job-ready profile.' },
    { slug: 'tutors', label: 'Explore Tutors', icon: 'users', blurb: 'Tutors matched to your gaps, style, budget and free slots.' },
    { slug: 'universities', label: 'University Fit', icon: 'graduation', blurb: 'Reach, target and safe universities with requirements and deadlines.' },
    { slug: 'assessments', label: 'Assessments', icon: 'clipboard', blurb: 'Onboarding, chapter checks, weekly tests and mocks with gap analysis.' },
    { slug: 'career', label: 'Career', icon: 'compass', blurb: 'Careers that fit you, and the skill gap with time and cost to get there.' },
    { slug: 'sessions', label: 'Sessions', icon: 'video', blurb: 'Tutor and counsellor sessions, reports and homework.' },
  ],
  parent: [
    { slug: '', label: 'Home', icon: 'home', blurb: 'This week at a glance for each child.' },
    { slug: 'progress', label: 'Progress', icon: 'chart', blurb: 'Mastery, gaps and learning rate by subject.' },
    { slug: 'plan', label: 'Plan and spend', icon: 'wallet', blurb: 'What each gap costs in time and rupees, and paid help to approve.' },
    { slug: 'timetable', label: 'Timetable', icon: 'calendar', blurb: "Your child's week." },
    { slug: 'payments', label: 'Sessions and payments', icon: 'clipboard', blurb: 'Tutor sessions, invoices and receipts.' },
    { slug: 'applications', label: 'Applications', icon: 'graduation', blurb: 'University deadlines and status, read only.' },
    { slug: 'messages', label: 'Messages', icon: 'message', blurb: 'Notes from counsellors, teachers and tutors.' },
    { slug: 'privacy', label: 'Privacy and consent', icon: 'shield', blurb: 'What is collected, who sees it, and your consents.' },
  ],
  teacher: [
    { slug: '', label: 'Classes', icon: 'layers', blurb: 'Your sections with a students × subtopics mastery heatmap.' },
    { slug: 'assign', label: 'Assign', icon: 'send', blurb: 'Assign a chapter check or a re-teach set.' },
    { slug: 'class-gaps', label: 'Class gaps', icon: 'grid', blurb: 'Gap clusters across the class, by subtopic and gap type.' },
    { slug: 'students', label: 'Students', icon: 'user', blurb: 'One student in depth: mastery, gaps and history.' },
    { slug: 'gap-log', label: 'Gap log', icon: 'list', blurb: 'Diagnoses to validate, as in the workbook Gap Log.' },
  ],
  counsellor: [
    { slug: '', label: 'Caseload', icon: 'users', blurb: 'Your students, with flags and what needs you today.' },
    { slug: 'student-360', label: 'Student 360', icon: 'user', blurb: 'The full profile with source and confidence for every parameter.' },
    { slug: 'timetable-requests', label: 'Timetable requests', icon: 'calendar', blurb: 'Schedule change requests to approve.' },
    { slug: 'career-sessions', label: 'Career sessions', icon: 'compass', blurb: 'Run a career session and save notes with action items.' },
    { slug: 'applications', label: 'Applications pipeline', icon: 'graduation', blurb: 'Every application on one board.' },
    { slug: 'draft-reviews', label: 'Draft reviews', icon: 'file', blurb: 'Essays waiting for your comments.' },
    { slug: 'risk-flags', label: 'Risk flags', icon: 'alert', blurb: 'Deadlines under 14 days with open items, wellbeing flags.' },
  ],
  tutor: [
    { slug: '', label: 'Home', icon: 'home', blurb: 'Requests, upcoming sessions and earnings this month.' },
    { slug: 'students', label: 'Students', icon: 'users', blurb: 'Your students and the gap snapshots they shared.' },
    { slug: 'sessions', label: 'Sessions', icon: 'video', blurb: 'Past and upcoming sessions with reports.' },
    { slug: 'today', label: 'Today', icon: 'clock', blurb: "Today's sessions with AI-prepared focus notes." },
    { slug: 'earnings', label: 'Earnings', icon: 'wallet', blurb: 'Payouts, platform fee and monthly trend.' },
    { slug: 'profile', label: 'Profile', icon: 'star', blurb: 'Your listing, availability and pricing.' },
  ],
  mentor: [
    { slug: '', label: 'Mentees', icon: 'users', blurb: 'Your mentees and their career goals.' },
    { slug: 'career-sessions', label: 'Career sessions', icon: 'compass', blurb: 'Session notes and action items.' },
    { slug: 'skill-plans', label: 'Skill plans', icon: 'briefcase', blurb: 'Skill gaps and the plan to close them.' },
    { slug: 'messages', label: 'Messages', icon: 'message', blurb: 'Conversations with mentees.' },
  ],
};

export const ROLE_LABEL: Record<Role, string> = {
  student: 'Student', parent: 'Parent', teacher: 'School teacher', counsellor: 'Counsellor', tutor: 'Tutor', mentor: 'Mentor',
};

export const roleHome = (role: Role) => `/${role}`;

export function navHref(role: Role, item: NavItem) {
  return item.slug ? `/${role}/${item.slug}` : `/${role}`;
}

export function findNavItem(role: Role, slug: string): NavItem | undefined {
  return NAV[role].find((i) => i.slug === slug);
}
