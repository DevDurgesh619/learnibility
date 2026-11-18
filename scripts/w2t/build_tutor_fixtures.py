#!/usr/bin/env python3
"""
W2-T demo content for the tutor app: Rahul Verma's practice (tutor HTML 2a to 8e).

Writes data/fixtures/contrib/w2t-tutors.json in the W2-0 contrib shape:
  { schemaVersion, generatedBy, collections: { student, gaps, mastery, attempts, bookings, sessions,
    assignments, messages, tutorNotes, payouts, tasks } }

Learners:
  - Fixture learners with real history: lrn_kabir_singh (CBSE 9 maths, in Rahul's Class 9 group) and
    lrn_rohan_das (CBSE 10 maths, paid 1:1 since 20 Oct, the persona brief's paid-tutor trigger).
    Contributions for persona-backed learners are ignored by the data layer once Wave 3 lands.
  - Background marketplace students (not personas): light student records plus enough learning data
    for the tutor's workspace screens.
  - lrn_ishita_rao is deliberately NOT booked: the demo flow books her live.

Deterministic; run: python3 scripts/w2t/build_tutor_fixtures.py
"""
import json
import os
from datetime import date, datetime, timedelta, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'data', 'fixtures', 'contrib', 'w2t-tutors.json')
IST = timezone(timedelta(hours=5, minutes=30))
NOW = datetime(2026, 11, 18, 9, 0, tzinfo=IST)
TUTOR = 'tut_rahul_verma'
RATE_1 = 800
RATE_G = 350
FEE = 0.15


def curriculum(sid):
    with open(os.path.join(ROOT, 'data', 'curriculum', f'{sid}.json')) as f:
        d = json.load(f)
    return {c['id']: c['name'] for c in d['items']}, {s['id']: s for s in d['subtopics']}


CH = {}
ST = {}
for sid in ['cbse-g11-physics', 'cbse-g12-maths', 'cbse-g9-maths', 'cbse-g10-maths', 'cambridge-g10-maths']:
    c, s = curriculum(sid)
    CH.update(c)
    ST.update(s)


def iso(dt):
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')


def at(d, hhmm):
    h, m = map(int, hhmm.split(':'))
    return datetime(d.year, d.month, d.day, h, m, tzinfo=IST)


def sname(stid):
    return ST[stid]['name']


def short(stid, n=None):
    # first clause of the subtopic name, e.g. "Definite integrals: fundamental theorem..." -> "Definite integrals"
    head = sname(stid).replace(';', ':').split(':')[0].split(',')[0].strip()
    return head


# ------------------------------------------------------------------ background students

def student(lid, first, last, board, grade, stream, programme, school, city, goal, subjects, windows, joined, band='average'):
    return {
        'id': lid, 'role': 'student', 'firstName': first, 'lastName': last, 'name': f'{first} {last}',
        'board': board, 'grade': grade, 'stream': stream, 'programme': programme, 'school': school, 'city': city,
        'medium': 'English', 'band': band, 'plan': 'free', 'goal': goal,
        'subjects': [{'subjectId': s, 'depth': 'light'} for s in subjects],
        'availability': [{'day': d, 'start': a, 'end': b} for d, a, b in windows], 'weeklyHours': 8, 'tzOffsetMinutes': 330,
        'onboardedUtc': iso(joined), 'joinedUtc': iso(joined), 'parentIds': [], 'counsellorIds': [], 'mentorIds': [],
        'tutorIds': [TUTOR], 'sectionIds': [], 'profileCompletionPct': 55,
        'story': 'Marketplace student of Rahul Verma (background, not a persona).',
    }


EVE = [(d, '16:00', '21:30') for d in ['mon', 'tue', 'wed', 'thu', 'fri']] + [('sat', '09:00', '13:00')]
BG = [
    student('lrn_tanvi_bhatia', 'Tanvi', 'Bhatia', 'cbse', 11, 'science', 'CBSE Class 11 Science (PCM)', 'Delhi Public School, R.K. Puram', 'Delhi', 'JEE Main 2028', ['cbse-g11-physics'], EVE, datetime(2026, 9, 26, 18, 0, tzinfo=IST), 'above_avg'),
    student('lrn_yash_gupta', 'Yash', 'Gupta', 'cbse', 12, 'science', 'CBSE Class 12 Science (PCM)', 'Modern School, Barakhamba Road', 'Delhi', 'JEE Main 2027', ['cbse-g12-maths'], EVE, datetime(2026, 9, 30, 17, 0, tzinfo=IST)),
    student('lrn_riya_sen', 'Riya', 'Sen', 'cambridge', 10, 'none', 'Cambridge IGCSE (Year 10)', 'Pathways School, Noida', 'Noida', 'IGCSE Maths A*', ['cambridge-g10-maths'], EVE, datetime(2026, 10, 3, 10, 0, tzinfo=IST)),
    student('lrn_mehul_jain', 'Mehul', 'Jain', 'cbse', 9, 'none', 'CBSE Class 9', 'Springdales School', 'Delhi', 'Class 9 Maths', ['cbse-g9-maths'], EVE, datetime(2026, 10, 5, 20, 0, tzinfo=IST)),
    student('lrn_arnav_khanna', 'Arnav', 'Khanna', 'cbse', 9, 'none', 'CBSE Class 9', 'Springdales School', 'Delhi', 'Class 9 Maths', ['cbse-g9-maths'], EVE, datetime(2026, 10, 5, 20, 0, tzinfo=IST)),
    student('lrn_sana_malik', 'Sana', 'Malik', 'cbse', 11, 'science', 'CBSE Class 11 Science (PCM)', "St. Mary's School", 'Ghaziabad', 'JEE Main 2028', ['cbse-g11-physics'], EVE, datetime(2026, 11, 12, 19, 0, tzinfo=IST)),
    student('lrn_dev_arora', 'Dev', 'Arora', 'cbse', 10, 'none', 'CBSE Class 10', 'Amity International, Saket', 'Delhi', 'Class 10 boards: 90%+ in Maths', ['cbse-g10-maths'], EVE, datetime(2026, 11, 14, 18, 0, tzinfo=IST)),
]
NAMES = {s['id']: s['firstName'] for s in BG}
NAMES.update({'lrn_kabir_singh': 'Kabir', 'lrn_rohan_das': 'Rohan'})

