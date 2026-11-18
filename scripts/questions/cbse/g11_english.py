#!/usr/bin/env python3
"""Generate the CBSE class 11 English Core (301) question bank (cbse-g11-english, NCERT Hornbill + Snapshots, 948 questions).

Chapter data: g11_english_a.py (Hornbill 1-5, reading/note-making passages), g11_english_b.py (Hornbill 6-10),
g11_english_c.py (Snapshots 11-15). Engines: eng_kit_g8_g9_g12.py and eng_kit_g8_g9_g12_grammar.py (imported, not edited;
the writing forms the kit lacks – speech, debate, classified advertisement, poster – are added to its tables here).

Mock design (class XI blueprint, 80 marks, 16 questions):
Reading 26 = unseen passage 10 + case-based factual passage 8 + note-making 5 + summary 3;
Grammar 7 = 4 + 3; Writing 16 = classified advertisement/poster 4 + letter/job application 6 + speech/debate/report/article 6;
Literature 31 = poetry extract 4 + prose extract 4 + Hornbill short answers 3 x 2 + Snapshots short answers 2 x 2
+ one Hornbill 3-mark answer + Hornbill long answer 5 + Snapshots long answer 5.

Run: python3 scripts/questions/cbse/g11_english.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import F  # noqa: E402
import eng_kit_g8_g9_g12 as K  # noqa: E402
from eng_kit_g8_g9_g12 import (EngBuilder, build_subject, writing_item, passage_set, data_case, mock_extract, mock_short_set,  # noqa: E402
                               first_st)
from eng_kit_g8_g9_g12_grammar import mock_grammar  # noqa: E402
import g11_english_a as A  # noqa: E402
import g11_english_b as B  # noqa: E402
import g11_english_c as C  # noqa: E402

SID = 'cbse-g11-english'
GRADE = 11

PATTERN = [(1, 10, 'read10'), (1, 8, 'read8'), (1, 5, 'notes5'), (1, 3, 'summary3'), (1, 4, 'grammar4'), (1, 3, 'grammar3'),
           (1, 4, 'adv4'), (1, 6, 'letter6'), (1, 6, 'speech6'), (1, 4, 'poem4'), (1, 4, 'prose4'), (1, 6, 'shortH6'),
           (1, 4, 'shortS4'), (1, 3, 'shortH3'), (1, 5, 'longH'), (1, 5, 'longS')]

HORNBILL = range(1, 11)
POEMS = (2, 5, 6, 7, 10)
SNAPSHOTS = range(11, 16)

# ---------------------------------------------------------------- writing forms the shared kit does not cover

K.WORDS.setdefault('classified', ['50', 'not more than 50'])
K.WORDS.setdefault('poster', ['50', 'not more than 50'])
K.WORDS.setdefault('debate', ['120–150'])
K.FORM_LABEL.setdefault('classified', 'classified advertisement')
K.FORM_LABEL.setdefault('poster', 'poster')
K.FORM_LABEL.setdefault('debate', 'debate')
K.FORMAT_KEY.setdefault('classified', 'Format (1): the column heading (e.g. SITUATIONS VACANT, FOR SALE, TO LET), short phrases instead of full sentences, '
                                      'all essential details and a contact address or phone number. ')
K.FORMAT_KEY.setdefault('poster', 'Format (1): a catchy title or slogan, short lines of text arranged for display, a visual idea, and the name of the issuing body. ')
K.FORMAT_KEY.setdefault('debate', 'Format (1): address to the chairperson, judges and audience; a clear stand for or against the motion; arguments with examples; '
                                  'rebuttal of the other side; a strong conclusion and thanks. ')
K.FORM_FACTS.setdefault('speech', [
    ('A speech for the morning assembly usually begins with …', 'a greeting to the principal, teachers and fellow students', 'the date and a subject line', 'the word NOTICE', 'a list of abbreviations', 'A speech greets the audience first.'),
    ('In a speech, the speaker introduces …', 'himself or herself and the topic', 'the newspaper\'s address', 'a résumé', 'a column heading', 'Introduction of self and topic.'),
    ('A speech usually ends with …', 'a conclusion and a word of thanks', 'a list of references', 'a signature and designation only', 'a postscript', 'Speeches close with thanks.'),
    ('The language of a speech should be …', 'direct and engaging, addressing the audience', 'full of abbreviations', 'written in note form', 'entirely in the passive voice', 'It is spoken to listeners.'),
    ('Which device helps a speech hold the audience\'s attention?', 'Rhetorical questions and examples', 'Long lists of figures only', 'Footnotes', 'A table of contents', 'Engaging devices.'),
    ('The usual word limit for a speech in the class XI paper is …', '120–150 words', '20 words', '500 words', '50 words', 'Speech: 120–150 words.')])
K.FORM_FACTS.setdefault('classified', [
    ('A classified advertisement is written in …', 'short phrases, not full sentences', 'long paragraphs', 'the form of a diary', 'verse', 'Classifieds charge by the word.'),
    ('Why are classified advertisements kept brief?', 'They are charged by the number of words or lines', 'Newspapers dislike details', 'They are read aloud', 'They are written by children', 'Cost per word.'),
    ('Which column would carry an advertisement for a flat on rent?', 'To Let', 'Situations Vacant', 'Lost and Found', 'Matrimonial', 'Rental property goes under To Let.'),
    ('An advertisement for a job vacancy appears under …', 'Situations Vacant', 'To Let', 'For Sale', 'Travel', 'Jobs offered: Situations Vacant.'),
    ('Every classified advertisement must give …', 'a contact address or phone number', 'the writer\'s autobiography', 'a poem', 'a list of references', 'Readers must be able to respond.'),
    ('A poster differs from a classified advertisement because a poster …', 'uses a slogan and visual layout to catch the eye', 'is always printed in a newspaper column', 'has no title', 'is written in full paragraphs', 'Posters are visual.'),
    ('A poster should have …', 'a catchy slogan and the name of the issuing body', 'a salutation and complimentary close', 'a subject line', 'a byline only', 'Slogan and issuer.')])
K.FORM_AR.setdefault('speech', [('A speech addresses the audience directly.', 'A speech never addresses the audience.', 'It is meant to be heard by listeners, so the speaker speaks to them.',
                                 'It is meant to be printed in a newspaper.', 'Spoken to listeners.'),
                                ('A speech ends with a word of thanks.', 'A speech ends with a list of abbreviations.', 'It is polite to thank the audience for listening.', 'It must end with the date.', 'Courtesy.')])
K.FORM_AR.setdefault('classified', [('A classified advertisement uses short phrases.', 'A classified advertisement uses long paragraphs.', 'Newspapers charge advertisers by the number of words.',
                                     'Readers prefer long advertisements.', 'Cost per word.'),
                                    ('A poster carries a catchy slogan.', 'A poster never has a slogan.', 'It must catch the eye of passers-by at a glance.', 'It is read slowly at a desk.', 'Visual impact.')])
K.FORM_EXPLAIN.setdefault('speech', [('Why should a speech include examples and rhetorical questions?', 'They hold the audience\'s attention, make ideas concrete and invite listeners to think.'),
                                     ('How is a speech different from an article?', 'A speech is spoken to a present audience – greeting, direct address, thanks; an article is written for readers, with a title and byline.')])
K.FORM_EXPLAIN.setdefault('classified', [('Why must a classified advertisement be brief and precise?', 'Advertisers pay by the word, and readers scan many advertisements quickly, so only essential details are given.'),
                                         ('How is a poster different from a classified advertisement?', 'A poster uses a slogan, visuals and layout to persuade passers-by; a classified is a short text in a newspaper column.')])


# ---------------------------------------------------------------- every literature stem names its text

def _named(ch, s):
    """The text is named when its title (or short title) appears in quotation marks, so that common-word titles such as
    'Childhood' or 'Birth' are not mistaken for ordinary words."""
    low = s.lower()
    return any(t and (f"'{t.lower()}" in low or f'"{t.lower()}' in low) for t in (ch['title'], ch.get('short')))


COMMON = {'The', 'A', 'An', 'What', 'Who', 'Whom', 'Whose', 'How', 'Why', 'Which', 'When', 'Where', 'His', 'Her', 'Their', 'This', 'That',
          'These', 'Those', 'It', 'Its', 'There', 'Both', 'Each', 'Every', 'After', 'Before', 'At', 'On', 'In', 'By', 'For', 'From', 'With',
          'Some', 'All', 'No', 'One', 'Two', 'Three', 'Many', 'Most', 'Only', 'Even', 'Once', 'Though', 'Although', 'Despite', 'Do', 'Does',
          'Did', 'Is', 'Are', 'Was', 'Were', 'Has', 'Have', 'Had', 'Can', 'Could', 'Should', 'Would', 'Will', 'Describe', 'Explain', 'Trace',
          'Name', 'Write', 'Give', 'Discuss', 'Comment', 'Bring', 'Pick', 'Identify', 'Suggest', 'Narrate'}


def _lf(q):
    """Lower-case the first word only if it is a common word (never a name such as Gaitonde or Panipat)."""
    w = q.split(' ', 1)[0]
    return q[0].lower() + q[1:] if w in COMMON else q


def _nm(ch, q):
    return q if _named(ch, q) else f"In '{ch['title']}', {_lf(q)}"


def finish(chapters):
    """Make sure every literature fact, prompt and A-R statement names its text."""
    for ch in chapters.values():
        for st in ch['sts'].values():
            if st['kind'] != 'lit':
                continue
            assert _named(ch, st.get('ref', ch['title'])), (ch['title'], st.get('ref'))
            st['facts'] = [(_nm(ch, f[0]),) + tuple(f[1:]) for f in st.get('facts', [])]
            for key in ('explain', 'think', 'long'):
                st[key] = [(_nm(ch, q), a) for q, a in st.get(key, [])]
            st['ar'] = [(_nm(ch, t[0]), _nm(ch, t[1]) if t[1] else None) + tuple(t[2:]) for t in st.get('ar', [])]


def name_stems(chapters, fams):
    """Safety net for kit families on literature subtopics (e.g. chapter vocabulary): prefix the text's name."""
    for n, ch in chapters.items():
        for k, st in ch['sts'].items():
            if st['kind'] != 'lit':
                continue
            for f in fams.get(f'{SID}-ch{n:02d}-st{k}', []):
                f.gen = (lambda g, c: lambda r: _prefix(c, g(r)))(f.gen, ch)


