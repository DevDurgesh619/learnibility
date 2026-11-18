"""Cambridge International AS & A Level History 9489, A Level year (grade 12): Paper 3 Historical
Interpretations (the origins of the First World War; the Holocaust; the origins and development of
the Cold War, 1941-50) and Paper 4 Depth Studies (European history 1919-41: Mussolini's Italy,
Stalin's USSR, Hitler's Germany; the USA 1945-93: the economy, society and civil rights, politics
and the presidency; international history 1909-94: the Cold War in Europe, South Africa, nationalism
and decolonisation in Southeast Asia).

Paper 3 is one question on an extract from a historian: 'What can you learn from this extract about
the interpretation and approach of the historian who wrote it?' [40]. Paper 4 essays are marked out
of 30. The platform caps an item at 20 marks, so full Paper 3 and Paper 4 answers are set here at 20
marks with the levels scaled; shorter skill items (identifying the interpretation, the approach, testing
it against evidence, comparing extracts, planning) build towards them.

Extracts are labelled '(illustrative)' and attributed to unnamed historians; where a real historian's
argument is used it is summarised and marked as a summary, never quoted. Primary sources are either
well-attested words (quoted or summarised, marked as such) or labelled '(illustrative)'.
Builders for dates, 'Explain why', essays and sources come from g11_history.
"""
import re as _re

from ._lib import mcq, CTX, person
from .g9_history import S, T, cap, low2, _dot, _mins, add_terms, add_mcqs, add_claims, finalize, _markify
from .g11_history import add_dates, add_why, add_as_essays, add_as_sources, PROFILE, N_W  # noqa: F401

CHAPTERS = {}

ESS4_KEY = ('Level 5 (17-20): a focused, balanced and analytical answer with a sustained, well-supported judgement; precise and relevant knowledge throughout. '
            'Level 4 (13-16): analysis of both sides with a judgement, though not fully sustained or supported. '
            'Level 3 (9-12): some analysis, but one-sided or uneven, or with descriptive passages. Level 2 (5-8): mainly descriptive or narrative, with limited links to the question. '
            'Level 1 (1-4): general, unsupported or irrelevant points. (The examination essay is marked out of 30; levels are scaled.)')
WHY4_KEY = ('Level 4 (9-10): analyses a range of factors, showing how they interact, with a supported judgement on their relative importance. '
            'Level 3 (6-8): explains two or more factors with accurate support. Level 2 (3-5): describes or identifies factors, or explains one. Level 1 (1-2): general points.')
P3_KEY = ('Level 5 (17-20): demonstrates a full understanding of the historian\'s interpretation and approach, explained with close reference to the extract and '
          'tested against accurate own knowledge. Level 4 (13-16): explains the main interpretation with support from the extract and shows some understanding of the approach. '
          'Level 3 (9-12): identifies the main interpretation with some support, or explains sub-messages. Level 2 (5-8): identifies sub-messages or makes valid points about the topic linked to the extract. '
          'Level 1 (1-4): paraphrases or summarises the extract, or writes about the topic without reference to it. (The examination question is marked out of 40; levels are scaled.)')
CMPX_KEY = ('Up to 4 marks for identifying and explaining the interpretation of each extract with support; up to 4 marks for explaining how they differ, '
            'including their approaches or use of evidence; up to 2 marks for explaining why they differ (context, evidence available, school of thought)')
WHICH_KEY = ('Level 5 (17-20): evaluates both interpretations against own knowledge and their approach and use of evidence, reaching a sustained judgement on which is more convincing. '
             'Level 4 (13-16): tests both interpretations against own knowledge with a judgement. Level 3 (9-12): explains both interpretations and tests one. '
             'Level 2 (5-8): explains the interpretations without testing them. Level 1 (1-4): paraphrases the extracts.')


def X(who, text, school, view, approach, appr, sup, chal, context='', excl=()):
    return dict(who=who, text=text, school=school, view=view, approach=approach, appr=appr, sup=sup, chal=chal, context=context, excl=tuple(excl))


def _first(x):
    return _re.split(r'(?<=[.!?])\s', x['text'])[0]


def _xin(r, x, L=None):
    if L:
        return f'Extract {L}: {x["who"]}. “{x["text"]}”'
    return r.choice([f'Read the extract and then answer the question. Extract: {x["who"]}. “{x["text"]}”',
                     f'The following extract is from {x["who"]}. “{x["text"]}”',
                     f'Study the extract. “{x["text"]}” ({cap(x["who"])}.)'])


def add_interp(t, P):
    XS = P.get('ext', [])
    topic_ = P.get('enq', 'this topic')
    schools = [s for s, _ in P.get('schools', [])]
    sdesc = dict(P.get('schools', []))
    approaches = P.get('approaches', [])
    for x in XS:
        if len([s for s in schools if s not in x['excl']]) >= 4 and x['school'] in schools:
            def fsch(r, D, x=x):
                opts, a = mcq(r, x['school'], [s for s in schools if s != x['school'] and s not in x['excl']])
                q = r.choice(['Which interpretation does the extract best represent?', 'Which school of thought is the historian most closely associated with?',
                              'Which of these best describes the interpretation in the extract?'])
                return {'stem': _xin(r, x) + ' ' + q, 'options': opts, 'answer': a,
                        'key': f'{a}: {sdesc.get(a, "")}. The extract argues that {low2(x["view"])} [1]', 'marks': 1, 'minutes': 2}
            fsch.__name__ = 'school_mcq'
            t.add('C1', (1, 2, 3), 'mcq')(fsch)
        if len(approaches) >= 4 and x['appr'] in approaches:
            def fap(r, D, x=x):
                opts, a = mcq(r, x['appr'], [s for s in approaches if s != x['appr']])
                return {'stem': _xin(r, x) + ' Which of these best describes the approach of the historian who wrote the extract?', 'options': opts, 'answer': a,
                        'key': f'{_dot(x["approach"])} [1]', 'marks': 1, 'minutes': 2}
            fap.__name__ = 'approach_mcq'
            t.add('C2', (1, 2, 3), 'mcq')(fap)

        def fid(r, D, x=x):
            m = 3 if D <= 2 else 4
            n = 1 if m == 3 else 2
            q = r.choice([f'What is the main interpretation of the historian in the extract? Support your answer with {N_W[n] if n > 1 else "a"} detail{"s" if n > 1 else ""} from the extract.',
                          f'Identify the historian\'s interpretation of {topic_} and explain how the extract supports it.'])
            return {'stem': _xin(r, x) + ' ' + q, 'answer': f'Interpretation: {x["view"]} Support from the extract: for example, “{_first(x)}”',
                    'key': f'1 mark for identifying a sub-message; 2 marks for the main interpretation; up to {m - 2} mark{"s" if m > 3 else ""} for supporting detail from the extract [{m}]',
                    'type': 'explain', 'marks': m, 'minutes': _mins(m)}
        fid.__name__ = 'interp_id'
        t.add('C2', (2, 3, 4), 'explain')(fid)

        def fapp(r, D, x=x):
            return {'stem': _xin(r, x) + ' ' + r.choice(['Explain what the extract reveals about the historian\'s approach.', 'How does the historian approach the question? Use the extract to explain your answer.']),
                    'answer': f'Approach: {x["approach"]} Interpretation it supports: {x["view"]}',
                    'key': '1 mark for identifying the approach; up to 2 marks for explaining it with reference to the extract; 1 mark for linking the approach to the interpretation [4]',
                    'type': 'explain', 'marks': 4, 'minutes': 5}
        fapp.__name__ = 'approach'
        t.add('C2', (2, 3, 4), 'explain')(fapp)

        def fok(r, D, x=x):
            m = 10 if (CTX.get('want_marks') or 8) >= 10 or D >= 5 else 8
            return {'stem': _xin(r, x) + ' ' + r.choice([f'Use your knowledge of {topic_} to explain how far the evidence supports the interpretation in the extract.',
                                                          'How far does your own knowledge support the interpretation in the extract? Explain your answer.']),
                    'answer': 'Supporting evidence: ' + ' '.join(_dot(s) for s in x['sup']) + ' Challenging evidence: ' + ' '.join(_dot(s) for s in x['chal']) + ' Judgement: the interpretation is supported in part; its strength depends on the evidence it emphasises.',
                    'key': f'1 mark for identifying the interpretation; up to {(m - 2) // 2} marks for own knowledge that supports it and up to {(m - 2) // 2} for knowledge that challenges it, each linked to the extract; 1 mark for a supported judgement [{m}]',
                    'type': 'case', 'marks': m, 'minutes': _mins(m)}
        fok.__name__ = 'test_interp'
        t.add('C3', (2, 3, 4, 5), 'case')(fok)

        if x.get('context'):
            def fctx(r, D, x=x):
                return {'stem': _xin(r, x) + ' Explain how the time and circumstances in which the historian was writing might have shaped this interpretation.',
                        'answer': f'{x["context"]} This helps explain the interpretation: {x["view"]}',
                        'key': '1 mark for identifying a relevant context; up to 2 marks for explaining it; up to 2 marks for linking it to features of the interpretation in the extract [5]',
                        'type': 'explain', 'marks': 5, 'minutes': 7}
            fctx.__name__ = 'context'
            t.add('C3', (2, 3, 4), 'explain')(fctx)

        def fp3(r, D, x=x):
            if D <= 2:
                return {'stem': _xin(r, x) + ' Identify the historian\'s main interpretation and one feature of the historian\'s approach. Use the extract to support your answer.',
                        'answer': f'Interpretation: {x["view"]} Approach: {x["approach"]}',
                        'key': '2 marks for the main interpretation and 1 for support from the extract; 2 marks for a feature of the approach and 1 for support [6]', 'type': 'case', 'marks': 6, 'minutes': 8}
            q = (f'What can you learn from this extract about the interpretation and approach of the historian who wrote it? '
                 f'Use the extract and your knowledge of {topic_} to explain your answer.')
            return {'stem': _xin(r, x) + ' ' + q,
                    'answer': f'Interpretation: {x["view"]} Approach: {x["approach"]} Own knowledge that supports it: ' + ' '.join(_dot(s) for s in x['sup']) +
                              ' Own knowledge that challenges it: ' + ' '.join(_dot(s) for s in x['chal']) + (f' Context: {x["context"]}' if x.get('context') else ''),
                    'key': P3_KEY + ' [20]', 'type': 'case', 'marks': 20, 'minutes': 30}
        fp3.__name__ = 'paper3'
        t.add('C4', (2, 3, 4, 5), 'case')(fp3)

    if len(XS) >= 2:
        def fcmp(r, D):
            a, b = r.sample(XS, 2)
            return {'stem': f'Read the two extracts. {_xin(r, a, "A")} {_xin(r, b, "B")} ' + r.choice(['How do the interpretations in Extracts A and B differ? Explain your answer with reference to the approaches of the historians.',
                                                                                                         'Compare the interpretations of the historians who wrote Extracts A and B. Explain why they might differ.']),
                    'answer': f'Extract A: {a["view"]} ({a["school"]}; approach: {low2(a["approach"])}) Extract B: {b["view"]} ({b["school"]}; approach: {low2(b["approach"])}) They differ in the evidence and factors each emphasises.',
                    'key': CMPX_KEY + ' [10]', 'type': 'case', 'marks': 10, 'minutes': 15}
        fcmp.__name__ = 'compare_x'
        t.add('C3', (3, 4, 5), 'case')(fcmp)

        def fwhich(r, D):
            a, b = r.sample(XS, 2)
            return {'stem': f'Read the two extracts. {_xin(r, a, "A")} {_xin(r, b, "B")} Which extract offers the more convincing interpretation of {topic_}? Use both extracts and your own knowledge to explain your answer.',
                    'answer': f'Extract A: {a["view"]} Support: {_dot(a["sup"][0])} Challenge: {_dot(a["chal"][0])} Extract B: {b["view"]} Support: {_dot(b["sup"][0])} Challenge: {_dot(b["chal"][0])} Any supported judgement.',
                    'key': WHICH_KEY + ' [20]', 'type': 'case', 'marks': 20, 'minutes': 30}
        fwhich.__name__ = 'which_x'
        t.add('C4', (3, 4, 5), 'case')(fwhich)


def build_a2(t, P):
    start = len(t.templates)
    add_terms(t, P.get('terms', []))
    add_dates(t, P.get('dates', []))
    add_mcqs(t, P.get('mcq', []))
    add_why(t, P, lead_full='Analyse the reasons why', wkey=WHY4_KEY)
    add_claims(t, P.get('claims', []))
    add_as_essays(t, P, ekey=ESS4_KEY)
    add_as_sources(t, P)
    add_interp(t, P)
    _markify(t, start)
    t.pack = P
    return t


def add_data(t, C, D, typ='numerical'):
    return t.add(C, D, typ)


# ============================================================== CHAPTER 1: Historical interpretations, the origins of the First World War

SCH1 = [('German responsibility (the Fischer thesis)', 'Germany deliberately sought or risked a European war to achieve dominance'),
        ('Shared responsibility', 'several great powers contributed to a war that none of them fully intended'),
        ('Structural explanation', 'long-term forces such as alliances, arms races and military planning made war likely'),
        ('Marxist-Leninist interpretation', 'the war resulted from rivalry between capitalist imperialist powers'),
        ('Primacy of domestic politics', 'leaders risked war to escape crises and pressures at home')]
APP1 = ['Intentionalist: focuses on the aims and decisions of leaders', 'Structural: focuses on long-term impersonal forces and the international system',
        'Diplomatic: reconstructs decisions taken in several capitals during the July Crisis', 'Economic: explains events through economic interests and class']
WW1 = dict(schools=SCH1, approaches=APP1, enq='the origins of the First World War')

o1a = T('The Fischer thesis and German responsibility for war', 'fischer thesis', 'german responsibility for war')
build_a2(o1a, dict(WW1, **{
    'claim': 'Germany was mainly responsible for the outbreak of war in 1914',
    'stim': ['In 1961 Fritz Fischer published Griff nach der Weltmacht (translated as Germany\'s Aims in the First World War).', 'On 5-6 July 1914 Germany promised Austria-Hungary its full support against Serbia.',
             'Article 231 of the Treaty of Versailles made Germany accept responsibility for the war.'],
    'terms': [
        ('blank cheque', 'Germany\'s promise of 5-6 July 1914 to support Austria-Hungary in whatever action it took against Serbia'),
        ('September Programme', 'the list of German war aims drawn up for Bethmann Hollweg in September 1914, including domination of central Europe'),
        ('war council of December 1912', 'the meeting of the Kaiser with his military chiefs at which Moltke said war was unavoidable and "the sooner the better"'),
        ('Weltpolitik', 'Germany\'s policy from the late 1890s of seeking world power status through colonies and a large navy'),
        ('encirclement', 'the German fear of being surrounded by the hostile powers of the Triple Entente'),
        ('Fischer controversy', 'the fierce debate among German historians in the 1960s over Fischer\'s claim that Germany sought war'),
    ],
    'dates': [('Fischer published Griff nach der Weltmacht', 1961), ('the Kaiser held the "war council" with his military chiefs', 1912, 12.08), ('Germany gave Austria-Hungary the "blank cheque"', 1914, 7.05),
              ('Bethmann Hollweg\'s September Programme was drawn up', 1914, 9.09), ('Fischer published Krieg der Illusionen (War of Illusions)', 1969)],
    'mcq': [
        ('Which German chancellor\'s policies in 1914 were central to Fischer\'s argument?', 'Bethmann Hollweg', ['Bismarck', 'Stresemann', 'Brüning'], '[1]'),
        ('What kind of evidence did Fischer mainly use?', 'German government archives', ['Soldiers\' letters from the front', 'Soviet party records', 'British newspaper reports'], 'He used records of the imperial government, some newly accessible. [1]'),
        ('Why was the Fischer thesis so controversial in West Germany in the 1960s?', 'It suggested continuity between the aims of imperial Germany and those of Nazi Germany', ['It blamed Britain for the war', 'It denied that Germany had lost the war', 'It argued that Russia started the war deliberately'], '[1]'),
    ],
    'why': [
        ('the Fischer thesis caused such controversy in the 1960s', ['It overturned the post-war West German consensus that the powers had slid into war together', 'It implied continuity of aims from the Kaiser to Hitler',
                                                                   'It relied on documents that critics argued were read selectively', 'It reopened the question of war guilt settled by Article 231'],
         'its claim of continuity with Nazi aims touched the most sensitive issue in post-war German identity'),
    ],
    'claims': [
        ('Fischer argued that Germany bore the main responsibility for the outbreak of war in 1914.', True, 'He argued that Germany\'s leaders deliberately risked or sought a European war.'),
        ('The September Programme was drawn up before the July Crisis.', False, 'It was drawn up in September 1914, after the war had begun.'),
        ('Fischer\'s later work stressed domestic pressures on German leaders.', True, 'War of Illusions (1969) linked foreign policy to the elite\'s fear of socialism at home.'),
    ],
    'ess': [
        dict(q='‘Germany was mainly responsible for the outbreak of war in 1914.’',
             pro=['The blank cheque encouraged Austria to take a hard line', 'German war plans required an attack on France through Belgium', 'German leaders believed a war sooner was better than later'],
             con=['Austria-Hungary decided on war against Serbia for its own reasons', 'Russia\'s general mobilisation turned a local war into a European one', 'The alliance system and arms races made all powers ready for war'],
             judge='Germany bears a heavy share of responsibility for turning a Balkan crisis into a European war, but it was not alone'),
        dict(q='How convincing is the Fischer thesis?',
             pro=['It is based on extensive German documents', 'The blank cheque and German pressure on Vienna support it', 'German military leaders spoke of preventive war'],
             con=['The September Programme came after the war began', 'It neglects decisions in Vienna, St Petersburg and Paris', 'The 1912 war council led to no immediate plan'],
             judge='Fischer showed convincingly that German leaders accepted the risk of war, but his claim of a long-planned war of conquest is less convincing'),
    ],
    'ext': [
        X('a historian writing in the 1960s (illustrative)', 'The documents of the German government leave little room for doubt. From the meeting of December 1912 to the war aims of September 1914, Germany\'s leaders pursued one aim: to break out of encirclement and establish German mastery in Europe. The blank cheque was not a blunder but a calculated risk, taken in the knowledge that it would probably bring a continental war.',
          'German responsibility (the Fischer thesis)', 'Germany\'s leaders deliberately risked a European war in 1914 to achieve a long-standing aim of dominating Europe.',
          'The historian relies on German government documents and focuses on the aims and decisions of German leaders, tracing continuity from before the war into its war aims.', APP1[0],
          ['The blank cheque of 5-6 July 1914 promised Austria unconditional support', 'German leaders urged Vienna to act quickly against Serbia', 'The September Programme set out annexationist aims'],
          ['The September Programme was drawn up after war began, so it may not show pre-war aims', 'The 1912 meeting led to no immediate decisions', 'Austria-Hungary and Russia also took decisions that escalated the crisis'],
          context='Fischer\'s work, using German archives, challenged the post-1945 West German consensus that all the powers had slid into war, and it provoked a fierce national controversy.',
          excl=['Primacy of domestic politics']),
        X('a historian writing in the 1970s (illustrative)', 'The roots of German policy in 1914 lay at home. An elite of landowners, industrialists and officers faced the rise of the Social Democrats, the largest party in the Reichstag after 1912. A successful war promised to rally the nation behind the old order and to postpone the reforms it feared.',
          'Primacy of domestic politics', 'Germany\'s rulers risked war to preserve their power against democratic and socialist pressure at home.',
          'The historian examines the structure of German society and politics and explains foreign policy as a product of domestic pressures.', APP1[1],
          ['The SPD won 110 seats in 1912 and became the largest party', 'Weltpolitik and the navy were used to rally support for the government', 'The elite feared reform of the Prussian franchise'],
          ['Other powers faced domestic crises too', 'Decisions in July 1914 were taken by a small group focused on diplomacy and military timing', 'The SPD voted for war credits in August 1914'],
          context='This approach developed in West Germany in the 1960s-70s among social historians influenced by Fischer\'s later work.', excl=['German responsibility (the Fischer thesis)']),
        X('a historian writing in 2000 (illustrative)', 'In July 1914 Berlin held the key. Vienna would not have moved against Serbia without German backing, and the advice from Berlin was to act swiftly and present Europe with a fait accompli. Only when British intervention appeared likely did the chancellor try to restrain Austria, and by then the generals\' timetable had taken over.',
          'German responsibility (the Fischer thesis)', 'Germany bore the main responsibility because its backing and urging turned a Balkan crisis into a European war.',
          'The historian reconstructs the July Crisis day by day, concentrating on the choices made by German leaders.', APP1[2],
          ['Germany urged Austria to act quickly', 'Germany\'s attempt to restrain Vienna came only on 29-30 July', 'The Schlieffen Plan required an immediate attack on France'],
          ['Russia mobilised on 30 July before Germany', 'Austria-Hungary had its own reasons to crush Serbia', 'France gave Russia firm support'], excl=['Primacy of domestic politics']),
    ],
}))

o1b = T('Revisionist and post-revisionist views: shared responsibility and the July Crisis', 'revisionist and post-revisionist', 'shared responsibility', 'july crisis')
build_a2(o1b, dict(WW1, **{
    'claim': 'responsibility for the war was shared among the great powers',
    'stim': ['On 28 June 1914 Archduke Franz Ferdinand was assassinated in Sarajevo.', 'Austria-Hungary sent an ultimatum to Serbia on 23 July 1914.',
             'Russia ordered general mobilisation on 30 July 1914.'],
    'terms': [
        ('July Crisis', 'the diplomatic crisis between the assassination at Sarajevo and the outbreak of war in early August 1914'),
        ('Black Hand', 'the Serbian nationalist secret society linked to the assassination of Franz Ferdinand'),
        ('mobilisation', 'calling up reservists and moving armies to war stations'),
        ('the Sleepwalkers', 'the title of Christopher Clark\'s 2012 study, which argued that leaders blundered into war without fully seeing its consequences'),
        ('revisionism (inter-war)', 'the view, popular in the 1920s and 1930s, that Germany was not solely guilty and that all powers shared responsibility'),
        ('post-revisionism', 'later interpretations that look at decisions in all capitals while accepting that some powers bore more responsibility than others'),
    ],
    'dates': [('Franz Ferdinand was assassinated in Sarajevo', 1914, 6.28), ('Austria-Hungary sent its ultimatum to Serbia', 1914, 7.23), ('Austria-Hungary declared war on Serbia', 1914, 7.28),
              ('Russia ordered general mobilisation', 1914, 7.30), ('Germany declared war on Russia', 1914, 8.01), ('Britain declared war on Germany', 1914, 8.04)],
    'mcq': [
        ('Which British wartime leader later said that the nations "slithered over the brink" into war?', 'Lloyd George', ['Asquith', 'Churchill', 'Grey'], 'In his War Memoirs. [1]'),
        ('Which historian\'s 2012 book described the leaders of 1914 as sleepwalkers?', 'Christopher Clark', ['Fritz Fischer', 'A. J. P. Taylor', 'Gerhard Ritter'], '[1]'),
        ('Why did Britain enter the war on 4 August 1914?', 'Germany invaded Belgium, whose neutrality Britain had guaranteed', ['Austria-Hungary attacked Britain', 'Russia asked Britain to mobilise', 'Germany invaded Britain'], 'Under the Treaty of London of 1839. [1]'),
    ],
    'why': [
        ('historians have increasingly stressed shared responsibility for the war', ['Research in Austrian, Russian, Serbian and French archives revealed their leaders\' choices', 'The end of the Cold War reduced the political weight of the German guilt debate',
                                                                                     'New studies stressed misperception and contingency', 'The Fischer thesis was criticised for reading German aims backwards from 1914'],
         'new archival evidence from other capitals widened the focus beyond Berlin'),
    ],
    'claims': [
        ('Russia ordered general mobilisation before Germany declared war on Russia.', True, 'Russia mobilised on 30 July; Germany declared war on 1 August.'),
        ('Serbia rejected every point of the Austrian ultimatum.', False, 'Serbia accepted most of its terms but rejected Austrian participation in the investigation inside Serbia.'),
        ('Inter-war revisionists argued that Germany alone caused the war.', False, 'They argued that responsibility was shared, against the verdict of Article 231.'),
    ],
    'ess': [
        dict(q='‘Responsibility for the outbreak of war in 1914 was shared among the great powers.’',
             pro=['Austria-Hungary chose war against Serbia', 'Russia\'s early mobilisation escalated the crisis', 'France backed Russia; Serbian nationalists began the crisis'],
             con=['Germany\'s blank cheque encouraged Austria', 'The Schlieffen Plan turned a Balkan war into a world war', 'German leaders accepted war as preferable before Russia grew stronger'],
             judge='responsibility was shared, but not equally: Germany and Austria-Hungary took the decisions that made a European war most likely'),
        dict(q='How far was the July Crisis, rather than long-term causes, responsible for the outbreak of war?',
             pro=['Without Sarajevo there would have been no war in 1914', 'Decisions in July were contingent and could have gone differently', 'Earlier crises had been settled peacefully'],
             con=['Alliances and mobilisation plans made a local crisis general', 'Arms races and imperial rivalry created mistrust', 'Leaders believed war was inevitable'],
             judge='long-term causes made a general war possible, but the decisions of the July Crisis made it happen'),
    ],
    'ext': [
        X('a historian writing in 2012 (illustrative)', 'The crisis of July 1914 was the product of a shared political culture. In every capital, decision-makers acted on partial information, mistrusted their rivals and believed they were acting defensively. Serbian nationalists, Austrian hawks, Russian ministers and French leaders all made choices that narrowed the path to peace. None of them wanted the war that followed, but all helped to bring it about.',
          'Shared responsibility', 'Responsibility was shared among the powers, whose leaders blundered into a war none of them fully intended.',
          'The historian examines decision-making in several capitals during the July Crisis, stressing perceptions and contingency rather than a single plan.', APP1[2],
          ['Austria\'s ultimatum was designed to be rejected', 'Russia\'s general mobilisation on 30 July made war much more likely', 'France gave Russia firm support during Poincaré\'s visit in July'],
          ['Germany\'s blank cheque encouraged Austria', 'German war plans turned a Balkan war into a European one', 'Fischer\'s evidence of German aims'],
          context='Written after the end of the Cold War, when archives in several capitals had been studied, this view moved away from the German-centred debate of the 1960s.'),
        X('a historian writing in the 1980s (illustrative)', 'By 1914 the European states system had become rigid. Two armed blocs faced each other; mobilisation plans left statesmen almost no time to negotiate. Arms races and imperial rivalries had created a climate in which war was widely expected. The assassination at Sarajevo merely lit a fuse that had long been laid.',
          'Structural explanation', 'The war was caused by long-term forces, such as alliances, arms races and military planning, rather than by the decisions of one government.',
          'The historian stresses long-term impersonal forces and the international system rather than individual decisions.', APP1[1],
          ['The Triple Alliance and Triple Entente divided Europe', 'The Anglo-German naval race increased mistrust', 'The Schlieffen Plan required rapid mobilisation and an attack on France'],
          ['Italy stayed neutral in 1914, so alliances were not automatic', 'Earlier crises such as Morocco and Bosnia were settled peacefully', 'Individual decisions in July 1914 were crucial']),
        X('a historian writing in 2013 (illustrative)', 'Austria-Hungary, not Germany, took the first fatal decision. Its leaders, convinced that Serbian nationalism threatened the monarchy\'s survival, resolved on war against Serbia. In St Petersburg the decision to begin military preparations came early, and its significance was concealed from the other powers.',
          'Shared responsibility', 'Austria-Hungary and Russia bore major responsibility, so the war was not mainly Germany\'s doing.',
          'The historian reconstructs decisions in Vienna and St Petersburg, using their archives to shift attention away from Berlin.', APP1[2],
          ['Vienna\'s leaders, such as Conrad, had long wanted war with Serbia', 'Russia began the "Period Preparatory to War" on 26 July', 'Russia mobilised before Germany'],
          ['Austria sought and waited for German backing before acting', 'Germany declared war on Russia and France', 'German plans required invading Belgium']),
    ],
}))

o1c = T("Identifying a historian's approach: structural versus intentionalist and the use of evidence", "identifying a historian's approach", 'structural versus intentionalist', 'use of evidence')
build_a2(o1c, dict(WW1, **{
    'claim': 'the outbreak of war in 1914 is best explained by long-term structural forces',
    'stim': ['Paper 3 asks what you can learn from an extract about the interpretation and approach of the historian who wrote it.', 'Historians\' interpretations depend on the questions they ask and the evidence they select.',
             'A. J. P. Taylor argued in 1969 that the war was imposed on statesmen by railway timetables.'],
    'terms': [
        ('interpretation', 'a historian\'s argument or explanation about the past, based on a selection of evidence'),
        ('approach', 'the way a historian investigates a question, such as the evidence used and the factors emphasised'),
        ('intentionalist approach', 'an approach that explains events through the aims and decisions of individuals'),
        ('structural approach', 'an approach that explains events through long-term impersonal forces and systems'),
        ('sub-message', 'a secondary point in an extract that supports or qualifies the main interpretation'),
        ('provenance', 'information about who produced a piece of writing, when and why'),
    ],
    'dates': [('Sidney Fay published The Origins of the World War, an influential revisionist account', 1928), ('Luigi Albertini\'s detailed study of the July Crisis was published in Italian', 1942),
              ('A. J. P. Taylor published War by Timetable', 1969), ('Christopher Clark published The Sleepwalkers', 2012)],
    'mcq': [
        ('Which of these is the best evidence that an extract uses an intentionalist approach?', 'It quotes private statements of leaders to show what they intended', ['It discusses the growth of railways across Europe', 'It describes the size of the armies in 1914', 'It explains the economic rivalry between the powers'], '[1]'),
        ('In Paper 3, what is meant by the historian\'s approach?', 'How the historian goes about answering the question, including the evidence and factors emphasised', ['The date the extract was written', 'Whether the historian is right or wrong', 'The number of sources the historian lists'], '[1]'),
        ('Which approach would stress mobilisation plans and alliance systems?', 'A structural approach', ['An intentionalist approach', 'A biographical approach', 'A cultural approach'], '[1]'),
    ],
    'why': [
        ('historians reach different interpretations of the origins of the war', ['They use different evidence, such as different national archives', 'They ask different questions, about individuals or about systems', 'They write in different contexts, such as during the Cold War',
                                                                                  'They belong to different schools of thought', 'New evidence becomes available over time'],
         'differences in approach and evidence, shaped by the historian\'s context, explain most differences in interpretation'),
    ],
    'claims': [
        ('A Paper 3 answer should mainly summarise the content of the extract.', False, 'It should explain the interpretation and approach and test them against own knowledge.'),
        ('The same evidence can support different interpretations.', True, 'Historians may interpret documents such as the blank cheque differently.'),
        ('A structural approach focuses mainly on the personalities of leaders.', False, 'That is an intentionalist approach; a structural approach stresses impersonal forces.'),
    ],
    'ess': [
        dict(q='‘The outbreak of war in 1914 is best explained by long-term structural forces.’',
             pro=['Alliances divided Europe into armed blocs', 'Mobilisation plans limited diplomacy', 'Imperial rivalry and arms races created hostility'],
             con=['Individual decisions in Berlin, Vienna and St Petersburg were crucial', 'Earlier crises were resolved', 'Italy\'s neutrality shows alliances were not automatic'],
             judge='structural forces made a general war possible and dangerous, but intentional decisions turned the crisis into war'),
        dict(q='How far do intentionalist and structural approaches to the origins of the war complement each other?',
             pro=['Structures limited the choices leaders felt they had', 'Leaders\' intentions were shaped by structures such as alliances', 'Most modern accounts combine both'],
             con=['They lead to different judgements about responsibility', 'Intentionalists blame particular governments; structuralists blame the system', 'They rely on different kinds of evidence'],
             judge='the approaches are complementary in explaining how war came, but they lead to different judgements on who was responsible'),
    ],
    'ext': [
        X('a historian writing in 1965 (illustrative)', 'The memoranda of the Kaiser\'s ministers reveal a single thread. Again and again they speak of breaking the ring of enemies, of a place in the sun, of the need to strike before Russia grows too strong. These were not idle words; they guided the decisions of July 1914.',
          'German responsibility (the Fischer thesis)', 'German leaders intended to break out of encirclement by war, and these intentions guided their decisions in July 1914.',
          'An intentionalist approach that uses the private statements and documents of German leaders to reveal their intentions.', APP1[0],
          ['Moltke and others argued for war before Russian rearmament was complete', 'Weltpolitik sought a "place in the sun"', 'The blank cheque reflected a willingness to risk war'],
          ['Statements of intent do not prove a plan was followed', 'Other powers\' decisions also mattered', 'Leaders also feared war and tried to restrain Austria late in the crisis'], excl=['Primacy of domestic politics']),
        X('a historian writing in 1969 (illustrative)', 'Once the railway timetables began to roll, nothing could stop them. The generals of every great power had planned for a war of rapid mobilisation, and mobilisation meant war. The statesmen of July 1914 found that the machines they had built had taken the decision out of their hands.',
          'Structural explanation', 'War came because rigid mobilisation plans and railway timetables left statesmen no room to manoeuvre.',
          'A structural approach that explains the war through military planning and technology rather than the aims of individuals.', APP1[1],
          ['The Schlieffen Plan required an attack on France as soon as Russia mobilised', 'Russia could not partially mobilise against Austria alone', 'Railway timetables made mobilisation hard to stop'],
          ['Statesmen chose to mobilise; the plans did not act by themselves', 'The Kaiser briefly considered halting the attack in the west on 1 August', 'Diplomacy continued until the last days']),
        X('a historian writing in the 1960s (illustrative)', 'The war of 1914 was a war for the redivision of the world. Finance capital in Britain, Germany and France had outgrown its national markets; colonies, spheres of investment and sources of raw materials were the stakes. Governments managed this competition, and the workers of every nation were sent to die for it.',
          'Marxist-Leninist interpretation', 'The war resulted from competition between capitalist imperialist powers for markets, investment and colonies.',
          'An economic approach that explains the war through capitalist interests and class, following Lenin\'s theory of imperialism.', APP1[3],
          ['Imperial rivalry in Africa and the Moroccan crises', 'Anglo-German trade competition', 'The Berlin-Baghdad railway alarmed Britain and Russia'],
          ['Britain and Germany were major trading partners and many bankers opposed war', 'The crisis began in the Balkans, not over colonies', 'Imperial disputes such as Fashoda were settled peacefully'],
          context='Marxist interpretations followed Lenin\'s Imperialism (1916) and were the official view in the USSR and East Germany during the Cold War.'),
    ],
}))

