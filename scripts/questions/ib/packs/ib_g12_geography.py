"""IB DP Geography SL/HL (guide for first assessment 2019) - ib-g12-geography, year 2.

Year 2 covers Option D Geophysical hazards, the HL extension (Power, places and networks; Human development
and diversity; Global risks and resilience) and the internal assessment write-up with Paper 3 synthesis skills.

Item styles follow ib_g11_geography.py (whose shared machinery - parametric gens, essay / infographic / data
templates and markbands - is imported here): C1 define / state, C2 explain / distinguish / misconception,
C3 named, located case studies and computed data items (moment-magnitude energy ratios, S-P wave distances,
tsunami speed, hazard risk equation, VEI, landslide factor of safety, HDI, MPI, Gini from quintile shares,
ODA as % of GNI, debt ratios, KOF-style indices, freight emissions, Greenberg language diversity, Spearman's
rank), C4 Paper 1 extended response [10], Paper 3 HL (a) [12] "Examine" and (b) [16] "To what extent"
essays with markband keys. Figures for real events are rounded published values (USGS, UNDRR, UNDP, OECD,
World Bank, UNCTAD); parametric data sets are labelled as samples or illustrative data.
"""
from __future__ import annotations

import math
import re

from _common import F, Registry, T, mcq, name

import ib_g11_geography as G
from ib_g11_geography import GENS, MB10, mk, lc, pc

CONFIG = {'minutesPerMark': 1.8, 'mcqMinutes': 1.5}

# One mock = Paper 1 Option D Geophysical hazards (structured question [10] + extended response [10]),
# Paper 3 HL (one two-part question: (a) [12] + (b) [16]), HL-extension short-answer preparation [13] and
# internal-assessment skills (data analysis and evaluation) [22]. 18 items, 83 marks.
OPT_D, HLX, IA = [1, 2, 3, 4], list(range(5, 13)), [13]
MOCK = [
    dict(section='Paper 1 Option D Geophysical hazards - structured question (a): define / state', count=1, c=['C1'], d=[2], type='short', marks=2, chapters=OPT_D),
    dict(section='Paper 1 Option D - structured question (b): data / resource interpretation', count=1, c=['C3'], d=[2, 3], type='numerical', marks=2, style='data', chapters=OPT_D),
    dict(section='Paper 1 Option D - structured question (c): explain', count=1, c=['C2'], d=[3], type='explain', marks=3, chapters=OPT_D),
    dict(section='Paper 1 Option D - structured question (d): explain with a named example', count=1, c=['C3'], d=[3], type='short', marks=3, chapters=OPT_D),
    dict(section='Paper 1 Option D - extended response', count=1, c=['C4'], d=[4], type='long', marks=10, style='p1ext', chapters=OPT_D),
    dict(section='HL extension review - define / state (Paper 3 preparation)', count=2, c=['C1'], d=[2], type='short', marks=2, chapters=HLX),
    dict(section='HL extension review - explain (Paper 3 preparation)', count=2, c=['C2'], d=[3], type='explain', marks=3, chapters=HLX),
    dict(section='HL extension review - data / resource analysis', count=1, c=['C3'], d=[3], type='numerical', marks=3, style='data', chapters=HLX),
    dict(section='Paper 3 (HL) - question part (a)', count=1, c=['C4'], d=[4], type='long', marks=12, style='p3a', chapters=HLX),
    dict(section='Paper 3 (HL) - question part (b)', count=1, c=['C4'], d=[5], type='long', marks=16, style='p3b', chapters=HLX),
    dict(section='Internal assessment skills - data analysis', count=4, c=['C3'], d=[3, 4], type='numerical', marks=4, style='data', chapters=IA),
    dict(section='Internal assessment skills - conclusion and evaluation', count=2, c=['C2'], d=[3], type='explain', marks=3, chapters=IA),
]

R = Registry()
USE: dict = {}
RES: dict = {}


def init(subject_id):
    pass


def S(key, gens=(), res=(), **kw):
    def sent(x):
        x = x.strip()
        x = x[0].upper() + x[1:]
        return x if x[-1] in '.!?)' else x + '.'
    if 'cases' in kw:
        kw['cases'] = [(c, sent(w), concept, sent(h)) for c, w, concept, h in kw['cases']]
    R.facts(key, F(**kw))
    USE[key] = list(gens)
    RES[key] = list(res)


def templates(st):
    key = G._key(st)
    f = R.f.get(key)
    out = [t for t in R.build(st, {'eval_marks': 10, 'essay_marks': 15, 'markband': G.MB15})
           if t.name not in ('evaluate', 'source', 'extended')]
    for g in USE.get(key, []):
        c, d, fn, ty, sty = GENS[g]
        out.append(T(c, d, fn, ty, sty, g))
    if f:
        ch = int(key[2:4])
        hl = 5 <= ch <= 12 or key == 'ch13-st3'      # Paper 3 essays only for HL-extension content
        out += [t for t in G.geo_templates(f, RES.get(key, []), hl) if t.name != 'essay15']
    return out


def gen(nm, c='C3', d=(1, 5), type='numerical', style='data'):
    def deco(fn):
        GENS[nm] = (c, d, fn, type, style)
        return fn
    return deco


# extra themes for the shared percentage-change generator
G.PCT_CTX['hazard'] = [
    ('number of people living within 10 km of {p}', 'people', 20000, 900000, ['Mount Merapi, Indonesia', 'Vesuvius, Italy', 'Popocatépetl, Mexico', 'Mount Rainier, USA'], (1.02, 1.6)),
    ('annual insured losses from earthquakes recorded by {p}', 'US$ million', 50, 9000, ['a reinsurer in Zurich', 'a Japanese insurer', 'a New Zealand public insurer']),
    ('population of {p}', 'people', 50000, 4000000, ['a city on the North Anatolian Fault', 'a district of Kathmandu', 'a coastal town in Sumatra', 'a suburb of Lima'], (1.05, 2.0))]
G.PCT_CTX['global'] = [
    ('inward FDI stock of {p}', 'US$ billion', 5, 400, ['a South-East Asian manufacturing economy', 'an East African country', 'a Central European EU member', 'a Latin American middle-income country'], (1.2, 2.2)),
    ('merchandise exports of {p}', 'US$ billion', 3, 400, ['a South Asian garment-exporting country', 'a South-East Asian electronics exporter', 'an East African country', 'a copper-exporting South American country'], (0.8, 2.2)),
    ('number of international tourist arrivals in {p}', 'million', 1, 40, ['a South-East Asian country', 'a Central American country', 'a North African country', 'a Mediterranean EU member'], (0.6, 2.0)),
    ('internet users in {p}', 'million', 2, 150, ['a West African country', 'a South-East Asian archipelago state', 'an East African country', 'a South Asian country'], (1.4, 2.2))]
G.pct_theme('pct_hazard', ['hazard'])
G.pct_theme('pct_global', ['global'])
G.SP_CTX['hazard'] = [
    ('GDP per capita (US$ thousand, PPP)', 'deaths per million people from earthquakes (1990-2020)', -1, 'a sample of seismically active countries compiled from {city}', ['EM-DAT data', 'USGS and World Bank data'], (2, 60, 1), (1, 900, 0)),
    ('distance from the epicentre (km)', 'percentage of buildings damaged', -1, 'survey points after an earthquake near {city}', ['Kathmandu', 'Christchurch', 'Kahramanmaraş', 'Port-au-Prince'], (2, 80, 0), (3, 85, 0)),
    ('slope angle (°)', 'number of landslide scars per km²', 1, 'sample areas of hillslope in {city}', ['Hong Kong', 'the Nepal Himalaya', 'Rio de Janeiro', 'the Philippines'], (5, 45, 0), (0, 40, 0)),
    ('distance from the volcano (km)', 'thickness of ash deposit (mm)', -1, 'sampling sites downwind of {city}', ['Eyjafjallajökull', 'Mount Pinatubo', 'Mount Merapi', 'Mount St Helens'], (2, 60, 0), (1, 400, 0)),
]
G.SP_CTX['global'] = [
    ('KOF globalisation index', 'GDP per capita (US$ thousand, PPP)', 1, 'a sample of countries from {city}', ['the KOF Swiss Economic Institute', 'World Bank data'], (40, 90, 1), (2, 80, 1)),
    ('HDI', 'Gender Inequality Index', -1, 'a sample of countries from {city}', ['the UNDP Human Development Report', 'UN data'], (0.40, 0.96, 2), (0.02, 0.65, 2)),
    ('internet users (% of population)', 'KOF social globalisation score', 1, 'a sample of countries from {city}', ['ITU and KOF data', 'World Bank data'], (10, 99, 0), (30, 92, 0)),
    ('distance from the world\'s main ports (thousand km)', 'trade as % of GDP', -1, 'a sample of landlocked and coastal countries in {city}', ['Africa', 'Asia', 'Latin America'], (0.5, 12, 1), (20, 150, 0)),
]
for _nm, _th in (('spearman_hazard', ['hazard']), ('spearman_global', ['global', 'dev'])):
    GENS[_nm] = ('C3', (2, 5), G.spearman_fn(_th), 'numerical', 'data')

# culture / development contexts for the shared chi-squared and descriptive-statistics generators
G.CHI_CTX['culture'] = [
    ('the language used on {tot} shop signs recorded along a main street in {p}', ['local language only', 'English only', 'bilingual'], ['Bangkok', 'Hanoi', 'Kuala Lumpur', 'Barcelona']),
    ('the type of {tot} food outlets recorded in a central district of {p}', ['local cuisine', 'US fast-food chain', 'other Asian', 'European'], ['Seoul', 'Nairobi', 'Lima', 'Jakarta']),
    ('the identity chosen by {tot} second-generation migrants surveyed in {p}', ['host nationality only', 'heritage nationality only', 'dual (hyphenated) identity'], ['London', 'Toronto', 'Berlin', 'Sydney']),
    ('the music that {tot} secondary students surveyed in {p} stream most', ['local artists', 'US/UK artists', 'K-pop', 'Latin artists'], ['Manila', 'Mexico City', 'Istanbul', 'Johannesburg'])]
G.CHI_CTX['global'] = [
    ('the views of {tot} residents interviewed about a new foreign-owned factory in {p}', ['support', 'neutral', 'oppose'], ['Bac Ninh, Vietnam', 'Chennai', 'Monterrey', 'Tangier']),
    ('the country of origin of {tot} fruit and vegetable products sampled in a supermarket in {p}', ['domestic', 'same continent', 'other continent'], ['Amsterdam', 'Singapore', 'Dubai', 'Toronto']),
    ('the reasons given by {tot} shoppers in {p} for choosing a local market over a supermarket', ['price', 'freshness', 'supporting local producers', 'convenience'], ['Lyon', 'Oaxaca', 'Hanoi', 'Bristol'])]
GENS['chi_culture'] = ('C3', (2, 5), G.chi_fn(['culture']), 'numerical', 'data')
GENS['chi_global'] = ('C3', (2, 5), G.chi_fn(['global']), 'numerical', 'data')
G.STAT_CTX['dev'] = [
    ('daily wages (US$) reported by garment workers surveyed in {r}', ['Dhaka', 'Phnom Penh', 'Yangon', 'Addis Ababa'], 2, 12),
    ('monthly remittances received (US$) by households surveyed in {r}', ['rural Nepal', 'the Khatlon region of Tajikistan', 'Kerala', 'Central Luzon'], 40, 600),
    ('daily times (minutes) spent collecting water by households surveyed in {r}', ['rural Niger', 'northern Ghana', 'Tigray', 'rural Malawi'], 10, 180),
    ('years of schooling completed by adults surveyed in {r}', ['a village in Bihar', 'a district of rural Chad', 'a township near Durban', 'a suburb of Quito'], 0, 16)]
GENS['stats_dev'] = ('C3', (1, 5), G.stats_fn(['dev']), 'numerical', 'data')

# ---------------------------------------------------------------------------------------------
# parametric hazard and development generators (answers computed)
# ---------------------------------------------------------------------------------------------
QUAKES = [('the 2011 Tōhoku earthquake, Japan', 9.1), ('the 2004 Sumatra-Andaman earthquake', 9.1), ('the 2010 Maule earthquake, Chile', 8.8),
          ('the 2008 Sichuan earthquake, China', 7.9), ('the 2015 Gorkha earthquake, Nepal', 7.8), ('the February 2023 Kahramanmaraş earthquake, Türkiye', 7.8),
          ('the 2010 Haiti earthquake', 7.0), ('the 1995 Kobe earthquake, Japan', 6.9), ('the 2023 Al Haouz earthquake, Morocco', 6.8),
          ('the 2009 L\'Aquila earthquake, Italy', 6.3), ('the February 2011 Christchurch earthquake, New Zealand', 6.2), ('the 2025 Mandalay earthquake, Myanmar', 7.7)]


@gen('magnitude', d=(1, 4))
def g_mag(rng, slot):
    (a, ma), (b, mb) = rng.sample(QUAKES, 2)
    if ma == mb:
        return None
    if ma < mb:
        (a, ma), (b, mb) = (b, mb), (a, ma)
    dm = round(ma - mb, 1)
    amp = 10 ** dm
    en = 10 ** (1.5 * dm)
    stem = rng.choice([f'{a[0].upper() + a[1:]} had a moment magnitude of {ma} and {b} had a magnitude of {mb}.',
                       f'USGS data: {a} - Mw {ma}; {b} - Mw {mb}.'])
    if slot.d <= 2:
        return dict(stem=stem + ' How many times larger was the ground-motion amplitude of the first earthquake?', answer=f'10^{dm} ≈ {amp:,.0f} times',
                    markingKey=f'M1 each whole unit = ×10 amplitude; A1 10^{dm} ≈ {amp:,.0f}.', marks=mk(slot, 2))
    stem += ' Calculate how many times more energy was released by the first earthquake (energy increases by a factor of about 10^1.5 ≈ 31.6 per unit of magnitude).'
    if slot.d >= 4:
        stem += ' Explain why the larger earthquake did not necessarily cause more deaths.'
    return dict(stem=stem, answer=f'Energy ratio = 10^(1.5 × {dm}) ≈ {en:,.0f} times' + ('; deaths depend on vulnerability - building quality, population density, preparedness, depth and distance from cities, time of day.' if slot.d >= 4 else ''),
                markingKey=f'M1 10^(1.5ΔM) with ΔM = {dm}; A1 ≈ {en:,.0f}.' + (' R1 R1 vulnerability factors with an example.' if slot.d >= 4 else ''), marks=mk(slot, 3 if slot.d <= 3 else 5))


@gen('pswave', d=(2, 5))
def g_ps(rng, slot):
    vp = rng.choice([6.0, 6.5, 7.0])
    vs = round(vp / rng.choice([1.70, 1.73, 1.75]), 1)
    dt = round(rng.uniform(4, 90), 1)
    dist = dt * vp * vs / (vp - vs)
    st = rng.choice(['a seismograph station in Wellington', 'a station in Kathmandu', 'a monitoring station in Santiago', 'a school seismometer in Istanbul', 'a station in Tokyo'])
    stem = (f'At {st}, the S-waves from an earthquake arrived {dt} s after the P-waves. Assuming P-waves travel at {vp} km/s and S-waves at {vs} km/s, '
            'calculate the distance to the earthquake focus (d = Δt × vp × vs / (vp − vs)).')
    if slot.d >= 4:
        stem += ' Explain why at least three stations are needed to locate the epicentre.'
    return dict(stem=stem, answer=f'd = {dt} × {vp} × {vs} / ({vp} − {vs}) = {dist:,.0f} km' + ('; one station gives only a distance (a circle); circles from three stations intersect at the epicentre (triangulation).' if slot.d >= 4 else ''),
                markingKey=f'M1 substitution; A1 {dist:,.0f} km.' + (' R1 triangulation explained.' if slot.d >= 4 else ''), marks=mk(slot, 3 if slot.d <= 3 else 4))


TSU = [('the 2004 Indian Ocean tsunami', 'the Sumatra coast', 'Sri Lanka', 1600, 3500), ('the 2011 Tōhoku tsunami', 'the Japan Trench', 'Hawaii', 6200, 4600),
       ('the 2010 Chile tsunami', 'the coast of Maule', 'Japan', 17000, 4200), ('the 2004 Indian Ocean tsunami', 'Sumatra', 'the coast of Somalia', 5000, 4000),
       ('a scenario tsunami', 'the Cascadia subduction zone', 'Japan', 7500, 4300), ('the 2022 Hunga Tonga-Hunga Ha\'apai tsunami', 'Tonga', 'New Zealand', 2000, 3500)]


@gen('tsunami', d=(2, 5))
def g_tsu(rng, slot):
    ev, src, dest, D, depth = rng.choice(TSU)
    depth = round(depth * rng.uniform(0.9, 1.1), -1)
    D = round(D * rng.uniform(0.95, 1.05), -1)
    v = math.sqrt(9.81 * depth)
    vk = v * 3.6
    t = D / vk
    stem = (f'For {ev}, waves travelled about {D:,.0f} km from {src} to {dest} across ocean with a mean depth of about {depth:,.0f} m. '
            'Using v = √(g × d) with g = 9.81 m/s², calculate the wave speed (m/s and km/h) and the approximate travel time.')
    if slot.d >= 4:
        stem += ' Explain why tsunami waves increase in height as they approach the coast.'
    return dict(stem=stem, answer=f'v = √(9.81 × {depth:,.0f}) = {v:.0f} m/s = {vk:.0f} km/h; time ≈ {D:,.0f} / {vk:.0f} = {t:.1f} hours' + ('; in shallow water speed falls, so the wave shortens and energy is compressed into a greater height (shoaling).' if slot.d >= 4 else ''),
                markingKey=f'M1 √(gd); A1 {v:.0f} m/s; A1 {vk:.0f} km/h; A1 {t:.1f} h.' + (' R1 shoaling explanation.' if slot.d >= 4 else ''), marks=mk(slot, 4 if slot.d <= 3 else 6))


@gen('risk', d=(1, 4))
def g_risk(rng, slot):
    pa, pb = rng.sample(['a coastal district of Port-au-Prince', 'central Christchurch', 'a hillside favela in Rio de Janeiro', 'a district of Kathmandu',
                         'downtown Tokyo', 'a town near Mount Merapi', 'a barangay in Tacloban', 'a suburb of Lima', 'a village in the Nepal Himalaya'], 2)
    h1, v1, c1 = rng.randint(4, 9), rng.randint(2, 9), rng.randint(1, 9)
    h2, v2, c2 = rng.randint(4, 9), rng.randint(2, 9), rng.randint(1, 9)
    r1, r2 = h1 * v1 / c1, h2 * v2 / c2
    stem = (f'A planner scores two places from 1 (low) to 10 (high) - {pa}: hazard {h1}, vulnerability {v1}, capacity {c1}; {pb}: hazard {h2}, vulnerability {v2}, capacity {c2}. '
            'Using risk = hazard × vulnerability / capacity, calculate the risk score for each place and state which has the greater risk.')
    if slot.d >= 3:
        stem += ' Suggest how the place with greater risk could reduce it, other than by changing the hazard.'
    hi = pa if r1 > r2 else pb
    return dict(stem=stem, answer=f'{pa}: {r1:.1f}; {pb}: {r2:.1f}; greater risk: {hi}' + ('; reduce vulnerability (building codes, land-use zoning) or increase capacity (warnings, drills, emergency services, insurance).' if slot.d >= 3 else ''),
                markingKey=f'A1 {r1:.1f}; A1 {r2:.1f}; R1 comparison.' + (' R1 strategy targeting vulnerability or capacity.' if slot.d >= 3 else ''), marks=mk(slot, 3 if slot.d <= 2 else 4))


@gen('vei', d=(1, 4))
def g_vei(rng, slot):
    exp = rng.choice([-3, -2, -1, 0, 1, 2])
    vol = round(10 ** exp * rng.uniform(1.05, 9.5), 3 if exp < 0 else 1)
    vei = {-3: 2, -2: 3, -1: 4, 0: 5, 1: 6, 2: 7}[exp]
    volc = rng.choice(['a stratovolcano in the Andes', 'a volcano in the Aleutian arc', 'an Indonesian stratovolcano', 'a volcano in Kamchatka', 'a Philippine volcano'])
    stem = (f'An eruption of {volc} ejected about {vol} km³ of tephra. The VEI scale is logarithmic: VEI 2 ≥ 0.001 km³, VEI 3 ≥ 0.01, VEI 4 ≥ 0.1, VEI 5 ≥ 1, VEI 6 ≥ 10, VEI 7 ≥ 100 km³. '
            'Assign the eruption a VEI.')
    ans = f'VEI {vei}'
    key = f'A1 VEI {vei} ({vol} km³ lies between {10 ** exp:g} and {10 ** (exp + 1):g} km³).'
    if slot.d >= 3:
        ref, rv = rng.choice([('Mount St Helens 1980', 1.0), ('Pinatubo 1991', 10.0), ('Tambora 1815', 150.0), ('Eyjafjallajökull 2010', 0.27)])
        ratio = vol / rv
        stem += f' How does its ejected volume compare with {ref} (about {rv} km³)?'
        ans += f'; {vol} / {rv} = {ratio:.3g} times the volume of {ref}'
        key += f' A1 ratio {ratio:.3g}.'
    return dict(stem=stem, answer=ans, markingKey=key, marks=mk(slot, 2 if slot.d <= 2 else 3))


@gen('landslide', d=(2, 5))
def g_fs(rng, slot):
    s = rng.randint(40, 120)
    t = rng.randint(30, 110)
    loss = rng.choice([15, 20, 25, 30, 35])
    fs1 = s / t
    fs2 = s * (1 - loss / 100) / t
    site = rng.choice(['a cut slope above a highway in Hong Kong', 'a hillside above a favela in Petrópolis, Brazil', 'a terraced slope in the Nepal Middle Hills',
                       'a road cutting in Kerala', 'a slope in the Cordillera, Philippines'])
    stem = (f'At {site}, the shear strength of the regolith is {s} kPa and the shear stress acting down the slope is {t} kPa. Calculate the factor of safety (strength ÷ stress). '
            f'Intense rainfall then raises pore-water pressure, reducing shear strength by {loss}%. Calculate the new factor of safety and state whether the slope is likely to fail.')
    if slot.d >= 4:
        stem += ' Explain one human action that could have reduced the factor of safety.'
    return dict(stem=stem, answer=f'FS = {s}/{t} = {fs1:.2f}; after rain FS = {s * (1 - loss / 100):.1f}/{t} = {fs2:.2f}; ' + ('failure likely (FS < 1)' if fs2 < 1 else 'stable but marginal (FS ≥ 1)' if fs2 < 1.3 else 'stable (FS ≥ 1)')
                + ('; e.g. undercutting the slope for roads or houses increases shear stress; deforestation removes root cohesion; leaking water pipes raise pore pressure.' if slot.d >= 4 else ''),
                markingKey=f'A1 FS {fs1:.2f}; M1 strength reduced by {loss}%; A1 FS {fs2:.2f}; R1 FS < 1 means failure.' + (' R1 human action explained.' if slot.d >= 4 else ''), marks=mk(slot, 4 if slot.d <= 3 else 5))


@gen('gutenberg', d=(2, 4))
def g_gr(rng, slot):
    n4 = rng.choice([120, 250, 400, 800, 1500, 3000])
    m1 = rng.choice([4, 4.5, 5])
    m2 = m1 + rng.choice([1, 1.5, 2])
    n1 = n4
    n2 = n1 / 10 ** (m2 - m1)
    reg = rng.choice(['Japan', 'California', 'Chile', 'Indonesia', 'Türkiye', 'New Zealand'])
    return dict(stem=f'A seismic network in {reg} records on average {n1} earthquakes of magnitude ≥ {m1} per year. Assuming the Gutenberg-Richter relationship with b = 1 (ten times fewer earthquakes for each unit increase in magnitude), '
                     f'estimate the number of earthquakes of magnitude ≥ {m2} per year and the average recurrence interval of such an event.',
                answer=f'{n1} / 10^{m2 - m1:g} = {n2:.3g} per year; recurrence interval ≈ {1 / n2:.3g} years',
                markingKey=f'M1 divide by 10^(ΔM); A1 {n2:.3g} per year; A1 recurrence {1 / n2:.3g} years.', marks=mk(slot, 3))


DIS = [('the 2010 Haiti earthquake (Mw 7.0)', 160000, 10.0, 'Haiti'), ('the 2010 Maule earthquake, Chile (Mw 8.8)', 525, 17.1, 'Chile'),
       ('the 2015 Gorkha earthquake (Mw 7.8)', 9000, 28.0, 'Nepal'), ('the February 2011 Christchurch earthquake (Mw 6.2)', 185, 4.4, 'New Zealand'),
       ('the 2011 Tōhoku earthquake and tsunami (Mw 9.1)', 18500, 128, 'Japan'), ('the 1995 Kobe earthquake (Mw 6.9)', 6434, 125, 'Japan'),
       ('the 2023 Kahramanmaraş earthquakes (Mw 7.8 and 7.5)', 53500, 85, 'Türkiye'), ('the 2023 Al Haouz earthquake (Mw 6.8)', 2960, 37.0, 'Morocco')]


@gen('deathrate', d=(1, 4))
def g_dr(rng, slot):
    (a, da, pa, ca), (b, db, pb, cb) = rng.sample(DIS, 2)
    ra, rb = da / pa, db / pb
    stem = (f'{a[0].upper() + a[1:]} caused about {da:,} deaths in {ca} (national population about {pa} million); {b} caused about {db:,} deaths in {cb} (population about {pb} million). '
            'Calculate deaths per million people for each event.')
    if slot.d >= 3:
        stem += ' Suggest two reasons for the difference.'
    hi = a if ra > rb else b
    return dict(stem=stem, answer=f'{ca}: {ra:,.1f} per million; {cb}: {rb:,.1f} per million; higher: {hi}' + ('; e.g. building codes and enforcement, poverty and informal construction, preparedness and warning systems, governance and emergency response, depth/distance of the earthquake from population.' if slot.d >= 3 else ''),
                markingKey=f'M1 deaths ÷ population (millions); A1 {ra:,.1f}; A1 {rb:,.1f}.' + (' R1 R1 two valid, developed reasons.' if slot.d >= 3 else ''), marks=mk(slot, 3 if slot.d <= 2 else 5))


HDI_C = [('Norway', 83.3, 18.6, 13.1, 69000), ('Japan', 84.8, 15.2, 13.4, 44000), ('Brazil', 73.4, 15.6, 8.3, 17700), ('India', 67.7, 12.6, 6.6, 6950),
         ('Bangladesh', 73.7, 12.4, 7.4, 6500), ('Nigeria', 53.6, 10.1, 7.6, 4800), ('Niger', 61.6, 7.0, 2.1, 1240), ('Mexico', 74.8, 14.9, 9.2, 19100),
         ('Kenya', 62.1, 11.0, 6.9, 4800), ('Vietnam', 74.6, 13.0, 8.5, 11000), ('Chile', 79.5, 16.8, 11.1, 25000), ('Ethiopia', 65.0, 9.4, 3.2, 2400)]


@gen('hdi', d=(2, 5))
def g_hdi(rng, slot):
    c, le, eys, mys, gni = rng.choice(HDI_C)
    lei = (le - 20) / 65
    ei = (min(mys, 15) / 15 + min(eys, 18) / 18) / 2
    ii = (math.log(gni) - math.log(100)) / (math.log(75000) - math.log(100))
    hdi = (lei * ei * ii) ** (1 / 3)
    cat = 'very high' if hdi >= 0.8 else 'high' if hdi >= 0.7 else 'medium' if hdi >= 0.55 else 'low'
    stem = (f'Approximate data for {c}: life expectancy {le} years; expected years of schooling {eys}; mean years of schooling {mys}; GNI per capita US${gni:,} (PPP). '
            'Using the UNDP method - life expectancy index = (LE − 20)/65; education index = (MYS/15 + EYS/18)/2, with EYS capped at 18; income index = (ln GNI − ln 100)/(ln 75,000 − ln 100); '
            'HDI = geometric mean of the three indices - calculate the HDI and its category.')
    if slot.d >= 4:
        stem += ' Identify the weakest dimension and suggest one policy to improve it.'
    weakest = min([('health', lei), ('education', ei), ('income', ii)], key=lambda x: x[1])[0]
    return dict(stem=stem, answer=f'LEI {lei:.3f}; EI {ei:.3f}; II {ii:.3f}; HDI = ({lei:.3f} × {ei:.3f} × {ii:.3f})^(1/3) = {hdi:.3f} ({cat} human development)' + (f'; weakest dimension: {weakest}.' if slot.d >= 4 else ''),
                markingKey=f'A1 LEI {lei:.3f}; A1 EI {ei:.3f}; A1 II {ii:.3f}; M1 geometric mean; A1 HDI {hdi:.3f}, {cat}.' + (f' R1 {weakest} identified, R1 relevant policy.' if slot.d >= 4 else ''),
                marks=mk(slot, 5 if slot.d <= 3 else 7))


@gen('mpi', d=(1, 4))
def g_mpi(rng, slot):
    # headcount ranges roughly consistent with UNDP-OPHI subnational estimates
    reg, hlo, hhi = rng.choice([('a rural region of Niger', 75, 95), ('a province of Afghanistan', 40, 80), ('a state in northern India', 20, 45), ('a region of Ethiopia', 55, 90),
                                ('a department of Haiti', 25, 60), ('a province of Madagascar', 55, 85), ('a division of Bangladesh', 15, 35), ('a county of northern Kenya', 50, 85)])
    h = rng.randint(hlo, hhi)
    a = rng.randint(38, 62)
    mpi = h / 100 * a / 100
    stem = f'In {reg}, {h}% of people are multidimensionally poor (headcount, H) and the poor are deprived in an average of {a}% of the weighted indicators (intensity, A). Calculate the Multidimensional Poverty Index (MPI = H × A).'
    if slot.d >= 3:
        h2 = max(5, h - rng.randint(5, 25))
        mpi2 = h2 / 100 * a / 100
        stem += f' Ten years later H has fallen to {h2}% with no change in intensity: calculate the new MPI and the percentage reduction.'
        return dict(stem=stem, answer=f'MPI = {h / 100:.2f} × {a / 100:.2f} = {mpi:.3f}; new MPI = {mpi2:.3f}; reduction {(mpi - mpi2) / mpi * 100:.1f}%',
                    markingKey=f'A1 {mpi:.3f}; A1 {mpi2:.3f}; A1 {(mpi - mpi2) / mpi * 100:.1f}%.', marks=mk(slot, 4))
    return dict(stem=stem, answer=f'MPI = {h / 100:.2f} × {a / 100:.2f} = {mpi:.3f}', markingKey=f'M1 H × A as proportions; A1 {mpi:.3f}.', marks=mk(slot, 2))


@gen('gini', d=(2, 5))
def g_gini(rng, slot):
    for _ in range(50):
        raw = sorted(rng.uniform(1, 10) for _ in range(5))
        raw[-1] *= rng.uniform(1.0, 3.0)
        tot = sum(raw)
        sh = [round(x / tot * 100) for x in raw]
        sh[-1] = 100 - sum(sh[:-1])
        if all(sh[i] < sh[i + 1] for i in range(4)) and sh[0] >= 1:
            break
    else:
        return None
    cum = [0]
    for x in sh:
        cum.append(cum[-1] + x / 100)
    g = 1 - sum(0.2 * (cum[i] + cum[i + 1]) for i in range(5))
    c = rng.choice(['South Africa', 'Brazil', 'Sweden', 'Vietnam', 'Colombia', 'Germany', 'Indonesia', 'Namibia'])
    stem = (f'Income shares by quintile (poorest to richest 20%) in an illustrative data set modelled on {c}: {", ".join(f"{x}%" for x in sh)}. '
            'Calculate the cumulative shares and estimate the Gini coefficient using G = 1 − Σ (Xk − Xk−1)(Yk + Yk−1), where X steps by 0.2.')
    if slot.d >= 4:
        stem += ' Calculate the ratio of the richest to the poorest quintile\'s share and comment on the level of inequality.'
    lvl = 'high' if g >= 0.45 else 'moderate' if g >= 0.3 else 'low'
    return dict(stem=stem, answer=f'cumulative shares {", ".join(f"{x:.2f}" for x in cum[1:])}; Gini ≈ {g:.3f}' + (f'; top/bottom ratio = {sh[-1] / sh[0]:.1f}; {lvl} inequality' if slot.d >= 4 else ''),
                markingKey=f'M1 cumulative shares; M1 trapezium sum; A1 G ≈ {g:.3f}.' + (f' A1 ratio {sh[-1] / sh[0]:.1f}; R1 interpretation ({lvl}).' if slot.d >= 4 else ''), marks=mk(slot, 4 if slot.d <= 3 else 6))


ODA = [('Norway', 5.5, 570), ('Sweden', 5.6, 620), ('Germany', 37.9, 4700), ('the UK', 19.1, 3330), ('France', 15.4, 3090),
       ('Japan', 19.6, 4500), ('the USA', 66.0, 27700), ('Australia', 3.3, 1700), ('Canada', 8.1, 2100), ('South Korea', 3.1, 1800)]


@gen('oda', d=(1, 4))
def g_oda(rng, slot):
    c, oda, gni = rng.choice(ODA)
    oda = round(oda * rng.uniform(0.95, 1.05), 1)
    s = oda / gni * 100
    stem = f'In a recent year {c} provided about US${oda} billion of official development assistance; its GNI was about US${gni:,} billion. Calculate ODA as a percentage of GNI and compare it with the UN target of 0.7%.'
    gap = (0.007 * gni - oda)
    if slot.d >= 3:
        stem += ' How much extra ODA (US$ billion) would be needed to meet the target?'
        return dict(stem=stem, answer=f'{s:.2f}% of GNI ({"above" if s >= 0.7 else "below"} 0.7%); ' + (f'extra needed ≈ US${gap:.1f} billion' if gap > 0 else 'no extra needed - target already met'),
                    markingKey=f'A1 {s:.2f}%; R1 comparison; A1 0.7% × {gni:,} − {oda} = {gap:.1f}.', marks=mk(slot, 3))
    return dict(stem=stem, answer=f'{s:.2f}% of GNI - {"meets" if s >= 0.7 else "below"} the 0.7% target', markingKey=f'M1 ODA ÷ GNI × 100; A1 {s:.2f}%; R1 comparison.', marks=mk(slot, 2))


@gen('debt', d=(2, 5))
def g_debt(rng, slot):
    c = rng.choice(['Zambia', 'Sri Lanka', 'Ghana', 'Pakistan', 'Kenya', 'Ethiopia', 'Egypt', 'Laos'])
    gdp = rng.randint(15, 400)
    debt = round(gdp * rng.uniform(0.3, 1.1), 1)
    exp = round(gdp * rng.uniform(0.1, 0.35), 1)
    serv = round(exp * rng.uniform(0.08, 0.45), 2)
    r1_, r2_ = debt / gdp * 100, serv / exp * 100
    stem = (f'Illustrative data for {c}: GDP US${gdp} billion; external debt US${debt} billion; exports of goods and services US${exp} billion; annual external debt service US${serv} billion. '
            'Calculate the external debt-to-GDP ratio and the debt-service-to-exports ratio.')
    if slot.d >= 4:
        stem += ' Explain why a high debt-service ratio can hold back development.'
    return dict(stem=stem, answer=f'debt/GDP = {r1_:.1f}%; debt service/exports = {r2_:.1f}%' + ('; export earnings spent on repayments cannot fund health, education or infrastructure, and currency shortages raise import costs (e.g. Sri Lanka 2022, Zambia default 2020).' if slot.d >= 4 else ''),
                markingKey=f'A1 {r1_:.1f}%; A1 {r2_:.1f}%.' + (' R1 R1 developed explanation with example.' if slot.d >= 4 else ''), marks=mk(slot, 3 if slot.d <= 3 else 5))


@gen('kof', d=(1, 4))
def g_kof(rng, slot):
    # approximate KOF sub-indices (economic, social, political), KOF 2023 release; small noise added so items differ
    KOF = {'Switzerland': (87, 90, 94), 'the Netherlands': (91, 88, 93), 'Singapore': (91, 86, 77), 'Germany': (81, 88, 96), 'Brazil': (55, 65, 89),
           'India': (52, 51, 89), 'Nigeria': (46, 42, 81), 'Chad': (31, 27, 65), 'Vietnam': (73, 58, 80), 'Bolivia': (56, 57, 72), 'Mongolia': (62, 55, 62), 'Japan': (70, 80, 93)}
    a, b = rng.sample(sorted(KOF), 2)
    ea, sa, pa = (min(99, v + rng.randint(-2, 2)) for v in KOF[a])
    eb, sb, pb = (min(99, v + rng.randint(-2, 2)) for v in KOF[b])
    ka, kb = (ea + sa + pa) / 3, (eb + sb + pb) / 3
    stem = (f'Approximate globalisation sub-index scores (0-100): {a} - economic {ea}, social {sa}, political {pa}; {b} - economic {eb}, social {sb}, political {pb}. '
            'Assuming the three dimensions are weighted equally (as in the KOF index), calculate the overall index for each country.')
    if slot.d >= 3:
        stem += ' Explain one limitation of composite globalisation indices.'
    return dict(stem=stem, answer=f'{a}: {ka:.1f}; {b}: {kb:.1f}' + ('; limitation: weights are arbitrary, national averages hide regional differences, and data on informal or illicit flows are missing.' if slot.d >= 3 else ''),
                markingKey=f'A1 {ka:.1f}; A1 {kb:.1f}.' + (' R1 limitation.' if slot.d >= 3 else ''), marks=mk(slot, 2 if slot.d <= 2 else 4))


FREIGHT = [('container ship', 12), ('rail', 25), ('heavy goods vehicle', 80), ('air freight', 600)]


@gen('freight', d=(1, 4))
def g_freight(rng, slot):
    (m1, f1), (m2, f2) = rng.sample(FREIGHT, 2)
    t = rng.choice([1, 5, 20, 40, 100, 500])
    route, km = rng.choice([('Shanghai to Rotterdam', 19500), ('Nairobi to Amsterdam', 6600), ('Santiago to Los Angeles', 9000), ('Shenzhen to Frankfurt', 9000), ('Mumbai to London', 7200)])
    e1, e2 = t * km * f1 / 1e6, t * km * f2 / 1e6
    stem = (f'A firm moves {t} tonnes of goods from {route} (about {km:,} km). Emission factors: {m1} {f1} g CO₂ per tonne-km; {m2} {f2} g CO₂ per tonne-km. '
            'Calculate the emissions (tonnes CO₂) for each mode and how many times higher the larger figure is.')
    return dict(stem=stem, answer=f'{m1}: {e1:,.2f} t; {m2}: {e2:,.2f} t; ratio {max(e1, e2) / min(e1, e2):.1f}',
                markingKey=f'M1 tonnes × km × factor ÷ 10⁶; A1 {e1:,.2f}; A1 {e2:,.2f}; A1 ratio {max(e1, e2) / min(e1, e2):.1f}.', marks=mk(slot, 4))


