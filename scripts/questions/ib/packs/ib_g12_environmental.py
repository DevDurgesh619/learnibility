"""IB DP Environmental Systems and Societies SL/HL (guide for first assessment 2026) - ib-g12-environmental, year 2.

Year 2 covers Topic 5 Land (5.1 Soil, 5.2 Agriculture and food), Topic 6 Atmosphere and climate change (6.1-6.4),
Topic 7 Natural resources (7.1 Natural resources, 7.2 Energy, 7.3 Solid waste), Topic 8 Human populations and urban
systems (8.1-8.3), the HL lenses (environmental law, environmental economics, environmental ethics) and the internal
assessment (individual investigation).

Same item styles and mock structure as year 1 (machinery imported from ib_g11_environmental.py). Parametric
generators COMPUTE: soil loss vs formation and soil texture class, energy efficiency of diets and land per person,
ozone depletion and ODS decay, CO₂ growth rate, radiative forcing, CO₂-equivalents with GWP100, remaining carbon budget,
reserves-to-production ratio, capacity factor and energy mix, waste generation and landfill life, CBR/CDR/NIR/doubling
time/TFR and dependency ratio, urban growth, PM2.5 against WHO guidelines, external cost and Pigouvian tax, discounting
of ecosystem services, Spearman's rank, chi-squared, mean / standard deviation and the t-test.
"""
from __future__ import annotations

import math

from _common import name
from ib_g11_environmental import (CONFIG, GENS, MB9, MOCK, Pack, comma, gen, mk, pick)  # noqa: F401

P = Pack()
S = P.S
R = P.R


def init(subject_id):
    pass


def templates(st):
    return P.templates(st)


# =============================================================================================
# Parametric generators - every answer is computed
# =============================================================================================
SOIL_SITES = [('a maize field on a 6° slope in the Ethiopian Highlands', 'tilled with no conservation measures'),
              ('a vineyard on a hillside in the Douro valley, Portugal', 'bare soil between rows'),
              ('a cassava plot cleared from forest in Rwanda', 'cultivated up and down the slope'),
              ('a wheat field on the Loess Plateau, China', 'before terracing'),
              ('an overgrazed rangeland in Inner Mongolia', 'with patchy grass cover'),
              ('a soybean field in Mato Grosso, Brazil', 'after the first rains')]


@gen('soil_loss', d=(1, 5))
def g_soil_loss(rng, slot):
    site, cond = pick(rng, SOIL_SITES)
    loss = rng.choice([5, 8, 12, 15, 20, 30, 45, 60])
    form = rng.choice([0.5, 1.0])
    bulk = rng.choice([1.2, 1.3, 1.4])  # t/m³
    depth_mm = loss / (bulk * 10)  # 1 mm over 1 ha = 10 m³
    if slot.d <= 2:
        return dict(stem=f'Soil loss from {site}, {cond}, was measured at {loss} t ha⁻¹ yr⁻¹. Soil forms at about {form} t ha⁻¹ yr⁻¹. Calculate how many times faster soil is being lost than formed.',
                    answer=f'{loss} / {form} = {loss / form:g} times faster', markingKey=f'M1 loss ÷ formation; A1 {loss / form:g}.', marks=mk(slot, 2))
    topsoil = rng.choice([150, 200, 250, 300])
    yrs = topsoil / depth_mm
    red = rng.choice([50, 70, 80, 90])
    return dict(stem=f'Soil loss from {site}, {cond}, is {loss} t ha⁻¹ yr⁻¹. The soil bulk density is {bulk} t m⁻³ and the topsoil is {topsoil} mm deep (1 mm of soil over 1 ha = 10 m³). (a) Calculate the depth of soil lost per year in mm. (b) Calculate how long the topsoil would last. (c) Contour ploughing and cover crops are expected to cut erosion by {red}%. Calculate the new loss and evaluate whether this would be sustainable if soil forms at {form} t ha⁻¹ yr⁻¹.',
                answer=f'(a) {loss} t ÷ {bulk} t m⁻³ = {loss / bulk:.1f} m³ per ha = {depth_mm:.2f} mm per year (b) {topsoil} / {depth_mm:.2f} ≈ {yrs:.0f} years (c) {loss * (1 - red / 100):.1f} t ha⁻¹ yr⁻¹; ' + ('still above the formation rate, so not yet sustainable - further measures (terracing, agroforestry) are needed' if loss * (1 - red / 100) > form else 'at or below the formation rate, so sustainable'),
                markingKey=f'(a) M1 mass ÷ density, A1 {depth_mm:.2f} mm. (b) A1 ≈ {yrs:.0f} years. (c) A1 {loss * (1 - red / 100):.1f}; R1 comparison with formation rate.', marks=mk(slot, 6))


TEXTURE_RULES = ('Simplified classification: clay ≥ 40%; sand ≥ 85%; silt ≥ 80%; loam if sand 23-52%, silt 28-50% and clay 7-27%; '
                 'sandy loam if sand 52-85% and clay < 20%; otherwise clay loam.')


def texture(sa, si, cl):
    if cl >= 40:
        return 'clay'
    if sa >= 85:
        return 'sand'
    if si >= 80:
        return 'silt'
    if 23 <= sa <= 52 and 28 <= si <= 50 and 7 <= cl <= 27:
        return 'loam'
    if 52 < sa < 85 and cl < 20:
        return 'sandy loam'
    return 'clay loam'


@gen('soil_texture', d=(1, 4))
def g_soil_texture(rng, slot):
    who = name(rng)
    tot = rng.choice([50, 80, 100, 120, 200])
    profile = pick(rng, [(40, 40, 20), (88, 7, 5), (20, 30, 50), (65, 25, 10), (10, 82, 8), (30, 35, 35), (45, 40, 15)])
    sa_g, si_g = round(tot * profile[0] / 100), round(tot * profile[1] / 100)
    cl_g = tot - sa_g - si_g
    sa, si, cl = sa_g / tot * 100, si_g / tot * 100, cl_g / tot * 100
    cls = texture(sa, si, cl)
    loc = pick(rng, ['a school garden in Lyon', 'a rice paddy in the Philippines', 'a dune slack in Wales', 'a vegetable plot in Nairobi', 'a floodplain field in Bangladesh', 'a forest clearing in Ontario'])
    if slot.d <= 2:
        return dict(stem=f'{who} separated a {tot} g soil sample from {loc} by sedimentation and sieving: sand {sa_g} g, silt {si_g} g, clay {cl_g} g. Calculate the percentage of each fraction.',
                    answer=f'sand {sa:.0f}%, silt {si:.0f}%, clay {cl:.0f}%', markingKey='M1 mass of fraction ÷ total × 100; A1 all three correct.', marks=mk(slot, 2))
    props = {'clay': 'high water and nutrient retention but poor drainage and aeration; heavy to work',
             'sand': 'good drainage and aeration but low water and nutrient retention; easily leached',
             'silt': 'holds water well and is fertile but compacts and is easily eroded',
             'loam': 'balanced drainage, water retention and nutrient-holding capacity - ideal for most crops',
             'sandy loam': 'drains well and warms quickly; moderate fertility, needs organic matter',
             'clay loam': 'good nutrient retention, moderate drainage; can become waterlogged'}
    return dict(stem=f'A {tot} g soil sample from {loc} contained sand {sa_g} g, silt {si_g} g and clay {cl_g} g. {TEXTURE_RULES} (a) Calculate the percentage composition and classify the soil. (b) Describe how this texture affects its suitability for agriculture. (c) Suggest one way to improve it.',
                answer=f'(a) sand {sa:.0f}%, silt {si:.0f}%, clay {cl:.0f}% → {cls} (b) {props[cls]} (c) e.g. add organic matter (compost, manure) to improve structure, water retention and drainage; liming or drainage where needed.',
                markingKey=f'(a) A1 percentages, A1 {cls}. (b) R1 R1 properties linked to texture. (c) R1 valid improvement.', marks=mk(slot, 5))


DIETS = [('wheat grain', 3400), ('maize', 3650), ('rice', 3600), ('soybeans', 4460)]  # kcal per kg (approx)


def pp(x):
    v = f'{x:,.1f}' if x < 10 else f'{x:,.0f}'
    return v + (' person' if v in ('1', '1.0') else ' people')


@gen('diet_energy', d=(1, 5))
def g_diet_energy(rng, slot):
    crop, kcal = pick(rng, DIETS)
    area = rng.choice([1, 2, 5, 10, 50])
    yld = rng.choice([3, 4, 5, 6, 7, 8])  # t/ha
    eff = rng.choice([5, 8, 10, 12, 15])
    need = 2500 * 365
    direct = area * yld * 1000 * kcal
    people_d = direct / need
    people_m = people_d * eff / 100
    if slot.d <= 2:
        return dict(stem=f'One hectare of {crop} yields {yld} t, containing about {comma(kcal)} kcal per kg. Calculate the total food energy produced per hectare.',
                    answer=f'{yld} × 1,000 kg × {comma(kcal)} kcal = {yld * 1000 * kcal:,.0f} kcal per ha', markingKey='M1 convert t to kg; A1 correct total.', marks=mk(slot, 2))
    return dict(stem=f'A farm of {area} ha produces {yld} t ha⁻¹ of {crop} ({comma(kcal)} kcal per kg). A person needs about 2,500 kcal per day. (a) Calculate how many people the crop could feed for a year if eaten directly. (b) If the crop is fed to livestock with an energy conversion efficiency of {eff}%, calculate how many people the resulting meat could feed. (c) Explain these results using ecological principles and discuss one reason why livestock farming may still be appropriate in some places.',
                answer=f'(a) {area} × {yld} × 1,000 × {comma(kcal)} = {direct:,.0f} kcal ÷ (2,500 × 365) ≈ {people_d:,.0f} people (b) {people_d:,.1f} × {eff / 100:g} ≈ {pp(people_m)} (c) each extra trophic level loses most energy as heat in respiration (second law), so eating producers supports more people; however, grazing animals can convert grass on land unsuitable for crops (steep, arid rangeland) into food and provide manure, income and nutrients.',
                markingKey=f'(a) M1 total energy ÷ annual need, A1 ≈ {people_d:,.0f}. (b) A1 ≈ {pp(people_m)}. (c) R1 energy loss between trophic levels, R1 valid reason for livestock.', marks=mk(slot, 6))


@gen('yield_change', d=(1, 4))
def g_yield_change(rng, slot):
    c = pick(rng, [('India', 'wheat', 0.8, 3.5), ('Mexico', 'wheat', 0.75, 5.3), ('China', 'rice', 2.0, 7.0), ('Ethiopia', 'maize', 1.0, 4.2),
                   ('Brazil', 'soybeans', 1.1, 3.4), ('Vietnam', 'rice', 1.9, 6.0)])
    country, crop, y0, y1 = c
    y0 = round(y0 * rng.uniform(0.9, 1.1), 2)
    y1 = round(y1 * rng.uniform(0.9, 1.1), 2)
    a, b = rng.choice([(1961, 2020), (1965, 2015), (1970, 2020)])
    pct = (y1 - y0) / y0 * 100
    if slot.d <= 2:
        return dict(stem=f'Average {crop} yields in {country} rose from about {y0} t ha⁻¹ in {a} to {y1} t ha⁻¹ in {b}. Calculate the percentage increase.',
                    answer=f'({y1} − {y0}) / {y0} × 100 = {pct:.0f}%', markingKey=f'M1 change ÷ original × 100; A1 {pct:.0f}%.', marks=mk(slot, 2))
    rate = ((y1 / y0) ** (1 / (b - a)) - 1) * 100
    return dict(stem=f'Average {crop} yields in {country} rose from about {y0} t ha⁻¹ in {a} to {y1} t ha⁻¹ in {b}. (a) Calculate the percentage increase and the mean annual compound growth rate. (b) Outline three inputs that explain this increase. (c) Evaluate the environmental sustainability of these changes.',
                answer=f'(a) {pct:.0f}%; ({y1}/{y0})^(1/{b - a}) − 1 ≈ {rate:.2f}% per year (b) high-yielding varieties (Green Revolution), synthetic fertilisers, irrigation, pesticides and mechanisation (c) more food from less land spared habitat, but costs include groundwater depletion (Punjab), eutrophication, soil degradation, loss of crop genetic diversity and high fossil-fuel inputs.',
                markingKey=f'(a) A1 {pct:.0f}%, A1 {rate:.2f}%. (b) R1 ×3. (c) R1 benefit, R1 cost.', marks=mk(slot, 6))


@gen('ozone', d=(1, 5))
def g_ozone(rng, slot):
    base = rng.choice([300, 320, 330, 350])
    low = rng.choice([92, 100, 110, 125, 140, 160])
    pct = (base - low) / base * 100
    yr = rng.choice([1993, 1998, 2000, 2006, 2015, 2020, 2023])
    if slot.d <= 2:
        return dict(stem=f'Total column ozone over Halley Research Station, Antarctica, averaged about {base} Dobson units (DU) in October before 1975, but fell to {low} DU in October {yr}. Calculate the percentage depletion. (The ozone "hole" is defined as < 220 DU.)',
                    answer=f'({base} − {low}) / {base} × 100 = {pct:.0f}% depletion; below 220 DU so within the ozone hole',
                    markingKey=f'M1 change ÷ original × 100; A1 {pct:.0f}%.', marks=mk(slot, 2))
    gas, life = pick(rng, [('CFC-11', 52), ('CFC-12', 102), ('CFC-113', 93), ('carbon tetrachloride', 32), ('halon-1301', 72)])
    c0 = rng.choice([200, 250, 300, 500, 550])
    t = rng.choice([20, 30, 40, 50])
    c1 = c0 * math.exp(-t / life)
    return dict(stem=f'(a) October ozone over Antarctica fell from {base} DU (pre-1975) to {low} DU in {yr}. Calculate the percentage depletion. (b) {gas} has an atmospheric lifetime of about {life} years; after emissions stopped its concentration falls as C = C₀e^(−t/τ). If the concentration was {c0} ppt when emissions ended, calculate the concentration after {t} years. (c) Use your answer to explain why ozone recovery is slow despite the Montreal Protocol.',
                answer=f'(a) {pct:.0f}% (b) {c0} × e^(−{t}/{life}) ≈ {c1:.0f} ppt (c) ODS persist for decades, so chlorine and bromine continue to destroy ozone long after production stops; full recovery of the Antarctic hole is expected around 2066 (WMO/UNEP 2022).',
                markingKey=f'(a) A1 {pct:.0f}%. (b) M1 substitution, A1 ≈ {c1:.0f} ppt. (c) R1 long lifetimes / catalytic destruction continues, R1 recovery date or time lag.', marks=mk(slot, 5))


MAUNA = [(1960, 316.9), (1970, 325.7), (1980, 338.8), (1990, 354.4), (2000, 369.7), (2010, 389.9), (2015, 401.0), (2020, 414.2), (2023, 421.1)]


@gen('co2_rate', d=(1, 4))
def g_co2_rate(rng, slot):
    i, j = sorted(rng.sample(range(len(MAUNA)), 2))
    (a, ca), (b, cb) = MAUNA[i], MAUNA[j]
    rate = (cb - ca) / (b - a)
    if slot.d <= 2:
        return dict(stem=f'Annual mean CO₂ concentration at Mauna Loa Observatory (NOAA) was {ca} ppm in {a} and {cb} ppm in {b}. Calculate the mean rate of increase in ppm per year.',
                    answer=f'({cb} − {ca}) / ({b} − {a}) = {rate:.2f} ppm per year', markingKey=f'M1 change ÷ time; A1 {rate:.2f}.', marks=mk(slot, 2))
    tab = '; '.join(f'{y}: {c}' for y, c in MAUNA)
    r1_ = (MAUNA[3][1] - MAUNA[0][1]) / 30
    r2_ = (MAUNA[7][1] - MAUNA[3][1]) / 30
    yrs450 = (450 - MAUNA[-1][1]) / ((MAUNA[-1][1] - MAUNA[-3][1]) / 8)
    return dict(stem=f'Annual mean CO₂ at Mauna Loa (ppm): {tab}. (a) Calculate the mean rate of increase for 1960-1990 and for 1990-2020 and comment on the trend. (b) Using the 2015-2023 rate, estimate the year in which 450 ppm will be reached. (c) Explain the small seasonal cycle superimposed on this trend.',
                answer=f'(a) {r1_:.2f} ppm/yr and {r2_:.2f} ppm/yr - the rate of increase is accelerating as emissions grew (b) rate = ({MAUNA[-1][1]} − {MAUNA[-3][1]})/8 = {(MAUNA[-1][1] - MAUNA[-3][1]) / 8:.2f} ppm/yr; (450 − {MAUNA[-1][1]})/rate ≈ {yrs450:.0f} years → about {2023 + round(yrs450)} (c) Northern Hemisphere vegetation draws down CO₂ by photosynthesis in summer and releases it by respiration/decomposition in winter.',
                markingKey=f'(a) A1 {r1_:.2f}, A1 {r2_:.2f}, R1 acceleration. (b) A1 ≈ {2023 + round(yrs450)}. (c) R1 seasonal photosynthesis vs respiration.', marks=mk(slot, 6))


@gen('forcing', d=(2, 5))
def g_forcing(rng, slot):
    c0 = 280
    c = rng.choice([350, 380, 400, 420, 450, 560, 700])
    dF = 5.35 * math.log(c / c0)
    lam = rng.choice([0.5, 0.8])
    dT = lam * dF
    if slot.d <= 3:
        return dict(stem=f'The radiative forcing from CO₂ can be estimated by ΔF = 5.35 ln(C/C₀) W m⁻², where C₀ = 280 ppm (pre-industrial). Calculate ΔF when CO₂ reaches {c} ppm.',
                    answer=f'5.35 × ln({c}/280) = {dF:.2f} W m⁻²', markingKey=f'M1 substitution; A1 {dF:.2f} W m⁻².', marks=mk(slot, 2 if slot.d <= 2 else 3))
    return dict(stem=f'Radiative forcing from CO₂ is ΔF = 5.35 ln(C/280) W m⁻², and equilibrium warming is ΔT ≈ λΔF with climate sensitivity parameter λ = {lam} K per W m⁻². (a) Calculate ΔF and ΔT for C = {c} ppm. (b) Calculate ΔT for a doubling of CO₂ (560 ppm). (c) Explain why actual warming may differ from these estimates.',
                answer=f'(a) ΔF = {dF:.2f} W m⁻²; ΔT = {dT:.1f} K (b) 5.35 ln 2 = {5.35 * math.log(2):.2f} W m⁻² → {lam * 5.35 * math.log(2):.1f} K (c) other greenhouse gases and aerosols add or offset forcing; feedbacks (water vapour, ice-albedo, clouds) are uncertain; oceans delay warming (thermal inertia), so the climate is not yet at equilibrium.',
                markingKey=f'(a) A1 {dF:.2f}, A1 {dT:.1f}. (b) A1 {lam * 5.35 * math.log(2):.1f} K. (c) R1 R1 valid reasons.', marks=mk(slot, 6))


@gen('co2e', d=(1, 5))
def g_co2e(rng, slot):
    who = pick(rng, ['a dairy farm in New Zealand', 'a rice-growing district in Bangladesh', 'a landfill site near Lagos', 'a beef ranch in Argentina',
                     'a natural-gas field with leaking pipelines', 'a fertilised wheat farm in Canada'])
    co2 = rng.randint(100, 5000)
    ch4 = rng.randint(10, 400)
    n2o = rng.randint(1, 40)
    g_ch4, g_n2o = 28, 265
    tot = co2 + ch4 * g_ch4 + n2o * g_n2o
    if slot.d <= 2:
        return dict(stem=f'Each year {who} emits {ch4} t of methane (GWP₁₀₀ = {g_ch4}). Calculate the emission in tonnes of CO₂-equivalent.',
                    answer=f'{ch4} × {g_ch4} = {ch4 * g_ch4:,} t CO₂e', markingKey='M1 mass × GWP; A1 correct.', marks=mk(slot, 2))
    share = ch4 * g_ch4 / tot * 100
    big = max([('CO₂', co2), ('CH₄', ch4 * g_ch4), ('N₂O', n2o * g_n2o)], key=lambda x: x[1])[0]
    return dict(stem=f'Annual emissions from {who}: CO₂ {co2:,} t; CH₄ {ch4} t; N₂O {n2o} t. Using GWP₁₀₀ values of CH₄ = {g_ch4} and N₂O = {g_n2o}: (a) calculate total emissions in t CO₂e; (b) calculate the percentage contributed by methane and identify the largest contributor; (c) explain why methane is sometimes evaluated using GWP₂₀ (about 80) and what this implies for mitigation priorities.',
                answer=f'(a) {co2:,} + {ch4} × {g_ch4} + {n2o} × {g_n2o} = {tot:,} t CO₂e (b) methane {share:.0f}%; largest: {big} (c) methane has a short lifetime (~12 years) but is very potent, so over 20 years its warming effect is about 80 times CO₂; cutting methane (leaks, landfill, livestock) gives rapid near-term cooling, as targeted by the Global Methane Pledge (30% by 2030).',
                markingKey=f'(a) M1 × GWPs, A1 {tot:,}. (b) A1 {share:.0f}%, A1 {big}. (c) R1 short lifetime / high potency, R1 implication.', marks=mk(slot, 6))


@gen('carbon_budget_left', d=(1, 5))
def g_budget(rng, slot):
    budget = rng.choice([250, 300, 380, 400, 500, 1150])  # Gt CO2
    tgt = '1.5 °C (50% probability)' if budget <= 500 else '2 °C (67% probability)'
    em = rng.choice([36.8, 37.4, 40.0, 41.6, 42.0])
    yrs = budget / em
    if slot.d <= 2:
        return dict(stem=f'An estimate of the remaining carbon budget for limiting warming to {tgt} is about {budget} Gt CO₂. Global CO₂ emissions are about {em} Gt per year. Calculate how many years of current emissions the budget represents.',
                    answer=f'{budget} / {em} ≈ {yrs:.1f} years', markingKey=f'M1 budget ÷ annual emissions; A1 {yrs:.1f}.', marks=mk(slot, 2))
    n = budget / (em / 2)  # linear decline to zero uses budget when area = em*n/2
    pc = rng.choice([(14.9, 'the USA'), (8.0, 'China'), (2.0, 'India'), (7.6, 'Germany'), (0.4, 'Nigeria'), (15.3, 'Australia')])
    return dict(stem=f'The remaining carbon budget for {tgt} is about {budget} Gt CO₂ and global emissions are {em} Gt CO₂ per year. (a) Calculate how long the budget would last at constant emissions. (b) If emissions instead fall linearly to zero, calculate the year by which net zero must be reached (start in 2025). (c) Per-capita emissions in {pc[1]} are about {pc[0]} t CO₂. Discuss how the remaining budget could be shared fairly between countries.',
                answer=f'(a) {yrs:.1f} years (b) area of triangle: {budget} = {em} × n / 2 → n = {n:.1f} years → net zero by about {2025 + round(n)} (c) approaches include equal per-capita shares, historical responsibility (high-income countries emitted most cumulative CO₂), capability to pay, and the right to development; {pc[1]}\'s per-capita emissions of {pc[0]} t compared with a world average of about 4.7 t illustrate unequal responsibility.',
                markingKey=f'(a) A1 {yrs:.1f}. (b) M1 triangle area, A1 ≈ {2025 + round(n)}. (c) R1 equity principle, R1 use of per-capita data / common but differentiated responsibilities.', marks=mk(slot, 6))


RES_RP = [('world oil', 1732, 34.0, 'billion barrels', 'billion barrels'), ('world natural gas', 188, 4.0, 'trillion m³', 'trillion m³'),
          ('world coal', 1074, 8.7, 'billion t', 'billion t'), ('world lithium', 28, 0.18, 'million t', 'million t'),
          ('world copper', 1000, 22, 'million t', 'million t'), ('world phosphate rock', 74000, 220, 'million t', 'million t')]


@gen('rp_ratio', d=(1, 5))
def g_rp(rng, slot):
    what, res, prod, u, pu = pick(rng, RES_RP)
    res = round(res * rng.uniform(0.9, 1.1), 1 if res < 100 else 0)
    prod = round(prod * rng.uniform(0.9, 1.1), 2)
    rp = res / prod
    if slot.d <= 2:
        return dict(stem=f'Proven reserves of {what} are about {res:,} {u} and annual production is about {prod} {pu}. Calculate the reserves-to-production (R/P) ratio.',
                    answer=f'{res:,} / {prod} ≈ {rp:.0f} years', markingKey=f'M1 reserves ÷ annual production; A1 ≈ {rp:.0f} years.', marks=mk(slot, 2))
    g = rng.choice([1, 2, 3])
    yrs = math.log(1 + g / 100 * rp) / math.log(1 + g / 100)
    return dict(stem=f'Proven reserves of {what} are {res:,} {u}; production is {prod} {pu} per year. (a) Calculate the static R/P ratio. (b) If production grows by {g}% per year, the reserves last n years where n = ln(1 + g·R/P)/ln(1 + g) (g as a decimal). Calculate n. (c) Explain why R/P ratios are poor predictors of when a resource will run out.',
                answer=f'(a) ≈ {rp:.0f} years (b) n = ln(1 + {g / 100} × {rp:.0f}) / ln(1.{g:02d}) ≈ {yrs:.0f} years (c) reserves change with prices, technology and new discoveries (dynamic nature of resources); demand changes with substitution and policy (e.g. phasing out coal); recycling extends supply; some reserves become uneconomic.',
                markingKey=f'(a) A1 {rp:.0f}. (b) M1 substitution, A1 ≈ {yrs:.0f}. (c) R1 R1 dynamic reserves / demand changes.', marks=mk(slot, 6))


PLANTS = [('an offshore wind farm in the North Sea', 'wind', (0.35, 0.50)), ('an onshore wind farm in Texas', 'wind', (0.30, 0.40)),
          ('a solar PV park in Rajasthan', 'solar PV', (0.18, 0.25)), ('a solar PV farm in Germany', 'solar PV', (0.10, 0.13)),
          ('a nuclear power station in France', 'nuclear', (0.70, 0.90)), ('a hydroelectric dam in Norway', 'hydro', (0.40, 0.55)),
          ('a geothermal plant in Iceland', 'geothermal', (0.80, 0.92))]


@gen('capacity_factor', d=(1, 5))
def g_cf(rng, slot):
    plant, src, (lo, hi) = pick(rng, PLANTS)
    cap = rng.choice([50, 120, 300, 500, 1000, 1600])
    cf = round(rng.uniform(lo, hi), 2)
    gwh = cap * 8760 * cf / 1000
    if slot.d <= 2:
        return dict(stem=f'{plant[0].upper() + plant[1:]} has an installed capacity of {cap} MW and generated {gwh:,.0f} GWh in a year (8,760 hours). Calculate its capacity factor.',
                    answer=f'{gwh:,.0f} GWh / ({cap} MW × 8,760 h / 1,000) = {cf:.2f} ({cf * 100:.0f}%)', markingKey=f'M1 actual ÷ maximum possible output; A1 {cf * 100:.0f}%.', marks=mk(slot, 2))
    ef = rng.choice([0.82, 0.9, 0.95])  # t CO2 / MWh for coal
    saved = gwh * 1000 * ef / 1e6
    homes = gwh * 1e6 / rng.choice([3500, 4000, 4500])
    return dict(stem=f'{plant[0].upper() + plant[1:]} has an installed capacity of {cap} MW and a capacity factor of {cf * 100:.0f}%. (a) Calculate its annual electricity generation in GWh. (b) Calculate the CO₂ avoided if this electricity replaces coal generation emitting {ef} t CO₂ per MWh. (c) Explain why the capacity factor of {src} differs from that of other sources and discuss one implication for energy security.',
                answer=f'(a) {cap} × 8,760 × {cf} / 1,000 = {gwh:,.0f} GWh (b) {gwh:,.0f} × 1,000 MWh × {ef} = {saved:.2f} million t CO₂ (c) ' + ('intermittent output depends on wind speed or sunlight (night, cloud, calm), so storage, grid interconnection or back-up are needed' if src in ('wind', 'solar PV') else 'it can run continuously (baseload) apart from maintenance, giving reliable supply, though it is less flexible or depends on water availability'),
                markingKey=f'(a) M1 capacity × hours × CF, A1 {gwh:,.0f}. (b) A1 {saved:.2f} Mt. (c) R1 reason for CF, R1 security implication.', marks=mk(slot, 6))


MIX = [('Norway', [('hydro', 88), ('wind', 10), ('fossil', 2)]), ('France', [('nuclear', 65), ('hydro', 12), ('wind and solar', 13), ('fossil', 10)]),
       ('Poland', [('coal', 61), ('gas', 9), ('wind and solar', 22), ('oil and other fossil', 8)]), ('India', [('coal', 74), ('hydro', 8), ('wind and solar', 12), ('nuclear', 3), ('gas and oil', 3)]),
       ('Brazil', [('hydro', 61), ('wind and solar', 20), ('biomass', 8), ('fossil', 11)]), ('Kenya', [('geothermal', 45), ('hydro', 22), ('wind and solar', 20), ('fossil', 13)])]


MIXF = {'Norway': 'abundant rainfall and steep mountain valleys give large hydropower potential; oil and gas are exported rather than used for electricity; strong public support for renewables',
        'France': 'the Messmer plan after the 1973 oil crisis built a large nuclear fleet because France lacked domestic fossil fuels; state ownership (EDF); Alpine and Pyrenean rivers for hydro',
        'Poland': 'large domestic coal reserves (Silesia) and coal-mining jobs; energy security concerns about Russian gas; EU climate policy and carbon prices driving new wind and solar',
        'India': 'large domestic coal reserves and rapidly rising demand; low cost of coal power; high solar resource and government targets (500 GW non-fossil capacity by 2030)',
        'Brazil': 'large rivers (Amazon, Paraná) and high rainfall for hydro (e.g. Itaipu); strong winds in the north-east; sugar-cane bagasse for biomass',
        'Kenya': 'location on the East African Rift gives geothermal resources (Olkaria); rivers for hydro; Lake Turkana wind farm; few domestic fossil fuels'}


@gen('energy_mix', d=(1, 4))
def g_mix(rng, slot):
    c, parts = pick(rng, MIX)
    tot = rng.choice([20, 60, 150, 450, 1800])
    gw = [(s, tot * p / 100) for s, p in parts]
    tab = '; '.join(f'{s} {v:,.1f} TWh' for s, v in gw)
    low = sum(v for s, v in gw if s not in ('coal', 'gas', 'fossil', 'oil and other fossil', 'gas and oil'))
    if slot.d <= 2:
        return dict(stem=f'Illustrative electricity generation in {c} (total {tot} TWh): {tab}. Calculate the percentage of electricity from low-carbon sources.',
                    answer=f'{low:,.1f} / {tot} × 100 = {low / tot * 100:.0f}%', markingKey='M1 sum low-carbon ÷ total × 100; A1 correct.', marks=mk(slot, 2))
    return dict(stem=f'Illustrative electricity generation in {c} (total {tot} TWh): {tab}. (a) Calculate the percentage share of each source and of low-carbon sources overall. (b) Suggest two factors that explain {c}\'s energy mix. (c) Evaluate one strategy {c} could use to improve its energy security.',
                answer='(a) ' + '; '.join(f'{s} {p}%' for s, p in parts) + f'; low-carbon {low / tot * 100:.0f}% (b) e.g. {MIXF[c]}. (c) e.g. diversify sources, expand storage and interconnectors, improve efficiency, develop domestic renewables; evaluate cost, intermittency and political acceptability.',
                markingKey='(a) A1 shares, A1 low-carbon total. (b) R1 R1 factors linked to country. (c) R1 strategy, R1 evaluation.', marks=mk(slot, 6))


CITY_W = [('Copenhagen', 1.1), ('Singapore', 1.4), ('Tokyo', 0.9), ('Lagos', 0.6), ('Dubai', 2.0), ('São Paulo', 1.1), ('Mumbai', 0.6),
          ('Toronto', 1.2), ('Nairobi', 0.6), ('Seoul', 1.0)]


@gen('waste', d=(1, 5))
def g_waste(rng, slot):
    city, kg = pick(rng, CITY_W)
    kg = round(kg * rng.uniform(0.9, 1.1), 2)
    pop = rng.choice([1.2, 2.5, 4.4, 5.9, 9.6, 14.0, 21.0])
    tot = kg * pop * 1e6 * 365 / 1000
    if slot.d <= 2:
        return dict(stem=f'Residents of {city} generate about {kg} kg of municipal solid waste per person per day. The population is {pop} million. Calculate the annual waste generated in tonnes.',
                    answer=f'{kg} × {pop} × 10⁶ × 365 / 1,000 = {tot:,.0f} t per year', markingKey='M1 per capita × population × 365; A1 correct (÷1,000 for tonnes).', marks=mk(slot, 2))
    rec = rng.choice([10, 20, 30, 45])
    cap = rng.choice([5, 10, 20, 40]) * 1e6
    left = tot * (1 - rec / 100)
    yrs = cap / left
    rec2 = rec + 20
    yrs2 = cap / (tot * (1 - rec2 / 100))
    return dict(stem=f'{city} ({pop} million people) generates {kg} kg of waste per person per day. {rec}% is recycled or composted and the rest goes to a landfill with {cap / 1e6:.0f} million t of remaining capacity. (a) Calculate the annual waste sent to landfill. (b) Calculate the remaining life of the landfill. (c) Calculate the new life if recycling rises to {rec2}%, and evaluate two other strategies to reduce landfill use.',
                answer=f'(a) {tot:,.0f} × {1 - rec / 100:.2f} = {left:,.0f} t per year (b) {cap:,.0f} / {left:,.0f} ≈ {yrs:.1f} years (c) ≈ {yrs2:.1f} years; e.g. waste-to-energy incineration (reduces volume by ~90% and generates electricity, as at Copenhill, Copenhagen, but emits CO₂ and toxic ash), composting food waste (reduces methane), pay-as-you-throw charges and bans on single-use plastics (reduce generation).',
                markingKey=f'(a) A1 {left:,.0f}. (b) A1 {yrs:.1f}. (c) A1 {yrs2:.1f}; R1 R1 evaluated strategies.', marks=mk(slot, 6))


DEMO = [('Niger', 46, 8, 6.7), ('Nigeria', 37, 12, 5.1), ('India', 16, 7, 2.0), ('Japan', 6, 13, 1.2), ('Germany', 9, 12, 1.4),
        ('Brazil', 12, 7, 1.6), ('Bangladesh', 18, 5, 1.9), ('Ethiopia', 32, 6, 4.0), ('South Korea', 5, 7, 0.72), ('Italy', 7, 12, 1.2),
        ('Kenya', 27, 5, 3.3), ('Indonesia', 16, 7, 2.1), ('Mexico', 15, 7, 1.8), ('Egypt', 22, 5, 2.9)]


@gen('demography', d=(1, 5))
def g_demo(rng, slot):
    c, b, d_, tfr = pick(rng, DEMO)
    cbr = round(b + rng.uniform(-1, 1), 1)
    cdr = round(d_ + rng.uniform(-0.8, 0.8), 1)
    nir = (cbr - cdr) / 10
    if slot.d <= 2:
        births = rng.randint(50, 900) * 1000
        pop = rng.choice([20, 45, 80, 120, 200])
        r_ = births / (pop * 1e6) * 1000
        return dict(stem=pick(rng, [f'{c} recorded about {births:,} live births in a year with a mid-year population of {pop} million. Calculate the crude birth rate (CBR).',
                                    f'A country with {pop} million people had {births:,} births in one year. Calculate its CBR per 1,000.']),
                    answer=f'{births:,} / ({pop} × 10⁶) × 1,000 = {r_:.1f} per 1,000', markingKey=f'M1 births ÷ population × 1,000; A1 {r_:.1f}.', marks=mk(slot, 2))
    if nir <= 0:
        return dict(stem=f'{c} has a CBR of {cbr} per 1,000 and a CDR of {cdr} per 1,000 (TFR about {tfr}). (a) Calculate the natural increase rate (NIR) as a percentage. (b) Identify the stage of the demographic transition model and explain two consequences of this population trend.',
                    answer=f'(a) ({cbr} − {cdr}) / 10 = {nir:.2f}% (natural decrease) (b) stage 5 (declining); consequences: ageing population and rising dependency ratio, labour shortages, pressure on pensions and healthcare; possible policies: pro-natalist incentives, immigration.',
                    markingKey=f'(a) A1 {nir:.2f}%. (b) A1 stage 5, R1 R1 consequences.', marks=mk(slot, 4))
    dt = 70 / nir
    st = 'stage 2' if cbr > 30 else 'stage 3' if cbr > 15 else 'stage 4'
    return dict(stem=f'{c} has a CBR of {cbr} per 1,000, a CDR of {cdr} per 1,000 and a total fertility rate (TFR) of about {tfr}. (a) Calculate the NIR as a percentage. (b) Calculate the doubling time. (c) Suggest the DTM stage and explain two factors influencing its TFR.',
                answer=f'(a) ({cbr} − {cdr}) / 10 = {nir:.2f}% (b) 70 / {nir:.2f} ≈ {dt:.0f} years (c) {st} (justify from CBR, CDR and TFR {tfr}; replacement level is 2.1); factors: education of women, access to contraception, child mortality, urbanisation, religion/culture, cost of children and government policy.',
                markingKey=f'(a) M1 (CBR − CDR)/10, A1 {nir:.2f}%. (b) A1 ≈ {dt:.0f} years. (c) A1 {st} with justification, R1 R1 factors.', marks=mk(slot, 6))


DEP = [('Niger', 49, 3), ('Uganda', 45, 2), ('Nigeria', 42, 3), ('India', 25, 7), ('Brazil', 20, 10), ('China', 17, 14),
       ('the USA', 18, 17), ('Germany', 14, 22), ('Italy', 12, 24), ('Japan', 12, 29), ('South Korea', 11, 19)]


