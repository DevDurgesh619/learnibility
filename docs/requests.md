# Requests for shared files

Add a heading per request: who asks, which file, what change, why. The owner marks it done.

## W2-T → W4 catalogues: Rahul Verma must teach Cambridge grade 8 maths (2026-11-18)
- File: `data/catalogues/tutors.json`, `tut_rahul_verma`.
- Change: in his `maths` subject add grade `8` (board `cambridge` is already there) and topic strengths `fractions`, `integers`, `number`.
- Why: the W2-T acceptance flow is "Ishita (Cambridge grade 8, maths G1 gaps on fractions and integers) books Rahul Verma". Today `matchTutors` drops Rahul for her gaps because he teaches grades 9–12 only, so he can never be recommended to her.
- Done 2026-11-18 by W4 (commit ad6e358): Rahul now teaches maths for CBSE and Cambridge grades 8-12, with fractions, integers and number added to his topic strengths.

## W2-0 data layer → W1: "Reset demo" in the user menu (2026-11-18)
- File: `components/shell/app-shell.tsx`.
- Change: a "Reset demo" button in the top bar, a plain form POSTing to `/api/demo-reset`.
- Done 2026-11-18 by W1: icon button (rotate arrow, title "Reset demo") between the persona name and "Switch persona"; the route redirects back to the current page.

## W2-S1 → W2-0 data layer: Zoya on the login picker and in fixtures (2026-11-18)
- File: `data/fixtures/personas.json` (or `data/personas/index.json` via Wave 3).
- Change: add `lrn_zoya_fernandes` (student, Zoya Fernandes, grade 9, CBSE, stream none, story "Signed up today; onboarding not done yet"). No student.json: W2-S1's onboarding writes her full Student record.
- Why: sign-up (`/signup`) logs the new user in as Zoya; `RoleLayout` redirects to /login when `getPersona` cannot find her, so after onboarding she cannot reach `/student`.

## W2-S1 → W1 foundations: landing page and Home links (2026-11-18)
- File: `app/page.tsx`.
- Change: either redirect `/` to `/welcome` (W2-S1's PDF 1a landing, `app/(entry)/welcome`), or point its "Try the demo" button at `/signup` and add a "Get started" link there. Keep `/login` reachable (the 1b screen links "Demo persona picker").
- Why: PDF 1a → 1b; the new-user demo starts at the landing page.
- Done 2026-11-18 by W1 (commit 3c0d3e9): `/` redirects to `/welcome`.

## W2-S1 → everyone assigning tests (teacher, tutor, counsellor): how a test task opens (2026-11-18)
- A `Task` with `kind: 'test'` and `questionIds` opens at `/student/assessments/task.{taskId}` (overview → instructions → full-screen test). Submitting it writes the attempt with `taskId` and `assignedBy` = `task.createdBy`, marks the task done and calls `recomputeLearner`.
- For a whole chapter check use `href: '/student/assessments/chk.{chapterId}'` (practice forms `pfa.{chapterId}` / `pfb.{chapterId}`); the task is closed when that test is submitted.

## W2-S1 → W1: root URL opens the landing (2026-11-18)
- File: `app/page.tsx`.
- Change: `/` redirects to `/welcome` (PDF 1a landing); `/login` stays the persona picker.
- Done 2026-11-18 by W1.

## W2-A → W1 foundations: sidebar label for Application Support (2026-11-18)
- File: student sidebar nav config.
- Change: for students on the `application_support` plan, label the universities entry "Application Support", link it to `/student/applications` and highlight it on `/student/applications/**` and `/student/universities/**`. Free students keep "Universities" → `/student/universities`.
- Why: PDF 7a; paid students land on the command center, free ones on the explorer (which redirects paid users).
- Done 2026-11-18 by W1: `navFor(role, { plan })` in `lib/nav.ts`; students on `application_support` or `full_package` see "Application Support" → `/student/applications`, active on `/student/applications/**` and `/student/universities/**`. Free students keep "University Fit" → `/student/universities` (the blueprint's name). Checked as Nikhil (paid) and Kabir (free).
