"""IB DP Hindi B SL/HL (Language B guide, first assessment 2020) – ib-g11-hindi (DP year 1).

Prescribed themes: identities, experiences, human ingenuity, social organisation, sharing the planet
(year 1 covers identities, experiences and part of human ingenuity, plus the first HL literary work).
Assessment: Paper 1 writing (one task of three; SL 250–400 words, HL 450–600 words; criteria
A language 12, B message 12, C conceptual understanding 6 = 30 marks); Paper 2 receptive skills
(listening 25 marks, reading 40 marks); Individual Oral (30 marks; HL on a literary extract).

Everything a student sees (stems, options, answers, marking keys) is written in Hindi (Devanagari).
All passages, transcripts, blogs, letters, advertisements and poem extracts are ORIGINAL texts written
for this bank; HL literature items refer to well-known public-domain Hindi works (Premchand, Kabir,
Bharatendu) in general terms.

This module also holds the shared Hindi kit (text-type conventions, criteria, generators) that
ib_g12_hindi.py imports, so both years build items the same way.

Item styles per subtopic kind
  * vocab    – meaning / synonym / reverse MCQs (C1), word-in-context (C2), gap-fill and sentence making (C3),
               paragraph with given words (C4)
  * reading  – original texts: retrieval MCQs, word-in-text (C1), explain (C2), true/false with justification
               and inference (C3), evaluation / personal response (C4)
  * listening– the same on transcripts of audio texts (style p2l)
  * writing  – conventions of the text type (C1/C2), openings, titles, register shifts (C3), full Paper 1 tasks (C4)
  * grammar  – authored transformation banks (C1–C3) and grammar-focused writing (C4)
  * oral     – useful phrases (C1), discussion prompts and visual stimuli (C2–C4)
  * lit      – authored items on the literary work plus original extracts
Every subtopic also gets theme-based Paper 1 tasks (style p1) so any subtopic can feed a mock.
"""
from __future__ import annotations

import itertools
import re

from _common import Registry, T, mcq

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.0}

# One mock = HL Paper 1 (three task options, 10 marks each = 30) + Paper 2 listening (5 x 1 + 10 x 2 = 25)
# + Paper 2 reading (10 x 1 + 5 x 2 + 5 x 4 = 40). 38 items, 95 marks per mock.
LISTEN_CH_G11 = [2, 6, 8, 14]
READ_CH_G11 = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]


def make_mock(listen, read):
    """38 items, 95 marks: Paper 1 (3 x 10) + Paper 2 listening (25) + Paper 2 reading (40)."""
    return [
        dict(section='पेपर 1 – लेखन (तीन में से एक कार्य; मानदंड A, B, C)', count=3, c=['C4'], d=[4, 5, 4], type='long', marks=10, style='p1'),
        dict(section='पेपर 2 – श्रवण: बहुविकल्पी प्रश्न', count=5, c=['C1', 'C1', 'C3'], d=[2, 3], type='mcq', marks=1, style='p2l', chapters=listen),
        dict(section='पेपर 2 – श्रवण: लघु उत्तर', count=10, c=['C2', 'C3'], d=[3, 4], type='short', marks=2, style='p2l', chapters=listen),
        dict(section='पेपर 2 – पठन: बहुविकल्पी प्रश्न', count=10, c=['C1', 'C3'], d=[2, 3], type='mcq', marks=1, style='p2r', chapters=read),
        dict(section='पेपर 2 – पठन: सही/गलत औचित्य सहित', count=5, c=['C3', 'C2'], d=[3], type='short', marks=2, style='p2r', chapters=read),
        dict(section='पेपर 2 – पठन: लघु और विस्तृत उत्तर', count=5, c=['C3', 'C4'], d=[3, 4], type='short', marks=4, style='p2r', chapters=read),
    ]


MOCK = make_mock(LISTEN_CH_G11, READ_CH_G11)

R = Registry()

WORDS = 'मानक स्तर पर 250–400 शब्द; उच्च स्तर पर 450–600 शब्द'

# --------------------------------------------------------------------------------------------
# Text types (Language B guide: personal, professional, mass media)
# --------------------------------------------------------------------------------------------
TT = {
    'blog': dict(name='ब्लॉग प्रविष्टि', grp='व्यक्तिगत', reg='अर्ध-औपचारिक या अनौपचारिक, मित्रवत और आत्मीय लहजा, पर भाषा शुद्ध',
                 aud='ऑनलाइन पाठक, प्रायः समान रुचि वाले लोग',
                 conv=['आकर्षक शीर्षक और प्रविष्टि की तिथि', 'प्रथम पुरुष (मैं) में बातचीत जैसी आत्मीय शैली',
                       'पाठकों से सीधा संवाद और अंत में टिप्पणी करने का आमंत्रण', 'निजी अनुभवों और किस्सों से विचारों को जीवंत बनाना']),
    'diary': dict(name='डायरी प्रविष्टि', grp='व्यक्तिगत', reg='अनौपचारिक, निजी और भावनात्मक', aud='स्वयं लेखक',
                  conv=['दिनांक, दिन और कभी-कभी समय का उल्लेख', 'प्रथम पुरुष में निजी भावनाओं की ईमानदार अभिव्यक्ति',
                        '‘प्रिय डायरी’ जैसा संबोधन और स्वयं से बातचीत की शैली', 'दिन की घटनाओं पर आत्म-चिंतन और भविष्य के संकल्प']),
    'pletter': dict(name='अनौपचारिक पत्र', grp='व्यक्तिगत', reg='अनौपचारिक और आत्मीय; ‘तुम’ का प्रयोग', aud='मित्र या परिवार का सदस्य',
                    conv=['ऊपर पता और दिनांक, फिर ‘प्रिय मित्र’ जैसा आत्मीय संबोधन', 'कुशल-क्षेम पूछने वाली आत्मीय भूमिका',
                          '‘तुम्हारा मित्र’ या ‘तुम्हारी सखी’ जैसा आत्मीय समापन', 'घर-परिवार को नमस्कार कहने जैसी निजी बातें']),
    'fletter': dict(name='औपचारिक पत्र', grp='व्यावसायिक', reg='औपचारिक, विनम्र और संक्षिप्त; ‘आप’ और आदरसूचक क्रियाएँ', aud='अधिकारी, संपादक या संस्था',
                    conv=['प्रेषक का पता, दिनांक और प्राप्तकर्ता का पद व पता', 'विषय-पंक्ति और ‘महोदय/महोदया’ जैसा औपचारिक संबोधन',
                          '‘भवदीय/भवदीया’ जैसा औपचारिक समापन, नाम और हस्ताक्षर', 'समस्या का तथ्यात्मक विवरण और स्पष्ट अनुरोध']),
    'email': dict(name='औपचारिक ईमेल', grp='व्यावसायिक', reg='औपचारिक, संक्षिप्त और स्पष्ट', aud='संस्था, कंपनी या अधिकारी',
                  conv=['प्रति, विषय-पंक्ति और आवश्यकता होने पर संलग्नक का उल्लेख', 'संक्षिप्त अनुच्छेदों में मुख्य अनुरोध या जानकारी',
                        'औपचारिक अभिवादन और नाम, पद तथा संपर्क विवरण के साथ समापन', 'उत्तर की अपेक्षा या अगले कदम का विनम्र उल्लेख']),
    'speech': dict(name='भाषण', grp='जनसंचार', reg='संदर्भ के अनुसार औपचारिक या अर्ध-औपचारिक; प्रेरक और प्रभावी', aud='सभा में उपस्थित श्रोता',
                   conv=['श्रोताओं को आदरपूर्वक संबोधन, जैसे ‘आदरणीय प्रधानाचार्य जी, प्रिय साथियो’', 'अलंकारिक प्रश्न, दोहराव और श्रोताओं से सीधा संवाद',
                         'स्पष्ट आह्वान वाला समापन और धन्यवाद', 'वक्ता का परिचय और भाषण के विषय की घोषणा']),
    'article': dict(name='लेख', grp='जनसंचार', reg='अर्ध-औपचारिक या औपचारिक, सूचनाप्रद और रोचक', aud='पत्रिका या समाचार-पत्र के पाठक',
                    conv=['आकर्षक शीर्षक और लेखक का नाम (बाइलाइन)', 'रोचक भूमिका, उपशीर्षकों में विकसित विचार और निष्कर्ष',
                          'तथ्य, आँकड़े और उदाहरण देकर बात को पुष्ट करना', 'पाठकों की रुचि जगाने वाला प्रश्न या किस्सा']),
    'opinion': dict(name='मत-प्रधान लेख', grp='जनसंचार', reg='औपचारिक, तर्कपूर्ण और संतुलित', aud='समाचार-पत्र, पत्रिका या वेबसाइट के जागरूक पाठक',
                    conv=['स्पष्ट मत प्रकट करने वाला शीर्षक और भूमिका', 'तर्क, प्रमाण और विरोधी मत का खंडन',
                          'निष्कर्ष में अपने मत की पुनः पुष्टि', 'संयोजक शब्दों (इसके अतिरिक्त, दूसरी ओर, अतः) से तर्कों का क्रम']),
    'brochure': dict(name='जागरूकता पत्रक (ब्रोशर)', grp='जनसंचार', reg='सरल, स्पष्ट और सीधा; आज्ञार्थ और विधिलिंग क्रियाएँ', aud='आम जनता या कोई विशेष समूह',
                     conv=['आकर्षक मुख्य शीर्षक और उपशीर्षक', 'बुलेट-बिंदुओं में संक्षिप्त जानकारी और सुझाव',
                           'संपर्क-सूत्र, हेल्पलाइन या वेबसाइट का उल्लेख', 'प्रश्न-उत्तर या ‘क्या करें, क्या न करें’ जैसे खंड']),
    'news': dict(name='समाचार रिपोर्ट', grp='जनसंचार', reg='औपचारिक, तथ्यात्मक और निष्पक्ष; प्रायः कर्मवाच्य', aud='समाचार-पत्र या समाचार-वेबसाइट के पाठक',
                 conv=['शीर्षक और स्थान-दिनांक-पंक्ति (जैसे ‘जयपुर, 12 मार्च’)', 'पहले अनुच्छेद में कौन, क्या, कब, कहाँ, क्यों और कैसे',
                       'प्रत्यक्षदर्शियों या अधिकारियों के उद्धरण', 'तृतीय पुरुष में निष्पक्ष भाषा, निजी राय के बिना']),
    'interview': dict(name='साक्षात्कार', grp='जनसंचार', reg='प्रश्न औपचारिक-विनम्र, उत्तरों में स्वाभाविक बोलचाल', aud='पत्रिका या विद्यालय-पत्रिका के पाठक',
                      conv=['साक्षात्कारदाता का संक्षिप्त परिचय देने वाली भूमिका', 'प्रश्न-उत्तर प्रारूप, जिसमें प्रश्नकर्ता और उत्तरदाता स्पष्ट हों',
                            'धन्यवाद के साथ समापन', 'खुले प्रश्न (कैसे, क्यों) जो विस्तृत उत्तर दिलवाएँ']),
    'review': dict(name='समीक्षा', grp='जनसंचार', reg='अर्ध-औपचारिक, मूल्यांकनपरक और रोचक', aud='पत्रिका, ब्लॉग या वेबसाइट के पाठक',
                   conv=['कृति का नाम, निर्देशक या लेखक और विधा का उल्लेख', 'कहानी का संक्षिप्त सार, पर अंत बताए बिना',
                         'अभिनय, संगीत, भाषा आदि का मूल्यांकन', 'अंत में रेटिंग या स्पष्ट सिफ़ारिश']),
    'travelogue': dict(name='यात्रा-वृत्तांत', grp='व्यक्तिगत', reg='अर्ध-औपचारिक, वर्णनात्मक और आत्मीय', aud='पत्रिका या ब्लॉग के पाठक',
                       conv=['स्थानों और घटनाओं का क्रमिक वर्णन', 'दृश्य, ध्वनि, गंध और स्वाद जैसे संवेदी विवरण',
                             'लेखक के निजी अनुभव और यात्रा से मिली सीख', 'स्थानीय लोगों से मुलाक़ात और संस्कृति का जीवंत चित्रण']),
    'report': dict(name='औपचारिक रिपोर्ट (प्रतिवेदन)', grp='व्यावसायिक', reg='औपचारिक, वस्तुनिष्ठ और संक्षिप्त; कर्मवाच्य का प्रयोग', aud='प्रधानाचार्य, समिति या संस्था',
                   conv=['शीर्षक तथा किसके लिए और किसके द्वारा तैयार किया गया', 'उद्देश्य, निष्कर्ष और सिफ़ारिशों के अलग-अलग खंड',
                         'तिथि, नाम और पद के साथ समापन', 'आँकड़ों या सर्वेक्षण के परिणामों का निष्पक्ष प्रस्तुतीकरण']),
    'appeal': dict(name='अपील (निवेदन)', grp='जनसंचार', reg='भावनात्मक, प्रेरक और विनम्र', aud='आम जनता या समुदाय',
                   conv=['भावनात्मक और प्रेरक शीर्षक', 'समस्या का स्पष्ट विवरण और यह कि सहायता क्यों आवश्यक है',
                         'सहायता का तरीका, संपर्क और कार्य करने का आह्वान', 'अपील करने वाली संस्था का नाम']),
    'notice': dict(name='सूचना', grp='व्यावसायिक', reg='औपचारिक, अत्यंत संक्षिप्त और स्पष्ट', aud='विद्यालय, कार्यालय या मोहल्ले के लोग',
                   conv=['‘सूचना’ शीर्षक, संस्था का नाम और दिनांक', 'क्या, कब, कहाँ और किसके लिए का संक्षिप्त विवरण',
                         'जारीकर्ता का नाम और पद', 'बॉक्स में सीमित शब्दों में लिखी गई जानकारी']),
    'advert': dict(name='विज्ञापन', grp='जनसंचार', reg='आकर्षक, संक्षिप्त और प्रेरक', aud='संभावित ग्राहक',
                   conv=['आकर्षक नारा (स्लोगन) और उत्पाद या सेवा का नाम', 'लाभ बताने वाली प्रेरक भाषा',
                         'मूल्य, छूट और संपर्क जानकारी', 'चित्र या बड़े अक्षरों जैसे दृश्य तत्व']),
    'biodata': dict(name='परिचय-पत्र (बायोडाटा)', grp='व्यावसायिक', reg='औपचारिक, तथ्यात्मक और बिंदुवार', aud='नियोक्ता या चयन समिति',
                    conv=['नाम, संपर्क विवरण और करियर उद्देश्य', 'शैक्षिक योग्यता और अनुभव का क्रमबद्ध विवरण',
                          'कौशल, उपलब्धियाँ और रुचियाँ बिंदुओं में', 'संदर्भ और घोषणा के साथ समापन']),
    'proposal': dict(name='प्रस्ताव', grp='व्यावसायिक', reg='औपचारिक, स्पष्ट और व्यावहारिक', aud='प्रधानाचार्य, नगर परिषद या कोई समिति',
                     conv=['प्रस्ताव का शीर्षक और किसे संबोधित है', 'वर्तमान समस्या और प्रस्ताव की आवश्यकता',
                           'योजना, ख़र्च और समय-सीमा के चरण', 'अपेक्षित लाभ और स्वीकृति का अनुरोध']),
}
KINDS = ['लेख', 'ब्लॉग प्रविष्टि', 'समाचार रिपोर्ट', 'विज्ञापन', 'औपचारिक पत्र', 'अनौपचारिक पत्र', 'साक्षात्कार', 'डायरी प्रविष्टि',
         'जागरूकता पत्रक', 'समीक्षा', 'भाषण', 'यात्रा-वृत्तांत', 'संपादकीय', 'कविता', 'कहानी का अंश', 'सूचना']
SIMILAR = [{'लेख', 'संपादकीय', 'ब्लॉग प्रविष्टि'}, {'औपचारिक पत्र', 'अनौपचारिक पत्र'}, {'डायरी प्रविष्टि', 'ब्लॉग प्रविष्टि', 'यात्रा-वृत्तांत'},
           {'विज्ञापन', 'जागरूकता पत्रक'}, {'कविता', 'कहानी का अंश'}, {'साक्षात्कार', 'भाषण'}, {'सूचना', 'जागरूकता पत्रक'}]


FEM_HEADS = {'प्रविष्टि', 'रिपोर्ट', 'सूचना', 'कविता', 'समीक्षा', 'वार्ता', 'उद्घोषणा', 'घोषणा', 'बातचीत', 'कमेंट्री'}


def given(kind):
    """‘दिया गया’ / ‘दी गई’ agreeing with the text type's head noun."""
    return 'दी गई' if kind.split()[-1].strip('()') in FEM_HEADS else 'दिया गया'


def _far_kinds(k):
    near = {k}
    for s in SIMILAR:
        if k in s:
            near |= s
    return [x for x in KINDS if x not in near]


# Paper 1 criteria (Language B guide, 2020): A language 12, B message 12, C conceptual understanding 6.
def p1_key(m):
    a = round(m * 0.4)
    b = round(m * 0.4)
    c = m - a - b
    return (f'पेपर 1 मानदंड (कुल {m} अंक; मूल अनुपात 12 : 12 : 6). '
            f'A — भाषा ({a}): विविध और सटीक शब्दावली, मुहावरेदार प्रयोग, सरल और जटिल वाक्य-संरचनाओं का शुद्ध प्रयोग; त्रुटियाँ संप्रेषण में बाधा न डालें। '
            f'B — संदेश ({b}): कार्य की सभी माँगें पूरी हों; विचार प्रासंगिक, विकसित, उदाहरणों से पुष्ट और तार्किक क्रम में हों; अनुच्छेदों में सुसंगति हो। '
            f'C — अवधारणात्मक समझ ({c}): पाठ-प्रकार उद्देश्य, पाठक और संदर्भ के अनुकूल हो; रजिस्टर और लहजा उपयुक्त हो; पाठ-प्रकार की परंपराएँ स्पष्ट दिखें। '
            'उच्चतम बैंड: प्रभावी, सुसंगठित और पाठक पर केंद्रित उत्तर; मध्य बैंड: प्रासंगिक पर असमान रूप से विकसित; निम्न बैंड: सीमित, अस्पष्ट या पाठ-प्रकार से भटका हुआ उत्तर।')


def para_key(m, extra=''):
    return (f'{m} अंक: भाषा (शब्दावली और व्याकरण की शुद्धता) {m // 2} अंक; विषय-वस्तु और सुसंगति {m - m // 2} अंक। ' + extra).strip()


def cap(s):
    return s[:1].upper() + s[1:]


def _bul(items):
    return '\n'.join('• ' + b for b in items)


# --------------------------------------------------------------------------------------------
# Global banks
# --------------------------------------------------------------------------------------------
ORAL_PHRASES = [
    ('अपना मत प्रकट करना', 'मेरे विचार में…', ['इसके विपरीत…', 'उदाहरण के लिए…', 'क्या आप दोहरा सकते हैं?']),
    ('विनम्रता से असहमति जताना', 'मैं आपकी बात से पूरी तरह सहमत नहीं हूँ, क्योंकि…', ['आप बिल्कुल ठीक कह रहे हैं।', 'सबसे पहले…', 'संक्षेप में कहूँ तो…']),
    ('उदाहरण देना', 'उदाहरण के तौर पर…', ['अंततः…', 'मैं असहमत हूँ…', 'माफ़ कीजिए, फिर से कहिए?']),
    ('स्पष्टीकरण माँगना', 'क्या आप इसे थोड़ा और स्पष्ट कर सकते हैं?', ['मेरे विचार में…', 'इसके अतिरिक्त…', 'निष्कर्ष यह है कि…']),
    ('सोचने के लिए समय लेना', 'यह एक दिलचस्प प्रश्न है; मुझे एक क्षण सोचने दीजिए…', ['बिल्कुल नहीं!', 'इसलिए…', 'उदाहरण के लिए…']),
    ('निष्कर्ष निकालना', 'अंततः मैं यह कहना चाहूँगा कि…', ['सबसे पहले…', 'क्या आप सहमत हैं?', 'उदाहरण के तौर पर…']),
    ('सहमति जताना', 'मैं आपसे पूरी तरह सहमत हूँ।', ['मुझे इसमें संदेह है…', 'दूसरी ओर…', 'क्या आप फिर से कहेंगे?']),
    ('विरोधी विचार प्रस्तुत करना', 'दूसरी ओर, कुछ लोग मानते हैं कि…', ['इसी प्रकार…', 'मैं पूरी तरह सहमत हूँ।', 'उदाहरण के लिए…']),
    ('नया बिंदु जोड़ना', 'इसके अतिरिक्त…', ['इसके बावजूद…', 'मुझे माफ़ कीजिए…', 'अंत में…']),
    ('व्यक्तिगत अनुभव जोड़ना', 'मुझे याद है, जब मैं…', ['आँकड़ों के अनुसार…', 'अतः…', 'क्या आप स्पष्ट करेंगे?']),
    ('बात को दोबारा कहना', 'दूसरे शब्दों में कहूँ तो…', ['इसके विपरीत…', 'सबसे पहले…', 'मुझे नहीं पता।']),
    ('कारण बताना', 'इसका मुख्य कारण यह है कि…', ['उदाहरण के तौर पर…', 'क्या मैं कुछ पूछ सकता हूँ?', 'अंततः…']),
]

PURPOSES = ['जानकारी देना', 'पाठकों को किसी काम के लिए प्रेरित करना', 'मनोरंजन करना', 'शिकायत दर्ज करना', 'सलाह देना',
            'किसी उत्पाद को बेचना', 'निजी अनुभव साझा करना', 'किसी विचार का विरोध करना']


# --------------------------------------------------------------------------------------------
# Generators
# --------------------------------------------------------------------------------------------
STOP = set('का की के को में से है हैं था थी थे और पर भी तो यह वह ये वे एक कि ने नहीं कर रहा रही रहे हो गया गई गए अपने अपनी इस उस लिए साथ जो क्या क्यों कैसे कौन कौन-से कौन-सा कौन-सी पाठ अनुसार लेखक बताइए लिखिए दीजिए कीजिए समझाइए किस किसी'.split())


def _toks(s):
    import re
    return {w for w in re.findall(r'[\u0900-\u097F]+(?:-[\u0900-\u097F]+)?|\d+', s) if len(w) > 2 and w not in STOP}


def excerpt(body, probe, width=3):
    """The sentences of body around the one that best matches probe (question + answer)."""
    import re
    parts = [x.strip() for x in re.split(r'(?<=[।?!])\s+|\n', body) if x.strip()]
    if len(parts) <= width:
        return body
    pt = _toks(probe)
    best = max(range(len(parts)), key=lambda i: (len(_toks(parts[i]) & pt), -i))
    lo = max(0, min(best - 1, len(parts) - width))
    return ' '.join(parts[lo:lo + width])


class Kit:
    """Builds templates for one subject from chapter themes (TH) and subtopic specs."""

    def __init__(self, R):
        self.R = R

    mock_only = False

    def add(self, key, c, d, fn, type='short', style=None, name=''):
        if self.mock_only:  # Paper 2 texts lent to a non-reading subtopic: used only in mock papers
            inner = fn

            def fn(rng, slot, inner=inner):
                return inner(rng, slot) if slot.set == 'mock' else None
            name = 'mock_' + (name or inner.__name__)
        self.R.t.setdefault(key, []).append(T(c, d, fn, type, style, name or fn.__name__))

    # ---- authored items ---------------------------------------------------------------------
    def items(self, key, items):
        """items: ('C1', stem, answer, [3 wrong], why) -> MCQ; ('C2', stem, answer, key[, marks]) -> written."""
        mc, wr = {}, {}
        for it in items:
            if isinstance(it[3], list):
                mc.setdefault(it[0], []).append(it)
            else:
                wr.setdefault(it[0], []).append(it)
        rng_d = {'C1': (1, 3), 'C2': (1, 4), 'C3': (1, 5), 'C4': (2, 5)}
        for c, lst in mc.items():
            def fn(rng, slot, lst=lst):
                _, q, a, w, why = rng.choice(lst)
                return mcq(rng, q, a, w, why)
            self.add(key, c, rng_d[c], fn, 'mcq', None, 'auth_mcq')
        for c, lst in wr.items():
            def fn(rng, slot, lst=lst, c=c):
                it = rng.choice(lst)
                m = it[4] if len(it) > 4 else {'C1': 1, 'C2': 2, 'C3': 3, 'C4': 6}[c]
                ty = 'long' if m >= 8 else 'explain' if c in ('C2', 'C4') else 'short'
                return dict(stem=it[1], answer=it[2], markingKey=it[3], marks=m, type=ty)
            self.add(key, c, rng_d[c], fn, 'explain' if c in ('C2', 'C4') else 'short', None, 'auth_wr')

    # ---- vocabulary -------------------------------------------------------------------------
    def vocab(self, key, th, parts=('c1', 'c2', 'c3', 'c4')):
        V = th['vocab']
        cn = th['name']
        if 'c1' in parts:
            def meaning(rng, slot):
                w, m, s, _ = rng.choice(V)
                others = [x[1] for x in V if x[0] != w]
                return mcq(rng, rng.choice([f'‘{cn}’ विषय के पाठ में आए शब्द ‘{w}’ का सबसे उपयुक्त अर्थ क्या है?',
                                            f'‘{cn}’ से जुड़े शब्द ‘{w}’ का अर्थ बताने वाला विकल्प चुनिए।']),
                           m, rng.sample(others, 3), f'‘{w}’ का अर्थ है — {m}।')
            self.add(key, 'C1', (1, 3), meaning, 'mcq', 'p2r', 'v_meaning')

            def synonym(rng, slot):
                w, m, s, _ = rng.choice(V)
                others = [x[2] for x in V if x[0] != w and x[2] != s]
                return mcq(rng, f'‘{cn}’ विषय की शब्दावली: ‘{w}’ शब्द का पर्यायवाची (समान अर्थ वाला) शब्द कौन-सा है?',
                           s, rng.sample(others, 3), f'‘{w}’ और ‘{s}’ दोनों का अर्थ है — {m}।')
            self.add(key, 'C1', (1, 2), synonym, 'mcq', None, 'v_syn')

            def reverse(rng, slot):
                w, m, s, _ = rng.choice(V)
                others = [x[0] for x in V if x[0] != w]
                return mcq(rng, f'‘{cn}’ विषय से जुड़ा वह शब्द चुनिए जिसका अर्थ है: “{m}”।', w, rng.sample(others, 3),
                           f'इस अर्थ वाला शब्द ‘{w}’ है।')
            self.add(key, 'C1', (1, 3), reverse, 'mcq', None, 'v_rev')
        if 'c2' in parts:
            def context(rng, slot):
                w, m, s, sent = rng.choice(V)
                full = sent.replace('____', w)
                return dict(stem=f'यह वाक्य पढ़िए: “{full}”\nइस वाक्य में ‘{w}’ शब्द का क्या अर्थ है? संदर्भ के आधार पर समझाइए और इसका एक पर्यायवाची शब्द लिखिए।',
                            answer=f'यहाँ ‘{w}’ का अर्थ है — {m}। पर्यायवाची: {s}।', type='explain', marks=2,
                            markingKey=f'1 अंक: संदर्भ के अनुरूप अर्थ ({m}); 1 अंक: उपयुक्त पर्यायवाची ({s} या समान अर्थ वाला कोई शुद्ध शब्द)।')
            self.add(key, 'C2', (1, 4), context, 'explain', 'p2r', 'v_ctx')
        if 'c3' in parts:
            def gap(rng, slot):
                w, m, s, sent = rng.choice(V)
                others = [x[0] for x in V if x[0] != w]
                return mcq(rng, f'रिक्त स्थान के लिए सबसे उपयुक्त शब्द चुनिए:\n“{sent}”', w, rng.sample(others, 3),
                           f'‘{w}’ ({m}) ही वाक्य के अर्थ और संदर्भ में सही बैठता है।')
            self.add(key, 'C3', (1, 3), gap, 'mcq', 'p2r', 'v_gap')

            def pair(rng, slot):
                a, b = rng.sample(V, 2)
                return dict(stem=f'‘{a[0]}’ और ‘{b[0]}’ शब्दों का प्रयोग करते हुए ‘{cn}’ विषय पर दो सार्थक वाक्य लिखिए, जिनसे दोनों शब्दों का अर्थ स्पष्ट हो।',
                            answer=f'नमूना उत्तर: {a[3].replace("____", a[0])} {b[3].replace("____", b[0])}', type='short', marks=2,
                            markingKey=f'प्रत्येक वाक्य के लिए 1 अंक: शब्द का अर्थ के अनुरूप ({a[0]} = {a[1]}; {b[0]} = {b[1]}) और व्याकरण की दृष्टि से शुद्ध प्रयोग। केवल शब्द रख देने पर, जिससे अर्थ स्पष्ट न हो, अंक नहीं।')
            self.add(key, 'C3', (2, 4), pair, 'short', None, 'v_pair')
        if 'c4' in parts:
            def para(rng, slot):
                ws = rng.sample(V, 4)
                topic = rng.choice(th['topics'])
                m = 6 if slot.d >= 4 else 4
                n = '100–120' if m == 6 else '70–90'
                return dict(stem=f'‘{topic}’ विषय पर {n} शब्दों का एक अनुच्छेद लिखिए। उसमें इन चारों शब्दों का सार्थक प्रयोग कीजिए: {", ".join(w[0] for w in ws)}।',
                            answer='अपेक्षित: विषय पर केंद्रित, सुसंगठित अनुच्छेद जिसमें चारों शब्द सही अर्थ में आएँ — ' + '; '.join(f'{w[0]} ({w[1]})' for w in ws) + '।',
                            type='long', marks=m, markingKey=para_key(m, 'प्रत्येक शब्द का अर्थ के अनुरूप प्रयोग अनिवार्य; किसी शब्द के छूटने या गलत अर्थ में आने पर भाषा के अंक घटाएँ।'))
            self.add(key, 'C4', (2, 5), para, 'long', None, 'v_para')

    # ---- texts (reading) and transcripts (listening) ----------------------------------------
    def texts(self, key, th, which='texts', style='p2r'):
        TX = th[which]
        cn = th['name']
        if which.startswith('texts'):
            lead = lambda t: f'नीचे {given(t["kind"])} {t["kind"]} पढ़िए और प्रश्न का उत्तर दीजिए।'
            lead2 = lambda t: f'{t["kind"]} “{t["title"]}” का यह अंश पढ़िए और प्रश्न का उत्तर दीजिए।'
        else:
            lead = lambda t: f'नीचे एक {t["kind"]} का प्रतिलेख है (परीक्षा में आप इसे सुनेंगे)। ध्यान से पढ़िए और उत्तर दीजिए।'
            lead2 = lambda t: f'{t["kind"]} “{t["title"]}” के प्रतिलेख का यह अंश ध्यान से पढ़िए (परीक्षा में आप इसे सुनेंगे) और उत्तर दीजिए।'

        def body(t, q=None):
            if q is None:
                return f'{lead(t)}\n\n“{t["title"]}”\n{t["body"]}\n\n'
            return f'{lead2(t)}\n\n{excerpt(t["body"], " ".join(str(x) for x in q[1:] if isinstance(x, str)))}\n\n'

        def pool(cat):
            out = []
            for t in TX:
                for q in t['qs']:
                    if cat == 'mcq1' and q[0] == 'C1' and len(q) > 3:
                        out.append((t, q))
                    elif cat == 'mcq3' and q[0] in ('C2', 'C3') and len(q) > 3:
                        out.append((t, q))
                    elif cat == 'c1' and q[0] == 'C1' and len(q) == 3:
                        out.append((t, q))
                    elif cat == 'c2' and q[0] == 'C2' and len(q) == 3:
                        out.append((t, q))
                    elif cat == 'tf' and q[0] == 'tf':
                        out.append((t, q))
                    elif cat == 'c3' and q[0] == 'C3' and len(q) == 3:
                        out.append((t, q))
                    elif cat == 'c4' and q[0] == 'C4':
                        out.append((t, q))
            return out

        P = {k: pool(k) for k in ('mcq1', 'mcq3', 'c1', 'c2', 'tf', 'c3', 'c4')}

        if P['mcq1']:
            def m1(rng, slot):
                t, q = rng.choice(P['mcq1'])
                return mcq(rng, body(t, q) + q[1], q[2], q[3], f'पाठ में स्पष्ट रूप से दिया गया है: {q[2]}।')
            self.add(key, 'C1', (1, 3), m1, 'mcq', style, 'tx_m1')

        def kind(rng, slot):
            t = rng.choice(TX)
            if t['kind'] not in KINDS:
                return None
            q = 'यह पाठ किस प्रकार का है?' if which.startswith('texts') else 'यह श्रव्य अंश मूल रूप से किस प्रकार का है?'
            far = _far_kinds(t['kind'])
            st = f'“{t["title"]}”\n{t["body"]}\n\n{q} सही पाठ-प्रकार चुनिए।'
            return mcq(rng, st, t['kind'], rng.sample(far, 3), f'प्रारूप, संबोधन और भाषा से स्पष्ट है कि यह {t["kind"]} है।')
        if which.startswith('texts'):
            self.add(key, 'C1', (1, 2), kind, 'mcq', style, 'tx_kind')
        if P['mcq3']:
            def m3(rng, slot):
                t, q = rng.choice(P['mcq3'])
                return mcq(rng, body(t, q) + q[1], q[2], q[3], f'पाठ के संकेतों से यही निष्कर्ष निकलता है: {q[2]}।')
            self.add(key, 'C3', (2, 4), m3, 'mcq', style, 'tx_m3')
        if P['c1']:
            def s1(rng, slot):
                t, q = rng.choice(P['c1'])
                return dict(stem=body(t, q) + q[1], answer=q[2], type='short', marks=1,
                            markingKey=f'{q[2]} — केवल पाठ में दिया गया शब्द/तथ्य मान्य; अतिरिक्त गलत जानकारी जोड़ने पर अंक नहीं।')
            self.add(key, 'C1', (1, 3), s1, 'short', style, 'tx_s1')
        if P['c2']:
            def s2(rng, slot):
                t, q = rng.choice(P['c2'])
                return dict(stem=body(t, q) + q[1], answer=q[2], type='explain', marks=2,
                            markingKey=f'{q[2]} — 1 अंक मुख्य विचार के लिए, 1 अंक अपने शब्दों में स्पष्ट व्याख्या के लिए; पाठ की पंक्ति ज्यों की त्यों उतारने पर केवल 1 अंक।')
            self.add(key, 'C2', (1, 4), s2, 'explain', style, 'tx_s2')
        if P['tf']:
            def tf(rng, slot):
                t, q = rng.choice(P['tf'])
                return dict(stem=body(t, q) + f'निम्नलिखित कथन सही है या गलत? पाठ के शब्दों से अपने उत्तर का औचित्य दीजिए।\nकथन: {q[1]}',
                            answer=f'{q[2]} — औचित्य: {q[3]}', type='short', marks=slot.marks or (2 if slot.d >= 3 else 1),
                            markingKey=f'{q[2]}; औचित्य: {q[3]} — सही/गलत और पाठ से लिया गया उचित औचित्य, दोनों होने पर ही अंक; केवल ‘सही’ या ‘गलत’ लिखने पर अंक नहीं।')
            self.add(key, 'C3', (2, 4), tf, 'short', style, 'tx_tf')

            def tf2(rng, slot):
                t, q = rng.choice(P['tf'])
                src = 'वक्ता' if which.startswith('audio') else 'लेखक'
                return dict(stem=body(t, q) + f'{src} के अनुसार इस कथन की पुष्टि या खंडन कीजिए और अंश के जिस वाक्य से यह पता चलता है, उसे उद्धृत कीजिए।\nकथन: “{q[1]}”',
                            answer=f'{"पुष्टि (कथन सही है)" if q[2] == "सही" else "खंडन (कथन गलत है)"} — प्रमाण: {q[3]}', type='short', marks=slot.marks or 2,
                            markingKey=f'1 अंक: सही निर्णय ({q[2]}); 1 अंक: अंश से उचित उद्धरण — {q[3]}')
            self.add(key, 'C2', (2, 4), tf2, 'short', style, 'tx_tf2')
        if P['c3']:
            def s3(rng, slot):
                t, q = rng.choice(P['c3'])
                m = slot.marks or (2 if slot.d <= 2 else 3 if slot.d == 3 else 4)
                return dict(stem=body(t, q) + q[1], answer=q[2], type='short', marks=m,
                            markingKey=f'{q[2]} — अनुमान/निष्कर्ष पाठ के प्रमाण पर आधारित हो; प्रत्येक उचित, पाठ-आधारित बिंदु के लिए 1 अंक (अधिकतम {m})।')
            self.add(key, 'C3', (1, 5), s3, 'short', style, 'tx_s3')
        if P['c4']:
            def s4(rng, slot):
                t, q = rng.choice(P['c4'])
                m = slot.marks or (4 if slot.d <= 3 else 6)
                return dict(stem=body(t) + q[1], answer=q[2], type='explain', marks=m,
                            markingKey=f'{q[2]} — {m} अंक: स्पष्ट मत (1), पाठ से प्रमाण (1–2), अपने अनुभव/ज्ञान से तर्क (1–2), सुसंगत और शुद्ध भाषा (1)।')
            self.add(key, 'C4', (2, 5), s4, 'explain', style, 'tx_s4')

            def _sents(t):
                return [x.strip() for x in re.split(r'(?<=[।?!])\s+', t['body']) if x.strip()]

            def s4b(rng, slot):
                t, q = rng.choice(P['c4'])
                part = ' '.join(_sents(t)[:3])
                src = 'वक्ता' if which.startswith('audio') else 'लेखक'
                m = slot.marks or 4
                return dict(stem=f'{lead2(t)}\n\n{part}\n\n{src} ने जो मुद्दा उठाया है, उसे अपनी संस्कृति या समुदाय के अनुभव से जोड़िए: क्या वहाँ स्थिति समान है या भिन्न? उदाहरण सहित 100–120 शब्दों में लिखिए।',
                            answer=f'विचार-बिंदु: {q[2]} — अपनी संस्कृति से ठोस तुलना और उदाहरण।', type='explain', marks=m,
                            markingKey=f'{m} अंक: मुद्दे की सही पहचान (1), अपनी संस्कृति से तुलना (1–2), ठोस उदाहरण (1), सुसंगत भाषा (शेष)।')
            self.add(key, 'C4', (3, 5), s4b, 'explain', style, 'tx_s4b')

            def s4c(rng, slot):
                t, q = rng.choice(P['c4'])
                part = ' '.join(_sents(t)[-3:])
                src = 'वक्ता' if which.startswith('audio') else 'लेखक'
                m = slot.marks or 4
                return dict(stem=f'{lead2(t)}\n\n{part}\n\nक्या आप {src} के निष्कर्ष से सहमत हैं? {src} को संबोधित करते हुए 80–100 शब्दों की एक प्रतिक्रिया (टिप्पणी) लिखिए जिसमें आपका मत और एक तर्क हो।',
                            answer=f'विचार-बिंदु: {q[2]} — स्पष्ट सहमति/असहमति, एक विकसित तर्क, विनम्र संबोधन।', type='explain', marks=m,
                            markingKey=f'{m} अंक: स्पष्ट मत (1), अंश से जुड़ा विकसित तर्क (1–2), प्रतिक्रिया के अनुरूप संबोधन और लहजा (1), शुद्ध भाषा (शेष)।')
            self.add(key, 'C4', (3, 5), s4c, 'explain', style, 'tx_s4c')

    # ---- writing ----------------------------------------------------------------------------
    def p1(self, key, th, focus='', d=(4, 5)):
        """Theme-based Paper 1 tasks (style p1)."""
        cn = th['name']

        def p1(rng, slot):
            sit, tt, bl = rng.choice(th['tasks'])
            nm = TT[tt]['name']
            m = slot.marks or 15
            f = rng.choice([0, 1])
            if f == 0:
                stem = f'{sit}\nइस स्थिति के लिए एक {nm} लिखिए। अपने उत्तर में:\n{_bul(bl)}\n{focus}\nशब्द-सीमा: {WORDS}।'
            else:
                stem = f'पेपर 1 का कार्य (विषय: {cn})\n{sit}\nउपयुक्त प्रारूप में {nm} लिखिए और इन बिंदुओं पर विचार कीजिए — {"; ".join(bl)}। {focus} ({WORDS})'
            ans = (f'अपेक्षित उत्तर: {nm} की परंपराएँ — {"; ".join(TT[tt]["conv"][:3])}। विषय-वस्तु — {"; ".join(bl)}। '
                   f'रजिस्टर — {TT[tt]["reg"]}; पाठक — {TT[tt]["aud"]}।')
            return dict(stem=stem.replace('\n\n', '\n'), answer=ans, markingKey=p1_key(m), type='long', marks=m, minutes=40)
        self.add(key, 'C4', d, p1, 'long', 'p1', 'p1')

    def writing(self, key, th, tt, tasks):
        """Text-type subtopic: tasks = [(situation, [bullets])] for this text type."""
        cn = th['name']
        X = TT[tt]
        nm = X['name']
        others = [k for k, v in TT.items() if v['grp'] != X['grp']]

        def conv_yes(rng, slot):
            sit, bl = rng.choice(tasks)
            c = rng.choice(X['conv'])
            w = [rng.choice(TT[k]['conv']) for k in rng.sample(others, 3)]
            return mcq(rng, f'स्थिति: {sit}\nइस {nm} के प्रारूप में निम्नलिखित में से कौन-सी विशेषता सबसे उपयुक्त होगी?', c, w,
                       f'{nm} की एक प्रमुख परंपरा है — {c}। बाकी विकल्प दूसरे पाठ-प्रकारों की विशेषताएँ हैं।')
        self.add(key, 'C1', (1, 3), conv_yes, 'mcq', None, 'w_conv')

        def conv_no(rng, slot):
            sit, bl = rng.choice(tasks)
            right = rng.sample(X['conv'], 3)
            k = rng.choice(others)
            wrong = rng.choice(TT[k]['conv'])
            return mcq(rng, f'‘{cn}’ विषय पर {nm} लिखते समय निम्नलिखित में से कौन-सी विशेषता इस पाठ-प्रकार के लिए उपयुक्त नहीं है?\n(संदर्भ: {sit})',
                       wrong, right, f'‘{wrong}’ — यह {TT[k]["name"]} की विशेषता है, {nm} की नहीं।')
        self.add(key, 'C1', (2, 3), conv_no, 'mcq', None, 'w_convno')

        def register(rng, slot):
            sit, bl = rng.choice(tasks)
            return dict(stem=f'स्थिति: {sit}\nइस {nm} के लिए कैसा रजिस्टर और लहजा उपयुक्त होगा? पाठक और उद्देश्य का उल्लेख करते हुए समझाइए।',
                        answer=f'रजिस्टर: {X["reg"]}। पाठक: {X["aud"]}। कारण: पाठक से संबंध और उद्देश्य ({bl[0]}) के अनुसार भाषा का स्तर तय होता है।',
                        type='explain', marks=3, markingKey=f'1 अंक उपयुक्त रजिस्टर ({X["reg"]}); 1 अंक पाठक की पहचान ({X["aud"]}); 1 अंक उद्देश्य से जोड़कर कारण।')
        self.add(key, 'C2', (2, 4), register, 'explain', None, 'w_reg')

        def why_conv(rng, slot):
            sit, bl = rng.choice(tasks)
            a, b = rng.sample(X['conv'], 2)
            return dict(stem=f'‘{sit}’ — इस कार्य के लिए {nm} में (क) {a} और (ख) {b} क्यों आवश्यक हैं? प्रत्येक का पाठक पर प्रभाव समझाइए।',
                        answer=f'(क) {a} — इससे पाठ-प्रकार तुरंत पहचाना जाता है और पाठक को संदर्भ मिलता है। (ख) {b} — इससे उद्देश्य पूरा होता है और पाठक जुड़ाव महसूस करता है।',
                        type='explain', marks=4, markingKey='प्रत्येक विशेषता के लिए 2 अंक: 1 अंक कार्य/उद्देश्य बताने पर, 1 अंक पाठक पर प्रभाव से जोड़ने पर (मानदंड C — अवधारणात्मक समझ)।')
        self.add(key, 'C2', (2, 4), why_conv, 'explain', None, 'w_why')

        def opening(rng, slot):
            sit, bl = rng.choice(tasks)
            return dict(stem=f'स्थिति: {sit}\nइस {nm} का केवल आरंभिक भाग (40–60 शब्द) लिखिए, जिसमें पाठ-प्रकार की आरंभिक परंपराएँ स्पष्ट हों।',
                        answer=f'अपेक्षित: {X["conv"][0]}; विषय का परिचय ({bl[0]}); {X["reg"]}।', type='short', marks=4,
                        markingKey=f'2 अंक: आरंभ की परंपराएँ ({X["conv"][0]}); 1 अंक: विषय का स्पष्ट परिचय; 1 अंक: उपयुक्त रजिस्टर और शुद्ध भाषा।')
        self.add(key, 'C3', (2, 4), opening, 'short', None, 'w_open')

        def closing(rng, slot):
            sit, bl = rng.choice(tasks)
            return dict(stem=f'आपने ‘{sit}’ विषय पर {nm} का मुख्य भाग लिख लिया है। अब इसका समापन (30–50 शब्द) लिखिए, जो पाठ-प्रकार और उद्देश्य के अनुरूप हो।',
                        answer=f'अपेक्षित: मुख्य संदेश का सार ({bl[-1]}), पाठ-प्रकार के अनुरूप समापन ({X["conv"][2]}), {X["reg"]}।', type='short', marks=3,
                        markingKey='1 अंक: मुख्य संदेश का सार; 1 अंक: पाठ-प्रकार के अनुरूप समापन की परंपरा; 1 अंक: उपयुक्त लहजा और शुद्ध भाषा।')
        self.add(key, 'C3', (2, 4), closing, 'short', None, 'w_close')

        def plan(rng, slot):
            sit, bl = rng.choice(tasks)
            return dict(stem=f'स्थिति: {sit}\nइस {nm} की रूपरेखा बनाइए: शीर्षक/संबोधन, तीन मुख्य अनुच्छेदों के विचार (प्रत्येक के साथ एक उदाहरण) और समापन।',
                        answer=f'अपेक्षित रूपरेखा: {X["conv"][0]}; अनुच्छेद — {"; ".join(bl)}; समापन — {X["conv"][2]}।', type='short', marks=5,
                        markingKey='5 अंक: पाठ-प्रकार के अनुरूप आरंभ (1), तीन प्रासंगिक और तार्किक क्रम वाले बिंदु (3), समापन (1)।')
        self.add(key, 'C3', (3, 5), plan, 'short', None, 'w_plan')

        def full(rng, slot):
            sit, bl = rng.choice(tasks)
            m = slot.marks or 15
            if rng.random() < 0.5:
                stem = f'{sit}\nइस स्थिति के लिए एक {nm} लिखिए। अपने उत्तर में:\n{_bul(bl)}\nशब्द-सीमा: {WORDS}।'
            else:
                stem = f'लेखन कार्य — {nm}\n{sit}\nपाठक, उद्देश्य और संदर्भ को ध्यान में रखते हुए लिखिए और ये बिंदु शामिल कीजिए: {"; ".join(bl)}। ({WORDS})'
            ans = f'अपेक्षित उत्तर: {nm} की परंपराएँ — {"; ".join(X["conv"])}। विषय-वस्तु — {"; ".join(bl)}। रजिस्टर — {X["reg"]}।'
            return dict(stem=stem, answer=ans, markingKey=p1_key(m), type='long', marks=m, minutes=40)
        self.add(key, 'C4', (3, 5), full, 'long', 'p1', 'w_full')

    def register_shift(self, key, th, pairs):
        """pairs: (informal sentence, formal sentence)."""
        cn = th['name']

        def fn(rng, slot):
            a, b = rng.choice(pairs)
            if rng.random() < 0.5:
                return dict(stem=f'यह वाक्य एक मित्र को लिखे संदेश से है: “{a}”\nइसे ‘{cn}’ विषय पर औपचारिक पत्र या रिपोर्ट के लिए उपयुक्त औपचारिक भाषा में फिर से लिखिए।',
                            answer=b, type='short', marks=2, markingKey=f'नमूना: {b} — 1 अंक: आदरसूचक/औपचारिक शब्दावली; 1 अंक: अर्थ सुरक्षित और वाक्य शुद्ध।')
            return dict(stem=f'औपचारिक वाक्य: “{b}”\nइसी बात को मित्र को भेजे जाने वाले अनौपचारिक संदेश की स्वाभाविक भाषा में लिखिए और बताइए कि आपने कौन-से दो बदलाव किए।',
                        answer=f'नमूना: {a} (बदलाव: ‘आप’ के स्थान पर ‘तुम’, औपचारिक शब्दों के स्थान पर बोलचाल के शब्द)', type='short', marks=3,
                        markingKey='1 अंक: स्वाभाविक अनौपचारिक वाक्य; 2 अंक: दो बदलावों की सही पहचान (सर्वनाम/क्रिया-रूप, शब्दावली, वाक्य-लंबाई)।')
        self.add(key, 'C3', (2, 4), fn, 'short', None, 'reg_shift')

    # ---- oral -------------------------------------------------------------------------------
    def oral(self, key, th, phrases=True):
        cn = th['name']
        D = th['discuss']
        if phrases:
            def ph(rng, slot):
                f, p, w = rng.choice(ORAL_PHRASES)
                return mcq(rng, f'‘{cn}’ पर शिक्षक के साथ मौखिक चर्चा में आप {f} चाहते हैं। इसके लिए सबसे उपयुक्त वाक्यांश कौन-सा है?', p, w,
                           f'{f} के लिए ‘{p}’ उपयुक्त है।')
            self.add(key, 'C1', (1, 3), ph, 'mcq', None, 'o_phrase')

        def d2(rng, slot):
            q, pts = rng.choice(D)
            return dict(stem=f'मौखिक चर्चा का प्रश्न: “{q}”\nइस प्रश्न पर अपना मत दो कारणों सहित संक्षेप में (50–70 शब्द) स्पष्ट कीजिए।',
                        answer='संभावित बिंदु: ' + '; '.join(pts), type='explain', marks=3,
                        markingKey='1 अंक स्पष्ट मत के लिए; 2 अंक दो प्रासंगिक, विकसित कारणों के लिए। ' + 'संभावित बिंदु: ' + '; '.join(pts))
        self.add(key, 'C2', (1, 4), d2, 'explain', None, 'o_d2')

        def d3(rng, slot):
            q, pts = rng.choice(D)
            return dict(stem=f'शिक्षक आपसे पूछते हैं: “{q}” — अपने देश या समुदाय के एक ठोस उदाहरण के साथ 80–100 शब्दों में उत्तर दीजिए और अंत में शिक्षक से एक प्रति-प्रश्न पूछिए।',
                        answer='संभावित बिंदु: ' + '; '.join(pts) + '। प्रति-प्रश्न विषय से जुड़ा और खुला हो।', type='short', marks=4,
                        markingKey='1 अंक मत; 1 अंक ठोस, प्रासंगिक उदाहरण; 1 अंक तर्क का विकास; 1 अंक संवाद को आगे बढ़ाने वाला प्रति-प्रश्न (मानदंड C — संवाद-कौशल)।')
        self.add(key, 'C3', (2, 4), d3, 'short', None, 'o_d3')

        def d4(rng, slot):
            q, pts = rng.choice(D)
            m = 6 if slot.d >= 4 else 4
            return dict(stem=f'“{q}” — इस प्रश्न पर पक्ष और विपक्ष, दोनों के तर्क प्रस्तुत कीजिए और फिर संतुलित निष्कर्ष दीजिए (मौखिक प्रस्तुति की तैयारी, 120–150 शब्द)।',
                        answer='पक्ष/विपक्ष के संभावित बिंदु: ' + '; '.join(pts) + '। निष्कर्ष तर्कों से निकले और स्पष्ट हो।', type='explain', marks=m,
                        markingKey=f'{m} अंक: पक्ष के तर्क ({m // 3}), विपक्ष के तर्क ({m // 3}), तर्कसंगत निष्कर्ष और सुसंगत भाषा ({m - 2 * (m // 3)})।')
        self.add(key, 'C4', (2, 5), d4, 'explain', None, 'o_d4')

        if th.get('pics'):
            P = th['pics']

            def pic1(rng, slot):
                desc, pts = rng.choice(P)
                return dict(stem=f'दृश्य उद्दीपन (चित्र का विवरण): {desc}\nचित्र में दिखाई देने वाली तीन बातों का वर्णन कीजिए और बताइए कि यह चित्र ‘{cn}’ विषय से कैसे जुड़ा है।',
                            answer='संभावित उत्तर: ' + '; '.join(pts), type='short', marks=4,
                            markingKey='3 अंक: चित्र के तीन सटीक विवरण (स्थान, लोग, गतिविधि); 1 अंक: विषय से स्पष्ट संबंध।')
            self.add(key, 'C3', (1, 4), pic1, 'short', None, 'o_pic')

            def pic2(rng, slot):
                desc, pts = rng.choice(P)
                m = 6 if slot.d >= 4 else 5
                return dict(stem=f'दृश्य उद्दीपन: {desc}\nइस चित्र पर 3–4 मिनट की मौखिक प्रस्तुति की योजना बनाइए: वर्णन, विषय से संबंध, अपनी संस्कृति से तुलना और एक व्यक्तिगत विचार।',
                            answer='संभावित योजना: ' + '; '.join(pts) + '; अपनी संस्कृति से तुलना; व्यक्तिगत निष्कर्ष।', type='explain', marks=m,
                            markingKey=f'{m} अंक: सटीक वर्णन (1), विषय से संबंध (1–2), सांस्कृतिक तुलना (1–2), व्यक्तिगत, तर्कसंगत विचार (1)।')
            self.add(key, 'C4', (2, 5), pic2, 'explain', None, 'o_pic4')

    # ---- whole subtopic ---------------------------------------------------------------------
    def setup(self, key, kind, th, spec=None):
        spec = spec or {}
        focus = spec.get('focus', '')
        if kind == 'vocab':
            self.vocab(key, th)
        elif kind == 'reading':
            self.texts(key, th, 'texts', 'p2r')
            self.vocab(key, th, ('c2', 'c3'))
        elif kind == 'listening':
            self.texts(key, th, 'audio', 'p2l')
            self.vocab(key, th, ('c1', 'c2', 'c3'))
        elif kind == 'writing':
            self.writing(key, th, spec['tt'], spec['tasks'])
        elif kind == 'oral':
            self.oral(key, th)
            self.vocab(key, th, ('c2', 'c3'))
        elif kind == 'none':
            self.vocab(key, th, ('c3',))
        if spec.get('items'):
            self.items(key, spec['items'])
        for g in spec.get('gens', []):
            g(self, key, th)
        if spec.get('p1', True):
            self.p1(key, th, focus)


KIT = Kit(R)


# --------------------------------------------------------------------------------------------
# Grammar generators (bank-driven)
# --------------------------------------------------------------------------------------------
def g_transform(bank, label_a, label_b, c=('C3',), marks=2, both=True, extra_key=''):
    """bank: list of (a, b). Asks to change a -> b (and b -> a when both)."""
    def gen(kit, key, th):
        def fn(rng, slot):
            a, b = rng.choice(bank)
            if both and rng.random() < 0.5:
                return dict(stem=f'निम्नलिखित वाक्य को {label_a} में बदलिए:\n“{b}”', answer=a, type='short', marks=marks,
                            markingKey=f'{a} {extra_key}'.strip())
            return dict(stem=f'निम्नलिखित वाक्य को {label_b} में बदलिए:\n“{a}”', answer=b, type='short', marks=marks,
                        markingKey=f'{b} {extra_key}'.strip())
        kit.add(key, c, (1, 4), fn, 'short', None, 'g_tr')
    return gen


def g_choose_form(bank, labels, c='C2', name='g_form'):
    """bank: list of tuples of forms aligned with labels; MCQ: pick the form for a target label."""
    def gen(kit, key, th):
        def fn(rng, slot):
            row = rng.choice(bank)
            i, j = rng.sample(range(len(labels)), 2)
            others = [row[k] for k in range(len(labels)) if k != j]
            if len(set(others + [row[j]])) < 4:
                return None
            return mcq(rng, f'वाक्य “{row[i]}” का {labels[j]} वाला रूप कौन-सा है?', row[j], rng.sample(others, 3),
                       f'{labels[j]}: {row[j]}')
        kit.add(key, c, (1, 4), fn, 'mcq', None, name)

        def ident(rng, slot):
            row = rng.choice(bank)
            j = rng.randrange(len(labels))
            others = [l for k, l in enumerate(labels) if k != j]
            return mcq(rng, f'निम्नलिखित वाक्य में किस रूप/काल का प्रयोग हुआ है?\n“{row[j]}”', labels[j], rng.sample(others, 3),
                       f'“{row[j]}” — {labels[j]}।')
        kit.add(key, 'C1', (1, 3), ident, 'mcq', 'p2r', name + '_id')

        def tr(rng, slot):
            row = rng.choice(bank)
            i, j = rng.sample(range(len(labels)), 2)
            return dict(stem=f'वाक्य को {labels[j]} में बदलकर लिखिए:\n“{row[i]}”', answer=row[j], type='short', marks=2,
                        markingKey=f'{row[j]} — 1 अंक सही क्रिया-रूप के लिए, 1 अंक लिंग-वचन की सही अन्विति (और आवश्यकता होने पर ‘ने’) के लिए।')
        kit.add(key, 'C3', (1, 4), tr, 'short', None, name + '_tr')

        def para(rng, slot):
            rows = rng.sample(bank, 3)
            i, j = rng.sample(range(len(labels)), 2)
            src = ' '.join(r[i] for r in rows)
            ans = ' '.join(r[j] for r in rows)
            return dict(stem=f'नीचे दिए गए अनुच्छेद के सभी वाक्यों को {labels[j]} में बदलकर फिर से लिखिए:\n“{src}”', answer=ans, type='short',
                        marks=3, markingKey=f'{ans} — प्रत्येक सही रूपांतरित वाक्य के लिए 1 अंक (क्रिया-रूप और अन्विति दोनों सही होने चाहिए)।')
        kit.add(key, 'C3', (3, 5), para, 'short', None, name + '_para')
    return gen


def g_free(prompts, c='C4', marks=6, name='g_free'):
    """prompts: (stem, answer). Written production with a grammar focus."""
    def gen(kit, key, th):
        def fn(rng, slot):
            s, a = rng.choice(prompts)
            topic = rng.choice(th['topics'])
            return dict(stem=s.format(topic=topic), answer=a, type='long', marks=marks, markingKey=para_key(marks, a))
        kit.add(key, c, (2, 5), fn, 'long', None, name)
    return gen


# ============================================================================================
# G11 THEMES
# ============================================================================================
TH = {}

TH[1] = dict(
    name='जीवन-शैली',
    vocab=[
        ('दिनचर्या', 'रोज़ के कामों का नियमित क्रम', 'रोज़मर्रा', 'परीक्षा के दिनों में मेरी ____ बदल जाती है; मैं सुबह पाँच बजे उठने लगता हूँ।'),
        ('पौष्टिक', 'शरीर को पोषण देने वाला', 'पोषक', 'माँ कहती हैं कि नाश्ते में ____ भोजन, जैसे दलिया, अंकुरित दालें और फल, लेना चाहिए।'),
        ('गतिहीन', 'जिसमें शारीरिक हलचल बहुत कम हो', 'निष्क्रिय', 'दिन भर कुर्सी पर बैठे रहने वाली ____ जीवन-शैली मोटापे का कारण बन सकती है।'),
        ('संतुलन', 'दो या अधिक चीज़ों के बीच उचित अनुपात', 'सामंजस्य', 'पढ़ाई और खेल-कूद के बीच ____ बनाए रखना ज़रूरी है।'),
        ('आदत', 'बार-बार करने से स्वाभाविक बन गया व्यवहार', 'अभ्यास', 'रात को सोने से पहले फ़ोन देखने की ____ छोड़ना कठिन है।'),
        ('उपभोक्ता', 'वस्तुएँ या सेवाएँ ख़रीदकर उपयोग करने वाला व्यक्ति', 'ग्राहक', 'आज का जागरूक ____ ऑनलाइन ख़रीदारी से पहले समीक्षाएँ पढ़ता है।'),
        ('शाकाहारी', 'मांस, मछली और अंडा न खाने वाला', 'निरामिष', 'रोहन पूरी तरह ____ है; वह अंडा भी नहीं खाता।'),
        ('फ़ुर्सत', 'काम से खाली समय', 'अवकाश', 'सप्ताहांत में ____ मिलते ही मैं बालकनी में बागवानी करती हूँ।'),
        ('सादगी', 'दिखावे से रहित सरल जीवन', 'सरलता', 'दादाजी की ____ सबको प्रभावित करती है; वे बहुत कम चीज़ों में खुश रहते हैं।'),
        ('व्यस्त', 'जिसके पास खाली समय न हो', 'मशगूल', 'महानगर की ____ ज़िंदगी में परिवार के साथ बैठकर भोजन करना भी मुश्किल हो गया है।'),
        ('स्वावलंबी', 'अपने काम स्वयं करने वाला', 'आत्मनिर्भर', 'छात्रावास में रहकर नेहा ____ बन गई; अब वह अपने कपड़े ख़ुद धोती है और खाना भी बना लेती है।'),
        ('फ़िज़ूलख़र्ची', 'अनावश्यक चीज़ों पर पैसा उड़ाना', 'अपव्यय', 'हर महीने नए जूते ख़रीदना ____ के सिवा कुछ नहीं है।'),
        ('अनुशासन', 'नियमों और समय का दृढ़ता से पालन', 'नियमबद्धता', 'सेना के जवानों का जीवन कड़े ____ से बँधा होता है।'),
        ('प्रवृत्ति', 'किसी ओर बढ़ता झुकाव या रुझान', 'रुझान', 'युवाओं में घर बैठे खाना मँगवाने की ____ तेज़ी से बढ़ रही है।'),
    ],
    topics=['मेरी दिनचर्या और स्वस्थ आदतें', 'शहर और गाँव की जीवन-शैली', 'फ़ास्ट फ़ूड बनाम घर का खाना', 'सप्ताहांत कैसे बिताएँ',
            'सादा जीवन, उच्च विचार', 'ऑनलाइन ख़रीदारी की बढ़ती आदत', 'किशोरों की नींद और स्क्रीन-टाइम'],
    texts=[
        dict(kind='लेख', title='धीमी ज़िंदगी की ओर लौटते युवा',
             body='बेंगलुरु की चौबीस वर्षीय सॉफ़्टवेयर इंजीनियर तन्वी हर रविवार को ‘डिजिटल उपवास’ रखती हैं। उस दिन वे फ़ोन बंद कर देती हैं, बाज़ार से सब्ज़ियाँ ख़ुद ख़रीदती हैं और दोस्तों के साथ धीरे-धीरे खाना पकाती हैं। तन्वी कहती हैं, “पहले मैं हर समय थकी रहती थी; अब पूरे सप्ताह की ऊर्जा इसी एक दिन से मिलती है।” समाजशास्त्रियों के अनुसार महानगरों में ऐसे युवाओं की संख्या बढ़ रही है जो कम चीज़ों में संतोष चाहते हैं।',
             qs=[('C1', 'तन्वी ‘डिजिटल उपवास’ कब रखती हैं?', 'हर रविवार को', ['हर शनिवार को', 'महीने में एक बार', 'काम के दिनों में']),
                 ('C1', 'पाठ से वह शब्द चुनिए जिसका अर्थ ‘संतुष्टि’ है।', 'संतोष'),
                 ('C2', 'लेखक ने ‘डिजिटल उपवास’ शब्द का प्रयोग किस अर्थ में किया है? अपने शब्दों में समझाइए।', 'एक तय समय के लिए फ़ोन और डिजिटल उपकरणों से जान-बूझकर दूर रहना — जैसे उपवास में भोजन छोड़ा जाता है, वैसे ही यहाँ स्क्रीन छोड़ी जाती है।'),
                 ('tf', 'डिजिटल उपवास के बाद तन्वी की थकान और बढ़ गई है।', 'गलत', '“अब पूरे सप्ताह की ऊर्जा इसी एक दिन से मिलती है।”'),
                 ('tf', 'समाजशास्त्रियों के अनुसार सादा जीवन चाहने वाले युवाओं की संख्या घट रही है।', 'गलत', '“महानगरों में ऐसे युवाओं की संख्या बढ़ रही है।”'),
                 ('C3', 'तन्वी सब्ज़ियाँ ख़ुद ख़रीदने और धीरे-धीरे खाना पकाने को महत्व क्यों देती होंगी? पाठ के आधार पर अनुमान लगाइए।', 'ये काम उसे भाग-दौड़ से हटकर धीमी गति से जीने और दोस्तों के साथ समय बिताने का अवसर देते हैं, जिससे थकान दूर होती है और ऊर्जा मिलती है।'),
                 ('C3', 'पाठ के अनुसार तन्वी की जीवन-शैली में आए परिवर्तन का मुख्य कारण क्या था?', 'लगातार थकान', ['ऊँचा वेतन', 'दोस्तों का दबाव', 'नई नौकरी']),
                 ('C4', 'क्या ‘डिजिटल उपवास’ हर विद्यार्थी के लिए व्यावहारिक है? पाठ के विचारों और अपने अनुभव के आधार पर 80–100 शब्दों में तर्कसंगत उत्तर दीजिए।', 'संभावित पक्ष: थकान और तनाव घटता है, परिवार-मित्रों के लिए समय मिलता है (तन्वी का उदाहरण)। विपक्ष: ऑनलाइन कक्षाएँ और गृहकार्य फ़ोन पर निर्भर हैं, इसलिए पूरा दिन संभव नहीं; आंशिक उपवास (कुछ घंटे) अधिक व्यावहारिक।')]),
        dict(kind='ब्लॉग प्रविष्टि', title='मेरी दादी का रसोईघर — 14 अगस्त',
             body='नमस्ते दोस्तो! इस गर्मी की छुट्टियों में मैं लखनऊ में दादी के पास रहा। वहाँ न माइक्रोवेव था, न पैकेट वाला खाना। दादी सुबह छह बजे उठकर आँगन में तुलसी को पानी देतीं, फिर मौसमी सब्ज़ियों से सादा खाना बनातीं। शुरू-शुरू में मुझे पिज़्ज़ा की बहुत याद आई, लेकिन दो हफ़्तों में मेरी नींद सुधर गई और पेट की शिकायत भी ग़ायब हो गई। क्या आपके घर में भी कोई ऐसी परंपरा है? नीचे टिप्पणी में ज़रूर बताइए!',
             qs=[('C1', 'लेखक गर्मी की छुट्टियों में कहाँ रहा?', 'लखनऊ में दादी के पास', ['बेंगलुरु में दोस्तों के साथ', 'छात्रावास में', 'अपने माता-पिता के साथ विदेश में']),
                 ('C1', 'दादी सुबह उठकर सबसे पहले क्या करती थीं?', 'आँगन में तुलसी को पानी देती थीं'),
                 ('C1', 'पाठ में आए शब्द ‘ग़ायब’ का अर्थ लिखिए।', 'लुप्त / समाप्त हो जाना / दिखाई न देना'),
                 ('C2', '“शुरू-शुरू में मुझे पिज़्ज़ा की बहुत याद आई” — इस वाक्य से लेखक की किस भावना का पता चलता है?', 'नई, सादी जीवन-शैली को अपनाने में आरंभिक कठिनाई और अपनी पुरानी खान-पान की आदतों के प्रति लगाव।'),
                 ('tf', 'दादी के घर में तैयार पैकेट वाला खाना मिलता था।', 'गलत', '“वहाँ न माइक्रोवेव था, न पैकेट वाला खाना।”'),
                 ('tf', 'दो हफ़्तों में लेखक की नींद बेहतर हो गई।', 'सही', '“दो हफ़्तों में मेरी नींद सुधर गई।”'),
                 ('C3', 'ब्लॉग की कौन-सी दो भाषिक विशेषताएँ बताती हैं कि लेखक पाठकों से सीधा संबंध बनाना चाहता है? उदाहरण दीजिए।', '‘नमस्ते दोस्तो!’ जैसा मित्रवत संबोधन; अंत में प्रश्न ‘क्या आपके घर में भी कोई ऐसी परंपरा है?’ और टिप्पणी करने का आमंत्रण।'),
                 ('C3', 'लेखक के स्वास्थ्य में सुधार का कारण संभवतः क्या था?', 'दादी का सादा, मौसमी और नियमित भोजन', ['पिज़्ज़ा खाना', 'माइक्रोवेव का प्रयोग', 'देर से उठना']),
                 ('C4', 'लेखक के अनुभव के आधार पर बताइए कि क्या पारंपरिक जीवन-शैली आधुनिक शहरी जीवन से बेहतर है। संतुलित उत्तर दीजिए (80–100 शब्द)।', 'पक्ष: मौसमी भोजन, नियमित दिनचर्या, बेहतर नींद और पाचन (ब्लॉग के उदाहरण)। विपक्ष: आधुनिक जीवन में सुविधाएँ, समय की बचत, विविधता। निष्कर्ष: दोनों का संतुलन — पारंपरिक आदतों को आधुनिक जीवन में अपनाना।')]),
        dict(kind='विज्ञापन', title='‘फ़िटबस्ती’ — अब सेहत आपके मोहल्ले में!',
             body='थक गए हैं महँगे जिम से? ‘फ़िटबस्ती’ लाया है आपके पास के पार्क में सुबह और शाम की सामूहिक कसरत। प्रशिक्षित कोच, योग, ज़ुम्बा और दौड़ने के समूह — सब कुछ केवल 299 रुपये महीने में! पहला सप्ताह बिल्कुल मुफ़्त। बुज़ुर्गों और विद्यार्थियों के लिए विशेष छूट। आज ही ऐप डाउनलोड कीजिए या 98XXX-XXXXX पर संदेश भेजिए। ‘फ़िटबस्ती’ — चलिए, साथ-साथ स्वस्थ बनें!',
             qs=[('C1', '‘फ़िटबस्ती’ की कसरत कहाँ होती है?', 'आस-पास के पार्क में', ['महँगे जिम में', 'घर पर ऑनलाइन', 'विद्यालय के मैदान में']),
                 ('C1', 'पहले सप्ताह के लिए कितना शुल्क देना होगा?', 'कुछ नहीं (पहला सप्ताह मुफ़्त है)'),
                 ('C2', 'विज्ञापन की शुरुआत प्रश्न (“थक गए हैं महँगे जिम से?”) से क्यों की गई है? समझाइए।', 'प्रश्न सीधे पाठक की समस्या (महँगा जिम) को छूता है, उसका ध्यान खींचता है और उसे तुरंत समाधान पढ़ने के लिए प्रेरित करता है।'),
                 ('tf', '‘फ़िटबस्ती’ में विद्यार्थियों को कोई छूट नहीं मिलती।', 'गलत', '“बुज़ुर्गों और विद्यार्थियों के लिए विशेष छूट।”'),
                 ('C3', 'विज्ञापन किस प्रकार के लोगों को सबसे अधिक आकर्षित करना चाहता है? पाठ से दो प्रमाण दीजिए।', 'वे लोग जो कम ख़र्च में और घर के पास व्यायाम करना चाहते हैं — ‘थक गए हैं महँगे जिम से?’, ‘केवल 299 रुपये महीने में’, ‘पास के पार्क में’।'),
                 ('C3', 'नारे “चलिए, साथ-साथ स्वस्थ बनें!” का मुख्य संदेश क्या है?', 'सामूहिक रूप से व्यायाम करना अधिक प्रेरक है', ['अकेले व्यायाम करना बेहतर है', 'जिम जाना आवश्यक है', 'स्वास्थ्य के लिए दवा ज़रूरी है']),
                 ('C4', 'क्या यह विज्ञापन किसी गतिहीन किशोर को व्यायाम शुरू करने के लिए प्रेरित कर पाएगा? विज्ञापन की भाषा और प्रस्तावों के आधार पर मूल्यांकन कीजिए।', 'प्रेरक तत्व: मुफ़्त सप्ताह, कम शुल्क, छूट, समूह का साथ, आज्ञार्थक नारा। सीमाएँ: किशोरों की रुचि (खेल, ऐप-आधारित चुनौतियाँ) का सीधा उल्लेख नहीं; सुबह का समय विद्यालय से टकरा सकता है। संतुलित निष्कर्ष आवश्यक।')]),
    ],
    tasks=[
        ('आपके विद्यालय की ऑनलाइन पत्रिका ‘स्वस्थ किशोर’ विषय पर विद्यार्थियों के लेख आमंत्रित कर रही है। आप अपनी दिनचर्या में किए गए एक बदलाव के बारे में लिखना चाहते हैं।', 'blog',
         ['आपने कौन-सा बदलाव किया और क्यों', 'इस बदलाव से आपके जीवन पर क्या प्रभाव पड़ा', 'दूसरे विद्यार्थियों के लिए सुझाव']),
        ('आपके शहर के एक समाचार-पत्र में छपा है कि किशोर दिन में औसतन सात घंटे स्क्रीन के सामने बिताते हैं। आप इस विषय पर पत्रिका के लिए एक लेख लिखना चाहते हैं।', 'article',
         ['समस्या के कारण', 'स्वास्थ्य और पढ़ाई पर प्रभाव', 'परिवार और विद्यालय क्या कर सकते हैं']),
        ('आपका मित्र विदेश से भारत आकर आपके परिवार के साथ एक सप्ताह रहने वाला है। वह जानना चाहता है कि भारतीय परिवारों की दिनचर्या और खान-पान कैसा होता है।', 'pletter',
         ['आपके परिवार की सामान्य दिनचर्या', 'खान-पान की विशेषताएँ और शिष्टाचार', 'उसे किन बातों के लिए तैयार रहना चाहिए']),
        ('आपके विद्यालय की कैंटीन में तला-भुना और मीठा खाना अधिक बिकता है। विद्यार्थी परिषद के सदस्य के रूप में आप प्रधानाचार्य को पत्र लिखना चाहते हैं।', 'fletter',
         ['वर्तमान स्थिति और उसके दुष्प्रभाव', 'कैंटीन के लिए ठोस सुझाव', 'विद्यार्थियों की ओर से सहयोग का आश्वासन']),
        ('विद्यालय की प्रातः सभा में आपको ‘सादा जीवन, उच्च विचार — क्या आज भी प्रासंगिक है?’ विषय पर बोलना है।', 'speech',
         ['उपभोक्तावादी जीवन-शैली के उदाहरण', 'सादगी के लाभ', 'विद्यार्थियों से एक ठोस आह्वान']),
        ('आपने एक महीने तक ‘जंक फ़ूड नहीं’ चुनौती पूरी की है। आज चुनौती का अंतिम दिन है।', 'diary',
         ['पूरे महीने के अनुभव और कठिनाइयाँ', 'शरीर और मन में आए परिवर्तन', 'आगे के लिए आपका संकल्प']),
    ],
    discuss=[
        ('क्या आधुनिक जीवन-शैली ने हमें अधिक सुविधा दी है या अधिक तनाव?', ['तकनीक से समय की बचत और सुविधा', 'लंबे कार्य-घंटे, स्क्रीन-टाइम और अकेलापन', 'संतुलन व्यक्ति के चुनाव पर निर्भर']),
        ('क्या किशोरों को अपनी दिनचर्या ख़ुद तय करने की आज़ादी होनी चाहिए?', ['स्वावलंबन और ज़िम्मेदारी का विकास', 'अनुभव की कमी, नींद और पढ़ाई पर असर', 'माता-पिता के साथ मिलकर नियम बनाना']),
        ('क्या शाकाहारी भोजन पर्यावरण और स्वास्थ्य दोनों के लिए बेहतर है?', ['कम कार्बन उत्सर्जन और पानी की बचत', 'प्रोटीन और पोषण की योजना आवश्यक', 'सांस्कृतिक और व्यक्तिगत चुनाव का सम्मान']),
        ('क्या ऑनलाइन ख़रीदारी ने हमें फ़िज़ूलख़र्च बना दिया है?', ['आसान भुगतान और छूट से आवेगपूर्ण ख़रीदारी', 'समय और यात्रा की बचत, तुलना की सुविधा', 'बजट और सोच-समझकर ख़रीदने की आदत']),
        ('गाँव की जीवन-शैली से शहर के लोग क्या सीख सकते हैं?', ['प्रकृति के साथ तालमेल और मौसमी भोजन', 'समुदाय और पड़ोस का साथ', 'शहरी सुविधाओं की अपनी उपयोगिता']),
    ],
    pics=[('एक मेज़ पर चार लोगों का परिवार बैठा है; सबके हाथ में मोबाइल है और खाना ठंडा हो रहा है। दीवार की घड़ी रात के नौ बजा रही है।',
           ['परिवार साथ है पर बातचीत नहीं', 'तकनीक का पारिवारिक समय पर प्रभाव', 'भोजन के समय फ़ोन-मुक्त नियम का सुझाव']),
          ('सुबह के समय एक पार्क में अलग-अलग उम्र के लोग योग, दौड़ और खुली कसरत कर रहे हैं; एक कोने में चाय की गाड़ी है।',
           ['स्वस्थ जीवन-शैली के प्रति जागरूकता', 'सामुदायिक गतिविधि और सामाजिक मेल-जोल', 'शहरों में सार्वजनिक खुली जगहों का महत्व'])],
)

TENSE_LABELS = ['सामान्य वर्तमान काल', 'अपूर्ण वर्तमान काल', 'सामान्य भूतकाल', 'पूर्ण भूतकाल', 'सामान्य भविष्यत् काल']
TENSE_BANK = [
    ('मीरा पार्क में योग करती है।', 'मीरा पार्क में योग कर रही है।', 'मीरा ने पार्क में योग किया।', 'मीरा पार्क में योग कर चुकी थी।', 'मीरा पार्क में योग करेगी।'),
    ('हम रात को हल्का खाना खाते हैं।', 'हम रात को हल्का खाना खा रहे हैं।', 'हमने रात को हल्का खाना खाया।', 'हम रात को हल्का खाना खा चुके थे।', 'हम रात को हल्का खाना खाएँगे।'),
    ('दादाजी बरामदे में अख़बार पढ़ते हैं।', 'दादाजी बरामदे में अख़बार पढ़ रहे हैं।', 'दादाजी ने बरामदे में अख़बार पढ़ा।', 'दादाजी बरामदे में अख़बार पढ़ चुके थे।', 'दादाजी बरामदे में अख़बार पढ़ेंगे।'),
    ('अनुज साइकिल से विद्यालय जाता है।', 'अनुज साइकिल से विद्यालय जा रहा है।', 'अनुज साइकिल से विद्यालय गया।', 'अनुज साइकिल से विद्यालय जा चुका था।', 'अनुज साइकिल से विद्यालय जाएगा।'),
    ('मेरी बहन ऑनलाइन कपड़े ख़रीदती है।', 'मेरी बहन ऑनलाइन कपड़े ख़रीद रही है।', 'मेरी बहन ने ऑनलाइन कपड़े ख़रीदे।', 'मेरी बहन ऑनलाइन कपड़े ख़रीद चुकी थी।', 'मेरी बहन ऑनलाइन कपड़े ख़रीदेगी।'),
    ('माँ बाज़ार से ताज़ी सब्ज़ियाँ लाती हैं।', 'माँ बाज़ार से ताज़ी सब्ज़ियाँ ला रही हैं।', 'माँ बाज़ार से ताज़ी सब्ज़ियाँ लाईं।', 'माँ बाज़ार से ताज़ी सब्ज़ियाँ ला चुकी थीं।', 'माँ बाज़ार से ताज़ी सब्ज़ियाँ लाएँगी।'),
    ('तुम बहुत ज़्यादा चाय पीते हो।', 'तुम बहुत ज़्यादा चाय पी रहे हो।', 'तुमने बहुत ज़्यादा चाय पी।', 'तुम बहुत ज़्यादा चाय पी चुके थे।', 'तुम बहुत ज़्यादा चाय पियोगे।'),
    ('मैं शाम को झील के किनारे दौड़ती हूँ।', 'मैं शाम को झील के किनारे दौड़ रही हूँ।', 'मैं शाम को झील के किनारे दौड़ी।', 'मैं शाम को झील के किनारे दौड़ चुकी थी।', 'मैं शाम को झील के किनारे दौड़ूँगी।'),
    ('बच्चे मैदान में फ़ुटबॉल खेलते हैं।', 'बच्चे मैदान में फ़ुटबॉल खेल रहे हैं।', 'बच्चों ने मैदान में फ़ुटबॉल खेला।', 'बच्चे मैदान में फ़ुटबॉल खेल चुके थे।', 'बच्चे मैदान में फ़ुटबॉल खेलेंगे।'),
    ('पिताजी घर पर रोटियाँ बनाते हैं।', 'पिताजी घर पर रोटियाँ बना रहे हैं।', 'पिताजी ने घर पर रोटियाँ बनाईं।', 'पिताजी घर पर रोटियाँ बना चुके थे।', 'पिताजी घर पर रोटियाँ बनाएँगे।'),
    ('रिया मोबाइल पर पुराने गीत सुनती है।', 'रिया मोबाइल पर पुराने गीत सुन रही है।', 'रिया ने मोबाइल पर पुराने गीत सुने।', 'रिया मोबाइल पर पुराने गीत सुन चुकी थी।', 'रिया मोबाइल पर पुराने गीत सुनेगी।'),
    ('लोग मेट्रो से दफ़्तर पहुँचते हैं।', 'लोग मेट्रो से दफ़्तर पहुँच रहे हैं।', 'लोग मेट्रो से दफ़्तर पहुँचे।', 'लोग मेट्रो से दफ़्तर पहुँच चुके थे।', 'लोग मेट्रो से दफ़्तर पहुँचेंगे।'),
    ('नानी गमलों में पानी डालती हैं।', 'नानी गमलों में पानी डाल रही हैं।', 'नानी ने गमलों में पानी डाला।', 'नानी गमलों में पानी डाल चुकी थीं।', 'नानी गमलों में पानी डालेंगी।'),
]

SPEC = {}
SPEC['ch01-st1'] = ('vocab', dict(focus='लेखन में जीवन-शैली से जुड़ी विविध और सटीक शब्दावली (जैसे दिनचर्या, संतुलन, पौष्टिक) का प्रयोग कीजिए।', items=[
    ('C1', '‘जीवन-शैली’ शब्द का सबसे सटीक अर्थ क्या है?', 'किसी व्यक्ति या समूह के रहने, खाने, काम करने और समय बिताने का ढंग', ['केवल किसी व्यक्ति का पहनावा', 'किसी देश की शासन-व्यवस्था', 'किसी परिवार की आर्थिक स्थिति'], 'जीवन-शैली में दिनचर्या, खान-पान, आदतें और मूल्य सभी शामिल हैं।'),
    ('C1', 'इनमें से कौन-सा शब्द ‘पौष्टिक’ का विलोम है?', 'पोषणहीन', ['पोषक', 'स्वास्थ्यवर्धक', 'संतुलित'], '‘पौष्टिक’ = पोषण देने वाला; विलोम = पोषणहीन।'),
    ('C1', '‘स्वावलंबी’ शब्द में कौन-सा उपसर्ग/पूर्वपद है?', 'स्व', ['अव', 'लंबी', 'वलं'], 'स्व (अपना) + अवलंबी (आश्रित) = अपने ऊपर आश्रित।'),
    ('C2', '‘फ़ुर्सत’ और ‘आलस्य’ में अंतर स्पष्ट कीजिए।', '‘फ़ुर्सत’ काम से मिला खाली समय है, जो सकारात्मक या तटस्थ है; ‘आलस्य’ काम करने की अनिच्छा या सुस्ती है, जो नकारात्मक गुण है।', '1 अंक प्रत्येक शब्द के सही अर्थ के लिए; अंतर स्पष्ट न होने पर अधिकतम 1 अंक।'),
    ('C2', '‘व्यस्त’ और ‘अस्त-व्यस्त’ शब्दों के अर्थ का अंतर उदाहरण देकर समझाइए।', '‘व्यस्त’ = जिसके पास खाली समय न हो (माँ आज बहुत व्यस्त हैं); ‘अस्त-व्यस्त’ = बिखरा हुआ, अव्यवस्थित (परीक्षा के बाद मेरा कमरा अस्त-व्यस्त था)।', '1 अंक प्रत्येक अर्थ के लिए, 1 अंक उदाहरणों के लिए।', 3),
    ('C2', '‘गतिहीन जीवन-शैली’ से स्वास्थ्य पर पड़ने वाले दो प्रभाव बताइए और समझाइए कि यह शब्द-युग्म किस प्रकार की दिनचर्या का वर्णन करता है।', 'ऐसी दिनचर्या जिसमें व्यक्ति अधिकतर बैठा रहता है (स्क्रीन, कुर्सी, वाहन)। प्रभाव: मोटापा, पीठ-दर्द, हृदय रोग का ख़तरा, नींद की समस्या।', '1 अंक अर्थ के लिए, 2 अंक दो प्रासंगिक प्रभावों के लिए।', 3),
    ('C3', 'इन शब्दों को दो समूहों — ‘स्वस्थ आदतें’ और ‘अस्वस्थ आदतें’ — में बाँटिए: देर रात तक जागना, नियमित व्यायाम, पौष्टिक नाश्ता, फ़िज़ूलख़र्ची, संतुलित दिनचर्या, घंटों स्क्रीन देखना।', 'स्वस्थ: नियमित व्यायाम, पौष्टिक नाश्ता, संतुलित दिनचर्या। अस्वस्थ: देर रात तक जागना, फ़िज़ूलख़र्ची, घंटों स्क्रीन देखना।', 'प्रत्येक दो सही वर्गीकरण के लिए 1 अंक (अधिकतम 3)।'),
]))
SPEC['ch01-st2'] = ('grammar', dict(focus='लेखन में वर्तमान, भूत और भविष्यत् कालों का सटीक और विविध प्रयोग कीजिए।', gens=[
    g_choose_form(TENSE_BANK, TENSE_LABELS),
    g_free([('‘{topic}’ विषय पर 100–120 शब्दों का अनुच्छेद लिखिए: पहले बताइए कि पहले क्या होता था (भूतकाल), फिर आज क्या हो रहा है (वर्तमान काल) और अंत में भविष्य में आप क्या करेंगे (भविष्यत् काल)।',
             'अपेक्षित: तीनों कालों का स्पष्ट और शुद्ध प्रयोग; भूतकाल में ‘ने’ और अन्विति सही; विचार विषय से जुड़े और क्रमबद्ध।'),
            ('‘{topic}’ — इस विषय पर अपने पिछले सप्ताहांत का वर्णन 80–100 शब्दों में कीजिए। कम से कम दो वाक्य पूर्ण भूतकाल (जैसे ‘…कर चुका था’) में हों।',
             'अपेक्षित: सामान्य भूतकाल और पूर्ण भूतकाल का सही प्रयोग; घटनाओं का क्रम स्पष्ट; सकर्मक क्रियाओं के साथ ‘ने’ का सही प्रयोग।')]),
], items=[
    ('C1', '‘मीरा योग कर चुकी थी’ — इस वाक्य में ‘चुकी थी’ किस बात का संकेत है?', 'कार्य भूतकाल में किसी समय से पहले पूरा हो गया था', ['कार्य अभी चल रहा है', 'कार्य भविष्य में होगा', 'कार्य रोज़ होता है'], '‘चुका/चुकी/चुके थे’ पूर्ण भूतकाल का संकेत है।'),
    ('C1', 'किस वाक्य में ‘ने’ का प्रयोग सही है?', 'बच्चों ने फ़ुटबॉल खेला।', ['अनुज ने विद्यालय गया।', 'माँ ने बाज़ार से आईं।', 'लोग ने मेट्रो से पहुँचे।'], 'सकर्मक क्रिया (खेलना) के सामान्य भूतकाल में कर्ता के साथ ‘ने’ आता है; जाना, आना, पहुँचना अकर्मक हैं।'),
    ('C1', 'अपूर्ण वर्तमान काल की पहचान क्या है?', 'क्रिया के साथ ‘रहा/रही/रहे है/हैं’', ['क्रिया के साथ ‘गा/गी/गे’', 'क्रिया के साथ ‘चुका था’', 'कर्ता के साथ ‘ने’'], 'अपूर्ण (सातत्य) वर्तमान काल: कार्य इस समय चल रहा है — ‘खा रहा है’।'),
    ('C2', '“पिताजी ने रोटियाँ बनाईं” में क्रिया ‘बनाईं’ स्त्रीलिंग बहुवचन में क्यों है, जबकि कर्ता ‘पिताजी’ पुल्लिंग है? समझाइए।', '‘ने’ वाले वाक्यों (सकर्मक, सामान्य भूतकाल) में क्रिया कर्ता से नहीं, कर्म से अन्विति करती है; कर्म ‘रोटियाँ’ स्त्रीलिंग बहुवचन है, इसलिए ‘बनाईं’।', '1 अंक नियम (‘ने’ के बाद कर्म से अन्विति), 1 अंक इस वाक्य पर सही प्रयोग।'),
    ('C2', '“अनुज विद्यालय गया” और “अनुज ने खाना खाया” — एक में ‘ने’ है, दूसरे में नहीं। कारण स्पष्ट कीजिए।', '‘जाना’ अकर्मक क्रिया है (कर्म नहीं), इसलिए ‘ने’ नहीं आता और क्रिया कर्ता से अन्विति करती है; ‘खाना’ सकर्मक है, इसलिए सामान्य भूतकाल में ‘ने’ आता है।', '1 अंक अकर्मक/सकर्मक की पहचान, 1 अंक ‘ने’ के नियम की व्याख्या।'),
    ('C2', 'सामान्य भूतकाल (“मैंने खाना खाया”) और पूर्ण भूतकाल (“मैं खाना खा चुका था”) के प्रयोग में क्या अंतर है? एक-एक उदाहरण से समझाइए।', 'सामान्य भूतकाल बताता है कि कार्य बीते समय में हुआ; पूर्ण भूतकाल बताता है कि कार्य किसी दूसरी बीती घटना से पहले पूरा हो चुका था — “जब मेहमान आए, तब तक हम खाना खा चुके थे।”', '1 अंक प्रत्येक काल के अर्थ के लिए, 1 अंक उपयुक्त उदाहरण के लिए।', 3),
    ('C3', 'वाक्य शुद्ध कीजिए: “माँ ने बाज़ार गई और सब्ज़ियाँ ख़रीदी।”', 'माँ बाज़ार गईं और (उन्होंने) सब्ज़ियाँ ख़रीदीं।', '1 अंक ‘ने’ हटाकर ‘गईं’ (अकर्मक, आदरसूचक बहुवचन), 1 अंक ‘ख़रीदीं’ (कर्म ‘सब्ज़ियाँ’ स्त्रीलिंग बहुवचन से अन्विति)।', 2),
    ('C3', 'वाक्य शुद्ध कीजिए: “कल हम पिकनिक पर जाएँगे थे और बहुत मज़ा किया।”', 'कल हम पिकनिक पर गए थे और (हमने) बहुत मज़ा किया।', '1 अंक भविष्यत् और भूत के मिश्रण को हटाकर ‘गए थे’; 1 अंक ‘हमने… किया’ (सकर्मक के साथ ‘ने’)।', 2),
]))
SPEC['ch01-st3'] = ('reading', dict(focus='लेख के मुख्य विचार को अपने उदाहरणों से विकसित कीजिए।', items=[
    ('C1', 'किसी लेख का ‘मुख्य विचार’ प्रायः कहाँ मिलता है?', 'शीर्षक, भूमिका और निष्कर्ष में', ['केवल चित्र के कैप्शन में', 'लेखक के नाम में', 'केवल अंतिम वाक्य के बीच के शब्दों में'], 'मुख्य विचार शीर्षक, भूमिका और निष्कर्ष में स्पष्ट होता है; बीच के अनुच्छेद उसे विकसित करते हैं।'),
    ('C2', 'किसी लेख में ‘मुख्य विचार’ और ‘सहायक विवरण’ में क्या अंतर है? ‘धीमी ज़िंदगी’ जैसे विषय का उदाहरण देकर समझाइए।', 'मुख्य विचार लेख का केंद्रीय संदेश है (युवा धीमी, संतुलित ज़िंदगी चुन रहे हैं); सहायक विवरण उसे पुष्ट करने वाले तथ्य, उदाहरण और उद्धरण हैं (तन्वी का डिजिटल उपवास, समाजशास्त्रियों की राय)।', '1 अंक प्रत्येक अवधारणा के लिए, 1 अंक उदाहरण के लिए।', 3),
]))
SPEC['ch01-st4'] = ('writing', dict(tt='blog', focus='ब्लॉग की आत्मीय शैली बनाए रखिए।', tasks=[
    ('आप अपने निजी ब्लॉग ‘मेरी ज़िंदगी, मेरे नियम’ पर अपनी जीवन-शैली के बारे में पहली प्रविष्टि लिख रहे हैं।', ['आपकी दिनचर्या की एक झलक', 'आपकी सबसे अच्छी और सबसे बुरी आदत', 'पाठकों से उनकी आदतों के बारे में प्रश्न']),
    ('आपने एक सप्ताह तक बिना सोशल मीडिया के रहने का प्रयोग किया। अब आप अपने ब्लॉग पर इसका अनुभव साझा करना चाहते हैं।', ['प्रयोग क्यों शुरू किया', 'सबसे कठिन और सबसे सुखद क्षण', 'आपकी सीख और पाठकों के लिए चुनौती']),
    ('आप अपने परिवार के साथ शहर से एक छोटे पहाड़ी कस्बे में रहने आ गए हैं। अपने ब्लॉग पर दोनों जगहों की जीवन-शैली की तुलना कीजिए।', ['दिनचर्या और खान-पान में अंतर', 'क्या अच्छा लगा और किस चीज़ की कमी खलती है', 'आपका निष्कर्ष']),
    ('आपके ब्लॉग के पाठकों ने पूछा है कि आप पढ़ाई, खेल और शौक़ के बीच संतुलन कैसे बनाते हैं।', ['आपकी समय-सारणी के मुख्य नियम', 'एक असफल प्रयोग और उससे मिली सीख', 'पाठकों के लिए तीन व्यावहारिक सुझाव']),
    ('आपने हाल ही में शाकाहारी भोजन अपनाया है और अपने ब्लॉग पर इसके बारे में लिखना चाहते हैं।', ['निर्णय के कारण', 'परिवार और मित्रों की प्रतिक्रिया', 'शुरुआत करने वालों के लिए सुझाव और आसान व्यंजन']),
], items=[
    ('C1', 'ब्लॉग प्रविष्टि में प्रायः किस पुरुष (व्यक्ति) में लिखा जाता है?', 'प्रथम पुरुष (मैं/हम)', ['केवल तृतीय पुरुष (वह/वे)', 'केवल मध्यम पुरुष (आप)', 'कर्मवाच्य में'], 'ब्लॉग निजी अनुभवों पर आधारित होता है, इसलिए प्रथम पुरुष स्वाभाविक है।'),
    ('C2', 'ब्लॉग और डायरी प्रविष्टि दोनों निजी अनुभवों पर आधारित हैं, फिर भी इनमें मुख्य अंतर क्या है?', 'डायरी केवल लेखक के लिए होती है, इसलिए निजी और गोपनीय होती है; ब्लॉग ऑनलाइन पाठकों के लिए लिखा जाता है, इसलिए उसमें पाठकों से संवाद, आकर्षक शीर्षक और टिप्पणी का आमंत्रण होता है।', '1 अंक पाठक के अंतर के लिए, 1 अंक भाषा/प्रारूप पर उसके प्रभाव के लिए।'),
]))


# ---------------------------------------------------------------- ch02 स्वास्थ्य और कल्याण
TH[2] = dict(
    name='स्वास्थ्य और कल्याण',
    vocab=[
        ('तनाव', 'मन पर पड़ने वाला दबाव और बेचैनी', 'दबाव', 'परीक्षा से एक रात पहले ____ के कारण मुझे नींद नहीं आई।'),
        ('रोग-प्रतिरोधक क्षमता', 'शरीर की बीमारियों से लड़ने की शक्ति', 'प्रतिरक्षा', 'आँवला और हल्दी ____ बढ़ाने में सहायक माने जाते हैं।'),
        ('व्यायाम', 'शरीर को स्वस्थ रखने के लिए किया जाने वाला शारीरिक श्रम', 'कसरत', 'डॉक्टर ने दादाजी को रोज़ हल्का ____ करने की सलाह दी।'),
        ('मानसिक', 'मन से संबंधित', 'मनोवैज्ञानिक', 'शारीरिक स्वास्थ्य के साथ-साथ ____ स्वास्थ्य पर भी ध्यान देना चाहिए।'),
        ('चिंता', 'किसी बात को लेकर मन में बना रहने वाला डर या फ़िक्र', 'फ़िक्र', 'माँ को मेरी सेहत की बहुत ____ रहती है।'),
        ('उपचार', 'बीमारी ठीक करने का तरीका', 'इलाज', 'समय पर ____ मिलने से मरीज़ जल्दी ठीक हो गया।'),
        ('ध्यान', 'मन को एकाग्र और शांत करने का अभ्यास', 'मेडिटेशन', 'सुबह दस मिनट ____ करने से मेरा मन पूरे दिन शांत रहता है।'),
        ('लक्षण', 'किसी बीमारी के संकेत', 'चिह्न', 'बुख़ार, खाँसी और थकान फ़्लू के आम ____ हैं।'),
        ('संक्रमण', 'कीटाणुओं का एक व्यक्ति से दूसरे तक फैलना', 'छूत', 'बार-बार हाथ धोने से ____ का ख़तरा कम होता है।'),
        ('आहार', 'रोज़ खाया जाने वाला भोजन', 'भोजन', 'संतुलित ____ में अनाज, दालें, फल और सब्ज़ियाँ सभी शामिल होते हैं।'),
        ('अनिद्रा', 'नींद न आने की समस्या', 'निद्राहीनता', 'देर रात तक फ़ोन चलाने से कई किशोरों को ____ की शिकायत हो जाती है।'),
        ('परामर्शदाता', 'समस्याओं पर सलाह देने वाला प्रशिक्षित व्यक्ति', 'काउंसलर', 'विद्यालय के ____ ने मुझे परीक्षा का डर दूर करने के उपाय बताए।'),
        ('लत', 'किसी हानिकारक चीज़ की ऐसी आदत जो छूटे नहीं', 'व्यसन', 'मोबाइल गेम की ____ से उसकी पढ़ाई और नींद दोनों प्रभावित हुईं।'),
        ('कल्याण', 'शरीर और मन की समग्र भलाई', 'हित', 'विद्यार्थियों के ____ के लिए विद्यालय ने ‘खुशहाली सप्ताह’ मनाया।'),
    ],
    topics=['परीक्षा का तनाव और उससे निपटने के उपाय', 'योग और ध्यान का महत्व', 'किशोरों का मानसिक स्वास्थ्य', 'स्वस्थ आहार, स्वस्थ जीवन',
            'खेल-कूद और शारीरिक स्वास्थ्य', 'मोबाइल की लत और नींद', 'बदलते मौसम में स्वास्थ्य की देखभाल'],
    texts=[
        dict(kind='लेख', title='योग: मुद्रा से अधिक मन की बात',
             body='संयुक्त राष्ट्र ने 2014 में 21 जून को ‘अंतरराष्ट्रीय योग दिवस’ घोषित किया। आज टोरंटो से टोक्यो तक लोग योग करते हैं, पर विशेषज्ञ याद दिलाते हैं कि योग केवल कठिन आसनों का प्रदर्शन नहीं है। प्राणायाम और ध्यान इसके उतने ही महत्वपूर्ण अंग हैं। दिल्ली की योग-शिक्षिका सुधा वर्मा कहती हैं, “जो विद्यार्थी रोज़ दस मिनट श्वास पर ध्यान देते हैं, वे परीक्षा के तनाव को बेहतर ढंग से सँभाल पाते हैं।”',
             qs=[('C1', 'अंतरराष्ट्रीय योग दिवस किस तारीख़ को मनाया जाता है?', '21 जून', ['14 सितंबर', '2 अक्टूबर', '21 मार्च']),
                 ('C1', 'पाठ के अनुसार योग के कौन-से दो अंग आसनों जितने ही महत्वपूर्ण हैं?', 'प्राणायाम और ध्यान'),
                 ('C2', '“योग: मुद्रा से अधिक मन की बात” — इस शीर्षक का आशय स्पष्ट कीजिए।', 'योग का उद्देश्य केवल शरीर की मुद्राएँ (आसन) दिखाना नहीं, बल्कि श्वास और ध्यान के माध्यम से मन को शांत और संतुलित करना भी है।'),
                 ('tf', 'विशेषज्ञों के अनुसार योग का अर्थ केवल कठिन आसन करना है।', 'गलत', '“योग केवल कठिन आसनों का प्रदर्शन नहीं है।”'),
                 ('tf', 'सुधा वर्मा के अनुसार श्वास पर ध्यान देने वाले विद्यार्थी तनाव को बेहतर सँभालते हैं।', 'सही', '“वे परीक्षा के तनाव को बेहतर ढंग से सँभाल पाते हैं।”'),
                 ('C3', '“टोरंटो से टोक्यो तक” — लेखक ने यह अभिव्यक्ति किस उद्देश्य से प्रयोग की है?', 'यह दिखाने के लिए कि योग अब पूरी दुनिया में लोकप्रिय है', ['यह बताने के लिए कि योग केवल कनाडा में होता है', 'यात्रा के ख़र्च की तुलना करने के लिए', 'यह बताने के लिए कि योग जापान से आया']),
                 ('C3', 'सुधा वर्मा का कथन लेख के तर्क को कैसे मज़बूत करता है?', 'एक विशेषज्ञ (योग-शिक्षिका) का अनुभव-आधारित कथन यह प्रमाण देता है कि ध्यान और श्वास का अभ्यास मानसिक लाभ देता है, जिससे लेख का दावा विश्वसनीय बनता है।'),
                 ('C4', 'क्या विद्यालयों में योग और ध्यान को अनिवार्य विषय बनाया जाना चाहिए? लेख के आधार पर और अपने विचारों से उत्तर दीजिए।', 'पक्ष: तनाव-प्रबंधन, एकाग्रता, स्वास्थ्य (लेख का प्रमाण)। विपक्ष: अनिवार्यता से रुचि घट सकती है, सांस्कृतिक/धार्मिक संवेदनशीलता, अन्य खेलों का विकल्प। संतुलित निष्कर्ष: वैकल्पिक या विविध कल्याण-कार्यक्रम।')]),
        dict(kind='अनौपचारिक पत्र', title='प्रिय अदिति के नाम',
             body='पुणे, 3 मार्च\nप्रिय अदिति,\nतुम्हारा पत्र पढ़कर लगा कि तुम बोर्ड परीक्षा को लेकर बहुत घबराई हुई हो। पिछले साल मेरा भी यही हाल था। मैंने तीन काम किए: पढ़ाई को छोटे-छोटे हिस्सों में बाँटा, हर पचास मिनट बाद दस मिनट का विराम लिया और रात को फ़ोन दूसरे कमरे में रखा। सबसे बड़ी बात — मैंने माँ से खुलकर बात की। मन हल्का हो गया। तुम भी अकेले मत घुटना।\nतुम्हारी दीदी,\nमानसी',
             qs=[('C1', 'मानसी ने पढ़ाई के बीच कितनी देर का विराम लिया?', 'हर पचास मिनट बाद दस मिनट', ['हर घंटे बाद आधा घंटा', 'हर बीस मिनट बाद पाँच मिनट', 'दिन में केवल एक बार']),
                 ('C1', 'मानसी रात को फ़ोन कहाँ रखती थी?', 'दूसरे कमरे में'),
                 ('C2', '“तुम भी अकेले मत घुटना” — इस वाक्य का आशय स्पष्ट कीजिए।', 'अपनी चिंता और परेशानी मन में दबाकर अकेले दुखी मत होना; किसी अपने से बात करके मन हल्का करना।'),
                 ('tf', 'मानसी को पिछले साल परीक्षा का कोई तनाव नहीं था।', 'गलत', '“पिछले साल मेरा भी यही हाल था।”'),
                 ('tf', 'माँ से बात करने के बाद मानसी को राहत मिली।', 'सही', '“मन हल्का हो गया।”'),
                 ('C3', 'पत्र की कौन-सी विशेषताएँ बताती हैं कि यह अनौपचारिक पत्र है? दो प्रमाण दीजिए।', '‘प्रिय अदिति’ जैसा आत्मीय संबोधन; ‘तुम’ का प्रयोग; ‘तुम्हारी दीदी’ जैसा आत्मीय समापन; निजी अनुभव साझा करना।'),
                 ('C3', 'मानसी के अनुसार तनाव कम करने का सबसे महत्वपूर्ण उपाय कौन-सा था?', 'माँ से खुलकर बात करना', ['फ़ोन दूसरे कमरे में रखना', 'पढ़ाई छोड़ देना', 'देर रात तक पढ़ना']),
                 ('C4', 'मानसी की सलाहों में से कौन-सी आपको सबसे उपयोगी लगती है और क्यों? क्या आप कोई और उपाय जोड़ना चाहेंगे?', 'किसी एक सलाह का चुनाव और कारण (जैसे बातचीत — भावनात्मक सहारा; विराम — एकाग्रता); अतिरिक्त उपाय: व्यायाम, पर्याप्त नींद, परामर्शदाता से बात। तर्क और उदाहरण आवश्यक।')]),
        dict(kind='जागरूकता पत्रक', title='लू से बचाव: क्या करें, क्या न करें',
             body='ज़िला स्वास्थ्य विभाग, जोधपुर की ओर से जनहित में जारी।\nक्या करें: दिन भर में बार-बार पानी पिएँ, भले ही प्यास न लगी हो। हल्के रंग के सूती कपड़े पहनें। बाहर निकलें तो सिर को गमछे या टोपी से ढकें। छाछ, नींबू-पानी और ओआरएस का घोल लें।\nक्या न करें: दोपहर बारह से तीन बजे के बीच धूप में न निकलें। ख़ाली पेट बाहर न जाएँ।\nचक्कर या तेज़ बुख़ार हो तो तुरंत 108 पर फ़ोन करें।',
             qs=[('C1', 'किस समय धूप में निकलने से मना किया गया है?', 'दोपहर बारह से तीन बजे के बीच', ['सुबह छह से नौ बजे के बीच', 'शाम पाँच बजे के बाद', 'रात दस बजे के बाद']),
                 ('C1', 'आपात स्थिति में किस नंबर पर फ़ोन करने को कहा गया है?', '108'),
                 ('C2', 'पत्रक में ‘क्या करें’ और ‘क्या न करें’ जैसे खंड क्यों रखे गए हैं?', 'जानकारी को स्पष्ट, छोटे और याद रखने योग्य हिस्सों में बाँटने के लिए, ताकि आम जनता जल्दी पढ़कर तुरंत अमल कर सके।'),
                 ('tf', 'पत्रक के अनुसार केवल प्यास लगने पर ही पानी पीना चाहिए।', 'गलत', '“बार-बार पानी पिएँ, भले ही प्यास न लगी हो।”'),
                 ('tf', 'यह पत्रक एक सरकारी विभाग ने जारी किया है।', 'सही', '“ज़िला स्वास्थ्य विभाग, जोधपुर की ओर से जनहित में जारी।”'),
                 ('C3', 'पत्रक में क्रियाओं के किस रूप (जैसे ‘पिएँ’, ‘पहनें’, ‘न निकलें’) का प्रयोग हुआ है और क्यों?', 'विधिलिंग/आदरसूचक सुझाव वाले रूपों का, क्योंकि पत्रक आम जनता को विनम्र पर स्पष्ट निर्देश देता है।'),
                 ('C3', 'यह पत्रक मुख्य रूप से किन लोगों के लिए है?', 'गर्मी में बाहर निकलने वाले आम नागरिकों के लिए', ['केवल डॉक्टरों के लिए', 'केवल विदेशी पर्यटकों के लिए', 'केवल किसानों के लिए']),
                 ('C4', 'इस पत्रक को किशोरों के लिए और अधिक प्रभावी बनाने के लिए आप कौन-से दो बदलाव सुझाएँगे? कारण सहित लिखिए।', 'उदाहरण: खेल-अभ्यास और विद्यालय आने-जाने के समय की विशेष सलाह; चित्र/इन्फ़ोग्राफ़िक और सोशल मीडिया संस्करण; पानी की बोतल साथ रखने जैसे व्यावहारिक सुझाव। प्रत्येक बदलाव का पाठक पर प्रभाव समझाया जाए।')]),
    ],
    audio=[
        dict(kind='रेडियो साक्षात्कार', title='‘सेहत की बात’ — डॉ. रश्मि त्रिपाठी से बातचीत',
             body='प्रस्तोता: नमस्कार श्रोताओ! आज हमारे साथ हैं मनोचिकित्सक डॉ. रश्मि त्रिपाठी। डॉक्टर साहिबा, किशोरों में तनाव क्यों बढ़ रहा है?\nडॉ. त्रिपाठी: देखिए, पढ़ाई का दबाव तो हमेशा था, पर अब सोशल मीडिया पर लगातार दूसरों से तुलना भी होती है। नींद कम हो गई है — कई बच्चे रात एक बजे तक जागते हैं।\nप्रस्तोता: माता-पिता क्या करें?\nडॉ. त्रिपाठी: डाँटने के बजाय सुनें। रोज़ पंद्रह मिनट बिना फ़ोन के बच्चे से बात करें।',
             qs=[('C1', 'डॉ. रश्मि त्रिपाठी किस क्षेत्र की विशेषज्ञ हैं?', 'मनोचिकित्सा', ['हृदय रोग', 'दंत चिकित्सा', 'आहार-विज्ञान']),
                 ('C1', 'डॉक्टर के अनुसार कई बच्चे रात को कब तक जागते हैं?', 'रात एक बजे तक'),
                 ('C1', 'डॉक्टर माता-पिता को रोज़ कितनी देर बच्चे से बात करने की सलाह देती हैं?', 'पंद्रह मिनट', ['पाँच मिनट', 'एक घंटा', 'आधा घंटा']),
                 ('C2', 'डॉक्टर के अनुसार आज के किशोरों के तनाव का कौन-सा कारण पहले नहीं था? समझाइए।', 'सोशल मीडिया पर लगातार दूसरों से तुलना — पढ़ाई का दबाव पहले भी था, पर यह नया कारण है जो आत्म-सम्मान और नींद दोनों पर असर डालता है।'),
                 ('tf', 'डॉक्टर के अनुसार किशोरों की नींद पहले से बढ़ गई है।', 'गलत', '“नींद कम हो गई है।”'),
                 ('C3', '“डाँटने के बजाय सुनें” — इस सलाह से डॉक्टर का दृष्टिकोण क्या झलकता है?', 'वे संवाद और सहानुभूति को अनुशासन से अधिक प्रभावी मानती हैं', ['वे सख़्ती को सबसे अच्छा उपाय मानती हैं', 'वे मानती हैं कि बच्चों से बात करना व्यर्थ है', 'वे फ़ोन पर अधिक समय बिताने की सलाह देती हैं']),
                 ('C3', 'साक्षात्कार की कौन-सी विशेषताएँ बताती हैं कि यह रेडियो के लिए है? दो संकेत लिखिए।', '‘नमस्कार श्रोताओ!’ जैसा संबोधन; प्रस्तोता का अतिथि-परिचय; बोलचाल के शब्द जैसे ‘देखिए’; प्रश्न-उत्तर का संवादात्मक क्रम।'),
                 ('C4', 'डॉक्टर के सुझाव के अलावा विद्यालय किशोरों के मानसिक स्वास्थ्य के लिए क्या कर सकते हैं? साक्षात्कार के बिंदुओं से जोड़ते हुए उत्तर दीजिए।', 'परामर्शदाता की उपलब्धता, सोशल मीडिया-साक्षरता की कक्षाएँ, गृहकार्य का संतुलन, नींद पर जागरूकता; साक्षात्कार के कारणों (तुलना, नींद की कमी) से स्पष्ट संबंध।')]),
        dict(kind='जन-सूचना प्रसारण', title='आकाशवाणी: डेंगू से बचाव का संदेश',
             body='यह संदेश स्वास्थ्य मंत्रालय की ओर से है। बरसात के मौसम में डेंगू के मामले बढ़ जाते हैं। डेंगू का मच्छर साफ़, रुके हुए पानी में पनपता है और प्रायः दिन में काटता है। इसलिए कूलर, गमलों और पुराने टायरों में पानी जमा न होने दें। पूरी बाँह के कपड़े पहनें और मच्छरदानी का प्रयोग करें। तेज़ बुख़ार, सिरदर्द या जोड़ों में दर्द हो तो अपने आप दवा न लें — नज़दीकी स्वास्थ्य केंद्र पर मुफ़्त जाँच कराएँ।',
             qs=[('C1', 'डेंगू का मच्छर किस तरह के पानी में पनपता है?', 'साफ़, रुके हुए पानी में', ['बहते हुए नदी के पानी में', 'खारे समुद्री पानी में', 'गर्म पानी में']),
                 ('C1', 'डेंगू का मच्छर प्रायः कब काटता है?', 'दिन में'),
                 ('C1', 'संदेश में डेंगू के कौन-से तीन लक्षण बताए गए हैं?', 'तेज़ बुख़ार, सिरदर्द और जोड़ों में दर्द'),
                 ('C2', 'संदेश में “अपने आप दवा न लें” की सलाह क्यों दी गई है?', 'क्योंकि बिना जाँच के ली गई दवा से रोग की पहचान में देर हो सकती है और स्थिति बिगड़ सकती है; सही उपचार के लिए स्वास्थ्य केंद्र पर जाँच ज़रूरी है।'),
                 ('tf', 'स्वास्थ्य केंद्र पर डेंगू की जाँच के लिए शुल्क देना पड़ता है।', 'गलत', '“नज़दीकी स्वास्थ्य केंद्र पर मुफ़्त जाँच कराएँ।”'),
                 ('C3', 'संदेश में कूलर, गमलों और टायरों का उल्लेख क्यों किया गया है?', 'क्योंकि इन्हीं में रुका हुआ साफ़ पानी जमा होता है, जहाँ मच्छर पनपता है', ['क्योंकि ये चीज़ें महँगी होती हैं', 'क्योंकि इनसे बुख़ार होता है', 'क्योंकि ये दिन में गर्म हो जाती हैं']),
                 ('C3', 'इस प्रसारण का मुख्य उद्देश्य क्या है? पाठ से दो प्रमाण दीजिए।', 'लोगों को डेंगू से बचाव के लिए जागरूक करना और व्यावहारिक निर्देश देना — ‘पानी जमा न होने दें’, ‘मच्छरदानी का प्रयोग करें’, ‘मुफ़्त जाँच कराएँ’।'),
                 ('C4', 'क्या रेडियो जैसा माध्यम आज भी ऐसे स्वास्थ्य-संदेशों के लिए प्रभावी है? अपने विचार कारण सहित दीजिए।', 'पक्ष: गाँवों और कम साक्षर लोगों तक पहुँच, सस्ता, भरोसेमंद। विपक्ष: युवा सोशल मीडिया पर अधिक; दृश्य सामग्री का अभाव। निष्कर्ष: बहु-माध्यम अभियान।')]),
        dict(kind='पॉडकास्ट', title='‘नींद क्यों ज़रूरी है?’ — पॉडकास्ट ‘तन-मन’ का अंश',
             body='नमस्ते, मैं हूँ आरव, और आप सुन रहे हैं ‘तन-मन’। आज बात नींद की। वैज्ञानिकों के अनुसार किशोरों को हर रात आठ से दस घंटे की नींद चाहिए, पर एक सर्वेक्षण में पता चला कि बड़े शहरों के आधे से ज़्यादा किशोर सात घंटे से कम सोते हैं। नींद में ही हमारा दिमाग़ दिन भर की सीखी बातों को सहेजता है। इसलिए परीक्षा से पहले रात भर जागकर पढ़ना उल्टा नुक़सान करता है। मेरा सुझाव? सोने से एक घंटा पहले स्क्रीन बंद!',
             qs=[('C1', 'वैज्ञानिकों के अनुसार किशोरों को हर रात कितनी नींद चाहिए?', 'आठ से दस घंटे', ['छह से सात घंटे', 'पाँच घंटे', 'बारह घंटे से अधिक']),
                 ('C1', 'पॉडकास्ट का नाम क्या है?', '‘तन-मन’'),
                 ('C2', 'आरव के अनुसार परीक्षा से पहले रात भर जागकर पढ़ना नुक़सानदेह क्यों है?', 'क्योंकि नींद के दौरान दिमाग़ सीखी हुई बातों को सहेजता है; नींद न लेने से पढ़ा हुआ याद नहीं रहता और थकान बढ़ती है।'),
                 ('tf', 'सर्वेक्षण के अनुसार बड़े शहरों के अधिकतर किशोर पर्याप्त नींद लेते हैं।', 'गलत', '“आधे से ज़्यादा किशोर सात घंटे से कम सोते हैं।”'),
                 ('C3', 'आरव श्रोताओं को क्या करने का सुझाव देता है?', 'सोने से एक घंटा पहले स्क्रीन बंद करना', ['रात भर पढ़ाई करना', 'दिन में ज़्यादा सोना', 'सोने से पहले वीडियो देखना']),
                 ('C3', 'पॉडकास्ट की शैली किस प्रकार की है? दो भाषिक प्रमाण देकर समझाइए।', 'अनौपचारिक और संवादात्मक — ‘नमस्ते, मैं हूँ आरव’, ‘मेरा सुझाव?’ जैसा प्रश्न, ‘स्क्रीन बंद!’ जैसा छोटा, सीधा वाक्य।'),
                 ('C4', 'क्या आप आरव के इस दावे से सहमत हैं कि “रात भर जागकर पढ़ना उल्टा नुक़सान करता है”? अपने अनुभव और पॉडकास्ट के तर्क के आधार पर उत्तर दीजिए।', 'मत स्पष्ट हो; पॉडकास्ट का वैज्ञानिक तर्क (स्मृति का सहेजा जाना) और आँकड़े; निजी अनुभव (थकान, एकाग्रता); संभावित अपवाद और संतुलित निष्कर्ष।')]),
    ],
    tasks=[
        ('आपके विद्यालय में ‘मानसिक स्वास्थ्य सप्ताह’ मनाया जा रहा है। आयोजन समिति ने आपसे विद्यार्थियों के लिए एक पत्रक तैयार करने को कहा है।', 'brochure',
         ['तनाव के सामान्य लक्षण', 'तनाव कम करने के व्यावहारिक उपाय', 'सहायता कहाँ से मिल सकती है']),
        ('आपके मोहल्ले के पार्क में खुले जिम की मशीनें टूटी पड़ी हैं और लोग व्यायाम नहीं कर पा रहे। आप नगर निगम के स्वास्थ्य अधिकारी को लिखना चाहते हैं।', 'fletter',
         ['समस्या का विवरण', 'इससे लोगों के स्वास्थ्य पर पड़ने वाला प्रभाव', 'आपके सुझाव और अनुरोध']),
        ('विद्यालय पत्रिका के ‘सेहत विशेषांक’ के लिए आपको एक खिलाड़ी का साक्षात्कार लेना है जिसने चोट के बाद वापसी की है।', 'interview',
         ['चोट और उपचार का अनुभव', 'मानसिक मज़बूती कैसे बनाए रखी', 'युवा खिलाड़ियों के लिए संदेश']),
        ('आपके एक मित्र ने बताया है कि वह पूरी रात मोबाइल पर गेम खेलता है और दिन में थका रहता है।', 'pletter',
         ['उसकी स्थिति पर आपकी चिंता', 'इसके दुष्प्रभाव', 'आदत छोड़ने के व्यावहारिक सुझाव']),
        ('विश्व स्वास्थ्य दिवस (7 अप्रैल) पर आपको विद्यालय सभा में ‘स्वस्थ तन में स्वस्थ मन’ विषय पर बोलना है।', 'speech',
         ['शारीरिक और मानसिक स्वास्थ्य का संबंध', 'विद्यार्थियों की आम अस्वस्थ आदतें', 'तीन संकल्प जो सभी ले सकते हैं']),
        ('आपने पहली बार दस किलोमीटर की दौड़ पूरी की है।', 'diary',
         ['तैयारी के महीने और कठिनाइयाँ', 'दौड़ के दिन की भावनाएँ', 'इस अनुभव से मिली सीख']),
    ],
    discuss=[
        ('क्या आज के किशोरों के लिए मानसिक स्वास्थ्य, शारीरिक स्वास्थ्य से अधिक बड़ी चुनौती है?', ['पढ़ाई और सोशल मीडिया का दबाव', 'शारीरिक निष्क्रियता और मोटापा भी गंभीर', 'दोनों एक-दूसरे से जुड़े हैं']),
        ('क्या स्वास्थ्य से जुड़े ऐप और स्मार्टवॉच हमें सचमुच स्वस्थ बनाते हैं?', ['प्रेरणा और आँकड़ों से जागरूकता', 'अत्यधिक निर्भरता और चिंता', 'डेटा की निजता का प्रश्न']),
        ('क्या विद्यालयों में जंक फ़ूड पर पूरी तरह प्रतिबंध लगना चाहिए?', ['बच्चों के स्वास्थ्य की रक्षा', 'व्यक्तिगत चुनाव की स्वतंत्रता', 'प्रतिबंध से बेहतर शिक्षा और विकल्प']),
        ('क्या पारंपरिक उपचार (आयुर्वेद, घरेलू नुस्ख़े) आधुनिक चिकित्सा का स्थान ले सकते हैं?', ['कुछ घरेलू उपाय उपयोगी और सस्ते', 'गंभीर रोगों में वैज्ञानिक जाँच आवश्यक', 'दोनों का पूरक प्रयोग']),
        ('क्या खेल-कूद को परीक्षा के अंकों जितना महत्व मिलना चाहिए?', ['टीम-भावना, अनुशासन और स्वास्थ्य', 'करियर और दाख़िले में अंकों का महत्व', 'संतुलित मूल्यांकन-प्रणाली']),
    ],
    pics=[('एक अस्पताल के प्रतीक्षा-कक्ष में लंबी कतार है; दीवार पर पोस्टर लगा है: “टीका लगवाएँ, सुरक्षित रहें।” एक नर्स बुज़ुर्ग महिला की मदद कर रही है।',
           ['सार्वजनिक स्वास्थ्य सेवाओं पर भीड़', 'टीकाकरण के प्रति जागरूकता', 'स्वास्थ्यकर्मियों की भूमिका']),
          ('एक विद्यार्थी देर रात मेज़ पर किताबों के ढेर के बीच सिर पकड़े बैठा है; पास में कॉफ़ी के तीन कप और जलता हुआ मोबाइल है।',
           ['परीक्षा का तनाव', 'नींद की कमी और अस्वस्थ आदतें', 'मदद माँगने और समय-प्रबंधन का महत्व'])],
)

IMP_LABELS = ['आज्ञार्थ (‘तुम’ के लिए)', 'आदरसूचक आज्ञार्थ (‘आप’ के लिए)', 'विधिलिंग (विनम्र सुझाव)', '‘चाहिए’ वाला सलाह-वाक्य']
IMP_BANK = [
    ('रोज़ आठ गिलास पानी पियो।', 'रोज़ आठ गिलास पानी पीजिए।', 'रोज़ आठ गिलास पानी पिएँ।', 'आपको रोज़ आठ गिलास पानी पीना चाहिए।'),
    ('रात को समय पर सो जाओ।', 'रात को समय पर सो जाइए।', 'रात को समय पर सो जाएँ।', 'आपको रात को समय पर सो जाना चाहिए।'),
    ('रोज़ हरी सब्ज़ियाँ खाओ।', 'रोज़ हरी सब्ज़ियाँ खाइए।', 'रोज़ हरी सब्ज़ियाँ खाएँ।', 'आपको रोज़ हरी सब्ज़ियाँ खानी चाहिए।'),
    ('खाने से पहले हाथ धोओ।', 'खाने से पहले हाथ धोइए।', 'खाने से पहले हाथ धोएँ।', 'आपको खाने से पहले हाथ धोने चाहिए।'),
    ('घबराहट हो तो गहरी साँस लो।', 'घबराहट हो तो गहरी साँस लीजिए।', 'घबराहट हो तो गहरी साँस लें।', 'घबराहट होने पर आपको गहरी साँस लेनी चाहिए।'),
    ('रोज़ आधा घंटा टहलो।', 'रोज़ आधा घंटा टहलिए।', 'रोज़ आधा घंटा टहलें।', 'आपको रोज़ आधा घंटा टहलना चाहिए।'),
    ('धूप में निकलते समय टोपी पहनो।', 'धूप में निकलते समय टोपी पहनिए।', 'धूप में निकलते समय टोपी पहनें।', 'आपको धूप में निकलते समय टोपी पहननी चाहिए।'),
    ('मीठे पेयों से दूर रहो।', 'मीठे पेयों से दूर रहिए।', 'मीठे पेयों से दूर रहें।', 'आपको मीठे पेयों से दूर रहना चाहिए।'),
    ('डॉक्टर की सलाह के बिना दवा मत लो।', 'डॉक्टर की सलाह के बिना दवा मत लीजिए।', 'डॉक्टर की सलाह के बिना दवा न लें।', 'आपको डॉक्टर की सलाह के बिना दवा नहीं लेनी चाहिए।'),
    ('परेशानी हो तो किसी भरोसेमंद व्यक्ति से बात करो।', 'परेशानी हो तो किसी भरोसेमंद व्यक्ति से बात कीजिए।', 'परेशानी हो तो किसी भरोसेमंद व्यक्ति से बात करें।', 'परेशानी होने पर आपको किसी भरोसेमंद व्यक्ति से बात करनी चाहिए।'),
    ('सोने से पहले फ़ोन दूर रख दो।', 'सोने से पहले फ़ोन दूर रख दीजिए।', 'सोने से पहले फ़ोन दूर रख दें।', 'आपको सोने से पहले फ़ोन दूर रख देना चाहिए।'),
    ('हर सुबह दस मिनट ध्यान करो।', 'हर सुबह दस मिनट ध्यान कीजिए।', 'हर सुबह दस मिनट ध्यान करें।', 'आपको हर सुबह दस मिनट ध्यान करना चाहिए।'),
    ('लिफ़्ट के बजाय सीढ़ियों का प्रयोग करो।', 'लिफ़्ट के बजाय सीढ़ियों का प्रयोग कीजिए।', 'लिफ़्ट के बजाय सीढ़ियों का प्रयोग करें।', 'आपको लिफ़्ट के बजाय सीढ़ियों का प्रयोग करना चाहिए।'),
]

SPEC['ch02-st1'] = ('vocab', dict(focus='लेखन में स्वास्थ्य और कल्याण से जुड़ी सटीक शब्दावली (जैसे तनाव, रोग-प्रतिरोधक क्षमता, परामर्शदाता) का प्रयोग कीजिए।', items=[
    ('C1', '‘शारीरिक’ और ‘मानसिक’ के साथ कौन-सा शब्द जोड़कर ‘संपूर्ण भलाई’ का भाव बनता है?', 'कल्याण', ['लक्षण', 'संक्रमण', 'अनिद्रा'], 'शारीरिक और मानसिक कल्याण = तन और मन की समग्र भलाई।'),
    ('C1', '‘योग’ के संदर्भ में ‘प्राणायाम’ का अर्थ क्या है?', 'श्वास को नियंत्रित करने का अभ्यास', ['कठिन आसन करना', 'उपवास रखना', 'दौड़ लगाना'], 'प्राण (श्वास) + आयाम (नियंत्रण/विस्तार)।'),
    ('C1', '‘स्वास्थ्य’ संज्ञा का विशेषण रूप कौन-सा है?', 'स्वस्थ', ['स्वास्थ्यता', 'स्वस्थता', 'स्वास्थ्यी'], '‘स्वास्थ्य’ संज्ञा है; ‘स्वस्थ’ विशेषण (स्वस्थ बच्चा)।'),
    ('C2', '‘तनाव’ और ‘चिंता’ में क्या अंतर है? एक-एक उदाहरण दीजिए।', '‘तनाव’ किसी दबाव या माँग से उत्पन्न मानसिक-शारीरिक खिंचाव है (परीक्षा के कार्यक्रम से तनाव); ‘चिंता’ किसी संभावित बुरी बात के बारे में मन में बना रहने वाला डर या फ़िक्र है (परिणाम की चिंता)।', '1 अंक प्रत्येक अर्थ के लिए, 1 अंक उदाहरणों के लिए।', 3),
    ('C2', '‘उपचार’ और ‘रोकथाम’ में अंतर स्पष्ट कीजिए और बताइए कि स्वास्थ्य-अभियानों में ‘रोकथाम’ पर अधिक ज़ोर क्यों दिया जाता है।', '‘उपचार’ बीमारी होने के बाद उसका इलाज है; ‘रोकथाम’ बीमारी को होने से पहले ही रोकना है (टीका, स्वच्छता)। रोकथाम सस्ती, सुरक्षित और अधिक लोगों तक पहुँचने वाली है।', '2 अंक अंतर के लिए, 1 अंक कारण के लिए।', 3),
    ('C3', 'वाक्य में अंग्रेज़ी शब्द के स्थान पर उपयुक्त हिंदी शब्द लिखिए: “डॉक्टर ने कहा कि मेरी ‘इम्युनिटी’ कमज़ोर है।”', 'रोग-प्रतिरोधक क्षमता', '1 अंक: ‘रोग-प्रतिरोधक क्षमता’ या ‘प्रतिरक्षा’।', 1),
]))
SPEC['ch02-st2'] = ('listening', dict(focus='लेखन में स्वास्थ्य-विशेषज्ञों के विचारों को उद्धरण की तरह प्रस्तुत कीजिए।', items=[
    ('C1', 'श्रवण परीक्षा में प्रश्न पढ़ने का सबसे अच्छा समय कौन-सा है?', 'अंश सुनने से पहले दिए गए पढ़ने के समय में', ['अंश समाप्त होने के बाद ही', 'केवल दूसरी बार सुनते समय', 'प्रश्न पढ़ने की आवश्यकता नहीं होती'], 'पहले प्रश्न पढ़ने से पता चलता है कि किन जानकारियों पर ध्यान देना है।'),
    ('C1', 'जन-सूचना प्रसारण (जैसे आकाशवाणी का स्वास्थ्य संदेश) का मुख्य उद्देश्य क्या होता है?', 'आम जनता को जानकारी और निर्देश देना', ['किसी उत्पाद को बेचना', 'श्रोताओं का मनोरंजन करना', 'किसी व्यक्ति की आलोचना करना'], 'ऐसे संदेश सरकार या संस्था जनहित में जारी करती है।'),
    ('C2', 'रेडियो साक्षात्कार सुनते समय प्रस्तोता के प्रश्न ध्यान से सुनना क्यों उपयोगी है?', 'प्रस्तोता के प्रश्न बताते हैं कि अगला उत्तर किस विषय पर होगा; इससे सुनने वाला मुख्य जानकारी पहचानकर नोट कर पाता है।', '1 अंक प्रश्नों की संकेतक भूमिका, 1 अंक उत्तर पहचानने/नोट लेने से संबंध।'),
    ('C2', 'स्वास्थ्य-संबंधी श्रव्य अंशों में अंक, समय और आँकड़े (जैसे ‘108’, ‘आठ से दस घंटे’) अलग से लिखना क्यों ज़रूरी है?', 'ऐसे विवरण प्रायः प्रश्नों में सीधे पूछे जाते हैं और एक बार सुनने पर भूल जाते हैं; तुरंत लिखने से सटीक उत्तर दिया जा सकता है।', '1 अंक कारण, 1 अंक उदाहरण सहित प्रयोग।'),
]))
SPEC['ch02-st3'] = ('writing', dict(tt='brochure', tasks=[
    ('आपके विद्यालय की स्वास्थ्य-समिति परीक्षा से पहले विद्यार्थियों के लिए ‘तनाव-मुक्त परीक्षा’ पत्रक बाँटना चाहती है।', ['परीक्षा-तनाव के लक्षण', 'पढ़ाई, नींद और भोजन से जुड़े सुझाव', 'परामर्शदाता से संपर्क का तरीका']),
    ('आपके शहर में डेंगू के मामले बढ़ रहे हैं। एक स्वयंसेवी संस्था के लिए आप जन-जागरूकता पत्रक तैयार कर रहे हैं।', ['डेंगू कैसे फैलता है', 'घर और मोहल्ले में बचाव के उपाय', 'लक्षण दिखने पर क्या करें']),
    ('एक सामुदायिक केंद्र बुज़ुर्गों के लिए मुफ़्त योग-कक्षाएँ शुरू कर रहा है। आपको इसके लिए पत्रक बनाना है।', ['कक्षाओं का समय और स्थान', 'बुज़ुर्गों के लिए योग के लाभ', 'पंजीकरण की प्रक्रिया']),
    ('आपके विद्यालय में कई विद्यार्थी नाश्ता किए बिना आते हैं। कैंटीन ‘स्वस्थ नाश्ता’ अभियान के लिए पत्रक चाहती है।', ['नाश्ता छोड़ने के दुष्प्रभाव', 'जल्दी बनने वाले पौष्टिक विकल्प', 'कैंटीन की नई योजना']),
    ('किशोरों में मोबाइल की लत पर एक ग़ैर-सरकारी संस्था माता-पिता के लिए पत्रक तैयार कर रही है।', ['लत के चेतावनी-संकेत', 'घर में अपनाए जा सकने वाले नियम', 'मदद के लिए हेल्पलाइन']),
], items=[
    ('C1', 'जागरूकता पत्रक में बुलेट-बिंदुओं का प्रयोग क्यों किया जाता है?', 'जानकारी को संक्षिप्त और जल्दी पढ़ने योग्य बनाने के लिए', ['पत्रक को लंबा दिखाने के लिए', 'लेखक की निजी भावनाएँ प्रकट करने के लिए', 'कहानी सुनाने के लिए'], 'पत्रक जल्दी पढ़ा जाता है; बिंदु मुख्य जानकारी उभारते हैं।'),
    ('C1', 'पत्रक में आम जनता को संबोधित करने के लिए सबसे उपयुक्त सर्वनाम कौन-सा है?', 'आप', ['तू', 'तुम', 'मैं'], 'पत्रक आम जनता के लिए होता है, इसलिए आदरसूचक ‘आप’।'),
    ('C2', 'जागरूकता पत्रक और लेख, दोनों जानकारी देते हैं; फिर भी इनके प्रारूप में मुख्य अंतर क्या है?', 'पत्रक में संक्षिप्त शीर्षक, उपशीर्षक, बुलेट-बिंदु, निर्देश और संपर्क-सूत्र होते हैं और वह तुरंत कार्रवाई के लिए प्रेरित करता है; लेख में अनुच्छेदों में विकसित विचार, विश्लेषण और लेखक का नाम होता है।', '1 अंक प्रत्येक पाठ-प्रकार की विशेषता, 1 अंक उद्देश्य के अंतर के लिए।', 3),
]))
SPEC['ch02-st4'] = ('grammar', dict(focus='लेखन में सलाह और सुझाव देने के लिए आज्ञार्थ, विधिलिंग और ‘चाहिए’ वाले वाक्यों का सटीक प्रयोग कीजिए।', gens=[
    g_choose_form(IMP_BANK, IMP_LABELS, name='g_imp'),
    g_free([('‘{topic}’ विषय पर अपने छोटे भाई या बहन को 80–100 शब्दों का एक संदेश लिखिए जिसमें कम से कम पाँच सलाहें ‘तुम’ वाले आज्ञार्थ रूप में हों।',
             'अपेक्षित: ‘तुम’ वाले आज्ञार्थ रूप (करो, पियो, सो जाओ, मत लो) का शुद्ध प्रयोग; आत्मीय लहजा; सलाहें विषय से जुड़ी।'),
            ('‘{topic}’ विषय पर मोहल्ले के सूचना-पट के लिए 80–100 शब्दों का एक विनम्र निवेदन लिखिए जिसमें विधिलिंग (करें, पिएँ, न लें) और ‘चाहिए’ वाले वाक्यों का प्रयोग हो।',
             'अपेक्षित: विधिलिंग और ‘चाहिए’ वाले वाक्यों का शुद्ध प्रयोग (चाहिए के साथ कर्म से अन्विति: सब्ज़ियाँ खानी चाहिए); विनम्र, औपचारिक लहजा।')]),
], items=[
    ('C1', '“कृपया शांत रहें” — इस वाक्य में क्रिया का कौन-सा रूप है?', 'विधिलिंग (विनम्र अनुरोध)', ['सामान्य भूतकाल', 'अपूर्ण वर्तमान काल', 'प्रश्नवाचक'], '‘रहें’ — विधिलिंग; सूचना-पट और निर्देशों में प्रचलित।'),
    ('C1', 'किस वाक्य में आदरसूचक आज्ञार्थ का प्रयोग है?', 'कृपया बैठिए।', ['बैठो।', 'बैठ।', 'वह बैठेगा।'], '‘बैठिए’ — ‘आप’ के लिए आदरसूचक आज्ञार्थ।'),
    ('C1', '‘करना’ क्रिया का मानक आदरसूचक आज्ञार्थ रूप क्या है?', 'कीजिए', ['करिया', 'करो', 'करेगा'], '‘करना’ → ‘कीजिए’ (अनियमित रूप); इसी प्रकार ‘लेना’ → ‘लीजिए’, ‘देना’ → ‘दीजिए’, ‘पीना’ → ‘पीजिए’।'),
    ('C2', '“आपको हरी सब्ज़ियाँ खानी चाहिए” में ‘खानी’ क्यों है, ‘खाना’ क्यों नहीं? समझाइए।', '‘चाहिए’ वाले वाक्यों में क्रिया कर्म से अन्विति करती है; कर्म ‘सब्ज़ियाँ’ स्त्रीलिंग है, इसलिए ‘खानी चाहिए’ — मानक हिंदी में यही शुद्ध है।', '1 अंक नियम, 1 अंक इस वाक्य में प्रयोग।'),
    ('C2', 'डॉक्टर किसी मरीज़ से ‘दवा लो’ के बजाय ‘दवा लीजिए’ या ‘दवा लें’ क्यों कहेगा? रजिस्टर की दृष्टि से समझाइए।', 'मरीज़ से औपचारिक और आदरपूर्ण संबंध होता है; ‘लीजिए/लें’ आदरसूचक और विनम्र हैं, जबकि ‘लो’ मित्रों या छोटों के लिए अनौपचारिक रूप है।', '1 अंक रूपों की पहचान, 1 अंक संबंध/रजिस्टर से जोड़ने पर।'),
    ('C3', 'इस अनौपचारिक सलाह को सार्वजनिक सूचना-पट के लिए विधिलिंग में बदलिए: “यहाँ कूड़ा मत फेंको, पानी बर्बाद मत करो।”', 'यहाँ कूड़ा न फेंकें, पानी बर्बाद न करें।', '1 अंक प्रत्येक सही विधिलिंग रूप के लिए।', 2),
]))


# ---------------------------------------------------------------- ch03 आस्थाएँ, मूल्य और उपसंस्कृतियाँ
TH[3] = dict(
    name='आस्थाएँ, मूल्य और उपसंस्कृतियाँ',
    vocab=[
        ('उपसंस्कृति', 'बड़ी संस्कृति के भीतर किसी समूह की अपनी विशिष्ट रुचियाँ, पहनावा और भाषा', 'उपसमूह-संस्कृति', 'हिप-हॉप और गेमिंग जैसी ____ युवाओं को अपनी अलग पहचान देती हैं।'),
        ('मूल्य', 'वे सिद्धांत जिन्हें कोई व्यक्ति या समाज महत्वपूर्ण मानता है', 'आदर्श', 'ईमानदारी और बड़ों का सम्मान हमारे परिवार के मुख्य ____ हैं।'),
        ('आस्था', 'किसी विचार, ईश्वर या व्यक्ति पर गहरा विश्वास', 'श्रद्धा', 'दादी की पूजा-पाठ में गहरी ____ है।'),
        ('पीढ़ी', 'लगभग एक ही समय में जन्मे लोगों का समूह', 'पुश्त', 'हर नई ____ अपने ढंग से फ़ैशन और संगीत को परिभाषित करती है।'),
        ('रूढ़िवादी', 'पुरानी परंपराओं से कसकर बँधा, बदलाव का विरोधी', 'परंपरावादी', 'कुछ ____ लोग अब भी लड़कियों के देर शाम बाहर जाने का विरोध करते हैं।'),
        ('सहिष्णुता', 'दूसरों के अलग विचारों और आस्थाओं को सहन और स्वीकार करना', 'सहनशीलता', 'विविधता से भरे समाज में ____ ही शांति की कुंजी है।'),
        ('पहचान', 'वह विशेषता जिससे कोई व्यक्ति या समूह अलग दिखे', 'अस्मिता', 'टैटू और पहनावा कई युवाओं के लिए अपनी ____ व्यक्त करने का माध्यम हैं।'),
        ('संयुक्त परिवार', 'ऐसा परिवार जिसमें कई पीढ़ियाँ एक साथ रहती हैं', 'सम्मिलित परिवार', 'हमारे ____ में दादा-दादी, चाचा-चाची और सभी बच्चे एक ही घर में रहते हैं।'),
        ('विद्रोह', 'स्थापित नियमों या सत्ता का खुला विरोध', 'बग़ावत', 'पंक संगीत को अक्सर समाज के नियमों के प्रति ____ का प्रतीक माना गया।'),
        ('अनुयायी', 'किसी के विचारों या मार्ग पर चलने वाला', 'समर्थक', 'उस गायक के सोशल मीडिया पर लाखों ____ हैं।'),
        ('भेदभाव', 'किसी के साथ जाति, धर्म, लिंग आदि के आधार पर अनुचित अंतर करना', 'पक्षपात', 'संविधान धर्म या जाति के आधार पर ____ की अनुमति नहीं देता।'),
        ('रीति', 'काम करने का परंपरागत ढंग', 'प्रथा', 'घर आए मेहमान को पहले पानी देना हमारी पुरानी ____ है।'),
        ('स्वीकार्यता', 'समाज द्वारा किसी बात को मान लेने की स्थिति', 'मान्यता', 'पिछले दस वर्षों में ई-स्पोर्ट्स को करियर के रूप में अधिक ____ मिली है।'),
        ('अंधविश्वास', 'बिना तर्क या प्रमाण के किसी बात पर विश्वास', 'वहम', 'बिल्ली के रास्ता काटने को अशुभ मानना एक ____ है।'),
    ],
    topics=['युवा उपसंस्कृतियाँ और पहचान', 'पीढ़ियों का अंतर', 'संयुक्त परिवार बनाम एकल परिवार', 'सहिष्णुता और विविधता',
            'अंधविश्वास और वैज्ञानिक सोच', 'सोशल मीडिया पर बनते नए समुदाय', 'मेरे परिवार के मूल्य'],
    texts=[
        dict(kind='लेख', title='के-पॉप से कव्वाली तक: नई पीढ़ी की पहचान',
             body='गुवाहाटी की सत्रह वर्षीय रिंकी कोरियाई बैंडों के गीतों पर नृत्य के वीडियो बनाती है और उसके ऑनलाइन समूह में दुनिया भर के चार हज़ार सदस्य हैं। वहीं लखनऊ का अयान दोस्तों के साथ कव्वाली की महफ़िलें सजाता है। समाजशास्त्री डॉ. मीनाक्षी राव मानती हैं कि ऐसी उपसंस्कृतियाँ युवाओं को अपनेपन का एहसास देती हैं। “जब परिवार और विद्यालय से मेल न बैठे, तब समान रुचि वाला समूह सहारा बनता है,” वे कहती हैं। पर वे चेताती भी हैं कि ऑनलाइन समूह कभी-कभी बाहरी लोगों के प्रति असहिष्णु हो जाते हैं।',
             qs=[('C1', 'रिंकी के ऑनलाइन समूह में कितने सदस्य हैं?', 'चार हज़ार', ['चार सौ', 'चालीस हज़ार', 'चार लाख']),
                 ('C1', 'अयान किस प्रकार के संगीत की महफ़िलें सजाता है?', 'कव्वाली'),
                 ('C2', 'डॉ. राव के अनुसार उपसंस्कृतियाँ युवाओं के लिए क्यों महत्वपूर्ण हैं? अपने शब्दों में लिखिए।', 'वे युवाओं को अपनेपन और पहचान का एहसास देती हैं; जब परिवार या विद्यालय से तालमेल न हो, तब समान रुचि वाले लोग भावनात्मक सहारा देते हैं।'),
                 ('tf', 'डॉ. राव ऑनलाइन समूहों को पूरी तरह हानिरहित मानती हैं।', 'गलत', '“वे चेताती भी हैं कि ऑनलाइन समूह कभी-कभी बाहरी लोगों के प्रति असहिष्णु हो जाते हैं।”'),
                 ('tf', 'रिंकी के समूह के सदस्य केवल गुवाहाटी के हैं।', 'गलत', '“दुनिया भर के चार हज़ार सदस्य हैं।”'),
                 ('C3', 'लेखक ने रिंकी और अयान, दोनों के उदाहरण साथ-साथ क्यों दिए हैं?', 'यह दिखाने के लिए कि नई पीढ़ी की पहचान वैश्विक और पारंपरिक दोनों रुचियों से बनती है', ['यह साबित करने के लिए कि कव्वाली के-पॉप से बेहतर है', 'दोनों शहरों की जनसंख्या की तुलना करने के लिए', 'यह बताने के लिए कि युवा संगीत नहीं सुनते']),
                 ('C3', 'शीर्षक ‘के-पॉप से कव्वाली तक’ लेख के विषय से कैसे जुड़ता है?', 'शीर्षक युवाओं की रुचियों के विस्तार (विदेशी लोकप्रिय संगीत से परंपरागत सूफ़ी संगीत तक) को दिखाता है, जो लेख के उदाहरणों और विषय — विविध उपसंस्कृतियाँ और पहचान — से मेल खाता है।'),
                 ('C4', '“उपसंस्कृतियाँ युवाओं को जोड़ती भी हैं और बाँटती भी हैं।” लेख के आधार पर इस कथन का मूल्यांकन कीजिए।', 'जोड़ती हैं: अपनापन, वैश्विक मित्रता, रचनात्मकता (रिंकी, अयान)। बाँटती हैं: बाहरी लोगों के प्रति असहिष्णुता, परिवार से दूरी। निष्कर्ष: खुलेपन और संवाद से सकारात्मक पक्ष मज़बूत होता है।')]),
        dict(kind='ब्लॉग प्रविष्टि', title='मेरी दादी और मेरा स्केटबोर्ड — 9 नवंबर',
             body='जब मैंने पहली बार स्केटबोर्ड ख़रीदा, दादी ने कहा, “लड़कियाँ ऐसे खेल नहीं खेलतीं।” मैं नाराज़ हुई, पर बहस नहीं की। अगले रविवार मैं उन्हें पार्क ले गई। उन्होंने देखा कि वहाँ लड़के-लड़कियाँ साथ अभ्यास करते हैं, गिरते हैं, एक-दूसरे को उठाते हैं। लौटते समय दादी मुस्कराईं: “हमारे ज़माने में हम पेड़ों पर चढ़ते थे, तुम इस पहियों वाली तख़्ती पर।” उस दिन मुझे समझ आया कि बदलाव ज़िद से नहीं, संवाद से आता है। आप अपने बड़ों से असहमति कैसे सुलझाते हैं? लिखिए!',
             qs=[('C1', 'दादी ने शुरू में स्केटबोर्ड के बारे में क्या कहा?', 'लड़कियाँ ऐसे खेल नहीं खेलतीं', ['यह बहुत महँगा है', 'यह ख़तरनाक नहीं है', 'उन्हें भी सीखना है']),
                 ('C1', 'लेखिका दादी को कहाँ ले गई?', 'पार्क (जहाँ लोग स्केटबोर्ड का अभ्यास करते हैं)'),
                 ('C2', '“बदलाव ज़िद से नहीं, संवाद से आता है” — इस वाक्य का अर्थ ब्लॉग के प्रसंग में समझाइए।', 'लेखिका ने दादी से लड़ने के बजाय उन्हें अनुभव कराया और बात की; इससे दादी की सोच बदली। यानी विचार बदलने के लिए धैर्य और बातचीत, हठ से अधिक प्रभावी है।'),
                 ('tf', 'दादी की बात सुनकर लेखिका ने उनसे ज़ोरदार बहस की।', 'गलत', '“मैं नाराज़ हुई, पर बहस नहीं की।”'),
                 ('tf', 'पार्क में लड़के और लड़कियाँ साथ अभ्यास करते हैं।', 'सही', '“वहाँ लड़के-लड़कियाँ साथ अभ्यास करते हैं।”'),
                 ('C3', 'दादी की अंतिम टिप्पणी (“हमारे ज़माने में हम पेड़ों पर चढ़ते थे…”) से उनके दृष्टिकोण में आए किस बदलाव का पता चलता है?', 'वे स्केटबोर्डिंग को अपने बचपन के खेलों जैसा स्वाभाविक साहसिक खेल मानने लगीं', ['वे स्केटबोर्ड से और अधिक नाराज़ हो गईं', 'वे चाहती हैं कि लेखिका पेड़ों पर चढ़े', 'उन्हें पार्क पसंद नहीं आया']),
                 ('C3', 'ब्लॉग में पीढ़ियों के अंतर को किस प्रकार दिखाया गया है? दो उदाहरण दीजिए।', 'दादी की पारंपरिक सोच (लड़कियों के खेल पर रोक) बनाम लेखिका की आधुनिक रुचि (स्केटबोर्ड); ‘हमारे ज़माने में पेड़’ बनाम ‘पहियों वाली तख़्ती’ — दोनों पीढ़ियों के खेल अलग पर भावना समान।'),
                 ('C4', 'क्या लेखिका का तरीका हर पारिवारिक असहमति में सफल हो सकता है? उदाहरण सहित अपने विचार दीजिए।', 'पक्ष: अनुभव कराना और संवाद पूर्वाग्रह तोड़ते हैं। सीमा: कुछ मुद्दे गहरी आस्था या सुरक्षा से जुड़े होते हैं जहाँ एक अनुभव पर्याप्त नहीं; धैर्य, समझौता और कभी-कभी तीसरे व्यक्ति की मध्यस्थता चाहिए।')]),
        dict(kind='संपादकीय', title='अंधविश्वास पर विज्ञान की जीत ज़रूरी',
             body='पिछले सप्ताह एक गाँव में ‘भूत भगाने’ के नाम पर एक बीमार बच्ची को अस्पताल ले जाने में देर कर दी गई। यह घटना बताती है कि शिक्षा के प्रसार के बावजूद अंधविश्वास की जड़ें गहरी हैं। संविधान का अनुच्छेद 51A नागरिकों से वैज्ञानिक दृष्टिकोण विकसित करने की अपेक्षा करता है। आस्था व्यक्तिगत अधिकार है, पर जब वह किसी के जीवन को ख़तरे में डाले, तब समाज को चुप नहीं रहना चाहिए। विद्यालयों को केवल विज्ञान के तथ्य नहीं, प्रश्न पूछने की आदत भी सिखानी होगी।',
             qs=[('C1', 'संविधान का कौन-सा अनुच्छेद वैज्ञानिक दृष्टिकोण विकसित करने की बात करता है?', 'अनुच्छेद 51A', ['अनुच्छेद 343', 'अनुच्छेद 21', 'अनुच्छेद 14']),
                 ('C1', 'पाठ में वर्णित घटना में बीमार बच्ची के साथ क्या हुआ?', 'उसे अस्पताल ले जाने में देर कर दी गई'),
                 ('C2', 'लेखक ‘आस्था’ और ‘अंधविश्वास’ के बीच क्या रेखा खींचता है? समझाइए।', 'आस्था व्यक्ति का अधिकार है और उसका सम्मान होना चाहिए; पर जब कोई विश्वास तर्कहीन होकर किसी के जीवन या स्वास्थ्य को ख़तरे में डाले, तब वह अंधविश्वास है जिसका विरोध ज़रूरी है।'),
                 ('tf', 'लेखक मानता है कि शिक्षा ने अंधविश्वास को पूरी तरह समाप्त कर दिया है।', 'गलत', '“शिक्षा के प्रसार के बावजूद अंधविश्वास की जड़ें गहरी हैं।”'),
                 ('C3', 'संपादकीय का स्वर (लहजा) कैसा है?', 'चिंतित और सुधार की माँग करने वाला', ['हास्यपूर्ण और हल्का', 'पूरी तरह तटस्थ और सूचनात्मक', 'निराशावादी और उदासीन']),
                 ('C3', 'लेखक विद्यालयों से क्या अपेक्षा करता है और यह सुझाव समस्या से कैसे जुड़ा है?', 'विद्यालय केवल तथ्य न रटाएँ, बल्कि प्रश्न पूछने की आदत सिखाएँ; क्योंकि अंधविश्वास बिना प्रश्न किए मान लेने से पनपता है, इसलिए तर्कशील सोच उसकी जड़ पर प्रहार करती है।'),
                 ('C4', 'क्या केवल क़ानून बनाकर अंधविश्वास को रोका जा सकता है? संपादकीय के तर्कों को ध्यान में रखते हुए अपना मत लिखिए।', 'क़ानून हानिकारक प्रथाओं पर रोक लगा सकता है, पर सोच बदलने के लिए शिक्षा, स्वास्थ्य-सेवाओं तक पहुँच और सामुदायिक संवाद आवश्यक (संपादकीय: प्रश्न पूछने की आदत)। संतुलित निष्कर्ष।')]),
    ],
    tasks=[
        ('आपके शहर के समाचार-पत्र में एक पाठक ने लिखा है कि “आज के युवा अपने मूल्यों और परंपराओं को भूल रहे हैं।” आप इस मत पर प्रतिक्रिया देना चाहते हैं।', 'opinion',
         ['पाठक के मत का संक्षिप्त उल्लेख', 'युवाओं के मूल्यों के बारे में आपके तर्क और उदाहरण', 'संतुलित निष्कर्ष']),
        ('आपकी विद्यालय-पत्रिका ‘हमारी पहचान’ पर विशेषांक निकाल रही है। आप किसी युवा उपसंस्कृति (जैसे गेमिंग, रैप, कॉस्प्ले) पर लिखना चाहते हैं।', 'article',
         ['उस उपसंस्कृति की विशेषताएँ', 'युवा उसकी ओर क्यों आकर्षित होते हैं', 'उसके सकारात्मक और नकारात्मक पक्ष']),
        ('आप एक संयुक्त परिवार में रहते हैं। आपका एक मित्र, जो एकल परिवार में रहता है, जानना चाहता है कि आपके घर में जीवन कैसा है।', 'pletter',
         ['आपके परिवार के सदस्य और दिनचर्या', 'संयुक्त परिवार के लाभ और कठिनाइयाँ', 'परिवार के कौन-से मूल्य आपको प्रिय हैं']),
        ('विद्यालय की अंतर-सांस्कृतिक सभा में आपको ‘विविधता में एकता: सहिष्णुता क्यों ज़रूरी है?’ विषय पर भाषण देना है।', 'speech',
         ['विद्यालय/देश की विविधता के उदाहरण', 'असहिष्णुता के ख़तरे', 'विद्यार्थियों से ठोस आह्वान']),
        ('आपने अपने दादा-दादी से बातचीत की और जाना कि उनकी किशोरावस्था आपसे कितनी अलग थी।', 'blog',
         ['उनकी किशोरावस्था की रुचियाँ और नियम', 'आपके जीवन से तुलना', 'आपको किस बात ने सबसे अधिक प्रभावित किया']),
        ('आपके इलाक़े में अफ़वाह फैल रही है कि ग्रहण के समय खाना खाने से बीमारी होती है, और लोग बच्चों को भूखा रख रहे हैं।', 'appeal',
         ['ग्रहण के बारे में वैज्ञानिक तथ्य', 'अंधविश्वास से होने वाली हानि', 'लोगों से अपील और जानकारी का स्रोत']),
    ],
    discuss=[
        ('क्या परिवार के मूल्य बच्चों पर थोपे जाने चाहिए या उन्हें अपने मूल्य स्वयं चुनने देने चाहिए?', ['परिवार नैतिक आधार देता है', 'स्वतंत्र सोच और आत्म-निर्णय का अधिकार', 'संवाद और उदाहरण से मूल्य सिखाना']),
        ('क्या युवा उपसंस्कृतियाँ पारंपरिक संस्कृति के लिए ख़तरा हैं?', ['वैश्वीकरण से स्थानीय परंपराएँ पीछे', 'उपसंस्कृतियाँ परंपरा को नए रूप देती हैं (फ़्यूज़न संगीत)', 'संस्कृति स्थिर नहीं, बदलती रहती है']),
        ('क्या सोशल मीडिया ने पीढ़ियों के बीच दूरी बढ़ाई है?', ['डिजिटल भाषा और रुचियों का अंतर', 'वीडियो-कॉल से दूर रहने वाले दादा-दादी से जुड़ाव', 'तकनीक सिखाने से संवाद बढ़ता है']),
        ('संयुक्त परिवार या एकल परिवार — आज के समय में कौन-सा बेहतर है?', ['संयुक्त परिवार में सहयोग और देखभाल', 'एकल परिवार में स्वतंत्रता और निजता', 'परिस्थिति और आपसी संबंधों पर निर्भर']),
        ('क्या टैटू और अलग पहनावे से किसी व्यक्ति के चरित्र का अनुमान लगाना उचित है?', ['रूढ़ धारणाएँ और पूर्वाग्रह', 'आत्म-अभिव्यक्ति का अधिकार', 'कार्यस्थल के नियम और सामाजिक संदर्भ']),
        ('क्या धार्मिक त्योहारों को सार्वजनिक रूप से मनाने के लिए कुछ नियम होने चाहिए?', ['सांस्कृतिक अभिव्यक्ति और सामुदायिक आनंद', 'शोर, यातायात और पर्यावरण की समस्या', 'सभी समुदायों के लिए समान और संतुलित नियम']),
    ],
    pics=[('एक घर के आँगन में दिवाली की रात तीन पीढ़ियाँ हैं: दादी दीया जला रही हैं, माता-पिता मिठाई बाँट रहे हैं और किशोर बच्चे फ़ोन से सेल्फ़ी ले रहे हैं।',
           ['परंपरा और आधुनिकता का साथ-साथ होना', 'पारिवारिक मूल्यों और त्योहारों की भूमिका', 'पीढ़ियों के बीच अलग ढंग से जश्न मनाना']),
          ('एक शहर के चौक पर रंग-बिरंगे कपड़ों और बालों वाले युवा ब्रेक-डांस कर रहे हैं; कुछ बुज़ुर्ग राहगीर हैरानी से देख रहे हैं, कुछ ताली बजा रहे हैं।',
           ['युवा उपसंस्कृति और आत्म-अभिव्यक्ति', 'समाज की मिली-जुली प्रतिक्रिया', 'सार्वजनिक स्थानों पर कला']),
          ('एक गुरुद्वारे के लंगर में अलग-अलग पहनावे वाले लोग ज़मीन पर पंक्ति में बैठकर साथ भोजन कर रहे हैं; स्वयंसेवक रोटियाँ परोस रहे हैं।',
           ['समानता और सेवा का मूल्य', 'आस्था और सामुदायिक सहयोग', 'विविधता में एकता का उदाहरण'])],
)

SPEC['ch03-st1'] = ('reading', dict(focus='लेख में युवा उपसंस्कृतियों से जुड़े ठोस उदाहरण दीजिए।', items=[
    ('C1', 'किसी लेख में ‘राय’ (मत) को ‘तथ्य’ से अलग पहचानने का सबसे अच्छा संकेत क्या है?', '‘मानती हैं’, ‘मेरे विचार में’, ‘चाहिए’ जैसे शब्द', ['संख्याएँ और तारीख़ें', 'स्थानों के नाम', 'उद्धरण-चिह्नों का न होना'], 'राय प्रायः ‘मानना’, ‘लगता है’, ‘चाहिए’ जैसे शब्दों से व्यक्त होती है; तथ्य जाँचे जा सकते हैं।'),
    ('C2', '“रिंकी के समूह में चार हज़ार सदस्य हैं” और “उपसंस्कृतियाँ युवाओं को अपनेपन का एहसास देती हैं” — इनमें कौन-सा तथ्य है और कौन-सा राय? कारण सहित बताइए।', 'पहला तथ्य है — इसे गिनकर जाँचा जा सकता है; दूसरा राय/व्याख्या है — यह समाजशास्त्री का मत है जिससे असहमत हुआ जा सकता है।', '1 अंक सही वर्गीकरण, 1 अंक कारण।'),
    ('C2', 'युवा उपसंस्कृतियों पर लिखे लेखों में ‘विशेषज्ञ की राय’ और ‘युवा का निजी अनुभव’ दोनों क्यों दिए जाते हैं?', 'निजी अनुभव लेख को जीवंत और विश्वसनीय मानवीय चेहरा देता है; विशेषज्ञ की राय उसे व्यापक संदर्भ और प्रामाणिकता देती है — दोनों मिलकर संतुलित चित्र बनाते हैं।', '1 अंक प्रत्येक के प्रभाव के लिए, 1 अंक संतुलन के विचार के लिए।', 3),
]))
SPEC['ch03-st2'] = ('writing', dict(tt='opinion', tasks=[
    ('आपके विद्यालय ने नियम बनाया है कि विद्यार्थी अपने बालों को रंग नहीं सकते। विद्यालय की वेबसाइट पर इस विषय पर मत-प्रधान लेख आमंत्रित हैं।', ['नियम के पक्ष के तर्क', 'आत्म-अभिव्यक्ति और पहचान का प्रश्न', 'आपका स्पष्ट मत और सुझाव']),
    ('एक राष्ट्रीय पत्रिका ने पूछा है: “क्या संयुक्त परिवार की परंपरा ख़त्म हो रही है?” आप इस पर अपना मत-प्रधान लेख भेजना चाहते हैं।', ['आँकड़े या उदाहरण', 'बदलाव के कारण', 'आपका निष्कर्ष कि यह अच्छा है या बुरा']),
    ('“ऑनलाइन गेमिंग समुदाय युवाओं को अकेला बना रहे हैं।” — इस कथन पर समाचार-पत्र के युवा-पृष्ठ के लिए लिखना है।', ['कथन के पक्ष में तर्क', 'गेमिंग समुदायों के सकारात्मक पक्ष', 'आपका संतुलित मत']),
    ('आपके शहर में कुछ लोग अलग धर्म के पड़ोसियों के त्योहारों में शामिल होने का विरोध कर रहे हैं। आप सहिष्णुता पर लिखना चाहते हैं।', ['विविधता के लाभ', 'विरोध के पीछे के डर', 'सहिष्णु समाज के लिए सुझाव']),
    ('“पुराने मूल्य आज के समय में अप्रासंगिक हैं।” — इस विचार पर अपनी विद्यालय-पत्रिका के लिए लिखना है।', ['कौन-से मूल्य बदल गए हैं', 'कौन-से मूल्य आज भी ज़रूरी हैं', 'आपका स्पष्ट निष्कर्ष']),
], items=[
    ('C1', 'मत-प्रधान लेख में विरोधी मत का उल्लेख क्यों किया जाता है?', 'उसका खंडन करके अपने तर्क को अधिक विश्वसनीय बनाने के लिए', ['लेख की शब्द-संख्या बढ़ाने के लिए', 'पाठक को भ्रमित करने के लिए', 'अपना मत छिपाने के लिए'], 'विरोधी मत का उल्लेख और खंडन संतुलित, परिपक्व तर्क दिखाता है।'),
    ('C1', 'इनमें से कौन-सा संयोजक विरोधी विचार प्रस्तुत करने के लिए उपयुक्त है?', 'दूसरी ओर', ['इसके अतिरिक्त', 'उदाहरण के लिए', 'इसी प्रकार'], '‘दूसरी ओर’, ‘इसके विपरीत’, ‘फिर भी’ विरोध दिखाते हैं।'),
    ('C2', 'मत-प्रधान लेख में ‘तर्क’ और ‘प्रमाण’ में क्या अंतर है? उदाहरण दीजिए।', 'तर्क वह कारण है जो मत का समर्थन करता है (संयुक्त परिवार बुज़ुर्गों को सुरक्षा देता है); प्रमाण वह तथ्य, आँकड़ा या उदाहरण है जो तर्क को सिद्ध करता है (एक सर्वेक्षण के आँकड़े, किसी परिवार का अनुभव)।', '1 अंक प्रत्येक अवधारणा, 1 अंक उदाहरण।', 3),
    ('C3', 'इस कमज़ोर निष्कर्ष को बेहतर बनाइए: “तो यह था मेरा लेख। धन्यवाद।”', 'नमूना: “अतः स्पष्ट है कि मूल्य बदलते नहीं, उनके रूप बदलते हैं। यदि हम परंपरा और आधुनिकता के बीच संवाद बनाए रखें, तो नई पीढ़ी अपनी जड़ों से जुड़ी रहकर भी आगे बढ़ सकती है।”', '1 अंक मत की पुनः पुष्टि, 1 अंक मुख्य तर्कों का सार, 1 अंक पाठक पर प्रभाव डालने वाला अंतिम वाक्य; ‘धन्यवाद’ जैसा भाषण-समापन अनुचित।'),
]))
SPEC['ch03-st3'] = ('oral', dict(focus='लेखन में अपने परिवार या समुदाय के मूल्यों के ठोस उदाहरण दीजिए।', items=[
    ('C1', 'मौखिक चर्चा में शिक्षक के प्रश्न का उत्तर देते समय सबसे अच्छी रणनीति क्या है?', 'मत देना, कारण बताना और उदाहरण से पुष्ट करना', ['केवल ‘हाँ’ या ‘नहीं’ कहना', 'रटा हुआ भाषण दोहराना', 'प्रश्न को अनदेखा कर दूसरे विषय पर बोलना'], 'मत + कारण + उदाहरण से उत्तर विकसित और संवादात्मक बनता है।'),
    ('C2', 'मौखिक परीक्षा में ‘मुझे नहीं पता’ कहने के बजाय कौन-से वाक्यांश बेहतर हैं और क्यों?', '“यह एक कठिन प्रश्न है, पर मुझे लगता है कि…”, “मैंने इस पर पहले नहीं सोचा, लेकिन…” — ये बातचीत को जारी रखते हैं, सोचने का समय देते हैं और संवाद-कौशल (मानदंड C) दिखाते हैं।', '1 अंक उपयुक्त वाक्यांश, 1 अंक कारण।'),
    ('C3', 'शिक्षक कहते हैं: “आपके परिवार में कौन-सा मूल्य सबसे महत्वपूर्ण है?” — 60–80 शब्दों में उत्तर दीजिए जिसमें एक पारिवारिक घटना का उदाहरण हो।', 'अपेक्षित: एक मूल्य का स्पष्ट नाम (जैसे ईमानदारी, अतिथि-सत्कार, बड़ों का सम्मान), उसका महत्व, एक ठोस पारिवारिक घटना, और निजी विचार।', '1 अंक मूल्य, 1 अंक कारण, 1 अंक ठोस उदाहरण, 1 अंक प्रवाह और शुद्धता।', 4),
]))


# ---------------------------------------------------------------- ch04 भाषा और पहचान
TH[4] = dict(
    name='भाषा और पहचान',
    vocab=[
        ('मातृभाषा', 'वह भाषा जो बच्चा सबसे पहले घर में सीखता है', 'मादरी ज़बान', 'मेरी ____ मराठी है, पर विद्यालय में मैं हिंदी और अंग्रेज़ी भी बोलता हूँ।'),
        ('बहुभाषिकता', 'एक से अधिक भाषाएँ जानने और प्रयोग करने की क्षमता', 'बहुभाषिता', 'भारत जैसे देश में ____ एक सामान्य बात है; लोग दिन भर में तीन भाषाएँ बोल लेते हैं।'),
        ('बोली', 'किसी क्षेत्र विशेष में बोला जाने वाला भाषा का रूप', 'उपभाषा', 'भोजपुरी एक लोकप्रिय ____ है जिसमें बहुत-से लोकगीत गाए जाते हैं।'),
        ('लिपि', 'भाषा को लिखने के लिए प्रयुक्त अक्षरों की व्यवस्था', 'लेखन-प्रणाली', 'हिंदी, मराठी और नेपाली देवनागरी ____ में लिखी जाती हैं।'),
        ('उच्चारण', 'शब्दों को बोलने का ढंग', 'बोलने का लहजा', 'उसके ____ से पता चलता है कि वह बिहार से है।'),
        ('अनुवाद', 'एक भाषा की सामग्री को दूसरी भाषा में बदलना', 'भाषांतर', 'प्रेमचंद की कहानियों का कई विदेशी भाषाओं में ____ हुआ है।'),
        ('विलुप्त', 'पूरी तरह समाप्त हो चुका या होने वाला', 'लुप्त', 'यूनेस्को के अनुसार दुनिया की सैकड़ों भाषाएँ ____ होने के कगार पर हैं।'),
        ('संप्रेषण', 'विचारों और सूचनाओं का आदान-प्रदान', 'संचार', 'भाषा का मुख्य उद्देश्य प्रभावी ____ है।'),
        ('शब्दावली', 'किसी भाषा या व्यक्ति के शब्दों का भंडार', 'शब्द-भंडार', 'रोज़ अख़बार पढ़ने से मेरी हिंदी ____ समृद्ध हुई है।'),
        ('प्रवाह', 'बिना रुके सहज रूप से बोलने की क्षमता', 'धाराप्रवाहिता', 'दो साल के अभ्यास के बाद वह हिंदी ____ के साथ बोलने लगी।'),
        ('विरासत', 'पूर्वजों से मिली संपत्ति, परंपरा या संस्कृति', 'धरोहर', 'लोकगीत हमारी भाषाई ____ का अमूल्य हिस्सा हैं।'),
        ('हीनभावना', 'स्वयं को दूसरों से कमतर समझने का भाव', 'आत्महीनता', 'कई बच्चे अपनी बोली बोलने में ____ महसूस करते हैं, क्योंकि लोग उनका मज़ाक उड़ाते हैं।'),
        ('मिश्रित', 'कई चीज़ों को मिलाकर बना', 'संकर', '‘हिंग्लिश’ हिंदी और अंग्रेज़ी की ____ भाषा-शैली है।'),
        ('अभिव्यक्ति', 'विचारों और भावनाओं को प्रकट करना', 'प्रकटीकरण', 'अपनी भाषा में भावनाओं की ____ सबसे सहज होती है।'),
    ],
    topics=['मेरी मातृभाषा, मेरी पहचान', 'हिंग्लिश: भाषा का विकास या विनाश?', 'बहुभाषिकता के लाभ', 'विलुप्त होती भाषाएँ और बोलियाँ',
            'विदेश में बसे परिवारों में मातृभाषा', 'सोशल मीडिया और बदलती भाषा', 'हिंदी दिवस का महत्व'],
    texts=[
        dict(kind='लेख', title='हिंग्लिश: नई पीढ़ी की नई ज़बान?',
             body='“यार, आज का लेक्चर बहुत बोरिंग था, पर क्विज़ में मज़ा आया।” मेट्रो में ऐसे वाक्य अब आम हैं। भाषाविद् प्रो. आलोक सिन्हा के अनुसार हिंग्लिश कोई बीमारी नहीं, बल्कि दो भाषाओं के संपर्क का स्वाभाविक परिणाम है। वे याद दिलाते हैं कि हिंदी ने पहले भी फ़ारसी, अरबी और पुर्तगाली से शब्द लिए हैं — ‘मेज़’, ‘किताब’ और ‘चाबी’ इसके उदाहरण हैं। फिर भी वे चिंतित हैं कि कई युवा हिंदी में एक पूरा अनुच्छेद लिख नहीं पाते।',
             qs=[('C1', 'प्रो. सिन्हा के अनुसार हिंग्लिश किसका परिणाम है?', 'दो भाषाओं के संपर्क का', ['सरकारी नीति का', 'हिंदी की कमज़ोरी का', 'केवल फ़िल्मों का']),
                 ('C1', 'पाठ में पुर्तगाली भाषा से आए किस शब्द का उदाहरण है?', 'चाबी'),
                 ('C2', '“हिंग्लिश कोई बीमारी नहीं” — प्रो. सिन्हा ऐसा क्यों कहते हैं? समझाइए।', 'क्योंकि भाषाएँ हमेशा एक-दूसरे से शब्द लेती रही हैं (फ़ारसी, अरबी, पुर्तगाली के उदाहरण); इसलिए मिश्रण स्वाभाविक विकास है, कोई ख़तरनाक विकृति नहीं।'),
                 ('tf', 'प्रो. सिन्हा को युवाओं की हिंदी लेखन-क्षमता को लेकर कोई चिंता नहीं है।', 'गलत', '“फिर भी वे चिंतित हैं कि कई युवा हिंदी में एक पूरा अनुच्छेद लिख नहीं पाते।”'),
                 ('tf', 'हिंदी ने पहले कभी दूसरी भाषाओं से शब्द नहीं लिए।', 'गलत', '“हिंदी ने पहले भी फ़ारसी, अरबी और पुर्तगाली से शब्द लिए हैं।”'),
                 ('C3', 'लेख की शुरुआत मेट्रो में सुने गए वाक्य से क्यों की गई है?', 'पाठकों को रोज़मर्रा का परिचित उदाहरण देकर तुरंत विषय से जोड़ने के लिए', ['मेट्रो की आलोचना करने के लिए', 'यह बताने के लिए कि क्विज़ उबाऊ था', 'अंग्रेज़ी सिखाने के लिए']),
                 ('C3', 'प्रो. सिन्हा का दृष्टिकोण संतुलित क्यों कहा जा सकता है? पाठ से दो प्रमाण दीजिए।', 'वे हिंग्लिश को स्वाभाविक मानते हैं (‘कोई बीमारी नहीं’, पुराने उधार शब्दों के उदाहरण), पर साथ ही युवाओं की लेखन-क्षमता पर चिंता भी जताते हैं (‘फिर भी वे चिंतित हैं…’)।'),
                 ('C4', '“हिंग्लिश हिंदी को समृद्ध कर रही है।” — लेख के आधार पर इस कथन से आप कहाँ तक सहमत हैं?', 'पक्ष: संपर्क से शब्द-भंडार बढ़ता है, भाषा जीवंत रहती है, युवाओं में लोकप्रिय। विपक्ष: औपचारिक हिंदी लेखन-कौशल का ह्रास, हिंदी के अपने शब्दों का प्रयोग घटना। निष्कर्ष: संदर्भ के अनुसार रजिस्टर बदलने की क्षमता आवश्यक।')]),
        dict(kind='साक्षात्कार', title='“मेरी बेटी पहले हिंदी में सपने देखती थी” — मॉरीशस से श्रीमती दीपा रामगुलाम',
             body='प्रश्न: आपके परिवार में कौन-सी भाषाएँ बोली जाती हैं?\nउत्तर: घर में दादी भोजपुरी बोलती हैं, हम हिंदी और क्रियोल, और बच्चे विद्यालय में अंग्रेज़ी-फ़्रेंच पढ़ते हैं।\nप्रश्न: क्या बच्चे हिंदी से जुड़े हैं?\nउत्तर: छोटी उम्र में बेटी हिंदी में सपने देखती थी, अब फ़्रेंच में देखती है! इसलिए हम हर शनिवार उसे हिंदी कक्षा भेजते हैं और रात को रामायण की कहानियाँ सुनाते हैं।\nप्रश्न: इतनी भाषाओं से भ्रम नहीं होता?\nउत्तर: बिल्कुल नहीं। हर भाषा एक खिड़की है।',
             qs=[('C1', 'श्रीमती रामगुलाम के घर में दादी कौन-सी भाषा बोलती हैं?', 'भोजपुरी', ['फ़्रेंच', 'अंग्रेज़ी', 'तमिल']),
                 ('C1', 'बेटी हिंदी कक्षा में कब जाती है?', 'हर शनिवार'),
                 ('C2', '“हर भाषा एक खिड़की है” — इस रूपक का अर्थ स्पष्ट कीजिए।', 'जैसे खिड़की से बाहर की दुनिया दिखती है, वैसे ही हर भाषा एक नई संस्कृति, विचार और लोगों से जुड़ने का रास्ता खोलती है; भाषाएँ भ्रम नहीं, विस्तार देती हैं।'),
                 ('tf', 'श्रीमती रामगुलाम के अनुसार कई भाषाएँ सीखने से बच्चों में भ्रम होता है।', 'गलत', '“बिल्कुल नहीं। हर भाषा एक खिड़की है।”'),
                 ('C3', 'बेटी के “अब फ़्रेंच में सपने देखने” से परिवार की किस चिंता का पता चलता है?', 'कि बेटी हिंदी से दूर होती जा रही है और प्रमुख भाषा उसकी सोच की भाषा बन रही है', ['कि बेटी को फ़्रेंच नहीं आती', 'कि बेटी को नींद नहीं आती', 'कि बेटी विद्यालय नहीं जाती']),
                 ('C3', 'परिवार बेटी को हिंदी से जोड़े रखने के लिए कौन-से दो उपाय करता है और ये उपाय भाषा तथा संस्कृति, दोनों से कैसे जुड़े हैं?', 'शनिवार की हिंदी कक्षा (भाषा का औपचारिक अभ्यास) और रात को रामायण की कहानियाँ (सांस्कृतिक विरासत से भावनात्मक जुड़ाव)।'),
                 ('C4', 'प्रवासी परिवारों में मातृभाषा बचाए रखने की ज़िम्मेदारी किसकी है — परिवार की, समुदाय की या सरकार की? साक्षात्कार के आधार पर तर्क दीजिए।', 'परिवार: घर में भाषा-प्रयोग, कहानियाँ (साक्षात्कार का उदाहरण); समुदाय: शनिवार-कक्षाएँ, उत्सव; सरकार/संस्थाएँ: पाठ्यक्रम में स्थान, सांस्कृतिक केंद्र। निष्कर्ष: साझा ज़िम्मेदारी।')]),
        dict(kind='भाषण', title='हिंदी दिवस पर विद्यार्थी-परिषद अध्यक्ष का भाषण (अंश)',
             body='आदरणीय प्रधानाचार्या जी, शिक्षकगण और मेरे प्यारे साथियो! 14 सितंबर 1949 को संविधान सभा ने देवनागरी लिपि में लिखी हिंदी को संघ की राजभाषा के रूप में स्वीकार किया था। पर साथियो, क्या भाषा केवल सरकारी फ़ाइलों की चीज़ है? नहीं! भाषा वह है जिसमें माँ लोरी गाती है, जिसमें हम पहली बार ‘दोस्त’ कहते हैं। आइए, संकल्प लें कि हम हिंदी को शर्म नहीं, गर्व के साथ बोलेंगे — और दूसरी भाषाओं का भी उतना ही सम्मान करेंगे।',
             qs=[('C1', 'संविधान सभा ने हिंदी को राजभाषा के रूप में कब स्वीकार किया?', '14 सितंबर 1949', ['26 जनवरी 1950', '15 अगस्त 1947', '10 जनवरी 1975']),
                 ('C1', 'वक्ता ने श्रोताओं को किस शब्द से बार-बार संबोधित किया है?', 'साथियो'),
                 ('C2', '“क्या भाषा केवल सरकारी फ़ाइलों की चीज़ है?” — वक्ता ने यह प्रश्न क्यों पूछा?', 'यह अलंकारिक प्रश्न है; उत्तर अपेक्षित नहीं। वक्ता श्रोताओं का ध्यान खींचकर बताना चाहता है कि भाषा केवल प्रशासन की नहीं, भावनाओं और जीवन की भाषा है।'),
                 ('tf', 'वक्ता केवल हिंदी के सम्मान की बात करता है और दूसरी भाषाओं को महत्व नहीं देता।', 'गलत', '“…और दूसरी भाषाओं का भी उतना ही सम्मान करेंगे।”'),
                 ('C3', 'भाषण की कौन-सी विशेषता श्रोताओं को भावनात्मक रूप से जोड़ती है?', 'माँ की लोरी और पहली बार ‘दोस्त’ कहने जैसे आत्मीय उदाहरण', ['तारीख़ों की लंबी सूची', 'कठिन तकनीकी शब्द', 'तृतीय पुरुष में तटस्थ वर्णन']),
                 ('C3', 'इस अंश में भाषण की तीन परंपराएँ पहचानिए और प्रत्येक का एक उदाहरण दीजिए।', 'आदरपूर्ण संबोधन (‘आदरणीय प्रधानाचार्या जी…’); अलंकारिक प्रश्न और उत्तर (‘क्या भाषा…? नहीं!’); आह्वान/संकल्प (‘आइए, संकल्प लें…’)।'),
                 ('C4', 'क्या ‘हिंदी दिवस’ जैसे आयोजन भाषा के प्रति युवाओं का दृष्टिकोण सचमुच बदलते हैं? भाषण के संदर्भ में मूल्यांकन कीजिए।', 'पक्ष: गर्व और जागरूकता, भावनात्मक भाषण प्रेरित करते हैं। विपक्ष: एक दिन का उत्सव, रोज़मर्रा में अंग्रेज़ी का दबाव। निष्कर्ष: पुस्तकालय, लेखन-प्रतियोगिताएँ, डिजिटल सामग्री जैसे निरंतर प्रयास ज़रूरी।')]),
    ],
    tasks=[
        ('आपके विद्यालय में ‘अंतरराष्ट्रीय मातृभाषा दिवस’ (21 फ़रवरी) मनाया जा रहा है। आपको सभा में मातृभाषा के महत्व पर बोलना है।', 'speech',
         ['मातृभाषा और पहचान का संबंध', 'मातृभाषा छोड़ने के नुक़सान', 'साथियों के लिए ठोस सुझाव']),
        ('एक ऑनलाइन पत्रिका ने युवाओं से पूछा है: “क्या हिंग्लिश हिंदी को कमज़ोर कर रही है?” आप अपना लेख भेजना चाहते हैं।', 'opinion',
         ['हिंग्लिश के उदाहरण', 'पक्ष और विपक्ष के तर्क', 'आपका स्पष्ट निष्कर्ष']),
        ('आप विदेश में रहते हैं और आपका छोटा भाई हिंदी बोलने में झिझकता है। आप उसे पत्र लिखकर प्रोत्साहित करना चाहते हैं।', 'pletter',
         ['हिंदी जानने से आपको मिले अनुभव', 'उसकी झिझक दूर करने के उपाय', 'आप उसकी कैसे मदद करेंगे']),
        ('आपने एक सप्ताह तक केवल हिंदी बोलने की चुनौती ली। अपने ब्लॉग पर अनुभव लिखिए।', 'blog',
         ['चुनौती के नियम और कारण', 'मज़ेदार और कठिन पल', 'आपकी भाषा-सीख']),
        ('आपके शहर में एक स्थानीय बोली के लोकगीतों का संग्रहालय बंद होने वाला है। आप सांस्कृतिक विभाग को लिखना चाहते हैं।', 'fletter',
         ['संग्रहालय का महत्व', 'बंद होने से होने वाली हानि', 'संग्रहालय बचाने के सुझाव']),
        ('विद्यालय-पत्रिका के लिए आपको एक ऐसे व्यक्ति का साक्षात्कार लेना है जो पाँच भाषाएँ बोलता है।', 'interview',
         ['भाषाएँ कैसे सीखीं', 'बहुभाषिकता से मिले अवसर', 'युवाओं के लिए भाषा सीखने के सुझाव']),
    ],
    discuss=[
        ('क्या बच्चों की प्रारंभिक शिक्षा मातृभाषा में होनी चाहिए?', ['मातृभाषा में अवधारणाएँ जल्दी समझ आती हैं', 'वैश्विक भाषा (अंग्रेज़ी) के अवसर', 'बहुभाषी शिक्षा का संतुलित मॉडल']),
        ('क्या किसी भाषा के बिना कोई अपनी संस्कृति से पूरी तरह जुड़ा रह सकता है?', ['भाषा में लोकगीत, मुहावरे, कहानियाँ', 'भोजन, त्योहार और मूल्य भाषा के बिना भी', 'अनुवाद से सांस्कृतिक जुड़ाव']),
        ('क्या अंग्रेज़ी बोलने को ‘सफलता’ का प्रतीक मानना उचित है?', ['रोज़गार और वैश्विक संपर्क', 'औपनिवेशिक मानसिकता और हीनभावना', 'कौशल और ज्ञान का महत्व भाषा से अधिक']),
        ('क्या सोशल मीडिया भाषा को बिगाड़ रहा है या नया जीवन दे रहा है?', ['संक्षिप्त रूप और वर्तनी की गड़बड़ी', 'बोलियों और क्षेत्रीय भाषाओं की नई पहुँच', 'रचनात्मक नए शब्द और मीम-संस्कृति']),
        ('क्या विलुप्त होती बोलियों को बचाने का प्रयास सार्थक है?', ['सांस्कृतिक विरासत और ज्ञान की रक्षा', 'आर्थिक उपयोगिता कम', 'डिजिटल अभिलेख और समुदाय की भूमिका']),
    ],
)

COMPOUND = [
    ('रिया हिंदी बोलती है।', 'उसकी माँ तमिल बोलती हैं।', 'रिया हिंदी बोलती है, जबकि उसकी माँ तमिल बोलती हैं।', 'जबकि', 'मिश्र'),
    ('मैंने बहुत अभ्यास किया।', 'मैं भाषण-प्रतियोगिता जीत गया।', 'मैंने बहुत अभ्यास किया, इसलिए मैं भाषण-प्रतियोगिता जीत गया।', 'इसलिए', 'संयुक्त'),
    ('अर्जुन फ़्रेंच समझता है।', 'वह फ़्रेंच बोल नहीं पाता।', 'अर्जुन फ़्रेंच समझता है, लेकिन वह फ़्रेंच बोल नहीं पाता।', 'लेकिन', 'संयुक्त'),
    ('दादी कहानियाँ सुनाती हैं।', 'बच्चे ध्यान से सुनते हैं।', 'दादी कहानियाँ सुनाती हैं और बच्चे ध्यान से सुनते हैं।', 'और', 'संयुक्त'),
    ('वह भोजपुरी बोलता है।', 'उसके दादा बिहार से आए थे।', 'वह भोजपुरी बोलता है, क्योंकि उसके दादा बिहार से आए थे।', 'क्योंकि', 'मिश्र'),
    ('तुम रोज़ हिंदी अख़बार पढ़ोगे।', 'तुम्हारी शब्दावली बढ़ेगी।', 'यदि तुम रोज़ हिंदी अख़बार पढ़ोगे, तो तुम्हारी शब्दावली बढ़ेगी।', 'यदि…तो', 'मिश्र'),
    ('नेहा ने एक किताब ख़रीदी।', 'वह किताब हिंदी की कहानियों का संग्रह है।', 'नेहा ने जो किताब ख़रीदी, वह हिंदी की कहानियों का संग्रह है।', 'जो…वह', 'मिश्र'),
    ('बारिश हो रही थी।', 'हम हिंदी-मेले में गए।', 'हालाँकि बारिश हो रही थी, फिर भी हम हिंदी-मेले में गए।', 'हालाँकि…फिर भी', 'मिश्र'),
    ('शिक्षक कक्षा में आए।', 'सब विद्यार्थी खड़े हो गए।', 'जैसे ही शिक्षक कक्षा में आए, सब विद्यार्थी खड़े हो गए।', 'जैसे ही', 'मिश्र'),
    ('मीरा ने जल्दी काम ख़त्म किया।', 'वह समय पर स्टेशन पहुँच सके।', 'मीरा ने जल्दी काम ख़त्म किया, ताकि वह समय पर स्टेशन पहुँच सके।', 'ताकि', 'मिश्र'),
    ('मैं तेलुगु सीखना चाहता था।', 'मुझे कोई शिक्षक नहीं मिला।', 'मैं तेलुगु सीखना चाहता था, परंतु मुझे कोई शिक्षक नहीं मिला।', 'परंतु', 'संयुक्त'),
    ('पापा ने मुझे एक बात बताई।', 'वे बचपन में बांग्ला बोलते थे।', 'पापा ने मुझे बताया कि वे बचपन में बांग्ला बोलते थे।', 'कि', 'मिश्र'),
    ('तुम आज हिंदी फ़िल्म देखोगे।', 'तुम मराठी नाटक देखने चलोगे।', 'तुम आज हिंदी फ़िल्म देखोगे या मराठी नाटक देखने चलोगे?', 'या', 'संयुक्त'),
    ('मेरे पास शब्दकोश था।', 'मैंने कठिन शब्दों के अर्थ तुरंत ढूँढ लिए।', 'मेरे पास शब्दकोश था, अतः मैंने कठिन शब्दों के अर्थ तुरंत ढूँढ लिए।', 'अतः', 'संयुक्त'),
]
CONNECTORS = ['और', 'लेकिन', 'इसलिए', 'क्योंकि', 'जबकि', 'ताकि', 'या', 'परंतु', 'कि', 'जैसे ही', 'अतः', 'यदि…तो', 'हालाँकि…फिर भी', 'जो…वह']


def g_compound(kit, key, th):
    def join(rng, slot):
        a, b, j, c, t = rng.choice(COMPOUND)
        return dict(stem=f'‘{c}’ का प्रयोग करते हुए इन दो सरल वाक्यों को जोड़कर एक {t} वाक्य बनाइए:\n(1) {a}\n(2) {b}', answer=j, type='short', marks=2,
                    markingKey=f'{j} — 1 अंक सही संयोजक/स्थान, 1 अंक शुद्ध अन्विति और विराम-चिह्न।')
    kit.add(key, 'C3', (1, 4), join, 'short', None, 'cmp_join')

    def pick(rng, slot):
        a, b, j, c, t = rng.choice(COMPOUND)
        if '…' in c:
            return None
        blank = j.replace(f', {c} ', ', ____ ', 1)
        if '____' not in blank:
            blank = j.replace(f' {c} ', ' ____ ', 1)
        if '____' not in blank:
            return None
        wrong = [x for x in CONNECTORS if x != c and '…' not in x and x not in ('परंतु', 'लेकिन') or (c not in ('परंतु', 'लेकिन') and x in ('लेकिन',))]
        wrong = [x for x in dict.fromkeys(wrong) if x != c and '…' not in x]
        syn = {'लेकिन': {'परंतु'}, 'परंतु': {'लेकिन'}, 'इसलिए': {'अतः'}, 'अतः': {'इसलिए'}}
        wrong = [x for x in wrong if x not in syn.get(c, set())]
        return mcq(rng, f'उपयुक्त संयोजक से रिक्त स्थान भरिए:\n“{blank}”', c, rng.sample(wrong, 3), f'अर्थ के अनुसार ‘{c}’ उपयुक्त है: {j}')
    kit.add(key, 'C3', (1, 3), pick, 'mcq', 'p2r', 'cmp_pick')

    def kind(rng, slot):
        a, b, j, c, t = rng.choice(COMPOUND)
        s = rng.choice([a, j, j])
        ans = 'सरल वाक्य' if s == a else f'{t} वाक्य'
        opts = [o for o in ['सरल वाक्य', 'संयुक्त वाक्य', 'मिश्र वाक्य', 'विस्मयादिबोधक वाक्य'] if o != ans]
        return mcq(rng, f'रचना के आधार पर यह वाक्य किस प्रकार का है?\n“{s}”', ans, opts[:3],
                   'संयुक्त वाक्य में दो स्वतंत्र उपवाक्य समानाधिकरण संयोजक (और, लेकिन, इसलिए, या, अतः) से जुड़ते हैं; मिश्र वाक्य में एक प्रधान और एक आश्रित उपवाक्य (कि, क्योंकि, जो, यदि, जबकि, ताकि) होता है।')
    kit.add(key, 'C1', (1, 3), kind, 'mcq', None, 'cmp_kind')

    def split(rng, slot):
        a, b, j, c, t = rng.choice(COMPOUND)
        return dict(stem=f'इस {t} वाक्य को दो सरल वाक्यों में तोड़िए और बताइए कि इसमें कौन-सा संयोजक है:\n“{j}”', answer=f'(1) {a} (2) {b} — संयोजक: {c}', type='short', marks=2,
                    markingKey=f'1 अंक दोनों सरल वाक्यों के लिए ({a} / {b}), 1 अंक संयोजक ‘{c}’ की पहचान के लिए।')
    kit.add(key, 'C2', (1, 3), split, 'short', None, 'cmp_split')

    def para(rng, slot):
        cs = rng.sample(CONNECTORS, 4)
        topic = rng.choice(th['topics'])
        return dict(stem=f'‘{topic}’ विषय पर 80–100 शब्दों का अनुच्छेद लिखिए जिसमें इन चार संयोजकों का सही प्रयोग हो: {", ".join(cs)}। कम से कम दो वाक्य मिश्र वाक्य हों।',
                    answer=f'अपेक्षित: चारों संयोजकों ({", ".join(cs)}) का अर्थ के अनुसार प्रयोग; संयुक्त और मिश्र वाक्यों का मिश्रण; विषय पर केंद्रित, सुसंगत विचार।', type='long', marks=6,
                    markingKey=para_key(6, 'प्रत्येक सही संयोजक-प्रयोग आवश्यक; मिश्र वाक्यों में प्रधान और आश्रित उपवाक्य स्पष्ट हों।'))
    kit.add(key, 'C4', (2, 5), para, 'long', None, 'cmp_para')


DIALECT = [
    ('भोजपुरी', 'का हाल बा?', 'क्या हाल है?'),
    ('भोजपुरी', 'हम बाज़ार जात बानी।', 'मैं बाज़ार जा रहा हूँ।'),
    ('भोजपुरी', 'तू का करत बाड़?', 'तुम क्या कर रहे हो?'),
    ('ब्रज', 'मैया मोरी, मैं नहिं माखन खायो।', 'माँ, मैंने मक्खन नहीं खाया।'),
    ('हरियाणवी', 'के करै सै?', 'क्या कर रहा है?'),
    ('अवधी', 'हम काल्हि जाब।', 'हम कल जाएँगे।'),
    ('राजस्थानी (मारवाड़ी)', 'थे कठै जाओ हो?', 'आप कहाँ जा रहे हैं?'),
    ('भोजपुरी', 'हमार नाम सुनीता ह।', 'मेरा नाम सुनीता है।'),
]


def g_dialect(kit, key, th):
    def fn(rng, slot):
        b, s, m = rng.choice(DIALECT)
        return dict(stem=f'यह वाक्य {b} में है: “{s}”\nइसे मानक हिंदी (खड़ी बोली) में लिखिए और एक ऐसा शब्द पहचानिए जो मानक हिंदी से अलग है।', answer=f'{m} (बोली का कोई भिन्न शब्द/क्रिया-रूप पहचानना अपेक्षित)',
                    type='short', marks=2, markingKey=f'1 अंक मानक रूप: {m}; 1 अंक बोली के किसी भिन्न शब्द/क्रिया-रूप की सही पहचान।')
    kit.add(key, ('C2', 'C3'), (1, 4), fn, 'short', None, 'dialect')


SPEC['ch04-st1'] = ('reading', dict(focus='लेखन में बहुभाषिकता और पहचान से जुड़े निजी अनुभव शामिल कीजिए।', items=[
    ('C1', '‘हिंग्लिश’ शब्द किस प्रकार बना है?', 'हिंदी और इंग्लिश को मिलाकर', ['हिंदी और इंग्लैंड को मिलाकर', 'हिंदुस्तानी और फ़्रेंच से', 'हिंदी के एक पुराने शब्द से'], 'हिंदी + इंग्लिश = हिंग्लिश (मिश्रित भाषा-शैली)।'),
    ('C2', 'बातचीत में एक भाषा से दूसरी भाषा में आना-जाना (कोड-मिश्रण) बहुभाषी लोगों में क्यों आम है? एक उदाहरण देकर समझाइए।', 'बहुभाषी लोग विषय, श्रोता और भावना के अनुसार उस भाषा के शब्द चुनते हैं जो उस समय सबसे सटीक या सहज हो — जैसे “मीटिंग के बाद हम घर जाएँगे” में ‘मीटिंग’ अंग्रेज़ी से।', '1 अंक कारण, 1 अंक उपयुक्त उदाहरण।'),
]))
SPEC['ch04-st2'] = ('grammar', dict(focus='लेखन में सरल, संयुक्त और मिश्र वाक्यों का संतुलित प्रयोग और विविध संयोजक शब्द दिखाइए।', gens=[g_compound], items=[
    ('C1', 'इनमें से कौन-सा संयोजक मिश्र वाक्य बनाता है?', 'क्योंकि', ['और', 'या', 'लेकिन'], '‘क्योंकि’ आश्रित (कारणवाचक) उपवाक्य जोड़ता है, इसलिए मिश्र वाक्य बनता है।'),
    ('C1', 'संयुक्त वाक्य की सबसे सटीक परिभाषा कौन-सी है?', 'दो या अधिक स्वतंत्र उपवाक्य जो समानाधिकरण संयोजक से जुड़े हों', ['एक ही उपवाक्य वाला वाक्य', 'एक प्रधान और एक आश्रित उपवाक्य वाला वाक्य', 'केवल प्रश्न पूछने वाला वाक्य'], 'संयुक्त वाक्य: और, लेकिन, या, इसलिए से जुड़े स्वतंत्र उपवाक्य।'),
    ('C2', 'संयुक्त और मिश्र वाक्य में अंतर एक-एक उदाहरण से स्पष्ट कीजिए।', 'संयुक्त: दोनों उपवाक्य स्वतंत्र — “मैंने अभ्यास किया, इसलिए मैं जीत गया।” मिश्र: एक प्रधान, एक आश्रित — “मैं जीत गया, क्योंकि मैंने अभ्यास किया था।” (‘क्योंकि…’ वाला भाग अकेले पूरा अर्थ नहीं देता)।', '1 अंक प्रत्येक परिभाषा, 1 अंक सही उदाहरण।', 3),
    ('C2', 'पेपर 1 के लेखन में केवल सरल वाक्यों का प्रयोग करने से मानदंड A (भाषा) पर क्या प्रभाव पड़ता है? समझाइए।', 'मानदंड A में जटिल संरचनाओं का प्रभावी प्रयोग अपेक्षित है; केवल सरल वाक्य भाषा को एकरस और सीमित दिखाते हैं, जिससे उच्च बैंड नहीं मिलता। संयुक्त और मिश्र वाक्य विचारों के संबंध (कारण, विरोध, शर्त) स्पष्ट करते हैं।', '1 अंक मानदंड A की अपेक्षा, 1 अंक प्रभाव की व्याख्या।'),
]))
SPEC['ch04-st3'] = ('writing', dict(tt='speech', tasks=[
    ('अंतरराष्ट्रीय मातृभाषा दिवस पर विद्यालय सभा में आपको ‘मातृभाषा: हमारी जड़ें’ विषय पर भाषण देना है।', ['मातृभाषा और भावनाओं का संबंध', 'मातृभाषा भूलने के ख़तरे', 'हर दिन मातृभाषा को जीवित रखने के उपाय']),
    ('हिंदी दिवस पर अभिभावकों और विद्यार्थियों की संयुक्त सभा में आपको हिंदी के महत्व पर बोलना है।', ['हिंदी का इतिहास और संवैधानिक स्थान', 'आज की पीढ़ी और हिंदी', 'अभिभावकों और विद्यार्थियों से अपील']),
    ('आपके अंतरराष्ट्रीय विद्यालय में बीस देशों के विद्यार्थी हैं। ‘भाषा-मेला’ के उद्घाटन पर आपको बहुभाषिकता पर बोलना है।', ['विद्यालय की भाषाई विविधता', 'कई भाषाएँ सीखने के लाभ', 'मेले की गतिविधियों में भाग लेने का आह्वान']),
    ('ज़िला-स्तरीय वाद-विवाद प्रतियोगिता में विषय है: “अंग्रेज़ी के बिना प्रगति असंभव है।” आपको विपक्ष में बोलना है।', ['विपक्ष का स्पष्ट मत', 'मातृभाषा में शिक्षा पाए सफल लोगों के उदाहरण', 'अंग्रेज़ी का स्थान और संतुलन']),
    ('आपके नगर के पुस्तकालय में हिंदी पुस्तकों का नया खंड खुल रहा है। उद्घाटन समारोह में आपको युवा-प्रतिनिधि के रूप में बोलना है।', ['पढ़ने की आदत और भाषा', 'युवाओं के लिए रोचक हिंदी साहित्य', 'पुस्तकालय से जुड़ने का आह्वान']),
], items=[
    ('C1', 'भाषण के अंत में सबसे उपयुक्त क्या होता है?', 'श्रोताओं से आह्वान और धन्यवाद', ['प्रेषक का पता', 'विषय-पंक्ति', 'संदर्भ-सूची'], 'भाषण श्रोताओं को संबोधित होता है; अंत में आह्वान और धन्यवाद।'),
    ('C1', 'भाषण में ‘साथियो, क्या हम अपनी भाषा को भूल जाने देंगे?’ — यह किस प्रकार का प्रश्न है?', 'अलंकारिक प्रश्न', ['सर्वेक्षण-प्रश्न', 'बहुविकल्पी प्रश्न', 'साक्षात्कार-प्रश्न'], 'अलंकारिक प्रश्न का उत्तर अपेक्षित नहीं; वह श्रोताओं को सोचने पर मजबूर करता है।'),
    ('C2', 'भाषण और लेख में भाषा-प्रयोग का मुख्य अंतर क्या है? दो बिंदुओं में समझाइए।', 'भाषण सुना जाता है, इसलिए उसमें सीधा संबोधन, दोहराव, अलंकारिक प्रश्न और छोटे, प्रभावी वाक्य होते हैं; लेख पढ़ा जाता है, इसलिए उसमें शीर्षक, उपशीर्षक, विस्तृत तर्क और प्रमाण होते हैं।', '1-1 अंक प्रत्येक बिंदु, 1 अंक श्रोता/पाठक से संबंध।', 3),
]))
SPEC['ch04-st4'] = ('none', dict(focus='लेखन में किसी बोली या क्षेत्रीय भाषा का उदाहरण देकर भाषाई विविधता दिखाइए।', gens=[g_dialect], items=[
    ('C1', 'आधुनिक मानक हिंदी किस बोली पर आधारित है?', 'खड़ी बोली', ['ब्रज', 'अवधी', 'भोजपुरी'], 'आधुनिक मानक हिंदी का आधार दिल्ली-मेरठ क्षेत्र की खड़ी बोली है।'),
    ('C1', 'तुलसीदास ने ‘रामचरितमानस’ किस भाषा/बोली में लिखा?', 'अवधी', ['ब्रज', 'खड़ी बोली', 'मैथिली'], 'रामचरितमानस अवधी में है।'),
    ('C1', 'सूरदास के पदों की भाषा कौन-सी है?', 'ब्रज', ['अवधी', 'भोजपुरी', 'हरियाणवी'], 'सूरदास ने ब्रजभाषा में कृष्ण-लीला के पद रचे।'),
    ('C1', 'मॉरीशस, फ़िजी, सूरीनाम और त्रिनिदाद में बसे भारतवंशियों की बोलचाल में प्रायः किस बोली के तत्व मिलते हैं?', 'भोजपुरी', ['ब्रज', 'बुंदेली', 'कुमाऊँनी'], 'उन्नीसवीं सदी में गिरमिटिया मज़दूर अधिकतर पूर्वी उत्तर प्रदेश और बिहार से गए थे।'),
    ('C1', '‘बोली’ और ‘भाषा’ के संबंध के बारे में कौन-सा कथन सही है?', 'बोली का क्षेत्र प्रायः सीमित होता है, जबकि मानक भाषा का प्रयोग शिक्षा, प्रशासन और साहित्य में व्यापक होता है', ['बोली में कभी साहित्य नहीं लिखा जाता', 'बोली भाषा का ग़लत रूप है', 'भाषा और बोली में कोई अंतर नहीं'], 'बोलियाँ भाषा के क्षेत्रीय रूप हैं; ब्रज और अवधी में महान साहित्य रचा गया है।'),
    ('C2', 'यह धारणा क्यों ग़लत है कि “बोलियाँ अशुद्ध हिंदी हैं”? उदाहरण सहित समझाइए।', 'बोलियों की अपनी व्याकरण-व्यवस्था और समृद्ध साहित्यिक परंपरा है — सूरदास (ब्रज), तुलसीदास (अवधी)। वे भाषा के क्षेत्रीय रूप हैं, अशुद्ध रूप नहीं; मानक भाषा भी एक बोली (खड़ी बोली) का विकसित, स्वीकृत रूप है।', '1 अंक ग़लत धारणा की पहचान, 1 अंक व्याकरण/साहित्य का तर्क, 1 अंक उदाहरण।', 3),
    ('C2', 'एक ही भाषा के भीतर क्षेत्रीय विविधता (उच्चारण, शब्द, मुहावरे) किन कारणों से विकसित होती है?', 'भौगोलिक दूरी, स्थानीय संस्कृति और व्यवसाय, पड़ोसी भाषाओं का प्रभाव और ऐतिहासिक प्रवास — इनसे हर क्षेत्र में उच्चारण और शब्दावली अलग विकसित होती है।', '1-1 अंक प्रत्येक सही कारण (अधिकतम 3)।', 3),
    ('C2', 'मानक भाषा की आवश्यकता क्यों होती है, जबकि लोग घर में अलग-अलग बोलियाँ बोलते हैं? समझाइए।', 'मानक भाषा अलग-अलग क्षेत्रों के लोगों के बीच साझा संप्रेषण, शिक्षा, प्रशासन, समाचार और पाठ्य-पुस्तकों के लिए एक समान, सर्वमान्य रूप देती है; बोलियाँ स्थानीय और आत्मीय संप्रेषण के लिए बनी रहती हैं।', '1 अंक साझा संप्रेषण, 1 अंक औपचारिक क्षेत्रों का उदाहरण, 1 अंक बोलियों से संबंध।', 3),
    ('C3', 'आपके परिवार में दादी अवधी, माता-पिता मानक हिंदी और आप हिंग्लिश बोलते हैं। इस स्थिति को ‘भाषा और पहचान’ के संदर्भ में 60–80 शब्दों में समझाइए।', 'तीन पीढ़ियों की भाषा उनके परिवेश और पहचान को दिखाती है: अवधी — क्षेत्रीय जड़ें; मानक हिंदी — शिक्षा और शहरी जीवन; हिंग्लिश — वैश्विक युवा पहचान। भाषाई बदलाव पीढ़ियों के अनुभवों का दर्पण है।', '1 अंक प्रत्येक पीढ़ी की भाषा-पहचान का संबंध, 1 अंक निष्कर्ष।', 4),
    ('C3', 'एक हिंदी फ़िल्म में गाँव का पात्र भोजपुरी बोलता है और शहर का पात्र हिंग्लिश। निर्देशक ने भाषा का यह अंतर क्यों रखा होगा? दो कारण दीजिए।', 'पात्रों की सामाजिक-भौगोलिक पहचान स्पष्ट करने के लिए; यथार्थ और विश्वसनीयता लाने के लिए; गाँव-शहर के सांस्कृतिक अंतर या टकराव को उभारने के लिए।', '1-1 अंक प्रत्येक कारण, 1 अंक भाषा-पहचान संबंध की स्पष्टता।', 3),
    ('C4', '“हर बोली के लुप्त होने के साथ ज्ञान और संस्कृति का एक पूरा संसार लुप्त हो जाता है।” इस कथन की विवेचना कीजिए (120–150 शब्द)।', 'पक्ष: लोकगीत, कहावतें, स्थानीय औषधि और कृषि-ज्ञान बोली में संचित; पहचान और आत्मसम्मान। विपक्ष/जटिलता: रोज़गार और शिक्षा के लिए मानक भाषा की आवश्यकता; अनुवाद और डिजिटल अभिलेख से कुछ ज्ञान बचाया जा सकता है। निष्कर्ष: बहुभाषी नीति और सामुदायिक प्रयास।', 'मत (1), पक्ष के तर्क (2), विपक्ष/जटिलता (2), निष्कर्ष और भाषा (1)।', 6),
    ('C4', 'आपके विद्यालय में प्रस्ताव है कि हर महीने एक दिन ‘बोली दिवस’ मनाया जाए, जिसमें विद्यार्थी अपनी पारिवारिक बोली में कविता या कहानी सुनाएँ। इस प्रस्ताव के लाभ और चुनौतियों का मूल्यांकन कीजिए।', 'लाभ: भाषाई विविधता का सम्मान, हीनभावना में कमी, विरासत का संरक्षण। चुनौतियाँ: समझने में कठिनाई, मज़ाक का डर, समय। सुझाव: अनुवाद सहित प्रस्तुति, सम्मानजनक नियम। स्पष्ट निष्कर्ष।', 'लाभ (2), चुनौतियाँ (2), सुझाव/निष्कर्ष (1), भाषा (1)।', 6),
    ('C4', 'क्या टेलीविज़न और फ़िल्मों में बोलियों का प्रयोग उन्हें लोकप्रिय बनाता है या केवल हास्य का साधन बना देता है? उदाहरण सहित विवेचना कीजिए।', 'लोकप्रियता: भोजपुरी/हरियाणवी गीत और वेब-सीरीज़ से नई पहुँच, गर्व। हास्य/रूढ़ि: बोली बोलने वाले पात्रों को अनपढ़ या हास्यास्पद दिखाना, जिससे हीनभावना बढ़ती है। संतुलित निष्कर्ष: सम्मानजनक, यथार्थ चित्रण की आवश्यकता।', 'दोनों पक्ष (2+2), उदाहरण (1), निष्कर्ष और भाषा (1)।', 6),
]))


# ---------------------------------------------------------------- ch05 अवकाश, छुट्टियाँ और यात्रा
TH[5] = dict(
    name='अवकाश, छुट्टियाँ और यात्रा',
    vocab=[
        ('पर्यटन', 'घूमने-फिरने और नई जगहें देखने के लिए की जाने वाली यात्रा', 'सैर-सपाटा', 'केरल की अर्थव्यवस्था में ____ का बड़ा योगदान है।'),
        ('पर्यटक', 'घूमने के लिए आया हुआ यात्री', 'सैलानी', 'गर्मियों में शिमला की माल रोड ____ से भरी रहती है।'),
        ('दर्शनीय', 'देखने योग्य, सुंदर', 'मनोरम', 'जैसलमेर का सोनार क़िला एक ____ स्थल है।'),
        ('आरक्षण', 'टिकट या कमरा पहले से पक्का करवाना', 'बुकिंग', 'त्योहारों के दिनों में रेल का ____ महीनों पहले करवाना पड़ता है।'),
        ('सामान', 'यात्रा में साथ ले जाई जाने वाली वस्तुएँ', 'असबाब', 'हवाई यात्रा में बीस किलो से अधिक ____ ले जाने पर अतिरिक्त शुल्क लगता है।'),
        ('मार्गदर्शक', 'पर्यटकों को स्थान दिखाने और जानकारी देने वाला व्यक्ति', 'गाइड', 'हमारे ____ ने ताजमहल के निर्माण की रोचक कहानी सुनाई।'),
        ('रोमांच', 'साहसिक काम से मिलने वाला उत्साह', 'साहसिकता', 'ऋषिकेश में रिवर-राफ़्टिंग का ____ मैं कभी नहीं भूलूँगा।'),
        ('तीर्थ', 'धार्मिक महत्व का पवित्र स्थान', 'तीर्थस्थल', 'वाराणसी हिंदुओं का एक प्राचीन ____ है।'),
        ('अवकाश', 'काम या पढ़ाई से छुट्टी का समय', 'छुट्टी', 'दिवाली के ____ में हम राजस्थान घूमने गए।'),
        ('यात्रा-वृत्तांत', 'किसी यात्रा का क्रमबद्ध, अनुभवपरक वर्णन', 'सफ़रनामा', 'राहुल सांकृत्यायन ने तिब्बत की यात्राओं पर प्रसिद्ध ____ लिखे।'),
        ('स्मृति-चिह्न', 'यात्रा की याद के रूप में ख़रीदी गई वस्तु', 'यादगार', 'मैंने कच्छ से ____ के रूप में कढ़ाई वाला थैला ख़रीदा।'),
        ('भीड़-भाड़', 'बहुत अधिक लोगों का जमावड़ा', 'जमघट', 'छुट्टियों में पहाड़ों पर इतनी ____ होती है कि सड़कें जाम हो जाती हैं।'),
        ('आतिथ्य', 'मेहमानों का आदर-सत्कार', 'मेहमाननवाज़ी', 'राजस्थान के गाँवों का ____ पर्यटकों का दिल जीत लेता है।'),
        ('पारिस्थितिक पर्यटन', 'प्रकृति को नुक़सान पहुँचाए बिना की जाने वाली ज़िम्मेदार यात्रा', 'इको-टूरिज़्म', 'सिक्किम ____ को बढ़ावा देता है, जहाँ पर्यटक प्लास्टिक नहीं ले जा सकते।'),
    ],
    topics=['मेरी सबसे यादगार यात्रा', 'ज़िम्मेदार पर्यटन', 'छुट्टियाँ: घर पर या घूमने?', 'पहाड़ों की सैर', 'स्थानीय त्योहार देखने की यात्रा',
            'अकेले यात्रा करने के अनुभव', 'शौक़ और अवकाश की गतिविधियाँ'],
    texts=[
        dict(kind='विज्ञापन', title='चलो कच्छ! — रण उत्सव में आपका स्वागत है',
             body='सफ़ेद रेगिस्तान पर चाँदनी रात, लोक-संगीत की धुन और ऊँट-सफ़ारी का रोमांच! गुजरात पर्यटन आपको आमंत्रित करता है ‘रण उत्सव’ में — नवंबर से फ़रवरी तक। आरामदायक टेंट, स्थानीय व्यंजन और हस्तशिल्प-बाज़ार। परिवार-पैकेज पर बीस प्रतिशत छूट, बशर्ते आरक्षण तीस दिन पहले हो। प्लास्टिक-मुक्त उत्सव — कृपया अपनी पानी की बोतल साथ लाएँ। आज ही बुक करें!',
             qs=[('C1', 'रण उत्सव किन महीनों में होता है?', 'नवंबर से फ़रवरी तक', ['जून से अगस्त तक', 'केवल दिसंबर में', 'मार्च से मई तक']),
                 ('C1', 'परिवार-पैकेज पर छूट पाने की शर्त क्या है?', 'आरक्षण तीस दिन पहले करना'),
                 ('C2', '“सफ़ेद रेगिस्तान पर चाँदनी रात” — विज्ञापन की शुरुआत ऐसे दृश्य-वर्णन से क्यों की गई है?', 'पाठक के मन में सुंदर, अनोखा दृश्य जगाकर उसकी कल्पना और जिज्ञासा को आकर्षित करने के लिए, ताकि वह यात्रा करने को प्रेरित हो।'),
                 ('tf', 'उत्सव में पर्यटक प्लास्टिक की बोतलें ख़रीद सकते हैं।', 'गलत', '“प्लास्टिक-मुक्त उत्सव — कृपया अपनी पानी की बोतल साथ लाएँ।”'),
                 ('C3', 'विज्ञापन किस प्रकार के पर्यटकों को विशेष रूप से लक्ष्य करता है? दो प्रमाण दीजिए।', 'परिवारों और संस्कृति/रोमांच पसंद पर्यटकों को — ‘परिवार-पैकेज पर बीस प्रतिशत छूट’, ‘लोक-संगीत’, ‘ऊँट-सफ़ारी का रोमांच’, ‘हस्तशिल्प-बाज़ार’।'),
                 ('C3', '“आज ही बुक करें!” — यह वाक्य विज्ञापन में क्या भूमिका निभाता है?', 'पाठक को तुरंत कार्य करने के लिए प्रेरित करने वाला आह्वान', ['उत्सव का इतिहास बताना', 'छूट की शर्त समझाना', 'स्थानीय व्यंजनों का वर्णन करना']),
                 ('C4', 'क्या यह विज्ञापन ‘ज़िम्मेदार पर्यटन’ को भी बढ़ावा देता है? विज्ञापन के तत्वों के आधार पर मूल्यांकन कीजिए।', 'हाँ: प्लास्टिक-मुक्त उत्सव, अपनी बोतल लाने का अनुरोध, स्थानीय हस्तशिल्प और व्यंजन से स्थानीय लोगों को आय। सीमा: भीड़, रेगिस्तान के पारिस्थितिकी-तंत्र पर दबाव, टेंट-निर्माण का प्रभाव — इनका उल्लेख नहीं। संतुलित निष्कर्ष।')]),
        dict(kind='यात्रा-वृत्तांत', title='लद्दाख की डायरी से: बादलों के पार',
             body='लेह पहुँचते ही ड्राइवर ताशी ने हिदायत दी, “पहले दो दिन आराम कीजिए, यहाँ हवा पतली है।” सचमुच, होटल की सीढ़ियाँ चढ़ते ही साँस फूल गई। तीसरे दिन हम खारदुंग ला की ओर चले। रास्ते में बर्फ़ से ढकी चोटियाँ धूप में चाँदी-सी चमक रही थीं और नीचे सिंधु नदी फ़िरोज़ी रिबन की तरह लहरा रही थी। एक छोटे गाँव में एक बुज़ुर्ग अम्मा ने हमें नमकीन मक्खन-चाय पिलाई। उनकी मुस्कान ठंडी हवा में भी गरमाहट भर गई।',
             qs=[('C1', 'ताशी ने पर्यटकों को पहले दो दिन क्या करने की सलाह दी?', 'आराम करने की', ['तुरंत खारदुंग ला जाने की', 'सिंधु नदी में तैरने की', 'बाज़ार में ख़रीदारी करने की']),
                 ('C1', 'बुज़ुर्ग अम्मा ने पर्यटकों को क्या पिलाया?', 'नमकीन मक्खन-चाय'),
                 ('C2', 'ताशी ने “यहाँ हवा पतली है” क्यों कहा? पाठ के आधार पर समझाइए।', 'ऊँचाई पर हवा में ऑक्सीजन कम होती है; इसलिए शरीर को अभ्यस्त होने के लिए आराम ज़रूरी है — लेखक की साँस सीढ़ियाँ चढ़ते ही फूल गई।'),
                 ('tf', 'लेखक को होटल की सीढ़ियाँ चढ़ने में कोई कठिनाई नहीं हुई।', 'गलत', '“होटल की सीढ़ियाँ चढ़ते ही साँस फूल गई।”'),
                 ('C3', '“सिंधु नदी फ़िरोज़ी रिबन की तरह लहरा रही थी” — इस उपमा का प्रभाव क्या है?', 'ऊँचाई से दिखती नदी का रंग, पतलापन और बहाव आँखों के सामने जीवंत हो उठता है', ['यह बताती है कि नदी में बाढ़ आई थी', 'यह नदी की लंबाई का सटीक माप देती है', 'यह बताती है कि नदी सूख गई थी']),
                 ('C3', 'इस अंश में यात्रा-वृत्तांत की दो विशेषताएँ पहचानिए और उदाहरण दीजिए।', 'संवेदी और चित्रात्मक वर्णन (‘चाँदी-सी चमक’, ‘फ़िरोज़ी रिबन’); निजी अनुभव (‘साँस फूल गई’); स्थानीय लोगों से मुलाक़ात (ताशी, बुज़ुर्ग अम्मा); घटनाओं का क्रम (पहुँचना → आराम → खारदुंग ला)।'),
                 ('C4', '“यात्रा का सबसे यादगार हिस्सा स्थान नहीं, लोग होते हैं।” — इस अंश और अपने अनुभव के आधार पर इस कथन पर विचार कीजिए।', 'अंश का प्रमाण: अम्मा की मुस्कान ने ‘गरमाहट’ भरी, ताशी की देखभाल। विपक्ष: प्राकृतिक दृश्य (चोटियाँ, नदी) भी गहरी छाप छोड़ते हैं। निजी उदाहरण और संतुलित निष्कर्ष।')]),
        dict(kind='लेख', title='‘ओवर-टूरिज़्म’: जब सैलानी ही बोझ बन जाएँ',
             body='मनाली में पिछली गर्मियों में एक ही दिन में चालीस हज़ार गाड़ियाँ पहुँचीं और सड़कें घंटों जाम रहीं। वेनिस से लेकर हिमालय तक कई पर्यटन-स्थल ‘ओवर-टूरिज़्म’ यानी ज़रूरत से ज़्यादा पर्यटन की समस्या झेल रहे हैं। इससे कूड़ा, पानी की कमी और स्थानीय लोगों के लिए महँगाई बढ़ती है। विशेषज्ञ सुझाते हैं कि पर्यटक भीड़ वाले मौसम के बजाय ‘ऑफ़-सीज़न’ में यात्रा करें, स्थानीय होमस्टे में रुकें और कम-प्रसिद्ध जगहों को भी चुनें।',
             qs=[('C1', 'पिछली गर्मियों में एक दिन में कितनी गाड़ियाँ मनाली पहुँचीं?', 'चालीस हज़ार', ['चार हज़ार', 'चार लाख', 'चौदह हज़ार']),
                 ('C1', 'पाठ में ‘ओवर-टूरिज़्म’ का हिंदी अर्थ क्या बताया गया है?', 'ज़रूरत से ज़्यादा पर्यटन'),
                 ('C2', 'ओवर-टूरिज़्म से स्थानीय लोगों को कौन-सी समस्याएँ होती हैं? अपने शब्दों में लिखिए।', 'कूड़े का ढेर, पानी की कमी और चीज़ों के दाम बढ़ने से स्थानीय लोगों का रोज़मर्रा का जीवन कठिन और महँगा हो जाता है।'),
                 ('tf', 'विशेषज्ञ पर्यटकों को सबसे भीड़ वाले मौसम में यात्रा करने की सलाह देते हैं।', 'गलत', '“भीड़ वाले मौसम के बजाय ‘ऑफ़-सीज़न’ में यात्रा करें।”'),
                 ('C3', 'लेखक ने मनाली के साथ वेनिस का उल्लेख क्यों किया है?', 'यह दिखाने के लिए कि यह समस्या केवल भारत की नहीं, बल्कि वैश्विक है', ['वेनिस की सुंदरता की प्रशंसा करने के लिए', 'यह बताने के लिए कि वेनिस में जाम नहीं लगता', 'पर्यटकों को वेनिस भेजने के लिए']),
                 ('C3', 'विशेषज्ञों के तीन सुझावों में से कौन-सा सुझाव स्थानीय लोगों की आय बढ़ाने में सबसे सीधे सहायक होगा और क्यों?', 'स्थानीय होमस्टे में रुकना — इससे पैसा सीधे स्थानीय परिवारों तक पहुँचता है, बड़े होटल-समूहों तक नहीं।'),
                 ('C4', 'क्या पर्यटन-स्थलों पर पर्यटकों की संख्या सीमित करने के लिए शुल्क या परमिट लगाना उचित है? लेख के आधार पर तर्क दीजिए।', 'पक्ष: पर्यावरण और स्थानीय संसाधनों की रक्षा, भीड़ प्रबंधन (मनाली का उदाहरण)। विपक्ष: कम आय वाले यात्रियों के साथ अन्याय, स्थानीय व्यापार पर असर। निष्कर्ष: परमिट के साथ ऑफ़-सीज़न प्रोत्साहन और कम-प्रसिद्ध स्थलों का प्रचार।')]),
    ],
    tasks=[
        ('आप हाल ही में परिवार के साथ किसी पहाड़ी स्थान की यात्रा से लौटे हैं। विद्यालय-पत्रिका ने यात्रा-अनुभव आमंत्रित किए हैं।', 'travelogue',
         ['यात्रा का क्रम और प्रमुख स्थान', 'स्थानीय लोगों और संस्कृति से मुलाक़ात', 'यात्रा से मिली सीख']),
        ('आपकी कक्षा ‘ज़िम्मेदार पर्यटन’ पर अभियान चला रही है। आपको युवा पर्यटकों के लिए एक ब्लॉग प्रविष्टि लिखनी है।', 'blog',
         ['ओवर-टूरिज़्म की समस्या', 'यात्रा के दौरान ज़िम्मेदार व्यवहार', 'आपका निजी अनुभव या संकल्प']),
        ('आपने एक होटल में कमरा आरक्षित कराया था, पर वहाँ पहुँचने पर पता चला कि आरक्षण रद्द हो गया है।', 'email',
         ['आरक्षण का विवरण', 'आपको हुई असुविधा', 'आप क्या समाधान या मुआवज़ा चाहते हैं']),
        ('आपके शहर में एक नया साहसिक खेल केंद्र खुला है। आप उसके लिए युवाओं को आकर्षित करने वाला विज्ञापन बनाना चाहते हैं।', 'advert',
         ['उपलब्ध गतिविधियाँ', 'सुरक्षा और प्रशिक्षकों की जानकारी', 'छूट और संपर्क']),
        ('आपका एक विदेशी मित्र अगली सर्दियों में भारत आना चाहता है और पूछ रहा है कि उसे कहाँ जाना चाहिए।', 'pletter',
         ['दो-तीन सुझाए गए स्थान और कारण', 'मौसम, भोजन और यात्रा की व्यावहारिक सलाह', 'आप उसके साथ क्या करना चाहेंगे']),
        ('आपने विद्यालय की शैक्षिक यात्रा में पहली बार किसी गाँव में होमस्टे में रात बिताई।', 'diary',
         ['दिन की घटनाएँ', 'मेज़बान परिवार का व्यवहार और आपका अनुभव', 'शहर के जीवन से तुलना पर आपके विचार']),
    ],
    discuss=[
        ('क्या आज यात्रा अनुभव के लिए कम और सोशल मीडिया पर तस्वीरें डालने के लिए ज़्यादा की जाती है?', ['इंस्टाग्राम-योग्य स्थलों की होड़', 'तस्वीरें यादें सहेजती हैं और दूसरों को प्रेरित करती हैं', 'सचेत यात्रा का महत्व']),
        ('क्या विद्यार्थियों के लिए शैक्षिक यात्राएँ कक्षा की पढ़ाई से अधिक सिखाती हैं?', ['प्रत्यक्ष अनुभव और जिज्ञासा', 'ख़र्च और सुरक्षा की चिंता', 'यात्रा और पाठ्यक्रम का संबंध']),
        ('घरेलू पर्यटन या विदेश यात्रा — युवाओं को पहले क्या चुनना चाहिए?', ['अपने देश की विविधता को जानना', 'विदेश में नई संस्कृति और भाषा का अनुभव', 'बजट और उद्देश्य पर निर्भर']),
        ('क्या धार्मिक तीर्थस्थलों का व्यवसायीकरण उचित है?', ['स्थानीय रोज़गार और सुविधाएँ', 'आस्था और शांति पर असर', 'नियंत्रित विकास और स्वच्छता']),
        ('क्या छुट्टियों में भी विद्यार्थियों को कोचिंग और गृहकार्य से मुक्त रहना चाहिए?', ['आराम, रचनात्मकता और परिवार का समय', 'प्रतिस्पर्धा और पढ़ाई की निरंतरता', 'संतुलित छुट्टी-योजना']),
    ],
    pics=[('एक हिल-स्टेशन की सड़क पर गाड़ियों की लंबी कतार है; किनारे प्लास्टिक की बोतलों का ढेर है और कुछ पर्यटक बंदरों को चिप्स खिला रहे हैं।',
           ['ओवर-टूरिज़्म और जाम', 'प्रदूषण और वन्यजीवों पर असर', 'ज़िम्मेदार पर्यटन की आवश्यकता']),
          ('एक रेलवे स्टेशन पर एक परिवार भारी सूटकेस लिए खड़ा है; बच्चा खिड़की से बाहर झाँक रहा है और दादी हाथ में खाने का टिफ़िन लिए हैं।',
           ['रेल-यात्रा की भारतीय संस्कृति', 'परिवार के साथ छुट्टियाँ', 'यात्रा की तैयारी और उत्साह'])],
)

ADJADV = [
    ('हम धीरे-धीरे पहाड़ की चोटी की ओर बढ़े।', 'धीरे-धीरे', 'रीतिवाचक क्रिया-विशेषण'),
    ('कल हम ऋषिकेश पहुँचे।', 'कल', 'कालवाचक क्रिया-विशेषण'),
    ('बच्चे बाहर बर्फ़ में खेल रहे थे।', 'बाहर', 'स्थानवाचक क्रिया-विशेषण'),
    ('रास्ता इतना कठिन था कि हम थोड़ा ही चल पाए।', 'थोड़ा', 'परिमाणवाचक क्रिया-विशेषण'),
    ('झील का पानी नीला और साफ़ था।', 'नीला', 'गुणवाचक विशेषण'),
    ('हमने तीन मंदिर देखे।', 'तीन', 'संख्यावाचक विशेषण'),
    ('मुझे दो लीटर पानी चाहिए।', 'दो लीटर', 'परिमाणवाचक विशेषण'),
    ('वह होटल बहुत महँगा था।', 'वह', 'सार्वनामिक विशेषण'),
    ('गाइड ने हमें प्राचीन क़िले का इतिहास बताया।', 'प्राचीन', 'गुणवाचक विशेषण'),
    ('ट्रेन अचानक रुक गई।', 'अचानक', 'रीतिवाचक क्रिया-विशेषण'),
    ('हम प्रतिवर्ष गर्मियों में नानी के गाँव जाते हैं।', 'प्रतिवर्ष', 'कालवाचक क्रिया-विशेषण'),
    ('यहाँ से समुद्र साफ़ दिखाई देता है।', 'यहाँ', 'स्थानवाचक क्रिया-विशेषण'),
    ('बाज़ार में कुछ पर्यटक मोलभाव कर रहे थे।', 'कुछ', 'संख्यावाचक विशेषण'),
    ('थाली में थोड़ी खिचड़ी बची थी।', 'थोड़ी', 'परिमाणवाचक विशेषण'),
    ('हम ऊपर छत पर बैठकर सूर्यास्त देखते रहे।', 'ऊपर', 'स्थानवाचक क्रिया-विशेषण'),
    ('उस गाँव के लोग बड़े मिलनसार थे।', 'मिलनसार', 'गुणवाचक विशेषण'),
    ('यात्रा के बाद मैं बहुत थक गया।', 'बहुत', 'परिमाणवाचक क्रिया-विशेषण'),
    ('यह रास्ता झरने तक जाता है।', 'यह', 'सार्वनामिक विशेषण'),
]
ADJ_CATS = ['रीतिवाचक क्रिया-विशेषण', 'कालवाचक क्रिया-विशेषण', 'स्थानवाचक क्रिया-विशेषण', 'परिमाणवाचक क्रिया-विशेषण',
            'गुणवाचक विशेषण', 'संख्यावाचक विशेषण', 'परिमाणवाचक विशेषण', 'सार्वनामिक विशेषण']
ENRICH = [
    ('हम झील पर गए।', 'सुबह-सुबह हम शांत, नीली झील पर धीरे-धीरे टहलने गए।'),
    ('बाज़ार में भीड़ थी।', 'शाम को रंग-बिरंगे बाज़ार में बहुत भारी भीड़ थी।'),
    ('बर्फ़ गिर रही थी।', 'रात भर चुपचाप सफ़ेद, रुई-सी बर्फ़ गिर रही थी।'),
    ('हमने खाना खाया।', 'ढाबे पर हमने गरमागरम, स्वादिष्ट खाना जी भरकर खाया।'),
    ('बस चल पड़ी।', 'टूटी-फूटी पुरानी बस अचानक झटके से चल पड़ी।'),
    ('लहरें किनारे से टकराईं।', 'ऊँची, झागदार लहरें बार-बार ज़ोर से किनारे से टकराईं।'),
    ('मंदिर में घंटियाँ बजीं।', 'प्राचीन पत्थर के मंदिर में सुबह-सवेरे मधुर घंटियाँ लगातार बजीं।'),
    ('हम पहाड़ पर चढ़े।', 'हम हाँफते हुए, धीरे-धीरे उस खड़ी, पथरीली पहाड़ी पर ऊपर चढ़े।'),
    ('बच्चे हँसे।', 'नन्हे, शरारती बच्चे खिलखिलाकर ज़ोर से हँसे।'),
    ('सूरज डूबा।', 'नारंगी सूरज धीरे-धीरे दूर रेत के टीलों के पीछे डूब गया।'),
]


def g_adjadv(kit, key, th):
    def ident(rng, slot):
        s, w, c = rng.choice(ADJADV)
        return mcq(rng, f'वाक्य में ‘{w}’ शब्द किस प्रकार का है?\n“{s}”', c, rng.sample([x for x in ADJ_CATS if x != c], 3),
                   f'‘{w}’ — {c}। विशेषण संज्ञा/सर्वनाम की विशेषता बताता है, क्रिया-विशेषण क्रिया की।')
    kit.add(key, ('C1', 'C2'), (1, 3), ident, 'mcq', None, 'adj_id')

    def find(rng, slot):
        s, w, c = rng.choice(ADJADV)
        kind = 'क्रिया-विशेषण' if 'क्रिया' in c else 'विशेषण'
        return dict(stem=f'इस वाक्य से {kind} छाँटिए और उसका भेद बताइए:\n“{s}”', answer=f'{w} — {c}', type='short', marks=2,
                    markingKey=f'1 अंक सही शब्द ‘{w}’ के लिए, 1 अंक सही भेद ({c}) के लिए।')
    kit.add(key, ('C1', 'C2', 'C3'), (1, 3), find, 'short', None, 'adj_find')

    def enrich(rng, slot):
        a, b = rng.choice(ENRICH)
        fr = rng.choice(['इस सादे वाक्य में कम से कम दो विशेषण और एक क्रिया-विशेषण जोड़कर इसे यात्रा-वृत्तांत के लिए अधिक सजीव बनाइए:\n“{a}”',
                         'आपकी डायरी में यह वाक्य बहुत फीका लग रहा है: “{a}” — रंग, आकार, समय या ढंग बताने वाले शब्द जोड़कर इसे चित्रात्मक बनाइए (कम से कम तीन नए शब्द)।',
                         '“{a}” — यात्रा-पत्रिका के संपादक ने कहा है कि यह वाक्य पाठक की आँखों के सामने दृश्य नहीं खींचता। विशेषणों और क्रिया-विशेषणों की सहायता से इसे फिर से लिखिए और जोड़े गए शब्दों के भेद बताइए।'])
        return dict(stem=fr.format(a=a),
                    answer=f'नमूना: {b}', type='short', marks=3,
                    markingKey='1 अंक प्रत्येक उपयुक्त विशेषण (अधिकतम 2), 1 अंक उपयुक्त क्रिया-विशेषण; अर्थ स्वाभाविक और व्याकरण शुद्ध हो।')
    kit.add(key, 'C3', (1, 4), enrich, 'short', None, 'adj_enrich')

    def descr(rng, slot):
        topic = rng.choice(th['topics'])
        cats = rng.sample(ADJ_CATS, 3)
        return dict(stem=f'‘{topic}’ विषय पर 100–120 शब्दों का वर्णनात्मक अनुच्छेद लिखिए। उसमें {", ".join(cats)} — तीनों का कम से कम एक-एक उदाहरण हो और उन्हें रेखांकित कीजिए।',
                    answer=f'अपेक्षित: संवेदी और चित्रात्मक वर्णन; {", ".join(cats)} के सही उदाहरण; विषय पर केंद्रित, सुसंगत अनुच्छेद।', type='long', marks=6,
                    markingKey=para_key(6, 'तीनों भेदों के सही उदाहरण अनिवार्य; केवल सूची देने पर भाषा के अंक नहीं।'))
    kit.add(key, 'C4', (2, 5), descr, 'long', None, 'adj_descr')


SPEC['ch05-st1'] = ('vocab', dict(focus='लेखन में यात्रा और पर्यटन से जुड़ी विविध शब्दावली (जैसे आरक्षण, आतिथ्य, पारिस्थितिक पर्यटन) का सटीक प्रयोग कीजिए।', items=[
    ('C1', '‘पर्यटक’ और ‘तीर्थयात्री’ में मुख्य अंतर क्या है?', 'तीर्थयात्री धार्मिक उद्देश्य से यात्रा करता है', ['पर्यटक कभी विदेश नहीं जाता', 'तीर्थयात्री केवल हवाई जहाज़ से जाता है', 'दोनों में कोई अंतर नहीं'], 'तीर्थयात्रा का उद्देश्य धार्मिक होता है; पर्यटन घूमने-देखने के लिए।'),
    ('C1', '‘सैलानी’ शब्द का सबसे उपयुक्त पर्यायवाची कौन-सा है?', 'पर्यटक', ['मेज़बान', 'तीर्थ', 'मार्ग'], '‘सैलानी’ = सैर करने वाला = पर्यटक।'),
    ('C2', '‘पर्यटन’ और ‘पारिस्थितिक पर्यटन’ में अंतर स्पष्ट कीजिए।', 'पर्यटन सामान्य रूप से घूमने-फिरने की यात्रा है; पारिस्थितिक पर्यटन ऐसी ज़िम्मेदार यात्रा है जो प्रकृति और स्थानीय समुदाय को नुक़सान पहुँचाए बिना, संरक्षण को ध्यान में रखकर की जाती है।', '1 अंक प्रत्येक अर्थ, 1 अंक अंतर/उदाहरण।', 3),
    ('C3', 'इन शब्दों को यात्रा के क्रम में सजाइए: स्मृति-चिह्न ख़रीदना, आरक्षण, सामान बाँधना, मार्गदर्शक के साथ भ्रमण।', 'आरक्षण → सामान बाँधना → मार्गदर्शक के साथ भ्रमण → स्मृति-चिह्न ख़रीदना', '2 अंक: पूर्ण सही क्रम; एक स्थान की गलती पर 1 अंक।', 2),
]))
SPEC['ch05-st2'] = ('writing', dict(tt='travelogue', tasks=[
    ('आपने हाल ही में अपने दादा-दादी के गाँव की यात्रा की। आप इस यात्रा का वृत्तांत विद्यालय-पत्रिका के लिए लिखना चाहते हैं।', ['गाँव तक पहुँचने का रास्ता और पहला दृश्य', 'गाँव की दिनचर्या, भोजन और लोग', 'शहर लौटते समय आपकी भावनाएँ']),
    ('आपने किसी ऐतिहासिक नगर (जैसे हम्पी, जयपुर या खजुराहो) की यात्रा की। एक यात्रा-पत्रिका ने युवा लेखकों से वृत्तांत माँगे हैं।', ['नगर का इतिहास और दर्शनीय स्थल', 'संवेदी विवरण और रोचक घटना', 'अन्य युवाओं के लिए सुझाव']),
    ('आपने पहली बार अकेले रेल-यात्रा की, जो चौबीस घंटे लंबी थी। इस अनुभव पर यात्रा-वृत्तांत लिखिए।', ['यात्रा की तैयारी और घबराहट', 'सहयात्रियों से बातचीत', 'आत्मनिर्भरता के बारे में सीख']),
    ('आपने समुद्र-तट पर स्वच्छता-अभियान के साथ एक सप्ताह की स्वयंसेवी यात्रा की।', ['तट का दृश्य और समस्या', 'अभियान की गतिविधियाँ और साथी', 'इस यात्रा ने आपके पर्यटन के प्रति दृष्टिकोण को कैसे बदला']),
    ('आप परिवार के साथ एक पहाड़ी ट्रेक पर गए, जहाँ ख़राब मौसम के कारण योजना बदलनी पड़ी।', ['ट्रेक की योजना और शुरुआत', 'मौसम बिगड़ने की घटना', 'परिवार ने कठिनाई का सामना कैसे किया']),
], items=[
    ('C1', 'यात्रा-वृत्तांत और यात्रा-विज्ञापन में मुख्य अंतर क्या है?', 'वृत्तांत लेखक के निजी अनुभव का वर्णन है, विज्ञापन यात्रा बेचने के लिए प्रेरित करता है', ['वृत्तांत में कभी स्थानों के नाम नहीं होते', 'विज्ञापन हमेशा भूतकाल में होता है', 'दोनों का उद्देश्य एक ही है'], 'उद्देश्य का अंतर: अनुभव साझा करना बनाम बिक्री।'),
    ('C2', 'यात्रा-वृत्तांत प्रायः भूतकाल में क्यों लिखा जाता है, फिर भी कुछ लेखक बीच-बीच में वर्तमान काल का प्रयोग क्यों करते हैं?', 'यात्रा बीत चुकी होती है, इसलिए भूतकाल स्वाभाविक है; पर किसी नाटकीय क्षण को जीवंत बनाने के लिए लेखक वर्तमान काल (“अचानक बादल घिर आते हैं…”) का प्रयोग करते हैं, ताकि पाठक को लगे कि घटना अभी घट रही है।', '1 अंक भूतकाल का कारण, 2 अंक वर्तमान काल के प्रभाव की व्याख्या।', 3),
    ('C2', 'डायरी प्रविष्टि और यात्रा-वृत्तांत दोनों में यात्रा का वर्णन हो सकता है। दोनों के पाठक और भाषा में क्या अंतर होगा?', 'डायरी का पाठक स्वयं लेखक है, इसलिए भाषा निजी, भावनात्मक और अनौपचारिक; यात्रा-वृत्तांत सार्वजनिक पाठकों के लिए है, इसलिए उसमें क्रमबद्ध, चित्रात्मक वर्णन, स्थानों की जानकारी और पाठकों के लिए सुझाव होते हैं।', '1 अंक पाठक का अंतर, 2 अंक भाषा/प्रारूप का अंतर।', 3),
], gens=[lambda kit, key, th: kit.writing(key, th, 'diary', [
    ('आज आपकी स्कूल-यात्रा का पहला दिन था और आप पहली बार परिवार से दूर एक शिविर में हैं।', ['दिन भर की गतिविधियाँ', 'नए दोस्तों के बारे में भावनाएँ', 'घर की याद और कल की योजना']),
    ('आज यात्रा में आपका बटुआ खो गया, पर एक अजनबी ने उसे लौटा दिया।', ['घटना का क्रम', 'उस समय की घबराहट और राहत', 'अजनबी की ईमानदारी पर आपके विचार']),
    ('छुट्टियों के आख़िरी दिन आप अपने चचेरे भाई-बहनों से विदा ले रहे हैं।', ['छुट्टियों की सबसे अच्छी यादें', 'विदा लेते समय की भावनाएँ', 'अगली छुट्टियों के लिए संकल्प']),
    ('आज आपने पहली बार समुद्र देखा।', ['पहली झलक का अनुभव', 'दिन भर की गतिविधियाँ', 'इस अनुभव का आपके लिए अर्थ']),
])]))
SPEC['ch05-st3'] = ('reading', dict(focus='लेखन में पर्यटन-विज्ञापन और मार्गदर्शिका की भाषा की विशेषताएँ दिखाइए।', items=[
    ('C1', 'पर्यटन-विज्ञापनों में ‘स्वर्ग’, ‘अद्भुत’, ‘अविस्मरणीय’ जैसे शब्दों का प्रयोग क्यों होता है?', 'पाठक की भावनाओं को छूकर यात्रा के लिए आकर्षित करने के लिए', ['तथ्यात्मक जानकारी देने के लिए', 'स्थान की आलोचना करने के लिए', 'मूल्य बताने के लिए'], 'ये अतिशयोक्तिपूर्ण, भावनात्मक विशेषण प्रेरक भाषा के उदाहरण हैं।'),
    ('C1', 'यात्रा-मार्गदर्शिका (गाइडबुक) में सबसे अधिक किस प्रकार की जानकारी होती है?', 'व्यावहारिक जानकारी — पहुँचने का रास्ता, समय, शुल्क और ठहरने के विकल्प', ['लेखक की निजी भावनाएँ', 'काल्पनिक कहानियाँ', 'केवल विज्ञापन के नारे'], 'मार्गदर्शिका का उद्देश्य यात्री की व्यावहारिक सहायता है।'),
    ('C2', 'पर्यटन-विज्ञापन को पढ़ते समय पाठक को किन बातों के प्रति सतर्क रहना चाहिए? दो उदाहरण दीजिए।', 'अतिशयोक्ति (‘धरती का स्वर्ग’) और शर्तों के छोटे अक्षरों (‘बशर्ते आरक्षण तीस दिन पहले हो’) के प्रति; छिपे शुल्क और भीड़ जैसी बातें जिनका उल्लेख नहीं होता।', '1-1 अंक प्रत्येक उचित सावधानी, उदाहरण सहित।'),
]))
SPEC['ch05-st4'] = ('grammar', dict(focus='लेखन में विशेषणों और क्रिया-विशेषणों से वर्णन को सजीव और चित्रात्मक बनाइए।', gens=[g_adjadv], items=[
    ('C1', 'विशेषण किसकी विशेषता बताता है?', 'संज्ञा या सर्वनाम की', ['क्रिया की', 'केवल दूसरे विशेषण की', 'संयोजक की'], 'विशेषण संज्ञा/सर्वनाम की विशेषता बताता है (नीली झील)।'),
    ('C1', 'क्रिया-विशेषण किसकी विशेषता बताता है?', 'क्रिया की', ['संज्ञा की', 'सर्वनाम की', 'केवल संख्या की'], 'क्रिया-विशेषण बताता है कि क्रिया कैसे, कब, कहाँ या कितनी हुई (धीरे चलना)।'),
    ('C2', '‘बहुत’ शब्द कभी विशेषण होता है और कभी क्रिया-विशेषण। दो वाक्यों से स्पष्ट कीजिए।', '“नदी में बहुत पानी है।” — ‘बहुत’ संज्ञा ‘पानी’ की मात्रा बताता है: परिमाणवाचक विशेषण। “वह बहुत तेज़ दौड़ा।” — ‘बहुत’ क्रिया-विशेषण ‘तेज़’ की विशेषता बताता है: परिमाणवाचक क्रिया-विशेषण।', '1-1 अंक प्रत्येक सही वाक्य और पहचान, 1 अंक नियम की स्पष्टता।', 3),
    ('C2', 'यात्रा-वृत्तांत में विशेषणों और क्रिया-विशेषणों का प्रयोग मानदंड A और B, दोनों में कैसे सहायक है?', 'मानदंड A: विविध और सटीक शब्दावली दिखती है; मानदंड B: संवेदी, जीवंत वर्णन से संदेश प्रभावी और पाठक के लिए रोचक बनता है।', '1-1 अंक प्रत्येक मानदंड से सही संबंध।'),
]))

# ---------------------------------------------------------------- ch06 जीवन-गाथाएँ
TH[6] = dict(
    name='जीवन-गाथाएँ',
    vocab=[
        ('आत्मकथा', 'किसी व्यक्ति द्वारा स्वयं लिखी गई अपने जीवन की कहानी', 'स्वजीवनी', 'गांधीजी की ____ ‘सत्य के प्रयोग’ विश्व भर में पढ़ी जाती है।'),
        ('जीवनी', 'किसी व्यक्ति के जीवन का दूसरे व्यक्ति द्वारा लिखा गया वर्णन', 'जीवन-चरित', 'इतिहासकार ने एक प्रसिद्ध वैज्ञानिक की ____ लिखने में पाँच वर्ष लगाए।'),
        ('संघर्ष', 'कठिनाइयों से जूझना', 'जद्दोजहद', 'बचपन की ग़रीबी से निकलकर डॉक्टर बनने तक उसका ____ प्रेरणादायक है।'),
        ('प्रेरणा', 'कुछ करने के लिए मिलने वाला उत्साह', 'उत्प्रेरण', 'माँ की मेहनत ही मेरी सबसे बड़ी ____ है।'),
        ('उपलब्धि', 'मेहनत से प्राप्त की गई सफलता', 'कामयाबी', 'ओलंपिक पदक जीतना उसके जीवन की सबसे बड़ी ____ थी।'),
        ('दृढ़ संकल्प', 'किसी लक्ष्य को पाने का पक्का इरादा', 'अटल निश्चय', 'चोट के बावजूद ____ के बल पर वह फिर मैदान में लौटी।'),
        ('विपरीत परिस्थितियाँ', 'कठिन और प्रतिकूल हालात', 'प्रतिकूलताएँ', 'उसने ____ में भी पढ़ाई नहीं छोड़ी।'),
        ('संस्मरण', 'किसी व्यक्ति या घटना की यादों पर आधारित रचना', 'याद-लेख', 'लेखिका ने अपने शिक्षक पर एक मार्मिक ____ लिखा।'),
        ('आदर्श', 'वह व्यक्ति जिसका अनुसरण किया जाए', 'मिसाल', 'कई युवा खिलाड़ी उसे अपना ____ मानते हैं।'),
        ('संयोग', 'अचानक घटी अनपेक्षित घटना', 'इत्तफ़ाक़', 'एक ____ ने उसकी मुलाक़ात उस संगीत-गुरु से करा दी, जिन्होंने उसका जीवन बदल दिया।'),
        ('विनम्र', 'जिसमें घमंड न हो, नम्र', 'नम्र', 'इतनी प्रसिद्धि के बाद भी वे बहुत ____ स्वभाव के हैं।'),
        ('मोड़', 'जीवन में आया निर्णायक बदलाव', 'पड़ाव', 'विदेश में मिली छात्रवृत्ति उसके जीवन का सबसे बड़ा ____ साबित हुई।'),
        ('प्रतिभा', 'जन्मजात या विकसित विशेष योग्यता', 'हुनर', 'गाँव के उस लड़के की गणित ____ ने सबको चकित कर दिया।'),
        ('विरासत', 'किसी व्यक्ति द्वारा पीछे छोड़ा गया प्रभाव या योगदान', 'धरोहर', 'उस समाजसेविका की सबसे बड़ी ____ वे विद्यालय हैं जो उन्होंने गाँवों में खोले।'),
    ],
    topics=['मेरे जीवन का एक प्रेरक व्यक्ति', 'असफलता से मिली सीख', 'मेरे दादा-दादी की जीवन-गाथा', 'एक खिलाड़ी का संघर्ष',
            'संघर्ष से सफलता तक', 'मेरे जीवन का एक मोड़', 'आत्मकथा क्यों पढ़नी चाहिए'],
    texts=[
        dict(kind='जीवनी का अंश', title='रामेश्वरम का अख़बार वाला लड़का',
             body='1931 में तमिलनाडु के रामेश्वरम में जन्मे अवुल पकिर जैनुलाब्दीन अब्दुल कलाम का परिवार साधारण था। स्कूल के दिनों में वे परिवार की मदद के लिए सुबह-सुबह अख़बार बाँटते थे। आगे चलकर उन्होंने इंजीनियरिंग पढ़ी और भारत के अंतरिक्ष और मिसाइल कार्यक्रमों में महत्वपूर्ण योगदान दिया, जिससे वे ‘मिसाइल मैन’ कहलाए। 2002 से 2007 तक वे भारत के राष्ट्रपति रहे। उनकी आत्मकथा ‘विंग्स ऑफ़ फ़ायर’ (हिंदी में ‘अग्नि की उड़ान’) आज भी लाखों विद्यार्थियों को प्रेरित करती है।',
             qs=[('C1', 'डॉ. कलाम का जन्म कहाँ हुआ था?', 'रामेश्वरम (तमिलनाडु) में', ['दिल्ली में', 'मुंबई में', 'कोलकाता में']),
                 ('C1', 'डॉ. कलाम किस अवधि में भारत के राष्ट्रपति रहे?', '2002 से 2007 तक'),
                 ('C1', 'उनकी आत्मकथा का हिंदी नाम क्या है?', 'अग्नि की उड़ान', ['सत्य के प्रयोग', 'मेरी कहानी', 'गोदान']),
                 ('C2', 'शीर्षक ‘रामेश्वरम का अख़बार वाला लड़का’ जीवनी के किस पक्ष को उभारता है?', 'यह उनके साधारण, संघर्षपूर्ण बचपन को उभारता है और दिखाता है कि मेहनत से एक साधारण लड़का भी असाधारण ऊँचाई तक पहुँच सकता है।'),
                 ('tf', 'डॉ. कलाम का परिवार बहुत धनी था।', 'गलत', '“…का परिवार साधारण था।”'),
                 ('C3', 'उन्हें ‘मिसाइल मैन’ क्यों कहा गया?', 'भारत के मिसाइल कार्यक्रम में उनके महत्वपूर्ण योगदान के कारण', ['क्योंकि वे अख़बार बाँटते थे', 'क्योंकि वे राष्ट्रपति थे', 'क्योंकि उन्होंने आत्मकथा लिखी']),
                 ('C3', 'यह अंश जीवनी है, आत्मकथा नहीं — पाठ से दो प्रमाण दीजिए।', 'तृतीय पुरुष का प्रयोग (‘वे अख़बार बाँटते थे’, ‘उन्होंने इंजीनियरिंग पढ़ी’); किसी अन्य लेखक द्वारा तथ्यात्मक वर्णन (जन्म-वर्ष, कार्यकाल), ‘मैं’ का प्रयोग नहीं।'),
                 ('C4', '“महान व्यक्तियों की जीवनियाँ पढ़ना विद्यार्थियों के लिए पाठ्य-पुस्तकों जितना ही ज़रूरी है।” — इस अंश के आधार पर अपने विचार लिखिए।', 'पक्ष: प्रेरणा, मूल्य (मेहनत, विनम्रता), करियर की दिशा (कलाम का उदाहरण)। विपक्ष: जीवनियाँ कभी-कभी आदर्शीकृत होती हैं; हर किसी की परिस्थितियाँ अलग। निष्कर्ष: आलोचनात्मक दृष्टि से पढ़ना।')]),
        dict(kind='आत्मकथा का अंश', title='मेरी पहली दौड़',
             body='मैं बारह साल की थी जब गाँव के मेले में पहली बार दौड़ प्रतियोगिता देखी। मेरे पास जूते नहीं थे, इसलिए मैं नंगे पाँव दौड़ी और आख़िरी आई। लौटते समय रोते-रोते मैंने बापू से कहा कि मैं कभी नहीं दौड़ूँगी। बापू ने कुछ नहीं कहा; अगली सुबह उन्होंने मुझे खेत की मेड़ पर दौड़ने के लिए जगा दिया। दो साल बाद उसी मेले में मैं पहले स्थान पर थी — इस बार भी नंगे पाँव। आज जब मैं राष्ट्रीय शिविर में नए जूते पहनती हूँ, तो वह मेड़ याद आती है।',
             qs=[('C1', 'लेखिका ने पहली बार दौड़ प्रतियोगिता कहाँ देखी?', 'गाँव के मेले में', ['विद्यालय के मैदान में', 'टेलीविज़न पर', 'राष्ट्रीय शिविर में']),
                 ('C1', 'पहली दौड़ में लेखिका किस स्थान पर आई?', 'आख़िरी'),
                 ('C2', 'बापू ने रोती हुई बेटी से “कुछ नहीं कहा”, फिर भी उनका व्यवहार उसके लिए प्रेरणा कैसे बना?', 'उन्होंने उपदेश देने के बजाय अगली सुबह उसे अभ्यास के लिए जगाकर कर्म से समर्थन दिखाया; इससे बेटी को विश्वास मिला कि हार अंत नहीं, शुरुआत है।'),
                 ('tf', 'दो साल बाद लेखिका ने नए जूते पहनकर मेले की दौड़ जीती।', 'गलत', '“मैं पहले स्थान पर थी — इस बार भी नंगे पाँव।”'),
                 ('tf', 'लेखिका आज राष्ट्रीय शिविर में अभ्यास करती है।', 'सही', '“आज जब मैं राष्ट्रीय शिविर में नए जूते पहनती हूँ…”'),
                 ('C3', 'अंत में “वह मेड़ याद आती है” — इस वाक्य से लेखिका की किस भावना का पता चलता है?', 'अपनी जड़ों, संघर्ष और पिता के समर्थन के प्रति कृतज्ञता', ['खेती के प्रति अरुचि', 'नए जूतों से असंतोष', 'राष्ट्रीय शिविर छोड़ने की इच्छा']),
                 ('C3', '‘नंगे पाँव’ का दो बार उल्लेख करके लेखिका क्या संदेश देना चाहती है?', 'साधनों की कमी सफलता को नहीं रोक सकती; पहली बार यह अभाव और हार का प्रतीक है, दूसरी बार उसी अभाव में जीत दृढ़ संकल्प का प्रतीक बन जाती है।'),
                 ('C4', 'इस अंश में आत्मकथा की कौन-सी विशेषताएँ इसे पाठक के लिए प्रभावशाली बनाती हैं? उदाहरण सहित मूल्यांकन कीजिए।', 'प्रथम पुरुष की ईमानदार अभिव्यक्ति (‘रोते-रोते’), भावनात्मक मोड़ (हार → अभ्यास → जीत), प्रतीक (नंगे पाँव, मेड़), वर्तमान से अतीत को जोड़ता समापन। संभावित सीमा: संक्षेप में कई वर्ष — विवरण कम। निष्कर्ष।')]),
        dict(kind='लेख', title='एवरेस्ट पर कृत्रिम पैर से पहली भारतीय महिला',
             body='2011 में रेल-यात्रा के दौरान लुटेरों का विरोध करने पर राष्ट्रीय स्तर की वॉलीबॉल खिलाड़ी अरुणिमा सिन्हा को चलती ट्रेन से धक्का दे दिया गया और उनका एक पैर काटना पड़ा। अस्पताल के बिस्तर पर ही उन्होंने एवरेस्ट पर चढ़ने का निश्चय किया। प्रसिद्ध पर्वतारोही बछेंद्री पाल के मार्गदर्शन में प्रशिक्षण लेकर मई 2013 में वे कृत्रिम पैर के साथ एवरेस्ट पर पहुँचने वाली विश्व की पहली महिला बनीं। उनकी कहानी बताती है कि शरीर की सीमा, मन की सीमा नहीं होती।',
             qs=[('C1', 'अरुणिमा सिन्हा किस खेल की राष्ट्रीय स्तर की खिलाड़ी थीं?', 'वॉलीबॉल', ['क्रिकेट', 'हॉकी', 'बैडमिंटन']),
                 ('C1', 'अरुणिमा ने किसके मार्गदर्शन में प्रशिक्षण लिया?', 'बछेंद्री पाल'),
                 ('C1', 'अरुणिमा एवरेस्ट पर कब पहुँचीं?', 'मई 2013'),
                 ('C2', 'अरुणिमा ने अस्पताल के बिस्तर पर ही एवरेस्ट पर चढ़ने का निश्चय किया — इससे उनके व्यक्तित्व के बारे में क्या पता चलता है?', 'वे निराशा में डूबने के बजाय तुरंत नया, कठिन लक्ष्य बनाने वाली, साहसी और दृढ़ संकल्प वाली व्यक्ति हैं।'),
                 ('tf', 'अरुणिमा का पैर एक खेल-दुर्घटना में घायल हुआ था।', 'गलत', '“लुटेरों का विरोध करने पर… चलती ट्रेन से धक्का दे दिया गया।”'),
                 ('C3', '“शरीर की सीमा, मन की सीमा नहीं होती” — इस वाक्य का अर्थ क्या है?', 'शारीरिक कठिनाई होने पर भी दृढ़ इच्छाशक्ति से असंभव लगने वाले लक्ष्य पाए जा सकते हैं', ['शरीर और मन का कोई संबंध नहीं', 'पर्वतारोहण केवल मानसिक खेल है', 'कृत्रिम पैर से चलना आसान है']),
                 ('C3', 'लेख घटनाओं को किस क्रम में प्रस्तुत करता है और यह क्रम पाठक पर क्या प्रभाव डालता है?', 'कालक्रम में: दुर्घटना (2011) → निश्चय → प्रशिक्षण → एवरेस्ट (2013) → संदेश। यह त्रासदी से विजय तक की यात्रा दिखाकर पाठक में सहानुभूति और फिर प्रेरणा जगाता है।'),
                 ('C4', 'क्या मीडिया को ऐसी प्रेरक कहानियाँ अधिक दिखानी चाहिए? इस लेख के आधार पर तर्क दीजिए।', 'पक्ष: प्रेरणा, विकलांगता के प्रति सोच में बदलाव, युवाओं के आदर्श। विपक्ष/सावधानी: ‘प्रेरणा-प्रदर्शन’ से संघर्षरत लोगों पर दबाव, सुलभता (रेल-सुरक्षा, कृत्रिम अंग) जैसे व्यवस्थागत प्रश्न ओझल। संतुलित निष्कर्ष।')]),
    ],
    audio=[
        dict(kind='रेडियो साक्षात्कार', title='‘हौसलों की उड़ान’ — चित्रकार फ़ातिमा शेख़ से बातचीत',
             body='प्रस्तोता: फ़ातिमा जी, आप पैरों से चित्र बनाती हैं। यह सफ़र कैसे शुरू हुआ?\nफ़ातिमा: जन्म से मेरे हाथ काम नहीं करते। सात साल की उम्र में मैंने भाई की पेंसिल पैर की उँगलियों में पकड़ ली — बस, वहीं से शुरुआत हुई।\nप्रस्तोता: सबसे कठिन समय?\nफ़ातिमा: जब एक कला-विद्यालय ने कहा कि मैं ‘सामान्य’ विद्यार्थियों के साथ नहीं पढ़ सकती। मैंने घर पर अभ्यास जारी रखा। पिछले साल उसी विद्यालय ने मेरी प्रदर्शनी लगाई।\nप्रस्तोता: युवाओं के लिए संदेश?\nफ़ातिमा: दूसरों की ‘नहीं’ को अपनी ‘हाँ’ से छोटा मत होने दीजिए।',
             qs=[('C1', 'फ़ातिमा ने चित्र बनाना किस उम्र में शुरू किया?', 'सात साल की उम्र में', ['सत्रह साल की उम्र में', 'तीन साल की उम्र में', 'बीस साल की उम्र में']),
                 ('C1', 'फ़ातिमा ने पहली बार किसकी पेंसिल पकड़ी?', 'अपने भाई की'),
                 ('C2', 'कला-विद्यालय के इनकार का फ़ातिमा पर क्या प्रभाव पड़ा? समझाइए।', 'वह निराश होकर रुकी नहीं; घर पर अभ्यास जारी रखा और अंततः उसी विद्यालय ने उसकी प्रदर्शनी लगाई — इनकार ने उसके संकल्प को और मज़बूत किया।'),
                 ('tf', 'कला-विद्यालय ने आज तक फ़ातिमा के काम को मान्यता नहीं दी।', 'गलत', '“पिछले साल उसी विद्यालय ने मेरी प्रदर्शनी लगाई।”'),
                 ('C3', '“दूसरों की ‘नहीं’ को अपनी ‘हाँ’ से छोटा मत होने दीजिए” — इस संदेश का आशय क्या है?', 'दूसरों के इनकार से अधिक अपनी इच्छाशक्ति और आत्मविश्वास को महत्व दो', ['दूसरों की हर बात मान लो', 'कभी किसी को ‘नहीं’ मत कहो', 'केवल ‘हाँ’ कहने वाले मित्र बनाओ']),
                 ('C3', 'फ़ातिमा की कहानी में ‘विडंबना’ (उल्टा परिणाम) कहाँ दिखाई देती है?', 'जिस विद्यालय ने उसे पढ़ाने से इनकार किया था, उसी ने बाद में उसकी प्रदर्शनी लगाई — अस्वीकार करने वाला ही सम्मान देने वाला बन गया।'),
                 ('C4', 'फ़ातिमा के अनुभव के आधार पर बताइए कि शिक्षा-संस्थान विकलांग विद्यार्थियों के लिए अधिक समावेशी कैसे बन सकते हैं।', 'प्रवेश-नीति में भेदभाव समाप्त करना, अनुकूल उपकरण और शिक्षण-विधियाँ, शिक्षकों का प्रशिक्षण, सहपाठियों में संवेदनशीलता; साक्षात्कार के प्रसंग (इनकार → प्रदर्शनी) से स्पष्ट संबंध।')]),
        dict(kind='पॉडकास्ट', title='‘मेरी कहानी’ — ढाबा चलाने वाली दादी की बातें',
             body='नमस्कार, मैं हूँ निधि, और आज हम बात कर रहे हैं सत्तर वर्षीय कमला दादी से, जो पिछले चालीस साल से हाईवे पर ढाबा चलाती हैं। दादी बताती हैं कि पति के निधन के बाद उनके पास केवल एक चूल्हा और दो बर्तन थे। “लोग कहते थे, औरत ढाबा नहीं चला सकती,” वे हँसकर कहती हैं। आज उनके ढाबे पर दस लोग काम करते हैं और ट्रक-ड्राइवर दूर-दूर से उनके राजमा-चावल खाने आते हैं। उन्होंने अपनी दोनों बेटियों को इंजीनियर बनाया।',
             qs=[('C1', 'कमला दादी कितने साल से ढाबा चला रही हैं?', 'चालीस साल से', ['चौदह साल से', 'सत्तर साल से', 'दस साल से']),
                 ('C1', 'ढाबे पर आज कितने लोग काम करते हैं?', 'दस'),
                 ('C1', 'ट्रक-ड्राइवर दादी के ढाबे पर क्या खाने आते हैं?', 'राजमा-चावल'),
                 ('C2', '“लोग कहते थे, औरत ढाबा नहीं चला सकती” — दादी यह बात हँसकर क्यों कहती हैं?', 'क्योंकि उन्होंने अपनी सफलता से उस पूर्वाग्रह को ग़लत साबित कर दिया; अब वह बात उन्हें दुख नहीं, आत्मविश्वास और संतोष देती है।'),
                 ('tf', 'पति के निधन के समय दादी के पास बहुत-सा सामान था।', 'गलत', '“उनके पास केवल एक चूल्हा और दो बर्तन थे।”'),
                 ('C3', 'दादी की सबसे बड़ी उपलब्धि क्या मानी जा सकती है?', 'अकेले संघर्ष करके व्यवसाय खड़ा करना और बेटियों को इंजीनियर बनाना', ['हाईवे के पास घर बनाना', 'ट्रक चलाना सीखना', 'पॉडकास्ट में भाग लेना']),
                 ('C3', 'यह अंश लैंगिक रूढ़ियों के बारे में क्या संदेश देता है? पाठ से दो प्रमाण दीजिए।', 'महिलाएँ हर क्षेत्र में सफल हो सकती हैं — ‘औरत ढाबा नहीं चला सकती’ की धारणा टूटी; दस लोगों को रोज़गार; बेटियों को इंजीनियर बनाया।'),
                 ('C4', 'साधारण लोगों की जीवन-गाथाएँ प्रसिद्ध हस्तियों की कहानियों जितनी ही प्रेरक हो सकती हैं — कमला दादी के उदाहरण से इस विचार का मूल्यांकन कीजिए।', 'पक्ष: पाठक/श्रोता इनसे अधिक जुड़ाव महसूस करते हैं, यथार्थ और सुलभ लक्ष्य, स्थानीय नायक। विपक्ष: प्रसिद्ध लोगों की कहानियाँ व्यापक प्रभाव और पहुँच रखती हैं। निष्कर्ष।')]),
        dict(kind='रेडियो वार्ता', title='‘आज का प्रेरक व्यक्तित्व’ — मैरी कॉम',
             body='श्रोताओ, आज के कार्यक्रम में बात करते हैं मणिपुर की मुक्केबाज़ मैरी कॉम की। एक किसान परिवार में जन्मी मैरी ने परिवार की जानकारी के बिना मुक्केबाज़ी का प्रशिक्षण शुरू किया था। उन्होंने छह बार विश्व चैंपियनशिप का ख़िताब जीता और 2012 के लंदन ओलंपिक में कांस्य पदक हासिल किया। जुड़वाँ बेटों की माँ बनने के बाद भी उन्होंने रिंग में शानदार वापसी की। उनकी कहानी बताती है कि परिवार और सपनों के बीच चुनाव ज़रूरी नहीं।',
             qs=[('C1', 'मैरी कॉम किस राज्य से हैं?', 'मणिपुर', ['असम', 'हरियाणा', 'केरल']),
                 ('C1', 'मैरी कॉम ने 2012 के ओलंपिक में कौन-सा पदक जीता?', 'कांस्य पदक', ['स्वर्ण पदक', 'रजत पदक', 'कोई पदक नहीं']),
                 ('C1', 'मैरी कॉम ने कितनी बार विश्व चैंपियनशिप का ख़िताब जीता?', 'छह बार'),
                 ('C2', '“परिवार और सपनों के बीच चुनाव ज़रूरी नहीं” — वार्ताकार ने यह निष्कर्ष किस तथ्य से निकाला है?', 'मैरी कॉम जुड़वाँ बेटों की माँ बनने के बाद भी रिंग में लौटीं और सफल रहीं — इससे पता चलता है कि पारिवारिक ज़िम्मेदारियों के साथ भी सपने पूरे किए जा सकते हैं।'),
                 ('tf', 'मैरी कॉम ने परिवार की अनुमति से ही प्रशिक्षण शुरू किया था।', 'गलत', '“परिवार की जानकारी के बिना मुक्केबाज़ी का प्रशिक्षण शुरू किया था।”'),
                 ('C3', 'मैरी कॉम का परिवार की जानकारी के बिना प्रशिक्षण शुरू करना उनके बारे में क्या बताता है?', 'अपने सपने के प्रति गहरी लगन और जोखिम उठाने का साहस', ['वे परिवार की परवाह नहीं करती थीं', 'उन्हें मुक्केबाज़ी पसंद नहीं थी', 'वे केवल पदक के लिए खेलती थीं']),
                 ('C4', 'आपके विचार में किसी खिलाड़ी की सफलता में परिवार, कोच और स्वयं खिलाड़ी में से किसकी भूमिका सबसे बड़ी होती है? मैरी कॉम के उदाहरण से तर्क दीजिए।', 'खिलाड़ी की लगन (गुप्त प्रशिक्षण, वापसी), कोच/सुविधाएँ, परिवार का बाद का समर्थन; स्पष्ट मत और तीनों का संतुलित विश्लेषण।')]),
    ],
    tasks=[
        ('आपकी विद्यालय-पत्रिका ‘हमारे नायक’ नाम से विशेषांक निकाल रही है। आपको अपने समुदाय के किसी प्रेरक व्यक्ति का साक्षात्कार प्रकाशित करना है।', 'interview',
         ['व्यक्ति का परिचय', 'उनके संघर्ष और उपलब्धियाँ', 'युवाओं के लिए उनका संदेश']),
        ('आपके दादा-दादी अस्सी वर्ष के हो गए हैं। आप उनकी जीवन-गाथा परिवार के ब्लॉग पर साझा करना चाहते हैं।', 'blog',
         ['उनके बचपन और युवावस्था की प्रमुख घटनाएँ', 'उनके जीवन के संघर्ष', 'आपने उनसे क्या सीखा']),
        ('आपने हाल ही में किसी प्रसिद्ध व्यक्ति की आत्मकथा पढ़ी है। आप उस पर समीक्षा लिखना चाहते हैं।', 'review',
         ['पुस्तक और लेखक का परिचय', 'जीवन की प्रमुख घटनाएँ और लेखन-शैली', 'पुस्तक पढ़ने की सिफ़ारिश क्यों']),
        ('आपके विद्यालय के एक पूर्व छात्र ने असाधारण सफलता पाई है। प्रधानाचार्य चाहते हैं कि वार्षिकोत्सव में आप उनका परिचय देते हुए भाषण दें।', 'speech',
         ['पूर्व छात्र की उपलब्धियाँ', 'विद्यालय से उनका संबंध', 'विद्यार्थियों के लिए प्रेरणा']),
        ('आज आपकी किसी बड़ी असफलता के ठीक एक साल पूरे हुए हैं, और आज आपने उसी क्षेत्र में सफलता पाई।', 'diary',
         ['एक साल पहले की घटना और भावनाएँ', 'बीच के महीनों का संघर्ष', 'आज की भावनाएँ और सीख']),
        ('एक मित्र आत्मविश्वास खो बैठा है। आप उसे पत्र में किसी प्रेरक व्यक्ति की जीवन-गाथा सुनाकर हिम्मत देना चाहते हैं।', 'pletter',
         ['मित्र की स्थिति पर सहानुभूति', 'प्रेरक व्यक्ति की कहानी', 'मित्र के लिए व्यावहारिक सुझाव']),
    ],
    discuss=[
        ('क्या सफलता के लिए प्रतिभा से अधिक मेहनत ज़रूरी है?', ['निरंतर अभ्यास और अनुशासन', 'जन्मजात योग्यता की भूमिका', 'अवसर और परिस्थितियाँ']),
        ('क्या प्रसिद्ध व्यक्तियों को युवाओं का आदर्श मानना उचित है?', ['प्रेरणा और लक्ष्य', 'उनकी कमियाँ और छवि-निर्माण', 'परिवार और समुदाय के नायक']),
        ('क्या आत्मकथाएँ हमेशा सच बताती हैं?', ['निजी अनुभव की प्रामाणिकता', 'आत्म-प्रशंसा और चुनिंदा स्मृतियाँ', 'पाठक की आलोचनात्मक दृष्टि']),
        ('क्या असफलता सफलता से अधिक सिखाती है?', ['आत्म-चिंतन और सुधार', 'बार-बार की असफलता से आत्मविश्वास में कमी', 'सहयोग और सही दृष्टिकोण']),
        ('क्या हर व्यक्ति की जीवन-गाथा लिखे जाने योग्य है?', ['साधारण लोगों के असाधारण अनुभव', 'इतिहास में अनसुनी आवाज़ें', 'निजता और रुचि का प्रश्न']),
    ],
    pics=[('एक बुज़ुर्ग महिला गाँव के चबूतरे पर बैठी हैं और आस-पास बैठे बच्चे उनकी बातें ध्यान से सुन रहे हैं; पास में पुरानी तस्वीरों का एक एल्बम खुला है।',
           ['मौखिक इतिहास और जीवन-गाथाएँ', 'पीढ़ियों के बीच ज्ञान का आदान-प्रदान', 'यादों को सहेजने का महत्व'])],
)

SPEECH = [
    ('माँ ने कहा, “मैं आज बाज़ार जाऊँगी।”', 'माँ ने कहा कि वे आज बाज़ार जाएँगी।'),
    ('शिक्षक ने रोहन से पूछा, “क्या तुमने गृहकार्य कर लिया है?”', 'शिक्षक ने रोहन से पूछा कि क्या उसने गृहकार्य कर लिया है।'),
    ('पर्वतारोही सुमन ने कहा, “मैंने अपने डर पर विजय पाई है।”', 'पर्वतारोही सुमन ने कहा कि उसने अपने डर पर विजय पाई है।'),
    ('पिताजी ने मुझसे कहा, “समय पर घर लौट आना।”', 'पिताजी ने मुझे समय पर घर लौट आने को कहा।'),
    ('दादी ने कहा, “मेरे बचपन में गाँव में बिजली नहीं थी।”', 'दादी ने कहा कि उनके बचपन में गाँव में बिजली नहीं थी।'),
    ('रीना ने अमित से पूछा, “तुम कहाँ जा रहे हो?”', 'रीना ने अमित से पूछा कि वह कहाँ जा रहा है।'),
    ('कोच ने खिलाड़ियों से कहा, “हार से निराश मत होना।”', 'कोच ने खिलाड़ियों से हार से निराश न होने को कहा।'),
    ('लेखिका ने कहा, “मेरी पहली कहानी एक पत्रिका ने लौटा दी थी।”', 'लेखिका ने बताया कि उनकी पहली कहानी एक पत्रिका ने लौटा दी थी।'),
    ('डॉक्टर ने मरीज़ से कहा, “आप रोज़ सुबह टहलिए।”', 'डॉक्टर ने मरीज़ को रोज़ सुबह टहलने की सलाह दी।'),
    ('अनु ने कहा, “मुझे पहाड़ बहुत पसंद हैं।”', 'अनु ने कहा कि उसे पहाड़ बहुत पसंद हैं।'),
    ('बच्चे ने माँ से पूछा, “क्या मैं खेलने जा सकता हूँ?”', 'बच्चे ने माँ से पूछा कि क्या वह खेलने जा सकता है।'),
    ('खिलाड़ी ने पत्रकारों से कहा, “यह जीत मेरे पूरे गाँव की है।”', 'खिलाड़ी ने पत्रकारों से कहा कि वह जीत उसके पूरे गाँव की है।'),
    ('प्रधानाचार्या ने विद्यार्थियों से कहा, “कल विद्यालय बंद रहेगा।”', 'प्रधानाचार्या ने विद्यार्थियों को बताया कि अगले दिन विद्यालय बंद रहेगा।'),
]

def g_speech(kit, key, th):
    def which(rng, slot):
        d, i = rng.choice(SPEECH)
        others = [x[0] for x in SPEECH if x[0] != d]
        return mcq(rng, 'इनमें से कौन-सा वाक्य अप्रत्यक्ष कथन में है?', i, rng.sample(others, 3),
                   'अप्रत्यक्ष कथन में उद्धरण-चिह्न नहीं होते; बात ‘कि’ या ‘को कहा/से पूछा कि क्या’ से रिपोर्ट की जाती है।')
    kit.add(key, 'C1', (1, 3), which, 'mcq', None, 'sp_which')

    def changes(rng, slot):
        d, i = rng.choice(SPEECH)
        return dict(stem=f'प्रत्यक्ष कथन: {d}\nअप्रत्यक्ष कथन: {i}\nइस रूपांतरण में हुए कोई दो बदलाव पहचानिए और प्रत्येक का कारण समझाइए।',
                    answer='संभावित बदलाव: उद्धरण-चिह्न हटे; ‘कि’ जोड़ा गया या आज्ञा ‘…को कहा/की सलाह दी’ में बदली; प्रश्न ‘…से पूछा कि क्या…’ बना; बोलने वाले के अनुसार सर्वनाम (मैं → वह/वे, तुम → वह) और क्रिया-रूप बदले।',
                    type='explain', marks=2, markingKey='प्रत्येक सही बदलाव और उसके कारण के लिए 1 अंक (अधिकतम 2)।')
    kit.add(key, 'C2', (1, 4), changes, 'explain', None, 'sp_changes')


SPEC['ch06-st1'] = ('reading', dict(focus='लेखन में किसी जीवन-गाथा की घटनाओं को कालक्रम में प्रस्तुत कीजिए।', items=[
    ('C1', 'आत्मकथा की सबसे प्रमुख भाषिक पहचान क्या है?', 'प्रथम पुरुष (मैं) में लेखक द्वारा अपने जीवन का वर्णन', ['तृतीय पुरुष में किसी दूसरे का वर्णन', 'केवल संवादों का प्रयोग', 'प्रश्न-उत्तर का प्रारूप'], 'आत्मकथा लेखक स्वयं अपने बारे में लिखता है।'),
    ('C1', 'प्रेमचंद के जीवन पर उनके पुत्र अमृत राय ने ‘क़लम का सिपाही’ लिखी। यह किस विधा की रचना है?', 'जीवनी', ['आत्मकथा', 'यात्रा-वृत्तांत', 'उपन्यास'], 'किसी दूसरे व्यक्ति के जीवन पर लिखी गई रचना जीवनी है।'),
    ('C2', 'आत्मकथा और जीवनी में दृष्टिकोण (कथन-दृष्टि) का क्या अंतर होता है और इसका पाठक पर क्या प्रभाव पड़ता है?', 'आत्मकथा में लेखक अपने अनुभव और भावनाएँ भीतर से बताता है, जिससे आत्मीयता और भावनात्मक गहराई आती है; जीवनी में लेखक बाहर से, शोध और तथ्यों के आधार पर लिखता है, जिससे अधिक वस्तुनिष्ठ, संतुलित चित्र बनता है।', '1-1 अंक प्रत्येक दृष्टिकोण, 1 अंक प्रभाव।', 3),
]))
SPEC['ch06-st2'] = ('listening', dict(focus='लेखन में किसी प्रेरक व्यक्ति के कथनों को अप्रत्यक्ष कथन में प्रस्तुत कीजिए।', items=[
    ('C1', 'साक्षात्कार सुनते समय ‘मुख्य शब्द’ (कीवर्ड) पहचानने का सबसे अच्छा तरीका क्या है?', 'प्रश्नों में आए नाम, संख्या और विषय-शब्दों को पहले रेखांकित करना', ['हर शब्द लिखने का प्रयास करना', 'केवल अंतिम वाक्य सुनना', 'प्रश्न बाद में पढ़ना'], 'प्रश्न के मुख्य शब्द बताते हैं कि श्रव्य अंश में किस जानकारी पर ध्यान देना है।'),
    ('C2', 'प्रेरक व्यक्तित्वों के साक्षात्कारों में ‘सबसे कठिन समय’ जैसे प्रश्न क्यों पूछे जाते हैं? श्रोता के दृष्टिकोण से समझाइए।', 'ये प्रश्न व्यक्ति के संघर्ष और भावनाओं को सामने लाते हैं; श्रोता इससे जुड़ाव महसूस करता है और सफलता के पीछे की मेहनत समझता है, जिससे प्रेरणा मिलती है।', '1 अंक प्रश्न का उद्देश्य, 1 अंक श्रोता पर प्रभाव।'),
]))
SPEC['ch06-st3'] = ('writing', dict(tt='interview', tasks=[
    ('विद्यालय-पत्रिका के लिए आपको विद्यालय के सबसे पुराने कर्मचारी (जैसे माली या चपरासी) का साक्षात्कार लेना है, जो तीस साल से वहाँ काम कर रहे हैं।', ['उनका परिचय और विद्यालय से जुड़ाव', 'विद्यालय में आए बदलाव', 'विद्यार्थियों के लिए उनका संदेश']),
    ('आपके शहर की एक युवा उद्यमी ने पुराने कपड़ों से थैले बनाने का व्यवसाय शुरू किया है। स्थानीय पत्रिका के लिए उनका साक्षात्कार लिखिए।', ['व्यवसाय का विचार कैसे आया', 'शुरुआती कठिनाइयाँ', 'पर्यावरण और युवाओं के लिए संदेश']),
    ('एक राष्ट्रीय स्तर के पैरा-एथलीट आपके विद्यालय आए। विद्यालय की वेबसाइट के लिए उनका साक्षात्कार तैयार कीजिए।', ['खेल की शुरुआत', 'संघर्ष और समाज का दृष्टिकोण', 'भविष्य के लक्ष्य']),
    ('आपकी दादी ने 1970 के दशक में गाँव की पहली महिला शिक्षिका के रूप में काम किया था। परिवार-पत्रिका के लिए उनका साक्षात्कार लीजिए।', ['उस समय की परिस्थितियाँ', 'उन्हें मिला विरोध और समर्थन', 'आज की लड़कियों के लिए उनकी सीख']),
    ('एक प्रवासी लेखक, जो विदेश में रहकर हिंदी में लिखते हैं, आपके शहर के पुस्तक-मेले में आए हैं। उनका साक्षात्कार लिखिए।', ['विदेश में हिंदी लेखन का अनुभव', 'उनकी रचनाओं के विषय', 'नई पीढ़ी को हिंदी से जोड़ने के सुझाव']),
], items=[
    ('C1', 'साक्षात्कार में ‘खुले प्रश्न’ का उदाहरण कौन-सा है?', 'आपको इस काम की प्रेरणा कहाँ से मिली?', ['क्या आप ख़ुश हैं?', 'क्या आपकी उम्र तीस साल है?', 'क्या आपने पुरस्कार जीता?'], 'खुले प्रश्न (कैसे, क्यों, कहाँ से) विस्तृत उत्तर दिलवाते हैं; ‘क्या’ वाले बंद प्रश्नों का उत्तर हाँ/नहीं में होता है।'),
    ('C2', 'साक्षात्कार की भूमिका में साक्षात्कारदाता का परिचय क्यों आवश्यक है?', 'पाठक को पता चलता है कि व्यक्ति कौन है और उसका साक्षात्कार क्यों पढ़ना चाहिए; इससे संदर्भ बनता है और पाठक की रुचि जगती है।', '1 अंक संदर्भ, 1 अंक पाठक की रुचि/उद्देश्य।'),
    ('C3', 'इस बंद प्रश्न को खुले प्रश्न में बदलिए: “क्या आपको बचपन में चित्रकारी पसंद थी?”', 'नमूना: “बचपन में चित्रकारी के प्रति आपकी रुचि कैसे जगी, और उस समय आप क्या बनाना पसंद करते थे?”', '1 अंक ‘कैसे/क्यों/क्या-क्या’ जैसे खुले प्रश्न-शब्द, 1 अंक अर्थ सुरक्षित।', 2),
]))
SPEC['ch06-st4'] = ('grammar', dict(focus='लेखन में प्रत्यक्ष और अप्रत्यक्ष कथन का सही प्रयोग कीजिए।', gens=[
    g_speech,
    g_transform(SPEECH, 'प्रत्यक्ष कथन', 'अप्रत्यक्ष कथन', extra_key='— 1 अंक ‘कि’/उपयुक्त संरचना, 1 अंक सर्वनाम और क्रिया-रूप का सही परिवर्तन।'),
    g_free([('‘{topic}’ विषय पर किसी व्यक्ति से हुई बातचीत को 80–100 शब्दों में रिपोर्ट कीजिए। कम से कम चार कथन अप्रत्यक्ष कथन में और एक कथन प्रत्यक्ष कथन (उद्धरण-चिह्नों सहित) में हो।',
             'अपेक्षित: ‘कि’ और ‘को कहा/से पूछा कि क्या’ जैसी संरचनाओं का शुद्ध प्रयोग; सर्वनामों का सही परिवर्तन; एक सही विराम-चिह्नित उद्धरण।')]),
], items=[
    ('C1', 'प्रत्यक्ष कथन को अप्रत्यक्ष कथन में बदलते समय हिंदी में प्रायः कौन-सा योजक जोड़ा जाता है?', 'कि', ['और', 'लेकिन', 'या'], '“उसने कहा कि…” — ‘कि’ अप्रत्यक्ष कथन का सामान्य योजक है।'),
    ('C1', '“माँ ने कहा, ‘मैं आज बाज़ार जाऊँगी।’” — इसका सही अप्रत्यक्ष रूप कौन-सा है?', 'माँ ने कहा कि वे आज बाज़ार जाएँगी।', ['माँ ने कहा कि मैं आज बाज़ार जाऊँगी।', 'माँ ने कहा कि तुम आज बाज़ार जाओगे।', 'माँ ने कहा, वे आज बाज़ार जाएँगी कि।'], 'अप्रत्यक्ष कथन में ‘मैं’ → ‘वे’ (आदरसूचक), क्रिया उसी के अनुसार।'),
    ('C1', '“कोच ने कहा, ‘निराश मत होना।’” — इसका सही अप्रत्यक्ष रूप कौन-सा है?', 'कोच ने निराश न होने को कहा।', ['कोच ने कहा कि निराश मत होना।', 'कोच ने निराश होने को कहा।', 'कोच ने पूछा कि क्या निराश मत होना।'], 'आज्ञा/निषेध वाले कथन में ‘…न होने को कहा’ जैसी संरचना प्रयुक्त होती है।'),
    ('C2', 'आज्ञावाचक प्रत्यक्ष कथन (“समय पर लौट आना”) को अप्रत्यक्ष कथन में बदलते समय क्रिया का रूप क्यों बदल जाता है? समझाइए।', 'अप्रत्यक्ष कथन में आज्ञा को रिपोर्ट किया जाता है, इसलिए आज्ञार्थ क्रिया क्रियार्थक संज्ञा में बदलती है और ‘को कहा/की सलाह दी’ जुड़ता है — “पिताजी ने मुझे समय पर लौट आने को कहा।”', '1 अंक नियम, 1 अंक सही उदाहरण।'),
    ('C2', 'जीवनी या समाचार-रिपोर्ट में लेखक कभी प्रत्यक्ष कथन (उद्धरण) और कभी अप्रत्यक्ष कथन क्यों चुनता है?', 'प्रत्यक्ष कथन व्यक्ति के अपने शब्दों से भावना और प्रामाणिकता लाता है; अप्रत्यक्ष कथन बात को संक्षेप में, लेखक के प्रवाह में प्रस्तुत करता है — दोनों का मिश्रण पाठ को रोचक और संतुलित बनाता है।', '1 अंक प्रत्येक के प्रभाव के लिए।'),
]))


# ---------------------------------------------------------------- ch07 रीति-रिवाज, परंपराएँ और संस्कार
TH[7] = dict(
    name='रीति-रिवाज, परंपराएँ और संस्कार',
    vocab=[
        ('संस्कार', 'जीवन के महत्वपूर्ण पड़ावों पर किए जाने वाले पारंपरिक अनुष्ठान', 'अनुष्ठान', 'नामकरण, मुंडन और विवाह हिंदू परिवारों के प्रमुख ____ हैं।'),
        ('परंपरा', 'पीढ़ी-दर-पीढ़ी चली आ रही रीति', 'रिवाज', 'होली पर रंग खेलने की ____ सदियों पुरानी है।'),
        ('उत्सव', 'आनंद और उल्लास से मनाया जाने वाला अवसर', 'पर्व', 'पोंगल तमिलनाडु का फ़सल से जुड़ा प्रमुख ____ है।'),
        ('विदाई', 'किसी को जाते समय दी जाने वाली भावनात्मक बिदाई', 'बिदाई', 'विवाह के बाद दुल्हन की ____ पर पूरा परिवार भावुक हो गया।'),
        ('आशीर्वाद', 'बड़ों द्वारा दी गई शुभकामना', 'दुआ', 'परीक्षा से पहले मैंने दादी का ____ लिया।'),
        ('पकवान', 'विशेष अवसरों पर बनने वाले स्वादिष्ट व्यंजन', 'व्यंजन', 'ईद पर अम्मी सेवइयाँ और कई ____ बनाती हैं।'),
        ('शोभायात्रा', 'उत्सव पर निकाला जाने वाला सजा हुआ जुलूस', 'जुलूस', 'गणेश-विसर्जन की ____ में हज़ारों लोग नाचते-गाते चले।'),
        ('रंगोली', 'त्योहारों पर आँगन या द्वार पर रंगों से बनाई जाने वाली सजावट', 'अल्पना', 'दिवाली पर बहन ने द्वार पर सुंदर ____ बनाई।'),
        ('व्रत', 'धार्मिक कारण से रखा जाने वाला उपवास', 'उपवास', 'कई लोग नवरात्रि में नौ दिन का ____ रखते हैं।'),
        ('सामूहिक', 'सबके साथ मिलकर किया जाने वाला', 'सम्मिलित', 'लोहड़ी पर अलाव के चारों ओर ____ नृत्य होता है।'),
        ('लोकाचार', 'समाज में प्रचलित व्यवहार के नियम', 'सामाजिक रीति', 'बड़ों के पैर छूना उत्तर भारत का एक आम ____ है।'),
        ('आधुनिकता', 'नए विचारों और जीवन-शैली को अपनाने की प्रवृत्ति', 'नवीनता', 'शहरों में विवाह के रीति-रिवाजों पर ____ का गहरा असर दिखता है।'),
        ('दहेज', 'विवाह में वधू-पक्ष से वर-पक्ष को दिया जाने वाला धन-सामान', 'दायज', '____ लेना और देना दोनों क़ानूनन अपराध हैं।'),
        ('अनुष्ठान', 'विधि-विधान से किया जाने वाला धार्मिक कार्य', 'कर्मकांड', 'गृह-प्रवेश के ____ के लिए पंडित जी को बुलाया गया।'),
    ],
    topics=['मेरा प्रिय त्योहार', 'परंपरा और आधुनिकता का संतुलन', 'शादियों में फ़िज़ूलख़र्ची', 'पर्यावरण-अनुकूल त्योहार',
            'विदेश में भारतीय त्योहार', 'जीवन के संस्कार और उनका अर्थ', 'दादी-नानी की परंपराएँ'],
    texts=[
        dict(kind='लेख', title='हरी होली, ख़ुशहाल होली',
             body='पिछले कुछ वर्षों में होली के रासायनिक रंगों से त्वचा-रोग और आँखों की समस्याओं की शिकायतें बढ़ी हैं। इसलिए इंदौर के ‘हरित मित्र’ समूह ने तीन साल पहले फूलों और हल्दी से प्राकृतिक रंग बनाने की कार्यशालाएँ शुरू कीं। पहले साल केवल पचास लोग आए, इस साल पाँच सौ से ज़्यादा। समूह की संयोजिका रचना जोशी कहती हैं, “त्योहार बदलें नहीं, बेहतर बनें — यही हमारा लक्ष्य है।” कई परिवार अब पानी की बचत के लिए ‘सूखी होली’ भी खेलने लगे हैं।',
             qs=[('C1', '‘हरित मित्र’ समूह प्राकृतिक रंग किससे बनाता है?', 'फूलों और हल्दी से', ['रासायनिक पाउडर से', 'प्लास्टिक से', 'मिट्टी के तेल से']),
                 ('C1', 'इस साल कार्यशाला में लगभग कितने लोग आए?', 'पाँच सौ से ज़्यादा'),
                 ('C2', '“त्योहार बदलें नहीं, बेहतर बनें” — रचना जोशी के इस कथन का आशय स्पष्ट कीजिए।', 'त्योहार की मूल भावना और परंपरा बनी रहे, पर उसके हानिकारक तरीके (रासायनिक रंग, पानी की बर्बादी) सुधारे जाएँ, ताकि वह स्वास्थ्य और पर्यावरण के लिए अनुकूल हो।'),
                 ('tf', 'पहले साल कार्यशाला में पाँच सौ लोग आए थे।', 'गलत', '“पहले साल केवल पचास लोग आए।”'),
                 ('tf', 'कई परिवार पानी बचाने के लिए सूखी होली खेलने लगे हैं।', 'सही', '“पानी की बचत के लिए ‘सूखी होली’ भी खेलने लगे हैं।”'),
                 ('C3', 'कार्यशाला में आने वालों की संख्या में वृद्धि से क्या निष्कर्ष निकलता है?', 'लोगों में पर्यावरण-अनुकूल त्योहारों के प्रति जागरूकता बढ़ रही है', ['लोग होली मनाना छोड़ रहे हैं', 'रासायनिक रंग सस्ते हो गए हैं', 'कार्यशाला मुफ़्त भोजन देती है']),
                 ('C3', 'लेख किस समस्या से शुरू होकर किस समाधान तक पहुँचता है? संक्षेप में लिखिए।', 'समस्या: रासायनिक रंगों से त्वचा और आँखों के रोग। समाधान: प्राकृतिक रंगों की कार्यशालाएँ और पानी बचाने वाली सूखी होली।'),
                 ('C4', 'क्या पारंपरिक त्योहारों को पर्यावरण के अनुसार बदलना उनकी मूल भावना के विरुद्ध है? लेख के आधार पर अपना मत दीजिए।', 'नहीं: मूल भावना (मेल-मिलाप, उल्लास) सुरक्षित, केवल तरीके बदलते हैं; परंपराएँ सदा विकसित हुई हैं। विपक्ष: कुछ लोग इसे परंपरा में हस्तक्षेप मानते हैं। निष्कर्ष: समुदाय की सहमति से सुधार।')]),
        dict(kind='ब्लॉग प्रविष्टि', title='टोरंटो में मेरी पहली दिवाली — 12 नवंबर',
             body='इस साल मैं पढ़ाई के लिए कनाडा में हूँ, और दिवाली पर घर से दूर होने का ख़याल ही उदास कर रहा था। फिर हॉस्टल की नेपाली और गुयानी सहेलियों ने कहा, “चलो, यहीं मनाते हैं!” हमने कमरे में बिजली वाले दीये लगाए, क्योंकि हॉस्टल में असली दीये जलाना मना है। मेरी कोरियाई रूममेट ने पहली बार रंगोली बनाई — टेढ़ी-मेढ़ी, पर दिल से। वीडियो-कॉल पर माँ ने आरती करवाई। सच कहूँ, परंपरा जगह में नहीं, लोगों में बसती है। आप विदेश में त्योहार कैसे मनाते हैं?',
             qs=[('C1', 'लेखिका किस देश में पढ़ाई कर रही है?', 'कनाडा', ['नेपाल', 'कोरिया', 'गुयाना']),
                 ('C1', 'हॉस्टल में बिजली वाले दीये क्यों लगाए गए?', 'क्योंकि हॉस्टल में असली दीये जलाना मना है'),
                 ('C2', '“टेढ़ी-मेढ़ी, पर दिल से” — लेखिका ने रूममेट की रंगोली के बारे में ऐसा क्यों कहा?', 'रंगोली कलात्मक रूप से पूरी तरह सही नहीं थी, पर उसमें प्रेम, उत्साह और दूसरी संस्कृति को अपनाने की सच्ची भावना थी — लेखिका के लिए भावना सुंदरता से अधिक मूल्यवान थी।'),
                 ('tf', 'लेखिका ने दिवाली अकेले मनाई।', 'गलत', '“हॉस्टल की नेपाली और गुयानी सहेलियों ने कहा, ‘चलो, यहीं मनाते हैं!’”'),
                 ('tf', 'माँ ने वीडियो-कॉल पर आरती करवाई।', 'सही', '“वीडियो-कॉल पर माँ ने आरती करवाई।”'),
                 ('C3', '“परंपरा जगह में नहीं, लोगों में बसती है” — इस निष्कर्ष तक लेखिका किस अनुभव से पहुँची?', 'विदेश में अलग-अलग देशों की सहेलियों के साथ दिवाली मनाकर, जिससे घर जैसी ख़ुशी मिली', ['भारत लौटकर दिवाली मनाने से', 'हॉस्टल के नियम तोड़ने से', 'अकेले रहकर उदास होने से']),
                 ('C3', 'इस ब्लॉग में बहुसांस्कृतिकता के कौन-से दो उदाहरण मिलते हैं?', 'नेपाली और गुयानी सहेलियों का साथ मिलकर त्योहार मनाना; कोरियाई रूममेट का पहली बार रंगोली बनाना; कनाडा में भारतीय त्योहार।'),
                 ('C4', 'क्या प्रवासी लोगों के लिए अपने त्योहार मनाना अपनी पहचान बचाए रखने का सबसे अच्छा तरीका है? ब्लॉग और अपने विचारों के आधार पर उत्तर दीजिए।', 'पक्ष: त्योहार सांस्कृतिक जुड़ाव, भावनात्मक सहारा, नई पीढ़ी तक परंपरा पहुँचाना। अन्य तरीके: भाषा, भोजन, समुदाय-संगठन। ब्लॉग का प्रमाण: लोग और संबंध ही परंपरा को जीवित रखते हैं।')]),
        dict(kind='संपादकीय', title='शादी या शान-शौकत?',
             body='एक सर्वेक्षण के अनुसार मध्यमवर्गीय भारतीय परिवार अपनी बचत का बड़ा हिस्सा केवल विवाह-समारोहों पर ख़र्च कर देते हैं। कई परिवार इसके लिए क़र्ज़ तक लेते हैं। दिखावे की यह होड़ विवाह के मूल अर्थ — दो परिवारों के मिलन — को पीछे धकेल रही है। सुखद बात यह है कि कुछ युवा जोड़े अब सादे विवाह, अदालत में पंजीकरण या सामूहिक विवाह चुन रहे हैं और बचे पैसे से पढ़ाई या घर की योजना बना रहे हैं। समाज को इस सादगी का सम्मान करना सीखना होगा।',
             qs=[('C1', 'सर्वेक्षण के अनुसार मध्यमवर्गीय परिवार अपनी बचत का बड़ा हिस्सा किस पर ख़र्च करते हैं?', 'विवाह-समारोहों पर', ['पढ़ाई पर', 'स्वास्थ्य पर', 'यात्रा पर']),
                 ('C1', 'लेखक के अनुसार विवाह का मूल अर्थ क्या है?', 'दो परिवारों का मिलन'),
                 ('C2', '‘दिखावे की होड़’ से लेखक का क्या तात्पर्य है?', 'समाज में अपनी प्रतिष्ठा दिखाने के लिए दूसरों से अधिक भव्य और महँगा आयोजन करने की प्रतिस्पर्धा, भले ही उसके लिए क़र्ज़ लेना पड़े।'),
                 ('tf', 'लेखक सादे विवाह चुनने वाले युवा जोड़ों की आलोचना करता है।', 'गलत', '“सुखद बात यह है कि कुछ युवा जोड़े अब सादे विवाह… चुन रहे हैं।”'),
                 ('C3', 'संपादकीय का मुख्य उद्देश्य क्या है?', 'विवाहों में फ़िज़ूलख़र्ची के विरुद्ध सादगी को बढ़ावा देना', ['शादी की सजावट के सुझाव देना', 'क़र्ज़ देने वाले बैंकों का विज्ञापन करना', 'विवाह की परंपरा को समाप्त करना']),
                 ('C3', 'शीर्षक ‘शादी या शान-शौकत?’ में प्रश्नवाचक रूप क्यों चुना गया है?', 'पाठक को सोचने पर मजबूर करने के लिए कि विवाह का असली उद्देश्य संबंध है या प्रदर्शन; यह संपादकीय की केंद्रीय दुविधा को सीधे सामने रखता है।'),
                 ('C4', '“भव्य विवाह परंपरा का हिस्सा हैं और कई लोगों को रोज़गार देते हैं।” — इस प्रतितर्क को ध्यान में रखते हुए संपादकीय के मत का मूल्यांकन कीजिए।', 'प्रतितर्क: कारीगरों, कैटरिंग, संगीतकारों की आजीविका; सांस्कृतिक उल्लास। संपादकीय का पक्ष: क़र्ज़, सामाजिक दबाव, दहेज से संबंध। निष्कर्ष: सामर्थ्य के अनुसार उत्सव, दबाव-मुक्त चुनाव।')]),
    ],
    tasks=[
        ('आपके अंतरराष्ट्रीय विद्यालय की पत्रिका ‘विश्व-त्योहार’ विशेषांक निकाल रही है। आप अपने परिवार के किसी त्योहार के बारे में लिखना चाहते हैं।', 'article',
         ['त्योहार का महत्व और कहानी', 'आपके परिवार में उसे कैसे मनाया जाता है', 'समय के साथ आए बदलाव']),
        ('आपके मोहल्ले में त्योहारों पर देर रात तक तेज़ आवाज़ में संगीत बजता है, जिससे बुज़ुर्गों और विद्यार्थियों को परेशानी होती है।', 'fletter',
         ['समस्या और उसका प्रभाव', 'त्योहार की भावना का सम्मान करते हुए सुझाव', 'प्रशासन से अनुरोध']),
        ('आपके बड़े भाई की शादी सादगी से होने वाली है, पर कुछ रिश्तेदार नाराज़ हैं। आप इस पर अपना ब्लॉग लिखना चाहते हैं।', 'blog',
         ['परिवार का निर्णय और कारण', 'रिश्तेदारों की प्रतिक्रिया', 'सादे विवाह पर आपके विचार']),
        ('विद्यालय में ‘परंपरा और आधुनिकता’ विषय पर भाषण प्रतियोगिता है।', 'speech',
         ['एक परंपरा जो आज भी उपयोगी है', 'एक परंपरा जिसमें बदलाव ज़रूरी है', 'युवाओं की भूमिका']),
        ('आप पहली बार किसी दूसरे धर्म के मित्र के घर उसके त्योहार में शामिल हुए।', 'diary',
         ['आपने क्या देखा और किया', 'आपकी भावनाएँ और सीख', 'अपनी परंपराओं से तुलना']),
        ('आपके विदेशी पत्र-मित्र ने पूछा है कि भारत में किशोरावस्था से जुड़े कौन-से संस्कार या रस्में होती हैं।', 'pletter',
         ['एक-दो संस्कारों का वर्णन', 'उनका अर्थ और महत्व', 'आपका निजी अनुभव और विचार']),
    ],
    discuss=[
        ('क्या आधुनिक जीवन में पारंपरिक संस्कारों का कोई महत्व बचा है?', ['परिवार और समुदाय को जोड़ते हैं', 'कुछ रस्में अर्थहीन या ख़र्चीली', 'अर्थ समझकर संस्कारों को अपनाना']),
        ('क्या त्योहारों का व्यवसायीकरण उनकी असली भावना को कम कर रहा है?', ['ऑनलाइन सेल और उपहारों का दबाव', 'व्यापार और रोज़गार में वृद्धि', 'सादगी और सामुदायिक भावना']),
        ('क्या हर परंपरा का पालन केवल इसलिए करना चाहिए कि वह पुरानी है?', ['परंपरा में संचित अनुभव', 'तर्क और मानवाधिकार की कसौटी', 'हानिकारक प्रथाओं (दहेज) का विरोध']),
        ('क्या विद्यालयों में सभी धर्मों और संस्कृतियों के त्योहार मनाए जाने चाहिए?', ['समावेश और आपसी समझ', 'समय और संवेदनशीलता की चुनौती', 'शैक्षिक दृष्टि से त्योहारों का परिचय']),
        ('क्या पटाखों पर प्रतिबंध त्योहार की ख़ुशी छीन लेता है?', ['प्रदूषण, जानवरों और बीमारों पर असर', 'परंपरा और बच्चों का उत्साह', 'हरित पटाखे और सामुदायिक आयोजन']),
    ],
    pics=[('एक गाँव में करवा चौथ की शाम छत पर महिलाएँ छलनी से चाँद देख रही हैं; पास में एक युवा पति भी व्रत रखकर खड़ा है और मुस्करा रहा है।',
           ['परंपरागत व्रत और पारिवारिक संबंध', 'परंपरा में लैंगिक भूमिकाओं का बदलाव', 'आस्था और आधुनिक सोच का मेल']),
          ('ओणम पर केरल के एक घर के आँगन में फूलों की गोल ‘पूकलम’ बनाई गई है; बच्चे फूल सजा रहे हैं और पीछे केले के पत्ते पर ‘सद्या’ भोज परोसा जा रहा है।',
           ['फ़सल-उत्सव और प्रकृति', 'सामूहिकता और पारिवारिक भोज', 'भारत की क्षेत्रीय सांस्कृतिक विविधता']),
          ('एक विवाह-मंडप में दूल्हा-दुल्हन सात फेरे ले रहे हैं; मेहमानों में से कई अपने मोबाइल से वीडियो बना रहे हैं और एक ड्रोन कैमरा ऊपर उड़ रहा है।',
           ['संस्कार और तकनीक', 'विवाह में दिखावा बनाम भावना', 'परंपरा का बदलता स्वरूप'])],
)

IDIOMS = [
    ('आँखों का तारा', 'बहुत प्यारा', 'छोटी बहन पूरे परिवार की [आँखों का तारा] है।', 'मुहावरा'),
    ('नौ दो ग्यारह होना', 'भाग जाना', 'पुलिस को देखते ही चोर [नौ दो ग्यारह हो गए]।', 'मुहावरा'),
    ('ईद का चाँद होना', 'बहुत दिनों बाद दिखाई देना', 'तुम तो आजकल [ईद का चाँद हो गए] हो!', 'मुहावरा'),
    ('नाक में दम करना', 'बहुत परेशान करना', 'शरारती बच्चों ने मेहमानों की [नाक में दम कर दिया]।', 'मुहावरा'),
    ('हाथ-पाँव फूलना', 'घबरा जाना', 'मंच पर पहुँचते ही मेरे [हाथ-पाँव फूल गए]।', 'मुहावरा'),
    ('आसमान सिर पर उठाना', 'बहुत शोर मचाना', 'मेले में बच्चों ने [आसमान सिर पर उठा लिया]।', 'मुहावरा'),
    ('घी के दीये जलाना', 'बहुत ख़ुशियाँ मनाना', 'बेटे के सकुशल लौटने पर परिवार ने [घी के दीये जलाए]।', 'मुहावरा'),
    ('मुँह में पानी आना', 'खाने की तीव्र इच्छा होना', 'गरम जलेबियाँ देखकर मेरे [मुँह में पानी आ गया]।', 'मुहावरा'),
    ('फूला न समाना', 'बहुत अधिक प्रसन्न होना', 'परिणाम सुनकर वह [फूली न समाई]।', 'मुहावरा'),
    ('आग में घी डालना', 'झगड़े या क्रोध को और भड़काना', 'उसकी कड़वी बात ने [आग में घी डालने] का काम किया।', 'मुहावरा'),
    ('दाँतों तले उँगली दबाना', 'बहुत आश्चर्यचकित होना', 'नन्हे बच्चे का तबला-वादन सुनकर सबने [दाँतों तले उँगली दबा ली]।', 'मुहावरा'),
    ('पानी-पानी होना', 'बहुत लज्जित होना', 'झूठ पकड़े जाने पर वह [पानी-पानी हो गया]।', 'मुहावरा'),
    ('सिर आँखों पर बिठाना', 'बहुत आदर-सत्कार करना', 'गाँव वालों ने पदक-विजेता को [सिर आँखों पर बिठाया]।', 'मुहावरा'),
    ('कमर कसना', 'किसी काम के लिए पूरी तरह तैयार होना', 'वार्षिक परीक्षा के लिए हमने [कमर कस ली] है।', 'मुहावरा'),
    ('अब पछताए होत क्या, जब चिड़िया चुग गई खेत', 'समय निकल जाने के बाद पछताना व्यर्थ है', 'पूरे साल नहीं पढ़े और अब रो रहे हो? [अब पछताए होत क्या, जब चिड़िया चुग गई खेत]।', 'लोकोक्ति'),
    ('जैसी करनी वैसी भरनी', 'जैसा कर्म, वैसा फल', 'उसने सबको धोखा दिया और अब कोई उसकी मदद नहीं करता — [जैसी करनी वैसी भरनी]।', 'लोकोक्ति'),
    ('नाच न जाने आँगन टेढ़ा', 'अपनी कमी का दोष दूसरों पर डालना', 'ख़ुद तैयारी नहीं की और कहता है कि प्रश्न-पत्र ग़लत था — [नाच न जाने आँगन टेढ़ा]।', 'लोकोक्ति'),
    ('एक अनार सौ बीमार', 'एक वस्तु के अनेक चाहने वाले', 'एक ही ख़ाली सीट और बीस उम्मीदवार — [एक अनार सौ बीमार]।', 'लोकोक्ति'),
    ('ऊँट के मुँह में ज़ीरा', 'आवश्यकता से बहुत कम', 'इतने बड़े परिवार के लिए एक किलो मिठाई तो [ऊँट के मुँह में ज़ीरा] है।', 'लोकोक्ति'),
    ('घर की मुर्गी दाल बराबर', 'घर की चीज़ या व्यक्ति का महत्व न समझना', 'विदेशी लोग उनकी पेंटिंग ख़रीदते हैं, पर अपने ही शहर में कोई क़द्र नहीं — [घर की मुर्गी दाल बराबर]।', 'लोकोक्ति'),
    ('जहाँ चाह, वहाँ राह', 'सच्ची इच्छा हो तो रास्ता मिल ही जाता है', 'बिना कोचिंग के उसने परीक्षा पास कर ली — सच है, [जहाँ चाह, वहाँ राह]।', 'लोकोक्ति'),
    ('दूर के ढोल सुहावने', 'दूर की चीज़ें अच्छी लगती हैं', 'विदेश में रहना आसान लगता था, पर वहाँ जाकर समझ आया कि [दूर के ढोल सुहावने] होते हैं।', 'लोकोक्ति'),
]


def g_idioms(bank, label):
    def gen(kit, key, th):
        def meaning(rng, slot):
            i, m, s, k = rng.choice(bank)
            others = [x[1] for x in bank if x[0] != i]
            return mcq(rng, f'{k} ‘{i}’ का सही अर्थ क्या है?', m, rng.sample(others, 3), f'‘{i}’ — {m}।')
        kit.add(key, 'C1', (1, 3), meaning, 'mcq', 'p2r', 'id_mean')

        def rev(rng, slot):
            i, m, s, k = rng.choice(bank)
            others = [x[0] for x in bank if x[0] != i and x[3] == k]
            return mcq(rng, f'इस अर्थ के लिए सही {k} चुनिए: “{m}”', i, rng.sample(others, 3), f'‘{m}’ के लिए ‘{i}’।')
        kit.add(key, 'C1', (1, 3), rev, 'mcq', None, 'id_rev')

        def ctx(rng, slot):
            i, m, s, k = rng.choice(bank)
            sent = s.replace('[', '‘').replace(']', '’')
            return dict(stem=f'इस वाक्य में प्रयुक्त {k} का अर्थ स्पष्ट कीजिए और बताइए कि वक्ता इसके माध्यम से क्या भाव व्यक्त कर रहा है:\n“{sent}”',
                        answer=f'‘{i}’ = {m}। वक्ता का भाव संदर्भ से स्पष्ट हो।', type='explain', marks=2,
                        markingKey=f'1 अंक अर्थ ({m}); 1 अंक संदर्भ में भाव/प्रभाव की व्याख्या।')
        kit.add(key, 'C2', (1, 4), ctx, 'explain', None, 'id_ctx')

        def gap(rng, slot):
            pv = [x for x in bank if x[3] == 'लोकोक्ति']
            i, m, s, k = rng.choice(pv)
            blank = s.split('[')[0] + '____' + s.split(']')[1]
            others = [x[0] for x in pv if x[0] != i]
            return mcq(rng, f'उपयुक्त लोकोक्ति से रिक्त स्थान भरिए:\n“{blank}”', i, rng.sample(others, 3), f'स्थिति का भाव है — {m}; इसलिए ‘{i}’।')
        kit.add(key, 'C3', (1, 4), gap, 'mcq', 'p2r', 'id_gap')

        def use(rng, slot):
            i, m, s, k = rng.choice(bank)
            topic = rng.choice(th['topics'])
            return dict(stem=f'{k} ‘{i}’ का ‘{topic}’ विषय से जुड़े किसी प्रसंग में ऐसा वाक्य-प्रयोग कीजिए जिससे उसका अर्थ स्पष्ट हो जाए।',
                        answer=f'अर्थ: {m}। नमूना: {s.replace("[", "").replace("]", "")}', type='short', marks=2,
                        markingKey=f'1 अंक अर्थ के अनुरूप प्रसंग, 1 अंक {k} का शुद्ध (आवश्यकतानुसार रूपांतरित) प्रयोग; केवल अर्थ लिखने पर 1 अंक से अधिक नहीं।')
        kit.add(key, 'C3', (2, 4), use, 'short', None, 'id_use')

        def story(rng, slot):
            three = rng.sample(bank, 3)
            topic = rng.choice(th['topics'])
            return dict(stem=f'‘{topic}’ विषय पर 100–120 शब्दों की एक छोटी कहानी या प्रसंग लिखिए जिसमें इन तीनों का सार्थक प्रयोग हो: {"; ".join(x[0] for x in three)}।',
                        answer='अपेक्षित: ' + '; '.join(f'{x[0]} ({x[1]})' for x in three) + ' — तीनों का अर्थ के अनुरूप, स्वाभाविक प्रयोग; कहानी में आरंभ, घटना और अंत।', type='long', marks=6,
                        markingKey=para_key(6, 'प्रत्येक मुहावरे/लोकोक्ति का अर्थपूर्ण प्रयोग आवश्यक; ज़बरदस्ती ठूँसे गए प्रयोग पर भाषा के अंक घटाएँ।'))
        kit.add(key, 'C4', (2, 5), story, 'long', None, 'id_story')
    return gen


SPEC['ch07-st1'] = ('vocab', dict(focus='लेखन में त्योहारों, संस्कारों और पारिवारिक समारोहों से जुड़ी सटीक शब्दावली का प्रयोग कीजिए।', items=[
    ('C1', 'जन्म के बाद शिशु को नाम देने के संस्कार को क्या कहते हैं?', 'नामकरण', ['मुंडन', 'गृह-प्रवेश', 'विदाई'], 'नामकरण संस्कार में शिशु का नाम रखा जाता है।'),
    ('C1', 'पंजाब में फ़सल-कटाई से जुड़ा, जनवरी में अलाव जलाकर मनाया जाने वाला त्योहार कौन-सा है?', 'लोहड़ी', ['ओणम', 'बिहू', 'पोंगल'], 'लोहड़ी पंजाब में 13 जनवरी के आस-पास मनाई जाती है; ओणम केरल, बिहू असम, पोंगल तमिलनाडु का फ़सल-उत्सव है।'),
    ('C1', 'रमज़ान के महीने के बाद मनाया जाने वाला त्योहार कौन-सा है?', 'ईद-उल-फ़ित्र', ['बैसाखी', 'क्रिसमस', 'नवरोज़'], 'ईद-उल-फ़ित्र रमज़ान के रोज़ों के बाद मनाई जाती है।'),
    ('C2', '‘परंपरा’ और ‘अंधविश्वास’ में अंतर स्पष्ट कीजिए।', 'परंपरा पीढ़ियों से चली आ रही रीति है जिसमें प्रायः सांस्कृतिक या सामाजिक अर्थ होता है (जैसे बड़ों का आशीर्वाद लेना); अंधविश्वास बिना तर्क या प्रमाण का विश्वास है जो कभी-कभी हानिकारक होता है।', '1-1 अंक प्रत्येक अर्थ, 1 अंक उदाहरण सहित अंतर।', 3),
]))
SPEC['ch07-st2'] = ('reading', dict(focus='लेखन में परंपरा और आधुनिकता के बीच संतुलन पर अपने विचार उदाहरणों सहित दीजिए।', items=[
    ('C1', 'संपादकीय में लेखक का मत प्रायः कहाँ सबसे स्पष्ट होता है?', 'अंतिम अनुच्छेद या निष्कर्ष में', ['केवल शीर्षक के नीचे लेखक के नाम में', 'चित्र के कैप्शन में', 'विज्ञापन वाले हिस्से में'], 'संपादकीय का निष्कर्ष प्रायः समाज से अपील या स्पष्ट मत के रूप में होता है।'),
    ('C2', 'परंपरा और आधुनिकता पर लिखे लेखों में लेखक ‘संतुलन’ की बात क्यों करते हैं?', 'क्योंकि पूरी तरह परंपरा से चिपके रहना बदलाव और सुधार को रोकता है, जबकि पूरी तरह छोड़ देना पहचान और सामुदायिक जुड़ाव मिटा सकता है; संतुलन उपयोगी परंपराएँ बचाते हुए हानिकारक पक्ष बदलने देता है।', '1 अंक प्रत्येक अति के ख़तरे, 1 अंक संतुलन का लाभ।', 3),
]))
SPEC['ch07-st3'] = ('oral', dict(focus='लेखन में किसी चित्र या दृश्य का वर्णन करते हुए उसे परंपरा और संस्कृति से जोड़िए।', items=[
    ('C1', 'चित्र-आधारित मौखिक प्रस्तुति की शुरुआत के लिए सबसे उपयुक्त वाक्य कौन-सा है?', 'इस चित्र में हम देख सकते हैं कि…', ['मुझे कुछ नहीं पता।', 'अंत में मैं कहना चाहूँगा…', 'प्रिय मित्र, नमस्ते।'], 'प्रस्तुति वर्णन से शुरू होती है, फिर विषय-संबंध और व्यक्तिगत विचार।'),
    ('C1', 'चित्र के अग्रभाग (सामने के हिस्से) का वर्णन करने के लिए उपयुक्त शब्द कौन-सा है?', 'सामने की ओर / अग्रभाग में', ['पृष्ठभूमि में', 'ऊपर दाएँ कोने में', 'चित्र के बाहर'], 'अग्रभाग = सामने का भाग; पृष्ठभूमि = पीछे का भाग।'),
    ('C2', 'मौखिक प्रस्तुति में चित्र का केवल वर्णन करना पर्याप्त क्यों नहीं है?', 'मानदंड B (संदेश) में चित्र को विषय-वस्तु (theme) और लक्ष्य-भाषा की संस्कृति से जोड़ना अपेक्षित है; केवल वर्णन से विश्लेषण, तुलना और व्यक्तिगत दृष्टिकोण नहीं दिखता।', '1 अंक मानदंड की अपेक्षा, 1 अंक विश्लेषण/संबंध का महत्व।'),
    ('C3', 'चित्र: एक मेले में झूले, चूड़ियों की दुकानें और कठपुतली का खेल। इस चित्र को ‘परंपरा और आधुनिकता’ से जोड़ते हुए तीन वाक्य बोलने के लिए लिखिए।', 'नमूना: “इस चित्र में एक पारंपरिक ग्रामीण मेला दिखाई दे रहा है। कठपुतली का खेल हमारी लोक-कला की परंपरा है, पर आज के बच्चे मोबाइल गेम्स की ओर अधिक आकर्षित हैं। मेरे विचार में ऐसे मेले लोक-कलाओं को जीवित रखने का अच्छा माध्यम हैं।”', '1 अंक वर्णन, 1 अंक विषय से संबंध, 1 अंक व्यक्तिगत विचार।', 3),
]))
SPEC['ch07-st4'] = ('grammar', dict(focus='लेखन में उपयुक्त मुहावरों और लोकोक्तियों का स्वाभाविक प्रयोग कीजिए।', gens=[g_idioms(IDIOMS, 'मुहावरे')], items=[
    ('C1', 'मुहावरे और लोकोक्ति में मुख्य अंतर क्या है?', 'मुहावरा वाक्यांश होता है जो वाक्य में प्रयोग होता है; लोकोक्ति अपने-आप में पूरा वाक्य होती है', ['मुहावरा हमेशा पूरा वाक्य होता है', 'लोकोक्ति का अर्थ हमेशा शाब्दिक होता है', 'दोनों में कोई अंतर नहीं'], 'मुहावरा: ‘नौ दो ग्यारह होना’ (वाक्यांश); लोकोक्ति: ‘जैसी करनी वैसी भरनी’ (स्वतंत्र वाक्य)।'),
    ('C2', 'मुहावरों का अर्थ प्रायः शाब्दिक क्यों नहीं होता? ‘नौ दो ग्यारह होना’ के उदाहरण से समझाइए।', 'मुहावरे का अर्थ रूढ़ (लाक्षणिक) होता है, शब्दों के जोड़ से नहीं निकलता; ‘नौ दो ग्यारह होना’ का गणित से कोई संबंध नहीं, इसका अर्थ है ‘भाग जाना’।', '1 अंक लाक्षणिक अर्थ की अवधारणा, 1 अंक उदाहरण।'),
    ('C2', 'पेपर 1 के लेखन में मुहावरों का प्रयोग कब प्रभावी और कब हानिकारक होता है?', 'प्रभावी: जब संदर्भ और रजिस्टर के अनुरूप, स्वाभाविक रूप से प्रयोग हो — भाषा समृद्ध दिखती है (मानदंड A)। हानिकारक: जब ज़बरदस्ती ठूँसा जाए, गलत अर्थ में या औपचारिक रिपोर्ट जैसे पाठ-प्रकार में अनुचित रूप से प्रयोग हो।', '1-1 अंक प्रत्येक स्थिति, 1 अंक उदाहरण या मानदंड से संबंध।', 3),
]))

# ---------------------------------------------------------------- ch08 प्रवासन
TH[8] = dict(
    name='प्रवासन',
    vocab=[
        ('प्रवासी', 'अपना देश या क्षेत्र छोड़कर दूसरी जगह बसने वाला व्यक्ति', 'आप्रवासी', 'दुबई में लाखों भारतीय ____ निर्माण और सेवा क्षेत्र में काम करते हैं।'),
        ('विस्थापन', 'मजबूरी में अपने घर से उजड़ जाना', 'उजड़ना', 'बाँध बनने से कई गाँवों का ____ हुआ।'),
        ('शरणार्थी', 'युद्ध या उत्पीड़न के कारण दूसरे देश में शरण लेने वाला व्यक्ति', 'शरणागत', '1947 के विभाजन के बाद लाखों ____ दिल्ली और पंजाब में बसे।'),
        ('पलायन', 'रोज़गार या संकट के कारण बड़ी संख्या में एक जगह से दूसरी जगह जाना', 'निष्क्रमण', 'सूखे के कारण गाँव से शहरों की ओर ____ बढ़ गया।'),
        ('मूल निवास', 'वह स्थान जहाँ से कोई व्यक्ति मूल रूप से है', 'पैतृक स्थान', 'उनका ____ बिहार है, पर वे पचास साल से कोलकाता में रहते हैं।'),
        ('अकेलापन', 'साथ न होने से होने वाला खालीपन', 'एकाकीपन', 'नए शहर में पहले कुछ महीने मुझे बहुत ____ महसूस हुआ।'),
        ('अनुकूलन', 'नई परिस्थितियों के अनुसार स्वयं को ढालना', 'सामंजस्य', 'विदेशी विद्यार्थियों को नई संस्कृति से ____ में समय लगता है।'),
        ('वीज़ा', 'किसी दूसरे देश में प्रवेश और ठहरने की आधिकारिक अनुमति', 'प्रवेश-अनुमति', 'पढ़ाई के लिए कनाडा जाने हेतु उसे छात्र ____ चाहिए।'),
        ('प्रेषित धन', 'विदेश में काम करने वालों द्वारा घर भेजा गया पैसा', 'रेमिटेंस', 'केरल के कई परिवारों की आय खाड़ी देशों से आने वाले ____ पर निर्भर है।'),
        ('जड़ें', 'किसी स्थान, संस्कृति या परिवार से गहरा मूल संबंध', 'मूल', 'विदेश में जन्मी होने पर भी उसे अपनी ____ से गहरा लगाव है।'),
        ('भेदभाव', 'किसी के साथ अनुचित, असमान व्यवहार', 'पक्षपात', 'कई प्रवासी मज़दूरों को भाषा के कारण ____ का सामना करना पड़ता है।'),
        ('गिरमिटिया', 'अनुबंध (एग्रीमेंट) पर विदेश भेजे गए उन्नीसवीं सदी के भारतीय मज़दूर', 'अनुबंधित श्रमिक', 'मॉरीशस और फ़िजी में ____ मज़दूरों के वंशज आज भी भोजपुरी गीत गाते हैं।'),
        ('महानगर', 'बहुत बड़ा और घनी आबादी वाला शहर', 'मेट्रो शहर', 'रोज़गार की तलाश में हर साल लाखों लोग ____ आते हैं।'),
        ('घर की याद', 'घर से दूर रहने पर घर-परिवार को याद करके होने वाली उदासी', 'गृह-विरह', 'त्योहारों पर प्रवासी विद्यार्थियों को ____ सबसे ज़्यादा सताती है।'),
    ],
    topics=['गाँव से शहर की ओर पलायन', 'विदेश में पढ़ाई के अनुभव', 'प्रवासी भारतीय और उनकी पहचान', 'नए शहर में अकेलापन',
            'प्रवासी मज़दूरों की समस्याएँ', 'घर की याद', 'प्रवास से मिले अवसर'],
    texts=[
        dict(kind='लेख', title='गिरमिटिया की यादें: मॉरीशस का आप्रवासी घाट',
             body='मॉरीशस की राजधानी पोर्ट लुई में ‘आप्रवासी घाट’ नाम की एक साधारण-सी इमारत है, जिसे यूनेस्को ने 2006 में विश्व धरोहर घोषित किया। 1834 से उन्नीसवीं सदी के अंत तक लाखों भारतीय अनुबंधित मज़दूर यहीं की सीढ़ियाँ चढ़कर इस द्वीप पर पहुँचे। अधिकतर बिहार और पूर्वी उत्तर प्रदेश से आए ये ‘गिरमिटिया’ गन्ने के खेतों में कठिन परिस्थितियों में काम करते थे। आज उनके वंशज मॉरीशस की आबादी का बड़ा हिस्सा हैं और भोजपुरी लोकगीत, रामायण-पाठ और त्योहार अपनी जड़ों की याद दिलाते हैं।',
             qs=[('C1', 'यूनेस्को ने आप्रवासी घाट को विश्व धरोहर कब घोषित किया?', '2006 में', ['1834 में', '1947 में', '2016 में']),
                 ('C1', 'गिरमिटिया मज़दूर मॉरीशस में मुख्य रूप से कहाँ काम करते थे?', 'गन्ने के खेतों में'),
                 ('C1', 'अधिकतर गिरमिटिया मज़दूर भारत के किन क्षेत्रों से आए थे?', 'बिहार और पूर्वी उत्तर प्रदेश', ['पंजाब और हरियाणा', 'केरल और तमिलनाडु', 'गुजरात और राजस्थान']),
                 ('C2', 'लेखक ने आप्रवासी घाट को ‘साधारण-सी इमारत’ क्यों कहा, जबकि वह विश्व धरोहर है?', 'इमारत दिखने में भव्य नहीं है, पर उसका ऐतिहासिक और भावनात्मक महत्व बहुत बड़ा है — यह विरोधाभास बताता है कि धरोहर का मूल्य उसकी कहानी में है, सुंदरता में नहीं।'),
                 ('tf', 'गिरमिटिया मज़दूरों के वंशज आज मॉरीशस की आबादी का बहुत छोटा हिस्सा हैं।', 'गलत', '“आज उनके वंशज मॉरीशस की आबादी का बड़ा हिस्सा हैं।”'),
                 ('C3', 'वंशजों के लिए भोजपुरी लोकगीत और रामायण-पाठ का क्या महत्व है?', 'वे अपनी मूल संस्कृति और पूर्वजों की पहचान से जुड़े रहने का माध्यम हैं', ['वे केवल मनोरंजन के लिए हैं', 'वे सरकारी नियमों के कारण होते हैं', 'वे गन्ने की खेती से जुड़े हैं']),
                 ('C3', '“यहीं की सीढ़ियाँ चढ़कर” — यह विवरण पाठक के मन में कैसा चित्र बनाता है?', 'हज़ारों थके, अनिश्चित भविष्य वाले मज़दूरों के नए देश में पहला कदम रखने का भावनात्मक, ऐतिहासिक दृश्य — सीढ़ियाँ नई ज़िंदगी की शुरुआत और कठिन यात्रा का प्रतीक बनती हैं।'),
                 ('C4', 'आज के आर्थिक प्रवासन (जैसे खाड़ी देशों में भारतीय मज़दूर) और गिरमिटिया प्रवास में क्या समानताएँ और अंतर हैं? लेख और अपने ज्ञान के आधार पर विवेचना कीजिए।', 'समानताएँ: रोज़गार के लिए प्रवास, कठिन श्रम, परिवार से दूरी, घर की याद। अंतर: आज अधिक क़ानूनी अधिकार, संचार और वापसी की सुविधा, पर पासपोर्ट ज़ब्ती जैसी समस्याएँ भी। संतुलित निष्कर्ष।')]),
        dict(kind='अनौपचारिक पत्र', title='बेंगलुरु से माँ के नाम',
             body='बेंगलुरु, 20 जुलाई\nप्यारी माँ,\nयहाँ नौकरी को तीन महीने हो गए। ऑफ़िस अच्छा है, पर शाम को कमरे में लौटकर सन्नाटा चुभता है। यहाँ के लोग कन्नड़ बोलते हैं; मैंने कुछ शब्द सीख लिए हैं — ‘नमस्कार’, ‘धन्यवाद’ के लिए ‘धन्यवादगळु’। मकान-मालकिन अम्मा कभी-कभी रसम-चावल खिला देती हैं, तब घर जैसा लगता है। तुम्हारे हाथ की अरहर दाल की बहुत याद आती है। दिवाली पर ज़रूर आऊँगा।\nतुम्हारा राजू',
             qs=[('C1', 'राजू को बेंगलुरु में नौकरी करते हुए कितना समय हुआ है?', 'तीन महीने', ['तीन साल', 'तीन सप्ताह', 'एक साल']),
                 ('C1', 'मकान-मालकिन अम्मा राजू को क्या खिलाती हैं?', 'रसम-चावल'),
                 ('C2', '“शाम को कमरे में लौटकर सन्नाटा चुभता है” — इस वाक्य से राजू की किस भावना का पता चलता है?', 'गहरे अकेलेपन और घर की याद का; दिन में काम में व्यस्त रहने के बाद ख़ाली कमरा उसे परिवार की कमी का दर्द महसूस कराता है।'),
                 ('tf', 'राजू ने कन्नड़ भाषा का एक भी शब्द नहीं सीखा है।', 'गलत', '“मैंने कुछ शब्द सीख लिए हैं…”'),
                 ('C3', 'राजू के कन्नड़ शब्द सीखने से उसके किस प्रयास का पता चलता है?', 'नई जगह की संस्कृति के साथ अनुकूलन करने का', ['घर लौटने की तैयारी का', 'नौकरी बदलने का', 'मकान-मालकिन से झगड़े का']),
                 ('C3', 'पत्र में ‘भोजन’ किस प्रकार घर और नई जगह, दोनों से राजू के संबंध को दिखाता है?', 'रसम-चावल नई जगह के लोगों की आत्मीयता और अपनापन दिखाता है; अरहर दाल माँ और घर की याद का प्रतीक है — भोजन भावनात्मक जुड़ाव का माध्यम है।'),
                 ('C4', 'राजू के अनुभव के आधार पर बताइए कि नए शहर में बसने वाले युवाओं के लिए अकेलेपन से निपटने के सबसे प्रभावी उपाय क्या हो सकते हैं।', 'स्थानीय भाषा सीखना (राजू का उदाहरण), पड़ोसियों/सहकर्मियों से संबंध (अम्मा), परिवार से नियमित संपर्क, शौक़ और समुदाय-समूह; पत्र से प्रमाण और व्यावहारिक सुझाव।')]),
        dict(kind='समाचार रिपोर्ट', title='प्रवासी भारतीय दिवस पर युवाओं का सम्मेलन',
             body='नई दिल्ली, 9 जनवरी। प्रवासी भारतीय दिवस के अवसर पर आज राजधानी में विश्व के तीस देशों से आए युवा प्रवासी भारतीयों का सम्मेलन हुआ। यह दिवस 1915 में महात्मा गांधी के दक्षिण अफ़्रीका से भारत लौटने की याद में मनाया जाता है। सम्मेलन में फ़िजी की छात्रा अनीता प्रसाद ने कहा कि उनकी पीढ़ी हिंदी गीतों और फ़िल्मों से भारत को जानती है। आयोजकों ने बताया कि अगले वर्ष से युवाओं के लिए ऑनलाइन हिंदी पाठ्यक्रम शुरू किया जाएगा।',
             qs=[('C1', 'प्रवासी भारतीय दिवस किस घटना की याद में मनाया जाता है?', '1915 में गांधीजी के दक्षिण अफ़्रीका से भारत लौटने की', ['भारत की स्वतंत्रता की', 'संविधान लागू होने की', 'पहले गिरमिटिया जहाज़ के पहुँचने की']),
                 ('C1', 'सम्मेलन में कितने देशों से युवा आए?', 'तीस'),
                 ('C2', 'अनीता प्रसाद के कथन से प्रवासी युवाओं और भारत के संबंध के बारे में क्या पता चलता है?', 'नई प्रवासी पीढ़ी का भारत से संबंध प्रत्यक्ष अनुभव से कम और लोकप्रिय संस्कृति (हिंदी गीत, फ़िल्में) के माध्यम से अधिक है।'),
                 ('tf', 'ऑनलाइन हिंदी पाठ्यक्रम इसी वर्ष से शुरू हो चुका है।', 'गलत', '“अगले वर्ष से… ऑनलाइन हिंदी पाठ्यक्रम शुरू किया जाएगा।”'),
                 ('C3', 'रिपोर्ट के पहले वाक्य से पाठक को कौन-सी जानकारी तुरंत मिल जाती है?', 'कब, कहाँ, क्या और कौन — 9 जनवरी, नई दिल्ली, युवा प्रवासी भारतीयों का सम्मेलन', ['केवल लेखक की राय', 'गांधीजी की पूरी जीवनी', 'पाठ्यक्रम का शुल्क']),
                 ('C3', 'इस अंश में समाचार रिपोर्ट की कौन-सी दो विशेषताएँ दिखाई देती हैं? उदाहरण सहित लिखिए।', 'स्थान-दिनांक-पंक्ति (‘नई दिल्ली, 9 जनवरी’); पहले वाक्य में मुख्य तथ्य; उद्धृत कथन (अनीता प्रसाद); तृतीय पुरुष में निष्पक्ष भाषा; कर्मवाच्य (‘मनाया जाता है’, ‘शुरू किया जाएगा’)।'),
                 ('C4', 'क्या ऑनलाइन पाठ्यक्रम प्रवासी युवाओं को भारतीय भाषा और संस्कृति से जोड़ने के लिए पर्याप्त हैं? रिपोर्ट के आधार पर मूल्यांकन कीजिए।', 'पक्ष: दूर बैठे युवाओं तक पहुँच, सस्ता, लचीला। सीमाएँ: बोलने का अभ्यास और सांस्कृतिक अनुभव कम; परिवार और समुदाय की भूमिका ज़रूरी। निष्कर्ष: ऑनलाइन + सांस्कृतिक आदान-प्रदान कार्यक्रम।')]),
    ],
    audio=[
        dict(kind='रेडियो वृत्तचित्र', title='‘गाँव से शहर की ओर’ — भाग 1',
             body='उद्घोषक: बुंदेलखंड के एक गाँव में सुबह के छह बजे हैं। बस-अड्डे पर बीस-पच्चीस युवक बोरियाँ लिए खड़े हैं।\nरामकिशन (बत्तीस वर्ष): तीन साल से बारिश ठीक नहीं हुई। खेत में कुछ नहीं उगता। दिल्ली में ईंट-भट्ठे पर काम मिल जाता है, महीने के बारह-तेरह हज़ार।\nउद्घोषक: गाँव में अब ज़्यादातर बुज़ुर्ग, महिलाएँ और बच्चे बचे हैं।\nसावित्री (रामकिशन की पत्नी): खेत, पशु, बच्चों की पढ़ाई — सब मुझे ही देखना पड़ता है। वह होली पर आता है, बस।',
             qs=[('C1', 'गाँव के युवक काम की तलाश में कहाँ जाते हैं?', 'दिल्ली', ['मुंबई', 'विदेश', 'पास के क़स्बे']),
                 ('C1', 'रामकिशन को महीने में लगभग कितना मिलता है?', 'बारह-तेरह हज़ार रुपये', ['पाँच हज़ार रुपये', 'पचास हज़ार रुपये', 'तीस हज़ार रुपये']),
                 ('C1', 'रामकिशन के अनुसार गाँव छोड़ने का मुख्य कारण क्या है?', 'तीन साल से बारिश ठीक न होना / खेती न हो पाना'),
                 ('C2', 'सावित्री के कथन से पलायन के किस प्रभाव का पता चलता है? समझाइए।', 'पुरुषों के जाने से गाँव में रह गई महिलाओं पर खेती, पशु और बच्चों की पढ़ाई का पूरा बोझ आ जाता है; परिवार साल में बहुत कम समय साथ रह पाता है।'),
                 ('tf', 'गाँव में अब अधिकतर युवा पुरुष रहते हैं।', 'गलत', '“गाँव में अब ज़्यादातर बुज़ुर्ग, महिलाएँ और बच्चे बचे हैं।”'),
                 ('C3', 'वृत्तचित्र की शुरुआत बस-अड्डे के दृश्य से क्यों की गई है?', 'श्रोता को तुरंत पलायन के यथार्थ दृश्य से जोड़ने के लिए', ['बसों का विज्ञापन करने के लिए', 'मौसम की जानकारी देने के लिए', 'होली के त्योहार का वर्णन करने के लिए']),
                 ('C3', 'इस अंश में पलायन के ‘धक्का देने वाले’ (गाँव से निकालने वाले) और ‘खींचने वाले’ (शहर की ओर ले जाने वाले) कारण पहचानिए।', 'धक्का: बारिश की कमी, खेती से आय न होना। खिंचाव: दिल्ली में ईंट-भट्ठे पर काम और नियमित मज़दूरी (बारह-तेरह हज़ार)।'),
                 ('C4', 'सरकार और समाज क्या करें कि ग्रामीण युवाओं को मजबूरी में पलायन न करना पड़े? वृत्तचित्र के तथ्यों से जोड़ते हुए सुझाव दीजिए।', 'जल-संरक्षण और सिंचाई (सूखे का समाधान), ग्रामीण रोज़गार योजनाएँ, कौशल-प्रशिक्षण, स्थानीय उद्योग; महिलाओं के लिए सहायता। तथ्यों (बारिश, मज़दूरी, अकेली महिलाएँ) से स्पष्ट संबंध।')]),
        dict(kind='रेडियो वृत्तचित्र', title='‘गाँव से शहर की ओर’ — भाग 2: शहर की कहानी',
             body='उद्घोषक: दिल्ली के बाहरी इलाक़े की एक बस्ती। एक कमरे में छह लोग रहते हैं।\nरामकिशन: यहाँ पानी ख़रीदना पड़ता है। कभी मालिक समय पर पैसे नहीं देता। पर गाँव से अच्छा है — बच्चे की फ़ीस तो भर पाता हूँ।\nउद्घोषक: एक स्वयंसेवी संस्था ‘साथी’ यहाँ प्रवासी मज़दूरों को उनके अधिकारों और सरकारी योजनाओं के बारे में बताती है।\nसंस्था की कार्यकर्ता नसरीन: बहुत-से मज़दूरों के पास पहचान-पत्र नहीं होते, इसलिए उन्हें राशन तक नहीं मिलता। हम उनके काग़ज़ बनवाने में मदद करते हैं।',
             qs=[('C1', 'बस्ती के एक कमरे में कितने लोग रहते हैं?', 'छह', ['दो', 'दस', 'बारह']),
                 ('C1', 'स्वयंसेवी संस्था का नाम क्या है?', '‘साथी’'),
                 ('C2', 'रामकिशन कठिनाइयों के बावजूद शहर को गाँव से बेहतर क्यों मानता है?', 'क्योंकि शहर में मिलने वाली मज़दूरी से वह अपने बच्चे की फ़ीस भर पाता है — बच्चे का भविष्य उसके लिए अपनी कठिनाइयों से अधिक महत्वपूर्ण है।'),
                 ('tf', 'बस्ती में पानी मुफ़्त मिलता है।', 'गलत', '“यहाँ पानी ख़रीदना पड़ता है।”'),
                 ('C3', 'नसरीन के अनुसार पहचान-पत्र न होने का सबसे बड़ा परिणाम क्या है?', 'मज़दूरों को राशन और सरकारी सुविधाएँ नहीं मिल पातीं', ['मज़दूर गाँव नहीं लौट पाते', 'मज़दूरों की मज़दूरी बढ़ जाती है', 'मज़दूर बस में यात्रा नहीं कर सकते']),
                 ('C3', 'भाग 1 और भाग 2 को साथ सुनने पर पलायन की कौन-सी दोहरी तस्वीर बनती है?', 'गाँव में: परिवार का बिखराव और महिलाओं पर बोझ; शहर में: भीड़-भरे कमरे, पानी ख़रीदना, शोषण — फिर भी आय और बच्चों की पढ़ाई की आशा। पलायन मजबूरी और अवसर, दोनों है।'),
                 ('C4', '“प्रवासी मज़दूर शहरों को बनाते हैं, पर शहर उन्हें अपनाते नहीं।” — इस वृत्तचित्र के आधार पर इस कथन का मूल्यांकन कीजिए।', 'पक्ष: भट्ठों और निर्माण में श्रम, पर भीड़ भरे कमरे, पानी ख़रीदना, पहचान-पत्र और राशन से वंचित, देर से मज़दूरी। विपक्ष/जटिलता: रोज़गार और शिक्षा के अवसर, ‘साथी’ जैसी संस्थाएँ। संतुलित निष्कर्ष।')]),
        dict(kind='पॉडकास्ट', title='‘दो देश, एक दिल’ — विदेश में पढ़ने वाले विद्यार्थी की बातें',
             body='नमस्ते दोस्तो, मैं हूँ ज़ोया, और मैं पिछले दो साल से जर्मनी के म्यूनिख़ शहर में इंजीनियरिंग पढ़ रही हूँ। पहले छह महीने बहुत कठिन थे — भाषा नहीं आती थी, सर्दियों में शाम चार बजे ही अँधेरा हो जाता था, और खाने में मिर्च का नामो-निशान नहीं! फिर मैंने जर्मन भाषा की शाम की कक्षाएँ शुरू कीं और विश्वविद्यालय के भारतीय छात्र-संघ से जुड़ी। अब मेरे जर्मन दोस्त मेरे हाथ की बिरयानी के दीवाने हैं। मेरी सलाह? नई भाषा से डरिए मत, वही दरवाज़ा खोलती है।',
             qs=[('C1', 'ज़ोया जर्मनी के किस शहर में पढ़ रही है?', 'म्यूनिख़', ['बर्लिन', 'हैम्बर्ग', 'फ़्रैंकफ़र्ट']),
                 ('C1', 'ज़ोया क्या पढ़ रही है?', 'इंजीनियरिंग'),
                 ('C2', 'ज़ोया के लिए पहले छह महीने कठिन क्यों थे? तीन कारण लिखिए।', 'भाषा न आना; सर्दियों में जल्दी अँधेरा होना; भोजन का स्वाद अलग (मिर्च न होना)।'),
                 ('tf', 'ज़ोया के जर्मन दोस्तों को भारतीय खाना पसंद नहीं है।', 'गलत', '“मेरे जर्मन दोस्त मेरे हाथ की बिरयानी के दीवाने हैं।”'),
                 ('C3', 'ज़ोया ने नए देश में अनुकूलन के लिए कौन-से दो कदम उठाए?', 'जर्मन भाषा की कक्षाएँ और भारतीय छात्र-संघ से जुड़ना', ['नौकरी छोड़ना और घर लौटना', 'केवल भारतीय दोस्त बनाना', 'विश्वविद्यालय बदलना']),
                 ('C3', '“नई भाषा… वही दरवाज़ा खोलती है” — ज़ोया के अनुभव से इस रूपक की व्याख्या कीजिए।', 'भाषा सीखने के बाद ही उसके नए दोस्त बने और वह स्थानीय समाज से जुड़ पाई (जर्मन दोस्त, बिरयानी); भाषा नए संबंधों और अवसरों तक पहुँचने का रास्ता है।'),
                 ('C4', 'विदेश में पढ़ाई के लाभ और चुनौतियों का मूल्यांकन ज़ोया के अनुभव और अपने विचारों के आधार पर कीजिए।', 'लाभ: वैश्विक शिक्षा, स्वावलंबन, बहुसांस्कृतिक मित्रता। चुनौतियाँ: भाषा, अकेलापन, जलवायु, भोजन, ख़र्च। ज़ोया के उदाहरण और संतुलित निष्कर्ष।')]),
    ],
    tasks=[
        ('आप विदेश के एक विश्वविद्यालय में दाख़िला लेने वाले हैं, पर छात्रावास के बारे में आपको जानकारी नहीं मिली है।', 'email',
         ['आपका परिचय और दाख़िले का विवरण', 'छात्रावास, भोजन और सुरक्षा से जुड़े प्रश्न', 'उत्तर की अपेक्षा और धन्यवाद']),
        ('आपके शहर में प्रवासी मज़दूरों के बच्चों के लिए विद्यालय की सुविधा नहीं है। आप ज़िला शिक्षा अधिकारी को लिखना चाहते हैं।', 'fletter',
         ['समस्या और प्रभावित बच्चों की स्थिति', 'शिक्षा के अधिकार का उल्लेख', 'ठोस सुझाव और अनुरोध']),
        ('आपका परिवार हाल ही में दूसरे देश में बसा है। आप अपने अनुभवों पर ब्लॉग लिखना चाहते हैं।', 'blog',
         ['पहले कुछ सप्ताह के अनुभव', 'सबसे बड़ी चुनौती और उससे निपटना', 'नए प्रवासियों के लिए सुझाव']),
        ('विद्यालय-पत्रिका के लिए आपको किसी ऐसे व्यक्ति का साक्षात्कार लेना है जो चालीस साल पहले दूसरे देश में जाकर बसे थे।', 'interview',
         ['प्रवास के कारण और यात्रा', 'नई जगह में संघर्ष', 'अपनी जड़ों से संबंध आज कैसे बनाए रखते हैं']),
        ('आपकी कक्षा ‘प्रवास: अवसर या संकट?’ विषय पर वाद-विवाद कर रही है।', 'speech',
         ['प्रवास के अवसर', 'प्रवास की चुनौतियाँ', 'आपका संतुलित मत']),
        ('आपके एक मित्र का परिवार दूसरे शहर में जा रहा है और वह बहुत दुखी है।', 'pletter',
         ['उसकी भावनाओं के प्रति सहानुभूति', 'नए शहर के संभावित अच्छे पक्ष', 'संपर्क बनाए रखने के तरीके']),
    ],
    discuss=[
        ('क्या प्रवास से व्यक्ति अपनी संस्कृति खो देता है या नई संस्कृति पाता है?', ['भाषा और परंपराओं से दूरी', 'मिश्रित पहचान और नई दृष्टि', 'परिवार और समुदाय की भूमिका']),
        ('क्या प्रतिभाशाली युवाओं का विदेश जाना (प्रतिभा-पलायन) देश के लिए हानिकारक है?', ['देश में कुशल लोगों की कमी', 'प्रेषित धन और वैश्विक संपर्क', 'देश में अवसर बढ़ाने की ज़रूरत']),
        ('क्या शहरों को प्रवासी मज़दूरों के लिए बेहतर सुविधाएँ देनी चाहिए?', ['शहरों के निर्माण में उनका योगदान', 'संसाधनों और भीड़ का दबाव', 'मानवाधिकार और गरिमा']),
        ('क्या दूसरी पीढ़ी के प्रवासियों को मातृभाषा सीखना ज़रूरी है?', ['परिवार और जड़ों से जुड़ाव', 'स्थानीय भाषा में दक्षता का दबाव', 'बहुभाषी होने के लाभ']),
        ('क्या आप भविष्य में पढ़ाई या काम के लिए विदेश जाना चाहेंगे? क्यों?', ['बेहतर शिक्षा और अनुभव', 'परिवार और संस्कृति से दूरी', 'लौटकर देश के लिए योगदान']),
    ],
    pics=[('एक हवाई अड्डे पर एक युवती बड़ा सूटकेस लिए खड़ी है; माता-पिता उसे गले लगा रहे हैं और छोटा भाई रो रहा है। पीछे बोर्ड पर लिखा है: “अंतरराष्ट्रीय प्रस्थान”।',
           ['पढ़ाई या काम के लिए प्रवास', 'परिवार से विदा की भावनाएँ', 'नई ज़िंदगी की आशाएँ और डर'])],
)

SPEC['ch08-st1'] = ('reading', dict(focus='लेखन में प्रवास के अनुभवों को भावनात्मक और तथ्यात्मक, दोनों दृष्टियों से प्रस्तुत कीजिए।', items=[
    ('C1', 'मॉरीशस में हर साल 2 नवंबर को ‘आप्रवासी दिवस’ किस घटना की याद में मनाया जाता है?', '1834 में भारतीय अनुबंधित मज़दूरों के पहले दल के पहुँचने की', ['मॉरीशस की स्वतंत्रता की', 'गांधीजी की मॉरीशस यात्रा की', 'हिंदी दिवस की'], 'आप्रवासी दिवस गिरमिटिया मज़दूरों के आगमन की स्मृति में है।'),
    ('C1', '‘भारतवंशी’ शब्द किसके लिए प्रयोग होता है?', 'भारतीय मूल के वे लोग जो पीढ़ियों से दूसरे देशों में बसे हैं', ['केवल भारत में रहने वाले लोग', 'भारत आने वाले विदेशी पर्यटक', 'भारत के सरकारी कर्मचारी'], 'भारतवंशी = भारतीय मूल के, विदेश में बसे लोग।'),
    ('C2', '‘प्रवासी’ और ‘शरणार्थी’ में अंतर स्पष्ट कीजिए।', 'प्रवासी सामान्यतः रोज़गार, शिक्षा या बेहतर जीवन के लिए स्वेच्छा से दूसरी जगह जाता है; शरणार्थी युद्ध, उत्पीड़न या संकट के कारण जान बचाने के लिए मजबूरी में देश छोड़ता है और सुरक्षा माँगता है।', '1-1 अंक प्रत्येक अर्थ, 1 अंक स्वेच्छा/मजबूरी के अंतर पर।', 3),
]))
SPEC['ch08-st2'] = ('writing', dict(tt='fletter', tasks=[
    ('आप नए शहर में आए प्रवासी परिवार के सदस्य हैं। आपके क्षेत्र में राशन-कार्ड बनवाने की प्रक्रिया बहुत कठिन है। ज़िला आपूर्ति अधिकारी को पत्र लिखिए।', ['आपकी स्थिति और समस्या', 'प्रक्रिया में आने वाली कठिनाइयाँ', 'सरलीकरण के सुझाव और अनुरोध']),
    ('आपके विद्यालय में दूसरे राज्यों से आए विद्यार्थियों के लिए भाषा-सहायता की कोई व्यवस्था नहीं है। प्रधानाचार्य को पत्र लिखिए।', ['ऐसे विद्यार्थियों की कठिनाइयाँ', 'प्रस्तावित भाषा-सहायता कार्यक्रम', 'आपकी ओर से सहयोग']),
    ('आपके मोहल्ले में प्रवासी मज़दूरों के साथ भाषा के कारण दुर्व्यवहार की घटनाएँ बढ़ी हैं। स्थानीय समाचार-पत्र के संपादक को पत्र लिखिए।', ['घटनाओं का विवरण', 'यह व्यवहार क्यों अनुचित है', 'समाज और प्रशासन से अपेक्षाएँ']),
    ('आप विदेश में पढ़ाई के लिए छात्रवृत्ति चाहते हैं। छात्रवृत्ति-समिति के अध्यक्ष को आवेदन-पत्र लिखिए।', ['आपकी शैक्षिक योग्यता', 'आप विदेश क्यों पढ़ना चाहते हैं', 'लौटकर आप देश के लिए क्या करेंगे']),
    ('आपके शहर के रेलवे स्टेशन पर प्रवासी मज़दूरों के लिए प्रतीक्षालय और पीने के पानी की व्यवस्था नहीं है। स्टेशन-अधीक्षक को पत्र लिखिए।', ['समस्या और उसका प्रभाव', 'त्योहारों के समय की भीड़', 'सुझाव और अनुरोध']),
], items=[
    ('C1', 'औपचारिक पत्र में ‘विषय’ पंक्ति कहाँ लिखी जाती है?', 'संबोधन (महोदय/महोदया) से पहले', ['पत्र के अंत में हस्ताक्षर के बाद', 'प्रेषक के पते से पहले', 'पत्र में विषय-पंक्ति नहीं होती'], 'क्रम: प्रेषक का पता, दिनांक, प्राप्तकर्ता, विषय, संबोधन, मुख्य भाग, समापन।'),
    ('C1', 'औपचारिक पत्र के समापन के लिए सबसे उपयुक्त शब्द कौन-सा है?', 'भवदीय', ['तुम्हारा मित्र', 'प्यार सहित', 'जल्दी मिलेंगे'], '‘भवदीय/भवदीया’ औपचारिक समापन है।'),
    ('C2', 'औपचारिक पत्र और औपचारिक ईमेल के प्रारूप में दो अंतर बताइए।', 'पत्र में प्रेषक-प्राप्तकर्ता के पूरे पते और दिनांक ऊपर लिखे जाते हैं, ईमेल में ‘प्रति’ और ‘विषय’ फ़ील्ड होते हैं; ईमेल प्रायः अधिक संक्षिप्त होता है और उसमें संलग्नक का उल्लेख हो सकता है, अंत में नाम-पद-संपर्क विवरण।', '1-1 अंक प्रत्येक अंतर।'),
], gens=[lambda kit, key, th: kit.writing(key, th, 'email', [
    ('आपने ऑनलाइन वीज़ा-आवेदन जमा किया था, पर तीन सप्ताह से कोई सूचना नहीं मिली।', ['आवेदन का विवरण और संदर्भ-संख्या', 'देरी से होने वाली कठिनाई', 'शीघ्र कार्रवाई का अनुरोध']),
    ('आप एक अंतरराष्ट्रीय विद्यार्थी हैं और विश्वविद्यालय के छात्र-सहायता केंद्र से अंशकालिक काम के नियमों के बारे में पूछना चाहते हैं।', ['आपका परिचय', 'नियमों से जुड़े विशिष्ट प्रश्न', 'मिलने का समय माँगना']),
    ('एक प्रवासी-सहायता संस्था स्वयंसेवक चाहती है। आप उसमें जुड़ना चाहते हैं।', ['आपका परिचय और रुचि', 'आपकी भाषाएँ और कौशल', 'आप कब उपलब्ध हैं']),
])]))
SPEC['ch08-st3'] = ('listening', dict(focus='लेखन में प्रवास (गाँव से शहर या एक देश से दूसरे देश) के कारणों और प्रभावों को स्पष्ट कीजिए।', items=[
    ('C1', 'रेडियो वृत्तचित्र की पहचान क्या है?', 'वास्तविक लोगों की आवाज़ों, उद्घोषक के विवरण और दृश्य जैसी ध्वनियों से किसी सच्चे विषय की पड़ताल', ['पूरी तरह काल्पनिक कहानी', 'केवल संगीत', 'किसी उत्पाद का विज्ञापन'], 'वृत्तचित्र तथ्यात्मक होता है और प्रत्यक्ष गवाहियों पर आधारित होता है।'),
    ('C2', 'वृत्तचित्र सुनते समय उद्घोषक के कथन और लोगों के निजी अनुभवों में अंतर पहचानना क्यों ज़रूरी है?', 'उद्घोषक संदर्भ और तथ्य देता है, जबकि लोग अपने निजी अनुभव और भावनाएँ बताते हैं; प्रश्न अक्सर पूछते हैं कि ‘किसने’ क्या कहा, इसलिए वक्ता की पहचान सही उत्तर के लिए आवश्यक है।', '1 अंक भूमिकाओं का अंतर, 1 अंक प्रश्नोत्तर से संबंध।'),
]))


# ---------------------------------------------------------------- ch09 मनोरंजन
TH[9] = dict(
    name='मनोरंजन',
    vocab=[
        ('समीक्षा', 'किसी कृति के गुण-दोषों का मूल्यांकन', 'आलोचना', 'अख़बार में नई फ़िल्म की ____ पढ़कर मैंने टिकट ख़रीदे।'),
        ('कथानक', 'कहानी या फ़िल्म की घटनाओं का क्रम', 'प्लॉट', 'फ़िल्म का ____ इतना कसा हुआ था कि एक पल भी ऊब नहीं हुई।'),
        ('अभिनय', 'पात्र को परदे या मंच पर जीवंत करना', 'अदाकारी', 'नई अभिनेत्री के सहज ____ ने दर्शकों का दिल जीत लिया।'),
        ('निर्देशक', 'फ़िल्म या नाटक के निर्माण का मार्गदर्शन करने वाला', 'डायरेक्टर', 'फ़िल्म के ____ ने हर दृश्य को बड़ी बारीकी से फ़िल्माया।'),
        ('पटकथा', 'फ़िल्म के दृश्यों और संवादों का लिखित रूप', 'स्क्रिप्ट', 'कमज़ोर ____ के कारण बड़े सितारे भी फ़िल्म को नहीं बचा सके।'),
        ('दर्शक', 'फ़िल्म, नाटक या खेल देखने वाले लोग', 'प्रेक्षक', 'मैच के आख़िरी ओवर में स्टेडियम के ____ साँस रोके बैठे थे।'),
        ('लोकप्रिय', 'जिसे बहुत लोग पसंद करें', 'मशहूर', 'यह वेब-सीरीज़ किशोरों में बहुत ____ है।'),
        ('मनोरंजन', 'मन बहलाने का साधन', 'मनबहलाव', 'आजकल मोबाइल ही ज़्यादातर लोगों के ____ का मुख्य साधन है।'),
        ('संवाद', 'पात्रों के बीच की बातचीत', 'डायलॉग', 'फ़िल्म के चुटीले ____ लोगों की ज़ुबान पर चढ़ गए।'),
        ('पार्श्व-संगीत', 'दृश्यों के पीछे चलने वाला संगीत', 'बैकग्राउंड म्यूज़िक', 'डरावने दृश्यों में ____ ने रोमांच दोगुना कर दिया।'),
        ('लत', 'किसी चीज़ की ऐसी आदत जो छूटे नहीं', 'व्यसन', 'लगातार कड़ियाँ देखने की ____ से उसकी नींद ख़राब होने लगी।'),
        ('प्रदर्शन', 'फ़िल्म का सिनेमाघरों में दिखाया जाना', 'रिलीज़', 'फ़िल्म के ____ के पहले ही दिन सारे टिकट बिक गए।'),
        ('रोमांचक', 'जिससे उत्सुकता और उत्तेजना पैदा हो', 'सनसनीख़ेज़', 'जासूसी कहानी का अंत बहुत ____ था।'),
        ('सिफ़ारिश', 'किसी को कुछ करने या चुनने का सुझाव', 'अनुशंसा', 'मेरी ____ है कि आप यह फ़िल्म पूरे परिवार के साथ देखें।'),
    ],
    topics=['मेरी प्रिय फ़िल्म', 'वेब-सीरीज़ और किशोर', 'सिनेमाघर बनाम ओटीटी', 'वीडियो गेम: मनोरंजन या लत?', 'संगीत और मेरा मूड',
            'टीवी रियलिटी शो', 'खेल-प्रतियोगिताएँ देखने का आनंद'],
    texts=[
        dict(kind='समीक्षा', title='फ़िल्म-समीक्षा: ‘मिट्टी के रंग’ ★★★★☆',
             body='निर्देशक: अनुराधा मेनन | अवधि: 128 मिनट\n‘मिट्टी के रंग’ राजस्थान के एक कुम्हार परिवार की कहानी है, जिसकी बेटी चंपा अपने पिता की कला को ऑनलाइन बाज़ार तक पहुँचाना चाहती है। नवोदित अभिनेत्री रिया सेठी ने चंपा के रूप में कमाल का सहज अभिनय किया है। रेगिस्तान के सुनहरे दृश्य और लोक-संगीत फ़िल्म की जान हैं। हाँ, दूसरे हिस्से में कहानी थोड़ी धीमी पड़ जाती है। फिर भी, परिवार के साथ देखने लायक़ यह फ़िल्म परंपरा और तकनीक का सुंदर मेल है।',
             qs=[('C1', 'फ़िल्म ‘मिट्टी के रंग’ की निर्देशक कौन हैं?', 'अनुराधा मेनन', ['रिया सेठी', 'चंपा', 'कोई नवोदित अभिनेता']),
                 ('C1', 'फ़िल्म की अवधि कितनी है?', '128 मिनट'),
                 ('C1', 'समीक्षक के अनुसार फ़िल्म की कमज़ोरी क्या है?', 'दूसरे हिस्से में कहानी का थोड़ा धीमा पड़ना', ['अभिनय कमज़ोर है', 'संगीत ख़राब है', 'दृश्य अंधेरे हैं']),
                 ('C2', '“रेगिस्तान के सुनहरे दृश्य और लोक-संगीत फ़िल्म की जान हैं” — इस वाक्य का अर्थ स्पष्ट कीजिए।', 'फ़िल्म का सबसे प्रभावशाली और जीवंत पक्ष उसका छायांकन (सुनहरे रेगिस्तानी दृश्य) और लोक-संगीत है; ये फ़िल्म को आकर्षक और यादगार बनाते हैं।'),
                 ('tf', 'समीक्षक फ़िल्म को परिवार के साथ देखने की सलाह नहीं देता।', 'गलत', '“परिवार के साथ देखने लायक़ यह फ़िल्म…”'),
                 ('C3', 'समीक्षक ने चार सितारे क्यों दिए, पाँच क्यों नहीं? पाठ के आधार पर समझाइए।', 'अभिनय, दृश्य, संगीत और विषय (परंपरा-तकनीक का मेल) की प्रशंसा की, पर दूसरे हिस्से की धीमी गति को कमज़ोरी माना — इसलिए एक सितारा कम।'),
                 ('C3', 'इस समीक्षा में किस प्रकार का संतुलन दिखाई देता है?', 'गुणों की प्रशंसा के साथ कमज़ोरी का भी उल्लेख', ['केवल प्रशंसा', 'केवल आलोचना', 'केवल कहानी का सार']),
                 ('C4', 'क्या यह समीक्षा पाठक को फ़िल्म देखने का निर्णय लेने में पर्याप्त सहायता करती है? समीक्षा की विशेषताओं के आधार पर मूल्यांकन कीजिए।', 'हाँ: निर्देशक, अवधि, कथासार (अंत बताए बिना), अभिनय-संगीत का मूल्यांकन, कमज़ोरी, रेटिंग और लक्षित दर्शक। सीमाएँ: टिकट/मंच की जानकारी नहीं, अन्य कलाकारों का उल्लेख नहीं। निष्कर्ष।')]),
        dict(kind='लेख', title='‘बिंज-वॉचिंग’: एक के बाद एक कड़ी, और रात ग़ायब!',
             body='ओटीटी मंचों पर पूरी वेब-सीरीज़ एक साथ उपलब्ध होने से ‘बिंज-वॉचिंग’ यानी लगातार कई कड़ियाँ देखने का चलन बढ़ा है। अहमदाबाद के एक कॉलेज के सर्वेक्षण में चालीस प्रतिशत विद्यार्थियों ने माना कि वे सप्ताह में कम से कम एक बार आधी रात के बाद तक सीरीज़ देखते हैं। मनोवैज्ञानिक बताते हैं कि हर कड़ी का अंत जान-बूझकर रहस्य पर छोड़ा जाता है, ताकि दर्शक अगली कड़ी चलाए बिना न रह सके। ‘ऑटो-प्ले’ बंद करना और पहले से समय तय करना इससे बचने के सरल उपाय हैं।',
             qs=[('C1', 'सर्वेक्षण में कितने प्रतिशत विद्यार्थियों ने आधी रात के बाद तक सीरीज़ देखने की बात मानी?', 'चालीस प्रतिशत', ['चार प्रतिशत', 'चौदह प्रतिशत', 'अस्सी प्रतिशत']),
                 ('C1', 'पाठ में ‘बिंज-वॉचिंग’ का क्या अर्थ बताया गया है?', 'लगातार कई कड़ियाँ देखना'),
                 ('C2', 'मनोवैज्ञानिकों के अनुसार कड़ियों का अंत रहस्य पर क्यों छोड़ा जाता है?', 'दर्शक की जिज्ञासा जगाकर उसे अगली कड़ी तुरंत देखने के लिए मजबूर करने के लिए, ताकि वह मंच पर अधिक समय बिताए।'),
                 ('tf', 'सर्वेक्षण अहमदाबाद के एक विद्यालय में किया गया था।', 'गलत', '“अहमदाबाद के एक कॉलेज के सर्वेक्षण में…”'),
                 ('C3', 'लेखक द्वारा सुझाए गए उपायों का उद्देश्य क्या है?', 'दर्शक को अपने देखने के समय पर नियंत्रण लौटाना', ['ओटीटी मंचों को बंद करवाना', 'अधिक सीरीज़ देखने के लिए प्रेरित करना', 'केवल फ़िल्में देखने की सलाह देना']),
                 ('C3', 'शीर्षक में ‘और रात ग़ायब!’ — यह अंश किस प्रभाव के लिए जोड़ा गया है?', 'हल्के-फुल्के, नाटकीय ढंग से समस्या (नींद/समय का पता न चलना) को उभारने और पाठक का ध्यान खींचने के लिए।'),
                 ('C4', 'क्या ओटीटी मंचों को ‘ऑटो-प्ले’ जैसी सुविधाएँ बंद कर देनी चाहिए, या यह दर्शक की अपनी ज़िम्मेदारी है? लेख के आधार पर तर्क दीजिए।', 'मंच की ज़िम्मेदारी: जान-बूझकर बनाई गई लत लगाने वाली डिज़ाइन, युवाओं की नींद। दर्शक की ज़िम्मेदारी: आत्म-नियंत्रण, समय-सीमा, सेटिंग बदलना। संतुलित निष्कर्ष: डिफ़ॉल्ट सुरक्षा-सुविधाएँ + डिजिटल साक्षरता।')]),
        dict(kind='साक्षात्कार', title='“गेम खेलना भी एक कौशल है” — ई-स्पोर्ट्स खिलाड़ी कबीर से बातचीत',
             body='प्रश्न: आपके माता-पिता ने ई-स्पोर्ट्स को करियर के रूप में कैसे स्वीकार किया?\nकबीर: आसानी से नहीं! पहले उन्हें लगता था कि मैं समय बर्बाद कर रहा हूँ। जब मैंने एशियाई स्तर की प्रतियोगिता के लिए क्वालीफ़ाई किया, तब उनका नज़रिया बदला।\nप्रश्न: आप दिन में कितना अभ्यास करते हैं?\nकबीर: छह घंटे, पर साथ में एक घंटा व्यायाम और पूरी नींद। लोग सोचते हैं हम बस खेलते रहते हैं; असल में यह टीम-वर्क, रणनीति और अनुशासन का खेल है।',
             qs=[('C1', 'कबीर दिन में कितने घंटे अभ्यास करते हैं?', 'छह घंटे', ['दो घंटे', 'बारह घंटे', 'एक घंटा']),
                 ('C1', 'माता-पिता का नज़रिया कब बदला?', 'जब कबीर ने एशियाई स्तर की प्रतियोगिता के लिए क्वालीफ़ाई किया'),
                 ('C2', 'कबीर ई-स्पोर्ट्स को ‘कौशल’ क्यों मानते हैं? पाठ के आधार पर समझाइए।', 'क्योंकि इसमें टीम-वर्क, रणनीति और अनुशासन की आवश्यकता होती है और नियमित अभ्यास, व्यायाम तथा नींद के संतुलन से ही प्रदर्शन अच्छा होता है।'),
                 ('tf', 'कबीर के माता-पिता ने शुरू से ही उनके करियर का समर्थन किया।', 'गलत', '“आसानी से नहीं! पहले उन्हें लगता था कि मैं समय बर्बाद कर रहा हूँ।”'),
                 ('C3', 'कबीर अभ्यास के साथ व्यायाम और नींद का उल्लेख क्यों करते हैं?', 'यह दिखाने के लिए कि पेशेवर गेमिंग में स्वस्थ, संतुलित दिनचर्या ज़रूरी है', ['यह बताने के लिए कि वे गेम कम खेलते हैं', 'माता-पिता की शिकायत करने के लिए', 'प्रतियोगिता के नियम बताने के लिए']),
                 ('C3', 'इस साक्षात्कार से ई-स्पोर्ट्स के बारे में किस रूढ़ धारणा को चुनौती मिलती है?', 'कि गेम खेलना केवल समय की बर्बादी है और खिलाड़ी ‘बस खेलते रहते हैं’; कबीर दिखाते हैं कि यह अनुशासन, रणनीति और टीम-वर्क वाला पेशेवर खेल है।'),
                 ('C4', 'क्या विद्यालयों को ई-स्पोर्ट्स को अन्य खेलों की तरह मान्यता देनी चाहिए? साक्षात्कार के आधार पर अपना मत दीजिए।', 'पक्ष: कौशल, टीम-वर्क, करियर के अवसर (कबीर)। विपक्ष: शारीरिक गतिविधि कम, स्क्रीन-टाइम और लत का ख़तरा। निष्कर्ष: नियमों और संतुलन के साथ सीमित मान्यता।')]),
    ],
    tasks=[
        ('आपने हाल ही में एक हिंदी फ़िल्म या वेब-सीरीज़ देखी है। विद्यालय-पत्रिका के ‘मनोरंजन’ खंड के लिए उसकी समीक्षा लिखिए।', 'review',
         ['कहानी का संक्षिप्त परिचय (अंत बताए बिना)', 'अभिनय, संगीत और निर्देशन का मूल्यांकन', 'रेटिंग और किसे देखनी चाहिए']),
        ('आपके विद्यालय में ‘स्क्रीन-मुक्त सप्ताहांत’ की योजना है। आपको सभा में विद्यार्थियों को इसके लिए प्रेरित करना है।', 'speech',
         ['स्क्रीन पर अधिक समय बिताने के प्रभाव', 'मनोरंजन के अन्य विकल्प', 'सप्ताहांत की योजना और आह्वान']),
        ('“ओटीटी मंचों ने सिनेमाघरों का जादू ख़त्म कर दिया है।” — इस विषय पर समाचार-पत्र के लिए लिखिए।', 'opinion',
         ['ओटीटी के लाभ', 'सिनेमाघर के सामूहिक अनुभव का महत्व', 'आपका स्पष्ट मत']),
        ('आपके शहर में पहली बार एक अंतरराष्ट्रीय बाल-फ़िल्म महोत्सव हुआ। स्थानीय समाचार-पत्र के लिए रिपोर्ट लिखिए।', 'news',
         ['महोत्सव का विवरण (कब, कहाँ, कितनी फ़िल्में)', 'मुख्य आकर्षण और प्रतिभागियों के कथन', 'आयोजकों की आगे की योजना']),
        ('आपका छोटा भाई दिन भर वीडियो गेम खेलता है। आप उसे पत्र लिखकर समझाना चाहते हैं।', 'pletter',
         ['उसकी आदत पर आपकी चिंता', 'गेमिंग के सकारात्मक और नकारात्मक पक्ष', 'संतुलन के सुझाव']),
        ('आपने एक लाइव कॉन्सर्ट में भाग लिया जो आपके जीवन का सबसे रोमांचक अनुभव था।', 'blog',
         ['कॉन्सर्ट का माहौल', 'सबसे यादगार पल', 'लाइव संगीत और रिकॉर्डेड संगीत में अंतर']),
    ],
    discuss=[
        ('क्या फ़िल्मों और वेब-सीरीज़ में हिंसा युवाओं पर बुरा प्रभाव डालती है?', ['नक़ल और असंवेदनशीलता का ख़तरा', 'कला की स्वतंत्रता और यथार्थ', 'आयु-वर्गीकरण और अभिभावकों की भूमिका']),
        ('क्या वीडियो गेम केवल समय की बर्बादी हैं?', ['रणनीति और टीम-वर्क के कौशल', 'लत और शारीरिक निष्क्रियता', 'संतुलित उपयोग']),
        ('क्या रियलिटी शो वास्तविक होते हैं?', ['पटकथा और नाटकीयता', 'प्रतिभाओं को मंच मिलना', 'दर्शकों की आलोचनात्मक दृष्टि']),
        ('क्या मनोरंजन का उद्देश्य केवल हँसाना है या समाज को संदेश देना भी?', ['मनोरंजन तनाव दूर करता है', 'सामाजिक मुद्दों पर फ़िल्में बदलाव लाती हैं', 'संदेश और मनोरंजन का संतुलन']),
        ('क्या सिनेमाघर भविष्य में बंद हो जाएँगे?', ['ओटीटी की सुविधा और कम ख़र्च', 'बड़े परदे और सामूहिक अनुभव का आकर्षण', 'नई तकनीक से सिनेमाघरों का बदलाव']),
    ],
)

CMP_CTX = [
    dict(noun='फ़िल्म', g='f', more='लंबी', less='छोटी', unit='मिनट', attr='अवधि', lo=95, hi=180,
         names=['चाँदनी रात', 'पहली उड़ान', 'सपनों का शहर', 'नीली छतरी', 'आख़िरी ट्रेन', 'बारिश की धुन', 'खोया हुआ गाँव', 'रेत का समंदर']),
    dict(noun='गीत', g='m', more='लंबा', less='छोटा', unit='मिनट', attr='अवधि', lo=3, hi=9,
         names=['सावन की झड़ी', 'मेरा गाँव', 'चल उड़ जा', 'तारों की बात', 'माटी की ख़ुशबू', 'दिल की धड़कन', 'सफ़र', 'नदिया किनारे']),
    dict(noun='सभागार', g='m', more='बड़ा', less='छोटा', unit='सीटें', attr='क्षमता', lo=200, hi=1500,
         names=['कला भवन', 'रंगमंच सदन', 'नेहरू सभागार', 'संगीत मंदिर', 'लोक मंच', 'नगर सभागार', 'टैगोर हॉल', 'कमानी सभागार']),
    dict(noun='उपन्यास', g='m', more='मोटा', less='पतला', unit='पृष्ठ', attr='पृष्ठ-संख्या', lo=120, hi=650,
         names=['धूप-छाँव', 'नदी के द्वीप', 'पहाड़ की बेटी', 'अधूरा सफ़र', 'नीम का पेड़', 'काग़ज़ की नाव', 'शहर में गाँव', 'चिट्ठियाँ']),
]


def _cmp_table(rng):
    c = rng.choice(CMP_CTX)
    names = rng.sample(c['names'], 3)
    vals = rng.sample(range(c['lo'], c['hi'] + 1), 3)
    tab = '; '.join(f'‘{n}’ — {v} {c["unit"]}' for n, v in zip(names, vals))
    return c, names, vals, f'तालिका ({c["noun"]} और {c["attr"]}): {tab}'


def g_compare(kit, key, th):
    def se(rng, slot):
        c, n, v, tab = _cmp_table(rng)
        i, j = rng.sample(range(3), 2)
        adj = c['more'] if v[i] > v[j] else c['less']
        mk = rng.choice(['से', 'की तुलना में'])
        ans = f'‘{n[i]}’, ‘{n[j]}’ {mk} {adj} है।'
        return dict(stem=f'{tab}\n‘{mk}’ का प्रयोग करते हुए ‘{n[i]}’ और ‘{n[j]}’ की तुलना करने वाला एक शुद्ध वाक्य लिखिए।', answer=ans, type='short', marks=2,
                    markingKey=f'{ans} ({v[i]} बनाम {v[j]} {c["unit"]}) — 1 अंक सही तुलना (अधिक/कम), 1 अंक ‘{mk}’ और विशेषण की लिंग-अन्विति ({c["noun"]} — {"स्त्रीलिंग" if c["g"] == "f" else "पुल्लिंग"})।')
    kit.add(key, 'C3', (1, 4), se, 'short', None, 'cmp_se')

    def most(rng, slot):
        c, n, v, tab = _cmp_table(rng)
        big = rng.random() < 0.5
        k = v.index(max(v)) if big else v.index(min(v))
        adj = c['more'] if big else c['less']
        ans = f'‘{n[k]}’ सबसे {adj} {c["noun"]} है।'
        return dict(stem=f'{tab}\n‘सबसे’ का प्रयोग करते हुए वह वाक्य लिखिए जो बताए कि इन तीनों में कौन-सा/कौन-सी {c["noun"]} सबसे {adj} है।', answer=ans, type='short', marks=2,
                    markingKey=f'{ans} — 1 अंक सही चयन, 1 अंक ‘सबसे + विशेषण’ की शुद्ध संरचना और अन्विति।')
    kit.add(key, 'C3', (1, 4), most, 'short', None, 'cmp_most')

    def pick(rng, slot):
        c, n, v, tab = _cmp_table(rng)
        i, j = rng.sample(range(3), 2)
        hi_ = c['more'] if v[i] > v[j] else c['less']
        lo_ = c['less'] if v[i] > v[j] else c['more']
        k = v.index(max(v))
        m = v.index(min(v))
        true = f'‘{n[i]}’, ‘{n[j]}’ से {hi_} है।'
        wrongs = [f'‘{n[i]}’, ‘{n[j]}’ से {lo_} है।', f'‘{n[m]}’ सबसे {c["more"]} {c["noun"]} है।', f'‘{n[k]}’ सबसे {c["less"]} {c["noun"]} है।']
        return mcq(rng, f'{tab}\nतालिका के अनुसार कौन-सा वाक्य सही है?', true, wrongs, f'{n[i]} = {v[i]}, {n[j]} = {v[j]} {c["unit"]}; अधिकतम: {n[k]}, न्यूनतम: {n[m]}।')
    kit.add(key, ('C2', 'C3'), (1, 4), pick, 'mcq', 'p2r', 'cmp_pick')

    def form(rng, slot):
        c = rng.choice(CMP_CTX)
        a, b = rng.sample(c['names'], 2)
        right = c['more']
        wrong = [c['more'][:-1] + ('ा' if c['g'] == 'f' else 'ी'), c['more'][:-1] + 'े', c['less']]
        if len(set(wrong + [right])) < 4:
            return None
        return mcq(rng, f'शुद्ध रूप चुनिए: “{c["noun"]} ‘{a}’, ‘{b}’ से ____ है।” (पहला {c["noun"]} अधिक {c["attr"]} वाला है)', right, wrong,
                   f'‘{c["noun"]}’ {"स्त्रीलिंग" if c["g"] == "f" else "पुल्लिंग"} एकवचन है, इसलिए विशेषण ‘{right}’।')
    kit.add(key, 'C1', (1, 3), form, 'mcq', None, 'cmp_form')

    def essay(rng, slot):
        topic = rng.choice(['दो फ़िल्में जो आपने हाल में देखीं', 'सिनेमाघर और ओटीटी', 'दो गायक या संगीत-शैलियाँ', 'वीडियो गेम और मैदानी खेल', 'टीवी और यूट्यूब'])
        return dict(stem=f'‘{topic}’ की तुलना करते हुए 100–120 शब्दों का अनुच्छेद लिखिए। उसमें ‘से’, ‘की तुलना में’, ‘सबसे’ और ‘जितना… उतना’ — चारों संरचनाओं का प्रयोग हो।',
                    answer='अपेक्षित: चारों तुलनात्मक संरचनाओं का शुद्ध प्रयोग; तुलना के स्पष्ट आधार (कहानी, अभिनय, सुविधा, ख़र्च); संतुलित निष्कर्ष।', type='long', marks=6,
                    markingKey=para_key(6, 'चारों संरचनाएँ आवश्यक; विशेषण की लिंग-वचन अन्विति पर ध्यान दें।'))
    kit.add(key, 'C4', (2, 5), essay, 'long', None, 'cmp_essay')


SPEC['ch09-st1'] = ('reading', dict(focus='लेखन में किसी फ़िल्म या वेब-सीरीज़ के गुण-दोषों का संतुलित मूल्यांकन कीजिए।', items=[
    ('C1', 'समीक्षा में ‘स्पॉइलर’ (कहानी का अंत बता देना) से क्यों बचना चाहिए?', 'ताकि पाठक का फ़िल्म देखने का आनंद और उत्सुकता बनी रहे', ['ताकि समीक्षा छोटी लगे', 'क्योंकि अंत हमेशा उबाऊ होता है', 'क्योंकि निर्देशक मना करते हैं'], 'समीक्षा पाठक को निर्णय में मदद करती है, अनुभव नहीं छीनती।'),
    ('C2', 'समीक्षा में दी गई ‘रेटिंग’ (जैसे ★★★★☆) और लिखित मूल्यांकन — दोनों क्यों आवश्यक हैं?', 'रेटिंग एक नज़र में समग्र राय देती है; लिखित मूल्यांकन बताता है कि वह राय किन कारणों (अभिनय, कहानी, संगीत) पर आधारित है, ताकि पाठक अपनी रुचि के अनुसार निर्णय ले सके।', '1 अंक प्रत्येक की भूमिका।'),
]))
SPEC['ch09-st2'] = ('writing', dict(tt='review', tasks=[
    ('आपने एक हिंदी उपन्यास पढ़ा है जो किशोरों के जीवन पर आधारित है। अपनी विद्यालय-वेबसाइट के ‘पुस्तक-कोना’ के लिए उसकी समीक्षा लिखिए।', ['पुस्तक और लेखक का परिचय', 'कथानक, पात्र और भाषा का मूल्यांकन', 'किन पाठकों को यह पुस्तक पढ़नी चाहिए']),
    ('आपने एक नया संगीत-एल्बम सुना है जिसमें लोक-संगीत और आधुनिक संगीत का मिश्रण है। एक संगीत-ब्लॉग के लिए समीक्षा लिखिए।', ['एल्बम और कलाकार का परिचय', 'सबसे अच्छे और कमज़ोर गीत', 'रेटिंग और सिफ़ारिश']),
    ('आपके शहर के रंगमंच पर एक हिंदी नाटक का मंचन हुआ। स्थानीय पत्रिका के लिए उसकी समीक्षा लिखिए।', ['नाटक का विषय और कथासार', 'अभिनय, मंच-सज्जा और प्रकाश-व्यवस्था', 'दर्शकों की प्रतिक्रिया और आपकी रेटिंग']),
    ('एक लोकप्रिय वेब-सीरीज़ का नया सीज़न आया है। युवाओं की ऑनलाइन पत्रिका के लिए उसकी समीक्षा लिखिए।', ['पिछले सीज़न से तुलना', 'कहानी और पात्रों का विकास', 'आयु-उपयुक्तता और सिफ़ारिश']),
    ('आपने एक ऐतिहासिक विषय पर बनी फ़िल्म देखी जिसमें इतिहास के साथ कुछ छूट ली गई है। उसकी समीक्षा लिखिए।', ['फ़िल्म का परिचय', 'ऐतिहासिक सटीकता और कलात्मक स्वतंत्रता', 'आपका संतुलित निर्णय']),
], items=[
    ('C1', 'समीक्षा की शुरुआत में सामान्यतः क्या दिया जाता है?', 'कृति का नाम, निर्माता/लेखक और मूल जानकारी', ['रेटिंग का कारण', 'पत्र का विषय', 'साक्षात्कार का प्रश्न'], 'पहले कृति का परिचय, फिर सार, मूल्यांकन और सिफ़ारिश।'),
    ('C2', 'समीक्षा और विज्ञापन, दोनों किसी फ़िल्म के बारे में हो सकते हैं। दोनों के उद्देश्य और भाषा में अंतर बताइए।', 'समीक्षा निष्पक्ष मूल्यांकन करती है — गुण-दोष दोनों बताती है, भाषा तर्कपूर्ण और मूल्यांकनपरक होती है; विज्ञापन केवल प्रशंसा करके टिकट बेचना चाहता है — भाषा अतिशयोक्तिपूर्ण और प्रेरक होती है।', '1 अंक उद्देश्य, 2 अंक भाषा/संतुलन का अंतर।', 3),
    ('C3', 'इस कमज़ोर समीक्षात्मक वाक्य को बेहतर बनाइए: “फ़िल्म अच्छी थी, सबको देखनी चाहिए।”', 'नमूना: “सधे हुए अभिनय, मार्मिक संगीत और कसी हुई पटकथा के कारण यह फ़िल्म किशोरों और अभिभावकों, दोनों के लिए देखने योग्य है — हालाँकि अंतिम दृश्य थोड़े लंबे खिंच गए हैं।”', '1 अंक मूल्यांकन के ठोस आधार, 1 अंक लक्षित दर्शक, 1 अंक संतुलन (कमज़ोरी का उल्लेख)।'),
]))
SPEC['ch09-st3'] = ('grammar', dict(focus='लेखन में ‘से’, ‘की तुलना में’, ‘सबसे’ और ‘जितना… उतना’ जैसी तुलनात्मक संरचनाओं का प्रयोग कीजिए।', gens=[g_compare], items=[
    ('C1', 'हिंदी में दो वस्तुओं की तुलना के लिए सबसे सामान्य परसर्ग कौन-सा है?', 'से', ['को', 'ने', 'पर'], '“यह फ़िल्म उससे लंबी है।” — ‘से’ तुलना का परसर्ग है।'),
    ('C1', '“वह अपने भाई जितना ही लंबा है।” — इस वाक्य में किस प्रकार की तुलना है?', 'समानता की तुलना', ['श्रेष्ठता की तुलना', 'सर्वश्रेष्ठता (सबसे) की तुलना', 'कोई तुलना नहीं'], '‘जितना…उतना/जितना ही’ समानता दिखाता है।'),
    ('C2', 'हिंदी में अंग्रेज़ी की तरह विशेषण का अलग ‘तुलनात्मक रूप’ (जैसे taller) प्रायः क्यों नहीं बनता? उदाहरण सहित समझाइए।', 'हिंदी में तुलना परसर्ग ‘से’ या ‘की तुलना में’ और ‘अधिक/ज़्यादा’ से होती है, विशेषण वही रहता है: “राम श्याम से लंबा है” — ‘लंबा’ नहीं बदलता; सर्वश्रेष्ठता के लिए ‘सबसे’ जुड़ता है। तत्सम शब्दों में ‘-तर/-तम’ (उच्चतर, उच्चतम) भी प्रयुक्त होते हैं।', '1 अंक नियम, 1 अंक उदाहरण, 1 अंक -तर/-तम या सबसे का उल्लेख।', 3),
    ('C2', '‘अधिक’ और ‘सबसे’ के प्रयोग में अंतर समझाइए।', '‘अधिक’ दो वस्तुओं की तुलना में किसी एक की श्रेष्ठता बताता है (“यह फ़िल्म उससे अधिक रोचक है”); ‘सबसे’ समूह में सर्वश्रेष्ठता (“यह सबसे रोचक फ़िल्म है”)।', '1-1 अंक प्रत्येक प्रयोग, उदाहरण सहित।'),
]))

# ---------------------------------------------------------------- ch10 कलात्मक अभिव्यक्तियाँ
TH[10] = dict(
    name='कलात्मक अभिव्यक्तियाँ',
    vocab=[
        ('लोककला', 'किसी क्षेत्र के आम लोगों की परंपरागत कला', 'जनकला', 'मधुबनी चित्रकला बिहार की प्रसिद्ध ____ है।'),
        ('शास्त्रीय', 'नियमों और परंपरा पर आधारित, परिष्कृत', 'क्लासिकी', 'भरतनाट्यम एक ____ नृत्य-शैली है।'),
        ('रंगमंच', 'नाटक के मंचन की कला और स्थान', 'थिएटर', 'हबीब तनवीर ने ____ में लोक-कलाकारों को शामिल किया।'),
        ('कलाकार', 'कला की साधना करने वाला व्यक्ति', 'फ़नकार', 'गाँव के ____ ने मिट्टी से अद्भुत मूर्तियाँ बनाईं।'),
        ('शिल्प', 'हाथ से वस्तुएँ बनाने की कला', 'दस्तकारी', 'चन्नपटना के लकड़ी के खिलौनों का ____ विश्व प्रसिद्ध है।'),
        ('सुर', 'संगीत की ध्वनि का निश्चित स्वर', 'स्वर', 'उसकी आवाज़ में ____ और ताल का अद्भुत मेल है।'),
        ('ताल', 'संगीत में समय और लय का नियमित चक्र', 'लय', 'तबला-वादक ने तीन ____ में अद्भुत प्रस्तुति दी।'),
        ('मंचन', 'नाटक को मंच पर प्रस्तुत करना', 'प्रस्तुति', 'विद्यालय में ‘अंधेर नगरी’ नाटक का ____ हुआ।'),
        ('प्रदर्शनी', 'कलाकृतियों को देखने के लिए सजाकर रखना', 'नुमाइश', 'कला-भवन में युवा चित्रकारों की ____ लगी है।'),
        ('संरक्षण', 'किसी चीज़ को नष्ट होने से बचाना', 'रक्षा', 'लुप्त होती कलाओं के ____ के लिए सरकार ने योजना बनाई।'),
        ('रचनात्मकता', 'नया सृजन करने की क्षमता', 'सृजनशीलता', 'कला विद्यार्थियों की ____ को निखारती है।'),
        ('घराना', 'संगीत या नृत्य की कोई विशिष्ट परंपरा या शैली-परिवार', 'परंपरा-शैली', 'किराना ____ अपनी मधुर गायकी के लिए जाना जाता है।'),
        ('अभिव्यक्ति', 'भावों और विचारों को प्रकट करना', 'प्रकटन', 'नृत्य भावनाओं की ____ का सुंदर माध्यम है।'),
        ('कठपुतली', 'धागों से नचाई जाने वाली गुड़िया', 'पुतली', 'राजस्थान के ____ खेल में अमर सिंह राठौड़ की कथा दिखाई जाती है।'),
    ],
    topics=['मेरी प्रिय कला', 'लुप्त होती लोक-कलाएँ', 'कला और तकनीक', 'विद्यालयों में कला-शिक्षा', 'संगीत का जादू',
            'रंगमंच का महत्व', 'कला और पहचान'],
    texts=[
        dict(kind='लेख', title='मधुबनी: दीवारों से दुनिया तक',
             body='बिहार के मिथिला क्षेत्र की मधुबनी चित्रकला पहले शादियों और त्योहारों पर घर की दीवारों और आँगन में बनाई जाती थी। इसमें प्रकृति, देवी-देवता और मछली, कछुआ जैसे शुभ प्रतीक चटख प्राकृतिक रंगों से उकेरे जाते हैं। परंपरागत रूप से यह कला माँ से बेटी तक पहुँचती थी। 1960 के दशक के सूखे के बाद इसे काग़ज़ और कपड़े पर उतारा गया, ताकि परिवारों को आय मिल सके। आज मधुबनी चित्र दुनिया भर की प्रदर्शनियों में दिखते हैं और कई कलाकारों को पद्म सम्मान मिल चुके हैं।',
             qs=[('C1', 'मधुबनी चित्रकला किस क्षेत्र से जुड़ी है?', 'बिहार के मिथिला क्षेत्र से', ['राजस्थान के मेवाड़ से', 'केरल के मालाबार से', 'गुजरात के कच्छ से']),
                 ('C1', 'पहले यह चित्रकला कहाँ बनाई जाती थी?', 'घर की दीवारों और आँगन में'),
                 ('C1', 'मधुबनी चित्रों में कौन-से दो शुभ प्रतीकों का उल्लेख पाठ में है?', 'मछली और कछुआ'),
                 ('C2', 'मधुबनी कला को काग़ज़ और कपड़े पर क्यों उतारा गया? समझाइए।', '1960 के दशक के सूखे के बाद परिवारों को आय की ज़रूरत थी; काग़ज़-कपड़े पर बने चित्र बेचे जा सकते थे, इसलिए कला आजीविका का साधन बनी।'),
                 ('tf', 'परंपरागत रूप से मधुबनी कला पिता से पुत्र तक पहुँचती थी।', 'गलत', '“परंपरागत रूप से यह कला माँ से बेटी तक पहुँचती थी।”'),
                 ('C3', 'शीर्षक ‘दीवारों से दुनिया तक’ किस परिवर्तन की ओर संकेत करता है?', 'घरेलू, स्थानीय कला के अंतरराष्ट्रीय पहचान पाने की यात्रा', ['दीवार बनाने की तकनीक', 'कलाकारों के विदेश में बसने', 'चित्रों के महँगे होने']),
                 ('C3', 'सूखे जैसी आपदा ने इस कला के लिए अवसर कैसे पैदा किया? पाठ के आधार पर समझाइए।', 'आर्थिक संकट ने कला को नए माध्यम (काग़ज़, कपड़ा) पर लाने को प्रेरित किया; इससे कला बाज़ार, प्रदर्शनियों और अंतरराष्ट्रीय पहचान तक पहुँची — संकट नवाचार का कारण बना।'),
                 ('C4', 'क्या लोककला का व्यावसायीकरण उसकी मौलिकता को नुक़सान पहुँचाता है? मधुबनी के उदाहरण से विवेचना कीजिए।', 'पक्ष (नुक़सान): बाज़ार की माँग से विषयों और रंगों में बदलाव, धार्मिक-सामाजिक संदर्भ का क्षरण। विपक्ष: आय, सम्मान, कला का संरक्षण और विस्तार। निष्कर्ष: समुदाय के नियंत्रण में संतुलित व्यावसायीकरण।')]),
        dict(kind='साक्षात्कार', title='“कठपुतली मेरे हाथ में नहीं, दिल में नाचती है” — कलाकार पूरन भाट',
             body='प्रश्न: आप कितनी पीढ़ियों से कठपुतली का खेल दिखा रहे हैं?\nपूरन: मेरे परदादा राजाओं के दरबार में खेल दिखाते थे। मैं चौथी पीढ़ी हूँ।\nप्रश्न: आज के बच्चे मोबाइल में खोए रहते हैं। क्या उन्हें कठपुतली अच्छी लगती है?\nपूरन: जब मैं धागा खींचता हूँ और पुतली नाचती है, तो बच्चे मोबाइल भूल जाते हैं! अब मैं पुरानी कहानियों के साथ प्लास्टिक-प्रदूषण और पानी बचाने जैसी नई कहानियाँ भी दिखाता हूँ।\nप्रश्न: सबसे बड़ी चिंता?\nपूरन: मेरा बेटा यह काम नहीं करना चाहता। इसमें कमाई कम है।',
             qs=[('C1', 'पूरन भाट कठपुतली-कलाकारों की कौन-सी पीढ़ी हैं?', 'चौथी', ['पहली', 'दूसरी', 'दसवीं']),
                 ('C1', 'पूरन के परदादा कहाँ खेल दिखाते थे?', 'राजाओं के दरबार में'),
                 ('C2', 'पूरन ने अपने खेलों में नई कहानियाँ क्यों जोड़ी हैं?', 'कला को आज के दर्शकों के लिए प्रासंगिक बनाने और प्लास्टिक-प्रदूषण, जल-संरक्षण जैसे समसामयिक संदेश देने के लिए, ताकि बच्चे जुड़े रहें।'),
                 ('tf', 'पूरन का बेटा पिता की तरह कठपुतली-कलाकार बनना चाहता है।', 'गलत', '“मेरा बेटा यह काम नहीं करना चाहता।”'),
                 ('C3', 'पूरन की ‘सबसे बड़ी चिंता’ से लोककलाओं के सामने किस संकट का पता चलता है?', 'कम आय के कारण नई पीढ़ी के कला छोड़ देने से कला के लुप्त होने का', ['मोबाइल फ़ोन महँगे होने का', 'कठपुतलियों के टूट जाने का', 'दर्शकों की भीड़ बढ़ने का']),
                 ('C3', 'शीर्षक “कठपुतली मेरे हाथ में नहीं, दिल में नाचती है” से पूरन के कला के प्रति किस भाव का पता चलता है?', 'उनके लिए कठपुतली केवल तकनीक या रोज़ी नहीं, बल्कि भावनात्मक लगाव, पारिवारिक विरासत और आत्मा से जुड़ी कला है।'),
                 ('C4', 'लोक-कलाकारों की नई पीढ़ी को कला से जोड़े रखने के लिए सरकार और समाज क्या कर सकते हैं? साक्षात्कार के आधार पर सुझाव दीजिए।', 'आर्थिक सहायता और पेंशन, विद्यालयों में कार्यशालाएँ, ऑनलाइन मंच और पर्यटन से जोड़ना, नई कहानियों से प्रासंगिकता (पूरन का प्रयोग); समस्या (कम कमाई) से स्पष्ट संबंध।')]),
        dict(kind='सूचना', title='सूचना: अंतर-विद्यालय लोकनृत्य प्रतियोगिता',
             body='दिल्ली पब्लिक विद्यालय, जयपुर\nदिनांक: 5 अक्टूबर\nसभी विद्यार्थियों को सूचित किया जाता है कि 25 अक्टूबर को विद्यालय सभागार में अंतर-विद्यालय लोकनृत्य प्रतियोगिता आयोजित की जाएगी। प्रत्येक दल में छह से आठ प्रतिभागी हो सकते हैं और प्रस्तुति की अवधि अधिकतम आठ मिनट होगी। केवल पारंपरिक लोकनृत्य (जैसे घूमर, भांगड़ा, बिहू, गरबा) मान्य होंगे। इच्छुक विद्यार्थी 15 अक्टूबर तक संगीत-शिक्षिका श्रीमती कविता शर्मा के पास नाम लिखवाएँ।\nसांस्कृतिक सचिव',
             qs=[('C1', 'प्रतियोगिता किस तारीख़ को होगी?', '25 अक्टूबर', ['5 अक्टूबर', '15 अक्टूबर', '8 अक्टूबर']),
                 ('C1', 'प्रत्येक प्रस्तुति की अधिकतम अवधि कितनी है?', 'आठ मिनट'),
                 ('C1', 'नाम किसके पास लिखवाने हैं?', 'संगीत-शिक्षिका श्रीमती कविता शर्मा के पास'),
                 ('C2', 'सूचना में ‘केवल पारंपरिक लोकनृत्य मान्य होंगे’ — इस नियम का उद्देश्य क्या हो सकता है?', 'प्रतियोगिता को लोक-संस्कृति के संरक्षण और प्रदर्शन पर केंद्रित रखना, ताकि विद्यार्थी फ़िल्मी या आधुनिक नृत्य के बजाय क्षेत्रीय परंपराएँ सीखें।'),
                 ('tf', 'एक दल में अधिकतम दस प्रतिभागी हो सकते हैं।', 'गलत', '“प्रत्येक दल में छह से आठ प्रतिभागी हो सकते हैं।”'),
                 ('C3', 'इस सूचना की कौन-सी विशेषता बताती है कि यह औपचारिक पाठ है?', 'संस्था का नाम, दिनांक, कर्मवाच्य (‘सूचित किया जाता है’) और जारीकर्ता का पद', ['आत्मीय संबोधन और भावनाएँ', 'कहानी जैसा वर्णन', 'प्रश्न-उत्तर प्रारूप']),
                 ('C3', 'यदि कोई विद्यार्थी 18 अक्टूबर को नाम लिखवाने जाए तो क्या होगा? सूचना के आधार पर तर्क दीजिए।', 'उसका नाम संभवतः स्वीकार नहीं होगा, क्योंकि अंतिम तिथि 15 अक्टूबर है।'),
                 ('C4', 'इस सूचना को और अधिक प्रभावी बनाने के लिए कौन-सी दो जानकारियाँ जोड़ी जानी चाहिए? कारण सहित बताइए।', 'उदाहरण: समय (कितने बजे), पुरस्कार, निर्णायक-मानदंड, वेशभूषा/संगीत की व्यवस्था, पूर्वाभ्यास की तिथि। प्रत्येक सुझाव का प्रतिभागियों के लिए महत्व समझाया जाए।')]),
    ],
    tasks=[
        ('आपके शहर में एक लुप्त होती लोककला की प्रदर्शनी लगी थी। विद्यालय-पत्रिका के लिए उस पर लेख लिखिए।', 'article',
         ['कला का परिचय और इतिहास', 'कलाकारों की समस्याएँ', 'संरक्षण के सुझाव']),
        ('आपके विद्यालय ने बजट की कमी के कारण संगीत और कला की कक्षाएँ कम कर दी हैं। प्रधानाचार्य को पत्र लिखिए।', 'fletter',
         ['निर्णय से विद्यार्थियों पर प्रभाव', 'कला-शिक्षा का महत्व', 'वैकल्पिक सुझाव']),
        ('विद्यालय-पत्रिका के लिए किसी स्थानीय कलाकार (चित्रकार, संगीतकार या नर्तक) का साक्षात्कार लीजिए।', 'interview',
         ['कलाकार की यात्रा', 'कला में चुनौतियाँ', 'युवा कलाकारों के लिए संदेश']),
        ('आपने पहली बार किसी शास्त्रीय संगीत-समारोह में भाग लिया।', 'blog',
         ['समारोह का माहौल', 'संगीत का अनुभव', 'शास्त्रीय संगीत पर आपके बदले विचार']),
        ('विश्व रंगमंच दिवस (27 मार्च) पर आपको विद्यालय सभा में रंगमंच के महत्व पर बोलना है।', 'speech',
         ['रंगमंच क्या सिखाता है', 'फ़िल्मों और ओटीटी के दौर में रंगमंच', 'नाटक-क्लब से जुड़ने का आह्वान']),
        ('आपके शहर में ‘लोक-कला मेला’ हो रहा है। आयोजकों के लिए एक आकर्षक विज्ञापन तैयार कीजिए।', 'advert',
         ['मेले के आकर्षण', 'तिथि, स्थान और प्रवेश-शुल्क', 'कार्यशालाओं और ख़रीदारी की जानकारी']),
    ],
    discuss=[
        ('क्या कला को स्कूल में परीक्षा के अंकों से मापा जाना चाहिए?', ['मूल्यांकन से गंभीरता', 'रचनात्मकता पर दबाव', 'पोर्टफ़ोलियो जैसे वैकल्पिक तरीके']),
        ('क्या कृत्रिम बुद्धिमत्ता से बनी पेंटिंग या संगीत को ‘कला’ कहा जा सकता है?', ['रचनात्मक संभावनाएँ', 'मानवीय भावना और अनुभव का अभाव', 'कलाकार के अधिकार और मौलिकता']),
        ('क्या लोककलाओं को बचाना सरकार की ज़िम्मेदारी है?', ['सांस्कृतिक धरोहर की रक्षा', 'समुदाय और बाज़ार की भूमिका', 'साझा प्रयास']),
        ('क्या फ़्यूज़न संगीत परंपरा का अपमान है या उसका विस्तार?', ['नई पीढ़ी तक पहुँच', 'शास्त्रीय नियमों का उल्लंघन', 'कला का स्वाभाविक विकास']),
        ('क्या हर व्यक्ति कलाकार हो सकता है?', ['रचनात्मकता सबमें होती है', 'प्रतिभा और साधना की आवश्यकता', 'कला का अर्थ व्यापक है']),
    ],
    pics=[('एक संग्रहालय की दीवार पर एक बड़ी वारली चित्रकला है; एक विदेशी पर्यटक-समूह उसकी तस्वीरें ले रहा है और एक आदिवासी कलाकार उन्हें प्रतीकों का अर्थ समझा रहा है।',
           ['आदिवासी कला की वैश्विक पहचान', 'कला के माध्यम से सांस्कृतिक संवाद', 'कलाकार का सम्मान और आय']),
          ('एक गली में कुछ युवा दीवार पर विशाल भित्ति-चित्र (म्यूरल) बना रहे हैं, जिसमें गांधीजी, एक पेड़ और ‘स्वच्छ शहर’ लिखा है; बच्चे रंगों के डिब्बे थामे हैं।',
           ['सार्वजनिक कला और सामाजिक संदेश', 'समुदाय की भागीदारी', 'शहरी सौंदर्यीकरण'])],
)

SPEC['ch10-st1'] = ('vocab', dict(focus='लेखन में लोककला, संगीत, नृत्य और रंगमंच की सटीक शब्दावली का प्रयोग कीजिए।', items=[
    ('C1', 'कथक किस प्रकार का नृत्य है?', 'उत्तर भारत का शास्त्रीय नृत्य', ['पंजाब का लोकनृत्य', 'असम का फ़सल-नृत्य', 'आधुनिक पश्चिमी नृत्य'], 'कथक उत्तर भारत की शास्त्रीय नृत्य-शैली है।'),
    ('C1', 'घूमर किस राज्य का प्रसिद्ध लोकनृत्य है?', 'राजस्थान', ['केरल', 'पंजाब', 'ओडिशा'], 'घूमर राजस्थान का पारंपरिक लोकनृत्य है।'),
    ('C1', 'सितार किस प्रकार का वाद्य-यंत्र है?', 'तार वाला वाद्य', ['फूँक से बजने वाला वाद्य', 'चमड़े से मढ़ा ताल-वाद्य', 'धातु की घंटी'], 'सितार तंतु (तार) वाद्य है; तबला ताल-वाद्य, बाँसुरी सुषिर (फूँक) वाद्य।'),
    ('C2', '‘लोककला’ और ‘शास्त्रीय कला’ में अंतर उदाहरण सहित स्पष्ट कीजिए।', 'लोककला आम लोगों की परंपरा से स्वाभाविक रूप से विकसित होती है और उसके नियम लचीले होते हैं (घूमर, मधुबनी); शास्त्रीय कला लिखित शास्त्रों/कड़े नियमों और गुरु-शिष्य परंपरा पर आधारित होती है (भरतनाट्यम, हिंदुस्तानी शास्त्रीय संगीत)।', '1-1 अंक प्रत्येक अर्थ, 1 अंक उदाहरण।', 3),
]))
SPEC['ch10-st2'] = ('reading', dict(focus='लेखन में किसी कलाकार के जीवन और कला-यात्रा का प्रभावी चित्रण कीजिए।', items=[
    ('C1', 'किसी कलाकार पर लिखे लेख में ‘पृष्ठभूमि’ खंड में सामान्यतः क्या होता है?', 'कलाकार का परिचय, क्षेत्र और कला की परंपरा', ['पाठक के लिए प्रश्नावली', 'टिकट की क़ीमत', 'केवल लेखक की निजी यात्रा'], 'पृष्ठभूमि पाठक को संदर्भ देती है।'),
    ('C2', 'कलाकार के साक्षात्कार में उसके अपने शब्द (प्रत्यक्ष उद्धरण) पाठक के लिए क्यों मूल्यवान होते हैं?', 'वे कलाकार की भावनाएँ, दृष्टिकोण और व्यक्तित्व को सीधे प्रकट करते हैं; इससे प्रामाणिकता और आत्मीयता आती है, जो लेखक के वर्णन से संभव नहीं।', '1 अंक प्रामाणिकता, 1 अंक भावनात्मक प्रभाव।'),
]))
SPEC['ch10-st3'] = ('oral', dict(focus='लेखन में अपनी प्रिय कला के बारे में व्यक्तिगत अनुभव और विचार प्रस्तुत कीजिए।', items=[
    ('C1', 'अपनी प्रिय कला पर मौखिक प्रस्तुति का सबसे उपयुक्त क्रम कौन-सा है?', 'परिचय → निजी अनुभव → कला का महत्व → निष्कर्ष', ['निष्कर्ष → परिचय → प्रश्न', 'केवल कला की परिभाषा', 'केवल कलाकारों के नाम'], 'तार्किक क्रम संदेश (मानदंड B) को स्पष्ट बनाता है।'),
    ('C2', 'मौखिक प्रस्तुति में लिखा हुआ पूरा पाठ पढ़ने के बजाय संकेत-बिंदुओं (नोट्स) से बोलना क्यों बेहतर है?', 'इससे बोलने में स्वाभाविकता, प्रवाह और श्रोता से आँख-संपर्क बना रहता है; रटा हुआ पाठ पढ़ने से संवाद-कौशल (मानदंड C) और भाषा की सहजता कम दिखती है।', '1 अंक प्रवाह/स्वाभाविकता, 1 अंक मानदंड से संबंध।'),
]))

# ---------------------------------------------------------------- ch11 संचार और मीडिया
TH[11] = dict(
    name='संचार और मीडिया',
    vocab=[
        ('संवाददाता', 'घटनास्थल से समाचार भेजने वाला पत्रकार', 'रिपोर्टर', 'हमारे ____ ने बाढ़-प्रभावित गाँव से ताज़ा जानकारी भेजी।'),
        ('संपादकीय', 'समाचार-पत्र का वह लेख जिसमें संपादक का मत होता है', 'अग्रलेख', 'आज के ____ में बढ़ती महँगाई पर चिंता जताई गई है।'),
        ('सुर्ख़ी', 'समाचार का मुख्य शीर्षक', 'शीर्षक', 'अख़बार की ____ थी: “भारत ने विश्व कप जीता।”'),
        ('अफ़वाह', 'बिना पुष्टि के फैलने वाली बात', 'किंवदंती', 'सोशल मीडिया पर फैली ____ के कारण बाज़ार में अफ़रा-तफ़री मच गई।'),
        ('पुष्टि', 'किसी बात के सच होने का प्रमाण', 'तसदीक़', 'किसी समाचार को साझा करने से पहले उसकी ____ ज़रूर करें।'),
        ('निष्पक्ष', 'जो किसी का पक्ष न ले', 'तटस्थ', 'अच्छी पत्रकारिता के लिए ____ होना आवश्यक है।'),
        ('प्रसारण', 'रेडियो या टीवी द्वारा कार्यक्रम दिखाना या सुनाना', 'टेलीकास्ट', 'मैच का सीधा ____ दस भाषाओं में हुआ।'),
        ('गोपनीयता', 'निजी जानकारी को सुरक्षित रखने का अधिकार', 'निजता', 'ऐप डाउनलोड करते समय अपनी ____ की शर्तें ध्यान से पढ़ें।'),
        ('प्रामाणिक', 'जिस पर भरोसा किया जा सके, सत्यापित', 'विश्वसनीय', 'शोध-कार्य के लिए केवल ____ स्रोतों का प्रयोग करें।'),
        ('भ्रामक', 'जो ग़लत धारणा बनाए', 'गुमराह करने वाला', 'वह शीर्षक इतना ____ था कि लोगों ने पूरा समाचार ही ग़लत समझा।'),
        ('अनुयायी', 'सोशल मीडिया पर किसी को फ़ॉलो करने वाले लोग', 'फ़ॉलोअर', 'उस विज्ञान-यूट्यूबर के दस लाख ____ हैं।'),
        ('साक्षरता', 'पढ़ने-लिखने और समझने की योग्यता', 'शिक्षितता', 'डिजिटल ____ का अर्थ है ऑनलाइन जानकारी को सही ढंग से परखना।'),
        ('विज्ञापन', 'किसी वस्तु या सेवा के प्रचार की सूचना', 'इश्तिहार', 'बच्चों के कार्यक्रमों के बीच मीठे पेयों के ____ पर रोक की माँग उठी है।'),
        ('सनसनीख़ेज़', 'जानबूझकर उत्तेजना पैदा करने वाला', 'उत्तेजक', 'कुछ चैनल दर्शक बढ़ाने के लिए ____ ख़बरें दिखाते हैं।'),
    ],
    topics=['सोशल मीडिया और किशोर', 'फ़ेक न्यूज़ से कैसे बचें', 'समाचार-पत्र बनाम डिजिटल समाचार', 'विज्ञापनों का प्रभाव', 'ऑनलाइन निजता',
            'पत्रकारिता की ज़िम्मेदारी', 'रेडियो का बदलता रूप'],
    texts=[
        dict(kind='समाचार रिपोर्ट', title='विद्यार्थियों ने पकड़ी ‘फ़ेक न्यूज़’, पुलिस ने की सराहना',
             body='पुणे, 14 फ़रवरी। एक स्थानीय विद्यालय की कक्षा ग्यारह के चार विद्यार्थियों ने सोशल मीडिया पर वायरल हो रहे उस संदेश की सच्चाई उजागर की, जिसमें दावा किया गया था कि शहर का पानी ज़हरीला हो गया है। विद्यार्थियों ने नगर निगम की वेबसाइट, जल-प्रयोगशाला की रिपोर्ट और एक पुराने समाचार की तारीख़ जाँचकर पाया कि तस्वीर तीन साल पुरानी और दूसरे राज्य की थी। साइबर पुलिस ने विद्यार्थियों को सम्मानित किया और नागरिकों से अपील की कि कोई भी संदेश आगे भेजने से पहले उसकी पुष्टि करें।',
             qs=[('C1', 'वायरल संदेश में क्या दावा किया गया था?', 'शहर का पानी ज़हरीला हो गया है', ['शहर में बाढ़ आ गई है', 'विद्यालय बंद हो गए हैं', 'बिजली कटौती होगी']),
                 ('C1', 'वायरल तस्वीर के बारे में विद्यार्थियों ने क्या पाया?', 'तस्वीर तीन साल पुरानी और दूसरे राज्य की थी'),
                 ('C1', 'विद्यार्थियों को किसने सम्मानित किया?', 'साइबर पुलिस ने'),
                 ('C2', 'विद्यार्थियों द्वारा अपनाई गई जाँच-प्रक्रिया को अपने शब्दों में समझाइए।', 'उन्होंने आधिकारिक स्रोत (नगर निगम की वेबसाइट), वैज्ञानिक प्रमाण (जल-प्रयोगशाला की रिपोर्ट) और तस्वीर की मूल तारीख़-स्थान की तुलना करके दावे को परखा।'),
                 ('tf', 'वायरल तस्वीर पुणे शहर की ही थी।', 'गलत', '“तस्वीर तीन साल पुरानी और दूसरे राज्य की थी।”'),
                 ('C3', 'रिपोर्ट के अंत में पुलिस की अपील का उल्लेख क्यों किया गया है?', 'घटना से आम नागरिकों के लिए व्यावहारिक सीख देने के लिए', ['विद्यार्थियों की आलोचना करने के लिए', 'नगर निगम का विज्ञापन करने के लिए', 'पानी की क़ीमत बताने के लिए']),
                 ('C3', 'इस रिपोर्ट को ‘निष्पक्ष समाचार’ क्यों कहा जा सकता है? दो प्रमाण दीजिए।', 'तृतीय पुरुष में तथ्यात्मक वर्णन, लेखक की निजी राय नहीं; स्रोतों का उल्लेख (नगर निगम, जल-प्रयोगशाला, साइबर पुलिस); स्थान-दिनांक-पंक्ति।'),
                 ('C4', 'क्या विद्यालयों में ‘फ़ैक्ट-चेकिंग’ (तथ्य-जाँच) को अनिवार्य पाठ्यक्रम का हिस्सा बनाया जाना चाहिए? इस रिपोर्ट के आधार पर तर्क दीजिए।', 'पक्ष: डिजिटल साक्षरता, अफ़वाहों से सामाजिक नुक़सान की रोकथाम, विद्यार्थियों का सफल उदाहरण। विपक्ष: पाठ्यक्रम का बोझ; अन्य विषयों में एकीकरण संभव। निष्कर्ष।')]),
        dict(kind='संपादकीय', title='सुर्ख़ियों की होड़ में सच कहाँ?',
             body='चौबीस घंटे चलने वाले समाचार-चैनलों में ‘सबसे पहले’ ख़बर देने की होड़ इतनी तेज़ है कि कई बार ‘सबसे सही’ ख़बर पीछे छूट जाती है। पिछले महीने एक दुर्घटना में मृतकों की संख्या तीन चैनलों ने तीन अलग-अलग बताई। विज्ञापन से होने वाली आय दर्शक-संख्या पर निर्भर है, इसलिए सनसनीख़ेज़ शीर्षक और चीख़ते एंकर आम हो गए हैं। पत्रकारिता लोकतंत्र का चौथा स्तंभ कहलाती है; यदि यह स्तंभ ही डगमगाए तो जनता का भरोसा कैसे टिकेगा? मीडिया को गति नहीं, विश्वसनीयता को अपनी पहचान बनाना होगा।',
             qs=[('C1', 'संपादकीय के अनुसार समाचार-चैनलों में किस बात की होड़ है?', 'सबसे पहले ख़बर देने की', ['सबसे सस्ते विज्ञापन की', 'सबसे कम ख़बरें दिखाने की', 'सबसे लंबे कार्यक्रम की']),
                 ('C1', 'पत्रकारिता को लोकतंत्र का कौन-सा स्तंभ कहा जाता है?', 'चौथा स्तंभ'),
                 ('C2', '‘सबसे पहले’ और ‘सबसे सही’ — लेखक ने इन दोनों का विरोधाभास किस उद्देश्य से प्रस्तुत किया है?', 'यह दिखाने के लिए कि गति की होड़ में सटीकता की बलि दी जा रही है; दोनों शब्दों की तुलना से समस्या तीखे और यादगार ढंग से उभरती है।'),
                 ('tf', 'तीनों चैनलों ने दुर्घटना में मृतकों की संख्या एक समान बताई।', 'गलत', '“…मृतकों की संख्या तीन चैनलों ने तीन अलग-अलग बताई।”'),
                 ('C3', 'लेखक के अनुसार सनसनीख़ेज़ शीर्षकों का मूल कारण क्या है?', 'विज्ञापन-आय का दर्शक-संख्या पर निर्भर होना', ['पत्रकारों की कमी', 'सरकार का आदेश', 'दर्शकों की कम रुचि']),
                 ('C3', '“यदि यह स्तंभ ही डगमगाए तो…” — इस अलंकारिक प्रश्न का प्रभाव समझाइए।', 'यह पाठक को लोकतंत्र में मीडिया की भूमिका की गंभीरता पर सोचने को विवश करता है; ‘स्तंभ’ के रूपक से भरोसे के गिरने का ख़तरा नाटकीय ढंग से सामने आता है।'),
                 ('C4', '“दर्शक जैसी ख़बरें देखना चाहते हैं, चैनल वैसी ही दिखाते हैं।” — इस प्रतितर्क के आलोक में संपादकीय के मत का मूल्यांकन कीजिए।', 'प्रतितर्क: माँग-आपूर्ति, दर्शकों की ज़िम्मेदारी। संपादकीय: मीडिया की नैतिक ज़िम्मेदारी, लोकतंत्र में भरोसा, विज्ञापन-आधारित मॉडल की समस्या। निष्कर्ष: दोनों पक्षों की ज़िम्मेदारी, मीडिया-साक्षरता और नियामक।')]),
        dict(kind='ब्लॉग प्रविष्टि', title='मैंने अपने ‘लाइक्स’ छिपा दिए — 3 मार्च',
             body='पिछले महीने मैंने इंस्टाग्राम पर अपनी पोस्टों के ‘लाइक्स’ की गिनती छिपा दी। शुरुआत में अजीब लगा — पोस्ट डालते ही बार-बार फ़ोन देखने की आदत जो थी। पर दो सप्ताह बाद मैंने महसूस किया कि अब मैं वही तस्वीरें डालती हूँ जो मुझे पसंद हैं, न कि वे जो ‘ज़्यादा लाइक्स’ बटोरें। मेरी एक सहेली कहती है कि लाइक्स से उसे प्रेरणा मिलती है। ठीक है, पर मेरे लिए यह आज़ादी जैसा है। आप अपने सोशल मीडिया के मालिक हैं या वह आपका? सोचिए!',
             qs=[('C1', 'लेखिका ने इंस्टाग्राम पर क्या छिपाया?', 'अपनी पोस्टों के लाइक्स की गिनती', ['अपनी प्रोफ़ाइल तस्वीर', 'अपने सारे दोस्तों के नाम', 'अपनी सारी पोस्ट']),
                 ('C1', 'लेखिका को कितने समय बाद बदलाव महसूस हुआ?', 'दो सप्ताह बाद'),
                 ('C2', 'लाइक्स छिपाने के बाद लेखिका की पोस्ट चुनने की आदत में क्या परिवर्तन आया?', 'पहले वह ऐसी तस्वीरें डालती थी जिन पर ज़्यादा लाइक्स मिलें; अब वह वही डालती है जो उसे स्वयं पसंद हैं — दूसरों की स्वीकृति के बजाय अपनी रुचि महत्वपूर्ण हो गई।'),
                 ('tf', 'लेखिका की सहेली भी लाइक्स को हानिकारक मानती है।', 'गलत', '“मेरी एक सहेली कहती है कि लाइक्स से उसे प्रेरणा मिलती है।”'),
                 ('C3', '“आप अपने सोशल मीडिया के मालिक हैं या वह आपका?” — इस प्रश्न से लेखिका क्या कहना चाहती है?', 'हम अक्सर सोशल मीडिया के नियंत्रण में आ जाते हैं, जबकि हमें उसे अपने नियंत्रण में रखना चाहिए', ['सोशल मीडिया कंपनियाँ बेचनी चाहिए', 'हर किसी के पास इंस्टाग्राम होना चाहिए', 'लाइक्स ख़रीदे जा सकते हैं']),
                 ('C3', 'ब्लॉग में सहेली का विपरीत मत शामिल करने से लेखिका के तर्क पर क्या प्रभाव पड़ता है?', 'लेखिका संतुलित और निष्पक्ष दिखती है; वह दूसरों के अनुभव को स्वीकारते हुए भी अपनी बात रखती है, जिससे पाठक उसके तर्क पर अधिक भरोसा करता है।'),
                 ('C4', 'क्या सोशल मीडिया कंपनियों को सभी उपयोगकर्ताओं के लिए ‘लाइक्स’ स्थायी रूप से छिपा देने चाहिए? ब्लॉग के आधार पर विवेचना कीजिए।', 'पक्ष: तुलना और चिंता में कमी, रचनात्मक स्वतंत्रता (लेखिका)। विपक्ष: प्रेरणा (सहेली), कलाकारों-व्यवसायों के लिए प्रतिक्रिया का माप, उपयोगकर्ता का चुनाव। निष्कर्ष: विकल्प उपयोगकर्ता पर।')]),
        dict(kind='विज्ञापन', title='‘सच-सेतु’ ऐप — हर ख़बर की जाँच, एक क्लिक में!',
             body='क्या आपके परिवार के व्हाट्सऐप समूह में रोज़ ‘चौंकाने वाले’ संदेश आते हैं? अब घबराइए नहीं! ‘सच-सेतु’ ऐप में किसी भी संदेश, तस्वीर या वीडियो का लिंक डालिए और जानिए कि वह सही है, भ्रामक है या पूरी तरह झूठा। बारह भारतीय भाषाओं में उपलब्ध। प्रशिक्षित पत्रकारों की टीम द्वारा जाँच। विद्यार्थियों के लिए बिल्कुल मुफ़्त! आज ही डाउनलोड कीजिए — क्योंकि आगे भेजने से पहले सोचना ज़रूरी है।',
             qs=[('C1', '‘सच-सेतु’ ऐप कितनी भारतीय भाषाओं में उपलब्ध है?', 'बारह', ['दो', 'बाईस', 'पाँच']),
                 ('C1', 'ऐप में जाँच कौन करता है?', 'प्रशिक्षित पत्रकारों की टीम'),
                 ('C2', 'विज्ञापन की शुरुआत परिवार के व्हाट्सऐप समूह के उदाहरण से क्यों की गई है?', 'यह एक आम, परिचित अनुभव है जिससे पाठक तुरंत जुड़ जाता है और समस्या को अपनी समस्या मानकर समाधान (ऐप) की ओर आकर्षित होता है।'),
                 ('tf', 'विद्यार्थियों को ऐप के लिए शुल्क देना होगा।', 'गलत', '“विद्यार्थियों के लिए बिल्कुल मुफ़्त!”'),
                 ('C3', 'विज्ञापन में ‘प्रशिक्षित पत्रकारों की टीम’ का उल्लेख किस उद्देश्य से है?', 'ऐप की विश्वसनीयता स्थापित करने के लिए', ['पत्रकारों की नौकरी का विज्ञापन करने के लिए', 'ऐप की कमियाँ बताने के लिए', 'समाचार-पत्र बेचने के लिए']),
                 ('C3', 'विज्ञापन की दो भाषिक विशेषताएँ बताइए जो पाठक को कार्य करने के लिए प्रेरित करती हैं।', 'आज्ञार्थक/आदरसूचक क्रियाएँ (‘डालिए’, ‘जानिए’, ‘डाउनलोड कीजिए’); विस्मयादिबोधक वाक्य (‘अब घबराइए नहीं!’); पाठक से सीधा प्रश्न; मुफ़्त जैसा आकर्षक प्रस्ताव।'),
                 ('C4', 'क्या तथ्य-जाँच के लिए किसी एक ऐप पर निर्भर रहना पर्याप्त है? विज्ञापन के दावों को ध्यान में रखते हुए मूल्यांकन कीजिए।', 'लाभ: सुविधा, बहुभाषी, विशेषज्ञ जाँच। सीमाएँ: ऐप की अपनी विश्वसनीयता और पक्षपात, निजता (लिंक साझा करना), हर संदेश की जाँच में देरी; अपनी आलोचनात्मक सोच और कई स्रोत आवश्यक। निष्कर्ष।')]),
    ],
    tasks=[
        ('आपके विद्यालय में एक झूठी अफ़वाह फैली कि परीक्षाएँ रद्द हो गई हैं, जिससे बहुत भ्रम हुआ। विद्यालय-पत्रिका के लिए समाचार रिपोर्ट लिखिए।', 'news',
         ['घटना कब और कैसे हुई', 'विद्यार्थियों और अभिभावकों पर प्रभाव', 'प्रधानाचार्य का कथन और आगे के कदम']),
        ('किशोरों के बीच सोशल मीडिया के बढ़ते प्रयोग पर आपको अभिभावकों की सभा में बोलना है।', 'speech',
         ['सोशल मीडिया के लाभ', 'जोखिम: लत, साइबर-बुलिंग, निजता', 'अभिभावकों और किशोरों के लिए सुझाव']),
        ('आपके इलाक़े के केबल-चैनल पर बच्चों के कार्यक्रमों के बीच अनुचित विज्ञापन दिखाए जा रहे हैं। चैनल-प्रबंधक को पत्र लिखिए।', 'fletter',
         ['विज्ञापनों का विवरण', 'बच्चों पर प्रभाव', 'आपकी माँगें']),
        ('विद्यालय में ‘डिजिटल साक्षरता सप्ताह’ के लिए विद्यार्थियों हेतु पत्रक तैयार कीजिए।', 'brochure',
         ['फ़ेक न्यूज़ पहचानने के संकेत', 'ऑनलाइन निजता की सुरक्षा', 'मदद कहाँ से लें']),
        ('“समाचार-पत्र पढ़ने की आदत ख़त्म हो रही है।” — इस विषय पर अपनी विद्यालय-पत्रिका के लिए मत-प्रधान लेख लिखिए।', 'opinion',
         ['डिजिटल समाचार का बढ़ता प्रयोग', 'समाचार-पत्र के लाभ', 'आपका स्पष्ट निष्कर्ष']),
        ('आपने एक सप्ताह तक केवल रेडियो से समाचार सुने और सोशल मीडिया से दूर रहे।', 'blog',
         ['प्रयोग का कारण', 'आपको क्या अलग लगा', 'आपके निष्कर्ष']),
    ],
    discuss=[
        ('क्या सोशल मीडिया ने लोकतंत्र को मज़बूत किया है या कमज़ोर?', ['आम लोगों की आवाज़ और जागरूकता', 'फ़ेक न्यूज़ और ध्रुवीकरण', 'नियमन और डिजिटल साक्षरता']),
        ('क्या 16 वर्ष से कम उम्र के बच्चों के लिए सोशल मीडिया पर प्रतिबंध होना चाहिए?', ['सुरक्षा और मानसिक स्वास्थ्य', 'अभिव्यक्ति और सीखने के अवसर', 'अभिभावकों की निगरानी और शिक्षा']),
        ('क्या पत्रकारों को किसी भी हाल में अपने स्रोत गुप्त रखने चाहिए?', ['स्रोतों की सुरक्षा और खोजी पत्रकारिता', 'जवाबदेही और सत्यता', 'क़ानूनी और नैतिक सीमाएँ']),
        ('क्या विज्ञापन हमारी ज़रूरतें बनाते हैं या केवल बताते हैं?', ['उपभोक्तावाद और कृत्रिम इच्छाएँ', 'जानकारी और विकल्प', 'जागरूक उपभोक्ता']),
        ('क्या भविष्य में मुद्रित समाचार-पत्र पूरी तरह समाप्त हो जाएँगे?', ['डिजिटल की गति और पहुँच', 'मुद्रित की विश्वसनीयता और गहराई', 'दोनों का सह-अस्तित्व']),
    ],
)

FAKE = [
    ('“ज़रूरी सूचना!!! कल से सभी एटीएम एक सप्ताह के लिए बंद रहेंगे। तुरंत पैसे निकालें और यह संदेश दस लोगों को भेजें!”', 'कोई स्रोत या आधिकारिक संदर्भ नहीं; अनेक विस्मयादिबोधक चिह्न और घबराहट फैलाने वाली भाषा; ‘दस लोगों को भेजें’ का दबाव', 'बैंक या रिज़र्व बैंक की आधिकारिक वेबसाइट और विश्वसनीय समाचार-स्रोत देखें'),
    ('“वैज्ञानिकों ने सिद्ध किया है कि रोज़ एक चम्मच हल्दी खाने से कोई भी बीमारी नहीं होती।”', '‘वैज्ञानिकों’ का नाम, संस्था या शोध का संदर्भ नहीं; ‘कोई भी बीमारी’ जैसा अतिशयोक्तिपूर्ण दावा', 'प्रकाशित शोध, डॉक्टर या स्वास्थ्य मंत्रालय जैसे प्रामाणिक स्रोत से पुष्टि करें'),
    ('“यह तस्वीर देखिए — कल रात हमारे शहर में आई बाढ़!” (तस्वीर में दिख रही दुकानों के बोर्ड दूसरी भाषा और दूसरे देश के हैं)', 'तस्वीर के भीतर के संकेत (दूसरी भाषा के बोर्ड) दावे से मेल नहीं खाते; तारीख़ और स्रोत नहीं', 'रिवर्स इमेज सर्च से तस्वीर का मूल स्रोत और तारीख़ खोजें; स्थानीय समाचार देखें'),
    ('“प्रधानाचार्य ने घोषणा की है कि अगले सोमवार से विद्यालय का समय सुबह छह बजे होगा।” (भेजने वाला: अज्ञात नंबर)', 'अज्ञात भेजने वाला; विद्यालय के आधिकारिक माध्यम (वेबसाइट, सूचना-पत्र) का उल्लेख नहीं', 'विद्यालय की वेबसाइट, आधिकारिक ऐप या कक्षा-अध्यापक से पुष्टि करें'),
    ('“केवल आज! इस लिंक पर क्लिक करें और मुफ़्त में नया फ़ोन जीतें — बस अपना बैंक-विवरण भरें।”', 'अविश्वसनीय रूप से आकर्षक प्रस्ताव; बैंक-विवरण की माँग — ठगी (फ़िशिंग) का स्पष्ट संकेत; समय का दबाव', 'लिंक पर क्लिक न करें; कंपनी की आधिकारिक वेबसाइट देखें; साइबर-अपराध हेल्पलाइन पर सूचना दें'),
    ('“एक प्रसिद्ध अभिनेता का यह वीडियो देखिए जिसमें वे कह रहे हैं कि परीक्षाएँ बेकार हैं।” (वीडियो में होंठों की हरकत और आवाज़ मेल नहीं खाती)', 'संभवतः डीपफ़ेक — होंठ और आवाज़ का बेमेल; मूल स्रोत या चैनल का पता नहीं', 'अभिनेता के आधिकारिक खाते और विश्वसनीय समाचार देखें; तथ्य-जाँच वेबसाइटें खोजें'),
]


def g_fake(kit, key, th):
    def flags(rng, slot):
        p, f, v = rng.choice(FAKE)
        return dict(stem=f'आपको यह संदेश मिला है:\n{p}\nइस संदेश के भ्रामक या झूठा होने के दो संकेत पहचानिए और बताइए कि आप इसकी पुष्टि कैसे करेंगे।',
                    answer=f'संकेत: {f}। पुष्टि: {v}।', type='short', marks=3,
                    markingKey=f'2 अंक: दो उचित संकेत ({f}); 1 अंक: पुष्टि का व्यावहारिक तरीका ({v})।')
    kit.add(key, 'C3', (2, 4), flags, 'short', None, 'fake_flags')

    def reply(rng, slot):
        p, f, v = rng.choice(FAKE)
        return dict(stem=f'आपके परिवार के व्हाट्सऐप समूह में किसी रिश्तेदार ने यह संदेश भेजा है:\n{p}\nउन्हें विनम्रता से समझाते हुए 50–70 शब्दों का उत्तर लिखिए, ताकि वे इसे आगे न भेजें।',
                    answer=f'अपेक्षित: विनम्र, आदरसूचक लहजा; संदेश के संदिग्ध होने के कारण ({f}); पुष्टि का तरीका ({v}); आगे न भेजने का अनुरोध।', type='explain', marks=4,
                    markingKey='1 अंक उपयुक्त आदरसूचक रजिस्टर, 2 अंक तर्क (संकेत और पुष्टि), 1 अंक स्पष्ट अनुरोध और शुद्ध भाषा।')
    kit.add(key, 'C4', (2, 4), reply, 'explain', None, 'fake_reply')


SPEC['ch11-st1'] = ('reading', dict(focus='लेखन में समाचार और संपादकीय की भाषा का अंतर स्पष्ट दिखाइए।', items=[
    ('C1', 'समाचार रिपोर्ट की भाषा की मुख्य विशेषता क्या है?', 'तथ्यात्मक, निष्पक्ष और तृतीय पुरुष', ['भावनात्मक और प्रथम पुरुष', 'काव्यात्मक और अलंकृत', 'केवल प्रश्नवाचक'], 'समाचार तथ्य देता है, लेखक की राय नहीं।'),
    ('C1', 'समाचार-लेखन की ‘उल्टा पिरामिड’ शैली का अर्थ क्या है?', 'सबसे महत्वपूर्ण जानकारी पहले, कम महत्वपूर्ण विवरण बाद में', ['कहानी का अंत पहले बताना', 'सबसे कम महत्वपूर्ण बात पहले', 'केवल चित्रों से समाचार देना'], 'पाठक पहले अनुच्छेद से ही मुख्य बात जान लेता है।'),
    ('C2', 'समाचार रिपोर्ट और संपादकीय की भाषा में दो प्रमुख अंतर उदाहरण सहित बताइए।', 'समाचार निष्पक्ष, तथ्यात्मक और प्रायः कर्मवाच्य में (“सम्मानित किया गया”); संपादकीय में स्पष्ट मत, मूल्यांकनपरक शब्द, अलंकारिक प्रश्न और अपील (“मीडिया को विश्वसनीयता को अपनी पहचान बनाना होगा”)।', '1-1 अंक प्रत्येक अंतर, 1 अंक उदाहरण।', 3),
    ('C2', 'समाचार रिपोर्ट में प्रायः कर्मवाच्य (“अपील की गई”, “सम्मानित किया गया”) का प्रयोग क्यों किया जाता है?', 'कर्मवाच्य कार्य/घटना पर ध्यान केंद्रित करता है, कर्ता पर नहीं; इससे भाषा औपचारिक, वस्तुनिष्ठ और निष्पक्ष लगती है।', '1 अंक ध्यान-केंद्र, 1 अंक औपचारिकता/निष्पक्षता।'),
]))
SPEC['ch11-st2'] = ('writing', dict(tt='news', tasks=[
    ('आपके विद्यालय के विद्यार्थियों ने राज्य-स्तरीय रोबोटिक्स प्रतियोगिता जीती है। स्थानीय समाचार-पत्र के लिए रिपोर्ट लिखिए।', ['प्रतियोगिता का विवरण (कब, कहाँ, कितने दल)', 'जीतने वाले दल और उनका रोबोट', 'प्रधानाचार्य या दल के सदस्य का कथन']),
    ('आपके शहर में भारी बारिश के कारण कई इलाक़ों में पानी भर गया। समाचार-वेबसाइट के लिए रिपोर्ट लिखिए।', ['प्रभावित क्षेत्र और नुक़सान', 'प्रशासन और स्वयंसेवकों के राहत-कार्य', 'प्रत्यक्षदर्शियों के कथन और मौसम-विभाग की चेतावनी']),
    ('आपके विद्यालय में ‘पुस्तक-दान अभियान’ से दो हज़ार पुस्तकें इकट्ठी हुईं। विद्यालय-पत्रिका के लिए रिपोर्ट लिखिए।', ['अभियान का उद्देश्य और अवधि', 'परिणाम और पुस्तकें किसे दी जाएँगी', 'आयोजकों के कथन']),
    ('आपके शहर में एक अंतरराष्ट्रीय साहित्य-उत्सव हुआ जिसमें कई हिंदी लेखक आए। समाचार-पत्र के लिए रिपोर्ट लिखिए।', ['उत्सव का विवरण', 'मुख्य वक्ता और चर्चित सत्र', 'दर्शकों की प्रतिक्रिया']),
    ('आपके इलाक़े में साइबर-ठगी के मामलों के बाद पुलिस ने विद्यालयों में जागरूकता-शिविर लगाया। स्थानीय समाचार-पत्र के लिए रिपोर्ट लिखिए।', ['शिविर कब और कहाँ', 'विद्यार्थियों को क्या सिखाया गया', 'पुलिस अधिकारी का कथन और हेल्पलाइन']),
], items=[
    ('C1', 'समाचार रिपोर्ट का पहला अनुच्छेद (आमुख) किन प्रश्नों का उत्तर देता है?', 'कौन, क्या, कब, कहाँ, क्यों और कैसे', ['लेखक कौन है और उसकी राय क्या है', 'पाठक को क्या ख़रीदना चाहिए', 'कहानी का अंत क्या है'], 'आमुख में मुख्य तथ्य होते हैं — पाँच ‘क’ और एक ‘कैसे’।'),
    ('C2', 'समाचार रिपोर्ट में प्रत्यक्षदर्शियों या अधिकारियों के उद्धरण क्यों दिए जाते हैं?', 'वे रिपोर्ट को प्रामाणिक और विश्वसनीय बनाते हैं, घटना को मानवीय दृष्टिकोण देते हैं और पत्रकार की निजी राय के बिना विभिन्न पक्ष सामने लाते हैं।', '1 अंक प्रामाणिकता, 1 अंक निष्पक्षता/मानवीय पक्ष।'),
    ('C3', 'इस वाक्य को निष्पक्ष समाचार-भाषा में बदलिए: “हमारे शानदार विद्यार्थियों ने कमाल कर दिया और सबको हरा दिया!”', 'नमूना: “विद्यालय के विद्यार्थियों ने प्रतियोगिता में प्रथम स्थान प्राप्त किया।”', '1 अंक भावनात्मक/निजी शब्द हटाने पर, 1 अंक तथ्यात्मक, तृतीय पुरुष की शुद्ध भाषा।', 2),
]))
SPEC['ch11-st3'] = ('none', dict(focus='लेखन में सोशल मीडिया और डिजिटल साक्षरता से जुड़े व्यावहारिक सुझाव दीजिए।', gens=[g_fake, lambda kit, key, th: kit.texts(key, th, 'texts', 'p2r'), lambda kit, key, th: kit.vocab(key, th, ('c2',))], items=[
    ('C1', '‘फ़ेक न्यूज़’ का सबसे सटीक अर्थ क्या है?', 'जानबूझकर या असावधानी से फैलाई गई झूठी या भ्रामक जानकारी जो समाचार जैसी दिखती है', ['कोई भी पुराना समाचार', 'केवल व्यंग्य-लेख', 'सरकारी घोषणा'], 'फ़ेक न्यूज़ समाचार का रूप धरकर ग़लत जानकारी फैलाती है।'),
    ('C1', '‘डीपफ़ेक’ किसे कहते हैं?', 'कृत्रिम बुद्धिमत्ता से बनाया गया नकली वीडियो या ऑडियो जो असली जैसा लगे', ['बहुत पुरानी तस्वीर', 'टूटा हुआ लिंक', 'धीमा इंटरनेट'], 'डीपफ़ेक में किसी व्यक्ति का चेहरा या आवाज़ नकली रूप से जोड़ी जाती है।'),
    ('C1', 'ऑनलाइन ठगी (फ़िशिंग) का सबसे आम संकेत क्या है?', 'इनाम के बदले बैंक-विवरण या पासवर्ड माँगना', ['आधिकारिक वेबसाइट पर सूचना', 'बिना लिंक का समाचार', 'शिक्षक का ईमेल'], 'कोई भी विश्वसनीय संस्था पासवर्ड या ओटीपी नहीं माँगती।'),
    ('C2', '‘ग़लत सूचना’ (अनजाने में फैली) और ‘दुष्प्रचार’ (जानबूझकर फैलाई गई) में अंतर स्पष्ट कीजिए।', 'ग़लत सूचना बिना बुरी नीयत के, असावधानी से साझा की गई ग़लत जानकारी है (जैसे रिश्तेदार का बिना जाँचे संदेश आगे भेजना); दुष्प्रचार किसी उद्देश्य (राजनीतिक, आर्थिक) से जानबूझकर फैलाया गया झूठ है।', '1-1 अंक प्रत्येक अर्थ, 1 अंक नीयत के अंतर पर।', 3),
    ('C2', '‘डिजिटल साक्षरता’ केवल कंप्यूटर चलाना जानने से अधिक क्यों है? समझाइए।', 'डिजिटल साक्षरता में ऑनलाइन जानकारी को परखना, स्रोत की विश्वसनीयता जाँचना, निजता की रक्षा, साइबर-सुरक्षा और ज़िम्मेदार व्यवहार शामिल है — केवल तकनीकी कौशल नहीं।', '1 अंक तकनीकी बनाम आलोचनात्मक कौशल, 1 अंक उदाहरण।'),
    ('C2', 'सोशल मीडिया के ‘एल्गोरिद्म’ उपयोगकर्ता को ‘इको-चैंबर’ (एक जैसी राय की प्रतिध्वनि) में कैसे फँसा सकते हैं?', 'एल्गोरिद्म वही सामग्री अधिक दिखाते हैं जो हम पहले पसंद कर चुके हैं; इससे हमें केवल अपने जैसे विचार दिखते हैं, विरोधी मत नहीं — हमारी सोच संकुचित और पूर्वाग्रह मज़बूत होता है।', '1 अंक एल्गोरिद्म की कार्य-प्रणाली, 1 अंक प्रभाव।'),
    ('C4', '“फ़ेक न्यूज़ रोकने की ज़िम्मेदारी सोशल मीडिया कंपनियों की है, उपयोगकर्ताओं की नहीं।” — इस कथन से आप कहाँ तक सहमत हैं? (120–150 शब्द)', 'कंपनियाँ: एल्गोरिद्म, तथ्य-जाँच, लेबल, फ़र्ज़ी खातों पर कार्रवाई। उपयोगकर्ता: आगे भेजने से पहले पुष्टि, डिजिटल साक्षरता। सरकार: नियमन, पर अभिव्यक्ति की स्वतंत्रता का संतुलन। स्पष्ट, संतुलित निष्कर्ष।', 'मत (1), कंपनियों की भूमिका (2), उपयोगकर्ताओं की भूमिका (2), निष्कर्ष और भाषा (1)।', 6),
]))



# --------------------------------------------------------------------------------------------
# ch12 – HL literary work 1: prose fiction (original extracts + Premchand in general terms)
# --------------------------------------------------------------------------------------------
TH[12] = dict(
    name='साहित्य: गद्य कथा-साहित्य',
    vocab=[
        ('कथानक', 'कहानी की घटनाओं का क्रमबद्ध ढाँचा', 'कथावस्तु', 'इस कहानी का ____ एक गरीब किसान की एक रात के इर्द-गिर्द घूमता है।'),
        ('चरमोत्कर्ष', 'कहानी का वह बिंदु जहाँ संघर्ष सबसे तीव्र होता है', 'पराकाष्ठा', 'कहानी का ____ तब आता है जब नायक रिश्वत ठुकरा देता है।'),
        ('पात्र-चित्रण', 'कहानी के पात्रों के स्वभाव और व्यक्तित्व का वर्णन', 'चरित्र-चित्रण', 'लेखक का ____ इतना सजीव है कि हामिद हमें अपने आसपास का बच्चा लगता है।'),
        ('परिवेश', 'कहानी का स्थान, समय और वातावरण', 'पृष्ठभूमि', 'कहानी का ____ बीसवीं सदी के आरंभ का एक गाँव है।'),
        ('द्वंद्व', 'पात्र के मन में या पात्रों के बीच का संघर्ष', 'अंतर्विरोध', 'नायक के मन में कर्तव्य और लोभ का ____ चल रहा था।'),
        ('कथावाचक', 'वह जो कहानी सुनाता है', 'सूत्रधार', 'इस कहानी का ____ स्वयं छोटा भाई है, इसलिए हम सब कुछ उसी की आँखों से देखते हैं।'),
        ('व्यंग्य', 'हास्य के सहारे किसी बुराई पर चोट करना', 'कटाक्ष', 'लेखक ने रिश्वतख़ोरी पर तीखा ____ किया है।'),
        ('प्रतीक', 'वह वस्तु जो किसी बड़े विचार का संकेत दे', 'चिह्न', 'कहानी में चिमटा दादी के प्रति प्रेम और त्याग का ____ है।'),
        ('यथार्थवाद', 'जीवन को जैसा है वैसा ही चित्रित करने की प्रवृत्ति', 'वास्तविकतावाद', 'प्रेमचंद के ____ में गाँव की गरीबी बिना सजावट के दिखाई देती है।'),
        ('विडंबना', 'अपेक्षा और वास्तविकता के बीच का कटु अंतर', 'विरोधाभास', 'यह ____ ही है कि कफ़न के पैसों से शराब ख़रीदी गई।'),
        ('पूर्वाभास', 'आगे होने वाली घटना का पहले से मिलने वाला संकेत', 'पूर्व-संकेत', 'आरंभ में बादलों का घिरना आने वाले संकट का ____ देता है।'),
        ('आंचलिक', 'किसी विशेष क्षेत्र की भाषा और जीवन से जुड़ा', 'क्षेत्रीय', 'इस उपन्यास की ____ भाषा में बिहार के गाँवों की सुगंध है।'),
        ('मनोवैज्ञानिक', 'मन की भावनाओं और विचारों से संबंधित', 'मानसिक', 'लेखक ने नायक की बेचैनी का सूक्ष्म ____ विश्लेषण किया है।'),
        ('संवेदना', 'दूसरों के दुख को अनुभव करने की भावना', 'सहानुभूति', 'कहानी पढ़कर पाठक के मन में किसानों के प्रति गहरी ____ जागती है।'),
    ],
    topics=['प्रेमचंद की कहानियों में गाँव', 'बाल-मन का चित्रण', 'ईमानदारी और भ्रष्टाचार', 'गरीबी और शोषण', 'स्त्री पात्रों की भूमिका',
            'कहानी में प्रतीकों का प्रयोग', 'कथावाचक की दृष्टि'],
    texts=[
        dict(kind='कहानी का अंश', title='बरगद वाली बुआ',
             body='गाँव के बीचोंबीच खड़ा बरगद जितना पुराना था, बुआ उससे कुछ ही कम पुरानी लगती थीं। सुबह होते ही वे उसके चबूतरे पर आ बैठतीं और आने-जाने वालों का हाल पूछतीं। '
                  'उस दिन शहर से उनका बेटा रमेश आया था। उसने चमकते जूते उतारे बिना ही कहा, “अम्मा, अब बहुत हुआ। सामान बाँध लो, कल सुबह की गाड़ी से शहर चलना है।” '
                  'बुआ ने बरगद की एक लटकती जटा को अपनी उँगलियों में लपेट लिया, जैसे कोई बच्चा माँ का आँचल पकड़ लेता है। “शहर में मेरा बरगद कहाँ होगा, बेटा?” '
                  'रमेश हँसा, “वहाँ पार्क है, अम्मा। बेंचें हैं, फव्वारा है।” बुआ चुप रहीं। उनकी आँखों के सामने वे सब चेहरे घूम गए जिन्होंने इसी चबूतरे पर बैठकर अपने दुख-सुख कहे थे। '
                  'रात को आँगन में लेटे-लेटे उन्होंने सुना कि रमेश फ़ोन पर किसी से कह रहा है, “हाँ, मकान का सौदा पक्का समझो, अम्मा को मना लूँगा।” '
                  'बुआ के भीतर कुछ टूट गया, पर उनके चेहरे पर एक शांत मुस्कान आ गई। सुबह जब रमेश ने गाड़ी का हॉर्न बजाया, तो बुआ चबूतरे पर बैठी थीं, हाथ में वही जटा थी। '
                  '“तू जा बेटा,” उन्होंने कहा, “बरगद की जड़ें उखाड़कर दूसरी जगह नहीं लगतीं।”',
             qs=[('C1', 'रमेश अपनी माँ को कहाँ ले जाना चाहता था?', 'शहर', ['मंदिर', 'मायके', 'अस्पताल']),
                 ('C1', 'बुआ सुबह-सुबह कहाँ जाकर बैठती थीं?', 'बरगद के चबूतरे पर'),
                 ('C1', 'रात को रमेश फ़ोन पर किस बात का सौदा पक्का कर रहा था?', 'गाँव के मकान का'),
                 ('C2', '“जैसे कोई बच्चा माँ का आँचल पकड़ लेता है” — इस उपमा से बुआ और बरगद के संबंध के बारे में क्या पता चलता है?', 'बुआ बरगद से उसी तरह भावनात्मक रूप से जुड़ी हैं और उस पर निर्भर हैं, जैसे बच्चा माँ से; बरगद उनके लिए सुरक्षा और अपनापन है।'),
                 ('tf', 'बुआ ने बेटे के साथ शहर जाने का निर्णय लिया।', 'गलत', '“तू जा बेटा … बरगद की जड़ें उखाड़कर दूसरी जगह नहीं लगतीं।”'),
                 ('C3', 'रमेश के “चमकते जूते उतारे बिना” बात करने का विवरण उसके चरित्र के बारे में क्या संकेत देता है?', 'वह गाँव और माँ की भावनाओं से कट चुका, जल्दबाज़ और शहरी दिखावे वाला व्यक्ति है', ['वह बहुत विनम्र और धैर्यवान है', 'उसके जूते नए थे इसलिए उसे गर्व था', 'वह गाँव में बहुत दिन रुकना चाहता था']),
                 ('C3', 'अंतिम वाक्य में ‘बरगद की जड़ें’ किसका प्रतीक हैं? पाठ के आधार पर समझाइए।', 'बुआ की अपनी जड़ों — गाँव, स्मृतियों, समुदाय और पहचान — का; जैसे पुराना पेड़ उखाड़कर दूसरी जगह नहीं लगता, वैसे ही बुआ भी अपने परिवेश से अलग होकर जी नहीं सकतीं।'),
                 ('C4', 'क्या बुआ का निर्णय सही था? पीढ़ियों के बीच के अंतर और शहरीकरण के संदर्भ में अपना मत दीजिए।', 'पक्ष: पहचान, आत्मसम्मान, समुदाय; रमेश का स्वार्थ (मकान का सौदा)। विपक्ष: बुढ़ापे में अकेलापन, स्वास्थ्य-सुविधाओं की कमी। संतुलित निष्कर्ष: बुज़ुर्गों की इच्छा का सम्मान और संवाद आवश्यक।'),
             ]),
        dict(kind='कहानी का अंश', title='आख़िरी बस',
             body='मैं जब हाँफता हुआ बस-अड्डे पहुँचा, तब तक आख़िरी बस की लाल बत्तियाँ मोड़ पर ओझल हो चुकी थीं। जेब में कुल बीस रुपये थे और घर पैंतीस किलोमीटर दूर। '
                  'अड्डे पर एक टूटी बेंच, एक बुझता हुआ बल्ब और कोने में चाय का एक ढाबा था। ढाबे वाला बूढ़ा अपनी भट्ठी समेट रहा था। मैंने सोचा, अजनबी पर भरोसा करना ठीक नहीं; माँ यही तो कहती थीं। '
                  'पर ठंड बढ़ती जा रही थी। आख़िरकार मैं ढाबे के पास जाकर खड़ा हो गया। बूढ़े ने मुझे ऊपर से नीचे तक देखा और बिना कुछ पूछे एक गिलास चाय मेरी ओर बढ़ा दी। '
                  '“पैसे?” मैंने संकोच से पूछा। “पहले पी लो, बेटा। हिसाब ऊपर वाला रखता है,” वह हँसा। फिर उसने अपने ट्रक-ड्राइवर भतीजे को फ़ोन किया, जो सुबह चार बजे उसी रास्ते से जाने वाला था। '
                  'रात मैंने ढाबे की बेंच पर उसके पुराने कंबल में बिताई। नींद कम आई, पर डर उससे भी कम था। '
                  'आज इतने बरस बाद भी, जब कोई मुझसे पूछता है कि दुनिया अच्छी है या बुरी, तो मुझे वह गिलास याद आता है — टूटी किनारी वाला, पर गर्म।',
             qs=[('C1', 'कथावाचक के पास कितने रुपये थे?', 'बीस रुपये', ['पैंतीस रुपये', 'दस रुपये', 'पचास रुपये']),
                 ('C1', 'कथावाचक का घर बस-अड्डे से कितनी दूर था?', 'पैंतीस किलोमीटर'),
                 ('C1', 'ढाबे वाले ने कथावाचक को घर पहुँचाने के लिए किसे फ़ोन किया?', 'अपने ट्रक-ड्राइवर भतीजे को'),
                 ('C2', 'कथावाचक पहले ढाबे वाले के पास जाने से क्यों हिचक रहा था? अपने शब्दों में समझाइए।', 'माँ ने अजनबियों पर भरोसा न करने की सीख दी थी, इसलिए वह डरा हुआ और संकोच में था; ठंड बढ़ने पर ही वह गया।'),
                 ('tf', 'ढाबे वाले ने चाय देने से पहले कथावाचक से पैसे माँगे।', 'गलत', '“पहले पी लो, बेटा। हिसाब ऊपर वाला रखता है।”'),
                 ('C3', 'कहानी किस दृष्टि (कथन-दृष्टि) से कही गई है और इसका पाठक पर क्या प्रभाव पड़ता है?', 'प्रथम पुरुष (‘मैं’) में, जिससे पाठक कथावाचक के डर और राहत को सीधे अनुभव करता है', ['तृतीय पुरुष सर्वज्ञ दृष्टि से, जिससे पाठक सबके मन की बात जानता है', 'संवाद-शैली में, जिसमें कोई कथावाचक नहीं है', 'डायरी के रूप में, जिससे तारीख़ें स्पष्ट होती हैं']),
                 ('C3', '“टूटी किनारी वाला, पर गर्म” — अंतिम पंक्ति में गिलास का यह वर्णन कहानी के मुख्य विचार को कैसे व्यक्त करता है?', 'गिलास ढाबे वाले जैसा है — गरीब और साधारण (टूटी किनारी), पर मन से उदार (गर्म); यह दिखाता है कि मनुष्यता बाहरी हालत पर नहीं, हृदय पर निर्भर है और दुनिया में अच्छाई बची है।'),
                 ('C4', '“अजनबी पर भरोसा करना ठीक नहीं।” — इस कहानी और आज के समाज के संदर्भ में इस सीख का मूल्यांकन कीजिए।', 'सावधानी आवश्यक (ऑनलाइन ठगी, सुरक्षा), पर हर अजनबी बुरा नहीं; कहानी दिखाती है कि करुणा और विश्वास से समाज टिकता है। संतुलन: विवेक के साथ भरोसा।'),
             ]),
        dict(kind='कहानी का अंश', title='मेले की पायल',
             body='गुड़िया ने पूरे साल गुल्लक में सिक्के जोड़े थे। उसका सपना था कि दशहरे के मेले से चाँदी जैसी चमकती पायल ख़रीदेगी, जैसी मुखिया की बेटी पहनती थी। '
                  'मेले में पहुँचते ही रंग-बिरंगी दुकानों ने उसे घेर लिया। चूड़ियों की खनक, जलेबी की महक, झूलों की चीख़ें — सब उसे बुला रहे थे। पायल वाली दुकान पर उसने गुल्लक के सारे पैसे गिने; पूरे अड़तालीस रुपये। पायल पचास की थी। '
                  'दुकानदार ने मुँह बनाया, पर फिर बोला, “चल, अड़तालीस में ले जा।” गुड़िया का मन नाच उठा। तभी उसकी नज़र बगल की दुकान पर पड़ी, जहाँ एक प्लास्टिक का चश्मा टँगा था। '
                  'उसे याद आया कि बापू खेत में धूप से आँखें मिचमिचाते रहते हैं और रात को आँखें मलते हुए सोते हैं। उसने पायल को एक बार और देखा, फिर धीरे से उसे वापस रख दिया। '
                  'शाम को जब बापू ने वह धूप का चश्मा पहना, तो वे किसी फ़िल्मी हीरो की तरह अकड़कर चले और सारा घर हँसी से भर गया। गुड़िया के पाँव सूने थे, पर उसे लगा, उसके भीतर कहीं पायल बज रही है।',
             qs=[('C1', 'गुड़िया मेले से क्या ख़रीदना चाहती थी?', 'पायल', ['चूड़ियाँ', 'जलेबी', 'गुल्लक']),
                 ('C1', 'गुड़िया की गुल्लक में कुल कितने रुपये थे?', 'अड़तालीस रुपये'),
                 ('C1', 'गुड़िया ने अंततः बापू के लिए क्या ख़रीदा?', 'धूप का चश्मा'),
                 ('C2', 'मेले के वर्णन में लेखक ने किन-किन इंद्रियों (ध्वनि, गंध आदि) का प्रयोग किया है? दो उदाहरण देकर उनका प्रभाव बताइए।', 'ध्वनि — चूड़ियों की खनक, झूलों की चीख़ें; गंध — जलेबी की महक; दृश्य — रंग-बिरंगी दुकानें। इससे मेला सजीव और आकर्षक लगता है और गुड़िया का लालच समझ में आता है।'),
                 ('tf', 'पायल का दाम गुड़िया के पैसों से अधिक था।', 'सही', '“पूरे अड़तालीस रुपये। पायल पचास की थी।”'),
                 ('C3', 'गुड़िया का पायल वापस रख देना उसके चरित्र के बारे में क्या दिखाता है?', 'वह अपनी इच्छा से ऊपर परिवार के प्रति प्रेम और त्याग को रखती है', ['वह पायल को पसंद नहीं करती थी', 'उसे दुकानदार पर भरोसा नहीं था', 'वह मुखिया की बेटी से ईर्ष्या करती थी']),
                 ('C3', '“उसके भीतर कहीं पायल बज रही है” — इस अंतिम पंक्ति का भाव स्पष्ट कीजिए।', 'बाहरी पायल न होने पर भी गुड़िया को त्याग से जो आंतरिक आनंद और संतोष मिला, वह पायल की खनक जैसा है; सच्चा सुख वस्तु में नहीं, दूसरों को खुश करने में है।'),
                 ('C4', 'इस अंश की तुलना प्रेमचंद की कहानी ‘ईदगाह’ से कीजिए। दोनों में बाल-मन और त्याग का चित्रण कैसे हुआ है?', 'ईदगाह में हामिद खिलौनों के बजाय दादी अमीना के लिए चिमटा ख़रीदता है; यहाँ गुड़िया पायल के बजाय बापू के लिए चश्मा। दोनों में गरीबी, बच्चे की परिपक्वता, वस्तु का प्रतीकात्मक अर्थ और भावनात्मक अंत।'),
             ]),
    ],
    tasks=[
        ('आपकी कक्षा ने प्रेमचंद की एक कहानी पढ़ी है। विद्यालय-पत्रिका के लिए उस कहानी की समीक्षा लिखिए।', 'review',
         ['कहानी का संक्षिप्त परिचय', 'पात्र और भाषा की विशेषताएँ', 'आज के पाठक के लिए प्रासंगिकता']),
        ('‘ईदगाह’ का हामिद मेले से लौटकर उस रात अपनी डायरी लिखता है।', 'diary',
         ['मेले के अनुभव', 'चिमटा ख़रीदने का निर्णय', 'दादी की प्रतिक्रिया पर उसकी भावनाएँ']),
        ('आप ‘नमक का दारोगा’ के मुंशी वंशीधर हैं। नौकरी से निकाले जाने के बाद अपने पिता को पत्र लिखिए।', 'pletter',
         ['घटना का विवरण', 'आपने रिश्वत क्यों नहीं ली', 'भविष्य के बारे में आपके विचार']),
        ('विद्यालय के साहित्य-क्लब में आपको ‘क्या प्रेमचंद आज भी प्रासंगिक हैं?’ विषय पर बोलना है।', 'speech',
         ['प्रेमचंद के प्रमुख विषय', 'आज के समाज से समानताएँ', 'युवाओं के लिए संदेश']),
        ('एक साहित्यिक ब्लॉग के लिए लिखिए कि किसी एक कहानी ने आपकी सोच कैसे बदली।', 'blog',
         ['कहानी और उसका मुख्य पात्र', 'कहानी का आप पर प्रभाव', 'पाठकों को सुझाव']),
        ('आपने अपने विद्यालय के पुस्तकालयाध्यक्ष का साक्षात्कार लिया कि आज के किशोर साहित्य क्यों कम पढ़ते हैं।', 'interview',
         ['पढ़ने की आदत में बदलाव', 'डिजिटल माध्यम का प्रभाव', 'पढ़ने को बढ़ावा देने के उपाय']),
    ],
    discuss=[
        ('क्या साहित्य समाज का दर्पण है या समाज को बदलने का साधन?', ['प्रेमचंद का यथार्थवाद समाज दिखाता है', 'सुधारवादी दृष्टि बदलाव की प्रेरणा देती है', 'पाठक की संवेदना जगाना']),
        ('क्या सौ साल पुरानी कहानियाँ आज के किशोरों को आकर्षित कर सकती हैं?', ['मानवीय भावनाएँ नहीं बदलतीं', 'भाषा और परिवेश की कठिनाई', 'शिक्षक और रूपांतरण (फ़िल्म, नाटक) की भूमिका']),
        ('क्या किसी कहानी का अंत दुखद होना उसे अधिक प्रभावशाली बनाता है?', ['दुखद अंत पाठक को सोचने पर मजबूर करता है', 'आशावादी अंत प्रेरणा देता है', 'अंत कहानी के उद्देश्य पर निर्भर']),
        ('कहानी में बच्चे को मुख्य पात्र बनाने से लेखक को क्या लाभ होता है?', ['मासूम दृष्टि से बड़ों की दुनिया की आलोचना', 'पाठक की सहानुभूति', 'सरल भाषा में गहरी बात']),
        ('क्या ईमानदारी का फल हमेशा मीठा होता है, जैसा ‘नमक का दारोगा’ में दिखाया गया है?', ['कहानी में अंततः सम्मान मिलता है', 'वास्तविक जीवन में संघर्ष और हानि', 'आत्मसम्मान सबसे बड़ा पुरस्कार']),
        ('क्या साहित्य को अनुवाद में पढ़ने से उसकी आत्मा खो जाती है?', ['मुहावरे और आंचलिकता खो सकती है', 'अनुवाद से वैश्विक पाठक मिलते हैं', 'अच्छे अनुवादक की भूमिका']),
    ],
    pics=[
        ('एक गाँव के मेले का दृश्य — रंगीन दुकानें, एक छोटा लड़का हाथ में लोहे का चिमटा लिए खड़ा है, उसके दोस्त खिलौने लिए हँस रहे हैं।', ['मेले का माहौल', 'बच्चे का अलग चुनाव', '‘ईदगाह’ से संबंध: त्याग और प्रेम']),
        ('जाड़े की रात, खेत के किनारे एक किसान अलाव के पास कंबल के बिना बैठा है और उसका कुत्ता उससे सटकर लेटा है।', ['ठंड और गरीबी', 'मनुष्य और पशु का संबंध', '‘पूस की रात’ से संबंध: किसान का शोषण']),
        ('एक पुस्तकालय में किशोर हाथों में मोबाइल लिए बैठे हैं, जबकि अलमारियों में पुरानी हिंदी किताबें धूल खा रही हैं।', ['पढ़ने की बदलती आदतें', 'डिजिटल माध्यम', 'साहित्य को जीवित रखने के उपाय']),
    ],
)

LIT_DEVICES = [
    ('उसकी आँखें दो दीयों की तरह चमक उठीं।', 'उपमा', 'आँखों की चमक की तुलना ‘की तरह’ से दीयों से की गई है; इससे बच्चे की ख़ुशी दृश्य रूप में सामने आती है।'),
    ('दादी के हाथ सूखी लकड़ी जैसे थे।', 'उपमा', '‘जैसे’ से हाथों की तुलना सूखी लकड़ी से — बुढ़ापा और कठोर परिश्रम का संकेत।'),
    ('माँ घर की धुरी थी।', 'रूपक', 'माँ को सीधे ‘धुरी’ कह दिया गया (‘जैसे’ के बिना), जिससे पता चलता है कि पूरा घर उन्हीं पर टिका है।'),
    ('उसका हृदय पत्थर हो चुका था।', 'रूपक', 'हृदय को ही पत्थर बताया गया है; पात्र की संवेदनहीनता पर ज़ोर।'),
    ('बूढ़ा पीपल हवा में सिर हिलाकर हामी भर रहा था।', 'मानवीकरण', 'पेड़ को मनुष्य की तरह ‘हामी भरते’ दिखाया गया; प्रकृति कहानी में साथी-पात्र बन जाती है।'),
    ('रात ने गाँव को अपनी काली चादर में लपेट लिया।', 'मानवीकरण', 'रात को मनुष्य की तरह चादर लपेटते दिखाया गया; अँधेरे और रहस्य का वातावरण बनता है।'),
    ('दारोगा जी इतने ईमानदार थे कि रिश्वत की पूरी गठरी ‘भेंट’ में लेकर ही घर लौटते थे।', 'व्यंग्य', 'ऊपर से प्रशंसा, भीतर से भ्रष्टाचार पर चोट; हास्य के सहारे आलोचना।'),
    ('जिस किसान ने सबका पेट भरा, उसी के घर में चूल्हा नहीं जला।', 'विडंबना', 'अपेक्षा (अन्नदाता के पास अनाज होगा) और वास्तविकता (भूख) का कटु अंतर — शोषण पर टिप्पणी।'),
    ('कफ़न के लिए जुटाए पैसों से उन्होंने उस रात दावत उड़ाई।', 'विडंबना', 'जो पैसा मृतक के सम्मान के लिए था, वही भोग पर ख़र्च हुआ — गरीबी से उपजी संवेदनहीनता का कटु चित्र।'),
    ('उसने इतना रोया कि गाँव की नदी में बाढ़ आ गई।', 'अतिशयोक्ति', 'बात को बहुत बढ़ा-चढ़ाकर कहा गया है ताकि दुख की तीव्रता पर ज़ोर पड़े।'),
    ('सुबह से ही आसमान में चीलें मँडरा रही थीं।', 'पूर्वाभास', 'चीलों का मँडराना किसी अशुभ घटना या मृत्यु का संकेत देता है जो आगे घटने वाली है।'),
    ('दरवाज़े पर लटका ताला अब भी जंग खा रहा था।', 'प्रतीक', 'जंग लगा ताला बंद अवसरों, उपेक्षा और रुके हुए जीवन का प्रतीक है।'),
    ('“मुझे क्या करना चाहिए? अगर मैं पैसे ले लूँ तो… नहीं, नहीं!” वह मन ही मन बड़बड़ाया।', 'आंतरिक एकालाप', 'पात्र के मन के भीतर का द्वंद्व सीधे पाठक के सामने आता है।'),
    ('रोटी, रोटी और बस रोटी — यही उसके जीवन का एकमात्र सपना था।', 'पुनरावृत्ति', 'एक ही शब्द को दोहराकर भूख और अभाव की तीव्रता पर ज़ोर दिया गया है।'),
]
DEVICE_NAMES = ['उपमा', 'रूपक', 'मानवीकरण', 'व्यंग्य', 'विडंबना', 'अतिशयोक्ति', 'पूर्वाभास', 'प्रतीक', 'आंतरिक एकालाप', 'पुनरावृत्ति']

NARR = [
    ('मैं जब घर पहुँचा तो दरवाज़ा खुला था और भीतर से किसी के रोने की आवाज़ आ रही थी।', 'प्रथम पुरुष (‘मैं’) कथावाचक', 'पाठक केवल वही जानता है जो कथावाचक देखता-सुनता है; रहस्य और आत्मीयता बनती है।'),
    ('रामू सोच रहा था कि मालिक नाराज़ होंगे, जबकि मालिक मन ही मन उसकी ईमानदारी से प्रसन्न थे।', 'तृतीय पुरुष सर्वज्ञ कथावाचक', 'कथावाचक दोनों पात्रों के मन की बात जानता है; पाठक को पूरी तस्वीर मिलती है।'),
    ('मीना ने खिड़की से बाहर देखा। उसे लगा, आज कुछ अलग होगा, पर क्या, वह नहीं जानती थी।', 'सीमित तृतीय पुरुष कथावाचक', '‘वह’ से कथा कही जाती है, पर केवल एक पात्र (मीना) के मन तक पहुँच है।'),
    ('हमारे गाँव में सब कहते थे कि उस कुएँ का पानी मीठा है, पर हम बच्चे उसके पास जाने से डरते थे।', 'प्रथम पुरुष बहुवचन (‘हम’) कथावाचक', 'समुदाय की सामूहिक आवाज़; कथा व्यक्तिगत न होकर पूरे गाँव की लगती है।'),
    ('तुम उस दिन स्टेशन पर खड़े थे, हाथ में टिकट और आँखों में आँसू लिए।', 'द्वितीय पुरुष (‘तुम’) कथन', 'पाठक को सीधे संबोधित कर उसे कहानी के भीतर खींच लिया जाता है।'),
]


def g_devices(kit, key, th):
    def ident(rng, slot):
        s, d, e = rng.choice(LIT_DEVICES)
        w = rng.sample([x for x in DEVICE_NAMES if x != d], 3)
        return mcq(rng, f'कथा-अंश का वाक्य: “{s}”\nइस वाक्य में कौन-सा साहित्यिक उपकरण (शैली-तत्व) प्रयुक्त हुआ है?', d, w, e)
    kit.add(key, 'C1', (1, 3), ident, 'mcq', 'p2r', 'dev_id')

    def effect(rng, slot):
        s, d, e = rng.choice(LIT_DEVICES)
        return dict(stem=f'“{s}”\nइस वाक्य में प्रयुक्त ‘{d}’ को पहचानकर बताइए कि यह पाठक पर क्या प्रभाव डालता है।', answer=e, type='explain', marks=2,
                    markingKey=f'1 अंक: उपकरण की सही पहचान ({d}) और वाक्य में उसका स्थान; 1 अंक: प्रभाव — {e}')
    kit.add(key, 'C2', (2, 4), effect, 'explain', None, 'dev_eff')

    def create(rng, slot):
        d = rng.choice(['उपमा', 'रूपक', 'मानवीकरण', 'पूर्वाभास', 'विडंबना'])
        topic = rng.choice(th['topics'])
        ex = next(s for s, dd, e in LIT_DEVICES if dd == d)
        return dict(stem=f'‘{topic}’ से जुड़े किसी दृश्य के लिए ‘{d}’ का प्रयोग करते हुए दो मौलिक वाक्य लिखिए और बताइए कि आपका उपकरण क्या प्रभाव पैदा करता है।',
                    answer=f'उदाहरण-संदर्भ: “{ex}” जैसे वाक्य; विद्यार्थी के अपने मौलिक वाक्य मान्य।', type='short', marks=3,
                    markingKey=f'2 अंक: ‘{d}’ का सही और मौलिक प्रयोग (प्रत्येक वाक्य 1); 1 अंक: प्रभाव की स्पष्ट व्याख्या।')
    kit.add(key, 'C3', (2, 4), create, 'short', None, 'dev_make')

    def narr_id(rng, slot):
        s, n, e = rng.choice(NARR)
        w = rng.sample([x[1] for x in NARR if x[1] != n], 3)
        return mcq(rng, f'कथा-अंश: “{s}”\nयह अंश किस कथन-दृष्टि (कथावाचक के प्रकार) से लिखा गया है?', n, w, e)
    kit.add(key, ('C1', 'C2'), (1, 3), narr_id, 'mcq', 'p2r', 'narr_id')

    def narr_change(rng, slot):
        s, n, e = rng.choice(NARR)
        target = rng.choice([x[1] for x in NARR if x[1] != n][:3])
        return dict(stem=f'कथा-अंश ({n}): “{s}”\nइस अंश को ‘{target}’ में फिर से लिखिए और बताइए कि बदलाव से पाठक के अनुभव में क्या अंतर आता है।',
                    answer=f'मूल प्रभाव: {e} नई दृष्टि में सर्वनाम और जानकारी की सीमा बदलेगी; पाठक की निकटता/दूरी बदल जाती है।', type='short', marks=4,
                    markingKey='2 अंक: नई कथन-दृष्टि में सही पुनर्लेखन (सर्वनाम, क्रिया-रूप); 2 अंक: पाठक पर प्रभाव के अंतर की व्याख्या।')
    kit.add(key, 'C3', (3, 5), narr_change, 'short', None, 'narr_chg')


PREM = [
    ('C1', '‘ईदगाह’ कहानी में हामिद मेले से अपनी दादी के लिए क्या ख़रीदता है?', 'चिमटा', ['मिट्टी का खिलौना', 'मिठाई', 'चूड़ियाँ'], 'हामिद तीन पैसे में चिमटा ख़रीदता है ताकि रोटियाँ सेंकते समय दादी की उँगलियाँ न जलें।'),
    ('C1', '‘ईदगाह’ में हामिद की दादी का नाम क्या है?', 'अमीना', ['मुन्नी', 'बुधिया', 'धनिया'], 'हामिद अपनी दादी अमीना के साथ रहता है।'),
    ('C1', '‘पूस की रात’ कहानी के मुख्य पात्र किसान का नाम क्या है?', 'हल्कू', ['होरी', 'घीसू', 'हामिद'], 'हल्कू एक गरीब किसान है।'),
    ('C1', '‘पूस की रात’ में हल्कू के साथ खेत पर कौन रहता है?', 'उसका कुत्ता जबरा', ['उसकी पत्नी मुन्नी', 'सहना महाजन', 'उसका बेटा'], 'जबरा कुत्ता ठंडी रात में हल्कू का एकमात्र साथी है।'),
    ('C1', '‘पूस की रात’ में हल्कू ने कंबल के लिए जोड़े पैसे किसे दे दिए?', 'सहना (महाजन) को', ['मुन्नी को', 'ज़मींदार के कारिंदे को', 'जबरा के इलाज में'], 'सहना कर्ज़ वसूलने आता है और हल्कू को पैसे देने पड़ते हैं।'),
    ('C1', '‘नमक का दारोगा’ में ईमानदार दारोगा का नाम क्या है?', 'मुंशी वंशीधर', ['पंडित अलोपीदीन', 'हल्कू', 'माधव'], 'मुंशी वंशीधर नमक विभाग के ईमानदार दारोगा हैं।'),
    ('C1', '‘नमक का दारोगा’ में अलोपीदीन वंशीधर को अंत में कितने हज़ार रुपये की रिश्वत देने को तैयार हो जाते हैं?', 'चालीस हज़ार', ['चार हज़ार', 'दस हज़ार', 'एक लाख'], 'बोली बढ़ते-बढ़ते चालीस हज़ार तक पहुँचती है, पर वंशीधर नहीं मानते।'),
    ('C1', '‘कफ़न’ कहानी के दो मुख्य पात्र कौन हैं?', 'घीसू और माधव', ['हल्कू और जबरा', 'हामिद और मोहसिन', 'वंशीधर और अलोपीदीन'], 'घीसू (पिता) और माधव (पुत्र) कहानी के केंद्र में हैं।'),
    ('C1', 'प्रेमचंद का वास्तविक नाम क्या था?', 'धनपत राय', ['नवाब राय', 'जयशंकर प्रसाद', 'सूर्यकांत त्रिपाठी'], 'उनका वास्तविक नाम धनपत राय श्रीवास्तव था; आरंभ में वे उर्दू में ‘नवाब राय’ नाम से लिखते थे।'),
    ('C1', 'प्रेमचंद का जन्म कहाँ हुआ था?', 'वाराणसी के पास लमही गाँव में', ['इलाहाबाद में', 'लखनऊ में', 'पटना में'], 'प्रेमचंद का जन्म 31 जुलाई 1880 को लमही (वाराणसी) में हुआ।'),
    ('C1', 'प्रेमचंद की कहानियों का संग्रह किस नाम से प्रसिद्ध है?', 'मानसरोवर', ['गोदान', 'कामायनी', 'मधुशाला'], '‘मानसरोवर’ आठ खंडों में उनकी कहानियों का संग्रह है; ‘गोदान’ उपन्यास है।'),
    ('C1', 'प्रेमचंद का कौन-सा कहानी-संग्रह अंग्रेज़ी सरकार ने ज़ब्त कर लिया था?', 'सोज़े-वतन', ['मानसरोवर', 'गोदान', 'निर्मला'], '1908 में प्रकाशित ‘सोज़े-वतन’ को देशभक्ति के कारण ज़ब्त किया गया।'),
    ('C2', '‘ईदगाह’ में हामिद द्वारा चिमटा ख़रीदने के निर्णय से उसके चरित्र की कौन-सी दो विशेषताएँ सामने आती हैं?', 'दादी के प्रति प्रेम और संवेदनशीलता; उम्र से अधिक परिपक्वता और त्याग (अपनी इच्छा छोड़ना); साथ ही तर्क से दोस्तों को चुप कराने की चतुराई।',
     '2 अंक: दो विशेषताएँ, प्रत्येक के लिए कहानी से संक्षिप्त प्रमाण सहित 1 अंक।'),
    ('C2', '‘नमक का दारोगा’ में वंशीधर के पिता ने उसे नौकरी के बारे में क्या सलाह दी थी और यह सलाह किस सामाजिक सच्चाई को दिखाती है?', 'पिता ने कहा कि मासिक वेतन पूर्णमासी का चाँद है जो घटता जाता है, ऊपरी आय बहता स्रोत है — यानी रिश्वत की कमाई पर ध्यान दो; यह समाज में फैले भ्रष्टाचार की स्वीकृति दिखाती है।',
     '1 अंक: सलाह का सार (ऊपरी आय/रिश्वत); 1 अंक: सामाजिक सच्चाई — भ्रष्टाचार को सामान्य मानना।'),
    ('C2', '‘पूस की रात’ के अंत में फ़सल नष्ट होने पर भी हल्कू प्रसन्न क्यों दिखाई देता है?', 'अब उसे ठंडी रातों में खेत पर नहीं सोना पड़ेगा; खेती से उसे लाभ नहीं, केवल कष्ट और कर्ज़ मिलता था — यह किसान की हताशा और शोषण को दिखाता है।',
     '1 अंक: कारण (खेत पर ठंड में न सोना); 1 अंक: गहरा अर्थ — खेती से मोहभंग और शोषण।'),
    ('C3', '‘कफ़न’ में घीसू और माधव का व्यवहार अमानवीय लगता है। प्रेमचंद इसके लिए केवल उन्हें दोषी ठहराते हैं या समाज को भी? तर्क सहित उत्तर दीजिए।', 'प्रेमचंद समाज को भी दोषी ठहराते हैं: पीढ़ियों की गरीबी, मेहनत का उचित फल न मिलना और शोषण ने उनकी संवेदना को मार दिया; कहानी व्यवस्था पर व्यंग्य है, जिसमें जीवित को कपड़ा नहीं मिलता और मरे को कफ़न चाहिए।',
     '3 अंक: स्पष्ट मत (1), सामाजिक कारणों का विश्लेषण (1), कहानी से प्रमाण/उद्धरण (1)।'),
    ('C3', '‘बड़े भाई साहब’ कहानी में लेखक ने परीक्षा-प्रणाली पर किस तरह व्यंग्य किया है?', 'रटंत विद्या, बेमतलब के प्रश्नों और अंकों पर आधारित मूल्यांकन पर हास्य के सहारे चोट; पढ़ाकू बड़ा भाई बार-बार फ़ेल होता है और खेलता रहने वाला छोटा भाई पास — यह व्यवस्था की विडंबना दिखाता है।',
     '3 अंक: व्यंग्य का विषय (1), कहानी से उदाहरण (1), विडंबना/हास्य की तकनीक की व्याख्या (1)।'),
    ('C4', 'प्रेमचंद को ‘यथार्थवादी’ लेखक क्यों कहा जाता है? किन्हीं दो कहानियों के आधार पर विश्लेषण कीजिए।', 'गाँव, किसान, गरीबी, शोषण, भ्रष्टाचार का बिना आदर्शीकरण चित्रण (पूस की रात, कफ़न); आम बोलचाल की भाषा; सामान्य लोग नायक। आरंभिक कहानियों (नमक का दारोगा) में आदर्शोन्मुख यथार्थवाद, बाद की कहानियों में कठोर यथार्थ।',
     '6 अंक: यथार्थवाद की परिभाषा (1), दो कहानियों से विश्लेषण (2+2), भाषा और संरचना (1)।', 6),
    ('C4', '‘ईदगाह’ और ‘पूस की रात’ — दोनों में गरीबी का चित्रण है, पर स्वर अलग है। तुलना कीजिए।', 'ईदगाह: गरीबी के बीच प्रेम, त्याग और आशा, भावुक-सुखद अंत; पूस की रात: गरीबी से उपजी हताशा और मोहभंग, कटु-व्यंग्यात्मक अंत। दोनों में प्रतीक (चिमटा; अलाव/कंबल) और ग्रामीण परिवेश।',
     '6 अंक: समानताएँ (2), भिन्नताएँ — स्वर और अंत (2), प्रतीकों/भाषा का विश्लेषण (1), निष्कर्ष (1)।', 6),
]

IO_ITEMS = [
    ('C1', 'उच्च स्तर (HL) के व्यक्तिगत मौखिक मूल्यांकन में तैयारी के लिए कितना समय मिलता है?', '20 मिनट', ['5 मिनट', '45 मिनट', '1 घंटा'], 'HL में साहित्यिक अंश पर तैयारी के लिए 20 मिनट मिलते हैं।'),
    ('C1', 'HL व्यक्तिगत मौखिक मूल्यांकन में साहित्यिक अंश पर प्रस्तुति कितने मिनट की होती है?', '3–4 मिनट', ['10–12 मिनट', '1 मिनट', '15 मिनट'], 'प्रस्तुति 3–4 मिनट की होती है, फिर 4–5 मिनट चर्चा।'),
    ('C1', 'HL मौखिक में प्रस्तुति के बाद अंश पर शिक्षक के साथ चर्चा कितने मिनट चलती है?', '4–5 मिनट', ['1–2 मिनट', '10 मिनट', '20 मिनट'], 'प्रस्तुति के बाद 4–5 मिनट अंश पर चर्चा होती है।'),
    ('C1', 'HL मौखिक के अंतिम भाग में किस पर सामान्य बातचीत होती है?', 'पाठ्यक्रम के किसी एक अतिरिक्त विषय (थीम) पर', ['केवल व्याकरण पर', 'छात्र के परीक्षा-परिणाम पर', 'अंश के लेखक की जीवनी पर'], 'अंतिम 5–6 मिनट में किसी अन्य थीम पर सामान्य बातचीत होती है।'),
    ('C1', 'व्यक्तिगत मौखिक मूल्यांकन के कुल अंक कितने हैं?', '30', ['25', '40', '60'], 'मानदंड A (12) + B1 (6) + B2 (6) + C (6) = 30 अंक।'),
    ('C1', 'मौखिक मूल्यांकन में मानदंड A किससे संबंधित है?', 'भाषा — शब्दावली, व्याकरण और उच्चारण', ['अंश की विषय-वस्तु', 'संवाद-कौशल', 'प्रस्तुति की अवधि'], 'मानदंड A (12 अंक) भाषा पर है।'),
    ('C1', 'HL मौखिक में मानदंड B1 किसका मूल्यांकन करता है?', 'साहित्यिक अंश की विषय-वस्तु और उसकी समझ', ['सामान्य बातचीत में भाषा', 'उच्चारण की शुद्धता', 'पढ़ने की गति'], 'B1 (6 अंक): अंश की प्रस्तुति में संदेश/विषय-वस्तु।'),
    ('C1', 'मौखिक मूल्यांकन में मानदंड C (6 अंक) किससे संबंधित है?', 'संवाद-कौशल — प्रश्नों को समझना और बातचीत आगे बढ़ाना', ['लिखित भाषा की शुद्धता', 'अंश को कंठस्थ करना', 'लेखक का परिचय'], 'C: परस्पर संवाद और प्रतिक्रिया।'),
    ('C2', 'अंश पर प्रस्तुति की तैयारी के 20 मिनटों का उपयोग कैसे करना चाहिए? तीन चरण बताइए।', 'अंश को दो बार ध्यान से पढ़ना और संदर्भ पहचानना; मुख्य विषय, पात्र और शैली-तत्व चिह्नित करना; संक्षिप्त नोट्स (10 बिंदु तक) में भूमिका–विश्लेषण–निष्कर्ष की रूपरेखा बनाना।',
     '3 अंक: प्रत्येक उचित चरण के लिए 1 अंक।', 3),
    ('C2', 'मौखिक प्रस्तुति में अंश का सारांश सुनाने के बजाय विश्लेषण करना क्यों आवश्यक है?', 'मानदंड B1 अंश की समझ और व्याख्या को परखता है; केवल सारांश से गहरी समझ (पात्र, भाव, शैली, संदर्भ) नहीं दिखती; विश्लेषण से व्यक्तिगत प्रतिक्रिया और कृति से संबंध दिखता है।',
     '2 अंक: मानदंड से संबंध (1), विश्लेषण के लाभ का स्पष्टीकरण (1)।'),
    ('C3', 'एक विद्यार्थी ने प्रस्तुति आरंभ की: “इस अंश में हामिद मेले जाता है, फिर वह चिमटा ख़रीदता है, फिर वह घर आता है…” — इस आरंभ की कमियाँ बताइए और बेहतर आरंभ लिखिए।', 'कमियाँ: केवल घटना-क्रम (सारांश), कोई संदर्भ या मुख्य विचार नहीं, ‘फिर’ की पुनरावृत्ति। बेहतर: “यह अंश प्रेमचंद की कहानी ‘ईदगाह’ के उस मोड़ से है जहाँ हामिद अपनी इच्छाओं पर दादी के प्रति प्रेम को प्राथमिकता देता है; मैं पात्र-चित्रण, प्रतीक (चिमटा) और भाषा पर बात करूँगा।”',
     '4 अंक: दो कमियाँ (2), संदर्भ और मुख्य विचार सहित बेहतर आरंभ (2)।', 4),
    ('C4', '‘पूस की रात’ के अंतिम अंश (हल्कू का अलाव के पास सो जाना और सुबह मुन्नी की चिंता) पर 3–4 मिनट की मौखिक प्रस्तुति की रूपरेखा बनाइए।', 'भूमिका: कहानी और अंश का संदर्भ; विश्लेषण: हल्कू की थकान और मोहभंग, जबरा की वफ़ादारी, प्रकृति (ठंड) का चित्रण, विडंबनापूर्ण अंत; भाषा: ग्रामीण, सरल, बिंब; निष्कर्ष: किसान का शोषण और कहानी की प्रासंगिकता।',
     '6 अंक: संदर्भ (1), विषय-वस्तु का विश्लेषण (2), शैली/भाषा (1), व्यक्तिगत प्रतिक्रिया और प्रासंगिकता (1), तार्किक क्रम (1)।', 6),
]

CONTEXT_ITEMS = [
    ('C1', 'प्रेमचंद की अधिकांश कहानियों का परिवेश कैसा है?', 'उत्तर भारत के गाँव और कस्बे', ['यूरोप के शहर', 'राजमहल', 'विज्ञान-कथा की काल्पनिक दुनिया'], 'उनकी कहानियाँ प्रायः ग्रामीण उत्तर भारत में रची गई हैं।'),
    ('C1', 'प्रेमचंद का लेखन-काल मुख्यतः किस ऐतिहासिक दौर से जुड़ा है?', 'स्वतंत्रता आंदोलन का दौर (बीसवीं सदी के आरंभिक दशक)', ['मुगल काल', 'स्वतंत्रता के पचास साल बाद', 'इक्कीसवीं सदी'], 'वे 1936 तक लिखते रहे; यह स्वतंत्रता संग्राम का समय था।'),
    ('C1', '‘पूस की रात’ में किसान की मुख्य समस्या किस सामाजिक व्यवस्था से जुड़ी है?', 'महाजनी कर्ज़ और शोषण', ['औद्योगिक प्रदूषण', 'शहरी बेरोज़गारी', 'शिक्षा का अभाव'], 'सहना जैसे महाजन का कर्ज़ हल्कू को गरीबी में बाँधे रखता है।'),
    ('C1', '‘नमक का दारोगा’ में नमक-विभाग की नौकरी को लोग क्यों आकर्षक मानते थे?', 'ऊपरी आय (रिश्वत) के कारण', ['कम काम के कारण', 'विदेश यात्रा के कारण', 'सरकारी पुरस्कार के कारण'], 'कहानी के आरंभ में ही बताया गया है कि नमक विभाग में ऊपरी कमाई बहुत थी।'),
    ('C1', 'प्रेमचंद का अंतिम पूर्ण उपन्यास कौन-सा है, जो किसान होरी की कथा है?', 'गोदान', ['मानसरोवर', 'सोज़े-वतन', 'ईदगाह'], '‘गोदान’ (1936) किसान होरी के संघर्ष की कथा है।'),
    ('C2', '‘ईदगाह’ में ईद के मेले का सांस्कृतिक महत्त्व समझाइए। यह कहानी के अर्थ को कैसे गहरा करता है?', 'ईद उत्सव, सामूहिकता और आनंद का पर्व है; अमीरी-गरीबी का अंतर मेले में साफ़ दिखता है; उत्सव के बीच हामिद का त्याग कहानी को भावुक और मानवीय बनाता है।',
     '2 अंक: सांस्कृतिक महत्त्व (1), कहानी के अर्थ से संबंध (1)।'),
    ('C2', 'प्रेमचंद की कहानियों में स्त्री पात्र (जैसे अमीना, मुन्नी, बुधिया) किस सामाजिक स्थिति को दर्शाते हैं?', 'गरीबी, घरेलू श्रम और पीड़ा का बोझ; फिर भी वे परिवार की रीढ़ हैं — अमीना का स्नेह, मुन्नी की व्यावहारिकता, बुधिया की उपेक्षित मृत्यु स्त्री की असहाय स्थिति दिखाती है।',
     '2 अंक: स्थिति की पहचान (1), किसी पात्र से उदाहरण (1)।'),
    ('C3', 'प्रेमचंद के समय की कौन-सी सामाजिक समस्याएँ आज भी भारत में दिखाई देती हैं? दो उदाहरण कहानियों से जोड़कर दीजिए।', 'किसानों का कर्ज़ और आत्महत्या (पूस की रात); भ्रष्टाचार (नमक का दारोगा); गरीबी और असमानता (ईदगाह, कफ़न); रटंत शिक्षा (बड़े भाई साहब)।',
     '3 अंक: दो समस्याएँ (1), प्रत्येक का कहानी से संबंध (1), आज के संदर्भ की व्याख्या (1)।'),
    ('C4', '“प्रेमचंद का साहित्य स्वतंत्रता आंदोलन की आवाज़ भी है।” — उनके सामाजिक-ऐतिहासिक संदर्भ के आधार पर इस कथन का विवेचन कीजिए।', 'सोज़े-वतन की ज़ब्ती; देशभक्ति और सामाजिक सुधार; किसानों-मज़दूरों के शोषण का विरोध; गांधीवादी आदर्शों (ईमानदारी, सादगी) का प्रभाव; हिंदी-उर्दू की साझी भाषा।',
     '6 अंक: संदर्भ (2), कहानियों/कृतियों से प्रमाण (2), विश्लेषण और निष्कर्ष (2)।', 6),
]

SPEC['ch12-st1'] = ('reading', dict(focus='लेखन में किसी कहानी के पात्र, परिवेश और कथानक का उल्लेख कीजिए।', items=PREM[:16]))
SPEC['ch12-st2'] = ('none', dict(focus='लेखन में शैली के एक-दो साहित्यिक उपकरणों (जैसे उपमा, प्रतीक) का सोच-समझकर प्रयोग कीजिए।', gens=[g_devices], items=[
    ('C1', 'प्रेमचंद की भाषा की सबसे प्रमुख विशेषता क्या मानी जाती है?', 'सरल, बोलचाल की हिंदुस्तानी, जिसमें हिंदी-उर्दू दोनों के शब्द हैं', ['कठिन संस्कृतनिष्ठ हिंदी', 'केवल अंग्रेज़ी शब्दों से भरी भाषा', 'छंदबद्ध काव्य-भाषा'], 'प्रेमचंद आम जन की हिंदुस्तानी में लिखते थे।'),
    ('C1', 'जब कथावाचक सभी पात्रों के मन की बात जानता हो, तो उसे क्या कहते हैं?', 'सर्वज्ञ कथावाचक', ['प्रथम पुरुष कथावाचक', 'अविश्वसनीय कथावाचक', 'संवाद-शैली'], 'सर्वज्ञ कथावाचक सब कुछ जानता है।'),
    ('C2', '‘बड़े भाई साहब’ प्रथम पुरुष (छोटे भाई) की दृष्टि से लिखी गई है। इससे कहानी के हास्य पर क्या प्रभाव पड़ता है?', 'छोटा भाई बड़े भाई के भाषणों और व्यवहार को मासूम पर व्यंग्यपूर्ण दृष्टि से देखता है; पाठक उसके साथ हँसता है, फिर भी अंत में बड़े भाई के प्रति सहानुभूति जागती है।', '1 अंक: दृष्टि की पहचान; 1 अंक: हास्य/व्यंग्य पर प्रभाव।'),
    ('C2', '‘ईदगाह’ में हामिद और उसके दोस्तों के बीच के संवाद कहानी के लिए क्यों महत्त्वपूर्ण हैं?', 'संवाद बच्चों की स्वाभाविक भाषा और तर्क दिखाते हैं, पात्रों को सजीव बनाते हैं और हामिद की चतुराई (चिमटे को ‘रुस्तमे-हिंद’ सिद्ध करना) सामने लाते हैं।', '1 अंक: संवाद का कार्य; 1 अंक: उदाहरण सहित प्रभाव।'),
    ('C4', 'किसी कहानी के एक अंश में लेखक की शैली (भाषा, उपकरण, कथन-दृष्टि) का विश्लेषण करते हुए 150 शब्दों का अनुच्छेद लिखिए। आप इस खंड की ‘बरगद वाली बुआ’, ‘आख़िरी बस’ या प्रेमचंद की कोई कहानी चुन सकते हैं।', 'अपेक्षित: कथन-दृष्टि की पहचान और प्रभाव; दो उपकरण (उपमा, प्रतीक आदि) उद्धरण सहित; भाषा का स्तर (सरल/आंचलिक); पाठक पर समग्र प्रभाव।', '6 अंक: कथन-दृष्टि (1), दो उपकरण उद्धरण सहित (2), प्रभाव का विश्लेषण (2), सुसंगत भाषा (1)।', 6),
]))
SPEC['ch12-st3'] = ('vocab', dict(focus='लेखन में किसी साहित्यिक कृति के सामाजिक संदर्भ को आज के समाज से जोड़िए।', items=CONTEXT_ITEMS + PREM[16:]))
SPEC['ch12-st4'] = ('oral', dict(focus='लेखन में अपनी बात को भूमिका, विश्लेषण और निष्कर्ष के क्रम में प्रस्तुत कीजिए।', items=IO_ITEMS,
                                  gens=[lambda kit, key, th: kit.texts(key, th, 'texts', None)]))



# --------------------------------------------------------------------------------------------
# ch13 – Paper 1 writing skills: text type, criteria, timed writing and revision
# --------------------------------------------------------------------------------------------
TH[13] = dict(
    name='पेपर 1: लेखन-कौशल',
    vocab=[
        ('संबोधन', 'पत्र या भाषण के आरंभ में पाठक/श्रोता को पुकारने का ढंग', 'संबोधक शब्द', 'औपचारिक पत्र में ‘आदरणीय महोदय’ जैसा ____ लिखा जाता है।'),
        ('प्रारूप', 'किसी पाठ-प्रकार का निर्धारित ढाँचा', 'ढाँचा', 'समाचार रिपोर्ट के ____ में शीर्षक, स्थान-तिथि और आमुख आते हैं।'),
        ('लहजा', 'लेखन या बोलने का भावात्मक स्वर', 'स्वर', 'अपील का ____ विनम्र पर दृढ़ होना चाहिए।'),
        ('सुसंगति', 'विचारों का तार्किक और जुड़ा हुआ क्रम', 'संबद्धता', 'अनुच्छेदों के बीच ____ बनाए रखने के लिए संयोजक शब्दों का प्रयोग कीजिए।'),
        ('संयोजक', 'वाक्यों या विचारों को जोड़ने वाले शब्द', 'योजक', '‘इसके अतिरिक्त’ और ‘फिर भी’ उपयोगी ____ शब्द हैं।'),
        ('उद्देश्य', 'लिखने का लक्ष्य, जैसे सूचना देना या मनाना', 'प्रयोजन', 'लिखने से पहले अपने पाठ का ____ स्पष्ट कर लीजिए।'),
        ('लक्षित', 'जिसके लिए कुछ विशेष रूप से बनाया गया हो', 'निर्धारित', 'इस पत्रक के ____ पाठक किशोर विद्यार्थी हैं।'),
        ('प्रवाह', 'भाषा का सहज, बिना रुकावट का बहाव', 'रवानी', 'छोटे-बड़े वाक्यों के मिश्रण से लेखन में ____ आता है।'),
        ('शुद्धता', 'व्याकरण और वर्तनी की त्रुटिहीनता', 'परिशुद्धता', 'मानदंड A में भाषा की ____ और विविधता दोनों देखी जाती हैं।'),
        ('विविधता', 'अलग-अलग प्रकार का होना', 'वैविध्य', 'शब्दावली में ____ से उच्च अंक मिलते हैं।'),
        ('प्रासंगिक', 'जो विषय से जुड़ा हो', 'संगत', 'केवल ____ उदाहरण दीजिए; विषय से भटकने पर अंक कटते हैं।'),
        ('संशोधन', 'लिखे हुए को सुधारना', 'परिष्कार', 'परीक्षा के अंतिम दस मिनट ____ के लिए बचाकर रखिए।'),
        ('रूपरेखा', 'लिखने से पहले बनाई गई संक्षिप्त योजना', 'ख़ाका', 'पाँच मिनट में ____ बनाने से उत्तर व्यवस्थित होता है।'),
        ('प्रभावशाली', 'जो पाठक पर गहरा असर डाले', 'असरदार', 'भाषण का ____ समापन श्रोताओं को कार्य के लिए प्रेरित करता है।'),
    ],
    topics=['पाठ-प्रकार का चुनाव', 'पाठक और उद्देश्य', 'औपचारिक और अनौपचारिक रजिस्टर', 'अनुच्छेद-संरचना', 'संयोजक शब्द', 'समय-प्रबंधन', 'त्रुटि-संशोधन'],
    texts=[
        dict(kind='अनौपचारिक पत्र', title='प्रिय तन्वी',
             body='बेंगलुरु, 3 मार्च। प्रिय तन्वी, ढेर सारा प्यार! तुम्हारा पत्र पाकर मन ख़ुश हो गया। तुमने पूछा था कि नए विद्यालय में मेरा मन लगा या नहीं। '
                  'सच कहूँ तो पहले हफ़्ते मुझे बहुत अकेलापन लगा; कैंटीन में मैं अकेली बैठकर खाना खाती थी। फिर एक दिन नाटक-क्लब की सूचना देखी और हिम्मत करके नाम लिखा दिया। '
                  'अब हम ‘अंधेर नगरी’ की तैयारी कर रहे हैं और मुझे चौपट राजा की भूमिका मिली है! सोचो, तुम्हारी शर्मीली सहेली राजा बनकर दहाड़ेगी। '
                  'तुम्हारा क्रिकेट कैसा चल रहा है? चाची जी को मेरा प्रणाम कहना। जल्दी लिखना। तुम्हारी सहेली, अदिति।',
             qs=[('C1', 'अदिति ने नए विद्यालय में किस क्लब में नाम लिखाया?', 'नाटक-क्लब', ['क्रिकेट-क्लब', 'विज्ञान-क्लब', 'संगीत-क्लब']),
                 ('C1', 'अदिति को नाटक में कौन-सी भूमिका मिली है?', 'चौपट राजा की'),
                 ('C2', 'इस पत्र की भाषा से कैसे पता चलता है कि यह अनौपचारिक पत्र है? दो प्रमाण दीजिए।', '‘प्रिय तन्वी, ढेर सारा प्यार’ जैसा आत्मीय संबोधन; ‘तुम’ का प्रयोग, व्यक्तिगत भावनाएँ, विस्मयादिबोधक चिह्न और ‘तुम्हारी सहेली’ जैसा समापन।'),
                 ('tf', 'अदिति को नए विद्यालय में शुरू से ही बहुत मज़ा आया।', 'गलत', '“पहले हफ़्ते मुझे बहुत अकेलापन लगा।”'),
                 ('C3', 'इस पत्र का मुख्य उद्देश्य क्या है?', 'सहेली को अपने नए अनुभव बताना और संबंध बनाए रखना', ['नाटक-क्लब का विज्ञापन करना', 'विद्यालय की शिकायत करना', 'क्रिकेट के नियम समझाना']),
                 ('C3', 'यदि अदिति यही जानकारी विद्यालय-पत्रिका के लिए ‘नए विद्यार्थियों के लिए सुझाव’ लेख में लिखे, तो उसे भाषा और ढाँचे में कौन-से तीन बदलाव करने होंगे?', 'शीर्षक और लेखक का नाम; ‘तुम’ के स्थान पर सामान्य पाठक-संबोधन (‘आप’/‘हम’); निजी बातें (चाची, क्रिकेट) हटाकर सामान्य सुझाव; अर्ध-औपचारिक रजिस्टर और अनुच्छेद-संरचना।'),
                 ('C4', 'अदिति का अनुभव बताता है कि नए परिवेश में ढलने के लिए पहल ज़रूरी है। क्या आप सहमत हैं? अपने अनुभव से तर्क दीजिए।', 'पक्ष: क्लब/गतिविधियाँ मित्रता बनाती हैं, आत्मविश्वास बढ़ता है; विद्यालय की ज़िम्मेदारी (साथी-कार्यक्रम)। व्यक्तिगत उदाहरण और संतुलित निष्कर्ष।'),
             ]),
        dict(kind='सूचना', title='पुस्तक-मेला: स्वयंसेवकों की आवश्यकता',
             body='सरस्वती विद्या निकेतन, जयपुर। सूचना। दिनांक: 10 जुलाई। सभी विद्यार्थियों को सूचित किया जाता है कि विद्यालय में 25 से 27 जुलाई तक वार्षिक पुस्तक-मेला आयोजित किया जाएगा। '
                  'मेले के संचालन के लिए कक्षा 9 से 12 के बीस स्वयंसेवकों की आवश्यकता है। स्वयंसेवकों को पुस्तकों की व्यवस्था, अतिथियों के स्वागत और बिक्री-काउंटर पर सहायता करनी होगी। '
                  'इच्छुक विद्यार्थी 18 जुलाई तक पुस्तकालय में अपना नाम दर्ज कराएँ। चयनित स्वयंसेवकों को प्रमाण-पत्र दिए जाएँगे। हस्ताक्षर: रीना शर्मा, सचिव, साहित्य-परिषद।',
             qs=[('C1', 'पुस्तक-मेले के लिए कितने स्वयंसेवकों की आवश्यकता है?', 'बीस', ['दस', 'पच्चीस', 'अठारह']),
                 ('C1', 'नाम दर्ज कराने की अंतिम तिथि क्या है?', '18 जुलाई'),
                 ('C2', 'सूचना में कर्मवाच्य (“सूचित किया जाता है”, “आयोजित किया जाएगा”) का प्रयोग क्यों किया गया है?', 'कर्मवाच्य औपचारिक और निर्वैयक्तिक लहजा देता है; ध्यान व्यक्ति पर नहीं, सूचना पर रहता है — यह सूचना-पत्र की परंपरा है।'),
                 ('tf', 'स्वयंसेवकों को मेले के बाद प्रमाण-पत्र मिलेगा।', 'सही', '“चयनित स्वयंसेवकों को प्रमाण-पत्र दिए जाएँगे।”'),
                 ('C3', 'इस सूचना के लक्षित पाठक कौन हैं?', 'विद्यालय के विद्यार्थी, विशेष रूप से कक्षा 9 से 12', ['अभिभावक', 'पुस्तक-विक्रेता', 'शहर के सभी नागरिक']),
                 ('C3', 'सूचना-पत्र के किन्हीं तीन प्रारूप-तत्वों को इस पाठ से पहचानिए।', 'संस्था का नाम (सरस्वती विद्या निकेतन), ‘सूचना’ शीर्षक, दिनांक, संक्षिप्त तथ्यात्मक विवरण, अंत में हस्ताक्षर और पद (सचिव)।'),
                 ('C4', 'इसी जानकारी को विद्यालय के सोशल मीडिया पेज के लिए आकर्षक ‘पोस्ट’ में बदलना हो, तो आप क्या-क्या बदलेंगे और क्यों?', 'छोटे वाक्य, प्रश्न/आह्वान (“क्या आप किताबों के दीवाने हैं?”), इमोजी/हैशटैग, ‘आप’ से सीधा संबोधन, आवश्यक तथ्य (तिथि, अंतिम तिथि) बनाए रखना; पाठक और माध्यम के अनुसार रजिस्टर बदलता है।'),
             ]),
        dict(kind='विज्ञापन', title='‘हरियाली’ पौधशाला — घर को बनाइए हरा-भरा!',
             body='क्या आपकी बालकनी सूनी है? क्या आप शहर की धूल-धुएँ से परेशान हैं? तो आइए ‘हरियाली’ पौधशाला में! यहाँ मिलेंगे 200 से अधिक किस्मों के इनडोर और आउटडोर पौधे। '
                  'विशेष छूट: विद्यार्थियों के लिए हर ख़रीद पर 15% छूट! हर रविवार सुबह 10 बजे निःशुल्क ‘बागवानी कार्यशाला’। '
                  'पता: गली नंबर 4, सेक्टर 9, चंडीगढ़। संपर्क: 98XXXXXX10। हरियाली — क्योंकि हर साँस क़ीमती है!',
             qs=[('C1', 'विद्यार्थियों को कितनी छूट मिलेगी?', '15%', ['10%', '20%', '50%']),
                 ('C1', 'निःशुल्क बागवानी कार्यशाला कब होती है?', 'हर रविवार सुबह 10 बजे'),
                 ('C2', 'विज्ञापन की शुरुआत प्रश्नों से क्यों की गई है?', 'प्रश्न पाठक को सीधे संबोधित करते हैं, उसकी समस्या (सूनी बालकनी, प्रदूषण) से जोड़ते हैं और उत्सुकता जगाते हैं।'),
                 ('tf', 'पौधशाला में केवल आउटडोर पौधे मिलते हैं।', 'गलत', '“200 से अधिक किस्मों के इनडोर और आउटडोर पौधे।”'),
                 ('C3', '“हर साँस क़ीमती है” — इस नारे (टैगलाइन) का प्रयोग किस भावना को जगाने के लिए किया गया है?', 'स्वास्थ्य और स्वच्छ हवा के प्रति चिंता, ताकि पौधे ख़रीदना ज़रूरत लगे', ['डर, ताकि लोग शहर छोड़ दें', 'हास्य, ताकि लोग हँसें', 'ईर्ष्या, ताकि लोग पड़ोसियों से होड़ करें']),
                 ('C3', 'इस विज्ञापन में प्रयुक्त किन्हीं तीन प्रेरक (मनाने वाली) तकनीकों को पहचानिए।', 'पाठक से प्रश्न; विशेष छूट/निःशुल्क प्रस्ताव; संख्या से विश्वसनीयता (200 किस्में); विस्मयादिबोधक चिह्न; यादगार नारा।'),
                 ('C4', 'क्या विज्ञापनों में ‘डर’ या ‘चिंता’ जगाकर कुछ बेचना नैतिक है? इस विज्ञापन के संदर्भ में अपना मत दीजिए।', 'यहाँ चिंता (प्रदूषण) वास्तविक है और समाधान सकारात्मक है; पर अतिरंजित डर भ्रामक हो सकता है। संतुलित मत: सच्चाई और पारदर्शिता हो तो स्वीकार्य।'),
             ]),
    ],
    tasks=[
        ('आपके विद्यालय में मोबाइल फ़ोन पर पूर्ण प्रतिबंध लगाने का प्रस्ताव है। इस पर अपना मत रखते हुए विद्यालय-पत्रिका के लिए लिखिए।', 'opinion',
         ['प्रतिबंध के पक्ष के तर्क', 'विपक्ष के तर्क', 'आपका संतुलित सुझाव']),
        ('आपने हाल ही में एक नए शहर में पहला सप्ताह बिताया। अपने अनुभव ऑनलाइन पाठकों से साझा कीजिए।', 'blog',
         ['पहली छाप', 'कठिनाइयाँ और सुखद अनुभव', 'नए आने वालों के लिए सुझाव']),
        ('आपके इलाक़े के पार्क में खेल का सामान टूटा हुआ है। नगर निगम के अधिकारी को लिखिए।', 'fletter',
         ['समस्या का विवरण', 'बच्चों और बुज़ुर्गों पर प्रभाव', 'आपके ठोस सुझाव']),
        ('विद्यालय के वार्षिकोत्सव में आपको मुख्य अतिथि का स्वागत करते हुए विद्यार्थियों की ओर से बोलना है।', 'speech',
         ['अतिथि का परिचय और स्वागत', 'विद्यालय की वर्ष-भर की उपलब्धियाँ', 'धन्यवाद और आगे का संकल्प']),
        ('आपके विद्यालय ने एक गाँव में स्वास्थ्य-शिविर लगाया। शिविर के बारे में समाचार-पत्र के लिए लिखिए।', 'news',
         ['शिविर कब, कहाँ और किसने लगाया', 'कितने लोगों को लाभ हुआ', 'आयोजकों और ग्रामीणों के कथन']),
        ('आपके शहर में खुले नए विज्ञान-संग्रहालय को आपने देखा। विद्यालय-पत्रिका के पाठकों के लिए उसका मूल्यांकन कीजिए।', 'review',
         ['संग्रहालय का संक्षिप्त परिचय', 'सबसे अच्छी और कमज़ोर बातें', 'किसके लिए उपयोगी और आपकी रेटिंग']),
    ],
    discuss=[
        ('क्या परीक्षा में समयबद्ध लेखन वास्तविक लेखन-क्षमता को मापता है?', ['दबाव में सोचने की क्षमता', 'संशोधन का कम समय', 'अभ्यास से सुधार']),
        ('क्या अच्छी भाषा के बिना अच्छा संदेश दिया जा सकता है?', ['स्पष्ट विचार भाषा से अधिक महत्त्वपूर्ण', 'त्रुटियाँ अर्थ बिगाड़ती हैं', 'मानदंड A और B का संतुलन']),
        ('क्या औपचारिक भाषा धीरे-धीरे लुप्त हो रही है?', ['ईमेल और संदेशों की छोटी भाषा', 'सरकारी और व्यावसायिक लेखन में आवश्यकता', 'संदर्भ के अनुसार भाषा बदलने का कौशल']),
        ('लिखने से पहले रूपरेखा बनाना समय की बर्बादी है या आवश्यकता?', ['व्यवस्थित विचार', 'समय-प्रबंधन', 'भटकने से बचाव']),
        ('क्या कृत्रिम बुद्धिमत्ता के युग में विद्यार्थियों को लेखन सीखने की ज़रूरत है?', ['सोचने और अभिव्यक्ति का कौशल', 'एआई पर निर्भरता के ख़तरे', 'एआई को सहायक के रूप में प्रयोग']),
    ],
)

TT_SITU = [
    ('आप चाहते हैं कि आपके शहर के सभी नागरिक रविवार को नदी-तट की सफ़ाई में भाग लें। आप पूरे शहर से अपील करना चाहते हैं।', 'appeal'),
    ('आपकी नानी गाँव में अकेली रहती हैं। आप उन्हें अपनी नई नौकरी और शहर के जीवन के बारे में बताना चाहते हैं।', 'pletter'),
    ('आप विद्यालय के सभी विद्यार्थियों को बताना चाहते हैं कि अगले सप्ताह पुस्तकालय दो दिन बंद रहेगा।', 'notice'),
    ('आप हर दिन अपने मन की बातें और भावनाएँ सिर्फ़ अपने लिए लिखना चाहते हैं।', 'diary'),
    ('आप एक प्रसिद्ध पर्वतारोही से बातचीत करके उनके अनुभव पत्रिका-पाठकों तक पहुँचाना चाहते हैं।', 'interview'),
    ('आपने एक नई फ़िल्म देखी और आप पाठकों को बताना चाहते हैं कि यह देखने लायक है या नहीं।', 'review'),
    ('आप एक बहुराष्ट्रीय कंपनी में इंटर्नशिप के लिए आवेदन के साथ अपनी शिक्षा और कौशल का विवरण भेजना चाहते हैं।', 'biodata'),
    ('आपको विद्यालय की सभा में सैकड़ों विद्यार्थियों के सामने परीक्षा के तनाव पर बोलना है।', 'speech'),
    ('आप पर्यटकों को अपने शहर के दर्शनीय स्थलों, होटलों और यात्रा-सुविधाओं की जानकारी एक छोटे मुड़े हुए पृष्ठ पर देना चाहते हैं।', 'brochure'),
    ('आप अपनी लद्दाख-यात्रा के दृश्य, अनुभव और रोमांच साहित्यिक ढंग से पाठकों तक पहुँचाना चाहते हैं।', 'travelogue'),
    ('आपके मोहल्ले में तीन दिन से पानी नहीं आ रहा। आप जल-बोर्ड के अधिकारी से कार्रवाई की माँग करना चाहते हैं।', 'fletter'),
    ('आप ऑनलाइन पाठकों के साथ अपने शाकाहारी खाना बनाने के अनुभव और नुस्ख़े नियमित रूप से साझा करना चाहते हैं।', 'blog'),
    ('विद्यालय में हुई अंतर-विद्यालय वाद-विवाद प्रतियोगिता के बारे में आपको प्रधानाचार्य के लिए तथ्य, आँकड़े और सुझाव प्रस्तुत करने हैं।', 'report'),
    ('आप अपने विद्यालय में कंपोस्ट-इकाई शुरू करने के लिए प्रबंधन से बजट और योजना सहित स्वीकृति माँगना चाहते हैं।', 'proposal'),
    ('आप अपने नए कोचिंग-केंद्र की ओर ग्राहकों को आकर्षित करना चाहते हैं — कम शब्दों में, नारे और छूट के साथ।', 'advert'),
    ('कल आपके शहर में हुई भारी ओलावृष्टि की तथ्यात्मक जानकारी आप समाचार-पत्र के पाठकों तक पहुँचाना चाहते हैं।', 'news'),
    ('आप समाचार-पत्र के पाठकों को तर्कों के साथ यह मनाना चाहते हैं कि विद्यालयों में खेल का पीरियड रोज़ होना चाहिए।', 'opinion'),
    ('आप अपनी कंपनी के ग्राहक-सेवा विभाग को डिलीवरी में देरी के बारे में तुरंत और संक्षेप में लिखना चाहते हैं।', 'email'),
    ('आप ‘ऑनलाइन शिक्षा के फ़ायदे और नुक़सान’ पर संतुलित, सूचनात्मक जानकारी विद्यालय-पत्रिका के सामान्य पाठकों को देना चाहते हैं।', 'article'),
    ('आप अपनी बचपन की सहेली को उसके जन्मदिन पर बधाई देते हुए पुरानी यादें ताज़ा करना चाहते हैं।', 'pletter'),
    ('विद्यालय की बस-सेवा में बदलाव की जानकारी आप सभी अभिभावकों को सूचना-पट्ट और वेबसाइट पर देना चाहते हैं।', 'notice'),
    ('आप भूकंप-पीड़ितों के लिए कपड़े और भोजन दान करने का आग्रह सभी देशवासियों से करना चाहते हैं।', 'appeal'),
]


def g_tt_situ(kit, key, th):
    def pick(rng, slot):
        s, tt = rng.choice(TT_SITU)
        X = TT[tt]
        pool = [v['name'] for k, v in TT.items() if v['grp'] != X['grp']]
        return mcq(rng, f'स्थिति: {s}\nइस स्थिति के लिए सबसे उपयुक्त पाठ-प्रकार कौन-सा है?', X['name'], rng.sample(pool, 3),
                   f'पाठक ({X["aud"]}) और उद्देश्य को देखते हुए {X["name"]} सबसे उपयुक्त है।')
    kit.add(key, 'C1', (1, 3), pick, 'mcq', None, 'tt_pick')

    def plan(rng, slot):
        s, tt = rng.choice(TT_SITU)
        X = TT[tt]
        return dict(stem=f'स्थिति: {s}\nइस स्थिति के लिए (क) पाठ-प्रकार, (ख) लक्षित पाठक, (ग) उद्देश्य और (घ) रजिस्टर बताइए।',
                    answer=f'(क) {X["name"]}; (ख) {X["aud"]}; (ग) स्थिति के अनुसार सूचना देना/मनाना/अनुभव साझा करना; (घ) {X["reg"]}।', type='explain', marks=4,
                    markingKey=f'चारों भागों के लिए 1-1 अंक। पाठ-प्रकार: {X["name"]}; रजिस्टर: {X["reg"]} — मिलते-जुलते उचित उत्तर भी मान्य।')
    kit.add(key, 'C2', (2, 4), plan, 'explain', None, 'tt_plan')

    def why(rng, slot):
        s, tt = rng.choice(TT_SITU)
        X = TT[tt]
        oth = rng.choice([k for k, v in TT.items() if v['grp'] != X['grp']])
        Y = TT[oth]
        return dict(stem=f'स्थिति: {s}\nएक विद्यार्थी ने इसके लिए {Y["name"]} लिखा। यह चुनाव उपयुक्त क्यों नहीं है? सही पाठ-प्रकार बताकर दो परंपराओं के आधार पर समझाइए।',
                    answer=f'सही पाठ-प्रकार: {X["name"]} — {X["conv"][0]}; {X["conv"][1]}। {Y["name"]} का पाठक ({Y["aud"]}) और रजिस्टर ({Y["reg"]}) इस स्थिति से मेल नहीं खाते।',
                    type='short', marks=3, markingKey='1 अंक: सही पाठ-प्रकार; 2 अंक: पाठक/उद्देश्य/परंपराओं के आधार पर अनुपयुक्तता की व्याख्या (मानदंड C)।')
    kit.add(key, 'C3', (2, 4), why, 'short', None, 'tt_why')

    def which_tt(rng, slot):
        tt = rng.choice(list(TT))
        X = TT[tt]
        c = rng.choice(X['conv'])
        pool = [v['name'] for k, v in TT.items() if v['grp'] != X['grp']]
        return mcq(rng, f'निम्नलिखित विशेषता किस पाठ-प्रकार की प्रमुख परंपरा है?\n“{c}”', X['name'], rng.sample(pool, 3), f'यह {X["name"]} की परंपरा है।')
    kit.add(key, 'C1', (1, 3), which_tt, 'mcq', None, 'tt_which')

    def reg(rng, slot):
        tt = rng.choice(list(TT))
        X = TT[tt]
        return dict(stem=f'{X["name"]} लिखते समय रजिस्टर कैसा होना चाहिए और क्यों? लक्षित पाठक का उल्लेख करते हुए एक उदाहरण-वाक्य भी लिखिए।',
                    answer=f'रजिस्टर: {X["reg"]}। पाठक: {X["aud"]}। उदाहरण-वाक्य इसी रजिस्टर में हो।', type='explain', marks=3,
                    markingKey='1 अंक: उचित रजिस्टर; 1 अंक: पाठक से संबंध; 1 अंक: रजिस्टर के अनुरूप उदाहरण-वाक्य।')
    kit.add(key, 'C2', (2, 4), reg, 'explain', None, 'tt_reg')


CRIT = [
    ('शब्दावली की विविधता और सटीकता', 'A'), ('व्याकरणिक संरचनाओं की शुद्धता', 'A'), ('जटिल वाक्य-संरचनाओं का प्रभावी प्रयोग', 'A'),
    ('वर्तनी और लिंग-वचन की त्रुटियाँ', 'A'), ('मुहावरों और लोकोक्तियों का उचित प्रयोग', 'A'), ('भाषा का सहज प्रवाह', 'A'),
    ('कार्य में दिए गए सभी बिंदुओं को पूरा करना', 'B'), ('विचारों का विकास और ठोस उदाहरण', 'B'), ('अनुच्छेदों का तार्किक क्रम', 'B'),
    ('संयोजक शब्दों से विचारों को जोड़ना (सुसंगति)', 'B'), ('विषय से न भटकना और प्रासंगिक तर्क देना', 'B'), ('संदेश की स्पष्टता', 'B'),
    ('पाठ-प्रकार का सही चुनाव', 'C'), ('पाठक के अनुरूप रजिस्टर और लहजा', 'C'), ('पाठ-प्रकार की परंपराओं (प्रारूप, संबोधन) का पालन', 'C'),
    ('उद्देश्य (सूचना देना, मनाना आदि) के अनुरूप भाषा', 'C'), ('संदर्भ के अनुसार औपचारिकता का स्तर', 'C'),
]
CNAME = {'A': 'मानदंड A — भाषा (12 अंक)', 'B': 'मानदंड B — संदेश (12 अंक)', 'C': 'मानदंड C — अवधारणात्मक समझ (6 अंक)'}

SAMPLES = [
    ('नगर निगम को औपचारिक पत्र', '“अरे भाई साहब, हमारी गली की हालत देखो! एकदम कचरा ही कचरा है यार। जल्दी कुछ करो ना।”', 'C',
     'रजिस्टर अनौपचारिक है (‘अरे भाई साहब’, ‘यार’, ‘करो ना’); औपचारिक पत्र की परंपराएँ नहीं।', '“महोदय, मैं आपका ध्यान हमारी गली में फैली गंदगी की ओर आकर्षित करना चाहता हूँ। कृपया शीघ्र कार्रवाई करें।”'),
    ('विद्यालय-पत्रिका के लिए लेख: मोबाइल का प्रभाव', '“मोबाइल अच्छा है। मोबाइल बुरा भी है। मोबाइल से बात होती है। मोबाइल से आँखें ख़राब होती हैं।”', 'A',
     'वाक्य बहुत सरल और दोहराव वाले हैं; संयोजक और शब्दावली की विविधता नहीं।', '“मोबाइल फ़ोन ने संचार को सरल बनाया है, किंतु इसका अत्यधिक प्रयोग आँखों और एकाग्रता, दोनों को हानि पहुँचाता है।”'),
    ('पर्यावरण पर भाषण (कार्य: समस्या, कारण, समाधान)', 'विद्यार्थी ने समस्या और कारण विस्तार से बताए, पर समाधान का कोई उल्लेख नहीं किया।', 'B',
     'कार्य का एक आवश्यक बिंदु (समाधान) छूट गया; संदेश अधूरा है।', 'अंतिम अनुच्छेद में तीन ठोस समाधान जोड़ना: वृक्षारोपण, प्लास्टिक पर रोक, सार्वजनिक परिवहन।'),
    ('मित्र को अनौपचारिक पत्र', '“आदरणीय महोदय, मैं आपको सूचित करना चाहता हूँ कि मेरी छुट्टियाँ अच्छी बीतीं। भवदीय, राहुल।”', 'C',
     'मित्र के लिए अत्यधिक औपचारिक संबोधन और समापन; पाठक से संबंध के अनुरूप रजिस्टर नहीं।', '“प्रिय अमन, कैसे हो? मेरी छुट्टियाँ तो कमाल की रहीं! … तुम्हारा दोस्त, राहुल।”'),
    ('ब्लॉग: मेरी पहली ट्रेकिंग', '“मैं पहाड़ गया। फिर मैं ऊपर चढ़ा। फिर मैं नीचे आया। फिर मैं घर गया।”', 'A',
     '‘फिर’ की पुनरावृत्ति, सरल वाक्य, वर्णनात्मक शब्दावली का अभाव।', '“सुबह की ठंडी हवा में जब हमने चढ़ाई शुरू की, तो देवदार की ख़ुशबू ने थकान भुला दी।”'),
    ('मत-प्रधान लेख: क्या गृहकार्य बंद होना चाहिए?', 'विद्यार्थी ने पहले अनुच्छेद में ‘हाँ’ कहा, तीसरे में ‘नहीं’ और निष्कर्ष में फिर ‘हाँ’ — बिना कारण बताए।', 'B',
     'मत स्पष्ट और सुसंगत नहीं है; तर्कों का तार्किक विकास नहीं।', 'आरंभ में स्पष्ट मत, फिर पक्ष के तर्क, विपक्ष का खंडन (‘हालाँकि…, फिर भी…’), और उसी मत पर निष्कर्ष।'),
    ('समाचार रिपोर्ट: विद्यालय का खेल-दिवस', '“मुझे लगता है कि यह अब तक का सबसे शानदार खेल-दिवस था और हमारे प्रधानाचार्य सबसे अच्छे हैं!”', 'C',
     'समाचार में निजी राय और भावनात्मक भाषा; निष्पक्ष, तृतीय पुरुष शैली नहीं।', '“विद्यालय में शुक्रवार को वार्षिक खेल-दिवस आयोजित किया गया, जिसमें 600 विद्यार्थियों ने भाग लिया।”'),
    ('जागरूकता पत्रक: डेंगू से बचाव', 'विद्यार्थी ने डेंगू का इतिहास और वैज्ञानिक नाम पर पूरा पृष्ठ लिखा, बचाव के उपाय केवल एक पंक्ति में दिए।', 'B',
     'संदेश उद्देश्य (बचाव की जानकारी) पर केंद्रित नहीं; अप्रासंगिक विवरण अधिक।', 'उपशीर्षकों में स्पष्ट उपाय: ‘पानी जमा न होने दें’, ‘पूरी बाँह के कपड़े’, ‘लक्षण दिखें तो डॉक्टर से मिलें’।'),
    ('विद्यालय-पत्रिका के लिए लेख', '“आजकल विद्यार्थी लोग बहुत तनाव में रहती है क्योंकि उनको परीक्षा का डर लगते हैं।”', 'A',
     'कर्ता-क्रिया अन्विति की त्रुटियाँ (‘विद्यार्थी … रहती है’, ‘डर लगते हैं’)।', '“आजकल विद्यार्थी बहुत तनाव में रहते हैं, क्योंकि उन्हें परीक्षा का डर लगता है।”'),
    ('प्रधानाचार्य को ईमेल', 'ईमेल में ‘विषय’ पंक्ति नहीं है, और अंत में न नाम है न कक्षा।', 'C',
     'ईमेल की परंपराएँ (विषय-पंक्ति, हस्ताक्षर) छूट गईं; पाठक को संदर्भ नहीं मिलता।', '“विषय: विज्ञान-प्रयोगशाला के समय में परिवर्तन हेतु अनुरोध … सादर, नेहा वर्मा, कक्षा 11-ब।”'),
]


def g_criteria(kit, key, th):
    def crit(rng, slot):
        d, c = rng.choice(CRIT)
        w = [CNAME[x] for x in 'ABC' if x != c] + ['मौखिक मूल्यांकन का मानदंड B2']
        return mcq(rng, f'पेपर 1 के मूल्यांकन में “{d}” मुख्य रूप से किस मानदंड के अंतर्गत आता है?', CNAME[c], w, f'{d} — {CNAME[c]}।')
    kit.add(key, 'C1', (1, 3), crit, 'mcq', None, 'cr_id')

    def diag_mcq(rng, slot):
        t, s, c, why, fix = rng.choice(SAMPLES)
        w = [CNAME[x] for x in 'ABC' if x != c] + ['कोई कमी नहीं; यह उत्तर उत्कृष्ट है']
        return mcq(rng, f'कार्य: {t}\nविद्यार्थी के उत्तर का अंश/विवरण: {s}\nइस अंश में मुख्य कमज़ोरी किस मानदंड से संबंधित है?', CNAME[c], w, why)
    kit.add(key, ('C2', 'C3'), (2, 4), diag_mcq, 'mcq', None, 'cr_diag')

    def diag(rng, slot):
        t, s, c, why, fix = rng.choice(SAMPLES)
        return dict(stem=f'कार्य: {t}\nविद्यार्थी के उत्तर का अंश/विवरण: {s}\nएक परीक्षक के रूप में इस अंश की कमी पहचानिए, बताइए कि इसका असर किस मानदंड पर पड़ेगा और सुधरा हुआ रूप लिखिए।',
                    answer=f'कमी: {why} प्रभावित मानदंड: {CNAME[c]}। सुधरा रूप: {fix}', type='short', marks=4,
                    markingKey='1 अंक: कमी की सटीक पहचान; 1 अंक: सही मानदंड; 2 अंक: उपयुक्त सुधरा रूप (भाषा/संदेश/रजिस्टर के अनुसार)।')
    kit.add(key, 'C3', (3, 5), diag, 'short', None, 'cr_fix')

    def explain(rng, slot):
        c = rng.choice('ABC')
        ds = [d for d, x in CRIT if x == c]
        return dict(stem=f'{CNAME[c]} में परीक्षक किन बातों को देखते हैं? तीन बातें बताइए और प्रत्येक के लिए अपने लेखन को सुधारने का एक उपाय लिखिए।',
                    answer='संभावित बातें: ' + '; '.join(ds[:4]) + '। उपाय: अभ्यास, संशोधन-सूची, नमूना-उत्तर पढ़ना आदि।', type='explain', marks=3,
                    markingKey='तीन सही बातें, प्रत्येक के साथ व्यावहारिक उपाय — प्रत्येक के लिए 1 अंक।')
    kit.add(key, 'C2', (2, 4), explain, 'explain', None, 'cr_expl')


ERRS = [
    ('मेरे को यह किताब चाहिए।', 'मुझे यह किताब चाहिए।', 'सर्वनाम-रूप'),
    ('लड़की ने पत्र लिखा था और वह घर गया।', 'लड़की ने पत्र लिखा था और वह घर गई।', 'लिंग-अन्विति'),
    ('हम लोग कल बाज़ार जाएगा।', 'हम लोग कल बाज़ार जाएँगे।', 'वचन-अन्विति'),
    ('उसने खाना खाया और फिर उसने सो गया।', 'उसने खाना खाया और फिर वह सो गया।', '‘ने’ का प्रयोग'),
    ('मैंने उसको किताब दिया।', 'मैंने उसको किताब दी।', 'कर्म के अनुसार क्रिया'),
    ('यह बात मेरे लिए बहुत महत्वपूर्ण है, इसलिए क्योंकि मैं इसे लिख रहा हूँ।', 'यह बात मेरे लिए बहुत महत्वपूर्ण है, इसलिए मैं इसे लिख रहा हूँ।', 'संयोजक का दोहरा प्रयोग'),
    ('कृपया आप मुझे बताने की कृपा करें।', 'कृपया मुझे बताएँ।', 'शब्दों की पुनरावृत्ति'),
    ('सभी छात्रों ने अपना-अपना काम पूरा कर लिया हैं।', 'सभी छात्रों ने अपना-अपना काम पूरा कर लिया है।', 'सहायक क्रिया'),
    ('मेरी माता जी आ गई हैं और वे बहुत ख़ुश है।', 'मेरी माता जी आ गई हैं और वे बहुत ख़ुश हैं।', 'आदरसूचक बहुवचन'),
    ('उसे परीक्षा में अच्छे अंक प्राप्त हुआ।', 'उसे परीक्षा में अच्छे अंक प्राप्त हुए।', 'वचन-अन्विति'),
    ('मैं कल दिल्ली को गया था।', 'मैं कल दिल्ली गया था।', 'अनावश्यक परसर्ग'),
    ('पेड़ों पर पक्षी चहचहा रही है।', 'पेड़ों पर पक्षी चहचहा रहे हैं।', 'लिंग-वचन अन्विति'),
    ('राम और श्याम विद्यालय गया।', 'राम और श्याम विद्यालय गए।', 'संयुक्त कर्ता'),
    ('यदि तुम मेहनत करोगे, तो तुम सफल हुए।', 'यदि तुम मेहनत करोगे, तो तुम सफल होगे।', 'काल-संगति'),
    ('हमने बहुत मज़ा किया और खूब नाचा।', 'हमें बहुत मज़ा आया और हम खूब नाचे।', 'मुहावरेदार प्रयोग'),
    ('मैं आपसे निवेदन करता हूँ कि मेरे को छुट्टी दें।', 'मैं आपसे निवेदन करता हूँ कि मुझे छुट्टी दें।', 'सर्वनाम-रूप'),
    ('दादी ने मुझे एक कहानी सुनाया।', 'दादी ने मुझे एक कहानी सुनाई।', 'कर्म के अनुसार क्रिया'),
    ('यह सबसे सर्वश्रेष्ठ उपाय है।', 'यह सर्वश्रेष्ठ उपाय है।', 'अतिशयोक्त विशेषण'),
    ('हर एक विद्यार्थियों को पुरस्कार मिला।', 'हर एक विद्यार्थी को पुरस्कार मिला।', 'वचन'),
    ('कृपया नीचे लिखे हुए नियमों का पालन करें जो नीचे लिखे हैं।', 'कृपया नीचे लिखे नियमों का पालन करें।', 'पुनरावृत्ति'),
    ('मुझे चाय पसंद है परंतु लेकिन कॉफ़ी नहीं।', 'मुझे चाय पसंद है, परंतु कॉफ़ी नहीं।', 'संयोजक का दोहरा प्रयोग'),
    ('उसकी आँखों से आँसू बह रहा था।', 'उसकी आँखों से आँसू बह रहे थे।', 'वचन-अन्विति'),
    ('बच्चों ने मैदान में खेला और वे थक गई।', 'बच्चों ने मैदान में खेला और वे थक गए।', 'लिंग-अन्विति'),
    ('मैं तुम्हारा इंतज़ार कल से करता हूँ।', 'मैं तुम्हारा इंतज़ार कल से कर रहा हूँ।', 'काल-संगति'),
]


def g_errors(kit, key, th):
    def pick(rng, slot):
        w, r, t = rng.choice(ERRS)
        others = [x[0] for x in ERRS if x[0] != w]
        return mcq(rng, f'संशोधन-अभ्यास: “{w}” — इस वाक्य का शुद्ध रूप कौन-सा है?', r, [w] + _variants(w, r, rng), f'त्रुटि-प्रकार: {t}। शुद्ध रूप: {r}')
    kit.add(key, 'C1', (1, 3), pick, 'mcq', None, 'err_pick')

    def ident(rng, slot):
        w, r, t = rng.choice(ERRS)
        return dict(stem=f'संशोधन-अभ्यास: “{w}”\nइस वाक्य में त्रुटि पहचानिए, उसका प्रकार बताइए और शुद्ध वाक्य लिखिए।',
                    answer=f'त्रुटि-प्रकार: {t}। शुद्ध वाक्य: {r}', type='short', marks=2,
                    markingKey=f'1 अंक: त्रुटि और उसके प्रकार ({t}) की पहचान; 1 अंक: शुद्ध वाक्य — {r}')
    kit.add(key, 'C2', (1, 3), ident, 'short', None, 'err_id')

    def para(rng, slot):
        S = rng.sample(ERRS, 3)
        return dict(stem='अपने लेखन का संशोधन करते समय आपको नीचे दिए तीन वाक्यों में त्रुटियाँ मिलीं। प्रत्येक को शुद्ध कीजिए और बताइए कि यह त्रुटि मानदंड A को कैसे प्रभावित करती है।\n'
                         + '\n'.join(f'{i + 1}. {w}' for i, (w, r, t) in enumerate(S)),
                    answer=' '.join(f'{i + 1}. {r} ({t})' for i, (w, r, t) in enumerate(S)) + ' — ऐसी त्रुटियाँ भाषा की शुद्धता घटाती हैं और बार-बार होने पर अर्थ को अस्पष्ट करती हैं।',
                    type='short', marks=4, markingKey='3 अंक: तीनों वाक्यों का सही संशोधन (1-1); 1 अंक: मानदंड A (भाषा की शुद्धता) पर प्रभाव की व्याख्या।')
    kit.add(key, 'C3', (2, 4), para, 'short', None, 'err_para')


def _variants(w, r, rng):
    """Two plausible but wrong versions of the correct sentence, made by whole-word swaps."""
    SW = {'है': 'हैं', 'हैं': 'है', 'गए': 'गया', 'गई': 'गया', 'मुझे': 'मेरे को', 'था': 'थी', 'थे': 'था', 'रहे': 'रहा',
          'दी': 'दिया', 'दिया': 'दी', 'सुनाई': 'सुनाया', 'हुए': 'हुआ', 'होगे': 'हुए', 'जाएँगे': 'जाएगा', 'वह': 'उसने', 'हम': 'हमने',
          'आया': 'किया', 'नाचे': 'नाचा', 'विद्यार्थी': 'विद्यार्थियों', 'सर्वश्रेष्ठ': 'सबसे सर्वश्रेष्ठ', 'परंतु': 'परंतु लेकिन',
          'बताएँ।': 'बताने की कृपा करें।', 'इसलिए': 'इसलिए क्योंकि', 'दिल्ली': 'दिल्ली को', 'नियमों': 'लिखे हुए नियमों', 'ख़ुश': 'ख़ुशी'}
    toks = r.split(' ')
    idx = [i for i, t in enumerate(toks) if t.strip('।,') in SW or t in SW]
    rng.shuffle(idx)
    out = []
    for i in idx:
        t = toks[i]
        core = t if t in SW else t.strip('।,')
        v = ' '.join(toks[:i] + [t.replace(core, SW[core], 1)] + toks[i + 1:])
        if v not in (r, w) and v not in out:
            out.append(v)
        if len(out) == 2:
            break
    for i in range(len(idx)):
        if len(out) >= 2:
            break
        for k in range(i + 1, len(idx)):
            a, b = idx[i], idx[k]
            tt = list(toks)
            for z in (a, b):
                core = tt[z] if tt[z] in SW else tt[z].strip('।,')
                tt[z] = tt[z].replace(core, SW[core], 1)
            v = ' '.join(tt)
            if v not in (r, w) and v not in out:
                out.append(v)
                break
    while len(out) < 2:
        out.append('मूल वाक्य ही शुद्ध है; कोई परिवर्तन आवश्यक नहीं।' if 'मूल वाक्य ही शुद्ध है; कोई परिवर्तन आवश्यक नहीं।' not in out else w.replace('।', '') + ' भी।')
    return out[:2]


def g_timed(kit, key, th):
    def all_tasks():
        return [t for k in sorted(TH) for t in TH[k].get('tasks', [])]

    def timed(rng, slot):
        sit, tt, bl = rng.choice(all_tasks())
        X = TT[tt]
        m = slot.marks or 15
        stem = (f'समयबद्ध अभ्यास (60 मिनट: 5 मिनट योजना, 45 मिनट लेखन, 10 मिनट संशोधन)\n{sit}\n'
                f'उपयुक्त प्रारूप में {X["name"]} लिखिए। अपने उत्तर में: {"; ".join(bl)}। लिखने के बाद अपने उत्तर की भाषा-त्रुटियाँ जाँचिए। ({WORDS})')
        ans = f'अपेक्षित: {X["name"]} की परंपराएँ — {"; ".join(X["conv"][:3])}; विषय-वस्तु — {"; ".join(bl)}; रजिस्टर — {X["reg"]}।'
        return dict(stem=stem, answer=ans, markingKey=p1_key(m), type='long', marks=m, minutes=60)
    kit.add(key, 'C4', (4, 5), timed, 'long', 'p1', 'timed')

    def selfcheck(rng, slot):
        sit, tt, bl = rng.choice(all_tasks())
        X = TT[tt]
        return dict(stem=f'आपने यह कार्य लिखा है: “{sit}”\nअपने उत्तर के आत्म-मूल्यांकन के लिए मानदंड A, B और C पर आधारित पाँच प्रश्नों की जाँच-सूची बनाइए।',
                    answer=f'उदाहरण: (A) क्या लिंग-वचन और काल सही हैं? क्या शब्दावली विविध है? (B) क्या सभी बिंदु ({"; ".join(bl)}) पूरे हुए? क्या अनुच्छेद क्रमबद्ध हैं? (C) क्या {X["name"]} की परंपराएँ ({X["conv"][0]}) और रजिस्टर ({X["reg"]}) उचित हैं?',
                    type='short', marks=5, markingKey='5 अंक: प्रत्येक उचित, विशिष्ट जाँच-प्रश्न के लिए 1 अंक; तीनों मानदंडों का कम से कम एक प्रश्न आवश्यक।')
    kit.add(key, 'C3', (3, 5), selfcheck, 'short', None, 'selfchk')

    def wordcount(rng, slot):
        return mcq(rng, 'उच्च स्तर (HL) के पेपर 1 में लेखन के लिए अपेक्षित शब्द-सीमा क्या है?', '450–600 शब्द', ['250–400 शब्द', '100–150 शब्द', '800–1000 शब्द'],
                   'HL: 450–600 शब्द; SL: 250–400 शब्द।') if rng.random() < 0.5 else \
            mcq(rng, 'मानक स्तर (SL) के पेपर 1 में लेखन के लिए अपेक्षित शब्द-सीमा क्या है?', '250–400 शब्द', ['450–600 शब्द', '100–150 शब्द', '700–900 शब्द'],
                'SL: 250–400 शब्द; HL: 450–600 शब्द।')
    kit.add(key, 'C1', (1, 2), wordcount, 'mcq', None, 'wc')


SPEC['ch13-st1'] = ('reading', dict(focus='पाठ-प्रकार, पाठक, उद्देश्य और रजिस्टर का सही चुनाव स्पष्ट रूप से दिखाइए।', gens=[g_tt_situ], items=[
    ('C1', 'पेपर 1 में विद्यार्थी को कितने कार्यों में से एक चुनना होता है?', 'तीन', ['दो', 'चार', 'पाँच'], 'पेपर 1 में तीन कार्य दिए जाते हैं, विद्यार्थी एक चुनता है।'),
    ('C2', 'पेपर 1 के लिए पाठ-प्रकारों को व्यक्तिगत, व्यावसायिक और जनसंचार — इन तीन समूहों में बाँटा जाता है। प्रत्येक समूह के दो उदाहरण दीजिए।', 'व्यक्तिगत: डायरी, ब्लॉग, अनौपचारिक पत्र; व्यावसायिक: औपचारिक पत्र, ईमेल, प्रस्ताव, रिपोर्ट; जनसंचार: लेख, समाचार रिपोर्ट, भाषण, विज्ञापन, पत्रक, समीक्षा।', '3 अंक: प्रत्येक समूह के दो सही उदाहरणों के लिए 1 अंक।', 3),
]))
SPEC['ch13-st2'] = ('none', dict(focus='लेखन के बाद मानदंड A, B और C के अनुसार अपने उत्तर की जाँच कीजिए।', gens=[g_criteria], items=[
    ('C1', 'पेपर 1 के लेखन-कार्य के कुल अंक कितने हैं?', '30', ['24', '25', '40'], 'A (12) + B (12) + C (6) = 30 अंक।'),
    ('C1', 'पेपर 1 में मानदंड C के अधिकतम अंक कितने हैं?', '6', ['12', '10', '8'], 'मानदंड C (अवधारणात्मक समझ) 6 अंकों का है।'),
    ('C1', 'पेपर 1 में मानदंड B (संदेश) के अधिकतम अंक कितने हैं?', '12', ['6', '10', '15'], 'मानदंड B 12 अंकों का है।'),
    ('C2', 'मानदंड B (संदेश) और मानदंड C (अवधारणात्मक समझ) में क्या अंतर है? एक उदाहरण दीजिए।', 'B — क्या कहा गया: विचार, विकास, क्रम और कार्य के बिंदु; C — कैसे कहा गया: पाठ-प्रकार, पाठक, उद्देश्य और रजिस्टर। उदाहरण: अच्छे तर्कों वाला लेख (B ऊँचा) यदि ‘यार’ जैसी भाषा में संपादक को लिखा जाए तो C कम।', '1 अंक: B की व्याख्या; 1 अंक: C की व्याख्या और उदाहरण।'),
    ('C4', 'एक मित्र कहता है, “पेपर 1 में बस व्याकरण ठीक हो, बाक़ी अंक अपने-आप मिल जाते हैं।” तीनों मानदंडों के आधार पर उसकी ग़लतफ़हमी दूर करते हुए 150 शब्दों का उत्तर लिखिए।', 'A (भाषा) केवल 12 अंक; B (संदेश) 12 अंक — विचारों का विकास, बिंदुओं को पूरा करना, सुसंगति; C (6) — पाठ-प्रकार और रजिस्टर। व्याकरण-शुद्ध पर अप्रासंगिक या ग़लत पाठ-प्रकार वाले उत्तर को कम अंक मिलेंगे।', '6 अंक: तीनों मानदंडों की सही व्याख्या (3), उदाहरण (2), सुसंगत भाषा (1)।', 6),
]))
SPEC['ch13-st3'] = ('none', dict(focus='समय-सीमा में लिखिए और अंतिम दस मिनट संशोधन के लिए रखिए।', gens=[g_errors, g_timed], items=[
    ('C1', 'HL पेपर 1 की कुल अवधि कितनी होती है?', '1 घंटा 30 मिनट', ['1 घंटा', '2 घंटे', '45 मिनट'], 'HL पेपर 1: 1 घंटा 30 मिनट; SL: 1 घंटा 15 मिनट।'),
    ('C2', 'परीक्षा में लेखन के बाद संशोधन करते समय किन तीन प्रकार की त्रुटियों पर विशेष ध्यान देना चाहिए?', 'लिंग-वचन और कर्ता-क्रिया की अन्विति; ‘ने’ परसर्ग के साथ क्रिया-रूप; वर्तनी (अनुस्वार/चंद्रबिंदु, ह्रस्व-दीर्घ) और विराम-चिह्न।', '3 अंक: प्रत्येक उचित त्रुटि-प्रकार के लिए 1 अंक।', 3),
]))



# --------------------------------------------------------------------------------------------
# ch14 – Paper 2: reading question types, listening strategies, timed practice
# --------------------------------------------------------------------------------------------
TH[14] = dict(
    name='पेपर 2: पठन और श्रवण',
    vocab=[
        ('अनुमान', 'संकेतों के आधार पर निकाला गया निष्कर्ष', 'अटकल', 'शीर्षक और चित्र देखकर पाठ के विषय का ____ लगाइए।'),
        ('औचित्य', 'किसी उत्तर के सही होने का कारण या प्रमाण', 'तर्कसंगत आधार', 'सही/गलत प्रश्नों में पाठ से ____ देना अनिवार्य है।'),
        ('संदर्भ', 'वह प्रसंग जिसमें कोई शब्द या बात आई हो', 'प्रसंग', 'किसी शब्द का अर्थ उसके ____ से समझिए।'),
        ('मुख्य', 'सबसे महत्त्वपूर्ण', 'प्रधान', 'हर अनुच्छेद का ____ विचार एक पंक्ति में लिखिए।'),
        ('सारांश', 'किसी पाठ की मुख्य बातों का संक्षिप्त रूप', 'संक्षेप', 'श्रव्य अंश सुनने के बाद उसका ____ अपने शब्दों में लिखिए।'),
        ('स्कैन', 'किसी विशेष जानकारी के लिए पाठ पर तेज़ी से नज़र दौड़ाना', 'खोजी पठन', 'तारीख़ें और नाम ढूँढ़ने के लिए पाठ को ____ कीजिए।'),
        ('लहजा', 'वक्ता या लेखक की भावना का स्वर', 'स्वर', 'वक्ता के ____ से पता चलता है कि वह नाराज़ है।'),
        ('विकल्प', 'चुनने के लिए दिए गए उत्तरों में से एक', 'चुनाव', 'बहुविकल्पी प्रश्न में हर ____ को ध्यान से पढ़िए।'),
        ('प्रतिलेख', 'बोले गए अंश का लिखित रूप', 'लिप्यंतर', 'अभ्यास के बाद श्रव्य अंश का ____ पढ़कर अपने उत्तर जाँचिए।'),
        ('संकेत-शब्द', 'वे शब्द जो विचार के मोड़ की सूचना दें', 'सूचक शब्द', '‘लेकिन’ और ‘दूसरी ओर’ जैसे ____ विचार बदलने का संकेत देते हैं।'),
        ('ध्यानपूर्वक', 'पूरी एकाग्रता के साथ', 'सावधानी से', 'निर्देश ____ पढ़िए; कभी-कभी केवल दो शब्द माँगे जाते हैं।'),
        ('समानार्थी', 'समान अर्थ वाला शब्द', 'पर्यायवाची', 'पाठ में प्रश्न के शब्द नहीं, उनके ____ शब्द मिल सकते हैं।'),
        ('अभिप्राय', 'किसी कथन के पीछे छिपा अर्थ या आशय', 'आशय', 'वक्ता के ____ को समझने के लिए उसकी आवाज़ के उतार-चढ़ाव पर ध्यान दीजिए।'),
        ('क्रमबद्ध', 'सही क्रम में लगा हुआ', 'सिलसिलेवार', 'घटनाओं को ____ करने वाले प्रश्नों में समय-सूचक शब्द देखिए।'),
    ],
    topics=['बहुविकल्पी प्रश्नों की रणनीति', 'सही/गलत और औचित्य', 'शब्द-संदर्भ प्रश्न', 'श्रवण से पहले पूर्वानुमान', 'मुख्य शब्द पहचानना', 'नोट लेना', 'समय-प्रबंधन'],
    texts=[
        dict(kind='लेख', title='क्या हम बहुत जल्दी में हैं?',
             body='सुबह की चाय से लेकर रात के आख़िरी संदेश तक, हमारा दिन एक दौड़ बन गया है। एक सर्वेक्षण के अनुसार भारत के महानगरों में 62 प्रतिशत युवा मानते हैं कि उनके पास ‘सोचने का समय’ नहीं है। '
                  'मनोवैज्ञानिक डॉ. अनुराधा सेन कहती हैं, “लगातार जल्दबाज़ी मस्तिष्क को हमेशा ‘ख़तरे’ की स्थिति में रखती है, जिससे चिड़चिड़ापन और नींद की कमी होती है।” '
                  'इसी के जवाब में ‘धीमा जीवन’ आंदोलन लोकप्रिय हो रहा है। इसके समर्थक बिना फ़ोन के भोजन करने, पैदल चलने और सप्ताह में एक दिन ‘डिजिटल उपवास’ रखने की सलाह देते हैं। '
                  'हालाँकि आलोचकों का कहना है कि यह आंदोलन केवल उन लोगों के लिए संभव है जिनके पास आर्थिक सुरक्षा है; दिहाड़ी मज़दूर के लिए ‘धीमा होना’ विकल्प नहीं, विलासिता है। '
                  'शायद समाधान बीच में है — गति को पूरी तरह छोड़ना नहीं, बल्कि यह पहचानना कि कब रुकना ज़रूरी है।',
             qs=[('C1', 'सर्वेक्षण के अनुसार कितने प्रतिशत युवा मानते हैं कि उनके पास सोचने का समय नहीं है?', '62 प्रतिशत', ['26 प्रतिशत', '52 प्रतिशत', '72 प्रतिशत']),
                 ('C1', '‘धीमा जीवन’ आंदोलन के समर्थक सप्ताह में एक दिन क्या रखने की सलाह देते हैं?', 'डिजिटल उपवास'),
                 ('C1', 'पाठ में ‘विलासिता’ शब्द का सबसे निकट अर्थ क्या है?', 'ऐसी सुविधा जो केवल संपन्न लोगों को मिल सके', ['मजबूरी', 'बीमारी', 'परंपरा']),
                 ('C2', 'डॉ. अनुराधा सेन के अनुसार लगातार जल्दबाज़ी का मस्तिष्क पर क्या प्रभाव पड़ता है? अपने शब्दों में लिखिए।', 'मस्तिष्क हमेशा तनाव/ख़तरे की अवस्था में रहता है, जिससे व्यक्ति चिड़चिड़ा हो जाता है और ठीक से सो नहीं पाता।'),
                 ('tf', '‘धीमा जीवन’ आंदोलन सभी आर्थिक वर्गों के लिए समान रूप से संभव है।', 'गलत', '“यह आंदोलन केवल उन लोगों के लिए संभव है जिनके पास आर्थिक सुरक्षा है।”'),
                 ('tf', 'लेखक का सुझाव है कि गति को पूरी तरह छोड़ देना चाहिए।', 'गलत', '“गति को पूरी तरह छोड़ना नहीं, बल्कि यह पहचानना कि कब रुकना ज़रूरी है।”'),
                 ('C3', 'चौथे वाक्य में ‘हालाँकि’ शब्द किस बात का संकेत देता है?', 'लेख में विपरीत दृष्टिकोण (आलोचना) प्रस्तुत किया जा रहा है', ['आगे एक उदाहरण आएगा', 'लेख समाप्त हो रहा है', 'पिछली बात को दोहराया जा रहा है']),
                 ('C3', 'लेखक का अपना दृष्टिकोण क्या है और यह पाठ के किस भाग से स्पष्ट होता है?', 'लेखक संतुलित मध्य मार्ग का समर्थन करता है — न पूरी जल्दबाज़ी, न पूरा ठहराव; यह अंतिम वाक्य (“शायद समाधान बीच में है…”) से स्पष्ट है।'),
                 ('C4', 'क्या किशोरों के लिए ‘डिजिटल उपवास’ व्यावहारिक है? लेख के तर्कों और अपने अनुभव से उत्तर दीजिए।', 'पक्ष: नींद, एकाग्रता, परिवार से संवाद; विपक्ष: पढ़ाई और मित्रता ऑनलाइन, सामाजिक दबाव। सुझाव: आंशिक उपवास, निश्चित समय। स्पष्ट निष्कर्ष।'),
             ]),
        dict(kind='साक्षात्कार', title='“मिट्टी ही मेरी प्रयोगशाला है” — युवा किसान रोहित से बातचीत',
             body='प्रश्न: रोहित जी, आपने इंजीनियरिंग छोड़कर खेती क्यों चुनी? उत्तर: मैं बेंगलुरु में नौकरी करता था, पर हर छुट्टी में गाँव आकर देखता कि पिताजी की ज़मीन बंजर होती जा रही है। मुझे लगा, मेरी असली ज़रूरत यहाँ है। '
                  'प्रश्न: शुरुआत कैसी रही? उत्तर: बहुत कठिन! पहले साल ओलावृष्टि ने आधी फ़सल बर्बाद कर दी। गाँव वाले हँसते थे कि पढ़ा-लिखा लड़का मिट्टी में हाथ गंदे कर रहा है। '
                  'प्रश्न: फिर बदलाव कैसे आया? उत्तर: मैंने ड्रिप-सिंचाई लगाई और रासायनिक खाद छोड़कर जैविक खाद अपनाई। तीसरे साल तक पानी की खपत चालीस प्रतिशत घट गई और मेरी जैविक हल्दी की माँग शहरों में बढ़ गई। '
                  'प्रश्न: युवाओं से क्या कहेंगे? उत्तर: खेती को पिछड़ापन मत समझिए। तकनीक और धैर्य हो, तो मिट्टी भी प्रयोगशाला बन जाती है।',
             qs=[('C1', 'रोहित खेती शुरू करने से पहले कहाँ नौकरी करते थे?', 'बेंगलुरु में', ['दिल्ली में', 'मुंबई में', 'विदेश में']),
                 ('C1', 'पहले साल रोहित की आधी फ़सल किससे बर्बाद हुई?', 'ओलावृष्टि से'),
                 ('C1', 'ड्रिप-सिंचाई के बाद पानी की खपत कितनी घटी?', 'चालीस प्रतिशत'),
                 ('C2', 'गाँव वाले शुरू में रोहित पर क्यों हँसते थे?', 'उन्हें अजीब लगता था कि एक पढ़ा-लिखा (इंजीनियर) युवक अच्छी नौकरी छोड़कर खेती जैसा मेहनत का काम कर रहा है।'),
                 ('tf', 'रोहित ने रासायनिक खाद का प्रयोग बढ़ा दिया।', 'गलत', '“रासायनिक खाद छोड़कर जैविक खाद अपनाई।”'),
                 ('C3', '“मिट्टी ही मेरी प्रयोगशाला है” — इस शीर्षक से रोहित के खेती के प्रति दृष्टिकोण के बारे में क्या पता चलता है?', 'वे खेती को प्रयोग, विज्ञान और नवाचार का क्षेत्र मानते हैं', ['वे खेती को केवल परंपरा मानते हैं', 'वे प्रयोगशाला की नौकरी याद करते हैं', 'वे मिट्टी की जाँच से परेशान हैं']),
                 ('C3', 'साक्षात्कार की संरचना (प्रश्न-उत्तर) पाठक को रोहित की कहानी समझने में कैसे सहायता करती है?', 'प्रश्न कहानी को चरणों में बाँटते हैं — कारण, संघर्ष, समाधान, संदेश; उत्तर प्रथम पुरुष में होने से रोहित की आवाज़ सीधे और विश्वसनीय रूप में आती है।'),
                 ('C4', 'क्या शिक्षित युवाओं का गाँव लौटकर खेती करना ग्रामीण भारत की समस्याओं का समाधान हो सकता है? साक्षात्कार के आधार पर तर्क दीजिए।', 'पक्ष: तकनीक, जल-संरक्षण, बाज़ार से जुड़ाव, पलायन में कमी। विपक्ष: पूँजी, जोखिम, मौसम, सामाजिक सोच। सरकार और सहकारी समितियों की भूमिका; संतुलित निष्कर्ष।'),
             ]),
        dict(kind='ब्लॉग प्रविष्टि', title='मेरी दादी की रसोई का विज्ञान',
             body='आज मैंने दादी से पूछा कि वे दाल में हमेशा हल्दी और हींग क्यों डालती हैं। वे हँसकर बोलीं, “स्वाद के लिए, और पेट के लिए।” मुझे यह जवाब अधूरा लगा, तो मैंने इंटरनेट और अपनी जीव-विज्ञान की किताब खँगाली। '
                  'पता चला कि हल्दी में करक्यूमिन नाम का तत्व सूजन कम करने में सहायक माना जाता है और हींग पाचन में मदद करती है। दादी ने कभी यह शब्द नहीं सुना, पर पीढ़ियों का अनुभव उन्हें यही सिखा गया। '
                  'फिर मैंने सोचा — क्या हर पुरानी परंपरा वैज्ञानिक होती है? नहीं। दादी यह भी मानती हैं कि रात को नाख़ून काटना अशुभ है, जिसका कोई प्रमाण नहीं। '
                  'तो मेरा निष्कर्ष? परंपरा को आँख मूँदकर मत मानो, और आँख मूँदकर ठुकराओ भी मत। सवाल पूछो — जैसे मैंने आज पूछा। आप अपने घर की कौन-सी परंपरा परखना चाहेंगे? टिप्पणी में लिखिए!',
             qs=[('C1', 'दादी दाल में हमेशा कौन-सी दो चीज़ें डालती हैं?', 'हल्दी और हींग', ['नमक और मिर्च', 'जीरा और धनिया', 'घी और चीनी']),
                 ('C1', 'हल्दी में पाए जाने वाले तत्व का नाम क्या है?', 'करक्यूमिन'),
                 ('C2', 'लेखक को दादी का जवाब ‘अधूरा’ क्यों लगा और उसने क्या किया?', 'दादी ने केवल ‘स्वाद और पेट’ कहा, वैज्ञानिक कारण नहीं बताया; इसलिए लेखक ने इंटरनेट और जीव-विज्ञान की किताब से कारण खोजा।'),
                 ('tf', 'लेखक के अनुसार दादी की सभी परंपराएँ वैज्ञानिक हैं।', 'गलत', '“क्या हर पुरानी परंपरा वैज्ञानिक होती है? नहीं।”'),
                 ('C3', '“आँख मूँदकर” मुहावरे का पाठ में क्या अर्थ है?', 'बिना सोचे-समझे', ['सोते हुए', 'डर के कारण', 'बहुत ध्यान से']),
                 ('C3', 'ब्लॉग के अंत में लेखक पूछता है, “आप अपने घर की कौन-सी परंपरा परखना चाहेंगे? टिप्पणी में लिखिए!” — ऐसा प्रश्न क्यों पूछा गया है? ब्लॉग की दो अन्य विशेषताएँ भी पाठ से बताइए।', 'पाठकों से संवाद और टिप्पणियों के लिए; अन्य विशेषताएँ: प्रथम पुरुष, आत्मीय-अनौपचारिक लहजा, निजी अनुभव, रोचक शीर्षक।'),
                 ('C4', '“परंपरा को आँख मूँदकर मत मानो, और आँख मूँदकर ठुकराओ भी मत।” — अपने परिवार या समुदाय की किसी परंपरा के उदाहरण से इस विचार का मूल्यांकन कीजिए।', 'परंपरा का उदाहरण; उसके पीछे का तर्क/प्रमाण; कौन-सा भाग उपयोगी, कौन-सा अंधविश्वास; प्रश्न पूछने और सम्मान, दोनों का संतुलन।'),
             ]),
    ],
    audio=[
        dict(kind='रेडियो घोषणा', title='मेट्रो सेवा में परिवर्तन',
             body='नमस्कार, यात्रियों के लिए एक महत्त्वपूर्ण सूचना। रखरखाव कार्य के कारण इस शनिवार और रविवार, नीली लाइन पर राजीव चौक से द्वारका तक मेट्रो सेवाएँ सुबह छह बजे के बजाय आठ बजे से आरंभ होंगी। '
                  'इस दौरान यात्रियों की सुविधा के लिए हर पंद्रह मिनट पर निःशुल्क शटल बसें चलाई जाएँगी, जो सभी प्रमुख स्टेशनों के बाहर से मिलेंगी। '
                  'कृपया ध्यान दें कि सोमवार से सेवाएँ सामान्य समय पर चलेंगी। अधिक जानकारी के लिए हेल्पलाइन नंबर 155370 पर संपर्क करें। असुविधा के लिए हमें खेद है। धन्यवाद।',
             qs=[('C1', 'शनिवार और रविवार को मेट्रो सेवाएँ किस समय से आरंभ होंगी?', 'सुबह आठ बजे से', ['सुबह छह बजे से', 'सुबह सात बजे से', 'दोपहर बारह बजे से']),
                 ('C1', 'शटल बसें कितनी देर के अंतराल पर चलेंगी?', 'हर पंद्रह मिनट पर', ['हर पाँच मिनट पर', 'हर आधे घंटे पर', 'हर घंटे']),
                 ('C1', 'मेट्रो सेवाएँ किस दिन से सामान्य समय पर चलेंगी?', 'सोमवार से'),
                 ('C2', 'सेवाओं में परिवर्तन का कारण क्या है और यात्रियों के लिए क्या वैकल्पिक व्यवस्था की गई है?', 'कारण: रखरखाव कार्य; व्यवस्था: प्रमुख स्टेशनों के बाहर से हर पंद्रह मिनट पर निःशुल्क शटल बसें।'),
                 ('tf', 'शटल बसों के लिए यात्रियों को किराया देना होगा।', 'गलत', '“निःशुल्क शटल बसें चलाई जाएँगी।”'),
                 ('C3', 'घोषणा के अंत में “असुविधा के लिए हमें खेद है” कहने का उद्देश्य क्या है?', 'यात्रियों के प्रति विनम्रता और ज़िम्मेदारी दिखाकर उनकी नाराज़गी कम करना', ['यात्रियों को सेवा बंद होने की धमकी देना', 'टिकट के दाम बढ़ने की सूचना देना', 'शटल बसों का विज्ञापन करना']),
                 ('C3', 'श्रवण से पहले ‘मेट्रो सेवा में परिवर्तन’ शीर्षक देखकर आप किन तीन प्रकार की जानकारियों का पूर्वानुमान लगाएँगे?', 'दिन/तारीख़ और समय; प्रभावित लाइन या स्टेशन; परिवर्तन का कारण और वैकल्पिक व्यवस्था/संपर्क नंबर।'),
             ]),
        dict(kind='पॉडकास्ट', title='‘भाषा-यात्रा’: बहुभाषी परिवारों की कहानी',
             body='स्वागत है ‘भाषा-यात्रा’ में! मैं हूँ सुमन। आज हमारे साथ हैं प्रोफ़ेसर इक़बाल अहमद, जो बहुभाषी परिवारों पर शोध करते हैं। प्रोफ़ेसर साहब, बच्चे एक साथ कई भाषाएँ कैसे सीख लेते हैं? '
                  'देखिए सुमन जी, बच्चे का मस्तिष्क भाषाओं के लिए स्पंज जैसा होता है। हमारे अध्ययन में तीन भाषाएँ बोलने वाले घरों के बच्चे समस्या-समाधान में औसतन बेहतर निकले। '
                  'लेकिन एक चुनौती भी है — कई माता-पिता अंग्रेज़ी के दबाव में घर की भाषा छोड़ देते हैं, और फिर बच्चे दादा-दादी से बात नहीं कर पाते। '
                  'मेरा सुझाव है ‘एक व्यक्ति, एक भाषा’ नियम: माँ एक भाषा में बात करे, पिता दूसरी में, और विद्यालय तीसरी भाषा सिखाए। भाषा केवल शब्द नहीं, पीढ़ियों का पुल है।',
             qs=[('C1', 'प्रोफ़ेसर इक़बाल अहमद किस विषय पर शोध करते हैं?', 'बहुभाषी परिवारों पर', ['बच्चों के खेलों पर', 'अंग्रेज़ी व्याकरण पर', 'विद्यालयी परीक्षाओं पर']),
                 ('C1', 'प्रोफ़ेसर ने बच्चे के मस्तिष्क की तुलना किससे की?', 'स्पंज से'),
                 ('C1', 'प्रोफ़ेसर किस नियम का सुझाव देते हैं?', '‘एक व्यक्ति, एक भाषा’ नियम'),
                 ('C2', 'प्रोफ़ेसर के अनुसार घर की भाषा छोड़ने का परिवार पर क्या नकारात्मक प्रभाव पड़ता है?', 'बच्चे दादा-दादी जैसी पुरानी पीढ़ी से बात नहीं कर पाते; पीढ़ियों का भावनात्मक और सांस्कृतिक संबंध टूटता है।'),
                 ('tf', 'अध्ययन में तीन भाषाएँ बोलने वाले घरों के बच्चे समस्या-समाधान में कमज़ोर निकले।', 'गलत', '“समस्या-समाधान में औसतन बेहतर निकले।”'),
                 ('C3', 'वक्ता ने ‘लेकिन’ शब्द के बाद किस बात की ओर ध्यान दिलाया?', 'बहुभाषिकता से जुड़ी एक चुनौती की ओर', ['एक और लाभ की ओर', 'कार्यक्रम के अंत की ओर', 'अपनी पुस्तक के विज्ञापन की ओर']),
                 ('C3', '“भाषा केवल शब्द नहीं, पीढ़ियों का पुल है” — इस वाक्य का आशय स्पष्ट कीजिए।', 'भाषा से परिवार की पीढ़ियाँ — दादा-दादी, माता-पिता और बच्चे — जुड़ती हैं; उसके साथ संस्कृति, कहानियाँ और स्मृतियाँ आगे जाती हैं; भाषा खोने से यह संबंध टूट जाता है।'),
                 ('C4', 'क्या भारतीय परिवारों में बच्चों को घर की भाषा से अधिक अंग्रेज़ी पर ध्यान देना चाहिए? पॉडकास्ट के आधार पर अपना मत दीजिए।', 'अंग्रेज़ी: अवसर, वैश्विक संपर्क; मातृभाषा: पहचान, पीढ़ियों का संबंध, संज्ञानात्मक लाभ। ‘एक व्यक्ति, एक भाषा’ जैसा संतुलन; स्पष्ट निष्कर्ष।'),
             ]),
        dict(kind='रेडियो साक्षात्कार', title='पर्वतारोही पेमा से बातचीत',
             body='उद्घोषक: आज हमारे स्टूडियो में हैं सिक्किम की पेमा डोलमा, जिन्होंने बीस साल की उम्र में माउंट एवरेस्ट पर तिरंगा फहराया। पेमा, सबसे कठिन पल कौन-सा था? '
                  'पेमा: शिखर से लगभग तीन सौ मीटर पहले मेरा ऑक्सीजन-मास्क जम गया। उस पल मुझे लगा कि सब ख़त्म हो गया। मेरे शेरपा साथी ने अपनी गरम दस्तानों वाली उँगलियों से उसे पिघलाया। '
                  'उद्घोषक: आपने तैयारी कैसे की? पेमा: दो साल तक रोज़ सुबह चार बजे उठकर पीठ पर बीस किलो का बोझ लेकर दौड़ती थी। और सबसे ज़रूरी — मन की तैयारी। पहाड़ शरीर से नहीं, धैर्य से जीते जाते हैं। '
                  'उद्घोषक: लड़कियों के लिए संदेश? पेमा: लोग कहेंगे, यह तुम्हारे बस की बात नहीं। उन्हें जवाब मत दीजिए, अपनी चढ़ाई से जवाब दीजिए।',
             qs=[('C1', 'पेमा ने किस उम्र में माउंट एवरेस्ट पर चढ़ाई की?', 'बीस साल की उम्र में', ['अठारह साल की उम्र में', 'पच्चीस साल की उम्र में', 'तीस साल की उम्र में']),
                 ('C1', 'शिखर से कितनी दूरी पहले पेमा का ऑक्सीजन-मास्क जम गया?', 'लगभग तीन सौ मीटर'),
                 ('C1', 'तैयारी के दौरान पेमा पीठ पर कितना बोझ लेकर दौड़ती थीं?', 'बीस किलो'),
                 ('C2', 'सबसे कठिन पल में पेमा की सहायता किसने और कैसे की?', 'उनके शेरपा साथी ने अपनी गरम दस्तानों वाली उँगलियों से जमे हुए मास्क को पिघलाया।'),
                 ('tf', 'पेमा के अनुसार पहाड़ केवल शारीरिक शक्ति से जीते जाते हैं।', 'गलत', '“पहाड़ शरीर से नहीं, धैर्य से जीते जाते हैं।”'),
                 ('C3', '“अपनी चढ़ाई से जवाब दीजिए” — पेमा का लड़कियों को क्या संदेश है?', 'आलोचकों से बहस करने के बजाय अपनी उपलब्धियों से उन्हें ग़लत सिद्ध करें', ['पहाड़ों पर चढ़ना छोड़ दें', 'लोगों की बातों का तुरंत जवाब दें', 'केवल शेरपा के साथ चढ़ाई करें']),
                 ('C3', 'श्रवण के दौरान नोट लेते समय आप इस साक्षात्कार की कौन-सी चार जानकारियाँ संक्षेप में लिखेंगे? संक्षिप्त नोट के रूप में लिखिए।', 'पेमा डोलमा — सिक्किम; 20 वर्ष — एवरेस्ट; 300 मी. पहले मास्क जमा — शेरपा ने मदद की; तैयारी: 2 साल, सुबह 4 बजे, 20 किलो; संदेश: धैर्य, चढ़ाई से जवाब।'),
                 ('C4', 'पेमा के अनुभव से साहस और टीम-भावना के बारे में आप क्या सीखते हैं? अपने जीवन के किसी चुनौतीपूर्ण अनुभव से तुलना कीजिए।', 'साहस = धैर्य और मन की तैयारी; टीम-भावना = शेरपा की सहायता; अनुशासन। व्यक्तिगत अनुभव से तुलना और निष्कर्ष।'),
             ]),
    ],
    texts2=[
        dict(kind='जागरूकता पत्रक', title='गर्मी की लहर (लू) से बचाव',
             body='लू से सावधान! तापमान 45 डिग्री से ऊपर जाने पर लू जानलेवा हो सकती है। क्या करें: दिन में कम से कम आठ-दस गिलास पानी पिएँ, भले ही प्यास न लगी हो। हल्के, ढीले और सूती कपड़े पहनें। '
                  'बाहर निकलें तो सिर को टोपी या गमछे से ढकें। क्या न करें: दोपहर बारह से तीन बजे के बीच धूप में न निकलें। बंद गाड़ी में बच्चों या पालतू जानवरों को अकेला न छोड़ें। '
                  'लक्षण पहचानें: चक्कर आना, तेज़ सिरदर्द, उल्टी या पसीना बंद हो जाना लू के संकेत हैं। ऐसे व्यक्ति को तुरंत छाया में लिटाएँ, गीले कपड़े से शरीर पोंछें और 108 पर फ़ोन करें। जन-स्वास्थ्य विभाग द्वारा जारी।',
             qs=[('C1', 'पत्रक के अनुसार दिन में कितना पानी पीना चाहिए?', 'कम से कम आठ-दस गिलास', ['दो-तीन गिलास', 'पंद्रह-बीस गिलास', 'केवल प्यास लगने पर']),
                 ('C1', 'किस समय धूप में निकलने से मना किया गया है?', 'दोपहर बारह से तीन बजे के बीच'),
                 ('C1', 'लू लगने पर किस नंबर पर फ़ोन करने को कहा गया है?', '108'),
                 ('C2', 'लू के किन्हीं दो लक्षणों और उस समय की जाने वाली दो प्राथमिक सहायताओं का उल्लेख कीजिए।', 'लक्षण: चक्कर, तेज़ सिरदर्द, उल्टी, पसीना बंद होना। सहायता: छाया में लिटाना, गीले कपड़े से शरीर पोंछना, 108 पर फ़ोन।'),
                 ('tf', 'पत्रक के अनुसार प्यास लगने पर ही पानी पीना चाहिए।', 'गलत', '“भले ही प्यास न लगी हो।”'),
                 ('C3', 'पत्रक को ‘क्या करें’, ‘क्या न करें’ और ‘लक्षण पहचानें’ खंडों में बाँटने का क्या लाभ है?', 'पाठक जल्दी और आसानी से ज़रूरी जानकारी ढूँढ़ सकता है', ['पत्रक लंबा और कठिन लगता है', 'केवल डॉक्टर इसे समझ सकते हैं', 'इससे विज्ञापन की जगह बनती है']),
                 ('C3', 'इस पत्रक की भाषा में आज्ञार्थ क्रियाओं (“पिएँ”, “पहनें”, “न निकलें”) का प्रयोग क्यों किया गया है?', 'सीधे, स्पष्ट निर्देश देने के लिए; ‘-एँ’ रूप विनम्र पर दृढ़ है; पाठक तुरंत कार्य कर सके — यह जागरूकता पत्रक की परंपरा है।'),
                 ('C4', 'आपके विचार से जलवायु-परिवर्तन के कारण बढ़ती गर्मी से निपटने के लिए सरकार और नागरिकों को क्या करना चाहिए? पत्रक के संदर्भ में उत्तर दीजिए।', 'नागरिक: पत्रक के उपाय, पेड़ लगाना, पानी बचाना; सरकार: शीतल आश्रय, काम के समय में बदलाव, हरित शहरी योजना, चेतावनी-प्रणाली।'),
             ]),
        dict(kind='समीक्षा', title='पुस्तक-समीक्षा: ‘पहाड़ों के पार’',
             body='लेखिका नीलिमा राव का पहला उपन्यास ‘पहाड़ों के पार’ उत्तराखंड के एक गाँव की किशोरी गौरी की कहानी है, जो पढ़ाई के लिए रोज़ बारह किलोमीटर पैदल चलती है। '
                  'उपन्यास की सबसे बड़ी ताक़त इसकी भाषा है — पहाड़ी शब्दों की मिठास और प्रकृति के सजीव चित्र पाठक को सीधे देवदार के जंगलों में ले जाते हैं। गौरी का चरित्र विश्वसनीय है; वह आदर्श नायिका नहीं, डरती भी है और ग़लतियाँ भी करती है। '
                  'फिर भी, उपन्यास का मध्य भाग कुछ खिंचा हुआ लगता है, और कुछ सहायक पात्र — जैसे गौरी के चाचा — अधूरे छोड़ दिए गए हैं। '
                  'कुल मिलाकर, यह उपन्यास पंद्रह वर्ष से अधिक आयु के उन पाठकों के लिए है जो संघर्ष और आशा की सच्ची कहानियाँ पसंद करते हैं। रेटिंग: पाँच में से चार सितारे।',
             qs=[('C1', 'उपन्यास की नायिका गौरी पढ़ाई के लिए रोज़ कितने किलोमीटर पैदल चलती है?', 'बारह किलोमीटर', ['दो किलोमीटर', 'बीस किलोमीटर', 'पाँच किलोमीटर']),
                 ('C1', 'समीक्षक ने उपन्यास को कितने सितारे दिए?', 'पाँच में से चार'),
                 ('C2', 'समीक्षक उपन्यास की भाषा की प्रशंसा क्यों करते हैं?', 'पहाड़ी शब्दों की मिठास और प्रकृति के सजीव चित्रों से पाठक को लगता है कि वह स्वयं पहाड़ों/जंगलों में है।'),
                 ('tf', 'समीक्षक के अनुसार गौरी एक आदर्श, कभी न डरने वाली नायिका है।', 'गलत', '“वह आदर्श नायिका नहीं, डरती भी है और ग़लतियाँ भी करती है।”'),
                 ('C3', 'तीसरे अनुच्छेद में ‘फिर भी’ से समीक्षक क्या करते हैं?', 'उपन्यास की कमियाँ बताकर संतुलित मूल्यांकन करते हैं', ['उपन्यास का सारांश देते हैं', 'लेखिका की जीवनी बताते हैं', 'दूसरे उपन्यास की तुलना करते हैं']),
                 ('C3', 'यह पाठ ‘समीक्षा’ है — इसके तीन प्रमाण पाठ से दीजिए।', 'शीर्षक में पुस्तक-नाम और लेखिका; संक्षिप्त कथासार; गुण (भाषा, चरित्र) और दोष (खिंचा मध्य भाग, अधूरे पात्र); लक्षित पाठक की सिफ़ारिश; रेटिंग।'),
                 ('C4', 'क्या कोई पात्र ‘आदर्श’ न होकर ग़लतियाँ करने वाला हो, तो वह पाठकों को अधिक प्रभावित करता है? इस समीक्षा और अपने पढ़े किसी पात्र के आधार पर उत्तर दीजिए।', 'विश्वसनीयता और पाठक का जुड़ाव; मानवीय कमज़ोरियाँ; उदाहरण (हामिद, हल्कू आदि या कोई अन्य); आदर्श पात्र प्रेरणा देते हैं — संतुलित निष्कर्ष।'),
             ]),
    ],
    audio2=[
        dict(kind='समाचार बुलेटिन', title='संध्या समाचार',
             body='नमस्कार, ये हैं आज के मुख्य समाचार। केरल के कोच्चि शहर में देश का पहला पूरी तरह सौर-ऊर्जा से चलने वाला जल-परिवहन टर्मिनल आज जनता के लिए खोला गया। इससे हर साल लगभग पाँच सौ टन कार्बन-उत्सर्जन कम होने का अनुमान है। '
                  'दूसरी ओर, राजस्थान के कई ज़िलों में पारा 47 डिग्री तक पहुँच गया है; प्रशासन ने विद्यालयों का समय सुबह साढ़े सात से साढ़े ग्यारह कर दिया है। '
                  'खेल जगत से — भारत की महिला हॉकी टीम ने एशियाई चैम्पियनशिप के सेमीफ़ाइनल में जापान को 3–1 से हराया। फ़ाइनल रविवार को चीन से होगा। मौसम: अगले दो दिन उत्तर भारत में आँधी की संभावना। अभी के लिए इतना ही।',
             qs=[('C1', 'देश का पहला सौर-ऊर्जा से चलने वाला जल-परिवहन टर्मिनल किस शहर में खोला गया?', 'कोच्चि', ['मुंबई', 'चेन्नई', 'गोवा']),
                 ('C1', 'राजस्थान में विद्यालयों का नया समय क्या है?', 'सुबह साढ़े सात से साढ़े ग्यारह बजे तक', ['सुबह आठ से दो बजे तक', 'दोपहर बारह से चार बजे तक', 'सुबह छह से दस बजे तक']),
                 ('C1', 'महिला हॉकी टीम ने सेमीफ़ाइनल में जापान को किस अंतर से हराया?', '3–1'),
                 ('C1', 'फ़ाइनल में भारत का मुक़ाबला किस टीम से होगा?', 'चीन से'),
                 ('C2', 'सौर-ऊर्जा टर्मिनल पर्यावरण के लिए क्यों महत्त्वपूर्ण है?', 'यह हर साल लगभग पाँच सौ टन कार्बन-उत्सर्जन घटाएगा और स्वच्छ ऊर्जा से परिवहन का उदाहरण बनेगा।'),
                 ('tf', 'अगले दो दिन उत्तर भारत में भारी बर्फ़बारी की संभावना है।', 'गलत', '“अगले दो दिन उत्तर भारत में आँधी की संभावना।”'),
                 ('C3', 'बुलेटिन में ‘दूसरी ओर’ वाक्यांश का प्रयोग किस उद्देश्य से हुआ है?', 'एक समाचार से दूसरे, अलग प्रकार के समाचार पर जाने के लिए', ['पिछले समाचार को दोहराने के लिए', 'बुलेटिन समाप्त करने के लिए', 'मौसम का पूर्वानुमान देने के लिए']),
                 ('C3', 'समाचार बुलेटिन सुनते समय नोट लेने के लिए आप कौन-सी तालिका बनाएँगे? इस बुलेटिन के आधार पर उसे भरिए।', 'स्तंभ: समाचार | स्थान | मुख्य तथ्य/संख्या। सौर टर्मिनल | कोच्चि | 500 टन कार्बन कम; गर्मी | राजस्थान | 47°, स्कूल 7:30–11:30; हॉकी | एशियाई चैम्पियनशिप | जापान पर 3–1, फ़ाइनल रविवार चीन से; मौसम | उत्तर भारत | आँधी।'),
             ]),
        dict(kind='भाषण', title='विद्यालय-सभा में पूर्व छात्रा का संबोधन',
             body='आदरणीय प्रधानाचार्य जी, शिक्षकगण और मेरे प्यारे साथियो! पंद्रह साल पहले मैं भी इन्हीं पंक्तियों में बैठती थी — सबसे पीछे, ताकि कोई मुझसे प्रश्न न पूछे। '
                  'मैं गणित में दो बार फ़ेल हुई। एक दिन हमारी गणित-शिक्षिका शर्मा मैडम ने मुझसे कहा, “तुम्हें गणित नहीं आता, यह सच नहीं है; तुमने अभी तक उससे दोस्ती नहीं की है।” '
                  'उस एक वाक्य ने मेरी दिशा बदल दी। आज मैं इसरो में उपग्रहों की कक्षा की गणना करती हूँ। साथियो, असफलता अंत नहीं, एक पड़ाव है। '
                  'अपने शिक्षकों से प्रश्न पूछिए, ग़लतियाँ करने से मत डरिए, और कभी किसी को यह मत कहने दीजिए कि कोई विषय आपके बस का नहीं। धन्यवाद।',
             qs=[('C1', 'वक्ता किस संस्था में काम करती हैं?', 'इसरो में', ['एक बैंक में', 'इसी विद्यालय में', 'एक अस्पताल में']),
                 ('C1', 'वक्ता गणित में कितनी बार फ़ेल हुई थीं?', 'दो बार'),
                 ('C1', 'वक्ता की गणित-शिक्षिका का नाम क्या था?', 'शर्मा मैडम'),
                 ('C2', 'विद्यार्थी के रूप में वक्ता सबसे पीछे क्यों बैठती थीं, और इससे उनके तब के आत्मविश्वास के बारे में क्या पता चलता है?', 'ताकि कोई उनसे प्रश्न न पूछे; इससे पता चलता है कि उनमें आत्मविश्वास की कमी थी और वे असफलता से डरती थीं।'),
                 ('tf', 'शर्मा मैडम ने कहा कि वक्ता को गणित बिल्कुल नहीं आता।', 'गलत', '“तुम्हें गणित नहीं आता, यह सच नहीं है; तुमने अभी तक उससे दोस्ती नहीं की है।”'),
                 ('C3', '“असफलता अंत नहीं, एक पड़ाव है” — इस कथन से वक्ता श्रोताओं को क्या समझाना चाहती हैं?', 'असफलता अस्थायी है और आगे बढ़ने की यात्रा का हिस्सा है', ['असफल होने पर पढ़ाई छोड़ देनी चाहिए', 'गणित सबसे कठिन विषय है', 'केवल शिक्षक ही सफलता दिला सकते हैं']),
                 ('C3', 'वक्ता ने अपने भाषण को प्रभावशाली बनाने के लिए कौन-सी तीन तकनीकें अपनाई हैं?', 'निजी कहानी/अनुभव; शिक्षिका का उद्धरण; श्रोताओं से सीधा संबोधन (‘साथियो’); आज्ञार्थ आह्वान (‘प्रश्न पूछिए’, ‘मत डरिए’); सूक्ति जैसा वाक्य।'),
                 ('C4', 'क्या एक शिक्षक का एक वाक्य सचमुच किसी विद्यार्थी का जीवन बदल सकता है? भाषण और अपने अनुभव के आधार पर विचार कीजिए।', 'हाँ: प्रोत्साहन, ‘ग्रोथ माइंडसेट’, आत्मविश्वास (भाषण का उदाहरण); सीमाएँ: विद्यार्थी का अपना परिश्रम और परिस्थितियाँ। व्यक्तिगत उदाहरण, निष्कर्ष।'),
             ]),
    ],
    tasks=[
        ('आपने एक रेडियो-कार्यक्रम में किसी वैज्ञानिक का प्रेरक साक्षात्कार सुना। उसके बारे में अपने ब्लॉग-पाठकों को बताइए।', 'blog',
         ['वैज्ञानिक और उनका काम', 'साक्षात्कार की सबसे प्रेरक बात', 'आपने क्या सीखा']),
        ('आपके शहर में लू (गर्मी की लहर) से कई लोग बीमार पड़ रहे हैं। नागरिकों के लिए पत्रक तैयार कीजिए।', 'brochure',
         ['लू के ख़तरे', 'बचाव के उपाय', 'आपातकालीन संपर्क']),
        ('आपके विद्यालय की एक पूर्व छात्रा ने अंतरिक्ष-विज्ञान में बड़ी उपलब्धि पाई है। विद्यालय-पत्रिका के लिए उनका साक्षात्कार लिखिए।', 'interview',
         ['विद्यालय की यादें', 'संघर्ष और सफलता', 'विद्यार्थियों के लिए संदेश']),
        ('“क्या हम बहुत जल्दी में हैं?” — इस प्रश्न पर अपने विचार राष्ट्रीय समाचार-पत्र के युवा-स्तंभ के लिए लिखिए।', 'opinion',
         ['तेज़ जीवन-शैली के उदाहरण', 'इसके प्रभाव', 'संतुलन के सुझाव']),
        ('आपने हाल ही में एक उपन्यास पढ़ा जिसकी नायिका संघर्ष करके शिक्षा प्राप्त करती है। उसकी समीक्षा लिखिए।', 'review',
         ['कहानी और पात्र', 'भाषा और शैली के गुण-दोष', 'पाठकों के लिए सिफ़ारिश']),
        ('आपके इलाक़े में मेट्रो के काम के कारण सड़कों पर भारी जाम लगता है। मेट्रो प्राधिकरण को पत्र लिखिए।', 'fletter',
         ['समस्या का विवरण', 'नागरिकों पर प्रभाव', 'वैकल्पिक व्यवस्था के सुझाव']),
    ],
    discuss=[
        ('क्या पढ़ने की तुलना में सुनकर समझना अधिक कठिन है?', ['सुनने में दोबारा देखने का अवसर नहीं', 'लहजा और गति', 'अभ्यास से सुधार']),
        ('क्या बहुविकल्पी प्रश्न वास्तविक समझ को मापते हैं?', ['तेज़ और निष्पक्ष मूल्यांकन', 'अनुमान से सही उत्तर', 'खुले प्रश्नों का महत्त्व']),
        ('क्या हिंदी समाचार और पॉडकास्ट सुनना भाषा सीखने का सबसे अच्छा तरीक़ा है?', ['वास्तविक भाषा और उच्चारण', 'नई शब्दावली', 'केवल सुनना पर्याप्त नहीं']),
        ('क्या परीक्षा में समय का दबाव विद्यार्थियों की असली क्षमता छिपा देता है?', ['तनाव और ग़लतियाँ', 'वास्तविक जीवन में भी समय-सीमा', 'रणनीति से दबाव कम करना']),
        ('क्या डिजिटल युग में लंबे पाठ पढ़ने की आदत ख़त्म हो रही है?', ['छोटी पोस्टें और वीडियो', 'एकाग्रता में कमी', 'ई-पुस्तकें और ऑडियो-पुस्तकें']),
    ],
)

P2_ITEMS_R = [
    ('C1', 'सही/गलत प्रश्न में पूरे अंक पाने के लिए क्या आवश्यक है?', 'सही/गलत लिखने के साथ पाठ से औचित्य (प्रमाण) देना', ['केवल ‘सही’ या ‘गलत’ लिखना', 'अपने शब्दों में लंबा निबंध लिखना', 'प्रश्न को दोबारा लिखना'], 'औचित्य के बिना अंक नहीं मिलते।'),
    ('C1', 'पठन में ‘स्कैनिंग’ का प्रयोग कब किया जाता है?', 'किसी विशेष तथ्य, नाम या संख्या को तेज़ी से ढूँढ़ने के लिए', ['पूरे पाठ का भाव समझने के लिए', 'कविता का सौंदर्य समझने के लिए', 'पाठ को कंठस्थ करने के लिए'], 'स्कैनिंग = विशिष्ट जानकारी की खोज।'),
    ('C1', 'पठन में ‘स्किमिंग’ का उद्देश्य क्या है?', 'पाठ का सामान्य विषय और मुख्य विचार जल्दी समझना', ['हर शब्द का अर्थ खोजना', 'वर्तनी की त्रुटियाँ ढूँढ़ना', 'केवल अंतिम पंक्ति पढ़ना'], 'स्किमिंग = सरसरी नज़र से मुख्य विचार।'),
    ('C1', 'बहुविकल्पी प्रश्न में सबसे अच्छी रणनीति कौन-सी है?', 'पहले स्पष्ट रूप से ग़लत विकल्प हटाना, फिर पाठ से मिलान करना', ['सबसे लंबा विकल्प चुनना', 'हमेशा पहला विकल्प चुनना', 'पाठ पढ़े बिना अनुमान लगाना'], 'विलोपन की विधि और पाठ से मिलान।'),
    ('C2', '‘शब्द-संदर्भ’ प्रश्न (जैसे, पाठ में ‘विलासिता’ का अर्थ) हल करने के तीन चरण बताइए।', 'शब्द वाला पूरा वाक्य और आसपास के वाक्य पढ़ना; वाक्य में शब्द का कार्य (संज्ञा/विशेषण) और भाव समझना; विकल्प को शब्द की जगह रखकर देखना कि अर्थ बना रहता है या नहीं।', '3 अंक: प्रत्येक उचित चरण के लिए 1 अंक।', 3),
    ('C2', 'प्रश्न में ‘पाठ के शब्दों में’ और ‘अपने शब्दों में’ लिखा हो, तो उत्तर देने में क्या अंतर होगा?', '‘पाठ के शब्दों में’ — पाठ से सटीक शब्द/वाक्यांश उतारना; ‘अपने शब्दों में’ — अर्थ को अपनी भाषा में फिर से कहना, पाठ की पंक्ति ज्यों की त्यों नहीं।', '1 अंक: पहले निर्देश की सही व्याख्या; 1 अंक: दूसरे की।'),
    ('C3', 'पाठ के उत्तर ढूँढ़ते समय यह क्यों याद रखना चाहिए कि प्रश्न के शब्द पाठ में अक्सर समानार्थी रूप में होते हैं? एक उदाहरण दीजिए।', 'परीक्षक सीधे मिलान से बचने के लिए समानार्थी शब्द रखते हैं, ताकि समझ परखी जाए। उदाहरण: प्रश्न में ‘निःशुल्क’, पाठ में ‘मुफ़्त’; प्रश्न में ‘चुनौती’, पाठ में ‘कठिनाई’।', '2 अंक: कारण (1), उचित उदाहरण (1)।', 2),
]
P2_ITEMS_L = [
    ('C1', 'पेपर 2 के श्रवण भाग में प्रत्येक श्रव्य अंश कितनी बार सुनाया जाता है?', 'दो बार', ['एक बार', 'तीन बार', 'चार बार'], 'प्रत्येक श्रव्य अंश दो बार सुनाया जाता है।'),
    ('C1', 'श्रवण से पहले प्रश्न पढ़ने का सबसे बड़ा लाभ क्या है?', 'पता चल जाता है कि किस जानकारी को ध्यान से सुनना है', ['उत्तर अपने-आप मिल जाते हैं', 'श्रव्य अंश छोटा हो जाता है', 'प्रश्न बदल जाते हैं'], 'पूर्व-पठन से सुनने का उद्देश्य तय होता है।'),
    ('C1', 'श्रवण के दौरान नोट लेने का सबसे अच्छा ढंग कौन-सा है?', 'मुख्य शब्द, संख्याएँ और संक्षिप्त संकेत लिखना', ['हर शब्द पूरा लिखना', 'कुछ भी न लिखना', 'केवल अपनी राय लिखना'], 'संक्षिप्त नोट से ध्यान नहीं भटकता।'),
    ('C1', 'वक्ता ‘लेकिन’, ‘दूसरी ओर’, ‘हालाँकि’ कहे, तो इसका क्या संकेत है?', 'विचार में मोड़ या विरोधी बात आने वाली है', ['भाषण समाप्त हो रहा है', 'वक्ता प्रश्न पूछ रहा है', 'एक संख्या आने वाली है'], 'ये विरोध-सूचक संकेत-शब्द हैं।'),
    ('C2', 'श्रवण-अंश का शीर्षक और प्रकार (जैसे ‘रेडियो घोषणा’) जानकर पूर्वानुमान कैसे लगाया जाता है? एक उदाहरण दीजिए।', 'पाठ-प्रकार से संरचना और जानकारी का अनुमान: घोषणा में समय, स्थान, परिवर्तन, संपर्क; साक्षात्कार में प्रश्न-उत्तर, अनुभव, संदेश। उदाहरण: ‘मेट्रो सेवा में परिवर्तन’ — तारीख़, समय, विकल्प।', '1 अंक: पूर्वानुमान की विधि; 1 अंक: उदाहरण।'),
    ('C2', 'पहली और दूसरी बार सुनते समय आपकी रणनीति में क्या अंतर होना चाहिए?', 'पहली बार: मुख्य विचार और आसान तथ्य, संक्षिप्त नोट; दूसरी बार: छूटी जानकारी, विवरण और कठिन प्रश्नों के उत्तर जाँचना।', '1 अंक: पहली बार की रणनीति; 1 अंक: दूसरी बार की।'),
    ('C3', 'वक्ता के ‘लहजे’ से उसके दृष्टिकोण का अनुमान कैसे लगाया जा सकता है? दो संकेत बताइए।', 'आवाज़ का उतार-चढ़ाव और गति (उत्साह/चिंता); भावसूचक शब्द और विस्मयादिबोधक; कुछ शब्दों पर ज़ोर; हँसी, विराम या व्यंग्य।', '2 अंक: दो उचित संकेत, प्रत्येक 1 अंक।', 2),
]

SPEC['ch14-st1'] = ('reading', dict(focus='लेखन में पढ़े गए पाठ के तथ्यों और तर्कों का प्रमाण सहित प्रयोग कीजिए।', items=P2_ITEMS_R))
SPEC['ch14-st2'] = ('listening', dict(focus='लेखन में सुनी गई जानकारी को व्यवस्थित नोट्स से विकसित कीजिए।', items=P2_ITEMS_L))
SPEC['ch14-st3'] = ('none', dict(focus='समय-सीमा का पालन करते हुए योजना, लेखन और संशोधन कीजिए।', gens=[
    lambda kit, key, th: kit.texts(key, th, 'texts2', 'p2r'),
    lambda kit, key, th: kit.texts(key, th, 'audio2', 'p2l'),
    lambda kit, key, th: kit.vocab(key, th, ('c1', 'c2')),
], items=[
    ('C1', 'पेपर 2 में पठन भाग के कुल अंक कितने होते हैं?', '40', ['25', '30', '65'], 'पठन 40 अंक, श्रवण 25 अंक।'),
    ('C1', 'पेपर 2 में श्रवण भाग के कुल अंक कितने होते हैं?', '25', ['40', '30', '15'], 'श्रवण 25 अंक।'),
    ('C2', 'पेपर 2 के पठन भाग (तीन पाठ) में समय का बँटवारा कैसे करेंगे? कारण सहित बताइए।', 'हर पाठ के लिए लगभग बराबर समय, प्रश्नों के अंकों के अनुसार; अंत में 5 मिनट जाँच के लिए; कठिन प्रश्न पर अटकें नहीं, बाद में लौटें।', '1 अंक: व्यावहारिक बँटवारा; 1 अंक: कारण।'),
    ('C3', 'आपके पास पठन-परीक्षा में दस मिनट बचे हैं और एक पूरा पाठ बाक़ी है। आप किस क्रम में प्रश्न हल करेंगे और क्यों?', 'पहले बहुविकल्पी और तथ्यात्मक (कम समय, निश्चित अंक) प्रश्न, फिर सही/गलत औचित्य सहित, अंत में लंबे उत्तर वाले प्रश्न संक्षेप में; कोई प्रश्न ख़ाली न छोड़ें।', '3 अंक: तर्कसंगत क्रम (2), कारण (1)।', 3),
]))



# --------------------------------------------------------------------------------------------
# Extra questions on the listening transcripts (Paper 2 listening needs a deep pool for mocks)
# --------------------------------------------------------------------------------------------
EXTRA_AUDIO_QS = {
    '‘सेहत की बात’ — डॉ. रश्मि त्रिपाठी से बातचीत': [
        ('C1', 'डॉ. त्रिपाठी के अनुसार किशोरों के तनाव का एक नया कारण क्या है?', 'सोशल मीडिया पर लगातार दूसरों से तुलना', ['खेलों की कमी', 'महँगी फ़ीस', 'भारी बस्ता']),
        ('C2', 'डॉ. त्रिपाठी माता-पिता को कौन-सी दो सलाह देती हैं? अपने शब्दों में लिखिए।', 'बच्चों को डाँटने के बजाय उनकी बात ध्यान से सुनें, और हर दिन पंद्रह मिनट बिना फ़ोन के उनसे बातचीत करें।'),
        ('C3', 'डॉ. त्रिपाठी का “पढ़ाई का दबाव तो हमेशा था, पर अब…” कहना क्या संकेत देता है?', 'तनाव के पुराने कारण बने हुए हैं, पर नए कारण (सोशल मीडिया, कम नींद) जुड़ने से समस्या पहले से गंभीर हो गई है।'),
    ],
    'आकाशवाणी: डेंगू से बचाव का संदेश': [
        ('C1', 'यह संदेश किसकी ओर से प्रसारित किया गया है?', 'स्वास्थ्य मंत्रालय की ओर से', ['एक निजी अस्पताल की ओर से', 'नगर निगम की ओर से', 'एक दवा कंपनी की ओर से']),
        ('C2', 'संदेश के अनुसार मच्छर के काटने से बचने के कौन-से दो व्यक्तिगत उपाय हैं?', 'पूरी बाँह के कपड़े पहनना और मच्छरदानी का प्रयोग करना।'),
        ('C3', 'संदेश में ‘साफ़, रुके हुए पानी’ पर ज़ोर क्यों दिया गया है, जबकि लोग प्रायः गंदे पानी को ही ख़तरनाक मानते हैं?', 'आम धारणा को सुधारने के लिए: डेंगू का मच्छर साफ़ रुके पानी (कूलर, गमले) में पनपता है, इसलिए लोग घर के भीतर के साफ़ दिखने वाले पानी पर भी ध्यान दें।'),
    ],
    '‘नींद क्यों ज़रूरी है?’ — पॉडकास्ट ‘तन-मन’ का अंश': [
        ('C1', 'सर्वेक्षण के अनुसार बड़े शहरों के आधे से ज़्यादा किशोर कितने घंटे से कम सोते हैं?', 'सात घंटे से कम', ['पाँच घंटे से कम', 'दस घंटे से कम', 'चार घंटे से कम']),
        ('C2', 'आरव के अनुसार नींद के दौरान दिमाग़ क्या करता है, और इसका पढ़ाई से क्या संबंध है?', 'दिमाग़ दिन भर सीखी बातों को सहेजता (याद में पक्का करता) है; इसलिए पर्याप्त नींद से पढ़ा हुआ बेहतर याद रहता है।'),
        ('C3', 'पॉडकास्ट में पहले वैज्ञानिक तथ्य और सर्वेक्षण, फिर अंत में सुझाव क्यों दिया गया है?', 'तथ्यों और आँकड़ों से विश्वसनीयता बनती है और समस्या स्पष्ट होती है; फिर सुझाव (सोने से पहले स्क्रीन बंद) श्रोता को व्यावहारिक और तर्कसंगत लगता है।'),
    ],
    '‘हौसलों की उड़ान’ — चित्रकार फ़ातिमा शेख़ से बातचीत': [
        ('C1', 'फ़ातिमा शेख़ चित्र किस तरह बनाती हैं?', 'पैरों से', ['बाएँ हाथ से', 'मुँह में ब्रश पकड़कर', 'कंप्यूटर से']),
        ('C2', 'कला-विद्यालय के इनकार के बाद फ़ातिमा ने क्या किया और इसका क्या परिणाम निकला?', 'उन्होंने हार नहीं मानी और घर पर अभ्यास जारी रखा; परिणामस्वरूप पिछले साल उसी विद्यालय ने उनकी प्रदर्शनी लगाई।'),
        ('C3', 'फ़ातिमा ने ‘सामान्य’ शब्द को उद्धरण-चिह्नों में क्यों रखा है? इससे उनकी किस भावना का पता चलता है?', 'वे इस शब्द पर व्यंग्य करती हैं और उस सोच पर प्रश्न उठाती हैं जो विकलांग लोगों को ‘असामान्य’ मानती है; इसमें आहत भावना और आत्मसम्मान दोनों झलकते हैं।'),
    ],
    '‘मेरी कहानी’ — ढाबा चलाने वाली दादी की बातें': [
        ('C1', 'कमला दादी की उम्र कितनी है?', 'सत्तर वर्ष', ['चालीस वर्ष', 'साठ वर्ष', 'अस्सी वर्ष']),
        ('C2', 'पति के निधन के बाद दादी की आर्थिक स्थिति कैसी थी और आज कैसी है? तुलना कीजिए।', 'तब उनके पास केवल एक चूल्हा और दो बर्तन थे; आज उनके ढाबे पर दस लोग काम करते हैं, दूर-दूर से ग्राहक आते हैं और उन्होंने बेटियों को इंजीनियर बनाया।'),
        ('C3', 'प्रस्तोता ने दादी की बेटियों के इंजीनियर बनने की बात अंत में क्यों रखी है?', 'यह दादी के संघर्ष का सबसे बड़ा फल है और दिखाता है कि उनकी सफलता अगली पीढ़ी तक पहुँची; अंत में रखने से श्रोता पर गहरा प्रभाव पड़ता है।'),
    ],
    '‘आज का प्रेरक व्यक्तित्व’ — मैरी कॉम': [
        ('C1', 'मैरी कॉम किस खेल से जुड़ी हैं?', 'मुक्केबाज़ी', ['कुश्ती', 'भारोत्तोलन', 'तीरंदाज़ी']),
        ('C2', 'माँ बनने के बाद मैरी कॉम की ‘शानदार वापसी’ को वार्ताकार इतना महत्त्वपूर्ण क्यों मानते हैं?', 'आम धारणा है कि माँ बनने के बाद महिला खिलाड़ी का करियर रुक जाता है; मैरी ने जुड़वाँ बेटों के बाद भी वापसी करके यह धारणा तोड़ी।'),
        ('C3', 'वार्ता में मैरी के ‘किसान परिवार’ में जन्म का उल्लेख क्यों किया गया है?', 'साधारण, सीमित साधनों वाली पृष्ठभूमि दिखाकर उनकी उपलब्धि को और प्रेरक बनाने के लिए — सफलता साधनों पर नहीं, परिश्रम पर निर्भर है।'),
    ],
    '‘गाँव से शहर की ओर’ — भाग 1': [
        ('C1', 'वृत्तचित्र का यह भाग किस क्षेत्र के गाँव से शुरू होता है?', 'बुंदेलखंड', ['विदर्भ', 'मेवाड़', 'तराई']),
        ('C2', 'रामकिशन के जाने के बाद सावित्री पर कौन-कौन-सी ज़िम्मेदारियाँ आ गई हैं?', 'खेत, पशु और बच्चों की पढ़ाई — घर और खेती की सारी ज़िम्मेदारी अकेले उन पर है।'),
        ('C3', '“वह होली पर आता है, बस।” — सावित्री के इस छोटे वाक्य से उनकी किस भावना का पता चलता है?', 'अकेलेपन, शिकायत और विवशता की; पति साल में एक बार ही आता है और परिवार का भावनात्मक संबंध कमज़ोर हो रहा है।'),
    ],
    '‘गाँव से शहर की ओर’ — भाग 2: शहर की कहानी': [
        ('C1', 'नसरीन किस प्रकार की संस्था में काम करती हैं?', 'स्वयंसेवी संस्था', ['सरकारी बैंक', 'ईंट-भट्ठा कंपनी', 'निजी विद्यालय']),
        ('C2', 'शहर में रामकिशन को किन दो कठिनाइयों का सामना करना पड़ता है?', 'पानी ख़रीदना पड़ता है और कभी-कभी मालिक समय पर मज़दूरी नहीं देता; साथ ही छह लोगों के साथ एक कमरे में रहना।'),
        ('C3', 'संस्था ‘साथी’ का नाम उसके काम से कैसे मेल खाता है?', 'संस्था अकेले पड़े प्रवासी मज़दूरों की सहायक बनकर उनके काग़ज़ बनवाती और अधिकार बताती है — यानी उनका ‘साथी’ बनती है।'),
    ],
    '‘दो देश, एक दिल’ — विदेश में पढ़ने वाले विद्यार्थी की बातें': [
        ('C1', 'ज़ोया कितने साल से जर्मनी में पढ़ रही है?', 'दो साल से', ['छह महीने से', 'चार साल से', 'एक साल से']),
        ('C2', 'ज़ोया के जर्मन दोस्त उसकी बिरयानी के ‘दीवाने’ हैं — इससे उसके अनुकूलन के बारे में क्या पता चलता है?', 'वह नए समाज में घुल-मिल गई है और अपनी संस्कृति भी साझा कर रही है; अनुकूलन दोतरफ़ा सांस्कृतिक आदान-प्रदान बन गया है।'),
        ('C3', 'शीर्षक ‘दो देश, एक दिल’ ज़ोया के अनुभव को कैसे व्यक्त करता है?', 'ज़ोया भारत और जर्मनी, दोनों से भावनात्मक रूप से जुड़ी है; उसकी पहचान दोनों संस्कृतियों के मेल से बनी है।'),
    ],
    'मेट्रो सेवा में परिवर्तन': [
        ('C1', 'सेवाओं में परिवर्तन किस मेट्रो लाइन पर है?', 'नीली लाइन', ['पीली लाइन', 'लाल लाइन', 'हरी लाइन']),
        ('C2', 'यदि कोई यात्री शनिवार सुबह सात बजे द्वारका जाना चाहता है, तो घोषणा के अनुसार उसे क्या करना चाहिए?', 'उस समय मेट्रो बंद रहेगी (सेवा आठ बजे से), इसलिए वह स्टेशन के बाहर से निःशुल्क शटल बस ले सकता है या अधिक जानकारी के लिए हेल्पलाइन 155370 पर फ़ोन कर सकता है।'),
        ('C2', 'घोषणा में यात्रियों के लिए दी गई दो व्यावहारिक जानकारियाँ अपने शब्दों में लिखिए।', 'सप्ताहांत में सेवा दो घंटे देर से (आठ बजे) शुरू होगी; स्टेशनों के बाहर से हर पंद्रह मिनट पर मुफ़्त शटल बसें मिलेंगी; सोमवार से सामान्य समय; हेल्पलाइन नंबर।'),
    ],
    '‘भाषा-यात्रा’: बहुभाषी परिवारों की कहानी': [
        ('C1', 'पॉडकास्ट की प्रस्तोता का नाम क्या है?', 'सुमन', ['इक़बाल', 'आरव', 'निधि']),
        ('C2', '‘एक व्यक्ति, एक भाषा’ नियम में माता, पिता और विद्यालय की क्या-क्या भूमिका है?', 'माँ बच्चे से एक भाषा में, पिता दूसरी भाषा में बात करें, और विद्यालय तीसरी भाषा सिखाए।'),
        ('C3', 'प्रोफ़ेसर ने बच्चे के मस्तिष्क को ‘स्पंज’ क्यों कहा? इस तुलना का आशय स्पष्ट कीजिए।', 'स्पंज जैसे पानी सोख लेता है, वैसे ही बच्चे का मस्तिष्क आसपास की भाषाएँ सहजता से ग्रहण कर लेता है; इसलिए बचपन में कई भाषाएँ सीखना आसान है।'),
    ],
    'पर्वतारोही पेमा से बातचीत': [
        ('C1', 'पेमा डोलमा किस राज्य से हैं?', 'सिक्किम', ['उत्तराखंड', 'हिमाचल प्रदेश', 'अरुणाचल प्रदेश']),
        ('C2', 'पेमा ने अपनी तैयारी में शारीरिक और मानसिक, दोनों पक्षों पर कैसे काम किया?', 'शारीरिक: दो साल तक रोज़ सुबह चार बजे उठकर बीस किलो बोझ के साथ दौड़ना; मानसिक: धैर्य और मन की तैयारी को सबसे ज़रूरी मानना।'),
        ('C2', 'मास्क जमने के क्षण का वर्णन पेमा की किस भावना को दर्शाता है और यह संकट कैसे टला?', 'निराशा और भय (“सब ख़त्म हो गया”); शेरपा साथी ने गरम दस्तानों वाली उँगलियों से मास्क पिघलाया।'),
    ],
    'संध्या समाचार': [
        ('C2', 'राजस्थान में विद्यालयों का समय क्यों बदला गया और नया समय किस बात को ध्यान में रखकर तय किया गया लगता है?', 'पारा 47 डिग्री तक पहुँचने से; नया समय (7:30–11:30) दोपहर की तेज़ गर्मी से पहले विद्यालय बंद करने के लिए है ताकि बच्चे लू से बचें।'),
        ('C3', 'समाचार-बुलेटिन में समाचारों का क्रम (पर्यावरण, मौसम/गर्मी, खेल, मौसम-पूर्वानुमान) क्या दर्शाता है?', 'पहले सबसे महत्त्वपूर्ण/राष्ट्रीय समाचार, फिर जनहित की सूचना, फिर खेल और अंत में मौसम — बुलेटिन की मानक संरचना, जिससे श्रोता के लिए जानकारी व्यवस्थित रहती है।'),
    ],
    'विद्यालय-सभा में पूर्व छात्रा का संबोधन': [
        ('C2', 'शर्मा मैडम के वाक्य ने वक्ता की सोच कैसे बदली? अपने शब्दों में समझाइए।', 'उन्होंने असफलता को क्षमता की कमी नहीं, बल्कि विषय से जुड़ाव की कमी बताया; इससे वक्ता का आत्मविश्वास जागा और उन्होंने गणित से ‘दोस्ती’ करने की कोशिश की।'),
        ('C3', 'वक्ता ने भाषण की शुरुआत अपने पीछे बैठने की आदत से क्यों की?', 'श्रोताओं (विद्यार्थियों) से तुरंत आत्मीयता बनाने और दिखाने के लिए कि सफल व्यक्ति भी कभी उनकी तरह डरा हुआ था; इससे बाद का संदेश अधिक विश्वसनीय लगता है।'),
    ],
}
for _k in TH:
    for _a in TH[_k].get('audio', []) + TH[_k].get('audio2', []):
        _a['qs'] = list(_a['qs']) + EXTRA_AUDIO_QS.get(_a['title'], [])


# === FOOTER ===
def register(kit, TH, SPEC, listen=(), read=()):
    for key, (kind, spec) in SPEC.items():
        ch = int(key[2:4])
        kit.setup(key, kind, TH[ch], spec)
        # Mock Paper 2 sections may draw any subtopic of a listening/reading chapter:
        # give the others the chapter's texts as mock-only templates.
        kit.mock_only = True
        if ch in listen and kind != 'listening' and TH[ch].get('audio'):
            kit.texts(key, TH[ch], 'audio', 'p2l')
        if ch in read and kind != 'reading' and TH[ch].get('texts'):
            kit.texts(key, TH[ch], 'texts', 'p2r')
        kit.mock_only = False


register(KIT, TH, SPEC, LISTEN_CH_G11, READ_CH_G11)


def init(subject_id):
    pass


def templates(st):
    return R.build(st)
