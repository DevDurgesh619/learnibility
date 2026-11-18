# Deploying the demo to Vercel

One shareable link for every flow: `/demo` (12 guided scenarios), `/login` (persona picker) and Reset demo.

## Steps
1. vercel.com/new, sign in with GitHub, import `DevDurgesh619/learnibility`.
2. Framework preset: Next.js (auto-detected). Leave build, install and output settings on their defaults.
   Vercel runs `npm run vercel-build`, which packs the question banks and then runs `next build`.
3. No environment variables are needed. Click Deploy (about 3 to 5 minutes).
4. Open `https://<project>.vercel.app/demo`.

## How it differs from local
- **Question banks** (data/questions, ~185 MB of JSON) are packed to minified `*.json.gz` (~22 MB) during the
  Vercel build only (`scripts/vercel/pack-data.mjs`). `lib/data/source.ts` reads both forms. Each server
  function is about 68 MB, well under Vercel's 250 MB limit. The repository keeps the readable JSON.
- **Demo writes** (attempts, tasks, bookings, approvals...) live in server memory on Vercel instead of SQLite
  (`LEARNIBILITY_OVERLAY` defaults to `memory` when `VERCEL` is set). They last while the instance is warm.
  After roughly 5 to 15 idle minutes, or a redeploy, the next visit starts from the seeded data, as if Reset
  had been pressed. Start a scenario from `/demo` again if that happens.
- **Reset** clears the instance that receives it and stamps a `learnibility_reset` cookie; every page instance
  clears its own writes the first time it sees a newer stamp (`syncResetEpoch` in `lib/store/overlay.ts`).
  This is needed because Vercel runs route handlers and pages as separate functions.
- Writes are shared by everyone using the same deployment at the same time. That is fine for one presenter.

## Check a Vercel-style build locally
    npx vercel build --yes        # needs a .vercel/project.json; runs pack-data, so use a throwaway copy
    VERCEL=1 npx next start -p 3100
    BASE_URL=http://localhost:3100 npx tsx scripts/e2e/demo.spec.ts
