"""Parent form: 16 short items (family context, budgets, abroad plans, consent), all M2 parent-declared.

Money bands are in rupees (integer bounds in each option's `sets`). Financial and family items are T2:
role-restricted, not shown to the student verbatim. p30 guardian consent is required (DPDP s.9(1)).
"""

def opt(*labels):
    return [{'label': l, 'value': v} for l, v in labels]


def band(label, value, lo, hi):
    return {'label': label, 'value': value, 'sets': {'minInr': lo, 'maxInr': hi}}


def P(prompt, param, rtype, options=None, **kw):
    it = {'part': 'P', 'respondent': 'parent', 'prompt': prompt, 'responseType': rtype, 'paramId': param,
          'optional': False}
    if options is not None:
        it['options'] = options
    it.update(kw)
    return it


CAREERS = opt(('Engineering and technology', 'engineering'), ('Medicine and health', 'medicine'),
              ('Business, finance and commerce', 'business'), ('Law, government and public policy', 'law'),
              ('Design, media and the arts', 'design'), ('Science and research', 'research'),
              ('Teaching, psychology and social work', 'social'), ("Whatever my child chooses", 'child_choice'))


def items_for(board, grade, stream):
    items = [
        P('Who does your child live with?', 'p154', 'single',
          opt(('Both parents', 'nuclear'), ('Parents and grandparents or other relatives', 'joint'),
              ('One parent', 'single_parent'), ('Another guardian', 'guardian'))),
        P("What is the highest education level in your child's home?", 'p155', 'single',
          opt(('School', 'school'), ("Bachelor's degree", 'graduate'), ("Master's degree", 'postgraduate'),
              ('Professional or doctoral degree (CA, MBBS, PhD, LLB...)', 'professional'))),
        P("Which best describes the main earner's work?", 'p156', 'single',
          opt(('Salaried, private sector', 'private'), ('Salaried, government or PSU', 'government'),
              ('Own business', 'business'), ('Self-employed professional', 'professional'),
              ('Agriculture', 'agriculture'), ('Other', 'other'))),
        P('Which languages are spoken at home?', 'p157', 'multi',
          opt(('English', 'en'), ('Hindi', 'hi'), ('Another Indian language', 'regional'), ('Another language', 'other'))),
        P("How involved are you in your child's daily study?", 'p159', 'single',
          opt(('I check in every day', 'daily'), ('A few times a week', 'weekly'), ('Mainly around exams', 'exams'),
              ('Rarely, my child manages it', 'rarely'))),
        P('Does your child attend tuition or coaching?', 'p21', 'single',
          opt(('No', 'none'), ('One subject', 'one_subject'), ('Two or more subjects', 'multi_subject'),
              ('A coaching institute (e.g. for JEE, NEET or boards)', 'institute'))),
        P('Annual household income (optional, helps us suggest scholarships)', 'p176', 'single',
          [band('Under ₹5 lakh', 'lt_5l', 0, 500000), band('₹5 to 10 lakh', '5_10l', 500000, 1000000),
           band('₹10 to 25 lakh', '10_25l', 1000000, 2500000), band('₹25 to 50 lakh', '25_50l', 2500000, 5000000),
           band('Over ₹50 lakh', 'gt_50l', 5000000, None)], optional=True),
        P('How much can you spend on extra learning each year (tuition, courses, tests)?', 'p178', 'single',
          [band('Under ₹50,000', 'lt_50k', 0, 50000), band('₹50,000 to 1.5 lakh', '50k_150k', 50000, 150000),
           band('₹1.5 to 3 lakh', '150k_300k', 150000, 300000), band('₹3 to 6 lakh', '300k_600k', 300000, 600000),
           band('Over ₹6 lakh', 'gt_600k', 600000, None)]),
        P('What total budget can you plan for an undergraduate degree in India?', 'p180', 'single',
          [band('Under ₹5 lakh', 'lt_5l', 0, 500000), band('₹5 to 15 lakh', '5_15l', 500000, 1500000),
           band('₹15 to 30 lakh', '15_30l', 1500000, 3000000), band('Over ₹30 lakh', 'gt_30l', 3000000, None)]),
        P('If your child studies abroad, what total budget could you plan?', 'p181', 'single',
          [band('Not considering study abroad', 'none', 0, 0), band('Under ₹25 lakh', 'lt_25l', 0, 2500000),
           band('₹25 to 50 lakh', '25_50l', 2500000, 5000000), band('₹50 lakh to 1 crore', '50l_1cr', 5000000, 10000000),
           band('Over ₹1 crore', 'gt_1cr', 10000000, None)], alsoInforms=['p192']),
        P('Would you consider an education loan?', 'p182', 'single',
          opt(('Yes', 'yes'), ('Maybe, depending on the course', 'maybe'), ('No', 'no'))),
        P('Which career direction would you like for your child?', 'p202', 'single', CAREERS, alsoInforms=['p203']),
        P("How supportive is your family of your child studying abroad?", 'p234', 'scale',
          [{'label': '1 Not supportive', 'value': 1}, {'label': '2', 'value': 2}, {'label': '3', 'value': 3},
           {'label': '4', 'value': 4}, {'label': '5 Fully supportive', 'value': 5}]),
        P('What device and internet does your child use for study?', 'p193', 'single',
          opt(('Own laptop or tablet with reliable internet', 'own_device'), ('A shared family computer', 'shared'),
              ('Mainly a phone', 'phone_only'), ('Internet is often unreliable', 'unreliable'))),
        P("I consent to Learnibility processing my child's data to personalise their learning, as described in the privacy notice.",
          'p30', 'consent', opt(('I agree', 'granted'), ('I do not agree', 'refused')),
          helpText='Required for a child under 18 (DPDP Act 2023, s.9(1)). You can withdraw consent at any time in Settings.'),
        P("I allow my child's selected work to be shown to teachers, tutors and counsellors on the platform.", 'p277', 'consent',
          opt(('Yes', 'granted'), ('Not now', 'refused')), optional=True,
          helpText='Optional. Nothing is shared outside the platform without asking you again.'),
    ]
    return items