CHAPTERS[1] = [o1a, o1b, o1c]


# ============================================================== CHAPTER 2: Historical interpretations, the Holocaust

SCH2 = [('Intentionalist', 'the Holocaust resulted from Hitler\'s long-held ideological intention to destroy the Jews'),
        ('Functionalist (structuralist)', 'the Holocaust emerged through cumulative radicalisation within a chaotic Nazi system, without a single plan'),
        ('Synthesis', 'Hitler\'s ideology set the goal while initiatives and improvisation from below shaped how and when it was carried out'),
        ('Situational explanation of perpetrators', 'ordinary people became killers because of group pressure, conformity and wartime circumstances'),
        ('Eliminationist antisemitism thesis', 'ordinary Germans were willing killers because of a deep-rooted German antisemitism')]
APP2 = ['Focus on Hitler\'s ideology and statements', 'Focus on the structures of the Nazi state and bureaucracy', 'Focus on local initiatives in the occupied territories',
        'Focus on the behaviour and motives of individual perpetrators', 'Focus on collaborators and bystanders across occupied Europe']
HOL = dict(schools=SCH2, approaches=APP2, enq='the Holocaust')
HOL_DATES = [('the Nuremberg Laws were passed', 1935, 9), ('Kristallnacht took place', 1938, 11.09), ('Hitler made his Reichstag "prophecy" about the annihilation of the Jews', 1939, 1.30),
             ('Germany invaded the Soviet Union and Einsatzgruppen killings began', 1941, 6.22), ('gassings began at Chełmno', 1941, 12.08), ('the Wannsee Conference was held', 1942, 1.20)]

h2a = T("Intentionalist interpretations: Hitler's ideology and a long-term plan", 'intentionalist interpretations', "hitler's ideology", 'long-term plan')
build_a2(h2a, dict(HOL, **{
    'claim': 'the Holocaust was the result of Hitler\'s long-term intention',
    'stim': ['In Mein Kampf (1925) Hitler presented the Jews as the enemy of the German people.', 'On 30 January 1939 Hitler told the Reichstag that a new world war would mean "the annihilation of the Jewish race in Europe".',
             'No written order from Hitler for the "Final Solution" has been found.'],
    'terms': [
        ('intentionalism', 'the interpretation that the Holocaust was the result of Hitler\'s ideology and long-term intention'),
        ('Final Solution', 'the Nazi term for the plan to murder all the Jews of Europe'),
        ('Reichstag prophecy', 'Hitler\'s speech of 30 January 1939 threatening the annihilation of the Jews of Europe if there were another world war'),
        ('Führerprinzip', 'the leadership principle, by which the Führer\'s will was the source of all authority'),
        ('Mein Kampf', 'Hitler\'s book of 1925-26 setting out his racial and political ideas'),
        ('racial state', 'the Nazi aim of a society organised by race, excluding those defined as racially inferior'),
    ],
    'dates': HOL_DATES[:4] + [('Mein Kampf was first published', 1925)],
    'mcq': [
        ('Which historian\'s The War Against the Jews (1975) is a leading intentionalist account?', 'Lucy Dawidowicz', ['Hans Mommsen', 'Christopher Browning', 'Raul Hilberg'], '[1]'),
        ('Which piece of evidence do intentionalists most often cite?', 'Hitler\'s Reichstag speech of 30 January 1939', ['Records of local Gauleiters in 1941', 'Interrogations of police reservists', 'Railway timetables for deportations'], '[1]'),
        ('What problem does the lack of a written order from Hitler pose for intentionalists?', 'It makes it harder to prove that Hitler planned and ordered the genocide', ['It proves that Hitler did not know about the killing', 'It shows the Holocaust did not happen', 'It shows Himmler opposed the killing'], '[1]'),
    ],
    'why': [
        ('intentionalist historians stress Hitler\'s role in the Holocaust', ['Hitler\'s antisemitism was consistent from his early writings to his last testament', 'His speeches repeatedly threatened the annihilation of the Jews',
                                                                              'In a dictatorship based on the Führer principle, nothing so large could happen without his approval', 'Himmler and Heydrich acted with his authority'],
         'they see Hitler\'s ideology as the only explanation for a genocide on this scale'),
    ],
    'claims': [
        ('Intentionalists argue that Hitler\'s ideology was the main driving force behind the Holocaust.', True, 'They see a link from his early antisemitism to the death camps.'),
        ('Nazi policy before 1941 aimed mainly at forcing Jews to emigrate.', True, 'Emigration and expulsion, including the Madagascar Plan of 1940, were pursued before mass murder.'),
        ('A signed order from Hitler for the Final Solution was found at Nuremberg.', False, 'No written order from Hitler has been found.'),
    ],
    'ess': [
        dict(q='‘The Holocaust was the result of Hitler\'s long-term intention.’',
             pro=['Hitler\'s antisemitism was central and consistent', 'The 1939 prophecy linked war to the annihilation of the Jews', 'Key escalations, such as the decisions of 1941, required his approval'],
             con=['Policy shifted from emigration to expulsion to murder', 'Local initiatives drove killing in the occupied east', 'Competition between agencies radicalised policy'],
             judge='Hitler\'s ideology set the goal and his approval was essential, but the path to genocide was not a long-planned blueprint'),
        dict(q='How far does the lack of a written order from Hitler weaken the intentionalist interpretation?',
             pro=['It removes direct proof of a plan', 'It fits functionalist evidence of improvised decisions', 'Policy changed in ways a fixed plan would not explain'],
             con=['Hitler often gave oral orders', 'Himmler and others referred to the Führer\'s wishes', 'Speeches show clear murderous intent'],
             judge='the lack of an order weakens claims of a long-term plan, but not the argument that Hitler\'s ideology and approval were essential'),
    ],
    'ext': [
        X('a historian writing in the 1970s (illustrative)', 'From the pages of Mein Kampf to the bunker in Berlin, Hitler\'s hatred of the Jews was the one constant of his career. The Final Solution was not an accident of war or a product of rivalry between officials. It was the fulfilment of a purpose that Hitler had announced openly, and which he pursued step by step as circumstances allowed.',
          'Intentionalist', 'The Holocaust was the result of Hitler\'s long-held intention to destroy the Jews, carried out step by step as circumstances allowed.',
          'The historian focuses on Hitler\'s ideology and statements, tracing a straight line from his early writings to genocide.', APP2[0],
          ['Mein Kampf expressed extreme antisemitism', 'The Reichstag prophecy of January 1939 threatened annihilation', 'Hitler approved key escalations of persecution'],
          ['Policy before 1941 aimed at emigration and expulsion, as with the Madagascar Plan', 'No written order from Hitler has been found', 'The timing of mass murder was shaped by the invasion of the USSR'],
          context='Intentionalist accounts of the 1970s stressed Hitler\'s central role, partly in reaction to structural interpretations that seemed to some to reduce his responsibility.', excl=['Synthesis']),
        X('a historian writing in the 1980s (illustrative)', 'The absence of a signed order proves nothing. Hitler preferred to give his most terrible commands orally, through Himmler and Heydrich. His speeches repeat the prophecy of annihilation, and every step towards the death camps carried his authority.',
          'Intentionalist', 'Hitler ordered the Holocaust orally and every step towards genocide carried his authority.',
          'The historian uses Hitler\'s speeches and the testimony of subordinates to argue that his intention lay behind each step, explaining away the lack of a written order.', APP2[0],
          ['Himmler and Heydrich acted with Hitler\'s authority', 'Hitler repeated his prophecy publicly', 'Himmler\'s Posen speeches of October 1943 spoke openly of extermination'],
          ['Local officials improvised killing before central decisions', 'Hitler may have approved initiatives rather than planned them', 'The Wannsee Conference was about coordination, suggesting policy was still evolving'], excl=['Synthesis']),
        X('a historian writing in the 1990s (illustrative)', 'Hitler did not need a blueprint. His world view defined the Jews as the enemy who must disappear from Europe; the method and the moment were all that remained open. The war against the Soviet Union, conceived from the start as a war of annihilation, provided both.',
          'Intentionalist', 'Hitler\'s ideology made the destruction of the Jews his goal, and the war against the USSR provided the means and the moment.',
          'The historian focuses on Hitler\'s ideology but links its realisation to the circumstances of the war in the east.', APP2[0],
          ['The war in the east was planned as a racial war', 'Einsatzgruppen began killing Jews immediately after the invasion', 'Hitler\'s ideology linked Jews and Bolshevism'],
          ['Killing escalated in stages, from men to women and children', 'Decisions about Western European Jews came later, in autumn 1941', 'Functionalists stress the role of local officials'], excl=['Synthesis']),
    ],
}))

h2b = T('Functionalist and structuralist interpretations: cumulative radicalisation and the role of the bureaucracy', 'functionalist and structuralist', 'cumulative radicalisation', 'bureaucracy')
build_a2(h2b, dict(HOL, **{
    'claim': 'the Holocaust was the result of cumulative radicalisation within the Nazi system',
    'stim': ['From 1939 Nazi plans to expel Jews from the Reich to occupied Poland repeatedly broke down.', 'In 1940 Nazi officials considered deporting European Jews to the island of Madagascar.',
             'The Wannsee Conference of January 1942 coordinated the work of different ministries and agencies.'],
    'terms': [
        ('functionalism', 'the interpretation that the Holocaust emerged from the way the Nazi system worked rather than from a plan'),
        ('cumulative radicalisation', 'Hans Mommsen\'s term for the process by which competing agencies drove policy to ever more extreme measures'),
        ('polycracy', 'the description of the Nazi state as many competing centres of power rather than an ordered hierarchy'),
        ('working towards the Führer', 'Ian Kershaw\'s phrase for officials anticipating Hitler\'s wishes and competing to fulfil them'),
        ('Madagascar Plan', 'the Nazi plan of 1940 to deport European Jews to Madagascar, abandoned when Britain was not defeated'),
        ('Einsatzgruppen', 'SS mobile killing units that followed the German army into the Soviet Union in 1941'),
    ],
    'dates': HOL_DATES[1:] + [('the Madagascar Plan was proposed', 1940, 6)],
    'mcq': [
        ('Which historian is most associated with the idea of cumulative radicalisation?', 'Hans Mommsen', ['Lucy Dawidowicz', 'Daniel Goldhagen', 'Gerald Fleming'], '[1]'),
        ('Which evidence do functionalists use to show that there was no early plan for genocide?', 'The repeated changes of policy from emigration to expulsion to murder', ['Hitler\'s 1939 Reichstag speech', 'The text of Mein Kampf', 'Himmler\'s Posen speech of 1943'], '[1]'),
        ('Where did the first systematic gassings of Jews take place, from December 1941?', 'Chełmno', ['Dachau', 'Buchenwald', 'Theresienstadt'], 'In the Warthegau, annexed to the Reich. [1]'),
    ],
    'why': [
        ('functionalist historians argue that the Holocaust was not planned in advance', ['Policy changed several times, from emigration to expulsion to murder', 'Rival agencies competed to solve the "Jewish question"', 'Local officials in the east began killing on their own initiative',
                                                                                         'The failure of expulsion plans such as Madagascar created pressure for a "solution"', 'No written order from Hitler exists'],
         'the improvised and changing nature of policy suggests a process of radicalisation rather than a plan'),
    ],
    'claims': [
        ('Functionalists deny that Hitler was antisemitic.', False, 'They accept his antisemitism but argue that it did not amount to a plan for genocide.'),
        ('The Madagascar Plan was abandoned partly because Britain controlled the seas.', True, 'Without defeating Britain, deportation by sea was impossible.'),
        ('The Wannsee Conference coordinated the work of different agencies in carrying out the Final Solution.', True, 'Heydrich chaired it in January 1942.'),
    ],
    'ess': [
        dict(q='‘The Holocaust was the result of cumulative radicalisation within the Nazi system.’',
             pro=['Policy shifted as earlier solutions failed', 'Rival agencies competed to show zeal', 'Local initiatives in the occupied east escalated killing'],
             con=['Hitler\'s ideology defined the Jews as the enemy', 'Hitler\'s approval was needed for key decisions', 'The radicalisation always moved in one direction, set by ideology'],
             judge='cumulative radicalisation explains how the Holocaust developed, but not why its target was the Jews, which requires Hitler\'s ideology'),
        dict(q='How far did the war against the Soviet Union transform Nazi policy towards the Jews?',
             pro=['Einsatzgruppen began mass shootings in 1941', 'Millions of Jews came under German control', 'The war of annihilation removed restraints'],
             con=['Persecution had grown steadily since 1933', 'Ghettos in Poland already caused mass deaths', 'Ideology made Jews the target before the war'],
             judge='the war against the USSR was the decisive turning point from persecution to genocide, but it radicalised an existing ideological aim'),
    ],
    'ext': [
        X('a historian writing in the 1970s (illustrative)', 'The Third Reich was not a monolith but a jungle of competing agencies. Gauleiters, the SS, the ministries and the occupation authorities each pursued their own answer to a "Jewish question" that the regime had defined but never solved. When expulsion proved impossible, the deportations jammed and the ghettos overflowed, officials improvised the solution of murder.',
          'Functionalist (structuralist)', 'The Holocaust emerged through cumulative radicalisation within a chaotic, competitive system rather than from a plan.',
          'The historian focuses on the structures of the Nazi state and how decisions were made, rather than on Hitler\'s ideas.', APP2[1],
          ['Rival agencies competed for power', 'Expulsion plans such as Madagascar failed', 'Local officials began gassings at Chełmno in December 1941'],
          ['Hitler\'s statements and prophecy show intent', 'Himmler reported to Hitler and acted with his authority', 'Antisemitic ideology was central from 1933'],
          context='West German historians such as Martin Broszat and Hans Mommsen developed this view in the 1970s using the records of the Nazi administration.'),
        X('a historian writing in 1999 (illustrative)', 'In the occupied east in the summer of 1941 the killing spread from Jewish men of military age to women and children. The decisive steps were often taken by commanders on the spot, competing to show their zeal and reporting their "successes" to Berlin. Policy was made as much in the occupied cities of the east as in the Reich Chancellery.',
          'Functionalist (structuralist)', 'Radicalisation came from initiatives in the occupied territories as much as from orders from the centre.',
          'The historian focuses on local initiatives in the occupied territories, using regional records.', APP2[2],
          ['Einsatzgruppen reports show competition in numbers killed', 'Killing of women and children spread from late July and August 1941', 'Babi Yar, September 1941, was organised locally with the army'],
          ['Himmler toured the east and encouraged escalation', 'The killing was consistent with Hitler\'s ideological war', 'Central decisions were needed for deportations from the Reich']),
        X('a historian writing in 1998 (illustrative)', 'Officials across the Reich worked towards the Führer: they anticipated what Hitler wanted and competed to deliver it. Hitler set the ideological direction and gave his approval at crucial moments; the initiatives and the radicalism came from below. Neither intention nor structure alone explains the Holocaust.',
          'Synthesis', 'Hitler\'s ideology and approval were essential, but cumulative radicalisation by officials working towards his wishes drove the process.',
          'The historian combines analysis of Hitler\'s role with the structures of the regime, explaining how his authority worked through the system.', APP2[1],
          ['Hitler\'s approval was sought for deportations from the Reich in autumn 1941', 'Officials competed to fulfil his wishes', 'Ideological goals were clear but methods were improvised'],
          ['Intentionalists argue Hitler planned more directly', 'Goldhagen stressed ordinary Germans\' motives', 'Some decisions may have come entirely from the centre']),
    ],
}))

h2c = T("Synthesis and 'ordinary men' debates: perpetrators, collaborators and bystanders", 'synthesis', 'ordinary men', 'perpetrators, collaborators and bystanders')
build_a2(h2c, dict(HOL, **{
    'claim': 'ordinary perpetrators killed mainly because of situational pressures rather than ideology',
    'stim': ['Reserve Police Battalion 101, made up mainly of middle-aged men from Hamburg, took part in the murder of tens of thousands of Jews in Poland in 1942-43.', 'At Babi Yar near Kiev, more than 33,000 Jews were shot on 29-30 September 1941.',
             'Local police in many occupied countries helped to round up Jews for deportation.'],
    'terms': [
        ('perpetrators', 'those who took part directly in persecution and killing'),
        ('collaborators', 'non-Germans in occupied or allied countries who assisted the Nazi persecution'),
        ('bystanders', 'those who knew of persecution but did not take part or intervene'),
        ('Ordinary Men', 'Christopher Browning\'s 1992 study of Reserve Police Battalion 101'),
        ('Hitler\'s Willing Executioners', 'Daniel Goldhagen\'s 1996 book arguing that eliminationist antisemitism motivated ordinary Germans'),
        ('Józefów', 'the Polish village where Reserve Police Battalion 101 shot about 1,500 Jews in July 1942'),
    ],
    'dates': [('Reserve Police Battalion 101 carried out the massacre at Józefów', 1942, 7.13), ('the Babi Yar massacre took place', 1941, 9.29), ('Christopher Browning published Ordinary Men', 1992),
              ('Daniel Goldhagen published Hitler\'s Willing Executioners', 1996), ('Raul Hilberg published Perpetrators, Victims, Bystanders', 1992)],
    'mcq': [
        ('What did Major Trapp offer his men before the massacre at Józefów?', 'The chance to step out and not take part', ['Extra pay for each killing', 'Promotion to the SS', 'Exemption from service in Russia if they refused'], 'Only about a dozen stepped out at first. [1]'),
        ('Which historian argued that a German "eliminationist antisemitism" motivated the killers?', 'Daniel Goldhagen', ['Christopher Browning', 'Ian Kershaw', 'Hans Mommsen'], '[1]'),
        ('What kind of evidence did Browning mainly use in Ordinary Men?', 'Post-war judicial interrogations of members of the battalion', ['Hitler\'s speeches', 'Soviet archives', 'Diaries of Jewish victims only'], '[1]'),
    ],
    'why': [
        ('ordinary men became killers', ['Conformity and unwillingness to break ranks with comrades', 'Obedience to authority and fear of appearing weak', 'Antisemitic propaganda dehumanised victims', 'Brutalisation by war and the division of labour in killing', 'Careerism and opportunism'],
         'situational pressures explain why most took part, though ideology shaped how they saw their victims'),
    ],
    'claims': [
        ('Men who refused to take part in shootings in Reserve Police Battalion 101 were executed.', False, 'No one was punished severely for refusing; this shows the men had some choice.'),
        ('Collaborators in occupied countries took part in the Holocaust.', True, 'For example, local police in France and auxiliary units in the Baltic states and Ukraine.'),
        ('Browning and Goldhagen studied some of the same police battalion evidence but reached different conclusions.', True, 'Both drew on Reserve Police Battalion 101.'),
    ],
    'ess': [
        dict(q='‘Ordinary perpetrators of the Holocaust killed mainly because of situational pressures rather than ideology.’',
             pro=['Few stepped out when given the chance at Józefów', 'Conformity and peer pressure were powerful', 'Many perpetrators were not Nazi activists'],
             con=['Antisemitic propaganda shaped attitudes', 'Some killed with enthusiasm beyond orders', 'Non-Germans also killed, suggesting varied motives including ideology and opportunism'],
             judge='situational pressures explain why most ordinary men took part, but ideology defined who the victims were and made killing acceptable'),
        dict(q='How far does the study of collaborators and bystanders change our understanding of the Holocaust?',
             pro=['It shows the Holocaust depended on participation across Europe', 'It reveals the role of indifference and opportunism', 'It moves the focus beyond Hitler and the SS'],
             con=['The decisions and machinery of murder were German', 'Collaborators acted within a system created by the Nazis', 'Intentionalist and functionalist debates remain central to explaining decisions'],
             judge='it widens our understanding of how the Holocaust was carried out, but not of why it was decided upon'),
    ],
    'ext': [
        X('a historian writing in 1992 (illustrative)', 'The men of the battalion were middle-aged reservists from a German city, not committed Nazis. When offered the chance to step out before their first massacre, only a handful did. Most killed because they did not want to break ranks, to appear weak, or to leave the dirty work to their comrades.',
          'Situational explanation of perpetrators', 'Ordinary men became killers mainly because of conformity, peer pressure and wartime circumstances rather than ideology.',
          'The historian focuses on the behaviour and motives of individual perpetrators, using post-war interrogations.', APP2[3],
          ['At Józefów few men stepped out when offered the chance', 'Most members of the battalion were not party activists', 'Psychological studies of obedience support the importance of conformity'],
          ['Antisemitic propaganda shaped attitudes', 'Some men refused without punishment, so there was choice', 'Goldhagen argued antisemitism was the main motive'],
          context='This reflects the approach of Christopher Browning\'s Ordinary Men (1992), which used the interrogations of members of Reserve Police Battalion 101.'),
        X('a historian writing in 1996 (illustrative)', 'The perpetrators were willing. They killed with zeal, photographed their deeds and sent the pictures home. Such conduct cannot be explained by obedience or peer pressure. It sprang from a conviction, long rooted in German culture, that the Jews were a dangerous enemy who deserved to be eliminated.',
          'Eliminationist antisemitism thesis', 'Ordinary Germans were willing executioners motivated by a long-standing eliminationist antisemitism.',
          'The historian focuses on perpetrators\' behaviour and explains it through national political culture.', APP2[3],
          ['Cruelty went beyond orders, as on the death marches of 1945', 'Antisemitism was widespread', 'Few refused even when they could'],
          ['Many non-Germans also took part', 'Antisemitism existed across Europe', 'Situational explanations account for behaviour without a uniquely German culture'],
          context='This reflects Daniel Goldhagen\'s Hitler\'s Willing Executioners (1996), which was popular with the public but widely criticised by historians.'),
        X('a historian writing in 2001 (illustrative)', 'The murder of Europe\'s Jews required the participation of many beyond the SS: railway clerks who scheduled the trains, local police who made the arrests, neighbours who took over empty flats. Most were neither fanatics nor sadists. Their indifference, opportunism and fear made the killing possible.',
          'Situational explanation of perpetrators', 'The Holocaust depended on the participation and indifference of many collaborators and bystanders, not just committed Nazis.',
          'The historian looks at collaborators and bystanders across Europe, not just the leadership.', APP2[4],
          ['The Reichsbahn organised deportation trains', 'French police carried out the Vel d\'Hiv round-up of July 1942', 'Property of deported Jews was taken over by neighbours'],
          ['The decisions were taken by the Nazi leadership', 'Some bystanders and rescuers helped Jews, as in Denmark in 1943', 'Ideology drove the core perpetrators']),
    ],
}))

h2d = T('Assessing an extract: context, approach and how far the evidence supports the interpretation', 'assessing an extract', 'context, approach')
build_a2(h2d, dict(HOL, **{
    'claim': 'Hitler\'s role was the decisive factor in the Holocaust',
    'stim': ['Historians\' interpretations of the Holocaust have changed as new evidence has become available, including Eastern European archives after 1991.', 'In Paper 3, own knowledge is used to test the interpretation in the extract.',
             'Interpretations of the Holocaust have been shaped by the politics of the Cold War and of post-war Germany.'],
    'terms': [
        ('context of the historian', 'the time, place and circumstances in which a historian wrote, which may shape their questions and conclusions'),
        ('testing an interpretation', 'using own knowledge to judge how far the evidence supports or challenges a historian\'s argument'),
        ('main interpretation', 'the overall argument of an extract, as opposed to its sub-messages'),
        ('historiography', 'the study of how historians have interpreted the past and how interpretations have changed'),
        ('selection of evidence', 'the choice of which evidence to use and emphasise, which shapes an interpretation'),
    ],
    'dates': [('the Nuremberg trials of major war criminals began', 1945, 11), ('the Eichmann trial took place in Jerusalem', 1961), ('Raul Hilberg published The Destruction of the European Jews', 1961), ('the Soviet Union collapsed, opening many Eastern European archives', 1991)],
    'mcq': [
        ('What should a strong Paper 3 answer do with own knowledge?', 'Use it to test the interpretation in the extract', ['Replace the extract with a narrative of events', 'Ignore it and focus only on the wording', 'Use it to describe the historian\'s life'], '[1]'),
        ('Why did the opening of Eastern European archives after 1991 matter to Holocaust historians?', 'It gave access to records of killing in the occupied east', ['It proved that Hitler signed an order in 1939', 'It showed that the Holocaust began in 1945', 'It closed the debate between schools'], '[1]'),
        ('Which of these is a sub-message rather than a main interpretation?', 'Local officials sometimes competed to report higher numbers of victims', ['The Holocaust was the product of Hitler\'s intention', 'The Holocaust emerged from cumulative radicalisation', 'Ordinary Germans were willing executioners'], '[1]'),
    ],
    'why': [
        ('interpretations of the Holocaust have changed over time', ['New evidence, such as Eastern European archives, became available', 'Historians asked new questions, about perpetrators and bystanders', 'The political context of the Cold War and of German memory changed', 'Debates between schools refined arguments'],
         'new evidence and new questions, shaped by changing contexts, explain the development of the debate'),
    ],
    'claims': [
        ('The context in which a historian writes can help explain their interpretation.', True, 'For example, intentionalist emphasis on Hitler partly responded to arguments that seemed to diminish his responsibility.'),
        ('A good Paper 3 answer explains the interpretation and tests it with own knowledge.', True, 'Paraphrasing the extract only reaches the lower levels.'),
        ('A historian\'s approach is the same thing as their conclusion.', False, 'The approach is how they investigate; the interpretation is what they conclude.'),
    ],
    'ess': [
        dict(q='‘Hitler\'s role was the decisive factor in the Holocaust.’',
             pro=['His ideology defined the Jews as the enemy', 'His approval was needed for key decisions', 'His prophecy and speeches set the direction'],
             con=['Rival agencies radicalised policy', 'Local initiatives drove killing', 'Ordinary perpetrators, collaborators and bystanders made it possible'],
             judge='Hitler\'s role was necessary but not sufficient: the Holocaust required a system and many participants to carry it out'),
        dict(q='How far has the debate between intentionalists and functionalists been resolved by a synthesis?',
             pro=['Most historians now combine ideology and structure', 'Kershaw\'s "working towards the Führer" links both', 'Research on 1941 decisions shows central and local roles'],
             con=['Debates continue over when and how decisions were taken', 'The perpetrator debate raised new questions', 'Historians still weight Hitler\'s role differently'],
             judge='a synthesis has largely replaced the old polarised debate, but disagreements over timing and emphasis remain'),
    ],
    'ext': [
        X('a historian writing in the 1980s (illustrative)', 'To ask whether Hitler planned the Holocaust is to ask the wrong question. The regime set itself an impossible aim, a Germany "free of Jews", and every failure to achieve it by deportation increased the pressure for more radical measures. The bureaucracy did not need orders; it needed only a goal.',
          'Functionalist (structuralist)', 'The Holocaust resulted from the regime\'s attempt to achieve an impossible goal, with failure driving radicalisation.',
          'The historian focuses on how the bureaucracy worked and how failure produced radicalisation, rather than on Hitler\'s decisions.', APP2[1],
          ['Deportation plans repeatedly failed', 'Rival agencies sought radical solutions', 'Ghettos created crises officials tried to solve'],
          ['Hitler\'s statements show intent', 'Key decisions in 1941 involved Hitler', 'Ideology defined the goal'],
          context='Written during the intense intentionalist-functionalist debate, before Eastern European archives opened.'),
        X('a historian writing in 2004 (illustrative)', 'The new evidence from the archives of the east shows decisions taken in stages in the second half of 1941, each approved by Hitler and each more radical than the last. Hitler was not the author of every initiative, but nothing of significance happened without him.',
          'Synthesis', 'The Holocaust was decided in stages in 1941, with Hitler approving each radical step though not originating every initiative.',
          'The historian uses newly available archives to reconstruct the timing of decisions and the interaction of Hitler and his subordinates.', APP2[1],
          ['Mass shootings escalated in summer 1941', 'Deportations from the Reich were approved in autumn 1941', 'Death camps were built from late 1941'],
          ['Intentionalists see a plan earlier', 'Functionalists stress local initiatives more', 'The exact date of a decision remains disputed'],
          context='Written after Eastern European archives opened in the 1990s, allowing detailed study of decisions in 1941.'),
        X('a historian writing in the 1970s (illustrative)', 'Antisemitism was not one of many Nazi ideas; it was the core of Hitler\'s world view. Everything else, the war for living space, the struggle with Bolshevism, was bound up with it. To understand the Holocaust, one must take Hitler at his word.',
          'Intentionalist', 'Antisemitism was the core of Hitler\'s world view, so the Holocaust follows from taking his words seriously.',
          'The historian focuses on Hitler\'s ideology, treating his statements as reliable guides to his intentions.', APP2[0],
          ['Hitler linked Jews and Bolshevism', 'His speeches threatened annihilation', 'The war in the east was a racial war'],
          ['Hitler\'s statements were also propaganda', 'Policy changed significantly over time', 'Local initiatives drove much of the killing'], excl=['Synthesis']),
    ],
}))

CHAPTERS[2] = [h2a, h2b, h2c, h2d]


# ============================================================== CHAPTER 3: Historical interpretations, the origins and development of the Cold War, 1941-50

SCH3 = [('Orthodox', 'Soviet expansionism and communist ideology caused the Cold War; the USA responded defensively'),
        ('Revisionist', 'US economic expansion and atomic diplomacy caused the Cold War; the USSR acted defensively'),
        ('Post-revisionist', 'both superpowers contributed through mutual misperception and security fears'),
        ('Post-Cold War', 'evidence from Soviet archives shows that Stalin\'s ideology and personality were central')]
APP3 = ['Focus on Soviet ideology and actions in Eastern Europe', 'Focus on US economic interests and policy', 'Focus on mutual perceptions and security fears', 'Use of newly opened Soviet archives']
CW = dict(schools=SCH3, approaches=APP3, enq='the origins of the Cold War')
CW_DATES = [('the Yalta Conference was held', 1945, 2), ('the Potsdam Conference was held', 1945, 7), ('Kennan sent the Long Telegram', 1946, 2.22), ('Churchill gave his "Iron Curtain" speech at Fulton', 1946, 3.05),
            ('the Truman Doctrine was announced', 1947, 3.12), ('Marshall announced his plan for European recovery', 1947, 6.05), ('the communists took power in Czechoslovakia', 1948, 2), ('the Berlin Blockade began', 1948, 6.24),
            ('NATO was founded', 1949, 4), ('the USSR tested its first atomic bomb', 1949, 8)]

