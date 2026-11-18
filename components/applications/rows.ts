import 'server-only';
import type { University } from '@/lib/types';
import type { UniRow } from './explorer';
import { mainRoute } from './fit';
import { fmtShort } from './logic';
import { COUNTRY_NAME, lakh } from './ui';

export function uniRow(u: University, saved: Set<string>, preferFields: string[] = []): UniRow {
  const route = mainRoute(u);
  const req = route?.requirements;
  const sat = req?.satMid50;
  const satLabel = req?.testPolicy === 'not_applicable' ? 'No SAT' : req?.testPolicy === 'blind' ? 'Test-blind' : sat ? `SAT ${sat[0]}+${req?.testPolicy === 'optional' ? ' (optional)' : ''}` : req?.testPolicy === 'optional' ? 'Test-optional' : 'Board marks';
  return {
    id: u.id,
    name: u.name,
    shortName: u.shortName,
    country: u.country,
    countryName: COUNTRY_NAME[u.country] ?? u.country.toUpperCase(),
    city: u.city,
    type: u.type,
    qsRank: u.qsWorldRank.value,
    acceptancePct: u.acceptanceRatePct.value,
    tuitionInr: u.tuitionInrPerYear,
    tuitionLabel: `${lakh(u.tuitionInrPerYear)} / yr`,
    fields: [...new Set(u.programmes.map((p) => p.field))],
    programmes: u.programmes.map((p) => p.name),
    satLabel,
    satLow: sat?.[0] ?? null,
    testOptional: req?.testPolicy !== 'required',
    ielts: req?.ielts ?? null,
    deadline: route?.deadline.value ?? '',
    deadlineLabel: route ? fmtShort(route.deadline.value) : '—',
    saved: saved.has(u.id),
    defaultProgrammeId: (u.programmes.find((p) => preferFields.includes(p.field)) ?? u.programmes[0])?.id ?? '',
    defaultProgramme: preferFields.length ? u.programmes.find((p) => preferFields.includes(p.field))?.name : undefined,
  };
}
