import Link from 'next/link';
import { Logo } from '@/components/shell/logo';
import { buttonVariants } from '@/components/ui/button';
import parameters from '@/data/profile/parameters.json';

export default function Home() {
  return (
    <div className="min-h-screen">
      <header className="mx-auto flex max-w-6xl items-center justify-between p-6">
        <Logo />
        <Link href="/login" className={buttonVariants({ variant: 'secondary', size: 'sm' })}>Log in</Link>
      </header>
      <main className="mx-auto flex max-w-3xl flex-col items-start gap-6 px-6 py-20">
        <p className="text-sm font-medium uppercase tracking-wide text-brand-600">Grades 8 to 12 · CBSE · Cambridge · IB</p>
        <h1 className="text-4xl font-semibold tracking-tight sm:text-5xl">Plan your studies, tests and university applications in one place.</h1>
        <p className="text-lg text-muted">
          Learnibility finds exactly where each student is stuck, builds the week around closing it, and connects students,
          parents, teachers, counsellors and tutors around one verified {parameters.items.length}-parameter learner record.
        </p>
        <Link href="/login" className={buttonVariants({ size: 'lg' })}>Try the demo</Link>
      </main>
    </div>
  );
}
