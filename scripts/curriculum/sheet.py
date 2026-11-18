"""Reads the assessment cost sheet (reference/assessment-cost-gr8-12.xlsx)
and returns one record per subject row, with Learnibility subject IDs, names and the
canonical chapter list where the sheet names every chapter.

Used by build.py (writes data/curriculum/*) and by the authoring briefs.
"""
import re
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[2]
COST_SHEET = ROOT / "reference" / "assessment-cost-gr8-12.xlsx"

TABS = {
    "CBSE 8th  to 10th": "cbse", "Cbse 11th -12th ": "cbse",
    "IGCSE 8th-10th ": "cambridge", "IGCSE 11th and 12th ": "cambridge",
    "IB - 8th to 10th ": "ib", "IB 11th and 12th ": "ib",
}

# sheet subject label (lowercased, trimmed) -> slug, per board. Grades 8-10 and 11-12 share labels.
SLUG = {
    "maths": "maths", "science": "science", "social science": "social-science", "english": "english",
    "hindi": "hindi", "hindi (course a)": "hindi", "hindi (course b)": "hindi-b",
    "maths – advanced level (optional)": "maths-advanced", "science – advanced level (optional)": "science-advanced",
    "physics": "physics", "chemistry": "chemistry", "biology": "biology", "bio": "biology",
    "social science – history": "history", "social science – geography": "geography",
    "eco": "economics", "economics": "economics", "comp science": "computer-science", "psychology": "psychology",
    "enviormental science": "environmental", "accounts": "accountancy", "bussiness studies": "business",
    "ip and information practice": "informatics", "maths - stats": "applied-maths", "legal studies": "legal-studies",
    "enterprenuership": "entrepreneurship", "management behavior studeos": "management-behaviour",
    "history": "history", "pol science": "political-science", "geography": "geography", "sociology": "sociology",
}
# board-specific slug overrides where the board's real course is a different subject
SLUG_OVERRIDE = {
    ("cambridge", "ip and information practice"): "information-technology",
    ("cambridge", "legal studies"): "law",
    ("cambridge", "pol science"): "global-perspectives",
    ("cambridge", "maths - stats"): "statistics",
    ("ib", "ip and information practice"): "digital-society",
    ("ib", "maths - stats"): "maths-ai",
    ("ib", "pol science"): "global-politics",
    ("ib", "sociology"): "anthropology",
}

NAMES = {  # (board or '*', slug) -> display name
    ("*", "maths"): "Mathematics", ("*", "science"): "Science", ("*", "social-science"): "Social Science",
    ("*", "english"): "English", ("*", "hindi"): "Hindi", ("*", "physics"): "Physics", ("*", "chemistry"): "Chemistry",
    ("*", "biology"): "Biology", ("*", "history"): "History", ("*", "geography"): "Geography",
    ("*", "economics"): "Economics", ("*", "computer-science"): "Computer Science", ("*", "psychology"): "Psychology",
    ("*", "environmental"): "Environmental Management", ("*", "accountancy"): "Accountancy",
    ("*", "business"): "Business Studies", ("*", "informatics"): "Informatics Practices",
    ("*", "applied-maths"): "Applied Mathematics", ("*", "legal-studies"): "Legal Studies",
    ("*", "entrepreneurship"): "Entrepreneurship", ("*", "political-science"): "Political Science",
    ("*", "sociology"): "Sociology", ("*", "information-technology"): "Information Technology", ("*", "law"): "Law",
    ("*", "global-perspectives"): "Global Perspectives & Research", ("*", "statistics"): "Probability & Statistics 2",
    ("*", "digital-society"): "Digital Society", ("*", "maths-ai"): "Mathematics: Applications & Interpretation",
    ("*", "global-politics"): "Global Politics", ("*", "anthropology"): "Social & Cultural Anthropology",
    ("*", "hindi-b"): "Hindi (Course B)", ("*", "maths-advanced"): "Mathematics at Advanced Level",
    ("*", "science-advanced"): "Science at Advanced Level", ("*", "management-behaviour"): "Management & Behaviour",
    ("cambridge", "social-science"): "Humanities (People, Past, Places)",
    ("ib", "social-science"): "Individuals & Societies", ("ib", "english"): "Language & Literature (English)",
    ("ib", "hindi"): "Language Acquisition (Hindi)", ("ib", "maths"): "Mathematics",
    ("ib", "environmental"): "Environmental Systems & Societies", ("ib", "business"): "Business Management",
    ("cambridge", "english"): "English", ("ib", "science"): "Sciences",
    ("cambridge", "business"): "Business", ("cambridge", "accountancy"): "Accounting",
}