# ------------------------------------------------------------------ background learning record

mastery, gaps, attempts = [], [], []


def m(lid, stid, level, p, tested):
    mastery.append({'learnerId': lid, 'subtopicId': stid, 'chapterId': ST[stid]['chapterId'], 'subjectId': stid.rsplit('-ch', 1)[0],
                    'level': level, 'pMastery': p, 'lastTestedUtc': iso(tested)})


def gap(lid, stid, code, level, hours, status='confirmed', detected=None, causes=None):
    sid = stid.rsplit('-ch', 1)[0]
    d = detected or NOW - timedelta(days=10)
    gaps.append({
        'id': f'gap_{lid[4:]}_{stid.split("-", 3)[3]}', 'learnerId': lid, 'subtopicId': stid, 'chapterId': ST[stid]['chapterId'], 'subjectId': sid,
        'code': code, 'secondaryFlags': [], 'level': level, 'size': max(1, 5 - level), 'hoursToClose': hours, 'status': status,
        'detectedUtc': iso(d), 'updatedUtc': iso(d), 'band': 'average', 'weeks': round(hours / 2, 1), 'scorePct': [20, 35, 50, 62, 75][min(level, 4)],
        'confirmingProbe': None, 'likelyCauses': causes, 'prerequisiteToProbe': None,
    })


def attempt(lid, n, kind, title, sid, chid, when, score, max_score, minutes=30):
    attempts.append({
        'id': f'att_{lid[4:]}_w2t{n}', 'learnerId': lid, 'kind': kind, 'title': title, 'subjectId': sid, 'chapterId': chid,
        'questionIds': [], 'responses': [], 'startedUtc': iso(when - timedelta(minutes=minutes)), 'submittedUtc': iso(when),
        'minutesAllotted': minutes, 'score': score, 'maxScore': max_score, 'status': 'submitted',
    })


P = 'cbse-g11-physics'
d0 = datetime(2026, 9, 27, 11, 0, tzinfo=IST)
for stid, lv, p, dd in [('ch01-st1', 5, .93, 15), ('ch01-st2', 4, .88, 15), ('ch01-st3', 4, .86, 15), ('ch02-st1', 4, .84, 29), ('ch02-st2', 3, .72, 29),
                        ('ch02-st3', 3, .66, 29), ('ch02-st4', 4, .8, 29), ('ch03-st1', 4, .78, 43), ('ch03-st2', 3, .7, 43), ('ch03-st3', 3, .64, 43),
                        ('ch03-st4', 3, .66, 43), ('ch04-st1', 3, .62, 52), ('ch04-st2', 2, .42, 52), ('ch04-st3', 2, .48, 52)]:
    m('lrn_tanvi_bhatia', f'{P}-{stid}', lv, p, d0 + timedelta(days=dd))
gap('lrn_tanvi_bhatia', f'{P}-ch04-st2', 'G3', 2, 3.2, causes='Writes one equation per body but skips the string constraint')
gap('lrn_tanvi_bhatia', f'{P}-ch04-st3', 'G2', 2, 2.8, causes='Friction direction chosen by habit, not by relative motion')
gap('lrn_tanvi_bhatia', f'{P}-ch02-st3', 'G6', 3, 1.4, status='in_progress', causes='Graph slopes slipping after 3 weeks')
for i, (kind, title, ch, dd, sc, mx) in enumerate([
        ('onboarding', 'Onboarding test · Physics', 'ch01', 0, 29, 50), ('chapter_check', 'Chapter check · Units and Measurements', 'ch01', 15, 22, 25),
        ('chapter_check', 'Chapter check · Motion in a Straight Line', 'ch02', 29, 17, 25), ('weekly', 'Weekly test · Motion in a Plane', 'ch03', 43, 18, 25),
        ('chapter_check', 'Chapter check · Laws of Motion', 'ch04', 52, 15, 25)]):
    attempt('lrn_tanvi_bhatia', i + 1, kind, title, P, f'{P}-{ch}', d0 + timedelta(days=dd), sc, mx)

Y = 'cbse-g12-maths'
for stid, lv, p, dd in [('ch05-st1', 4, .86, 10), ('ch05-st2', 4, .8, 10), ('ch05-st3', 3, .74, 10), ('ch05-st4', 4, .82, 10), ('ch06-st1', 4, .85, 30),
                        ('ch06-st2', 4, .83, 30), ('ch06-st3', 3, .72, 30), ('ch06-st4', 3, .6, 30), ('ch07-st1', 4, .8, 45), ('ch07-st2', 3, .62, 45), ('ch07-st3', 2, .5, 45)]:
    m('lrn_yash_gupta', f'{Y}-{stid}', lv, p, d0 + timedelta(days=dd))
gap('lrn_yash_gupta', f'{Y}-ch07-st3', 'G3', 2, 2.4, causes='Sets up partial fractions but drops a repeated-factor term')
gap('lrn_yash_gupta', f'{Y}-ch06-st4', 'G5', 3, 2.0, causes='Optimisation word problems: cannot pick the variable to maximise')
for i, (kind, title, ch, dd, sc, mx) in enumerate([
        ('onboarding', 'Onboarding test · Maths', 'ch05', 3, 31, 50), ('chapter_check', 'Chapter check · Continuity and Differentiability', 'ch05', 10, 19, 25),
        ('chapter_check', 'Chapter check · Application of Derivatives', 'ch06', 30, 18, 25), ('weekly', 'Weekly test · Integrals I', 'ch07', 45, 20, 25)]):
    attempt('lrn_yash_gupta', i + 1, kind, title, Y, f'{Y}-{ch}', d0 + timedelta(days=dd), sc, mx)

