import { NextResponse } from 'next/server';
import { listPersonas } from '@/lib/data/personas';

/** GET /demo/personas.json: the persona picker list, for the E2E specs (ids, roles, linked learners). */
export function GET() {
  return NextResponse.json(listPersonas().map(({ id, role, name, linkedLearnerIds }) => ({ id, role, name, linkedLearnerIds })));
}