w3a = T("Orthodox interpretations: Soviet expansionism and Stalin's responsibility", 'orthodox interpretations', 'soviet expansionism', "stalin's responsibility")
build_a2(w3a, dict(CW, **{
    'claim': 'Stalin was mainly responsible for the Cold War',
    'stim': ['At Yalta in February 1945 the Allies signed a Declaration on Liberated Europe promising free elections.', 'In February 1946 George Kennan sent the "Long Telegram" from Moscow.',
             'In February 1948 the communists seized power in Czechoslovakia.'],
    'terms': [
        ('orthodox interpretation', 'the view, dominant in the West in the 1940s and 1950s, that Soviet expansionism caused the Cold War'),
        ('containment', 'the US policy of preventing the spread of communism, outlined by Kennan'),
        ('Declaration on Liberated Europe', 'the Yalta agreement of 1945 promising free elections in liberated countries'),
        ('salami tactics', 'the gradual removal of non-communist parties in Eastern Europe, slice by slice'),
        ('Long Telegram', 'Kennan\'s message of February 1946 arguing that Soviet hostility was rooted in ideology and insecurity and must be contained'),
        ('Cominform', 'the organisation set up by Stalin in 1947 to coordinate communist parties'),
    ],
    'dates': CW_DATES[:7],
    'mcq': [
        ('Which historian\'s work is a classic orthodox account of the origins of the Cold War?', 'Herbert Feis', ['William Appleman Williams', 'Gar Alperovitz', 'Gabriel Kolko'], '[1]'),
        ('Which event do orthodox historians use as evidence that Stalin broke the Yalta agreements?', 'The failure to hold free elections in Poland', ['The Marshall Plan', 'The dropping of the atomic bomb', 'The formation of NATO'], '[1]'),
        ('When were orthodox interpretations most dominant in the USA?', 'The late 1940s and 1950s', ['The 1960s and 1970s', 'The 1990s', 'The 1920s'], '[1]'),
    ],
    'why': [
        ('orthodox historians blamed the Soviet Union for the Cold War', ['Soviet control of Eastern Europe broke the promises of Yalta', 'Communist ideology taught that conflict with capitalism was inevitable', 'Events such as the Czech coup and the Berlin Blockade looked like aggression',
                                                                        'Many wrote during the Cold War and shared the assumptions of US policymakers', 'They had access mainly to Western sources'],
         'Soviet actions in Eastern Europe, interpreted through the climate of the early Cold War, made Soviet responsibility seem obvious'),
    ],
    'claims': [
        ('Orthodox historians argued that US policy was a defensive response to Soviet expansion.', True, 'They saw containment as a reaction to Soviet actions.'),
        ('Free elections were held throughout Eastern Europe in 1945-47 as agreed at Yalta.', False, 'Communists used pressure and fraud, as in the Polish election of 1947.'),
        ('Orthodox accounts were written with full access to Soviet archives.', False, 'Soviet archives were closed until the 1990s.'),
    ],
    'ess': [
        dict(q='‘Stalin was mainly responsible for the Cold War.’',
             pro=['Soviet control of Eastern Europe broke Yalta promises', 'The Czech coup and Berlin Blockade appeared aggressive', 'Post-Cold War archives show Stalin\'s ideological hostility'],
             con=['The USA used atomic diplomacy and economic pressure', 'The Truman Doctrine exaggerated the Soviet threat', 'Stalin\'s aims were largely defensive after huge wartime losses'],
             judge='Stalin bears the larger share, as his actions in Eastern Europe destroyed trust, but US policy also deepened the division'),
        dict(q='How far was the Cold War caused by the Soviet takeover of Eastern Europe?',
             pro=['It broke the Declaration on Liberated Europe', 'It created the Iron Curtain', 'It persuaded the USA to adopt containment'],
             con=['The Western allies had accepted Soviet influence in the percentages agreement', 'Disputes over Germany and reparations mattered as much', 'Ideological rivalry predated 1945'],
             judge='the takeover of Eastern Europe was the central issue that turned wartime tension into Cold War'),
    ],
    'ext': [
        X('a historian writing in the 1950s (illustrative)', 'Within months of Yalta, the Soviet Union had broken its promise of free elections in Poland and was installing obedient communist governments across Eastern Europe. Stalin\'s ideology taught him that conflict with the capitalist world was inevitable, and he expanded wherever he met no resistance. The Truman Doctrine and the Marshall Plan were the West\'s belated response.',
          'Orthodox', 'Soviet expansionism, driven by Stalin and communist ideology, caused the Cold War, and the USA responded defensively.',
          'The historian focuses on Soviet ideology and actions in Eastern Europe, judging the USSR by its breaches of wartime agreements.', APP3[0],
          ['Yalta promised free elections, which were not held in Poland', 'Communist takeovers, as in Czechoslovakia in 1948', 'The Berlin Blockade of 1948-49'],
          ['The USSR lost about 27 million people and sought security', 'The 1944 percentages agreement accepted Soviet influence in Romania and Bulgaria', 'Stalin gave little help to Greek communists and withdrew from Iran in 1946'],
          context='Orthodox accounts were written in the USA in the late 1940s and 1950s, during the early Cold War and McCarthyism, often by historians close to government.'),
        X('a historian writing in the 1960s (illustrative)', 'In February 1946 Stalin told Soviet voters that war was inevitable while capitalism survived. Two weeks later Kennan explained to Washington that Soviet power was impervious to reason but sensitive to force. American policy thereafter was a response to a threat that Moscow had chosen to make.',
          'Orthodox', 'The Cold War was a response to a Soviet threat deliberately created by Stalin\'s hostility to the West.',
          'The historian uses statements by Soviet and American leaders to show that the USA reacted to Soviet hostility.', APP3[0],
          ['Stalin\'s election speech of February 1946', 'Kennan\'s Long Telegram', 'Soviet pressure on Turkey and Iran in 1946'],
          ['Speeches were for domestic audiences', 'US policy also had economic motives', 'Western statements, such as Churchill\'s Iron Curtain speech, also raised tension']),
        X('a historian writing in the 1950s (illustrative)', 'The blockade of Berlin was the moment when even the most hopeful saw the truth. Stalin sought to drive the Western powers out of the city and to bend Germany to his will. Only the airlift and the formation of NATO showed him that the West would not retreat.',
          'Orthodox', 'Stalin\'s aggression, shown by the Berlin Blockade, forced the West to organise its defence.',
          'The historian focuses on Soviet actions in Germany and Eastern Europe and presents Western policy as reactive.', APP3[0],
          ['The blockade began in June 1948', 'The airlift supplied West Berlin until May 1949', 'NATO was formed in April 1949'],
          ['The blockade followed Western currency reform in their zones', 'The West was creating a West German state', 'Stalin may have aimed to stop West German formation, not to seize Berlin']),
    ],
}))

w3b = T('Revisionist interpretations: US economic imperialism and atomic diplomacy', 'revisionist interpretations', 'economic imperialism', 'atomic diplomacy')
build_a2(w3b, dict(CW, **{
    'claim': 'US policy was the main cause of the Cold War',
    'stim': ['In 1959 William Appleman Williams published The Tragedy of American Diplomacy.', 'The first atomic bomb was dropped on Hiroshima on 6 August 1945.',
             'The Marshall Plan provided about 13 billion dollars of aid to Western Europe from 1948.'],
    'terms': [
        ('revisionist interpretation', 'the view, developed from the late 1950s, that US policy was largely responsible for the Cold War'),
        ('Open Door', 'the US aim of an open world economy in which American goods and capital could move freely'),
        ('atomic diplomacy', 'the use of the US monopoly of the atomic bomb to put pressure on the USSR'),
        ('dollar imperialism', 'the Soviet description of the Marshall Plan as a means of US economic domination'),
        ('Molotov Plan', 'the Soviet programme of trade agreements with Eastern Europe in 1947, a response to Marshall Aid'),
        ('Novikov telegram', 'the Soviet ambassador\'s report of September 1946 claiming the USA sought world supremacy'),
    ],
    'dates': CW_DATES[1:6] + [('the atomic bomb was dropped on Hiroshima', 1945, 8.06)],
    'mcq': [
        ('Which historian argued that atomic diplomacy shaped US policy in 1945?', 'Gar Alperovitz', ['John Lewis Gaddis', 'Herbert Feis', 'Arthur Schlesinger'], 'Atomic Diplomacy (1965). [1]'),
        ('Why did revisionism grow in the USA in the 1960s?', 'The Vietnam War led many to question US foreign policy', ['Soviet archives opened', 'The Cold War ended', 'The USA left NATO'], '[1]'),
        ('Why did the USSR reject Marshall Aid?', 'It saw it as a means of extending US economic and political influence', ['It had no need of aid', 'The USA refused to offer it', 'It was only for Asia'], '[1]'),
    ],
    'why': [
        ('revisionist historians blamed the USA for the Cold War', ['US leaders sought an open world economy that threatened Soviet control', 'The atomic bomb was used partly to intimidate the USSR', 'The Truman Doctrine exaggerated the Soviet threat to win support in Congress',
                                                                    'The Marshall Plan divided Europe economically', 'The Vietnam War encouraged scepticism of US motives'],
         'they saw US economic expansion as the driving force, a view encouraged by the context of the Vietnam War'),
    ],
    'claims': [
        ('Revisionists argued that the USSR acted mainly defensively after 1945.', True, 'They stressed Soviet wartime losses and security needs.'),
        ('The first US atomic test took place the day before the Potsdam Conference opened.', True, 'The Trinity test was on 16 July 1945; Potsdam opened on 17 July. Revisionists argue Truman timed the conference with this in mind.'),
        ('The USSR accepted Marshall Aid for Poland and Czechoslovakia.', False, 'Stalin forced them to refuse it.'),
    ],
    'ess': [
        dict(q='‘US policy was the main cause of the Cold War.’',
             pro=['Atomic diplomacy and the end of Lend-Lease alarmed Stalin', 'The Truman Doctrine divided the world into two camps', 'The Marshall Plan and currency reform divided Europe and Germany'],
             con=['Soviet actions in Eastern Europe came first', 'Stalin\'s ideology and suspicion made cooperation difficult', 'US policy was largely a response to perceived Soviet threats'],
             judge='US policy contributed to the division, but it was more a response to Soviet actions than their cause'),
        dict(q='How far was the Marshall Plan an act of economic imperialism?',
             pro=['It opened European markets to US goods', 'It tied recipients to US economic policy', 'It aimed to prevent communist parties winning in Western Europe'],
             con=['It was offered to all of Europe, including the USSR', 'It helped European recovery and was welcomed', 'European governments shaped how aid was used'],
             judge='it served US economic and political interests, but it was also a genuine recovery programme that Europeans welcomed'),
    ],
    'ext': [
        X('a historian writing in the late 1950s (illustrative)', 'American leaders believed that the prosperity of the United States depended on an open world economy. The Open Door, not the Iron Curtain, was the starting point of their policy. The Marshall Plan offered aid on terms that would tie Europe to American markets, and Moscow could hardly be expected to accept them.',
          'Revisionist', 'US economic expansion and the pursuit of an open world economy caused the Cold War.',
          'The historian focuses on US economic interests and policy, treating Soviet actions as responses.', APP3[1],
          ['The USA sought free trade through Bretton Woods', 'Marshall Aid required economic openness', 'Soviet rejection of the plan followed from its terms'],
          ['Soviet control of Eastern Europe preceded the Marshall Plan', 'The Plan was offered to the USSR', 'Stalin\'s ideology was hostile regardless of US economics'],
          context='Revisionism developed in the USA from the late 1950s, influenced by W. A. Williams, and grew during the Vietnam War, when many questioned US foreign policy.'),
        X('a historian writing in 1965 (illustrative)', 'The bombs dropped on Hiroshima and Nagasaki were aimed as much at Moscow as at Tokyo. The President delayed the meeting at Potsdam until the atomic test had succeeded, and his advisers believed the bomb would make the Russians more manageable in Europe. Atomic diplomacy convinced Stalin that the West meant to deny him security.',
          'Revisionist', 'The USA used atomic diplomacy to pressure the USSR, which convinced Stalin of Western hostility.',
          'The historian focuses on US policy and decision-making, especially the use of the atomic bomb.', APP3[1],
          ['Potsdam began the day after the Trinity test', 'Byrnes believed the bomb would strengthen the US hand', 'The US monopoly lasted until 1949'],
          ['The bomb was used mainly to end the war quickly and save US lives', 'Soviet actions in Poland came before the bomb', 'Stalin already knew of the project through spies']),
        X('a historian writing in the 1970s (illustrative)', 'In March 1947 the President told Congress that the world faced a choice between two ways of life. The danger in Greece and Turkey did not justify such language; it was chosen to frighten a reluctant Congress into paying. The Truman Doctrine turned a local crisis into a global crusade.',
          'Revisionist', 'The Truman Doctrine deliberately exaggerated the Soviet threat, turning local crises into a global confrontation.',
          'The historian examines US policymaking and the domestic political motives behind US rhetoric.', APP3[1],
          ['Britain\'s withdrawal from Greece created the immediate need for aid', 'Senator Vandenberg reportedly advised Truman to "scare the hell out of" the American people', 'Stalin gave little help to the Greek communists'],
          ['Soviet pressure on Turkey over the Straits was real', 'Communist expansion in Eastern Europe made fears plausible', 'Europe was economically vulnerable to communist parties']),
    ],
}))

w3c = T('Post-revisionist interpretations and the impact of Soviet archives', 'post-revisionist interpretations', 'soviet archives')
build_a2(w3c, dict(CW, **{
    'claim': 'both superpowers were responsible for the Cold War',
    'stim': ['In 1972 John Lewis Gaddis published The United States and the Origins of the Cold War, 1941-1947.', 'After 1991 many Soviet and Eastern European archives became available to historians.',
             'In 1997 Gaddis published We Now Know: Rethinking Cold War History.'],
    'terms': [
        ('post-revisionism', 'the interpretation, from the 1970s, that both superpowers contributed to the Cold War through mutual misperception'),
        ('security dilemma', 'a situation in which one state\'s defensive measures make another feel less secure'),
        ('misperception', 'misunderstanding of the motives and actions of another state'),
        ('revolutionary-imperial paradigm', 'the idea that Soviet policy combined communist ideology with traditional Russian imperial aims'),
        ('preponderance of power', 'Melvyn Leffler\'s description of the US aim of keeping a dominant position in world affairs for its security'),
        ('new Cold War history', 'research since the 1990s using archives from the former communist states'),
    ],
    'dates': CW_DATES[3:] + [('the Soviet Union collapsed', 1991, 12)],
    'mcq': [
        ('Which historian is most associated with post-revisionism?', 'John Lewis Gaddis', ['William Appleman Williams', 'Herbert Feis', 'Gabriel Kolko'], 'His 1972 work; his later We Now Know (1997) moved closer to an orthodox view. [1]'),
        ('What new evidence became available to Cold War historians after 1991?', 'Soviet and Eastern European archives', ['The Long Telegram', 'The Truman Doctrine speech', 'US newspapers of the 1940s'], '[1]'),
        ('Which historian argued that the USA sought a "preponderance of power"?', 'Melvyn Leffler', ['Lucy Dawidowicz', 'Gar Alperovitz', 'Herbert Feis'], 'A Preponderance of Power (1992). [1]'),
    ],
    'why': [
        ('post-revisionist interpretations emerged in the 1970s', ['Newly released US government records gave a fuller picture of decision-making', 'Historians sought a middle ground after the polarised orthodox-revisionist debate', 'Détente encouraged a less partisan view',
                                                                   'Research showed both sides acted from security fears'],
         'new US evidence and the less tense climate of détente encouraged a more balanced view'),
    ],
    'claims': [
        ('Post-revisionists argued that both sides contributed to the Cold War.', True, 'They stressed mutual misperception and security fears.'),
        ('Soviet archives were fully open to historians in the 1950s.', False, 'They became partly accessible only after 1991.'),
        ('Gaddis\'s later work put more weight on Stalin\'s responsibility.', True, 'We Now Know (1997) argued that Stalin\'s personality and ideology made the Cold War likely.'),
    ],
    'ess': [
        dict(q='‘Both superpowers were equally responsible for the Cold War.’',
             pro=['Each misread the other\'s defensive moves as aggressive', 'US atomic diplomacy and Soviet control of Eastern Europe both raised tension', 'Ideological rivalry made trust impossible on both sides'],
             con=['Soviet archives suggest Stalin\'s ideology and suspicion were central', 'Soviet takeovers came before most US measures', 'US actions were largely reactions'],
             judge='both contributed, but responsibility was not equal: Stalin\'s actions did most to create the Cold War'),
        dict(q='How far has the opening of Soviet archives changed interpretations of the origins of the Cold War?',
             pro=['It revealed Stalin\'s ideological outlook and suspicion', 'It showed Soviet direction of Eastern European communists', 'It led Gaddis and others to put more weight on Stalin'],
             con=['Much remains closed or fragmentary', 'It confirmed Soviet security fears stressed by revisionists', 'US evidence and economic factors remain important'],
             judge='the archives shifted the balance towards Stalin\'s responsibility, but they did not end the debate'),
    ],
    'ext': [
        X('a historian writing in 1972 (illustrative)', 'Neither side sought a Cold War. Each acted to secure itself, and each read the other\'s defensive moves as offensive. American leaders, constrained by Congress and public opinion, oversold the Soviet threat; Stalin\'s search for a security belt in Eastern Europe looked like expansion from Washington.',
          'Post-revisionist', 'Both superpowers contributed to the Cold War through mutual misperception and the pursuit of security.',
          'The historian focuses on mutual perceptions and security fears, using US government records.', APP3[2],
          ['Soviet security concerns after invasion in 1941', 'US domestic politics shaped rhetoric such as the Truman Doctrine', 'Each side misread the other\'s actions'],
          ['Soviet archives later showed ideological hostility', 'Soviet takeovers went beyond security needs', 'Some US actions were driven by economic interest'],
          context='Post-revisionism emerged in the 1970s, drawing on newly released US records and seeking a middle ground after the Vietnam-era debate.'),
        X('a historian writing in 1997 (illustrative)', 'The opening of the Soviet archives has changed the debate. They show a Stalin who saw the world through the lens of Marxist-Leninist ideology, who distrusted even his allies, and who probed for advantage wherever he could. As long as Stalin ruled, a Cold War was probably unavoidable.',
          'Post-Cold War', 'Evidence from the Soviet archives shows that Stalin\'s ideology and personality made the Cold War unavoidable.',
          'The historian uses newly opened Soviet archives to reassess Stalin\'s aims.', APP3[3],
          ['Archives show Stalin\'s suspicion of the West', 'Soviet direction of Eastern European communist parties', 'Stalin approved the Berlin Blockade and later the Korean War'],
          ['The archives also show Soviet security fears', 'Some archives remain closed', 'US policy also contributed'],
          context='Written after the collapse of the USSR in 1991, when Soviet and Eastern European archives became partly accessible.'),
        X('a historian writing in 1992 (illustrative)', 'American officials did not expect a Soviet attack. What they feared was that the USSR might gain control of the industrial and human resources of Europe and Asia through economic collapse and local communist parties. To prevent this, they sought a preponderance of power, a defensive aim pursued by expansive means.',
          'Post-revisionist', 'The USA pursued a preponderance of power for defensive reasons, which helped to create the Cold War.',
          'The historian examines US national security policy and how officials perceived threats.', APP3[2],
          ['US officials did not expect an immediate Soviet attack', 'The Marshall Plan aimed to stabilise Western Europe', 'NATO and West Germany strengthened the Western position'],
          ['Soviet actions gave real grounds for fear', 'Post-Cold War evidence emphasises Stalin\'s aims', 'Revisionists see economic motives as more aggressive']),
    ],
}))

CHAPTERS[3] = [w3a, w3b, w3c]


# ============================================================== CHAPTER 4: European history 1919-41, Mussolini's Italy

m4a = T('The rise of Fascism and the March on Rome, 1919-22', 'rise of fascism', 'march on rome')
build_a2(m4a, {
    'enq': 'the rise of Fascism', 'claim': 'Mussolini came to power mainly because of the weakness of the Liberal state',
    'stim': ['The Fasci di Combattimento were founded in Milan in March 1919.', 'In 1919-20, the "two red years", strikes and factory occupations spread across northern Italy.',
             'On 28 October 1922 Fascist squads converged on Rome; King Victor Emmanuel III refused to declare martial law.'],
    'terms': [
        ('mutilated victory', 'the nationalist claim that Italy had been cheated of its rightful gains at the peace conference of 1919'),
        ('biennio rosso', 'the "two red years" of 1919-20, marked by strikes, land seizures and factory occupations'),
        ('squadristi', 'armed Fascist squads that attacked socialists, trade unions and peasant leagues'),
        ('trasformismo', 'the Liberal practice of building governments through deals between individual deputies rather than parties'),
        ('ras', 'local Fascist bosses who led the squads in the provinces'),
        ('Fiume', 'the Adriatic port seized by the nationalist poet D\'Annunzio in September 1919'),
    ],
    'dates': [('the Fasci di Combattimento were founded in Milan', 1919, 3), ('D\'Annunzio seized Fiume', 1919, 9), ('workers occupied factories in northern Italy', 1920, 9),
              ('the National Fascist Party (PNF) was founded', 1921, 11), ('the March on Rome took place', 1922, 10)],
    'mcq': [
        ('How many Fascist deputies were elected in May 1921 as part of Giolitti\'s National Bloc?', '35', ['135', '3', '275'], '[1]'),
        ('Why did Victor Emmanuel III refuse to declare martial law in October 1922?', 'He doubted the army\'s loyalty and feared civil war', ['The army had already joined the Fascists', 'Parliament ordered him not to', 'Mussolini had already been elected prime minister'], '[1]'),
        ('Which group gave most support to Fascist squads in the Po valley in 1920-21?', 'Landowners alarmed by socialist peasant leagues', ['Industrial workers', 'The Catholic Popolari', 'Southern sharecroppers'], '[1]'),
    ],
    'why': [
        ('Mussolini became prime minister in October 1922', ['The Liberal governments were weak and unstable', 'Fear of socialism after the biennio rosso won support from landowners, industrialists and the middle class', 'Fascist violence destroyed socialist organisations while the police looked on',
                                                            'Mussolini combined violence with negotiation and appeared respectable', 'The king and elites chose to bring him into government rather than resist'],
         'Mussolini came to power because the elites, fearing socialism and lacking confidence in Liberal government, chose to appoint him'),
    ],
    'claims': [
        ('Mussolini seized power by defeating the army in Rome.', False, 'The king invited him to form a government; the army was never ordered to resist.'),
        ('Italy gained Fiume at the Paris peace conference.', False, 'Fiume was not awarded to Italy, which fed the idea of a mutilated victory.'),
        ('Fascist squads attacked socialist and trade union offices in 1920-22.', True, 'Squad violence was concentrated in the north and centre.'),
    ],
    'ess': [
        dict(q='‘Mussolini came to power mainly because of the weakness of the Liberal state.’',
             pro=['Governments were short-lived coalitions', 'Liberals failed to deal with post-war economic problems and unrest', 'Liberal leaders tried to absorb Fascism, as in the 1921 National Bloc'],
             con=['Fear of socialism drove elites to support Fascism', 'Fascist violence and organisation', 'Mussolini\'s political skill and the king\'s decision in October 1922'],
             judge='the weakness of the Liberal state created the opportunity, but Mussolini came to power because elites afraid of socialism turned to him'),
        dict(q='How far was the March on Rome a bluff?',
             pro=['The squads were poorly armed and could have been dispersed by the army', 'Mussolini stayed in Milan, near the Swiss border', 'Power came by royal invitation'],
             con=['The threat of violence was real and had been demonstrated', 'Fascists had seized control of many northern towns', 'It persuaded the king that resistance risked civil war'],
             judge='the march was a bluff militarily, but the threat it represented was real enough to persuade the king to give way'),
    ],
    'src': [
        S('a report by a prefect in the Po valley, 1921 (illustrative)', 'The Fascist squads move by lorry from town to town, burning the offices of the leagues. The carabinieri watch and do nothing; the landowners pay for the petrol.',
          'Fascist violence', 'It suggests that squads acted with the support of landowners and the tolerance of the authorities.',
          'To report to the government on disorder in the province.', 'prefects had direct knowledge of local conditions', 'a prefect may have exaggerated to explain his failure to keep order',
          'It does not show the role of Mussolini or the national government.', stance=True, why='it shows the state failing to uphold the law'),
        S('a speech by Mussolini, Naples, 24 October 1922 (summary)', 'Mussolini told the Fascist congress that either the government would be given to the Fascists or they would take it by marching on Rome.',
          'Mussolini\'s strategy in 1922', 'It shows Mussolini threatening force to gain power.',
          'To mobilise Fascists and pressure the government.', 'it is Mussolini\'s own public statement days before the march', 'it was intended to intimidate and may not reflect his real plans',
          'It does not show the king\'s reasons for giving way.', stance=False, why='it suggests Fascist threats and Mussolini\'s strategy, not just Liberal weakness'),
    ],
})

m4b = T('Consolidation of power and the Fascist dictatorship, 1922-29', 'consolidation of power', 'fascist dictatorship')
build_a2(m4b, {
    'enq': 'the consolidation of Fascist power', 'claim': 'the Matteotti crisis was the turning point in the creation of the Fascist dictatorship',
    'stim': ['The Acerbo Law of 1923 gave two-thirds of the seats in parliament to the party winning the most votes, provided it had at least 25 per cent.', 'The socialist deputy Giacomo Matteotti was murdered by Fascists in June 1924.',
             'The Lateran Agreements were signed with the papacy in February 1929.'],
    'terms': [
        ('Acerbo Law', 'the electoral law of 1923 giving two-thirds of seats to the list with most votes if it won at least 25 per cent'),
        ('Aventine Secession', 'the walk-out of opposition deputies from parliament after the murder of Matteotti in 1924'),
        ('leggi fascistissime', 'the "most Fascist laws" of 1925-26 that banned opposition parties and controlled the press'),
        ('OVRA', 'the Fascist secret police, set up in 1927'),
        ('Lateran Agreements', 'the treaties of 1929 that recognised the Vatican City as a sovereign state and made Catholicism the state religion'),
        ('Grand Council of Fascism', 'the Fascist party body that became an organ of state in 1928'),
    ],
    'dates': [('the Acerbo Law was passed', 1923, 7), ('the Fascist-led list won about two-thirds of the vote in the general election', 1924, 4), ('Matteotti was murdered', 1924, 6),
              ('Mussolini accepted responsibility for Fascist violence in a speech to parliament', 1925, 1.03), ('the OVRA secret police was set up', 1927), ('the Lateran Agreements were signed', 1929, 2)],
    'mcq': [
        ('Why did the Aventine Secession fail to bring down Mussolini?', 'The king refused to dismiss him and the opposition had no other way to act', ['Mussolini resigned', 'The army arrested the opposition deputies', 'The pope supported the opposition'], '[1]'),
        ('What did the Lateran Agreements give the Church?', 'Sovereignty over the Vatican City and compensation for lost territory', ['Control of the Italian army', 'The right to appoint ministers', 'Ownership of all schools'], '[1]'),
        ('What was the effect of the Acerbo Law in 1924?', 'It gave the government list a large majority of seats', ['It banned all political parties', 'It gave women the vote', 'It abolished the monarchy'], '[1]'),
    ],
    'why': [
        ('Mussolini survived the Matteotti crisis of 1924', ['The king refused to dismiss him', 'The opposition withdrew from parliament rather than acting', 'Elites still saw him as a barrier to socialism', 'Fascist radicals pressured Mussolini to act decisively, leading to his speech of January 1925'],
         'he survived because the king and the elites would not abandon him and the opposition had no means of forcing him out'),
        ('the Lateran Agreements were important to Mussolini', ['They ended the conflict between the Church and the Italian state since 1870', 'They won Catholic support for the regime', 'They increased his international prestige', 'They removed a possible centre of opposition'],
         'they gave the regime a legitimacy that no other policy achieved'),
    ],
    'claims': [
        ('Mussolini became a dictator immediately in October 1922.', False, 'He led a coalition government and built the dictatorship gradually up to 1926.'),
        ('Opposition parties were banned in 1926.', True, 'This was part of the leggi fascistissime.'),
        ('The monarchy was abolished under Mussolini.', False, 'The king remained head of state and dismissed Mussolini in July 1943.'),
    ],
    'ess': [
        dict(q='‘The Matteotti crisis was the turning point in the creation of the Fascist dictatorship.’',
             pro=['It led to the speech of January 1925 and the move to open dictatorship', 'The opposition\'s failure removed the last parliamentary challenge', 'It was followed by the leggi fascistissime'],
             con=['The Acerbo Law and the 1924 election had already given Fascists control of parliament', 'The dictatorship was built gradually through 1926-28', 'The support of the king and elites was the decisive factor throughout'],
             judge='the Matteotti crisis was the turning point because Mussolini\'s survival showed that no one would stop him, but it accelerated a process already under way'),
        dict(q='To what extent was Fascist Italy a totalitarian state by 1929?',
             pro=['Opposition parties and free trade unions were banned', 'The press was controlled and OVRA watched dissent', 'Parliament became a rubber stamp'],
             con=['The king, the Church and the army kept independent power', 'Mussolini relied on deals with elites', 'Repression was milder than in Nazi Germany or the USSR'],
             judge='Italy was a personal dictatorship by 1929 but not fully totalitarian, because traditional institutions retained power'),
    ],
    'src': [
        S('Mussolini, speech to the Chamber of Deputies, 3 January 1925 (translated, abridged)', 'I declare that I, and I alone, assume the political, moral and historical responsibility for all that has happened.',
          'Mussolini\'s response to the Matteotti crisis', 'Mussolini openly accepts responsibility for Fascist actions and challenges his opponents.',
          'To end the crisis by asserting his authority and preparing open dictatorship.', 'it is Mussolini\'s own words at the turning point', 'it is a political performance designed to intimidate',
          'It does not show the role of the king or the opposition.', stance=True, why='it marks the move from coalition government to dictatorship after the crisis'),
        S('a letter from a Liberal politician, 1924 (illustrative)', 'We have left the chamber in protest, but the king will not act and the industrialists still prefer Mussolini to disorder. We have made ourselves powerless.',
          'the Aventine Secession', 'It suggests the opposition lacked power because the king and elites backed Mussolini.',
          'To express frustration privately.', 'it shows the view of an opposition politician at the time', 'it is a private view, perhaps written in despair',
          'It does not show what happened next.', stance=False, why='it suggests the support of elites, not the crisis itself, was decisive'),
    ],
})

m4c = T('Fascist economic and social policies, including youth, women and the Church', 'fascist economic and social policies', 'youth, women and the church')
build_a2(m4c, {
    'enq': 'Fascist economic and social policies', 'claim': 'Fascist economic policies were a failure',
    'stim': ['In 1925 Mussolini launched the Battle for Grain.', 'In 1927 the lira was revalued at 90 to the pound (Quota 90).',
             'The Opera Nazionale Balilla was set up in 1926 to organise young Italians.',
             'In 1927 Mussolini launched the Battle for Births to raise the birth rate.'],
    'terms': [
        ('Battle for Grain', 'the campaign from 1925 to make Italy self-sufficient in wheat'),
        ('Quota 90', 'the revaluation of the lira in 1927 at 90 to the pound, for prestige'),
        ('corporate state', 'the Fascist system of organising employers and workers in corporations under state control'),
        ('IRI', 'the Institute for Industrial Reconstruction, set up in 1933 to rescue failing banks and industries'),
        ('Dopolavoro', 'the Fascist leisure organisation for workers, set up in 1925'),
        ('Battle for Births', 'the campaign from 1927 to raise Italy\'s birth rate'),
        ('autarky', 'the policy of economic self-sufficiency pursued especially after the sanctions of 1935-36'),
    ],
    'dates': [('the Battle for Grain was launched', 1925), ('the Opera Nazionale Balilla was set up', 1926), ('the Charter of Labour was issued', 1927),
              ('the IRI was set up', 1933), ('anti-Jewish racial laws were introduced', 1938), ('the Chamber of Fasces and Corporations replaced the Chamber of Deputies', 1939)],
    'mcq': [
        ('What was the main cost of the Battle for Grain?', 'Land was switched from more valuable crops and exports such as olives and fruit', ['Italy became dependent on imported wheat', 'Grain output fell sharply', 'Farmers were all forced into collectives'], 'Wheat output rose, but at the expense of other farming. [1]'),
        ('Why did the Quota 90 revaluation harm Italian industry?', 'It made Italian exports more expensive', ['It made imports more expensive', 'It caused hyperinflation', 'It ended all foreign trade'], '[1]'),
        ('Which youth organisation replaced the ONB in 1937?', 'The Gioventù Italiana del Littorio (GIL)', ['The Hitler Youth', 'Catholic Action', 'The Dopolavoro'], '[1]'),
    ],
    'why': [
        ('the Battle for Births failed', ['Economic hardship discouraged large families', 'Urbanisation and women\'s employment reduced birth rates', 'Incentives such as tax breaks were small', 'Many Italians ignored propaganda in private life'],
         'propaganda could not overcome economic and social trends that pushed birth rates down'),
        ('Mussolini sought good relations with the Church', ['Most Italians were Catholic, so Church support strengthened the regime', 'It removed a rival source of loyalty', 'It increased his international prestige', 'Both opposed communism'],
         'Church support was the cheapest way of winning legitimacy among ordinary Italians'),
    ],
    'claims': [
        ('Wheat production rose during the Battle for Grain.', True, 'Output rose, though at the cost of other crops and efficiency.'),
        ('The corporate state gave workers real control over their industries.', False, 'Employers kept far more influence; workers\' independent unions had been banned.'),
        ('The birth rate rose steadily under Fascism.', False, 'It continued to fall despite the Battle for Births.'),
    ],
    'ess': [
        dict(q='‘Fascist economic policies were a failure.’',
             pro=['Quota 90 harmed exports and caused deflation', 'The Battle for Grain distorted agriculture', 'Living standards and real wages fell for many workers', 'Autarky failed to prepare Italy for war'],
             con=['Public works, such as draining the Pontine Marshes, were completed', 'The IRI saved banks and industries in the Depression', 'Wheat output and some heavy industry grew'],
             judge='Fascist economic policy achieved some propaganda successes and rescued industry in the Depression, but it failed to modernise the economy or prepare Italy for war'),
        dict(q='How successful was the Fascist regime in winning the support of young people?',
             pro=['The ONB and GIL enrolled millions', 'Schools taught Fascist values and the cult of the Duce', 'University Fascist groups attracted ambitious students'],
             con=['Membership was often for careers or sport rather than belief', 'Catholic Action remained a rival', 'Many young people became disillusioned, especially in the war'],
             judge='the regime reached most young people but won the genuine loyalty of fewer, as shown by the collapse of support during the war'),
    ],
    'src': [
        S('a Fascist propaganda poster for the Battle for Grain, 1920s (description)', 'The poster shows Mussolini, stripped to the waist, threshing wheat beside peasant farmers under a bright sun.',
          'the Battle for Grain', 'It presents Mussolini as a man of the people leading a successful national campaign.',
          'To win support for the Battle for Grain and build the cult of the Duce.', 'it shows how the regime wanted to be seen', 'it is propaganda and tells us nothing about real results',
          'It does not show the effect on other crops.', stance=False, why='it presents economic policy as a success'),
        S('a report by a British diplomat in Rome, 1932 (illustrative)', 'Wages have been cut repeatedly and the high lira has hit the export trades. The regime speaks of corporations, but in practice the employers decide.',
          'living standards and the corporate state', 'It suggests that workers lost out and the corporate state favoured employers.',
          'To report on conditions in Italy to London.', 'diplomats were well informed and not subject to Fascist censorship', 'a foreign observer might lack contact with ordinary Italians',
          'It does not mention public works or the IRI.', stance=True, why='it shows economic policy harming workers and exports'),
    ],
})