# The sheet lists chapter names for most CBSE and some Cambridge subjects. Where its list is a
# compressed summary, these overrides give the full official list (same count as the sheet).
CHAPTER_OVERRIDES = {
    "cbse-g10-english": [
        "A Letter to God", "Dust of Snow", "Fire and Ice", "Nelson Mandela: Long Walk to Freedom", "A Tiger in the Zoo",
        "Two Stories About Flying", "How to Tell Wild Animals", "The Ball Poem", "From the Diary of Anne Frank",
        "Glimpses of India", "Amanda!", "Mijbil the Otter", "The Trees", "Madam Rides the Bus", "Fog",
        "The Sermon at Benares", "The Tale of Custard the Dragon", "The Proposal", "For Anne Gregory",
        "A Triumph of Surgery", "The Thief's Story", "The Midnight Visitor", "A Question of Trust",
        "Footprints Without Feet", "The Making of a Scientist", "The Necklace", "Bholi", "The Book that Saved the Earth"],
    "cbse-g11-english": [
        "The Portrait of a Lady", "A Photograph", "We're Not Afraid to Die... if We Can All Be Together",
        "Discovering Tut: The Saga Continues", "The Laburnum Top", "The Voice of the Rain", "Childhood", "The Adventure",
        "Silk Road", "Father to Son", "The Summer of the Beautiful White Horse", "The Address", "Mother's Day", "Birth",
        "The Tale of Melon City"],
    "cbse-g12-english": [
        "The Last Lesson", "Lost Spring", "Deep Water", "The Rattrap", "Indigo", "Poets and Pancakes", "The Interview",
        "Going Places", "My Mother at Sixty-six", "Keeping Quiet", "A Thing of Beauty", "A Roadside Stand",
        "Aunt Jennifer's Tigers", "The Third Level", "The Tiger King", "Journey to the End of the Earth", "The Enemy",
        "On the Face of It", "Memories of Childhood"],
    "cbse-g11-biology": [
        "The Living World", "Biological Classification", "Plant Kingdom", "Animal Kingdom", "Morphology of Flowering Plants",
        "Anatomy of Flowering Plants", "Structural Organisation in Animals", "Cell: The Unit of Life", "Biomolecules",
        "Cell Cycle and Cell Division", "Photosynthesis in Higher Plants", "Respiration in Plants",
        "Plant Growth and Development", "Breathing and Exchange of Gases", "Body Fluids and Circulation",
        "Excretory Products and their Elimination", "Locomotion and Movement", "Neural Control and Coordination",
        "Chemical Coordination and Integration"],
    "cbse-g11-accountancy": [
        "Introduction to Accounting", "Theory Base of Accounting", "Recording of Transactions I",
        "Recording of Transactions II", "Bank Reconciliation Statement", "Trial Balance and Rectification of Errors",
        "Depreciation, Provisions and Reserves", "Financial Statements I", "Financial Statements II"],
    "cbse-g11-political-science": [
        "Constitution: Why and How?", "Rights in the Indian Constitution", "Election and Representation", "Executive",
        "Legislature", "Judiciary", "Federalism", "Local Governments", "Constitution as a Living Document",
        "The Philosophy of the Constitution", "Political Theory: An Introduction", "Freedom", "Equality",
        "Social Justice", "Rights", "Citizenship", "Nationalism", "Secularism"],
    "cbse-g12-geography": [
        "Human Geography: Nature and Scope", "The World Population", "Human Development", "Primary Activities",
        "Secondary Activities", "Tertiary and Quaternary Activities", "Transport and Communication", "International Trade",
        "Population: Distribution, Density, Growth and Composition", "Human Settlements", "Land Resources and Agriculture",
        "Water Resources", "Mineral and Energy Resources", "Planning and Sustainable Development in Indian Context",
        "Transport and Communication (India)", "International Trade (India)",
        "Geographical Perspective on Selected Issues and Problems", "Data: Its Source and Compilation",
        "Data Processing", "Graphical Representation of Data", "Spatial Information Technology"],
    "cbse-g11-physics": [
        "Units and Measurements", "Motion in a Straight Line", "Motion in a Plane", "Laws of Motion",
        "Work, Energy and Power", "System of Particles and Rotational Motion", "Gravitation",
        "Mechanical Properties of Solids", "Mechanical Properties of Fluids", "Thermal Properties of Matter",
        "Thermodynamics", "Kinetic Theory", "Oscillations", "Waves"],
    "cbse-g11-chemistry": [
        "Some Basic Concepts of Chemistry", "Structure of Atom", "Classification of Elements and Periodicity in Properties",
        "Chemical Bonding and Molecular Structure", "Thermodynamics", "Equilibrium", "Redox Reactions",
        "Organic Chemistry: Some Basic Principles and Techniques", "Hydrocarbons"],
    "cbse-g12-computer-science": [
        "Python Revision and Functions", "Exception Handling", "File Handling (Text, Binary, CSV)", "Data Structures: Stack",
        "Computer Networks", "Data Communication", "Database Concepts", "Structured Query Language (SQL)",
        "Interface of Python with MySQL"],
}