@gen('tsc', d=(1, 4))
def g_tsc(rng, slot):
    route, km = rng.choice([('London to New York', 5570), ('Lisbon to Rio de Janeiro', 7700), ('Southampton to Cape Town', 9700), ('Marseille to Saigon (Ho Chi Minh City)', 12000)])
    v1n, v1 = rng.choice([('a sailing ship (about 10 km/h average)', 10), ('an early steamship (about 25 km/h)', 25)])
    v2n, v2 = rng.choice([('a jet airliner (about 850 km/h)', 850), ('a modern ocean liner (about 45 km/h)', 45)])
    t1, t2 = km / v1, km / v2
    return dict(stem=f'The distance from {route} is about {km:,} km. Calculate the journey time by {v1n} and by {v2n}, and the factor by which travel time has been reduced. Explain how this illustrates time-space compression.',
                answer=f'{t1:,.0f} h ({t1 / 24:.1f} days) vs {t2:,.1f} h; reduced by a factor of {t1 / t2:.0f}; places are effectively "closer" in time, increasing flows of people, goods and ideas.',
                markingKey=f'A1 {t1:,.0f} h; A1 {t2:,.1f} h; A1 factor {t1 / t2:.0f}; R1 time-space compression.', marks=mk(slot, 4))


@gen('diversity', d=(2, 5))
def g_div(rng, slot):
    k = rng.choice([3, 4, 5])
    for _ in range(50):
        cuts = sorted(rng.sample(range(2, 98), k - 1))
        sh = [b - a for a, b in zip([0] + cuts, cuts + [100])]
        if min(sh) >= 2:
            break
    place, pool = rng.choice([('a district of Nairobi', ['Swahili', 'Kikuyu', 'English', 'Luo', 'Luhya', 'Kamba']),
                              ('a ward of East London', ['English', 'Bengali', 'Urdu', 'Polish', 'Somali', 'Punjabi']),
                              ('a neighbourhood of Toronto', ['English', 'Cantonese', 'Mandarin', 'Tagalog', 'Punjabi', 'Portuguese']),
                              ('a municipality near La Paz, Bolivia', ['Spanish', 'Aymara', 'Quechua', 'Guaraní', 'English']),
                              ('a district of Kuala Lumpur', ['Malay', 'Mandarin', 'Cantonese', 'Tamil', 'English']),
                              ('a suburb of Sydney', ['English', 'Arabic', 'Mandarin', 'Vietnamese', 'Greek', 'Hindi'])])
    langs = rng.sample(pool, k)
    di = 1 - sum((x / 100) ** 2 for x in sh)
    stem = (f'A survey of home languages in {place} found: ' + ', '.join(f'{l} {x}%' for l, x in zip(langs, sh)) +
            '. Calculate Greenberg\'s diversity index (DI = 1 − Σp², where p is each language\'s share as a proportion).')
    if slot.d >= 4:
        stem += ' Interpret the result and explain one limitation of the index.'
    return dict(stem=stem, answer=f'Σp² = {sum((x / 100) ** 2 for x in sh):.4f}; DI = {di:.3f} (probability two random people speak different home languages)' + ('; limitation: depends on how languages/dialects are defined and ignores multilingualism.' if slot.d >= 4 else ''),
                markingKey=f'M1 squares of proportions summed; A1 DI = {di:.3f}.' + (' R1 interpretation; R1 limitation.' if slot.d >= 4 else ''), marks=mk(slot, 3 if slot.d <= 3 else 5))


# =============================================================================================
# Option D Geophysical hazards
# =============================================================================================
S('ch01-st1', gens=['pswave', 'pct_hazard', 'gutenberg'],
  terms=[('lithosphere', 'the rigid outer layer of the Earth, made of the crust and uppermost mantle, broken into tectonic plates'),
         ('asthenosphere', 'the weak, partially molten layer of the upper mantle beneath the lithosphere on which plates move'),
         ('mantle convection', 'the slow circulation of heated mantle rock, rising where hot and sinking where cooler, which helps drive plate movement'),
         ('slab pull', 'the force exerted by a cold, dense subducting plate sinking into the mantle, pulling the rest of the plate behind it'),
         ('hotspot', 'a fixed area of unusually hot mantle (a mantle plume) that produces volcanoes away from plate boundaries, e.g. Hawaii'),
         ('subduction zone', 'a convergent boundary where a denser oceanic plate sinks beneath another plate, forming an ocean trench')],
  facts=[('Which type of plate boundary is found along the Mid-Atlantic Ridge?', 'Divergent (constructive)', ['Convergent (destructive)', 'Conservative (transform)', 'Collision'], 'The North American and Eurasian plates move apart at about 2.5 cm a year.'),
         ('The San Andreas Fault in California is an example of a:', 'conservative (transform) boundary', ['divergent boundary', 'oceanic-continental subduction zone', 'hotspot'], 'The Pacific and North American plates slide past each other.'),
         ('Which force is now thought to be the most important driver of plate movement?', 'Slab pull', ['Earth\'s rotation', 'Tidal forces', 'Wind'], 'Ridge push and mantle convection also contribute.'),
         ('The Himalayas formed mainly as a result of:', 'collision between the Indian and Eurasian plates', ['a hotspot beneath Tibet', 'divergence along a mid-ocean ridge', 'a transform fault'], 'The collision began about 50 million years ago and still raises the mountains.'),
         ('Hawaii\'s volcanoes are explained by:', 'a hotspot beneath the moving Pacific Plate', ['subduction of the Pacific Plate', 'a divergent continental rift', 'a conservative boundary'], 'The Hawaiian-Emperor chain records plate movement over the plume.')],
  why=[('Explain why most volcanoes and earthquakes are located along plate boundaries.', 'Plates interact at boundaries: subduction generates magma and stress; divergence allows magma to rise; transform motion builds and releases stress - so seismic and volcanic activity is concentrated in belts such as the Pacific Ring of Fire.'),
       ('Explain how subduction leads to volcanic activity.', 'The descending oceanic plate carries water-rich sediments; at about 100 km depth water is released, lowering the melting point of the overlying mantle wedge, which partially melts; buoyant magma rises to form volcanic arcs such as the Andes or Japan.'),
       ('Explain how a hotspot produces a chain of volcanoes.', 'A stationary mantle plume melts the lithosphere above it; as the plate moves over the plume, older volcanoes are carried away and become extinct while new ones form above the hotspot, creating a chain (Hawaiian-Emperor chain).'),
       ('Explain why collision boundaries produce earthquakes but few volcanoes.', 'Both plates are continental and too buoyant to subduct deeply, so crust crumples and thickens (Himalayas) causing faulting and earthquakes, but little magma is generated.')],
  contrast=[('the lithosphere', 'the asthenosphere', 'The lithosphere is the rigid crust and upper mantle forming plates; the asthenosphere is the hotter, weaker, partially molten mantle layer below on which the plates move.'),
            ('a divergent boundary', 'a convergent boundary', 'At divergent boundaries plates move apart and new crust forms (Mid-Atlantic Ridge); at convergent boundaries plates move together and crust is destroyed by subduction or crumpled by collision (Andes, Himalayas).')],
  misc=[('Tectonic plates float on a layer of liquid magma.', 'The mantle is almost entirely solid; plates move over the asthenosphere, which is weak and only partially molten.'),
        ('All earthquakes and volcanoes occur at plate boundaries.', 'Hotspots (Hawaii, Yellowstone) and intraplate faults (e.g. the 1811-12 New Madrid earthquakes) occur away from boundaries.'),
        ('Mantle convection is the only force driving plate movement.', 'Slab pull and ridge push are now thought to be important, perhaps dominant, forces.')],
  apply=[('Using a named example, describe the processes at one type of plate boundary.', 'e.g. the Nazca and South American plates: the dense oceanic Nazca plate subducts at about 7 cm/yr, forming the Peru-Chile Trench, the Andes and volcanoes such as Villarrica, with frequent large earthquakes (Maule 2010, Mw 8.8).', 4),
         ('Suggest why Iceland has both volcanoes and frequent small earthquakes.', 'It lies on the Mid-Atlantic Ridge where plates diverge and also above a hotspot, so magma rises easily and rifting causes shallow earthquakes.', 2)],
  cases=[('the Peru-Chile Trench', 'the Nazca Plate subducts beneath South America, producing the Andes and earthquakes such as Maule 2010 (Mw 8.8)', 'oceanic-continental subduction', 'subduction generates both magma for volcanoes and stress for great earthquakes'),
         ('Iceland', 'it sits on the Mid-Atlantic Ridge above a mantle plume, with fissure eruptions such as Holuhraun (2014-15) and the Reykjanes eruptions from 2021', 'divergent boundary and hotspot processes', 'plates pulling apart allow basaltic magma to rise to the surface'),
         ('the Hawaiian-Emperor seamount chain', 'a chain over 6,000 km long, with active volcanoes such as Kīlauea on the Big Island', 'hotspot volcanism', 'the age progression of volcanoes records movement of the Pacific Plate over a fixed plume'),
         ('the Himalayas', 'the Indian plate converges with Eurasia at about 4-5 cm a year, raising Everest and causing earthquakes such as Gorkha 2015', 'continental collision', 'buoyant continental crust crumples and thickens rather than subducting')],
  evaluate=[('Plate tectonic theory fully explains the global distribution of geophysical hazards.', ['most earthquakes and volcanoes lie along boundaries (Ring of Fire)', 'explains different hazard types by boundary type'], ['hotspots and intraplate earthquakes need additional explanation (mantle plumes)', 'mass movements depend on climate, relief and human activity'], 'Plate tectonics explains most volcanic and seismic hazards, but not all geophysical hazards.'),
            ('Slab pull is the most important driver of plate movement.', ['subducting plates move fastest (Pacific, Nazca)', 'models show slab pull provides most force'], ['ridge push and mantle convection also contribute', 'plates without subducting edges still move'], 'Slab pull is probably dominant, but plate motion results from several interacting forces.')],
  extended=[('Explain the internal structure of the Earth and how it causes movement of tectonic plates.', 'Crust, mantle (lithosphere, asthenosphere), outer and inner core; heat from radioactive decay; convection, slab pull, ridge push; boundary types with examples.', 10, 'long')],
  res=[('Table: plate motion rates (cm per year, approximate) - Nazca relative to South America 7; Pacific relative to North America (San Andreas) 3.5; India relative to Eurasia 4.5; Mid-Atlantic Ridge spreading 2.5.',
        [('Calculate how far the Nazca Plate moves relative to South America in 1,000 years (in metres).', '7 cm × 1,000 = 7,000 cm = 70 m'),
         ('Suggest why plate speeds differ.', 'Plates attached to long subducting slabs (Nazca, Pacific) are pulled faster by slab pull; continental plates and slow ridges move more slowly.')]),
       ('Map description: a world map shows narrow belts of earthquake epicentres along the margins of the Pacific Ocean, the mid-ocean ridges and from the Mediterranean through Iran to the Himalayas, with isolated volcanoes in Hawaii and Yellowstone.',
        [('Describe the distribution shown.', 'Linear belts along plate boundaries - especially the Pacific Ring of Fire, mid-ocean ridges and the Alpine-Himalayan belt - with a few isolated intraplate hotspots.'),
         ('Explain the isolated volcanoes shown on the map.', 'Hawaii and Yellowstone are above mantle plumes (hotspots), where heat rising from deep in the mantle melts the overlying plate.')])])

S('ch01-st2', gens=['vei', 'pct_hazard', 'spearman_hazard'],
  terms=[('Volcanic Explosivity Index (VEI)', 'a logarithmic scale from 0 to 8 measuring eruption size by volume of ejected material, eruption column height and duration'),
         ('stratovolcano', 'a steep-sided composite volcano built of alternating layers of lava and ash, typical of subduction zones, e.g. Mount Fuji'),
         ('shield volcano', 'a broad, gently sloping volcano formed by fluid basaltic lava flows, e.g. Mauna Loa'),
         ('viscosity', 'the resistance of magma to flow; high-silica (andesitic, rhyolitic) magma is viscous and traps gas, giving explosive eruptions'),
         ('pyroclastic flow', 'a fast-moving current of hot gas, ash and rock that flows down a volcano at over 100 km/h'),
         ('tephra', 'fragments of volcanic material ejected into the air during an eruption, from fine ash to large volcanic bombs')],
  facts=[('Which eruption had a VEI of 6 and cooled global temperatures by about 0.5 °C?', 'Mount Pinatubo, 1991', ['Eyjafjallajökull, 2010', 'Kīlauea, 2018', 'Mount St Helens, 1980'], 'Pinatubo ejected about 10 km³ of material.'),
         ('Each step on the VEI scale represents about how much more erupted material?', 'Ten times', ['Twice', 'One hundred times', 'One thousand times'], 'The scale is logarithmic above VEI 2.'),
         ('Which type of magma produces the most explosive eruptions?', 'Rhyolitic (high silica, high gas, high viscosity)', ['Basaltic (low silica)', 'Ultramafic', 'Carbonatite'], 'Viscous magma traps gases until pressure is released explosively.'),
         ('The 1815 eruption of Tambora, Indonesia (VEI 7) led to:', '"the year without a summer" in 1816', ['the Little Ice Age beginning in 1300', 'the end of the last glacial period', 'the 2004 tsunami'], 'Crop failures and famine occurred in Europe and North America.')],
  why=[('Explain why eruptions at subduction zones are usually more explosive than at hotspots.', 'Subduction produces andesitic to rhyolitic magma rich in silica and water; high viscosity traps gas, so pressure builds until it is released explosively; hotspot magma is basaltic, runny and gas escapes easily.'),
       ('Explain why the VEI does not measure the impact of an eruption on people.', 'It measures physical size (volume, column height), not exposure or vulnerability; a small eruption near a city (e.g. Nevado del Ruiz 1985, VEI 3) can kill more people than a larger remote one.'),
       ('Explain how a shield volcano differs in form from a stratovolcano.', 'Fluid basaltic lava flows long distances to build broad, gentle slopes (Mauna Loa); viscous lava and ash layers build steep, symmetrical cones (Fuji, Mayon).'),
       ('Explain why gas content is important in determining the type of eruption.', 'Dissolved gases (water vapour, CO₂) expand as magma rises; if they cannot escape, they fragment magma into ash and drive explosive Plinian eruptions; low gas or easy escape gives effusive eruptions.')],
  contrast=[('effusive eruptions', 'explosive eruptions', 'Effusive eruptions release fluid lava flows with low gas pressure (Kīlauea); explosive eruptions fragment viscous, gas-rich magma into ash, pumice and pyroclastic flows (Pinatubo).'),
            ('a shield volcano', 'a stratovolcano', 'A shield volcano is broad and gently sloping, built of basaltic lava (Mauna Loa); a stratovolcano is steep and layered with lava and ash from andesitic magma (Fuji).')],
  misc=[('Lava flows are the most deadly volcanic hazard.', 'Lava usually moves slowly enough to escape; pyroclastic flows, lahars and famine after eruptions cause most deaths.'),
        ('A higher VEI always means more deaths.', 'Deaths depend on population exposure and preparedness; Pinatubo (VEI 6) killed about 850 thanks to evacuation, whereas Nevado del Ruiz (VEI 3) killed about 23,000.'),
        ('All volcanoes erupt in the same way.', 'Eruption style depends on magma composition, gas content and tectonic setting.')],
  apply=[('Using a named eruption, describe its characteristics and explain them using magma type.', 'e.g. Mount St Helens 1980: a lateral blast and Plinian column (VEI 5) after a bulge grew on the north flank; dacitic, gas-rich, viscous magma from Cascadia subduction trapped pressure until a landslide released it.', 4),
         ('Suggest why Eyjafjallajökull (2010, VEI 4) had large economic impacts.', 'Fine glass-rich ash was carried by north-westerly winds into European airspace, closing airspace for about six days and cancelling about 100,000 flights.', 2)],
  cases=[('the 1991 eruption of Mount Pinatubo, Philippines', 'a VEI 6 eruption ejected about 10 km³ of material, but evacuation of about 60,000 people limited deaths to about 850', 'explosive eruptions at subduction zones', 'silica-rich magma and gas pressure produced a very large Plinian eruption'),
         ('the 2018 eruption of Kīlauea, Hawaii', 'lava flows destroyed over 700 homes in Leilani Estates but caused no direct deaths', 'effusive basaltic eruptions', 'fluid, low-viscosity lava flowed rather than exploding'),
         ('the 2010 eruption of Eyjafjallajökull, Iceland', 'meltwater from the glacier chilled magma, producing fine ash that closed European airspace', 'the interaction of magma and ice in eruptions', 'phreatomagmatic fragmentation made unusually fine, far-travelled ash'),
         ('the 1980 eruption of Mount St Helens, USA', 'the north flank collapsed in the largest landslide in recorded history, followed by a lateral blast and a VEI 5 eruption', 'the eruption style of stratovolcanoes', 'viscous dacitic magma trapped gas until the flank collapse released pressure suddenly')],
  evaluate=[('The Volcanic Explosivity Index is the most useful way to compare volcanic hazards.', ['objective, comparable measure of eruption size', 'logarithmic scale captures huge range'], ['does not measure impacts, gas output (climate effects) or lava hazards', 'risk depends on exposure and vulnerability'], 'VEI is useful for size but must be combined with measures of impact and risk.'),
            ('Explosive eruptions are a greater threat to people than effusive eruptions.', ['pyroclastic flows, lahars and ash affect large areas (Pinatubo, Ruiz)', 'global climatic effects (Tambora)'], ['effusive eruptions can destroy property and release toxic gases (Laki 1783 killed about a fifth of Iceland\'s population)', 'many explosive volcanoes are remote'], 'Explosive eruptions generally pose greater threats to life, but large effusive eruptions can have severe indirect impacts.')],
  extended=[('Explain how magma type and plate setting influence the characteristics of volcanic eruptions.', 'Basaltic vs andesitic/rhyolitic magma; viscosity and gas; hotspot/divergent vs subduction settings; shield vs stratovolcano; VEI; named examples (Kīlauea, Pinatubo, Eyjafjallajökull).', 10, 'long')],
  res=[('Table: selected eruptions - Kīlauea 2018: VEI 0-1, lava flows; Eyjafjallajökull 2010: VEI 4, about 0.27 km³; Mount St Helens 1980: VEI 5, about 1 km³; Pinatubo 1991: VEI 6, about 10 km³; Tambora 1815: VEI 7, about 150 km³.',
        [('How many times greater was the ejected volume of Tambora than Mount St Helens?', '150 / 1 = 150 times (just over two VEI steps).'),
         ('Explain why Tambora had global effects.', 'It injected large amounts of sulphur dioxide into the stratosphere, forming aerosols that reflected sunlight and cooled the Northern Hemisphere ("year without a summer", 1816).')]),
       ('Graph description: ash thickness (mm) at distances downwind of a volcano - 5 km: 320; 10 km: 180; 20 km: 90; 40 km: 30; 80 km: 6.',
        [('Calculate the percentage decrease in ash thickness between 5 km and 40 km.', f'(30 − 320)/320 × 100 = {pc(320, 30)}'),
         ('Describe the relationship shown.', 'Ash thickness decreases rapidly with distance, roughly halving with each doubling of distance, as heavier particles fall out first.')])])

S('ch01-st3', gens=['magnitude', 'pswave', 'gutenberg'],
  terms=[('focus (hypocentre)', 'the point within the Earth where an earthquake rupture begins'),
         ('epicentre', 'the point on the Earth\'s surface directly above the focus'),
         ('moment magnitude scale', 'a logarithmic scale (Mw) measuring the energy released by an earthquake, based on fault area, slip and rock rigidity'),
         ('Modified Mercalli Intensity scale', 'a scale from I to XII describing the effects of shaking on people, buildings and the landscape at a particular place'),
         ('P-waves', 'primary seismic waves that are compressional, travel fastest and pass through solids and liquids'),
         ('S-waves', 'secondary seismic waves that are shear waves, slower than P-waves and unable to pass through liquids'),
         ('elastic rebound', 'the sudden release of strain energy stored in rocks as a fault ruptures, causing an earthquake')],
  facts=[('An increase of one unit on the moment magnitude scale represents about how much more energy?', 'About 32 times', ['About 2 times', 'About 10 times', 'About 1,000 times'], 'Energy increases by 10^1.5 ≈ 31.6 per unit.'),
         ('Which seismic waves cause most damage at the surface?', 'Surface waves (Love and Rayleigh waves)', ['P-waves', 'Tidal waves', 'Radio waves'], 'Surface waves have large amplitudes and arrive last.'),
         ('The Mercalli scale differs from the moment magnitude scale because it measures:', 'observed effects of shaking at a location', ['the energy released at the focus', 'the length of the fault', 'the depth of the focus'], 'An earthquake has one magnitude but many intensities.'),
         ('The largest earthquake ever recorded was:', 'the 1960 Valdivia earthquake, Chile (Mw 9.5)', ['the 2011 Tōhoku earthquake (Mw 9.1)', 'the 2004 Sumatra earthquake (Mw 9.1)', 'the 1906 San Francisco earthquake (Mw 7.9)'], 'It generated a Pacific-wide tsunami.')],
  why=[('Explain how earthquakes are caused by elastic rebound.', 'Plates are locked by friction while moving; strain energy builds in rocks either side of the fault; when stress exceeds friction the fault slips suddenly and the rocks rebound, releasing energy as seismic waves.'),
       ('Explain why shallow-focus earthquakes are often more damaging than deep-focus earthquakes.', 'Shallow foci (0-70 km) are closer to the surface, so seismic energy is less attenuated and shaking is more intense at the epicentre, e.g. Christchurch 2011 at about 5 km depth.'),
       ('Explain why the same earthquake can have different Mercalli intensities at different places.', 'Intensity decreases with distance from the epicentre, but also depends on local geology (soft sediments amplify shaking), building quality and population density.'),
       ('Explain why magnitude scales are logarithmic.', 'Earthquake sizes vary over many orders of magnitude; a logarithmic scale compresses this range so that each unit represents a ten-fold increase in amplitude and about 32 times more energy.')],
  contrast=[('magnitude', 'intensity', 'Magnitude measures the energy released at the source and has one value per earthquake; intensity describes the effects of shaking at a particular location and varies from place to place.'),
            ('P-waves', 'S-waves', 'P-waves are compressional, faster and travel through solids and liquids; S-waves are shear waves, slower and travel only through solids, so they are absent from the outer core\'s shadow zone.')],
  misc=[('A magnitude 8 earthquake releases twice as much energy as a magnitude 4 earthquake.', 'The scale is logarithmic: four units difference is about 31.6⁴ ≈ 1,000,000 times more energy.'),
        ('Earthquakes can now be predicted to the exact day.', 'Scientists can forecast probabilities over decades for a fault but cannot predict the time, place and size of a specific earthquake.'),
        ('The epicentre is the point underground where the earthquake starts.', 'That is the focus (hypocentre); the epicentre is the point on the surface directly above it.')],
  apply=[('Using a named example, explain how fault movement caused an earthquake.', 'e.g. 2023 Kahramanmaraş, Türkiye: strain on the East Anatolian Fault, a left-lateral strike-slip fault between the Anatolian and Arabian plates, was released over a rupture about 350 km long, producing a Mw 7.8 earthquake followed by a Mw 7.5 event.', 4),
         ('Suggest why the 2011 Christchurch earthquake (Mw 6.2) was more damaging than the larger 2010 Darfield earthquake (Mw 7.1).', 'Its focus was shallow (about 5 km) and close to the city centre; strong vertical acceleration; liquefaction of soft sediments; buildings were already weakened in 2010; it struck at lunchtime.', 3)],
  cases=[('the 1960 Valdivia earthquake, Chile', 'the largest earthquake ever recorded (Mw 9.5) ruptured about 1,000 km of the subduction zone and caused a Pacific-wide tsunami', 'megathrust earthquakes', 'the sudden slip of a huge locked area of a subduction zone released enormous energy'),
         ('the February 2011 Christchurch earthquake', 'a shallow Mw 6.2 earthquake on a previously unknown fault killed 185 people', 'the influence of focal depth and proximity on intensity', 'a shallow focus close to the city produced very strong shaking despite moderate magnitude'),
         ('the 2023 Kahramanmaraş earthquakes, Türkiye and Syria', 'two earthquakes (Mw 7.8 and 7.5) on the East Anatolian Fault killed over 59,000 people', 'strike-slip faulting', 'long ruptures on a transform fault produced intense shaking over a wide area'),
         ('the 1906 San Francisco earthquake', 'about 477 km of the San Andreas Fault ruptured, and fires burned much of the city', 'elastic rebound', 'Reid\'s study of offset fences and roads after this event led to elastic rebound theory')],
  evaluate=[('Earthquake magnitude is the most important factor in determining earthquake impacts.', ['higher magnitude releases more energy and shakes larger areas', 'great earthquakes can trigger tsunamis (Tōhoku 2011)'], ['Haiti 2010 (Mw 7.0) killed far more than Chile 2010 (Mw 8.8)', 'depth, distance, geology, buildings and preparedness determine impacts'], 'Magnitude sets the potential, but vulnerability and local conditions largely determine impacts.'),
            ('Intensity scales are more useful than magnitude scales for hazard management.', ['show where damage occurs and guide emergency response', 'can be compiled from public reports ("Did you feel it?")'], ['magnitude is objective and needed for tsunami warnings', 'intensity depends on subjective observations'], 'Both are needed: magnitude for scientific warning and intensity for planning and response.')],
  extended=[('Explain the causes and characteristics of earthquakes.', 'Elastic rebound; types of faults and plate settings; focus and epicentre; P, S and surface waves; magnitude and intensity scales; examples (Tōhoku, Christchurch, Kahramanmaraş).', 10, 'long')],
  res=[('Table: two New Zealand earthquakes - Darfield, September 2010: Mw 7.1, depth 10 km, 40 km west of Christchurch, 0 deaths; Christchurch, February 2011: Mw 6.2, depth 5 km, 10 km south-east of the centre, 185 deaths.',
        [('Calculate how many times more energy was released by the Darfield earthquake.', f'10^(1.5 × 0.9) = {10 ** 1.35:.1f} times'),
         ('Suggest reasons why the smaller earthquake caused more deaths.', 'Shallower focus and epicentre much closer to the city centre; very strong vertical ground acceleration; buildings weakened in 2010; occurred at 12:51 on a weekday when the CBD was busy.')]),
       ('Seismogram description: a station records the first P-wave at 10:42:05 and the first S-wave at 10:43:17; large surface waves arrive at 10:44:00.',
        [('Calculate the S-P interval.', '10:43:17 − 10:42:05 = 72 seconds'),
         ('Using a rule of thumb of 8 km per second of S-P interval, estimate the distance to the earthquake.', '72 × 8 = 576 km')])])

S('ch01-st4', gens=['landslide', 'spearman_hazard', 'pct_hazard'],
  terms=[('mass movement', 'the downslope movement of rock, regolith or snow under the influence of gravity'),
         ('landslide', 'the rapid downslope movement of a mass of rock or soil along a shear plane'),
         ('avalanche', 'a rapid flow of snow (sometimes with rock and ice) down a slope'),
         ('shear strength', 'the internal resistance of slope materials to movement, from friction and cohesion'),
         ('pore-water pressure', 'the pressure of water in the spaces between soil particles, which reduces friction and shear strength'),
         ('factor of safety', 'the ratio of shear strength to shear stress on a slope; values below 1 indicate likely failure')],
  facts=[('Which of these is most likely to trigger a landslide?', 'Intense rainfall that raises pore-water pressure', ['A long dry period', 'Planting trees on the slope', 'Reducing the slope angle'], 'Water reduces shear strength and adds weight.'),
         ('The 1970 Huascarán avalanche, triggered by an earthquake, buried which Peruvian town?', 'Yungay', ['Cusco', 'Arequipa', 'Lima'], 'About 20,000 people died in Yungay and Ranrahirca.'),
         ('Which type of mass movement involves the rotational slip of material along a curved surface?', 'Slumping (rotational slide)', ['Rockfall', 'Soil creep', 'Mudflow'], 'Common in clay cliffs and saturated slopes.'),
         ('In 2018 a landslide-related debris flow struck Montecito, California, shortly after:', 'a wildfire removed vegetation from the hills', ['an earthquake in the Pacific', 'a drought ended suddenly in the Sahara', 'a volcanic eruption nearby'], 'Burned slopes have low infiltration and little root cohesion.')],
  why=[('Explain how heavy rainfall can trigger landslides.', 'Water infiltrates and raises pore-water pressure, reducing friction and cohesion (shear strength), while adding weight that increases shear stress; when stress exceeds strength the slope fails.'),
       ('Explain how human activity can increase the risk of mass movement.', 'Undercutting slopes for roads and buildings, deforestation removing root cohesion, adding weight (buildings, waste tips), leaking water pipes and quarrying all reduce slope stability, e.g. hillside favelas in Rio de Janeiro.'),
       ('Explain why avalanches are most common on slopes of about 30-45°.', 'Snow accumulates and forms weak layers on these slopes; steeper slopes shed snow frequently in small amounts, while gentler slopes lack the gravitational force to trigger large slides.'),
       ('Explain why earthquakes often trigger landslides in mountainous regions.', 'Ground shaking temporarily increases shear stress and can cause liquefaction or loosening of regolith on steep slopes, e.g. tens of thousands of landslides after the 2008 Sichuan and 2015 Gorkha earthquakes.')],
  contrast=[('shear strength', 'shear stress', 'Shear strength is the resistance of slope material to movement; shear stress is the force acting to move material downslope - failure occurs when stress exceeds strength.'),
            ('slow mass movements', 'rapid mass movements', 'Slow movements such as soil creep move millimetres a year and rarely threaten life; rapid ones such as rockfalls, debris flows and avalanches move metres per second and are highly hazardous.')],
  misc=[('Landslides only happen on very steep mountain slopes.', 'Landslides also occur on moderate slopes of weak, saturated material and on human-made slopes such as spoil tips (Aberfan, 1966).'),
        ('Planting vegetation always stops landslides.', 'Roots increase cohesion near the surface, but deep-seated failures and intense rainfall can still cause landslides on vegetated slopes.'),
        ('Avalanches are caused only by skiers.', 'Most are triggered naturally by heavy snowfall, wind loading and warming, though people trigger many fatal avalanches.')],
  apply=[('Using a named example, explain the causes of a mass movement event.', 'e.g. Aberfan, Wales (1966): a colliery spoil tip built over springs became saturated after heavy rain; the liquefied waste flowed downhill into a school, killing 144 people, 116 of them children.', 4),
         ('Suggest two methods to reduce landslide risk on slopes above a city.', 'Drainage to lower pore-water pressure; retaining walls and soil nailing (as in Hong Kong); re-vegetation; land-use zoning that prevents building on unstable slopes; early warning based on rainfall thresholds.', 2)],
  cases=[('the 1966 Aberfan disaster, Wales', 'a saturated colliery spoil tip flowed into the village, killing 144 people', 'human factors in mass movement', 'building a waste tip over springs on a slope created a disaster'),
         ('the 1970 Huascarán avalanche, Peru', 'an earthquake loosened ice and rock that fell from Huascarán and buried Yungay, killing about 20,000 people', 'earthquake-triggered mass movement', 'shaking released a huge mass of ice and rock that travelled at very high speed'),
         ('Hong Kong\'s slope safety programme', 'since 1977 the Geotechnical Engineering Office has upgraded thousands of man-made slopes, sharply reducing landslide deaths', 'management of landslide risk', 'engineering, mapping and warnings can reduce risk on steep urban slopes'),
         ('the 2022 Petrópolis floods and landslides, Brazil', 'about 250 mm of rain in three hours triggered landslides that killed over 230 people in hillside neighbourhoods', 'the interaction of rainfall and urbanisation in landslides', 'intense rain on steep slopes with informal housing produced deadly failures')],
  evaluate=[('Human activity is now the main cause of mass movement hazards.', ['undercutting, deforestation and informal hillside settlement raise risk (Petrópolis, Rio)', 'spoil tips and mining (Aberfan)'], ['earthquakes, intense rainfall and snow are natural triggers (Huascarán, Sichuan)', 'many landslides occur in uninhabited mountains'], 'Natural processes trigger mass movements, but human activity increasingly determines where they become disasters.'),
            ('Engineering is the most effective way to manage landslide risk.', ['Hong Kong\'s slope programme cut deaths dramatically', 'drainage and retaining walls address causes'], ['expensive; not affordable for poor communities', 'land-use planning and warnings may be more cost-effective'], 'Engineering works best for high-value urban slopes; planning and warnings are essential elsewhere.')],
  extended=[('Explain the physical and human factors that cause mass movements.', 'Slope angle, geology, weathering, water/pore pressure, vegetation, earthquakes, snow; human undercutting, loading, deforestation, drainage changes; examples (Aberfan, Huascarán, Petrópolis).', 10, 'long')],
  res=[('Table: rainfall and landslides in Hong Kong - years with over 300 mm in 24 hours at the observatory are followed by many landslide reports; 2008: 620 mm in one day, over 2,400 reported landslides; 1997: 245 mm, about 300 landslides.',
        [('Describe the relationship suggested by the data.', 'Higher maximum daily rainfall is associated with many more landslides - over 2,400 after 620 mm compared with about 300 after 245 mm.'),
         ('Explain why rainfall intensity matters for landslides.', 'Intense rain raises pore-water pressure faster than water can drain, reducing shear strength and triggering failures.')]),
       ('Slope stability data for a cutting - shear strength 85 kPa; shear stress 70 kPa; after rainfall shear strength falls by 25%.',
        [('Calculate the factor of safety before and after rainfall.', f'Before 85/70 = {85 / 70:.2f}; after {85 * 0.75:.2f}/70 = {85 * 0.75 / 70:.2f}'),
         ('State and explain whether the slope is likely to fail.', f'Yes - FS falls to {85 * 0.75 / 70:.2f} (< 1), so shear stress exceeds shear strength.')])])

S('ch02-st1', gens=['magnitude', 'gutenberg', 'pct_hazard'],
  terms=[('hazard magnitude', 'the size or energy of a hazard event, measured for example by Mw for earthquakes or VEI for eruptions'),
         ('hazard frequency', 'how often a hazard event of a given magnitude occurs in an area'),
         ('recurrence interval', 'the average time between events of a given magnitude, calculated as (n + 1)/m from a ranked record'),
         ('spatial extent', 'the size of the area affected by a hazard event'),
         ('predictability', 'the extent to which the timing, location and size of a hazard event can be forecast'),
         ('speed of onset', 'the time between the start of a hazard event and its peak impact, from seconds (earthquakes) to weeks (some eruptions)')],
  facts=[('Which relationship between hazard magnitude and frequency is usually observed?', 'High-magnitude events are much less frequent than low-magnitude events', ['High-magnitude events are more frequent', 'Magnitude and frequency are unrelated', 'All magnitudes occur equally often'], 'This inverse relationship is described by the Gutenberg-Richter law for earthquakes.'),
         ('Which geophysical hazard is generally the most predictable in timing?', 'Volcanic eruptions at monitored volcanoes', ['Earthquakes', 'Rockfalls', 'Snow avalanches on unmonitored slopes'], 'Precursors such as tremors, ground swelling and gas emissions often precede eruptions.'),
         ('Which hazard usually has the most rapid speed of onset?', 'An earthquake', ['A drought', 'A slow-moving lava flow', 'Soil creep'], 'Shaking reaches its peak within seconds.'),
         ('The 2004 Indian Ocean tsunami had a very large spatial extent because:', 'tsunami waves crossed the ocean and affected 14 countries', ['the earthquake lasted only one second', 'it occurred on land', 'it was caused by a lava flow'], 'Around 230,000 people died from Indonesia to Somalia.')],
  why=[('Explain why earthquakes are less predictable than volcanic eruptions.', 'Stress builds silently on faults with no reliable short-term precursors, whereas magma movement produces measurable signs such as tremors, deformation and SO₂ emissions before many eruptions.'),
       ('Explain why spatial extent affects the scale of a hazard event\'s impacts.', 'The larger the area affected, the more people, infrastructure and economic activity are exposed, and the harder it is to organise relief over a wide region, e.g. the 2004 tsunami across 14 countries.'),
       ('Explain how speed of onset influences the impacts of geophysical hazards.', 'Rapid-onset hazards such as earthquakes and landslides give little or no warning time to evacuate, so deaths are often high; slower onset allows warnings and evacuation, e.g. Pinatubo 1991.'),
       ('Explain why recurrence intervals should be used with caution in planning.', 'They are averages from short, incomplete records; events are not regular, and a "1-in-100-year" event can occur in successive years; climate or land-use change can alter frequency.')],
  contrast=[('magnitude', 'frequency', 'Magnitude is the size or energy of a single event; frequency is how often events of a given size occur - the two are inversely related.'),
            ('a forecast', 'a prediction', 'A forecast gives the probability of an event over a period and area (e.g. 30-year earthquake probabilities); a prediction states the specific time, place and size, which is not yet possible for earthquakes.')],
  misc=[('A 1-in-100-year earthquake will not happen again for 100 years.', 'Recurrence intervals are averages; the probability of such an event is about 1% in any year, regardless of when the last one occurred.'),
        ('Small earthquakes release pressure and prevent large ones.', 'Small earthquakes release only a tiny fraction of the energy of large ones (each unit of Mw is about 32 times more energy).'),
        ('All geophysical hazards are rapid-onset events.', 'Some volcanic eruptions build over weeks or months and some landslides creep slowly before failing.')],
  apply=[('Using the hazard characteristics of magnitude, frequency, extent and predictability, compare earthquakes and volcanic eruptions.', 'Earthquakes: rapid onset, unpredictable, extent depends on magnitude and depth; eruptions: often preceded by precursors, extent depends on VEI and wind (ash), lahars along valleys; both show inverse magnitude-frequency relationships.', 4),
         ('Suggest why the Cascadia subduction zone is a concern even though no great earthquake has occurred there since 1700.', 'Strain is accumulating on a locked megathrust; geological evidence shows Mw 9 events roughly every 300-500 years; a long gap means stored energy, not safety.', 2)],
  cases=[('the 1700 Cascadia earthquake', 'a Mw 9 earthquake recorded by a tsunami in Japan and drowned forests in Washington State; recurrence is estimated at about 300-500 years', 'magnitude-frequency relationships', 'great earthquakes recur on long, irregular intervals, so long records are needed to estimate risk'),
         ('the 2004 Indian Ocean tsunami', 'waves generated by a Mw 9.1 earthquake reached 14 countries and killed about 230,000 people', 'spatial extent of hazards', 'a single event can affect an entire ocean basin'),
         ('the 1991 Pinatubo eruption', 'monitoring of earthquakes, gas and ground swelling allowed a successful forecast and evacuation', 'predictability of eruptions', 'precursors allowed warnings days before the climactic eruption'),
         ('the 2009 L\'Aquila earthquake, Italy', 'a Mw 6.3 earthquake killed 309 people after experts were accused of giving false reassurance', 'the limits of earthquake prediction', 'foreshocks did not allow scientists to predict the main shock reliably')],
  evaluate=[('Hazard magnitude is more important than frequency in determining hazard risk.', ['high-magnitude events cause most deaths and losses (Tōhoku, Sumatra)', 'they exceed the capacity of defences'], ['frequent small events cause cumulative damage and losses', 'frequency affects preparedness and perception'], 'Both matter: rare high-magnitude events dominate losses, but frequency shapes preparedness and long-term costs.'),
            ('Geophysical hazards will never be accurately predicted.', ['no reliable short-term earthquake precursors', 'complex non-linear systems'], ['volcanic eruptions are increasingly forecast (Pinatubo)', 'early-warning systems give seconds to minutes of warning'], 'Eruptions are partly predictable; earthquakes can be forecast probabilistically but not predicted.')],
  extended=[('Explain how the characteristics of geophysical hazards influence their impacts.', 'Magnitude, frequency, duration, speed of onset, spatial extent and predictability; contrasting examples such as Tōhoku 2011, Pinatubo 1991 and Huascarán 1970.', 10, 'long')],
  res=[('Table: number of earthquakes per year worldwide (USGS averages) - Mw 8+: 1; Mw 7-7.9: 15; Mw 6-6.9: 134; Mw 5-5.9: 1,319.',
        [('Calculate how many times more frequent Mw 5-5.9 earthquakes are than Mw 7-7.9 earthquakes.', f'1,319 / 15 = {1319 / 15:.0f} times'),
         ('Describe the magnitude-frequency relationship shown.', 'An inverse relationship: each one-unit increase in magnitude is roughly ten times less frequent.')]),
       ('Record: in a 120-year record for a volcano, eruptions of VEI 3 or above occurred 5 times.',
        [('Calculate the recurrence interval of VEI 3+ eruptions using (n + 1)/m.', f'(120 + 1)/5 = {121 / 5:.1f} years'),
         ('Calculate the annual probability of such an eruption.', f'1/24.2 × 100 = {100 / 24.2:.1f}%')])])