R = 'cambridge-g10-maths'
for stid, lv, p, dd in [('ch02-st1', 4, .82, 20), ('ch02-st2', 3, .64, 20), ('ch02-st3', 4, .8, 20), ('ch02-st5', 2, .45, 34)]:
    m('lrn_riya_sen', f'{R}-{stid}', lv, p, d0 + timedelta(days=dd))
gap('lrn_riya_sen', f'{R}-ch02-st5', 'G1', 1, 3.0, causes='Fraction rules from Year 8 not secure')
for i, (kind, title, ch, dd, sc, mx) in enumerate([('onboarding', 'Onboarding test · Maths', 'ch02', 8, 30, 50), ('chapter_check', 'Chapter check · Equations and inequalities', 'ch02', 20, 17, 25), ('weekly', 'Weekly test · Algebraic fractions', 'ch02', 34, 12, 25)]):
    attempt('lrn_riya_sen', i + 1, kind, title, R, f'{R}-{ch}', d0 + timedelta(days=dd), sc, mx)

N9 = 'cbse-g9-maths'
for lid, base in [('lrn_mehul_jain', .78), ('lrn_arnav_khanna', .66)]:
    for j, stid in enumerate(['ch02-st1', 'ch02-st2', 'ch02-st4', 'ch03-st1', 'ch03-st3', 'ch03-st5', 'ch04-st1', 'ch04-st2']):
        pm = round(base - (j % 3) * 0.06, 2)
        m(lid, f'{N9}-{stid}', 4 if pm >= .75 else 3 if pm >= .6 else 2, pm, d0 + timedelta(days=20 + j * 4))
    attempt(lid, 1, 'chapter_check', 'Chapter check · Linear Polynomials', N9, f'{N9}-ch02', d0 + timedelta(days=24), round(25 * base), 25)
    attempt(lid, 2, 'chapter_check', 'Chapter check · The World of Numbers', N9, f'{N9}-ch03', d0 + timedelta(days=40), round(25 * base) + 1, 25)
gap('lrn_arnav_khanna', f'{N9}-ch03-st5', 'G3', 2, 2.2, causes='Rationalising denominators: multiplies only the numerator')

for lid, sid, items in [
        ('lrn_sana_malik', P, [('ch06-st4', 'G2', 1, 3.4), ('ch07-st3', 'G1', 2, 2.6), ('ch06-st2', 'G3', 2, 1.8)]),
        ('lrn_dev_arora', 'cbse-g10-maths', [('ch04-st3', 'G3', 2, 2.2), ('ch04-st4', 'G5', 2, 2.0), ('ch02-st3', 'G2', 3, 1.5)])]:
    for stid, code, lv, h in items:
        gap(lid, f'{sid}-{stid}', code, lv, h, status='suspected', detected=NOW - timedelta(days=4))

# ------------------------------------------------------------------ sessions, reports, homework, payouts

sessions, tasks, notes, messages, bookings = [], [], [], [], []
code_n = [0]


def task(lid, title, kind, due, status, sess_id, minutes=30, sid=None, detail=None, done_at=None):
    t = {'id': f'task_w2t_{len(tasks) + 1:03d}', 'learnerId': lid, 'title': title, 'kind': kind, 'dueDate': due.isoformat(), 'status': status,
         'source': 'tutor', 'createdBy': TUTOR, 'createdUtc': iso(datetime.combine(due - timedelta(days=2), datetime.min.time(), IST) + timedelta(hours=19)),
         'minutes': minutes, 'subjectId': sid, 'refId': sess_id, 'detail': detail or 'From your tutor session'}
    if status == 'done':
        t['completedUtc'] = iso(done_at or datetime.combine(due - timedelta(days=1), datetime.min.time(), IST) + timedelta(hours=20))
    tasks.append(t)
    return t['id']


PLAN = {
    'tanvi': [('ch01-st1', 'ch01-st2'), ('ch01-st2', 'ch01-st3'), ('ch02-st1', 'ch02-st2'), ('ch02-st2', 'ch02-st3'), ('ch02-st3', 'ch02-st4'), ('ch03-st1', 'ch03-st2'),
              ('ch03-st3', 'ch03-st3'), ('ch03-st4', 'ch04-st1'), ('ch04-st1', 'ch04-st1'), ('ch04-st2', 'ch04-st2'), ('ch04-st2', 'ch04-st3'), ('ch04-st3', 'ch04-st2'), ('ch04-st2', 'ch04-st3'), ('ch04-st3', 'ch04-st2')],
    'yash': [('ch05-st1', 'ch05-st2'), ('ch05-st3', 'ch05-st4'), ('ch05-st5', 'ch05-st5'), ('ch06-st1', 'ch06-st2'), ('ch06-st3', 'ch06-st3'), ('ch06-st4', 'ch06-st4'),
             ('ch07-st1', 'ch07-st1'), ('ch07-st2', 'ch07-st2'), ('ch07-st2', 'ch07-st3'), ('ch07-st3', 'ch07-st3'), ('ch07-st3', 'ch07-st4'), ('ch07-st4', 'ch07-st5'), ('ch07-st4', 'ch07-st5'), ('ch07-st5', 'ch07-st5')],
    'rohan': [('ch02-st1', 'ch02-st2'), ('ch02-st3', 'ch02-st3'), ('ch02-st3', 'ch02-st4'), ('ch04-st1', 'ch04-st1'), ('ch04-st2', 'ch04-st2'), ('ch04-st2', 'ch04-st2'), ('ch04-st3', 'ch04-st3'), ('ch04-st3', 'ch04-st3'), ('ch04-st3', 'ch04-st4'), ('ch04-st4', 'ch04-st4')],
    'group': [('ch02-st1', 'ch02-st2'), ('ch02-st3', 'ch02-st4'), ('ch02-st4', 'ch02-st4'), ('ch03-st1', 'ch03-st2'), ('ch03-st3', 'ch03-st3'), ('ch03-st4', 'ch03-st5'),
              ('ch03-st5', 'ch03-st5'), ('ch04-st1', 'ch04-st1'), ('ch04-st2', 'ch04-st2'), ('ch04-st3', 'ch04-st3'), ('ch04-st3', 'ch04-st4'), ('ch04-st4', 'ch04-st4'), ('ch04-st4', 'ch04-st5'), ('ch04-st5', 'ch04-st5'), ('ch04-st5', 'ch04-st5')],
    'riya': [('ch02-st1', 'ch02-st1'), ('ch02-st2', 'ch02-st2'), ('ch02-st3', 'ch02-st4'), ('ch02-st5', 'ch02-st5'), ('ch02-st5', 'ch02-st5')],
}
NOTES = {
    'struggled': ['Lost the thread on the second worked example; slowed down and re-did it on the board.', 'Needed hints on every problem. Back to basics next time.'],
    'getting_there': ['Got there with one nudge per problem. Narrating the steps aloud helps.', 'Method is right, arithmetic slips under time pressure.'],
    'confident': ['Solved the stretch problem unaided. Ready to move on.', 'Quick and accurate today; set a harder homework.'],
}