def _num(v):
    return 0 if v is None else v

def _parse_names(s):
    if not s:
        return []
    pfx = (r"^(?:(?:Part I+|Part B|History|Geography|Pol Sci|Economics|First Flight prose|Footprints|Statistics|Micro|Macro|"
           r"IED|India|Practical|Flamingo|Vistas|गद्य|काव्य|क्षितिज|कृतिका|आरोह गद्य|आरोह|वितान)\s*:\s*|U\d\s+|Ch \d+–\d+:\s*)")
    out = []
    for seg in re.split(r"\s*[;·]\s*", s):
        seg = seg.strip()
        if seg.startswith("Grammar:"):
            continue
        seg = re.sub(pfx, "", seg).strip()
        seg = re.sub(r"^\d+\s+(?=[A-Z])", "", seg)
        if seg:
            out.append(seg)
    return out

def subject_id(board, grade, slug):
    return f"{board}-g{grade}-{slug}"

def read_rows(path=COST_SHEET):
    wb = openpyxl.load_workbook(path, data_only=True)
    rows = []
    for tab, board in TABS.items():
        ws = wb[tab]
        stream = "none"
        for i, r in enumerate(ws.iter_rows(values_only=True), 1):
            if i == 1:
                continue
            if r[0] is None and r[2] and not r[3]:
                stream = r[2].strip().lower()
                continue
            if not (r[1] and r[3]):
                continue
            grade = int(re.match(r"(\d+)", str(r[1])).group(1))
            label = r[3].strip().lower()
            slug = SLUG_OVERRIDE.get((board, label), SLUG[label])
            sid = subject_id(board, grade, slug)
            names = CHAPTER_OVERRIDES.get(sid) or _parse_names(r[6])
            chapters = int(_num(r[5]))
            rows.append(dict(
                id=sid, board=board, grade=grade, stream=(stream if grade >= 11 else "none"), slug=slug,
                name=NAMES.get((board, slug)) or NAMES[("*", slug)], label=r[3].strip(), tab=tab.strip(), row=i,
                course=(r[4] or "").strip(), chapterCount=chapters,
                chapterNames=names if len(names) == chapters else None, chapterHint=r[6],
                perChapter=_num(r[7]), bankQuestions=_num(r[8]), practiceTests=_num(r[9]),
                questionsPerTest=_num(r[10]), practiceQuestions=_num(r[11]), mocks=_num(r[12]),
                questionsPerMock=_num(r[13]), mockQuestions=_num(r[14]), questionTarget=int(_num(r[15])),
                counted=(r[16] == "Y"), examPattern=(r[19] or "").strip(), questionFormat=(r[20] or "").strip(),
                officialSource=(r[21] or "").strip(),
            ))
    return rows

BOARD_TOTALS = {"cbse": 63582, "cambridge": 62540, "ib": 53893}
GRAND_TOTAL = 180015
