import { NextResponse } from 'next/server';
import { DEMO_COOKIE } from '@/components/demo/scenarios';

/** POST /demo/exit: hides the Demo guide panel and goes back to the page it was closed on. */
export async function POST(req: Request) {
  const back = req.headers.get('referer') ?? '/demo';
  const res = NextResponse.redirect(new URL(back, req.url), 303);
  res.cookies.delete(DEMO_COOKIE);
  return res;
}