def series(key, lids, sid, kind, slots, first, last, perf_cycle, skip=(), no_show=(), missing_report=()):
    plan = PLAN[key]
    i = 0
    d = first
    out = []
    while d <= last:
        for wd, hhmm in slots:
            if d.weekday() != wd:
                continue
            start = at(d, hhmm)
            if d in skip:
                continue
            topics_ids = plan[min(i, len(plan) - 1)]
            nxt = plan[min(i + 1, len(plan) - 1)]
            code_n[0] += 1
            sid_ = f'ses_w2t_{code_n[0]:03d}'
            past = start < NOW
            focus = short(f'{sid}-{topics_ids[0]}')
            s = {
                'id': sid_, 'code': f'S-{code_n[0]}', 'learnerId': lids[0], 'learnerIds': lids, 'hostId': TUTOR, 'hostRole': 'tutor', 'kind': kind,
                'title': f'{CH[sid + "-" + topics_ids[0][:4]]}', 'subjectId': sid, 'focus': focus, 'startUtc': iso(start), 'minutes': 60,
                'status': 'scheduled', 'mode': 'online', 'joinUrl': f'https://meet.learnibility.demo/{sid_}', 'bookingId': f'bkg_w2t_{key}',
                'rateInr': RATE_G if kind == 'group' else RATE_1, 'report': None,
            }
            if past:
                if d in no_show:
                    s['status'] = 'no_show'
                else:
                    s['status'] = 'completed'
                    if d not in missing_report:
                        perf = perf_cycle[i % len(perf_cycle)]
                        hw = []
                        due = (start + timedelta(days=2)).date()
                        for lid in lids:
                            st_done = 'done' if (due < NOW.date() and not (lid == 'lrn_rohan_das' and i % 3 == 2)) else 'todo'
                            hw.append(task(lid, f'Practise: {short(sid + "-" + topics_ids[1], 6)}', 'homework', due, st_done, sid_, 30, sid,
                                           detail=f'Homework from {s["code"]}'))
                        s['report'] = {
                            'topics': [sname(f'{sid}-{t}') for t in dict.fromkeys(topics_ids)],
                            'performance': perf, 'engagement': 'high' if perf == 'confident' else 'medium' if perf == 'getting_there' else ('low' if key == 'rohan' else 'medium'),
                            'notes': NOTES[perf][i % 2], 'homeworkTaskIds': hw, 'nextFocus': short(f'{sid}-{nxt[0]}', 7),
                            'submittedUtc': iso(start + timedelta(minutes=75)),
                        }
                        if i % 4 == 1:
                            for lid in lids[:1]:
                                notes.append({'id': f'note_w2t_{len(notes) + 1:03d}', 'learnerId': lid, 'tutorId': TUTOR, 'text': s['report']['notes'],
                                              'createdUtc': s['report']['submittedUtc'], 'source': 'session_report'})
            else:
                fa = f'{sid}-{topics_ids[0]}'
                s['focus'] = short(fa, 6)
            out.append(s)
            i += 1
        d += timedelta(days=1)
    sessions.extend(out)
    return out


MON, TUE, WED, THU, FRI, SAT = 0, 1, 2, 3, 4, 5
END = date(2026, 11, 27)
tanvi = series('tanvi', ['lrn_tanvi_bhatia'], P, 'one_to_one', [(MON, '18:00'), (WED, '18:00')], date(2026, 9, 28), END,
               ['getting_there', 'confident', 'getting_there', 'struggled'])
yash = series('yash', ['lrn_yash_gupta'], Y, 'one_to_one', [(MON, '16:00'), (WED, '16:00')], date(2026, 10, 5), END,
              ['getting_there', 'confident', 'confident', 'getting_there'])
rohan = series('rohan', ['lrn_rohan_das'], 'cbse-g10-maths', 'one_to_one', [(TUE, '16:00'), (THU, '16:00')], date(2026, 10, 20), END,
               ['struggled', 'getting_there', 'struggled', 'getting_there'], no_show={date(2026, 11, 5)}, missing_report={date(2026, 11, 17)})
group = series('group', ['lrn_kabir_singh', 'lrn_mehul_jain', 'lrn_arnav_khanna'], N9, 'group', [(WED, '20:00'), (FRI, '20:00')], date(2026, 10, 7), END,
               ['confident', 'getting_there', 'getting_there', 'confident'])
