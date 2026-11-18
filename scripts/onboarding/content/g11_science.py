"""Design g11-science: grade 11 Science stream (Physics, Chemistry, Mathematics, Biology) for all three boards."""
from dsl import G
from content.senior_sci import (PHYSICS_PRE_G11, PHYSICS_CUR_G11, CHEMISTRY_PRE_G11, CHEMISTRY_CUR_G11,
                                MATHS_PRE_G11, MATHS_CUR_G11, BIOLOGY_PRE_G11, BIOLOGY_CUR_G11)
from content.senior_titles import title


def groups(board):
    return [
        G('physics', 'Physics', PHYSICS_PRE_G11, PHYSICS_CUR_G11),
        G('chemistry', 'Chemistry', CHEMISTRY_PRE_G11, CHEMISTRY_CUR_G11),
        G('maths', 'Mathematics', MATHS_PRE_G11, MATHS_CUR_G11),
        G('biology', 'Biology', BIOLOGY_PRE_G11, BIOLOGY_CUR_G11),
    ]


DESIGN = {
    'designId': 'g11-science', 'grade': 11, 'stream': 'science', 'boards': ['cbse', 'cambridge', 'ib'],
    'title': title(11, 'science'),
    'groups': groups,
}
