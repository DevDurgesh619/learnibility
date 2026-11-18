"""Grade 8 Hindi (school Hindi reader leading into IGCSE Hindi as a Second Language 0549).

Ten lessons (prose and poetry) with व्याकरण, शब्द-भंडार and रचना. Every poem, दोहा, extract, sentence and
passage in this file is original, written for this bank. All stems, options, answers and keys are in Hindi.

The first part of the file is the shared Hindi machinery, reused by g9_hindi.py and g10_hindi.py:
names and places in Devanagari, gender agreement, a Hindi compose() with (क) (ख) part letters,
grammar banks (संज्ञा … समास, मुहावरे, पर्यायवाची, विलोम …) and template factories:
  tagbank()   classify a quoted word / sentence (संज्ञा-भेद, काल, वाक्य-भेद, अलंकार …)
  xform()     transform (संधि, वाच्य, काल-परिवर्तन, वर्तनी-शुद्धि …)
  meanings()  term -> meaning (मुहावरे, पर्यायवाची, शब्दार्थ …)
  reading()   passage / transcript frames -> retrieval, inference, notes, summary items
  writing()   writing tasks (पत्र, ई-मेल, लेख, रिपोर्ट …) level-marked in Hindi
  literary()  poem / extract banks -> भाव, शब्दार्थ, व्याख्या, मूल्यांकन
"""
import re

from ._lib import topic, mcq, CTX  # noqa: F401
from core import MARKS

PROFILE = {'mark_scale': {'long': (2.5, 2.5)}, 'wordy': True}
CHAPTERS = {}

# =========================================================== shared helpers

HL = 'कखगघङचछजझ'
_MK = re.compile(r'\[(\d+)\]')

NAMES = [('आरव', 'm'), ('रोहन', 'm'), ('कबीर', 'm'), ('अर्जुन', 'm'), ('समीर', 'm'), ('इमरान', 'm'), ('करण', 'm'), ('देव', 'm'),
         ('यश', 'm'), ('अमन', 'm'), ('निखिल', 'm'), ('विवेक', 'm'), ('फ़ैज़ान', 'm'), ('तनुज', 'm'), ('सिद्धार्थ', 'm'), ('राहुल', 'm'),
         ('अनन्या', 'f'), ('प्रिया', 'f'), ('मीरा', 'f'), ('सना', 'f'), ('काव्या', 'f'), ('ज़ोया', 'f'), ('नेहा', 'f'), ('रिया', 'f'),
         ('दीया', 'f'), ('आयशा', 'f'), ('तारा', 'f'), ('इशिता', 'f'), ('गौरी', 'f'), ('निधि', 'f'), ('पूजा', 'f'), ('सिमरन', 'f')]
SURN = ['शर्मा', 'वर्मा', 'खान', 'सिंह', 'पटेल', 'मेहता', 'जोशी', 'गुप्ता', 'नायर', 'अली', 'रेड्डी', 'चौधरी', 'मिश्रा', 'कपूर', 'बोस', 'दास']
CITIES = [('नैरोबी', 'केन्या'), ('लंदन', 'ब्रिटेन'), ('टोरंटो', 'कनाडा'), ('दुबई', 'संयुक्त अरब अमीरात'), ('सिंगापुर', 'सिंगापुर'),
          ('सिडनी', 'ऑस्ट्रेलिया'), ('डरबन', 'दक्षिण अफ़्रीका'), ('पोर्ट लुई', 'मॉरीशस'), ('सूवा', 'फ़िजी'), ('न्यूयॉर्क', 'अमेरिका'),
          ('मस्कट', 'ओमान'), ('कुआलालंपुर', 'मलेशिया'), ('काठमांडू', 'नेपाल'), ('दोहा', 'क़तर'), ('ऑकलैंड', 'न्यूज़ीलैंड'),
          ('जयपुर', 'भारत'), ('पुणे', 'भारत'), ('लखनऊ', 'भारत'), ('भोपाल', 'भारत'), ('कोच्चि', 'भारत'), ('इंदौर', 'भारत'), ('पटना', 'भारत')]
INDIA = [c for c, k in CITIES if k == 'भारत']
WEEKDAYS = ['सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार']
MONTHS = ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']
NUMW = {1: 'एक', 2: 'दो', 3: 'तीन', 4: 'चार', 5: 'पाँच', 6: 'छह', 7: 'सात', 8: 'आठ', 9: 'नौ', 10: 'दस'}


def name(r, g=None):
    pool = [x for x in NAMES if g is None or x[1] == g]
    return r.choice(pool)


def names(r, k=2, gs=None):
    out = []
    while len(out) < k:
        x = name(r, gs[len(out)] if gs else None)
        if x[0] not in [y[0] for y in out]:
            out.append(x)
    return out


def city(r, abroad=None):
    pool = [x for x in CITIES if abroad is None or (x[1] != 'भारत') == abroad]
    return r.choice(pool)


def others(r, pool, correct, k=3):
    """k distinct items from pool that differ from correct."""
    ds = []
    for x in r.sample(list(pool), len(pool)):
        if x != correct and x not in ds:
            ds.append(x)
        if len(ds) == k:
            break
    return ds


def A(s, g):
    """Gender agreement markers: {ा} -> ा / ी, {या} -> या / ई, {े} -> े / ी, {ाा} for पढ़ा-लिखा style is not used."""
    if g == 'f':
        return s.replace('{ा}', 'ी').replace('{या}', 'ई').replace('{े}', 'ी')
    return s.replace('{ा}', 'ा').replace('{या}', 'या').replace('{े}', 'े')


def clean(s):
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s)
    return s.strip()


def Q(s):
    return f'“{s}”'


def mk(C, D, long=False):
    """Marks for a (C, D) cell, following the requested total when a form or mock asks for one."""
    base = MARKS.get((C, D), (2, 2))[0]
    want = CTX.get('want_marks')
    if long:
        sc = max(1, round(base * 2.5))
        return want if (want and want >= 6) else sc
    return want or base


def tail(key, m):
    return key if _MK.search(key) else f'{key} [{m}]'


def item(stem, answer, key, m, typ=None, options=None, minutes=None):
    q = {'stem': clean(stem), 'answer': answer, 'key': tail(key, m), 'marks': m}
    if typ:
        q['type'] = typ
    if options:
        q['options'] = options
    if minutes:
        q['minutes'] = minutes
    return q


def mq(r, stem, correct, distractors, key):
    opts, ans = mcq(r, correct, list(distractors))
    return {'stem': clean(stem), 'options': opts, 'answer': ans, 'key': tail(f'सही उत्तर: {ans.rstrip("।")}। {key}', 1), 'marks': 1}


def _pm(key):
    m = _MK.findall(key)
    return int(m[-1]) if m else 1


def hcompose(r, intro, parts, k=(2, 3), keep_order=True, type_=None, want=None):
    """Multi-part structured item with Hindi part letters. parts: (text, answer, key) tuples (or callables)."""
    built = []
    for i, p in enumerate(parts):
        x = p(r) if callable(p) else p
        if x:
            built.append((i, x, _pm(x[2])))
    if not built:
        return None
    want = want or CTX.get('want_marks')
    sizes = [n for n in k if n <= len(built)] or [len(built)]
    if want:
        sizes = sorted(set(sizes) | ({1, 2, 3, 4} if want <= 3 else {2, 3, 4, 5}))
    best = None
    for _ in range(60):
        n = min(r.choice(sizes), len(built))
        pk = r.sample(built, n)
        tot = sum(m for _, _, m in pk)
        score = abs(tot - want) if want else 0
        if want and n == 1 and want > 2:
            score += 2
        if best is None or score < best[0]:
            best = (score, pk, tot)
        if score == 0:
            break
    _, pk, tot = best
    if keep_order:
        pk.sort(key=lambda x: x[0])
    if want and want >= 6 and tot < want:
        # long-section use: stretch part marks to the wanted total (more depth expected per part)
        ms = [m for _, _, m in pk]
        exact = [m * want / tot for m in ms]
        new = [int(e) for e in exact]
        for j in sorted(range(len(ms)), key=lambda j: -(exact[j] - new[j]))[:want - sum(new)]:
            new[j] += 1
        pk = [(i, (x[0], x[1], re.sub(r'\s*\[\d+\]\s*$', ('' if nm == m else ' (विस्तृत उत्तर अपेक्षित)') + f' [{nm}]', x[2])), nm)
              for (i, x, m), nm in zip(pk, new)]
        tot = want
    got = [x for _, x, _ in pk]
    if len(got) == 1:
        t, a, kk = got[0]
        intro = re.sub(r'(सभी भागों के उत्तर|प्रश्नों के उत्तर|सभी भाग हल कीजिए|प्रत्येक भाग का उत्तर)', 'प्रश्न का उत्तर', intro).replace('प्रश्न का उत्तर दीजिए।', 'प्रश्न का उत्तर दीजिए।')
        q = {'stem': clean(intro + '\n' + t), 'answer': a, 'key': kk}
    else:
        q = {'stem': clean(intro + '\n' + '\n'.join(f'({HL[j]}) {t}' for j, (t, _, _) in enumerate(got))),
             'answer': ' '.join(f'({HL[j]}) {a}' for j, (_, a, _) in enumerate(got)),
             'key': ' '.join(f'({HL[j]}) {kk}' for j, (_, _, kk) in enumerate(got))}
    q['marks'] = max(1, min(20, tot))
    q['minutes'] = round(max(1.0, q['marks'] * 1.25) * 2) / 2
    if type_:
        q['type'] = type_
    return q


def bands(n):
    a, b = n // 3, (2 * n) // 3

    def rg(x, y):
        return str(y) if x >= y else f'{x}–{y}'
    return rg(1, max(1, a)), rg(a + 1, max(a + 1, b)), rg(b + 1, n)


def fx(t, C, D, entries, typ=None):
    """Fixed items without the core's English auto-pairing: (stem, answer, key[, distractors])."""
    for e in entries:
        def fn(r, D_, e=e):
            if len(e) > 3 and e[3]:
                return mq(r, e[0], e[1], e[3], e[2])
            return item(e[0], e[1], e[2], mk(C, D_), typ or ('short' if C == 'C1' else 'explain'))
        fn.__name__ = 'fx'
        t.add(C, D, typ)(fn)


# =========================================================== factory: tag bank (classification)

TB_INTRO = ['निम्नलिखित वाक्य ध्यान से पढ़िए।', 'नीचे दिया गया वाक्य पढ़िए।', 'इस वाक्य पर ध्यान दीजिए।', 'दिए गए वाक्य को पढ़कर उत्तर दीजिए।']


def tagbank(t, bank, labels, what, defs=None, people=True, c4=True, c3=True, c2=True, c1=True, unit='शब्द', noun='वाक्य', link=' में'):
    """bank: (sentence-with-{N}, target, label, reason). The target is quoted in the stem; the label is what is asked.
    target may be '' when the whole sentence is classified (वाक्य-भेद)."""
    defs = defs or {}

    def fill(r, s):
        n, g = name(r)
        return A(s.replace('{N}', n), g), n, g

    def tgt(e, s):
        return f' में {Q(e[1])}' if e[1] else link

    if c1:
        @t.add('C1', (1, 2, 3))
        def tb_c1(r, D):
            e = r.choice(bank)
            s, _, _ = fill(r, e[0])
            frame = r.choice(['{i} {s} इस {nn}{t} {w} क्या है?', '{i} {s} बताइए कि इस {nn}{t} {w} कौन-सा है।',
                              '{nn} {s}{t} {w} पहचानिए।'])
            stem = frame.format(i=r.choice(TB_INTRO) if noun == 'वाक्य' else '', s=Q(s), t=tgt(e, s), w=what, nn=noun)
            return mq(r, stem, e[2], [x for x in labels if x != e[2]], e[3])

    if c2:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def tb_c2(r, D):
            e = r.choice(bank)
            s, n, g = fill(r, e[0])
            m = mk('C2', D)
            if r.random() < 0.5:
                wrong = r.choice([x for x in labels if x != e[2]])
                p, pg = name(r)
                stem = (f'{p} ने कहा कि {noun} {Q(s)}' + tgt(e, s) + f' {what} “{wrong}” है। क्या {p} सही है? '
                        + ('अपने उत्तर का कारण दीजिए।' if m <= 2 else 'कारण दीजिए और सही उत्तर को परिभाषा से जोड़कर स्पष्ट कीजिए।'))
                ans = f'नहीं। यहाँ {what} “{e[2]}” है। {e[3]}'
                key = f'“{e[2]}” पहचानने पर 1 अंक; कारण ({e[3]}) पर शेष अंक।' + (f' परिभाषा: {defs[e[2]]}' if e[2] in defs else '')
            else:
                stem = f'{noun} {Q(s)}' + tgt(e, s) + f' {what} “{e[2]}” क्यों है? स्पष्ट कीजिए।'
                ans = e[3]
                key = f'कारण: {e[3]}' + (f' परिभाषा से जोड़ने पर अतिरिक्त अंक: {defs[e[2]]}' if e[2] in defs and m > 1 else '')
            return item(stem, ans, key, m, 'explain')

    if c3:
        @t.add('C3', (1, 2, 3, 4, 5), 'short')
        def tb_c3(r, D):
            es = r.sample(bank, min(len(bank), 5))
            parts = []
            for e in es:
                s, _, _ = fill(r, e[0])
                if r.random() < 0.6 or D <= 2:
                    parts.append((f'{noun} {Q(s)}' + tgt(e, s) + f' {what} लिखिए।', e[2], f'{e[2]} [1]'))
                else:
                    parts.append((f'{noun} {Q(s)}' + tgt(e, s) + f' {what} लिखिए और कारण बताइए।', f'{e[2]} — {e[3]}', f'{e[2]} (1); कारण (1) [2]'))
            lab = r.choice(labels)
            if noun in ('शब्द', 'समस्त पद'):
                ex_ = [e[0] for e in bank if e[2] == lab and e[0] not in [x[0] for x in es]]
                parts.append((f'“{lab}” का एक अन्य उदाहरण ({noun}) लिखिए।', f'जैसे {Q(ex_[0])}' if ex_ else f'कोई भी सही उदाहरण ({lab})', f'सही उदाहरण [1]'))
            else:
                parts.append((f'“{lab}” का एक नया उदाहरण-वाक्य बनाइए' + (' और उसमें संबंधित ' + unit + ' रेखांकित कीजिए।' if bank[0][1] else '।'),
                              f'कोई भी उपयुक्त वाक्य जिसमें {lab} का सही प्रयोग हो।' + (f' ({defs[lab]})' if lab in defs else ''), f'सही उदाहरण (1); शुद्ध वाक्य (1) [2]'))
            return hcompose(r, r.choice(['निम्नलिखित प्रश्नों के उत्तर दीजिए।', 'सभी भागों के उत्तर दीजिए।', 'व्याकरण के आधार पर उत्तर लिखिए।']) + f' ({what})', parts, k=(2, 3, 4))

    if c4:
        @t.add('C4', (2, 3, 4, 5), 'multi_step')
        def tb_c4(r, D):
            k = min(len(bank), 3 + (D >= 4))
            es = r.sample(bank, k)
            sents = []
            for e in es:
                s, _, _ = fill(r, e[0])
                sents.append((s, e))
            m = mk('C4', D)
            lines = '\n'.join(f'{i + 1}. {s}' + (f' — {Q(e[1])}' if e[1] else '') for i, (s, e) in enumerate(sents))
            ask = r.choice([f'प्रत्येक वाक्य में {what} पहचानिए और कारण दीजिए। फिर इनमें से किसी एक उदाहरण को बदलकर दूसरा भेद बनाइए और बताइए कि क्या बदला।',
                            f'प्रत्येक के लिए {what} लिखिए और अपने उत्तर को व्याकरण के नियम से सिद्ध कीजिए। अंत में बताइए कि इनमें से कौन-सा उदाहरण सबसे अधिक भ्रम पैदा कर सकता है और क्यों।',
                            f'इन उदाहरणों का {what} के आधार पर वर्गीकरण कीजिए, प्रत्येक का कारण दीजिए और हर भेद का अपना एक नया उदाहरण भी लिखिए।'])
            stem = f'नीचे दिए गए उदाहरणों को ध्यान से पढ़िए।\n{lines}\n{ask}'
            ans = ' '.join(f'{i + 1}. {e[2]} — {e[3]}' for i, (s, e) in enumerate(sents))
            per = max(1, (m - 1) // k)
            key = (f'प्रत्येक सही पहचान और कारण के लिए लगभग {per} अंक ({k} उदाहरण); अंतिम भाग (परिवर्तन / भ्रम का विश्लेषण / नए उदाहरण) के लिए शेष अंक। '
                   f'अपेक्षित उत्तर: ' + '; '.join(f'{i + 1}. {e[2]}' for i, (s, e) in enumerate(sents)) + f'। [{m}]')
            return item(stem, ans, key, m, 'multi_step')


# =========================================================== factory: transformations

def xform(t, bank, instr, rule=None, wrongs=None, c1=True, c2=True, c3=True, c4=True, label='परिवर्तन', people=True):
    """bank: (source-with-{N}, target, note[, [wrong forms]]). instr: what to do, e.g. 'संधि-विच्छेद कीजिए'."""

    def fill(r, e):
        n, g = name(r)
        return A(e[0].replace('{N}', n), g), A(e[1].replace('{N}', n), g), n, g

    if c1:
        @t.add('C1', (1, 2, 3))
        def xf_c1(r, D):
            e = r.choice(bank)
            s, tg, n, g = fill(r, e)
            own = [x for x in dict.fromkeys(A(w.replace('{N}', n), g) for w in (e[3] if len(e) > 3 else [])) if x != tg][:3]
            rest = [x for x in dict.fromkeys(A(x[1].replace('{N}', n), g) for x in bank) if x != tg and x not in own]
            if len(own) + len(rest) < 3:
                return None
            pick = own + r.sample(rest, 3 - len(own))
            stem = r.choice(['{i}: {s}', 'सही विकल्प चुनिए। {i}: {s}', '{s} — {i}।']).format(i=instr.rstrip('।'), s=Q(s))
            return mq(r, stem, tg, pick, e[2])

    if c2:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def xf_c2(r, D):
            e = r.choice(bank)
            s, tg, n, g = fill(r, e)
            m = mk('C2', D)
            ws = [A(w.replace('{N}', n), g) for w in (e[3] if len(e) > 3 else [])]
            if ws and r.random() < 0.6:
                p, pg = name(r)
                w = r.choice(ws)
                stem = (f'{instr.rstrip("।")} — इस प्रश्न के उत्तर में {p} ने लिखा: {Q(s)} → {Q(w)}। '
                        + r.choice(['क्या यह उत्तर सही है? त्रुटि बताइए और सही उत्तर लिखिए।', 'उत्तर की जाँच कीजिए; यदि गलत है तो कारण सहित सुधारिए।']))
                ans = f'नहीं। सही उत्तर {Q(tg)} है। {e[2]}'
                key = f'त्रुटि पहचानना (1); सही रूप {Q(tg)}' + (' (1); नियम/कारण (1)' if m >= 3 else '') + f'। {e[2]}'
            else:
                stem = f'{Q(s)} → {Q(tg)}। ' + r.choice([f'यह {label} किस नियम से हुआ है? स्पष्ट कीजिए।', f'इस {label} का नियम उदाहरण सहित समझाइए।'])
                ans = e[2]
                key = f'नियम/कारण: {e[2]}' + (f' {rule}' if rule and m > 2 else '')
            return item(stem, ans, key, m, 'explain')

    if c3:
        @t.add('C3', (1, 2, 3, 4, 5), 'short')
        def xf_c3(r, D):
            es = r.sample(bank, min(len(bank), 5))
            parts = []
            for e in es:
                s, tg, n, g = fill(r, e)
                if D >= 3 and r.random() < 0.4:
                    parts.append((f'{Q(s)} — {instr.rstrip("।")} और नियम का नाम/कारण लिखिए।', f'{tg} ({e[2]})', f'{tg} (1); कारण (1) [2]'))
                else:
                    parts.append((f'{Q(s)} — {instr.rstrip("।")}।', tg, f'{tg} [1]'))
            return hcompose(r, r.choice(['निर्देशानुसार उत्तर दीजिए।', 'नीचे दिए गए प्रत्येक भाग का उत्तर लिखिए।', 'सभी भाग हल कीजिए।']), parts, k=(2, 3, 4))

    if c4:
        @t.add('C4', (2, 3, 4, 5), 'multi_step')
        def xf_c4(r, D):
            k = 3 + (D >= 4)
            es = r.sample(bank, min(len(bank), k))
            filled = [fill(r, e) for e in es]
            m = mk('C4', D)
            lines = '\n'.join(f'{i + 1}. {Q(s)}' for i, (s, tg, n, g) in enumerate(filled))
            ask = r.choice([f'{instr.rstrip("।")}। प्रत्येक में लागू नियम बताइए और अंत में अपना एक नया उदाहरण बनाकर उसी प्रकार हल कीजिए।',
                            f'{instr.rstrip("।")}। फिर बताइए कि इन उदाहरणों में कौन-सा नियम बार-बार लागू हुआ है और विद्यार्थी इसमें आम तौर पर क्या गलती करते हैं।',
                            f'{instr.rstrip("।")} और प्रत्येक उत्तर का कारण दीजिए। अंत में एक ऐसा वाक्य/उदाहरण लिखिए जिसमें यह {label} सही ढंग से प्रयुक्त हो।'])
            stem = f'{lines}\n{ask}'
            ans = ' '.join(f'{i + 1}. {tg} — {e[2]}' for i, ((s, tg, n, g), e) in enumerate(zip(filled, es)))
            key = (f'प्रत्येक सही {label} के लिए 1 अंक और कारण के लिए आंशिक अंक; अंतिम भाग के लिए 1–2 अंक। अपेक्षित: '
                   + '; '.join(f'{i + 1}. {tg}' for i, (s, tg, n, g) in enumerate(filled)) + f'। [{m}]')
            return item(stem, ans, key, m, 'multi_step')


# =========================================================== factory: term -> meaning

def dpl(term):
    if term.endswith('ा'):
        return term[:-1] + 'े'
    if term.endswith('ि'):
        return term + 'याँ'
    return term


def meanings(t, bank, what='अर्थ', term='शब्द', plural=None, usage=True, c4task=None, c1=True, c2=True, c3=True, c4=True):
    """bank: (term, meaning, sentence-with-___ or '', [distractor meanings] or None)."""
    plural = plural or term + 'ों'

    if c1:
        @t.add('C1', (1, 2, 3))
        def mn_c1(r, D):
            e = r.choice(bank)
            own = list(e[3]) if len(e) > 3 and e[3] else []
            pool = own + others(r, [x[1] for x in bank], e[1], 6)
            ds = [d for d in dict.fromkeys(pool) if d != e[1]]
            frame = r.choice([f'{term} {Q(e[0])} का सही {what} क्या है?', f'{Q(e[0])} — इस {dpl(term)} का {what} चुनिए।', f'सही विकल्प चुनिए: {Q(e[0])} का {what} है'])
            return mq(r, frame, e[1], (own + [d for d in ds if d not in own])[:max(3, len(own))], f'{Q(e[0])} = {e[1]}।')

    if c1 and len(bank) >= 6:
        @t.add('C1', (1, 2, 3))
        def mn_c1r(r, D):
            e = r.choice(bank)
            ds = others(r, [x[0] for x in bank], e[0], 3)
            return mq(r, f'किस {dpl(term)} का {what} {Q(e[1])} है?', e[0], ds, f'{Q(e[0])} = {e[1]}।')

    def sent(r, e):
        p, pg = name(r)
        return A(e[2].replace('{N}', p), pg) if e[2] else ''

    if c2:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def mn_c2(r, D):
            m = mk('C2', D)
            e = r.choice(bank)
            s = sent(r, e)
            if s and r.random() < 0.6:
                stem = (f'वाक्य {Q(s)} में {term} {Q(e[0])} का क्या {what} है? ' +
                        r.choice(['स्पष्ट कीजिए कि प्रसंग से यह अर्थ कैसे समझ में आता है।', 'वाक्य के प्रसंग के आधार पर समझाइए।']) + (' इसी अर्थ में अपना एक वाक्य भी बनाइए।' if m >= 3 else ''))
                ans = f'{what}: {e[1]}। प्रसंग में यही भाव व्यक्त हो रहा है।'
                key = f'सही {what} (1)' + ('; प्रसंग से जोड़कर स्पष्टीकरण (1)' if m >= 2 else '') + ('; अपना शुद्ध वाक्य (1)' if m >= 3 else '')
            else:
                stem = f'{term} {Q(e[0])} का {what} लिखिए और उसका अपने वाक्य में प्रयोग कीजिए।' + (' ऐसा वाक्य बनाइए जिससे अर्थ स्पष्ट हो जाए।' if m >= 3 else ' उत्तर संक्षेप में दीजिए।')
                ans = f'{what}: {e[1]}।' + (f' उदाहरण: {s}' if s else f' कोई भी उपयुक्त वाक्य जिसमें {Q(e[0])} का सही प्रयोग हो।')
                key = f'{what} (1)' + ('; अर्थ स्पष्ट करने वाला शुद्ध वाक्य (1)' if m >= 2 else '') + ('; प्रसंग पूरी तरह स्पष्ट (1)' if m >= 3 else '')
            return item(stem, ans, key, m, 'explain')

    if c3:
        @t.add('C3', (1, 2, 3, 4, 5), 'short')
        def mn_c3(r, D):
            es = r.sample(bank, min(len(bank), 5))
            parts = []
            for e in es:
                s = sent(r, e)
                if s and r.random() < 0.6:
                    parts.append((f'वाक्य {Q(s)} में प्रयुक्त {term} {Q(e[0])} का {what} लिखिए।', e[1], f'{e[1]} [1]'))
                else:
                    parts.append((f'{Q(e[0])} का {what} लिखिए।', e[1], f'{e[1]} [1]'))
            if usage:
                e = r.choice(bank)
                parts.append((f'{Q(e[0])} का ऐसा वाक्य-प्रयोग कीजिए जिससे उसका {what} स्पष्ट हो।', f'{what} “{e[1]}” को स्पष्ट करने वाला कोई भी शुद्ध वाक्य।', 'सही प्रयोग (1); शुद्ध वाक्य (1) [2]'))
            return hcompose(r, r.choice(['निर्देशानुसार उत्तर दीजिए।', 'सभी भागों के उत्तर लिखिए।', f'{term} और उसके {what} पर आधारित प्रश्न।']), parts, k=(2, 3, 4))

    if c4:
        @t.add('C4', (2, 3, 4, 5), 'multi_step')
        def mn_c4(r, D):
            k = 3 + (D >= 4)
            es = r.sample(bank, min(len(bank), k))
            m = mk('C4', D)
            words = ', '.join(Q(e[0]) for e in es)
            sit = c4task(r) if c4task else r.choice(['अपने स्कूल के खेल-दिवस', 'किसी यादगार यात्रा', 'परिवार के साथ बिताए एक दिन', 'किसी मित्र की सहायता', 'बारिश के एक दिन', 'एक कठिन परीक्षा'])
            stem = (f'{words} — इन {plural} के {what} लिखिए। फिर {sit} पर लगभग {40 + 20 * D} शब्दों का एक अनुच्छेद लिखिए जिसमें इन सभी का प्रसंग के अनुसार सही प्रयोग हो। '
                    f'प्रयोग किए गए {dpl(term)} रेखांकित कीजिए।')
            ans = ' '.join(f'{Q(e[0])} = {e[1]}।' for e in es) + ' अनुच्छेद: प्रसंग से जुड़ा, सुसंगठित, सभी शब्दों का सही अर्थ में प्रयोग।'
            key = (f'{what} — प्रत्येक के लिए आधा/एक अंक ({len(es)} {dpl(term)}); अनुच्छेद में प्रत्येक सही प्रयोग के लिए अंक; '
                   f'विषय से जुड़ाव, क्रम और भाषा की शुद्धता के लिए शेष अंक। [{m}]')
            return item(stem, ans, key, m, 'multi_step')


# =========================================================== factory: reading / listening

R_INTRO = {
    'read': ['नीचे दिया गया {k} पढ़िए और प्रश्न का उत्तर दीजिए।', 'निम्नलिखित {k} ध्यान से पढ़िए।', '{k} पढ़कर दिए गए प्रश्न का उत्तर लिखिए।', 'इस {k} को पढ़िए।'],
    'listen': ['आप एक {k} सुनेंगे। नीचे उसका प्रतिलेख दिया गया है। ध्यान से पढ़कर (सुनकर) उत्तर दीजिए।', 'श्रवण-अभ्यास: नीचे एक {k} का प्रतिलेख है। इसे सुनने के बाद प्रश्न का उत्तर दीजिए।',
               '{k} का प्रतिलेख पढ़िए (परीक्षा में आप इसे दो बार सुनेंगे)।', 'नीचे दिए गए {k} को सुनिए (प्रतिलेख दिया गया है)।'],
    'extract': ['निम्नलिखित {k} पढ़कर प्रश्न का उत्तर दीजिए।', 'नीचे दिए गए {k} को ध्यान से पढ़िए।', 'इस {k} पर आधारित प्रश्न का उत्तर लिखिए।'],
}
SRC = {'read': 'पाठ', 'listen': 'प्रतिलेख', 'extract': 'अंश'}


FEM_HEADS = {'कहानी', 'घोषणा', 'बातचीत', 'कविता', 'चर्चा', 'रिपोर्ट', 'सूचना', 'भेंटवार्ता', 'वार्ता', 'टिप्पणी', 'समीक्षा', 'पोस्ट', 'प्रविष्टि', 'बहस', 'कमेंट्री', 'सूची', 'समय-सारिणी', 'पुस्तिका', 'ब्रोशर-सामग्री'}


def intro_fix(s, kind):
    s = re.sub(r'का (अंश|प्रतिलेख|अनुच्छेद|लेख|संदेश|विज्ञापन) को', r'के \1 को', s)
    if kind.split()[-1] in FEM_HEADS:
        s = s.replace('दिए गए ' + kind, 'दी गई ' + kind).replace('दिया गया ' + kind, 'दी गई ' + kind)
    return s


def frame_of(r, frames, mode):
    for _ in range(6):
        P = r.choice(frames)(r)
        if P:
            P.setdefault('kind', 'पाठ')
            P['intro'] = intro_fix(r.choice(R_INTRO[mode]).format(k=P['kind']), P['kind'])
            P['mode'] = mode
            return P
    return None


def head(P):
    return P['intro'] + '\n' + P['text'].strip() + '\n'


def summ_words(D):
    return {1: '30–40', 2: '40–50', 3: '50–60', 4: '60–80', 5: '80–100'}.get(D, '50–60')


def open_q(r, x):
    """A fact question asked without MCQ options: questions that only make sense with choices
    (“इनमें से…”, negative “… नहीं …?”) carry their choices inline."""
    q, a, ds = x[0], x[1], list(x[2]) if len(x) > 2 else []
    if ds and ('इनमें से' in q or ' नहीं ' in q or q.rstrip('?').endswith('नहीं')):
        ch = [a] + ds[:3]
        r.shuffle(ch)
        return f'{q} (विकल्प: {" / ".join(ch)})'
    return q


def reading(t, frames, mode='read', c1=True, c2=True, c3=True, c4=True, c4kinds=('notes', 'summary', 'eval', 'views')):
    """frames: f(r) -> dict(text, kind, facts=[(q, a, [ds])], vocab=[(w, meaning, [ds])], tf=[(stmt, bool, why)],
    infer=[(q, a)], title=(good, [bad]), notes={heading: [points]}, points=[...], views=[(who, view, [ds])], eval=[(q, a)])."""

    if c1:
        @t.add('C1', (1, 2, 3))
        def rd_c1(r, D):
            P = frame_of(r, frames, mode)
            if not P:
                return None
            pool = [('f', x) for x in P.get('facts', [])] + [('v', x) for x in P.get('vocab', [])] + [('w', x) for x in P.get('views', [])]
            if not pool:
                return None
            kind, x = r.choice(pool)
            if kind == 'f':
                q, a, ds = x[:3]
                return mq(r, head(P) + q, a, ds, x[3] if len(x) > 3 else f'{SRC[mode]} में स्पष्ट रूप से यही जानकारी दी गई है।')
            if kind == 'v':
                w, a, ds = x
                return mq(r, head(P) + f'{SRC[mode] if mode != "listen" else "बातचीत"} में प्रयुक्त शब्द {Q(w)} का अर्थ है', a, ds, f'प्रसंग के अनुसार {Q(w)} = {a}।')
            who, v, ds = x
            return mq(r, head(P) + f'{who} की राय क्या है?', v, ds, f'{who} के शब्दों से यही विचार स्पष्ट होता है।')

    if c2:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def rd_c2(r, D):
            P = frame_of(r, frames, mode)
            if not P:
                return None
            m = mk('C2', D)
            opts = []
            if P.get('tf'):
                opts.append('tf')
            if P.get('infer'):
                opts += ['inf', 'inf']
            if P.get('title') and m <= 2:
                opts.append('title')
            if P.get('views') and len(P['views']) >= 2:
                opts.append('who')
            if not opts:
                return None
            k = r.choice(opts)
            if k == 'tf':
                st, ok, why = r.choice(P['tf'])
                stem = head(P) + f'यह कथन सही है या गलत? {SRC[mode]} के आधार पर कारण दीजिए: {Q(st)}'
                return item(stem, ('सही। ' if ok else 'गलत। ') + why, f'सही/गलत की पहचान (1)' + ('; पाठ से कारण (1)' if m >= 2 else '') + ('; पूर्ण, स्पष्ट उत्तर (1)' if m >= 3 else '') + f'। {why}', m, 'explain')
            if k == 'inf':
                q, a = r.choice(P['infer'])
                ask = r.choice(['', ' अपने उत्तर के समर्थन में ' + SRC[mode] + ' से प्रमाण दीजिए।']) if m >= 2 else ''
                return item(head(P) + q + ask, a, f'मुख्य बिंदु: {a}' + (f' प्रमाण सहित स्पष्ट उत्तर के लिए पूरे {m} अंक।' if m >= 2 else ''), m, 'explain')
            if k == 'who':
                (w1, v1, _), (w2, v2, _) = r.sample(P['views'], 2)
                stem = head(P) + f'{w1} और {w2} के विचारों में क्या अंतर है? स्पष्ट कीजिए।'
                return item(stem, f'{w1}: {v1} जबकि {w2}: {v2}', f'{w1} का विचार (1); {w2} का विचार (1)' + ('; अंतर स्पष्ट रूप से बताना (1)' if m >= 3 else ''), m, 'explain')
            good, bad = P['title']
            return mq(r, head(P) + f'इस {P["kind"]} के लिए सबसे उपयुक्त शीर्षक कौन-सा है?', good, bad, 'यह शीर्षक पूरे पाठ के मुख्य विषय को समेटता है; अन्य शीर्षक किसी एक अंश तक सीमित या असंबद्ध हैं।')

    if c3:
        @t.add('C3', (1, 2, 3, 4, 5), 'short')
        def rd_c3(r, D):
            P = frame_of(r, frames, mode)
            if not P:
                return None
            parts = []
            for x in r.sample(P.get('facts', []), min(4, len(P.get('facts', [])))):
                parts.append((open_q(r, x), x[1], f'{x[1]} [1]'))
            for w, a, ds in P.get('vocab', [])[:1]:
                parts.append((f'{Q(w)} शब्द का अर्थ प्रसंग के अनुसार लिखिए।', a, f'{a} [1]'))
            for st, ok, why in r.sample(P.get('tf', []), min(1, len(P.get('tf', [])))):
                parts.append((f'सही या गलत लिखिए और कारण दीजिए: {Q(st)}', ('सही — ' if ok else 'गलत — ') + why, f'सही/गलत (1); कारण (1) [2]'))
            for q, a in r.sample(P.get('infer', []), min(1 + (D >= 4), len(P.get('infer', [])))):
                parts.append((q, a, f'{a} [2]'))
            if not parts:
                return None
            r.shuffle(parts)
            return hcompose(r, head(P) + r.choice(['प्रश्नों के उत्तर दीजिए।', 'नीचे दिए गए प्रश्नों के उत्तर संक्षेप में लिखिए।', 'सभी भागों के उत्तर दीजिए।']), parts, k=(2, 3, 4), keep_order=False)

    if c4:
        @t.add('C4', (2, 3, 4, 5), 'multi_step')
        def rd_c4(r, D):
            P = frame_of(r, frames, mode)
            if not P:
                return None
            m = mk('C4', D)
            ks = [k for k in c4kinds if P.get({'summary': 'points'}.get(k, k))]
            if 'views' in ks and len(P['views']) < 2:
                ks.remove('views')
            if not ks:
                return None
            k = r.choice(ks)
            if k == 'notes':
                hs = list(P['notes'])
                pick = r.sample(hs, min(len(hs), 2 + (D >= 4)))
                need = max(2, (m + len(pick) - 1) // len(pick))
                stem = head(P) + (f'{SRC[mode]} के आधार पर नोट्स बनाइए। प्रत्येक शीर्षक के अंतर्गत कम से कम {need if m > 4 else 2} बिंदु लिखिए: '
                                  + '; '.join(Q(h) for h in pick) + '। बिंदु छोटे वाक्यांशों में लिखें।')
                ans = ' '.join(f'{h}: ' + '; '.join(P['notes'][h]) + '।' for h in pick)
                key = f'प्रत्येक सही, प्रासंगिक बिंदु के लिए 1 अंक, अधिकतम {m} अंक। स्वीकार्य बिंदु — ' + ans + f' [{m}]'
                return item(stem, ans, key, m, 'multi_step')
            if k == 'summary':
                pts = P['points']
                stem = head(P) + r.choice([f'इस {P["kind"]} का सारांश लगभग {summ_words(D)} शब्दों में अपने शब्दों में लिखिए।',
                                           f'{SRC[mode]} के मुख्य विचारों को लगभग {summ_words(D)} शब्दों में अपने शब्दों में प्रस्तुत कीजिए।'])
                cm = max(1, m - max(1, m // 3))
                key = (f'विषय-वस्तु: प्रत्येक मुख्य बिंदु के लिए 1 अंक, अधिकतम {cm} अंक; भाषा और अपने शब्दों में संक्षिप्त प्रस्तुति के लिए {m - cm} अंक। '
                       f'मुख्य बिंदु — ' + '; '.join(pts) + f'। [{m}]')
                return item(stem, '; '.join(pts) + '।', key, m, 'multi_step')
            if k == 'views':
                vs = P['views']
                stem = head(P) + r.choice(['सभी वक्ताओं के विचारों की तुलना कीजिए। आप किसके विचार से अधिक सहमत हैं? दो कारण दीजिए।',
                                           'वक्ताओं के विचार कहाँ मिलते हैं और कहाँ अलग हैं? स्पष्ट कीजिए और अपनी राय भी कारण सहित लिखिए।'])
                ans = ' '.join(f'{w}: {v.rstrip("।")}।' for w, v, _ in vs) + ' अपनी राय: कोई भी तर्कसंगत पक्ष, दो कारणों सहित।'
                key = f'प्रत्येक वक्ता का विचार सही पहचानना (1-1); तुलना (1); अपनी राय के दो कारण (शेष अंक)। [{m}]'
                return item(stem, ans, key, m, 'multi_step')
            ev = P['eval']
            q, a = r.choice(ev)
            parts = [(q, a, f'{a} [{max(2, m - 2)}]')]
            for qq, aa in r.sample(P.get('infer', []), min(2, len(P.get('infer', [])))):
                parts.append((qq, aa, f'{aa} [2]'))
            for x in r.sample(P.get('facts', []), min(1, len(P.get('facts', [])))):
                parts.append((open_q(r, x), x[1], f'{x[1]} [1]'))
            out = hcompose(r, head(P) + 'नीचे दिए गए प्रश्नों के उत्तर दीजिए।', parts, k=(2, 3), want=m)
            out['type'] = 'multi_step'
            return out


# =========================================================== factory: writing

WORDS = {1: '50–60', 2: '60–80', 3: '80–100', 4: '100–120', 5: '130–150'}
LANG = ('भाषा: शब्द-भंडार विविध और सटीक; वाक्य-रचना में विविधता (संयोजक, मिश्र वाक्य); शैली और संबोधन पाठक के अनुरूप; व्याकरण (लिंग, वचन, काल, ने का प्रयोग) और वर्तनी लगभग पूरी तरह शुद्ध',
        'भाषा: शब्द-भंडार उपयुक्त; कुछ जटिल वाक्य; शैली अधिकांशतः उपयुक्त; कुछ त्रुटियाँ जो अर्थ में बाधा नहीं डालतीं',
        'भाषा: सरल और दोहराव वाले शब्द; छोटे सरल वाक्य; शैली अस्थिर; बार-बार त्रुटियाँ जो कभी-कभी अर्थ अस्पष्ट करती हैं')


def wkey(m, form, bullets, ind):
    a = max(1, round(m * 0.5))
    b = m - a
    lo, mi, hi = bands(a)
    slo, smi, shi = bands(b)
    pts = '; '.join(bullets)
    return (f'स्तर-आधारित अंकन, कुल {m} अंक: विषय-वस्तु और कार्य-पूर्ति {a} अंक, भाषा {b} अंक। '
            f'विषय-वस्तु — उच्च स्तर ({hi}): सभी बिंदु ({pts}) विस्तार से और प्रासंगिक ढंग से; {form} का प्रारूप और उद्देश्य पूरी तरह स्पष्ट; '
            f'मध्य स्तर ({mi}): अधिकांश बिंदु, कुछ विस्तार; प्रारूप पहचानने योग्य; निम्न स्तर ({lo}): एक-दो बिंदु, बहुत कम विस्तार या प्रारूप अस्पष्ट। '
            f'भाषा — उच्च ({shi}): {LANG[0]}; मध्य ({smi}): {LANG[1]}; निम्न ({slo}): {LANG[2]}। '
            f'संकेतक विषय-वस्तु: {ind} [{m}]')


FEM_FORMS = {'सूचना', 'कहानी', 'डायरी', 'रिपोर्ट', 'समीक्षा'}


def writing(t, form, tasks, facts=(), flaws=(), short=(), c1=True, c2=True, c3=True, c4=True, words=WORDS):
    """tasks: f(r) -> dict(task, bullets, ind, model). facts: (q, a, [ds], why) about the form.
    flaws: (sample-with-{N}, problem, fix). short: f(r, D) -> (stem, answer, key-without-marks) for short productive tasks."""
    fem = form in FEM_FORMS
    kk = 'की' if fem else 'के'

    if c1 and facts:
        @t.add('C1', (1, 2, 3))
        def wr_c1(r, D):
            q, a, ds, why = r.choice(facts)
            return mq(r, q, a, ds, why)

    if c1 and flaws:
        @t.add('C1', (1, 2, 3))
        def wr_c1b(r, D):
            s, prob, fix = r.choice(flaws)
            n, g = name(r)
            s = A(s.replace('{N}', n), g)
            fix = A(fix.replace('{N}', n), g)
            ds = others(r, [f[1] for f in flaws if f[1] != prob], prob, 3)
            if len(ds) < 3:
                return None
            return mq(r, f'{form} के इस अंश में मुख्य कमी क्या है? {Q(s)}', prob, ds, f'सुधार: {fix}')

    if c2 and flaws:
        @t.add('C2', (1, 2, 3, 4), 'explain')
        def wr_c2(r, D):
            s, prob, fix = r.choice(flaws)
            n, g = name(r)
            s = A(s.replace('{N}', n), g)
            fix = A(fix.replace('{N}', n), g)
            m = mk('C2', D)
            stem = r.choice([f'{n} ने {form} में यह अंश लिखा: {Q(s)} इसमें क्या कमी है? स्पष्ट कीजिए' + (' और इसे सुधारकर लिखिए।' if m >= 2 else '। उत्तर संक्षेप में दीजिए।'),
                             f'एक विद्यार्थी {kk} {form} का अंश पढ़िए: {Q(s)} बताइए कि यह {form} के उद्देश्य या शैली के अनुरूप क्यों नहीं है' + (' और सुधार सुझाइए।' if m >= 2 else '। उत्तर संक्षेप में दीजिए।')])
            return item(stem, f'{prob} सुधार: {fix}', f'कमी की पहचान (1)' + ('; उपयुक्त सुधार (1)' if m >= 2 else '') + ('; शैली/पाठक से जोड़कर कारण (1)' if m >= 3 else '') + f'। अपेक्षित: {prob}', m, 'explain')

    if c3:
        @t.add('C3', (1, 2, 3, 4, 5), 'short')
        def wr_c3(r, D):
            m = mk('C3', D)
            if short and r.random() < 0.5:
                x = r.choice(short)(r, D)
                if x:
                    stem, ans, key = x
                    if m <= 2:
                        key = re.sub(r'\s*\(\d\)', '', key)
                    return item(stem, ans, key + f' [{m}]', m, 'short')
            T = r.choice(tasks)(r)
            b = r.choice(T['bullets'])
            part = r.choice([f'इस {form} का केवल वह अनुच्छेद लिखिए जिसमें यह बिंदु हो: {Q(b)}। लगभग {20 + 10 * D} शब्द।',
                             f'इस {form} का आरंभ (संबोधन/शीर्षक और पहले दो-तीन वाक्य) तथा अंत लिखिए।' if D <= 3 else f'इस {form} की रूपरेखा बनाइए: प्रत्येक बिंदु के लिए एक-एक वाक्य, और उपयुक्त आरंभ-अंत।'])
            stem = f'{T["task"]}\n' + part
            key = f'उपयुक्त प्रारूप/शैली (1); बिंदु का प्रासंगिक विस्तार; भाषा की शुद्धता। अपेक्षित: {T["ind"]} [{m}]'
            return item(stem, T.get('model', T['ind']), key, m, 'short')

    if c4:
        @t.add('C4', (2, 3, 4, 5), 'long')
        def wr_c4(r, D):
            T = r.choice(tasks)(r)
            m = mk('C4', D, long=True)
            bl = T['bullets'][:3 if D <= 3 else 4] if len(T['bullets']) > 3 and D <= 3 else T['bullets']
            stem = (f'{T["task"]}\n{"अपनी" if fem else "अपने"} {form} में ये बातें अवश्य लिखिए:\n' + '\n'.join(f'• {b}' for b in bl)
                    + f'\nलगभग {words.get(D, "80–100")} शब्दों में लिखिए।')
            return item(stem, T.get('model', T['ind']), wkey(m, form, bl, T['ind']), m, 'long', minutes=min(40, round(m * 1.5)))


# =========================================================== grammar banks (shared)

SANGYA_L = ['व्यक्तिवाचक संज्ञा', 'जातिवाचक संज्ञा', 'भाववाचक संज्ञा', 'समूहवाचक संज्ञा', 'द्रव्यवाचक संज्ञा']
SANGYA_DEF = {'व्यक्तिवाचक संज्ञा': 'जो शब्द किसी विशेष व्यक्ति, स्थान या वस्तु का नाम बताए।',
              'जातिवाचक संज्ञा': 'जो शब्द किसी पूरी जाति (एक ही प्रकार के सभी प्राणियों/वस्तुओं) का बोध कराए।',
              'भाववाचक संज्ञा': 'जो शब्द किसी गुण, दशा, भाव या अवस्था का नाम बताए, जिसे केवल अनुभव किया जा सके।',
              'समूहवाचक संज्ञा': 'जो शब्द व्यक्तियों या वस्तुओं के समूह का बोध कराए।',
              'द्रव्यवाचक संज्ञा': 'जो शब्द किसी पदार्थ या द्रव्य का बोध कराए जिसे नापा-तौला जाता है, गिना नहीं जाता।'}
SANGYA = [
    ('{N} ने गंगा के किनारे सूर्योदय देखा।', 'गंगा', 'व्यक्तिवाचक संज्ञा', 'यह एक विशेष नदी का नाम है।'),
    ('हिमालय भारत की उत्तरी सीमा पर स्थित है।', 'हिमालय', 'व्यक्तिवाचक संज्ञा', 'यह एक विशेष पर्वत का नाम है।'),
    ('{N} की ईमानदारी की सब प्रशंसा करते हैं।', 'ईमानदारी', 'भाववाचक संज्ञा', 'यह एक गुण का नाम है जिसे देखा-छुआ नहीं जा सकता, केवल अनुभव किया जा सकता है।'),
    ('बगीचे में एक बूढ़ा पेड़ खड़ा है।', 'पेड़', 'जातिवाचक संज्ञा', 'यह किसी एक विशेष पेड़ का नहीं, पेड़ों की पूरी जाति का नाम है।'),
    ('कक्षा ने मिलकर विद्यालय में पौधे लगाए।', 'कक्षा', 'समूहवाचक संज्ञा', 'यह विद्यार्थियों के पूरे समूह का बोध कराता है।'),
    ('माँ ने गिलास में दूध डाला।', 'दूध', 'द्रव्यवाचक संज्ञा', 'दूध एक द्रव्य है जिसे नापा जाता है, गिना नहीं जाता।'),
    ('{N} को बचपन की बातें बहुत याद आती हैं।', 'बचपन', 'भाववाचक संज्ञा', 'यह जीवन की एक अवस्था का नाम है।'),
    ('मेले में बहुत भीड़ थी।', 'भीड़', 'समूहवाचक संज्ञा', 'यह बहुत-से लोगों के समूह का बोध कराता है।'),
    ('ताजमहल आगरा में स्थित है।', 'आगरा', 'व्यक्तिवाचक संज्ञा', 'यह एक विशेष शहर का नाम है।'),
    ('{N} ने बाज़ार से एक किलो चीनी खरीदी।', 'चीनी', 'द्रव्यवाचक संज्ञा', 'चीनी एक पदार्थ है जिसे तौला जाता है।'),
    ('पहाड़ों पर ठंडी हवा चलती है।', 'पहाड़ों', 'जातिवाचक संज्ञा', 'यह सभी पहाड़ों की जाति का बोध कराता है, किसी विशेष पहाड़ का नहीं।'),
    ('दादी की कहानियों में अनोखी मिठास है।', 'मिठास', 'भाववाचक संज्ञा', 'यह एक गुण/भाव का नाम है जो अनुभव किया जाता है।'),
    ('सेना ने बाढ़ में फँसे लोगों की सहायता की।', 'सेना', 'समूहवाचक संज्ञा', 'यह सैनिकों के समूह का बोध कराता है।'),
    ('{N} अपनी बहन के साथ लखनऊ ग{या}।', 'लखनऊ', 'व्यक्तिवाचक संज्ञा', 'यह एक विशेष शहर का नाम है।'),
    ('मेज़ पर एक पुस्तक रखी है।', 'पुस्तक', 'जातिवाचक संज्ञा', 'यह सभी पुस्तकों की जाति का नाम है।'),
    ('उस बच्चे के चेहरे पर डर साफ़ दिख रहा था।', 'डर', 'भाववाचक संज्ञा', 'यह एक भाव (मन की दशा) का नाम है।'),
    ('गाड़ी में पेट्रोल खत्म हो गया।', 'पेट्रोल', 'द्रव्यवाचक संज्ञा', 'पेट्रोल एक द्रव है जिसे लीटर में नापा जाता है।'),
    ('आसमान में पक्षियों का झुंड उड़ रहा था।', 'झुंड', 'समूहवाचक संज्ञा', 'यह पक्षियों के समूह का बोध कराता है।'),
    ('{N} ने अपने मित्र की सहायता की।', 'मित्र', 'जातिवाचक संज्ञा', 'यह किसी एक व्यक्ति का नाम नहीं, मित्र कहलाने वाले सभी लोगों का बोध कराता है।'),
    ('रामायण एक प्रसिद्ध ग्रंथ है।', 'रामायण', 'व्यक्तिवाचक संज्ञा', 'यह एक विशेष ग्रंथ का नाम है।'),
    ('परिश्रम से ही सफलता मिलती है।', 'सफलता', 'भाववाचक संज्ञा', 'यह एक अवस्था/भाव का नाम है।'),
    ('लोहे की अलमारी बहुत भारी है।', 'लोहे', 'द्रव्यवाचक संज्ञा', 'लोहा एक धातु (द्रव्य) है जिसे तौला जाता है।'),
    ('{N} ने यमुना नदी पर बना पुल देखा।', 'यमुना', 'व्यक्तिवाचक संज्ञा', 'यह एक विशेष नदी का नाम है।'),
    ('बचपन से ही {N} में दया का भाव था।', 'दया', 'भाववाचक संज्ञा', 'दया एक भाव है जिसे केवल अनुभव किया जा सकता है।'),
]
BHAV_X = [
    ('मीठा', 'मिठास', '“मीठा” विशेषण में “आस” प्रत्यय लगाकर भाववाचक संज्ञा बनती है।', ['मीठापन', 'मीठी', 'मिठाई']),
    ('बच्चा', 'बचपन', '“बच्चा” जातिवाचक संज्ञा से “पन” प्रत्यय द्वारा भाववाचक संज्ञा।', ['बच्चापन', 'बच्चे', 'बचाव']),
    ('सुंदर', 'सुंदरता', '“ता” प्रत्यय से गुण का नाम बनता है।', ['सुंदरी', 'सुंदराई', 'सुंदरपन']),
    ('मित्र', 'मित्रता', '“ता” प्रत्यय से संबंध/भाव का नाम।', ['मित्री', 'मित्रपन', 'मित्रों']),
    ('चतुर', 'चतुराई', '“आई” प्रत्यय से गुण का नाम।', ['चतुरी', 'चतुरपन', 'चातुरी-पन']),
    ('गरीब', 'गरीबी', '“ई” प्रत्यय से दशा का नाम।', ['गरीबता', 'गरीबपन', 'गरीबाई']),
    ('बूढ़ा', 'बुढ़ापा', '“आपा” प्रत्यय से अवस्था का नाम।', ['बूढ़ापन', 'बुढ़ाई', 'बूढ़ी']),
    ('हँसना', 'हँसी', 'क्रिया से भाववाचक संज्ञा बनी है।', ['हँसता', 'हँसमुख', 'हँसाई']),
    ('थकना', 'थकान', 'क्रिया से “आन” प्रत्यय द्वारा भाववाचक संज्ञा।', ['थका', 'थकता', 'थकाऊ']),
    ('वीर', 'वीरता', '“ता” प्रत्यय से गुण का नाम।', ['वीराई', 'वीरपन', 'वीरी']),
    ('ऊँचा', 'ऊँचाई', '“आई” प्रत्यय से भाववाचक संज्ञा।', ['ऊँचापन', 'ऊँचता', 'ऊँची']),
    ('अपना', 'अपनापन', 'सर्वनाम से “पन” प्रत्यय द्वारा भाववाचक संज्ञा।', ['अपनाई', 'अपनता', 'अपनी']),
    ('शत्रु', 'शत्रुता', '“ता” प्रत्यय से भाव का नाम।', ['शत्रुपन', 'शत्रुआई', 'शत्रुओं']),
    ('कड़वा', 'कड़वाहट', '“आहट” प्रत्यय से भाववाचक संज्ञा।', ['कड़वाई', 'कड़वी', 'कड़वता']),
    ('लिखना', 'लिखावट', 'क्रिया से “आवट” प्रत्यय द्वारा भाववाचक संज्ञा।', ['लिखता', 'लेखक', 'लिखित']),
    ('मनुष्य', 'मनुष्यता', '“ता” प्रत्यय से भाववाचक संज्ञा।', ['मनुष्यपन', 'मानुषी', 'मनुष्याई']),
]

SARV_L = ['पुरुषवाचक सर्वनाम', 'निश्चयवाचक सर्वनाम', 'अनिश्चयवाचक सर्वनाम', 'संबंधवाचक सर्वनाम', 'प्रश्नवाचक सर्वनाम', 'निजवाचक सर्वनाम']
SARV_DEF = {'पुरुषवाचक सर्वनाम': 'बोलने वाले, सुनने वाले या जिसके बारे में बात हो, उसके लिए प्रयुक्त सर्वनाम (मैं, तुम, आप, वह)।',
            'निश्चयवाचक सर्वनाम': 'जो पास या दूर की किसी निश्चित वस्तु/व्यक्ति की ओर संकेत करे (यह, वह, ये, वे)।',
            'अनिश्चयवाचक सर्वनाम': 'जिससे किसी निश्चित व्यक्ति या वस्तु का बोध न हो (कोई, कुछ)।',
            'संबंधवाचक सर्वनाम': 'जो वाक्य के दो भागों में संबंध जोड़े (जो–सो, जिसकी–उसकी)।',
            'प्रश्नवाचक सर्वनाम': 'जो प्रश्न पूछने के लिए प्रयुक्त हो (कौन, क्या)।',
            'निजवाचक सर्वनाम': 'जो कर्ता स्वयं अपने लिए प्रयोग करे (आप, स्वयं, खुद, अपने-आप)।'}
SARV = [
    ('{N} बोल{ा}, “मैं कल पुस्तकालय जाऊँग{ा}।”', 'मैं', 'पुरुषवाचक सर्वनाम', 'बोलने वाला अपने लिए इसका प्रयोग करता है (उत्तम पुरुष)।'),
    ('दरवाज़े पर कोई खड़ा है।', 'कोई', 'अनिश्चयवाचक सर्वनाम', 'इससे किसी निश्चित व्यक्ति का बोध नहीं होता।'),
    ('दूध में कुछ गिर गया है।', 'कुछ', 'अनिश्चयवाचक सर्वनाम', 'इससे किसी निश्चित वस्तु का बोध नहीं होता।'),
    ('जो परिश्रम करता है, वह सफल होता है।', 'जो', 'संबंधवाचक सर्वनाम', 'यह वाक्य के दो भागों (जो–वह) के बीच संबंध जोड़ता है।'),
    ('{N}, तुम्हारे बैग में क्या है?', 'क्या', 'प्रश्नवाचक सर्वनाम', 'यह किसी वस्तु के बारे में प्रश्न पूछने के लिए प्रयुक्त है।'),
    ('बाहर कौन गा रहा है?', 'कौन', 'प्रश्नवाचक सर्वनाम', 'यह किसी व्यक्ति के बारे में प्रश्न पूछता है।'),
    ('{N} अपना काम स्वयं करत{ा} है।', 'स्वयं', 'निजवाचक सर्वनाम', 'कर्ता इसे अपने लिए प्रयोग करता है।'),
    ('यह मेरी पुस्तक है।', 'यह', 'निश्चयवाचक सर्वनाम', 'यह पास की एक निश्चित वस्तु की ओर संकेत करता है।'),
    ('वह हमारा विद्यालय है।', 'वह', 'निश्चयवाचक सर्वनाम', 'यह दूर की एक निश्चित वस्तु (भवन) की ओर संकेत करता है।'),
    ('हम सब शाम को पार्क में खेलेंगे।', 'हम', 'पुरुषवाचक सर्वनाम', 'बोलने वाले अपने लिए इसका प्रयोग करते हैं (उत्तम पुरुष, बहुवचन)।'),
    ('{N}, आप कहाँ रहत{े} हैं?', 'आप', 'पुरुषवाचक सर्वनाम', 'यहाँ “आप” सुनने वाले के लिए आदर से प्रयुक्त है (मध्यम पुरुष)।'),
    ('{N} ने कहा, “मैं यह काम आप ही कर लूँग{ा}।”', 'आप', 'निजवाचक सर्वनाम', 'यहाँ “आप ही” का अर्थ “स्वयं” है; कर्ता अपने लिए प्रयोग कर रहा है।'),
    ('जिसने यह चित्र बनाया, उसे पुरस्कार मिलेगा।', 'जिसने', 'संबंधवाचक सर्वनाम', 'यह “जिसने–उसे” द्वारा दो उपवाक्यों में संबंध जोड़ता है।'),
    ('किसी ने मेरी साइकिल की घंटी बजाई।', 'किसी', 'अनिश्चयवाचक सर्वनाम', 'बजाने वाला कौन था, यह निश्चित नहीं है।'),
    ('तुम्हें किसने बुलाया था?', 'किसने', 'प्रश्नवाचक सर्वनाम', 'यह व्यक्ति के बारे में प्रश्न पूछता है।'),
    ('{N} अपने-आप तैयार हो ग{या}।', 'अपने-आप', 'निजवाचक सर्वनाम', 'कर्ता ने बिना किसी की सहायता के स्वयं काम किया।'),
    ('ये मेरे मित्र के जूते हैं।', 'ये', 'निश्चयवाचक सर्वनाम', 'यह पास की निश्चित वस्तुओं की ओर संकेत करता है।'),
    ('तुम कल समय पर आ जाना।', 'तुम', 'पुरुषवाचक सर्वनाम', 'यह सुनने वाले के लिए प्रयुक्त है (मध्यम पुरुष)।'),
]

SARV_X = [
    ('{N} बाज़ार ग{या}। {N} ने फल खरीदे। {N} घर लौट आ{या}।', '{N} बाज़ार ग{या}। उसने फल खरीदे। वह घर लौट आ{या}।', 'संज्ञा की बार-बार आवृत्ति से बचने के लिए “उसने” और “वह” सर्वनाम प्रयुक्त हुए; “ने” के साथ “वह” का रूप “उसने” होता है।',
     ['{N} बाज़ार ग{या}। वह ने फल खरीदे। उसने घर लौट आ{या}।', 'वह बाज़ार ग{या}। {N} ने फल खरीदे। उसने घर लौट आ{या}।', '{N} बाज़ार ग{या}। उसको फल खरीदे। उसका घर लौट आ{या}।']),
    ('मीना की माँ डॉक्टर हैं। मीना की माँ अस्पताल में काम करती हैं।', 'मीना की माँ डॉक्टर हैं। वे अस्पताल में काम करती हैं।', 'आदर के लिए बहुवचन सर्वनाम “वे” का प्रयोग होता है।',
     ['मीना की माँ डॉक्टर हैं। वह ने अस्पताल में काम करती हैं।', 'मीना की माँ डॉक्टर हैं। उसकी अस्पताल में काम करती हैं।', 'मीना की माँ डॉक्टर हैं। उन्हें अस्पताल में काम करती हैं।']),
    ('बच्चों ने पतंगें उड़ाईं। बच्चों ने बहुत आनंद लिया।', 'बच्चों ने पतंगें उड़ाईं। उन्होंने बहुत आनंद लिया।', '“ने” के साथ बहुवचन सर्वनाम “उन्होंने” बनता है।',
     ['बच्चों ने पतंगें उड़ाईं। वे ने बहुत आनंद लिया।', 'बच्चों ने पतंगें उड़ाईं। उसने बहुत आनंद लिया।', 'बच्चों ने पतंगें उड़ाईं। उनको बहुत आनंद लिया।']),
    ('{N} मेरा पड़ोसी है। {N} के पिताजी शिक्षक हैं।', '{N} मेरा पड़ोसी है। उसके पिताजी शिक्षक हैं।', 'संबंध बताने के लिए “उसके” (वह + के) सर्वनाम।',
     ['{N} मेरा पड़ोसी है। वह के पिताजी शिक्षक हैं।', '{N} मेरा पड़ोसी है। उसका पिताजी शिक्षक हैं।', '{N} मेरा पड़ोसी है। उन्होंने पिताजी शिक्षक हैं।']),
]

VISH_L = ['गुणवाचक विशेषण', 'संख्यावाचक विशेषण', 'परिमाणवाचक विशेषण', 'सार्वनामिक विशेषण']
VISH_DEF = {'गुणवाचक विशेषण': 'जो संज्ञा के गुण, दोष, रंग, आकार, दशा आदि बताए।', 'संख्यावाचक विशेषण': 'जो संज्ञा की संख्या (निश्चित या अनिश्चित, क्रम) बताए।',
            'परिमाणवाचक विशेषण': 'जो संज्ञा की मात्रा या नाप-तौल बताए।', 'सार्वनामिक विशेषण': 'जो सर्वनाम संज्ञा से पहले आकर उसकी ओर संकेत करे (यह पुस्तक, वह लड़का)।'}
VISH = [
    ('मेज़ पर लाल गुलाब रखा है।', 'लाल', 'गुणवाचक विशेषण', 'यह रंग बताता है; विशेष्य “गुलाब” है।', 'गुलाब'),
    ('कक्षा में चालीस विद्यार्थी हैं।', 'चालीस', 'संख्यावाचक विशेषण', 'यह निश्चित संख्या बताता है; विशेष्य “विद्यार्थी” है।', 'विद्यार्थी'),
    ('मुझे दो किलो आटा चाहिए।', 'दो किलो', 'परिमाणवाचक विशेषण', 'यह तौल (मात्रा) बताता है; विशेष्य “आटा” है।', 'आटा'),
    ('यह घड़ी मेरे दादाजी की है।', 'यह', 'सार्वनामिक विशेषण', 'सर्वनाम “यह” संज्ञा “घड़ी” से पहले आकर उसकी ओर संकेत करता है।', 'घड़ी'),
    ('ईमानदार व्यक्ति का सब सम्मान करते हैं।', 'ईमानदार', 'गुणवाचक विशेषण', 'यह गुण बताता है; विशेष्य “व्यक्ति” है।', 'व्यक्ति'),
    ('गिलास में थोड़ा दूध बचा है।', 'थोड़ा', 'परिमाणवाचक विशेषण', 'यह मात्रा बताता है (अनिश्चित परिमाण); विशेष्य “दूध” है।', 'दूध'),
    ('{N} पहली बार हवाई जहाज़ में बैठ{ा}।', 'पहली', 'संख्यावाचक विशेषण', 'यह क्रम बताता है (क्रमवाचक); विशेष्य “बार” है।', 'बार'),
    ('उस बगीचे में आम के पेड़ हैं।', 'उस', 'सार्वनामिक विशेषण', 'सर्वनाम “उस” संज्ञा “बगीचे” की ओर संकेत करता है।', 'बगीचे'),
    ('पुरानी हवेली में अब कोई नहीं रहता।', 'पुरानी', 'गुणवाचक विशेषण', 'यह दशा/काल बताता है; विशेष्य “हवेली” है।', 'हवेली'),
    ('बाज़ार से पाँच मीटर कपड़ा लाओ।', 'पाँच मीटर', 'परिमाणवाचक विशेषण', 'यह नाप बताता है; विशेष्य “कपड़ा” है।', 'कपड़ा'),
    ('{N} ने तीन चित्र बनाए।', 'तीन', 'संख्यावाचक विशेषण', 'यह निश्चित संख्या बताता है; विशेष्य “चित्र” है।', 'चित्र'),
    ('कौन-सी किताब तुम्हें पसंद है?', 'कौन-सी', 'सार्वनामिक विशेषण', 'प्रश्नवाचक सर्वनाम संज्ञा “किताब” से पहले विशेषण की तरह आया है।', 'किताब'),
    ('नीले आसमान में पतंगें उड़ रही थीं।', 'नीले', 'गुणवाचक विशेषण', 'यह रंग बताता है; विशेष्य “आसमान” है।', 'आसमान'),
    ('बर्तन में बहुत पानी है।', 'बहुत', 'परिमाणवाचक विशेषण', 'यह मात्रा बताता है; विशेष्य “पानी” है।', 'पानी'),
    ('कुछ बच्चे मैदान में खेल रहे हैं।', 'कुछ', 'संख्यावाचक विशेषण', 'यह अनिश्चित संख्या बताता है (बच्चे गिने जा सकते हैं); विशेष्य “बच्चे” है।', 'बच्चे'),
    ('{N} एक मेहनती विद्यार्थी है।', 'मेहनती', 'गुणवाचक विशेषण', 'यह गुण बताता है; विशेष्य “विद्यार्थी” है।', 'विद्यार्थी'),
    ('वह लड़का मेरा पड़ोसी है।', 'वह', 'सार्वनामिक विशेषण', 'सर्वनाम “वह” संज्ञा “लड़का” से पहले आकर उसकी ओर संकेत करता है।', 'लड़का'),
    ('थैले में एक लीटर तेल है।', 'एक लीटर', 'परिमाणवाचक विशेषण', 'यह नाप बताता है; विशेष्य “तेल” है।', 'तेल'),
    ('{N} के पास दस रंगीन पेंसिलें हैं।', 'रंगीन', 'गुणवाचक विशेषण', 'यह रूप/गुण बताता है; विशेष्य “पेंसिलें” है।', 'पेंसिलें'),
    ('तीसरी मंज़िल पर हमारा घर है।', 'तीसरी', 'संख्यावाचक विशेषण', 'यह क्रम बताता है; विशेष्य “मंज़िल” है।', 'मंज़िल'),
]
VISH_X = [
    ('दया', 'दयालु', '“आलु” प्रत्यय से गुणवाचक विशेषण।', ['दयाई', 'दयता', 'दयापन']),
    ('धन', 'धनवान', '“वान” प्रत्यय से विशेषण।', ['धनता', 'धनाई', 'धनपन']),
    ('रंग', 'रंगीला', '“ईला” प्रत्यय से विशेषण।', ['रंगता', 'रंगाई', 'रंगपन']),
    ('समाज', 'सामाजिक', '“इक” प्रत्यय लगने पर पहले स्वर में वृद्धि (स → सा) होती है।', ['समाजिक', 'समाजी', 'समाजता']),
    ('भारत', 'भारतीय', '“ईय” प्रत्यय से विशेषण।', ['भारती', 'भारतिक', 'भारतता']),
    ('बुद्धि', 'बुद्धिमान', '“मान” प्रत्यय से विशेषण।', ['बुद्धिता', 'बुद्धिपन', 'बुद्धाई']),
    ('दिन', 'दैनिक', '“इक” प्रत्यय से विशेषण; पहले स्वर में वृद्धि (दि → दै)।', ['दिनिक', 'दिनी', 'दिनता']),
    ('चमक', 'चमकीला', '“ईला” प्रत्यय से विशेषण।', ['चमकता', 'चमकाई', 'चमकपन']),
    ('इतिहास', 'ऐतिहासिक', '“इक” प्रत्यय से विशेषण; पहले स्वर में वृद्धि (इ → ऐ)।', ['इतिहासिक', 'इतिहासी', 'ऐतिहास']),
    ('गुण', 'गुणवान', '“वान” प्रत्यय से विशेषण।', ['गुणता', 'गुणाई', 'गुणपन']),
    ('पहाड़', 'पहाड़ी', '“ई” प्रत्यय से विशेषण।', ['पहाड़ता', 'पहाड़िक', 'पहाड़पन']),
    ('भूख', 'भूखा', '“आ” प्रत्यय से विशेषण।', ['भूखता', 'भूखिक', 'भूखपन']),
]

KAAL_L = ['सामान्य वर्तमान काल', 'अपूर्ण वर्तमान काल', 'सामान्य भूतकाल', 'अपूर्ण भूतकाल', 'पूर्ण भूतकाल', 'सामान्य भविष्यत् काल']
KAAL_DEF = {'सामान्य वर्तमान काल': 'क्रिया का वर्तमान में सामान्य/नियमित रूप से होना (…ता/ती है)।', 'अपूर्ण वर्तमान काल': 'क्रिया का अभी चल रहा होना (…रहा/रही है)।',
            'सामान्य भूतकाल': 'क्रिया का बीते समय में सामान्य रूप से पूरा होना (…आ/ई, गया/गई)।', 'अपूर्ण भूतकाल': 'क्रिया का बीते समय में चल रहा होना (…रहा/रही था/थी)।',
            'पूर्ण भूतकाल': 'क्रिया का बीते समय में बहुत पहले पूरा हो चुका होना (…चुका था, लिया था)।', 'सामान्य भविष्यत् काल': 'क्रिया का आने वाले समय में होना (…गा/गी/गे)।'}
KAAL = [
    ('{N} रोज़ सुबह दूध पीत{ा} है।', '', 'सामान्य वर्तमान काल', 'क्रिया “…ता/ती है” रूप में है और वर्तमान में नियमित रूप से होने वाला काम बताती है।'),
    ('{N} इस समय पत्र लिख रह{ा} है।', '', 'अपूर्ण वर्तमान काल', '“रहा/रही है” से पता चलता है कि काम अभी चल रहा है।'),
    ('{N} कल शाम बाज़ार ग{या}।', '', 'सामान्य भूतकाल', 'काम बीते समय में हुआ; क्रिया “गया/गई” सामान्य भूत का रूप है।'),
    ('{N} उस समय खाना बना रह{ा} थ{ा}।', '', 'अपूर्ण भूतकाल', '“रहा/रही था/थी” से पता चलता है कि काम बीते समय में चल रहा था।'),
    ('{N} ने गृहकार्य पहले ही पूरा कर लिया था।', '', 'पूर्ण भूतकाल', '“कर लिया था” से पता चलता है कि काम बीते समय में पहले ही पूरा हो चुका था।'),
    ('{N} अगले सप्ताह मुंबई जाएग{ा}।', '', 'सामान्य भविष्यत् काल', '“जाएगा/जाएगी” से पता चलता है कि काम आने वाले समय में होगा।'),
    ('बच्चे मैदान में फुटबॉल खेल रहे हैं।', '', 'अपूर्ण वर्तमान काल', '“खेल रहे हैं” — काम अभी जारी है।'),
    ('हम हर रविवार दादी से मिलने जाते हैं।', '', 'सामान्य वर्तमान काल', '“जाते हैं” — वर्तमान में नियमित रूप से होने वाला काम।'),
    ('पिछली गर्मियों में हमने पहाड़ों की यात्रा की।', '', 'सामान्य भूतकाल', '“यात्रा की” — बीते समय में पूरा हुआ काम।'),
    ('गाड़ी प्लेटफ़ॉर्म से पहले ही जा चुकी थी।', '', 'पूर्ण भूतकाल', '“जा चुकी थी” — काम बीते समय में पूरा हो चुका था।'),
    ('कल सुबह तेज़ बारिश हो रही थी।', '', 'अपूर्ण भूतकाल', '“हो रही थी” — बीते समय में जारी काम।'),
    ('परीक्षा का परिणाम अगले महीने घोषित होगा।', '', 'सामान्य भविष्यत् काल', '“घोषित होगा” — आने वाले समय की क्रिया।'),
    ('{N} रोज़ शाम को पौधों को पानी देत{ा} है।', '', 'सामान्य वर्तमान काल', '“देता/देती है” — नियमित रूप से होने वाला काम।'),
    ('माँ रसोई में चाय बना रही हैं।', '', 'अपूर्ण वर्तमान काल', '“बना रही हैं” — काम अभी चल रहा है।'),
    ('{N} ने पिछले वर्ष तैरना सीखा।', '', 'सामान्य भूतकाल', '“सीखा” — बीते समय में हुआ काम।'),
    ('हम लोग रविवार को पिकनिक पर जाएँगे।', '', 'सामान्य भविष्यत् काल', '“जाएँगे” — आने वाले समय का काम।'),
    ('दादाजी बरामदे में अख़बार पढ़ रहे थे।', '', 'अपूर्ण भूतकाल', '“पढ़ रहे थे” — बीते समय में जारी काम।'),
    ('{N} ने चिट्ठी पहले ही भेज दी थी।', '', 'पूर्ण भूतकाल', '“भेज दी थी” — काम बीते समय में पूरा हो चुका था।'),
]
KAAL_X = [
    ('{N} पत्र लिखत{ा} है। (सामान्य भूतकाल में)', '{N} ने पत्र लिखा।', 'सकर्मक क्रिया के सामान्य भूतकाल में कर्ता के साथ “ने” आता है और क्रिया कर्म “पत्र” (पुल्लिंग) के अनुसार होती है।',
     ['{N} ने पत्र लिखी।', '{N} पत्र लिखा।', '{N} पत्र लिखेग{ा}।']),
    ('{N} बाज़ार जात{ा} है। (सामान्य भविष्यत् काल में)', '{N} बाज़ार जाएग{ा}।', 'भविष्यत् काल में क्रिया के अंत में “गा/गी” लगता है; अकर्मक क्रिया कर्ता के लिंग के अनुसार बदलती है।',
     ['{N} बाज़ार ग{या}।', '{N} बाज़ार जा रह{ा} है।', '{N} ने बाज़ार जाएग{ा}।']),
    ('{N} गीत गाएग{ा}। (सामान्य भूतकाल में)', '{N} ने गीत गाया।', 'सकर्मक क्रिया “गाना” के भूतकाल में “ने” लगता है; क्रिया कर्म “गीत” (पुल्लिंग) के अनुसार “गाया” होती है।',
     ['{N} गीत गाया।', '{N} ने गीत गाई।', '{N} गीत गात{ा} थ{ा}।']),
    ('{N} चाय पीत{ा} है। (सामान्य भूतकाल में)', '{N} ने चाय पी।', '“चाय” स्त्रीलिंग है, इसलिए “ने” के साथ क्रिया “पी” (स्त्रीलिंग) होती है।',
     ['{N} ने चाय पिया।', '{N} चाय पिएग{ा}।', '{N} ने चाय पीया।']),
    ('{N} स्कूल ग{या}। (सामान्य वर्तमान काल में)', '{N} स्कूल जात{ा} है।', 'सामान्य वर्तमान में क्रिया “…ता/ती है” रूप में आती है।',
     ['{N} स्कूल जाएग{ा}।', '{N} ने स्कूल जात{ा} है।', '{N} स्कूल जा चुक{ा} है।']),
    ('{N} कहानी सुनात{ा} है। (अपूर्ण भूतकाल में)', '{N} कहानी सुना रह{ा} थ{ा}।', 'अपूर्ण भूत में “रहा/रही था/थी” लगता है; इसमें “ने” नहीं लगता।',
     ['{N} ने कहानी सुना रह{ा} थ{ा}।', '{N} ने कहानी सुनाई।', '{N} कहानी सुना रह{ा} है।']),
    ('{N} ने रोटी खाई। (सामान्य भविष्यत् काल में)', '{N} रोटी खाएग{ा}।', 'भविष्यत् काल में “ने” नहीं लगता; क्रिया कर्ता के लिंग-वचन के अनुसार होती है।',
     ['{N} ने रोटी खाएग{ा}।', '{N} रोटी खा रह{ा} है।', '{N} रोटी खाई।']),
    ('{N} नदी में तैरत{ा} है। (अपूर्ण वर्तमान काल में)', '{N} नदी में तैर रह{ा} है।', 'चल रहे काम के लिए “रहा/रही है” का प्रयोग होता है।',
     ['{N} नदी में तैरेग{ा}।', '{N} नदी में तैर{ा}।', '{N} ने नदी में तैर रह{ा} है।']),
    ('{N} किताबें पढ़त{ा} है। (सामान्य भूतकाल में)', '{N} ने किताबें पढ़ीं।', '“किताबें” स्त्रीलिंग बहुवचन है; “ने” के साथ क्रिया “पढ़ीं” होती है।',
     ['{N} ने किताबें पढ़ा।', '{N} किताबें पढ़ा।', '{N} ने किताबें पढ़े।']),
    ('{N} दोस्तों से मिलत{ा} है। (सामान्य भूतकाल में)', '{N} दोस्तों से मिल{ा}।', '“मिलना” (से) के साथ “ने” नहीं लगता; क्रिया कर्ता के लिंग के अनुसार होती है।',
     ['{N} ने दोस्तों से मिला।', '{N} ने दोस्तों को मिला।', '{N} दोस्तों से मिलेग{ा}।']),
    ('{N} कपड़े धोत{ा} है। (सामान्य भूतकाल में)', '{N} ने कपड़े धोए।', '“कपड़े” पुल्लिंग बहुवचन है, इसलिए “ने” के साथ “धोए”।',
     ['{N} ने कपड़े धोया।', '{N} कपड़े धोए।', '{N} ने कपड़े धोई।']),
    ('{N} घर लौटत{ा} है। (सामान्य भविष्यत् काल में)', '{N} घर लौटेग{ा}।', 'भविष्यत् काल: “…एगा/एगी”; “ने” नहीं लगता।',
     ['{N} घर लौट{ा}।', '{N} ने घर लौटेग{ा}।', '{N} घर लौट रह{ा} है।']),
    ('{N} चित्र बना रह{ा} है। (पूर्ण भूतकाल में)', '{N} ने चित्र बना लिया था।', 'पूर्ण भूत में काम बीते समय में पूरा हो चुका होता है (“लिया था”); “ने” के साथ क्रिया कर्म “चित्र” (पुल्लिंग) के अनुसार।',
     ['{N} चित्र बना रह{ा} थ{ा}।', '{N} ने चित्र बनाएग{ा}।', '{N} ने चित्र बना ली थी।']),
    ('बच्चे पार्क में खेलते हैं। (अपूर्ण भूतकाल में)', 'बच्चे पार्क में खेल रहे थे।', 'अपूर्ण भूत: “रहे थे” (पुल्लिंग बहुवचन); “ने” नहीं लगता।',
     ['बच्चों ने पार्क में खेल रहे थे।', 'बच्चे पार्क में खेलेंगे।', 'बच्चे पार्क में खेल रहे हैं।']),
]
KRIYA = [
    ('{N} पुस्तक पढ़त{ा} है।', 'पढ़ता/पढ़ती है', 'सकर्मक क्रिया', '“क्या पढ़ता है?” पूछने पर उत्तर “पुस्तक” मिलता है — कर्म है।'),
    ('बच्चा सो रहा है।', 'सो रहा है', 'अकर्मक क्रिया', 'क्रिया का फल कर्ता पर ही पड़ता है; कोई कर्म नहीं है।'),
    ('{N} ज़ोर से हँस{ा}।', 'हँसा/हँसी', 'अकर्मक क्रिया', 'इसमें कोई कर्म नहीं है।'),
    ('माँ ने स्वादिष्ट खाना बनाया।', 'बनाया', 'सकर्मक क्रिया', '“क्या बनाया?” — खाना (कर्म)।'),
    ('पक्षी आकाश में उड़ रहे हैं।', 'उड़ रहे हैं', 'अकर्मक क्रिया', 'कोई कर्म नहीं; “आकाश में” स्थान बताता है।'),
    ('दादी ने एक कहानी सुनाई।', 'सुनाई', 'सकर्मक क्रिया', '“क्या सुनाई?” — कहानी (कर्म)।'),
    ('घोड़ा तेज़ दौड़ता है।', 'दौड़ता है', 'अकर्मक क्रिया', 'कोई कर्म नहीं है।'),
    ('{N} ने गेंद दूर फेंकी।', 'फेंकी', 'सकर्मक क्रिया', '“क्या फेंकी?” — गेंद (कर्म)।'),
    ('बगीचे में फूल खिले हैं।', 'खिले हैं', 'अकर्मक क्रिया', 'कोई कर्म नहीं है।'),
    ('{N} ने अपने मित्र को पत्र लिखा।', 'लिखा', 'सकर्मक क्रिया', '“क्या लिखा?” — पत्र (कर्म)।'),
]

VACH_L = ['कर्तृवाच्य', 'कर्मवाच्य', 'भाववाच्य']
VACH_DEF = {'कर्तृवाच्य': 'क्रिया कर्ता के अनुसार हो और कर्ता प्रधान हो।', 'कर्मवाच्य': 'क्रिया कर्म के अनुसार हो; कर्ता के साथ “द्वारा/से” लगे (सकर्मक क्रिया)।',
            'भाववाच्य': 'क्रिया का भाव प्रधान हो; अकर्मक क्रिया, कर्ता के साथ “से”, क्रिया सदा पुल्लिंग एकवचन अन्य पुरुष (प्रायः निषेध/असमर्थता में)।'}
VACH = [
    ('{N} मधुर गीत गात{ा} है।', '', 'कर्तृवाच्य', 'कर्ता प्रधान है और क्रिया “गाता/गाती है” कर्ता के अनुसार है।'),
    ('पत्र डाकिए द्वारा लाया गया।', '', 'कर्मवाच्य', 'कर्ता के साथ “द्वारा” है और क्रिया कर्म “पत्र” के अनुसार है।'),
    ('मुझसे अब और बैठा नहीं जाता।', '', 'भाववाच्य', 'अकर्मक क्रिया “बैठना”, कर्ता के साथ “से” और क्रिया पुल्लिंग एकवचन — भाव प्रधान है।'),
    ('रोगी से उठा नहीं जाता।', '', 'भाववाच्य', 'अकर्मक क्रिया “उठना” भाववाच्य में; कर्ता के साथ “से”।'),
    ('शिक्षक द्वारा प्रश्न समझाया गया।', '', 'कर्मवाच्य', 'कर्ता के साथ “द्वारा”; क्रिया कर्म “प्रश्न” के अनुसार।'),
    ('किसानों ने खेत जोते।', '', 'कर्तृवाच्य', 'कर्ता “किसानों” प्रधान है; वाक्य कर्ता के माध्यम से कहा गया है।'),
    ('प्रदर्शनी का उद्घाटन मंत्री द्वारा किया जाएगा।', '', 'कर्मवाच्य', 'कर्ता “मंत्री” के साथ “द्वारा”; क्रिया कर्म “उद्घाटन” के अनुसार।'),
    ('आओ, अब चला जाए।', '', 'भाववाच्य', 'अकर्मक क्रिया “चलना” का भाव प्रधान है; क्रिया पुल्लिंग एकवचन।'),
    ('बच्चे मैदान में दौड़ रहे हैं।', '', 'कर्तृवाच्य', 'कर्ता “बच्चे” प्रधान; क्रिया कर्ता के अनुसार।'),
    ('घायल पक्षी से उड़ा नहीं गया।', '', 'भाववाच्य', 'अकर्मक क्रिया “उड़ना”; कर्ता के साथ “से”; भाव प्रधान।'),
    ('नई सड़क नगर निगम द्वारा बनवाई गई।', '', 'कर्मवाच्य', 'कर्ता के साथ “द्वारा”; क्रिया कर्म “सड़क” (स्त्रीलिंग) के अनुसार “बनवाई गई”।'),
    ('{N} ने निबंध प्रतियोगिता जीती।', '', 'कर्तृवाच्य', 'कर्ता प्रधान है; वाक्य कर्ता के माध्यम से कहा गया है।'),
]
VACH_X = [
    ('{N} पत्र लिखत{ा} है। (कर्मवाच्य में)', '{N} द्वारा पत्र लिखा जाता है।', 'कर्मवाच्य में कर्ता के साथ “द्वारा” लगता है और क्रिया कर्म “पत्र” (पुल्लिंग) के अनुसार “लिखा जाता है” बनती है।',
     ['{N} पत्र लिखा जाता है।', '{N} द्वारा पत्र लिखत{ा} है।', '{N} द्वारा पत्र लिखी जाती है।']),
    ('माँ ने खाना बनाया। (कर्मवाच्य में)', 'माँ द्वारा खाना बनाया गया।', '“ने” हटाकर “द्वारा” लगता है; क्रिया “बनाया गया” कर्म “खाना” के अनुसार।',
     ['माँ ने खाना बनाया गया।', 'माँ द्वारा खाना बनाई गई।', 'माँ द्वारा खाना बनाती है।']),
    ('प्रधानाचार्य ने पुरस्कार बाँटे। (कर्मवाच्य में)', 'प्रधानाचार्य द्वारा पुरस्कार बाँटे गए।', 'कर्म “पुरस्कार” पुल्लिंग बहुवचन है, इसलिए “बाँटे गए”।',
     ['प्रधानाचार्य द्वारा पुरस्कार बाँटा गया।', 'प्रधानाचार्य ने पुरस्कार बाँटे गए।', 'प्रधानाचार्य द्वारा पुरस्कार बाँटी गईं।']),
    ('{N} ने कविता सुनाई। (कर्मवाच्य में)', '{N} द्वारा कविता सुनाई गई।', '“कविता” स्त्रीलिंग है, इसलिए “सुनाई गई”।',
     ['{N} द्वारा कविता सुनाया गया।', '{N} ने कविता सुनाई गई।', '{N} कविता सुनाई जाती है।']),
    ('मैं इस गर्मी में चल नहीं सकता। (भाववाच्य में)', 'मुझसे इस गर्मी में चला नहीं जाता।', 'भाववाच्य में अकर्मक क्रिया, कर्ता के साथ “से” और क्रिया सदा पुल्लिंग एकवचन (“चला नहीं जाता”)।',
     ['मुझसे इस गर्मी में चली नहीं जाती।', 'मैं इस गर्मी में चला नहीं जाता।', 'मुझसे इस गर्मी में चलता नहीं है।']),
    ('बच्चे रात भर सो नहीं सके। (भाववाच्य में)', 'बच्चों से रात भर सोया नहीं गया।', 'कर्ता “बच्चों” के साथ “से”; क्रिया “सोया नहीं गया” पुल्लिंग एकवचन।',
     ['बच्चों से रात भर सोए नहीं गए।', 'बच्चे रात भर सोया नहीं गया।', 'बच्चों द्वारा रात भर सो नहीं सके।']),
    ('{N} हँस नहीं सकत{ा}। (भाववाच्य में)', '{N} से हँसा नहीं जाता।', 'भाववाच्य में कर्ता के साथ “से” और क्रिया पुल्लिंग एकवचन, चाहे कर्ता स्त्रीलिंग हो या पुल्लिंग।',
     ['{N} से हँसी नहीं जाती।', '{N} हँसा नहीं जाता।', '{N} द्वारा हँस नहीं सकत{ा}।']),
    ('दादाजी द्वारा अख़बार पढ़ा जाता है। (कर्तृवाच्य में)', 'दादाजी अख़बार पढ़ते हैं।', 'कर्तृवाच्य में “द्वारा” हटता है और क्रिया कर्ता (आदरसूचक बहुवचन) के अनुसार होती है।',
     ['दादाजी अख़बार पढ़ा जाता है।', 'दादाजी द्वारा अख़बार पढ़ते हैं।', 'दादाजी ने अख़बार पढ़ा जाता है।']),
    ('पुलिस द्वारा चोर पकड़ा गया। (कर्तृवाच्य में)', 'पुलिस ने चोर को पकड़ा।', 'कर्तृवाच्य (भूतकाल, सकर्मक) में कर्ता के साथ “ने” लगता है।',
     ['पुलिस ने चोर पकड़ा गया।', 'पुलिस चोर को पकड़ा गया।', 'पुलिस द्वारा चोर को पकड़ी।']),
    ('हम अब दौड़ नहीं सकते। (भाववाच्य में)', 'हमसे अब दौड़ा नहीं जाता।', 'कर्ता “हम” → “हमसे”; क्रिया पुल्लिंग एकवचन “दौड़ा नहीं जाता”।',
     ['हमसे अब दौड़े नहीं जाते।', 'हम अब दौड़ा नहीं जाता।', 'हमारे द्वारा अब दौड़ नहीं सकते।']),
    ('वैज्ञानिकों ने नया टीका विकसित किया। (कर्मवाच्य में)', 'वैज्ञानिकों द्वारा नया टीका विकसित किया गया।', 'कर्म “टीका” पुल्लिंग एकवचन है, इसलिए “किया गया”।',
     ['वैज्ञानिकों ने नया टीका विकसित किया गया।', 'वैज्ञानिकों द्वारा नया टीका विकसित करते हैं।', 'वैज्ञानिकों द्वारा नई टीका विकसित की गई।']),
]

RACH_L = ['सरल वाक्य', 'संयुक्त वाक्य', 'मिश्र वाक्य']
RACH_DEF = {'सरल वाक्य': 'जिसमें एक ही उद्देश्य और एक ही मुख्य विधेय (मुख्य क्रिया) हो।', 'संयुक्त वाक्य': 'जिसमें दो या अधिक स्वतंत्र उपवाक्य समानाधिकरण योजक (और, पर, इसलिए, या) से जुड़े हों।',
            'मिश्र वाक्य': 'जिसमें एक प्रधान उपवाक्य और एक या अधिक आश्रित उपवाक्य (कि, जो, जब…तब, यदि…तो, क्योंकि) हों।'}
RACH = [
    ('{N} रोज़ सुबह योग करत{ा} है।', '', 'सरल वाक्य', 'एक ही उद्देश्य और एक ही मुख्य क्रिया है।'),
    ('बारिश रुकी और बच्चे बाहर खेलने निकल पड़े।', '', 'संयुक्त वाक्य', 'दो स्वतंत्र उपवाक्य “और” से जुड़े हैं।'),
    ('जब बारिश रुकी, तब बच्चे बाहर खेलने निकले।', '', 'मिश्र वाक्य', '“जब बारिश रुकी” आश्रित उपवाक्य है जो प्रधान उपवाक्य पर निर्भर है (जब…तब)।'),
    ('{N} ने बहुत मेहनत की, इसलिए परीक्षा में प्रथम स्थान मिला।', '', 'संयुक्त वाक्य', 'दो स्वतंत्र उपवाक्य “इसलिए” (समानाधिकरण योजक) से जुड़े हैं।'),
    ('मुझे विश्वास है कि हमारी टीम जीतेगी।', '', 'मिश्र वाक्य', '“कि हमारी टीम जीतेगी” आश्रित संज्ञा उपवाक्य है।'),
    ('वह लड़का, जो कल आया था, मेरा चचेरा भाई है।', '', 'मिश्र वाक्य', '“जो कल आया था” आश्रित विशेषण उपवाक्य है।'),
    ('माँ बाज़ार गईं, पर दुकानें बंद थीं।', '', 'संयुक्त वाक्य', 'दो स्वतंत्र उपवाक्य “पर” से जुड़े हैं।'),
    ('सूरज निकलते ही पक्षी चहचहाने लगे।', '', 'सरल वाक्य', 'केवल एक मुख्य क्रिया (चहचहाने लगे) है; “निकलते ही” अलग उपवाक्य नहीं है।'),
    ('यदि तुम समय पर आते, तो बस न छूटती।', '', 'मिश्र वाक्य', '“यदि तुम समय पर आते” आश्रित उपवाक्य है (यदि…तो)।'),
    ('{N} ने खाना खाया और सो ग{या}।', '', 'संयुक्त वाक्य', 'दो स्वतंत्र उपवाक्य (खाना खाया, सो गया) “और” से जुड़े हैं।'),
    ('मेरे दादाजी हर शाम पार्क में टहलते हैं।', '', 'सरल वाक्य', 'एक उद्देश्य और एक विधेय।'),
    ('क्योंकि सड़क पर पानी भरा था, इसलिए विद्यालय बंद रहा।', '', 'मिश्र वाक्य', '“क्योंकि…” कारण बताने वाला आश्रित उपवाक्य है।'),
    ('परिश्रमी विद्यार्थी सदा सफल होते हैं।', '', 'सरल वाक्य', 'एक ही उद्देश्य (परिश्रमी विद्यार्थी) और एक ही विधेय है।'),
    ('तुम पढ़ाई करो या घर के काम में हाथ बँटाओ।', '', 'संयुक्त वाक्य', 'दो स्वतंत्र उपवाक्य “या” से जुड़े हैं।'),
]
RACH_X = [
    ('{N} बीमार थ{ा}। {N} विद्यालय नहीं ग{या}। (संयुक्त वाक्य बनाइए)', '{N} बीमार थ{ा}, इसलिए विद्यालय नहीं ग{या}।', 'दो स्वतंत्र उपवाक्यों को समानाधिकरण योजक “इसलिए” से जोड़ा गया।',
     ['क्योंकि {N} बीमार थ{ा}, इसलिए विद्यालय नहीं ग{या}।', 'बीमार होने के कारण {N} विद्यालय नहीं ग{या}।', 'जो बीमार थ{ा} वह {N} विद्यालय नहीं ग{या}।']),
    ('{N} बीमार थ{ा}। {N} विद्यालय नहीं ग{या}। (मिश्र वाक्य बनाइए)', 'क्योंकि {N} बीमार थ{ा}, इसलिए विद्यालय नहीं ग{या}।', '“क्योंकि” से आश्रित उपवाक्य बनाया गया।',
     ['{N} बीमार थ{ा}, इसलिए विद्यालय नहीं ग{या}।', 'बीमार होने के कारण {N} विद्यालय नहीं ग{या}।', '{N} बीमार थ{ा} और विद्यालय नहीं ग{या}।']),
    ('घंटी बजी। सब विद्यार्थी कक्षा में चले गए। (मिश्र वाक्य बनाइए)', 'जैसे ही घंटी बजी, वैसे ही सब विद्यार्थी कक्षा में चले गए।', '“जैसे ही…वैसे ही” से कालवाचक आश्रित उपवाक्य बना।',
     ['घंटी बजी और सब विद्यार्थी कक्षा में चले गए।', 'घंटी बजते ही सब विद्यार्थी कक्षा में चले गए।', 'घंटी बजी, पर सब विद्यार्थी कक्षा में चले गए।']),
    ('घंटी बजी। सब विद्यार्थी कक्षा में चले गए। (सरल वाक्य बनाइए)', 'घंटी बजते ही सब विद्यार्थी कक्षा में चले गए।', 'एक क्रिया को “बजते ही” (कृदंत) बनाकर एक ही मुख्य क्रिया रखी गई।',
     ['घंटी बजी और सब विद्यार्थी कक्षा में चले गए।', 'जैसे ही घंटी बजी, वैसे ही सब विद्यार्थी कक्षा में चले गए।', 'घंटी बजी, इसलिए सब विद्यार्थी कक्षा में चले गए।']),
    ('मेहनत करो। सफलता मिलेगी। (मिश्र वाक्य बनाइए)', 'यदि तुम मेहनत करोगे, तो सफलता मिलेगी।', '“यदि…तो” से शर्त बताने वाला आश्रित उपवाक्य बना।',
     ['मेहनत करो और सफलता मिलेगी।', 'मेहनत करने से सफलता मिलेगी।', 'मेहनत करो, पर सफलता मिलेगी।']),
    ('मेहनत करो। सफलता मिलेगी। (सरल वाक्य बनाइए)', 'मेहनत करने से सफलता मिलेगी।', 'दो क्रियाओं के स्थान पर एक मुख्य क्रिया; “मेहनत करने से” पदबंध है।',
     ['यदि तुम मेहनत करोगे, तो सफलता मिलेगी।', 'मेहनत करो और सफलता मिलेगी।', 'मेहनत करो, इसलिए सफलता मिलेगी।']),
    ('उसने एक लड़की देखी। लड़की गा रही थी। (मिश्र वाक्य बनाइए)', 'उसने एक लड़की देखी जो गा रही थी।', '“जो” से विशेषण उपवाक्य बना।',
     ['उसने एक गाती हुई लड़की देखी।', 'उसने एक लड़की देखी और वह गा रही थी।', 'उसने एक लड़की देखी, इसलिए गा रही थी।']),
    ('उसने एक लड़की देखी। लड़की गा रही थी। (सरल वाक्य बनाइए)', 'उसने एक गाती हुई लड़की देखी।', 'उपवाक्य को “गाती हुई” विशेषण-पदबंध बनाकर एक ही मुख्य क्रिया रखी गई।',
     ['उसने एक लड़की देखी जो गा रही थी।', 'उसने एक लड़की देखी और वह गा रही थी।', 'जब उसने लड़की देखी तब वह गा रही थी।']),
]
ARTH_L = ['विधानवाचक वाक्य', 'निषेधवाचक वाक्य', 'प्रश्नवाचक वाक्य', 'आज्ञावाचक वाक्य', 'इच्छावाचक वाक्य', 'संदेहवाचक वाक्य', 'संकेतवाचक वाक्य', 'विस्मयादिबोधक वाक्य']
ARTH = [
    ('{N} कल दिल्ली जाएग{ा}।', '', 'विधानवाचक वाक्य', 'इसमें किसी बात का सामान्य कथन है।'),
    ('आज बारिश नहीं होगी।', '', 'निषेधवाचक वाक्य', '“नहीं” से कार्य के न होने का बोध होता है।'),
    ('क्या तुमने गृहकार्य पूरा कर लिया?', '', 'प्रश्नवाचक वाक्य', 'इसमें प्रश्न पूछा गया है।'),
    ('कृपया दरवाज़ा बंद कर दीजिए।', '', 'आज्ञावाचक वाक्य', 'इसमें अनुरोध/आज्ञा दी गई है।'),
    ('भगवान तुम्हें लंबी उम्र दे!', '', 'इच्छावाचक वाक्य', 'इसमें शुभकामना/इच्छा प्रकट हुई है।'),
    ('शायद {N} आज विद्यालय न आए।', '', 'संदेहवाचक वाक्य', '“शायद” से संदेह प्रकट होता है।'),
    ('यदि तुम मेहनत करोगे तो अवश्य सफल होगे।', '', 'संकेतवाचक वाक्य', 'एक बात दूसरी बात पर निर्भर है (शर्त — यदि…तो)।'),
    ('वाह! कितना सुंदर दृश्य है!', '', 'विस्मयादिबोधक वाक्य', '“वाह!” से आश्चर्य/हर्ष का भाव प्रकट होता है।'),
    ('{N} ने अपना वादा कभी नहीं तोड़ा।', '', 'निषेधवाचक वाक्य', '“नहीं” से निषेध का बोध होता है।'),
    ('तुम्हारी यात्रा मंगलमय हो।', '', 'इच्छावाचक वाक्य', 'इसमें शुभकामना है।'),
    ('अरे! इतनी बड़ी पतंग!', '', 'विस्मयादिबोधक वाक्य', '“अरे!” से आश्चर्य प्रकट होता है।'),
    ('हो सकता है कि कल छुट्टी हो।', '', 'संदेहवाचक वाक्य', '“हो सकता है” से संभावना/संदेह प्रकट होता है।'),
    ('अगर समय पर बारिश होती, तो फसल अच्छी होती।', '', 'संकेतवाचक वाक्य', 'एक क्रिया का होना दूसरी पर निर्भर है।'),
    ('जल्दी से तैयार हो जाओ।', '', 'आज्ञावाचक वाक्य', 'इसमें आदेश दिया गया है।'),
    ('तुम्हारा घर किस शहर में है?', '', 'प्रश्नवाचक वाक्य', 'इसमें प्रश्न पूछा गया है।'),
    ('सूरज पूर्व दिशा में उगता है।', '', 'विधानवाचक वाक्य', 'यह एक सामान्य कथन है।'),
]

ALANK_L = ['अनुप्रास अलंकार', 'उपमा अलंकार', 'मानवीकरण अलंकार', 'रूपक अलंकार']
ALANK_DEF = {'अनुप्रास अलंकार': 'जहाँ एक ही वर्ण की बार-बार आवृत्ति से चमत्कार उत्पन्न हो।',
             'उपमा अलंकार': 'जहाँ एक वस्तु की तुलना किसी दूसरी प्रसिद्ध वस्तु से “सा, सी, से, सम, समान, जैसा” आदि वाचक शब्दों द्वारा की जाए।',
             'मानवीकरण अलंकार': 'जहाँ प्रकृति या निर्जीव वस्तुओं पर मनुष्य जैसी भावनाओं और क्रियाओं का आरोप हो।',
             'रूपक अलंकार': 'जहाँ उपमेय और उपमान में भेद न रहे, उपमेय पर उपमान का अभेद आरोप हो (जैसे “जीवन-नैया”)।'}
ALANK = [
    ('काली-काली कोयल कूके, कुंज-कुंज में कलरव छाया।', '', 'अनुप्रास अलंकार', '“क” वर्ण की बार-बार आवृत्ति से संगीतात्मकता उत्पन्न हुई है।'),
    ('सुंदर सुमन सजे सब ओर, सुरभित सुखद सुहानी भोर।', '', 'अनुप्रास अलंकार', '“स” वर्ण की आवृत्ति है।'),
    ('घिर-घिर घोर घटाएँ आईं, गगन घने घन से भर आया।', '', 'अनुप्रास अलंकार', '“घ” और “ग” वर्णों की आवृत्ति है।'),
    ('मंद-मंद मीठी मलय-मारुत मन को भाती।', '', 'अनुप्रास अलंकार', '“म” वर्ण की आवृत्ति है।'),
    ('माँ का आँचल बादल-सा शीतल है।', '', 'उपमा अलंकार', 'आँचल की तुलना बादल से “सा” वाचक शब्द द्वारा की गई है।'),
    ('उसका मुख चाँद के समान उजला है।', '', 'उपमा अलंकार', 'मुख की तुलना चाँद से “के समान” द्वारा की गई है।'),
    ('झील का पानी दर्पण जैसा साफ़ था।', '', 'उपमा अलंकार', 'पानी की तुलना दर्पण से “जैसा” द्वारा की गई है।'),
    ('बच्चे की हँसी फूलों-सी कोमल थी।', '', 'उपमा अलंकार', 'हँसी की तुलना फूलों से “सी” द्वारा की गई है।'),
    ('नदी की धारा चाँदी की रेखा-सी चमकती है।', '', 'उपमा अलंकार', 'धारा की तुलना चाँदी की रेखा से “सी” द्वारा की गई है।'),
    ('हवा ने खिड़की पर दस्तक दी और चुपके से कुछ कह गई।', '', 'मानवीकरण अलंकार', 'हवा पर दस्तक देने और कहने जैसी मानवीय क्रियाओं का आरोप है।'),
    ('पहाड़ सिर उठाए चुपचाप पहरा दे रहे थे।', '', 'मानवीकरण अलंकार', 'पहाड़ों पर पहरेदार जैसी मानवीय क्रिया का आरोप है।'),
    ('नदी मुस्कुराती हुई मैदानों की ओर दौड़ पड़ी।', '', 'मानवीकरण अलंकार', 'नदी पर मुस्कुराने जैसी मानवीय क्रिया का आरोप है।'),
    ('सूरज ने अलसाई आँखें खोलीं और धरती को जगाया।', '', 'मानवीकरण अलंकार', 'सूरज पर आँखें खोलने और जगाने जैसी मानवीय क्रियाओं का आरोप है।'),
    ('पेड़ हाथ हिलाकर राहगीरों को बुला रहे थे।', '', 'मानवीकरण अलंकार', 'पेड़ों पर बुलाने जैसी मानवीय क्रिया का आरोप है।'),
    ('जीवन-नैया पार लगेगी, साहस की पतवार चलाओ।', '', 'रूपक अलंकार', 'जीवन को ही नैया और साहस को ही पतवार मान लिया गया है (अभेद आरोप)।'),
    ('ज्ञान-दीप से मन का अँधियारा दूर करो।', '', 'रूपक अलंकार', 'ज्ञान को ही दीपक मान लिया गया है।'),
]

SANDHI_L = ['दीर्घ संधि', 'गुण संधि', 'वृद्धि संधि', 'यण संधि', 'अयादि संधि']
SANDHI = [
    ('विद्यालय', 'विद्या + आलय', 'दीर्घ संधि', 'आ + आ = आ', ['विद्य + आलय', 'विद्या + लय', 'विद्या + अलय']),
    ('हिमालय', 'हिम + आलय', 'दीर्घ संधि', 'अ + आ = आ', ['हिमा + लय', 'हिमा + आलय', 'हिम + अलय']),
    ('रवींद्र', 'रवि + इंद्र', 'दीर्घ संधि', 'इ + इ = ई', ['रवी + इंद्र', 'रव + इंद्र', 'रवि + ईंद्र']),
    ('गिरीश', 'गिरि + ईश', 'दीर्घ संधि', 'इ + ई = ई', ['गिरी + ईश', 'गिर + ईश', 'गिरि + इश']),
    ('भानूदय', 'भानु + उदय', 'दीर्घ संधि', 'उ + उ = ऊ', ['भानू + उदय', 'भान + उदय', 'भानु + ऊदय']),
    ('परमार्थ', 'परम + अर्थ', 'दीर्घ संधि', 'अ + अ = आ', ['परमा + अर्थ', 'परम + आर्थ', 'पर + मार्थ']),
    ('पुस्तकालय', 'पुस्तक + आलय', 'दीर्घ संधि', 'अ + आ = आ', ['पुस्तका + लय', 'पुस्तक + अलय', 'पुस्तका + आलय']),
    ('गुरूपदेश', 'गुरु + उपदेश', 'दीर्घ संधि', 'उ + उ = ऊ', ['गुरू + उपदेश', 'गुरु + ऊपदेश', 'गुर + उपदेश']),
    ('देवेंद्र', 'देव + इंद्र', 'गुण संधि', 'अ + इ = ए', ['देवे + इंद्र', 'देव + एंद्र', 'देवी + इंद्र']),
    ('महोत्सव', 'महा + उत्सव', 'गुण संधि', 'आ + उ = ओ', ['महो + उत्सव', 'महा + ओत्सव', 'मह + उत्सव']),
    ('नरेश', 'नर + ईश', 'गुण संधि', 'अ + ई = ए', ['नरे + ईश', 'नर + एश', 'न + रेश']),
    ('परोपकार', 'पर + उपकार', 'गुण संधि', 'अ + उ = ओ', ['परो + उपकार', 'पर + ओपकार', 'परो + पकार']),
    ('सूर्योदय', 'सूर्य + उदय', 'गुण संधि', 'अ + उ = ओ', ['सूर्यो + उदय', 'सूर्य + ओदय', 'सूर + योदय']),
    ('महर्षि', 'महा + ऋषि', 'गुण संधि', 'आ + ऋ = अर्', ['मह + ऋषि', 'महर + षि', 'महा + अर्षि']),
    ('गणेश', 'गण + ईश', 'गुण संधि', 'अ + ई = ए', ['गणे + ईश', 'गण + एश', 'ग + णेश']),
    ('सदैव', 'सदा + एव', 'वृद्धि संधि', 'आ + ए = ऐ', ['सदै + एव', 'सद + एव', 'सदा + ऐव']),
    ('एकैक', 'एक + एक', 'वृद्धि संधि', 'अ + ए = ऐ', ['एकै + एक', 'एक + ऐक', 'ए + कैक']),
    ('मतैक्य', 'मत + ऐक्य', 'वृद्धि संधि', 'अ + ऐ = ऐ', ['मतै + क्य', 'मत + एक्य', 'मतै + ऐक्य']),
    ('वनौषधि', 'वन + औषधि', 'वृद्धि संधि', 'अ + औ = औ', ['वनौ + षधि', 'वन + ओषधि', 'वनौ + औषधि']),
    ('महौषधि', 'महा + औषधि', 'वृद्धि संधि', 'आ + औ = औ', ['महौ + षधि', 'मह + औषधि', 'महा + ओषधि']),
    ('जलौघ', 'जल + ओघ', 'वृद्धि संधि', 'अ + ओ = औ', ['जलौ + घ', 'जल + औघ', 'जलो + ओघ']),
    ('इत्यादि', 'इति + आदि', 'यण संधि', 'इ + आ = या', ['इत्य + आदि', 'इति + यादि', 'इत + आदि']),
    ('यद्यपि', 'यदि + अपि', 'यण संधि', 'इ + अ = य', ['यद्य + अपि', 'यदि + पि', 'यद् + यपि']),
    ('अत्यधिक', 'अति + अधिक', 'यण संधि', 'इ + अ = य', ['अत्य + अधिक', 'अति + धिक', 'अत + यधिक']),
    ('स्वागत', 'सु + आगत', 'यण संधि', 'उ + आ = वा', ['स्व + आगत', 'सु + वागत', 'स्वा + गत']),
    ('अन्वेषण', 'अनु + एषण', 'यण संधि', 'उ + ए = वे', ['अन्व + एषण', 'अनु + वेषण', 'अन + वेषण']),
    ('प्रत्येक', 'प्रति + एक', 'यण संधि', 'इ + ए = ये', ['प्रत्य + एक', 'प्रति + येक', 'प्रत + येक']),
    ('अभ्युदय', 'अभि + उदय', 'यण संधि', 'इ + उ = यु', ['अभ्य + उदय', 'अभि + युदय', 'अभ + युदय']),
    ('नयन', 'ने + अन', 'अयादि संधि', 'ए + अ = अय', ['नय + न', 'न + यन', 'नै + अन']),
    ('पवन', 'पो + अन', 'अयादि संधि', 'ओ + अ = अव', ['पव + न', 'प + वन', 'पौ + अन']),
    ('गायक', 'गै + अक', 'अयादि संधि', 'ऐ + अ = आय', ['गाय + क', 'गा + यक', 'गे + अक']),
    ('पावक', 'पौ + अक', 'अयादि संधि', 'औ + अ = आव', ['पाव + क', 'पा + वक', 'पो + अक']),
    ('नाविक', 'नौ + इक', 'अयादि संधि', 'औ + इ = आवि', ['नाव + इक', 'ना + विक', 'नो + इक']),
    ('भवन', 'भो + अन', 'अयादि संधि', 'ओ + अ = अव', ['भव + न', 'भ + वन', 'भौ + अन']),
    ('पवित्र', 'पो + इत्र', 'अयादि संधि', 'ओ + इ = अवि', ['पवि + त्र', 'प + वित्र', 'पौ + इत्र']),
]
SANDHI_V = [
    ('सदाचार', 'सत् + आचार', 'व्यंजन संधि', 'त् के बाद स्वर आने पर त् → द्', ['सदा + चार', 'सद + आचार', 'सत + आचार']),
    ('जगदीश', 'जगत् + ईश', 'व्यंजन संधि', 'त् के बाद स्वर आने पर त् → द्', ['जगद + ईश', 'जग + दीश', 'जगत + ईश']),
    ('उन्नति', 'उत् + नति', 'व्यंजन संधि', 'त् के बाद न आने पर त् → न्', ['उन + नति', 'उन्न + ति', 'उत + नति']),
    ('संतोष', 'सम् + तोष', 'व्यंजन संधि', 'म् के बाद त आने पर म् → अनुस्वार', ['सं + तोष', 'सन + तोष', 'सम + तोष']),
    ('दिग्गज', 'दिक् + गज', 'व्यंजन संधि', 'क् के बाद ग आने पर क् → ग्', ['दिग + गज', 'दि + ग्गज', 'दिग् + अज']),
    ('वागीश', 'वाक् + ईश', 'व्यंजन संधि', 'क् के बाद स्वर आने पर क् → ग्', ['वाग + ईश', 'वा + गीश', 'वाक + ईश']),
    ('उल्लास', 'उत् + लास', 'व्यंजन संधि', 'त् के बाद ल आने पर त् → ल्', ['उल + लास', 'उल्ल + आस', 'उत + लास']),
    ('सज्जन', 'सत् + जन', 'व्यंजन संधि', 'त् के बाद ज आने पर त् → ज्', ['सज + जन', 'स + ज्जन', 'सत + जन']),
    ('उज्ज्वल', 'उत् + ज्वल', 'व्यंजन संधि', 'त् के बाद ज आने पर त् → ज्', ['उज + ज्वल', 'उज्ज + वल', 'उत + ज्वल']),
    ('जगन्नाथ', 'जगत् + नाथ', 'व्यंजन संधि', 'त् के बाद न आने पर त् → न्', ['जगन + नाथ', 'जग + न्नाथ', 'जगत + नाथ']),
    ('संकल्प', 'सम् + कल्प', 'व्यंजन संधि', 'म् के बाद क आने पर म् → अनुस्वार', ['सं + कल्प', 'सन + कल्प', 'संक + ल्प']),
    ('मनोयोग', 'मनः + योग', 'विसर्ग संधि', 'अः के बाद घोष व्यंजन आने पर अः → ओ', ['मनो + योग', 'मन + योग', 'म + नोयोग']),
    ('निश्चल', 'निः + चल', 'विसर्ग संधि', 'विसर्ग के बाद च आने पर विसर्ग → श्', ['निश + चल', 'नि + श्चल', 'निस् + चल']),
    ('दुर्गम', 'दुः + गम', 'विसर्ग संधि', 'इ/उ के बाद विसर्ग और आगे घोष व्यंजन आने पर विसर्ग → र्', ['दुर + गम', 'दु + र्गम', 'दुर् + अगम']),
    ('निर्धन', 'निः + धन', 'विसर्ग संधि', 'इ के बाद विसर्ग और आगे घोष व्यंजन आने पर विसर्ग → र्', ['निर + धन', 'नि + र्धन', 'निर्ध + न']),
    ('नमस्ते', 'नमः + ते', 'विसर्ग संधि', 'विसर्ग के बाद त आने पर विसर्ग → स्', ['नमस + ते', 'नम + स्ते', 'नमस् + अते']),
    ('निराशा', 'निः + आशा', 'विसर्ग संधि', 'इ के बाद विसर्ग और आगे स्वर आने पर विसर्ग → र्', ['निरा + शा', 'नि + राशा', 'निर + आशा']),
    ('दुर्लभ', 'दुः + लभ', 'विसर्ग संधि', 'उ के बाद विसर्ग और आगे ल आने पर विसर्ग → र्', ['दुर + लभ', 'दु + र्लभ', 'दुर्ल + भ']),
    ('मनोबल', 'मनः + बल', 'विसर्ग संधि', 'अः के बाद घोष व्यंजन (ब) आने पर अः → ओ', ['मनो + बल', 'मन + बल', 'म + नोबल']),
    ('तपोभूमि', 'तपः + भूमि', 'विसर्ग संधि', 'अः के बाद घोष व्यंजन (भ) आने पर अः → ओ', ['तपो + भूमि', 'तप + भूमि', 'त + पोभूमि']),
]

SAMAS_L4 = ['तत्पुरुष समास', 'द्वंद्व समास', 'द्विगु समास', 'कर्मधारय समास']
SAMAS_L6 = SAMAS_L4 + ['अव्ययीभाव समास', 'बहुव्रीहि समास']
SAMAS_DEF = {'तत्पुरुष समास': 'उत्तर पद प्रधान; विग्रह में कारक-चिह्न (का, की, के लिए, से, में) लगते हैं।', 'द्वंद्व समास': 'दोनों पद प्रधान; विग्रह में “और/या” लगता है।',
             'द्विगु समास': 'पहला पद संख्यावाचक; पूरा पद समूह/समाहार का बोध कराता है।', 'कर्मधारय समास': 'विशेषण-विशेष्य या उपमेय-उपमान का संबंध (“है जो”, “के समान”, “रूपी”)।',
             'अव्ययीभाव समास': 'पहला पद अव्यय और प्रधान; पूरा पद अव्यय की तरह प्रयुक्त।', 'बहुव्रीहि समास': 'कोई भी पद प्रधान नहीं; दोनों मिलकर किसी तीसरे (अन्य) अर्थ की ओर संकेत करते हैं।'}
SAMAS_WHY = {'तत्पुरुष समास': 'विग्रह में कारक-चिह्न आता है और उत्तर पद प्रधान है।', 'द्वंद्व समास': 'दोनों पद प्रधान हैं और विग्रह में “और” आता है।',
             'द्विगु समास': 'पहला पद संख्यावाचक है और पूरा पद समूह का बोध कराता है।', 'कर्मधारय समास': 'पदों में विशेषण-विशेष्य या उपमेय-उपमान का संबंध है।',
             'अव्ययीभाव समास': 'पहला पद अव्यय है और पूरा पद क्रियाविशेषण (अव्यय) की तरह प्रयुक्त होता है।', 'बहुव्रीहि समास': 'दोनों पद मिलकर किसी अन्य (तीसरे) व्यक्ति का बोध कराते हैं।'}
SAMAS = [
    ('राजपुत्र', 'राजा का पुत्र', 'तत्पुरुष समास'), ('देशभक्ति', 'देश की भक्ति', 'तत्पुरुष समास'), ('रसोईघर', 'रसोई के लिए घर', 'तत्पुरुष समास'),
    ('गंगाजल', 'गंगा का जल', 'तत्पुरुष समास'), ('हस्तलिखित', 'हस्त (हाथ) से लिखित', 'तत्पुरुष समास'), ('पथभ्रष्ट', 'पथ से भ्रष्ट', 'तत्पुरुष समास'),
    ('सेनापति', 'सेना का पति', 'तत्पुरुष समास'), ('शरणागत', 'शरण में आगत (आया हुआ)', 'तत्पुरुष समास'), ('ग्रामवासी', 'ग्राम का वासी', 'तत्पुरुष समास'),
    ('गुणहीन', 'गुण से हीन', 'तत्पुरुष समास'), ('राष्ट्रपति', 'राष्ट्र का पति', 'तत्पुरुष समास'),
    ('माता-पिता', 'माता और पिता', 'द्वंद्व समास'), ('दाल-रोटी', 'दाल और रोटी', 'द्वंद्व समास'), ('सुख-दुख', 'सुख और दुख', 'द्वंद्व समास'),
    ('रात-दिन', 'रात और दिन', 'द्वंद्व समास'), ('भाई-बहन', 'भाई और बहन', 'द्वंद्व समास'), ('लेन-देन', 'लेना और देना', 'द्वंद्व समास'),
    ('अन्न-जल', 'अन्न और जल', 'द्वंद्व समास'), ('पाप-पुण्य', 'पाप और पुण्य', 'द्वंद्व समास'), ('हानि-लाभ', 'हानि और लाभ', 'द्वंद्व समास'),
    ('चौराहा', 'चार राहों का समूह', 'द्विगु समास'), ('त्रिभुज', 'तीन भुजाओं का समूह', 'द्विगु समास'), ('सप्ताह', 'सात दिनों का समूह', 'द्विगु समास'),
    ('नवरत्न', 'नौ रत्नों का समूह', 'द्विगु समास'), ('शताब्दी', 'सौ वर्षों (अब्दों) का समूह', 'द्विगु समास'), ('त्रिलोक', 'तीन लोकों का समूह', 'द्विगु समास'),
    ('दोपहर', 'दो पहरों का समूह', 'द्विगु समास'), ('चौमासा', 'चार मासों का समूह', 'द्विगु समास'), ('पंचतत्व', 'पाँच तत्वों का समूह', 'द्विगु समास'),
    ('नीलकमल', 'नीला है जो कमल', 'कर्मधारय समास'), ('महात्मा', 'महान है जो आत्मा', 'कर्मधारय समास'), ('नीलगगन', 'नीला है जो गगन', 'कर्मधारय समास'),
    ('महापुरुष', 'महान है जो पुरुष', 'कर्मधारय समास'), ('सज्जन', 'सत् (अच्छा) है जो जन', 'कर्मधारय समास'), ('परमानंद', 'परम है जो आनंद', 'कर्मधारय समास'),
    ('कालीमिर्च', 'काली है जो मिर्च', 'कर्मधारय समास'), ('चंद्रमुख', 'चंद्र के समान मुख', 'कर्मधारय समास'), ('विद्याधन', 'विद्या रूपी धन', 'कर्मधारय समास'),
    ('क्रोधाग्नि', 'क्रोध रूपी अग्नि', 'कर्मधारय समास'),
]
SAMAS_X = [
    ('यथाशक्ति', 'शक्ति के अनुसार', 'अव्ययीभाव समास'), ('प्रतिदिन', 'हर दिन', 'अव्ययीभाव समास'), ('आजीवन', 'जीवन भर', 'अव्ययीभाव समास'),
    ('भरपेट', 'पेट भरकर', 'अव्ययीभाव समास'), ('यथासंभव', 'जितना संभव हो', 'अव्ययीभाव समास'), ('बेखटके', 'बिना खटके के', 'अव्ययीभाव समास'), ('आमरण', 'मरण तक', 'अव्ययीभाव समास'),
    ('दशानन', 'दस हैं आनन (मुख) जिसके — अर्थात् रावण', 'बहुव्रीहि समास'), ('लंबोदर', 'लंबा है उदर जिसका — अर्थात् गणेश', 'बहुव्रीहि समास'),
    ('चक्रपाणि', 'चक्र है पाणि (हाथ) में जिसके — अर्थात् विष्णु', 'बहुव्रीहि समास'), ('गजानन', 'गज का-सा आनन है जिसका — अर्थात् गणेश', 'बहुव्रीहि समास'),
    ('नीलकंठ', 'नीला है कंठ जिसका — अर्थात् शिव', 'बहुव्रीहि समास'), ('गिरिधर', 'गिरि को धारण करने वाला — अर्थात् कृष्ण', 'बहुव्रीहि समास'),
    ('चंद्रशेखर', 'चंद्र है शिखर (मस्तक) पर जिसके — अर्थात् शिव', 'बहुव्रीहि समास'),
]

UPSARG = [
    ('अपमान', 'अप + मान'), ('अनुशासन', 'अनु + शासन'), ('अभिमान', 'अभि + मान'), ('उपवन', 'उप + वन'), ('दुर्गुण', 'दुर् + गुण'),
    ('निर्धन', 'निर् + धन'), ('प्रगति', 'प्र + गति'), ('पराजय', 'परा + जय'), ('विदेश', 'वि + देश'), ('सुपुत्र', 'सु + पुत्र'),
    ('बेईमान', 'बे + ईमान'), ('लापरवाह', 'ला + परवाह'), ('अनपढ़', 'अन + पढ़'), ('अज्ञान', 'अ + ज्ञान'), ('प्रतिदिन', 'प्रति + दिन'),
    ('अधिकार', 'अधि + कार'), ('कुपुत्र', 'कु + पुत्र'), ('सपरिवार', 'स + परिवार'), ('निडर', 'नि + डर'), ('बेचैन', 'बे + चैन'),
    ('अनुकरण', 'अनु + करण'), ('उपनाम', 'उप + नाम'), ('विज्ञान', 'वि + ज्ञान'), ('सुगंध', 'सु + गंध'),
]
PRATYAY = [
    ('सुंदरता', 'सुंदर + ता'), ('बचपन', 'बच्चा + पन'), ('पढ़ाई', 'पढ़ + आई'), ('सामाजिक', 'समाज + इक'), ('दैनिक', 'दिन + इक'),
    ('रंगीला', 'रंग + ईला'), ('दूधवाला', 'दूध + वाला'), ('घबराहट', 'घबरा + आहट'), ('चित्रकार', 'चित्र + कार'), ('ईमानदार', 'ईमान + दार'),
    ('सजावट', 'सज + आवट'), ('राष्ट्रीय', 'राष्ट्र + ईय'), ('बुद्धिमान', 'बुद्धि + मान'), ('धनवान', 'धन + वान'), ('दयालु', 'दया + आलु'),
    ('मानवता', 'मानव + ता'), ('लिखावट', 'लिख + आवट'), ('भारतीय', 'भारत + ईय'), ('मिठास', 'मीठा + आस'), ('गरीबी', 'गरीब + ई'),
    ('चमकीला', 'चमक + ईला'), ('कलाकार', 'कला + कार'), ('दुकानदार', 'दुकान + दार'), ('मुस्कुराहट', 'मुस्कुरा + आहट'),
]

PARYAY = [
    ('सूर्य', ['रवि', 'दिनकर', 'भानु', 'दिवाकर']), ('चंद्रमा', ['चाँद', 'शशि', 'इंदु', 'सुधाकर']), ('पानी', ['जल', 'नीर', 'वारि', 'अंबु']),
    ('पृथ्वी', ['धरती', 'भूमि', 'धरा', 'वसुधा']), ('आकाश', ['गगन', 'नभ', 'अंबर', 'व्योम']), ('पर्वत', ['पहाड़', 'गिरि', 'अचल', 'शैल']),
    ('नदी', ['सरिता', 'तटिनी', 'तरंगिणी', 'सरि']), ('पेड़', ['वृक्ष', 'तरु', 'विटप', 'पादप']), ('फूल', ['पुष्प', 'सुमन', 'कुसुम', 'प्रसून']),
    ('हवा', ['पवन', 'वायु', 'समीर', 'अनिल']), ('आग', ['अग्नि', 'अनल', 'पावक', 'आतिश']), ('घर', ['गृह', 'सदन', 'भवन', 'निकेतन']),
    ('मित्र', ['दोस्त', 'सखा', 'सहचर', 'सुहृद']), ('आँख', ['नेत्र', 'नयन', 'लोचन', 'चक्षु']), ('बादल', ['मेघ', 'जलद', 'घन', 'जलधर']),
    ('रात', ['रात्रि', 'निशा', 'रजनी', 'यामिनी']), ('समुद्र', ['सागर', 'जलधि', 'सिंधु', 'रत्नाकर']), ('राजा', ['नृप', 'भूप', 'महीप', 'नरेश']),
    ('कमल', ['पंकज', 'जलज', 'सरोज', 'नीरज']), ('सोना', ['स्वर्ण', 'कनक', 'कंचन', 'हेम']), ('शरीर', ['देह', 'तन', 'काया', 'गात']),
    ('जंगल', ['वन', 'कानन', 'अरण्य', 'विपिन']), ('माँ', ['माता', 'जननी', 'अंबा', 'मैया']), ('दुख', ['पीड़ा', 'कष्ट', 'व्यथा', 'वेदना']),
]
VILOM = [
    ('दिन', 'रात'), ('सुख', 'दुख'), ('आदर', 'अनादर'), ('उन्नति', 'अवनति'), ('आशा', 'निराशा'), ('आय', 'व्यय'), ('उदय', 'अस्त'),
    ('प्राचीन', 'नवीन'), ('आरंभ', 'अंत'), ('विजय', 'पराजय'), ('स्वतंत्र', 'परतंत्र'), ('सज्जन', 'दुर्जन'), ('सत्य', 'असत्य'),
    ('आयात', 'निर्यात'), ('धनी', 'निर्धन'), ('ज्ञान', 'अज्ञान'), ('मित्र', 'शत्रु'), ('सरल', 'कठिन'), ('स्वदेश', 'विदेश'),
    ('जीवन', 'मरण'), ('मान', 'अपमान'), ('निर्माण', 'विनाश'), ('स्वस्थ', 'अस्वस्थ'), ('सक्रिय', 'निष्क्रिय'), ('लाभ', 'हानि'),
    ('अमृत', 'विष'), ('कृतज्ञ', 'कृतघ्न'), ('उत्तीर्ण', 'अनुत्तीर्ण'), ('शीत', 'उष्ण'), ('आदान', 'प्रदान'), ('सजीव', 'निर्जीव'),
    ('प्रकाश', 'अंधकार'), ('स्मरण', 'विस्मरण'), ('उपस्थित', 'अनुपस्थित'), ('गुण', 'दोष'), ('आकर्षण', 'विकर्षण'),
]

MUHAVARE = [
    ('आँखों का तारा होना', 'बहुत प्यारा होना', '{N} अपनी दादी की आँखों का तारा है।'),
    ('नौ दो ग्यारह होना', 'भाग जाना', 'पुलिस को देखते ही चोर नौ दो ग्यारह हो गया।'),
    ('ईद का चाँद होना', 'बहुत दिनों बाद दिखाई देना', 'अरे {N}, आजकल तो तुम ईद का चाँद हो गए हो!'),
    ('दाँतों तले उँगली दबाना', 'बहुत हैरान होना', 'नन्हे जादूगर का खेल देखकर दर्शकों ने दाँतों तले उँगली दबा ली।'),
    ('आसमान सिर पर उठाना', 'बहुत शोर मचाना', 'शिक्षक के बाहर जाते ही बच्चों ने आसमान सिर पर उठा लिया।'),
    ('नाक में दम करना', 'बहुत परेशान करना', 'पड़ोस के शरारती कुत्ते ने सबकी नाक में दम कर रखा है।'),
    ('हाथ-पाँव फूल जाना', 'बहुत घबरा जाना', 'मंच पर पहुँचते ही {N} के हाथ-पाँव फूल गए।'),
    ('पानी-पानी होना', 'बहुत लज्जित होना', 'झूठ पकड़े जाने पर {N} पानी-पानी हो ग{या}।'),
    ('घी के दीये जलाना', 'बहुत खुशियाँ मनाना', 'टीम की जीत पर पूरे मोहल्ले ने घी के दीये जलाए।'),
    ('आग बबूला होना', 'बहुत क्रोधित होना', 'टूटा हुआ गमला देखकर माली आग बबूला हो गया।'),
    ('कमर कसना', 'किसी काम के लिए पूरी तरह तैयार होना', 'परीक्षा के लिए {N} ने कमर कस ली है।'),
    ('अंगूठा दिखाना', 'समय पर साफ़ मना कर देना', 'काम निकलते ही उसने अंगूठा दिखा दिया।'),
    ('आँखें बिछाना', 'प्रेम से स्वागत करना', 'मेहमानों के स्वागत में गाँव वालों ने आँखें बिछा दीं।'),
    ('मुँह में पानी आना', 'खाने की तीव्र इच्छा होना', 'गरम जलेबियाँ देखकर {N} के मुँह में पानी आ गया।'),
    ('लोहे के चने चबाना', 'बहुत कठिन काम करना', 'पहाड़ पर सड़क बनाना लोहे के चने चबाने जैसा था।'),
    ('टस से मस न होना', 'अपनी बात पर अड़े रहना', 'सबने बहुत समझाया, पर {N} टस से मस न हु{या}।'),
    ('हवा से बातें करना', 'बहुत तेज़ दौड़ना', 'नया घोड़ा मैदान में हवा से बातें करने लगा।'),
    ('कान खड़े होना', 'सावधान हो जाना', 'झाड़ियों में सरसराहट सुनकर चौकीदार के कान खड़े हो गए।'),
    ('पेट में चूहे दौड़ना', 'बहुत भूख लगना', 'खेल के बाद {N} के पेट में चूहे दौड़ने लगे।'),
    ('फूला न समाना', 'बहुत प्रसन्न होना', 'पुरस्कार पाकर {N} फूल{ा} न समा{या}।'),
    ('खून-पसीना एक करना', 'कड़ी मेहनत करना', 'किसानों ने खून-पसीना एक करके फसल उगाई।'),
    ('श्रीगणेश करना', 'किसी काम की शुरुआत करना', 'नए पुस्तकालय का श्रीगणेश प्रधानाचार्य ने किया।'),
    ('चिकना घड़ा होना', 'किसी बात का कोई असर न होना', 'उसे कितना भी समझाओ, वह तो चिकना घड़ा है।'),
    ('आस्तीन का साँप', 'कपटी मित्र', 'जिसे हम अपना मानते थे, वही आस्तीन का साँप निकला।'),
]
LOKOKTI = [
    ('अब पछताए होत क्या जब चिड़िया चुग गई खेत', 'समय निकल जाने पर पछताना व्यर्थ है', 'पूरे साल नहीं पढ़े, अब रोने से क्या — अब पछताए होत क्या जब चिड़िया चुग गई खेत।'),
    ('नाच न जाने आँगन टेढ़ा', 'अपनी कमी को दूसरों या परिस्थिति पर डालना', 'खेलना नहीं आता तो मैदान को दोष देता है — नाच न जाने आँगन टेढ़ा।'),
    ('अधजल गगरी छलकत जाय', 'कम ज्ञान वाला अधिक दिखावा करता है', 'थोड़ी-सी जानकारी पर इतना घमंड! अधजल गगरी छलकत जाय।'),
    ('ऊँट के मुँह में जीरा', 'आवश्यकता से बहुत कम वस्तु', 'पहलवान के लिए एक केला ऊँट के मुँह में जीरा है।'),
    ('जिसकी लाठी उसकी भैंस', 'शक्तिशाली की ही जीत होती है', 'बिना नियम के खेल में जिसकी लाठी उसकी भैंस वाली बात हो जाती है।'),
    ('बूँद-बूँद से घड़ा भरता है', 'थोड़ा-थोड़ा जोड़ने से बहुत हो जाता है', 'रोज़ दस रुपये बचाओ; बूँद-बूँद से घड़ा भरता है।'),
    ('दूर के ढोल सुहावने', 'दूर की चीज़ें अच्छी लगती हैं', 'विदेश का जीवन आसान लगता है, पर दूर के ढोल सुहावने होते हैं।'),
    ('आम के आम गुठलियों के दाम', 'दोहरा लाभ', 'पुरानी किताबें बेचीं और जगह भी खाली हुई — आम के आम गुठलियों के दाम।'),
    ('एक पंथ दो काज', 'एक काम से दो लाभ', 'दादी से मिलने गए और मेला भी देख लिया — एक पंथ दो काज।'),
    ('थोथा चना बाजे घना', 'गुणहीन व्यक्ति अधिक दिखावा करता है', 'जो कुछ नहीं जानता वही सबसे ज़्यादा बोलता है; थोथा चना बाजे घना।'),
    ('जल में रहकर मगर से बैर', 'जिसके अधीन रहना, उसी से शत्रुता करना', 'मालिक से रोज़ झगड़ा करना जल में रहकर मगर से बैर करने जैसा है।'),
    ('घर का भेदी लंका ढाए', 'आपसी भेद खोलने वाला बड़ा नुकसान करता है', 'टीम की योजना अपने ही खिलाड़ी ने बता दी — घर का भेदी लंका ढाए।'),
]

ANEKARTH = [
    ('कल', [('बीता हुआ दिन', 'कल हम चिड़ियाघर गए थे।'), ('आने वाला दिन', 'कल मेरी परीक्षा है।'), ('मशीन/यंत्र', 'कारखाने में नई कल लगाई गई।')]),
    ('अर्थ', [('मतलब', 'इस शब्द का अर्थ बताइए।'), ('धन', 'अर्थ के बिना व्यापार नहीं चलता।')]),
    ('हार', [('पराजय', 'खेल में हार-जीत होती रहती है।'), ('माला', 'माँ ने गले में मोतियों का हार पहना।')]),
    ('पत्र', [('चिट्ठी', 'मैंने दादाजी को पत्र लिखा।'), ('पत्ता', 'पेड़ से एक सूखा पत्र गिरा।')]),
    ('कर', [('हाथ', 'उसने दोनों कर जोड़कर प्रणाम किया।'), ('टैक्स', 'नागरिकों को समय पर कर चुकाना चाहिए।'), ('किरण', 'सूर्य के कर धरती पर फैल गए।')]),
    ('उत्तर', [('जवाब', 'उसने प्रश्न का सही उत्तर दिया।'), ('एक दिशा', 'हिमालय भारत के उत्तर में है।')]),
    ('फल', [('खाने का फल', 'बाज़ार से ताज़े फल लाओ।'), ('परिणाम', 'मेहनत का फल मीठा होता है।')]),
    ('सोना', [('एक धातु', 'सोना बहुत महँगा हो गया है।'), ('नींद लेना', 'रात को जल्दी सोना चाहिए।')]),
    ('मत', [('राय', 'इस विषय पर सबका मत अलग है।'), ('वोट', 'चुनाव में हर नागरिक मत देता है।'), ('नहीं (निषेध)', 'वहाँ मत जाओ।')]),
    ('आम', [('एक फल', 'गर्मियों में आम खूब मिलते हैं।'), ('साधारण', 'यह आम लोगों की समस्या है।')]),
    ('तीर', [('बाण', 'शिकारी ने तीर चलाया।'), ('किनारा', 'नदी के तीर पर मंदिर है।')]),
    ('अंबर', [('आकाश', 'अंबर में तारे चमक रहे थे।'), ('वस्त्र', 'राजा ने पीला अंबर पहना था।')]),
    ('पद', [('पैर', 'गुरु के पद छूकर आशीर्वाद लिया।'), ('ओहदा', 'उन्हें प्रबंधक का पद मिला।'), ('कविता का अंश', 'भक्त कवियों के पद बहुत मधुर हैं।')]),
    ('वर', [('दूल्हा', 'बारात में वर घोड़ी पर बैठा था।'), ('वरदान', 'देवता ने तपस्वी को वर दिया।')]),
]

VARTANI = [
    ('आशिर्वाद', 'आशीर्वाद', '“शी” में दीर्घ ई होती है और रेफ “वा” के ऊपर आता है।', ['आर्शीवाद', 'आशीरवाद', 'आशिरवाद']),
    ('उज्वल', 'उज्ज्वल', 'उत् + ज्वल — ज का द्वित्व होता है।', ['उजज्वल', 'उज्जवल', 'उजवल']),
    ('कवियत्री', 'कवयित्री', 'शुद्ध रूप “कवयित्री” है।', ['कवित्री', 'कवियित्री', 'कव्यत्री']),
    ('अतिथी', 'अतिथि', 'अंत में ह्रस्व इ है।', ['अतीथि', 'अतीथी', 'अथिति']),
    ('परिक्षा', 'परीक्षा', '“री” में दीर्घ ई होती है।', ['परिच्छा', 'परीक्शा', 'पारीक्षा']),
    ('प्रदर्शिनी', 'प्रदर्शनी', '“र्श” के बाद सीधा “नी” आता है।', ['प्रदरशनी', 'परदर्शनी', 'प्रदर्शनि']),
    ('सन्यासी', 'संन्यासी', 'सम् + न्यासी — “सं” के बाद “न्या”।', ['सन्न्यासी', 'संयासी', 'सनयासी']),
    ('व्यवहारिक', 'व्यावहारिक', '“इक” प्रत्यय से पहले स्वर में वृद्धि — “व्या”।', ['व्यवहारीक', 'व्यवाहारिक', 'वयवहारिक']),
    ('अत्याधिक', 'अत्यधिक', 'अति + अधिक = अत्यधिक (यण संधि)।', ['अतिअधिक', 'अत्यधीक', 'अतयधिक']),
    ('इतिहासिक', 'ऐतिहासिक', '“इक” प्रत्यय लगने पर “इ” का “ऐ” हो जाता है।', ['ऐतिहासीक', 'एतिहासिक', 'ऐतीहासिक']),
    ('बिमारी', 'बीमारी', '“बी” में दीर्घ ई है।', ['बीमारि', 'बिमारि', 'बीमारीं']),
    ('दिवार', 'दीवार', '“दी” में दीर्घ ई है।', ['दिवाल', 'दीबार', 'दिवारें']),
    ('श्रीमति', 'श्रीमती', 'अंत में दीर्घ ई है।', ['श्रिमती', 'श्रीमतीं', 'शीमती']),
    ('पुज्य', 'पूज्य', '“पू” में दीर्घ ऊ है।', ['पूजय', 'पुजय', 'पूज्या']),
    ('उपरोक्त', 'उपर्युक्त', 'उपरि + उक्त = उपर्युक्त (यण संधि)।', ['उपर्योक्त', 'उपरयुक्त', 'उपरीयुक्त']),
    ('कृप्या', 'कृपया', 'शुद्ध रूप “कृपया” है।', ['क्रिपया', 'कृपाया', 'किरपया']),
    ('स्त्रोत', 'स्रोत', '“स्रोत” में “त” केवल अंत में है — स् + र + ओ + त।', ['स्तोत्र', 'सरोत', 'श्रोत']),
    ('प्रमाणिक', 'प्रामाणिक', '“इक” प्रत्यय से वृद्धि — “प्रा”।', ['परमाणिक', 'प्रामाणीक', 'प्रमानिक']),
    ('सहस्त्र', 'सहस्र', 'शुद्ध रूप “सहस्र” है — इसमें “त” नहीं है।', ['सहश्र', 'सहस्रा', 'सहसर']),
    ('ज्योत्सना', 'ज्योत्स्ना', '“त्स्ना” — स् के बाद न।', ['ज्योतसना', 'ज्योस्तना', 'जोत्स्ना']),
    ('आधीन', 'अधीन', 'शुद्ध रूप “अधीन” है।', ['अधिन', 'आधिन', 'अधीण']),
    ('अनाधिकार', 'अनधिकार', 'अन् + अधिकार = अनधिकार।', ['अनधीकार', 'अनाधीकार', 'अनधिकर']),
]

ERRORS = [
    ('मैंने अपना गृहकार्य पूरी कर ली है।', 'मैंने अपना गृहकार्य पूरा कर लिया है।', '“गृहकार्य” पुल्लिंग है, इसलिए “पूरा कर लिया”।', ['मैंने अपनी गृहकार्य पूरी कर ली है।', 'मैं अपना गृहकार्य पूरा कर लिया है।', 'मैंने अपना गृहकार्य पूरे कर लिए है।']),
    ('मेरे को यह पुस्तक चाहिए।', 'मुझे यह पुस्तक चाहिए।', '“मेरे को” अशुद्ध है; शुद्ध रूप “मुझे” या “मुझको”।', ['मेरे को यह पुस्तक चाहिए है।', 'मैंने यह पुस्तक चाहिए।', 'मेरा यह पुस्तक चाहिए।']),
    ('उसने बाज़ार गया।', 'वह बाज़ार गया।', '“जाना” अकर्मक क्रिया है; इसके साथ “ने” नहीं लगता।', ['उसने बाज़ार गई।', 'उसको बाज़ार गया।', 'उसने बाज़ार जाया।']),
    ('हम ने चाय पिया।', 'हमने चाय पी।', '“हमने” मिलाकर लिखा जाता है; “चाय” स्त्रीलिंग है, इसलिए “पी”।', ['हमने चाय पिया।', 'हम चाय पी।', 'हमने चाय पिये।']),
    ('कृपया मुझे कल अवकाश देने की कृपा करें।', 'मुझे कल अवकाश देने की कृपा करें।', '“कृपया” और “कृपा करें” साथ लिखना पुनरुक्ति दोष है।', ['कृपया मुझे कल अवकाश देने की कृपया करें।', 'कृपा मुझे कल अवकाश देने की कृपया करें।', 'कृपया मुझे कल अवकाश देने कृपा करें।']),
    ('प्रत्येक छात्रों को पुस्तक मिलेगी।', 'प्रत्येक छात्र को पुस्तक मिलेगी।', '“प्रत्येक” के साथ एकवचन संज्ञा आती है।', ['प्रत्येक छात्रों को पुस्तकें मिलेगी।', 'प्रत्येक छात्रों ने पुस्तक मिलेगी।', 'हर एक छात्रों को पुस्तक मिलेगी।']),
    ('वह सबसे सुंदरतम चित्र है।', 'वह सबसे सुंदर चित्र है।', '“सबसे” और “तम” दोनों श्रेष्ठता बताते हैं — एक ही पर्याप्त है।', ['वह सबसे सुंदरतर चित्र है।', 'वह सब से सुंदरतम चित्र है।', 'वह सबसे अधिक सुंदरतम चित्र है।']),
    ('मैं आपका दर्शन करने आया हूँ।', 'मैं आपके दर्शन करने आया हूँ।', '“दर्शन” सदा बहुवचन में प्रयुक्त होता है।', ['मैं आपकी दर्शन करने आया हूँ।', 'मैंने आपके दर्शन करने आया हूँ।', 'मैं आपका दर्शनों करने आया हूँ।']),
    ('उसकी आँखों में अश्रु के आँसू थे।', 'उसकी आँखों में आँसू थे।', '“अश्रु” और “आँसू” का एक ही अर्थ है — पुनरुक्ति दोष।', ['उसकी आँखों में अश्रु के आँसू था।', 'उसके आँखों में आँसू थे।', 'उसकी आँखें में आँसू थे।']),
    ('मेरे पिताजी कल आएगा।', 'मेरे पिताजी कल आएँगे।', 'आदर के लिए क्रिया बहुवचन में आती है।', ['मेरे पिताजी कल आएगी।', 'मेरा पिताजी कल आएँगे।', 'मेरे पिताजी कल आएगें।']),
    ('लड़कियाँ मैदान में खेल रहा है।', 'लड़कियाँ मैदान में खेल रही हैं।', 'कर्ता स्त्रीलिंग बहुवचन है, इसलिए क्रिया “खेल रही हैं”।', ['लड़कियाँ मैदान में खेल रहे हैं।', 'लड़कियाँ मैदान में खेल रही है।', 'लड़कियों ने मैदान में खेल रही हैं।']),
    ('{N} ने गीत गाई।', '{N} ने गीत गाया।', '“ने” के साथ क्रिया कर्म “गीत” (पुल्लिंग) के अनुसार होती है, कर्ता के अनुसार नहीं।', ['{N} गीत गाई।', '{N} ने गीत गाये गए।', '{N} ने गीत गाईं।']),
    ('मैंने उसको एक पत्र भेजी।', 'मैंने उसको एक पत्र भेजा।', '“पत्र” पुल्लिंग है।', ['मैं उसको एक पत्र भेजा।', 'मैंने उसको एक पत्र भेजे।', 'मैंने उसके एक पत्र भेजी।']),
    ('{N} अपना माँ के साथ ग{या}।', '{N} अपनी माँ के साथ ग{या}।', '“माँ” स्त्रीलिंग है, इसलिए “अपनी”।', ['{N} अपने माँ के साथ ग{या}।', '{N} उसकी माँ के साथ ग{या}।', '{N} अपनी माँ का साथ ग{या}।']),
    ('मुझे तुम्हारे से बात करनी है।', 'मुझे तुमसे बात करनी है।', '“तुम्हारे से” अशुद्ध है; शुद्ध रूप “तुमसे”।', ['मुझे तुम्हारे से बात करना है।', 'मैंने तुमसे बात करनी है।', 'मेरे को तुमसे बात करनी है।']),
    ('आज ठंडी हवा चल रहा है।', 'आज ठंडी हवा चल रही है।', '“हवा” स्त्रीलिंग है।', ['आज ठंडा हवा चल रहा है।', 'आज ठंडी हवा चल रहे हैं।', 'आज ठंडे हवा चल रही है।']),
    ('पुस्तक मेज़ में रखी है।', 'पुस्तक मेज़ पर रखी है।', 'सतह के ऊपर रखी वस्तु के लिए “पर” परसर्ग आता है।', ['पुस्तक मेज़ से रखी है।', 'पुस्तक मेज़ में रखा है।', 'पुस्तक मेज़ को रखी है।']),
    ('उसने मेरे को बुलाया।', 'उसने मुझे बुलाया।', '“मेरे को” के स्थान पर “मुझे”।', ['वह मेरे को बुलाया।', 'उसने मेरा बुलाया।', 'उसने मैं को बुलाया।']),
    ('यह बात मैंने तुम्हें पहले ही बता दिया था।', 'यह बात मैंने तुम्हें पहले ही बता दी थी।', '“बात” स्त्रीलिंग है, इसलिए “बता दी थी”।', ['यह बात मैं तुम्हें पहले ही बता दी थी।', 'यह बात मैंने तुम्हें पहले ही बता दिये थे।', 'यह बात मैंने तुम्हारे को पहले ही बता दी थी।']),
    ('हमें बड़ों का आदर करनी चाहिए।', 'हमें बड़ों का आदर करना चाहिए।', '“आदर” पुल्लिंग है, इसलिए “करना चाहिए”।', ['हमें बड़ों की आदर करनी चाहिए।', 'हमने बड़ों का आदर करना चाहिए।', 'हम बड़ों का आदर करना चाहिए।']),
]

EKSHABD = [
    ('जो ईश्वर में विश्वास रखता हो', 'आस्तिक', '', ['नास्तिक', 'धार्मिक', 'पुजारी']),
    ('जिसका कोई अंत न हो', 'अनंत', '', ['अनादि', 'अमर', 'अटूट']),
    ('जो पढ़ना-लिखना न जानता हो', 'निरक्षर', '', ['साक्षर', 'अज्ञानी', 'अनाड़ी']),
    ('जो दूसरों का भला करता हो', 'परोपकारी', '', ['स्वार्थी', 'दानी', 'सज्जन']),
    ('जो कम बोलता हो', 'मितभाषी', '', ['मृदुभाषी', 'बहुभाषी', 'मौन']),
    ('जिसे जीता न जा सके', 'अजेय', '', ['अमर', 'अभय', 'अटल']),
    ('जो देखने योग्य हो', 'दर्शनीय', '', ['दृश्य', 'सुंदर', 'प्रत्यक्ष']),
    ('जहाँ पहुँचना कठिन हो', 'दुर्गम', '', ['दुर्लभ', 'सुगम', 'अदृश्य']),
    ('जो सब कुछ जानता हो', 'सर्वज्ञ', '', ['सर्वव्यापी', 'विद्वान', 'ज्ञानी']),
    ('जो दूर की बात सोचता हो', 'दूरदर्शी', '', ['दूरदर्शन', 'विचारक', 'बुद्धिमान']),
    ('जो मांस न खाता हो', 'शाकाहारी', '', ['मांसाहारी', 'उपवासी', 'सर्वाहारी']),
    ('जिसका कोई आकार न हो', 'निराकार', '', ['साकार', 'अदृश्य', 'असीम']),
    ('जो किए गए उपकार को माने', 'कृतज्ञ', '', ['कृतघ्न', 'उपकारी', 'दानी']),
    ('जो किए गए उपकार को न माने', 'कृतघ्न', '', ['कृतज्ञ', 'स्वार्थी', 'निर्दयी']),
    ('सप्ताह में एक बार होने वाला', 'साप्ताहिक', '', ['मासिक', 'दैनिक', 'पाक्षिक']),
    ('प्रतिदिन होने वाला', 'दैनिक', '', ['साप्ताहिक', 'वार्षिक', 'मासिक']),
    ('जो विश्वास के योग्य हो', 'विश्वसनीय', '', ['विश्वासी', 'आस्तिक', 'आत्मविश्वासी']),
    ('जिसका वर्णन न किया जा सके', 'अवर्णनीय', '', ['अदृश्य', 'अपठनीय', 'अनुपम']),
    ('आकाश में विचरण करने वाला', 'नभचर', '', ['जलचर', 'थलचर', 'निशाचर']),
    ('जल में रहने वाला', 'जलचर', '', ['नभचर', 'थलचर', 'निशाचर']),
    ('जो पहले कभी न हुआ हो', 'अभूतपूर्व', '', ['अद्भुत', 'नवीन', 'अनुपम']),
    ('जो अपनी प्रतिज्ञा पर दृढ़ रहे', 'दृढ़प्रतिज्ञ', '', ['ज़िद्दी', 'साहसी', 'आत्मनिर्भर']),
]


# =========================================================== more factories (word level)

import unicodedata as _ud


def bad_splits(w, correct, k=6):
    """Wrong ways of splitting a word into two parts (never inside a matra / halant)."""
    out = []
    for i in range(1, len(w)):
        if _ud.category(w[i])[0] == 'M' or w[i - 1] == '्':
            continue
        sp = f'{w[:i]} + {w[i:]}'
        if sp != correct and sp not in out:
            out.append(sp)
    return out[:k]


def splitx(bank, what):
    """(word, split) -> xform bank with automatic wrong splits."""
    out = []
    for w, sp in bank:
        a, b = sp.split(' + ')
        note = f'{Q(w)} = {sp}; ' + (f'उपसर्ग {Q(a)}, मूल शब्द {Q(b)}।' if what == 'उपसर्ग' else f'मूल शब्द {Q(a)}, प्रत्यय {Q(b)}।')
        out.append((w, sp, note, bad_splits(w, sp)))
    return out


def paryay(t, groups, c4=True):
    allw = [(h, s) for h, ss in groups for s in ss]

    @t.add('C1', (1, 2, 3))
    def py_c1(r, D):
        h, ss = r.choice(groups)
        if r.random() < 0.5:
            c = r.choice(ss)
            ds = r.sample([s for hh, s in allw if hh != h], 3)
            return mq(r, r.choice([f'{Q(h)} का पर्यायवाची शब्द कौन-सा है?', f'इनमें से कौन-सा शब्द {Q(h)} का पर्यायवाची है?']), c, ds, f'{Q(h)} के पर्यायवाची: {", ".join(ss)}।')
        good = r.sample(ss, 3)
        odd = r.choice([s for hh, s in allw if hh != h])
        oh = [hh for hh, s in allw if s == odd][0]
        opts = good + [odd]
        r.shuffle(opts)
        return {'stem': f'इनमें से कौन-सा शब्द {Q(h)} का पर्यायवाची नहीं है?', 'options': opts, 'answer': odd, 'marks': 1,
                'key': f'सही उत्तर: {odd}। {Q(odd)} {Q(oh)} का पर्यायवाची है; शेष शब्द {Q(h)} के पर्यायवाची हैं। [1]'}

    @t.add('C2', (1, 2, 3, 4), 'explain')
    def py_c2(r, D):
        m = mk('C2', D)
        h, ss = r.choice(groups)
        good = r.sample(ss, 2)
        odd = r.choice([s for hh, s in allw if hh != h])
        oh = [hh for hh, s in allw if s == odd][0]
        p, pg = name(r)
        lst = good + [odd]
        r.shuffle(lst)
        stem = f'{p} ने {Q(h)} के तीन पर्यायवाची लिखे: {", ".join(lst)}। क्या सभी सही हैं? गलत शब्द पहचानिए' + (', कारण दीजिए और उसके स्थान पर सही पर्यायवाची लिखिए।' if m >= 2 else '। उत्तर संक्षेप में दीजिए।')
        ok = [s for s in ss if s not in good]
        ans = f'{Q(odd)} गलत है — यह {Q(oh)} का पर्यायवाची है।' + (f' सही विकल्प: {ok[0]}।' if ok else '')
        return item(stem, ans, 'गलत शब्द की पहचान (1)' + ('; कारण (1)' if m >= 2 else '') + ('; सही पर्यायवाची (1)' if m >= 3 else ''), m, 'explain')

    @t.add('C3', (1, 2, 3, 4, 5), 'short')
    def py_c3(r, D):
        parts = []
        for h, ss in r.sample(groups, 4):
            if r.random() < 0.5:
                parts.append((f'{Q(h)} के दो पर्यायवाची शब्द लिखिए।', ', '.join(ss[:2]), f'कोई दो: {", ".join(ss)} (1+1) [2]'))
            else:
                c = r.choice(ss)
                parts.append((f'{Q(c)} किस शब्द का पर्यायवाची है?', h, f'{h} [1]'))
        return hcompose(r, r.choice(['पर्यायवाची शब्दों पर आधारित प्रश्नों के उत्तर दीजिए।', 'निर्देशानुसार उत्तर लिखिए।']), parts, k=(2, 3, 4))

    if c4:
        @t.add('C4', (2, 3, 4, 5), 'multi_step')
        def py_c4(r, D):
            m = mk('C4', D)
            gs = r.sample(groups, 3 + (D >= 4))
            ws = ', '.join(Q(h) for h, _ in gs)
            stem = (f'{ws} — इन शब्दों के दो-दो पर्यायवाची लिखिए। फिर {r.choice(["वर्षा ऋतु", "सुबह की सैर", "समुद्र-तट की एक शाम", "पहाड़ों की यात्रा"])} पर लगभग {40 + 15 * D} शब्दों का अनुच्छेद लिखिए '
                    f'जिसमें मूल शब्दों के स्थान पर उनके पर्यायवाची प्रयुक्त हों। बताइए कि पर्यायवाची के प्रयोग से भाषा पर क्या प्रभाव पड़ा।')
            ans = ' '.join(f'{h}: {", ".join(ss[:2])}।' for h, ss in gs) + ' अनुच्छेद में पर्यायवाची का प्रसंगानुकूल प्रयोग; प्रभाव — दोहराव से बचाव, भाषा में विविधता और काव्यात्मकता।'
            key = f'प्रत्येक शब्द के दो सही पर्यायवाची (1-1 अंक तक); अनुच्छेद में सही प्रयोग; प्रभाव का स्पष्टीकरण (1)। [{m}]'
            return item(stem, ans, key, m, 'multi_step')


def vilom(t, pairs, c4=True):
    words = [a for a, b in pairs] + [b for a, b in pairs]
    opp = {}
    for a, b in pairs:
        opp[a] = b
        opp[b] = a

    @t.add('C1', (1, 2, 3))
    def vl_c1(r, D):
        a, b = r.choice(pairs)
        if r.random() < 0.5:
            a, b = b, a
        ds = r.sample([w for w in words if w not in (a, b)], 3)
        return mq(r, r.choice([f'{Q(a)} का विलोम शब्द है', f'{Q(a)} का सही विलोम चुनिए।', f'इनमें से कौन-सा शब्द {Q(a)} का विलोम है?']), b, ds, f'{a} × {b}।')

    @t.add('C2', (1, 2, 3, 4), 'explain')
    def vl_c2(r, D):
        m = mk('C2', D)
        (a, b), (c, d) = r.sample(pairs, 2)
        p, pg = name(r)
        stem = (f'{p} ने लिखा: {Q(a)} का विलोम {Q(d)} है। ' + r.choice(['यह उत्तर सही है या गलत? सही विलोम लिखिए', 'उत्तर की जाँच कीजिए और सुधार कीजिए'])
                + (' और दोनों विलोम शब्दों का प्रयोग करते हुए एक वाक्य बनाइए।' if m >= 2 else '। उत्तर संक्षेप में दीजिए।'))
        ans = f'गलत। {Q(a)} का विलोम {Q(b)} है; {Q(d)} तो {Q(c)} का विलोम है।'
        return item(stem, ans, 'गलत बताना और सही विलोम (1)' + ('; दोनों शब्दों वाला शुद्ध, सार्थक वाक्य (1)' if m >= 2 else '') + ('; वाक्य में विरोध का भाव स्पष्ट (1)' if m >= 3 else ''), m, 'explain')

    @t.add('C3', (1, 2, 3, 4, 5), 'short')
    def vl_c3(r, D):
        parts = []
        for a, b in r.sample(pairs, 4):
            if r.random() < 0.6:
                parts.append((f'{Q(a)} का विलोम लिखिए।', b, f'{b} [1]'))
            else:
                parts.append((f'{Q(a)} और उसके विलोम शब्द का प्रयोग करते हुए एक वाक्य बनाइए।', f'विलोम {b}; उदाहरण: ऐसा वाक्य जिसमें {a} और {b} दोनों का सार्थक प्रयोग हो।', f'सही विलोम (1); सार्थक वाक्य (1) [2]'))
        return hcompose(r, r.choice(['विलोम शब्दों पर आधारित प्रश्न।', 'निर्देशानुसार उत्तर दीजिए।']), parts, k=(2, 3, 4))

    if c4:
        @t.add('C4', (2, 3, 4, 5), 'multi_step')
        def vl_c4(r, D):
            m = mk('C4', D)
            ps = r.sample(pairs, 3 + (D >= 4))
            stem = (', '.join(Q(a) for a, b in ps) + ' — इन शब्दों के विलोम लिखिए। फिर “' + r.choice(['जीवन में उतार-चढ़ाव', 'खेल में हार-जीत', 'शहर और गाँव', 'पुराना और नया ज़माना'])
                    + f'” विषय पर लगभग {40 + 15 * D} शब्दों का अनुच्छेद लिखिए जिसमें कम से कम तीन विलोम-युग्मों का प्रयोग हो। विलोम-युग्म रेखांकित कीजिए।')
            ans = ' '.join(f'{a} × {b}।' for a, b in ps) + ' अनुच्छेद: विषय से जुड़ा, विलोम-युग्मों का सार्थक प्रयोग।'
            return item(stem, ans, f'प्रत्येक सही विलोम (1-1 अंक तक); अनुच्छेद में तीन सही विलोम-युग्म; विषय-संगति और शुद्धता के लिए शेष अंक। [{m}]', m, 'multi_step')


def anekarth(t, bank):
    allm = [(w, mn) for w, lst in bank for mn, s in lst]

    @t.add('C1', (1, 2, 3))
    def an_c1(r, D):
        w, lst = r.choice(bank)
        mn, s = r.choice(lst)
        own = [x for x, _ in lst if x != mn]
        ds = own + r.sample([x for ww, x in allm if ww != w], 3 - len(own) if len(own) < 3 else 0)
        return mq(r, f'वाक्य {Q(s)} में {Q(w)} शब्द किस अर्थ में प्रयुक्त हुआ है?', mn, ds[:3], f'प्रसंग से स्पष्ट है कि यहाँ {Q(w)} = {mn}।')

    @t.add('C1', (1, 2, 3))
    def an_c1b(r, D):
        w, lst = r.choice(bank)
        goods = [x for x, _ in lst]
        pool = [x for ww, x in allm if ww != w and x not in goods]
        if len(goods) >= 3:
            odd = r.choice(pool)
            opts = r.sample(goods, 3) + [odd]
            r.shuffle(opts)
            return {'stem': f'इनमें से कौन-सा {Q(w)} शब्द का अर्थ नहीं है?', 'options': opts, 'answer': odd, 'marks': 1,
                    'key': f'सही उत्तर: {odd}। {Q(w)} के अर्थ: {", ".join(goods)}। [1]'}
        return mq(r, f'{Q(w)} एक अनेकार्थी शब्द है। इनमें से कौन-सा उसका एक अर्थ है?', r.choice(goods), r.sample(pool, 3), f'{Q(w)} के अर्थ: {", ".join(goods)}।')

    @t.add('C2', (1, 2, 3, 4), 'explain')
    def an_c2(r, D):
        m = mk('C2', D)
        w, lst = r.choice(bank)
        a, b = r.sample(lst, 2)
        stem = f'{Q(w)} शब्द के दो अलग-अलग अर्थ लिखिए' + (' और दोनों अर्थों में उसका अलग-अलग वाक्य-प्रयोग कीजिए।' if m >= 2 else '। उत्तर संक्षेप में दीजिए।')
        ans = f'{a[0]} — {a[1]} {b[0]} — {b[1]}'
        return item(stem, ans, 'दो सही अर्थ (1)' + ('; प्रत्येक अर्थ के लिए सही वाक्य (1-1)' if m >= 2 else ''), m, 'explain')

    @t.add('C3', (1, 2, 3, 4, 5), 'short')
    def an_c3(r, D):
        parts = []
        for w, lst in r.sample(bank, 4):
            mn, s = r.choice(lst)
            if r.random() < 0.6:
                parts.append((f'वाक्य {Q(s)} में {Q(w)} का अर्थ लिखिए।', mn, f'{mn} [1]'))
            else:
                parts.append((f'{Q(w)} के दो अर्थ लिखिए।', ', '.join(x for x, _ in lst[:2]), f'कोई दो अर्थ (1+1) [2]'))
        return hcompose(r, 'अनेकार्थी शब्दों पर आधारित प्रश्नों के उत्तर दीजिए।', parts, k=(2, 3, 4))

    @t.add('C4', (2, 3, 4, 5), 'multi_step')
    def an_c4(r, D):
        m = mk('C4', D)
        es = r.sample(bank, 3)
        stem = (', '.join(Q(w) for w, _ in es) + ' — प्रत्येक शब्द के दो-दो अर्थ लिखिए और हर अर्थ के लिए ऐसा वाक्य बनाइए जिससे अर्थ स्पष्ट हो जाए। अंत में बताइए कि वाक्य में अनेकार्थी शब्द का अर्थ कैसे तय होता है।')
        ans = ' '.join(f'{w}: ' + '; '.join(f'{mn} ({s})' for mn, s in lst[:2]) + '।' for w, lst in es) + ' अर्थ प्रसंग (आस-पास के शब्दों) से तय होता है।'
        return item(stem, ans, f'प्रत्येक सही अर्थ और वाक्य के लिए अंक (अधिकतम {m - 1}); प्रसंग का महत्व समझाने के लिए 1 अंक। [{m}]', m, 'multi_step')


def choose_fill(t, bank, what='योजक', c4=None):
    """bank: (sentence-with-___ and {N}, answer, note, [3 distractors])."""

    def fill(r, s):
        n, g = name(r)
        return A(s.replace('{N}', n), g)

    @t.add('C1', (1, 2, 3))
    def cf_c1(r, D):
        s, a, note, ds = r.choice(bank)
        return mq(r, f'उचित {dpl(what)} से रिक्त स्थान भरिए: {Q(fill(r, s))}', a, ds, note)

    @t.add('C2', (1, 2, 3, 4), 'explain')
    def cf_c2(r, D):
        m = mk('C2', D)
        s, a, note, ds = r.choice(bank)
        w = r.choice(ds)
        p, pg = name(r)
        stem = f'{p} ने रिक्त स्थान में {Q(w)} लिखा: {Q(fill(r, s))} यह {what} उपयुक्त क्यों नहीं है? सही {what} बताइए' + (' और कारण स्पष्ट कीजिए।' if m >= 2 else '। उत्तर संक्षेप में दीजिए।')
        return item(stem, f'सही {what}: {a}। {note}', f'सही {what} (1)' + ('; कारण — वाक्य के दो भागों का संबंध (1)' if m >= 2 else '') + ('; गलत विकल्प से अर्थ कैसे बदलता है (1)' if m >= 3 else ''), m, 'explain')

    @t.add('C3', (1, 2, 3, 4, 5), 'short')
    def cf_c3(r, D):
        parts = []
        for s, a, note, ds in r.sample(bank, 4):
            parts.append((f'रिक्त स्थान भरिए: {Q(fill(r, s))}', a, f'{a} [1]'))
        parts.append((f'{Q(r.choice(["क्योंकि", "इसलिए", "जबकि", "ताकि", "हालाँकि… फिर भी"]))} का प्रयोग करते हुए अपने शहर के बारे में एक वाक्य बनाइए।', 'कोई भी शुद्ध वाक्य जिसमें योजक का सही प्रयोग हो।', 'सही प्रयोग (1); शुद्ध वाक्य (1) [2]'))
        return hcompose(r, f'{dpl(what)} पर आधारित प्रश्नों के उत्तर दीजिए।', parts, k=(2, 3, 4))

    if c4:
        t.add('C4', (2, 3, 4, 5), 'multi_step')(c4)


# =========================================================== literary frames (poems, extracts)

GLOSS_POOL = []
BHAV_POOL = []
TITLE_POOL = []


def poem(title, st1, st2, gloss, facts, infer, bhav, alank=(), evals=(), vy=None, tf=()):
    """A poem as a reading frame. gloss: (word, meaning, stanza); facts: (q, a, [ds], stanza); infer: (q, a, stanza);
    alank: (line, label, reason, stanza); vy: {1: व्याख्या of stanza 1, 2: …}. stanza 0 = whole poem."""
    for w, m, s in gloss:
        GLOSS_POOL.append(m)
    BHAV_POOL.append(bhav)
    TITLE_POOL.append(title)

    def f(r):
        v = r.choice([0, 1, 2, 1, 2])
        lines = st1 + st2 if v == 0 else (st1 if v == 1 else st2)
        ok = lambda s: v == 0 or s in (0, v)
        P = {'kind': 'काव्यांश', 'text': f'कविता: {title}\n' + '\n'.join(lines)}
        P['facts'] = [(q, a, ds) for q, a, ds, s in facts if ok(s)]
        if v == 0:
            P['facts'].append(('इस कविता का मूल भाव क्या है?', bhav, others(r, [b for b in BHAV_POOL if b != bhav], bhav, 3), 'पूरी कविता इसी केंद्रीय भाव के इर्द-गिर्द रची गई है; अन्य विकल्प दूसरी कविताओं के भाव हैं।'))
            P['title'] = (title, others(r, [x for x in TITLE_POOL if x != title], title, 3))
        for ln, lab, why, s in alank:
            if ok(s):
                P['facts'].append((f'पंक्ति {Q(ln)} में कौन-सा अलंकार है?', lab, [x for x in ALANK_L if x != lab][:3], why))
        P['vocab'] = [(w, m, others(r, [x for x in GLOSS_POOL if x != m], m, 3)) for w, m, s in gloss if ok(s)]
        P['infer'] = [(q, a) for q, a, s in infer if ok(s)] + [(f'पंक्ति {Q(ln)} में प्रयुक्त अलंकार का नाम लिखकर उसे स्पष्ट कीजिए।', f'{lab}: {why}') for ln, lab, why, s in alank if ok(s)]
        P['tf'] = [(st, b, why) for st, b, why, s in tf if ok(s)]
        P['points'] = [bhav]
        ev = [(q, a) for q, a in evals]
        if vy and v in vy:
            ev.append(('इस काव्यांश की प्रसंग सहित व्याख्या कीजिए (प्रसंग, व्याख्या और काव्य-सौंदर्य/विशेष लिखिए)।', vy[v]))
        P['eval'] = ev
        return P
    return f


def ex(kind, text, facts=(), vocab=(), tf=(), infer=(), title=None, points=(), evals=(), notes=None, views=()):
    P = {'kind': kind, 'text': text, 'facts': list(facts), 'vocab': list(vocab), 'tf': list(tf), 'infer': list(infer),
         'points': list(points), 'eval': list(evals)}
    if title:
        P['title'] = title
    if notes:
        P['notes'] = notes
    if views:
        P['views'] = list(views)
    return P


def money(r, lo, hi, step=10):
    return r.randrange(lo, hi + 1, step)


def num_ds(r, a, spread=None, k=3, unit=''):
    spread = spread or max(2, abs(a) // 4 or 2)
    out = []
    while len(out) < k:
        d = a + r.choice([-1, 1]) * r.randint(1, spread)
        if d > 0 and d != a and f'{d}{unit}' not in out:
            out.append(f'{d}{unit}')
    return out


def gv(g, m, f):
    return f if g == 'f' else m


# =========================================================== G8 · पाठ 1 कविता — देशप्रेम

P_DESH = [
    poem('मेरी माटी',
         ['मेरी माटी, मेरा गौरव, इसकी गंध निराली है,', 'खेतों में लहराती फसलें, हर डाली हरियाली है।',
          'सीमा पर जो जाग रहे हैं, उनको शीश झुकाता हूँ,', 'उनके साहस की गाथा मैं गीतों में दोहराता हूँ।'],
         ['भाषा, वेश अलग हों चाहे, मन तो सबका एक रहे,', 'रंग-बिरंगे फूलों जैसा, देश हमारा नेक रहे।',
          'दूर बसूँ मैं किसी नगर में, याद तुम्हारी आएगी,', 'मातृभूमि, तेरी ममता ही मुझको राह दिखाएगी।'],
         [('गौरव', 'गर्व, सम्मान', 1), ('निराली', 'अनोखी', 1), ('शीश', 'सिर', 1), ('गाथा', 'कथा, यशगान', 1), ('वेश', 'पहनावा', 2), ('नेक', 'भला, अच्छा', 2), ('ममता', 'माँ जैसा स्नेह', 2)],
         [('कवि किसके आगे शीश झुकाता है?', 'सीमा पर जागने वाले सैनिकों के आगे', ['खेतों के किसानों के आगे', 'अपने शिक्षकों के आगे', 'नगर के लोगों के आगे'], 1),
          ('कवि अपने गीतों में क्या दोहराता है?', 'सैनिकों के साहस की गाथा', ['खेतों की हरियाली', 'नगर की याद', 'फूलों के रंग'], 1),
          ('कवि ने देश की तुलना किससे की है?', 'रंग-बिरंगे फूलों से', ['ऊँचे पर्वत से', 'बहती नदी से', 'सुनहरी फसल से'], 2),
          ('दूर रहने पर कवि को कौन राह दिखाएगी?', 'मातृभूमि की ममता', ['सैनिकों का साहस', 'गीतों की गाथा', 'खेतों की हरियाली'], 2)],
         [('“भाषा, वेश अलग हों चाहे, मन तो सबका एक रहे” — इस पंक्ति का भाव स्पष्ट कीजिए।', 'देश में लोगों की भाषाएँ और पहनावे अलग-अलग हो सकते हैं, पर सबके मन में एकता और भाईचारा होना चाहिए — विविधता में एकता।', 2),
          ('“सीमा पर जो जाग रहे हैं” — इससे कवि का क्या आशय है?', 'सैनिक जो रात-दिन सजग रहकर देश की सीमाओं की रक्षा करते हैं, ताकि देशवासी सुरक्षित रहें।', 1),
          ('कवि को अपनी माटी पर गर्व क्यों है? दो कारण लिखिए।', 'उसकी गंध अनोखी है, खेतों में फसलें लहराती हैं और चारों ओर हरियाली है; उस पर रक्षा करने वाले वीर सैनिक हैं।', 1)],
         'देश की मिट्टी पर गर्व, सैनिकों के प्रति सम्मान, विविधता में एकता और दूर रहकर भी मातृभूमि से जुड़ाव।',
         [('रंग-बिरंगे फूलों जैसा, देश हमारा नेक रहे।', 'उपमा अलंकार', 'देश की तुलना रंग-बिरंगे फूलों से “जैसा” वाचक शब्द द्वारा की गई है।', 2),
          ('मेरी माटी, मेरा गौरव, इसकी गंध निराली है,', 'अनुप्रास अलंकार', '“म” वर्ण की आवृत्ति (मेरी, माटी, मेरा) है।', 1)],
         [('विदेश में रहने वाले भारतीयों के लिए इस कविता की अंतिम दो पंक्तियाँ कितनी सार्थक हैं? अपने विचार उदाहरण सहित लिखिए।',
           'सार्थक हैं — दूर रहकर भी लोग त्योहार, भाषा, भोजन और परिवार के माध्यम से मातृभूमि से जुड़े रहते हैं; मातृभूमि की यादें और संस्कार उन्हें कठिन समय में सहारा और दिशा देते हैं।')],
         {1: 'प्रसंग: यह अंश “मेरी माटी” कविता से है, जिसमें कवि मातृभूमि के प्रति प्रेम प्रकट करता है। व्याख्या: कवि कहता है कि उसकी माटी उसका गौरव है, उसकी गंध अनोखी है और खेतों में फसलें लहराती हैं। वह सीमा पर जागकर रक्षा करने वाले सैनिकों को सिर झुकाकर प्रणाम करता है और उनके साहस को अपने गीतों में गाता है। विशेष: “म” वर्ण की आवृत्ति में अनुप्रास; सरल, प्रवाहपूर्ण खड़ी बोली; देशप्रेम का भाव।',
          2: 'प्रसंग: “मेरी माटी” कविता का अंश, जिसमें एकता और मातृभूमि से जुड़ाव का भाव है। व्याख्या: भाषा और वेश भले अलग हों, सबका मन एक होना चाहिए; देश रंग-बिरंगे फूलों जैसा सुंदर और भला बना रहे। कवि कहता है कि वह किसी भी नगर में बसे, मातृभूमि की याद आएगी और उसकी ममता ही उसे राह दिखाएगी। विशेष: “फूलों जैसा” में उपमा; विविधता में एकता का संदेश; मातृभूमि का माँ के रूप में संबोधन।'},
         [('कवि केवल देश के खेतों की प्रशंसा करता है, सैनिकों की नहीं।', False, 'कवि सैनिकों को शीश झुकाता है और उनके साहस की गाथा गाता है।', 1),
          ('कवि चाहता है कि सबका मन एक रहे।', True, '“मन तो सबका एक रहे” — यही कवि की कामना है।', 2)]),
    poem('तिरंगा',
         ['ऊँचा-ऊँचा लहर-लहरकर, कहता हमसे प्यारा झंडा,', 'केसरिया है त्याग सिखाता, साहस का है न्यारा झंडा।',
          'श्वेत रंग में शांति बसी है, सच की राह दिखाता है,', 'हरा रंग खेतों की खुशबू, धरती से जुड़वाता है।'],
         ['बीच चक्र जो घूम रहा है, कहता — आगे बढ़ना है,', 'मिल-जुलकर, मेहनत के बल पर, नई ऊँचाई चढ़ना है।',
          'इसकी शान न घटने देंगे, यह प्रण आज उठाते हैं,', 'हम बच्चे भारत माता के, मिलकर शीश झुकाते हैं।'],
         [('न्यारा', 'अनोखा, निराला', 1), ('श्वेत', 'सफ़ेद', 1), ('प्रण', 'प्रतिज्ञा, संकल्प', 2), ('शान', 'मान-प्रतिष्ठा', 2), ('चक्र', 'पहिया', 2)],
         [('कविता के अनुसार केसरिया रंग क्या सिखाता है?', 'त्याग और साहस', ['शांति और सत्य', 'खेती और हरियाली', 'प्रगति और गति'], 1),
          ('श्वेत रंग में क्या बसा है?', 'शांति', ['त्याग', 'साहस', 'खुशबू'], 1),
          ('हरा रंग किससे जोड़ता है?', 'धरती (खेतों) से', ['आकाश से', 'सीमा से', 'सागर से'], 1),
          ('घूमता हुआ चक्र क्या संदेश देता है?', 'आगे बढ़ते रहना है', ['रुककर आराम करना है', 'पीछे लौट जाना है', 'अकेले चलना है'], 2),
          ('बच्चे क्या प्रण उठाते हैं?', 'तिरंगे की शान न घटने देने का', ['नया झंडा बनाने का', 'खेत जोतने का', 'सीमा पर जाने का'], 2)],
         [('“बीच चक्र जो घूम रहा है, कहता — आगे बढ़ना है” — इस पंक्ति का भाव लिखिए।', 'चक्र गति और प्रगति का प्रतीक है; यह संदेश देता है कि देश को निरंतर, मिल-जुलकर और मेहनत से आगे बढ़ना है।', 2),
          ('कविता में तिरंगे के तीनों रंगों के क्या-क्या अर्थ बताए गए हैं?', 'केसरिया — त्याग और साहस; श्वेत — शांति और सत्य; हरा — खेतों की खुशबू, धरती से जुड़ाव (हरियाली)।', 1)],
         'तिरंगे के रंगों और चक्र के संदेश द्वारा त्याग, शांति, सत्य, प्रगति और एकता की प्रेरणा तथा झंडे की शान बनाए रखने का संकल्प।',
         [('ऊँचा-ऊँचा लहर-लहरकर, कहता हमसे प्यारा झंडा,', 'मानवीकरण अलंकार', 'झंडे पर “कहने” जैसी मानवीय क्रिया का आरोप है।', 1)],
         [('आप अपने विद्यालय में तिरंगे की शान बनाए रखने के लिए क्या-क्या कर सकते हैं? कविता के संदेश से जोड़कर लिखिए।',
           'उदाहरण: अनुशासन और सत्य का पालन, मिल-जुलकर काम करना, मेहनत से पढ़ाई, राष्ट्रीय पर्वों पर ध्वज-संहिता का सम्मान — कविता के त्याग, शांति, प्रगति और एकता के संदेश से जोड़कर।')],
         {1: 'प्रसंग: “तिरंगा” कविता में कवि झंडे के रंगों का संदेश बताता है। व्याख्या: लहराता हुआ झंडा मानो हमसे बात करता है — केसरिया रंग त्याग और साहस सिखाता है, श्वेत रंग में शांति है और वह सच की राह दिखाता है, हरा रंग खेतों की खुशबू लिए हमें धरती से जोड़ता है। विशेष: झंडे का मानवीकरण; “ऊँचा-ऊँचा”, “लहर-लहरकर” में पुनरुक्ति; प्रतीकात्मक भाषा।',
          2: 'प्रसंग: “तिरंगा” कविता का अंतिम अंश। व्याख्या: झंडे के बीच का चक्र आगे बढ़ने का संदेश देता है — मिल-जुलकर और मेहनत से नई ऊँचाइयाँ छूनी हैं। बच्चे प्रण लेते हैं कि झंडे की शान कभी नहीं घटने देंगे और भारत माता को मिलकर नमन करते हैं। विशेष: चक्र प्रगति का प्रतीक; संकल्प का भाव; सरल खड़ी बोली।'},
         [('कविता के अनुसार हरा रंग शांति का प्रतीक है।', False, 'कविता में शांति श्वेत रंग में बसी है; हरा रंग खेतों/धरती से जोड़ता है।', 1)]),
    poem('सरहद का दीया',
         ['बर्फ़ीली चोटी पर बैठा, एक सिपाही गाता है,', 'ठिठुरी रातों में भी उसका मन न कभी घबराता है।',
          'घर की चिट्ठी पढ़-पढ़कर वह, धीरे से मुस्काता है,', 'माँ की बातें याद करे तो, आँसू भी पी जाता है।'],
         ['उसकी आँखों में सपना है — गाँव, खेत, खलिहानों का,', 'उसके कंधों पर ज़िम्मा है, लाखों-लाख मकानों का।',
          'हम निश्चिंत सोएँ घर में, वह दीया-सा जलता है,', 'उसके दम से ही भारत का, हर उत्सव चलता है।'],
         [('ठिठुरी', 'ठंड से सिकुड़ी हुई', 1), ('मुस्काना', 'मुस्कुराना', 1), ('खलिहान', 'वह स्थान जहाँ फसल का अनाज निकाला जाता है', 2), ('ज़िम्मा', 'उत्तरदायित्व', 2), ('निश्चिंत', 'बिना चिंता के', 2), ('दम', 'बल, साहस', 2)],
         [('सिपाही कहाँ बैठा है?', 'बर्फ़ीली चोटी पर', ['गाँव के खेत में', 'घर के आँगन में', 'नदी के किनारे'], 1),
          ('चिट्ठी पढ़कर सिपाही क्या करता है?', 'धीरे से मुस्काता है', ['ज़ोर से रोता है', 'गीत लिखता है', 'घर लौट जाता है'], 1),
          ('सिपाही के कंधों पर किसका ज़िम्मा है?', 'लाखों-लाख मकानों (देशवासियों) की रक्षा का', ['गाँव के खेतों का', 'माँ की चिट्ठियों का', 'उत्सवों के आयोजन का'], 2),
          ('कवि ने सिपाही की तुलना किससे की है?', 'जलते दीये से', ['बहती नदी से', 'ऊँचे पेड़ से', 'चमकते तारे से'], 2)],
         [('“आँसू भी पी जाता है” — इसका आशय स्पष्ट कीजिए।', 'माँ की याद आने पर सिपाही दुखी होता है, पर अपने कर्तव्य के कारण वह अपना दुख छिपा लेता है और कमज़ोर नहीं पड़ता।', 1),
          ('“वह दीया-सा जलता है” — सिपाही को दीये के समान क्यों कहा गया है?', 'जैसे दीया स्वयं जलकर अँधेरा दूर करता है, वैसे ही सिपाही कठिनाइयाँ सहकर देशवासियों को सुरक्षा और निश्चिंतता देता है।', 2),
          ('“उसके दम से ही भारत का, हर उत्सव चलता है” — इस पंक्ति का भाव लिखिए।', 'सैनिकों की रक्षा के कारण ही देश सुरक्षित है और लोग शांति से अपने त्योहार-उत्सव मना पाते हैं।', 2)],
         'सीमा पर कठिन परिस्थितियों में डटे सिपाही के त्याग, कर्तव्य-भावना और भावनाओं का चित्रण, जिसके कारण देशवासी सुरक्षित रहते हैं।',
         [('हम निश्चिंत सोएँ घर में, वह दीया-सा जलता है,', 'उपमा अलंकार', 'सिपाही की तुलना दीये से “सा” वाचक शब्द द्वारा की गई है।', 2)],
         [('सैनिकों के प्रति अपना आभार हम किन-किन तरीकों से प्रकट कर सकते हैं? कविता के आधार पर तर्क सहित लिखिए।',
           'उदाहरण: उन्हें पत्र/शुभकामनाएँ भेजना, उनके परिवारों का सम्मान और सहायता, राष्ट्रीय पर्वों पर उन्हें याद करना, अनुशासित और जिम्मेदार नागरिक बनना — क्योंकि कविता बताती है कि उनके त्याग से ही हमारा जीवन सुरक्षित है।')],
         {1: 'प्रसंग: “सरहद का दीया” कविता में सीमा पर तैनात सिपाही का चित्र है। व्याख्या: बर्फ़ीली चोटी पर बैठा सिपाही ठिठुरती रातों में भी गाता है और घबराता नहीं। घर की चिट्ठी पढ़कर वह मुस्कुराता है, पर माँ की याद आने पर अपना दुख भीतर ही पी जाता है। विशेष: “पढ़-पढ़कर” में पुनरुक्ति; “आँसू पी जाना” मुहावरे का सुंदर प्रयोग; करुण और वीर भाव।',
          2: 'प्रसंग: “सरहद का दीया” कविता का दूसरा अंश। व्याख्या: सिपाही की आँखों में अपने गाँव और खेतों का सपना है, पर उसके कंधों पर लाखों घरों की रक्षा का दायित्व है। हम घरों में निश्चिंत सोते हैं जबकि वह दीये की तरह जलता है; उसी के बल पर देश के उत्सव चलते हैं। विशेष: “दीया-सा” में उपमा; त्याग और कृतज्ञता का भाव।'},
         [('सिपाही ठंडी रातों में घबरा जाता है।', False, 'कविता कहती है — “उसका मन न कभी घबराता है”।', 1)]),
    poem('जन्मभूमि की पुकार',
         ['सात समंदर पार बसा हूँ, फिर भी मन में देश बसा,', 'माँ की लोरी, दादी के किस्से, मेरा हर परिवेश बसा।',
          'जब भी सुनता ढोलक की धुन, पाँव थिरकने लगते हैं,', 'दीवाली के दीप यहाँ भी, मन में जगने लगते हैं।'],
         ['भाषा मेरी, मेरी पहचान, इसे न कभी भुलाऊँगा,', 'अपने बच्चों को भी इसके, मीठे बोल सिखाऊँगा।',
          'जहाँ रहूँ, जिस देश रहूँ, मैं उसका भी सम्मान करूँ,', 'पर अपनी जन्मभूमि पर, जीवन भर अभिमान करूँ।'],
         [('परिवेश', 'आस-पास का वातावरण', 1), ('थिरकना', 'नाचना, झूमना', 1), ('लोरी', 'बच्चे को सुलाने के लिए गाया जाने वाला गीत', 1), ('पहचान', 'अस्मिता, अपनी विशेषता', 2), ('अभिमान', 'गर्व', 2)],
         [('कवि कहाँ बसा है?', 'सात समंदर पार (विदेश में)', ['अपने गाँव में', 'सीमा पर', 'पहाड़ों पर'], 1),
          ('ढोलक की धुन सुनकर क्या होता है?', 'पाँव थिरकने लगते हैं', ['आँखें भीग जाती हैं', 'नींद आ जाती है', 'मन उदास हो जाता है'], 1),
          ('कवि अपने बच्चों को क्या सिखाना चाहता है?', 'अपनी भाषा के मीठे बोल', ['ढोलक बजाना', 'विदेशी गीत', 'दीये बनाना'], 2),
          ('कवि जिस देश में रहता है, उसके प्रति उसका क्या भाव है?', 'वह उसका भी सम्मान करता है', ['वह उसे पसंद नहीं करता', 'वह उसे छोड़ना चाहता है', 'वह उससे डरता है'], 2)],
         [('“भाषा मेरी, मेरी पहचान” — कवि भाषा को अपनी पहचान क्यों मानता है?', 'भाषा से ही व्यक्ति अपनी संस्कृति, परिवार और जड़ों से जुड़ा रहता है; विदेश में रहते हुए भी भाषा उसे बताती है कि वह कौन है।', 2),
          ('कवि विदेश में रहकर भी अपने देश से कैसे जुड़ा है? दो उदाहरण दीजिए।', 'माँ की लोरी और दादी के किस्सों की यादें; ढोलक की धुन पर थिरकना; दीवाली के दीपों का मन में जगना।', 1)],
         'प्रवासी भारतीय का मातृभूमि, भाषा और संस्कृति से अटूट लगाव, तथा जिस देश में वह रहता है उसके प्रति सम्मान का संतुलित भाव।',
         [],
         [('कवि कहता है कि वह जिस देश में रहे, उसका भी सम्मान करे और जन्मभूमि पर गर्व भी करे। क्या ये दोनों भाव एक साथ संभव हैं? तर्क दीजिए।',
           'हाँ — व्यक्ति नए देश के नियमों, लोगों और संस्कृति का सम्मान करते हुए अपनी भाषा, त्योहारों और मूल्यों को सँजो सकता है; दोनों भाव एक-दूसरे के विरोधी नहीं, बल्कि व्यक्ति को उदार और जड़ों से जुड़ा बनाते हैं।')],
         {1: 'प्रसंग: “जन्मभूमि की पुकार” कविता में विदेश में बसे एक भारतीय की भावनाएँ हैं। व्याख्या: कवि सात समंदर पार रहता है, फिर भी उसके मन में देश, माँ की लोरी और दादी के किस्से बसे हैं। ढोलक की धुन सुनकर उसके पाँव थिरकते हैं और विदेश में भी दीवाली के दीप उसके मन में जग उठते हैं। विशेष: “सात समंदर पार” मुहावरेदार प्रयोग; स्मृतियों का भावपूर्ण चित्रण।',
          2: 'प्रसंग: इसी कविता का अंतिम अंश। व्याख्या: कवि संकल्प लेता है कि अपनी भाषा को, जो उसकी पहचान है, कभी नहीं भूलेगा और अपने बच्चों को भी सिखाएगा। वह जिस देश में रहे, उसका सम्मान करेगा, पर अपनी जन्मभूमि पर जीवन भर गर्व करेगा। विशेष: संतुलित दृष्टिकोण; भाषा-प्रेम का भाव; सरल प्रवाहपूर्ण भाषा।'}),
]
for _p in P_DESH:
    pass

t = topic('कविता का भाव और संदेश: देशप्रेम', 'कविता का भाव और संदेश')
reading(t, P_DESH, 'extract', c4kinds=('eval', 'summary'))
t1_1 = t

t = topic('कविता के कठिन शब्दों के अर्थ और प्रसंग सहित व्याख्या', 'प्रसंग सहित व्याख्या')
reading(t, P_DESH, 'extract', c4kinds=('eval',))
meanings(t, [('गौरव', 'गर्व, सम्मान', 'हमें अपनी संस्कृति पर गौरव है।'), ('शीश', 'सिर', 'वीरों के आगे सबने शीश झुकाया।'), ('गाथा', 'कथा, यशगान', 'दादी ने वीरों की गाथा सुनाई।'),
             ('न्यारा', 'अनोखा', 'इस गाँव का मेला सबसे न्यारा है।'), ('प्रण', 'प्रतिज्ञा', '{N} ने रोज़ व्यायाम करने का प्रण लिया।'), ('ठिठुरना', 'ठंड से काँपना/सिकुड़ना', 'पहाड़ पर रात को हम ठिठुर गए।'),
             ('निश्चिंत', 'बिना चिंता के', 'परीक्षा की तैयारी पूरी है, इसलिए {N} निश्चिंत है।'), ('परिवेश', 'आस-पास का वातावरण', 'नए परिवेश में ढलने में समय लगता है।'),
             ('अभिमान', 'गर्व', 'हमें अपनी मातृभाषा पर अभिमान है।'), ('ममता', 'माँ जैसा स्नेह', 'नानी की ममता सबको बाँध लेती है।')], c4=False)
t1_2 = t

t = topic('व्याकरण: संज्ञा और सर्वनाम के भेद', 'संज्ञा और सर्वनाम')
tagbank(t, SANGYA, SANGYA_L, 'संज्ञा का भेद', SANGYA_DEF)
tagbank(t, SARV, SARV_L, 'सर्वनाम का भेद', SARV_DEF, c3=False, c4=False)
xform(t, BHAV_X, 'भाववाचक संज्ञा बनाइए', label='भाववाचक संज्ञा-निर्माण', c4=False)
xform(t, SARV_X, 'दोहराई गई संज्ञा के स्थान पर उपयुक्त सर्वनाम लगाकर वाक्य फिर से लिखिए', label='सर्वनाम-प्रयोग', c3=False, c4=False)
t1_3 = t

# अपठित पद्यांश — the unseen poems (written for this bank, not taught in any lesson here)
P_UNSEEN = [
    poem('किताबें',
         ['किताबें चुपके से कहती हैं, आओ, हमसे बात करो,', 'दुनिया भर की सैर कराएँ, बस पन्नों पर हाथ धरो।',
          'इनमें राजा-रानी मिलते, इनमें तारे, सागर हैं,', 'इनमें बीते युग के किस्से, ज्ञान भरे सब आखर हैं।'],
         ['जो इनसे दोस्ती कर लेता, कभी अकेला होता ना,', 'इनके संग जो जागा करता, अज्ञान में सोता ना।',
          'मोबाइल की चमक-दमक में, इनको भूल न जाना तुम,', 'रोज़ किसी पन्ने से मिलकर, कुछ नया सीख आना तुम।'],
         [('आखर', 'अक्षर', 1), ('युग', 'लंबा काल, ज़माना', 1), ('धरो', 'रखो', 1), ('संग', 'साथ', 2), ('चमक-दमक', 'दिखावटी चमक', 2)],
         [('किताबें क्या करने को कहती हैं?', 'उनसे बात करने को', ['उन्हें बेचने को', 'उन्हें सजाने को', 'उन्हें छिपाने को'], 1),
          ('किताबों में किसके किस्से हैं?', 'बीते युग के', ['केवल राजाओं के', 'आने वाले कल के', 'मोबाइल के'], 1),
          ('किताबों से दोस्ती करने वाला कैसा नहीं होता?', 'अकेला', ['खुश', 'ज्ञानी', 'जागरूक'], 2),
          ('कवि किसकी चमक-दमक में किताबें न भूलने को कहता है?', 'मोबाइल की', ['बाज़ार की', 'तारों की', 'सागर की'], 2)],
         [('“किताबें चुपके से कहती हैं” — किताबें कैसे बोल सकती हैं? स्पष्ट कीजिए।', 'किताबें सचमुच नहीं बोलतीं; कवि ने उनका मानवीकरण किया है — पढ़ने पर उनके विचार और कहानियाँ पाठक से बात करते-से लगते हैं।', 1),
          ('“अज्ञान में सोता ना” का क्या अर्थ है?', 'जो किताबें पढ़ता है, वह अज्ञानी नहीं रहता; उसका मन जागरूक और ज्ञान से भरा रहता है।', 2)],
         'किताबें सच्ची मित्र हैं जो दुनिया की सैर कराती हैं और ज्ञान देती हैं; मोबाइल के युग में भी रोज़ पढ़ने की आदत बनाए रखनी चाहिए।',
         [('किताबें चुपके से कहती हैं, आओ, हमसे बात करो,', 'मानवीकरण अलंकार', 'किताबों पर कहने जैसी मानवीय क्रिया का आरोप है।', 1)],
         [('क्या आज के डिजिटल युग में भी छपी किताबें पढ़ना ज़रूरी है? कविता के आधार पर अपने विचार लिखिए।', 'कोई भी तर्कसंगत पक्ष: किताबें एकाग्रता, कल्पना और गहरा ज्ञान देती हैं; डिजिटल माध्यम सुविधाजनक हैं पर ध्यान भटकाते हैं; संतुलन आवश्यक — कविता का संदेश रोज़ पढ़ना।')]),
    poem('पेड़ की पुकार',
         ['मैं पेड़ खड़ा हूँ बरसों से, तुमको छाया देता हूँ,', 'धूप, धुआँ सब सह लेता हूँ, ताज़ी साँसें देता हूँ।',
          'चिड़ियों का मैं घर हूँ प्यारा, गिलहरी मेरी सखी है,', 'मेरी डाली पर झूले की, यादें तुमने रखी हैं।'],
         ['फिर क्यों मुझ पर आरी चलती, क्यों मेरी डाली टूटे,', 'मुझसे ही तो जुड़ी साँस है, कहीं न यह नाता छूटे।',
          'एक पेड़ जो आज लगाओ, कल वह बाग बनेगा,', 'हरी-भरी धरती का सपना, सबका साथ बनेगा।'],
         [('सखी', 'सहेली, मित्र', 1), ('आरी', 'लकड़ी काटने का दाँतेदार औज़ार', 2), ('नाता', 'संबंध, रिश्ता', 2), ('बाग', 'बगीचा', 2)],
         [('पेड़ हमें क्या-क्या देता है?', 'छाया और ताज़ी साँसें (शुद्ध हवा)', ['केवल लकड़ी', 'केवल फल', 'धुआँ और धूप'], 1),
          ('पेड़ किसका घर है?', 'चिड़ियों का', ['मछलियों का', 'बादलों का', 'आरी का'], 1),
          ('पेड़ किस बात से दुखी है?', 'उस पर आरी चलने (कटाई) से', ['धूप से', 'चिड़ियों से', 'झूले से'], 2),
          ('आज लगाया एक पेड़ कल क्या बनेगा?', 'बाग', ['जंगल की आग', 'सड़क', 'मकान'], 2)],
         [('“मुझसे ही तो जुड़ी साँस है” — पेड़ ऐसा क्यों कहता है?', 'पेड़ ऑक्सीजन (शुद्ध वायु) देते हैं; उनके बिना मनुष्य का जीवन संभव नहीं, इसलिए हमारी साँसें उनसे जुड़ी हैं।', 2),
          ('पेड़ अपनी पीड़ा किस प्रकार व्यक्त करता है?', 'वह पूछता है कि उसकी सेवा के बदले उस पर आरी क्यों चलती है और उसकी डालियाँ क्यों तोड़ी जाती हैं।', 2)],
         'पेड़ मनुष्य को छाया, शुद्ध हवा और यादें देते हैं, फिर भी काटे जाते हैं; हमें पेड़ बचाने और नए पेड़ लगाने चाहिए।',
         [('मैं पेड़ खड़ा हूँ बरसों से, तुमको छाया देता हूँ,', 'मानवीकरण अलंकार', 'पेड़ स्वयं मनुष्य की तरह बोल रहा है और अपनी बात कह रहा है।', 1)],
         [('अपने मोहल्ले में पेड़ बचाने के लिए आप कौन-से तीन कदम उठाएँगे? कविता के संदेश से जोड़कर लिखिए।', 'उदाहरण: वृक्षारोपण अभियान, पेड़ों की देखभाल की ज़िम्मेदारी बाँटना, कटाई के विरोध में पत्र/जागरूकता — पेड़ों और मनुष्य के “नाते” को बचाने के लिए।')]),
]

t = topic('अपठित पद्यांश: प्रश्नों के उत्तर', 'अपठित पद्यांश')
reading(t, P_UNSEEN, 'read', c4kinds=('eval', 'summary'))
t1_4 = t
CHAPTERS[1] = [t1_1, t1_2, t1_3, t1_4]


# =========================================================== G8 · पाठ 2 कहानी — पारिवारिक संबंध

def ex_chashma(r):
    n, g = name(r)
    gp = r.choice(['दादी', 'नानी'])
    par = r.choice(['पापा', 'मम्मी'])
    amt = money(r, 150, 400)
    cost = money(r, 60, amt - 40)
    thing, tg = r.choice([('साइकिल की घंटी', 'f'), ('क्रिकेट का बल्ला', 'm'), ('नई पेंसिल-पेटी', 'f'), ('खिलौना-गाड़ी', 'f')])
    text = A(f'{n} की {gp} का चश्मा पिछले हफ़्ते टूट गया था। {par} ने कहा था, “अगले महीने नया बनवा देंगे, इस महीने खर्च बहुत हो गया है।” {gp} ने कुछ नहीं कहा। '
             f'पर {n} ने देखा कि {gp} ने अख़बार पढ़ना छोड़ दिया है और शाम को खिड़की के पास बैठकर चुपचाप बाहर देखती रहती हैं। '
             f'एक दिन {n} ने अपनी गुल्लक तोड़ी। उसमें {amt} रुपये निकले। वह सीधे चश्मे की दुकान पर पहुँच{{ा}} और दुकानदार से बोल{{ा}}, “मेरी {gp} का चश्मा ठीक कर दीजिए। पैसे कम पड़ें तो मैं {gv(tg, "अपना", "अपनी")} {thing} भी बेच दूँग{{ा}}।” '
             f'दुकानदार मुस्कुराया। उसने टूटी कमानी बदल दी और केवल {cost} रुपये लिए। '
             f'उस शाम {gp} ने फिर से अख़बार उठाया। पढ़ते-पढ़ते उन्होंने {n} के सिर पर हाथ फेरा और धीरे से कहा, “चश्मा तो अब ठीक हुआ, पर आँखें आज भीग गईं।”', g)
    return ex('गद्यांश', text,
              facts=[(f'{n} की गुल्लक से कितने रुपये निकले?', f'{amt} रुपये', num_ds(r, amt, 60, unit=' रुपये')),
                     (f'दुकानदार ने चश्मा ठीक करने के कितने रुपये लिए?', f'{cost} रुपये', num_ds(r, cost, 40, unit=' रुपये')),
                     (f'चश्मा टूटने के बाद {gp} ने क्या पढ़ना छोड़ दिया था?', 'अख़बार', ['कहानियाँ', 'चिट्ठियाँ', 'धार्मिक पुस्तकें']),
                     (f'{par} ने नया चश्मा कब बनवाने की बात कही थी?', 'अगले महीने', ['अगले हफ़्ते', 'उसी दिन', 'अगले साल']),
                     (f'चश्मा ठीक होने के बाद {n} के पास कितने रुपये बचे?', f'{amt - cost} रुपये', num_ds(r, amt - cost, 30, unit=' रुपये'))],
              vocab=[('कमानी', 'चश्मे का वह भाग जो कान पर टिकता है', ['चश्मे का शीशा', 'चश्मे का डिब्बा', 'आँख की दवा']),
                     ('गुल्लक', 'पैसे जमा करने का छोटा पात्र', ['पढ़ने की मेज़', 'खिलौनों का डिब्बा', 'बटुआ']),
                     ('भीगना', 'गीला होना (यहाँ — आँसू आ जाना)', ['सूख जाना', 'थक जाना', 'चमक जाना'])],
              tf=[(f'दुकानदार ने पूरे {amt} रुपये ले लिए।', False, f'उसने केवल {cost} रुपये लिए।'),
                  (f'{gp} ने चश्मा टूटने की शिकायत बार-बार की।', False, f'{gp} ने कुछ नहीं कहा, वे चुप रहीं।'),
                  (A(f'{n} ने अपनी गुल्लक के पैसों से चश्मा ठीक करवाया।', g), True, 'गुल्लक तोड़कर वह दुकान पर गया/गई और चश्मा ठीक करवाया।')],
              infer=[(f'{gp} चुप क्यों रहीं? अनुमान लगाइए।', f'वे घर के खर्च की स्थिति समझती थीं और {par} पर बोझ नहीं डालना चाहती थीं — उनका स्वाभिमान और समझदारी।'),
                     (f'“पर आँखें आज भीग गईं” — {gp} की आँखें क्यों भीग गईं?', f'{n} के प्रेम और त्याग को देखकर वे भावुक हो गईं; ये खुशी और कृतज्ञता के आँसू थे।'),
                     (f'{n} के चरित्र की दो विशेषताएँ पाठ के आधार पर लिखिए।', f'संवेदनशील — {gp} की चुप्पी और उदासी समझी; त्यागी/उदार — अपनी गुल्लक के पैसे और प्रिय वस्तु तक देने को तैयार।'),
                     ('दुकानदार ने केवल थोड़े पैसे क्यों लिए होंगे?', 'बच्चे के प्रेम और भोलेपन से प्रभावित होकर; उसने केवल कमानी बदली, नया चश्मा नहीं बनाया।')],
              title=(f'{gp} का चश्मा', ['चश्मे की दुकान', f'{par} का खर्च', 'टूटी गुल्लक का दुख']),
              points=[f'{gp} का चश्मा टूटा', f'{par} ने खर्च के कारण बात टाली', f'{gp} उदास रहने लगीं', f'{n} ने गुल्लक तोड़ी', 'दुकानदार ने कम पैसे लिए', f'{gp} भावुक हो गईं'],
              evals=[(A(f'क्या {n} को घर में बताए बिना गुल्लक तोड़नी चाहिए थी? अपना मत तर्क सहित लिखिए।', g), 'कोई भी तर्कसंगत मत: प्रेम और संवेदना सराहनीय है; पर बड़ों को बताना भी उचित होता — दोनों पक्षों पर विचार।'),
                     ('यह कहानी परिवार के संबंधों के बारे में क्या संदेश देती है?', 'परिवार में एक-दूसरे की अनकही ज़रूरतें समझना, त्याग और प्रेम संबंधों को मज़बूत बनाते हैं; बड़े-बूढ़ों का ध्यान रखना हमारा कर्तव्य है।')])


def ex_bhai(r):
    n, g = name(r)
    b, _ = name(r, 'm')
    if b == n:
        return None
    call = gv(g, 'भैया', 'दीदी')
    k = r.randint(4, 7)
    tot = r.choice([50, 80, 100])
    got = r.randint(int(tot * 0.6), int(tot * 0.9))
    subj = r.choice([('भिन्न', 'रोटी, केक और पिज़्ज़ा के टुकड़ों'), ('दशमलव', 'रुपये-पैसे और नाप-तौल'), ('प्रतिशत', 'क्रिकेट के स्कोर और दुकान की छूट')])
    text = A(f'{n} का छोटा भाई {b} गणित से बहुत डरता था। परीक्षा से एक सप्ताह पहले वह रोने लगा, “मुझसे {subj[0]} के सवाल कभी नहीं होंगे।” '
             f'{n} उस समय अपने विद्यालय की नाटक-प्रतियोगिता की तैयारी कर रह{{ा}} थ{{ा}}। उसने कुछ देर सोचा, फिर नाटक का अभ्यास {k} दिनों के लिए छोड़ दिया। '
             f'हर शाम वह {b} के साथ बैठत{{ा}} और {subj[1]} के उदाहरणों से {subj[0]} समझात{{ा}}। धीरे-धीरे {b} हँसने लगा — “{call}, गणित तो खेल जैसा मज़ेदार है!” '
             f'परीक्षा में {b} को {tot} में से {got} अंक मिले। नाटक में {n} को मुख्य भूमिका नहीं मिली, पर उसे इस बात का ज़रा भी दुख नहीं था।', g)
    return ex('गद्यांश', text,
              facts=[(f'{b} किस विषय से डरता था?', 'गणित', ['विज्ञान', 'हिंदी', 'इतिहास']),
                     (f'{n} किसकी तैयारी कर रह{A("{ा}", g)} थ{A("{ा}", g)}?', 'नाटक-प्रतियोगिता की', ['खेल-प्रतियोगिता की', 'गणित की परीक्षा की', 'चित्रकला प्रदर्शनी की']),
                     (f'{n} ने नाटक का अभ्यास कितने दिनों के लिए छोड़ा?', f'{k} दिन', num_ds(r, k, 2, unit=' दिन')),
                     (f'परीक्षा में {b} को कितने अंक मिले?', f'{tot} में से {got}', [f'{tot} में से {x}' for x in num_ds(r, got, 8)]),
                     (f'{n} ने {subj[0]} समझाने के लिए किसके उदाहरण लिए?', subj[1], [x[1] for x in [('', 'रोटी, केक और पिज़्ज़ा के टुकड़ों'), ('', 'रुपये-पैसे और नाप-तौल'), ('', 'क्रिकेट के स्कोर और दुकान की छूट'), ('', 'पेड़ों और पत्तियों')] if x[1] != subj[1]][:3])],
              vocab=[('अभ्यास', 'बार-बार करके सीखना (रिहर्सल)', ['आराम', 'प्रतियोगिता', 'पुरस्कार']),
                     ('मुख्य भूमिका', 'नाटक का सबसे प्रमुख पात्र', ['नाटक का मंच', 'नाटक का निर्देशक', 'नाटक का दर्शक'])],
              tf=[(f'{b} को परीक्षा में पूरे अंक मिले।', False, f'उसे {tot} में से {got} अंक मिले।'),
                  (A(f'मुख्य भूमिका न मिलने पर {n} बहुत दुखी हु{{या}}।', g), False, 'उसे ज़रा भी दुख नहीं था।')],
              infer=[(A(f'मुख्य भूमिका न मिलने पर भी {n} दुखी क्यों नहीं थ{{ा}}?', g), 'उसके लिए भाई की खुशी और सफलता अपनी उपलब्धि से अधिक महत्वपूर्ण थी; उसे संतोष था कि उसका त्याग सफल हुआ।'),
                     (f'{n} ने रोज़मर्रा की चीज़ों के उदाहरण क्यों दिए होंगे?', 'ताकि कठिन विषय ठोस और रोचक उदाहरणों से समझ में आए और भाई का डर कम हो।'),
                     (f'{n} के चरित्र की दो विशेषताएँ बताइए।', 'त्यागी — अपना अभ्यास छोड़ दिया; धैर्यवान और समझदार — रोज़ शाम धीरे-धीरे, रोचक ढंग से पढ़ाया।')],
              title=(f'{call} की पाठशाला', ['नाटक-प्रतियोगिता', 'गणित की परीक्षा का परिणाम', 'मुख्य भूमिका की खोज']),
              points=[f'{b} गणित से डरता था', f'{n} नाटक की तैयारी में व्यस्त था/थी', 'अभ्यास छोड़कर भाई को पढ़ाया', 'रोचक उदाहरणों से डर दूर हुआ', 'भाई को अच्छे अंक मिले', 'मुख्य भूमिका न मिलने का दुख नहीं'],
              evals=[('क्या अपने लक्ष्य को छोड़कर किसी और की सहायता करना सदा सही होता है? कहानी के आधार पर अपने विचार लिखिए।', 'संतुलित उत्तर: परिवार के लिए त्याग मूल्यवान है, पर अपनी ज़िम्मेदारियों का संतुलन भी आवश्यक है; कहानी में भाई की ज़रूरत अधिक तात्कालिक थी।')])


def ex_videocall(r):
    n, g = name(r)
    c, _ = city(r, abroad=True)
    mo = r.randint(3, 9)
    cnt = r.choice(['सौ', 'अस्सी', 'साठ', 'नब्बे'])
    gp = r.choice([('दादाजी', 'तालाब', 'तालाब'), ('नानाजी', 'नदी के घाट', 'नदी का घाट'), ('दादाजी', 'आम के बाग', 'आम का बाग')])
    text = A(f'जब {n} का परिवार {c} रहने आया, तो उसे सबसे ज़्यादा याद {gp[0]} की आती थी। गाँव में हर सुबह {gp[0]} उसे साइकिल पर बिठाकर {gp[1]} तक ले जाते थे। '
             f'यहाँ ऊँची इमारतें थीं, पर कहीं {gp[1]} जैसा कुछ नहीं था। एक दिन {n} ने {gp[0]} को वीडियो-कॉल किया और रो पड़{{ा}}। '
             f'{gp[0]} हँसे, “अरे, {gp[2]} नहीं है तो क्या, आसमान तो वही है! शाम को बालकनी में खड़े होकर सूरज डूबते देखना और मुझे बताना कि आज कौन-सा रंग सबसे गहरा था।” '
             f'उस दिन से हर शाम {n} आसमान के रंग गिनत{{ा}} और रात को {gp[0]} को सुनात{{ा}}। {mo} महीने बाद जब {gp[0]} {c} आए, तो {n} ने उन्हें अपनी कॉपी दिखाई — उसमें {cnt} से ज़्यादा सूर्यास्तों के चित्र थे।', g)
    return ex('गद्यांश', text,
              facts=[(f'{n} का परिवार कहाँ रहने आया?', c, others(r, [x for x, k in CITIES if k != 'भारत'], c)),
                     (f'गाँव में {gp[0]} {n} को कहाँ ले जाते थे?', f'{gp[1]} तक', [f'{x} तक' for x in ['बाज़ार', 'मंदिर', 'खेतों', 'तालाब', 'नदी के घाट', 'आम के बाग'] if x != gp[1]][:3]),
                     (f'{gp[0]} ने {n} को शाम को क्या करने को कहा?', 'सूर्यास्त देखकर सबसे गहरा रंग बताने को', ['बालकनी में पौधे लगाने को', 'गाँव लौट आने को', 'रोज़ साइकिल चलाने को']),
                     (f'{gp[0]} कितने महीने बाद {c} आए?', f'{mo} महीने', num_ds(r, mo, 3, unit=' महीने')),
                     (f'{n} की कॉपी में क्या था?', 'सूर्यास्तों के चित्र', ['गाँव की तस्वीरें', 'इमारतों के नक्शे', 'वीडियो-कॉल के नोट्स'])],
              vocab=[('बालकनी', 'घर का बाहर निकला हुआ खुला भाग', ['घर की छत', 'सीढ़ी', 'रसोई']), ('सूर्यास्त', 'सूरज का डूबना', ['सूरज का निकलना', 'दोपहर', 'चाँदनी रात'])],
              tf=[(f'{c} में भी {gp[1]} जैसा स्थान था।', False, f'वहाँ ऊँची इमारतें थीं, {gp[1]} जैसा कुछ नहीं था।'), (f'{gp[0]} वीडियो-कॉल पर हँसे।', True, f'“{gp[0]} हँसे” — पाठ में स्पष्ट लिखा है।')],
              infer=[(f'{gp[0]} ने “आसमान तो वही है” क्यों कहा?', 'यह समझाने के लिए कि दूरी होने पर भी कुछ चीज़ें दोनों को जोड़ती हैं; नई जगह में भी खुशी और सुंदरता खोजी जा सकती है।'),
                     (f'{gp[0]} के स्वभाव की दो विशेषताएँ लिखिए।', 'स्नेही — पोते/पोती की भावनाएँ समझते हैं; समझदार/रचनात्मक — उदासी दूर करने का नया उपाय सुझाते हैं; आशावादी।'),
                     (f'सूर्यास्त के रंग गिनने की आदत ने {n} की कैसे मदद की?', 'नई जगह से जुड़ाव बना, उदासी कम हुई और दादा/नाना से रोज़ बात का बहाना मिला; रिश्ता दूरी में भी जीवित रहा।')],
              title=('आसमान तो वही है', [f'{c} की इमारतें', 'साइकिल की सवारी', 'नई कॉपी']),
              points=['परिवार विदेश गया', f'{n} को {gp[0]} की याद', 'वीडियो-कॉल पर रोना', 'सूर्यास्त देखने का सुझाव', 'रोज़ रंग गिनना और सुनाना', 'चित्रों से भरी कॉपी'],
              evals=[('यह कहानी दूर रहने वाले परिवार के सदस्यों के संबंधों के बारे में क्या बताती है? अपने अनुभव से जोड़कर लिखिए।', 'तकनीक और रचनात्मक आदतें दूरी को कम कर सकती हैं; स्नेह और नियमित संपर्क से रिश्ते मज़बूत रहते हैं।')])


STORIES_FAM = [ex_chashma, ex_bhai, ex_videocall]

t = topic('कहानी का सार और पात्रों का चरित्र-चित्रण', 'कहानी का सार')
reading(t, STORIES_FAM, 'extract', c4kinds=('summary', 'eval'))
t2_1 = t

t = topic('व्याकरण: विशेषण और विशेष्य', 'विशेषण और विशेष्य')
tagbank(t, [e[:4] for e in VISH], VISH_L, 'विशेषण का भेद', VISH_DEF)


@t.add('C1', (1, 2, 3))
def g8_visheshya(r, D):
    s, w, lab, why, vs = r.choice(VISH)
    n, g = name(r)
    s = A(s.replace('{N}', n), g)
    ds = [x for x in s.rstrip('।?').split() if x not in (vs, w) and x not in w.split() and len(x) > 1][:6]
    if len(ds) < 3:
        return None
    return mq(r, f'वाक्य {Q(s)} में विशेषण {Q(w)} का विशेष्य कौन-सा है?', vs, r.sample(ds, 3), f'विशेषण जिस संज्ञा की विशेषता बताता है, वही विशेष्य है — {Q(vs)}।')


xform(t, VISH_X, 'विशेषण बनाइए', label='विशेषण-निर्माण', c4=False)
t2_2 = t


def un_water(r):
    sc = r.choice(['सरस्वती विद्यालय', 'ज्ञानदीप स्कूल', 'नवोदय पब्लिक स्कूल', 'आदर्श विद्यालय'])
    c = r.choice(INDIA)
    tanks = r.randint(2, 6)
    lit = r.choice([5000, 8000, 10000, 12000])
    month = r.choice(['जुलाई', 'अगस्त', 'सितंबर'])
    pct = r.choice([20, 25, 30, 40])
    text = (f'{c} के {sc} में पिछले साल पानी की भारी कमी हो गई थी। गर्मियों में नल सूख गए और पानी के टैंकर मँगवाने पड़े। तब विद्यार्थियों ने मिलकर “वर्षा-जल संचयन” की योजना बनाई। '
            f'छत से बहने वाले बारिश के पानी को पाइपों द्वारा {tanks} बड़ी टंकियों में जमा किया जाने लगा। हर टंकी में लगभग {lit} लीटर पानी भरता है। '
            f'{month} तक सभी टंकियाँ भर गईं। अब इस पानी से बगीचे के पौधे सींचे जाते हैं और शौचालयों में भी इसका उपयोग होता है। इससे विद्यालय का पानी का बिल लगभग {pct} प्रतिशत कम हो गया है। '
            f'प्रधानाचार्य कहती हैं, “पानी बचाना केवल सरकार का काम नहीं, हम सबका कर्तव्य है।”')
    total = tanks * lit
    return ex('गद्यांश', text,
              facts=[('विद्यार्थियों ने कौन-सी योजना बनाई?', 'वर्षा-जल संचयन', ['वृक्षारोपण', 'सौर ऊर्जा', 'कचरा प्रबंधन']),
                     ('बारिश का पानी कितनी टंकियों में जमा किया जाता है?', str(tanks), num_ds(r, tanks, 2)),
                     ('सभी टंकियाँ कब तक भर गईं?', month, others(r, MONTHS, month)),
                     ('पानी का बिल लगभग कितना कम हुआ?', f'{pct} प्रतिशत', [f'{x} प्रतिशत' for x in [10, 15, 20, 25, 30, 40, 50] if x != pct][:3]),
                     ('सभी टंकियाँ भरने पर कुल कितना पानी जमा होता है?', f'{total} लीटर', num_ds(r, total, lit, unit=' लीटर'))],
              vocab=[('संचयन', 'इकट्ठा करना, जमा करना', ['बर्बाद करना', 'बाँटना', 'बेचना']), ('कर्तव्य', 'करने योग्य काम, ज़िम्मेदारी', ['अधिकार', 'शौक', 'इनाम'])],
              tf=[('टंकियों का पानी पीने के लिए प्रयोग होता है।', False, 'पाठ के अनुसार इससे पौधे सींचे जाते हैं और शौचालयों में उपयोग होता है।'),
                  ('पिछले साल विद्यालय में पानी के टैंकर मँगवाने पड़े।', True, 'गर्मियों में नल सूख गए थे, इसलिए टैंकर मँगवाने पड़े।')],
              infer=[('प्रधानाचार्य के कथन का क्या अर्थ है?', 'पानी बचाने की ज़िम्मेदारी हर व्यक्ति की है; केवल सरकार पर निर्भर रहना ठीक नहीं।'),
                     ('इस योजना से विद्यालय को कौन-से दो लाभ हुए?', 'पानी की कमी दूर हुई (पौधों/शौचालयों के लिए पानी), और पानी का बिल कम हुआ।')],
              title=('बूँद-बूँद की बचत', ['गर्मियों की छुट्टियाँ', 'विद्यालय का बगीचा', 'पानी का बिल']),
              points=['पानी की कमी की समस्या', 'वर्षा-जल संचयन की योजना', f'{tanks} टंकियों में जमा', 'पौधों और शौचालयों में उपयोग', f'बिल {pct}% कम', 'पानी बचाना सबका कर्तव्य'],
              evals=[('आप अपने घर में पानी बचाने के लिए कौन-से तीन उपाय अपनाएँगे? पाठ से प्रेरणा लेकर लिखिए।', 'उदाहरण: नल बंद रखना/टपकते नल ठीक कराना, बाल्टी से नहाना, पौधों को सुबह-शाम सींचना, आरओ का बचा पानी पोंछे में प्रयोग।')],
              notes={'समस्या': ['गर्मियों में नल सूखे', 'टैंकर मँगवाने पड़े'], 'समाधान': ['छत का पानी पाइपों से टंकियों में', f'{tanks} टंकियाँ, हर एक में {lit} लीटर'], 'लाभ': ['पौधों की सिंचाई', 'शौचालयों में उपयोग', f'बिल {pct}% कम']})


def un_library(r):
    n, g = name(r)
    c = r.choice(INDIA)
    books = r.choice([300, 450, 500, 600, 750])
    days = r.choice(['शनिवार', 'रविवार'])
    hrs = r.choice([('सुबह 9 बजे', 'दोपहर 1 बजे', 4), ('सुबह 10 बजे', 'दोपहर 2 बजे', 4), ('शाम 4 बजे', 'शाम 7 बजे', 3)])
    text = A(f'{c} की एक तंग गली में रहने वाल{{े}} {n} ने देखा कि मोहल्ले के बच्चे छुट्टियों में दिन भर मोबाइल पर खेलते रहते हैं। उसने सोचा, क्यों न एक छोटा-सा पुस्तकालय बनाया जाए? '
             f'पहले उसने अपनी पुरानी किताबें दान कीं, फिर पड़ोसियों से किताबें माँगीं। देखते-देखते {books} किताबें इकट्ठी हो गईं। मोहल्ले के मंदिर के पास एक खाली कमरा मिल गया। '
             f'अब हर {days} {hrs[0]} से {hrs[1]} तक यह पुस्तकालय खुलता है। बच्चे यहाँ कहानियाँ पढ़ते हैं, चित्र बनाते हैं और बड़े बच्चे छोटों को पढ़कर सुनाते हैं। '
             f'{n} कहत{{ा}} है, “किताब हाथ में हो तो कोई भी बच्चा अकेला नहीं रहता।”', g)
    return ex('गद्यांश', text,
              facts=[(f'{n} ने पुस्तकालय बनाने का विचार क्यों किया?', 'बच्चे छुट्टियों में दिन भर मोबाइल पर खेलते रहते थे', ['विद्यालय में पुस्तकालय नहीं था', 'उसे किताबें बेचनी थीं', 'मंदिर का कमरा खाली था']),
                     ('कुल कितनी किताबें इकट्ठी हुईं?', str(books), num_ds(r, books, 150)),
                     ('पुस्तकालय कहाँ खोला गया?', 'मंदिर के पास एक खाली कमरे में', ['विद्यालय के भवन में', f'{n} के घर की छत पर', 'बाज़ार की एक दुकान में']),
                     ('पुस्तकालय सप्ताह में किस दिन खुलता है?', days, others(r, WEEKDAYS, days)),
                     ('पुस्तकालय एक दिन में कितने घंटे खुलता है?', f'{hrs[2]} घंटे', num_ds(r, hrs[2], 2, unit=' घंटे'))],
              vocab=[('दान', 'बिना बदले में कुछ लिए दे देना', ['उधार', 'बेचना', 'छिपाना']), ('तंग', 'सँकरी, पतली', ['चौड़ी', 'लंबी', 'साफ़'])],
              tf=[('पुस्तकालय रोज़ खुलता है।', False, f'यह केवल हर {days} खुलता है।'), (A(f'{n} ने सबसे पहले अपनी पुरानी किताबें दान कीं।', g), True, 'पाठ में “पहले उसने अपनी पुरानी किताबें दान कीं” लिखा है।')],
              infer=[(f'{n} के कथन “किताब हाथ में हो तो कोई भी बच्चा अकेला नहीं रहता” का आशय स्पष्ट कीजिए।', 'किताबें मित्र की तरह साथ देती हैं; उनकी कहानियाँ और ज्ञान बच्चे का मन लगाए रखते हैं।'),
                     (f'इस घटना से {n} के बारे में क्या पता चलता है?', 'वह समाज के प्रति जागरूक, पहल करने वाला/वाली और दूसरों को साथ जोड़ने वाला/वाली व्यक्ति है।')],
              title=('गली का पुस्तकालय', ['मोबाइल के खेल', 'मंदिर का कमरा', 'छुट्टियों की यात्रा']),
              points=['बच्चे मोबाइल में व्यस्त', 'पुस्तकालय का विचार', 'किताबें दान और इकट्ठी', 'मंदिर के पास कमरा', 'साप्ताहिक गतिविधियाँ', 'किताबें सच्ची मित्र'],
              evals=[('क्या मोहल्ले के ऐसे पुस्तकालय मोबाइल की आदत कम कर सकते हैं? अपने विचार तर्क सहित लिखिए।', 'कोई भी तर्कसंगत पक्ष: रोचक गतिविधियाँ और साथी मिलने से आदत कम हो सकती है; पर घर पर नियम और बड़ों का उदाहरण भी ज़रूरी।')],
              notes={'समस्या': ['बच्चे दिन भर मोबाइल पर'], 'कदम': ['अपनी किताबें दान', 'पड़ोसियों से किताबें', 'मंदिर के पास कमरा'], 'गतिविधियाँ': ['कहानियाँ पढ़ना', 'चित्र बनाना', 'बड़े बच्चे छोटों को पढ़कर सुनाते हैं']})


def un_plastic(r):
    c = r.choice(INDIA)
    shops = r.randint(40, 120)
    bags = r.choice([2000, 3000, 5000])
    wk = r.randint(3, 8)
    price = r.choice([10, 15, 20])
    text = (f'{c} के एक पुराने बाज़ार में हर दिन हज़ारों प्लास्टिक की थैलियाँ इस्तेमाल होती थीं। ये थैलियाँ नालियों में फँस जातीं और बरसात में सड़कें पानी से भर जातीं। '
            f'तब बाज़ार के व्यापारियों और पास के विद्यालय के विद्यार्थियों ने मिलकर “थैला लाओ” अभियान शुरू किया। विद्यार्थियों ने पुराने कपड़ों से {bags} थैले सिले और '
            f'{shops} दुकानों पर रखे। ग्राहक केवल {price} रुपये में थैला ले सकते हैं और अगली बार लौटाने पर पूरे पैसे वापस मिलते हैं। '
            f'{wk} सप्ताह में ही बाज़ार की नालियाँ साफ़ दिखने लगीं। एक बुज़ुर्ग फल-विक्रेता ने कहा, “पहले लगता था कि छोटी-सी थैली से क्या फ़र्क पड़ता है, अब समझ आया कि बूँद-बूँद से ही घड़ा भरता है।”')
    return ex('गद्यांश', text,
              facts=[('प्लास्टिक की थैलियों से क्या समस्या होती थी?', 'नालियाँ बंद हो जातीं और बरसात में सड़कें पानी से भर जातीं', ['दुकानों में आग लग जाती', 'फल जल्दी सड़ जाते', 'ग्राहक कम आते']),
                     ('विद्यार्थियों ने थैले किससे बनाए?', 'पुराने कपड़ों से', ['काग़ज़ से', 'जूट की बोरियों से', 'प्लास्टिक से']),
                     ('थैले कितनी दुकानों पर रखे गए?', str(shops), num_ds(r, shops, 20)),
                     ('एक थैले की कीमत कितनी है?', f'{price} रुपये', [f'{x} रुपये' for x in [5, 10, 15, 20, 25, 30] if x != price][:3]),
                     ('कितने सप्ताह में नालियाँ साफ़ दिखने लगीं?', f'{wk} सप्ताह', num_ds(r, wk, 2, unit=' सप्ताह'))],
              vocab=[('अभियान', 'किसी उद्देश्य के लिए चलाया गया संगठित प्रयास', ['त्योहार', 'प्रतियोगिता', 'व्यापार']), ('बुज़ुर्ग', 'बूढ़ा, वृद्ध', ['युवा', 'बालक', 'अमीर'])],
              tf=[('ग्राहक को थैला लौटाने पर पैसे वापस नहीं मिलते।', False, 'लौटाने पर पूरे पैसे वापस मिलते हैं।'), ('अभियान में व्यापारी और विद्यार्थी दोनों शामिल थे।', True, 'व्यापारियों और विद्यार्थियों ने मिलकर अभियान शुरू किया।')],
              infer=[('फल-विक्रेता ने “बूँद-बूँद से ही घड़ा भरता है” क्यों कहा?', 'उसे समझ आया कि हर व्यक्ति का छोटा प्रयास (एक थैली न लेना) मिलकर बड़ा बदलाव लाता है।'),
                     ('पैसे लौटाने वाली व्यवस्था क्यों रखी गई होगी?', 'ताकि लोग थैले बार-बार प्रयोग करें और लौटाएँ; ग्राहकों पर बोझ न पड़े और थैले बेकार न जाएँ।')],
              title=('थैला लाओ, बाज़ार बचाओ', ['बरसात का मौसम', 'फल-विक्रेता की दुकान', 'पुराने कपड़ों की सिलाई']),
              points=['थैलियों से नालियाँ बंद', '“थैला लाओ” अभियान', 'पुराने कपड़ों से थैले', 'थैला लौटाने पर पैसे वापस', 'नालियाँ साफ़ हुईं', 'छोटे प्रयासों का बड़ा असर'],
              evals=[('क्या प्लास्टिक पर पूरी तरह प्रतिबंध लगाना ही एकमात्र उपाय है? पाठ के आधार पर अपना मत लिखिए।', 'संतुलित उत्तर: प्रतिबंध के साथ विकल्प (कपड़े के थैले), जागरूकता और प्रोत्साहन आवश्यक; पाठ दिखाता है कि सामुदायिक प्रयास से भी बदलाव संभव।')],
              notes={'समस्या': ['थैलियाँ नालियों में फँसतीं', 'बरसात में सड़कों पर पानी'], 'अभियान': ['कपड़े के थैले', f'{price} रुपये, लौटाने पर वापसी'], 'परिणाम': [f'{wk} सप्ताह में नालियाँ साफ़', 'लोगों की सोच बदली']})


UNSEEN_PROSE = [un_water, un_library, un_plastic]

t = topic('अपठित गद्यांश: तथ्यात्मक और अनुमान आधारित प्रश्न', 'अपठित गद्यांश')
reading(t, UNSEEN_PROSE, 'read', c4kinds=('notes', 'summary', 'eval'))
t2_3 = t

# ---------------------------------------------------------------- रचना: अनौपचारिक पत्र
LETTER_FACTS = [
    ('अनौपचारिक पत्र किसे लिखा जाता है?', 'परिवार के सदस्यों, मित्रों और परिचितों को', ['प्रधानाचार्य को', 'समाचार-पत्र के संपादक को', 'किसी कंपनी के प्रबंधक को'], 'अनौपचारिक पत्र निजी संबंधों वाले लोगों को लिखे जाते हैं।'),
    ('बड़ों को लिखे अनौपचारिक पत्र में संबोधन के बाद क्या लिखा जाता है?', 'सादर प्रणाम / सादर चरण-स्पर्श', ['सेवा में', 'विषय', 'भवदीय'], 'बड़ों के लिए अभिवादन “सादर प्रणाम” आदि होता है।'),
    ('मित्र को लिखे पत्र के अंत में प्रायः क्या लिखा जाता है?', 'तुम्हारा मित्र / तुम्हारी सखी', ['भवदीय', 'प्रार्थी', 'आपका आज्ञाकारी शिष्य'], 'अनौपचारिक पत्र में समापन आत्मीय होता है।'),
    ('अनौपचारिक पत्र में सबसे ऊपर बाईं ओर क्या लिखा जाता है?', 'भेजने वाले का पता और तिथि', ['विषय', 'पाने वाले का पद', 'हस्ताक्षर'], 'पत्र के आरंभ में प्रेषक का पता और तिथि लिखी जाती है।'),
    ('इनमें से कौन-सा अनौपचारिक पत्र का विषय नहीं होगा?', 'नगर निगम से सड़क की मरम्मत की माँग', ['मित्र को जन्मदिन की बधाई', 'दादी को छुट्टियों का हाल', 'भाई को परीक्षा के लिए शुभकामनाएँ'], 'शिकायत/माँग औपचारिक पत्र का विषय है।'),
    ('छोटों को लिखे पत्र में अभिवादन के लिए कौन-सा शब्द उपयुक्त है?', 'शुभाशीर्वाद / ढेर सारा प्यार', ['सादर प्रणाम', 'सेवा में', 'महोदय'], 'छोटों को आशीर्वाद दिया जाता है।'),
]
LETTER_FLAWS = [
    ('प्रिय दादीजी, सेवा में निवेदन है कि मैं यहाँ कुशल हूँ।', '“सेवा में निवेदन है” औपचारिक भाषा है, दादी को लिखे पत्र में अनुचित है।', 'प्रिय दादीजी, सादर प्रणाम। मैं यहाँ कुशल हूँ और आशा करत{ा} हूँ कि आप भी स्वस्थ होंगी।'),
    ('प्रिय मित्र, भवदीय, {N}', 'मित्र को लिखे पत्र में “भवदीय” जैसा औपचारिक समापन उचित नहीं है।', 'तुम्हारा प्रिय मित्र / तुम्हारी सखी, {N}'),
    ('पूज्य पिताजी, तुम कैसे हो? तुमने मेरा पत्र पढ़ा या नहीं?', 'पिताजी के लिए “तुम” के स्थान पर आदरसूचक “आप” होना चाहिए।', 'पूज्य पिताजी, सादर प्रणाम। आप कैसे हैं? आशा है आपको मेरा पिछला पत्र मिल गया होगा।'),
    ('प्रिय अनु, मैं ठीक हूँ। बाकी सब ठीक है। और क्या लिखूँ। ठीक है।', 'पत्र में विषय-वस्तु का विस्तार नहीं है; बातें दोहराई गई हैं और कोई ठोस समाचार नहीं है।', 'प्रिय अनु, मैं ठीक हूँ। पिछले सप्ताह हमारे विद्यालय में विज्ञान-मेला हुआ, जिसमें मेरे मॉडल को दूसरा स्थान मिला…'),
    ('प्रिय भाई, विषय: जन्मदिन की बधाई हेतु।', 'अनौपचारिक पत्र में “विषय” पंक्ति नहीं लिखी जाती।', 'प्रिय भाई, ढेर सारा प्यार। जन्मदिन की बहुत-बहुत बधाई!'),
]


def lt_task(r):
    n, g = name(r)
    rc = r.choice([('मित्र', 'प्रिय'), ('दादी', 'पूज्य'), ('चचेरे भाई', 'प्रिय'), ('मौसी', 'आदरणीय'), ('छोटी बहन', 'प्रिय')])
    c, _ = city(r)
    sit = r.choice([
        (f'आप हाल ही में अपने परिवार के साथ {c} घूमकर आए हैं। अपने {rc[0]} को पत्र लिखकर यात्रा का अनुभव बताइए।',
         ['आप कहाँ गए और किसके साथ', 'वहाँ सबसे अच्छा क्या लगा', 'कोई मज़ेदार या अनोखी घटना', 'उन्हें अगली बार साथ चलने का निमंत्रण'],
         'यात्रा का स्थान और साथी; दर्शनीय स्थल/भोजन का वर्णन; एक रोचक घटना; आत्मीय निमंत्रण; उचित संबोधन और समापन।'),
        (f'आपके विद्यालय में वार्षिक उत्सव हुआ जिसमें आपने भाग लिया। अपने {rc[0]} को पत्र लिखकर इसका वर्णन कीजिए।',
         ['उत्सव कब और कहाँ हुआ', 'आपने किस कार्यक्रम में भाग लिया', 'आपको कैसा लगा', f'अपने {rc[0]} का हाल-चाल पूछना'],
         'उत्सव का विवरण; अपनी भूमिका; भावनाएँ (घबराहट/खुशी); हाल-चाल; आत्मीय शैली।'),
        (f'आपको नई साइकिल/किताबें उपहार में मिली हैं। उपहार भेजने वाले अपने {rc[0]} को धन्यवाद-पत्र लिखिए।',
         ['उपहार मिलने पर आपकी प्रतिक्रिया', 'आप उसका उपयोग कैसे करेंगे', 'घर के समाचार', 'मिलने की इच्छा'],
         'धन्यवाद और खुशी; उपयोग की योजना; पारिवारिक समाचार; आत्मीय समापन।'),
        (f'आपका {rc[0]} परीक्षा को लेकर बहुत घबराया हुआ है। उसे पत्र लिखकर हिम्मत बँधाइए और सुझाव दीजिए।' if rc[0] in ('मित्र', 'चचेरे भाई') else f'आप छुट्टियों में {rc[0]} के घर जाना चाहते हैं। उन्हें पत्र लिखकर अपनी योजना बताइए।',
         ['पत्र लिखने का कारण', 'दो-तीन व्यावहारिक सुझाव या योजना की बातें', 'अपना कोई अनुभव', 'शुभकामनाएँ'],
         'कारण स्पष्ट; सुझाव/योजना; व्यक्तिगत अनुभव; शुभकामनाएँ; संबंध के अनुसार भाषा।'),
    ])
    return {'task': sit[0], 'bullets': sit[1], 'ind': f'प्रारूप: प्रेषक का पता, तिथि, संबोधन ({rc[1]} {rc[0]}), अभिवादन, मुख्य भाग, समापन और नाम। ' + sit[2],
            'model': f'मॉडल आरंभ: {c}, 12 अगस्त। {rc[1]} {rc[0]}, सादर प्रणाम/ढेर सारा प्यार। … समापन: आपका/तुम्हारा … {n}। मुख्य भाग में सभी बिंदु आत्मीय भाषा में।'}


def lt_short(r, D):
    s, prob, fix = r.choice(LETTER_FLAWS)
    n, g = name(r)
    return (f'अनौपचारिक पत्र के इस अंश को सुधारकर लिखिए और बताइए कि आपने क्या बदला: {Q(A(s.replace("{N}", n), g))}', A(fix.replace('{N}', n), g) + f' ({prob})', f'शुद्ध, उपयुक्त रूप (1); बदलाव का कारण (1); भाषा की शुद्धता')


t = topic('रचना: अनौपचारिक पत्र लेखन', 'अनौपचारिक पत्र')
writing(t, 'अनौपचारिक पत्र', [lt_task], LETTER_FACTS, LETTER_FLAWS, [lt_short])
t2_4 = t
CHAPTERS[2] = [t2_1, t2_2, t2_3, t2_4]


# =========================================================== G8 · पाठ 3 संस्मरण — यादगार व्यक्ति

def mem_teacher(r):
    n, g = name(r)
    tch = r.choice(['शर्मा जी', 'वर्मा जी', 'जोशी जी', 'मिश्रा जी'])
    cls = r.choice(['पाँचवीं', 'छठी', 'सातवीं'])
    yrs = r.randint(3, 6)
    prize = r.choice([('एक नीली डायरी', 'डायरी'), ('कविताओं की एक पुरानी किताब', 'किताब'), ('हरे रंग का एक पेन', 'पेन')])
    text = A(f'आज भी जब मैं कोई कविता पढ़त{{ा}} हूँ, तो मुझे {tch} की आवाज़ सुनाई देने लगती है। {yrs} साल पहले, जब मैं {cls} कक्षा में थ{{ा}}, वे हमारे हिंदी के अध्यापक बनकर आए थे। '
             f'पहले ही दिन उन्होंने किताब बंद कर दी और खिड़की के बाहर बरसते बादलों पर एक कविता सुनाई। पूरी कक्षा चुप होकर सुनती रही। '
             f'मैं हिंदी में कमज़ोर थ{{ा}} और बोलने से डरत{{ा}} थ{{ा}}। एक दिन उन्होंने मुझे खड़ा करके चार पंक्तियाँ पढ़ने को कहा। मेरी आवाज़ काँप रही थी, पर उन्होंने बीच में टोका नहीं। '
             f'पढ़ना पूरा होते ही उन्होंने ताली बजाई और मुझे {prize[0]} दी — “इसमें रोज़ एक पंक्ति अपनी लिखना।” वह {prize[1]} आज भी मेरी मेज़ की दराज़ में है। '
             f'उन्होंने मुझे सिखाया कि गलती से डरने वाला कभी नहीं सीखता।', g)
    return ex('संस्मरण का अंश', text,
              facts=[('लेखक/लेखिका को कविता पढ़ते समय किसकी आवाज़ सुनाई देती है?', tch, others(r, ['शर्मा जी', 'वर्मा जी', 'जोशी जी', 'मिश्रा जी', 'प्रधानाचार्य जी'], tch)),
                     ('अध्यापक जब आए, तब लेखक/लेखिका किस कक्षा में थ' + gv(g, 'े', 'ीं') + '?', f'{cls} कक्षा', [f'{x} कक्षा' for x in ['चौथी', 'पाँचवीं', 'छठी', 'सातवीं', 'आठवीं'] if x != cls][:3]),
                     ('पहले दिन अध्यापक ने क्या किया?', 'बरसते बादलों पर एक कविता सुनाई', ['कठिन परीक्षा ली', 'गृहकार्य जाँचा', 'कक्षा से बाहर भेज दिया']),
                     ('अध्यापक ने उपहार में क्या दिया?', prize[0], others(r, ['एक नीली डायरी', 'कविताओं की एक पुरानी किताब', 'हरे रंग का एक पेन', 'एक शब्दकोश'], prize[0]))],
              vocab=[('टोकना', 'बीच में रोककर कुछ कहना', ['प्रशंसा करना', 'चुप रहना', 'डाँट देना']), ('दराज़', 'मेज़ का खींचने वाला खाना', ['अलमारी का दरवाज़ा', 'बस्ता', 'खिड़की'])],
              tf=[('अध्यापक ने पहले दिन किताब से पाठ पढ़ाया।', False, 'उन्होंने किताब बंद कर दी और कविता सुनाई।'),
                  ('लेखक/लेखिका की आवाज़ काँपने पर भी अध्यापक ने बीच में नहीं टोका।', True, 'पाठ में यही कहा गया है।')],
              infer=[('लेखक/लेखिका के अनुसार अध्यापक की सबसे बड़ी सीख क्या थी?', 'गलती से डरने वाला कभी नहीं सीखता — आत्मविश्वास से प्रयास करना चाहिए।'),
                     ('अध्यापक ने बीच में न टोककर क्या दिखाया?', 'उनका धैर्य और विद्यार्थी के प्रति सहानुभूति; वे उसका आत्मविश्वास बढ़ाना चाहते थे।'),
                     ('इस अंश को संस्मरण क्यों कहा जाएगा? दो विशेषताएँ बताइए।', 'लेखक अपनी स्मृति से एक वास्तविक व्यक्ति (अध्यापक) का आत्मीय चित्रण करता है; प्रथम पुरुष (“मैं”) शैली और भूतकाल का प्रयोग; भावात्मकता।')],
              title=(f'{tch} की नीली स्याही' if prize[1] == 'पेन' else f'मेरे हिंदी वाले {tch}', ['बरसात का दिन', 'मेरी परीक्षा', 'मेज़ की दराज़']),
              points=['अध्यापक की याद', 'पहले दिन कविता', 'बोलने का डर', 'बिना टोके सुनना', 'उपहार और रोज़ लिखने की सीख', 'गलती से न डरने की सीख'],
              evals=[('लेखक/लेखिका का अपने अध्यापक के प्रति क्या दृष्टिकोण है? पाठ से प्रमाण देकर लिखिए।', 'आदर, कृतज्ञता और आत्मीयता — वर्षों बाद भी उनकी आवाज़ याद आती है, उनका उपहार सँभालकर रखा है, उनकी सीख को जीवन का आधार माना है।'),
                     ('आपके जीवन में भी क्या कोई ऐसा व्यक्ति है जिसने आपका डर दूर किया? संस्मरण की शैली में चार-पाँच वाक्य लिखिए।', 'प्रथम पुरुष, भूतकाल, वास्तविक व्यक्ति, एक प्रसंग और उसका प्रभाव।')])


def mem_postman(r):
    pm = r.choice(['रघु चाचा', 'हरि काका', 'मोहन चाचा'])
    gp = r.choice(['दादी', 'नानी'])
    who = r.choice([('बुआ', 'कोलकाता'), ('मामा', 'दुबई'), ('चाचा', 'मुंबई'), ('मौसी', 'नैरोबी')])
    yrs = r.randint(8, 15)
    n, g = name(r)
    text = A(f'हमारे कस्बे के डाकिया {pm} को मैं कभी नहीं भूल सकत{{ा}}। मेरी {gp} पढ़ना नहीं जानती थीं। जब भी {who[1]} से {who[0]} की चिट्ठी आती, {pm} अपनी साइकिल बरामदे में खड़ी करते, '
             f'चश्मा नाक पर टिकाते और पूरी चिट्ठी ज़ोर-ज़ोर से पढ़कर सुनाते। कभी-कभी तो वे {gp} के कहने पर जवाब भी लिख देते। '
             f'{gp} उन्हें चाय पिलाए बिना जाने नहीं देती थीं। बारिश हो या कड़ी धूप, वे समय पर आते। एक बार वे तेज़ बुखार में भी चिट्ठी देने आए, क्योंकि उन्हें पता था कि {gp} उसका इंतज़ार कर रही हैं। '
             f'आज {yrs} साल बाद जब मैं मोबाइल पर एक पल में संदेश भेज देत{{ा}} हूँ, तब भी मुझे उस साइकिल की घंटी की आवाज़ याद आती है।', g)
    return ex('संस्मरण का अंश', text,
              facts=[('डाकिये का नाम क्या था?', pm, others(r, ['रघु चाचा', 'हरि काका', 'मोहन चाचा', 'श्याम बाबू'], pm)),
                     (f'{gp} को चिट्ठी पढ़वाने की आवश्यकता क्यों पड़ती थी?', 'वे पढ़ना नहीं जानती थीं', ['उनकी आँखें कमज़ोर थीं', 'वे व्यस्त रहती थीं', 'चिट्ठी अंग्रेज़ी में होती थी']),
                     ('चिट्ठी कहाँ से आती थी?', who[1], others(r, ['कोलकाता', 'दुबई', 'मुंबई', 'नैरोबी', 'लंदन'], who[1])),
                     (f'{gp} डाकिये को किसके बिना जाने नहीं देती थीं?', 'चाय पिलाए बिना', ['खाना खिलाए बिना', 'पैसे दिए बिना', 'धन्यवाद-पत्र दिए बिना']),
                     ('डाकिया एक बार किस हालत में भी चिट्ठी देने आया?', 'तेज़ बुखार में', ['टूटी साइकिल के साथ', 'आधी रात को', 'छुट्टी के दिन'])],
              vocab=[('कस्बा', 'गाँव से बड़ी और शहर से छोटी बस्ती', ['महानगर', 'राजधानी', 'जंगल']), ('इंतज़ार', 'प्रतीक्षा', ['शिकायत', 'जल्दबाज़ी', 'नाराज़गी'])],
              tf=[('डाकिया केवल चिट्ठी देकर तुरंत चला जाता था।', False, 'वह चिट्ठी पढ़कर सुनाता, कभी जवाब लिखता और चाय पीकर जाता।'), ('डाकिया बारिश और धूप में भी समय पर आता था।', True, 'पाठ में यही कहा गया है।')],
              infer=[('डाकिये के चरित्र की दो विशेषताएँ लिखिए।', 'कर्तव्यनिष्ठ — बुखार और मौसम की परवाह किए बिना समय पर आते; दयालु/संवेदनशील — चिट्ठी पढ़कर सुनाते और जवाब लिखते।'),
                     ('लेखक/लेखिका को आज भी साइकिल की घंटी क्यों याद आती है?', 'वह घंटी उन आत्मीय संबंधों और इंतज़ार की याद दिलाती है जो मोबाइल के तेज़ संदेशों में नहीं मिलते।')],
              title=(f'डाकिया {pm}', ['मोबाइल का ज़माना', 'बारिश का दिन', 'चाय की प्याली']),
              points=['डाकिये की याद', f'{gp} पढ़ना नहीं जानती थीं', 'चिट्ठी पढ़ना और जवाब लिखना', 'चाय और आत्मीयता', 'बुखार में भी कर्तव्य', 'आज के मोबाइल से तुलना'],
              evals=[('इस संस्मरण में लेखक/लेखिका पुराने समय और आज के समय की तुलना कैसे करता/करती है? आप किससे सहमत हैं?', 'पहले संदेश धीरे पहुँचते थे पर आत्मीयता थी; आज संदेश तुरंत पहुँचते हैं पर मानवीय जुड़ाव कम है — कोई भी तर्कसंगत मत।')])


def mem_coach(r):
    n, g = name(r)
    co = r.choice(['डिसूज़ा सर', 'गिल सर', 'नायर सर', 'खन्ना सर'])
    sport = r.choice(['क्रिकेट', 'फ़ुटबॉल', 'बैडमिंटन', 'हॉकी'])
    score = r.choice(['फ़ाइनल', 'सेमीफ़ाइनल'])
    gap = r.randint(2, 9)
    text = A(f'विद्यालय की {sport} टीम में जगह पाकर मैं बहुत खुश थ{{ा}}। हमारे कोच {co} बहुत कड़े अनुशासन वाले थे — सुबह छह बजे मैदान, और एक मिनट की देरी पर दस चक्कर! '
             f'उस साल हम ज़िले के {score} में पहुँचे, पर केवल {gap} अंकों के अंतर से हार गए। मैदान से लौटते समय मैं रो रह{{ा}} थ{{ा}}। {co} ने मेरे कंधे पर हाथ रखा और कहा, '
             f'“हारना बुरा नहीं, हार से कुछ न सीखना बुरा है। चलो, विरोधी टीम से हाथ मिलाकर आओ।” मुझे उस दिन उनका यह आदेश बहुत कठिन लगा, पर आज समझ आता है कि उन्होंने मुझे खेल से बड़ी बात सिखाई — सम्मान के साथ हारना। '
             f'अगले साल हम जीते, पर मुझे जीत से ज़्यादा वह हाथ मिलाना याद है।', g)
    return ex('संस्मरण का अंश', text,
              facts=[('लेखक/लेखिका किस खेल की टीम में थ' + gv(g, 'े', 'ीं') + '?', sport, others(r, ['क्रिकेट', 'फ़ुटबॉल', 'बैडमिंटन', 'हॉकी', 'कबड्डी'], sport)),
                     ('देरी होने पर कोच क्या सज़ा देते थे?', 'मैदान के दस चक्कर', ['खेल से बाहर करना', 'जुर्माना', 'अतिरिक्त गृहकार्य']),
                     ('टीम कितने अंकों के अंतर से हारी?', f'{gap} अंकों से', num_ds(r, gap, 3, unit=' अंकों से')),
                     ('हार के बाद कोच ने क्या करने को कहा?', 'विरोधी टीम से हाथ मिलाने को', ['घर जाकर आराम करने को', 'दोबारा मैच की माँग करने को', 'अंपायर से शिकायत करने को'])],
              vocab=[('अनुशासन', 'नियमों का पालन', ['आलस्य', 'मनमानी', 'मनोरंजन']), ('विरोधी', 'सामने वाला, प्रतिद्वंद्वी', ['सहयोगी', 'दर्शक', 'निर्णायक'])],
              tf=[('टीम उस साल फ़ाइनल/सेमीफ़ाइनल जीत गई।', False, f'टीम {gap} अंकों से हार गई; जीत अगले साल मिली।'), ('लेखक/लेखिका को कोच का आदेश उस दिन कठिन लगा।', True, '“मुझे उस दिन उनका यह आदेश बहुत कठिन लगा।”')],
              infer=[('“हारना बुरा नहीं, हार से कुछ न सीखना बुरा है” — इस कथन का आशय स्पष्ट कीजिए।', 'असफलता स्वाभाविक है; उससे सीखकर सुधार करना ही वास्तविक सफलता का मार्ग है।'),
                     ('लेखक/लेखिका को जीत से ज़्यादा हाथ मिलाना क्यों याद है?', 'उस क्षण ने खेल-भावना और सम्मान के साथ हारना सिखाया — यह सीख जीत से अधिक मूल्यवान थी।')],
              title=('सम्मान के साथ हार', [f'{sport} का मैदान', 'सुबह छह बजे', 'दस चक्कर']),
              points=['टीम में चयन', 'कोच का अनुशासन', f'{score} में हार', 'कोच की सीख', 'विरोधी से हाथ मिलाना', 'खेल-भावना की याद'],
              evals=[('कोच के कड़े अनुशासन को आप कितना उचित मानते हैं? संस्मरण के आधार पर तर्क दीजिए।', 'संतुलित उत्तर: अनुशासन से समय-पालन और मेहनत की आदत बनी; कोच संवेदनशील भी थे — हार पर सांत्वना दी; कठोरता और स्नेह का संतुलन।')])


MEMOIRS = [mem_teacher, mem_postman, mem_coach]

VIDHA_L = ['संस्मरण', 'कहानी', 'निबंध', 'यात्रा-वृत्तांत', 'एकांकी', 'आत्मकथा']
VIDHA = [
    ('मुझे आज भी याद है, जब हमारे पड़ोस वाले बाबा पहली बार हमें चिड़ियों के नाम सिखाने ले गए थे। उनकी झुर्रियों भरी मुस्कान आज भी आँखों में है।', '', 'संस्मरण', 'लेखक अपनी स्मृति से किसी दूसरे वास्तविक व्यक्ति (बाबा) का आत्मीय चित्रण कर रहा है।'),
    ('एक गाँव में रामू नाम का एक गरीब कुम्हार रहता था। एक दिन उसके चाक पर ऐसा घड़ा बना कि राजा भी देखने आ गया।', '', 'कहानी', 'कल्पित पात्र, घटना-क्रम और कथानक है।'),
    ('विज्ञान ने मानव-जीवन को सरल बना दिया है, किंतु इसके कुछ दुष्परिणाम भी हैं। इस निबंध में हम दोनों पक्षों पर विचार करेंगे।', '', 'निबंध', 'किसी विषय पर विचारों और तर्कों का क्रमबद्ध प्रस्तुतीकरण है।'),
    ('सुबह सात बजे हमारी बस पहाड़ों की ओर चल पड़ी। रास्ते भर नदी साथ-साथ बहती रही और दोपहर तक हम घाटी में पहुँच गए।', '', 'यात्रा-वृत्तांत', 'किसी यात्रा के मार्ग, स्थानों और अनुभवों का क्रमवार वर्णन है।'),
    ('(मंच पर अँधेरा। धीरे-धीरे प्रकाश होता है।) माँ: इतनी रात को कहाँ जा रहे हो? बेटा: (घबराकर) कहीं नहीं, माँ!', '', 'एकांकी', 'पात्रों के संवाद और कोष्ठक में रंग-निर्देश हैं।'),
    ('मेरा जन्म एक छोटे-से कस्बे में हुआ था। बचपन में मैं बहुत शरारती था और पढ़ाई से भागता था। आगे चलकर मेरे जीवन ने कई मोड़ लिए।', '', 'आत्मकथा', 'लेखक अपने ही जीवन की कहानी क्रम से सुना रहा है।'),
    ('हमारी पुरानी कामवाली दीदी हर दिन अपने साथ गीत लेकर आती थीं। उनके जाने के बाद घर बहुत सूना लगा — यह बात मैं कभी नहीं भूल पाई।', '', 'संस्मरण', 'लेखिका किसी वास्तविक व्यक्ति के साथ बिताए क्षणों को याद कर रही है।'),
    ('दोपहर को हम ऊँट पर बैठकर रेत के टीलों की ओर निकले। सूरज ढलते ही रेत सुनहरी हो उठी।', '', 'यात्रा-वृत्तांत', 'यात्रा में देखे दृश्यों और अनुभवों का वर्णन है।'),
    ('पर्यावरण की रक्षा केवल सरकार का नहीं, हर नागरिक का दायित्व है। पहला कारण यह है कि…', '', 'निबंध', 'विषय पर तर्कपूर्ण विचार-प्रस्तुति है।'),
    ('(दरवाज़े पर दस्तक।) दादी: कौन है? डाकिया: (बाहर से) चिट्ठी है, अम्मा!', '', 'एकांकी', 'संवाद और रंग-निर्देश नाटक की पहचान हैं।'),
]

t = topic('संस्मरण विधा की विशेषताएँ', 'संस्मरण विधा')
fx(t, 'C1', (1, 2), [
    ('संस्मरण किस पर आधारित होता है?', 'लेखक की स्मृतियों में बसे वास्तविक व्यक्ति या घटना पर', 'संस्मरण में लेखक अपनी याद के आधार पर किसी वास्तविक व्यक्ति/घटना का चित्रण करता है।', ['पूरी तरह कल्पित पात्रों पर', 'केवल वैज्ञानिक तथ्यों पर', 'मंच पर अभिनय पर']),
    ('संस्मरण प्रायः किस पुरुष (शैली) में लिखा जाता है?', 'उत्तम पुरुष (मैं) में', 'लेखक स्वयं “मैं” के रूप में अपने अनुभव बताता है।', ['मध्यम पुरुष (तुम) में', 'केवल संवाद के रूप में', 'केवल पद्य में']),
    ('संस्मरण और आत्मकथा में मुख्य अंतर क्या है?', 'संस्मरण में किसी दूसरे व्यक्ति/घटना का स्मरण होता है, आत्मकथा में लेखक अपने पूरे जीवन की कथा कहता है', 'संस्मरण का केंद्र स्मृत व्यक्ति/घटना है; आत्मकथा का केंद्र स्वयं लेखक।',
     ['दोनों में कोई अंतर नहीं होता', 'संस्मरण पद्य में और आत्मकथा गद्य में होती है', 'संस्मरण कल्पित और आत्मकथा वास्तविक होती है']),
    ('संस्मरण में सामान्यतः किस काल का अधिक प्रयोग होता है?', 'भूतकाल', 'बीती घटनाओं की याद होने के कारण।', ['भविष्यत् काल', 'केवल वर्तमान काल', 'आज्ञार्थक रूप']),
    ('इनमें से कौन-सी विशेषता संस्मरण की नहीं है?', 'काल्पनिक घटनाओं का मनगढ़ंत वर्णन', 'संस्मरण वास्तविकता पर आधारित होता है।', ['आत्मीयता और भावुकता', 'वास्तविक व्यक्ति का चित्रण', 'लेखक की स्मृतियों का प्रयोग']),
])
tagbank(t, VIDHA, VIDHA_L, 'विधा', noun='अंश', link=' की', c3=False)
MEM_WHO = {mem_teacher: 'हिंदी के अध्यापक', mem_postman: 'मोहल्ले के डाकिया', mem_coach: 'खेल के कोच'}


def mem_pick(r):
    f = r.choice(MEMOIRS)
    P = f(r)
    txt = P['text']
    fp = next((w for w in ['मैं', 'मुझे', 'मेरी', 'मेरे', 'मेरा'] if w in txt.split()), 'मैं')
    m = re.search(r'(\S+ (?:था|थी|थे))[ ।,]', txt)
    past = m.group(1) if m else 'थे'
    return P, MEM_WHO[f], fp, past


@t.add('C2', (2, 3, 4), 'short')
def mem_feat2(r, D):
    P, who, fp, past = mem_pick(r)
    m = mk('C2', D)
    stem = f'नीचे दिया गया अंश पढ़िए।\n{P["text"]}\nयह अंश संस्मरण विधा का है — इसकी पुष्टि करने वाली दो विशेषताएँ अंश से उदाहरण देकर लिखिए।'
    ans = f'(1) लेखक “{fp}” कहकर उत्तम पुरुष में अपनी स्मृति बता रहा है। (2) {who} जैसे वास्तविक व्यक्ति का आत्मीय चित्रण है; बीती घटनाएँ भूतकाल में हैं (जैसे “{past}”)।'
    return item(stem, ans, 'प्रत्येक विशेषता उदाहरण सहित (1) — उत्तम पुरुष, वास्तविक व्यक्ति का स्मरण, भूतकाल, आत्मीयता में से कोई दो' + (f'; कुल {m} अंकों तक स्पष्टता के अनुसार' if m > 2 else ''), m, 'explain')


@t.add('C3', (2, 3, 4, 5), 'short')
def mem_feat3(r, D):
    P, who, fp, past = mem_pick(r)
    parts = [
        ('यह अंश किस पुरुष (शैली) में लिखा गया है? अंश से एक शब्द उदाहरण के रूप में दीजिए।', f'उत्तम पुरुष; जैसे “{fp}”', f'उत्तम पुरुष (1/2), उदाहरण “{fp}” (1/2) [1]'),
        ('अंश में किस वास्तविक व्यक्ति का स्मरण किया गया है?', who, f'{who} [1]'),
        ('अंश में मुख्य रूप से किस काल का प्रयोग हुआ है और क्यों?', f'भूतकाल (जैसे “{past}”), क्योंकि लेखक बीती घटनाएँ याद कर रहा है', f'भूतकाल (1/2); कारण — बीती घटनाओं की स्मृति (1/2) [1]'),
        ('लेखक की भावना उस व्यक्ति के प्रति कैसी है? एक कारण दीजिए।', 'आदर और आत्मीयता की; वह उनकी सीख/व्यवहार को आज भी याद करता है', 'आदर/आत्मीयता (1/2); अंश से कारण (1/2) [1]'),
        ('यह अंश कहानी से किस प्रकार भिन्न है?', 'इसमें कल्पित कथानक नहीं, लेखक की वास्तविक स्मृतियाँ हैं', 'वास्तविक बनाम कल्पित का अंतर [1]'),
    ]
    return hcompose(r, f'नीचे दिया गया अंश पढ़कर प्रश्नों के उत्तर दीजिए।\n{P["text"]}', parts, (3,) if D < 4 else (4,), type_='short')


@t.add('C4', (3, 4, 5), 'long')
def mem_feat4(r, D):
    P, who, fp, past = mem_pick(r)
    m = mk('C4', D, True)
    stem = (f'नीचे दिया गया अंश पढ़िए।\n{P["text"]}\n'
            f'“यह अंश संस्मरण विधा की लगभग सभी विशेषताएँ दिखाता है।” — इस कथन की समीक्षा कीजिए। संस्मरण की कम-से-कम चार विशेषताओं को अंश के उदाहरणों से सिद्ध कीजिए और अंत में बताइए कि इसे आत्मकथा क्यों नहीं कहा जा सकता।')
    ans = (f'विशेषताएँ: उत्तम पुरुष (“{fp}”); वास्तविक व्यक्ति ({who}) का चित्रण; भूतकाल में बीती घटनाएँ (“{past}”); आत्मीयता और भावुकता; '
           f'लेखक पर पड़े प्रभाव/सीख का उल्लेख। आत्मकथा नहीं — क्योंकि केंद्र में लेखक का पूरा जीवन नहीं, बल्कि {who} से जुड़ी कुछ स्मृतियाँ हैं।')
    key = f'चार विशेषताएँ, प्रत्येक अंश के उदाहरण सहित (प्रति विशेषता लगभग {max(1, (m - 2) // 4)} अंक); आत्मकथा से अंतर (1); सुसंगत प्रस्तुति (1) [{m}]'
    return item(stem, ans, key, m, 'long', minutes=min(25, m * 2))


t3_1 = t

t = topic('पाठ के प्रमुख प्रसंग और लेखक का दृष्टिकोण', 'लेखक का दृष्टिकोण')
reading(t, MEMOIRS, 'extract', c4kinds=('eval', 'summary'))
t3_2 = t

t = topic('व्याकरण: क्रिया और काल (भूत, वर्तमान, भविष्य)', 'क्रिया और काल')
tagbank(t, KAAL, KAAL_L, 'काल', KAAL_DEF)
tagbank(t, [(s, w, l, why) for s, w, l, why in KRIYA], ['सकर्मक क्रिया', 'अकर्मक क्रिया'], 'क्रिया का भेद (कर्म के आधार पर)', {'सकर्मक क्रिया': 'जिस क्रिया का फल कर्म पर पड़े; “क्या/किसे” पूछने पर उत्तर मिले।', 'अकर्मक क्रिया': 'जिस क्रिया का फल कर्ता पर ही पड़े; कोई कर्म न हो।'}, c1=False, c4=False)
xform(t, KAAL_X, 'निर्देशानुसार काल-परिवर्तन कीजिए', label='काल-परिवर्तन')
t3_3 = t
CHAPTERS[3] = [t3_1, t3_2, t3_3]


# =========================================================== G8 · पाठ 4 कविता — प्रकृति चित्रण

P_PRAKRITI = [
    poem('वर्षा आई',
         ['घिर-घिर आए काले बादल, नभ में ढोल बजाते हैं,', 'प्यासी धरती के आँगन में, मोती-से बरसाते हैं।',
          'मेंढक टर्र-टर्र गाते हैं, मोर पंख फैलाता है,', 'सूखा-सा जो पेड़ खड़ा था, फिर से हरियाता है।'],
         ['नदियाँ उमड़ीं, नाले उमड़े, खेतों में भर आया पानी,', 'दादी कहतीं — “इस बरस तो, फसल उगेगी खूब सुहानी।”',
          'बच्चे कागज़ की नावों को, गलियों में तैराते हैं,', 'वर्षा रानी के स्वागत में, सब मिलकर गीत सुनाते हैं।'],
         [('नभ', 'आकाश', 1), ('हरियाना', 'हरा-भरा हो जाना', 1), ('उमड़ना', 'भरकर ऊपर तक बढ़ जाना', 2), ('सुहानी', 'मन को अच्छी लगने वाली', 2), ('बरस', 'वर्ष, साल', 2)],
         [('बादल नभ में क्या करते हुए दिखाए गए हैं?', 'ढोल बजाते हुए', ['सोते हुए', 'रोते हुए', 'भागते हुए'], 1),
          ('वर्षा आने पर मोर क्या करता है?', 'पंख फैलाता है', ['गीत गाता है', 'उड़ जाता है', 'छिप जाता है'], 1),
          ('दादी किस बात से प्रसन्न हैं?', 'इस बरस फसल अच्छी होगी', ['बच्चे नावें चला रहे हैं', 'नाले उमड़ रहे हैं', 'बादल गरज रहे हैं'], 2),
          ('बच्चे गलियों में क्या तैराते हैं?', 'कागज़ की नावें', ['पत्ते', 'खिलौने', 'फूल'], 2)],
         [('“प्यासी धरती के आँगन में, मोती-से बरसाते हैं” — इस पंक्ति का भाव लिखिए।', 'गर्मी से सूखी धरती पर बादल बूँदें बरसाते हैं जो मोतियों जैसी सुंदर और कीमती लगती हैं; धरती की प्यास बुझती है।', 1),
          ('वर्षा आने पर प्रकृति में कौन-कौन से परिवर्तन होते हैं? कविता के आधार पर लिखिए।', 'बादल घिर आते हैं, मेंढक टर्राते हैं, मोर नाचता है, सूखे पेड़ हरे होते हैं, नदियाँ-नाले उमड़ते हैं और खेत पानी से भर जाते हैं।', 0)],
         'वर्षा ऋतु के आगमन पर प्रकृति, पशु-पक्षियों, किसानों और बच्चों में छाई प्रसन्नता का सजीव चित्रण।',
         [('प्यासी धरती के आँगन में, मोती-से बरसाते हैं।', 'उपमा अलंकार', 'वर्षा की बूँदों की तुलना मोतियों से “से” वाचक शब्द द्वारा की गई है।', 1),
          ('घिर-घिर आए काले बादल, नभ में ढोल बजाते हैं,', 'मानवीकरण अलंकार', 'बादलों पर ढोल बजाने जैसी मानवीय क्रिया का आरोप है।', 1),
          ('वर्षा रानी के स्वागत में, सब मिलकर गीत सुनाते हैं।', 'मानवीकरण अलंकार', 'वर्षा को “रानी” कहकर उस पर मानवीय रूप का आरोप किया गया है।', 2)],
         [('आपके क्षेत्र में वर्षा ऋतु का स्वागत कैसे होता है? कविता से तुलना करते हुए लिखिए।', 'अपने अनुभव — त्योहार, खेती, बच्चों के खेल, भोजन — कविता के दृश्यों (मोर, नावें, फसल) से तुलना।')],
         {1: 'प्रसंग: “वर्षा आई” कविता में वर्षा ऋतु के आगमन का चित्रण है। व्याख्या: काले बादल घिर-घिरकर आते हैं, मानो आकाश में ढोल बजा रहे हों, और प्यासी धरती पर मोतियों जैसी बूँदें बरसाते हैं। मेंढक टर्राते हैं, मोर पंख फैलाकर नाचता है और सूखा पेड़ फिर हरा हो जाता है। विशेष: “मोती-से” में उपमा; बादलों का मानवीकरण; “टर्र-टर्र” ध्वन्यात्मक शब्द।',
          2: 'प्रसंग: इसी कविता का दूसरा अंश। व्याख्या: नदियाँ-नाले उमड़ आते हैं, खेत पानी से भर जाते हैं और दादी अच्छी फसल की आशा करती हैं। बच्चे गलियों में कागज़ की नावें चलाते हैं और सब मिलकर “वर्षा रानी” का स्वागत गीतों से करते हैं। विशेष: “वर्षा रानी” में मानवीकरण; ग्रामीण जीवन का सजीव चित्र; प्रसन्नता का भाव।'},
         [('वर्षा से पहले पेड़ हरा-भरा था।', False, 'पेड़ “सूखा-सा” था, वर्षा के बाद फिर से हरा हुआ।', 1)]),
    poem('भोर',
         ['पूरब के आँगन में आकर, ऊषा ने रंग बिखेरा,', 'चिड़ियों ने चहचहाकर बोला — “जागो, हुआ सवेरा!”',
          'ओस की बूँदें घासों पर, मोती-सी चमक रही हैं,', 'कलियाँ धीरे-धीरे खुलकर, मंद-मंद महक रही हैं।'],
         ['ठंडी-ठंडी पवन चली तो, पेड़ों ने सिर डोलाया,', 'नदिया ने कल-कल स्वर में, भोर का गीत सुनाया।',
          'आलस छोड़ो, बाहर आओ, देखो सुंदर नज़ारा है,', 'प्रकृति माँ की गोदी में, हर पल कितना प्यारा है।'],
         [('ऊषा', 'भोर की लाली, प्रभात', 1), ('ओस', 'रात में घास-पत्तों पर जमी पानी की बूँदें', 1), ('मंद', 'धीमी', 1), ('डोलाना', 'हिलाना', 2), ('नज़ारा', 'दृश्य', 2)],
         [('ऊषा ने रंग कहाँ बिखेरा?', 'पूरब के आँगन में', ['पश्चिम के आकाश में', 'नदी के किनारे', 'खेतों में'], 1),
          ('चिड़ियाँ क्या कहती हैं?', '“जागो, हुआ सवेरा!”', ['“सो जाओ, रात हुई!”', '“बारिश आने वाली है!”', '“चलो, घर लौटें!”'], 1),
          ('ओस की बूँदें किसके समान चमक रही हैं?', 'मोती के समान', ['तारों के समान', 'आग के समान', 'दर्पण के समान'], 1),
          ('पवन चलने पर पेड़ों ने क्या किया?', 'सिर डोलाया', ['फल गिराए', 'पत्ते छिपाए', 'गीत गाया'], 2),
          ('कवि क्या छोड़कर बाहर आने को कहता है?', 'आलस', ['घर', 'पढ़ाई', 'खेल'], 2)],
         [('“पेड़ों ने सिर डोलाया” — इसका अर्थ और भाव स्पष्ट कीजिए।', 'ठंडी हवा से पेड़ हिलने लगे; कवि ने कल्पना की है कि पेड़ मानो सिर हिलाकर भोर का अभिवादन कर रहे हैं।', 2),
          ('कवि ने प्रकृति को “माँ” क्यों कहा है?', 'प्रकृति माँ की तरह हमें पालती है, सुख, सौंदर्य और जीवन देती है; उसकी गोद में हर पल प्यारा लगता है।', 2)],
         'प्रभात के समय प्रकृति के सौंदर्य — ऊषा की लाली, चिड़ियों का चहचहाना, ओस, कलियाँ, पवन और नदी — का चित्रण और आलस छोड़कर प्रकृति का आनंद लेने का संदेश।',
         [('ओस की बूँदें घासों पर, मोती-सी चमक रही हैं,', 'उपमा अलंकार', 'ओस की बूँदों की तुलना मोती से “सी” वाचक शब्द द्वारा की गई है।', 1),
          ('ठंडी-ठंडी पवन चली तो, पेड़ों ने सिर डोलाया,', 'मानवीकरण अलंकार', 'पेड़ों पर सिर हिलाने जैसी मानवीय क्रिया का आरोप है।', 2),
          ('कलियाँ धीरे-धीरे खुलकर, मंद-मंद महक रही हैं।', 'अनुप्रास अलंकार', '“म” वर्ण (मंद-मंद महक) की आवृत्ति है।', 1)],
         [('सुबह जल्दी उठने के क्या लाभ हैं? कविता के संदेश से जोड़कर अपने विचार लिखिए।', 'ताज़ी हवा, शांत वातावरण, व्यायाम और पढ़ाई के लिए समय, प्रकृति का सौंदर्य — कविता आलस छोड़कर भोर का आनंद लेने को कहती है।')],
         {1: 'प्रसंग: “भोर” कविता में सुबह के सौंदर्य का वर्णन है। व्याख्या: पूर्व दिशा में ऊषा ने लाली बिखेर दी है, चिड़ियाँ चहचहाकर सबको जगा रही हैं, घास पर ओस की बूँदें मोती-सी चमक रही हैं और कलियाँ धीरे-धीरे खिलकर महक रही हैं। विशेष: “मोती-सी” में उपमा; “मंद-मंद महक” में अनुप्रास; ऊषा का मानवीकरण।',
          2: 'प्रसंग: “भोर” कविता का दूसरा अंश। व्याख्या: ठंडी हवा चलने पर पेड़ मानो सिर हिलाकर अभिवादन करते हैं और नदी कल-कल स्वर में भोर का गीत सुनाती है। कवि आलस छोड़कर बाहर आने और प्रकृति माँ की गोद के सुंदर दृश्य देखने को कहता है। विशेष: पेड़ों और नदी का मानवीकरण; “कल-कल” ध्वन्यात्मक शब्द; प्रेरणा का स्वर।'}),
    poem('पर्वत',
         ['ऊँचे-ऊँचे पर्वत देखो, बादल से बतियाते हैं,', 'सिर पर बर्फ़ का मुकुट सजाकर, राजा-से इठलाते हैं।',
          'इनकी गोदी से झरने निकले, गीत सुनाते बहते हैं,', 'घाटी-घाटी फूल खिलाकर, “आओ, आओ” कहते हैं।'],
         ['चीड़ और देवदार कतारों में, प्रहरी-से डटे खड़े,', 'झील के निर्मल दर्पण में, सूरज-चंदा झाँक पड़े।',
          'हम मनुष्य जो काट रहे हैं, इनके हरे-भरे वन को,', 'सोचो, कौन बचाएगा फिर, धरती के इस जीवन को?'],
         [('बतियाना', 'बातें करना', 1), ('इठलाना', 'गर्व से इतराना', 1), ('प्रहरी', 'पहरेदार', 2), ('निर्मल', 'स्वच्छ, साफ़', 2), ('कतार', 'पंक्ति', 2)],
         [('पर्वत किससे बातें करते हैं?', 'बादल से', ['नदी से', 'सूरज से', 'मनुष्य से'], 1),
          ('पर्वतों ने सिर पर क्या सजाया है?', 'बर्फ़ का मुकुट', ['फूलों का हार', 'बादलों की पगड़ी', 'सूरज का दीपक'], 1),
          ('चीड़ और देवदार किसके समान खड़े हैं?', 'प्रहरी (पहरेदार) के समान', ['राजा के समान', 'बच्चों के समान', 'यात्रियों के समान'], 2),
          ('कविता के अंत में कवि किस बात पर चिंता प्रकट करता है?', 'मनुष्य द्वारा वनों की कटाई पर', ['बर्फ़ पिघलने पर', 'झरनों के सूखने पर', 'पर्यटकों की भीड़ पर'], 2)],
         [('“झील के निर्मल दर्पण में, सूरज-चंदा झाँक पड़े” — इस पंक्ति में किस दृश्य का चित्रण है?', 'झील का पानी इतना साफ़ है कि उसमें सूरज और चाँद की परछाईं दिखती है, मानो वे दर्पण में झाँक रहे हों।', 2),
          ('कवि ने पर्वतों को राजा के समान क्यों कहा है?', 'वे ऊँचे हैं, बर्फ़ का मुकुट पहने हैं और गर्व से खड़े हैं, जैसे कोई राजा।', 1)],
         'पर्वतों, झरनों, घाटियों, वनों और झीलों के सौंदर्य का चित्रण तथा वनों की कटाई से प्रकृति को होने वाली हानि पर चिंता।',
         [('सिर पर बर्फ़ का मुकुट सजाकर, राजा-से इठलाते हैं।', 'उपमा अलंकार', 'पर्वतों की तुलना राजा से “से” वाचक शब्द द्वारा की गई है।', 1),
          ('ऊँचे-ऊँचे पर्वत देखो, बादल से बतियाते हैं,', 'मानवीकरण अलंकार', 'पर्वतों पर बातें करने जैसी मानवीय क्रिया का आरोप है।', 1),
          ('चीड़ और देवदार कतारों में, प्रहरी-से डटे खड़े,', 'उपमा अलंकार', 'पेड़ों की तुलना प्रहरी से “से” द्वारा की गई है।', 2)],
         [('कविता के अंतिम प्रश्न “कौन बचाएगा फिर, धरती के इस जीवन को?” का उत्तर आप कैसे देंगे? सुझाव सहित लिखिए।', 'हम सबको — वृक्षारोपण, कटाई पर रोक, पर्यटन में स्वच्छता, पहाड़ों पर प्लास्टिक न फैलाना; व्यक्तिगत और सामूहिक ज़िम्मेदारी।')],
         {1: 'प्रसंग: “पर्वत” कविता में पहाड़ों के सौंदर्य का वर्णन है। व्याख्या: ऊँचे पर्वत मानो बादलों से बातें करते हैं और बर्फ़ का मुकुट पहनकर राजा की तरह इतराते हैं। उनकी गोद से झरने गीत गाते बहते हैं और घाटियों में फूल खिलाकर सबको बुलाते हैं। विशेष: “राजा-से” में उपमा; पर्वतों और झरनों का मानवीकरण; “ऊँचे-ऊँचे”, “घाटी-घाटी” में पुनरुक्ति।',
          2: 'प्रसंग: इसी कविता का दूसरा अंश। व्याख्या: चीड़ और देवदार के पेड़ पहरेदारों की तरह कतारों में खड़े हैं और साफ़ झील में सूरज-चाँद की परछाईं दिखती है। कवि चिंता करता है कि मनुष्य इन वनों को काट रहा है; फिर धरती के जीवन को कौन बचाएगा? विशेष: “प्रहरी-से” में उपमा; “झील के निर्मल दर्पण” में रूपक; पर्यावरण-चेतना।'}),
    poem('नदी की यात्रा',
         ['पर्वत की गोदी से निकली, छोटी-सी जलधारा मैं,', 'कल-कल गाती, आगे बढ़ती, कभी न थककर हारी मैं।',
          'खेतों को मैंने सींचा है, प्यास बुझाई गाँवों की,', 'मेरे तट पर गूँज रही है, हँसी-ठिठोली नावों की।'],
         ['पर अब मुझमें कचरा फेंको, तो मैं रोती रहती हूँ,', 'मैली होकर चुपके-चुपके, सबका दुख मैं सहती हूँ।',
          'मुझे बचाओ, स्वच्छ रखो तो, फिर मैं गीत सुनाऊँगी,', 'सागर तक जाकर भी मैं, तुमको याद दिलाऊँगी।'],
         [('जलधारा', 'पानी की धारा', 1), ('सींचना', 'पानी देना', 1), ('तट', 'किनारा', 1), ('हँसी-ठिठोली', 'हँसी-मज़ाक', 1), ('मैली', 'गंदी', 2)],
         [('नदी कहाँ से निकली?', 'पर्वत की गोदी से', ['सागर से', 'बादलों से', 'खेतों से'], 1),
          ('नदी ने किसकी प्यास बुझाई?', 'गाँवों की', ['सागर की', 'पर्वतों की', 'बादलों की'], 1),
          ('कचरा फेंकने पर नदी क्या करती है?', 'रोती रहती है', ['गीत सुनाती है', 'तेज़ बहती है', 'सूख जाती है'], 2),
          ('स्वच्छ रखने पर नदी क्या करेगी?', 'फिर गीत सुनाएगी', ['रास्ता बदल लेगी', 'बाढ़ लाएगी', 'रुक जाएगी'], 2)],
         [('इस कविता में नदी स्वयं अपनी कहानी कह रही है। इसका क्या प्रभाव पड़ता है?', 'नदी का मानवीकरण पाठक के मन में उसके प्रति सहानुभूति जगाता है; उसकी पीड़ा सीधे हमारे दिल तक पहुँचती है।', 0),
          ('“मैली होकर चुपके-चुपके, सबका दुख मैं सहती हूँ” — भाव स्पष्ट कीजिए।', 'प्रदूषण से गंदी होकर भी नदी चुपचाप सब सहती है और शिकायत नहीं करती; यह मनुष्य की लापरवाही पर व्यंग्य है।', 2)],
         'नदी की आत्मकथा के माध्यम से उसकी उपयोगिता (सिंचाई, प्यास बुझाना) और प्रदूषण से होने वाली पीड़ा का चित्रण तथा नदियों को स्वच्छ रखने का संदेश।',
         [('पर अब मुझमें कचरा फेंको, तो मैं रोती रहती हूँ,', 'मानवीकरण अलंकार', 'नदी पर रोने जैसी मानवीय भावना का आरोप है।', 2),
          ('कल-कल गाती, आगे बढ़ती, कभी न थककर हारी मैं।', 'मानवीकरण अलंकार', 'नदी पर गाने और थकने जैसी मानवीय क्रियाओं का आरोप है।', 1)],
         [('नदियों को स्वच्छ रखने के लिए विद्यार्थी क्या-क्या कर सकते हैं? कविता के संदेश के आधार पर लिखिए।', 'जागरूकता अभियान, घाटों की सफ़ाई में भाग लेना, पूजा-सामग्री/प्लास्टिक नदी में न डालना, परिवार को समझाना।')],
         {1: 'प्रसंग: “नदी की यात्रा” कविता में नदी स्वयं अपनी कहानी कहती है। व्याख्या: नदी कहती है कि वह पर्वत की गोद से छोटी धारा बनकर निकली और कल-कल गाती, बिना थके आगे बढ़ती रही। उसने खेतों को सींचा, गाँवों की प्यास बुझाई और उसके तट पर नावों की हँसी-ठिठोली गूँजती है। विशेष: पूरी कविता में मानवीकरण; “कल-कल” ध्वन्यात्मक; आत्मकथात्मक शैली।',
          2: 'प्रसंग: इसी कविता का दूसरा अंश। व्याख्या: नदी दुखी होकर कहती है कि लोग उसमें कचरा फेंकते हैं तो वह रोती है और मैली होकर चुपचाप सब सहती है। वह विनती करती है कि उसे स्वच्छ रखा जाए तो वह फिर गीत सुनाएगी। विशेष: मानवीकरण; करुण भाव; पर्यावरण-संरक्षण का संदेश।'}),
]

t = topic('कविता में प्रकृति का सौंदर्य और भाव-सौंदर्य', 'प्रकृति का सौंदर्य')
reading(t, P_PRAKRITI, 'extract', c4kinds=('eval', 'summary'))
t4_1 = t

t = topic('काव्य-सौंदर्य: अनुप्रास, उपमा और मानवीकरण अलंकार', 'अलंकार')
fx(t, 'C1', (1, 2), [
    ('उपमा अलंकार में तुलना के लिए प्रयुक्त शब्द (सा, सी, से, समान) क्या कहलाते हैं?', 'वाचक शब्द', 'उपमा के चार अंग: उपमेय, उपमान, साधारण धर्म और वाचक शब्द।', ['उपमेय', 'उपमान', 'साधारण धर्म']),
    ('“मुख चाँद के समान सुंदर है” — इसमें उपमेय क्या है?', 'मुख', 'जिसकी तुलना की जाए वह उपमेय (मुख); जिससे तुलना हो वह उपमान (चाँद)।', ['चाँद', 'समान', 'सुंदर']),
    ('जहाँ एक ही वर्ण बार-बार आए, वहाँ कौन-सा अलंकार होता है?', 'अनुप्रास अलंकार', 'वर्णों की आवृत्ति अनुप्रास है।', ['उपमा अलंकार', 'मानवीकरण अलंकार', 'रूपक अलंकार']),
    ('प्रकृति पर मानवीय भावनाओं के आरोप को क्या कहते हैं?', 'मानवीकरण अलंकार', 'निर्जीव/प्रकृति को मनुष्य की तरह दिखाना।', ['अनुप्रास अलंकार', 'उपमा अलंकार', 'यमक अलंकार']),
])
tagbank(t, ALANK, ALANK_L, 'अलंकार', ALANK_DEF, noun='पंक्ति')
t4_2 = t

t = topic('व्याकरण: पर्यायवाची और विलोम शब्द', 'पर्यायवाची और विलोम')
paryay(t, PARYAY)
vilom(t, VILOM, c4=False)
t4_3 = t

PARA_FACTS = [
    ('अनुच्छेद लेखन में सबसे पहले क्या करना चाहिए?', 'विषय से जुड़े मुख्य बिंदुओं की रूपरेखा बनाना', 'रूपरेखा से विचार क्रमबद्ध रहते हैं।', ['सीधे अंतिम वाक्य लिखना', 'कठिन शब्दों की सूची बनाना', 'शीर्षक को बार-बार दोहराना']),
    ('अनुच्छेद में विचार कैसे होने चाहिए?', 'एक ही विषय पर केंद्रित और क्रमबद्ध', 'अनुच्छेद एक केंद्रीय विचार पर आधारित होता है।', ['अलग-अलग विषयों पर बिखरे हुए', 'केवल संवाद के रूप में', 'केवल प्रश्नों के रूप में']),
    ('प्रकृति-वर्णन वाले अनुच्छेद को सजीव बनाने के लिए क्या उपयोगी है?', 'इंद्रियों से जुड़े विवरण (रंग, ध्वनि, गंध) और उपमा जैसे अलंकार', 'दृश्य, ध्वनि और गंध के विवरण चित्र खड़ा करते हैं।', ['केवल आँकड़े', 'केवल कठिन संस्कृत शब्द', 'बहुत लंबे वाक्यों की सूची']),
    ('अनुच्छेद का अंतिम वाक्य कैसा होना चाहिए?', 'पूरे विचार का निष्कर्ष या भाव प्रकट करने वाला', 'अंत में निष्कर्ष/संदेश से अनुच्छेद पूरा लगता है।', ['नए विषय की शुरुआत करने वाला', 'पहले वाक्य की हूबहू नकल', 'केवल एक शब्द का']),
]
PARA_FLAWS = [
    ('बारिश अच्छी है। बारिश में पानी गिरता है। बारिश में मज़ा आता है। बारिश अच्छी है।', 'एक ही बात और शब्द “बारिश” बार-बार दोहराया गया है; वर्णन में न दृश्य है, न भावना।', 'आसमान में काले बादल घिर आए और पहली बूँदों के साथ मिट्टी की सौंधी गंध फैल गई…'),
    ('सुबह का दृश्य सुंदर था। कल मैंने क्रिकेट देखा। मेरी गणित की परीक्षा अच्छी हुई।', 'वाक्य अलग-अलग विषयों पर हैं; अनुच्छेद एक विषय पर केंद्रित नहीं है।', 'सुबह का दृश्य बहुत सुंदर था — पूरब में लाली फैली थी, चिड़ियाँ चहचहा रही थीं…'),
    ('पेड़ हमें ऑक्सीजन देते हैं इसलिए हमें पेड़ लगाने चाहिए क्योंकि पेड़ छाया देते हैं और फल देते हैं और पक्षियों का घर होते हैं और…', 'एक ही बहुत लंबा, बिना विराम का वाक्य है; विचार क्रमबद्ध नहीं।', 'पेड़ हमें ऑक्सीजन, छाया और फल देते हैं। वे पक्षियों का घर भी हैं। इसलिए हमें अधिक से अधिक पेड़ लगाने चाहिए।'),
]


def para_task(r):
    top = r.choice([
        ('वर्षा ऋतु का पहला दिन', ['बादलों और पहली बूँदों का दृश्य', 'मिट्टी की गंध और ठंडी हवा', 'लोगों और पशु-पक्षियों की प्रसन्नता', 'आपकी अपनी भावना'], 'दृश्य-ध्वनि-गंध का वर्णन; पशु-पक्षी; लोगों की प्रतिक्रिया; व्यक्तिगत भावना; एक-दो अलंकार।'),
        ('समुद्र-तट पर सूर्यास्त', ['आकाश के बदलते रंग', 'लहरों की ध्वनि', 'तट पर लोगों की गतिविधियाँ', 'उस दृश्य का आप पर प्रभाव'], 'रंगों का क्रमिक परिवर्तन; लहरों की ध्वनि; लोग; शांति/आनंद का भाव।'),
        ('मेरे घर के पास का बगीचा', ['बगीचे में लगे पेड़-पौधे और फूल', 'वहाँ आने वाले पक्षी', 'सुबह या शाम का वातावरण', 'बगीचे का महत्व'], 'पौधों-फूलों के नाम; पक्षियों की ध्वनि; वातावरण; स्वास्थ्य/पर्यावरण के लिए महत्व।'),
        ('पहाड़ों में एक सुबह', ['बर्फ़ से ढकी चोटियाँ', 'ठंडी हवा और कोहरा', 'झरने, पेड़ और पक्षी', 'शहर की सुबह से तुलना'], 'चोटियाँ, कोहरा, झरने; ठंड का अनुभव; शहर से तुलना; निष्कर्ष।'),
        ('सर्दियों की धूप', ['सुबह का कोहरा', 'धूप की गरमाहट', 'लोगों की दिनचर्या में बदलाव', 'आपको यह ऋतु क्यों अच्छी/बुरी लगती है'], 'कोहरा; धूप का सुख; दिनचर्या; व्यक्तिगत राय।'),
    ])
    return {'task': f'“{top[0]}” विषय पर एक अनुच्छेद लिखिए।', 'bullets': top[1], 'ind': f'एक केंद्रीय विचार, क्रमबद्ध वाक्य, आकर्षक आरंभ और निष्कर्षपूर्ण अंत। {top[2]}',
            'model': f'मॉडल आरंभ: “{top[0]}” — … (दृश्य-वर्णन से शुरुआत, बीच में बिंदुओं का विस्तार, अंत में भावपूर्ण निष्कर्ष)।'}


t = topic('रचना: अनुच्छेद लेखन (प्रकृति पर)', 'अनुच्छेद लेखन')
writing(t, 'अनुच्छेद', [para_task], PARA_FACTS, PARA_FLAWS)
t4_4 = t
CHAPTERS[4] = [t4_1, t4_2, t4_3, t4_4]


# =========================================================== G8 · पाठ 5 दोहे और साखियाँ

GURU_V = set('आईऊएऐओऔ')
LAGHU_V = set('अइउऋ')
GURU_M = set('ाीूेैोौ')
LAGHU_M = set('िुृ')


def syl(word):
    out = []
    i = 0
    w = word
    while i < len(w):
        c = w[i]
        if c in GURU_V or c in LAGHU_V:
            out.append([c, 2 if c in GURU_V else 1])
            i += 1
        elif 'क' <= c <= 'ह':
            j = i + 1
            if j < len(w) and w[j] == '़':
                j += 1
            if j < len(w) and w[j] == '्':
                if out:
                    out[-1][1] = 2
                    out[-1][0] += w[i:j + 1]
                i = j + 1
                continue
            wt = 1
            if j < len(w) and w[j] in GURU_M:
                wt = 2
                j += 1
            elif j < len(w) and w[j] in LAGHU_M:
                j += 1
            if j < len(w) and w[j] == 'ँ':
                j += 1
            out.append([w[i:j], wt])
            i = j
        elif c in 'ंः':
            if out:
                out[-1][1] = 2
                out[-1][0] += c
            i += 1
        else:
            if out:
                out[-1][0] += c
            i += 1
    return out


def matra(s):
    return sum(x[1] for wd in re.findall(r'[ऀ-ॿ]+', s) for x in syl(wd))


def marks_of(word):
    return ' '.join('ऽ' if x[1] == 2 else '।' for x in syl(word))


DOHE = [
    ('मीठी वाणी बोलिए, मन का मैल मिटाय।', 'कड़वे बोल न बोलिए, प्रेम-डोर टुट जाय।', 'मीठी वाणी बोलनी चाहिए, क्योंकि इससे मन की कटुता मिट जाती है; कड़वे वचन प्रेम के बंधन को तोड़ देते हैं।',
     'मधुर वाणी का महत्व', [('वाणी', 'बोली'), ('मैल', 'गंदगी, कटुता'), ('डोर', 'धागा, बंधन')],
     [('कवि के अनुसार कड़वे बोल क्या करते हैं?', 'प्रेम की डोर तोड़ देते हैं', ['मन का मैल मिटाते हैं', 'मित्रता बढ़ाते हैं', 'मन को शांत करते हैं'])]),
    ('समय बड़ा अनमोल है, इसको व्यर्थ न खोय।', 'जो पल बीता सो गया, लौट न आवे कोय।', 'समय बहुत मूल्यवान है, इसे बेकार नहीं गँवाना चाहिए; जो पल बीत गया, वह कभी लौटकर नहीं आता।',
     'समय का सदुपयोग', [('अनमोल', 'जिसका मूल्य आँका न जा सके'), ('व्यर्थ', 'बेकार'), ('कोय', 'कोई')],
     [('बीते हुए पल के बारे में कवि क्या कहता है?', 'वह लौटकर नहीं आता', ['वह फिर से आता है', 'वह सबसे मीठा होता है', 'उसे भूल जाना चाहिए'])]),
    ('विद्या धन सबसे बड़ा, बाँटे से बढ़ जाय।', 'चोर न इसको ले सके, आग न इसे जलाय।', 'विद्या सबसे बड़ा धन है जो बाँटने से बढ़ता है; इसे न चोर चुरा सकता है, न आग जला सकती है।',
     'विद्या रूपी धन की श्रेष्ठता', [('विद्या', 'ज्ञान'), ('बाँटे', 'बाँटने पर')],
     [('विद्या-धन की कौन-सी विशेषता बताई गई है?', 'बाँटने से बढ़ता है', ['बाँटने से घटता है', 'चोर चुरा सकता है', 'आग में जल जाता है'])]),
    ('मात-पिता की सीख को, रखना सदा सहेज।', 'उनके आशीर्वाद से, जीवन बने सतेज।', 'माता-पिता की सीख को सदा सँभालकर रखना चाहिए; उनके आशीर्वाद से जीवन तेजस्वी और सफल बनता है।',
     'माता-पिता की सीख और आशीर्वाद का महत्व', [('सहेज', 'सँभालकर'), ('सतेज', 'तेजस्वी, चमकदार')],
     [('जीवन किससे सतेज बनता है?', 'माता-पिता के आशीर्वाद से', ['धन-दौलत से', 'मित्रों की संगति से', 'अकेले रहने से'])]),
    ('पेड़ लगाओ प्रेम से, धरती हो खुशहाल।', 'छाया, फल, जल, वायु से, जीवन रहे निहाल।', 'प्रेम से पेड़ लगाने चाहिए ताकि धरती सुखी हो; पेड़ों से मिलने वाली छाया, फल, जल और वायु से जीवन पूरी तरह संतुष्ट रहता है।',
     'वृक्षारोपण और पर्यावरण का महत्व', [('खुशहाल', 'सुख-समृद्धि से भरा'), ('निहाल', 'पूर्णतः प्रसन्न, संतुष्ट')],
     [('दोहे में पेड़ों से मिलने वाली कौन-सी चीज़ें बताई गई हैं?', 'छाया, फल, जल और वायु', ['धन, सोना और चाँदी', 'केवल लकड़ी', 'केवल फूल'])]),
    ('जो दूजे का दुख हरे, वह सच्चा इंसान।', 'अपने सुख में डूबकर, भूले नहीं जहान।', 'जो दूसरों का दुख दूर करता है, वही सच्चा मनुष्य है; वह अपने सुख में डूबकर भी संसार (दूसरों) को नहीं भूलता।',
     'परोपकार और मानवता', [('दूजे', 'दूसरे'), ('हरे', 'दूर करे'), ('जहान', 'संसार')],
     [('कवि के अनुसार सच्चा इंसान कौन है?', 'जो दूसरों का दुख दूर करे', ['जो केवल अपने सुख में डूबा रहे', 'जिसके पास बहुत धन हो', 'जो सबसे अधिक बोले'])]),
    ('चींटी छोटी है मगर, करती श्रम दिन-रात।', 'धीरज रख जो जुट रहे, उसकी बनती बात।', 'चींटी छोटी होकर भी दिन-रात मेहनत करती है; जो धैर्य रखकर लगातार प्रयास करता है, उसका काम अवश्य सफल होता है।',
     'परिश्रम और धैर्य', [('श्रम', 'मेहनत'), ('धीरज', 'धैर्य'), ('बात बनना', 'काम सफल होना')],
     [('दोहे में किसका उदाहरण दिया गया है?', 'चींटी का', ['हाथी का', 'शेर का', 'मधुमक्खी का'])]),
    ('सच की राह कठिन सही, देती मन को चैन।', 'झूठ भले मीठा लगे, कटें दुखों में रैन।', 'सच का मार्ग कठिन हो सकता है, पर वह मन को शांति देता है; झूठ भले मीठा लगे, अंत में रातें दुख में कटती हैं।',
     'सत्य की महिमा', [('चैन', 'शांति, सुकून'), ('रैन', 'रात')],
     [('सच की राह मन को क्या देती है?', 'चैन (शांति)', ['दुख', 'डर', 'थकान'])]),
    ('सच्चा मित्र वही बने, जो संकट में साथ।', 'सुख में तो सब संग हैं, दुख में थामे हाथ।', 'सच्चा मित्र वही है जो संकट में साथ दे; सुख में तो सब साथ होते हैं, सच्चा मित्र दुख में हाथ थामता है।',
     'सच्ची मित्रता की पहचान', [('संकट', 'मुसीबत, विपत्ति'), ('थामे', 'पकड़े, सहारा दे')],
     [('कवि के अनुसार सच्चे मित्र की पहचान कब होती है?', 'संकट (दुख) के समय', ['उत्सव के समय', 'खेल के समय', 'यात्रा के समय'])]),
    ('नल को खुला न छोड़िए, बहे न यूँ ही नीर।', 'आज बचाया जल अगर, कल न सहें हम पीर।', 'नल खुला न छोड़ें ताकि पानी व्यर्थ न बहे; आज पानी बचाएँगे तो कल हमें पानी की कमी की पीड़ा नहीं सहनी पड़ेगी।',
     'जल-संरक्षण', [('नीर', 'पानी'), ('पीर', 'पीड़ा, दुख')],
     [('आज पानी बचाने से क्या लाभ होगा?', 'कल पीड़ा (पानी की कमी) नहीं सहनी पड़ेगी', ['नल जल्दी खराब होगा', 'पानी का रंग बदलेगा', 'बारिश अधिक होगी'])]),
    ('पुस्तक सच्चा मीत है, देती ज्ञान अपार।', 'जितना इसको पढ़ सको, उतना बढ़े विचार।', 'पुस्तक सच्ची मित्र है जो अपार ज्ञान देती है; जितना अधिक पढ़ते हैं, विचार उतने ही बढ़ते और गहरे होते हैं।',
     'पुस्तकों का महत्व', [('मीत', 'मित्र'), ('अपार', 'बहुत अधिक, असीम')],
     [('दोहे में पुस्तक को क्या कहा गया है?', 'सच्चा मीत (मित्र)', ['कठिन बोझ', 'समय की बर्बादी', 'केवल परीक्षा का साधन'])]),
    ('सबसे हिल-मिल कर रहो, जैसे फूल अनेक।', 'रंग अलग, खुशबू अलग, माला तो है एक।', 'सबसे मिल-जुलकर रहना चाहिए, जैसे अलग-अलग रंग और खुशबू वाले अनेक फूल एक ही माला में पिरोए रहते हैं।',
     'विविधता में एकता', [('अनेक', 'बहुत-से'), ('हिल-मिल', 'मेल-जोल से')],
     [('कवि ने मिल-जुलकर रहने की तुलना किससे की है?', 'एक माला में पिरोए अनेक फूलों से', ['बहती नदी से', 'ऊँचे पर्वत से', 'चमकते तारों से'])]),
]
MSGS = [d[3] for d in DOHE]


def doha_frame(d):
    l1, l2, arth, msg, gl, fq = d

    def f(r):
        facts = [(q, a, ds) for q, a, ds in fq]
        facts.append(('इस दोहे का मुख्य संदेश क्या है?', msg, others(r, [m for m in MSGS if m != msg], msg, 3), f'दोहे का भाव: {arth}'))
        vocab = [(w, m, others(r, [x for dd in DOHE for _, x in dd[4] if x != m], m, 3)) for w, m in gl]
        return ex('दोहा', f'{l1}\n{l2}', facts=facts, vocab=vocab,
                  infer=[('इस दोहे का भावार्थ अपने शब्दों में लिखिए।', arth), ('इस दोहे की सीख को अपने दैनिक जीवन से जोड़कर एक उदाहरण दीजिए।', f'उदाहरण ऐसा हो जो “{msg}” को दर्शाए।')],
                  points=[arth], evals=[(f'क्या आज के समय में भी “{msg}” की सीख उपयोगी है? दोहे के आधार पर तर्क सहित लिखिए।', f'हाँ — {arth} आज के जीवन से एक-दो उदाहरण।')],
                  title=None)
    return f


DOHA_FR = [doha_frame(d) for d in DOHE]

t = topic('दोहों का अर्थ और नैतिक संदेश', 'दोहों का अर्थ')
reading(t, DOHA_FR, 'extract', c4kinds=('eval',))


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def doha_compare(r, D):
    a, b = r.sample(DOHE, 2)
    m = mk('C4', D)
    stem = (f'नीचे दिए गए दो दोहे पढ़िए।\n1. {a[0]}\n{a[1]}\n2. {b[0]}\n{b[1]}\n'
            + r.choice(['दोनों दोहों का भावार्थ लिखिए। इनमें से कौन-सी सीख आपको आज के जीवन में अधिक आवश्यक लगती है? कारण सहित लिखिए।',
                        'दोनों दोहों के संदेशों की तुलना कीजिए और बताइए कि इन्हें अपने विद्यालय-जीवन में कैसे अपनाया जा सकता है।']))
    ans = f'1. {a[2]} 2. {b[2]} अपना मत: कोई भी तर्कसंगत चुनाव, उदाहरण सहित।'
    return item(stem, ans, f'प्रत्येक दोहे का सही भावार्थ (लगभग 1-2 अंक); तुलना/चुनाव और तर्क के लिए शेष अंक। [{m}]', m, 'multi_step')


t5_1 = t

t = topic('दोहा छंद की पहचान और लय', 'दोहा छंद')
fx(t, 'C1', (1, 2), [
    ('दोहे के विषम (पहले और तीसरे) चरणों में कितनी मात्राएँ होती हैं?', '13', 'दोहा: विषम चरण 13, सम चरण 11 मात्राएँ।', ['11', '16', '24']),
    ('दोहे के सम (दूसरे और चौथे) चरणों में कितनी मात्राएँ होती हैं?', '11', 'सम चरणों में 11 मात्राएँ होती हैं और अंत में गुरु-लघु (ऽ।)।', ['13', '12', '16']),
    ('दोहे की एक पंक्ति में कुल कितनी मात्राएँ होती हैं?', '24', '13 + 11 = 24 मात्राएँ।', ['26', '22', '32']),
    ('दोहे में कुल कितने चरण होते हैं?', 'चार', 'दो पंक्तियाँ, प्रत्येक में दो चरण।', ['दो', 'छह', 'आठ']),
    ('लघु मात्रा का चिह्न क्या है?', '।', 'लघु = । (1 मात्रा), गुरु = ऽ (2 मात्राएँ)।', ['ऽ', '॥', '—']),
    ('दोहे में तुक (अंत्यानुप्रास) कहाँ मिलती है?', 'सम चरणों (दूसरे और चौथे) के अंत में', 'जैसे “मिटाय–जाय”, “खोय–कोय”।', ['विषम चरणों के आरंभ में', 'हर शब्द के बीच में', 'कहीं नहीं']),
    ('दोहे में यति (ठहराव) कहाँ आती है?', 'प्रत्येक पंक्ति में 13 मात्राओं के बाद', 'विषम चरण के बाद अल्पविराम जैसा ठहराव।', ['हर शब्द के बाद', 'केवल अंत में', '8 मात्राओं के बाद']),
    ('दोहा किस प्रकार का छंद है?', 'अर्धसम मात्रिक छंद', 'मात्राओं पर आधारित; पहले-तीसरे और दूसरे-चौथे चरण समान।', ['वर्णिक छंद', 'मुक्त छंद', 'सम मात्रिक छंद']),
])
CHARANS = [(c, i) for d in DOHE for line in d[:2] for i, c in enumerate(line.rstrip('।').rsplit(', ', 1))]


@t.add('C1', (1, 2, 3))
def ch_count(r, D):
    c, i = r.choice(CHARANS)
    n = matra(c)
    return mq(r, f'दोहे के इस चरण में कितनी मात्राएँ हैं? {Q(c)}', str(n), [str(x) for x in (n - 1, n + 1, n + 2, n - 2) if x != n][:3],
              'मात्राएँ: ' + ' | '.join(f'{w} ({marks_of(w)})' for w in c.split()) + f' = {n}।')


WORDS_M = sorted({w for d in DOHE for line in d[:2] for w in re.findall(r'[ऀ-ॣ०-ॿ]+', line) if 2 <= len(syl(w)) <= 4})


@t.add('C2', (1, 2, 3, 4), 'explain')
def ch_broken(r, D):
    d = r.choice(DOHE)
    line = r.choice(d[:2])
    c1, c2 = line.rstrip('।').rsplit(', ', 1)
    add = r.choice(['बहुत', 'सदा', 'तुम', 'सब'])
    ws = c1.split()
    k = r.randrange(1, len(ws))
    bad = ' '.join(ws[:k] + [add] + ws[k:])
    n = matra(bad)
    m = mk('C2', D)
    stem = f'{Q(bad + ", " + c2 + "।")} — क्या यह दोहे की सही पंक्ति है? मात्राएँ गिनकर स्पष्ट कीजिए' + (' और सुधार भी सुझाइए।' if m >= 2 else '। उत्तर संक्षेप में दीजिए।')
    ans = f'नहीं। पहले चरण “{bad}” में {n} मात्राएँ हैं, जबकि दोहे के विषम चरण में 13 होनी चाहिए। “{add}” हटाने पर सही चरण बनता है: “{c1}” (13 मात्राएँ)।'
    return item(stem, ans, 'मात्रा-गणना सही (1)' + ('; 13 मात्राओं के नियम से तुलना (1)' if m >= 2 else '') + ('; सही सुधार (1)' if m >= 3 else ''), m, 'explain')


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def ch_parts(r, D):
    d = r.choice(DOHE)
    l1, l2 = d[0], d[1]
    c = r.choice([l1, l2]).rstrip('।').rsplit(', ', 1)
    ws = r.sample(WORDS_M, 2)
    t1 = l1.rstrip('।').rsplit(', ', 1)[1].split()[-1]
    t2 = l2.rstrip('।').rsplit(', ', 1)[1].split()[-1]
    parts = [
        (f'शब्द {Q(ws[0])} पर लघु (।) और गुरु (ऽ) के चिह्न लगाकर मात्राएँ गिनिए।', f'{marks_of(ws[0])} = {matra(ws[0])}', f'{marks_of(ws[0])} = {matra(ws[0])} [1]'),
        (f'शब्द {Q(ws[1])} की मात्राएँ गिनिए।', str(matra(ws[1])), f'{marks_of(ws[1])} = {matra(ws[1])} [1]'),
        (f'चरण {Q(c[0])} में कितनी मात्राएँ हैं? चिह्न लगाकर दिखाइए।', str(matra(c[0])), ' | '.join(f'{w} {marks_of(w)}' for w in c[0].split()) + f' = {matra(c[0])} [2]'),
        (f'दोहे की तुक वाले शब्द लिखिए:\n{l1}\n{l2}', f'{t1} – {t2}', f'सम चरणों के अंतिम शब्द: {t1}, {t2} [1]'),
        (f'चरण {Q(c[1])} के अंत में कौन-सा मात्रा-क्रम है?', 'गुरु-लघु (ऽ।)', f'अंतिम शब्द “{c[1].split()[-1]}” = {marks_of(c[1].split()[-1])}; अंत में ऽ। [1]'),
    ]
    return hcompose(r, 'दोहा छंद पर आधारित प्रश्नों के उत्तर दीजिए।', parts, k=(2, 3, 4))


@t.add('C4', (2, 3, 4, 5), 'multi_step')
def ch_prove(r, D):
    d = r.choice(DOHE)
    m = mk('C4', D)
    cs = [x for line in d[:2] for x in line.rstrip('।').rsplit(', ', 1)]
    stem = (f'{d[0]}\n{d[1]}\nदोहा छंद के लक्षण लिखिए। फिर इस दोहे के चारों चरणों की मात्राएँ गिनकर सिद्ध कीजिए कि यह दोहा है'
            + (' और तुक वाले शब्द भी बताइए।' if D <= 3 else '। अंत में किसी नैतिक विषय पर अपना एक दोहा (या दोहे की एक पंक्ति) रचने का प्रयास कीजिए।'))
    ans = ('लक्षण: चार चरण; विषम चरण 13, सम चरण 11 मात्राएँ; सम चरणों के अंत में गुरु-लघु और तुक; 13 के बाद यति। गणना: '
           + '; '.join(f'“{c}” = {matra(c)}' for c in cs) + '।')
    return item(stem, ans, f'लक्षण (1-2); प्रत्येक चरण की सही गणना (1-1 अंक तक); निष्कर्ष/तुक या स्वरचित पंक्ति के लिए शेष अंक। [{m}]', m, 'multi_step')


t5_2 = t

t = topic('व्याकरण: मुहावरे और लोकोक्तियाँ', 'मुहावरे और लोकोक्तियाँ')
fx(t, 'C1', (1, 2), [
    ('मुहावरे और लोकोक्ति में मुख्य अंतर क्या है?', 'मुहावरा वाक्यांश होता है जो वाक्य का अंग बनता है, लोकोक्ति अपने-आप में पूर्ण वाक्य होती है', 'लोकोक्ति स्वतंत्र, पूर्ण कथन है।', ['दोनों में कोई अंतर नहीं', 'लोकोक्ति सदा संस्कृत में होती है', 'मुहावरा केवल कविता में आता है']),
    ('मुहावरे का प्रयोग करते समय क्या होता है?', 'उसका लाक्षणिक (विशेष) अर्थ लिया जाता है, शाब्दिक अर्थ नहीं', 'जैसे “आँखों का तारा” = बहुत प्यारा, सचमुच तारा नहीं।', ['केवल शाब्दिक अर्थ लिया जाता है', 'उसके शब्द बदल दिए जाते हैं', 'उसे वाक्य के अंत में ही लिखते हैं']),
    ('इनमें से कौन-सी लोकोक्ति है?', 'अधजल गगरी छलकत जाय', 'यह एक पूर्ण कथन है जो अनुभव का सार बताता है।', ['नौ दो ग्यारह होना', 'आँखों का तारा होना', 'कमर कसना']),
])
meanings(t, MUHAVARE, 'अर्थ', 'मुहावरा', plural='मुहावरों')
meanings(t, LOKOKTI, 'अर्थ', 'लोकोक्ति', plural='लोकोक्तियों', c1=True, c2=True, c3=False, c4=False)
t5_3 = t
CHAPTERS[5] = [t5_1, t5_2, t5_3]


# =========================================================== G8 · पाठ 6 कहानी — समाज और संवेदना

def story_purpose(t, frames):
    """Extra templates on उद्देश्य and शीर्षक की सार्थकता. Each frame dict carries 'purpose' and 'title'."""

    def pick(r):
        P = r.choice(frames)(r)
        return P

    @t.add('C1', (1, 2, 3))
    def sp_c1(r, D):
        P = pick(r)
        pool = [f(r)['purpose'] for f in frames]
        ds = [x for x in dict.fromkeys(pool) if x != P['purpose']] + PURPOSE_DS
        return mq(r, f'नीचे दिया गया कहानी का अंश पढ़िए।\n{P["text"]}\nइस कहानी का मुख्य उद्देश्य क्या है?', P['purpose'], others(r, ds, P['purpose'], 3),
                  'कहानी की घटनाएँ और पात्रों का परिवर्तन इसी संदेश की ओर ले जाते हैं।')

    @t.add('C2', (2, 3, 4), 'explain')
    def sp_c2(r, D):
        P = pick(r)
        m = mk('C2', D)
        good = P['title'][0]
        stem = f'नीचे दिया गया कहानी का अंश पढ़िए।\n{P["text"]}\nइस कहानी का शीर्षक {Q(good)} कहाँ तक सार्थक है? ' + ('अंश के आधार पर दो कारण दीजिए।' if m >= 2 else 'एक कारण दीजिए।')
        return item(stem, P['why_title'], f'शीर्षक का कहानी के केंद्र से संबंध (1)' + ('; अंश से प्रमाण (1)' if m >= 2 else '') + ('; प्रतीकात्मक/जिज्ञासा जगाने वाले पक्ष का उल्लेख (1)' if m >= 3 else '') + f'। अपेक्षित: {P["why_title"]}', m, 'explain')

    @t.add('C3', (2, 3, 4, 5), 'short')
    def sp_c3(r, D):
        P = pick(r)
        parts = [
            ('कहानी का मुख्य उद्देश्य एक वाक्य में लिखिए।', P['purpose'], f'{P["purpose"]} [1]'),
            (f'शीर्षक {Q(P["title"][0])} कहानी के लिए उपयुक्त क्यों है?', P['why_title'], 'शीर्षक और केंद्रीय घटना/भाव का संबंध [2]'),
            ('कहानी के लिए एक अन्य उपयुक्त शीर्षक सुझाइए और कारण लिखिए।', f'जैसे {Q(P["alt_title"])} — {P["why_alt"]}', 'उपयुक्त शीर्षक (1); कारण (1) [2]'),
            ('कहानी समाज की किस समस्या या संवेदना की ओर संकेत करती है?', P['issue'], f'{P["issue"]} [1]'),
        ]
        return hcompose(r, f'नीचे दिया गया कहानी का अंश पढ़कर प्रश्नों के उत्तर दीजिए।\n{P["text"]}', parts, k=(2, 3, 4))

    @t.add('C4', (3, 4, 5), 'long')
    def sp_c4(r, D):
        P = pick(r)
        m = mk('C4', D, True)
        stem = (f'नीचे दिया गया कहानी का अंश पढ़िए।\n{P["text"]}\n'
                f'“कहानी का उद्देश्य केवल मनोरंजन नहीं, समाज को संवेदनशील बनाना भी है।” — इस कहानी के आधार पर इस कथन की समीक्षा कीजिए। '
                f'अपने उत्तर में कहानी का उद्देश्य, शीर्षक की सार्थकता, किसी एक पात्र के व्यवहार में आया परिवर्तन और आज के समाज से इसका संबंध लिखिए।')
        ans = f'उद्देश्य: {P["purpose"]} शीर्षक: {P["why_title"]} परिवर्तन: {P["change"]} आज के समाज से संबंध: {P["issue"]}'
        key = f'उद्देश्य (2); शीर्षक की सार्थकता प्रमाण सहित (2); पात्र-परिवर्तन (2); समाज से संबंध और निजी विचार (शेष अंक); सुसंगत प्रस्तुति [{m}]'
        return item(stem, ans, key, m, 'long', minutes=min(25, m * 2))


PURPOSE_DS = ['पाठकों को केवल हँसाना', 'शहर के जीवन को गाँव से श्रेष्ठ बताना', 'धन कमाने को जीवन का एकमात्र लक्ष्य बताना', 'प्रकृति के सौंदर्य का वर्णन करना']


def st_ticket(r):
    n, g = name(r)
    bus = r.choice(['चौदह', 'सत्ताईस', 'बयालीस', 'नौ'])
    fare = r.choice([10, 15, 20])
    text = A(f'{n} रोज़ की तरह बस नंबर {bus} में बैठ{{ा}} था। अगले स्टॉप पर एक बुज़ुर्ग महिला काँपते हाथों से डंडा पकड़कर चढ़ीं। कंडक्टर ने रूखे स्वर में कहा, “अम्मा, {fare} रुपये निकालो, जल्दी!” '
             f'बुज़ुर्ग महिला ने अपनी पोटली टटोली, पर उसमें केवल कुछ सिक्के थे। बस में बैठे लोग खिड़कियों से बाहर देखने लगे, जैसे कुछ हुआ ही न हो। '
             f'{n} की जेब में भी बस घर लौटने का किराया था। एक पल के लिए वह रुक{{ा}}, फिर उठकर बोल{{ा}}, “भैया, इनका टिकट मेरे पैसों से काट दीजिए, मैं घर पैदल चल{{ा}} जाऊँग{{ा}}।” '
             f'कंडक्टर कुछ क्षण उसे देखता रहा। फिर उसने टिकट काटा और पैसे लौटाते हुए धीरे से कहा, “रहने दो बेटा, आज यह टिकट मेरी ओर से।” बस में बैठे कई चेहरे झुक गए।', g)
    P = ex('कहानी का अंश', text,
           facts=[(f'{n} किस नंबर की बस में बैठ{A("{ा}", g)} था?', bus, others(r, ['चौदह', 'सत्ताईस', 'बयालीस', 'नौ', 'इकतीस'], bus)),
                  ('कंडक्टर ने बुज़ुर्ग महिला से कितने रुपये माँगे?', f'{fare} रुपये', [f'{x} रुपये' for x in (5, 10, 15, 20, 25) if x != fare][:3]),
                  ('बुज़ुर्ग महिला की पोटली में क्या था?', 'केवल कुछ सिक्के', ['पूरा किराया', 'एक टिकट', 'कुछ नहीं, वह खाली थी']),
                  ('अंत में टिकट के पैसे किसने दिए?', 'किसी ने नहीं — कंडक्टर ने टिकट अपनी ओर से दिया', [f'{n} ने', 'बुज़ुर्ग महिला ने', 'बस के यात्रियों ने'])],
           vocab=[('रूखे स्वर', 'कठोर, बिना स्नेह की आवाज़', ['मीठी आवाज़', 'धीमी फुसफुसाहट', 'ऊँचा गीत']), ('टटोलना', 'हाथ से छूकर खोजना', ['फेंक देना', 'सिलना', 'गिनना'])],
           tf=[('बस के सभी यात्रियों ने महिला की मदद की।', False, 'लोग खिड़कियों से बाहर देखने लगे, जैसे कुछ हुआ ही न हो।'),
               (f'{n} के पास बहुत अधिक पैसे थे।', False, 'उसकी जेब में केवल घर लौटने का किराया था।')],
           infer=[('“बस में बैठे कई चेहरे झुक गए” — इसका क्या कारण था?', 'यात्रियों को अपनी उदासीनता पर लज्जा आई, क्योंकि एक बच्चे और कंडक्टर ने वह किया जो उन्हें करना चाहिए था।'),
                  ('कंडक्टर के व्यवहार में परिवर्तन क्यों आया?', f'{n} का त्याग देखकर उसकी संवेदना जाग उठी; उसे अपने रूखेपन का एहसास हुआ।')],
           title=('टिकट', ['बस की सवारी', 'पैदल यात्रा', 'शहर की सड़कें']),
           points=['बुज़ुर्ग महिला का बस में चढ़ना', 'कंडक्टर का रूखा व्यवहार', 'यात्रियों की उदासीनता', f'{n} का किराया देने का निर्णय', 'कंडक्टर का हृदय-परिवर्तन', 'यात्रियों की लज्जा'],
           evals=[('यदि आप उस बस में होते तो क्या करते? कहानी के आधार पर अपने उत्तर का औचित्य बताइए।', 'व्यक्तिगत उत्तर: मदद करना; तर्क — छोटा त्याग भी किसी के लिए बड़ा सहारा; उदासीनता समाज को कठोर बनाती है।')],
           notes={'पात्र': ['बुज़ुर्ग महिला', 'कंडक्टर', n], 'घटना': ['किराया न होना', 'यात्रियों की चुप्पी', f'{n} की पेशकश'], 'परिणाम': ['कंडक्टर का हृदय-परिवर्तन', 'यात्रियों की लज्जा']})
    P.update(purpose='यह दिखाना कि एक व्यक्ति की छोटी-सी संवेदना दूसरों के हृदय को भी बदल सकती है', why_title='पूरी कहानी एक टिकट के इर्द-गिर्द घूमती है; वही टिकट संवेदना की परीक्षा बनता है और कंडक्टर के हृदय-परिवर्तन का कारण भी।',
             alt_title='एक टिकट की कीमत', why_alt='टिकट की असली कीमत पैसे से नहीं, मानवीयता से आँकी गई।', issue='समाज में बढ़ती उदासीनता और बुज़ुर्गों के प्रति संवेदनहीनता',
             change='कंडक्टर पहले रूखा था, पर बच्चे का त्याग देखकर उसने स्वयं टिकट का खर्च उठाया।')
    return P


def st_pyau(r):
    n, g = name(r)
    c = r.choice(INDIA)
    deg = r.choice([44, 45, 46, 47])
    text = A(f'उस साल {c} में गर्मी ने सारे रिकॉर्ड तोड़ दिए थे; पारा {deg} डिग्री तक पहुँच गया था। {n} के घर के सामने मज़दूरों की एक बस्ती थी, जहाँ दोपहर में लोग प्यास से बेहाल रहते। '
             f'{n} ने अपनी गुल्लक तोड़ी और दो बड़े मटके खरीद लाई। पिताजी ने पूछा, “इनका क्या करोगे?” {n} ने कहा, “गेट के बाहर प्याऊ लगाऊँग{{ा}}।” '
             f'पहले दिन मोहल्ले के कुछ लोग हँसे — “दो मटकों से किसकी प्यास बुझेगी?” पर {n} रोज़ सुबह मटके भरत{{ा}} और उन पर गीला कपड़ा लपेट देत{{ा}}। '
             f'एक हफ़्ते में पड़ोस की आंटी ने एक मटका और जोड़ दिया; फिर सामने वाले दुकानदार ने स्टील के गिलास रख दिए। महीने के अंत तक वहाँ सात मटके थे और मोहल्ले के बच्चे बारी-बारी से उन्हें भरते थे।', g)
    text = text.replace('खरीद लाई', 'खरीद लाया' if g == 'm' else 'खरीद लाई')
    P = ex('कहानी का अंश', text,
           facts=[('उस साल तापमान कितने डिग्री तक पहुँच गया था?', f'{deg} डिग्री', [f'{x} डिग्री' for x in (40, 42, 44, 45, 46, 47, 48) if x != deg][:3]),
                  (f'{n} ने मटके खरीदने के लिए पैसे कहाँ से लिए?', 'अपनी गुल्लक तोड़कर', ['पिताजी से माँगकर', 'दुकानदार से उधार लेकर', 'मोहल्ले से चंदा लेकर']),
                  ('महीने के अंत तक प्याऊ पर कितने मटके हो गए?', 'सात', ['दो', 'तीन', 'दस']),
                  ('सामने वाले दुकानदार ने क्या योगदान दिया?', 'स्टील के गिलास रखे', ['एक मटका दिया', 'बर्फ़ दी', 'छाया के लिए तिरपाल लगाया'])],
           vocab=[('बेहाल', 'बहुत परेशान, बुरी दशा में', ['प्रसन्न', 'आलसी', 'स्वस्थ']), ('प्याऊ', 'राहगीरों को मुफ़्त पानी पिलाने का स्थान', ['पानी की टंकी', 'कुआँ', 'दुकान'])],
           tf=[('मोहल्ले के लोगों ने पहले दिन से ही प्याऊ की प्रशंसा की।', False, 'पहले दिन कुछ लोग हँसे थे।'),
               ('मटकों पर गीला कपड़ा पानी ठंडा रखने के लिए लपेटा जाता था।', True, 'गीला कपड़ा मटके के पानी को ठंडा रखता है।')],
           infer=[('मोहल्ले वालों का व्यवहार कैसे बदला और क्यों?', f'पहले वे हँसे, पर {n} की लगन देखकर स्वयं सहयोग करने लगे; एक अच्छे काम ने दूसरों को प्रेरित किया।'),
                  (f'{n} के चरित्र की दो विशेषताएँ लिखिए।', 'संवेदनशील (मज़दूरों की प्यास का ध्यान), दृढ़ और लगनशील (हँसी के बाद भी रोज़ मटके भरे), त्यागी (गुल्लक तोड़ी)।')],
           title=('सात मटके', ['गर्मी की छुट्टियाँ', 'गुल्लक', 'मज़दूरों की बस्ती']),
           points=['भीषण गर्मी', 'मज़दूरों की प्यास', 'गुल्लक तोड़कर मटके', 'लोगों की हँसी', 'पड़ोसियों का सहयोग', 'सात मटकों का प्याऊ'],
           evals=[(f'“अच्छे काम की शुरुआत छोटी होती है” — {n} की कहानी के आधार पर इस कथन की पुष्टि कीजिए।', 'दो मटकों से शुरुआत, लोगों की हँसी, फिर सहयोग से सात मटके; छोटा प्रयास सामूहिक आंदोलन बना।')],
           notes={'समस्या': ['भीषण गर्मी', 'मज़दूरों की प्यास'], 'प्रयास': ['गुल्लक तोड़ी', 'दो मटके', 'रोज़ भरना'], 'परिणाम': ['पड़ोसियों का सहयोग', 'सात मटके', 'बच्चों की भागीदारी']})
    P.update(purpose='यह संदेश देना कि छोटा-सा निःस्वार्थ प्रयास भी पूरे समाज को सहयोग के लिए प्रेरित कर सकता है', why_title='“सात मटके” दो से सात तक बढ़ते सहयोग का प्रतीक है; शीर्षक जिज्ञासा जगाता है और कहानी का परिणाम भी बताता है।',
             alt_title='प्यास का पुल', why_alt='प्याऊ ने अमीर-गरीब मोहल्ले और बस्ती के बीच संवेदना का पुल बनाया।', issue='गरीब मज़दूरों की कठिनाइयों के प्रति समाज की उदासीनता और सामूहिक सहयोग की आवश्यकता',
             change='मोहल्ले के लोग पहले हँसे, बाद में स्वयं मटके और गिलास जोड़कर सहयोगी बन गए।')
    return P


def st_cycle(r):
    n, g = name(r)
    f, fg = name(r)
    cls = r.choice(['सातवीं', 'आठवीं'])
    km = r.choice([4, 5, 6])
    text = A(f'{n} की नीली साइकिल उसे अपनी जान से भी प्यारी थी। जन्मदिन पर मिली उस साइकिल की घंटी तक वह रोज़ चमकात{{ा}}। उसी कक्षा में {f} पढ़त{{ी2}} थ{{ी2}}, जो रोज़ {km} किलोमीटर पैदल चलकर आत{{ी2}} थ{{ी2}} और अक्सर पहली घंटी के बाद पहुँचत{{ी2}}। '
             f'एक दिन बारिश में भीगकर {f} कक्षा में आई तो अध्यापक ने देर से आने पर डाँट दिया। {n} ने देखा कि उसकी चप्पल टूटी हुई थी। '
             f'उस रात {n} देर तक सो न सक{{ा}}। अगली सुबह उसने अपनी नीली साइकिल {f} के घर के सामने खड़ी कर दी और साथ में एक पर्ची छोड़ी — “मेरे पास अब बस है, यह तुम्हारे काम आएगी।” '
             f'उस दिन {n} पहली बार स्कूल बस से ग{{या}}, पर मन में अजीब-सी हल्की खुशी थी।', g)
    text = text.replace('{ी2}', 'ा' if fg == 'm' else 'ी').replace('भीगकर ' + f + ' कक्षा में आई', 'भीगकर ' + f + (' कक्षा में आया' if fg == 'm' else ' कक्षा में आई'))
    P = ex('कहानी का अंश', text,
           facts=[(f'{f} रोज़ कितने किलोमीटर पैदल चलकर विद्यालय आता/आती थी?', f'{km} किलोमीटर', [f'{x} किलोमीटर' for x in (2, 3, 4, 5, 6, 8) if x != km][:3]),
                  (f'{n} को साइकिल कब मिली थी?', 'जन्मदिन पर', ['परीक्षा में प्रथम आने पर', 'दिवाली पर', 'दादाजी के आने पर']),
                  (f'अध्यापक ने {f} को क्यों डाँटा?', 'देर से आने पर', ['गृहकार्य न करने पर', 'शोर मचाने पर', 'किताब भूलने पर']),
                  (f'{n} ने साइकिल के साथ क्या छोड़ा?', 'एक पर्ची', ['घंटी', 'नई चप्पल', 'कुछ पैसे'])],
           vocab=[('पर्ची', 'कागज़ का छोटा टुकड़ा जिस पर कुछ लिखा हो', ['बड़ा पत्र', 'किताब', 'टिकट']), ('अक्सर', 'प्रायः, ज़्यादातर', ['कभी नहीं', 'एक बार', 'तुरंत'])],
           tf=[(f'{n} को अपनी साइकिल प्यारी नहीं थी, इसलिए उसने दे दी।', False, 'साइकिल उसे जान से भी प्यारी थी; फिर भी उसने त्याग किया।'),
               (f'{f} की चप्पल टूटी हुई थी।', True, f'{n} ने देखा कि उसकी चप्पल टूटी हुई थी।')],
           infer=[(f'“उस रात {n} देर तक सो न सक{A("{ा}", g)}” — इसका कारण क्या था?', f'{f} की कठिनाई और उसे मिली डाँट ने {n} के मन को बेचैन कर दिया; वह मदद करने का उपाय सोच रह{A("{ा}", g)} था।'),
                  ('“मन में अजीब-सी हल्की खुशी थी” — यह खुशी कैसी थी?', 'त्याग और दूसरों की सहायता से मिलने वाली आत्मिक संतुष्टि की खुशी।')],
           title=('नीली साइकिल', ['बारिश का दिन', 'स्कूल बस', 'देर से आना']),
           points=[f'{n} की प्यारी साइकिल', f'{f} का रोज़ पैदल आना', 'बारिश में डाँट', 'टूटी चप्पल', 'बेचैन रात', 'साइकिल का उपहार और खुशी'],
           evals=[(f'क्या {n} का निर्णय उचित था? अपने विचार कारण सहित लिखिए।', 'संतुलित उत्तर: त्याग और संवेदना प्रशंसनीय; ज़रूरतमंद की स्थायी मदद; बड़ों से सलाह लेकर करना और भी अच्छा।')],
           notes={'पात्र': [n, f, 'अध्यापक'], 'समस्या': [f'{f} का {km} किमी पैदल आना', 'देर पर डाँट'], 'समाधान': ['साइकिल उपहार में देना', 'स्वयं बस से जाना']})
    P.update(purpose='यह दिखाना कि सच्ची खुशी अपनी प्रिय वस्तु दूसरों की ज़रूरत के लिए त्यागने में है', why_title='नीली साइकिल कहानी की केंद्रीय वस्तु है — पहले वह मोह का प्रतीक है, अंत में त्याग और मित्रता का।',
             alt_title='सबसे हल्की खुशी', why_alt='अंत में त्याग से मिली “हल्की खुशी” कहानी का मर्म है।', issue='ग्रामीण/गरीब विद्यार्थियों की कठिनाइयाँ और उनके प्रति संवेदनशीलता की आवश्यकता',
             change=A(f'{n} पहले साइकिल से बहुत मोह रखत{{ा}} थ{{ा}}, पर {f} की कठिनाई देखकर उसने साइकिल दे दी।', g))
    return P


STORIES_SOC = [st_ticket, st_pyau, st_cycle]

t = topic('कहानी का उद्देश्य और शीर्षक की सार्थकता', 'कहानी का उद्देश्य')
reading(t, STORIES_SOC, 'extract', c4kinds=('eval', 'summary'))
story_purpose(t, STORIES_SOC)
t6_1 = t

UP_PR_L = ['केवल उपसर्ग', 'केवल प्रत्यय', 'उपसर्ग और प्रत्यय दोनों', 'न उपसर्ग, न प्रत्यय']
UP_PR = ([(w, '', 'केवल उपसर्ग', f'{w} = {sp}; आरंभ में उपसर्ग जुड़ा है।') for w, sp in UPSARG[:10]]
         + [(w, '', 'केवल प्रत्यय', f'{w} = {sp}; अंत में प्रत्यय जुड़ा है।') for w, sp in PRATYAY[:10]]
         + [('असफलता', '', 'उपसर्ग और प्रत्यय दोनों', 'अ (उपसर्ग) + सफल + ता (प्रत्यय)।'), ('अपमानित', '', 'उपसर्ग और प्रत्यय दोनों', 'अप (उपसर्ग) + मान + इत (प्रत्यय)।'),
            ('प्रगतिशील', '', 'उपसर्ग और प्रत्यय दोनों', 'प्र (उपसर्ग) + गति + शील (प्रत्यय)।'), ('बेईमानी', '', 'उपसर्ग और प्रत्यय दोनों', 'बे (उपसर्ग) + ईमान + ई (प्रत्यय)।'),
            ('निर्दयता', '', 'उपसर्ग और प्रत्यय दोनों', 'निर् (उपसर्ग) + दया + ता (प्रत्यय)।'),
            ('कमल', '', 'न उपसर्ग, न प्रत्यय', 'यह मूल (रूढ़) शब्द है; इसे सार्थक खंडों में नहीं तोड़ा जा सकता।'), ('पर्वत', '', 'न उपसर्ग, न प्रत्यय', 'यह मूल शब्द है।'),
            ('नदी', '', 'न उपसर्ग, न प्रत्यय', 'यह मूल शब्द है।'), ('घोड़ा', '', 'न उपसर्ग, न प्रत्यय', 'यह मूल शब्द है।')])

t = topic('व्याकरण: उपसर्ग और प्रत्यय', 'उपसर्ग और प्रत्यय')
fx(t, 'C1', (1, 2), [
    ('उपसर्ग शब्द के किस भाग में जुड़ता है?', 'आरंभ में', 'उपसर्ग मूल शब्द से पहले जुड़कर अर्थ बदलता है, जैसे अ + ज्ञान = अज्ञान।', ['अंत में', 'बीच में', 'कहीं भी नहीं']),
    ('प्रत्यय शब्द के किस भाग में जुड़ता है?', 'अंत में', 'प्रत्यय मूल शब्द के बाद जुड़ता है, जैसे मीठा + आस = मिठास।', ['आरंभ में', 'बीच में', 'उपसर्ग से पहले']),
    ('इनमें से कौन-सा शब्द “अ” उपसर्ग से बना है?', 'अज्ञान', '“अ” उपसर्ग “नहीं/अभाव” का अर्थ देता है: अ + ज्ञान।', ['आकाश', 'आलय', 'अमरूद']),
    ('“बचपन” में कौन-सा प्रत्यय है?', 'पन', 'बच्चा + पन = बचपन; “पन” भाववाचक प्रत्यय है।', ['बच', 'अन', 'चपन']),
    ('“दुर्” उपसर्ग प्रायः कैसा अर्थ देता है?', 'बुरा या कठिन', 'दुर् + गुण = दुर्गुण (बुरा गुण), दुर्गम (कठिनाई से जाने योग्य)।', ['अच्छा', 'साथ', 'पीछे']),
])
tagbank(t, UP_PR, UP_PR_L, 'शब्द-रचना (उपसर्ग/प्रत्यय)', noun='शब्द', link=' की', c4=False)
xform(t, splitx(UPSARG, 'उपसर्ग'), 'उपसर्ग और मूल शब्द अलग कीजिए', label='शब्द-विच्छेद')
xform(t, splitx(PRATYAY, 'प्रत्यय'), 'मूल शब्द और प्रत्यय अलग कीजिए', label='शब्द-विच्छेद', c2=False)
t6_2 = t

FORMAL_FACTS = [
    ('औपचारिक पत्र में “सेवा में” के बाद क्या लिखा जाता है?', 'पत्र पाने वाले का पद और पता', ['भेजने वाले का नाम', 'तिथि', 'विषय'], 'प्रारूप: सेवा में, पद, संस्था का नाम और पता।'),
    ('औपचारिक पत्र में “विषय” क्यों लिखा जाता है?', 'ताकि पढ़ने वाला एक पंक्ति में पत्र का उद्देश्य समझ ले', ['पत्र को लंबा बनाने के लिए', 'भेजने वाले का पता बताने के लिए', 'आशीर्वाद देने के लिए'], 'विषय पत्र का सार एक पंक्ति में बताता है।'),
    ('प्रधानाचार्य को लिखे पत्र के अंत में कौन-सा समापन उपयुक्त है?', 'आपका आज्ञाकारी शिष्य / आपकी आज्ञाकारिणी शिष्या', ['तुम्हारा मित्र', 'ढेर सारा प्यार', 'तुम्हारी सखी'], 'औपचारिक और आदरपूर्ण समापन चाहिए।'),
    ('संपादक को पत्र में संबोधन कैसे करते हैं?', 'महोदय / महोदया', ['प्रिय मित्र', 'पूज्य पिताजी', 'प्यारे भाई'], 'औपचारिक संबोधन “महोदय/महोदया” होता है।'),
    ('इनमें से कौन-सा औपचारिक पत्र का विषय है?', 'मोहल्ले में पानी की कमी की शिकायत', ['मित्र को जन्मदिन की बधाई', 'दादी को छुट्टियों का हाल', 'बहन को उपहार के लिए धन्यवाद'], 'शिकायत या प्रार्थना सरकारी/संस्थागत व्यक्ति से की जाती है।'),
    ('औपचारिक पत्र की भाषा कैसी होनी चाहिए?', 'शिष्ट, संक्षिप्त और विषय पर केंद्रित', ['भावुक और लंबी', 'मज़ाकिया और अनौपचारिक', 'केवल अंग्रेज़ी शब्दों वाली'], 'औपचारिक पत्र में अनावश्यक बातें नहीं होतीं।'),
]
FORMAL_FLAWS = [
    ('प्रिय प्रधानाचार्य जी, कैसे हो? मुझे दो दिन की छुट्टी चाहिए।', 'प्रधानाचार्य के लिए “प्रिय” और “कैसे हो” अनौपचारिक व अनादरपूर्ण है; “सेवा में… महोदय/महोदया” होना चाहिए।', 'सेवा में, प्रधानाचार्य महोदय/महोदया, … सविनय निवेदन है कि मुझे दो दिन का अवकाश प्रदान करने की कृपा करें।'),
    ('महोदय, हमारी गली में बहुत गंदगी है। और कल मेरा जन्मदिन था, बहुत मज़ा आया।', 'शिकायती पत्र में विषय से हटकर निजी बातें (जन्मदिन) लिखी गई हैं।', 'महोदय, हमारी गली में कई दिनों से कूड़ा नहीं उठाया गया है, जिससे दुर्गंध और मच्छर बढ़ रहे हैं। कृपया शीघ्र सफ़ाई की व्यवस्था करवाएँ।'),
    ('सेवा में, संपादक महोदय, … तुम्हारा प्यारा, {N}', '“तुम्हारा प्यारा” अनौपचारिक समापन है; संपादक को “भवदीय/भवदीया” लिखना चाहिए।', 'भवदीय/भवदीया, {N}'),
    ('सेवा में, प्रधानाचार्य महोदया, मुझे छुट्टी चाहिए।', 'पत्र में विषय, कारण और अवधि नहीं दी गई; अनुरोध बहुत रूखा है।', 'विषय: तीन दिन के अवकाश हेतु प्रार्थना-पत्र। महोदया, सविनय निवेदन है कि बुखार के कारण मैं 5 से 7 तारीख तक विद्यालय आने में असमर्थ हूँ…'),
    ('महोदय, आप लोग कुछ काम नहीं करते! सड़क टूटी पड़ी है।', 'भाषा आरोपपूर्ण और अशिष्ट है; शिकायत शिष्टता से करनी चाहिए।', 'महोदय, विनम्र निवेदन है कि हमारे क्षेत्र की मुख्य सड़क कई स्थानों पर टूट गई है, जिससे दुर्घटनाओं का खतरा है। कृपया शीघ्र मरम्मत करवाएँ।'),
]


def fl_task(r):
    n, g = name(r)
    c = r.choice(INDIA)
    sit = r.choice([
        ('प्रधानाचार्य', f'अपनी बड़ी बहन के विवाह के कारण तीन दिन के अवकाश के लिए प्रधानाचार्य को प्रार्थना-पत्र लिखिए।',
         ['अवकाश का कारण', 'अवकाश की तिथियाँ', 'छूटे हुए कार्य को पूरा करने का आश्वासन', 'विनम्र अनुरोध'], 'कारण, तिथियाँ, पढ़ाई पूरी करने का आश्वासन; “सविनय निवेदन है कि…”'),
        ('प्रधानाचार्य', 'विद्यालय के पुस्तकालय में हिंदी की नई पुस्तकें और पत्रिकाएँ मँगवाने का अनुरोध करते हुए प्रधानाचार्य को पत्र लिखिए।',
         ['वर्तमान स्थिति (पुरानी/कम पुस्तकें)', 'किस प्रकार की पुस्तकें चाहिए', 'विद्यार्थियों को होने वाला लाभ', 'धन्यवाद सहित अनुरोध'], 'समस्या, सुझाव, लाभ, शिष्ट अनुरोध।'),
        ('संपादक', f'{c} के अपने इलाके में आवारा पशुओं से हो रही परेशानी के बारे में किसी समाचार-पत्र के संपादक को पत्र लिखिए।',
         ['समस्या का वर्णन', 'लोगों, विशेषकर बच्चों-बुज़ुर्गों को होने वाली कठिनाई', 'कोई घटना जो आपने देखी', 'अधिकारियों से अपेक्षित कार्रवाई'], 'समस्या, प्रभाव, उदाहरण-घटना, समाधान की माँग; “भवदीय/भवदीया”।'),
        ('संपादक', f'{c} में बिजली की बार-बार कटौती से विद्यार्थियों की पढ़ाई पर पड़ रहे प्रभाव के बारे में संपादक को पत्र लिखिए।',
         ['कटौती कब और कितनी देर होती है', 'परीक्षा के दिनों में कठिनाई', 'अन्य लोगों पर प्रभाव', 'सुझाव'], 'समस्या का सटीक विवरण, प्रभाव, सुझाव, शिष्ट भाषा।'),
    ])
    who = 'प्रधानाचार्य महोदय/महोदया, (विद्यालय का नाम)' if sit[0] == 'प्रधानाचार्य' else 'संपादक महोदय, (समाचार-पत्र का नाम और पता)'
    close = 'आपका आज्ञाकारी शिष्य / आपकी आज्ञाकारिणी शिष्या' if sit[0] == 'प्रधानाचार्य' else 'भवदीय / भवदीया'
    return {'task': sit[1], 'bullets': sit[2], 'ind': f'प्रारूप: सेवा में, {who}; तिथि; विषय; संबोधन (महोदय/महोदया); मुख्य भाग; समापन ({close}), नाम। ' + sit[3],
            'model': f'मॉडल: सेवा में, {who}। तिथि: 10 सितंबर। विषय: … महोदय/महोदया, सविनय निवेदन है कि … अतः आपसे अनुरोध है कि … धन्यवाद सहित, {close}, {n}।'}


def fl_short(r, D):
    s, prob, fix = r.choice(FORMAL_FLAWS)
    n, g = name(r)
    return (f'औपचारिक पत्र के इस अंश को सुधारकर लिखिए और बताइए कि आपने क्या बदला: {Q(A(s.replace("{N}", n), g))}', A(fix.replace('{N}', n), g) + f' ({prob})', 'शुद्ध, औपचारिक रूप (1); बदलाव का कारण (1); भाषा की शुद्धता')


def fl_subject(r, D):
    T = fl_task(r)
    return (f'{T["task"]}\nइस पत्र के लिए केवल “विषय” पंक्ति, संबोधन और पहला वाक्य लिखिए।', T['model'], 'संक्षिप्त, सटीक विषय (1); औपचारिक संबोधन (1); “सविनय निवेदन है कि…” जैसा उपयुक्त आरंभ')


t = topic('रचना: औपचारिक पत्र लेखन (प्रधानाचार्य/संपादक को)', 'औपचारिक पत्र')
writing(t, 'औपचारिक पत्र', [fl_task], FORMAL_FACTS, FORMAL_FLAWS, [fl_short, fl_subject])
t6_3 = t

DLG_FACTS = [
    ('संवाद लेखन में सबसे आवश्यक क्या है?', 'पात्रों के अनुसार स्वाभाविक, छोटे और प्रसंग से जुड़े कथन', ['लंबे-लंबे वर्णनात्मक अनुच्छेद', 'केवल एक पात्र के कथन', 'हर वाक्य में कठिन शब्द'], 'संवाद बातचीत की तरह स्वाभाविक होते हैं।'),
    ('संवाद में पात्र का नाम कहाँ लिखा जाता है?', 'हर कथन से पहले, उसके बाद कोलन (:) लगाकर', ['केवल अंत में', 'शीर्षक में', 'कहीं नहीं'], 'जैसे — माँ: … बेटा: …'),
    ('संवाद में कोष्ठक ( ) में क्या लिखा जाता है?', 'पात्र के हाव-भाव या क्रिया (जैसे — मुस्कुराते हुए)', ['पात्र का पता', 'संवाद का शीर्षक', 'लेखक का नाम'], 'कोष्ठक के निर्देश बोलने के ढंग को स्पष्ट करते हैं।'),
    ('ग्राहक और दुकानदार के संवाद की भाषा कैसी होनी चाहिए?', 'शिष्ट और स्थिति के अनुरूप', ['कविता जैसी', 'पूरी तरह संस्कृतनिष्ठ', 'अशिष्ट और कठोर'], 'पात्र और स्थिति के अनुसार भाषा चुनी जाती है।'),
    ('अच्छे संवाद का अंत कैसा होना चाहिए?', 'बातचीत किसी निष्कर्ष या समाधान पर पहुँचे', ['अचानक बीच में रुक जाए', 'नए विषय से शुरू हो', 'केवल अभिवादन हो'], 'संवाद का उद्देश्य पूरा होना चाहिए।'),
]
DLG_FLAWS = [
    ('माँ: बेटा, खाना खा लो। बेटा: माँ, मैं खाना खा लूँगा। माँ: बेटा, खाना खा लो।', 'संवाद आगे नहीं बढ़ता; एक ही बात दोहराई गई है, कोई प्रसंग या निष्कर्ष नहीं है।', 'माँ: बेटा, खाना ठंडा हो रहा है। बेटा: (किताब बंद करते हुए) बस यह सवाल पूरा कर लूँ, माँ! माँ: ठीक है, पर दस मिनट में आ जाना।'),
    ('ग्राहक: ए दुकानदार, जल्दी किताब दे! दुकानदार: ले, पकड़।', 'भाषा अशिष्ट है; ग्राहक और दुकानदार की बातचीत में शिष्टता होनी चाहिए।', 'ग्राहक: भैया, कक्षा आठ की हिंदी की किताब है? दुकानदार: जी हाँ, यह लीजिए। एक सौ बीस रुपये हुए।'),
    ('{N} ने अपने मित्र से कहा कि कल मैच है और मित्र ने कहा कि वह आएगा।', 'यह संवाद नहीं, वर्णन (अप्रत्यक्ष कथन) है; पात्रों के नाम और उनके सीधे कथन होने चाहिए।', '{N}: कल हमारा मैच है, तुम आओगे न? मित्र: (उत्साह से) ज़रूर! मैं समय पर पहुँच जाऊँगा।'),
    ('अध्यापक: तुमने गृहकार्य क्यों नहीं किया? विद्यार्थी: मौसम बहुत सुहावना है और आज रविवार है।', 'उत्तर प्रश्न से असंबद्ध है; संवाद तर्कसंगत रूप से आगे नहीं बढ़ता।', 'अध्यापक: तुमने गृहकार्य क्यों नहीं किया? विद्यार्थी: (सिर झुकाकर) क्षमा कीजिए, कल मैं बीमार था। आज शाम तक पूरा कर दूँगा।'),
]


def dlg_task(r):
    n, g = name(r)
    sit = r.choice([
        ('दो मित्रों के बीच परीक्षा की तैयारी को लेकर संवाद लिखिए।', ['एक मित्र की घबराहट', 'दूसरे मित्र के सुझाव', 'समय-सारणी बनाने की बात', 'साथ पढ़ने का निर्णय'], 'घबराहट, सुझाव (समय-सारणी, नींद, अभ्यास), सकारात्मक अंत।'),
        ('पुस्तक-विक्रेता और ग्राहक के बीच संवाद लिखिए।', ['ग्राहक को कौन-सी पुस्तकें चाहिए', 'मूल्य और छूट की बात', 'कोई पुस्तक उपलब्ध न होना', 'भुगतान और धन्यवाद'], 'शिष्ट भाषा, मूल्य-छूट, विकल्प, समापन।'),
        ('माँ और बच्चे के बीच मोबाइल फ़ोन के अधिक प्रयोग को लेकर संवाद लिखिए।', ['माँ की चिंता', 'बच्चे का तर्क', 'दोनों का समझौता', 'नियम तय करना'], 'चिंता, तर्क-प्रतितर्क, आदरपूर्ण भाषा, समझौता।'),
        ('डॉक्टर और रोगी के बीच संवाद लिखिए।', ['रोगी के लक्षण', 'डॉक्टर के प्रश्न', 'दवा और परहेज़', 'अगली जाँच की तिथि'], 'लक्षण, प्रश्न, सलाह, परहेज़, समापन।'),
        ('दो पड़ोसियों के बीच मोहल्ले की सफ़ाई को लेकर संवाद लिखिए।', ['समस्या का उल्लेख', 'एक-दूसरे के सुझाव', 'सबको जोड़ने की योजना', 'अगले रविवार का अभियान'], 'समस्या, सुझाव, योजना, सहयोग का भाव।'),
    ])
    return {'task': sit[0], 'bullets': sit[1], 'ind': f'प्रारूप: पात्रों के नाम और कोलन; छोटे स्वाभाविक कथन; कोष्ठक में हाव-भाव; प्रसंग के अनुसार भाषा; निष्कर्षपूर्ण अंत। ' + sit[2],
            'model': f'मॉडल आरंभ: {n}: (चिंतित स्वर में) … दूसरा पात्र: (मुस्कुराकर) … — संवाद कम-से-कम 8–10 कथनों में आगे बढ़े और समाधान पर समाप्त हो।'}


def dlg_short(r, D):
    s, prob, fix = r.choice(DLG_FLAWS)
    n, g = name(r)
    return (f'इस अंश को सही संवाद-रूप में सुधारकर लिखिए और बताइए कि आपने क्या बदला: {Q(A(s.replace("{N}", n), g))}', A(fix.replace('{N}', n), g) + f' ({prob})', 'सही संवाद-प्रारूप (1); स्वाभाविक, प्रसंगानुकूल कथन (1); बदलाव का कारण')


def dlg_convert(r, D):
    n, g = name(r)
    s = A(f'{n} ने दुकानदार से पूछा कि क्या उनके पास नीले रंग का पेन है। दुकानदार ने कहा कि नीला पेन खत्म हो गया है, पर काला पेन है। {n} ने कहा कि वह काला पेन ही ले लेग{{ा}}।', g)
    ans = A(f'{n}: भैया, क्या आपके पास नीले रंग का पेन है? दुकानदार: नीला तो खत्म हो गया, पर काला पेन है। {n}: ठीक है, काला ही दे दीजिए।', g)
    return (f'इस वर्णन को संवाद के रूप में लिखिए: {Q(s)}', ans, 'पात्रों के नाम-कोलन (1); प्रत्यक्ष कथन में सही परिवर्तन (1); शिष्ट भाषा')


t = topic('रचना: संवाद लेखन', 'संवाद लेखन')
writing(t, 'संवाद', [dlg_task], DLG_FACTS, DLG_FLAWS, [dlg_short, dlg_convert])
t6_4 = t
CHAPTERS[6] = [t6_1, t6_2, t6_3, t6_4]


# =========================================================== G8 · पाठ 7 निबंध — विज्ञान और तकनीक

def es_vardan(r):
    yr = r.choice([1950, 1960, 1970])
    text = (f'विज्ञान ने मनुष्य के जीवन को इतना बदल दिया है कि आज उसके बिना जीवन की कल्पना भी कठिन है। {yr} के आसपास जिन बीमारियों से लाखों लोग मर जाते थे, आज टीकों और दवाओं से उनका उपचार संभव है। '
            'बिजली, मोबाइल फ़ोन और इंटरनेट ने दूरियाँ मिटा दी हैं; गाँव का विद्यार्थी भी घर बैठे दुनिया भर की जानकारी पा सकता है। '
            'किंतु विज्ञान का एक दूसरा पहलू भी है। कारखानों के धुएँ से हवा ज़हरीली हो रही है, प्लास्टिक से धरती और समुद्र भर गए हैं, और विनाशकारी हथियार पूरी मानवता के लिए खतरा बन गए हैं। '
            'वास्तव में विज्ञान स्वयं न वरदान है, न अभिशाप; वह एक शक्ति है। चाकू से फल भी काटा जा सकता है और किसी को चोट भी पहुँचाई जा सकती है। '
            'इसलिए आवश्यक है कि हम विज्ञान का उपयोग विवेक और मानवीय मूल्यों के साथ करें।')
    return ex('निबंध का अंश', text,
              facts=[('लेखक के अनुसार इंटरनेट ने क्या किया है?', 'दूरियाँ मिटा दी हैं', ['बीमारियाँ बढ़ा दी हैं', 'गाँवों को खाली कर दिया है', 'पढ़ाई कठिन बना दी है']),
                     ('लेखक ने विज्ञान की तुलना किससे की है?', 'चाकू से', ['दीपक से', 'नदी से', 'पुस्तक से']),
                     ('इनमें से कौन-सी हानि अंश में नहीं बताई गई?', 'बेरोज़गारी', ['ज़हरीली हवा', 'प्लास्टिक प्रदूषण', 'विनाशकारी हथियार']),
                     ('लेखक के अनुसार विज्ञान वास्तव में क्या है?', 'एक शक्ति, जिसका परिणाम उपयोग पर निर्भर है', ['केवल वरदान', 'केवल अभिशाप', 'एक खेल'])],
              vocab=[('विवेक', 'सही-गलत को पहचानने की बुद्धि', ['क्रोध', 'आलस्य', 'अहंकार']), ('विनाशकारी', 'नष्ट करने वाला', ['बनाने वाला', 'बचाने वाला', 'सजाने वाला'])],
              tf=[('लेखक विज्ञान को पूरी तरह हानिकारक मानता है।', False, 'लेखक के अनुसार विज्ञान न वरदान है, न अभिशाप; वह एक शक्ति है।'),
                  ('टीकों और दवाओं से कई पुरानी घातक बीमारियों का इलाज संभव हुआ है।', True, 'अंश में यही कहा गया है।')],
              infer=[('चाकू के उदाहरण से लेखक क्या सिद्ध करना चाहता है?', 'किसी साधन का अच्छा या बुरा होना उसके उपयोग पर निर्भर करता है; विज्ञान भी ऐसा ही है।'),
                     ('लेखक का मुख्य तर्क क्या है?', 'विज्ञान के लाभ और हानि दोनों हैं; उसका उपयोग विवेक और मानवीय मूल्यों के साथ होना चाहिए।')],
              title=('विज्ञान: वरदान या अभिशाप', ['बिजली का आविष्कार', 'गाँव का विद्यार्थी', 'समुद्र की सैर']),
              points=['विज्ञान ने जीवन बदला', 'चिकित्सा में प्रगति', 'संचार से दूरियाँ मिटीं', 'प्रदूषण और हथियारों का खतरा', 'विज्ञान एक शक्ति — चाकू का उदाहरण', 'विवेकपूर्ण उपयोग आवश्यक'],
              evals=[('क्या आप लेखक के इस विचार से सहमत हैं कि विज्ञान “न वरदान है, न अभिशाप”? दो तर्कों सहित उत्तर दीजिए।', 'सहमति/असहमति दोनों स्वीकार्य; तर्क: उपयोग पर निर्भरता (परमाणु ऊर्जा — बिजली भी, बम भी), इंटरनेट — शिक्षा भी, लत भी।')],
              notes={'लाभ': ['बीमारियों का उपचार', 'बिजली, मोबाइल, इंटरनेट', 'जानकारी तक पहुँच'], 'हानियाँ': ['वायु प्रदूषण', 'प्लास्टिक', 'विनाशकारी हथियार'], 'निष्कर्ष': ['विज्ञान एक शक्ति', 'विवेकपूर्ण उपयोग']})


def es_internet(r):
    hrs = r.choice([3, 4, 5])
    pct = r.choice([60, 65, 70, 75])
    text = (f'एक सर्वेक्षण के अनुसार हमारे देश में लगभग {pct} प्रतिशत किशोर रोज़ इंटरनेट का प्रयोग करते हैं, और उनमें से कई दिन में {hrs} घंटे से अधिक स्क्रीन के सामने रहते हैं। '
            'इंटरनेट ने पढ़ाई के नए द्वार खोले हैं — ऑनलाइन कक्षाएँ, डिजिटल पुस्तकालय और शैक्षिक वीडियो कठिन विषयों को सरल बना देते हैं। '
            'पर इसका अति-प्रयोग नींद की कमी, आँखों की थकान और एकाग्रता में कमी लाता है। सोशल मीडिया पर दिखने वाली “परफ़ेक्ट” ज़िंदगियाँ किशोरों में हीनभावना भी पैदा करती हैं। '
            'समाधान इंटरनेट से दूर भागना नहीं, बल्कि उसका अनुशासित उपयोग है: पढ़ाई और मनोरंजन के लिए समय तय करना, सोने से एक घंटा पहले स्क्रीन बंद करना, और ऑनलाइन मिली हर जानकारी को परखना।')
    return ex('निबंध का अंश', text,
              facts=[('अंश के अनुसार कितने प्रतिशत किशोर रोज़ इंटरनेट का प्रयोग करते हैं?', f'{pct} प्रतिशत', [f'{x} प्रतिशत' for x in (50, 60, 65, 70, 75, 80) if x != pct][:3]),
                     ('लेखक ने इंटरनेट से पढ़ाई का कौन-सा लाभ बताया है?', 'ऑनलाइन कक्षाएँ और शैक्षिक वीडियो कठिन विषय सरल बनाते हैं', ['परीक्षा की आवश्यकता समाप्त होती है', 'अध्यापकों की ज़रूरत नहीं रहती', 'किताबें सस्ती होती हैं']),
                     ('सोने से कितनी देर पहले स्क्रीन बंद करने की सलाह दी गई है?', 'एक घंटा', ['दस मिनट', 'तीन घंटे', 'आधा दिन']),
                     ('लेखक के अनुसार समस्या का समाधान क्या है?', 'इंटरनेट का अनुशासित उपयोग', ['इंटरनेट पूरी तरह बंद करना', 'केवल रात में इंटरनेट चलाना', 'मोबाइल फ़ोन तोड़ देना'])],
              vocab=[('एकाग्रता', 'मन को एक जगह टिकाए रखना', ['बेचैनी', 'थकान', 'उदासी']), ('हीनभावना', 'स्वयं को दूसरों से कम समझने का भाव', ['घमंड', 'प्रसन्नता', 'साहस'])],
              tf=[('लेखक इंटरनेट से पूरी तरह दूर रहने की सलाह देता है।', False, 'लेखक दूर भागने के बजाय अनुशासित उपयोग की बात करता है।'),
                  ('अति-प्रयोग से आँखों की थकान हो सकती है।', True, 'अंश में यह हानि बताई गई है।')],
              infer=[('लेखक ने “परफ़ेक्ट” शब्द को उद्धरण-चिह्नों में क्यों रखा है?', 'यह संकेत करने के लिए कि सोशल मीडिया पर दिखने वाली ज़िंदगियाँ वास्तव में उतनी आदर्श नहीं होतीं — वह दिखावा है।'),
                     ('लेखक का दृष्टिकोण संतुलित क्यों कहा जा सकता है?', 'वह लाभ (पढ़ाई के साधन) और हानियाँ (नींद, एकाग्रता, हीनभावना) दोनों बताकर व्यावहारिक समाधान देता है।')],
              title=('इंटरनेट: सही उपयोग की कला', ['सर्वेक्षण के आँकड़े', 'नींद का महत्व', 'डिजिटल पुस्तकालय']),
              points=[f'{pct}% किशोर रोज़ इंटरनेट पर', 'पढ़ाई के नए साधन', 'नींद, आँखें, एकाग्रता पर दुष्प्रभाव', 'सोशल मीडिया से हीनभावना', 'अनुशासित उपयोग ही समाधान', 'समय तय करना और जानकारी परखना'],
              evals=[('अपनी दिनचर्या में इंटरनेट के अनुशासित उपयोग के लिए आप कौन-से तीन नियम बनाएँगे? अंश से जोड़कर लिखिए।', 'जैसे: पढ़ाई/मनोरंजन का निश्चित समय, सोने से पहले स्क्रीन बंद, जानकारी के स्रोत की जाँच; कारण सहित।')],
              notes={'लाभ': ['ऑनलाइन कक्षाएँ', 'डिजिटल पुस्तकालय', 'शैक्षिक वीडियो'], 'हानियाँ': ['नींद की कमी', 'आँखों की थकान', 'एकाग्रता में कमी', 'हीनभावना'], 'उपाय': ['समय तय करना', 'सोने से पहले स्क्रीन बंद', 'जानकारी परखना']})


def es_solar(r):
    c = r.choice(INDIA)
    units = r.choice([200, 250, 300])
    text = (f'भारत को धूप का वरदान मिला है — साल के लगभग तीन सौ दिन यहाँ तेज़ धूप रहती है। फिर भी हम बिजली के लिए अधिकतर कोयले पर निर्भर हैं, जो धुआँ फैलाता है और जिसके भंडार सीमित हैं। '
            f'सौर ऊर्जा इस समस्या का स्वच्छ समाधान है। {c} के एक गाँव में घरों की छतों पर सौर पैनल लगाए गए; अब हर घर महीने में लगभग {units} यूनिट बिजली स्वयं बनाता है और बची हुई बिजली ग्रिड को बेचता है। '
            'सौर पैनल लगाने का शुरुआती खर्च ज़रूर अधिक है, पर पाँच-छह वर्षों में वह बिजली के बिलों की बचत से निकल आता है। '
            'यदि सरकार सस्ती किस्तों की सुविधा दे और लोग जागरूक हों, तो सौर ऊर्जा देश को स्वच्छ और आत्मनिर्भर बना सकती है।')
    return ex('निबंध का अंश', text,
              facts=[('भारत में साल में लगभग कितने दिन तेज़ धूप रहती है?', 'तीन सौ', ['सौ', 'दो सौ', 'तीन सौ पैंसठ']),
                     ('कोयले की कौन-सी दो कमियाँ बताई गई हैं?', 'धुआँ फैलाता है और भंडार सीमित हैं', ['महँगा और भारी है', 'गीला और ठंडा है', 'दुर्लभ और सुंदर है']),
                     ('गाँव का हर घर महीने में लगभग कितनी बिजली बनाता है?', f'{units} यूनिट', [f'{x} यूनिट' for x in (100, 150, 200, 250, 300, 400) if x != units][:3]),
                     ('सौर पैनल का खर्च कितने वर्षों में निकल आता है?', 'पाँच-छह वर्षों में', ['एक महीने में', 'बीस वर्षों में', 'कभी नहीं'])],
              vocab=[('भंडार', 'जमा किया हुआ संग्रह', ['खाली स्थान', 'बाज़ार', 'रास्ता']), ('आत्मनिर्भर', 'अपनी ज़रूरतें स्वयं पूरी करने वाला', ['दूसरों पर निर्भर', 'आलसी', 'कमज़ोर'])],
              tf=[('सौर पैनल लगाने का शुरुआती खर्च बहुत कम है।', False, 'शुरुआती खर्च अधिक है, पर बचत से निकल आता है।'),
                  ('गाँव के घर बची हुई बिजली ग्रिड को बेचते हैं।', True, 'अंश में यही बताया गया है।')],
              infer=[('लेखक ने “धूप का वरदान” क्यों कहा है?', 'क्योंकि वर्ष भर की तेज़ धूप भारत को बिना प्रदूषण के बिजली बनाने का प्राकृतिक अवसर देती है।'),
                     ('लेखक सौर ऊर्जा के पक्ष में कौन-सा आर्थिक तर्क देता है?', 'शुरुआती खर्च पाँच-छह वर्षों में बिलों की बचत से निकल आता है और बची बिजली बेचकर आय भी होती है।')],
              title=('धूप से उजाला', ['कोयले की खान', 'गाँव का मेला', 'बिजली का बिल']),
              points=['भारत में भरपूर धूप', 'कोयले पर निर्भरता और उसकी कमियाँ', 'सौर ऊर्जा स्वच्छ समाधान', f'गाँव का उदाहरण — {units} यूनिट', 'खर्च और बचत', 'सरकारी सहायता व जागरूकता'],
              evals=[('आपके विद्यालय में सौर पैनल लगाने के पक्ष में प्रधानाचार्य को कौन-से तर्क देंगे? अंश के आधार पर लिखिए।', 'स्वच्छ ऊर्जा, बिल की बचत, बची बिजली की बिक्री, विद्यार्थियों के लिए सीख; शुरुआती खर्च का उत्तर — कुछ वर्षों में वसूली।')],
              notes={'समस्या': ['कोयले पर निर्भरता', 'धुआँ', 'सीमित भंडार'], 'समाधान': ['छतों पर सौर पैनल', 'स्वयं बिजली बनाना', 'बची बिजली बेचना'], 'शर्तें': ['सस्ती किस्तें', 'जन-जागरूकता']})


ESSAYS = [es_vardan, es_internet, es_solar]

t = topic('पाठ के मुख्य विचार और तर्क', 'मुख्य विचार और तर्क')
reading(t, ESSAYS, 'extract', c4kinds=('notes', 'summary', 'eval'))
t7_1 = t

SANDHI_TB = [(w, '', ty, f'{w} = {sp}; {rule}।') for w, sp, ty, rule, ws in SANDHI]
SANDHI_SPLIT = [(w, sp, f'{ty}: {rule}', ws) for w, sp, ty, rule, ws in SANDHI]
SANDHI_JOIN = [(sp, w, f'{ty}: {rule}') for w, sp, ty, rule, ws in SANDHI]

t = topic('व्याकरण: संधि (स्वर संधि)', 'स्वर संधि')
fx(t, 'C1', (1, 2), [
    ('संधि किसे कहते हैं?', 'दो निकटवर्ती वर्णों के मेल से होने वाला परिवर्तन', 'जैसे विद्या + आलय = विद्यालय (आ + आ = आ)।', ['दो शब्दों के बीच योजक लगाना', 'दो वाक्यों को जोड़ना', 'शब्दों का क्रम बदलना']),
    ('स्वर संधि में किनका मेल होता है?', 'स्वर के साथ स्वर का', 'स्वर संधि में पहले शब्द का अंतिम स्वर और दूसरे शब्द का पहला स्वर मिलते हैं।', ['व्यंजन के साथ व्यंजन का', 'विसर्ग के साथ व्यंजन का', 'दो पूरे वाक्यों का']),
    ('अ + इ मिलकर क्या बनते हैं?', 'ए', 'यह गुण संधि का नियम है, जैसे देव + इंद्र = देवेंद्र।', ['ऐ', 'ई', 'ओ']),
    ('अ + ए मिलकर क्या बनते हैं?', 'ऐ', 'यह वृद्धि संधि का नियम है, जैसे एक + एक = एकैक।', ['ए', 'ओ', 'औ']),
    ('इ + अ (भिन्न स्वर) मिलने पर इ का क्या हो जाता है?', 'य्', 'यह यण संधि है, जैसे इति + आदि = इत्यादि (इ → य्)।', ['व्', 'र्', 'ए']),
])
tagbank(t, SANDHI_TB, SANDHI_L, 'संधि का भेद', noun='शब्द', link=' में')
xform(t, SANDHI_SPLIT, 'संधि-विच्छेद कीजिए', label='संधि-विच्छेद')
xform(t, SANDHI_JOIN, 'संधि कीजिए (शब्द जोड़िए)', label='संधि', c1=False, c2=False)
t7_2 = t

ESSAY_FACTS = [
    ('निबंध की भूमिका में क्या लिखा जाता है?', 'विषय का परिचय और पाठक की रुचि जगाने वाला आरंभ', ['सभी तर्कों का विस्तार', 'केवल निष्कर्ष', 'लेखक का पता'], 'भूमिका निबंध का प्रवेश-द्वार है।'),
    ('निबंध के “विस्तार” भाग में क्या होता है?', 'विषय के विभिन्न पक्ष, तर्क और उदाहरण अलग-अलग अनुच्छेदों में', ['केवल एक वाक्य', 'केवल शीर्षक', 'समापन और धन्यवाद'], 'विस्तार निबंध का मुख्य भाग है।'),
    ('उपसंहार में क्या लिखा जाता है?', 'पूरे निबंध का सार, निष्कर्ष या सुझाव', ['नया विषय', 'पहला तर्क', 'केवल प्रश्न'], 'उपसंहार निबंध को पूर्णता देता है।'),
    ('अच्छे निबंध में अनुच्छेद कैसे होने चाहिए?', 'हर अनुच्छेद में एक मुख्य विचार, क्रम से जुड़े हुए', ['सारी बातें एक ही अनुच्छेद में', 'हर वाक्य अलग अनुच्छेद में', 'बिना किसी क्रम के'], 'अनुच्छेद-विभाजन से विचार स्पष्ट होते हैं।'),
    ('निबंध में उद्धरण या आँकड़े देने से क्या लाभ है?', 'तर्क अधिक विश्वसनीय और प्रभावशाली बनते हैं', ['निबंध छोटा हो जाता है', 'भाषा कठिन हो जाती है', 'शीर्षक बदल जाता है'], 'प्रमाण से तर्क पुष्ट होते हैं।'),
]
ESSAY_FLAWS = [
    ('विज्ञान अच्छा है। विज्ञान से बिजली मिलती है। विज्ञान से मोबाइल मिलता है। विज्ञान अच्छा है।', 'वाक्य छोटे और दोहराव वाले हैं; विचारों का विकास, उदाहरण और संयोजक नहीं हैं।', 'विज्ञान ने हमारे जीवन को सुविधाजनक बनाया है; बिजली से घर रोशन हैं और मोबाइल फ़ोन से हम पल भर में दूर बैठे परिजनों से बात कर लेते हैं।'),
    ('उपसंहार: इसके बाद मैं आपको इंटरनेट के तीन और लाभ बताता हूँ।', 'उपसंहार में नए तर्क नहीं, बल्कि सार और निष्कर्ष होना चाहिए।', 'उपसंहार: स्पष्ट है कि इंटरनेट एक उपयोगी साधन है, बशर्ते हम इसका उपयोग संयम और विवेक से करें।'),
    ('भूमिका: सौर ऊर्जा के पाँच लाभ हैं — पहला, दूसरा, तीसरा, चौथा और पाँचवाँ…', 'भूमिका में सारे तर्क गिना दिए गए हैं; भूमिका में केवल परिचय और रुचि जगाने वाला आरंभ होना चाहिए।', 'भूमिका: सूर्य हज़ारों वर्षों से धरती को जीवन देता आया है; क्या वही सूर्य आज हमारी बिजली की समस्या भी हल कर सकता है?'),
    ('मेरे विचार से प्रदूषण बुरा है क्योंकि वह बुरा होता है।', 'तर्क स्वयं को ही दोहराता है; कोई कारण या प्रमाण नहीं दिया गया।', 'प्रदूषण हानिकारक है, क्योंकि दूषित वायु से दमा जैसी बीमारियाँ बढ़ती हैं और बच्चों व बुज़ुर्गों का स्वास्थ्य सबसे अधिक प्रभावित होता है।'),
]


def es_task(r):
    top = r.choice([
        ('विज्ञान के बढ़ते कदम', ['भूमिका — विज्ञान का अर्थ और महत्व', 'दैनिक जीवन में विज्ञान (चिकित्सा, संचार, यातायात)', 'विज्ञान के दुष्परिणाम', 'उपसंहार — विवेकपूर्ण उपयोग'], 'भूमिका, विस्तार में तीन क्षेत्र उदाहरण सहित, दुष्परिणाम, संतुलित उपसंहार।'),
        ('इंटरनेट: लाभ और हानियाँ', ['भूमिका', 'शिक्षा और संचार में लाभ', 'अति-प्रयोग की हानियाँ', 'उपसंहार — संयमित उपयोग'], 'दोनों पक्ष, उदाहरण, व्यक्तिगत अनुभव, संतुलित निष्कर्ष।'),
        ('सौर ऊर्जा: भविष्य की ऊर्जा', ['भूमिका — ऊर्जा संकट', 'सौर ऊर्जा के लाभ', 'कठिनाइयाँ और समाधान', 'उपसंहार'], 'समस्या, लाभ, कठिनाइयाँ, समाधान, आशावादी निष्कर्ष।'),
        ('यदि बिजली न होती', ['भूमिका — कल्पना का आरंभ', 'घर और विद्यालय का बदला हुआ जीवन', 'अस्पताल, उद्योग और संचार पर प्रभाव', 'उपसंहार — बिजली का महत्व और बचत'], 'कल्पनाशील पर तर्कसंगत वर्णन, विविध क्षेत्र, बचत का संदेश।'),
        ('मोबाइल फ़ोन: सुविधा या समस्या', ['भूमिका', 'मोबाइल की सुविधाएँ', 'विद्यार्थियों पर दुष्प्रभाव', 'उपसंहार — मेरा मत'], 'सुविधाएँ, दुष्प्रभाव, उदाहरण, स्पष्ट निजी मत।'),
    ])
    return {'task': f'“{top[0]}” विषय पर एक निबंध लिखिए।', 'bullets': top[1], 'ind': f'संरचना: भूमिका, विस्तार (अलग अनुच्छेद), उपसंहार; तर्क और उदाहरण; संयोजक शब्द। {top[2]}',
            'model': f'मॉडल रूपरेखा: “{top[0]}” — भूमिका (रोचक प्रश्न/उद्धरण से आरंभ), विस्तार (प्रत्येक बिंदु एक अनुच्छेद, उदाहरण सहित), उपसंहार (सार और सुझाव)।'}


def es_intro(r, D):
    T = es_task(r)
    part = r.choice(['भूमिका', 'उपसंहार'])
    return (f'{T["task"]}\nइस निबंध का केवल {part} लगभग 40–50 शब्दों में लिखिए।', T['model'],
            f'{part} का उद्देश्य पूरा (1); विषय से जुड़ाव (1); भाषा और प्रवाह')


t = topic('रचना: निबंध लेखन (भूमिका, विस्तार, उपसंहार)', 'निबंध लेखन')
writing(t, 'निबंध', [es_task], ESSAY_FACTS, ESSAY_FLAWS, [es_intro], words={1: '80–100', 2: '100–120', 3: '120–150', 4: '150–180', 5: '180–200'})
t7_3 = t
CHAPTERS[7] = [t7_1, t7_2, t7_3]


# =========================================================== G8 · पाठ 8 एकांकी — मंच और संवाद

def ek_ghadi(r):
    n, g = name(r, 'm')
    text = (f'(एक साधारण बैठक। दीवार पर पुरानी घड़ी टँगी है जो बंद पड़ी है। दादाजी आरामकुर्सी पर अख़बार पढ़ रहे हैं। {n} हाथ में नई डिजिटल घड़ी लिए प्रवेश करता है।)\n'
            f'{n}: (उत्साह से) दादाजी, देखिए! पापा मेरे लिए नई घड़ी लाए हैं। अब यह पुरानी घड़ी उतार दें? बेकार में दीवार घेरे खड़ी है।\n'
            f'दादाजी: (अख़बार नीचे रखते हुए, धीमे स्वर में) बेकार? यह घड़ी तुम्हारी दादी ने अपनी पहली तनख़्वाह से खरीदी थी।\n'
            f'{n}: पर यह चलती तो है नहीं!\n'
            f'दादाजी: (उठकर घड़ी के पास जाते हैं, उस पर हाथ फेरते हैं) हाँ, चलती नहीं। पर इसकी सुइयाँ उस शाम पर रुकी हैं, जब तुम्हारी दादी आख़िरी बार इसे चाबी देकर गई थीं।\n'
            f'({n} चुप हो जाता है। कुछ क्षण मंच पर सन्नाटा रहता है।)\n'
            f'{n}: (धीरे से) दादाजी… क्या हम इसे ठीक करवा सकते हैं? मैं अपनी नई घड़ी इसके पास ही रख दूँगा।\n'
            f'दादाजी: (मुस्कुराकर उसके सिर पर हाथ रखते हुए) चलो, कल घड़ीसाज़ के पास चलते हैं।\n'
            f'(प्रकाश धीरे-धीरे मंद होता है।)')
    P = ex('एकांकी का अंश', text,
           facts=[('पुरानी घड़ी किसने खरीदी थी?', 'दादी ने, अपनी पहली तनख़्वाह से', ['दादाजी ने', 'पापा ने', f'{n} ने']),
                  (f'{n} पुरानी घड़ी के बारे में क्या चाहता है?', 'उसे दीवार से उतार देना', ['उसे बेच देना', 'उसे सजाना', 'उसे दादाजी को देना']),
                  ('अंत में क्या निर्णय होता है?', 'घड़ी को घड़ीसाज़ से ठीक करवाया जाएगा', ['घड़ी फेंक दी जाएगी', 'नई घड़ी लौटाई जाएगी', 'घड़ी को अलमारी में रखा जाएगा']),
                  ('घड़ी की सुइयाँ कब पर रुकी हैं?', 'उस शाम पर जब दादी ने आख़िरी बार इसे चाबी दी थी', ['दादाजी के जन्मदिन पर', 'सुबह छह बजे पर', 'जब घड़ी गिर गई थी'])],
           vocab=[('घड़ीसाज़', 'घड़ी ठीक करने वाला कारीगर', ['घड़ी बेचने वाला', 'बढ़ई', 'लोहार']), ('सन्नाटा', 'गहरी चुप्पी', ['शोर', 'संगीत', 'हँसी'])],
           tf=[(f'{n} शुरू से ही पुरानी घड़ी का महत्व जानता था।', False, 'वह पहले उसे “बेकार” कहता है; बाद में उसका भावनात्मक महत्व समझता है।'),
               ('पुरानी घड़ी बंद पड़ी है।', True, 'रंग-निर्देश में बताया गया है कि घड़ी बंद पड़ी है।')],
           infer=[('इस अंश में संघर्ष किन दो दृष्टिकोणों के बीच है?', 'नई चीज़ों के आकर्षण (उपयोगिता) और पुरानी चीज़ों से जुड़ी भावनाओं/स्मृतियों के बीच।'),
                  (f'“कुछ क्षण मंच पर सन्नाटा रहता है” — इस रंग-निर्देश का नाटकीय महत्व क्या है?', f'यह {n} के मन में आए परिवर्तन को दिखाता है; दर्शक भी दादाजी के दुख को महसूस कर पाते हैं।')],
           title=('रुकी हुई घड़ी', ['नई घड़ी', 'पुराना अख़बार', 'आरामकुर्सी']),
           points=['नई घड़ी का उत्साह', 'पुरानी घड़ी को बेकार कहना', 'दादी की स्मृति का रहस्य', 'सन्नाटा और परिवर्तन', 'घड़ी ठीक कराने का निर्णय'],
           evals=[('यह अंश पुरानी पीढ़ी और नई पीढ़ी के संबंधों के बारे में क्या कहता है? अपने विचार लिखिए।', 'नई पीढ़ी उपयोगिता देखती है, पुरानी पीढ़ी भावनाएँ; संवाद से दोनों एक-दूसरे को समझ सकते हैं; सम्मान और संवेदना का महत्व।')],
           notes={'पात्र': [n, 'दादाजी'], 'संघर्ष': ['नई घड़ी बनाम पुरानी घड़ी', 'उपयोगिता बनाम स्मृति'], 'समाधान': ['घड़ी ठीक कराना', 'नई घड़ी पास रखना']})
    P.update(chars=[n, 'दादाजी'], setting='एक साधारण बैठक जिसकी दीवार पर पुरानी बंद घड़ी टँगी है',
             dirs=[('(अख़बार नीचे रखते हुए, धीमे स्वर में)', 'दादाजी के मन की उदासी और गंभीरता दिखाना'), ('(उठकर घड़ी के पास जाते हैं, उस पर हाथ फेरते हैं)', 'घड़ी से जुड़ा गहरा लगाव दृश्य रूप में दिखाना'),
                   (f'({n} चुप हो जाता है। कुछ क्षण मंच पर सन्नाटा रहता है।)', f'{n} के मन में आए परिवर्तन और भावनात्मक क्षण को उभारना'), ('(प्रकाश धीरे-धीरे मंद होता है।)', 'दृश्य के शांत, भावुक अंत का संकेत देना')],
             lines=[f'{n}: पर यह चलती तो है नहीं!', 'दादाजी: चलो, कल घड़ीसाज़ के पास चलते हैं।', f'{n}: दादाजी, देखिए! पापा मेरे लिए नई घड़ी लाए हैं।'],
             conflict='नई वस्तु की उपयोगिता और पुरानी वस्तु से जुड़ी स्मृतियों के बीच', resolve=f'{n} दादाजी की भावना समझकर घड़ी ठीक कराने का सुझाव देता है।')
    return P


def ek_result(r):
    n, g = name(r, 'f')
    sub = r.choice(['गणित', 'विज्ञान', 'अंग्रेज़ी'])
    mk_ = r.choice([42, 45, 48])
    text = (f'(रात का समय। रसोई में माँ खाना परोस रही हैं। {n} बस्ता कंधे पर लटकाए, सिर झुकाए धीरे-धीरे प्रवेश करती है।)\n'
            f'माँ: (बिना मुड़े) आ गई? हाथ धो लो, आज तुम्हारी पसंद की खीर बनी है।\n'
            f'{n}: (बस्ता कुर्सी पर रखते हुए, धीमे स्वर में) माँ… आज {sub} का परिणाम आया।\n'
            f'माँ: (मुड़कर, उत्सुकता से) अच्छा! कितने अंक आए?\n'
            f'{n}: (आँखें चुराते हुए) सौ में से {mk_}। (रुककर) मैं जानती हूँ, आप नाराज़ होंगी।\n'
            f'(माँ कुछ क्षण चुप रहती हैं। फिर कटोरी मेज़ पर रखकर {n} के पास बैठ जाती हैं।)\n'
            f'माँ: नाराज़ नहीं हूँ। पर एक बात बताओ — कौन-से प्रश्न गलत हुए, यह देखा?\n'
            f'{n}: (आश्चर्य से) आप डाँटेंगी नहीं?\n'
            f'माँ: (हल्की मुस्कान के साथ) डाँटने से अंक नहीं बढ़ते, बेटा। चलो, खाना खाकर कॉपी साथ बैठकर देखेंगे।\n'
            f'({n} की आँखों में आँसू और चेहरे पर मुस्कान एक साथ आ जाते हैं।)')
    P = ex('एकांकी का अंश', text,
           facts=[(f'{n} का किस विषय का परिणाम आया?', sub, others(r, ['गणित', 'विज्ञान', 'अंग्रेज़ी', 'हिंदी', 'इतिहास'], sub)),
                  (f'{n} को कितने अंक मिले?', f'सौ में से {mk_}', [f'सौ में से {x}' for x in (35, 42, 45, 48, 52, 60) if x != mk_][:3]),
                  ('माँ ने आज क्या बनाया था?', 'खीर', ['हलवा', 'पूरी', 'लड्डू']),
                  ('माँ ने परिणाम सुनकर क्या सुझाव दिया?', 'गलत हुए प्रश्नों को साथ बैठकर देखना', ['ट्यूशन लगवाना', 'खेलना बंद करना', 'अध्यापक से शिकायत करना'])],
           vocab=[('उत्सुकता', 'जानने की तीव्र इच्छा', ['उदासी', 'क्रोध', 'थकान']), ('आँखें चुराना', 'नज़रें न मिलाना (संकोच या लज्जा से)', ['आँखें बंद करना', 'ध्यान से देखना', 'रोना'])],
           tf=[(f'माँ ने {n} को कम अंकों के लिए डाँटा।', False, 'माँ ने कहा कि डाँटने से अंक नहीं बढ़ते; उन्होंने साथ बैठकर कॉपी देखने की बात कही।'),
               (f'{n} को डर था कि माँ नाराज़ होंगी।', True, '“मैं जानती हूँ, आप नाराज़ होंगी।”')],
           infer=[('इस अंश में संघर्ष किस प्रकार का है?', f'आंतरिक संघर्ष — {n} के मन में डर, लज्जा और अपेक्षा का द्वंद्व; साथ ही माँ की प्रतिक्रिया को लेकर तनाव।'),
                  ('“आँखों में आँसू और चेहरे पर मुस्कान एक साथ” — यह मनःस्थिति क्या बताती है?', 'राहत और भावुकता — डर दूर होने की खुशी और माँ के स्नेह से भर आया मन।')],
           title=('डाँट नहीं, साथ', ['खीर', 'रसोई की रात', 'कॉपी']),
           points=[f'{n} का उदास प्रवेश', 'माँ का स्नेहपूर्ण स्वागत', f'{sub} में {mk_} अंक', 'डाँट का डर', 'माँ की समझदारी', 'साथ मिलकर सुधार का निर्णय'],
           evals=[('माँ का व्यवहार आपको कितना उचित लगता है? अपने अनुभव से जोड़कर लिखिए।', 'उचित — डाँट से डर बढ़ता है, समझ से सुधार; गलतियों का विश्लेषण; भावनात्मक सहारा; व्यक्तिगत उदाहरण।')],
           notes={'पात्र': [n, 'माँ'], 'संघर्ष': ['कम अंक', 'डाँट का डर'], 'समाधान': ['माँ की समझदारी', 'कॉपी साथ देखना']})
    P.update(chars=[n, 'माँ'], setting='रात के समय घर की रसोई, जहाँ माँ खाना परोस रही हैं',
             dirs=[('(बस्ता कंधे पर लटकाए, सिर झुकाए धीरे-धीरे प्रवेश करती है।)', f'{n} की उदासी और डर को बिना शब्दों के दिखाना'), ('(आँखें चुराते हुए)', 'संकोच और लज्जा का भाव दिखाना'),
                   ('(माँ कुछ क्षण चुप रहती हैं।)', 'तनाव बढ़ाना; दर्शक माँ की प्रतिक्रिया की प्रतीक्षा करते हैं'), ('(हल्की मुस्कान के साथ)', 'माँ के स्नेह और धैर्य को प्रकट करना')],
             lines=['माँ: डाँटने से अंक नहीं बढ़ते, बेटा।', f'{n}: आप डाँटेंगी नहीं?', 'माँ: आ गई? हाथ धो लो।'],
             conflict=f'{n} के मन के डर और माँ की अपेक्षाओं के बीच (आंतरिक संघर्ष)', resolve='माँ डाँटने के बजाय गलतियाँ साथ बैठकर देखने का निर्णय लेती हैं।')
    return P


def ek_tanki(r):
    a, ag = name(r, 'm')
    text = ('(मोहल्ले का चौक। बीच में पानी की टंकी, जिसके नल से बूँद-बूँद पानी टपक रहा है। कुछ लोग बाल्टियाँ लिए खड़े हैं। शर्मा जी और गुप्ता जी आपस में बहस कर रहे हैं।)\n'
            'शर्मा जी: (ऊँचे स्वर में) तीन दिन से पानी नहीं आया! यह सब गुप्ता जी की वजह से है, इन्होंने मोटर चलाकर सारा पानी अपनी छत की टंकी में भर लिया।\n'
            'गुप्ता जी: (हाथ नचाते हुए) मुझ पर आरोप मत लगाइए! पाइप तो आपके घर के सामने फटा है।\n'
            f'(भीड़ में खुसुर-फुसुर। तभी {a}, हाथ में एक कागज़ लिए, आगे आता है।)\n'
            f'{a}: (शांत स्वर में) अंकल, लड़ने से पानी नहीं आएगा। मैंने कल नगर निगम को शिकायत भेजी थी; यह रही उसकी रसीद। उन्होंने आज शाम मिस्त्री भेजने को कहा है।\n'
            'शर्मा जी: (झेंपते हुए) अरे… हमें तो पता ही नहीं था।\n'
            f'{a}: और जब तक पाइप ठीक न हो, सब लोग बारी-बारी से पानी भरें — मैंने यह सूची बनाई है।\n'
            'गुप्ता जी: (मुस्कुराकर शर्मा जी की ओर हाथ बढ़ाते हुए) चलिए शर्मा जी, पहली बाल्टी आपकी।\n'
            '(सब हँस पड़ते हैं। पर्दा गिरता है।)')
    P = ex('एकांकी का अंश', text,
           facts=[('मोहल्ले में कितने दिन से पानी नहीं आया था?', 'तीन दिन से', ['एक दिन से', 'एक सप्ताह से', 'दो महीने से']),
                  ('शर्मा जी ने किस पर आरोप लगाया?', 'गुप्ता जी पर', [f'{a} पर', 'नगर निगम पर', 'मिस्त्री पर']),
                  (f'{a} ने समस्या के समाधान के लिए क्या किया था?', 'नगर निगम को शिकायत भेजी थी', ['पाइप स्वयं ठीक किया था', 'नई टंकी खरीदी थी', 'पुलिस बुलाई थी']),
                  ('पहली बाल्टी किसकी बताई गई?', 'शर्मा जी की', ['गुप्ता जी की', f'{a} की', 'मिस्त्री की'])],
           vocab=[('झेंपना', 'लज्जित होना, शर्मिंदा होना', ['क्रोधित होना', 'प्रसन्न होना', 'डर जाना']), ('खुसुर-फुसुर', 'धीमी आवाज़ में आपस में बातें', ['ज़ोर का शोर', 'गीत', 'चीख'])],
           tf=[('पाइप गुप्ता जी के घर के सामने फटा था।', False, 'गुप्ता जी के अनुसार पाइप शर्मा जी के घर के सामने फटा है।'),
               (f'{a} ने पानी भरने की बारी की सूची बनाई।', True, '“मैंने यह सूची बनाई है।”')],
           infer=[('इस अंश में संघर्ष किनके बीच है और उसका कारण क्या है?', 'शर्मा जी और गुप्ता जी के बीच; पानी की कमी को लेकर एक-दूसरे पर आरोप।'),
                  (f'{a} के चरित्र की दो विशेषताएँ लिखिए।', 'शांत और समझदार (लड़ाई के बजाय समाधान), ज़िम्मेदार नागरिक (नगर निगम को शिकायत), व्यवस्थित (बारी की सूची)।')],
           title=('टपकती टंकी', ['मोहल्ले का चौक', 'नगर निगम', 'बाल्टियाँ']),
           points=['पानी की कमी और भीड़', 'शर्मा जी और गुप्ता जी की बहस', f'{a} का प्रवेश', 'शिकायत की रसीद', 'बारी की सूची', 'मेल-मिलाप'],
           evals=[('“लड़ने से पानी नहीं आएगा” — यह कथन आज के समाज के लिए कितना प्रासंगिक है? उदाहरण सहित लिखिए।', 'सामूहिक समस्याओं में आरोप-प्रत्यारोप के बजाय संवाद, सही अधिकारी तक शिकायत और सहयोग; मोहल्ले/विद्यालय के उदाहरण।')],
           notes={'पात्र': ['शर्मा जी', 'गुप्ता जी', a], 'संघर्ष': ['पानी की कमी', 'आपसी आरोप'], 'समाधान': ['नगर निगम को शिकायत', 'बारी की सूची', 'मेल-मिलाप']})
    P.update(chars=['शर्मा जी', 'गुप्ता जी', a], setting='मोहल्ले का चौक, जहाँ पानी की टंकी से बूँद-बूँद पानी टपक रहा है',
             dirs=[('(ऊँचे स्वर में)', 'शर्मा जी का क्रोध और झुँझलाहट दिखाना'), ('(हाथ नचाते हुए)', 'गुप्ता जी की उत्तेजना और बचाव का भाव दिखाना'),
                   ('(भीड़ में खुसुर-फुसुर।)', 'मोहल्ले के तनावपूर्ण वातावरण को सजीव करना'), ('(झेंपते हुए)', 'शर्मा जी की लज्जा और भूल का एहसास दिखाना'),
                   ('(सब हँस पड़ते हैं। पर्दा गिरता है।)', 'तनाव के सुखद अंत और दृश्य की समाप्ति का संकेत')],
             lines=['गुप्ता जी: मुझ पर आरोप मत लगाइए!', f'{a}: अंकल, लड़ने से पानी नहीं आएगा।', 'शर्मा जी: अरे… हमें तो पता ही नहीं था।'],
             conflict='शर्मा जी और गुप्ता जी के बीच, पानी की कमी को लेकर (बाहरी संघर्ष)', resolve=f'{a} नगर निगम की शिकायत और बारी की सूची से विवाद सुलझाता है।')
    return P


EKANKI = [ek_ghadi, ek_result, ek_tanki]
EK_INTRO = 'नीचे दिया गया एकांकी का अंश पढ़िए।\n'

t = topic('एकांकी की विशेषताएँ: पात्र, संवाद और रंग-निर्देश', 'एकांकी की विशेषताएँ')
fx(t, 'C1', (1, 2), [
    ('एकांकी में सामान्यतः कितने अंक होते हैं?', 'एक', 'एकांकी = एक अंक का नाटक; कथा एक ही अंक में पूरी होती है।', ['तीन', 'पाँच', 'सात']),
    ('रंग-निर्देश सामान्यतः किस रूप में लिखे जाते हैं?', 'कोष्ठक ( ) में', 'कोष्ठक में मंच-सज्जा, पात्रों के हाव-भाव और प्रकाश-ध्वनि के निर्देश होते हैं।', ['उद्धरण-चिह्नों में', 'शीर्षक के रूप में', 'पद्य के रूप में']),
    ('रंग-निर्देश किसके लिए सबसे अधिक उपयोगी होते हैं?', 'अभिनेताओं और निर्देशक के लिए', 'वे बताते हैं कि मंच कैसा हो और पात्र कैसे बोलें/चलें।', ['केवल परीक्षक के लिए', 'केवल प्रकाशक के लिए', 'केवल संगीतकार के लिए']),
    ('एकांकी की कथा मुख्य रूप से किसके माध्यम से आगे बढ़ती है?', 'पात्रों के संवादों से', 'नाटक में वर्णन कम और संवाद अधिक होते हैं।', ['लंबे वर्णनों से', 'कविताओं से', 'चित्रों से']),
    ('एकांकी में पात्रों की संख्या प्रायः कैसी होती है?', 'सीमित (कम)', 'एक अंक की छोटी कथा में कम पात्र होते हैं ताकि प्रभाव केंद्रित रहे।', ['बहुत अधिक', 'केवल एक', 'अनगिनत']),
])


@t.add('C1', (1, 2, 3))
def ek_c1_dir(r, D):
    P = r.choice(EKANKI)(r)
    d, why = r.choice(P['dirs'])
    ds = r.sample(P['lines'], 3)
    return mq(r, f'{EK_INTRO}{P["text"]}\nइनमें से कौन-सा अंश रंग-निर्देश है?', d, ds, f'कोष्ठक में लिखा यह निर्देश बताता है: {why}।')


@t.add('C1', (1, 2, 3))
def ek_c1_n(r, D):
    P = r.choice(EKANKI)(r)
    k = len(P['chars'])
    w = {2: 'दो', 3: 'तीन', 4: 'चार', 1: 'एक', 5: 'पाँच'}
    return mq(r, f'{EK_INTRO}{P["text"]}\nइस अंश में बोलने वाले पात्र कितने हैं?', w[k], [w[x] for x in (1, 2, 3, 4, 5) if x != k][:3], 'पात्र: ' + ', '.join(P['chars']) + '।')


@t.add('C2', (1, 2, 3, 4), 'explain')
def ek_c2(r, D):
    P = r.choice(EKANKI)(r)
    d, why = r.choice(P['dirs'])
    m = mk('C2', D)
    stem = f'{EK_INTRO}{P["text"]}\nरंग-निर्देश {Q(d)} का दृश्य में क्या महत्व है?' + (' यदि यह निर्देश न हो तो दर्शक पर क्या प्रभाव पड़ेगा?' if m >= 3 else ' उत्तर संक्षेप में दीजिए।')
    return item(stem, f'{why}।' + (' इसके बिना भाव केवल शब्दों पर निर्भर रहेगा और दृश्य का प्रभाव कमज़ोर हो जाएगा।' if m >= 3 else ''),
                'रंग-निर्देश का उद्देश्य (1)' + ('; दृश्य/भाव से संबंध (1)' if m >= 2 else '') + ('; निर्देश न होने का प्रभाव (1)' if m >= 3 else ''), m, 'explain')


@t.add('C3', (1, 2, 3, 4, 5), 'short')
def ek_c3(r, D):
    P = r.choice(EKANKI)(r)
    d, why = r.choice(P['dirs'])
    parts = [
        ('इस अंश के पात्रों के नाम लिखिए।', ', '.join(P['chars']), 'सभी पात्र [1]'),
        ('अंश के आरंभ में दी गई मंच-सज्जा का वर्णन एक वाक्य में कीजिए।', P['setting'], f'{P["setting"]} [1]'),
        (f'रंग-निर्देश {Q(d)} क्या बताता है?', why, f'{why} [1]'),
        ('इस अंश के संवादों की दो विशेषताएँ लिखिए।', 'छोटे, स्वाभाविक और पात्र के स्वभाव के अनुरूप; कथा को आगे बढ़ाते हैं और भाव प्रकट करते हैं', 'कोई दो उपयुक्त विशेषताएँ (1+1) [2]'),
        ('इस अंश में संघर्ष किनके बीच है?', P['conflict'], f'{P["conflict"]} [1]'),
    ]
    return hcompose(r, f'{EK_INTRO}{P["text"]}\nप्रश्नों के उत्तर दीजिए।', parts, k=(2, 3, 4))


@t.add('C4', (2, 3, 4, 5), 'long')
def ek_c4(r, D):
    P = r.choice(EKANKI)(r)
    m = mk('C4', D, True)
    stem = (f'{EK_INTRO}{P["text"]}\n'
            + r.choice([f'इस दृश्य को आगे बढ़ाते हुए 8–10 संवाद लिखिए। इसमें कम-से-कम तीन रंग-निर्देश हों और पात्रों का स्वभाव वही रहे।',
                        f'एकांकी की विशेषताओं (पात्र, संवाद, रंग-निर्देश, मंच-सज्जा, संघर्ष) के आधार पर इस अंश का विश्लेषण कीजिए। प्रत्येक विशेषता के लिए अंश से उदाहरण दीजिए।']))
    if 'आगे बढ़ाते' in stem:
        ans = f'मॉडल: पात्र {", ".join(P["chars"])} — संवाद कथा को आगे बढ़ाएँ (पिछली स्थिति: {P["resolve"].rstrip("।")}), कोष्ठक में हाव-भाव/प्रकाश के निर्देश, पात्रों की भाषा और स्वभाव में निरंतरता।'
        key = f'कथानक की तार्किक निरंतरता (2); संवाद-प्रारूप और स्वाभाविकता (2); कम-से-कम तीन सार्थक रंग-निर्देश (2); भाषा की शुद्धता (शेष अंक) [{m}]'
    else:
        ans = (f'पात्र: {", ".join(P["chars"])}; मंच-सज्जा: {P["setting"]}; रंग-निर्देश: {P["dirs"][0][0]} — {P["dirs"][0][1]}; '
               f'संवाद छोटे और भावपूर्ण; संघर्ष: {P["conflict"]}; समाधान: {P["resolve"]}')
        key = f'प्रत्येक विशेषता उदाहरण सहित (लगभग 1–2 अंक प्रति विशेषता); सुसंगत निष्कर्ष (1) [{m}]'
    return item(stem, ans, key, m, 'long', minutes=min(25, m * 2))


t8_1 = t

t = topic('नाटक का कथानक और संघर्ष', 'कथानक और संघर्ष')
reading(t, EKANKI, 'extract', c4kinds=('summary', 'eval'))


@t.add('C2', (2, 3, 4), 'explain')
def ek_conf(r, D):
    P = r.choice(EKANKI)(r)
    m = mk('C2', D)
    stem = f'{EK_INTRO}{P["text"]}\nइस अंश का संघर्ष कैसे सुलझता है?' + (' संघर्ष के सुलझने में किस पात्र की भूमिका सबसे महत्वपूर्ण है?' if m >= 3 else ' उत्तर संक्षेप में दीजिए।')
    return item(stem, P['resolve'], 'संघर्ष की पहचान (1); समाधान (1)' + ('; मुख्य पात्र की भूमिका (1)' if m >= 3 else '') + f'। अपेक्षित: संघर्ष {P["conflict"]}; {P["resolve"]}', m, 'explain')


t8_2 = t

t = topic('व्याकरण: वाक्य के भेद (रचना और अर्थ के आधार पर)', 'वाक्य के भेद')
fx(t, 'C1', (1, 2), [
    ('रचना के आधार पर वाक्य के कितने भेद होते हैं?', 'तीन', 'सरल, संयुक्त और मिश्र वाक्य।', ['दो', 'पाँच', 'आठ']),
    ('अर्थ के आधार पर वाक्य के कितने भेद होते हैं?', 'आठ', 'विधानवाचक, निषेधवाचक, प्रश्नवाचक, आज्ञावाचक, इच्छावाचक, संदेहवाचक, संकेतवाचक, विस्मयादिबोधक।', ['तीन', 'चार', 'छह']),
    ('मिश्र वाक्य में आश्रित उपवाक्य प्रायः किस शब्द से जुड़ता है?', 'कि / जो / जब / यदि', 'ये शब्द आश्रित उपवाक्य को प्रधान उपवाक्य से जोड़ते हैं।', ['और / तथा', 'या / अथवा', 'पर / लेकिन']),
    ('संयुक्त वाक्य के उपवाक्य कैसे होते हैं?', 'दोनों स्वतंत्र (प्रधान) उपवाक्य', 'संयुक्त वाक्य में समानाधिकरण योजक (और, पर, या, इसलिए) से दो स्वतंत्र उपवाक्य जुड़ते हैं।', ['एक प्रधान, एक आश्रित', 'दोनों आश्रित', 'केवल एक उपवाक्य']),
])
tagbank(t, RACH, RACH_L, 'रचना के आधार पर वाक्य-भेद', RACH_DEF, c1=False)
tagbank(t, ARTH, ARTH_L, 'अर्थ के आधार पर वाक्य-भेद', c4=False)
xform(t, RACH_X, 'निर्देशानुसार वाक्य-परिवर्तन कीजिए', label='वाक्य-परिवर्तन')
t8_3 = t
CHAPTERS[8] = [t8_1, t8_2, t8_3]


# =========================================================== G8 · पाठ 9 यात्रा-वृत्तांत

def tr_jaisalmer(r):
    n, g = name(r)
    hrs = r.choice([6, 7, 8])
    deg = r.choice([41, 42, 43])
    text = A(f'दिल्ली से रात की रेलगाड़ी पकड़कर जब हम सुबह जैसलमेर पहुँचे, तो लगा जैसे किसी सुनहरी कहानी में आ गए हों। पीले पत्थर से बना किला धूप में सोने की तरह चमक रहा था — शायद इसीलिए इसे “सोनार किला” कहते हैं। '
             f'किले के भीतर आज भी लोग रहते हैं; तंग गलियों में रंग-बिरंगे दुपट्टे सूख रहे थे और कहीं से कठपुतली वाले के गीत की आवाज़ आ रही थी। '
             f'दोपहर में पारा {deg} डिग्री था, पर शाम होते ही सम के रेतीले टीलों पर ठंडी हवा चलने लगी। ऊँट की सवारी करते हुए मैं डर के मारे कूबड़ पकड़े बैठ{{ा}} रह{{ा}}, और सब हँसते रहे। '
             f'सूरज ढला तो रेत का रंग पहले नारंगी, फिर गुलाबी और अंत में बैंगनी हो गया। रात को अलाव के पास बैठकर लोक-कलाकारों का संगीत सुनते हुए मैंने सोचा — रेगिस्तान सूना नहीं, सुरों से भरा है।', g)
    return ex('यात्रा-वृत्तांत का अंश', text,
              facts=[('लेखक जैसलमेर कैसे पहुँचा?', 'दिल्ली से रात की रेलगाड़ी से', ['हवाई जहाज़ से', 'अपनी कार से', 'बस से']),
                     ('जैसलमेर के किले को “सोनार किला” क्यों कहते हैं?', 'पीले पत्थर से बना होने के कारण धूप में सोने-सा चमकता है', ['इसमें सोना रखा है', 'इसे सुनारों ने बनाया', 'इसका दरवाज़ा सोने का है']),
                     ('दोपहर में तापमान कितना था?', f'{deg} डिग्री', [f'{x} डिग्री' for x in (38, 40, 41, 42, 43, 45) if x != deg][:3]),
                     ('सूर्यास्त के समय रेत का अंतिम रंग क्या था?', 'बैंगनी', ['नारंगी', 'गुलाबी', 'सफ़ेद'])],
              vocab=[('टीले', 'रेत या मिट्टी के ऊँचे ढेर', ['नदियाँ', 'झीलें', 'खेत']), ('अलाव', 'खुले में जलाई गई आग', ['दीपक', 'चूल्हा', 'टॉर्च'])],
              tf=[('किले के भीतर अब कोई नहीं रहता।', False, 'किले के भीतर आज भी लोग रहते हैं।'),
                  ('शाम को टीलों पर ठंडी हवा चलने लगी।', True, 'अंश में यही वर्णन है।')],
              infer=[('“रेगिस्तान सूना नहीं, सुरों से भरा है” — लेखक ने ऐसा क्यों कहा?', 'लोक-संगीत, कठपुतली के गीत और लोगों की जीवंतता ने दिखाया कि रेगिस्तान संस्कृति और संगीत से भरपूर है।'),
                     ('लेखक के अनुभव में हास्य का कौन-सा प्रसंग है?', 'ऊँट की सवारी में डरकर कूबड़ पकड़े बैठे रहना और सबका हँसना।')],
              title=('सुनहरी रेत के सुर', ['रेल की यात्रा', 'ऊँट का कूबड़', 'दिल्ली की रात']),
              points=['रात की रेल से जैसलमेर', 'सोनार किला', 'किले की जीवंत गलियाँ', 'सम के टीले और ऊँट-सवारी', 'रेत के बदलते रंग', 'अलाव और लोक-संगीत'],
              evals=[('इस वृत्तांत को पढ़कर क्या आप जैसलमेर जाना चाहेंगे? लेखक के वर्णन से दो कारण दीजिए।', 'हाँ/नहीं कारण सहित: सोनार किला, टीलों पर सूर्यास्त, लोक-संगीत; गर्मी का उल्लेख।')],
              notes={'स्थान': ['सोनार किला', 'सम के टीले'], 'अनुभव': ['ऊँट-सवारी का डर', 'सूर्यास्त के रंग', 'लोक-संगीत'], 'मौसम': [f'दोपहर {deg} डिग्री', 'शाम को ठंडी हवा']})


def tr_kerala(r):
    n, g = name(r)
    hrs = r.choice([5, 6])
    text = A(f'केरल के अलप्पुझा में हमने एक हाउसबोट पर पूरा दिन बिताया। नारियल की चटाइयों और बाँस से बनी यह नाव किसी तैरते घर जैसी थी — उसमें रसोई, बैठक और सोने का कमरा, सब कुछ था। '
             f'नाव धीरे-धीरे बैकवॉटर की शांत नहरों में बढ़ती रही। दोनों ओर नारियल के ऊँचे पेड़ पानी में झुककर अपनी परछाईं निहार रहे थे। किनारे पर बच्चे छोटी नावों में स्कूल जा रहे थे और औरतें घाट पर कपड़े धो रही थीं। '
             f'दोपहर को नाविक ने केले के पत्ते पर चावल, मछली और नारियल की चटनी परोसी — ऐसा स्वाद मैंने पहले कभी नहीं चखा था। '
             f'लगभग {hrs} घंटे की इस यात्रा में मुझे समझ आया कि यहाँ पानी केवल सुंदरता नहीं, लोगों के जीवन का रास्ता है।', g)
    return ex('यात्रा-वृत्तांत का अंश', text,
              facts=[('लेखक ने हाउसबोट की यात्रा कहाँ की?', 'केरल के अलप्पुझा में', ['गोवा में', 'कश्मीर की डल झील में', 'मुंबई में']),
                     ('हाउसबोट किन चीज़ों से बनी थी?', 'नारियल की चटाइयों और बाँस से', ['लोहे और प्लास्टिक से', 'ईंट और सीमेंट से', 'केवल लकड़ी के तख्तों से']),
                     ('किनारे पर बच्चे स्कूल कैसे जा रहे थे?', 'छोटी नावों में', ['साइकिल से', 'बस से', 'पैदल']),
                     ('भोजन किस पर परोसा गया?', 'केले के पत्ते पर', ['स्टील की थाली में', 'कागज़ की प्लेट में', 'मिट्टी के बर्तन में'])],
              vocab=[('परछाईं', 'प्रकाश के रुकने से बनी छाया-आकृति', ['आवाज़', 'सुगंध', 'लहर']), ('निहारना', 'प्रेम या ध्यान से देखना', ['छिपना', 'सुनना', 'भागना'])],
              tf=[('हाउसबोट में सोने का कमरा नहीं था।', False, 'उसमें रसोई, बैठक और सोने का कमरा, सब कुछ था।'),
                  ('लेखक को दोपहर का भोजन बहुत स्वादिष्ट लगा।', True, '“ऐसा स्वाद मैंने पहले कभी नहीं चखा था।”')],
              infer=[('“पानी केवल सुंदरता नहीं, लोगों के जीवन का रास्ता है” — आशय स्पष्ट कीजिए।', 'नहरें ही वहाँ के आवागमन, स्कूल जाने, कपड़े धोने और रोज़गार (नाव, मछली) का माध्यम हैं।'),
                     ('“नारियल के पेड़ अपनी परछाईं निहार रहे थे” — इस पंक्ति में कौन-सा अलंकार है?', 'मानवीकरण — पेड़ों पर मनुष्य की तरह निहारने की क्रिया का आरोप।')],
              title=('तैरते घर की एक दिन की यात्रा', ['केरल का भोजन', 'नारियल के पेड़', 'स्कूल की नाव']),
              points=['अलप्पुझा में हाउसबोट', 'तैरते घर जैसी नाव', 'नहरें और नारियल के पेड़', 'किनारे का जीवन', 'केले के पत्ते पर भोजन', 'पानी — जीवन का रास्ता'],
              evals=[('लेखक ने केरल के लोगों के जीवन के बारे में क्या सीखा? आपके अपने इलाके के जीवन से इसकी तुलना कीजिए।', 'पानी पर निर्भर जीवन — नाव से स्कूल, घाट; तुलना: सड़क/बस आधारित जीवन; प्रकृति से तालमेल।')],
              notes={'नाव': ['नारियल की चटाई और बाँस', 'रसोई, बैठक, कमरा'], 'दृश्य': ['शांत नहरें', 'नारियल के पेड़', 'नाव से स्कूल जाते बच्चे'], 'अनुभव': ['केले के पत्ते पर भोजन', f'लगभग {hrs} घंटे की यात्रा']})


def tr_darjeeling(r):
    n, g = name(r)
    t_ = r.choice(['चार', 'साढ़े चार', 'पाँच'])
    text = A(f'दार्जिलिंग में हमारी सुबह चार बजे शुरू हुई, क्योंकि टाइगर हिल से सूर्योदय देखना था। कड़ाके की ठंड में हम शॉल लपेटे सैकड़ों लोगों के बीच खड़े थे। '
             f'अचानक दूर कंचनजंगा की चोटी पर पहली किरण पड़ी — बर्फ़ पहले गुलाबी हुई, फिर सुनहरी, और फिर चाँदी-सी चमक उठी। भीड़ में एक साथ “वाह!” की आवाज़ गूँजी। '
             f'बाद में हम खिलौना-रेल में बैठे, जो पहाड़ों के घुमावदार रास्तों पर धीरे-धीरे सीटी बजाती चलती है। रास्ते में चाय के बागानों में महिलाएँ पीठ पर टोकरियाँ बाँधे पत्तियाँ तोड़ रही थीं। '
             f'वहाँ के लोगों की मुस्कान और सादगी ने मुझे सबसे अधिक प्रभावित किया। लौटते हुए मैंने चाय का एक छोटा पैकेट खरीदा, ताकि घर पर उस सुबह की खुशबू याद रहे।', g)
    return ex('यात्रा-वृत्तांत का अंश', text,
              facts=[('लेखक सुबह जल्दी क्यों उठा?', 'टाइगर हिल से सूर्योदय देखने के लिए', ['रेल पकड़ने के लिए', 'चाय तोड़ने के लिए', 'बाज़ार जाने के लिए']),
                     ('सूर्य की पहली किरण किस चोटी पर पड़ी?', 'कंचनजंगा', ['एवरेस्ट', 'नंदा देवी', 'टाइगर हिल']),
                     ('खिलौना-रेल कैसे चलती है?', 'घुमावदार रास्तों पर धीरे-धीरे सीटी बजाती हुई', ['बहुत तेज़ गति से', 'सुरंग के भीतर', 'नदी के ऊपर पुल पर']),
                     ('लेखक ने लौटते समय क्या खरीदा?', 'चाय का एक छोटा पैकेट', ['एक शॉल', 'एक खिलौना-रेल', 'एक टोकरी'])],
              vocab=[('कड़ाके की ठंड', 'बहुत तेज़ सर्दी', ['हल्की गर्मी', 'बारिश', 'उमस']), ('बागान', 'बड़ा बाग़, जहाँ एक तरह के पौधे उगाए जाते हैं', ['जंगल', 'रेगिस्तान', 'बाज़ार'])],
              tf=[('टाइगर हिल पर लेखक अकेला था।', False, 'वह सैकड़ों लोगों के बीच खड़ा था।'),
                  ('चाय के बागानों में महिलाएँ पत्तियाँ तोड़ रही थीं।', True, 'अंश में यही वर्णन है।')],
              infer=[('बर्फ़ के बदलते रंगों का वर्णन लेखक की किस भावना को दिखाता है?', 'प्रकृति के सौंदर्य के प्रति विस्मय और आनंद।'),
                     ('लेखक ने चाय का पैकेट क्यों खरीदा?', 'यात्रा की स्मृति (उस सुबह की खुशबू) को सँजोकर रखने के लिए।')],
              title=('कंचनजंगा की पहली किरण', ['चाय का पैकेट', 'घर वापसी', 'शॉल की गरमाहट']),
              points=['सुबह चार बजे टाइगर हिल', 'कंचनजंगा पर सूर्योदय', 'बर्फ़ के बदलते रंग', 'खिलौना-रेल की यात्रा', 'चाय-बागान', 'लोगों की सादगी और स्मृति'],
              evals=[('यात्रा-वृत्तांत में लेखक के व्यक्तिगत अनुभव क्यों महत्वपूर्ण होते हैं? इस अंश के उदाहरणों से समझाइए।', 'वे वर्णन को सजीव और विश्वसनीय बनाते हैं: ठंड, भीड़ की “वाह”, चाय का पैकेट; पाठक स्वयं को वहाँ महसूस करता है।')],
              notes={'स्थान': ['टाइगर हिल', 'कंचनजंगा', 'चाय-बागान'], 'अनुभव': ['कड़ाके की ठंड', 'सूर्योदय', 'खिलौना-रेल'], 'प्रभाव': ['लोगों की सादगी', 'चाय की खुशबू की याद']})


TRAVELS = [tr_jaisalmer, tr_kerala, tr_darjeeling]

t = topic('यात्रा-वृत्तांत का वर्णन और लेखक के अनुभव', 'यात्रा-वृत्तांत')
reading(t, TRAVELS, 'extract')
t9_1 = t

SAMAS_TB = [(w, '', ty, f'विग्रह: {vg}।') for w, vg, ty in SAMAS]
SAMAS_VG = [(w, vg, f'{ty}; {SAMAS_DEF[ty].split(";")[0]}।') for w, vg, ty in SAMAS]

t = topic('व्याकरण: समास (तत्पुरुष, द्वंद्व, द्विगु, कर्मधारय)', 'समास')
fx(t, 'C1', (1, 2), [
    ('समास का शाब्दिक अर्थ क्या है?', 'संक्षेप (छोटा करना)', 'दो या अधिक पदों को मिलाकर एक छोटा, सार्थक पद बनाना।', ['विस्तार', 'मेल-मिलाप', 'विरोध']),
    ('समस्त पद के पदों को अलग करके लिखने को क्या कहते हैं?', 'समास-विग्रह', 'जैसे राजपुत्र → राजा का पुत्र।', ['संधि-विच्छेद', 'उपसर्ग', 'प्रत्यय']),
    ('जिस समास का पहला पद संख्यावाचक हो, वह कौन-सा है?', 'द्विगु समास', 'जैसे चौराहा — चार राहों का समूह।', ['द्वंद्व समास', 'तत्पुरुष समास', 'कर्मधारय समास']),
    ('द्वंद्व समास के विग्रह में प्रायः कौन-सा योजक आता है?', 'और / या', 'दोनों पद प्रधान होते हैं, जैसे माता-पिता — माता और पिता।', ['का / की', 'के समान', 'है जो']),
    ('“नीलकमल” का विग्रह “नीला है जो कमल” किस समास का संकेत है?', 'कर्मधारय समास', 'विशेषण (नीला) + विशेष्य (कमल) — कर्मधारय।', ['द्विगु समास', 'द्वंद्व समास', 'तत्पुरुष समास']),
])
tagbank(t, SAMAS_TB, SAMAS_L4, 'समास का भेद', SAMAS_DEF, noun='समस्त पद', link=' में')
xform(t, SAMAS_VG, 'समास-विग्रह कीजिए', label='समास-विग्रह')
t9_2 = t

NOTICE_FACTS = [
    ('सूचना के सबसे ऊपर क्या लिखा जाता है?', 'संस्था का नाम और “सूचना” शब्द', ['लिखने वाले के हस्ताक्षर', 'केवल तिथि', 'धन्यवाद'], 'प्रारूप: संस्था का नाम, “सूचना”, तिथि, शीर्षक, विवरण, नाम-पद।'),
    ('सूचना की भाषा कैसी होनी चाहिए?', 'संक्षिप्त, स्पष्ट और औपचारिक', ['लंबी और भावुक', 'कविता जैसी', 'मज़ाकिया'], 'सूचना में कम शब्दों में पूरी जानकारी।'),
    ('विज्ञापन का मुख्य उद्देश्य क्या है?', 'किसी वस्तु/सेवा की ओर लोगों का ध्यान आकर्षित करना', ['किसी को शिकायत भेजना', 'कहानी सुनाना', 'परीक्षा का परिणाम बताना'], 'विज्ञापन आकर्षक नारे और जानकारी से ग्राहक जोड़ता है।'),
    ('सूचना में कौन-सी जानकारी अनिवार्य है?', 'क्या, कब, कहाँ और किसके लिए', ['लेखक का जन्मदिन', 'मौसम का हाल', 'पिछले साल की घटनाएँ'], 'पाठक को कार्यक्रम/निर्देश की पूरी जानकारी मिलनी चाहिए।'),
    ('विज्ञापन में “नारा” (स्लोगन) क्यों दिया जाता है?', 'ताकि बात छोटी, आकर्षक और याद रखने योग्य बने', ['ताकि विज्ञापन लंबा हो', 'ताकि मूल्य छिपाया जा सके', 'ताकि शिकायत दर्ज हो'], 'नारा विज्ञापन की पहचान बनता है।'),
]
NOTICE_FLAWS = [
    ('सूचना — कल एक कार्यक्रम है, सब लोग आएँ।', 'कार्यक्रम का नाम, तिथि, समय, स्थान और जारी करने वाले का नाम नहीं है।', 'आदर्श विद्यालय — सूचना, 5 अगस्त। “वृक्षारोपण दिवस”: 8 अगस्त को सुबह 9 बजे विद्यालय-प्रांगण में… — {N}, सचिव, पर्यावरण क्लब'),
    ('प्यारे दोस्तो, आपको बताते हुए बहुत खुशी हो रही है कि हमारे स्कूल में बहुत मज़ेदार चीज़ होने वाली है और…', 'सूचना की भाषा औपचारिक और संक्षिप्त नहीं; मुख्य जानकारी देर से और अस्पष्ट है।', 'सूचना: विद्यालय में 12 सितंबर को अंतर-सदन वाद-विवाद प्रतियोगिता होगी। इच्छुक विद्यार्थी 8 सितंबर तक नाम दें।'),
    ('सूचना: सभी विद्यार्थी ध्यान दें — कल विद्यालय बंद रहेगा।', 'तिथि, अवकाश का कारण और सूचना जारी करने वाले का नाम-पद नहीं दिया गया।', 'आदर्श विद्यालय — सूचना, 14 नवंबर। कल 15 नवंबर को स्थानीय पर्व के कारण विद्यालय बंद रहेगा। — {N}, सचिव, विद्यार्थी परिषद'),
    ('विज्ञापन: हमारी दुकान में किताबें मिलती हैं।', 'विज्ञापन में आकर्षण, नारा, विशेष छूट और संपर्क जानकारी नहीं है।', '“ज्ञान का खज़ाना, अब आपके पास!” — ज्ञानदीप पुस्तक भंडार: हर किताब पर 20% छूट; पता: मुख्य बाज़ार; संपर्क: 98765 43210'),
]


def notice_task(r):
    n, g = name(r)
    ev = r.choice([
        ('विद्यालय में होने वाले “पुस्तक मेले” के बारे में', ['मेले की तिथि और समय', 'स्थान', 'क्या-क्या उपलब्ध होगा', 'संपर्क व्यक्ति']),
        ('विद्यालय की बस का समय बदलने के बारे में', ['पुराना और नया समय', 'कब से लागू', 'कारण', 'संपर्क व्यक्ति']),
        ('सोसाइटी में दो दिन पानी की आपूर्ति बंद रहने के बारे में', ['तिथियाँ और समय', 'कारण (टंकी की सफ़ाई)', 'निवासियों से अनुरोध', 'जारीकर्ता का नाम-पद']),
        ('विद्यालय में “स्वच्छता सप्ताह” के आयोजन के बारे में', ['तिथियाँ', 'होने वाली गतिविधियाँ', 'भाग लेने का तरीका', 'संपर्क व्यक्ति']),
    ])
    return {'task': f'{ev[0]} एक सूचना लिखिए। आप {n} हैं, विद्यार्थी परिषद के सचिव।', 'bullets': ev[1],
            'ind': 'प्रारूप: संस्था का नाम; “सूचना”; तिथि; आकर्षक शीर्षक; क्या-कब-कहाँ-किसके लिए; जारीकर्ता का नाम और पद; बॉक्स में।',
            'model': f'मॉडल: (संस्था का नाम) — सूचना — तिथि। शीर्षक। संक्षिप्त विवरण (क्या, कब, कहाँ, किसके लिए)। {n}, सचिव, विद्यार्थी परिषद।'}


def ad_task(r):
    item_ = r.choice([
        ('घर की बनी जैविक सब्ज़ियों की एक नई दुकान', ['नारा', 'विशेषताएँ (ताज़ा, रसायन-मुक्त)', 'उद्घाटन छूट', 'पता और संपर्क']),
        ('बच्चों के लिए गर्मी की छुट्टियों का चित्रकला शिविर', ['आकर्षक नारा', 'आयु-वर्ग और समय', 'शुल्क और सुविधाएँ', 'पंजीकरण का तरीका']),
        ('पुरानी किताबें दान करने का अभियान', ['प्रेरक नारा', 'कौन-सी किताबें', 'कहाँ और कब जमा करें', 'किसे लाभ होगा']),
        ('एक नए साइकिल-मरम्मत केंद्र', ['नारा', 'सेवाएँ और दरें', 'विशेष छूट', 'पता, समय और संपर्क']),
    ])
    return {'task': f'{item_[0]} के लिए एक आकर्षक विज्ञापन तैयार कीजिए।', 'bullets': item_[1],
            'ind': 'आकर्षक शीर्षक/नारा; मुख्य विशेषताएँ; छूट/प्रस्ताव; पता-संपर्क; कम शब्दों में प्रभावशाली प्रस्तुति (बॉक्स में)।',
            'model': f'मॉडल: “नारा!” — {item_[0]}: विशेषताएँ… विशेष छूट… पता… संपर्क…'}


t = topic('रचना: सूचना और विज्ञापन लेखन', 'सूचना और विज्ञापन')
writing(t, 'सूचना', [notice_task], NOTICE_FACTS, NOTICE_FLAWS, words={1: '20–30', 2: '25–35', 3: '30–40', 4: '40–50', 5: '50–60'})
writing(t, 'विज्ञापन', [ad_task], (), (), c1=False, c2=False, words={1: '20–30', 2: '25–35', 3: '30–40', 4: '40–50', 5: '50–60'})
t9_3 = t

EMAIL_FACTS = [
    ('ई-मेल में “विषय” पंक्ति का क्या काम है?', 'ई-मेल का उद्देश्य एक नज़र में बताना', ['भेजने वाले का पता लिखना', 'संलग्न फ़ाइल खोलना', 'ई-मेल को लंबा करना'], 'पाने वाला विषय पढ़कर ही मेल का महत्व समझ लेता है।'),
    ('औपचारिक ई-मेल का समापन कैसा होना चाहिए?', 'धन्यवाद सहित, भवदीय/भवदीया और नाम', ['ढेर सारा प्यार', 'बाय-बाय', 'बिना किसी समापन के'], 'औपचारिक मेल शिष्ट समापन से पूरा होता है।'),
    ('ई-मेल की भाषा कैसी होनी चाहिए?', 'संक्षिप्त, स्पष्ट और पाने वाले के अनुरूप', ['बहुत लंबी और भावुक', 'केवल अंग्रेज़ी में', 'संक्षिप्त रूपों से भरी (जैसे “प्लीज़ कॉल”)'], 'ई-मेल तुरंत पढ़ा जाता है, इसलिए बात सीधी हो।'),
    ('ई-मेल में “प्रति” के स्थान पर क्या लिखा जाता है?', 'पाने वाले का ई-मेल पता', ['भेजने वाले का फ़ोन नंबर', 'विषय', 'तिथि'], 'ई-मेल का “प्रति” पता बताता है कि मेल किसे जा रहा है।'),
    ('ई-मेल का पत्र से मुख्य अंतर क्या है?', 'ई-मेल तुरंत पहुँचता है और उसमें फ़ाइल संलग्न की जा सकती है', ['ई-मेल में संबोधन नहीं होता', 'ई-मेल हमेशा कविता में होता है', 'ई-मेल में विषय नहीं होता'], 'गति और संलग्नक ई-मेल की विशेषता है।'),
]
EMAIL_FLAWS = [
    ('विषय: कुछ नहीं', '“विषय” पंक्ति खाली/अर्थहीन है; उसमें मेल का उद्देश्य होना चाहिए।', 'विषय: विज्ञान-प्रदर्शनी में भाग लेने की अनुमति हेतु'),
    ('आदरणीय महोदया, मुझे कल की क्लास के नोट्स भेज दो ना प्लीज़, जल्दी!!!', 'औपचारिक संबोधन के बाद भाषा अनौपचारिक और अशिष्ट है; विस्मयादि चिह्नों की भरमार।', 'आदरणीय महोदया, कृपया कल की कक्षा के नोट्स भेजने का कष्ट करें। मैं अस्वस्थता के कारण अनुपस्थित थ{ा}। धन्यवाद।'),
    ('आदरणीय महोदय, मुझे कल की कक्षा के नोट्स चाहिए। कृपया भेज दें।', 'मेल के अंत में समापन और भेजने वाले का नाम नहीं है।', 'धन्यवाद सहित, भवदीय/भवदीया, {N}, कक्षा आठ'),
    ('प्रिय मित्र, … भवदीय, {N}', 'मित्र को भेजे ई-मेल में “भवदीय” जैसा औपचारिक समापन उचित नहीं है।', 'तुम्हारा मित्र / तुम्हारी सखी, {N}'),
]


def email_task(r):
    n, g = name(r)
    sit = r.choice([
        ('अपनी कक्षा-अध्यापिका को ई-मेल लिखकर बीमारी के कारण दो दिन की छुट्टी और गृहकार्य की जानकारी माँगिए।', ['अनुपस्थिति का कारण और तिथियाँ', 'छूटे हुए गृहकार्य के बारे में अनुरोध', 'वापस आने की तिथि', 'धन्यवाद']),
        ('पुस्तकालय-प्रभारी को ई-मेल लिखकर खोई हुई पुस्तक के बारे में सूचित कीजिए और जुर्माने की जानकारी माँगिए।', ['पुस्तक का नाम और कब ली', 'खोने की परिस्थिति', 'क्षमा-याचना', 'जुर्माना/नई पुस्तक देने का प्रस्ताव']),
        ('अपने मित्र को ई-मेल लिखकर विद्यालय की यात्रा की तस्वीरें भेजिए और यात्रा का अनुभव बताइए।', ['संलग्न तस्वीरों का उल्लेख', 'यात्रा की सबसे अच्छी बात', 'एक मज़ेदार घटना', 'मिलने की योजना']),
        ('खेल-शिक्षक को ई-मेल लिखकर विद्यालय की फ़ुटबॉल टीम में शामिल होने की इच्छा व्यक्त कीजिए।', ['अपना परिचय', 'खेल का अनुभव', 'टीम में शामिल होने का कारण', 'चयन-परीक्षा के बारे में प्रश्न']),
    ])
    return {'task': sit[0], 'bullets': sit[1], 'ind': 'प्रारूप: प्रति (ई-मेल पता), विषय, संबोधन, मुख्य भाग (संक्षिप्त अनुच्छेद), समापन, नाम; पाने वाले के अनुरूप भाषा।',
            'model': f'मॉडल: प्रति: …@… विषय: … संबोधन: आदरणीय महोदया/प्रिय मित्र, … मुख्य भाग … धन्यवाद सहित, {n}।'}


def email_short(r, D):
    s, prob, fix = r.choice(EMAIL_FLAWS)
    n, g = name(r)
    return (f'ई-मेल के इस अंश को सुधारकर लिखिए और बताइए कि आपने क्या बदला: {Q(A(s.replace("{N}", n), g))}', A(fix.replace('{N}', n), g) + f' ({prob})', 'शुद्ध, उपयुक्त रूप (1); बदलाव का कारण (1); भाषा की शुद्धता')


t = topic('रचना: ई-मेल लेखन', 'ई-मेल लेखन')
writing(t, 'ई-मेल', [email_task], EMAIL_FACTS, EMAIL_FLAWS, [email_short])
t9_4 = t
CHAPTERS[9] = [t9_1, t9_2, t9_3, t9_4]


# =========================================================== G8 · पाठ 10 कविता — प्रेरणा और संघर्ष

P_PRERNA = [
    poem('चलते रहना',
         ['राहों में काँटे बिखरे हों, पाँव भले ही छिल जाएँ,', 'आँधी आए, तूफ़ाँ घेरे, बादल भी घिर-घिर आएँ।',
          'रुकना मत, थकना मत, साथी, मंज़िल तुम्हें बुलाती है,', 'हर ठोकर कुछ कहती है, हर गिरावट कुछ सिखलाती है।'],
         ['नदिया पत्थर से टकराकर, अपनी राह बनाती है,', 'नन्ही-सी बूँद लगातार गिरे, तो चट्टान घिस जाती है।',
          'तुम भी अपने सपनों का दीप, हवा में जलाए रखना,', 'हार-जीत तो आती-जाती, बस कदम बढ़ाए रखना।'],
         [('मंज़िल', 'लक्ष्य, गंतव्य', 1), ('ठोकर', 'पैर से टकराने वाली चोट; असफलता', 1), ('तूफ़ाँ', 'तूफ़ान, आँधी-बवंडर', 1), ('चट्टान', 'बड़ा, कठोर पत्थर', 2), ('घिस जाना', 'रगड़ से धीरे-धीरे कम हो जाना', 2)],
         [('कवि के अनुसार हर ठोकर क्या करती है?', 'कुछ कहती है (सीख देती है)', ['पीछे लौटा देती है', 'सपने तोड़ देती है', 'मंज़िल छीन लेती है'], 1),
          ('नदी अपनी राह कैसे बनाती है?', 'पत्थरों से टकराकर', ['रुककर', 'सूखकर', 'पीछे मुड़कर'], 2),
          ('चट्टान किससे घिस जाती है?', 'लगातार गिरने वाली नन्ही बूँद से', ['आँधी से', 'आग से', 'धूप से'], 2),
          ('कवि ने “दीप” को कहाँ जलाए रखने को कहा है?', 'हवा में (कठिनाइयों के बीच)', ['मंदिर में', 'घर के आँगन में', 'नदी के किनारे'], 2)],
         [('“नन्ही-सी बूँद लगातार गिरे, तो चट्टान घिस जाती है” — इस पंक्ति का भाव लिखिए।', 'निरंतर छोटा प्रयास भी बड़ी-से-बड़ी बाधा को दूर कर सकता है; लगन से असंभव भी संभव होता है।', 2),
          ('कवि “साथी” कहकर किसे संबोधित कर रहा है और क्यों?', 'पाठक/हर संघर्षशील व्यक्ति को; आत्मीयता से हिम्मत बँधाने के लिए।', 1)],
         'कठिनाइयों में भी निरंतर आगे बढ़ते रहने और असफलता से सीखने की प्रेरणा।',
         [('रुकना मत, थकना मत, साथी, मंज़िल तुम्हें बुलाती है,', 'मानवीकरण अलंकार', 'मंज़िल पर मनुष्य की तरह बुलाने की क्रिया का आरोप है।', 1),
          ('आँधी आए, तूफ़ाँ घेरे, बादल भी घिर-घिर आएँ।', 'अनुप्रास अलंकार', '“घ” वर्ण की आवृत्ति (घेरे, घिर-घिर) से ध्वनि-सौंदर्य।', 1)],
         [('यह कविता आज के विद्यार्थी के जीवन से कैसे जुड़ती है? उदाहरण सहित लिखिए।', 'परीक्षा में असफलता, खेल में हार, नई चीज़ सीखने की कठिनाई — निरंतर अभ्यास और धैर्य से सफलता; उदाहरण।')],
         {1: 'प्रसंग: “चलते रहना” कविता का प्रथम अंश, जिसमें कवि संघर्षशील साथी को प्रेरित करता है। व्याख्या: रास्ते में काँटे, आँधी-तूफ़ान आएँ, फिर भी रुकना-थकना नहीं; मंज़िल पुकार रही है और हर असफलता सीख देती है। विशेष: मानवीकरण (मंज़िल बुलाती है), अनुप्रास (घेरे, घिर-घिर), संबोधन शैली।',
          2: 'प्रसंग: कविता का दूसरा अंश, प्रकृति के उदाहरणों से प्रेरणा। व्याख्या: नदी पत्थरों से टकराकर राह बनाती है, बूँद लगातार गिरकर चट्टान घिस देती है; वैसे ही हमें कठिनाइयों में भी सपनों का दीप जलाए रखना है। विशेष: दृष्टांत शैली, “सपनों का दीप” में रूपक।'},
         [('कवि हार को जीवन का अंत मानता है।', False, '“हार-जीत तो आती-जाती” — कवि हार को अस्थायी मानता है।', 2), ('कविता में प्रकृति के उदाहरणों से प्रेरणा दी गई है।', True, 'नदी और बूँद के उदाहरण दिए गए हैं।', 2)]),
    poem('डोर और पतंग',
         ['छत पर खड़ा था एक लड़का, हाथों में थी डोर,', 'आसमान में उड़ती पतंग, चली हवा के ज़ोर।',
          'पतंग बोली, “छोड़ो डोर, मैं ऊँचे जाना चाहूँ,', 'बादल छू लूँ, सूरज चूमूँ, खुलकर मैं लहराऊँ।”'],
         ['लड़के ने ज्यों ढील छोड़ी, कटकर गिरी पतंग,', 'झाड़ी में उलझी पड़ी रही, बिखर गया सब रंग।',
          'तब समझी वह — डोर नहीं थी बंधन, थी आधार,', 'अनुशासन की डोर थामकर, छूते हैं आकाश अपार।'],
         [('डोर', 'धागा; यहाँ अनुशासन/सहारा', 1), ('ढील', 'खिंचाव कम करना, ढीला छोड़ना', 2), ('आधार', 'सहारा, नींव', 2), ('अपार', 'जिसका पार न हो, असीम', 2)],
         [('पतंग लड़के से क्या चाहती थी?', 'डोर छोड़ दे ताकि वह और ऊँचे उड़ सके', ['उसे नीचे उतार ले', 'उसे रंग दे', 'उसे दूसरी छत पर ले जाए'], 1),
          ('पतंग के क्या-क्या सपने थे?', 'बादल छूना, सूरज चूमना और खुलकर लहराना', ['घर लौटना', 'झाड़ी में छिपना', 'नदी में तैरना'], 1),
          ('डोर छूटने पर पतंग का क्या हुआ?', 'वह कटकर झाड़ी में उलझ गई', ['वह सूरज तक पहुँच गई', 'वह और ऊँची उड़ी', 'वह लड़के के पास लौट आई'], 2),
          ('अंत में पतंग ने डोर को क्या माना?', 'आधार (सहारा)', ['बंधन', 'बोझ', 'शत्रु'], 2)],
         [('“डोर नहीं थी बंधन, थी आधार” — इस पंक्ति का भाव स्पष्ट कीजिए।', 'जो नियम/अनुशासन हमें बंधन लगते हैं, वही वास्तव में हमें सँभालकर ऊँचाई तक पहुँचाने वाले सहारे हैं।', 2),
          ('इस कविता में पतंग और डोर किसके प्रतीक हैं?', 'पतंग — स्वतंत्रता चाहने वाला मन/युवा; डोर — अनुशासन, माता-पिता या शिक्षकों का मार्गदर्शन।', 0)],
         'अनुशासन बंधन नहीं, ऊँचाई तक पहुँचने का आधार है — इसका प्रतीकात्मक संदेश।',
         [('बादल छू लूँ, सूरज चूमूँ, खुलकर मैं लहराऊँ।', 'मानवीकरण अलंकार', 'पतंग मनुष्य की तरह बोलती और इच्छा प्रकट करती है।', 1)],
         [('क्या आप कविता के इस विचार से सहमत हैं कि अनुशासन स्वतंत्रता का विरोधी नहीं है? अपने जीवन से उदाहरण दीजिए।', 'संतुलित उत्तर: अनुशासन (समय-सारणी, अभ्यास) से ही वास्तविक स्वतंत्रता और सफलता; उदाहरण — खिलाड़ी का अभ्यास।')],
         {1: 'प्रसंग: “डोर और पतंग” का प्रथम अंश। व्याख्या: छत पर लड़का पतंग उड़ा रहा है; पतंग डोर को बंधन मानकर उससे मुक्त होकर बादल-सूरज तक जाना चाहती है। विशेष: मानवीकरण, संवाद शैली, प्रतीकात्मकता।',
          2: 'प्रसंग: कविता का दूसरा अंश, जिसमें पतंग को अपनी भूल समझ आती है। व्याख्या: डोर ढीली होते ही पतंग कटकर झाड़ी में उलझ जाती है; तब वह समझती है कि डोर उसका आधार थी। विशेष: प्रतीक — डोर = अनुशासन; सरल, गेय भाषा।'},
         [('पतंग डोर से छूटकर सूरज तक पहुँच गई।', False, 'डोर छूटते ही वह कटकर झाड़ी में गिर गई।', 2)]),
    poem('नया सवेरा',
         ['रात कितनी भी अँधेरी, भोर फिर भी आएगी,', 'सूखी डाली पर भी इक दिन, कोंपल मुस्काएगी।',
          'बीज धरती में दबा है, पर उसे है यह यकीन,', 'तोड़कर मिट्टी की परतें, देखेगा वह दिन हसीन।'],
         ['हारकर जो बैठ जाए, उसको क्या मिलता कहो?', 'जो उठे फिर से, चले फिर, वो ही जीता, सच कहो।',
          'आँख में आँसू सही, पर होंठ पर मुस्कान रख,', 'हर अँधेरे के परे है, एक नया सवेरा देख।'],
         [('भोर', 'सुबह, प्रातःकाल', 1), ('कोंपल', 'नई कोमल पत्ती', 1), ('यकीन', 'विश्वास', 1), ('हसीन', 'सुंदर', 1), ('परे', 'उस पार, आगे', 2)],
         [('कवि के अनुसार अँधेरी रात के बाद क्या आएगा?', 'भोर (सुबह)', ['और गहरी रात', 'तूफ़ान', 'सन्नाटा'], 1),
          ('धरती में दबे बीज को किस बात का यकीन है?', 'वह मिट्टी तोड़कर सुंदर दिन देखेगा', ['वह कभी नहीं उगेगा', 'उसे कोई निकाल लेगा', 'बारिश नहीं होगी'], 1),
          ('कवि के अनुसार कौन जीतता है?', 'जो हारकर भी फिर उठे और चले', ['जो कभी न गिरे', 'जो सबसे तेज़ हो', 'जो हारकर बैठ जाए'], 2),
          ('कवि आँसुओं के साथ भी क्या रखने को कहता है?', 'होंठों पर मुस्कान', ['मन में डर', 'हाथ में दीपक', 'आँखें बंद'], 2)],
         [('“सूखी डाली पर भी इक दिन, कोंपल मुस्काएगी” — इस पंक्ति का भाव लिखिए।', 'निराशा की स्थिति में भी आशा बनी रहती है; कठिन समय के बाद नया जीवन और खुशी लौटती है।', 1),
          ('बीज का उदाहरण देकर कवि क्या समझाना चाहता है?', 'जैसे बीज मिट्टी की परतें तोड़कर बाहर आता है, वैसे ही धैर्य और विश्वास से मनुष्य बाधाएँ पार करता है।', 1)],
         'निराशा के अँधेरे में भी आशा बनाए रखने और हार के बाद फिर उठ खड़े होने का संदेश।',
         [('सूखी डाली पर भी इक दिन, कोंपल मुस्काएगी।', 'मानवीकरण अलंकार', 'कोंपल पर मनुष्य की तरह मुस्कुराने की क्रिया का आरोप है।', 1)],
         [('कोई ऐसा अनुभव लिखिए जब असफलता के बाद आपने या किसी परिचित ने फिर से प्रयास किया। कविता की किन पंक्तियों से वह जुड़ता है?', 'व्यक्तिगत अनुभव + “जो उठे फिर से, चले फिर, वो ही जीता” जैसी पंक्ति से जोड़।')],
         {1: 'प्रसंग: “नया सवेरा” का प्रथम अंश। व्याख्या: कवि कहता है कि रात कितनी भी अँधेरी हो, सुबह आती है; सूखी डाली पर भी कोंपल फूटती है; बीज मिट्टी तोड़कर सुंदर दिन देखता है। विशेष: प्रकृति के प्रतीकों से आशा का संदेश, मानवीकरण।',
          2: 'प्रसंग: कविता का दूसरा अंश, प्रत्यक्ष प्रेरणा। व्याख्या: हारकर बैठने वाले को कुछ नहीं मिलता; जो फिर उठकर चलता है वही जीतता है; आँसुओं के बीच भी मुस्कान रखनी चाहिए। विशेष: प्रश्न शैली, विरोधाभासी चित्र (आँसू-मुस्कान), “अँधेरा-सवेरा” प्रतीक।'},
         [('कवि हारकर बैठ जाने को उचित मानता है।', False, '“हारकर जो बैठ जाए, उसको क्या मिलता कहो?” — कवि इसे व्यर्थ मानता है।', 2)]),
]

t = topic('प्रेरक कविता का भाव और आज के जीवन से संबंध', 'प्रेरक कविता')
reading(t, P_PRERNA, 'read', c4kinds=('eval',))
t10_1 = t

t = topic('व्याकरण: अनेकार्थी शब्द और वर्तनी शुद्धि', 'अनेकार्थी शब्द और वर्तनी')
anekarth(t, ANEKARTH)
xform(t, VARTANI, 'शुद्ध वर्तनी लिखिए', label='वर्तनी-शुद्धि', c4=False)
t10_2 = t

STORY_FACTS = [
    ('संकेत बिंदुओं के आधार पर कहानी लिखते समय पहले क्या करना चाहिए?', 'सभी बिंदुओं को क्रम से जोड़कर कथानक की रूपरेखा बनाना', ['सीधे अंत लिखना', 'केवल शीर्षक लिखना', 'बिंदुओं का क्रम बदलना'], 'रूपरेखा से कहानी तार्किक बनती है।'),
    ('अच्छी कहानी के अंत में प्रायः क्या होता है?', 'कोई शिक्षा, संदेश या रोचक परिणाम', ['नए पात्रों का परिचय', 'संकेत बिंदुओं की सूची', 'कहानी का पहला वाक्य'], 'अंत कहानी को सार्थक बनाता है।'),
    ('कहानी में संवादों का प्रयोग क्यों किया जाता है?', 'पात्रों को सजीव और कहानी को रोचक बनाने के लिए', ['कहानी को छोटा करने के लिए', 'शीर्षक बताने के लिए', 'व्याकरण दिखाने के लिए'], 'संवाद पात्रों का स्वभाव प्रकट करते हैं।'),
    ('कहानी का शीर्षक कैसा होना चाहिए?', 'छोटा, आकर्षक और कहानी के केंद्रीय भाव से जुड़ा', ['बहुत लंबा', 'कहानी से असंबद्ध', 'पूरी कहानी का सार'], 'शीर्षक जिज्ञासा जगाता है।'),
    ('संकेत बिंदुओं वाली कहानी किस काल में लिखी जाती है?', 'प्रायः भूतकाल में', ['केवल भविष्यत् काल में', 'आज्ञार्थ में', 'केवल प्रश्नवाचक वाक्यों में'], 'घटनाएँ बीत चुकी मानकर सुनाई जाती हैं।'),
]
STORY_FLAWS = [
    ('एक लड़का था। वह जंगल गया। उसने शेर देखा। वह भाग गया। कहानी खत्म।', 'वाक्य बहुत छोटे और सूचनात्मक हैं; वर्णन, भावना, संवाद और शिक्षा नहीं है।', 'घने जंगल में लकड़ियाँ बीनते हुए {N} ने अचानक झाड़ियों में दो चमकती आँखें देखीं। उसका दिल ज़ोर से धड़कने लगा…'),
    ('राजा ने कहा कि वह कल आएगा और फिर मोबाइल पर वीडियो देखने लगा।', 'कहानी के परिवेश (राजा का युग) और विवरण (मोबाइल) में असंगति है।', 'राजा ने घोषणा करवाई कि वह अगले दिन नगर का भ्रमण करेगा; फिर वह अपने महल के उद्यान में टहलने लगा।'),
    ('परीक्षा का दिन था। {N} को रास्ते में देर हो गई। अंत में अध्यापक ने उसकी प्रशंसा की और सब खुश हो गए।', 'सभी संकेत बिंदुओं का प्रयोग नहीं हुआ; बीच की घटनाएँ (घायल कुत्ते की मदद, कारण बताना) छूट गईं, इसलिए अंत तर्कहीन लगता है।', 'हर संकेत बिंदु को एक-एक घटना के रूप में विस्तार दें, फिर तार्किक अंत तक पहुँचें।'),
]


def story_task(r):
    n, g = name(r)
    pts = r.choice([
        ('एक प्यासा कौआ — शहर में पानी नहीं — नल के नीचे टपकती बूँदें — कौए ने बच्चे को देखा — बच्चे ने नल ठीक से बंद किया — कौआ भी पानी पी सका', 'जल-संरक्षण'),
        ('परीक्षा का दिन — रास्ते में घायल कुत्ता — मदद करना — परीक्षा में देरी — अध्यापक को कारण बताना — प्रशंसा और अतिरिक्त समय', 'करुणा और ईमानदारी'),
        ('दो मित्र — एक की पेंसिल चोरी — दूसरे पर शक — सच्चाई का पता चलना — क्षमा माँगना — मित्रता और गहरी', 'जल्दबाज़ी में निर्णय न लेना'),
        ('गाँव में मेला — दादी का बटुआ खोना — ईमानदार लड़की को मिलना — घोषणा-कक्ष में लौटाना — दादी का आशीर्वाद', 'ईमानदारी'),
        ('पुराना पीपल का पेड़ — उसे काटने की योजना — बच्चों का विरोध — पंचायत की बैठक — पेड़ बचा, नए पेड़ लगे', 'पर्यावरण-प्रेम'),
    ])
    bl = [x.strip() for x in pts[0].split('—')]
    return {'task': f'दिए गए संकेत बिंदुओं के आधार पर एक कहानी लिखिए और उसे उपयुक्त शीर्षक दीजिए:\n{pts[0]}', 'bullets': ['सभी संकेत बिंदुओं का क्रम से प्रयोग', 'कम-से-कम दो संवाद', 'उपयुक्त शीर्षक', 'अंत में शिक्षा/संदेश'],
            'ind': f'सभी बिंदु क्रम से ({", ".join(bl)}); आरंभ-मध्य-अंत; संवाद; उपयुक्त शीर्षक; संदेश: {pts[1]}।',
            'model': f'मॉडल: कहानी के केंद्र से जुड़ा आकर्षक शीर्षक — आकर्षक आरंभ, हर संकेत बिंदु एक घटना, संवादों से सजीवता, अंत में संदेश: {pts[1]}।'}


def story_short(r, D):
    T = story_task(r)
    return (f'{T["task"]}\nइस कहानी का केवल आरंभ (पहले चार-पाँच वाक्य) लिखिए और उपयुक्त शीर्षक दीजिए।', T['model'], 'आकर्षक आरंभ और परिवेश (1); पहले संकेत बिंदु का प्रयोग (1); उपयुक्त शीर्षक')


t = topic('रचना: कहानी लेखन (संकेत बिंदुओं के आधार पर)', 'कहानी लेखन')
writing(t, 'कहानी', [story_task], STORY_FACTS, STORY_FLAWS, [story_short])
t10_3 = t


def un_bird(r):
    c = r.choice(INDIA)
    k = r.choice([120, 150, 180])
    yrs = r.choice([10, 15, 20])
    text = (f'कुछ वर्ष पहले तक हमारे आँगन में सुबह-सुबह गौरैया की चहचहाहट सुनाई देती थी, पर अब वह बहुत कम दिखती है। विशेषज्ञों के अनुसार {c} जैसे शहरों में पिछले {yrs} वर्षों में गौरैया की संख्या तेज़ी से घटी है। '
            'इसके कई कारण हैं — पक्के मकानों में घोंसले के लिए जगह नहीं बची, बगीचों में कीटनाशकों से कीड़े मर गए जो चूज़ों का भोजन थे, और पेड़ कटने से छाया भी कम हो गई। '
            f'अच्छी बात यह है कि लोग अब जागरूक हो रहे हैं। एक विद्यालय के बच्चों ने लकड़ी के {k} घोंसले बनाकर मोहल्ले के घरों में लगाए और छतों पर पानी के बर्तन रखे। '
            'कुछ ही महीनों में कई घोंसलों में गौरैया लौट आई। यदि हम थोड़ा-सा ध्यान दें, तो यह नन्ही चिड़िया फिर से हमारे आँगन की रौनक बन सकती है।')
    return ex('गद्यांश', text,
              facts=[('पहले सुबह-सुबह आँगन में क्या सुनाई देता था?', 'गौरैया की चहचहाहट', ['कोयल की कूक', 'मोर की आवाज़', 'कौओं की काँव-काँव']),
                     ('बच्चों ने कितने घोंसले बनाए?', str(k), num_ds(r, k, 30)),
                     ('चूज़ों का भोजन कम क्यों हो गया?', 'कीटनाशकों से कीड़े मर गए', ['बारिश अधिक हुई', 'लोगों ने दाना डालना बंद किया', 'पेड़ों पर फल नहीं आए']),
                     ('बच्चों ने छतों पर क्या रखा?', 'पानी के बर्तन', ['दाने की बोरियाँ', 'पौधों के गमले', 'दर्पण'])],
              vocab=[('रौनक', 'चहल-पहल, शोभा', ['उदासी', 'अँधेरा', 'सन्नाटा']), ('कीटनाशक', 'कीड़ों को मारने वाला रसायन', ['खाद', 'बीज', 'पानी'])],
              tf=[('गौरैया की संख्या घटने का केवल एक कारण है।', False, 'अंश में कई कारण बताए गए हैं — घोंसलों की कमी, कीटनाशक, पेड़ों की कटाई।'),
                  ('बच्चों के प्रयास से कुछ घोंसलों में गौरैया लौट आई।', True, 'अंश में यही बताया गया है।')],
              infer=[('लेखक ने गद्यांश का अंत आशावादी ढंग से क्यों किया है?', 'यह दिखाने के लिए कि छोटे-छोटे प्रयासों से समस्या हल हो सकती है; पाठक को प्रेरित करने के लिए।'),
                     ('पक्के मकान गौरैया के लिए समस्या क्यों बने?', 'उनमें छेद, दरारें या छज्जे जैसी जगहें नहीं होतीं जहाँ गौरैया घोंसला बना सके।')],
              title=('लौट आई गौरैया', ['पक्के मकान', 'पानी के बर्तन', 'कीटनाशक']),
              points=['गौरैया का घटना', f'{yrs} वर्षों में तेज़ गिरावट', 'घोंसलों की कमी', 'कीटनाशक और पेड़ कटना', f'बच्चों के {k} घोंसले', 'गौरैया की वापसी और आशा'],
              evals=[('आप अपने इलाके में पक्षियों की रक्षा के लिए कौन-से तीन उपाय करेंगे? गद्यांश से जोड़कर लिखिए।', 'घोंसले लगाना, पानी-दाना रखना, पेड़ लगाना, कीटनाशक कम करना; कारण सहित।')],
              notes={'कारण': ['घोंसलों की जगह नहीं', 'कीटनाशक', 'पेड़ों की कटाई'], 'उपाय': [f'{k} लकड़ी के घोंसले', 'छतों पर पानी'], 'परिणाम': ['गौरैया की वापसी']})


def un_sports(r):
    n, g = name(r, 'f')
    age = r.choice([14, 15, 16])
    text = A(f'{n} एक छोटे-से गाँव की लड़की है, जहाँ खेल का कोई मैदान नहीं था। वह सुबह पाँच बजे उठकर खेतों की मेड़ पर दौड़ती थी। गाँव के कुछ लोग कहते, “लड़की होकर दौड़ेगी? घर का काम सीखो।” '
             f'पर उसके पिता ने कहा, “मेरी बेटी जितना दौड़ना चाहे, दौड़ेगी।” उन्होंने उसके लिए पुराने जूते खरीदे, जिनके तले घिस चुके थे। '
             f'{age} वर्ष की आयु में {n} ने ज़िला स्तर की दौड़ में भाग लिया और प्रथम आई। आज वही लोग, जो कभी ताने देते थे, अपनी बेटियों को उसके साथ सुबह दौड़ने भेजते हैं। '
             f'{n} कहती है, “मेरी सबसे बड़ी जीत पदक नहीं, गाँव की वे लड़कियाँ हैं जो अब मेरे साथ दौड़ती हैं।”', g)
    return ex('गद्यांश', text,
              facts=[(f'{n} दौड़ने का अभ्यास कहाँ करती थी?', 'खेतों की मेड़ पर', ['स्कूल के मैदान में', 'स्टेडियम में', 'सड़क पर']),
                     (f'{n} के पिता ने उसके लिए क्या खरीदा?', 'पुराने जूते', ['नए जूते', 'साइकिल', 'खेल की पोशाक']),
                     (f'{n} ने किस आयु में ज़िला स्तर की दौड़ जीती?', f'{age} वर्ष', [f'{x} वर्ष' for x in (12, 13, 14, 15, 16, 17) if x != age][:3]),
                     (f'{n} अपनी सबसे बड़ी जीत किसे मानती है?', 'गाँव की उन लड़कियों को जो अब उसके साथ दौड़ती हैं', ['ज़िला स्तर के पदक को', 'नए जूतों को', 'अख़बार में छपी तस्वीर को'])],
              vocab=[('ताने देना', 'व्यंग्य से चुभती बात कहना', ['प्रशंसा करना', 'सहायता करना', 'उपहार देना']), ('मेड़', 'खेतों के बीच की ऊँची, पतली पगडंडी', ['कुआँ', 'नहर', 'छप्पर'])],
              tf=[(f'गाँव के सभी लोग शुरू से {n} के दौड़ने के पक्ष में थे।', False, 'कुछ लोग ताने देते थे कि लड़की होकर दौड़ेगी।'),
                  (f'{n} के जूतों के तले घिसे हुए थे।', True, '“पुराने जूते, जिनके तले घिस चुके थे।”')],
              infer=[('गाँव के लोगों की सोच में आए परिवर्तन का कारण क्या था?', f'{n} की सफलता ने दिखा दिया कि लड़कियाँ भी खेल में आगे बढ़ सकती हैं; उदाहरण ने सोच बदल दी।'),
                     (f'{n} के पिता के चरित्र की एक विशेषता लिखिए।', 'प्रगतिशील और सहयोगी — समाज के तानों के बावजूद बेटी का साथ दिया।')],
              title=('मेड़ से मैदान तक', ['पुराने जूते', 'गाँव के ताने', 'सुबह पाँच बजे']),
              points=['गाँव में मैदान नहीं', 'मेड़ पर अभ्यास', 'समाज के ताने', 'पिता का साथ और पुराने जूते', f'{age} वर्ष में ज़िला स्तर पर प्रथम', 'गाँव की सोच में परिवर्तन'],
              evals=[(f'{n} की कहानी लड़कियों के खेलने के अधिकार के बारे में क्या संदेश देती है? अपने विचार लिखिए।', 'समान अवसर; परिवार का सहयोग; एक व्यक्ति का उदाहरण समाज बदल सकता है; व्यक्तिगत विचार।')],
              notes={'चुनौतियाँ': ['मैदान का अभाव', 'समाज के ताने', 'घिसे जूते'], 'सहारा': ['पिता का साथ'], 'उपलब्धि': [f'{age} वर्ष में ज़िला स्तर पर प्रथम', 'गाँव की लड़कियाँ भी दौड़ने लगीं']})


def un_poem_kisan():
    return poem('किसान',
                ['धूप जले या बरसे पानी, खेतों में वह जाता है,', 'माथे से बहता है पसीना, फिर भी वह मुस्काता है।'],
                ['उसके हल की हर रेखा में, लिखी हमारी रोटी है,', 'उसकी मेहनत के आगे तो, हर दौलत भी छोटी है।'],
                [('हल', 'खेत जोतने का औज़ार', 1), ('दौलत', 'धन-संपत्ति', 2)],
                [('किसान किस मौसम में भी खेतों में जाता है?', 'धूप हो या बरसात — हर मौसम में', ['केवल सर्दियों में', 'केवल बसंत में', 'कभी नहीं'], 1),
                 ('पसीना बहने पर भी किसान क्या करता है?', 'मुस्कुराता है', ['रोता है', 'काम छोड़ देता है', 'सो जाता है'], 1),
                 ('हल की रेखा में क्या लिखा बताया गया है?', 'हमारी रोटी', ['किसान का नाम', 'मौसम का हाल', 'गाँव का नक्शा'], 2)],
                [('“उसके हल की हर रेखा में, लिखी हमारी रोटी है” — भाव स्पष्ट कीजिए।', 'किसान के खेत जोतने से ही अनाज उगता है; हमारा भोजन उसकी मेहनत पर निर्भर है।', 2)],
                'किसान के कठोर परिश्रम और उसके प्रति समाज की कृतज्ञता का भाव।',
                [('माथे से बहता है पसीना, फिर भी वह मुस्काता है।', 'अनुप्रास अलंकार', '“म” वर्ण की आवृत्ति (माथे, मुस्काता) से ध्वनि-सौंदर्य।', 1)],
                [('आज के समय में किसानों के प्रति हमारा क्या कर्तव्य है? कविता के आधार पर लिखिए।', 'भोजन का सम्मान, अन्न की बर्बादी न करना, किसानों के श्रम का आदर; उचित मूल्य का समर्थन।')],
                tf=[('कविता के अनुसार किसान का परिश्रम धन से भी बड़ा है।', True, '“उसकी मेहनत के आगे तो, हर दौलत भी छोटी है।”', 2)])


def un_poem_diya():
    return poem('दीया',
                ['छोटा-सा मिट्टी का दीया, अँधियारे से लड़ता है,', 'आँधी आए, तेल घटे, पर साहस से वह जलता है।'],
                ['खुद जलकर भी देता है जो, औरों को उजियारा,', 'ऐसा दीया बन जाए तो, जग हो जाए प्यारा।'],
                [('अँधियारा', 'अंधकार', 1), ('उजियारा', 'प्रकाश, रोशनी', 2), ('जग', 'संसार', 2)],
                [('दीया किससे लड़ता है?', 'अँधियारे से', ['पानी से', 'आग से', 'मिट्टी से'], 1),
                 ('दीया किस चीज़ का बना है?', 'मिट्टी का', ['पीतल का', 'काँच का', 'लोहे का'], 1),
                 ('दीया दूसरों को क्या देता है?', 'उजियारा (प्रकाश)', ['छाया', 'ठंडक', 'तेल'], 2)],
                [('“खुद जलकर भी देता है जो, औरों को उजियारा” — इस पंक्ति का भाव लिखिए।', 'त्याग और परोपकार — स्वयं कष्ट सहकर भी दूसरों का भला करना।', 2)],
                'छोटे दीये के माध्यम से साहस, त्याग और परोपकार का संदेश।',
                [('छोटा-सा मिट्टी का दीया, अँधियारे से लड़ता है,', 'मानवीकरण अलंकार', 'दीये पर मनुष्य की तरह लड़ने की क्रिया का आरोप है।', 1)],
                [('“ऐसा दीया बन जाए तो, जग हो जाए प्यारा” — आप अपने जीवन में “दीया” कैसे बन सकते हैं? उदाहरण दीजिए।', 'दूसरों की सहायता, ज्ञान बाँटना, कठिनाई में साथ देना; व्यक्तिगत उदाहरण।')],
                tf=[('दीया आँधी आने पर बुझ जाता है।', False, 'कविता के अनुसार आँधी आए, तेल घटे, फिर भी वह साहस से जलता है।', 1)])


UNSEEN_10 = [un_bird, un_sports, un_poem_kisan(), un_poem_diya()]

t = topic('अपठित गद्यांश और पद्यांश: परीक्षा अभ्यास', 'अपठित अभ्यास')
reading(t, UNSEEN_10, 'read')
t10_4 = t
CHAPTERS[10] = [t10_1, t10_2, t10_3, t10_4]
