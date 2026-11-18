"""IB DP Business Management SL/HL (first assessment 2024) - ib-g12-business, year 2 (Units 4-5, Paper 1/3 skills, IA).

Same assessment model and shared machinery as ib_g11_business.py (markbands, Paper 1/2/3 templates, social
enterprise cases for Paper 3). Paper 2 calculation slots draw on the quantitative chapters of year 2:
sales forecasting (moving averages, seasonal variation), sampling and survey statistics, break-even and
contribution, margin of safety and target profit/price, make-or-buy and capacity utilisation, stock control,
and critical path analysis. Numbers in parametric items are for fictional firms; real organizations appear
in cases with rounded, public facts.
"""
from __future__ import annotations

import copy

from _common import F, Registry, T, mcq, name, two_names, CITIES  # noqa: F401
import ib_g11_business as base
from ib_g11_business import (CONFIG, STYLE, CONCEPTS, MB10, MB15, MB20, SE, bm_templates, make_S, firm, cur, m,  # noqa: F401
                             p1, p2, MK, lc, cap)

# Same 15-item, 105-mark mock as year 1; Paper 2 calculations come from the forecasting/research and
# break-even/production-planning chapters, where every subtopic has computed generators.
MOCK = copy.deepcopy(base.MOCK)
for _sec in MOCK:
    if _sec.get('style') == 'calc':
        _sec['chapters'] = [2, 10]

R = Registry()
CONC: dict[str, tuple] = {}
S = make_S(R, CONC)


def more(key, **kw):
    base.more(key, reg=R, **kw)


def calc(key, c='C3', d=(1, 5), ty='numerical'):
    return base.calc(key, c, d, ty, reg=R)


def init(subject_id):
    pass


def templates(st):
    return bm_templates(R, CONC, st)


def pct(x):
    return p1(x) + '%'


# =============================================================================================
# ch01 Unit 4.1-4.2 Introduction to marketing and marketing planning
# =============================================================================================
S('ch01-st1', concepts=('change', 'creativity', 'ethics'),
  terms=[('marketing', 'the management process of identifying, anticipating and satisfying customer needs and wants profitably'),
         ('market orientation', 'an approach in which a business researches customer needs and wants first and then develops products to satisfy them'),
         ('product orientation', 'an approach in which a business focuses on making a product it is good at, then tries to find customers to buy it'),
         ('market', 'a place or process where buyers and sellers exchange goods and services'),
         ('social marketing', 'marketing that aims to change people\'s behaviour for the benefit of society, such as campaigns against smoking'),
         ('marketing mix', 'the combination of elements (the 7Ps: product, price, promotion, place, people, processes and physical evidence) used to market a product')],
  facts=[('A business that develops products after researching what customers want is:', 'market oriented', ['product oriented', 'sales oriented', 'production oriented'], 'Market orientation starts with customer needs.'),
         ('Which business function must work most closely with marketing when a new product is planned?', 'Operations, which must be able to produce it at the required quality and cost', ['Only human resources', 'No other function', 'Only the legal department'], 'Marketing decisions affect finance, HR and operations.'),
         ('Dyson\'s focus on engineering breakthroughs such as the bagless vacuum cleaner is often given as an example of:', 'product orientation driven by innovation', ['social marketing', 'mass marketing of commodities', 'a loss leader strategy'], 'Dyson designs technically superior products and then markets them.'),
         ('Which of the following is a feature of marketing goods rather than services?', 'Goods can be stored as inventory', ['Goods are intangible', 'Goods are perishable at the point of delivery', 'Goods cannot be separated from the provider'], 'Services are intangible and perishable.')],
  why=[('Explain why market orientation can reduce the risk of product failure.', 'Products are designed around researched customer needs, so demand is more likely to exist at launch; feedback can be used to adapt products before large sums are invested.'),
       ('Explain why marketing decisions affect the finance function.', 'Marketing campaigns, product launches and pricing decisions require budgets and affect sales revenue and cash flow, so finance must fund them and forecast their returns.'),
       ('Explain why some firms in high-technology markets remain product oriented.', 'Customers may not know they want a radical new technology until it exists, so firms rely on research and development to create products and then persuade customers to buy them.')],
  contrast=[('market orientation', 'product orientation', 'A market-oriented firm starts from customer research and designs products to satisfy needs; a product-oriented firm starts from what it can make well and then looks for buyers.'),
            ('marketing goods', 'marketing services', 'Goods are tangible and can be stored and inspected before purchase; services are intangible, perishable and produced at the point of delivery, so people, processes and physical evidence matter more.')],
  misc=[('Marketing is the same as advertising.', 'Advertising is only one part of promotion; marketing includes research, product development, pricing, distribution and customer service.'),
        ('A product-oriented business never succeeds.', 'Product-oriented firms can succeed when they innovate products customers value, as Dyson and early Apple did, but they carry higher risk.')],
  cases=[('Dyson\'s bagless vacuum cleaner', 'James Dyson built 5,127 prototypes over five years before launching the bagless vacuum cleaner in 1993.', 'product orientation', 'the firm built a technically superior product first and then created demand for it'),
         ('Netflix\'s viewing data', 'Netflix uses viewing data from over 270 million subscribers to decide which series to commission and how to recommend them.', 'market orientation', 'customer data drives product decisions, reducing the risk of commissioning unpopular content'),
         ('the UK\'s anti-smoking campaigns', 'UK government campaigns such as "Stoptober", launched in 2012, encourage smokers to quit for 28 days.', 'social marketing', 'marketing techniques are used to change behaviour for public benefit rather than to sell a product')],
  apply=[('A start-up has developed a solar-powered phone charger but has not researched demand. Explain one risk of this product-oriented approach and suggest how it could become more market oriented.', 'Risk: customers may not value the features or price, so sales may be too low to cover development costs. It could test the prototype with target customers, run surveys or a crowdfunding campaign to measure demand, and adapt the design and price before full launch.', 4),
         ('A hotel chain plans a large advertising campaign. Explain how the campaign affects the human resources and operations functions.', 'HR may need to recruit and train extra staff for higher demand; operations must ensure rooms, food and services can handle more guests at the promised quality, or the campaign will damage the brand.', 4)],
  evaluate=[('Market orientation is always better than product orientation.', ['reduces risk of failure', 'products meet customer needs', 'easier to adapt to change'],
             ['customers may not imagine radical innovations', 'research is costly and slow', 'product-led innovators such as Dyson succeed', 'copying customer wishes may reduce creativity'], 'Market orientation suits most firms, but a balance is best: radical innovators may need a product-led approach backed by later market testing.')],
  )


@calc('ch01-st2', 'C3', (1, 5))
def market_share(rng, slot):
    c = cur(rng)
    firms = rng.sample(['AquaPure', 'BlueSpring', 'Crystal Co.', 'DewDrop', 'Evergreen Springs', 'Fjell Water'], 4)
    sales = [rng.choice([12, 15, 18, 20, 24, 30, 36, 40]) for _ in firms]
    tot = sum(sales)
    if slot.d <= 2:
        i = rng.randrange(4)
        return dict(stem=f'In a bottled-water market worth {m(tot, c)} million a year, {firms[i]} has sales of {m(sales[i], c)} million. Calculate its market share.',
                    answer=f'{pct(100 * sales[i] / tot)}', markingKey=MK(f'{sales[i]}/{tot} × 100 = {p1(100 * sales[i] / tot)}%.', f'{p1(100 * sales[i] / tot)}%'), marks=2)
    g = rng.choice([4, 5, 8, 10, 12])
    gi = rng.choice([10, 15, 20, 25])
    i = rng.randrange(4)
    tot2 = tot * (1 + g / 100)
    s2 = sales[i] * (1 + gi / 100)
    sh1 = 100 * sales[i] / tot
    sh2 = 100 * s2 / tot2
    tab = '; '.join(f'{f} {m(s, c)} m' for f, s in zip(firms, sales))
    stem = (f'Annual sales in a bottled-water market were: {tab}. Next year the market is forecast to grow by {g}% and {firms[i]}\'s sales by {gi}%. '
            f'Calculate the market size, {firms[i]}\'s market share now and next year, and comment on the change.')
    return dict(stem=stem,
                answer=f'Market size = {m(tot, c)} m; share now = {p1(sh1)}%; next year market = {m(round(tot2, 2), c)} m, sales = {m(round(s2, 2), c)} m, share = {p1(sh2)}%. '
                       f'Its sales grow faster than the market, so its market share rises by {p1(sh2 - sh1)} percentage points, a sign of competitive strength.',
                markingKey=MK(f'total {tot}; {sales[i]}/{tot} × 100 = {p1(sh1)}%; {tot} × {1 + g / 100:g} = {tot2:g}; {sales[i]} × {1 + gi / 100:g} = {s2:g}; {s2:g}/{tot2:g} × 100 = {p1(sh2)}%.', 'all values') + ' [1] comment.',
                marks=4 if slot.d <= 3 else 6)


S('ch01-st2', concepts=('change', 'creativity'),
  terms=[('market share', 'the percentage of total sales in a market made by one business: firm\'s sales / total market sales × 100'),
         ('market size', 'the total sales of all businesses in a market, measured by value or volume'),
         ('market growth', 'the percentage change in the size of a market over a period'),
         ('market leader', 'the business with the largest market share in a market'),
         ('saturated market', 'a market in which there is little or no growth because most potential customers already own the product')],
  facts=[('A firm sells $30 m in a market worth $200 m. Its market share is:', '15%', ['30%', '6.7%', '20%'], '30/200 × 100 = 15%.'),
         ('A market grows from $400 m to $440 m. Market growth is:', '10%', ['40%', '9.1%', '4%'], '(440 − 400)/400 × 100 = 10%.'),
         ('If a firm\'s sales rise by 5% while the market grows by 10%, its market share will:', 'fall', ['rise', 'stay the same', 'double'], 'Its sales grow more slowly than the market.'),
         ('Which company had the largest share of global smartphone shipments in many quarters of 2023-2024?', 'Samsung or Apple, each with roughly 20%', ['Nokia, with over 50%', 'BlackBerry, with about 40%', 'Huawei, with over 60%'], 'The two leaders each hold about a fifth of shipments.')],
  why=[('Explain why market share is a useful measure of a firm\'s performance.', 'It shows performance relative to competitors rather than in isolation; a rising share means the firm is winning customers, which can bring economies of scale and bargaining power.'),
       ('Explain why a firm can gain sales but lose market share.', 'If the market grows faster than the firm\'s sales, the firm\'s sales are a smaller percentage of a bigger market, even though they rose in absolute terms.'),
       ('Explain why firms in saturated markets compete aggressively for market share.', 'With little market growth, a firm can only grow by taking customers from rivals, so firms use price cuts, promotion and differentiation to win share.')],
  contrast=[('market share', 'market size', 'Market size is the total sales of all firms in the market; market share is the percentage of that total achieved by one firm.'),
            ('market growth', 'market share', 'Market growth measures how fast the whole market is expanding; market share measures one firm\'s position within it.')],
  misc=[('If a firm\'s sales increase, its market share must increase.', 'Market share also depends on market growth; if the market grows faster than the firm\'s sales, its share falls.')],
  cases=[('the global smartphone market', 'Global smartphone shipments of around 1.2 bn a year are close to saturation, with Samsung and Apple each holding about a fifth of the market.', 'market share in a saturated market', 'growth must come from winning rivals\' customers or upgrades, so competition focuses on features and brand'),
         ('the rise of BYD', 'Chinese firm BYD sold over 3 million new-energy vehicles in 2023, overtaking Tesla in some quarters as the world\'s largest seller of electric cars.', 'market share and market growth', 'BYD grew faster than a fast-growing market, increasing its share through low-cost models'),
         ('Oatly and plant-based milk', 'Plant-based milk sales grew quickly in the late 2010s; Oatly\'s early lead was then challenged by supermarket own-label oat drinks.', 'market growth and competition', 'a growing market attracts new entrants, so an early leader may see its share fall even while its sales rise')],
  apply=[('A firm\'s sales rose from $8 m to $9 m while the market grew from $80 m to $100 m. Calculate its market share in both years and comment.', 'Year 1: 8/80 = 10%; year 2: 9/100 = 9%. Sales grew 12.5% but the market grew 25%, so market share fell; the firm is losing ground to competitors.', 4),
         ('Explain two ways a firm could increase its market share in a slow-growing market.', 'For example: cut prices or offer promotions to win customers from rivals; differentiate the product through features or branding; acquire a competitor; or improve distribution.', 4)],
  evaluate=[('Increasing market share should be the main marketing objective for every business.', ['economies of scale', 'brand recognition and bargaining power', 'shows competitiveness'],
             ['share gained through price cuts may reduce profit', 'niche firms may prefer high margins in small markets', 'growing market may matter more', 'regulation of dominant firms'], 'Market share is a useful objective for mass-market firms, but profitability and customer loyalty may matter more, especially for niche businesses.')],
  )

S('ch01-st3', concepts=('change', 'creativity', 'ethics'),
  terms=[('marketing plan', 'a document setting out a firm\'s marketing objectives, target market, marketing mix, budget and timescale'),
         ('target market', 'the group of customers a business aims to sell its product to'),
         ('market segmentation', 'dividing a market into distinct groups of customers with similar characteristics and needs'),
         ('demographic segmentation', 'dividing a market by characteristics such as age, gender, income, education or ethnicity'),
         ('psychographic segmentation', 'dividing a market by lifestyle, values, attitudes and personality'),
         ('niche market', 'a small, well-defined segment of a market with specific needs'),
         ('mass market', 'a large market in which a standard product is sold to most customers')],
  facts=[('Dividing customers by lifestyle and values is:', 'psychographic segmentation', ['demographic segmentation', 'geographic segmentation', 'mass marketing'], 'Psychographic = lifestyle, values, attitudes.'),
         ('Which is a feature of niche marketing?', 'Targeting a small segment with specialised needs', ['Selling the same product to everyone', 'Very high sales volumes', 'Always the lowest prices'], 'Niche firms specialise.'),
         ('Which of the following belongs in a marketing plan?', 'Marketing objectives, the marketing mix and the marketing budget', ['Only the cash-flow forecast', 'Only the organization chart', 'Only staff contracts'], 'A plan sets objectives, strategy, mix and budget.'),
         ('Rolex targets wealthy customers who value status. This is an example of segmentation by:', 'income and lifestyle', ['geography only', 'age only', 'product usage rate only'], 'Luxury brands use demographic and psychographic segmentation.')],
  why=[('Explain why segmentation helps a business use its marketing budget efficiently.', 'Marketing can be aimed at the customers most likely to buy, through the media they use, with messages that match their needs, so less money is wasted on people who will not buy.'),
       ('Explain why a small business may choose niche marketing.', 'It avoids direct competition with large mass-market firms, allows premium prices for specialised products and builds customer loyalty with a small budget.'),
       ('Explain why a marketing plan should be reviewed regularly.', 'Customer tastes, competitors and the external environment change, so objectives, budgets and the mix need updating to stay effective.')],
  contrast=[('niche marketing', 'mass marketing', 'Niche marketing targets a small segment with specialised products, often at premium prices; mass marketing sells a largely standard product to the whole market at high volume.'),
            ('demographic segmentation', 'psychographic segmentation', 'Demographic segmentation uses measurable characteristics such as age and income; psychographic segmentation uses lifestyle, attitudes and values.')],
  misc=[('Niche markets are always less profitable than mass markets.', 'Niche firms can charge premium prices and face less competition, so margins can be high even though volumes are lower.')],
  cases=[('Lululemon\'s target market', 'Lululemon built its brand around yoga and fitness customers, originally women aged about 25-40 with high incomes and active lifestyles.', 'market segmentation and targeting', 'a clear psychographic and demographic target allowed premium pricing and community-based marketing'),
         ('Unilever\'s Dove and Axe brands', 'Unilever markets both Dove, with its "Real Beauty" campaign, and Axe (Lynx), aimed at young men, despite very different brand messages.', 'segmentation and different target markets', 'separate brands let one company target distinct segments with tailored messages'),
         ('Coca-Cola\'s range of colas', 'Coca-Cola sells Coca-Cola Classic, Diet Coke and Coca-Cola Zero Sugar, each aimed at different consumer groups.', 'segmentation', 'product variants target health-conscious and taste-focused segments within one mass market')],
  apply=[('A gym chain wants to grow. Suggest two market segments it could target and explain how the marketing mix should differ between them.', 'For example, students (low price, off-peak membership, social media promotion) and retired people (daytime classes, health-focused programmes, local press and doctors\' referrals). Price, promotion and product features should match each segment\'s needs.', 4),
         ('A market for running shoes is worth $500 m. Research suggests that 30% of sales come from serious runners and 70% from casual buyers. A new brand targets only serious runners and aims for a 5% share of that segment. Calculate its target sales.', 'Serious-runner segment = 30% × $500 m = $150 m; 5% × $150 m = $7.5 m target sales.', 2)],
  evaluate=[('Segmentation is essential for every business.', ['efficient use of marketing budget', 'products tailored to needs', 'identifies gaps in the market'],
             ['research costs', 'segments may be too small to be profitable', 'some products suit mass marketing (e.g. salt, petrol)', 'risk of stereotyping customers'], 'Segmentation is valuable for most firms, but its benefits depend on whether segments are distinct, measurable and large enough.')],
  )

S('ch01-st4', concepts=('creativity', 'change'),
  terms=[('position map', 'a two-dimensional diagram showing how customers perceive brands in a market against two variables, such as price and quality'),
         ('unique selling point (USP)', 'a feature that makes a product different from and preferred to competitors\' products'),
         ('product differentiation', 'making a product different from rivals\' products through features, design, branding or service'),
         ('repositioning', 'changing customers\' perceptions of a brand so that it occupies a different position in the market'),
         ('gap in the market', 'an area of a position map with no or few products, which may indicate unmet customer needs')],
  facts=[('A position map usually shows:', 'how customers perceive brands against two variables', ['a firm\'s cash flow', 'the product life cycle', 'the organization chart'], 'It maps perceptions, e.g. price vs quality.'),
         ('A gap on a position map:', 'may show an opportunity, but research is needed to check demand', ['always means guaranteed profit', 'shows illegal products', 'means the market is saturated'], 'Gaps may exist because there is no demand.'),
         ('Volvo has long positioned its cars around:', 'safety', ['the lowest price', 'speed records', 'off-road racing'], 'Safety has been central to Volvo\'s brand since the three-point seatbelt in 1959.')],
  why=[('Explain why a USP can allow a firm to charge a higher price.', 'Customers see the product as different and better than substitutes, so demand is less price elastic and they will pay a premium.'),
       ('Explain why a gap on a position map may not be a profitable opportunity.', 'There may be no gap in demand – for example few customers want a high-price, low-quality product – or the segment may be too small to cover costs.'),
       ('Explain why firms reposition their brands.', 'Customer tastes change, competitors move into the brand\'s position, or the firm wants to reach a growing or more profitable segment.')],
  contrast=[('a USP', 'product differentiation', 'A USP is one specific feature that makes a product unique; product differentiation is the broader process of making a product different from rivals in any way.')],
  misc=[('Every gap on a position map is a profitable opportunity.', 'A gap may exist because customers do not want that combination of features, so market research is needed before entering it.')],
  cases=[('Burberry\'s repositioning', 'In the 2000s Burberry\'s check pattern was widely copied and linked with counterfeit goods; the firm reduced licensing and refocused on luxury catwalk collections.', 'repositioning a brand', 'tighter control of the brand moved it back to the high-price, high-status part of the market'),
         ('Aldi and Lidl in the UK', 'The discount supermarkets Aldi and Lidl raised their combined UK market share to around 18% by 2024 by offering low prices with acceptable quality.', 'positioning on a position map', 'they occupy a low-price, good-value position, attracting shoppers from the traditional "big four" supermarkets'),
         ('Tesla\'s early positioning', 'Tesla launched the high-priced Roadster and Model S before cheaper models, positioning electric cars as high-performance products.', 'product differentiation and positioning', 'a premium, high-tech position changed perceptions of electric cars and supported high prices')],
  apply=[('Draw and explain a position map for the coffee shop market using price and atmosphere as axes, placing three real or imagined brands.', 'Axes: price (low to high) and atmosphere (basic to premium). Example: a vending machine (low, basic), a chain such as Costa or Starbucks (medium-high, comfortable), an independent artisan café (high, premium). The map shows where competition is strong and where gaps may exist.', 4),
         ('A smartphone maker\'s USP is its battery life. Explain one risk of relying on this USP.', 'Competitors may copy or improve battery technology, removing the USP; the firm then needs another source of differentiation or must compete on price.', 2)],
  evaluate=[('A strong USP guarantees long-term success.', ['supports premium prices', 'brand loyalty', 'clear marketing message'],
             ['rivals can copy features', 'technology and tastes change', 'USP must be communicated and valued by customers', 'other mix elements matter'], 'A USP gives an advantage, but it must be protected, communicated and renewed as markets change.')],
  )


