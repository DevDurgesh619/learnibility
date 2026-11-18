import { NextResponse } from 'next/server';
import { getProfileValues, listParameters } from '@/lib/data';

/**
 * GET /demo/t3.json?learner=…: the names of this learner's T3 (screened wellbeing) parameters that hold a value.
 * scripts/e2e/privacy.spec.ts checks no parent, teacher, tutor, mentor or sales screen shows any of them.
 */
export function GET(req: Request) {
  const id = new URL(req.url).searchParams.get('learner') ?? '';
  const names = new Map(listParameters().map((p) => [p.id, p.name]));
  const t3 = getProfileValues(id).filter((v) => v.tier === 'T3' && v.value !== null && v.value !== undefined && v.value !== '');
  return NextResponse.json({ learner: id, names: [...new Set(t3.map((v) => names.get(v.paramId)).filter(Boolean))] });
}
