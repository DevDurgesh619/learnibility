# CRM lead funnel (W3-CRM)

A generic sales CRM inside Learnibility for the admissions team: lead to paid to onboarded, then hand-off to the core platform. No external calls and no third-party branding; every message, payment and follow-up is simulated and logged.

## Log in
`/login` → **Sales reps**: Priya Malhotra (manager), Aman Gupta, Neha Joseph. Routes live under `/sales` (the role home pattern `/{role}`), sidebar: Dashboard, Leads, Pipeline, Follow-ups, Payments, Conversions, Settings.

## Demo script (2 minutes)
1. Aman → Dashboard: funnel with stage conversion rates, revenue this month, leads by source, leaderboard, follow-ups due today. Note "Proposals awaiting payment": Maria Fernandes for Zoya.
2. Open Zoya's lead (`/sales/leads/lead_0013`): timeline from website form to demo to proposal; the 3-day rule's call task is due 11:00 today.
3. **Record payment** (UPI) → Closed won, invoice and receipt numbers, WhatsApp "payment received" logged.
4. **Convert to platform** → Converted; Zoya's learner record activated (Full package plan, Heena Qureshi as counsellor, parent Maria Fernandes), subscription and invoice filed, `crm_handoff` event on her record.
5. **Open Zoya in platform** → signed in as Zoya at `/onboarding/about`.
6. Back on the Dashboard (Switch persona → Aman): revenue this month +₹22,797 and won this month +1.

Reset demo (top bar) restores everything.

## Data
`npx tsx scripts/crm/build.ts` regenerates `data/crm/*.json` (seed `learnibility-2026:crm`, byte-identical reruns):
- `leads.json` 193 leads: 180 generic over the 90 days before DEMO_NOW plus 13 persona families (12 Converted before their history starts; Zoya's family at Proposal sent with payment pending today). Phones are fake (`+91 90000 0xxxx`), except returning demo sign-in numbers and Zoya's sign-up number 98765 43210.
- `activities.json` every stage change, call, WhatsApp/email template, demo, payment and hand-off (rep or `system`).
- `followups.json` from the rules in `rules.json` (welcome, no reply 48 h, demo 24 h and 1 h, no-show, proposal unpaid 3 days, nurture every 30 days, rep tasks).
- `payments.json` (pending, paid, failed; invoice `LRN/yyyy-yy/nnnn`, receipt, GST 18%), `conversions.json`, `subscriptions.json`, `team.json`, `templates.json`.
- **Prices**: `data/crm/packages.json` is hand-written and the only place to change what the CRM sells (dummy values; monthly rates follow the platform's Application Support 4,999 and Full package 7,999).

Persona family leads show the parent's platform name when the parent persona exists; for families W3-P has not created yet the CRM uses its own parent name (Radha Iyer, Sanjay Joshi, Deepa Nair, Rajesh Sharma, Anil Menon, Sunil Verma, Maria Fernandes).

## Code
- Types `components/crm/types.ts`; reads `lib/data/crm.ts` (JSON merged with the demo overlay, collections `crm_*`); writes `lib/actions/crm.ts`.
- Convert to platform writes through `lib/actions/core.ts`: `student`, `adults` (parent, counsellor caseload), `invoices`, `events` (`crm_handoff`, source M2). Zoya's existing persona is activated; other leads get a new learner with empty states that onboarding fills.
- Smoke: `BASE_URL=http://localhost:3000 node scripts/smoke/w3-crm.spec.ts` (24 routes at 1440 and 390 px for two reps, then the Zoya flow at both sizes). Screens in `docs/screens/w3-crm/`.

## Known limits
- New learners created from generic leads can't be signed into yet: `getPersona` reads only the JSON persona lists (request in docs/requests.md). Their records exist and show in the counsellor caseload.
- Persona families' starter payments are CRM-side only; the platform's parent invoices don't list them (W3-P may add them).