S('ch02-st2', gens=['tsunami', 'vei', 'deathrate'],
  terms=[('primary hazard', 'a hazard produced directly by the geophysical event, such as ground shaking, lava flows or pyroclastic flows'),
         ('secondary hazard', 'a hazard triggered by the primary event, such as a tsunami, landslide, lahar, liquefaction or fire'),
         ('lahar', 'a volcanic mudflow of ash, rock and water, often from melted snow and ice or heavy rain, which flows along river valleys'),
         ('tsunami', 'a series of long-wavelength ocean waves caused by the sudden displacement of water, usually by a sub-sea earthquake'),
         ('liquefaction', 'the loss of strength of saturated, loose sediments during shaking so that they behave like a liquid'),
         ('pyroclastic flow', 'a ground-hugging current of hot gas and volcanic fragments moving at over 100 km/h at temperatures over 500 °C')],
  facts=[('In 1985, a lahar from Nevado del Ruiz destroyed which Colombian town?', 'Armero', ['Medellín', 'Pasto', 'Cali'], 'About 23,000 of Armero\'s 29,000 people died.'),
         ('The 79 CE eruption of Vesuvius destroyed Pompeii mainly through:', 'pyroclastic flows and surges', ['lava flows', 'a tsunami', 'liquefaction'], 'Hot ash and gas killed people within minutes.'),
         ('Which secondary hazard caused most deaths in the 2011 Tōhoku disaster?', 'Tsunami', ['Ground shaking', 'Liquefaction', 'Fire'], 'Over 90% of the roughly 18,500 deaths were from drowning.'),
         ('Liquefaction caused severe damage in which city in 2011?', 'Christchurch, New Zealand', ['Kathmandu, Nepal', 'Lima, Peru', 'Naples, Italy'], 'Eastern suburbs built on sands and silts were badly affected.')],
  why=[('Explain why tsunami waves increase in height as they approach the coast.', 'Wave speed depends on depth (√(gd)); as depth decreases, waves slow, wavelength shortens and energy is compressed into a smaller volume, so height increases (shoaling).'),
       ('Explain how a volcanic eruption can generate a lahar.', 'Heat from the eruption melts snow and glacier ice, or heavy rain falls on loose ash; the water mixes with tephra to form a dense slurry that flows down valleys at high speed, as at Nevado del Ruiz in 1985.'),
       ('Explain why liquefaction occurs during earthquakes.', 'Shaking increases pore-water pressure in saturated, loose sand and silt; grains lose contact so the sediment loses strength and behaves like a liquid, causing buildings to sink or tilt and sand boils to form.'),
       ('Explain why secondary hazards can cause more deaths than the primary hazard.', 'They may affect much larger areas (tsunami), arrive after people think the danger has passed, travel far from the source (lahars) and destroy infrastructure needed for rescue (fires, landslides).')],
  contrast=[('a pyroclastic flow', 'a lahar', 'A pyroclastic flow is a hot current of gas and fragments that moves extremely fast during an eruption; a lahar is a cooler mudflow of water and debris that follows valleys and can occur during or long after an eruption.'),
            ('primary hazards', 'secondary hazards', 'Primary hazards come directly from the event (shaking, lava, ash fall); secondary hazards are triggered by it (tsunami, lahars, landslides, liquefaction, fires).')],
  misc=[('A tsunami is a single giant wave.', 'A tsunami is a series of waves, often arriving tens of minutes apart, and later waves can be larger.'),
        ('The sea always rises first when a tsunami arrives.', 'Often the sea first withdraws (drawdown) when a wave trough arrives first, which can draw people onto the exposed seabed.'),
        ('Lahars only occur during eruptions.', 'Rain can remobilise ash deposits for years afterwards, as happened around Pinatubo for over a decade.')],
  apply=[('Using a named example, explain how secondary hazards increased the impacts of an earthquake.', 'e.g. Tōhoku 2011: the Mw 9.1 earthquake generated a tsunami up to about 40 m high that overtopped sea walls, killing most of the roughly 18,500 victims, and caused the Fukushima Daiichi nuclear meltdowns.', 4),
         ('Suggest why the deaths at Armero in 1985 were described as avoidable.', 'Hazard maps had shown Armero on lahar paths, but warnings were not acted on; evacuation was not ordered and communications failed at night.', 3)],
  cases=[('the 1985 Nevado del Ruiz lahar, Colombia', 'a relatively small eruption (VEI 3) melted summit ice and lahars buried Armero 74 km away, killing about 23,000 people', 'secondary volcanic hazards', 'meltwater lahars travelled far down valleys, so a small eruption had huge impacts'),
         ('the 2011 Tōhoku tsunami, Japan', 'waves up to about 40 m high overtopped sea walls and killed most of the roughly 18,500 victims', 'tsunamis as secondary hazards', 'the tsunami caused far more deaths than the ground shaking'),
         ('the 2018 Palu earthquake and tsunami, Indonesia', 'a Mw 7.5 earthquake triggered a tsunami, landslides and widespread liquefaction that swallowed whole neighbourhoods, killing over 4,300 people', 'multiple secondary hazards', 'liquefaction and tsunami combined with shaking to cause disaster'),
         ('the 2022 Hunga Tonga-Hunga Ha\'apai eruption', 'an explosive submarine eruption generated a Pacific-wide tsunami and an atmospheric pressure wave', 'volcanic tsunamis', 'explosive interaction of magma and seawater displaced water and air on a global scale')],
  evaluate=[('Secondary hazards are more dangerous than primary hazards.', ['tsunamis caused most deaths in 2004 and 2011', 'lahars killed 23,000 at Armero'], ['ground shaking and building collapse caused most deaths in Haiti 2010 and Türkiye 2023', 'pyroclastic flows are primary and extremely deadly'], 'It depends on the event: secondary hazards dominate for coastal and ice-capped settings, primary shaking for inland urban earthquakes.'),
            ('Tsunamis are the most destructive geophysical hazard.', ['ocean-wide extent and high death tolls (2004)', 'major economic losses (Tōhoku, about US$235 billion)'], ['infrequent compared with earthquake shaking', 'warnings and evacuation can reduce deaths'], 'Tsunamis are among the most destructive, but shaking causes more deaths over time.')],
  extended=[('Explain the formation and impacts of two secondary hazards associated with geophysical events.', 'e.g. tsunami (water displacement, shoaling, Tōhoku 2011) and lahars (meltwater, Armero 1985) or liquefaction (Christchurch 2011); impacts on people and environment.', 10, 'long')],
  res=[('Data: a tsunami travels across ocean 4,000 m deep. Use v = √(gd) with g = 9.8 m/s².',
        [('Calculate the speed of the tsunami in km/h.', f'v = √(9.8 × 4,000) = {math.sqrt(9.8 * 4000):.0f} m/s ≈ {math.sqrt(9.8 * 4000) * 3.6:.0f} km/h'),
         ('Explain why this speed matters for warning systems.', 'At about 700 km/h a tsunami crosses an ocean in hours, so warnings must be issued within minutes for nearby coasts but allow time for distant coasts to evacuate.')]),
       ('Table: deaths by cause, 2011 Tōhoku disaster (approximate) - drowning 90%; crushing and injury 4%; burns 1%; other/unknown 5%; total about 18,500 dead and missing.',
        [('Calculate the approximate number of deaths caused by drowning.', f'90% of 18,500 = {0.9 * 18500:,.0f}'),
         ('Suggest why so few deaths were caused by shaking.', 'Strict building codes and seismic engineering meant few buildings collapsed; the tsunami, a secondary hazard, overwhelmed sea walls.')])])

S('ch02-st3', gens=['density', 'risk', 'pct_hazard'],
  terms=[('exposure', 'the people, property and infrastructure located in an area that could be affected by a hazard'),
         ('building quality', 'the extent to which structures are designed and constructed to resist hazards, e.g. through seismic codes'),
         ('informal settlement', 'housing built without planning permission or legal tenure, often on hazardous land such as steep slopes or floodplains'),
         ('land-use planning', 'the regulation of where and how different activities may be developed in order to reduce exposure to hazards'),
         ('soft-storey building', 'a building with an open ground floor (shops, parking) that is weak and prone to collapse in earthquakes')],
  facts=[('Which factor contributed most to deaths in the 2023 Kahramanmaraş earthquakes in Türkiye?', 'Poor enforcement of building codes', ['A tsunami', 'A volcanic eruption', 'Lava flows'], 'Tens of thousands of buildings collapsed despite modern codes on paper.'),
         ('Rapid urbanisation increases hazard risk mainly because it:', 'concentrates more people and buildings in exposed locations', ['reduces the frequency of earthquakes', 'moves cities away from faults', 'reduces seismic wave speed'], 'Many megacities such as Istanbul, Tehran and Manila lie near active faults.'),
         ('Mexico City suffers amplified earthquake shaking because it is built on:', 'soft lake-bed sediments', ['solid granite', 'a hotspot', 'permafrost'], 'Shaking in 1985 and 2017 was amplified on the old lake bed.'),
         ('Which megacity has a high probability of a large earthquake on the North Anatolian Fault?', 'Istanbul', ['Cairo', 'Paris', 'Moscow'], 'Studies estimate a significant chance of a Mw 7+ event within decades.')],
  why=[('Explain how rapid urbanisation can increase earthquake risk.', 'Rapid growth leads to dense informal housing, poorly built multi-storey blocks, building on unstable land and limited enforcement of codes, so more people are exposed and buildings are more likely to collapse.'),
       ('Explain why local geology affects the human impacts of earthquakes.', 'Soft, water-saturated sediments amplify seismic waves and may liquefy, so buildings on them suffer more damage than those on bedrock, e.g. Mexico City in 1985 and 2017.'),
       ('Explain why poorer people are often concentrated on the most hazardous land.', 'Hazardous land such as steep slopes and floodplains is cheap or unclaimed; the poor cannot afford safer locations, so informal settlements grow there, e.g. hillside favelas in Rio and Petrópolis.'),
       ('Explain how land use can increase the risk from volcanic hazards.', 'Fertile volcanic soils attract farming and settlement close to volcanoes; towns built on valley floors lie on lahar paths; tourism brings visitors close to vents (Whakaari/White Island 2019).')],
  contrast=[('exposure', 'vulnerability', 'Exposure is the presence of people and assets in a hazard zone; vulnerability is their susceptibility to harm, which depends on factors such as building quality, wealth and preparedness.'),
            ('formal housing', 'informal housing', 'Formal housing is planned, legally built and inspected under building codes; informal housing is self-built without permission or inspection, often on hazardous land and with weak materials.')],
  misc=[('Earthquakes kill people directly.', 'Most deaths are caused by collapsing buildings and secondary hazards, not by ground shaking itself - "earthquakes don\'t kill people, buildings do".'),
        ('High population density always means high death tolls.', 'Dense cities with good building codes and preparedness, such as Tokyo, can have relatively low death tolls.'),
        ('Building codes guarantee safety.', 'Codes only work when enforced; in Türkiye in 2023 amnesties for illegal construction left many unsafe buildings.')],
  apply=[('Using a named city, explain how human factors increase its exposure to geophysical hazards.', 'e.g. Istanbul: about 16 million people near the North Anatolian Fault; many illegally built or older concrete apartment blocks; dense historic districts with narrow streets that hinder rescue; building amnesties.', 4),
         ('Suggest why Kathmandu suffered heavy damage in the 2015 Gorkha earthquake.', 'Rapid growth of unregulated multi-storey buildings on soft lake sediments, old brick and timber heritage buildings and poor code enforcement.', 3)],
  cases=[('the 2023 Kahramanmaraş earthquakes, Türkiye', 'more than 160,000 buildings collapsed or were badly damaged, partly because building amnesties legalised unsafe construction', 'building quality and risk', 'weak enforcement of codes turned a natural event into a disaster'),
         ('Mexico City', 'the 1985 earthquake killed about 10,000 people, mostly in mid-rise buildings on the old lake bed', 'the amplification of shaking by soft sediments', 'local geology combined with dense urban development to raise risk'),
         ('Kathmandu, Nepal', 'the 2015 Gorkha earthquake killed about 9,000 people in Nepal and destroyed or damaged about 800,000 houses', 'rapid unplanned urbanisation and risk', 'poorly built housing and soft sediments in a fast-growing city increased damage'),
         ('Istanbul, Türkiye', 'about 16 million people live close to the North Anatolian Fault, which has ruptured westward in a sequence of earthquakes since 1939', 'megacity exposure to seismic hazards', 'concentrated population and older buildings create very high potential losses')],
  evaluate=[('Human factors are more important than physical factors in determining geophysical hazard risk.', ['building quality explains differences between Chile 2010 and Haiti 2010', 'land-use choices determine exposure'], ['magnitude and depth determine potential energy', 'secondary hazards such as tsunamis can overwhelm even good defences (Tōhoku)'], 'Physical factors set the hazard, but human factors largely determine whether it becomes a disaster.'),
            ('Rapid urbanisation is the greatest cause of rising geophysical hazard risk.', ['more people in megacities on faults', 'informal settlement on unstable slopes'], ['poverty, governance and corruption also matter', 'urbanisation can bring better buildings and services'], 'Urbanisation increases exposure, but whether it raises risk depends on governance and building standards.')],
  extended=[('Explain how human factors influence the level of risk from geophysical hazards.', 'Population density and urbanisation, land use, building quality and codes, informal settlement, wealth, governance and corruption; examples (Türkiye 2023, Kathmandu 2015, Mexico City 1985).', 10, 'long')],
  res=[('Table: two districts of a city near a fault - District A: 48,000 people on 3.2 km², 60% of buildings pre-code; District B: 25,000 people on 6.5 km², 15% pre-code.',
        [('Calculate the population density of each district.', f'A: 48,000/3.2 = {48000 / 3.2:,.0f} per km²; B: 25,000/6.5 = {25000 / 6.5:,.0f} per km²'),
         ('Suggest which district has the higher earthquake risk and why.', 'District A: it has about four times the density and a much higher share of buildings constructed before seismic codes, so exposure and vulnerability are both higher.')]),
       ('Map description: a hazard map of a volcano shows lahar paths along three river valleys; two towns lie on the valley floors 20-50 km downstream; a third town lies on a ridge.',
        [('Identify which settlements are most at risk from lahars.', 'The two towns on the valley floors, because lahars are channelled along river valleys.'),
         ('Suggest one land-use planning measure to reduce risk.', 'Zoning to prevent new building on valley floors and relocating key services to higher ground, with evacuation routes to the ridge.')])])

S('ch03-st1', gens=['risk', 'deathrate', 'spearman_hazard'],
  terms=[('vulnerability', 'the characteristics of a person or community that affect their ability to anticipate, cope with, resist and recover from a hazard'),
         ('capacity', 'the strengths and resources of a community, such as money, organisation, knowledge and infrastructure, that reduce risk'),
         ('hazard risk', 'the probability of harmful consequences from a hazard, often expressed as risk = hazard × vulnerability / capacity'),
         ('disaster', 'a hazard event causing widespread loss of life or damage that exceeds a community\'s ability to cope using its own resources'),
         ('resilience', 'the ability of a community to resist, absorb and recover from the effects of a hazard in a timely way'),
         ('Pressure and Release (PAR) model', 'a model showing disaster as the outcome of pressures from vulnerability (root causes, dynamic pressures, unsafe conditions) meeting a hazard')],
  facts=[('In the risk equation, increasing community capacity will:', 'reduce risk', ['increase risk', 'have no effect on risk', 'increase hazard magnitude'], 'Capacity is the denominator in risk = hazard × vulnerability / capacity.'),
         ('In the Pressure and Release model, "root causes" include:', 'limited access to power, resources and political systems', ['plate tectonics only', 'unstable slopes', 'the earthquake magnitude'], 'Root causes lead through dynamic pressures to unsafe conditions.'),
         ('Which group is usually most vulnerable during geophysical disasters?', 'The elderly, the poor, women, children and people with disabilities', ['Wealthy middle-aged adults', 'Government officials', 'Tourists in luxury hotels'], 'Social vulnerability depends on age, gender, health and income.'),
         ('A hazard becomes a disaster when:', 'it exceeds the community\'s capacity to cope', ['its magnitude exceeds 6', 'it occurs at night', 'it is recorded by satellites'], 'The same event can be a disaster in one place but not another.')],
  why=[('Explain why the same magnitude of hazard can produce very different levels of risk in different places.', 'Risk depends on vulnerability and capacity as well as the hazard: wealthier places with codes, preparedness and resources can reduce losses, whereas poverty, weak governance and poor housing magnify them.'),
       ('Explain how the Pressure and Release model helps explain disasters.', 'It shows disasters result from vulnerability progressing from root causes (poverty, power) via dynamic pressures (rapid urbanisation, lack of training) to unsafe conditions (fragile housing), which meet a hazard; reducing these pressures "releases" the risk.'),
       ('Explain why women are often more vulnerable than men in disasters.', 'Social roles may keep them at home caring for children; lower literacy and access to warnings in some societies; restrictive clothing or norms; and lower income and property rights affect recovery, e.g. women made up a majority of deaths in parts of Aceh in 2004.'),
       ('Explain how increasing capacity reduces hazard risk.', 'Resources such as education, early warning systems, emergency services, insurance and strong governance help communities prepare, respond and recover, reducing the denominator in the risk equation.')],
  contrast=[('vulnerability', 'capacity', 'Vulnerability is the susceptibility of people to harm; capacity is the resources and abilities that allow them to resist and recover - risk rises with vulnerability and falls with capacity.'),
            ('a hazard', 'a disaster', 'A hazard is a potential threat from a natural event; a disaster occurs when the event causes losses that exceed the community\'s ability to cope.')],
  misc=[('Disasters are caused only by extreme natural events.', 'Disasters result when hazards meet vulnerable populations; human factors such as poverty and poor governance are central.'),
        ('Vulnerability only depends on wealth.', 'It also depends on age, gender, disability, education, governance, social networks and location.'),
        ('Risk cannot be reduced unless the hazard is controlled.', 'Most risk reduction works by reducing vulnerability and increasing capacity, since hazards themselves are rarely controllable.')],
  apply=[('Use the Pressure and Release model to explain a named disaster.', 'e.g. Haiti 2010: root causes - colonial debt, poverty, weak state; dynamic pressures - rapid urbanisation of Port-au-Prince, lack of building codes and training; unsafe conditions - unreinforced concrete housing on slopes; hazard - Mw 7.0 shallow earthquake close to the capital.', 4),
         ('Suggest two ways a local government could increase community capacity.', 'Training community response teams and drills; funding early warning systems; enforcing building codes; providing emergency supplies; public education.', 2)],
  cases=[('the 2010 Haiti earthquake', 'a Mw 7.0 earthquake near Port-au-Prince killed an estimated 100,000-316,000 people', 'vulnerability in disasters', 'poverty, weak governance and unreinforced buildings magnified the impact'),
         ('the 2004 Indian Ocean tsunami in Aceh', 'in some villages women died at about three to four times the rate of men', 'gendered vulnerability', 'social roles and lower ability to swim or climb increased women\'s vulnerability'),
         ('the 2016 Kaikōura earthquake, New Zealand', 'a Mw 7.8 earthquake killed only 2 people, helped by strong codes, low density and good emergency services', 'capacity and risk', 'high capacity limited losses from a large earthquake'),
         ('the 2023 Al Haouz earthquake, Morocco', 'a Mw 6.8 earthquake killed about 2,960 people, mostly in remote Atlas mountain villages of mud-brick houses', 'rural vulnerability', 'isolation and traditional building materials raised vulnerability and delayed rescue')],
  evaluate=[('Vulnerability is more important than the physical hazard in determining disaster impacts.', ['Haiti vs Chile 2010', 'PAR model shows root causes of disasters'], ['very large events overwhelm capacity even in rich countries (Tōhoku)', 'hazard magnitude limits what preparation can achieve'], 'Vulnerability largely explains differences in impacts, but extreme hazards can overwhelm any society.'),
            ('The risk equation (risk = hazard × vulnerability / capacity) is a useful tool for hazard management.', ['identifies what can be changed (vulnerability, capacity)', 'simple framework for comparing places'], ['variables are hard to measure and combine', 'oversimplifies interactions and changes over time'], 'Useful as a conceptual framework, but limited as a precise measurement tool.')],
  extended=[('Explain how vulnerability and capacity influence hazard risk.', 'Risk equation; social, economic, physical, political vulnerability; capacity (wealth, governance, preparedness); PAR model; contrasting examples (Haiti and Chile 2010, Kaikōura 2016).', 10, 'long')],
  res=[('Index scores for two cities (0-10 scale) - City X: hazard 8, vulnerability 7, capacity 3.5; City Y: hazard 8, vulnerability 3, capacity 8.',
        [('Calculate the risk score for each city using risk = hazard × vulnerability / capacity.', f'X: 8 × 7 / 3.5 = {8 * 7 / 3.5:.1f}; Y: 8 × 3 / 8 = {8 * 3 / 8:.1f}'),
         ('Explain why the cities have different risk despite the same hazard.', 'City X has higher vulnerability and lower capacity, so the same hazard produces about five times the risk.')]),
       ('Table: deaths by age group in a coastal district after a tsunami - under 10: 38%; 10-59: 34%; 60 and over: 28%; under-10s and over-60s made up 30% of the population.',
        [('Calculate the share of deaths among people under 10 and over 60.', '38 + 28 = 66% of deaths, compared with 30% of the population.'),
         ('Explain what this suggests about vulnerability.', 'Children and the elderly were more than twice as likely to die as their population share suggests, because they were less able to run, swim or climb to safety.')])])

S('ch03-st2', gens=['deathrate', 'magnitude', 'risk'],
  terms=[('high-income country (HIC)', 'a country with gross national income per capita above the World Bank threshold (about US$14,000 in 2024)'),
         ('low-income country (LIC)', 'a country with gross national income per capita below about US$1,150 (World Bank, 2024)'),
         ('economic loss', 'the monetary value of damage to property, infrastructure and economic activity caused by a disaster'),
         ('insured loss', 'the part of economic losses covered by insurance payouts, usually much higher as a share in HICs'),
         ('death toll', 'the number of people killed by a hazard event, often much higher in lower-income countries')],
  facts=[('The 2010 Haiti earthquake (Mw 7.0) and the 2010 Chile earthquake (Mw 8.8) killed approximately:', 'over 100,000 and about 525 people respectively', ['about 500 and over 100,000 respectively', 'similar numbers of people', 'fewer than 100 people each'], 'Chile released about 500 times more energy but had far fewer deaths.'),
         ('The 2011 Tōhoku disaster is estimated to be the costliest natural disaster in history, at about:', 'US$235 billion', ['US$2 billion', 'US$20 million', 'US$2 trillion'], 'World Bank estimate; much of the loss was uninsured.'),
         ('Economic losses are usually higher in HICs mainly because:', 'property and infrastructure have higher value', ['earthquakes there are always larger', 'they have more volcanoes', 'insurance increases damage'], 'Deaths tend to be higher in LICs, absolute economic losses in HICs.'),
         ('Which country\'s 2015 earthquake led to the loss of about a third of its GDP?', 'Nepal', ['Japan', 'New Zealand', 'Italy'], 'Losses of about US$7 billion compared with GDP of about US$21 billion.')],
  why=[('Explain why deaths from geophysical hazards are usually higher in low-income countries.', 'Poor building quality and lack of enforced codes, informal settlements on hazardous land, weak warning systems, fewer emergency services and health care, and limited capacity for rescue and recovery.'),
       ('Explain why economic losses are often higher in absolute terms in high-income countries.', 'They have high-value buildings, infrastructure and businesses, and disruption to integrated economies and supply chains is costly, e.g. Tōhoku 2011 affected global car and electronics supply chains.'),
       ('Explain why economic losses may be relatively greater for low-income countries.', 'Losses form a much larger share of GDP; little is insured; governments lack reserves and rely on aid and loans, so development is set back for years, e.g. Haiti 2010 (losses of about 120% of GDP).'),
       ('Explain why comparing disasters only by death toll can be misleading.', 'Death tolls ignore economic, social and environmental impacts, injuries and long-term displacement, and data in poorer countries are often uncertain (Haiti estimates range from about 100,000 to 316,000).')],
  contrast=[('the impacts of the 2010 Haiti earthquake', 'the impacts of the 2010 Chile earthquake', 'Haiti (Mw 7.0) had over 100,000 deaths and losses greater than its GDP because of poor buildings and weak governance; Chile (Mw 8.8) had about 525 deaths because of building codes and emergency capacity, though losses were about US$30 billion.'),
            ('absolute economic losses', 'relative economic losses', 'Absolute losses are the total cost in money and are usually highest in HICs; relative losses compare costs with GDP and are often highest in LICs.')],
  misc=[('Rich countries do not suffer disasters.', 'HICs can suffer major disasters, e.g. Tōhoku 2011 (about 18,500 dead) and Kobe 1995 (about 6,400 dead), especially from extreme events.'),
        ('Low-income countries always have smaller economic losses.', 'Absolute losses may be smaller, but relative to GDP they are often much larger.'),
        ('Differences in impact between Haiti and Chile were due to the size of the earthquakes.', 'Chile\'s earthquake was much larger; differences reflect vulnerability and capacity.')],
  apply=[('Compare the impacts of a geophysical disaster in a high-income country and a low-income country.', 'e.g. Christchurch 2011 (185 deaths, about NZ$40 billion losses, mostly insured via EQC) vs Haiti 2010 (100,000+ deaths, 1.5 million homeless, losses about US$7.8 billion with little insurance); explain by codes, governance, preparedness and wealth.', 6),
         ('Suggest why recovery after the 2015 Nepal earthquake was slow.', 'Mountainous terrain and landslides blocked access; political disputes delayed the reconstruction authority; limited funds and skilled labour; monsoon rains.', 3)],
  cases=[('the 2010 Chile earthquake', 'a Mw 8.8 earthquake killed about 525 people despite releasing about 500 times more energy than the Haiti earthquake', 'the influence of development on disaster impacts', 'strict building codes and emergency planning limited deaths in a middle/high-income country'),
         ('the 2010 Haiti earthquake', 'over 100,000 people died and about 1.5 million were made homeless, with losses estimated at about 120% of GDP', 'disasters in low-income countries', 'poverty, weak government and poor building quality magnified impacts'),
         ('the 1995 Kobe earthquake, Japan', 'a Mw 6.9 earthquake killed about 6,400 people and caused about US$100 billion of damage', 'economic losses in high-income countries', 'high-value infrastructure and older buildings led to huge economic costs'),
         ('the 2015 Gorkha earthquake, Nepal', 'about 9,000 people died and losses of about US$7 billion equalled about a third of GDP', 'relative economic loss', 'a lower-income country suffered losses large relative to its economy')],
  evaluate=[('Level of economic development is the most important factor explaining differences in disaster impacts.', ['Haiti vs Chile 2010', 'wealth funds codes, warnings and services'], ['governance and corruption matter (Türkiye 2023, an upper-middle-income country)', 'hazard magnitude and type (Tōhoku tsunami)'], 'Development is a key factor, but governance and the nature of the hazard are also crucial.'),
            ('High-income countries recover more successfully from geophysical disasters than low-income countries.', ['insurance and government funds (Christchurch EQC)', 'faster rebuilding of infrastructure'], ['Christchurch recovery still took over a decade', 'some LICs rebuild community-led with international aid'], 'HICs usually recover faster economically, but recovery is uneven in all countries.')],
  extended=[('Explain why the impacts of geophysical disasters differ between high-income and low-income countries.', 'Contrasting named examples with figures; deaths vs economic losses; building codes, preparedness, governance, insurance, aid; absolute vs relative losses.', 10, 'long')],
  res=[('Table: 2010 earthquakes - Haiti: Mw 7.0, depth 13 km, deaths about 160,000 (mid estimate), population affected 3.5 million; Chile: Mw 8.8, depth 35 km, deaths 525, population affected 1.8 million.',
        [('Calculate deaths per 1,000 people affected in each country.', f'Haiti: 160,000/3,500,000 × 1,000 = {160000 / 3500000 * 1000:.1f}; Chile: 525/1,800,000 × 1,000 = {525 / 1800000 * 1000:.2f}'),
         ('Explain the difference shown.', 'Haiti\'s rate was over 150 times Chile\'s because of poorly built concrete housing, no enforced codes, weak government and limited rescue capacity.')]),
       ('Table: economic losses as % of GDP - Haiti 2010: 120%; Nepal 2015: 33%; Chile 2010: 18%; Japan (Tōhoku) 2011: about 4%.',
        [('Describe the pattern shown.', 'Losses relative to GDP were highest in the lowest-income countries (Haiti, Nepal) and lowest in Japan, the richest.'),
         ('Suggest why Japan\'s absolute losses were nevertheless the highest.', 'Its losses (about US$235 billion) involved very high-value infrastructure, housing and industry, plus the Fukushima nuclear disaster.')])])

S('ch03-st3', gens=['risk', 'pct_hazard', 'deathrate'],
  terms=[('hazard perception', 'the way people view the likelihood and seriousness of a hazard, shaped by experience, culture, education and wealth'),
         ('fatalism', 'the belief that hazards are acts of God or fate and cannot be prevented, so people accept losses'),
         ('risk compensation', 'the tendency to take greater risks when people feel protected, e.g. building behind sea walls'),
         ('non-governmental organisation (NGO)', 'a non-profit organisation independent of government, such as the Red Cross/Red Crescent or Oxfam, that provides aid and builds capacity'),
         ('governance', 'the way decisions are made and implemented by governments and institutions, including laws, enforcement and accountability'),
         ('early warning system', 'a system to detect a hazard and communicate warnings so people can act in time, e.g. Japan\'s J-Alert')],
  facts=[('Which response to hazards involves accepting losses as inevitable?', 'Fatalism', ['Adaptation', 'Mitigation', 'Risk sharing'], 'Other responses include adaptation, prediction and risk sharing.'),
         ('Why do many people continue to live on the slopes of Mount Merapi?', 'Fertile volcanic soils and strong cultural and spiritual ties to the volcano', ['There are no other settlements in Java', 'The volcano is extinct', 'Insurance is compulsory there'], 'The volcano last erupted in 2010, killing about 350 people.'),
         ('Japan\'s J-Alert system is an example of:', 'a national early warning system', ['an NGO', 'a building code', 'a fatalistic response'], 'It sends satellite alerts about earthquakes, tsunamis and missiles.'),
         ('Which organisation co-ordinates international humanitarian response within the UN?', 'OCHA (UN Office for the Coordination of Humanitarian Affairs)', ['the World Trade Organization', 'the IMF', 'OPEC'], 'OCHA works with NGOs and governments after major disasters.')],
  why=[('Explain why people may choose to live in hazardous areas.', 'Economic benefits (fertile soils, tourism, geothermal energy), lack of alternatives, family and cultural ties, low perception of risk or optimism, and belief that technology will protect them.'),
       ('Explain how past experience can affect hazard perception.', 'People who have experienced a hazard may perceive higher risk and prepare more; but long gaps between events lead to complacency, and survivors of small events may underestimate larger ones.'),
       ('Explain why governance affects disaster outcomes.', 'Effective governments enforce codes, fund warning systems and plan evacuations; corruption, weak institutions or conflict reduce enforcement and delay response, as in Türkiye 2023 and Haiti 2010.'),
       ('Explain the role of NGOs in reducing hazard risk.', 'NGOs provide emergency relief and shelter, fund and train community-based preparedness, build safer schools, and advocate for vulnerable groups, often reaching places that governments cannot.')],
  contrast=[('a fatalistic response', 'an adaptive response', 'A fatalistic response accepts losses as inevitable; an adaptive response changes behaviour or the built environment to reduce losses, such as earthquake-resistant homes or evacuation planning.'),
            ('governments', 'NGOs', 'Governments set and enforce laws, fund infrastructure and lead national response; NGOs are independent, often work at community level, and provide relief, training and advocacy.')],
  misc=[('Everyone perceives hazard risk in the same way.', 'Perception varies with experience, culture, religion, education, wealth and personality.'),
        ('More information always leads to safer behaviour.', 'Information must be trusted, understood and acted on; warnings can be ignored, and false alarms create "warning fatigue".'),
        ('NGOs can replace government action in disasters.', 'NGOs complement governments but lack the authority, scale and long-term funding of the state; poor co-ordination can cause problems (Haiti 2010).')],
  apply=[('Using a named example, explain how information and communication reduced the impacts of a hazard.', 'e.g. Pinatubo 1991: PHIVOLCS and USGS monitoring and a five-level alert system led to the evacuation of about 60,000 people, saving an estimated 5,000+ lives.', 4),
         ('Suggest why some residents refused to evacuate during the 2010 Merapi eruption.', 'Fear of losing livestock and property, trust in the spiritual gatekeeper rather than scientists, previous eruptions that were smaller, and lack of alternative income.', 3)],
  cases=[('the 2010 eruption of Mount Merapi, Indonesia', 'about 350 people died, including the spiritual gatekeeper Mbah Maridjan, who refused to leave', 'cultural influences on hazard perception', 'traditional beliefs and attachment to place affected responses to warnings'),
         ('the 1991 eruption of Mount Pinatubo', 'scientific monitoring and a staged alert system led to the evacuation of about 60,000 people', 'the role of information in reducing risk', 'clear communication of scientific forecasts saved thousands of lives'),
         ('the 2009 L\'Aquila earthquake trial, Italy', 'six scientists and an official were convicted of manslaughter in 2012 for reassuring statements, though the scientists were later acquitted', 'risk communication and governance', 'poor communication of uncertainty damaged trust between scientists and the public'),
         ('the 2010 Haiti earthquake response', 'thousands of NGOs arrived, but poor co-ordination and a weak government slowed recovery', 'the role of NGOs and governance', 'NGO help was limited without effective governance and co-ordination')],
  evaluate=[('Hazard perception is the most important factor in determining how people respond to hazards.', ['influences preparedness and evacuation decisions (Merapi)', 'complacency after long quiet periods'], ['poverty limits choices regardless of perception', 'governance determines warnings and codes'], 'Perception shapes behaviour, but wealth and governance constrain what people can do.'),
            ('NGOs are more effective than governments in reducing hazard risk.', ['reach local communities and marginalised groups', 'flexible and trusted'], ['governments set codes, fund infrastructure and co-ordinate at scale', 'NGO aid can be short-term and unco-ordinated (Haiti)'], 'NGOs are most effective working alongside capable governments rather than replacing them.')],
  extended=[('Explain how perception, information and governance influence responses to geophysical hazards.', 'Range of perceptions (fatalism, adaptation, risk compensation); role of warnings and trusted information; governance and NGOs; examples (Pinatubo, Merapi, L\'Aquila, Haiti).', 10, 'long')],
  res=[('Survey results from 200 residents living near a volcano: "eruption likely in next 10 years" - farmers 28 of 80; townspeople 66 of 120. "Would evacuate if ordered" - farmers 44 of 80; townspeople 102 of 120.',
        [('Calculate the percentage of farmers and townspeople who would evacuate if ordered.', f'Farmers 44/80 = {44 / 80 * 100:.0f}%; townspeople 102/120 = {102 / 120 * 100:.0f}%'),
         ('Suggest reasons for the difference.', 'Farmers depend on land and livestock that cannot be moved, have stronger ties to the land and may perceive lower risk; townspeople have fewer assets at risk and more access to information.')]),
       ('Timeline description: before the 1991 Pinatubo eruption, the alert level rose from 1 (2 April) to 3 (7 June), 4 (9 June) and 5 (eruption in progress, 12 June); the climactic eruption was on 15 June.',
        [('State how many days of warning were given between alert level 3 and the climactic eruption.', '7 June to 15 June = 8 days'),
         ('Explain why staged alert levels are useful.', 'They communicate increasing risk simply, allowing progressive evacuation and avoiding the costs of evacuating too early.')])])

