"""Design g12-science: grade 12 Science stream (Physics, Chemistry, Mathematics, Biology) for all three boards."""
from dsl import G
from content.senior_sci import (PHYSICS_PRE_G12, PHYSICS_CUR_G12, CHEMISTRY_PRE_G12, CHEMISTRY_CUR_G12,
                                MATHS_PRE_G12, MATHS_CUR_G12, BIOLOGY_PRE_G12, BIOLOGY_CUR_G12)
from content.senior_titles import title


def groups(board):
    return [
        G('physics', 'Physics', PHYSICS_PRE_G12, PHYSICS_CUR_G12),
        G('chemistry', 'Chemistry', CHEMISTRY_PRE_G12, CHEMISTRY_CUR_G12),
        G('maths', 'Mathematics', MATHS_PRE_G12, MATHS_CUR_G12),
        G('biology', 'Biology', BIOLOGY_PRE_G12, BIOLOGY_CUR_G12),
    ]


DESIGN = {
    'designId': 'g12-science', 'grade': 12, 'stream': 'science', 'boards': ['cbse', 'cambridge', 'ib'],
    'title': title(12, 'science'),
    'groups': groups,
}