riya = series('riya', ['lrn_riya_sen'], R, 'one_to_one', [(SAT, '10:00')], date(2026, 10, 10), date(2026, 11, 7),
              ['getting_there', 'getting_there', 'struggled', 'getting_there'])
# Riya paused after 7 Nov (school exams); no sessions since.

# Demo sessions that started each relationship (all free)
for key, lid, sid, day, hhmm, topic in [('tanvi', 'lrn_tanvi_bhatia', P, date(2026, 9, 26), '17:00', 'Kinematics graphs feel shaky; JEE prep from scratch'),
                                        ('yash', 'lrn_yash_gupta', Y, date(2026, 10, 1), '17:00', 'Calculus for JEE, especially integration'),
                                        ('rohan', 'lrn_rohan_das', 'cbse-g10-maths', date(2026, 10, 16), '16:30', 'Parents want help before the pre-boards'),
                                        ('group', 'lrn_mehul_jain', N9, date(2026, 10, 3), '10:00', 'Small group for Class 9 maths with two friends'),
                                        ('riya', 'lrn_riya_sen', R, date(2026, 10, 3), '11:00', 'IGCSE algebra, fractions keep tripping me up')]:
    code_n[0] += 1
    sessions.append({'id': f'ses_w2t_demo_{key}', 'code': f'S-{code_n[0]}', 'learnerId': lid, 'learnerIds': [lid], 'hostId': TUTOR, 'hostRole': 'tutor', 'kind': 'demo',
                     'title': 'Free demo', 'subjectId': sid, 'focus': topic, 'startUtc': iso(at(day, hhmm)), 'minutes': 30, 'status': 'completed', 'mode': 'online',
                     'bookingId': f'bkg_w2t_demo_{key}', 'rateInr': 0, 'report': None})
    bookings.append({'id': f'bkg_w2t_demo_{key}', 'learnerId': lid, 'tutorId': TUTOR, 'kind': 'demo', 'status': 'completed', 'format': 'one_to_one', 'mode': 'online',
                     'subjectId': sid, 'priceInr': 0, 'requestedAt': iso(at(day, hhmm) - timedelta(days=2)), 'slotStartUtc': iso(at(day, hhmm)), 'minutes': 30, 'topic': topic,
                     'respondedUtc': iso(at(day, hhmm) - timedelta(days=2) + timedelta(hours=3)), 'sharedGapSnapshot': None})

# Regular bookings behind each series
for key, lids, sid, fmt, since, per_week in [('tanvi', ['lrn_tanvi_bhatia'], P, 'one_to_one', date(2026, 9, 27), 2), ('yash', ['lrn_yash_gupta'], Y, 'one_to_one', date(2026, 10, 2), 2),
                                             ('rohan', ['lrn_rohan_das'], 'cbse-g10-maths', 'one_to_one', date(2026, 10, 17), 2),
                                             ('riya', ['lrn_riya_sen'], R, 'one_to_one', date(2026, 10, 4), 1)]:
    bookings.append({'id': f'bkg_w2t_{key}', 'learnerId': lids[0], 'tutorId': TUTOR, 'kind': 'regular', 'status': 'active', 'format': fmt, 'mode': 'online', 'subjectId': sid,
                     'priceInr': RATE_1, 'requestedAt': iso(at(since, '19:00')), 'minutes': 60, 'sessionsPerWeek': per_week, 'respondedUtc': iso(at(since, '21:00')), 'sharedGapSnapshot': None})
for lid in ['lrn_kabir_singh', 'lrn_mehul_jain', 'lrn_arnav_khanna']:
    bookings.append({'id': 'bkg_w2t_group' if lid == 'lrn_kabir_singh' else f'bkg_w2t_group_{lid[4:]}', 'learnerId': lid, 'tutorId': TUTOR, 'kind': 'regular', 'status': 'active',
                     'format': 'group', 'mode': 'online', 'subjectId': N9, 'priceInr': RATE_G, 'requestedAt': iso(at(date(2026, 10, 4), '18:00')), 'minutes': 60,
                     'sessionsPerWeek': 2, 'respondedUtc': iso(at(date(2026, 10, 4), '20:00')), 'sharedGapSnapshot': None})

# Rohan's paid booking needs his parent's approval (W2-P shows it); approved when it started.
for b in bookings:
    if b['id'] == 'bkg_w2t_rohan':
        b['parentApproval'] = {'parentId': 'par_sunita_das', 'status': 'approved', 'utc': iso(at(date(2026, 10, 18), '10:00'))}
        b['matchReason'] = 'Strong in Quadratic equations; concept-first teaching; ₹800/hr within budget; 4.8★ from 31 reviews.'

# Open requests (2b, 2c)
def snap(lid, sid, score, ids):
    gs = [g for g in gaps if g['learnerId'] == lid and g['subtopicId'] in ids]
    return {'sharedUtc': iso(NOW - timedelta(hours=14)), 'subjectId': sid, 'score': score,
            'gaps': [{'gapId': g['id'], 'subtopicId': g['subtopicId'], 'name': sname(g['subtopicId']), 'code': g['code'], 'level': g['level'], 'hoursToClose': g['hoursToClose']} for g in gs]}


sana_slot = at(date(2026, 11, 19), '17:00')
dev_slot = at(date(2026, 11, 20), '17:00')
code_n[0] += 1
sessions.append({'id': 'ses_w2t_demo_sana', 'code': f'S-{code_n[0]}', 'learnerId': 'lrn_sana_malik', 'learnerIds': ['lrn_sana_malik'], 'hostId': TUTOR, 'hostRole': 'tutor',
                 'kind': 'demo', 'title': 'Free demo', 'subjectId': P, 'focus': 'Rotational motion from basics', 'startUtc': iso(sana_slot), 'minutes': 30, 'status': 'scheduled',
                 'mode': 'online', 'joinUrl': 'https://meet.learnibility.demo/ses_w2t_demo_sana', 'bookingId': 'bkg_w2t_req_sana', 'rateInr': 0, 'report': None})