def _prefix(ch, v):
    if not v['stem'].startswith('Assertion (A)') and not str(v.get('key', '')).startswith('Format') and not _named(ch, v['stem']):
        v = dict(v, stem=f"From '{ch['title']}': {v['stem']}")
    return v


# ---------------------------------------------------------------- note-making and summary (reading section)

def g_notes(texts):
    def g(r):
        t = r.choice(texts)
        stem = ('Read the passage given below and make notes on it in points only, using headings and sub-headings and at least four '
                'recognisable abbreviations. Supply a suitable title.\n\n' + t['text'])
        return {'stem': stem, 'answer': t['notes'],
                'key': f'Title 1; abbreviations with key 1; content in a proper note format (headings, sub-headings, indentation) 3. Model notes: {t["notes"]}',
                'marks': 5, 'minutes': 9, 'gap': 'G7'}
    return g


def g_summary(texts):
    def g(r):
        t = r.choice(texts)
        stem = ('Read the passage given below and write a summary of it in about 50 words. Give it a suitable title.\n\n' + t['text'])
        return {'stem': stem, 'answer': t['summary'],
                'key': f'Content 2 (all key points, in one\'s own words), expression 1 (coherent, within the word limit). Model summary: {t["summary"]}',
                'marks': 3, 'minutes': 6, 'gap': 'G7'}
    return g


