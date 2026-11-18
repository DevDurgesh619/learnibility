"""Design g12-commerce: grade 12 Commerce stream.

CBSE: Accountancy, Business Studies, Economics, Applied Mathematics. Cambridge: Accounting, Business, Economics and
Probability & Statistics. IB: Business Management, Economics, Mathematics AI (no Accountancy, so 3 groups).
"""
from dsl import G
from content.senior_com import (ACCOUNTANCY_PRE_G12, ACCOUNTANCY_CUR_G12, BUSINESS_PRE_G12, BUSINESS_CUR_G12,
                                ECONOMICS_PRE_G12, ECONOMICS_CUR_G12, APPLIED_PRE_G12, APPLIED_CUR_G12, APPLIED_CUR_G11)

from content.senior_titles import title

def groups(board):
    acc = G('accountancy', 'Accountancy', ACCOUNTANCY_PRE_G12, ACCOUNTANCY_CUR_G12)
    bus = G('business', 'Business Studies', BUSINESS_PRE_G12, BUSINESS_CUR_G12)
    eco = G('economics', 'Economics', ECONOMICS_PRE_G12, ECONOMICS_CUR_G12)
    if board == 'cambridge':
        return [acc, bus, eco, G('applied-maths', 'Probability and Statistics', APPLIED_PRE_G12, APPLIED_CUR_G12)]
    applied = G('applied-maths', 'Applied Mathematics', APPLIED_PRE_G12, APPLIED_CUR_G12)
    if board == 'ib':
        return [bus, eco, applied]
    return [acc, bus, eco, applied]

DESIGN = {
    'designId': 'g12-commerce', 'grade': 12, 'stream': 'commerce', 'boards': ['cbse', 'cambridge', 'ib'],
    'title': title(12, 'commerce'),
    'groups': groups,
}
