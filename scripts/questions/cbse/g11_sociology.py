#!/usr/bin/env python3
"""Generate the CBSE class 11 Sociology (039) question bank (cbse-g11-sociology, 630 questions).

Fact tables per subtopic live in g11_sociology_a.py (Introducing Sociology, chapters 1-4) and
g11_sociology_b.py (Understanding Society, chapters 5-7); g12_hum_engine.py turns them into question
families. No textbook passage is reproduced.

Paper pattern (school annual exam on the XII design, 80 marks, 35 questions): Section A 16 × 1
(14 MCQ + 2 Assertion-Reason), Section B 9 × 2, Section C 7 × 4 (5 short answers + 2 passage-based),
Section D 3 × 6 long answers. The 4- and 6-mark slots use custom kinds ('q4', 'long6') so that only
items written for those marks fill them.

Run: python3 scripts/questions/cbse/g11_sociology.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import qbank  # noqa: E402
import g12_hum_engine as E  # noqa: E402
import g11_hum_kit as K  # noqa: E402

SID = 'cbse-g11-sociology'
MOCK_PATTERN = [(14, 1, 'mcq'), (2, 1, 'ar'), (9, 2, 'short'), (5, 4, 'q4'), (2, 4, 'case'), (3, 6, 'long6')]
DEFAULTS = {'long_marks': 6, 'case_marks': (1, 1, 2)}
CUSTOM = {'q4', 'long6'}


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


# Curated term pairs for 'Distinguish between' items (terms from the chapter's T lines).
PAIRS = {
    '01-st1': [('personal troubles', 'public issues'), ('sociological imagination', 'common sense')],
    '01-st2': [('Enlightenment', 'Industrial Revolution'), ('positivism', 'capitalism')],
    '01-st3': [('colonial ethnography', 'social anthropology')],
    '01-st4': [('micro sociology', 'macro sociology')],
    '02-st1': [('primary group', 'secondary group'), ('in-group', 'out-group'), ('social group', 'quasi-group'),
               ('reference group', 'peer group')],
    '02-st2': [('ascribed status', 'achieved status'), ('status', 'role'), ('role conflict', 'role stereotyping')],
    '02-st3': [('caste', 'class'), ('estate', 'slavery'), ('class', 'social mobility')],
    '02-st4': [('formal social control', 'informal social control'), ('sanction', 'deviance')],
    '03-st1': [('nuclear family', 'extended family'), ('endogamy', 'exogamy'), ('affinal kin', 'consanguineous kin'),
               ('matrilineal family', 'patrilineal family')],
    '03-st2': [('Fordism', 'scientific management'), ('informal sector', 'outsourcing')],
    '03-st3': [('power', 'authority'), ('state', 'stateless society'), ('citizenship', 'pressure group')],
    '03-st4': [('sacred', 'profane')],
    '04-st1': [('norms', 'mores'), ('normative dimension of culture', 'material dimension of culture'),
               ('cognitive dimension of culture', 'normative dimension of culture')],
    '04-st2': [('ethnocentrism', 'cosmopolitanism'), ('cultural lag', 'cultural change'), ('subculture', 'cosmopolitanism')],
    '04-st3': [('primary socialisation', 'secondary socialisation')],
    '04-st4': [('agency', 'social structure')],
    '05-st1': [('evolutionary change', 'revolutionary change')],
    '05-st2': [('law', 'crime'), ('domination', 'contestation')],
    '05-st3': [('village', 'urban area'), ('dominant caste', 'land reform')],
    '05-st4': [('gentrification', 'ghettoisation'), ('urbanisation', 'gated community')],
    '06-st1': [('Enlightenment', 'French Revolution')],
    '06-st2': [('forces of production', 'relations of production'), ('bourgeoisie', 'proletariat'),
               ('mode of production', 'class struggle')],
    '06-st3': [('mechanical solidarity', 'organic solidarity'), ('repressive law', 'restitutive law')],
    '06-st4': [('rational-legal authority', 'charismatic authority'), ('ideal type', 'bureaucracy')],
    '07-st1': [('segmental division', 'hierarchical division')],
    '07-st2': [('shruti', 'smriti'), ('smriti', 'anubhava')],
    '07-st3': [('welfare state', 'mixed economy')],
    '07-st4': [('field view', 'book view'), ('village studies', 'Sanskritisation')],
}


def extras(chapters):
    """'Distinguish between' (2 marks) over PAIRS, and a two-part 4-mark item (reason + correction) per subtopic."""
    out = {}
    for subs, _ in chapters:
        out = K.merge(out, K.pairs(subs, PAIRS, marks=2))
        for sb in subs:
            out = K.merge(out, {sb.sid: K.combo(sb, marks=4, C='C3', D='D3')})
    return out


def chapters():
    out = []
    for mod in ('g11_sociology_a', 'g11_sociology_b'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5-6 random generated items per chapter (40 items) plus one full mock (35 items) re-solved by hand against '
              'NCERT Introducing Sociology and Understanding Society (class XI)',
    'checked': 75,
    'mismatches': 0,
    'fixes': [
        "D.P. Mukerji described as calling himself a 'marxologist', as NCERT does",
        'MCQ distractors that were not sociological concepts replaced with same-category alternatives',
        "public-issue assertion reworded to 'mass unemployment' so it matches C. Wright Mills' distinction",
    ],
}]


def main():
    qbank._fits = fits
    chs = chapters()
    fams = tag(E.families([c for c, _ in chs], [cfg for _, cfg in chs], extras(chs)))
    b = qbank.Builder(SID, 'scripts/questions/cbse/g11_sociology.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.25)
    need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
    if set(fams) != need:
        raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = b.build()
    b.write(files, accuracy=ACCURACY or None)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files


if __name__ == '__main__':
    main()
