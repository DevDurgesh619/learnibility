# Data layer (W2-0)

Screens read persona data only through `@/lib/data` and write only through `@/lib/actions/core` (or a thread's own `lib/actions/*.ts` that calls it). Both are server only.

## Reads (`import { ... } from '@/lib/data'`)

| Function | Returns |
| --- | --- |
| `getStudent(id)`, `listStudents()`, `getAdult(id)`, `listAdults(role?)`, `getPersonName(id)` | `Student`, `Adult` |
| `getProfile(id, viewerRole, opts?)` | `VisibleValue[]` filtered by `lib/visibility` (tutors: only `sharedParamIds`, taken from their bookings when `viewerId` is passed) |
| `getProfileValues(id)` | raw `ProfileValue[]` (engines only; never render for non-counsellor roles) |
| `getEvents(id, {type?, since?})`, `getEvidenceDensity(id)` | `EvidenceEvent[]`; filled params and events per 430 section. Wellbeing check-ins are events of type `wellbeing_checkin` (T3) |
| `getMastery(id, subjectId?)` | `MasteryRecord[]` |
| `getAlr(id)` | `{ chapters, history, overall }` |
| `getGaps(id, {status?: 'open' \| status \| status[], subjectId?})` | `GapRecord[]`, worst first; teacher validation on `validation` |
| `getPlans(id)`, `getCurrentPlan(id)` | `PlanRecord[]` (`plan` is the engine's `InterventionPlan`; `plan.paidTuition` is the 3-week rule) |
| `getTimetable(id, weekStart?)` | `TimetableWeek` (stored week, else built live by the engine) |
| `getTasks(id, date?, {range?, status?, source?, createdBy?})` | `Task[]` |
| `getTimetableRequests({learnerId?, counsellorId?, status?})` | `TimetableRequest[]` |
| `getAttempts(id, filter?)`, `getAttempt(attemptId)` | `Attempt[]` (responses inside) |
| `getSessions(personId, {from?, to?, status?})` | `Session[]` for a learner or a host (tutor, counsellor, mentor, teacher) |
| `getBookings(personId)`, `getTutorMatches(id, {subjectId?})` | `Booking[]`, engine `TutorMatch[]` |
| `getCareerMatches(id)` | `CareerMatches` (fits, shortlist, careerGap per shortlisted career) |
| `getApplications(id)`, `getApplication(appId)`, `getApplicationsPipeline(counsellorId)` | `{ applications, shortlist, meetings, finance }`; `riskFlags` computed on read |
| `getMeetingNotes(id, {staffId?, kind?})`, `getDocuments(id, folder?)`, `getInvoices(personId)`, `getConsents(id)`, `getMessages(personId, f?)`, `getComments(type, id)`, `getApprovals(f)` | as named |
| `getNextBestActions(id)` | engine `NextAction[]`, computed live |
| `getChildren(parentId)` | `ChildSummary[]` |
| `getSections(teacherId)`, `getSection(id)`, `getSectionHeatmap(sectionId, {chapterId?})` | `Section[]`; heatmap rows × subtopics + gap clusters |
| `getCaseload(staffId)` | `CaseloadEntry[]` with risk flags and "needs you today" |
| `getTutorWorkspace(tutorId)` | `TutorWorkspace` (students, bookings, sessions, assignments, messages, notes, payouts, earnings at 15% fee) |
| `getSubject`, `getChapter`, `getSubtopic`, `listSubjects`, `namesFor`, `getQuestions(filter)`, `getQuestion(id)` | curriculum (hours filled by the mastery-time engine) and questions (real bank, else fixture set) |
| `listTutors(f)`, `getTutor`, `listCareers`, `getCareer`, `listSkills`, `listExams`, `listResources`, `listUniversities(f)`, `getUniversity` | catalogues |
| `demoNow()`, `demoToday()`, `weekStartOf(date)` | demo clock helpers |

## Writes (`import { ... } from '@/lib/actions/core'`)

- `putRecord(collection, record)`: upsert. Collections: `student profile events attempts mastery alr gaps plans timetable tasks requests bookings sessions meetings careers applications shortlist finance documents invoices consents messages comments approvals assignments tutorNotes payouts adults sections tutorSettings`. Keys: `id` for most; `learnerId:paramId` (profile), `learnerId:subtopicId` (mastery), `learnerId:weekStart` (timetable), `learnerId` (careers).
- `appendEvent(learnerId, { sourceMethod, type, payload })`.
- `recomputeLearner(learnerId, { reason? })`: diagnoses new attempts (gaps, mastery, ALR), writes a new plan when gaps changed, re-plans this week's timetable. Call it after an attempt, an approved timetable request (`reason: 'request_approved'`), a booking (`'session_booked'`) or assigned tasks (`'task_assigned'`).
- `nowStamp()`, `newId(prefix)`: timestamps on the demo clock and ids for new records.
- `resetDemo()`; `POST /api/demo-reset` (form posts redirect back).

Writes land in an overlay (SQLite `.data/overlay.sqlite` via better-sqlite3; memory when SQLite is unavailable or `LEARNIBILITY_OVERLAY=memory`). Reads merge overlay over JSON. Reset deletes the overlay only.

## Files (contract for Wave 3 personas)

Per learner, `data/personas/students/{learnerId}/` (wins) or `data/fixtures/students/{learnerId}/`, each a `DataFile<T>` of the type in `lib/data/types.ts`:

`student.json` (Student, one item) · `profile.json` (ProfileValue) · `events.json` · `attempts.json` · `mastery.json` · `alr.json` · `gaps.json` · `plans.json` · `timetable.json` (TimetableWeek per week) · `tasks.json` · `requests.json` · `bookings.json` · `sessions.json` · `meetings.json` · `careers.json` (CareerMatches, one item) · `applications.json` · `shortlist.json` · `finance.json` · `documents.json` · `invoices.json` · `consents.json` · `messages.json` · `comments.json` · `approvals.json` · `assignments.json` · `tutorNotes.json`. Missing files read as empty.

Shared: `{personas|fixtures}/adults/*.json` (Adult), `{personas|fixtures}/classes/{sectionId}.json` (Section with background students). Persona folders win over fixtures.

Contributions: `data/fixtures/contrib/{thread}.json` = `{ schemaVersion: 1, generatedBy, collections: { applications: [...], sessions: [...] } }`. Screen threads may author demo content there in the same types; records of persona-backed learners are ignored.

Fixture people show on the login picker through `data/fixtures/personas.json` (merged into `listPersonas()`; the index wins on the same id).