@gen('dependency', d=(1, 4))
def g_dependency(rng, slot):
    c, y, o = pick(rng, DEP)
    w = 100 - y - o
    dr = (y + o) / w * 100
    if slot.d <= 2:
        return dict(stem=f'In {c} about {y}% of the population is aged 0-14 and {o}% is aged 65 and over. Calculate the dependency ratio.',
                    answer=f'({y} + {o}) / {w} × 100 = {dr:.0f} dependants per 100 people of working age',
                    markingKey=f'M1 (young + old) ÷ working-age (15-64) × 100; A1 {dr:.0f}.', marks=mk(slot, 2))
    yd, od = y / w * 100, o / w * 100
    shape = 'wide-based, triangular (expanding) pyramid' if y > 35 else 'narrow-based, top-heavy (contracting) pyramid' if o > y else 'more column-shaped (stationary) pyramid'
    return dict(stem=f'In {c} {y}% of the population is aged 0-14 and {o}% is aged 65+. (a) Calculate the total, youth and old-age dependency ratios. (b) Describe the likely shape of its age-sex pyramid. (c) Explain one environmental and one economic implication of this age structure.',
                answer=f'(a) total {dr:.0f}; youth {yd:.0f}; old-age {od:.0f} (per 100 aged 15-64) (b) {shape} (c) ' + ('a youthful population means future growth (population momentum), rising demand for food, water, land and energy, and the need for schools and jobs' if y > 35 else 'an ageing population means slower growth or decline, possibly lower resource demand, but higher healthcare and pension costs and labour shortages' if o > y else 'a large working-age share can give a demographic dividend (more workers, savings and growth), but rising consumption increases resource use and emissions; falling fertility means ageing and higher pension costs will follow'),
                markingKey=f'(a) A1 {dr:.0f}, A1 {yd:.0f} and {od:.0f}. (b) A1 shape. (c) R1 environmental, R1 economic implication.', marks=mk(slot, 6))


URB = [('Lagos', 5.6, 15.9, 30), ('Dhaka', 7.5, 23.2, 30), ('Delhi', 10.0, 32.9, 30), ('Kinshasa', 4.3, 16.3, 30), ('Shanghai', 8.9, 29.2, 30),
       ('Cairo', 10.2, 22.6, 30), ('Jakarta', 8.6, 11.2, 30), ('Nairobi', 1.6, 5.3, 30)]


@gen('urban_growth', d=(1, 4))
def g_urban(rng, slot):
    city, p0, p1, n = pick(rng, URB)
    a = 2023 - n
    pct = (p1 - p0) / p0 * 100
    r = ((p1 / p0) ** (1 / n) - 1) * 100
    if slot.d <= 2:
        return dict(stem=f'The urban agglomeration population of {city} grew from about {p0} million in {a} to about {p1} million in 2023 (UN estimates). Calculate the percentage increase.',
                    answer=f'({p1} − {p0}) / {p0} × 100 = {pct:.0f}%', markingKey=f'M1 change ÷ original × 100; A1 {pct:.0f}%.', marks=mk(slot, 2))
    p2 = p1 * (1 + r / 100) ** 10
    return dict(stem=f'The urban agglomeration population of {city} grew from about {p0} million in {a} to about {p1} million in 2023. (a) Calculate the mean annual growth rate. (b) Assuming this rate continues, project the population in 2033. (c) Explain two environmental problems that this growth creates for the urban system and one sustainable planning response.',
                answer=f'(a) ({p1}/{p0})^(1/{n}) − 1 ≈ {r:.1f}% per year (b) {p1} × (1 + {r / 100:.3f})^10 ≈ {p2:.1f} million (c) e.g. air pollution from traffic and industry, inadequate sewage and solid-waste collection, urban heat island, loss of wetlands and farmland to sprawl, water shortages; responses: bus rapid transit (Lagos BRT), compact growth, green infrastructure, upgraded sanitation.',
                markingKey=f'(a) M1 compound growth formula, A1 {r:.1f}%. (b) A1 ≈ {p2:.1f}. (c) R1 R1 problems, R1 response.', marks=mk(slot, 6))


PM = [('Delhi', 92), ('Lahore', 98), ('Dhaka', 80), ('Beijing', 34), ('Cairo', 41), ('Mexico City', 22), ('London', 10), ('Paris', 13),
      ('Lagos', 40), ('Jakarta', 43), ('Seoul', 22), ('Los Angeles', 12)]


@gen('pm25', d=(1, 4))
def g_pm25(rng, slot):
    city, v = pick(rng, PM)
    v = round(v * rng.uniform(0.95, 1.05), 1)
    who = 5
    x = v / who
    if slot.d <= 2:
        return dict(stem=f'The annual mean PM2.5 concentration in {city} was about {v} µg/m³. The WHO 2021 air-quality guideline is {who} µg/m³. Calculate how many times the guideline this represents.',
                    answer=f'{v} / {who} = {x:.1f} times the guideline', markingKey=f'M1 ÷ guideline; A1 {x:.1f}.', marks=mk(slot, 2))
    days = [round(v * rng.uniform(0.4, 2.2)) for _ in range(7)]
    over = sum(1 for d in days if d > 15)
    mean = sum(days) / 7
    return dict(stem=f'Daily mean PM2.5 (µg/m³) for one week in {city}: {", ".join(map(str, days))}. The WHO 24-hour guideline is 15 µg/m³ and the annual guideline is 5 µg/m³. (a) Calculate the weekly mean and the number of days exceeding the 24-hour guideline. (b) Explain why PM2.5 is particularly harmful to health. (c) Suggest two reasons why concentrations vary from day to day.',
                answer=f'(a) mean {mean:.1f} µg/m³; {over} of 7 days exceed 15 µg/m³ (b) particles under 2.5 µm penetrate deep into the lungs and bloodstream, causing respiratory and cardiovascular disease; air pollution causes millions of premature deaths a year (c) weather (temperature inversions trap pollutants, wind disperses them, rain washes out particles), traffic and industrial activity on weekdays, seasonal crop-residue burning (e.g. Punjab in October-November), dust storms.',
                markingKey=f'(a) A1 {mean:.1f}, A1 {over} days. (b) R1 small size penetrates lungs/blood, R1 named health effect. (c) R1 R1 reasons.', marks=mk(slot, 5))


EXT = [('a coal power station', ('MWh of electricity', 'MWh of electricity'), 'air pollution and CO₂ damage to health and climate', 1),
       ('a paper mill on a river', ('tonne of paper', 'tonnes of paper'), 'water pollution harming downstream fisheries', 10),
       ('a factory farm', ('pig raised for pork', 'pigs raised for pork'), 'ammonia, odour and nitrate pollution', 3),
       ('an airline', ('passenger flight', 'passenger flights'), 'CO₂ emissions and noise', 3),
       ('a cement works', ('tonne of cement', 'tonnes of cement'), 'CO₂ and dust emissions', 1)]


@gen('externality', d=(1, 5))
def g_ext(rng, slot):
    firm, (u1, un), harm, sc = pick(rng, EXT)
    pc = rng.randint(20, 80) * sc
    ec = rng.randint(5, 40) * sc
    q = rng.choice([1000, 5000, 20000, 100000])
    if slot.d <= 2:
        return dict(stem=f'The private cost to {firm} of producing one {u1} is ${pc}; the external cost of {harm} is ${ec} per {u1}. Calculate the social cost per unit and state the size of the Pigouvian tax that would internalise the externality.',
                    answer=f'social cost = private + external = {pc} + {ec} = ${pc + ec} per unit; Pigouvian tax = ${ec} per unit (equal to the marginal external cost)',
                    markingKey=f'M1 private + external; A1 ${pc + ec}; A1 tax = ${ec}.', marks=mk(slot, 3))
    rev = ec * q
    return dict(stem=f'{firm[0].upper() + firm[1:]} produces {q:,} {un} a year at a private cost of ${pc} per {u1}. Each {u1} causes ${ec} of external cost through {harm}. (a) Calculate the total external cost per year and the social cost per unit. (b) Explain why the market over-produces this good and how a Pigouvian tax would correct this. (c) Evaluate a tax compared with a regulation (emission limit) as a way of reducing the externality.',
                answer=f'(a) {ec} × {q:,} = ${rev:,} per year; social cost ${pc + ec} per unit (b) the price reflects only private cost, so marginal social cost exceeds private cost and output is above the socially optimal level (market failure); a tax of ${ec} per unit raises costs to reflect social cost, reducing output and pollution, and raises ${rev:,} if output were unchanged (polluter pays). (c) taxes give a continuous incentive to innovate and raise revenue, but the external cost is hard to value and may be regressive; regulation gives certainty of outcome but no incentive to go beyond the limit and needs enforcement.',
                markingKey=f'(a) A1 ${rev:,}, A1 ${pc + ec}. (b) R1 MSC > MPC → over-production, R1 tax internalises. (c) R1 tax strength/weakness, R1 regulation strength/weakness.', marks=mk(slot, 6))


ESV = [('a mangrove forest in Vietnam', 'coastal protection and fisheries'), ('a wetland upstream of a city in Uganda (Nakivubo)', 'water purification'),
       ('a coral reef in Belize', 'tourism, fisheries and shoreline protection'), ('a watershed forest supplying New York City (Catskills)', 'clean drinking water'),
       ('pollinator habitat around farms in California', 'crop pollination')]


@gen('esv', d=(2, 5))
def g_esv(rng, slot):
    eco, svc = pick(rng, ESV)
    v = rng.choice([500, 1200, 3000, 8000, 15000])
    area = rng.choice([100, 400, 1000, 2500])
    r = rng.choice([3, 5, 7])
    yrs = rng.choice([20, 30, 50])
    annual = v * area
    pv = annual * (1 - (1 + r / 100) ** -yrs) / (r / 100)
    conv = rng.choice([0.5, 1, 2, 4]) * pv / 1e6
    if slot.d <= 3:
        return dict(stem=f'The ecosystem services ({svc}) of {eco} are valued at ${v:,} per hectare per year. The area is {area:,} ha. Calculate the total annual value.',
                    answer=f'{v:,} × {area:,} = ${annual:,} per year', markingKey='M1 value × area; A1 correct.', marks=mk(slot, 2 if slot.d <= 2 else 3))
    return dict(stem=f'The ecosystem services ({svc}) of {eco} ({area:,} ha) are valued at ${v:,} per ha per year. A developer offers a project with a net present value of ${conv:.1f} million that would destroy the ecosystem. (a) Calculate the present value of the ecosystem services over {yrs} years at a {r}% discount rate, using PV = A × [1 − (1 + r)^−n] / r. (b) Compare this with the project. (c) Discuss the strengths and limitations of using monetary valuation in this decision.',
                answer=f'(a) annual value A = ${annual:,}; PV = {annual:,} × [1 − 1.{r:02d}^−{yrs}] / {r / 100} ≈ ${pv / 1e6:.1f} million (b) ' + ('the services are worth more than the project, so conservation is economically justified' if pv / 1e6 > conv else 'the project appears more valuable, but the valuation may omit non-market and future values') + ' (c) strengths: makes hidden values visible in cost-benefit analysis, supports payments for ecosystem services; limitations: values uncertain and sensitive to the discount rate (a high rate undervalues future generations), intrinsic and cultural values cannot be priced, irreversibility is ignored.',
                markingKey=f'(a) M1 annuity formula, A1 ≈ ${pv / 1e6:.1f} million. (b) R1 comparison. (c) R1 strength, R1 limitation (discount rate / intrinsic value).', marks=mk(slot, 6))


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: -v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


SPEAR = [('distance from a footpath (m)', 'plant species richness per quadrat', 'trampling'),
         ('distance downstream from a sewage outfall (km)', 'dissolved oxygen (mg/L)', 'organic pollution'),
         ('distance from a city centre (km)', 'lichen species per tree trunk', 'air pollution (SO₂)'),
         ('soil moisture (%)', 'percentage cover of rushes', 'drainage'),
         ('altitude (m)', 'mean tree height (m)', 'temperature and exposure'),
         ('distance from the sea along a dune transect (m)', 'soil organic matter (%)', 'succession')]


@gen('spearman', d=(2, 5))
def g_spearman(rng, slot):
    xl, yl, ctx = pick(rng, SPEAR)
    n = 8 if slot.d <= 3 else 10
    x = sorted(rng.sample(range(2, 60), n))
    sign = rng.choice([1, 1, -1])
    y = [max(1, round(20 + sign * 0.4 * xi + rng.uniform(-6, 6))) for xi in x]
    if len(set(y)) < n:
        return None
    rx, ry = ranks(x), ranks(y)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    rs = 1 - 6 * d2 / (n * (n * n - 1))
    crit = {8: 0.738, 10: 0.648}[n]
    sig = abs(rs) >= crit
    tab = '; '.join(f'({a}, {b})' for a, b in zip(x, y))
    return dict(stem=f'A student investigating {ctx} recorded {xl} and {yl} at {n} sites: {tab}. (a) Calculate Spearman\'s rank correlation coefficient, rs = 1 − 6Σd² / n(n² − 1). (b) The critical value at p = 0.05 for n = {n} is {crit}. State whether the correlation is significant and interpret it.' + (' (c) Explain why correlation does not prove causation in this investigation.' if slot.d >= 4 else ''),
                answer=f'(a) Σd² = {d2:g}; rs = 1 − 6 × {d2:g} / ({n} × {n * n - 1}) = {rs:.2f} (b) |rs| ' + ('≥' if sig else '<') + f' {crit}, so the ' + ('correlation is significant at p = 0.05 - reject the null hypothesis; there is a ' + ('positive' if rs > 0 else 'negative') + ' relationship' if sig else 'correlation is not significant - accept the null hypothesis of no correlation') + ('. (c) other variables (e.g. soil type, shade, sampling error) may covary; a causal mechanism must be supported by further evidence or controlled experiments.' if slot.d >= 4 else ''),
                markingKey=f'(a) M1 ranks and d², A1 Σd² = {d2:g}, A1 rs = {rs:.2f}. (b) R1 comparison with critical value and correct conclusion.' + (' (c) R1 confounding variables / no mechanism.' if slot.d >= 4 else ''), marks=mk(slot, 6 if slot.d >= 4 else 5))


CHI = [('presence of a lichen species on trees near and far from a main road', ['near road', 'far from road'], ['present', 'absent']),
       ('whether residents near and far from a landfill support a new incinerator', ['near', 'far'], ['support', 'oppose']),
       ('limpets on north- and south-facing rocks', ['north-facing', 'south-facing'], ['present', 'absent']),
       ('recycling behaviour of households with and without a doorstep collection', ['with collection', 'without collection'], ['recycle', 'do not recycle'])]


@gen('chi2', d=(3, 5))
def g_chi(rng, slot):
    what, rows, cols = pick(rng, CHI)
    a, b = rng.randint(10, 40), rng.randint(5, 35)
    c, d = rng.randint(5, 35), rng.randint(10, 40)
    n = a + b + c + d
    obs = [[a, b], [c, d]]
    rt = [a + b, c + d]
    ct = [a + c, b + d]
    exp = [[rt[i] * ct[j] / n for j in range(2)] for i in range(2)]
    chi = sum((obs[i][j] - exp[i][j]) ** 2 / exp[i][j] for i in range(2) for j in range(2))
    crit = 3.84
    sig = chi >= crit
    return dict(stem=f'An investigation of {what} recorded: {rows[0]} - {cols[0]} {a}, {cols[1]} {b}; {rows[1]} - {cols[0]} {c}, {cols[1]} {d}. (a) Calculate the expected frequencies. (b) Calculate the chi-squared statistic, χ² = Σ(O − E)²/E. (c) With 1 degree of freedom the critical value at p = 0.05 is 3.84. State and justify your conclusion.',
                answer=f'(a) expected: {exp[0][0]:.1f}, {exp[0][1]:.1f}, {exp[1][0]:.1f}, {exp[1][1]:.1f} (row total × column total ÷ {n}) (b) χ² = {chi:.2f} (c) ' + (f'{chi:.2f} ≥ 3.84, so reject the null hypothesis: there is a significant association between the variables (p < 0.05).' if sig else f'{chi:.2f} < 3.84, so accept the null hypothesis: no significant association at p = 0.05.'),
                markingKey=f'(a) M1 expected = row × column ÷ total, A1 values. (b) A1 χ² = {chi:.2f}. (c) R1 comparison with 3.84 and correct decision about the null hypothesis.', marks=mk(slot, 6))


SITES2 = [('nitrate (mg/L) upstream and downstream of a farm', 'mg/L', 3, 30), ('earthworms per m² in organic and conventional fields', 'per m²', 60, 300),
          ('leaf length (mm) of plantain in trampled and untrampled areas', 'mm', 40, 150), ('noise level (dB) on a main road and a side street', 'dB', 50, 80),
          ('species per quadrat in grazed and ungrazed grassland', 'species', 5, 25)]