m4d = T('Italian foreign policy, 1922-41', 'italian foreign policy', 'foreign policy, 1922-41')
build_a2(m4d, {
    'enq': 'Italian foreign policy', 'claim': 'Mussolini\'s foreign policy was driven mainly by a desire for prestige',
    'stim': ['In 1923 Mussolini bombarded and occupied Corfu.', 'In October 1935 Italy invaded Abyssinia.', 'Italy declared war on Britain and France on 10 June 1940.'],
    'terms': [
        ('Rome-Berlin Axis', 'the alignment between Italy and Germany announced by Mussolini in November 1936'),
        ('Stresa Front', 'the agreement of April 1935 between Italy, Britain and France to oppose German breaches of the treaties'),
        ('Pact of Steel', 'the military alliance between Italy and Germany signed in May 1939'),
        ('non-belligerence', 'Italy\'s position from September 1939 to June 1940, supporting Germany without fighting'),
        ('spazio vitale', 'the Fascist idea of "living space" in the Mediterranean and Africa'),
        ('Corfu incident', 'Mussolini\'s occupation of the Greek island in 1923 after the murder of an Italian general'),
    ],
    'dates': [('Italy occupied Corfu', 1923, 8), ('Italy invaded Abyssinia', 1935, 10), ('Mussolini announced the Rome-Berlin Axis', 1936, 11),
              ('Italy invaded Albania', 1939, 4), ('Italy signed the Pact of Steel', 1939, 5), ('Italy declared war on Britain and France', 1940, 6.10), ('Italy invaded Greece', 1940, 10)],
    'mcq': [
        ('Why did Mussolini move troops to the Brenner Pass in July 1934?', 'To deter a Nazi takeover of Austria after the murder of Dollfuss', ['To invade Germany', 'To support the Anschluss', 'To prepare for the invasion of Abyssinia'], '[1]'),
        ('Which civil war did Italy intervene in from 1936?', 'The Spanish Civil War', ['The Russian Civil War', 'The Greek Civil War', 'The Chinese Civil War'], 'Italy sent tens of thousands of troops to support Franco. [1]'),
        ('What happened to the Italian invasion of Greece in 1940?', 'It was driven back, and Germany had to intervene in 1941', ['Greece surrendered within a week', 'Britain joined Italy', 'It was cancelled before it began'], '[1]'),
    ],
    'why': [
        ('Mussolini invaded Abyssinia in 1935', ['To avenge the defeat at Adwa in 1896', 'To win prestige and distract from economic problems', 'To build an empire in Africa', 'He believed Britain and France would not stop him after Stresa'],
         'prestige and empire were the main motives, and he acted because he judged Britain and France would not resist'),
        ('Italy moved closer to Germany after 1935', ['Britain and France imposed sanctions over Abyssinia', 'Germany supported Italy over Abyssinia', 'Both intervened for Franco in Spain', 'Mussolini admired German strength and saw the chance to gain from it'],
         'the Abyssinian crisis broke Italy from Britain and France and pushed Mussolini towards Hitler'),
    ],
    'claims': [
        ('Italy entered the Second World War in September 1939.', False, 'It declared non-belligerence and entered the war only in June 1940.'),
        ('The Abyssinian war led to League sanctions against Italy.', True, 'Sanctions were imposed in 1935 but excluded oil.'),
        ('Mussolini opposed German annexation of Austria in 1934.', True, 'He sent troops to the Brenner Pass.'),
    ],
    'ess': [
        dict(q='‘Mussolini\'s foreign policy was driven mainly by a desire for prestige.’',
             pro=['Corfu, Abyssinia and Albania were showy, opportunistic actions', 'Propaganda presented foreign policy as national greatness', 'He joined the war in 1940 to share in victory'],
             con=['He pursued consistent aims of Mediterranean and African expansion', 'He sought security, as at the Brenner in 1934 and Stresa', 'Ideology drew him to Germany and against communism in Spain'],
             judge='prestige was a constant motive, but it served a consistent goal of making Italy the dominant Mediterranean power'),
        dict(q='How far was Mussolini\'s foreign policy successful before 1940?',
             pro=['Abyssinia was conquered', 'Albania was annexed', 'He was a key figure at Munich in 1938'],
             con=['Abyssinia led to sanctions and dependence on Germany', 'Spain drained resources', 'Italy became the junior partner of Germany'],
             judge='he won territory and prestige, but at the cost of independence, leaving Italy tied to Germany and unprepared for war'),
    ],
    'src': [
        S('a speech by Mussolini, October 1935 (summary)', 'Announcing the war against Abyssinia, Mussolini told Italians that their country had been denied its place in the sun and that its patience was at an end.',
          'motives for the Abyssinian war', 'It presents the war as a matter of national honour and status.',
          'To rally Italians behind the war.', 'it is Mussolini\'s own justification at the time', 'it is propaganda that may hide other motives',
          'It does not show the economic or strategic calculations.', stance=True, why='it stresses national prestige and status'),
        S('a memorandum by an Italian diplomat, 1939 (illustrative)', 'The Duce speaks of the Mediterranean as our sea, but the army lacks guns and the factories cannot supply them. An alliance with Germany ties us to a war we cannot fight.',
          'Italy\'s position in 1939', 'It suggests Mussolini had ambitious aims but Italy was not ready for war.',
          'To warn against the German alliance.', 'it shows the view of an insider', 'a diplomat opposed to the alliance may exaggerate weakness',
          'It does not show Mussolini\'s own reasoning.', stance=False, why='it suggests consistent expansionist aims rather than prestige alone'),
    ],
})

CHAPTERS[4] = [m4a, m4b, m4c, m4d]


# ---------------------------------------------------------------- data-response helper

