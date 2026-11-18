import { NextResponse } from 'next/server';
import { resetDemo } from '@/lib/actions/core';

/** POST /api/demo-reset: clears every demo write (overlay); JSON persona/fixture data is untouched. */
export async function POST(req: Request) {
  const { cleared } = resetDemo();
  // Plain form posts (the "Reset demo" menu item) get sent back where they came from.
  if ((req.headers.get('content-type') ?? '').includes('form')) {
    return NextResponse.redirect(new URL(req.headers.get('referer') ?? '/', req.url), 303);
  }
  return NextResponse.json({ ok: true, cleared });
}
