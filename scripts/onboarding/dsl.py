"""Tiny authoring DSL for onboarding Part A content.

A subject group has 8 slots. Slots 1-4 probe the previous grade's prerequisites, 5-8 this
grade's first chapters. The adaptive ladder starts at D2, so:
  slot 1 holds only a D2 item, slot 2 holds D1 and D2, slots 3-8 hold D1, D2 and D3.
A student sees one item per slot (8 per group); the pool per group is 1 + 2 + 6*3 = 21.

Item tuple:  (stem, correct, [wrong1, wrong2, wrong3], why)          -> MCQ
             (stem, correct, None, why)                              -> numerical entry
Reference:   "subjectId:chapterNo:subtopicNo"  or {board: "subjectId:ch:st"} for shared slots.
"""

LEVELS_BY_SLOT = {1: ['D2'], 2: ['D1', 'D2']}
for _s in range(3, 9):
    LEVELS_BY_SLOT[_s] = ['D1', 'D2', 'D3']


def S(ref, hint, items, note=None, gaps=None):
    """One slot. `items` in D order. `gaps` optional list overriding likelyGapOnWrong per item."""
    return {'ref': ref, 'hint': hint, 'items': items, 'note': note, 'gaps': gaps}


def G(group, label, pre, cur):
    """A subject group: 4 prerequisite slots + 4 current-chapter slots."""
    assert len(pre) == 4 and len(cur) == 4, f'{group}: need 4 + 4 slots'
    return {'group': group, 'label': label, 'slots': list(pre) + list(cur)}


BOARDS = ['cbse', 'cambridge', 'ib']


def K(grade, subj, kw):
    """Keyword ref for every board: subj and kw are a string or {board: value}.
    Resolves to the first subtopic (chapter order) whose name contains one of the '|'-separated keywords."""
    subj = subj if isinstance(subj, dict) else {b: subj for b in BOARDS}
    kw = kw if isinstance(kw, dict) else {b: kw for b in BOARDS}
    return {b: f'{b}-g{grade}-{subj[b]}~{kw[b]}' for b in BOARDS if b in subj and b in kw}
