import type { Career, EntranceExam, Resource, Skill, Tutor } from '../../types/catalogue';

export function tutor(over: Partial<Tutor> & { id: string }): Tutor {
  return {
    firstName: 'A', lastName: 'B', displayName: over.id, gender: 'male', city: 'Delhi', timeZone: 'Asia/Kolkata', headline: '', bio: '',
    qualifications: [], yearsExperience: 5,
    subjects: [{ subjectSlug: 'maths', boards: ['cbse'], grades: [8, 9, 10], topicStrengths: ['square-roots', 'algebra'] }],
    examPrep: [], audiences: ['school'], helpTypes: ['concept_learning'], teachingStyles: ['concept_first', 'socratic'],
    formats: ['one_to_one', 'group'], modes: ['online'], languages: ['English', 'Hindi'], homework: 'weekly', idealStudent: '',
    availability: [{ day: 'mon', start: '17:00', end: '20:00' }, { day: 'wed', start: '17:00', end: '20:00' }],
    sessionMinutes: 60, maxSessionsPerDay: 4,
    pricing: { oneToOnePerHourInr: 800, groupPerStudentPerHourInr: 350, groupSize: [3, 6], demoInr: 0, demoMinutes: 30, packages: [] },
    platformFeeRate: 0.15, rating: 4.8, reviewsCount: 120, rebookPct: 80, sessionsCompleted: 900, responseTimeHours: 2, verified: true,
    verification: { identity: true, qualification: true, experience: true }, joinedOn: '2024-01-01', profileStrengthPct: 90, reviews: [],
    ...over,
  };
}

export const skills: Skill[] = [
  { id: 'skill-programming', name: 'Programming', kind: 'technical', category: 'Digital', description: '', levelDescriptors: ['a', 'b', 'c', 'd', 'e'], hoursPerLevel: [20, 40, 80, 150, 300], subjectSlugs: [], profileParamIds: ['p215'], resourceIds: ['res-cs50'] },
  { id: 'skill-algebra', name: 'Algebra', kind: 'academic', category: 'Quantitative', description: '', levelDescriptors: ['a', 'b', 'c', 'd', 'e'], hoursPerLevel: [10, 20, 30, 40, 60], subjectSlugs: ['maths'], profileParamIds: [], resourceIds: [] },
  { id: 'skill-communication', name: 'Communication', kind: 'future', category: 'Communication', description: '', levelDescriptors: ['a', 'b', 'c', 'd', 'e'], hoursPerLevel: [10, 15, 25, 40, 60], subjectSlugs: [], profileParamIds: ['p210'], resourceIds: [] },
];

export const resources: Resource[] = [
  { id: 'res-cs50', kind: 'free_resource', title: 'CS50', provider: 'Harvard', format: 'course', url: '', description: '', subjectSlugs: [], boards: [], grades: [], skillOutcomes: [{ skillId: 'skill-programming', toLevel: 3 }], examIds: [], topicTags: [], hours: 100, priceInr: 0, language: ['English'], certificate: false },
  { id: 'course-python-pro', kind: 'paid_course', title: 'Python Pro', provider: 'X', format: 'course', url: '', description: '', subjectSlugs: [], boards: [], grades: [], skillOutcomes: [{ skillId: 'skill-programming', toLevel: 4 }], examIds: [], topicTags: [], hours: 120, priceInr: 12000, language: ['English'], certificate: true },
  { id: 'course-cheap', kind: 'paid_course', title: 'Cheap intro', provider: 'Y', format: 'course', url: '', description: '', subjectSlugs: [], boards: [], grades: [], skillOutcomes: [{ skillId: 'skill-programming', toLevel: 2 }], examIds: [], topicTags: [], hours: 30, priceInr: 2000, language: ['English'], certificate: true },
];

export const exams: EntranceExam[] = [
  { id: 'jee-main', name: 'JEE Main', fullName: '', kind: 'india_entrance', conductedBy: 'NTA', sittings: ['Jan', 'Apr'], typicalGrade: 12, subjects: [], feeInr: 1000, prepHours: 800, scoreFormat: '', website: '' },
];

export function career(over: Partial<Career> & { id: string }): Career {
  return {
    title: over.id, cluster: 'Technology', summary: '', dayInLife: '', streams: ['science'], riasec: ['I', 'R', 'C'], aptitudeParamIds: ['p62', 'p65'],
    subjects: [{ subjectSlug: 'maths', minPercent: 75, required: true }, { subjectSlug: 'physics', minPercent: 70, required: false }],
    skills: [{ skillId: 'skill-programming', targetLevel: 4, importance: 'core' }, { skillId: 'skill-communication', targetLevel: 3, importance: 'helpful' }],
    pathways: [
      { id: 'x-india', label: 'B.Tech via JEE Main', region: 'india', country: 'in', stream: 'science', examIds: ['jee-main'], degree: 'B.Tech', steps: [], yearsToEntry: 4, costInr: { low: 400000, typical: 1000000, high: 2500000 }, costNote: '', universityIds: [] },
      { id: 'x-us', label: 'BS in the US', region: 'abroad', country: 'us', stream: 'science', examIds: ['sat'], degree: 'BS', steps: [], yearsToEntry: 4, costInr: { low: 8000000, typical: 25000000, high: 40000000 }, costNote: '', universityIds: [] },
    ],
    salaryInr: { entryLow: 600000, entryHigh: 1500000, mid: 2500000, senior: 5000000 }, demand: 'very_high', growthPct: 12, topCities: [], topRecruiters: [], workStyle: [], relatedCareerIds: [], sources: [],
    ...over,
  };
}
