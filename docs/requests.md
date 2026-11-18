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