S('ch04-st1', gens=['magnitude', 'pswave', 'density'],
  terms=[('hazard mapping', 'mapping areas by their exposure to hazards, such as lahar paths, liquefaction zones or tsunami inundation areas, to guide planning'),
         ('land-use zoning', 'regulating which activities may take place in different zones, e.g. preventing housing in high-risk areas'),
         ('base isolation', 'placing a building on flexible bearings (rubber and steel pads) so that the ground can move without transferring all shaking to the structure'),
         ('earthquake early warning', 'a system that detects P-waves and sends alerts seconds before stronger S- and surface waves arrive, e.g. ShakeAlert'),
         ('retrofitting', 'strengthening existing buildings, e.g. with steel bracing or shear walls, to resist hazards'),
         ('volcano monitoring', 'measuring seismicity, ground deformation, gas emissions and temperature to forecast eruptions')],
  facts=[('ShakeAlert, the earthquake early warning system on the US west coast, works by:', 'detecting P-waves and alerting before damaging waves arrive', ['predicting earthquakes days in advance', 'stopping fault movement', 'measuring tide levels'], 'Warning times are typically seconds to tens of seconds.'),
         ('Which is a feature of earthquake-resistant building design?', 'Cross-bracing and base isolators', ['Heavy concrete roofs', 'Soft-storey open ground floors', 'Unreinforced brick walls'], 'Design aims to absorb and dissipate seismic energy.'),
         ('Tiltmeters and GPS are used to monitor volcanoes because they detect:', 'ground swelling as magma rises', ['ash colour', 'rainfall', 'tidal changes'], 'Inflation of the volcano can indicate magma moving into the chamber.'),
         ('The Taipei 101 skyscraper contains a 660-tonne:', 'tuned mass damper that counteracts swaying', ['water tank for firefighting', 'seismometer that predicts earthquakes', 'lead roof that adds weight'], 'It reduces movement in typhoons and earthquakes.')],
  why=[('Explain how earthquake-resistant design reduces deaths.', 'Base isolation, cross-bracing, shear walls, flexible steel frames and dampers absorb or dissipate energy so buildings sway rather than collapse; since most deaths are from collapse, this greatly reduces casualties.'),
       ('Explain why hazard mapping is an important pre-event strategy.', 'Mapping identifies zones of high risk (fault traces, liquefaction, lahar and tsunami zones) so planners can restrict building, locate key services safely and design evacuation routes.'),
       ('Explain why prediction is more effective for volcanoes than for earthquakes.', 'Rising magma produces measurable precursors such as harmonic tremor, ground deformation and SO₂ emissions, whereas faults give no reliable short-term warning signs.'),
       ('Explain why land-use zoning is often difficult to apply in practice.', 'Land in hazard zones may already be built up, valuable or culturally important; poor people may have no alternative; enforcement is weak in informal settlements; and political pressure favours development.')],
  contrast=[('prediction', 'protection', 'Prediction tries to forecast when and where a hazard will occur so people can be warned; protection reduces damage when it occurs, e.g. by building design or sea walls.'),
            ('new earthquake-resistant buildings', 'retrofitting existing buildings', 'New buildings can incorporate designs such as base isolation from the start at relatively low extra cost; retrofitting strengthens existing buildings but is often expensive and disruptive.')],
  misc=[('Earthquake early warning systems predict earthquakes.', 'They detect earthquakes that have already started and give seconds of warning before strong shaking arrives.'),
        ('Earthquake-resistant buildings are only affordable in rich countries.', 'Low-cost methods exist, such as timber frames, reinforced adobe and confined masonry, promoted by NGOs in Peru and Nepal.'),
        ('Sea walls make coastal settlements completely safe from tsunamis.', 'In 2011 many sea walls in Tōhoku were overtopped; they can also create false security (risk compensation).')],
  apply=[('Using named examples, explain how pre-event management can reduce earthquake risk.', 'e.g. Japan: strict building codes updated after Kobe 1995, base-isolated buildings, school drills on 1 September (Disaster Prevention Day), and earthquake early warning that halted Shinkansen trains in 2011; hazard maps for tsunami evacuation.', 6),
         ('Suggest why hazard maps for volcanoes need regular updating.', 'Vents and lahar paths change after eruptions; settlement expands; new monitoring data improve understanding of hazard zones.', 2)],
  cases=[('Japan\'s earthquake preparedness', 'building codes strengthened after 1981 and 1995, early warning and national drills limited building collapse in 2011', 'pre-event management in a high-income country', 'investment in design, warnings and education reduced deaths from shaking'),
         ('the ShakeAlert system, USA', 'the West Coast system since 2019 sends alerts to phones in California, Oregon and Washington seconds before strong shaking', 'earthquake early warning', 'detecting P-waves gives time to stop trains, open fire-station doors and take cover'),
         ('the Mount Vesuvius red zone, Italy', 'about 700,000 people live in the red zone, with an evacuation plan and incentives to move', 'hazard mapping and zoning', 'mapping informs evacuation planning where relocation is politically difficult'),
         ('low-cost housing in Nepal after 2015', 'NGOs trained masons in earthquake-resistant techniques such as horizontal timber bands and reinforced corners', 'low-cost building design', 'appropriate technology can reduce vulnerability without high costs')],
  evaluate=[('Building design is the most effective way to reduce earthquake risk.', ['most deaths come from collapse', 'Japan and Chile show codes work'], ['useless without enforcement (Türkiye)', 'cannot prevent tsunami deaths; warnings and education also needed'], 'Building design is the single most important measure, but it must be enforced and combined with warnings and planning.'),
            ('Prediction is more important than preparation in managing volcanic hazards.', ['Pinatubo evacuation saved thousands', 'monitoring gives warning time'], ['predictions are uncertain and false alarms cause distrust', 'preparation (plans, education, zoning) is needed to act on warnings'], 'Prediction is only effective when combined with preparation and trusted communication.')],
  extended=[('Explain how pre-event strategies can reduce the risk from geophysical hazards.', 'Monitoring and prediction, early warning, hazard mapping, land-use zoning, building design and retrofitting, education and drills; examples (Japan, ShakeAlert, Pinatubo, Vesuvius).', 10, 'long')],
  res=[('Data: an early warning station 40 km from an epicentre detects P-waves (6 km/s); S-waves travel at 3.5 km/s. A city lies 120 km from the epicentre.',
        [('Calculate the time taken for S-waves to reach the city.', f'120 / 3.5 = {120 / 3.5:.1f} s'),
         ('Calculate the warning time for the city if the alert is issued 5 seconds after the P-wave reaches the station.', f'P arrives at the station at 40/6 = {40 / 6:.1f} s; alert at {40 / 6 + 5:.1f} s; warning = {120 / 3.5:.1f} − {40 / 6 + 5:.1f} = {120 / 3.5 - 40 / 6 - 5:.1f} s')]),
       ('Table: building damage in a 2010s earthquake by construction type - unreinforced masonry: 62% collapsed; non-ductile concrete frame: 31%; reinforced concrete to modern code: 4%; timber frame: 2%.',
        [('How many times more likely to collapse were unreinforced masonry buildings than modern reinforced concrete?', f'62 / 4 = {62 / 4:.1f} times'),
         ('Explain the differences shown.', 'Unreinforced masonry is heavy and brittle; modern code concrete and timber are ductile and flex without collapsing.')])])

S('ch04-st2', gens=['deathrate', 'pct_hazard', 'risk'],
  terms=[('emergency response', 'the immediate actions after a disaster to save lives and meet basic needs, such as search and rescue, medical care, shelter, water and food'),
         ('the golden 72 hours', 'the period after an earthquake within which most trapped survivors can be rescued alive'),
         ('recovery', 'the restoration of services, livelihoods and infrastructure after a disaster, over months to years'),
         ('reconstruction', 'rebuilding housing and infrastructure after a disaster, ideally to a higher standard ("build back better")'),
         ('build back better', 'using reconstruction to reduce future risk, e.g. safer buildings, better land use and stronger institutions'),
         ('the hazard management cycle', 'a model linking response, recovery, mitigation and preparedness as a continuous cycle')],
  facts=[('Which phrase describes reconstruction that reduces future disaster risk?', 'Build back better', ['Leave no one behind', 'Polluter pays', 'Think global, act local'], 'It is a priority of the Sendai Framework.'),
         ('After the 2010 Haiti earthquake, which disease outbreak killed about 10,000 people?', 'Cholera', ['Malaria', 'Ebola', 'Measles'], 'It was introduced by UN peacekeepers and spread through poor sanitation.'),
         ('In the Park model of disaster response, the "relief" phase typically lasts:', 'hours to days after the event', ['several years', 'decades', 'only before the event'], 'It is followed by rehabilitation and reconstruction.'),
         ('Christchurch\'s central business district was cordoned off after the 2011 earthquake for about:', 'two years', ['two days', 'two weeks', 'twenty years'], 'The "red zone" cordon was finally lifted in June 2013.')],
  why=[('Explain why the first 72 hours after an earthquake are critical.', 'Most people trapped under rubble die of injury, dehydration or exposure within about three days, so rapid search and rescue, medical care and access are vital to survival rates.'),
       ('Explain why recovery from disasters often takes longer in low-income countries.', 'Limited government funds and insurance, dependence on aid that is slow or unco-ordinated, weak institutions, lack of land titles, and damage forming a large share of GDP slow rebuilding.'),
       ('Explain how the Park model can be used to compare disaster responses.', 'It plots quality of life over time through relief, rehabilitation and reconstruction; comparing curves shows how deep the impact was, how fast recovery occurred and whether conditions were improved after the disaster.'),
       ('Explain why "building back better" is difficult to achieve.', 'Pressure to rebuild quickly, cost of higher standards, land disputes, lack of skilled builders and materials, weak enforcement, and communities wanting to rebuild where they lived before.')],
  contrast=[('emergency response', 'long-term recovery', 'Emergency response happens in the first hours to weeks and focuses on saving lives and meeting basic needs; long-term recovery takes months to years and rebuilds housing, infrastructure and livelihoods.'),
            ('international aid', 'local response', 'International aid brings money, specialist teams and supplies but may arrive slowly and lack local knowledge; local responders act immediately, know the area and rescue most survivors.')],
  misc=[('International rescue teams save most people trapped after earthquakes.', 'Most survivors are rescued by neighbours and local responders in the first hours, before international teams arrive.'),
        ('Recovery is complete once buildings have been rebuilt.', 'Recovery includes livelihoods, mental health, services and social networks, which can take far longer than rebuilding.'),
        ('More aid always means faster recovery.', 'Unco-ordinated aid can overwhelm local systems, undermine local markets and bypass governments (Haiti 2010).')],
  apply=[('Using a named example, evaluate the post-event response to a geophysical disaster.', 'e.g. Nepal 2015: rapid local and Indian/Chinese rescue, but landslides blocked access; the National Reconstruction Authority was created only eight months later; by 2020 most of about 800,000 homes had been rebuilt with government grants, some using earthquake-resistant designs.', 6),
         ('Suggest why access was a major problem for responders after the 2023 Al Haouz earthquake in Morocco.', 'Remote mountain villages in the High Atlas were reached by narrow roads blocked by landslides and rockfalls, so helicopters and mules were needed.', 2)],
  cases=[('the 2010 Haiti earthquake response', 'over US$13 billion was pledged, yet ten years later many people still lived in informal camps and a cholera outbreak killed about 10,000', 'challenges of post-event recovery in a low-income country', 'unco-ordinated aid and weak government slowed recovery'),
         ('Christchurch\'s rebuild after 2011', 'the CBD was cordoned for two years, and insurers and the EQC paid out about NZ$40 billion', 'post-event recovery in a high-income country', 'insurance funded reconstruction, but recovery still took over a decade'),
         ('Kobe after 1995', 'the port and expressway were rebuilt within about two years and codes were strengthened', 'reconstruction and building back better', 'reconstruction improved standards to reduce future risk'),
         ('the 2004 tsunami response in Aceh, Indonesia', 'the BRR reconstruction agency rebuilt about 140,000 homes, and the disaster helped end the Aceh conflict in 2005', 'recovery and governance', 'a dedicated agency and peace agreement supported rebuilding')],
  evaluate=[('Post-event responses are less effective than pre-event strategies in reducing the impacts of geophysical hazards.', ['prevention saves more lives (codes, warnings)', 'every dollar on preparedness saves several in response'], ['rapid response saves trapped survivors', 'recovery offers chances to build back better'], 'Pre-event strategies are more cost-effective, but effective response and recovery remain essential.'),
            ('International aid is essential for recovery from geophysical disasters in low-income countries.', ['funds rebuilding and specialist rescue', 'Haiti, Nepal relied on donors'], ['can be slow, tied or poorly co-ordinated', 'local capacity matters more in the long term'], 'Aid is often necessary but is effective only when it supports local institutions.')],
  extended=[('Explain how and why responses to geophysical disasters change over time after the event.', 'Hazard management cycle; Park model stages - relief, rehabilitation, reconstruction; local vs international actors; contrasting examples (Haiti 2010, Christchurch 2011, Nepal 2015).', 10, 'long')],
  res=[('Table: people rescued alive from rubble by day after a large earthquake - day 1: 420; day 2: 210; day 3: 95; day 4: 30; day 5: 12.',
        [('Calculate the percentage of all live rescues that happened within the first 72 hours.', f'(420 + 210 + 95) / {420 + 210 + 95 + 30 + 12} × 100 = {725 / 767 * 100:.1f}%'),
         ('Explain the trend shown.', 'Survival falls rapidly with time because of injuries, dehydration, crush syndrome and exposure, so rapid local search and rescue is vital.')]),
       ('Graph description: a Park model curve for two earthquakes - City A\'s quality of life falls to 30% of its pre-disaster level and returns to 100% after 4 years; City B\'s falls to 70% and returns to 100% after 1 year, then rises to 110%.',
        [('Compare the two curves.', 'City A suffered a much deeper fall (70 percentage points vs 30) and took four times longer to recover; City B recovered quickly and improved beyond its previous level.'),
         ('Suggest what City B\'s curve after one year suggests about its reconstruction.', 'It built back better - improved buildings and services raised quality of life above pre-disaster levels.')])])

S('ch04-st3', gens=['pct_hazard', 'risk', 'deathrate'],
  terms=[('Sendai Framework for Disaster Risk Reduction', 'the UN agreement for 2015-2030 with seven targets and four priorities to reduce disaster deaths, losses and affected people'),
         ('insurance', 'a risk-sharing mechanism in which people pay premiums to receive compensation after losses'),
         ('catastrophe bond', 'a bond whose investors lose their money if a specified disaster occurs, transferring risk to financial markets'),
         ('community-based disaster risk reduction', 'preparedness led by local communities, such as volunteer response teams, local hazard mapping and drills'),
         ('parametric insurance', 'insurance that pays out automatically when a measured trigger (e.g. a magnitude or wind speed) is reached, rather than after loss assessment')],
  facts=[('The Sendai Framework covers the period:', '2015-2030', ['2000-2015', '1990-2000', '2020-2050'], 'It replaced the Hyogo Framework for Action (2005-2015).'),
         ('New Zealand\'s public natural hazard insurer, which paid many claims after the Christchurch earthquakes, is now called:', 'the Natural Hazards Commission (formerly the Earthquake Commission, EQC)', ['the Reserve Bank', 'Lloyd\'s of London', 'the Red Cross'], 'A levy on home insurance funds it.'),
         ('The Caribbean Catastrophe Risk Insurance Facility (CCRIF) is an example of:', 'parametric insurance shared between countries', ['a building code', 'a tsunami warning system', 'an NGO evacuation plan'], 'It pays governments quickly after earthquakes and hurricanes.'),
         ('Which Sendai Framework priority focuses on "build back better"?', 'Priority 4: enhancing preparedness for effective response and reconstruction', ['Priority 1: understanding disaster risk', 'Priority 2: governance', 'Priority 3: investing in resilience'], 'There are four priorities in total.')],
  why=[('Explain how insurance increases resilience to geophysical hazards.', 'It spreads losses across many people and over time, providing money for rapid rebuilding and reducing the economic burden on households and governments; risk-based premiums can encourage safer building.'),
       ('Explain why insurance coverage is low in many low-income countries.', 'People cannot afford premiums, insurers lack data and markets, informal housing lacks legal title, and governments may expect international aid instead.'),
       ('Explain how community preparedness builds resilience.', 'Local volunteers trained in first aid and search and rescue, evacuation drills, emergency kits and local hazard maps mean people can act immediately before outside help arrives.'),
       ('Explain the aims of the Sendai Framework.', 'It shifts the focus from managing disasters to reducing risk, with targets to cut deaths, affected people, economic losses and damage to infrastructure by 2030, and to increase early warning and national strategies.')],
  contrast=[('resilience', 'resistance', 'Resistance is the ability to withstand a hazard without damage; resilience includes the ability to absorb impacts and recover quickly afterwards.'),
            ('traditional indemnity insurance', 'parametric insurance', 'Indemnity insurance pays for assessed losses, which can take months; parametric insurance pays automatically when a trigger is reached, giving fast cash but possibly not matching actual losses.')],
  misc=[('Insurance reduces the physical damage caused by hazards.', 'Insurance does not prevent damage; it spreads the financial cost and speeds recovery.'),
        ('The Sendai Framework is legally binding on countries.', 'It is a voluntary, non-binding agreement, although 187 UN member states adopted it.'),
        ('Resilience is only about strong buildings.', 'Resilience includes social networks, governance, economic diversity, insurance and preparedness.')],
  apply=[('Using a named example, explain how community preparedness reduces disaster risk.', 'e.g. Japan: Disaster Prevention Day drills on 1 September; neighbourhood associations with emergency stores; "tsunami tendenko" tradition of evacuating immediately - in Kamaishi in 2011 almost all schoolchildren survived because of drills.', 4),
         ('Suggest one advantage and one disadvantage of catastrophe bonds for a government.', 'Advantage: transfers risk to investors and provides rapid funds (e.g. Mexico\'s earthquake bond paid out after 2017); disadvantage: costly premiums and pays only if trigger conditions are met.', 2)],
  cases=[('the "Miracle of Kamaishi", Japan', 'almost all of the roughly 3,000 elementary and junior high school students in Kamaishi survived the 2011 tsunami after years of evacuation drills', 'community preparedness', 'education and drills enabled immediate self-evacuation'),
         ('the Caribbean Catastrophe Risk Insurance Facility', 'it paid Haiti about US$7.75 million within 14 days of the 2010 earthquake', 'parametric risk pooling', 'shared insurance provided rapid funds to a government with few reserves'),
         ('New Zealand\'s Earthquake Commission', 'it handled claims of about NZ$10 billion after the 2010-11 Canterbury earthquakes', 'public insurance and resilience', 'a national insurance scheme funded large-scale rebuilding'),
         ('Mexico\'s catastrophe bond', 'it paid out US$150 million after the September 2017 Chiapas earthquake (Mw 8.2)', 'risk transfer to financial markets', 'parametric bonds give governments rapid post-disaster funds')],
  evaluate=[('The Sendai Framework will significantly reduce disaster losses by 2030.', ['global targets and monitoring', 'focus on reducing risk rather than response'], ['non-binding; many countries lack funds', 'losses are rising with urbanisation and climate change'], 'The framework improves priorities and data, but achieving targets depends on national action and funding.'),
            ('Insurance is the most effective way to build resilience to geophysical hazards.', ['speeds recovery (Christchurch)', 'risk pooling (CCRIF)'], ['does not save lives', 'unaffordable for the poor; community preparedness and codes matter more'], 'Insurance builds financial resilience but must be combined with preparedness and risk reduction.')],
  extended=[('Explain how resilience to geophysical hazards can be increased at different scales.', 'Household (kits, insurance), community (drills, volunteers - Kamaishi), national (codes, EQC, catastrophe bonds) and global (Sendai Framework, CCRIF).', 10, 'long')],
  res=[('Table: insured share of economic losses - Christchurch 2011: about 80%; Tōhoku 2011: about 17%; Kahramanmaraş 2023: about 6%; Haiti 2010: under 1%.',
        [('If losses from the Christchurch earthquakes were NZ$40 billion, calculate the insured amount.', '80% × 40 = NZ$32 billion'),
         ('Suggest why insured shares were so different.', 'New Zealand has a compulsory national levy (EQC) with high coverage; Japanese earthquake cover is optional and limited; poorer households and informal housing in Türkiye and Haiti were largely uninsured.')]),
       ('Sendai target data: a country recorded 2,400 disaster deaths per year on average in 2005-2015 and 1,560 in 2015-2025.',
        [('Calculate the percentage change in average annual deaths.', f'(1,560 − 2,400)/2,400 × 100 = {pc(2400, 1560)}'),
         ('Suggest why this measure alone may not show improved resilience.', 'Deaths vary with the number and size of events, so a quiet decade may look like improvement; economic losses and numbers affected must also be considered.')])])

# =============================================================================================
# HL extension: Power, places and networks
# =============================================================================================
S('ch05-st1', gens=['kof', 'pct_global', 'spearman_global'],
  terms=[('globalisation', 'the growing interconnectedness and interdependence of places through flows of goods, capital, people, information and ideas'),
         ('KOF Globalisation Index', 'a composite index produced by the KOF Swiss Economic Institute measuring economic, social and political globalisation of countries'),
         ('economic globalisation', 'the integration of national economies through trade, foreign direct investment and financial flows'),
         ('social globalisation', 'the spread of ideas, information, culture and people, measured by tourism, migration, internet use and trade in cultural goods'),
         ('political globalisation', 'the diffusion of government policies and participation in international organisations, embassies, treaties and UN peacekeeping'),
         ('global participation', 'the degree to which a place, group or country takes part in global flows and networks')],
  facts=[('The KOF Globalisation Index is produced by an institute in which country?', 'Switzerland', ['Japan', 'the USA', 'Brazil'], 'The KOF Swiss Economic Institute is part of ETH Zürich.'),
         ('Which three dimensions does the KOF index combine?', 'Economic, social and political', ['Physical, human and environmental', 'Urban, rural and coastal', 'Military, cultural and religious'], 'Each has de facto (flows) and de jure (policy) components.'),
         ('Countries that usually top the KOF overall rankings include:', 'Switzerland, the Netherlands and Belgium', ['Eritrea, Somalia and North Korea', 'Chad, Niger and Mali', 'Bhutan, Nepal and Laos'], 'Small, open, trade-oriented economies tend to score highest.'),
         ('A "de facto" measure of globalisation records:', 'actual flows and activities, such as trade volumes', ['laws and policies that enable flows', 'the size of the population', 'average temperature'], 'De jure measures record policies and institutions.')],
  why=[('Explain why small, wealthy European countries score highly on the KOF index.', 'Small domestic markets make them very dependent on trade; they host TNC headquarters and finance; open borders within the EU encourage migration and tourism; and they belong to many international organisations.'),
       ('Explain why national globalisation indices can hide spatial variations.', 'They are national averages; core cities such as Shanghai or Mumbai are highly connected while remote rural areas and poorer groups may be largely excluded.'),
       ('Explain why some countries have low participation in global networks.', 'Landlocked location, conflict or sanctions (North Korea), limited infrastructure and internet access, low incomes, political isolation and dependence on a narrow range of exports.'),
       ('Explain how the KOF index distinguishes between de facto and de jure globalisation.', 'De facto measures actual flows (trade, FDI, tourism, internet bandwidth); de jure measures policies and conditions enabling flows (tariff rates, treaties, freedom to visit), so a country may be open in law but have low actual flows.')],
  contrast=[('economic globalisation', 'social globalisation', 'Economic globalisation concerns flows of goods, services and capital; social globalisation concerns flows of people, information and culture.'),
            ('de facto globalisation', 'de jure globalisation', 'De facto globalisation measures actual flows and interactions; de jure globalisation measures the policies and institutions that enable or restrict those flows.')],
  misc=[('A high KOF score means a country is wealthy.', 'KOF and GDP per capita are positively correlated, but some middle-income open economies score highly and wealth is not part of the index.'),
        ('Globalisation affects all parts of a country equally.', 'Participation is concentrated in global cities, ports and export zones; rural and marginalised groups may be "switched off".'),
        ('Globalisation is a recent phenomenon only since the internet.', 'Global trade and migration have long histories (Silk Roads, colonial empires); recent decades show acceleration due to technology and liberalisation.')],
  apply=[('Using a named country, explain how its KOF index score reflects its global interactions.', 'e.g. Singapore: very high economic globalisation (trade over 300% of GDP, major port and FDI hub); high social globalisation (migrant workers, tourism, internet); moderate political score because it is a small state.', 4),
         ('Suggest two other indicators that could be used to measure a country\'s global participation.', 'Number of TNC headquarters, international airline connections, internet bandwidth per user, number of international students, membership of trade blocs, and cultural exports.', 2)],
  cases=[('Switzerland', 'it is ranked among the top two or three countries on the KOF index, with high trade, finance, tourism and international organisations in Geneva', 'high global participation', 'a small, open economy with many international institutions scores highly'),
         ('Singapore', 'a city-state whose trade is over three times its GDP, home to one of the world\'s busiest container ports', 'economic globalisation', 'its location on the Strait of Malacca and openness make it a global hub'),
         ('North Korea', 'it has very low trade, tourism and internet access because of isolationist policies and UN sanctions', 'low global participation', 'political choices and sanctions can "switch off" a country from global flows'),
         ('India', 'Bengaluru\'s IT and outsourcing industry is highly globalised, while many rural districts have limited participation', 'uneven globalisation within countries', 'national scores hide large internal variations')],
  evaluate=[('The KOF Globalisation Index is the best way to measure global interactions.', ['covers economic, social and political dimensions', 'long time series since 1970 allows comparison'], ['national averages hide inequality', 'weightings and indicators are chosen subjectively; informal flows missed'], 'KOF is a useful comparative tool but must be complemented by local and qualitative evidence.'),
            ('Economic globalisation is more important than social or political globalisation.', ['trade and FDI drive growth and jobs', 'economic integration often leads others'], ['culture, migration and information flows shape identities', 'political cooperation (UN, treaties) shapes global rules'], 'Economic flows are often the driving force, but the dimensions are interdependent.')],
  extended=[('Explain how globalisation can be measured and why some countries are more globalised than others.', 'KOF index dimensions and indicators; de facto/de jure; contrasting countries (Switzerland, Singapore, North Korea); size, location, policy, wealth; limitations of indices.', 10, 'long')],
  res=[('Table: KOF Globalisation Index 2023 edition (2021 data, approximate) - Switzerland 90.8; Netherlands 90.1; Germany 88.1; Brazil 61.6; India 62.4; Ethiopia 45.5; Eritrea 32.3.',
        [('Calculate the range of the index scores shown.', f'90.8 − 32.3 = {90.8 - 32.3:.1f}'),
         ('Suggest why India and Brazil have similar scores despite different populations.', 'Both are large economies with big domestic markets, so trade is a smaller share of GDP; both participate in G20 and BRICS but have lower social globalisation per person than small European states.')]),
       ('Graph description: a scatter graph of KOF index (x) against GDP per capita (y) for 20 countries shows a positive relationship; Singapore and Ireland plot well above the trend line; Gulf states plot above it; Rwanda plots below.',
        [('Describe the relationship shown.', 'A positive correlation: more globalised countries tend to have higher GDP per capita, with some anomalies.'),
         ('Suggest one reason why Ireland lies above the trend line.', 'Large FDI from US TNCs (tech and pharmaceuticals) booking profits in Ireland inflates GDP per capita.')])])

S('ch05-st2', gens=['pct_global', 'spearman_global', 'kof'],
  terms=[('superpower', 'a state with dominant global influence through economic, military, political and cultural power, e.g. the USA'),
         ('emerging economy', 'a country with rapid economic growth and increasing global influence, e.g. China, India, Brazil'),
         ('hard power', 'influence through coercion or payment, using military force, sanctions or economic pressure'),
         ('soft power', 'influence through attraction and persuasion, using culture, values, education and diplomacy (Joseph Nye)'),
         ('smart power', 'the strategic combination of hard and soft power to achieve goals'),
         ('BRICS', 'a grouping of major emerging economies - Brazil, Russia, India, China, South Africa - which expanded from 2024 to include Egypt, Ethiopia, Iran, the UAE and Indonesia')],
  facts=[('The concept of "soft power" was developed by:', 'Joseph Nye', ['Walt Rostow', 'Immanuel Wallerstein', 'Thomas Malthus'], 'Nye introduced it in 1990.'),
         ('China\'s Belt and Road Initiative, launched in 2013, mainly invests in:', 'infrastructure such as ports, railways and power plants', ['Hollywood films', 'military alliances in Europe', 'university fees in the USA'], 'Over 140 countries have signed BRI agreements.'),
         ('Which is an example of hard power?', 'Economic sanctions on Russia after the 2022 invasion of Ukraine', ['K-pop concerts', 'Confucius Institutes', 'Erasmus student exchanges'], 'Sanctions use economic coercion.'),
         ('The USA\'s military spending in 2023 was about what share of the world total?', 'About 37%', ['About 5%', 'About 75%', 'About 15%'], 'SIPRI estimated about US$916 billion out of about US$2.4 trillion.')],
  why=[('Explain how a country can use soft power to increase its global influence.', 'Attractive culture (films, music, sport), universities attracting students, aid and humanitarian work, diplomacy and values make others want to co-operate, e.g. South Korea\'s "Hallyu" wave and the UK\'s BBC World Service.'),
       ('Explain why China is considered a rising superpower.', 'Second largest economy (largest by PPP), the largest exporter, BRI investments in over 140 countries, a growing navy, technology firms (Huawei, BYD), and growing influence in the UN and BRICS.'),
       ('Explain why economic power can be converted into political influence.', 'Large markets, investment and loans create dependence, giving bargaining power in trade negotiations and votes in international organisations, e.g. Chinese loans and investment in Africa.'),
       ('Explain why emerging economies seek greater influence in global governance.', 'Their share of world GDP has grown but votes in the IMF and World Bank and permanent UN Security Council seats still reflect 1945 power; groups such as BRICS and the New Development Bank provide alternatives.')],
  contrast=[('hard power', 'soft power', 'Hard power uses coercion such as military force and sanctions; soft power uses attraction such as culture, education and values to persuade others.'),
            ('a superpower', 'an emerging economy', 'A superpower has dominant influence across economic, military, political and cultural spheres (USA); an emerging economy is rapidly growing in influence but does not yet have global dominance in all spheres (India, Brazil).')],
  misc=[('Military strength alone makes a country a superpower.', 'Superpowers combine military, economic, political and cultural power; Russia has a large military but a much smaller economy than the USA or China.'),
        ('Soft power is less effective than hard power.', 'Soft power can achieve lasting influence without costs of conflict, and smart power combines both.'),
        ('Emerging economies all have the same strategies.', 'They differ widely: China invests heavily in infrastructure abroad, India in IT services and diaspora links, Brazil in agriculture and regional leadership.')],
  apply=[('Using named examples, compare how two countries use hard and soft power.', 'e.g. USA: hard - largest military, about 750 overseas bases, sanctions, the dollar; soft - Hollywood, universities, tech brands. China: hard - navy in the South China Sea, economic leverage; soft - Confucius Institutes, BRI, TikTok, panda diplomacy.', 6),
         ('Suggest why South Korea\'s cultural exports are an example of soft power.', 'K-pop, K-dramas and films such as Parasite increase global interest in Korea, boosting tourism, brand exports (Samsung, Hyundai) and positive attitudes.', 2)],
  cases=[('the Belt and Road Initiative', 'China has financed ports, railways and power plants in over 140 countries since 2013, such as the Mombasa-Nairobi railway and Hambantota port in Sri Lanka', 'economic power of an emerging superpower', 'infrastructure finance extends political and economic influence'),
         ('the Korean Wave (Hallyu)', 'K-pop groups such as BTS and films such as Parasite (Oscar winner 2020) spread Korean culture worldwide', 'soft power', 'cultural attraction raises a country\'s global profile and exports'),
         ('sanctions on Russia from 2022', 'the EU, USA and allies froze central bank assets and removed banks from SWIFT', 'hard economic power', 'economic coercion was used instead of direct military intervention'),
         ('the expansion of BRICS in 2024', 'Egypt, Ethiopia, Iran and the UAE joined, with Indonesia following in 2025', 'emerging economies and global power', 'emerging countries are building alternatives to Western-led institutions')],
  evaluate=[('China will replace the USA as the world\'s dominant superpower.', ['economy largest by PPP and growing faster', 'BRI and trade networks extend influence'], ['USA still leads in military, finance (dollar), technology and alliances', 'China faces an ageing population, debt and slower growth'], 'A multipolar world is more likely than a simple replacement of US dominance.'),
            ('Soft power is now more important than hard power in global interactions.', ['culture, information and values shape global opinion', 'hard power is costly and can provoke resistance'], ['wars in Ukraine and the Middle East show military power still matters', 'sanctions and trade leverage remain decisive'], 'Smart power combining both is most effective; neither alone is sufficient.')],
  extended=[('Explain how global superpowers and emerging economies exercise power.', 'Hard, soft and smart power; economic, military, political, cultural; USA, China, India or Brazil examples; BRI, BRICS, sanctions, cultural exports.', 10, 'long')],
  res=[('Table: share of world GDP at PPP (%) - USA: 2000 20.1, 2023 15.5; China: 2000 7.4, 2023 18.7; India: 2000 4.2, 2023 7.6; EU: 2000 20.4, 2023 14.4.',
        [('Calculate the percentage change in China\'s share of world GDP from 2000 to 2023.', f'(18.7 − 7.4)/7.4 × 100 = {pc(7.4, 18.7)}'),
         ('Describe the shift in global economic power shown.', 'Power shifted from the USA and EU (both falling by about 5-6 percentage points) towards emerging Asian economies, with China overtaking the USA at PPP.')]),
       ('Table: military expenditure 2023 (US$ billion, SIPRI) - USA 916; China 296; Russia 109; India 84; Saudi Arabia 76; world total 2,443.',
        [('Calculate the USA\'s share of world military spending.', f'916 / 2,443 × 100 = {916 / 2443 * 100:.1f}%'),
         ('Suggest one limitation of using military spending to measure hard power.', 'It ignores differences in costs and purchasing power, technology, nuclear weapons, alliances and the effectiveness of forces.')])])

S('ch05-st3', gens=['oda', 'pct_global', 'kof'],
  terms=[('global governance', 'the institutions, rules and processes through which states and other actors co-operate to manage global issues'),
         ('G7', 'an informal group of seven major advanced economies - Canada, France, Germany, Italy, Japan, the UK and the USA (with the EU)'),
         ('G20', 'a forum of 19 countries plus the EU and the African Union representing about 85% of world GDP'),
         ('International Monetary Fund (IMF)', 'a global financial institution that promotes monetary stability and lends to countries facing balance-of-payments crises, often with conditions'),
         ('structural adjustment', 'conditions attached to IMF and World Bank loans, such as cutting public spending, privatisation and trade liberalisation'),
         ('UN Security Council', 'the UN body responsible for peace and security, with five permanent members holding a veto (China, France, Russia, UK, USA)')],
  facts=[('Which country has the largest voting share in the IMF?', 'The USA', ['China', 'India', 'Brazil'], 'At about 16.5% it can veto decisions requiring an 85% majority.'),
         ('The African Union became a permanent member of the G20 in:', '2023', ['1999', '2008', '2015'], 'It joined at the New Delhi summit.'),
         ('The five permanent members of the UN Security Council are:', 'China, France, Russia, the UK and the USA', ['Brazil, India, Japan, Germany and South Africa', 'the G7 countries', 'the BRICS countries'], 'Each has a veto over resolutions.'),
         ('The G20 leaders\' summit was first held in 2008 in response to:', 'the global financial crisis', ['the 2004 tsunami', 'the end of the Cold War', 'the Paris Agreement'], 'The finance ministers\' G20 dates from 1999.')],
  why=[('Explain why the IMF has been criticised by many developing countries.', 'Voting shares favour wealthy countries; structural adjustment conditions (spending cuts, privatisation) increased poverty and inequality in the 1980s-90s in Africa and Latin America; and Western countries traditionally choose its head.'),
       ('Explain why the G20 has become more influential than the G7.', 'It includes major emerging economies such as China, India and Brazil, so it represents about 85% of world GDP and two-thirds of world population, giving it greater legitimacy and economic weight.'),
       ('Explain why reforming the UN Security Council is difficult.', 'Changes require the agreement of the permanent members, each with a veto; regional rivalries (e.g. Pakistan vs India, Argentina vs Brazil) complicate choosing new members.'),
       ('Explain how international organisations can limit national sovereignty.', 'Membership involves accepting shared rules and rulings, e.g. WTO trade rules, IMF loan conditions or EU law, which constrain government choices.')],
  contrast=[('the G7', 'the G20', 'The G7 is a small group of advanced Western economies plus Japan; the G20 is broader, including major emerging economies and the EU and AU, and so represents more of the world economy and population.'),
            ('the IMF', 'the World Bank', 'The IMF lends short-term to stabilise currencies and balance of payments; the World Bank lends long-term for development projects such as infrastructure, health and education.')],
  misc=[('All UN members have equal power.', 'The General Assembly gives one vote each, but the five permanent Security Council members hold vetoes.'),
        ('IMF loans have no conditions.', 'IMF loans usually come with policy conditions (conditionality), such as fiscal reforms.'),
        ('The G20 is a formal organisation with binding laws.', 'It is an informal forum without a permanent secretariat or binding decisions.')],
  apply=[('Using a named example, explain the influence of an international organisation on a country.', 'e.g. IMF and Greece 2010-2018: bailouts totalling about €289 billion (with the EU) required austerity, tax rises and privatisation, contributing to unemployment of over 27% at its peak in 2013.', 4),
         ('Suggest why emerging economies created the New Development Bank in 2014.', 'To provide infrastructure finance without Western-dominated conditions, to reflect their growing economic weight and to reduce dependence on the IMF and World Bank.', 2)],
  cases=[('the IMF and Greek debt crisis', 'Greece received bailouts of about €289 billion between 2010 and 2018 with strict austerity conditions', 'the influence of global financial institutions', 'loan conditions shaped national economic policy and limited sovereignty'),
         ('the G20 response to the 2008 financial crisis', 'leaders agreed a US$1.1 trillion package in London in 2009 to restore growth', 'global governance during economic crises', 'co-ordinated action between major economies stabilised the global economy'),
         ('the UN Security Council and the war in Ukraine', 'Russian vetoes blocked resolutions condemning the 2022 invasion', 'the limits of global governance', 'the veto system allows permanent members to block collective action'),
         ('the New Development Bank (BRICS bank)', 'based in Shanghai, it had approved about 100 projects worth over US$30 billion by 2024', 'emerging-economy alternatives to Western institutions', 'emerging economies are building their own governance institutions')],
  evaluate=[('International organisations are dominated by the interests of high-income countries.', ['IMF voting shares and US veto', 'UNSC permanent members reflect 1945'], ['G20 includes emerging economies', 'BRICS and NDB offer alternatives; China is an influential UNSC member'], 'High-income countries still dominate many institutions, but power is gradually shifting.'),
            ('Global governance has been effective in managing global issues.', ['G20 response to 2008 crisis', 'Montreal Protocol, WTO dispute system'], ['UNSC deadlock (Syria, Ukraine)', 'slow progress on climate change'], 'Effectiveness varies: strong when interests align, weak when major powers disagree.')],
  extended=[('Explain the role of international organisations in global governance.', 'UN and Security Council, G7/G20, IMF, World Bank, WTO; examples (Greece, 2008 crisis); influence on sovereignty; criticisms and reform.', 10, 'long')],
  res=[('Table: IMF voting shares (%, approximate) - USA 16.5; Japan 6.1; China 6.1; Germany 5.3; India 2.6; Brazil 2.2; 85% supermajority needed for major decisions.',
        [('Explain why the USA effectively has a veto over major IMF decisions.', 'Its 16.5% share is greater than 15%, so other members cannot reach the 85% supermajority without it.'),
         ('Calculate the combined voting share of China, India and Brazil.', f'6.1 + 2.6 + 2.2 = {6.1 + 2.6 + 2.2:.1f}%')]),
       ('Table: G20 share of the world - GDP about 85%; trade about 75%; population about 66%; land area about 60%.',
        [('Suggest why the G20 is described as a more representative forum than the G7.', 'It covers about two-thirds of the world\'s population and includes emerging economies, the EU and the AU, not just advanced economies.'),
         ('State one limitation of the G20 as a governance body.', 'Its decisions are not binding and it excludes most low-income countries.')])])

