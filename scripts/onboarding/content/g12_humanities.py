"""Design g12-humanities: grade 12 Humanities stream (History, Political Science, Geography, Economics).

Cambridge's Political Science slot is Global Perspectives & Research; IB's is Global Politics.
Economics reuses the Commerce economics bank.
"""
from dsl import G
from content.senior_hum import (HISTORY_PRE_G12, HISTORY_CUR_G12, POLSCI_PRE_G12, POLSCI_CUR_G12,
                                GEOGRAPHY_PRE_G12, GEOGRAPHY_CUR_G12)
from content.senior_com import ECONOMICS_PRE_G12, ECONOMICS_CUR_G12
from content.senior_titles import title

POLSCI_LABEL = {'cbse': 'Political Science', 'cambridge': 'Global Perspectives & Research', 'ib': 'Global Politics'}


def groups(board):
    return [
        G('history', 'History', HISTORY_PRE_G12, HISTORY_CUR_G12),
        G('political-science', POLSCI_LABEL[board], POLSCI_PRE_G12, POLSCI_CUR_G12),
        G('geography', 'Geography', GEOGRAPHY_PRE_G12, GEOGRAPHY_CUR_G12),
        G('economics', 'Economics', ECONOMICS_PRE_G12, ECONOMICS_CUR_G12),
    ]


DESIGN = {
    'designId': 'g12-humanities', 'grade': 12, 'stream': 'humanities', 'boards': ['cbse', 'cambridge', 'ib'],
    'title': title(12, 'humanities'),
    'groups': groups,
}
