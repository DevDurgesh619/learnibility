#!/usr/bin/env python3
"""Generate the CBSE class 11 Political Science question bank (cbse-g11-political-science, 1,440 questions).

Fact tables per subtopic live in g11_political_science_a.py and g11_political_science_b.py (Indian Constitution
at Work, chapters 1-10) and g11_political_science_c.py (Political Theory, chapters 11-18); g12_hum_engine.py
turns them into question families, and g11_hum_kit.py adds 'Distinguish between' and two-part items.

Paper pattern (school annual exam on the XI-XII design, 80 marks, 30 questions): Section A 12 × 1
(10 MCQ + 2 Assertion-Reason), Section B 6 × 2, Section C 5 × 4, Section D 3 passage/cartoon-based × 4,
Section E 4 × 6 long answers. Custom kinds 'q4' and 'long6' keep the 4- and 6-mark slots for items written
for those marks.

Run: python3 scripts/questions/cbse/g11_political_science.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import qbank  # noqa: E402
import g12_hum_engine as E  # noqa: E402
import g11_hum_kit as K  # noqa: E402

SID = 'cbse-g11-political-science'
MOCK_PATTERN = [(10, 1, 'mcq'), (2, 1, 'ar'), (6, 2, 'short'), (5, 4, 'q4'), (3, 4, 'case'), (4, 6, 'long6')]
DEFAULTS = {'long_marks': 6, 'case_marks': (1, 1, 2)}
CUSTOM = {'q4', 'long6'}

PAIRS = {
    '01-st1': [('coordination and assurance', 'limitation of power'), ('constitution', 'aspirations of society')],
    '01-st2': [('mode of promulgation', 'substantive provisions'), ('balanced institutional design', 'checks and balances')],
    '01-st3': [('Constituent Assembly', 'Drafting Committee'), ('Objectives Resolution', 'Cabinet Mission')],
    '01-st4': [('first past the post', 'judicial review'), ('Directive Principles of State Policy', 'residual powers')],
    '02-st1': [('Bill of Rights', 'Fundamental Rights'), ('rights', 'justiciable')],
    '02-st2': [('right to equality', 'right to freedom'), ('right against exploitation', 'cultural and educational rights'),
               ('preventive detention', 'right to freedom')],
    '02-st3': [('habeas corpus', 'mandamus'), ('mandamus', 'quo warranto'), ('writ', 'National Human Rights Commission')],
    '02-st4': [('non-justiciable', 'Fundamental Duties'), ('welfare state', 'Fundamental Duties')],
    '03-st1': [('direct democracy', 'representative democracy'), ('proportional representation', 'single transferable vote')],
    '03-st2': [('reserved constituency', 'Delimitation Commission')],
    '03-st3': [('universal adult franchise', 'Election Commission'), ('Model Code of Conduct', 'electoral roll')],
    '03-st4': [('electoral reforms', 'state funding of elections')],
    '04-st1': [('political executive', 'permanent executive'), ('parliamentary system', 'presidential system'),
               ('presidential system', 'semi-presidential system')],
    '04-st2': [('impeachment', 'pocket veto'), ('electoral college', 'discretionary powers')],
    '04-st3': [('Council of Ministers', 'Cabinet'), ('collective responsibility', 'coalition government')],
    '04-st4': [('bureaucracy', 'All India Services'), ('Union Public Service Commission', 'political neutrality')],
    '05-st1': [('bicameral legislature', 'unicameral legislature')],
    '05-st2': [('Lok Sabha', 'Rajya Sabha'), ('money bill', 'joint sitting')],
    '05-st3': [('question hour', 'zero hour'), ('no-confidence motion', 'adjournment motion')],
    '05-st4': [('standing committee', 'Joint Parliamentary Committee'), ('anti-defection law', 'defection')],
    '06-st1': [('independence of the judiciary', 'collegium'), ('removal of judges', 'contempt of court')],
    '06-st2': [('original jurisdiction', 'appellate jurisdiction'), ('advisory jurisdiction', 'writ jurisdiction')],
    '06-st3': [('judicial activism', 'public interest litigation')],
    '06-st4': [('judicial review', 'basic structure')],
    '07-st1': [('federalism', 'union of states')],
    '07-st2': [('Union List', 'State List'), ('Concurrent List', 'residuary powers')],
    '07-st3': [('Governor', "President's Rule"), ('Sarkaria Commission', 'demand for autonomy')],
    '07-st4': [('Article 371', 'Sixth Schedule')],
    '08-st1': [('local government', 'gram sabha'), ('Community Development Programme', 'Balwant Rai Mehta Committee')],
    '08-st2': [('Eleventh Schedule', 'Twelfth Schedule'), ('Zilla Parishad', 'municipal corporation')],
    '08-st3': [('State Election Commission', 'State Finance Commission')],
    '09-st1': [('special majority', 'ratification by states')],
    '09-st2': [('42nd Amendment', '44th Amendment')],
    '09-st3': [('basic structure doctrine', 'judicial interpretation')],
    '10-st1': [('philosophy of the Constitution', 'democratic transformation')],
    '10-st2': [('social justice', 'minority rights'), ('principled distance', 'asymmetric federalism')],
    '10-st3': [('deliberation', 'consensus')],
    '11-st1': [('politics', 'political theory')],
    '11-st2': [('conceptual clarity', 'censorship')],
    '11-st3': [('informed citizen', 'tolerance')],
    '12-st1': [('negative liberty', 'positive liberty'), ('freedom', 'swaraj')],
    '12-st2': [('self-regarding actions', 'other-regarding actions'), ('harm principle', 'reasonable restrictions')],
    '12-st3': [('freedom of expression', 'ban')],
    '13-st1': [('natural inequalities', 'social inequalities'), ('equality', 'equality of opportunity')],
    '13-st2': [('political equality', 'economic equality'), ('social equality', 'political equality')],
    '13-st3': [('feminism', 'patriarchy'), ('socialism', 'liberalism'), ('Marxism', 'liberalism')],
    '13-st4': [('formal equality', 'differential treatment'), ('affirmative action', 'formal equality')],
    '14-st1': [('proportionate justice', 'equal treatment for equals'), ('recognition of special needs', 'proportionate justice')],
    '14-st2': [('veil of ignorance', 'original position')],
    '14-st3': [('free market', 'state intervention')],
    '15-st1': [('natural rights', 'legal rights')],
    '15-st2': [('political rights', 'economic rights'), ('cultural rights', 'civil liberties')],
    '15-st3': [('human rights', 'Universal Declaration of Human Rights')],
    '16-st1': [('citizenship', 'Citizenship Act')],
    '16-st2': [('civil rights movement', 'segregation')],
    '16-st3': [('refugee', 'stateless person'), ('universal citizenship', 'global citizenship')],
    '17-st1': [('nation', 'nationalism')],
    '17-st2': [('national self-determination', 'pluralism')],
    '17-st3': [('Indian nationalism', 'inclusive nationalism')],
    '18-st1': [('inter-religious domination', 'intra-religious domination')],
    '18-st2': [('mutual exclusion', 'principled distance')],
    '18-st3': [('minoritism', 'vote-bank politics')],
}


def fits(f, kind):
    if kind in CUSTOM:
        return kind in f.kinds
    return E.strict_fits(f, kind)


def tag(fams):
    for fs in fams.values():
        for f in fs:
            if f.type == 'long' and f.marks == 6:
                f.kinds = tuple(f.kinds) + ('long6',)
            elif f.type == 'explain' and 'case' not in f.kinds and f.marks == 4:
                f.kinds = tuple(f.kinds) + ('q4',)
    return fams


def extras(chapters):
    out = {}
    for subs, _ in chapters:
        out = K.merge(out, K.pairs(subs, PAIRS, marks=2))
        for sb in subs:
            out = K.merge(out, {sb.sid: K.combo(sb, marks=4, C='C3', D='D3')})
    return out


def chapters():
    out = []
    for mod in ('g11_political_science_a', 'g11_political_science_b', 'g11_political_science_c'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': 'about 5 random generated items per chapter (95 items) plus one full mock (30 items) re-solved by hand against '
              'NCERT Indian Constitution at Work and Political Theory (class XI); articles, amendments and years checked',
    'checked': 125,
    'mismatches': 0,
    'fixes': [
        'implausible MCQ distractors in the Political Theory chapters (11-18) replaced with concepts from the same chapter',
    ],
}]


def main():
    qbank._fits = fits
    chs = chapters()
    fams = tag(E.families([c for c, _ in chs], [cfg for _, cfg in chs], extras(chs)))
    b = qbank.Builder(SID, 'scripts/questions/cbse/g11_political_science.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.25)
    need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
    if set(fams) != need:
        raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = b.build()
    b.write(files, accuracy=ACCURACY or None)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files


if __name__ == '__main__':
    main()