S('ch06-st1', gens=['remit', 'oda', 'debt'],
  terms=[('official development assistance (ODA)', 'government aid to promote the economic development and welfare of developing countries, given as grants or concessional loans'),
         ('remittances', 'money sent home by migrants to their families in their country of origin'),
         ('foreign direct investment (FDI)', 'investment by a company in productive assets in another country, such as a factory or a controlling share of a firm'),
         ('debt relief', 'the cancellation or rescheduling of a country\'s external debts, e.g. under the HIPC Initiative and MDRI'),
         ('tied aid', 'aid that must be spent on goods and services from the donor country'),
         ('Heavily Indebted Poor Countries (HIPC) Initiative', 'an IMF and World Bank programme from 1996 that cancelled debts of qualifying poor countries in return for poverty-reduction reforms')],
  facts=[('The UN target for ODA from donor countries is:', '0.7% of gross national income', ['7% of GDP', '0.07% of GNI', '10% of government spending'], 'Only a few donors, such as Norway, Sweden, Luxembourg and Denmark, regularly meet it.'),
         ('Which country receives the largest total value of remittances in the world?', 'India', ['Mexico', 'Germany', 'Nigeria'], 'India received about US$125 billion in 2023 (World Bank).'),
         ('Which country receives the highest remittances relative to GDP?', 'Tajikistan', ['India', 'China', 'Brazil'], 'Remittances, mostly from Russia, were about 48% of GDP in 2023.'),
         ('Since about 2000, the largest financial flow to low- and middle-income countries (excluding China) has generally been:', 'remittances', ['ODA', 'debt relief', 'military aid'], 'Remittances have exceeded both ODA and FDI since 2019.')],
  why=[('Explain why remittances can be more beneficial to households than ODA.', 'They go directly to families without passing through governments, are spent on food, school fees, health and housing, and often increase during crises (counter-cyclical).'),
       ('Explain why FDI is concentrated in a small number of countries.', 'TNCs seek large markets, skilled or cheap labour, good infrastructure, political stability and favourable tax policies, so FDI flows mainly to high-income countries and major emerging economies such as China, India and Brazil.'),
       ('Explain why debt relief may not always lead to development.', 'Savings may not be spent on poverty reduction; corruption or weak governance; countries may borrow again (new Chinese and Eurobond lending), leading to new debt crises, e.g. Zambia\'s default in 2020.'),
       ('Explain the arguments against tied aid.', 'It reduces the value of aid by up to 30% because recipients cannot buy cheapest goods, benefits donor businesses, and may not meet local needs.')],
  contrast=[('ODA', 'FDI', 'ODA is government aid for development, often grants or concessional loans; FDI is private investment by companies seeking profit in productive assets abroad.'),
            ('bilateral aid', 'multilateral aid', 'Bilateral aid goes directly from one government to another and may be tied to donor interests; multilateral aid is channelled through international organisations such as the World Bank or UN.')],
  misc=[('Most money flowing to developing countries is aid.', 'Remittances and FDI are much larger than ODA for most low- and middle-income countries.'),
        ('Remittances only benefit the families who receive them.', 'They also have multiplier effects in local economies through spending on construction, services and businesses, and they provide foreign exchange.'),
        ('Debt relief has solved the debt problems of poor countries.', 'HIPC cancelled about US$100 billion, but by 2024 more than half of low-income countries were at high risk of or in debt distress.')],
  apply=[('Using a named country, explain the importance of remittances to its economy.', 'e.g. Nepal: remittances about 26% of GDP, mainly from workers in the Gulf, Malaysia and India; fund household consumption, education and housing; but create dependency and a "brain and brawn drain".', 4),
         ('Suggest two reasons why a TNC might choose to invest in Vietnam.', 'Relatively low labour costs, a young workforce, political stability, free trade agreements (EVFTA, CPTPP), proximity to China and supply chains, e.g. Samsung\'s phone factories.', 2)],
  cases=[('remittances to Tajikistan', 'money from migrants working mainly in Russia equalled about 48% of GDP in 2023', 'dependence on remittances', 'remittances support households but expose the economy to shocks in the host country'),
         ('Samsung\'s investment in Vietnam', 'Samsung has invested over US$20 billion in factories near Hanoi, which make around half of its smartphones', 'FDI by transnational corporations', 'FDI brings jobs and exports but profits flow back to the parent company'),
         ('debt relief for Ethiopia under the HIPC Initiative', 'Ethiopia had about US$3.3 billion cancelled in 2004 and increased spending on primary education and health', 'debt relief', 'cancelling debt freed resources for poverty reduction'),
         ('Norway\'s ODA programme', 'Norway gives about 1% of GNI as aid, exceeding the UN target of 0.7%', 'official development assistance', 'some donors give well above the agreed target')],
  evaluate=[('Remittances are more important than aid for development.', ['larger flows than ODA', 'reach households directly'], ['aid funds public goods such as health systems and infrastructure', 'remittances can increase inequality and dependency'], 'Remittances are larger and more direct, but aid funds public goods remittances cannot.'),
            ('FDI brings more benefits than costs to host countries.', ['jobs, technology, exports and tax (Vietnam)', 'multiplier effects'], ['profit repatriation, low wages, environmental damage', 'footloose investment can leave'], 'Benefits outweigh costs where governments regulate FDI and link it to local firms.')],
  extended=[('Explain the role of different financial flows in the development of low-income countries.', 'ODA (bilateral, multilateral, tied), remittances, FDI, loans and debt relief; scale and direction of flows; examples (Nepal, Tajikistan, Vietnam, Ethiopia).', 10, 'long')],
  res=[('Table: financial flows to low- and middle-income countries excluding China (US$ billion, 2022, World Bank estimates) - remittances 647; FDI 370; ODA 210.',
        [('Calculate remittances as a percentage of the total of the three flows.', f'647 / {647 + 370 + 210} × 100 = {647 / 1227 * 100:.1f}%'),
         ('Suggest why remittances have grown faster than ODA.', 'Rising international migration, cheaper and digital transfer methods, migrants\' wages, while many donors have frozen or cut aid budgets.')]),
       ('Table: ODA as % of GNI in 2023 (OECD, approximate) - Norway 1.09; Luxembourg 0.99; Sweden 0.91; Germany 0.79; UK 0.58; Japan 0.44; USA 0.24.',
        [('State how many of the countries shown met the UN target of 0.7%.', 'Four - Norway, Luxembourg, Sweden and Germany.'),
         ('Suggest why the USA gives the largest total amount of ODA despite its low percentage.', 'Its GNI is far larger than any other donor, so 0.24% equals about US$66 billion.')])])

S('ch06-st2', gens=['freight', 'pct_global', 'stats_dev'],
  terms=[('global supply chain', 'the network of firms and places involved in producing a good, from raw materials to final consumer'),
         ('value chain', 'the sequence of activities that add value to a product, from design and components to assembly, marketing and sales'),
         ('transnational corporation (TNC)', 'a company that operates in more than one country, with headquarters usually in its country of origin'),
         ('commodity', 'a raw material or primary product traded globally, such as oil, copper, coffee or cocoa'),
         ('offshoring', 'moving business functions to another country, often to reduce costs'),
         ('just-in-time production', 'a system of supplying components exactly when needed, minimising stock but increasing vulnerability to disruption')],
  facts=[('Which country makes most of Apple\'s iPhones?', 'China', ['the USA', 'Germany', 'Mexico'], 'Foxconn and other contractors assemble most iPhones in China, though India\'s share is rising.'),
         ('Côte d\'Ivoire and Ghana together produce about what share of world cocoa?', 'About 60%', ['About 10%', 'About 25%', 'About 95%'], 'Most of the value is added by chocolate companies in Europe and the USA.'),
         ('The "smile curve" shows that most value in manufacturing is added by:', 'design and marketing at either end of the chain', ['assembly in the middle', 'raw material extraction only', 'shipping'], 'Assembly adds relatively little value.'),
         ('Which of these has been the world\'s largest TNC by revenue in most recent years?', 'Walmart', ['FIFA', 'UNESCO', 'Oxfam'], 'Fortune Global 500 has listed Walmart first for many years.')],
  why=[('Explain why many TNCs locate assembly in lower-income countries.', 'Lower labour costs, large workforces, tax incentives and export processing zones, weaker regulation, and access to growing markets, e.g. Foxconn in Zhengzhou or garment factories in Bangladesh.'),
       ('Explain why countries that export primary commodities often gain little from global trade.', 'Commodity prices are volatile and often fall relative to manufactured goods; most value is added in processing and branding abroad; tariff escalation discourages processing in exporting countries.'),
       ('Explain why TNCs are important in global supply chains.', 'They co-ordinate production across many countries, control design, branding and distribution, determine where investment and jobs go, and capture much of the value added.'),
       ('Explain how containerisation has helped global trade grow.', 'Standard containers transfer quickly between ships, trains and trucks, reducing loading time, labour and theft; huge container ships give economies of scale, cutting freight costs per unit.')],
  contrast=[('upstream activities', 'downstream activities', 'Upstream activities are early in the value chain, such as raw material extraction and components; downstream activities are closer to the consumer, such as distribution, marketing and retail.'),
            ('offshoring', 'outsourcing', 'Offshoring is relocating activities to another country (whether owned by the firm or not); outsourcing is contracting activities to another firm (which may be at home or abroad).')],
  misc=[('An iPhone labelled "Made in China" is mostly Chinese value.', 'Components come from many countries (Japan, Korea, Taiwan, USA) and design and profits are mainly American; assembly in China captures only a small share of value.'),
        ('Global trade benefits all countries equally.', 'Gains are uneven; countries exporting processed and high-tech goods gain more than raw commodity exporters.'),
        ('TNCs only move to countries to exploit cheap labour.', 'Market access, skills, infrastructure and tax policies are often more important, which is why most FDI goes to high-income countries.')],
  apply=[('Using a named TNC, explain its global supply chain.', 'e.g. Apple: designed in California; components from Japan (sensors), Korea (displays from Samsung), Taiwan (chips from TSMC), USA; assembly by Foxconn in China and increasingly India; global sales through Apple stores and online; profits largely retained by Apple.', 6),
         ('Suggest why cocoa farmers in Ghana receive a small share of the value of a chocolate bar.', 'Most value is added by processing, branding and retail in Europe and North America; farmers sell raw beans at volatile world prices and lack bargaining power.', 3)],
  cases=[('Apple\'s iPhone supply chain', 'designed in California, with components from over 40 countries, and assembled mainly by Foxconn in China', 'global value chains', 'design and marketing capture most value while assembly earns little'),
         ('cocoa in Côte d\'Ivoire and Ghana', 'they grow about 60% of the world\'s cocoa, but farmers earn only about 6-7% of the value of a chocolate bar', 'commodity dependence in trade', 'value is added mainly by processors and retailers in high-income countries'),
         ('the garment industry in Bangladesh', 'garments make up over 80% of export earnings, and the 2013 Rana Plaza collapse killed 1,134 workers', 'TNC supply chains and labour standards', 'competition for low-cost production can put workers at risk'),
         ('the port of Rotterdam', 'Europe\'s largest port handles about 14 million containers (TEU) a year', 'nodes in global trade networks', 'major ports concentrate flows and value in global supply chains')],
  evaluate=[('TNCs bring more benefits than costs to the countries where they operate.', ['jobs and skills (Foxconn, Samsung)', 'exports and tax revenue'], ['low wages, poor conditions (Rana Plaza)', 'profit repatriation and tax avoidance'], 'TNCs can bring large benefits, but outcomes depend on host regulation and bargaining power.'),
            ('Global supply chains mainly benefit high-income countries.', ['value captured by design, branding and finance', 'commodity exporters gain little'], ['East Asian economies grew rapidly by joining supply chains', 'consumers everywhere gain cheaper goods'], 'High-income countries capture most value, but supply chains have been a route to development for some emerging economies.')],
  extended=[('Explain how global supply chains and TNCs influence patterns of trade.', 'Value chains, smile curve, TNC organisation, offshoring and outsourcing, containerisation; named examples (Apple, cocoa, Bangladesh garments); uneven gains.', 10, 'long')],
  res=[('Table: estimated breakdown of the retail price of a smartphone (US$1,000) - components and materials 450; assembly 30; Apple profit 350; distribution and retail 120; other 50.',
        [('Calculate the share of the retail price earned by assembly.', '30 / 1,000 × 100 = 3%'),
         ('Use the data to explain the smile curve.', 'Assembly (middle of the chain) earns only 3%, while design/brand profit (35%) and components and retail capture most value at the ends of the chain.')]),
       ('Table: value of a US$1 chocolate bar - cocoa farmer 6.6 cents; traders and grinders 8 cents; manufacturers 35 cents; retailers 44 cents; taxes 6.4 cents.',
        [('Calculate the combined share received by manufacturers and retailers.', '35 + 44 = 79%'),
         ('Suggest one way farmers could gain a larger share of value.', 'Processing cocoa locally into chocolate or butter; Fairtrade premiums; co-operatives increasing bargaining power; government price controls (e.g. Ghana and Côte d\'Ivoire\'s Living Income Differential).')])])

S('ch06-st3', gens=['migration', 'remit', 'pct_pop'],
  terms=[('labour migration', 'the movement of people across borders to find work, often temporary or circular'),
         ('migration controls', 'policies regulating who can enter and work in a country, such as visas, points systems, quotas and border walls'),
         ('kafala system', 'a sponsorship system in Gulf states tying migrant workers\' legal status to their employer'),
         ('points-based system', 'an immigration system that awards points for skills, qualifications, language and salary, used in Australia, Canada and the UK'),
         ('brain drain', 'the emigration of highly skilled and educated people from a country'),
         ('circular migration', 'repeated temporary movement between origin and destination, often seasonal')],
  facts=[('About what share of the UAE\'s population are non-citizens?', 'About 88%', ['About 20%', 'About 50%', 'About 5%'], 'Most are labour migrants from South Asia and the Philippines.'),
         ('The Schengen Area allows:', 'passport-free movement between most EU and some non-EU European countries', ['free migration from anywhere in the world to Europe', 'only goods to move freely', 'a single currency'], 'It has 29 member countries.'),
         ('Which country is the largest source of international migrants?', 'India', ['the USA', 'China', 'Germany'], 'About 18 million Indians live abroad (UN DESA 2020).'),
         ('Canada\'s Express Entry system is an example of:', 'a points-based immigration system', ['a refugee camp', 'a border wall', 'a free trade agreement'], 'Points are awarded for age, education, language and job offers.')],
  why=[('Explain why the Gulf states attract large numbers of labour migrants.', 'Oil wealth funded construction and services; small citizen populations; higher wages than in South Asia; government recruitment through the kafala system.'),
       ('Explain why governments introduce migration controls.', 'To meet labour shortages while limiting competition for jobs, manage pressure on housing and services, address security concerns, respond to public opinion, and protect cultural identity.'),
       ('Explain how migration controls can affect migrants\' rights.', 'Sponsorship systems such as kafala can tie workers to employers, leading to passport confiscation and exploitation; irregular migrants have little legal protection; temporary visas limit family reunion.'),
       ('Explain why labour migration benefits both source and host countries.', 'Hosts fill labour shortages and gain taxes and skills; source countries gain remittances, reduced unemployment and returning migrants with skills.')],
  contrast=[('a points-based immigration system', 'a quota system', 'A points system admits migrants who reach a threshold based on skills, language and salary; a quota system sets a fixed number of migrants by country, sector or year.'),
            ('voluntary labour migration', 'forced migration', 'Voluntary labour migrants choose to move for work and income; forced migrants (refugees, internally displaced people) are compelled to move by conflict, persecution or disaster.')],
  misc=[('Most international migrants move from poor countries to rich countries.', 'About a third of migrants move between low- and middle-income countries (South-South migration).'),
        ('Stronger border controls stop migration.', 'Controls may redirect migration to more dangerous routes and increase irregular migration and smuggling.'),
        ('Labour migrants take jobs from local workers.', 'Many fill shortages in jobs locals do not want or lack skills for, such as construction in the Gulf or care work in Europe.')],
  apply=[('Using a named example, explain the effects of labour migration on a host country.', 'e.g. Qatar: migrants about 88% of population; built 2022 World Cup stadiums and infrastructure; reports of deaths and abuses led to reforms of kafala in 2020 (minimum wage, ability to change jobs).', 4),
         ('Suggest how the UK\'s post-Brexit immigration system changed labour migration.', 'Ending free movement from the EU in 2021 and introducing a points-based system reduced EU migration but increased non-EU migration, especially health and care workers from India, Nigeria and Zimbabwe.', 3)],
  cases=[('labour migration to Qatar', 'migrants make up about 88% of residents, many from Nepal, India and Bangladesh, building 2022 World Cup infrastructure', 'labour migration and the kafala system', 'migration controls tied workers to employers until reforms in 2020'),
         ('the UK points-based system', 'free movement from the EU ended in January 2021, and non-EU migration then rose to record levels', 'changes in migration controls', 'policy changed the sources rather than the scale of migration'),
         ('Filipino overseas workers', 'about 2 million Filipinos work abroad at any time, with remittances equal to about 9% of GDP', 'state-managed labour migration', 'a government agency promotes and protects workers abroad as an export strategy'),
         ('the US-Mexico border', 'about 1,000 km of barriers exist, yet US Border Patrol recorded about 2 million encounters in 2023', 'migration controls and their limits', 'physical controls redirect rather than stop migration flows')],
  evaluate=[('Migration controls are effective in managing labour migration.', ['points systems select skills (Canada, Australia)', 'quotas match demand'], ['irregular migration continues (US-Mexico)', 'labour shortages after restrictions (UK care sector)'], 'Controls shape who migrates, but economic forces mean they rarely control numbers fully.'),
            ('Labour migration brings more benefits to source countries than costs.', ['remittances (Nepal, Philippines)', 'skills of returnees'], ['brain drain of doctors and nurses', 'family separation and dependency'], 'Benefits are significant, but losses of skilled workers can harm services in small source countries.')],
  extended=[('Explain how and why governments control flows of labour migrants.', 'Types of controls (points, quotas, visas, kafala, walls, free movement areas); reasons (labour demand, security, public opinion); examples (Qatar, UK, Canada, USA); effects on migrants.', 10, 'long')],
  res=[('Table: non-citizen share of population (approximate) - UAE 88%; Qatar 88%; Kuwait 68%; Saudi Arabia 42%.',
        [('If Qatar\'s population is 2.7 million, estimate the number of non-citizens.', f'88% × 2.7 = {0.88 * 2.7:.2f} million'),
         ('Suggest why Gulf states depend so heavily on migrant labour.', 'Small citizen populations, rapid oil-funded construction and service growth, and citizens preferring public-sector jobs.')]),
       ('Graph description: UK net migration (thousand) - 2019: 184; 2021: 488; 2022: 764; 2023: 685; EU net migration became negative after 2021 while non-EU migration rose sharply.',
        [('Calculate the percentage change in net migration between 2019 and 2022.', f'(764 − 184)/184 × 100 = {pc(184, 764)}'),
         ('Suggest reasons for the change.', 'Visa routes for health and care workers and students, humanitarian schemes for Ukrainians and Hong Kong residents, and the end of EU free movement changing the mix of migrants.')])])

S('ch07-st1', gens=['tsc', 'pct_global', 'spearman_global'],
  terms=[('time-space compression', 'the reduction in the time taken to move goods, people and information between places, making the world effectively "shrink" (David Harvey)'),
         ('shrinking world', 'the idea that improvements in transport and communications have reduced the relative distance between places'),
         ('digital divide', 'the gap between people and places with good access to information and communication technology and those without'),
         ('global network', 'a set of interconnected places (nodes) linked by flows such as trade, finance, data and transport'),
         ('submarine cable', 'a fibre-optic cable on the seabed carrying most international internet and telephone data')],
  facts=[('About what share of intercontinental internet data travels through submarine cables?', 'About 95-99%', ['About 10%', 'About 50%', 'About 1%'], 'Satellites carry only a small share of international data.'),
         ('The concept of time-space compression is most associated with:', 'David Harvey', ['W. W. Rostow', 'Ernest Ravenstein', 'Thomas Malthus'], 'Harvey described it in The Condition of Postmodernity (1989).'),
         ('In 2024 about what share of the world\'s population did not use the internet?', 'About a third', ['About 1%', 'About two-thirds', 'About 90%'], 'The ITU estimated about 2.6 billion people were offline.'),
         ('Which region has the lowest internet use as a share of population?', 'Sub-Saharan Africa', ['Europe', 'North America', 'East Asia'], 'Internet penetration was under 40% in many countries in 2023.')],
  why=[('Explain how time-space compression has changed global interactions.', 'Faster, cheaper transport (jets, container ships) and instant communications allow goods, people, capital and information to move rapidly, enabling global supply chains, financial markets, tourism and migration.'),
       ('Explain why the world has not "shrunk" equally for all places.', 'Connections are concentrated between global cities and well-connected regions; remote, poor and landlocked places have fewer flights, slower internet and higher costs, so relative distance remains large (the digital divide).'),
       ('Explain how technology has changed the location of service industries.', 'Broadband and cheap telecoms allow back-office work, call centres and software development to be offshored to places such as Bengaluru and Manila, and remote working has grown since 2020.'),
       ('Explain why submarine cables are important to global networks.', 'They carry almost all intercontinental data; their landing points and routes determine which places are well connected, and damage to cables can disconnect countries, e.g. Tonga after the 2022 eruption.')],
  contrast=[('absolute distance', 'relative distance', 'Absolute distance is the physical distance between places in km; relative distance is measured in time, cost or effort and has fallen with transport and communications technology.'),
            ('places that are "switched on"', 'places that are "switched off"', 'Switched-on places are well connected to global flows (London, Singapore); switched-off places have limited connection due to remoteness, poverty, conflict or policy (rural Chad, North Korea).')],
  misc=[('Time-space compression means places are physically closer together.', 'Physical distances are unchanged; it is the time and cost of interactions that have fallen.'),
        ('The internet is accessible to almost everyone.', 'About a third of humanity remained offline in 2024, mostly in low-income and rural areas.'),
        ('Technology always reduces inequality between places.', 'It can widen gaps when well-connected places gain first and remote places are left behind.')],
  apply=[('Using examples, explain how improvements in transport have caused time-space compression.', 'e.g. sailing ships (London-Sydney about 100 days in 1850), steamships (about 40 days by 1900), jet aircraft (about 22 hours today); container ships have cut freight costs dramatically.', 4),
         ('Suggest why M-Pesa in Kenya shows technology can increase global participation.', 'Mobile money lets people without bank accounts transfer money and receive remittances, joining digital economic networks; over 90% of Kenyan adults use mobile money.', 2)],
  cases=[('M-Pesa in Kenya', 'mobile money launched by Safaricom in 2007 is used by most Kenyan adults to save, pay and receive remittances', 'technology widening participation', 'mobile phones let people bypass the lack of bank branches'),
         ('the 2022 Tonga cable break', 'the Hunga Tonga eruption cut the single international submarine cable, isolating Tonga for about five weeks', 'vulnerability of global networks', 'dependence on a single connection makes small states vulnerable'),
         ('the Bengaluru IT cluster', 'Bengaluru hosts about a third of India\'s IT exports and offices of firms such as Infosys and Google', 'time-space compression and service offshoring', 'cheap telecoms allowed services to be delivered globally from India'),
         ('the 2Africa submarine cable', 'one of the world\'s longest cables, at about 45,000 km, connects 33 countries around Africa, Europe and the Middle East', 'investment in global connectivity', 'new infrastructure is reducing the digital divide')],
  evaluate=[('Time-space compression has benefited everyone.', ['cheaper goods, travel and communication', 'access to information and remittances (M-Pesa)'], ['digital divide excludes about a third of the world', 'deindustrialisation and job losses in high-income regions'], 'Benefits have been widespread but highly uneven between and within countries.'),
            ('Technology is the most important factor in increasing global interactions.', ['containerisation, jets, internet', 'mobile phones in Africa'], ['trade liberalisation, political decisions and TNC strategies', 'cheap energy for transport'], 'Technology enables interactions, but political and economic decisions determine their scale and direction.')],
  extended=[('Explain how technology has led to time-space compression and its uneven effects.', 'Transport (jets, containers) and ICT (submarine cables, internet, mobile); shrinking world; digital divide; examples (Bengaluru, M-Pesa, Tonga).', 10, 'long')],
  res=[('Table: travel time London to Sydney - 1850 sailing ship: 100 days; 1900 steamship: 40 days; 1950 propeller aircraft: 4 days; 2024 jet: 22 hours.',
        [('Calculate how many times faster the 2024 journey is than in 1850.', f'100 × 24 / 22 = {100 * 24 / 22:.0f} times'),
         ('Explain how the data illustrate time-space compression.', 'The relative distance in time has fallen by over 99% while the absolute distance is unchanged.')]),
       ('Table: internet users (% of population, 2023, ITU) - Europe 91; Americas 87; Asia-Pacific 66; Arab States 70; Africa 37; world 67.',
        [('Calculate the difference between Europe and Africa.', '91 − 37 = 54 percentage points'),
         ('Suggest two reasons for low internet use in Africa.', 'Low incomes and high data costs; limited electricity and broadband infrastructure in rural areas; low digital literacy.')])])

S('ch07-st2', gens=['pct_global', 'spearman_global', 'debt'],
  terms=[('landlocked state', 'a country with no coastline, which must use neighbours\' ports and transport routes for sea trade, e.g. Bolivia, Ethiopia, Laos'),
         ('resource curse', 'the paradox that countries rich in natural resources often have slower growth, more corruption and conflict than resource-poor countries'),
         ('isolationism', 'a policy of minimising involvement in international affairs and trade'),
         ('trade bloc', 'a group of countries that reduce trade barriers between themselves, such as the EU, ASEAN or AfCFTA'),
         ('sanctions', 'measures, such as trade bans and asset freezes, imposed on a country to change its behaviour'),
         ('special economic zone', 'an area with tax and regulatory incentives to attract investment and exports, such as Shenzhen')],
  facts=[('How many landlocked countries are there in the world?', 'About 44', ['About 4', 'About 12', 'About 90'], 'The figure varies slightly if partially recognised states are included; 16 are in Africa.'),
         ('Landlocked developing countries face trade costs about how much higher than coastal neighbours?', 'Often around 50% or more', ['About 1%', 'Exactly the same', 'Lower costs'], 'Transit delays, border crossings and long distances add cost.'),
         ('Shenzhen became China\'s first special economic zone in:', '1980', ['1949', '1997', '2013'], 'It grew from about 30,000 people to over 17 million.'),
         ('Bolivia lost its coastline to Chile in the:', 'War of the Pacific (1879-1884)', ['Second World War', 'Chaco War', 'Falklands War'], 'In 2018 the ICJ ruled Chile was not obliged to negotiate sea access.')],
  why=[('Explain why landlocked states often have lower participation in global trade.', 'They depend on neighbours\' ports, roads and political goodwill; transit delays, extra border crossings and longer distances raise costs and reduce competitiveness.'),
       ('Explain how a resource curse can reduce development.', 'Commodity exports raise the exchange rate (Dutch disease) and harm other exports; revenues encourage corruption and rent-seeking; price volatility destabilises budgets; competition for resources can fuel conflict (e.g. DR Congo minerals).'),
       ('Explain how political systems influence global interactions.', 'Open, stable governments attract investment and join trade blocs; authoritarian or isolationist regimes may restrict flows (North Korea); sanctions limit trade (Iran); conflict deters investment.'),
       ('Explain how a landlocked country can overcome its disadvantages.', 'Regional integration and transit agreements, investment in railways and dry ports (Ethiopia-Djibouti railway), exporting high-value, low-weight goods or services, and air cargo (Rwanda, Switzerland).')],
  contrast=[('physical factors affecting global participation', 'human factors affecting global participation', 'Physical factors include location, landlocked status, relief, climate and natural resources; human factors include political systems, policies, infrastructure, education and conflict.'),
            ('a landlocked high-income country', 'a landlocked low-income country', 'High-income landlocked states (Switzerland, Austria) have good transport links, EU membership and high-value exports; low-income ones (Chad, Niger) suffer high transit costs, poor infrastructure and dependence on unstable neighbours.')],
  misc=[('Being landlocked always prevents development.', 'Switzerland, Austria and Luxembourg are landlocked but very wealthy and globalised.'),
        ('Natural resources always lead to wealth.', 'Many resource-rich countries experience the resource curse, though good governance helped Botswana and Norway avoid it.'),
        ('Political factors only affect participation in the short term.', 'Policies such as China\'s opening from 1978 or North Korea\'s isolation have had long-lasting effects.')],
  apply=[('Using a named landlocked country, explain how it has tried to increase its global participation.', 'e.g. Ethiopia: about 95% of trade passes through Djibouti; the Chinese-built Addis Ababa-Djibouti electric railway (2016) cut transit from about 3 days by road to about 12 hours; growth of air cargo via Ethiopian Airlines (flowers to Europe).', 4),
         ('Suggest why Botswana avoided the resource curse.', 'Stable democratic institutions, transparent management of diamond revenue through the Debswana partnership with De Beers, and investment in education and infrastructure.', 3)],
  cases=[('Ethiopia and the Addis Ababa-Djibouti railway', 'about 95% of Ethiopia\'s trade passes through Djibouti, and the 752 km railway opened in 2016', 'overcoming landlocked disadvantage', 'investment in transit infrastructure reduces the costs of being landlocked'),
         ('Botswana\'s diamond economy', 'diamonds discovered after independence in 1966 helped make it an upper-middle-income country with stable democratic government', 'avoiding the resource curse', 'good governance can turn resources into development'),
         ('Shenzhen special economic zone', 'a fishing area of about 30,000 people in 1980 grew into a city of over 17 million producing electronics for global markets', 'political decisions and global participation', 'China\'s open-door policy drew the city into global networks'),
         ('the DR Congo\'s mineral wealth', 'it holds about 70% of world cobalt output, yet over 60% of the population lives in extreme poverty', 'the resource curse', 'conflict, corruption and foreign control limit the benefits of resources')],
  evaluate=[('Physical factors are more important than human factors in explaining global participation.', ['landlocked states have higher trade costs', 'resources attract investment'], ['Switzerland and Rwanda show policy can overcome geography', 'North Korea shows politics can isolate a coastal state'], 'Physical factors create advantages or barriers, but human factors largely decide participation.'),
            ('Natural resource wealth is more of a curse than a blessing for development.', ['DR Congo, Nigeria, Venezuela', 'Dutch disease and conflict'], ['Botswana, Norway, Chile used resources well', 'resources fund infrastructure and services'], 'Outcomes depend on governance and institutions rather than resources themselves.')],
  extended=[('Explain how physical and human factors influence the participation of countries in global interactions.', 'Location, landlocked status, resources and climate; political systems, conflict, policy, infrastructure and education; examples (Ethiopia, Botswana, Shenzhen, North Korea).', 10, 'long')],
  res=[('Table: cost to export a container (US$, World Bank Doing Business estimates) - Singapore 450; Kenya 2,250; Uganda 3,050; Chad 6,600; Central African Republic 5,500.',
        [('How many times more did it cost to export a container from Chad than from Singapore?', f'6,600 / 450 = {6600 / 450:.1f} times'),
         ('Explain the pattern shown.', 'Landlocked countries (Uganda, Chad, CAR) face much higher costs because goods travel long distances overland through neighbouring countries with border delays; Singapore is a highly efficient coastal hub.')]),
       ('Data: before the railway, a truck from Addis Ababa to Djibouti port took about 72 hours; the railway takes about 12 hours for 752 km.',
        [('Calculate the average speed of the railway journey.', f'752 / 12 = {752 / 12:.0f} km/h'),
         ('Calculate the percentage reduction in journey time.', f'(12 − 72)/72 × 100 = {pc(72, 12)}')])])

S('ch07-st3', gens=['freight', 'carbon', 'pct_climate'],
  terms=[('carbon footprint', 'the total greenhouse gas emissions caused by an activity, product or person, expressed as CO₂ equivalent'),
         ('food miles', 'the distance food travels from where it is produced to where it is consumed'),
         ('embedded emissions', 'greenhouse gases released during the production and transport of goods, which may be counted in the producing country rather than the consuming one'),
         ('carbon leakage', 'the shift of emissions-intensive production to countries with weaker climate policies'),
         ('consumption-based emissions', 'emissions accounted to the country where goods are consumed rather than produced')],
  facts=[('International shipping accounts for about what share of global greenhouse gas emissions?', 'About 3%', ['About 30%', 'About 0.01%', 'About 15%'], 'The IMO adopted a target of net zero by about 2050.'),
         ('Per tonne-kilometre, which mode of freight transport has the highest emissions?', 'Air freight', ['Container ship', 'Rail', 'Pipeline'], 'Air freight emits roughly 50 times more than shipping per tonne-km.'),
         ('The EU\'s Carbon Border Adjustment Mechanism (CBAM) aims to:', 'charge imports for their embedded carbon to prevent carbon leakage', ['ban all imports from Asia', 'subsidise air freight', 'abolish carbon pricing'], 'Its definitive phase starts in 2026.'),
         ('A UK study found that tomatoes grown in heated greenhouses in the UK can have:', 'a larger carbon footprint than tomatoes trucked from Spain', ['zero emissions', 'the same footprint as air-freighted ones', 'a lower footprint than locally grown field tomatoes in summer'], 'Food miles alone do not determine footprints.')],
  why=[('Explain why consumption-based emissions accounting gives different results from production-based accounting.', 'Goods made in China and consumed in Europe or the USA carry embedded emissions; production-based figures assign them to China, consumption-based figures to the importer, raising rich countries\' totals.'),
       ('Explain why food miles can be a misleading measure of environmental impact.', 'Production methods (heated greenhouses, fertilisers, land use) often create more emissions than transport, and transport mode matters - shipping is far less carbon-intensive than air.'),
       ('Explain why aviation and shipping are difficult to decarbonise.', 'They need energy-dense fuels; ships and aircraft last decades; international emissions are not assigned to any one country under the Paris Agreement; alternatives (ammonia, hydrogen, sustainable aviation fuel) are expensive and immature.'),
       ('Explain how global supply chains increase the carbon footprint of products.', 'Components travel between many countries for processing and assembly, adding transport emissions; production is often in countries with coal-heavy electricity.')],
  contrast=[('production-based emissions', 'consumption-based emissions', 'Production-based emissions are counted where goods are made; consumption-based emissions are counted where goods are consumed, including emissions embedded in imports.'),
            ('shipping', 'air freight', 'Shipping is slow but emits about 10-15 g CO₂ per tonne-km; air freight is fast but emits about 500-600 g per tonne-km, so is used for perishable or high-value goods.')],
  misc=[('Buying local food always has the lowest carbon footprint.', 'Local food produced in heated greenhouses or with high inputs can have a larger footprint than imported food shipped by sea.'),
        ('High-income countries have reduced their emissions mainly through efficiency.', 'Part of the reduction reflects offshoring of manufacturing; consumption-based emissions have fallen more slowly.'),
        ('International transport emissions are included in national Paris Agreement targets.', 'International aviation and shipping are dealt with separately by ICAO and the IMO.')],
  apply=[('Using a named product, explain the carbon footprint of its global supply chain.', 'e.g. Kenyan roses flown to the UK: grown in natural sunlight near Lake Naivasha with lower emissions than heated Dutch greenhouses, but air freight adds significant emissions; overall footprint can still be lower than Dutch roses.', 4),
         ('Suggest two ways TNCs could reduce the carbon footprint of their supply chains.', 'Shift from air to sea or rail freight; source renewable electricity for factories; nearshoring; efficient packaging and logistics; supplier emissions targets (Scope 3).', 2)],
  cases=[('Kenyan cut flowers', 'about 38% of EU rose imports come from Kenya, grown by Lake Naivasha and flown to Europe', 'the carbon footprint of air-freighted trade', 'production in natural sunlight can offset some air freight emissions'),
         ('the EU Carbon Border Adjustment Mechanism', 'from 2026 importers of steel, cement, aluminium, fertilisers, electricity and hydrogen must buy certificates for embedded emissions', 'responses to carbon leakage', 'trade policy is being used to price emissions in global supply chains'),
         ('Maersk\'s methanol-powered container ships', 'the world\'s first large methanol-enabled container ship entered service in 2024', 'decarbonising shipping', 'TNCs are investing in low-carbon fuels for global trade'),
         ('UK consumption-based emissions', 'UK territorial emissions fell about 50% between 1990 and 2022, but consumption-based emissions fell by much less', 'embedded emissions in trade', 'offshoring of production hides part of a country\'s footprint')],
  evaluate=[('Global trade is the main cause of rising greenhouse gas emissions.', ['transport emissions from shipping and aviation', 'carbon leakage to coal-based economies'], ['most emissions come from domestic energy, buildings and land use', 'trade can spread efficient technologies such as solar panels'], 'Trade contributes significantly, but domestic energy systems are the main cause.'),
            ('Consumers in high-income countries should be held responsible for emissions embedded in imports.', ['consumption drives production', 'fair accounting of footprints'], ['producers control technology and energy choices', 'hard to measure and enforce'], 'Responsibility should be shared between consumers, producers and governments.')],
  extended=[('Explain how global trade and transport contribute to carbon emissions.', 'Freight modes and emissions per tonne-km; supply chains; embedded emissions and carbon leakage; consumption vs production accounting; examples (Kenyan flowers, CBAM, shipping).', 10, 'long')],
  res=[('Table: emissions factors (g CO₂ per tonne-km, approximate) - container ship 12; rail 25; heavy goods vehicle 80; air freight 600. A 20-tonne shipment travels 9,000 km.',
        [('Calculate the emissions (tonnes CO₂) by ship and by air.', f'Ship: 20 × 9,000 × 12 / 10⁶ = {20 * 9000 * 12 / 1e6:.2f} t; air: 20 × 9,000 × 600 / 10⁶ = {20 * 9000 * 600 / 1e6:.0f} t'),
         ('Explain why some goods are still sent by air.', 'Perishable or high-value, time-sensitive goods (flowers, fruit, pharmaceuticals, electronics) justify the cost and emissions of fast transport.')]),
       ('Table: CO₂ emissions 2021 (million tonnes) - UK production-based 347, consumption-based 509; China production-based 11,470, consumption-based 10,340.',
        [('Calculate the percentage by which the UK\'s consumption-based emissions exceed its production-based emissions.', f'(509 − 347)/347 × 100 = {(509 - 347) / 347 * 100:.1f}%'),
         ('Explain why China shows the opposite pattern.', 'China is a net exporter of manufactured goods, so emissions from making goods consumed elsewhere are counted in its production-based total.')])])

