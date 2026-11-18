"""Cambridge International A Level Geography 9696 (grade 12): the A Level options.

Paper 3 (Physical options: tropical environments, coastal environments, hazardous environments, hot arid and
semi-arid environments) and Paper 4 (Human options: production, location and change; environmental management;
global interdependence; economic transition). For each option: a structured, resource-based question
(figures and tables described in words, answers computed in code, 10 marks) and essays marked out of 20 with
the 9696 four-level mark scheme; case studies need named, located examples with place-specific detail.

Builds on the AS knowledge-pack builders in g11_geography.py (imported, not modified) with level 'A2'.
"""
import math
from ._lib import topic, mcq, compose, person, two_people, city, sf, fmt
from .g9_geography import T, cap, low, an, mean, median, pct_change, nf, MON, MONTHS
from . import g11_geography as _as
from .g11_geography import data, as_c4, kk, sgn, add_spearman, spearman, CRIT, dp

PROFILE = dict(_as.PROFILE)
CHAPTERS = {}


def B(t, P):
    return _as.B(t, P, lvl='A2')


def sd(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


# ============================================================== CHAPTER 1: Tropical climates

TSTAT = [
    ('Singapore (1°N), humid tropical', [234, 113, 175, 165, 171, 131, 158, 176, 169, 194, 256, 288], [26.5, 27.1, 27.5, 28.0, 28.3, 28.3, 27.9, 27.9, 27.6, 27.6, 27.0, 26.5]),
    ('Manaus, Brazil (3°S), humid tropical', [260, 290, 315, 300, 255, 115, 85, 60, 85, 125, 185, 220], [26.1, 26.0, 26.1, 26.2, 26.4, 26.6, 26.8, 27.5, 28.0, 27.9, 27.3, 26.7]),
    ('Kano, Nigeria (12°N), seasonally humid', [0, 0, 2, 9, 60, 110, 200, 300, 130, 15, 0, 0], [22, 25, 29, 31, 30, 28, 26, 25, 26, 27, 25, 22]),
    ('Darwin, Australia (12°S), seasonally humid', [420, 360, 320, 100, 20, 2, 1, 5, 15, 70, 140, 250], [28.5, 28.3, 28.4, 28.3, 27.2, 25.5, 25.1, 26.0, 27.9, 29.1, 29.4, 29.0]),
    ('Kolkata, India (22°N), monsoonal', [12, 22, 33, 48, 135, 300, 360, 340, 300, 160, 25, 6], [20, 23, 28, 31, 31, 31, 30, 30, 30, 29, 25, 21]),
    ('Lusaka, Zambia (15°S), seasonally humid', [230, 190, 140, 20, 3, 0, 0, 0, 1, 15, 90, 200], [22, 22, 22, 21, 19, 16, 16, 19, 23, 25, 24, 22]),
]

t1a = T('Distribution and characteristics of humid tropical and seasonally humid climates', 'distribution characteristics of humid tropical seasonally humid climates')
B(t1a, {
    'terms': [
        ('humid tropical (equatorial) climate', 'a climate with high temperatures (about 26-28 °C) all year, a small annual range and heavy rainfall in every month, typically over 2000 mm a year'),
        ('seasonally humid tropical (savanna) climate', 'a tropical climate with a distinct wet season and dry season, and annual rainfall of about 500-1500 mm'),
        ('annual temperature range', 'the difference between the mean temperatures of the warmest and coolest months'),
        ('diurnal temperature range', 'the difference between the maximum and minimum temperatures within a 24-hour period'),
        ('convectional rainfall', 'rain caused by intense surface heating, rising air, cooling and condensation, often in afternoon thunderstorms'),
        ('Köppen classification', 'a climate classification based on temperature and precipitation; Af is tropical rainforest, Aw is tropical savanna and Am is tropical monsoon'),
    ],
    'mcq': [
        ('In the humid tropics the diurnal temperature range is usually', 'greater than the annual temperature range', ['smaller than the annual temperature range', 'zero', 'over 30 °C'], '[1]'),
        ('Seasonally humid tropical climates are found mainly', 'between about 5° and 20° north and south of the equator', ['along the equator only', 'between 30° and 40°', 'inside the Arctic Circle'], '[1]'),
        ('The Köppen code for a tropical savanna climate is', 'Aw', ['Af', 'BWh', 'Cfb'], '[1]'),
        ('In a seasonally humid climate, the hottest month usually comes', 'just before the wet season begins', ['in the middle of the wet season', 'at the end of the wet season', 'in the coolest month'], 'Clear skies and a high sun precede the rains. [1]'),
    ],
    'explain': [
        ('Describe the characteristics of the humid tropical climate.', 'Mean monthly temperatures about 26-28 °C with an annual range under 3 °C; high humidity; annual rainfall 1500-3000 mm, falling in all months, often in afternoon convectional storms; no distinct dry season (or a short one).', '1 mark per characteristic with data [4]'),
        ('Compare the climate of a seasonally humid tropical area with that of a humid tropical area.', 'Both are hot all year; seasonally humid areas have a larger annual temperature range, lower annual rainfall concentrated in a wet season, and a dry season of several months with low humidity.', '1 mark per developed comparison [3]'),
        ('Explain why temperatures in the humid tropics vary little through the year.', 'The sun is high in the sky all year and day length is about 12 hours, so insolation is consistently high; cloud cover limits extremes.', '[2]'),
    ],
    'claims': [
        ('Equatorial climates are the hottest climates in the world.', False, 'Hot deserts have higher maximum temperatures because skies are clear; cloud keeps equatorial maxima around 30-32 °C.'),
        ('The length of the dry season increases with distance from the equator in the tropics.', True, 'Further from the equator the ITCZ is overhead for a shorter period.'),
        ('Rainfall in the seasonally humid tropics is reliable from year to year.', False, 'Rainfall varies greatly between years, causing drought, as in the Sahel.'),
    ],
    'essays': [
        ('the difference between humid tropical and seasonally humid tropical climates is mainly a difference of rainfall rather than temperature',
         ['Rainfall total and seasonality define the contrast: rain in all months near the equator versus a long dry season further away; temperatures are hot all year in both.'],
         ['Seasonally humid areas have larger annual and diurnal temperature ranges, higher maxima before the rains and cooler dry-season nights; humidity and evapotranspiration differ.'],
         'Rainfall regime is the defining difference, though temperature range differences are significant and linked to it.',
         ['the ITCZ', 'temperature range', 'dry season', 'Köppen classification']),
    ],
})


@data(t1a)
def t1a_clim(r, D):
    nm, rain, temp = r.choice(TSTAT)
    rain = [max(0, round(x * r.uniform(0.92, 1.08))) for x in rain]
    tot = sum(rain)
    dry = [MON[i] for i in range(12) if rain[i] < 60]
    tr = max(temp) - min(temp)
    stem = f'Table 1.1 shows climate data for {nm}. ' + ' '.join(f'{MON[i]}: {fmt(temp[i], 1)} °C, {rain[i]} mm.' for i in range(12))
    pc = max(rain) / tot * 100
    if D == 1:
        opts, a = mcq(r, f'{dp(tr, 1)} °C', [f'{dp(max(temp), 1)} °C', f'{dp(mean(temp), 1)} °C', f'{dp(tr * 2, 1)} °C', f'{dp(tr + 3, 1)} °C'])
        return {'stem': stem + ' What is the annual temperature range?', 'options': opts, 'answer': a, 'key': f'{fmt(max(temp), 1)} − {fmt(min(temp), 1)} = {dp(tr, 1)} °C. [1]'}
    parts = [
        lambda r: ('Calculate the annual rainfall total and the annual temperature range.', f'{nf(tot)} mm; {dp(tr, 1)} °C', '1 mark each [2]'),
        lambda r: ('Identify the dry months (less than 60 mm).', ', '.join(dry) if dry else 'None: every month has at least 60 mm.', '[1]'),
        lambda r: ('Calculate the percentage of annual rainfall falling in the wettest month.', f'{dp(pc)}%', f'{max(rain)} ÷ {nf(tot)} × 100 [2]'),
        lambda r: ('State whether the station has a humid tropical or a seasonally humid climate. Justify your answer with data.', ('Humid tropical: rain in all or nearly all months and a small temperature range.' if len(dry) <= 2 else 'Seasonally humid: a distinct dry season of several months.'), '1 mark type; 1 mark data [2]'),
        lambda r: ('Explain the pattern of rainfall shown.', 'Rain falls when the ITCZ lies overhead, with convergence of trade winds, intense heating and convectional uplift; dry months occur when the ITCZ has moved to the other hemisphere and the subtropical high or dry trade winds dominate.', '1 mark per developed point [3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t1b = T('Causes of tropical climates: ITCZ, trade winds and subtropical high pressure', 'causes of tropical climates itcz trade winds subtropical high pressure')
B(t1b, {
    'terms': [
        ('ITCZ', 'the Inter-Tropical Convergence Zone, a belt of low pressure where the north-east and south-east trade winds converge'),
        ('subtropical high pressure', 'belts of sinking, warming, dry air at about 25-35° N and S, associated with deserts'),
        ('trade winds', 'steady winds blowing from the subtropical highs towards the ITCZ'),
        ('Hadley cell', 'the low-latitude circulation cell with rising air at the ITCZ, poleward flow aloft, sinking air at the subtropical highs and surface trade winds'),
        ('Walker circulation', 'an east-west circulation over the tropical Pacific, which weakens or reverses during El Niño'),
        ('El Niño Southern Oscillation (ENSO)', 'a periodic warming of the eastern tropical Pacific that changes pressure, winds and rainfall across the tropics'),
    ],
    'mcq': [
        ('Air sinking in the subtropical highs is dry because', 'it warms adiabatically as it descends, lowering relative humidity', ['it is cooled by the ocean', 'it has passed over mountains', 'it contains more water vapour'], '[1]'),
        ('During an El Niño event, rainfall usually', 'decreases over Indonesia and northern Australia and increases over coastal Peru', ['increases over Indonesia', 'is unchanged everywhere', 'increases over the Atacama only in winter'], '[1]'),
        ('The ITCZ moves furthest from the equator over', 'large continents such as Asia and Africa', ['the central Pacific Ocean', 'Antarctica', 'small islands'], '[1]'),
        ('Converging trade winds at the ITCZ produce', 'rising air, cumulonimbus clouds and heavy rain', ['sinking air and clear skies', 'frost and fog', 'strong westerly winds'], '[1]'),
    ],
    'explain': [
        ('Explain how the Hadley cell produces both humid and arid tropical climates.', 'At the ITCZ, intense heating and convergence cause air to rise, cool and condense, giving heavy rain; the air flows polewards aloft, cools, and sinks at about 30°, warming adiabatically and creating dry subtropical highs; trade winds return air to the ITCZ.', '1 mark per stage [4]'),
        ('Explain the seasonal migration of the ITCZ and its effect on rainfall.', 'The ITCZ follows the zone of maximum heating (overhead sun) north in June-July and south in December-January, bringing a wet season to the areas it passes over; places it does not reach remain dry.', '[3]'),
        ('Explain how El Niño affects tropical climates.', 'Weakened trade winds allow warm water to spread east; convection shifts to the central and eastern Pacific; drought in Indonesia, Australia and southern Africa; floods in Peru and Ecuador; weaker Indian monsoon.', '1 mark per point [3]'),
    ],
    'claims': [
        ('The ITCZ follows the overhead sun exactly.', False, 'It lags the sun by a few weeks and migrates further over land than over the oceans.'),
        ('Trade winds in the Southern Hemisphere blow from the south-east.', True, 'Air moving towards the equator is deflected to the left by the Coriolis effect.'),
        ('The subtropical high pressure belts are associated with heavy rainfall.', False, 'Sinking air suppresses cloud formation, producing the world’s hot deserts.'),
    ],
    'essays': [
        ('the movement of the ITCZ is the main factor explaining the climates of the tropics',
         ['The ITCZ brings convergence and convectional rain, controlling the timing and length of wet seasons from equatorial to savanna climates.'],
         ['Subtropical highs, cold ocean currents, relief and rain shadows, monsoon pressure systems and ENSO also shape tropical climates; local factors create variation (e.g. the dry coast of Peru).'],
         'The ITCZ is the main control over rainfall seasonality, but other circulation features and local factors are needed for a full explanation.',
         ['the Hadley cell', 'monsoons', 'ocean currents', 'ENSO']),
    ],
})


@data(t1b)
def t1b_itcz(r, D):
    lat = r.choice([2, 5, 8, 12, 15, 18])
    hem = r.choice(['N', 'S'])
    north = {2: 11, 5: 9, 8: 7, 12: 5, 15: 4, 18: 3}[lat]
    stn = f'a station at {lat}°{hem}'
    months = north
    stem = (f'Fig. 1.2 shows that the ITCZ migrates between about 5°S in January and 20°N in July over Africa. A student estimates that {stn} lies within the rainy zone of the ITCZ for about {months} months of the year.')
    dry = 12 - months
    if D == 1:
        opts, a = mcq(r, f'{dry} months', [f'{months} months', f'{12 - dry // 2} months', '12 months', f'{max(1, dry - 2)} months' if dry > 2 else '6 months'])
        return {'stem': stem + ' How long is the dry season likely to be?', 'options': opts, 'answer': a, 'key': f'12 − {months} = {dry} months. [1]'}
    wet = ('June-September' if hem == 'N' else 'December-March') if lat >= 8 else 'two rainy seasons around the equinoxes'
    parts = [
        lambda r: ('Calculate the likely length of the dry season.', f'{dry} months', f'12 − {months} [1]'),
        lambda r: ('Suggest when the wet season occurs at this station.', wet, '[1]'),
        lambda r: ('Explain why places near the equator may have two rainfall maxima.', 'The ITCZ passes overhead twice a year, around the equinoxes, as it moves north and then south.', '[2]'),
        lambda r: ('Explain why the dry season becomes longer with distance from the equator.', 'The ITCZ spends less time over places nearer its limits; for the rest of the year they are under the influence of the subtropical high and dry trade winds.', '[2]'),
        lambda r: ('Suggest why the ITCZ moves further north over Africa and Asia than over the Atlantic Ocean.', 'Land heats up more than the sea in summer, creating a stronger thermal low further from the equator.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t1c = T('Tropical cyclones and monsoon rainfall in tropical climates', 'tropical cyclones monsoon rainfall in tropical climates')
SS = [(119, 153, 1), (154, 177, 2), (178, 208, 3), (209, 251, 4), (252, 400, 5)]


def ss_cat(v):
    for lo, hi, c in SS:
        if lo <= v <= hi:
            return c
    return 0


B(t1c, {
    'terms': [
        ('tropical cyclone', 'an intense low-pressure system that forms over warm tropical oceans, with sustained winds of at least 119 km/h; called a hurricane or typhoon in some regions'),
        ('eye of a cyclone', 'the calm, cloud-free centre of a tropical cyclone, where air sinks'),
        ('eyewall', 'the ring of towering cumulonimbus clouds around the eye, with the strongest winds and heaviest rain'),
        ('storm surge', 'a rise in sea level caused by low pressure and onshore winds pushing water towards the coast during a cyclone'),
        ('Saffir-Simpson scale', 'a 1-5 scale classifying hurricanes by sustained wind speed'),
        ('monsoon trough', 'the zone of low pressure into which monsoon winds blow, associated with the ITCZ over South Asia in summer'),
    ],
    'mcq': [
        ('Tropical cyclones normally form only where sea-surface temperatures are at least', '26-27 °C', ['10 °C', '18 °C', '35 °C'], '[1]'),
        ('Tropical cyclones do not form within about 5° of the equator because', 'the Coriolis effect is too weak to start rotation', ['the sea is too cold', 'there are no thunderstorms', 'pressure is too high'], '[1]'),
        ('A hurricane with sustained winds of 230 km/h is in Saffir-Simpson category', '4', ['2', '3', '5'], 'Category 4: 209-251 km/h. [1]'),
        ('In the Northern Hemisphere tropical cyclones rotate', 'anticlockwise', ['clockwise', 'not at all', 'east to west only'], '[1]'),
    ],
    'explain': [
        ('Explain the conditions needed for tropical cyclones to form.', 'Sea surface at least 26-27 °C to a depth of about 60 m; latitude 5-20° so the Coriolis effect is strong enough; low vertical wind shear; moist, unstable air; an initial disturbance such as an easterly wave; upper-level divergence.', '1 mark per condition [4]'),
        ('Explain why tropical cyclones weaken when they move over land.', 'They lose their supply of warm, moist air and latent heat; friction over land reduces wind speed.', '[2]'),
        ('Explain the contribution of tropical cyclones to rainfall in tropical climates.', 'They bring very heavy rain over a few days (often hundreds of mm), contributing a large share of annual rainfall in places such as the Philippines and north-west Australia, but also floods and landslides.', '[3]'),
    ],
    'claims': [
        ('Tropical cyclones are most frequent in late summer and autumn.', True, 'Sea-surface temperatures peak then, e.g. August-October in the North Atlantic.'),
        ('The strongest winds in a tropical cyclone are in the eye.', False, 'The eye is calm; the strongest winds are in the eyewall.'),
        ('Monsoon rainfall is the same every year.', False, 'Monsoon onset, strength and breaks vary, linked to ENSO and other factors.'),
    ],
    'essays': [
        ('tropical cyclones bring more benefits than problems to tropical environments',
         ['They supply rainfall that recharges water stores and reservoirs, break droughts and redistribute heat.'],
         ['They cause storm surges, flooding, landslides and destruction of crops and buildings (Cyclone Idai 2019, Typhoon Haiyan 2013); deaths and long recovery.'],
         'Physical benefits exist, but for people the damage usually outweighs them, especially in vulnerable low-income countries.',
         ['rainfall', 'storm surge', 'vulnerability', 'ecosystems']),
    ],
})


@data(t1c)
def t1c_cyc(r, D):
    names = ['Haiyan (2013, Philippines)', 'Idai (2019, Mozambique)', 'Katrina (2005, USA)', 'Nargis (2008, Myanmar)', 'Maria (2017, Puerto Rico)', 'Amphan (2020, India/Bangladesh)', 'Ian (2022, USA)']
    nm = r.choice(names)
    obs = [('day 1', r.randint(60, 110)), ('day 2', r.randint(110, 180)), ('day 3', r.randint(180, 290)), ('day 4', r.randint(140, 250)), ('day 5 (after landfall)', r.randint(60, 120))]
    stem = f'Table 1.3 shows the maximum sustained wind speed (km/h) of a tropical cyclone similar to {nm} on successive days: ' + ', '.join(f'{d} {v}' for d, v in obs) + '. Saffir-Simpson categories: 1: 119-153, 2: 154-177, 3: 178-208, 4: 209-251, 5: 252 or more.'
    cats = [(d, ss_cat(v)) for d, v in obs]
    pk = max(obs, key=lambda x: x[1])
    if D == 1:
        c = ss_cat(pk[1])
        opts, a = mcq(r, f'Category {c}', [f'Category {k}' for k in range(1, 6) if k != c])
        return {'stem': stem + ' What was the highest category reached?', 'options': opts, 'answer': a, 'key': f'{pk[1]} km/h = category {c}. [1]'}
    parts = [
        lambda r: ('Classify the storm on each day using the Saffir-Simpson scale.', '; '.join(f'{d}: ' + (f'category {c}' if c else 'below hurricane strength') for d, c in cats), '[2]'),
        lambda r: ('Calculate the percentage fall in wind speed between the peak and day 5.', f'{dp((pk[1] - obs[-1][1]) / pk[1] * 100)}%', f'({pk[1]} − {obs[-1][1]}) ÷ {pk[1]} × 100 [2]'),
        lambda r: ('Explain why the storm intensified over the first three days.', 'It moved over very warm ocean water (above 27 °C), with low wind shear; evaporation supplied moisture and condensation released latent heat, fuelling stronger winds.', '[3]'),
        lambda r: ('Explain why the storm weakened after landfall.', 'Loss of warm, moist air and latent heat energy; increased surface friction.', '[2]'),
        lambda r: ('Explain why storm surge often causes more deaths than wind.', 'Low pressure and strong onshore winds raise sea level several metres, flooding low-lying coasts and deltas quickly, e.g. Nargis in the Irrawaddy delta.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[1] = [t1a, t1b, t1c]


# ============================================================== CHAPTER 2: Tropical landforms and weathering

t2a = T('Weathering in humid tropics: deep weathering profiles and the weathering front', 'weathering in humid tropics deep weathering profiles weathering front')
B(t2a, {
    'terms': [
        ('weathering front', 'the boundary between weathered material (regolith) and unweathered bedrock'),
        ('regolith', 'the layer of loose, weathered material lying above solid bedrock'),
        ('saprolite', 'chemically weathered rock that has rotted in place but keeps its original structure'),
        ('corestone', 'a rounded block of less-weathered rock surrounded by saprolite in a weathering profile'),
        ('laterite', 'a hard, iron- and aluminium-rich layer formed by intense chemical weathering and leaching in the tropics'),
        ('deep weathering', 'chemical weathering that extends tens of metres below the surface in warm, wet climates'),
        ('basal surface of weathering', 'another name for the weathering front, the irregular lower limit of the regolith'),
    ],
    'mcq': [
        ('Weathering profiles in the humid tropics may reach depths of', 'over 60 m', ['less than 1 m', 'exactly 2 m', 'over 5 km'], '[1]'),
        ('The dominant weathering process in granite in the humid tropics is', 'hydrolysis', ['freeze-thaw', 'exfoliation', 'salt crystallisation'], '[1]'),
        ('Deep weathering profiles are found mainly on', 'ancient, tectonically stable land surfaces such as continental shields', ['young fold mountains', 'active volcanoes', 'glaciated valleys'], '[1]'),
        ('The weathering front is irregular mainly because', 'weathering penetrates further along joints and fractures', ['the climate changes daily', 'animals dig it', 'it is eroded by wind'], '[1]'),
    ],
    'explain': [
        ('Explain why weathering profiles are so deep in the humid tropics.', 'High temperatures speed chemical reactions; abundant rainfall all year provides water; organic acids from rapid decay; long periods of stability without glaciation or erosion; joints allow water to penetrate deeply.', '1 mark per factor [4]'),
        ('Describe a typical deep weathering profile in granite.', 'From the surface down: soil and lateritic crust; completely weathered clay-rich saprolite; partially weathered zone with corestones; weathering front; fresh jointed bedrock.', '1 mark per zone in order [4]'),
        ('Explain how the weathering front can later be exposed to form landforms.', 'Changes in base level or climate increase erosion, which strips away the regolith (etching), exposing corestones and the irregular weathering front as tors and inselbergs.', '[3]'),
    ],
    'claims': [
        ('Physical weathering dominates in the humid tropics.', False, 'Chemical weathering dominates because of heat and moisture.'),
        ('The weathering front is usually a smooth, flat surface.', False, 'It is highly irregular because weathering follows joints.'),
        ('Corestones are evidence that weathering acts from joints inwards.', True, 'Blocks bounded by joints are weathered from their edges, leaving rounded cores.'),
    ],
    'essays': [
        ('climate is the most important factor in explaining the depth of weathering in tropical environments',
         ['High temperatures and rainfall drive rapid chemical weathering (hydrolysis, carbonation, chelation).'],
         ['Rock type and jointing, time and tectonic stability (Gondwana shields), relief and drainage, vegetation and erosion rates control how deep profiles become.'],
         'Climate sets the rate, but depth depends on long periods of stability, rock structure and slow removal of regolith.',
         ['rock type', 'time', 'relief', 'vegetation']),
    ],
})


@data(t2a)
def t2a_prof(r, D):
    zones = ['soil and lateritic crust', 'completely weathered saprolite', 'partially weathered rock with corestones']
    th = [round(r.uniform(1, 4), 1), round(r.uniform(8, 35), 1), round(r.uniform(4, 15), 1)]
    tot = sum(th)
    age = r.choice([2, 5, 10, 20])  # million years
    rate = tot / age  # m per Ma
    plc = r.choice(['a borehole in granite in Nigeria', 'a road cutting in granite in Malaysia', 'a quarry in gneiss in Uganda', 'a borehole in granite in Brazil'])
    stem = f'Fig. 2.1 shows a weathering profile from {plc}. Thicknesses: ' + ', '.join(f'{z} {fmt(t, 1)} m' for z, t in zip(zones, th)) + f'. The weathering front is below this. Dating suggests the profile developed over about {age} million years.'
    if D == 1:
        opts, a = mcq(r, f'{dp(tot, 1)} m', [f'{dp(tot - th[0], 1)} m', f'{dp(th[1], 1)} m', f'{dp(tot * 2, 1)} m', f'{dp(tot / 3, 1)} m'])
        return {'stem': stem + ' What is the depth to the weathering front?', 'options': opts, 'answer': a, 'key': ' + '.join(fmt(t, 1) for t in th) + f' = {dp(tot, 1)} m. [1]'}
    parts = [
        lambda r: ('Calculate the depth of the weathering front below the surface.', f'{dp(tot, 1)} m', 'sum of thicknesses [1]'),
        lambda r: ('Calculate the mean rate of advance of the weathering front in metres per million years.', f'{dp(rate, 2)} m per million years', f'{dp(tot, 1)} ÷ {age} [2]'),
        lambda r: ('Calculate the percentage of the profile made up of saprolite.', f'{dp(th[1] / tot * 100)}%', f'{fmt(th[1], 1)} ÷ {dp(tot, 1)} × 100 [1]'),
        lambda r: ('Explain the formation of corestones in the lower zone.', 'Water penetrates along joints; hydrolysis attacks the edges and corners of joint-bounded blocks most rapidly, rounding them and leaving fresh cores surrounded by weathered material.', '[3]'),
        lambda r: ('Suggest why the measured rate may be an underestimate of present-day weathering.', 'The top of the profile has been eroded; climate may have been drier in the past; dating is uncertain.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t2b = T('Granite landforms: tors, inselbergs and bornhardts', 'granite landforms tors inselbergs bornhardts')
B(t2b, {
    'terms': [
        ('inselberg', 'an isolated, steep-sided hill rising abruptly from a plain, typical of tropical shield areas'),
        ('bornhardt', 'a large, dome-shaped inselberg of massive, sparsely jointed rock, such as Sugarloaf Mountain in Rio de Janeiro'),
        ('tor', 'a small exposure of jointed rock, often granite, forming piles of blocks on hilltops'),
        ('kopje (castle koppie)', 'a small inselberg made of piles of granite blocks, common in southern Africa'),
        ('etchplain', 'a surface formed when the regolith has been stripped away, exposing the irregular weathering front'),
        ('two-stage theory', 'the idea that tors and inselbergs form first by deep weathering and then by stripping of the regolith (Linton; Thomas)'),
        ('sheet joints', 'curved joints parallel to the surface of granite domes, formed by pressure release'),
    ],
    'mcq': [
        ('Sugarloaf Mountain (Pão de Açúcar) in Rio de Janeiro is an example of', 'a bornhardt', ['a tor of limestone', 'a karst tower', 'a volcanic plug of basalt'], '[1]'),
        ('Linton’s two-stage theory explains tors as the result of', 'deep chemical weathering followed by removal of the regolith', ['glacial erosion only', 'wind abrasion', 'volcanic eruption'], '[1]'),
        ('Uluru (Australia) is an inselberg made of', 'arkose sandstone', ['granite', 'limestone', 'basalt'], '[1]'),
        ('Bornhardts survive as high domes mainly because they', 'are massive with widely spaced joints, so water penetrates little', ['are made of soft rock', 'are covered by ice', 'have many joints'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of inselbergs.', 'Deep chemical weathering penetrates further where joints are closely spaced; areas of massive rock remain unweathered; later stripping of regolith (base-level fall, climate change) exposes these as isolated hills; scarp retreat and pediplanation (King) may also contribute.', '1 mark per stage [4]'),
        ('Explain the role of jointing in the formation of granite landforms.', 'Joint spacing controls where water penetrates and chemical weathering is concentrated; widely jointed rock forms domes (bornhardts); closely jointed rock breaks into blocks (tors, kopjes); sheet joints shape domes.', '[3]'),
        ('Compare the theories of King and Thomas for the origin of inselbergs.', 'King: parallel retreat of slopes in semi-arid conditions leaves residual hills above pediplains. Thomas: deep weathering beneath a humid climate followed by stripping (two-stage).', '[3]'),
    ],
    'claims': [
        ('Inselbergs only form in present-day hot deserts.', False, 'Many formed under humid tropical weathering and are now found in savanna and arid lands.'),
        ('Tors can form by deep weathering and stripping.', True, 'Linton’s two-stage theory explains Dartmoor tors this way.'),
        ('All inselbergs are made of granite.', False, 'Uluru is sandstone and Kata Tjuta conglomerate.'),
    ],
    'essays': [
        ('the formation of granite landforms in the tropics is explained better by deep weathering than by slope retreat',
         ['Exposed weathering fronts, corestones and etchplains support the two-stage theory (Thomas, Linton); joints control where weathering penetrates.'],
         ['King’s parallel slope retreat and pediplanation explain inselbergs in semi-arid Africa; multiple cycles of weathering and stripping and climate change complicate both.'],
         'Deep weathering explains many tropical granite landforms, but slope retreat and climate change are needed to explain their exposure and shape.',
         ['joint spacing', 'two-stage theory', 'pediplains', 'climate change']),
    ],
})


@data(t2b, c4=False)
def t2b_joint(r, D):
    sites = []
    for nm in ('A', 'B', 'C', 'D'):
        js = round(r.uniform(0.3, 8.0), 1)
        h = round(max(5, js * r.uniform(15, 40) + r.uniform(-20, 20)))
        sites.append((f'Hill {nm}', js, h))
    stem = 'Table 2.2 shows mean joint spacing (m) and height above the surrounding plain (m) for four granite hills in Zimbabwe: ' + '; '.join(f'{n}: joint spacing {fmt(j, 1)} m, height {h} m' for n, j, h in sites) + '.'
    hi = max(sites, key=lambda x: x[2])
    if D == 1:
        opts, a = mcq(r, hi[0], [s[0] for s in sites if s is not hi])
        return {'stem': stem + ' Which hill stands highest above the plain?', 'options': opts, 'answer': a, 'key': f'{hi[0]}: {hi[2]} m. [1]'}
    parts = [
        lambda r: ('Describe the relationship between joint spacing and height.', 'Generally, hills with more widely spaced joints stand higher.', '[1]'),
        lambda r: ('Explain this relationship.', 'Widely spaced joints allow little water to penetrate, so the rock resists chemical weathering and survives as high domes when regolith is stripped; closely jointed rock is weathered deeply and removed.', '[3]'),
        lambda r: ('Suggest which hill is most likely to be a bornhardt and which a kopje. Give reasons.', f'Bornhardt: {max(sites, key=lambda x: x[1])[0]} (widest joints, massive dome); kopje: {min(sites, key=lambda x: x[1])[0]} (closely jointed, piles of blocks).', '1 mark each with reason [2]'),
        lambda r: ('Suggest why a sample of four hills is not enough to reach a reliable conclusion.', 'Too small for statistical testing (e.g. Spearman’s rank needs about 8-10); other factors such as rock composition may vary.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t2c = T('Limestone landforms in the tropics: karst towers and cockpit karst', 'limestone landforms in the tropics karst towers cockpit karst')
B(t2c, {
    'terms': [
        ('tower karst', 'a landscape of steep-sided, isolated limestone hills (towers) rising from a flat plain, such as around Guilin, China'),
        ('cockpit karst', 'a landscape of closely spaced conical hills separated by star-shaped depressions (cockpits), as in Jamaica'),
        ('doline', 'a closed depression in limestone formed by solution or collapse'),
        ('carbonation', 'the reaction between carbonic acid and calcium carbonate, producing soluble calcium bicarbonate'),
        ('foot cave', 'a notch or cave at the base of a karst tower, formed by solution where water lies against it'),
        ('allogenic water', 'water flowing onto limestone from adjacent impermeable rocks, which increases solution'),
    ],
    'mcq': [
        ('The tower karst landscapes around Guilin and Yangshuo are in', 'southern China', ['Jamaica', 'Iceland', 'Egypt'], '[1]'),
        ('The Cockpit Country is found in', 'Jamaica', ['Vietnam', 'Brazil', 'Madagascar'], '[1]'),
        ('Solution of limestone is especially rapid in the humid tropics because', 'heavy rainfall and decaying vegetation supply abundant carbonic and organic acids', ['the water is very cold', 'there is no vegetation', 'limestone is harder there'], '[1]'),
        ('Ha Long Bay in Vietnam is an example of', 'drowned tower karst', ['a coral atoll', 'a fjord', 'a volcanic island arc'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of cockpit karst.', 'Solution is concentrated where water drains into depressions along joints; depressions deepen and enlarge into star-shaped cockpits; the intervening areas remain as conical hills; heavy rainfall and organic acids speed the process.', '1 mark per stage [3]'),
        ('Explain the formation of tower karst.', 'Solution of limestone down to a level of the water table or impermeable rock leaves isolated towers; lateral solution by swamps and rivers at the base (foot caves) undercuts and steepens them; alluvial plains form between towers.', '1 mark per point [4]'),
        ('Explain why tropical karst differs from temperate karst.', 'Higher rainfall, temperatures and biogenic CO₂ cause more rapid solution, producing larger-scale positive landforms (towers, cones) rather than mainly negative forms (pavements, dolines).', '[3]'),
    ],
    'claims': [
        ('Cold water dissolves limestone faster, so tropical karst should be less developed.', False, 'Although cold water holds more CO₂, tropical soils produce far more CO₂ and rainfall is greater, so tropical solution rates are high.'),
        ('Karst towers are always surrounded by flat alluvial plains.', False, 'Some form in groups on uplifted plateaus or are drowned by the sea (Ha Long Bay).'),
        ('Rock structure and jointing influence the pattern of cockpits.', True, 'Solution follows joints, so depressions are aligned with them.'),
    ],
    'essays': [
        ('the landforms of tropical karst are mainly the result of climate',
         ['Intense rainfall and biogenic CO₂ produce rapid solution and large cockpits and towers (Guilin, Jamaica, Ha Long Bay).'],
         ['Rock purity, jointing, uplift and base level, tectonic history and allogenic rivers control where towers and cockpits develop; similar forms occur in some non-tropical areas.'],
         'Climate accounts for the intensity and scale of tropical karst, but geology and tectonics determine its form and distribution.',
         ['solution', 'rock structure', 'uplift', 'base level']),
    ],
})


@data(t2c)
def t2c_corbel(r, D):
    E = r.choice([5, 8, 10, 12, 15, 20])   # runoff in decimetres
    Tc = r.randint(40, 180)   # mg/l CaCO3
    X = 4 * E * Tc / 100
    plc = r.choice(['Guilin, China', 'the Cockpit Country, Jamaica', 'northern Vietnam', 'Puerto Rico', 'the Yorkshire Dales, UK', 'the Burren, Ireland'])
    stem = (f'Corbel’s formula estimates limestone solution: X = 4ET ÷ 100, where X is the rate of solution (m³ per km² per year, equal to mm per 1000 years), E is annual runoff in decimetres and T is the mean concentration of dissolved CaCO₃ in mg/l. '
            f'In {plc}, E = {E} dm ({E * 100} mm) and T = {Tc} mg/l.')
    if D == 1:
        opts, a = mcq(r, f'{dp(X, 1)} mm per 1000 years', [f'{dp(4 * E * Tc, 0)} mm per 1000 years', f'{dp(E * Tc / 100, 1)} mm per 1000 years', f'{dp(X / 10, 2)} mm per 1000 years', f'{dp(X * 2, 1)} mm per 1000 years'])
        return {'stem': stem + ' What is the rate of solution?', 'options': opts, 'answer': a, 'key': f'4 × {E} × {Tc} ÷ 100 = {dp(X, 1)}. [1]'}
    yrs = r.choice([100000, 500000, 1000000])
    low = X * yrs / 1000 / 1000
    parts = [
        lambda r: ('Calculate the rate of solution.', f'{dp(X, 1)} m³ per km² per year ({dp(X, 1)} mm per 1000 years)', f'4 × {E} × {Tc} ÷ 100 [2]'),
        lambda r: (f'Calculate how much the limestone surface would be lowered in {nf(yrs)} years at this rate.', f'{dp(low, 2)} m', f'{dp(X, 1)} mm × {yrs // 1000} = {dp(X * yrs / 1000, 0)} mm [2]'),
        lambda r: ('Explain why solution rates in the humid tropics are usually higher than in temperate areas.', 'Higher runoff from heavy rainfall; high soil CO₂ from rapid decay of vegetation increases acidity; warm temperatures speed reactions.', '[3]'),
        lambda r: ('Suggest one limitation of Corbel’s formula.', 'It assumes all CaCO₃ comes from limestone in the basin and ignores solution underground, variation in runoff and concentration over time, and dolomite or other rocks.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[2] = [t2a, t2b, t2c]


# ============================================================== CHAPTER 3: Tropical ecosystems

t3a = T('Tropical rainforest ecosystem: structure, nutrient cycling and soils', 'tropical rainforest ecosystem structure nutrient cycling soils')
B(t3a, {
    'terms': [
        ('emergent layer', 'the tallest trees of the rainforest, up to 50-60 m high, rising above the main canopy'),
        ('canopy', 'the continuous layer of tree crowns at about 30-40 m that intercepts most sunlight'),
        ('nutrient cycle', 'the transfer of nutrients between the biomass, litter and soil stores of an ecosystem'),
        ('Gersmehl diagram', 'a model showing the relative sizes of the biomass, litter and soil nutrient stores and the transfers between them'),
        ('ferralitic soil (oxisol)', 'a deep, red, highly weathered and leached tropical soil, rich in iron and aluminium oxides but poor in nutrients'),
        ('leaching', 'the removal of soluble nutrients from the soil by water moving downwards'),
        ('net primary productivity (NPP)', 'the rate at which plants produce new organic matter, after respiration, per unit area per year'),
        ('mycorrhizae', 'fungi associated with tree roots that help them take up nutrients rapidly from the litter'),
    ],
    'mcq': [
        ('In a tropical rainforest, most nutrients are stored in', 'the biomass', ['the litter', 'the soil', 'the atmosphere'], '[1]'),
        ('The NPP of tropical rainforest is about', '2000-2200 g/m²/yr', ['90 g/m²/yr', '500 g/m²/yr', '10 000 g/m²/yr'], 'The highest of any terrestrial biome. [1]'),
        ('Rainforest soils are infertile mainly because', 'heavy rainfall leaches nutrients and most are held in the vegetation', ['they are frozen', 'they have too much organic matter', 'there is no weathering'], '[1]'),
        ('Buttress roots help rainforest trees by', 'supporting tall trees in shallow soils', ['storing water for the dry season', 'resisting fire', 'collecting snow'], '[1]'),
    ],
    'explain': [
        ('Explain the nutrient cycle of the tropical rainforest.', 'Large biomass store; rapid leaf fall all year; small litter store because decomposition is fast in hot, humid conditions; nutrients released quickly and taken up by shallow roots and mycorrhizae; small soil store due to leaching; little loss when undisturbed.', '1 mark per store/transfer [4]'),
        ('Explain the structure of the tropical rainforest.', 'Layers (emergents, canopy, understorey, shrub layer, forest floor) result from competition for light; tall straight trunks, buttress roots, drip-tip leaves, lianas and epiphytes are adaptations.', '1 mark per feature explained [4]'),
        ('Explain why rainforest soils become infertile rapidly after clearance.', 'The nutrient store in biomass is removed; heavy rain leaches remaining nutrients and erodes topsoil; laterite may form on exposure; litter supply stops.', '[3]'),
    ],
    'claims': [
        ('The lush vegetation of rainforests shows that their soils are very fertile.', False, 'Nutrients are held mainly in the biomass; the soils are leached and poor.'),
        ('Decomposition in the rainforest is very rapid.', True, 'Constant heat and moisture allow decomposers to break litter down within weeks.'),
        ('Tropical rainforests have high biodiversity.', True, 'They contain over half of the world’s terrestrial species in about 6% of its land area.'),
    ],
    'essays': [
        ('the tropical rainforest is a fragile ecosystem',
         ['Nutrients held in biomass are lost on clearance; soils leach and erode; species are highly specialised; recovery takes centuries; tipping-point risk in the Amazon.'],
         ['High productivity and rapid regrowth (secondary forest), large genetic diversity and complex food webs give resilience to small disturbances; shifting cultivation was sustainable at low densities.'],
         'Rainforests are resilient to small-scale disturbance but fragile when cleared on a large scale, because of their nutrient cycle and soils.',
         ['nutrient cycling', 'soils', 'biodiversity', 'scale of disturbance']),
    ],
})


@data(t3a)
def t3a_gers(r, D):
    biome = r.choice([('tropical rainforest', (65, 80), (2, 6)), ('savanna grassland', (25, 40), (3, 8)), ('temperate deciduous forest', (35, 50), (10, 20))])
    nm, (b1, b2), (l1, l2) = biome
    B_ = r.randint(b1, b2)
    L_ = r.randint(l1, l2)
    S_ = 100 - B_ - L_
    tot = r.choice([800, 1200, 1500, 2000, 3000])  # kg/ha
    stem = f'In a Gersmehl model for a {nm}, the nutrient stores hold: biomass {B_}%, litter {L_}%, soil {S_}% of a total of {nf(tot)} kg of nutrients per hectare.'
    if D == 1:
        opts, a = mcq(r, f'{nf(round(tot * B_ / 100))} kg/ha', [f'{nf(round(tot * S_ / 100))} kg/ha', f'{nf(round(tot * L_ / 100))} kg/ha', f'{nf(round(tot / B_))} kg/ha', f'{nf(B_ * 10)} kg/ha'])
        return {'stem': stem + ' How many kilograms of nutrients per hectare are in the biomass?', 'options': opts, 'answer': a, 'key': f'{B_}% × {nf(tot)} = {nf(round(tot * B_ / 100))}. [1]'}
    rf = nm == 'tropical rainforest'
    parts = [
        lambda r: ('Calculate the mass of nutrients in each store.', f'biomass {nf(round(tot * B_ / 100))}; litter {nf(round(tot * L_ / 100))}; soil {nf(round(tot * S_ / 100))} kg/ha', '[2]'),
        lambda r: ('Calculate the ratio of the biomass store to the soil store.', f'{dp(B_ / S_, 2)} : 1', f'{B_} ÷ {S_} [1]'),
        lambda r: ('Explain the relative size of the litter store.', ('Very small: rapid decomposition in constant heat and humidity, so litter is broken down within weeks.' if rf else 'Small in savanna because fire and termites remove litter quickly.' if 'savanna' in nm else 'Fairly large: seasonal leaf fall in autumn and slower decomposition in cool winters.'), '[2]'),
        lambda r: ('Explain what would happen to the nutrient stores if the vegetation were cleared and burned.', 'Biomass store removed (some nutrients released as ash, briefly enriching soil); with no canopy, heavy rain leaches and erodes the soil; the litter input stops; the cycle collapses.', '1 mark per point [3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t3b = T('Savanna ecosystem: vegetation, soils and the role of fire', 'savanna ecosystem vegetation soils role of fire')
B(t3b, {
    'terms': [
        ('savanna', 'a tropical grassland with scattered trees and shrubs, in areas with a long dry season'),
        ('pyrophyte', 'a plant adapted to survive or benefit from fire, for example with thick bark or underground storage organs'),
        ('xerophyte', 'a plant adapted to survive drought'),
        ('deciduous (in the dry season)', 'shedding leaves during the dry season to reduce water loss'),
        ('plinthite (laterite)', 'an iron-rich layer in savanna soils that hardens when exposed to repeated wetting and drying'),
        ('fire-climax vegetation', 'vegetation maintained in its present state by repeated burning'),
    ],
    'mcq': [
        ('The baobab tree survives the savanna dry season mainly by', 'storing water in its swollen trunk', ['growing needles', 'staying in leaf all year in deep shade', 'living in water'], '[1]'),
        ('Savanna soils are often red because', 'of iron oxides concentrated by weathering and leaching', ['of high carbon content', 'they are frozen', 'of volcanic ash only'], '[1]'),
        ('Fires in the savanna are most common', 'in the dry season', ['in the wet season', 'only in deserts', 'when the grass is green'], '[1]'),
        ('The Serengeti is a savanna ecosystem in', 'Tanzania', ['Brazil', 'India', 'Australia'], '[1]'),
    ],
    'explain': [
        ('Explain how savanna vegetation is adapted to the climate.', 'Grasses die back in the dry season and regrow from roots; trees are deciduous, have small leathery leaves, thorns, deep tap roots and thick bark; baobabs store water; acacias have umbrella crowns.', '1 mark per adaptation explained [4]'),
        ('Explain the role of fire in the savanna ecosystem.', 'Fire (natural lightning and human burning) removes dead grass and woody seedlings, maintains grassland, releases nutrients as ash, stimulates new growth and germination; fire-resistant species dominate.', '1 mark per point [3]'),
        ('Explain the formation of savanna soils.', 'Seasonal rainfall leaches nutrients in the wet season; upward capillary movement in the dry season; iron oxides accumulate, sometimes forming hard laterite crusts; limited humus because fire and termites remove litter.', '[3]'),
    ],
    'claims': [
        ('Savannas exist only because of climate.', False, 'Fire, grazing and soils also help maintain savannas; some may be fire-climax rather than climatic-climax vegetation.'),
        ('Savanna grasses are adapted to survive fire.', True, 'Their growing points lie at or below ground level, so they regrow after burning.'),
        ('Savannas have the same NPP as rainforests.', False, 'NPP is about 900 g/m²/yr, much lower than rainforest, because of the dry season.'),
    ],
    'essays': [
        ('human activity is more important than climate in maintaining savanna vegetation',
         ['Burning by farmers and pastoralists, grazing and clearance maintain grassland and prevent woodland; fire-climax savannas.'],
         ['The long dry season, rainfall variability, soils (laterite) and natural lightning fires limit tree growth; savannas existed before humans.'],
         'Climate creates the conditions for savanna, but human-set fires and grazing largely determine its present structure.',
         ['fire', 'grazing', 'the dry season', 'soils']),
    ],
})

add_spearman(t3b, [
    {'intro': 'Researchers recorded mean annual rainfall and woody (tree) cover at {n} savanna sites in East Africa.', 'label': 'Site',
     'x': ('mean annual rainfall (mm)', 300, 1200, 0), 'y': ('tree cover (%)', 2, 70, 0), 'sign': 1,
     'why': 'Higher rainfall supports more trees, as water is the main limit on woody growth in savanna; drier sites favour grasses that survive drought by dying back.',
     'limit': 'Fire frequency, grazing and soils also vary between sites; record and control for these, and use more sites from one region.'},
    {'intro': 'A study compared the number of fires in ten years with tree cover at {n} plots in a savanna national park.', 'label': 'Plot',
     'x': ('number of fires in ten years', 0, 9, 0), 'y': ('tree cover (%)', 3, 60, 0), 'sign': -1,
     'why': 'Frequent fires kill woody seedlings and saplings, keeping vegetation as open grassland; fire-resistant grasses regrow quickly.',
     'limit': 'Fire intensity and timing matter as well as frequency; record fire season and intensity, and include plots with similar rainfall.'},
])


t3c = T('Succession and climatic climax in tropical ecosystems', 'succession climatic climax in tropical ecosystems')
B(t3c, {
    'terms': [
        ('succession', 'the sequence of changes in plant communities over time on a site'),
        ('climatic climax community', 'the final, stable plant community in equilibrium with the climate of an area'),
        ('seral stage (sere)', 'one of the stages in a plant succession'),
        ('plagioclimax', 'a plant community prevented from reaching its climatic climax by human activity such as burning or grazing'),
        ('secondary succession', 'succession on land where vegetation has been removed but soil remains, such as abandoned farmland'),
        ('pioneer species', 'the first plants to colonise a bare or disturbed site'),
    ],
    'mcq': [
        ('Vegetation regrowing on abandoned shifting-cultivation plots in the rainforest is an example of', 'secondary succession', ['primary succession on bare rock', 'a climatic climax', 'a plagioclimax caused by grazing'], '[1]'),
        ('A savanna maintained by regular burning is an example of', 'a plagioclimax (fire climax)', ['a primary succession', 'a climatic climax rainforest', 'a sere on sand dunes'], '[1]'),
        ('Primary succession after the 1883 eruption of Krakatau showed that', 'forest re-established on the new volcanic surface within a few decades', ['nothing has grown since', 'only grasses ever grew', 'ice covered the islands'], '[1]'),
        ('Pioneer species in tropical secondary succession are typically', 'fast-growing, light-demanding trees such as Cecropia and Macaranga', ['slow-growing shade-tolerant giants', 'mosses only', 'cacti'], '[1]'),
    ],
    'explain': [
        ('Explain the process of secondary succession in a tropical rainforest clearing.', 'Fast-growing pioneers colonise the gap; they shade the ground and add litter; shade-tolerant species grow beneath and eventually overtop them; biodiversity and biomass increase towards a climax over decades to centuries.', '1 mark per stage [3]'),
        ('Explain why the savanna may be regarded as a plagioclimax.', 'In many areas rainfall could support woodland, but repeated burning and grazing by people prevent trees from establishing.', '[2]'),
        ('Explain why recovered secondary forest differs from primary forest.', 'Lower biodiversity and biomass for many decades; fewer emergents; different species mix dominated by pioneers; soils degraded.', '[3]'),
    ],
    'claims': [
        ('Climatic climax vegetation never changes.', False, 'Climax communities change with climate change and natural disturbances.'),
        ('Human activity can arrest succession.', True, 'Burning, grazing and cultivation create plagioclimax communities.'),
        ('Succession in the humid tropics is faster than in cold climates.', True, 'High temperatures and rainfall support rapid growth.'),
    ],
    'essays': [
        ('the concept of a climatic climax is of limited use in understanding tropical vegetation',
         ['Fire, grazing, shifting cultivation and logging have modified most tropical vegetation; many savannas are plagioclimaxes; climate itself has changed.'],
         ['The idea explains the broad zonal pattern (rainforest to savanna to desert) and the direction of succession on cleared land.'],
         'The concept is a useful model of the potential vegetation, but most tropical vegetation is a product of human and natural disturbance.',
         ['plagioclimax', 'fire', 'succession', 'climate change']),
    ],
})


@data(t3c, c4=False)
def t3c_succ(r, D):
    ages = [0, 5, 10, 20, 40, 80]
    sp = [round(r.uniform(2, 6))]
    for _ in ages[1:]:
        sp.append(sp[-1] + r.randint(8, 30))
    bio = [0]
    for a in ages[1:]:
        bio.append(round(380 * (1 - math.exp(-a / r.uniform(25, 40)))))
    stem = 'Table 3.3 shows tree species richness and above-ground biomass (t/ha) on abandoned farmland of different ages in Costa Rica: ' + '; '.join(f'{a} years: {s} species, {b} t/ha' for a, s, b in zip(ages, sp, bio)) + '. Nearby primary forest has about 400 t/ha.'
    if D == 1:
        opts, a = mcq(r, f'{dp(bio[-1] / 400 * 100)}%', [f'{dp(bio[-1] / 4, 1)}%', f'{dp(100 - bio[-1] / 400 * 100)}%', f'{dp(bio[3] / 400 * 100)}%', f'{dp(min(99, bio[-1] / 400 * 100 + 15))}%'])
        return {'stem': stem + ' What percentage of the primary-forest biomass has been regained after 80 years?', 'options': opts, 'answer': a, 'key': f'{bio[-1]} ÷ 400 × 100 = {dp(bio[-1] / 400 * 100)}%. [1]'}
    parts = [
        lambda r: ('Calculate the mean rate of biomass accumulation in the first 20 years.', f'{dp(bio[3] / 20, 1)} t/ha per year', f'{bio[3]} ÷ 20 [2]'),
        lambda r: ('Calculate the percentage of the primary-forest biomass regained after 80 years.', f'{dp(bio[-1] / 400 * 100)}%', f'{bio[-1]} ÷ 400 × 100 [1]'),
        lambda r: ('Describe and explain the changes in biomass with time.', 'Rapid gain at first as fast-growing pioneers grow in full light, then slower as the canopy closes and growth shifts to slow-growing shade-tolerant species, approaching the climax.', '[3]'),
        lambda r: ('Suggest why species richness may take longer to recover than biomass.', 'Many climax species have heavy seeds dispersed by animals that need nearby forest; specialists require mature conditions.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[3] = [t3a, t3b, t3c]


# ============================================================== CHAPTER 4: Sustainable management of tropical environments

PRODES = [(2004, 27772), (2008, 12911), (2012, 4571), (2016, 7893), (2019, 10129), (2021, 13038), (2022, 11594), (2023, 9001), (2024, 6288)]

t4a = T('Causes and impacts of tropical deforestation and savanna degradation', 'causes impacts of tropical deforestation savanna degradation')
B(t4a, {
    'terms': [
        ('deforestation', 'the permanent removal of forest cover for other land uses'),
        ('cattle ranching', 'large-scale beef production on cleared land, the main driver of Amazon deforestation'),
        ('slash-and-burn', 'clearing vegetation by cutting and burning it, used by both shifting cultivators and commercial farmers'),
        ('land degradation', 'a decline in the productive capacity of land through soil erosion, nutrient loss or vegetation change'),
        ('bush encroachment', 'the spread of woody shrubs into savanna grassland, often after overgrazing and fire suppression'),
        ('tipping point (Amazon)', 'a threshold of deforestation (perhaps 20-25%) beyond which parts of the rainforest could turn into degraded savanna'),
    ],
    'mcq': [
        ('The main direct cause of deforestation in the Brazilian Amazon is', 'clearance for cattle pasture', ['urban growth', 'firewood collection by city dwellers', 'mining for coal'], '[1]'),
        ('In Indonesia and Malaysia, a major cause of rainforest loss has been', 'oil palm plantations', ['tea plantations at high altitude', 'wheat farming', 'reindeer herding'], '[1]'),
        ('Annual deforestation in the Brazilian Amazon fell most sharply between', '2004 and 2012', ['2012 and 2021', '1990 and 1995', '2021 and 2022'], 'From about 27 800 km² to about 4 600 km² (PRODES). [1]'),
        ('Overgrazing in the savanna can lead to', 'loss of grass cover, soil erosion and bush encroachment', ['more dense rainforest', 'increased soil fertility', 'higher rainfall'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of tropical deforestation.', 'Cattle ranching, commercial crops (soya, oil palm), logging, mining (Carajás), road building (BR-163), HEP reservoirs, settlement schemes and population pressure; demand from global markets and government policy.', '1 mark per cause with example [4]'),
        ('Explain the environmental impacts of tropical deforestation.', 'Loss of biodiversity and habitats; soil erosion and leaching; reduced evapotranspiration and rainfall recycling; increased flood peaks and siltation; release of carbon contributing to climate change.', '1 mark per impact [4]'),
        ('Explain the causes of savanna degradation.', 'Overgrazing as herds grow; expansion of cultivation; fuelwood collection; changing fire regimes; drought; sedentarisation of pastoralists.', '[3]'),
    ],
    'claims': [
        ('Deforestation only has local impacts.', False, 'It affects global carbon, regional rainfall and global biodiversity.'),
        ('Indigenous territories in the Amazon have lower deforestation rates than surrounding areas.', True, 'Legally recognised indigenous lands act as barriers to clearance.'),
        ('Deforestation rates in Brazil have been unaffected by government policy.', False, 'Rates fell after enforcement increased in 2004-12, rose when enforcement weakened in 2019-22 and fell again after 2023.'),
    ],
    'essays': [
        ('economic development is the main cause of tropical deforestation',
         ['Commercial agriculture (cattle, soya, oil palm), logging, mining and HEP, driven by global demand and national development plans.'],
         ['Population pressure and poverty (shifting cultivators, fuelwood), weak governance and land speculation, and climate-related fires also drive loss.'],
         'Commercial economic activity is now the dominant driver, enabled by government policy and weak enforcement, with poverty playing a smaller role.',
         ['cattle ranching', 'oil palm', 'governance', 'poverty']),
    ],
})


@data(t4a)
def t4a_prodes(r, D):
    a, b = sorted(r.sample(range(len(PRODES)), 2))
    (y1, v1), (y2, v2) = PRODES[a], PRODES[b]
    pc = pct_change(v1, v2)
    stem = 'Fig. 4.1 shows annual deforestation in the Brazilian Legal Amazon (km², PRODES satellite monitoring): ' + ', '.join(f'{y}: {nf(v)}' for y, v in PRODES) + '.'
    if D == 1:
        opts, ans = mcq(r, f'{sgn(pc)}%', [f'{sgn(-pc)}%', f'{sgn(pc / 2)}%', f'{sgn(v2 / v1 * 100)}%', f'{sgn(pc + 15)}%'])
        return {'stem': stem + f' What was the percentage change between {y1} and {y2}?', 'options': opts, 'answer': ans, 'key': f'({nf(v2)} − {nf(v1)}) ÷ {nf(v1)} × 100 = {sgn(pc)}%. [1]'}
    area = 30  # football pitches: 1 km² ≈ 140 pitches
    parts = [
        lambda r: (f'Calculate the percentage change in annual deforestation between {y1} and {y2}.', f'{sgn(pc)}%', f'({nf(v2)} − {nf(v1)}) ÷ {nf(v1)} × 100 [2]'),
        lambda r: ('Calculate the total area deforested in the years shown.', f'{nf(sum(v for _, v in PRODES))} km²', 'sum [1]'),
        lambda r: ('Suggest reasons for the fall in deforestation between 2004 and 2012.', 'Stronger enforcement by IBAMA using satellite monitoring (DETER); new protected areas and indigenous reserves; soy moratorium (2006); restrictions on credit for illegal clearers; lower commodity prices.', '1 mark per reason [3]'),
        lambda r: ('Suggest reasons for the rise between 2012 and 2021.', 'Weakened environmental enforcement and budgets, changes to the Forest Code (2012), high beef and soya prices, land grabbing and political signals encouraging clearance.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t4b = T('Case study of sustainable management of a tropical environment', 'case study of sustainable management of a tropical environment')
B(t4b, {
    'terms': [
        ('sustainable management', 'using an environment to meet present needs without reducing its ability to meet the needs of future generations'),
        ('extractive reserve', 'a protected area in which local people can harvest products such as rubber and Brazil nuts sustainably'),
        ('REDD+', 'a UN scheme that pays countries to Reduce Emissions from Deforestation and forest Degradation'),
        ('debt-for-nature swap', 'an agreement in which part of a country’s foreign debt is cancelled in return for investment in conservation'),
        ('selective logging', 'felling only certain mature trees and leaving the rest of the forest standing'),
        ('Forest Stewardship Council (FSC)', 'an organisation that certifies timber from responsibly managed forests'),
    ],
    'mcq': [
        ('The Chico Mendes Extractive Reserve is in', 'Acre, Brazil', ['Borneo', 'the Congo basin', 'Costa Rica'], '[1]'),
        ('Which country is often cited for reversing deforestation through payments for ecosystem services since the 1990s?', 'Costa Rica', ['Indonesia', 'Brazil in 2019-21', 'Madagascar'], 'Forest cover rose from about 21% (1987) to over 50%. [1]'),
        ('The Amazon Fund, supported mainly by Norway and Germany, pays for', 'projects that reduce deforestation in Brazil', ['new cattle ranches', 'oil exploration', 'road building'], '[1]'),
        ('Which is a feature of sustainable forest management?', 'Harvesting at rates no faster than regrowth', ['Clear-felling large areas', 'Burning to create pasture', 'Mining in protected areas'], '[1]'),
    ],
    'explain': [
        ('Explain the role of indigenous people in the sustainable management of rainforests.', 'Traditional knowledge, low-impact use (shifting cultivation with long fallows, hunting, gathering), legal land rights that block clearance; e.g. Kayapó territories in Pará.', '[3]'),
        ('Explain the difficulties of achieving sustainable management in tropical environments.', 'Pressure from commercial interests and global demand; poverty; weak enforcement and corruption; land-rights conflicts; cost of monitoring; competing government priorities.', '1 mark per difficulty [4]'),
        ('Explain how certification schemes such as FSC can support sustainable management.', 'Consumers and firms buy certified timber, rewarding producers who log selectively, protect biodiversity and respect local rights; but coverage is small and fraud occurs.', '[3]'),
    ],
    'claims': [
        ('Protecting forests always conflicts with economic development.', False, 'Ecotourism, extractive reserves, carbon payments and agroforestry can provide income.'),
        ('International funding can help reduce deforestation.', True, 'REDD+ and the Amazon Fund pay for monitoring, enforcement and alternative livelihoods.'),
        ('Sustainable management needs the support of local communities.', True, 'Schemes imposed without local benefits are often ignored or resisted.'),
    ],
    'cs': [
        ('the sustainable management of a tropical environment', [
            ('Costa Rica', {'strategy': 'National parks and reserves cover about 25% of the land; Payments for Ecosystem Services (PSA, 1997) funded by a fuel tax pay landowners to protect forest; ecotourism (Monteverde, Corcovado); ban on clearing forest (1996 Forestry Law).',
                            'evaluate': 'Forest cover rose from about 21% in the late 1980s to over 50%; tourism earns several billion US dollars; but some cleared land was low-value pasture anyway, payments are small, and pressures from pineapple and oil palm plantations remain.'}),
            ('the Brazilian Amazon (PPCDAm and the Amazon Fund)', {'strategy': 'Action Plan for Prevention and Control of Deforestation (2004): satellite monitoring (DETER), IBAMA enforcement, new protected areas and indigenous lands; soy moratorium (2006); Amazon Fund (2008) financed by Norway and Germany.',
                                                                  'evaluate': 'Deforestation fell by about 80% from 2004 to 2012; rose again to over 13 000 km² in 2021 when enforcement weakened; fell to about 6300 km² in 2024 after policies were restored; illegal mining and land grabbing persist.'}),
            ('the Danum Valley, Sabah (Malaysian Borneo)', {'strategy': 'Conservation area of primary lowland dipterocarp forest within a larger logging concession; reduced-impact logging trials; research centre; ecotourism lodge; Yayasan Sabah Foundation management.',
                                                             'evaluate': 'Protects biodiversity including orang-utans and provides research data on recovery after logging; but surrounding areas were heavily logged and converted to oil palm; isolated fragments limit wildlife movement.'}),
        ], [
            ('describe the strategies used to manage the environment sustainably', 'strategy', 'Named measures, actors, dates, scale.'),
            ('evaluate the success of the management', 'evaluate', 'Evidence of success and limitations, environmental, economic and social.', 'evaluate the extent to which the tropical environment has been managed sustainably.'),
        ]),
    ],
    'essays': [
        ('sustainable management of tropical environments is only possible with international support',
         ['Funding from the Amazon Fund, REDD+, debt-for-nature swaps and certification markets pays for monitoring and alternative livelihoods.'],
         ['National policies and local action are decisive: Costa Rica’s fuel-tax-funded PES, indigenous land rights, community forestry in Nepal or Mexico; international funding fails without governance.'],
         'International support helps, but strong national governance and local community benefits are the key requirements.',
         ['funding', 'governance', 'indigenous rights', 'markets']),
    ],
})


t4c = T('Conservation, ecotourism and agroforestry strategies', 'conservation ecotourism agroforestry strategies')
B(t4c, {
    'terms': [
        ('ecotourism', 'responsible tourism to natural areas that conserves the environment and benefits local people'),
        ('agroforestry', 'growing trees alongside crops or livestock on the same land, for example shade-grown coffee or alley cropping'),
        ('national park', 'a large protected area where development is restricted to conserve landscape and wildlife'),
        ('biosphere reserve', 'a UNESCO-designated area with a strictly protected core, a buffer zone and a transition zone where people live and work'),
        ('wildlife corridor', 'a strip of habitat linking fragments of forest so that animals can move between them'),
        ('carrying capacity (tourism)', 'the maximum number of visitors an area can support without unacceptable damage'),
    ],
    'mcq': [
        ('A biosphere reserve is divided into', 'a core, a buffer zone and a transition zone', ['three national parks', 'only one strictly protected zone', 'a farm, a town and a forest'], '[1]'),
        ('Shade-grown coffee is an example of', 'agroforestry', ['monoculture plantation', 'clear-felling', 'cattle ranching'], '[1]'),
        ('Which feature is essential for tourism to be described as ecotourism?', 'Local communities benefit and the environment is conserved', ['Large hotels owned by foreign companies', 'High visitor numbers', 'Building new roads into forests'], '[1]'),
        ('Rwanda’s gorilla tourism in Volcanoes National Park charges permit fees of about', 'US$1500 per person', ['US$15', 'US$150 000', 'nothing'], 'Some revenue is shared with local communities. [1]'),
    ],
    'explain': [
        ('Explain the benefits of agroforestry for farmers and the environment.', 'Trees protect soil from erosion, fix nitrogen and add litter; provide fruit, fuel and timber; diversify income; shade crops; store carbon; reduce pressure to clear forest.', '1 mark per benefit [4]'),
        ('Explain how ecotourism can support conservation.', 'Provides income and jobs that depend on intact ecosystems; entry fees fund rangers and research; raises awareness; gives local people an incentive to protect wildlife.', '[3]'),
        ('Explain the limitations of ecotourism.', 'Small scale, so limited income; visitor impacts (trampling, waste, disturbance); flights add carbon; leakage of profits to foreign firms; vulnerable to shocks such as COVID-19.', '1 mark per limitation [3]'),
    ],
    'claims': [
        ('Ecotourism has no environmental impacts.', False, 'Even low-impact tourism causes trampling, waste and disturbance, and long-haul flights emit carbon.'),
        ('Agroforestry can raise farm incomes.', True, 'It provides several products and reduces the risk of crop failure.'),
        ('Strictly protected parks that exclude local people always succeed.', False, 'Excluded communities may resent and ignore protection (“fortress conservation”).'),
    ],
    'essays': [
        ('ecotourism is the most effective strategy for conserving tropical environments',
         ['Ecotourism links income to conservation (Costa Rica, Rwanda gorillas, Danum Valley); fees pay for rangers.'],
         ['Ecotourism is small-scale and vulnerable; legal protection, indigenous land rights, agroforestry, REDD+ payments and enforcement against illegal clearance often have larger effects.'],
         'Ecotourism helps in accessible, scenic areas, but large-scale conservation depends on legal protection and alternative livelihoods across whole landscapes.',
         ['income', 'scale', 'agroforestry', 'legal protection']),
    ],
})


@data(t4c)
def t4c_eco(r, D):
    v = r.choice([5000, 12000, 20000, 40000])
    fee = r.choice([20, 50, 100, 1500 if v <= 5000 else 80])
    spend = r.choice([150, 300, 500])
    leak = r.randint(20, 70)
    plc = r.choice(['a rainforest reserve in Costa Rica', 'a national park in Rwanda', 'a reserve in Sabah, Malaysia', 'a lodge in the Peruvian Amazon', 'a savanna conservancy in Kenya'])
    fees = v * fee
    local = v * spend * (100 - leak) / 100
    stem = f'In one year, {plc} received {nf(v)} visitors. Each paid an entry fee of US${fee} and spent an average of US${spend} on accommodation, food and guides. About {leak}% of this spending leaked out of the local economy.'
    if D == 1:
        opts, a = mcq(r, f'US${nf(int(local))}', [f'US${nf(int(v * spend))}', f'US${nf(int(v * spend * leak / 100))}', f'US${nf(int(fees))}', f'US${nf(int(local / 10))}'])
        return {'stem': stem + ' How much visitor spending stayed in the local economy?', 'options': opts, 'answer': a, 'key': f'{nf(v)} × {spend} × {100 - leak}% = US${nf(int(local))}. [1]'}
    parts = [
        lambda r: ('Calculate the total income from entry fees.', f'US${nf(fees)}', f'{nf(v)} × {fee} [1]'),
        lambda r: ('Calculate the visitor spending retained in the local economy.', f'US${nf(int(local))}', f'{nf(v)} × {spend} × (100 − {leak})% [2]'),
        lambda r: ('Explain why leakage occurs and how it could be reduced.', 'Foreign-owned lodges and tour operators, imported food and goods, and non-local staff send money out of the area; reduce by local ownership, employing and training local guides, buying local produce.', '1 mark cause; 2 marks reduction [3]'),
        lambda r: ('Suggest how the reserve could prevent visitor numbers from damaging the ecosystem.', 'Limit numbers by permit; zoning with trails; trained guides; boardwalks; seasonal closures; monitoring.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[4] = [t4a, t4b, t4c]


# ============================================================== CHAPTER 5: Coastal processes

t5a = T('Waves: formation, wave refraction and constructive and destructive waves', 'waves formation wave refraction constructive destructive waves')
B(t5a, {
    'terms': [
        ('fetch', 'the distance of open water over which the wind blows to generate waves'),
        ('wave refraction', 'the bending of wave crests as they slow down in shallower water, concentrating energy on headlands and spreading it in bays'),
        ('constructive wave', 'a low, long, gently breaking wave with a strong swash and weak backwash that builds up beaches'),
        ('destructive wave', 'a high, steep, frequent wave with a weak swash and strong backwash that removes beach material'),
        ('swash', 'the movement of water up a beach after a wave breaks'),
        ('backwash', 'the return flow of water down a beach under gravity'),
        ('wave period', 'the time in seconds between two successive wave crests passing a fixed point'),
    ],
    'mcq': [
        ('Wave energy is proportional to', 'the square of the wave height', ['the wave period only', 'the square root of the wave height', 'the depth of water'], '[1]'),
        ('As waves approach a headland, energy is concentrated on it because', 'the crests slow and bend in the shallower water off the headland', ['waves speed up in shallow water', 'the fetch is longer at the headland', 'the tide is higher there'], '[1]'),
        ('A wave begins to break when the water depth is about', '1.3 times the wave height', ['ten times the wavelength', 'half the wave period', 'equal to the fetch'], '[1]'),
        ('Destructive waves typically break at a frequency of about', '10-14 per minute', ['1-2 per minute', '6-8 per minute', '40-50 per minute'], '[1]'),
    ],
    'explain': [
        ('Explain how waves are formed.', 'Friction between wind and the sea surface transfers energy, forming ripples that grow into waves; size depends on wind speed, duration and fetch; water particles move in orbits, so energy rather than water travels forward.', '1 mark per point [3]'),
        ('Explain the process of wave refraction and its effect on a coastline of headlands and bays.', 'Waves slow in shallow water off headlands so crests bend to become parallel with the coast; energy converges on headlands (erosion) and diverges in bays (deposition); the coast is gradually straightened.', '1 mark per developed point [4]'),
        ('Compare constructive and destructive waves.', 'Constructive: low height, long wavelength, low frequency (6-8 per minute), spilling breakers, swash stronger than backwash, build berms. Destructive: high, steep, frequent (10-14 per minute), plunging breakers, strong backwash, remove material and steepen then flatten beaches.', '1 mark per comparison [4]'),
    ],
    'claims': [
        ('In deep water, wave motion moves water forward towards the coast.', False, 'Water particles move in near-circular orbits; only the energy moves forward until the wave breaks.'),
        ('A longer fetch can produce larger waves.', True, 'Wind has more distance over which to transfer energy to the water.'),
        ('Destructive waves always make beaches steeper.', False, 'They often comb material offshore, lowering the beach gradient.'),
    ],
    'essays': [
        ('wave energy is the most important factor influencing coastal processes',
         ['Wave height and steepness control erosion by hydraulic action and abrasion, longshore drift and whether beaches build or erode; refraction distributes energy.'],
         ['Geology and rock structure, tidal range, sediment supply, sub-aerial processes, sea-level change and human intervention also control processes and their rates.'],
         'Wave energy drives most marine processes, but its effects depend on geology, sediment supply and tidal range.',
         ['fetch', 'refraction', 'geology', 'tides']),
    ],
})


@data(t5a)
def t5a_wave(r, D):
    w = []
    for nm in ('A', 'B'):
        H = round(r.uniform(0.4, 4.0), 1)
        Tp = r.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        w.append((nm, H, Tp))
    if w[0][1] == w[1][1]:
        return None
    L = [1.56 * t ** 2 for _, _, t in w]
    st = [h / l for (_, h, _), l in zip(w, L)]
    kind = ['destructive' if s > 0.025 else 'constructive' for s in st]
    er = (w[0][1] / w[1][1]) ** 2
    plc = r.choice(['the Holderness coast, England', 'a beach in Cornwall, England', 'the coast of Kerala, India', 'Durban, South Africa', 'the Gold Coast, Australia'])
    stem = (f'Table 5.1 shows measurements of two waves recorded off {plc}. Wave A: height {fmt(w[0][1], 1)} m, period {w[0][2]} s. Wave B: height {fmt(w[1][1], 1)} m, period {w[1][2]} s. '
            'Deep-water wavelength L = 1.56T² (metres, T in seconds). Waves with a steepness (H ÷ L) greater than 0.025 are usually destructive.')
    if D == 1:
        opts, a = mcq(r, f'{dp(L[0], 1)} m', [f'{dp(1.56 * w[0][2], 1)} m', f'{dp(L[0] * 2, 1)} m', f'{dp(L[1], 1)} m' if abs(L[1] - L[0]) > 0.5 else f'{dp(L[0] / 2, 1)} m', f'{dp(w[0][2] ** 2, 1)} m'])
        return {'stem': stem + ' What is the deep-water wavelength of wave A?', 'options': opts, 'answer': a, 'key': f'1.56 × {w[0][2]}² = {dp(L[0], 1)} m. [1]'}
    parts = [
        lambda r: ('Calculate the deep-water wavelength of each wave.', f'A: {dp(L[0], 1)} m; B: {dp(L[1], 1)} m', '1.56 × T² [2]'),
        lambda r: ('Calculate the steepness of each wave and classify it as constructive or destructive.', f'A: {fmt(st[0], 3)} ({kind[0]}); B: {fmt(st[1], 3)} ({kind[1]})', 'H ÷ L; 1 mark values, 1 mark classification [2]'),
        lambda r: ('Wave energy is proportional to H². Calculate how many times more energy wave A has than wave B.', f'{dp(er, 2)} times', f'({fmt(w[0][1], 1)} ÷ {fmt(w[1][1], 1)})² [2]'),
        lambda r: ('Describe the effects of destructive waves on a beach profile.', 'Plunging breakers with a strong backwash drag sediment offshore, forming offshore bars; the beach is lowered and a storm ridge may form at the top; the profile is flattened.', '[3]'),
        lambda r: ('Explain how wave refraction affects the distribution of wave energy along a coast of headlands and bays.', 'Waves slow in shallow water off headlands, bending so that orthogonals converge on the headland and diverge in bays; erosion is concentrated on headlands and deposition occurs in bays.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t5b = T('Marine erosion, transport and deposition; sediment cells', 'marine erosion transport deposition sediment cells')
B(t5b, {
    'terms': [
        ('hydraulic action', 'erosion caused by the force of water and air compressed into cracks in rock by breaking waves'),
        ('abrasion (corrasion)', 'erosion caused by waves hurling sand and pebbles against rock'),
        ('longshore drift', 'the movement of sediment along a coast by swash at an angle and backwash straight down the beach'),
        ('sediment cell', 'a stretch of coast, often bounded by headlands, within which sediment movement is largely self-contained'),
        ('sediment budget', 'the balance between inputs and outputs of sediment in a coastal system'),
        ('flocculation', 'the clumping together of fine clay particles in salt water so that they settle out, forming salt marshes'),
    ],
    'mcq': [
        ('England and Wales are divided into how many major sediment cells for shoreline management?', '11', ['3', '25', '100'], '[1]'),
        ('Deposition is most likely where', 'wave energy is reduced, as in sheltered bays and estuaries', ['waves are steep and frequent', 'the fetch is longest', 'cliffs are highest'], '[1]'),
        ('Attrition is the process in which', 'rock fragments knock against each other and become smaller and rounder', ['seawater dissolves limestone', 'air is compressed in cracks', 'waves throw pebbles at a cliff'], '[1]'),
        ('The main direction of longshore drift is controlled by', 'the direction of the prevailing wind and dominant waves', ['the tidal range', 'the height of the cliffs', 'the rock type of the beach'], '[1]'),
    ],
    'explain': [
        ('Explain the processes of marine erosion.', 'Hydraulic action (compressed air and wave pressure in cracks); abrasion (sediment thrown against rock); attrition; solution/corrosion of limestone and chalk.', '1 mark per process explained [4]'),
        ('Explain the concept of a sediment cell.', 'A closed system with sources (cliff erosion, rivers, offshore), transfers (longshore drift) and sinks (beaches, spits, offshore); boundaries at headlands; interference in one part affects others down-drift.', '[3]'),
        ('Explain why groynes at one place can cause erosion further along the coast.', 'They trap sediment moving by longshore drift; less sediment reaches down-drift beaches, which become narrower and offer less protection, so cliffs behind erode faster (e.g. Mappleton, Holderness).', '[3]'),
    ],
    'claims': [
        ('Sediment cells are completely closed systems.', False, 'Fine sediment and material in storms can move between cells.'),
        ('Most beach sediment on some coasts comes from rivers.', True, 'Rivers supply much sediment on many coasts, though dams can reduce this supply.'),
        ('Saltation is a method of transport in which particles bounce along the bed.', True, 'Medium-sized particles are lifted and dropped repeatedly.'),
    ],
    'essays': [
        ('the sediment cell is the most useful concept for understanding coastal processes',
         ['It links erosion, transport and deposition as one system with inputs, stores and outputs, explains down-drift effects and underpins shoreline management plans.'],
         ['Boundaries are leaky; it says little about rates of erosion of particular cliffs, which depend on geology, wave energy and sub-aerial processes; sea-level change alters cells.'],
         'The concept is a powerful framework, especially for management, but must be combined with an understanding of local processes.',
         ['systems', 'longshore drift', 'shoreline management', 'geology']),
    ],
})


@data(t5b)
def t5b_budget(r, D):
    ins = [('cliff erosion', r.randint(150, 900)), ('rivers', r.randint(20, 300)), ('longshore drift into the cell', r.randint(50, 400))]
    outs = [('longshore drift out of the cell', r.randint(150, 700)), ('offshore transport', r.randint(50, 400)), ('dredging and extraction', r.randint(0, 120))]
    ti, to = sum(v for _, v in ins), sum(v for _, v in outs)
    net = ti - to
    if net == 0:
        return None
    plc = r.choice(['the Holderness coast', 'a coast in East Anglia', 'the Sussex coast', 'a bay in New South Wales', 'the coast of Ghana near Keta'])
    stem = (f'Table 5.2 shows a sediment budget (thousand m³ per year) for {plc}. Inputs: ' + ', '.join(f'{n} {v}' for n, v in ins) +
            '. Outputs: ' + ', '.join(f'{n} {v}' for n, v in outs) + '.')
    pcl = ins[0][1] / ti * 100
    state = 'a surplus, so beaches are likely to accrete' if net > 0 else 'a deficit, so beaches are likely to narrow and erosion to increase'
    if D == 1:
        opts, a = mcq(r, f'{sgn(net, 0)} thousand m³', [f'{sgn(-net, 0)} thousand m³', f'{ti + to} thousand m³', f'{ti} thousand m³', f'{to} thousand m³'])
        return {'stem': stem + ' What is the net sediment budget?', 'options': opts, 'answer': a, 'key': f'{ti} − {to} = {sgn(net, 0)} thousand m³ per year. [1]'}
    parts = [
        lambda r: ('Calculate the net sediment budget and state whether it is a surplus or a deficit.', f'{sgn(net, 0)} thousand m³ per year: {state}.', f'{ti} − {to}; 1 mark value, 1 mark interpretation [2]'),
        lambda r: ('Calculate the percentage of inputs supplied by cliff erosion.', f'{dp(pcl)}%', f'{ins[0][1]} ÷ {ti} × 100 [1]'),
        lambda r: ('Suggest the likely effect on the budget of protecting the cliffs with a sea wall.', f'Inputs fall by up to {ins[0][1]} thousand m³, so the budget would become {sgn(net - ins[0][1], 0)} thousand m³ per year; beaches down-drift would be starved of sediment.', '[2]'),
        lambda r: ('Explain how sediment is transported along the coast.', 'Longshore drift: swash moves material up the beach at the angle of approach of the waves, backwash returns it at right angles under gravity, giving a zigzag movement; also traction, saltation, suspension and solution.', '[3]'),
        lambda r: ('Explain why the sediment budget may vary from year to year.', 'Storm frequency changes cliff erosion and offshore losses; river floods vary supply; wind direction changes drift; human dredging and defences.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t5c = T('Sub-aerial processes and sea-level change', 'sub-aerial processes sea-level change')
B(t5c, {
    'terms': [
        ('sub-aerial processes', 'weathering and mass movement acting on the land surface of a coast, above the reach of the sea'),
        ('eustatic change', 'a global change in sea level caused by a change in the volume of water in the oceans'),
        ('isostatic change', 'a local change in the level of the land relative to the sea, for example rebound after ice sheets melt'),
        ('rotational slumping', 'a mass movement in which saturated material slides along a curved slip plane'),
        ('thermal expansion', 'the increase in volume of seawater as it warms, a major cause of present sea-level rise'),
        ('glacio-isostatic rebound', 'the slow rise of land that was depressed by the weight of ice sheets'),
    ],
    'mcq': [
        ('Melting of land ice and thermal expansion produce', 'a eustatic rise in sea level', ['an isostatic rise of the land', 'a fall in sea level', 'no change in sea level'], '[1]'),
        ('During the last glacial maximum, about 20 000 years ago, global sea level was about', '120 m lower than today', ['10 m higher than today', 'the same as today', '1000 m lower than today'], '[1]'),
        ('Global mean sea level is currently rising at about', '3-4 mm per year', ['3-4 cm per day', '30-40 cm per year', 'nothing at all'], 'Satellite altimetry since 1993. [1]'),
        ('Which sub-aerial process is most important on clay cliffs such as at Holderness?', 'slumping after saturation by rain', ['freeze-thaw only', 'salt weathering', 'abrasion'], '[1]'),
    ],
    'explain': [
        ('Explain how sub-aerial processes contribute to cliff retreat.', 'Weathering (freeze-thaw, wetting and drying, biological, solution) weakens rock; rainfall saturates clays, raising pore pressure and causing slumps, slides and falls; the debris is removed by waves, exposing fresh rock.', '1 mark per point [4]'),
        ('Explain the difference between eustatic and isostatic sea-level change.', 'Eustatic change is global, caused by changes in ocean water volume (ice melting and growth, thermal expansion); isostatic change is local, caused by vertical movement of the land (loading by ice, sediment, rebound).', '[3]'),
        ('Explain why parts of Scotland are rising while south-east England is sinking.', 'Scotland is still rebounding after the removal of the ice sheet; south-east England, beyond the ice margin, is subsiding as the crust readjusts (a see-saw effect), as well as compaction of sediments.', '[3]'),
    ],
    'claims': [
        ('Sea level rise is the same everywhere on Earth.', False, 'Relative sea-level change varies with land movement, ocean currents and gravity effects.'),
        ('Cliffs of weak rock can retreat by over a metre a year.', True, 'Holderness boulder clay cliffs retreat at about 1.8 m a year on average.'),
        ('Sub-aerial processes are unimportant where waves are powerful.', False, 'Waves remove debris, but weathering and mass movement still supply much of the material and shape cliff profiles.'),
    ],
    'essays': [
        ('marine processes are more important than sub-aerial processes in the retreat of cliffs',
         ['Waves undercut cliffs by hydraulic action and abrasion and remove debris; without removal, cliffs would stabilise.'],
         ['On weak clay cliffs, rain-induced slumping supplies most retreat; weathering weakens chalk and limestone; relative importance varies with rock type, climate and exposure.'],
         'Marine processes control the long-term rate by removing debris, but sub-aerial processes are often the immediate cause of retreat on weak cliffs.',
         ['geology', 'mass movement', 'wave energy', 'climate']),
    ],
})


@data(t5c)
def t5c_retreat(r, D):
    plc, rate = r.choice([('Holderness, East Yorkshire (boulder clay)', 1.8), ('Happisburgh, Norfolk (glacial sands and clays)', 2.5), ('the chalk cliffs at Birling Gap, East Sussex', 0.7), ('Christchurch Bay, Dorset (sands and clays)', 1.2)])
    yrs = [2000, 2005, 2010, 2015, 2020]
    pos = [0.0]
    for _ in yrs[1:]:
        pos.append(round(pos[-1] + rate * 5 * r.uniform(0.5, 1.6), 1))
    tot = pos[-1]
    mr = tot / 20
    house = round(r.uniform(25, 80))
    left = house - tot
    years_left = left / mr
    stem = (f'Fig. 5.3 shows the total distance the cliff top at {plc} had retreated from its 2000 position: ' + ', '.join(f'{y}: {fmt(p, 1)} m' for y, p in zip(yrs, pos)) +
            f'. A house stood {house} m from the cliff top in 2000.')
    if D == 1:
        opts, a = mcq(r, f'{dp(mr, 2)} m per year', [f'{dp(tot, 1)} m per year', f'{dp(tot / 5, 2)} m per year', f'{dp(mr * 2, 2)} m per year', f'{dp(mr / 2, 2)} m per year'])
        return {'stem': stem + ' What was the mean rate of retreat between 2000 and 2020?', 'options': opts, 'answer': a, 'key': f'{fmt(tot, 1)} ÷ 20 = {dp(mr, 2)} m per year. [1]'}
    inc = [round(b - a, 1) for a, b in zip(pos, pos[1:])]
    big = inc.index(max(inc))
    parts = [
        lambda r: ('Calculate the mean annual rate of cliff retreat between 2000 and 2020.', f'{dp(mr, 2)} m per year', f'{fmt(tot, 1)} ÷ 20 [1]'),
        lambda r: ('Estimate in which year the cliff top will reach the house if the mean rate continues.', f'about {2020 + math.ceil(years_left)}', f'({house} − {fmt(tot, 1)}) ÷ {dp(mr, 2)} = {dp(years_left, 1)} years after 2020 [2]'),
        lambda r: (f'Identify the five-year period with the most retreat and suggest a reason.', f'{yrs[big]}-{yrs[big + 1]} ({fmt(inc[big], 1)} m): possibly more frequent storms, a wet period saturating the cliff, or a narrow beach.', '1 mark period; 1 mark reason [2]'),
        lambda r: ('Explain the role of sub-aerial processes in the retreat of these cliffs.', 'Rainfall infiltrates and raises pore-water pressure, causing rotational slumps and mudflows; weathering weakens the cliff face; waves then remove the slumped debris at the cliff foot.', '[3]'),
        lambda r: ('Suggest why the rate of retreat may increase in future.', 'Rising sea level and more intense storms allow waves to reach the cliff foot more often; wetter winters increase slumping; defences up-drift reduce beach protection.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[5] = [t5a, t5b, t5c]


# ============================================================== CHAPTER 6: Coastal landforms

t6a = T('Cliffs and wave-cut platforms; headlands and bays', 'cliffs wave-cut platforms headlands bays')
B(t6a, {
    'terms': [
        ('wave-cut notch', 'an indentation at the base of a cliff between high and low tide levels, cut by erosion'),
        ('wave-cut (shore) platform', 'a gently sloping rocky surface left at the foot of a retreating cliff'),
        ('discordant coastline', 'a coast where bands of different rock run at right angles to the shore, producing headlands and bays'),
        ('concordant coastline', 'a coast where rock bands run parallel to the shore, as at Lulworth Cove'),
        ('stack', 'an isolated pillar of rock left when the arch above a cave collapses'),
        ('geo', 'a narrow inlet formed by erosion along a fault or joint in a cliff'),
    ],
    'mcq': [
        ('The correct sequence of landforms produced by erosion of a headland is', 'crack, cave, arch, stack, stump', ['stack, arch, cave, stump', 'cave, stack, arch, crack', 'stump, stack, cave, arch'], '[1]'),
        ('Wave-cut platforms rarely exceed about 500 m in width because', 'waves lose energy crossing a wide platform, so erosion of the cliff slows', ['the tide never reaches them', 'they are covered by ice', 'longshore drift fills them'], '[1]'),
        ('Old Harry Rocks in Dorset are an example of', 'chalk stacks and stumps', ['a granite tor', 'a sand spit', 'a raised beach'], '[1]'),
        ('Cliff profiles are steepest where', 'rock is resistant and strata are horizontal or dip inland', ['rock is soft clay', 'strata dip seawards at a low angle', 'there is a wide beach'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of a wave-cut platform.', 'Waves erode a notch at the cliff base between high and low tide by hydraulic action and abrasion; the overhang collapses; repetition causes the cliff to retreat, leaving a gently sloping platform; debris is removed and abrades the platform.', '1 mark per stage [4]'),
        ('Explain how geology influences the formation of headlands and bays.', 'On discordant coasts less resistant rocks (clays, sands) erode faster to form bays, more resistant rocks (chalk, limestone, granite) remain as headlands; joints and faults are lines of weakness.', '[3]'),
        ('Explain how rock structure influences cliff profiles.', 'Dip of strata: seaward-dipping beds give sloping cliffs prone to slides; landward dip gives steep cliffs; joints and faults allow erosion; alternating hard and soft beds give stepped profiles.', '[3]'),
    ],
    'claims': [
        ('Bays are always formed in softer rock.', False, 'They may also form along faults or joints in a single rock type.'),
        ('Headlands experience more erosion than bays.', True, 'Wave refraction concentrates energy on headlands.'),
        ('Wave-cut platforms can widen indefinitely.', False, 'As they widen, waves lose energy before reaching the cliff, slowing erosion.'),
    ],
    'essays': [
        ('geology is more important than wave energy in explaining the formation of cliffs and headlands',
         ['Lithology and structure (joints, faults, dip) control resistance and profile; discordant coasts form headlands and bays (Swanage, Dorset).'],
         ['Wave energy, fetch and refraction control erosion rates; sub-aerial processes and sea-level change shape profiles; time also matters.'],
         'Geology controls where landforms develop and their form, but waves supply the energy, so both are essential.',
         ['lithology', 'structure', 'refraction', 'sub-aerial processes']),
    ],
})


@data(t6a)
def t6a_platform(r, D):
    W = r.randint(80, 450)
    h = round(r.uniform(2.0, 9.0), 1)
    g = h / W
    ang = math.degrees(math.atan(g))
    rate = round(r.uniform(0.05, 0.6), 2)
    yrs = W / rate
    plc = r.choice(['Kimmeridge Bay, Dorset', 'Southerndown, Glamorgan', 'Flamborough Head, Yorkshire', 'the Kaikoura Peninsula, New Zealand', 'Robin Hood’s Bay, Yorkshire'])
    stem = (f'Fig. 6.1 is a cross-section of the wave-cut platform at {plc}. The platform is {W} m wide from the cliff foot to the low-water mark and falls {fmt(h, 1)} m over this distance. '
            f'The cliff is retreating at about {fmt(rate, 2)} m per year.')
    if D == 1:
        opts, a = mcq(r, f'{dp(ang, 1)}°', [f'{dp(ang * 3, 1)}°', f'{dp(g * 100, 1)}°', f'{dp(90 - ang, 1)}°', f'{dp(ang / 3 + 0.05, 2)}°'])
        return {'stem': stem + ' What is the mean slope angle of the platform?', 'options': opts, 'answer': a, 'key': f'tan⁻¹({fmt(h, 1)} ÷ {W}) = {dp(ang, 1)}°. [1]'}
    parts = [
        lambda r: ('Calculate the mean gradient of the platform as a ratio and as an angle.', f'1 in {round(W / h)}; {dp(ang, 1)}°', f'{fmt(h, 1)} ÷ {W}; tan⁻¹ [2]'),
        lambda r: ('Calculate how long the platform would take to form at the present rate of retreat.', f'about {nf(round(yrs))} years', f'{W} ÷ {fmt(rate, 2)} [2]'),
        lambda r: ('Suggest why the platform may be older than your calculated value.', 'Retreat may have been slower in the past, sea level has changed since the last glacial, and part of the platform may have formed during earlier high sea levels.', '[2]'),
        lambda r: ('Explain the formation of the wave-cut platform.', 'Erosion at the cliff base forms a notch; the cliff above collapses; retreat leaves a gently sloping surface; abrasion by debris and weathering lower the platform.', '[3]'),
        lambda r: ('Explain why the rate of cliff retreat slows as the platform widens.', 'Waves break further out and lose energy crossing the platform, so less energy reaches the cliff foot.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t6b = T('Beaches, spits, bars, tombolos and dunes', 'beaches spits bars tombolos dunes')
B(t6b, {
    'terms': [
        ('spit', 'a long, narrow ridge of sand or shingle attached to the land at one end, formed by longshore drift where the coast changes direction'),
        ('bar', 'a ridge of sediment that extends across a bay or river mouth, enclosing a lagoon'),
        ('tombolo', 'a ridge of sediment that joins an island to the mainland'),
        ('berm', 'a ridge of sand or shingle at the top of a beach formed at the limit of the swash of constructive waves'),
        ('embryo dune', 'a small, newly formed sand dune at the back of a beach, colonised by pioneer plants such as sea couch grass'),
        ('psammosere', 'the plant succession on sand dunes'),
    ],
    'mcq': [
        ('Spurn Head on the Holderness coast is an example of', 'a spit', ['a tombolo', 'a stack', 'a wave-cut platform'], '[1]'),
        ('Chesil Beach in Dorset is often described as', 'a tombolo or barrier beach linking the Isle of Portland to the mainland', ['a cuspate foreland', 'a coral atoll', 'a ria'], '[1]'),
        ('The plant that most helps to stabilise yellow dunes is', 'marram grass', ['heather', 'oak', 'mangrove'], '[1]'),
        ('Shingle beaches are usually steeper than sand beaches because', 'coarse sediment allows the backwash to percolate, so less material is carried back down', ['shingle is lighter', 'waves are larger on shingle', 'sand is coarser'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of a spit.', 'Longshore drift carries sediment along the coast; where the coast changes direction, deposition continues out into the sea in sheltered, deeper water; wind and waves curve the end (recurved tip); a salt marsh forms behind.', '1 mark per stage [4]'),
        ('Explain the development of a sand dune system.', 'Sand dries and is blown landward; it is trapped by obstacles and pioneer plants; embryo dunes grow into yellow dunes stabilised by marram grass; humus accumulates to form grey dunes; dune slacks and climax heath or woodland further inland.', '1 mark per stage [4]'),
        ('Explain the formation of a tombolo.', 'Wave refraction around an island creates a zone of low energy behind it; longshore drift or swash-aligned deposition builds a ridge linking the island to the mainland.', '[3]'),
    ],
    'claims': [
        ('Beach sediment usually becomes finer in the direction of longshore drift.', True, 'Attrition reduces particle size along the drift direction.'),
        ('Spits form only where there is a large tidal range.', False, 'They need a supply of sediment, longshore drift and a change in coastline direction; strong tidal currents can limit their growth.'),
        ('Dunes provide natural coastal defence.', True, 'They absorb wave energy and store sand that replenishes beaches during storms.'),
    ],
    'essays': [
        ('the supply of sediment is the most important factor in the formation of depositional coastal landforms',
         ['Without sediment from cliffs, rivers and offshore, spits, bars and dunes cannot form; dams and defences that cut supply cause erosion (e.g. the Nile delta).'],
         ['Wave energy and direction, longshore drift, coastal shape, tides, wind for dunes, vegetation and sea-level change also control formation.'],
         'Sediment supply is a necessary condition, but the form and location of features depend on processes and coastal configuration.',
         ['longshore drift', 'wave energy', 'vegetation', 'human activity']),
    ],
})

add_spearman(t6b, [
    {'intro': 'Students measured the mean size of 20 pebbles at {n} sites spaced along a shingle beach in the direction of longshore drift.', 'label': 'Site',
     'x': ('distance along the beach (m)', 50, 1500, 0), 'y': ('mean pebble long axis (mm)', 12, 90, 0), 'sign': -1,
     'why': 'Longshore drift carries pebbles along the beach; attrition makes them smaller and rounder with distance, and smaller particles are carried further.',
     'limit': 'Sampling may be biased towards larger pebbles; use random sampling at fixed points, measure at the same tide level and repeat over several days.'},
    {'intro': 'A survey recorded mean sediment size and beach gradient at {n} beaches along one coast.', 'label': 'Beach',
     'x': ('mean sediment size (mm)', 1, 60, 0), 'y': ('beach gradient (degrees)', 2, 25, 0), 'sign': 1,
     'why': 'Coarse sediment is permeable, so backwash percolates and is weak, leaving material at the top of the beach and steepening it.',
     'limit': 'Wave energy and recent storms also affect gradient; survey all beaches in similar conditions and on the same day.'},
])


t6c = T('Landforms of sea-level change: rias, fjords and raised beaches', 'landforms of sea-level change rias fjords raised beaches')
B(t6c, {
    'terms': [
        ('ria', 'a drowned river valley formed when sea level rises, with a winding outline and decreasing depth inland'),
        ('fjord', 'a drowned glacial trough with steep sides, great depth and a shallow threshold at its mouth'),
        ('raised beach', 'a former beach left above present sea level when the land rose or sea level fell'),
        ('relict cliff', 'an old cliff, now inland and above the reach of the sea, behind a raised beach'),
        ('emergent coastline', 'a coast where the land has risen relative to the sea'),
        ('submergent coastline', 'a coast where the sea has risen relative to the land'),
    ],
    'mcq': [
        ('Sognefjord in Norway is an example of', 'a fjord, a drowned glacial trough', ['a ria', 'a raised beach', 'a coral atoll'], '[1]'),
        ('Rias are typical of the coast of', 'south-west England and north-west Spain (Galicia)', ['the Netherlands', 'Holderness', 'the Sahara'], '[1]'),
        ('Raised beaches on the Isle of Arran in Scotland were formed mainly by', 'isostatic rebound after the melting of the ice sheet', ['global sea-level rise', 'coral growth', 'volcanic activity'], '[1]'),
        ('A fjord is deepest', 'inland, with a shallow threshold at the mouth', ['at the mouth', 'evenly along its length', 'only at high tide'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of a ria.', 'River valleys were cut when sea level was lower during glacials; the post-glacial (Flandrian) eustatic rise drowned the lower valleys, producing winding inlets with tributary arms that become shallower inland.', '[3]'),
        ('Compare the characteristics of rias and fjords.', 'Rias: drowned river valleys, V-shaped cross-section, gentle sides, deepest at the mouth. Fjords: drowned glacial troughs, U-shaped, steep sides, very deep with a shallow threshold at the mouth, straighter.', '1 mark per comparison [4]'),
        ('Explain the formation of a raised beach.', 'Beaches and cliffs formed at a former sea level; isostatic uplift after deglaciation (or a fall in sea level) left them above present sea level, where they are no longer affected by waves.', '[3]'),
    ],
    'claims': [
        ('All raised beaches were formed by a fall in global sea level.', False, 'Many, as in Scotland, result from isostatic uplift of the land.'),
        ('Fjords were eroded by rivers and then drowned.', False, 'They were eroded by glaciers below sea level and then flooded.'),
        ('A coastline can show evidence of both emergence and submergence.', True, 'Eustatic and isostatic changes have alternated, as in Scotland.'),
    ],
    'essays': [
        ('isostatic change has had a greater impact than eustatic change on coastal landforms',
         ['In formerly glaciated regions (Scotland, Scandinavia, Canada) rebound produced raised beaches and relict cliffs; isostatic subsidence drowns other coasts.'],
         ['The post-glacial eustatic rise of about 120 m drowned river valleys and glacial troughs worldwide, forming rias, fjords, estuaries and barrier islands, and set the level of present-day processes.'],
         'Eustatic change has had the more widespread effect, but isostatic change dominates locally in formerly glaciated regions.',
         ['rias', 'fjords', 'raised beaches', 'present sea-level rise']),
    ],
})


@data(t6c)
def t6c_raised(r, D):
    plc = r.choice(['the Isle of Arran, Scotland', 'the Isle of Jura, Scotland', 'the Gulf of Bothnia, Sweden', 'Hudson Bay, Canada', 'northern Norway'])
    h = r.randint(5, 40)
    age = r.choice([6, 7, 8, 9, 10])
    s = {6: 3, 7: 6, 8: 12, 9: 20, 10: 30}[age] + r.choice([-1, 0, 1])
    up = h + s
    rate = up / age  # m per thousand years = mm per year
    stem = (f'A raised beach at {plc} lies {h} m above present sea level. Shells in the beach are dated to about {age} thousand years ago, when global (eustatic) sea level was about {s} m lower than today.')
    if D == 1:
        opts, a = mcq(r, f'{dp(rate, 1)} mm per year', [f'{dp(h / age, 1)} mm per year', f'{dp(rate * 2, 1)} mm per year', f'{dp(up / (age * 10), 2)} mm per year', f'{dp(up, 1)} mm per year'])
        return {'stem': stem + ' What was the mean rate of land uplift?', 'options': opts, 'answer': a, 'key': f'Uplift = {h} + {s} = {up} m in {age} thousand years = {dp(rate, 1)} mm per year. [1]'}
    parts = [
        lambda r: ('Calculate the total uplift of the land since the beach formed.', f'{up} m', f'{h} + {s}: the land rose by the beach height plus the eustatic rise [2]'),
        lambda r: ('Calculate the mean rate of uplift in millimetres per year.', f'{dp(rate, 1)} mm per year', f'{up} m ÷ {nf(age * 1000)} years [2]'),
        lambda r: ('Explain why the land has risen.', 'The weight of the ice sheet depressed the crust during the last glacial; after the ice melted, the land has slowly rebounded (glacio-isostatic adjustment).', '[2]'),
        lambda r: ('Describe the landforms associated with the raised beach.', 'A flat terrace of beach deposits backed by a relict cliff, sometimes with caves, arches and stacks now inland and vegetated.', '[2]'),
        lambda r: ('Explain why the coast may now be affected by both emergence and submergence.', 'Isostatic uplift is slowing while eustatic rise from thermal expansion and ice melt is accelerating, so in some areas relative sea level now rises.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[6] = [t6a, t6b, t6c]


# ============================================================== CHAPTER 7: Coral reefs

REEF_SITES = ['Site P', 'Site Q', 'Site R', 'Site S', 'Site T']

t7a = T('Conditions for coral reef growth and reef types', 'conditions for coral reef growth reef types')
B(t7a, {
    'terms': [
        ('coral polyp', 'a small marine animal that secretes a calcium carbonate skeleton; colonies build reefs'),
        ('zooxanthellae', 'single-celled algae living in coral tissue that photosynthesise and supply the coral with food'),
        ('fringing reef', 'a reef growing close to the shore of a landmass, separated from it by a narrow, shallow lagoon or none at all'),
        ('barrier reef', 'a reef separated from the mainland by a wide, deep lagoon, such as the Great Barrier Reef'),
        ('atoll', 'a ring-shaped reef enclosing a lagoon, with no central island'),
        ('patch reef', 'a small isolated reef within a lagoon'),
    ],
    'mcq': [
        ('Reef-building corals grow best where water temperatures are about', '23-29 °C', ['5-10 °C', '35-40 °C', '0-5 °C'], '[1]'),
        ('Reef-building corals rarely grow deeper than about 25-30 m because', 'there is not enough light for the zooxanthellae to photosynthesise', ['the water is too warm', 'salinity is too low', 'there are no waves'], '[1]'),
        ('Coral reefs are generally absent near large river mouths because', 'fresh water and sediment reduce salinity and light', ['the water is too clear', 'waves are too small', 'temperatures are too high'], '[1]'),
        ('The Great Barrier Reef is about', '2300 km long', ['23 km long', '230 km long', '23 000 km long'], '[1]'),
    ],
    'explain': [
        ('Explain the conditions needed for coral reef growth.', 'Warm water (above about 18 °C, optimum 23-29 °C); clear, shallow, well-lit water (less than about 25 m); salinity about 32-35‰; low sediment; wave action bringing oxygen and nutrients; a solid base.', '1 mark per condition [4]'),
        ('Explain the relationship between corals and zooxanthellae.', 'Symbiosis: algae photosynthesise and supply up to 90% of the coral’s food and its colour; the coral provides shelter, carbon dioxide and nutrients; stress causes the coral to expel the algae (bleaching).', '[3]'),
        ('Compare fringing and barrier reefs.', 'Fringing reefs grow close to the shore with little or no lagoon; barrier reefs lie further offshore, separated by a wide, deep lagoon; barrier reefs are larger and often older.', '[3]'),
    ],
    'claims': [
        ('Coral reefs are found mainly on the west coasts of continents in the tropics.', False, 'Cold currents and upwelling make tropical west coasts too cool; reefs are mainly on east coasts.'),
        ('Coral reefs support about a quarter of marine species.', True, 'They cover under 1% of the ocean floor but are very biodiverse.'),
        ('Corals obtain all their food by filter-feeding.', False, 'Most food comes from the zooxanthellae.'),
    ],
    'essays': [
        ('temperature is the most important factor controlling the distribution of coral reefs',
         ['Reefs are limited to waters above 18 °C, explaining their tropical distribution and their absence on coasts with cold currents.'],
         ['Light and depth, salinity, sediment from rivers, a suitable base and wave action control local distribution (none at the mouth of the Amazon); sea-level history matters for reef types.'],
         'Temperature sets the broad latitudinal limits, but local distribution depends on light, sediment and salinity.',
         ['light', 'salinity', 'sediment', 'ocean currents']),
    ],
})


@data(t7a)
def t7a_sites(r, D):
    rows = []
    for s in REEF_SITES:
        rows.append((s, r.choice([16, 19, 22, 25, 27, 28, 31, 33]), r.choice([5, 10, 15, 20, 35, 50]), r.choice([25, 30, 34, 35, 36, 40]), r.choice(['clear', 'clear', 'turbid'])))

    def ok(row):
        _, t, d, s, w = row
        return [18 <= t <= 32, d <= 25, 30 <= s <= 38, w == 'clear']
    goods = [row[0] for row in rows if all(ok(row))]
    if len(goods) not in (1, 2):
        return None
    stem = ('Table 7.1 shows conditions at five sites in a tropical sea (water temperature °C, depth m, salinity ‰, water clarity): ' +
            '; '.join(f'{s}: {t} °C, {d} m, {sa}‰, {w}' for s, t, d, sa, w in rows) +
            '. Reef-building corals need 18-32 °C, depth no greater than 25 m, salinity 30-38‰ and clear water.')
    if D == 1:
        if len(goods) != 1:
            return None
        opts, a = mcq(r, goods[0], [s for s in REEF_SITES if s != goods[0]])
        return {'stem': stem + ' At which site could coral reefs grow?', 'options': opts, 'answer': a, 'key': f'Only {goods[0]} meets all four conditions. [1]'}
    fails = '; '.join(f'{row[0]}: ' + ', '.join(n for n, g in zip(['temperature', 'depth', 'salinity', 'clarity'], ok(row)) if not g) for row in rows if not all(ok(row)))
    parts = [
        lambda r: ('Identify the site or sites where coral could grow.', ' and '.join(goods), '[1]'),
        lambda r: ('For each other site, state which condition or conditions are not met.', fails, '[3]'),
        lambda r: ('Calculate the mean water temperature of the five sites.', f'{dp(mean([row[1] for row in rows]), 1)} °C', '[1]'),
        lambda r: ('Explain why turbid water limits coral growth.', 'Suspended sediment reduces light for zooxanthellae photosynthesis and can smother polyps and clog their feeding structures.', '[2]'),
        lambda r: ('Explain why coral reefs are absent from the coast of Peru although it lies in the tropics.', 'The cold Humboldt (Peru) current and upwelling keep water temperatures below the 18 °C limit for much of the year.', '[2]'),
        lambda r: ('Explain why reefs are usually fringing reefs close to recently formed volcanic islands.', 'Coral grows in the shallow, sunlit water around the island; there has not been enough time for subsidence to form a lagoon and a barrier reef.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t7b = T('Theories of atoll formation: Darwin, Daly and Murray', 'theories of atoll formation darwin daly murray')
B(t7b, {
    'terms': [
        ('subsidence theory', 'Darwin’s theory (1842) that fringing reefs around a sinking volcanic island grow upwards to become barrier reefs and then atolls'),
        ('glacial control theory', 'Daly’s theory that reefs grew on platforms planed by waves during low glacial sea levels and grew upwards as sea level rose'),
        ('antecedent platform theory', 'Murray’s theory that reefs grew on submarine platforms built up by sediment to near the surface'),
        ('guyot', 'a flat-topped submarine volcano (seamount) that was eroded at sea level and has since subsided'),
        ('reef accretion', 'the upward growth of a reef as corals and other organisms add calcium carbonate'),
        ('Enewetak drilling', 'boreholes on Enewetak Atoll in 1952 that passed through about 1400 m of reef limestone to volcanic rock, supporting Darwin’s theory'),
    ],
    'mcq': [
        ('Drilling on Enewetak Atoll in 1952 found volcanic rock beneath about', '1400 m of reef limestone', ['14 m of sand', '14 km of granite', 'no limestone at all'], '[1]'),
        ('Darwin’s theory of atoll formation depends on', 'slow subsidence of a volcanic island while coral grows upwards', ['a fall in sea level', 'tectonic uplift', 'coral growing in deep cold water'], '[1]'),
        ('Daly’s glacial control theory links reef growth to', 'the post-glacial rise in sea level', ['volcanic eruptions only', 'river deposition', 'subsidence of continents'], '[1]'),
        ('A modern explanation of the subsidence of volcanic islands in the Pacific is', 'cooling and contraction of the oceanic plate as it moves away from a hotspot or ridge', ['the weight of coral alone', 'erosion by rivers', 'continental drift towards the poles'], '[1]'),
    ],
    'explain': [
        ('Explain Darwin’s subsidence theory of atoll formation.', 'A fringing reef grows around a volcanic island; the island slowly subsides; the coral grows upwards at a similar rate, so the reef becomes separated from the shrinking island by a lagoon (barrier reef); when the island sinks below sea level, a ring-shaped atoll remains.', '1 mark per stage [4]'),
        ('Explain the evidence that supports Darwin’s theory.', 'Boreholes such as Enewetak show thick reef limestone over volcanic basement; shallow-water coral fossils at depth show subsidence; guyots; plate tectonics explains subsidence of cooling oceanic crust.', '[3]'),
        ('Explain how glacial sea-level changes affected atolls.', 'During glacials sea level fell by up to 120 m, exposing reefs to erosion and solution; as sea level rose, corals grew upwards on the eroded platforms; the shape of many present reefs reflects this.', '[3]'),
    ],
    'claims': [
        ('Darwin’s theory was confirmed by drilling more than a century after it was proposed.', True, 'Enewetak boreholes in 1952 reached volcanic rock beneath reef limestone.'),
        ('The three theories of atoll formation are entirely incompatible.', False, 'Subsidence explains the long-term pattern, while glacial sea-level changes explain the present surface forms.'),
        ('Corals can grow upwards faster than most volcanic islands subside.', True, 'Coral grows about 1-10 mm a year; subsidence is usually much slower.'),
    ],
    'essays': [
        ('Darwin’s theory provides a complete explanation of the formation of atolls',
         ['Subsidence of volcanic islands with upward reef growth explains the sequence of fringing reef, barrier reef and atoll; supported by Enewetak drilling and plate tectonics.'],
         ['It does not explain the shape and depth of lagoons or recent features, which reflect glacial sea-level changes (Daly); some reefs grow on antecedent platforms (Murray).'],
         'Darwin’s theory explains the origin of most atolls, but a complete explanation needs glacial sea-level change as well.',
         ['subsidence', 'sea-level change', 'evidence', 'plate tectonics']),
    ],
})


@data(t7b)
def t7b_atoll(r, D):
    d = r.randint(900, 1600)
    age = r.randint(30, 55)
    rate = d / age  # m per Ma = mm per ka
    mmyr = rate / 1000
    g = r.choice([1, 2, 5, 10])
    atl = r.choice(['Enewetak Atoll, Marshall Islands', 'Bikini Atoll, Marshall Islands', 'an atoll in French Polynesia', 'Funafuti Atoll, Tuvalu'])
    stem = (f'A borehole on an atoll similar to {atl} passes through {nf(d)} m of shallow-water reef limestone before reaching volcanic basalt. The oldest reef limestone is about {age} million years old. '
            f'Reef corals can grow upwards at about {g} mm per year.')
    if D == 1:
        opts, a = mcq(r, f'{dp(rate, 1)} m per million years', [f'{dp(rate * 10, 1)} m per million years', f'{dp(d * age, 0)} m per million years', f'{dp(rate / 10, 2)} m per million years', f'{dp(age / d * 1000, 1)} m per million years'])
        return {'stem': stem + ' What was the mean rate of subsidence?', 'options': opts, 'answer': a, 'key': f'{nf(d)} ÷ {age} = {dp(rate, 1)} m per million years. [1]'}
    parts = [
        lambda r: ('Calculate the mean rate of subsidence in metres per million years and in millimetres per year.', f'{dp(rate, 1)} m per million years = {fmt(mmyr, 3)} mm per year', f'{nf(d)} ÷ {age}; ÷ 1000 [2]'),
        lambda r: ('Calculate how many times faster coral can grow than the island subsided.', f'about {nf(round(g / mmyr))} times', f'{g} ÷ {fmt(mmyr, 3)} [2]'),
        lambda r: ('Explain why the borehole evidence supports Darwin’s theory.', 'Shallow-water corals cannot grow at depth, so their presence 1 km down shows the base has subsided while reef growth kept pace; the volcanic base confirms the original island.', '[3]'),
        lambda r: ('Explain why reefs have not always kept up with sea-level change.', 'Rapid post-glacial sea-level rise (up to 10-20 mm a year at times) and cooling or poor conditions slowed growth; some reefs drowned to form guyots.', '[2]'),
        lambda r: ('Outline Daly’s glacial control theory.', 'Low glacial sea levels allowed waves to plane off islands and reefs; as sea level rose after glaciation, corals grew up on the platforms forming atolls and barrier reefs.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t7c = T('Threats to coral reefs and their management', 'threats to coral reefs their management')
B(t7c, {
    'terms': [
        ('coral bleaching', 'the loss of colour when stressed corals expel their zooxanthellae, often caused by high water temperatures'),
        ('ocean acidification', 'the fall in ocean pH as seawater absorbs carbon dioxide, which makes it harder for corals to build skeletons'),
        ('degree heating weeks (DHW)', 'a measure of accumulated heat stress: the sum of weekly temperature excesses of at least 1 °C above the usual summer maximum over 12 weeks'),
        ('crown-of-thorns starfish', 'a coral-eating starfish whose outbreaks, linked to nutrient run-off, damage reefs such as the Great Barrier Reef'),
        ('marine protected area (MPA)', 'an area of sea where human activities such as fishing are restricted to conserve ecosystems'),
        ('blast fishing', 'using explosives to kill fish, which destroys coral structures'),
    ],
    'mcq': [
        ('Mass bleaching of the Great Barrier Reef occurred in', '2016, 2017, 2020, 2022 and 2024', ['only in 1950', 'never', 'every year since 1900'], '[1]'),
        ('Significant coral bleaching is likely when degree heating weeks reach about', '4 °C-weeks', ['0.1 °C-weeks', '40 °C-weeks', '400 °C-weeks'], 'Severe bleaching and mortality above about 8. [1]'),
        ('Agricultural run-off threatens coral reefs mainly because', 'nutrients encourage algal growth and crown-of-thorns outbreaks, and sediment reduces light', ['it cools the water', 'it increases salinity', 'it adds oxygen'], '[1]'),
        ('The Great Barrier Reef Marine Park zoning plan (2004) made about what share of the park no-take “green zones”?', 'about one-third', ['about 1%', 'all of it', 'none'], '[1]'),
    ],
    'explain': [
        ('Explain how climate change threatens coral reefs.', 'Higher sea temperatures cause bleaching and mortality; ocean acidification reduces calcification; stronger cyclones damage reefs; sea-level rise may outpace growth in some places.', '1 mark per threat [4]'),
        ('Explain the local human threats to coral reefs.', 'Overfishing and destructive fishing (blast, cyanide); pollution and sediment from farming and deforestation; coastal development and dredging; tourism damage (anchors, trampling); coral mining.', '1 mark per threat [4]'),
        ('Explain how reefs can be managed sustainably.', 'Marine protected areas with zoning; controls on run-off and sewage; fishing limits; mooring buoys and visitor education; coral gardening and restoration; reducing global emissions.', '[3]'),
    ],
    'claims': [
        ('Bleached corals always die.', False, 'Corals can recover if temperatures fall soon enough, but prolonged stress kills them.'),
        ('Marine protected areas can increase fish catches in surrounding waters.', True, 'Protected stocks grow and spill over into fished areas.'),
        ('Local management can fully protect reefs from climate change.', False, 'Global emissions must be reduced; local action only improves resilience.'),
    ],
    'essays': [
        ('global threats are more serious than local threats to coral reefs',
         ['Warming causes repeated mass bleaching (Great Barrier Reef 2016-2024); acidification reduces calcification; these cannot be managed locally.'],
         ['Local threats (overfishing, run-off, coastal development, blast fishing in Indonesia) are severe and immediate in many places and reduce resilience to warming; they can be managed.'],
         'Global warming is the greatest long-term threat, but local pressures determine whether reefs can survive it.',
         ['bleaching', 'acidification', 'pollution', 'management']),
    ],
})


@data(t7c)
def t7c_dhw(r, D):
    mmm = round(r.uniform(27.5, 29.5), 1)
    peak = r.uniform(0.6, 3.0)
    ssts = []
    for i in range(12):
        bump = peak * math.sin(math.pi * (i + 0.5) / 12)
        ssts.append(round(mmm + 0.4 + bump + r.uniform(-0.4, 0.4), 1))
    hs = [round(s - mmm, 1) for s in ssts]
    cnt = [h for h in hs if h >= 1.0]
    dhw = round(sum(cnt), 1)
    lvl = 'severe bleaching and significant mortality likely' if dhw >= 8 else 'significant bleaching likely' if dhw >= 4 else 'possible bleaching / no significant bleaching expected'
    reef = r.choice(['Lizard Island, Great Barrier Reef', 'a reef in the Maldives', 'a reef off Okinawa, Japan', 'a reef in the Florida Keys', 'a reef in Fiji'])
    stem = (f'Table 7.3 shows weekly mean sea-surface temperatures (°C) for 12 summer weeks at {reef}: ' + ', '.join(fmt(s, 1) for s in ssts) +
            f'. The maximum monthly mean (MMM) summer temperature is {fmt(mmm, 1)} °C. A weekly HotSpot = SST − MMM; degree heating weeks (DHW) are the sum of the HotSpots of 1.0 °C or more. '
            'DHW of 4 or more: significant bleaching likely; 8 or more: severe bleaching and mortality likely.')
    if D == 1:
        opts, a = mcq(r, f'{dp(dhw, 1)} °C-weeks', [f'{dp(sum(h for h in hs if h > 0), 1)} °C-weeks' if abs(sum(h for h in hs if h > 0) - dhw) > 0.05 else f'{dp(dhw + 2, 1)} °C-weeks', f'{len(cnt)} °C-weeks' if abs(len(cnt) - dhw) > 0.05 else f'{dp(dhw / 2, 1)} °C-weeks', f'{dp(max(hs), 1)} °C-weeks' if abs(max(hs) - dhw) > 0.05 else f'{dp(dhw * 1.5 + 1, 1)} °C-weeks', f'{dp(dhw + 1, 1)} °C-weeks'])
        return {'stem': stem + ' What is the DHW value?', 'options': opts, 'answer': a, 'key': 'HotSpots ≥ 1.0: ' + (' + '.join(fmt(h, 1) for h in cnt) or 'none') + f' = {dp(dhw, 1)}. [1]'}
    parts = [
        lambda r: ('Calculate the degree heating weeks for this period.', f'{dp(dhw, 1)} °C-weeks', 'HotSpots ≥ 1.0 °C: ' + (' + '.join(fmt(h, 1) for h in cnt) or 'none') + ' [3]'),
        lambda r: ('State the likely effect on the reef.', lvl[0].upper() + lvl[1:] + '.', '[1]'),
        lambda r: ('Explain why high temperatures cause coral bleaching.', 'Heat stress damages the photosynthetic system of the zooxanthellae, which produce toxic compounds; the coral expels them, losing colour and most of its food supply.', '[3]'),
        lambda r: ('Suggest why some bleached reefs recover while others do not.', 'Recovery depends on how long and how severe the heat stress was, the time before the next event, water quality, fishing pressure, the presence of herbivorous fish and larval supply from healthy reefs.', '[3]'),
        lambda r: ('Suggest how managers of the reef could increase its resilience.', 'Reduce nutrient and sediment run-off, control crown-of-thorns starfish, create no-take zones, limit damaging tourism, restore coral with heat-tolerant strains.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[7] = [t7a, t7b, t7c]


# ============================================================== CHAPTER 8: Sustainable development of coasts

t8a = T('Hard and soft engineering of coasts', 'hard soft engineering of coasts')
B(t8a, {
    'terms': [
        ('hard engineering', 'building artificial structures such as sea walls, groynes and rock armour to control natural processes'),
        ('soft engineering', 'working with natural processes, for example beach nourishment, dune stabilisation and managed realignment'),
        ('rock armour (rip-rap)', 'large boulders placed at the foot of a cliff or in front of a sea wall to absorb wave energy'),
        ('beach nourishment', 'adding sand or shingle to a beach to make it wider and higher, so that it absorbs more wave energy'),
        ('managed realignment', 'allowing the coastline to move inland in a controlled way, often creating new salt marsh'),
        ('recurved sea wall', 'a concrete wall with a curved face that reflects wave energy back out to sea'),
    ],
    'mcq': [
        ('Which strategy is an example of soft engineering?', 'beach nourishment', ['a recurved sea wall', 'rock groynes', 'a revetment'], '[1]'),
        ('The Sand Engine (Zandmotor) in the Netherlands, built in 2011, is', 'a large artificial sand peninsula that waves and currents spread along the coast', ['a sea wall', 'a tidal barrage', 'a set of concrete groynes'], 'About 21.5 million m³ of sand. [1]'),
        ('A disadvantage of sea walls is that', 'reflected waves scour the beach in front of them', ['they are cheap', 'they encourage salt marshes', 'they increase sediment supply'], '[1]'),
        ('Groynes work by', 'trapping sediment carried by longshore drift', ['reflecting waves', 'absorbing tides', 'stopping rain from reaching cliffs'], '[1]'),
    ],
    'explain': [
        ('Compare the advantages and disadvantages of hard and soft engineering.', 'Hard: effective, long-lasting protection of high-value land, but expensive, unattractive, disrupt sediment and shift erosion down-drift. Soft: cheaper, natural, create habitats and adapt to change, but need regular maintenance and may lose land.', '1 mark per developed comparison [4]'),
        ('Explain how beach nourishment protects a coastline.', 'A wider, higher beach absorbs wave energy before it reaches the cliffs or sea wall; it also supplies sediment to down-drift beaches; but sediment is lost and must be replaced every few years.', '[3]'),
        ('Explain why managed realignment is increasingly used.', 'Rising sea level and the cost of maintaining defences; the salt marsh created absorbs wave energy and provides habitat; cheaper long-term than holding the line (e.g. Medmerry, 2013).', '[3]'),
    ],
    'claims': [
        ('Hard engineering always solves erosion problems.', False, 'It often moves the problem down-drift and can fail in severe storms.'),
        ('Salt marshes reduce wave energy.', True, 'Vegetation and shallow water dissipate wave energy before it reaches defences.'),
        ('Soft engineering never involves construction.', False, 'Nourishment, dune fencing and new embankments in realignment schemes all involve construction.'),
    ],
    'essays': [
        ('soft engineering is the most sustainable approach to coastal management',
         ['It works with natural processes, adapts to sea-level rise, creates habitats and is cheaper in the long term (Medmerry, Sand Engine).'],
         ['Hard engineering is needed to protect high-value assets and dense populations (Malé seawall, Dutch Delta Works); soft schemes need repeated maintenance and may sacrifice land and homes.'],
         'Soft engineering is more sustainable where land values are low, but a mix of approaches is needed on developed coasts.',
         ['cost', 'environment', 'land values', 'sea-level rise']),
    ],
})

DEFS = [('recurved sea wall', 6000, 15000, 50), ('rock armour', 1500, 4000, 30), ('timber groynes', 800, 2000, 20), ('beach nourishment', 400, 1500, 8), ('managed realignment', 300, 900, 100)]


@data(t8a)
def t8a_cost(r, D):
    opts_ = r.sample(DEFS, 4)
    L = r.choice([500, 800, 1200, 2000])
    rows = [(n, round(r.uniform(lo, hi), -2), life) for n, lo, hi, life in opts_]
    ann = [(n, c / life) for n, c, life in rows]
    cheap = min(ann, key=lambda x: x[1])
    val = r.choice([20, 40, 80, 150])  # £ million property protected
    plc = r.choice(['a coastal town in Norfolk', 'a resort in Lincolnshire', 'a village in West Sussex', 'a town on the Holderness coast'])
    stem = (f'Table 8.1 shows options for protecting a {L} m stretch of coast at {plc}. Cost per metre (£) and expected lifespan (years): ' +
            '; '.join(f'{n}: £{nf(int(c))} per m, {life} years' for n, c, life in rows) + f'. Property and infrastructure worth about £{val} million is at risk.')
    if D == 1:
        o, a = mcq(r, cap(cheap[0]), [cap(n) for n, _ in ann if n != cheap[0]])
        return {'stem': stem + ' Which option has the lowest cost per metre per year of lifespan?', 'options': o, 'answer': a, 'key': '; '.join(f'{n} £{dp(v, 0)}' for n, v in ann) + ' per m per year. [1]'}
    cmap = {n: c for n, c, _ in rows}
    parts = [
        lambda r: ('Calculate the annual cost per metre of each option over its lifespan.', '; '.join(f'{n}: £{dp(v, 0)}' for n, v in ann), 'cost ÷ lifespan [2]'),
        lambda r: (f'Calculate the total cost of the cheapest option over its lifespan for the {L} m stretch.', f'£{nf(int(cmap[cheap[0]] * L))}', f'cost per metre × {L} [1]'),
        lambda r: (f'Calculate the benefit-cost ratio of {_bcr(rows, L, val)[0]} for the whole stretch, taking the benefit as the value of property at risk.', _bcr(rows, L, val)[1], 'benefit ÷ total cost [2]'),
        lambda r: ('Suggest why the option with the lowest annual cost may not be chosen.', 'It may not give enough protection for the value at risk; it may lose land or homes; local opposition; environmental designations; maintenance needs; effects down-drift.', '[3]'),
        lambda r: ('Evaluate the use of hard engineering on this stretch of coast.', 'Effective and long-lasting where property values are high, but costly, starves down-drift beaches of sediment and reflects wave energy causing beach scour; a mixed approach may be best.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


def _bcr(rows, L, val):
    pick = [x for x in rows if x[0] == 'rock armour'] or [max(rows, key=lambda x: x[1])]
    n, c, _ = pick[0]
    cost = c * L / 1e6
    return n, f'Cost £{dp(cost, 2)} million; benefit-cost ratio {val} ÷ {dp(cost, 2)} = {dp(val / cost, 1)}'


t8b = T('Integrated coastal zone and shoreline management plans', 'integrated coastal zone shoreline management plans')
B(t8b, {
    'terms': [
        ('integrated coastal zone management (ICZM)', 'managing the whole coastal zone, land and sea, in a coordinated way that involves all stakeholders and considers environmental, economic and social needs'),
        ('shoreline management plan (SMP)', 'a plan for a sediment cell or sub-cell that sets a management policy for each stretch of coast in England and Wales'),
        ('hold the line', 'an SMP policy of maintaining the existing position of the shoreline by defences'),
        ('no active intervention', 'an SMP policy of not investing in defences and allowing natural processes to continue'),
        ('advance the line', 'an SMP policy of building new defences seaward of the existing shoreline'),
        ('stakeholder', 'a person or group with an interest in how an area is managed'),
    ],
    'mcq': [
        ('The four SMP policy options are hold the line, advance the line, managed realignment and', 'no active intervention', ['build more groynes', 'compulsory purchase', 'beach nourishment'], '[1]'),
        ('Shoreline management plans in England and Wales are based on', 'sediment cells and sub-cells', ['county boundaries', 'parliamentary constituencies', 'river basins only'], '[1]'),
        ('A key principle of ICZM is', 'involving all stakeholders and managing land and sea together', ['protecting only tourist beaches', 'building defences everywhere', 'ignoring natural processes'], '[1]'),
        ('Happisburgh in Norfolk is an example of a place where the policy is', 'managed realignment / no active intervention, so homes have been lost', ['advance the line', 'hold the line with a new sea wall', 'land reclamation'], '[1]'),
    ],
    'explain': [
        ('Explain why coastal management should be integrated.', 'Coastal processes link places within a sediment cell, so defences in one place affect others; many stakeholders compete for coastal resources; land and sea issues interact; long-term planning for sea-level rise is needed.', '[4]'),
        ('Explain why there are conflicts over shoreline management decisions.', 'Residents and businesses want protection; government must balance cost against benefit; conservation groups want natural processes; down-drift communities lose sediment; insurers and farmers have different interests.', '[3]'),
        ('Explain how a shoreline management plan decides between policies.', 'Cost-benefit analysis of the value at risk, environmental impact assessment, technical feasibility, effects on adjacent stretches, consultation with stakeholders, over 20, 50 and 100 year epochs.', '[3]'),
    ],
    'claims': [
        ('Every stretch of coast in England is defended.', False, 'Many stretches are assigned no active intervention or managed realignment.'),
        ('Shoreline management plans consider time scales of up to 100 years.', True, 'Policies are set for epochs of 0-20, 20-50 and 50-100 years.'),
        ('ICZM is only about engineering.', False, 'It includes planning, conservation, economic and social policies across the coastal zone.'),
    ],
    'essays': [
        ('integrated coastal zone management is easier to plan than to achieve',
         ['ICZM principles are widely adopted (EU recommendation 2002, SMPs) and give a logical, cell-based, long-term framework.'],
         ['Conflicts between stakeholders, limited funding, compensation problems for people whose homes are not protected, political pressure and different administrative boundaries hinder implementation.'],
         'The concept is sound, but funding, conflicting interests and political pressure make full integration hard to achieve.',
         ['stakeholders', 'funding', 'sediment cells', 'sea-level rise']),
    ],
})


@data(t8b)
def t8b_matrix(r, D):
    pols = ['hold the line', 'managed realignment', 'no active intervention']
    crit = [('protection of property', r.choice([3, 2])), ('cost', r.choice([1, 2])), ('environment', r.choice([1, 2, 3])), ('effect on down-drift coasts', r.choice([1, 2]))]
    sc = {'hold the line': [5, r.choice([1, 2]), r.choice([1, 2]), r.choice([1, 2])],
          'managed realignment': [r.choice([2, 3]), r.choice([3, 4]), r.choice([4, 5]), r.choice([3, 4])],
          'no active intervention': [1, 5, r.choice([3, 4, 5]), 5]}
    tots = {p: sum(s * w for s, (_, w) in zip(sc[p], crit)) for p in pols}
    best = max(tots, key=tots.get)
    if sorted(tots.values())[-1] == sorted(tots.values())[-2]:
        return None
    stem = ('Table 8.2 shows scores (1 = poor, 5 = good) for three shoreline management policies at a stretch of eroding coast, with a weighting for each criterion. ' +
            ' '.join(f'{cap(c)} (weight {w}): ' + ', '.join(f'{p} {sc[p][i]}' for p in pols) + '.' for i, (c, w) in enumerate(crit)))
    if D == 1:
        o, a = mcq(r, cap(best), [cap(p) for p in pols if p != best] + ['Advance the line'])
        return {'stem': stem + ' Which policy has the highest weighted score?', 'options': o, 'answer': a, 'key': '; '.join(f'{p} {tots[p]}' for p in pols) + '. [1]'}
    parts = [
        lambda r: ('Calculate the weighted total score for each policy.', '; '.join(f'{p}: {tots[p]}' for p in pols), 'score × weight, summed [3]'),
        lambda r: ('Identify the policy that should be chosen on this evidence.', cap(best), '[1]'),
        lambda r: ('Suggest why different stakeholders might weight the criteria differently.', 'Homeowners would weight protection of property highly; the Environment Agency and taxpayers weight cost; conservation groups weight the environment; down-drift councils weight effects on their coast.', '[3]'),
        lambda r: ('Explain why managed realignment may be preferred on coasts backed by farmland.', 'Low-value land does not justify the cost of defences; new salt marsh absorbs wave energy and creates habitat; it adapts to sea-level rise.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t8c = T('Case study of coastal management and sustainability', 'case study of coastal management sustainability')
B(t8c, {
    'terms': [
        ('sustainable coastal management', 'managing a coast to protect people and the economy while maintaining natural processes and ecosystems for the future'),
        ('Medmerry managed realignment', 'a 2013 scheme in West Sussex that breached a shingle bank and created 183 ha of intertidal habitat behind new inland embankments'),
        ('Sand Engine (Zandmotor)', 'a mega-nourishment of about 21.5 million m³ of sand placed off the Dutch coast in 2011 to be spread by natural processes'),
        ('Mappleton scheme', 'a 1991 scheme of two rock groynes and rock armour that protected the village of Mappleton on the Holderness coast'),
        ('terminal groyne syndrome', 'increased erosion just down-drift of the last groyne in a scheme, because sediment is trapped up-drift'),
        ('coastal squeeze', 'the loss of intertidal habitat trapped between rising sea level and fixed defences'),
    ],
    'mcq': [
        ('The Mappleton scheme (1991) caused increased erosion', 'south of the groynes, down-drift', ['in the village itself', 'north of Bridlington only', 'nowhere'], 'Cliffs south of Mappleton retreated faster. [1]'),
        ('Medmerry in West Sussex is an example of', 'managed realignment', ['hold the line with a sea wall', 'a tidal barrier', 'a Sand Engine'], '[1]'),
        ('The Maldives capital Malé is protected by', 'a sea wall around the island, built with Japanese aid', ['managed realignment', 'mangrove planting only', 'nothing'], '[1]'),
        ('The Sand Engine aims to protect the Dutch coast for about', '20 years', ['2 years', '200 years', '2000 years'], '[1]'),
    ],
    'explain': [
        ('Explain why the Holderness coast is difficult to manage sustainably.', 'Very rapid erosion of soft boulder clay (about 1.8 m a year); defending one place starves down-drift beaches; low-value farmland makes defences hard to justify; gas terminal at Easington and villages need protection.', '[4]'),
        ('Explain why managed realignment at Medmerry is considered sustainable.', 'It protects about 350 homes and roads more cheaply in the long term than maintaining the shingle bank; it creates intertidal habitat, offsetting coastal squeeze; it works with natural processes.', '[3]'),
        ('Explain the advantages of a mega-nourishment such as the Sand Engine.', 'One large placement disturbs the ecosystem less often than repeated nourishments; natural processes spread the sand along the coast; it creates recreational space and dunes; it adapts to sea-level rise.', '[3]'),
    ],
    'claims': [
        ('The Mappleton scheme had no negative effects.', False, 'It increased erosion down-drift at Great Cowden.'),
        ('Managed realignment can create valuable habitats.', True, 'Medmerry created intertidal mudflats and salt marsh used by birds.'),
        ('Small island states can easily afford hard engineering everywhere.', False, 'The Maldives has over 1000 islands; defences around all of them are unaffordable.'),
    ],
    'cs': [
        ('the management of a stretch of coastline', [
            ('the Holderness coast, England', {'strategy': 'Hard defences at Hornsea, Withernsea and Mappleton (two rock groynes and rock armour, 1991, about £2 million); rock armour at the Easington gas terminal; elsewhere no active intervention in the SMP; roll-back of caravan parks.',
                                               'evaluate': 'Protected towns and the gas terminal, but terminal groyne syndrome increased erosion down-drift; average retreat about 1.8 m a year continues on undefended stretches; farmers and residents lose land with little compensation.'}),
            ('Medmerry, West Sussex, England', {'strategy': 'Managed realignment completed in 2013 by the Environment Agency: the shingle bank was breached and 7 km of new embankments were built inland, creating 183 ha of intertidal habitat; cost about £28 million.',
                                                'evaluate': 'Protects about 350 homes and the A27 approach; flooding has not recurred; the RSPB reserve supports birds; but farmland was lost and some locals opposed it.'}),
            ('the Sand Engine (Zandmotor), South Holland, Netherlands', {'strategy': 'Mega-nourishment of about 21.5 million m³ of sand placed in 2011 as a hook-shaped peninsula; waves, wind and currents redistribute the sand along about 20 km of coast; cost about €70 million.',
                                                                        'evaluate': 'Sand has spread along the coast and new dunes formed, reducing the need for frequent nourishment; it created recreational and nature space; but it is costly, slower to spread than predicted, and may not be suitable on high-energy or sediment-poor coasts.'}),
        ], [
            ('describe the management strategies used', 'strategy', 'Named schemes, dates, costs and scale.'),
            ('evaluate how sustainable the management has been', 'evaluate', 'Environmental, economic and social outcomes, including effects elsewhere.', 'assess the extent to which the coastal management has been sustainable.'),
        ]),
    ],
    'essays': [
        ('coastal management can never be fully sustainable',
         ['Defences shift problems down-drift, need repeated maintenance and cause coastal squeeze; rising sea level will make many defences unaffordable.'],
         ['Managed realignment (Medmerry), mega-nourishment (Sand Engine) and ICZM work with natural processes and adapt to change; mangrove restoration provides protection and livelihoods.'],
         'Full sustainability is difficult, but approaches that work with natural processes and plan for sea-level rise come closest.',
         ['hard engineering', 'managed realignment', 'sea-level rise', 'stakeholders']),
    ],
})


CHAPTERS[8] = [t8a, t8b, t8c]


# ============================================================== CHAPTER 9: Tectonic hazards

t9a = T('Distribution of earthquakes and volcanoes and the hazards they produce', 'distribution of earthquakes volcanoes hazards they produce')
B(t9a, {
    'terms': [
        ('Pacific Ring of Fire', 'the belt of subduction zones around the Pacific Ocean containing about 75% of the world’s active volcanoes and most large earthquakes'),
        ('subduction zone', 'a convergent boundary where denser oceanic lithosphere sinks beneath another plate'),
        ('Benioff zone', 'the inclined zone of earthquake foci along a subducting plate'),
        ('hotspot', 'a fixed plume of hot mantle material that produces volcanoes within a plate, such as Hawaii'),
        ('focus (hypocentre)', 'the point within the Earth where an earthquake rupture begins'),
        ('epicentre', 'the point on the surface directly above the focus'),
    ],
    'mcq': [
        ('The deepest earthquakes, down to about 700 km, occur at', 'subduction zones', ['mid-ocean ridges', 'hotspots', 'transform faults such as the San Andreas'], '[1]'),
        ('Iceland’s volcanoes are mainly the result of', 'a constructive plate boundary combined with a hotspot', ['subduction', 'a collision boundary', 'a transform fault'], '[1]'),
        ('The 2004 Indian Ocean earthquake (magnitude 9.1) occurred at', 'the subduction zone off Sumatra', ['the Mid-Atlantic Ridge', 'the Himalayas', 'the Hawaiian hotspot'], '[1]'),
        ('Explosive volcanoes are typical of destructive boundaries because', 'magma is viscous and rich in silica and gases', ['magma is runny basalt', 'there is no magma', 'the crust is thin'], '[1]'),
    ],
    'explain': [
        ('Describe the global distribution of earthquakes.', 'Narrow belts along plate boundaries: around the Pacific Ring of Fire, along the Alpine-Himalayan belt, along mid-ocean ridges; shallow at ridges and transform faults, deep at subduction zones; few within plates.', '1 mark per point with example [4]'),
        ('Explain why volcanic eruptions at destructive boundaries are more hazardous than those at constructive boundaries.', 'Andesitic and rhyolitic magma is viscous and gas-rich, so eruptions are explosive with pyroclastic flows, ash and lahars; constructive-boundary basaltic eruptions are effusive with lava flows; destructive boundaries are often densely populated.', '[4]'),
        ('Explain the occurrence of volcanoes away from plate boundaries.', 'Mantle plumes create hotspots under plates; as the plate moves over the fixed hotspot, a chain of volcanoes forms, e.g. the Hawaiian-Emperor chain.', '[3]'),
    ],
    'claims': [
        ('All earthquakes occur at plate boundaries.', False, 'Intraplate earthquakes occur on old faults, e.g. New Madrid (USA) in 1811-12.'),
        ('Collision boundaries such as the Himalayas have many earthquakes but few volcanoes.', True, 'Continental crust is too buoyant to subduct deeply, so little magma forms.'),
        ('Shield volcanoes are typical of subduction zones.', False, 'Shield volcanoes form from runny basalt at hotspots and ridges; composite cones are typical of subduction zones.'),
    ],
    'essays': [
        ('the type of plate boundary is the main factor determining the hazards produced by tectonic activity',
         ['Boundary type controls magma type and eruption style, earthquake depth and magnitude (megathrust earthquakes and tsunamis at subduction zones).'],
         ['Hazard impacts also depend on local geology (liquefaction in Mexico City), population density, building quality, preparedness and secondary hazards; hotspots produce hazards away from boundaries.'],
         'Boundary type explains the nature of the physical hazard, but the effects on people depend on vulnerability.',
         ['subduction', 'magma type', 'vulnerability', 'secondary hazards']),
    ],
})


@data(t9a)
def t9a_dist(r, D):
    cats = ['subduction (destructive) boundaries', 'collision boundaries', 'constructive boundaries', 'transform boundaries', 'intraplate locations']
    base = [r.randint(55, 75), r.randint(8, 18), r.randint(3, 8), r.randint(4, 10), r.randint(1, 4)]
    tot = sum(base)
    pcs = [v / tot * 100 for v in base]
    stem = (f'Table 9.1 classifies the {tot} earthquakes of magnitude 7.0 or more recorded in a period by tectonic setting: ' + ', '.join(f'{c} {v}' for c, v in zip(cats, base)) + '.')
    if D == 1:
        opts, a = mcq(r, f'{dp(pcs[0])}%', [f'{dp(pcs[1])}%', f'{dp(100 - pcs[0])}%', f'{dp(base[0])}%' if abs(base[0] - pcs[0]) > 0.5 else f'{dp(pcs[0] - 10)}%', f'{dp(pcs[0] + pcs[1])}%'])
        return {'stem': stem + ' What percentage occurred at subduction boundaries?', 'options': opts, 'answer': a, 'key': f'{base[0]} ÷ {tot} × 100 = {dp(pcs[0])}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage of earthquakes in each setting.', '; '.join(f'{c} {dp(p)}%' for c, p in zip(cats, pcs)), 'value ÷ total × 100 [2]'),
        lambda r: ('Calculate the angle of the subduction-boundary sector if the data were shown as a pie chart.', f'{dp(pcs[0] * 3.6, 0)}°', f'{dp(pcs[0])} × 3.6 [1]'),
        lambda r: ('Explain why most large earthquakes occur at subduction boundaries.', 'Stress builds where the plates lock along a large, gently dipping fault (megathrust); the rupture area is very large, so the energy released is great; the Benioff zone extends deep.', '[3]'),
        lambda r: ('Explain why earthquakes at constructive boundaries are usually small and shallow.', 'The crust is thin and hot, so it cannot store much strain; faults are short and normal faulting releases stress frequently.', '[2]'),
        lambda r: ('Suggest why intraplate earthquakes can be very damaging even when infrequent.', 'Buildings are not designed for earthquakes, people are unprepared, and old cold crust transmits shaking over large distances.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t9b = T('Earthquake hazards: ground shaking, liquefaction, landslides and tsunamis', 'earthquake hazards ground shaking liquefaction landslides tsunamis')
B(t9b, {
    'terms': [
        ('moment magnitude scale', 'a logarithmic scale of earthquake size based on the energy released; each whole number increase means about 32 times more energy'),
        ('Modified Mercalli Intensity scale', 'a 12-point scale (I-XII) describing the observed effects of an earthquake at a place'),
        ('liquefaction', 'the loss of strength of saturated, loose sediment when shaking makes it behave like a liquid'),
        ('tsunami', 'a series of waves caused by sudden displacement of the sea floor, for example by a submarine earthquake'),
        ('seismic waves (P, S and surface)', 'energy waves from an earthquake: fast primary waves, slower secondary waves and the most damaging surface waves'),
        ('aftershock', 'a smaller earthquake following the main shock as the crust adjusts'),
    ],
    'mcq': [
        ('A magnitude 8 earthquake releases about how much more energy than a magnitude 6?', 'about 1000 times', ['2 times', '20 times', '100 times'], '32 × 32 ≈ 1000. [1]'),
        ('Liquefaction caused severe damage in Christchurch, New Zealand in', '2011', ['1906', '1985', '2023'], '[1]'),
        ('In the open ocean a tsunami travels at about', '700-800 km/h', ['10 km/h', '70 km/h', '7000 km/h'], 'v = √(gd) for d ≈ 4000 m. [1]'),
        ('The 2011 Tōhoku earthquake caused most deaths through', 'the tsunami', ['ground shaking', 'volcanic ash', 'fires only'], '[1]'),
    ],
    'explain': [
        ('Explain how liquefaction occurs and why it is hazardous.', 'Shaking increases pore-water pressure in saturated sands and silts, so grains lose contact and the soil behaves like a liquid; buildings tilt or sink, pipes break, sand boils erupt (Christchurch 2011, Kobe port 1995).', '[3]'),
        ('Explain the formation of a tsunami and why its height increases near the coast.', 'Sudden vertical displacement of the sea floor at a subduction zone displaces the water column; waves spread out with long wavelengths and high speed; in shallow water they slow, wavelength shortens and height increases (shoaling).', '[4]'),
        ('Explain why the impacts of earthquakes of similar magnitude vary.', 'Depth of focus, distance from the epicentre, local geology (soft sediments amplify shaking), building quality, population density, time of day, preparedness and secondary hazards.', '1 mark per factor [4]'),
    ],
    'claims': [
        ('Magnitude and intensity measure the same thing.', False, 'Magnitude measures energy released; intensity measures the effects at a place.'),
        ('Soft sediments can amplify ground shaking.', True, 'Mexico City’s lake-bed clays amplified shaking in 1985.'),
        ('Tsunami waves are tallest in the deep ocean.', False, 'They are low in deep water and grow as they slow in shallow water.'),
    ],
    'essays': [
        ('secondary hazards cause more deaths than primary hazards in earthquakes',
         ['Tsunamis (2004 Indian Ocean, about 230 000 deaths; 2011 Tōhoku), landslides (2008 Sichuan), fires (1923 Kantō) and disease can cause most deaths.'],
         ['Building collapse from ground shaking causes most deaths in many earthquakes (Haiti 2010, Turkey-Syria 2023 with over 50 000 deaths); vulnerability is the key factor.'],
         'It depends on setting: subduction earthquakes near coasts are dominated by tsunamis, but in most earthquakes building collapse from shaking is the main killer.',
         ['tsunami', 'building collapse', 'landslides', 'vulnerability']),
    ],
})


@data(t9b)
def t9b_quake(r, D):
    m1 = round(r.uniform(5.5, 7.0), 1)
    dm = r.choice([1.0, 1.5, 2.0, 2.5])
    m2 = round(m1 + dm, 1)
    amp = 10 ** dm
    en = 10 ** (1.5 * dm)
    d = r.choice([2000, 3000, 4000, 4500])
    v = math.sqrt(9.81 * d)
    vk = v * 3.6
    dist = r.choice([150, 400, 800, 1600, 2500])
    tt = dist / vk * 60
    stem = (f'Two earthquakes occurred in a subduction zone: earthquake X of magnitude {fmt(m1, 1)} and earthquake Y of magnitude {fmt(m2, 1)}. '
            f'Earthquake Y generated a tsunami in water about {nf(d)} m deep. Tsunami speed v = √(gd), where g = 9.81 m/s² and d is the depth in metres. A coastal town lies {nf(dist)} km from the epicentre.')
    if D == 1:
        ef_ = lambda x: f'{nf(round(x))} times'
        opts, a = mcq(r, ef_(en), [ef_(amp), ef_(dm * 32), ef_(en * 10), ef_(10 ** (2 * dm)), ef_(en / 2)])
        return {'stem': stem + ' About how many times more energy did earthquake Y release than earthquake X? (Energy increases by about 10^1.5 for each unit of magnitude.)', 'options': opts, 'answer': a, 'key': f'10^(1.5 × {fmt(dm, 1)}) ≈ {nf(round(en))} times. [1]'}
    parts = [
        lambda r: ('Calculate how many times greater the ground-shaking amplitude of Y was than that of X.', f'{dp(amp, 0)} times', f'10^{fmt(dm, 1)} [1]'),
        lambda r: ('Calculate how many times more energy Y released than X (energy increases by about 10^1.5 per unit of magnitude).', f'about {nf(round(en))} times', f'10^(1.5 × {fmt(dm, 1)}) [2]'),
        lambda r: ('Calculate the speed of the tsunami in km/h and the time it would take to reach the town.', f'{dp(v, 0)} m/s = {dp(vk, 0)} km/h; about {dp(tt, 0)} minutes', f'√(9.81 × {nf(d)}) × 3.6; {nf(dist)} ÷ {dp(vk, 0)} × 60 [3]'),
        lambda r: ('Explain why the tsunami wave height increases as it approaches the coast.', 'In shallower water the wave slows; the energy is compressed into a shorter wavelength, so the height increases (shoaling); bays and estuaries can funnel it further.', '[2]'),
        lambda r: ('Suggest how the town could reduce the risk from future tsunamis.', 'Warning systems with sirens and text alerts; evacuation routes and drills; vertical evacuation buildings; sea walls; land-use zoning; mangrove belts.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t9c = T('Volcanic hazards: lava, pyroclastic flows, lahars and gases', 'volcanic hazards lava pyroclastic flows lahars gases')
VEI = [(1e-5, 0), (1e-3, 1), (1e-2, 2), (1e-1, 3), (1, 4), (10, 5), (100, 6), (1000, 7)]


def vei(v):
    for lim, k in VEI:
        if v < lim:
            return k
    return 8


B(t9c, {
    'terms': [
        ('pyroclastic flow', 'a fast-moving (often over 100 km/h) current of hot gas, ash and rock fragments that flows down a volcano'),
        ('lahar', 'a volcanic mudflow of ash and debris mixed with water from rain, melted snow or a crater lake'),
        ('tephra', 'all fragments of rock and ash ejected into the air by an eruption'),
        ('Volcanic Explosivity Index (VEI)', 'a 0-8 logarithmic scale of eruption size based on the volume of material erupted and the height of the eruption column'),
        ('jökulhlaup', 'a sudden glacial outburst flood caused by a volcanic eruption beneath an ice cap'),
        ('volcanic gases', 'gases such as water vapour, carbon dioxide and sulphur dioxide released from magma'),
    ],
    'mcq': [
        ('The 1985 eruption of Nevado del Ruiz killed about 23 000 people in Armero through', 'a lahar', ['lava flows', 'a tsunami', 'an earthquake'], '[1]'),
        ('The eruption of Mount Pinatubo in 1991 had a VEI of', '6', ['1', '3', '8'], 'About 10 km³ of tephra. [1]'),
        ('In 1986 carbon dioxide released from Lake Nyos in Cameroon killed about', '1700 people', ['17 people', '17 000 people', '170 000 people'], '[1]'),
        ('Pyroclastic flows destroyed St Pierre in Martinique in', '1902', ['1815', '1980', '2010'], 'Mont Pelée; about 28 000 deaths. [1]'),
    ],
    'explain': [
        ('Explain why pyroclastic flows are the most dangerous volcanic hazard.', 'They move at over 100 km/h at temperatures of several hundred °C, so escape is impossible; they burn, bury and asphyxiate everything in their path (St Pierre 1902, Merapi 2010).', '[3]'),
        ('Explain how lahars form and why they can affect places far from the volcano.', 'Ash mixes with water from heavy rain, melted ice or crater lakes; the mudflow follows river valleys at high speed for tens of kilometres, burying towns downstream (Armero, 74 km from Ruiz).', '[3]'),
        ('Explain how the effects of volcanic eruptions can be global.', 'Large eruptions inject sulphur dioxide into the stratosphere, forming aerosols that reflect sunlight and cool global temperatures (Pinatubo cooled the world by about 0.5 °C); ash clouds disrupt aviation (Eyjafjallajökull 2010).', '[3]'),
    ],
    'claims': [
        ('Lava flows usually cause more deaths than pyroclastic flows.', False, 'Lava flows are usually slow enough to escape.'),
        ('Lahars can occur years after an eruption.', True, 'Rain remobilises ash deposits, as around Pinatubo for years after 1991.'),
        ('Each step on the VEI represents about a tenfold increase in erupted volume.', True, 'Above VEI 2 the scale is logarithmic.'),
    ],
    'essays': [
        ('volcanic hazards have greater impacts than earthquake hazards',
         ['Large eruptions affect wide areas and global climate (Tambora 1815, the “year without a summer”); pyroclastic flows and lahars are deadly; ash disrupts aviation.'],
         ['Earthquakes strike without warning and have caused far more deaths in recent decades (Haiti 2010, 2004 tsunami, Turkey-Syria 2023); volcanoes can be monitored and evacuated (Pinatubo 1991).'],
         'Earthquakes usually have greater impacts on people because they are hard to predict, though the largest eruptions can have global effects.',
         ['prediction', 'scale', 'deaths', 'economic impacts']),
    ],
})


@data(t9c)
def t9c_vei(r, D):
    vol = r.choice([0.005, 0.02, 0.05, 0.3, 0.6, 2.5, 5, 12, 30])
    k = vei(vol)
    dist = r.randint(20, 80)
    sp = r.choice([20, 30, 40, 50, 60])
    t = dist / sp * 60
    warn = r.choice([30, 45, 60, 90])
    volc = r.choice(['a stratovolcano in the Andes', 'a composite volcano in Indonesia', 'a volcano in the Philippines', 'an ice-capped volcano in Colombia'])
    stem = (f'An eruption of {volc} produced about {fmt(vol, 3) if vol < 0.1 else fmt(vol, 1)} km³ of tephra. VEI classes by tephra volume: VEI 2: 0.001-0.01 km³; VEI 3: 0.01-0.1; VEI 4: 0.1-1; VEI 5: 1-10; VEI 6: 10-100. '
            f'A lahar travelled down a river valley towards a town {dist} km away at an average speed of {sp} km/h. It took {warn} minutes to issue the evacuation warning after the lahar started.')
    if D == 1:
        opts, a = mcq(r, f'VEI {k}', [f'VEI {j}' for j in range(max(0, k - 2), k + 3) if j != k][:4])
        return {'stem': stem + ' What was the VEI of the eruption?', 'options': opts, 'answer': a, 'key': f'{vol} km³ lies in the VEI {k} class. [1]'}
    spare = t - warn
    parts = [
        lambda r: ('State the VEI of the eruption.', f'VEI {k}', '[1]'),
        lambda r: ('Calculate the time taken for the lahar to reach the town and the time left for evacuation after the warning.', f'{dp(t, 0)} minutes; ' + (f'{dp(spare, 0)} minutes to evacuate' if spare > 0 else f'none: the lahar arrives {dp(-spare, 0)} minutes before the warning'), f'{dist} ÷ {sp} × 60 − {warn} [3]'),
        lambda r: ('Explain how lahars form.', 'Volcanic ash and debris mix with water from melted snow and ice, heavy rain or a crater lake to form a dense mudflow that follows valleys.', '[2]'),
        lambda r: ('Explain why so many people died at Armero in 1985.', 'Warnings were ignored or not passed on; hazard maps were not acted upon; the town lay on old lahar deposits in a valley; the lahar arrived at night about two and a half hours after the eruption.', '[3]'),
        lambda r: ('Suggest how the town could be protected from future lahars.', 'Acoustic flow monitors upstream linked to sirens; hazard mapping and relocation; check dams (sabo dams) and channels; evacuation drills.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[9] = [t9a, t9b, t9c]


# ============================================================== CHAPTER 10: Mass movement hazards

t10a = T('Causes of mass movement hazards: slope failure and triggering factors', 'causes of mass movement hazards slope failure triggering factors')
B(t10a, {
    'terms': [
        ('shear stress', 'the force acting to move material downslope, which increases with slope angle and weight'),
        ('shear strength', 'the internal resistance of slope material to movement, from friction and cohesion'),
        ('factor of safety', 'shear strength ÷ shear stress; a slope with a value below 1 is likely to fail'),
        ('pore-water pressure', 'the pressure of water in the spaces between soil particles, which reduces friction and strength'),
        ('rainfall intensity-duration threshold', 'the combination of rainfall intensity and duration above which landslides are likely'),
        ('trigger', 'an event such as heavy rain, an earthquake or excavation that causes an unstable slope to fail'),
    ],
    'mcq': [
        ('Which change increases shear stress on a slope?', 'adding weight to the top of the slope', ['planting trees with deep roots', 'draining the slope', 'reducing the slope angle'], '[1]'),
        ('Heavy rain triggers landslides mainly by', 'raising pore-water pressure and reducing shear strength', ['cooling the slope', 'reducing the weight of soil', 'increasing friction'], '[1]'),
        ('The 2008 Wenchuan (Sichuan) earthquake triggered about', '60 000 landslides', ['6 landslides', '600 landslides', '6 million landslides'], '[1]'),
        ('A slope has a factor of safety of 0.9. This means it is', 'likely to fail', ['completely stable', 'made of rock', 'protected by vegetation'], '[1]'),
    ],
    'explain': [
        ('Explain the factors that increase the likelihood of slope failure.', 'Steep slopes; weak, weathered or jointed rock; bedding dipping parallel to the slope; saturation and high pore pressure; removal of vegetation; undercutting by rivers, waves or road cuts; loading by buildings; earthquake shaking.', '1 mark per factor [4]'),
        ('Explain how deforestation increases landslide risk.', 'Roots that bind soil decay; interception and transpiration fall, so more water reaches and stays in the soil, raising pore pressure.', '[3]'),
        ('Explain why earthquakes trigger landslides.', 'Shaking adds a horizontal force (increasing shear stress) and can cause liquefaction or fracturing that reduces shear strength.', '[2]'),
    ],
    'claims': [
        ('Landslides are always caused by a single trigger.', False, 'Slopes become progressively weaker; a trigger causes failure of an already unstable slope.'),
        ('Human activity can make slopes less stable.', True, 'Road cuts, quarrying, loading, deforestation and leaking pipes increase instability.'),
        ('A longer storm can trigger landslides at a lower rainfall intensity.', True, 'Intensity-duration thresholds fall as duration increases.'),
    ],
    'essays': [
        ('human activity is now the main cause of mass movement hazards',
         ['Deforestation, road building, quarrying, slope loading and informal settlements on steep slopes increase failures (Rio de Janeiro favelas, Hong Kong before 1977, Freetown 2017).'],
         ['Natural factors (steep slopes, weak rocks, monsoon rain, earthquakes like Wenchuan 2008 or Nepal 2015) cause most landslides; humans mainly increase exposure.'],
         'Natural factors are the underlying causes, but human activity increasingly triggers failures and, above all, puts people at risk.',
         ['deforestation', 'urbanisation', 'rainfall', 'earthquakes']),
    ],
})


@data(t10a)
def t10a_thresh(r, D):
    storms = []
    for nm in ('A', 'B', 'C', 'D'):
        dur = r.choice([1, 2, 3, 6, 12, 24, 48])
        thr = 14.82 * dur ** -0.39
        I = round(thr * r.choice([0.4, 0.6, 0.8, 1.3, 1.6, 2.2]), 1)
        storms.append((nm, dur, I, thr))
    above = [s for s in storms if s[2] > s[3]]
    if not above or len(above) == 4:
        return None
    tot = [round(s[1] * s[2]) for s in storms]
    stem = ('Table 10.1 shows four rainstorms on a hillside in Nepal (duration in hours, mean intensity in mm/h): ' + '; '.join(f'storm {n}: {d} h, {fmt(I, 1)} mm/h' for n, d, I, _ in storms) +
            '. A global threshold for shallow landslides is I = 14.82 D^−0.39, where I is intensity (mm/h) and D is duration (h).')
    if D == 1:
        if len(above) != 1:
            return None
        o, a = mcq(r, f'Storm {above[0][0]}', [f'Storm {s[0]}' for s in storms if s is not above[0]])
        return {'stem': stem + ' Which storm exceeded the landslide threshold?', 'options': o, 'answer': a, 'key': '; '.join(f'{n}: threshold {dp(t, 1)} mm/h' for n, _, _, t in storms) + '. [1]'}
    parts = [
        lambda r: ('Calculate the threshold intensity for each storm and identify those likely to trigger landslides.', '; '.join(f'{n}: {dp(t, 1)} mm/h' for n, _, _, t in storms) + '. Above threshold: ' + ', '.join(s[0] for s in above), '14.82 × D^−0.39 [3]'),
        lambda r: ('Calculate the total rainfall in each storm.', '; '.join(f'{s[0]}: {v} mm' for s, v in zip(storms, tot)), 'duration × intensity [1]'),
        lambda r: ('Explain why the threshold intensity falls as storm duration increases.', 'Long storms progressively saturate the soil and raise the water table, so a lower intensity is enough to raise pore-water pressure to the point of failure.', '[2]'),
        lambda r: ('Suggest why local thresholds may differ from the global threshold.', 'Differences in slope angle, soil depth and permeability, vegetation, antecedent moisture and human modification of slopes.', '[2]'),
        lambda r: ('Explain how such thresholds could be used in a warning system.', 'Real-time rain gauges and forecasts are compared with the threshold; when it is approached, warnings are issued and people on vulnerable slopes evacuated.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t10b = T('Landslides, avalanches and mudflows: impacts on people', 'landslides avalanches mudflows impacts on people')
B(t10b, {
    'terms': [
        ('landslide', 'the rapid movement of a mass of rock or soil down a slope along a slip plane'),
        ('mudflow', 'a rapid flow of saturated fine material, often channelled along valleys'),
        ('snow avalanche', 'a rapid flow of snow down a slope, triggered by overloading, warming or disturbance'),
        ('debris flow', 'a fast-moving mixture of water, mud, rock and vegetation'),
        ('rockfall', 'the free fall of rock fragments from a steep cliff or slope, often after freeze-thaw'),
        ('landslide density', 'the number or area of landslides per square kilometre'),
    ],
    'mcq': [
        ('The 2017 landslide in Regent, Freetown, Sierra Leone killed over', '1000 people', ['10 people', '100 people', '100 000 people'], '[1]'),
        ('Snow avalanches are most likely on slopes of about', '30-45°', ['0-5°', '5-15°', '80-90°'], '[1]'),
        ('The 1999 Vargas tragedy in Venezuela was mainly caused by', 'debris flows after extreme rainfall', ['an avalanche', 'a volcanic eruption', 'a tsunami'], '[1]'),
        ('In the Alps, snow avalanches pose most risk to', 'ski resorts, roads and villages in valleys', ['coastal ports', 'deserts', 'coral reefs'], '[1]'),
    ],
    'explain': [
        ('Explain the impacts of landslides on people in LICs.', 'Deaths and injuries; destruction of homes in informal settlements on steep slopes; blocked roads and rivers (landslide dams); loss of farmland; disruption of water supplies; long recovery.', '[4]'),
        ('Explain why snow avalanches occur.', 'Heavy new snow on a weak layer; slopes of 30-45°; warming or rain weakens the pack; wind loading; disturbance by skiers or vibration.', '[3]'),
        ('Explain why the impacts of mass movements are increasing.', 'Urban growth on steep slopes; deforestation; road building in mountains; heavier rainfall linked to climate change; more tourism in mountains.', '[3]'),
    ],
    'claims': [
        ('Landslides only affect rural mountain areas.', False, 'Cities on steep slopes such as Rio de Janeiro, Hong Kong and Freetown are affected.'),
        ('Landslides can cause floods.', True, 'Landslide dams block rivers and may burst.'),
        ('Avalanches occur only in winter.', False, 'Wet-snow avalanches are common in spring.'),
    ],
    'essays': [
        ('the impacts of mass movements depend more on human factors than on the type of movement',
         ['Vulnerability (poverty, informal housing on slopes, lack of warning, weak planning) explains high deaths in Freetown 2017 and Vargas 1999.'],
         ['Fast movements such as debris flows, rock avalanches (Huascarán 1970) and mudflows kill far more than slow creep or slumps whatever the human situation.'],
         'The type of movement sets the potential impact, but human vulnerability and exposure determine the actual losses.',
         ['speed', 'vulnerability', 'planning', 'warning']),
    ],
})


@data(t10b)
def t10b_density(r, D):
    cls = ['0-10°', '10-20°', '20-30°', '30-40°', 'over 40°']
    area = [r.randint(20, 60), r.randint(25, 60), r.randint(15, 45), r.randint(8, 25), r.randint(2, 10)]
    dens_t = [0.1, 0.6, 1.8, 3.2, r.choice([2.0, 2.8, 4.5])]
    n = [max(0, round(a * d * r.uniform(0.7, 1.3))) for a, d in zip(area, dens_t)]
    dens = [x / a for x, a in zip(n, area)]
    top = cls[dens.index(max(dens))]
    if sorted(dens)[-1] == sorted(dens)[-2]:
        return None
    reg = r.choice(['a district in the Darjeeling Himalaya, India', 'a hillside district in Kerala, India', 'a catchment in the Rwenzori Mountains, Uganda', 'a district near Freetown, Sierra Leone'])
    stem = ('Table 10.2 shows the area (km²) of each slope class and the number of landslides recorded after a monsoon season in ' + reg + ': ' +
            '; '.join(f'{c}: {a} km², {x} landslides' for c, a, x in zip(cls, area, n)) + '.')
    if D == 1:
        o, a = mcq(r, top, [c for c in cls if c != top])
        return {'stem': stem + ' Which slope class had the highest landslide density?', 'options': o, 'answer': a, 'key': '; '.join(f'{c} {dp(d, 2)}' for c, d in zip(cls, dens)) + ' per km². [1]'}
    parts = [
        lambda r: ('Calculate the landslide density (landslides per km²) for each slope class.', '; '.join(f'{c}: {dp(d, 2)}' for c, d in zip(cls, dens)), 'number ÷ area [3]'),
        lambda r: ('Calculate the percentage of all landslides that occurred on slopes over 30°.', f'{dp((n[3] + n[4]) / sum(n) * 100)}%', f'({n[3]} + {n[4]}) ÷ {sum(n)} × 100 [2]'),
        lambda r: ('Describe the relationship between slope angle and landslide density.', 'Density increases with slope angle' + (', though it falls on the steepest slopes, where soil is thin or bare rock dominates.' if dens[4] < dens[3] else ', with the highest density on the steepest slopes.'), '[2]'),
        lambda r: ('Suggest why the number of landslides alone is a poor measure of hazard.', 'It ignores the size of the area of each class, landslide size and speed, and the number of people and buildings exposed.', '[2]'),
        lambda r: ('Explain the impacts of the landslides on people in the district.', 'Deaths and injuries, destroyed houses and tea gardens or farms, blocked roads cutting off villages, damaged water pipes and power lines, loss of income and costs of clearance.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t10c = T('Reducing mass movement risk: monitoring, stabilisation and planning', 'reducing mass movement risk monitoring stabilisation planning')
B(t10c, {
    'terms': [
        ('inclinometer', 'an instrument in a borehole that measures slope movement at depth'),
        ('extensometer', 'an instrument that measures the widening of cracks or the distance between points on a slope'),
        ('soil nailing', 'inserting steel bars into a slope and grouting them to hold the soil together'),
        ('retaining wall', 'a wall built to hold back soil or rock on a slope'),
        ('slope drainage', 'pipes or channels that remove water from a slope to reduce pore-water pressure'),
        ('hazard zoning', 'mapping areas by level of risk and restricting development in the most dangerous zones'),
    ],
    'mcq': [
        ('Hong Kong set up the Geotechnical Control Office in 1977 after', 'a series of deadly landslides in 1972 and 1976', ['an earthquake in 1977', 'a typhoon in 2018', 'a volcanic eruption'], '[1]'),
        ('Which method stabilises a slope by reducing pore-water pressure?', 'drainage pipes', ['adding a building on top', 'removing vegetation', 'cutting the base'], '[1]'),
        ('Avalanche defences in the Alps include', 'snow fences, deflecting dams and controlled explosions', ['groynes', 'sabo dams only', 'sea walls'], '[1]'),
        ('Satellite radar (InSAR) is used in landslide management to', 'detect millimetre-scale ground movement over large areas', ['measure rainfall', 'grow vegetation', 'stop earthquakes'], '[1]'),
    ],
    'explain': [
        ('Explain how engineering can reduce landslide risk.', 'Regrading to reduce slope angle; retaining walls and soil nails increase strength; drainage reduces pore pressure; rock bolts and netting stop rockfalls; vegetation binds soil.', '1 mark per method [4]'),
        ('Explain how monitoring can reduce the impact of landslides.', 'Rain gauges, inclinometers, extensometers, GPS and InSAR detect accelerating movement or threshold rainfall, allowing warnings and evacuation before failure.', '[3]'),
        ('Explain why planning may be more effective than engineering in LICs.', 'Engineering is expensive; hazard mapping and land-use zoning that keep people off dangerous slopes are cheaper; community warning schemes; but enforcement in informal settlements is difficult.', '[3]'),
    ],
    'claims': [
        ('Engineering can remove landslide risk completely.', False, 'It reduces risk but extreme events can still cause failures.'),
        ('Hong Kong’s slope safety programme reduced landslide deaths.', True, 'Deaths fell sharply after systematic slope registration and upgrading.'),
        ('Planting vegetation can help stabilise slopes.', True, 'Roots bind soil and plants remove water by transpiration.'),
    ],
    'essays': [
        ('monitoring and warning are more effective than stabilisation in reducing mass movement risk',
         ['Monitoring (inclinometers, InSAR, rain thresholds) gives warnings over large areas cheaply and saves lives.'],
         ['Stabilisation (Hong Kong’s slope upgrading, drainage, retaining walls) reduces the hazard itself and protects property; warnings are useless without evacuation plans; planning keeps people away from danger.'],
         'A combined approach is best: stabilise high-risk slopes in cities, monitor and warn over wider areas, and use planning to reduce exposure.',
         ['cost', 'scale', 'planning', 'Hong Kong']),
    ],
})


@data(t10c)
def t10c_monitor(r, D):
    days = [0, 7, 14, 21, 28, 35]
    rates = sorted([round(r.uniform(0.2, 1.5), 1) for _ in range(5)])
    if r.random() < 0.3:
        r.shuffle(rates)
    pos = [0.0]
    for v in rates:
        pos.append(round(pos[-1] + v * 7, 1))
    last = rates[-1]
    first = rates[0]
    thr = r.choice([1.0, 1.2, 1.5])
    plc = r.choice(['a slope above a road in Hong Kong', 'a landslide above a village in the Swiss Alps', 'a hillside in Wellington, New Zealand', 'a cut slope on a highway in Malaysia'])
    stem = (f'Fig. 10.3 shows the cumulative displacement (mm) recorded by an extensometer on {plc}: ' + ', '.join(f'day {d}: {fmt(p, 1)}' for d, p in zip(days, pos)) +
            f'. Engineers issue an alert when the rate of movement exceeds {fmt(thr, 1)} mm per day.')
    rr = [round((b - a) / 7, 2) for a, b in zip(pos, pos[1:])]
    over = [f'days {days[i]}-{days[i + 1]}' for i, v in enumerate(rr) if v > thr]
    if D == 1:
        mr = pos[-1] / 35
        opts, a = mcq(r, f'{dp(mr, 2)} mm per day', [f'{dp(pos[-1] / 5, 2)} mm per day', f'{dp(pos[-1], 1)} mm per day', f'{dp(mr * 7, 2)} mm per day', f'{dp(mr / 2, 2)} mm per day'])
        return {'stem': stem + ' What was the mean rate of movement over the 35 days?', 'options': opts, 'answer': a, 'key': f'{fmt(pos[-1], 1)} ÷ 35 = {dp(mr, 2)} mm per day. [1]'}
    parts = [
        lambda r: ('Calculate the rate of movement in mm per day for each week.', '; '.join(f'days {days[i]}-{days[i + 1]}: {dp(v, 2)}' for i, v in enumerate(rr)), 'change ÷ 7 [2]'),
        lambda r: ('Identify the periods in which an alert should have been issued.', ', '.join(over) if over else 'None: the rate never exceeded the threshold.', '[1]'),
        lambda r: ('Explain why an increasing rate of movement is a warning sign.', 'Acceleration shows that shear strength is falling relative to stress, often as water pressure rises or a slip surface develops, and may precede rapid failure.', '[2]'),
        lambda r: ('Suggest how the slope could be stabilised.', 'Install drainage to lower pore pressure; build a retaining wall or use soil nails and anchors; regrade to a lower angle; plant vegetation.', '[3]'),
        lambda r: ('Suggest limitations of relying on one extensometer.', 'It measures movement at only one point and at the surface; movement elsewhere or at depth may be missed; instrument failure; data need continuous checking.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[10] = [t10a, t10b, t10c]


# ============================================================== CHAPTER 11: Atmospheric hazards

t11a = T('Tropical cyclones: formation, distribution and hazards', 'tropical cyclones formation distribution hazards')
B(t11a, {
    'terms': [
        ('storm surge', 'a rise in sea level above the normal tide caused by low pressure and strong onshore winds'),
        ('inverse barometer effect', 'the rise of sea level of about 1 cm for each 1 hPa fall in air pressure'),
        ('cyclone track', 'the path followed by the centre of a tropical cyclone'),
        ('landfall', 'the moment when the centre of a cyclone crosses the coast'),
        ('rapid intensification', 'an increase in maximum sustained winds of at least 55 km/h in 24 hours'),
        ('hurricane, typhoon and cyclone', 'regional names for tropical cyclones in the Atlantic and NE Pacific, the NW Pacific, and the Indian Ocean and South Pacific respectively'),
    ],
    'mcq': [
        ('The Atlantic hurricane season officially runs from', '1 June to 30 November', ['1 January to 31 March', '1 April to 31 May', 'all year equally'], '[1]'),
        ('Typhoon Haiyan (2013) caused most deaths in Tacloban through', 'a storm surge of over 5 m', ['an earthquake', 'a drought', 'snow'], '[1]'),
        ('Tropical cyclones in the Northern Hemisphere usually track', 'westwards and then recurve north-eastwards', ['eastwards along the equator', 'directly south', 'only northwards over land'], '[1]'),
        ('A central pressure of 920 hPa would raise sea level by about how much through the inverse barometer effect alone?', '0.9 m', ['9 cm', '9 m', '0.09 cm'], '1013 − 920 = 93 hPa ≈ 93 cm. [1]'),
    ],
    'explain': [
        ('Explain the global distribution of tropical cyclones.', 'Over warm oceans (above 26.5 °C) between about 5° and 20-30° N and S; not at the equator (no Coriolis effect) or in the South Atlantic and SE Pacific (cold water, wind shear); most in the NW Pacific.', '[4]'),
        ('Explain the hazards associated with tropical cyclones.', 'High winds damage buildings and crops; storm surges flood coasts; torrential rain causes river floods and landslides; tornadoes may form; secondary hazards include disease and contamination of water.', '1 mark per hazard [4]'),
        ('Explain why storm surges are particularly dangerous in places such as Bangladesh.', 'The shallow, funnel-shaped Bay of Bengal amplifies surges; the delta is very low-lying and densely populated; many people are poor with weak housing (1970 Bhola, 1991).', '[3]'),
    ],
    'claims': [
        ('All tropical cyclones make landfall.', False, 'Many stay over the ocean and die out over cooler water.'),
        ('Rainfall flooding can cause more damage than wind in a tropical cyclone.', True, 'Hurricane Harvey (2017) dropped over 1500 mm on parts of Texas.'),
        ('Slow-moving cyclones bring less rain to a place.', False, 'Slow movement concentrates rain over one area, increasing flooding.'),
    ],
    'essays': [
        ('storm surge is the most dangerous hazard associated with tropical cyclones',
         ['Surges cause most deaths in low-lying coasts and deltas (Bhola 1970, Nargis 2008, Haiyan 2013, Katrina 2005).'],
         ['Rain-induced flooding and landslides cause most deaths inland and in mountainous islands (Mitch 1998 in Honduras, Harvey 2017); wind destroys buildings and crops.'],
         'Surge is usually the deadliest hazard on low coasts, but the main hazard varies with relief, storm speed and vulnerability.',
         ['coastal relief', 'rainfall', 'wind', 'vulnerability']),
    ],
})


@data(t11a)
def t11a_surge(r, D):
    p = r.randint(905, 985)
    baro = 1013 - p
    wind = round(r.uniform(0.5, 4.5), 1)
    tide = round(r.uniform(0.3, 2.0), 1)
    tot = baro / 100 + wind
    elev = round(r.uniform(1.0, 6.0), 1)
    d6 = round(math.hypot(r.randint(60, 140), r.randint(0, 60)))
    spd = d6 / 6
    coast = r.choice(['the coast of Bangladesh', 'Tacloban, Philippines', 'the Mississippi delta, USA', 'the coast of Odisha, India', 'Beira, Mozambique'])
    stem = (f'A tropical cyclone approaching {coast} has a central pressure of {p} hPa (normal pressure 1013 hPa). Each 1 hPa fall in pressure raises sea level by about 1 cm. '
            f'Onshore winds are forecast to add a further {fmt(wind, 1)} m, and landfall coincides with a high tide {fmt(tide, 1)} m above mean sea level. '
            f'The track shows the centre moved {d6} km in the last 6 hours. Much of the coastal land lies {fmt(elev, 1)} m above mean sea level.')
    if D == 1:
        opts, a = mcq(r, f'{dp(baro / 100, 2)} m', [f'{dp(baro, 0)} m', f'{dp(baro / 10, 1)} m', f'{dp(p / 100, 2)} m', f'{dp(baro / 1000, 3)} m'])
        return {'stem': stem + ' How much would sea level rise from the low pressure alone?', 'options': opts, 'answer': a, 'key': f'(1013 − {p}) × 1 cm = {baro} cm = {dp(baro / 100, 2)} m. [1]'}
    wl = tot + tide
    parts = [
        lambda r: ('Calculate the total storm surge and the expected water level above mean sea level at landfall.', f'surge {dp(tot, 2)} m; water level {dp(wl, 2)} m', f'{baro} cm + {fmt(wind, 1)} m; + {fmt(tide, 1)} m tide [3]'),
        lambda r: ('State whether the coastal land is likely to flood and by how much.', (f'Yes, by about {dp(wl - elev, 2)} m.' if wl > elev else f'No, the water level is {dp(elev - wl, 2)} m below the land surface (but waves may still overtop).'), '[1]'),
        lambda r: ('Calculate the forward speed of the cyclone.', f'{dp(spd, 1)} km/h', f'{d6} ÷ 6 [1]'),
        lambda r: ('Explain why the shape of the coastline affects storm surge height.', 'Shallow, gently sloping continental shelves and funnel-shaped bays concentrate water, so surges are higher (Bay of Bengal); steep, deep coasts have smaller surges.', '[2]'),
        lambda r: ('Suggest how the people of the coast could be protected from the surge.', 'Early warning and evacuation to raised cyclone shelters; embankments and sea walls; mangrove belts; raised houses and land-use zoning.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t11b = T('Tornadoes: formation, distribution and hazards', 'tornadoes formation distribution hazards')
EF = [(105, 137, 0), (138, 177, 1), (178, 217, 2), (218, 266, 3), (267, 322, 4), (323, 500, 5)]


def ef(v):
    for lo, hi, k in EF:
        if lo <= v <= hi:
            return k
    return -1


B(t11b, {
    'terms': [
        ('tornado', 'a violently rotating column of air extending from a thunderstorm cloud to the ground'),
        ('supercell', 'a long-lived thunderstorm with a rotating updraft (mesocyclone) that can produce strong tornadoes'),
        ('Enhanced Fujita (EF) scale', 'a 0-5 scale that rates tornadoes by estimated wind speed from the damage they cause'),
        ('Tornado Alley', 'the area of the central USA (the Great Plains) where tornadoes are most frequent'),
        ('wind shear', 'a change in wind speed or direction with height, which allows storms to rotate'),
        ('mesocyclone', 'a rotating updraft several kilometres wide inside a supercell thunderstorm'),
    ],
    'mcq': [
        ('Tornadoes are most frequent in the central USA because', 'warm moist air from the Gulf of Mexico meets cold dry air from Canada and dry air from the Rockies', ['the area is next to the Pacific', 'it is near the equator', 'there are no mountains anywhere nearby'], '[1]'),
        ('The Joplin, Missouri tornado of 2011 was rated', 'EF5', ['EF0', 'EF1', 'EF2'], 'About 160 deaths. [1]'),
        ('Which country, outside the USA, has the highest tornado deaths per event, largely due to vulnerable housing?', 'Bangladesh', ['Iceland', 'Egypt', 'New Zealand'], 'Daulatpur-Saturia tornado 1989, about 1300 deaths. [1]'),
        ('Tornado path widths are typically', 'tens to hundreds of metres', ['tens of kilometres', 'a few centimetres', 'about 500 km'], '[1]'),
    ],
    'explain': [
        ('Explain how tornadoes form.', 'Warm, moist air at low levels and cold, dry air above give instability; wind shear makes the updraft rotate, forming a mesocyclone in a supercell; downdrafts and stretching concentrate the rotation into a narrow vortex reaching the ground.', '[4]'),
        ('Explain why tornadoes are difficult to predict.', 'They are small and short-lived and form within storms; conditions favourable for tornadoes can be forecast hours ahead, but individual tornadoes are usually detected by Doppler radar only minutes before they strike.', '[3]'),
        ('Compare the hazards of tornadoes and tropical cyclones.', 'Tornadoes have faster winds (over 320 km/h) but narrow paths and short duration; cyclones affect areas hundreds of km wide for days with surge and flooding, so total damage and deaths are usually larger.', '[3]'),
    ],
    'claims': [
        ('Tornadoes only occur in the USA.', False, 'They occur in Bangladesh, Argentina, Europe, South Africa and elsewhere.'),
        ('The EF scale is based on damage.', True, 'Wind speeds are estimated from damage to indicators such as buildings and trees.'),
        ('Mobile homes are particularly vulnerable to tornadoes.', True, 'They are light and poorly anchored.'),
    ],
    'essays': [
        ('tornadoes are a greater hazard to people than tropical cyclones',
         ['Tornadoes have the strongest surface winds, strike with little warning and destroy everything in their path (Joplin 2011, Moore 2013).'],
         ['Tropical cyclones affect much larger areas for longer, with storm surge and floods causing far more deaths and damage (Haiyan, Katrina, Nargis).'],
         'Locally tornadoes are more intense, but tropical cyclones are the greater hazard to people overall.',
         ['wind speed', 'area affected', 'warning time', 'vulnerability']),
    ],
})


@data(t11b)
def t11b_ef(r, D):
    torn = []
    for nm in ('A', 'B', 'C', 'D'):
        v = r.randint(110, 340)
        L = round(r.uniform(2, 40), 1)
        w = r.choice([50, 100, 200, 400, 800, 1200])
        torn.append((nm, v, L, w))
    cats = [ef(v) for _, v, _, _ in torn]
    if len(set(cats)) < 3:
        return None
    areas = [L * w / 1000 for _, _, L, w in torn]
    big = torn[areas.index(max(areas))][0]
    stem = ('Table 11.2 shows estimated peak winds (km/h), path length (km) and mean path width (m) of four tornadoes in Oklahoma: ' +
            '; '.join(f'{n}: {v} km/h, {fmt(L, 1)} km, {w} m' for n, v, L, w in torn) +
            '. EF scale (km/h): EF0 105-137; EF1 138-177; EF2 178-217; EF3 218-266; EF4 267-322; EF5 over 322.')
    if D == 1:
        c = cats[0]
        o, a = mcq(r, f'EF{c}', [f'EF{k}' for k in range(6) if k != c])
        return {'stem': stem + ' What is the EF rating of tornado A?', 'options': o, 'answer': a, 'key': f'{torn[0][1]} km/h lies in EF{c}. [1]'}
    parts = [
        lambda r: ('Classify each tornado on the EF scale.', '; '.join(f'{t[0]}: EF{c}' for t, c in zip(torn, cats)), '[2]'),
        lambda r: ('Calculate the area affected by each tornado (km²) and identify the largest.', '; '.join(f'{t[0]}: {dp(a, 2)} km²' for t, a in zip(torn, areas)) + f'. Largest: {big}', 'length × width ÷ 1000 [3]'),
        lambda r: ('Explain why a tornado with a lower EF rating may cause more deaths than one with a higher rating.', 'It may cross a densely populated area, strike at night with little warning, or hit vulnerable buildings such as mobile homes, while a stronger tornado crosses open farmland.', '[2]'),
        lambda r: ('Explain the conditions that produce tornadoes in the Great Plains in spring.', 'Warm moist air from the Gulf of Mexico at low levels, dry air from the south-west above and cold air from the north create instability; the jet stream provides wind shear; supercells develop along the dry line and cold fronts.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t11c = T('Prediction and impacts of atmospheric hazards on people', 'prediction impacts of atmospheric hazards on people')
B(t11c, {
    'terms': [
        ('forecast cone (cone of uncertainty)', 'the area within which the centre of a tropical cyclone is likely to track, widening with forecast time'),
        ('track forecast error', 'the distance between the forecast and actual position of a cyclone centre'),
        ('Doppler radar', 'radar that detects the motion of raindrops, revealing rotation in storms and giving tornado warnings'),
        ('lead time', 'the time between a warning and the arrival of the hazard'),
        ('numerical weather prediction', 'computer modelling of the atmosphere to forecast weather'),
        ('Cyclone Preparedness Programme (CPP)', 'Bangladesh’s community warning system, with tens of thousands of volunteers who spread warnings and help evacuation'),
    ],
    'mcq': [
        ('The average US tornado warning lead time is about', '10-15 minutes', ['10-15 seconds', '10-15 hours', '10-15 days'], '[1]'),
        ('Tropical cyclone track forecasts have improved mainly because of', 'satellites, better computer models and aircraft observations', ['fewer cyclones', 'weaker winds', 'cooler oceans'], '[1]'),
        ('Deaths from cyclones in Bangladesh have fallen mainly because of', 'early warnings, cyclone shelters and evacuation', ['fewer cyclones', 'emigration', 'cooler seas'], '[1]'),
        ('Hurricane Katrina (2005) caused about how many deaths?', 'about 1800', ['about 18', 'about 18 000', 'about 180 000'], '[1]'),
    ],
    'explain': [
        ('Explain how tropical cyclones are predicted.', 'Satellites track cloud systems; hurricane-hunter aircraft and buoys measure pressure and winds; computer models forecast track and intensity; forecasts are shown as cones of uncertainty with warnings issued 36-48 hours ahead.', '[4]'),
        ('Explain why the impacts of tropical cyclones differ between HICs and LICs.', 'HICs have better forecasts, communications, building codes, evacuation and insurance, so fewer deaths but higher economic losses; LICs have more vulnerable housing, poverty and weak infrastructure, so more deaths (Katrina vs Nargis).', '[4]'),
        ('Explain why forecasts of intensity are less accurate than forecasts of track.', 'Intensity depends on small-scale processes in the eyewall, ocean heat below the surface and wind shear that models represent poorly; rapid intensification is hard to predict.', '[3]'),
    ],
    'claims': [
        ('Accurate prediction always prevents deaths.', False, 'Warnings must reach people, be trusted and acted on, as Katrina and Nargis showed.'),
        ('Economic losses from atmospheric hazards are greatest in HICs.', True, 'Property values are higher, although losses as a share of GDP are often higher in LICs.'),
        ('Tornado forecasts can give several days’ warning of exactly where a tornado will strike.', False, 'Only the risk area can be forecast days ahead; specific warnings come minutes before.'),
    ],
    'essays': [
        ('improvements in prediction have been the main reason for the fall in deaths from tropical cyclones',
         ['Satellites and models reduced track errors and allow evacuation days ahead; Bangladesh warnings in 2007 (Sidr) and 2020 (Amphan) contrasted with 1970.'],
         ['Shelters, education, building codes, evacuation planning, community volunteers and development (better housing, communications) were essential; warnings in Myanmar 2008 failed to reach people.'],
         'Prediction is necessary but not sufficient; falling deaths come from prediction combined with preparedness and reduced vulnerability.',
         ['forecasting', 'shelters', 'education', 'development']),
    ],
})


@data(t11c)
def t11c_errors(r, D):
    hrs = [24, 48, 72]
    e1 = [r.randint(150, 200), r.randint(300, 380), r.randint(450, 560)]
    f = r.uniform(0.3, 0.5)
    e2 = [round(e * f * r.uniform(0.9, 1.1)) for e in e1]
    y1, y2 = r.choice([(1990, 2020), (1995, 2022), (1992, 2023)])
    imp = [pct_change(a, b) for a, b in zip(e1, e2)]
    stem = (f'Table 11.3 shows mean track forecast errors (km) for Atlantic hurricanes at a forecasting centre. {y1}: ' + ', '.join(f'{h} h {e}' for h, e in zip(hrs, e1)) +
            f'. {y2}: ' + ', '.join(f'{h} h {e}' for h, e in zip(hrs, e2)) + '.')
    if D == 1:
        opts, a = mcq(r, f'{sgn(imp[2])}%', [f'{sgn(-imp[2])}%', f'{sgn(imp[0])}%' if abs(imp[0] - imp[2]) > 0.5 else f'{sgn(imp[2] / 2)}%', f'{sgn(e2[2] / e1[2] * 100)}%', f'{sgn(imp[2] + 10)}%'])
        return {'stem': stem + f' What was the percentage change in the 72-hour error between {y1} and {y2}?', 'options': opts, 'answer': a, 'key': f'({e2[2]} − {e1[2]}) ÷ {e1[2]} × 100 = {sgn(imp[2])}%. [1]'}
    parts = [
        lambda r: (f'Calculate the percentage change in forecast error at each lead time between {y1} and {y2}.', '; '.join(f'{h} h: {sgn(p)}%' for h, p in zip(hrs, imp)), '(new − old) ÷ old × 100 [3]'),
        lambda r: (f'Describe how forecast error changes with lead time in {y2}.', f'Error increases with lead time, from {e2[0]} km at 24 h to {e2[2]} km at 72 h, about {dp(e2[2] / e2[0], 1)} times larger.', '[2]'),
        lambda r: ('Explain why forecasts have improved.', 'More and better satellite data, aircraft reconnaissance, faster computers running higher-resolution models, ensemble forecasting and better understanding of steering winds.', '[3]'),
        lambda r: ('Explain why reduced forecast errors save lives and money.', 'Warning areas can be smaller and more accurate, so evacuations are better targeted and trusted, fewer people are evacuated unnecessarily and more time is available to prepare.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[11] = [t11a, t11b, t11c]


# ============================================================== CHAPTER 12: Hazard management

t12a = T('Hazard perception, vulnerability and the hazard risk equation', 'hazard perception vulnerability hazard risk equation')
B(t12a, {
    'terms': [
        ('hazard', 'a natural event that threatens life and property'),
        ('disaster', 'a hazard event that causes serious disruption, loss of life and damage beyond a community’s capacity to cope'),
        ('vulnerability', 'the degree to which people are susceptible to loss from a hazard, depending on social, economic and physical factors'),
        ('capacity', 'the resources and abilities that help people prepare for, cope with and recover from hazards'),
        ('risk equation', 'risk = hazard × vulnerability ÷ capacity'),
        ('hazard perception', 'the way people view the threat from a hazard, influenced by experience, education, culture and wealth'),
    ],
    'mcq': [
        ('According to the risk equation, risk increases when', 'vulnerability increases or capacity to cope falls', ['capacity increases', 'the hazard becomes less frequent', 'people are better prepared'], '[1]'),
        ('Fatalism as a hazard perception means people', 'accept hazards as unavoidable and take little action', ['always move away', 'build sea walls', 'buy insurance'], '[1]'),
        ('The Pressure and Release (PAR) model explains disasters as', 'the result of hazard events meeting vulnerability produced by root causes and unsafe conditions', ['only the result of physical processes', 'random events', 'caused by climate change alone'], '[1]'),
        ('Which factor most reduces vulnerability to earthquakes?', 'enforced building codes', ['higher population density', 'informal housing', 'lack of education'], '[1]'),
    ],
    'explain': [
        ('Explain why poverty increases vulnerability to hazards.', 'Poor people live in hazardous locations and weak housing, lack savings and insurance, have poor access to warnings, health care and transport, and recover slowly.', '[4]'),
        ('Explain the factors that influence hazard perception.', 'Experience of past events; education and awareness; wealth and ability to act; religious and cultural beliefs; media; time since the last event; attachment to place.', '1 mark per factor [4]'),
        ('Explain the risk equation.', 'Risk depends on the magnitude and frequency of the hazard multiplied by people’s vulnerability, divided by their capacity to cope; reducing vulnerability or increasing capacity reduces risk even if the hazard is unchanged.', '[3]'),
    ],
    'claims': [
        ('A hazard in an uninhabited area is still a disaster.', False, 'A disaster requires people or property to be affected.'),
        ('Vulnerability can be reduced by development.', True, 'Better housing, education, health and incomes increase resilience.'),
        ('Everyone in a community is equally vulnerable to a hazard.', False, 'The poor, elderly, disabled, women and children are often more vulnerable.'),
    ],
    'essays': [
        ('vulnerability is more important than the physical hazard in determining the scale of a disaster',
         ['Similar hazards cause very different losses: Haiti 2010 (M7.0, over 200 000 deaths) vs Christchurch 2011 (M6.2, 185 deaths); PAR model.'],
         ['Extreme magnitude events overwhelm even prepared societies (Tōhoku 2011); the type and speed of onset of the hazard matter; some hazards are inherently deadly.'],
         'Vulnerability usually explains differences in losses, though very large events cause disasters even where vulnerability is low.',
         ['PAR model', 'magnitude', 'development', 'governance']),
    ],
})


@data(t12a)
def t12a_risk(r, D):
    places = ['Settlement A', 'Settlement B', 'Settlement C', 'Settlement D']
    rows = [(p, r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)) for p in places]
    risk = [h * v / c for _, h, v, c in rows]
    if len(set(round(x, 2) for x in risk)) < 4:
        return None
    hi = places[risk.index(max(risk))]
    stem = ('Table 12.1 shows scores (1 = low, 10 = high) for hazard, vulnerability and capacity for four settlements on the slopes of a volcano: ' +
            '; '.join(f'{p}: hazard {h}, vulnerability {v}, capacity {c}' for p, h, v, c in rows) + '. Risk = hazard × vulnerability ÷ capacity.')
    if D == 1:
        o, a = mcq(r, hi, [p for p in places if p != hi])
        return {'stem': stem + ' Which settlement has the highest risk?', 'options': o, 'answer': a, 'key': '; '.join(f'{p} {dp(x, 1)}' for p, x in zip(places, risk)) + '. [1]'}
    rk = sorted(zip(places, risk), key=lambda x: -x[1])
    parts = [
        lambda r: ('Calculate the risk score for each settlement and rank them from highest to lowest risk.', ', '.join(f'{p} {dp(x, 1)}' for p, x in rk), 'H × V ÷ C; 1 mark ranking [3]'),
        lambda r: ('Suggest two ways of increasing the capacity score of the highest-risk settlement.', 'Evacuation plans and drills; warning sirens linked to the volcano observatory; trained local response teams; access roads; savings and insurance schemes.', '[2]'),
        lambda r: ('Explain why vulnerability may differ between settlements at a similar distance from the volcano.', 'Differences in wealth, housing quality, age structure, education and awareness, access to roads and warnings, and dependence on farming.', '[3]'),
        lambda r: ('Suggest limitations of using scores in the risk equation.', 'Scores are subjective; factors are not independent; they combine very different variables; the hazard varies with eruption type.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t12b = T('Prediction, prevention, preparedness and response strategies', 'prediction prevention preparedness response strategies')
B(t12b, {
    'terms': [
        ('prediction', 'forecasting when and where a hazard will occur, for example by monitoring volcanoes'),
        ('preparedness', 'actions taken before a hazard to reduce its impacts, such as education, drills and emergency plans'),
        ('mitigation', 'actions that reduce the severity of a hazard’s impacts, for example building codes or levees'),
        ('Park’s disaster response curve', 'a model showing how quality of life falls during a disaster and recovers through relief, rehabilitation and reconstruction'),
        ('hazard management cycle', 'the continuous cycle of response, recovery, mitigation and preparedness'),
        ('aseismic building design', 'construction that resists earthquake shaking, for example with cross-bracing, base isolators and flexible frames'),
    ],
    'mcq': [
        ('Japan’s earthquake early warning system gives up to about', 'tens of seconds of warning before strong shaking', ['several days', 'several weeks', 'no warning at all'], '[1]'),
        ('Which is an example of preparedness?', 'school earthquake drills', ['rebuilding after a flood', 'international aid after a disaster', 'search and rescue'], '[1]'),
        ('Deaths from cyclones in Bangladesh fell from about 300 000 in 1970 to under 30 in 2020 (Amphan), partly because of', 'cyclone shelters and the Cyclone Preparedness Programme', ['fewer cyclones', 'no people on the coast', 'cooler seas'], '[1]'),
        ('Earthquakes cannot yet be predicted precisely because', 'there are no reliable short-term precursors of rupture', ['seismometers do not exist', 'they never occur on faults', 'they always give warning signs'], '[1]'),
    ],
    'explain': [
        ('Explain how volcanic eruptions can be predicted.', 'Monitoring of seismic swarms, ground deformation (tiltmeters, GPS, InSAR), gas emissions (SO₂), temperature changes and past eruption history; allowed the evacuation of over 60 000 people before Pinatubo in 1991.', '[4]'),
        ('Explain the stages of Park’s disaster response curve.', 'Normal quality of life; the event causes a sharp fall; relief (hours to days: rescue, medical care, aid); rehabilitation (weeks to months: services restored); reconstruction (years), possibly to a better level than before.', '[4]'),
        ('Explain how land-use planning can reduce hazard impacts.', 'Hazard maps restrict building in high-risk zones (floodplains, lahar paths, liquefiable land); open spaces as refuges; critical buildings in safe areas.', '[3]'),
    ],
    'claims': [
        ('Prevention of earthquakes is possible.', False, 'Earthquakes cannot be prevented; only their effects can be reduced.'),
        ('Response is more effective when communities are trained in advance.', True, 'Most survivors are rescued by neighbours in the first hours.'),
        ('Aid after disasters always reaches those who need it most.', False, 'Distribution can be slow, unequal or affected by corruption and poor access.'),
    ],
    'essays': [
        ('preparedness is more effective than response in reducing the impacts of hazards',
         ['Warnings, drills, shelters and building codes save lives before an event (Bangladesh, Japan, Chile 2010); every dollar spent on preparedness saves several in response.'],
         ['Rapid effective response (search and rescue, medical care, aid) reduces deaths and long-term impacts; some events are too large or sudden for preparedness alone.'],
         'Preparedness is generally more cost-effective, but effective response and recovery remain essential parts of the hazard management cycle.',
         ['warnings', 'building codes', 'aid', 'recovery']),
    ],
})


BD = [(1970, 'Bhola cyclone', 300000), (1991, 'the 1991 cyclone', 138000), (2007, 'Cyclone Sidr', 3400), (2020, 'Cyclone Amphan', 26)]


@data(t12b)
def t12b_bd(r, D):
    a, b = sorted(r.sample(range(4), 2))
    (y1, n1, d1), (y2, n2, d2) = BD[a], BD[b]
    pc = pct_change(d1, d2)
    pd = 2 if abs(pc) > 99 else 1
    stem = 'Table 12.2 shows the approximate number of deaths in Bangladesh from four major tropical cyclones: ' + '; '.join(f'{y} ({n}): about {nf(d)}' for y, n, d in BD) + '.'
    if D == 1:
        opts, ans = mcq(r, f'{sgn(pc, pd)}%', [f'{sgn(-pc, pd)}%', f'{sgn(d2 / d1 * 100, 2)}%', f'{sgn(pc / 2, pd)}%', f'{sgn(pc + 5, pd)}%'])
        return {'stem': stem + f' What was the percentage change in deaths between {y1} and {y2}?', 'options': opts, 'answer': ans, 'key': f'({nf(d2)} − {nf(d1)}) ÷ {nf(d1)} × 100 = {sgn(pc, pd)}%. [1]'}
    parts = [
        lambda r: (f'Calculate the percentage change in deaths between {y1} and {y2}.', f'{sgn(pc, pd)}%', f'({nf(d2)} − {nf(d1)}) ÷ {nf(d1)} × 100 [2]'),
        lambda r: ('Explain how preparedness has reduced cyclone deaths in Bangladesh.', 'The Cyclone Preparedness Programme’s volunteers spread warnings by megaphone and radio; thousands of raised cyclone shelters; evacuation of millions (about 2.4 million before Amphan); embankments and mangrove planting; better forecasting.', '1 mark per developed point [4]'),
        lambda r: ('Suggest why deaths are not the only measure of the success of hazard management.', 'Economic losses, homes and crops destroyed, people displaced, injuries, salinisation of land and long-term poverty also measure impact.', '[2]'),
        lambda r: ('Suggest why comparing these cyclones may be misleading.', 'The cyclones differed in strength, surge height, track, landfall time and tide; death counts in 1970 are uncertain; population has grown.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t12c = T('Case study of the management of a hazardous environment', 'case study of the management of a hazardous environment')
B(t12c, {
    'terms': [
        ('multi-hazard environment', 'a place affected by several hazards, such as earthquakes, tsunamis, volcanoes and typhoons in Japan'),
        ('exclusion zone', 'an area that people are forbidden to enter because of hazard, such as the southern part of Montserrat'),
        ('tsunami wall', 'a sea wall built to stop tsunami waves reaching the land, as along the Tōhoku coast'),
        ('resilience', 'the ability of a community to resist, absorb and recover from the effects of a hazard'),
        ('Hyogo and Sendai Frameworks', 'UN agreements (2005 and 2015) setting targets for disaster risk reduction'),
        ('hazard map', 'a map showing areas at risk from a hazard, used for planning and evacuation'),
    ],
    'mcq': [
        ('The Soufrière Hills volcano on Montserrat began erupting in', '1995', ['1902', '1980', '2010'], 'About two-thirds of the population left the island. [1]'),
        ('The Tōhoku earthquake of 2011 had a magnitude of', '9.0-9.1', ['6.0', '7.0', '10.5'], '[1]'),
        ('In Japan, 1 September is', 'Disaster Prevention Day, marked by national drills', ['a holiday for the end of typhoons', 'the start of the monsoon', 'the anniversary of Pinatubo'], 'It commemorates the 1923 Great Kantō earthquake. [1]'),
        ('Chile’s low death toll in the M8.8 earthquake of 2010 is mainly credited to', 'strict building codes', ['the absence of tsunamis', 'its low population', 'luck alone'], '[1]'),
    ],
    'explain': [
        ('Explain why Japan is a hazardous environment.', 'It lies where four plates meet (Pacific, Philippine Sea, Eurasian, North American): earthquakes, tsunamis and over 100 active volcanoes; typhoons, heavy rain and landslides; dense coastal population.', '[4]'),
        ('Explain the management of the volcanic hazard on Montserrat.', 'Montserrat Volcano Observatory monitors the volcano; exclusion zone covering the south including the old capital Plymouth; evacuation and resettlement in the north; UK aid for new housing and infrastructure.', '[3]'),
        ('Explain why management did not prevent large losses in the 2011 Tōhoku tsunami.', 'The tsunami (up to about 40 m locally) overtopped walls designed for smaller events; people relied on walls and earlier warnings underestimated the height; the Fukushima nuclear accident added a technological disaster.', '[3]'),
    ],
    'claims': [
        ('Japan’s management prevented any deaths in 2011.', False, 'About 18 000 people died, mostly in the tsunami.'),
        ('Building codes saved many lives in Japan in 2011.', True, 'Few buildings collapsed from shaking despite magnitude 9.'),
        ('The population of Montserrat is now larger than before 1995.', False, 'It fell from about 11 000 to about 5000.'),
    ],
    'cs': [
        ('the management of a hazardous environment', [
            ('Japan (Tōhoku 2011 and earthquake preparedness)', {'strategy': 'Strict building codes revised after 1981 and 1995 (Kobe); earthquake early warning system (2007); tsunami walls and evacuation towers; Disaster Prevention Day drills; hazard maps; JMA monitoring; after 2011 higher sea walls, raised land and relocation of homes uphill.',
                                                                 'evaluate': 'Few buildings collapsed from shaking in the M9.0 event and trains stopped safely; but about 18 000 died as the tsunami overtopped walls; Fukushima nuclear disaster; reconstruction cost over US$200 billion; some new walls are resented.'}),
            ('Montserrat (Soufrière Hills volcano)', {'strategy': 'Montserrat Volcano Observatory (1995) monitors seismicity, deformation and gas; exclusion zone and hazard-level system; evacuation of the south including Plymouth; resettlement in the north at Little Bay and Brades; UK aid.',
                                                      'evaluate': 'Only 19 deaths, in 1997, among people who had entered the exclusion zone; but the capital, airport and port were destroyed, two-thirds of the people emigrated and the economy depends on UK aid.'}),
            ('Bangladesh (tropical cyclones)', {'strategy': 'Cyclone Preparedness Programme (1972) with over 70 000 volunteers; thousands of multi-purpose cyclone shelters; coastal embankments and mangrove green belts; improved forecasting and mobile-phone warnings.',
                                                'evaluate': 'Deaths fell from about 300 000 (1970) to about 3400 (Sidr 2007) and 26 (Amphan 2020); but losses of homes, crops and land to salinity remain high, shelters can be overcrowded and poor women face barriers to evacuation.'}),
        ], [
            ('describe the strategies used to manage the hazards', 'strategy', 'Named strategies with dates and scale.'),
            ('evaluate the success of the management', 'evaluate', 'Evidence of successes and limitations, social, economic and environmental.', 'evaluate the extent to which hazard management has been successful.'),
        ]),
    ],
    'essays': [
        ('the management of hazardous environments is more successful in HICs than in LICs',
         ['Japan and Chile have strong building codes, monitoring and resources; deaths per event are low.'],
         ['HICs can fail (Katrina 2005, Tōhoku 2011); LICs such as Bangladesh have reduced cyclone deaths dramatically through low-cost community preparedness; economic losses are often higher in HICs.'],
         'Wealth helps, but effective governance and community preparedness are what make management successful.',
         ['wealth', 'governance', 'community preparedness', 'economic losses']),
    ],
})


CHAPTERS[12] = [t12a, t12b, t12c]


# ============================================================== CHAPTER 13: Hot arid and semi-arid climates

AI_CLS = [(0.05, 'hyper-arid'), (0.20, 'arid'), (0.50, 'semi-arid'), (0.65, 'dry sub-humid')]


def ai_class(x):
    for lim, n in AI_CLS:
        if x < lim:
            return n
    return 'humid'


ARID = [('Aswan, Egypt', 1, 2500), ('In Salah, Algeria', 15, 2300), ('Riyadh, Saudi Arabia', 100, 2100), ('Alice Springs, Australia', 280, 1900),
        ('Niamey, Niger', 540, 2000), ('Phoenix, USA', 200, 1800), ('Windhoek, Namibia', 360, 1900), ('Jodhpur, India', 360, 1800),
        ('Lima, Peru', 10, 900), ('Kano, Nigeria', 900, 1900), ('Kimberley, South Africa', 420, 1700), ('Dakar, Senegal', 450, 1600)]

t13a = T('Distribution and causes of hot arid and semi-arid climates', 'distribution causes of hot arid semi-arid climates')
B(t13a, {
    'terms': [
        ('aridity index', 'the ratio of annual precipitation to potential evapotranspiration (P ÷ PET); below 0.05 is hyper-arid, 0.05-0.20 arid and 0.20-0.50 semi-arid'),
        ('hot arid climate', 'a climate with annual rainfall usually below 250 mm, high temperatures and potential evapotranspiration far exceeding precipitation (Köppen BWh)'),
        ('semi-arid climate', 'a climate with about 250-500 mm of rainfall a year, usually in a short, unreliable wet season (Köppen BSh)'),
        ('subtropical anticyclone', 'a persistent area of high pressure at about 20-30° N and S where descending air warms and dries'),
        ('rainfall variability', 'the amount by which rainfall differs from the average from year to year, often measured by the coefficient of variation'),
        ('potential evapotranspiration (PET)', 'the amount of water that would be lost by evaporation and transpiration if water were always available'),
    ],
    'mcq': [
        ('Most hot deserts lie at about', '20-30° north and south of the equator', ['0-5° of the equator', '50-60° N', 'inside the Arctic Circle'], '[1]'),
        ('Clear skies in hot deserts cause', 'high daytime maxima and large diurnal temperature ranges', ['small diurnal ranges', 'frequent fog inland', 'constant temperatures'], '[1]'),
        ('A station with an aridity index of 0.12 is classed as', 'arid', ['hyper-arid', 'semi-arid', 'humid'], '[1]'),
        ('The Sahara is mainly caused by', 'descending air in the subtropical high-pressure belt', ['a cold current alone', 'a rain shadow alone', 'its high altitude'], '[1]'),
    ],
    'explain': [
        ('Explain how the global atmospheric circulation produces hot deserts.', 'Air rising at the ITCZ flows polewards aloft, cools and sinks at about 30°; sinking air warms adiabatically and its relative humidity falls, so clouds cannot form; the trade winds blowing out of the highs are dry.', '[4]'),
        ('Describe the characteristics of a hot arid climate.', 'Annual rainfall below 250 mm, falling irregularly in short intense storms; high summer temperatures (over 40 °C maxima); large diurnal range (20 °C or more); low humidity; very high PET.', '1 mark per characteristic [4]'),
        ('Explain why rainfall is highly variable in semi-arid areas.', 'They lie on the margins of the ITCZ or monsoon, so small shifts in its position or ENSO events change whether rain-bearing systems arrive; rainfall comes from a few large storms.', '[3]'),
    ],
    'claims': [
        ('All deserts are hot.', False, 'There are cold deserts such as the Gobi and Antarctica.'),
        ('Rainfall variability is generally greater where mean annual rainfall is low.', True, 'A few storms make up most of the total, so totals vary greatly.'),
        ('Deserts have no rain at all.', False, 'Most receive some rain, often in rare intense storms.'),
    ],
    'essays': [
        ('the subtropical high pressure belts are the main cause of hot arid climates',
         ['Most hot deserts (Sahara, Arabian, Kalahari, Australian) lie under the descending limbs of the Hadley cells.'],
         ['Cold ocean currents (Atacama, Namib), continentality (interior Australia, Thar margins), rain shadows (Patagonia, parts of the Great Basin) contribute; local factors explain the most extreme deserts.'],
         'Subtropical highs explain the global pattern, while currents, continentality and relief explain variations and the driest areas.',
         ['Hadley cell', 'cold currents', 'rain shadow', 'continentality']),
    ],
})


@data(t13a)
def t13a_ai(r, D):
    sts = r.sample(ARID, 4)
    sts = [(n, max(1, round(p * r.uniform(0.9, 1.1))), round(e * r.uniform(0.95, 1.05), -1)) for n, p, e in sts]
    ai = [p / e for _, p, e in sts]
    cl = [ai_class(x) for x in ai]
    stem = 'Table 13.1 shows mean annual precipitation (P) and potential evapotranspiration (PET) for four stations (mm): ' + '; '.join(f'{n}: P {p}, PET {nf(int(e))}' for n, p, e in sts) + '. Aridity index = P ÷ PET. Hyper-arid: below 0.05; arid: 0.05-0.20; semi-arid: 0.20-0.50; dry sub-humid: 0.50-0.65.'
    if D == 1:
        o, a = mcq(r, fmt(ai[0], 3), [fmt(sts[0][2] / sts[0][1], 1), fmt(ai[0] * 10, 3), fmt(ai[1], 3) if abs(ai[1] - ai[0]) > 0.001 else fmt(ai[0] / 2, 3), fmt(ai[0] + 0.1, 3)])
        return {'stem': stem + f' What is the aridity index of {sts[0][0]}?', 'options': o, 'answer': a, 'key': f'{sts[0][1]} ÷ {nf(int(sts[0][2]))} = {fmt(ai[0], 3)}. [1]'}
    deficit = [e - p for _, p, e in sts]
    parts = [
        lambda r: ('Calculate the aridity index of each station and classify it.', '; '.join(f'{s[0]}: {fmt(x, 3)} ({c})' for s, x, c in zip(sts, ai, cl)), 'P ÷ PET; 1 mark classification [3]'),
        lambda r: ('Calculate the annual water deficit (PET − P) at each station.', '; '.join(f'{s[0]}: {nf(int(d))} mm' for s, d in zip(sts, deficit)), '[1]'),
        lambda r: ('Explain why PET is so high in hot deserts.', 'High temperatures, intense insolation under clear skies, low humidity and often strong winds increase the potential rate of evaporation.', '[2]'),
        lambda r: (f'Suggest why {sts[0][0]} has the climate shown.', _ai_reason(sts[0][0]), '[2]'),
        lambda r: ('Explain why the aridity index is a better measure of aridity than rainfall alone.', 'It takes account of water lost by evapotranspiration, so a cool place and a hot place with the same rainfall can have very different water availability.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


def _ai_reason(n):
    if 'Lima' in n:
        return 'The cold Humboldt current and upwelling cool the air from below, creating a stable inversion that prevents rain, while the Andes block moist air from the east.'
    if any(k in n for k in ('Niamey', 'Kano', 'Dakar', 'Jodhpur')):
        return 'It lies on the margin of the ITCZ or monsoon, so it receives a short wet season, and lies under subtropical high pressure for the rest of the year.'
    if any(k in n for k in ('Alice', 'Phoenix', 'Windhoek', 'Kimberley')):
        return 'Subtropical high pressure, distance from the sea (continentality) and, in places, rain shadow from mountains limit rainfall.'
    return 'It lies under the descending air of the subtropical high-pressure belt, far from moisture sources, so air is stable and dry.'


t13b = T('Cold ocean currents, continentality and rain-shadow effects', 'cold ocean currents continentality rain-shadow effects')
B(t13b, {
    'terms': [
        ('cold ocean current', 'a current flowing from high latitudes towards the equator, such as the Benguela and Humboldt currents, which cools the air above it'),
        ('upwelling', 'the rise of cold, nutrient-rich water to the surface, often off west coasts where winds push surface water away'),
        ('temperature inversion', 'a layer where temperature increases with height, making the air stable and preventing rising air and rain'),
        ('continentality', 'the effect of distance from the sea, giving large temperature ranges and low rainfall'),
        ('rain shadow', 'the dry area on the leeward side of mountains, where descending air warms and dries'),
        ('fog desert', 'a coastal desert such as the Namib or Atacama where fog is frequent but rainfall almost nil'),
    ],
    'mcq': [
        ('The Atacama Desert is dry mainly because of', 'the cold Humboldt current, subtropical high pressure and the Andean rain shadow', ['the warm Gulf Stream', 'the ITCZ', 'monsoon winds'], '[1]'),
        ('Coastal fog in the Namib Desert forms when', 'moist air is cooled over the cold Benguela current', ['hot air rises over dunes', 'rain falls from cumulonimbus clouds', 'the ITCZ arrives'], '[1]'),
        ('Compared with a coastal desert station, an inland station at the same latitude usually has', 'a larger annual temperature range', ['a smaller annual temperature range', 'more fog days', 'cooler summers'], '[1]'),
        ('The Patagonian Desert in Argentina is mainly the result of', 'a rain shadow east of the Andes', ['a warm current', 'the ITCZ', 'subtropical low pressure'], '[1]'),
    ],
    'explain': [
        ('Explain how cold ocean currents contribute to aridity.', 'They cool the lowest layer of air, creating a temperature inversion and stable air; little evaporation; onshore air warms over land and its relative humidity falls; fog but little rain.', '[4]'),
        ('Explain how continentality affects the climate of desert interiors.', 'Distance from the sea means air has lost its moisture; land heats and cools quickly, giving very hot summers, cool winters and large ranges.', '[3]'),
        ('Explain the formation of a rain shadow.', 'Moist air is forced over mountains, cools adiabatically and loses moisture as rain on the windward side; on the leeward side it descends, warms at the dry adiabatic rate and becomes very dry.', '[3]'),
    ],
    'claims': [
        ('Coastal deserts beside cold currents have large annual temperature ranges.', False, 'The ocean moderates temperatures, giving small ranges and mild conditions.'),
        ('Fog can be an important water source in coastal deserts.', True, 'Plants, beetles and people (fog nets) collect fog water in the Namib and Atacama.'),
        ('Rain shadows only occur in the tropics.', False, 'They occur anywhere mountains lie across prevailing winds, e.g. Patagonia.'),
    ],
    'essays': [
        ('local factors are more important than global factors in explaining the location of the driest deserts',
         ['The driest places (Atacama, Namib) combine cold currents, inversions and rain shadow with subtropical highs.'],
         ['Global circulation (subtropical highs) explains the location of most arid areas, including the Sahara and Arabian deserts.'],
         'Global circulation explains the general pattern, but local factors explain the most extreme aridity.',
         ['subtropical highs', 'cold currents', 'relief', 'continentality']),
    ],
})


@data(t13b)
def t13b_coast(r, D):
    pair = r.choice([('Walvis Bay (coast, Namibia)', 'Keetmanshoop (inland, Namibia)'), ('Swakopmund (coast, Namibia)', 'Keetmanshoop (inland, Namibia)'), ('Lüderitz (coast, Namibia)', 'Upington (inland, South Africa)')])
    c = [round(x + r.uniform(-0.6, 0.6), 1) for x in [19.5, 20.0, 19.5, 18.0, 16.5, 15.5, 14.5, 14.0, 14.5, 15.5, 17.0, 18.5]]
    i = [round(x + r.uniform(-1.0, 1.0), 1) for x in [27.0, 26.0, 24.0, 20.5, 16.5, 13.0, 13.0, 15.5, 19.5, 22.5, 25.0, 26.5]]
    rc, ri = max(c) - min(c), max(i) - min(i)
    fog = r.randint(80, 140)
    stem = (f'Table 13.2 shows mean monthly temperatures (°C) at two stations at a similar latitude. {pair[0]}: ' + ', '.join(fmt(x, 1) for x in c) +
            f'. {pair[1]}: ' + ', '.join(fmt(x, 1) for x in i) + f'. (January first.) The coastal station has about {fog} fog days a year and almost no rain.')
    if D == 1:
        o, a = mcq(r, f'{dp(ri - rc, 1)} °C', [f'{dp(ri, 1)} °C', f'{dp(rc, 1)} °C', f'{dp(ri + rc, 1)} °C', f'{dp(max(i) - max(c), 1)} °C' if abs(max(i) - max(c) - (ri - rc)) > 0.05 else f'{dp(ri - rc + 2, 1)} °C'])
        return {'stem': stem + ' By how much is the annual temperature range greater inland than at the coast?', 'options': o, 'answer': a, 'key': f'{dp(ri, 1)} − {dp(rc, 1)} = {dp(ri - rc, 1)} °C. [1]'}
    parts = [
        lambda r: ('Calculate the annual temperature range at each station.', f'coast {dp(rc, 1)} °C; inland {dp(ri, 1)} °C', 'max − min [2]'),
        lambda r: ('Calculate the mean annual temperature at each station.', f'coast {dp(mean(c), 1)} °C; inland {dp(mean(i), 1)} °C', '[2]'),
        lambda r: ('Explain the differences in temperature between the two stations.', 'The cold current keeps coastal air cool and stable all year, and the sea heats and cools slowly, giving a small range; inland, land heats and cools rapidly with clear skies (continentality), giving hot summers and a large range.', '[3]'),
        lambda r: ('Explain why the coastal station has frequent fog but almost no rain.', 'Moist air from the ocean is cooled to its dew point over the cold current, forming advection fog; the inversion prevents the air from rising high enough to form rain clouds.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t13c = T('Climate change and the margins of arid environments', 'climate change margins of arid environments')
B(t13c, {
    'terms': [
        ('Sahel', 'the semi-arid belt south of the Sahara, from Senegal to Sudan, receiving about 200-600 mm of rain a year'),
        ('desert margin', 'a transition zone between a desert and wetter environments, sensitive to changes in rainfall'),
        ('coefficient of variation (CV)', 'the standard deviation of a data set divided by its mean, expressed as a percentage, used to measure rainfall variability'),
        ('African Humid Period', 'a wetter phase about 11 000-5000 years ago when the Sahara was largely grassland with lakes ("Green Sahara")'),
        ('drought', 'a long period of below-average rainfall causing water shortage'),
        ('expansion of the drylands', 'the predicted spread of arid conditions with global warming as the subtropical highs move polewards'),
    ],
    'mcq': [
        ('Severe Sahel droughts occurred mainly in', 'the 1970s and 1980s', ['the 1920s only', 'the 2050s', 'every year since 1500'], '[1]'),
        ('Evidence that the Sahara was once wetter includes', 'rock paintings of cattle and giraffes and old lake shorelines', ['ice cores from the Alps', 'coral reefs in the desert', 'glacial moraines in the Sahara'], '[1]'),
        ('Global warming is expected to cause the subtropical dry zones to', 'expand polewards', ['contract towards the equator', 'disappear', 'move into the Arctic'], '[1]'),
        ('A high coefficient of variation of rainfall means that rainfall is', 'unreliable from year to year', ['always high', 'always low', 'the same each year'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of drought in the Sahel.', 'Southward shift or weakening of the West African monsoon and ITCZ; changes in Atlantic sea-surface temperatures; aerosols; land degradation reducing moisture recycling; ENSO influences.', '[4]'),
        ('Explain why desert margins are sensitive to climate change.', 'Rainfall is close to the minimum for vegetation and farming; small changes in the position of the ITCZ or monsoon cause large percentage changes in rainfall; people depend on rain-fed farming and grazing.', '[3]'),
        ('Explain the evidence for past climate change in hot deserts.', 'Fossil dunes now vegetated, dry lake beds and shorelines, wadi systems cut by larger rivers, rock art, pollen in lake sediments, groundwater dated as fossil water.', '[3]'),
    ],
    'claims': [
        ('Rainfall in the Sahel has partly recovered since the 1980s.', True, 'Totals have increased, though with more intense storms and variability.'),
        ('Desert boundaries are fixed.', False, 'They have shifted with climate over thousands of years and continue to fluctuate.'),
        ('Climate change is the only cause of land degradation at desert margins.', False, 'Overgrazing, cultivation and deforestation also contribute.'),
    ],
    'essays': [
        ('climate change is the greatest threat to people living on the margins of arid environments',
         ['Rising temperatures increase evaporation; more variable rainfall and longer droughts reduce yields and pasture; the drylands are expected to expand.'],
         ['Population growth, poverty, conflict (Sahel), overgrazing and poor water management are often more immediate threats; adaptation can reduce risk.'],
         'Climate change multiplies existing threats, but human pressures and vulnerability determine how serious they become.',
         ['drought', 'population pressure', 'adaptation', 'land degradation']),
    ],
})


@data(t13c)
def t13c_cv(r, D):
    stn = r.choice(['Niamey, Niger', 'Kayes, Mali', 'Ouagadougou, Burkina Faso', 'El Obeid, Sudan', 'Tahoua, Niger'])
    base = r.randint(300, 600)
    yrs = list(range(2010, 2020))
    rain = [max(60, round(base * r.uniform(0.5, 1.5))) for _ in yrs]
    m = mean(rain)
    s = sd(rain)
    cv = s / m * 100
    below = sum(1 for x in rain if x < 0.75 * m)
    stem = f'Table 13.3 shows annual rainfall (mm) at {stn}: ' + ', '.join(f'{y}: {x}' for y, x in zip(yrs, rain)) + '.'
    if D == 1:
        o, a = mcq(r, f'{dp(m, 1)} mm', [f'{dp(median(rain), 1)} mm' if abs(median(rain) - m) > 0.05 else f'{dp(m + 20, 1)} mm', f'{max(rain) - min(rain)} mm', f'{dp(sum(rain) / 9, 1)} mm', f'{dp(m * 0.75, 1)} mm'])
        return {'stem': stem + ' What is the mean annual rainfall?', 'options': o, 'answer': a, 'key': f'{nf(sum(rain))} ÷ 10 = {dp(m, 1)} mm. [1]'}
    parts = [
        lambda r: ('Calculate the mean annual rainfall.', f'{dp(m, 1)} mm', f'{nf(sum(rain))} ÷ 10 [1]'),
        lambda r: ('The standard deviation of the data is ' + dp(s, 1) + ' mm. Calculate the coefficient of variation (CV = standard deviation ÷ mean × 100).', f'{dp(cv, 1)}%', f'{dp(s, 1)} ÷ {dp(m, 1)} × 100 [2]'),
        lambda r: ('Count the years with rainfall less than 75% of the mean.', f'{below} years (below {dp(0.75 * m, 1)} mm)', '[2]'),
        lambda r: ('Explain why rainfall is so variable in the Sahel.', 'Rain comes from the West African monsoon as the ITCZ moves north; small changes in how far north it moves and how long it stays, linked to ocean temperatures and ENSO, cause large changes in totals; a few storms supply much of the rain.', '[3]'),
        lambda r: ('Suggest the impacts of this variability on farmers and herders.', 'Crop failure in dry years; loss of pasture and livestock; food insecurity and migration; difficulty planning planting; in wet years floods and soil erosion.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[13] = [t13a, t13b, t13c]


# ============================================================== CHAPTER 14: Desert landforms

t14a = T('Weathering in deserts: insolation weathering and salt weathering', 'weathering in deserts insolation weathering salt weathering')
B(t14a, {
    'terms': [
        ('insolation weathering (thermal fracture)', 'the breakdown of rock by repeated expansion and contraction caused by large daily temperature changes'),
        ('exfoliation', 'the peeling away of curved sheets from a rock surface, often linked to thermal stress and the release of pressure'),
        ('granular disintegration', 'the breakdown of coarse-grained rock into individual grains as minerals expand and contract at different rates'),
        ('salt crystallisation', 'the growth of salt crystals in rock pores as water evaporates, exerting pressure that breaks the rock'),
        ('desert varnish', 'a dark coating of manganese and iron oxides on exposed desert rock surfaces'),
        ('hydration', 'the absorption of water by minerals such as salts and clays, causing them to expand'),
    ],
    'mcq': [
        ('Rock surface temperatures in hot deserts can range over a day by about', '40-50 °C', ['1-2 °C', '5 °C', '200 °C'], '[1]'),
        ('Salt weathering is most effective', 'where salty water evaporates repeatedly, as near playas and at the base of slopes', ['in permanently frozen ground', 'under rainforests', 'at the bottom of the sea'], '[1]'),
        ('Laboratory experiments by Griggs (1936) suggested that heating and cooling alone', 'caused little rock breakdown unless water was present', ['shattered rocks quickly', 'only affected ice', 'turned rock into salt'], '[1]'),
        ('Coarse-grained rocks such as granite are prone to granular disintegration because', 'their different minerals expand at different rates', ['they are porous like sandstone', 'they dissolve in rain', 'they contain fossils'], '[1]'),
    ],
    'explain': [
        ('Explain the process of salt weathering.', 'Saline water enters pores and cracks; evaporation causes crystals to grow, exerting pressure; heating makes salts expand and hydration makes them swell; repeated cycles break off grains and flakes.', '[3]'),
        ('Explain why the importance of insolation weathering has been questioned.', 'Experiments show heating and cooling of dry rock causes little breakdown; water (dew, rain) is usually needed, so chemical and salt processes may be more important; but very large and rapid changes can cause stress.', '[3]'),
        ('Explain why weathering rates are generally slow in hot deserts.', 'Lack of water limits chemical weathering; little vegetation and organic acids; but where moisture is present (dew, salt), weathering can be locally rapid.', '[3]'),
    ],
    'claims': [
        ('Water plays a role in most desert weathering.', True, 'Dew, fog and occasional rain enable salt, chemical and thermal processes.'),
        ('Salt weathering damages buildings in desert cities.', True, 'Concrete and stone are attacked in cities such as Bahrain and Cairo.'),
        ('Chemical weathering does not occur in deserts.', False, 'It occurs slowly, producing desert varnish and weathering in moist micro-sites.'),
    ],
    'essays': [
        ('weathering in hot deserts is mainly the result of high temperatures',
         ['Large diurnal temperature ranges cause thermal stress, exfoliation and granular disintegration.'],
         ['Experiments show heat alone is ineffective; moisture is essential for salt crystallisation, hydration and chemical processes; rock type and structure influence rates.'],
         'Temperature changes contribute, but moisture, especially salt solutions, is the critical factor in most desert weathering.',
         ['salt weathering', 'moisture', 'rock type', 'experiments']),
    ],
})


@data(t14a)
def t14a_salt(r, D):
    sol = ['distilled water', 'sodium chloride solution', 'sodium sulphate solution', 'magnesium sulphate solution']
    m0 = [round(r.uniform(95, 110), 1) for _ in sol]
    loss = [r.uniform(0.1, 0.6), r.uniform(2, 6), r.uniform(10, 30), r.uniform(5, 15)]
    m1 = [round(a * (1 - l / 100), 1) for a, l in zip(m0, loss)]
    pl = [(a - b) / a * 100 for a, b in zip(m0, m1)]
    cyc = r.choice([20, 30, 40])
    rock = r.choice(['sandstone', 'limestone', 'granite'])
    stem = (f'In an experiment, four blocks of {rock} were soaked in different solutions, dried at 60 °C, and the cycle repeated {cyc} times. Initial and final masses (g): ' +
            '; '.join(f'{s}: {fmt(a, 1)} to {fmt(b, 1)}' for s, a, b in zip(sol, m0, m1)) + '.')
    best = sol[pl.index(max(pl))]
    if D == 1:
        o, a = mcq(r, f'{dp(pl[2], 1)}%', [f'{dp(m0[2] - m1[2], 1)}%', f'{dp(pl[1], 1)}%', f'{dp(100 - pl[2], 1)}%', f'{dp(pl[3], 1)}%'])
        return {'stem': stem + ' What was the percentage loss in mass of the block in sodium sulphate solution?', 'options': o, 'answer': a, 'key': f'({fmt(m0[2], 1)} − {fmt(m1[2], 1)}) ÷ {fmt(m0[2], 1)} × 100 = {dp(pl[2], 1)}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage loss in mass for each block.', '; '.join(f'{s}: {dp(p, 1)}%' for s, p in zip(sol, pl)), '(initial − final) ÷ initial × 100 [3]'),
        lambda r: ('Identify the most effective solution and calculate the mean loss per cycle in grams.', f'{best}: {dp((m0[pl.index(max(pl))] - m1[pl.index(max(pl))]) / cyc, 2)} g per cycle', f'loss ÷ {cyc} [2]'),
        lambda r: ('Explain why the block in distilled water lost very little mass.', 'No salt crystals grow in the pores, so there is no crystallisation pressure; only slight wetting and drying.', '[2]'),
        lambda r: ('Explain why salts break rock.', 'As water evaporates, crystals grow in pores and exert pressure; salts such as sodium sulphate also expand when hydrated and heated; repeated cycles widen cracks and loosen grains.', '[3]'),
        lambda r: ('Suggest how the experiment could be made more reliable.', 'Repeat with several blocks per solution; use blocks of the same size and porosity; control temperature and drying time; weigh accurately after each cycle.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t14b = T('Wind processes and aeolian landforms: dunes, yardangs and zeugen', 'wind processes aeolian landforms dunes yardangs zeugen')
B(t14b, {
    'terms': [
        ('deflation', 'the removal of loose, fine material by wind, which can lower the land surface and form hollows'),
        ('abrasion (aeolian)', 'the wearing away of rock by sand grains carried by the wind, most effective within about 1-2 m of the ground'),
        ('saltation (aeolian)', 'the movement of sand grains in short hops close to the ground'),
        ('barchan', 'a crescent-shaped dune with horns pointing downwind, formed where sand supply is limited and wind blows from one direction'),
        ('seif (linear) dune', 'a long ridge of sand parallel to the dominant wind, formed by winds from two directions'),
        ('yardang', 'a streamlined ridge of rock carved by wind abrasion, parallel to the prevailing wind'),
        ('zeuge', 'a tabular block of resistant rock on a pedestal of softer rock, formed where horizontal strata are undercut by abrasion'),
    ],
    'mcq': [
        ('The horns of a barchan dune point', 'downwind', ['upwind', 'towards the equator', 'in random directions'], '[1]'),
        ('Wind abrasion is concentrated near the ground because', 'most sand grains move by saltation within 1-2 m of the surface', ['wind is fastest at ground level', 'there is no wind higher up', 'rocks are softer at the base'], '[1]'),
        ('Large barchan dunes move more slowly than small ones because', 'more sand must be moved to advance a larger dune', ['the wind is weaker over them', 'they are made of clay', 'they are fixed by vegetation'], '[1]'),
        ('Yardangs are aligned', 'parallel to the prevailing wind', ['at right angles to the wind', 'along river channels', 'randomly'], '[1]'),
    ],
    'explain': [
        ('Explain how wind transports sand.', 'Above a threshold velocity, grains are lifted; most move by saltation in short hops; impacts push larger grains along the surface (surface creep/reptation); fine dust travels in suspension.', '[3]'),
        ('Explain the formation of a barchan dune.', 'Wind blows sand up the gentle windward slope; at the crest it falls down the steep slip face (about 32-34°); the edges move faster as they contain less sand, forming horns pointing downwind; forms where sand supply is limited.', '[4]'),
        ('Explain the formation of zeugen and yardangs.', 'Abrasion by wind-blown sand attacks rock near the ground; zeugen form where horizontal resistant strata cap softer rock, undercut along joints; yardangs form in vertical bands parallel to the wind, streamlined by abrasion and deflation.', '[4]'),
    ],
    'claims': [
        ('Wind is the main agent shaping most desert landscapes.', False, 'Water is thought to be more important in many deserts; wind dominates locally.'),
        ('Dune type depends on wind direction and sand supply.', True, 'Barchans need limited sand and one wind direction; star dunes form with variable winds.'),
        ('Ergs (sand seas) cover most of the Sahara.', False, 'They cover about a fifth; most is rocky or stony desert.'),
    ],
    'essays': [
        ('wind is the most important agent in the formation of desert landforms',
         ['Wind forms dunes and ergs, deflation hollows (Qattara Depression), yardangs, zeugen and ventifacts.'],
         ['Water, from rare floods and from wetter past climates, forms wadis, alluvial fans, pediments, playas and mesas and buttes; weathering prepares material.'],
         'Wind is locally dominant, but water, past and present, is more important in shaping most desert landscapes.',
         ['dunes', 'wadis', 'past climates', 'weathering']),
    ],
})

add_spearman(t14b, [
    {'intro': 'Researchers measured the height and annual migration distance of {n} barchan dunes in the Kharga depression, Egypt.', 'label': 'Dune',
     'x': ('dune height (m)', 2, 30, 1), 'y': ('migration distance (m per year)', 3, 60, 0), 'sign': -1,
     'why': 'A larger dune contains more sand, and the wind can move only a limited volume per year, so tall dunes advance more slowly.',
     'limit': 'Wind speed and sand supply may differ between dunes; measure over several years and choose dunes in one dune field.'},
    {'intro': 'A study recorded the height above the ground and the depth of abrasion grooves on a yardang at {n} points.', 'label': 'Point',
     'x': ('height above ground (cm)', 10, 250, 0), 'y': ('groove depth (mm)', 1, 40, 0), 'sign': -1,
     'why': 'Most sand moves by saltation close to the ground, so abrasion is greatest near the base and declines with height.',
     'limit': 'Rock hardness may vary with height; sample several yardangs and test rock strength at each point.'},
])


t14c = T('Water in deserts: wadis, alluvial fans, pediments and playas', 'water in deserts wadis alluvial fans pediments playas')
B(t14c, {
    'terms': [
        ('wadi', 'a steep-sided, flat-floored valley in a desert, dry for most of the year but carrying flash floods after storms'),
        ('flash flood', 'a sudden, short-lived flood following an intense storm, with a very steep rising limb'),
        ('alluvial fan', 'a cone of sediment deposited where a mountain stream emerges onto a plain and loses energy'),
        ('bajada', 'a continuous slope formed by alluvial fans joining together along a mountain front'),
        ('pediment', 'a gently sloping rock surface at the foot of a steep mountain front in a desert'),
        ('playa', 'a flat, dry lake bed in a desert basin, covered by salts after water evaporates'),
        ('inselberg', 'an isolated steep-sided hill rising from a plain'),
    ],
    'mcq': [
        ('Flash floods in deserts are common because', 'intense storms fall on bare, often crusted ground with little infiltration', ['rain falls slowly for weeks', 'vegetation intercepts most rain', 'soils are deep and permeable'], '[1]'),
        ('Material on an alluvial fan usually becomes', 'finer away from the apex', ['coarser away from the apex', 'the same size everywhere', 'organic'], '[1]'),
        ('A bajada is formed by', 'the coalescence of alluvial fans', ['wind deposition', 'glaciers', 'coral growth'], '[1]'),
        ('Playas are covered with salt because', 'water evaporates from the basin, leaving dissolved salts behind', ['the sea floods them daily', 'salt is blown from glaciers', 'rocks are made of salt'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of an alluvial fan.', 'A stream emerges from a confined mountain canyon onto a plain; the channel widens and gradient falls; velocity drops and infiltration reduces discharge, so sediment is deposited, coarse near the apex and fine further out; channels shift, building a cone.', '[4]'),
        ('Explain why wadis have steep sides and flat floors.', 'Flash floods carry a large load and erode vertically and laterally; banks have little vegetation and collapse; sediment is spread across the floor as floods wane.', '[3]'),
        ('Explain the formation of a playa.', 'Streams flow into an enclosed basin after storms; a temporary lake forms; evaporation leaves fine sediment and salts; the flat surface is re-flooded only occasionally.', '[3]'),
    ],
    'claims': [
        ('Many desert landforms were formed under wetter past climates.', True, 'Large wadi systems and lake shorelines date from pluvial periods.'),
        ('Flash floods have long lag times.', False, 'Lag times are very short because overland flow is rapid.'),
        ('Pediments are formed only by wind.', False, 'They are thought to result mainly from sheet floods, weathering and scarp retreat.'),
    ],
    'essays': [
        ('present-day processes can explain most desert landforms',
         ['Flash floods form wadis, alluvial fans and playas today; wind shapes dunes; weathering continues.'],
         ['Many features (large wadis, pediments, inselbergs, fossil dunes, lake shorelines) formed under wetter or different climates; present rates are too slow to explain them.'],
         'Present processes modify desert landscapes, but many major landforms are inherited from past climates.',
         ['flash floods', 'pluvial periods', 'wind', 'equifinality']),
    ],
})


@data(t14c)
def t14c_flash(r, D):
    hrs = [0, 1, 2, 3, 4, 5, 6, 8, 10]
    peak_i = r.choice([2, 3])
    pk = r.randint(80, 400)
    q = []
    for i, h in enumerate(hrs):
        if i < peak_i:
            q.append(round(pk * (h / hrs[peak_i]) ** 2 * r.uniform(0.6, 0.9)) if h else 0)
        elif i == peak_i:
            q.append(pk)
        else:
            q.append(round(pk * math.exp(-(h - hrs[peak_i]) / r.uniform(1.0, 1.8))))
    rain_peak = r.choice([0.5, 1.5]) if peak_i == 3 else 0.5
    lag = hrs[peak_i] - rain_peak
    rise = pk / hrs[peak_i]
    w = r.choice(['Wadi Hadramawt, Yemen', 'a wadi in Oman', 'a wash in Arizona, USA', 'a wadi near Jeddah, Saudi Arabia', 'a dry river in the Negev, Israel'])
    stem = (f'Fig. 14.3 shows discharge (m³/s) in {w} after a thunderstorm whose peak rainfall occurred at {fmt(rain_peak, 1)} hours: ' +
            ', '.join(f'{h} h: {v}' for h, v in zip(hrs, q)) + '. Before the storm the channel was dry.')
    if D == 1:
        o, a = mcq(r, f'{fmt(lag, 1)} hours', [f'{hrs[peak_i]} hours', f'{fmt(lag + 1, 1)} hours', f'{fmt(lag + 3, 1)} hours', f'{fmt(rain_peak, 1)} hours' if rain_peak != lag else '6 hours'])
        return {'stem': stem + ' What was the lag time?', 'options': o, 'answer': a, 'key': f'{hrs[peak_i]} − {fmt(rain_peak, 1)} = {fmt(lag, 1)} hours. [1]'}
    parts = [
        lambda r: ('State the peak discharge and calculate the lag time.', f'{pk} m³/s; lag time {fmt(lag, 1)} hours', '[2]'),
        lambda r: ('Calculate the mean rate of rise of discharge from the start of the flood to the peak.', f'{dp(rise, 1)} m³/s per hour', f'{pk} ÷ {hrs[peak_i]} [2]'),
        lambda r: ('Explain why the hydrograph has a very steep rising limb.', 'Intense rainfall exceeds the infiltration capacity of bare, crusted soils, so rapid overland flow reaches the channel; little vegetation to intercept rain; steep slopes.', '[3]'),
        lambda r: ('Explain why discharge falls rapidly after the peak.', 'Rain stops quickly; water infiltrates into the dry channel bed (transmission losses) and evaporates; there is no groundwater baseflow.', '[3]'),
        lambda r: ('Suggest why flash floods are a hazard in desert towns.', 'Little warning; people and roads in dry wadi beds; high sediment loads damage property; drivers underestimate depth (e.g. Jeddah 2009).', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[14] = [t14a, t14b, t14c]


# ============================================================== CHAPTER 15: Desert soils and vegetation

CROPS_SALT = [('wheat', 6.0, 7.1), ('cotton', 7.7, 5.2), ('maize', 1.7, 12.0), ('rice', 3.0, 12.0), ('tomato', 2.5, 9.9), ('barley', 8.0, 5.0)]

t15a = T('Desert soils: aridisols and salinisation', 'desert soils aridisols salinisation')
B(t15a, {
    'terms': [
        ('aridisol', 'a desert soil with little organic matter, weak horizons and often accumulations of calcium carbonate, gypsum or salts'),
        ('salinisation', 'the accumulation of soluble salts in the soil, often caused by capillary rise and evaporation of irrigation water'),
        ('capillary action', 'the upward movement of water through soil pores, drawn towards the surface where it evaporates'),
        ('calcrete', 'a hard layer of calcium carbonate formed in desert soils by evaporation of water'),
        ('electrical conductivity (EC)', 'a measure of soil salinity in deci-siemens per metre (dS/m); soils above about 4 dS/m are classed as saline'),
        ('waterlogging', 'the saturation of soil, often caused by over-irrigation and poor drainage, which raises the water table'),
    ],
    'mcq': [
        ('A soil with an electrical conductivity of 6 dS/m is', 'saline', ['non-saline', 'acidic', 'peat'], 'Saline soils exceed about 4 dS/m. [1]'),
        ('Salinisation is most likely when', 'irrigation raises the water table and water evaporates from the surface', ['rainfall exceeds evaporation', 'soils are well drained and leached', 'land is left fallow under forest'], '[1]'),
        ('Desert soils are low in organic matter because', 'there is little vegetation to supply litter', ['decomposition is very slow because it is cold', 'it is all washed away by rain each day', 'earthworms remove it'], '[1]'),
        ('Large areas of irrigated land are affected by salinity in', 'the Indus Basin, Pakistan and the Murray-Darling Basin, Australia', ['the Amazon Basin', 'Ireland', 'Iceland'], '[1]'),
    ],
    'explain': [
        ('Explain the formation of aridisols.', 'Low rainfall means little leaching, so salts and carbonates accumulate; high evaporation draws water up by capillary action, depositing calcrete and salts; sparse vegetation gives little humus; weak horizon development.', '[4]'),
        ('Explain how irrigation can cause salinisation.', 'Water applied in excess raises the water table; capillary rise brings saline groundwater to the surface; evaporation leaves salts; irrigation water also contains dissolved salts; poor drainage prevents flushing.', '[4]'),
        ('Explain how salinisation can be managed.', 'Efficient irrigation (drip) and less water; drainage to lower the water table; leaching salts with extra water where drainage exists; salt-tolerant crops; planting trees to lower the water table.', '[3]'),
    ],
    'claims': [
        ('Desert soils are naturally very fertile for most crops.', False, 'They lack organic matter and nitrogen and may contain harmful salts.'),
        ('Salinisation reduces crop yields.', True, 'Salts make it harder for plants to absorb water and can be toxic.'),
        ('Salinisation can be reversed only by adding more salt.', False, 'It is reversed by leaching and drainage.'),
    ],
    'essays': [
        ('human activity is the main cause of soil degradation in arid environments',
         ['Irrigation without drainage causes salinisation and waterlogging (Indus Basin, Aral Sea basin); overgrazing and cultivation expose soil to erosion.'],
         ['Natural salinity, wind erosion of bare soils and drought cause degradation; climate change increases evaporation.'],
         'Natural conditions make arid soils fragile, but human mismanagement is the main cause of rapid degradation.',
         ['irrigation', 'overgrazing', 'drought', 'management']),
    ],
})


@data(t15a)
def t15a_salinity(r, D):
    crops = r.sample(CROPS_SALT, 3)
    ec = round(r.uniform(4.5, 12.0), 1)
    y = [max(0, min(100, 100 - b * (ec - a))) if ec > a else 100 for _, a, b in crops]
    plc = r.choice(['an irrigated field in Punjab, Pakistan', 'a farm in the Murray-Darling Basin, Australia', 'a field near the Aral Sea, Uzbekistan', 'a farm in the Nile delta, Egypt'])
    stem = (f'Soil at {plc} has an electrical conductivity (EC) of {fmt(ec, 1)} dS/m. Relative yield (%) = 100 − b × (EC − a) when EC is greater than a, where a is the crop’s salinity threshold (dS/m) and b the % yield loss per dS/m above it. Values: ' +
            '; '.join(f'{c}: a = {fmt(a, 1)}, b = {fmt(b, 1)}' for c, a, b in crops) + '.')
    best = crops[y.index(max(y))][0]
    if D == 1:
        c, a, b = crops[0]
        o, ans = mcq(r, f'{dp(y[0], 1)}%', [f'{dp(v, 1)}%' for v in (100 - y[0], y[0] / 2, y[0] + 15, y[0] - 15, y[0] + 8, y[0] - 8) if 0 <= v <= 100])
        return {'stem': stem + f' What is the expected relative yield of {c}?', 'options': o, 'answer': ans, 'key': (f'100 − {fmt(b, 1)} × ({fmt(ec, 1)} − {fmt(a, 1)}) = {dp(y[0], 1)}%. [1]' if ec > a else f'EC is below the threshold, so 100%. [1]')}
    parts = [
        lambda r: ('Calculate the expected relative yield of each crop.', '; '.join(f'{c}: {dp(v, 1)}%' for (c, _, _), v in zip(crops, y)), '100 − b(EC − a) [3]'),
        lambda r: ('State which crop the farmer should grow and why.', f'{cap(best)}: it is the most salt-tolerant of the three, giving the highest relative yield.', '[1]'),
        lambda r: ('Explain how the soil may have become saline.', 'Over-irrigation without drainage raised the water table; capillary rise and evaporation left salts at the surface; irrigation water added salts.', '[3]'),
        lambda r: ('Suggest how the field could be reclaimed.', 'Install sub-surface drains, then flush salts with good-quality water; switch to drip irrigation; grow salt-tolerant crops; apply gypsum on sodic soils.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t15b = T('Plant and animal adaptations to aridity: xerophytes and ephemerals', 'plant animal adaptations to aridity xerophytes ephemerals')
B(t15b, {
    'terms': [
        ('xerophyte', 'a plant adapted to survive long periods of drought, for example by storing water or reducing water loss'),
        ('ephemeral', 'a plant that completes its life cycle in a few weeks after rain and survives drought as seeds'),
        ('phreatophyte', 'a plant with very long roots that reach the water table, such as mesquite'),
        ('succulent', 'a plant that stores water in fleshy stems or leaves, such as a cactus'),
        ('CAM photosynthesis', 'a process in which stomata open at night to take in carbon dioxide, reducing water loss in the heat of the day'),
        ('aestivation', 'a state of dormancy that some desert animals enter to survive hot, dry periods'),
    ],
    'mcq': [
        ('The saguaro cactus stores water in', 'its expandable, pleated stem', ['its long leaves', 'its flowers', 'underground bulbs only'], '[1]'),
        ('Mesquite roots can reach depths of over', '50 m', ['5 cm', '50 cm', '5 km'], '[1]'),
        ('Ephemerals survive drought by', 'producing seeds that remain dormant until the next rain', ['storing water in trunks', 'growing tall', 'shedding bark'], '[1]'),
        ('The fennec fox’s large ears help it to', 'lose heat', ['store water', 'find mates only', 'dig burrows'], '[1]'),
    ],
    'explain': [
        ('Explain how xerophytes are adapted to aridity.', 'Small, waxy or spiny leaves and sunken stomata reduce transpiration; water storage in stems; deep tap roots or wide shallow roots; CAM photosynthesis; shedding leaves in drought.', '1 mark per adaptation [4]'),
        ('Explain the life cycle of desert ephemerals.', 'Seeds stay dormant for years; germination is triggered by enough rain (inhibitors washed out); rapid growth, flowering and seed setting within weeks before the soil dries.', '[3]'),
        ('Explain how desert animals survive high temperatures and lack of water.', 'Nocturnal behaviour and burrowing; concentrated urine and dry faeces; metabolic water from food; large ears or pale colour to lose heat; camels tolerate dehydration and body-temperature changes.', '[3]'),
    ],
    'claims': [
        ('All desert plants have deep roots.', False, 'Many cacti have wide, shallow roots to catch brief rain.'),
        ('Some desert plants open their stomata at night.', True, 'CAM plants take in carbon dioxide at night, reducing water loss.'),
        ('Camels store water in their humps.', False, 'Humps store fat; camels tolerate dehydration and conserve water.'),
    ],
    'essays': [
        ('plants and animals in hot deserts are adapted more to lack of water than to high temperatures',
         ['Most adaptations reduce water loss (waxy leaves, CAM, concentrated urine) or obtain water (deep roots, storage, metabolic water).'],
         ['Many adaptations deal with heat (pale colours, nocturnal behaviour, large ears, burrowing); the two stresses are linked since cooling by evaporation uses water.'],
         'Water shortage is the dominant stress, but adaptations to heat and water are closely linked.',
         ['xerophytes', 'ephemerals', 'animal behaviour', 'CAM']),
    ],
})


t15c = T('Semi-arid ecosystems and the effects of grazing', 'semi-arid ecosystems effects of grazing')
B(t15c, {
    'terms': [
        ('carrying capacity (grazing)', 'the maximum number of livestock an area can support without damaging the vegetation and soil'),
        ('overgrazing', 'grazing by more animals than the land can support, removing vegetation cover and exposing soil'),
        ('piosphere', 'a zone of degraded vegetation around a waterhole or borehole, where grazing pressure is highest'),
        ('tropical livestock unit (TLU)', 'a standard unit for comparing livestock, equivalent to an animal of 250 kg such as a cow'),
        ('nomadic pastoralism', 'moving herds seasonally between pastures in response to rainfall'),
        ('rotational grazing', 'moving livestock between fenced areas so that pasture can recover'),
    ],
    'mcq': [
        ('Vegetation cover around boreholes in the Sahel is usually', 'lowest close to the borehole and increases with distance', ['highest close to the borehole', 'the same everywhere', 'highest at 100 m only'], '[1]'),
        ('The sedentarisation of pastoralists tends to', 'concentrate grazing and increase degradation near settlements', ['reduce grazing pressure everywhere', 'increase rainfall', 'stop soil erosion'], '[1]'),
        ('Semi-arid vegetation such as the Sahel is dominated by', 'grasses with scattered thorny trees such as acacia', ['tall rainforest', 'coniferous forest', 'mosses and lichens'], '[1]'),
        ('Bush encroachment in semi-arid rangeland is encouraged by', 'heavy grazing that removes grasses and reduces fire', ['more frequent fires', 'removing all livestock', 'higher rainfall alone'], '[1]'),
    ],
    'explain': [
        ('Explain how overgrazing leads to land degradation.', 'Livestock remove grass faster than it regrows; trampling compacts soil and reduces infiltration; bare soil is eroded by wind and rain; palatable species disappear and shrubs invade.', '[4]'),
        ('Explain why traditional nomadic pastoralism was relatively sustainable.', 'Herds moved with the rains, so pasture had time to recover; herd size adjusted to drought; mixed herds used different vegetation.', '[3]'),
        ('Explain why grazing can be beneficial for semi-arid ecosystems.', 'Moderate grazing stimulates grass growth, recycles nutrients in dung, disperses seeds and reduces fuel for intense fires.', '[3]'),
    ],
    'claims': [
        ('Grazing always degrades semi-arid land.', False, 'Moderate, mobile grazing can maintain grasslands.'),
        ('Drilling boreholes can increase degradation locally.', True, 'Livestock concentrate around new water points.'),
        ('Carrying capacity is constant from year to year.', False, 'It varies with rainfall and pasture growth.'),
    ],
    'essays': [
        ('overgrazing is the main cause of degradation in semi-arid ecosystems',
         ['Rising herd sizes, sedentarisation and boreholes concentrate grazing, causing loss of cover and erosion (Sahel piospheres).'],
         ['Drought, rainfall variability, expansion of cultivation, fuelwood collection and fire changes also cause degradation; many rangelands recover after droughts (non-equilibrium ecology).'],
         'Overgrazing is important locally, especially around water points, but rainfall variability and other land uses are also major causes.',
         ['boreholes', 'drought', 'cultivation', 'resilience']),
    ],
})

add_spearman(t15c, [
    {'intro': 'Students measured grass cover at {n} quadrats at increasing distances from a borehole in northern Kenya.', 'label': 'Quadrat',
     'x': ('distance from the borehole (m)', 50, 3000, 0), 'y': ('grass cover (%)', 2, 80, 0), 'sign': 1,
     'why': 'Livestock gather near the water point, so grazing and trampling are most intense there and decline with distance (a piosphere).',
     'limit': 'Soil type and slope may vary; use transects in several directions and record dung counts as a measure of grazing.'},
    {'intro': 'A survey recorded stocking density and the percentage of bare ground at {n} plots in semi-arid rangeland in Botswana.', 'label': 'Plot',
     'x': ('stocking density (livestock units per km²)', 5, 60, 0), 'y': ('bare ground (%)', 5, 75, 0), 'sign': 1,
     'why': 'Higher stocking removes more vegetation and compacts the soil, leaving more bare ground.',
     'limit': 'Rainfall in the season before the survey affects cover; survey in the same season and record rainfall at each plot.'},
])


CHAPTERS[15] = [t15a, t15b, t15c]


# ============================================================== CHAPTER 16: Sustainable management of arid areas

t16a = T('Desertification: causes and impacts', 'desertification causes impacts')
B(t16a, {
    'terms': [
        ('desertification', 'land degradation in arid, semi-arid and dry sub-humid areas resulting from climatic variations and human activities (UN definition)'),
        ('land degradation', 'a reduction in the biological or economic productivity of land'),
        ('environmental refugee', 'a person forced to leave their home because of environmental change such as drought or desertification'),
        ('fuelwood crisis', 'a shortage of wood for cooking and heating, which leads to clearance of trees and shrubs'),
        ('UNCCD', 'the UN Convention to Combat Desertification (1994)'),
        ('dust storm', 'a strong wind carrying large amounts of dust, which increases where vegetation cover is removed'),
    ],
    'mcq': [
        ('The UN defines desertification as land degradation in', 'arid, semi-arid and dry sub-humid areas', ['all areas of the world', 'only hyper-arid deserts', 'tropical rainforests'], '[1]'),
        ('Which is a human cause of desertification?', 'overcultivation without fallow periods', ['the movement of the ITCZ', 'El Niño', 'the Coriolis effect'], '[1]'),
        ('Desertification is best described as', 'the degradation of land on the margins of deserts', ['the natural advance of sand dunes into rainforests', 'the formation of new deserts by volcanoes', 'the growth of oases'], '[1]'),
        ('About what share of the world’s land area is drylands?', 'about 40%', ['about 4%', 'about 90%', 'about 1%'], '[1]'),
    ],
    'explain': [
        ('Explain the human causes of desertification.', 'Overgrazing, overcultivation and shorter fallows, deforestation for fuelwood, poor irrigation causing salinisation, population growth, sedentarisation and cash-crop expansion onto marginal land.', '1 mark per cause [4]'),
        ('Explain the impacts of desertification on people.', 'Falling crop yields and loss of pasture; food insecurity and malnutrition; loss of income; migration to cities; conflict over land and water; dust storms affecting health.', '[4]'),
        ('Explain the role of feedback in desertification.', 'Loss of vegetation increases albedo and reduces evapotranspiration and moisture recycling, which may reduce rainfall, causing more vegetation loss (Charney hypothesis).', '[3]'),
    ],
    'claims': [
        ('Desertification means that deserts are steadily advancing.', False, 'It is patchy degradation, often around settlements and water points, not an advancing front.'),
        ('Desertification can be reversed.', True, 'Regreening in Niger and Burkina Faso shows land can recover.'),
        ('Population growth always causes desertification.', False, 'In Machakos, Kenya, more people led to better land management ("More people, less erosion").'),
    ],
    'essays': [
        ('desertification is caused more by human activity than by climate',
         ['Overgrazing, overcultivation, deforestation and poor irrigation directly degrade land; the UN definition stresses human activities.'],
         ['Drought and climatic variability (Sahel 1970s-80s) drive many degradation episodes; vegetation recovered when rains returned; climate change increases aridity.'],
         'Climate triggers degradation, but human pressures turn drought into lasting desertification.',
         ['drought', 'overgrazing', 'population', 'recovery']),
    ],
})


@data(t16a)
def t16a_cc(r, D):
    area = r.choice([2000, 5000, 8000, 12000])  # ha
    prod = r.choice([600, 800, 1000, 1500, 2000])  # kg dry matter per ha per year
    use = r.choice([0.3, 0.4, 0.5])
    need = 2300  # kg per TLU per year
    cc = area * prod * use / need
    herd = round(cc * r.uniform(0.6, 1.8))
    plc = r.choice(['a pastoral area in northern Burkina Faso', 'a rangeland in Turkana, Kenya', 'a communal grazing area in Botswana', 'a grazing area in Darfur, Sudan'])
    stem = (f'{cap(plc)} covers {nf(area)} ha. Grass production averages {prod} kg of dry matter per hectare per year, of which only {int(use * 100)}% can be eaten without damaging the pasture. '
            f'One tropical livestock unit (TLU) eats about {nf(need)} kg of dry matter a year. The present herd is {nf(herd)} TLU.')
    if D == 1:
        o, a = mcq(r, f'{nf(round(cc))} TLU', [f'{nf(round(cc / use))} TLU', f'{nf(round(area * prod / need * 0.1))} TLU', f'{nf(round(cc * 2))} TLU', f'{nf(herd)} TLU' if abs(herd - cc) > 5 else f'{nf(round(cc / 2))} TLU'])
        return {'stem': stem + ' What is the carrying capacity of the area?', 'options': o, 'answer': a, 'key': f'{nf(area)} × {prod} × {use} ÷ {nf(need)} = {nf(round(cc))} TLU. [1]'}
    st = herd / cc * 100
    parts = [
        lambda r: ('Calculate the carrying capacity of the area in TLU.', f'{nf(round(cc))} TLU', f'{nf(area)} × {prod} × {use} ÷ {nf(need)} [2]'),
        lambda r: ('Calculate the present stocking as a percentage of carrying capacity and state whether the area is overgrazed.', f'{dp(st)}%: ' + ('overgrazed' if st > 100 else 'not overgrazed at present'), f'{nf(herd)} ÷ {nf(round(cc))} × 100 [2]'),
        lambda r: ('Suggest why carrying capacity in a drought year would be lower.', 'Less rain means less grass growth, so the same herd exceeds the capacity; animals concentrate around remaining water.', '[2]'),
        lambda r: ('Explain how overgrazing can lead to desertification.', 'Loss of vegetation exposes soil to wind and water erosion; trampling compacts soil and reduces infiltration; palatable species decline; productivity falls in a downward spiral.', '[3]'),
        lambda r: ('Suggest how herders could manage the pasture more sustainably.', 'Reduce herd size or sell animals before droughts; rotational grazing; move herds seasonally; fodder banks; water points spaced out; community grazing rules.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t16b = T('Case study of sustainable management of an arid or semi-arid area', 'case study of sustainable management of an arid or semi-arid area')
B(t16b, {
    'terms': [
        ('Farmer Managed Natural Regeneration (FMNR)', 'a low-cost technique in which farmers protect and prune tree stumps and shoots regrowing in their fields'),
        ('zaï pits', 'small planting pits filled with manure that collect water and nutrients, used in Burkina Faso and Niger'),
        ('stone lines (cordons pierreux)', 'lines of stones laid along contours to slow run-off, trap soil and increase infiltration'),
        ('Great Green Wall', 'an African Union initiative launched in 2007 to restore degraded land across the Sahel from Senegal to Djibouti'),
        ('Grain for Green', 'a Chinese programme (1999) paying farmers to convert steep cropland to forest and grassland, used on the Loess Plateau'),
        ('regreening', 'the recovery of trees and vegetation in degraded drylands through local and planned action'),
    ],
    'mcq': [
        ('FMNR has helped regreen about 5 million hectares of farmland in', 'southern Niger', ['northern Canada', 'the Amazon', 'Japan'], '[1]'),
        ('Zaï pits are used to', 'concentrate water and manure around crops', ['store grain', 'drain wetlands', 'farm fish'], '[1]'),
        ('The Great Green Wall was originally planned as a belt about', '8000 km long and 15 km wide', ['80 km long', '800 m long', '80 000 km long'], '[1]'),
        ('The Loess Plateau Watershed Rehabilitation Project in China used', 'terracing, a ban on free grazing and planting on steep slopes', ['nuclear power', 'desalination', 'cloud seeding only'], '[1]'),
    ],
    'explain': [
        ('Explain why FMNR is considered sustainable.', 'It is cheap and uses existing root stocks; farmers own the trees and benefit from fuel, fodder and fruit; trees reduce wind erosion and improve soil fertility; spreads farmer to farmer.', '[3]'),
        ('Explain why large tree-planting schemes in drylands often fail.', 'Seedlings die without water and care; species unsuited to local conditions; little local ownership; grazing animals eat seedlings; insecurity and funding gaps.', '[3]'),
        ('Explain how water harvesting techniques help to combat desertification.', 'Stone lines, zaï pits and half-moons slow run-off, increase infiltration, trap sediment and organic matter, raise yields and allow trees and grasses to regenerate.', '[3]'),
    ],
    'claims': [
        ('The Great Green Wall has been completed as a continuous belt of trees.', False, 'Only a fraction of its target had been restored by the 2020s, and its approach has shifted to a mosaic of land-use practices.'),
        ('Local knowledge has been central to successful regreening in the Sahel.', True, 'Zaï pits and FMNR were developed and spread by farmers.'),
        ('The Loess Plateau project reduced sediment loads in the Yellow River.', True, 'Terracing and vegetation sharply reduced erosion.'),
    ],
    'cs': [
        ('the sustainable management of an arid or semi-arid area', [
            ('Maradi and Zinder regions, Niger (FMNR and water harvesting)', {'strategy': 'From the 1980s farmers protected regrowing stumps (FMNR), helped by changes to tree ownership laws; zaï pits and half-moons; NGO support (World Vision, Tony Rinaudo); farmer-to-farmer spread.',
                                                                           'evaluate': 'About 200 million trees on about 5 million ha; higher yields, fuelwood and fodder; less wind erosion; but gains are threatened by population growth, insecurity and drought, and benefits are uneven between households.'}),
            ('the Loess Plateau, China', {'strategy': 'Loess Plateau Watershed Rehabilitation Project (1994-2005, World Bank) and Grain for Green: terraces, check dams, bans on free grazing, tree and grass planting on steep slopes, land tenure for farmers.',
                                          'evaluate': 'Erosion and Yellow River sediment fell sharply; incomes roughly doubled for participants; vegetation cover rose; but planted trees use scarce water, some areas over-planted, and the approach was costly.'}),
            ('the Great Green Wall, Senegal', {'strategy': 'Part of the African Union initiative (2007): planting drought-tolerant species such as acacia, community gardens, fenced plots, local employment; aims to restore 100 million ha across the Sahel by 2030.',
                                               'evaluate': 'Some local successes with gardens and improved incomes; but high seedling mortality, only a small share of the target restored by the 2020s, funding delays and limited local ownership in places.'}),
        ], [
            ('describe the strategies used to manage the area', 'strategy', 'Named techniques, organisations, dates and scale.'),
            ('evaluate the extent to which the management is sustainable', 'evaluate', 'Environmental, economic and social evidence; limitations.', 'evaluate how successful the management has been in achieving sustainability.'),
        ]),
    ],
    'essays': [
        ('small-scale local schemes are more successful than large-scale projects in managing arid areas sustainably',
         ['FMNR and zaï pits in Niger and Burkina Faso are cheap, owned by farmers and have regreened millions of hectares.'],
         ['Large projects such as the Loess Plateau scheme achieved major improvements with government and World Bank funding; national policy (tree tenure laws) enabled local success; the Great Green Wall shows large schemes can fail without local ownership.'],
         'Local ownership is the key to success; large-scale schemes work when they support local action rather than impose top-down solutions.',
         ['community', 'funding', 'policy', 'scale']),
    ],
})


t16c = T('Water management and irrigation in arid lands', 'water management irrigation in arid lands')
B(t16c, {
    'terms': [
        ('fossil water', 'groundwater stored in aquifers thousands of years ago and not being recharged under the present climate'),
        ('drip irrigation', 'delivering water slowly to plant roots through pipes and emitters, reducing evaporation losses'),
        ('irrigation efficiency', 'the percentage of water applied that is actually used by the crop'),
        ('qanat (falaj, karez)', 'a traditional gently sloping underground channel that carries groundwater from hills to settlements by gravity'),
        ('desalination', 'removing salt from seawater or brackish water to make it usable'),
        ('Great Man-Made River', 'a Libyan project that pipes fossil groundwater from aquifers under the Sahara to coastal cities'),
    ],
    'mcq': [
        ('The approximate efficiency of surface (flood) irrigation is', '40-60%', ['90-95%', '5%', '100%'], '[1]'),
        ('Libya’s Great Man-Made River draws water from', 'the Nubian Sandstone Aquifer System', ['the River Nile', 'the Mediterranean Sea', 'glaciers'], '[1]'),
        ('Israel produces much of its drinking water by', 'desalination', ['importing icebergs', 'cloud seeding', 'qanats only'], '[1]'),
        ('The shrinking of the Aral Sea was caused mainly by', 'diversion of the Amu Darya and Syr Darya rivers for cotton irrigation', ['an earthquake', 'increased rainfall', 'tidal changes'], '[1]'),
    ],
    'explain': [
        ('Explain why the use of fossil water is unsustainable.', 'Aquifers are not recharged under present climates, so extraction lowers the water table permanently; wells must go deeper and costs rise; supplies will eventually run out.', '[3]'),
        ('Explain the advantages and disadvantages of drip irrigation.', 'Advantages: efficiency up to 90-95%, less salinisation, fertiliser applied with water, higher yields. Disadvantages: high installation cost, clogging, needs maintenance and reliable water pressure, less suited to some crops.', '[4]'),
        ('Explain the environmental impacts of large irrigation schemes in arid lands.', 'Salinisation and waterlogging; falling river flows and drying lakes (Aral Sea); falling water tables; pollution from fertilisers; loss of wetlands; disease in canals.', '[4]'),
    ],
    'claims': [
        ('Traditional qanats are sustainable because they use gravity and tap only what flows.', True, 'They take water at the rate of natural flow without pumping.'),
        ('Desalination has no environmental costs.', False, 'It uses much energy and discharges concentrated brine.'),
        ('Irrigation always increases food security in the long term.', False, 'Salinisation and aquifer depletion can reduce production over time.'),
    ],
    'essays': [
        ('technology can solve water shortages in arid environments',
         ['Desalination (Israel, the Gulf states), drip irrigation, water recycling and pipelines (Great Man-Made River) have greatly increased supply.'],
         ['Technology is costly and energy-intensive; fossil aquifers will run out; demand management, pricing, governance and traditional methods are needed; conflicts over shared rivers (Nile, Tigris-Euphrates).'],
         'Technology helps, but sustainable water management depends on reducing demand and fair governance.',
         ['desalination', 'drip irrigation', 'governance', 'fossil water']),
    ],
})


@data(t16c)
def t16c_irr(r, D):
    crop, req = r.choice([('cotton', 700), ('wheat', 450), ('dates', 1500), ('tomatoes', 600), ('alfalfa', 1200)])
    ha = r.choice([10, 25, 50, 120, 400])
    eff = [('flood', r.choice([40, 45, 50])), ('sprinkler', r.choice([70, 75])), ('drip', r.choice([85, 90]))]
    need = req * ha * 10  # m³
    supply = [(n, need / (e / 100)) for n, e in eff]
    saved = supply[0][1] - supply[2][1]
    plc = r.choice(['an oasis in Oman', 'a farm in the Negev, Israel', 'a farm near Ouarzazate, Morocco', 'a project in Rajasthan, India', 'a farm in Arizona, USA'])
    stem = (f'A farmer at {plc} grows {ha} ha of {crop}, which needs {req} mm of water per season. 1 mm of water over 1 ha = 10 m³. '
            'Irrigation efficiencies: ' + ', '.join(f'{n} {e}%' for n, e in eff) + '.')
    if D == 1:
        o, a = mcq(r, f'{nf(int(need))} m³', [f'{nf(int(req * ha))} m³', f'{nf(int(need * 10))} m³', f'{nf(int(supply[0][1]))} m³', f'{nf(int(need / 10))} m³'])
        return {'stem': stem + ' How much water does the crop itself need in one season?', 'options': o, 'answer': a, 'key': f'{req} × {ha} × 10 = {nf(int(need))} m³. [1]'}
    parts = [
        lambda r: ('Calculate the crop water requirement for the farm in m³.', f'{nf(int(need))} m³', f'{req} × {ha} × 10 [1]'),
        lambda r: ('Calculate the water that must be supplied with each irrigation method.', '; '.join(f'{n}: {nf(int(round(v)))} m³' for n, v in supply), 'requirement ÷ efficiency [3]'),
        lambda r: ('Calculate the water saved per season by switching from flood to drip irrigation.', f'{nf(int(round(saved)))} m³ ({dp(saved / supply[0][1] * 100)}% less)', '[2]'),
        lambda r: ('Explain why flood irrigation is inefficient in hot arid climates.', 'High evaporation from open channels and wet soil; seepage from unlined canals; water percolates below the roots; run-off from the field.', '[2]'),
        lambda r: ('Suggest why many farmers in LICs still use flood irrigation.', 'Low cost and simple technology; drip systems are expensive and need maintenance, filters and pumps; water is cheap or unpriced; small, fragmented plots.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[16] = [t16a, t16b, t16c]


# ============================================================== CHAPTER 17: Agricultural systems and food production

t17a = T('Agricultural systems and the factors affecting agricultural land use', 'agricultural systems factors affecting agricultural land use')
B(t17a, {
    'terms': [
        ('agricultural system', 'a farm viewed as a system with inputs (land, labour, capital, seeds), processes (ploughing, harvesting) and outputs (crops, livestock, income)'),
        ('intensive farming', 'farming with high inputs of labour or capital per unit area and high outputs per hectare'),
        ('extensive farming', 'farming with low inputs per unit area over large areas, giving low outputs per hectare'),
        ('subsistence farming', 'farming mainly to feed the farmer’s household, with little surplus for sale'),
        ('commercial farming', 'farming for sale and profit'),
        ('pastoral farming', 'rearing livestock for meat, milk, wool or hides'),
        ('arable farming', 'growing crops on ploughed land'),
    ],
    'mcq': [
        ('Wet rice cultivation in the Ganges delta is an example of', 'intensive subsistence farming', ['extensive commercial ranching', 'nomadic pastoralism', 'shifting cultivation'], '[1]'),
        ('Cattle ranching in the Australian outback is an example of', 'extensive commercial pastoral farming', ['intensive subsistence arable farming', 'market gardening', 'plantation agriculture'], '[1]'),
        ('Which is a physical factor affecting agricultural land use?', 'length of the growing season', ['government subsidies', 'access to markets', 'land tenure'], '[1]'),
        ('Market gardening near large cities is mainly influenced by', 'high land values and perishable produce needing quick transport', ['low rainfall', 'cheap land', 'remoteness from consumers'], '[1]'),
    ],
    'explain': [
        ('Explain the physical factors affecting agricultural land use.', 'Temperature and growing season, rainfall and its reliability, relief and slope, altitude, soil type, depth and drainage, aspect, risk of frost, drought and flood.', '1 mark per factor with effect [4]'),
        ('Explain the human factors affecting agricultural land use.', 'Markets and transport, capital and technology, labour supply, land tenure and farm size, government policy (subsidies, quotas), culture and diet, knowledge.', '1 mark per factor [4]'),
        ('Compare intensive and extensive farming systems.', 'Intensive: small areas, high inputs of labour or capital, high yields per ha (rice in Bangladesh, Dutch greenhouses). Extensive: large areas, low inputs per ha, low yields per ha but often high output per worker (Australian ranches, Canadian wheat).', '[3]'),
    ],
    'claims': [
        ('Intensive farming always involves large amounts of machinery.', False, 'Wet rice farming is labour-intensive with little machinery.'),
        ('Government policies can change farming land use.', True, 'Subsidies, quotas and land reform influence what farmers grow.'),
        ('Extensive farms usually have high outputs per hectare.', False, 'Output per hectare is low, though output per worker may be high.'),
    ],
    'essays': [
        ('physical factors are less important than human factors in explaining agricultural land use',
         ['Markets, capital, technology, government policy and land tenure explain much land use, especially in HICs (Dutch horticulture, irrigation in deserts).'],
         ['Climate, soil and relief set the limits for crops and livestock (e.g. rice needs warmth and water; ranching in semi-arid areas); physical risk remains important in LICs.'],
         'Physical factors set the possible range of land uses, while human factors decide which are actually chosen; human factors grow in importance with development.',
         ['climate', 'markets', 'technology', 'policy']),
    ],
})


@data(t17a)
def t17a_systems(r, D):
    farms = [('wet rice farm, Bangladesh', r.uniform(0.5, 1.5), r.randint(3, 6), round(r.uniform(4.0, 6.5), 1), 'rice'),
             ('wheat farm, Saskatchewan, Canada', r.randint(800, 1500), r.randint(2, 4), round(r.uniform(2.5, 3.5), 1), 'wheat'),
             ('cattle ranch, Queensland, Australia', r.randint(20000, 60000), r.randint(3, 8), round(r.uniform(0.002, 0.006), 4), 'beef (liveweight)')]
    farms = [(n, round(a, 1) if a < 10 else a, w, y, c) for n, a, w, y, c in farms]
    out = [a * y for _, a, _, y, _ in farms]
    per_w = [o / w for o, (_, _, w, _, _) in zip(out, farms)]
    stem = ('Table 17.1 shows data for three farms: area (ha), number of workers and output (tonnes per hectare per year). ' +
            '; '.join(f'{n}: {fmt(a, 1) if a < 10 else nf(a)} ha, {w} workers, {fmt(y, 4) if y < 0.1 else fmt(y, 1)} t/ha of {c}' for n, a, w, y, c in farms) + '.')
    if D == 1:
        o, a = mcq(r, f'{dp(per_w[1], 1)} t', [f'{dp(out[1], 1)} t', f'{dp(farms[1][3] / farms[1][2], 2)} t', f'{dp(per_w[0], 2)} t', f'{dp(per_w[1] / 2, 1)} t'])
        return {'stem': stem + ' What is the output per worker on the wheat farm?', 'options': o, 'answer': a, 'key': f'{nf(farms[1][1])} × {fmt(farms[1][3], 1)} ÷ {farms[1][2]} = {dp(per_w[1], 1)} t. [1]'}
    parts = [
        lambda r: ('Calculate the total output and the output per worker of each farm.', '; '.join(f'{f[0].split(",")[0]}: {dp(o, 1)} t, {dp(p, 2)} t per worker' for f, o, p in zip(farms, out, per_w)), 'area × yield; ÷ workers [3]'),
        lambda r: ('Classify each farm as intensive or extensive and justify your answer with data.', 'Rice: intensive (highest yield per ha, many workers per ha); wheat: extensive but capital-intensive (low yield per ha, very high output per worker); ranch: extensive (very low output per ha over a huge area).', '[3]'),
        lambda r: ('Explain why output per hectare is so low on the cattle ranch.', 'Semi-arid climate with low, unreliable rainfall gives sparse pasture, so stocking density must be very low; long distances to markets; low inputs.', '[2]'),
        lambda r: ('Explain why the rice farm uses so much labour.', 'Small plots, terracing, transplanting, weeding and water control are done by hand; labour is plentiful and cheap; capital for machinery is scarce.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t17b = T('Food production and food security at global and national scales', 'food production food security at global national scales')
B(t17b, {
    'terms': [
        ('food security', 'when all people at all times have physical and economic access to sufficient, safe and nutritious food (FAO, 1996)'),
        ('food insecurity', 'lack of reliable access to enough affordable, nutritious food'),
        ('undernourishment', 'when a person’s food intake is not enough to meet dietary energy requirements'),
        ('food import dependency', 'the share of a country’s food supply that is imported'),
        ('famine', 'an extreme, widespread shortage of food causing mass hunger and deaths'),
        ('four pillars of food security', 'availability, access, utilisation and stability'),
    ],
    'mcq': [
        ('About how many people worldwide were undernourished in the early 2020s?', 'about 700-800 million', ['about 7 million', 'about 70 million', 'about 7 billion'], '[1]'),
        ('Amartya Sen argued that famines are usually caused by', 'loss of access to food (entitlement failure) rather than absolute shortage', ['too much food', 'population decline', 'high rainfall'], '[1]'),
        ('The recommended average dietary energy requirement is about', '2100-2500 kcal per person per day', ['500 kcal', '10 000 kcal', '50 kcal'], '[1]'),
        ('The 2022 war in Ukraine raised global food prices because Ukraine and Russia are major exporters of', 'wheat, maize and sunflower oil', ['rice and tea', 'coffee and cocoa', 'bananas'], '[1]'),
    ],
    'explain': [
        ('Explain the factors that cause food insecurity.', 'Physical: drought, floods, pests, soil degradation. Human: poverty, conflict, high food prices, poor infrastructure and storage, population growth, dependence on imports, poor governance.', '1 mark per factor [4]'),
        ('Explain why a country may produce enough food but still have food insecurity.', 'Poor people cannot afford food; unequal distribution between regions and groups; exports of crops; waste and poor storage; conflict blocking access.', '[3]'),
        ('Explain the global pattern of food insecurity.', 'Highest in sub-Saharan Africa and South Asia, linked to poverty, conflict, climate hazards and rapid population growth; low in HICs with high incomes and imports.', '[3]'),
    ],
    'claims': [
        ('The world produces enough food to feed everyone.', True, 'Hunger results mainly from poverty, distribution and waste.'),
        ('Food security only concerns the quantity of food.', False, 'It also concerns nutrition, safety, access and stability.'),
        ('High dependence on food imports can increase vulnerability.', True, 'Price spikes and supply shocks quickly affect import-dependent countries.'),
    ],
    'essays': [
        ('food insecurity is caused more by human factors than by physical factors',
         ['Poverty, conflict (Yemen, Sudan), prices, poor infrastructure and inequality explain most hunger; famines are entitlement failures (Sen).'],
         ['Drought, floods, pests (locusts in East Africa 2020) and climate change reduce production; physical shocks trigger crises in vulnerable places.'],
         'Physical events often trigger food crises, but human factors determine who goes hungry.',
         ['poverty', 'conflict', 'drought', 'access']),
    ],
})


@data(t17b)
def t17b_import(r, D):
    cty = r.choice(['Country A', 'Country B'])
    prod = r.randint(10, 80) * 100
    imp = r.randint(5, 40) * 100
    exp_ = r.randint(0, min(prod // 100 - 1, 10)) * 100
    supply = prod + imp - exp_
    dep = imp / supply * 100
    pop = r.choice([10, 20, 35, 50])
    kg = supply * 1000 / (pop * 1e6) * 1000  # thousand tonnes -> kg per person
    stem = (f'Table 17.2 shows cereal data for {cty} in one year (thousand tonnes): production {nf(prod)}, imports {nf(imp)}, exports {nf(exp_)}. The population is {pop} million. '
            'Import dependency ratio = imports ÷ (production + imports − exports) × 100.')
    if D == 1:
        o, a = mcq(r, f'{dp(dep)}%', [f'{dp(v)}%' for v in (imp / prod * 100, imp / (prod + imp) * 100, 100 - dep, dep + 10, dep / 2, prod / supply * 100)])
        return {'stem': stem + ' What is the cereal import dependency ratio?', 'options': o, 'answer': a, 'key': f'{nf(imp)} ÷ ({nf(prod)} + {nf(imp)} − {nf(exp_)}) × 100 = {dp(dep)}%. [1]'}
    parts = [
        lambda r: ('Calculate the cereal import dependency ratio.', f'{dp(dep)}%', f'{nf(imp)} ÷ {nf(supply)} × 100 [2]'),
        lambda r: ('Calculate the cereal supply per person in kilograms per year.', f'{dp(kg, 0)} kg', f'{nf(supply)} thousand t ÷ {pop} million [2]'),
        lambda r: ('Suggest why a high import dependency ratio may threaten food security.', 'Price spikes on world markets (2008, 2022), currency falls, export bans and transport disruption can cut supplies; the poor spend a large share of income on food.', '[3]'),
        lambda r: ('Suggest how the country could increase its food security.', 'Invest in irrigation, improved seeds and extension services; reduce post-harvest losses with better storage; strategic grain reserves; diversify import sources; social safety nets.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


GR = [(1961, 0.85), (1970, 1.21), (1980, 1.44), (1990, 2.12), (2000, 2.78), (2010, 2.84), (2020, 3.43)]

t17c = T('Agricultural intensification and the Green Revolution', 'agricultural intensification green revolution')
B(t17c, {
    'terms': [
        ('Green Revolution', 'the spread from the 1960s of high-yielding varieties of wheat and rice, with fertilisers, pesticides and irrigation, especially in Asia and Latin America'),
        ('high-yielding variety (HYV)', 'a crop variety bred to give much larger yields, often short-stemmed and responsive to fertiliser, such as IR8 rice'),
        ('agricultural intensification', 'increasing output per hectare through greater inputs of labour, capital, fertiliser or technology'),
        ('Gene Revolution', 'the use of genetically modified crops to raise yields or resistance to pests and drought'),
        ('mechanisation', 'replacing human and animal labour with machines such as tractors and combine harvesters'),
        ('multiple cropping', 'growing two or more crops on the same land in one year'),
    ],
    'mcq': [
        ('IR8, the first “miracle rice”, was released in 1966 by', 'the International Rice Research Institute in the Philippines', ['the WTO', 'the European Union', 'NASA'], '[1]'),
        ('The Green Revolution in India was most successful in', 'Punjab and Haryana', ['Kerala’s hill forests', 'the Thar Desert', 'Arunachal Pradesh'], '[1]'),
        ('A problem associated with the Green Revolution is', 'falling water tables from heavy irrigation', ['lower wheat yields', 'less fertiliser use', 'more crop diversity'], '[1]'),
        ('The Green Revolution had least impact in sub-Saharan Africa partly because', 'staple crops such as cassava, sorghum and millet received less research and irrigation is limited', ['Africa grows no crops', 'there is too much water', 'land is too cheap'], '[1]'),
    ],
    'explain': [
        ('Explain the positive impacts of the Green Revolution.', 'Yields of wheat and rice doubled or tripled; India became self-sufficient in grain; fewer famines; double cropping; higher incomes for larger farmers; lower food prices.', '[4]'),
        ('Explain the negative impacts of the Green Revolution.', 'Wider inequality as richer farmers could afford inputs; debt; falling water tables and salinisation (Punjab); pesticide pollution and health effects; loss of crop diversity; mechanisation reducing jobs.', '1 mark per impact [4]'),
        ('Explain why the Green Revolution spread unevenly.', 'HYVs needed irrigation, fertiliser and credit, so areas with water and wealthier farmers adopted first; staple crops of drylands and Africa were neglected; infrastructure and markets varied.', '[3]'),
    ],
    'claims': [
        ('The Green Revolution ended hunger in India.', False, 'Production rose greatly, but many people remain undernourished because of poverty.'),
        ('HYVs need more water and fertiliser than traditional varieties.', True, 'Their high yields depend on high inputs.'),
        ('The Green Revolution increased the yields of all crops equally.', False, 'Wheat and rice gained most; pulses and millets much less.'),
    ],
    'essays': [
        ('the benefits of the Green Revolution have outweighed its costs',
         ['Huge increases in yields and output saved millions from famine; India and other Asian countries became self-sufficient; food prices fell.'],
         ['Environmental damage (groundwater depletion, salinisation, pesticides), rising inequality and debt, loss of biodiversity, farmer distress in Punjab; less success in Africa.'],
         'Overall the benefits in food supply were huge, but the environmental and social costs mean the model now needs to become more sustainable.',
         ['yields', 'inequality', 'water', 'sustainability']),
    ],
})


@data(t17c)
def t17c_gr(r, D):
    a, b = sorted(r.sample(range(len(GR)), 2))
    (y1, v1), (y2, v2) = GR[a], GR[b]
    pc = pct_change(v1, v2)
    n = y2 - y1
    cagr = ((v2 / v1) ** (1 / n) - 1) * 100
    stem = 'Fig. 17.3 shows mean wheat yields in India (tonnes per hectare): ' + ', '.join(f'{y}: {fmt(v, 2)}' for y, v in GR) + '.'
    if D == 1:
        o, ans = mcq(r, f'{sgn(pc)}%', [f'{sgn(v2 / v1 * 100)}%', f'{sgn(pc / 2)}%', f'{sgn((v2 - v1) * 100)}%' if abs((v2 - v1) * 100 - pc) > 1 else f'{sgn(pc + 20)}%', f'{sgn(pc - 20)}%'])
        return {'stem': stem + f' What was the percentage increase in yield between {y1} and {y2}?', 'options': o, 'answer': ans, 'key': f'({fmt(v2, 2)} − {fmt(v1, 2)}) ÷ {fmt(v1, 2)} × 100 = {sgn(pc)}%. [1]'}
    dec = [(GR[i][0], GR[i + 1][0], GR[i + 1][1] - GR[i][1]) for i in range(len(GR) - 1)]
    big = max(dec, key=lambda x: x[2])
    parts = [
        lambda r: (f'Calculate the percentage increase in yield between {y1} and {y2}.', f'{sgn(pc)}%', f'({fmt(v2, 2)} − {fmt(v1, 2)}) ÷ {fmt(v1, 2)} × 100 [2]'),
        lambda r: (f'Calculate the mean annual growth rate of yield between {y1} and {y2}.', f'{dp(cagr, 2)}% per year', f'({fmt(v2, 2)} ÷ {fmt(v1, 2)})^(1/{n}) − 1 [2]'),
        lambda r: ('Identify the period with the largest increase and explain why yields rose rapidly then.', f'{big[0]}-{big[1]} (+{fmt(big[2], 2)} t/ha): spread of high-yielding varieties, expansion of tube-well irrigation, fertiliser subsidies and guaranteed minimum support prices.', '[3]'),
        lambda r: ('Suggest why yield growth slowed between 2000 and 2010.', 'Diminishing returns to fertiliser, soil degradation and falling water tables in Punjab, little new irrigated land, heat stress and limited new varieties.', '[2]'),
        lambda r: ('Explain one environmental problem caused by the Green Revolution in Punjab.', 'Over-pumping of groundwater for irrigation has lowered water tables by about 0.5-1 m a year in places; or heavy fertiliser and pesticide use pollutes water and soils.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[17] = [t17a, t17b, t17c]


# ============================================================== CHAPTER 18: The management of agricultural change

t18a = T('Land reform and changes in land tenure', 'land reform changes in land tenure')
B(t18a, {
    'terms': [
        ('land tenure', 'the system by which land is owned, rented or held, including the rights of those who use it'),
        ('land reform', 'the redistribution of land ownership and changes to tenure, usually to reduce inequality'),
        ('land consolidation', 'combining small, scattered plots into larger, more efficient holdings'),
        ('sharecropping', 'a tenancy in which the farmer pays the landowner a share of the crop as rent'),
        ('collectivisation', 'the combining of individual farms into large state or communal farms'),
        ('latifundia and minifundia', 'very large estates and very small holdings, typical of land inequality in Latin America'),
    ],
    'mcq': [
        ('Land reform in Zimbabwe after 2000 involved', 'the fast-track redistribution of large commercial farms', ['collectivisation into communes', 'consolidation of small plots into estates', 'privatisation of state farms'], '[1]'),
        ('China’s Household Responsibility System (from 1978)', 'allowed families to farm land and sell surpluses after meeting quotas', ['created large private estates', 'abolished farming', 'collectivised all farms'], '[1]'),
        ('Fragmented landholdings reduce efficiency because', 'farmers waste time travelling between plots and machinery is hard to use', ['plots are too large', 'they increase soil fertility', 'they are always irrigated'], '[1]'),
        ('Secure land tenure encourages farmers to', 'invest in soil conservation and trees', ['abandon farming', 'reduce yields', 'move to cities'], '[1]'),
    ],
    'explain': [
        ('Explain why land reform is carried out.', 'To reduce inequality in land ownership; to increase production by giving land to those who farm it; to reduce rural poverty and conflict; to correct historical injustices such as colonial land seizure.', '[4]'),
        ('Explain how insecure land tenure can lead to environmental degradation.', 'Tenants and squatters have little incentive to invest in long-term improvements such as terraces or trees; they maximise short-term output; land may be overused.', '[3]'),
        ('Explain the problems of land reform.', 'Resistance from landowners; lack of credit, seeds and skills for new owners; falling output during transition; corruption and elite capture; plots too small; compensation costs.', '[3]'),
    ],
    'claims': [
        ('Land reform always increases agricultural production.', False, 'Production fell sharply in Zimbabwe after 2000.'),
        ('Unequal land ownership is common in Latin America.', True, 'Large estates own a high share of land in Brazil and other countries.'),
        ('Land consolidation can help mechanisation.', True, 'Larger, compact plots suit machines.'),
    ],
    'essays': [
        ('land reform is the most effective way of improving rural livelihoods',
         ['Redistribution reduces inequality and poverty (Taiwan and South Korea after 1950, China’s Household Responsibility System raised output); secure tenure encourages investment.'],
         ['Reform without credit, inputs and markets can fail (Zimbabwe); infrastructure, education, irrigation, microfinance and non-farm jobs may matter more.'],
         'Land reform can be powerful but works only as part of a package of rural development policies.',
         ['inequality', 'tenure', 'support services', 'productivity']),
    ],
})


@data(t18a)
def t18a_tenure(r, D):
    cls = ['under 1 ha', '1-5 ha', '5-20 ha', 'over 20 ha']
    hh = [r.randint(45, 65), r.randint(20, 30), r.randint(6, 12), 0]
    hh[3] = 100 - sum(hh[:3])
    if hh[3] < 1:
        return None
    land = [r.randint(2, 6), r.randint(10, 20), r.randint(15, 25), 0]
    land[3] = 100 - sum(land[:3])
    ratio = (land[3] / hh[3]) / (land[0] / hh[0])
    cty = r.choice(['a district in Brazil', 'a region of Guatemala', 'a province in the Philippines', 'a region of Kenya'])
    stem = ('Table 18.1 shows the distribution of farm households and farmland by farm size in ' + cty + ' (% of households, % of land): ' +
            '; '.join(f'{c}: {h}%, {l}%' for c, h, l in zip(cls, hh, land)) + '.')
    if D == 1:
        o, a = mcq(r, f'{land[3]}%', [f'{hh[3]}%', f'{100 - land[3]}%', f'{land[2]}%', f'{land[3] + hh[3]}%'])
        return {'stem': stem + f' What percentage of the land is held by the {hh[3]}% of households with farms over 20 ha?', 'options': o, 'answer': a, 'key': f'{land[3]}% (read from the table). [1]'}
    parts = [
        lambda r: ('Calculate the ratio of the share of land to the share of households for each farm size class.', '; '.join(f'{c}: {dp(l / h, 2)}' for c, h, l in zip(cls, hh, land)), '% land ÷ % households [3]'),
        lambda r: ('Calculate how many times more land per household the largest farms have than the smallest.', f'about {dp(ratio, 0)} times', f'({land[3]} ÷ {hh[3]}) ÷ ({land[0]} ÷ {hh[0]}) [2]'),
        lambda r: ('Describe what the data show about land inequality.', f'Highly unequal: {hh[0]}% of households (under 1 ha) hold only {land[0]}% of land, while {hh[3]}% (over 20 ha) hold {land[3]}%.', '[2]'),
        lambda r: ('Suggest the problems of land reform that redistributes land from the largest farms.', 'Opposition and legal challenges from owners; cost of compensation; new farmers need credit, seeds, training and markets; output may fall; land may go to political supporters.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t18b = T('Agricultural change and its environmental and social impacts', 'agricultural change its environmental social impacts')
B(t18b, {
    'terms': [
        ('eutrophication', 'enrichment of water by nutrients from fertilisers or sewage, causing algal blooms and oxygen depletion'),
        ('diminishing returns', 'when each additional unit of an input such as fertiliser gives a smaller increase in output'),
        ('agribusiness', 'large-scale, capital-intensive farming run as a business, often linked to processing and retail companies'),
        ('monoculture', 'growing a single crop over a large area year after year'),
        ('rural-urban migration', 'the movement of people from the countryside to towns and cities, often as farming mechanises'),
        ('organic farming', 'farming without synthetic fertilisers and pesticides'),
    ],
    'mcq': [
        ('Excess nitrogen fertiliser most commonly causes', 'nitrate pollution of rivers and groundwater', ['ozone depletion', 'earthquakes', 'acid rain from volcanoes'], '[1]'),
        ('Mechanisation of farming usually leads to', 'fewer farm jobs and larger farms', ['more farm workers', 'smaller fields', 'less output per worker'], '[1]'),
        ('Removal of hedgerows in the UK after 1945 led to', 'loss of wildlife habitats and more soil erosion', ['more biodiversity', 'less machinery use', 'smaller fields'], '[1]'),
        ('A social impact of commercial agriculture expanding in LICs is', 'displacement of smallholders and land grabs', ['higher biodiversity', 'more subsistence farming', 'lower exports'], '[1]'),
    ],
    'explain': [
        ('Explain the environmental impacts of agricultural intensification.', 'Soil erosion and compaction; nitrate and phosphate pollution causing eutrophication; pesticide effects on wildlife and pollinators; loss of hedgerows and habitats; groundwater depletion; greenhouse gas emissions.', '1 mark per impact [4]'),
        ('Explain the social impacts of agricultural change in rural areas.', 'Fewer jobs and rural depopulation; growth of larger farms; rising inequality; debt for inputs; changing gender roles; loss of traditional knowledge; better incomes for some.', '[4]'),
        ('Explain the concept of diminishing returns in fertiliser use.', 'At first, extra fertiliser raises yields greatly, but each further increment adds less, until the crop cannot use more and excess is lost to water.', '[2]'),
    ],
    'claims': [
        ('Agricultural change has only negative impacts.', False, 'It has raised food production and incomes for many.'),
        ('Monocultures are vulnerable to pests and disease.', True, 'A single crop allows pests to spread rapidly.'),
        ('Fertiliser use always raises yields in proportion to the amount applied.', False, 'Returns diminish at higher application rates.'),
    ],
    'essays': [
        ('the environmental costs of agricultural change are greater than the social costs',
         ['Soil degradation, water pollution, groundwater depletion and biodiversity loss threaten future production everywhere.'],
         ['Social costs (rural depopulation, inequality, debt and farmer distress, displacement by land grabs) affect millions directly and are severe in LICs.'],
         'Both are serious; their relative importance depends on the place and type of change.',
         ['pollution', 'inequality', 'mechanisation', 'sustainability']),
    ],
})


@data(t18b)
def t18b_fert(r, D):
    rates = [0, 50, 100, 150, 200, 250]
    ymax = round(r.uniform(6.0, 9.0), 1)
    y0 = round(r.uniform(2.0, 3.5), 1)
    k = r.uniform(0.010, 0.018)
    ys = [round(y0 + (ymax - y0) * (1 - math.exp(-k * x)), 1) for x in rates]
    inc = [round(ys[i + 1] - ys[i], 1) for i in range(5)]
    if len(set(inc)) < 3:
        return None
    crop = r.choice(['wheat', 'maize', 'rice'])
    stem = (f'Table 18.2 shows the results of a fertiliser trial on {crop} in Punjab, India (nitrogen applied in kg/ha, yield in t/ha): ' + ', '.join(f'{x} kg: {fmt(y, 1)} t' for x, y in zip(rates, ys)) + '.')
    if D == 1:
        o, a = mcq(r, f'{fmt(inc[0], 1)} t/ha', [f'{fmt(inc[-1], 1)} t/ha', f'{fmt(ys[1], 1)} t/ha', f'{fmt(ys[-1] - ys[0], 1)} t/ha', f'{fmt(inc[0] / 2, 2)} t/ha'])
        return {'stem': stem + ' What was the increase in yield from the first 50 kg/ha of nitrogen?', 'options': o, 'answer': a, 'key': f'{fmt(ys[1], 1)} − {fmt(ys[0], 1)} = {fmt(inc[0], 1)} t/ha. [1]'}
    parts = [
        lambda r: ('Calculate the increase in yield for each additional 50 kg/ha of nitrogen.', '; '.join(f'{rates[i]}-{rates[i + 1]}: {fmt(v, 1)} t' for i, v in enumerate(inc)), '[2]'),
        lambda r: ('Calculate the percentage increase in yield from 0 to 250 kg/ha.', f'{sgn(pct_change(ys[0], ys[-1]))}%', f'({fmt(ys[-1], 1)} − {fmt(ys[0], 1)}) ÷ {fmt(ys[0], 1)} × 100 [2]'),
        lambda r: ('Use the data to explain the idea of diminishing returns.', f'Each extra 50 kg adds less yield, falling from {fmt(inc[0], 1)} t to {fmt(inc[-1], 1)} t, as other factors such as water, other nutrients and the crop’s genetic potential become limiting.', '[2]'),
        lambda r: ('Explain the environmental impacts of applying fertiliser at high rates.', 'Unused nitrate leaches into groundwater and rivers, causing eutrophication and contaminating drinking water; nitrous oxide emissions; soil acidification.', '[3]'),
        lambda r: ('Suggest why farmers may apply more fertiliser than is economically worthwhile.', 'Subsidised fertiliser prices; lack of soil testing and advice; insurance against poor soils; belief that more is better.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t18c = T('Case study of the management of agricultural change in one country', 'case study of the management of agricultural change in one country')
B(t18c, {
    'terms': [
        ('Doi Moi', 'economic reforms in Vietnam from 1986 that gave farmers land-use rights and allowed markets, turning Vietnam into a major rice exporter'),
        ('Crop Intensification Programme (CIP)', 'Rwanda’s programme from 2007 combining land-use consolidation, improved seeds, fertiliser and extension services'),
        ('land-use consolidation (Rwanda)', 'farmers on neighbouring plots growing the same selected crop to gain economies of scale while keeping ownership'),
        ('minimum support price', 'a guaranteed price paid by the government for crops such as wheat and rice in India'),
        ('extension services', 'advice and training for farmers on new methods and technology'),
        ('food self-sufficiency', 'when a country produces enough food to meet its own needs'),
    ],
    'mcq': [
        ('Following Doi Moi reforms, Vietnam became', 'one of the world’s largest rice exporters', ['a major wheat importer', 'self-sufficient in oil palm only', 'a net food importer of rice'], '[1]'),
        ('Rwanda’s Crop Intensification Programme began in', '2007', ['1947', '1986', '2020'], '[1]'),
        ('India’s Green Revolution was supported by', 'subsidised inputs and minimum support prices', ['banning fertiliser', 'collectivisation', 'removing irrigation'], '[1]'),
        ('A criticism of Rwanda’s land-use consolidation is that', 'farmers lost freedom to choose crops and food diversity fell for some households', ['it raised no yields', 'it collectivised all land ownership', 'it banned fertiliser'], '[1]'),
    ],
    'explain': [
        ('Explain how government policy can manage agricultural change.', 'Land reform and tenure security; subsidies and guaranteed prices; research and extension services; credit; irrigation investment; market liberalisation; environmental regulation.', '[4]'),
        ('Explain why the management of agricultural change can create winners and losers.', 'Larger and richer farmers can adopt new inputs and gain; poorer farmers may fall into debt or lose land; consumers gain from cheaper food; regions with irrigation benefit more.', '[3]'),
        ('Explain how Vietnam’s Doi Moi reforms changed agriculture.', 'Collective farming ended; households got long-term land-use rights; they could sell output at market prices; investment in irrigation and new varieties rose; rice output and exports grew rapidly.', '[3]'),
    ],
    'claims': [
        ('Rwanda’s CIP raised yields of maize and beans.', True, 'Yields of target crops rose substantially after 2007.'),
        ('Agricultural change is always managed by governments.', False, 'Markets, TNCs, NGOs and farmers themselves drive much change.'),
        ('Vietnam was a rice importer before Doi Moi.', True, 'It imported rice in the early 1980s.'),
    ],
    'cs': [
        ('the management of agricultural change in one country', [
            ('Vietnam (Doi Moi reforms)', {'strategy': 'From 1986 collective farms were dissolved; 1988 Resolution 10 gave households control of land and output; 1993 Land Law gave 20-year transferable land-use rights; market prices and export liberalisation; investment in Mekong delta irrigation and improved rice varieties.',
                                           'evaluate': 'Rice production more than doubled and Vietnam became one of the top three rice exporters; rural poverty fell sharply; but inequality grew, intensive rice causes pollution and the Mekong delta faces salinisation and subsidence.'}),
            ('Rwanda (Crop Intensification Programme)', {'strategy': 'From 2007: land-use consolidation with farmers growing selected crops (maize, beans, wheat, cassava, Irish potatoes) by region; subsidised improved seed and fertiliser; extension officers; terracing and irrigation; land tenure registration.',
                                                         'evaluate': 'Large rises in yields and production of target crops and better food security indicators; but loss of crop diversity, some farmers forced to grow unsuitable crops, unequal benefits and dependence on subsidised inputs.'}),
            ('India (Green Revolution in Punjab)', {'strategy': 'From the mid-1960s: high-yielding wheat and rice, subsidised fertiliser and electricity for tube wells, minimum support prices and government procurement, agricultural universities and extension, credit.',
                                                    'evaluate': 'Punjab became India’s “bread basket” and national grain self-sufficiency was achieved; but groundwater is falling rapidly, soils are degraded, rice-wheat monoculture dominates, farmer debt and stubble burning causing air pollution in Delhi.'}),
        ], [
            ('describe how agricultural change was managed', 'strategy', 'Named policies, dates, actors and scale.'),
            ('evaluate the success of the management of agricultural change', 'evaluate', 'Economic, social and environmental outcomes with evidence.', 'assess how successfully agricultural change has been managed.'),
        ]),
    ],
    'essays': [
        ('the management of agricultural change has benefited richer farmers more than poorer farmers',
         ['Green Revolution inputs favoured farmers with land, irrigation and credit; subsidies and support prices benefit larger producers; land consolidation can marginalise smallholders.'],
         ['Doi Moi and China’s reforms reduced rural poverty widely; extension and subsidised inputs in Rwanda reached smallholders; consumers benefited from lower prices.'],
         'Richer farmers usually gain first and most, but well-designed policies can spread benefits widely.',
         ['inequality', 'subsidies', 'land tenure', 'poverty']),
    ],
})


CHAPTERS[18] = [t18a, t18b, t18c]


# ============================================================== CHAPTER 19: Manufacturing and related service industry

t19a = T('Factors affecting manufacturing location: Weber and changing locational factors', 'factors affecting manufacturing location weber changing locational factors')
B(t19a, {
    'terms': [
        ('Weber’s least-cost theory', 'a model (1909) proposing that industry locates where total transport costs of raw materials and finished products are lowest'),
        ('material index', 'the weight of localised raw materials divided by the weight of the finished product; above 1 suggests a location near raw materials'),
        ('weight-losing industry', 'an industry in which the product weighs less than the raw materials, such as steel or sugar refining'),
        ('footloose industry', 'an industry that is not tied to raw materials or markets and can locate in many places'),
        ('agglomeration economies', 'cost savings from locating close to other firms, such as shared suppliers, skilled labour and services'),
        ('ubiquitous material', 'a raw material available almost everywhere, such as water or air'),
    ],
    'mcq': [
        ('An industry with a material index of 3 is likely to locate', 'near its raw materials', ['near its market', 'anywhere', 'at a port only if index is below 1'], '[1]'),
        ('Soft drinks bottling is market-oriented because', 'it is weight-gaining: ubiquitous water is added', ['it loses weight', 'it uses iron ore', 'it needs coal'], '[1]'),
        ('Which factor has become more important for high-technology industry?', 'access to skilled labour and universities', ['proximity to coalfields', 'rivers for water power', 'iron ore deposits'], '[1]'),
        ('A limitation of Weber’s model is that it', 'assumes perfect knowledge and ignores labour quality, government policy and behaviour', ['includes too many factors', 'only applies to services', 'assumes transport costs are zero'], '[1]'),
    ],
    'explain': [
        ('Explain Weber’s least-cost theory of industrial location.', 'Firms seek the location with lowest total transport costs of materials and products; weight-losing industries locate near materials, weight-gaining near markets; labour cost savings or agglomeration may justify moving away from the least-transport-cost point.', '[4]'),
        ('Explain why transport costs are less important for manufacturing location today.', 'Containerisation, bulk carriers and better roads have cut costs; products are lighter and higher value; labour costs, skills, government incentives and markets now dominate.', '[3]'),
        ('Explain the importance of agglomeration economies.', 'Firms share suppliers, skilled labour pools, infrastructure and knowledge; clusters such as Silicon Valley or the Pearl River Delta attract further investment.', '[3]'),
    ],
    'claims': [
        ('Weber’s model assumes transport costs increase with distance and weight.', True, 'Costs are proportional to weight and distance in the model.'),
        ('Footloose industries must locate near raw materials.', False, 'They have freedom of location.'),
        ('Government incentives can override least-cost locations.', True, 'Grants, tax breaks and SEZs attract firms to particular places.'),
    ],
    'essays': [
        ('Weber’s least-cost theory is no longer useful in explaining the location of manufacturing industry',
         ['Transport costs are now small; labour, skills, markets, government policy, globalisation and behavioural factors dominate; most modern industry is footloose.'],
         ['Heavy, weight-losing industries (steel, cement, aluminium smelting near cheap power) still follow least-cost principles; the idea of cost minimisation remains central to TNC decisions.'],
         'The theory’s assumptions are outdated, but its central idea of minimising costs still helps explain some industries.',
         ['transport costs', 'labour', 'globalisation', 'government policy']),
    ],
})


@data(t19a)
def t19a_weber(r, D):
    ind = r.choice([('steel', 'iron ore', 'coking coal'), ('cement', 'limestone', 'clay'), ('aluminium', 'alumina', 'carbon anodes')])
    m1 = round(r.uniform(1.0, 2.0), 1)
    m2 = round(r.uniform(0.2, 1.0), 1)
    mi = (m1 + m2) / 1.0
    sites = {'site X (at the {0} mine)'.format(ind[1]): (0, r.randint(80, 200), r.randint(100, 300)),
             'site Y (at the {0} source)'.format(ind[2]): (r.randint(80, 200), 0, r.randint(100, 300)),
             'site Z (at the market)': (r.randint(100, 300), r.randint(100, 300), 0)}
    cost = {s: (m1 * a + m2 * b + 1.0 * c) for s, (a, b, c) in sites.items()}
    best = min(cost, key=cost.get)
    if sorted(cost.values())[0] == sorted(cost.values())[1]:
        return None
    stem = (f'Making 1 tonne of {ind[0]} uses {fmt(m1, 1)} t of {ind[1]} and {fmt(m2, 1)} t of {ind[2]}. Transport costs $1 per tonne-km for all goods. Distances (km) from each possible site to the {ind[1]} source, the {ind[2]} source and the market: ' +
            '; '.join(f'{s}: {a}, {b}, {c}' for s, (a, b, c) in sites.items()) + '.')
    if D == 1:
        o, a = mcq(r, fmt(mi, 1), [fmt(1 / mi, 2), fmt(m1, 1) if m1 != mi else fmt(mi + 1, 1), fmt(mi * 2, 1), fmt(mi - 0.5, 1) if mi > 0.6 else fmt(mi + 0.5, 1)])
        return {'stem': stem + ' What is the material index?', 'options': o, 'answer': a, 'key': f'({fmt(m1, 1)} + {fmt(m2, 1)}) ÷ 1 = {fmt(mi, 1)}. [1]'}
    parts = [
        lambda r: ('Calculate the material index and state what it suggests about location.', f'{fmt(mi, 1)}: ' + ('weight-losing, so a location near raw materials is favoured.' if mi > 1 else 'weight-gaining or neutral, so the market is favoured.'), '[2]'),
        lambda r: ('Calculate the total transport cost per tonne of product at each site and identify the least-cost site.', '; '.join(f'{s}: ${dp(v, 0)}' for s, v in cost.items()) + f'. Least cost: {best}', 'Σ(weight × distance) [3]'),
        lambda r: ('Suggest why the firm might not choose the least-cost site.', 'Cheaper or more skilled labour elsewhere; government grants or tax breaks; agglomeration economies; land availability; energy prices; political stability.', '[2]'),
        lambda r: ('Explain why Weber’s theory is less relevant to most modern industries.', 'Most products are light and high-value and use components rather than bulky materials; transport costs have fallen; labour, markets, skills and policy matter more; firms are not fully rational or informed.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t19b = T('Deindustrialisation, the informal sector and the global shift', 'deindustrialisation informal sector global shift')
B(t19b, {
    'terms': [
        ('deindustrialisation', 'the long-term decline of manufacturing employment and output in an area or country'),
        ('global shift', 'the movement of manufacturing from HICs to NICs and LICs, especially in Asia, since the 1970s'),
        ('informal sector', 'economic activity that is not registered, taxed or regulated by government, such as street trading'),
        ('location quotient (LQ)', 'the share of an industry in a region’s employment divided by its share in national employment; above 1 indicates specialisation'),
        ('rust belt', 'a region of declining heavy industry, such as parts of the US Midwest'),
        ('reshoring', 'returning manufacturing to the home country from abroad'),
    ],
    'mcq': [
        ('A region with a location quotient of 2.0 for textiles has', 'twice the national share of employment in textiles', ['half the national share', 'no textile industry', 'exactly the national share'], '[1]'),
        ('Which is a cause of deindustrialisation in HICs?', 'competition from lower-cost producers in Asia', ['rising wages in China only', 'rising demand for coal', 'new coalfields'], '[1]'),
        ('Dharavi in Mumbai is well known for its', 'informal-sector recycling, leather and pottery industries', ['car factories', 'oil refineries', 'aircraft industry'], '[1]'),
        ('The global shift of manufacturing has benefited most', 'China and other East and South-east Asian countries', ['Antarctica', 'Western Europe', 'the Sahara'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of deindustrialisation in HICs.', 'Competition from lower-wage countries; automation; exhaustion of resources (coal); old plant and infrastructure; high labour and land costs; strong currencies; shift of investment to services; TNC relocation.', '[4]'),
        ('Explain the impacts of deindustrialisation on a region.', 'Unemployment and loss of skilled jobs; out-migration and population decline; derelict land; multiplier effect reduces services; social problems; but cleaner environment and regeneration opportunities.', '[4]'),
        ('Explain why the informal sector is large in many LIC cities.', 'Rapid urban growth exceeds formal job creation; low skills; easy entry with little capital; regulations and taxes avoided; provides flexible income for migrants.', '[3]'),
    ],
    'claims': [
        ('Deindustrialisation means a country produces no manufactured goods.', False, 'Output may stay high with fewer workers through automation.'),
        ('The informal sector provides most jobs in some LICs.', True, 'In much of sub-Saharan Africa and South Asia most workers are informal.'),
        ('Manufacturing employment in the UK peaked in the 1960s.', True, 'It has fallen since, from about 9 million to under 3 million.'),
    ],
    'essays': [
        ('the global shift of manufacturing has had more advantages than disadvantages for LICs and NICs',
         ['Jobs, export earnings, FDI, skills and infrastructure; rapid growth in China, South Korea, Vietnam and Bangladesh; poverty reduction.'],
         ['Low wages and poor conditions (Rana Plaza 2013), pollution, dependence on TNCs, profits leaving the country, footloose plants relocating, inequality between regions.'],
         'For many countries the advantages have been large, but they depend on upgrading skills and protecting workers and the environment.',
         ['jobs', 'working conditions', 'TNCs', 'environment']),
    ],
})


@data(t19b)
def t19b_lq(r, D):
    nat_tot = r.choice([20, 25, 30, 32])  # million
    nat_man = round(nat_tot * r.uniform(0.08, 0.15), 1)
    regs = []
    for nm in ('Region A', 'Region B', 'Region C', 'Region D'):
        tot = round(r.uniform(1.0, 4.0), 2)
        man = round(tot * r.uniform(0.04, 0.25), 2)
        regs.append((nm, tot, man))
    ns = nat_man / nat_tot
    lq = [(m / t) / ns for _, t, m in regs]
    top = regs[lq.index(max(lq))][0]
    stem = (f'Table 19.2 shows employment (millions) in a country. National total {nat_tot}, of which manufacturing {fmt(nat_man, 1)}. Regions (total, manufacturing): ' +
            '; '.join(f'{n}: {fmt(t, 2)}, {fmt(m, 2)}' for n, t, m in regs) + '. LQ = (regional manufacturing ÷ regional total) ÷ (national manufacturing ÷ national total).')
    if D == 1:
        n, t, m = regs[0]
        o, a = mcq(r, fmt(lq[0], 2), [fmt((m / t), 2), fmt(1 / lq[0], 2), fmt(lq[0] * 2, 2), fmt(lq[1], 2) if abs(lq[1] - lq[0]) > 0.01 else fmt(lq[0] + 0.3, 2)])
        return {'stem': stem + ' What is the location quotient for manufacturing in Region A?', 'options': o, 'answer': a, 'key': f'({fmt(m, 2)} ÷ {fmt(t, 2)}) ÷ ({fmt(nat_man, 1)} ÷ {nat_tot}) = {fmt(lq[0], 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the location quotient for manufacturing in each region.', '; '.join(f'{g[0]}: {fmt(v, 2)}' for g, v in zip(regs, lq)), '[3]'),
        lambda r: ('Identify the region most specialised in manufacturing and state what its LQ shows.', f'{top}: LQ {fmt(max(lq), 2)}, so its share of manufacturing employment is {fmt(max(lq), 2)} times the national share.', '[1]'),
        lambda r: ('Suggest why regions with high LQs for manufacturing may be badly affected by deindustrialisation.', 'They depend heavily on one sector, so closures cause high unemployment, multiplier effects and out-migration; skills may not suit new jobs.', '[3]'),
        lambda r: ('Explain how a region could respond to deindustrialisation.', 'Regeneration of derelict land; attracting service and high-tech firms with grants and enterprise zones; retraining; improving infrastructure; tourism and heritage.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t19c = T('Government policies and the management of industrial change', 'government policies management of industrial change')
B(t19c, {
    'terms': [
        ('special economic zone (SEZ)', 'an area with tax breaks, relaxed regulations and good infrastructure to attract foreign investment, such as Shenzhen (1980)'),
        ('export processing zone (EPZ)', 'an industrial estate where imported components are assembled for export with tax and tariff exemptions'),
        ('industrial policy', 'government strategies to promote particular industries or regions'),
        ('import substitution industrialisation (ISI)', 'protecting domestic industries with tariffs so they can replace imports'),
        ('export-oriented industrialisation', 'promoting manufacturing for export, as in the Asian Tigers'),
        ('enterprise zone', 'an area where firms receive tax allowances and simplified planning to encourage investment'),
    ],
    'mcq': [
        ('Shenzhen became China’s first Special Economic Zone in', '1980', ['1949', '1997', '2010'], '[1]'),
        ('The Asian Tigers (South Korea, Taiwan, Hong Kong, Singapore) grew mainly through', 'export-oriented industrialisation', ['import substitution only', 'subsistence agriculture', 'oil exports'], '[1]'),
        ('Make in India, launched in 2014, aims to', 'increase manufacturing’s share of the economy and attract FDI', ['close all factories', 'ban foreign investment', 'promote subsistence farming'], '[1]'),
        ('A disadvantage of EPZs for host countries is', 'few links with local firms and low tax revenue', ['they create no jobs', 'they ban exports', 'they reduce FDI'], '[1]'),
    ],
    'explain': [
        ('Explain how governments attract manufacturing investment.', 'Tax holidays and grants; SEZs and EPZs with infrastructure; low tariffs on imported components; relaxed regulations; trained labour; political stability; trade agreements.', '[4]'),
        ('Explain the advantages and disadvantages of special economic zones.', 'Advantages: FDI, jobs, exports, technology transfer, infrastructure (Shenzhen grew from a fishing town to over 17 million people). Disadvantages: loss of tax revenue, exploitation of workers, pollution, regional inequality, enclaves with few local links.', '[4]'),
        ('Explain why governments may try to manage industrial decline.', 'To reduce unemployment and social problems, retrain workers, attract new industries, regenerate derelict areas and reduce regional inequality.', '[3]'),
    ],
    'claims': [
        ('Government policy has played a major role in the growth of NICs.', True, 'South Korea and China used planning, SEZs, credit and protection.'),
        ('Tax incentives always create long-term jobs.', False, 'Footloose firms may leave when incentives end.'),
        ('Import substitution was used by many Latin American countries in the 1950s-70s.', True, 'Tariffs protected domestic manufacturing in Brazil, Argentina and Mexico.'),
    ],
    'essays': [
        ('government policy is the most important factor in the growth of manufacturing in NICs',
         ['Planning, SEZs, export promotion, education and infrastructure investment drove growth in South Korea, Taiwan and China.'],
         ['Low labour costs, TNC investment, global markets, location on trade routes, culture and timing were also important; some policies failed (ISI in Latin America).'],
         'Policy was crucial in creating the conditions for growth, but it worked because it exploited global market opportunities and low-cost labour.',
         ['SEZs', 'TNCs', 'labour costs', 'education']),
    ],
})


@data(t19c)
def t19c_incent(r, D):
    grant = r.choice([20, 40, 60, 90, 150])  # $ million
    jobs = r.choice([500, 800, 1200, 2000, 3000])
    mult = round(r.uniform(1.4, 2.5), 1)
    yrs = r.choice([5, 10])
    cpj = grant * 1e6 / jobs
    tot = jobs * mult
    zone, wage = r.choice([('an SEZ in India', 3000), ('an EPZ in Kenya', 2500), ('an enterprise zone in north-east England', 34000), ('an industrial park in Vietnam', 4200), ('a free zone in Morocco', 5000)])
    stem = (f'A government gave a foreign car-parts company US${grant} million in grants and tax relief to open a factory in {zone}. The factory employs {nf(jobs)} people at an average wage of US${nf(wage)} a year. '
            f'The regional employment multiplier is estimated at {fmt(mult, 1)}. The company agreed to stay for at least {yrs} years.')
    if D == 1:
        o, a = mcq(r, f'US${nf(round(cpj))}', [f'US${nf(round(cpj / mult))}', f'US${nf(round(cpj * 10))}', f'US${nf(round(grant * 1e6 / (jobs * yrs)))}', f'US${nf(wage)}' if abs(wage - cpj) > 1 else f'US${nf(round(cpj / 2))}'])
        return {'stem': stem + ' What was the cost of the incentive per direct job?', 'options': o, 'answer': a, 'key': f'{grant} million ÷ {nf(jobs)} = US${nf(round(cpj))}. [1]'}
    parts = [
        lambda r: ('Calculate the incentive cost per direct job.', f'US${nf(round(cpj))}', f'{grant} 000 000 ÷ {nf(jobs)} [1]'),
        lambda r: ('Calculate the total number of jobs created, including indirect and induced jobs, and the cost per job.', f'{nf(round(tot))} jobs; US${nf(round(grant * 1e6 / tot))} per job', f'{nf(jobs)} × {fmt(mult, 1)} [2]'),
        lambda r: (f'Calculate the total wages paid to direct employees over {yrs} years.', f'US${nf(jobs * wage * yrs)}', f'{nf(jobs)} × {nf(wage)} × {yrs} [2]'),
        lambda r: ('Explain why the multiplier effect creates additional jobs.', 'The factory buys components and services from local suppliers, and employees spend wages in local shops, creating indirect and induced jobs; tax revenue funds services.', '[2]'),
        lambda r: ('Evaluate the use of such incentives to attract manufacturing.', 'They bring jobs, skills and investment, but are costly per job, may attract footloose firms that leave when incentives end, and may simply move jobs from other regions.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[19] = [t19a, t19b, t19c]


# ============================================================== CHAPTER 20: Sustainable energy supplies

MIX = {'Norway': [('hydro', 88), ('wind', 10), ('fossil fuels', 2)],
       'France': [('nuclear', 65), ('hydro', 12), ('wind and solar', 13), ('fossil fuels', 10)],
       'South Africa': [('coal', 82), ('nuclear', 4), ('wind and solar', 9), ('other', 5)],
       'Kenya': [('geothermal', 45), ('hydro', 22), ('wind', 18), ('fossil fuels and other', 15)],
       'China': [('coal', 60), ('hydro', 14), ('wind and solar', 16), ('nuclear', 5), ('other', 5)],
       'Brazil': [('hydro', 60), ('wind and solar', 20), ('biomass', 8), ('fossil fuels', 9), ('nuclear', 3)]}

t20a = T('Energy mix: non-renewable and renewable sources in HICs and LICs', 'energy mix non-renewable renewable sources in hics lics')
B(t20a, {
    'terms': [
        ('energy mix', 'the combination of different energy sources used by a country'),
        ('non-renewable energy', 'energy from finite sources such as coal, oil, natural gas and uranium'),
        ('renewable energy', 'energy from sources that are naturally replenished, such as solar, wind, hydro, geothermal and biomass'),
        ('fuelwood', 'wood used for cooking and heating, the main energy source for many rural households in LICs'),
        ('energy security', 'reliable access to affordable energy supplies'),
        ('primary energy', 'energy in its natural form before conversion, such as coal, crude oil and sunlight'),
    ],
    'mcq': [
        ('Kenya generates a large share of its electricity from', 'geothermal power in the Rift Valley', ['nuclear power', 'coal', 'tidal power'], 'Olkaria. [1]'),
        ('France generates most of its electricity from', 'nuclear power', ['coal', 'geothermal', 'oil'], '[1]'),
        ('In many rural areas of sub-Saharan Africa the main domestic energy source is', 'fuelwood and charcoal', ['nuclear power', 'natural gas', 'geothermal'], '[1]'),
        ('Fossil fuels still supply about what share of global primary energy?', 'about 80%', ['about 20%', 'about 50%', 'about 99%'], '[1]'),
    ],
    'explain': [
        ('Explain why energy mixes differ between HICs and LICs.', 'HICs use more commercial energy, oil, gas, nuclear and growing renewables, with large grids; LICs rely more on fuelwood and charcoal, with limited grids and imported oil; resources, wealth, technology and policy differ.', '[4]'),
        ('Explain the advantages and disadvantages of nuclear power.', 'Advantages: low carbon, reliable base load, small fuel volume, energy security. Disadvantages: high construction and decommissioning costs, radioactive waste, accident risk (Chernobyl 1986, Fukushima 2011), long build times.', '[4]'),
        ('Explain why the share of renewable electricity is growing.', 'Falling costs of solar and wind; climate targets (Paris 2015); energy security; government subsidies and auctions; improved storage and grids.', '[3]'),
    ],
    'claims': [
        ('Renewable energy sources produce no environmental impacts.', False, 'Dams flood land, wind farms affect landscapes and birds, biofuels use farmland.'),
        ('Hydroelectric power supplies most of Norway’s electricity.', True, 'Mountainous relief and high rainfall provide abundant hydro potential.'),
        ('LICs use more energy per person than HICs.', False, 'Energy use per person is far higher in HICs.'),
    ],
    'essays': [
        ('the energy mix of a country is determined mainly by its physical resources',
         ['Resources shape the mix: Norway’s hydro, Kenya’s geothermal, South Africa’s coal, Saudi oil.'],
         ['Wealth, technology, government policy (France’s nuclear programme after 1973, Germany’s Energiewende), climate commitments, prices and trade allow countries to import or develop alternatives.'],
         'Physical resources give advantages, but policy, wealth and technology increasingly determine the energy mix.',
         ['resources', 'policy', 'technology', 'climate change']),
    ],
})


@data(t20a)
def t20a_mix(r, D):
    a, b = r.sample(list(MIX), 2)
    ma = MIX[a]
    renew = {'hydro', 'wind', 'solar', 'wind and solar', 'geothermal', 'biomass'}
    ra = sum(v for n, v in ma if n in renew)
    rb = sum(v for n, v in MIX[b] if n in renew)
    tot = r.choice([30, 60, 120, 250])  # TWh
    stem = (f'Table 20.1 shows the approximate share (%) of electricity generation by source. {a}: ' + ', '.join(f'{n} {v}%' for n, v in ma) +
            f'. {b}: ' + ', '.join(f'{n} {v}%' for n, v in MIX[b]) + f'. {a} generates about {tot} TWh a year.')
    if D == 1:
        o, ans = mcq(r, f'{ra}%', [f'{100 - ra}%', f'{rb}%' if rb != ra else f'{ra // 2}%', f'{ma[0][1]}%' if ma[0][1] != ra else f'{min(99, ra + 10)}%', f'{max(1, ra - 7)}%'])
        return {'stem': stem + f' What percentage of {a}’s electricity comes from renewable sources?', 'options': o, 'answer': ans, 'key': f'Sum of renewable sources = {ra}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage of electricity from renewable sources in each country.', f'{a}: {ra}%; {b}: {rb}%', '[2]'),
        lambda r: (f'Calculate the angle of each sector for {a} if shown on a pie chart.', '; '.join(f'{n} {dp(v * 3.6, 0)}°' for n, v in ma), '% × 3.6 [2]'),
        lambda r: (f'Calculate the electricity generated from the largest source in {a}.', f'{dp(tot * ma[0][1] / 100, 1)} TWh from {ma[0][0]}', f'{tot} × {ma[0][1]}% [1]'),
        lambda r: (f'Suggest reasons for the energy mix of {a}.', _mix_reason(a), '[3]'),
        lambda r: ('Explain the problems of relying on one main source of electricity.', 'Vulnerable to supply shocks (droughts reduce hydro, fuel price rises, plant outages); less energy security; may lock in high emissions.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


def _mix_reason(c):
    return {'Norway': 'Mountainous relief, high rainfall and snowmelt and deep valleys give huge hydro potential; oil and gas are mostly exported.',
            'France': 'Few fossil fuel reserves; after the 1973 oil crisis the government built a large nuclear programme for energy security.',
            'South Africa': 'Large, cheap coal reserves in Mpumalanga; state utility Eskom built coal power stations; renewables are growing through auctions.',
            'Kenya': 'Geothermal resources in the Rift Valley (Olkaria); rivers for hydro; wind at Lake Turkana; few fossil fuels, so imported oil is expensive.',
            'China': 'Huge coal reserves and rapid industrial growth; large rivers for hydro (Three Gorges); world-leading investment in wind and solar to cut pollution and emissions.',
            'Brazil': 'Large rivers with high hydro potential (Itaipu, Belo Monte); strong wind in the north-east; sugar-cane biomass; offshore oil mainly used for transport.'}[c]


t20b = T('Factors affecting energy supply: physical, economic and political', 'factors affecting energy supply physical economic political')
B(t20b, {
    'terms': [
        ('capacity factor', 'the actual electricity generated by a plant over a period as a percentage of the maximum it could generate at full output'),
        ('installed capacity', 'the maximum power output of a power station, in megawatts (MW) or gigawatts (GW)'),
        ('intermittency', 'the variability of output from sources such as wind and solar, which depend on the weather'),
        ('levelised cost of electricity', 'the average cost of producing electricity over a plant’s lifetime, per MWh'),
        ('geopolitics of energy', 'the influence of international relations, conflicts and alliances on energy supply'),
        ('energy poverty', 'lack of access to modern energy services such as electricity and clean cooking'),
    ],
    'mcq': [
        ('A typical capacity factor for onshore wind farms is about', '25-40%', ['90-95%', '1-2%', '100%'], '[1]'),
        ('The 2022 Russian invasion of Ukraine affected energy supply in Europe mainly by', 'reducing natural gas imports from Russia and raising prices', ['increasing coal reserves', 'ending solar power', 'flooding hydro dams'], '[1]'),
        ('Which physical factor most limits hydroelectric power?', 'river flow, relief and reliability of rainfall', ['wind speed', 'sunshine hours', 'depth of oil reserves'], '[1]'),
        ('Nuclear power stations usually have capacity factors of about', '80-90%', ['10-20%', '30-40%', '100% always'], '[1]'),
    ],
    'explain': [
        ('Explain the physical factors that affect energy supply.', 'Geology determines fossil fuel and uranium reserves and geothermal potential; relief and rainfall for hydro; wind speeds and sunshine for wind and solar; tides; climate hazards.', '[4]'),
        ('Explain the economic factors that affect energy supply.', 'Cost of extraction and development; world prices; investment capital; technology; demand; subsidies and carbon prices; infrastructure (grids, pipelines).', '[4]'),
        ('Explain how political factors affect energy supply.', 'Conflict and sanctions (Russia 2022); OPEC decisions; government policy on nuclear, coal and renewables; climate agreements; nationalisation; public opposition.', '[3]'),
    ],
    'claims': [
        ('A wind farm with 100 MW capacity produces 100 MW all the time.', False, 'Output varies with wind; the capacity factor is often 25-40%.'),
        ('Falling costs have made solar power one of the cheapest sources of new electricity.', True, 'Solar module costs fell by about 90% between 2010 and 2020.'),
        ('Energy supply is affected only by physical resources.', False, 'Economic and political factors are often decisive.'),
    ],
    'essays': [
        ('political factors are now more important than physical factors in determining energy supply',
         ['Conflict and sanctions (2022), OPEC, government policy on nuclear (Germany’s phase-out, France’s programme), climate agreements and subsidies decide which resources are developed.'],
         ['Physical resources and geology remain the basis of supply (Gulf oil, Norway’s hydro, Kenya’s geothermal); climate and weather limit renewables.'],
         'Physical factors determine potential, but political and economic factors increasingly determine actual supply.',
         ['geology', 'conflict', 'policy', 'costs']),
    ],
})


CF_WHY = {'wind farm': 'Wind farm output depends on wind speed, which varies, and turbines stop in calm or very strong winds.',
          'solar farm': 'Solar output is zero at night and lower in cloudy weather and winter, so its capacity factor is lowest.',
          'nuclear plant': 'Nuclear plants run continuously at near full output except during maintenance and refuelling.',
          'gas plant': 'Gas plants are switched on and off to follow demand, so they often run below full capacity.'}


@data(t20b)
def t20b_cf(r, D):
    plants = [('wind farm', r.randint(50, 400), r.uniform(0.25, 0.40)), ('solar farm', r.randint(50, 500), r.uniform(0.12, 0.25)), ('nuclear plant', r.choice([1000, 1200, 1600, 3200]), r.uniform(0.80, 0.92)), ('gas plant', r.randint(400, 1200), r.uniform(0.40, 0.60))]
    pl = r.sample(plants, 3)
    pl = [(n, c, round(c * 8760 * f / 1000)) for n, c, f in pl]  # GWh
    cf = [g * 1000 / (c * 8760) * 100 for _, c, g in pl]
    stem = ('Table 20.2 shows the installed capacity (MW) and annual output (GWh) of three power stations: ' + '; '.join(f'{n}: {c} MW, {nf(g)} GWh' for n, c, g in pl) +
            '. There are 8760 hours in a year; 1 GWh = 1000 MWh. Capacity factor = actual output ÷ (capacity × 8760) × 100.')
    if D == 1:
        n, c, g = pl[0]
        o, a = mcq(r, f'{dp(cf[0])}%', [f'{dp(g / c * 100)}%', f'{dp(cf[0] / 10)}%', f'{dp(100 - cf[0])}%', f'{dp(cf[1])}%' if abs(cf[1] - cf[0]) > 0.5 else f'{dp(cf[0] + 15)}%'])
        return {'stem': stem + f' What is the capacity factor of the {n}?', 'options': o, 'answer': a, 'key': f'{nf(g * 1000)} ÷ ({c} × 8760) × 100 = {dp(cf[0])}%. [1]'}
    parts = [
        lambda r: ('Calculate the capacity factor of each power station.', '; '.join(f'{p[0]}: {dp(x)}%' for p, x in zip(pl, cf)), '[3]'),
        lambda r: ('Explain the differences in capacity factor.', ' '.join(CF_WHY[n] for n, _, _ in pl), '[3]'),
        lambda r: ('Calculate the installed solar capacity needed to generate the same annual output as the largest station, assuming a 15% capacity factor.', f'{nf(round(max(g for _, _, g in pl) * 1000 / (8760 * 0.15)))} MW', 'output ÷ (8760 × 0.15) [2]'),
        lambda r: ('Suggest how countries can manage the intermittency of renewable energy.', 'Battery and pumped storage; interconnectors with neighbouring countries; a mix of sources in different places; demand management; back-up gas or hydro.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t20c = T('Case study of the management of energy supply in one country', 'case study of the management of energy supply in one country')
B(t20c, {
    'terms': [
        ('Energiewende', 'Germany’s energy transition policy to replace nuclear and fossil fuels with renewables'),
        ('feed-in tariff', 'a guaranteed payment for electricity generated from renewable sources and fed into the grid'),
        ('Olkaria geothermal complex', 'a group of geothermal power stations in Kenya’s Rift Valley near Lake Naivasha'),
        ('Three Gorges Dam', 'the world’s largest hydroelectric power station by capacity (22.5 GW) on the Yangtze River, China'),
        ('energy transition', 'the shift from fossil fuels to low-carbon energy sources'),
        ('off-grid solar', 'solar panels and batteries supplying homes not connected to the national grid'),
    ],
    'mcq': [
        ('Germany closed its last nuclear power stations in', '2023', ['1990', '2005', '2040'], '[1]'),
        ('Germany’s 2000 Renewable Energy Sources Act introduced', 'feed-in tariffs for renewable electricity', ['a ban on wind power', 'new coal subsidies only', 'nuclear expansion'], '[1]'),
        ('The Lake Turkana Wind Power project in Kenya has a capacity of about', '310 MW', ['3 MW', '3100 MW', '31 GW'], '[1]'),
        ('The Three Gorges Dam displaced about', '1.3 million people', ['13 000 people', '130 people', '13 million people'], '[1]'),
    ],
    'explain': [
        ('Explain why governments try to manage energy supply.', 'To ensure energy security, keep prices affordable, meet growing demand, reduce emissions to meet climate targets, reduce air pollution and widen access to electricity.', '[3]'),
        ('Explain the challenges of an energy transition.', 'Intermittency and need for storage and grids; high investment costs; job losses in coal regions; public opposition to wind farms and pylons; energy prices; dependence on imports during transition.', '[4]'),
        ('Explain how off-grid solar can improve energy access in LICs.', 'Cheap, modular panels and pay-as-you-go schemes (e.g. M-KOPA in Kenya) reach rural homes far from the grid, replacing kerosene and allowing lighting, phone charging and small businesses.', '[3]'),
    ],
    'claims': [
        ('Renewables supplied over half of Germany’s electricity in 2023-24.', True, 'Wind and solar grew rapidly under the Energiewende.'),
        ('Kenya relies mainly on coal for electricity.', False, 'Geothermal and hydro dominate.'),
        ('Large dams have only positive impacts.', False, 'They displace people, trap sediment and affect ecosystems.'),
    ],
    'cs': [
        ('the management of energy supply in one country', [
            ('Germany (Energiewende)', {'strategy': 'Renewable Energy Sources Act (2000) with feed-in tariffs, later auctions; nuclear phase-out after Fukushima (completed 2023); coal phase-out planned by 2038; expansion of onshore and offshore wind and rooftop solar; new north-south transmission lines.',
                                        'evaluate': 'Renewables rose from about 6% of electricity in 2000 to over 50% by 2023; but electricity prices are among the highest in Europe, coal use stayed high for years, dependence on Russian gas was exposed in 2022, and grid expansion lags.'}),
            ('Kenya', {'strategy': 'Geothermal development at Olkaria by KenGen; Lake Turkana Wind Power (310 MW); hydro on the Tana River; Last Mile Connectivity Project to extend the grid; support for off-grid solar companies such as M-KOPA.',
                       'evaluate': 'About 90% of electricity is from renewables and access rose from under 30% (2013) to around 75%; but costs remain high for the poor, geothermal projects displaced Maasai communities, and droughts reduce hydro output.'}),
            ('China', {'strategy': 'Large hydro (Three Gorges, 22.5 GW); world’s largest investment in wind, solar and nuclear; ultra-high-voltage lines from the west to eastern cities; air pollution action plans; carbon peak by 2030 and neutrality by 2060 targets.',
                       'evaluate': 'China leads the world in renewable capacity and air quality in cities improved after 2013; but coal still supplies about 60% of electricity and new coal plants are approved; Three Gorges displaced 1.3 million people.'}),
        ], [
            ('describe how energy supply is managed', 'strategy', 'Named policies, projects, dates and scale.'),
            ('evaluate the extent to which the management of energy supply is sustainable', 'evaluate', 'Economic, social and environmental evidence.', 'assess how sustainable the management of energy supply has been.'),
        ]),
    ],
    'essays': [
        ('it is impossible for a country to achieve both energy security and sustainability',
         ['Fossil fuels give reliable, controllable supply; intermittent renewables need back-up; Germany’s reliance on Russian gas and coal during transition.'],
         ['Domestic renewables increase security by reducing imports (Kenya, Brazil hydro); storage, grids and diverse mixes deal with intermittency; efficiency reduces demand.'],
         'There are trade-offs in the short term, but a diverse low-carbon mix can achieve both in the long term.',
         ['renewables', 'imports', 'intermittency', 'policy']),
    ],
})


CHAPTERS[20] = [t20a, t20b, t20c]


# ============================================================== CHAPTER 21: Environmental degradation

t21a = T('Pollution of air, water and land', 'pollution of air water land')
B(t21a, {
    'terms': [
        ('PM2.5', 'fine particulate matter less than 2.5 micrometres across, which penetrates deep into the lungs'),
        ('WHO air quality guideline', 'the WHO (2021) recommended limits for pollutants, including an annual mean of 5 µg/m³ and a 24-hour mean of 15 µg/m³ for PM2.5'),
        ('point source pollution', 'pollution from a single identifiable source, such as a factory outfall'),
        ('non-point (diffuse) source pollution', 'pollution from many scattered sources, such as fertiliser run-off from farmland'),
        ('photochemical smog', 'a haze formed when sunlight reacts with nitrogen oxides and hydrocarbons from vehicles, producing ozone'),
        ('land contamination', 'pollution of soil by toxic substances such as heavy metals, oil or industrial waste'),
    ],
    'mcq': [
        ('The WHO (2021) guideline for annual mean PM2.5 is', '5 µg/m³', ['50 µg/m³', '500 µg/m³', '0.5 µg/m³'], '[1]'),
        ('Winter smog in Delhi is made worse by', 'temperature inversions trapping pollutants and crop-stubble burning in Punjab and Haryana', ['strong winds', 'monsoon rain', 'sea breezes'], '[1]'),
        ('Which is an example of non-point source pollution?', 'nitrate run-off from many farms', ['a pipe discharging factory waste', 'an oil tanker spill', 'a single chimney'], '[1]'),
        ('Mexico City’s air pollution is trapped mainly because', 'the city lies in a basin surrounded by mountains with frequent inversions', ['it is on the coast', 'it has no vehicles', 'it lies at sea level'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of urban air pollution in LIC and NIC cities.', 'Rapid growth in vehicle numbers with old engines and poor fuel; industry and power stations burning coal; domestic burning of wood, charcoal and waste; construction dust; weak regulation; inversions and basin sites trap pollutants.', '[4]'),
        ('Explain the difference between point and non-point source pollution and why the latter is harder to control.', 'Point sources come from one identifiable outlet; non-point sources are diffuse (run-off from farms and roads), so they are hard to monitor, regulate and treat.', '[3]'),
        ('Explain how land becomes contaminated.', 'Industrial waste disposal, mining spoil, leaking landfill, pesticide use, oil spills and e-waste recycling deposit heavy metals and toxins in soil.', '[3]'),
    ],
    'claims': [
        ('Air pollution is a problem only in LICs.', False, 'Many HIC cities exceed WHO guidelines, though levels are generally lower.'),
        ('Temperature inversions make air pollution worse.', True, 'Warm air above cool air traps pollutants near the ground.'),
        ('Pollution can cross international borders.', True, 'Acid rain, haze from Indonesian fires and river pollution cross borders.'),
    ],
    'essays': [
        ('economic development inevitably leads to environmental pollution',
         ['Industrialisation and urbanisation in China, India and earlier in the UK caused severe air and water pollution; consumption and waste rise with income.'],
         ['The environmental Kuznets curve suggests pollution falls at higher incomes with regulation and cleaner technology (London, Los Angeles, Beijing since 2013); policy can decouple growth from pollution.'],
         'Pollution often rises in early development, but it is not inevitable: policy and technology can reduce it.',
         ['industrialisation', 'regulation', 'technology', 'Kuznets curve']),
    ],
})


@data(t21a)
def t21a_pm(r, D):
    city, base = r.choice([('Delhi', 100), ('Lahore', 95), ('Dhaka', 80), ('Beijing', 40), ('Lagos', 45), ('Jakarta', 40), ('London', 10), ('Mexico City', 22)])
    pat = [1.6, 1.3, 1.0, 0.8, 0.7, 0.5, 0.4, 0.4, 0.6, 1.1, 1.6, 1.8]
    vals = [max(3, round(base * p * r.uniform(0.8, 1.2))) for p in pat]
    m = mean(vals)
    over = sum(1 for v in vals if v > 15)
    ratio = m / 5
    stem = f'Table 21.1 shows the monthly mean PM2.5 concentration (µg/m³) in {city}: ' + ', '.join(f'{MON[i]} {v}' for i, v in enumerate(vals)) + '. The WHO annual guideline is 5 µg/m³ and the 24-hour guideline is 15 µg/m³.'
    if D == 1:
        o, a = mcq(r, f'{dp(ratio, 1)} times', [f'{dp(m, 1)} times', f'{dp(m / 15, 1)} times', f'{dp(max(vals) / 5, 1)} times', f'{dp(ratio / 2, 1)} times'])
        return {'stem': stem + ' How many times the WHO annual guideline is the annual mean?', 'options': o, 'answer': a, 'key': f'mean {dp(m, 1)} ÷ 5 = {dp(ratio, 1)} times. [1]'}
    hi = MON[vals.index(max(vals))]
    parts = [
        lambda r: ('Calculate the annual mean PM2.5 concentration and express it as a multiple of the WHO annual guideline.', f'{dp(m, 1)} µg/m³; {dp(ratio, 1)} times the guideline', f'{sum(vals)} ÷ 12; ÷ 5 [2]'),
        lambda r: ('State the number of months in which the monthly mean exceeded the 24-hour guideline.', f'{over} months', '[1]'),
        lambda r: (f'Suggest reasons why PM2.5 was highest in {hi}.', 'Winter temperature inversions and low wind speeds trap pollutants; more burning for heating; seasonal crop-residue burning; no rain to wash particles out.', '[3]'),
        lambda r: ('Explain the effects of PM2.5 on human health.', 'Fine particles penetrate deep into the lungs and bloodstream, causing asthma, bronchitis, heart disease, stroke and lung cancer, and reducing life expectancy.', '[2]'),
        lambda r: ('Suggest how the city could reduce PM2.5 concentrations.', 'Cleaner vehicle fuels and emission standards; public transport and electric buses; closing or cleaning coal plants; controls on construction dust and waste burning; alternatives to stubble burning.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t21b = T('Causes and consequences of environmental degradation', 'causes consequences of environmental degradation')
B(t21b, {
    'terms': [
        ('environmental degradation', 'the deterioration of the environment through depletion of resources, destruction of ecosystems and pollution'),
        ('biochemical oxygen demand (BOD)', 'the amount of oxygen used by micro-organisms to break down organic matter in water; high BOD indicates organic pollution'),
        ('dissolved oxygen (DO)', 'the amount of oxygen dissolved in water, needed by fish and other aquatic life'),
        ('oxygen sag curve', 'the fall and recovery of dissolved oxygen downstream of a source of organic pollution'),
        ('tragedy of the commons', 'the overuse of a shared resource because individuals gain from using it while costs are shared by all'),
        ('ecological footprint', 'the area of productive land and water needed to supply a population’s resources and absorb its wastes'),
    ],
    'mcq': [
        ('Downstream of a sewage outfall, dissolved oxygen in a river usually', 'falls and then gradually recovers', ['rises immediately', 'stays constant', 'falls to zero permanently'], '[1]'),
        ('Fish such as trout generally need dissolved oxygen of at least about', '6-7 mg/l', ['0.1 mg/l', '1 mg/l', '50 mg/l'], '[1]'),
        ('The tragedy of the commons helps explain', 'overfishing and overgrazing of shared resources', ['why private gardens are well kept', 'why the sea is salty', 'why deserts are hot'], '[1]'),
        ('The Aral Sea shrank to about what fraction of its 1960 area by 2010?', 'about 10%', ['about 90%', 'about 50%', 'it grew'], '[1]'),
    ],
    'explain': [
        ('Explain the causes of environmental degradation.', 'Population growth and rising consumption; industrialisation and urbanisation; poverty forcing overuse of resources; weak regulation and enforcement; market failure where pollution is not priced; inappropriate technology.', '[4]'),
        ('Explain the consequences of water pollution for ecosystems.', 'Oxygen depletion from organic waste kills fish; eutrophication causes algal blooms and dead zones; toxins and heavy metals bioaccumulate in food chains; loss of biodiversity.', '[4]'),
        ('Explain the tragedy of the commons.', 'Each user of a common resource gains the full benefit of extra use but shares the cost of degradation with others, so without regulation the resource is overused and degraded.', '[3]'),
    ],
    'claims': [
        ('Environmental degradation affects only the environment, not the economy.', False, 'It reduces fisheries, farm yields, tourism and health, costing economies heavily.'),
        ('Poverty can be both a cause and a consequence of environmental degradation.', True, 'The poor may overuse resources and also suffer most from degradation.'),
        ('Rivers can recover from organic pollution downstream.', True, 'Aeration and decomposition restore oxygen levels (the oxygen sag curve).'),
    ],
    'essays': [
        ('poverty is the main cause of environmental degradation',
         ['The poor depend directly on natural resources and may overuse land, forests and fuelwood; they lack capital for conservation.'],
         ['Consumption in wealthy countries, industrial pollution, TNC activity, commercial agriculture and weak governance cause far greater total degradation; ecological footprints are highest in HICs.'],
         'Poverty contributes locally, but wealth, consumption and industrial activity are the larger causes globally.',
         ['consumption', 'industry', 'governance', 'ecological footprint']),
    ],
})


@data(t21b)
def t21b_sag(r, D):
    dist = [-1, 0, 2, 5, 10, 20, 35, 50]
    up = round(r.uniform(8.5, 10.0), 1)
    mn = round(r.uniform(1.5, 5.0), 1)
    at = r.choice([5, 10])
    do = []
    for d in dist:
        if d < 0:
            do.append(up)
        elif d <= at:
            do.append(round(up - (up - mn) * (d / at) ** 0.7, 1))
        else:
            do.append(round(mn + (up - 0.5 - mn) * (1 - math.exp(-(d - at) / r.uniform(10, 18))), 1))
    lowest = min(do)
    ld = dist[do.index(lowest)]
    below = [d for d, v in zip(dist, do) if v < 6]
    riv = r.choice(['a river below a sewage outfall in an Indian city', 'the River Thames below a treatment works in the 1950s', 'a river downstream of a palm-oil mill in Malaysia', 'a river below a paper mill'])
    stem = (f'Fig. 21.2 shows dissolved oxygen (mg/l) along {riv}; distance in km from the outfall (negative = upstream): ' + ', '.join(f'{d} km: {fmt(v, 1)}' for d, v in zip(dist, do)) +
            '. Many fish need at least 6 mg/l.')
    if D == 1:
        o, a = mcq(r, f'{fmt(up - lowest, 1)} mg/l', [f'{fmt(lowest, 1)} mg/l', f'{fmt(up, 1)} mg/l', f'{fmt(do[-1], 1)} mg/l' if do[-1] != up - lowest else f'{fmt(up + lowest, 1)} mg/l', f'{fmt((up - lowest) / 2, 2)} mg/l'])
        return {'stem': stem + ' By how much did dissolved oxygen fall from upstream to its lowest point?', 'options': o, 'answer': a, 'key': f'{fmt(up, 1)} − {fmt(lowest, 1)} = {fmt(up - lowest, 1)} mg/l. [1]'}
    parts = [
        lambda r: ('Calculate the fall in dissolved oxygen from upstream to the lowest value, and the percentage fall.', f'{fmt(up - lowest, 1)} mg/l; {dp((up - lowest) / up * 100)}%', '[2]'),
        lambda r: ('Identify the stretch of river where fish needing 6 mg/l could not survive.', ('from about ' + str(below[0]) + ' km to ' + str(below[-1]) + ' km') if below else 'None: oxygen never fell below 6 mg/l.', '[1]'),
        lambda r: ('Explain the shape of the oxygen sag curve.', f'Organic waste raises BOD, so bacteria decomposing it use up oxygen faster than it is replaced, reaching a minimum at about {ld} km; downstream, as the waste is broken down and the water is re-aerated by turbulence and photosynthesis, oxygen recovers.', '[3]'),
        lambda r: ('Explain the consequences of the pollution for people living downstream.', 'Fish deaths reduce fisheries and food; water unsafe to drink, bathe and irrigate; waterborne diseases such as cholera; odour; treatment costs.', '[2]'),
        lambda r: ('Suggest how the pollution could be reduced.', 'Build or upgrade sewage treatment; enforce discharge limits with fines; charge polluters; aerate the river; connect informal settlements to sewers.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t21c = T('Environmental degradation and its effects on human health and livelihoods', 'environmental degradation its effects on human health livelihoods')
B(t21c, {
    'terms': [
        ('environmental health', 'the effects of the physical environment, including pollution and sanitation, on human health'),
        ('waterborne disease', 'an illness caused by micro-organisms in contaminated water, such as cholera and typhoid'),
        ('bioaccumulation', 'the build-up of toxins such as mercury or pesticides in organisms over time and up food chains'),
        ('livelihood', 'the means by which people secure the necessities of life, such as farming, fishing or wage labour'),
        ('e-waste', 'discarded electronic equipment, often processed informally in LICs, releasing lead, mercury and dioxins'),
        ('premature death', 'death before the expected age, often used to measure the health impacts of pollution'),
    ],
    'mcq': [
        ('The WHO estimates that ambient and household air pollution together cause about how many premature deaths a year?', 'about 7 million', ['about 7000', 'about 70 000', 'about 700 million'], '[1]'),
        ('Minamata disease in Japan was caused by', 'mercury from a factory accumulating in fish', ['lead in petrol', 'arsenic in groundwater', 'radiation'], '[1]'),
        ('Arsenic in groundwater from tube wells has affected millions of people in', 'Bangladesh and West Bengal', ['Iceland', 'Norway', 'New Zealand'], '[1]'),
        ('Agbogbloshie in Accra, Ghana became known for', 'informal e-waste recycling', ['coral reefs', 'geothermal power', 'wheat farming'], '[1]'),
    ],
    'explain': [
        ('Explain how environmental degradation affects human health.', 'Air pollution causes respiratory and heart disease; contaminated water spreads cholera and diarrhoea; toxins (mercury, lead, arsenic) cause poisoning and birth defects; degraded land reduces nutrition.', '[4]'),
        ('Explain how environmental degradation affects livelihoods.', 'Declining fish stocks, soil erosion and salinisation reduce incomes; tourism falls; ill health reduces ability to work; costs of treatment; forced migration.', '[3]'),
        ('Explain why the poor are often most affected by environmental degradation.', 'They live near polluting industries, dumps and in informal settlements without sanitation; depend directly on natural resources; cannot afford treatment or protection.', '[3]'),
    ],
    'claims': [
        ('Household air pollution from cooking fires is a major health risk in LICs.', True, 'Burning wood, charcoal and dung indoors causes respiratory disease, especially among women and children.'),
        ('Environmental health problems are confined to LICs.', False, 'Flint, Michigan (lead in water, 2014) and air pollution in European cities show HICs are affected.'),
        ('Toxins can become more concentrated at higher levels of food chains.', True, 'This biomagnification affected people eating fish at Minamata.'),
    ],
    'essays': [
        ('the health effects of environmental degradation are more serious than its effects on livelihoods',
         ['Millions of premature deaths a year from air pollution and unsafe water; long-term poisoning (Minamata, arsenic in Bangladesh).'],
         ['Loss of livelihoods (fisheries, soils, tourism) affects far more people, deepening poverty, which itself harms health; the two are closely linked.'],
         'Health and livelihood effects reinforce each other; health effects are the most direct, but livelihood loss is more widespread.',
         ['air pollution', 'water', 'poverty', 'fisheries']),
    ],
})


@data(t21c)
def t21c_rates(r, D):
    regs = []
    for nm in ('City A', 'City B', 'City C', 'City D'):
        pop = round(r.uniform(1.0, 30.0), 1)
        rate = r.uniform(20, 160)
        deaths = round(pop * 1e6 * rate / 1e5)
        regs.append((nm, pop, deaths))
    rts = [d / (p * 1e6) * 1e5 for _, p, d in regs]
    hi = regs[rts.index(max(rts))][0]
    stem = ('Table 21.3 shows the estimated number of premature deaths attributed to air pollution in one year in four cities, with their populations: ' +
            '; '.join(f'{n}: {nf(d)} deaths, population {fmt(p, 1)} million' for n, p, d in regs) + '.')
    if D == 1:
        o, a = mcq(r, hi, [g[0] for g in regs if g[0] != hi])
        return {'stem': stem + ' Which city has the highest death rate per 100 000 people?', 'options': o, 'answer': a, 'key': '; '.join(f'{g[0]} {dp(x, 1)}' for g, x in zip(regs, rts)) + ' per 100 000. [1]'}
    parts = [
        lambda r: ('Calculate the death rate per 100 000 people for each city.', '; '.join(f'{g[0]}: {dp(x, 1)}' for g, x in zip(regs, rts)), 'deaths ÷ population × 100 000 [3]'),
        lambda r: ('Explain why rates are a better basis for comparison than total deaths.', 'Cities have very different populations, so totals reflect size; rates show the risk to an individual.', '[2]'),
        lambda r: ('Suggest reasons why air pollution death rates differ between cities.', 'Differences in pollution levels (traffic, industry, coal use, domestic burning), site and climate (basins, inversions), age structure, health care and regulation.', '[3]'),
        lambda r: ('Suggest why these estimates are uncertain.', 'Deaths are modelled from exposure-response relationships, not counted; monitoring stations are few; other causes of disease such as smoking overlap.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[21] = [t21a, t21b, t21c]


# ============================================================== CHAPTER 22: The management of a degraded environment

t22a = T('Strategies to restore degraded environments', 'strategies to restore degraded environments')
B(t22a, {
    'terms': [
        ('restoration', 'returning a degraded environment towards its original condition'),
        ('rehabilitation', 'improving a degraded environment so that it can be used productively, though not necessarily as it was'),
        ('remediation', 'removing or neutralising pollutants from contaminated land or water'),
        ('polluter pays principle', 'the principle that those who cause pollution should pay the cost of managing it'),
        ('phytoremediation', 'using plants to absorb or break down pollutants in soil and water'),
        ('brownfield site', 'previously developed land, often derelict and contaminated, that can be redeveloped'),
    ],
    'mcq': [
        ('The Rhine Action Programme was launched after', 'the Sandoz chemical spill at Basel in 1986', ['the Chernobyl accident', 'the Aral Sea crisis', 'the 2004 tsunami'], '[1]'),
        ('Atlantic salmon returned to the Rhine in the 1990s after', 'improved water quality and fish passes', ['the river was dammed', 'more industry', 'salt was added'], '[1]'),
        ('Phytoremediation involves', 'using plants to remove pollutants', ['burning soil', 'adding more chemicals', 'building sea walls'], '[1]'),
        ('Which is an example of rehabilitation rather than restoration?', 'turning a former quarry into a park and lake', ['returning a forest to its original species', 'reintroducing extinct species', 'removing all human use'], '[1]'),
    ],
    'explain': [
        ('Explain the strategies used to restore degraded rivers.', 'Treatment of sewage and industrial effluent; discharge limits and monitoring; removal of contaminated sediment; re-naturalising channels and floodplains; fish passes; international cooperation on shared rivers.', '[4]'),
        ('Explain how degraded land can be restored.', 'Remediation of contaminated soils; capping landfill; replanting native vegetation; terracing and erosion control; reintroduction of species; reuse of brownfield sites.', '[3]'),
        ('Explain the factors that influence the success of restoration.', 'Funding; political will and legislation; enforcement; stakeholder cooperation; scale and severity of degradation; time; monitoring.', '[3]'),
    ],
    'claims': [
        ('Restoration can always return an environment to its original state.', False, 'Some changes, such as extinctions, are irreversible.'),
        ('Restoration is usually more expensive than preventing degradation.', True, 'Cleaning up after damage generally costs much more.'),
        ('International cooperation is needed to restore shared rivers.', True, 'Pollution from upstream countries affects those downstream.'),
    ],
    'essays': [
        ('legislation is the most effective way to restore degraded environments',
         ['Laws and enforcement (Clean Air Act 1956, EU Water Framework Directive, polluter pays) forced industries to clean up and drove river and air recovery.'],
         ['Funding, technology (treatment works), community involvement, market incentives and international cooperation are also needed; laws without enforcement fail (Ganga Action Plan).'],
         'Legislation provides the framework, but restoration also needs funding, technology and cooperation.',
         ['regulation', 'funding', 'technology', 'stakeholders']),
    ],
})


@data(t22a)
def t22a_restore(r, D):
    yrs = [1985, 1990, 1995, 2000, 2005, 2010]
    do0 = round(r.uniform(3.0, 5.0), 1)
    do = [do0]
    for _ in yrs[1:]:
        do.append(round(min(11, do[-1] + r.uniform(0.3, 1.2)), 1))
    sp0 = r.randint(5, 15)
    sp = [sp0]
    for _ in yrs[1:]:
        sp.append(sp[-1] + r.randint(2, 10))
    cost = r.choice([5, 8, 12, 15])  # € billion
    riv = r.choice(['the River Rhine at the Dutch-German border', 'the River Thames in London', 'the River Mersey', 'the River Seine below Paris'])
    stem = (f'Table 22.1 shows mean dissolved oxygen (mg/l) and the number of fish species recorded in {riv} during a clean-up programme costing about €{cost} billion: ' +
            '; '.join(f'{y}: {fmt(d, 1)} mg/l, {s} species' for y, d, s in zip(yrs, do, sp)) + '.')
    pc = pct_change(sp[0], sp[-1])
    if D == 1:
        o, a = mcq(r, f'{sgn(pc)}%', [f'{sgn(sp[-1] / sp[0] * 100)}%', f'{sgn(sp[-1] - sp[0], 0)}%', f'{sgn(pc / 2)}%', f'{sgn(pct_change(do[0], do[-1]))}%'])
        return {'stem': stem + ' What was the percentage increase in fish species from 1985 to 2010?', 'options': o, 'answer': a, 'key': f'({sp[-1]} − {sp[0]}) ÷ {sp[0]} × 100 = {sgn(pc)}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage increase in fish species and in dissolved oxygen between 1985 and 2010.', f'species {sgn(pc)}%; oxygen {sgn(pct_change(do[0], do[-1]))}%', '[2]'),
        lambda r: ('Calculate the cost of the programme per additional fish species recorded.', f'about €{dp(cost * 1000 / (sp[-1] - sp[0]), 0)} million per species', f'{cost} billion ÷ {sp[-1] - sp[0]} [2]'),
        lambda r: ('Explain why the number of fish species increased.', 'Better sewage treatment and controls on industrial discharges reduced organic pollution and toxins, so dissolved oxygen rose above the levels needed by sensitive species; fish passes and habitat restoration allowed recolonisation.', '[3]'),
        lambda r: ('Suggest why the number of fish species is a limited measure of the success of the clean-up.', 'It ignores fish numbers, health and invertebrates; sampling effort may have increased; some species are introduced; contaminants in sediment may remain; other aims such as recreation and drinking water matter too.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t22b = T('Stakeholders and conflicts in environmental management', 'stakeholders conflicts in environmental management')
B(t22b, {
    'terms': [
        ('stakeholder', 'an individual, group or organisation with an interest in a decision or place'),
        ('conflict matrix', 'a table showing whether the interests of pairs of stakeholders are in conflict, compatible or neutral'),
        ('environmental impact assessment (EIA)', 'a formal study of the likely environmental effects of a project before a decision is made'),
        ('NGO', 'a non-governmental organisation, such as Greenpeace or WWF, that campaigns or works on issues'),
        ('trade-off', 'accepting less of one benefit to gain more of another'),
        ('participatory management', 'involving local people and other stakeholders in decision-making'),
    ],
    'mcq': [
        ('Which stakeholder is most likely to oppose stricter discharge limits on a river?', 'factory owners discharging effluent', ['downstream fishing communities', 'conservation NGOs', 'water supply companies'], '[1]'),
        ('An environmental impact assessment is carried out', 'before a project is approved', ['only after a disaster', 'only by tourists', 'only in LICs'], '[1]'),
        ('The Narmada dam projects in India were opposed mainly by', 'displaced communities and NGOs such as Narmada Bachao Andolan', ['electricity companies', 'the state government', 'farmers receiving irrigation'], '[1]'),
        ('A conflict matrix is used to', 'identify where stakeholders’ interests clash', ['measure river flow', 'calculate GDP', 'map soil types'], '[1]'),
    ],
    'explain': [
        ('Explain why conflicts arise in the management of degraded environments.', 'Stakeholders have different priorities (profit, jobs, health, conservation); costs and benefits fall on different groups; uncertainty over causes; who pays; short-term vs long-term interests.', '[4]'),
        ('Explain the role of NGOs in environmental management.', 'Campaign and raise awareness; monitor pollution; take legal action; fund and run projects; represent local communities; but may lack power and funding.', '[3]'),
        ('Explain why involving local stakeholders can improve environmental management.', 'Local knowledge; greater acceptance and compliance; fairer sharing of benefits; long-term commitment and monitoring.', '[3]'),
    ],
    'claims': [
        ('All stakeholders benefit equally from environmental restoration.', False, 'Some, such as polluting firms, bear costs while others benefit.'),
        ('Governments often act as both regulators and stakeholders.', True, 'They may own industries or seek growth while also enforcing rules.'),
        ('Conflicts between stakeholders can never be resolved.', False, 'Negotiation, compensation and participatory planning can resolve many conflicts.'),
    ],
    'essays': [
        ('conflict between stakeholders is the main obstacle to managing degraded environments',
         ['Opposition from industry, farmers and governments seeking growth delays action; disputes over cost-sharing on international rivers.'],
         ['Lack of funding, technology, scientific understanding and enforcement capacity can be greater obstacles; some schemes succeed despite conflict through legislation.'],
         'Conflict is a major obstacle, but funding and governance often determine whether it can be overcome.',
         ['stakeholders', 'funding', 'governance', 'scale']),
    ],
})


@data(t22b)
def t22b_matrix(r, D):
    sh = ['factory owners', 'local fishers', 'water company', 'conservation NGO', 'city council']
    pairs = [(a, b) for i, a in enumerate(sh) for b in sh[i + 1:]]
    vals = {}
    for a, b in pairs:
        if 'factory owners' in (a, b) and b in ('local fishers', 'conservation NGO', 'water company'):
            vals[(a, b)] = 'conflict'
        else:
            vals[(a, b)] = r.choice(['compatible', 'compatible', 'neutral', 'conflict'])
    nc = sum(1 for v in vals.values() if v == 'conflict')
    per = {s: sum(1 for (a, b), v in vals.items() if v == 'conflict' and s in (a, b)) for s in sh}
    most = max(per, key=per.get)
    if sorted(per.values())[-1] == sorted(per.values())[-2]:
        return None
    stem = ('Table 22.2 is a conflict matrix for stakeholders in a scheme to clean up a polluted river. Pairs: ' + '; '.join(f'{a} / {b}: {v}' for (a, b), v in vals.items()) + '.')
    if D == 1:
        o, a = mcq(r, cap(most), [cap(s) for s in sh if s != most])
        return {'stem': stem + ' Which stakeholder is involved in the most conflicts?', 'options': o, 'answer': a, 'key': '; '.join(f'{s} {n}' for s, n in per.items()) + '. [1]'}
    parts = [
        lambda r: ('Calculate the number and percentage of stakeholder pairs that are in conflict.', f'{nc} of {len(pairs)} pairs = {dp(nc / len(pairs) * 100)}%', '[2]'),
        lambda r: ('Identify the stakeholder involved in the most conflicts and suggest why.', f'{cap(most)} ({per[most]} conflicts): ' + ('cleaning up would require costly treatment of its effluent, while the others gain from cleaner water.' if most == 'factory owners' else 'its aims differ from several other groups.'), '[2]'),
        lambda r: ('Suggest how the conflicts between the factory owners and other stakeholders could be reduced.', 'Grants or low-interest loans for treatment plants; phased discharge limits; polluter-pays charges used for clean-up; negotiation through a river basin committee; publicising pollution data.', '[3]'),
        lambda r: ('Explain why the water company and conservation NGO may sometimes be in conflict.', 'The water company may want to abstract more water or build reservoirs and treatment works, which conflicts with conservation of river habitats and flows.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t22c = T('Case study of the management of a degraded environment and evaluation of success', 'case study of the management of a degraded environment evaluation of success')
B(t22c, {
    'terms': [
        ('Namami Gange', 'an Indian government programme launched in 2014 to clean and restore the River Ganges'),
        ('ProAire', 'a series of air quality management programmes in Mexico City since 1990'),
        ('Hoy No Circula', 'a Mexico City scheme (1989) banning cars from driving on one weekday according to their number plate'),
        ('Thames Tideway Tunnel', 'a 25 km “super sewer” under London, completed in the mid-2020s, to stop sewage overflows into the Thames'),
        ('combined sewer overflow', 'a point where sewage and rainwater overflow into a river when sewers are full'),
        ('success criteria', 'measurable indicators, such as pollutant levels or species numbers, used to judge whether management has worked'),
    ],
    'mcq': [
        ('The River Thames was declared “biologically dead” in', 'the late 1950s', ['the 1990s', '2020', '1800'], '[1]'),
        ('Mexico City’s air quality management includes', 'Hoy No Circula driving restrictions and cleaner fuels', ['building more coal power stations', 'banning public transport', 'clearing forests'], '[1]'),
        ('The Ganga Action Plan was first launched in', '1986', ['1947', '2014', '2024'], 'Namami Gange followed in 2014. [1]'),
        ('A major remaining problem in the Thames before the Tideway Tunnel was', 'sewage overflows after heavy rain', ['radioactive waste', 'oil spills every day', 'salt from roads in summer'], '[1]'),
    ],
    'explain': [
        ('Explain why it is difficult to evaluate the success of managing a degraded environment.', 'Success depends on the criteria chosen; long time scales; changes may be due to other factors (industrial decline, weather); limited monitoring data; different stakeholders judge success differently.', '[4]'),
        ('Explain why the clean-up of the Ganges has been difficult.', 'Huge population and untreated sewage from many cities; industrial effluent (tanneries at Kanpur); religious practices; weak enforcement; many states and agencies; low flows from abstraction.', '[3]'),
        ('Explain how Mexico City has managed air pollution.', 'Unleaded and cleaner fuels; catalytic converters; vehicle inspection and Hoy No Circula; Metrobus and cycle schemes; moving industries and refinery closure (1991); monitoring and alerts.', '[3]'),
    ],
    'claims': [
        ('The Thames now supports over 100 species of fish.', True, 'About 125 species have been recorded since the clean-up.'),
        ('Mexico City’s air quality has not changed since 1990.', False, 'Lead, sulphur dioxide and carbon monoxide fell sharply, though ozone and PM2.5 remain problems.'),
        ('Namami Gange has completely cleaned the Ganges.', False, 'Water quality has improved in places but many stretches still fail standards.'),
    ],
    'cs': [
        ('the management of a degraded environment', [
            ('the River Thames, London', {'strategy': 'From the 1960s new sewage treatment works (Beckton, Crossness) and controls on industrial discharges; Thames Water and the Environment Agency monitoring; Thames Tideway Tunnel (about £4.5 billion) to capture combined sewer overflows.',
                                          'evaluate': 'From biologically dead in 1957 to about 125 fish species, seals and seahorses; but sewage overflows still occurred in heavy rain, microplastics and road run-off remain, and costs fall on water bills.'}),
            ('Mexico City (air pollution)', {'strategy': 'ProAire programmes since 1990: unleaded petrol (from 1990), catalytic converters, vehicle inspection, Hoy No Circula, closure of the 18 de Marzo refinery (1991), Metrobus (2005), Ecobici, pollution alerts.',
                                             'evaluate': 'Lead, SO₂ and CO fell sharply and ozone peaks fell; but ozone and PM2.5 still often exceed WHO guidelines, car numbers keep rising and Hoy No Circula encouraged people to buy second cars.'}),
            ('the River Ganges, India (Ganga Action Plan and Namami Gange)', {'strategy': 'Ganga Action Plan (1986), then Namami Gange (2014, about US$3 billion): sewage treatment plants, closure or treatment of tannery effluent, riverfront development, crematoria improvements, river surface cleaning, afforestation.',
                                                                            'evaluate': 'Treatment capacity has increased and dissolved oxygen improved at some sites; but faecal coliforms remain far above bathing standards in many places, plants operate below capacity, and enforcement and coordination are weak.'}),
        ], [
            ('describe the strategies used to manage the degraded environment', 'strategy', 'Named strategies, organisations, dates and costs.'),
            ('evaluate the success of the management', 'evaluate', 'Measured outcomes against criteria; continuing problems.', 'evaluate the extent to which the management has been successful.'),
        ]),
    ],
    'essays': [
        ('the management of degraded environments is more successful in HICs than in LICs and NICs',
         ['HICs have funding, technology, strong regulation and monitoring: Thames and Rhine recoveries.'],
         ['Mexico City and Beijing have reduced pollution substantially; HICs still have problems (Thames overflows); LICs often face larger populations and faster growth rather than lower competence.'],
         'Resources and governance favour HICs, but NICs show that strong policy can bring major improvements.',
         ['funding', 'regulation', 'population pressure', 'evaluation criteria']),
    ],
})


CHAPTERS[22] = [t22a, t22b, t22c]


# ============================================================== CHAPTER 23: Trade flows and trading patterns

t23a = T('Global trade patterns, commodities and terms of trade', 'global trade patterns commodities terms of trade')
B(t23a, {
    'terms': [
        ('terms of trade', 'the ratio of a country’s export prices to its import prices, usually expressed as an index: export price index ÷ import price index × 100'),
        ('primary commodity', 'an unprocessed raw material or crop such as copper, coffee or cocoa'),
        ('commodity dependence', 'when a large share of a country’s export earnings comes from one or a few primary commodities'),
        ('balance of trade', 'the difference between the value of a country’s exports and imports of goods'),
        ('visible and invisible trade', 'trade in physical goods, and trade in services such as tourism, banking and insurance'),
        ('value added', 'the increase in value of a product at each stage of processing or manufacture'),
    ],
    'mcq': [
        ('If export prices rise by 10% and import prices rise by 20%, the terms of trade', 'worsen', ['improve', 'stay the same', 'double'], '[1]'),
        ('Zambia’s exports are dominated by', 'copper', ['coffee', 'oil', 'cars'], 'Copper is about 70% of exports. [1]'),
        ('Côte d’Ivoire and Ghana together produce about what share of the world’s cocoa?', 'about 60%', ['about 6%', 'about 95%', 'about 25%'], '[1]'),
        ('Which is an example of invisible trade?', 'tourism spending by foreign visitors', ['exports of copper', 'imports of oil', 'exports of cars'], '[1]'),
    ],
    'explain': [
        ('Explain why many LICs experience declining terms of trade.', 'They export primary commodities whose prices are volatile and tend to fall relative to manufactured goods; demand is price-inelastic; many producers compete; synthetic substitutes; tariff escalation discourages processing.', '[4]'),
        ('Describe the pattern of global trade.', 'Dominated by HICs and East Asia; most trade is between HICs and within regions (EU, East Asia, North America); China is the largest exporter of goods; LDCs account for about 1% of world merchandise exports.', '[4]'),
        ('Explain the problems of commodity dependence.', 'Export earnings fluctuate with world prices; government revenues and debt repayments are unpredictable; little value added at home; vulnerability to shocks and to “Dutch disease”.', '[3]'),
    ],
    'claims': [
        ('Commodity prices are stable from year to year.', False, 'They are highly volatile, e.g. copper and oil.'),
        ('Trade in services is growing faster than trade in goods.', True, 'Digital, financial and business services trade has expanded rapidly.'),
        ('Processing raw materials before export increases value added.', True, 'Chocolate is worth much more than cocoa beans.'),
    ],
    'essays': [
        ('dependence on primary commodities is the main reason why some countries gain little from world trade',
         ['Volatile and falling commodity prices, declining terms of trade, little value added (Zambia’s copper, Burundi’s coffee).'],
         ['Tariff escalation, trade rules, lack of infrastructure, conflict, weak institutions and the power of TNCs also limit gains; some commodity exporters gain greatly (Botswana diamonds, Gulf oil).'],
         'Commodity dependence is a key factor, but governance and the structure of trade rules determine whether countries benefit.',
         ['terms of trade', 'value added', 'tariffs', 'governance']),
    ],
})


@data(t23a)
def t23a_tot(r, D):
    yrs = [2015, 2017, 2019, 2021, 2023]
    ex = [100] + [round(100 * r.uniform(0.7, 1.4)) for _ in yrs[1:]]
    im = [100] + [round(100 + i * r.uniform(2, 8)) for i in range(1, len(yrs))]
    tot = [e / i * 100 for e, i in zip(ex, im)]
    cty = r.choice(['Zambia (copper)', 'Côte d’Ivoire (cocoa)', 'Ethiopia (coffee)', 'Chile (copper)', 'Ghana (gold and cocoa)'])
    stem = (f'Table 23.1 shows export and import price indices (2015 = 100) for {cty}: ' + '; '.join(f'{y}: exports {e}, imports {i}' for y, e, i in zip(yrs, ex, im)) +
            '. Terms of trade = export price index ÷ import price index × 100.')
    k = r.randint(1, 4)
    if D == 1:
        o, a = mcq(r, dp(tot[k]), [dp(im[k] / ex[k] * 100), dp(ex[k] - im[k] + 100, 0), dp(tot[k] + 10), dp(tot[k] - 10), dp(tot[k] + 5)])
        return {'stem': stem + f' What was the terms of trade index in {yrs[k]}?', 'options': o, 'answer': a, 'key': f'{ex[k]} ÷ {im[k]} × 100 = {dp(tot[k])}. [1]'}
    best = yrs[tot.index(max(tot[1:]))] if max(tot[1:]) > 100 else None
    parts = [
        lambda r: ('Calculate the terms of trade index for each year.', '; '.join(f'{y}: {dp(t)}' for y, t in zip(yrs, tot)), '[3]'),
        lambda r: ('State the years when the terms of trade were favourable compared with 2015.', ', '.join(str(y) for y, t in zip(yrs[1:], tot[1:]) if t > 100) or 'None: the index was at or below 100 in all later years.', '[1]'),
        lambda r: ('Explain what a falling terms of trade means for the country.', 'It must export more to pay for the same quantity of imports, reducing real income, government revenue and the ability to repay debt.', '[2]'),
        lambda r: ('Suggest why the export price index fluctuated.', 'Commodity prices depend on world demand (Chinese growth), supply from other producers, weather and disease affecting harvests, speculation and exchange rates.', '[2]'),
        lambda r: ('Suggest how the country could reduce its vulnerability to changes in the terms of trade.', 'Diversify exports; process commodities at home to add value; develop manufacturing and services; stabilisation funds; Fairtrade and long-term contracts.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t23b = T('Trade blocs, the WTO and fair trade', 'trade blocs wto fair trade')
B(t23b, {
    'terms': [
        ('trade bloc', 'a group of countries that reduce barriers to trade between them, such as the EU, USMCA, ASEAN or ECOWAS'),
        ('World Trade Organization (WTO)', 'the international organisation (1995) that sets rules for trade and settles disputes between its members'),
        ('tariff', 'a tax on imported goods'),
        ('quota', 'a limit on the quantity of a good that can be imported'),
        ('Fairtrade', 'a certification scheme guaranteeing producers a minimum price and a social premium, with standards on labour and the environment'),
        ('Fairtrade premium', 'an extra sum paid to producer cooperatives to invest in community or business projects'),
    ],
    'mcq': [
        ('The African Continental Free Trade Area (AfCFTA) began trading in', '2021', ['1957', '1995', '2035'], '[1]'),
        ('The WTO replaced GATT in', '1995', ['1945', '1973', '2008'], '[1]'),
        ('A customs union differs from a free trade area because members', 'also have a common external tariff', ['have a common currency', 'have no trade', 'have tariffs between each other'], '[1]'),
        ('The Fairtrade minimum price protects farmers when', 'the market price falls below the minimum', ['the market price is very high', 'they sell to local markets only', 'they grow nothing'], '[1]'),
    ],
    'explain': [
        ('Explain the advantages of trade blocs for member countries.', 'Larger markets without tariffs; economies of scale; more foreign investment; increased competition and efficiency; stronger bargaining power in negotiations.', '[3]'),
        ('Explain why trade blocs may disadvantage non-member countries.', 'Common external tariffs make their exports less competitive (trade diversion); subsidies such as the EU’s Common Agricultural Policy depress world prices.', '[3]'),
        ('Explain the benefits and limitations of Fairtrade.', 'Benefits: minimum price, premium for schools, clinics and equipment, stable contracts, better conditions. Limitations: small share of world trade, certification costs, benefits may not reach labourers, consumers pay more.', '[4]'),
    ],
    'claims': [
        ('The WTO has removed all barriers to trade.', False, 'Many tariffs, subsidies and non-tariff barriers remain.'),
        ('Fairtrade products account for a large share of world trade in coffee.', False, 'Only a small share is sold on Fairtrade terms.'),
        ('Tariff escalation discourages processing in LICs.', True, 'Higher tariffs on processed goods than on raw materials favour exports of unprocessed commodities.'),
    ],
    'essays': [
        ('fair trade is more effective than free trade in helping LICs benefit from world trade',
         ['Fairtrade guarantees minimum prices and premiums, improving livelihoods for certified farmers (cocoa cooperatives in Ghana such as Kuapa Kokoo).'],
         ['Fairtrade is small-scale; free trade and access to large markets drove growth in East Asia; removal of HIC subsidies and tariff escalation would benefit far more people.'],
         'Fair trade helps particular producers, but reforms to trade rules and market access have greater potential impact.',
         ['minimum price', 'market access', 'subsidies', 'scale']),
    ],
})


@data(t23b)
def t23b_ft(r, D):
    mp = round(r.uniform(1.10, 2.40), 2)
    fmin = round(r.choice([1.40, 1.60, 1.80]), 2)
    prem = round(r.choice([0.20, 0.30, 0.40]), 2)
    lb = r.choice([2000, 3500, 5000, 8000])
    paid = max(mp, fmin) + prem
    inc_ft = paid * lb
    inc_m = mp * lb
    gain = inc_ft - inc_m
    stem = (f'A coffee cooperative member in Peru sells {nf(lb)} lb of coffee. The world market price is US${fmt(mp, 2)} per lb. The Fairtrade minimum price is US${fmt(fmin, 2)} per lb (or the market price if higher), plus a Fairtrade premium of US${fmt(prem, 2)} per lb.')
    if D == 1:
        o, a = mcq(r, f'US${fmt(paid, 2)}', [f'US${fmt(fmin, 2)}', f'US${fmt(mp + prem, 2)}' if mp + prem != paid else f'US${fmt(fmin + mp, 2)}', f'US${fmt(mp, 2)}', f'US${fmt(fmin + prem + mp, 2)}'])
        return {'stem': stem + ' What price per lb, including the premium, does the cooperative receive under Fairtrade?', 'options': o, 'answer': a, 'key': f'max({fmt(mp, 2)}, {fmt(fmin, 2)}) + {fmt(prem, 2)} = US${fmt(paid, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the income from selling the coffee on the open market and under Fairtrade.', f'market US${nf(round(inc_m))}; Fairtrade US${nf(round(inc_ft))}', f'{nf(lb)} × {fmt(mp, 2)}; {nf(lb)} × {fmt(paid, 2)} [2]'),
        lambda r: ('Calculate the percentage increase in income under Fairtrade.', f'{sgn(gain / inc_m * 100)}%', '(Fairtrade − market) ÷ market × 100 [2]'),
        lambda r: ('Suggest how the cooperative could use the Fairtrade premium.', 'Community projects such as schools, clinics and clean water; business investment such as processing equipment, organic conversion and training to improve quality.', '[2]'),
        lambda r: ('Explain why the benefits of Fairtrade may be limited.', 'Cooperatives can sell only part of their crop on Fairtrade terms; certification costs; hired labourers may not benefit; small share of the market; premium shared across members.', '[3]'),
        lambda r: ('Explain why coffee farmers often receive a small share of the retail price.', 'Most value is added by roasting, branding and retailing in consumer countries; traders and TNCs take margins; farmers sell unprocessed beans.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t23c = T('Participation in world trade by HICs and LICs', 'participation in world trade by hics lics')
B(t23c, {
    'terms': [
        ('least developed countries (LDCs)', 'a UN category of low-income countries with severe structural barriers to development, about 45 countries'),
        ('export concentration', 'the extent to which a country’s exports depend on a small number of products'),
        ('trade openness', 'the value of exports plus imports as a percentage of GDP'),
        ('Everything But Arms (EBA)', 'an EU scheme giving LDCs duty-free, quota-free access for all exports except arms'),
        ('global value chain', 'the stages of production of a good spread across several countries'),
        ('trade deficit', 'when the value of imports exceeds the value of exports'),
    ],
    'mcq': [
        ('LDCs account for about what share of world merchandise exports?', 'about 1%', ['about 10%', 'about 25%', 'about 50%'], '[1]'),
        ('The largest exporter of goods in the world in the 2020s is', 'China', ['the UK', 'Nigeria', 'Brazil'], '[1]'),
        ('Which factor most limits LIC participation in world trade?', 'poor infrastructure and dependence on a few primary products', ['too many ports', 'very high wages', 'excess manufacturing capacity'], '[1]'),
        ('Bangladesh’s exports are dominated by', 'ready-made garments', ['oil', 'cars', 'copper'], 'About 80% of export earnings. [1]'),
    ],
    'explain': [
        ('Explain why HICs dominate world trade.', 'They produce high-value manufactured goods and services; have large markets, capital, technology and infrastructure; TNC headquarters; trade rules and institutions shaped by them.', '[4]'),
        ('Explain the barriers to LIC participation in world trade.', 'Dependence on low-value primary products; poor transport and port infrastructure; landlocked locations; tariffs and non-tariff barriers (standards) in HIC markets; HIC subsidies; lack of finance and skills.', '[4]'),
        ('Explain how some LICs and NICs have increased their participation in world trade.', 'Export-oriented manufacturing (Bangladesh garments, Vietnam electronics); joining global value chains; trade agreements and preferential access (EBA, AGOA); investment in ports and SEZs.', '[3]'),
    ],
    'claims': [
        ('Landlocked countries face higher trade costs.', True, 'They depend on neighbours’ transport routes and ports.'),
        ('All LICs have trade surpluses.', False, 'Many run deficits, importing fuel, food and manufactured goods.'),
        ('Joining global value chains can help countries industrialise.', True, 'Vietnam and Bangladesh grew through assembly and garment exports.'),
    ],
    'essays': [
        ('the pattern of world trade benefits HICs more than LICs',
         ['HICs and East Asia capture most trade value; LICs export low-value commodities with declining terms of trade; subsidies and tariff escalation.'],
         ['Many LICs and NICs have gained from trade (China, Vietnam, Bangladesh); preferential access schemes; South-South trade is growing; consumers in LICs gain from cheaper imports.'],
         'The current pattern favours HICs, but countries that diversify into manufacturing and services can benefit greatly.',
         ['commodities', 'value chains', 'trade rules', 'NICs']),
    ],
})


@data(t23c)
def t23c_conc(r, D):
    cty, items = r.choice([('Bangladesh', ['ready-made garments', 'jute goods', 'leather', 'fish and shrimps', 'other']),
                           ('Zambia', ['copper', 'cobalt', 'maize and sugar', 'tobacco', 'other']),
                           ('Ethiopia', ['coffee', 'oilseeds', 'cut flowers', 'gold', 'other']),
                           ('Nigeria', ['crude oil', 'natural gas', 'cocoa', 'sesame seeds', 'other'])])
    top = r.randint(55, 85)
    rest = 100 - top
    a = r.randint(1, rest - 3)
    b = r.randint(1, rest - a - 2)
    c = r.randint(1, rest - a - b - 1)
    shares = [top, a, b, c, rest - a - b - c]
    totv = r.choice([5, 12, 20, 45, 60])  # US$ billion
    gdp = round(totv * r.uniform(3, 8))
    imp = round(totv * r.uniform(0.9, 1.6), 1)
    stem = (f'Table 23.3 shows the share (%) of export earnings by product for {cty} in one year: ' + ', '.join(f'{n} {s}%' for n, s in zip(items, shares)) +
            f'. Total exports were US${totv} billion, imports US${fmt(imp, 1)} billion and GDP US${gdp} billion.')
    bal = totv - imp
    if D == 1:
        o, an = mcq(r, f'US${dp(totv * top / 100, 1)} billion', [f'US${dp(totv * (100 - top) / 100, 1)} billion', f'US${top} billion', f'US${dp(totv * top / 10, 1)} billion', f'US${dp(gdp * top / 100, 1)} billion'])
        return {'stem': stem + f' What was the value of {items[0]} exports?', 'options': o, 'answer': an, 'key': f'{totv} × {top}% = US${dp(totv * top / 100, 1)} billion. [1]'}
    parts = [
        lambda r: (f'Calculate the value of {items[0]} exports.', f'US${dp(totv * top / 100, 1)} billion', '[1]'),
        lambda r: ('Calculate the balance of trade and trade openness (exports + imports as % of GDP).', f'balance {sgn(bal)} billion US$; openness {dp((totv + imp) / gdp * 100)}%', f'{totv} − {fmt(imp, 1)}; ({totv} + {fmt(imp, 1)}) ÷ {gdp} × 100 [3]'),
        lambda r: ('Explain the risks of such a high export concentration.', f'Earnings depend on the price and demand for {items[0]}; a fall in world prices or demand, or a supply shock, sharply reduces income, revenue and the ability to pay for imports.', '[3]'),
        lambda r: ('Suggest how the country could diversify its exports.', 'Process raw materials domestically; develop other manufacturing and services; invest in infrastructure, education and SEZs; seek trade agreements; promote tourism and horticulture.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[23] = [t23a, t23b, t23c]


# ============================================================== CHAPTER 24: Debt and aid

t24a = T('The causes and consequences of international debt', 'causes consequences of international debt')
B(t24a, {
    'terms': [
        ('external debt', 'money owed by a country’s government, firms and people to foreign lenders'),
        ('debt service', 'the repayments of capital and interest on debt in a year'),
        ('debt service ratio', 'debt service as a percentage of export earnings; above about 20% is often regarded as unsustainable'),
        ('structural adjustment programmes (SAPs)', 'conditions imposed by the IMF and World Bank in the 1980s-90s, such as cutting public spending and privatising industries, in return for loans'),
        ('debt crisis', 'a situation in which a country cannot repay its debts, as in Latin America in 1982'),
        ('debt-to-GDP ratio', 'a country’s debt as a percentage of its annual GDP'),
    ],
    'mcq': [
        ('The 1980s debt crisis began when', 'Mexico announced it could not service its debt in 1982', ['the WTO was founded', 'Germany reunified', 'the euro was launched'], '[1]'),
        ('A country with debt service of $2 billion and exports of $8 billion has a debt service ratio of', '25%', ['4%', '40%', '2.5%'], '[1]'),
        ('Rising US interest rates in the late 1970s and early 1980s', 'increased the cost of servicing variable-rate loans for LICs', ['cancelled LIC debt', 'reduced oil prices to zero', 'had no effect'], '[1]'),
        ('Zambia defaulted on its external debt in', '2020', ['1950', '1970', '2010'], 'It was the first African country to default during the COVID-19 pandemic. [1]'),
    ],
    'explain': [
        ('Explain the causes of the debt crisis of the 1980s.', 'Banks recycled petrodollars as cheap loans in the 1970s; oil price rises increased import bills; interest rates rose sharply in 1979-81; commodity prices fell; loans were spent on unproductive projects or lost to corruption; currencies fell.', '[4]'),
        ('Explain the consequences of high debt for an LIC.', 'Debt repayments divert money from health, education and infrastructure; austerity under SAPs; reduced investment; pressure to export commodities; reliance on new loans; social unrest.', '[4]'),
        ('Explain why debt problems have returned in some LICs since 2015.', 'Borrowing from bond markets and China at higher interest rates; falling commodity prices; the COVID-19 pandemic; rising US interest rates and a strong dollar in 2022-23.', '[3]'),
    ],
    'claims': [
        ('All borrowing harms development.', False, 'Loans for productive investment can raise growth and repayment capacity.'),
        ('Structural adjustment programmes often reduced spending on health and education.', True, 'Austerity cut public services in many countries.'),
        ('Debt service ratios are measured relative to imports.', False, 'They are measured relative to export earnings.'),
    ],
    'essays': [
        ('the causes of international debt lie mainly outside the indebted countries',
         ['Oil shocks, rising world interest rates, falling commodity prices, irresponsible lending by banks and later bond markets; strong dollar.'],
         ['Domestic factors: corruption, poor investment choices, weak tax systems, conflict, excessive borrowing by governments; some countries with similar shocks avoided crisis.'],
         'External shocks usually trigger debt crises, but domestic policies decide how vulnerable countries are.',
         ['interest rates', 'commodity prices', 'governance', 'lenders']),
    ],
})


@data(t24a)
def t24a_dsr(r, D):
    cs = []
    for nm in ('Country A', 'Country B', 'Country C', 'Country D'):
        ex = r.choice([2, 4, 6, 8, 12, 15, 20])
        ds = round(ex * r.uniform(0.05, 0.45), 2)
        gdp = round(ex * r.uniform(3, 6))
        debt = round(gdp * r.uniform(0.3, 1.1))
        cs.append((nm, ex, ds, gdp, debt))
    dsr = [ds / ex * 100 for _, ex, ds, _, _ in cs]
    dg = [d / g * 100 for _, _, _, g, d in cs]
    hi = cs[dsr.index(max(dsr))][0]
    stem = ('Table 24.1 shows data (US$ billion) for four low-income countries: ' + '; '.join(f'{n}: exports {ex}, debt service {fmt(ds, 2)}, GDP {g}, external debt {d}' for n, ex, ds, g, d in cs) +
            '. Debt service ratio = debt service ÷ exports × 100; above 20% is often considered unsustainable.')
    if D == 1:
        o, a = mcq(r, hi, [c[0] for c in cs if c[0] != hi])
        return {'stem': stem + ' Which country has the highest debt service ratio?', 'options': o, 'answer': a, 'key': '; '.join(f'{c[0]} {dp(x)}%' for c, x in zip(cs, dsr)) + '. [1]'}
    unsus = [c[0] for c, x in zip(cs, dsr) if x > 20]
    parts = [
        lambda r: ('Calculate the debt service ratio of each country and identify those above 20%.', '; '.join(f'{c[0]}: {dp(x)}%' for c, x in zip(cs, dsr)) + '. Above 20%: ' + (', '.join(unsus) or 'none'), '[3]'),
        lambda r: ('Calculate the debt-to-GDP ratio of each country.', '; '.join(f'{c[0]}: {dp(x)}%' for c, x in zip(cs, dg)), '[2]'),
        lambda r: ('Explain why the debt service ratio is a useful measure of the burden of debt.', 'Debt is repaid in foreign currency, mainly earned from exports, so the ratio shows the share of foreign earnings used for repayments rather than imports or investment.', '[2]'),
        lambda r: ('Explain how a high debt burden affects development.', 'Less money for health, education and infrastructure; austerity; lower investment and growth; dependence on new loans and conditions from lenders.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t24b = T('Types of aid: bilateral, multilateral, tied and NGO aid', 'types of aid bilateral multilateral tied ngo aid')
B(t24b, {
    'terms': [
        ('official development assistance (ODA)', 'government aid to promote the development and welfare of LICs and MICs, measured by the OECD'),
        ('bilateral aid', 'aid given directly from one government to another'),
        ('multilateral aid', 'aid given through international organisations such as the World Bank, UN agencies or the EU'),
        ('tied aid', 'aid given on condition that the recipient spends it on goods and services from the donor country'),
        ('NGO aid', 'aid given by non-governmental organisations such as Oxfam or WaterAid, often for small-scale projects'),
        ('0.7% target', 'the UN target (1970) for donor countries to give 0.7% of their gross national income as ODA'),
    ],
    'mcq': [
        ('The UN target for ODA is', '0.7% of donor GNI', ['7% of donor GNI', '0.07% of donor GNI', '70% of donor tax revenue'], '[1]'),
        ('Which countries have regularly met the 0.7% target?', 'Norway, Sweden, Luxembourg and Denmark', ['the USA and Japan', 'China and India', 'no countries ever'], '[1]'),
        ('Aid given through the World Bank is an example of', 'multilateral aid', ['bilateral aid', 'tied aid only', 'remittances'], '[1]'),
        ('A criticism of tied aid is that', 'it may not provide the best-value goods and benefits donor firms', ['it is too flexible', 'it is never spent', 'it is always given in cash'], '[1]'),
    ],
    'explain': [
        ('Compare bilateral and multilateral aid.', 'Bilateral aid is given directly between governments and may reflect donors’ political and commercial interests, sometimes tied; multilateral aid is pooled through international agencies, less political, often for large programmes but may carry conditions.', '[4]'),
        ('Explain the advantages of NGO aid.', 'Small-scale, bottom-up projects using appropriate technology; works directly with communities; can reach the poorest; responsive in emergencies; less affected by corruption.', '[3]'),
        ('Explain the difference between short-term emergency aid and long-term development aid.', 'Emergency aid (food, shelter, medical care) saves lives after disasters; development aid funds education, health, infrastructure and livelihoods to reduce poverty over years.', '[3]'),
    ],
    'claims': [
        ('Most donor countries meet the 0.7% target.', False, 'Only a few, mainly in northern Europe, do so.'),
        ('Aid can be used to pursue donor countries’ political interests.', True, 'Strategic allies and former colonies often receive more aid.'),
        ('NGO aid is always better than government aid.', False, 'NGO projects are small and may be uncoordinated; large infrastructure needs government or multilateral funding.'),
    ],
    'essays': [
        ('aid does more to benefit donor countries than recipient countries',
         ['Tied aid, political influence, access to markets and resources, contracts for donor firms; aid can create dependency.'],
         ['Aid has eradicated smallpox, cut deaths from malaria, HIV and measles (Global Fund, Gavi), funded education and emergency relief; untied and multilateral aid focus on need.'],
         'Some aid serves donor interests, but well-targeted aid brings large benefits to recipients.',
         ['tied aid', 'health', 'dependency', 'governance']),
    ],
})


@data(t24b)
def t24b_oda(r, D):
    ds = []
    for nm in ('Donor P', 'Donor Q', 'Donor R', 'Donor S'):
        gni = r.choice([300, 500, 800, 1500, 2500, 4000, 25000])
        pc = r.uniform(0.15, 1.1)
        oda = round(gni * pc / 100, 1)
        ds.append((nm, gni, oda))
    pcs = [o / g * 100 for _, g, o in ds]
    meet = [d[0] for d, p in zip(ds, pcs) if p >= 0.7]
    stem = ('Table 24.2 shows gross national income (GNI) and official development assistance (ODA) for four donor countries (US$ billion): ' + '; '.join(f'{n}: GNI {nf(g)}, ODA {fmt(o, 1)}' for n, g, o in ds) + '.')
    big = ds[[o for _, _, o in ds].index(max(o for _, _, o in ds))][0]
    if D == 1:
        o, a = mcq(r, f'{fmt(pcs[0], 2)}%', [f'{fmt(pcs[0] * 10, 2)}%', f'{fmt(pcs[0] / 10, 3)}%', f'{fmt(ds[0][1] / ds[0][2], 1)}%', f'{fmt(pcs[0] + 0.3, 2)}%'])
        return {'stem': stem + ' What percentage of its GNI does Donor P give as ODA?', 'options': o, 'answer': a, 'key': f'{fmt(ds[0][2], 1)} ÷ {nf(ds[0][1])} × 100 = {fmt(pcs[0], 2)}%. [1]'}
    gap = [(d[0], 0.007 * d[1] - d[2]) for d in ds if pcs[ds.index(d)] < 0.7]
    parts = [
        lambda r: ('Calculate ODA as a percentage of GNI for each donor and identify those meeting the 0.7% target.', '; '.join(f'{d[0]}: {fmt(p, 2)}%' for d, p in zip(ds, pcs)) + '. Meeting target: ' + (', '.join(meet) or 'none'), '[3]'),
        lambda r: ('Calculate how much extra ODA each donor below the target would need to give to reach 0.7%.', '; '.join(f'{n}: US${dp(v, 1)} billion' for n, v in gap) or 'None: all donors meet the target.', '0.7% × GNI − ODA [2]'),
        lambda r: ('Explain why the donor giving the largest amount of aid may not be the most generous.', f'{big} gives the most in absolute terms because its economy is large, but generosity is better measured as a share of GNI or per person.', '[2]'),
        lambda r: ('Suggest why donors give different shares of GNI as aid.', 'Political priorities and public opinion; historical ties to former colonies; budget pressures; strategic and commercial interests; tradition of generosity (Scandinavia).', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t24c = T('Debt relief and evaluating the effectiveness of aid', 'debt relief evaluating effectiveness of aid')
B(t24c, {
    'terms': [
        ('Heavily Indebted Poor Countries (HIPC) Initiative', 'a programme launched in 1996 by the IMF and World Bank to reduce the debts of the poorest countries to sustainable levels'),
        ('Multilateral Debt Relief Initiative (MDRI)', 'a 2005 scheme that cancelled debts owed to the IMF, World Bank and African Development Fund by countries completing the HIPC process'),
        ('Jubilee 2000', 'a campaign by NGOs and churches for the cancellation of the debts of the poorest countries by the year 2000'),
        ('aid dependency', 'a situation in which a country relies on aid for a large share of its government budget'),
        ('conditionality', 'requirements attached to loans, aid or debt relief, such as economic reforms or poverty reduction plans'),
        ('aid effectiveness', 'how far aid achieves its aims of reducing poverty and promoting development'),
    ],
    'mcq': [
        ('About how many countries have received debt relief under the HIPC Initiative?', 'about 37', ['about 3', 'about 370', 'all countries'], '[1]'),
        ('Countries completing HIPC had to prepare', 'a Poverty Reduction Strategy Paper', ['a military plan', 'a tourism brochure', 'nothing'], '[1]'),
        ('After debt relief, Uganda used savings partly to', 'abolish primary school fees and expand enrolment', ['build a space programme', 'buy more debt', 'cut education'], '[1]'),
        ('A common criticism of aid effectiveness is that', 'aid may be lost to corruption or not reach the poorest', ['aid is always too large', 'aid never pays for health', 'aid only goes to HICs'], '[1]'),
    ],
    'explain': [
        ('Explain the benefits of debt relief for LICs.', 'Money saved on repayments can be spent on health, education and infrastructure; improves credit ratings; reduces pressure to export commodities; encourages investment.', '[3]'),
        ('Explain why debt relief has not solved the debt problem.', 'Conditions delayed relief; only some debts were cancelled; countries borrowed again from new lenders at higher rates; commodity price falls and shocks; COVID-19.', '[3]'),
        ('Explain how the effectiveness of aid can be evaluated.', 'Indicators before and after (school enrolment, child mortality, access to water); cost per beneficiary; sustainability after funding ends; independent evaluations and randomised trials; views of local people.', '[4]'),
    ],
    'claims': [
        ('Debt relief has always been unconditional.', False, 'HIPC relief required policy reforms and poverty reduction plans.'),
        ('Some countries increased social spending after debt relief.', True, 'Spending on health and education rose in many HIPC countries.'),
        ('Aid effectiveness is easy to measure.', False, 'Outcomes have many causes and take years to appear.'),
    ],
    'essays': [
        ('debt relief is more effective than aid in promoting development',
         ['Relief frees government budgets for long-term spending chosen by the country (Uganda, Tanzania abolished school fees); no administrative costs; reduces dependency.'],
         ['Aid can target specific needs and the poorest (vaccines, water projects, emergencies); relief benefits governments that may be corrupt; many countries have new debts.'],
         'Both are valuable; debt relief gives flexibility, while well-targeted aid addresses specific problems; governance determines the effectiveness of each.',
         ['HIPC', 'governance', 'social spending', 'dependency']),
    ],
})


@data(t24c)
def t24c_hipc(r, D):
    cty = r.choice(['Uganda', 'Tanzania', 'Mozambique', 'Ghana', 'Malawi', 'Zambia'])
    ds1 = round(r.uniform(1.5, 4.5), 1)  # % of GDP
    ds2 = round(ds1 * r.uniform(0.2, 0.5), 1)
    ed1 = round(r.uniform(1.5, 3.0), 1)
    ed2 = round(ed1 + r.uniform(0.5, 2.0), 1)
    h1 = round(r.uniform(0.6, 1.5), 1)
    h2 = round(h1 + r.uniform(0.3, 1.5), 1)
    gdp = r.choice([10, 20, 30, 45])  # US$ bn
    saved = (ds1 - ds2) / 100 * gdp
    extra = ((ed2 - ed1) + (h2 - h1)) / 100 * gdp
    stem = (f'Table 24.3 shows government spending in {cty} as a percentage of GDP before and after debt relief under HIPC and MDRI. Debt service: {fmt(ds1, 1)}% then {fmt(ds2, 1)}%. Education: {fmt(ed1, 1)}% then {fmt(ed2, 1)}%. '
            f'Health: {fmt(h1, 1)}% then {fmt(h2, 1)}%. Assume GDP was US${gdp} billion in both periods.')
    if D == 1:
        o, a = mcq(r, f'US${dp(saved, 2)} billion', [f'US${dp(ds1 - ds2, 1)} billion', f'US${dp(ds2 / 100 * gdp, 2)} billion', f'US${dp(saved * 10, 1)} billion', f'US${dp(extra, 2)} billion' if abs(extra - saved) > 0.01 else f'US${dp(saved / 2, 2)} billion'])
        return {'stem': stem + ' How much less was spent on debt service each year after relief?', 'options': o, 'answer': a, 'key': f'({fmt(ds1, 1)} − {fmt(ds2, 1)})% × {gdp} = US${dp(saved, 2)} billion. [1]'}
    parts = [
        lambda r: ('Calculate the annual saving in debt service in US$.', f'US${dp(saved, 2)} billion', f'({fmt(ds1, 1)} − {fmt(ds2, 1)})% × {gdp} billion [2]'),
        lambda r: ('Calculate the combined increase in health and education spending and compare it with the debt service saving.', f'US${dp(extra, 2)} billion, ' + ('more than' if extra > saved else 'less than') + ' the saving', '[2]'),
        lambda r: ('Suggest reasons why social spending may have risen by a different amount from the debt saving.', 'Other revenues and aid changed; economic growth; some savings went to infrastructure or other budgets; conditions required poverty-reducing spending.', '[3]'),
        lambda r: ('Explain why higher education spending does not automatically lead to development.', 'Quality of teaching, teacher numbers, buildings and materials, corruption, rural access and children’s health and poverty affect outcomes; results take years.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[24] = [t24a, t24b, t24c]


# ============================================================== CHAPTER 25: International tourism

ARR = [(1950, 25), (1980, 278), (1990, 435), (2000, 674), (2010, 952), (2019, 1465), (2020, 407), (2023, 1300)]

t25a = T('Growth and global pattern of international tourism', 'growth global pattern of international tourism')
B(t25a, {
    'terms': [
        ('international tourist arrival', 'a visitor who travels to a country other than their own and stays at least one night'),
        ('mass tourism', 'large numbers of people visiting the same destinations, often on package holidays'),
        ('long-haul tourism', 'travel to distant destinations, usually involving flights of more than about six hours'),
        ('tourism receipts', 'the spending of international visitors in a country'),
        ('pleasure periphery', 'the zone of tourist destinations surrounding the main tourist-generating regions, extending further as transport improves'),
        ('UN Tourism (UNWTO)', 'the UN agency that monitors and promotes tourism'),
    ],
    'mcq': [
        ('International tourist arrivals in 2019 were about', '1.5 billion', ['15 million', '150 million', '15 billion'], '[1]'),
        ('The region receiving the most international tourist arrivals is', 'Europe', ['Africa', 'South America', 'Oceania'], 'About half of all arrivals. [1]'),
        ('International arrivals fell by about 70% in 2020 because of', 'the COVID-19 pandemic', ['the 2008 financial crisis', 'a volcanic eruption', 'higher oil prices'], '[1]'),
        ('A key reason for the growth of tourism since 1960 is', 'cheaper air travel, including jet aircraft and low-cost airlines', ['less leisure time', 'falling incomes', 'more travel restrictions'], '[1]'),
    ],
    'explain': [
        ('Explain the reasons for the growth of international tourism.', 'Rising incomes and paid holidays; cheaper and faster air travel (jumbo jets, low-cost carriers); package holidays; internet booking; growth of the middle class in China and India; marketing; visa relaxation.', '1 mark per reason [4]'),
        ('Describe the global pattern of international tourism.', 'Europe receives about half of arrivals; Asia-Pacific has grown fastest; the Americas next; Africa and the Middle East have small shares; most tourism is between HICs and within regions.', '[3]'),
        ('Explain why tourism is vulnerable to external shocks.', 'It depends on travel, confidence and disposable income: pandemics, terrorism, natural disasters, recessions, conflict and oil prices quickly reduce arrivals.', '[3]'),
    ],
    'claims': [
        ('Most international tourists travel to LICs.', False, 'Most visit HICs, particularly in Europe.'),
        ('China has become the largest source of international tourist spending.', True, 'Chinese outbound spending grew rapidly before 2020.'),
        ('International arrivals recovered fully to 2019 levels in 2021.', False, 'Recovery took until about 2024.'),
    ],
    'essays': [
        ('the growth of international tourism is mainly the result of improvements in transport',
         ['Jet aircraft, wide-bodied jets and low-cost airlines cut journey times and costs, extending the pleasure periphery.'],
         ['Rising incomes, paid holidays, the internet, marketing, the growth of the middle class in Asia, political changes and visa policies also drove growth.'],
         'Transport made long-distance tourism possible, but rising incomes and leisure time created the demand.',
         ['air travel', 'incomes', 'technology', 'globalisation']),
    ],
})


@data(t25a)
def t25a_arr(r, D):
    a, b = sorted(r.sample([0, 1, 2, 3, 4, 5], 2))
    (y1, v1), (y2, v2) = ARR[a], ARR[b]
    n = y2 - y1
    cagr = ((v2 / v1) ** (1 / n) - 1) * 100
    fall = pct_change(1465, 407)
    rec = 1300 / 1465 * 100
    stem = 'Fig. 25.1 shows international tourist arrivals (millions): ' + ', '.join(f'{y}: {v}' for y, v in ARR) + '.'
    if D == 1:
        o, ans = mcq(r, f'{sgn(fall)}%', [f'{sgn(407 / 1465 * 100)}%', f'{sgn(-fall)}%', f'{sgn(fall / 2)}%', f'{sgn(fall + 10)}%'])
        return {'stem': stem + ' What was the percentage change in arrivals between 2019 and 2020?', 'options': o, 'answer': ans, 'key': f'(407 − 1465) ÷ 1465 × 100 = {sgn(fall)}%. [1]'}
    parts = [
        lambda r: (f'Calculate the mean annual growth rate of arrivals between {y1} and {y2}.', f'{dp(cagr, 2)}% per year', f'({v2} ÷ {v1})^(1/{n}) − 1 [3]'),
        lambda r: ('Calculate the percentage change in arrivals between 2019 and 2020.', f'{sgn(fall)}%', '(407 − 1465) ÷ 1465 × 100 [1]'),
        lambda r: ('Calculate arrivals in 2023 as a percentage of the 2019 level.', f'{dp(rec)}%', '1300 ÷ 1465 × 100 [1]'),
        lambda r: ('Explain the growth in arrivals between 1950 and 2019.', 'Rising incomes and paid holidays, cheaper air travel, package and low-cost holidays, internet booking, growth of Asian middle classes and new destinations.', '[3]'),
        lambda r: ('Explain why arrivals fell in 2020 and recovered slowly.', 'COVID-19 border closures, quarantine rules and flight cancellations; afterwards lost incomes, health fears, slow reopening in Asia and staff shortages.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t25b = T('The tourism multiplier and the Butler model', 'tourism multiplier butler model')
BUTLER = ['exploration', 'involvement', 'development', 'consolidation', 'stagnation', 'decline or rejuvenation']

B(t25b, {
    'terms': [
        ('tourism multiplier', 'the process by which tourist spending creates further rounds of income and jobs as money circulates in the local economy'),
        ('leakage', 'tourist spending that leaves the destination, for example profits to foreign hotel chains and payments for imports'),
        ('Butler model (tourist area life cycle)', 'a model (1980) showing how a resort passes through exploration, involvement, development, consolidation, stagnation and then decline or rejuvenation'),
        ('carrying capacity (tourism)', 'the maximum number of visitors a destination can support without unacceptable environmental, social or economic damage'),
        ('rejuvenation', 'renewed growth of a declining resort through investment and new attractions'),
        ('enclave tourism', 'tourism concentrated in self-contained resorts with few links to the local economy'),
    ],
    'mcq': [
        ('In the Butler model, the stage at which local people first provide facilities for visitors is', 'involvement', ['exploration', 'stagnation', 'decline'], '[1]'),
        ('All-inclusive resorts tend to', 'reduce the local multiplier effect', ['increase local spending', 'eliminate leakage', 'raise local wages above all other jobs'], '[1]'),
        ('Blackpool’s attempts to attract new visitors since the 1990s are an example of', 'rejuvenation in the Butler model', ['exploration', 'involvement', 'development'], '[1]'),
        ('Leakage is likely to be highest in', 'small island destinations that import most goods', ['large diversified economies', 'domestic tourism', 'locally owned guesthouses'], '[1]'),
    ],
    'explain': [
        ('Explain the tourism multiplier effect.', 'Tourist spending creates direct jobs and income in hotels and attractions; suppliers gain indirect income; employees spend their wages locally (induced effect); tax revenue funds infrastructure, attracting more visitors.', '[4]'),
        ('Explain the stages of the Butler model.', 'Exploration (few adventurous visitors); involvement (local facilities); development (rapid growth, external investment); consolidation (growth slows); stagnation (capacity reached, reputation falls); then decline or rejuvenation.', '1 mark per stage [4]'),
        ('Explain the limitations of the Butler model.', 'Not all resorts follow every stage; timescales vary; difficult to identify the stage; ignores external shocks and planning; rejuvenation can happen repeatedly.', '[3]'),
    ],
    'claims': [
        ('All tourist spending stays in the destination.', False, 'Much leaks out through imports and foreign ownership.'),
        ('Resorts can avoid decline through planning and investment.', True, 'Diversification and new attractions can rejuvenate resorts.'),
        ('The Butler model predicts exact dates for each stage.', False, 'It is descriptive; timings differ between resorts.'),
    ],
    'essays': [
        ('the Butler model is useful for managing tourist destinations',
         ['It identifies warning signs of stagnation and the need for planning, diversification and carrying-capacity limits (e.g. Benidorm, Blackpool).'],
         ['Many destinations do not follow its stages; it is hard to apply predictively; external shocks dominate; it is better as a description than a management tool.'],
         'The model is a helpful framework for thinking about change, but managers need detailed local data to use it.',
         ['stagnation', 'rejuvenation', 'carrying capacity', 'shocks']),
    ],
})


@data(t25b)
def t25b_mult(r, D):
    spend = r.choice([50, 120, 300, 800])  # $ million direct
    leak = r.randint(20, 75) / 100
    mpc = round(r.uniform(0.4, 0.7), 2)  # share of local income re-spent locally
    k = 1 / (1 - mpc * (1 - leak))
    tot = spend * (1 - leak) * k
    dest = r.choice(['Jamaica', 'the Maldives', 'the Gambia', 'Kenya’s coast', 'Bali, Indonesia', 'St Lucia'])
    stem = (f'International tourists spent US${spend} million in {dest} in one year. About {int(leak * 100)}% of this spending leaked out of the economy immediately. Of the income that remains, local people re-spend about {int(mpc * 100)}% locally; each round of spending also leaks {int(leak * 100)}%. '
            f'The multiplier k = 1 ÷ (1 − {fmt(mpc, 2)} × (1 − {fmt(leak, 2)})).')
    if D == 1:
        o, a = mcq(r, fmt(k, 2), [fmt(1 / (1 - mpc), 2), fmt(1 / leak, 2), fmt(k + 0.5, 2), fmt(max(1.01, k - 0.3), 2)])
        return {'stem': stem + ' What is the value of the multiplier?', 'options': o, 'answer': a, 'key': f'1 ÷ (1 − {fmt(mpc, 2)} × {fmt(1 - leak, 2)}) = {fmt(k, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the spending retained after initial leakage.', f'US${dp(spend * (1 - leak), 1)} million', f'{spend} × (1 − {fmt(leak, 2)}) [1]'),
        lambda r: ('Calculate the multiplier and the total income generated in the local economy.', f'k = {fmt(k, 2)}; total US${dp(tot, 1)} million', f'retained × k [3]'),
        lambda r: ('Explain why leakage is high in many small tourist destinations.', 'Foreign-owned hotels and airlines send profits abroad; food, drink and building materials are imported; foreign managers; all-inclusive packages paid in the source country.', '[3]'),
        lambda r: ('Suggest how the destination could increase the multiplier effect.', 'Encourage local ownership and suppliers (local food), train local staff for management jobs, limit all-inclusives, promote local crafts and excursions, tax foreign operators.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t25c = T('Case study of the management of a tourist destination and sustainable tourism', 'case study of the management of a tourist destination sustainable tourism')
B(t25c, {
    'terms': [
        ('sustainable tourism', 'tourism that takes full account of its current and future economic, social and environmental impacts, meeting the needs of visitors, industry, the environment and host communities'),
        ('overtourism', 'when visitor numbers exceed the capacity of a destination, harming residents’ quality of life and the environment'),
        ('Sustainable Development Fee (Bhutan)', 'a daily charge on most international visitors to Bhutan to fund conservation and public services'),
        ('day-tripper access fee (Venice)', 'a charge introduced in 2024 for day visitors entering Venice’s historic centre on peak days'),
        ('community-based tourism', 'tourism owned or managed by local communities so that benefits stay local'),
        ('visitor management', 'measures such as quotas, timed entry, zoning and pricing to control visitor numbers and behaviour'),
    ],
    'mcq': [
        ('Bhutan’s tourism policy is often described as', 'high value, low volume', ['mass tourism', 'no tourism allowed', 'free entry for all'], '[1]'),
        ('Venice banned large cruise ships from entering its historic lagoon centre in', '2021', ['1950', '1990', '2030'], '[1]'),
        ('Machu Picchu in Peru manages visitor numbers through', 'timed tickets and daily limits', ['unlimited entry', 'a new airport at the site', 'free camping on the ruins'], '[1]'),
        ('The Maldives is particularly vulnerable to', 'sea-level rise and coral bleaching', ['volcanic eruptions', 'avalanches', 'desertification'], 'Most islands are less than 1.5 m above sea level. [1]'),
    ],
    'explain': [
        ('Explain the negative impacts of mass tourism on destinations.', 'Overcrowding and congestion; rising house prices and loss of residents (Venice); damage to ecosystems and heritage; water shortages; waste and pollution; seasonal, low-paid jobs; cultural erosion.', '[4]'),
        ('Explain how tourist destinations can be managed sustainably.', 'Visitor limits and pricing; zoning; local ownership and employment; environmental regulations; investment of revenue in conservation; diversifying the season; community involvement.', '[4]'),
        ('Explain why the Maldives depends on tourism and why this makes it vulnerable.', 'Tourism provides about a quarter of GDP and most foreign exchange; few other resources; vulnerable to pandemics, recessions, coral bleaching and sea-level rise.', '[3]'),
    ],
    'claims': [
        ('Restricting visitor numbers always reduces income.', False, 'Higher-value visitors and fees can maintain or increase income.'),
        ('Overtourism can lead to local protests.', True, 'Residents in Barcelona, Venice and Majorca have protested.'),
        ('Ecotourism has no environmental impact.', False, 'Flights and visitor activities still cause impacts.'),
    ],
    'cs': [
        ('the management of a tourist destination', [
            ('Venice, Italy', {'strategy': 'Ban on large cruise ships in the lagoon centre (2021); day-tripper access fee (2024, €5, raised to €10 for late bookings in 2025); limits on group sizes; restrictions on new hotels and short-term lets; MOSE flood barriers protect the city and its tourism.',
                               'evaluate': 'Cruise traffic in the centre stopped and the fee raised revenue, but visitor numbers on fee days fell little, the resident population of the historic centre has fallen below 50 000, and UNESCO has warned about overtourism.'}),
            ('Bhutan', {'strategy': 'High value, low volume policy since 1974; Sustainable Development Fee (US$200 per night from 2022, reduced to US$100 in 2023); licensed guides; protected areas cover about half of the country; constitutional requirement for 60% forest cover.',
                        'evaluate': 'Culture and environment are well protected and fees fund health and education; but high costs limit arrivals and income, and tourism recovery after COVID-19 was slow.'}),
            ('the Maldives', {'strategy': 'One island, one resort model separating resorts from local communities; rules limiting building heights and coverage; marine protected areas; guesthouse tourism on local islands since 2009; green tax on tourists.',
                              'evaluate': 'Tourism has driven high incomes and arrivals of nearly 2 million a year; but leakage is high, coral bleaching and sea-level rise threaten resorts, waste is dumped at Thilafushi, and benefits are uneven between Malé and outer atolls.'}),
        ], [
            ('describe how tourism in the destination is managed', 'strategy', 'Named policies, dates, fees and organisations.'),
            ('evaluate the extent to which tourism in the destination is sustainable', 'evaluate', 'Economic, social and environmental evidence.', 'assess how sustainable the management of tourism has been.'),
        ]),
    ],
    'essays': [
        ('sustainable tourism is an unrealistic goal for most tourist destinations',
         ['Mass tourism brings overtourism, leakage and environmental damage; long-haul flights cause emissions; destinations depend on growth (Venice, Maldives).'],
         ['High-value, low-volume (Bhutan), community-based tourism, visitor management (Machu Picchu) and local ownership show sustainable approaches can work.'],
         'Full sustainability is difficult, especially with air travel, but management can make tourism much more sustainable.',
         ['overtourism', 'visitor management', 'leakage', 'climate change']),
    ],
})


CHAPTERS[25] = [t25a, t25b, t25c]


# ============================================================== CHAPTER 26: National development

t26a = T('The sectors of the economy and the Clark-Fisher model', 'sectors of the economy clark-fisher model')
B(t26a, {
    'terms': [
        ('primary sector', 'activities that extract raw materials from the land or sea, such as farming, fishing, forestry and mining'),
        ('secondary sector', 'activities that process raw materials and manufacture goods'),
        ('tertiary sector', 'activities that provide services, such as retail, transport, health and education'),
        ('quaternary sector', 'knowledge-based services such as research and development, ICT and consultancy'),
        ('Clark-Fisher model', 'a model showing how the share of employment shifts from the primary to the secondary and then the tertiary sector as a country develops'),
        ('post-industrial economy', 'an economy in which most employment is in services rather than manufacturing'),
    ],
    'mcq': [
        ('According to the Clark-Fisher model, a pre-industrial economy has most employment in the', 'primary sector', ['secondary sector', 'tertiary sector', 'quaternary sector'], '[1]'),
        ('In the UK today the share of employment in the tertiary sector is about', '80%', ['8%', '30%', '50%'], '[1]'),
        ('A limitation of the Clark-Fisher model is that', 'some countries move from primary to tertiary employment without a large manufacturing phase', ['all countries industrialise in the same way', 'it includes too many sectors', 'it applies only to farming'], '[1]'),
        ('Which job is in the quaternary sector?', 'a software researcher', ['a coal miner', 'a car assembly worker', 'a shop assistant'], '[1]'),
    ],
    'explain': [
        ('Explain the changes in employment structure shown by the Clark-Fisher model.', 'Pre-industrial: most work in the primary sector; industrialisation: mechanisation of farming releases labour to manufacturing, secondary share rises; post-industrial: automation and global shift reduce manufacturing, rising incomes increase demand for services.', '[4]'),
        ('Explain why employment in the primary sector falls as countries develop.', 'Mechanisation and higher productivity in farming; better jobs and pay in cities attract workers; declining share of income spent on food.', '[3]'),
        ('Explain the limitations of the Clark-Fisher model.', 'Based on the historical experience of HICs; ignores the informal sector; globalisation lets countries specialise differently; some LICs have large informal tertiary sectors without industrialisation.', '[3]'),
    ],
    'claims': [
        ('A large tertiary sector always indicates a high level of development.', False, 'Many LICs have large informal service sectors.'),
        ('Manufacturing output can rise while manufacturing employment falls.', True, 'Automation raises productivity.'),
        ('The model shows employment by sector over time.', True, 'It plots sectoral shares through stages of development.'),
    ],
    'essays': [
        ('the Clark-Fisher model is no longer useful for understanding economic development',
         ['Globalisation, the global shift and the growth of informal services mean countries no longer follow the HIC path; service-led growth (India) and premature deindustrialisation.'],
         ['The general trend from primary to secondary to tertiary still applies (South Korea, China); it is a useful descriptive framework for comparing countries.'],
         'The model describes broad trends, but paths of development are now more varied.',
         ['globalisation', 'informal sector', 'NICs', 'deindustrialisation']),
    ],
})


@data(t26a)
def t26a_cf(r, D):
    yrs = [1970, 1990, 2010, 2025]
    p0 = r.randint(50, 70)
    s0 = r.randint(10, 20)
    rows = []
    p, s = p0, s0
    for i, y in enumerate(yrs):
        if i:
            p = max(3, p - r.randint(12, 22))
            s = s + r.randint(5, 12) if i < 2 else max(12, s - r.randint(-2, 6))
        rows.append((y, p, s, 100 - p - s))
    if any(t < 5 for _, _, _, t in rows):
        return None
    cty = r.choice(['Country A', 'Country B'])
    stem = (f'Table 26.1 shows employment structure (% of workers in primary, secondary and tertiary sectors) for {cty}: ' + '; '.join(f'{y}: {p}%, {s}%, {t}%' for y, p, s, t in rows) + '.')
    ch = rows[-1][1] - rows[0][1]
    if D == 1:
        o, a = mcq(r, f'{rows[-1][3]}%', [f'{rows[0][3]}%', f'{rows[-1][2]}%', f'{rows[-1][1] + rows[-1][2]}%', f'{rows[-1][3] - rows[0][3]}%'])
        return {'stem': stem + ' What percentage of workers were in the tertiary sector in 2025?', 'options': o, 'answer': a, 'key': f'100 − {rows[-1][1]} − {rows[-1][2]} = {rows[-1][3]}%. [1]'}
    peak = max(rows, key=lambda x: x[2])
    parts = [
        lambda r: ('Calculate the change in the share of primary employment between 1970 and 2025, in percentage points and as a percentage change.', f'{sgn(ch, 0)} percentage points; {sgn(pct_change(rows[0][1], rows[-1][1]))}%', '[2]'),
        lambda r: ('Identify the year in which the secondary sector share was highest.', f'{peak[0]} ({peak[2]}%)', '[1]'),
        lambda r: ('Describe how the changes fit the Clark-Fisher model.', 'Primary employment falls steadily; secondary rises with industrialisation' + (' and then falls' if rows[-1][2] < peak[2] else '') + '; tertiary grows to become the largest sector, as the model predicts.', '[3]'),
        lambda r: ('Suggest reasons for the fall in primary employment.', 'Mechanisation and higher farm productivity; rural-urban migration for better-paid jobs; land consolidation; decline of mining.', '[2]'),
        lambda r: ('Suggest why the tertiary sector grew.', 'Rising incomes increase demand for services (retail, health, education, finance, tourism); government services expand; ICT and outsourcing; automation reduces manufacturing jobs.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t26b = T('Measuring national development and the development gap', 'measuring national development development gap')
B(t26b, {
    'terms': [
        ('Human Development Index (HDI)', 'a UN composite measure of development combining life expectancy, education (mean and expected years of schooling) and GNI per capita (PPP)'),
        ('GNI per capita (PPP)', 'gross national income per person adjusted for differences in the cost of living (purchasing power parity)'),
        ('development gap', 'the difference in wealth and well-being between the richest and poorest countries'),
        ('Gini coefficient', 'a measure of inequality from 0 (perfect equality) to 1 (one person has everything)'),
        ('Multidimensional Poverty Index', 'a measure of poverty combining deprivations in health, education and living standards'),
        ('composite indicator', 'a measure that combines several indicators into one value'),
    ],
    'mcq': [
        ('The three dimensions of the HDI are', 'health, education and standard of living', ['population, area and GDP', 'trade, aid and debt', 'climate, soils and relief'], '[1]'),
        ('The HDI is calculated as', 'the geometric mean of the three dimension indices', ['the sum of GDP and life expectancy', 'the arithmetic mean of GDP growth rates', 'life expectancy divided by income'], '[1]'),
        ('A country with an HDI of 0.82 is classed as', 'very high human development', ['low human development', 'medium human development', 'high human development'], 'Very high: 0.800 or more. [1]'),
        ('Purchasing power parity adjusts income for', 'differences in the cost of living between countries', ['inflation only', 'population size', 'the value of exports'], '[1]'),
    ],
    'explain': [
        ('Explain why the HDI is a better measure of development than GNI per capita alone.', 'It includes health and education as well as income, reflecting quality of life; two countries with similar incomes may differ greatly in life expectancy and schooling.', '[3]'),
        ('Explain the limitations of the HDI.', 'Averages hide inequality within countries; omits political freedom, environment and gender inequality; data quality varies; equal weighting is arbitrary; slow to change.', '[4]'),
        ('Explain the causes of the development gap.', 'Colonial history; dependence on primary exports; debt; trade rules; conflict and governance; disease and climate; lack of investment in education and infrastructure; technology gaps.', '[4]'),
    ],
    'claims': [
        ('The HDI measures inequality within a country.', False, 'The inequality-adjusted IHDI does this; the standard HDI uses averages.'),
        ('GNI per capita can be distorted by a small wealthy elite.', True, 'Averages hide large inequalities.'),
        ('The development gap between some regions has narrowed since 1990.', True, 'East Asia has converged with HICs, though some African countries have fallen further behind.'),
    ],
    'essays': [
        ('the development gap is widening',
         ['The gap in absolute income between the richest and poorest countries has grown; some LDCs and fragile states have stagnated; inequality within countries is rising.'],
         ['Many countries, especially in Asia, have converged; global poverty fell sharply until 2019; HDI gaps in life expectancy and schooling have narrowed.'],
         'The gap has narrowed for many countries and indicators, but widened for the poorest and most fragile states.',
         ['HDI', 'income', 'NICs', 'fragile states']),
    ],
})


def _hdi(le, mys, eys, gni):
    h = (le - 20) / 65
    e = (min(mys, 15) / 15 + min(eys, 18) / 18) / 2
    i = (math.log(gni) - math.log(100)) / (math.log(75000) - math.log(100))
    return h, e, i, (h * e * i) ** (1 / 3)


def _hdi_cat(x):
    return 'very high' if x >= 0.8 else 'high' if x >= 0.7 else 'medium' if x >= 0.55 else 'low'


@data(t26b)
def t26b_hdi(r, D):
    le = round(r.uniform(55, 82), 1)
    mys = round(r.uniform(3, 13), 1)
    eys = round(min(18.0, mys + r.uniform(1.0, 5.0)), 1)
    gni = r.choice([1200, 2500, 5000, 9000, 15000, 30000, 50000])
    h, e, i, hdi = _hdi(le, mys, eys, gni)
    stem = (f'Country X has a life expectancy of {fmt(le, 1)} years, mean years of schooling of {fmt(mys, 1)}, expected years of schooling of {fmt(eys, 1)} and GNI per capita of US${nf(gni)} (PPP). '
            'Health index = (LE − 20) ÷ 65. Education index = (mean years ÷ 15 + expected years ÷ 18) ÷ 2. Income index = (ln GNI − ln 100) ÷ (ln 75 000 − ln 100). HDI = cube root of (health × education × income).')
    if D == 1:
        o, a = mcq(r, fmt(h, 3), [fmt(le / 85, 3), fmt((le - 20) / 85, 3), fmt(h + 0.05, 3), fmt(h - 0.05, 3)])
        return {'stem': stem + ' What is the health index?', 'options': o, 'answer': a, 'key': f'({fmt(le, 1)} − 20) ÷ 65 = {fmt(h, 3)}. [1]'}
    parts = [
        lambda r: ('Calculate the health and education indices.', f'health {fmt(h, 3)}; education {fmt(e, 3)}', '[2]'),
        lambda r: ('Calculate the income index.', f'{fmt(i, 3)}', f'(ln {nf(gni)} − ln 100) ÷ (ln 75 000 − ln 100) [2]'),
        lambda r: ('Calculate the HDI and state its category (low below 0.550; medium 0.550-0.699; high 0.700-0.799; very high 0.800 or more).', f'{fmt(hdi, 3)}: {_hdi_cat(hdi)} human development', f'({fmt(h, 3)} × {fmt(e, 3)} × {fmt(i, 3)})^(1/3) [3]'),
        lambda r: ('Explain why a logarithm of income is used in the HDI.', 'Each extra dollar adds less to well-being at higher incomes (diminishing returns), so the log reduces the influence of very high incomes.', '[2]'),
        lambda r: ('Suggest why the HDI may not reflect the well-being of all people in Country X.', 'It is an average and hides inequality by income, region, gender and ethnicity; it omits freedom, security and environmental quality.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t26c = T('Newly industrialised countries and emerging economies', 'newly industrialised countries emerging economies')
B(t26c, {
    'terms': [
        ('newly industrialised country (NIC)', 'a country that has experienced rapid industrial growth and rising incomes since the 1960s, such as South Korea, Taiwan and Singapore'),
        ('emerging economy', 'a country with rapid economic growth and increasing integration into global markets, such as China, India, Brazil, Indonesia and Mexico'),
        ('BRICS', 'a grouping of major emerging economies, originally Brazil, Russia, India, China and South Africa, expanded from 2024'),
        ('Asian Tigers', 'the first-generation NICs: South Korea, Taiwan, Hong Kong and Singapore'),
        ('chaebol', 'a large family-controlled business conglomerate in South Korea, such as Samsung or Hyundai'),
        ('economic growth rate', 'the annual percentage increase in GDP'),
    ],
    'mcq': [
        ('South Korea’s rapid growth from the 1960s was led by', 'state-guided export-oriented industrialisation and chaebol', ['oil exports', 'tourism only', 'subsistence agriculture'], '[1]'),
        ('At a steady growth rate of 7% a year, GDP doubles in about', '10 years', ['2 years', '35 years', '70 years'], 'Rule of 70: 70 ÷ 7. [1]'),
        ('Which is a second-generation NIC?', 'Malaysia', ['Germany', 'Japan', 'the UK'], '[1]'),
        ('A common problem in rapidly growing emerging economies is', 'rising regional and income inequality', ['falling urban populations', 'lower energy use', 'less pollution'], '[1]'),
    ],
    'explain': [
        ('Explain the reasons for the rapid growth of NICs.', 'Export-oriented policies; investment in education and skills; low labour costs at first; strong state planning, credit and protection for key industries; FDI; high savings; location on trade routes; Cold War aid.', '[4]'),
        ('Explain the problems that may result from rapid economic growth in emerging economies.', 'Pollution and environmental damage; regional inequality; rapid urbanisation and slums; rising income inequality; exploitation of workers; dependence on exports and FDI.', '[4]'),
        ('Explain why some NICs have moved into high-technology industries.', 'Rising wages reduced competitiveness in labour-intensive industry; investment in R&D and universities; government strategy; skilled workforce; brands such as Samsung and TSMC.', '[3]'),
    ],
    'claims': [
        ('All emerging economies grow at the same rate.', False, 'Growth rates vary greatly and fluctuate.'),
        ('Education was a key factor in South Korea’s development.', True, 'High investment in schooling created a skilled workforce.'),
        ('NICs no longer have any low-wage industries.', False, 'Many still have low-wage sectors and informal employment.'),
    ],
    'essays': [
        ('the growth of NICs and emerging economies has been driven mainly by globalisation',
         ['FDI, TNC outsourcing, access to global markets and global value chains (Vietnam, China, Mexico) drove growth.'],
         ['Domestic factors were decisive: state planning, land reform, education, savings and infrastructure in South Korea and China; some open economies did not grow.'],
         'Globalisation provided opportunities, but domestic policies determined which countries could take advantage.',
         ['FDI', 'education', 'state policy', 'exports']),
    ],
})


@data(t26c)
def t26c_growth(r, D):
    cty = r.choice(['Country P', 'Country Q'])
    g = round(r.uniform(3.0, 9.0), 1)
    y0 = r.choice([1990, 1995, 2000])
    v0 = r.choice([800, 1500, 3000, 5000])
    n = r.choice([20, 25, 30])
    v1 = round(v0 * (1 + g / 100) ** n * r.uniform(0.97, 1.03), -1)
    cagr = ((v1 / v0) ** (1 / n) - 1) * 100
    dbl = 70 / cagr
    stem = f'{cty}, an emerging economy, had GDP per capita (constant US$) of {nf(v0)} in {y0} and {nf(int(v1))} in {y0 + n}.'
    if D == 1:
        o, a = mcq(r, f'{dp(cagr, 1)}%', [f'{dp(pct_change(v0, v1) / n, 1)}%', f'{dp(pct_change(v0, v1), 0)}%', f'{dp(cagr * 2, 1)}%', f'{dp(cagr / 2, 1)}%'])
        return {'stem': stem + ' What was the mean annual growth rate?', 'options': o, 'answer': a, 'key': f'({nf(int(v1))} ÷ {nf(v0)})^(1/{n}) − 1 = {dp(cagr, 1)}%. [1]'}
    parts = [
        lambda r: ('Calculate the percentage increase in GDP per capita over the period.', f'{sgn(pct_change(v0, v1))}%', '[1]'),
        lambda r: ('Calculate the mean annual growth rate.', f'{dp(cagr, 2)}% per year', f'({nf(int(v1))} ÷ {nf(v0)})^(1/{n}) − 1 [2]'),
        lambda r: ('Use the rule of 70 to estimate how long it took GDP per capita to double.', f'about {dp(dbl, 1)} years', f'70 ÷ {dp(cagr, 2)} [2]'),
        lambda r: ('Explain factors that may have contributed to this growth.', 'Export-oriented manufacturing and FDI, investment in education and infrastructure, urbanisation moving workers into higher-productivity jobs, stable government policy, high savings.', '[3]'),
        lambda r: ('Suggest why GDP per capita growth may not reflect improvements for everyone.', 'Gains may go mainly to urban and coastal regions or the wealthy; inequality may rise; environmental costs; informal workers excluded.', '[2]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[26] = [t26a, t26b, t26c]


# ============================================================== CHAPTER 27: Globalisation of economic activity

t27a = T('TNCs and the new international division of labour', 'tncs new international division of labour')
B(t27a, {
    'terms': [
        ('transnational corporation (TNC)', 'a company that operates in more than one country, usually with headquarters in its home country'),
        ('new international division of labour (NIDL)', 'the spatial separation of TNC activities: headquarters and R&D in HICs, manufacturing and assembly in lower-wage countries'),
        ('foreign direct investment (FDI)', 'investment by a company in productive assets in another country'),
        ('offshoring', 'moving business activities to another country'),
        ('vertical integration', 'when a company controls several stages of production, from raw materials to retail'),
        ('horizontal integration', 'when a company expands by acquiring or merging with firms at the same stage of production'),
    ],
    'mcq': [
        ('Under the NIDL, TNC headquarters are usually located in', 'major cities in HICs', ['rural LICs', 'export processing zones', 'remote mining towns'], '[1]'),
        ('The largest TNCs have annual revenues greater than the GDP of', 'many countries', ['no countries', 'only the USA', 'all of Europe combined'], '[1]'),
        ('TNCs locate assembly plants in LICs mainly because of', 'lower labour costs', ['higher wages', 'more skilled scientists', 'colder climates'], '[1]'),
        ('Apple’s iPhones have mainly been assembled by', 'Foxconn in China', ['Apple in California', 'Samsung in Germany', 'Tata in the UK'], '[1]'),
    ],
    'explain': [
        ('Explain the new international division of labour.', 'TNCs separate stages of production: high-skilled HQ, design and R&D in HICs; component making in NICs; assembly in low-wage countries; enabled by cheap transport and ICT.', '[3]'),
        ('Explain why TNCs have become more powerful.', 'Huge revenues, global supply chains and control of technology and brands; ability to move investment between countries gives bargaining power over governments; lobbying and tax planning.', '[3]'),
        ('Explain the reasons for the growth of TNCs.', 'Falling transport and communication costs; trade liberalisation; access to markets and cheap labour and resources; economies of scale; mergers and acquisitions; government incentives.', '[4]'),
    ],
    'claims': [
        ('TNCs are found only in HICs.', False, 'Many TNCs come from emerging economies, such as Tata (India) and Huawei (China).'),
        ('TNCs can shift profits to low-tax countries.', True, 'Transfer pricing and subsidiaries in tax havens reduce tax paid.'),
        ('The NIDL means all stages of production stay in one country.', False, 'It is the spatial division of stages across countries.'),
    ],
    'essays': [
        ('TNCs are now more powerful than national governments',
         ['Largest TNC revenues exceed many countries’ GDPs; footloose investment gives bargaining power; tax avoidance; lobbying.'],
         ['Governments control regulation, taxation, trade policy and market access (China’s controls, EU fines on tech firms, global minimum tax agreement 2021); TNCs depend on states for infrastructure and stability.'],
         'TNCs have great influence, especially over small countries, but large states retain significant power.',
         ['revenue', 'regulation', 'tax', 'bargaining power']),
    ],
})


@data(t27a)
def t27a_wage(r, D):
    cs = [('the USA', r.randint(35, 45)), ('Mexico', r.randint(4, 7)), ('China', r.randint(6, 10)), ('Vietnam', r.randint(2, 4)), ('Bangladesh', r.choice([1, 1.5, 2]))]
    hrs = round(r.uniform(0.3, 2.0), 1)
    units = r.choice([100000, 500000, 2000000])
    lc = [(c, w * hrs) for c, w in cs]
    cheap = min(lc, key=lambda x: x[1])
    saving = (lc[0][1] - cheap[1]) * units
    prod = r.choice(['a pair of trainers', 'a smartphone', 'a shirt', 'a laptop'])
    stem = (f'Table 27.1 shows hourly labour costs (US$, including benefits) in manufacturing: ' + ', '.join(f'{c} ${fmt(w, 1)}' for c, w in cs) +
            f'. Assembling {prod} takes {fmt(hrs, 1)} hours of labour. A TNC plans to make {nf(units)} units a year.')
    if D == 1:
        o, a = mcq(r, f'US${dp(lc[2][1], 2)}', [f'US${dp(v, 2)}' for v in (cs[2][1], cs[2][1] / hrs, lc[0][1], lc[2][1] * 2, lc[2][1] / 2, lc[1][1])])
        return {'stem': stem + ' What is the labour cost per unit in China?', 'options': o, 'answer': a, 'key': f'{cs[2][1]} × {fmt(hrs, 1)} = US${dp(lc[2][1], 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the labour cost per unit in each country.', '; '.join(f'{c}: ${dp(v, 2)}' for c, v in lc), 'hourly cost × hours [2]'),
        lambda r: ('Calculate the annual saving in labour costs from assembling in the cheapest country rather than the USA.', f'US${nf(round(saving))} ({cheap[0]})', f'(US cost − cheapest cost) × {nf(units)} [2]'),
        lambda r: ('Suggest why the TNC might not choose the country with the lowest labour cost.', 'Lower productivity and skills; poor infrastructure and power supply; distance from markets and longer delivery times; political risk; tariffs and trade agreements (USMCA favours Mexico); reputational risk over working conditions.', '[3]'),
        lambda r: ('Explain how this example illustrates the new international division of labour.', 'Labour-intensive assembly is located in low-wage countries, while design, marketing and headquarters remain in HICs where skilled labour and markets are.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t27b = T('Global production networks and outsourcing of services', 'global production networks outsourcing of services')
B(t27b, {
    'terms': [
        ('global production network', 'the interconnected network of firms, suppliers and workers across several countries involved in making and selling a product'),
        ('outsourcing', 'contracting another firm to carry out work previously done in-house'),
        ('business process outsourcing (BPO)', 'outsourcing services such as call centres, payroll, data processing and IT support, often to India or the Philippines'),
        ('value capture', 'the share of the final value of a product received by each firm or country in the production network'),
        ('just-in-time production', 'delivering components only when needed, reducing stock but making supply chains vulnerable to disruption'),
        ('nearshoring', 'moving production or services to a nearby country, such as US firms moving to Mexico'),
    ],
    'mcq': [
        ('The Philippines and India are major centres for', 'business process outsourcing', ['cocoa growing', 'car design only', 'shipbuilding'], '[1]'),
        ('In global production networks, the largest share of value is usually captured by', 'brand owners, designers and retailers', ['assembly workers', 'raw material miners', 'shipping crews'], '[1]'),
        ('The COVID-19 pandemic exposed the vulnerability of', 'just-in-time global supply chains', ['subsistence farming', 'local markets', 'tourism only'], '[1]'),
        ('Bangalore (Bengaluru) is known as India’s', 'Silicon Valley', ['main port', 'coal capital', 'tea-growing centre'], '[1]'),
    ],
    'explain': [
        ('Explain why services are increasingly outsourced to countries such as India and the Philippines.', 'Lower wages; large English-speaking, educated workforces; time-zone differences allowing 24-hour service; fast internet; government support for IT parks.', '[4]'),
        ('Explain how global production networks distribute value between countries.', 'High-value activities (R&D, design, branding, marketing) are in HICs and capture most value; low-value assembly in LICs captures little; upgrading allows countries to capture more.', '[3]'),
        ('Explain the risks of long global supply chains.', 'Disruption from pandemics, natural disasters, conflict, trade disputes and shipping blockages (Suez 2021); quality control and ethical problems; transport emissions.', '[3]'),
    ],
    'claims': [
        ('Assembly in China captures most of the value of an iPhone.', False, 'Assembly captures only a few per cent; most value goes to Apple and component makers.'),
        ('Some firms are reshoring or nearshoring production.', True, 'Supply-chain risks and rising wages in China encourage this.'),
        ('Outsourcing only involves manufacturing.', False, 'Services such as call centres and software are widely outsourced.'),
    ],
    'essays': [
        ('LICs gain little from participating in global production networks',
         ['They capture a small share of value through low-wage assembly; footloose investment; poor working conditions (Rana Plaza 2013).'],
         ['Jobs, export earnings, skills and technology transfer; upgrading (South Korea, Taiwan, China moved into higher value activities); India’s IT services sector.'],
         'Gains are initially small, but countries that invest in skills and upgrading can capture more value over time.',
         ['value capture', 'upgrading', 'jobs', 'working conditions']),
    ],
})


@data(t27b)
def t27b_value(r, D):
    price = r.choice([400, 700, 1000, 1200])
    shares = {'brand owner (design, software, marketing)': r.randint(30, 45), 'component makers (chips, screen, memory)': r.randint(20, 35),
              'retail and distribution': r.randint(10, 20), 'final assembly': r.choice([2, 3, 4])}
    shares['other costs'] = 100 - sum(shares.values())
    if shares['other costs'] < 2:
        return None
    vals = {k: price * v / 100 for k, v in shares.items()}
    stem = (f'Fig. 27.2 shows the share of the retail price (US${price}) of a smartphone captured at each stage of its global production network: ' + ', '.join(f'{k} {v}%' for k, v in shares.items()) + '.')
    a_ = vals['final assembly']
    if D == 1:
        o, a = mcq(r, f'US${dp(a_, 2)}', [f'US${shares["final assembly"]}', f'US${dp(price * shares["final assembly"] / 10, 0)}', f'US${dp(vals["retail and distribution"], 2)}', f'US${dp(a_ * 2, 2)}'])
        return {'stem': stem + ' How much of the retail price is captured by final assembly?', 'options': o, 'answer': a, 'key': f'{price} × {shares["final assembly"]}% = US${dp(a_, 2)}. [1]'}
    ratio = vals['brand owner (design, software, marketing)'] / a_
    parts = [
        lambda r: ('Calculate the value captured at each stage.', '; '.join(f'{k}: US${dp(v, 2)}' for k, v in vals.items()), '[2]'),
        lambda r: ('Calculate how many times more value the brand owner captures than final assembly.', f'{dp(ratio, 1)} times', '[1]'),
        lambda r: ('Explain why final assembly captures so little value.', 'It is labour-intensive, low-skilled and easily moved; many firms and countries compete for assembly contracts; value lies in design, technology, brands and components.', '[3]'),
        lambda r: ('Explain how a country could capture more value from the production network.', 'Invest in education, R&D and infrastructure to make components and develop brands (upgrading), as in South Korea and Taiwan; attract higher-value FDI; local supplier development.', '[3]'),
        lambda r: ('Suggest why the brand owner keeps design and marketing in its home country.', 'Highly skilled staff, universities and research clusters; protection of intellectual property; close to main markets and headquarters.', '[1]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t27c = T('Impacts of globalisation on host and home countries', 'impacts of globalisation on host home countries')
B(t27c, {
    'terms': [
        ('host country', 'a country that receives investment and operations from a foreign TNC'),
        ('home country', 'the country where a TNC has its headquarters'),
        ('technology transfer', 'the spread of knowledge, skills and technology from foreign firms to local firms and workers'),
        ('race to the bottom', 'competition between countries to attract investment by lowering wages, taxes and environmental standards'),
        ('repatriation of profits', 'the transfer of profits made in a host country back to the TNC’s home country'),
        ('linkages', 'connections between TNC operations and local suppliers and firms'),
    ],
    'mcq': [
        ('The Rana Plaza factory collapse in 2013, which killed over 1100 workers, occurred in', 'Bangladesh', ['China', 'Mexico', 'Vietnam'], '[1]'),
        ('A disadvantage of TNCs for host countries is', 'repatriation of profits to the home country', ['creation of jobs', 'technology transfer', 'export earnings'], '[1]'),
        ('Job losses in a TNC’s home country caused by moving production abroad are an effect of', 'offshoring', ['reshoring', 'agglomeration', 'import substitution'], '[1]'),
        ('Positive impacts of TNCs on host countries include', 'jobs, skills and infrastructure investment', ['higher pollution', 'loss of tax revenue', 'repatriation of profits'], '[1]'),
    ],
    'explain': [
        ('Explain the advantages of TNC investment for host countries.', 'Jobs and higher wages than local firms; skills and technology transfer; infrastructure; export earnings and tax revenue; multiplier effects through local suppliers.', '[4]'),
        ('Explain the disadvantages of TNC investment for host countries.', 'Low wages and poor conditions; profits repatriated; few local linkages; environmental damage; footloose plants may leave; competition harms local firms; political influence.', '[4]'),
        ('Explain the impacts of globalisation on TNC home countries.', 'Profits and dividends flow home; cheaper imports for consumers; high-skilled HQ and R&D jobs; but deindustrialisation and job losses in manufacturing regions, rising inequality.', '[3]'),
    ],
    'claims': [
        ('Globalisation benefits all groups in home countries equally.', False, 'Manufacturing workers may lose jobs while shareholders and consumers gain.'),
        ('TNCs can improve working conditions through codes of conduct.', True, 'After Rana Plaza, the Bangladesh Accord improved factory safety.'),
        ('TNC investment always creates many local linkages.', False, 'Enclave operations may import components and employ few locals.'),
    ],
    'essays': [
        ('host countries gain more than home countries from the activities of TNCs',
         ['Host countries gain jobs, FDI, technology and export growth (China, Vietnam, Ireland); industrialisation reduces poverty.'],
         ['Home countries gain profits, cheaper goods and high-value jobs; host countries face low wages, repatriated profits, environmental damage and dependence.'],
         'Both gain, but unequally; the balance depends on host country policy and the type of investment.',
         ['FDI', 'profits', 'jobs', 'policy']),
    ],
})


@data(t27c)
def t27c_fdi(r, D):
    inv = r.choice([200, 500, 1000, 2500])  # $ million
    jobs = r.choice([800, 1500, 3000, 6000])
    wage = r.choice([2400, 4800, 9000])
    loc = r.randint(15, 60)
    prof = round(inv * r.uniform(0.08, 0.2))
    rep = r.randint(50, 90)
    host = r.choice(['Vietnam', 'Mexico', 'Ethiopia', 'Poland', 'India', 'Morocco'])
    stem = (f'A TNC invested US${inv} million in an electronics factory in {host}. It employs {nf(jobs)} local workers at an average of US${nf(wage)} a year. {loc}% of components are bought from local suppliers. '
            f'Annual profit is US${prof} million, of which {rep}% is repatriated to the home country.')
    wb = jobs * wage / 1e6
    kept = prof * (100 - rep) / 100
    if D == 1:
        o, a = mcq(r, f'US${dp(prof * rep / 100, 1)} million', [f'US${dp(kept, 1)} million', f'US${prof} million', f'US${dp(inv * rep / 100, 0)} million', f'US${dp(prof * rep / 1000, 2)} million'])
        return {'stem': stem + ' How much profit is repatriated each year?', 'options': o, 'answer': a, 'key': f'{prof} × {rep}% = US${dp(prof * rep / 100, 1)} million. [1]'}
    parts = [
        lambda r: ('Calculate the annual wage bill paid to local workers.', f'US${dp(wb, 1)} million', f'{nf(jobs)} × {nf(wage)} [1]'),
        lambda r: ('Calculate the profit repatriated and the profit retained in the host country each year.', f'repatriated US${dp(prof * rep / 100, 1)} million; retained US${dp(kept, 1)} million', '[2]'),
        lambda r: ('Calculate the investment per job created.', f'US${nf(round(inv * 1e6 / jobs))}', f'{inv} million ÷ {nf(jobs)} [1]'),
        lambda r: ('Explain why the share of components bought locally matters for the host country.', 'Local purchases create linkages and multiplier effects, supporting local firms and jobs, and transferring technology and standards; low local content means an enclave with little wider benefit.', '[3]'),
        lambda r: ('Evaluate the benefits of this investment for the host country.', 'Jobs, wages, exports and skills are significant; but most profit leaves, linkages may be limited, and the factory may relocate if costs rise; benefits depend on upgrading and local supplier development.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


CHAPTERS[27] = [t27a, t27b, t27c]


# ============================================================== CHAPTER 28: Regional development

t28a = T('Regional disparities: core-periphery and cumulative causation (Myrdal)', 'regional disparities core-periphery cumulative causation myrdal')
B(t28a, {
    'terms': [
        ('core region', 'a prosperous area with concentrated wealth, investment, population and decision-making'),
        ('periphery', 'a less developed area with lower incomes and out-migration, dependent on the core'),
        ('cumulative causation', 'Myrdal’s (1957) idea that once a region gains an advantage, the multiplier effect attracts further growth, widening disparities'),
        ('backwash effects', 'negative effects of core growth on the periphery, such as out-migration of young skilled workers and capital'),
        ('spread (trickle-down) effects', 'positive effects of core growth on the periphery, such as demand for raw materials and the diffusion of investment'),
        ('Friedmann’s core-periphery model', 'a model (1966) of how the space economy evolves from isolated centres to a single core and periphery, then to an integrated system'),
    ],
    'mcq': [
        ('In Myrdal’s model, the migration of young skilled workers from the periphery to the core is a', 'backwash effect', ['spread effect', 'trickle-down effect', 'multiplier in the periphery'], '[1]'),
        ('The core region of Brazil is', 'the south-east (São Paulo, Rio de Janeiro, Minas Gerais)', ['Amazonas', 'the north-east', 'Roraima'], '[1]'),
        ('Spread effects occur when', 'growth in the core increases demand for products and investment in the periphery', ['the periphery loses workers', 'capital moves to the core', 'factories close in the core'], '[1]'),
        ('Northern Italy is the core and southern Italy (the Mezzogiorno) the periphery. GDP per capita in the south is about', 'half to 60% of that in the north', ['twice that of the north', 'the same as the north', 'less than 10% of the north'], '[1]'),
    ],
    'explain': [
        ('Explain Myrdal’s theory of cumulative causation.', 'A region gains an initial advantage (resources, port, capital); new industry creates jobs and income; the multiplier attracts more firms, services and workers; tax revenue improves infrastructure; growth becomes self-reinforcing while the periphery suffers backwash.', '[4]'),
        ('Explain why regional disparities develop within countries.', 'Physical factors (resources, climate, relief, coasts); historical advantages (colonial ports, capital cities); infrastructure and investment concentrated in core; agglomeration; migration of skilled people; government policy.', '[4]'),
        ('Explain how spread effects can reduce regional disparities.', 'Core growth raises demand for food and raw materials from the periphery; firms relocate to cheaper land and labour; investment and innovation diffuse; remittances.', '[3]'),
    ],
    'claims': [
        ('Regional disparities always narrow over time.', False, 'Cumulative causation can widen them without intervention.'),
        ('Capital cities are often core regions.', True, 'They concentrate government, finance and investment.'),
        ('Backwash effects benefit the periphery.', False, 'They take workers and capital away from the periphery.'),
    ],
    'essays': [
        ('regional disparities within countries are inevitable',
         ['Cumulative causation and agglomeration concentrate growth in core regions; physical advantages persist; disparities are found in almost all countries.'],
         ['Spread effects, regional policy, infrastructure and decentralisation can narrow gaps (Friedmann’s stage 4; EU cohesion funds; China’s western development); some peripheries have grown fast.'],
         'Disparities arise naturally, but their size can be reduced by policy and spread effects.',
         ['cumulative causation', 'policy', 'migration', 'infrastructure']),
    ],
})


@data(t28a)
def t28a_disp(r, D):
    cty, regs = r.choice([('Brazil', ['South-east', 'South', 'Centre-west', 'North', 'North-east']),
                          ('Italy', ['North-west', 'North-east', 'Centre', 'South', 'Islands']),
                          ('China', ['East coast', 'North-east', 'Central', 'West']),
                          ('Thailand', ['Bangkok region', 'Central', 'East', 'North', 'North-east'])])
    v = sorted([round(r.uniform(4, 30), 1) for _ in regs], reverse=True)
    if v[0] / v[-1] < 1.4:
        return None
    m = mean(v)
    s = sd(v)
    cv = s / m * 100
    stem = (f'Table 28.1 shows GDP per capita (thousand US$, PPP) by region in a country similar to {cty}: ' + ', '.join(f'{n} {fmt(x, 1)}' for n, x in zip(regs, v)) + '.')
    ratio = v[0] / v[-1]
    if D == 1:
        o, a = mcq(r, dp(ratio, 2), [dp(v[-1] / v[0], 2), dp(v[0] - v[-1], 1), dp(ratio * 2, 2), dp(v[0] / m, 2)])
        return {'stem': stem + ' What is the ratio of the richest region’s GDP per capita to the poorest region’s?', 'options': o, 'answer': a, 'key': f'{fmt(v[0], 1)} ÷ {fmt(v[-1], 1)} = {dp(ratio, 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the ratio of the richest to the poorest region.', dp(ratio, 2), '[1]'),
        lambda r: (f'The standard deviation is {dp(s, 2)}. Calculate the mean and the coefficient of variation (CV = standard deviation ÷ mean × 100).', f'mean {dp(m, 2)}; CV {dp(cv, 1)}%', '[3]'),
        lambda r: ('Explain how the theory of cumulative causation could account for these disparities.', f'The {regs[0]} region gained an early advantage (port, capital, resources); investment and the multiplier attracted more firms and skilled migrants, while backwash effects drained workers and capital from the {regs[-1]} region.', '[3]'),
        lambda r: ('Suggest why the CV is a better measure of regional disparity than the ratio of richest to poorest.', 'It uses all regions rather than only the extremes and is independent of the units, allowing comparison between countries and over time.', '[2]'),
        lambda r: ('Suggest limitations of using GDP per capita to measure regional disparities.', 'It ignores inequality within regions, the cost of living, the informal economy and other aspects of well-being such as health and education.', '[1]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t28b = T('Policies for regional development and the management of disparities', 'policies for regional development management of disparities')
B(t28b, {
    'terms': [
        ('regional policy', 'government measures to reduce differences in income and employment between regions'),
        ('growth pole', 'a centre where investment is concentrated so that growth spreads to the surrounding region'),
        ('EU Cohesion Fund', 'EU funding for infrastructure and environmental projects in member states with lower GNI per capita'),
        ('decentralisation', 'moving government functions and investment away from the capital or core region'),
        ('Western Development Strategy (China)', 'a programme launched in 2000 to develop China’s western provinces through infrastructure, energy and investment'),
        ('Levelling Up', 'a UK government agenda (2019-24) to reduce regional inequalities, especially between London and the South East and other regions'),
    ],
    'mcq': [
        ('Brasília was built as Brazil’s new capital in 1960 partly to', 'move development into the interior away from the coast', ['strengthen the south-east only', 'reduce the size of Amazonas', 'develop tourism on the coast'], '[1]'),
        ('The Manaus Free Trade Zone, set up in 1967, aims to', 'attract industry to the Amazon region with tax incentives', ['ban industry in the Amazon', 'export only timber', 'protect fishing'], '[1]'),
        ('Italy’s Cassa per il Mezzogiorno (1950-84) was', 'a fund to develop southern Italy', ['a northern bank', 'a tourist board', 'an EU trade agreement'], '[1]'),
        ('China’s Qinghai-Tibet railway, completed in 2006, is an example of', 'infrastructure investment in a peripheral region', ['deindustrialisation', 'a tourism tax', 'a land reform'], '[1]'),
    ],
    'explain': [
        ('Explain the strategies used to reduce regional disparities.', 'Infrastructure (roads, railways, broadband); grants and tax incentives for firms; growth poles and SEZs; relocating government offices; education and training; EU structural funds; controls on growth in the core.', '[4]'),
        ('Explain why regional policies often have limited success.', 'Incentives attract capital-intensive firms with few jobs ("cathedrals in the desert" in southern Italy); corruption; firms leave when grants end; peripheral regions lack skills; core growth continues.', '[3]'),
        ('Explain the growth pole concept.', 'Concentrating investment in a key industry or city creates linkages and multiplier effects that spread growth to surrounding areas over time.', '[3]'),
    ],
    'claims': [
        ('Regional policy always narrows the gap between core and periphery.', False, 'Many gaps, such as in Italy, have persisted.'),
        ('Infrastructure investment can reduce the isolation of peripheral regions.', True, 'Roads, railways and broadband reduce costs and improve access.'),
        ('EU funding has supported development in poorer regions such as Poland.', True, 'Cohesion and structural funds financed major infrastructure.'),
    ],
    'essays': [
        ('top-down regional policies have failed to reduce regional disparities',
         ['Southern Italy remains far poorer despite decades of investment; Brazil’s north-east lags; China’s coastal-inland gap persists.'],
         ['Some policies helped: EU funds in Poland and Ireland, China’s western provinces grew faster than the east after 2000; Brasília and Manaus created new growth centres.'],
         'Results are mixed: policies can raise growth in peripheral regions, but closing gaps fully needs sustained investment, skills and local initiative.',
         ['growth poles', 'infrastructure', 'EU funds', 'local development']),
    ],
})


@data(t28b)
def t28b_conv(r, D):
    yrs = [2000, 2005, 2010, 2015, 2020]
    core0 = round(r.uniform(15, 30), 1)
    per0 = round(core0 / r.uniform(2.5, 4.0), 1)
    gc = r.uniform(3, 6)
    gp = gc + r.uniform(-1, 4)
    core = [round(core0 * (1 + gc / 100) ** (y - 2000), 1) for y in yrs]
    per = [round(per0 * (1 + gp / 100) ** (y - 2000), 1) for y in yrs]
    rat = [c / p for c, p in zip(core, per)]
    plc = r.choice(['eastern and western provinces of China', 'core and periphery of Brazil', 'northern and southern Italy', 'capital region and north-east of Thailand'])
    stem = (f'Table 28.2 shows GDP per capita (thousand US$) in the core region and a peripheral region of a country, similar to the {plc}, after a regional development programme began in 2000: ' +
            '; '.join(f'{y}: core {fmt(c, 1)}, periphery {fmt(p, 1)}' for y, c, p in zip(yrs, core, per)) + '.')
    trend = 'narrowed' if rat[-1] < rat[0] else 'widened'
    if D == 1:
        o, a = mcq(r, dp(rat[-1], 2), [dp(rat[0], 2) if abs(rat[0] - rat[-1]) > 0.01 else dp(rat[-1] + 0.3, 2), dp(core[-1] - per[-1], 1), dp(1 / rat[-1], 2), dp(rat[-1] + 0.5, 2)])
        return {'stem': stem + ' What was the ratio of core to periphery GDP per capita in 2020?', 'options': o, 'answer': a, 'key': f'{fmt(core[-1], 1)} ÷ {fmt(per[-1], 1)} = {dp(rat[-1], 2)}. [1]'}
    parts = [
        lambda r: ('Calculate the ratio of core to periphery GDP per capita in 2000 and 2020, and state whether the relative gap has narrowed or widened.', f'{dp(rat[0], 2)} and {dp(rat[-1], 2)}: the relative gap {trend}', '[3]'),
        lambda r: ('Calculate the absolute gap in GDP per capita in 2000 and 2020.', f'{dp(core[0] - per[0], 1)} and {dp(core[-1] - per[-1], 1)} thousand US$', '[2]'),
        lambda r: ('Explain why the absolute gap can widen even when the relative gap narrows.', 'The core starts from a much higher base, so a smaller percentage growth still adds more dollars than faster growth in the periphery.', '[2]'),
        lambda r: ('Suggest policies that might have influenced the trend.', 'Infrastructure (roads, railways, broadband), tax incentives and SEZs in the periphery, relocating state firms and offices, education spending, transfers and investment in energy and resources.', '[3]'),
    ]
    return compose(r, stem, parts, k=kk(D), type_='numerical')


t28c = T('Case study of regional development within a country', 'case study of regional development within a country')
B(t28c, {
    'terms': [
        ('Mezzogiorno', 'southern Italy, including Sicily and Sardinia, historically poorer than the north'),
        ('Go West (Western Development) policy', 'China’s strategy from 2000 to develop the western provinces, including Sichuan, Xinjiang, Tibet and Chongqing'),
        ('SUDENE', 'a Brazilian agency (1959) set up to promote development in the north-east'),
        ('cathedral in the desert', 'a large capital-intensive industrial plant built in a peripheral region with few local linkages, such as the Taranto steelworks in southern Italy'),
        ('hukou system', 'China’s household registration system, which has limited the rights of rural migrants in cities'),
        ('regional convergence', 'the narrowing of differences in income between regions over time'),
    ],
    'mcq': [
        ('The Taranto steelworks in southern Italy is often given as an example of', 'a “cathedral in the desert”', ['a growth pole that eliminated poverty', 'a tourist resort', 'a nature reserve'], '[1]'),
        ('China’s Western Development Strategy was launched in', '2000', ['1949', '1978', '2015'], '[1]'),
        ('Chongqing became a municipality directly under central government in', '1997', ['1900', '1949', '2020'], '[1]'),
        ('Brazil’s north-east region has long suffered from', 'drought, poverty and out-migration', ['excessive industrial pollution only', 'cold winters', 'glaciers'], '[1]'),
    ],
    'explain': [
        ('Explain the reasons for regional disparities in a named country.', 'Physical factors (relief, climate, resources); historical concentration of industry and ports; infrastructure; migration of skilled workers; cumulative causation; government policy (e.g. China’s coastal SEZs after 1978).', '[4]'),
        ('Explain why the Mezzogiorno has remained poorer than northern Italy.', 'Distance from European markets; large capital-intensive plants with few jobs; organised crime and corruption; poor infrastructure; out-migration of young people; weaker institutions.', '[3]'),
        ('Explain the impacts of China’s Western Development Strategy.', 'Huge investment in roads, railways, airports and energy (West-East gas pipeline, Qinghai-Tibet railway); faster growth in western provinces after 2000; cities such as Chengdu and Chongqing boomed; but environmental damage, ethnic tensions and gaps in incomes remain.', '[3]'),
    ],
    'claims': [
        ('Southern Italy has caught up with the north.', False, 'GDP per capita in the south is still only around half to 60% of that of the north.'),
        ('Western Chinese provinces grew faster than the east in parts of the 2000s and 2010s.', True, 'Infrastructure and investment raised growth rates in the west.'),
        ('Brasília’s construction moved Brazil’s core to the interior.', False, 'The south-east remains the economic core, though the centre-west has grown.'),
    ],
    'cs': [
        ('regional development within a country', [
            ('Italy (the Mezzogiorno)', {'strategy': 'Cassa per il Mezzogiorno (1950-84): land reform, roads, irrigation and large state industrial plants (Taranto steelworks, petrochemicals in Sicily and Sardinia); later EU structural and cohesion funds; motorways such as the A2 to Reggio Calabria.',
                                         'evaluate': 'Infrastructure and living standards improved, but GDP per capita remains about half to 60% of the north; plants created few linked jobs ("cathedrals in the desert"); corruption and organised crime diverted funds; out-migration continues.'}),
            ('China (Western Development Strategy)', {'strategy': 'From 2000: investment in infrastructure (Qinghai-Tibet railway 2006, highways, airports), West-East gas pipeline and electricity transmission, Chongqing and Chengdu as growth poles, tax incentives, ecological programmes such as Grain for Green.',
                                                      'evaluate': 'Western provinces grew faster than the coast in parts of the 2000s and 2010s and inland cities attracted manufacturing; but the absolute gap remains large, much investment is state-led and capital-intensive, and environmental and ethnic tensions have increased.'}),
            ('Brazil (the North and North-east)', {'strategy': 'SUDENE (1959) for the north-east; Brasília (1960) and roads such as the Trans-Amazonian Highway; Manaus Free Trade Zone (1967) with tax incentives for electronics and motorcycle assembly; Bolsa Família cash transfers from 2003.',
                                                   'evaluate': 'Manaus has over 500 factories and about 2 million people; poverty in the north-east fell after 2003; but the south-east still dominates GDP, Manaus depends on tax incentives, and Amazon roads encouraged deforestation.'}),
        ], [
            ('describe the strategies used to promote regional development', 'strategy', 'Named policies, dates, places and scale.'),
            ('evaluate the success of these strategies', 'evaluate', 'Evidence of convergence or not; social, economic and environmental outcomes.', 'evaluate the extent to which regional disparities have been reduced.'),
        ]),
    ],
    'essays': [
        ('regional disparities are best reduced by investment in infrastructure',
         ['Roads, railways, energy and broadband reduce isolation and costs (China’s western railways, EU-funded motorways); attract firms and tourism.'],
         ['Infrastructure alone can increase backwash by making it easier to serve the periphery from the core; education, health, local enterprise, governance and cash transfers (Bolsa Família) may be more effective.'],
         'Infrastructure is necessary but not sufficient; it must be combined with investment in people and institutions.',
         ['infrastructure', 'education', 'growth poles', 'governance']),
    ],
})


CHAPTERS[28] = [t28a, t28b, t28c]


# ============================================================== essay slots
# In A2 mocks the extended-response slots ask for 15-25 marks; only the 20-mark essays (and full case-study
# questions) should fill them, so every other C3/C4 template stands aside when 12 or more marks are wanted.

def _guard(fn):
    def g(r, D, fn=fn):
        if (_as.CTX.get('want_marks') or 0) >= 12:
            return None
        return fn(r, D)
    g.__name__ = getattr(fn, '__name__', 'tpl')
    return g


for _topics in CHAPTERS.values():
    for _t in _topics:
        for _tp in _t.templates:
            if _tp.C in ('C3', 'C4') and _tp.name not in ('essay', 'essay3', 'cs', 'cs3') and not getattr(_tp, '_guarded', False):
                _tp.fn = _guard(_tp.fn)
                _tp._guarded = True
