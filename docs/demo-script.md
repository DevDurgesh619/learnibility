# Learnibility demo script

_Generated from `components/demo/scenarios.ts` by `npx tsx scripts/e2e/build-demo-script.ts`. Edit the scenarios file, not this one._

## Before you start

- Run the app (`npm run dev`) and open **http://localhost:3000/demo**.
- Each scenario card has **Reset and start**: it clears every demo write (tests taken, bookings, approvals, conversions), logs you in as the right person and opens that scenario's first screen.
- A **Demo guide** panel follows you around the app with the numbered steps. Each step's link switches to the right person and screen; **Next step** moves on. Close it with the X. On a phone it starts collapsed; tap its title to open it.
- **Reset demo** at the top of `/demo` (or the circular-arrow icon in any app header) clears demo writes without starting a scenario.
- The demo clock is fixed at Wednesday 18 November 2026, 9:00 AM India time. All people, schools, prices and data are fictional; prices are sample values.
- `/login` lets you log in as anyone directly, outside a scenario.

## Scenarios at a glance

| # | Scenario | Log in as | Start at | Roles |
| --- | --- | --- | --- | --- |
| 1 | Lead to student | Aman Gupta | `/crm` | Sales, Student |
| 2 | Kabir: careless and over-confident | Kabir Singh | `/student` | Student |
| 3 | Rohan: free plan fails, paid tutor suggested | Rohan Das | `/student` | Student, Parent, Tutor |
| 4 | Ishita books Rahul Verma | Ishita Rao | `/student/tutors` | Student, Tutor |
| 5 | Vihaan: Chemistry retention | Vihaan Joshi | `/student` | Student |
| 6 | Teacher finds a G3 cluster | Suresh Pillai | `/teacher` | Teacher, Student |
| 7 | Counsellor approves a change and runs a career session | Heena Qureshi | `/counsellor` | Counsellor, Student |
| 8 | Nikhil's application | Nikhil Reddy | `/student/applications` | Student, Counsellor |
| 9 | Ananya: University Fit to Application Support | Ananya Kapoor | `/student/universities` | Student |
| 10 | Meera: wellbeing, seen by the right people | Heena Qureshi | `/counsellor/risk-flags` | Counsellor, Parent |
| 11 | Aarav: topper, stretched | Aarav Kapoor | `/student` | Student, Parent |
| 12 | Tara and Kunal: careers from strengths | Tara Menon | `/student/career` | Student, Mentor |

## 1. Lead to student

A sales rep closes Zoya's family, converts the lead, and Zoya onboards and gets a personal plan.

**Log in as:** Aman Gupta  
**Start at:** `/crm`

1. **Sales dashboard** at `/crm`. Funnel by stage, leads by source, revenue this month and follow-ups due today.
2. **Open Zoya Fernandes' lead** at `/crm/leads`. Leads, search "Fernandes". The timeline shows every call, WhatsApp and the proposal sent.
3. **Record the payment**. On the lead, Record payment, mark it paid. An invoice with the GST line is created.
4. **Convert to platform**. Convert to platform assigns the counsellor and creates the subscription. Then Open in platform.
5. **Zoya onboards** (switch to Zoya Fernandes) at `/onboarding/about`. About, needs and profile, then the starting test.
6. **Take the starting test** at `/onboarding/test`. Answer a few items, then "Answer the rest for me (demo)" on each part.
7. **Home fills in** at `/student`. Gaps, plan, timetable and the next best action, all from her test.
8. **Back in sales** (switch to Aman Gupta) at `/crm`. The funnel and revenue now count Zoya as converted.

**Point out**

- One record from first enquiry to first lesson: nothing is typed twice.
- Follow-up rules (48 h nudge, demo reminders, payment chase) are shown and simulated, not sent.
- Zoya's starting profile comes from one 40-minute test, at low confidence until evidence builds.

## 2. Kabir: careless and over-confident

A chapter check finds G4 careless and G9 over-confidence; the plan uses estimate-first practice and the week re-plans.

**Log in as:** Kabir Singh  
**Start at:** `/student`

1. **Home** at `/student`. Mastery, MCI (confidence calibration) trending up, and the next best action.
2. **Take the in-class chapter check** at `/student/assessments`. Assessments, the chapter his class is on now. Answer quickly and confidently.
3. **Gap analysis**. After submit, open Gap analysis: G4 (careless) and G9 (over-confident) with the evidence for each.
4. **Topic detail**. Open a topic: "why you chose this", free plan steps with estimate-first practice, a matched tutor.
5. **Timetable re-plans** at `/student/timetable`. The week now holds the new practice blocks; the change log says why.

