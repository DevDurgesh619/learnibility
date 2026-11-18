"""Design g11-commerce: grade 11 Commerce stream.

CBSE: Accountancy, Business Studies, Economics, Applied Mathematics. Cambridge: Accounting, Business, Economics and
Mathematics (no Applied Maths at AS). IB: Business Management, Economics, Mathematics AI (no Accountancy, so 3 groups).
"""
from dsl import G
from content.senior_com import (ACCOUNTANCY_PRE_G11, ACCOUNTANCY_CUR_G11, BUSINESS_PRE_G11, BUSINESS_CUR_G11,
                                ECONOMICS_PRE_G11, ECONOMICS_CUR_G11, APPLIED_PRE_G12, APPLIED_CUR_G12, APPLIED_CUR_G11)
from content.senior_sci import MATHS_PRE_G11, MATHS_CUR_G11
from content.senior_titles import title


def groups(board):
    acc = G('accountancy', 'Accountancy', ACCOUNTANCY_PRE_G11, ACCOUNTANCY_CUR_G11)
    bus = G('business', 'Business Studies', BUSINESS_PRE_G11, BUSINESS_CUR_G11)
    eco = G('economics', 'Economics', ECONOMICS_PRE_G11, ECONOMICS_CUR_G11)
    if board == 'cambridge':
        return [acc, bus, eco, G('maths', 'Mathematics', MATHS_PRE_G11, MATHS_CUR_G11)]
    applied = G('applied-maths', 'Applied Mathematics', MATHS_PRE_G11, APPLIED_CUR_G11)
    if board == 'ib':
        return [bus, eco, applied]
    return [acc, bus, eco, applied]


DESIGN = {
    'designId': 'g11-commerce', 'grade': 11, 'stream': 'commerce', 'boards': ['cbse', 'cambridge', 'ib'],
    'title': title(11, 'commerce'),
    'groups': groups,
}