def sd(v):
    m = sum(v) / len(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


@gen('mean_sd_t', d=(2, 5))
def g_meansd(rng, slot):
    what, u, lo, hi = pick(rng, SITES2)
    n = 6 if slot.d <= 3 else 8
    m1, m2 = rng.randint(lo, hi), rng.randint(lo, hi)
    gap = max(3, round(0.15 * m1))
    if abs(m1 - m2) < gap:
        m2 = m1 + rng.choice([-1, 1]) * gap
        if m2 > hi:
            m2 = m1 - gap
        if m2 <= 2:
            return None
    s = max(2, round(max(m1, m2) * rng.uniform(0.06, 0.2)))
    A = [max(1, round(m1 + rng.uniform(-s, s))) for _ in range(n)]
    B = [max(1, round(m2 + rng.uniform(-s, s))) for _ in range(n)]
    ma, mb = sum(A) / n, sum(B) / n
    sa, sb = sd(A), sd(B)
    if sa == 0 or sb == 0:
        return None
    if slot.d <= 3:
        return dict(stem=f'Data on {what}: Site A {", ".join(map(str, A))}; Site B {", ".join(map(str, B))}. Calculate the mean and the sample standard deviation for each site and comment on the reliability of the data.',
                    answer=f'A: mean {ma:.1f} {u}, SD {sa:.2f}; B: mean {mb:.1f} {u}, SD {sb:.2f}. ' + ('Small SDs relative to the means suggest consistent, reliable data; ' if max(sa / ma, sb / mb) < 0.2 else 'Large SDs relative to the means indicate high variability, so more samples are needed; ') + 'overlap of mean ± SD ranges suggests whether the difference may be significant.',
                    markingKey=f'A1 means {ma:.1f} and {mb:.1f}; A1 SDs {sa:.2f} and {sb:.2f}; R1 comment on spread / reliability.', marks=mk(slot, 4))
    t = abs(ma - mb) / math.sqrt(sa ** 2 / n + sb ** 2 / n)
    crit = {6: 2.23, 8: 2.14}[n]
    sig = t >= crit
    return dict(stem=f'Data on {what} (n = {n} at each site): Site A {", ".join(map(str, A))}; Site B {", ".join(map(str, B))}. (a) Calculate the mean and standard deviation for each site. (b) Calculate t = |x̄A − x̄B| / √(sA²/nA + sB²/nB). (c) The critical value of t at p = 0.05 with {2 * n - 2} degrees of freedom is {crit}. State your conclusion about the null hypothesis. (d) Suggest one way to improve the investigation.',
                answer=f'(a) A: {ma:.2f}, SD {sa:.2f}; B: {mb:.2f}, SD {sb:.2f} (b) t ≈ {t:.2f} (c) ' + (f'{t:.2f} ≥ {crit}: reject the null hypothesis - the difference is significant (p < 0.05)' if sig else f'{t:.2f} < {crit}: accept the null hypothesis - no significant difference') + ' (d) larger sample size, random sampling within each site, controlling time of day/season, repeating on several dates.',
                markingKey=f'(a) A1 means, A1 SDs. (b) M1 substitution, A1 t ≈ {t:.2f}. (c) R1 correct decision. (d) R1 valid improvement.', marks=mk(slot, 7))


# =============================================================================================
# ch01 5.1 Soil
# =============================================================================================
S('ch01-st1',
  terms=[('soil system', 'a dynamic system of storages (organic matter, organisms, nutrients, minerals, air, water) with inputs, outputs, transfers and transformations, linking the lithosphere, atmosphere, hydrosphere and biosphere'),
         ('soil horizon', 'a distinct layer within a soil profile, such as the O (organic), A (topsoil), B (subsoil) and C (weathered parent material) horizons'),
         ('soil profile', 'a vertical section through a soil showing its horizons from the surface to the parent rock'),
         ('humus', 'dark, partially decomposed organic matter in soil that holds water and nutrients'),
         ('leaching', 'the removal of soluble minerals and nutrients from the upper soil horizons by water percolating downwards'),
         ('weathering', 'the breakdown of rock in situ by physical, chemical and biological processes, producing the mineral fraction of soil')],
  facts=[('Which horizon is rich in decomposing organic matter (litter)?', 'The O horizon', ['The B horizon', 'The C horizon', 'Bedrock (R)'], 'O = organic; A = topsoil mixed with humus.'),
         ('Which process moves clay and iron from the A horizon to the B horizon?', 'Translocation (illuviation) by percolating water', ['Weathering of bedrock', 'Evaporation', 'Photosynthesis'], 'Material eluviated from A is deposited in B.'),
         ('How long can it take to form about 2.5 cm of topsoil?', 'Several hundred years or more', ['About one week', 'About one year', 'Ten million years'], 'Soil is effectively a non-renewable resource on human timescales.'),
         ('Which is an output from the soil system?', 'Leaching of nutrients into groundwater', ['Leaf litter', 'Precipitation', 'Weathering of parent rock'], 'Leaching, erosion, uptake and respiration remove matter.')],
  why=[('Explain how soil acts as a system.', 'It has inputs (organic matter, precipitation, weathered parent material, energy), storages (organic matter, nutrients, water, air, organisms), transfers (leaching, translocation) and transformations (decomposition, weathering, humification), and outputs (uptake by plants, erosion, leaching, gases).'),
       ('Explain why soils are described as a non-renewable resource.', 'Soil forms extremely slowly (about 1 cm per 100-400 years), whereas erosion from poorly managed land can remove centimetres in a few years; lost soil cannot be replaced on human timescales.'),
       ('Explain why tropical rainforest soils are often thin and infertile.', 'High rainfall leaches soluble nutrients; rapid decomposition and uptake mean nutrients are stored in biomass, not soil; deep weathering leaves iron- and aluminium-rich oxisols with little humus.')],
  contrast=[('the A horizon', 'the B horizon', 'The A horizon (topsoil) is dark, mixed with humus, biologically active and loses material by eluviation; the B horizon (subsoil) is lighter, lower in organic matter and gains clay, iron and aluminium washed down from above.'),
            ('physical weathering', 'chemical weathering', 'Physical weathering breaks rock into smaller pieces without changing its composition (freeze-thaw); chemical weathering changes the minerals (carbonation, hydrolysis, oxidation).')],
  misc=[('Soil is just crushed rock.', 'Soil is a mixture of mineral particles, organic matter (humus), water, air and living organisms, and has structure and horizons formed by soil processes.'),
        ('All soils have the same horizons.', 'Profiles vary with climate, parent material, organisms, relief and time (CLORPT): podzols have a bleached E horizon; chernozems a thick dark A horizon.')],
  apply=[('Describe the soil profile of a podzol under a boreal coniferous forest.', 'Acidic needle litter (O); thin dark A; grey, bleached E horizon from intense leaching of iron and humus; reddish-brown B horizon where iron and humus accumulate (iron pan); C horizon.', 4),
         ('List two inputs, two transformations and two outputs of the soil system.', 'Inputs: leaf litter, precipitation, parent rock weathering; transformations: decomposition, humification, nitrification, weathering; outputs: leaching, erosion, uptake by plants, CO₂ from respiration.', 3)],
  cases=[('chernozems of the Ukrainian steppe', 'deep, black soils up to 1 m thick formed under grassland, with high humus content (up to 10-15%)', 'how climate and vegetation shape soil profiles', 'grass roots die back each year adding organic matter, while moderate rainfall limits leaching, building one of the world\'s most fertile soils'),
         ('podzols under the Scandinavian taiga', 'acidic conifer litter and cold, wet conditions produce a bleached E horizon and an iron pan', 'leaching and translocation in soil systems', 'organic acids mobilise iron and aluminium, which are washed down and deposited in the B horizon')],
  evaluate=[('Soil should be managed as a non-renewable resource.', ['formation rate ~1 t/ha/yr vs erosion up to 10-100 t/ha/yr', 'a third of soils are moderately or highly degraded (FAO 2015)'], ['soil organic matter and structure can be rebuilt with good management', 'some soils form faster (volcanic, alluvial)'], 'On human timescales soil should be treated as effectively non-renewable, though its quality can be restored if not lost.'),
            ('Soils are the most undervalued ecosystem in environmental policy.', ['store about 1,500 GtC in the top metre - more than vegetation and atmosphere combined', '95% of food grown in soil'], ['soils feature in the EU Soil Monitoring Law and SDG 15', 'other ecosystems (oceans) are also undervalued'], 'Soils remain under-protected compared with air and water, although recognition is growing.')],
  extended=[('Explain how soil-forming processes produce distinct horizons in two contrasting soils. [7]', 'Podzol vs chernozem (or oxisol); weathering, humification, leaching, translocation, CLORPT; describe horizons and link to climate and vegetation.', 7, 'explain')],
  res=[('Soil pit description (deciduous woodland, Germany): O horizon 0-5 cm leaf litter; A horizon 5-25 cm dark brown, crumb structure, many earthworms; B horizon 25-70 cm lighter brown, clay-rich; C horizon 70 cm+ weathered sandstone.',
        [('Identify two pieces of evidence that this is a fertile soil.', 'Thick dark A horizon with humus; crumb structure; many earthworms mixing organic matter; leaf litter input.'),
         ('Explain the role of earthworms in this soil system.', 'They mix organic matter into the A horizon (bioturbation), create burrows improving aeration and drainage, and break down litter, speeding nutrient cycling.')])])

S('ch01-st2', gens=['soil_texture'],
  terms=[('soil texture', 'the relative proportions of sand, silt and clay particles in a soil'),
         ('soil structure', 'the way soil particles are aggregated into peds (crumbs, blocks, plates), which affects drainage and aeration'),
         ('soil fertility', 'the ability of a soil to supply nutrients, water and air to plants for growth'),
         ('cation exchange capacity (CEC)', 'the ability of soil particles (clay and humus) to hold and exchange positively charged nutrient ions such as Ca²⁺, K⁺ and Mg²⁺'),
         ('loam', 'a soil with a balanced mixture of sand, silt and clay, combining good drainage with good water and nutrient retention'),
         ('soil organic matter', 'material derived from living organisms - roots, litter, microbes and humus - that improves structure and fertility')],
  facts=[('Which soil particle size is smallest?', 'Clay (< 0.002 mm)', ['Sand (0.05-2 mm)', 'Silt (0.002-0.05 mm)', 'Gravel (> 2 mm)'], 'Clay\'s tiny size gives a large surface area for holding nutrients.'),
         ('Which soil type has the highest water-holding capacity but poorest drainage?', 'Clay', ['Sand', 'Loam', 'Gravel'], 'Small pores hold water by capillarity.'),
         ('Why does adding organic matter improve a sandy soil?', 'It increases water and nutrient retention', ['It increases drainage further', 'It reduces the number of soil organisms', 'It removes nutrients'], 'Humus has a high cation exchange capacity.'),
         ('Which soil texture is generally best for most crops?', 'Loam', ['Pure sand', 'Heavy clay', 'Peat with pH 3'], 'It balances drainage, aeration and retention.')],
  why=[('Explain why clay soils are often more fertile than sandy soils but harder to farm.', 'Clay particles have a large surface area and negative charge, holding water and nutrient cations (high CEC); but small pores give poor drainage and aeration, they become waterlogged in winter, crack when dry and are heavy to plough.'),
       ('Explain how soil structure affects plant growth.', 'Crumb structure creates pores for air and water, allows roots to penetrate and supports soil organisms; compaction or platy structure reduces infiltration, causes waterlogging and limits root growth.'),
       ('Explain why soil organic matter is important for fertility.', 'It supplies nutrients as it decomposes, increases CEC and water retention, binds particles into stable crumbs, feeds soil organisms and buffers pH.')],
  contrast=[('soil texture', 'soil structure', 'Texture is the proportion of sand, silt and clay (fixed for a given soil); structure is how particles are arranged into aggregates, which can be improved or damaged by management.'),
            ('sandy soils', 'clay soils', 'Sandy soils have large particles and pores, drain freely, warm quickly and are easily leached of nutrients; clay soils have tiny particles, hold water and nutrients well but drain poorly and compact easily.')],
  misc=[('The more clay a soil contains, the better it is for crops.', 'Very high clay content causes waterlogging, poor aeration and difficult cultivation; loams with moderate clay are best.'),
        ('Fertiliser alone can maintain soil fertility indefinitely.', 'Fertiliser supplies nutrients but does not maintain structure, organic matter or soil life; organic matter decline leads to erosion and lower yields.')],
  apply=[('Describe a simple method to determine the texture of a soil sample.', 'Sedimentation test: shake soil with water in a jar and let it settle; sand settles first, then silt, then clay; measure the thickness of each layer to estimate percentages (or use sieves for sand and the feel/ribbon test).', 3),
         ('Suggest how a farmer could improve a heavy clay soil.', 'Add organic matter (manure, compost), install field drains, add lime or gypsum to promote flocculation, avoid working the soil when wet to prevent compaction, use cover crops.', 3)],
  cases=[('terra preta soils of the Amazon', 'dark anthropogenic soils created by Indigenous people over centuries contain charcoal (biochar), pottery and organic waste and remain fertile today', 'how organic matter improves soil fertility', 'stable charcoal raises CEC and holds nutrients that would otherwise be leached from tropical soils'),
         ('the Dutch polders', 'reclaimed marine clay soils are very fertile but required extensive drainage and careful management to farm', 'texture and drainage as limits on fertility', 'clay soils hold nutrients well but must be drained to allow aeration and root growth')],
  evaluate=[('Soil texture is more important than soil management in determining agricultural productivity.', ['texture controls drainage and water-holding capacity', 'cannot easily be changed'], ['management (organic matter, drainage, irrigation) transforms productivity (terra preta, polders)', 'poor management degrades even the best soils'], 'Texture sets the baseline, but management largely determines whether productivity is achieved and sustained.')],
  extended=[('Explain how soil texture and structure influence water retention, aeration and fertility. [7]', 'Particle size and pore space; clay CEC; sand drainage and leaching; crumb structure; organic matter; compaction; examples.', 7, 'explain')],
  res=[('Infiltration test results (time for 500 mL of water to soak into a ring): sandy soil 45 s; loam 3 min 20 s; compacted clay at a field gateway 25 min.',
        [('Calculate how many times longer infiltration took at the compacted gateway than in the sandy soil.', '25 min = 1,500 s; 1,500 / 45 ≈ 33 times longer.'),
         ('Explain the differences in infiltration and one consequence of the slow rate at the gateway.', 'Sand has large pores so water infiltrates quickly; clay has tiny pores and compaction by machinery/livestock closes them; slow infiltration causes surface runoff, waterlogging and erosion.')])])

S('ch01-st3', gens=['soil_loss'],
  terms=[('soil degradation', 'the decline in soil quality through erosion, loss of organic matter, salinisation, compaction, acidification, contamination or nutrient depletion'),
         ('soil erosion', 'the removal of soil by wind or water faster than it can form'),
         ('salinisation', 'the accumulation of salts in soil, often caused by irrigation in hot climates where evaporation draws saline water to the surface'),
         ('desertification', 'land degradation in arid, semi-arid and dry sub-humid areas resulting from climatic variations and human activities'),
         ('contour ploughing', 'ploughing across a slope following the contours, so furrows trap water and soil and reduce erosion'),
         ('terracing', 'the construction of level steps on slopes to reduce runoff and soil erosion')],
  facts=[('According to the FAO, approximately what proportion of the world\'s soils are moderately to highly degraded?', 'About one-third', ['About 1%', 'About two-thirds', 'About 95%'], 'FAO Status of the World\'s Soil Resources (2015).'),
         ('The 1930s Dust Bowl in the US Great Plains was caused mainly by:', 'ploughing up prairie grassland followed by severe drought and wind erosion', ['volcanic eruptions', 'acid rain', 'flooding of the Mississippi'], 'Removal of deep-rooted grasses left soil exposed.'),
         ('Which practice is most likely to cause salinisation?', 'Irrigation with poor drainage in an arid climate', ['Planting windbreaks', 'Adding compost', 'No-till farming'], 'Evaporation leaves salts at the surface.'),
         ('Which soil conservation method protects soil from wind erosion on open plains?', 'Shelter belts (windbreaks)', ['Removing hedges', 'Bare fallowing', 'Burning crop residues'], 'Trees reduce wind speed at the surface.')],
  why=[('Explain how overgrazing can lead to desertification.', 'Livestock remove vegetation cover and trample soil, compacting it; bare soil is eroded by wind and water, organic matter falls, infiltration declines and rainfall runs off; vegetation cannot re-establish, so degradation spreads.'),
       ('Explain how no-till (conservation) agriculture reduces soil degradation.', 'Crops are sown directly into the residue of the previous crop; residues protect the surface from raindrop impact and wind, increase organic matter and soil biota, improve infiltration and reduce erosion and fuel use.'),
       ('Explain why soil degradation is a threat to food security.', 'Erosion removes the most fertile topsoil, organic matter and nutrient loss reduce yields, salinisation makes land unusable, and about 95% of food comes from soils; degradation affects about 3.2 billion people.')],
  contrast=[('wind erosion', 'water erosion', 'Wind erosion lifts and transports fine dry particles from bare, dry surfaces (Dust Bowl, Sahel); water erosion removes soil by raindrop splash, sheet wash, rills and gullies, especially on slopes.'),
            ('salinisation', 'acidification', 'Salinisation is the build-up of salts, usually from irrigation in hot climates; acidification is a fall in soil pH from acid rain, ammonium fertilisers or conifer litter.')],
  misc=[('Soil erosion only happens in low-income countries.', 'Erosion is serious in high-income countries too (e.g. about 1.7 billion t a year from US cropland; UK arable soils), although conservation measures are more widely used.'),
        ('Planting trees anywhere will stop desertification.', 'Inappropriate tree planting in drylands can deplete groundwater; farmer-managed natural regeneration and grazing management are often more effective.')],
  apply=[('Suggest three soil conservation strategies for a hillside farm in Nepal.', 'Terracing; contour ploughing and grass strips; agroforestry; mulching and cover crops; avoiding cultivation of the steepest slopes; check dams in gullies.', 3),
         ('Outline how farmer-managed natural regeneration (FMNR) has reversed land degradation in Niger.', 'Farmers protect and prune sprouting tree stumps rather than clearing them; about 5 million ha have been re-greened since the 1980s, reducing wind erosion, adding organic matter and increasing yields.', 3)],
  cases=[('the 1930s Dust Bowl, USA', 'about 40 million ha of the Great Plains lost topsoil when drought struck land ploughed from prairie; "Black Sunday" (14 April 1935) storms carried dust to the Atlantic', 'causes of soil degradation', 'removing deep-rooted grasses and bare fallowing left soil exposed to wind erosion during drought'),
         ('the Loess Plateau Watershed Rehabilitation Project, China', 'from 1994 terracing, grazing bans and tree planting on about 35,000 km² cut sediment flows to the Yellow River and doubled incomes for 2.5 million people', 'soil conservation at a regional scale', 'reducing slope cultivation and restoring vegetation increased infiltration and dramatically reduced erosion'),
         ('salinisation in the Murray-Darling Basin, Australia', 'clearing deep-rooted native vegetation and irrigation raised water tables, bringing salt to the surface and affecting millions of hectares', 'salinisation as a form of soil degradation', 'rising groundwater carried salts into the root zone, making land unproductive')],
  evaluate=[('Soil conservation is more cost-effective than restoring degraded land.', ['prevention costs less than restoration', 'topsoil lost is effectively irreplaceable'], ['restoration can succeed and pay back (Loess Plateau, FMNR)', 'farmers may lack incentives to invest in prevention without support'], 'Conservation is generally more cost-effective, but restoration is necessary and worthwhile where degradation has already occurred.'),
            ('Desertification is caused more by human activity than by climate.', ['overgrazing, over-cultivation, deforestation and poor irrigation', 'regreening shows human management can reverse it'], ['drought cycles in the Sahel', 'climate change increases aridity'], 'Climate sets the vulnerability, but human land use is usually the main driver and the main lever for reversing desertification.')],
  extended=[('Evaluate strategies used to conserve soils in a named region. [9]', 'Loess Plateau, Niger FMNR, US Soil Conservation Service after Dust Bowl, Ethiopian terracing; methods (terracing, contour ploughing, cover crops, no-till, windbreaks, grazing control); effectiveness, cost, community involvement; judgement.', 9, 'long')],
  res=[('Erosion plot data (t ha⁻¹ yr⁻¹) on a 10° slope in the Ethiopian Highlands: bare tilled soil 42; maize up-and-down slope 25; maize with contour bunds 9; maize with grass strips and mulch 4; natural grassland 1.',
        [('Calculate the percentage reduction in erosion achieved by grass strips and mulch compared with up-and-down cultivation.', '(25 − 4)/25 × 100 = 84%.'),
         ('Explain why the grassland plot has the lowest erosion.', 'Continuous plant cover intercepts rainfall, roots bind the soil, organic matter improves infiltration and reduces runoff.')])])


# =============================================================================================
# ch02 5.2 Agriculture and food
# =============================================================================================
S('ch02-st1', gens=['diet_energy'],
  terms=[('commercial agriculture', 'farming to produce crops or livestock for sale at market, often large-scale and intensive'),
         ('subsistence agriculture', 'farming to feed the farmer\'s own family or community, with little surplus for sale'),
         ('intensive agriculture', 'farming with high inputs of labour, capital, fertiliser or technology per unit area to obtain high yields'),
         ('extensive agriculture', 'farming with low inputs per unit area over large areas, giving lower yields per hectare'),
         ('monoculture', 'the growing of a single crop species over a large area'),
         ('agroforestry', 'a land-use system combining trees with crops and/or livestock on the same land')],
  facts=[('Which is an example of extensive commercial agriculture?', 'Cattle ranching in the Australian outback', ['Rice paddies in Bali tended by families', 'Greenhouse tomatoes in the Netherlands', 'Allotment gardening'], 'Low inputs per hectare over very large areas, for sale.'),
         ('The Netherlands is the world\'s second-largest agricultural exporter by value mainly because of:', 'highly intensive, technology-based farming such as greenhouses', ['very large farm area', 'subsistence farming', 'extensive ranching'], 'It exports over €100 billion a year from a small land area.'),
         ('Which feature is typical of shifting cultivation (slash-and-burn) in tropical forests?', 'Clearing a plot, farming it for a few years, then moving on to let it regenerate', ['Permanent irrigation', 'Heavy use of machinery', 'Large monoculture plantations'], 'It is sustainable at low population densities with long fallows.'),
         ('Approximately what share of the world\'s habitable land is used for agriculture?', 'About half', ['About 5%', 'About 20%', 'About 90%'], 'Of this, about 77% is used for livestock (grazing and feed).')],
  why=[('Explain why commercial farms often have higher yields than subsistence farms.', 'They use high-yielding varieties, synthetic fertiliser, irrigation, pesticides and machinery financed by capital and access to markets; subsistence farmers often lack money, credit, technology and secure land tenure.'),
       ('Explain why monocultures are vulnerable to pests and diseases.', 'Large areas of genetically similar plants provide abundant food for specialist pests, allow diseases to spread quickly and lack natural predators found in diverse systems (e.g. Panama disease in Cavendish bananas).'),
       ('Explain why livestock farming uses so much land.', 'Animals are at a higher trophic level, so about 90% of energy in feed is lost; grazing and feed crops require large areas; livestock provide about 18% of calories but use about 77% of agricultural land.')],
  contrast=[('commercial agriculture', 'subsistence agriculture', 'Commercial farms produce for sale, often at large scale with high capital inputs and specialisation; subsistence farms produce food for the household, are usually small and use family labour and low inputs.'),
            ('intensive agriculture', 'extensive agriculture', 'Intensive farming has high inputs and outputs per hectare on small areas (Dutch greenhouses, Asian rice paddies); extensive farming has low inputs and yields per hectare over large areas (ranching, nomadic pastoralism).')],
  misc=[('Subsistence farming is always unsustainable.', 'Many subsistence systems (rotational farming, agroforestry, terraced rice) have been sustainable for centuries when population pressure is low.'),
        ('Intensive farming always causes more environmental damage than extensive farming.', 'Intensive farming produces more per hectare, which may spare land for nature; extensive systems like ranching can drive large-scale deforestation.')],
  apply=[('Compare a named commercial farming system with a named subsistence system in terms of inputs, outputs and environmental impact.', 'e.g. soy in Mato Grosso (machinery, fertiliser, pesticides; high yields for export; deforestation and pesticide runoff) vs maize-bean farming in Malawi (family labour, little fertiliser; low yields for household; soil nutrient depletion).', 4),
         ('Identify the inputs, processes and outputs of a dairy farm as a system.', 'Inputs: grass, feed, fertiliser, water, energy, labour, capital; processes: grazing, milking, breeding; outputs: milk, meat, calves, manure, methane, nitrate runoff.', 3)],
  cases=[('soy farming in Mato Grosso, Brazil', 'Brazil is the world\'s largest soybean producer (about 150 million t), much grown in the Cerrado and southern Amazon for animal feed exports', 'commercial agriculture and its environmental impacts', 'large-scale, mechanised monoculture for export drives habitat conversion and pesticide and fertiliser use'),
         ('the Netherlands\' greenhouse horticulture', 'Westland greenhouses produce tomatoes at about 50 kg per m² with hydroponics, recycled water and LED lighting', 'intensive commercial agriculture', 'very high inputs of technology and energy per unit area give extremely high yields and water efficiency'),
         ('the rice terraces of Ifugao, Philippines', 'terraced paddies maintained for about 2,000 years by community irrigation and forest management (muyong) above the fields', 'sustainable subsistence agriculture', 'community management of water, soil and forest sustains yields with minimal external inputs')],
  evaluate=[('Intensive commercial agriculture is necessary to feed a growing world population.', ['high yields spare land for nature', 'Green Revolution averted famine'], ['causes pollution, soil degradation, biodiversity loss', 'enough food already produced - waste and distribution are key problems', 'smallholders produce about a third of world food'], 'Intensification is part of the answer but must be sustainable, and reducing waste and improving access are just as important.'),
            ('Subsistence farming is more sustainable than commercial farming.', ['low inputs, local consumption, diverse crops', 'traditional knowledge (Ifugao terraces)'], ['low yields may drive expansion into forest', 'soil nutrient mining where fallows shorten', 'commercial farms can adopt sustainable practices'], 'Sustainability depends on practices and population pressure rather than on whether a farm is subsistence or commercial.')],
  extended=[('Compare and contrast the sustainability of two named food production systems. [7]', 'Inputs, outputs, energy efficiency, environmental impacts, social and economic aspects; e.g. Dutch greenhouses vs Ifugao terraces, or Brazilian soy vs Malawian smallholder maize.', 7, 'explain')],
  res=[('Land use and calorie supply (Our World in Data, approximate): livestock (meat, dairy, and feed crops) use about 77% of agricultural land but supply about 18% of global calories and 37% of protein; crops for human consumption use 23% of land and supply 82% of calories.',
        [('Calculate the ratio of land share to calorie share for livestock and for crops.', 'Livestock 77/18 ≈ 4.3; crops 23/82 ≈ 0.28 - livestock use about 15 times more land per calorie.'),
         ('Explain these differences using ecological principles.', 'Livestock are at a higher trophic level, so energy is lost in respiration and heat (second law); more land is needed to grow feed or graze than to grow crops eaten directly.')])])

S('ch02-st2', gens=['yield_change'],
  terms=[('Green Revolution', 'the increase in agricultural production from the 1950s-1970s using high-yielding crop varieties, synthetic fertilisers, irrigation and pesticides'),
         ('agrochemicals', 'chemicals such as fertilisers, pesticides and herbicides used in farming'),
         ('energy subsidy', 'the extra energy (fossil fuels, fertiliser manufacture, machinery) put into a food production system beyond solar energy'),
         ('food miles', 'the distance food travels from where it is produced to where it is consumed'),
         ('integrated pest management (IPM)', 'a pest-control approach combining biological control, crop rotation, resistant varieties and targeted pesticide use to minimise chemical use'),
         ('genetically modified (GM) crop', 'a crop whose DNA has been altered using genetic engineering, e.g. Bt cotton or Golden Rice')],
  facts=[('Approximately what share of global greenhouse-gas emissions comes from food systems?', 'About a quarter to a third', ['About 1%', 'About 10%', 'About 75%'], 'Crippa et al. (2021) estimated 34% including supply chains.'),
         ('Who is regarded as the "father of the Green Revolution"?', 'Norman Borlaug', ['Rachel Carson', 'Thomas Malthus', 'Fritz Haber'], 'He developed semi-dwarf wheat in Mexico and won the 1970 Nobel Peace Prize.'),
         ('Which environmental problem is linked to groundwater irrigation in Punjab, India?', 'Water tables falling by about 0.5-1 m per year', ['Rising sea ice', 'Ozone depletion', 'Volcanic soil formation'], 'Free electricity for pumps encouraged over-extraction for rice and wheat.'),
         ('Which input in industrial agriculture requires the most fossil energy?', 'Synthetic nitrogen fertiliser', ['Seeds', 'Sunlight', 'Rainwater'], 'The Haber-Bosch process is energy-intensive.')],
  why=[('Explain why industrial agriculture is described as energy-inefficient despite high yields.', 'Large fossil-fuel subsidies go into fertiliser, machinery, irrigation, processing and transport; the energy output in food can be less than the energy input (e.g. greenhouse vegetables, feedlot beef).'),
       ('Explain how agriculture contributes to biodiversity loss.', 'Conversion of forests, grasslands and wetlands to farmland; monocultures remove habitat diversity; pesticides kill non-target insects and pollinators; fertilisers cause eutrophication; hedgerow removal fragments habitats.'),
       ('Explain why the Green Revolution had mixed social impacts.', 'It raised yields and reduced famine in Asia and Latin America, but favoured farmers with capital and irrigation; smaller farmers fell into debt buying inputs, and inequality and land concentration increased in some areas.')],
  contrast=[('organic farming', 'conventional (industrial) farming', 'Organic farming avoids synthetic fertilisers and pesticides, relying on rotations, manure and biological control, usually with lower yields; conventional farming uses synthetic inputs to maximise yields but has greater pollution and fossil-energy costs per hectare.'),
            ('biological pest control', 'chemical pest control', 'Biological control uses natural enemies (ladybirds, parasitic wasps) to reduce pests with few side effects; chemical control uses pesticides, which act quickly but can harm non-target species, persist and lead to resistance.')],
  misc=[('Organic food always has a lower environmental impact.', 'Organic farming often has lower pollution per hectare, but lower yields can mean more land and sometimes higher emissions per kg of food.'),
        ('Food miles are the main source of a food\'s carbon footprint.', 'Transport usually accounts for under 10% of food emissions; land-use change and on-farm emissions (methane, N₂O) dominate, so what you eat matters more than where it comes from.')],
  apply=[('Suggest three environmental impacts of large-scale palm-oil plantations.', 'Deforestation and loss of orangutan habitat; peatland drainage and fires releasing CO₂; pesticide and fertiliser runoff; soil erosion; loss of biodiversity in monoculture.', 3),
         ('Outline two benefits and two risks of growing Bt cotton in India.', 'Benefits: reduced bollworm damage, less insecticide spraying, higher yields; risks: pink bollworm evolved resistance, high seed costs and farmer debt, reduced crop genetic diversity.', 4)],
  cases=[('the Green Revolution in Punjab, India', 'wheat and rice yields roughly tripled from the 1960s, but water tables are falling by about 0.5-1 m a year and soils have lost organic matter', 'the sustainability of intensive agriculture', 'high-input farming raised food security but depleted groundwater and soils that future production depends on'),
         ('the honeybee and pollinator decline', 'neonicotinoid insecticides were restricted for outdoor use in the EU from 2018 after evidence of harm to bees', 'impacts of agrochemicals on ecosystems', 'systemic pesticides harmed pollinators that provide an ecosystem service worth hundreds of billions of dollars a year'),
         ('agriculture-driven deforestation in the Amazon', 'cattle ranching accounts for about 80% of deforestation in the Brazilian Amazon', 'land-use change from food production', 'converting forest to pasture releases carbon, reduces rainfall recycling and destroys habitat')],
  evaluate=[('The environmental costs of the Green Revolution outweigh its benefits.', ['groundwater depletion, soil degradation, pesticide poisoning', 'loss of crop diversity', 'eutrophication'], ['averted mass famine; yields doubled or tripled', 'spared land from conversion', 'lifted millions out of poverty'], 'The benefits were enormous, but the environmental costs now threaten future production, so a "greener" second revolution is needed.'),
            ('Genetically modified crops are essential for sustainable food production.', ['pest and drought resistance reduce inputs', 'biofortification (Golden Rice) addresses malnutrition'], ['resistance evolves', 'corporate control of seeds and costs for farmers', 'agroecology can achieve similar gains'], 'GM crops can contribute but are not essential; their benefits depend on regulation, access and integration with other practices.')],
  extended=[('Evaluate the environmental impacts of a named intensive food production system. [9]', 'e.g. Brazilian soy, Punjab wheat-rice, US corn belt, feedlot beef, Spanish greenhouses of Almería: inputs, outputs, pollution, water, soil, biodiversity, emissions; mitigation; judgement.', 9, 'long')],
  res=[('Greenhouse-gas emissions per kg of food (kg CO₂e, approximate global values based on Poore and Nemecek 2018): beef (beef herd) 60; lamb 24; cheese 21; pig meat 7; poultry 6; rice 4; tofu 3; wheat 1.4; peas 1.0.',
        [('Calculate how many times greater the emissions of beef are than tofu and than peas.', '60/3 = 20 times tofu; 60/1.0 = 60 times peas.'),
         ('Explain why ruminant meat has such high emissions.', 'Enteric fermentation in ruminants releases methane; large land areas (deforestation) and feed production; low feed conversion efficiency; manure releases N₂O and methane.')])])

S('ch02-st3',
  terms=[('sustainable agriculture', 'farming that meets current food needs while maintaining soil, water, biodiversity and livelihoods for future generations'),
         ('agroecology', 'the application of ecological principles to farming, using diversity, recycling and local knowledge rather than external inputs'),
         ('food waste', 'food fit for consumption that is discarded at retail or consumer level'),
         ('food loss', 'food lost between harvest and retail, e.g. through poor storage, pests or transport'),
         ('crop rotation', 'growing different crops in succession on the same land to maintain fertility and reduce pests'),
         ('regenerative agriculture', 'farming practices (no-till, cover crops, diverse rotations, managed grazing) aimed at rebuilding soil organic matter and biodiversity')],
  facts=[('Approximately what fraction of food produced globally is lost or wasted?', 'About one-third', ['About 1%', 'About 10%', 'About two-thirds'], 'FAO: about 1.3 billion t a year; UNEP 2024 estimates over 1 billion t wasted at retail/consumer level.'),
         ('In high-income countries, most food waste occurs at the:', 'household (consumer) stage', ['harvest stage', 'storage on farms', 'processing in mills'], 'In low-income countries more is lost after harvest.'),
         ('Which law made France the first country to ban supermarkets from destroying unsold food (2016)?', 'The Garot Law', ['The Brundtland Law', 'The Clean Air Act', 'The Paris Agreement'], 'Supermarkets must donate edible unsold food.'),
         ('Which practice adds nitrogen to soil without synthetic fertiliser?', 'Planting legumes in rotation', ['Burning crop residues', 'Bare fallowing', 'Deep ploughing'], 'Legumes host nitrogen-fixing Rhizobium.')],
  why=[('Explain why reducing food waste is an effective way to reduce environmental impacts.', 'Wasted food carries all the land, water, energy and emissions used to produce it; food waste accounts for about 8-10% of global greenhouse-gas emissions; landfilled food releases methane.'),
       ('Explain how agroforestry improves the sustainability of farming.', 'Trees fix nitrogen (some species), add organic matter, reduce erosion and wind, provide shade, fuel, fruit and fodder, store carbon and increase biodiversity, diversifying income and resilience.'),
       ('Explain why food loss is higher in low-income countries.', 'Lack of cold storage, poor roads and transport, pests in grain stores and limited processing mean crops spoil between harvest and market.')],
  contrast=[('food loss', 'food waste', 'Food loss occurs before retail - during harvest, storage, processing and transport (common in low-income countries); food waste occurs at retail and consumer level when edible food is discarded (common in high-income countries).'),
            ('regenerative agriculture', 'organic agriculture', 'Organic agriculture is a certified system defined by bans on synthetic inputs; regenerative agriculture is defined by outcomes, using practices that rebuild soil health and may still use some synthetic inputs.')],
  misc=[('Reducing food waste is only the responsibility of consumers.', 'Producers, retailers (cosmetic standards, promotions), governments and the hospitality sector all contribute; policies like France\'s Garot Law target retailers.'),
        ('Sustainable agriculture always means lower yields.', 'Practices such as push-pull pest control, agroforestry and improved rotations can maintain or increase yields while reducing inputs.')],
  apply=[('Suggest four ways a city could reduce food waste.', 'Separate food-waste collection for composting/anaerobic digestion; food redistribution apps and food banks; education campaigns ("Love Food Hate Waste"); clearer date labels; pay-as-you-throw waste charges (South Korea).', 4),
         ('Describe the "push-pull" system used by farmers in East Africa.', 'Desmodium planted between maize rows repels ("pushes") stemborer moths and suppresses Striga weed while fixing nitrogen; Napier grass around the field attracts ("pulls") the moths away; yields can double without pesticides.', 3)],
  cases=[('South Korea\'s food-waste recycling system', 'since 2013 households pay by weight for food waste using RFID bins; over 90% of food waste is now recycled into compost, feed or biogas', 'strategies to reduce food waste', 'pricing waste by weight gives a direct incentive to reduce it, and separate collection allows recycling'),
         ('the push-pull system in Kenya', 'developed by ICIPE, it is used by over 250,000 farmers and can increase maize yields by 2-3 times', 'agroecology as sustainable agriculture', 'ecological interactions replace pesticides and fertiliser, raising yields while reducing costs'),
         ('the zaï pits of Burkina Faso', 'farmers dig small pits filled with manure to capture rain on degraded, crusted soils, restoring thousands of hectares', 'low-cost sustainable soil and water management', 'concentrating water and nutrients allows crops to grow and termites to improve soil structure')],
  evaluate=[('Reducing food waste is more important than increasing food production for achieving food security.', ['a third of food is lost or wasted', 'waste reduction lowers environmental impact', 'enough food is produced for everyone'], ['population growth to about 10 billion requires more food', 'waste reduction is hard to achieve and does not reach the hungry directly', 'yields are low in sub-Saharan Africa'], 'Reducing waste is a high priority and very cost-effective, but must be combined with sustainable yield growth and better access.'),
            ('Agroecology can feed the world.', ['push-pull and agroforestry raise smallholder yields', 'lower costs and pollution', 'more resilient to climate change'], ['yields often lower than intensive systems', 'labour-intensive', 'knowledge and markets needed'], 'Agroecology can make a major contribution, especially for smallholders, but a mix of approaches is likely to be needed.')],
  extended=[('Evaluate strategies to increase the sustainability of terrestrial food production. [9]', 'Crop rotation, IPM, agroforestry, no-till/regenerative, precision agriculture, reducing waste, dietary change, GM crops; examples (push-pull, Netherlands, zaï pits, South Korea); judgement.', 9, 'long')],
  res=[('UNEP Food Waste Index (2024): about 1.05 billion t of food wasted in 2022 - households 60%, food service 28%, retail 12%; average household waste about 79 kg per person per year.',
        [('Calculate the mass of food wasted by households globally.', '60% × 1.05 billion t ≈ 0.63 billion t (630 million t).'),
         ('Suggest two reasons why households waste so much food.', 'Over-buying (promotions), confusion over "best before" vs "use by" dates, poor storage, large portions, low food prices relative to income.')])])

S('ch02-st4',
  terms=[('food security', 'when all people at all times have physical and economic access to sufficient, safe and nutritious food to meet their dietary needs for an active and healthy life'),
         ('food insecurity', 'a lack of reliable access to sufficient, affordable, nutritious food'),
         ('undernutrition', 'a condition resulting from insufficient intake of energy or nutrients, causing stunting, wasting or underweight'),
         ('overnutrition', 'excess intake of energy, leading to overweight and obesity'),
         ('planetary health diet', 'the EAT-Lancet Commission (2019) reference diet that is healthy and within planetary boundaries - mainly plant-based with small amounts of meat and dairy')],
  facts=[('According to the FAO (2024), about how many people were undernourished in 2023?', 'About 733 million', ['About 50 million', 'About 2 billion', 'About 4 billion'], 'About 1 in 11 people worldwide.'),
         ('The planetary health diet recommends limiting red meat to about:', '14 g per day (about 100 g per week)', ['200 g per day', '1 kg per day', 'no limit'], 'EAT-Lancet 2019.'),
         ('Which of these is one of the four pillars of food security?', 'Access', ['Advertising', 'Altitude', 'Automation'], 'Availability, access, utilisation and stability.'),
         ('A shift to which diet would reduce food-related land use the most?', 'Plant-based (vegan) diet', ['High-beef diet', 'Diet with more dairy', 'More air-freighted vegetables'], 'Poore and Nemecek estimated a 75% reduction in farmland use.')],
  why=[('Explain why food insecurity exists even though enough food is produced globally.', 'Poverty limits access; conflict, poor infrastructure and price shocks disrupt supply; food is used for animal feed and biofuels; waste and loss; unequal distribution between and within countries.'),
       ('Explain how dietary choices affect the environment.', 'Animal products use more land, water and energy and emit more greenhouse gases per calorie because of trophic inefficiency and methane from ruminants; plant-based diets have much lower footprints.'),
       ('Explain how climate change threatens food security.', 'Droughts, heatwaves and floods reduce yields; shifting rainfall; pests and diseases spread; sea-level rise salinises deltas; price spikes harm the poor.')],
  contrast=[('food availability', 'food access', 'Availability is whether enough food is physically present (production, imports, stocks); access is whether people can obtain it, depending on income, prices and markets.'),
            ('undernutrition', 'malnutrition', 'Undernutrition is a deficiency of energy or nutrients; malnutrition includes both undernutrition and overnutrition (obesity) and micronutrient deficiencies.')],
  misc=[('Food insecurity is caused mainly by global food shortages.', 'Global production exceeds needs; food insecurity is driven mostly by poverty, conflict, inequality and access.'),
        ('A vegetarian diet always has a smaller footprint than any diet with meat.', 'Diets high in cheese, air-freighted produce or greenhouse vegetables can have large footprints; small amounts of low-impact meat may be lower than some vegetarian diets.')],
  apply=[('Suggest how the environmental value system of a person might influence their food choices.', 'Ecocentric: vegan/vegetarian, local organic, minimal packaging; anthropocentric: follows health guidelines and labels, supports regulation; technocentric: accepts lab-grown meat, GM crops and vertical farming.', 3),
         ('Outline two causes of the 2007-2008 global food price crisis.', 'High oil prices raised fertiliser and transport costs; biofuel demand diverted grain (US maize); droughts in Australia; export bans; speculation.', 2)],
  cases=[('the 2007-2008 global food price crisis', 'world food prices rose about 80% between 2006 and 2008, causing riots in over 30 countries', 'factors affecting food security', 'high fuel costs, biofuel demand, drought and export restrictions combined to make food unaffordable for the poorest'),
         ('the EAT-Lancet planetary health diet (2019)', 'it proposes roughly doubling the consumption of fruit, vegetables, nuts and legumes and cutting red meat and sugar by about half globally', 'linking diet to planetary boundaries', 'a shift towards plant-based diets could feed about 10 billion people within environmental limits'),
         ('famine in the Horn of Africa (2011)', 'drought combined with conflict in Somalia led to famine that killed about 260,000 people', 'the role of conflict and climate in food insecurity', 'drought reduced harvests, but conflict blocked aid and markets, turning a crisis into famine')],
  evaluate=[('Changing diets in high-income countries is the most effective way to improve global food security.', ['frees land and grain used for feed', 'reduces emissions that threaten yields'], ['food insecurity is mainly about poverty and conflict', 'cultural resistance to change', 'benefits may not reach the poorest'], 'Dietary change would reduce environmental pressure, but improving access, incomes and stability in food-insecure regions is more directly effective.')],
  extended=[('Discuss how different environmental value systems influence food choices and food policy. [9]', 'Ecocentric (veganism, local organic, agroecology), anthropocentric (taxes on sugar/meat, labelling, subsidies), technocentric (GM, lab-grown meat, vertical farms); cultural and religious factors; examples; judgement.', 9, 'long')],
  res=[('Daily intake (g per person per day): planetary health diet - red meat 14, poultry 29, dairy 250, legumes 75, nuts 50, vegetables 300; typical diet in a high-income country - red meat 120, poultry 60, dairy 350, legumes 15, nuts 10, vegetables 220.',
        [('Calculate the percentage reduction in red meat needed for the high-income diet to meet the planetary health diet.', '(120 − 14)/120 × 100 ≈ 88%.'),
         ('Suggest two policies that could encourage this dietary shift.', 'Taxes or removal of subsidies on red meat; subsidies for vegetables and legumes; public procurement (school meals) with plant-based options; labelling and education.')])])


# =============================================================================================
# ch03 6.1 Introduction to the atmosphere; 6.4 Stratospheric ozone
# =============================================================================================
S('ch03-st1',
  terms=[('atmosphere', 'the layer of gases surrounding Earth, held by gravity, consisting mainly of nitrogen (78%) and oxygen (21%) with argon, CO₂, water vapour and trace gases'),
         ('troposphere', 'the lowest layer of the atmosphere (up to about 10-16 km) where weather occurs and temperature decreases with height'),
         ('stratosphere', 'the layer above the troposphere (about 12-50 km) containing the ozone layer, where temperature increases with height'),
         ('albedo', 'the proportion of incoming solar radiation reflected by a surface'),
         ('lapse rate', 'the rate at which air temperature decreases with increasing altitude, on average about 6.5 °C per km in the troposphere')],
  facts=[('Which gas makes up about 78% of the dry atmosphere?', 'Nitrogen', ['Oxygen', 'Argon', 'Carbon dioxide'], 'Oxygen is about 21%, argon about 0.9%, CO₂ about 0.04%.'),
         ('Why does temperature increase with height in the stratosphere?', 'Ozone absorbs ultraviolet radiation', ['It is closer to the Sun', 'Clouds trap heat', 'Water vapour condenses'], 'Absorption of UV warms the layer.'),
         ('What proportion of the atmosphere\'s mass lies in the troposphere?', 'About 75-80%', ['About 10%', 'About 50%', 'About 99.9%'], 'Air density decreases rapidly with height.'),
         ('Which process produced most of the oxygen in Earth\'s atmosphere?', 'Photosynthesis by cyanobacteria and later plants', ['Volcanic eruptions', 'Lightning', 'Decomposition'], 'The Great Oxidation Event began about 2.4 billion years ago.')],
  why=[('Explain why the atmosphere is described as a dynamic system.', 'It has inputs (volcanic gases, emissions, photosynthetic oxygen), outputs (gases dissolved in oceans, absorbed by plants or rocks), storages and transformations (photochemical reactions), and continuously exchanges energy and matter with the hydrosphere, biosphere and lithosphere.'),
       ('Explain how human activities have changed the composition of the atmosphere.', 'Burning fossil fuels and deforestation raised CO₂ from about 280 to over 420 ppm; agriculture and fossil fuels raised methane (about 1,900 ppb, over 2.5 times pre-industrial) and N₂O; CFCs were added; aerosols and pollutants from industry and traffic.'),
       ('Explain why most weather occurs in the troposphere.', 'It contains almost all the water vapour and about 80% of the atmosphere\'s mass; it is heated from below by the ground, so temperature falls with height, causing convection, cloud formation and precipitation.')],
  contrast=[('the troposphere', 'the stratosphere', 'The troposphere is the lowest layer where temperature falls with height, convection and weather occur; the stratosphere lies above it, is stable, contains the ozone layer and warms with height because ozone absorbs UV.')],
  misc=[('The ozone layer and the greenhouse effect are the same thing.', 'The ozone layer is in the stratosphere and absorbs UV radiation; the greenhouse effect is the trapping of infrared radiation, mainly by gases in the troposphere.'),
        ('The atmosphere has always had its present composition.', 'Early atmosphere lacked free oxygen; it was transformed by photosynthesis over billions of years, and humans are now changing it again.')],
  apply=[('Outline two ways in which the biosphere has influenced the composition of the atmosphere.', 'Photosynthesis added oxygen and removes CO₂; respiration and decomposition release CO₂; wetlands and termites release methane; nitrogen-fixing and denitrifying bacteria cycle nitrogen.', 2),
         ('Suggest why air at the summit of Mount Everest contains only about a third of the oxygen per breath compared with sea level.', 'Air pressure and density decrease with height, so each breath contains fewer molecules, although the percentage of oxygen (21%) is unchanged.', 2)],
  cases=[('the Great Oxidation Event', 'about 2.4 billion years ago cyanobacteria released enough oxygen to accumulate in the atmosphere, forming banded iron formations', 'the biosphere changing atmospheric composition', 'photosynthetic organisms transformed the atmosphere, allowing aerobic life and the ozone layer to develop'),
         ('the 1991 eruption of Mount Pinatubo, Philippines', 'about 15-20 million t of SO₂ entered the stratosphere and global temperatures fell by about 0.5 °C for 1-2 years', 'interaction between the lithosphere and atmosphere', 'sulfate aerosols reflected sunlight, showing how natural inputs alter atmospheric energy balance')],
  evaluate=[('Human activities are now the main driver of changes in atmospheric composition.', ['CO₂ up 50% since 1750; methane up over 150%', 'CFCs and many pollutants are entirely human-made'], ['volcanic eruptions still cause short-term changes', 'natural cycles dominate total fluxes'], 'Humans now dominate long-term changes in greenhouse gases and pollutants, though natural processes still control the bulk composition and short-term variability.')],
  extended=[('Explain how the atmosphere interacts with other Earth systems. [7]', 'Exchange of gases with the biosphere (photosynthesis/respiration), hydrosphere (evaporation, CO₂ dissolution), lithosphere (volcanism, weathering); energy flows; human changes.', 7, 'explain')],
  res=[('Atmospheric composition (dry air): nitrogen 78.08%; oxygen 20.95%; argon 0.93%; carbon dioxide 0.042%; methane 0.00019%.',
        [('Convert the CO₂ and methane percentages into parts per million and parts per billion.', 'CO₂: 0.042% = 420 ppm; methane: 0.00019% = 1.9 ppm = 1,900 ppb.'),
         ('Explain why gases present in tiny amounts can still have a large effect on climate.', 'CO₂ and methane absorb infrared radiation, while nitrogen and oxygen do not; small concentrations of greenhouse gases strongly affect the energy balance.')])])

S('ch03-st2', gens=['forcing'],
  terms=[('greenhouse effect', 'the natural process by which greenhouse gases absorb and re-radiate long-wave (infrared) radiation emitted by Earth\'s surface, warming the lower atmosphere'),
         ('greenhouse gas', 'a gas that absorbs and emits infrared radiation, such as water vapour, carbon dioxide, methane, nitrous oxide and ozone'),
         ('short-wave radiation', 'incoming solar radiation, mainly visible and ultraviolet, that passes largely through the atmosphere'),
         ('long-wave radiation', 'infrared radiation emitted by Earth\'s surface and atmosphere'),
         ('radiative forcing', 'the change in the balance of incoming and outgoing energy at the top of the atmosphere, measured in W m⁻²')],
  facts=[('Without the natural greenhouse effect, Earth\'s mean surface temperature would be about:', '−18 °C', ['+15 °C', '+30 °C', '−100 °C'], 'The greenhouse effect raises it by about 33 °C to about +15 °C.'),
         ('Which is the most abundant greenhouse gas in the atmosphere?', 'Water vapour', ['Carbon dioxide', 'Methane', 'Nitrous oxide'], 'Its concentration is controlled by temperature, so it acts as a feedback.'),
         ('Approximately what percentage of incoming solar radiation is reflected back to space by Earth (planetary albedo)?', 'About 30%', ['About 5%', 'About 60%', 'About 90%'], 'Clouds, aerosols, ice and surfaces reflect it.'),
         ('Why do greenhouse gases absorb infrared but not most visible light?', 'Their molecules vibrate at frequencies matching infrared wavelengths', ['They are coloured', 'They are heavier than nitrogen', 'They reflect sunlight'], 'Asymmetric molecular vibrations absorb IR.')],
  why=[('Explain how the natural greenhouse effect maintains a habitable planet.', 'Short-wave solar radiation passes through the atmosphere and warms the surface; the surface emits long-wave radiation, which greenhouse gases absorb and re-emit in all directions, including back down, keeping the average temperature about 33 °C warmer than without it.'),
       ('Explain why the atmosphere is in dynamic equilibrium in terms of energy.', 'Over the long term, incoming solar energy is balanced by outgoing reflected and emitted radiation; changes in albedo, greenhouse gases or solar output shift the balance until a new equilibrium temperature is reached.'),
       ('Explain why water vapour is regarded as a feedback rather than a driver of climate change.', 'Its concentration depends on temperature and it stays in the atmosphere only about 9 days; warming caused by CO₂ increases evaporation, adding water vapour that amplifies warming (positive feedback).')],
  contrast=[('the natural greenhouse effect', 'the enhanced greenhouse effect', 'The natural greenhouse effect keeps Earth about 33 °C warmer than it would otherwise be; the enhanced greenhouse effect is the extra warming caused by human increases in greenhouse gases.'),
            ('short-wave radiation', 'long-wave radiation', 'Short-wave radiation comes from the hot Sun (visible and UV) and passes through the atmosphere; long-wave radiation is infrared emitted by the cooler Earth, which greenhouse gases absorb.')],
  misc=[('The greenhouse effect is entirely caused by human pollution.', 'The greenhouse effect is natural and essential for life; humans have enhanced it.'),
        ('Greenhouse gases trap heat by reflecting sunlight back to Earth.', 'They absorb and re-emit infrared radiation from the surface; they do not reflect incoming sunlight.')],
  apply=[('Describe the flows of energy in Earth\'s global energy budget.', 'Incoming solar ~340 W m⁻²; ~30% reflected; ~70% absorbed by surface and atmosphere; surface emits long-wave radiation, most absorbed by greenhouse gases and re-emitted; outgoing long-wave radiation balances absorbed solar; latent and sensible heat transfers.', 4),
         ('Suggest why deserts become very cold at night.', 'Dry air contains little water vapour (a greenhouse gas) and skies are clear, so long-wave radiation escapes to space rapidly.', 2)],
  cases=[('Venus and Mars as comparisons', 'Venus has a dense CO₂ atmosphere and surface temperatures of about 465 °C; Mars has a thin atmosphere and a mean of about −60 °C', 'the role of the greenhouse effect', 'the amount of greenhouse gas strongly controls planetary surface temperature'),
         ('the Mount Pinatubo cooling (1991-93)', 'stratospheric aerosols reduced incoming solar radiation and global temperatures fell by about 0.5 °C', 'changes to the atmospheric energy balance', 'increasing reflection of short-wave radiation temporarily shifted the dynamic equilibrium to a cooler state')],
  evaluate=[('The greenhouse effect is better described as a "blanket" than a "greenhouse".', ['gases absorb and re-emit IR, like a blanket reducing heat loss', 'real greenhouses work mainly by stopping convection'], ['the term is widely understood', 'both analogies oversimplify'], 'Neither analogy is perfect, but the blanket model better represents the radiative process.')],
  extended=[('Explain how the natural greenhouse effect and atmospheric dynamic equilibrium regulate Earth\'s temperature. [7]', 'Short- and long-wave radiation, absorption by greenhouse gases, energy budget, albedo, feedbacks (water vapour, ice), equilibrium and forcing.', 7, 'explain')],
  res=[('Earth\'s energy budget (approximate, W m⁻²): incoming solar 340; reflected by clouds and atmosphere 77; reflected by surface 23; absorbed by atmosphere 78; absorbed by surface 162.',
        [('Calculate the planetary albedo.', '(77 + 23)/340 = 100/340 ≈ 0.29 (29%).'),
         ('Show that the absorbed and reflected flows balance the incoming radiation.', '77 + 23 + 78 + 162 = 340 W m⁻², so energy is conserved.')])])

S('ch03-st3', gens=['ozone'],
  terms=[('ozone layer', 'a region of the stratosphere (about 15-35 km) with a high concentration of ozone (O₃) that absorbs most incoming ultraviolet-B and all UV-C radiation'),
         ('ozone-depleting substances (ODS)', 'chemicals such as CFCs, halons, carbon tetrachloride and methyl bromide that release chlorine or bromine in the stratosphere and destroy ozone'),
         ('chlorofluorocarbons (CFCs)', 'stable, non-toxic compounds of chlorine, fluorine and carbon formerly used as refrigerants, aerosol propellants and foam-blowing agents'),
         ('Dobson unit (DU)', 'the unit of total column ozone; 300 DU is typical, and below 220 DU defines the ozone "hole"'),
         ('polar stratospheric clouds', 'clouds that form in the extremely cold Antarctic winter stratosphere, on which reactions release active chlorine')],
  facts=[('How does UV radiation form ozone in the stratosphere?', 'UV splits O₂ into oxygen atoms, which combine with O₂ to form O₃', ['Lightning combines nitrogen and oxygen', 'Plants release ozone', 'Volcanoes emit ozone'], 'Ozone is continually formed and destroyed - a dynamic equilibrium.'),
         ('Approximately how many ozone molecules can one chlorine atom destroy?', 'About 100,000', ['One', 'About 10', 'About 100 million'], 'Chlorine acts as a catalyst and is regenerated.'),
         ('Why does the ozone hole form over Antarctica in spring (September-October)?', 'Sunlight returns after winter and drives reactions on polar stratospheric clouds that release chlorine', ['Antarctica has the most factories', 'The Sun is closest in October', 'Ozone moves north'], 'The polar vortex isolates the cold air mass.'),
         ('Who first reported the Antarctic ozone hole in 1985?', 'Farman, Gardiner and Shanklin of the British Antarctic Survey', ['Molina and Rowland', 'James Hansen', 'Charles Keeling'], 'Molina and Rowland had predicted CFC damage in 1974.')],
  why=[('Explain how CFCs destroy stratospheric ozone.', 'CFCs are stable and drift into the stratosphere, where UV breaks them down releasing chlorine atoms; Cl + O₃ → ClO + O₂, then ClO + O → Cl + O₂, so chlorine is regenerated and acts as a catalyst destroying many ozone molecules.'),
       ('Explain why ozone depletion is harmful to living organisms.', 'More UV-B reaches the surface, increasing skin cancers and cataracts, suppressing immune systems, damaging DNA, reducing phytoplankton productivity (base of marine food webs) and crop yields.'),
       ('Explain why the ozone layer is described as being in dynamic equilibrium.', 'Ozone is continuously formed (UV splitting O₂) and destroyed (UV splitting O₃) at balanced rates; ODS increase the destruction rate, shifting the equilibrium to lower ozone concentration.')],
  contrast=[('stratospheric ozone', 'tropospheric ozone', 'Stratospheric ozone is beneficial, absorbing UV radiation; tropospheric (ground-level) ozone is a secondary pollutant in photochemical smog that harms lungs and plants.')],
  misc=[('The ozone hole causes global warming.', 'Ozone depletion and climate change are different problems: the hole lets in more UV; global warming is caused by greenhouse gases (though CFCs are also potent greenhouse gases).'),
        ('Ozone depletion only affects Antarctica.', 'Thinning occurs globally, with significant Arctic depletion in cold years (e.g. 2020), and increased UV affects populated southern regions such as Australia and Chile.')],
  apply=[('Outline the main uses of ozone-depleting substances before the Montreal Protocol.', 'Refrigerants and air conditioning (CFC-12), aerosol propellants, foam-blowing agents and solvents (CFC-11, CFC-113), fire extinguishers (halons), soil fumigants (methyl bromide).', 3),
         ('Suggest why Australia has one of the highest rates of skin cancer in the world.', 'High UV due to latitude and sunny climate, seasonal ozone thinning over the Southern Hemisphere, outdoor lifestyle and a largely fair-skinned population.', 2)],
  cases=[('the Antarctic ozone hole', 'it reached a maximum of about 29.9 million km² in September 2000 and was first reported by the British Antarctic Survey in 1985 from Halley Station data', 'stratospheric ozone destruction by ODS', 'cold polar stratospheric clouds and returning spring sunlight activate chlorine from CFCs, rapidly destroying ozone'),
         ('the 2020 Arctic ozone hole', 'an unusually strong and cold polar vortex led to record Arctic ozone loss in March 2020', 'the influence of temperature on ozone depletion', 'very cold conditions allowed polar stratospheric clouds to form, activating chlorine as in Antarctica')],
  evaluate=[('Ozone depletion is a solved environmental problem.', ['ODS production down over 99%', 'ozone layer recovering, on track for 2066 in Antarctica'], ['long-lived ODS persist for decades', 'illegal CFC-11 emissions detected (eastern China, 2010s)', 'HFC substitutes are potent greenhouse gases', 'climate change affects recovery'], 'Ozone depletion is on the way to being solved, but it requires continued vigilance and enforcement.')],
  extended=[('Explain the formation and destruction of stratospheric ozone, including the role of human activities. [7]', 'O₂ + UV → 2O; O + O₂ → O₃; O₃ + UV → O₂ + O; dynamic equilibrium; CFC breakdown, Cl catalytic cycle; polar stratospheric clouds; consequences of increased UV.', 7, 'explain')],
  res=[('Antarctic ozone hole: maximum area (million km², approximate) - 1985: 18.0; 1995: 24.0; 2000: 29.9; 2006: 29.6; 2015: 28.2; 2019: 16.4 (unusually warm); 2023: 26.0.',
        [('Calculate the percentage increase in maximum area between 1985 and 2000.', '(29.9 − 18.0)/18.0 × 100 ≈ 66%.'),
         ('Suggest why the area varies from year to year even though ODS levels are declining.', 'Stratospheric temperatures and the strength of the polar vortex vary, and colder years have more polar stratospheric clouds; volcanic aerosols (e.g. Hunga Tonga 2022) and smoke can also enhance depletion.')])])

S('ch03-st4',
  terms=[('Montreal Protocol', 'the 1987 international treaty to phase out the production and consumption of ozone-depleting substances, ratified by all UN member states'),
         ('Vienna Convention', 'the 1985 framework convention for the protection of the ozone layer, under which the Montreal Protocol was agreed'),
         ('Kigali Amendment', 'the 2016 amendment to the Montreal Protocol to phase down hydrofluorocarbons (HFCs), which are potent greenhouse gases'),
         ('HCFCs', 'hydrochlorofluorocarbons, transitional replacements for CFCs with lower ozone-depleting potential, now also being phased out'),
         ('Multilateral Fund', 'the fund established in 1990 under the Montreal Protocol to help developing countries phase out ODS')],
  facts=[('The Montreal Protocol was the first UN treaty to achieve:', 'universal ratification by all 197 parties', ['a ban on fossil fuels', 'a global carbon tax', 'the end of all air pollution'], 'Universal ratification was reached in 2009.'),
         ('By how much has global consumption of controlled ODS fallen since the Montreal Protocol?', 'By over 99%', ['By about 10%', 'By about half', 'Not at all'], 'UNEP Ozone Secretariat.'),
         ('The Kigali Amendment (2016) is expected to avoid up to about how much global warming by 2100?', '0.3-0.5 °C', ['3-5 °C', '0.01 °C', 'None'], 'By phasing down HFCs.'),
         ('Why were developing countries given a longer time to phase out CFCs?', 'Common but differentiated responsibilities - they had contributed least and needed time and funding', ['They used no CFCs', 'CFCs are harmless in the tropics', 'They refused to sign'], 'The Multilateral Fund paid for the transition.')],
  why=[('Explain why the Montreal Protocol is considered the most successful international environmental agreement.', 'Clear scientific consensus, a small number of producers, affordable substitutes, binding phase-out schedules, trade restrictions on non-parties, funding for developing countries and regular amendments based on science; ODS fell over 99% and the ozone layer is recovering.'),
       ('Explain why it was easier to tackle ozone depletion than climate change.', 'ODS were produced by a few companies in a few countries and had substitutes; climate change involves fossil fuels central to all economies, billions of emitters and much higher costs of transition.'),
       ('Explain why the replacement of CFCs with HFCs created a new problem.', 'HFCs do not deplete ozone but are powerful greenhouse gases (GWP hundreds to thousands of times CO₂), so their growing use in air conditioning would add to global warming - hence the Kigali Amendment.')],
  contrast=[('CFCs', 'HFCs', 'CFCs contain chlorine and destroy stratospheric ozone as well as being greenhouse gases; HFCs contain no chlorine so do not deplete ozone, but are potent greenhouse gases now being phased down.'),
            ('the Montreal Protocol', 'the Kyoto Protocol', 'The Montreal Protocol (1987) phased out ozone-depleting substances with universal participation and great success; the Kyoto Protocol (1997) set emissions targets only for developed countries, lacked US ratification and had limited success.')],
  misc=[('Since the Montreal Protocol the ozone hole has disappeared.', 'The hole still forms every Antarctic spring; full recovery to 1980 levels is expected around 2066 because ODS persist for decades.'),
        ('The Montreal Protocol only benefits the ozone layer.', 'Because CFCs are potent greenhouse gases, the Protocol has also avoided more warming than the Kyoto Protocol - an estimated 0.5-1 °C by mid-century.')],
  apply=[('Outline three features that contributed to the success of the Montreal Protocol.', 'Strong science and the visible ozone hole; substitutes available (HCFCs, HFCs, hydrocarbons); binding phase-out schedules; Multilateral Fund for developing countries; trade bans with non-parties; adjustable amendments.', 3),
         ('Suggest how lessons from the Montreal Protocol could be applied to climate change.', 'Sector-by-sector agreements (e.g. HFCs via Kigali, methane), funding for developing countries, trade measures (carbon border adjustments), regular science-led review and tightening.', 3)],
  cases=[('the Montreal Protocol (1987)', 'ODS consumption fell by over 99%; the ozone layer is projected to recover by about 2040 at mid-latitudes and 2066 over Antarctica', 'international management of ozone depletion', 'binding phase-outs, substitutes and financial support allowed a global problem to be addressed effectively'),
         ('the illegal CFC-11 emissions in eastern China', 'atmospheric monitoring detected unexpected CFC-11 emissions around 2013-2017, traced to foam manufacture; after enforcement emissions fell sharply by 2019', 'monitoring and enforcement of environmental agreements', 'independent atmospheric measurements revealed non-compliance and allowed rapid correction')],
  evaluate=[('The Montreal Protocol provides a model that can be applied to tackle climate change.', ['shows global cooperation can work', 'funding and differentiated responsibilities', 'Kigali Amendment already tackles HFCs'], ['fossil fuels are far more economically central than CFCs', 'many more sources and actors', 'substitutes are costlier'], 'Its principles can guide climate policy, but the scale and economic importance of fossil fuels make climate change much harder to solve.')],
  extended=[('Evaluate the effectiveness of the Montreal Protocol in managing ozone depletion. [9]', 'Achievements (99% ODS reduction, recovery projections, climate co-benefits, Kigali), reasons for success, limitations (persistence, illegal production, HFCs, time lags, nitrous oxide not controlled); judgement.', 9, 'long')],
  res=[('Equivalent effective stratospheric chlorine (EESC, ppt, Antarctic, approximate): 1980: 2,000 (benchmark); 2000: 3,800 (peak); 2020: 3,350; projected 2066: back to 2,000.',
        [('Calculate the percentage decline in EESC from the 2000 peak to 2020.', '(3,800 − 3,350)/3,800 × 100 ≈ 11.8%.'),
         ('Explain why recovery is so slow despite the near-complete ban on ODS.', 'CFCs have atmospheric lifetimes of 50-100 years, so chlorine already emitted remains in the stratosphere for decades.')])])


# =============================================================================================
# ch04 6.2 Climate change: causes and impacts
# =============================================================================================
S('ch04-st1', gens=['co2e', 'co2_rate'],
  terms=[('enhanced greenhouse effect', 'the increase in the natural greenhouse effect caused by human emissions of greenhouse gases, leading to global warming'),
         ('anthropogenic emissions', 'greenhouse-gas emissions caused by human activities such as burning fossil fuels, deforestation, agriculture and industry'),
         ('global warming potential (GWP)', 'a measure of how much heat a greenhouse gas traps over a period (usually 100 years) relative to the same mass of CO₂'),
         ('CO₂-equivalent (CO₂e)', 'the amount of CO₂ that would have the same warming effect as a given mass of another greenhouse gas, calculated as mass × GWP'),
         ('climate change', 'long-term changes in temperature and weather patterns; current climate change is mainly caused by human greenhouse-gas emissions')],
  facts=[('Which sector produces the largest share of global greenhouse-gas emissions?', 'Energy (electricity, heat and transport)', ['Waste', 'Aviation alone', 'Cement only'], 'Energy accounts for about three-quarters of emissions.'),
         ('Approximately how much has global surface temperature risen since 1850-1900 (IPCC AR6, 2011-2020)?', 'About 1.1 °C', ['About 0.1 °C', 'About 3 °C', 'About 5 °C'], 'It reached about 1.45 °C above pre-industrial in 2023 and exceeded 1.5 °C in 2024.'),
         ('Which country has the largest cumulative (historical) CO₂ emissions since 1750?', 'The United States', ['China', 'India', 'Brazil'], 'The USA has emitted about a quarter of cumulative CO₂; China now has the largest annual emissions.'),
         ('Which greenhouse gas is released mainly by livestock, rice paddies, landfill and fossil-fuel leaks?', 'Methane', ['Nitrous oxide', 'CFC-12', 'Sulfur hexafluoride'], 'Methane concentration is over 2.5 times pre-industrial.')],
  why=[('Explain how burning fossil fuels enhances the greenhouse effect.', 'Combustion transfers carbon stored for millions of years into the atmosphere as CO₂; higher concentrations absorb more outgoing long-wave radiation, reducing heat loss to space and raising the equilibrium temperature.'),
       ('Explain why methane is an important target for climate policy despite its lower concentration than CO₂.', 'Per molecule it traps much more heat (GWP₁₀₀ ≈ 28, GWP₂₀ ≈ 80), and its short lifetime (~12 years) means cuts quickly reduce warming; it is responsible for about 30% of warming since pre-industrial times.'),
       ('Explain why per-capita emissions are important when comparing countries.', 'Total emissions reflect population size; per-capita figures show the lifestyle and energy intensity of residents and are central to debates about fairness (e.g. USA ~15 t vs India ~2 t CO₂ per person).')],
  contrast=[('the natural greenhouse effect', 'the enhanced greenhouse effect', 'The natural greenhouse effect is caused by naturally occurring gases and keeps Earth habitable; the enhanced effect results from human additions of greenhouse gases and causes additional warming.'),
            ('total national emissions', 'per-capita emissions', 'Total emissions measure a country\'s overall contribution (China is largest); per-capita emissions divide by population, showing that people in some smaller countries (Qatar, Australia, USA) emit much more each.')],
  misc=[('Global warming is caused by the hole in the ozone layer.', 'Global warming is caused by greenhouse gases trapping infrared radiation; the ozone hole lets in more UV but has little effect on global temperature.'),
        ('CO₂ cannot be causing warming because it makes up only 0.04% of the atmosphere.', 'Nitrogen and oxygen do not absorb infrared; small amounts of CO₂ strongly absorb it, and a 50% increase since 1750 has a measurable effect.')],
  apply=[('Identify three human sources of greenhouse gases and the gas each releases.', 'Burning coal, oil and gas (CO₂); deforestation (CO₂); cattle and rice paddies (methane); landfill (methane); synthetic fertilisers (N₂O); refrigerants (HFCs).', 3),
         ('Suggest why emissions from aviation are hard to reduce.', 'Jet fuel has high energy density; batteries are too heavy for long flights; sustainable aviation fuels are expensive and limited; demand is rising; international aviation is not covered by national targets.', 2)],
  cases=[('China\'s emissions', 'China emitted about 12 Gt CO₂ in 2023 (about 30% of the global total) but about 8-9 t per person and is the world\'s largest installer of solar and wind', 'national contributions to anthropogenic emissions', 'rapid industrialisation powered by coal made China the largest emitter, while its per-capita and historical emissions are lower than those of the USA'),
         ('the Mauna Loa (Keeling) curve', 'continuous measurements since 1958 show CO₂ rising from about 315 ppm to over 420 ppm', 'evidence for rising greenhouse-gas concentrations', 'the long, accurate record links rising CO₂ to fossil-fuel emissions and shows the seasonal cycle of photosynthesis')],
  evaluate=[('Countries with the highest historical emissions should bear the greatest responsibility for reducing them.', ['the USA and Europe emitted most cumulative CO₂', 'they have greater wealth and capability', 'principle of common but differentiated responsibilities'], ['current emissions are dominated by China and other emerging economies', 'past emitters did not know the consequences', 'all countries must reach net zero'], 'Historical emitters should lead and fund mitigation, but all major current emitters must also reduce emissions rapidly.'),
            ('Agriculture should be given the same priority as energy in cutting greenhouse-gas emissions.', ['food systems cause about a third of emissions', 'methane and N₂O cuts give fast results'], ['energy produces about three-quarters of emissions', 'food security concerns', 'agricultural emissions are harder to measure'], 'Energy must remain the top priority, but agriculture requires much more attention than it currently receives.')],
  extended=[('Explain how human activities have enhanced the greenhouse effect. [7]', 'Sources (fossil fuels, deforestation, agriculture, industry, F-gases), changes in concentrations (CO₂ 280→420+ ppm, CH₄, N₂O), radiative forcing, GWP, per-capita vs total; evidence.', 7, 'explain')],
  res=[('Greenhouse-gas emissions by sector (global, approximate, % of total CO₂e): energy use in industry 24; transport 16; energy use in buildings 17; agriculture, forestry and land use 18; fugitive energy emissions 6; industrial processes 5; waste 3; other energy 11.',
        [('Calculate the total percentage of emissions from energy (industry, transport, buildings, fugitive and other energy).', '24 + 16 + 17 + 6 + 11 = 74%.'),
         ('Suggest two strategies to reduce emissions from buildings.', 'Insulation and efficient heating (heat pumps); renewable electricity; efficient appliances and lighting; building codes for net-zero buildings.')])])

S('ch04-st2', gens=['co2_rate'],
  terms=[('ice core', 'a cylinder of ice drilled from an ice sheet or glacier; trapped air bubbles and isotopes provide records of past atmospheric composition and temperature'),
         ('proxy data', 'indirect evidence of past climate from natural records such as ice cores, tree rings, corals, pollen and sediments'),
         ('IPCC', 'the Intergovernmental Panel on Climate Change, established in 1988 by UNEP and the WMO to assess the science of climate change'),
         ('temperature anomaly', 'the difference between the observed temperature and a long-term average baseline'),
         ('instrumental record', 'direct measurements of temperature and other variables using instruments, available globally from about 1850')],
  facts=[('The EPICA Dome C ice core from Antarctica provides a record of climate going back about:', '800,000 years', ['8,000 years', '80,000 years', '8 million years'], 'It shows CO₂ ranged about 180-300 ppm in glacial-interglacial cycles.'),
         ('The IPCC Sixth Assessment Report (2021) concluded that human influence on warming is:', '"unequivocal"', ['"unlikely"', '"about as likely as not"', '"impossible to determine"'], 'Earlier reports used "very likely" (2007) and "extremely likely" (2013).'),
         ('Which isotope ratio in ice cores is used as a proxy for past temperature?', 'Oxygen-18 to oxygen-16 (δ¹⁸O) or deuterium', ['Carbon-14 to nitrogen-14', 'Uranium-238 to lead-206', 'Hydrogen to helium'], 'Colder periods produce snow depleted in heavy isotopes.'),
         ('Which year was the warmest on record globally (as of 2025)?', '2024', ['1998', '2005', '2016'], 'It was the first calendar year above 1.5 °C (about 1.55 °C, WMO).')],
  why=[('Explain how ice cores provide evidence for past climate change.', 'Snow accumulates in annual layers; air bubbles trapped in the ice preserve samples of past atmosphere (CO₂, methane); isotope ratios indicate past temperatures; dust and ash show volcanic events; the record shows CO₂ and temperature rising and falling together.'),
       ('Explain why the IPCC is regarded as an authoritative source of evidence.', 'It assesses thousands of peer-reviewed studies; reports are written by hundreds of scientists from many countries and reviewed by experts and governments; it communicates confidence and likelihood levels.'),
       ('Explain why multiple lines of evidence are needed to establish that climate is changing.', 'Each record has limitations (urban heat island in thermometers, gaps, proxy uncertainty); agreement between independent records - temperatures, sea level, ice loss, ocean heat content, species shifts - makes the conclusion robust.')],
  contrast=[('proxy data', 'instrumental data', 'Proxy data (ice cores, tree rings, corals) indirectly record past climate over thousands of years but with greater uncertainty; instrumental data are direct measurements (thermometers, satellites) available only for about the last 170 years.'),
            ('weather', 'climate', 'Weather is the short-term state of the atmosphere; climate is the long-term average (typically 30 years), so a cold winter does not disprove warming.')],
  misc=[('Climate has changed naturally before, so current change must be natural.', 'Past changes had natural causes (orbital cycles, volcanoes), but the current rate is far faster, and natural drivers cannot explain it; only human greenhouse gases fit the evidence.'),
        ('A very cold winter disproves global warming.', 'Weather varies; climate trends are measured over decades, and the long-term global average continues to rise.')],
  apply=[('Outline three lines of evidence that the climate is warming.', 'Rising global surface temperatures (~1.1-1.3 °C); sea-level rise (~20 cm since 1900, accelerating); shrinking Arctic sea ice and glaciers; ocean heat content increasing; earlier springs and shifting species ranges.', 3),
         ('Suggest one limitation of tree-ring data as evidence of past climate.', 'Ring width depends on several factors (rainfall, temperature, CO₂, pests), and the record is limited to regions with seasonal growth and to the age of trees.', 2)],
  cases=[('the EPICA Dome C and Vostok ice cores', 'cores from Antarctica show eight glacial cycles over 800,000 years with CO₂ between about 180 and 300 ppm, compared with over 420 ppm today', 'evidence for the link between CO₂ and temperature', 'temperature and CO₂ rose and fell together, and current CO₂ is far outside the natural range'),
         ('the IPCC Sixth Assessment Report (2021-2023)', 'it concluded that human influence has unequivocally warmed the atmosphere, ocean and land and that warming of 1.5 °C is likely to be reached in the early 2030s', 'the role of IPCC assessments', 'synthesising evidence from thousands of studies provides an authoritative basis for policy such as the Paris Agreement')],
  evaluate=[('Ice-core data provide the most convincing evidence of human-caused climate change.', ['long records show CO₂ outside the natural range', 'direct samples of past air'], ['correlation does not show cause; temperature sometimes led CO₂ in the past', 'instrumental records and attribution studies give direct evidence of current change'], 'Ice cores provide crucial context, but the most convincing evidence comes from combining them with instrumental records and physical understanding.')],
  extended=[('Evaluate the evidence for anthropogenic climate change. [9]', 'Instrumental temperatures, ice cores, Keeling curve, sea-level rise, ice loss, ocean heat, isotopic fingerprint (more ¹²C from fossil fuels), IPCC attribution; uncertainties and sceptics\' arguments; judgement.', 9, 'long')],
  res=[('Global temperature anomaly relative to 1850-1900 (°C, approximate): 1900: 0.0; 1950: 0.2; 1980: 0.4; 2000: 0.7; 2010: 0.9; 2016: 1.3; 2020: 1.3; 2023: 1.45; 2024: 1.55.',
        [('Calculate the mean rate of warming per decade between 1980 and 2020.', '(1.3 − 0.4)/4 decades ≈ 0.23 °C per decade.'),
         ('Suggest why the anomaly does not rise smoothly every year.', 'Natural variability - El Niño (warm years such as 2016, 2023-24) and La Niña, volcanic eruptions, solar cycles - is superimposed on the long-term trend.')])])

S('ch04-st3', gens=['forcing'],
  terms=[('climate feedback', 'a process that amplifies (positive) or dampens (negative) an initial change in climate'),
         ('climate tipping point', 'a critical threshold beyond which a part of the climate system changes abruptly and often irreversibly, e.g. collapse of the West Antarctic Ice Sheet'),
         ('permafrost', 'ground that remains frozen for at least two consecutive years, storing large amounts of carbon'),
         ('ice-albedo feedback', 'the positive feedback in which melting ice exposes darker surfaces that absorb more solar radiation, causing more warming and melting'),
         ('climate sensitivity', 'the eventual global warming from a doubling of atmospheric CO₂, estimated at about 3 °C (likely 2.5-4 °C, IPCC AR6)')],
  facts=[('Which is a negative climate feedback?', 'Increased plant growth from higher CO₂ removing more CO₂', ['Thawing permafrost releasing methane', 'Melting sea ice lowering albedo', 'Forest dieback releasing carbon'], 'CO₂ fertilisation partly offsets increases, but its effect is limited.'),
         ('Approximately how much carbon is stored in northern permafrost soils?', 'About 1,400-1,600 GtC', ['About 1 GtC', 'About 50 GtC', 'About 100,000 GtC'], 'Roughly twice the carbon currently in the atmosphere.'),
         ('Which tipping element could raise sea level by several metres over centuries if it collapsed?', 'The West Antarctic Ice Sheet', ['The Sahara Desert', 'The Gulf Stream only', 'Alpine glaciers'], 'It holds enough ice for about 3-5 m of sea-level rise.'),
         ('What is the IPCC AR6 best estimate of equilibrium climate sensitivity?', 'About 3 °C', ['About 0.5 °C', 'About 6 °C', 'About 10 °C'], 'Likely range 2.5-4 °C.')],
  why=[('Explain how thawing permafrost acts as a positive feedback.', 'Warming thaws frozen soils; microbes decompose previously frozen organic matter, releasing CO₂ and methane; these enhance the greenhouse effect, causing more warming and more thaw.'),
       ('Explain why tipping points make climate change difficult to manage.', 'Once a threshold is crossed, change may become self-sustaining and irreversible on human timescales; thresholds are uncertain; tipping elements may interact (cascade), and impacts could be abrupt.'),
       ('Explain how clouds can act as both positive and negative feedbacks.', 'More low, thick clouds reflect sunlight (cooling - negative); more high, thin cirrus trap long-wave radiation (warming - positive); the overall effect is likely slightly positive but is the largest source of uncertainty.')],
  contrast=[('a positive climate feedback', 'a negative climate feedback', 'A positive feedback amplifies warming (ice-albedo, permafrost, water vapour); a negative feedback dampens it (CO₂ fertilisation, increased outgoing radiation from a warmer Earth, some cloud effects).')],
  misc=[('Negative feedbacks mean climate change will stop by itself.', 'The main negative feedback (more radiation emitted by a warmer planet) limits warming only at a higher temperature; other negative feedbacks are weaker than positive ones.'),
        ('Tipping points are certain to occur at exactly 1.5 °C.', 'Thresholds are uncertain; some (coral reefs, Greenland) may be at risk around 1.5 °C, others at 2-4 °C or more (Armstrong McKay et al., 2022).')],
  apply=[('Draw (describe) a positive feedback loop linking Arctic warming, sea ice and albedo.', 'Arctic warms → sea ice melts → dark ocean exposed (albedo falls from ~0.6 to ~0.06) → more solar radiation absorbed → ocean and air warm further → more ice melts.', 3),
         ('Suggest why Amazon dieback is considered a potential climate tipping point.', 'Deforestation and drought reduce rainfall recycling; forest stress causes tree death and fires releasing carbon; beyond about 20-25% deforestation or 3-4 °C warming parts could shift to savanna, releasing large amounts of CO₂.', 3)],
  cases=[('permafrost thaw in Siberia', 'thaw is creating thermokarst lakes and craters on the Yamal Peninsula and releasing methane', 'positive feedback in the climate system', 'carbon locked in frozen soils for millennia is being decomposed and released, amplifying warming'),
         ('the Greenland Ice Sheet', 'it lost an average of about 270 Gt of ice per year between 2002 and 2023, contributing about 0.7 mm per year to sea-level rise', 'a climate tipping element', 'as the surface lowers it becomes warmer (height-melt feedback), and beyond a threshold loss may become self-sustaining')],
  evaluate=[('Positive feedbacks make catastrophic climate change inevitable.', ['ice-albedo, permafrost and forest dieback amplify warming', 'tipping points may cascade'], ['feedbacks scale with warming, so limiting emissions limits them', 'negative feedbacks exist', 'some tipping points are centuries away'], 'Feedbacks make rapid emissions cuts urgent, but catastrophic outcomes are not inevitable if warming is limited.')],
  extended=[('Discuss the importance of feedback loops and tipping points in the climate system. [9]', 'Positive feedbacks (water vapour, ice-albedo, permafrost, forest dieback), negative feedbacks (Planck response, CO₂ fertilisation), tipping elements (Greenland, WAIS, AMOC, Amazon, coral reefs), uncertainty, policy implications (precautionary principle); judgement.', 9, 'long')],
  res=[('Selected tipping elements and estimated warming thresholds (Armstrong McKay et al., 2022): Greenland Ice Sheet collapse ~1.5 °C (range 0.8-3.0); low-latitude coral reef die-off ~1.5 °C (1.0-2.0); boreal permafrost abrupt thaw ~1.5 °C (1.0-2.3); Amazon dieback ~3.5 °C (2.0-6.0); AMOC collapse ~4.0 °C (1.4-8.0).',
        [('Identify the tipping elements that could be triggered within the Paris Agreement range of 1.5-2 °C.', 'Greenland Ice Sheet, coral reefs and abrupt permafrost thaw (and possibly the AMOC and Amazon at the lower end of their ranges).'),
         ('Explain why the ranges are so wide.', 'Limited observations, complex interacting processes, model differences and uncertainty about how fast the climate system responds.')])])

S('ch04-st4',
  terms=[('climate impact', 'a consequence of climate change for natural or human systems, such as sea-level rise, extreme weather or crop failure'),
         ('sea-level rise', 'the increase in mean sea level caused by thermal expansion of seawater and melting of glaciers and ice sheets'),
         ('climate refugee (climate migrant)', 'a person forced to leave their home because of climate-related environmental change'),
         ('phenology', 'the timing of seasonal biological events such as flowering, migration and breeding, which climate change is altering'),
         ('vulnerability', 'the degree to which a system or community is susceptible to and unable to cope with the adverse effects of climate change')],
  facts=[('Global mean sea level has risen by about how much since 1901?', 'About 20 cm', ['About 2 cm', 'About 2 m', 'It has fallen'], 'IPCC AR6: about 0.20 m (1901-2018), now rising about 3.7 mm per year.'),
         ('Which country\'s capital is planned to relocate partly because of subsidence and sea-level rise?', 'Indonesia (Jakarta to Nusantara)', ['Norway', 'Egypt', 'Chile'], 'Parts of Jakarta are sinking up to about 25 cm per year.'),
         ('The 2022 floods in Pakistan affected about how many people?', 'About 33 million', ['About 3,000', 'About 300,000', 'About 330 million'], 'About a third of the country was flooded; damages exceeded US$30 billion.'),
         ('Which effect of climate change is mismatching the breeding of great tits with caterpillar abundance in Europe?', 'Earlier spring warming advancing caterpillar emergence', ['Ozone depletion', 'Acid rain', 'Ocean acidification'], 'A phenological mismatch reduces chick survival.')],
  why=[('Explain why low-income countries are often the most vulnerable to climate change.', 'Greater dependence on climate-sensitive agriculture; many people live in exposed areas (deltas, drylands); weaker infrastructure, health systems and finance for adaptation; less capacity to recover - despite contributing least to emissions.'),
       ('Explain how climate change affects coral reef ecosystems.', 'Marine heatwaves cause bleaching as corals expel zooxanthellae; repeated events prevent recovery; acidification slows calcification; storms damage reefs; losses reduce fisheries, tourism and coastal protection for about 500 million people.'),
       ('Explain how climate change can affect human health.', 'More heatwaves cause heat stress and deaths (e.g. Europe 2022, ~60,000 deaths); vector-borne diseases (malaria, dengue) spread to new areas; crop failures cause malnutrition; floods spread water-borne disease; air quality worsens with wildfires.')],
  contrast=[('impacts on ecosystems', 'impacts on societies', 'Ecosystem impacts include range shifts, bleaching, phenological mismatch and extinction risk; societal impacts include crop losses, water shortages, flooding of settlements, health effects and migration - the two are linked because societies depend on ecosystem services.')],
  misc=[('Climate change will affect all places equally.', 'Impacts vary: the Arctic warms 3-4 times faster than average, small islands and deltas face sea-level rise, and some high-latitude areas may see longer growing seasons.'),
        ('Sea-level rise is caused only by melting sea ice.', 'Melting floating sea ice does not raise sea level significantly; thermal expansion and melting land ice (glaciers, Greenland and Antarctic ice sheets) cause the rise.')],
  apply=[('Outline three impacts of climate change on a named small island developing state.', 'e.g. Tuvalu or the Maldives: sea-level rise and storm surges flood land; saltwater intrudes into groundwater and crops; coral bleaching harms fisheries and tourism; possible future migration (Australia-Tuvalu Falepili Union, 2023).', 3),
         ('Suggest two ways in which climate change could affect agriculture in the Sahel.', 'More variable rainfall and longer droughts reduce yields and pasture; higher temperatures increase evaporation and crop stress; desertification; conflict between farmers and herders over shrinking resources.', 2)],
  cases=[('Tuvalu', 'most of the land is less than 3 m above sea level; king tides and storm surges already flood homes and salinise pulaka pits; the 2023 Falepili Union with Australia offers climate mobility', 'the impacts of sea-level rise on societies', 'a low-lying island nation faces loss of land, water and culture, despite producing a negligible share of emissions'),
         ('the 2022 Pakistan floods', 'record monsoon rains and glacial melt flooded about a third of the country, killing over 1,700 people and affecting about 33 million', 'extreme weather linked to climate change', 'attribution studies found climate change likely increased the intensity of the rainfall, showing how warming amplifies extremes'),
         ('Great Barrier Reef bleaching', 'mass bleaching occurred in 1998, 2002, 2016, 2017, 2020, 2022 and 2024', 'climate impacts on ecosystems', 'repeated marine heatwaves now occur more frequently than reefs can recover')],
  evaluate=[('The impacts of climate change will be felt most severely by those who contributed least to it.', ['low-income countries and small islands are most vulnerable', 'least able to adapt', 'climate injustice'], ['high-income countries face severe heatwaves, wildfires and floods too', 'within all countries the poor are most vulnerable'], 'The poorest people and countries are indeed most affected relative to their contribution, which supports climate finance and loss-and-damage funding.')],
  extended=[('Discuss the impacts of climate change on ecosystems and societies, with reference to named examples. [9]', 'Ecosystems (coral bleaching, range shifts, phenology, Arctic); societies (sea-level rise in Tuvalu/Bangladesh, Pakistan floods, heatwaves, agriculture, health, migration); variation by location and wealth; judgement.', 9, 'long')],
  res=[('Projected global mean sea-level rise by 2100 relative to 1995-2014 (IPCC AR6, likely range): SSP1-2.6 (low emissions) 0.32-0.62 m; SSP2-4.5 0.44-0.76 m; SSP5-8.5 (very high emissions) 0.63-1.01 m.',
        [('Calculate the difference between the mid-points of the low and very high emissions scenarios.', 'Mid-points: 0.47 m and 0.82 m; difference ≈ 0.35 m.'),
         ('Explain why sea level will continue to rise after 2100 even under low emissions.', 'Oceans continue to warm and expand for centuries (thermal inertia), and ice sheets respond slowly to past warming.')])])


# =============================================================================================
# ch05 6.3 Climate change: mitigation and adaptation
# =============================================================================================
S('ch05-st1', gens=['carbon_budget_left'],
  terms=[('mitigation', 'actions that reduce the sources or enhance the sinks of greenhouse gases, such as renewable energy, energy efficiency and reforestation'),
         ('carbon capture and storage (CCS)', 'capturing CO₂ from power stations or industry and storing it underground in geological formations'),
         ('direct air capture (DAC)', 'technology that removes CO₂ directly from ambient air for storage or use'),
         ('net zero', 'a state in which human greenhouse-gas emissions are balanced by removals from the atmosphere'),
         ('carbon tax', 'a charge on emissions of CO₂ (or on fossil fuels by carbon content) to make polluters pay and encourage reductions'),
         ('geoengineering', 'deliberate large-scale intervention in the climate system, such as solar radiation management or ocean fertilisation')],
  facts=[('Which country introduced one of the first carbon taxes in 1991 and now has one of the highest rates (over US$100 per tonne)?', 'Sweden', ['China', 'Saudi Arabia', 'Australia'], 'Swedish emissions fell by about a third while GDP grew.'),
         ('The Sleipner project in the North Sea has stored CO₂ beneath the seabed since:', '1996', ['1960', '2015', '2023'], 'About 1 million t of CO₂ a year are injected into a saline aquifer.'),
         ('Which is a nature-based mitigation strategy?', 'Restoring peatlands and mangroves', ['Building coal power stations', 'Solar radiation management with aerosols', 'Expanding airports'], 'They increase carbon sinks and protect stores.'),
         ('According to the IPCC, to limit warming to 1.5 °C global CO₂ emissions must reach net zero around:', '2050', ['2030', '2100', '2200'], 'With emissions falling about 45% from 2010 levels by 2030 (SR1.5).')],
  why=[('Explain why carbon pricing is considered an efficient mitigation tool.', 'It makes emitters pay the external cost, so emissions are cut first where it is cheapest; it encourages innovation and switching to low-carbon options; revenue can fund the transition or be returned to households.'),
       ('Explain why direct air capture is controversial as a mitigation strategy.', 'It is very expensive (about US$400-1,000 per tonne) and energy-intensive; capacity is tiny (thousands of tonnes vs ~37 billion tonnes emitted); it may create moral hazard, delaying emissions cuts.'),
       ('Explain why both reducing emissions and enhancing sinks are needed to reach net zero.', 'Some emissions (cement, agriculture, aviation) are hard to eliminate, so removals (forests, soils, DAC) are needed to balance them; but sinks are limited, so deep emissions cuts are essential.')],
  contrast=[('mitigation', 'adaptation', 'Mitigation tackles the causes of climate change by reducing emissions or increasing sinks; adaptation reduces vulnerability to its impacts (sea walls, drought-resistant crops).'),
            ('a carbon tax', 'a cap-and-trade (emissions trading) scheme', 'A carbon tax sets the price of carbon and lets the quantity emitted vary; cap-and-trade sets the quantity (cap) and lets the market determine the price of allowances (e.g. EU ETS).')],
  misc=[('Planting trees can compensate for all fossil-fuel emissions.', 'The land needed far exceeds what is available, trees take decades to grow, and stored carbon can be lost to fire; tree planting supports but cannot replace emissions cuts.'),
        ('Geoengineering would solve climate change without cutting emissions.', 'Solar radiation management would not stop ocean acidification, carries risks to rainfall and the ozone layer, and could cause "termination shock" if stopped.')],
  apply=[('Suggest four mitigation strategies a national government could adopt.', 'Carbon pricing; phasing out coal and subsidising renewables; energy-efficiency standards for buildings and vehicles; investment in public transport and EV charging; protecting forests and peatlands; methane regulation.', 4),
         ('Outline how the EU Emissions Trading System works.', 'A cap on total emissions from power, industry and aviation decreases each year; companies receive or buy allowances, which can be traded; firms that cut emissions cheaply sell spare allowances; emissions in covered sectors fell about 47% from 2005 to 2023.', 3)],
  cases=[('Sweden\'s carbon tax (1991)', 'the tax rose to about US$120 per tonne of CO₂ and emissions fell by about a third between 1990 and 2020 while GDP grew by over 80%', 'carbon pricing as mitigation', 'a high, predictable price shifted heating from oil to district heating and biomass, decoupling growth from emissions'),
         ('the Sleipner CCS project, Norway', 'Equinor has injected about 1 million t of CO₂ a year into a saline aquifer below the North Sea since 1996, encouraged by Norway\'s offshore carbon tax', 'carbon capture and storage', 'separated CO₂ is stored permanently underground rather than vented, showing CCS is technically feasible at scale'),
         ('the UK\'s coal phase-out', 'coal fell from about 40% of electricity in 2012 to zero when Ratcliffe-on-Soar closed in September 2024', 'reducing emissions in the power sector', 'carbon pricing, renewables growth and regulation removed the most carbon-intensive fuel')],
  evaluate=[('Technological solutions such as CCS and direct air capture are essential to reach net zero.', ['IPCC pathways for 1.5 °C include carbon removal', 'hard-to-abate sectors need CCS'], ['costly, unproven at scale', 'moral hazard', 'renewables and efficiency are cheaper now'], 'Some carbon removal will be needed, but the priority must be rapid deployment of proven, cheaper mitigation.'),
            ('A carbon tax is the most effective way to reduce greenhouse-gas emissions.', ['efficient and technology-neutral (Sweden)', 'raises revenue'], ['politically unpopular (French gilets jaunes, 2018)', 'regressive without compensation', 'regulation needed where demand is price-insensitive'], 'Carbon pricing is powerful but needs complementary regulation, investment and fair compensation to be effective.')],
  extended=[('Evaluate mitigation strategies for reducing greenhouse-gas emissions from energy production. [9]', 'Renewables, nuclear, CCS, efficiency, carbon pricing, fuel switching, coal phase-out (UK), Sweden carbon tax, EU ETS; costs, scale, speed, equity; judgement.', 9, 'long')],
  res=[('Emissions pathway data (Gt CO₂ per year, approximate): 2019 - 38; 2030 required for 1.5 °C - 21; 2030 projected under current policies - 37.',
        [('Calculate the percentage reduction from 2019 needed by 2030 for 1.5 °C and the "emissions gap" under current policies.', '(38 − 21)/38 × 100 ≈ 45%; gap = 37 − 21 = 16 Gt CO₂ per year.'),
         ('Suggest two reasons why the gap is so large.', 'Continued fossil-fuel dependence and new investment; insufficient national targets (NDCs) and weak implementation; rising energy demand in developing economies; political resistance.')])])

S('ch05-st2',
  terms=[('adaptation', 'adjustments in natural or human systems in response to actual or expected climate change, to moderate harm or exploit opportunities'),
         ('resilience', 'the ability of a system or community to absorb shocks, recover and reorganise while retaining its essential functions'),
         ('managed retreat', 'the planned relocation of people and infrastructure away from areas at risk, such as eroding coasts'),
         ('climate-smart agriculture', 'farming practices that increase productivity, build resilience to climate change and reduce emissions'),
         ('early warning system', 'a system that monitors hazards and alerts people in time to take action, e.g. cyclone warnings in Bangladesh')],
  facts=[('How did Bangladesh reduce cyclone deaths from about 300,000 (1970) to fewer than 200 in some recent cyclones?', 'Early warning systems and over 14,000 cyclone shelters', ['Building sea walls around the whole coast', 'Banning coastal settlement', 'Cloud seeding'], 'Volunteers relay warnings and evacuate communities.'),
         ('The Netherlands\' "Room for the River" programme adapts to flooding by:', 'lowering floodplains and moving dykes to give rivers more space', ['raising all dykes by 10 m', 'draining all wetlands', 'diverting rivers into the sea'], 'Completed at about 30 sites by 2015.'),
         ('Which is an example of adaptation rather than mitigation?', 'Planting drought-resistant crop varieties', ['Building a wind farm', 'Installing solar panels', 'Introducing a carbon tax'], 'Adaptation reduces vulnerability to impacts.'),
         ('The Loss and Damage Fund agreed at COP27 (2022) aims to:', 'help vulnerable countries cope with unavoidable climate impacts', ['fund oil exploration', 'pay for carbon capture in rich countries', 'replace the Paris Agreement'], 'It was operationalised at COP28 in Dubai.')],
  why=[('Explain why adaptation is necessary even if emissions are cut rapidly.', 'Greenhouse gases already emitted commit the world to further warming and sea-level rise for decades because of time lags and thermal inertia, so impacts must be managed.'),
       ('Explain why the capacity to adapt differs between countries.', 'Wealth, technology, governance, infrastructure, education and insurance determine whether communities can afford sea walls, irrigation or relocation; poorer countries and communities have fewer resources.'),
       ('Explain how ecosystem-based adaptation can increase resilience.', 'Restoring mangroves, wetlands and forests buffers storm surges, absorbs floodwater, stabilises slopes and supports livelihoods, often at lower cost than hard engineering and with co-benefits for biodiversity and carbon.')],
  contrast=[('hard engineering adaptation', 'soft (ecosystem-based) adaptation', 'Hard engineering uses built structures (sea walls, flood barriers such as the Thames Barrier) that are costly and inflexible; soft adaptation works with natural processes (mangrove restoration, managed retreat, floodplain restoration).'),
            ('adaptation', 'maladaptation', 'Adaptation reduces vulnerability; maladaptation is an action intended to adapt that increases vulnerability or emissions elsewhere, e.g. sea walls that cause erosion downdrift or air conditioning powered by coal.')],
  misc=[('Adaptation means giving up on reducing emissions.', 'Adaptation and mitigation are complementary; adaptation manages unavoidable impacts while mitigation limits how severe they become.'),
        ('Building higher sea walls is always the best adaptation for coastal cities.', 'Sea walls are costly, may fail when exceeded and can damage ecosystems; combinations of nature-based solutions, planning and managed retreat may be better.')],
  apply=[('Suggest three adaptation strategies for a farming community facing more frequent drought.', 'Drought-tolerant and early-maturing varieties; water harvesting (zaï pits, ponds); drip irrigation; diversification of crops and income; crop insurance; agroforestry.', 3),
         ('Outline how a city could adapt to more intense heatwaves.', 'Urban greening and street trees, cool/white roofs, heat action plans and cooling centres (e.g. Ahmedabad Heat Action Plan), early warnings, building design for ventilation, water features.', 3)],
  cases=[('cyclone preparedness in Bangladesh', 'the Cyclone Preparedness Programme with about 76,000 volunteers and over 14,000 shelters reduced deaths from about 300,000 in 1970 to under 200 in Cyclone Amphan (2020)', 'adaptation through early warning and preparedness', 'low-cost community warning and shelters greatly reduced vulnerability even in a low-income country'),
         ('Room for the River, Netherlands', 'about 30 projects (2006-2015, about €2.3 billion) lowered floodplains, moved dykes and created bypass channels on the Rhine delta rivers', 'soft and hard adaptation to flood risk', 'giving rivers space to flood safely increased resilience and created habitat and recreation areas'),
         ('the Ahmedabad Heat Action Plan, India (2013)', 'the first heat action plan in South Asia uses early warnings, cooling centres and public awareness; it is estimated to avoid over 1,000 deaths a year', 'adaptation to extreme heat', 'coordinated warnings and simple measures reduce health impacts of heatwaves')],
  evaluate=[('Adaptation is more important than mitigation for low-income countries.', ['they contribute little to emissions but face severe impacts', 'immediate benefits for lives and livelihoods'], ['mitigation in all countries limits future impacts', 'low-income countries can leapfrog to clean energy', 'adaptation has limits (sea-level rise)'], 'Adaptation is the immediate priority for low-income countries, but global mitigation is essential to keep impacts within adaptable limits.'),
            ('Nature-based solutions are the most effective form of climate adaptation.', ['cheap, flexible, co-benefits for carbon and biodiversity', 'mangroves reduce wave height by up to two-thirds'], ['may be insufficient for extreme events', 'need space and time to establish', 'hard defences protect dense cities (Thames Barrier)'], 'Nature-based solutions are highly effective in many places but are best combined with engineered defences and planning.')],
  extended=[('Evaluate adaptation strategies used in two contrasting named places. [9]', 'Bangladesh cyclone shelters, Netherlands Room for the River, Maldives artificial island (Hulhumalé), Tuvalu land reclamation, Ahmedabad Heat Action Plan; effectiveness, cost, equity, limits; judgement.', 9, 'long')],
  res=[('Deaths in major cyclones striking Bangladesh: Bhola (1970) about 300,000; 1991 cyclone about 138,000; Sidr (2007) about 3,400; Amphan (2020) 26 in Bangladesh.',
        [('Calculate the percentage reduction in deaths between the 1991 cyclone and Sidr.', '(138,000 − 3,400)/138,000 × 100 ≈ 97.5%.'),
         ('Suggest three reasons for the reduction in deaths.', 'Early warning systems (radio, mobile phones, volunteers); thousands of cyclone shelters; mangrove belts and embankments; improved forecasting; evacuation planning.')])])

S('ch05-st3',
  terms=[('UNFCCC', 'the United Nations Framework Convention on Climate Change, opened for signature at the 1992 Rio Earth Summit, whose parties meet at annual Conferences of the Parties (COPs)'),
         ('Kyoto Protocol', 'the 1997 agreement that set legally binding emission-reduction targets for developed (Annex I) countries for 2008-2012'),
         ('Paris Agreement', 'the 2015 agreement in which almost all countries committed to hold warming well below 2 °C and pursue efforts to limit it to 1.5 °C, through nationally determined contributions'),
         ('nationally determined contribution (NDC)', 'a country\'s self-set climate action plan and emissions target under the Paris Agreement, updated every five years'),
         ('common but differentiated responsibilities', 'the principle that all countries share responsibility for climate change, but developed countries should lead because of greater historical emissions and capacity'),
         ('global stocktake', 'a five-yearly assessment under the Paris Agreement of collective progress towards its goals; the first was completed at COP28 in 2023')],
  facts=[('Under the Kyoto Protocol, which countries had binding targets?', 'Developed (Annex I) countries only', ['All countries', 'Only China and India', 'Only small island states'], 'Developing countries had no binding targets.'),
         ('Which major emitter signed but never ratified the Kyoto Protocol?', 'The United States', ['Germany', 'Japan', 'The United Kingdom'], 'Canada also withdrew in 2011.'),
         ('The Paris Agreement aims to limit warming to:', 'well below 2 °C, pursuing efforts towards 1.5 °C', ['exactly 3 °C', 'below 0.5 °C', 'no specific limit'], 'Article 2.'),
         ('At COP28 (Dubai, 2023), parties agreed for the first time to:', 'transition away from fossil fuels in energy systems', ['ban all cars', 'end the UNFCCC', 'build new coal plants'], 'Also to triple renewable capacity by 2030.')],
  why=[('Explain why the Paris Agreement achieved wider participation than the Kyoto Protocol.', 'It is bottom-up: each country sets its own NDC, so all countries, including China, India and the USA, could join; targets are non-binding but reporting and review are; ambition is ratcheted up every five years.'),
       ('Explain why international climate agreements are difficult to achieve.', 'Climate is a global commons - each country bears the costs of cuts but shares the benefits (free-rider problem); differing levels of development, responsibility and vulnerability; fossil-fuel interests; short political cycles.'),
       ('Explain why current NDCs are insufficient to meet the Paris goals.', 'Fully implemented NDCs would lead to about 2.5-2.9 °C of warming (UNEP Emissions Gap Report 2023); many are not on track; finance for developing countries is below promises.')],
  contrast=[('the Kyoto Protocol', 'the Paris Agreement', 'Kyoto was top-down with legally binding targets for developed countries only; Paris is bottom-up with self-determined targets (NDCs) for all countries and a binding process of reporting and five-yearly ratchets.'),
            ('a top-down agreement', 'a bottom-up agreement', 'A top-down agreement sets targets centrally and allocates them to countries; a bottom-up agreement lets each country pledge its own contribution, increasing participation but reducing ambition and enforceability.')],
  misc=[('The Paris Agreement legally requires each country to meet its NDC.', 'Countries are legally required to prepare, report and update NDCs, but meeting the targets is not legally binding.'),
        ('The Kyoto Protocol failed completely.', 'Annex I countries that remained collectively exceeded their first-period target (though partly due to the collapse of Eastern European industry), and Kyoto created carbon markets and monitoring systems used today.')],
  apply=[('Outline the main features of the Paris Agreement.', 'Temperature goals (well below 2 °C, 1.5 °C); NDCs from all parties updated every five years; transparency framework; global stocktake; climate finance ($100 billion a year goal, new goal of $300 billion by 2035 from COP29); adaptation and loss and damage.', 4),
         ('Suggest why small island states have pushed for the 1.5 °C goal.', 'Their survival depends on limiting sea-level rise and coral loss; the difference between 1.5 and 2 °C is decisive for low-lying atolls (Alliance of Small Island States).', 2)],
  cases=[('the Paris Agreement (COP21, 2015)', 'adopted by 196 parties, it entered into force in 2016; the USA withdrew in 2020, rejoined in 2021 and announced withdrawal again in 2025', 'international climate agreements', 'its flexible, bottom-up design gained near-universal participation but relies on peer pressure rather than enforcement'),
         ('the Kyoto Protocol (1997)', 'Annex I parties agreed to cut emissions by about 5% below 1990 levels in 2008-2012; the USA never ratified and Canada withdrew', 'the limits of top-down agreements', 'excluding developing countries and lacking major emitters limited its effect on global emissions, which rose about 40% from 1997 to 2012')],
  evaluate=[('The Paris Agreement is more effective than the Kyoto Protocol.', ['near-universal participation including China and India', 'ratchet mechanism', 'projected warming fell from ~4 °C to ~2.7 °C'], ['targets not binding', 'current NDCs insufficient', 'withdrawal by the USA undermines it'], 'Paris is more effective in participation and has bent the curve of projected warming, but it is not yet sufficient to meet its own goals.'),
            ('International agreements are less important than national and local action in tackling climate change.', ['implementation happens nationally (UK Climate Change Act, Sweden)', 'cities and businesses lead (C40)'], ['agreements set common goals and prevent free-riding', 'finance and technology transfer require international frameworks'], 'Both are essential: agreements set direction and fairness, while national and local action delivers emissions cuts.')],
  extended=[('Evaluate the effectiveness of international agreements in addressing climate change. [9]', 'UNFCCC, Kyoto (targets, flexibility mechanisms, limits), Paris (NDCs, ratchet, stocktake, finance), COP26-29 outcomes; comparison with Montreal Protocol; judgement.', 9, 'long')],
  res=[('Projected warming by 2100 (approximate): before Paris (no policies, ~2010) about 4 °C; current policies (2023) about 2.7 °C; full implementation of unconditional NDCs about 2.5 °C; with all net-zero pledges about 1.9-2.1 °C.',
        [('Calculate the reduction in projected warming from pre-Paris to current policies.', '4 − 2.7 = 1.3 °C.'),
         ('Evaluate what these data suggest about the success of the Paris Agreement.', 'Paris has reduced projected warming considerably, but even full implementation of pledges overshoots 1.5 °C; success depends on turning pledges into action.')])])


# =============================================================================================
# ch06 7.1 Natural resources: uses and management
# =============================================================================================
S('ch06-st1', gens=['rp_ratio'],
  terms=[('renewable natural capital', 'natural capital that can be generated or replaced as fast as it is used, e.g. living species, forests, fish stocks, solar energy'),
         ('replenishable natural capital', 'non-living natural capital that is replaced over time by natural processes, e.g. groundwater, soil, the ozone layer'),
         ('non-renewable natural capital', 'natural capital that is either irreplaceable or replaced only over geological timescales, e.g. fossil fuels, minerals'),
         ('reserve', 'the part of a resource that has been discovered and can be extracted economically with current technology'),
         ('resource', 'any part of the environment that is useful to humans, including materials, energy and ecosystem services')],
  facts=[('Groundwater in an aquifer is best classified as:', 'replenishable natural capital', ['non-renewable natural capital', 'renewable living capital', 'human-made capital'], 'It is replenished by recharge but can be depleted faster than replacement.'),
         ('Which is an example of non-renewable natural capital?', 'Copper ore', ['A tuna stock', 'Solar radiation', 'A teak forest'], 'Ores form over geological time.'),
         ('Rare-earth elements used in wind turbines and EVs are mostly processed in:', 'China (about 85-90% of processing)', ['Norway', 'Peru', 'Kenya'], 'This raises resource-security concerns.'),
         ('Which statement describes the difference between a resource and a reserve?', 'A reserve is the part of a resource that is known and economically extractable', ['A reserve is always larger than a resource', 'They mean the same thing', 'A resource has already been used'], 'Reserves change with price and technology.')],
  why=[('Explain why replenishable resources can become non-renewable if mismanaged.', 'If extraction exceeds the replacement rate - e.g. pumping fossil groundwater faster than recharge, eroding soil faster than it forms - the stock is depleted and may take centuries or millennia to recover.'),
       ('Explain why reserves of non-renewable resources can increase over time.', 'Higher prices make lower-grade deposits economic; new technology (fracking, deep-sea drilling) allows extraction of previously inaccessible deposits; exploration discovers new deposits.'),
       ('Explain why some renewable resources are being depleted.', 'They are harvested faster than they regenerate (overfishing, deforestation); habitat damage reduces regeneration; open access encourages over-use (tragedy of the commons).')],
  contrast=[('renewable natural capital', 'non-renewable natural capital', 'Renewable natural capital regenerates on human timescales if used within its yield (forests, fish); non-renewable capital forms over geological time and is depleted by use (oil, copper).'),
            ('a resource', 'a reserve', 'A resource is the total amount of a material that exists in a usable form; a reserve is the portion that has been located and can be extracted economically with current technology.')],
  misc=[('Non-renewable resources will run out at the date given by the R/P ratio.', 'R/P ratios change as reserves are re-estimated, prices rise, technology improves, recycling increases and demand changes.'),
        ('Renewable resources can be used without limit.', 'Living renewable resources are limited by their regeneration rate; exceeding it depletes the stock.')],
  apply=[('Classify each as renewable, replenishable or non-renewable natural capital: an Atlantic salmon stock, phosphate rock, an aquifer in the Sahara, a mangrove forest, uranium.', 'Salmon: renewable; phosphate rock: non-renewable; Saharan (fossil) aquifer: effectively non-renewable (replenishable in principle); mangrove: renewable; uranium: non-renewable.', 4),
         ('Suggest why lithium is described as a critical raw material.', 'It is essential for batteries in EVs and grid storage, demand is rising rapidly, supply is concentrated (Australia, Chile, China), and extraction has environmental and social impacts (water use in the Atacama).', 3)],
  cases=[('lithium extraction in the Salar de Atacama, Chile', 'brine evaporation uses large volumes of water in one of the driest places on Earth, affecting local Indigenous communities and flamingo habitat', 'the costs of extracting natural capital for the energy transition', 'a resource needed for low-carbon technology creates local environmental pressures'),
         ('the Nubian Sandstone Aquifer System', 'shared by Egypt, Libya, Sudan and Chad, it holds about 150,000 km³ of largely fossil water; Libya\'s Great Man-Made River pumps it to coastal cities', 'replenishable capital being used as non-renewable', 'recharge is negligible today, so extraction depletes water stored thousands of years ago')],
  evaluate=[('Non-renewable resources should be conserved for future generations rather than used now.', ['intergenerational equity', 'finite stocks'], ['resources have value only when used', 'substitutes and technology may replace them', 'current poverty requires development'], 'Use should be efficient and paired with investment in substitutes and recycling, so future generations inherit equivalent capital.')],
  extended=[('Explain, with named examples, the differences between renewable, replenishable and non-renewable natural capital and how each can be managed sustainably. [7]', 'Definitions; examples (forests, fish; groundwater, soil, ozone; fossil fuels, minerals); sustainable management (harvest within yield, recharge-based limits, recycling and substitution).', 7, 'explain')],
  res=[('Global R/P ratios at end of 2020 (approximate, Energy Institute): oil 54 years; natural gas 49 years; coal 139 years.',
        [('Suggest why the R/P ratio for oil was about 30 years in the 1980s but over 50 years in 2020.', 'New discoveries (deep water, Canadian oil sands, US shale via fracking), higher prices making more reserves economic, and improved recovery rates added to reserves faster than production grew.'),
         ('Explain why coal has the highest R/P ratio but is being phased out.', 'Coal is the most carbon-intensive fuel, so climate policy, air-pollution concerns and cheap renewables reduce demand regardless of reserves.')])])

S('ch06-st2',
  terms=[('dynamic nature of resources', 'the idea that what counts as a resource and its value change over time with technology, culture, prices and needs'),
         ('economic value', 'the value of a resource that can be expressed in market prices'),
         ('ecological value', 'the value of a resource in maintaining ecosystem functions, without a direct market price'),
         ('intrinsic value', 'the value something has in itself, independent of its usefulness to humans'),
         ('total economic value', 'the sum of use values (direct, indirect, option) and non-use values (existence, bequest) of a resource')],
  facts=[('Which resource became valuable only after the invention of the internal combustion engine?', 'Crude oil (for petrol)', ['Timber', 'Clean water', 'Fish'], 'Oil was used in small quantities before but its value transformed in the 20th century.'),
         ('Uranium became a valuable resource mainly because of:', 'the development of nuclear power and weapons in the 20th century', ['its use as a fertiliser', 'its value as jewellery', 'its use in cooking'], 'Value depends on technology.'),
         ('The value of a wetland for flood control is an example of:', 'an indirect use value (regulating service)', ['a direct use value', 'an existence value', 'a market price'], 'It benefits people without consuming the wetland.'),
         ('Which resource lost value when synthetic alternatives were developed in the early 20th century?', 'Natural indigo dye', ['Lithium', 'Rare-earth elements', 'Fresh water'], 'Synthetic indigo replaced plant-based indigo.')],
  why=[('Explain why the value of a resource can change over time.', 'New technologies create uses (lithium for batteries) or substitutes (synthetic indigo, plastics replacing ivory); cultural values change (whales from oil source to tourism resource); scarcity raises prices; environmental awareness gives value to ecosystem services.'),
       ('Explain why some values of natural resources are difficult to measure.', 'Regulating, cultural and non-use values (existence, bequest, spiritual) have no market price; valuations rely on surveys and models that are uncertain and contested.'),
       ('Explain how whales illustrate the dynamic nature of resources.', 'In the 19th century whales were hunted for oil and baleen; substitutes (petroleum, plastics) and conservation values changed them into a resource for whale-watching tourism worth over US$2 billion a year.')],
  contrast=[('use value', 'non-use value', 'Use values come from using a resource directly (timber, fish) or indirectly (flood regulation); non-use values come from knowing a resource exists (existence value) or will be available for future generations (bequest value).'),
            ('economic value', 'intrinsic value', 'Economic value reflects usefulness to people and can often be priced; intrinsic value is value in itself, independent of human use, central to ecocentric worldviews.')],
  misc=[('A resource\'s value is fixed by its physical properties.', 'Value depends on human needs, technology, culture and markets, which change over time.'),
        ('Resources with no market price have no value.', 'Many ecosystem services (pollination, climate regulation) have enormous value even though they are not traded.')],
  apply=[('Suggest how the value of cobalt has changed and why.', 'Cobalt was a minor metal used in pigments and alloys; demand and price rose with lithium-ion batteries for phones and EVs, making DR Congo mines (about 70% of supply) strategically important.', 3),
         ('Identify direct use, indirect use and existence values of a coral reef.', 'Direct: fishing, tourism, diving; indirect: coastal protection, nursery habitat, carbon/nutrient cycling; existence: knowing reefs and their species exist.', 3)],
  cases=[('whaling and whale-watching', 'commercial whaling for oil peaked in the 20th century; the 1986 IWC moratorium followed, and whale-watching now attracts about 13 million people a year', 'the changing value of resources', 'technological substitutes and changing values transformed whales from an extractive to a non-consumptive resource'),
         ('cobalt in the Democratic Republic of Congo', 'the DRC produces about 70% of the world\'s cobalt, much demanded for EV batteries, with concerns about artisanal mining and child labour', 'how technology changes resource value', 'battery technology made a minor metal strategically valuable, with social and environmental consequences')],
  evaluate=[('The value of natural resources should be measured mainly in economic terms.', ['makes values comparable in decisions', 'supports payments for ecosystem services'], ['intrinsic, cultural and spiritual values cannot be priced', 'markets undervalue future generations'], 'Economic valuation is useful but incomplete; decisions should also respect non-market and intrinsic values.')],
  extended=[('Discuss how the value of a named natural resource has changed over time. [9]', 'e.g. whales, oil, lithium, cobalt, uranium, rainforests: technology, culture, scarcity, environmental awareness; different EVSs; judgement.', 9, 'long')],
  res=[('Price of lithium carbonate (approximate, US$ per tonne): 2015 - 6,000; 2018 - 16,000; 2020 - 7,000; late 2022 - 80,000; 2024 - 13,000.',
        [('Calculate the percentage increase in price between 2020 and late 2022.', '(80,000 − 7,000)/7,000 × 100 ≈ 1,043%.'),
         ('Suggest reasons for the large fluctuations in price.', 'Rapid growth in EV demand outpaced new mine supply, causing a spike; new projects in Australia, Chile, China and Africa then increased supply and prices fell; speculation and market concentration.')])])

S('ch06-st3',
  terms=[('sustainable resource management', 'the use of resources at a rate that does not exceed their regeneration and that maintains ecosystems and benefits for future generations'),
         ('tragedy of the commons', 'the depletion of a shared, open-access resource by individuals acting in their own interest (Garrett Hardin, 1968)'),
         ('common-pool resource', 'a resource that is shared, where one person\'s use reduces availability to others and it is difficult to exclude users, e.g. fisheries or grazing land'),
         ('sustainable forest management', 'managing forests to maintain their biodiversity, productivity, regeneration and social and economic functions, e.g. FSC certification'),
         ('circular resource use', 'keeping materials in use through reuse, repair and recycling, reducing extraction of new resources')],
  facts=[('Elinor Ostrom won the 2009 Nobel Prize in Economics for showing that:', 'communities can manage common-pool resources sustainably without privatisation or state control', ['all commons will inevitably collapse', 'markets always allocate resources efficiently', 'resources are unlimited'], 'Examples include Swiss alpine pastures and Spanish huertas.'),
         ('What does FSC certification indicate about timber?', 'It comes from forests managed to environmental and social standards', ['It is from a plantation of exotic species only', 'It is imported tax-free', 'It is recycled plastic'], 'The Forest Stewardship Council was founded in 1993.'),
         ('Which management tool sets a limit on how much timber can be harvested each year from a forest?', 'Annual allowable cut', ['Clear-felling', 'Feed-in tariff', 'Environmental impact statement'], 'Based on the forest\'s growth rate.'),
         ('Which country\'s forest cover rose from about 21% (1980s) to over 50% through payments for ecosystem services?', 'Costa Rica', ['Indonesia', 'Brazil', 'Madagascar'], 'Funded partly by a fuel tax.')],
  why=[('Explain why the "tragedy of the commons" leads to over-exploitation.', 'Each user captures the full benefit of extra use but shares the cost of depletion with all others, so individuals rationally over-use; without rules, the resource collapses (e.g. open-access fisheries).'),
       ('Explain how community management can avoid the tragedy of the commons.', 'Clear boundaries and membership, locally designed rules, monitoring and graduated sanctions, conflict resolution and recognition by government (Ostrom\'s principles) give users a stake and allow cooperation.'),
       ('Explain why certification schemes can help achieve sustainable resource use.', 'They set independent standards, allow consumers and businesses to choose sustainably produced goods, and reward producers with market access or premium prices; but they rely on trust, audits and consumer demand.')],
  contrast=[('open-access resources', 'common-pool resources managed by communities', 'Open-access resources have no rules on use and tend to be over-exploited; community-managed common-pool resources have rules on who can use them and how much, which can sustain them.')],
  misc=[('The tragedy of the commons proves that only privatisation can protect shared resources.', 'Ostrom showed many communities manage commons sustainably through local institutions; privatisation or state control are not the only solutions.'),
        ('Certification guarantees that a product is sustainable.', 'Certification standards vary, audits can be weak and fraud occurs; it improves practice but does not guarantee sustainability.')],
  apply=[('Suggest three strategies to manage a tropical forest sustainably.', 'Selective logging with annual allowable cuts and long rotations; reduced-impact logging; FSC certification; community forestry; payments for ecosystem services/REDD+; protected core areas; replanting with native species.', 3),
         ('Outline how the Törbel community in Switzerland has managed alpine pasture sustainably for centuries.', 'Rules dating from 1483 limit the number of cows each household can graze to the number it can feed over winter; monitoring and fines enforce the rules - an example used by Ostrom.', 3)],
  cases=[('Törbel, Switzerland', 'villagers have managed alpine meadows and forests as commons since at least 1224, with rules limiting grazing', 'community management of common-pool resources', 'locally made, enforced rules prevented over-grazing for centuries, contradicting the inevitability of the tragedy of the commons'),
         ('community forestry in Nepal', 'over 22,000 community forest user groups manage about a third of Nepal\'s forests; forest cover increased from about 29% in 1994 to about 45% by 2016', 'sustainable management of renewable resources', 'handing control to local users gave them incentives and rules to protect and regenerate forests'),
         ('the Grand Banks cod fishery', 'overfishing under weak regulation caused collapse in 1992', 'the tragedy of the commons', 'competitive harvesting of a shared stock exceeded its natural income')],
  evaluate=[('Community management is more effective than government regulation for sustaining natural resources.', ['local knowledge and legitimacy (Nepal, Törbel)', 'lower enforcement costs'], ['may exclude marginalised groups', 'cannot manage large-scale or migratory resources (ocean fisheries, atmosphere)', 'needs government support'], 'Community management works well for local commons, but large-scale resources require government and international regulation; co-management combines the strengths of both.')],
  extended=[('Evaluate strategies for the sustainable management of a named natural resource. [9]', 'e.g. forests (FSC, REDD+, community forestry in Nepal, Costa Rica PES), fisheries (ITQs, MPAs), groundwater, minerals (recycling, substitution); Ostrom principles; judgement.', 9, 'long')],
  res=[('Community forestry in Nepal (approximate): number of community forest user groups 1990: 300; 2000: 12,000; 2020: 22,000; national forest cover 1994: 29%; 2016: 45%.',
        [('Calculate the percentage-point increase in forest cover and the mean annual increase in user groups between 2000 and 2020.', 'Forest cover +16 percentage points; (22,000 − 12,000)/20 = 500 groups per year.'),
         ('Suggest why forest cover increased, other than community management.', 'Migration of rural people to cities and abroad reduced pressure; remittances lowered dependence on fuelwood; LPG and biogas replaced firewood; natural regeneration on abandoned farmland.')])])


# =============================================================================================
# ch07 7.2 Energy sources: uses and management
# =============================================================================================
S('ch07-st1', gens=['capacity_factor'],
  terms=[('renewable energy', 'energy from sources that are naturally replenished on human timescales, such as solar, wind, hydro, geothermal, tidal and biomass'),
         ('non-renewable energy', 'energy from finite sources formed over geological time, such as coal, oil, natural gas and uranium'),
         ('intermittency', 'the variability of output from some renewable sources (wind, solar) that depend on weather or time of day'),
         ('energy mix', 'the combination of primary energy sources used by a country or region'),
         ('baseload power', 'the minimum level of electricity demand over a period, traditionally met by sources that run continuously, such as nuclear, coal or hydro'),
         ('fracking (hydraulic fracturing)', 'injecting water, sand and chemicals at high pressure into shale rock to release oil or gas')],
  facts=[('Which source supplied the largest share of global primary energy in 2023?', 'Oil', ['Solar', 'Nuclear', 'Wind'], 'Fossil fuels supplied about 80% of primary energy (oil ~31%, coal ~26%, gas ~23%).'),
         ('Which renewable source generates the most electricity globally?', 'Hydropower', ['Tidal', 'Geothermal', 'Wave'], 'Hydro provided about 14% of global electricity in 2023; wind and solar together about 13%.'),
         ('Approximately what share of Iceland\'s electricity comes from hydro and geothermal?', 'Almost 100%', ['About 10%', 'About 50%', 'About 30%'], 'Its location on the Mid-Atlantic Ridge gives abundant geothermal heat.'),
         ('Which disadvantage applies to nuclear power?', 'Long-lived radioactive waste and high construction costs', ['High CO₂ emissions during operation', 'Intermittent output', 'Large air-pollution from smoke'], 'Nuclear is low-carbon and reliable but costly and controversial.')],
  why=[('Explain why the intermittency of wind and solar power is a challenge for electricity grids.', 'Output varies with weather and time of day and may not match demand (e.g. evening peaks); grids must balance supply and demand every second, so storage (batteries, pumped hydro), interconnectors, flexible demand or back-up generation are needed.'),
       ('Explain why fossil fuels still dominate global energy use.', 'High energy density, existing infrastructure (power stations, vehicles, pipelines), reliability, established industries and jobs, subsidies (over US$1 trillion of explicit consumption subsidies in 2022), and rising demand in emerging economies.'),
       ('Explain one advantage and one disadvantage of large hydroelectric dams.', 'Advantage: low-carbon, reliable, flexible electricity with water storage and flood control; disadvantage: displacement of people, loss of habitats, blocked fish migration and sediment, methane from flooded vegetation in tropical reservoirs.')],
  contrast=[('renewable energy', 'non-renewable energy', 'Renewable sources are replenished naturally and usually have low operating emissions (wind, solar, hydro); non-renewable sources are finite stocks that release CO₂ when burned (fossil fuels) or produce radioactive waste (nuclear).'),
            ('solar photovoltaic', 'solar thermal', 'Photovoltaic panels convert light directly into electricity; solar thermal collectors use the Sun\'s heat for hot water or to generate steam in concentrated solar power plants.')],
  misc=[('Renewable energy has no environmental impact.', 'Renewables have impacts: mining of materials, land use, bird and bat collisions with wind turbines, dams flooding valleys, biomass competing with food.'),
        ('Nuclear power is a major source of greenhouse gases.', 'Life-cycle emissions of nuclear power are very low (about 12 g CO₂e/kWh), comparable with wind.')],
  apply=[('Compare the advantages and disadvantages of wind power and coal power.', 'Wind: low-carbon, no fuel cost, fast to build; intermittent, visual and noise impacts, bird strikes. Coal: reliable baseload, existing infrastructure, cheap in some places; highest CO₂ per kWh, air pollution, mining impacts.', 4),
         ('Suggest why Kenya generates a large share of its electricity from geothermal energy.', 'It lies on the East African Rift Valley with high heat flow near the surface (Olkaria field); this provides reliable, low-carbon baseload power and reduces reliance on drought-sensitive hydro and imported oil.', 2)],
  cases=[('Iceland\'s geothermal and hydro energy', 'almost all electricity and about 90% of home heating come from renewable sources', 'the influence of geology on energy choices', 'location on a plate boundary provides geothermal heat, and glacial rivers provide hydropower'),
         ('the Three Gorges Dam, China', 'the world\'s largest power station (22.5 GW) produces about 100 TWh a year but displaced about 1.3 million people', 'the benefits and costs of large-scale renewable energy', 'low-carbon electricity and flood control came at a high social and ecological cost'),
         ('the Fukushima Daiichi nuclear disaster (2011)', 'a tsunami caused three reactor meltdowns; Germany then decided to close all its nuclear plants (completed 2023)', 'public perception and energy choices', 'a disaster in one country changed energy policy elsewhere, increasing reliance on gas and coal in the short term')],
  evaluate=[('Nuclear power should be a key part of the transition to a low-carbon energy system.', ['very low emissions, reliable baseload', 'small land footprint (France 65% nuclear)'], ['high cost and long build times (Hinkley Point C)', 'radioactive waste and accident risk', 'renewables now cheaper'], 'Nuclear can support decarbonisation where it is accepted and affordable, but renewables with storage are likely to supply most new low-carbon electricity.'),
            ('Hydroelectric power is the most sustainable source of electricity.', ['renewable, reliable, flexible, long-lived', 'storage for balancing wind and solar'], ['displacement and ecological damage', 'methane from reservoirs', 'vulnerable to drought (Zambia, Brazil)'], 'Hydropower is valuable but its sustainability depends on site, scale and management; small and run-of-river schemes are often more sustainable.')],
  extended=[('Evaluate the advantages and disadvantages of two named energy sources. [9]', 'Compare e.g. solar PV and coal, or nuclear and wind: emissions, reliability, cost, land, resources, waste, safety, energy security; named examples (Rajasthan solar, Three Gorges, Fukushima, Hinkley Point C); judgement.', 9, 'long')],
  res=[('Life-cycle greenhouse-gas emissions of electricity (g CO₂e per kWh, IPCC median approx.): coal 820; gas (combined cycle) 490; biomass 230; solar PV 48; hydro 24; nuclear 12; onshore wind 11.',
        [('Calculate how many times more CO₂e per kWh is emitted by coal than by onshore wind.', '820 / 11 ≈ 75 times.'),
         ('Suggest why solar PV has higher life-cycle emissions than wind or nuclear even though it has no emissions during operation.', 'Energy-intensive manufacture of panels (silicon purification), often using coal-powered electricity, and lower capacity factors spreading embodied emissions over less output.')])])

S('ch07-st2', gens=['energy_mix'],
  terms=[('energy security', 'the uninterrupted availability of energy sources at an affordable price'),
         ('energy independence', 'the ability of a country to meet its energy needs from domestic sources without relying on imports'),
         ('energy poverty', 'lack of access to modern energy services such as electricity and clean cooking'),
         ('geopolitics of energy', 'the influence of political power and international relations on energy supply and prices'),
         ('diversification', 'using a range of energy sources and suppliers to reduce the risk of disruption')],
  facts=[('The 2022 Russian invasion of Ukraine affected European energy security mainly because:', 'about 40% of EU gas imports had come from Russia', ['Europe imported all its coal from Ukraine', 'it destroyed all EU wind farms', 'oil was discovered in Ukraine'], 'Gas prices rose sharply and the EU diversified to LNG and renewables.'),
         ('About how many people lacked access to electricity in 2022 (IEA)?', 'About 760 million', ['About 7 million', 'About 2 billion', 'About 4 billion'], 'Most live in sub-Saharan Africa; about 2.3 billion lacked clean cooking.'),
         ('The 1973 oil crisis led France to:', 'rapidly expand nuclear power (the Messmer Plan)', ['abandon electricity', 'build only coal plants', 'import more oil'], 'Nuclear now supplies about 65-70% of French electricity.'),
         ('Which factor most influences whether a country uses geothermal energy?', 'Its geology (location near plate boundaries or hotspots)', ['Its population density', 'Its official language', 'Its distance from the equator only'], 'e.g. Iceland, Kenya, New Zealand, Indonesia.')],
  why=[('Explain why energy security is a priority for governments.', 'Energy underpins the economy, transport, food, health and defence; dependence on imports exposes countries to price shocks and political pressure (1973 oil crisis, 2022 gas crisis); reliable supply is politically essential.'),
       ('Explain how renewable energy can improve energy security.', 'Domestic renewable sources reduce dependence on imported fuels and price volatility; distributed generation (rooftop solar) is less vulnerable to single points of failure; there is no fuel to be cut off.'),
       ('Explain how cultural and political factors influence energy choices.', 'Public opinion (anti-nuclear movements in Germany), government priorities (climate targets, jobs in coal regions), lobbying by industries, cultural attitudes to landscape (opposition to wind farms) and international agreements shape energy policy.')],
  contrast=[('energy security', 'energy independence', 'Energy security means reliable, affordable access to energy, which can include imports from diverse, trusted suppliers; energy independence means meeting needs entirely from domestic sources.')],
  misc=[('Energy security can only be achieved by producing all energy domestically.', 'Diverse, reliable imports, storage, interconnection and efficiency can provide security without full independence.'),
        ('Energy choices are determined only by the availability of resources.', 'Cost, technology, politics, public opinion, environmental policy and international relations also strongly shape energy choices.')],
  apply=[('Suggest four factors that influence a country\'s choice of energy sources.', 'Availability of domestic resources; cost and technology; energy security and geopolitics; environmental and climate policy; public opinion; existing infrastructure; economic development and demand.', 4),
         ('Outline how Germany\'s Energiewende has changed its energy mix.', 'Renewables rose from about 6% of electricity in 2000 to over 50% in 2023; nuclear phased out in 2023; coal reduced but used during the 2022 gas crisis; high electricity prices and grid challenges.', 3)],
  cases=[('Germany\'s Energiewende', 'renewables supplied over half of German electricity in 2023 and the last nuclear plants closed in April 2023', 'political and cultural influences on energy choices', 'strong public opposition to nuclear power and climate policy drove a transition that improved long-term security but caused short-term reliance on coal'),
         ('Europe\'s response to the 2022 gas crisis', 'the EU cut Russian pipeline gas imports from about 40% to under 10% of supply within two years, building LNG terminals and accelerating renewables (REPowerEU)', 'energy security and diversification', 'a geopolitical shock forced rapid diversification of suppliers and sources'),
         ('Kenya\'s geothermal expansion', 'geothermal provides about 45% of Kenya\'s electricity from the Olkaria fields in the Rift Valley', 'geology and energy security', 'domestic, reliable geothermal power reduces dependence on imported oil and on drought-sensitive hydropower')],
  evaluate=[('Energy security is more important than climate change in determining national energy policy.', ['shocks (1973, 2022) cause immediate economic and political crises', 'governments prioritise affordability'], ['renewables now improve both security and climate goals', 'climate impacts threaten energy infrastructure', 'international commitments (Paris)'], 'Security often dominates in the short term, but renewables increasingly allow countries to meet both priorities together.')],
  extended=[('Discuss the factors that affect the energy choices of a named country. [9]', 'e.g. France (nuclear), Germany (Energiewende), Norway (hydro and oil exports), China (coal and renewables), Kenya (geothermal): resources, economics, geopolitics, culture, climate policy, technology; judgement.', 9, 'long')],
  res=[('EU imports of Russian gas as a share of total gas imports (approximate): 2021 - 40%; 2022 - 24%; 2023 - 15% (pipeline about 8%, LNG about 7%).',
        [('Calculate the percentage reduction in the share of Russian gas between 2021 and 2023.', '(40 − 15)/40 × 100 = 62.5%.'),
         ('Suggest two ways the EU replaced Russian gas.', 'LNG imports from the USA and Qatar; pipeline gas from Norway; reduced demand through efficiency and price; faster deployment of wind, solar and heat pumps.')])])

S('ch07-st3',
  terms=[('energy efficiency', 'using less energy to provide the same service, e.g. LED lighting or better insulation'),
         ('energy conservation', 'reducing energy use by changing behaviour, e.g. turning off lights or travelling less'),
         ('energy transition', 'the shift from fossil-fuel-based energy systems to low-carbon sources such as renewables and nuclear'),
         ('rebound effect', 'the tendency for efficiency gains to be partly offset by increased use because the service becomes cheaper'),
         ('feed-in tariff', 'a guaranteed price paid to producers of renewable electricity fed into the grid, used to encourage investment'),
         ('energy storage', 'technologies that store energy for later use, such as lithium-ion batteries, pumped hydro and green hydrogen')],
  facts=[('By approximately how much did the cost of solar PV electricity fall between 2010 and 2023?', 'About 90%', ['About 10%', 'About 30%', 'It increased'], 'IRENA: levelised cost fell by about 90%.'),
         ('LED bulbs use approximately how much less energy than incandescent bulbs for the same light?', 'About 75-90% less', ['About 5% less', 'About the same', 'More energy'], 'Incandescent bulbs waste most energy as heat.'),
         ('At COP28 countries agreed to do what with renewable capacity by 2030?', 'Triple it', ['Halve it', 'Freeze it', 'Double nuclear instead'], 'And double the rate of energy-efficiency improvement.'),
         ('Which is the largest form of grid energy storage worldwide?', 'Pumped-storage hydropower', ['Flywheels', 'Compressed air only', 'Hydrogen fuel cells'], 'It provides over 90% of stored energy capacity, though batteries are growing fastest.')],
  why=[('Explain why improving energy efficiency is often called the "first fuel".', 'It is usually the cheapest way to cut emissions and costs, reduces demand so fewer power stations are needed, improves energy security, and benefits households (lower bills) with no fuel or emissions.'),
       ('Explain how the rebound effect can reduce the benefits of energy efficiency.', 'Efficient technologies lower the cost of a service, so people use more of it (driving further in efficient cars, heating homes to higher temperatures), offsetting part of the savings.'),
       ('Explain why energy storage is important for the transition to low-carbon energy.', 'Storage shifts surplus wind and solar output to times of high demand, balances the grid, reduces curtailment and the need for fossil back-up, and allows higher shares of variable renewables.')],
  contrast=[('energy efficiency', 'energy conservation', 'Efficiency uses technology to provide the same service with less energy (LEDs, insulation); conservation reduces energy demand through behaviour change (turning off lights, cycling).')],
  misc=[('The transition to renewables is too expensive to be possible.', 'Solar and onshore wind are now the cheapest new electricity in most of the world; costs fell about 90% and 70% respectively since 2010.'),
        ('Electric vehicles produce no emissions.', 'EVs have no tailpipe emissions, but manufacturing (especially batteries) and electricity generation produce emissions; life-cycle emissions are still usually lower than petrol cars.')],
  apply=[('Suggest four ways a household could reduce its energy consumption.', 'Loft and wall insulation; heat pump instead of gas boiler; LED lighting; efficient appliances; smart thermostat and lower thermostat setting; draught-proofing; reduce car use; solar panels.', 4),
         ('Outline two policies that have accelerated the energy transition in a named country.', 'e.g. Germany: feed-in tariffs (Renewable Energy Sources Act, 2000); UK: contracts for difference auctions and carbon price floor; China: renewable targets and manufacturing subsidies; Norway: EV tax exemptions (about 90% of new car sales electric in 2024).', 3)],
  cases=[('Norway\'s electric vehicle policy', 'exemptions from purchase tax and VAT, toll and parking discounts made battery EVs about 89% of new car sales in 2024', 'policy driving the low-carbon transition', 'financial incentives made EVs cheaper than petrol cars, rapidly shifting consumer behaviour'),
         ('the Hornsdale Power Reserve, South Australia', 'a lithium-ion battery built in 2017 (expanded to 150 MW / 194 MWh in 2020) stabilises the grid and saved consumers tens of millions of dollars in its first years', 'energy storage enabling renewables', 'fast-responding storage balances fluctuations from a grid with a high share of wind and solar'),
         ('China\'s solar expansion', 'China installed over 200 GW of solar capacity in 2023, roughly half of all global additions', 'the scale of the energy transition', 'manufacturing scale and state policy drove down global costs and rapidly added low-carbon capacity')],
  evaluate=[('Improving energy efficiency is more important than expanding renewable energy.', ['cheapest emissions cuts', 'reduces demand and need for new capacity', 'benefits households'], ['rebound effects', 'efficiency alone cannot decarbonise remaining demand', 'renewables needed to replace fossil supply'], 'Both are essential and complementary; efficiency reduces the scale of the renewable build-out required.'),
            ('The transition to low-carbon energy will be fair to all countries and communities.', ['cheaper renewables expand energy access', 'new green jobs'], ['coal-dependent regions lose jobs', 'mineral extraction impacts (cobalt, lithium)', 'finance flows mainly to rich countries'], 'A just transition is possible but requires deliberate policies on finance, retraining and fair mineral supply chains.')],
  extended=[('Evaluate strategies for increasing energy efficiency and accelerating the transition to low-carbon energy. [9]', 'Efficiency standards, insulation, heat pumps, LEDs, EVs, feed-in tariffs, carbon pricing, storage, grid investment; examples (Norway EVs, Hornsdale, China solar, Germany); barriers (cost, rebound, vested interests); judgement.', 9, 'long')],
  res=[('Global weighted-average levelised cost of electricity for new projects (US$ per MWh, IRENA, approximate): 2010 - solar PV 460, onshore wind 110, fossil-fuel range 50-180; 2023 - solar PV 44, onshore wind 33.',
        [('Calculate the percentage fall in the cost of solar PV between 2010 and 2023.', '(460 − 44)/460 × 100 ≈ 90%.'),
         ('Suggest two reasons for the fall in cost.', 'Economies of scale in manufacturing (especially in China); technological improvements in panel efficiency; competitive auctions; lower financing costs; learning by doing.')])])


# =============================================================================================
# ch08 7.3 Solid waste
# =============================================================================================
S('ch08-st1', gens=['waste'],
  terms=[('municipal solid waste (MSW)', 'waste collected from households, offices, shops and institutions, such as food scraps, packaging, paper, plastics and textiles'),
         ('solid domestic waste (SDW)', 'the waste generated by households, including organic matter, paper, plastics, glass, metals and textiles'),
         ('e-waste', 'discarded electrical and electronic equipment, which contains valuable metals and hazardous substances such as lead and mercury'),
         ('biodegradable waste', 'waste that can be broken down by microorganisms, such as food and garden waste and paper'),
         ('waste stream', 'the flow of waste from its source through collection and treatment to final disposal')],
  facts=[('According to the World Bank, global municipal solid waste generation is about:', '2 billion tonnes per year, projected to reach about 3.4 billion t by 2050', ['20 million tonnes per year', '200 billion tonnes per year', '2 million tonnes per year'], 'What a Waste 2.0 (2018).'),
         ('What is the largest component of municipal waste globally?', 'Food and green (organic) waste - about 44%', ['Glass - about 40%', 'Metals - about 60%', 'Textiles - about 80%'], 'Paper is about 17% and plastics about 12%.'),
         ('About what percentage of e-waste was formally collected and recycled in 2022?', 'About 22%', ['About 2%', 'About 75%', 'About 95%'], 'Global E-waste Monitor 2024: 62 million t generated.'),
         ('High-income countries produce what share of the world\'s waste despite having about 16% of its population?', 'About a third', ['About 1%', 'About 5%', 'About 90%'], 'Per-capita generation rises with income.')],
  why=[('Explain why waste generation per person tends to increase with income.', 'Higher incomes bring greater consumption of packaged goods, electronics, clothing and convenience food, more disposable products and shorter product lifespans; urbanisation adds packaging and less home composting.'),
       ('Explain why the composition of waste differs between low- and high-income countries.', 'Low-income countries produce more organic (food) waste as a share; high-income countries produce more paper, plastics, metals and glass from packaged goods and more e-waste.'),
       ('Explain why e-waste is both a hazard and a resource.', 'It contains toxic lead, mercury, cadmium and flame retardants that pollute soil and water when dumped or burned (Agbogbloshie, Ghana); it also contains gold, copper, cobalt and rare earths - "urban mining" can recover them.')],
  contrast=[('biodegradable waste', 'non-biodegradable waste', 'Biodegradable waste (food, paper) is broken down by decomposers and can be composted but produces methane in landfill; non-biodegradable waste (most plastics, glass, metals) persists and must be reused, recycled or disposed of.')],
  misc=[('Most waste in low-income countries is plastic.', 'Organic waste makes up over half of waste in many low-income countries; plastics are a larger share in higher-income countries, though mismanaged plastic is a major problem in middle-income countries.'),
        ('E-waste is a small and harmless part of the waste stream.', 'E-waste is the fastest-growing waste stream (62 million t in 2022) and contains hazardous substances.')],
  apply=[('Suggest why the waste produced per person in Dubai is higher than in Nairobi.', 'Higher incomes and consumption, tourism and hospitality, more packaged imports, construction waste, convenience lifestyles; Nairobi has lower incomes and more reuse in the informal sector.', 3),
         ('Outline three sources of solid domestic waste in a typical household.', 'Food scraps and garden waste; packaging (plastic, cardboard, glass, cans); paper; clothing and textiles; electronic items; nappies.', 3)],
  cases=[('Agbogbloshie, Accra, Ghana', 'until its demolition in 2021, it was one of the world\'s largest informal e-waste sites, where workers burned cables to recover copper', 'the impacts of e-waste', 'unregulated recovery released lead, cadmium and dioxins, harming workers\' health and contaminating soil'),
         ('Kuwait\'s and the UAE\'s high waste generation', 'Gulf states generate over 1.5-2 kg of municipal waste per person per day, among the highest in the world', 'the link between income, consumption and waste', 'high incomes, subsidised consumption and limited recycling infrastructure lead to large waste volumes')],
  evaluate=[('Waste generation is a problem caused mainly by high-income countries.', ['a third of waste from 16% of people', 'export of waste and e-waste to lower-income countries'], ['fastest growth in waste is now in low- and middle-income countries', 'mismanaged waste mostly in middle-income countries', 'urbanisation everywhere increases waste'], 'High-income countries generate the most per person and have exported waste, but rapid growth elsewhere makes waste a global problem.')],
  extended=[('Explain how the type and quantity of solid domestic waste vary with economic development. [7]', 'Per-capita generation rises with income; composition shifts from organic to packaging, paper, plastics and e-waste; collection and treatment improve; examples (Nairobi, Dubai, Copenhagen, Tokyo).', 7, 'explain')],
  res=[('Global MSW composition (World Bank, What a Waste 2.0): food and green 44%; paper and cardboard 17%; plastic 12%; glass 5%; metal 4%; rubber and leather 2%; wood 2%; other 14%.',
        [('Calculate the mass of plastic waste in 2 billion tonnes of MSW.', '12% × 2 billion t = 240 million t.'),
         ('Suggest which components could be composted and which recycled, and calculate the combined percentage of recyclable materials (paper, plastic, glass, metal).', 'Compost food, green waste and paper; recycle paper/cardboard, plastics, glass and metals: 17 + 12 + 5 + 4 = 38%.')])])

S('ch08-st2',
  terms=[('landfill', 'the disposal of waste by burying it in the ground, ideally in an engineered site lined with clay or plastic to contain leachate and collect methane'),
         ('incineration', 'the burning of waste at high temperatures to reduce its volume, often recovering energy (waste-to-energy)'),
         ('composting', 'the aerobic decomposition of organic waste by microorganisms to produce humus-rich compost'),
         ('anaerobic digestion', 'the breakdown of organic waste by bacteria without oxygen, producing biogas (methane) and digestate'),
         ('leachate', 'liquid that drains from landfill, carrying dissolved and suspended pollutants that can contaminate groundwater'),
         ('open dump', 'an uncontrolled site where waste is deposited without engineering, monitoring or cover')],
  facts=[('Approximately what share of the world\'s waste is openly dumped or burned?', 'About a third or more', ['About 1%', 'About 5%', 'All of it'], 'World Bank: about 37% to landfill, 33% openly dumped, 19% recycled/composted, 11% incinerated.'),
         ('Which gas is produced when organic waste decomposes anaerobically in landfill?', 'Methane', ['Ozone', 'Chlorine', 'Sulfur hexafluoride'], 'Landfills are a major source of human methane emissions.'),
         ('Incineration can reduce the volume of waste by about:', '90%', ['10%', '30%', '0%'], 'The remaining ash must be disposed of safely.'),
         ('Copenhill (Amager Bakke) in Copenhagen is notable for:', 'a waste-to-energy plant with a ski slope on its roof', ['being the largest open dump in Europe', 'burning only coal', 'being a landfill under the sea'], 'It supplies electricity and district heating.')],
  why=[('Explain why landfill is still the most common disposal method in many countries.', 'It is cheap, simple, can accept mixed waste and needs little technology; land is available in many countries; alternatives require investment, separation and infrastructure.'),
       ('Explain the environmental impacts of poorly managed landfill.', 'Leachate contaminates groundwater and rivers; methane contributes to climate change and can cause explosions or fires; odour, vermin and disease; land take; plastics blown into the environment.'),
       ('Explain why composting is considered a sustainable waste option.', 'It diverts organic waste from landfill (avoiding methane), returns nutrients and organic matter to soil, reduces the need for fertiliser and is low-cost and possible at household or community scale.')],
  contrast=[('landfill', 'incineration', 'Landfill buries waste, is cheap and simple but uses land, produces methane and leachate; incineration burns waste, reducing volume by about 90% and generating energy, but is costly, emits CO₂ and pollutants (dioxins) and produces toxic ash.'),
            ('composting', 'anaerobic digestion', 'Composting decomposes organic waste aerobically to produce compost; anaerobic digestion decomposes it without oxygen in sealed tanks, producing biogas for energy as well as digestate fertiliser.')],
  misc=[('Incineration is a form of recycling.', 'Incineration with energy recovery recovers some energy, but materials are destroyed; it sits below recycling in the waste hierarchy.'),
        ('Modern landfills have no environmental impact.', 'Engineered landfills reduce impacts but still emit some methane, need long-term leachate management and occupy land.')],
  apply=[('Compare the advantages and disadvantages of incineration and landfill for a city with little available land.', 'Incineration: small land area, 90% volume reduction, energy recovery; but high cost, emissions and ash. Landfill: cheap but needs land the city lacks, methane, leachate. Incineration (with recycling) is likely more suitable, as in Singapore and Tokyo.', 4),
         ('Suggest how a landfill site could be managed to reduce its environmental impact.', 'Impermeable clay/plastic liners and leachate collection; methane capture for energy; daily soil cover; compaction; groundwater monitoring; restoration as parkland after closure.', 3)],
  cases=[('Semakau Landfill, Singapore', 'an offshore landfill built by enclosing sea between two islands receives incineration ash and non-incinerable waste; it is expected to be full by about 2035', 'waste disposal in a land-scarce city', 'incinerating most waste reduces volume, and an engineered offshore landfill with mangroves and monitoring limits impacts'),
         ('the Bantar Gebang landfill, Jakarta', 'one of the world\'s largest landfills receives about 7,000-8,000 t of waste a day and is reaching capacity', 'problems of landfill in rapidly growing cities', 'rapid growth in waste overwhelms disposal capacity, causing pollution and health risks for nearby residents and waste pickers'),
         ('Copenhill (Amager Bakke), Copenhagen', 'a waste-to-energy plant opened in 2017 burns about 440,000 t of waste a year, supplying electricity and heating to about 150,000 homes', 'incineration with energy recovery', 'burning residual waste provides energy and reduces landfill, though it still emits CO₂ and depends on a steady waste supply')],
  evaluate=[('Incineration is the best disposal option for residual waste in high-income cities.', ['reduces volume ~90%', 'generates energy and heat (Copenhill)', 'saves land'], ['emits CO₂ and air pollutants', 'locks in demand for waste, discouraging recycling', 'expensive'], 'Incineration can be appropriate for truly residual waste in land-scarce cities, but reduction, reuse and recycling should take priority.')],
  extended=[('Evaluate the sustainability of different waste disposal options. [9]', 'Landfill, incineration, composting, anaerobic digestion, recycling; environmental, economic, social criteria; examples (Singapore, Copenhagen, Bantar Gebang); waste hierarchy; judgement.', 9, 'long')],
  res=[('Waste treatment in selected countries (% of municipal waste, approximate): Germany - recycling/composting 67, incineration 32, landfill 1; Japan - recycling 20, incineration 78, landfill 2; Greece - recycling 20, incineration 1, landfill 79.',
        [('Compare the waste management of Germany and Greece.', 'Germany recycles/composts 67% and landfills only 1%; Greece landfills 79% and recycles 20% - Germany follows the waste hierarchy much more closely.'),
         ('Suggest why Japan relies so heavily on incineration.', 'Very limited land for landfill in a densely populated, mountainous country; high population density makes waste-to-energy efficient; cultural acceptance and strict sorting.')])])

S('ch08-st3',
  terms=[('circular economy', 'an economic model that designs out waste and pollution, keeps products and materials in use for as long as possible and regenerates natural systems'),
         ('linear economy', 'the "take-make-dispose" model in which resources are extracted, made into products, used and discarded'),
         ('waste hierarchy', 'the order of preference for waste management: reduce, reuse, recycle, recover (energy), dispose'),
         ('extended producer responsibility (EPR)', 'a policy that makes producers responsible for the collection, recycling or disposal of their products at the end of their life'),
         ('deposit-return scheme', 'a system in which consumers pay a small deposit on drinks containers, refunded when the containers are returned for recycling'),
         ('upcycling', 'reusing discarded materials to create products of higher quality or value')],
  facts=[('According to the Circularity Gap Report (2024), approximately what share of materials entering the global economy are cycled back?', 'About 7%', ['About 50%', 'About 25%', 'About 90%'], 'The global economy is still overwhelmingly linear.'),
         ('Which country\'s deposit-return scheme achieves about 97% return rates for drinks containers?', 'Norway', ['Brazil', 'India', 'Egypt'], 'The tax on bottles falls as return rates rise.'),
         ('Which is at the top of the waste hierarchy?', 'Reduce (prevention)', ['Recycle', 'Incinerate with energy recovery', 'Landfill'], 'Preventing waste avoids all downstream impacts.'),
         ('About what percentage of all plastic ever made has been recycled?', 'About 9%', ['About 50%', 'About 75%', 'About 99%'], 'Geyer et al. (2017): 9% recycled, 12% incinerated, 79% in landfill or the environment.')],
  why=[('Explain why the circular economy is more sustainable than the linear economy.', 'It reduces extraction of virgin resources, cuts waste and pollution, keeps materials\' value in use through repair, reuse, remanufacture and recycling, lowers energy use and emissions and can create local jobs.'),
       ('Explain why reducing waste is preferable to recycling it.', 'Recycling still uses energy, water and transport, materials degrade (downcycling), and not everything can be recycled; preventing waste avoids all these impacts and saves resources at source.'),
       ('Explain why plastic recycling rates are so low.', 'Many plastics are mixed, contaminated or multi-layered and cannot be recycled economically; virgin plastic from oil is cheap; recycling degrades quality; infrastructure for collection and sorting is lacking in many countries.')],
  contrast=[('the circular economy', 'the linear economy', 'The linear economy follows take-make-dispose, generating waste at the end of each product\'s life; the circular economy designs products to be reused, repaired and recycled so materials circulate and waste is minimised.'),
            ('recycling', 'reuse', 'Reuse uses a product again in the same form (refillable bottles), saving almost all the energy of making it; recycling breaks materials down to make new products, which requires energy and may reduce quality.')],
  misc=[('Recycling alone can solve the waste problem.', 'Recycling is limited by contamination, material degradation and economics; reducing consumption and designing for reuse are more effective.'),
        ('Biodegradable plastics break down harmlessly anywhere.', 'Many need industrial composting conditions (high temperature) and persist in the ocean or landfill; they can also contaminate recycling streams.')],
  apply=[('Using the waste hierarchy, suggest one action at each level for a school canteen.', 'Reduce: reusable plates and cutlery, portion control; reuse: refillable water stations; recycle: separate bins for cans, paper and plastic; recover: send food waste to anaerobic digestion; dispose: only residual waste to landfill.', 4),
         ('Outline how extended producer responsibility encourages a circular economy.', 'Producers pay for collection and recycling, so they have an incentive to design products that last, use less packaging and are easier to recycle (e.g. EU WEEE directive for electronics).', 3)],
  cases=[('Kamikatsu, Japan', 'the town aimed for zero waste by 2020, sorting waste into 45 categories and recycling about 80% of it', 'zero-waste community strategies', 'detailed source separation, reuse shops and community commitment greatly reduce landfill and incineration'),
         ('Norway\'s deposit-return scheme (Infinitum)', 'about 97% of plastic bottles and cans are returned, many being recycled into new bottles', 'policy tools in a circular economy', 'a refundable deposit gives consumers an incentive to return containers, enabling closed-loop recycling'),
         ('the Ellen MacArthur Foundation\'s Global Commitment', 'more than 1,000 organisations signed up to make plastic packaging reusable, recyclable or compostable, though many targets for 2025 were missed', 'business-led circular-economy initiatives', 'voluntary commitments raise ambition but progress depends on investment and regulation')],
  evaluate=[('The circular economy is achievable on a global scale.', ['successful examples (Kamikatsu, Norway DRS, Amsterdam)', 'business benefits from resource savings', 'policy support (EU Circular Economy Action Plan)'], ['global circularity only about 7%', 'consumption growing faster than recycling', 'some materials cannot circulate (energy, food)', 'requires redesign of whole supply chains'], 'Full circularity is unrealistic in the near term, but large increases are achievable with regulation, design changes and reduced consumption.'),
            ('Banning single-use plastics is the most effective way to reduce plastic waste.', ['immediate reduction (Kenya bag ban 2017)', 'clear signal to industry'], ['substitutes may have higher footprints (paper, cotton)', 'enforcement difficulties', 'deposit schemes and EPR tackle more of the waste stream'], 'Bans are effective for problem items, but must be part of a wider strategy including reuse systems and producer responsibility.')],
  extended=[('Evaluate the circular economy as a strategy for managing solid domestic waste. [9]', 'Principles (design out waste, keep materials in use, regenerate); tools (EPR, DRS, repair, sharing, product-as-a-service); examples (Kamikatsu, Norway, Amsterdam, EU policies); barriers (cost, consumer behaviour, global trade, 7% circularity); judgement.', 9, 'long')],
  res=[('Fate of all plastics ever produced to 2015 (Geyer et al., 2017): 8,300 million t produced; 6,300 million t became waste, of which 9% was recycled, 12% incinerated and 79% accumulated in landfill or the natural environment.',
        [('Calculate the mass of plastic waste that accumulated in landfill or the environment.', '79% × 6,300 million t ≈ 4,980 million t (about 5 billion t).'),
         ('Suggest two circular-economy measures that would reduce this.', 'Design for recyclability (single-polymer packaging); reuse and refill systems; extended producer responsibility; deposit-return schemes; reducing single-use plastic.')])])


# =============================================================================================
# ch09 8.1 Human populations
# =============================================================================================
S('ch09-st1', gens=['demography'],
  terms=[('crude birth rate (CBR)', 'the number of live births per 1,000 people in a population per year'),
         ('crude death rate (CDR)', 'the number of deaths per 1,000 people in a population per year'),
         ('total fertility rate (TFR)', 'the average number of children each woman has over her lifetime, given current age-specific fertility rates'),
         ('natural increase rate (NIR)', 'the rate of population growth from births minus deaths, excluding migration: (CBR − CDR) / 10, as a percentage'),
         ('doubling time (DT)', 'the time in years it takes for a population to double in size at a constant growth rate, approximately 70 ÷ NIR (%)'),
         ('replacement-level fertility', 'the TFR at which a population replaces itself from one generation to the next, about 2.1 in high-income countries')],
  facts=[('The world population reached 8 billion in:', 'November 2022', ['1999', '2011', '2040'], 'UN estimate (15 November 2022).'),
         ('Which country had the lowest total fertility rate in the world in 2023 (about 0.72)?', 'South Korea', ['Niger', 'India', 'Nigeria'], 'Far below the replacement level of 2.1.'),
         ('A country with an NIR of 2% will double its population in about:', '35 years', ['2 years', '70 years', '140 years'], 'Rule of 70: 70 ÷ 2 = 35.'),
         ('Which country overtook China as the most populous in 2023?', 'India', ['Indonesia', 'the USA', 'Nigeria'], 'India\'s population was about 1.43 billion.')],
  why=[('Explain why the CBR is not always the best measure of fertility.', 'CBR depends on the age structure: a population with many young adults has a high CBR even if each woman has few children; TFR measures fertility per woman independently of age structure.'),
       ('Explain why world population continued to grow rapidly in the 20th century.', 'Death rates fell sharply due to vaccines, antibiotics, clean water, sanitation and better nutrition (Green Revolution), while birth rates remained high in many countries for decades.'),
       ('Explain why a country with a TFR below 2.1 may still have a growing population.', 'Population momentum: a large number of young people entering reproductive age means births exceed deaths for decades; immigration and rising life expectancy also add to growth.')],
  contrast=[('crude birth rate', 'total fertility rate', 'CBR is births per 1,000 of the whole population per year and is affected by age structure; TFR is the average number of children per woman over her lifetime, a direct measure of fertility.'),
            ('natural increase', 'population growth rate', 'Natural increase is births minus deaths only; the population growth rate also includes net migration.')],
  misc=[('A high CBR always means rapid population growth.', 'Growth depends on CBR minus CDR (and migration); a high CBR with a high CDR may give slow growth.'),
        ('Doubling time stays the same as a population grows.', 'Doubling time changes as the growth rate changes; most countries\' growth rates are falling, so doubling times are increasing.')],
  apply=[('Suggest three factors that cause TFR to fall as a country develops.', 'Education and employment of women; access to contraception and family planning; falling infant mortality; urbanisation (children become costly); pensions reduce the need for children as old-age security.', 3),
         ('Outline why the world population growth rate has been falling since the late 1960s.', 'Falling fertility across Asia and Latin America through education, contraception, urbanisation and policies; growth peaked at about 2.1% a year in 1968 and was below 1% by 2020.', 2)],
  cases=[('South Korea\'s fertility decline', 'TFR fell from about 6 in 1960 to 0.72 in 2023 despite over US$200 billion spent on pro-natalist incentives since 2006', 'the factors behind very low fertility', 'high housing and education costs, long working hours and gender inequality discourage childbearing'),
         ('Niger', 'Niger has a TFR of about 6.7, the highest in the world, and a median age of about 15', 'high fertility in a low-income country', 'low female education, early marriage, limited contraception and agricultural livelihoods sustain high fertility')],
  evaluate=[('Population growth is the main cause of environmental problems.', ['more people increase resource demand (IPAT)', 'rapid growth in some regions pressures land and water'], ['consumption per person (affluence) and technology matter more; richest 10% emit about half of CO₂', 'population growth is slowing'], 'Population is a factor, but consumption and technology in high-income countries drive most global environmental impact.')],
  extended=[('Explain how demographic indicators can be used to compare population change in two named countries. [7]', 'CBR, CDR, NIR, TFR, DT, life expectancy, infant mortality; calculations; e.g. Niger vs Japan; explain differences by development, culture and policy.', 7, 'explain')],
  res=[('Demographic data (approximate): Niger - CBR 45, CDR 8, TFR 6.7; Japan - CBR 6, CDR 13, TFR 1.2; India - CBR 16, CDR 7, TFR 2.0.',
        [('Calculate the NIR for each country and the doubling time for Niger.', 'Niger 3.7%, Japan −0.7%, India 0.9%; Niger DT = 70/3.7 ≈ 19 years.'),
         ('Suggest two environmental implications of Niger\'s growth rate.', 'Increasing demand for farmland and fuelwood in a semi-arid region → desertification; pressure on scarce water; difficulty providing services; food insecurity.')])])

S('ch09-st2', gens=['dependency'],
  terms=[('demographic transition model (DTM)', 'a model describing how birth and death rates, and hence population growth, change as a country develops through five stages'),
         ('age-sex pyramid', 'a bar chart showing the percentage or number of males and females in each age group of a population'),
         ('dependency ratio', 'the ratio of the dependent population (aged 0-14 and 65+) to the working-age population (15-64), × 100'),
         ('ageing population', 'a population with an increasing proportion of older people, due to low fertility and rising life expectancy'),
         ('youthful population', 'a population with a high proportion of young people, giving a wide-based pyramid')],
  facts=[('In which stage of the DTM do death rates fall rapidly while birth rates remain high?', 'Stage 2', ['Stage 1', 'Stage 4', 'Stage 5'], 'Rapid population growth results.'),
         ('Which country is often given as an example of stage 5 of the DTM?', 'Japan', ['Niger', 'Afghanistan', 'Bangladesh'], 'Japan\'s population has declined since about 2010.'),
         ('A pyramid with a wide base and narrow top indicates:', 'a youthful, rapidly growing population', ['an ageing, declining population', 'a stable population', 'a population with high emigration of children'], 'Typical of stage 2 countries such as Niger.'),
         ('Which is a limitation of the DTM?', 'It is based on the experience of Western Europe and may not apply to all countries', ['It ignores birth rates', 'It only has one stage', 'It predicts exact population sizes'], 'Migration, culture and policy are not included.')],
  why=[('Explain why death rates fall before birth rates in stage 2 of the DTM.', 'Improvements in medicine, sanitation, clean water and food supply reduce mortality quickly, while birth rates depend on cultural norms, religion and economic need for children that change more slowly.'),
       ('Explain why age-sex pyramids are useful for planning.', 'They show the current and future numbers of children, workers and elderly, allowing governments to plan schools, jobs, housing, healthcare and pensions and to predict population momentum.'),
       ('Explain the environmental implications of an ageing population.', 'Slower or negative growth may reduce total resource demand, but older people may consume more energy for heating and healthcare; smaller workforces may limit investment; rural depopulation can lead to land abandonment and rewilding (e.g. Japan, Spain).')],
  contrast=[('stage 2 of the DTM', 'stage 4 of the DTM', 'Stage 2 has high birth rates and rapidly falling death rates, giving rapid growth and a youthful, wide-based pyramid; stage 4 has low birth and death rates, slow growth and a more column-shaped pyramid.'),
            ('a youthful population', 'an ageing population', 'A youthful population has a high proportion of under-15s (wide base), high youth dependency and future growth; an ageing population has a large proportion over 65, high old-age dependency and slowing or declining growth.')],
  misc=[('All countries pass through the DTM at the same speed.', 'Transitions have been much faster in some countries (South Korea, Iran) than in Europe, and some countries may stall at stage 3.'),
        ('A high dependency ratio means many people are unemployed.', 'The dependency ratio is based on age groups, not employment status.')],
  apply=[('Describe how the shape of an age-sex pyramid changes as a country moves from stage 2 to stage 4 of the DTM.', 'From a wide base and narrow top (triangular) to a narrower base, straighter sides and wider top (column/beehive) as birth rates fall and life expectancy rises.', 3),
         ('Suggest two consequences of a high youth dependency ratio for a government.', 'High spending on education, child healthcare and vaccination; need to create many jobs as young people reach working age; pressure on housing, food and water.', 2)],
  cases=[('Japan\'s ageing population', 'about 29% of the population is aged 65+ (2023), and the population has declined since 2010', 'stage 5 of the DTM and old-age dependency', 'very low fertility and the world\'s highest life expectancy create a top-heavy pyramid, labour shortages and rising care costs'),
         ('Nigeria\'s youthful population', 'about 42% of the population is under 15 and the population is projected to grow from about 220 million to over 375 million by 2050', 'stage 2-3 of the DTM', 'falling death rates with high fertility produce a wide-based pyramid and strong population momentum')],
  evaluate=[('The demographic transition model is a useful tool for predicting the future population of a country.', ['describes the general pattern in many countries', 'links population change to development'], ['based on European experience', 'ignores migration and policy (China\'s one-child policy)', 'timing and stage 5 uncertain', 'some countries stall'], 'The DTM is a useful descriptive model but a poor predictor; projections need demographic data and models that include migration, culture and policy.')],
  extended=[('Compare the population structures of two named countries at different stages of the DTM and discuss the implications for resource use. [9]', 'Pyramids, dependency ratios, growth rates (e.g. Niger vs Japan, Nigeria vs Germany); implications for food, water, energy demand and environmental impact; consumption differences; judgement.', 9, 'long')],
  res=[('Age structure (% of population): Uganda - 0-14: 45%, 15-64: 53%, 65+: 2%; Japan - 0-14: 12%, 15-64: 59%, 65+: 29%.',
        [('Calculate the dependency ratio of each country.', 'Uganda (45 + 2)/53 × 100 ≈ 89; Japan (12 + 29)/59 × 100 ≈ 69.'),
         ('Explain why both countries have high dependency ratios but face different challenges.', 'Uganda\'s dependants are mainly children (schools, jobs, future growth); Japan\'s are mainly elderly (pensions, healthcare, labour shortages, shrinking workforce).')])])

S('ch09-st3',
  terms=[('pro-natalist policy', 'a government policy to encourage higher birth rates, e.g. child payments, parental leave and childcare support'),
         ('anti-natalist policy', 'a government policy to reduce birth rates, e.g. family-planning programmes or limits on family size'),
         ('human carrying capacity', 'the maximum number of people that an area can support sustainably given its resources and technology'),
         ('Malthusian theory', 'the view (Thomas Malthus, 1798) that population grows geometrically while food supply grows arithmetically, leading to famine, disease and war'),
         ('Boserup theory', 'the view (Ester Boserup, 1965) that population pressure stimulates agricultural innovation and intensification, increasing food supply'),
         ('IPAT equation', 'Impact = Population × Affluence × Technology, a model of human environmental impact')],
  facts=[('China\'s one-child policy operated from 1980 until:', '2015 (replaced by a two-child policy, then three in 2021)', ['1985', '2000', 'It is still in force'], 'It contributed to a gender imbalance and rapid ageing.'),
         ('Which state in India achieved low fertility (TFR about 1.8) through education and healthcare rather than coercion?', 'Kerala', ['Bihar', 'Uttar Pradesh', 'Rajasthan'], 'High female literacy is key.'),
         ('Which country introduced the "Romanian decree 770" banning abortion and contraception in 1966 to raise births?', 'Romania', ['France', 'Sweden', 'China'], 'Births doubled briefly but at great human cost.'),
         ('According to Boserup, population growth leads to:', 'agricultural innovation that increases food production', ['inevitable famine', 'lower technology', 'no change in food supply'], 'She cited intensification such as terracing and irrigation.')],
  why=[('Explain why human carrying capacity is difficult to estimate.', 'Humans use technology, trade and changing diets to alter resource use; carrying capacity depends on consumption levels and technology, not just area; resources are imported from elsewhere; estimates range from 2 to over 1,000 billion.'),
       ('Explain how education of women reduces fertility.', 'Educated women marry later, have greater knowledge of and access to contraception, have more employment opportunities (raising the opportunity cost of children), have healthier children (lower infant mortality) and more decision-making power.'),
       ('Explain how the IPAT model helps to explain human environmental impact.', 'It shows impact depends on population, affluence (consumption per person) and technology (impact per unit consumed); a small population with high consumption may have a larger impact than a large population with low consumption.')],
  contrast=[('Malthusian theory', 'Boserup theory', 'Malthus argued food supply cannot keep up with population growth, leading to checks (famine, disease); Boserup argued population pressure drives innovation that increases food supply.'),
            ('pro-natalist policies', 'anti-natalist policies', 'Pro-natalist policies encourage more births (France\'s family allowances, Hungary\'s tax breaks); anti-natalist policies discourage births (China\'s one-child policy, family-planning campaigns).')],
  misc=[('Malthus was proved completely right by modern famines.', 'Global food production has outpaced population growth since 1798; modern famines are mainly caused by conflict, poverty and political failures, though Malthusian concerns resurface in debates about planetary limits.'),
        ('Coercive policies are the only effective way to reduce birth rates.', 'Kerala, Bangladesh and Iran reduced fertility rapidly mainly through education, healthcare and voluntary family planning.')],
  apply=[('Outline two pro-natalist policies used in a named country and assess their effectiveness.', 'e.g. France: generous child benefits, tax reductions for large families, subsidised childcare; TFR about 1.7-1.8, among the highest in Europe. Hungary: lifetime income-tax exemption for mothers of four or more; TFR rose from 1.23 (2011) to about 1.6 (2021).', 4),
         ('Use the IPAT equation to explain why a person in the USA has a greater environmental impact than a person in Bangladesh.', 'P is the same per person, but A (consumption) is far higher in the USA and T (energy and resource intensity of consumption) is high, so per-capita impact is much greater.', 3)],
  cases=[('China\'s one-child policy (1980-2015)', 'TFR fell from about 2.7 in 1979 to about 1.6, but the policy produced a sex ratio at birth of up to about 118 boys per 100 girls and rapid ageing', 'anti-natalist policies', 'coercive limits reduced births but caused serious social and demographic imbalances'),
         ('Kerala, India', 'with female literacy over 90%, Kerala reached replacement-level fertility in the late 1980s without coercion', 'the role of education and health in reducing fertility', 'investment in girls\' education and healthcare reduced infant mortality and fertility voluntarily'),
         ('France\'s family policies', 'universal family allowances, parental leave and subsidised childcare have kept France\'s TFR among the highest in Europe (about 1.7-1.8)', 'pro-natalist policies', 'support for working parents reduces the cost of children and helps sustain fertility')],
  evaluate=[('Reducing population growth is the most effective way to achieve sustainability.', ['fewer people reduce total demand (IPAT)', 'helps low-income countries meet needs'], ['consumption (A) and technology (T) dominate global impact', 'population growth already slowing; momentum makes rapid change impossible', 'ethical concerns about coercion'], 'Slowing population growth helps, but reducing consumption and improving technology in high-income countries are more effective levers for sustainability.'),
            ('Boserup\'s theory is a better description of the human-environment relationship than Malthus\'s.', ['food production has grown faster than population (Green Revolution)', 'innovation in water and energy'], ['innovation has caused environmental costs (soil degradation, emissions)', 'planetary boundaries are now exceeded', 'famines still occur'], 'Boserup better explains the past two centuries, but Malthusian limits reappear as environmental constraints, so both offer insights.')],
  extended=[('Evaluate the effectiveness of population policies in two named countries. [9]', 'e.g. China one-child policy, Kerala/India family planning, France or Hungary pro-natalist, South Korea incentives, Iran family planning; outcomes (TFR, social effects), ethics; judgement.', 9, 'long')],
  res=[('IPAT comparison (illustrative): Country X - population 300 million, consumption US$60,000 per person, technology 0.25 kg CO₂ per US$; Country Y - population 170 million, consumption US$2,500 per person, technology 0.25 kg CO₂ per US$.',
        [('Calculate the total CO₂ impact of each country in million tonnes.', 'X: 300 × 10⁶ × 60,000 × 0.25 kg = 4.5 × 10¹² kg = 4,500 Mt; Y: 170 × 10⁶ × 2,500 × 0.25 kg = 1.06 × 10¹¹ kg ≈ 106 Mt.'),
         ('Explain what the IPAT calculation shows about the relative importance of population and affluence.', 'Country X has under twice the population of Y but about 42 times the impact, because affluence (consumption per person) is 24 times higher - affluence dominates.')])])


# ---------------------------------------------------------------- ch10 urban systems and urban air pollution
S('ch10-st1', gens=['urban_growth'],
  terms=[('urbanisation', 'the increase in the proportion of a population living in urban areas'),
         ('urban system', 'a city viewed as an open system with inputs (energy, food, water, materials, people), storages (buildings, infrastructure) and outputs (waste, emissions, heat, products)'),
         ('urban heat island', 'the higher air and surface temperatures of a city compared with surrounding rural areas, caused by dark surfaces, buildings, waste heat and lack of vegetation'),
         ('megacity', 'an urban area with a population of over 10 million'),
         ('urban sprawl', 'the uncontrolled outward spread of low-density urban development into surrounding rural land'),
         ('urban metabolism', 'the flows of energy and materials into, through and out of a city, analysed like the metabolism of an organism')],
  facts=[('About what percentage of the world population lived in urban areas in 2018 (UN)?', '55%', ['25%', '40%', '80%'], 'Projected to reach about 68% by 2050.'),
         ('The world\'s largest urban agglomeration in 2018 (UN) was:', 'Tokyo', ['Lagos', 'London', 'São Paulo'], 'About 37 million people.'),
         ('Which is a typical output of an urban system?', 'sewage and solid waste', ['solar radiation', 'imported food', 'drinking water'], 'Food, water and solar radiation are inputs.'),
         ('Which feature contributes most to the urban heat island effect?', 'low-albedo surfaces such as asphalt and dark roofs', ['high vegetation cover', 'open water bodies', 'high wind speeds'], 'Dark surfaces absorb and re-radiate heat.')],
  why=[('Explain why cities are described as open systems.', 'They exchange both energy and matter with their surroundings: energy, food, water, materials and people flow in, while waste, emissions, heat, goods and people flow out.'),
       ('Explain why urbanisation is occurring fastest in low- and middle-income countries.', 'Rural-urban migration driven by push factors (lack of jobs, land pressure, drought, conflict) and pull factors (jobs, services, education), plus high natural increase in young urban populations.'),
       ('Explain why the urban heat island effect is strongest on calm, clear nights.', 'Buildings and roads release stored daytime heat slowly; with clear skies rural areas cool rapidly by radiation, while calm air means no wind mixes cooler rural air into the city, so the urban-rural difference is greatest.')],
  contrast=[('urbanisation', 'urban growth', 'Urbanisation is an increase in the proportion of people living in urban areas; urban growth is an increase in the absolute urban population or area, which can occur without urbanisation if rural populations grow equally.'),
            ('counter-urbanisation', 'suburbanisation', 'Counter-urbanisation is movement of people from urban areas to rural areas beyond the city; suburbanisation is movement from the inner city to the suburbs at the city\'s edge.')],
  misc=[('Cities have a lower environmental impact per person than rural areas in every respect.', 'Dense cities often have lower per-capita transport and heating energy, but higher consumption, imported resources and concentrated pollution; it depends on the city\'s wealth and design.'),
        ('Urbanisation only happens in low-income countries.', 'High-income countries urbanised earlier (UK over 80% urban); today\'s fastest rates are in Africa and Asia.')],
  apply=[('Draw and describe in words a systems diagram for a city, labelling two inputs, two storages and two outputs.', 'Box labelled "city" with arrows in: food, water, energy (fuels, electricity), raw materials, migrants; storages: buildings, infrastructure, people; arrows out: solid waste, sewage, air pollutants and CO₂, waste heat, manufactured goods.', 3),
         ('Outline two environmental consequences of urban sprawl.', 'Loss of farmland and habitats; increased car dependency, traffic, air pollution and CO₂; more impervious surfaces raise flood risk; fragmented ecosystems.', 2)],
  cases=[('Lagos, Nigeria', 'Lagos grew from about 1.4 million in 1970 to over 15 million by the early 2020s, with many residents in informal settlements such as Makoko', 'rapid urbanisation in a low-income country', 'growth outpaced infrastructure, leaving shortages of housing, water, sanitation and waste collection'),
         ('Hong Kong\'s urban metabolism', 'Hong Kong imports over 90% of its food and much of its water from mainland China', 'cities as open systems', 'a dense city depends on large inputs from a hinterland and exports waste and emissions'),
         ('Paris heat island in the 2003 heatwave', 'night temperatures in central Paris were up to about 8 °C higher than in the surrounding countryside and around 15,000 excess deaths occurred in France', 'the urban heat island', 'the heat island intensified the heatwave, especially at night, increasing mortality among the elderly')],
  evaluate=[('Urbanisation is beneficial for the environment.', ['higher density lowers per-capita land and transport energy', 'efficient service provision', 'lower fertility in cities'], ['concentrated pollution and waste', 'loss of farmland and habitats at the edges', 'high consumption and ecological footprint of urban residents', 'heat islands'], 'Urbanisation can reduce per-capita impact if cities are dense and well planned, but rapid unplanned growth and high consumption usually increase environmental pressure.'),
            ('Cities should be managed as closed systems to achieve sustainability.', ['reduces dependence on imports', 'circular use of water and materials', 'urban farming and local energy'], ['cities cannot be closed for energy or food at scale', 'trade gives efficiency', 'circular systems are costly'], 'Cities can become more circular, reducing inputs and outputs, but they will always remain open systems relying on a hinterland.')],
  extended=[('Explain how a named city can be modelled as a system, referring to inputs, outputs, storages and flows. [7]', 'Systems diagram in words; inputs (food, water, energy, people), storages (buildings, people, infrastructure), outputs (waste, emissions, heat, goods), transfers and transformations; named city data (e.g. Hong Kong, Lagos); feedback.', 7, 'explain')],
  res=[('UN data: urban share of population - China 1990: 26%, 2020: 61%; Nigeria 1990: 30%, 2020: 52%; Germany 1990: 73%, 2020: 77%.',
        [('Calculate the change in the urban share for each country.', 'China +35 percentage points; Nigeria +22; Germany +4.'),
         ('Suggest why Germany\'s urban share changed least.', 'Germany was already highly urbanised in 1990 (late stage of urbanisation), so there was little rural population left to migrate; counter-urbanisation also occurs.')])])

S('ch10-st2',
  terms=[('sustainable urban system', 'an urban system that meets the needs of its residents with minimal inputs and outputs, using renewable energy, efficient transport, green space and circular resource use'),
         ('green infrastructure', 'a network of natural and semi-natural features in a city, such as parks, green roofs, street trees and wetlands, that provide ecosystem services'),
         ('urban ecosystem', 'the living organisms of a city together with its built and natural environment and the interactions between them'),
         ('compact city', 'a high-density, mixed-use urban design that reduces travel distances and preserves surrounding land'),
         ('sustainable urban drainage system (SUDS)', 'drainage designs such as permeable paving, swales and retention ponds that slow and store runoff to reduce flooding')],
  facts=[('Which city is known for its bus rapid transit (BRT) system introduced in 1974?', 'Curitiba, Brazil', ['Dubai, UAE', 'Houston, USA', 'Lagos, Nigeria'], 'Curitiba pioneered BRT with dedicated lanes and tube stations.'),
         ('Which feature reduces surface runoff in a city?', 'permeable paving', ['tarmac car parks', 'concrete channels', 'storm drains'], 'Water infiltrates into the ground.'),
         ('Singapore\'s Gardens by the Bay and "City in Nature" vision are examples of:', 'green infrastructure', ['urban sprawl', 'brownfield pollution', 'counter-urbanisation'], 'Green space provides cooling and biodiversity.'),
         ('Building on previously developed land is called:', 'brownfield development', ['greenfield development', 'urban sprawl', 'suburbanisation'], 'It protects countryside from development.')],
  why=[('Explain how green roofs contribute to a sustainable urban system.', 'They intercept and store rainwater (reducing runoff and flooding), cool buildings by evapotranspiration and insulation (reducing energy use and the heat island), provide habitats and absorb some pollutants.'),
       ('Explain why compact cities can have lower per-capita carbon emissions.', 'Shorter distances make walking, cycling and public transport viable, reducing car use; apartments share walls and need less heating; infrastructure is shared by more people.'),
       ('Explain how urban green spaces support biodiversity.', 'Parks, street trees, gardens and wetlands provide habitats, food and nesting sites; green corridors connect fragments so species can disperse; varied planting increases niches.')],
  contrast=[('brownfield sites', 'greenfield sites', 'Brownfield sites are previously developed land (old factories) that may need decontamination but protect countryside; greenfield sites are undeveloped land, cheaper to build on but causing habitat and farmland loss.'),
            ('grey infrastructure', 'green infrastructure', 'Grey infrastructure is engineered concrete systems (pipes, drains, walls); green infrastructure uses vegetation and soils to provide services such as drainage, cooling and recreation.')],
  misc=[('Urban areas have no ecological value.', 'Cities support many species, e.g. peregrine falcons on buildings, urban foxes, pollinators in gardens; some cities have higher plant diversity than surrounding farmland.'),
        ('Planting trees in cities only has aesthetic value.', 'Trees provide shade and cooling, intercept rainfall, store carbon, trap particulates and improve mental health.')],
  apply=[('Suggest three strategies a city could use to reduce its ecological footprint.', 'Public transport, cycling infrastructure and low-traffic zones; renewable energy and building insulation; recycling and composting; local food; water recycling; compact mixed-use planning.', 3),
         ('Outline how SUDS could reduce flood risk in a city.', 'Permeable paving and swales increase infiltration, retention ponds and green roofs store water, slowing the flow to drains and rivers and reducing peak discharge.', 2)],
  cases=[('Curitiba, Brazil', 'Curitiba combined BRT, over 50 m² of green space per person and a "garbage that is not garbage" recycling programme', 'sustainable urban planning', 'integrated land-use, transport and waste policies reduced car use and improved the urban environment in a middle-income city'),
         ('Masdar City, UAE', 'planned as a zero-carbon city in 2006, its targets were scaled back and only a small part had been built by the 2020s', 'the challenges of new sustainable cities', 'high costs and the economic downturn limited a top-down eco-city design'),
         ('Copenhagen, Denmark', 'nearly half of all trips to work or education in the city are made by bicycle and the city aims for carbon neutrality', 'sustainable transport', 'investment in cycle superhighways and bridges made cycling the fastest way to travel')],
  evaluate=[('New "eco-cities" are the best way to achieve sustainable urban living.', ['designed from scratch with renewables and efficient transport', 'demonstrate technologies'], ['expensive and often unfinished (Masdar)', 'house few people compared with existing cities', 'retrofitting existing cities has greater impact'], 'Eco-cities can test ideas, but most urban populations live in existing cities, so retrofitting and better planning are more important.'),
            ('Green infrastructure is more effective than grey infrastructure in managing urban environments.', ['multiple benefits: cooling, biodiversity, flood control, health', 'lower maintenance'], ['less predictable capacity in extreme storms', 'needs space and time to mature', 'grey infrastructure may still be needed'], 'A combination works best: green infrastructure delivers many co-benefits while grey infrastructure provides reliable capacity in extreme events.')],
  extended=[('Discuss the extent to which a named city has achieved sustainable urban development. [9]', 'Named city (e.g. Curitiba, Copenhagen, Singapore); transport, energy, green space, waste and water; data; limitations (inequality, growth, informal settlements); judgement.', 9, 'long')],
  res=[('Surface runoff from a 1,000 m² area during a 20 mm storm: asphalt - 90% runoff; lawn - 25% runoff; green roof - 40% runoff.',
        [('Calculate the volume of runoff from each surface (1 mm on 1 m² = 1 litre).', 'Total rainfall = 20,000 L; asphalt 18,000 L; lawn 5,000 L; green roof 8,000 L.'),
         ('Explain the difference between asphalt and the green roof.', 'Asphalt is impermeable so almost all rain runs off immediately; a green roof\'s substrate and plants store water and lose it by evapotranspiration, reducing and delaying runoff.')])])

S('ch10-st3', gens=['pm25'],
  terms=[('primary pollutant', 'a pollutant emitted directly from a source, e.g. carbon monoxide, nitrogen oxides, sulfur dioxide, particulates, volatile organic compounds'),
         ('secondary pollutant', 'a pollutant formed in the atmosphere by chemical reactions between primary pollutants and other atmospheric components, e.g. tropospheric ozone, PANs'),
         ('photochemical smog', 'a mixture of primary and secondary pollutants, including tropospheric ozone, formed when sunlight drives reactions of nitrogen oxides and VOCs'),
         ('tropospheric ozone', 'ozone at ground level, a secondary pollutant that damages lungs, crops and plastics'),
         ('temperature inversion', 'a layer of warm air above cooler air near the ground that prevents vertical mixing and traps pollutants'),
         ('particulate matter (PM2.5)', 'airborne particles less than 2.5 micrometres in diameter that can penetrate deep into the lungs')],
  facts=[('Which is a secondary pollutant?', 'tropospheric ozone', ['carbon monoxide', 'nitrogen monoxide', 'sulfur dioxide'], 'Formed from NOx and VOCs in sunlight.'),
         ('The WHO 2021 annual guideline for PM2.5 is:', '5 µg/m³', ['15 µg/m³', '25 µg/m³', '50 µg/m³'], 'Reduced from 10 µg/m³ in 2005.'),
         ('Photochemical smog requires:', 'sunlight, nitrogen oxides and VOCs', ['rain and sulfur dioxide', 'cold, dark conditions', 'only carbon dioxide'], 'UV light splits NO₂ to start ozone formation.'),
         ('Which city\'s location in a mountain-ringed basin with frequent inversions makes it prone to smog?', 'Mexico City', ['Wellington', 'Amsterdam', 'Copenhagen'], 'It lies at about 2,240 m in the Valley of Mexico.'),
         ('About how many deaths a year does the WHO attribute to ambient (outdoor) air pollution?', 'about 4.2 million', ['about 42,000', 'about 420,000', 'about 42 million'], 'WHO estimate for 2019.')],
  why=[('Explain how tropospheric ozone forms in photochemical smog.', 'Vehicle exhausts emit NO which oxidises to NO₂; UV light splits NO₂ into NO and an oxygen atom, which combines with O₂ to form O₃; VOCs react with NO so it does not destroy the ozone, allowing ozone to accumulate.'),
       ('Explain why a temperature inversion makes air pollution worse.', 'Normally air cools with height and warm polluted air rises and disperses; in an inversion a warm layer caps cooler air near the ground, preventing convection, so pollutants are trapped and concentrations build up.'),
       ('Explain why ozone concentrations are often higher downwind of cities than in city centres.', 'Ozone takes hours to form photochemically as air moves; in city centres fresh NO emissions react with and remove ozone, so concentrations peak downwind in suburbs and rural areas.')],
  contrast=[('primary pollutants', 'secondary pollutants', 'Primary pollutants are emitted directly from sources (CO, NO, SO₂, soot); secondary pollutants form in the atmosphere from reactions of primaries (O₃, PANs, sulfuric acid).'),
            ('stratospheric ozone', 'tropospheric ozone', 'Stratospheric ozone absorbs harmful UV and protects life; tropospheric ozone is a ground-level secondary pollutant harmful to health and crops.')],
  misc=[('Photochemical smog is the same as the London smog of 1952.', 'The 1952 London smog was a sulfurous smog from coal burning (SO₂ and soot) in cold, foggy conditions; photochemical smog forms from vehicle NOx and VOCs in warm, sunny conditions.'),
        ('Ozone is always beneficial.', 'Ozone in the stratosphere is beneficial, but at ground level it is a toxic pollutant.')],
  apply=[('Describe the daily pattern of NO₂ and ozone concentrations in a sunny city.', 'NO₂ peaks in the morning rush hour from traffic; ozone rises through the late morning and peaks in mid-afternoon when sunlight is strongest, then falls in the evening as NO removes it and light fades.', 3),
         ('State two health effects of tropospheric ozone and particulates.', 'Ozone irritates airways and worsens asthma; PM2.5 causes respiratory and cardiovascular disease, lung cancer and premature death.', 2)],
  cases=[('Great Smog of London, 1952', 'a 5-day temperature inversion trapped coal smoke and SO₂, causing about 4,000 deaths at the time and an estimated 12,000 in total', 'sulfurous smog and inversions', 'cold, still conditions and coal burning trapped primary pollutants near the ground'),
         ('Los Angeles photochemical smog', 'Los Angeles\'s basin, sunshine and car dependency made it the classic site of photochemical smog from the 1940s', 'secondary pollutant formation', 'sunlight acting on vehicle NOx and VOCs trapped by inversions under the subtropical high produced ozone smog'),
         ('Delhi\'s winter smog', 'PM2.5 levels in Delhi often exceed 300 µg/m³ in November, with contributions from vehicles, industry, dust and crop-residue burning in Punjab and Haryana', 'multiple pollution sources', 'cold, calm winter conditions and inversions trap pollutants from many local and regional sources')],
  evaluate=[('Photochemical smog is mainly a problem caused by vehicles.', ['vehicles are the main source of NOx and VOCs in many cities', 'rush-hour peaks'], ['industry, power plants, solvents and biogenic VOCs contribute', 'climate and topography control severity', 'regional transport of ozone'], 'Vehicles are usually the largest single source, but topography, climate and other sources determine where smog becomes a serious problem.'),
            ('Air pollution is more of a threat to human health in low-income countries than in high-income countries.', ['highest PM2.5 levels in South Asia and Africa', 'indoor air pollution from cooking fuels', 'weaker regulation'], ['high-income cities still exceed WHO guidelines', 'ozone affects many wealthy regions', 'pollution is exported with manufacturing'], 'The burden is largest in low- and middle-income countries, but air pollution remains a significant health risk everywhere.')],
  extended=[('Explain the formation of photochemical smog and the conditions that make it more likely in a named city. [7]', 'Primary pollutants NOx and VOCs from vehicles; UV photolysis of NO₂; ozone and PANs formation; temperature inversions; basin topography and sunshine (e.g. Los Angeles, Mexico City, Santiago); effects.', 7, 'explain')],
  res=[('Hourly data on a sunny day in a city: 06:00 NO₂ 40, O₃ 20; 09:00 NO₂ 95, O₃ 30; 12:00 NO₂ 60, O₃ 85; 15:00 NO₂ 45, O₃ 120; 18:00 NO₂ 70, O₃ 70 (µg/m³).',
        [('Describe the change in ozone concentration through the day.', 'Ozone rises from 20 µg/m³ at 06:00 to a peak of 120 µg/m³ at 15:00 (six times higher), then falls to 70 µg/m³ by 18:00.'),
         ('Explain why the ozone peak occurs after the NO₂ peak.', 'NO₂ peaks with morning traffic; ozone is a secondary pollutant formed from NO₂ by photolysis, which needs strong sunlight and time, so it peaks in mid-afternoon.')])])

S('ch10-st4',
  terms=[('catalytic converter', 'a device in a vehicle exhaust that converts CO, NOx and unburnt hydrocarbons into CO₂, N₂ and water'),
         ('low-emission zone (LEZ)', 'an area where the most polluting vehicles are restricted or charged to enter'),
         ('congestion charge', 'a fee charged for driving into a city centre at busy times to reduce traffic'),
         ('flue-gas desulfurisation', 'removal of sulfur dioxide from power-station exhaust gases, usually by reaction with limestone'),
         ('electrostatic precipitator', 'a device that removes particulates from exhaust gases using an electrical charge')],
  facts=[('London\'s Ultra Low Emission Zone (ULEZ) was introduced in central London in:', '2019', ['1999', '2009', '2029'], 'It expanded to all London boroughs in 2023.'),
         ('A three-way catalytic converter reduces emissions of:', 'CO, NOx and hydrocarbons', ['CO₂ only', 'water vapour', 'only particulates'], 'It does not reduce CO₂.'),
         ('Which policy did Beijing use in its 2013-2017 clean air action plan?', 'replacing coal boilers with gas and electricity and closing polluting factories', ['banning all cars permanently', 'building more coal plants', 'removing all trees'], 'Beijing\'s annual PM2.5 fell by about 35% between 2013 and 2017.'),
         ('Mexico City\'s "Hoy No Circula" programme restricts:', 'car use on certain days according to the number plate', ['bicycle use', 'public transport', 'factory hours only'], 'Introduced in 1989.')],
  why=[('Explain why altering human activities is more sustainable than cleaning up pollution after release.', 'Preventing pollution (less driving, cleaner fuels) removes the source and associated costs; clean-up after release is costly, often incomplete and does not address the cause.'),
       ('Explain why driving restrictions can have unintended consequences.', 'People may buy a second (older, more polluting) car to avoid the restriction, as in Mexico City, or travel at different times; without alternatives such as public transport, restrictions may not reduce total emissions.'),
       ('Explain how a congestion charge reduces urban air pollution.', 'It raises the cost of driving into the centre, so fewer people drive and more use public transport, walk or cycle; less traffic and congestion reduce emissions of NOx, PM and CO; revenue can fund public transport.')],
  contrast=[('altering the human activity producing pollution', 'controlling the release of pollutants', 'Altering the activity reduces the source (fewer car journeys, switching from coal); controlling release uses technology at the point of emission (catalytic converters, scrubbers).'),
            ('a low-emission zone', 'a congestion charge', 'An LEZ charges or bans vehicles based on their emissions standard, targeting the most polluting vehicles; a congestion charge applies to all vehicles entering an area at busy times to reduce traffic volume.')],
  misc=[('Electric vehicles produce no air pollution.', 'EVs have no exhaust emissions but still produce particulates from tyres, brakes and roads, and emissions from electricity generation unless it is renewable.'),
        ('Catalytic converters solve urban air pollution.', 'They reduce CO, NOx and hydrocarbons per vehicle, but increasing traffic, cold starts and particulates mean pollution remains; they do not reduce CO₂.')],
  apply=[('Using the pollution management model, outline one strategy at each level to reduce photochemical smog.', 'Alter human activity: public transport, cycling, car-free days, clean energy; control release: catalytic converters, emission standards, LEZs; clean-up: planting trees, filters, health warnings and treatment of affected people.', 3),
         ('Suggest two reasons why air quality improved in Beijing between 2013 and 2020.', 'Coal-to-gas switching for heating, closure or relocation of heavy industry, stricter vehicle standards and restrictions, monitoring and enforcement, regional cooperation.', 2)],
  cases=[('London\'s ULEZ', 'roadside NO₂ in central London fell by about 46% compared with a no-ULEZ scenario by 2023 (Greater London Authority)', 'controlling release through low-emission zones', 'charging older polluting vehicles accelerated fleet renewal and reduced traffic emissions'),
         ('Beijing\'s Action Plan (2013-2017)', 'annual average PM2.5 fell from about 89 µg/m³ in 2013 to about 58 µg/m³ in 2017', 'top-down air quality management', 'replacing coal, closing factories and restricting vehicles reduced emissions, though levels remained above WHO guidelines'),
         ('Mexico City\'s air quality programmes', 'ozone and lead levels fell from the 1990s after unleaded fuel, catalytic converters, Hoy No Circula and the Metrobús BRT', 'combining strategies', 'multiple measures improved air quality, though ozone often still exceeds standards')],
  evaluate=[('Technological solutions are the most effective way to reduce urban air pollution.', ['catalytic converters and EVs cut emissions per vehicle', 'scrubbers and filters for industry'], ['rebound effects and more vehicles', 'non-exhaust particulates', 'behavioural change and planning reduce demand'], 'Technology is essential, but changes in transport behaviour and urban planning are needed to achieve lasting air-quality improvements.'),
            ('Low-emission zones are a fair way to improve urban air quality.', ['polluter pays', 'protects health of residents, especially children', 'revenue for public transport'], ['penalises low-income drivers with older vehicles', 'small businesses affected', 'may displace traffic'], 'LEZs are effective, but scrappage schemes and alternatives are needed to make them fair.')],
  extended=[('Evaluate strategies used to manage urban air pollution in a named city. [9]', 'Named city (London, Beijing, Delhi, Mexico City); strategies at each level of the pollution management model; data on effectiveness; social, economic and political issues; judgement.', 9, 'long')],
  res=[('Beijing annual mean PM2.5 (µg/m³): 2013: 89, 2015: 81, 2017: 58, 2020: 38, 2023: 32. WHO guideline 5 µg/m³; Chinese standard 35 µg/m³.',
        [('Calculate the percentage reduction in PM2.5 from 2013 to 2023.', '(89 − 32)/89 × 100 ≈ 64%.'),
         ('Evaluate the success of Beijing\'s air-quality policies.', 'Large reduction (64%), meeting roughly the national standard, but still over six times the WHO guideline; some reduction from industrial relocation to other regions; health benefits substantial.')])])


# ---------------------------------------------------------------- ch11 HL lenses: law, economics, ethics
S('ch11-st1',
  terms=[('environmental law', 'the body of national laws, regulations and international agreements that govern human interactions with the environment'),
         ('multilateral environmental agreement (MEA)', 'a legally binding agreement between three or more states on an environmental issue, e.g. the Montreal Protocol or CITES'),
         ('precautionary principle', 'the principle that where there are threats of serious or irreversible damage, lack of full scientific certainty should not be used to postpone cost-effective preventive measures (Rio Declaration, Principle 15)'),
         ('polluter pays principle', 'the principle that those who cause pollution should bear the costs of preventing or remedying it'),
         ('environmental impact assessment (EIA)', 'a legally required assessment of the likely environmental effects of a proposed development before a decision is made'),
         ('rights of nature', 'a legal approach that recognises ecosystems or natural entities as having legal rights, e.g. personhood for rivers')],
  facts=[('Which river was granted legal personhood in New Zealand in 2017?', 'the Whanganui River', ['the Waikato River', 'the Murray River', 'the Ganges'], 'Te Awa Tupua Act 2017, recognising Māori relationships with the river.'),
         ('Which country\'s constitution (2008) first recognised the rights of nature (Pachamama)?', 'Ecuador', ['Brazil', 'Canada', 'Australia'], 'Article 71 of Ecuador\'s constitution.'),
         ('The 2023 High Seas Treaty (BBNJ Agreement) aims to:', 'conserve marine biodiversity in areas beyond national jurisdiction', ['ban all fishing worldwide', 'regulate river pollution', 'phase out CFCs'], 'It enables marine protected areas on the high seas.'),
         ('In 2022 the UN General Assembly recognised:', 'the human right to a clean, healthy and sustainable environment', ['the end of the Kyoto Protocol', 'a global carbon tax', 'the rights of all rivers'], 'Resolution 76/300.'),
         ('Which agreement controls international trade in endangered species?', 'CITES', ['the Ramsar Convention', 'the Basel Convention', 'the Montreal Protocol'], 'Signed 1973, in force 1975.')],
  why=[('Explain why international environmental law is difficult to enforce.', 'States are sovereign and agreements depend on voluntary ratification; there is usually no international police or court with compulsory jurisdiction; states may withdraw (USA from Paris in 2017 and 2025); compliance relies on reporting, peer pressure and trade measures.'),
       ('Explain why the Montreal Protocol is regarded as a successful environmental agreement.', 'Universal ratification; clear science and identifiable substances; affordable substitutes; a Multilateral Fund to help developing countries; trade restrictions with non-parties; amendments strengthened it over time; ozone layer recovering.'),
       ('Explain how granting legal rights to nature could change environmental decision-making.', 'Ecosystems can be represented in court by guardians, so harm to the ecosystem itself becomes legally actionable rather than only harm to human property or health; it shifts law from anthropocentric towards ecocentric values.')],
  contrast=[('hard law', 'soft law', 'Hard law is legally binding with obligations and possible sanctions (Montreal Protocol, national statutes); soft law is non-binding guidance or declarations (Rio Declaration, Agenda 21) that influence behaviour without enforcement.'),
            ('national environmental law', 'international environmental law', 'National law is passed by a state\'s legislature and enforced by its courts and agencies; international law is agreed between states through treaties and relies on states to implement it domestically.')],
  misc=[('Signing an international agreement immediately makes it binding on a country.', 'A state usually must ratify the agreement (often requiring parliamentary approval) and the treaty must enter into force; signature alone signals intent.'),
        ('Environmental laws always protect the environment effectively.', 'Effectiveness depends on enforcement, monitoring, penalties and political will; many laws are poorly implemented.')],
  apply=[('Outline how the precautionary principle could be applied to a proposal for deep-sea mining.', 'Because impacts on poorly known deep-sea ecosystems may be serious and irreversible, mining should be delayed (moratorium) until research shows it can be done safely, with the burden of proof on the developer.', 3),
         ('State two features that make an international environmental agreement more likely to succeed.', 'Clear targets and timetables; financial and technical support for developing countries; monitoring and reporting; trade or other compliance mechanisms; broad participation.', 2)],
  cases=[('Te Awa Tupua (Whanganui River) Act 2017', 'New Zealand recognised the Whanganui River as a legal person, represented by two guardians, one from the Crown and one from the Whanganui iwi', 'rights of nature in law', 'law recognised an Indigenous ecocentric worldview and gave the river standing in its own right'),
         ('Urgenda Foundation v. State of the Netherlands', 'in 2019 the Dutch Supreme Court ordered the government to cut emissions by at least 25% from 1990 levels by 2020', 'climate litigation using national law and human rights', 'courts can require governments to strengthen climate action based on duties of care and human rights'),
         ('KlimaSeniorinnen v. Switzerland (2024)', 'the European Court of Human Rights ruled that Switzerland\'s inadequate climate policies violated the right to private and family life of older women', 'international human rights law and climate change', 'regional human rights courts can hold states accountable for climate inaction')],
  evaluate=[('International environmental agreements are more effective than national laws in tackling environmental problems.', ['global problems need global cooperation (ozone, climate)', 'set common standards'], ['enforcement weak; relies on national implementation', 'withdrawal possible', 'national laws enforced by courts and agencies'], 'International agreements are needed for transboundary issues, but they work only when implemented and enforced through national law.'),
            ('Granting legal personhood to rivers is an effective way to protect them.', ['ecosystems gain legal standing', 'reflects Indigenous values', 'guardians can sue polluters'], ['enforcement depends on resources and political will', 'Ganges and Yamuna rulings in India were stayed by the Supreme Court', 'may conflict with existing water rights'], 'Legal personhood can strengthen protection where backed by strong institutions, as in New Zealand, but alone it does not guarantee improvement.')],
  extended=[('Evaluate the role of law in addressing a named environmental issue at national and international scales. [9]', 'Named issue (climate, ozone, biodiversity, plastics); international agreements (Montreal, Paris, CITES); national laws and courts (Urgenda, Clean Air Acts); enforcement, compliance, equity; judgement.', 9, 'long')],
  res=[('Montreal Protocol: global consumption of ozone-depleting substances fell by about 99% between 1986 and 2010. Paris Agreement: NDCs submitted by 2023 were projected to lead to about 2.5-2.9 °C warming by 2100.',
        [('Compare the outcomes of the two agreements.', 'Montreal almost eliminated ODS and is close to its goal; Paris has not yet put the world on track for 1.5-2 °C, as NDCs are insufficient.'),
         ('Suggest two reasons for the difference in effectiveness.', 'ODS came from a few industries with available substitutes, while CO₂ comes from the whole economy; Montreal has binding phase-out schedules and trade restrictions, while Paris NDCs are nationally determined and not enforceable.')])])

S('ch11-st2', gens=['externality', 'esv'],
  terms=[('externality', 'a cost or benefit of an activity that affects third parties and is not reflected in the market price'),
         ('market failure', 'a situation where free markets fail to allocate resources efficiently, e.g. because of externalities or public goods'),
         ('tragedy of the commons', 'the overexploitation of a shared, open-access resource because individuals gain the full benefit of use while the costs are shared by all (Hardin, 1968)'),
         ('Pigouvian tax', 'a tax on an activity that generates negative externalities, set equal to the external cost to internalise it'),
         ('payment for ecosystem services (PES)', 'a scheme in which beneficiaries pay landowners to manage land to provide ecosystem services such as clean water or carbon storage'),
         ('total economic value (TEV)', 'the sum of use values (direct, indirect, option) and non-use values (existence, bequest) of a resource')],
  facts=[('Pollution from a factory affecting people downstream is an example of:', 'a negative externality', ['a positive externality', 'a public good', 'a subsidy'], 'The cost falls on third parties.'),
         ('Costa Rica\'s Pago por Servicios Ambientales programme (from 1997) is an example of:', 'payment for ecosystem services', ['a carbon tax', 'a cap-and-trade scheme', 'a fishing quota'], 'Landowners are paid to protect forest.'),
         ('Costanza et al. (2014) estimated global ecosystem services at about:', 'US$125 trillion per year', ['US$1.25 trillion per year', 'US$12.5 billion per year', 'US$1,250 trillion per year'], 'More than global GDP at the time.'),
         ('The Dasgupta Review (2021) on the economics of biodiversity was commissioned by:', 'the UK Treasury', ['the World Bank', 'the IPCC', 'the European Commission'], 'It argued that nature should be included in economic decision-making.'),
         ('Which is a non-use value of a coral reef?', 'existence value', ['tourism revenue', 'fish catch', 'coastal protection'], 'Valuing the reef simply because it exists.')],
  why=[('Explain why environmental problems are often described as market failures.', 'Prices do not include external costs such as pollution or loss of ecosystem services, so goods are overproduced and natural resources overused; many ecosystem services are public goods or open-access, with no market price.'),
       ('Explain how a carbon tax internalises an externality.', 'It adds the external cost of CO₂ emissions to the price of fossil fuels, so producers and consumers pay for the damage, reducing demand and encouraging low-carbon alternatives.'),
       ('Explain why placing a monetary value on ecosystem services is controversial.', 'It can make nature visible in cost-benefit decisions and justify protection, but values are uncertain, may undervalue non-use and cultural values, can treat nature as tradeable, and may ignore intrinsic value and justice.')],
  contrast=[('a carbon tax', 'a cap-and-trade scheme', 'A carbon tax sets a price per tonne of CO₂ and lets the quantity emitted vary; cap-and-trade sets a total cap on emissions and lets the permit price vary through trading.'),
            ('use values', 'non-use values', 'Use values come from direct or indirect use of a resource (timber, fishing, flood control); non-use values come from knowing it exists or can be passed on (existence and bequest values).')],
  misc=[('The tragedy of the commons is inevitable for all shared resources.', 'Elinor Ostrom showed that many communities manage common-pool resources sustainably through local rules, monitoring and sanctions (e.g. Swiss alpine pastures, Maine lobster fisheries).'),
        ('If something has no market price it has no economic value.', 'Ecosystem services such as pollination and climate regulation have large economic value even though they are not traded.')],
  apply=[('Suggest how a government could correct the market failure caused by plastic pollution.', 'Tax or levy on single-use plastics (e.g. bag charges), deposit-return schemes, extended producer responsibility, bans, subsidies for alternatives.', 3),
         ('Outline two methods used to value ecosystem services.', 'Market prices (timber, fish); replacement or avoided-cost methods (cost of artificial flood defences avoided by wetlands); travel-cost method (recreation); contingent valuation (willingness to pay surveys).', 2)],
  cases=[('EU Emissions Trading System', 'launched in 2005, it covers power, industry and aviation; emissions from covered sectors fell by about 47% from 2005 to 2023', 'cap-and-trade', 'a falling cap and a rising carbon price (over €80 per tonne in 2023) encouraged switching from coal'),
         ('Costa Rica\'s PES programme', 'forest cover rose from about 21% in the late 1980s to over 50% by the 2010s, supported by payments funded partly by a fuel tax', 'payment for ecosystem services', 'paying landowners for forest services helped reverse deforestation, alongside other policies'),
         ('New York City\'s Catskills watershed', 'in the 1990s the city invested about US$1.5 billion in watershed protection instead of a filtration plant estimated at US$6-8 billion', 'valuing ecosystem services', 'protecting natural capital provided clean water more cheaply than built infrastructure')],
  evaluate=[('Putting a price on nature is the best way to protect it.', ['makes nature visible in decisions', 'PES and carbon pricing change behaviour', 'Catskills shows cost savings'], ['values uncertain and incomplete', 'may commodify nature and crowd out intrinsic motives', 'some losses are irreversible and priceless', 'equity issues'], 'Economic valuation is a powerful tool but should complement, not replace, legal protection and ethical values.'),
            ('Carbon taxes are more effective than cap-and-trade schemes in reducing emissions.', ['price certainty', 'simple to administer', 'revenue can be recycled (British Columbia, Sweden)'], ['quantity of emissions uncertain', 'politically unpopular (gilets jaunes)', 'cap-and-trade guarantees an emissions cap'], 'Both can work; effectiveness depends on the price level, coverage and political design.')],
  extended=[('Discuss the use of economic tools to address a named environmental issue. [9]', 'Externalities and market failure; carbon tax, cap-and-trade, PES, subsidies, valuation; named examples (EU ETS, Costa Rica, Sweden carbon tax); strengths and limitations; equity; judgement.', 9, 'long')],
  res=[('A wetland near a city provides: flood protection (avoided damage) US$2.4 million/yr, water purification US$1.1 million/yr, fisheries US$0.6 million/yr, recreation US$0.4 million/yr. Draining it for farmland would earn US$1.8 million/yr.',
        [('Calculate the total annual value of the wetland\'s ecosystem services.', '2.4 + 1.1 + 0.6 + 0.4 = US$4.5 million per year.'),
         ('Use the data to discuss whether the wetland should be drained.', 'Ecosystem services (US$4.5 million) are 2.5 times the farmland income (US$1.8 million); draining would cause a net loss of US$2.7 million/yr, though farmers gain privately while costs fall on others, showing market failure; non-use values add more.')])])

S('ch11-st3',
  terms=[('environmental ethics', 'the study of moral principles governing the relationship between humans and the environment'),
         ('environmental justice', 'the fair distribution of environmental benefits and burdens and meaningful participation of all people in environmental decisions'),
         ('intrinsic value', 'the value something has in itself, independent of its usefulness to humans'),
         ('instrumental value', 'the value something has as a means to an end, especially its usefulness to humans'),
         ('intergenerational equity', 'fairness between present and future generations in the use of resources and environmental quality'),
         ('climate justice', 'an approach that recognises that those least responsible for climate change often suffer most from it, and that responses should be fair')],
  facts=[('Aldo Leopold\'s "land ethic" (1949) is an example of:', 'an ecocentric ethic', ['a technocentric ethic', 'a purely economic approach', 'utilitarian anthropocentrism'], 'From "A Sand County Almanac".'),
         ('The Warren County, North Carolina protests of 1982 against a toxic waste landfill are associated with the start of:', 'the environmental justice movement', ['the Montreal Protocol', 'the Chipko movement', 'the Green Belt Movement'], 'The site was in a mainly African American community.'),
         ('Which ethical framework judges actions by their consequences for overall well-being?', 'utilitarianism', ['deontology', 'virtue ethics', 'biocentrism'], 'The greatest good for the greatest number.'),
         ('The UNFCCC principle that recognises different responsibilities of countries is:', 'common but differentiated responsibilities', ['polluter pays', 'the precautionary principle', 'free prior informed consent'], 'Developed countries should take the lead.'),
         ('The Loss and Damage fund agreed at COP27 (2022) aims to:', 'help vulnerable countries cope with unavoidable climate impacts', ['fund oil exploration', 'buy carbon credits for rich countries', 'pay for nuclear weapons disarmament'], 'An outcome of climate justice campaigns.')],
  why=[('Explain why climate change is considered an issue of environmental justice.', 'High-income countries and wealthy people are responsible for most historical emissions, while low-income countries, small island states and poor communities face the greatest impacts (sea-level rise, drought, floods) with least capacity to adapt.'),
       ('Explain how different ethical frameworks could lead to different decisions about building a dam.', 'Utilitarian: build if total benefits (energy, water) outweigh costs; deontological: do not build if it violates rights of displaced people; ecocentric: oppose because it destroys river ecosystems with intrinsic value; virtue ethics: ask what a responsible, caring person would do.'),
       ('Explain why intergenerational equity is important for sustainability.', 'Sustainability means meeting present needs without compromising future generations; depleting natural capital, emitting long-lived greenhouse gases and driving extinctions impose costs on people who cannot take part in today\'s decisions.')],
  contrast=[('intrinsic value', 'instrumental value', 'Intrinsic value is the worth of something in itself regardless of use; instrumental value is worth as a means to human ends, such as timber or recreation.'),
            ('distributive justice', 'procedural justice', 'Distributive justice concerns the fair sharing of environmental benefits and harms; procedural justice concerns fair, inclusive and transparent decision-making processes.')],
  misc=[('Environmental ethics only concerns animals and plants.', 'It also concerns human rights, fairness between groups and generations, and how decisions are made.'),
        ('Environmental burdens are distributed randomly.', 'Studies show polluting facilities are disproportionately located near low-income and minority communities (e.g. "Cancer Alley", Louisiana).')],
  apply=[('Outline the ethical issues raised by a city locating a waste incinerator in a low-income neighbourhood.', 'Distributive injustice: residents bear the health risks while the whole city benefits; procedural injustice if residents were not consulted; utilitarian benefits versus rights of residents; intergenerational effects of pollution.', 3),
         ('Distinguish between anthropocentric and biocentric ethics using an example.', 'Anthropocentric: protect a forest because it provides water and timber for people; biocentric: protect it because all living organisms in it have intrinsic value.', 2)],
  cases=[('"Cancer Alley", Louisiana, USA', 'an 85-mile stretch of the Mississippi River with over 150 petrochemical plants, alongside mostly Black communities with elevated cancer risks', 'environmental justice', 'pollution burdens fall disproportionately on marginalised communities with limited political power'),
         ('Flint water crisis, Michigan (2014-2019)', 'a switch of water source to save money exposed a majority Black city to lead-contaminated water', 'distributive and procedural injustice', 'cost-cutting decisions made without community input harmed a low-income population'),
         ('Tuvalu and sea-level rise', 'Tuvalu, with a highest point of about 4.6 m, signed the Falepili Union with Australia in 2023 offering migration pathways to its citizens', 'climate justice', 'a nation with negligible emissions faces loss of territory due to emissions from others')],
  evaluate=[('Environmental justice should be the main consideration in environmental decision-making.', ['protects vulnerable groups', 'fair processes increase legitimacy and compliance', 'human rights obligations'], ['ecocentric values may be overlooked', 'trade-offs with economic efficiency', 'difficult to define fairness'], 'Justice is essential to legitimate and lasting decisions, but it should be balanced with ecological integrity and other values.'),
            ('Ecocentric ethics provide a better basis for environmental management than anthropocentric ethics.', ['recognises intrinsic value', 'protects species without obvious use', 'precautionary'], ['difficult to apply in practice', 'may conflict with human needs and poverty reduction', 'anthropocentric arguments (ecosystem services) persuade decision-makers'], 'Ecocentric ethics strengthen protection, but anthropocentric arguments are often needed to gain support; combining both is most effective.')],
  extended=[('Discuss how different ethical perspectives might be applied to a named environmental issue. [9]', 'Utilitarianism, deontology, virtue ethics; anthropocentric, biocentric, ecocentric; environmental and climate justice; named issue (Cancer Alley, climate change, dam); conflicts between perspectives; judgement.', 9, 'long')],
  res=[('Cumulative CO₂ emissions 1850-2021 (approximate share of world total): USA 20%, China 11%, Russia 7%, Germany 4%, UK 3%, all of Africa about 3%. Africa has about 18% of the world population.',
        [('Compare the share of cumulative emissions with population for Africa.', 'Africa has about 18% of the population but only about 3% of cumulative emissions, about one-sixth of its population share.'),
         ('Use the data to explain the principle of common but differentiated responsibilities.', 'Countries such as the USA and UK contributed far more historically, so they bear greater responsibility to cut emissions and finance adaptation in low-emitting regions such as Africa.')])])

S('ch11-st4',
  terms=[('HL lens', 'one of the three perspectives (environmental law, environmental economics, environmental ethics) used in HL ESS to analyse environmental issues'),
         ('stakeholder', 'a person or group with an interest in, or affected by, an environmental issue or decision'),
         ('cost-benefit analysis (CBA)', 'a method that compares the monetised costs and benefits of a project or policy over time'),
         ('free, prior and informed consent (FPIC)', 'the right of Indigenous peoples to give or withhold consent to projects affecting their lands, recognised in UNDRIP (2007)'),
         ('discount rate', 'the rate used in economic analysis to convert future costs and benefits into present values')],
  facts=[('The UN Declaration on the Rights of Indigenous Peoples (UNDRIP) was adopted in:', '2007', ['1972', '1992', '2015'], 'It recognises free, prior and informed consent.'),
         ('A higher discount rate in cost-benefit analysis tends to:', 'reduce the present value of long-term environmental benefits', ['increase the value of future benefits', 'have no effect on future values', 'remove all costs'], 'This is central to the Stern Review debate.'),
         ('The Stern Review (2006) concluded that the cost of strong climate action was about:', '1% of global GDP per year', ['50% of global GDP', '0.001% of global GDP', '20% of global GDP per year'], 'Inaction could cost 5-20% of GDP.'),
         ('Which lens would focus on whether a project complies with an EIA regulation?', 'environmental law', ['environmental ethics', 'environmental economics', 'none of them'], 'Legal compliance.')],
  why=[('Explain why using all three HL lenses gives a fuller understanding of an environmental issue.', 'Law shows what is required and enforceable; economics shows costs, benefits and incentives; ethics shows what is fair and right; an issue may be legal and profitable yet unjust, so combining lenses reveals conflicts and better solutions.'),
       ('Explain why the choice of discount rate is an ethical as well as an economic decision.', 'A high discount rate values future generations\' well-being less than present well-being, reducing the case for climate action; choosing a rate reflects judgements about intergenerational equity.'),
       ('Explain how the three lenses might conflict in the case of an Amazon mining project.', 'Law may allow the mine if licensed; economics may show large profits and jobs; ethics highlights Indigenous rights, FPIC, intrinsic value of forest and climate justice - so a legal, profitable project may be ethically unacceptable.')],
  contrast=[('the economic lens', 'the ethical lens', 'The economic lens analyses costs, benefits, incentives and efficiency, often in monetary terms; the ethical lens asks what is right, fair and just, including values that cannot be monetised.'),
            ('the legal lens', 'the ethical lens', 'The legal lens asks what laws and agreements require or allow and how they are enforced; the ethical lens asks what ought to be done, which may go beyond or conflict with current law.')],
  misc=[('If an activity is legal it must be ethical.', 'Many legal activities (e.g. permitted pollution in Cancer Alley) are considered unjust; laws often lag behind ethical understanding.'),
        ('Cost-benefit analysis gives an objective answer.', 'CBA depends on which costs and benefits are included, how they are valued and the discount rate chosen, all of which involve value judgements.')],
  apply=[('Apply the economic lens to the problem of overfishing.', 'Open-access fisheries are a tragedy of the commons; fishers do not pay for depletion (externality); subsidies encourage overcapacity; solutions include individual transferable quotas, removing harmful subsidies and valuing marine ecosystem services.', 3),
         ('Identify two stakeholders in a proposed coastal resort development and state one interest of each.', 'Developers (profit); local fishers (access to fishing grounds); tourists (recreation); conservation NGOs (protect mangroves/reefs); local government (tax revenue, jobs); Indigenous or local communities (land rights).', 2)],
  cases=[('Belo Monte Dam, Brazil', 'the dam on the Xingu River (completed 2019) displaced about 20,000 people and was challenged by Indigenous groups and in court for lack of proper consultation', 'combining legal, economic and ethical lenses', 'an economically justified energy project raised legal challenges and ethical concerns about FPIC and justice'),
         ('Pacific deep-sea mining', 'the International Seabed Authority has debated mining regulations, while more than 25 countries had called for a moratorium or precautionary pause by 2024', 'precaution, economics and ethics', 'demand for battery metals conflicts with precaution, unknown ecosystem value and intergenerational equity'),
         ('Standing Rock and the Dakota Access Pipeline', 'from 2016 the Standing Rock Sioux opposed the pipeline crossing near their water supply and sacred sites; a court later ordered a new environmental review', 'legal and ethical lenses', 'Indigenous rights and water justice were set against energy economics and permitting law')],
  evaluate=[('The economic lens is the most important when making decisions about environmental issues.', ['decision-makers respond to costs and benefits', 'incentives change behaviour', 'CBA makes trade-offs explicit'], ['ignores intrinsic value and justice', 'discount rates undervalue future generations', 'laws set non-negotiable limits'], 'Economics is influential, but sound decisions require legal compliance and ethical justification, so no single lens should dominate.'),
            ('Applying the HL lenses always leads to better environmental decisions.', ['reveals hidden costs and injustices', 'encourages inclusive decision-making', 'identifies legal duties'], ['lenses can conflict without a clear resolution', 'power imbalances shape which lens wins', 'time and data demands'], 'The lenses improve analysis and transparency, but better decisions also depend on political will and fair processes.')],
  extended=[('Using a named case study, evaluate how environmental law, economics and ethics can be used to resolve an environmental conflict. [9]', 'Named case (Belo Monte, Standing Rock, deep-sea mining, Whanganui); each lens applied with evidence; stakeholders; conflicts between lenses; outcome; judgement.', 9, 'long')],
  res=[('Cost-benefit analysis of a coastal mangrove restoration project (present values over 30 years): restoration cost US$12 million; avoided storm damage US$18 million; fisheries benefits US$6 million; carbon storage US$4 million. Using a higher discount rate halves the present value of all benefits.',
        [('Calculate the net present value at both discount rates.', 'Lower rate: 18 + 6 + 4 − 12 = +US$16 million; higher rate: 14 − 12 = +US$2 million.'),
         ('Discuss what the result shows about the role of value judgements in CBA.', 'The project is worthwhile in both cases, but the benefit is much smaller at a high discount rate; choosing the rate reflects how much we value future generations; non-market values (biodiversity, culture) are not included.')])])


# ---------------------------------------------------------------- ch12 internal assessment skills
S('ch12-st1',
  terms=[('research question (RQ)', 'a focused, answerable question that defines the purpose and scope of an investigation, naming the variables and the context'),
         ('independent variable', 'the variable that the investigator changes or selects to test its effect'),
         ('dependent variable', 'the variable that is measured in response to changes in the independent variable'),
         ('controlled variable', 'a variable kept constant or monitored so that it does not affect the results'),
         ('hypothesis', 'a testable prediction of the relationship between variables, based on scientific reasoning'),
         ('null hypothesis', 'a statement that there is no significant difference or relationship between variables, used in statistical testing')],
  facts=[('Which is the best research question for an ESS IA?', 'What is the effect of distance from a footpath (0-10 m) on the species richness of ground flora in Epping Forest?', ['Is trampling bad?', 'How do forests work?', 'What do people think about the environment?'], 'It names the IV, DV, range and context.'),
         ('In an investigation of the effect of river distance from a sewage outfall on dissolved oxygen, the dependent variable is:', 'dissolved oxygen concentration', ['distance from the outfall', 'water temperature', 'the time of sampling'], 'It is the measured response.'),
         ('A suitable null hypothesis for a study comparing litter on two beaches is:', 'There is no significant difference in the mass of litter per m² between the two beaches', ['Beach A has more litter', 'Litter is harmful', 'Tourists drop litter'], 'H₀ predicts no difference.'),
         ('The ESS internal assessment (first exams 2026) is worth what percentage of the SL final grade?', '25%', ['10%', '50%', '75%'], 'At HL it is 20%.'),
         ('A research question in ESS should ideally link an environmental issue to:', 'a local context and a wider environmental or social issue', ['only global data from the internet', 'a purely theoretical question', 'no particular location'], 'The IA should connect local data to a wider issue.')],
  why=[('Explain why a research question should be focused rather than broad.', 'A focused question defines specific variables, range and context, so appropriate data can be collected within time and resources and a clear, valid conclusion can be reached.'),
       ('Explain why a hypothesis should be based on scientific reasoning.', 'It shows understanding of the underlying ecology or social process, makes the prediction testable, and allows the results to be explained or the reasoning to be revised if the hypothesis is rejected.'),
       ('Explain why an ESS research question may combine environmental and social data.', 'ESS studies the interaction of environmental and human systems; issues such as waste or conservation involve human attitudes and behaviour, so surveys and environmental measurements together give a fuller picture.')],
  contrast=[('a hypothesis', 'a null hypothesis', 'A hypothesis predicts a specific relationship or difference based on reasoning; a null hypothesis states that there is no significant difference or relationship and is what the statistical test evaluates.'),
            ('independent variable', 'dependent variable', 'The independent variable is selected or changed by the investigator (e.g. distance from a road); the dependent variable is measured in response (e.g. lichen diversity).')],
  misc=[('A good research question can be answered with a simple yes or no.', 'Good RQs ask about the effect, relationship or extent ("What is the effect of…", "To what extent…") so that quantitative analysis is possible.'),
        ('Controlled variables do not need to be mentioned if they cannot be controlled in the field.', 'In fieldwork uncontrollable variables should be monitored and recorded (e.g. weather, time of day) and their possible effect discussed.')],
  apply=[('Write a focused research question and a hypothesis for an investigation of air pollution using lichens.', 'RQ: What is the effect of distance from a main road (0-500 m) on lichen species diversity on oak trunks in a named park? Hypothesis: lichen diversity will increase with distance from the road because NOx and SO₂ concentrations decrease and many lichens are sensitive to these pollutants.', 3),
         ('Identify the independent, dependent and two controlled variables in a study of the effect of grazing on grassland species richness.', 'IV: grazed vs ungrazed (or grazing intensity); DV: number of species per quadrat; controlled: quadrat size, slope/aspect, soil type, season/date of sampling.', 3)],
  cases=[('Lichen survey in a city park', 'a student linked lichen diversity on trees at increasing distances from a ring road to local NO₂ monitoring data', 'a research question with an environmental and local context', 'the RQ named the IV (distance), DV (lichen diversity), range and location, connecting local data to urban air pollution'),
         ('Survey of attitudes to a plastic-bag charge', 'a student surveyed shoppers before and after a supermarket introduced a bag charge', 'a social research question in ESS', 'a focused RQ on the effect of a policy on behaviour linked local data to the wider issue of plastic waste')],
  evaluate=[('Fieldwork-based investigations are more valuable than secondary-data investigations for the ESS IA.', ['first-hand data and understanding of methods', 'local context', 'control over method'], ['limited time and sample size', 'secondary data can cover longer periods and larger areas', 'safety and access issues'], 'Fieldwork offers depth and control, but secondary data can give scale; combining primary and secondary data is often strongest.'),
            ('A narrowly focused research question limits the value of an investigation.', ['may ignore wider context', 'results less generalisable'], ['allows clear variables and valid conclusions', 'feasible in the time available', 'can still be linked to wider issues in the discussion'], 'Focus improves validity; the wider significance is shown in the application to the environmental issue rather than by broadening the RQ.')],
  extended=[('Design an investigation into the effect of a named human activity on a local ecosystem, including a research question, hypothesis and variables. [7]', 'Focused RQ (IV, DV, range, context); hypothesis with reasoning; null hypothesis; IV, DV, controlled variables; sampling strategy outline; link to wider issue.', 7, 'explain')],
  res=[('Student RQ draft 1: "Does pollution affect rivers?" Draft 2: "What is the effect of distance downstream (0-2 km) from a sewage treatment works on the BMWP score of the River Wandle?"',
        [('Explain why draft 2 is better.', 'It names the IV (distance), its range, the DV (BMWP score) and the specific location, making it focused, measurable and testable.'),
         ('Suggest one controlled variable for draft 2.', 'Sampling method and time per kick sample; flow velocity/riffle habitats; date and weather; depth of sampling.')])])

S('ch12-st2', gens=['mean_sd_t'],
  terms=[('random sampling', 'a sampling method in which every individual or location has an equal chance of being selected, e.g. using random number coordinates'),
         ('systematic sampling', 'sampling at regular intervals, e.g. every 5 m along a transect'),
         ('stratified sampling', 'dividing a study area into distinct zones (strata) and sampling each in proportion to its area or importance'),
         ('pilot study', 'a small preliminary trial of a method to test its suitability and refine it before the main investigation'),
         ('risk assessment', 'identification of hazards in an investigation, the likelihood and severity of harm, and the precautions to minimise risk'),
         ('informed consent', 'voluntary agreement by a participant to take part in research after being told its purpose, how data will be used and their right to withdraw')],
  facts=[('Which sampling method is best for showing changes along an environmental gradient?', 'systematic sampling along a transect', ['random sampling across the whole area', 'opportunistic sampling', 'a single quadrat'], 'Regular intervals capture the gradient.'),
         ('How can a student decide how many quadrats are enough?', 'plot a species-area curve and continue until it levels off', ['always use one quadrat', 'stop when bored', 'use only the first five'], 'The plateau indicates most species are recorded.'),
         ('Which is an ethical consideration in a questionnaire survey?', 'participants remain anonymous and give informed consent', ['questions should lead respondents', 'only friends are surveyed', 'results are changed to match the hypothesis'], 'IB requires ethical treatment of participants.'),
         ('A Likert scale in a questionnaire records:', 'the degree of agreement with a statement, e.g. on a 1-5 scale', ['the age of respondents', 'only yes/no answers', 'the time of the survey'], 'It gives ordinal data.'),
         ('Which is a safety precaution for river fieldwork?', 'working in pairs and not entering water above knee depth', ['sampling during floods', 'working alone', 'wearing no footwear'], 'Part of a risk assessment.')],
  why=[('Explain why random sampling reduces bias.', 'Each location has an equal chance of selection, so the investigator cannot consciously or unconsciously choose sites that support the hypothesis; the sample is more likely to be representative.'),
       ('Explain why a pilot study is useful.', 'It tests whether methods work, reveals practical problems, helps determine suitable quadrat size, sample number and range of the IV, and checks that questionnaire questions are clear.'),
       ('Explain why sample size affects the reliability of conclusions.', 'Larger samples reduce the effect of random variation and outliers, give more reliable means and narrower standard deviations relative to the mean, and increase the power of statistical tests.')],
  contrast=[('random sampling', 'systematic sampling', 'Random sampling selects locations using random numbers, reducing bias in a uniform area; systematic sampling takes samples at regular intervals, which is suitable for gradients but can miss patterns that coincide with the interval.'),
            ('quantitative data', 'qualitative data', 'Quantitative data are numerical (counts, measurements) and can be analysed statistically; qualitative data are descriptive (interviews, observations) and analysed by themes.')],
  misc=[('Collecting more data always makes an investigation better.', 'More data improves reliability only if methods are valid; poorly designed methods produce more unreliable data.'),
        ('Ethics only apply to research on people.', 'Ethical fieldwork also minimises harm to organisms and habitats (returning animals, avoiding trampling, permits for protected sites).')],
  apply=[('Describe a method to sample the distribution of plants across a sand dune ecosystem.', 'Interrupted belt transect from strandline inland; 1 m² quadrats every 10-20 m; record percentage cover of each species; measure abiotic factors (wind speed, soil pH, moisture, organic content); repeat transects to improve reliability.', 4),
         ('Outline three ethical or safety considerations for a questionnaire on attitudes to wind farms in a village.', 'Informed consent and right to withdraw; anonymity and data protection; avoid leading questions; avoid vulnerable people without permission; work in pairs in public places; inform a teacher of location.', 3)],
  cases=[('Malham Tarn, UK, field survey', 'students sample limestone grassland and fen using stratified random quadrats in different vegetation zones', 'stratified sampling', 'dividing the area into strata ensures each habitat type is represented in the sample'),
         ('Coastal litter survey', 'volunteers in the Marine Conservation Society Great British Beach Clean record litter in 100 m sections of beach using standard categories', 'standardised methods and citizen science', 'standard protocols allow comparison between sites and years')],
  evaluate=[('Citizen science data are reliable enough to be used in environmental research.', ['huge spatial and temporal coverage', 'standard protocols (eBird, Big Garden Birdwatch)', 'statistical methods correct for bias'], ['variable observer skill', 'uneven sampling effort', 'identification errors'], 'With standardised protocols and validation, citizen science data are valuable for detecting large-scale trends, though less reliable for fine detail.'),
            ('Systematic sampling is better than random sampling for ecological fieldwork.', ['captures gradients', 'easy to apply', 'ensures coverage'], ['may introduce bias if patterns coincide with intervals', 'random sampling more representative in homogeneous areas'], 'The best method depends on the aim: systematic for gradients, random or stratified random for comparing areas.')],
  extended=[('Evaluate the methods that could be used to investigate the impact of trampling on a footpath ecosystem. [9]', 'Transect from the path; quadrats, percentage cover, species richness, soil compaction (penetrometer), infiltration; sampling strategy and sample size; controls; ethics and safety; limitations; judgement.', 9, 'long')],
  res=[('Species-area data: quadrat area (m²) 0.25: 4 species; 0.5: 7; 1: 10; 2: 12; 4: 13; 8: 13.',
        [('Identify the most suitable quadrat size from the data and justify your choice.', 'About 2-4 m²: the curve levels off at 13 species by 4 m², and 2 m² captures 12 of 13 species while saving time.'),
         ('Explain why the curve levels off.', 'As area increases, most species present in the community have already been recorded, so few new species are found.')])])

S('ch12-st3', gens=['spearman', 'chi2', 'mean_sd_t'],
  terms=[('standard deviation', 'a measure of the spread of data around the mean'),
         ('statistical significance', 'the likelihood that a result is not due to chance, commonly accepted when p < 0.05'),
         ('correlation', 'a statistical relationship between two variables, which may be positive or negative and does not prove causation'),
         ('Spearman\'s rank correlation', 'a statistical test that measures the strength and direction of a monotonic relationship between two ranked variables'),
         ('chi-squared test', 'a statistical test of association between categorical variables, comparing observed with expected frequencies'),
         ('t-test', 'a statistical test comparing the means of two samples to determine whether they differ significantly')],
  facts=[('Which test is appropriate to compare the mean number of earthworms in two fields?', 't-test', ['chi-squared test', 'Spearman\'s rank correlation', 'Lincoln index'], 'Comparing two means.'),
         ('Which graph is best for showing the relationship between two continuous variables?', 'a scatter graph', ['a pie chart', 'a bar chart of categories', 'a pictogram'], 'Each point shows one pair of values.'),
         ('Which test assesses whether the presence of a species is associated with a habitat type?', 'chi-squared test', ['t-test', 'Spearman\'s rank', 'Simpson\'s index'], 'Categorical frequency data.'),
         ('A Spearman\'s rank value of −0.92 indicates:', 'a strong negative correlation', ['a weak positive correlation', 'no correlation', 'a perfect positive correlation'], 'rs ranges from −1 to +1.'),
         ('Error bars showing ± one standard deviation that overlap greatly suggest:', 'the difference between the means may not be significant', ['the difference is definitely significant', 'the data are fabricated', 'the sample size is infinite'], 'A statistical test is needed to confirm.')],
  why=[('Explain why a statistical test is needed even when two means look different.', 'Differences may be due to random sampling variation; a test calculates the probability that the difference arose by chance, so the conclusion can be stated with known confidence.'),
       ('Explain why correlation does not prove causation.', 'Two variables may change together because a third variable affects both, by coincidence, or because the causal direction is reversed; a mechanism and controlled evidence are needed to show causation.'),
       ('Explain why the choice of graph matters when presenting data.', 'An appropriate graph (scatter for relationships, bar for categories, line for time series, kite diagrams for transects) shows patterns clearly; an inappropriate one can obscure or mislead.')],
  contrast=[('a t-test', 'a chi-squared test', 'A t-test compares the means of two samples of continuous data; a chi-squared test assesses association between categorical variables using frequency counts.'),
            ('accuracy', 'precision', 'Accuracy is how close a measurement is to the true value; precision is how close repeated measurements are to each other.')],
  misc=[('A p-value of 0.05 means the hypothesis is 95% certain to be true.', 'p = 0.05 means there is a 5% probability of obtaining a result at least this extreme if the null hypothesis were true; it does not give the probability that the hypothesis is true.'),
        ('Anomalous results should always be deleted.', 'Anomalies should be identified and investigated; they may be excluded only with justification (e.g. a known error) and this should be stated.')],
  apply=[('Suggest the most suitable graph for each: (a) species percentage cover along a sand dune transect, (b) monthly CO₂ concentration over 10 years, (c) proportion of waste types.', '(a) kite diagram; (b) line graph; (c) pie chart or divided bar chart.', 3),
         ('State the null hypothesis and the test you would use to investigate whether soil pH correlates with species richness at 12 sites.', 'H₀: there is no significant correlation between soil pH and species richness; Spearman\'s rank correlation (n = 12).', 2)],
  cases=[('Keeling Curve analysis', 'monthly CO₂ data from Mauna Loa since 1958 show a rising trend with an annual oscillation', 'presenting and analysing time-series data', 'a line graph reveals both a long-term trend and seasonal cycles caused by Northern Hemisphere photosynthesis'),
         ('Lichen and NO₂ study', 'students found rs = 0.85 between distance from a road and lichen diversity at 10 trees (critical value 0.648)', 'Spearman\'s rank correlation', 'the significant positive correlation supports the hypothesis, but other variables such as tree species and bark pH must be considered')],
  evaluate=[('Statistical tests are essential for drawing valid conclusions in environmental investigations.', ['distinguish real patterns from chance', 'quantify confidence', 'objective decision rule'], ['small samples give low power', 'tests depend on assumptions', 'qualitative data may be more appropriate for social studies', 'significance is not importance'], 'Statistical tests strengthen quantitative conclusions, but they must suit the data and be interpreted with ecological and social context.'),
            ('Graphs are more useful than statistical tests in communicating environmental data.', ['show patterns and anomalies clearly', 'accessible to non-specialists'], ['can mislead through scale choices', 'do not show whether differences are significant'], 'Graphs and statistics are complementary: graphs communicate patterns and tests confirm whether they are significant.')],
  extended=[('Explain how you would analyse and present data from an investigation comparing species diversity in two woodlands. [7]', 'Simpson\'s index for each site; mean and SD of quadrats; t-test with H₀; bar chart with error bars; table of raw and processed data; interpretation of significance; limitations.', 7, 'explain')],
  res=[('Percentage cover of marram grass along a sand dune transect: 0 m: 5%; 20 m: 60%; 40 m: 45%; 60 m: 15%; 80 m: 5%; 100 m: 0%.',
        [('Suggest a suitable graph and describe the pattern.', 'Kite diagram or line graph: cover rises sharply to a peak of 60% at 20 m (yellow dunes) then declines to 0% by 100 m.'),
         ('Explain the pattern using succession.', 'Marram thrives in mobile yellow dunes with burial by sand; further inland, stabilised soil with more organic matter allows other species to outcompete it.')])])

S('ch12-st4',
  terms=[('validity', 'the extent to which a method measures what it claims to measure and answers the research question'),
         ('reliability', 'the consistency of results when an investigation is repeated'),
         ('limitation', 'a weakness in the method or data that reduces the validity or reliability of the conclusion'),
         ('systematic error', 'an error that shifts all measurements in the same direction, e.g. a miscalibrated pH meter'),
         ('random error', 'unpredictable variation in measurements that can be reduced by repeating and averaging'),
         ('extension', 'a suggestion for further investigation that builds on the findings')],
  facts=[('Which improves the reliability of a field investigation?', 'repeating measurements and increasing the sample size', ['using a single quadrat', 'changing the method each time', 'sampling only one day'], 'Repeats reduce random error.'),
         ('A pH meter that always reads 0.3 units too high causes:', 'a systematic error', ['a random error', 'an anomaly that cannot be corrected', 'no error'], 'Calibration corrects it.'),
         ('In the ESS IA, the "application" criterion asks students to:', 'relate findings to the wider environmental issue and suggest solutions', ['only list equipment', 'repeat the method', 'copy secondary data'], 'Application links the investigation to the issue.'),
         ('Which is a valid conclusion from a significant Spearman\'s rank result?', 'there is a significant correlation between the variables at the p = 0.05 level', ['the IV definitely causes the DV', 'the result is 100% certain', 'the hypothesis is proven forever'], 'Correlation only.')],
  why=[('Explain why the limitations of an investigation should be discussed.', 'They show how far the conclusion can be trusted, distinguish significant from minor weaknesses, and lead to realistic improvements and extensions.'),
       ('Explain why conclusions should refer to the data and the research question.', 'The conclusion must answer the RQ using specific processed results and statistics, so it is supported by evidence rather than assumption.'),
       ('Explain why a small-scale investigation can still be applied to a wider environmental issue.', 'Local data illustrate processes that operate more widely (e.g. trampling, pollution gradients); findings can inform local management and be compared with published studies, though generalisation should be cautious.')],
  contrast=[('validity', 'reliability', 'Validity is whether the method measures what it is intended to and answers the RQ; reliability is whether repeated measurements give consistent results.'),
            ('systematic error', 'random error', 'Systematic error shifts all readings in one direction and is reduced by calibration or method changes; random error causes unpredictable scatter and is reduced by repeats and larger samples.')],
  misc=[('If results do not support the hypothesis the investigation has failed.', 'Rejecting a hypothesis is a valid scientific outcome; the discussion should explain possible reasons and what was learned.'),
        ('Listing many minor limitations shows good evaluation.', 'Strong evaluation identifies the most significant weaknesses, explains their effect on the results and proposes realistic improvements.')],
  apply=[('A student found no significant difference in lichen diversity between two parks. Suggest three reasons and an improvement for each.', 'Small sample size - sample more trees; uncontrolled tree species or bark pH - sample one species; parks have similar pollution levels - choose sites with greater contrast or measure NO₂ with diffusion tubes.', 3),
         ('Suggest how the findings of a footpath trampling study could be applied to management of a national park.', 'Boardwalks or surfaced paths, path rotation or closure for recovery, signs and fences to keep walkers on paths, visitor education, monitoring with repeat surveys.', 2)],
  cases=[('Footpath erosion study, Snowdon, Wales', 'students found vegetation cover fell from about 90% at 5 m to under 20% at the path edge', 'applying results to management', 'the data support stone pitching and path repairs used by Snowdonia National Park to concentrate walkers'),
         ('Microplastics on urban beaches', 'a student found more microplastic fragments near a storm drain outfall but sampled only on one day after rain', 'evaluating limitations', 'the single sampling date means weather may have caused the pattern, so repeated sampling is needed before linking it to the drain')],
  evaluate=[('Small-scale student investigations can contribute to solving environmental problems.', ['local data inform local decisions', 'citizen science databases', 'raises awareness'], ['limited samples and time', 'results may not generalise', 'lack of peer review'], 'Student investigations contribute mainly through local awareness and citizen-science datasets; their wider value depends on rigorous methods and sharing data.'),
            ('The evaluation section is the most important part of an environmental investigation.', ['shows the reliability of conclusions', 'leads to improvements'], ['without a valid method and analysis there is nothing to evaluate', 'the RQ and data underpin everything'], 'Evaluation is crucial for judging conclusions, but it depends on a sound research question, method and analysis.')],
  extended=[('Evaluate the strengths and limitations of an investigation into the effect of a named human activity on a local ecosystem and suggest how its findings could be applied. [9]', 'Strengths (sampling strategy, sample size, statistics); limitations (time, seasonality, uncontrolled variables, errors); impact on conclusion; improvements and extensions; application to management and the wider issue; judgement.', 9, 'long')],
  res=[('Student results: mean species per quadrat 0-2 m from path 3.2 (SD 1.1), 8-10 m from path 9.6 (SD 4.8); n = 5 quadrats at each distance; data collected on one afternoon in October.',
        [('Comment on the reliability of the data.', 'Low reliability: only five quadrats per distance; the SD at 8-10 m is half the mean (high variability); one date only, so seasonal effects are unknown.'),
         ('Suggest two improvements.', 'Increase to at least 10-15 quadrats per distance with random placement; repeat in different seasons; sample several transects; measure soil compaction to support the explanation.')])])


# ---------------------------------------------------------------- additional evaluate / discuss claims (C4 variety)
EXTRA_EV = {
    'ch06-st1': ('Renewable resources will always be more sustainable than non-renewable resources.', ['they regenerate within human timescales', 'solar and wind are effectively inexhaustible'], ['renewable stocks such as fisheries, forests and aquifers can be overexploited beyond recovery', 'renewable technologies rely on non-renewable minerals (lithium, cobalt, copper)'], 'Renewable resources are only sustainable if harvested within their natural income; poorly managed renewables can collapse, as Atlantic cod did.'),
    'ch06-st3': ('Sustainable yield is an effective basis for managing natural resources.', ['uses natural income without depleting natural capital', 'quantifiable targets (MSY, allowable cut)'], ['population and growth estimates are uncertain', 'ignores ecosystem interactions and bycatch', 'political pressure sets quotas above scientific advice'], 'Sustainable yield is a sound principle, but it must be applied with precaution and an ecosystem approach to be effective.'),
    'ch07-st2': ('Countries should aim for energy independence rather than relying on imported energy.', ['protects against supply shocks (Europe 2022)', 'domestic jobs and investment', 'renewables can be produced locally'], ['imports may be cheaper and more efficient', 'some countries lack domestic resources', 'interconnected grids improve resilience'], 'Greater self-sufficiency, especially through domestic renewables, improves security, but complete independence is rarely efficient; diversification and trusted interconnections matter more.'),
    'ch08-st1': ('Rising incomes inevitably lead to more solid domestic waste.', ['waste per person rises with GDP (World Bank What a Waste 2.0)', 'more packaging and consumer goods'], ['some high-income countries have cut waste per person through policy (Japan, Germany)', 'circular economy and reuse can decouple waste from income'], 'Waste generation tends to rise with income, but policy and cultural change show that the link is not inevitable.'),
    'ch09-st1': ('The world population will stop growing in the 21st century.', ['global TFR has fallen to about 2.3 and continues to fall', 'UN 2024 projections show a peak of about 10.3 billion in the mid-2080s'], ['population momentum and high fertility in sub-Saharan Africa', 'projections are uncertain and depend on future fertility decline'], 'Most projections show a peak this century, but its timing and size depend on how quickly fertility falls in high-fertility countries.'),
    'ch09-st2': ('An ageing population is a greater challenge than a youthful population.', ['shrinking workforce, rising pension and healthcare costs (Japan, Italy)', 'hard to reverse low fertility'], ['youthful populations need schools, jobs and food (Niger)', 'youth unemployment and resource pressure', 'ageing societies can use automation and migration'], 'Both create challenges; a youthful population can bring a demographic dividend if jobs and education are provided, while ageing is harder to reverse but wealthier societies have more means to adapt.'),
}
for _k, _ev in EXTRA_EV.items():
    P.R.f[_k].evaluate.append(_ev)