**Point out**

- Every gap code comes with the answer pattern that triggered it, not a guess.
- Estimate-first means he predicts the answer before solving, which trains calibration.
- The timetable is rebuilt by the engine after every test, inside his free slots.

## 3. Rohan: free plan fails, paid tutor suggested

Three weeks of free plan without recovery triggers a paid tutor suggestion; his parent approves and sees the spend.

**Log in as:** Rohan Das  
**Start at:** `/student`

1. **Rohan's home** at `/student`. Open gaps across chapters and the "paid tutor recommended" next action.
2. **His tutor request** at `/student/tutors`. Explore Tutors shows the matched tutors and the request waiting for his parent.
3. **Parent: Plan and spend** (switch to Anita Das) at `/parent/plan`. "Free plan has run 3 weeks" with the hours and rupees each gap costs.
4. **Approve the tutor**. Approve. The booking now waits for the tutor to accept.
5. **Spend shows** at `/parent/payments`. Sessions and payments lists the booking and what it will cost.

**Point out**

- The 3-week rule is an engine rule, not a sales nudge: free help first, paid only when it has not worked.
- The parent sees cost and progress, never wellbeing check-ins (T3).

## 4. Ishita books Rahul Verma

Ishita books a tutor, Rahul accepts with her gap snapshot, files a session report, and homework lands in her tasks.

**Log in as:** Ishita Rao  
**Start at:** `/student/tutors`

1. **Explore tutors** at `/student/tutors`. Matched on her G1 gaps (fractions, integers), style, budget and free slots.
2. **Book Rahul Verma**. Open Rahul's profile, Book, choose a slot, share the gap snapshot.
3. **Rahul sees the request** (switch to Rahul Verma) at `/tutor`. Home lists the request with her gap snapshot. Accept it.
4. **Run the session report** at `/tutor/sessions`. Sessions, open Ishita's session, Report: what was covered, and set homework.
5. **Homework in her tasks** (switch to Ishita Rao) at `/student/assessments`. Back as Ishita: the homework is in her tasks and her timetable.

**Point out**

- The tutor gets the diagnosis, not just a name: they start the first session knowing the gaps.
- The report and homework write back into the same record the student's plan reads.

## 5. Vihaan: Chemistry retention

A JEE aspirant whose Chemistry fades between tests gets spaced reviews built into his timetable.

**Log in as:** Vihaan Joshi  
**Start at:** `/student`

1. **Home** at `/student`. Strong Maths, Chemistry flagged for retention (R under 0.7).
2. **Retention gaps** at `/student/assessments`. Assessments, the latest Chemistry result, Gap analysis: G6 retention.
3. **Spaced reviews** at `/student/timetable`. Timetable: short review blocks spaced 1, 3 and 7 days after each Chemistry topic.
4. **His tutor** at `/student/sessions`. Sessions shows his Chemistry tutor and the last report.

**Point out**

- Retention is measured by 7-day probes, so "forgot it" is evidence, not a feeling.
- Reviews are short and placed by the forgetting curve, not added as extra hours.

## 6. Teacher finds a G3 cluster

Suresh Pillai spots several students with the same procedural gap and assigns one re-teach set.

**Log in as:** Suresh Pillai  
**Start at:** `/teacher`

1. **Class heatmap** at `/teacher`. 9A Maths: students by subtopics, coloured by mastery.
2. **Class gaps** at `/teacher/class-gaps`. A G3 cluster on one subtopic, with the students in it.
3. **Assign a re-teach set** at `/teacher/assign`. Assign the re-teach set to the cluster.
4. **Validate a gap** at `/teacher/gap-log`. Gap log: confirm or correct a diagnosis. It is written to the record as teacher-validated.
5. **Kabir sees it** (switch to Kabir Singh) at `/student/assessments`. As Kabir, the re-teach set is in his tasks.

**Point out**

- Teachers see T1 data only: mastery and gaps, never wellbeing or family details.
- One click turns a class pattern into individual tasks.

## 7. Counsellor approves a change and runs a career session

Heena approves a timetable change request, then runs Sara's career session: CA vs Data Analyst with time and cost.

**Log in as:** Heena Qureshi  
**Start at:** `/counsellor`

1. **Caseload** at `/counsellor`. All students with flags and what needs Heena today.
2. **Approve a timetable request** at `/counsellor/timetable-requests`. Kabir's pending request; approve it and the week re-plans.
3. **Sara's career session** at `/counsellor/career-sessions`. Career sessions, Sara: CA vs Data Analyst, skill gaps, years and rupees for each route.
4. **Save action items**. Save notes; action items become tasks for Sara.
5. **Sara's view** (switch to Sara Khan) at `/student/career`. Career: the comparison and her new tasks.