# =============================================================================================
# HL extension: Human development and diversity
# =============================================================================================
S('ch08-st1', gens=['hdi', 'gini', 'mpi'],
  terms=[('Human Development Index (HDI)', 'a UNDP composite index (0-1) combining life expectancy, education (expected and mean years of schooling) and GNI per capita (PPP)'),
         ('Gini coefficient', 'a measure of income inequality from 0 (perfect equality) to 1 (one person has all income), derived from the Lorenz curve'),
         ('Gender Inequality Index (GII)', 'a UNDP index measuring gender-based disadvantage in reproductive health, empowerment and the labour market (0 = equality)'),
         ('Multidimensional Poverty Index (MPI)', 'an index produced by UNDP and OPHI measuring deprivation in health, education and living standards; MPI = H × A'),
         ('Lorenz curve', 'a graph plotting the cumulative share of income against the cumulative share of population; the further from the line of equality, the greater the inequality'),
         ('inequality-adjusted HDI (IHDI)', 'the HDI discounted for inequality in each dimension within a country')],
  facts=[('Which country had the highest HDI in the 2023/24 Human Development Report?', 'Switzerland', ['the USA', 'Japan', 'Qatar'], 'Switzerland scored 0.967 (2022 data), followed by Norway and Iceland.'),
         ('South Africa has one of the world\'s highest Gini coefficients, at about:', '0.63', ['0.25', '0.35', '0.95'], 'World Bank data show it as the most unequal country measured.'),
         ('In the MPI, a person is counted as multidimensionally poor if deprived in at least:', 'one-third of the weighted indicators', ['one indicator', 'all ten indicators', 'half the indicators'], 'There are 10 indicators across health, education and living standards.'),
         ('Which dimension is NOT part of the HDI?', 'Gender equality', ['Life expectancy at birth', 'Mean and expected years of schooling', 'GNI per capita (PPP)'], 'Gender is measured separately by the GII and GDI.')],
  why=[('Explain why the HDI is considered a better measure of development than GNI per capita alone.', 'It combines economic, health and education dimensions, reflecting quality of life rather than only income, so countries with similar incomes can be distinguished by health and education outcomes.'),
       ('Explain why a high GNI per capita does not always mean low inequality.', 'GNI per capita is an average that ignores distribution; income may be concentrated among a wealthy elite, as shown by high Gini coefficients in countries such as South Africa and Brazil.'),
       ('Explain how the MPI differs from income-based poverty measures.', 'It measures overlapping deprivations (nutrition, child mortality, schooling, sanitation, water, electricity, housing, cooking fuel, assets) at household level, showing how and where people are poor, not just how little money they have.'),
       ('Explain why the GII is useful for understanding development.', 'It reveals gender gaps hidden in national averages - maternal mortality, adolescent births, parliamentary seats, secondary education and labour force participation - which constrain development.')],
  contrast=[('the HDI', 'the MPI', 'The HDI is a national average of health, education and income achievements; the MPI measures the share and intensity of household deprivation across health, education and living standards.'),
            ('the Gini coefficient', 'GNI per capita', 'GNI per capita measures average income; the Gini coefficient measures how evenly income is distributed among the population.')],
  misc=[('A country with a high HDI has no poverty.', 'National averages hide poverty in regions, groups and households; the IHDI and MPI reveal these gaps.'),
        ('A Gini coefficient of 0.5 means half the population is poor.', 'It measures the distribution of income, not the proportion of people in poverty.'),
        ('Development can be measured accurately by a single index.', 'Every index omits aspects such as freedom, environmental sustainability and happiness, and depends on data quality and weightings.')],
  apply=[('Using named countries, explain why using several indicators gives a better picture of development than using one.', 'e.g. Qatar has very high GNI per capita but a lower HDI rank and high gender inequality; Cuba has modest income but high life expectancy and education; South Africa\'s HDI is medium-high but its Gini is about 0.63 and multidimensional poverty persists.', 4),
         ('Suggest why the HDI of oil-rich Gulf states ranks lower than their GNI per capita.', 'Education indicators, especially mean years of schooling among older adults, are lower than in other countries with similar incomes.', 2)],
  cases=[('South Africa\'s inequality', 'a Gini coefficient of about 0.63, with the top 10% of earners receiving over half of income', 'the Gini coefficient', 'national income averages hide extreme inequality rooted in apartheid'),
         ('multidimensional poverty in India', 'about 415 million people moved out of multidimensional poverty between 2005-06 and 2019-21', 'the MPI', 'improvements in sanitation, cooking fuel and schooling reduced deprivation'),
         ('Norway', 'it is one of the highest-ranked countries on the HDI (0.966) with a Gini of about 0.28', 'high development with low inequality', 'welfare policies and oil revenue invested in a sovereign fund support equality'),
         ('Niger', 'it has one of the lowest HDI scores (about 0.39) and over 60% of people are multidimensionally poor', 'low human development', 'low life expectancy, schooling and income combine with high fertility and climate stress')],
  evaluate=[('The HDI is the most useful measure of human development.', ['combines three dimensions', 'widely available data allow comparisons'], ['ignores inequality, gender, environment and freedom', 'national averages hide internal differences'], 'HDI is a useful starting point, but must be used with IHDI, GII, MPI and Gini.'),
            ('Income inequality is the greatest barrier to development.', ['high Gini limits poverty reduction (South Africa, Brazil)', 'unequal access to health and education'], ['absolute poverty, conflict and governance also matter', 'some unequal countries still develop rapidly (China)'], 'Inequality is a major barrier, but poverty levels, governance and conflict are also crucial.')],
  extended=[('Explain how and why different measures of development can give different pictures of a country\'s development.', 'HDI, GNI per capita, Gini, GII, MPI, IHDI; what each measures and omits; contrasting examples (Qatar, Cuba, South Africa, Norway, Niger).', 10, 'long')],
  res=[('Table: selected countries - Norway: HDI 0.966, Gini 0.28, GII 0.012; Brazil: HDI 0.760, Gini 0.52, GII 0.391; South Africa: HDI 0.717, Gini 0.63, GII 0.401; Niger: HDI 0.394, Gini 0.33, GII 0.609.',
        [('Rank the countries by Gini coefficient from least to most unequal.', 'Norway 0.28, Niger 0.33, Brazil 0.52, South Africa 0.63'),
         ('Suggest why Niger has low inequality but very low HDI.', 'Most people share similarly low incomes as subsistence farmers, so inequality is low even though health, education and income are all very low.')]),
       ('MPI data for a district: 48% of people are multidimensionally poor (H); the average intensity of deprivation among them is 52% (A).',
        [('Calculate the MPI using MPI = H × A.', f'0.48 × 0.52 = {0.48 * 0.52:.3f}'),
         ('Explain why both incidence and intensity are needed.', 'Incidence shows how many are poor; intensity shows how severely; a policy that helps the poorest reduces A even if H barely changes.')])])

S('ch08-st2', gens=['oda', 'remit', 'pct_global'],
  terms=[('trade liberalisation', 'the reduction of barriers to trade such as tariffs and quotas to integrate an economy into global markets'),
         ('microfinance', 'small loans and financial services for poor people, especially women, who lack access to banks, e.g. Grameen Bank'),
         ('gender empowerment', 'increasing women\'s access to education, income, property, decision-making and political representation'),
         ('demographic dividend', 'the economic growth possible when the working-age share of the population rises after fertility falls'),
         ('conditional cash transfer', 'regular payments to poor families on condition they meet requirements such as school attendance, e.g. Brazil\'s Bolsa Família'),
         ('top-down development', 'development projects planned by governments or large organisations, such as dams or highways')],
  facts=[('Bangladesh\'s Grameen Bank, founded by Muhammad Yunus, mainly lends to:', 'poor rural women', ['large corporations', 'foreign governments', 'commercial farmers in Europe'], 'Yunus and Grameen shared the 2006 Nobel Peace Prize.'),
         ('Brazil\'s Bolsa Família is an example of:', 'a conditional cash transfer programme', ['a free trade agreement', 'a structural adjustment programme', 'a mega-dam project'], 'It reached about 14 million families at its peak.'),
         ('Which country\'s growth since 1978 lifted about 800 million people out of extreme poverty?', 'China', ['Argentina', 'Russia', 'Nigeria'], 'World Bank estimate (2022).'),
         ('According to the UN, each additional year of secondary schooling for girls can raise their future earnings by about:', '10-20%', ['1%', '50-60%', '100%'], 'Education also lowers fertility and child mortality.')],
  why=[('Explain why the empowerment of women is important for development.', 'Educated women have fewer, healthier children, invest more in families, increase household incomes and labour force participation, and influence decision-making - multiplier effects across health, education and the economy.'),
       ('Explain how trade can promote development.', 'Exports bring foreign exchange, jobs and investment; access to larger markets allows economies of scale; technology transfer; e.g. the export-led growth of South Korea and Vietnam.'),
       ('Explain why aid does not always lead to development.', 'Aid may be tied, poorly targeted, captured by elites, create dependency or fund prestige projects; donor priorities may not match local needs.'),
       ('Explain why microfinance has been both praised and criticised.', 'It gives women capital to start businesses and gain independence, but high interest rates, small loans and over-indebtedness (Andhra Pradesh crisis 2010) limit its impact on poverty.')],
  contrast=[('top-down development', 'bottom-up development', 'Top-down development is planned by governments or agencies, often large-scale (dams, highways); bottom-up development is led by local communities, small-scale and uses local knowledge (wells, co-operatives).'),
            ('trade', 'aid', 'Trade involves earning income by selling goods and services in markets; aid is a transfer of resources from donors that does not need to be earned.')],
  misc=[('Economic growth automatically reduces poverty.', 'Growth may be captured by the rich; inclusive policies (education, health, transfers) are needed to reduce poverty.'),
        ('Women\'s empowerment only benefits women.', 'It raises household income, child health and education and national growth.'),
        ('Trade always benefits low-income countries.', 'Gains depend on what is traded; dependence on raw commodities and unfair rules can limit benefits.')],
  apply=[('Using a named example, explain how investment can contribute to development.', 'e.g. Vietnam: Doi Moi reforms (1986) and FDI from Samsung, Intel and others created export manufacturing jobs; poverty fell from about 50% in the early 1990s to under 5%; but wages remain low and profits flow abroad.', 4),
         ('Suggest how conditional cash transfers can reduce poverty over the long term.', 'Conditions on school attendance and health check-ups increase human capital so the next generation earns more, breaking the cycle of poverty.', 2)],
  cases=[('Vietnam\'s Doi Moi reforms', 'from 1986 market reforms and FDI turned it into a major exporter, and extreme poverty fell from about 50% to under 5%', 'trade and investment-led development', 'opening to trade and FDI drove rapid poverty reduction'),
         ('Brazil\'s Bolsa Família', 'conditional cash transfers to about 14 million families helped cut extreme poverty and raise school attendance', 'social policy for development', 'targeted transfers reduced poverty and inequality'),
         ('the Grameen Bank, Bangladesh', 'it has lent to over 10 million borrowers, about 97% of them women', 'microfinance and women\'s empowerment', 'small loans gave women income and status'),
         ('Rwanda\'s parliament', 'women hold about 61% of seats in the lower house, the highest share in the world', 'the role of women in development', 'political representation of women has been linked to gender-focused policies')],
  evaluate=[('Trade is more effective than aid in promoting development.', ['East Asian export-led growth', 'aid dependency risks'], ['aid funds health and education that markets underprovide', 'trade rules can disadvantage poor countries'], 'Trade drives long-term growth, but aid remains important for public goods and the poorest countries.'),
            ('Empowering women is the most effective strategy for development.', ['multiplier effects on health, education and income', 'demographic dividend'], ['requires wider change in governance, infrastructure and jobs', 'cultural and legal barriers'], 'Women\'s empowerment is among the most effective strategies, but it works best alongside economic and political reforms.')],
  extended=[('Explain how trade, aid, investment and the role of women can contribute to development.', 'Mechanisms of each; top-down vs bottom-up; examples (Vietnam, Bolsa Família, Grameen, Rwanda); limitations.', 10, 'long')],
  res=[('Table: Vietnam - share of population in extreme poverty (%): 1992 52; 2002 28; 2010 4; 2020 1; exports (US$ billion): 1992 2.5; 2020 283.',
        [('Calculate the percentage increase in Vietnam\'s exports from 1992 to 2020.', f'(283 − 2.5)/2.5 × 100 = {pc(2.5, 283)}'),
         ('Describe the relationship between exports and poverty shown.', 'As exports grew rapidly, extreme poverty fell steeply from about half the population to about 1%, suggesting export-led growth helped reduce poverty.')]),
       ('Table: total fertility rate by mother\'s education in a West African country - no schooling 6.2; primary 5.1; secondary 3.6; higher 2.3.',
        [('Calculate the difference in fertility between mothers with no schooling and those with higher education.', '6.2 − 2.3 = 3.9 children'),
         ('Explain the relationship shown.', 'Education delays marriage, increases awareness and use of contraception and labour market opportunities, so educated women have fewer children.')])])

S('ch08-st3', gens=['hdi', 'mpi', 'pct_pop'],
  terms=[('Sustainable Development Goals (SDGs)', '17 UN goals with 169 targets adopted in 2015 to achieve by 2030, including ending poverty, hunger and inequality'),
         ('Millennium Development Goals (MDGs)', 'eight UN development goals for 2000-2015, which the SDGs replaced'),
         ('human rights', 'the basic rights and freedoms belonging to every person, set out in the 1948 Universal Declaration of Human Rights'),
         ('extreme poverty', 'living on less than US$2.15 a day (2017 PPP), the World Bank international poverty line'),
         ('Universal Declaration of Human Rights', 'the 1948 UN document setting out 30 articles of fundamental human rights')],
  facts=[('How many Sustainable Development Goals are there?', '17', ['8', '10', '169'], 'They contain 169 targets.'),
         ('SDG 5 aims to:', 'achieve gender equality and empower all women and girls', ['end poverty everywhere', 'conserve oceans', 'build resilient infrastructure'], 'Targets include ending child marriage and FGM.'),
         ('The UN 2024 SDG report found that by 2024 about what share of SDG targets were on track?', 'About 17%', ['About 80%', 'About 50%', 'All of them'], 'Progress was set back by COVID-19, conflict and climate change.'),
         ('Child marriage is most prevalent in which region?', 'Sub-Saharan Africa', ['Western Europe', 'North America', 'Oceania'], 'Niger has one of the highest rates, at about 76% of women married before 18.')],
  why=[('Explain why progress towards the SDGs has slowed since 2020.', 'COVID-19 reversed poverty and education gains, conflict (Ukraine, Sudan, Gaza) and climate disasters displaced millions, food and energy prices rose, and debt limited government spending.'),
       ('Explain why human rights are linked to development.', 'Rights to education, health, work and political participation build capabilities (Sen\'s "development as freedom"); discrimination and denial of rights limit people\'s ability to escape poverty.'),
       ('Explain why the SDGs are broader than the MDGs.', 'They include environmental sustainability, inequality, cities, peace and governance, apply to all countries (not just developing ones) and were negotiated more widely.'),
       ('Explain why indigenous peoples often have lower development indicators.', 'Historic land dispossession, discrimination, remoteness from services, language barriers and lack of political representation, e.g. Aboriginal Australians\' lower life expectancy.')],
  contrast=[('the MDGs', 'the SDGs', 'The MDGs (2000-2015) had 8 goals focused mainly on poverty, health and education in developing countries; the SDGs (2015-2030) have 17 universal goals including sustainability, inequality and governance.'),
            ('civil and political rights', 'economic and social rights', 'Civil and political rights include free speech, voting and fair trial; economic and social rights include education, health, work and adequate living standards.')],
  misc=[('The SDGs only apply to low-income countries.', 'They are universal and apply to all countries, including targets on inequality and consumption in high-income countries.'),
        ('Extreme poverty has been eliminated.', 'About 700 million people still lived in extreme poverty in 2024, mostly in sub-Saharan Africa.'),
        ('Economic growth guarantees human rights.', 'Growth can coexist with abuses of labour, gender or political rights; rights need laws and institutions.')],
  apply=[('Using a named example, explain progress towards one SDG.', 'e.g. SDG 4 (education) in Ethiopia: primary enrolment rose from about 30% in the mid-1990s to over 85%; but quality, secondary completion and conflict in Tigray remain challenges.', 4),
         ('Suggest why measuring progress towards the SDGs is difficult.', 'Many indicators lack data in poorer countries; 169 targets are complex; national averages hide inequalities; definitions vary.', 2)],
  cases=[('child marriage in Bangladesh', 'about half of women aged 20-24 were married before 18, despite the legal minimum age of 18', 'human rights and gender inequality', 'social norms and poverty limit girls\' rights and development'),
         ('indigenous Australians', 'the life expectancy gap with non-Indigenous Australians was about 8-9 years in 2015-17', 'inequality in a high-income country', 'historic dispossession and discrimination create persistent gaps'),
         ('Ethiopia\'s primary education expansion', 'primary enrolment rose from about 30% to over 85% since the mid-1990s', 'progress towards SDG 4', 'government investment in schools expanded access rapidly'),
         ('poverty reduction in China', 'extreme poverty was officially declared eliminated in 2021', 'progress towards SDG 1', 'rapid growth and targeted programmes cut poverty on a huge scale')],
  evaluate=[('The world will achieve most of the Sustainable Development Goals by 2030.', ['progress on poverty, child mortality and education before 2020', 'global framework and monitoring'], ['only about 17% of targets on track in 2024', 'COVID-19, conflict, climate change and debt'], 'Most goals are unlikely to be met by 2030, though progress continues in some areas.'),
            ('Human rights are more important than economic growth for development.', ['development as freedom (Sen)', 'rights protect the vulnerable'], ['growth funds services and lifts millions out of poverty (China)', 'both are interdependent'], 'Rights and growth are mutually reinforcing; sustainable development requires both.')],
  extended=[('Explain the relationship between human rights and progress towards the Sustainable Development Goals.', 'SDGs and their targets; rights to education, health, gender equality; examples (child marriage, indigenous peoples, Ethiopia, China); barriers to progress.', 10, 'long')],
  res=[('Table: people in extreme poverty (millions, World Bank, US$2.15/day) - 1990: 2,000; 2010: 1,140; 2019: 670; 2022: 712.',
        [('Calculate the percentage change from 1990 to 2019.', f'(670 − 2,000)/2,000 × 100 = {pc(2000, 670)}'),
         ('Suggest reasons for the increase after 2019.', 'COVID-19 job losses, rising food and energy prices after the war in Ukraine, conflict and debt crises.')]),
       ('Table: girls married before 18 (% of women aged 20-24) - Niger 76; Chad 61; Bangladesh 51; India 23; Brazil 26.',
        [('Calculate the mean of the five values.', f'(76 + 61 + 51 + 23 + 26)/5 = {(76 + 61 + 51 + 23 + 26) / 5:.1f}%'),
         ('Explain how child marriage affects progress towards the SDGs.', 'It ends schooling (SDG 4), increases early pregnancy and maternal mortality (SDG 3), limits women\'s economic participation (SDG 5, 8) and perpetuates poverty (SDG 1).')])])

S('ch09-st1', gens=['pct_global', 'chi_culture', 'chi_global'],
  terms=[('cultural diffusion', 'the spread of cultural traits such as language, religion, food, music and ideas from one place or group to another'),
         ('cultural imperialism', 'the imposition of one culture, often Western or American, over others through media, brands and economic power'),
         ('glocalisation', 'the adaptation of global products or services to local cultures, tastes and laws'),
         ('cultural homogenisation', 'the reduction of cultural diversity as a dominant global culture spreads'),
         ('Americanisation', 'the spread of US culture, brands and consumption patterns, e.g. fast food, Hollywood and social media'),
         ('cultural hybridity', 'the mixing of elements from different cultures to create new forms')],
  facts=[('McDonald\'s menus in India do not include beef because:', 'most Hindus do not eat beef', ['beef is not available anywhere in Asia', 'India banned all fast food', 'it is too expensive to import'], 'The Maharaja Mac uses chicken.'),
         ('Which is an example of glocalisation?', 'MTV producing local-language channels with local music', ['A global brand selling identical products everywhere', 'A country banning foreign films', 'A local language dying out'], 'Firms adapt global formats to local tastes.'),
         ('"McDonaldization" (efficiency, calculability, predictability, control) was described by:', 'George Ritzer', ['Joseph Nye', 'David Harvey', 'Edward Said'], 'Ritzer\'s book was published in 1993.'),
         ('The global spread of K-pop is an example of:', 'reverse cultural flow from Asia to the West', ['cultural imperialism by the USA', 'cultural homogenisation by Europe', 'isolationism'], 'Global culture is increasingly multi-directional.')],
  why=[('Explain why global brands often adopt glocalisation strategies.', 'Local tastes, religions, languages and laws vary; adapting products (McDonald\'s McAloo Tikki, KFC\'s congee in China) increases sales and acceptance and reduces opposition to foreign firms.'),
       ('Explain how the media contribute to cultural diffusion.', 'Films, TV, streaming platforms (Netflix), social media and music spread values, language, fashion and consumer brands worldwide almost instantly.'),
       ('Explain why some people see globalisation as cultural imperialism.', 'Dominant Western media, brands and English language spread through economic power, can displace local languages, foods and traditions, and promote consumerism.'),
       ('Explain why cultural diffusion is not simply one-way.', 'Migration, the internet and growing economies of emerging countries spread Asian, African and Latin American culture globally - K-pop, Bollywood, Nollywood, anime, sushi and reggaeton.')],
  contrast=[('cultural imperialism', 'glocalisation', 'Cultural imperialism is the imposition of a dominant culture on others; glocalisation is the adaptation of global products to fit local culture.'),
            ('cultural homogenisation', 'cultural hybridity', 'Homogenisation reduces diversity as places become more similar; hybridity creates new cultural forms by mixing elements from different cultures.')],
  misc=[('Globalisation is making all cultures identical.', 'Global flows also strengthen local identities, create hybrid forms and spread non-Western culture.'),
        ('Glocalisation means TNCs abandon their global brand.', 'They keep core brands and systems while adapting particular products, marketing and menus.'),
        ('Cultural diffusion only happens through TNCs.', 'Migration, tourism, education, religion and social media are also major channels.')],
  apply=[('Using named examples, explain how TNCs adapt products to local cultures.', 'e.g. McDonald\'s: no beef or pork in India (McAloo Tikki, Maharaja Mac), halal in Muslim countries, teriyaki burger in Japan; Netflix producing local content such as Squid Game (Korea) and Sacred Games (India).', 4),
         ('Suggest one way governments try to protect national culture from cultural imperialism.', 'Quotas for local content on radio and TV (France, Canada, South Korea\'s screen quota), subsidies for local film, restrictions on foreign media.', 2)],
  cases=[('McDonald\'s in India', 'its menu has no beef or pork, with items such as the McAloo Tikki and separate vegetarian kitchens', 'glocalisation', 'a global brand adapted products to religious and cultural values'),
         ('France\'s cultural exception policy', 'French radio must broadcast at least 40% French-language songs, and cinema is subsidised', 'resistance to cultural imperialism', 'governments can protect national culture through quotas'),
         ('the Korean Wave', 'K-pop and Korean dramas reached audiences across Asia, the Americas and Europe, and Squid Game became Netflix\'s most-watched series in 2021', 'multi-directional cultural flows', 'non-Western culture can spread globally through digital platforms'),
         ('Nollywood, Nigeria', 'it produces over 2,500 films a year, the second largest film industry by output after Bollywood', 'cultural production in the Global South', 'local industries compete with Hollywood and spread African culture')],
  evaluate=[('Globalisation is leading to cultural homogenisation.', ['spread of global brands, English and Hollywood', 'loss of languages and traditions'], ['glocalisation and hybridity', 'reverse flows (K-pop, Nollywood) and revival of local identities'], 'Global culture spreads, but it is adapted, resisted and mixed rather than simply homogenised.'),
            ('Glocalisation benefits local cultures.', ['respects religious and cultural values', 'creates local jobs and content'], ['still spreads global consumerism and brands', 'can commodify and superficially represent culture'], 'Glocalisation reduces cultural conflict but mainly serves TNC profits.')],
  extended=[('Explain how cultural diffusion, cultural imperialism and glocalisation are changing cultures.', 'Channels of diffusion (media, TNCs, migration, internet); Americanisation; glocalisation (McDonald\'s, Netflix); reverse flows (K-pop, Nollywood); resistance (France).', 10, 'long')],
  res=[('Table: share of box-office revenue from US films (approximate) - UK 70%; Germany 65%; France 45%; Japan 30%; South Korea 40%; India 10%.',
        [('Calculate the range of the data.', '70 − 10 = 60 percentage points'),
         ('Suggest why the share is lower in India and France.', 'India has a huge domestic film industry (Bollywood and regional cinemas) in local languages; France protects and subsidises French cinema.')]),
       ('Survey of 100 shoppers in a mall in Bangkok: 64 had eaten at a US fast-food chain in the last month; 41 said they preferred local adapted menu items; 23 preferred standard global items.',
        [('Calculate the percentage of fast-food customers who preferred local adapted items.', f'41/64 × 100 = {41 / 64 * 100:.1f}%'),
         ('Explain what the survey suggests about glocalisation.', 'Most customers of global chains preferred adapted local items, suggesting glocalisation helps global brands succeed.')])])

S('ch09-st2', gens=['remit', 'migration', 'chi_culture'],
  terms=[('diaspora', 'a population that has spread from its original homeland but keeps cultural, social or economic links with it'),
         ('hybrid identity', 'an identity combining elements of more than one culture, often among migrants and their descendants'),
         ('ethnic enclave', 'an area of a city with a concentration of one ethnic or cultural group, e.g. Chinatown in San Francisco'),
         ('assimilation', 'the process by which migrants adopt the culture of the host society'),
         ('multiculturalism', 'policies or attitudes that support the coexistence of different cultural groups with their own identities'),
         ('transnationalism', 'the maintenance of social, economic and political ties across national borders by migrants')],
  facts=[('The world\'s largest diaspora by country of origin is that of:', 'India (about 18 million emigrants)', ['Canada', 'Japan', 'Australia'], 'Large Indian communities live in the Gulf, the USA and the UK.'),
         ('Which city has the largest Chinatown outside Asia by many estimates?', 'New York', ['Rome', 'Moscow', 'Buenos Aires'], 'San Francisco\'s is the oldest in North America.'),
         ('The Chinese diaspora is estimated at about:', '50-60 million people', ['500,000 people', '5 million people', '500 million people'], 'Many live in South-East Asia.'),
         ('Nigeria\'s diaspora sent home remittances worth about what in 2023?', 'US$20 billion', ['US$200 million', 'US$2 billion', 'US$200 billion'], 'Remittances exceed ODA and often FDI.')],
  why=[('Explain how diasporas spread culture.', 'Migrants bring food, music, religion, festivals and language to host societies (e.g. Diwali in Leicester, Notting Hill Carnival); they also send ideas and goods home, and online media connect diaspora and homeland.'),
       ('Explain why second-generation migrants often develop hybrid identities.', 'They grow up between their parents\' heritage culture at home and the host culture at school and work, combining language, faith, food and values to create new identities such as "British Asian".'),
       ('Explain why ethnic enclaves form in cities.', 'Chain migration to join family; cheaper housing; support networks, shops and places of worship; protection from discrimination; and employment in community businesses.'),
       ('Explain how diasporas influence their countries of origin.', 'Remittances, investment, return migration, skills transfer, lobbying of host governments and political involvement, e.g. Indian diaspora investors in Bengaluru IT.')],
  contrast=[('assimilation', 'multiculturalism', 'Assimilation expects migrants to adopt the host culture and lose distinctive traits; multiculturalism supports groups keeping their identities within shared laws and citizenship.'),
            ('a diaspora', 'an ethnic enclave', 'A diaspora is a dispersed global population sharing an origin; an ethnic enclave is a specific neighbourhood with a concentration of one group.')],
  misc=[('Migrants either keep their culture or adopt the host culture.', 'Many develop hybrid identities and change both the host and home cultures.'),
        ('Diasporas lose contact with their homeland.', 'Cheap travel, phones and social media allow constant transnational links.'),
        ('Ethnic enclaves show a failure of integration.', 'Enclaves can provide support and businesses that help migrants integrate economically over time.')],
  apply=[('Using a named diaspora, explain its influence on a host country\'s culture.', 'e.g. the South Asian diaspora in the UK: about 5 million people; curry houses and "chicken tikka masala"; Bollywood and bhangra; Diwali in Leicester (one of the largest outside India); British Asian politicians and business leaders.', 4),
         ('Suggest how social media has changed links between diasporas and their homelands.', 'Instant, cheap communication; sharing of news, music and fashion; online remittances; diaspora political campaigns; virtual communities.', 2)],
  cases=[('Leicester, UK', 'about 43% of the population identified as Asian or British Asian in 2021, and the city hosts one of the largest Diwali celebrations outside India', 'diaspora cultural influence', 'migrant communities have reshaped a host city\'s cultural landscape'),
         ('the Filipino diaspora', 'about 10 million Filipinos live or work abroad, sending remittances equal to about 9% of GDP', 'transnational ties', 'migrants maintain strong economic and family links with home'),
         ('Chinatown in San Francisco', 'founded in the 1840s, it is the oldest Chinatown in North America', 'ethnic enclaves', 'concentrations of migrants preserve and display cultural identity'),
         ('the Turkish diaspora in Germany', 'about 3 million people of Turkish origin live in Germany, many descended from 1960s guest workers', 'hybrid identities', 'second and third generations combine German and Turkish identities')],
  evaluate=[('Diasporas are the most important way in which culture spreads.', ['bring food, faith and music directly into host societies', 'transnational links'], ['media, TNCs and the internet reach far more people', 'tourism and education also spread culture'], 'Diasporas are a powerful channel, especially for everyday culture, but media and TNCs spread culture more widely.'),
            ('Hybrid identities strengthen rather than weaken national cultures.', ['create new forms of music, food and language', 'add diversity and creativity'], ['some see loss of tradition', 'tensions over integration and identity politics'], 'Hybridity usually enriches cultures, though it can create tensions about identity.')],
  extended=[('Explain how diasporas spread culture and create hybrid identities.', 'Definition and examples (Indian, Chinese, Filipino, Turkish diasporas); enclaves; festivals and food; transnationalism; second-generation hybrid identities; effects on host and origin.', 10, 'long')],
  res=[('Table: population of Leicester by ethnic group (2021 census, %) - White 40.9; Asian or Asian British 43.4; Black 7.8; Mixed 3.8; other 4.1. Total population about 368,600.',
        [('Calculate the approximate number of people identifying as Asian or Asian British.', f'43.4% × 368,600 = {0.434 * 368600:,.0f}'),
         ('Suggest how this has influenced the city\'s cultural landscape.', 'Temples, mosques and gurdwaras; the "Golden Mile" of Indian shops and restaurants on Belgrave Road; large Diwali and Vaisakhi festivals.')]),
       ('Survey of 80 second-generation migrants: 52 described themselves with a hyphenated or dual identity (e.g. "British-Indian"), 18 with only the host nationality and 10 with only their parents\' nationality.',
        [('Calculate the percentage with a dual identity.', '52/80 × 100 = 65%'),
         ('Explain what this suggests about cultural identity.', 'Most second-generation migrants develop hybrid identities combining heritage and host cultures.')])])

S('ch09-st3', gens=['diversity', 'pct_global', 'chi_culture'],
  terms=[('cultural diversity', 'the variety of cultural groups, languages, religions and traditions in a place'),
         ('language endangerment', 'the threat that a language will cease to be spoken as fewer children learn it'),
         ('Greenberg\'s diversity index', 'a measure of linguistic diversity: the probability that two randomly chosen people in a population have different first languages (1 − Σp²)'),
         ('language revitalisation', 'efforts to increase the use of an endangered language, through schools, media and official status'),
         ('lingua franca', 'a language used for communication between people with different first languages, e.g. English, Swahili')],
  facts=[('About how many languages are spoken in the world today?', 'About 7,000', ['About 70', 'About 700', 'About 70,000'], 'Ethnologue lists about 7,160 living languages.'),
         ('Which country has the greatest number of living languages?', 'Papua New Guinea (about 840)', ['the USA', 'China', 'Brazil'], 'It has the highest linguistic diversity in the world.'),
         ('UNESCO estimates that what proportion of the world\'s languages are endangered?', 'About 40%', ['About 1%', 'About 10%', 'About 90%'], 'Many have fewer than 1,000 speakers.'),
         ('Which language has been successfully revived as an everyday language with millions of speakers?', 'Hebrew', ['Latin', 'Manx', 'Cornish'], 'Modern Hebrew is spoken by about 9 million people.')],
  why=[('Explain why many languages are endangered.', 'Dominant national and global languages (English, Spanish, Mandarin) are needed for education, jobs and the internet; urbanisation and migration break up communities; parents stop passing languages to children; historic suppression (e.g. residential schools).'),
       ('Explain how language revitalisation programmes work.', 'Immersion schools and pre-schools (Māori kōhanga reo), official status, media and digital content, adult classes, and community pride increase the number of young speakers.'),
       ('Explain why measuring cultural diversity is difficult.', 'Cultures and languages have fuzzy boundaries (dialects), people have multiple identities, censuses use different categories, and indices such as Greenberg\'s focus on single attributes.'),
       ('Explain why the loss of languages matters.', 'Languages carry knowledge of local environments, medicine, history and identity; their loss reduces cultural diversity and can harm wellbeing of indigenous communities.')],
  contrast=[('linguistic diversity', 'religious diversity', 'Linguistic diversity is the variety of languages spoken in an area; religious diversity is the variety of faiths practised.'),
            ('an endangered language', 'an extinct language', 'An endangered language still has speakers but children are not learning it; an extinct language has no remaining native speakers.')],
  misc=[('Language loss is caused only by globalisation.', 'Colonial policies, national language laws and urbanisation also caused much language loss.'),
        ('Once a language is endangered, it cannot recover.', 'Revitalisation has succeeded for Hebrew, Welsh and Māori, among others.'),
        ('A high diversity index means a country is in conflict.', 'The index measures diversity, not conflict; many diverse countries such as Tanzania are stable.')],
  apply=[('Using a named example, explain how a minority language has been revitalised.', 'e.g. Welsh: the Welsh Language Act 1993 and 2011 Measure, Welsh-medium schools, S4C TV channel (1982) and bilingual signs; about 538,000 speakers (17.8%) in 2021, with the goal of a million by 2050.', 4),
         ('Suggest why Papua New Guinea has so many languages.', 'Rugged mountains, dense forest and islands isolated communities for thousands of years; small clan-based societies; limited colonial unification.', 2)],
  cases=[('te reo Māori in New Zealand', 'kōhanga reo language nests from 1982, official status in 1987 and Māori Television helped increase speakers', 'language revitalisation', 'education and official recognition can reverse language decline'),
         ('the Welsh language', 'about 538,000 people (17.8%) spoke Welsh in 2021, and the government aims for a million speakers by 2050', 'minority language policy', 'legislation, media and schooling support a minority language'),
         ('Papua New Guinea', 'about 840 languages are spoken by about 10 million people, the highest linguistic diversity in the world', 'cultural diversity', 'physical isolation preserved many distinct languages'),
         ('the extinction of Manx', 'the last native speaker died in 1974, although a revival movement has created new speakers', 'language loss and revival', 'languages can be lost within a few generations but revived through community effort')],
  evaluate=[('Globalisation is the main cause of the loss of languages.', ['English and other global languages dominate trade, internet and education', 'migration to cities'], ['colonial and national policies (residential schools, French in France)', 'internet also helps minority language revival'], 'Globalisation accelerates language loss, but historic political policies were often more important.'),
            ('The Greenberg diversity index is a useful measure of cultural diversity.', ['simple, comparable, probability-based', 'easy to calculate from census data'], ['ignores multilingualism, dialects and other cultural traits', 'depends on census categories'], 'It is useful for comparing linguistic diversity, but it captures only one aspect of culture.')],
  extended=[('Explain why cultural diversity is changing and how it can be measured.', 'Causes of language loss and revival; Greenberg\'s index; endangered languages; examples (PNG, Welsh, Māori, Manx).', 10, 'long')],
  res=[('Table: languages spoken at home in a city - language A 50%; language B 30%; language C 20%.',
        [('Calculate Greenberg\'s diversity index (1 − Σp²).', f'1 − (0.5² + 0.3² + 0.2²) = 1 − {0.25 + 0.09 + 0.04:.2f} = {1 - 0.38:.2f}'),
         ('Interpret the result.', 'There is a 62% probability that two randomly chosen residents speak different home languages - moderately high diversity.')]),
       ('Data: Welsh speakers aged 3+ in Wales - 1911: 43.5%; 1971: 20.8%; 2011: 19.0%; 2021: 17.8%.',
        [('Calculate the percentage change in the share of Welsh speakers from 1911 to 2021.', f'(17.8 − 43.5)/43.5 × 100 = {pc(43.5, 17.8)}'),
         ('Suggest why the rate of decline slowed after 1971.', 'Language activism, Welsh-medium schools, S4C television and the Welsh Language Acts supported the language.')])])

S('ch10-st1', gens=['chi_global', 'pct_global', 'stats_dev'],
  terms=[('anti-globalisation movement', 'a loose coalition of groups opposing aspects of corporate globalisation, such as free trade rules, TNC power and inequality'),
         ('localism', 'support for local production, consumption, businesses and decision-making in preference to global ones'),
         ('civil society', 'organisations and groups outside government and business, such as NGOs, trade unions, faith groups and community associations'),
         ('Fairtrade', 'a certification system guaranteeing producers in developing countries minimum prices and a social premium'),
         ('transition town', 'a community-led movement to increase local self-reliance and reduce carbon emissions, started in Totnes, UK, in 2006'),
         ('ethical consumerism', 'buying goods produced in ways that minimise harm to people, animals and the environment')],
  facts=[('The 1999 protests known as the "Battle of Seattle" targeted a meeting of:', 'the World Trade Organization', ['the United Nations General Assembly', 'the Olympic Committee', 'NATO'], 'About 40,000 people protested and the talks collapsed.'),
         ('The Transition Towns movement began in which town?', 'Totnes, England', ['Seattle, USA', 'Porto Alegre, Brazil', 'Davos, Switzerland'], 'It has spread to over 1,000 communities worldwide.'),
         ('The World Social Forum was first held in 2001 in:', 'Porto Alegre, Brazil', ['Davos, Switzerland', 'New York, USA', 'Geneva, Switzerland'], 'It was set up as a counterpoint to the World Economic Forum.'),
         ('The Bristol Pound and the Brixton Pound were examples of:', 'local currencies to keep spending in local economies', ['national currencies', 'cryptocurrencies issued by central banks', 'global reserve currencies'], 'The Bristol Pound operated from 2012 to 2021.')],
  why=[('Explain why some groups oppose globalisation.', 'Concerns about TNC power, job losses from offshoring, low wages and poor conditions in supply chains, environmental damage, loss of cultural identity and national sovereignty, and rising inequality.'),
       ('Explain how localism can be a response to globalisation.', 'Communities support local food, businesses, currencies and energy to keep money circulating locally (local multiplier), reduce food miles and emissions, and maintain identity and control.'),
       ('Explain how civil society can influence TNCs.', 'NGO campaigns, boycotts, investigations and social media pressure damage brand reputation, pushing TNCs to adopt codes of conduct, supply-chain audits and Fairtrade sourcing, e.g. after Rana Plaza (the Bangladesh Accord).'),
       ('Explain why anti-globalisation movements are diverse.', 'They include environmental, labour, indigenous, religious and nationalist groups with different aims - some want fairer globalisation (alter-globalisation), others want less globalisation and more national control.')],
  contrast=[('anti-globalisation', 'alter-globalisation', 'Anti-globalisation rejects many aspects of global integration; alter-globalisation accepts global connections but seeks fairer, more democratic and sustainable forms.'),
            ('Fairtrade', 'free trade', 'Free trade removes barriers so market prices decide trade; Fairtrade sets minimum prices and premiums to protect producers from low world prices.')],
  misc=[('Anti-globalisation protesters reject all global connections.', 'Many use global networks and social media, and seek fairer rules rather than an end to trade.'),
        ('Local production always has lower environmental impacts.', 'Local food grown in heated greenhouses or with inefficient methods can have a larger footprint than imported food.'),
        ('Fairtrade guarantees farmers escape poverty.', 'Premiums help, but certification costs, small volumes sold at Fairtrade prices and low productivity limit benefits.')],
  apply=[('Using a named example, explain how a local community has responded to globalisation.', 'e.g. Totnes, UK: Transition Town since 2006 - local food networks, community energy (Totnes Renewable Energy Society), the Totnes Pound (2007-2019), and opposition to a Costa Coffee branch in 2012.', 4),
         ('Suggest one benefit and one limitation of local currencies.', 'Benefit: keeps spending within local businesses, increasing the local multiplier; limitation: limited acceptance and use, so many have closed (Bristol Pound 2021).', 2)],
  cases=[('the 1999 "Battle of Seattle"', 'about 40,000 protesters disrupted the WTO ministerial meeting, which ended without agreement', 'anti-globalisation protest', 'civil society coalitions can disrupt global governance'),
         ('Totnes Transition Town, UK', 'since 2006 the community has developed local food, energy and currency schemes', 'localism', 'local action aims to build resilience and reduce dependence on global systems'),
         ('the Bangladesh Accord on Fire and Building Safety', 'after the 2013 Rana Plaza collapse, over 200 brands signed a legally binding agreement on factory inspections', 'civil society pressure on TNCs', 'campaigns by unions and NGOs forced changes in supply-chain standards'),
         ('Via Campesina', 'an international peasant movement with about 200 million members in over 80 countries campaigns for food sovereignty', 'transnational civil society', 'small farmers organise globally to resist agribusiness and trade rules')],
  evaluate=[('Anti-globalisation movements have been successful in changing global interactions.', ['Bangladesh Accord, Fairtrade growth', 'stalled WTO negotiations'], ['global trade and TNC power have continued to grow', 'local initiatives small in scale'], 'They have influenced standards and debate, but have not reversed globalisation.'),
            ('Localism is an effective response to the negative effects of globalisation.', ['local multiplier, identity, lower food miles in some cases', 'community resilience'], ['small scale; higher costs; local currencies often fail', 'cannot replace global supply chains for most goods'], 'Localism brings community benefits but is a limited response to global forces.')],
  extended=[('Explain how civil society and local communities resist or modify the effects of globalisation.', 'Anti- and alter-globalisation; protests (Seattle); localism (Totnes, local currencies); Fairtrade and ethical consumption; NGO campaigns (Rana Plaza, Bangladesh Accord); Via Campesina.', 10, 'long')],
  res=[('Data: in a local multiplier study, £100 spent with a local supplier generated £176 for the local economy, while £100 spent with a non-local chain generated £136.',
        [('Calculate the local multiplier for each type of spending.', 'Local: 176/100 = 1.76; non-local: 136/100 = 1.36'),
         ('Explain why local spending generates a higher multiplier.', 'Local firms employ local people, buy from local suppliers and keep profits in the area, so more money is re-spent locally.')]),
       ('Table: Fairtrade retail sales (€ billion, global, approximate) - 2004: 0.8; 2010: 4.4; 2016: 7.9; 2022: 12.0.',
        [('Calculate the percentage increase from 2004 to 2022.', f'(12.0 − 0.8)/0.8 × 100 = {pc(0.8, 12.0)}'),
         ('Suggest one reason for the growth.', 'Rising ethical consumerism, campaigns by NGOs and supermarket adoption of Fairtrade products.')])])