def g_one(pairs, words, marks):
    def g(r):
        q, a = r.choice(pairs)
        return {'stem': f'Answer the following question in about {words} words.\n{q}', 'answer': a,
                'key': f'Value points: {a} ({marks} marks: content {marks - 1}, expression 1.)', 'marks': marks}
    return g


def g_long_mock(pairs, marks):
    def g(r):
        q, pts = r.choice(pairs)
        return {'stem': f'Answer the following question in about 120–150 words.\n{q}', 'answer': pts,
                'key': f'Value points: {pts} Content {marks - 2}, organisation and expression 2.', 'marks': marks, 'minutes': marks + 3, 'gap': 'G5'}
    return g


# ---------------------------------------------------------------- mock-only families

def mock_extra(chapters, fams):
    out = {}
    for n, ch in chapters.items():
        cid = f'{SID}-ch{n:02d}'
        lst = first_st(ch, cid)
        for k, st in ch['sts'].items():
            stid = f'{cid}-st{k}'
            if st['kind'] == 'gram':
                out.setdefault(stid, []).extend(mock_grammar(st, ch, GRADE, 4, 'grammar4'))
                out.setdefault(stid, []).extend(mock_grammar(st, ch, GRADE, 3, 'grammar3'))
            if st['kind'] == 'read':
                ps = A.PASSAGES.get(n, [])
                out.setdefault(stid, []).append(F('C3', 'D3', 'case', (lambda ps_: lambda r: passage_set(r, ps_, 10))(ps), kinds=('read10',), gap='G7'))
                out.setdefault(stid, []).append(F('C3', 'D3', 'case', lambda r: data_case(r, GRADE, 8), kinds=('read8',), gap='G7'))
                out.setdefault(stid, []).append(F('C4', 'D4', 'long', g_notes(A.NOTES), kinds=('notes5',)))
                out.setdefault(stid, []).append(F('C3', 'D3', 'explain', g_summary(A.NOTES), kinds=('summary3',)))
        # writing: group the chapter's prompts by mock slot
        prompts = [p for p in ch.get('writing', [])]
        for st in ch['sts'].values():
            prompts += st.get('prompts', [])
        wst = next((f'{cid}-st{k}' for k, st in ch['sts'].items() if st['kind'] == 'write'), lst)
        for kind, forms, marks in (('adv4', ('classified', 'poster'), 4), ('letter6', ('editor', 'job', 'letter'), 6),
                                   ('speech6', ('speech', 'debate', 'report', 'article'), 6)):
            ps = [p[:3] for p in prompts if p[0] in forms]
            if ps:
                out.setdefault(wst, []).append(F('C4', 'D4', 'long', (lambda ps_, m: lambda r: writing_item(r, GRADE, *r.choice(ps_), marks=m))(ps, marks),
                                                 kinds=(kind,), gap='G5'))
        # literature
        exs = ch.get('extracts', [])
        if exs and n in HORNBILL:
            est = f'{cid}-st{exs[0][0]}'
            out.setdefault(est, []).extend(mock_extract(ch, 4, 'poem4' if n in POEMS else 'prose4'))
        pairs = [p for st in ch['sts'].values() if st['kind'] == 'lit' for p in st.get('explain', []) + st.get('think', [])]
        longs = [p for st in ch['sts'].values() if st['kind'] == 'lit' for p in st.get('long', [])]
        if n in HORNBILL:
            out.setdefault(lst, []).extend(mock_short_set(ch, GRADE, 3, 'shortH6'))
            out.setdefault(lst, []).append(F('C3', 'D3', 'explain', g_one(pairs, '50–60', 3), kinds=('shortH3',)))
            out.setdefault(lst, []).append(F('C4', 'D4', 'long', g_long_mock(longs, 5), kinds=('longH',)))
        else:
            out.setdefault(lst, []).extend(mock_short_set(ch, GRADE, 2, 'shortS4'))
            out.setdefault(lst, []).append(F('C4', 'D4', 'long', g_long_mock(longs, 5), kinds=('longS',)))
    name_stems(chapters, out)
    return out


def main():
    chapters = {**A.CH, **B.CH, **C.CH}
    assert sorted(chapters) == list(range(1, 16)), sorted(chapters)
    finish(chapters)
    fams, mock_fams = build_subject(SID, 'scripts/questions/cbse/g11_english.py', GRADE, chapters, PATTERN, A.PASSAGES, mock_extra)
    name_stems(chapters, fams)
    b = EngBuilder(SID, 'scripts/questions/cbse/g11_english.py', fams, PATTERN, mock_families=mock_fams, mock_minutes_per_mark=2.25)
    files = b.build()
    p = os.path.join(HERE, 'g11_english_accuracy.json')
    acc = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else None
    b.write(files, acc)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
