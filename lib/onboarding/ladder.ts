/**
 * Onboarding Part A adaptive ladder (blueprint, "Onboarding test and starting profile").
 *
 * Each subject group has 8 slots (1-4 prerequisites, 5-8 this grade's first chapters) and each slot
 * has one item per difficulty it can be reached at. The first item is D2; after a miss the next
 * item is one level easier (not below D1); after two hits in a row it is one level harder
 * (not above D3). A student sees exactly one item per slot: 8 per group.
 *
 * Pure functions: no I/O, no clock.
 */
import type { Difficulty } from '../types/enums';
import type { LadderRule, OnboardingAcademicItem } from '../types/onboarding';

export const DEFAULT_LADDER: LadderRule = {
  start: 'D2',
  floor: 'D1',
  ceiling: 'D3',
  hitsToStepUp: 2,
  weights: { D1: 1, D2: 2, D3: 3 },
};

const ORDER: Difficulty[] = ['D1', 'D2', 'D3', 'D4', 'D5'];
const idx = (d: Difficulty) => ORDER.indexOf(d);

export interface LadderStep {
  difficulty: Difficulty;
  correct: boolean;
}

/** Difficulty of the next item, given the answers so far in this group. */
export function nextDifficulty(history: LadderStep[], rule: LadderRule = DEFAULT_LADDER): Difficulty {
  let level = idx(rule.start);
  let streak = 0;
  for (const step of history) {
    if (!step.correct) {
      level = Math.max(idx(rule.floor), level - 1);
      streak = 0;
    } else {
      streak += 1;
      if (streak >= rule.hitsToStepUp) {
        level = Math.min(idx(rule.ceiling), level + 1);
        streak = 0;
      }
    }
  }
  return ORDER[level];
}

/**
 * The next item to show in one group, or null when all 8 slots are answered.
 * `answered` maps questionId -> correct for items already answered in this group.
 * If a slot has no item at the wanted level (slot 1 only has D2, slot 2 has D1/D2), the nearest
 * easier level is used, then the nearest harder one.
 */
export function nextItem(
  groupItems: OnboardingAcademicItem[],
  answered: Record<string, boolean>,
  rule: LadderRule = DEFAULT_LADDER,
): OnboardingAcademicItem | null {
  const bySlot = new Map<number, OnboardingAcademicItem[]>();
  for (const it of groupItems) {
    const list = bySlot.get(it.slot) ?? [];
    list.push(it);
    bySlot.set(it.slot, list);
  }
  const slots = [...bySlot.keys()].sort((a, b) => a - b);
  const history: LadderStep[] = [];
  for (const s of slots) {
    const seen = bySlot.get(s)!.find((it) => it.id in answered);
    if (seen) {
      history.push({ difficulty: seen.difficulty, correct: answered[seen.id] });
      continue;
    }
    const want = nextDifficulty(history, rule);
    return pickAtLevel(bySlot.get(s)!, want);
  }
  return null;
}

export function pickAtLevel(items: OnboardingAcademicItem[], want: Difficulty): OnboardingAcademicItem {
  const exact = items.find((it) => it.difficulty === want);
  if (exact) return exact;
  const easier = items.filter((it) => idx(it.difficulty) < idx(want)).sort((a, b) => idx(b.difficulty) - idx(a.difficulty));
  if (easier.length) return easier[0];
  return [...items].sort((a, b) => idx(a.difficulty) - idx(b.difficulty))[0];
}

/** Simulate a whole group for a student who answers by a rule (used by the persona simulator and tests). */
export function runGroup(
  groupItems: OnboardingAcademicItem[],
  answer: (item: OnboardingAcademicItem) => boolean,
  rule: LadderRule = DEFAULT_LADDER,
): { item: OnboardingAcademicItem; correct: boolean }[] {
  const answered: Record<string, boolean> = {};
  const out: { item: OnboardingAcademicItem; correct: boolean }[] = [];
  for (let next = nextItem(groupItems, answered, rule); next; next = nextItem(groupItems, answered, rule)) {
    const correct = answer(next);
    answered[next.id] = correct;
    out.push({ item: next, correct });
  }
  return out;
}
