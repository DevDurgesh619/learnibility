import { redirect } from 'next/navigation';

/** The public landing (PDF screen 1a) lives at /welcome; /login is the persona picker for demos. */
export default function Home() {
  redirect('/welcome');
}
