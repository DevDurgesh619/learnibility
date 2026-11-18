"""Board-specific titles for the senior (grade 11-12) forms."""

YEAR = {
    (11, 'cbse'): 'CBSE Class 11', (12, 'cbse'): 'CBSE Class 12',
    (11, 'cambridge'): 'Cambridge AS Level', (12, 'cambridge'): 'Cambridge A Level',
    (11, 'ib'): 'IB Diploma Year 1', (12, 'ib'): 'IB Diploma Year 2',
}
STREAM = {'science': 'Science', 'commerce': 'Commerce', 'humanities': 'Humanities'}


def title(grade, stream):
    return lambda board: f'{YEAR[(grade, board)]} {STREAM[stream]} onboarding test'