# =============================================================================================
# ch02 Unit 4.3-4.4 Sales forecasting and market research
# =============================================================================================
@calc('ch02-st1', 'C3', (1, 5))
def moving_average(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    if slot.d <= 2:
        vals = [rng.choice(range(40, 90, 2)) for _ in range(5)]
        ma = [round(sum(vals[i:i + 3]) / 3, 1) for i in range(3)]
        yrs = [2019 + i for i in range(5)]
        return dict(stem=f'{f_}\'s annual sales (thousand units) were: ' + ', '.join(f'{y} {v}' for y, v in zip(yrs, vals)) + '. Calculate the three-year moving averages.',
                    answer=', '.join(f'{yrs[i + 1]}: {p1(ma[i])}' for i in range(3)),
                    markingKey=MK('; '.join(f'({vals[i]} + {vals[i + 1]} + {vals[i + 2]})/3 = {p1(ma[i])}' for i in range(3)), 'all three averages, centred on the middle year'), marks=2)
    # quarterly data, four-quarter centred moving average and seasonal variation
    trend = rng.choice([100, 120, 150, 200])
    step = rng.choice([2, 4, 5, 6])
    season = rng.choice([(-20, 10, 30, -20), (10, -10, -20, 20), (-30, 0, 40, -10), (15, 5, -25, 5)])
    q = [trend + step * i + season[i % 4] for i in range(8)]
    labels = [f'Y1 Q{i + 1}' for i in range(4)] + [f'Y2 Q{i + 1}' for i in range(4)]
    four = [sum(q[i:i + 4]) / 4 for i in range(5)]
    cen = [(four[i] + four[i + 1]) / 2 for i in range(4)]  # centred on Y1Q3, Y1Q4, Y2Q1, Y2Q2
    sv = [q[i + 2] - cen[i] for i in range(4)]
    tab = ', '.join(f'{lab} {v}' for lab, v in zip(labels, q))
    stem = f'{f_}\'s quarterly sales ({c}000) were: {tab}. Calculate the four-quarter centred moving averages for Y1 Q3 to Y2 Q2 and the seasonal variation for each of these quarters.'
    if slot.d >= 4:
        stem += ' Comment on the trend and explain one limitation of using moving averages to forecast sales.'
    ans = ('Centred moving averages: ' + ', '.join(f'{labels[i + 2]} {p2(cen[i])}' for i in range(4)) +
           '. Seasonal variations: ' + ', '.join(f'{labels[i + 2]} {"+" if sv[i] >= 0 else ""}{p2(sv[i])}'.replace('-', '−') for i in range(4)) + '.')
    if slot.d >= 4:
        ans += f' The trend rises by about {p2((cen[3] - cen[0]) / 3)} per quarter. Limitation: it assumes past patterns continue and cannot predict sudden changes (e.g. a new competitor or recession).'
    return dict(stem=stem, answer=ans,
                markingKey=MK('four-quarter totals ÷ 4 = ' + ', '.join(p2(x) for x in four) + '; centre by averaging adjacent pairs; seasonal variation = actual − trend.', 'all centred averages and variations') + (' [1] trend comment; [1] limitation.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch02-st1', concepts=('change', 'creativity'),
  terms=[('sales forecasting', 'predicting future sales levels, usually using past sales data, market research and judgement'),
         ('moving average', 'the average of a set number of consecutive data points, recalculated as each new point is added, used to smooth out fluctuations and show the trend'),
         ('trend', 'the underlying direction in which data is moving over time'),
         ('seasonal variation', 'the difference between actual sales and the trend that recurs at the same time each year'),
         ('cyclical variation', 'changes in sales caused by the business cycle, lasting longer than a year'),
         ('random variation', 'unpredictable changes in sales caused by one-off events such as extreme weather or a pandemic')],
  facts=[('Sales of 20, 26 and 32 give a three-period moving average of:', '26', ['78', '32', '24'], '(20 + 26 + 32)/3 = 26.'),
         ('Why is a four-quarter moving average "centred"?', 'Because the average of four quarters falls between two quarters, so two averages are averaged to align with a quarter', ['To remove the trend', 'To increase sales', 'Because it is required by law'], 'Centring aligns the trend with a specific quarter.'),
         ('Higher ice cream sales every summer are an example of:', 'seasonal variation', ['cyclical variation', 'random variation', 'a falling trend'], 'They recur at the same time each year.'),
         ('If the trend value for Q3 is 150 and actual sales were 170, the seasonal variation is:', '+20', ['−20', '320', '1.13'], 'Actual − trend = 170 − 150.')],
  why=[('Explain why sales forecasts are important to the operations and finance functions.', 'Operations uses them to plan production capacity, staffing and stock; finance uses them to prepare budgets and cash-flow forecasts and to plan borrowing.'),
       ('Explain why moving averages are used to identify the trend.', 'Averaging consecutive periods smooths out seasonal and random fluctuations, so the underlying direction of sales becomes clearer.'),
       ('Explain why sales forecasts based on past data may be inaccurate.', 'They assume past patterns continue, but changes in tastes, competition, the economy or one-off events can break the pattern.')],
  contrast=[('seasonal variation', 'cyclical variation', 'Seasonal variation recurs within each year (e.g. summer peaks); cyclical variation follows the business cycle over several years.'),
            ('the trend', 'random variation', 'The trend is the long-run underlying direction of sales; random variation is an unpredictable one-off change around that trend.')],
  misc=[('A moving average predicts future sales exactly.', 'It only identifies the past trend; extrapolating it assumes conditions stay the same, so forecasts are estimates.')],
  cases=[('retail sales in December', 'UK retailers typically make a large share of annual sales in November and December, around Black Friday and Christmas.', 'seasonal variation', 'firms hire temporary staff and build stock before the seasonal peak'),
         ('toilet paper during Covid-19', 'In March 2020 supermarket sales of toilet paper in many countries more than doubled for several weeks as shoppers stockpiled.', 'random variation and forecasting', 'a one-off event broke past patterns, so forecasts based on moving averages failed'),
         ('Zara\'s demand data', 'Zara uses daily sales data from its stores to adjust production in short runs, rather than relying on long-term forecasts.', 'limitations of sales forecasting', 'responding quickly to actual sales reduces the cost of forecasting errors in fast-changing fashion markets')],
  apply=[('A firm\'s sales trend is rising by 5 units per quarter and the latest trend value (Q4) is 200. The average seasonal variation for Q2 is −15. Forecast sales for Q2 next year.', 'Trend for Q2 next year = 200 + 2 × 5 = 210; forecast = 210 − 15 = 195 units.', 3)],
  evaluate=[('Sales forecasting using moving averages is of little use in a rapidly changing market.', ['past patterns may not continue', 'random events', 'new competitors and technology'],
             ['still identifies trend and seasonality', 'helps budgeting and capacity planning', 'can be combined with research and judgement', 'better than no forecast'], 'Moving averages are less reliable in volatile markets but remain a useful starting point when combined with market research and frequent updating.')],
  )

S('ch02-st2', concepts=('ethics', 'creativity'),
  terms=[('market research', 'the process of collecting, recording and analysing data about customers, competitors and the market'),
         ('primary research', 'the collection of new, first-hand data for a specific purpose, such as surveys, interviews, focus groups and observation'),
         ('secondary research', 'the use of data that already exists, collected by others for a different purpose, such as government statistics and market reports'),
         ('focus group', 'a small group of people who discuss their opinions about a product or idea, guided by a moderator'),
         ('questionnaire', 'a set of questions used to collect data from respondents'),
         ('observation', 'a primary research method in which researchers watch and record how people behave'),
         ('ethical considerations in research', 'principles such as informed consent, confidentiality, honesty and avoiding harm to respondents')],
  facts=[('Which is a secondary research source?', 'A government census report', ['A focus group', 'A street survey', 'A product trial'], 'It already exists and was collected for another purpose.'),
         ('An advantage of primary research is that it is:', 'specific to the firm\'s needs and up to date', ['always cheaper', 'always quick to collect', 'already published'], 'It is tailored but costly.'),
         ('Which method gives in-depth qualitative views from a small group?', 'A focus group', ['A national census', 'Sales records', 'A trade journal'], 'Moderated discussion gives depth.'),
         ('Under data-protection laws such as the EU\'s GDPR, researchers must:', 'obtain consent and protect personal data', ['sell data freely', 'record people secretly in their homes', 'publish respondents\' names'], 'Consent and confidentiality are required.')],
  why=[('Explain why a business might use secondary research before primary research.', 'It is cheaper and quicker, gives an overview of the market and helps identify what specific questions primary research needs to answer.'),
       ('Explain why primary research can be unreliable.', 'Samples may be small or biased, respondents may not answer honestly, and badly worded or leading questions distort results.'),
       ('Explain why ethical considerations matter in market research.', 'Collecting data without consent or misusing it breaks laws such as GDPR, damages trust and reputation, and can harm respondents.')],
  contrast=[('primary research', 'secondary research', 'Primary research collects new data for a specific purpose (e.g. surveys); secondary research uses existing data collected by others (e.g. market reports).'),
            ('a focus group', 'a questionnaire', 'A focus group gives in-depth qualitative views from a few people; a questionnaire collects mainly quantitative data from many respondents.')],
  misc=[('Secondary research is always less useful than primary research.', 'Secondary data is cheap, quick and often covers whole markets; it is less specific, but often the best starting point.')],
  cases=[('New Coke in 1985', 'Coca-Cola\'s taste tests with about 200,000 consumers favoured a sweeter formula, but the launch of "New Coke" caused protests and the original returned within 79 days.', 'limitations of market research', 'blind taste tests missed customers\' emotional attachment to the brand'),
         ('Lego\'s research with children', 'Lego\'s researchers observed girls playing in the late 2000s before launching Lego Friends in 2012, which became one of its best-selling ranges.', 'observation as primary research', 'watching real behaviour revealed needs that surveys might have missed'),
         ('Cambridge Analytica and Facebook data', 'In 2018 it emerged that data from up to 87 million Facebook users had been collected without proper consent and used for political targeting.', 'ethics of market research', 'misuse of personal data led to fines, lost trust and stricter data protection')],
  apply=[('A start-up café plans to open near a university. Suggest one primary and one secondary research method it should use and explain what each would reveal.', 'Primary: a survey or observation of students near the site, showing prices they will pay and preferred products. Secondary: council data on student numbers and footfall, or competitor menus online, showing market size and competition.', 4),
         ('A survey was sent to 800 customers and 200 replied; 120 of the replies said they would buy a new product. Calculate the response rate and the percentage of respondents who would buy, and explain one limitation of the result.', 'Response rate = 200/800 = 25%; would buy = 120/200 = 60%. Limitation: the 25% who replied may not represent all customers (non-response bias), and stated intentions often exceed actual purchases.', 4)],
  evaluate=[('Primary research is always worth its cost.', ['specific and up to date', 'confidential to the firm', 'can test new ideas directly'],
             ['expensive and time-consuming', 'risk of bias and small samples', 'secondary data may be enough', 'research did not save New Coke'], 'Primary research is worth the cost when decisions are large and risky, but it should be well designed and combined with secondary data.')],
  )


@calc('ch02-st3', 'C3', (1, 5))
def stratified(rng, slot):
    f_ = firm(rng)
    n = rng.choice([100, 150, 200, 250, 400])
    groups = rng.choice([[('under 25', 2), ('25-44', 3), ('45-64', 3), ('65 and over', 2)],
                         [('students', 1), ('full-time workers', 5), ('part-time workers', 2), ('retired', 2)],
                         [('city centre', 5), ('suburbs', 3), ('rural areas', 2)]])
    popn = rng.choice([2_000, 5_000, 8_000, 12_000, 20_000])
    wsum = sum(w for _, w in groups)
    pops = [popn * w // wsum for _, w in groups]
    pops[-1] = popn - sum(pops[:-1])
    sizes = [n * p / popn for p in pops]
    tab = '; '.join(f'{g} {p:,}' for (g, _), p in zip(groups, pops))
    stem = f'{f_} has {popn:,} customers: {tab}. It wants a stratified sample of {n} customers. Calculate how many customers should be sampled from each group.'
    if slot.d >= 4:
        stem += ' Explain one advantage of stratified sampling over convenience sampling for this business.'
    ans = '; '.join(f'{g}: {p:,}/{popn:,} × {n} = {p1(s).rstrip("0").rstrip(".")}' for (g, _), p, s in zip(groups, pops, sizes)) + '.'
    if slot.d >= 4:
        ans += ' Advantage: each customer group is represented in proportion to its size, so results are more representative than asking whoever is easiest to reach.'
    return dict(stem=stem, answer=ans,
                markingKey=MK('group size / population × sample size for each group.', 'all group sample sizes (total ' + str(n) + ')') + (' [2] advantage explained.' if slot.d >= 4 else ''),
                marks=3 if slot.d <= 3 else 5)


S('ch02-st3', concepts=('ethics', 'change'),
  terms=[('sampling', 'selecting a group of people from a population to take part in research, so that the results can be generalised to the whole population'),
         ('quota sampling', 'a method in which researchers fill set numbers (quotas) of respondents with given characteristics, choosing the individuals themselves'),
         ('random sampling', 'a method in which every member of the population has an equal chance of being selected'),
         ('stratified sampling', 'a method in which the population is divided into groups (strata) and a random sample is taken from each in proportion to its size'),
         ('convenience sampling', 'a method in which respondents are chosen because they are easy to reach'),
         ('snowball sampling', 'a method in which existing respondents recruit further respondents from among their contacts'),
         ('sampling error', 'the difference between the results from a sample and the true values for the whole population')],
  facts=[('Which method gives every member of the population an equal chance of selection?', 'Random sampling', ['Quota sampling', 'Convenience sampling', 'Snowball sampling'], 'Equal probability is the definition of random sampling.'),
         ('Snowball sampling is most useful when:', 'the population is hard to reach, such as users of a specialist product', ['the population is listed in a database', 'speed does not matter', 'every group must be equally represented'], 'Respondents refer others.'),
         ('A population is 60% female. In a stratified sample of 200, the number of females should be:', '120', ['60', '100', '140'], '60% × 200 = 120.'),
         ('Increasing the sample size usually:', 'reduces sampling error but raises cost', ['increases sampling error', 'removes all bias', 'reduces cost'], 'Bigger samples are more reliable but cost more.')],
  why=[('Explain why businesses use samples rather than surveying the whole population.', 'Surveying everyone is too costly and slow; a well-chosen sample gives reasonably accurate results at much lower cost.'),
       ('Explain why convenience sampling may give biased results.', 'People who are easy to reach, such as passers-by at one time and place, may not represent the whole target market, so their views can be skewed.'),
       ('Explain why quota sampling is popular with market research firms.', 'It is quicker and cheaper than random sampling, needs no full list of the population, and still ensures key groups are represented.')],
  contrast=[('quota sampling', 'stratified sampling', 'Both represent groups in set proportions, but in stratified sampling individuals in each group are chosen randomly, whereas in quota sampling the researcher chooses them, which can introduce bias.'),
            ('random sampling', 'convenience sampling', 'Random sampling gives every member an equal chance of selection and reduces bias; convenience sampling chooses whoever is easiest to reach, which is cheap but likely to be biased.')],
  misc=[('A larger sample always produces accurate results.', 'Size reduces random sampling error, but a biased method (e.g. surveying only one location) gives misleading results however large the sample.')],
  cases=[('the 1936 Literary Digest poll', 'The Literary Digest surveyed over 2 million people, mostly from car and telephone owner lists, and wrongly predicted that Roosevelt would lose the 1936 US election.', 'sampling bias', 'a huge but unrepresentative sample of wealthier people gave the wrong result'),
         ('opinion polling companies', 'Polling firms such as YouGov and Ipsos typically survey about 1,000-2,000 adults, weighted by age, gender, region and past voting.', 'quota and stratified sampling', 'representing groups in proportion allows a small sample to estimate national opinion'),
         ('research on rare-disease patients', 'Pharmaceutical firms researching treatments for rare diseases often recruit patients through patient support groups who refer other patients.', 'snowball sampling', 'referrals reach a small, hard-to-find population, though respondents may share similar views')],
  apply=[('A sports retailer has 3,000 customers: 1,800 aged under 30 and 1,200 aged 30 or over. Calculate a stratified sample of 150 and explain why stratified sampling suits this retailer.', 'Under 30: 1,800/3,000 × 150 = 90; 30 and over: 1,200/3,000 × 150 = 60. Stratified sampling ensures both age groups, who may have different tastes, are represented in proportion.', 4)],
  evaluate=[('Random sampling is always the best sampling method for a business.', ['every member has an equal chance', 'reduces selection bias', 'statistically valid'],
             ['needs a full list of the population', 'costly and slow', 'small groups may be missed', 'quota or stratified may be more practical'], 'Random sampling is the most valid in principle, but stratified or quota sampling is often more practical and representative for businesses with limited budgets.')],
  )


@calc('ch02-st4', 'C3', (1, 5))
def survey_stats(rng, slot):
    f_ = firm(rng)
    k = rng.choice([7, 9, 11])
    vals = sorted(rng.choice(range(2, 11)) for _ in range(k))
    rng.shuffle(vals)
    sv = sorted(vals)
    mean = sum(vals) / k
    med = sv[k // 2]
    counts = {v: sv.count(v) for v in sv}
    top = max(counts.values())
    modes = [v for v, n in counts.items() if n == top]
    rngv = sv[-1] - sv[0]
    mode_txt = (str(modes[0]) if len(modes) == 1 else ', '.join(map(str, modes[:-1])) + f' and {modes[-1]} (multimodal)') if top > 1 else 'none (every score appears once)'
    stem = f'{f_} asked {k} customers to rate a new product from 1 to 10. Scores: ' + ', '.join(map(str, vals)) + '. Calculate the mean, median, mode and range of the scores.'
    if slot.d >= 4:
        stem += ' Comment on what the results suggest and one limitation of this research.'
    ans = f'Mean = {sum(vals)}/{k} = {p2(mean)}; median = {med}; mode = {mode_txt}; range = {sv[-1]} − {sv[0]} = {rngv}.'
    if slot.d >= 4:
        ans += (' The average rating is ' + ('positive' if mean >= 6 else 'mixed') + f', but a range of {rngv} shows opinions vary. Limitation: a sample of {k} is too small to be reliable, and the respondents may not represent the target market.')
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'ordered: {", ".join(map(str, sv))}; mean = total/number; median = middle value; mode = most frequent; range = highest − lowest.', 'all four statistics') + (' [1] comment; [1] limitation.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch02-st4', concepts=('change', 'ethics'),
  terms=[('qualitative research', 'research that collects non-numerical data about opinions, attitudes and motives, often through interviews and focus groups'),
         ('quantitative research', 'research that collects numerical data that can be analysed statistically, often through questionnaires and sales data'),
         ('mean', 'the arithmetic average: the sum of values divided by the number of values'),
         ('median', 'the middle value when data is arranged in order'),
         ('mode', 'the value that occurs most often in a data set'),
         ('range', 'the difference between the highest and lowest values in a data set')],
  facts=[('Which is an example of qualitative data?', 'Customers\' comments on why they like a brand', ['The number of units sold', 'The average price paid', 'The percentage of repeat customers'], 'Qualitative data is non-numerical.'),
         ('For the data 2, 3, 3, 6, 11 the median is:', '3', ['5', '6', '11'], 'The middle value of the ordered list.'),
         ('For the data 2, 3, 3, 6, 11 the mean is:', '5', ['3', '6', '25'], '25/5 = 5.'),
         ('Which measure is least affected by one extreme value?', 'The median', ['The mean', 'The range', 'The total'], 'The median depends only on the middle value.')],
  why=[('Explain why businesses use both qualitative and quantitative research.', 'Quantitative data shows how many customers think or do something and allows comparisons; qualitative data explains why, giving depth that helps design products and messages.'),
       ('Explain why the mean may give a misleading picture of survey results.', 'Extreme values pull the mean up or down, so it may not represent a typical respondent; the median or mode may be better.'),
       ('Explain why research results should be interpreted with caution.', 'Samples may be small or biased, questions may be leading, and stated intentions often differ from actual behaviour.')],
  contrast=[('qualitative research', 'quantitative research', 'Qualitative research collects in-depth views and reasons from small groups; quantitative research collects numerical data from larger samples that can be analysed statistically.'),
            ('the mean', 'the median', 'The mean is the arithmetic average of all values and is affected by extreme values; the median is the middle value and is not affected by extremes.')],
  misc=[('Quantitative research is always more reliable than qualitative research.', 'Numbers can come from biased samples or poor questions; qualitative research can reveal motives that numbers miss.')],
  cases=[('IKEA\'s home visits', 'IKEA researchers visit customers\' homes around the world to observe how people actually live, cook and store things.', 'qualitative research', 'in-depth observation reveals needs and habits that questionnaires would not capture'),
         ('Amazon\'s star ratings', 'Amazon shows an average star rating for each product alongside the distribution of 1-5 star reviews.', 'interpreting quantitative data', 'the mean alone can hide polarised opinions, so the distribution and written reviews add meaning'),
         ('Spotify Wrapped', 'Each December Spotify\'s "Wrapped" campaign uses listeners\' quantitative streaming data to create personalised summaries that users share on social media.', 'quantitative data in marketing', 'large-scale usage data supports both personalised products and viral promotion')],
  apply=[('A survey of 10 customers gave satisfaction scores of 9, 9, 8, 8, 8, 7, 7, 6, 2, 1. Calculate the mean and median, and explain which better represents typical satisfaction.', 'Mean = 65/10 = 6.5; median = (8 + 7)/2 = 7.5. The median better represents typical satisfaction because two very low scores pull the mean down.', 4)],
  evaluate=[('Quantitative research is more useful than qualitative research for making marketing decisions.', ['measurable and comparable', 'larger samples', 'statistical analysis'],
             ['does not explain why customers behave as they do', 'depends on good question design', 'qualitative insight drives creative ideas (IKEA)', 'both are complementary'], 'Quantitative data is essential for sizing markets and tracking performance, but qualitative insight is needed to understand motives; the best decisions combine both.')],
  )


# =============================================================================================
# ch03 The 7Ps: product and price
# =============================================================================================
@calc('ch03-st1', 'C3', (2, 5))
def bcg_calc(rng, slot):
    c = cur(rng)
    prods = rng.sample(['Alpha', 'Bravo', 'Cosmo', 'Delta', 'Echo', 'Fusion'], 3)
    rows = []
    for p_ in prods:
        own = rng.choice([10, 20, 30, 40, 60])
        lead = rng.choice([20, 30, 40, 50])
        if own == lead:
            lead += 10
        g = rng.choice([1, 2, 3, 8, 12, 15])
        rms = own / lead
        quad = ('star' if g >= 8 else 'cash cow') if rms >= 1 else ('question mark' if g >= 8 else 'dog')
        rows.append((p_, own, lead, g, rms, quad))
    tab = '; '.join(f'{p_}: sales {m(o, c)} m, largest rival {m(l, c)} m, market growth {g}%' for p_, o, l, g, _, _ in rows)
    stem = f'A firm has three products: {tab}. Calculate the relative market share of each product and place it in the Boston Consulting Group matrix (high growth = 8% or more).'
    if slot.d >= 4:
        stem += ' Recommend a strategy for one of the products.'
    ans = '; '.join(f'{p_}: {p2(r)} → {q}' for p_, _, _, _, r, q in rows) + '.'
    if slot.d >= 4:
        ans += ' For example, use cash cows to fund question marks with good prospects, invest to build stars, and divest or harvest dogs.'
    return dict(stem=stem, answer=ans,
                markingKey=MK('relative market share = own sales / largest rival\'s sales; share ≥ 1 is high.', 'all three ratios and quadrants') + (' [1][1] justified strategy.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch03-st1', concepts=('change', 'creativity', 'sustainability'),
  terms=[('product life cycle', 'the stages a product goes through from its launch to its withdrawal: research and development, launch (introduction), growth, maturity, decline'),
         ('extension strategy', 'a method used to extend the maturity stage of a product\'s life cycle, such as new features, new markets or repackaging'),
         ('Boston Consulting Group (BCG) matrix', 'a tool that classifies a firm\'s products by market growth and relative market share into stars, cash cows, question marks and dogs'),
         ('cash cow', 'a product with a high market share in a low-growth market, which generates strong cash flow'),
         ('star', 'a product with a high market share in a high-growth market'),
         ('question mark (problem child)', 'a product with a low market share in a high-growth market'),
         ('dog', 'a product with a low market share in a low-growth market'),
         ('product portfolio', 'the range of products a business sells')],
  facts=[('In the BCG matrix, a product with high share of a low-growth market is a:', 'cash cow', ['star', 'question mark', 'dog'], 'High share, low growth.'),
         ('Cash flow is usually negative during which stage of the product life cycle?', 'Introduction (launch)', ['Maturity', 'Decline only', 'Growth after saturation'], 'Development and launch costs exceed early sales.'),
         ('Which is an extension strategy?', 'Selling the product in a new market overseas', ['Withdrawing the product', 'Raising the price and cutting promotion', 'Closing production'], 'New markets extend maturity.'),
         ('Coca-Cola Zero Sugar and new flavours are examples of:', 'extension strategies for a mature product', ['products in the research stage', 'loss leaders', 'dogs'], 'Variants extend the life of a mature brand.')],
  why=[('Explain why a firm needs a balanced product portfolio.', 'Cash cows generate cash to fund stars and question marks, while new products are needed to replace those that decline, spreading risk and sustaining profits over time.'),
       ('Explain why the product life cycle may be difficult to use for planning.', 'It is hard to know which stage a product is in or how long each stage will last, and life cycles vary widely between products.'),
       ('Explain why cash flow is usually strongest in the maturity stage.', 'Sales are high, development costs have been recovered and promotion can be reduced, so inflows greatly exceed outflows.')],
  contrast=[('a star', 'a cash cow', 'Both have high market share, but a star is in a high-growth market and needs investment, while a cash cow is in a low-growth market and generates surplus cash.'),
            ('the product life cycle', 'the BCG matrix', 'The product life cycle tracks sales of one product over time; the BCG matrix analyses a firm\'s whole portfolio by market growth and relative market share at one point in time.')],
  misc=[('A dog should always be withdrawn immediately.', 'A dog may still make a profit, support other products or serve loyal customers; managers may harvest it rather than withdraw it.')],
  cases=[('the iPod\'s life cycle', 'Apple launched the iPod in 2001; sales peaked at about 55 million units in 2008 and fell as smartphones took over, and the last model was withdrawn in 2022.', 'the product life cycle', 'a product that dominated its market declined as a new technology replaced it'),
         ('Lucozade\'s repositioning', 'Lucozade was sold for decades as a drink for people recovering from illness before being relaunched in the 1980s as a sports energy drink.', 'extension strategies', 'repositioning to a new target market extended the brand\'s life cycle'),
         ('Microsoft\'s product portfolio', 'Microsoft\'s Office and Windows generate large, steady cash flows, which helped fund investment in its Azure cloud services and AI.', 'the BCG matrix', 'cash cows funded stars and question marks in high-growth markets')],
  apply=[('A soft-drinks firm\'s best-selling cola is in the maturity stage. Suggest two extension strategies and explain one risk of each.', 'New flavours or a sugar-free version (risk: cannibalises sales of the original); entering new overseas markets (risk: cultural differences and high entry costs); new packaging (risk: costs may not be recovered).', 4)],
  evaluate=[('The BCG matrix is a reliable guide to product portfolio decisions.', ['simple visual overview', 'shows cash flow needs', 'encourages balance'],
             ['market share does not always mean profit', 'growth thresholds are arbitrary', 'ignores links between products', 'dogs may still be profitable'], 'The BCG matrix is a useful starting point, but decisions also need profit data, market research and strategic judgement.')],
  )

S('ch03-st2', concepts=('creativity', 'ethics'),
  terms=[('brand', 'a name, symbol, design or combination of these that identifies a product and distinguishes it from rivals'),
         ('brand awareness', 'the extent to which customers recognise or recall a brand'),
         ('brand development', 'the process of building and strengthening a brand\'s identity and position over time'),
         ('brand loyalty', 'the tendency of customers to keep buying the same brand rather than switching to rivals'),
         ('brand value', 'the financial and emotional worth of a brand, based on how much more customers will pay for it than for an unbranded equivalent'),
         ('own-label (private label) brand', 'a product sold under a retailer\'s own brand name, such as a supermarket\'s range')],
  facts=[('Which is a benefit of strong brand loyalty?', 'Demand becomes less price elastic, allowing higher prices', ['Costs of production fall to zero', 'Competitors are banned', 'Promotion is never needed'], 'Loyal customers are less price sensitive.'),
         ('Which company was valued as the world\'s most valuable brand in Interbrand\'s rankings for 2013-2024?', 'Apple', ['Nokia', 'Kodak', 'Blockbuster'], 'Apple\'s brand value exceeded $480 bn in 2024.'),
         ('Brand awareness can be increased mainly through:', 'promotion such as advertising and sponsorship', ['lower production costs', 'reducing distribution', 'cutting product range'], 'Exposure builds recognition.')],
  why=[('Explain why a strong brand can create a barrier to entry.', 'Loyal customers are reluctant to switch, so new entrants must spend heavily on promotion to win them, raising the cost and risk of entering the market.'),
       ('Explain why brand reputation can be damaged quickly.', 'Social media spreads news of scandals, poor quality or unethical behaviour rapidly, so trust built over years can be lost in days.'),
       ('Explain why supermarkets develop their own-label brands.', 'Own-label products earn higher margins, compete with manufacturers\' brands on price, and build loyalty to the store.')],
  contrast=[('brand awareness', 'brand loyalty', 'Brand awareness is whether customers recognise a brand; brand loyalty is whether they keep choosing it over rivals.'),
            ('a manufacturer\'s brand', 'an own-label brand', 'A manufacturer\'s brand (e.g. Heinz) is sold through many retailers; an own-label brand is created and sold only by one retailer, usually at a lower price.')],
  misc=[('A well-known brand always has loyal customers.', 'Awareness does not mean loyalty; customers may know a brand but prefer rivals or switch for lower prices.')],
  cases=[('Volkswagen\'s emissions scandal', 'In 2015 Volkswagen admitted fitting software to about 11 million diesel cars to cheat emissions tests, costing it over $30 bn in fines and settlements.', 'brand value and ethics', 'unethical behaviour damaged trust and brand value, showing that brands depend on reputation'),
         ('Nike\'s "Just Do It" campaign', 'Nike\'s 2018 campaign featuring Colin Kaepernick was criticised by some customers but was followed by a rise in online sales.', 'brand development', 'taking a clear values-based position strengthened loyalty among Nike\'s core young target market'),
         ('Aldi\'s own-label strategy', 'Around 90% of the products Aldi sells are own-label brands, often designed to look similar to leading brands.', 'own-label brands', 'own brands support low prices and high margins, although lookalike packaging has led to legal disputes')],
  apply=[('A local juice company wants to build brand loyalty. Suggest two methods and explain how each would work.', 'A loyalty scheme (rewards repeat purchases); consistent quality and packaging (builds trust); social media engagement and storytelling about local ingredients (emotional connection).', 4)],
  evaluate=[('Building a strong brand is the most important marketing objective for a business.', ['premium prices', 'loyalty and barriers to entry', 'easier to launch new products'],
             ['brands take time and money to build', 'reputation can be lost quickly', 'small firms may compete on price or service', 'product quality matters more'], 'A strong brand is very valuable, but it must be backed by good products and ethical behaviour, and some firms compete successfully without one.')],
  )


@calc('ch03-st3', 'C3', (1, 5))
def cost_plus(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    vc = rng.choice([6, 8, 10, 12, 15, 20])
    fc = rng.choice([20_000, 30_000, 40_000, 60_000])
    q = rng.choice([2_000, 4_000, 5_000, 8_000])
    mu = rng.choice([20, 25, 40, 50, 60])
    uc = vc + fc / q
    price = uc * (1 + mu / 100)
    if slot.d <= 2:
        return dict(stem=f'A product costs {m(uc, c)} per unit to make. {f_} uses cost-plus pricing with a mark-up of {mu}%. Calculate the selling price.',
                    answer=m(round(price, 2), c), markingKey=MK(f'{p2(uc)} × {1 + mu / 100:g} = {p2(price)}.', m(round(price, 2), c)), marks=2)
    margin = 100 * (price - uc) / price
    stem = (f'{f_} has fixed costs of {m(fc, c)} a month and variable costs of {m(vc, c)} per unit, and expects to sell {q:,} units a month. '
            f'It uses cost-plus pricing with a {mu}% mark-up on unit cost. Calculate the unit cost, the selling price and the profit margin as a percentage of price.')
    if slot.d >= 4:
        stem += ' Explain one limitation of cost-plus pricing.'
    ans = f'Unit cost = {m(vc, c)} + {m(fc, c)}/{q:,} = {m(round(uc, 2), c)}; price = {m(round(price, 2), c)}; margin = {p1(margin)}% of price.'
    if slot.d >= 4:
        ans += ' Limitation: it ignores demand and competitors\' prices; if sales are lower than expected the unit cost rises and the price may be uncompetitive.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{vc} + {fc:,}/{q:,} = {p2(uc)}; × {1 + mu / 100:g} = {p2(price)}; ({p2(price)} − {p2(uc)})/{p2(price)} × 100 = {p1(margin)}%.', 'unit cost, price and margin') + (' [1][1] limitation explained.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch03-st3', concepts=('ethics', 'creativity', 'change'),
  terms=[('cost-plus pricing', 'setting a price by adding a percentage mark-up to the unit cost of a product'),
         ('penetration pricing', 'setting a low price when entering a market to win market share quickly, then raising it later'),
         ('price skimming', 'setting a high price for a new, innovative product to maximise revenue from early adopters, then lowering it over time'),
         ('psychological pricing', 'setting prices that seem lower or more attractive to customers, such as $9.99 instead of $10'),
         ('loss leader', 'a product sold below cost to attract customers who will buy other, profitable products'),
         ('price discrimination', 'charging different prices to different customer groups for the same product, such as peak and off-peak fares'),
         ('dynamic pricing', 'changing prices frequently, often automatically, in response to real-time demand and supply')],
  facts=[('A new games console launched at a high price that falls over time is an example of:', 'price skimming', ['penetration pricing', 'loss leader pricing', 'cost-plus pricing'], 'High initial price for early adopters.'),
         ('A unit cost of $40 with a 25% mark-up gives a price of:', '$50', ['$65', '$45', '$32'], '$40 × 1.25 = $50.'),
         ('Uber\'s "surge pricing" during busy periods is an example of:', 'dynamic pricing', ['loss leader pricing', 'cost-plus pricing', 'psychological pricing'], 'Prices rise automatically with demand.'),
         ('Cheaper cinema tickets for students are an example of:', 'price discrimination', ['price skimming', 'penetration pricing', 'cost-plus pricing'], 'Different prices for different groups.')],
  why=[('Explain why penetration pricing may be used when entering a competitive market.', 'A low price attracts customers away from established rivals, builds market share quickly and can create economies of scale, after which the price can be raised.'),
       ('Explain why price skimming suits innovative technology products.', 'Early adopters will pay a premium for new technology, so a high price recovers R&D costs quickly before competitors launch similar products.'),
       ('Explain why supermarkets use loss leaders.', 'Selling popular items below cost attracts shoppers into the store, where they also buy other products with higher margins.')],
  contrast=[('penetration pricing', 'price skimming', 'Penetration pricing starts low to win market share quickly; price skimming starts high to earn high margins from early adopters before lowering the price.'),
            ('cost-plus pricing', 'dynamic pricing', 'Cost-plus pricing adds a fixed mark-up to unit cost and ignores demand; dynamic pricing changes prices continuously in response to demand and supply.')],
  misc=[('Cost-plus pricing guarantees a profit.', 'It only gives a profit if forecast sales are achieved; if sales fall, unit costs rise and the price may not cover them, and customers may reject the price.')],
  cases=[('Apple\'s iPhone pricing', 'The original iPhone launched in 2007 at $599; Apple cut the price to $399 after about two months, angering some early buyers.', 'price skimming', 'a high launch price captured early adopters before the price was lowered to reach a wider market'),
         ('Netflix\'s entry into India', 'In 2021 Netflix cut prices in India by up to 60%, including a mobile-only plan, to compete with Disney+ Hotstar and Amazon Prime Video.', 'penetration pricing', 'lower prices were used to win subscribers in a price-sensitive, highly competitive market'),
         ('Costco\'s $1.50 hot dog', 'Costco has sold its hot dog and soda combo for $1.50 since 1985, despite rising costs.', 'loss leader pricing', 'a famous low-price item attracts members and builds loyalty, while profits come from membership fees and other products')],
  apply=[('A new streaming service is entering a market dominated by Netflix and Disney+. Recommend a pricing strategy and justify your answer.', 'Penetration pricing (or a free trial): a low introductory price attracts subscribers from established rivals and builds market share, and prices can rise once content and loyalty are established. Risks: low early revenue and customers may leave when prices rise.', 4)],
  evaluate=[('Dynamic pricing is unethical.', ['can exploit customers at times of need (e.g. surge pricing in emergencies)', 'lack of transparency', 'can damage trust'],
             ['matches supply and demand efficiently', 'lower prices at quiet times', 'widely accepted in airlines and hotels', 'can be limited by caps and clear communication'], 'Dynamic pricing is not unethical in itself, but it becomes unethical when it exploits vulnerable customers or is hidden; firms should be transparent and set limits.')],
  )


# =============================================================================================
# ch04 The 7Ps: promotion and place
# =============================================================================================
@calc('ch04-st1', 'C3', (1, 5))
def campaign_roi(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    spend = rng.choice([5_000, 8_000, 10_000, 20_000, 25_000])
    clicks = rng.choice([4_000, 5_000, 8_000, 10_000, 20_000])
    conv = rng.choice([2, 2.5, 4, 5])
    aov = rng.choice([40, 50, 60, 80])
    gm = rng.choice([30, 40, 50])
    cpc = spend / clicks
    sales_n = clicks * conv / 100
    cpa = spend / sales_n
    rev = sales_n * aov
    gp = rev * gm / 100
    roi = 100 * (gp - spend) / spend
    if slot.d <= 2:
        return dict(stem=f'{f_} spent {m(spend, c)} on a social media campaign that produced {clicks:,} clicks. Calculate the cost per click.',
                    answer=f'{c}{p2(cpc)} per click', markingKey=MK(f'{spend:,}/{clicks:,} = {p2(cpc)}.', f'{c}{p2(cpc)}'), marks=2)
    stem = (f'{f_} spent {m(spend, c)} on an online campaign that produced {clicks:,} clicks; {conv:g}% of clicks led to a purchase, with an average order value of {m(aov, c)} '
            f'and a gross margin of {gm}%. Calculate the cost per click, the number of sales, the cost per sale (acquisition) and the return on the campaign (gross profit − spend as a % of spend).')
    if slot.d >= 4:
        stem += ' Comment on whether the campaign was worthwhile.'
    ans = (f'Cost per click = {c}{p2(cpc)}; sales = {sales_n:,.0f}; cost per sale = {c}{p2(cpa)}; revenue = {m(rev, c)}, gross profit = {m(gp, c)}; '
           f'return = ({m(gp, c)} − {m(spend, c)})/{m(spend, c)} × 100 = {p1(roi)}%.')
    if slot.d >= 4:
        ans += (' The campaign more than covered its cost in gross profit' if roi > 0 else ' The campaign did not cover its cost from gross profit on first orders') + ', but repeat purchases and brand awareness should also be considered.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{spend:,}/{clicks:,}; {clicks:,} × {conv:g}% = {sales_n:,.0f}; {spend:,}/{sales_n:,.0f}; {sales_n:,.0f} × {aov} × {gm}% = {gp:,.0f}; ({gp:,.0f} − {spend:,})/{spend:,} × 100.', 'all values') + (' [1] judgement.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch04-st1', concepts=('creativity', 'ethics', 'change'),
  terms=[('promotion', 'communication with customers to inform, persuade and remind them about a product or brand'),
         ('above-the-line promotion', 'paid-for promotion through independent mass media such as television, radio, cinema, print and online display advertising'),
         ('below-the-line promotion', 'promotion that the business controls directly, not through mass media, such as sales promotions, direct marketing, sponsorship and public relations'),
         ('promotional mix', 'the combination of promotional methods a business uses to communicate with its target market'),
         ('social media marketing', 'the use of platforms such as Instagram, TikTok and YouTube to promote products and interact with customers'),
         ('influencer marketing', 'paying or partnering with people who have large online followings to promote products')],
  facts=[('Which is an example of below-the-line promotion?', 'A buy-one-get-one-free offer in store', ['A television advert', 'A billboard campaign', 'A radio advert'], 'Sales promotions are below the line.'),
         ('An advantage of social media marketing is that it:', 'allows precise targeting and two-way interaction with customers', ['guarantees positive comments', 'costs nothing to manage', 'reaches only older consumers'], 'Platforms target by interests and allow engagement.'),
         ('UK and EU rules require influencers to label paid posts, for example with "#ad", because:', 'consumers should know when content is advertising', ['it increases the price of products', 'it is required for all personal photos', 'it removes the need for consent'], 'Hidden advertising misleads consumers.')],
  why=[('Explain why firms use a promotional mix rather than one method.', 'Different methods reach different audiences and objectives: mass media builds awareness, sales promotions trigger purchases and PR builds reputation, so combining them is more effective.'),
       ('Explain why social media marketing has grown in importance.', 'Customers, especially younger ones, spend more time online; social media allows targeted, measurable, low-cost campaigns and sharing that can make content go viral.'),
       ('Explain why social media can also be a risk for a brand.', 'Negative comments, complaints and mistakes spread quickly and publicly, and firms cannot control what users post.')],
  contrast=[('above-the-line promotion', 'below-the-line promotion', 'Above-the-line promotion uses paid mass media to reach a wide audience; below-the-line promotion uses methods controlled by the firm, such as sales promotions and direct marketing, to target specific customers.')],
  misc=[('Social media marketing is free.', 'Accounts are free, but content creation, staff time, paid advertising and influencer fees can be very expensive.')],
  cases=[('Duolingo\'s TikTok account', 'Language app Duolingo built over 10 million TikTok followers with humorous videos featuring its green owl mascot.', 'social media marketing', 'low-cost, entertaining content increased brand awareness among young users'),
         ('Red Bull\'s Stratos jump', 'In 2012 Red Bull sponsored Felix Baumgartner\'s jump from 39 km, watched live by over 8 million people on YouTube.', 'below-the-line promotion and sponsorship', 'an extreme event matched the brand\'s image and generated worldwide publicity'),
         ('the Super Bowl advertisements', 'A 30-second advertisement during the 2024 Super Bowl cost about $7 million and reached over 120 million US viewers.', 'above-the-line promotion', 'mass media reaches huge audiences at a high total cost, so it suits large brands with mass-market products')],
  apply=[('A new vegan snack brand has a small budget and targets 18-30-year-olds. Recommend a promotional mix and justify your choice.', 'Mainly social media and influencer marketing on Instagram and TikTok (cheap, targeted at young users, shareable), supported by free samples at gyms and universities (below the line, encourages trial). Television would be too costly and poorly targeted.', 4)],
  evaluate=[('Social media marketing has made traditional above-the-line advertising unnecessary.', ['precise targeting', 'lower cost', 'measurable', 'two-way engagement'],
             ['TV still reaches mass audiences at once', 'older consumers use less social media', 'risk of negative publicity', 'ad fatigue and declining organic reach'], 'Social media is now central to most promotional mixes, but above-the-line media remains effective for mass-market brands; the right mix depends on the target market.')],
  )

S('ch04-st2', concepts=('creativity', 'ethics'),
  terms=[('guerrilla marketing', 'unconventional, low-cost promotional methods that surprise people and generate word of mouth, such as street art or stunts'),
         ('viral marketing', 'promotion designed to be shared rapidly by people online, spreading the message at little cost'),
         ('digital marketing', 'the use of digital channels such as search engines, email, websites, apps and social media to promote products'),
         ('search engine optimisation (SEO)', 'improving a website so that it appears higher in unpaid search engine results'),
         ('ambush marketing', 'a brand linking itself to a major event without paying to be an official sponsor')],
  facts=[('Which is an example of guerrilla marketing?', 'Painting eye-catching artwork on pavements in a city centre', ['A national TV advert', 'A newspaper advert', 'A price list'], 'Unconventional, low-cost and surprising.'),
         ('A key advantage of digital marketing is that results can be:', 'measured precisely, e.g. through clicks and conversions', ['ignored', 'kept secret from managers', 'guaranteed in advance'], 'Analytics track performance.'),
         ('A risk of guerrilla marketing is that it may:', 'offend people or break local laws', ['be too expensive for small firms', 'reach no one', 'require a TV slot'], 'Stunts can backfire.')],
  why=[('Explain why guerrilla marketing suits small businesses.', 'It costs little, relies on creativity rather than large budgets, and can generate free publicity through social media and word of mouth.'),
       ('Explain why digital technology has changed promotion.', 'It allows targeted adverts based on user data, instant measurement of results, two-way interaction and the ability to change campaigns quickly.'),
       ('Explain why some guerrilla campaigns create ethical concerns.', 'They may mislead the public, cause fear or disruption, invade privacy or damage public property.')],
  contrast=[('guerrilla marketing', 'traditional mass media advertising', 'Guerrilla marketing is unconventional, low-cost and relies on surprise and sharing; traditional mass media advertising pays for planned exposure through TV, radio or print.')],
  misc=[('Guerrilla marketing always works because it is cheap.', 'Low cost does not guarantee impact; many stunts are ignored, and some backfire and damage the brand.')],
  cases=[('Boston\'s 2007 Aqua Teen Hunger Force scare', 'In 2007 light-up devices placed around Boston to promote a cartoon were mistaken for bombs, closing bridges; Turner Broadcasting paid $2 m in compensation.', 'risks of guerrilla marketing', 'an unconventional stunt caused public alarm and costs, damaging the brand'),
         ('the ALS Ice Bucket Challenge', 'In 2014 the Ice Bucket Challenge spread on social media and raised over $115 m for the ALS Association in the US in about eight weeks.', 'viral marketing', 'shareable, participatory content spread a message worldwide at almost no cost'),
         ('Beats by Dre at the 2012 Olympics', 'Beats gave free headphones to athletes, who wore them on camera at the London 2012 Olympics, even though Beats was not an official sponsor.', 'ambush marketing', 'the brand gained global exposure without paying sponsorship fees, despite restrictions')],
  apply=[('A new independent bookshop has a promotion budget of only $500. Suggest one guerrilla marketing idea and one digital marketing method, and explain how each would help.', 'Guerrilla: leaving free "mystery books" with the shop\'s label on park benches, encouraging people to share photos (low cost, word of mouth). Digital: a local SEO-optimised website and Google Business listing so local searches find the shop.', 4)],
  evaluate=[('Guerrilla marketing is more effective than traditional promotion.', ['low cost', 'memorable and shareable', 'suits creative brands'],
             ['unpredictable reach', 'may offend or break laws', 'hard to measure', 'mass media gives reliable reach'], 'Guerrilla marketing can be highly effective for awareness at low cost, but it is risky and works best as part of a wider promotional mix.')],
  )


@calc('ch04-st3', 'C3', (2, 5))
def channel_markup(rng, slot):
    c = cur(rng)
    cost = rng.choice([4, 5, 8, 10, 12, 20])
    mm = rng.choice([25, 40, 50])
    wm = rng.choice([10, 15, 20, 25])
    rm = rng.choice([30, 40, 50, 60])
    pm = cost * (1 + mm / 100)
    pw = pm * (1 + wm / 100)
    pr = pw * (1 + rm / 100)
    direct = rng.choice([0.8, 0.85, 0.9])
    stem = (f'A manufacturer makes a product for {m(cost, c)} and adds a {mm}% mark-up when selling to a wholesaler. The wholesaler adds {wm}% and the retailer adds {rm}%. '
            'Calculate the price at each stage of the distribution channel and the final retail price.')
    ans = f'Manufacturer → wholesaler: {c}{p2(pm)}; wholesaler → retailer: {c}{p2(pw)}; retail price: {c}{p2(pr)}.'
    if slot.d >= 4:
        dp = pr * direct
        stem += f' If the manufacturer sold directly online at {int(direct * 100)}% of the retail price, calculate its profit per unit and compare it with selling through intermediaries.'
        ans += f' Direct price = {c}{p2(dp)}; profit = {c}{p2(dp - cost)} per unit compared with {c}{p2(pm - cost)} through intermediaries, but it must pay for delivery, storage, its website and marketing.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{cost} × {1 + mm / 100:g} = {p2(pm)}; × {1 + wm / 100:g} = {p2(pw)}; × {1 + rm / 100:g} = {p2(pr)}.', 'each price') + (' [1][1] comparison including extra costs of direct selling.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch04-st3', concepts=('change', 'sustainability'),
  terms=[('place (distribution)', 'how a product gets from the producer to the customer, including channels, intermediaries and logistics'),
         ('distribution channel', 'the route a product takes from producer to final consumer'),
         ('intermediary', 'a business, such as a wholesaler, retailer or agent, that helps move products from producer to consumer'),
         ('wholesaler', 'an intermediary that buys in bulk from producers and sells in smaller quantities to retailers'),
         ('e-commerce', 'the buying and selling of goods and services over the internet'),
         ('direct-to-consumer (D2C)', 'a channel in which the producer sells directly to the final customer, usually online, without intermediaries'),
         ('omnichannel retailing', 'integrating physical stores, websites, apps and social media so customers can shop seamlessly across them')],
  facts=[('A zero-level (direct) channel is:', 'producer → consumer', ['producer → wholesaler → retailer → consumer', 'producer → retailer → consumer', 'producer → agent → wholesaler → consumer'], 'No intermediaries.'),
         ('Which is a benefit of using a wholesaler?', 'It breaks bulk and distributes to many small retailers', ['It increases the manufacturer\'s margin per unit', 'It removes all transport costs', 'It guarantees the lowest retail price'], 'Wholesalers spread products widely.'),
         ('Which is a limitation of e-commerce for customers?', 'They cannot touch or try products before buying', ['Prices are always higher', 'It is only open during office hours', 'There is less choice'], 'Lack of physical inspection is a drawback.')],
  why=[('Explain why many producers use intermediaries rather than selling directly.', 'Intermediaries already have distribution networks, storage and customer reach, so producers save on logistics and reach more customers, although they give up some margin.'),
       ('Explain why e-commerce has changed distribution strategies.', 'Producers can reach customers directly anywhere, cut out intermediaries, collect customer data and offer home delivery, forcing traditional retailers to adapt.'),
       ('Explain why direct-to-consumer brands may still sell through retailers.', 'Retailers provide wider reach, physical display and impulse purchases, and online customer acquisition costs have risen.')],
  contrast=[('a direct channel', 'an indirect channel', 'In a direct channel the producer sells straight to consumers and keeps all the margin; in an indirect channel intermediaries such as wholesalers and retailers distribute the product and take part of the margin.'),
            ('e-commerce', 'omnichannel retailing', 'E-commerce is selling online; omnichannel retailing integrates online and physical channels so customers can, for example, order online and collect in store.')],
  misc=[('Cutting out intermediaries always lowers the price for consumers.', 'The producer must then pay for storage, delivery and marketing itself, so costs may rise and prices may not fall.')],
  cases=[('Nike\'s direct-to-consumer strategy', 'From 2017 Nike cut many wholesale partners to sell directly through its own stores and app, but from 2023 it began rebuilding relationships with retailers such as Foot Locker.', 'distribution channels', 'selling direct raised margins and data, but losing retail shelf space helped rivals such as On and Hoka win customers'),
         ('Amazon\'s fulfilment network', 'Amazon operates hundreds of fulfilment centres worldwide, offering next-day or same-day delivery to Prime members.', 'e-commerce and logistics', 'a vast logistics network turns fast delivery into a competitive advantage'),
         ('Warby Parker\'s stores', 'Online glasses retailer Warby Parker, founded in 2010, opened over 250 physical stores in the US by 2024.', 'omnichannel retailing', 'physical stores let customers try products, complementing the online channel')],
  apply=[('A craft brewery sells through supermarkets. It is considering selling directly online. Explain one advantage and one disadvantage of this change.', 'Advantage: higher margin per unit and direct customer data/relationships. Disadvantage: costs of delivery, packaging and website, and lower reach than supermarkets; legal restrictions on alcohol delivery.', 4)],
  evaluate=[('E-commerce will make physical retail stores obsolete.', ['convenience and choice', 'lower overheads', 'data-driven personalisation'],
             ['customers want to see and try products', 'stores support brand experience', 'returns and delivery costs', 'omnichannel models combine both'], 'E-commerce will keep growing, but physical stores are likely to remain as part of omnichannel strategies rather than disappear.')],
  )


# =============================================================================================
# ch05 The 7Ps: people, processes and physical evidence
# =============================================================================================
S('ch05-st1', concepts=('ethics', 'change'),
  terms=[('people (marketing mix)', 'the employees who deliver a service and interact with customers, whose skills and attitudes shape the customer experience'),
         ('customer service', 'the support and assistance a business gives to customers before, during and after a purchase'),
         ('customer relationship management (CRM)', 'the strategies and systems used to build long-term relationships with customers'),
         ('customer loyalty', 'the willingness of customers to keep buying from the same business'),
         ('employee empowerment', 'giving employees the authority to make decisions, for example to solve customer problems')],
  facts=[('Why is "people" especially important in marketing services?', 'Services are delivered by staff at the point of consumption, so staff behaviour forms the product', ['Services can be stored', 'Staff never meet customers', 'It reduces price elasticity to zero'], 'Inseparability of services.'),
         ('Which is most likely to improve customer service in a hotel?', 'Training staff in communication and problem-solving', ['Cutting staff numbers sharply', 'Removing complaint procedures', 'Using untrained temporary staff only'], 'Training improves service quality.'),
         ('Singapore Airlines is known for:', 'extensive training of cabin crew in customer service', ['having no cabin crew', 'standing-room flights', 'refusing all complaints'], 'Its "Singapore Girl" service standard relies on training.')],
  why=[('Explain why training customer-facing staff can increase sales.', 'Well-trained staff give advice, solve problems and create positive experiences, encouraging repeat purchases, recommendations and higher spending.'),
       ('Explain why poor customer service can damage a business quickly.', 'Unhappy customers post reviews and complaints online, which deter potential customers and harm the brand.'),
       ('Explain why empowering frontline staff can improve customer service.', 'Staff can solve problems immediately without waiting for managers, making customers feel valued and staff more motivated.')],
  contrast=[('customer service', 'customer relationship management', 'Customer service is the help given during each interaction; CRM is the long-term strategy and systems for building relationships and loyalty across many interactions.')],
  misc=[('Customer service only matters for luxury businesses.', 'All businesses benefit; even low-cost firms lose customers when service is poor, and service can differentiate firms in competitive markets.')],
  cases=[('Zappos\' customer service culture', 'Online shoe retailer Zappos lets call-centre staff spend as long as needed with customers; one call famously lasted over 10 hours.', 'people in the marketing mix', 'empowered, customer-focused staff built loyalty and word-of-mouth publicity'),
         ('Pret A Manger\'s staff culture', 'Pret A Manger recruits staff partly on attitude and allows employees to give away a few free drinks or snacks to customers they choose.', 'customer service and empowerment', 'small acts of discretion create a friendly service image and motivate staff'),
         ('Southwest Airlines', 'Southwest Airlines has long put employees first, believing that happy employees deliver better customer service.', 'the role of employees in customer service', 'staff culture became part of the brand and supported customer loyalty')],
  apply=[('A mobile phone shop receives poor online reviews about rude staff. Recommend two actions management could take and justify them.', 'Customer service training (improves skills and attitudes) and introducing feedback-linked rewards or empowerment to resolve complaints (motivates staff to serve well). Monitoring reviews and responding publicly shows customers the firm cares.', 4)],
  evaluate=[('Investing in staff training is the most effective way to improve customer loyalty.', ['staff deliver the service', 'better problem-solving', 'motivated staff'],
             ['training costs and staff turnover', 'price and product quality also matter', 'loyalty schemes and CRM systems', 'processes and physical evidence'], 'Training is vital in service businesses, but loyalty also depends on product, price and processes, so it should be one part of a coherent mix.')],
  )


@calc('ch05-st2', 'C3', (2, 5))
def service_capacity(rng, slot):
    f_ = rng.choice(['A coffee shop', 'A bank branch', 'A car wash', 'A passport office', 'A fast-food restaurant'])
    servers = rng.choice([2, 3, 4, 5])
    mins = rng.choice([2, 3, 4, 5, 6])
    arrivals = rng.choice([40, 50, 60, 80, 90])
    cap_h = servers * 60 / mins
    util = 100 * arrivals / cap_h
    need = -(-arrivals * mins // 60)
    stem = (f'{f_} has {servers} service points, and each customer takes {mins} minutes to serve. At peak time {arrivals} customers arrive per hour. '
            'Calculate the maximum number of customers that can be served per hour and the utilisation of service capacity, and comment on the likely customer experience.')
    if slot.d >= 4:
        stem += ' Calculate the minimum number of service points needed at peak time and suggest one process improvement.'
    ans = f'Capacity = {servers} × 60/{mins} = {p1(cap_h).rstrip("0").rstrip(".")} customers per hour; utilisation = {arrivals}/{p1(cap_h).rstrip("0").rstrip(".")} × 100 = {p1(util)}%. ' + (
        'Demand exceeds capacity, so queues will build up and customers may leave.' if util > 100 else 'Capacity is enough on average, but high utilisation means queues at busy moments.' if util > 80 else 'There is spare capacity, so waiting times should be short.')
    if slot.d >= 4:
        ans += f' Minimum service points = {need}. Improvement: mobile pre-ordering, self-service kiosks or simplifying the menu to cut service time.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{servers} × 60/{mins}; {arrivals}/capacity × 100.', 'capacity and utilisation') + ' [1] comment.' + (f' [1] {arrivals} × {mins}/60 rounded up = {need}; [1] improvement.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch05-st2', concepts=('creativity', 'change'),
  terms=[('processes (marketing mix)', 'the procedures, systems and flow of activities through which a service is delivered to customers'),
         ('customer experience', 'the overall perception a customer forms from all interactions with a business'),
         ('customer journey', 'the stages a customer goes through when interacting with a business, from awareness to purchase and after-sales service'),
         ('service blueprint', 'a diagram that maps each step of a service process, including what customers see and the support activities behind it'),
         ('self-service technology', 'systems that allow customers to serve themselves, such as kiosks, apps and online check-in')],
  facts=[('Which is an example of improving a service process?', 'Allowing customers to order and pay through an app before arriving', ['Increasing the price', 'Changing the logo', 'Reducing product quality'], 'It speeds up delivery.'),
         ('McDonald\'s self-order kiosks mainly aim to:', 'speed up ordering, reduce errors and encourage customers to add items', ['remove all staff', 'raise waiting times', 'make menus shorter'], 'Kiosks change the ordering process.'),
         ('A customer journey map helps a business to:', 'identify problems and opportunities at each stage of the customer experience', ['calculate depreciation', 'set the share price', 'choose a legal structure'], 'It shows each touchpoint.')],
  why=[('Explain why efficient processes are important in service marketing.', 'Customers judge services by speed, reliability and ease; slow or confusing processes cause frustration and lost sales even if the product is good.'),
       ('Explain why technology can improve service processes.', 'Apps, kiosks and automated systems speed up ordering and payment, reduce errors, collect data and allow personalisation.'),
       ('Explain why introducing self-service technology can have drawbacks.', 'Some customers, such as older people, may find it hard to use; it can feel impersonal; and it requires investment and may lead to job losses.')],
  contrast=[('processes', 'people', 'Processes are the systems and procedures through which a service is delivered; people are the staff who carry out the service and interact with customers.')],
  misc=[('Automating service processes always improves the customer experience.', 'Automation can cut waiting times, but it may frustrate customers who want human help, and failures leave customers stuck.')],
  cases=[('Starbucks Mobile Order & Pay', 'By 2023 about a third of Starbucks\' US orders were placed through its app\'s Mobile Order & Pay feature.', 'service processes', 'app ordering cut queues and collected customer data, though it created congestion at pick-up counters'),
         ('Disney\'s MagicBand', 'Disney\'s MagicBand wristbands act as park tickets, room keys and payment, and allow ride reservations.', 'customer experience', 'a single device simplified the customer journey and gave Disney data on visitor flows'),
         ('Ryanair\'s online check-in', 'Ryanair requires passengers to check in online and charges a fee for airport check-in.', 'self-service processes', 'shifting tasks to customers cuts costs, but strict rules and fees have caused complaints')],
  apply=[('A busy restaurant has long waits for tables and food at weekends. Suggest two process improvements and explain their effect on the customer experience.', 'An online booking system with time slots (reduces waiting and uncertainty); a simplified weekend menu or kitchen display system (faster, more reliable food delivery). Both shorten waiting times and raise satisfaction.', 4)],
  evaluate=[('Technology is the best way to improve service processes.', ['speed and accuracy', 'data collection', 'lower labour costs'],
             ['cost and reliability of systems', 'impersonal service', 'excludes some customers', 'staff training and process design matter more'], 'Technology can greatly improve processes, but it must be designed around customers and supported by trained staff.')],
  )

S('ch05-st3', concepts=('creativity', 'sustainability'),
  terms=[('physical evidence', 'the tangible elements that customers see and use when receiving a service, such as premises, décor, uniforms, packaging and websites'),
         ('tangible cue', 'a physical sign that helps customers judge the quality of an intangible service'),
         ('servicescape', 'the physical environment in which a service is delivered'),
         ('intangibility', 'the characteristic of services that they cannot be seen, touched or tried before purchase')],
  facts=[('Why is physical evidence important in service marketing?', 'Services are intangible, so customers judge quality from tangible cues', ['Services can be stored', 'Physical evidence replaces staff', 'It sets the interest rate'], 'Tangible cues reduce uncertainty.'),
         ('Which is an example of physical evidence for a bank?', 'The design of its branches and mobile app', ['Its interest rate', 'Its share price', 'Its board structure'], 'Premises and digital interfaces are tangible cues.'),
         ('Apple Stores\' minimalist design with wooden tables and open space is an example of:', 'physical evidence supporting a premium brand', ['a loss leader', 'price discrimination', 'mass customisation'], 'The servicescape reflects the brand.')],
  why=[('Explain why physical evidence can influence the price a business can charge.', 'Attractive, clean, well-designed premises and materials signal high quality, so customers will pay more.'),
       ('Explain why websites and apps count as physical evidence.', 'They are tangible cues customers use to judge an online service; a slow or poorly designed site suggests poor quality.')],
  contrast=[('physical evidence', 'promotion', 'Physical evidence is the tangible environment and items customers experience when receiving a service; promotion is communication to inform and persuade customers.')],
  misc=[('Physical evidence only matters for expensive services.', 'All services rely on tangible cues; a dirty fast-food restaurant or poor website loses customers whatever the price.')],
  cases=[('Apple Stores', 'Apple\'s more than 500 stores use open layouts, wooden tables and a "Genius Bar" for technical support.', 'physical evidence', 'the design signals premium quality and lets customers try products'),
         ('Premier Inn\'s rooms', 'UK hotel chain Premier Inn advertises a "Good Night Guarantee" and standardised rooms with purple branding across over 800 hotels.', 'tangible cues', 'consistent rooms and branding reassure customers about quality before they stay'),
         ('McDonald\'s restaurant redesigns', 'McDonald\'s "Experience of the Future" redesigns added kiosks, table service and modern décor to many restaurants from 2015.', 'the servicescape', 'updating the physical environment aimed to improve the brand\'s image and customer experience')],
  apply=[('A dental clinic wants to attract more private patients. Suggest two ways it could improve its physical evidence.', 'A modern, clean waiting area with comfortable seating; professional staff uniforms; a clear, well-designed website with online booking; visible certificates and modern equipment.', 2),
         ('Explain how a food-delivery business with no shops can use physical evidence.', 'Through its app design, packaging, branded delivery bags and riders\' uniforms, which signal reliability and quality to customers.', 2)],
  evaluate=[('Physical evidence is the least important of the 7Ps.', ['product and price drive purchase decisions', 'online services have less physical presence'],
             ['services are intangible, so cues matter', 'shapes first impressions and price', 'supports brand image', 'digital physical evidence matters'], 'Physical evidence may matter less for some goods, but for services it strongly shapes perceptions of quality and can justify premium prices.')],
  )

S('ch05-st4', concepts=('change', 'creativity', 'sustainability'),
  terms=[('coherent marketing mix', 'a marketing mix in which all the 7Ps are consistent with each other and with the target market and brand position'),
         ('7Ps', 'product, price, promotion, place, people, processes and physical evidence'),
         ('4Ps', 'product, price, promotion and place, the traditional marketing mix for goods'),
         ('brand positioning', 'the place a brand occupies in customers\' minds relative to competitors')],
  facts=[('A luxury watch sold at a low price in discount stores would be an example of:', 'an incoherent marketing mix', ['price skimming', 'a coherent mix', 'quality assurance'], 'Place and price conflict with a luxury position.'),
         ('Which elements are added to the 4Ps to make the 7Ps?', 'People, processes and physical evidence', ['Profit, planning and partners', 'Packaging, patents and payments', 'Positioning, publicity and premises'], 'The extra three are important for services.'),
         ('A coherent mix for a budget airline would include:', 'low prices, online-only booking and no-frills service', ['luxury lounges and high prices', 'travel agent bookings with free meals', 'premium uniforms and personal chauffeurs'], 'All elements support low cost.')],
  why=[('Explain why the elements of the marketing mix must be coherent.', 'Inconsistent elements send mixed messages – e.g. a premium product in a discount store – which confuses customers and weakens the brand position.'),
       ('Explain why the marketing mix may need to change over the product life cycle.', 'Pricing, promotion and distribution needs differ at launch, growth, maturity and decline, so the mix must be adapted to stay effective.'),
       ('Explain why the 7Ps are more relevant to services than the 4Ps.', 'Services are intangible and delivered by people, so staff, processes and physical evidence strongly shape the customer\'s experience.')],
  contrast=[('the 4Ps', 'the 7Ps', 'The 4Ps (product, price, promotion, place) were developed for goods; the 7Ps add people, processes and physical evidence, which are important for services.')],
  misc=[('Getting one element of the marketing mix right guarantees success.', 'All elements must work together; a great product will fail if the price, place or promotion does not suit the target market.')],
  cases=[('Primark\'s marketing mix', 'Primark sells low-priced fashion in large stores, does almost no advertising and only began limited online click-and-collect in the UK in 2023.', 'a coherent marketing mix', 'low prices, cheap promotion and large stores all support a low-cost position'),
         ('Rolex\'s marketing mix', 'Rolex limits production, sells only through authorised dealers and sponsors events such as Wimbledon.', 'coherence with a luxury position', 'scarcity, exclusive distribution and prestigious sponsorship reinforce the brand\'s high price'),
         ('Gap\'s Yeezy partnership', 'Gap\'s 2020-2022 partnership with Kanye West aimed to bring premium hype to a mid-market brand but ended amid controversy.', 'incoherent marketing mix', 'a high-fashion collaboration clashed with Gap\'s mainstream image and distribution, and created reputational risk')],
  apply=[('A new organic skincare brand targets environmentally conscious consumers aged 25-40. Outline a coherent marketing mix for the brand.', 'Product: natural ingredients, recyclable packaging; price: premium; promotion: Instagram, influencers and sustainability messaging; place: own website and eco-friendly stores; people: knowledgeable staff; processes: easy online ordering and refills; physical evidence: minimalist natural packaging and store design.', 6)],
  evaluate=[('The marketing mix is more important than market research for a successful product launch.', ['the mix is what customers experience', 'coherence builds the brand', 'creativity in promotion'],
             ['the mix must be based on research about the target market', 'research reduces risk', 'both are needed', 'external factors matter'], 'An effective mix depends on good research; the two are complementary rather than alternatives.')],
  )


# =============================================================================================
# ch06 Unit 4.6 International marketing (HL)
# =============================================================================================
@calc('ch06-st1', 'C3', (2, 5))
def export_fx(rng, slot):
    f_ = firm(rng)
    price = rng.choice([20, 40, 50, 80, 100, 120])
    r1 = rng.choice([1.10, 1.20, 1.25, 1.30])
    ch = rng.choice([-10, -5, 5, 10, 20])
    r2 = round(r1 * (1 + ch / 100), 2)
    p1_ = price * r1
    p2_ = price * r2
    stem = (f'{f_}, a UK exporter, sells a product for £{price} to customers in the USA. The exchange rate changes from £1 = ${r1:.2f} to £1 = ${r2:.2f}. '
            'Calculate the dollar price before and after the change, and explain the likely effect on export sales.')
    better = r2 < r1
    ans = (f'Before: £{price} × {r1:.2f} = ${p2(p1_)}; after: £{price} × {r2:.2f} = ${p2(p2_)}. ' +
           ('The pound has depreciated, so the product is cheaper in dollars and export sales should rise, depending on price elasticity of demand.' if better
            else 'The pound has appreciated, so the product is dearer in dollars and export sales are likely to fall unless the firm cuts its sterling price.'))
    if slot.d >= 4:
        stem += ' Suggest one way the firm could reduce its exchange-rate risk.'
        ans += ' It could invoice in pounds, use forward contracts (hedging), or produce/buy inputs in the USA so costs and revenues are in the same currency.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'£{price} × old and new rates.', 'both dollar prices') + ' [1] direction of change in demand explained.' + (' [1] valid method of reducing risk.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 5)


S('ch06-st1', concepts=('change', 'ethics', 'sustainability'),
  terms=[('international marketing', 'marketing products in more than one country'),
         ('exporting', 'selling goods or services produced in the home country to customers in other countries'),
         ('joint venture', 'an agreement in which two or more businesses create a new, jointly owned business to pursue a shared project'),
         ('international franchising', 'allowing businesses in other countries to use a brand and business model in return for fees and royalties'),
         ('foreign direct investment (FDI)', 'investment by a business in production or other facilities that it owns and controls in another country'),
         ('licensing', 'allowing a foreign business to produce a product or use intellectual property in return for a fee')],
  facts=[('Which method of entry involves the most risk and control for the investing firm?', 'Foreign direct investment', ['Exporting through an agent', 'Licensing', 'International franchising'], 'FDI requires large investment but gives full control.'),
         ('Many foreign car makers entered China through:', 'joint ventures with Chinese firms', ['only exporting', 'licensing to consumers', 'franchising to farmers'], 'Rules long required joint ventures, e.g. Volkswagen with SAIC.'),
         ('McDonald\'s expands overseas mainly through:', 'franchising', ['only exporting burgers from the USA', 'licensing patents', 'wholly owned FDI in every restaurant'], 'Most restaurants are run by franchisees.')],
  why=[('Explain why a small business might choose exporting as its first method of international expansion.', 'Exporting needs little investment and risk, uses existing production, and can be started through agents or online platforms.'),
       ('Explain why joint ventures help firms enter unfamiliar markets.', 'The local partner brings knowledge of the market, culture, laws and distribution, and shares costs and risks.'),
       ('Explain why governments encourage inward FDI.', 'FDI creates jobs, brings technology and skills, increases tax revenue and can boost exports.')],
  contrast=[('a joint venture', 'foreign direct investment', 'A joint venture shares ownership, costs and control with a partner; FDI usually means the firm owns and controls the foreign operation itself.'),
            ('exporting', 'international franchising', 'Exporting sends products made in the home country abroad; international franchising lets foreign firms operate under the brand locally in return for fees.')],
  misc=[('Exporting is risk-free because the firm does not invest abroad.', 'Exporters face exchange-rate changes, tariffs, transport costs and the risk of non-payment by foreign customers.')],
  cases=[('Starbucks in India', 'Starbucks entered India in 2012 through Tata Starbucks, a 50:50 joint venture with Tata Consumer Products.', 'joint ventures', 'the local partner provided knowledge, sourcing and property expertise in a complex market'),
         ('Toyota\'s factories abroad', 'Toyota builds vehicles in over 25 countries, including large plants in the USA, the UK and Thailand.', 'foreign direct investment', 'producing close to customers avoids tariffs and transport costs and responds to local demand'),
         ('Scotch whisky exports', 'Scotch whisky exports were worth about £5.6 bn in 2023, sold to over 170 markets.', 'exporting', 'production must stay in Scotland by law, so exporting is the main route to international markets')],
  apply=[('A Swedish furniture start-up wants to sell in Japan. Compare exporting and a joint venture as methods of entry and recommend one.', 'Exporting: low cost and risk, but high transport costs and little local knowledge. Joint venture: local expertise and distribution but shared profits, possible conflict. Recommend exporting via an online platform or agent first to test demand, then consider a joint venture if sales grow.', 6)],
  evaluate=[('Foreign direct investment is the best way to enter an international market.', ['full control', 'avoids tariffs', 'local responsiveness', 'profits not shared'],
             ['high cost and risk', 'lack of local knowledge', 'political risk', 'joint ventures or franchising spread risk'], 'FDI suits large firms with long-term commitment to big markets; smaller firms or riskier markets may suit exporting, franchising or joint ventures.')],
  )

S('ch06-st2', concepts=('ethics', 'change'),
  terms=[('cultural differences', 'differences in values, beliefs, language, customs and behaviour between countries that affect marketing'),
         ('trade barriers', 'government measures such as tariffs, quotas and regulations that restrict international trade'),
         ('political risk', 'the risk that political events or government decisions in a foreign country harm a business'),
         ('economies of scale (international)', 'falling average costs from producing and selling at larger scale across several countries'),
         ('ethnocentrism', 'the belief that one\'s own culture is superior, leading firms to use home-country approaches abroad')],
  facts=[('Which is an opportunity of entering international markets?', 'Access to more customers and economies of scale', ['Higher exchange-rate risk', 'Higher tariffs', 'Cultural misunderstandings'], 'Bigger markets can raise sales and cut unit costs.'),
         ('A tariff is:', 'a tax on imported goods', ['a limit on the number of imports', 'a subsidy for exporters', 'a type of exchange rate'], 'Tariffs raise the price of imports.'),
         ('Russia\'s invasion of Ukraine in 2022 led many Western firms such as McDonald\'s to:', 'exit the Russian market', ['double their investment in Russia', 'move headquarters to Moscow', 'ignore sanctions'], 'Political risk and sanctions caused exits.')],
  why=[('Explain why cultural differences can be a threat when entering a new market.', 'Products, names, colours, adverts and business etiquette may be misunderstood or offensive, leading to poor sales and reputational damage.'),
       ('Explain why entering international markets can spread risk.', 'If demand falls in one country, sales in others may continue, so the firm is less dependent on one economy.'),
       ('Explain why political instability discourages international expansion.', 'Changes in government, conflict or sudden regulation can seize assets, block trade or disrupt operations, making returns uncertain.')],
  contrast=[('opportunities of international marketing', 'threats of international marketing', 'Opportunities include larger markets, economies of scale and spreading risk; threats include cultural differences, trade barriers, exchange-rate changes and political instability.')],
  misc=[('A product that sells well at home will sell well abroad.', 'Tastes, incomes, culture, competition and regulations differ, so products often need adapting.')],
  cases=[('Walmart in Germany', 'Walmart entered Germany in 1997 and withdrew in 2006 after losses estimated at $1 bn; practices such as greeters and smiling rules did not suit German shoppers and staff.', 'cultural issues in international markets', 'applying home-country practices without adapting to local culture led to failure'),
         ('Uber in China', 'Uber spent about $2 bn a year competing in China before selling its Chinese business to rival Didi in 2016.', 'threats of international markets', 'strong local competition and government support for local firms made the market unprofitable'),
         ('Netflix\'s global expansion', 'Netflix launched in over 130 new countries simultaneously in 2016 and now earns most of its revenue outside the US.', 'opportunities of international markets', 'a digital product allowed rapid expansion and economies of scale in content')],
  apply=[('A US fast-food chain plans to open in India. Identify two cultural issues it should consider and explain how it could adapt.', 'Many Indians do not eat beef (Hindu) or pork (Muslim), and vegetarianism is common: offer chicken and vegetarian menus, separate kitchens; spice preferences: adapt recipes; price sensitivity: value menus.', 4)],
  evaluate=[('The threats of entering international markets outweigh the opportunities for small businesses.', ['limited resources and knowledge', 'exchange-rate and political risk', 'cultural mistakes are costly'],
             ['e-commerce lowers entry costs', 'niche products can find global markets', 'export support from governments', 'growth limited at home'], 'Threats are greater for small firms, but low-risk methods such as online exporting can let them gain the opportunities.')],
  )

S('ch06-st3', concepts=('change', 'creativity'),
  terms=[('global marketing', 'using a standardised marketing mix in all countries'),
         ('local marketing', 'adapting the marketing mix to suit each country\'s market'),
         ('glocalisation', 'combining a global brand and strategy with local adaptations of products and promotion – "think global, act local"'),
         ('standardisation', 'selling the same product with the same marketing in all markets to gain economies of scale')],
  facts=[('McDonald\'s selling the McAloo Tikki burger in India is an example of:', 'glocalisation', ['pure standardisation', 'price skimming', 'a loss leader'], 'A global brand with a local product.'),
         ('A key advantage of a standardised global marketing strategy is:', 'economies of scale in production and promotion', ['perfect fit with every local culture', 'no need for a brand', 'no competition'], 'One product and campaign cost less.'),
         ('Coca-Cola\'s "Share a Coke" campaign, which printed popular local first names on bottles in each country, is an example of:', 'glocalisation of a global campaign', ['pure local marketing with no global link', 'mass customisation of production', 'a joint venture'], 'A global idea with local names.')],
  why=[('Explain why many multinational companies choose glocalisation.', 'It keeps the cost advantages and recognition of a global brand while adapting products and messages to local tastes, culture and laws, increasing sales.'),
       ('Explain why standardisation may fail in some markets.', 'Local tastes, incomes, religion, language and regulations differ, so an unchanged product or message may not appeal or may offend.')],
  contrast=[('global marketing', 'local marketing', 'Global marketing uses the same mix everywhere to cut costs and build a uniform brand; local marketing adapts the mix to each country, which suits local needs but costs more.')],
  misc=[('Glocalisation means changing the brand completely in every country.', 'It keeps the core global brand and identity while adapting specific elements such as menus, flavours or adverts.')],
  cases=[('KitKat flavours in Japan', 'Nestlé has sold over 300 limited-edition KitKat flavours in Japan, such as matcha green tea and sake, and the name sounds like "kitto katsu" ("you will surely win").', 'glocalisation', 'local flavours and meanings made a global brand part of Japanese culture and gift-giving'),
         ('Apple\'s standardised iPhone', 'Apple sells largely the same iPhone models and design worldwide, with minor changes for local regulations and networks.', 'global standardisation', 'a uniform premium product delivers economies of scale and a consistent brand image'),
         ('IKEA\'s product adaptations', 'IKEA adapts some products, such as smaller beds and rice cookers in Asia, while keeping its flat-pack, self-service global model.', 'glocal marketing strategies', 'a standard business model with local product changes balances cost efficiency and local appeal')],
  apply=[('A European snack brand plans to enter the Middle East. Explain two elements of the marketing mix it could adapt locally while keeping a global brand.', 'Product: halal-certified ingredients and local flavours; promotion: adverts in Arabic and culturally appropriate imagery; packaging and pack sizes for local retailers; pricing for local incomes.', 4)],
  evaluate=[('Glocalisation is always better than a standardised global strategy.', ['local appeal', 'respect for culture', 'higher sales'],
             ['higher costs', 'brand inconsistency', 'some products are universal (smartphones, luxury goods)', 'complexity of managing many variations'], 'Glocalisation suits culturally sensitive products such as food; standardisation suits technology and luxury goods where a uniform image is valued.')],
  )


# =============================================================================================
# ch07 Unit 5.1-5.2 Operations management and operations methods
# =============================================================================================
@calc('ch07-st1', 'C3', (1, 5))
def productivity(rng, slot):
    f_ = firm(rng)
    w = rng.choice([20, 25, 40, 50, 80])
    hrs = rng.choice([35, 38, 40])
    out = w * hrs * rng.choice([2, 3, 4, 5])
    if slot.d <= 2:
        return dict(stem=f'{f_} employs {w} workers who produced {out:,} units last week. Calculate labour productivity per worker per week.',
                    answer=f'{out // w if out % w == 0 else p1(out / w)} units per worker per week', markingKey=MK(f'{out:,}/{w} = {p1(out / w)}.', 'productivity with units'), marks=2)
    gain = rng.choice([10, 15, 20, 25])
    w2 = w - rng.choice([0, 2, 4, 5])
    out2 = out * (1 + gain / 100)
    lp1 = out / w
    lp2 = out2 / w2
    wage = rng.choice([400, 500, 600, 700])
    c = cur(rng)
    lc1 = wage * w / out
    lc2 = wage * w2 / out2
    stem = (f'{f_} employs {w} workers, each paid {m(wage, c)} a week, producing {out:,} units a week. After new equipment is installed, output rises by {gain}% and the workforce ' + (f'changes to {w2}. ' if w2 != w else f'stays at {w}. ') +
            'Calculate labour productivity and labour cost per unit before and after the change.')
    if slot.d >= 4:
        stem += ' Explain one reason why higher productivity may not lead to higher profit.'
    ans = (f'Before: {p1(lp1)} units per worker, labour cost {c}{p2(lc1)} per unit. After: output {out2:,.0f}, productivity {p1(lp2)} units per worker '
           f'(+{p1(100 * (lp2 - lp1) / lp1)}%), labour cost {c}{p2(lc2)} per unit.')
    if slot.d >= 4:
        ans += ' Profit may not rise if the equipment\'s cost (depreciation, interest, maintenance) outweighs labour savings, or if extra output cannot be sold.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'productivity = output/workers: {out:,}/{w}, {out2:,.0f}/{w2}; labour cost per unit = wage × workers/output.', 'all four values') + (' [1][1] reason explained.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch07-st1', concepts=('change', 'sustainability'),
  terms=[('operations management', 'the planning, organizing and controlling of the processes that turn inputs into goods and services'),
         ('production', 'the process of converting inputs (resources) into outputs (goods and services)'),
         ('labour productivity', 'output per worker in a given period: total output / number of workers'),
         ('capital productivity', 'output per unit of capital (machinery) in a given period'),
         ('value added', 'the difference between the price of a product and the cost of the bought-in inputs used to make it'),
         ('efficiency', 'producing output with the minimum use of resources and cost')],
  facts=[('Labour productivity is calculated as:', 'total output ÷ number of workers', ['number of workers ÷ total output', 'wages ÷ output', 'revenue − costs'], 'Output per worker.'),
         ('Operations management is closely linked to marketing because:', 'it must produce the quantity and quality that marketing promises customers', ['it sets the share price', 'it writes job contracts', 'it decides on dividends'], 'Operations delivers what marketing sells.'),
         ('Which is an output of a hospital?', 'Treated patients', ['Doctors\' skills', 'Medicines bought', 'Electricity used'], 'Outputs are the goods and services produced.')],
  why=[('Explain why operations management is linked to the finance function.', 'Operations decisions such as buying machinery, holding stock and choosing production methods require finance and determine costs, cash flow and profit.'),
       ('Explain why higher labour productivity can improve competitiveness.', 'More output per worker lowers labour cost per unit, allowing lower prices or higher margins.'),
       ('Explain why operations management matters in service businesses.', 'Services must be delivered efficiently and reliably – e.g. waiting times, staffing and processes in banks and hospitals – which determines quality and cost.')],
  contrast=[('labour productivity', 'capital productivity', 'Labour productivity measures output per worker; capital productivity measures output per unit of capital such as machinery.'),
            ('efficiency', 'effectiveness', 'Efficiency is producing with minimum resources and cost; effectiveness is achieving the intended objectives, such as meeting customer needs.')],
  misc=[('Higher productivity always means workers are working harder.', 'Productivity can rise because of better technology, training, organization or motivation, not just greater effort.')],
  cases=[('Amazon\'s warehouse robots', 'Amazon used over 750,000 mobile robots in its warehouses by 2023 to move shelves and packages to workers.', 'productivity and operations management', 'automation raised output per worker but raised concerns about job quality and workload'),
         ('Toyota\'s production system', 'Toyota\'s production system aims to eliminate waste and has been studied by manufacturers worldwide since the 1980s.', 'operations management and efficiency', 'efficient operations became a source of competitive advantage'),
         ('the NHS waiting lists', 'In 2023 waiting lists for NHS hospital treatment in England exceeded 7.5 million cases.', 'operations management in services', 'limited capacity and staffing in service operations can lead to long waits and lower quality')],
  apply=[('A bakery produces 3,600 loaves a week with 12 workers. A rival produces 4,000 loaves with 10 workers. Calculate labour productivity for each and suggest one reason for the difference.', 'Bakery: 3,600/12 = 300 loaves per worker; rival: 4,000/10 = 400. The rival may use more automated ovens, better training, or a more efficient layout.', 3)],
  evaluate=[('Improving labour productivity is the most important objective for operations managers.', ['lower unit costs', 'competitiveness', 'higher wages possible'],
             ['quality and customer satisfaction matter', 'sustainability objectives', 'worker well-being', 'flexibility and reliability'], 'Productivity is important, but operations managers must balance it with quality, flexibility and sustainability.')],
  )

S('ch07-st2', concepts=('creativity', 'change'),
  terms=[('job production', 'producing a single, unique product to a customer\'s specification, such as a bridge or a tailored suit'),
         ('batch production', 'producing a set quantity of identical products together, then switching to a different batch'),
         ('mass production', 'producing large quantities of standardised products, often on a continuous production line'),
         ('flow production', 'continuous production in which products move from one stage to the next without stopping'),
         ('mass customisation', 'combining the low unit costs of mass production with flexibility to tailor products to individual customers')],
  facts=[('A bakery making 200 white loaves, then 150 brown loaves, is using:', 'batch production', ['job production', 'flow production', 'mass customisation'], 'Groups of identical items in turn.'),
         ('Which production method has the lowest unit costs?', 'Mass/flow production', ['Job production', 'Small-batch production', 'Hand-crafted production'], 'Economies of scale reduce unit costs.'),
         ('Nike By You, which lets customers design their own trainers, is an example of:', 'mass customisation', ['job production of buildings', 'flow production of identical shoes', 'batch production of bread'], 'Mass production with individual choices.')],
  why=[('Explain why job production has high unit costs.', 'Each product is unique, requiring skilled labour, flexible equipment and individual planning, so there are few economies of scale.'),
       ('Explain why mass production can reduce worker motivation.', 'Jobs are repetitive and specialised, so workers may feel bored and alienated, leading to absenteeism and lower quality.'),
       ('Explain why mass customisation has become possible.', 'Computer-aided design and manufacturing, flexible robots and online ordering let firms tailor products cheaply at scale.')],
  contrast=[('batch production', 'flow production', 'Batch production makes groups of identical products and switches between batches; flow production makes a continuous stream of standardised products without stopping.')],
  misc=[('Job production is only used for small, cheap items.', 'Job production is often used for large, complex, expensive products such as ships, bridges and buildings.')],
  cases=[('Rolls-Royce bespoke cars', 'Rolls-Royce Motor Cars builds around 6,000 cars a year, most with bespoke features chosen by customers.', 'job production', 'tailored products justify very high prices despite high unit costs'),
         ('Ford\'s moving assembly line', 'In 1913 Ford\'s moving assembly line cut the time to build a Model T from about 12 hours to about 90 minutes.', 'mass/flow production', 'standardisation and continuous flow greatly reduced unit costs and prices'),
         ('Dell\'s build-to-order computers', 'Dell built its success on assembling PCs to each customer\'s chosen specification and delivering them within days.', 'mass customisation', 'flexible assembly combined customer choice with low costs')],
  apply=[('A furniture maker produces handmade tables to order and wants to grow. Explain one advantage and one disadvantage of moving to batch production.', 'Advantage: lower unit costs through specialisation and bulk buying, so it can sell more at lower prices. Disadvantage: less customisation and craftsmanship, which may weaken its USP; stock must be stored.', 4)],
  evaluate=[('Mass customisation is the best production method for all businesses.', ['customer choice', 'lower costs than job production', 'competitive advantage'],
             ['requires large investment in technology', 'not suitable for unique large projects', 'commodity products need no customisation', 'complex logistics'], 'Mass customisation suits consumer products where personal choice adds value, but job and mass production remain best in other markets.')],
  )

S('ch07-st3', concepts=('sustainability', 'ethics'),
  terms=[('sustainability (operations)', 'meeting present needs in operations without compromising the ability of future generations to meet theirs'),
         ('economic sustainability', 'the ability of operations to remain profitable over the long term'),
         ('social sustainability', 'operations that support the well-being of workers, communities and society'),
         ('environmental sustainability', 'operations that reduce harm to the environment, such as cutting emissions, waste and resource use'),
         ('circular economy', 'an economic model that keeps products and materials in use through reuse, repair and recycling'),
         ('carbon footprint', 'the total greenhouse gas emissions caused directly and indirectly by an organization or product')],
  facts=[('Paying fair wages to workers in a supply chain is an example of:', 'social sustainability', ['environmental sustainability only', 'economic unsustainability', 'cost-plus pricing'], 'It supports workers\' well-being.'),
         ('Which is an example of the circular economy?', 'A clothing brand repairing and reselling used garments', ['Single-use packaging', 'Planned obsolescence', 'Burning unsold stock'], 'Products are kept in use.'),
         ('Patagonia\'s "Worn Wear" programme:', 'repairs and resells used Patagonia clothing', ['destroys old stock', 'sells only new products', 'pays influencers to buy more'], 'Extending product life reduces waste.')],
  why=[('Explain why sustainable operations can reduce costs in the long run.', 'Using less energy, water and materials and cutting waste lowers costs, and firms avoid future carbon taxes and fines.'),
       ('Explain why there may be a trade-off between economic and environmental sustainability.', 'Greener materials, processes and equipment can cost more in the short term, reducing profit and competitiveness.'),
       ('Explain why stakeholders increasingly expect sustainable operations.', 'Consumers, investors, employees and governments are more concerned about climate change and ethics, so unsustainable firms face boycotts, regulation and higher finance costs.')],
  contrast=[('social sustainability', 'environmental sustainability', 'Social sustainability concerns the well-being of people, such as fair pay and safe conditions; environmental sustainability concerns reducing harm to the natural environment.')],
  misc=[('Sustainable operations always reduce profit.', 'Sustainability can cut waste and energy costs, attract customers and investors, and reduce regulatory risk, so it can increase long-term profit.')],
  cases=[('Interface\'s Mission Zero', 'Carpet-tile maker Interface set a goal in 1994 to eliminate its environmental impact, cutting greenhouse gas emissions per unit by over 90%.', 'environmental sustainability in operations', 'redesigning processes and materials reduced emissions while the firm remained profitable'),
         ('Fast fashion\'s environmental impact', 'The fashion industry is estimated to produce around 8-10% of global greenhouse gas emissions, with much clothing worn only a few times.', 'unsustainable operations', 'high-volume, low-cost production creates large environmental costs'),
         ('Unilever\'s factories', 'Unilever reported that its factories had sent no waste to landfill since 2015 and cut CO2 emissions from energy by around 70% between 2015 and 2023.', 'sustainable operations', 'waste and energy reduction cut costs and supported the firm\'s brand')],
  apply=[('A coffee chain uses single-use cups. Suggest two ways it could make its operations more environmentally sustainable and explain one cost of each.', 'Offer discounts for reusable cups (cost: lost revenue per discounted cup); switch to compostable cups (higher unit cost); install energy-efficient machines (capital cost). Both cut waste and emissions.', 4),
         ('A factory emits 2,000 tonnes of CO2 a year while producing 50,000 units. New equipment would cut emissions to 1,400 tonnes while output rises to 60,000 units. Calculate emissions per unit before and after, and the percentage reduction.', 'Before: 2,000/50,000 = 0.04 t (40 kg) per unit; after: 1,400/60,000 = 0.0233 t (23.3 kg) per unit; reduction = (40 − 23.3)/40 × 100 = 41.7%.', 4)],
  evaluate=[('Businesses should put environmental sustainability before profit.', ['climate change and stakeholder expectations', 'long-term survival', 'regulation and carbon costs'],
             ['firms must remain profitable to survive', 'higher prices may lose customers', 'greenwashing risk', 'governments should set rules'], 'Profit and sustainability are linked in the long run; firms should integrate sustainability into strategy while remaining economically viable.')],
  )


# =============================================================================================
# ch08 Unit 5.3 Lean production and quality management (HL)
# =============================================================================================
@calc('ch08-st1', 'C3', (2, 5))
def jit_saving(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    avg1 = rng.choice([200, 300, 400, 500]) * 1000
    cut = rng.choice([50, 60, 70, 75, 80])
    hold = rng.choice([15, 20, 25])
    deliv = rng.choice([12, 24, 52])
    extra = rng.choice([200, 300, 400, 500])
    avg2 = avg1 * (1 - cut / 100)
    save = (avg1 - avg2) * hold / 100
    extra_cost = deliv * extra * rng.choice([4, 6, 8]) // 4
    net = save - extra_cost
    stem = (f'{f_} holds average inventory worth {m(avg1, c)}. Annual holding costs (storage, insurance, waste and the cost of capital) are {hold}% of the value of inventory. '
            f'Moving to just-in-time (JIT) would cut average inventory by {cut}% but add {m(extra_cost, c)} a year in extra delivery costs. Calculate the net annual saving from JIT.')
    ans = f'New average inventory = {m(avg2, c)}; holding cost saving = ({m(avg1, c)} − {m(avg2, c)}) × {hold}% = {m(save, c)}; net saving = {m(save, c)} − {m(extra_cost, c)} = {m(net, c)}.'
    if slot.d >= 4:
        stem += ' Explain one risk of JIT for the business.'
        ans += ' Risk: with little buffer stock, a supplier delay or transport disruption (e.g. during Covid-19 or the 2021 Suez Canal blockage) can stop production.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{avg1:,} × (1 − {cut}%) = {avg2:,.0f}; saving {save:,.0f}; net {net:,.0f}.', 'net saving') + (' [1][1] risk explained.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch08-st1', concepts=('change', 'sustainability', 'creativity'),
  terms=[('lean production', 'an approach to operations that aims to minimise waste of all resources, including time, materials, space and labour'),
         ('kaizen', 'continuous improvement: small, frequent improvements suggested by employees at all levels'),
         ('just-in-time (JIT)', 'a stock control system in which materials arrive just when needed for production, so little stock is held'),
         ('kanban', 'a visual signalling system, often cards, that triggers the production or delivery of parts only when they are needed'),
         ('andon', 'a system that lets workers signal or stop production when a problem is found, often using lights or a cord'),
         ('just-in-case (JIC)', 'holding buffer stocks of materials and finished goods in case of unexpected demand or supply problems')],
  facts=[('Kaizen means:', 'continuous improvement through small steps', ['large one-off changes', 'mass production', 'cutting all staff'], 'Small, continuous improvements.'),
         ('An andon cord allows workers to:', 'stop the production line when they spot a problem', ['order new stock automatically', 'clock in and out', 'set prices'], 'It prevents defects moving down the line.'),
         ('Which is a disadvantage of JIT?', 'Production can stop if a supplier delivery is late', ['It increases storage costs', 'It needs large warehouses', 'It increases waste'], 'Little buffer stock means vulnerability.'),
         ('The lean production system most associated with JIT and kaizen was developed by:', 'Toyota', ['Ford', 'General Electric', 'IKEA'], 'The Toyota Production System.')],
  why=[('Explain why lean production can reduce costs.', 'It cuts waste of materials, time, space and stock, reducing storage costs, defects and idle time, so unit costs fall.'),
       ('Explain why kaizen depends on employee involvement.', 'Workers know their jobs best and can spot small improvements; their suggestions and commitment are needed for continuous improvement.'),
       ('Explain why JIT requires reliable suppliers.', 'Because little stock is held, materials must arrive on time and at the right quality, or production stops.')],
  contrast=[('just-in-time', 'just-in-case', 'JIT holds minimal stock and relies on frequent, reliable deliveries; JIC holds buffer stock to protect against supply disruptions and demand surges, at higher holding cost.'),
            ('kaizen', 'kanban', 'Kaizen is a philosophy of continuous small improvements; kanban is a visual signalling system that controls the flow of materials.')],
  misc=[('Lean production means employing as few workers as possible.', 'Lean production removes waste of all kinds; it relies on involved, multi-skilled workers rather than simply cutting staff.')],
  cases=[('the 2021 chip shortage', 'In 2021 a global semiconductor shortage forced car makers such as Ford and Volkswagen to halt production; industry losses were estimated at over $200 bn in revenue.', 'risks of just-in-time', 'lean supply chains with little buffer stock were badly exposed to supply disruption'),
         ('Toyota\'s andon cord', 'Any worker on a Toyota production line can pull the andon cord to stop the line when a problem occurs.', 'andon and quality', 'stopping to fix problems immediately prevents defects and supports continuous improvement'),
         ('Toyota\'s chip stockpile', 'After the 2011 Japanese earthquake, Toyota built up stocks of key chips, which helped it keep producing longer than rivals during the 2021 shortage.', 'just-in-case', 'holding buffer stocks of critical parts reduced the risk of production stopping')],
  apply=[('A sandwich bar throws away 15% of its ingredients at the end of each day. Explain how lean production methods could help.', 'JIT ordering of fresh ingredients in smaller, more frequent deliveries; kanban signals for restocking; kaizen suggestions from staff on portioning and demand forecasting – all reduce waste and costs.', 4)],
  evaluate=[('Just-in-time is too risky for businesses with global supply chains.', ['disruptions from pandemics, conflict and shipping', 'production stops without buffer stock', 'chip shortage example'],
             ['lower holding costs and waste', 'improved quality and efficiency', 'firms can hold JIC stock of critical parts only', 'diversified suppliers'], 'JIT remains valuable, but global firms increasingly combine it with buffer stocks of critical inputs and diversified suppliers.')],
  )


@calc('ch08-st2', 'C3', (1, 5))
def defect_rate(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    out = rng.choice([5_000, 8_000, 10_000, 20_000])
    d1 = rng.choice([2, 3, 4, 5, 6])
    d2 = rng.choice([0.5, 1, 1.5])
    rework = rng.choice([4, 6, 8, 12])
    n1 = out * d1 // 100
    if slot.d <= 2:
        return dict(stem=f'{f_} produced {out:,} units last month, of which {n1:,} were defective. Calculate the defect rate.',
                    answer=f'{d1}%', markingKey=MK(f'{n1:,}/{out:,} × 100 = {d1}%.', f'{d1}%'), marks=2)
    n2 = out * d2 / 100
    save = (n1 - n2) * rework * 12
    prog = rng.choice([20_000, 30_000, 40_000])
    stem = (f'{f_} produces {out:,} units a month with a defect rate of {d1}%. Each defective unit costs {m(rework, c)} to rework. A total quality management (TQM) programme costing {m(prog, c)} a year '
            f'would cut the defect rate to {d2:g}%. Calculate the number of defective units each month before and after, the annual saving in rework costs, and whether the programme is financially worthwhile.')
    ans = (f'Defects: {n1:,} → {n2:,.0f} a month; annual saving = ({n1:,} − {n2:,.0f}) × {m(rework, c)} × 12 = {m(save, c)}; net = {m(save - prog, c)} a year, so the programme is '
           + ('financially worthwhile' if save > prog else 'not justified on rework savings alone') + '. Non-financial benefits include fewer complaints and a better reputation.')
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{out:,} × {d1}% and × {d2:g}%; difference × {rework} × 12 = {save:,.0f}; compare with {prog:,}.', 'saving and judgement'),
                marks=4 if slot.d <= 3 else 6)


S('ch08-st2', concepts=('change', 'ethics'),
  terms=[('quality', 'the degree to which a product meets customers\' needs and expectations, being fit for purpose'),
         ('quality control', 'inspecting products, usually at the end of production, to find and remove defects'),
         ('quality assurance', 'a system that aims to prevent defects by setting and checking standards at every stage of production'),
         ('total quality management (TQM)', 'an approach in which every employee is responsible for quality at every stage, aiming for zero defects'),
         ('quality circle', 'a small group of workers who meet regularly to identify and solve quality problems'),
         ('benchmarking', 'comparing a firm\'s products, processes or performance with the best in the industry in order to improve'),
         ('ISO 9001', 'an international standard certifying that a firm has an effective quality management system')],
  facts=[('Which approach aims to prevent defects rather than detect them?', 'Quality assurance', ['Quality control by final inspection', 'Increasing output', 'Price skimming'], 'Prevention at each stage.'),
         ('Benchmarking involves:', 'comparing performance with the best in the industry', ['copying patents illegally', 'cutting prices', 'inspecting every product at the end'], 'Learning from best practice.'),
         ('A firm that produced 10,000 units with 250 defects has a defect rate of:', '2.5%', ['25%', '0.25%', '40%'], '250/10,000 × 100.')],
  why=[('Explain why quality assurance can be cheaper than quality control in the long run.', 'Preventing defects avoids the cost of scrap, rework, returns and complaints, and reduces the need for costly final inspection.'),
       ('Explain why TQM requires a change in organizational culture.', 'Every employee must take responsibility for quality, so firms need training, empowerment and commitment rather than relying on inspectors.'),
       ('Explain why quality circles can motivate employees.', 'Workers are involved in solving problems and their ideas are valued, meeting higher-level needs such as esteem and self-actualisation.')],
  contrast=[('quality control', 'quality assurance', 'Quality control detects defects by inspecting finished products; quality assurance prevents defects by setting standards and checking them throughout production.')],
  misc=[('Quality means a product is expensive and luxurious.', 'Quality means meeting customers\' expectations and being fit for purpose; a cheap product can be high quality if it meets those expectations.')],
  cases=[('Boeing 737 MAX quality problems', 'In January 2024 a door plug blew out of an Alaska Airlines Boeing 737 MAX 9 in flight; US regulators then capped Boeing\'s 737 production and increased inspections.', 'quality assurance failures', 'weak quality systems led to safety risks, regulation and damage to reputation'),
         ('Samsung Galaxy Note 7 recall', 'In 2016 Samsung recalled about 2.5 million Galaxy Note 7 phones after battery fires, costing an estimated $5 bn.', 'quality control and its costs', 'defects that reached customers caused huge recall costs and reputational damage'),
         ('Xerox\'s benchmarking', 'In the late 1970s Xerox benchmarked its costs and processes against Japanese rivals such as Canon and found they could sell copiers for less than Xerox\'s production cost.', 'benchmarking', 'comparison with the best competitors drove major improvements in cost and quality')],
  apply=[('A bicycle manufacturer has a 4% return rate due to faulty brakes. Recommend whether it should increase final inspections or introduce quality assurance, and justify your answer.', 'Quality assurance: set standards and checks at each stage (e.g. supplier parts, assembly), train workers and use quality circles. This prevents faults rather than finding them at the end, cutting rework and protecting safety and reputation.', 4)],
  evaluate=[('Total quality management is worth the cost for every business.', ['fewer defects and complaints', 'reputation and loyalty', 'motivated workers'],
             ['high training and implementation costs', 'needs culture change and time', 'small firms may lack resources', 'benefits are hard to measure'], 'TQM brings long-term benefits for most firms, especially where quality failures are costly or dangerous, but it requires commitment and time.')],
  )

S('ch08-st3', concepts=('ethics', 'change'),
  terms=[('stakeholder impact of lean production', 'the effects of lean methods on employees, suppliers, customers, shareholders and the community'),
         ('multi-skilling', 'training workers to perform several different tasks'),
         ('supplier partnership', 'a long-term, close relationship with suppliers based on trust, quality and reliable deliveries'),
         ('work intensification', 'increasing the pace or pressure of work, which can result from lean methods')],
  facts=[('How can lean production benefit customers?', 'Higher quality and lower prices', ['Longer waiting times', 'Less choice and more defects', 'Higher prices always'], 'Less waste lowers costs and defects.'),
         ('Which stakeholder may face pressure from JIT?', 'Suppliers, who must deliver frequently and reliably', ['Only shareholders', 'Only the government', 'No stakeholders'], 'Suppliers bear more responsibility.'),
         ('A possible negative effect of lean production on employees is:', 'more pressure and stress from intense work', ['less training', 'no responsibility', 'fewer skills'], 'Work intensification.')],
  why=[('Explain how lean production and TQM can benefit employees.', 'Multi-skilling, teamwork and involvement in kaizen and quality circles can make work more varied and give workers more responsibility and recognition.'),
       ('Explain why lean production may create conflict between shareholders and employees.', 'Shareholders gain from lower costs and higher profits, but employees may face job cuts, work intensification and pressure to keep improving.')],
  contrast=[('the impact of lean production on suppliers', 'the impact of lean production on customers', 'Suppliers must deliver small, frequent, high-quality orders, which can raise their costs; customers usually benefit from better quality and lower prices.')],
  misc=[('Lean production benefits all stakeholders equally.', 'Benefits and costs fall unequally; shareholders and customers may gain while some workers and suppliers face more pressure.')],
  cases=[('Amazon warehouse working conditions', 'Amazon has faced criticism and strikes in several countries over productivity targets and the pace of work in its warehouses.', 'impact of lean methods on employees', 'tight efficiency targets can raise productivity but increase stress and conflict'),
         ('Toyota\'s supplier relationships', 'Toyota works closely with a network of long-term suppliers, sharing knowledge and helping them improve quality.', 'supplier partnerships', 'close collaboration makes JIT reliable and shares the gains of lean production'),
         ('Virginia Mason hospital', 'Virginia Mason Medical Center in Seattle adopted the Toyota Production System in 2002, reporting shorter waiting times and fewer errors.', 'impact of lean production on customers', 'lean methods improved patient safety and service, though staff needed training and support')],
  apply=[('A clothing factory introduces lean production. Analyse its likely impact on two stakeholder groups.', 'Employees: multi-skilling and teamwork may increase job variety but also pressure and possible job losses. Customers/retailers: fewer defects, faster delivery and lower prices. Suppliers: must make small frequent deliveries.', 4)],
  evaluate=[('Lean production and TQM benefit employees more than they harm them.', ['multi-skilling and involvement', 'empowerment', 'job security in a competitive firm'],
             ['work intensification and stress', 'job cuts from efficiency', 'constant pressure to improve', 'depends on management style'], 'The effect depends on implementation: with genuine involvement and support, employees gain; when lean is used mainly to cut costs, they may be harmed.')],
  )


# =============================================================================================
# ch09 Unit 5.4 Location
# =============================================================================================
@calc('ch09-st1', 'C3', (2, 5))
def location_score(rng, slot):
    sites = rng.sample(['Site A (city edge)', 'Site B (port town)', 'Site C (rural)', 'Site D (science park)'], 3)
    crit = [('labour costs', rng.choice([3, 4])), ('access to market', rng.choice([4, 5])), ('transport links', rng.choice([2, 3])), ('government incentives', rng.choice([1, 2]))]
    scores = {s: [rng.choice(range(4, 10)) for _ in crit] for s in sites}
    tot = {s: sum(w * x for (_, w), x in zip(crit, scores[s])) for s in sites}
    best = max(sites, key=lambda s: tot[s])
    if list(tot.values()).count(tot[best]) > 1:
        scores[best][0] += 1
        tot[best] += crit[0][1]
    wt = ', '.join(f'{n} (weight {w})' for n, w in crit)
    tab = '; '.join(f'{s}: ' + ', '.join(str(x) for x in scores[s]) for s in sites)
    stem = f'A firm compares three locations, scoring each factor out of 10. Factors and weights: {wt}. Scores in that order – {tab}. Calculate the weighted score for each site and identify the preferred location.'
    if slot.d >= 4:
        stem += ' Explain one qualitative factor the firm should also consider.'
    ans = '; '.join(f'{s}: {tot[s]}' for s in sites) + f'. Preferred: {best}.'
    if slot.d >= 4:
        ans += ' Qualitative factors: quality of life for managers, local attitudes, political stability, room for expansion, or environmental impact.'
    return dict(stem=stem, answer=ans,
                markingKey=MK('weighted score = Σ(weight × score) for each site.', 'all three totals and the preferred site') + (' [1][1] qualitative factor explained.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch09-st1', concepts=('change', 'sustainability', 'ethics'),
  terms=[('location decision', 'the choice of where to place a business\'s operations, such as a factory, office or shop'),
         ('quantitative location factors', 'measurable factors such as land and labour costs, transport costs, government grants and expected revenue'),
         ('qualitative location factors', 'non-numerical factors such as quality of life, local culture, political stability and managers\' preferences'),
         ('infrastructure', 'the basic facilities a business needs, such as roads, ports, power, water and internet connections'),
         ('weighted factor analysis', 'a method of comparing locations by scoring each factor and multiplying by weights reflecting its importance')],
  facts=[('Which is a qualitative location factor?', 'Political stability of the country', ['Cost of land per square metre', 'Wage rates', 'Transport costs per tonne'], 'It is not directly measurable in money.'),
         ('A bulk-reducing industry such as steel-making is often located:', 'near its sources of raw materials', ['only in city centres', 'near its customers only', 'anywhere at random'], 'Transport of heavy raw materials is costly.'),
         ('Why did Tesla build Gigafactory Berlin near Berlin?', 'To serve the large European market and reduce transport and tariff costs', ['Because labour is cheapest in Europe', 'To avoid all regulation', 'Because there are no customers in the USA'], 'Production near the market.')],
  why=[('Explain why retailers usually locate close to their customers.', 'Retail sales depend on convenience and footfall, so being near customers increases sales, even if rents are higher.'),
       ('Explain why weighted factor analysis may not give the right location decision.', 'Weights and scores are subjective, it may ignore important qualitative issues, and forecasts of costs and revenue may be wrong.'),
       ('Explain why some businesses no longer need to locate near customers.', 'The internet and fast delivery allow online firms and services to serve customers from anywhere, so they can choose low-cost locations.')],
  contrast=[('quantitative location factors', 'qualitative location factors', 'Quantitative factors can be measured in numbers, such as costs and revenues; qualitative factors, such as culture and quality of life, cannot easily be measured but still affect success.')],
  misc=[('The cheapest location is always the best.', 'Low costs may be offset by poor infrastructure, low skills, distance from customers or political risk.')],
  cases=[('Tesla\'s Gigafactory in Berlin', 'Tesla opened its Gigafactory near Berlin in 2022, close to European customers, despite environmental protests over water use and forest clearance.', 'location factors', 'access to the market outweighed environmental and planning difficulties'),
         ('Silicon Valley', 'Many technology firms locate in Silicon Valley despite very high property and labour costs.', 'qualitative and quantitative location factors', 'access to skilled workers, venture capital and other tech firms outweighs high costs'),
         ('Intel\'s Ohio chip plants', 'In 2022 Intel announced chip plants in Ohio costing at least $20 bn, supported by US government subsidies.', 'government incentives and location', 'grants and political support influenced the choice of location')],
  apply=[('A supermarket chain is choosing between a town-centre site (high rent, high footfall) and an out-of-town site (low rent, needs car access). Explain two factors it should consider.', 'Customer access and footfall (town centre is convenient for pedestrians; out-of-town suits car-based weekly shopping); costs (rent, parking); planning permission; competition nearby; environmental impact of car travel.', 4)],
  evaluate=[('Quantitative factors are more important than qualitative factors in location decisions.', ['costs and revenues determine profit', 'measurable and comparable', 'objective'],
             ['qualitative factors such as stability and skills affect long-term success', 'numbers rely on forecasts', 'staff willingness to relocate', 'ethics and community reaction'], 'Quantitative factors are a key starting point, but qualitative factors can decide whether a location succeeds in the long run.')],
  )


@calc('ch09-st2', 'C3', (2, 5))
def offshore_cost(rng, slot):
    c = cur(rng)
    q = rng.choice([10_000, 20_000, 50_000])
    home = rng.choice([12, 15, 18, 20])
    abroad = round(home * rng.choice([0.4, 0.5, 0.6]), 2)
    ship = rng.choice([1, 1.5, 2, 3])
    tariff = rng.choice([0, 5, 10, 20])
    unit_abroad = abroad * (1 + tariff / 100) + ship
    save = (home - unit_abroad) * q
    stem = (f'A firm makes {q:,} units a year at home for {m(home, c)} each. Producing offshore would cost {m(abroad, c)} per unit, plus {m(ship, c)} per unit for shipping and {f"a {tariff}% import tariff on the production cost" if tariff else "no import tariff"}. '
            'Calculate the total cost per unit of offshoring and the annual saving.')
    ans = f'Offshore unit cost = {m(abroad, c)} × {1 + tariff / 100:g} + {m(ship, c)} = {c}{p2(unit_abroad)}; annual saving = ({m(home, c)} − {c}{p2(unit_abroad)}) × {q:,} = {m(round(save), c)}.'
    if slot.d >= 4:
        stem += ' Explain two non-financial factors the firm should consider before offshoring.'
        ans += ' Non-financial: quality control and longer lead times, reputation and ethics (working conditions), job losses at home and staff morale, supply-chain risk and exchange rates.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{abroad} × {1 + tariff / 100:g} + {ship} = {p2(unit_abroad)}; × {q:,}.', 'unit cost and saving') + (' [1][1] non-financial factors.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch09-st2', concepts=('ethics', 'change', 'sustainability'),
  terms=[('outsourcing', 'contracting out a business activity to an external firm instead of doing it internally'),
         ('offshoring', 'moving business activities to another country, either within the firm or to an external supplier'),
         ('insourcing', 'bringing an activity that was outsourced back inside the business'),
         ('reshoring', 'moving business activities back to the home country from abroad'),
         ('nearshoring', 'moving business activities to a nearby country, such as US firms moving production to Mexico')],
  facts=[('A UK firm moving its call centre to India is an example of:', 'offshoring', ['reshoring', 'insourcing', 'nearshoring to France'], 'Moving activities abroad.'),
         ('Which is a reason for reshoring?', 'Rising wages abroad and supply-chain risks', ['Lower wages abroad', 'Cheaper shipping costs abroad', 'No need for quality control'], 'Cost gaps have narrowed and risks increased.'),
         ('Apple\'s use of Foxconn to assemble iPhones is an example of:', 'outsourcing and offshoring', ['insourcing', 'reshoring', 'a cooperative'], 'An external firm in another country.')],
  why=[('Explain why businesses outsource non-core activities.', 'Specialist firms can do them more cheaply or better, so the business cuts costs and can focus on its core activities.'),
       ('Explain why offshoring can damage a firm\'s reputation.', 'It may be linked to poor working conditions, job losses at home or lower service quality, attracting criticism from customers and the media.'),
       ('Explain why some firms are reshoring production.', 'Wages in countries such as China have risen, shipping and supply-chain risks have increased, and governments offer incentives for domestic production.')],
  contrast=[('outsourcing', 'offshoring', 'Outsourcing means using an external firm for an activity (at home or abroad); offshoring means moving an activity to another country, which may be within the same firm.'),
            ('insourcing', 'reshoring', 'Insourcing brings an outsourced activity back inside the firm; reshoring brings an activity back to the home country.')],
  misc=[('Offshoring always reduces costs.', 'Lower wages may be offset by transport costs, tariffs, quality problems, communication difficulties and exchange-rate changes.')],
  cases=[('Apple and Foxconn', 'Most iPhones are assembled by Foxconn in China, and Apple began moving some production to India from 2017.', 'outsourcing and offshoring', 'outsourcing assembly cuts costs, while diversifying countries reduces political and supply-chain risk'),
         ('nearshoring to Mexico', 'In 2023 Mexico overtook China as the largest source of US imports, as firms moved production closer to the US market.', 'nearshoring', 'proximity, trade agreements and tensions with China changed location decisions'),
         ('GE\'s reshoring of appliances', 'In the 2010s GE Appliances moved production of some water heaters and refrigerators from China back to Kentucky.', 'reshoring', 'automation, quality and shorter supply chains made domestic production competitive')],
  apply=[('A UK clothing retailer outsources production to factories in Bangladesh. Explain one benefit and two risks of this decision.', 'Benefit: much lower labour costs. Risks: poor working conditions damaging reputation (e.g. Rana Plaza), long lead times and quality problems, exchange-rate and shipping disruption.', 4)],
  evaluate=[('Reshoring is the best response to supply-chain disruption.', ['shorter supply chains', 'less political risk', 'quality control', 'government incentives'],
             ['higher labour costs', 'skills shortages at home', 'nearshoring or diversification may be cheaper', 'automation needed'], 'Reshoring can reduce risk, but diversifying suppliers or nearshoring may give similar resilience at lower cost.')],
  )

S('ch09-st3', concepts=('ethics', 'sustainability'),
  terms=[('government incentives', 'grants, tax breaks, subsidised land or infrastructure offered by governments to attract businesses to an area'),
         ('clustering', 'the concentration of similar or related businesses in one area, such as technology firms in Silicon Valley'),
         ('external economies of scale', 'cost advantages that a firm gains from the growth of its industry in an area, such as skilled labour and specialist suppliers'),
         ('special economic zone', 'an area where business and trade rules differ from the rest of the country, often with lower taxes, to attract investment'),
         ('ethical location decisions', 'location choices that consider the effects on workers, communities and the environment, not just costs')],
  facts=[('Which is a benefit of clustering?', 'Access to skilled workers and specialist suppliers', ['Higher rents only', 'Less competition for staff', 'No need for infrastructure'], 'External economies of scale.'),
         ('China\'s Shenzhen became a manufacturing centre after being made a:', 'special economic zone in 1980', ['national park', 'tax haven for banks only', 'farming region'], 'Lower taxes and fewer restrictions attracted investment.'),
         ('The US Inflation Reduction Act of 2022 encouraged firms to locate:', 'clean-energy and battery production in the USA', ['call centres in Asia', 'coal mines in Europe', 'banks offshore'], 'Subsidies and tax credits influenced location.')],
  why=[('Explain why governments offer incentives to attract businesses.', 'New businesses create jobs, raise tax revenue, bring skills and technology and help regenerate poorer regions.'),
       ('Explain why clustering can attract firms despite high costs.', 'Being near related firms gives access to skilled labour, suppliers, ideas and customers, which can outweigh higher rents and wages.'),
       ('Explain why location decisions can raise ethical issues.', 'Firms may choose places with weak labour or environmental laws, low wages or tax advantages, which can exploit workers or harm communities.')],
  contrast=[('government incentives', 'clustering', 'Government incentives are financial or other support offered by the state to attract firms; clustering is the natural concentration of related firms that benefit from being near each other.')],
  misc=[('Government incentives always guarantee that a factory will stay in an area.', 'Firms may leave when incentives end or conditions change, as when some subsidised plants closed after grants expired.')],
  cases=[('Foxconn in Wisconsin', 'In 2017 Foxconn promised a $10 bn factory and 13,000 jobs in Wisconsin in return for about $3 bn in incentives; the project was later scaled back sharply.', 'government incentives', 'incentives did not guarantee the promised jobs, raising questions about value for taxpayers'),
         ('the City of London', 'The City of London clusters banks, insurers, lawyers and accountants within about one square mile.', 'clustering and external economies of scale', 'proximity to clients, talent and related services strengthens the financial centre'),
         ('Ireland\'s corporation tax', 'Ireland\'s 12.5% corporation tax rate helped attract the European headquarters of firms such as Google, Apple and Meta.', 'ethical and financial location decisions', 'low taxes attracted investment but raised concerns about profit shifting')],
  apply=[('A battery maker is offered a $200 m grant to build a factory in an area with high unemployment. Explain two factors, other than the grant, that it should consider.', 'Availability of skilled workers and training; infrastructure (power, transport); access to customers such as car makers; community and environmental reaction; whether the grant has conditions such as jobs targets.', 4)],
  evaluate=[('Businesses should always choose the location with the lowest costs.', ['profitability', 'competitiveness', 'shareholder returns'],
             ['ethical issues and reputation', 'clustering benefits', 'access to market and skills', 'political risk'], 'Cost matters, but long-term success and ethical responsibility require weighing skills, markets, risk and impact on communities.')],
  )


# =============================================================================================
# ch10 Unit 5.5-5.6 Break-even analysis and production planning
# =============================================================================================
@calc('ch10-st1', 'C3', (1, 5))
def break_even(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    p = rng.choice([12, 15, 20, 25, 30, 40, 50])
    vc = round(p * rng.choice([0.4, 0.5, 0.6]), 2)
    cpu = p - vc
    be = rng.choice([1_000, 1_500, 2_000, 2_500, 4_000, 5_000])
    fc = round(cpu * be)
    q = int(be * rng.choice([1.2, 1.25, 1.5, 1.6, 2]))
    if slot.d <= 2:
        return dict(stem=f'{f_} sells a product for {m(p, c)}; variable cost is {m(vc, c)} per unit. Calculate the contribution per unit.',
                    answer=m(cpu, c), markingKey=MK(f'{p} − {p2(vc)} = {p2(cpu)}.', m(cpu, c)), marks=2)
    tc = cpu * q
    prof = tc - fc
    stem = (f'{f_} sells a product for {m(p, c)}. Variable cost is {m(vc, c)} per unit and fixed costs are {m(fc, c)} a year. It expects to sell {q:,} units. '
            'Calculate the contribution per unit, total contribution, break-even quantity and profit.')
    ans = f'Contribution per unit = {m(cpu, c)}; total contribution = {m(round(tc), c)}; break-even = {m(fc, c)}/{m(cpu, c)} = {be:,} units; profit = {m(round(tc), c)} − {m(fc, c)} = {m(round(prof), c)}.'
    if slot.d >= 4:
        stem += ' Construct a break-even chart (describe the lines and where they cross) and explain one limitation of break-even analysis.'
        ans += (f' Chart: fixed cost line horizontal at {m(fc, c)}; total cost line from {m(fc, c)} rising by {m(vc, c)} per unit; revenue line from 0 rising by {m(p, c)} per unit; they cross at {be:,} units and {m(round(be * p), c)}. '
                'Limitation: it assumes all output is sold at one price and that costs are linear.')
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'{p} − {p2(vc)} = {p2(cpu)}; × {q:,}; {fc:,}/{p2(cpu)} = {be:,}; total contribution − fixed costs.', 'all four values') + (' [2] correctly labelled chart; [1] limitation.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch10-st1', concepts=('change', 'creativity'),
  terms=[('contribution per unit', 'selling price per unit minus variable cost per unit'),
         ('total contribution', 'contribution per unit multiplied by the number of units sold, or total revenue minus total variable costs'),
         ('break-even quantity', 'the level of output at which total revenue equals total costs, so there is neither profit nor loss: fixed costs / contribution per unit'),
         ('break-even point', 'the point on a break-even chart where the total revenue and total cost lines cross'),
         ('fixed costs', 'costs that do not change with the level of output in the short run, such as rent and salaries'),
         ('variable costs', 'costs that change directly with the level of output, such as raw materials')],
  facts=[('Price $20, variable cost $12, fixed costs $16,000. Break-even quantity is:', '2,000 units', ['800 units', '1,333 units', '500 units'], '16,000/(20 − 12) = 2,000.'),
         ('Profit can be calculated as:', 'total contribution − fixed costs', ['total contribution + fixed costs', 'price − fixed costs', 'variable costs − revenue'], 'Contribution first covers fixed costs.'),
         ('If variable costs per unit rise and price stays the same, the break-even quantity will:', 'rise', ['fall', 'stay the same', 'become zero'], 'Contribution per unit falls.')],
  why=[('Explain why contribution is important for break-even analysis.', 'Each unit sold contributes towards fixed costs; once total contribution covers fixed costs, extra contribution becomes profit.'),
       ('Explain why break-even analysis is useful for a new business.', 'It shows how many units must be sold to avoid a loss, helping to judge whether the plan is realistic and to support applications for finance.'),
       ('Explain why break-even analysis may give misleading results.', 'It assumes a single price, linear costs and that all output is sold, and it relies on forecasts that may be wrong.')],
  contrast=[('contribution', 'profit', 'Contribution is revenue minus variable costs, which goes towards covering fixed costs; profit is what remains after fixed costs have also been covered.'),
            ('fixed costs', 'variable costs', 'Fixed costs do not change with output in the short run; variable costs rise and fall directly with output.')],
  misc=[('A business makes a profit on every unit it sells above zero.', 'Only units sold beyond the break-even quantity generate profit; before that, contribution is still covering fixed costs.')],
  cases=[('airline break-even load factors', 'Airlines often need to fill about 70-80% of seats on a flight to break even, according to industry body IATA.', 'break-even analysis', 'high fixed costs mean airlines need high sales volumes before making a profit'),
         ('Disneyland Paris\'s early losses', 'Disneyland Paris (then Euro Disney) opened in 1992 with about 11 million visitors in its first year, fewer than forecast, and made large losses in its early years.', 'break-even and fixed costs', 'very high fixed costs and lower-than-expected sales meant break-even was not reached'),
         ('Netflix\'s content costs', 'Netflix spends around $17 bn a year on content, which is largely fixed regardless of subscriber numbers.', 'contribution and fixed costs', 'each extra subscriber adds contribution at low variable cost, so profit rises quickly once fixed costs are covered')],
  apply=[('A food truck sells burgers for $8 with variable costs of $3. Fixed costs are $2,500 a month. Calculate the break-even number of burgers per month and the profit if it sells 800 burgers.', 'Contribution = $5; break-even = 2,500/5 = 500 burgers; profit = 800 × 5 − 2,500 = $1,500.', 4)],
  evaluate=[('Break-even analysis is of limited use in business decision-making.', ['assumes linear costs and single price', 'all output sold', 'static', 'relies on forecasts'],
             ['simple and quick', 'shows effect of changes in price and cost', 'useful for start-ups and finance applications', 'supports what-if analysis'], 'Break-even analysis is a useful planning tool when its assumptions are understood and it is combined with research and other financial tools.')],
  )


@calc('ch10-st2', 'C3', (1, 5))
def margin_safety(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    p = rng.choice([20, 25, 30, 40, 50])
    vc = round(p * rng.choice([0.4, 0.5, 0.6]), 2)
    cpu = p - vc
    be = rng.choice([1_000, 2_000, 2_500, 4_000])
    fc = round(cpu * be)
    q = int(be * rng.choice([1.25, 1.5, 1.6, 2]))
    mos = q - be
    if slot.d <= 2:
        return dict(stem=f'{f_}\'s break-even quantity is {be:,} units and it expects to sell {q:,} units. Calculate the margin of safety.',
                    answer=f'{mos:,} units', markingKey=MK(f'{q:,} − {be:,} = {mos:,}.', f'{mos:,} units'), marks=2)
    tp = rng.choice([10_000, 20_000, 25_000, 40_000])
    tq = (fc + tp) / cpu
    tq_r = int(-(-(fc + tp) // cpu))
    tprice = vc + (fc + tp) / q
    stem = (f'{f_} sells a product for {m(p, c)}, with variable cost of {m(vc, c)} per unit and fixed costs of {m(fc, c)}. Expected sales are {q:,} units. '
            f'Calculate the break-even quantity, the margin of safety, the output needed to make a target profit of {m(tp, c)}, and the price needed to make that target profit at expected sales.')
    ans = (f'Break-even = {m(fc, c)}/{m(cpu, c)} = {be:,} units; margin of safety = {q:,} − {be:,} = {mos:,} units ({p1(100 * mos / q)}% of sales); ' +
           (f'target output = ({m(fc, c)} + {m(tp, c)})/{m(cpu, c)} = {tq_r:,} units; ' if abs(tq - tq_r) < 1e-9 else f'target output = ({m(fc, c)} + {m(tp, c)})/{m(cpu, c)} = {p1(tq)} → {tq_r:,} units (rounded up); ') +
           f'target price = {m(vc, c)} + ({m(fc, c)} + {m(tp, c)})/{q:,} = {c}{p2(tprice)}.')
    if slot.d >= 4:
        nf = int(fc * 1.2)
        nbe = nf / cpu
        stem += f' Fixed costs then rise by 20%. Calculate the new break-even quantity and comment on the effect on risk.'
        ans += f' New fixed costs {m(nf, c)}; new break-even = {p1(nbe)} → {int(-(-nf // cpu)):,} units (rounded up); the margin of safety falls, so the business is more exposed to a fall in sales.'
    return dict(stem=stem, answer=ans,
                markingKey=MK('break-even = FC/contribution; MoS = sales − break-even; target output = (FC + target profit)/contribution; target price = VC + (FC + target profit)/expected sales.', 'all values') + (' [1] new break-even; [1] comment.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch10-st2', concepts=('change', 'creativity'),
  terms=[('break-even chart', 'a graph showing total revenue, total costs and fixed costs against output, used to find the break-even point and profit or loss at each level of output'),
         ('margin of safety', 'the amount by which actual or forecast sales exceed the break-even quantity'),
         ('target profit output', 'the number of units needed to reach a given profit: (fixed costs + target profit) / contribution per unit'),
         ('target price', 'the price needed to reach a target profit at a given level of sales'),
         ('profit area', 'the area on a break-even chart to the right of the break-even point, between the total revenue and total cost lines')],
  facts=[('Break-even is 3,000 units and sales are 4,500 units. The margin of safety is:', '1,500 units', ['7,500 units', '3,000 units', '0.67 units'], '4,500 − 3,000.'),
         ('A price increase (with no change in costs) will make the break-even point:', 'lower', ['higher', 'unchanged', 'negative'], 'Contribution per unit rises.'),
         ('Fixed costs $30,000, contribution $15, target profit $15,000. Target output is:', '3,000 units', ['2,000 units', '1,000 units', '4,500 units'], '(30,000 + 15,000)/15.')],
  why=[('Explain why a large margin of safety reduces risk.', 'Sales can fall a long way before the business makes a loss, so it is better able to cope with a downturn or competition.'),
       ('Explain why a rise in fixed costs increases the break-even quantity.', 'More contribution is needed to cover the higher fixed costs, so more units must be sold before a profit is made.'),
       ('Explain why a price rise may not increase profit even though it lowers break-even.', 'Higher prices may reduce the quantity sold if demand is price elastic, so total contribution may fall.')],
  contrast=[('the break-even point', 'the margin of safety', 'The break-even point is the output at which total revenue equals total cost; the margin of safety is how far actual sales exceed that point.')],
  misc=[('A business with a large margin of safety cannot make a loss.', 'Sales and costs can change; a sharp fall in demand or rise in costs can still eliminate the margin of safety.')],
  cases=[('Peloton\'s sales collapse', 'Peloton\'s sales boomed during Covid-19 lockdowns, then fell sharply in 2022 after it had expanded capacity, leading to large losses.', 'margin of safety', 'high fixed costs from expansion left little margin of safety when demand fell'),
         ('energy costs in 2022', 'In 2022 many European bakeries and manufacturers saw energy bills rise several-fold, forcing price rises or closures.', 'changes in costs and break-even', 'rising costs pushed up break-even output, squeezing margins of safety'),
         ('Netflix price rises', 'Netflix raised the price of its US Standard plan from $13.99 to $15.49 in 2022 while still adding subscribers globally.', 'changes in price and break-even', 'a higher price raised contribution per subscriber, lowering the subscribers needed to cover fixed content costs')],
  apply=[('A theatre has fixed costs of $60,000 per production. Tickets sell for $40 with variable costs of $10 per ticket. Expected sales are 2,800 tickets. Calculate the break-even number of tickets, the margin of safety and the profit.', 'Contribution = $30; break-even = 60,000/30 = 2,000 tickets; margin of safety = 800 tickets; profit = 800 × 30 = $24,000.', 4)],
  evaluate=[('Break-even analysis is more useful for start-ups than for established businesses.', ['start-ups need to know the sales required to survive', 'supports finance applications', 'simple'],
             ['established firms use it for pricing and cost changes', 'what-if analysis', 'multi-product firms find it hard to apply', 'other tools such as budgets may be better'], 'It is especially valuable for start-ups, but established firms also use it for decisions about prices, costs and new products.')],
  )


@calc('ch10-st3', 'C3', (1, 5))
def make_or_buy(rng, slot):
    f_ = firm(rng)
    c = cur(rng)
    if slot.d <= 2 or rng.random() < 0.4:
        cap_ = rng.choice([5_000, 8_000, 10_000, 12_000, 20_000])
        out = int(cap_ * rng.choice([0.55, 0.6, 0.72, 0.8, 0.85, 0.9]))
        cu = 100 * out / cap_
        if slot.d <= 2:
            return dict(stem=f'{f_}\'s factory can produce {cap_:,} units a month and currently produces {out:,}. Calculate capacity utilisation.',
                        answer=pct(cu), markingKey=MK(f'{out:,}/{cap_:,} × 100 = {p1(cu)}%.', pct(cu)), marks=2)
        fc = rng.choice([40_000, 60_000, 80_000])
        new_out = int(cap_ * 0.9)
        stem = (f'{f_}\'s factory can produce {cap_:,} units a month. It produces {out:,} units and has fixed costs of {m(fc, c)} a month. '
                f'Calculate capacity utilisation and fixed cost per unit, and the fixed cost per unit if output rose to {new_out:,} units.')
        ans = f'Capacity utilisation = {p1(cu)}%; fixed cost per unit = {m(fc, c)}/{out:,} = {c}{p2(fc / out)}; at {new_out:,} units: {c}{p2(fc / new_out)} (utilisation 90%).'
        if slot.d >= 4:
            stem += ' Explain one problem of operating at close to 100% capacity.'
            ans += ' Problem: no time for maintenance, staff overwork and stress, and inability to take extra orders.'
        return dict(stem=stem, answer=ans,
                    markingKey=MK(f'{out:,}/{cap_:,} × 100; {fc:,}/{out:,}; {fc:,}/{new_out:,}.', 'all values') + (' [1][1] problem explained.' if slot.d >= 4 else ''),
                    marks=4 if slot.d <= 3 else 6)
    q = rng.choice([2_000, 5_000, 10_000])
    vc = rng.choice([4, 5, 6, 8])
    extra_fc = rng.choice([10_000, 15_000, 20_000, 30_000])
    buy = round(vc + rng.choice([-1, 1, 2, 3]) + rng.choice([0, 0.5]), 2)
    make = vc * q + extra_fc
    buyt = buy * q
    better = 'make' if make < buyt else 'buy'
    stem = (f'{f_} needs {q:,} components a year. Making them in-house would cost {m(vc, c)} per unit in variable costs plus {m(extra_fc, c)} a year in extra fixed costs. '
            f'A supplier will sell them for {m(buy, c)} each. Calculate the cost of making and the cost of buying, and state which is cheaper.')
    ans = f'Make: {q:,} × {m(vc, c)} + {m(extra_fc, c)} = {m(make, c)}; buy: {q:,} × {m(buy, c)} = {m(round(buyt), c)}. It is cheaper to {better}, saving {m(round(abs(make - buyt)), c)}.'
    if slot.d >= 4:
        stem += ' Explain two qualitative factors that should influence the decision.'
        ans += ' Qualitative factors: quality control and reliability of the supplier, spare capacity and skills in-house, confidentiality of designs, and flexibility to change volumes.'
    return dict(stem=stem, answer=ans,
                markingKey=MK(f'make = {q:,} × {vc} + {extra_fc:,}; buy = {q:,} × {buy:g}.', 'both totals and the decision') + (' [1][1] qualitative factors.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch10-st3', concepts=('change', 'sustainability'),
  terms=[('make-or-buy decision', 'the choice between producing a component or service in-house and buying it from an external supplier'),
         ('cost to make', 'the cost of producing in-house: variable costs plus any extra fixed costs'),
         ('cost to buy', 'the price paid to the supplier multiplied by the quantity needed'),
         ('capacity utilisation', 'actual output as a percentage of the maximum possible output: actual output / productive capacity × 100'),
         ('productive capacity', 'the maximum output a business can produce in a period with its existing resources')],
  facts=[('A factory can produce 10,000 units and produces 7,500. Capacity utilisation is:', '75%', ['133%', '25%', '7.5%'], '7,500/10,000 × 100.'),
         ('High capacity utilisation usually leads to:', 'lower fixed cost per unit', ['higher fixed cost per unit', 'higher total fixed costs', 'no change in unit costs'], 'Fixed costs are spread over more units.'),
         ('Which favours buying a component rather than making it?', 'A specialist supplier offers lower cost and reliable quality', ['The firm has lots of spare capacity and skilled staff', 'The design must be kept secret', 'The supplier is unreliable'], 'Buying suits non-core items where suppliers are efficient.')],
  why=[('Explain why low capacity utilisation can reduce profitability.', 'Fixed costs are spread over fewer units, so unit costs rise; workers and machines are idle.'),
       ('Explain why operating at 100% capacity can cause problems.', 'There is no time for maintenance, staff may be overworked, and the firm cannot accept extra orders or cope with breakdowns.'),
       ('Explain why a firm might make a component even if buying it is cheaper.', 'It may want control over quality, delivery and confidential designs, or to use spare capacity and keep skilled staff employed.')],
  contrast=[('the cost to make', 'the cost to buy', 'The cost to make includes in-house variable costs plus any extra fixed costs; the cost to buy is the supplier\'s price times the quantity.')],
  misc=[('Capacity utilisation of 100% is always the target.', 'Most firms aim for about 85-95% to allow maintenance, flexibility and new orders.')],
  cases=[('Tesla\'s in-house batteries', 'Tesla buys battery cells from suppliers such as Panasonic and CATL but also began making its own 4680 cells.', 'make-or-buy decisions', 'making key components in-house can secure supply and technology, but requires large investment'),
         ('hotel occupancy rates', 'Hotels track occupancy (capacity utilisation); average hotel occupancy in many European cities was around 70-80% in 2023.', 'capacity utilisation', 'empty rooms still incur fixed costs, so hotels use pricing to raise occupancy'),
         ('Apple\'s own chips', 'In 2020 Apple began replacing Intel processors in Macs with its own M1 chips, designed in-house and made by TSMC.', 'make-or-buy', 'designing chips in-house gave Apple control over performance and integration')],
  apply=[('A cinema has 400 seats and shows 4 films a day. Average attendance is 960 a day. Calculate capacity utilisation and suggest two ways to increase it.', 'Capacity = 1,600 seats a day; utilisation = 960/1,600 = 60%. Ways: discounted daytime tickets, special events, or renting screens for business conferences and gaming.', 4)],
  evaluate=[('A business should always buy components if a supplier is cheaper.', ['lower cost', 'focus on core activities', 'supplier expertise'],
             ['quality and reliability risk', 'loss of control and confidentiality', 'spare capacity in-house', 'supplier price rises later'], 'Cost is central, but strategic control, quality and supply risk may justify making components in-house.')],
  )


@calc('ch10-st4', 'C3', (1, 5))
def stock_control(rng, slot):
    f_ = firm(rng)
    use = rng.choice([100, 150, 200, 250, 400])
    lead = rng.choice([2, 3, 4, 5])
    buffer_ = use * rng.choice([1, 2, 3])
    rol = use * lead + buffer_
    if slot.d <= 2:
        return dict(stem=f'{f_} uses {use} units of stock a week. The supplier\'s lead time is {lead} weeks and the buffer stock is {buffer_:,} units. Calculate the reorder level.',
                    answer=f'{rol:,} units', markingKey=MK(f'{use} × {lead} + {buffer_} = {rol:,}.', f'{rol:,} units'), marks=2)
    maxs = buffer_ + use * rng.choice([6, 8, 10])
    roq = maxs - buffer_
    weeks = roq // use
    stem = (f'{f_} uses {use} units a week. Buffer stock is {buffer_:,} units, the maximum stock level is {maxs:,} units and the lead time is {lead} weeks. '
            'Calculate the reorder level, the reorder quantity, and how many weeks pass between deliveries. Describe the stock control chart.')
    ans = (f'Reorder level = {use} × {lead} + {buffer_:,} = {rol:,} units; reorder quantity = {maxs:,} − {buffer_:,} = {roq:,} units; time between deliveries = {roq:,}/{use} = {weeks} weeks. '
           f'Chart: stock falls in a straight line from {maxs:,} at {use} a week; an order is placed when it reaches {rol:,}; the delivery arrives {lead} weeks later as stock reaches {buffer_:,} and returns it to {maxs:,} (saw-tooth pattern).')
    if slot.d >= 4:
        stem += ' Explain one consequence of the supplier\'s lead time increasing unexpectedly.'
        ans += f' If lead time rises, buffer stock is used up and the firm may run out (stock-out), halting production or losing sales.'
    return dict(stem=stem, answer=ans,
                markingKey=MK('reorder level = usage × lead time + buffer; reorder quantity = max − buffer; interval = reorder quantity / usage.', 'all three values') + ' [1] chart described with labels.' + (' [1] consequence.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch10-st4', concepts=('change', 'sustainability'),
  terms=[('supply chain', 'the network of organizations and processes involved in producing and delivering a product, from raw materials to the final customer'),
         ('local supply chain', 'a supply chain in which suppliers are located near the business'),
         ('global supply chain', 'a supply chain with suppliers and production in several countries'),
         ('buffer stock', 'the minimum stock held to cope with unexpected demand or delays in delivery'),
         ('reorder level', 'the stock level at which a new order is placed: usage per period × lead time + buffer stock'),
         ('lead time', 'the time between placing an order and receiving the delivery'),
         ('reorder quantity', 'the amount of stock ordered each time: maximum stock level − buffer stock (on a simple stock chart)'),
         ('stock-out', 'running out of stock, causing lost sales or stopped production')],
  facts=[('Usage 50 units a day, lead time 4 days, buffer stock 100. The reorder level is:', '300 units', ['200 units', '154 units', '400 units'], '50 × 4 + 100.'),
         ('On a stock control chart, stock usually follows a:', 'saw-tooth pattern', ['horizontal line', 'bell curve', 'pie shape'], 'Stock falls with usage and jumps with each delivery.'),
         ('Holding too much stock leads to:', 'high storage costs and risk of waste or obsolescence', ['frequent stock-outs', 'lost sales', 'idle machines from lack of materials'], 'Excess stock ties up cash.')],
  why=[('Explain why businesses hold buffer stock.', 'To avoid stock-outs if demand rises unexpectedly or deliveries are late, protecting sales and production.'),
       ('Explain why global supply chains can increase risk.', 'Long distances, many countries and transport links expose firms to delays, political problems, exchange-rate changes and disasters.'),
       ('Explain why a just-in-case approach increases costs.', 'Holding more stock raises storage, insurance and wastage costs and ties up cash that could be used elsewhere.')],
  contrast=[('a local supply chain', 'a global supply chain', 'A local supply chain uses nearby suppliers, giving shorter lead times and lower transport emissions; a global supply chain uses suppliers around the world, often at lower cost but with more risk and longer lead times.'),
            ('JIT', 'JIC', 'JIT holds minimal stock and relies on frequent deliveries; JIC holds buffer stocks in case of unexpected demand or supply problems.')],
  misc=[('The reorder level is the same as the buffer stock.', 'The reorder level is higher: it includes the stock used during the lead time plus the buffer stock.')],
  cases=[('the Suez Canal blockage', 'In March 2021 the container ship Ever Given blocked the Suez Canal for six days, holding up an estimated $9 bn of trade a day.', 'risks of global supply chains', 'a single disruption delayed deliveries worldwide, showing the value of buffer stock'),
         ('Zara\'s local supply chain', 'Zara produces much of its fashion in Spain, Portugal, Morocco and Turkey, close to its headquarters, so new designs reach stores within weeks.', 'local supply chains', 'nearby production gives speed and flexibility at higher labour cost'),
         ('the UK fuel crisis of 2021', 'In September 2021 a shortage of lorry drivers and panic buying left many UK petrol stations without fuel.', 'stock-outs', 'low stocks and supply problems combined with a surge in demand caused shortages')],
  apply=[('A café uses 40 litres of milk a day. The supplier delivers 2 days after an order, and the café keeps 20 litres as buffer stock. Calculate the reorder level and explain one risk of holding too much milk.', 'Reorder level = 40 × 2 + 20 = 100 litres. Risk: milk is perishable, so excess stock may go off, wasting money.', 3)],
  evaluate=[('Global supply chains should be replaced by local supply chains.', ['shorter lead times', 'less disruption risk', 'lower emissions', 'support local economy'],
             ['higher costs', 'some inputs only available abroad', 'less choice of suppliers', 'diversification may be better'], 'Firms are rebalancing towards local and diversified supply for critical inputs, but global supply chains remain essential for cost and availability.')],
  )


# =============================================================================================
# ch11 Unit 5.7-5.9 Crisis management, R&D and management information systems (HL)
# =============================================================================================
S('ch11-st1', concepts=('change', 'ethics'),
  terms=[('crisis', 'an unexpected event that threatens a business\'s operations, reputation or survival'),
         ('crisis management', 'the steps an organization takes to limit the damage from a crisis as it happens'),
         ('contingency planning', 'planning in advance for possible future events or crises, so the business can respond quickly'),
         ('transparency (in a crisis)', 'communicating openly and honestly with stakeholders about what has happened'),
         ('business continuity', 'the ability to keep essential operations running during and after a crisis')],
  facts=[('Contingency planning takes place:', 'before a crisis happens', ['only after a crisis', 'only during a crisis', 'never in large firms'], 'It prepares for possible events.'),
         ('Which is a key principle of effective crisis management?', 'Speed and transparency of communication', ['Denying the problem', 'Delaying any statement', 'Blaming customers'], 'Fast, honest communication limits damage.'),
         ('Johnson & Johnson\'s 1982 Tylenol recall is often cited as an example of:', 'effective crisis management', ['ignoring a crisis', 'price skimming', 'offshoring'], 'It recalled 31 million bottles and introduced tamper-proof packaging.')],
  why=[('Explain why contingency planning can reduce the costs of a crisis.', 'Pre-agreed actions, responsibilities and resources allow a quick response, limiting disruption, financial losses and reputational damage.'),
       ('Explain why contingency planning has costs.', 'Time, money and staff are needed to identify risks, write plans, train staff and hold back-up resources for events that may never happen.'),
       ('Explain why speed of response matters in a crisis.', 'Social media spreads news immediately, so slow or unclear responses allow rumours and anger to grow, worsening damage.')],
  contrast=[('crisis management', 'contingency planning', 'Contingency planning prepares for possible crises in advance; crisis management is the response while the crisis is happening.')],
  misc=[('Contingency planning can prevent all crises.', 'It cannot prevent unexpected events; it prepares the firm to respond and limit damage.')],
  cases=[('the Tylenol recall', 'In 1982 Johnson & Johnson recalled about 31 million bottles of Tylenol after seven deaths from tampered capsules, and relaunched with tamper-proof packaging.', 'crisis management', 'putting customer safety first and communicating openly protected the brand'),
         ('BP\'s Deepwater Horizon oil spill', 'In 2010 the Deepwater Horizon explosion killed 11 workers and caused the largest marine oil spill in US history; BP\'s CEO was criticised for saying "I\'d like my life back".', 'poor crisis communication', 'insensitive communication worsened the reputational damage of a major disaster'),
         ('the 2024 CrowdStrike outage', 'In July 2024 a faulty CrowdStrike software update crashed about 8.5 million Windows computers, grounding flights and disrupting hospitals worldwide.', 'contingency planning', 'organizations with back-up systems and recovery plans restored services faster')],
  apply=[('A food manufacturer discovers that a batch of products may be contaminated. Outline the steps of an effective crisis response.', 'Recall affected products immediately; inform customers and regulators transparently; set up a helpline; investigate the cause; fix the process; communicate updates; review the contingency plan afterwards.', 4)],
  evaluate=[('Contingency planning is a waste of resources because crises are unpredictable.', ['plans may not match the actual crisis', 'costly', 'may never be used'],
             ['reduces response time and damage', 'protects reputation', 'required by regulators in some sectors', 'flexible plans still help'], 'Although no plan fits every crisis, contingency planning greatly improves response and is usually worth its cost.')],
  )


@calc('ch11-st2', 'C3', (2, 5))
def rd_intensity(rng, slot):
    c = cur(rng)
    rev = rng.choice([200, 400, 500, 800, 1_000])
    rd = rng.choice([10, 20, 30, 40, 60, 80])
    rev2 = rev * rng.choice([1.05, 1.1, 1.2])
    rd2 = rd * rng.choice([1.25, 1.5, 2])
    i1 = 100 * rd / rev
    i2 = 100 * rd2 / rev2
    stem = (f'A firm had revenue of {m(rev, c)} m and spent {m(rd, c)} m on research and development (R&D). Next year revenue is {m(round(rev2, 1), c)} m and R&D spending {m(round(rd2, 1), c)} m. '
            'Calculate R&D spending as a percentage of revenue (R&D intensity) in each year and comment on the change.')
    ans = f'Year 1: {rd}/{rev} × 100 = {p1(i1)}%; year 2: {rd2:g}/{rev2:g} × 100 = {p1(i2)}%. R&D intensity has risen, suggesting a focus on innovation, though returns are uncertain and profit may fall in the short run.'
    if slot.d >= 4:
        stem += ' Explain one way the firm could protect the results of its R&D.'
        ans += ' It could apply for patents (for inventions), trademarks (for brand names) or keep processes as trade secrets.'
    return dict(stem=stem, answer=ans,
                markingKey=MK('R&D / revenue × 100 for each year.', 'both percentages') + ' [1] comment.' + (' [1] protection method.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 5)


S('ch11-st2', concepts=('creativity', 'change', 'ethics'),
  terms=[('research and development (R&D)', 'investigating and developing new products, processes or technologies'),
         ('product innovation', 'introducing a new or significantly improved good or service'),
         ('process innovation', 'introducing a new or improved method of production or delivery'),
         ('incremental innovation', 'small improvements to existing products or processes'),
         ('disruptive innovation', 'an innovation that creates a new market or transforms an existing one, displacing established firms'),
         ('intellectual property (IP)', 'creations of the mind, such as inventions, designs, brands and creative works, that can be legally protected'),
         ('patent', 'a legal right that gives an inventor the exclusive right to make and sell an invention for a set period, usually 20 years'),
         ('copyright', 'a legal right protecting original creative works, such as books, music, films and software')],
  facts=[('Streaming replacing DVD rental is an example of:', 'disruptive innovation', ['incremental innovation', 'quality control', 'a loss leader'], 'It transformed the market and displaced Blockbuster.'),
         ('A patent usually lasts for about:', '20 years', ['5 years', '100 years', 'forever'], 'Then the invention can be copied.'),
         ('A brand name such as "Nike" is protected by:', 'a trademark', ['a patent', 'copyright', 'a franchise'], 'Trademarks protect names and logos.'),
         ('Which company spent the most on R&D in 2023, at over $80 bn?', 'Amazon', ['Coca-Cola', 'McDonald\'s', 'Walmart'], 'Large tech firms dominate R&D spending.')],
  why=[('Explain why R&D is important for businesses in fast-changing markets.', 'New technologies and changing tastes shorten product life cycles, so firms must keep developing new products to stay competitive.'),
       ('Explain why intellectual property protection encourages innovation.', 'Patents and copyright let firms earn returns from their inventions without immediate copying, so they are willing to invest in costly R&D.'),
       ('Explain why R&D is risky.', 'It is expensive, takes years and many projects fail, so returns are uncertain and cash flow suffers in the meantime.')],
  contrast=[('product innovation', 'process innovation', 'Product innovation creates new or improved goods and services for customers; process innovation improves how products are made or delivered, often cutting costs.'),
            ('incremental innovation', 'disruptive innovation', 'Incremental innovation improves existing products step by step; disruptive innovation creates new markets or transforms existing ones.')],
  misc=[('A patent protects an idea forever.', 'Patents last for a limited period, usually 20 years, and must be applied for and defended; after that, others can copy the invention.')],
  cases=[('Kodak and the digital camera', 'A Kodak engineer invented the digital camera in 1975, but Kodak focused on film and filed for bankruptcy in 2012.', 'disruptive innovation', 'failing to commercialise its own innovation let a new technology destroy its core market'),
         ('Moderna\'s mRNA vaccine', 'Moderna, which had spent about a decade on mRNA research, developed its Covid-19 vaccine within a year in 2020.', 'R&D and innovation', 'long-term R&D investment allowed rapid product development when demand emerged'),
         ('Apple v Samsung patents', 'In 2018 Apple and Samsung settled a seven-year patent dispute over smartphone designs, after a jury had awarded Apple over $500 m.', 'intellectual property', 'patents on design features are valuable assets that firms defend in court')],
  apply=[('A start-up has invented a new type of reusable coffee cup. Explain two ways it could protect its intellectual property.', 'A patent for the new technical design; a registered design right for its appearance; a trademark for its brand name and logo; copyright for its marketing materials.', 4)],
  evaluate=[('Spending heavily on R&D is the best way for a business to stay competitive.', ['new products and USPs', 'patents create barriers to entry', 'long-term growth'],
             ['high cost and risk', 'many projects fail', 'imitation or acquisition can be cheaper', 'marketing and efficiency also matter'], 'R&D is vital in technology-driven markets, but it must be well managed and commercialised; other sources of advantage may suit other markets.')],
  )

S('ch11-st3', concepts=('ethics', 'change', 'creativity'),
  terms=[('management information system (MIS)', 'a system that collects, stores and processes data to give managers the information they need to make decisions'),
         ('data analytics', 'examining data to find patterns, trends and insights that support decisions'),
         ('big data', 'very large and complex data sets that require advanced tools to analyse'),
         ('cybersecurity', 'protecting computer systems, networks and data from attacks, damage or unauthorised access'),
         ('artificial intelligence (AI)', 'computer systems that perform tasks normally requiring human intelligence, such as recognising patterns, making predictions and generating text'),
         ('data mining', 'searching large data sets to discover patterns and relationships')],
  facts=[('A supermarket analysing loyalty-card data to target offers is using:', 'data analytics', ['quality circles', 'cost-plus pricing', 'kaizen'], 'Data is used to find patterns.'),
         ('Which is a major risk of holding large amounts of customer data?', 'Cyberattacks and data breaches', ['Lower sales', 'Higher tariffs', 'Increased product life'], 'Breaches damage trust and incur fines.'),
         ('Under the EU\'s GDPR, a firm can be fined up to:', '4% of global annual revenue (or €20 m, whichever is higher)', ['$100', '0.01% of profit', 'nothing'], 'Serious breaches are heavily fined.')],
  why=[('Explain why management information systems improve decision-making.', 'They give managers accurate, timely and relevant information, so decisions are based on evidence rather than guesswork.'),
       ('Explain why AI raises ethical issues for businesses.', 'AI may make biased decisions, replace jobs, misuse personal data and be hard to explain, raising questions of fairness and accountability.'),
       ('Explain why cybersecurity is a growing concern for businesses.', 'More data and operations are online, so attacks can stop operations, steal data and cause financial and reputational damage.')],
  contrast=[('data', 'information', 'Data is raw facts and figures; information is data that has been processed and organised so that it is useful for decisions.')],
  misc=[('More data always leads to better decisions.', 'Data must be accurate, relevant and well analysed; too much data can cause information overload and false patterns.')],
  cases=[('the British Airways data breach', 'In 2018 hackers stole personal and payment data of about 400,000 British Airways customers; the UK regulator fined BA £20 m.', 'cybersecurity', 'weak security led to fines and lost customer trust'),
         ('Amazon\'s recruitment AI', 'Amazon abandoned an AI recruitment tool in 2018 after finding it favoured male candidates because it had been trained on past hiring data.', 'ethics of AI', 'AI can reproduce bias in its training data, creating unfair decisions'),
         ('Tesco Clubcard data', 'Tesco\'s Clubcard, launched in 1995, collects shopping data from millions of customers to personalise offers and plan stock.', 'data analytics', 'customer data supports targeted marketing and better operations decisions')],
  apply=[('A chain of gyms wants to use data analytics. Suggest two ways it could use members\' data and one ethical issue it must consider.', 'Uses: identify peak times to plan staffing and classes; predict which members may cancel and offer them incentives. Ethical issue: consent and privacy of health and location data; secure storage under data-protection law.', 4)],
  evaluate=[('Artificial intelligence will bring more benefits than costs to businesses.', ['productivity and lower costs', 'better predictions and personalisation', 'new products'],
             ['job losses and resistance', 'bias and errors', 'data privacy and cybersecurity risks', 'cost of implementation'], 'AI is likely to bring large benefits, but firms must manage risks of bias, privacy and job displacement through ethical policies and training.')],
  )


# =============================================================================================
# ch12 Paper 1 pre-released statement and Paper 3 social enterprise skills
# =============================================================================================
S('ch12-st1', concepts=('change', 'creativity', 'ethics', 'sustainability'),
  terms=[('pre-released statement', 'a short statement about the Paper 1 case study published about four months before the exam, giving the context and key issues'),
         ('stakeholder analysis', 'identifying the stakeholders in a case, their interests, power and likely conflicts'),
         ('STEEPLE analysis', 'a tool for analysing the external environment: social, technological, economic, environmental, political, legal and ethical factors'),
         ('SWOT analysis', 'a tool for analysing internal strengths and weaknesses and external opportunities and threats'),
         ('command term', 'a word in an exam question, such as "explain", "analyse" or "evaluate", that indicates the depth of answer required')],
  facts=[('The Paper 1 pre-released statement is published:', 'about four months before the exam', ['on the day of the exam', 'after the exam', 'one year after the exam'], 'Students research the context in advance.'),
         ('Which command term requires a judgement weighing strengths and limitations?', 'Evaluate', ['Define', 'State', 'Describe'], 'Evaluate requires a balanced judgement.'),
         ('A STEEPLE analysis looks at:', 'the external environment of the business', ['only internal strengths', 'only the finances', 'only the organization chart'], 'All seven factors are external.')],
  why=[('Explain why researching the context of the pre-released statement is useful.', 'Understanding the industry, typical stakeholders and likely issues helps students apply knowledge quickly and accurately to the unseen case in the exam.'),
       ('Explain why students should not memorise answers about real companies for Paper 1.', 'The exam case is fictional and contains new information, so answers must be applied to the case, not to real firms.'),
       ('Explain why stakeholder analysis is useful preparation for Paper 1.', 'Most cases involve decisions that affect several stakeholders, and evaluation questions reward considering their interests and conflicts.')],
  contrast=[('SWOT analysis', 'STEEPLE analysis', 'SWOT covers both internal (strengths, weaknesses) and external (opportunities, threats) factors; STEEPLE examines only the external environment, in more detail.'),
            ('"analyse"', '"evaluate"', '"Analyse" means breaking down an issue to show its parts and links; "evaluate" goes further by weighing strengths and limitations to reach a judgement.')],
  misc=[('In Paper 1, the more theory you write the higher your mark.', 'Marks reward relevant theory applied to the case; generic answers without reference to the case score low.')],
  cases=[('a pre-released statement on a social enterprise', 'A pre-released statement might introduce a social enterprise expanding fair-trade coffee sales in new markets, mentioning stakeholders and sustainability issues.', 'researching the pre-released statement', 'students should research fair trade, international expansion, stakeholders and possible finance issues'),
         ('a pre-released statement on an e-scooter firm', 'A pre-released statement might describe a start-up renting e-scooters in cities, facing new regulations and competition.', 'using STEEPLE to prepare', 'legal, environmental and technological factors are likely themes'),
         ('a pre-released statement on a family hotel', 'A pre-released statement might describe a family-owned hotel considering growth, with tension between family members and new managers.', 'stakeholder and ownership issues', 'likely issues include ownership change, leadership, finance and conflict between stakeholders')],
  apply=[('A pre-released statement describes a family-owned bakery planning to open cafés in other cities. Identify three issues the case is likely to explore and one tool you would prepare for each.', 'Growth and finance (sources of finance, investment appraisal); organizational change and leadership (force field analysis, leadership styles); marketing in new locations (STEEPLE, market research, the marketing mix).', 6)],
  evaluate=[('Research on the pre-released statement is more important than practising exam technique for Paper 1.', ['context helps application', 'knowledge of industry issues', 'confidence'],
             ['the case contains new information', 'command terms and timing determine marks', 'application to the case is assessed', 'both are needed'], 'Research helps, but exam technique – applying theory to the case under timed conditions – earns the marks; students need both.')],
  )


@calc('ch12-st2', 'C3', (2, 5))
def critical_path(rng, slot):
    # A -> B -> D -> F and A -> C -> E -> F; G parallel to (D) after B
    a, b, c_, d, e, f, g = (rng.choice(r) for r in ([2, 3, 4], [3, 4, 5, 6], [2, 3, 4], [4, 5, 6], [3, 5, 7, 8], [1, 2, 3], [2, 3]))
    acts = [('A', 'Design', a, 'none'), ('B', 'Order equipment', b, 'A'), ('C', 'Recruit staff', c_, 'A'), ('D', 'Install equipment', d, 'B'),
            ('E', 'Train staff', e, 'C'), ('G', 'Test systems', g, 'B'), ('F', 'Launch', f, 'D, E, G')]
    es = {'A': 0}
    es['B'] = a
    es['C'] = a
    es['D'] = a + b
    es['G'] = a + b
    es['E'] = a + c_
    es['F'] = max(es['D'] + d, es['E'] + e, es['G'] + g)
    total = es['F'] + f
    lf = {'F': total}
    lf['D'] = lf['E'] = lf['G'] = total - f
    lf['B'] = min(lf['D'] - d, lf['G'] - g)
    lf['C'] = lf['E'] - e
    lf['A'] = min(lf['B'] - b, lf['C'] - c_)
    dur = {k: v for k, _, v, _ in acts}
    tf = {k: lf[k] - dur[k] - es[k] for k in dur}
    crit = [k for k in ['A', 'B', 'C', 'D', 'E', 'G', 'F'] if tf[k] == 0]
    def wk(v):
        return f'{v} week' + ('' if v == 1 else 's')
    tab = '; '.join((f'{k} {n} ({wk(v)}, no predecessor)' if p == 'none' else f'{k} {n} ({wk(v)}, after {p})') for k, n, v, p in acts)
    stem = f'A firm is opening a new branch. Activities: {tab}. Calculate the earliest start time of each activity, the minimum project duration and the critical path, and the total float of each non-critical activity.'
    if slot.d >= 4:
        stem += ' Explain one benefit of critical path analysis to the project manager.'
    order = ['A', 'B', 'C', 'D', 'E', 'G', 'F']
    path = ('A–B–D–F' if tf['D'] == 0 else '') + (' and ' if tf['D'] == 0 and tf['E'] == 0 else '') + ('A–C–E–F' if tf['E'] == 0 else '')
    if tf['G'] == 0:
        path = (path + ' and ' if path else '') + 'A–B–G–F'
    ans = ('Earliest start times: ' + ', '.join(f'{k} {es[k]}' for k in order) + f'. Minimum duration = {total} weeks. Critical path: {path}. Float: ' +
           (', '.join(f'{k} {wk(tf[k])}' for k in order if tf[k] > 0) or 'none') + '.')
    if slot.d >= 4:
        ans += ' Benefit: it shows which activities cannot be delayed without delaying the whole project, so managers can focus resources on them and schedule non-critical tasks flexibly.'
    return dict(stem=stem, answer=ans,
                markingKey=MK('EST = latest finish of preceding activities; LFT worked backwards; total float = LFT − duration − EST; critical activities have zero float.', f'duration {total} weeks and the critical path') + (' [1][1] benefit explained.' if slot.d >= 4 else ''),
                marks=4 if slot.d <= 3 else 6)


S('ch12-st2', concepts=('change', 'creativity', 'ethics', 'sustainability'),
  terms=[('business management toolkit', 'the set of analytical tools in the IB course, such as SWOT, STEEPLE, Ansoff matrix, decision trees, force field analysis, critical path analysis and Porter\'s generic strategies'),
         ('critical path analysis (CPA)', 'a planning tool that shows the order and duration of a project\'s activities and identifies the sequence of activities that determines the minimum project duration'),
         ('critical path', 'the sequence of activities with zero float, any delay to which delays the whole project'),
         ('total float', 'the amount of time an activity can be delayed without delaying the whole project: latest finish time − duration − earliest start time'),
         ('Ansoff matrix', 'a tool for analysing growth strategies: market penetration, product development, market development and diversification'),
         ('Porter\'s generic strategies', 'cost leadership, differentiation and focus as ways to gain competitive advantage')],
  facts=[('Activities on the critical path have a total float of:', 'zero', ['one week', 'the project duration', 'any positive value'], 'They cannot be delayed.'),
         ('Selling a new product to a new market is which Ansoff strategy?', 'Diversification', ['Market penetration', 'Product development', 'Market development'], 'New product + new market.'),
         ('In a Paper 1 case, a question asking you to "apply" a tool requires:', 'using the tool with information from the case', ['defining the tool only', 'listing tools', 'writing about a real company'], 'Application to the case is needed.'),
         ('An activity with EST 4, duration 3 and LFT 10 has a total float of:', '3', ['7', '4', '10'], '10 − 3 − 4 = 3.')],
  why=[('Explain why business management tools improve the quality of answers to case-study questions.', 'Tools give a structured way to organise case evidence, identify key issues and support judgements, showing knowledge and application.'),
       ('Explain why critical path analysis helps managers plan a project.', 'It shows the order of activities, the minimum duration and which activities are critical, so resources can be focused and delays anticipated.'),
       ('Explain why a tool should be chosen to fit the question.', 'Each tool answers a different kind of question – e.g. Ansoff for growth strategy, decision trees for choices under risk – so the wrong tool gives irrelevant analysis.')],
  contrast=[('critical activities', 'non-critical activities', 'Critical activities have zero float and any delay extends the project; non-critical activities have float and can be delayed by up to that amount without affecting completion.'),
            ('a decision tree', 'the Ansoff matrix', 'A decision tree compares options quantitatively using probabilities and expected values; the Ansoff matrix classifies growth strategies by risk according to product and market newness.')],
  misc=[('Using as many tools as possible in an answer earns the highest marks.', 'Marks reward relevant, well-applied tools; listing many tools superficially without application to the case scores poorly.')],
  cases=[('the Crossrail project', 'London\'s Elizabeth line (Crossrail) opened in 2022, more than three years late and about £4 bn over its original budget.', 'project planning and critical path', 'delays to critical activities such as signalling and testing pushed back the whole project'),
         ('Disney\'s diversification', 'Disney has grown from animated films into theme parks, cruise lines, merchandise and streaming (Disney+).', 'the Ansoff matrix', 'diversification spreads risk but requires new capabilities'),
         ('Ryanair\'s cost leadership', 'Ryanair carries over 180 million passengers a year with low fares based on high aircraft utilisation and minimal frills.', 'Porter\'s generic strategies', 'cost leadership requires every part of operations to minimise costs')],
  apply=[('A Paper 1 case describes a café chain considering entering a new country with its existing menu. Identify which Ansoff strategy this is and analyse its risk.', 'Market development (existing product, new market). Medium risk: the product is proven, but the firm lacks knowledge of local tastes, culture, competitors and regulations.', 4)],
  evaluate=[('Critical path analysis guarantees that a project will be completed on time.', ['identifies critical activities', 'helps allocate resources', 'shows float'],
             ['durations are estimates', 'unexpected events', 'needs constant updating', 'does not ensure quality or budget'], 'CPA improves planning and control but cannot guarantee completion; its value depends on accurate estimates and active management.')],
  )

S('ch12-st3', concepts=('ethics', 'sustainability', 'change', 'creativity'),
  terms=[('social enterprise', 'a business with social or environmental objectives that reinvests most of its surplus to pursue them'),
         ('human need', 'a basic requirement for well-being, such as food, water, shelter, health, education, safety or belonging, that a social enterprise may aim to meet'),
         ('Paper 3', 'the HL exam paper based on a case study of a social enterprise, assessing understanding of human needs and decision-making'),
         ('recommendation', 'a justified choice of one option, weighing its advantages and disadvantages against the alternatives using the case'),
         ('social impact', 'the effect an organization\'s activities have on the well-being of people and communities')],
  facts=[('In Paper 3, the final question usually asks students to:', 'recommend one of two options for the social enterprise', ['define a term only', 'draw an organization chart', 'calculate a share price'], 'A 15-mark recommendation.'),
         ('Which is a human need?', 'Access to clean water', ['A luxury car', 'A higher share price', 'Faster broadband for gaming'], 'Basic requirements for well-being.'),
         ('A good Paper 3 recommendation should:', 'use evidence from the case to justify one option and consider its drawbacks', ['avoid making a choice', 'ignore the human need', 'only describe both options'], 'Justification and balance are rewarded.')],
  why=[('Explain why social enterprises must balance social objectives and financial sustainability.', 'Without enough revenue the enterprise cannot survive to meet its social goals, but focusing too much on profit can undermine its mission.'),
       ('Explain why the human need should be central to a Paper 3 recommendation.', 'Social enterprises exist to meet a human need, so the best option is the one that best meets that need sustainably, not just the most profitable.'),
       ('Explain why measuring the impact of a social enterprise is difficult.', 'Social outcomes such as health or empowerment are hard to quantify and take time, and it is hard to separate the enterprise\'s effect from other factors.')],
  contrast=[('a social enterprise', 'a charity', 'A social enterprise earns most of its income by trading goods or services; a charity relies mainly on donations and grants.')],
  misc=[('Social enterprises do not need to make a surplus.', 'They need a surplus to survive, invest and grow; it is reinvested in the social mission rather than distributed to owners.')],
  cases=[(se[0], se[1], 'meeting a human need', f'the enterprise addresses {se[2]} while needing to remain financially sustainable') for se in SE[:4]],
  apply=[('A social enterprise selling solar lamps in rural areas must choose between expanding to a new region or offering repair services in existing areas. Identify two considerations and explain how they affect your recommendation.', 'Human need met (expansion reaches more households without power; repairs extend lamp life for existing users); financial sustainability (expansion costs and risk vs steady service income); local partnerships and skills; environmental impact of waste.', 6)],
  evaluate=[('Social enterprises should prioritise growth so that they can meet the human need of more people.', ['greater reach and impact', 'economies of scale', 'more influence'],
             ['mission drift', 'quality may fall', 'finance and risk', 'deep impact in existing areas may matter more'], 'Growth can multiply impact, but only if it is financially sustainable and keeps the focus on the human need.')],
  )


# =============================================================================================
# ch13 Internal assessment: business research project
# =============================================================================================
S('ch13-st1', concepts=('change', 'creativity', 'ethics', 'sustainability'),
  terms=[('internal assessment (IA)', 'the business research project in which students analyse a real business issue in a real organization, using supporting documents and one key concept'),
         ('research question', 'a focused question about a real business issue that the IA answers, for example "How has the shift to e-commerce affected the profitability of X?"'),
         ('key concept', 'one of the four BM concepts – change, creativity, ethics or sustainability – that the IA must use as a lens'),
         ('real business issue', 'an actual problem, decision or change faced by a specific organization'),
         ('backward-looking question', 'a research question about a decision or change that has already happened, which the IA guide requires')],
  facts=[('How many key concepts must the IA focus on?', 'One', ['All four', 'Two', 'None'], 'One concept is the lens.'),
         ('Which is a suitable IA research question?', 'How has the introduction of self-service kiosks affected customer satisfaction at a local McDonald\'s?', ['What is marketing?', 'Should all businesses use social media?', 'Will Apple be the biggest company in 2050?'], 'Focused, real, specific and backward-looking.'),
         ('The IA must be based on:', 'a real organization and a real business issue', ['a fictional company', 'a general topic with no organization', 'only textbook theory'], 'It must be grounded in reality.')],
  why=[('Explain why a focused research question is important for the IA.', 'A narrow question allows depth of analysis within the word limit and makes it easier to select relevant documents and tools.'),
       ('Explain why the key concept must be integrated throughout the IA.', 'The concept should shape the analysis and conclusion, not just be mentioned, so the IA shows understanding of how the concept affects the issue.'),
       ('Explain why a backward-looking research question is recommended.', 'Supporting documents exist for decisions already made, so the student can analyse evidence rather than speculate about the future.')],
  contrast=[('a broad research question', 'a focused research question', 'A broad question (e.g. about marketing in general) is too large to answer in depth; a focused question targets a specific issue in a specific organization and period.')],
  misc=[('Any interesting business topic makes a good IA.', 'The IA needs a specific organization, a real issue, a focused backward-looking question, enough supporting documents and a clear link to one key concept.')],
  cases=[('an IA on a local supermarket', 'A student investigates how a local supermarket\'s switch to plastic-free packaging in 2023 affected sales and customer perceptions.', 'choosing a key concept', 'sustainability is the natural lens, linked to costs, revenue and stakeholders'),
         ('an IA on a streaming service', 'A student investigates how Netflix\'s introduction of an ad-supported plan in 2022 changed its revenue streams.', 'framing a research question', 'the question is real, focused and backward-looking, with plenty of published documents'),
         ('an IA on a family restaurant', 'A student investigates how a family restaurant adapted to Covid-19 by launching delivery and a new menu.', 'the concept of change and creativity', 'the issue shows how the business responded creatively to sudden change')],
  apply=[('A student\'s proposed IA question is "How can businesses be more ethical?" Explain why it is weak and rewrite it.', 'It is too broad, not about a real organization, and forward-looking. Better: "To what extent did Lush\'s decision to leave Facebook and Instagram in 2021 reflect its ethical values and affect its marketing?"', 4)],
  evaluate=[('Choosing the right organization and research question is the most important stage of the IA.', ['determines availability of documents', 'focus and depth', 'link to the concept'],
             ['quality of analysis and evaluation matters most for marks', 'use of tools', 'structure and word limit'], 'A strong question and organization are the foundation, but marks are earned through analysis, evaluation and use of the concept.')],
  )

S('ch13-st2', concepts=('change', 'creativity', 'ethics', 'sustainability'),
  terms=[('supporting documents', 'the 3-5 sources, such as company reports, articles and data, on which the IA analysis is based'),
         ('primary data (IA)', 'data collected by the student, such as interviews or surveys, which may support but should not replace supporting documents'),
         ('secondary data (IA)', 'data published by others, such as annual reports, news articles and market reports'),
         ('bias in sources', 'the tendency of a source to present information in a one-sided way, for example a firm\'s own press release'),
         ('triangulation', 'using several different sources to check and support findings')],
  facts=[('How many supporting documents should the IA be based on?', 'Three to five', ['One', 'Ten to fifteen', 'None'], 'The guide requires 3-5 documents.'),
         ('Which source is most likely to be biased in favour of the company?', 'The company\'s own press release', ['An independent industry report', 'A regulator\'s report', 'Government statistics'], 'Firms present themselves positively.'),
         ('Supporting documents should usually be:', 'published within the last three years', ['at least 20 years old', 'undated', 'fictional'], 'Up-to-date sources are expected.')],
  why=[('Explain why the IA should use a range of supporting documents.', 'Different sources give different perspectives and data, allowing triangulation and reducing the effect of bias.'),
       ('Explain why business management tools must be applied to the supporting documents.', 'Tools such as SWOT, ratios or force field analysis turn information into analysis and show the student can use course concepts.'),
       ('Explain why students should evaluate the reliability of their sources.', 'Sources may be biased, outdated or incomplete, so judging reliability strengthens the conclusion.')],
  contrast=[('primary data', 'secondary data', 'Primary data is collected by the student for the IA; secondary data comes from published sources such as reports and articles.')],
  misc=[('A survey of friends is a good supporting document.', 'Small convenience surveys are unreliable; supporting documents should mainly be credible secondary sources about the organization.')],
  cases=[('documents for an IA on Tesla', 'A student studying Tesla\'s price cuts in 2023 uses Tesla\'s quarterly results, a Reuters article, an industry sales report and an analyst note.', 'selecting supporting documents', 'a mix of company, news and independent sources allows triangulation'),
         ('using ratio analysis in an IA', 'A student uses two years of a retailer\'s annual reports to calculate profit margins and current ratios.', 'applying business management tools', 'ratio analysis turns financial data into evidence about performance'),
         ('a biased press release', 'A company\'s press release claims its new packaging is "100% sustainable" without independent evidence.', 'bias in sources', 'the student should compare it with independent sources before relying on it')],
  apply=[('A student\'s IA uses one company press release and two blog posts. Explain two weaknesses of these sources and suggest better alternatives.', 'Weaknesses: the press release is likely biased; blogs may be unreliable and unreferenced. Better: annual reports, reputable news articles (e.g. Financial Times, Reuters), industry or government reports.', 4)],
  evaluate=[('Primary research is more valuable than secondary documents in a business research project.', ['specific to the question', 'original insight'],
             ['the IA requires supporting documents', 'small samples are unreliable', 'secondary sources give financial data', 'time constraints'], 'Secondary supporting documents are the core of the IA; primary data can add insight but should support rather than replace them.')],
  )

S('ch13-st3', concepts=('change', 'creativity', 'ethics', 'sustainability'),
  terms=[('analysis (IA)', 'breaking down information from supporting documents using tools and theory to show causes, effects and relationships'),
         ('evaluation (IA)', 'weighing the strengths and limitations of the evidence and arguments to reach a judgement'),
         ('conclusion (IA)', 'a clear answer to the research question that follows from the analysis and evaluation'),
         ('word limit (IA)', 'the maximum of 1,800 words for the IA; work beyond the limit is not assessed'),
         ('limitations of research', 'weaknesses of the sources, methods or scope of the IA that affect the reliability of the conclusion')],
  facts=[('What is the IA word limit?', '1,800 words', ['500 words', '4,000 words', 'no limit'], 'The 2024 guide sets 1,800 words.'),
         ('A strong IA conclusion should:', 'answer the research question using evidence from the analysis', ['introduce new information', 'repeat the introduction', 'avoid a judgement'], 'It follows from the evidence.'),
         ('The IA is marked out of:', '25 marks', ['100 marks', '10 marks', '50 marks'], 'Assessed against criteria A-G.')],
  why=[('Explain why evaluation is necessary for high IA marks.', 'Analysis alone shows understanding, but higher marks require judging the significance and reliability of evidence and reaching a supported conclusion.'),
       ('Explain why the word limit requires careful planning.', 'With only 1,800 words, students must focus on the most relevant evidence and tools, avoiding description so space is left for analysis and evaluation.'),
       ('Explain why acknowledging limitations strengthens an IA.', 'It shows critical thinking about the evidence and explains how far the conclusion can be trusted.')],
  contrast=[('analysis', 'evaluation', 'Analysis explains how and why things happen using tools and evidence; evaluation weighs the evidence and arguments to judge their importance and reach a conclusion.')],
  misc=[('Including lots of description of the company improves an IA.', 'Description uses words but earns few marks; the IA rewards analysis, evaluation and use of the concept.')],
  cases=[('an IA on a coffee chain\'s price rise', 'A student concludes that a coffee chain\'s 2023 price rise increased revenue but reduced customer satisfaction, using sales data and reviews.', 'evaluation and conclusion', 'the judgement weighs financial gains against customer perceptions and notes limited data'),
         ('an IA that exceeded the word limit', 'A student wrote 2,300 words, so the examiner stopped reading after 1,800 words and the conclusion was not assessed.', 'the word limit', 'poor planning cost marks for the conclusion and evaluation'),
         ('an IA using force field analysis', 'A student uses force field analysis to assess the forces for and against a local bakery moving to online ordering.', 'analysis using tools', 'the tool structures evidence and supports a balanced judgement')],
  apply=[('A student\'s IA conclusion says: "In conclusion, the company is very successful." Explain why this is weak and suggest how it could be improved.', 'It does not answer the research question, gives no evidence and no judgement on the concept. Improve by directly answering the question, summarising key evidence from the analysis, weighing it, linking it to the key concept and noting limitations.', 4)],
  evaluate=[('Evaluation is more important than analysis in a business research project.', ['higher-level skill', 'needed for top marks', 'leads to the conclusion'],
             ['evaluation depends on good analysis', 'both are assessed', 'tools and documents are needed first'], 'Evaluation is the higher-level skill, but it is only convincing when built on thorough analysis of good evidence.')],
  )
