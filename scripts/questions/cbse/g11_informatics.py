#!/usr/bin/env python3
"""Generate the CBSE class 11 Informatics Practices (065) question bank (cbse-g11-informatics, 831 questions).

Fact tables: chapters 1-4 reuse the Computer Science class 11 text blocks (g11_computer_science_a.py / _b.py) composed
into the IP subtopics, with lines outside the IP syllabus left out; chapters 5-8 are in g11_informatics_a.py.
Computed families: g11_computer_science_kit.py (Python), g11_informatics_kit.py (statistics, NumPy, SQL) and the
validated class 12 families of g12_computer_science_a.py and g12_computer_science_d.py. Every code, NumPy and SQL
output is computed by running it, never typed by hand.

Paper (no CBSE SQP for class 11; class 12 template assumed, 70 marks, 37 questions): A 21 x 1 (19 MCQ + 2 A-R),
B 7 x 2, C 3 x 3, D 4 x 4, E 2 x 5.

Run: python3 scripts/questions/cbse/g11_informatics.py   (QB_LIMIT=n builds the first n chapters only)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

from qbank import Builder, F, ar  # noqa: E402
import g12_computer_science_kit as K12  # noqa: E402

SID = 'cbse-g11-informatics'
S = SID + '-ch'
MOCK_PATTERN = [(19, 1, 'mcq'), (2, 1, 'ar'), (7, 2, 'k2'), (3, 3, 'k3'), (4, 4, 'k4'), (2, 5, 'k5')]
CODE_SUBTOPICS = ([f'{S}{c:02d}-st{s}' for c in (3, 4, 6) for s in range(1, 5)] + [f'{S}05-st3', f'{S}08-st3', f'{S}08-st4'])
ACC = os.path.join(HERE, 'g11_informatics_accuracy.json')

# lines of the shared CS text that are outside the IP class 11 syllabus (dictionary pop(), string split())
DROP = {'dictmeth': ('pop(', 'split()')}


def text(key):
    import g11_computer_science_a as CA
    import g11_computer_science_b as CB
    import g11_informatics_a as IA
    ai, imm = IA.split_ai()
    pool = dict(CA.TXT)
    pool.update(CB.TXT)
    pool.update(IA.TXT)
    pool['ai_ip'], pool['imm_ip'] = ai, imm
    t = pool[key]
    if key in DROP:
        t = '\n'.join(ln for ln in t.strip().splitlines() if not any(b in ln for b in DROP[key]))
    return t


IP_MAP = {
    1: [('01-st1', 'components of a computer system, input and output devices', ['org']),
        ('01-st2', 'evolution of computers, memory and units of memory', ['evolution', 'memory']),
        ('01-st3', 'data and information: capturing, storage and retrieval', ['data']),
        ('01-st4', 'software, operating systems and language translators', ['software'])],
    2: [('02-st1', 'artificial intelligence, machine learning and natural language processing', ['ai_ip', 'ai_more']),
        ('02-st2', 'immersive experiences, robotics and big data', ['imm_ip', 'imm_more', 'robotics']),
        ('02-st3', 'Internet of Things, smart cities, cloud computing and grid computing', ['iot']),
        ('02-st4', 'blockchain technology', ['blockchain'])],
    3: [('03-st1', 'Python basics: modes, keywords, identifiers, variables and comments', ['pybasics']),
        ('03-st2', 'data types, operators and expressions', ['pytypes', 'pyops']),
        ('03-st3', 'input, output, type conversion and errors', ['pyio', 'pyerrors']),
        ('03-st4', 'flow of control: if-elif-else, for and while loops', ['pyif', 'pyloops'])],
    4: [('04-st1', 'lists: creation, indexing, slicing, operations and traversal', ['listops']),
        ('04-st2', 'list methods, built-in functions and list programs', ['listmeth', 'listprog']),
        ('04-st3', 'dictionaries: creating, accessing, adding, modifying and traversing', ['dicts']),
        ('04-st4', 'dictionary methods and programs', ['dictmeth'])],
    5: [('05-st1', 'data and its purpose; structured and unstructured data', ['dtypes']),
        ('05-st2', 'data collection, storage, processing and data quality', ['dcollect']),
        ('05-st3', 'statistical techniques: mean, median, mode, range, standard deviation and variance', ['dstats'])],
    6: [('06-st1', 'NumPy arrays and creating arrays', ['np1']),
        ('06-st2', 'indexing, slicing and operations on arrays', ['np2']),
        ('06-st3', 'concatenating, reshaping and splitting arrays', ['np3']),
        ('06-st4', 'statistical operations on arrays and loading arrays from files', ['np4'])],
    7: [('07-st1', 'file system and database management system', ['db1']),
        ('07-st2', 'relational data model', ['db2']),
        ('07-st3', 'keys in a relational database', ['db3'])],
    8: [('08-st1', 'SQL, MySQL data types and constraints', ['sql1']),
        ('08-st2', 'data definition commands', ['sql2']),
        ('08-st3', 'data manipulation commands', ['sql3']),
        ('08-st4', 'SELECT queries', ['sql4'])],
}


def subs(c):
    import g11_computer_science_a as CA
    return [K12.ST(S + suf, topic, CA._fix_a('\n'.join(text(k) for k in keys))) for suf, topic, keys in IP_MAP[c]]


def extra():
    import g11_computer_science_kit as K
    import g11_computer_science_b as CB
    import g12_computer_science_a as G
    import g12_computer_science_d as D
    import g11_informatics_kit as I
    only = I.only

    def arx(key, i=None):
        items = CB.AR_PY[key] if i is None else [CB.AR_PY[key][i]]
        return F('C3', 'D3', 'mcq', lambda r: ar(*r.choice(items)), kinds=('ar',))

    no_def = ('def ', 'T = (', 'tuple(')
    no_str = ('.upper', '.lower', '.isupper', '.islower', '.split', 'break', 'continue', 'def ')
    progs = [K.PROGS[i] for i in (0, 2, 3, 4, 5, 8, 9, 10, 11)]
    lprogs = [p for i, p in enumerate(K.LIST_PROGS) if i != 2]
    dprogs = [K.DICT_PROGS[i] for i in (0, 1, 3, 5)]
    st = lambda x: S + x
    E = {
        st('01-st2'): [F('C2', 'D2', 'mcq', K.unit_convert), F('C3', 'D3', 'explain', K.unit_written, marks=2)],
        st('03-st1'): [F('C4', 'D4', 'case', I.ip_py_case, marks=4, gap='G7'), F('C1', 'D1', 'mcq', K.keyword_pick), F('C2', 'D2', 'mcq', K.ident_valid),
                       F('C3', 'D3', 'explain', K.ident_classify, marks=2)],
        st('03-st2'): [F('C1', 'D2', 'mcq', K.type_out), F('C3', 'D3', 'mcq', K.mutability), F('C2', 'D2', 'mcq', G.expr_eval), F('C3', 'D3', 'mcq', K.ops_out),
                       F('C3', 'D4', 'mcq', G.expr_eval, gap='G5'), arx('types'), arx('ops'), F('C4', 'D4', 'case', I.ip_py_case, marks=4, gap='G7')],
        st('03-st3'): [F('C2', 'D2', 'mcq', K.conv_out), F('C2', 'D3', 'mcq', K.input_out), F('C3', 'D3', 'mcq', K.print_out), F('C2', 'D2', 'mcq', K.error_kind),
                       F('C4', 'D4', 'explain', only(K.error_find11, no_def), marks=2, gap='G5'), F('C3', 'D4', 'explain', only(G.error_find, no_def), marks=2, gap='G5'),
                       F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, K.PROGS[6:8]), marks=3)],
        st('03-st4'): [F('C2', 'D2', 'short', K.if_out, marks=1), F('C3', 'D3', 'short', K.if_out, marks=1), F('C2', 'D2', 'mcq', K.range_out),
                       F('C3', 'D3', 'short', only(G.loop_out, no_str), marks=2), arx('loops', 0),
                       F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, progs), marks=3), F('C4', 'D5', 'long', lambda r: K.prog_pair(r, progs), marks=5),
                       F('C4', 'D4', 'case', I.ip_loop_case, marks=4, gap='G7')],
        st('04-st1'): [F('C4', 'D4', 'case', K.list_case, marks=4, gap='G7'), F('C2', 'D2', 'mcq', K.list_index), F('C3', 'D3', 'mcq', K.list_index), arx('list'),
                       F('C3', 'D3', 'short', only(K.list_prog_out, ('break',)), marks=2)],
        st('04-st2'): [F('C4', 'D4', 'case', K.list_case, marks=4, gap='G7'), F('C2', 'D3', 'mcq', K.list_method), F('C3', 'D3', 'short', G.list_ops, marks=2),
                       F('C3', 'D4', 'mcq', K.list_method, gap='G5'), F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, lprogs), marks=3),
                       F('C4', 'D5', 'long', lambda r: K.prog_pair(r, lprogs), marks=5)],
        st('04-st3'): [F('C4', 'D4', 'case', I.ip_dict_case, marks=4, gap='G7'), F('C2', 'D2', 'mcq', only(G.dict_ops, ('.pop(',))), arx('dict'),
                       F('C3', 'D3', 'short', only(K.freq_out, ('.split',)), marks=2)],
        st('04-st4'): [F('C2', 'D3', 'mcq', only(K.dict_method, ('.pop(',))), F('C3', 'D4', 'mcq', only(K.dict_method, ('.pop(',)), gap='G5'),
                       F('C4', 'D4', 'case', I.ip_dict_case, marks=4, gap='G7'), F('C4', 'D3', 'multi_step', lambda r: K.prog_write(r, 3, dprogs), marks=3),
                       F('C4', 'D5', 'long', lambda r: K.prog_pair(r, dprogs), marks=5)],
        st('05-st3'): [F('C2', 'D2', 'mcq', I.stat_mcq), F('C2', 'D3', 'mcq', I.median_even), F('C3', 'D3', 'multi_step', I.stat_written, marks=3),
                       F('C3', 'D3', 'mcq', I.sd_mcq), F('C3', 'D4', 'multi_step', I.sd_written, marks=3, gap='G5'), F('C4', 'D4', 'case', I.stat_case, marks=4, gap='G7')],
        st('06-st1'): [F('C2', 'D2', 'mcq', I.np_attr), F('C2', 'D3', 'mcq', I.np_create), F('C3', 'D3', 'mcq', I.np_create), F('C4', 'D4', 'case', I.np_case_create, marks=4, gap='G7')],
        st('06-st2'): [F('C2', 'D2', 'mcq', I.np_index), F('C3', 'D3', 'short', I.np_index_short, marks=2), F('C2', 'D2', 'mcq', I.np_ops), F('C3', 'D3', 'mcq', I.np_ops),
                       F('C3', 'D4', 'mcq', I.np_2d_ops, gap='G5'), F('C4', 'D4', 'case', I.np_case_ops, marks=4, gap='G7')],
        st('06-st3'): [F('C3', 'D3', 'mcq', I.np_reshape), F('C3', 'D3', 'mcq', I.np_concat), F('C3', 'D4', 'short', I.np_concat_short, marks=3, gap='G5'),
                       F('C4', 'D4', 'case', I.np_case_reshape, marks=4, gap='G7')],
        st('06-st4'): [F('C2', 'D3', 'mcq', I.np_stats), F('C3', 'D3', 'short', I.np_stats_short, marks=3), F('C3', 'D4', 'short', I.np_std, marks=2, gap='G5'),
                       F('C3', 'D3', 'mcq', I.np_file), F('C3', 'D4', 'explain', I.np_genfromtxt, marks=2, gap='G5'), F('C4', 'D4', 'case', I.np_case_stats, marks=4, gap='G7')],
        st('07-st2'): [F('C3', 'D3', 'mcq', D.degree_card)],
        st('07-st3'): [F('C3', 'D3', 'mcq', D.keys_q), F('C3', 'D3', 'short', D.fk_q, marks=2), F('C4', 'D4', 'case', D.db_case, marks=4, gap='G7')],
        st('08-st1'): [F('C2', 'D2', 'mcq', D.constr_pick), F('C2', 'D2', 'mcq', D.dtype_pick), F('C4', 'D4', 'case', I.constr_case, marks=4, gap='G7')],
        st('08-st2'): [F('C2', 'D2', 'mcq', D.ddl_dml), F('C3', 'D3', 'multi_step', D.ddl_write, marks=3), F('C4', 'D4', 'case', I.ddl_case, marks=4, gap='G7')],
        st('08-st3'): [F('C3', 'D3', 'short', I.insert_write, marks=2), F('C3', 'D4', 'mcq', I.dml_effect, gap='G5'), F('C4', 'D4', 'case', I.dml_case, marks=4, gap='G7')],
        st('08-st4'): [F('C3', 'D3', 'short', lambda r: I.sql_out11(r, 1, 1), marks=1), F('C3', 'D3', 'short', lambda r: I.sql_out11(r, 2, 2), marks=2),
                       F('C3', 'D3', 'mcq', I.sql_out11_mcq), F('C2', 'D3', 'mcq', I.null_q), F('C2', 'D2', 'short', I.sql_write11_1, marks=1),
                       F('C4', 'D4', 'multi_step', lambda r: I.sql_write11(r, 4, 4), marks=4, gap='G5'),
                       F('C4', 'D5', 'long', lambda r: I.sql_write11(r, 5, 5), marks=5)],
    }
    return E


def families():
    chapters = [subs(c) for c in range(1, 9)]
    fams = K12.fact_families(chapters, extra(), drop_case=CODE_SUBTOPICS, code=CODE_SUBTOPICS)
    import g11_computer_science_kit as K
    return K12.assign_kinds(K.no_open_pick(fams))


def main():
    fams = families()
    b = Builder(SID, 'scripts/questions/cbse/g11_informatics.py', fams, MOCK_PATTERN, mock_minutes_per_mark=2.5)
    lim = int(os.environ.get('QB_LIMIT', '0'))
    if lim:
        b.cur['chapters'] = b.cur['chapters'][:lim]
        b.t = dict(b.t, chapters=lim)
    else:
        need = {s['id'] for ch in b.cur['chapters'] for s in ch['subtopics']}
        if set(fams) != need:
            raise SystemExit(f'subtopics missing: {sorted(need - set(fams))[:5]} extra: {sorted(set(fams) - need)[:5]}')
    files = b.build()
    acc = json.load(open(ACC)) if os.path.exists(ACC) else None
    b.write(files, accuracy=acc)
    print(f'{SID}: wrote {sum(len(v) for v in files.values())} questions')


if __name__ == '__main__':
    main()
