import { NextResponse } from 'next/server';
import { resetDemo } from '@/lib/actions/core';
import { DEMO_COOKIE } from '@/components/demo/scenarios';

/** POST /demo/reset: clears every demo write and the running scenario, then shows /demo with a confirmation. */
export async function POST(req: Request) {
  resetDemo();
  const res = NextResponse.redirect(new URL('/demo?reset=1', req.url), 303);
  res.cookies.delete(DEMO_COOKIE);
  return res;
}