S('ch10-st2', gens=['tariff', 'migration', 'pct_global'],
  terms=[('protectionism', 'government policies that restrict imports to protect domestic industries, such as tariffs, quotas and subsidies'),
         ('tariff', 'a tax on imported goods that raises their price relative to domestic goods'),
         ('quota', 'a limit on the quantity of a good that can be imported'),
         ('trade war', 'a situation where countries impose rising tariffs on each other\'s goods in retaliation'),
         ('border control', 'measures to regulate the movement of people and goods across national borders, such as visas, checks and walls'),
         ('economic nationalism', 'policies that prioritise domestic control of the economy, labour and capital, often with tariffs and limits on foreign ownership')],
  facts=[('The UK formally left the European Union on:', '31 January 2020', ['23 June 2016', '1 January 2016', '31 December 2024'], 'The transition period ended on 31 December 2020.'),
         ('In 2018 the USA imposed tariffs of 25% on imports of:', 'steel', ['crude oil', 'coffee', 'bananas'], 'A 10% tariff was placed on aluminium.'),
         ('Which agreement replaced NAFTA in 2020?', 'USMCA (CUSMA)', ['CPTPP', 'RCEP', 'Mercosur'], 'It includes the USA, Mexico and Canada.'),
         ('The EU\'s Common Agricultural Policy is an example of:', 'agricultural subsidies that protect farmers', ['a free trade agreement with Africa', 'a migration control', 'a cultural exchange programme'], 'It accounts for about a third of the EU budget.')],
  why=[('Explain why governments may adopt protectionist policies.', 'To protect jobs and infant industries, respond to unfair competition or dumping, secure strategic industries (steel, semiconductors), reduce trade deficits and respond to public opinion.'),
       ('Explain why the vote for Brexit was partly a response to globalisation.', 'Concerns about EU migration under free movement, loss of sovereignty to EU law, deindustrialisation in northern England and Wales, and feeling "left behind" by globalisation.'),
       ('Explain how tariffs can harm the country that imposes them.', 'They raise prices for consumers and firms using imported components, provoke retaliation against exports (e.g. Chinese tariffs on US soybeans in 2018), and reduce efficiency.'),
       ('Explain why some countries build border walls or fences.', 'To control irregular migration, smuggling and security threats and to respond to political pressure, e.g. the US-Mexico barrier, Hungary\'s fence (2015), India-Bangladesh fence.')],
  contrast=[('free trade', 'protectionism', 'Free trade removes tariffs and quotas so goods move freely; protectionism imposes barriers to shield domestic producers.'),
            ('tariffs', 'quotas', 'Tariffs tax imports, raising prices but allowing unlimited quantity; quotas limit the quantity imported regardless of price.')],
  misc=[('Protectionism always protects jobs.', 'Jobs may be saved in protected industries but lost in industries using imported inputs or facing retaliation.'),
        ('Brexit ended migration to the UK.', 'Net migration rose to record levels after 2021, but from non-EU countries.'),
        ('Border walls stop irregular migration.', 'They redirect routes, raise smuggling costs and dangers, but do not stop migration driven by economic and political factors.')],
  apply=[('Using a named example, explain the effects of a trade war.', 'e.g. US-China trade war from 2018: US tariffs on about US$360 billion of Chinese goods and Chinese tariffs on about US$110 billion of US goods; US soybean exports to China fell sharply; firms shifted production to Vietnam and Mexico; US consumers paid higher prices.', 4),
         ('Suggest why Brexit affected trade between Great Britain and Northern Ireland.', 'The Northern Ireland Protocol (later the Windsor Framework) kept Northern Ireland in the EU single market for goods to avoid a hard border with Ireland, so checks were introduced on goods crossing the Irish Sea.', 3)],
  cases=[('Brexit', 'the 2016 referendum (52% Leave) led the UK to leave the EU in 2020, ending free movement and creating new customs checks', 'political responses to migration and trade', 'concerns about sovereignty and migration led to withdrawal from a trade bloc'),
         ('the US-China trade war', 'tariffs from 2018 covered hundreds of billions of dollars of goods, and US soybean exports to China fell by about 75% in 2018', 'protectionism', 'tariff escalation disrupted trade flows and shifted supply chains'),
         ('Hungary\'s border fence', 'a 175 km fence on the Serbian border was built in 2015 during the European migration crisis', 'border controls', 'states responded to large migration flows by hardening borders'),
         ('India\'s 2019 withdrawal from RCEP negotiations', 'India left the talks over fears that Chinese imports would harm its farmers and manufacturers', 'economic nationalism', 'governments may reject trade deals to protect domestic producers')],
  evaluate=[('Protectionism is an effective response to the negative impacts of globalisation.', ['protects strategic and infant industries', 'responds to unfair competition'], ['higher prices and retaliation (US-China)', 'inefficient industries; loss of export markets'], 'Targeted protection can help strategic sectors, but widespread protectionism usually harms economies.'),
            ('Political responses to migration are mainly driven by economic concerns.', ['job competition, wages, public services', 'deindustrialised regions voted Leave'], ['identity, culture and sovereignty concerns', 'security fears and media framing'], 'Economic and cultural concerns are intertwined; cultural identity is often as important as economics.')],
  extended=[('Explain the reasons for and effects of protectionist and border-control responses to globalisation.', 'Tariffs, quotas, subsidies, walls, visas; reasons (jobs, sovereignty, security, identity); examples (Brexit, US-China trade war, Hungary fence); effects on trade and migration.', 10, 'long')],
  res=[('Data: a country imports 2 million tonnes of steel a year at US$600 a tonne. It imposes a 25% tariff.',
        [('Calculate the tariff paid per tonne and the total tariff revenue if imports fall to 1.5 million tonnes.', f'25% × 600 = US$150 per tonne; 150 × 1,500,000 = US${150 * 1.5:.0f} million'),
         ('Explain one effect of the tariff on firms that use steel.', 'Higher input costs reduce competitiveness of car makers and construction firms, which may raise prices or cut jobs.')]),
       ('Table: Brexit referendum 2016 (% Leave) - England 53.4; Wales 52.5; Scotland 38.0; Northern Ireland 44.2; UK total 51.9.',
        [('Calculate the difference between the highest and lowest Leave vote.', f'53.4 − 38.0 = {53.4 - 38.0:.1f} percentage points'),
         ('Suggest reasons for the spatial pattern.', 'Scotland and Northern Ireland had stronger pro-EU identities, concerns about the border and devolved politics; parts of England and Wales with deindustrialised towns and older populations voted Leave.')])])

S('ch10-st3', gens=['pct_global', 'chi_global', 'spearman_global'],
  terms=[('transnational activism', 'campaigning by networks of people and organisations across national borders on shared issues'),
         ('social media activism', 'using platforms such as X, Instagram and TikTok to raise awareness, organise protests and pressure governments or companies'),
         ('hashtag activism', 'campaigns organised around a hashtag, e.g. #MeToo, #FridaysForFuture, #BringBackOurGirls'),
         ('slacktivism', 'low-effort online support (likes, shares) that may have little real-world impact'),
         ('internet censorship', 'state control or suppression of online information, e.g. China\'s "Great Firewall"')],
  facts=[('Fridays for Future, the school climate strike movement, was started by:', 'Greta Thunberg in Sweden in 2018', ['Malala Yousafzai in Pakistan in 2012', 'Al Gore in the USA in 2006', 'Wangari Maathai in Kenya in 1977'], 'Over 6 million people joined the global strikes in September 2019.'),
         ('The Arab Spring protests of 2010-2011 began in:', 'Tunisia', ['Egypt', 'Syria', 'Libya'], 'Social media helped spread protests across North Africa and the Middle East.'),
         ('The #MeToo hashtag went viral globally in:', '2017', ['2001', '2008', '2022'], 'It was originally used by activist Tarana Burke in 2006.'),
         ('China\'s internet censorship system is commonly known as:', 'the Great Firewall', ['the Iron Curtain', 'the Bamboo Curtain', 'the Digital Silk Road'], 'Sites such as Google, Facebook and YouTube are blocked.')],
  why=[('Explain how social media has increased transnational activism.', 'It allows instant, low-cost sharing of information and images across borders, connects people with shared concerns, enables rapid organisation of protests and bypasses traditional media.'),
       ('Explain why governments sometimes shut down the internet during protests.', 'To prevent organisation and the spread of images of protests or repression, control the narrative and limit international attention, e.g. Iran in 2019 and 2022, India in Kashmir.'),
       ('Explain why some critics describe online activism as slacktivism.', 'Liking or sharing posts requires little effort or risk and may give a feeling of participation without changing policies; attention may fade quickly.'),
       ('Explain how technology can strengthen local groups in global campaigns.', 'Indigenous and local groups can document abuses with smartphones, share them globally and gain support from NGOs and consumers, e.g. Indigenous protests against the Dakota Access Pipeline at Standing Rock (2016).')],
  contrast=[('online activism', 'offline activism', 'Online activism uses digital platforms to spread messages and mobilise support; offline activism involves physical action such as marches, strikes and occupations - many movements combine both.'),
            ('open internet societies', 'censored internet societies', 'In open societies citizens can freely access global platforms; in censored ones the state blocks sites and monitors users, limiting transnational activism.')],
  misc=[('Social media alone caused the Arab Spring.', 'Deep grievances (unemployment, corruption, food prices) caused the protests; social media helped spread and organise them.'),
        ('Online campaigns never lead to real change.', 'Some have changed policies and corporate behaviour, e.g. #MeToo led to legal changes and resignations in many countries.'),
        ('Technology always strengthens democracy.', 'Governments also use technology for surveillance, censorship and disinformation.')],
  apply=[('Using a named example, explain how technology helped a transnational movement grow.', 'e.g. Fridays for Future: Greta Thunberg\'s solo strike in 2018 spread via Instagram and X; by September 2019 about 6 million people in over 150 countries joined strikes; it influenced climate debate and youth involvement in COP meetings.', 4),
         ('Suggest one reason why internet shutdowns are becoming more frequent.', 'Governments recognise the power of social media to mobilise protest and can easily order state-influenced telecom providers to cut access.', 2)],
  cases=[('Fridays for Future', 'Greta Thunberg\'s 2018 school strike grew into global strikes involving about 6 million people in September 2019', 'transnational activism through social media', 'digital networks spread a local protest worldwide'),
         ('the Arab Spring', 'protests that began in Tunisia in December 2010 spread across the region, toppling leaders in Tunisia, Egypt, Libya and Yemen', 'the role of technology in political change', 'social media accelerated the spread of protest between countries'),
         ('#MeToo', 'the hashtag was used millions of times in 2017 and spread to over 85 countries', 'hashtag activism', 'online sharing of experiences created a global movement'),
         ('Iran\'s internet shutdowns', 'authorities restricted internet access during protests in 2019 and after the death of Mahsa Amini in 2022', 'state responses to digital activism', 'governments can limit transnational activism by controlling networks')],
  evaluate=[('Social media has made transnational activism more effective.', ['rapid mobilisation (Fridays for Future, #MeToo)', 'global visibility for local struggles'], ['slacktivism and short attention spans', 'censorship, surveillance and disinformation'], 'Social media makes activism faster and wider, but lasting change needs offline organisation.'),
            ('Technology gives more power to citizens than to governments.', ['citizens can bypass state media and organise', 'documenting abuses'], ['states control infrastructure and surveillance (China, Iran)', 'platforms controlled by TNCs'], 'Technology empowers both; outcomes depend on political systems and platform control.')],
  extended=[('Explain how technology and social media have changed the nature of activism and resistance.', 'Social media activism, hashtag campaigns, transnational networks; examples (Fridays for Future, Arab Spring, #MeToo, Standing Rock); censorship and shutdowns; slacktivism.', 10, 'long')],
  res=[('Graph description: number of countries with at least one government internet shutdown (Access Now) - 2016: 13; 2018: 25; 2020: 29; 2022: 35; 2023: 39.',
        [('Calculate the percentage increase from 2016 to 2023.', f'(39 − 13)/13 × 100 = {pc(13, 39)}'),
         ('Suggest why the trend matters for transnational activism.', 'More governments are cutting connections to stop protests spreading, limiting citizens\' ability to organise and share information internationally.')]),
       ('Survey of 120 students: 96 had shared a climate post online in the last year; 30 had attended a climate protest; 12 had contacted a politician.',
        [('Calculate the percentage of students who had attended a protest.', '30/120 × 100 = 25%'),
         ('Use the data to discuss the idea of slacktivism.', 'Online sharing (80%) is far more common than offline action (25%) or contacting politicians (10%), suggesting much online support does not translate into action.')])])


TARIFF_C = [('the USA', 'steel from abroad', 'tonne', 500, 900), ('the EU', 'battery electric cars from China', 'car', 18000, 32000),
            ('India', 'smartphones', 'phone', 120, 400), ('the USA', 'washing machines from Asia', 'machine', 250, 500),
            ('Indonesia', 'imported rice', 'tonne', 380, 650), ('Brazil', 'imported solar panels', 'panel', 90, 220)]


@gen('tariff', d=(1, 4))
def g_tariff(rng, slot):
    c, good, unit, lo, hi = rng.choice(TARIFF_C)
    p = rng.randrange(lo, hi, 10)
    t = rng.choice([10, 15, 20, 25, 30, 35])
    q0 = rng.randint(20, 90) * 10
    fall = rng.choice([10, 15, 20, 25, 30, 40])
    q1 = q0 * (100 - fall) / 100
    pt = p * (1 + t / 100)
    rev = p * t / 100 * q1 * 1000 / 1e6
    stem = (f'{c[0].upper() + c[1:]} imposes a {t}% tariff on {good}. The world price is US${p:,} per {unit}. Imports were {q0:,} thousand {unit}s a year and fall by {fall}% after the tariff. '
            f'Calculate the import price including the tariff and the annual tariff revenue (US$ million).')
    if slot.d >= 3:
        stem += ' Explain one disadvantage of the tariff for consumers or firms in the importing country.'
    return dict(stem=stem, answer=f'price = {p:,} × {1 + t / 100:.2f} = US${pt:,.0f} per {unit}; imports {q1:,.0f} thousand; revenue = {p:,} × {t / 100:.2f} × {q1 * 1000:,.0f} = US${rev:,.1f} million'
                + ('; disadvantage: higher prices for consumers and higher costs for firms using the good, and possible retaliation against exports.' if slot.d >= 3 else ''),
                markingKey=f'A1 price US${pt:,.0f}; M1 new import quantity {q1:,.0f} thousand; A1 revenue US${rev:,.1f} million.' + (' R1 disadvantage.' if slot.d >= 3 else ''),
                marks=mk(slot, 3 if slot.d <= 2 else 4))

# =============================================================================================
# HL extension: Global risks and resilience
# =============================================================================================
S('ch11-st1', gens=['pct_global', 'chi_global', 'tariff'],
  terms=[('geopolitical risk', 'the threat that political events, conflicts or tensions between states will disrupt global interactions'),
         ('terrorism', 'the use or threat of violence against civilians to achieve political, religious or ideological aims'),
         ('cyberterrorism', 'politically motivated attacks on computer systems and networks to cause disruption or fear, e.g. against power grids or hospitals'),
         ('sovereignty', 'the authority of a state to govern itself without outside interference'),
         ('ransomware', 'malicious software that encrypts a victim\'s data until a ransom is paid'),
         ('failed state', 'a state whose government has lost control of its territory and cannot provide basic services or security')],
  facts=[('The 2017 WannaCry ransomware attack severely disrupted which national health service?', 'the UK\'s NHS', ['Canada\'s health system', 'Japan\'s health system', 'Brazil\'s SUS'], 'It affected over 200,000 computers in about 150 countries.'),
         ('The 2021 Colonial Pipeline cyberattack in the USA shut down:', 'the largest fuel pipeline on the US East Coast', ['the New York Stock Exchange', 'the Panama Canal', 'Google search'], 'The company paid a ransom of about US$4.4 million.'),
         ('Houthi attacks on shipping from late 2023 forced many ships to avoid:', 'the Red Sea and Suez Canal', ['the Strait of Gibraltar', 'the English Channel', 'the Panama Canal'], 'Ships rerouted around the Cape of Good Hope, adding about 10-14 days.'),
         ('The 9/11 attacks in 2001 led to:', 'large increases in airport security and the US-led "war on terror"', ['the creation of the WTO', 'the end of NATO', 'the opening of China to trade'], 'Global aviation security changed permanently.')],
  why=[('Explain how conflict disrupts global interactions.', 'It destroys infrastructure, closes trade routes and airspace, deters investment and tourism, displaces people, and triggers sanctions, e.g. the war in Ukraine disrupted grain, energy and fertiliser exports.'),
       ('Explain why cyberterrorism is a growing geopolitical risk.', 'Economies and infrastructure (power, water, health, finance) depend on interconnected digital systems; attacks are cheap, can be launched remotely and anonymously, and can cascade across borders.'),
       ('Explain how globalisation can lead to a loss of sovereignty.', 'Membership of trade blocs and international organisations requires accepting shared rules; TNCs and global markets constrain national policy; cross-border data and digital platforms escape national control.'),
       ('Explain why terrorism affects tourism-dependent economies.', 'Attacks reduce visitor confidence; governments issue travel advisories; airlines cancel routes; and the effects can last years, e.g. Tunisia after the 2015 Sousse attack.')],
  contrast=[('terrorism', 'cyberterrorism', 'Terrorism uses physical violence against people and places; cyberterrorism attacks digital networks and infrastructure to cause disruption and fear, often remotely.'),
            ('state actors', 'non-state actors', 'State actors are governments and their agencies (militaries, intelligence services); non-state actors include terrorist groups, hackers, TNCs and NGOs.')],
  misc=[('Cyberattacks only affect computers, not people.', 'Attacks on hospitals, power grids and fuel supplies can endanger lives and halt economies.'),
        ('Globalisation always reduces conflict.', 'Interdependence can reduce war between trading partners, but competition for resources and influence can also create tensions.'),
        ('Loss of sovereignty is always negative.', 'Pooling sovereignty can bring benefits such as trade access, shared security and solutions to global problems.')],
  apply=[('Using a named example, explain how a geopolitical event disrupted global flows.', 'e.g. Russia\'s 2022 invasion of Ukraine: Ukraine and Russia supplied about 30% of world wheat exports; Black Sea ports blockaded; food and energy prices spiked; EU cut Russian gas imports; sanctions froze assets; airspace closures lengthened Europe-Asia flights.', 6),
         ('Suggest why small states may be particularly vulnerable to cyberattacks.', 'Limited cybersecurity budgets and expertise, highly concentrated digital infrastructure and dependence on foreign providers, e.g. the 2007 attacks on Estonia.', 2)],
  cases=[('the 2007 cyberattacks on Estonia', 'banks, media and government websites were disabled for weeks after a dispute with Russia over a Soviet war memorial', 'cyberterrorism and sovereignty', 'a highly digital state was vulnerable to cross-border attacks'),
         ('the Red Sea shipping crisis from 2023', 'Houthi attacks cut Suez Canal traffic by about half, with ships rerouting around Africa', 'geopolitical risk to trade routes', 'conflict at a chokepoint raised shipping costs and times'),
         ('the WannaCry ransomware attack (2017)', 'it affected over 200,000 computers in about 150 countries, cancelling about 19,000 NHS appointments', 'cyber risks to services', 'interconnected systems allowed malware to spread globally within hours'),
         ('the war in Ukraine', 'from 2022 Black Sea grain exports were disrupted and European gas prices rose to record levels', 'conflict and global interdependence', 'war in one region transmitted price shocks worldwide')],
  evaluate=[('Cyberterrorism is now a greater risk to global interactions than physical terrorism.', ['digital dependence of infrastructure', 'attacks are cheap and cross borders easily'], ['physical conflict still disrupts trade and kills people (Red Sea, Ukraine)', 'cyber defences are improving'], 'Cyber risks are growing fastest, but physical conflict remains the more severe disruption.'),
            ('Globalisation has reduced national sovereignty.', ['WTO and EU rules, IMF conditions', 'TNC and digital platform power'], ['states still control borders, taxation and laws (Brexit, tariffs)', 'powerful states shape global rules'], 'Sovereignty is pooled and constrained, but states remain the main actors.')],
  extended=[('Explain the geopolitical risks associated with global interactions.', 'Conflict, terrorism, cyberterrorism, loss of sovereignty; examples (Ukraine, Red Sea, WannaCry, Estonia); effects on trade, migration and services.', 10, 'long')],
  res=[('Data: a container ship sailing from Shanghai to Rotterdam via Suez travels about 19,500 km; via the Cape of Good Hope about 25,000 km. Average speed 30 km/h.',
        [('Calculate the extra distance and extra sailing time via the Cape (in days).', f'Extra 5,500 km; 5,500 / 30 = {5500 / 30:.0f} hours ≈ {5500 / 30 / 24:.1f} days'),
         ('Explain one effect of this rerouting on global supply chains.', 'Longer journeys raise freight and fuel costs and insurance, delay deliveries and reduce effective shipping capacity, raising prices for consumers.')]),
       ('Table: Suez Canal transits (ships per month, approximate) - November 2023: 2,050; January 2024: 1,120; March 2024: 1,000.',
        [('Calculate the percentage change from November 2023 to March 2024.', f'(1,000 − 2,050)/2,050 × 100 = {pc(2050, 1000)}'),
         ('Suggest one effect on Egypt.', 'Lost canal revenue (a key source of foreign exchange), worsening Egypt\'s debt and currency problems.')])])

S('ch11-st2', gens=['debt', 'pct_global', 'tariff'],
  terms=[('financial crisis', 'a sudden fall in asset values and failure of financial institutions, which spreads through credit markets to the wider economy'),
         ('contagion', 'the spread of economic shocks from one country or market to others through financial and trade links'),
         ('sovereign debt crisis', 'a situation where a government cannot repay or refinance its debts, e.g. Greece 2010 or Sri Lanka 2022'),
         ('supply-chain disruption', 'interruption of the flow of materials and goods between firms, caused by events such as pandemics, disasters or blockages'),
         ('chokepoint', 'a narrow passage on a major trade route, such as the Strait of Malacca, Suez Canal or Strait of Hormuz'),
         ('subprime mortgage', 'a loan to borrowers with poor credit histories, at the centre of the 2007-08 US housing crash')],
  facts=[('The global financial crisis of 2008 began with the collapse of:', 'the US subprime mortgage market', ['the Chinese stock market', 'the price of coffee', 'the euro'], 'Lehman Brothers filed for bankruptcy in September 2008.'),
         ('In March 2021 the container ship Ever Given blocked which waterway for six days?', 'the Suez Canal', ['the Panama Canal', 'the Strait of Malacca', 'the Bosphorus'], 'It held up about US$9.6 billion of trade a day.'),
         ('Which country defaulted on its foreign debt in 2022 after running out of foreign currency?', 'Sri Lanka', ['Norway', 'Switzerland', 'Singapore'], 'It had large debts to China, India and bondholders.'),
         ('A global shortage of semiconductors in 2021 especially hit:', 'car manufacturing', ['coffee production', 'tourism', 'fishing'], 'Global car production fell by about 10 million vehicles.')],
  why=[('Explain why financial crises spread rapidly between countries.', 'Banks and investors are interconnected through global capital markets; losses in one country reduce lending elsewhere; trade falls as demand drops; and investor panic causes capital flight from vulnerable economies.'),
       ('Explain why just-in-time supply chains are vulnerable to disruption.', 'Low stock levels and dependence on single suppliers or routes mean any delay (pandemic lockdowns, blockages, disasters) quickly halts production, as with the semiconductor shortage of 2021.'),
       ('Explain why high debt can be a risk for low- and middle-income countries.', 'Debt service absorbs export earnings and government revenue; rising interest rates and currency falls increase repayments; default cuts access to credit and imports of food and fuel, as in Sri Lanka 2022.'),
       ('Explain why chokepoints create risks for global trade.', 'A large share of trade passes through a few narrow routes; blockages, conflict or drought (Panama Canal 2023) can delay a significant share of world shipping.')],
  contrast=[('a financial crisis', 'a supply-chain disruption', 'A financial crisis starts with failures of banks, credit or asset prices and spreads through money flows; a supply-chain disruption interrupts the physical flow of goods.'),
            ('just-in-time', 'just-in-case', 'Just-in-time keeps minimal stock for efficiency; just-in-case holds larger buffer stocks and diversified suppliers for resilience.')],
  misc=[('Financial crises only affect rich countries.', 'Contagion reduces trade, remittances and investment in poorer countries too.'),
        ('Supply-chain disruptions are rare one-off events.', 'Recent years saw repeated disruptions: COVID-19, Ever Given, semiconductor shortages, Red Sea attacks and Panama Canal drought.'),
        ('Debt is always harmful for development.', 'Borrowing can fund productive infrastructure; problems arise when debt is unsustainable or spent unproductively.')],
  apply=[('Using a named example, explain how a financial crisis spread globally.', 'e.g. 2008: US subprime mortgages were packaged into securities sold worldwide; Lehman Brothers collapsed; credit froze; Iceland\'s banks failed; world trade fell by about 12% in 2009; remittances and FDI to developing countries fell.', 6),
         ('Suggest why the Ever Given blockage had effects far beyond Egypt.', 'About 12% of world trade passes through Suez; hundreds of ships were delayed, disrupting just-in-time supply chains in Europe and Asia and raising freight rates.', 2)],
  cases=[('the 2008 global financial crisis', 'the collapse of Lehman Brothers led to a global recession, and world trade fell about 12% in 2009', 'financial contagion', 'interconnected banks transmitted a US housing crisis worldwide'),
         ('the Ever Given blockage of the Suez Canal (2021)', 'a 400 m container ship blocked the canal for six days, holding up over 400 vessels', 'chokepoint vulnerability', 'a single blockage disrupted a major artery of world trade'),
         ('Sri Lanka\'s 2022 debt crisis', 'Sri Lanka defaulted after foreign reserves ran out, causing fuel and medicine shortages and mass protests', 'sovereign debt risk', 'high debt and falling foreign currency earnings left the economy unable to pay for imports'),
         ('the 2021 semiconductor shortage', 'chip shortages cut global car production by about 10 million vehicles', 'supply-chain disruption', 'concentration of chip production in Taiwan and South Korea created vulnerability')],
  evaluate=[('Economic interdependence increases risk more than it increases prosperity.', ['contagion (2008), supply shocks (COVID, Ever Given)', 'debt crises'], ['trade and investment lifted billions from poverty', 'interdependence allows recovery support and diversification'], 'Interdependence increases exposure to shocks, but its benefits generally outweigh the risks if resilience is built in.'),
            ('Supply-chain disruptions are the greatest economic risk of globalisation.', ['frequent and costly (COVID, chips, Red Sea)', 'affect consumers worldwide'], ['financial crises cause deeper and longer recessions', 'debt crises harm the poorest countries most'], 'Supply chains are a major and growing risk, but financial crises remain the most damaging.')],
  extended=[('Explain how economic risks are transmitted through global interactions.', 'Financial contagion (2008), sovereign debt (Greece, Sri Lanka), supply chains (Ever Given, semiconductors, COVID); chokepoints; effects on different countries.', 10, 'long')],
  res=[('Data: an estimated US$9.6 billion of trade passed through the Suez Canal each day in 2021. The Ever Given blocked it for 6 days.',
        [('Calculate the value of trade held up.', f'9.6 × 6 = US${9.6 * 6:.1f} billion'),
         ('Suggest why the long-term effects were greater than the six-day closure suggests.', 'The backlog took about a week more to clear, ships and containers were out of position for weeks, and ports faced congestion, raising freight rates.')]),
       ('Table: world merchandise trade volume index (2007 = 100) - 2008: 102; 2009: 90; 2010: 103; 2011: 109.',
        [('Calculate the percentage change in trade between 2008 and 2009.', f'(90 − 102)/102 × 100 = {pc(102, 90)}'),
         ('Describe the pattern shown.', 'A sharp fall in 2009 after the financial crisis, followed by recovery above the 2008 level by 2010-11.')])])

S('ch11-st3', gens=['tariff', 'pct_global', 'kof'],
  terms=[('economic diversification', 'reducing dependence on a narrow range of products, markets or suppliers'),
         ('reshoring', 'returning production previously offshored back to the home country'),
         ('nearshoring', 'relocating production to countries close to the main market, e.g. US firms moving production to Mexico'),
         ('friend-shoring', 'relocating supply chains to politically allied countries to reduce geopolitical risk'),
         ('China plus one', 'a strategy of keeping production in China while adding another location such as Vietnam or India'),
         ('international cooperation', 'states working together through agreements and institutions to manage shared risks')],
  facts=[('The US CHIPS and Science Act (2022) aims to:', 'boost domestic semiconductor manufacturing', ['ban all imports from Europe', 'privatise NASA', 'increase tariffs on coffee'], 'It provides about US$52.7 billion for chip manufacturing and research.'),
         ('Which country overtook China as the largest source of US imports in 2023?', 'Mexico', ['Germany', 'Canada', 'Vietnam'], 'Nearshoring and tariffs on China contributed.'),
         ('Apple\'s move to assemble more iPhones in India is an example of:', 'the China plus one strategy', ['reshoring to the USA', 'import substitution', 'nationalisation'], 'India made about 14% of iPhones in 2023-24.'),
         ('The COVAX facility was an international cooperation scheme to share:', 'COVID-19 vaccines', ['oil reserves', 'military equipment', 'internet bandwidth'], 'It delivered about 2 billion doses to 146 countries.')],
  why=[('Explain why many firms are diversifying their supply chains.', 'COVID-19 lockdowns, the semiconductor shortage, US-China tensions and tariffs, and conflict showed the risks of dependence on one country or route; diversification spreads risk.'),
       ('Explain why reshoring is difficult for many industries.', 'Higher labour costs at home, loss of skills and supplier networks, the scale of Asian clusters, and the time and capital needed to build factories.'),
       ('Explain how international cooperation can increase resilience to global risks.', 'Shared rules, information, funds and resources help states respond to crises that cross borders - e.g. G20 financial co-ordination in 2009, IMF lending, vaccine sharing, Interpol and cybersecurity agreements.'),
       ('Explain why economic diversification is important for oil-exporting countries.', 'Oil prices are volatile and demand will fall with decarbonisation; diversification into tourism, logistics, finance and manufacturing reduces vulnerability, e.g. Saudi Vision 2030 and Dubai.')],
  contrast=[('reshoring', 'nearshoring', 'Reshoring brings production back to the home country; nearshoring moves it to a nearby country with lower costs, such as Mexico for the USA or Poland and Türkiye for Western Europe.'),
            ('national resilience strategies', 'international cooperation', 'National strategies reduce dependence through domestic production, stockpiles and subsidies; international cooperation reduces risk through shared rules, agreements and assistance.')],
  misc=[('Reshoring will bring back most manufacturing jobs to high-income countries.', 'New factories are often highly automated, so they create far fewer jobs than were lost.'),
        ('Diversification means abandoning China.', 'Most firms follow "China plus one", keeping Chinese operations while adding other locations.'),
        ('International cooperation is always effective.', 'Unequal power and national interests limit cooperation, e.g. vaccine nationalism during COVID-19.')],
  apply=[('Using named examples, explain how countries and firms are building resilience to supply-chain risks.', 'e.g. US CHIPS Act subsidies for TSMC and Intel fabs in Arizona and Ohio; EU Chips Act; Apple and Samsung moving assembly to India and Vietnam; firms holding larger inventories and dual-sourcing; nearshoring to Mexico.', 6),
         ('Suggest why Dubai is often cited as an example of diversification.', 'Oil is now only a few per cent of Dubai\'s GDP; it has developed aviation (Emirates), ports (Jebel Ali), tourism, finance and real estate.', 2)],
  cases=[('TSMC\'s factories in Arizona', 'supported by the CHIPS Act, TSMC committed over US$65 billion (later raised further) to chip fabs near Phoenix', 'reshoring strategic industries', 'governments subsidise domestic production of critical goods'),
         ('nearshoring to Mexico', 'Mexico became the USA\'s largest source of imports in 2023 as firms moved production from Asia', 'nearshoring', 'proximity and trade agreements make Mexico attractive for resilient supply chains'),
         ('Saudi Arabia\'s Vision 2030', 'a plan to diversify away from oil through tourism, entertainment, mining and new cities such as NEOM', 'economic diversification', 'reducing dependence on one commodity builds long-term resilience'),
         ('COVAX', 'it delivered about 2 billion vaccine doses to 146 countries, though deliveries were slower than planned', 'international cooperation', 'collective action helped but was limited by vaccine nationalism')],
  evaluate=[('Reshoring is the most effective way to reduce supply-chain risk.', ['secures strategic goods (chips)', 'reduces geopolitical exposure'], ['expensive, slow, raises prices', 'diversification and nearshoring are cheaper; domestic disasters still occur'], 'Reshoring suits strategic sectors; diversification is more effective for most goods.'),
            ('International cooperation is essential for resilience to global risks.', ['risks cross borders (pandemics, finance, cyber)', 'G20 2009, IMF'], ['national strategies and stockpiles also needed', 'cooperation weakened by rivalry'], 'Cooperation is essential for global risks, but must be combined with national resilience.')],
  extended=[('Explain the strategies that can be used to build resilience to geopolitical and economic risks.', 'Diversification, reshoring, nearshoring, friend-shoring, stockpiles, international cooperation (G20, IMF, COVAX); examples (CHIPS Act, Mexico, Vision 2030, Apple in India).', 10, 'long')],
  res=[('Table: share of US goods imports (%) - China: 2017 21.6, 2023 13.9; Mexico: 2017 13.4, 2023 15.4; Vietnam: 2017 2.0, 2023 3.6.',
        [('Calculate the percentage change in China\'s share between 2017 and 2023.', f'(13.9 − 21.6)/21.6 × 100 = {pc(21.6, 13.9)}'),
         ('Suggest reasons for the changes shown.', 'US tariffs on Chinese goods from 2018, firms diversifying supply chains after COVID-19 (China plus one), and nearshoring to Mexico under USMCA.')]),
       ('Table: oil and gas share of GDP (%) - Saudi Arabia 2012: 50, 2022: 40; UAE 2012: 38, 2022: 30.',
        [('Calculate the change in percentage points for each country.', 'Saudi Arabia −10; UAE −8'),
         ('Suggest one limitation of using these figures to measure diversification.', 'Shares change with oil prices, so a falling share may reflect lower oil prices rather than growth of other sectors.')])])

