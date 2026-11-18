import parameters from '@/data/profile/parameters.json';

export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center gap-4 p-8">
      <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Learnibility</p>
      <h1 className="text-4xl font-semibold">Every learner, one verified record.</h1>
      <p className="text-slate-600">
        Foundations are in place: shared types, ID helpers and the {parameters.items.length}-parameter learner profile.
        The persona login and role areas arrive next.
      </p>
    </main>
  );
}