**Point out**

- The comparison uses her real strengths (Accountancy) and gaps (Economics G2), not a generic quiz.
- Approving a request calls the same timetable engine the student uses.

## 8. Nikhil's application

A full Application Support subscriber: QA check, an essay comment round trip with Farah, then submit.

**Log in as:** Nikhil Reddy  
**Start at:** `/student/applications`

1. **Command center** at `/student/applications`. Universities, board and deadlines. Leeds is due 28 Nov with open items.
2. **QA check**. Open the Leeds application and run the QA check: what is missing before submit.
3. **Essay** at `/student/applications/essays`. Essays: versions, the AI pre-pass and anchored comments.
4. **Farah reviews** (switch to Farah Siddiqui) at `/counsellor/draft-reviews`. Draft reviews: add a comment on the essay.
5. **Nikhil replies and submits** (switch to Nikhil Reddy) at `/student/applications`. Resolve the comment, then submit the application once QA is clear.

**Point out**

- The deadline risk flag fires because the due date is under 14 days with open items.
- Comments are anchored to the exact sentence, across versions.

## 9. Ananya: University Fit to Application Support

A topper uses the free University Fit, sees reach, target and safe options, and is offered the paid upgrade.

**Log in as:** Ananya Kapoor  
**Start at:** `/student/universities`

1. **University Fit** at `/student/universities`. The free explorer with saved universities.
2. **Best Fit** at `/student/universities/best-fit`. Run Best Fit: reach, target and safe with the reason for each.
3. **A university**. Open one: requirements, deadlines and what she is missing.
4. **Upgrade** at `/student/applications/upgrade`. Application Support: what the paid plan adds and its price (sample pricing).

**Point out**

- Free tools are genuinely useful; the upgrade is offered, not forced.
- Prices are sample values kept in one config file.

## 10. Meera: wellbeing, seen by the right people

Meera's wellbeing check is visible to her counsellor in full and to her parent only as a summary.

**Log in as:** Heena Qureshi  
**Start at:** `/counsellor/risk-flags`

1. **Risk flags** at `/counsellor/risk-flags`. Meera's wellbeing flag (time pressure, under-confidence).
2. **Student 360** at `/counsellor/student-360`. Meera's full profile: each value with its source, confidence and tier.
3. **Parent's view** (switch to Iyer) at `/parent`. Home and Privacy: a summary only, no T3 values.
4. **Privacy and consent** at `/parent/privacy`. What is collected, who sees it, dated consents.

**Point out**

- T3 (screened wellbeing) data is visible only to the counsellor. Parents, teachers and tutors never get it.
- Consent is per purpose and can be withdrawn from the parent screen.

## 11. Aarav: topper, stretched

A strong learner gets advanced readiness, a compressed timetable and olympiad enrichment instead of more of the same.

**Log in as:** Aarav Kapoor  
**Start at:** `/student`

1. **Home** at `/student`. Excellent band, LRS about 0.84, advanced-topic readiness high.
2. **Timetable** at `/student/timetable`. Compressed: fewer hours for mastered work, enrichment blocks added.
3. **Enrichment** at `/student/inventory`. Inventory and career: olympiad preparation and resources.
4. **One parent, two children** (switch to Neha Kapoor) at `/parent`. Neha Kapoor switches between Aarav and Ananya.

**Point out**

- Personalisation works both ways: stretch for toppers, support for strugglers.
- Siblings share one parent account.

## 12. Tara and Kunal: careers from strengths

Tara's app projects become her portfolio; Kunal's debating and leadership point to careers, with language support for his G7 gap.

**Log in as:** Tara Menon  
**Start at:** `/student/career`

1. **Tara's careers** at `/student/career`. Software and CS careers ranked from her strengths.
2. **Portfolio** at `/student/inventory`. Inventory: code projects filed as application documents.
3. **Applications** at `/student/applications`. CS applications to the US and Canada; essay gaps flagged.
4. **Kunal's careers** (switch to Kunal Verma) at `/student/career`. Law, policy, public speaking: careers that use debating and leadership.
5. **Language support** at `/student`. His G7 language gap and the support plan (moved from Hindi medium).
6. **Mentor view** (switch to Kelvin Thomas) at `/mentor/skill-plans`. Kelvin's skill plans for Kunal.

**Point out**

- Weak marks do not mean weak prospects: careers come from strengths, not only scores.
- G7 language gaps get language support, not more subject drills.