S('ch12-st1', gens=['carbon', 'pct_climate', 'sea_level'],
  terms=[('transboundary pollution', 'pollution that originates in one country and causes harm in another, e.g. acid rain, haze or river pollution'),
         ('climate tipping point', 'a critical threshold beyond which a part of the climate system changes abruptly and often irreversibly, e.g. collapse of an ice sheet'),
         ('haze', 'smoke from forest and peat fires that spreads across borders, as in South-East Asia'),
         ('positive feedback', 'a process that amplifies change, e.g. melting sea ice reducing albedo and increasing warming'),
         ('Great Pacific Garbage Patch', 'an area of concentrated plastic debris in the North Pacific gyre'),
         ('e-waste', 'discarded electronic equipment, often exported to lower-income countries for processing')],
  facts=[('The 2015 South-East Asian haze was caused mainly by:', 'peat and forest fires in Indonesia', ['volcanic eruptions in the Philippines', 'factory emissions in Japan', 'dust storms from the Sahara'], 'It affected Singapore and Malaysia; estimates suggest about 100,000 premature deaths.'),
         ('Which is identified as a climate tipping element?', 'The West Antarctic Ice Sheet', ['The Sahara Desert\'s size', 'The Great Barrier Reef\'s tourism', 'The Himalayas\' height'], 'Others include the Amazon rainforest, AMOC and permafrost.'),
         ('The 1986 Chernobyl disaster spread radioactive fallout across:', 'much of Europe, including Scandinavia and the UK', ['only Ukraine', 'only Russia', 'South America'], 'Sheep movement restrictions in Wales lasted until 2012.'),
         ('Agbogbloshie in Accra, Ghana, was known as:', 'one of the world\'s largest e-waste sites', ['a major oil refinery', 'a nuclear plant', 'a coral reef'], 'It was demolished in 2021.')],
  why=[('Explain why transboundary pollution is difficult to manage.', 'Sources and impacts are in different countries; polluting states may lack incentive or capacity to act; sovereignty limits enforcement; scientific attribution is contested; agreements need cooperation.'),
       ('Explain how climate tipping points could cause abrupt change.', 'Beyond a threshold, positive feedbacks become self-sustaining - e.g. permafrost thaw releases methane, Amazon dieback reduces rainfall recycling, ice-sheet loss lowers albedo - so change continues even if emissions stop.'),
       ('Explain how global trade can increase environmental risks.', 'Demand for commodities drives deforestation (palm oil, soy, beef); shipping spreads invasive species and pollution; waste and e-waste are exported; production moves to places with weak regulation.'),
       ('Explain why the Amazon rainforest is considered at risk of a tipping point.', 'Deforestation (about 17% of the forest lost) and warming reduce evapotranspiration and rainfall; beyond about 20-25% loss parts may shift to savanna, releasing carbon and reducing rainfall regionally.')],
  contrast=[('local pollution', 'transboundary pollution', 'Local pollution affects the area where it is produced; transboundary pollution crosses national borders, so management requires international cooperation.'),
            ('gradual climate change', 'abrupt change at tipping points', 'Gradual change increases roughly in proportion to warming; abrupt change occurs suddenly once a threshold is crossed and may be irreversible.')],
  misc=[('Tipping points will only occur far in the future.', 'Research suggests some, such as warm-water coral reef die-off and Greenland ice loss, may be triggered between 1.5 and 2 °C of warming.'),
        ('Pollution stops at national borders.', 'Air, rivers and oceans carry pollution across borders and around the world.'),
        ('Exporting waste solves the problem for rich countries.', 'It shifts environmental and health risks to poorer countries and plastics return through oceans and food chains.')],
  apply=[('Using a named example, explain how transboundary pollution affected people in another country.', 'e.g. the 2015 Indonesian haze: fires on peatland cleared for palm oil and pulp plantations; smoke closed schools and airports in Singapore and Malaysia; PSI readings above 300 (hazardous); about 100,000 premature deaths estimated; Indonesia had ratified the ASEAN Agreement on Transboundary Haze Pollution only in 2014, and enforcement remained weak.', 4),
         ('Suggest why permafrost thaw is described as a positive feedback.', 'Thaw releases CO₂ and methane from decomposing organic matter, adding greenhouse gases that cause further warming and more thaw.', 2)],
  cases=[('the 2015 South-East Asian haze', 'fires in Indonesia sent smoke across Singapore, Malaysia and Thailand, closing schools and harming health', 'transboundary air pollution', 'land clearance in one country created health risks across a region'),
         ('Agbogbloshie e-waste site, Ghana', 'imported electronics were burned to recover copper, exposing workers to lead and dioxins', 'environmental risks of global trade', 'waste flows from rich to poorer countries shift risks to vulnerable people'),
         ('the Chernobyl disaster (1986)', 'fallout spread across Europe and restrictions on sheep in parts of the UK lasted until 2012', 'transboundary pollution', 'an accident in one country contaminated others for decades'),
         ('the Amazon rainforest', 'about 17% has been deforested, and scientists warn that 20-25% loss could trigger dieback', 'climate tipping points', 'land-use change driven by global demand could cause irreversible change')],
  evaluate=[('Global interactions are the main cause of environmental risks.', ['commodity demand drives deforestation; trade spreads pollution', 'consumption in rich countries drives emissions'], ['domestic energy and land use are major causes', 'natural processes (volcanoes, fires) also matter'], 'Global interactions amplify many environmental risks, but local and national decisions are also central.'),
            ('Climate tipping points are the greatest environmental risk facing the world.', ['irreversible, abrupt and global effects', 'positive feedbacks'], ['air pollution kills about 7 million people a year now', 'biodiversity loss and water scarcity also severe'], 'Tipping points may be the most catastrophic risk long term, but current pollution causes greater immediate harm.')],
  extended=[('Explain how global interactions create environmental risks at different scales.', 'Transboundary pollution (haze, Chernobyl, acid rain), waste trade (e-waste), deforestation for commodities, climate change and tipping points (Amazon, ice sheets, permafrost).', 10, 'long')],
  res=[('Table: PSI (Pollutant Standards Index) readings in Singapore during a haze episode - day 1: 85; day 2: 160; day 3: 245; day 4: 341; day 5: 210. PSI above 300 is "hazardous".',
        [('Calculate the mean PSI over the five days.', f'(85 + 160 + 245 + 341 + 210)/5 = {(85 + 160 + 245 + 341 + 210) / 5:.1f}'),
         ('Suggest two responses by the Singapore government.', 'Health advisories and free masks; school closures; diplomatic pressure on Indonesia; the Transboundary Haze Pollution Act (2014) to prosecute companies responsible.')]),
       ('Data: Amazon deforestation in Brazil (km²/year, PRODES) - 2004: 27,772; 2012: 4,571; 2021: 13,038; 2023: 9,001.',
        [('Calculate the percentage change from 2021 to 2023.', f'(9,001 − 13,038)/13,038 × 100 = {pc(13038, 9001)}'),
         ('Suggest reasons for changes in deforestation rates.', 'Stronger enforcement and monitoring (2004-2012 and from 2023 under Lula), weaker enforcement under Bolsonaro (2019-2022), commodity prices for soy and beef.')])])

S('ch12-st2', gens=['carbon_tax', 'pct_climate', 'carbon'],
  terms=[('international environmental agreement', 'a treaty between states to manage a shared environmental problem, e.g. the Montreal Protocol or Paris Agreement'),
         ('Montreal Protocol', 'the 1987 agreement to phase out ozone-depleting substances such as CFCs, ratified by every UN member state'),
         ('Paris Agreement', 'the 2015 UNFCCC agreement to limit warming to well below 2 °C, aiming for 1.5 °C, through nationally determined contributions'),
         ('nationally determined contribution (NDC)', 'each country\'s own pledge of emissions cuts and adaptation actions under the Paris Agreement'),
         ('civil society', 'non-governmental organisations, community groups, faith groups and citizens acting collectively outside government and business'),
         ('Global Plastics Treaty', 'a legally binding UN agreement on plastic pollution under negotiation since 2022')],
  facts=[('The Montreal Protocol is often described as the most successful environmental agreement because:', 'ozone-depleting substances fell by about 99% and the ozone layer is recovering', ['it stopped all global warming', 'it banned all plastics', 'it ended deforestation'], 'Recovery to 1980 levels is expected by about 2066 over Antarctica.'),
         ('Under the Paris Agreement, emissions targets are:', 'set by each country as nationally determined contributions', ['set by the UN for each country and legally enforced with fines', 'the same for every country', 'only required of developing countries'], 'They are reviewed in five-year cycles (the ratchet mechanism).'),
         ('The Kigali Amendment (2016) to the Montreal Protocol phases down:', 'HFCs, powerful greenhouse gases used in refrigeration', ['carbon dioxide from power stations', 'plastic bags', 'nuclear waste'], 'It could avoid up to about 0.4 °C of warming by 2100.'),
         ('Wangari Maathai\'s Green Belt Movement in Kenya is known for:', 'planting over 50 million trees with women\'s groups', ['building dams', 'oil exploration', 'nuclear power'], 'Maathai won the 2004 Nobel Peace Prize.')],
  why=[('Explain why the Montreal Protocol was more successful than climate agreements.', 'Few industries produced CFCs, substitutes were available, the threat (ozone hole) was clear and immediate, costs were low, and a fund helped developing countries; CO₂ comes from the whole energy system and is far harder to replace.'),
       ('Explain why the Paris Agreement has been criticised.', 'Pledges are voluntary and, even if met, imply about 2.5-2.9 °C of warming; there is no enforcement; climate finance promises have been missed; major emitters can withdraw (the USA in 2017 and again in 2025).'),
       ('Explain how civil society contributes to environmental resilience.', 'NGOs and community groups monitor pollution, plant forests, campaign for policy change, take legal action (e.g. climate litigation such as Urgenda v. Netherlands), and build local adaptation.'),
       ('Explain why local action is important for global environmental problems.', 'Global problems are caused by many local activities; local governments and communities control land use, transport and energy decisions, and act faster than international negotiations (e.g. C40 cities).')],
  contrast=[('the Montreal Protocol', 'the Paris Agreement', 'The Montreal Protocol has binding phase-out schedules for a few specific chemicals and near-universal compliance; the Paris Agreement relies on voluntary national pledges covering all greenhouse gases from the whole economy.'),
            ('top-down global agreements', 'bottom-up local actions', 'Top-down agreements set international rules and targets between states; bottom-up actions are led by communities, cities and NGOs and are adapted to local conditions.')],
  misc=[('The ozone hole and climate change are the same problem.', 'Ozone depletion is caused by CFCs destroying stratospheric ozone; climate change is caused by greenhouse gases trapping heat - though some CFCs and HFCs are also greenhouse gases.'),
        ('The Paris Agreement legally requires countries to meet their targets.', 'Countries must submit and report on NDCs, but meeting them is not legally enforced.'),
        ('Only governments can solve global environmental problems.', 'Civil society, businesses, cities and individuals also drive change through campaigns, investment and behaviour.')],
  apply=[('Using a named example, explain how civil society has increased resilience to environmental risk.', 'e.g. Urgenda Foundation v. Netherlands: the Dutch Supreme Court ruled in 2019 that the state must cut emissions by at least 25% from 1990 levels by 2020; led to coal plant closures; inspired climate litigation worldwide.', 4),
         ('Suggest why city networks such as C40 matter for climate resilience.', 'Cities produce about 70% of energy-related CO₂; mayors control transport, buildings and planning; networks share best practice (e.g. Copenhagen cycling, Bogotá TransMilenio).', 2)],
  cases=[('the Montreal Protocol (1987)', 'production of ozone-depleting substances fell by about 99%, and the ozone layer is expected to recover by mid-century', 'successful international agreements', 'clear science, available substitutes and finance enabled universal cooperation'),
         ('Urgenda v. the Netherlands', 'the Supreme Court ordered the government in 2019 to cut emissions by 25% from 1990 levels by 2020', 'civil society and climate resilience', 'legal action by citizens forced stronger government action'),
         ('the Green Belt Movement, Kenya', 'women\'s groups have planted over 50 million trees since 1977', 'community-based environmental action', 'local action restored land and empowered women'),
         ('the Paris Agreement (2015)', 'nearly every country submitted emissions pledges, but current policies imply about 2.5-2.9 °C of warming', 'limits of global agreements', 'voluntary pledges have not yet been sufficient to meet the 1.5 °C goal')],
  evaluate=[('International agreements are more effective than local action in building resilience to environmental risks.', ['Montreal Protocol success', 'global problems need global rules'], ['Paris pledges insufficient', 'local and civil society action faster and adapted (Urgenda, Green Belt)'], 'Agreements set frameworks, but implementation depends on national and local action.'),
            ('The Paris Agreement will prevent dangerous climate change.', ['universal participation and ratchet mechanism', 'rapid growth of renewables'], ['current pledges imply about 2.5-2.9 °C', 'no enforcement; withdrawals'], 'It is unlikely to prevent dangerous change on current pledges without much stronger action.')],
  extended=[('Explain how local and global actions can increase resilience to environmental risks.', 'International agreements (Montreal, Paris, Kigali, Plastics Treaty); civil society (Urgenda, Green Belt Movement); cities (C40); strengths and limitations.', 10, 'long')],
  res=[('Table: global consumption of ozone-depleting substances (thousand ODP tonnes, approximate) - 1986: 1,800; 1995: 500; 2005: 90; 2020: 20.',
        [('Calculate the percentage fall from 1986 to 2020.', f'(20 − 1,800)/1,800 × 100 = {pc(1800, 20)}'),
         ('Explain why the ozone layer is recovering only slowly.', 'CFCs persist in the atmosphere for 50-100 years, so concentrations fall slowly even after production stops.')]),
       ('Table: projected warming by 2100 (°C, Climate Action Tracker style estimates) - current policies 2.7; NDC pledges 2.5; net-zero pledges fully met 1.9; Paris goal 1.5.',
        [('Calculate the gap between current policies and the Paris 1.5 °C goal.', '2.7 − 1.5 = 1.2 °C'),
         ('Suggest what the data show about the effectiveness of the Paris Agreement.', 'Pledges and policies have lowered expected warming, but they are not yet enough to meet the 1.5 °C goal.')])])

S('ch12-st3', gens=['pct_climate', 'risk', 'sea_level'],
  terms=[('systems thinking', 'analysing how parts of a system (physical and human) interact, including feedbacks, so that change in one part affects others'),
         ('cascading risk', 'a risk in which one event triggers a chain of further impacts across systems, e.g. an earthquake causing a nuclear accident and supply-chain disruption'),
         ('compound hazard', 'two or more hazards occurring together or in sequence, increasing impacts, e.g. a cyclone during a pandemic'),
         ('polycrisis', 'a situation where several global crises (climate, conflict, debt, pandemics) interact so that their combined effects are greater than the sum of their parts'),
         ('future risk', 'the likely changes in hazards, exposure and vulnerability over coming decades due to population, urbanisation, climate and global interactions')],
  facts=[('The 2011 Tōhoku earthquake disrupted global car and electronics production mainly because:', 'Japanese suppliers of specialist components were shut down', ['all world shipping stopped', 'the yen was abolished', 'Japan banned exports'], 'Toyota production fell sharply worldwide.'),
         ('The 2011 Thailand floods severely disrupted the global supply of:', 'hard disk drives', ['coffee', 'crude oil', 'wheat'], 'About a quarter of global hard drive output was affected.'),
         ('Which event is an example of a cascading risk?', 'Tōhoku earthquake → tsunami → Fukushima nuclear accident → energy policy change', ['A single rockfall on an empty slope', 'A light rain shower', 'A small earthquake felt by few people'], 'Impacts cascaded from physical to technological to political systems.'),
         ('The UN estimates the world\'s urban population will reach about what share by 2050?', 'About 68%', ['About 20%', 'About 45%', 'About 95%'], 'Much of the growth will be in Asia and Africa, often in hazard-prone coastal cities.')],
  why=[('Explain how geophysical hazards can create risks for global interactions.', 'They damage key nodes (ports, factories, airports) and transport links; global supply chains spread disruption; eruptions close airspace (Eyjafjallajökull 2010); financial and insurance losses spread through markets.'),
       ('Explain why future hazard risk is likely to increase.', 'Population growth and urbanisation in hazard zones (megacities on faults and coasts), rising asset values, climate change increasing secondary hazards (landslides, sea-level rise), and growing interdependence that spreads impacts.'),
       ('Explain why global interactions can also increase resilience to hazards.', 'They provide access to aid, expertise, insurance and reinsurance markets, technology such as early warning and satellites, and alternative suppliers, allowing faster recovery.'),
       ('Explain why compound hazards are a growing concern.', 'Hazards increasingly overlap in time and space - e.g. earthquakes during pandemics or conflicts (Türkiye-Syria 2023) - straining response capacity and multiplying vulnerability.')],
  contrast=[('a single hazard event', 'a cascading risk', 'A single hazard has direct local impacts; a cascading risk spreads through linked physical, technological, economic and political systems far beyond the original event.'),
            ('vulnerability of global networks', 'resilience of global networks', 'Vulnerability arises from concentration and just-in-time links that spread shocks; resilience comes from diversification, redundancy and cooperation that absorb and recover from shocks.')],
  misc=[('Geophysical hazards only have local impacts.', 'Through global networks, local events can disrupt worldwide supply chains, air travel and financial markets.'),
        ('Globalisation always increases hazard risk.', 'It can also provide aid, technology, insurance and alternative supplies that increase resilience.'),
        ('Future risk depends only on the frequency of hazards.', 'Exposure and vulnerability, shaped by urbanisation, wealth and governance, are usually more important.')],
  apply=[('Using named examples, explain how a geophysical hazard affected global interactions.', 'e.g. Eyjafjallajökull 2010: ash closed European airspace for six days; about 100,000 flights cancelled; Kenyan flower and vegetable exports to Europe were stranded, costing growers about US$1.3 million a day; global airlines lost about US$1.7 billion.', 4),
         ('Suggest how a major earthquake in Taiwan could affect the global economy.', 'Taiwan (TSMC) produces most of the world\'s advanced semiconductors; damage to fabs would disrupt electronics, car and AI industries worldwide.', 2)],
  cases=[('the 2010 Eyjafjallajökull eruption', 'ash closed much of European airspace for six days, cancelling about 100,000 flights and stranding Kenyan flower exports', 'hazards and global networks', 'a moderate eruption disrupted global transport and trade'),
         ('the 2011 Tōhoku disaster', 'damage to Japanese component suppliers disrupted car and electronics production worldwide, and Germany chose to phase out nuclear power', 'cascading risk', 'impacts spread from physical to economic and political systems globally'),
         ('the 2011 Thailand floods', 'floods in industrial estates near Bangkok cut global hard drive production by about a quarter', 'supply-chain concentration and risk', 'clustering of production in a hazard zone created global vulnerability'),
         ('the 2023 Türkiye-Syria earthquakes', 'the earthquakes struck a region already hosting millions of Syrian refugees and affected by conflict', 'compound risk', 'hazards interacting with conflict and displacement multiplied impacts')],
  evaluate=[('Global interactions increase vulnerability to hazards more than they increase resilience.', ['supply chains spread shocks (Tōhoku, Thailand)', 'air travel disruption (Eyjafjallajökull)'], ['aid, insurance and expertise flow to affected places', 'alternative suppliers and global markets aid recovery'], 'Interactions both spread and absorb shocks; the balance depends on diversification and cooperation.'),
            ('Future geophysical hazard risk will be determined more by human factors than by physical processes.', ['urbanisation and exposure growing fast', 'governance and building quality'], ['major events (Cascadia, Tokyo, Istanbul) are inevitable', 'climate change increases secondary hazards'], 'Physical processes are constant, so changing human exposure and vulnerability will largely determine future risk.')],
  extended=[('Explain the interconnections between geophysical hazards, global interactions and future risk.', 'Cascading and compound risks; supply chains (Tōhoku, Thailand, Taiwan chips); aviation (Eyjafjallajökull); aid and insurance; urbanisation and exposure; future risk scenarios.', 10, 'long')],
  res=[('Data: during the 2010 Eyjafjallajökull ash closure, Kenya\'s horticulture sector lost about US$1.3 million per day for 6 days, and airlines lost about US$200 million per day for 6 days.',
        [('Calculate the total losses for Kenyan horticulture and for airlines.', f'Kenya: 1.3 × 6 = US${1.3 * 6:.1f} million; airlines: 200 × 6 = US${200 * 6:,} million (US$1.2 billion)'),
         ('Explain why an eruption in Iceland affected farmers in Kenya.', 'Kenyan flowers and vegetables are air-freighted to Europe in just-in-time supply chains; closed airspace stranded perishable goods.')]),
       ('Table: projected population of selected megacities in hazard zones (million) - Manila 2020: 13.9, 2035: 18.6; Jakarta 2020: 10.8, 2035: 12.7; Istanbul 2020: 15.2, 2035: 17.1; Tokyo 2020: 37.4, 2035: 36.0.',
        [('Calculate the percentage change in Manila\'s population from 2020 to 2035.', f'(18.6 − 13.9)/13.9 × 100 = {pc(13.9, 18.6)}'),
         ('Suggest what the data suggest about future hazard risk.', 'Rapid growth in Manila, Jakarta and Istanbul will increase exposure to earthquakes, volcanic and coastal hazards unless building quality and planning improve; Tokyo\'s risk is stable or falling in terms of exposure.')])])

# =============================================================================================
# Internal assessment and Paper 3 skills
# =============================================================================================
S('ch13-st1', gens=['spearman', 'chi', 'stats', 'nni'],
  terms=[('written analysis (criterion D)', 'the IA criterion (9 marks) rewarding analysis of results linked to the fieldwork question, using evidence, geographic theory and anomalies'),
         ('anomaly', 'a result that does not fit the general pattern or trend, which should be identified and explained'),
         ('statistical significance', 'the probability that a result could have occurred by chance; geographers usually accept results at the 0.05 (95%) level'),
         ('null hypothesis', 'a statement that there is no relationship or difference, which statistical tests try to reject'),
         ('correlation', 'a statistical relationship between two variables, positive or negative, which does not prove causation'),
         ('triangulation', 'using different methods or data sources to check that results are consistent')],
  facts=[('Under the IB DP Geography IA assessment criteria, how many marks are available for criterion D (written analysis)?', '9', ['3', '6', '12'], 'The IA is marked out of 30 in total.'),
         ('A Spearman\'s rank value of −0.92 with 10 pairs (critical value 0.564 at 0.05) indicates:', 'a strong, significant negative correlation', ['a weak positive correlation', 'no correlation', 'a significant positive correlation'], 'The absolute value exceeds the critical value.'),
         ('A nearest-neighbour index of about 1.0 indicates a:', 'random distribution', ['clustered distribution', 'perfectly regular distribution', 'linear distribution'], 'Rn ranges from 0 (clustered) to 2.15 (regular).'),
         ('Which statistical test is most suitable for testing whether observed frequencies differ from expected frequencies across categories?', 'Chi-squared test', ['Spearman\'s rank correlation', 'Mean and range', 'Nearest-neighbour index'], 'It compares observed and expected counts.')],
  why=[('Explain why IA analysis should refer back to the fieldwork question.', 'Criterion D rewards analysis that directly addresses the question; linking each result to the question and hypothesis keeps the analysis focused and allows a supported conclusion.'),
       ('Explain why a strong correlation does not prove causation.', 'Both variables may be influenced by a third factor, the relationship may be coincidental, or causation may run in the opposite direction; geographical explanation and other evidence are needed.'),
       ('Explain why anomalies should be discussed in an IA analysis.', 'They may reveal measurement errors, local factors not included in the hypothesis, or limitations of the method; explaining them shows critical understanding and supports evaluation.'),
       ('Explain why statistical significance testing strengthens fieldwork analysis.', 'It shows whether a pattern is likely to be real rather than due to chance, allowing a more confident conclusion about the hypothesis.')],
  contrast=[('description of results', 'analysis of results', 'Description states what the data show (patterns, trends, values); analysis explains why, using geographical theory, statistical tests and links to the fieldwork question.'),
            ('a positive correlation', 'a negative correlation', 'In a positive correlation both variables increase together; in a negative correlation one increases as the other decreases.')],
  misc=[('A large sample always guarantees reliable results.', 'Sampling must also be representative and methods consistent; a large biased sample is still unreliable.'),
        ('A significant result proves the hypothesis is true.', 'It means the null hypothesis can be rejected at a confidence level; there remains a chance of error and other explanations.'),
        ('Analysis is just describing graphs.', 'Analysis must interpret patterns, explain them with geographic concepts, use evidence and consider anomalies.')],
  apply=[('An IA investigates whether pedestrian counts decrease with distance from a city\'s CBD. Outline how the student should analyse the results.', 'Plot a scatter graph of distance vs pedestrian count; calculate Spearman\'s rank and test significance; describe the trend with data; explain using bid-rent theory and accessibility; identify and explain anomalies (e.g. a station or shopping centre); link back to the hypothesis.', 4),
         ('Suggest two ways of presenting river channel data in an IA.', 'Cross-sectional profiles drawn to scale; scatter graphs of width vs velocity with best-fit line; proportional symbols on a map; kite diagrams.', 2)],
  cases=[('an IA on CBD-frame land use in Lisbon', 'a student mapped land use at 60 points along transects, used chi-squared to test differences by zone and explained anomalies near metro stations', 'written analysis', 'statistical testing and theory were linked to the question'),
         ('an IA on downstream changes on a river in the Pennines', 'measurements at 8 sites showed width and depth increasing downstream, with Spearman values of 0.88 and 0.76', 'analysis of physical fieldwork data', 'the Bradshaw model provided theory for interpretation'),
         ('an IA on environmental quality in Bogotá', 'scores at 30 sites were compared across wards and correlated with income using Spearman\'s rank', 'analysis of human fieldwork data', 'combining scores and secondary data supported analysis'),
         ('an IA on beach sediment in Brighton', 'pebble size and roundness were measured along the beach to test longshore drift', 'interpretation of anomalies', 'groynes explained anomalies in the expected downdrift pattern')],
  evaluate=[('Statistical tests are essential for a high-quality IA analysis.', ['test significance of patterns', 'quantitative rigour'], ['small samples limit tests', 'qualitative analysis and theory are also valued'], 'Tests strengthen analysis when appropriate, but must be supported by geographical explanation.'),
            ('Quantitative data are more useful than qualitative data in fieldwork investigations.', ['measurable, comparable, testable', 'allow statistical analysis'], ['qualitative data (interviews, photos) explain perceptions and reasons', 'mixed methods give richer analysis'], 'Mixed methods usually give the strongest analysis.')],
  extended=[('Explain how a student can produce a high-quality written analysis in a geography IA.', 'Criterion D; linking to the question; appropriate graphs and maps; statistical tests and significance; geographical theory; anomalies; triangulation; example investigation.', 10, 'long')],
  res=[('Fieldwork data: distance from CBD (m) and pedestrian count per 10 min at 8 sites - 100: 210; 300: 160; 500: 145; 700: 90; 900: 110; 1,100: 60; 1,300: 40; 1,500: 30.',
        [('Identify the anomaly in the data and suggest a reason for it.', '900 m (110) is higher than 700 m (90), against the trend - perhaps a secondary shopping centre, school or transport stop.'),
         ('Ranking both variables from highest (1) to lowest, calculate Σd² and Spearman\'s rank (rs = 1 − 6Σd²/(n³ − n)).', f'Distance ranks 8, 7, 6, 5, 4, 3, 2, 1; count ranks 1, 2, 3, 5, 4, 6, 7, 8; Σd² = 49 + 25 + 9 + 0 + 0 + 9 + 25 + 49 = 166; rs = 1 − (6 × 166)/504 = {1 - 6 * 166 / 504:.3f} - a strong negative correlation, significant at 0.05 (critical value 0.643 for n = 8).')]),
       ('Fieldwork data: land use at 60 points in two zones - Zone A: commercial 22, residential 8; Zone B: commercial 9, residential 21.',
        [('Calculate the percentage of commercial land use in each zone.', f'A: 22/30 = {22 / 30 * 100:.1f}%; B: 9/30 = {9 / 30 * 100:.1f}%'),
         ('Suggest a statistical test to check whether the difference is significant.', 'Chi-squared test of association using a 2 × 2 contingency table (df = 1, critical value 3.84 at 0.05).')])])

S('ch13-st2', gens=['sampling', 'stats_phys', 'chi_phys'],
  terms=[('conclusion (criterion E)', 'the IA criterion (2 marks) for a clear, consistent answer to the fieldwork question based on the analysis'),
         ('evaluation (criterion F)', 'the IA criterion (3 marks) for assessing the strengths and weaknesses of the methods and suggesting improvements'),
         ('formal requirements (criterion G)', 'the IA criterion (4 marks) covering word limit, title page, table of contents, labelled maps and graphs, referencing and bibliography'),
         ('reliability', 'the extent to which a method would give the same results if repeated'),
         ('validity', 'the extent to which data and methods actually measure what the investigation intends to measure'),
         ('word limit', 'the maximum of 2,500 words for the geography IA, excluding labels, tables, references and appendices')],
  facts=[('What is the maximum word count for the IB DP Geography internal assessment?', '2,500 words', ['1,500 words', '4,000 words', '5,000 words'], 'Work beyond the limit is not assessed.'),
         ('The geography IA is marked out of:', '30 marks', ['20 marks', '24 marks', '40 marks'], 'It counts for 25% (SL) or 20% (HL) of the final grade.'),
         ('Which criterion assesses the fieldwork question and geographic context?', 'Criterion A (3 marks)', ['Criterion D (9 marks)', 'Criterion F (3 marks)', 'Criterion G (4 marks)'], 'A requires a focused question, context and a map.'),
         ('Which of these is the strongest evaluation point?', 'Pedestrian counts were taken only on one Tuesday morning, so they may not represent weekend or evening patterns; repeating at different times would improve reliability.', ['The fieldwork was fun.', 'The weather was nice.', 'I should have done better.'], 'Evaluation should be specific, linked to results and suggest improvements.')],
  why=[('Explain why a conclusion should be brief and directly answer the fieldwork question.', 'Criterion E rewards a clear and consistent summary of findings answering the question; new information or long description wastes words within the 2,500 limit.'),
       ('Explain why evaluation should consider the effect of weaknesses on the results.', 'Simply listing problems is not enough; explaining how a limitation (e.g. small sample, timing, equipment) may have biased or limited the results shows understanding of reliability and validity.'),
       ('Explain why a location map is required in the IA.', 'It shows the geographic context and the sites where data were collected, allowing the reader to understand spatial patterns and relate results to place.'),
       ('Explain why sampling strategy affects the validity of fieldwork results.', 'Random, systematic and stratified sampling reduce bias and ensure representativeness; opportunistic or poorly distributed samples may give misleading results.')],
  contrast=[('reliability', 'validity', 'Reliability is whether a method gives consistent results when repeated; validity is whether it measures what it is intended to measure and answers the question.'),
            ('random sampling', 'stratified sampling', 'Random sampling gives every point an equal chance of selection; stratified sampling divides the population into groups and samples each in proportion.')],
  misc=[('The evaluation should only list things that went wrong.', 'It should assess strengths and weaknesses, their effect on results and specific improvements.'),
        ('A longer IA scores more marks.', 'Only the first 2,500 words are assessed; concise, focused writing scores best.'),
        ('A conclusion should introduce new evidence.', 'It should summarise findings already analysed and answer the question.')],
  apply=[('A student measured infiltration rates at 6 sites on one dry day. Evaluate the method and suggest improvements.', 'Strengths: same equipment and procedure at each site; weaknesses: small sample of 6, single day so antecedent moisture not varied, possible operator error; improvements: more sites using stratified sampling by land use, repeat on several days, use a double-ring infiltrometer.', 4),
         ('Suggest how a student can stay within the 2,500-word limit.', 'Use tables, labelled graphs and annotated maps (which are not counted), avoid repetition, keep the introduction and methods concise, and focus analysis on the question.', 2)],
  cases=[('an IA on microclimate in a city park in Vienna', 'temperature and wind speed were measured at 20 sites with a handheld weather meter at 3 times of day', 'evaluating fieldwork methods', 'timing and equipment calibration affected reliability'),
         ('an IA on perception of tourism in Dubrovnik', 'a questionnaire of 50 residents showed most opposed cruise tourism', 'validity of questionnaire data', 'sample composition and question wording affected validity'),
         ('an IA on urban heat island in Singapore', 'a car transect at night recorded a 3.5 °C difference between the CBD and suburbs', 'drawing conclusions from data', 'clear patterns supported a confident conclusion'),
         ('an IA on sand dune succession in Studland, UK', 'quadrats at 10 m intervals along a transect showed increasing species diversity inland', 'systematic sampling', 'regular sampling captured changes along a gradient')],
  evaluate=[('Evaluation is the most important part of a geography IA.', ['shows critical understanding', 'improves future investigations'], ['only 3 of 30 marks; analysis carries 9', 'evaluation depends on good methods and analysis'], 'Evaluation is important, but analysis carries the most marks; both depend on sound methods.'),
            ('Primary data are always more reliable than secondary data.', ['collected by the student for the specific question', 'control of method'], ['small samples and inexperience', 'official secondary data (census) can be large and accurate'], 'Reliability depends on method and sample, not just source; combining both is strongest.')],
  extended=[('Explain how a student should write the conclusion and evaluation of a geography IA.', 'Criteria E and F; answering the question; reliability and validity; specific weaknesses and their effects; improvements; formal requirements (G); word limit.', 10, 'long')],
  res=[('Table: IA criteria (DP Geography) - A fieldwork question and context 3; B method(s) 3; C quality and treatment of information 6; D written analysis 9; E conclusion 2; F evaluation 3; G formal requirements 4.',
        [('Calculate the total marks and the percentage for criteria D and C combined.', f'Total 30; C + D = 15 = {15 / 30 * 100:.0f}%'),
         ('Suggest why criterion D carries the most marks.', 'Analysis shows the student\'s ability to interpret data using geographic understanding, the main skill the IA assesses.')]),
       ('Fieldwork record: temperature readings at a site repeated 5 times - 18.2, 18.6, 18.4, 21.9, 18.3 °C.',
        [('Identify the likely error and calculate the mean with and without it.', f'21.9 is an outlier; mean with = {(18.2 + 18.6 + 18.4 + 21.9 + 18.3) / 5:.2f} °C; without = {(18.2 + 18.6 + 18.4 + 18.3) / 4:.2f} °C'),
         ('Suggest how the reliability of the readings could be improved.', 'Shade the thermometer from direct sun, allow time to settle, calibrate equipment, take readings at the same height and time.')])])

S('ch13-st3', gens=['kof', 'hdi', 'pct_global'],
  terms=[('Paper 3 (HL)', 'the 1-hour HL exam on the HL core extension, with three questions of which one is answered; each has part (a) for 12 marks and part (b) for 16 marks'),
         ('synthesis', 'combining ideas from different parts of the course, scales and perspectives into a coherent argument'),
         ('perspective', 'a viewpoint of a stakeholder or group, shaped by values, interests and power, e.g. government, TNC, NGO, indigenous community'),
         ('geographic concepts', 'the four key concepts of the course - place, process, power and possibility - plus scale, spatial interactions and sustainability'),
         ('markband', 'a descriptor of the quality of an essay answer used to award a level of marks'),
         ('evaluation', 'weighing strengths and weaknesses or arguments to reach a supported judgement')],
  facts=[('Paper 3 (HL) lasts:', '1 hour', ['45 minutes', '1 hour 30 minutes', '2 hours 15 minutes'], 'It is worth 28 marks and 20% of the HL grade.'),
         ('Paper 3 part (b) is marked using markbands out of:', '16 marks', ['10 marks', '12 marks', '28 marks'], 'Part (a) is worth 12 marks.'),
         ('Which are the four key concepts of IB DP Geography?', 'Place, process, power and possibility', ['Scale, time, space and change', 'Supply, demand, price and profit', 'Weather, climate, rock and soil'], 'They are complemented by spatial interactions, scale and sustainability.'),
         ('Paper 3 part (b) questions typically require students to:', 'discuss or evaluate an issue using synthesis, perspectives and examples', ['define one key term', 'complete a map', 'carry out a calculation only'], 'Higher bands require a well-supported conclusion.')],
  why=[('Explain why Paper 3 answers should include a range of perspectives.', 'HL extension themes (power, development, risk) affect stakeholders differently; recognising governments, TNCs, NGOs and communities shows critical thinking and is needed for the top markbands.'),
       ('Explain why synthesis across the HL themes strengthens a Paper 3 essay.', 'Linking global interactions, development, culture and risk shows understanding of interconnections and allows a more nuanced, evaluative argument.'),
       ('Explain why using specific case studies at different scales is valuable.', 'Detailed, place-specific evidence at local, national and global scales supports arguments, shows how processes vary, and is rewarded in the markbands.'),
       ('Explain why an essay should reach a clear conclusion.', 'Command terms such as "to what extent" and "evaluate" require a judgement; the top markbands require a well-supported conclusion based on the evidence discussed.')],
  contrast=[('Paper 3 part (a)', 'Paper 3 part (b)', 'Part (a) (12 marks) usually asks students to explain or analyse a process or pattern; part (b) (16 marks) requires discussion or evaluation with perspectives, synthesis and a conclusion.'),
            ('a descriptive essay', 'an evaluative essay', 'A descriptive essay lists information about a topic; an evaluative essay weighs evidence and arguments to reach a justified judgement.')],
  misc=[('A Paper 3 essay should present only one side of the argument.', 'Higher bands require balance, different perspectives and a justified conclusion.'),
        ('Using more examples always gets more marks.', 'Examples must be relevant, detailed and used to support arguments, not simply listed.'),
        ('Paper 3 only tests knowledge of one HL unit.', 'Questions often require synthesis across the three HL extension themes.')],
  apply=[('Plan a 16-mark answer to: "To what extent is global power still concentrated in a few countries?"', 'Introduction defining power and key concepts; arguments for concentration (USA/China military, IMF voting, TNC headquarters); arguments against (BRICS expansion, G20, non-state actors, civil society, social media); perspectives (emerging economies, NGOs); scales; conclusion: power remains concentrated but is becoming more multipolar and diffuse.', 6),
         ('Suggest how a student could use the concept of "possibility" in a Paper 3 essay on global risks.', 'By discussing future scenarios and alternative strategies - e.g. reshoring vs international cooperation - and evaluating which offers the most sustainable and equitable outcomes.', 3)],
  cases=[('the rise of China as a global power', 'China combines the largest economy by PPP, the Belt and Road Initiative and growing technology firms', 'synthesis of power and global interactions', 'economic, political and cultural power interact at different scales'),
         ('the COVID-19 pandemic', 'it disrupted supply chains, reversed SDG progress and accelerated digital activism and remote work', 'interconnections between HL themes', 'a single risk linked global networks, development and resilience'),
         ('the Belt and Road Initiative in Kenya', 'the Chinese-financed Mombasa-Nairobi railway (2017) improved freight links but raised debt concerns', 'contrasting perspectives', 'governments, lenders, communities and critics view the same project differently'),
         ('climate litigation by Pacific Island states', 'Vanuatu led the request for an International Court of Justice advisory opinion on climate obligations, delivered in 2025', 'power and possibility', 'small states used international institutions to influence global responses')],
  evaluate=[('Global interactions bring more benefits than risks.', ['trade and FDI reduce poverty (China, Vietnam)', 'cultural exchange and technology'], ['financial contagion, supply-chain shocks, environmental damage', 'unequal power and loss of identity'], 'Benefits are large but unevenly shared; risks can be reduced with resilience and fair governance.'),
            ('Non-state actors are now more powerful than states in shaping global interactions.', ['TNCs larger than many economies; tech platforms control information', 'civil society influences norms (#MeToo, Fridays for Future)'], ['states control borders, tariffs, military power and regulation', 'states created and govern international institutions'], 'States remain most powerful, but non-state actors increasingly shape global interactions.')],
  extended=[('Explain how an HL student can show synthesis and evaluation in a Paper 3 essay.', 'Structure; command terms; key concepts (place, process, power, possibility); perspectives; examples at different scales; linking HL themes; balanced argument and conclusion; markbands.', 10, 'long')],
  res=[('Table: Paper 3 (HL) structure - 3 questions offered, 1 answered; part (a) 12 marks; part (b) 16 marks; 60 minutes.',
        [('Calculate a suitable time allocation for parts (a) and (b) in proportion to marks.', f'(a) 12/28 × 60 = {12 / 28 * 60:.0f} minutes; (b) 16/28 × 60 = {16 / 28 * 60:.0f} minutes'),
         ('Suggest why planning time is important.', 'A short plan ensures a clear argument, balanced perspectives and a conclusion that answers the question.')]),
       ('Graph description: share of world GDP (PPP) held by the G7 fell from about 50% in 1990 to about 30% in 2023, while BRICS (original five) rose from about 16% to about 32%.',
        [('Calculate the change in percentage points for each group.', 'G7: −20; BRICS: +16'),
         ('Use the data to discuss a shift in global power.', 'Economic power has moved towards emerging economies, with BRICS now larger than the G7 at PPP, supporting the idea of a multipolar world, though G7 countries still lead in finance, military and technology.')])])