bookings.append({'id': 'bkg_w2t_req_sana', 'learnerId': 'lrn_sana_malik', 'tutorId': TUTOR, 'kind': 'demo', 'status': 'requested', 'format': 'one_to_one', 'mode': 'online',
                 'subjectId': P, 'priceInr': 0, 'requestedAt': iso(NOW - timedelta(hours=14)), 'slotStartUtc': iso(sana_slot), 'minutes': 30, 'sessionsPerWeek': 2,
                 'topic': "Rotational motion and I don't get along. Need someone who explains from basics.",
                 'sharedGapSnapshot': snap('lrn_sana_malik', P, 58, [f'{P}-ch06-st4', f'{P}-ch07-st3', f'{P}-ch06-st2']),
                 'matchReason': 'Strong in Rotational motion and Gravitation; concept-first teaching suits a G2 gap; ₹800/hr; 4.8★ from 31 reviews.'})
code_n[0] += 1
sessions.append({'id': 'ses_w2t_demo_dev', 'code': f'S-{code_n[0]}', 'learnerId': 'lrn_dev_arora', 'learnerIds': ['lrn_dev_arora'], 'hostId': TUTOR, 'hostRole': 'tutor',
                 'kind': 'demo', 'title': 'Free demo', 'subjectId': 'cbse-g10-maths', 'focus': 'Quadratic equations', 'startUtc': iso(dev_slot), 'minutes': 30, 'status': 'scheduled',
                 'mode': 'online', 'joinUrl': 'https://meet.learnibility.demo/ses_w2t_demo_dev', 'bookingId': 'bkg_w2t_req_dev', 'rateInr': 0, 'report': None})
bookings.append({'id': 'bkg_w2t_req_dev', 'learnerId': 'lrn_dev_arora', 'tutorId': TUTOR, 'kind': 'demo', 'status': 'requested', 'format': 'one_to_one', 'mode': 'online',
                 'subjectId': 'cbse-g10-maths', 'priceInr': 0, 'requestedAt': iso(NOW - timedelta(hours=5)), 'slotStartUtc': iso(dev_slot), 'minutes': 30, 'sessionsPerWeek': 3,
                 'topic': 'Quadratic equations word problems before the pre-boards. Budget about ₹700 an hour.', 'note': 'Budget ₹700/hr',
                 'sharedGapSnapshot': snap('lrn_dev_arora', 'cbse-g10-maths', 64, [f'cbse-g10-maths-ch04-st3', 'cbse-g10-maths-ch04-st4', 'cbse-g10-maths-ch02-st3'])})

# Payouts: every Monday, net of 15% fee, for reported sessions up to the previous Sunday
def gross(s):
    return round(s['rateInr'] * s['minutes'] / 60) * (len(s['learnerIds']) if s['kind'] == 'group' else 1)


payouts = []
paid = set()
mon = date(2026, 10, 5)
while mon <= NOW.date():
    cutoff = at(mon, '00:00')
    ids = [s['id'] for s in sessions if s['status'] == 'completed' and s['report'] and s['rateInr'] > 0 and s['id'] not in paid and datetime.fromisoformat(s['startUtc'].replace('Z', '+00:00')) < cutoff]
    if ids:
        amt = sum(gross(s) - round(gross(s) * FEE) for s in sessions if s['id'] in ids)
        payouts.append({'id': f'pay_w2t_{mon.isoformat()}', 'tutorId': TUTOR, 'amountInr': amt, 'paidOn': mon.isoformat(), 'sessionIds': ids})
        paid.update(ids)
    mon += timedelta(days=7)

# ------------------------------------------------------------------ assignments (4g, 4h, 4k)

def q(i, kind, stid, stem, answer, marks, student_answer, correct, ai_score=None, ai_fb=None, review=False, options=None, rubric=None):
    return {'n': i, 'id': f'tq_{stid}_{i:02d}', 'type': kind, 'subtopicId': stid, 'stem': stem, 'options': options, 'answer': answer, 'markingKey': rubric or answer,
            'marks': marks}, {'questionId': f'tq_{stid}_{i:02d}', 'correct': correct, 'answer': student_answer, 'aiScore': ai_score if ai_score is not None else (marks if correct else 0),
                              'aiFeedback': ai_fb, 'needsReview': review}