def _pct(a, b):
    # exact decimal arithmetic, rounding halves away from zero (as a calculator would)
    from decimal import Decimal, ROUND_HALF_UP
    a, b = Decimal(str(a)), Decimal(str(b))
    q = ((b - a) / a * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(q)


def data_item(t, name, intro, table, unit, what, C=('C3',), D=(2, 3, 4, 5), notes=''):
    """table: [(label, value)] in time order. Builds calculate / describe-and-explain items from a data table."""
    def fn(r, D_):
        k = min(len(table), r.choice([3, 4, 5]) if D_ >= 3 else 3)
        i0 = r.randrange(0, len(table) - k + 1)
        rows = table[i0:i0 + k]
        (l1, v1), (l2, v2) = rows[0], rows[-1]
        tab = '; '.join(f'{l}: {v:,}{unit}' if isinstance(v, int) else f'{l}: {v}{unit}' for l, v in rows)
        p = _pct(v1, v2)
        ch = 'increase' if p >= 0 else 'decrease'
        if D_ <= 2:
            return {'stem': f'{intro} {tab}. Calculate the percentage {ch} in {what} between {l1} and {l2}. Give your answer to the nearest whole number.',
                    'answer': f'{abs(p)}%', 'key': f'({v2} - {v1}) / {v1} × 100 = {p}%: 1 mark for method, 1 mark for the answer [2]', 'type': 'numerical', 'marks': 2, 'minutes': 2.5}
        m = 6 if D_ <= 3 else 8
        return {'stem': f'{intro} {tab}. (a) Calculate the percentage {ch} in {what} between {l1} and {l2}, to the nearest whole number. [2] '
                        f'(b) {r.choice(["Explain what the data suggest about", "Using the data and your own knowledge, assess"])} {notes or what}. [{m - 2}]',
                'answer': f'(a) {abs(p)}% {ch}. (b) The figures show the trend from {l1} to {l2}; an answer should link this to own knowledge and note the limits of the statistics (source, reliability, what they do not measure).',
                'key': f'(a) ({v2} - {v1}) / {v1} × 100 = {p}%: 1 mark method, 1 mark answer [2] (b) 1 mark for describing the trend with figures; up to {m - 4} marks for explaining it with own knowledge; 1 mark for a comment on the reliability or limits of the data [{m - 2}]',
                'type': 'numerical', 'marks': m, 'minutes': _mins(m)}
    fn.__name__ = name
    for c in C:
        t.add(c, D, 'numerical')(fn)


# ============================================================== CHAPTER 5: European history 1919-41, Stalin's USSR

s5a = T("Stalin's rise to power, 1924-29", "stalin's rise to power")
build_a2(s5a, {
    'enq': 'Stalin\'s rise to power', 'claim': 'Stalin rose to power mainly because of his position as General Secretary',
    'stim': ['Lenin died in January 1924.', 'Stalin became General Secretary of the Communist Party in April 1922.', 'Trotsky was expelled from the Soviet Union in 1929.'],
    'terms': [
        ('General Secretary', 'the post Stalin held from 1922, which controlled appointments within the party'),
        ('Lenin\'s Testament', 'Lenin\'s notes of 1922-23 criticising the leading Bolsheviks and recommending Stalin\'s removal as General Secretary'),
        ('Socialism in One Country', 'Stalin\'s policy of building socialism in the USSR without waiting for world revolution'),
        ('Permanent Revolution', 'Trotsky\'s idea that the revolution must be spread abroad to survive'),
        ('Lenin Enrolment', 'the mass recruitment of new party members after Lenin\'s death, many of whom owed their position to Stalin'),
        ('nomenklatura', 'the system of lists of approved people for key posts, controlled by the party Secretariat'),
    ],
    'dates': [('Stalin became General Secretary', 1922, 4), ('Lenin died', 1924, 1), ('Trotsky lost his post as Commissar for War', 1925, 1),
              ('Trotsky was expelled from the Communist Party', 1927, 11), ('Bukharin and the Right were defeated', 1929), ('Trotsky was expelled from the USSR', 1929, 1)],
    'mcq': [
        ('Who were Stalin\'s allies against Trotsky in 1923-25?', 'Zinoviev and Kamenev', ['Bukharin and Rykov', 'Molotov and Beria', 'Tukhachevsky and Kirov'], 'The triumvirate. [1]'),
        ('Why was Lenin\'s Testament not published in 1924?', 'The party leaders agreed to suppress it', ['Lenin destroyed it', 'Trotsky lost it', 'It was written after Stalin took power'], '[1]'),
        ('Which policy did Bukharin and the Right defend in 1928?', 'Continuing the NEP', ['Rapid collectivisation', 'Permanent Revolution', 'War Communism'], '[1]'),
    ],
    'why': [
        ('Stalin emerged as leader by 1929', ['As General Secretary he controlled appointments and built a loyal following', 'His rivals underestimated him', 'He shifted alliances, first with the Left against Trotsky, then with the Right against the Left',
                                              'Socialism in One Country appealed to party members', 'Trotsky was arrogant and isolated and failed to use Lenin\'s Testament', 'He presented himself as Lenin\'s loyal disciple'],
         'his control of the party machine was decisive, combined with tactical skill and his rivals\' mistakes'),
    ],
    'claims': [
        ('Lenin\'s Testament recommended that Stalin be removed as General Secretary.', True, 'A postscript of January 1923 called him "too rude".'),
        ('Trotsky allied with Stalin against Zinoviev and Kamenev in 1923-25.', False, 'Zinoviev and Kamenev allied with Stalin against Trotsky.'),
        ('Stalin was elected leader by a vote of the Soviet people.', False, 'He rose through control of the party machine.'),
    ],
    'ess': [
        dict(q='‘Stalin rose to power mainly because of his position as General Secretary.’',
             pro=['He controlled appointments and promotions', 'The Lenin Enrolment brought in members loyal to him', 'He controlled party congresses through delegates'],
             con=['His rivals\' mistakes, especially Trotsky\'s', 'His shifting alliances and tactical skill', 'Socialism in One Country appealed to a war-weary party'],
             judge='the General Secretaryship gave Stalin the means, but his tactical skill and his rivals\' errors explain how he used it to win'),
        dict(q='How far was Trotsky responsible for his own defeat?',
             pro=['He was arrogant and alienated colleagues', 'He failed to attend Lenin\'s funeral', 'He did not use Lenin\'s Testament against Stalin'],
             con=['Stalin controlled the party machine', 'Others feared Trotsky as a potential Bonaparte', 'Permanent Revolution was less popular than Socialism in One Country'],
             judge='Trotsky made serious errors, but Stalin\'s control of the party was the main reason for his defeat'),
    ],
    'src': [
        S('Lenin\'s Testament, postscript of January 1923 (translated, abridged)', 'Stalin is too rude, and this defect becomes intolerable in a General Secretary. That is why I suggest that the comrades think about a way of removing Stalin from that post.',
          'Lenin\'s view of Stalin', 'Lenin warns that Stalin is unfit to be General Secretary.',
          'To advise the party on the leadership after Lenin\'s death.', 'it is Lenin\'s own judgement', 'Lenin was ill and his views may have been influenced by a personal quarrel with Stalin',
          'It does not show why the party ignored it.', stance=None),
        S('a memoir by a former Soviet official, written in exile, 1930s (illustrative)', 'Every regional secretary owed his post to the Secretariat, and every secretary chose the delegates to the congress. By 1927 Stalin did not need to win debates; he had already counted the votes.',
          'Stalin\'s control of the party', 'It suggests Stalin won because he controlled appointments and congress delegates.',
          'To explain Stalin\'s rise to a Western audience.', 'the author had inside knowledge of the party', 'an exile had reasons to portray Stalin as a manipulator',
          'It does not discuss the appeal of Stalin\'s policies.', stance=True, why='it shows the power of the General Secretary'),
    ],
})

s5b = T('The Great Turn: collectivisation and the Five-Year Plans', 'great turn', 'collectivisation', 'five-year plans')
build_a2(s5b, {
    'enq': 'the Great Turn', 'claim': 'the Five-Year Plans were a success',
    'stim': ['The first Five-Year Plan began in October 1928.', 'In December 1929 Stalin called for the "liquidation of the kulaks as a class".',
             'Famine in 1932-33 killed millions, especially in Ukraine and Kazakhstan.'],
    'terms': [
        ('Great Turn', 'the abandonment of the NEP from 1928-29 in favour of forced collectivisation and rapid industrialisation'),
        ('kolkhoz', 'a collective farm, in which peasants pooled land and worked together, handing produce to the state'),
        ('kulak', 'the term for a richer peasant, used to label and persecute opponents of collectivisation'),
        ('Gosplan', 'the state planning agency that set targets for the Five-Year Plans'),
        ('Stakhanovite', 'a worker who exceeded production targets, named after the miner Alexei Stakhanov'),
        ('Holodomor', 'the Ukrainian term for the famine of 1932-33'),
        ('MTS', 'machine tractor stations, which supplied tractors to collective farms and helped control them'),
    ],
    'dates': [('the first Five-Year Plan began', 1928, 10), ('Stalin called for the liquidation of the kulaks as a class', 1929, 12), ('Stalin published "Dizzy with Success"', 1930, 3),
              ('the first Five-Year Plan was declared complete after four years and three months', 1932, 12), ('Stakhanov mined 102 tonnes of coal in one shift', 1935, 8), ('the third Five-Year Plan began', 1938)],
    'mcq': [
        ('What did Stalin\'s article "Dizzy with Success" (March 1930) do?', 'It blamed local officials for excesses and allowed peasants to leave the collectives temporarily', ['It ended collectivisation permanently', 'It announced the first Five-Year Plan', 'It praised the kulaks'], '[1]'),
        ('Which new industrial city was built around a steel complex in the Urals?', 'Magnitogorsk', ['Leningrad', 'Odessa', 'Stalingrad'], '[1]'),
        ('Which sector did the Five-Year Plans give least priority to?', 'Consumer goods', ['Heavy industry', 'Electricity', 'Armaments'], '[1]'),
    ],
    'why': [
        ('Stalin introduced forced collectivisation', ['The grain procurement crisis of 1927-28 threatened food supplies to the towns', 'Grain exports were needed to pay for industrial machinery', 'Collective farms would be easier to control',
                                                       'Ideology opposed private farming and the kulaks', 'It strengthened Stalin against Bukharin and the Right'],
         'the need for grain to fund industrialisation was the main reason, reinforced by ideology and Stalin\'s political aims'),
        ('the Five-Year Plans achieved rapid growth in heavy industry', ['Massive investment directed by Gosplan', 'Forced labour in the Gulag', 'Propaganda and Stakhanovite campaigns', 'Huge expansion of the industrial workforce from the countryside', 'Foreign experts and technology'],
         'the state could concentrate resources on heavy industry regardless of the human cost'),
    ],
    'claims': [
        ('Collectivisation increased grain output immediately.', False, 'Output fell sharply and livestock numbers collapsed as peasants slaughtered animals.'),
        ('Soviet steel output rose several times over between 1928 and 1937.', True, 'It rose from about 4 million to about 18 million tonnes.'),
        ('The Five-Year Plans gave priority to consumer goods.', False, 'They gave priority to heavy industry; consumer goods were scarce.'),
    ],
    'ess': [
        dict(q='‘The Five-Year Plans were a success.’',
             pro=['Huge increases in coal, steel and electricity output', 'New industrial centres such as Magnitogorsk', 'They built the industrial base that helped the USSR survive the war'],
             con=['Targets were often unrealistic and statistics exaggerated', 'Consumer goods, housing and living standards suffered', 'Waste, poor quality and forced labour'],
             judge='they succeeded in Stalin\'s aim of rapid heavy industrialisation, but at enormous human cost and with much waste'),
        dict(q='To what extent did collectivisation achieve Stalin\'s aims?',
             pro=['The state gained control of the countryside and grain procurements', 'Grain was exported to fund industry', 'Peasants were forced into kolkhozes by the mid-1930s'],
             con=['Grain output fell and livestock collapsed', 'Famine killed millions', 'Peasants resisted and productivity stayed low'],
             judge='collectivisation achieved political control and grain for the state, but it was an economic disaster for agriculture'),
    ],
    'src': [
        S('Stalin, speech to industrial managers, February 1931 (translated, abridged)', 'We are fifty or a hundred years behind the advanced countries. We must make good this distance in ten years. Either we do it, or they crush us.',
          'the reasons for rapid industrialisation', 'Stalin argues that rapid industrialisation is necessary to survive attack by the capitalist powers.',
          'To motivate managers to meet targets.', 'it is Stalin\'s own explanation of his aims', 'it is a speech intended to drive managers harder',
          'It does not show the cost to workers and peasants.', stance=None),
        S('a letter from a worker in Magnitogorsk, 1932 (illustrative)', 'We live in tents and barracks, and there is never enough bread. But the blast furnaces are rising, and they say that soon we will make more steel than all of England.',
          'life during the first Five-Year Plan', 'It suggests that industrial growth was rapid but living conditions were very hard.',
          'To describe his life to his family.', 'it is a first-hand account', 'letters were often censored, so he may have been cautious',
          'It does not show conditions in the countryside.', stance=True, why='it shows rapid industrial growth'),
    ],
})
data_item(s5b, 'soviet_output', 'The table shows Soviet output of steel (million tonnes), from official Soviet figures as revised by Western historians.',
          [('1928', 4.0), ('1932', 5.9), ('1937', 17.7), ('1940', 18.3)], ' million tonnes', 'steel output', notes='the success of the Five-Year Plans')
data_item(s5b, 'soviet_coal', 'The table shows Soviet coal output (million tonnes), as estimated by Western historians.',
          [('1928', 35.4), ('1932', 64.3), ('1937', 128.0), ('1940', 165.9)], ' million tonnes', 'coal output', notes='the success of the Five-Year Plans in heavy industry')

s5c = T('The purges, the Great Terror and the totalitarian state', 'purges', 'great terror', 'totalitarian state')
build_a2(s5c, {
    'enq': 'the Great Terror', 'claim': 'the Great Terror was directed mainly by Stalin himself',
    'stim': ['Sergei Kirov, party leader in Leningrad, was assassinated on 1 December 1934.', 'In 1937-38 the NKVD arrested about 1.5 million people; Soviet records show about 680,000 executions.',
             'Marshal Tukhachevsky was executed in June 1937.'],
    'terms': [
        ('show trials', 'public trials of leading Bolsheviks such as Zinoviev, Kamenev and Bukharin, at which defendants confessed to invented crimes'),
        ('Yezhovshchina', 'the peak of the Terror in 1937-38, named after the NKVD chief Nikolai Yezhov'),
        ('NKVD', 'the Soviet secret police in the 1930s'),
        ('Gulag', 'the system of forced labour camps'),
        ('Order 00447', 'the NKVD order of July 1937 setting regional quotas for arrests and executions of "anti-Soviet elements"'),
        ('totalitarianism', 'a system in which the state seeks total control over every aspect of life'),
    ],
    'dates': [('Kirov was assassinated', 1934, 12.01), ('the trial of Zinoviev and Kamenev was held', 1936, 8), ('Order 00447 was issued', 1937, 7),
              ('Tukhachevsky and other generals were executed', 1937, 6), ('Bukharin was tried and executed', 1938, 3), ('Beria replaced Yezhov as head of the NKVD', 1938, 11)],
    'mcq': [
        ('Who headed the NKVD during the peak of the Terror in 1937-38?', 'Nikolai Yezhov', ['Lavrenty Beria', 'Genrikh Yagoda', 'Felix Dzerzhinsky'], '[1]'),
        ('Why was the purge of the Red Army in 1937-38 significant?', 'It removed many experienced commanders before the war with Germany', ['It strengthened the army before 1941', 'It ended conscription', 'It led to a military coup'], '[1]'),
        ('What does the evidence of Order 00447 suggest about the Terror?', 'It was centrally planned with quotas set from Moscow', ['It was entirely spontaneous', 'It targeted only party leaders', 'It was ordered by local soviets without Moscow\'s knowledge'], '[1]'),
    ],
    'why': [
        ('Stalin launched the Great Terror', ['To eliminate potential rivals such as the Old Bolsheviks', 'Paranoia and fear of a "fifth column" in the event of war', 'To find scapegoats for economic failures', 'To terrorise society into obedience',
                                              'Local officials used the Terror to settle scores and meet quotas'],
         'Stalin initiated and directed the Terror to remove any possible opposition, though local officials and denunciations widened it'),
    ],
    'claims': [
        ('Stalin signed lists of people to be executed during the Terror.', True, 'Archives show he signed lists containing tens of thousands of names.'),
        ('The Terror affected only senior party members.', False, 'Most victims were ordinary citizens, including peasants, workers and national minorities.'),
        ('Yezhov was himself arrested and executed.', True, 'He was arrested in 1939 and executed in 1940.'),
    ],
    'ess': [
        dict(q='‘The Great Terror was directed mainly by Stalin himself.’',
             pro=['Stalin signed execution lists', 'Order 00447 and quotas came from the centre', 'The Terror stopped when Stalin decided in late 1938'],
             con=['Local officials exceeded quotas and used the Terror for their own ends', 'Denunciations by ordinary citizens widened it', 'Some historians stress chaos and pressure from below'],
             judge='the archives show Stalin initiated and directed the Terror, though its scale grew through local zeal and denunciation'),
        dict(q='How far did the purges strengthen Stalin\'s position?',
             pro=['All potential rivals were eliminated', 'A new generation of officials owed everything to him', 'Fear ensured obedience'],
             con=['They weakened the army before 1941', 'They damaged industry and expertise', 'They created chaos that threatened the state'],
             judge='the purges made Stalin\'s personal power unchallengeable, but at great cost to the state\'s effectiveness'),
    ],
    'src': [
        S('a confession by a defendant at a Moscow show trial, 1938 (summary)', 'The defendant confessed to plotting with foreign intelligence services to murder Soviet leaders and restore capitalism.',
          'the show trials', 'It shows defendants confessing to crimes against the state.',
          'To prove the existence of a conspiracy and justify the Terror.', 'it is an official record of the trial', 'confessions were extracted by torture and threats, so they are not reliable evidence of guilt',
          'It does not show how confessions were obtained.', stance=True, why='it shows the regime staging trials directed from the top'),
        S('a report by a regional NKVD chief, 1937 (illustrative)', 'The quota for the first category has been fulfilled. In view of the large number of hostile elements remaining, we request permission to increase the limit by 2,000.',
          'the operation of the Terror', 'It suggests that regional officials asked to exceed quotas set by Moscow.',
          'To request higher quotas from the centre.', 'it shows how the Terror operated in practice', 'an official would want to show zeal to protect himself',
          'It does not show Stalin\'s own role directly.', stance=False, why='it suggests pressure from below as well as direction from above'),
    ],
})

s5d = T('Soviet society and culture under Stalin and Soviet foreign policy to 1941', 'soviet society and culture', 'soviet foreign policy to 1941')
build_a2(s5d, {
    'enq': 'Soviet society and foreign policy under Stalin', 'claim': 'Soviet foreign policy in the 1930s was driven mainly by the need for security',
    'stim': ['In 1934 socialist realism was declared the official style of Soviet art and literature.', 'The USSR joined the League of Nations in September 1934.',
             'On 23 August 1939 the USSR signed a non-aggression pact with Nazi Germany.'],
    'terms': [
        ('socialist realism', 'the official artistic style from 1934, requiring art to show the heroic building of socialism'),
        ('cult of personality', 'the glorification of Stalin as a genius and father of the people'),
        ('Popular Front', 'the Comintern policy from 1935 of communists cooperating with socialists and liberals against fascism'),
        ('collective security', 'the policy, pursued by Litvinov, of working with Western powers through the League against aggression'),
        ('Comintern', 'the Communist International, which directed communist parties around the world from Moscow'),
        ('Winter War', 'the Soviet war against Finland of 1939-40'),
    ],
    'dates': [('the Union of Soviet Writers held its first congress', 1934, 8), ('the USSR joined the League of Nations', 1934, 9), ('the USSR signed a mutual assistance pact with France', 1935, 5),
              ('abortion was banned and divorce made harder', 1936, 6), ('Molotov replaced Litvinov as Foreign Commissar', 1939, 5), ('the Nazi-Soviet Pact was signed', 1939, 8.23), ('Germany invaded the USSR', 1941, 6.22)],
    'mcq': [
        ('Which family policy did Stalin introduce in 1936?', 'Abortion was banned and divorce made more difficult', ['Divorce was made easier', 'Women were barred from work', 'Families were limited to two children'], '[1]'),
        ('Why was Litvinov replaced by Molotov in May 1939?', 'It signalled a move away from collective security towards a deal with Germany', ['Litvinov had been killed', 'Britain demanded it', 'It marked Soviet entry to the League'], 'Litvinov was Jewish and associated with collective security. [1]'),
        ('What did the secret protocol of the Nazi-Soviet Pact give the USSR?', 'A sphere of influence including eastern Poland and the Baltic states', ['Control of Germany', 'Alsace-Lorraine', 'Part of Turkey'], '[1]'),
    ],
    'why': [
        ('Stalin signed the Nazi-Soviet Pact in 1939', ['Britain and France seemed unwilling to make a serious alliance', 'Munich convinced Stalin the West wanted Hitler to turn east', 'The pact gained time to prepare for war', 'It gained territory in eastern Europe', 'The USSR faced Japan in the Far East'],
         'security was the main motive: Stalin distrusted the West and wanted time and territory'),
    ],
    'claims': [
        ('Soviet women gained equal rights in law but often carried a double burden of paid work and housework.', True, 'Women entered industry in huge numbers in the 1930s.'),
        ('The USSR was invited to the Munich Conference in 1938.', False, 'It was excluded.'),
        ('Socialist realism encouraged experimental and abstract art.', False, 'It required realistic, optimistic art that served the state.'),
    ],
    'ess': [
        dict(q='‘Soviet foreign policy in the 1930s was driven mainly by the need for security.’',
             pro=['Collective security and the League after the rise of Hitler', 'The Franco-Soviet pact of 1935', 'The Nazi-Soviet Pact gained time and a buffer zone'],
             con=['Ideology and the Comintern sought to spread communism', 'The secret protocol showed territorial ambitions in eastern Europe', 'The Winter War was aggression against Finland'],
             judge='security was the main driver, but Stalin also took the chance to expand Soviet territory when it came'),
        dict(q='How far did Stalin transform Soviet society in the 1930s?',
             pro=['Mass urbanisation and industrial employment', 'Expansion of education and literacy', 'Control of culture through socialist realism and the cult of personality'],
             con=['Traditional family values were restored after 1936', 'Religion and peasant traditions survived', 'Many changes were imposed rather than accepted'],
             judge='Stalin transformed the structure of society through industrialisation, but in values his policies were often conservative'),
    ],
    'src': [
        S('a Soviet poster, 1930s (description)', 'The poster shows a smiling Stalin holding a young girl with flowers, under the slogan "Thank you, dear Stalin, for our happy childhood!"',
          'the cult of personality', 'It presents Stalin as a caring father figure responsible for children\'s happiness.',
          'To build the cult of personality and loyalty to Stalin.', 'it shows how the regime presented Stalin', 'it is propaganda produced during the Terror and famine',
          'It does not show the reality of life for Soviet families.', stance=None),
        S('a speech by Litvinov to the League of Nations, 1936 (summary)', 'Litvinov argued that peace was indivisible and that only collective action by all peace-loving states could stop aggression.',
          'Soviet foreign policy', 'It shows the USSR presenting itself as a supporter of collective security.',
          'To persuade the League to act against aggression.', 'it is the official Soviet position at the time', 'it was a public speech to win Western trust',
          'It does not show Stalin\'s private calculations.', stance=True, why='it shows Soviet policy seeking security through collective action'),
    ],
})

CHAPTERS[5] = [s5a, s5b, s5c, s5d]


# ============================================================== CHAPTER 6: European history 1919-41, Hitler's Germany

H6_SEATS = [('May 1928', 12), ('September 1930', 107), ('July 1932', 230), ('November 1932', 196), ('March 1933', 288)]
H6_UNEMP = [('1932', 5.6), ('1933', 4.8), ('1934', 2.7), ('1935', 2.2), ('1936', 1.6), ('1937', 0.9), ('1938', 0.4)]

n6a = T('The Nazi rise to power, 1929-33', 'nazi rise to power')
build_a2(n6a, {
    'enq': 'the Nazi rise to power', 'claim': 'the Depression was the main reason for the Nazi rise to power',
    'stim': ['In the Reichstag election of May 1928 the Nazis won 12 seats.', 'By early 1932 about six million Germans were registered as unemployed.',
             'Hitler was appointed Chancellor by President Hindenburg on 30 January 1933.'],
    'terms': [
        ('Article 48', 'the clause of the Weimar constitution allowing the president to rule by emergency decree'),
        ('presidential government', 'government by chancellors appointed by Hindenburg and relying on decrees, from 1930 to 1933'),
        ('SA', 'the Nazi stormtroopers, led by Ernst Röhm'),
        ('Volksgemeinschaft', 'the Nazi idea of a national community united by race'),
        ('backstairs intrigue', 'the behind-the-scenes deals among Papen, Schleicher, Hindenburg and others that led to Hitler\'s appointment'),
        ('Harzburg Front', 'the alliance of nationalists, including the Nazis and Hugenberg\'s DNVP, formed in 1931'),
    ],
    'dates': [('the Wall Street Crash began', 1929, 10), ('Brüning became chancellor', 1930, 3), ('the Nazis won 107 seats in the Reichstag', 1930, 9),
              ('Hindenburg defeated Hitler in the presidential election', 1932, 4), ('the Nazis became the largest party with 230 seats', 1932, 7), ('Hitler was appointed Chancellor', 1933, 1.30)],
    'mcq': [
        ('Which chancellor persuaded Hindenburg to appoint Hitler in January 1933?', 'Franz von Papen', ['Heinrich Brüning', 'Kurt von Schleicher', 'Gustav Stresemann'], 'Papen became vice-chancellor and expected to control Hitler. [1]'),
        ('What happened to the Nazi vote in the November 1932 election?', 'It fell, from 230 to 196 seats', ['It rose to an absolute majority', 'It stayed exactly the same', 'The Nazis were banned'], '[1]'),
        ('Which social group was most over-represented among Nazi voters?', 'Protestant middle-class and rural voters', ['Catholic industrial workers', 'Jewish professionals', 'Members of trade unions in Berlin'], '[1]'),
    ],
    'why': [
        ('the Nazis became the largest party in the Reichstag by July 1932', ['The Depression caused mass unemployment and despair', 'Fear of communism among the middle classes, farmers and elites', 'Effective propaganda under Goebbels and Hitler\'s appeal',
                                                                            'The failure of Weimar governments and the use of Article 48 discredited democracy', 'The Nazis appealed to many social groups as a people\'s party'],
         'the Depression turned the Nazis into a mass party by creating desperation, which their propaganda and organisation exploited'),
        ('Hitler was appointed Chancellor in January 1933', ['Papen and Hindenburg\'s advisers believed they could control him', 'Schleicher had lost Hindenburg\'s confidence', 'The Nazis were the largest party, so their support was needed for a majority', 'Elites wanted mass support for authoritarian government'],
         'Hitler came to power through a backstairs deal by conservatives who wanted to use his mass support'),
    ],
    'claims': [
        ('Hitler was elected Chancellor by a majority of German voters.', False, 'He was appointed by Hindenburg; the Nazis never won a majority in a free election.'),
        ('The Nazis lost seats in the November 1932 election.', True, 'They fell from 230 to 196 seats.'),
        ('Brüning governed largely by presidential decree.', True, 'He used Article 48 from 1930.'),
    ],
    'ess': [
        dict(q='‘The Depression was the main reason for the Nazi rise to power.’',
             pro=['Nazi seats rose from 12 to 230 as unemployment soared', 'The Depression discredited Weimar governments', 'Fear of communism grew with the KPD\'s rising vote'],
             con=['Hitler was appointed through intrigue, not electoral victory', 'Nazi propaganda and organisation', 'Weaknesses of the Weimar constitution and presidential rule after 1930'],
             judge='the Depression made the Nazis a mass party, but Hitler became Chancellor because conservative elites chose to bring him in'),
        dict(q='How far was Hitler\'s appointment as Chancellor the result of backstairs intrigue?',
             pro=['Papen persuaded Hindenburg', 'Schleicher\'s fall opened the way', 'The Nazis were losing votes by November 1932'],
             con=['The Nazis were the largest party', 'Mass support gave Hitler bargaining power', 'The Depression and the collapse of parliamentary government made it possible'],
             judge='intrigue explains the timing and manner, but without mass support Hitler would not have been in a position to benefit'),
    ],
    'src': [
        S('a diary entry by a German civil servant, 1932 (illustrative)', 'My neighbour, a clerk out of work for a year, says he will vote for Hitler because the others have done nothing. He does not care much for the Jews either way; he wants bread and order.',
          'why Germans voted Nazi', 'It suggests unemployment and the failure of other parties drove people to vote Nazi.',
          'To record his observations privately.', 'it is a private account written at the time', 'it records one person\'s motives, which may not be typical',
          'It does not show the role of intrigue in 1933.', stance=True, why='it shows the Depression driving Nazi votes'),
        S('words attributed to Franz von Papen, January 1933 (as later reported; translated)', 'We have hired him. Within two months we will have pushed Hitler so far into a corner that he will squeak.',
          'the appointment of Hitler', 'It suggests conservatives believed they could control Hitler once in office.',
          'To reassure conservatives about the deal.', 'it shows the thinking of a leading conservative at the time', 'it was reported later, may be boastful, and was proved wrong',
          'It does not show why Germans voted Nazi.', stance=False, why='it shows intrigue by conservative elites'),
    ],
})
data_item(n6a, 'nazi_seats', 'The table shows the number of seats won by the Nazi Party in Reichstag elections.', H6_SEATS, ' seats', 'Nazi seats', notes='the reasons for the Nazi rise to power')

n6b = T("Hitler's consolidation of power, 1933-34: a 'legal revolution'?", "hitler's consolidation of power", 'legal revolution')
build_a2(n6b, {
    'enq': 'the consolidation of Nazi power', 'claim': 'Hitler\'s consolidation of power in 1933-34 was a legal revolution',
    'stim': ['The Reichstag building was set on fire on 27 February 1933.', 'On 23 March 1933 the Reichstag passed the Enabling Act by 444 votes to 94.',
             'On 2 August 1934 President Hindenburg died and Hitler became Führer.'],
    'terms': [
        ('Enabling Act', 'the law of March 1933 giving the government power to pass laws without the Reichstag for four years'),
        ('Gleichschaltung', 'coordination, the bringing of all institutions under Nazi control'),
        ('Night of the Long Knives', 'the purge of 30 June 1934 in which Röhm and other SA leaders, and some conservatives, were murdered'),
        ('Reichstag Fire Decree', 'the decree of 28 February 1933 suspending civil rights'),
        ('German Labour Front (DAF)', 'the Nazi organisation that replaced trade unions from May 1933'),
        ('Führer', 'the title Hitler took in August 1934, combining the offices of chancellor and president'),
    ],
    'dates': [('the Reichstag fire took place', 1933, 2.27), ('the Nazis won 43.9 per cent of the vote in the last multi-party election', 1933, 3.05), ('the Enabling Act was passed', 1933, 3.23),
              ('trade unions were abolished', 1933, 5.02), ('Germany became a one-party state', 1933, 7.14), ('the Night of the Long Knives took place', 1934, 6.30), ('Hindenburg died', 1934, 8.02)],
    'mcq': [
        ('Which party was banned from taking its seats when the Enabling Act was passed?', 'The Communist Party (KPD)', ['The Centre Party', 'The SPD', 'The DNVP'], 'Its deputies had been arrested or were in hiding. [1]'),
        ('Which party alone voted against the Enabling Act?', 'The SPD', ['The Centre Party', 'The DNVP', 'The Nazis'], '[1]'),
        ('Why did Hitler purge the SA in June 1934?', 'To win the support of the army and remove Röhm\'s demands for a second revolution', ['Because the SA had attacked the army', 'Because Röhm had won an election', 'Because Hindenburg ordered it'], '[1]'),
    ],
    'why': [
        ('Hitler was able to establish a dictatorship by August 1934', ['The Reichstag Fire Decree allowed the arrest of opponents', 'The Enabling Act gave the government legislative power', 'Gleichschaltung removed rival centres of power',
                                                                       'Opposition parties and trade unions collapsed or were banned', 'The Night of the Long Knives won the army\'s support', 'Terror by the SA and SS intimidated opponents'],
         'Hitler combined legal measures with terror, and the passivity of the elites allowed him to remove every rival'),
    ],
    'claims': [
        ('The Nazis won an absolute majority on their own in March 1933.', False, 'They won 43.9 per cent and needed the DNVP for a majority.'),
        ('The army swore an oath of personal loyalty to Hitler in August 1934.', True, 'This followed Hindenburg\'s death.'),
        ('The Centre Party voted for the Enabling Act.', True, 'It hoped for guarantees for the Catholic Church.'),
    ],
    'ess': [
        dict(q='‘Hitler\'s consolidation of power in 1933-34 was a legal revolution.’',
             pro=['Hitler was appointed constitutionally', 'The Enabling Act was passed by the Reichstag with the required two-thirds majority', 'Decrees were issued under Article 48'],
             con=['Communist deputies were excluded and SA men intimidated the Reichstag', 'Terror against opponents in 1933', 'The Night of the Long Knives was murder outside the law'],
             judge='the revolution used legal forms, but it rested on terror and intimidation, so "legal" describes its appearance rather than its reality'),
        dict(q='How important was the Enabling Act in the creation of the Nazi dictatorship?',
             pro=['It gave Hitler legislative power without the Reichstag', 'It provided the legal basis for later measures', 'It ended parliamentary government'],
             con=['The Reichstag Fire Decree had already suspended civil rights', 'Gleichschaltung and terror mattered as much', 'Control of the army was secured only in 1934'],
             judge='the Enabling Act was the legal foundation of the dictatorship, but it was one step in a process that also depended on terror and the army'),
    ],
    'src': [
        S('Otto Wels, SPD leader, speech in the Reichstag against the Enabling Act, 23 March 1933 (translated, abridged)', 'You can take our lives and our freedom, but you cannot take our honour.',
          'opposition to the Enabling Act', 'It shows the SPD defying the Nazis despite the threat of violence.',
          'To explain the SPD\'s vote against the Act.', 'it is a speech made in the Reichstag at the time', 'it shows the view of one party, made in a highly charged atmosphere',
          'It does not describe the pressure on other parties.', stance=False, why='it suggests the vote took place under threat, not in free conditions'),
        S('a newspaper report, Berlin, March 1933 (illustrative)', 'The deputies made their way to the Kroll Opera House through lines of SA men chanting "We want the bill - or fire and murder!"',
          'the passing of the Enabling Act', 'It suggests intimidation surrounded the vote.',
          'To report the event.', 'it is a contemporary report', 'the press was already under pressure in March 1933',
          'It does not show how deputies voted or why.', stance=False, why='it shows intimidation behind the legal form'),
    ],
})

n6c = T('The Nazi economy and society: the Volksgemeinschaft and racial policy', 'nazi economy and society', 'volksgemeinschaft', 'racial policy')
build_a2(n6c, {
    'enq': 'the Nazi economy and society', 'claim': 'the Nazi regime created a genuine Volksgemeinschaft',
    'stim': ['Registered unemployment in Germany fell from about 6 million in early 1933 to under half a million by 1938.', 'The Four-Year Plan of 1936 aimed to prepare the economy for war.',
             'The Nuremberg Laws of September 1935 deprived German Jews of citizenship.'],
    'terms': [
        ('New Plan', 'Schacht\'s policy of 1934 to control imports and make trade agreements with south-eastern Europe'),
        ('Four-Year Plan', 'the plan of 1936, run by Göring, to make Germany ready for war within four years'),
        ('Strength through Joy (KdF)', 'the Nazi leisure organisation that provided holidays and activities for workers'),
        ('Nuremberg Laws', 'the laws of 1935 depriving Jews of citizenship and banning marriage between Jews and non-Jews'),
        ('Kristallnacht', 'the pogrom of 9-10 November 1938 against Jewish property, synagogues and people'),
        ('Lebensborn', 'the SS programme to raise the birth rate of "racially pure" children'),
        ('autarky', 'economic self-sufficiency, a goal of the Four-Year Plan'),
    ],
    'dates': [('marriage loans were introduced', 1933, 6), ('Schacht introduced the New Plan', 1934, 9), ('the Nuremberg Laws were passed', 1935, 9),
              ('the Four-Year Plan was launched', 1936, 10), ('Kristallnacht took place', 1938, 11.09), ('the T4 euthanasia programme began', 1939)],
    'mcq': [
        ('Who was put in charge of the Four-Year Plan?', 'Hermann Göring', ['Hjalmar Schacht', 'Albert Speer', 'Robert Ley'], '[1]'),
        ('Why do historians question the Nazi claim to have ended unemployment?', 'Women, Jews and those in labour service or the army were removed from the figures', ['Unemployment rose after 1933', 'No statistics were collected', 'All workers were unemployed by 1938'], '[1]'),
        ('Which award encouraged women to have large families?', 'The Mother\'s Cross', ['The Iron Cross', 'The Blood Order', 'The Knight\'s Cross'], 'Introduced in 1938. [1]'),
    ],
    'why': [
        ('unemployment fell rapidly in Nazi Germany', ['Public works such as the autobahns', 'Rearmament and conscription from 1935', 'The National Labour Service', 'Recovery from the Depression was already under way', 'Women and Jews were removed from the figures'],
         'rearmament and public works created jobs, but the figures were also massaged'),
    ],
    'claims': [
        ('Real wages for many workers in 1938 were no higher than in 1928.', True, 'Longer hours and the loss of trade unions offset higher employment.'),
        ('The Nazis abolished private property in industry.', False, 'Big business remained privately owned, though under increasing state direction.'),
        ('The Nuremberg Laws deprived Jews of German citizenship.', True, 'They also banned marriage between Jews and non-Jews.'),
    ],
    'ess': [
        dict(q='‘The Nazi regime created a genuine Volksgemeinschaft.’',
             pro=['Unemployment fell and many workers enjoyed KdF benefits', 'Propaganda and youth organisations spread national unity', 'Many Germans remembered the 1930s as a time of order and recovery'],
             con=['Class differences remained and real wages stagnated', 'Large groups were excluded by race and politics', 'Conformity was enforced by terror'],
             judge='the regime created a sense of national community for many "Aryan" Germans, but it was built on exclusion and coercion rather than genuine equality'),
        dict(q='How successful was Nazi economic policy, 1933-39?',
             pro=['Unemployment fell from about 6 million to under half a million', 'Rapid rearmament', 'Recovery of industrial output'],
             con=['Autarky targets were missed', 'Living standards and consumer goods suffered (guns versus butter)', 'By 1939 the economy faced shortages and overheating'],
             judge='it achieved recovery and rearmament, but by 1939 it was unbalanced and not ready for a long war'),
    ],
    'src': [
        S('a report by an SPD underground observer (Sopade), 1936 (summary)', 'The reports noted that many workers were glad to have jobs and enjoyed KdF trips, but grumbled about long hours, low wages and food prices.',
          'workers\' attitudes', 'It suggests workers had mixed feelings: grateful for jobs but resentful of conditions.',
          'To inform the SPD leadership in exile about conditions in Germany.', 'Sopade reports were based on observers inside Germany', 'observers were opponents of the regime and might emphasise discontent',
          'It does not show the views of groups excluded from the Volksgemeinschaft.', stance=False, why='it shows grumbling and divisions'),
        S('a Nazi poster advertising the KdF car, 1938 (description)', 'The poster shows a family in a shiny Volkswagen on an autobahn, with the slogan "Save five marks a week if you want your own car!"',
          'the Volksgemeinschaft', 'It promises workers a share in prosperity.',
          'To win workers\' loyalty and savings.', 'it shows the image the regime wanted to project', 'it is propaganda; very few savers ever received a car',
          'It does not show real living standards.', stance=True, why='it shows the regime presenting a community of shared prosperity'),
    ],
})
data_item(n6c, 'nazi_unemp', 'The table shows average registered unemployment in Germany (millions), from official figures.', H6_UNEMP, ' million', 'registered unemployment',
          notes='how far Nazi economic policy succeeded')

n6d = T("Hitler's foreign policy and the drive to war, 1933-41", "hitler's foreign policy", 'drive to war')
build_a2(n6d, {
    'enq': 'Hitler\'s foreign policy', 'claim': 'Hitler followed a planned programme of expansion',
    'stim': ['In March 1936 German troops remilitarised the Rhineland.', 'On 1 September 1939 Germany invaded Poland.', 'On 22 June 1941 Germany invaded the Soviet Union in Operation Barbarossa.'],
    'terms': [
        ('Lebensraum', 'living space, Hitler\'s aim of conquering land in the east for German settlement'),
        ('Stufenplan', 'the idea, argued by some historians, that Hitler had a step-by-step plan for expansion'),
        ('Operation Barbarossa', 'the German invasion of the Soviet Union in June 1941'),
        ('Blitzkrieg', 'lightning war, using tanks and aircraft for rapid victories'),
        ('Hossbach Memorandum', 'the record of a meeting in November 1937 at which Hitler outlined plans for expansion'),
        ('Anschluss', 'the union of Germany and Austria in March 1938'),
    ],
    'dates': [('Germany left the League of Nations', 1933, 10), ('Germany reintroduced conscription', 1935, 3), ('German troops remilitarised the Rhineland', 1936, 3),
              ('the Anschluss took place', 1938, 3), ('Germany invaded Poland', 1939, 9.01), ('France surrendered to Germany', 1940, 6.22), ('Germany invaded the Soviet Union', 1941, 6.22)],
    'mcq': [
        ('Which historian\'s 1961 book argued that Hitler was an opportunist?', 'A. J. P. Taylor', ['Hugh Trevor-Roper', 'Fritz Fischer', 'Ian Kershaw'], 'Trevor-Roper argued for a consistent programme. [1]'),
        ('Why did Hitler sign a non-aggression pact with Poland in 1934?', 'To break up France\'s alliances in eastern Europe and appear peaceful', ['To prepare a joint attack on the USSR', 'Because Poland had joined the Axis', 'To return Danzig to Poland'], '[1]'),
        ('When did Germany declare war on the USA?', 'December 1941', ['April 1917', 'September 1939', 'June 1941'], 'After Pearl Harbor. [1]'),
    ],
    'why': [
        ('Hitler invaded the Soviet Union in 1941', ['To win Lebensraum in the east', 'Ideological hatred of "Jewish Bolshevism"', 'To gain resources such as Ukrainian grain and Caucasian oil', 'To defeat Britain\'s last potential ally on the continent', 'He believed the Red Army was weak after the purges'],
         'Barbarossa was the fulfilment of Hitler\'s core ideological aim of Lebensraum, justified also by strategic calculation'),
    ],
    'claims': [
        ('Hitler\'s first foreign policy steps included leaving the League of Nations.', True, 'Germany left in October 1933.'),
        ('Germany invaded the USSR before France fell.', False, 'France fell in June 1940; Barbarossa began in June 1941.'),
        ('Mein Kampf mentioned the aim of Lebensraum in the east.', True, 'It called for land in Russia and its border states.'),
    ],
    'ess': [
        dict(q='‘Hitler followed a planned programme of expansion.’',
             pro=['Mein Kampf set out the aim of Lebensraum', 'The Hossbach Memorandum showed plans for expansion', 'Barbarossa fulfilled his eastern aims'],
             con=['He exploited opportunities such as the Anschluss crisis', 'The timing of events often depended on others', 'He did not expect war with Britain in 1939'],
             judge='Hitler had consistent long-term aims but was an opportunist in their timing and method'),
        dict(q='How far was Hitler\'s foreign policy successful in 1933-41?',
             pro=['Versailles was overturned without war by 1938', 'Rapid victories over Poland and France', 'By 1941 Germany dominated continental Europe'],
             con=['He failed to defeat Britain', 'Barbarossa failed before Moscow in December 1941', 'He brought the USA into the war'],
             judge='his policy was spectacularly successful until 1940, but the attack on the USSR and war with the USA turned success into eventual defeat'),
    ],
    'src': [
        S('Hitler, Mein Kampf, 1925 (translated, abridged)', 'If we speak of soil in Europe today, we can primarily have in mind only Russia and her vassal border states.',
          'Hitler\'s aims', 'Hitler states that German expansion must be at the expense of Russia.',
          'To set out his ideas and win support.', 'it is Hitler\'s own statement of his ideas', 'it was written in 1924-25 before he had power, so it shows aims rather than a plan',
          'It does not give a timetable for expansion.', stance=True, why='it shows long-term aims of expansion in the east'),
        S('a historian writing in 1961 (summary of A. J. P. Taylor\'s argument)', 'Taylor argued that Hitler was a traditional statesman who took advantage of the opportunities others gave him, and that he did not intend a general war in 1939.',
          'Hitler\'s foreign policy', 'Taylor argues Hitler was an opportunist without a fixed plan.',
          'To challenge the view of Hitler as following a blueprint.', 'Taylor used diplomatic documents', 'his view was controversial and criticised for underplaying ideology',
          'It does not address Hitler\'s racial aims.', stance=False, why='it argues there was no planned programme', kind='secondary'),
    ],
})

CHAPTERS[6] = [n6a, n6b, n6c, n6d]


# ============================================================== CHAPTER 7: The USA 1945-93, the economy

US_INFL = [('1965', 1.6), ('1970', 5.7), ('1974', 11.0), ('1979', 11.3), ('1980', 13.5), ('1983', 3.2)]
US_UNEMP = [('1969', 3.5), ('1975', 8.5), ('1979', 5.8), ('1982', 9.7), ('1989', 5.3)]

u7a = T('The post-war boom: consumerism, suburbanisation and the affluent society', 'post-war boom', 'consumerism, suburbanisation', 'affluent society')
build_a2(u7a, {
    'enq': 'the post-war boom', 'claim': 'all Americans shared in the prosperity of the post-war boom',
    'stim': ['The GI Bill of 1944 helped millions of veterans to attend college and buy homes.', 'The first Levittown was built on Long Island, New York, from 1947.',
             'In 1958 J. K. Galbraith published The Affluent Society.'],
    'terms': [
        ('GI Bill', 'the Servicemen\'s Readjustment Act of 1944, which gave veterans education grants and cheap home loans'),
        ('baby boom', 'the sharp rise in the birth rate in the USA from 1946 to about 1964'),
        ('suburbanisation', 'the movement of people, especially white middle-class families, from cities to new suburbs'),
        ('consumerism', 'a culture centred on buying consumer goods such as cars, televisions and household appliances'),
        ('Levittown', 'the mass-produced suburban housing developments built by William Levitt from 1947'),
        ('The Affluent Society', 'Galbraith\'s 1958 book arguing that private wealth coexisted with public poverty'),
    ],
    'dates': [('the GI Bill was passed', 1944, 6), ('construction of the first Levittown began', 1947), ('the Interstate Highway Act was passed', 1956, 6),
              ('Galbraith published The Affluent Society', 1958), ('Michael Harrington published The Other America', 1962)],
    'mcq': [
        ('Which law of 1956 funded a national network of motorways?', 'The Federal-Aid Highway Act (Interstate Highway Act)', ['The GI Bill', 'The Employment Act', 'The Taft-Hartley Act'], '[1]'),
        ('Which book of 1962 drew attention to poverty in the USA?', 'The Other America by Michael Harrington', ['The Affluent Society by J. K. Galbraith', 'The Feminine Mystique by Betty Friedan', 'The Jungle by Upton Sinclair'], '[1]'),
        ('Which group was largely excluded from the new Levittown suburbs?', 'African Americans', ['War veterans', 'Young families', 'White factory workers'], 'Restrictive covenants and lending practices excluded them. [1]'),
    ],
    'why': [
        ('the US economy boomed after 1945', ['Pent-up wartime savings fuelled consumer spending', 'The GI Bill and cheap mortgages encouraged house building', 'Defence spending during the Cold War', 'US industry faced little foreign competition', 'Cheap oil and new technology'],
         'consumer demand released after the war, supported by government spending and US economic dominance, drove the boom'),
    ],
    'claims': [
        ('Poverty disappeared in the USA during the 1950s.', False, 'Around a fifth of Americans were still in poverty around 1960.'),
        ('Car ownership and television spread rapidly in the 1950s.', True, 'By 1960 most households had a television.'),
        ('The baby boom began in 1946.', True, 'It lasted until about 1964.'),
    ],
    'ess': [
        dict(q='‘All Americans shared in the prosperity of the post-war boom.’',
             pro=['Real incomes rose for most families', 'Home ownership and car ownership spread widely', 'Unionised workers gained higher wages and benefits'],
             con=['African Americans faced discrimination in housing and jobs', 'Rural poverty, as in Appalachia, persisted', 'Inner cities declined as the suburbs grew'],
             judge='the boom raised living standards for a majority, but significant groups, especially African Americans and the rural poor, were left out'),
        dict(q='How far was government policy responsible for the post-war boom?',
             pro=['The GI Bill and federal mortgage support', 'Defence spending', 'The Interstate Highway programme'],
             con=['Private consumer demand and savings', 'US industrial dominance with weak foreign competitors', 'Technological innovation and cheap energy'],
             judge='government policy supported and shaped the boom, but its main driver was private consumer demand in an economy without serious competitors'),
    ],
    'src': [
        S('an advertisement for a suburban housing development, 1950s (description)', 'The advertisement shows a smiling white family outside a new house with a car in the drive, under the slogan "Your own home - no money down for veterans".',
          'suburban life', 'It presents suburban home ownership as easily available and desirable.',
          'To sell houses.', 'it shows the ideal that was marketed at the time', 'it is advertising and shows only the image the builder wanted',
          'It does not show who was excluded.', stance=True, why='it presents prosperity as widely shared'),
        S('Michael Harrington, The Other America, 1962 (summary)', 'Harrington argued that around 40 to 50 million Americans lived in poverty, hidden from the affluent in rural areas and city slums.',
          'poverty in the affluent society', 'It argues that a large minority of Americans did not share in prosperity.',
          'To expose hidden poverty and press for action.', 'it was based on research and influenced Kennedy and Johnson', 'Harrington was a socialist campaigner and his estimates were debated',
          'It does not show the gains of the majority.', stance=False, why='it shows many Americans excluded from prosperity', kind='secondary'),
    ],
})

u7b = T('Government and the economy: Keynesianism, the Great Society and the Cold War economy', 'keynesianism', 'great society', 'cold war economy')
build_a2(u7b, {
    'enq': 'government and the economy', 'claim': 'the Great Society was a success',
    'stim': ['The Employment Act of 1946 committed the federal government to promoting maximum employment.', 'In his farewell address of January 1961 Eisenhower warned against the "military-industrial complex".',
             'In 1964 Lyndon Johnson declared an "unconditional war on poverty".'],
    'terms': [
        ('Keynesianism', 'the economic theory that governments should manage demand, spending more in recessions, to maintain full employment'),
        ('military-industrial complex', 'Eisenhower\'s term for the alliance of the armed forces and arms industries'),
        ('Great Society', 'Lyndon Johnson\'s programme of social reforms from 1964'),
        ('War on Poverty', 'the Great Society programmes, from 1964, aimed at reducing poverty'),
        ('Medicare', 'the federal health insurance programme for people over 65, created in 1965'),
        ('guns and butter', 'the attempt to fund both the Vietnam War and domestic social programmes'),
    ],
    'dates': [('the Employment Act was passed', 1946, 2), ('the Taft-Hartley Act restricted trade unions', 1947, 6), ('Eisenhower warned of the military-industrial complex', 1961, 1),
              ('the Kennedy-Johnson tax cut was passed', 1964, 2), ('the Economic Opportunity Act was passed', 1964, 8), ('Medicare and Medicaid were created', 1965, 7)],
    'mcq': [
        ('Which programme provided health care for poor Americans from 1965?', 'Medicaid', ['Medicare', 'Social Security', 'Head Start'], 'Medicare covered those over 65. [1]'),
        ('Which Great Society programme gave pre-school education to poor children?', 'Head Start', ['Job Corps', 'Medicare', 'VISTA'], '[1]'),
        ('How did the Vietnam War affect the Great Society?', 'It diverted money and political attention and fuelled inflation', ['It increased funding for poverty programmes', 'It had no effect', 'It ended unemployment permanently'], '[1]'),
    ],
    'why': [
        ('poverty fell in the 1960s', ['Strong economic growth created jobs', 'Great Society programmes such as Medicaid and food stamps', 'Increases in Social Security benefits reduced poverty among the elderly', 'Civil rights laws opened opportunities'],
         'economic growth did most to reduce poverty, but the Great Society made a real difference, especially for the elderly'),
    ],
    'claims': [
        ('The official poverty rate fell during the 1960s.', True, 'It fell from about 22 per cent in 1959 to about 12 per cent in 1969.'),
        ('Eisenhower called for higher defence spending in his farewell address.', False, 'He warned against the influence of the military-industrial complex.'),
        ('Medicare provides health insurance for older Americans.', True, 'It covers people aged 65 and over.'),
    ],
    'ess': [
        dict(q='‘The Great Society was a success.’',
             pro=['Poverty fell sharply in the 1960s', 'Medicare and Medicaid gave lasting health coverage', 'Education programmes such as Head Start'],
             con=['Many programmes were underfunded because of Vietnam', 'Inner-city poverty and unrest continued', 'Critics argued it created dependency and fuelled inflation'],
             judge='it achieved lasting gains, especially in health care and for the elderly, but fell short of its aim of ending poverty'),
        dict(q='How far did the Cold War shape the US economy, 1945-68?',
             pro=['Defence spending stimulated industry and technology', 'Aerospace and electronics grew in the Sunbelt', 'The space race funded research and education'],
             con=['Consumer demand was the main engine of growth', 'Housing and the car industry drove the boom', 'Government social programmes mattered too'],
             judge='the Cold War economy was a major support for growth and shaped its regional pattern, but consumer demand was the main engine'),
    ],
    'src': [
        S('Lyndon Johnson, State of the Union address, January 1964 (abridged)', 'This administration today, here and now, declares unconditional war on poverty in America.',
          'the War on Poverty', 'Johnson commits the government to ending poverty.',
          'To win support in Congress and the country for his programme.', 'it is the president\'s own statement of policy', 'it is political rhetoric and promises more than was delivered',
          'It does not show the results of the programmes.', stance=None),
        S('a report by a community worker in a city neighbourhood, 1968 (illustrative)', 'The programmes brought a clinic and a pre-school, and they are full. But the jobs have gone to the suburbs and the money from Washington has dried up since the war took over.',
          'the effects of the Great Society', 'It suggests the programmes helped but were limited by job losses and cuts linked to the war.',
          'To report on local conditions.', 'it is a first-hand local account', 'it describes one neighbourhood only',
          'It does not give national figures.', stance=False, why='it shows the limits of the Great Society'),
    ],
})

u7c = T('Stagflation and economic decline in the 1970s', 'stagflation', 'economic decline in the 1970s')
build_a2(u7c, {
    'enq': 'the US economy in the 1970s', 'claim': 'the oil crises were the main cause of stagflation in the 1970s',
    'stim': ['In August 1971 Nixon suspended the convertibility of the dollar into gold.', 'The OPEC oil embargo of 1973-74 quadrupled the price of oil.', 'In 1980 consumer price inflation in the USA reached 13.5 per cent.'],
    'terms': [
        ('stagflation', 'a combination of high inflation, high unemployment and slow economic growth'),
        ('Nixon Shock', 'Nixon\'s measures of August 1971, including ending gold convertibility of the dollar and a wage-price freeze'),
        ('OPEC', 'the Organization of the Petroleum Exporting Countries'),
        ('misery index', 'the sum of the inflation rate and the unemployment rate'),
        ('Bretton Woods system', 'the post-war system of fixed exchange rates tied to the dollar, which collapsed in 1971-73'),
        ('deindustrialisation', 'the decline of manufacturing industry, especially in the north-east and Midwest'),
    ],
    'dates': [('Nixon ended the convertibility of the dollar into gold', 1971, 8), ('the OPEC oil embargo began', 1973, 10), ('Ford launched the "Whip Inflation Now" campaign', 1974, 10),
              ('the Iranian revolution caused a second oil shock', 1979, 1), ('Paul Volcker became chairman of the Federal Reserve', 1979, 8)],
    'mcq': [
        ('Why did OPEC Arab states impose an oil embargo on the USA in 1973?', 'In response to US support for Israel in the Yom Kippur War', ['Because the USA had invaded Iran', 'Because of the Nixon Shock', 'Because the USA had nationalised oil firms'], '[1]'),
        ('How did Paul Volcker tackle inflation after 1979?', 'By raising interest rates sharply to restrict the money supply', ['By increasing government spending', 'By freezing all prices', 'By returning to the gold standard'], '[1]'),
        ('Which foreign competitors challenged US manufacturing in the 1970s?', 'Japan and West Germany', ['The USSR and China', 'Britain and France', 'Brazil and Argentina'], '[1]'),
    ],
    'why': [
        ('the US economy suffered stagflation in the 1970s', ['Oil price shocks in 1973 and 1979 raised costs', 'Spending on Vietnam and the Great Society without tax rises created inflation', 'Foreign competition from Japan and West Germany', 'Falling productivity growth', 'The collapse of Bretton Woods weakened the dollar'],
         'the oil shocks were the trigger, but inflation had deep roots in the spending of the 1960s and US competitiveness was declining'),
    ],
    'claims': [
        ('Stagflation means high inflation combined with high unemployment.', True, 'Keynesian policies struggled because the two normally move in opposite directions.'),
        ('Inflation was below 3 per cent throughout the 1970s.', False, 'It exceeded 11 per cent in 1974 and 1979.'),
        ('Nixon introduced a temporary freeze on wages and prices in 1971.', True, 'It was part of the New Economic Policy.'),
    ],
    'ess': [
        dict(q='‘The oil crises were the main cause of stagflation in the 1970s.’',
             pro=['Oil prices quadrupled in 1973-74 and rose again in 1979', 'Energy costs raised prices across the economy', 'Each shock was followed by recession'],
             con=['Inflation was already rising in the late 1960s because of Vietnam spending', 'Productivity growth slowed and foreign competition increased', 'Policy mistakes such as wage-price controls and loose monetary policy'],
             judge='the oil shocks made stagflation severe, but its roots lay in the spending of the 1960s and declining competitiveness'),
        dict(q='How effectively did US presidents deal with the economic problems of the 1970s?',
             pro=['Nixon\'s controls briefly slowed inflation', 'Carter appointed Volcker, whose policies eventually ended high inflation', 'Energy conservation measures were introduced'],
             con=['Controls caused shortages and inflation returned', 'Ford\'s WIN campaign achieved little', 'Inflation and unemployment were both high in 1980'],
             judge='presidents were largely ineffective, though Carter\'s appointment of Volcker began the cure'),
    ],
    'src': [
        S('Jimmy Carter, televised address, July 1979 (summary)', 'Carter spoke of a "crisis of confidence" among Americans and called on them to save energy and work together to overcome the nation\'s problems.',
          'responses to the economic crisis', 'It shows the president presenting the crisis as one of national morale.',
          'To rally the nation behind his energy policy.', 'it is the president\'s own analysis', 'it was a political speech that many saw as blaming the public',
          'It does not give economic data.', stance=None),
        S('a newspaper report from a petrol station, 1974 (illustrative)', 'The queue stretched for half a mile. Drivers who had waited two hours were told the pumps were dry. Prices have doubled since the autumn.',
          'the oil crisis', 'It shows shortages and rising prices caused by the oil crisis.',
          'To report the crisis to readers.', 'it is a contemporary eyewitness report', 'it describes one place and day',
          'It does not show other causes of inflation.', stance=True, why='it shows the direct effect of the oil crisis'),
    ],
})
data_item(u7c, 'us_inflation', 'The table shows the annual rate of consumer price inflation in the USA (per cent).', US_INFL, '%', 'the inflation rate', notes='the causes and extent of stagflation')

u7d = T('Reaganomics and the economy in the 1980s', 'reaganomics', 'economy in the 1980s')
build_a2(u7d, {
    'enq': 'Reaganomics', 'claim': 'Reaganomics revived the US economy',
    'stim': ['The Economic Recovery Tax Act of 1981 cut the top rate of income tax from 70 to 50 per cent.', 'In late 1982 unemployment in the USA reached about 10.8 per cent.',
             'The federal debt roughly tripled during the 1980s.'],
    'terms': [
        ('Reaganomics', 'Reagan\'s economic policies of tax cuts, deregulation, reduced domestic spending and tight money'),
        ('supply-side economics', 'the theory that lower taxes and less regulation encourage investment, work and growth'),
        ('trickle-down', 'the critics\' term for the idea that benefits to the rich would spread to everyone'),
        ('deregulation', 'the removal of government rules on business, for example in airlines and banking'),
        ('budget deficit', 'the gap when government spending exceeds revenue in a year'),
        ('PATCO strike', 'the air traffic controllers\' strike of 1981, broken when Reagan dismissed over 11,000 strikers'),
    ],
    'dates': [('the Economic Recovery Tax Act was passed', 1981, 8), ('Reagan dismissed striking air traffic controllers', 1981, 8), ('the US economy began to recover from recession', 1983),
              ('the Tax Reform Act cut the top rate to 28 per cent', 1986, 10), ('the stock market crashed on "Black Monday"', 1987, 10)],
    'mcq': [
        ('What happened to the federal budget deficit under Reagan?', 'It grew sharply because of tax cuts and higher defence spending', ['It disappeared', 'It stayed constant', 'It became a surplus by 1984'], '[1]'),
        ('What caused the recession of 1981-82?', 'Very high interest rates set by the Federal Reserve to curb inflation', ['The Wall Street Crash', 'The Vietnam War', 'A rise in income tax'], '[1]'),
        ('Which financial institutions suffered a major crisis in the late 1980s after deregulation?', 'Savings and loan associations', ['The Federal Reserve banks', 'Credit unions in Canada', 'The World Bank'], '[1]'),
    ],
    'why': [
        ('the US economy recovered after 1982', ['Inflation fell after Volcker\'s tight money policy', 'Tax cuts boosted spending and investment', 'Higher defence spending acted as a stimulus', 'Oil prices fell in the mid-1980s'],
         'falling inflation and oil prices, together with a large fiscal stimulus, explain the recovery more than supply-side theory'),
    ],
    'claims': [
        ('Reagan balanced the federal budget.', False, 'Deficits grew and the debt roughly tripled.'),
        ('Inflation fell sharply in the early 1980s.', True, 'It fell from 13.5 per cent in 1980 to about 3 per cent in 1983.'),
        ('Income inequality grew in the 1980s.', True, 'Gains went disproportionately to the highest earners.'),
    ],
    'ess': [
        dict(q='‘Reaganomics revived the US economy.’',
             pro=['Inflation fell and growth was strong from 1983', 'Millions of new jobs were created', 'Tax cuts and deregulation encouraged enterprise'],
             con=['Volcker\'s monetary policy, not Reagan\'s, defeated inflation', 'Deficits and debt soared', 'Manufacturing decline and inequality grew'],
             judge='the economy revived in the 1980s, but its recovery owed as much to falling inflation and deficit spending as to supply-side policies'),
        dict(q='How far did Reagan\'s economic policies benefit all Americans?',
             pro=['Unemployment fell after 1983', 'Lower inflation helped savers and consumers', 'Tax cuts applied to all income groups'],
             con=['Top earners gained most', 'Cuts in social programmes hurt the poor', 'Industrial workers lost jobs in the Rust Belt'],
             judge='most Americans were better off by 1989 than in 1980, but the gains were very unequal'),
    ],
    'src': [
        S('Ronald Reagan, inaugural address, January 1981 (abridged)', 'In this present crisis, government is not the solution to our problem; government is the problem.',
          'Reagan\'s economic philosophy', 'Reagan argues that big government caused the economic crisis.',
          'To set out his philosophy and win support for cutting government.', 'it is Reagan\'s own statement of his aims', 'it is rhetoric and simplifies the causes of the crisis',
          'It does not show the results of his policies.', stance=None),
        S('a letter from a laid-off steelworker in Ohio, 1986 (illustrative)', 'They tell me the economy is booming. Our mill closed three years ago and the only jobs here pay half what I used to earn.',
          'the effects of the 1980s economy', 'It suggests that recovery did not reach industrial workers.',
          'To express his experience in a local newspaper.', 'it is a first-hand account', 'it is one worker in one region',
          'It does not give national figures.', stance=False, why='it shows the limits of the recovery'),
    ],
})
data_item(u7d, 'us_unemp', 'The table shows the annual average unemployment rate in the USA (per cent).', US_UNEMP, '%', 'the unemployment rate', notes='the effects of economic policy in the 1970s and 1980s')

CHAPTERS[7] = [u7a, u7b, u7c, u7d]


# ============================================================== CHAPTER 8: The USA 1945-93, society and civil rights

r8a = T('The civil rights movement, 1945-68: strategies, leaders and federal responses', 'civil rights movement, 1945-68', 'strategies, leaders and federal responses')
build_a2(r8a, {
    'enq': 'the civil rights movement', 'claim': 'Martin Luther King was the most important reason for the success of the civil rights movement',
    'stim': ['In May 1954 the Supreme Court ruled in Brown v. Board of Education that segregated schools were unconstitutional.', 'The Montgomery Bus Boycott lasted 381 days from December 1955.',
             'About 250,000 people took part in the March on Washington in August 1963.'],
    'terms': [
        ('Brown v. Board of Education', 'the Supreme Court ruling of 1954 that segregation in public schools was unconstitutional'),
        ('NAACP', 'the National Association for the Advancement of Colored People, which fought segregation through the courts'),
        ('SCLC', 'the Southern Christian Leadership Conference, founded in 1957 with King as its leader'),
        ('SNCC', 'the Student Nonviolent Coordinating Committee, founded in 1960 after the sit-ins'),
        ('Freedom Rides', 'the 1961 bus journeys through the South to test the desegregation of interstate travel'),
        ('massive resistance', 'the campaign by southern white politicians to block school desegregation'),
    ],
    'dates': [('Truman ordered the desegregation of the armed forces', 1948, 7), ('the Brown v. Board of Education ruling was given', 1954, 5), ('the Montgomery Bus Boycott began', 1955, 12),
              ('federal troops escorted Black students into Central High School, Little Rock', 1957, 9), ('the Greensboro sit-in began', 1960, 2), ('the March on Washington took place', 1963, 8),
              ('the Civil Rights Act was passed', 1964, 7), ('the Voting Rights Act was passed', 1965, 8)],
    'mcq': [
        ('Why was the Birmingham campaign of 1963 significant?', 'Television images of police using dogs and fire hoses on protesters shocked the nation', ['It ended segregation in all southern states', 'It was the first sit-in', 'It led to Brown v. Board of Education'], '[1]'),
        ('What did the Voting Rights Act of 1965 do?', 'It banned literacy tests and allowed federal registrars to register voters', ['It desegregated schools', 'It created affirmative action', 'It gave the vote to women'], '[1]'),
        ('Which campaign in 1965 directly led to the Voting Rights Act?', 'The Selma to Montgomery marches', ['The Montgomery Bus Boycott', 'The Freedom Rides', 'The Albany Movement'], '[1]'),
    ],
    'why': [
        ('the civil rights movement achieved major legal changes by 1965', ['Nonviolent direct action exposed southern brutality', 'Television brought events to a national audience', 'Leaders such as King built alliances and won public support',
                                                                           'Federal courts and presidents Kennedy and Johnson acted', 'Grassroots activism by local people and students', 'The Cold War made segregation an embarrassment abroad'],
         'grassroots nonviolent protest created crises that forced the federal government to act'),
    ],
    'claims': [
        ('The Brown ruling immediately desegregated all southern schools.', False, 'Massive resistance meant most southern schools stayed segregated for years.'),
        ('The Civil Rights Act of 1964 banned segregation in public places.', True, 'It also banned discrimination in employment.'),
        ('Rosa Parks was a long-standing NAACP activist.', True, 'She was secretary of the Montgomery NAACP branch.'),
    ],
    'ess': [
        dict(q='‘Martin Luther King was the most important reason for the success of the civil rights movement, 1955-68.’',
             pro=['His leadership and oratory won national support', 'He led key campaigns at Montgomery, Birmingham and Selma', 'He built alliances with white liberals and the federal government'],
             con=['Grassroots activists and local leaders started many campaigns', 'The NAACP\'s legal strategy won Brown', 'Federal action by Johnson and Congress was decisive', 'SNCC and students led sit-ins and voter registration'],
             judge='King was the movement\'s most important national leader, but its success rested on grassroots activism and federal action'),
        dict(q='How far did the federal government help the civil rights movement, 1945-68?',
             pro=['The Supreme Court ruled against segregation in Brown', 'Johnson passed the Civil Rights and Voting Rights Acts', 'Federal troops were used at Little Rock and Ole Miss'],
             con=['Eisenhower and Kennedy acted reluctantly', 'The FBI under Hoover spied on King', 'Enforcement of Brown was slow'],
             judge='the federal government gave decisive help, especially in 1964-65, but usually only after protest forced it to act'),
    ],
    'src': [
        S('Martin Luther King, Letter from Birmingham Jail, April 1963 (abridged)', 'We know through painful experience that freedom is never voluntarily given by the oppressor; it must be demanded by the oppressed.',
          'civil rights strategy', 'King argues that direct action is necessary because rights will not be granted voluntarily.',
          'To answer white clergy who called his campaign untimely.', 'it is King\'s own explanation of his strategy', 'it is persuasive writing aimed at white moderates',
          'It does not show the role of other activists.', stance=True, why='it shows King\'s leadership in setting strategy'),
        S('a memoir by a SNCC voter-registration worker in Mississippi, 1970s (illustrative)', 'Dr King came for a day and the cameras came with him. When they left, it was local people who kept on, house by house, for years.',
          'grassroots activism', 'It suggests that local activists, not national leaders, did most of the work.',
          'To record the role of grassroots activists.', 'the author took part in the campaign', 'it was written later and may reflect SNCC\'s rivalry with King',
          'It does not show the effect of national campaigns.', stance=False, why='it stresses grassroots activism over King'),
    ],
})

r8b = T('Black Power and the civil rights movement after 1968', 'black power', 'after 1968')
build_a2(r8b, {
    'enq': 'the civil rights movement after 1968', 'claim': 'the Black Power movement did more harm than good to the cause of civil rights',
    'stim': ['In June 1966 Stokely Carmichael called for "Black Power" during the March Against Fear in Mississippi.', 'Martin Luther King was assassinated in Memphis on 4 April 1968.',
             'In 1971 the Supreme Court approved busing to desegregate schools in Swann v. Charlotte-Mecklenburg.'],
    'terms': [
        ('Black Power', 'the movement stressing Black pride, self-reliance and self-defence, popularised by Stokely Carmichael from 1966'),
        ('Black Panther Party', 'the organisation founded in Oakland in 1966 that combined armed self-defence with community programmes'),
        ('affirmative action', 'policies to increase opportunities for groups that had faced discrimination, for example in jobs and education'),
        ('busing', 'transporting pupils to schools outside their neighbourhood to achieve racial integration'),
        ('Kerner Commission', 'the commission that reported in 1968 that the USA was moving towards two societies, one Black, one white'),
        ('de facto segregation', 'segregation that exists in practice, for example in housing, rather than by law'),
    ],
    'dates': [('Malcolm X was assassinated', 1965, 2), ('the Black Panther Party was founded', 1966, 10), ('the Kerner Commission reported', 1968, 2),
              ('Martin Luther King was assassinated', 1968, 4.04), ('the Swann ruling approved busing', 1971, 4), ('the Bakke case limited racial quotas', 1978, 6)],
    'mcq': [
        ('What did the Black Panthers\' community programmes include?', 'Free breakfasts for children and health clinics', ['Building Levittowns', 'Voter registration in Mississippi in 1964', 'Running the Freedom Rides'], '[1]'),
        ('Which city saw violent opposition to busing in 1974?', 'Boston', ['Atlanta', 'Montgomery', 'Oakland'], '[1]'),
        ('Who became the first Black woman elected to Congress, in 1968?', 'Shirley Chisholm', ['Rosa Parks', 'Fannie Lou Hamer', 'Ella Baker'], '[1]'),
    ],
    'why': [
        ('Black Power gained support after 1965', ['Frustration at the slow pace of change, especially in northern cities', 'The limits of nonviolence in the face of violence', 'Urban riots such as Watts in 1965', 'The influence of Malcolm X', 'Desire for Black pride and community control'],
         'frustration that legal gains had not changed conditions in the northern ghettos drove support for Black Power'),
    ],
    'claims': [
        ('King\'s Poor People\'s Campaign focused on economic inequality.', True, 'He was planning it at the time of his death.'),
        ('Black Power rejected all forms of self-defence.', False, 'It accepted self-defence, unlike strict nonviolence.'),
        ('The number of Black elected officials grew substantially after 1965.', True, 'The Voting Rights Act made this possible.'),
    ],
    'ess': [
        dict(q='‘The Black Power movement did more harm than good to the cause of civil rights.’',
             pro=['It alienated white liberal supporters', 'Associations with violence fuelled a "law and order" backlash', 'It divided the movement'],
             con=['It built Black pride and cultural identity', 'Community programmes met real needs', 'It drew attention to economic and northern problems that legal change had not solved'],
             judge='Black Power damaged the movement\'s alliances, but it addressed issues that nonviolent campaigns had not reached'),
        dict(q='How far had African Americans achieved equality by the early 1990s?',
             pro=['Legal segregation had ended and voting rights were protected', 'A growing Black middle class', 'Black politicians such as mayors and members of Congress'],
             con=['Income and wealth gaps remained wide', 'Residential and school segregation persisted', 'Tensions over policing, as in Los Angeles in 1992'],
             judge='legal equality had been achieved, but economic and social equality had not'),
    ],
    'src': [
        S('Stokely Carmichael, speech, 1966 (summary)', 'Carmichael argued that Black people must define their own goals, lead their own organisations and build political and economic power in their communities.',
          'Black Power', 'It shows Black Power as a call for self-determination and community power.',
          'To explain and win support for Black Power.', 'it is the view of the leader who popularised the term', 'it is a political speech',
          'It does not show how white Americans reacted.', stance=False, why='it presents Black Power as constructive'),
        S('a newspaper editorial, 1967 (illustrative)', 'The slogan of Black Power has frightened the very people whose votes passed the Civil Rights Act. Every riot makes the next law harder to pass.',
          'reactions to Black Power', 'It suggests Black Power and riots caused a white backlash.',
          'To warn against militancy.', 'it shows white liberal opinion at the time', 'it may blame Black activists for wider white hostility',
          'It does not show the causes of the riots.', stance=True, why='it suggests Black Power harmed the movement'),
    ],
})

r8c = T("The growth of feminism and the women's movement in the 1960s and 1970s", 'growth of feminism', "women's movement")
build_a2(r8c, {
    'enq': 'the women\'s movement', 'claim': 'the women\'s movement achieved significant change by 1980',
    'stim': ['In 1963 Betty Friedan published The Feminine Mystique.', 'The National Organization for Women was founded in 1966.', 'In January 1973 the Supreme Court ruled in Roe v. Wade.'],
    'terms': [
        ('The Feminine Mystique', 'Betty Friedan\'s 1963 book describing the dissatisfaction of many suburban housewives'),
        ('NOW', 'the National Organization for Women, founded in 1966 to campaign for equal rights'),
        ('Equal Rights Amendment', 'the proposed amendment banning discrimination on grounds of sex, passed by Congress in 1972 but not ratified'),
        ('Title IX', 'the 1972 law banning sex discrimination in federally funded education'),
        ('women\'s liberation', 'the radical wing of the movement, which challenged patriarchy and stressed that "the personal is political"'),
        ('STOP ERA', 'Phyllis Schlafly\'s campaign against the Equal Rights Amendment'),
    ],
    'dates': [('the Equal Pay Act was passed', 1963, 6), ('Friedan published The Feminine Mystique', 1963, 2), ('NOW was founded', 1966, 6),
              ('Congress passed the Equal Rights Amendment', 1972, 3), ('the Roe v. Wade ruling was given', 1973, 1), ('the deadline for ratifying the ERA expired', 1982, 6)],
    'mcq': [
        ('Which part of the Civil Rights Act of 1964 banned employment discrimination on grounds of sex?', 'Title VII', ['Title IX', 'The Nineteenth Amendment', 'The Equal Pay Act'], '[1]'),
        ('Who led the campaign against the Equal Rights Amendment?', 'Phyllis Schlafly', ['Betty Friedan', 'Gloria Steinem', 'Shirley Chisholm'], '[1]'),
        ('Which magazine, founded in 1972, became a voice of the women\'s movement?', 'Ms.', ['Life', 'Time', 'Ebony'], 'Co-founded by Gloria Steinem. [1]'),
    ],
    'why': [
        ('the women\'s movement grew in the 1960s', ['Growing numbers of women in work and higher education', 'The Feminine Mystique voiced suburban dissatisfaction', 'Experience in the civil rights and student movements', 'The contraceptive pill gave women more control', 'Discrimination in pay and jobs'],
         'social change, especially women\'s education and employment, created the conditions, and the civil rights movement provided a model'),
    ],
    'claims': [
        ('The Equal Rights Amendment became part of the Constitution in 1982.', False, 'It fell three states short of ratification.'),
        ('Title IX expanded opportunities for women in college sport.', True, 'Female participation rose sharply.'),
        ('The women\'s movement was united in its aims and methods.', False, 'Liberal feminists, radical feminists and women of colour often disagreed.'),
    ],
    'ess': [
        dict(q='‘The women\'s movement achieved significant change by 1980.’',
             pro=['Laws on equal pay and employment discrimination', 'Roe v. Wade', 'Title IX and more women in higher education and professions'],
             con=['The ERA failed', 'A large pay gap remained', 'A conservative backlash grew in the late 1970s'],
             judge='the movement achieved major legal and social change, but equality in pay and political power remained far off'),
        dict(q='How far was the women\'s movement weakened by its divisions?',
             pro=['Liberal and radical feminists disagreed over aims', 'Many Black and working-class women felt excluded', 'Disputes over abortion and sexuality'],
             con=['The conservative backlash, such as STOP ERA, was a bigger obstacle', 'Diversity allowed the movement to reach different groups', 'It achieved major successes despite divisions'],
             judge='divisions weakened the movement, especially over the ERA, but organised conservative opposition was the main reason for its setbacks'),
    ],
    'src': [
        S('Betty Friedan, The Feminine Mystique, 1963 (summary)', 'Friedan described "the problem that has no name": the sense of emptiness felt by many educated suburban housewives whose lives were confined to home and family.',
          'women\'s lives in the early 1960s', 'It shows that many educated women felt frustrated by the domestic role.',
          'To expose women\'s dissatisfaction and argue for change.', 'it was based on surveys of women and was hugely influential', 'it focused on white, middle-class, educated women',
          'It does not represent working-class or Black women.', stance=None),
        S('a speech by an anti-ERA campaigner, 1977 (illustrative)', 'The ERA will take away a wife\'s right to be supported, send our daughters to war and destroy the family. American women already have more rights than any women in history.',
          'opposition to the ERA', 'It shows conservative women opposed the ERA as a threat to the family.',
          'To win support against ratification.', 'it shows arguments that helped defeat the ERA', 'it exaggerates the effects of the amendment',
          'It does not show the views of feminists.', stance=False, why='it shows the backlash that limited the movement'),
    ],
})

r8d = T('Youth, counterculture and the rise of the New Right', 'youth, counterculture', 'new right')
build_a2(r8d, {
    'enq': 'youth, counterculture and the New Right', 'claim': 'the rise of the New Right was mainly a reaction against the counterculture of the 1960s',
    'stim': ['In 1962 Students for a Democratic Society issued the Port Huron Statement.', 'About 400,000 people attended the Woodstock festival in August 1969.', 'In 1979 Jerry Falwell founded the Moral Majority.'],
    'terms': [
        ('counterculture', 'the youth culture of the 1960s that rejected mainstream values, associated with hippies, rock music and drugs'),
        ('New Left', 'student radicals of the 1960s, such as the SDS, who criticised American society and the Vietnam War'),
        ('New Right', 'the conservative movement of the 1970s and 1980s combining free-market economics with religious and social conservatism'),
        ('Moral Majority', 'the evangelical Christian political organisation founded by Jerry Falwell in 1979'),
        ('silent majority', 'Nixon\'s term of 1969 for the mainstream Americans who did not join protests'),
        ('Port Huron Statement', 'the 1962 manifesto of Students for a Democratic Society'),
    ],
    'dates': [('the SDS issued the Port Huron Statement', 1962, 6), ('the Berkeley Free Speech Movement began', 1964, 9), ('Barry Goldwater won the Republican nomination', 1964, 7),
              ('the Woodstock festival took place', 1969, 8), ('four students were shot at Kent State University', 1970, 5), ('the Moral Majority was founded', 1979)],
    'mcq': [
        ('Whose 1964 presidential campaign is often seen as the start of the modern conservative movement?', 'Barry Goldwater', ['Richard Nixon', 'George Wallace', 'Gerald Ford'], '[1]'),
        ('What happened at Kent State University in May 1970?', 'National Guardsmen shot dead four students during an anti-war protest', ['The Free Speech Movement began', 'The SDS was founded', 'A rock festival was held'], '[1]'),
        ('Which group became central to the New Right in the late 1970s?', 'Evangelical Christians', ['Trade union leaders', 'Student radicals', 'Black Power activists'], '[1]'),
    ],
    'why': [
        ('the New Right grew in the 1970s', ['Reaction against the counterculture, permissiveness and Roe v. Wade', 'Economic problems and resentment of taxes and big government', 'Evangelical Christians became politically organised',
                                             'Opposition to busing and affirmative action', 'Sense of national decline after Vietnam and the Iran hostage crisis'],
         'social and religious reaction against the 1960s combined with economic discontent to build a broad conservative coalition'),
    ],
    'claims': [
        ('Most young Americans in the 1960s were hippies.', False, 'The counterculture involved a minority; many young people were conservative or apolitical.'),
        ('The New Right helped Reagan win the presidency in 1980.', True, 'Evangelicals and economic conservatives formed part of his coalition.'),
        ('The Port Huron Statement was a conservative manifesto.', False, 'It was a New Left statement calling for participatory democracy.'),
    ],
    'ess': [
        dict(q='‘The rise of the New Right was mainly a reaction against the counterculture of the 1960s.’',
             pro=['Evangelicals opposed permissiveness, drugs and sexual liberation', 'Nixon appealed to the silent majority against protesters', 'Opposition to Roe v. Wade and the ERA'],
             con=['Economic problems of the 1970s drove support for tax cuts', 'Opposition to busing and racial change', 'Foreign policy humiliations such as Vietnam and Iran'],
             judge='reaction against the 1960s gave the New Right its moral energy, but economic discontent broadened its appeal'),
        dict(q='How far did the counterculture change American society?',
             pro=['Attitudes to sex, dress and music changed', 'Opposition to the Vietnam War grew', 'Environmental and other movements drew on it'],
             con=['It involved a minority of young people', 'It provoked a conservative backlash', 'Mainstream values of work and family remained strong'],
             judge='it changed culture and attitudes permanently, but it did not transform political or economic structures and provoked a powerful reaction'),
    ],
    'src': [
        S('the Port Huron Statement, 1962 (abridged)', 'We are people of this generation, bred in at least modest comfort, housed now in universities, looking uncomfortably to the world we inherit.',
          'student radicalism', 'It shows the unease of privileged young people about American society.',
          'To set out the aims of the SDS.', 'it is the founding statement of the main New Left group', 'it represents a small group of student activists',
          'It does not show the views of most young people.', stance=None),
        S('a letter to a newspaper from a parent in a small town, 1970 (illustrative)', 'We worked hard, served our country and went to church. Now we see students burning flags on television and the courts telling us how to raise our children. Someone has to stand up for decent people.',
          'conservative reactions', 'It suggests that resentment of protests and cultural change drove a conservative backlash.',
          'To express anger at social change.', 'it shows ordinary conservative opinion at the time', 'one letter may not be typical',
          'It does not mention economic concerns.', stance=True, why='it shows reaction against the 1960s'),
    ],
})

CHAPTERS[8] = [r8a, r8b, r8c, r8d]


# ============================================================== CHAPTER 9: The USA 1945-93, politics and the presidency

p9a = T('Truman, Eisenhower and McCarthyism', 'truman, eisenhower', 'mccarthyism')
build_a2(p9a, {
    'enq': 'McCarthyism', 'claim': 'McCarthyism was caused mainly by the international events of the early Cold War',
    'stim': ['In February 1950 Senator Joseph McCarthy claimed to have a list of communists in the State Department.', 'The USSR tested an atomic bomb in August 1949 and China became communist in October 1949.',
             'The Senate censured McCarthy in December 1954.'],
    'terms': [
        ('McCarthyism', 'the use of reckless accusations of communist sympathy, especially by Senator McCarthy in 1950-54'),
        ('HUAC', 'the House Un-American Activities Committee, which investigated alleged communists, including in Hollywood'),
        ('Fair Deal', 'Truman\'s programme of social reforms, many of which Congress rejected'),
        ('Loyalty Program', 'Truman\'s order of 1947 for checks on the loyalty of federal employees'),
        ('Hollywood Ten', 'screenwriters and directors jailed in 1950 for refusing to answer HUAC\'s questions'),
        ('Modern Republicanism', 'Eisenhower\'s acceptance of much of the New Deal combined with balanced budgets'),
    ],
    'dates': [('Truman introduced the federal Loyalty Program', 1947, 3), ('Truman defeated Dewey in the presidential election', 1948, 11), ('Alger Hiss was convicted of perjury', 1950, 1),
              ('McCarthy made his Wheeling speech', 1950, 2.09), ('the Rosenbergs were executed', 1953, 6), ('the Army-McCarthy hearings were televised', 1954, 4), ('the Senate censured McCarthy', 1954, 12)],
    'mcq': [
        ('What brought about McCarthy\'s downfall in 1954?', 'The televised Army-McCarthy hearings', ['His defeat in the 1952 election', 'Truman\'s impeachment of him', 'The end of the Korean War'], '[1]'),
        ('Which 1950 law required communist organisations to register with the government?', 'The McCarran Internal Security Act', ['The Taft-Hartley Act', 'The Employment Act', 'The GI Bill'], 'Passed over Truman\'s veto. [1]'),
        ('Which programme of Eisenhower expanded infrastructure in the 1950s?', 'The Interstate Highway System', ['The Great Society', 'The Fair Deal', 'The New Frontier'], '[1]'),
    ],
    'why': [
        ('McCarthyism gained support in 1950-54', ['Fear after the Soviet atomic bomb and the fall of China in 1949', 'Spy cases such as Hiss and the Rosenbergs', 'The Korean War from 1950', 'Republicans used anti-communism against the Democrats', 'Truman\'s Loyalty Program had already legitimised loyalty checks'],
         'international shocks created fear, which Republicans and McCarthy exploited for political advantage'),
    ],
    'claims': [
        ('McCarthy exposed large numbers of communist spies in the State Department.', False, 'He never proved his main accusations.'),
        ('Truman won the 1948 election despite predictions of defeat.', True, 'He defeated Thomas Dewey.'),
        ('Eisenhower dismantled the New Deal.', False, 'He accepted most of it, extending Social Security.'),
    ],
    'ess': [
        dict(q='‘McCarthyism was caused mainly by the international events of the early Cold War.’',
             pro=['The Soviet bomb and the fall of China in 1949', 'The Korean War', 'Real spy cases fed fear'],
             con=['Republicans used anti-communism for party advantage', 'Truman\'s Loyalty Program and HUAC came before McCarthy', 'Long-standing anti-radicalism in American politics'],
             judge='international events created the climate of fear, but domestic politics explains why it took such an extreme form'),
        dict(q='How far did Eisenhower change the role of the presidency?',
             pro=['He used a "hidden-hand" style of leadership', 'He sent troops to Little Rock', 'He warned of the military-industrial complex'],
             con=['He accepted the New Deal settlement', 'He was reluctant to act on civil rights', 'He was slow to confront McCarthy'],
             judge='Eisenhower consolidated rather than changed the presidency, using its powers cautiously'),
    ],
    'src': [
        S('Joseph McCarthy, speech at Wheeling, West Virginia, February 1950 (summary)', 'McCarthy claimed that he had a list of people in the State Department known to be members of the Communist Party; the number he gave changed in later accounts.',
          'McCarthy\'s accusations', 'It shows McCarthy making dramatic but unproven accusations.',
          'To win attention and attack the Truman administration.', 'it shows how McCarthy began his campaign', 'he could not substantiate his claims and changed the figures',
          'It does not show why people believed him.', stance=None),
        S('a poll report, 1950 (illustrative)', 'Since the news from China and the Soviet bomb, more than half of those asked believe that communists in government are a serious danger to the country.',
          'public fear of communism', 'It suggests international events increased fear of communists at home.',
          'To report public opinion.', 'polls measure opinion at the time', 'the wording of questions shapes the answers',
          'It does not show how politicians used the fear.', stance=True, why='it links fear to international events'),
    ],
})

p9b = T('Kennedy, Johnson and the expansion of federal power', 'kennedy, johnson', 'expansion of federal power')
build_a2(p9b, {
    'enq': 'the Kennedy and Johnson presidencies', 'claim': 'Johnson was a more effective president than Kennedy in domestic policy',
    'stim': ['Kennedy was assassinated in Dallas on 22 November 1963.', 'In 1964 Johnson won the presidential election with about 61 per cent of the popular vote.',
             'In 1964-65 Congress passed the Civil Rights Act, the Voting Rights Act, Medicare and Medicaid.'],
    'terms': [
        ('New Frontier', 'Kennedy\'s domestic programme, much of which was blocked by Congress'),
        ('Gulf of Tonkin Resolution', 'the 1964 resolution giving Johnson power to use force in Vietnam'),
        ('imperial presidency', 'the idea that presidential power had grown beyond constitutional limits'),
        ('conservative coalition', 'the alliance of southern Democrats and Republicans in Congress that blocked reform'),
        ('Elementary and Secondary Education Act', 'the 1965 law giving federal funds to schools in poor areas'),
        ('credibility gap', 'the public distrust of Johnson\'s statements about the Vietnam War'),
    ],
    'dates': [('Kennedy was inaugurated', 1961, 1), ('Kennedy was assassinated', 1963, 11.22), ('Congress passed the Gulf of Tonkin Resolution', 1964, 8),
              ('Johnson won the presidential election', 1964, 11), ('the Immigration and Nationality Act ended national-origin quotas', 1965, 10), ('Johnson announced he would not seek re-election', 1968, 3.31)],
    'mcq': [
        ('Why did Kennedy struggle to pass his domestic programme?', 'The conservative coalition of southern Democrats and Republicans blocked it', ['He did not propose any laws', 'Republicans controlled the presidency', 'The Supreme Court vetoed it'], '[1]'),
        ('Which event in 1968 led Johnson to withdraw from the presidential race?', 'The political impact of the Tet Offensive and his weak showing in the New Hampshire primary', ['His impeachment', 'His defeat by Nixon', 'The end of the Vietnam War'], '[1]'),
        ('Which law of 1965 abolished the national-origin quota system for immigrants?', 'The Immigration and Nationality Act', ['The McCarran Act', 'The Voting Rights Act', 'The Civil Rights Act'], '[1]'),
    ],
    'why': [
        ('Johnson was able to pass so much legislation in 1964-65', ['His skill in managing Congress from years as Senate majority leader', 'Sympathy after Kennedy\'s assassination', 'Large Democratic majorities after the 1964 landslide', 'Pressure from the civil rights movement', 'Economic growth made spending affordable'],
         'Johnson\'s legislative skill combined with exceptional political circumstances in 1964-65'),
    ],
    'claims': [
        ('Kennedy passed the Civil Rights Act before his death.', False, 'He proposed it in 1963; Johnson secured its passage in 1964.'),
        ('Johnson won the 1964 election by a landslide.', True, 'He won about 61 per cent of the vote against Goldwater.'),
        ('The Gulf of Tonkin Resolution increased presidential power over the use of force.', True, 'It allowed Johnson to escalate the war without a declaration.'),
    ],
    'ess': [
        dict(q='‘Johnson was a more effective president than Kennedy in domestic policy.’',
             pro=['Johnson passed the Civil Rights and Voting Rights Acts', 'Medicare, Medicaid and education laws', 'He secured Kennedy\'s tax cut'],
             con=['Kennedy set the agenda and proposed civil rights legislation', 'Johnson\'s programmes were undermined by Vietnam', 'Kennedy had less time and smaller majorities'],
             judge='Johnson was far more effective at turning proposals into law, though Kennedy laid foundations he built on'),
        dict(q='How far did federal power expand under Kennedy and Johnson?',
             pro=['Federal enforcement of civil rights', 'New federal programmes in health, education and poverty', 'Greater presidential power over war'],
             con=['Many programmes relied on states to implement', 'Congress still blocked some measures', 'Growth continued trends from the New Deal'],
             judge='federal power expanded more in these years than at any time since the New Deal'),
    ],
    'src': [
        S('Lyndon Johnson, speech at the University of Michigan, May 1964 (summary)', 'Johnson described a Great Society resting on abundance and liberty for all, demanding an end to poverty and racial injustice.',
          'Johnson\'s aims', 'It shows Johnson\'s ambitious vision of federal reform.',
          'To launch his programme publicly.', 'it is Johnson\'s own statement of aims', 'it is political rhetoric',
          'It does not show what was achieved.', stance=True, why='it shows Johnson\'s broader domestic ambition'),
        S('a memoir by a Kennedy aide, 1965 (illustrative)', 'The President knew what had to be done on civil rights and on poverty. The bills were written; what he lacked was time and the votes in Congress.',
          'Kennedy\'s domestic record', 'It suggests Kennedy prepared the reforms that Johnson passed.',
          'To defend Kennedy\'s reputation.', 'the aide had inside knowledge', 'written soon after the assassination by a loyal admirer',
          'It does not show the role of Johnson\'s skill.', stance=False, why='it credits Kennedy with the agenda'),
    ],
})

p9c = T('Nixon, Watergate and the crisis of the presidency', 'nixon, watergate', 'crisis of the presidency')
build_a2(p9c, {
    'enq': 'Watergate and the presidency', 'claim': 'Watergate permanently weakened the American presidency',
    'stim': ['On 17 June 1972 five men were arrested breaking into the Democratic National Committee offices in the Watergate building.', 'In November 1972 Nixon won 49 states in the presidential election.',
             'Nixon resigned on 9 August 1974.'],
    'terms': [
        ('Watergate', 'the scandal arising from the 1972 break-in and the cover-up by the Nixon administration'),
        ('Saturday Night Massacre', 'the events of October 1973 when Nixon ordered the dismissal of special prosecutor Archibald Cox'),
        ('United States v. Nixon', 'the Supreme Court ruling of July 1974 that Nixon must hand over the White House tapes'),
        ('War Powers Act', 'the 1973 law limiting the president\'s power to commit troops without Congress'),
        ('executive privilege', 'the claimed right of the president to withhold information from Congress and the courts'),
        ('smoking gun tape', 'the recording of June 1972 showing Nixon approved the cover-up'),
    ],
    'dates': [('the Watergate break-in took place', 1972, 6.17), ('Nixon won re-election by a landslide', 1972, 11), ('the Saturday Night Massacre took place', 1973, 10.20),
              ('Congress passed the War Powers Act over Nixon\'s veto', 1973, 11), ('the Supreme Court ordered Nixon to release the tapes', 1974, 7.24), ('Nixon resigned', 1974, 8.09), ('Ford pardoned Nixon', 1974, 9.08)],
    'mcq': [
        ('Which journalists of the Washington Post investigated Watergate?', 'Bob Woodward and Carl Bernstein', ['Walter Cronkite and Edward Murrow', 'Ida Tarbell and Lincoln Steffens', 'Mark Felt and John Dean'], '[1]'),
        ('Why did Nixon resign rather than face impeachment?', 'The release of the tapes destroyed his support in Congress', ['He lost the 1974 election', 'The Supreme Court removed him', 'He was ill'], '[1]'),
        ('Which historian coined the term "the imperial presidency" in 1973?', 'Arthur Schlesinger Jr', ['John Lewis Gaddis', 'Richard Hofstadter', 'Daniel Boorstin'], '[1]'),
    ],
    'why': [
        ('Watergate led to Nixon\'s resignation', ['Investigations by the press, the courts and the Senate', 'The existence of the White House tapes', 'The Supreme Court\'s ruling in United States v. Nixon', 'The loss of support among Republicans in Congress', 'Nixon\'s own decision to cover up the break-in'],
         'the cover-up, exposed by the tapes, destroyed Nixon\'s support and made impeachment certain'),
    ],
    'claims': [
        ('Nixon was impeached and removed from office by the Senate.', False, 'The House Judiciary Committee approved articles of impeachment, but he resigned before a vote.'),
        ('Congress passed laws after Watergate to limit presidential power.', True, 'For example, the War Powers Act and the Budget and Impoundment Control Act.'),
        ('Gerald Ford pardoned Nixon in 1974.', True, 'The pardon damaged Ford\'s popularity.'),
    ],
    'ess': [
        dict(q='‘Watergate permanently weakened the American presidency.’',
             pro=['Congress passed the War Powers Act and the Budget and Impoundment Control Act', 'Public trust in government fell sharply', 'Ford and Carter were weak presidents'],
             con=['Reagan restored presidential authority in the 1980s', 'Presidents continued to use military force without declarations', 'The system showed it could correct abuse'],
             judge='Watergate weakened the presidency in the 1970s, but the effect was not permanent, as Reagan showed'),
        dict(q='How far was Nixon a successful president apart from Watergate?',
             pro=['Détente with the USSR and the opening to China', 'The EPA and environmental laws', 'The end of US ground involvement in Vietnam'],
             con=['The war was extended to Cambodia and Laos', 'Inflation and economic problems', 'His methods and abuse of power'],
             judge='Nixon had real achievements, especially in foreign policy, but his abuses of power define his presidency'),
    ],
    'src': [
        S('Richard Nixon, press conference, November 1973 (abridged)', 'People have got to know whether or not their President is a crook. Well, I\'m not a crook.',
          'Nixon\'s defence', 'Nixon publicly denies wrongdoing.',
          'To restore public confidence.', 'it is Nixon\'s own public statement', 'the tapes later showed he had approved the cover-up',
          'It does not address the evidence against him.', stance=None),
        S('a newspaper editorial, August 1974 (illustrative)', 'The system has worked. A free press, an independent judiciary and a Congress that did its duty have shown that no man, not even a President, is above the law.',
          'the significance of Watergate', 'It suggests Watergate showed the strength of the constitution rather than its weakness.',
          'To reassure readers after the resignation.', 'it shows the mood at the time', 'it is an opinion written in the moment',
          'It does not consider the long-term effects on trust.', stance=False, why='it suggests the presidency was checked, not permanently weakened'),
    ],
})

p9d = T('Carter, Reagan and Bush: conservatism and the presidency, 1977-93', 'carter, reagan and bush', 'conservatism and the presidency')
build_a2(p9d, {
    'enq': 'the presidency 1977-93', 'claim': 'Reagan restored the power and prestige of the presidency',
    'stim': ['In November 1979 Iranian students seized the US embassy in Tehran; 52 Americans were held hostage until January 1981.', 'In 1980 the Iran hostage crisis and high inflation dominated the presidential election campaign.', 'In 1992 Bush lost to Bill Clinton, with Ross Perot winning about 19 per cent of the vote.'],
    'terms': [
        ('Iran hostage crisis', 'the holding of 52 American hostages in Tehran for 444 days, from November 1979 to January 1981'),
        ('Iran-Contra affair', 'the scandal of 1986 over secret arms sales to Iran, with profits used to fund the Contra rebels in Nicaragua'),
        ('Reagan Democrats', 'working-class Democrats who voted for Reagan'),
        ('malaise speech', 'the name given to Carter\'s July 1979 address about a "crisis of confidence"'),
        ('"Read my lips: no new taxes"', 'Bush\'s 1988 campaign pledge, broken by the budget deal of 1990'),
        ('Gulf War', 'the US-led war of 1991 that expelled Iraq from Kuwait'),
    ],
    'dates': [('Carter became president', 1977, 1), ('the Iran hostage crisis began', 1979, 11), ('Reagan defeated Carter', 1980, 11),
              ('the Iran-Contra affair became public', 1986, 11), ('Bush signed a budget deal that raised taxes', 1990, 11), ('the Gulf War took place', 1991, 1), ('Bush lost the presidential election to Clinton', 1992, 11)],
    'mcq': [
        ('Which agreement negotiated by Carter in 1978 brought peace between Egypt and Israel?', 'The Camp David Accords', ['The Helsinki Accords', 'The Oslo Accords', 'The Paris Peace Accords'], '[1]'),
        ('What damaged Reagan\'s reputation in his second term?', 'The Iran-Contra affair', ['Watergate', 'The Bay of Pigs', 'The Tet Offensive'], '[1]'),
        ('Why did Bush lose the 1992 election?', 'Recession, his broken tax pledge and Ross Perot\'s third-party challenge', ['Defeat in the Gulf War', 'Impeachment', 'He did not stand'], '[1]'),
    ],
    'why': [
        ('Carter lost the 1980 election', ['Inflation and unemployment were both high', 'The Iran hostage crisis made him look weak', 'The Soviet invasion of Afghanistan', 'Reagan\'s optimism and communication skills', 'Divisions within the Democratic Party, including Edward Kennedy\'s challenge'],
         'economic failure and the hostage crisis destroyed confidence in Carter, which Reagan exploited'),
    ],
    'claims': [
        ('The Iran hostage crisis lasted 444 days.', True, 'The hostages were released on 20 January 1981, the day of Reagan\'s inauguration.'),
        ('Reagan was impeached over Iran-Contra.', False, 'He was not impeached, though several officials were prosecuted.'),
        ('Bush kept his pledge never to raise taxes.', False, 'He agreed to tax rises in the 1990 budget deal.'),
    ],
    'ess': [
        dict(q='‘Reagan restored the power and prestige of the presidency.’',
             pro=['He won landslides in 1980 and 1984', 'He passed major tax cuts and set the political agenda', 'His communication skills restored public confidence'],
             con=['Iran-Contra showed abuse of power', 'Congress remained Democratic in the House and limited him', 'Deficits and scandals'],
             judge='Reagan restored confidence in the presidency after the 1970s, though Iran-Contra showed the risks of its power'),
        dict(q='How far did conservatism dominate American politics, 1977-93?',
             pro=['Reagan won two landslides and Bush won in 1988', 'Tax cuts and deregulation reshaped policy', 'The New Right grew in influence'],
             con=['Democrats controlled the House throughout', 'Social Security and Medicare remained', 'Clinton won in 1992'],
             judge='conservatism dominated the presidency and the political agenda, but not the whole system'),
    ],
    'src': [
        S('Jimmy Carter, televised address, July 1979 (abridged)', 'It is a crisis of confidence. It is a crisis that strikes at the very heart and soul and spirit of our national will.',
          'Carter\'s leadership', 'Carter argues the nation faces a crisis of confidence.',
          'To rally the nation behind his energy programme.', 'it is the president\'s own analysis', 'many saw it as blaming the public, which damaged him',
          'It does not show his achievements.', stance=False, why='it shows the presidency appearing weak before Reagan'),
        S('a political commentator, 1985 (illustrative)', 'Whatever one thinks of his policies, the President has made Americans feel good about their country again. The office no longer looks too big for the man.',
          'Reagan\'s presidency', 'It suggests Reagan restored the prestige of the presidency.',
          'To assess Reagan\'s first term.', 'it reflects opinion after the 1984 landslide', 'it was written before Iran-Contra',
          'It does not consider the deficit or scandals.', stance=True, why='it shows restored prestige'),
    ],
})

CHAPTERS[9] = [p9a, p9b, p9c, p9d]


# ============================================================== CHAPTER 10: International history 1909-94, the Cold War in Europe

k10a = T('The division of Europe and the formation of NATO and the Warsaw Pact', 'division of europe', 'nato and the warsaw pact')
build_a2(k10a, {
    'enq': 'the division of Europe', 'claim': 'the Berlin Blockade was the main reason for the division of Europe into two blocs',
    'stim': ['The Berlin Blockade lasted from June 1948 to May 1949.', 'NATO was founded in April 1949 by twelve states.', 'The Warsaw Pact was signed in May 1955, days after West Germany joined NATO.'],
    'terms': [
        ('NATO', 'the North Atlantic Treaty Organization, the Western military alliance founded in 1949'),
        ('Warsaw Pact', 'the military alliance of the USSR and its Eastern European satellites, founded in 1955'),
        ('Comecon', 'the Council for Mutual Economic Assistance, the Soviet bloc\'s economic organisation founded in 1949'),
        ('Berlin airlift', 'the Western supply of West Berlin by air during the blockade of 1948-49'),
        ('Bizonia', 'the merged British and American zones of Germany from 1947'),
        ('Iron Curtain', 'Churchill\'s phrase of 1946 for the division between Soviet-controlled Eastern Europe and the West'),
    ],
    'dates': [('Churchill spoke of an "iron curtain"', 1946, 3), ('the Berlin Blockade began', 1948, 6.24), ('NATO was founded', 1949, 4.04), ('the Federal Republic of Germany was created', 1949, 5),
              ('the German Democratic Republic was created', 1949, 10), ('West Germany joined NATO', 1955, 5.09), ('the Warsaw Pact was signed', 1955, 5.14)],
    'mcq': [
        ('What triggered the Berlin Blockade in June 1948?', 'The introduction of a new currency in the Western zones', ['The founding of NATO', 'The death of Stalin', 'The building of the Berlin Wall'], '[1]'),
        ('Which article of the NATO treaty states that an attack on one member is an attack on all?', 'Article 5', ['Article 10', 'Article 16', 'Article 231'], '[1]'),
        ('What was the immediate trigger for the Warsaw Pact?', 'West Germany\'s entry into NATO', ['The Hungarian Rising', 'The Marshall Plan', 'The Cuban Missile Crisis'], '[1]'),
    ],
    'why': [
        ('Europe was divided into two blocs by 1955', ['Soviet control of Eastern Europe after 1945', 'Disagreements over Germany and reparations', 'The Truman Doctrine and Marshall Plan', 'The Berlin Blockade convinced the West to form NATO', 'West German rearmament led to the Warsaw Pact'],
         'the failure to agree over Germany was at the heart of the division, made permanent by rival alliances'),
    ],
    'claims': [
        ('The Berlin airlift supplied West Berlin for about eleven months.', True, 'From June 1948 to May 1949, and supply flights continued until September.'),
        ('The Warsaw Pact was founded before NATO.', False, 'NATO was founded in 1949, the Warsaw Pact in 1955.'),
        ('Comecon was the Soviet response to the Marshall Plan.', True, 'It was founded in January 1949.'),
    ],
    'ess': [
        dict(q='‘The Berlin Blockade was the main reason for the division of Europe into two blocs.’',
             pro=['It led directly to the formation of NATO', 'It made the division of Germany permanent in 1949', 'It convinced the USA to commit to Western Europe\'s defence'],
             con=['Soviet takeovers in Eastern Europe came earlier', 'The Marshall Plan had already divided Europe economically', 'German rearmament and the Warsaw Pact completed the division in 1955'],
             judge='the blockade turned an economic and political division into a military one, but it was a stage in a process begun in 1945-47'),
        dict(q='How far was the formation of the Warsaw Pact a response to Western actions?',
             pro=['It followed West Germany\'s entry into NATO within days', 'Soviet fear of a rearmed Germany', 'It mirrored NATO'],
             con=['Soviet control of Eastern Europe already existed through bilateral treaties', 'It consolidated Soviet control of its satellites', 'It gave legal cover for Soviet troops in Eastern Europe'],
             judge='it was triggered by West German rearmament, but it mainly formalised Soviet control that already existed'),
    ],
    'src': [
        S('Winston Churchill, speech at Fulton, Missouri, March 1946 (abridged)', 'From Stettin in the Baltic to Trieste in the Adriatic, an iron curtain has descended across the Continent.',
          'the division of Europe', 'Churchill argues that Europe has been divided by Soviet control of the East.',
          'To warn Americans about Soviet expansion and encourage Anglo-American cooperation.', 'Churchill was an experienced statesman', 'he was out of office and wanted to influence US opinion',
          'It does not show Soviet security concerns.', stance=False, why='it shows the division was under way before the blockade'),
        S('a report by a US official in Berlin, 1948 (illustrative)', 'If we leave Berlin, Europe will believe we will leave anywhere. The airlift is the proof that the United States will stay, and our allies now ask for a formal alliance.',
          'the significance of the Berlin crisis', 'It suggests the blockade led the West to seek a formal alliance.',
          'To advise Washington on policy.', 'the official saw events at first hand', 'he had reasons to stress Berlin\'s importance',
          'It does not show Soviet motives.', stance=True, why='it links the blockade to the creation of NATO'),
    ],
})

k10b = T('Crises of the Cold War in Europe: Hungary, Berlin and Czechoslovakia', 'crises of the cold war in europe', 'hungary, berlin and czechoslovakia')
build_a2(k10b, {
    'enq': 'Cold War crises in Europe', 'claim': 'Soviet actions in Hungary in 1956 and Czechoslovakia in 1968 showed the strength of Soviet control over Eastern Europe',
    'stim': ['Soviet tanks entered Budapest on 4 November 1956.', 'The Berlin Wall was built on 13 August 1961.', 'Warsaw Pact forces invaded Czechoslovakia on the night of 20-21 August 1968.'],
    'terms': [
        ('Hungarian Rising', 'the revolt of October-November 1956 against Soviet control, crushed by the Red Army'),
        ('Imre Nagy', 'the Hungarian leader who announced withdrawal from the Warsaw Pact in 1956 and was later executed'),
        ('Berlin Wall', 'the barrier built by East Germany in 1961 to stop emigration to West Berlin'),
        ('Prague Spring', 'the reforms of 1968 under Dubček aiming at "socialism with a human face"'),
        ('Brezhnev Doctrine', 'the Soviet claim of 1968 to intervene where socialism was threatened in another socialist state'),
        ('Khrushchev\'s ultimatum', 'his demand of November 1958 that the Western powers leave West Berlin within six months'),
    ],
    'dates': [('Khrushchev denounced Stalin in his secret speech', 1956, 2), ('Soviet tanks crushed the Hungarian Rising', 1956, 11.04), ('Khrushchev issued his Berlin ultimatum', 1958, 11),
              ('the Berlin Wall was built', 1961, 8.13), ('Kennedy gave his "Ich bin ein Berliner" speech', 1963, 6), ('Dubček became leader of Czechoslovakia', 1968, 1), ('Warsaw Pact forces invaded Czechoslovakia', 1968, 8.20)],
    'mcq': [
        ('Why did the USSR intervene in Hungary in November 1956?', 'Nagy announced Hungary would leave the Warsaw Pact', ['Hungary had invaded Austria', 'NATO troops had entered Hungary', 'Nagy had asked for Soviet help'], '[1]'),
        ('Why was the Berlin Wall built?', 'To stop East Germans escaping to the West through West Berlin', ['To keep NATO troops out of East Germany', 'To mark the end of the blockade', 'Because the West demanded it'], 'About 2.7 million had left from 1949 to 1961. [1]'),
        ('How did Czechoslovaks mainly resist the invasion of 1968?', 'Through passive, non-violent resistance', ['Through a full-scale war', 'By joining NATO', 'By electing a new government that left the Warsaw Pact'], '[1]'),
    ],
    'why': [
        ('the West did not intervene in Hungary in 1956', ['Hungary was within the Soviet sphere and intervention risked nuclear war', 'Britain and France were distracted by the Suez crisis', 'The USA had no means of intervening militarily', 'The UN could only condemn'],
         'the risk of war with the USSR in its own sphere meant the West would not act, whatever its rhetoric'),
        ('the Berlin Wall was built in 1961', ['Mass emigration was draining East Germany of skilled workers', 'Khrushchev\'s attempts to force the West out of Berlin had failed', 'The Wall was an alternative to war', 'Kennedy had signalled he would defend only West Berlin'],
         'the Wall solved the refugee crisis without challenging the Western presence, avoiding war'),
    ],
    'claims': [
        ('The West sent troops to support the Hungarian Rising.', False, 'The West gave no military help.'),
        ('Romania refused to take part in the invasion of Czechoslovakia in 1968.', True, 'Ceaușescu condemned it.'),
        ('Dubček planned to take Czechoslovakia out of the Warsaw Pact.', False, 'Unlike Nagy, he promised to stay in the Pact.'),
    ],
    'ess': [
        dict(q='‘Soviet actions in Hungary in 1956 and Czechoslovakia in 1968 showed the strength of Soviet control over Eastern Europe.’',
             pro=['Both reform movements were crushed', 'The West did not intervene', 'The Brezhnev Doctrine asserted the right to intervene'],
             con=['The need for force showed the regimes lacked popular support', 'Opposition revived, as in Poland', 'The invasions damaged Soviet prestige and split communist parties'],
             judge='they showed the USSR\'s military power to maintain control, but also the weakness of its legitimacy'),
        dict(q='How far did the building of the Berlin Wall reduce tension in Europe?',
             pro=['It ended the refugee crisis', 'It removed Khrushchev\'s motive for ultimatums', 'Berlin was less of a flashpoint after 1962'],
             con=['The tank stand-off at Checkpoint Charlie in October 1961', 'It became a symbol of Cold War division', 'Shootings at the Wall caused continuing anger'],
             judge='the Wall reduced the risk of war over Berlin, though it became the most visible symbol of division'),
    ],
    'src': [
        S('Imre Nagy, radio broadcast, 4 November 1956 (translated, abridged)', 'Today at daybreak Soviet troops attacked our capital with the obvious intention of overthrowing the legal Hungarian democratic government.',
          'the Soviet invasion of Hungary', 'Nagy reports the Soviet attack and appeals for support.',
          'To inform the world and appeal for help.', 'it is the words of the Hungarian leader at the time', 'it was a desperate appeal for support',
          'It does not show Soviet reasons.', stance=True, why='it shows the USSR using force to keep control'),
        S('a letter from a Czechoslovak student, August 1968 (illustrative)', 'They have tanks but no one will speak to them. We take down the street signs and paint "Go home" on the walls. They control the streets but not our minds.',
          'resistance to the invasion', 'It suggests the invasion achieved military control but not popular support.',
          'To describe the invasion to a friend abroad.', 'it is a first-hand account', 'it shows one young person\'s view',
          'It does not show the later "normalisation".', stance=False, why='it suggests Soviet control rested on force, not consent'),
    ],
})

k10c = T('Détente and its collapse, 1969-85', 'détente', 'collapse, 1969-85')
build_a2(k10c, {
    'enq': 'détente', 'claim': 'détente collapsed mainly because of the Soviet invasion of Afghanistan',
    'stim': ['In May 1972 Nixon and Brezhnev signed the SALT I agreements in Moscow.', 'The Helsinki Final Act was signed in August 1975.', 'Soviet forces invaded Afghanistan in December 1979.'],
    'terms': [
        ('détente', 'the easing of tension between the superpowers in the late 1960s and 1970s'),
        ('Ostpolitik', 'West German Chancellor Willy Brandt\'s policy of improving relations with Eastern Europe'),
        ('SALT I', 'the Strategic Arms Limitation agreements of 1972, including the ABM Treaty'),
        ('Helsinki Final Act', 'the 1975 agreement accepting European borders and including commitments to human rights'),
        ('SDI', 'the Strategic Defense Initiative announced by Reagan in 1983, a planned defence against missiles'),
        ('Second Cold War', 'the period of renewed tension from 1979 to about 1985'),
    ],
    'dates': [('the Moscow Treaty between West Germany and the USSR was signed', 1970, 8), ('SALT I was signed', 1972, 5), ('the Helsinki Final Act was signed', 1975, 8),
              ('SALT II was signed', 1979, 6), ('the USSR invaded Afghanistan', 1979, 12), ('Reagan announced the Strategic Defense Initiative', 1983, 3)],
    'mcq': [
        ('Why was SALT II never ratified by the US Senate?', 'Carter withdrew it after the Soviet invasion of Afghanistan', ['The USSR refused to sign it', 'It was signed after Reagan took office', 'NATO opposed it'], '[1]'),
        ('Which part of the Helsinki Final Act caused most difficulty for Soviet bloc governments?', 'The commitment to human rights', ['The recognition of borders', 'Trade agreements', 'Scientific cooperation'], 'Groups such as Charter 77 used it. [1]'),
        ('Which Polish trade union challenged communist rule from 1980?', 'Solidarity', ['Comecon', 'Cominform', 'Charter 77'], '[1]'),
    ],
    'why': [
        ('détente developed in the late 1960s and early 1970s', ['Nuclear parity made arms control attractive', 'The cost of the arms race', 'The USA wanted to leave Vietnam', 'The USSR wanted Western trade and technology', 'Ostpolitik eased tension in Germany'],
         'mutual interest in reducing the risks and costs of confrontation drove détente'),
    ],
    'claims': [
        ('The Helsinki Final Act accepted the post-war borders of Europe.', True, 'This was a key Soviet aim.'),
        ('Reagan called the USSR an "evil empire" in 1983.', True, 'In a speech in March 1983.'),
        ('SALT I banned all nuclear weapons.', False, 'It limited some strategic weapons and anti-ballistic missile systems.'),
    ],
    'ess': [
        dict(q='‘Détente collapsed mainly because of the Soviet invasion of Afghanistan.’',
             pro=['Carter withdrew SALT II and imposed sanctions', 'The US boycotted the 1980 Moscow Olympics', 'It convinced Western leaders the USSR was expansionist'],
             con=['Détente was already weakened by Soviet actions in Africa and SS-20 deployments', 'US domestic criticism of détente and human rights concerns', 'Reagan\'s election and military build-up'],
             judge='Afghanistan was the decisive blow, but détente was already failing because each side saw it differently'),
        dict(q='How far did détente achieve its aims?',
             pro=['Arms control agreements such as SALT I', 'Recognition of borders and improved relations in Germany', 'Reduced risk of war in the 1970s'],
             con=['The arms race continued in other weapons', 'Competition in the Third World continued', 'It collapsed by 1980'],
             judge='détente achieved stability in Europe and some arms control, but not a lasting end to rivalry'),
    ],
    'src': [
        S('Ronald Reagan, speech to the National Association of Evangelicals, March 1983 (summary)', 'Reagan described the Soviet Union as an "evil empire" and warned against a nuclear freeze that would leave the USA weaker.',
          'the Second Cold War', 'It shows Reagan rejecting détente in favour of confrontation.',
          'To win support for his defence policies.', 'it is the president\'s own words', 'it was a speech to a sympathetic audience',
          'It does not show the effect of Afghanistan.', stance=False, why='it shows US policy changes as a cause of the end of détente'),
        S('a statement by President Carter, January 1980 (summary)', 'Carter called the Soviet invasion of Afghanistan the greatest threat to peace since the Second World War and announced sanctions and the withdrawal of SALT II from the Senate.',
          'the end of détente', 'It shows Carter abandoning détente because of Afghanistan.',
          'To announce and justify the US response.', 'it is the official US response at the time', 'it was also shaped by election-year politics',
          'It does not show earlier problems with détente.', stance=True, why='it links the collapse of détente to Afghanistan'),
    ],
})

k10d = T('Gorbachev and the end of the Cold War, 1985-91', 'gorbachev', 'end of the cold war')
build_a2(k10d, {
    'enq': 'the end of the Cold War', 'claim': 'Gorbachev was the main reason for the end of the Cold War',
    'stim': ['Gorbachev became General Secretary of the Soviet Communist Party in March 1985.', 'The Berlin Wall was opened on 9 November 1989.', 'The Soviet Union was dissolved in December 1991.'],
    'terms': [
        ('glasnost', 'openness, Gorbachev\'s policy of allowing freer discussion and criticism'),
        ('perestroika', 'restructuring, Gorbachev\'s attempt to reform the Soviet economy'),
        ('Sinatra Doctrine', 'the 1989 Soviet policy of letting Eastern European states "do it their way"'),
        ('INF Treaty', 'the 1987 treaty eliminating US and Soviet intermediate-range nuclear missiles'),
        ('Reykjavik summit', 'the 1986 meeting at which Reagan and Gorbachev discussed abolishing nuclear weapons'),
        ('August coup', 'the failed attempt by Soviet hardliners to overthrow Gorbachev in August 1991'),
    ],
    'dates': [('Gorbachev became Soviet leader', 1985, 3), ('the Reykjavik summit was held', 1986, 10), ('the INF Treaty was signed', 1987, 12), ('Soviet forces completed their withdrawal from Afghanistan', 1989, 2),
              ('the Berlin Wall was opened', 1989, 11.09), ('Germany was reunified', 1990, 10.03), ('the Soviet Union was dissolved', 1991, 12)],
    'mcq': [
        ('In which country were semi-free elections held in June 1989, won heavily by Solidarity?', 'Poland', ['Hungary', 'East Germany', 'Romania'], '[1]'),
        ('What did Gorbachev announce in his speech to the UN in December 1988?', 'A unilateral cut of 500,000 Soviet troops', ['The invasion of Poland', 'The building of new missiles', 'The end of glasnost'], '[1]'),
        ('Which Eastern European revolution of 1989 was the most violent?', 'Romania', ['Czechoslovakia', 'Poland', 'Hungary'], 'Ceaușescu was executed in December 1989. [1]'),
    ],
    'why': [
        ('the Cold War ended by 1991', ['Gorbachev\'s reforms and refusal to use force in Eastern Europe', 'The Soviet economy was in crisis and could not sustain the arms race', 'Reagan\'s military build-up and SDI put pressure on the USSR',
                                        'Popular movements in Eastern Europe, such as Solidarity', 'The war in Afghanistan drained Soviet resources'],
         'Soviet economic decline made change necessary, but Gorbachev\'s choices determined that it ended peacefully'),
    ],
    'claims': [
        ('Gorbachev used force to prevent the fall of the Berlin Wall.', False, 'He refused to intervene.'),
        ('The INF Treaty eliminated a whole class of nuclear weapons.', True, 'It removed intermediate-range missiles.'),
        ('Gorbachev intended to dissolve the Soviet Union.', False, 'He wanted to reform and preserve it.'),
    ],
    'ess': [
        dict(q='‘Gorbachev was the main reason for the end of the Cold War.’',
             pro=['His new thinking in foreign policy and arms control', 'He refused to use force in 1989', 'Glasnost undermined communist control'],
             con=['The Soviet economy was failing', 'Reagan\'s pressure and his willingness to negotiate', 'Popular movements in Eastern Europe'],
             judge='structural decline made change unavoidable, but Gorbachev\'s choices were decisive in ending the Cold War peacefully'),
        dict(q='How far did Reagan\'s policies cause the end of the Cold War?',
             pro=['The arms build-up and SDI strained the USSR', 'Support for anti-Soviet forces such as the Afghan mujahideen', 'His willingness to negotiate with Gorbachev after 1985'],
             con=['Soviet economic problems had deep internal causes', 'Gorbachev took the key decisions', 'Eastern European peoples brought down their own regimes'],
             judge='Reagan contributed through pressure and diplomacy, but the decisive factors were Soviet decline and Gorbachev\'s choices'),
    ],
    'src': [
        S('Gorbachev, speech to the UN General Assembly, December 1988 (summary)', 'Gorbachev said that force was no longer an instrument of foreign policy, that every nation had freedom of choice, and announced unilateral troop cuts.',
          'Gorbachev\'s foreign policy', 'It shows Gorbachev rejecting the use of force and the Brezhnev Doctrine.',
          'To change Western views of the USSR and reduce the burden of defence.', 'it is Gorbachev\'s own policy statement', 'it is a public speech aimed at world opinion',
          'It does not show economic pressures.', stance=True, why='it shows Gorbachev\'s choices driving change'),
        S('a memo by a Soviet economist, 1986 (illustrative)', 'We cannot match the Americans in new weapons and feed our people at the same time. Oil revenue has collapsed. Without reductions in military spending the economy will not survive.',
          'Soviet economic problems', 'It suggests economic crisis forced the USSR to seek an end to the arms race.',
          'To advise the leadership.', 'it shows thinking inside the Soviet system', 'it is one adviser\'s view',
          'It does not show Gorbachev\'s ideas.', stance=False, why='it stresses economic pressures rather than Gorbachev'),
    ],
})

CHAPTERS[10] = [k10a, k10b, k10c, k10d]


# ============================================================== CHAPTER 11: International history 1909-94, South Africa

a11a = T('The origins of apartheid and the National Party victory of 1948', 'origins of apartheid', 'national party victory of 1948')
build_a2(a11a, {
    'enq': 'the origins of apartheid', 'claim': 'the National Party won in 1948 mainly because of Afrikaner nationalism',
    'stim': ['The Natives Land Act of 1913 reserved about 7 per cent of land for Black Africans.', 'The Black urban population grew rapidly during the Second World War.', 'In May 1948 the National Party under D. F. Malan won the general election.'],
    'terms': [
        ('apartheid', 'the system of racial segregation and white minority rule introduced by the National Party from 1948'),
        ('Natives Land Act', 'the law of 1913 restricting Black land ownership to reserves'),
        ('Broederbond', 'the secret Afrikaner nationalist society founded in 1918'),
        ('Afrikaner nationalism', 'the political movement of Afrikaners for power, culture and identity'),
        ('swart gevaar', 'the "black danger", the fear exploited by the National Party in 1948'),
        ('Fagan Report', 'the 1948 report that accepted Black urbanisation as permanent'),
    ],
    'dates': [('the Union of South Africa was formed', 1910, 5), ('the Natives Land Act was passed', 1913), ('the Broederbond was founded', 1918), ('the centenary of the Great Trek was celebrated', 1938), ('the National Party won the general election', 1948, 5)],
    'mcq': [
        ('How did the National Party win in 1948 despite gaining fewer votes than the United Party?', 'The electoral system favoured rural constituencies', ['Black South Africans voted for it', 'The British government appointed it', 'The United Party did not stand'], '[1]'),
        ('Who led the National Party to victory in 1948?', 'D. F. Malan', ['Jan Smuts', 'Hendrik Verwoerd', 'P. W. Botha'], '[1]'),
        ('Which party did Jan Smuts lead in 1948?', 'The United Party', ['The National Party', 'The ANC', 'The Labour Party'], '[1]'),
    ],
    'why': [
        ('the National Party won the 1948 election', ['Afrikaner nationalism had been strengthened by the Broederbond and the 1938 centenary', 'White fears of Black urbanisation during the war', 'Smuts\'s United Party seemed to have no clear policy', 'The electoral system gave extra weight to rural seats', 'White workers feared competition for jobs'],
         'Afrikaner nationalism combined with white fears of Black urbanisation, helped by the electoral system'),
    ],
    'claims': [
        ('Racial segregation began only in 1948.', False, 'Segregation laws such as the 1913 Natives Land Act long preceded apartheid.'),
        ('The National Party won more seats but fewer votes than the United Party in 1948.', True, 'Rural seats had fewer voters.'),
        ('Black South Africans could vote in the 1948 general election in the Transvaal.', False, 'Black Africans had no vote there; the electorate was overwhelmingly white.'),
    ],
    'ess': [
        dict(q='‘The National Party won in 1948 mainly because of Afrikaner nationalism.’',
             pro=['Afrikaner cultural and political mobilisation', 'The Broederbond organised support', 'Resentment of British influence and the war'],
             con=['White fears of Black urbanisation (swart gevaar)', 'The weakness of the United Party', 'The electoral system'],
             judge='Afrikaner nationalism provided the core vote, but fear of Black urbanisation and the electoral system gave the Nationalists victory'),
        dict(q='How far was apartheid a continuation of earlier segregation?',
             pro=['Land segregation dated from 1913', 'Pass laws and job reservation existed before 1948', 'Black Africans already lacked political rights in most areas'],
             con=['Apartheid was more systematic and ideological', 'It classified the whole population by race', 'It removed the remaining rights of Coloured voters'],
             judge='apartheid built on earlier segregation, but its systematic racial classification made it a new and harsher system'),
    ],
    'src': [
        S('a National Party election statement, 1948 (summary)', 'The party warned that the white race faced being swamped by the Black majority and promised apartheid to keep the races separate and protect white jobs.',
          'the 1948 election', 'It shows the party appealing to white fears and promising separation.',
          'To win white votes.', 'it shows the party\'s own message', 'it is election propaganda',
          'It does not show Afrikaner cultural motives.', stance=False, why='it stresses white fear of Black urbanisation'),
        S('a speech at the Great Trek centenary, 1938 (illustrative)', 'One hundred years ago our fathers went into the wilderness to be free. Today the volk must again unite to take its rightful place in its own land.',
          'Afrikaner nationalism', 'It shows the strength of Afrikaner nationalist feeling.',
          'To inspire Afrikaner unity.', 'it shows the mood of the centenary', 'it is rhetoric for a celebration',
          'It does not show how people voted in 1948.', stance=True, why='it shows Afrikaner nationalism'),
    ],
})

a11b = T('The implementation of apartheid and resistance: ANC, Sharpeville and Soweto', 'implementation of apartheid', 'sharpeville', 'soweto')
build_a2(a11b, {
    'enq': 'apartheid and resistance', 'claim': 'Sharpeville was the turning point in resistance to apartheid',
    'stim': ['The Population Registration Act of 1950 classified every South African by race.', 'On 21 March 1960 police at Sharpeville opened fire on a crowd protesting against the pass laws, killing 69 people.',
             'On 16 June 1976 school students in Soweto protested against teaching in Afrikaans.'],
    'terms': [
        ('Population Registration Act', 'the 1950 law classifying all South Africans by race'),
        ('Group Areas Act', 'the 1950 law assigning residential areas to racial groups'),
        ('Bantu Education Act', 'the 1953 law creating a separate, inferior education system for Black Africans'),
        ('Freedom Charter', 'the statement of principles adopted by the Congress of the People at Kliptown in 1955'),
        ('Umkhonto we Sizwe', 'the armed wing of the ANC, formed in 1961'),
        ('Black Consciousness', 'the movement led by Steve Biko stressing Black self-reliance and pride'),
        ('bantustans', 'the homelands set aside for Black Africans, some declared "independent"'),
    ],
    'dates': [('the Population Registration Act was passed', 1950), ('the Defiance Campaign began', 1952, 6), ('the Freedom Charter was adopted', 1955, 6), ('the Sharpeville shootings took place', 1960, 3.21),
              ('Umkhonto we Sizwe was formed', 1961, 12), ('Mandela was sentenced to life imprisonment at the Rivonia Trial', 1964, 6), ('the Soweto uprising began', 1976, 6.16)],
    'mcq': [
        ('Which organisation called the protest at Sharpeville in 1960?', 'The Pan Africanist Congress', ['The ANC', 'The United Democratic Front', 'The Black Consciousness Movement'], '[1]'),
        ('What happened to the ANC and PAC after Sharpeville?', 'They were banned', ['They were invited into government', 'They merged with the National Party', 'They won seats in parliament'], '[1]'),
        ('Which Black Consciousness leader died in police custody in 1977?', 'Steve Biko', ['Nelson Mandela', 'Oliver Tambo', 'Walter Sisulu'], '[1]'),
    ],
    'why': [
        ('the ANC turned to armed struggle in 1961', ['Peaceful protest had met violent repression, as at Sharpeville', 'The ANC was banned in 1960, closing legal routes', 'Leaders such as Mandela believed non-violence had failed', 'The government declared a republic in 1961 without consulting Black people'],
         'the banning of the ANC and the violence of the state convinced its leaders that non-violence alone could not succeed'),
    ],
    'claims': [
        ('The Freedom Charter declared that South Africa belongs to all who live in it, black and white.', True, 'It was adopted in 1955.'),
        ('The Soweto uprising began as a protest against teaching in Afrikaans.', True, 'Students marched on 16 June 1976.'),
        ('Mandela was released after the Rivonia Trial.', False, 'He was sentenced to life imprisonment and released only in 1990.'),
    ],
    'ess': [
        dict(q='‘Sharpeville was the turning point in resistance to apartheid.’',
             pro=['It led to the banning of the ANC and PAC', 'It led the ANC to turn to armed struggle', 'It brought international condemnation'],
             con=['Resistance was crushed for over a decade afterwards', 'Soweto in 1976 revived mass resistance', 'The 1980s township revolt and the UDF did more to weaken apartheid'],
             judge='Sharpeville changed the methods of resistance, but Soweto marked the real revival of mass opposition'),
        dict(q='How effective was resistance to apartheid in the period 1948-76?',
             pro=['The Defiance Campaign and Freedom Charter built mass support', 'International opinion turned against South Africa', 'Soweto showed the regime could not control the young'],
             con=['The state banned organisations and imprisoned leaders', 'Armed struggle achieved little militarily', 'Apartheid was extended in these years'],
             judge='resistance kept opposition alive and won international support, but it could not stop the extension of apartheid before 1976'),
    ],
    'src': [
        S('Nelson Mandela, statement from the dock at the Rivonia Trial, April 1964 (abridged)', 'I have cherished the ideal of a democratic and free society in which all persons live together in harmony and with equal opportunities. It is an ideal which I hope to live for and to achieve. But if needs be, it is an ideal for which I am prepared to die.',
          'the aims of the ANC', 'Mandela states his commitment to a democratic, non-racial society.',
          'To explain his actions and reach a wider audience.', 'it is Mandela\'s own statement', 'it was made at a trial in which he faced a possible death sentence',
          'It does not show the effectiveness of the armed struggle.', stance=None),
        S('a report by a foreign journalist, 1976 (illustrative)', 'The students marched singing, carrying placards. When the police fired, the protest spread across the township and then the country. Something has changed: the young are no longer afraid.',
          'the Soweto uprising', 'It suggests Soweto marked a new phase of mass resistance.',
          'To report events abroad.', 'it is an eyewitness account', 'a journalist may dramatise events',
          'It does not show the role of Sharpeville.', stance=False, why='it suggests Soweto, not Sharpeville, revived resistance'),
    ],
})

a11c = T("Botha's Total Strategy and why it failed", "botha's total strategy", 'why it failed')
build_a2(a11c, {
    'enq': 'Botha\'s Total Strategy', 'claim': 'Botha\'s Total Strategy failed mainly because of internal resistance',
    'stim': ['P. W. Botha became prime minister in 1978.', 'The 1983 constitution created a Tricameral Parliament with houses for White, Coloured and Indian voters.', 'A state of emergency was declared in 1985.'],
    'terms': [
        ('Total Strategy', 'Botha\'s policy of combining limited reform with security measures against a perceived "total onslaught"'),
        ('total onslaught', 'the government\'s claim that South Africa faced a communist-inspired attack from inside and outside'),
        ('Tricameral Parliament', 'the parliament of 1984 with separate houses for White, Coloured and Indian South Africans, excluding Black Africans'),
        ('UDF', 'the United Democratic Front, the coalition of anti-apartheid groups formed in 1983'),
        ('Rubicon speech', 'Botha\'s speech of August 1985 in which he failed to announce expected reforms'),
        ('disinvestment', 'the withdrawal of foreign investment from South Africa'),
    ],
    'dates': [('Botha became prime minister', 1978, 9), ('the United Democratic Front was formed', 1983, 8), ('the Tricameral Parliament was introduced', 1984), ('Botha gave his Rubicon speech', 1985, 8),
              ('the pass laws were abolished', 1986, 7), ('the US Congress passed the Comprehensive Anti-Apartheid Act over Reagan\'s veto', 1986, 10)],
    'mcq': [
        ('Which group was excluded from the Tricameral Parliament?', 'Black Africans', ['Indians', 'Coloureds', 'Whites'], '[1]'),
        ('What was the effect of the Rubicon speech of 1985?', 'Foreign banks refused to roll over loans and the rand collapsed', ['Apartheid ended immediately', 'Mandela was released', 'Sanctions were lifted'], '[1]'),
        ('Which of these was a reform under Botha?', 'The abolition of the pass laws in 1986', ['The release of Mandela', 'Universal suffrage', 'The unbanning of the ANC'], '[1]'),
    ],
    'why': [
        ('Botha\'s Total Strategy failed', ['Reforms were too limited and provoked resistance, as with the Tricameral Parliament', 'The UDF and township revolt made areas ungovernable', 'International sanctions and disinvestment damaged the economy', 'The cost of military action in Angola and the region', 'Botha\'s refusal to share power with the Black majority'],
         'reform without power-sharing satisfied no one, provoking internal resistance that repression and the economy could not contain'),
    ],
    'claims': [
        ('Botha released Mandela in 1985.', False, 'Botha offered release on conditions Mandela rejected; Mandela was released in 1990 under de Klerk.'),
        ('States of emergency were declared in 1985 and 1986.', True, 'Thousands were detained.'),
        ('The UDF brought together hundreds of anti-apartheid organisations.', True, 'It was formed in 1983.'),
    ],
    'ess': [
        dict(q='‘Botha\'s Total Strategy failed mainly because of internal resistance.’',
             pro=['The township revolt of 1984-86', 'The UDF and trade unions such as COSATU', 'Resistance made reform impossible to control'],
             con=['International sanctions and disinvestment', 'The economic crisis', 'The end of the Cold War removed the "communist threat" argument'],
             judge='internal resistance was the main reason, though international pressure and economic decline made it impossible to sustain'),
        dict(q='How far did Botha reform apartheid?',
             pro=['Pass laws and the ban on mixed marriages were abolished', 'Black trade unions were recognised', 'The Tricameral Parliament gave some representation to Coloureds and Indians'],
             con=['Black Africans had no political rights', 'Repression increased under states of emergency', 'Residential segregation remained'],
             judge='Botha reformed aspects of petty apartheid but not its core of white political power'),
    ],
    'src': [
        S('P. W. Botha, speech, 1979 (summary)', 'Botha warned that white South Africans must "adapt or die", arguing that some reform was needed to survive.',
          'Botha\'s strategy', 'It shows Botha accepting limited reform as necessary for survival.',
          'To prepare white voters for change.', 'it is Botha\'s own words', 'it was rhetoric and the reforms were limited',
          'It does not show resistance.', stance=None),
        S('a UDF pamphlet, 1984 (illustrative)', 'The new constitution offers us nothing. We will not vote for apartheid\'s parliament. Make the townships ungovernable!',
          'resistance to the Tricameral Parliament', 'It shows mass rejection of Botha\'s reforms.',
          'To mobilise resistance.', 'it shows the UDF\'s message at the time', 'it is a campaigning document',
          'It does not show international pressure.', stance=True, why='it shows internal resistance defeating reform'),
    ],
})

a11d = T('The end of apartheid and the transition to majority rule, 1989-94', 'end of apartheid', 'transition to majority rule')
build_a2(a11d, {
    'enq': 'the end of apartheid', 'claim': 'de Klerk was the main reason for the end of apartheid',
    'stim': ['On 2 February 1990 President de Klerk announced the unbanning of the ANC.', 'Nelson Mandela was released from prison on 11 February 1990.', 'South Africa\'s first democratic elections were held in April 1994.'],
    'terms': [
        ('CODESA', 'the Convention for a Democratic South Africa, the negotiations that began in December 1991'),
        ('Record of Understanding', 'the agreement of September 1992 between the government and the ANC that restarted negotiations'),
        ('Inkatha Freedom Party', 'the Zulu-based party led by Mangosuthu Buthelezi, involved in violent conflict with the ANC'),
        ('Government of National Unity', 'the coalition government formed after the 1994 elections'),
        ('sunset clauses', 'the compromise of 1992 guaranteeing power-sharing and job security for officials for a transitional period'),
        ('whites-only referendum', 'the vote of March 1992 in which about 69 per cent of white voters supported negotiations'),
    ],
    'dates': [('de Klerk became president', 1989, 9), ('the ANC was unbanned', 1990, 2.02), ('Mandela was released from prison', 1990, 2.11), ('CODESA negotiations began', 1991, 12),
              ('the whites-only referendum supported reform', 1992, 3), ('Chris Hani was assassinated', 1993, 4), ('the first democratic elections were held', 1994, 4.27)],
    'mcq': [
        ('What share of the vote did the ANC win in the 1994 elections?', 'About 63 per cent', ['About 33 per cent', 'About 90 per cent', 'About 50 per cent'], '[1]'),
        ('Who shared the Nobel Peace Prize with Mandela in 1993?', 'F. W. de Klerk', ['P. W. Botha', 'Desmond Tutu', 'Mangosuthu Buthelezi'], '[1]'),
        ('Why did the assassination of Chris Hani in 1993 matter?', 'Mandela\'s appeal for calm helped push negotiations to set an election date', ['It ended negotiations permanently', 'It caused the ANC to leave the talks for good', 'It led to the return of Botha'], '[1]'),
    ],
    'why': [
        ('de Klerk unbanned the ANC in 1990', ['The economy was damaged by sanctions and resistance', 'The end of the Cold War removed the communist threat argument', 'Internal resistance had made repression too costly', 'He believed whites could negotiate a better deal while still strong', 'Secret talks with Mandela had shown that negotiation was possible'],
         'de Klerk acted because apartheid had become unsustainable, and the end of the Cold War gave him the opportunity'),
    ],
    'claims': [
        ('Mandela became president after the 1994 elections.', True, 'He was inaugurated on 10 May 1994.'),
        ('The transition to democracy was entirely peaceful.', False, 'Thousands died in political violence, especially between ANC and Inkatha supporters.'),
        ('The whites-only referendum of 1992 rejected negotiations.', False, 'About 69 per cent voted yes.'),
    ],
    'ess': [
        dict(q='‘De Klerk was the main reason for the end of apartheid.’',
             pro=['He unbanned the ANC and released Mandela', 'He won the 1992 referendum', 'He negotiated the transition'],
             con=['Internal resistance had made apartheid unworkable', 'Sanctions and economic decline', 'Mandela\'s leadership kept negotiations alive'],
             judge='de Klerk took the decisive steps, but he was responding to pressures that made apartheid unsustainable, and Mandela was equally vital'),
        dict(q='How far was the transition to majority rule a negotiated compromise?',
             pro=['Sunset clauses and the Government of National Unity', 'Protection for property and officials', 'Both sides made concessions at CODESA'],
             con=['The ANC achieved majority rule', 'Violence shaped negotiations', 'Mass action pushed the government to concede'],
             judge='it was a negotiated compromise in form, but the ANC achieved its central aim of majority rule'),
    ],
    'src': [
        S('F. W. de Klerk, speech at the opening of parliament, 2 February 1990 (summary)', 'De Klerk announced the unbanning of the ANC, PAC and Communist Party and the release of political prisoners, and called for negotiations on a new constitution.',
          'the end of apartheid', 'It shows de Klerk taking the decisive step towards negotiation.',
          'To begin negotiations and win international support.', 'it is the president\'s own announcement', 'it presented the decision as his initiative, not as a response to pressure',
          'It does not show the pressures that led to it.', stance=True, why='it shows de Klerk\'s role'),
        S('a South African businessman, 1989 (illustrative)', 'Sanctions, strikes and the falling rand are bleeding us dry. Business can no longer live with apartheid; we have told the government so.',
          'economic pressures', 'It suggests economic pressure forced change.',
          'To explain business views.', 'it shows business opinion', 'business leaders had their own interests',
          'It does not show de Klerk\'s motives.', stance=False, why='it stresses economic pressure rather than de Klerk'),
    ],
})

CHAPTERS[11] = [a11a, a11b, a11c, a11d]


# ============================================================== CHAPTER 12: International history 1909-94, nationalism and decolonisation in Southeast Asia

e12a = T('Colonial rule and early nationalism in Southeast Asia to 1941', 'colonial rule and early nationalism', 'southeast asia to 1941')
build_a2(e12a, {
    'enq': 'early nationalism in Southeast Asia', 'claim': 'nationalist movements in Southeast Asia were weak before 1941',
    'stim': ['By 1941 every country in Southeast Asia except Siam (Thailand) was under colonial rule.', 'Sukarno founded the Indonesian Nationalist Party (PNI) in 1927.', 'Ho Chi Minh founded the Indochinese Communist Party in 1930.'],
    'terms': [
        ('Budi Utomo', 'the Javanese cultural organisation founded in 1908, often seen as the start of Indonesian nationalism'),
        ('Sarekat Islam', 'the mass Muslim organisation in the Dutch East Indies, founded in 1912'),
        ('PNI', 'the Indonesian Nationalist Party founded by Sukarno in 1927'),
        ('Youth Pledge', 'the 1928 declaration of one motherland, one nation and one language, Indonesia'),
        ('Thakins', 'young Burmese nationalists of the Dobama Asiayone ("We Burmans") movement of the 1930s'),
        ('Tydings-McDuffie Act', 'the US law of 1934 promising the Philippines independence after ten years'),
    ],
    'dates': [('Budi Utomo was founded', 1908), ('Sarekat Islam was founded', 1912), ('the PNI was founded', 1927), ('the Youth Pledge was made', 1928, 10),
              ('the Indochinese Communist Party was founded', 1930, 2), ('the Tydings-McDuffie Act was passed', 1934, 3)],
    'mcq': [
        ('Which Southeast Asian country was never colonised?', 'Siam (Thailand)', ['Burma', 'Malaya', 'Vietnam'], '[1]'),
        ('How did the French respond to the Yen Bai mutiny of 1930?', 'With harsh repression of nationalists', ['By granting independence', 'By holding free elections', 'By leaving Indochina'], '[1]'),
        ('Which colonial power promised independence to its colony in the 1930s?', 'The USA, to the Philippines', ['France, to Vietnam', 'The Netherlands, to Indonesia', 'Britain, to Malaya'], '[1]'),
    ],
    'why': [
        ('nationalist movements had limited success before 1941', ['Colonial powers repressed them, exiling leaders such as Sukarno', 'Ethnic and religious divisions, as in Malaya', 'Nationalism was mainly limited to Western-educated elites', 'Divisions between communists, Islamists and secular nationalists'],
         'colonial repression and internal divisions prevented nationalists from building mass movements before the war'),
    ],
    'claims': [
        ('Sukarno was imprisoned and exiled by the Dutch in the 1930s.', True, 'He was exiled from 1933 until the Japanese invasion.'),
        ('Malayan nationalism was strong and united before 1941.', False, 'Divisions between Malays, Chinese and Indians made it weak.'),
        ('Burma was separated from British India in 1937.', True, 'It gained its own administration.'),
    ],
    'ess': [
        dict(q='‘Nationalist movements in Southeast Asia were weak before 1941.’',
             pro=['Colonial repression in Indonesia and Vietnam', 'Ethnic divisions in Malaya', 'Limited mass support outside the elites'],
             con=['Sarekat Islam had mass membership', 'The Youth Pledge created a sense of Indonesian identity', 'The Philippines won a promise of independence'],
             judge='nationalism had developed ideas and leaders by 1941, but colonial power prevented it from achieving independence'),
        dict(q='How far did colonial rule create the conditions for nationalism in Southeast Asia?',
             pro=['Western education produced nationalist leaders', 'Colonial boundaries defined future nations', 'Economic exploitation created grievances'],
             con=['Religious movements such as Islam provided identity independently', 'Communism came from international influence', 'Traditional resistance to foreign rule existed before'],
             judge='colonial rule shaped the form of nationalism, but religion, international ideas and traditions also mattered'),
    ],
    'src': [
        S('the Youth Pledge, October 1928 (translated)', 'We, the sons and daughters of Indonesia, declare that we belong to one motherland, Indonesia. We declare that we belong to one nation, the Indonesian nation. We uphold the language of unity, the Indonesian language.',
          'Indonesian nationalism', 'It shows young nationalists claiming a single Indonesian identity.',
          'To unite people of different islands and languages.', 'it is the declaration made at the time', 'it shows ideals of an educated youth congress, not mass opinion',
          'It does not show how many Indonesians shared these views.', stance=False, why='it shows nationalism developing a national identity'),
        S('a report by a Dutch colonial official, 1934 (illustrative)', 'The nationalist leaders are in exile and their parties are quiet. The villages are calm; the peasant cares for his rice, not for politics.',
          'nationalism in the Dutch East Indies', 'It suggests nationalism had been suppressed and had little peasant support.',
          'To reassure the colonial government.', 'officials had access to police reports', 'he had reasons to stress order',
          'It does not show underground activity.', stance=True, why='it shows nationalism suppressed and weak'),
    ],
})

e12b = T('The impact of Japanese occupation on nationalism, 1941-45', 'japanese occupation', 'impact of japanese occupation on nationalism')
build_a2(e12b, {
    'enq': 'the impact of the Japanese occupation', 'claim': 'the Japanese occupation was the main reason for the growth of nationalism in Southeast Asia',
    'stim': ['Singapore surrendered to Japan on 15 February 1942.', 'The Dutch in the East Indies surrendered to Japan in March 1942.', 'Japan granted nominal independence to Burma in August 1943.'],
    'terms': [
        ('Greater East Asia Co-Prosperity Sphere', 'Japan\'s name for its empire in East and Southeast Asia'),
        ('PETA', 'the Defenders of the Homeland, the Indonesian volunteer army trained by the Japanese from 1943'),
        ('Burma Independence Army', 'the force led by Aung San that entered Burma with the Japanese in 1942'),
        ('Viet Minh', 'the League for the Independence of Vietnam, formed by Ho Chi Minh in 1941'),
        ('romusha', 'forced labourers recruited by the Japanese, especially in Indonesia'),
        ('MPAJA', 'the Malayan Peoples\' Anti-Japanese Army, a mainly Chinese communist resistance force'),
    ],
    'dates': [('the Viet Minh was formed', 1941, 5), ('Singapore surrendered to Japan', 1942, 2.15), ('the Dutch surrendered in the East Indies', 1942, 3), ('Japan declared Burma independent', 1943, 8),
              ('the Japanese overthrew the French administration in Indochina', 1945, 3.09), ('Aung San\'s forces turned against Japan', 1945, 3.27), ('Sukarno proclaimed Indonesian independence', 1945, 8.17)],
    'mcq': [
        ('Why was the fall of Singapore in 1942 significant for nationalism?', 'It destroyed the image of European invincibility', ['It ended the war in Asia', 'It made Singapore independent', 'It strengthened British prestige'], '[1]'),
        ('How did the Japanese use Sukarno during the occupation?', 'They used him to mobilise support and labour for the war effort', ['They imprisoned him', 'They made him emperor', 'They exiled him to Japan'], '[1]'),
        ('Which famine of 1944-45 strengthened support for the Viet Minh?', 'The famine in northern Vietnam', ['The Bengal famine', 'The Irish famine', 'The Ukrainian famine'], '[1]'),
    ],
    'why': [
        ('the Japanese occupation strengthened nationalism', ['It destroyed European prestige', 'Japan gave nationalists positions and training, as with PETA', 'It created armies such as the Burma Independence Army', 'Japanese brutality and exploitation created resentment that resistance movements used', 'The defeat of Japan left a power vacuum in 1945'],
         'the occupation broke colonial authority and gave nationalists organisation and arms, leaving them ready to act in 1945'),
    ],
    'claims': [
        ('The Japanese occupation was welcomed by all Southeast Asians throughout the war.', False, 'Initial welcome in some places turned to resentment of brutality and forced labour.'),
        ('Sukarno proclaimed Indonesian independence two days after Japan\'s surrender.', True, 'On 17 August 1945.'),
        ('The Viet Minh fought against the Japanese.', True, 'It received some help from the US OSS in 1945.'),
    ],
    'ess': [
        dict(q='‘The Japanese occupation was the main reason for the growth of nationalism in Southeast Asia.’',
             pro=['It destroyed European prestige', 'It gave nationalists experience, organisation and armies', 'It created a power vacuum in 1945'],
             con=['Nationalist movements and leaders existed before 1941', 'Resistance to Japan built nationalism independently', 'Post-war economic and political conditions mattered'],
             judge='the occupation was the decisive catalyst, turning pre-war nationalist movements into forces able to claim independence'),
        dict(q='How far did the impact of the Japanese occupation differ between Southeast Asian countries?',
             pro=['Indonesia and Burma gained nationalist armies', 'Malaya\'s ethnic divisions deepened, with Chinese resisting and some Malays cooperating', 'Vietnam saw the Viet Minh grow as resistance'],
             con=['Everywhere European prestige collapsed', 'All suffered economic hardship and forced labour', 'All faced returning colonial powers in 1945'],
             judge='the occupation everywhere weakened colonial rule, but its effects on nationalism varied with local conditions'),
    ],
    'src': [
        S('a Burmese nationalist memoir, written in the 1950s (illustrative)', 'When the British ran from Rangoon, the spell was broken. The Japanese gave us arms and titles, but not freedom; so in 1945 we turned the guns on them.',
          'the impact of the occupation in Burma', 'It suggests the occupation broke British prestige and gave nationalists arms.',
          'To explain Burmese nationalists\' actions during the war.', 'the author was a participant', 'written later, it may justify cooperation with Japan',
          'It does not show the experience of ordinary Burmese.', stance=True, why='it shows the occupation strengthening nationalism'),
        S('a historian writing in 1990 (illustrative)', 'The war accelerated movements whose roots lay in the 1920s. Without the nationalist parties built before 1941, there would have been no leaders ready to seize the moment in 1945.',
          'the roots of nationalism', 'The historian argues pre-war nationalism was essential.',
          'To place the occupation in a longer perspective.', 'it is a considered interpretation', 'it is one view',
          'It does not discuss Japanese policy in detail.', stance=False, why='it stresses pre-war roots', kind='secondary'),
    ],
})

e12c = T('Decolonisation and independence: Indonesia, Malaya and Vietnam', 'decolonisation and independence', 'indonesia, malaya and vietnam')
build_a2(e12c, {
    'enq': 'decolonisation in Southeast Asia', 'claim': 'decolonisation in Southeast Asia was achieved mainly by armed struggle',
    'stim': ['The Netherlands transferred sovereignty to Indonesia in December 1949.', 'Malaya became independent on 31 August 1957.', 'The French were defeated at Dien Bien Phu in May 1954.'],
    'terms': [
        ('police actions', 'the Dutch military campaigns against the Indonesian Republic in 1947 and 1948'),
        ('Malayan Emergency', 'the communist insurgency in Malaya from 1948 to 1960'),
        ('Briggs Plan', 'the British plan to resettle Chinese squatters in "New Villages" to cut off communist guerrillas'),
        ('Alliance Party', 'the coalition of UMNO, the MCA and the MIC that won the 1955 Malayan election'),
        ('Dien Bien Phu', 'the battle of 1954 in which the Viet Minh defeated the French'),
        ('Geneva Accords', 'the 1954 agreements that divided Vietnam temporarily at the 17th parallel'),
    ],
    'dates': [('Ho Chi Minh declared Vietnamese independence', 1945, 9.02), ('the Philippines became independent', 1946, 7.04), ('the first Dutch police action began', 1947, 7), ('Burma became independent', 1948, 1.04),
              ('the Malayan Emergency was declared', 1948, 6), ('the Netherlands transferred sovereignty to Indonesia', 1949, 12), ('the French garrison at Dien Bien Phu fell', 1954, 5.07), ('Malaya became independent', 1957, 8.31)],
    'mcq': [
        ('Why did the Netherlands finally agree to Indonesian independence in 1949?', 'The USA threatened to withhold Marshall Aid', ['The Dutch won the war', 'Indonesia joined NATO', 'The Japanese demanded it'], '[1]'),
        ('Who led Malaya to independence in 1957?', 'Tunku Abdul Rahman', ['Sukarno', 'Aung San', 'Lee Kuan Yew'], '[1]'),
        ('Where was Vietnam divided by the Geneva Accords?', 'At the 17th parallel', ['At the 38th parallel', 'At the Mekong River', 'At the 49th parallel'], '[1]'),
    ],
    'why': [
        ('Malaya achieved independence peacefully in 1957', ['The British wanted to hand power to moderates and defeat the communists', 'The Alliance united the main ethnic groups', 'The Emergency was being won by the mid-1950s', 'Britain wanted to keep economic interests such as rubber and tin'],
         'Britain transferred power to a multi-ethnic moderate alliance to defeat communism and protect its interests'),
        ('France was defeated in Vietnam', ['The Viet Minh had mass support among peasants', 'Giap\'s military leadership and Chinese aid after 1949', 'France was weakened after the Second World War', 'French public opinion turned against the war'],
         'mass support and Chinese aid allowed the Viet Minh to defeat a France unable to commit the resources to win'),
    ],
    'claims': [
        ('Indonesia won independence without any fighting.', False, 'The Republic fought the Dutch from 1945 to 1949.'),
        ('The Malayan Emergency involved mainly Chinese communist guerrillas.', True, 'The MCP drew mostly on the Chinese community.'),
        ('Vietnam was united immediately after the Geneva Accords.', False, 'The planned elections of 1956 were not held, and Vietnam remained divided.'),
    ],
    'ess': [
        dict(q='‘Decolonisation in Southeast Asia was achieved mainly by armed struggle.’',
             pro=['Vietnam won independence by defeating France', 'Indonesia fought the Dutch from 1945 to 1949', 'Burma\'s army gave nationalists bargaining power'],
             con=['Malaya and the Philippines gained independence by negotiation', 'International pressure, especially from the USA, forced the Dutch to concede', 'Britain chose to leave'],
             judge='armed struggle was decisive in Vietnam and important in Indonesia, but negotiation and international pressure were more important elsewhere'),
        dict(q='How far did the Cold War shape decolonisation in Southeast Asia?',
             pro=['US pressure on the Dutch to prevent communist gains', 'Britain fought communists in Malaya and handed power to moderates', 'Vietnam\'s division reflected Cold War rivalry'],
             con=['Nationalist strength was the main force', 'Colonial powers were weakened by the Second World War', 'Local conditions differed greatly'],
             judge='the Cold War shaped the timing and outcome of decolonisation, but nationalist movements were its driving force'),
    ],
    'src': [
        S('Ho Chi Minh, Declaration of Independence of the Democratic Republic of Vietnam, 2 September 1945 (abridged)', 'All men are created equal. They are endowed by their Creator with certain unalienable rights; among these are Life, Liberty and the pursuit of Happiness.',
          'Vietnamese nationalism', 'Ho uses the words of the American Declaration to claim the right to independence.',
          'To declare independence and win US sympathy.', 'it is the founding statement of the DRV', 'Ho was a communist who chose words to appeal to the USA',
          'It does not show the French response.', stance=None),
        S('a report by a British official in Malaya, 1955 (illustrative)', 'The Alliance has won fifty-one of the fifty-two seats. If we give self-government to these moderate men, the communists lose their best argument.',
          'British policy in Malaya', 'It suggests Britain saw independence as a way to defeat communism.',
          'To advise London on policy.', 'it shows official thinking', 'it gives only the British view',
          'It does not show Malayan views.', stance=False, why='it shows negotiated decolonisation'),
    ],
})

e12d = T('Cold War pressures and nation-building after independence', 'cold war pressures', 'nation-building after independence')
build_a2(e12d, {
    'enq': 'nation-building in Southeast Asia', 'claim': 'Cold War pressures were the main obstacle to nation-building in Southeast Asia after independence',
    'stim': ['SEATO was founded in September 1954.', 'The Bandung Conference of Asian and African states met in April 1955.', 'ASEAN was founded in August 1967 by Indonesia, Malaysia, the Philippines, Singapore and Thailand.'],
    'terms': [
        ('domino theory', 'the US belief, stated by Eisenhower in 1954, that if one country fell to communism its neighbours would follow'),
        ('SEATO', 'the Southeast Asia Treaty Organization, the anti-communist alliance of 1954'),
        ('Non-Aligned Movement', 'the group of states, influenced by Bandung, that avoided joining either Cold War bloc'),
        ('Guided Democracy', 'Sukarno\'s authoritarian system in Indonesia from 1959'),
        ('Konfrontasi', 'Indonesia\'s confrontation with Malaysia from 1963 to 1966'),
        ('New Order', 'Suharto\'s military-backed regime in Indonesia from 1966'),
        ('ASEAN', 'the Association of Southeast Asian Nations, founded in 1967'),
    ],
    'dates': [('SEATO was founded', 1954, 9), ('the Bandung Conference was held', 1955, 4), ('Sukarno introduced Guided Democracy', 1959, 7), ('Ne Win seized power in Burma', 1962, 3),
              ('Malaysia was formed', 1963, 9), ('Singapore left Malaysia', 1965, 8.09), ('ASEAN was founded', 1967, 8.08)],
    'mcq': [
        ('What happened in Indonesia after the failed coup of 30 September 1965?', 'The army destroyed the communist party (PKI) in mass killings and Suharto took power', ['Sukarno became more powerful', 'The PKI won an election', 'Indonesia joined SEATO'], 'Estimates of the dead are around 500,000 or more. [1]'),
        ('Why did Singapore leave Malaysia in 1965?', 'Disputes between Malay and Chinese political leaders over the position of the Malays', ['Singapore was invaded by Indonesia', 'Britain ordered it to leave', 'It joined Indonesia'], '[1]'),
        ('Which policy did Malaysia introduce in 1971 after the riots of 1969?', 'The New Economic Policy to improve the economic position of the Malays', ['Guided Democracy', 'The domino theory', 'Konfrontasi'], '[1]'),
    ],
    'why': [
        ('nation-building was difficult in Southeast Asia after independence', ['Ethnic and religious divisions, as in Malaysia and Burma', 'Communist insurgencies and Cold War intervention', 'Economic underdevelopment and dependence on commodity exports', 'Weak democratic traditions and the power of the military', 'Borders inherited from colonial rule'],
         'internal divisions inherited from colonial rule were the main problem, made worse by Cold War intervention'),
    ],
    'claims': [
        ('ASEAN was founded in 1967 by five states.', True, 'Indonesia, Malaysia, the Philippines, Singapore and Thailand.'),
        ('Sukarno aligned Indonesia firmly with the USA.', False, 'He promoted non-alignment and moved closer to China and the PKI.'),
        ('Burma remained a democracy throughout the 1960s.', False, 'Ne Win\'s military coup of 1962 began decades of military rule.'),
    ],
    'ess': [
        dict(q='‘Cold War pressures were the main obstacle to nation-building in Southeast Asia after independence.’',
             pro=['War in Vietnam and Indochina', 'Communist insurgencies and US intervention', 'Superpower support for military regimes'],
             con=['Ethnic divisions in Malaysia, Burma and elsewhere', 'Economic weakness and poverty', 'Authoritarian leaders such as Sukarno, Ne Win and Marcos'],
             judge='Cold War pressures were decisive in Indochina, but elsewhere internal divisions and authoritarian rule were the main obstacles'),
        dict(q='How successful were Southeast Asian states in building stable nations by the 1990s?',
             pro=['ASEAN promoted regional cooperation', 'Rapid economic growth in Singapore, Malaysia and Thailand', 'Malaysia and Indonesia remained united'],
             con=['Military rule in Burma', 'Violence and genocide in Cambodia under the Khmer Rouge', 'Authoritarian government in Indonesia and the Philippines for long periods'],
             judge='several states achieved stability and growth, but often at the cost of democracy, and some suffered catastrophe'),
    ],
    'src': [
        S('President Eisenhower, press conference, April 1954 (abridged)', 'You have a row of dominoes set up, you knock over the first one, and what will happen to the last one is the certainty that it will go over very quickly.',
          'US policy in Southeast Asia', 'Eisenhower argues that the fall of one country to communism would lead to others falling.',
          'To explain why the USA was concerned about Indochina.', 'it is the president\'s own words', 'it is a simplified public explanation',
          'It does not show the views of Southeast Asians.', stance=True, why='it shows Cold War pressures shaping the region'),
        S('a historian writing in 2000 (illustrative)', 'The new states inherited borders drawn by colonial officials and populations divided by language, religion and race. The Cold War made these problems more dangerous, but it did not create them.',
          'nation-building', 'The historian argues internal divisions inherited from colonialism were the root problem.',
          'To explain the difficulties of nation-building.', 'it is a considered interpretation', 'it is one view',
          'It does not discuss particular countries.', stance=False, why='it stresses internal divisions', kind='secondary'),
    ],
})

CHAPTERS[12] = [e12a, e12b, e12c, e12d]
finalize(CHAPTERS)
