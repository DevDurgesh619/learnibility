#!/usr/bin/env python3
"""Generate the CBSE class 12 Sociology (039) question bank (cbse-g12-sociology, 885 questions).

Fact tables per subtopic live in g12_sociology_a.py (Indian Society, chapters 1-4, and Structural Change)
and g12_sociology_b.py (Cultural Change, rural and industrial society, social movements);
g12_hum_engine.py turns them into question families. No textbook passage is reproduced.

Paper pattern (SQP 2026-27, 80 marks, 35 questions): Section A 16 × 1 (14 MCQ + 2 Assertion-Reason),
Section B 9 × 2, Section C 7 × 4 (5 short answers + 2 passage/case-based), Section D 3 × 6 long answers.

Run: python3 scripts/questions/cbse/g12_sociology.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import qbank  # noqa: E402
import g12_hum_engine as E  # noqa: E402

SID = 'cbse-g12-sociology'
MOCK_PATTERN = [(14, 1, 'mcq'), (2, 1, 'ar'), (9, 2, 'short'), (5, 4, 'q4'), (2, 4, 'case'), (3, 6, 'long6')]
DEFAULTS = {'long_marks': 6, 'case_marks': (1, 1, 2)}
CUSTOM = {'q4', 'long6'}


def fits(f, kind):
    if kind in CUSTOM:
        return kind in f.kinds
    return E.strict_fits(f, kind)



def no_echo(fams):
    """Engine source items pick part (i) from a Q line and part (ii) from a T line independently; reject a
    variant whose part (ii) asks to explain the very term that is the answer to part (i), so _fresh retries."""
    for fs in fams.values():
        for f in fs:
            if f.type == 'case' and 'case' in f.kinds:
                def gen(r, g=f.gen):
                    v = g(r)
                    t = re.search(r"\(ii\) Explain the term '([^']+)'", v['stem'])
                    a = re.search(r"^\(i\) (.*?) \(ii\)", v['answer'])
                    if t and a and a.group(1).strip().rstrip('.').lower() == t.group(1).lower():
                        raise ValueError('source item asks the same term twice')
                    return v
                f.gen = gen
    return fams

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
    '01-st1': [('formal demography', 'social demography'), ('positive checks', 'preventive checks'), ('demography', 'social demography')],
    '01-st2': [('birth rate', 'death rate'), ('infant mortality rate', 'maternal mortality rate'), ('sex ratio', 'dependency ratio'),
               ('total fertility rate', 'birth rate'), ('life expectancy', 'infant mortality rate')],
    '01-st3': [('child sex ratio', 'sex ratio'), ('age structure', 'dependency ratio')],
    '01-st4': [('National Family Planning Programme', 'National Population Policy 2000'), ('urbanisation', 'literacy')],
    '02-st1': [('varna', 'jati'), ('endogamy', 'purity and pollution'), ('dominant caste', 'varna')],
    '02-st2': [('permanent traits', 'acquired traits'), ('tribe', 'jati')],
    '02-st3': [('nuclear family', 'extended family'), ('matrilineal family', 'matriarchy'), ('patrilocal family', 'matrilineal family')],
    '03-st1': [('prejudice', 'discrimination'), ('prejudice', 'stereotype'), ('social stratification', 'social exclusion'), ('stereotype', 'discrimination')],
    '03-st2': [('untouchability', 'affirmative action'), ('Dalit', 'Other Backward Classes')],
    '03-st3': [('Stri Purush Tulna', "Sultana's Dream"), ('Adivasi', 'Towards Equality')],
    '03-st4': [('disability', 'social model of disability'), ('differently abled', 'disability')],
    '04-st1': [('assimilationist policy', 'integrationist policy'), ('nation', 'state'), ('community identity', 'nation')],
    '04-st2': [('regionalism', 'communalism'), ('communalism', 'secularism'), ('linguistic reorganisation', 'regionalism')],
    '04-st3': [('authoritarian state', 'civil society'), ('minority', 'civil society')],
    '05-st1': [('colonialism', 'capitalism'), ('indentured labour', 'plantation')],
    '05-st2': [('port city', 'hill station'), ('hill station', 'cantonment'), ('deindustrialisation', 'port city')],
    '05-st3': [('metropolitan city', 'urban sprawl'), ('mixed economy', 'heavy industry')],
    '06-st1': [('Brahmo Samaj', 'Arya Samaj'), ('Arya Samaj', 'Satyashodhak Samaj'), ('social reform movement', 'modern framework')],
    '06-st2': [('Sanskritisation', 'Westernisation'), ('Sanskritisation', 'de-Sanskritisation'), ('positional change', 'Sanskritisation')],
    '06-st3': [('modernisation', 'secularisation'), ('universalism', 'modernisation'), ('secularisation', 'Westernisation')],
    '07-st1': [('tenant', 'landless agricultural labourer'), ('agrarian structure', 'begar')],
    '07-st2': [('Zamindari abolition', 'land ceiling'), ('land ceiling', 'benami transfer'), ('Operation Barga', 'Zamindari abolition')],
    '07-st3': [('circulation of labour', 'feminisation of agricultural labour'), ('footloose labour', 'circulation of labour')],
    '07-st4': [('contract farming', 'liberalisation of agriculture'), ('agrarian distress', 'contract farming')],
    '08-st1': [('organised sector', 'alienation'), ('assembly line', 'Taylorism')],
    '08-st2': [('disinvestment', 'outsourcing'), ('badli worker', 'jobber')],
    '08-st3': [('home-based work', 'working conditions'), ('piece rate', 'home-based work')],
    '08-st4': [('strike', 'lockout'), ('trade union', 'strike')],
    '09-st1': [('social movement', 'social change'), ('social movement', 'counter-movement')],
    '09-st2': [('reformist movement', 'revolutionary movement'), ('relative deprivation', 'logic of collective action'),
               ('logic of collective action', 'resource mobilisation theory'), ('new social movements', 'reformist movement')],
    '09-st3': [('peasant movement', "new farmers' movements"), ('Chipko movement', 'Tebhaga movement')],
    '09-st4': [('Dalit movement', "women's movement"), ('Satnami movement', 'Jharkhand movement')],
}


def distinguish(chapters):
    """Extra 2-mark family per subtopic: 'Distinguish between X and Y' over curated pairs of the chapter's key terms."""
    out = {}
    for subs, _ in chapters:
        terms = {t: m for sb in subs for t, m in sb.T}
        for sb in subs:
            pairs = PAIRS.get(sb.sid.split('-ch')[-1], [])
            if not pairs:
                continue
            for a, b in pairs:
                assert a in terms and b in terms, (sb.sid, a, b)
            d = E.deck([((a, terms[a]), (b, terms[b])) for a, b in pairs])

            def gen(r, d=d):
                (a, ma), (b, mb) = d(r)
                ans = f"{E.cap(a)}: {E.end(ma)} {E.cap(b)}: {E.end(mb)}"
                return {'stem': f"Distinguish between '{a}' and '{b}'.", 'answer': ans,
                        'key': f"2 marks: 1 mark for explaining '{a}' ({E.end(ma)}) and 1 mark for '{b}' ({E.end(mb)}), "
                               f"with the contrast between them made clear.", 'marks': 2, 'minutes': 3}
            out[sb.sid] = [qbank.F('C2', 'D2', 'explain', gen, marks=2, minutes=3)]
    return out