T4 = f'{P}-ch04'
hw3 = [
    q(1, 'mcq', f'{T4}-st1', 'A 2 kg block is pushed with a net force of 6 N. Its acceleration is', '3 m/s²', 1, '3 m/s²', True, options=['12 m/s²', '3 m/s²', '0.33 m/s²', '8 m/s²']),
    q(2, 'mcq', f'{T4}-st1', 'The impulse of a force equals the change in', 'momentum', 1, 'momentum', True, options=['velocity', 'kinetic energy', 'momentum', 'acceleration']),
    q(3, 'numerical', f'{T4}-st2', 'Two blocks of 3 kg and 5 kg hang over a frictionless pulley. Find the acceleration (g = 10 m/s²).', '2.5 m/s²', 1, 'a = g(5−3)/5 = 4 m/s²', False,
      ai_fb='Used a single-body equation; the string constraint a₁ = a₂ was never written, so the denominator misses the 3 kg block. Correct: a = (5−3)g/(5+3) = 2.5 m/s².'),
    q(4, 'numerical', f'{T4}-st3', 'A 4 kg block on a rough incline (30°, μ = 0.2) is released. Find its acceleration.', '3.27 m/s²', 1, '6.73 m/s²', False,
      ai_fb='Sign of friction reversed: friction opposes the motion down the slope, so a = g(sin30° − μcos30°) = 3.27 m/s².'),
    q(5, 'mcq', f'{T4}-st2', 'In a free-body diagram of a book resting on a table, the forces are', 'weight and normal force', 1, 'weight and normal force', True,
      options=['weight only', 'weight and normal force', 'normal force and friction', 'weight, normal force and friction']),
    q(6, 'explain', f'{T4}-st2', 'Explain why tension is equal on both sides of an ideal pulley.', 'Massless string and massless, frictionless pulley', 10,
      'Because the string is massless so the force is the same everywhere along it.', None, ai_score=6, ai_fb='Partially correct: mentions the massless string but not the frictionless (and massless) pulley.', review=True,
      rubric='Massless string (4) · frictionless pulley (3) · massless pulley so no net torque needed (3)'),
    q(7, 'numerical', f'{T4}-st1', 'A 0.15 kg ball hits a wall at 20 m/s and rebounds at 15 m/s. Find the impulse.', '5.25 N s', 1, '5.25 N s', True),
    q(8, 'mcq', f'{T4}-st3', 'Static friction on a block at rest on a horizontal floor with no applied force is', 'zero', 1, 'zero', True, options=['μN', 'zero', 'mg', 'μmg']),
    q(9, 'numerical', f'{T4}-st4', 'Find the maximum safe speed on a flat curve of radius 50 m with μ = 0.4 (g = 10).', '14.1 m/s', 1, '14.1 m/s', True),
    q(10, 'explain', f'{T4}-st3', 'Why is it easier to pull a lawn roller than to push it at the same angle?', 'Pulling reduces the normal force, so friction is smaller', 10,
      'When you pull, part of your force lifts the roller so normal force is less and friction is less.', None, ai_score=9, ai_fb='Correct idea and reason. Could name the vertical component explicitly.', review=True,
      rubric='Vertical component of the pull reduces N (5) · friction = μN so it drops (5)'),
    q(11, 'mcq', f'{T4}-st1', "Newton's third-law forces act on", 'different bodies', 1, 'the same body', False, options=['the same body', 'different bodies', 'only moving bodies', 'only bodies in contact']),
    q(12, 'numerical', f'{T4}-st2', 'A 10 kg mass hangs from two strings at 30° and 60° to the ceiling. Find the tension in the 30° string (g = 10).', '50 N', 1, '50 N', True),
]
asg = []


def assignment(aid, lid, title, stids, qs, status, due, score=None, max_score=None, extra=None):
    a = {'id': aid, 'learnerId': lid, 'tutorId': TUTOR, 'title': title, 'subtopicIds': stids, 'questionIds': [x[0]['id'] for x in qs], 'status': status, 'dueOn': due.isoformat(),
         'questions': [x[0] for x in qs], 'source': 'ai', 'evaluation': 'ai_review', 'timeLimitMin': 30}
    if status not in ('assigned', 'draft', 'overdue', 'in_progress'):
        a['perQuestion'] = [x[1] for x in qs]
    if score is not None:
        a['score'], a['maxScore'] = score, max_score
    if extra:
        a.update(extra)
    asg.append(a)


assignment('asg_w2t_tanvi_hw3', 'lrn_tanvi_bhatia', "Laws of Motion HW-3", [f'{T4}-st1', f'{T4}-st2', f'{T4}-st3'], hw3, 'ai_evaluated', date(2026, 11, 16), 22, 30,
           {'submittedUtc': iso(at(date(2026, 11, 16), '21:40')), 'minutesTaken': 28,
            'feedback': {'strength': 'Free-body diagrams drawn correctly; recognises which law applies.', 'weakness': 'Picks the wrong equation for connected bodies; friction sign errors on inclines.',
                         'nextStep': '15-minute practice on constraint equations, then review in the next session.'}})
simple = lambda stid, n, right: [q(i + 1, 'numerical' if i % 2 else 'mcq', stid, f'Practice item {i + 1}: {sname(stid)}', 'see key', 1, 'see key' if i < right else '—', i < right) for i in range(n)]
assignment('asg_w2t_tanvi_kin', 'lrn_tanvi_bhatia', 'Kinematics quiz', [f'{P}-ch02-st2', f'{P}-ch02-st3'], simple(f'{P}-ch02-st2', 20, 18), 'completed', date(2026, 10, 21), 18, 20)
assignment('asg_w2t_tanvi_units', 'lrn_tanvi_bhatia', 'Units practice', [f'{P}-ch01-st2'], simple(f'{P}-ch01-st2', 20, 19), 'completed', date(2026, 10, 7), 19, 20)
assignment('asg_w2t_tanvi_proj', 'lrn_tanvi_bhatia', 'Projectile motion set', [f'{P}-ch03-st3'], simple(f'{P}-ch03-st3', 15, 11), 'completed', date(2026, 11, 4), 11, 15)
assignment('asg_w2t_tanvi_pulley', 'lrn_tanvi_bhatia', 'Pulley practice set', [f'{T4}-st2'], simple(f'{T4}-st2', 8, 0), 'in_progress', date(2026, 11, 20))
assignment('asg_w2t_yash_der', 'lrn_yash_gupta', 'Derivatives in context', [f'{Y}-ch06-st1', f'{Y}-ch06-st3'], simple(f'{Y}-ch06-st3', 20, 16), 'completed', date(2026, 10, 28), 16, 20)
assignment('asg_w2t_yash_int1', 'lrn_yash_gupta', 'Integrals drill 1', [f'{Y}-ch07-st1', f'{Y}-ch07-st2'], simple(f'{Y}-ch07-st2', 20, 15), 'completed', date(2026, 11, 11), 15, 20)
assignment('asg_w2t_yash_int2', 'lrn_yash_gupta', 'Partial fractions set', [f'{Y}-ch07-st3'], simple(f'{Y}-ch07-st3', 12, 0), 'assigned', date(2026, 11, 21))
assignment('asg_w2t_rohan_poly', 'lrn_rohan_das', 'Polynomials HW', ['cbse-g10-maths-ch02-st3'], simple('cbse-g10-maths-ch02-st3', 15, 9), 'completed', date(2026, 10, 29), 9, 15)
assignment('asg_w2t_rohan_quad', 'lrn_rohan_das', 'Quadratic equations set', ['cbse-g10-maths-ch04-st2', 'cbse-g10-maths-ch04-st3'], simple('cbse-g10-maths-ch04-st3', 12, 0), 'overdue', date(2026, 11, 14))
assignment('asg_w2t_kabir_id', 'lrn_kabir_singh', 'Algebraic identities practice', [f'{N9}-ch04-st2', f'{N9}-ch04-st3'], simple(f'{N9}-ch04-st3', 10, 0), 'assigned', date(2026, 11, 20))
assignment('asg_w2t_riya_frac', 'lrn_riya_sen', 'Algebraic fractions set', [f'{R}-ch02-st5'], simple(f'{R}-ch02-st5', 12, 6), 'completed', date(2026, 11, 5), 6, 12)
for a in asg:
    if a['status'] in ('assigned', 'in_progress', 'overdue'):
        tid = task(a['learnerId'], f'Complete {a["title"]}', 'test', date.fromisoformat(a['dueOn']), 'todo', a['id'], 30, a['subtopicIds'][0].rsplit('-ch', 1)[0], detail='Assigned by your tutor')
        a['taskId'] = tid
