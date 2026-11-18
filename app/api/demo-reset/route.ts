import { NextResponse } from 'next/server';
import { resetCookie, resetDemo } from '@/lib/actions/core';

/** POST /api/demo-reset: clears every demo write (overlay); JSON persona/fixture data is untouched. */
export async function POST(req: Request) {
  const { cleared, epoch } = resetDemo();
  // Plain form posts (the "Reset demo" menu item) get sent back where they came from.
  const res = (req.headers.get('content-type') ?? '').includes('form')
    ? NextResponse.redirect(new URL(req.headers.get('referer') ?? '/', req.url), 303)
    : NextResponse.json({ ok: true, cleared });
  res.cookies.set(resetCookie(epoch));
  return res;
}
