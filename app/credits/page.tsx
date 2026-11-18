import type { Metadata } from 'next';
import Link from 'next/link';
import { Logo } from '@/components/shell/logo';
import { Avatar } from '@/components/ui/avatar';
import { Card, CardBody, CardHeader } from '@/components/ui/card';
import { SafeImg } from '@/components/ui/safe-img';
import { PERSON_PHOTOS, UNI_PHOTOS } from '@/lib/media';
import { getUniversity } from '@/lib/data';

export const metadata: Metadata = { title: 'Photo credits · Learnibility' };

/** Credits for every bundled photo: Unsplash portraits (Unsplash License) and Wikimedia Commons campus photos (their own licences). */
export default function CreditsPage() {
  const people = Object.entries(PERSON_PHOTOS).sort((a, b) => a[1].name.localeCompare(b[1].name));
  const campuses = Object.entries(UNI_PHOTOS).map(([id, p]) => ({ id, p, name: getUniversity(id)?.name ?? id })).sort((a, b) => a.name.localeCompare(b.name));
  return (
    <div className="min-h-screen bg-canvas">
      <header className="border-b border-line bg-surface">
        <div className="mx-auto flex max-w-5xl items-center gap-3 px-4 py-4 sm:px-6"><Logo href="/login" /></div>
      </header>
      <main className="mx-auto max-w-5xl space-y-6 px-4 py-8 sm:px-6">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-ink">Photo credits</h1>
          <p className="mt-1 max-w-3xl text-sm text-muted">
            Learnibility is a demo. Every person in it is fictional: the profile photos are free stock portraits of models, not the characters,
            and the names, marks and stories are made up. Campus photos show the real universities.
          </p>
        </div>
        {campuses.length > 0 && (
          <Card>
            <CardHeader title="University campus photos" description="From Wikimedia Commons, under the licence shown for each. Click through for the original file." />
            <CardBody className="pt-3">
              <ul className="grid gap-3 sm:grid-cols-2">
                {campuses.map(({ id, p, name }) => (
                  <li key={id} className="flex items-center gap-3">
                    <SafeImg src={p.src} alt="" className="h-12 w-16 shrink-0 rounded-md object-cover" fallback={<span className="h-12 w-16 shrink-0 rounded-md bg-surface-muted" />} />
                    <div className="min-w-0 text-xs">
                      <p className="truncate font-medium text-ink">{name}</p>
                      <p className="truncate text-muted">
                        {p.author} · {p.licenseUrl ? <a className="underline" href={p.licenseUrl} target="_blank" rel="noreferrer">{p.license}</a> : p.license} ·{' '}
                        <a className="underline" href={p.sourceUrl} target="_blank" rel="noreferrer">source</a>
                      </p>
                    </div>
                  </li>
                ))}
              </ul>
            </CardBody>
          </Card>
        )}
        <Card>
          <CardHeader title="Profile photos" description={<>Portraits from <a className="underline" href="https://unsplash.com" target="_blank" rel="noreferrer">Unsplash</a>, free to use under the <a className="underline" href="https://unsplash.com/license" target="_blank" rel="noreferrer">Unsplash License</a>.</>} />
          <CardBody className="pt-3">
            <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {people.map(([id, p]) => (
                <li key={id} className="flex items-center gap-3">
                  <Avatar name={p.name} src={p.src} size="sm" />
                  <div className="min-w-0 text-xs">
                    <p className="truncate font-medium text-ink">{p.name}</p>
                    <p className="truncate text-muted">Photo by <a className="underline" href={`https://unsplash.com/photos/${p.unsplashId}`} target="_blank" rel="noreferrer">{p.photographer}</a></p>
                  </div>
                </li>
              ))}
            </ul>
          </CardBody>
        </Card>
        <p className="text-xs text-subtle"><Link href="/login" className="underline">Back to the demo</Link></p>
      </main>
    </div>
  );
}