# extra open tasks for Rohan's "overdue" signal
task('lrn_rohan_das', 'Re-read NCERT 4.3 and redo examples 9–11', 'learn', date(2026, 11, 13), 'todo', 'ses_w2t_rohan', 30, 'cbse-g10-maths', detail='Forgot · from S-session notes')

# ------------------------------------------------------------------ messages and notes (4n, 4o)

def msg(lid, frm, text, when):
    messages.append({'id': f'msg_w2t_{len(messages) + 1:03d}', 'threadId': f'{lid}:{TUTOR}', 'learnerId': lid, 'from': frm, 'toIds': [lid, TUTOR] if frm == 'system' else ([TUTOR] if frm == lid else [lid]),
                     'text': text, 'sentUtc': iso(when), 'tutorId': TUTOR, 'readBy': [TUTOR, lid]})


msg('lrn_tanvi_bhatia', 'lrn_tanvi_bhatia', "Sir, I couldn't solve Q3 and Q4 in HW-3. The pulley and the incline ones.", at(date(2026, 11, 16), '21:52'))
msg('lrn_tanvi_bhatia', TUTOR, "Saw it. Those are constraint and friction-direction problems. We'll do them first thing on Wednesday. Try the pulley practice set before then.", at(date(2026, 11, 16), '22:10'))
msg('lrn_tanvi_bhatia', 'system', 'Rahul assigned Pulley practice set · due Fri 20 Nov', at(date(2026, 11, 16), '22:11'))
msg('lrn_tanvi_bhatia', 'lrn_tanvi_bhatia', 'Done with 3 of 8, rest tonight 👍', at(date(2026, 11, 17), '20:05'))
msg('lrn_rohan_das', TUTOR, 'Rohan, the quadratic set was due Saturday. Can you finish the first 6 questions before Tuesday?', at(date(2026, 11, 15), '18:30'))
msg('lrn_rohan_das', 'lrn_rohan_das', 'sorry sir had cricket practice, will do', at(date(2026, 11, 16), '22:47'))
msg('lrn_riya_sen', 'lrn_riya_sen', 'Ma’am said school exams start 9 Nov so I will pause tuition for two weeks.', at(date(2026, 11, 7), '12:15'))
msg('lrn_riya_sen', TUTOR, 'All the best Riya. Message me when you are back and we will pick up with algebraic fractions.', at(date(2026, 11, 7), '13:02'))
msg('lrn_yash_gupta', 'lrn_yash_gupta', 'Can we do more definite integrals PYQs this week?', at(date(2026, 11, 12), '19:20'))
msg('lrn_yash_gupta', TUTOR, 'Yes, I will bring 5 JEE PYQs on Monday.', at(date(2026, 11, 12), '19:41'))
msg('lrn_kabir_singh', 'system', 'Rahul assigned Algebraic identities practice · due Fri 20 Nov', at(date(2026, 11, 13), '21:10'))

for lid, text, when in [
        ('lrn_tanvi_bhatia', 'First demo: sharp, a bit impatient. Prefers problems over theory. Likes cricket analogies.', at(date(2026, 9, 26), '18:00')),
        ('lrn_tanvi_bhatia', 'Parent call: mother wants a fortnightly progress summary. School exams start 7 Dec, plan lighter homework that week.', at(date(2026, 10, 28), '20:30')),
        ('lrn_tanvi_bhatia', 'Struggles with choosing the equation under time pressure. Confident when talking it through aloud; make her narrate before writing.', at(date(2026, 11, 11), '19:20')),
        ('lrn_rohan_das', 'Parent (Mrs Das) is anxious about pre-boards. Rohan responds to short wins; keep homework to 20 minutes.', at(date(2026, 10, 20), '17:30')),
        ('lrn_kabir_singh', 'Quick but careless: drops signs when expanding. Ask him to check one line at a time.', at(date(2026, 10, 30), '21:20'))]:
    notes.append({'id': f'note_w2t_{len(notes) + 1:03d}', 'learnerId': lid, 'tutorId': TUTOR, 'text': text, 'createdUtc': iso(when), 'source': 'manual'})

out = {
    'schemaVersion': 1,
    'generatedBy': 'scripts/w2t/build_tutor_fixtures.py',
    'collections': {
        'student': BG, 'gaps': gaps, 'mastery': mastery, 'attempts': attempts, 'bookings': bookings, 'sessions': sorted(sessions, key=lambda s: s['startUtc']),
        'assignments': asg, 'messages': messages, 'tutorNotes': notes, 'payouts': payouts, 'tasks': tasks,
    },
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print({k: len(v) for k, v in out['collections'].items()}, 'payout total', sum(p['amountInr'] for p in payouts))