def chapters():
    out = []
    for mod in ('g12_sociology_a', 'g12_sociology_b'):
        m = __import__(mod)
        out += [(c, dict(DEFAULTS, **cfg)) for c, cfg in m.CHAPTERS]
    return out


ACCURACY = [{
    'date': '2026-11-18',
    'method': '5 random generated items per chapter (45 items) plus all written items of mock 1 (19 items) re-solved by hand against '
              'NCERT Indian Society and Social Change and Development in India; every fact line re-checked against the chapters',
    'checked': 64,
    'mismatches': 0,
    'fixes': [
        "source-based items: a variant whose part (ii) asks to explain the same term that answers part (i) is now rejected and regenerated (no_echo guard)",
        "'largest tribe' item replaced (Census 2011 counts more Bhils than Gonds); it now asks for one of the large tribes numbering over a million",
        "'Distinguish between' 2-mark items use curated contrastive term pairs only (the first draft paired unrelated terms such as civil society / RTI Act)",
        'the 2-mark mock section ran out of items in mock 5; the curated distinguish family fixes this',
        'Birsa Munda item distractor corrected to Sidhu Murmu',
    ],
}]


def main():
    qbank._fits = fits
    chs = chapters()
    fams = no_echo(tag(E.families([c for c, _ in chs], [cfg for _, cfg in chs], distinguish(chs))))
    b = qbank.Builder(SID, 'scripts/questions/cbse/g12_sociology.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.25)
    need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
    if set(fams) != need:
        raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = b.build()
    b.write(files, accuracy=ACCURACY or None)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')
    return b, files


if __name__ == '__main__':
    main()
