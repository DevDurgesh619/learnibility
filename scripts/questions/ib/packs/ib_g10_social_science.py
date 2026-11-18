"""IB MYP 5 Individuals and Societies (integrated humanities) – ib-g10-social-science.

Criteria: A knowing and understanding, B investigating, C communicating, D thinking critically (MYP year 5
descriptors). Real dated events, places and attributed (paraphrased) sources; sensitive topics (war, genocide,
Partition, apartheid, migration) are summarised neutrally in the third person and propaganda is described, never
quoted. Parametric generators compute answers for chronology, war statistics, reparations, hyperinflation,
industrial growth, development indicators (GDP per capita, HDI), trade, climate data, population and electoral
arithmetic. Mocks follow the MYP 5 on-screen eAssessment shape (3 tasks, 15 items, 80 marks).
"""
from __future__ import annotations

from _common import Registry, mcq, name  # noqa: F401
import ib_myp_is_common as C

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}
MOCK = C.mock(5)
R = Registry()
K = C.Kit(R, 5)
STYLE = C.style(5)


def init(subject_id):
    pass


def templates(st):
    return R.build(st, STYLE)


def series(key, rows, d=(1, 4)):
    C.pct_change(K, key, rows, d=d)


# =============================================================================================
# ch01 Causes and Consequences of the First World War
# =============================================================================================
WW1_EVENTS = [('the Franco-Prussian War ends with German unification', 1871), ('the Dual Alliance between Germany and Austria-Hungary', 1879),
              ('the Franco-Russian Alliance', 1894), ('the launch of HMS Dreadnought', 1906), ('the Anglo-Russian Entente completes the Triple Entente', 1907),
              ('the Bosnian Crisis', 1908), ('the Second Moroccan (Agadir) Crisis', 1911), ('the First Balkan War', 1912),
              ('the assassination of Archduke Franz Ferdinand', 1914), ('the Battle of the Somme', 1916), ('the United States enters the war', 1917),
              ('the armistice ends fighting on the Western Front', 1918), ('the Treaty of Versailles is signed', 1919), ('the League of Nations begins work', 1920)]

K.st('ch01-st1', 'the long-term causes of the First World War: militarism, alliances, imperialism and nationalism',
     terms=[('militarism', 'the belief that a country should build strong armed forces and be prepared to use them, giving the military great influence over policy'),
            ('alliance system', 'the two rival blocs before 1914: the Triple Alliance (Germany, Austria-Hungary, Italy) and the Triple Entente (Britain, France, Russia)'),
            ('imperialism', 'the policy of extending a country\'s power by acquiring colonies or controlling other territories'),
            ('nationalism', 'strong loyalty to one\'s nation, including the desire of national groups to have their own state'),
            ('Schlieffen Plan', 'Germany\'s plan to avoid a two-front war by defeating France quickly through Belgium before turning on Russia'),
            ('Weltpolitik', 'Kaiser Wilhelm II\'s "world policy" of expanding Germany\'s empire, navy and global influence'),
            ('naval race', 'the Anglo-German competition to build battleships, especially Dreadnoughts, from 1906')],
     facts=[('Which country launched HMS Dreadnought in 1906?', 'Britain', ['Germany', 'France', 'Russia'], 'It made earlier battleships obsolete and intensified the naval race.'),
            ('Which crisis of 1905–06 and 1911 involved German challenges to French influence in North Africa?', 'The Moroccan Crises', ['the Bosnian Crisis', 'the Fashoda Incident', 'the July Crisis'], 'Both pushed Britain and France closer together.'),
            ('Which region was called the "powder keg of Europe" before 1914?', 'The Balkans', ['Scandinavia', 'the Iberian Peninsula', 'the Low Countries'], 'Declining Ottoman power and nationalism created instability.'),
            ('Which country annexed Bosnia-Herzegovina in 1908, angering Serbia?', 'Austria-Hungary', ['Russia', 'Germany', 'Italy'], 'Serbian nationalists saw Bosnia as Serbian land.'),
            ('Which country, though in the Triple Alliance, did not join its allies in 1914?', 'Italy', ['Germany', 'Austria-Hungary', 'the Ottoman Empire'], 'Italy joined the Entente in 1915.')],
     why=[('Explain why the alliance system turned a local conflict into a general European war.', 'Commitments between the great powers meant that a dispute between Austria-Hungary and Serbia drew in Russia, then Germany, France and Britain, as each felt obliged or pressured to support its partner.'),
          ('Explain why the naval race worsened relations between Britain and Germany.', 'Britain depended on naval supremacy to protect its empire and trade, so Germany\'s rapid fleet building was seen as a direct threat, pushing Britain towards France and Russia.'),
          ('Explain why Serbian nationalism threatened Austria-Hungary.', 'Austria-Hungary was a multinational empire with many South Slavs; Serbian nationalism encouraged them to break away, threatening the empire\'s survival.'),
          ('Explain why militarism made war more likely in 1914.', 'Mass conscript armies, detailed mobilisation timetables such as the Schlieffen Plan and the influence of generals meant that once mobilisation began, diplomacy had little time to work.')],
     contrast=[('a long-term cause', 'a short-term trigger', 'Long-term causes such as alliances and militarism created tension over decades; a trigger such as the assassination at Sarajevo set the war off.'),
               ('the Triple Alliance', 'the Triple Entente', 'The Triple Alliance (1882) linked Germany, Austria-Hungary and Italy; the Triple Entente (completed 1907) was a looser understanding between Britain, France and Russia.')],
     misc=[('The alliances legally forced every country to go to war in 1914.', 'The Entente was not a binding military alliance; Britain entered mainly over Germany\'s invasion of Belgium, and Italy stayed neutral despite the Triple Alliance.'),
           ('The assassination of Franz Ferdinand was the main cause of the war.', 'It was the trigger; long-term tensions and the decisions of governments during the July Crisis explain why it led to a general war.'),
           ('Only Germany wanted war in 1914.', 'Historians debate responsibility; decisions in Vienna, St Petersburg, Paris and London also contributed.')],
     cases=[('the Anglo-German naval race', 'After 1906 both countries competed to build Dreadnought-type battleships; by 1914 Britain had 29 and Germany 17.', 'militarism and rivalry', 'arms competition increased mistrust and pushed Britain towards the Entente.'),
            ('the Second Moroccan Crisis (1911)', 'Germany sent the gunboat Panther to Agadir to challenge French control; Britain backed France, and Germany backed down.', 'imperial rivalry', 'colonial disputes strengthened the Entente and increased German fears of encirclement.')],
     evaluate=[('Militarism was the most important long-term cause of the First World War.', ['the naval and arms races created fear and mistrust', 'war plans like the Schlieffen Plan reduced time for diplomacy'], ['alliances turned a Balkan dispute into a European war', 'nationalism in the Balkans created the crisis itself'], 'Militarism made war more likely and harder to stop, but it interacted with alliances and nationalism; no single factor fully explains the outbreak.')],
     src=[('Historian\'s interpretation (paraphrased)', 'The historian argued that Germany\'s leaders deliberately pursued aggressive aims before 1914, seeking to dominate Europe and expand overseas, and that they used the July Crisis to launch a war they had long considered.', 'Paraphrase of Fritz Fischer, Griff nach der Weltmacht (Germany\'s Aims in the First World War), Düsseldorf, 1961', 'to challenge the post-war view that all powers shared responsibility, using German archives', 'It was based on extensive German government records and transformed the debate.', 'It focuses on German documents and may underplay the decisions of other powers; critics argued it read later aims back into 1914.', 'Germany bore primary responsibility because of its aggressive war aims.')],
     rq=[('To what extent was the Anglo-German naval race responsible for Britain entering the First World War in 1914?', 'Why did WWI happen?', 'it is too broad for a focused investigation', 'It weighs one long-term cause against others using evidence.', 'Use naval statistics, cabinet documents and two historians (e.g. Fischer, Clark); compare factors; evaluate perspectives; cite in MLA.')])
C.chronology(K, 'ch01-st1', events=WW1_EVENTS[:9])


@R.add('ch01-st1', ('C3', 'C4'), (1, 5), 'numerical')
def arms(rng, slot):
    rows = [('Germany', 'defence spending', 'million pounds', 1870, 10.8, 1914, 110.8), ('Britain', 'defence spending', 'million pounds', 1870, 22.4, 1914, 76.8),
            ('Russia', 'defence spending', 'million pounds', 1870, 22.0, 1914, 88.2), ('France', 'defence spending', 'million pounds', 1870, 22.4, 1914, 57.4),
            ('Britain', 'Dreadnought-type battleships', 'ships', 1906, 1, 1914, 29), ('Germany', 'Dreadnought-type battleships', 'ships', 1908, 4, 1914, 17)]
    co, what, unit, y1, v1, y2, v2 = rng.choice(rows)
    pc = (v2 - v1) / v1 * 100
    if slot.d <= 3:
        return dict(stem=f'{co}\'s {what} rose from {v1} {unit} in {y1} to {v2} {unit} in {y2} (approximate historians\' figures). Calculate the percentage increase.',
                    answer=f'{pc:.0f}%', type='numerical', marks=2, markingKey=f'({v2} − {v1}) ÷ {v1} × 100 = {pc:.0f}% (M1 A1).', gap='G3')
    o = rng.choice([r for r in rows if r[1] == what and r[0] != co])
    pc2 = (o[6] - o[4]) / o[4] * 100
    return dict(stem=(f'Approximate figures: {co}\'s {what} went from {v1} to {v2} {unit} ({y1}–{y2}); {o[0]}\'s went from {o[4]} to {o[6]} {unit} ({o[3]}–{o[5]}). '
                      'Calculate the percentage increase for each, and explain how such figures support the argument that militarism caused the war.'),
                answer=f'{co}: {pc:.0f}%; {o[0]}: {pc2:.0f}%', type='multi_step', marks=5,
                markingKey=f'{co} {pc:.0f}% (M1 A1); {o[0]} {pc2:.0f}% (A1). Analysis (2): rapid growth shows an arms race; each side saw the other\'s build-up as a threat, '
                           'increasing fear and the pressure to mobilise fast; but spending alone does not prove intent to start a war.', gap='G5')


K.st('ch01-st2', 'the July Crisis of 1914 and the outbreak of war',
     terms=[('July Crisis', 'the month of diplomatic crisis between the assassination of Franz Ferdinand on 28 June and the outbreak of general war in early August 1914'),
            ('blank cheque', 'Germany\'s promise on 5–6 July 1914 of unconditional support to Austria-Hungary against Serbia'),
            ('ultimatum', 'a final set of demands, with a threat of action if they are rejected; Austria-Hungary sent one to Serbia on 23 July 1914'),
            ('mobilisation', 'calling up and preparing armed forces for war'),
            ('Black Hand', 'a secret Serbian nationalist society linked to the assassination at Sarajevo'),
            ('Treaty of London (1839)', 'the treaty in which the great powers, including Prussia and Britain, guaranteed Belgian neutrality')],
     facts=[('Who assassinated Archduke Franz Ferdinand in Sarajevo on 28 June 1914?', 'Gavrilo Princip', ['Kaiser Wilhelm II', 'Tsar Nicholas II', 'Leon Trotsky'], 'He was a Bosnian Serb student linked to the Black Hand.'),
            ('On what date did Austria-Hungary declare war on Serbia?', '28 July 1914', ['28 June 1914', '4 August 1914', '11 November 1918'], 'One month after the assassination.'),
            ('Which event led Britain to declare war on Germany on 4 August 1914?', 'Germany\'s invasion of Belgium', ['the sinking of the Lusitania', 'the Zimmermann Telegram', 'the Russian Revolution'], 'Britain had guaranteed Belgian neutrality.'),
            ('Which country first ordered general mobilisation among the great powers in late July 1914?', 'Russia', ['Britain', 'Italy', 'the United States'], 'Russia mobilised on 30 July in support of Serbia.'),
            ('Which British foreign secretary is reported to have said "the lamps are going out all over Europe"?', 'Sir Edward Grey', ['Winston Churchill', 'David Lloyd George', 'Neville Chamberlain'], 'He said it on the eve of war.')],
     why=[('Explain why Germany issued the "blank cheque" to Austria-Hungary.', 'Germany saw Austria-Hungary as its only reliable ally and wanted it to crush Serbia quickly; some leaders also thought a war with Russia was better fought sooner than later.'),
          ('Explain why Russia\'s mobilisation was significant.', 'Germany\'s war plan required it to strike France before Russia was ready, so Russian mobilisation led Germany to declare war on Russia and France and invade Belgium.'),
          ('Explain why the Schlieffen Plan brought Britain into the war.', 'The plan required German troops to pass through neutral Belgium, whose neutrality Britain had guaranteed in 1839; the invasion also threatened the Channel coast.'),
          ('Explain why the July Crisis escalated so quickly.', 'Rigid war plans, alliance commitments, mutual distrust and leaders\' willingness to risk war left little time or will for diplomacy once mobilisation began.')],
     contrast=[('the assassination at Sarajevo', 'the July Crisis', 'The assassination was a single event on 28 June; the July Crisis was the month of decisions by governments that turned it into a general war.'),
               ('partial mobilisation', 'general mobilisation', 'Partial mobilisation prepares forces against one enemy; general mobilisation prepares the whole army, which other powers saw as a step towards war.')],
     misc=[('War broke out immediately after the assassination.', 'Austria-Hungary did not declare war on Serbia until 28 July, a month later, after the blank cheque and the ultimatum.'),
           ('Serbia rejected all of Austria-Hungary\'s demands.', 'Serbia accepted most demands but refused those that would let Austrian officials operate inside Serbia.'),
           ('Britain went to war because of its alliance with France.', 'Britain had no binding alliance with France; the invasion of Belgium was the decisive reason.')],
     cases=[('the Austro-Hungarian ultimatum to Serbia', 'Sent on 23 July 1914 with a 48-hour deadline, it demanded the suppression of anti-Austrian groups and Austrian participation in the investigation.', 'diplomacy designed to fail', 'its harsh terms were intended to provide a pretext for war.'),
            ('the German invasion of Belgium', 'German troops entered Belgium on 4 August 1914, meeting resistance at Liège; Britain declared war that day.', 'war plans driving decisions', 'the military timetable turned a continental war into a world war.')],
     evaluate=[('Germany was mainly responsible for the outbreak of war in 1914.', ['the blank cheque encouraged Austria-Hungary to act', 'the Schlieffen Plan required invading Belgium and attacking France'], ['Austria-Hungary chose to use the crisis to crush Serbia', 'Russian mobilisation and French support for Russia also escalated the crisis'], 'Germany bears major responsibility, but historians such as Christopher Clark argue that leaders in several capitals "sleepwalked" into war, so responsibility was shared.')],
     src=[('Historian\'s interpretation (paraphrased)', 'The historian argued that the outbreak of war was not the result of one country\'s plan but of decisions by leaders in several capitals who were watchful but unseeing, blind to the full horror of the war they were bringing about.', 'Paraphrase of Christopher Clark, The Sleepwalkers: How Europe Went to War in 1914, London, 2012', 'to re-examine the July Crisis from the perspectives of all the powers', 'It draws on archives from many countries and challenges simple blame.', 'Critics argue it underplays German and Austro-Hungarian responsibility; it is one interpretation.', 'Responsibility for the war was shared among several powers.')],
     rq=[('How far did the German "blank cheque" of July 1914 determine Austria-Hungary\'s decision to declare war on Serbia?', 'Who started WWI?', 'it is a closed, oversimplified question', 'It examines a specific decision and its consequences in the July Crisis.', 'Use diplomatic documents, the ultimatum text and two historians (Fischer and Clark); build a timeline; compare interpretations; cite in MLA.')])


@R.add('ch01-st2', 'C3', (1, 4), 'mcq')
def july_days(rng, slot):
    ev = [('the assassination at Sarajevo', 28, 6), ('the German "blank cheque"', 5, 7), ('the Austro-Hungarian ultimatum to Serbia', 23, 7),
          ('Austria-Hungary declares war on Serbia', 28, 7), ('Russia orders general mobilisation', 30, 7), ('Germany declares war on Russia', 1, 8),
          ('Germany declares war on France', 3, 8), ('Britain declares war on Germany', 4, 8)]
    import datetime as dt
    a, b = rng.sample(ev, 2)
    da = dt.date(1914, a[2], a[1]); db = dt.date(1914, b[2], b[1])
    if da > db:
        a, b, da, db = b, a, db, da
    n = (db - da).days
    if n == 0:
        return None
    wr = C._distinct(f'{n} days', [f'{x} days' for x in (n + 1, n - 1, n + 7, n + 30, abs(n - 30)) if x > 0])
    return C.mcq(rng, f'In 1914, {a[0]} took place on {a[1]} {da.strftime("%B")} and {b[0]} on {b[1]} {db.strftime("%B")}. How many days passed between the two events?',
                 f'{n} days', wr, f'Count from {a[1]} {da.strftime("%B")} to {b[1]} {db.strftime("%B")}: {n} days.')


K.st('ch01-st3', 'the experience of war: trench warfare, the home front and colonial soldiers, including Indian troops',
     terms=[('trench warfare', 'fighting from systems of dug-in trenches, typical of the Western Front from late 1914 to 1918'),
            ('no man\'s land', 'the area between opposing front-line trenches'),
            ('war of attrition', 'a strategy of wearing down the enemy through continual losses of soldiers and resources'),
            ('total war', 'a war in which governments mobilise the whole economy and society, including civilians, for the war effort'),
            ('home front', 'the civilian population and activities of a country at war'),
            ('conscription', 'compulsory enlistment in the armed forces; introduced in Britain in 1916'),
            ('shell shock', 'the term used during the war for the psychological trauma suffered by soldiers')],
     facts=[('About how many Indian soldiers served overseas in the First World War?', 'Over 1 million', ['About 10,000', 'About 100,000', 'About 13 million'], 'About 1.5 million Indians were recruited; they fought in France, Mesopotamia, Gallipoli, Egypt and East Africa.'),
            ('On the first day of the Battle of the Somme, 1 July 1916, about how many British casualties were there?', 'About 57,000', ['About 570', 'About 5,700', 'About 570,000'], 'Including about 19,000 killed.'),
            ('Which Indian soldier was the first to receive the Victoria Cross in the war, in 1914?', 'Khudadad Khan', ['Mangal Pandey', 'Bhagat Singh', 'Subhas Chandra Bose'], 'He fought at Hollebeke in Belgium.'),
            ('What was DORA, introduced in Britain in August 1914?', 'The Defence of the Realm Act, giving the government wide powers over civilian life', ['A new tank', 'A peace treaty', 'A women\'s union'], 'It allowed censorship, requisitioning and controls.'),
            ('Which gas, first used by Germany at Ypres in April 1915, began large-scale chemical warfare?', 'Chlorine', ['Oxygen', 'Helium', 'Nitrogen'], 'Phosgene and mustard gas followed.')],
     why=[('Explain why the Western Front became a stalemate.', 'Defensive weapons – machine guns, artillery, barbed wire and entrenchments – gave great advantages to defenders, so attacks across no man\'s land suffered huge losses for little ground.'),
          ('Explain why the First World War is described as a total war.', 'Governments mobilised entire economies, conscripted men, directed industry, rationed food, used propaganda and drew women into the workforce, so civilians were fully involved.'),
          ('Explain why Britain relied heavily on colonial soldiers.', 'Britain\'s small professional army needed reinforcements quickly; the Indian Army was the largest volunteer army in the empire and could be deployed rapidly to France and the Middle East.'),
          ('Explain why women\'s roles changed during the war.', 'With millions of men in the armed forces, women filled jobs in munitions, transport, offices and farming, and served as nurses, showing their contribution to the war economy.')],
     contrast=[('the Western Front', 'the Eastern Front', 'The Western Front in France and Belgium became a static line of trenches; the Eastern Front between Germany/Austria-Hungary and Russia was longer and more mobile.'),
               ('volunteering', 'conscription', 'Volunteers chose to enlist, as in Britain in 1914–15 and in India throughout the war; conscription made military service compulsory.')],
     misc=[('The First World War was fought only in Europe.', 'It was fought in the Middle East, Africa, Asia and at sea, and soldiers came from India, Africa, Australia, Canada and elsewhere.'),
           ('Soldiers spent all their time fighting at the front line.', 'Soldiers rotated between front-line, support and reserve trenches and rest areas; much time was spent on routine work, boredom and waiting.'),
           ('Colonial troops played only a minor role.', 'Over a million Indian soldiers served, along with large numbers from Africa, the Caribbean and other colonies, plus hundreds of thousands of labourers.')],
     cases=[('the Indian Corps at Neuve Chapelle', 'In March 1915 Indian and British troops attacked at Neuve Chapelle, capturing the village but suffering heavy losses.', 'the role of colonial soldiers', 'Indian troops played a central part on the Western Front in 1914–15.'),
            ('the Brighton Pavilion hospital', 'From 1914 to 1916 the Royal Pavilion in Brighton served as a hospital for wounded Indian soldiers, with separate kitchens for different dietary needs.', 'colonial soldiers\' experiences', 'it shows how the empire was visibly present on the British home front.')],
     evaluate=[('The experience of trench warfare has been exaggerated in popular memory.', ['soldiers did not spend all their time in front-line trenches', 'many soldiers were not involved in major offensives'], ['casualties on the Somme and at Verdun were enormous', 'disease, gas, shelling and mud caused great suffering'], 'Popular memory simplifies the experience, but the scale of suffering was real; historians argue that experiences varied widely by time, place and role.')],
     src=[('Letter (paraphrased)', 'An Indian soldier wounded in France wrote home that the fighting was unlike anything known before, with constant shelling and many comrades killed. He asked his family not to worry and said he was proud to have done his duty, but described the cold and the losses.', 'Composite paraphrase of letters by Indian soldiers, 1915, from the censored mail extracts collected by the Indian Mail Censor (published in David Omissi, Indian Voices of the Great War, 1999)', 'to communicate personal experiences to family in India', 'It is a rare first-hand account from a colonial soldier.', 'Letters were censored, so soldiers may have avoided criticism; they were also often written by scribes.', 'Indian soldiers experienced intense, unfamiliar warfare and heavy losses.')],
     rq=[('How did the experiences of Indian soldiers on the Western Front in 1914–15 compare with those of British soldiers?', 'What were trenches like?', 'it is a descriptive question', 'It compares perspectives using primary sources.', 'Use censored letters, war diaries and two historians; compare conditions; evaluate sources; cite in MLA.')])


@R.add('ch01-st3', ('C3', 'C4'), (1, 5), 'numerical')
def casualties(rng, slot):
    rows = [('Germany', 11.0, 1.77), ('France', 8.41, 1.36), ('the British Empire', 8.90, 0.91), ('Russia', 12.0, 1.7), ('Austria-Hungary', 7.8, 1.2),
            ('Italy', 5.6, 0.65), ('the United States', 4.36, 0.13)]
    co, mob, dead = rng.choice(rows)
    p = dead / mob * 100
    if slot.d <= 3:
        return dict(stem=f'About {mob} million men from {co} were mobilised in the First World War and about {dead} million were killed (approximate estimates). What percentage of mobilised men were killed?',
                    answer=f'{p:.1f}%', type='numerical', marks=2, markingKey=f'{dead} ÷ {mob} × 100 = {p:.1f}% (M1 A1). Figures vary between sources.', gap='G3')
    o = rng.choice([r for r in rows if r[0] != co])
    p2 = o[2] / o[1] * 100
    return dict(stem=(f'Approximate estimates: {co} mobilised {mob} million men and lost {dead} million killed; {o[0]} mobilised {o[1]} million and lost {o[2]} million. '
                      'Calculate the percentage killed for each and suggest two reasons why the figures differ.'),
                answer=f'{co}: {p:.1f}%; {o[0]}: {p2:.1f}%', type='multi_step', marks=5,
                markingKey=f'{co} {p:.1f}% (M1 A1); {o[0]} {p2:.1f}% (A1). Reasons (2): length of involvement (the USA fought from 1917–18), fronts fought on, intensity of battles such as Verdun, '
                           'medical care, and the reliability of records.', gap='G5')


K.st('ch01-st4', 'the Paris Peace Settlement and the Treaty of Versailles: terms and reactions',
     terms=[('Treaty of Versailles', 'the peace treaty between the Allies and Germany signed on 28 June 1919'),
            ('war guilt clause', 'Article 231 of the Treaty of Versailles, which held Germany and its allies responsible for the loss and damage of the war'),
            ('reparations', 'compensation payments imposed on Germany; set in 1921 at 132 billion gold marks'),
            ('Fourteen Points', 'US President Woodrow Wilson\'s 1918 peace programme, including self-determination and a League of Nations'),
            ('self-determination', 'the right of a national group to choose its own government'),
            ('mandate', 'a former German or Ottoman territory administered by an Allied power under League of Nations supervision'),
            ('diktat', 'a dictated peace; the term many Germans used for the Treaty of Versailles')],
     facts=[('Which article of the Treaty of Versailles became known as the war guilt clause?', 'Article 231', ['Article 1', 'Article 10', 'Article 370'], 'It justified reparations.'),
            ('What limit did the treaty place on the German army?', '100,000 men', ['1 million men', '10,000 men', 'No limit'], 'Conscription was banned too.'),
            ('Which territory was returned to France under the treaty?', 'Alsace-Lorraine', ['the Saar permanently', 'Bavaria', 'Danzig'], 'Germany had taken it in 1871.'),
            ('In 1921 the Reparations Commission set Germany\'s reparations at what sum?', '132 billion gold marks', ['1.32 billion gold marks', '13.2 trillion gold marks', '1,320 gold marks'], 'Much was never paid.'),
            ('Which leader of the "Big Three" most wanted a harsh peace to protect his country\'s security?', 'Georges Clemenceau of France', ['Woodrow Wilson of the USA', 'David Lloyd George of Britain', 'Vittorio Orlando of Italy'], 'France had suffered heavy losses and invasion.')],
     why=[('Explain why Clemenceau wanted a harsh treaty.', 'France had lost about 1.4 million soldiers, its north-east had been devastated and it had been invaded twice in fifty years, so Clemenceau wanted to weaken Germany permanently and secure compensation.'),
          ('Explain why many Germans resented the Treaty of Versailles.', 'They had not been invited to negotiate, many believed the army had not been defeated, and they saw the war guilt clause, reparations, territorial losses and disarmament as humiliating.'),
          ('Explain why Wilson\'s Fourteen Points were only partly applied.', 'Britain and France wanted security and compensation, self-determination was hard to apply in mixed areas, and colonial peoples were excluded, while the US Senate rejected the treaty.'),
          ('Explain why the peace settlement disappointed nationalists in colonies.', 'Leaders such as Ho Chi Minh and delegates from Egypt and India hoped self-determination would apply to them, but the victorious empires kept and enlarged their colonies through mandates.')],
     contrast=[('the aims of Clemenceau', 'the aims of Wilson', 'Clemenceau wanted to punish and weaken Germany for France\'s security; Wilson wanted a fair peace based on self-determination and a League of Nations to prevent future wars.'),
               ('the Treaty of Versailles', 'the Paris Peace Settlement', 'Versailles was the treaty with Germany; the wider settlement also included Saint-Germain (Austria), Trianon (Hungary), Neuilly (Bulgaria) and Sèvres (Ottoman Empire).')],
     misc=[('The Treaty of Versailles made Germany pay all of the 132 billion gold marks.', 'Payments were reduced by the Dawes (1924) and Young (1929) Plans and suspended in 1932; Germany paid only a fraction.'),
           ('The treaty destroyed Germany as a great power.', 'Germany remained united, with a large population and industry, which allowed it to recover; this is why some historians call the treaty too harsh to accept but too weak to enforce.'),
           ('Germany was the only defeated country treated harshly.', 'Austria, Hungary, Bulgaria and the Ottoman Empire also lost large territories; Hungary lost about two-thirds of its land under Trianon.')],
     cases=[('the Ruhr occupation (1923)', 'When Germany fell behind on reparations, French and Belgian troops occupied the Ruhr; German workers went on strike, and hyperinflation followed.', 'reactions to reparations', 'enforcing the treaty deepened German resentment and economic crisis.'),
            ('Keynes and the Carthaginian peace', 'British economist John Maynard Keynes resigned from the delegation and in 1919 published a book arguing that reparations would ruin Europe\'s economy.', 'contemporary criticism of the treaty', 'his critique shaped later British views that the treaty was too harsh.')],
     evaluate=[('The Treaty of Versailles was too harsh on Germany.', ['reparations and war guilt caused lasting resentment', 'Germany lost 13% of its European territory and all its colonies'], ['Germany\'s own treaty with Russia at Brest-Litovsk (1918) was harsher', 'Germany kept its unity and industry and reparations were later reduced'], 'The treaty was harsh enough to cause bitter resentment but not harsh enough to permanently weaken Germany; its problems lay as much in enforcement as in its terms.')],
     src=[('Book (paraphrased)', 'The author, an economist who had attended the conference, argued that the reparations demanded from Germany were far beyond its capacity to pay and that the treaty ignored the economic recovery of Europe. He predicted it would lead to economic disaster and political instability.', 'Paraphrase of John Maynard Keynes, The Economic Consequences of the Peace, London, 1919', 'to persuade the public and policymakers that the treaty should be revised', 'It is the view of an expert insider at the conference.', 'It was written quickly to influence opinion; historians such as Margaret MacMillan argue it exaggerated the harshness.', 'Reparations were excessive and would damage Europe.')],
     rq=[('How far did the reparations of the Treaty of Versailles cause the German hyperinflation of 1923?', 'Was Versailles fair?', 'it is a vague value question', 'It tests a causal claim with economic evidence.', 'Use exchange-rate data, reparation schedules and two historians; compare causes such as war debts and money printing; cite in MLA.')])
C.chronology(K, 'ch01-st4', events=WW1_EVENTS[8:] + [('the Dawes Plan reduces reparations payments', 1924), ('the Young Plan', 1929), ('the Lausanne Conference suspends reparations', 1932)])


@R.add('ch01-st4', ('C3', 'C4'), (1, 5), 'numerical')
def treaty_losses(rng, slot):
    rows = [('European territory', 13), ('population', 10), ('coal production', 16), ('iron ore production', 48)]
    what, p = rng.choice(rows)
    base = [b for b in [(540_000, 'square kilometres', 'European territory'), (65, 'million people', 'population'),
                        (190, 'million tonnes a year', 'coal production'), (28, 'million tonnes a year', 'iron ore production')] if b[2] == what][0]
    lost = base[0] * p / 100
    return dict(stem=(f'Historians estimate that under the Treaty of Versailles Germany lost about {p}% of its pre-war {what}. If pre-war {what} was about {base[0]:,} {base[1]}, '
                      'calculate the approximate amount lost' + (' and explain why this loss mattered for Germany.' if slot.d >= 3 else '.')),
                answer=f'about {lost:,.1f} {base[1]}', type='numerical' if slot.d < 3 else 'multi_step', marks=2 if slot.d < 3 else 4,
                markingKey=f'{p}% × {base[0]:,} = {lost:,.1f} (M1 A1).' + (' Explanation (2): e.g. loss of industrial resources weakened recovery and reparations capacity; losses fuelled resentment.' if slot.d >= 3 else ''),
                gap='G3')

# =============================================================================================
# ch02 Authoritarian States in the Interwar Years
# =============================================================================================
K.st('ch02-st1', 'the interwar crisis: the Great Depression and the weakness of new democracies',
     terms=[('Great Depression', 'the severe worldwide economic slump that followed the Wall Street Crash of October 1929 and lasted through the 1930s'),
            ('Wall Street Crash', 'the collapse of share prices on the New York Stock Exchange in October 1929'),
            ('hyperinflation', 'extremely rapid inflation, as in Germany in 1923 when prices doubled every few days'),
            ('Weimar Republic', 'the democratic German state established in 1919 and replaced by Nazi dictatorship in 1933'),
            ('Article 48', 'the clause of the Weimar constitution allowing the president to rule by emergency decree'),
            ('proportional representation', 'an electoral system giving parties seats in proportion to votes, which in Weimar Germany produced many small parties and unstable coalitions'),
            ('protectionism', 'protecting domestic industry with tariffs and quotas, such as the US Smoot–Hawley Tariff of 1930')],
     facts=[('In which month and year did the Wall Street Crash occur?', 'October 1929', ['October 1919', 'January 1933', 'September 1939'], 'Black Thursday was 24 October and Black Tuesday 29 October.'),
            ('About how many Germans were unemployed by early 1932?', 'About 6 million', ['About 600,000', 'About 60 million', 'About 60,000'], 'Roughly a third of the workforce.'),
            ('In November 1923, about how many German marks were needed to buy one US dollar?', 'About 4.2 trillion', ['About 4.2', 'About 420', 'About 4,200'], 'Hyperinflation destroyed savings.'),
            ('Which US law of 1930 raised tariffs and worsened the collapse of world trade?', 'The Smoot–Hawley Tariff Act', ['the New Deal', 'the Marshall Plan', 'the Dawes Plan'], 'Other countries retaliated.'),
            ('By roughly how much did world trade fall between 1929 and 1933?', 'About two-thirds in value', ['About 5%', 'It doubled', 'It did not change'], 'Kindleberger\'s spiral illustrates the collapse.')],
     why=[('Explain why the Great Depression hit Germany especially hard.', 'German recovery depended on US loans under the Dawes Plan; after 1929 these loans were recalled, causing bank failures, collapsing industry and mass unemployment.'),
          ('Explain why the Depression weakened support for democracy in Europe.', 'Mass unemployment and poverty made people lose faith in democratic governments that seemed unable to act, so extremist parties promising strong leadership gained support.'),
          ('Explain why proportional representation contributed to instability in Weimar Germany.', 'It allowed many small parties into the Reichstag, so no party won a majority and governments were short-lived coalitions that struggled to agree on policies during crises.'),
          ('Explain why protectionism deepened the Depression.', 'When countries raised tariffs to protect their industries, others retaliated, so world trade collapsed and export industries lost markets, increasing unemployment.')],
     contrast=[('the hyperinflation of 1923', 'the Depression of 1929–33', 'Hyperinflation in 1923 destroyed savings through rapidly rising prices; the Depression brought falling prices, collapsing output and mass unemployment.'),
               ('Article 48 emergency rule', 'parliamentary government', 'Article 48 let the president govern by decree without the Reichstag; parliamentary government relies on laws passed by elected representatives.')],
     misc=[('The Wall Street Crash alone caused the Great Depression.', 'The crash was a trigger; overproduction, weak banks, debt, the gold standard and protectionism turned it into a global depression.'),
           ('Weimar Germany was a failure from the start.', 'It survived the crises of 1919–23 and enjoyed relative stability and cultural achievement in 1924–29 under Stresemann.'),
           ('Hitler came to power by winning a majority of votes.', 'The Nazis never won a majority in free elections; their highest vote was 37% in July 1932, and Hitler was appointed chancellor through elite deals.')],
     cases=[('Germany\'s hyperinflation of 1923', 'After the Ruhr occupation the government printed money to pay striking workers; by November a loaf of bread cost billions of marks.', 'economic crisis undermining democracy', 'the middle classes lost savings and trust in the republic.'),
            ('Brüning\'s deflationary policies', 'Chancellor Heinrich Brüning (1930–32) cut spending and wages using Article 48 decrees; unemployment kept rising.', 'the weakening of parliamentary democracy', 'rule by decree made democracy seem irrelevant and austerity deepened the crisis.')],
     evaluate=[('The Great Depression was the main reason for the collapse of democracy in Germany.', ['unemployment of 6 million drove voters to the Nazis and Communists', 'the Nazi vote jumped from 2.6% in 1928 to 37% in July 1932'], ['the constitution\'s weaknesses, such as Article 48 and PR, made government unstable', 'elite politicians such as von Papen chose to bring Hitler into power'], 'The Depression was the essential trigger, but structural weaknesses and the decisions of conservative elites explain why democracy collapsed rather than survived as in Britain or the USA.')],
     src=[('Economic history (paraphrased)', 'The historian argued that the world depression was so deep and long because no country was willing or able to act as a stabiliser: Britain no longer could and the United States would not, so no one kept markets open, provided loans or acted as a lender of last resort.', 'Paraphrase of Charles P. Kindleberger, The World in Depression, 1929–1939, Berkeley, 1973', 'to explain the causes and duration of the Depression', 'It is an influential analysis by a leading economic historian.', 'It focuses on international leadership and gives less weight to domestic policies such as the gold standard.', 'The Depression was deep because there was no international leader to stabilise the economy.')],
     rq=[('How far did US loan recalls after 1929 cause the rise in German unemployment between 1929 and 1932?', 'What was the Depression?', 'it is a definition question', 'It tests a causal link using economic data.', 'Use German unemployment statistics, loan data and two historians; graph trends; weigh other causes; cite in MLA.')])


@R.add('ch02-st1', ('C3', 'C4'), (1, 5), 'numerical')
def inflation(rng, slot):
    rows = [('January 1922', 191.8), ('July 1922', 493.2), ('January 1923', 17_972), ('July 1923', 353_412), ('September 1923', 98_860_000),
            ('November 1923', 4_200_000_000_000)]
    a, b = sorted(rng.sample(rows, 2), key=lambda r: r[1])
    f = b[1] / a[1]
    if slot.d <= 3:
        return dict(stem=f'The exchange rate was about {a[1]:,} marks per US dollar in {a[0]} and about {b[1]:,} marks per dollar in {b[0]}. By what factor did the number of marks per dollar increase?',
                    answer=f'about {f:,.0f} times' if f >= 10 else f'about {f:.1f} times', type='numerical', marks=2,
                    markingKey=f'{b[1]:,} ÷ {a[1]:,} = {f:,.1f} (M1 A1). Approximate historical rates.', gap='G3')
    price = rng.choice([0.25, 0.5, 1])
    marks_needed = price * b[1]
    return dict(stem=(f'In {b[0]} one US dollar was worth about {b[1]:,} marks (approx.). A loaf of bread cost the equivalent of about US$ {price}. '
                      'Calculate the price of the loaf in marks, and explain two effects of hyperinflation on German society.'),
                answer=f'about {marks_needed:,.0f} marks', type='multi_step', marks=5,
                markingKey=f'{price} × {b[1]:,} = {marks_needed:,.0f} marks (M1 A1). Effects (3): savings and pensions wiped out (middle classes hit hardest); wages lost value daily; '
                           'debtors and some businesses gained; loss of trust in the republic.', gap='G5')


K.st('ch02-st2', 'political ideologies: democracy, communism, fascism and Nazism',
     terms=[('liberal democracy', 'a political system with free elections, the rule of law, protection of individual rights and peaceful transfer of power'),
            ('communism', 'an ideology based on Marx and Engels aiming at a classless society with collective ownership of the means of production'),
            ('fascism', 'an authoritarian, ultra-nationalist ideology emphasising a single leader, one party, militarism and the subordination of the individual to the state; first in power in Italy under Mussolini'),
            ('Nazism', 'the German form of fascism under Hitler, combining extreme nationalism, dictatorship and racist antisemitic ideology'),
            ('totalitarianism', 'a system in which a single party seeks total control over every aspect of public and private life'),
            ('authoritarianism', 'government by a ruler or small group that is not accountable to the people and restricts political freedom'),
            ('political spectrum', 'a way of placing ideologies from left (radical change, equality) to right (tradition, hierarchy)')],
     facts=[('In which year did Mussolini become prime minister of Italy after the March on Rome?', '1922', ['1919', '1933', '1940'], 'King Victor Emmanuel III appointed him.'),
            ('Which 1848 text by Marx and Engels set out the ideas of communism?', 'The Communist Manifesto', ['Mein Kampf', 'The Wealth of Nations', 'The Social Contract'], 'It called on workers of the world to unite.'),
            ('Which revolution in 1917 brought the Bolsheviks to power in Russia?', 'The October Revolution', ['the February Revolution only', 'the Glorious Revolution', 'the French Revolution'], 'Led by Lenin.'),
            ('Which of these is a feature shared by fascist and communist states in the 1930s?', 'A single-party state using censorship and secret police', ['Free multiparty elections', 'An independent free press', 'Private ownership as the core economic belief of both'], 'Both were totalitarian in practice.'),
            ('Which country remained a democracy throughout the interwar years despite the Depression?', 'Britain', ['Italy', 'Germany', 'Spain'], 'Also France, Czechoslovakia (until 1938) and the Scandinavian states.')],
     why=[('Explain why fascism appealed to many people in Italy after 1918.', 'Italians were angry at the "mutilated victory" at Paris, feared communist revolution after strikes in 1919–20 and wanted order, national greatness and strong leadership, which Mussolini promised.'),
          ('Explain why communism and fascism are placed at opposite ends of the political spectrum but are both totalitarian.', 'Communism aims at class equality and collective ownership, fascism at national unity and hierarchy; but in practice both used single-party rule, terror, propaganda and control of society.'),
          ('Explain why liberal democracy was under pressure in the 1930s.', 'Economic depression, fear of communism, nationalist grievances and the apparent success of dictatorships made many people doubt that democratic governments could solve crises.'),
          ('Explain why racial ideology was central to Nazism.', 'Nazis believed in a racial hierarchy and a "national community" defined by race; this ideology justified persecution of Jews and other groups and expansion to gain "living space" in the east.')],
     contrast=[('communism', 'fascism', 'Communism is internationalist, aims at a classless society and collective ownership; fascism is ultra-nationalist, accepts private property under state direction and glorifies the nation and leader.'),
               ('authoritarianism', 'totalitarianism', 'Authoritarian regimes restrict political freedom but may leave parts of society alone; totalitarian regimes seek control of all aspects of life, including beliefs.')],
     misc=[('Fascism and Nazism are exactly the same.', 'Nazism was a form of fascism, but its racial antisemitic ideology was more central and extreme than in Italian Fascism, at least before 1938.'),
           ('Communist states in practice achieved a classless, stateless society.', 'Soviet communism created a powerful state and a new privileged party elite, far from Marx\'s ideal.'),
           ('Democracy collapsed everywhere in Europe in the 1930s.', 'Britain, France, the Netherlands, Scandinavia, Switzerland and others remained democracies, though under strain.')],
     cases=[('Mussolini\'s Italy', 'After 1922 Mussolini built a one-party state, banned opposition parties by 1926 and used propaganda and the OVRA secret police.', 'fascism in power', 'it provided the first model of a fascist dictatorship.'),
            ('Czechoslovakia in the interwar years', 'Under President Tomáš Masaryk, Czechoslovakia remained a parliamentary democracy until 1938 despite economic and minority tensions.', 'democratic survival', 'it shows that democracy could survive in new states created in 1918.')],
     evaluate=[('Communism and fascism had more in common than their ideologies suggest.', ['both created single-party states with a leader cult, secret police and propaganda', 'both sought to control the economy and society'], ['their goals differed fundamentally: class equality versus national/racial hierarchy', 'their economic systems differed: collective ownership versus private business under state direction'], 'In methods of rule they were similar, which is why many historians use "totalitarianism"; in aims and economic organisation they differed greatly.')],
     src=[('Political writing (paraphrased)', 'The authors argued that the history of all existing society is the history of class struggles, and that the working class would overthrow capitalism and create a society without classes, in which the means of production would be owned in common.', 'Paraphrase of Karl Marx and Friedrich Engels, The Communist Manifesto, London, 1848', 'to set out the aims of the Communist League and rally workers', 'It is the foundational statement of communist ideology.', 'It is a political pamphlet, not a description of how communist states actually operated in the 20th century.', 'Class struggle drives history and workers will create a classless society.')],
     rq=[('How did Mussolini consolidate his power in Italy between 1922 and 1926?', 'What is fascism?', 'it is a definition question', 'It investigates how an ideology was put into practice.', 'Use laws, speeches (paraphrased) and two historians; build a timeline; compare factors such as violence and legal changes; cite in MLA.')])
C.chronology(K, 'ch02-st2', events=[('The Communist Manifesto is published', 1848), ('the October Revolution in Russia', 1917), ('the March on Rome', 1922),
                                     ('the USSR is formed', 1922), ('Mussolini bans opposition parties', 1926), ('Hitler becomes chancellor of Germany', 1933),
                                     ('the Spanish Civil War begins', 1936), ('Germany annexes Austria (Anschluss)', 1938)])


K.st('ch02-st3', 'the rise of Hitler and Nazi Germany: methods and propaganda',
     terms=[('Enabling Act', 'the law of March 1933 that allowed Hitler\'s government to make laws without the Reichstag for four years'),
            ('Reichstag Fire', 'the burning of the German parliament building on 27 February 1933, used to justify emergency decrees suspending civil rights'),
            ('Night of the Long Knives', 'the purge of 30 June–2 July 1934 in which the SA leadership and other opponents were killed'),
            ('Gestapo', 'the Nazi secret state police'),
            ('propaganda', 'information, often biased or misleading, used to promote a political cause or point of view'),
            ('Volksgemeinschaft', 'the Nazi idea of a "people\'s community" united by race and loyalty, which excluded those the regime defined as outsiders'),
            ('Gleichschaltung', '"coordination": the Nazi process of bringing all institutions, organisations and media under party control')],
     facts=[('On what date was Hitler appointed chancellor?', '30 January 1933', ['9 November 1923', '27 February 1933', '1 September 1939'], 'President Hindenburg appointed him.'),
            ('In the July 1932 Reichstag election, about what share of the vote did the Nazis win?', 'About 37%', ['About 2.6%', 'About 51%', 'About 90%'], 'It made them the largest party.'),
            ('Who headed the Ministry of Public Enlightenment and Propaganda?', 'Joseph Goebbels', ['Heinrich Himmler', 'Hermann Göring', 'Ernst Röhm'], 'He controlled press, radio and film.'),
            ('Which 1935 laws removed German citizenship from Jews?', 'The Nuremberg Laws', ['the Enabling Act', 'the Dawes Plan', 'the Munich Agreement'], 'They also banned marriages between Jews and non-Jews.'),
            ('In August 1934, after Hindenburg\'s death, Hitler combined the posts of chancellor and president with which title?', 'Führer', ['Kaiser', 'Duce', 'General Secretary'], 'The army swore an oath of personal loyalty to him.')],
     why=[('Explain why the Nazis gained support between 1929 and 1932.', 'The Depression created mass unemployment and fear; the Nazis offered strong leadership, jobs and national revival, used modern propaganda and blamed scapegoats, appealing to many groups.'),
          ('Explain why the Enabling Act was important for Hitler.', 'It allowed his government to make laws without the Reichstag, giving a legal appearance to dictatorship and enabling him to ban parties and trade unions.'),
          ('Explain why the Night of the Long Knives strengthened Hitler\'s position.', 'It removed SA leaders such as Röhm who threatened the army\'s support, eliminated other rivals and showed that Hitler would use violence, securing the army\'s backing.'),
          ('Explain why propaganda was central to the Nazi regime.', 'It built the Hitler myth, spread Nazi ideology, created consent for policies and dehumanised groups targeted for persecution, while censorship removed alternative views.')],
     contrast=[('propaganda', 'terror', 'Propaganda sought to persuade people to support the regime; terror (Gestapo, SS, camps) sought to frighten people into obedience.'),
               ('consent', 'coercion', 'Consent is support given willingly, for example due to jobs or propaganda; coercion is obedience forced by fear and repression.')],
     misc=[('Hitler seized power in a violent revolution in 1933.', 'He was appointed legally by President Hindenburg after conservative politicians believed they could control him; the dictatorship was then built step by step.'),
           ('All Germans supported the Nazis.', 'Many Germans conformed through fear or apathy; some resisted, such as the White Rose group and parts of the churches and labour movement.'),
           ('Nazi propaganda was only about posters and rallies.', 'It also used radio (the cheap People\'s Receiver), film, newspapers, schools, youth groups, sport (the 1936 Olympics) and the arts.')],
     cases=[('the 1936 Berlin Olympics', 'The regime used the Games to present a modern, peaceful Germany to the world, temporarily removing some antisemitic signs; Jesse Owens won four gold medals.', 'propaganda', 'a global event was used to improve Germany\'s international image.'),
            ('the Hitler Youth', 'Membership became compulsory in 1936 (enforced from 1939); by 1939 it had about 8 million members.', 'control of society', 'the regime aimed to shape young people\'s beliefs and loyalty.')],
     evaluate=[('Propaganda was more important than terror in maintaining Nazi control of Germany.', ['propaganda created the Hitler myth and genuine popularity among many', 'economic recovery and full employment, publicised by propaganda, won support'], ['the Gestapo, camps and informers crushed opposition', 'fear of denunciation silenced critics'], 'Historians such as Ian Kershaw argue that consent and coercion worked together: propaganda won many, while terror targeted those who would not conform.')],
     src=[('Historian\'s interpretation (paraphrased)', 'The historian argued that Hitler\'s power rested heavily on a "Hitler myth" – an image of a leader above party politics who embodied the nation – created by propaganda and sustained by foreign policy successes, and that it declined as the war turned against Germany.', 'Paraphrase of Ian Kershaw, The "Hitler Myth": Image and Reality in the Third Reich, Oxford, 1987', 'to analyse popular opinion and the role of propaganda in the Third Reich', 'It uses reports on public opinion from many sources.', 'Public opinion in a dictatorship is hard to measure, so conclusions are partly interpretive.', 'Propaganda created an image of Hitler that underpinned the regime\'s popularity.')],
     rq=[('How effective was Nazi radio propaganda in shaping public opinion in Germany between 1933 and 1939?', 'Who was Hitler?', 'it is a biographical, descriptive question', 'It evaluates a specific method of control.', 'Use radio ownership data, SOPADE reports and two historians; evaluate sources; reach a judgement; cite in MLA.')])
C.chronology(K, 'ch02-st3', events=[('the Munich (Beer Hall) Putsch', 1923), ('the Wall Street Crash', 1929), ('the Nazis become the largest party in the Reichstag', 1932),
                                     ('Hitler is appointed chancellor and the Enabling Act passes', 1933), ('the Night of the Long Knives', 1934), ('the Nuremberg Laws', 1935),
                                     ('the Berlin Olympics', 1936), ('Kristallnacht', 1938)])


@R.add('ch02-st3', ('C3', 'C4'), (1, 5), 'numerical')
def nazi_vote(rng, slot):
    rows = [('May 1928', 2.6, 12), ('September 1930', 18.3, 107), ('July 1932', 37.3, 230), ('November 1932', 33.1, 196), ('March 1933', 43.9, 288)]
    tot = {'May 1928': 491, 'September 1930': 577, 'July 1932': 608, 'November 1932': 584, 'March 1933': 647}
    a, b = sorted(rng.sample(rows, 2), key=lambda r: list(tot).index(r[0]))
    if slot.d <= 2:
        sp = a[2] / tot[a[0]] * 100
        return dict(stem=f'In the Reichstag election of {a[0]} the Nazi party won {a[2]} of {tot[a[0]]} seats. Calculate its share of seats as a percentage, and compare it with its vote share of {a[1]}%.',
                    answer=f'{sp:.1f}% of seats, close to its {a[1]}% vote share', type='numerical', marks=3,
                    markingKey=f'{a[2]} ÷ {tot[a[0]]} × 100 = {sp:.1f}% (M1 A1); similar to vote share because of proportional representation (R1).', gap='G3')
    ch = b[1] - a[1]
    return dict(stem=(f'The Nazi vote share was {a[1]}% in {a[0]} and {b[1]}% in {b[0]}. Calculate the change in percentage points and explain two reasons for the change.'),
                answer=f'{ch:+.1f} percentage points', type='multi_step', marks=4,
                markingKey=f'{b[1]} − {a[1]} = {ch:+.1f} points (M1 A1). Reasons (2) linked to the period: e.g. Depression and unemployment, propaganda, fear of communism; '
                           + ('in Nov 1932 slight economic recovery and voter fatigue reduced support; ' if 'November 1932' in (a[0], b[0]) else '')
                           + ('in March 1933 Nazi control of government, intimidation and the Reichstag Fire decree.' if b[0] == 'March 1933' else ''), gap='G5')


K.st('ch02-st4', 'Stalin\'s USSR: collectivisation, the Five-Year Plans and the Terror',
     terms=[('collectivisation', 'the forced merging of private peasant farms into large state-controlled collective farms (kolkhozy) from 1929'),
            ('Five-Year Plan', 'a centrally planned programme setting production targets for industry; the first ran from 1928'),
            ('kulak', 'a term for a relatively prosperous peasant; "dekulakisation" targeted millions for deportation or death'),
            ('Gulag', 'the Soviet system of forced labour camps'),
            ('Great Terror', 'the mass repression of 1936–38, including show trials and about 680,000 recorded executions'),
            ('Gosplan', 'the Soviet state planning committee that set economic targets'),
            ('Holodomor', 'the man-made famine in Ukraine in 1932–33, caused by collectivisation and grain requisitioning, in which millions died')],
     facts=[('In which year did Stalin launch the first Five-Year Plan?', '1928', ['1917', '1924', '1941'], 'It focused on heavy industry.'),
            ('Which new industrial city was built around a huge steelworks in the Urals during the first Five-Year Plan?', 'Magnitogorsk', ['Leningrad', 'Kyiv', 'Odesa'], 'It became a symbol of Soviet industrialisation.'),
            ('Which miner was celebrated in 1935 for cutting 102 tonnes of coal in one shift?', 'Alexei Stakhanov', ['Leon Trotsky', 'Sergei Kirov', 'Nikolai Bukharin'], 'The Stakhanovite movement promoted high output.'),
            ('Whose assassination in 1934 was used to justify the purges?', 'Sergei Kirov', ['Lenin', 'Trotsky', 'Zinoviev'], 'He was the Leningrad party leader.'),
            ('About how many people died in the famines of 1932–33 in the USSR, including Ukraine and Kazakhstan?', 'About 5–7 million', ['About 50,000', 'About 500,000', 'About 50 million'], 'Estimates vary.')],
     why=[('Explain why Stalin introduced the Five-Year Plans.', 'He wanted to industrialise rapidly to catch up with the West, build military strength against perceived threats, and create a socialist economy and working class.'),
          ('Explain why Stalin introduced collectivisation.', 'He wanted to secure grain to feed the cities and to export to pay for industrial machinery, to control the peasantry and to eliminate private farming.'),
          ('Explain why collectivisation caused famine.', 'Peasants resisted by slaughtering livestock, experienced farmers were deported, production fell, and the state still requisitioned grain, leaving rural areas without food.'),
          ('Explain why Stalin launched the Great Terror.', 'He sought to eliminate real and imagined rivals, old Bolsheviks and military leaders, to create fear and total loyalty and to blame failures on "enemies".')],
     contrast=[('the achievements of the Five-Year Plans', 'their human costs', 'Industrial output, especially coal, steel and electricity, rose rapidly; but this was achieved through forced labour, low living standards, famine and repression.'),
               ('a command economy', 'a market economy', 'In a command economy the state owns industry and sets output and prices; in a market economy private firms respond to prices set by supply and demand.')],
     misc=[('All Soviet economic targets were met.', 'Many targets were unrealistic and statistics were exaggerated; consumer goods and housing fell well short.'),
           ('The Terror only affected Stalin\'s political rivals.', 'It affected millions of ordinary people, including workers, peasants, ethnic minorities and army officers.'),
           ('Collectivisation increased food production immediately.', 'Grain output and especially livestock numbers fell sharply in the early 1930s.')],
     cases=[('Magnitogorsk', 'Built from 1929 on the steppe, the city had a huge steelworks constructed by workers, volunteers and forced labourers in harsh conditions.', 'rapid industrialisation', 'it shows both the scale of achievement and the human cost of the Five-Year Plans.'),
            ('the Moscow show trials', 'Between 1936 and 1938 leading Bolsheviks such as Zinoviev, Kamenev and Bukharin confessed to invented crimes and were executed.', 'the Great Terror', 'public trials spread fear and eliminated potential rivals.')],
     evaluate=[('Stalin\'s economic policies were a success.', ['industrial output grew rapidly and the USSR could fight and win the Second World War', 'new cities, factories and dams were built'], ['collectivisation caused famine with millions of deaths', 'living standards fell and growth relied on forced labour'], 'In industrial and military terms they achieved much, but at an enormous human cost; whether this counts as success depends on the criteria used.')],
     src=[('Speech (paraphrased)', 'The leader told industrial managers that the USSR was fifty to a hundred years behind the advanced countries and must make good the distance in ten years, or it would be crushed.', 'Paraphrase of Joseph Stalin, speech to the First All-Union Conference of Leading Personnel of Socialist Industry, Moscow, 4 February 1931', 'to justify the speed of industrialisation and motivate managers', 'It shows Stalin\'s official reasons for rapid industrialisation.', 'It is a public speech designed to motivate; it ignores the costs and his own political motives.', 'The USSR had to industrialise rapidly to survive.')],
     rq=[('How far did collectivisation achieve Stalin\'s aims for Soviet agriculture between 1929 and 1939?', 'Was Stalin bad?', 'it is a vague value question', 'It measures policy against stated aims using data.', 'Use grain and livestock statistics, Stalin\'s speeches and two historians; compare aims and outcomes; evaluate sources; cite in MLA.')])


@R.add('ch02-st4', ('C3', 'C4'), (1, 5), 'numerical')
def five_year(rng, slot):
    rows = [('coal', 'million tonnes', 35.4, 64.3, 128.0), ('steel', 'million tonnes', 4.0, 5.9, 17.7), ('oil', 'million tonnes', 11.7, 21.4, 28.5),
            ('electricity', 'billion kWh', 5.0, 13.4, 36.2)]
    g, unit, y28, y32, y37 = rng.choice(rows)
    pairs = [(1928, y28, 1932, y32), (1932, y32, 1937, y37), (1928, y28, 1937, y37)]
    a, va, b, vb = rng.choice(pairs)
    pc = (vb - va) / va * 100
    if slot.d <= 3:
        return dict(stem=f'Official Soviet figures give {g} output as {va} {unit} in {a} and {vb} {unit} in {b}. Calculate the percentage increase.',
                    answer=f'{pc:.0f}%', type='numerical', marks=2, markingKey=f'({vb} − {va}) ÷ {va} × 100 = {pc:.0f}% (M1 A1).', gap='G3')
    return dict(stem=(f'Official Soviet statistics show {g} output rising from {va} {unit} ({a}) to {vb} {unit} ({b}). Calculate the percentage increase, '
                      'and evaluate how far historians can rely on these figures as evidence of the success of the Five-Year Plans.'),
                answer=f'{pc:.0f}%', type='multi_step', marks=6,
                markingKey=f'({vb} − {va}) ÷ {va} × 100 = {pc:.0f}% (M1 A1). Evaluation (4): official figures were produced to show success and managers inflated output to meet targets; '
                           'quality was often poor; Western estimates are lower but still show rapid growth; consumer goods and human costs are not shown.', gap='G5')


# =============================================================================================
# ch03 The Second World War and the Holocaust
# =============================================================================================
WW2_EVENTS = [('Japan invades Manchuria', 1931), ('Germany leaves the League of Nations', 1933), ('Italy invades Abyssinia', 1935),
              ('Germany remilitarises the Rhineland', 1936), ('the Anschluss and the Munich Agreement', 1938), ('Germany invades Poland', 1939),
              ('the Battle of Britain', 1940), ('Germany invades the USSR (Operation Barbarossa)', 1941), ('Japan attacks Pearl Harbor', 1941),
              ('the Battle of Midway', 1942), ('the German surrender at Stalingrad', 1943), ('the D-Day landings in Normandy', 1944),
              ('the atomic bombings of Hiroshima and Nagasaki', 1945), ('the United Nations Charter comes into force', 1945)]

K.st('ch03-st1', 'the causes of the Second World War: appeasement, expansion and the failure of the League of Nations',
     terms=[('appeasement', 'the policy, associated with Neville Chamberlain, of making concessions to Hitler to avoid war'),
            ('League of Nations', 'the international organisation set up in 1920 to keep peace through collective security'),
            ('collective security', 'the principle that members of an organisation act together against an aggressor'),
            ('Anschluss', 'the union of Germany and Austria, carried out by Germany in March 1938'),
            ('Munich Agreement', 'the September 1938 agreement by Britain, France, Italy and Germany allowing Germany to take the Sudetenland'),
            ('Nazi–Soviet Pact', 'the non-aggression pact of 23 August 1939 between Germany and the USSR, with secret terms dividing Poland'),
            ('Lebensraum', 'the Nazi aim of "living space" for Germans in Eastern Europe')],
     facts=[('Which Japanese action in 1931 was the first major test of the League of Nations?', 'The invasion of Manchuria', ['the attack on Pearl Harbor', 'the invasion of Korea', 'the bombing of Shanghai in 1937 only'], 'The Lytton Report condemned Japan, which left the League.'),
            ('Which country invaded Abyssinia (Ethiopia) in 1935?', 'Italy', ['Germany', 'Japan', 'Britain'], 'League sanctions excluded oil.'),
            ('When did Germany remilitarise the Rhineland?', 'March 1936', ['March 1933', 'September 1938', 'September 1939'], 'It broke the Treaty of Versailles and Locarno.'),
            ('Which British prime minister signed the Munich Agreement?', 'Neville Chamberlain', ['Winston Churchill', 'Stanley Baldwin', 'Clement Attlee'], 'He claimed "peace for our time".'),
            ('On what date did Britain and France declare war on Germany?', '3 September 1939', ['1 September 1939', '7 December 1941', '28 June 1919'], 'Two days after Germany invaded Poland.')],
     why=[('Explain why the League of Nations failed to stop aggression in the 1930s.', 'It lacked an army, the USA never joined, decisions required unanimity, Britain and France put their own interests first, and sanctions were weak, as in Abyssinia.'),
          ('Explain why Britain followed a policy of appeasement.', 'Memories of the First World War, economic weakness, belief that Versailles had been unfair, fear of bombing, the need to rearm, and lack of support from the Dominions and the USA encouraged concessions.'),
          ('Explain why the Nazi–Soviet Pact made war more likely.', 'It removed the threat of a two-front war for Germany, so Hitler could invade Poland expecting no Soviet resistance.'),
          ('Explain why the Abyssinian Crisis damaged the League.', 'Britain and France did not ban oil sales or close the Suez Canal, and the secret Hoare–Laval Pact offered Italy much of Abyssinia, showing that collective security did not work.')],
     contrast=[('appeasement', 'collective security', 'Appeasement meant individual powers giving concessions to an aggressor; collective security meant all League members acting together against aggression.'),
               ('Hitler\'s actions in 1936–38', 'his invasion of Poland in 1939', 'Earlier actions involved German-speaking areas and were partly tolerated; invading Poland was clear aggression against a non-German state that Britain and France had guaranteed.')],
     misc=[('Appeasement was simply cowardice.', 'Many historians argue it reflected real military, economic and political constraints and bought time for British rearmament.'),
           ('Hitler had a detailed timetable for war from 1933.', 'Historians such as A. J. P. Taylor argue he was an opportunist; others such as Hugh Trevor-Roper emphasise long-term aims – the debate continues.'),
           ('The League of Nations achieved nothing.', 'It settled some disputes in the 1920s, such as the Åland Islands (1921), and its agencies did valuable work on refugees and health.')],
     cases=[('the Munich Agreement', 'On 29–30 September 1938 Britain and France agreed that Germany could annex the Sudetenland; Czechoslovakia was not invited.', 'appeasement at its height', 'concessions encouraged Hitler, who occupied the rest of Czechoslovakia in March 1939.'),
            ('the Manchurian Crisis', 'After Japan occupied Manchuria in 1931, the League\'s Lytton Report took a year; Japan left the League in 1933.', 'the failure of collective security', 'the League could not act against a great power.')],
     evaluate=[('Appeasement was the main cause of the Second World War.', ['concessions encouraged Hitler to make further demands', 'it convinced Hitler that Britain and France would not fight'], ['Hitler\'s ideology and expansionist aims drove the war', 'the failure of the League and the Nazi–Soviet Pact were also crucial'], 'Appeasement contributed by encouraging Hitler, but the primary cause was Nazi expansionism; appeasement explains why he was not stopped earlier rather than why war happened.')],
     src=[('Historian\'s interpretation (paraphrased)', 'The historian argued that Hitler was not following a fixed blueprint but acted as an opportunist, taking advantage of the weaknesses and mistakes of other powers; he suggested the war of 1939 was more the result of diplomatic blunders than a long-planned war.', 'Paraphrase of A. J. P. Taylor, The Origins of the Second World War, London, 1961', 'to challenge the view that Hitler alone planned the war', 'It provoked important debate and considered the role of other powers.', 'Many historians argue it underplays Hitler\'s ideology and aims set out in Mein Kampf.', 'The war resulted from opportunism and mistakes rather than a fixed plan.')],
     rq=[('To what extent was the Munich Agreement of 1938 a reasonable policy for Britain at the time?', 'What caused WWII?', 'it is too broad', 'It assesses a decision in its context using contemporary evidence.', 'Use cabinet records, military figures on rearmament, opinion polls and two historians; compare views; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch03-st1', events=WW2_EVENTS[:6] + [('the League of Nations is founded', 1920), ('the Locarno Treaties', 1925)])


K.st('ch03-st2', 'a global war: key turning points in Europe, Asia and the Pacific',
     terms=[('Blitzkrieg', '"lightning war": fast attacks combining tanks, aircraft and infantry, used by Germany in 1939–41'),
            ('turning point', 'a moment after which the course of events changes decisively'),
            ('Operation Barbarossa', 'the German invasion of the Soviet Union launched on 22 June 1941'),
            ('island hopping', 'the US strategy in the Pacific of capturing selected islands to approach Japan while bypassing others'),
            ('D-Day', 'the Allied landings in Normandy on 6 June 1944 (Operation Overlord)'),
            ('Lend-Lease', 'the US programme from March 1941 that supplied weapons and materials to Britain, the USSR and other Allies')],
     facts=[('Which battle, in June 1942, saw the US Navy sink four Japanese aircraft carriers?', 'The Battle of Midway', ['the Battle of the Coral Sea', 'Pearl Harbor', 'Iwo Jima'], 'It ended Japanese naval superiority in the Pacific.'),
            ('When did the German Sixth Army surrender at Stalingrad?', 'February 1943', ['June 1941', 'June 1944', 'May 1945'], 'About 91,000 German soldiers were captured.'),
            ('Which 1943 battle near Kursk was the largest tank battle in history?', 'The Battle of Kursk', ['El Alamein', 'the Bulge', 'Dunkirk'], 'After it the Red Army held the initiative.'),
            ('Where did British and Commonwealth forces defeat Rommel in late 1942?', 'El Alamein, Egypt', ['Dunkirk, France', 'Singapore', 'Kohima, India'], 'It was a turning point in North Africa.'),
            ('Which battles in 1944 stopped the Japanese invasion of India?', 'Imphal and Kohima', ['Midway and Coral Sea', 'Leyte Gulf and Okinawa', 'Anzio and Monte Cassino'], 'Indian troops formed a large part of the British 14th Army.')],
     why=[('Explain why Stalingrad is seen as a turning point in the war.', 'The destruction of the German Sixth Army ended German advances in the east, boosted Soviet morale and began a Red Army advance that continued to Berlin.'),
          ('Explain why the attack on Pearl Harbor changed the course of the war.', 'It brought the United States, with its vast industrial capacity, fully into the war in both the Pacific and Europe after Germany also declared war on it.'),
          ('Explain why Midway was a turning point in the Pacific.', 'Japan lost four carriers and experienced aircrews it could not replace, so the US gained the initiative and moved to the offensive.'),
          ('Explain why economic strength helped the Allies win.', 'The USA and USSR could out-produce the Axis in tanks, aircraft and ships, and Lend-Lease supplied allies, so Germany and Japan could not replace their losses.')],
     contrast=[('the war in Europe', 'the war in the Pacific', 'In Europe the decisive fighting was on land, especially on the Eastern Front; in the Pacific, naval and air power and island-hopping were decisive.'),
               ('a turning point', 'a decisive victory', 'A turning point changes the direction of a conflict; a decisive victory settles a battle, and not every decisive victory changes the whole war.')],
     misc=[('D-Day was the main reason Germany was defeated.', 'Most German military losses occurred on the Eastern Front; D-Day opened a second front that hastened defeat.'),
           ('The Second World War was fought only by European and American soldiers.', 'About 2.5 million Indians served in the Indian Army, the largest volunteer army in history, and soldiers from Africa, China, Australia and many other places fought.'),
           ('Japan surrendered immediately after Hiroshima.', 'Japan surrendered on 15 August 1945 after the bombings of Hiroshima (6 August) and Nagasaki (9 August) and the Soviet declaration of war (8 August).')],
     cases=[('the Battle of Stalingrad', 'From August 1942 to February 1943 Soviet forces defended the city and encircled the German Sixth Army in Operation Uranus.', 'a turning point on the Eastern Front', 'it marked the start of German retreat in the east.'),
            ('Imphal and Kohima', 'In 1944 British and Indian troops held off a Japanese offensive into north-east India; Japanese losses were very heavy.', 'a turning point in Asia', 'the defeat opened the way to the Allied reconquest of Burma.')],
     evaluate=[('The Battle of Stalingrad was the most important turning point of the Second World War.', ['it destroyed a German army and began Soviet advances', 'the Eastern Front was where most German forces were defeated'], ['Midway transformed the Pacific war', 'US entry after Pearl Harbor brought overwhelming economic power'], 'Stalingrad was arguably the decisive turning point in Europe, but the war was global; Midway and US entry were equally important in the Pacific.')],
     src=[('Memoir (paraphrased)', 'The British general recalled that at Imphal and Kohima Indian and British soldiers fought side by side in extremely difficult jungle and mountain conditions, and that the Japanese army suffered its greatest defeat on land up to that time.', 'Paraphrase of William Slim, Defeat into Victory, London, 1956', 'to give the commander\'s account of the Burma campaign', 'It is the account of the general who led the 14th Army.', 'As a memoir written after the war, it may emphasise his own decisions and the army\'s success.', 'Imphal and Kohima were a major defeat for Japan, won by Indian and British troops together.')],
     rq=[('How significant was the contribution of the Indian Army to Allied victory in Burma between 1943 and 1945?', 'What happened in WWII?', 'it is far too broad', 'It examines an often-overlooked contribution with evidence.', 'Use war diaries, Slim\'s memoir and two historians; compare troop numbers and campaigns; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch03-st2', events=WW2_EVENTS[5:13] + [('the Battle of Kursk', 1943), ('the battles of Imphal and Kohima', 1944)])


@R.add('ch03-st2', ('C3', 'C4'), (1, 5), 'numerical')
def production(rng, slot):
    rows = [('aircraft', 'the USA', 1941, 26_277, 1944, 96_318), ('aircraft', 'Germany', 1941, 11_776, 1944, 39_807), ('aircraft', 'the USSR', 1941, 15_735, 1944, 40_246),
            ('aircraft', 'Japan', 1941, 5_088, 1944, 28_180), ('tanks', 'the USSR', 1941, 6_590, 1944, 28_963), ('tanks', 'Germany', 1941, 5_200, 1944, 17_800)]
    w, co, a, va, b, vb = rng.choice(rows)
    pc = (vb - va) / va * 100
    if slot.d <= 3:
        return dict(stem=f'{C.cap(co)} produced about {va:,} {w} in {a} and {vb:,} in {b} (approximate figures). Calculate the percentage increase.',
                    answer=f'{pc:.0f}%', type='numerical', marks=2, markingKey=f'({vb:,} − {va:,}) ÷ {va:,} × 100 = {pc:.0f}% (M1 A1).', gap='G3')
    o = [r for r in rows if r[0] == w and r[1] != co]
    if not o:
        return None
    o = rng.choice(o)
    ratio = vb / o[5]
    return dict(stem=(f'In {b}, {co} produced about {vb:,} {w} and {o[1]} about {o[5]:,} (approximate figures). Calculate the ratio of {co}\'s output to {o[1]}\'s, '
                      'and explain how far industrial production explains the outcome of the war.'),
                answer=f'about {ratio:.2f} : 1', type='multi_step', marks=6,
                markingKey=f'{vb:,} ÷ {o[5]:,} = {ratio:.2f} (M1 A1). Discussion (4): the Allies combined outproduced the Axis by a large margin, allowing losses to be replaced; '
                           'but strategy, morale, leadership, resources (oil), and key battles also mattered; Germany\'s output peaked too late.', gap='G5')


K.st('ch03-st3', 'the Holocaust: persecution, genocide and responses',
     terms=[('Holocaust', 'the systematic, state-sponsored persecution and murder of about six million Jews by Nazi Germany and its collaborators between 1941 and 1945; also known as the Shoah'),
            ('genocide', 'acts committed with intent to destroy, in whole or in part, a national, ethnic, racial or religious group (UN Genocide Convention, 1948)'),
            ('antisemitism', 'hostility to, prejudice against or discrimination against Jews'),
            ('ghetto', 'a closed area of a city where the Nazis forced Jews to live in overcrowded conditions, such as the Warsaw ghetto'),
            ('Einsatzgruppen', 'mobile killing units that murdered Jews and others in mass shootings in the occupied Soviet territories from 1941'),
            ('Righteous Among the Nations', 'the title given by Yad Vashem to non-Jews who risked their lives to save Jews during the Holocaust'),
            ('Wannsee Conference', 'the meeting of senior Nazi officials on 20 January 1942 that coordinated the implementation of the genocide of Europe\'s Jews')],
     facts=[('About how many Jews were murdered in the Holocaust?', 'About six million', ['About 600,000', 'About 60,000', 'About 60 million'], 'Around two-thirds of Europe\'s Jews.'),
            ('Which 1935 laws stripped German Jews of citizenship?', 'The Nuremberg Laws', ['the Enabling Act', 'the Munich Agreement', 'the Wannsee Protocol'], 'They defined who was Jewish by ancestry.'),
            ('What was Kristallnacht (9–10 November 1938)?', 'A state-organised pogrom in which synagogues and Jewish businesses were attacked and about 30,000 Jewish men were sent to camps', ['A peace conference', 'An election', 'A military parade'], 'It marked a sharp escalation of violence.'),
            ('Which killing centre in occupied Poland was the largest, where about 1.1 million people were murdered?', 'Auschwitz-Birkenau', ['Dachau', 'Bergen-Belsen', 'Theresienstadt'], 'Most victims were Jews.'),
            ('Which 1948 UN convention made genocide a crime under international law?', 'The Convention on the Prevention and Punishment of the Crime of Genocide', ['the Geneva Convention of 1864', 'the Kellogg–Briand Pact', 'the Treaty of Rome'], 'The term genocide was coined by Raphael Lemkin in 1944.')],
     why=[('Explain why the persecution of Jews in Germany escalated between 1933 and 1939.', 'Nazi ideology placed antisemitism at its core; the regime moved step by step from boycotts and exclusion from jobs, to the Nuremberg Laws, to the violence of Kristallnacht, testing reactions and meeting limited resistance.'),
          ('Explain why the outbreak of war in 1939 and the invasion of the USSR in 1941 led to genocide.', 'Conquest brought millions more Jews under Nazi control, war reduced restraints and outside scrutiny, and the regime moved from ghettoisation and mass shootings to systematic murder in killing centres.'),
          ('Explain why historians study bystanders as well as perpetrators.', 'Genocide relied on the participation, compliance or indifference of many people; studying bystanders helps explain how such crimes became possible and what responsibility societies hold.'),
          ('Explain why the Holocaust led to new international laws.', 'The scale of the crimes led to the Nuremberg Trials, the 1948 Genocide Convention and the Universal Declaration of Human Rights, to hold individuals accountable and protect groups in the future.')],
     contrast=[('persecution', 'genocide', 'Persecution is the systematic mistreatment of a group, such as exclusion and violence; genocide is acting with intent to destroy the group.'),
               ('perpetrators', 'rescuers', 'Perpetrators carried out or organised the killings; rescuers, such as those recognised as Righteous Among the Nations, risked their lives to save Jews.')],
     misc=[('The Holocaust was carried out by only a small group of Nazi leaders.', 'It involved large numbers of officials, soldiers, police, railway workers and collaborators across occupied Europe.'),
           ('Jews did not resist the Holocaust.', 'There was armed resistance, such as the Warsaw Ghetto Uprising (1943), and spiritual and cultural resistance in ghettos and camps.'),
           ('The Holocaust began on the first day of the Nazi regime.', 'Persecution began in 1933, but systematic mass murder began in 1941; it was a process of escalation.')],
     cases=[('the Warsaw Ghetto Uprising', 'In April–May 1943 Jewish fighters in the Warsaw ghetto resisted deportation for almost a month against much stronger German forces.', 'Jewish resistance', 'it shows that victims resisted despite overwhelming odds.'),
            ('the Danish rescue of Jews', 'In October 1943 Danish citizens helped about 7,000 Jews escape by boat to neutral Sweden.', 'rescue and responses', 'it shows that collective action by ordinary people could save lives.')],
     evaluate=[('The Holocaust was the result of long-term planning by the Nazi leadership.', ['antisemitism was central to Nazi ideology from the start', 'the Wannsee Conference coordinated genocide across Europe'], ['policy escalated in stages, often radicalised by local officials and war conditions', 'historians describe a "twisted road" from emigration plans to mass murder'], 'Historians increasingly see a combination: ideology set the goal of removing Jews, while war and competition within the regime radicalised policy into genocide.')],
     src=[('Diary (summarised)', 'A Jewish teenager hiding with her family in a secret annex in Amsterdam recorded daily life, fears of discovery and hopes for the future between 1942 and 1944. The family was discovered and deported in August 1944; she died in Bergen-Belsen in 1945.', 'Summary of Anne Frank, diary written 1942–44, first published as Het Achterhuis, Amsterdam, 1947', 'originally a private diary, later revised by the author with a view to publication after the war', 'It gives a personal, contemporary view of persecution and life in hiding.', 'It reflects one family\'s experience in hiding and does not describe the camps or the experience of the majority of victims.', 'It records the fear and hope of a Jewish family in hiding during the Holocaust.')],
     rq=[('How did the Danish population respond to the attempted deportation of Danish Jews in October 1943?', 'What was the Holocaust?', 'it is a definition question', 'It investigates responses and choices, a key question in Holocaust history.', 'Use survivor testimonies (USC Shoah Foundation), Yad Vashem records and two historians; compare with other countries; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch03-st3', events=[('the boycott of Jewish businesses in Germany', 1933), ('the Nuremberg Laws', 1935), ('Kristallnacht', 1938),
                                     ('the Warsaw ghetto is sealed', 1940), ('mass shootings by the Einsatzgruppen begin in the occupied USSR', 1941),
                                     ('the Wannsee Conference', 1942), ('the Warsaw Ghetto Uprising', 1943), ('Soviet troops liberate Auschwitz', 1945),
                                     ('the UN Genocide Convention is adopted', 1948)])


K.st('ch03-st4', 'the consequences of the war: the United Nations and a new world order',
     terms=[('United Nations', 'the international organisation founded on 24 October 1945 to maintain peace and security and promote cooperation'),
            ('Security Council', 'the UN body responsible for peace and security, with five permanent members holding a veto'),
            ('veto', 'the power of a permanent Security Council member to block a resolution'),
            ('Nuremberg Trials', 'the 1945–46 international trials of leading Nazis for crimes against peace, war crimes and crimes against humanity'),
            ('superpower', 'a state with dominant global military, economic and political power, such as the USA and USSR after 1945'),
            ('Bretton Woods system', 'the post-war economic order agreed in 1944, creating the IMF and World Bank and fixed exchange rates')],
     facts=[('Which five countries are permanent members of the UN Security Council?', 'China, France, Russia, the UK and the USA', ['Germany, Japan, India, Brazil and the USA', 'the UK, France, Italy, Germany and Spain', 'China, India, Japan, the USA and Russia'], 'They were the main Allied powers.'),
            ('How many countries signed the UN Charter in 1945?', '50 (51 with Poland, which signed later)', ['5', '193', '15'], 'It was signed in San Francisco on 26 June 1945.'),
            ('About how many people died in the Second World War?', 'About 70–85 million', ['About 7–8 million', 'About 700,000', 'About 700 million'], 'Most were civilians.'),
            ('Which 1944 conference created the IMF and World Bank?', 'Bretton Woods', ['Yalta', 'Potsdam', 'Versailles'], 'Held in New Hampshire, USA.'),
            ('Who was the first Secretary-General of the UN?', 'Trygve Lie of Norway', ['Kofi Annan', 'Dag Hammarskjöld', 'U Thant'], 'He served from 1946 to 1952.')],
     why=[('Explain why the United Nations was designed to be stronger than the League of Nations.', 'It included the USA and USSR, the Security Council could authorise military action, and permanent members had a veto to keep great powers involved.'),
          ('Explain why the veto has limited the UN\'s effectiveness.', 'Permanent members can block action against themselves or their allies, so the Security Council is often paralysed on major conflicts.'),
          ('Explain why the Nuremberg Trials were significant.', 'They established that individuals, including leaders, could be held responsible for crimes against humanity, and that following orders was no defence.'),
          ('Explain why the war led to a bipolar world.', 'Europe\'s great powers were exhausted, while the USA and USSR emerged with huge armies and global influence, and their ideological rivalry divided the world.')],
     contrast=[('the League of Nations', 'the United Nations', 'The League lacked the USA and an enforcement mechanism; the UN has near-universal membership and a Security Council able to authorise force, but subject to vetoes.'),
               ('the General Assembly', 'the Security Council', 'The General Assembly includes all members, each with one vote, and makes recommendations; the Security Council has 15 members and can make binding decisions.')],
     misc=[('The UN has its own permanent army.', 'UN peacekeepers are contributed by member states for specific missions.'),
           ('The UN replaced the League immediately and was the same organisation.', 'The UN was a new organisation with a new Charter; the League formally dissolved in 1946.'),
           ('The war ended with a single peace treaty like Versailles.', 'There was no single treaty; Germany was occupied and divided, and peace treaties with other countries were signed separately.')],
     cases=[('the Nuremberg Trials', '22 leading Nazis were tried by an international tribunal; 12 were sentenced to death in October 1946.', 'international justice', 'the trials laid foundations for international criminal law and the later International Criminal Court.'),
            ('the Korean War and the UN', 'In 1950 the Security Council authorised military action to defend South Korea while the USSR was boycotting the Council.', 'the UN in a bipolar world', 'collective action was possible only because one superpower was absent.')],
     evaluate=[('The United Nations has been more successful than the League of Nations.', ['near-universal membership and survival for over 75 years', 'peacekeeping, humanitarian agencies and human rights law'], ['the veto has prevented action in conflicts such as Syria and Ukraine', 'it has failed to prevent genocides such as Rwanda (1994)'], 'The UN has been more durable and effective in many fields than the League, but its security role remains limited by great-power politics.')],
     src=[('Charter (paraphrased)', 'The founding document states that the peoples of the United Nations are determined to save future generations from the scourge of war, which twice in their lifetime had brought untold sorrow, and to reaffirm faith in fundamental human rights and the equal rights of nations large and small.', 'Paraphrase of the Preamble to the Charter of the United Nations, San Francisco, 26 June 1945', 'to set out the purposes of the new organisation and win support for it', 'It shows the aims and values agreed by the founding states.', 'It states ideals; it does not show how far states lived up to them, and it was shaped by the victorious powers.', 'The UN aimed to prevent war and promote human rights and equality.')],
     rq=[('How effective was the United Nations in resolving the Suez Crisis of 1956?', 'What is the UN?', 'it is a definition question', 'It evaluates the UN\'s role in a specific crisis.', 'Use UN resolutions, newspaper reports and two historians; assess the first UN peacekeeping force (UNEF); evaluate sources; cite in MLA.')])
series('ch03-st4', [('UN member states', 'members', 1945, 51, 2011, 193, 'United Nations'), ('UN member states', 'members', 1945, 51, 1965, 117, 'United Nations')], d=(1, 3))

# =============================================================================================
# ch04 The Cold War
# =============================================================================================
CW_EVENTS = [('the Yalta Conference', 1945), ('the Potsdam Conference', 1945), ('Churchill\'s "iron curtain" speech at Fulton', 1946),
             ('the Truman Doctrine is announced', 1947), ('the Berlin Blockade begins', 1948), ('NATO is founded', 1949), ('the USSR tests its first atomic bomb', 1949),
             ('the Korean War begins', 1950), ('the Warsaw Pact is formed', 1955), ('Sputnik 1 is launched', 1957), ('the Berlin Wall is built', 1961),
             ('the Cuban Missile Crisis', 1962), ('the Partial Test Ban Treaty', 1963), ('Apollo 11 lands on the Moon', 1969), ('the SALT I agreements', 1972),
             ('the Soviet invasion of Afghanistan', 1979), ('Gorbachev becomes Soviet leader', 1985), ('the INF Treaty', 1987), ('the Berlin Wall falls', 1989), ('the USSR is dissolved', 1991)]

K.st('ch04-st1', 'the origins of the Cold War: capitalism versus communism, Yalta, Potsdam and the iron curtain',
     terms=[('Cold War', 'the state of tension and rivalry between the USA and the USSR and their allies from about 1945 to 1991, without direct full-scale war between them'),
            ('iron curtain', 'Churchill\'s 1946 phrase for the division between Soviet-controlled Eastern Europe and the West'),
            ('satellite state', 'a country formally independent but under the control of another, such as Poland under Soviet influence'),
            ('Truman Doctrine', 'the 1947 US policy of supporting free peoples resisting subjugation, the start of containment'),
            ('Marshall Plan', 'the European Recovery Program (1948–52) in which the USA gave about US$ 13 billion to rebuild Western Europe'),
            ('containment', 'the US policy of preventing the spread of communism'),
            ('orthodox, revisionist and post-revisionist interpretations', 'historians\' views blaming the USSR, the USA, or both/mutual misunderstanding for the Cold War')],
     facts=[('Which three leaders met at Yalta in February 1945?', 'Roosevelt, Churchill and Stalin', ['Truman, Attlee and Stalin', 'Hitler, Mussolini and Tojo', 'Kennedy, Khrushchev and Castro'], 'They planned the post-war order.'),
            ('Who replaced Roosevelt as US president before the Potsdam Conference?', 'Harry S. Truman', ['Dwight Eisenhower', 'John F. Kennedy', 'Herbert Hoover'], 'Roosevelt died in April 1945.'),
            ('Where did Churchill make his "iron curtain" speech in March 1946?', 'Fulton, Missouri', ['London', 'Moscow', 'Berlin'], 'Truman was present.'),
            ('What was Comecon, set up by the USSR in 1949?', 'An organisation for economic cooperation among communist states', ['A military alliance', 'A spy agency', 'A space programme'], 'A response to the Marshall Plan.'),
            ('Which US diplomat\'s "Long Telegram" of 1946 shaped the policy of containment?', 'George Kennan', ['Henry Kissinger', 'John Foster Dulles', 'Dean Acheson'], 'He argued Soviet expansion must be contained.')],
     why=[('Explain why the wartime alliance between the USA and USSR broke down after 1945.', 'With the common enemy defeated, ideological differences, disagreements over Germany and Poland, mutual suspicion and the US atomic monopoly turned allies into rivals.'),
          ('Explain why Stalin wanted control of Eastern Europe.', 'The USSR had been invaded through Eastern Europe twice and lost about 27 million people in the war, so Stalin wanted a buffer zone of friendly communist states.'),
          ('Explain why the Marshall Plan increased Cold War tensions.', 'The USSR saw it as "dollar imperialism" to extend US influence; it forbade Eastern European states from accepting aid, deepening the division of Europe.'),
          ('Explain why Germany became the centre of Cold War rivalry.', 'Both sides wanted to control Germany\'s future and industrial power; disagreements over reparations, currency and government led to its division in 1949.')],
     contrast=[('capitalism', 'communism', 'Capitalism is based on private ownership, markets and individual freedom; communism (Soviet-style) on state ownership, central planning and one-party rule.'),
               ('the Yalta Conference', 'the Potsdam Conference', 'Yalta (February 1945) was relatively cooperative, agreeing on zones in Germany and free elections in Eastern Europe; Potsdam (July–August 1945) was tenser, with new leaders Truman and Attlee and disputes over Poland and reparations.')],
     misc=[('The Cold War began with a single event in 1945.', 'It developed gradually from 1945 to 1949 through a series of disputes and actions on both sides.'),
           ('The Cold War never involved real fighting.', 'The superpowers did not fight each other directly, but proxy wars in Korea, Vietnam, Afghanistan and elsewhere killed millions.'),
           ('Historians agree that the USSR caused the Cold War.', 'Orthodox historians blamed Soviet expansion, revisionists blamed US economic imperialism, and post-revisionists stress mutual misunderstanding.')],
     cases=[('the Berlin Blockade and Airlift', 'From June 1948 to May 1949 the USSR blocked land access to West Berlin; the Western Allies flew in about 2.3 million tonnes of supplies.', 'early confrontation', 'it showed the West\'s commitment to West Berlin and led to the founding of NATO.'),
            ('the communist takeover in Czechoslovakia', 'In February 1948 the Communist Party seized full power; Foreign Minister Jan Masaryk died in suspicious circumstances weeks later.', 'Sovietisation of Eastern Europe', 'it convinced Western leaders that Stalin aimed to spread communism.')],
     evaluate=[('The USSR was mainly responsible for the start of the Cold War.', ['Stalin imposed communist governments in Eastern Europe, breaking Yalta promises', 'the Berlin Blockade was an aggressive act'], ['the USA used its economic and atomic power to extend influence', 'mutual fears and misunderstandings drove both sides'], 'Post-revisionist historians such as John Lewis Gaddis argue that both sides contributed, though Stalin\'s actions and suspicion were particularly important.')],
     src=[('Speech (paraphrased)', 'The former British prime minister told an American audience that an iron curtain had descended across Europe from Stettin in the Baltic to Trieste in the Adriatic, and that the ancient capitals behind it were increasingly under Moscow\'s control. He called for close cooperation between Britain and the USA.', 'Paraphrase of Winston Churchill, "Sinews of Peace" speech, Westminster College, Fulton, Missouri, 5 March 1946', 'to warn of Soviet expansion and urge an Anglo-American alliance', 'It is an influential statement of Western fears by a leading statesman.', 'Churchill was no longer prime minister and spoke to persuade a US audience; Stalin condemned it as a call to war.', 'Soviet control was dividing Europe, so Britain and the USA must stand together.')],
     rq=[('How far did the Marshall Plan contribute to the division of Europe between 1947 and 1949?', 'Who started the Cold War?', 'it is a closed, oversimplified question', 'It examines one factor\'s role in a process, allowing evaluation of interpretations.', 'Use Marshall Plan data, Soviet responses (Molotov) and two historians; compare interpretations; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch04-st1', events=CW_EVENTS[:8])


K.st('ch04-st2', 'containment and crises: Berlin, Korea and the Cuban Missile Crisis',
     terms=[('proxy war', 'a conflict in which superpowers support opposing sides rather than fighting each other directly'),
            ('brinkmanship', 'pushing a dangerous situation to the edge of war to force the other side to back down'),
            ('domino theory', 'the US belief that if one country fell to communism, its neighbours would follow'),
            ('38th parallel', 'the line of latitude dividing North and South Korea after 1945'),
            ('quarantine', 'the US naval blockade of Cuba during the 1962 missile crisis'),
            ('hotline', 'the direct communication link between Washington and Moscow set up in 1963')],
     facts=[('When was the Berlin Wall built?', 'August 1961', ['June 1948', 'October 1962', 'November 1989'], 'It stopped the flight of East Germans to the West.'),
            ('Which country invaded South Korea in June 1950?', 'North Korea', ['China', 'the USSR', 'Japan'], 'UN forces led by the USA intervened.'),
            ('For how many days did the Cuban Missile Crisis last?', '13 days', ['3 days', '30 days', '13 months'], 'From 16 to 28 October 1962.'),
            ('Which agreement ended fighting in Korea in July 1953?', 'An armistice signed at Panmunjom', ['the Treaty of Versailles', 'the Helsinki Accords', 'a full peace treaty'], 'No peace treaty has been signed.'),
            ('In return for the removal of Soviet missiles from Cuba, the USA secretly agreed to remove its missiles from which country?', 'Turkey', ['Italy', 'West Germany', 'Japan'], 'The Jupiter missiles were withdrawn in 1963.')],
     why=[('Explain why the USA intervened in Korea in 1950.', 'Following containment and the domino theory, the USA feared that a communist victory in Korea would threaten Japan and Asia; the UN Security Council approved action while the USSR was absent.'),
          ('Explain why the Berlin Wall was built.', 'About 3 million East Germans had fled to the West through Berlin since 1949, damaging the East German economy and image; the wall stopped the exodus.'),
          ('Explain why the USSR placed missiles in Cuba.', 'Khrushchev wanted to protect Castro\'s Cuba after the Bay of Pigs, reduce the US lead in missiles near the USSR (Turkey) and gain bargaining power, for example over Berlin.'),
          ('Explain why the Cuban Missile Crisis led to improved relations.', 'Both leaders realised how close they had come to nuclear war, so they set up the hotline in 1963 and signed the Partial Test Ban Treaty.')],
     contrast=[('the Berlin Blockade', 'the building of the Berlin Wall', 'The Blockade (1948–49) tried to force the West out of Berlin; the Wall (1961) accepted the West\'s presence but sealed East Berliners in.'),
               ('containment', 'rollback', 'Containment aimed to stop the spread of communism; rollback aimed to push communism back, as attempted when UN forces advanced into North Korea in 1950.')],
     misc=[('The Korean War ended with a US victory.', 'It ended in a stalemate near the 38th parallel in 1953, with about 3 million deaths.'),
           ('Kennedy forced Khrushchev to back down without any concessions.', 'The USA pledged not to invade Cuba and secretly agreed to remove missiles from Turkey.'),
           ('The Berlin Wall divided East and West Germany along their whole border.', 'The Wall surrounded West Berlin; the inner German border was a separate fortified frontier.')],
     cases=[('the Cuban Missile Crisis', 'In October 1962 US spy planes found Soviet missile sites in Cuba; Kennedy ordered a naval quarantine, and after tense negotiations Khrushchev agreed to remove the missiles.', 'brinkmanship and crisis management', 'the superpowers came close to nuclear war and then moved towards arms control.'),
            ('the Korean War', 'After North Korea invaded in 1950, UN forces pushed north towards China; Chinese troops intervened, and the war ended in stalemate in 1953.', 'containment through proxy war', 'containment worked in preserving South Korea but at great human cost.')],
     evaluate=[('Containment was a successful policy for the USA between 1947 and 1962.', ['it preserved West Berlin, Western Europe and South Korea', 'Soviet missiles were removed from Cuba'], ['the USA failed to stop communist victories in China (1949) and Cuba (1959)', 'Korea ended in stalemate with huge loss of life'], 'Containment largely succeeded in Europe, but its record in Asia and Latin America was mixed and costly.')],
     src=[('Speech (paraphrased)', 'The US president told the nation that unmistakable evidence showed offensive missile sites were being built in Cuba. He announced a strict quarantine on all offensive military equipment shipped to Cuba and called on the Soviet leader to remove the threat.', 'Paraphrase of John F. Kennedy, televised address to the American people, 22 October 1962', 'to inform the public, justify US action and pressure the USSR', 'It shows the official US position and the president\'s public strategy.', 'It presents only the US perspective and does not mention US missiles in Turkey or secret negotiations.', 'Soviet missiles in Cuba were a threat, so the USA would blockade Cuba and demand their removal.')],
     rq=[('How significant was the secret agreement on the Turkish missiles in resolving the Cuban Missile Crisis?', 'What happened in Cuba?', 'it is a descriptive question', 'It uses declassified evidence to evaluate a turning point.', 'Use the ExComm tapes, Khrushchev\'s letters and two historians; compare public and secret accounts; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch04-st2', events=CW_EVENTS[4:13])


@R.add('ch04-st2', ('C3', 'C4'), (1, 5), 'numerical')
def berlin(rng, slot):
    rows = [('flights during the Berlin Airlift', 'flights', 277_000, 'June 1948 to September 1949', 15), ('tonnes of supplies flown into West Berlin', 'tonnes', 2_326_000, 'June 1948 to September 1949', 15),
            ('East Germans who fled to the West', 'people', 2_700_000, '1949 to August 1961', 12)]
    what, unit, tot, per, months_or_years = rng.choice(rows)
    if unit == 'people':
        yrs = months_or_years
        v = tot / yrs
        return dict(stem=f'About {tot:,} {what} between {per} (about {yrs} years). Calculate the average number per year' + (' and per day.' if slot.d >= 3 else '.'),
                    answer=f'about {v:,.0f} per year' + (f'; about {v / 365:,.0f} per day' if slot.d >= 3 else ''), type='numerical', marks=2 if slot.d < 3 else 3,
                    markingKey=f'{tot:,} ÷ {yrs} = {v:,.0f} per year (M1 A1)' + (f'; ÷ 365 = {v / 365:,.0f} per day (A1).' if slot.d >= 3 else '.'), gap='G3')
    m = months_or_years
    v = tot / m
    return dict(stem=f'About {tot:,} {what} were recorded from {per} (about {m} months). Calculate the average per month' + (' and per day (assume 30 days per month).' if slot.d >= 3 else '.'),
                answer=f'about {v:,.0f} per month' + (f'; about {v / 30:,.0f} per day' if slot.d >= 3 else ''), type='numerical', marks=2 if slot.d < 3 else 3,
                markingKey=f'{tot:,} ÷ {m} = {v:,.0f} per month (M1 A1)' + (f'; ÷ 30 = {v / 30:,.0f} per day (A1).' if slot.d >= 3 else '.'), gap='G3')


K.st('ch04-st3', 'the arms race, the space race and Cold War propaganda',
     terms=[('arms race', 'competition between the superpowers to build more and better weapons, especially nuclear weapons'),
            ('mutually assured destruction (MAD)', 'the idea that a nuclear war would destroy both sides, so neither would start one'),
            ('deterrence', 'preventing an attack by having the ability to retaliate with overwhelming force'),
            ('ICBM', 'an intercontinental ballistic missile, able to carry nuclear warheads between continents'),
            ('space race', 'the competition between the USA and USSR to achieve firsts in space exploration'),
            ('détente', 'the easing of Cold War tensions in the late 1960s and 1970s')],
     facts=[('In which year did the USSR test its first atomic bomb?', '1949', ['1945', '1957', '1962'], 'Ending the US monopoly.'),
            ('Which was the first artificial satellite, launched by the USSR in October 1957?', 'Sputnik 1', ['Apollo 11', 'Explorer 1', 'Vostok 1'], 'It shocked the USA.'),
            ('Who was the first human in space, in April 1961?', 'Yuri Gagarin', ['Neil Armstrong', 'John Glenn', 'Valentina Tereshkova'], 'Aboard Vostok 1.'),
            ('In which year did Apollo 11 land astronauts on the Moon?', '1969', ['1957', '1961', '1975'], 'Neil Armstrong and Buzz Aldrin walked on the Moon.'),
            ('Which 1963 treaty banned nuclear tests in the atmosphere, in space and under water?', 'The Partial Test Ban Treaty', ['the INF Treaty', 'SALT I', 'the NPT'], 'Signed by the USA, USSR and UK.')],
     why=[('Explain why Sputnik caused alarm in the United States.', 'It showed the USSR had rockets powerful enough to carry nuclear warheads to America and suggested Soviet technological superiority, leading to the "missile gap" fear and investment in science education and NASA.'),
          ('Explain why MAD may have helped prevent nuclear war.', 'Since both sides could destroy each other even after being attacked, neither could expect to win a nuclear war, which created a strong incentive to avoid direct conflict.'),
          ('Explain why both superpowers used propaganda.', 'They wanted to win support at home and abroad, show the superiority of their system and portray the other side as a threat.'),
          ('Explain why the space race was linked to the arms race.', 'The rockets used to launch satellites and astronauts were developed from missile technology, and space achievements demonstrated military and scientific power.')],
     contrast=[('the arms race', 'the space race', 'The arms race was competition in weapons for military power; the space race was competition in space exploration for prestige, though both used the same rocket technology.'),
               ('deterrence', 'disarmament', 'Deterrence keeps weapons to prevent attack; disarmament reduces or eliminates weapons.')],
     misc=[('The USA led the space race from the start.', 'The USSR achieved most early firsts – Sputnik (1957), the first animal and human in space (1957, 1961) and the first woman in space (1963).'),
           ('The arms race involved only the USA and USSR.', 'Britain (1952), France (1960) and China (1964) also developed nuclear weapons.'),
           ('Propaganda was used only by the Soviet Union.', 'Both sides used propaganda, including films, radio (e.g. Radio Free Europe), posters and sporting events.')],
     cases=[('the 1980 and 1984 Olympic boycotts', 'The USA and over 60 countries boycotted the 1980 Moscow Olympics after the Soviet invasion of Afghanistan; the USSR and allies boycotted the 1984 Los Angeles Games.', 'sport as propaganda', 'the Olympics became a stage for Cold War rivalry.'),
            ('the Apollo 11 Moon landing', 'On 20 July 1969 the USA landed astronauts on the Moon; an estimated 600 million people watched on television.', 'the space race', 'the USA achieved a symbolic victory and showed its technological power.')],
     evaluate=[('The nuclear arms race made the world safer during the Cold War.', ['MAD deterred direct war between the superpowers', 'crises such as Cuba led to arms control'], ['the world came close to nuclear war in 1962 and 1983', 'enormous resources were diverted and tests harmed people and environments'], 'Deterrence may have prevented a direct superpower war, but the arms race created serious risks of catastrophe; "safer" is debatable.')],
     src=[('Poster (described)', 'A Soviet poster from 1961 shows a smiling cosmonaut in a helmet with the letters of the USSR, a rocket rising behind him, and a slogan celebrating the glory of the Soviet people who opened the way to space.', 'Soviet propaganda poster celebrating Yuri Gagarin\'s flight, published by the state publisher, Moscow, 1961', 'to celebrate the achievement and promote pride in the Soviet system', 'It shows how the USSR used space success to promote communism.', 'It is state propaganda that hides failures and costs of the space programme.', 'The Soviet people and system led humanity into space.')],
     rq=[('How did the launch of Sputnik in 1957 influence US education and science policy?', 'Who won the space race?', 'it is a closed question', 'It investigates the wider consequences of Cold War competition.', 'Use the National Defense Education Act, NASA records, newspapers and two historians; evaluate sources; cite in MLA.')])


@R.add('ch04-st3', ('C3', 'C4'), (1, 5), 'numerical')
def warheads(rng, slot):
    rows = [(1950, 299, 5), (1960, 18_638, 1_605), (1970, 26_008, 11_643), (1980, 23_764, 30_062), (1986, 23_317, 40_159), (1990, 21_004, 37_000)]
    a, b = sorted(rng.sample(rows, 2))
    who = rng.choice(['USA', 'USSR'])
    va, vb = (a[1], b[1]) if who == 'USA' else (a[2], b[2])
    if va == 0:
        return None
    pc = (vb - va) / va * 100
    if slot.d <= 3:
        return dict(stem=f'Estimated nuclear warhead stockpiles ({who}): {a[0]} – {va:,}; {b[0]} – {vb:,} (Federation of American Scientists estimates). Calculate the percentage change.',
                    answer=f'{pc:+,.0f}%', type='numerical', marks=2, markingKey=f'({vb:,} − {va:,}) ÷ {va:,} × 100 = {pc:+,.0f}% (M1 A1).', gap='G3')
    tot_a, tot_b = a[1] + a[2], b[1] + b[2]
    return dict(stem=(f'Estimated stockpiles: {a[0]} – USA {a[1]:,}, USSR {a[2]:,}; {b[0]} – USA {b[1]:,}, USSR {b[2]:,}. Calculate the combined total for each year and the percentage change, '
                      'and explain what the figures suggest about the arms race and détente.'),
                answer=f'{tot_a:,} → {tot_b:,} ({(tot_b - tot_a) / tot_a * 100:+,.0f}%)', type='multi_step', marks=6,
                markingKey=f'Totals {tot_a:,} and {tot_b:,} (A1 A1); change ({tot_b:,} − {tot_a:,}) ÷ {tot_a:,} × 100 = {(tot_b - tot_a) / tot_a * 100:+,.0f}% (M1 A1). '
                           'Analysis (2): rapid growth shows the arms race; the USSR overtook the USA in the late 1970s; arms-control agreements (SALT) limited launchers rather than warheads, so stockpiles grew even during détente until the late 1980s.', gap='G5')


K.st('ch04-st4', 'the end of the Cold War and the fall of the Berlin Wall',
     terms=[('glasnost', 'Gorbachev\'s policy of "openness", allowing more freedom of expression and criticism'),
            ('perestroika', 'Gorbachev\'s policy of "restructuring" the Soviet economy and political system'),
            ('Solidarity', 'the independent Polish trade union founded in 1980 and led by Lech Wałęsa'),
            ('Velvet Revolution', 'the peaceful overthrow of communist rule in Czechoslovakia in November–December 1989'),
            ('Sinatra Doctrine', 'the Soviet policy under Gorbachev of letting Eastern European states choose their own path'),
            ('INF Treaty', 'the 1987 US–Soviet treaty eliminating intermediate-range nuclear missiles')],
     facts=[('On what date did the Berlin Wall open?', '9 November 1989', ['13 August 1961', '3 October 1990', '25 December 1991'], 'Crowds crossed after a confused announcement.'),
            ('When was Germany reunified?', '3 October 1990', ['9 November 1989', '1 January 1992', '8 May 1945'], 'East Germany joined the Federal Republic.'),
            ('When was the Soviet Union formally dissolved?', 'December 1991', ['November 1989', 'August 1968', 'March 1985'], 'Gorbachev resigned on 25 December.'),
            ('Which Polish trade union, founded in 1980, challenged communist rule?', 'Solidarity', ['Comecon', 'Charter 77', 'the Stasi'], 'It won partly free elections in June 1989.'),
            ('Which country first opened its border with Austria in 1989, allowing East Germans to escape?', 'Hungary', ['Poland', 'Romania', 'Bulgaria'], 'It began removing border fences in May 1989.')],
     why=[('Explain why the Soviet economy contributed to the end of the Cold War.', 'Central planning was inefficient, growth stagnated, and huge military spending, the war in Afghanistan and low oil prices drained resources, making reform urgent.'),
          ('Explain why Gorbachev\'s reforms helped bring down communism in Eastern Europe.', 'Glasnost allowed criticism, and his refusal to use Soviet troops to prop up communist regimes meant popular movements could succeed peacefully.'),
          ('Explain why the fall of the Berlin Wall was symbolically important.', 'The Wall had been the main symbol of the division of Europe and the Cold War; its opening showed that communist control was collapsing.'),
          ('Explain why Ronald Reagan\'s policies are debated as a cause of the end of the Cold War.', 'Some argue his arms build-up and SDI pressured the USSR; others argue Gorbachev\'s reforms and internal Soviet problems were decisive, and that Reagan\'s later willingness to negotiate mattered more.')],
     contrast=[('glasnost', 'perestroika', 'Glasnost was political openness and freedom of expression; perestroika was economic and political restructuring.'),
               ('the revolutions of 1989 in Poland and Hungary', 'the revolution in Romania', 'Poland and Hungary saw negotiated, peaceful transitions; Romania\'s revolution was violent and ended with the execution of Ceaușescu.')],
     misc=[('The USA defeated the USSR militarily to end the Cold War.', 'The Cold War ended without direct war, mainly through Soviet internal crisis, reform and popular movements in Eastern Europe.'),
           ('The fall of the Berlin Wall immediately ended the USSR.', 'The Wall fell in 1989; the USSR survived until December 1991.'),
           ('Gorbachev intended to end communism.', 'He aimed to reform and save Soviet socialism, but his reforms unleashed forces he could not control.')],
     cases=[('the Baltic Way', 'On 23 August 1989 about 2 million people formed a human chain about 675 km long across Estonia, Latvia and Lithuania to demand independence.', 'peaceful popular protest', 'non-violent mass action challenged Soviet rule.'),
            ('the Polish Round Table talks', 'In early 1989 the government negotiated with Solidarity; in the June elections Solidarity won almost all contested seats.', 'negotiated transition', 'it began the peaceful end of communist rule in Eastern Europe.')],
     evaluate=[('Gorbachev was the most important reason for the end of the Cold War.', ['his reforms and refusal to use force allowed peaceful change', 'he negotiated arms reductions such as the INF Treaty'], ['the Soviet economy was already in deep crisis', 'popular movements such as Solidarity and US pressure also mattered'], 'Gorbachev was the key individual, but his choices were shaped by economic crisis and popular pressure; the end of the Cold War had several interacting causes.')],
     src=[('Speech (paraphrased)', 'The Soviet leader told the United Nations that force and the threat of force could no longer be instruments of foreign policy, and that every nation must have freedom of choice. He announced a unilateral reduction of Soviet armed forces by 500,000 troops.', 'Paraphrase of Mikhail Gorbachev, address to the UN General Assembly, New York, 7 December 1988', 'to signal a new Soviet foreign policy to the world', 'It shows a major change in Soviet policy announced by its leader.', 'It is a public diplomatic statement; it does not show debates within the Soviet leadership.', 'The USSR would not use force and would let nations choose their own path.')],
     rq=[('How far did economic problems in the USSR in the 1980s cause the collapse of Soviet control in Eastern Europe in 1989?', 'Why did the Wall fall?', 'it is too narrow and descriptive', 'It weighs economic factors against others in a major historical change.', 'Use Soviet economic data, Gorbachev\'s speeches and two historians; compare causes; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch04-st4', events=CW_EVENTS[15:] + [('Solidarity is founded', 1980), ('the Velvet Revolution in Czechoslovakia', 1989), ('Germany is reunified', 1990)])

# =============================================================================================
# ch05 Decolonisation and Independence Movements
# =============================================================================================
K.st('ch05-st1', 'colonialism and the drive for independence after 1945 in Asia and Africa',
     terms=[('decolonisation', 'the process by which colonies gained independence from colonial powers, mainly between 1945 and 1975'),
            ('colonialism', 'the control of one territory and its people by a foreign power'),
            ('nationalism', 'a movement seeking self-government or independence for a nation'),
            ('wind of change', 'British Prime Minister Harold Macmillan\'s 1960 phrase for the spread of African nationalism'),
            ('Bandung Conference', 'the 1955 meeting in Indonesia of 29 Asian and African states opposing colonialism'),
            ('settler colony', 'a colony with a large population of European settlers, such as Kenya, Algeria or Rhodesia, where decolonisation was often violent')],
     facts=[('Which year is known as the "Year of Africa" because 17 African countries became independent?', '1960', ['1947', '1957', '1975'], 'Including Nigeria and many French colonies.'),
            ('Which country fought a war of independence against France from 1954 to 1962?', 'Algeria', ['Ghana', 'India', 'Kenya'], 'The war caused a political crisis in France.'),
            ('Which country gained independence from the Netherlands after a struggle from 1945 to 1949?', 'Indonesia', ['Vietnam', 'Malaysia', 'the Philippines'], 'Sukarno declared independence on 17 August 1945.'),
            ('At which battle in 1954 was France defeated in Vietnam?', 'Dien Bien Phu', ['Midway', 'Stalingrad', 'El Alamein'], 'It led to the Geneva Accords.'),
            ('About how many new members joined the UN between 1945 and 1975, mostly former colonies?', 'About 90', ['About 9', 'About 900', 'None'], 'Membership grew from 51 to 144.')],
     why=[('Explain why the Second World War weakened European empires.', 'Britain, France and the Netherlands were economically exhausted, Japan\'s victories in Asia destroyed the myth of European invincibility, and colonial soldiers and nationalists expected rewards for their war effort.'),
          ('Explain why the USA and USSR both put pressure on colonial powers.', 'The USA opposed formal empires and wanted open markets, while the USSR supported anti-colonial movements ideologically; both competed for influence in newly independent states.'),
          ('Explain why decolonisation was more violent in settler colonies.', 'European settlers had land and power to protect and resisted majority rule, so colonial governments fought nationalists, as in Kenya, Algeria and Rhodesia.'),
          ('Explain why the United Nations supported decolonisation.', 'Its Charter supported self-determination, and as new states joined they used the General Assembly, such as Resolution 1514 (1960), to demand an end to colonialism.')],
     contrast=[('negotiated independence', 'independence through armed struggle', 'Negotiated independence, as in Ghana (1957), came through elections and talks; armed struggle, as in Algeria (1954–62), involved long wars against the colonial power.'),
               ('formal empire', 'neo-colonialism', 'Formal empire is direct political control; neo-colonialism is continuing economic or political influence over formally independent states.')],
     misc=[('Colonial powers granted independence freely and willingly.', 'Most independence came after nationalist pressure, protest, war or economic and international pressure.'),
           ('Decolonisation happened at the same time and in the same way everywhere.', 'It ranged from 1946 (Philippines) to 1975 (Portuguese colonies) and beyond, through very different processes.'),
           ('Independence ended all foreign influence.', 'Many new states remained economically dependent on former colonial powers and were drawn into Cold War rivalries.')],
     cases=[('the Algerian War of Independence', 'The FLN fought French rule from 1954; the war killed hundreds of thousands and brought de Gaulle to power in 1958; Algeria became independent in 1962.', 'violent decolonisation', 'a settler colony resisted independence, leading to a long and brutal war.'),
            ('Indonesia\'s independence', 'Sukarno and Hatta declared independence in 1945; after Dutch military campaigns and UN and US pressure, the Netherlands transferred sovereignty in 1949.', 'international pressure and nationalism', 'armed resistance plus international pressure ended Dutch rule.')],
     evaluate=[('The Second World War was the main cause of decolonisation.', ['it exhausted the colonial powers and destroyed their prestige', 'it raised colonial expectations and boosted nationalism'], ['nationalist movements such as the Indian National Congress predated the war', 'Cold War pressures and the UN accelerated the process'], 'The war was a crucial catalyst, but decolonisation resulted from long-term nationalism combined with post-war international pressures.')],
     src=[('Speech (paraphrased)', 'The British prime minister told the South African parliament that a wind of change was blowing through the continent, and that the growth of national consciousness in Africa was a political fact that policies must take into account.', 'Paraphrase of Harold Macmillan, speech to the Parliament of South Africa, Cape Town, 3 February 1960', 'to signal British acceptance of African independence and distance Britain from apartheid', 'It shows a shift in British policy towards decolonisation.', 'It is a diplomatic speech that presents Britain\'s retreat as a principled choice rather than a response to pressure.', 'African nationalism was unstoppable and Britain would accept it.')],
     rq=[('How far did international pressure, rather than armed struggle, secure Indonesian independence between 1945 and 1949?', 'Why did empires end?', 'it is far too broad', 'It weighs causes in one case of decolonisation.', 'Use UN resolutions, Dutch and Indonesian sources and two historians; compare factors; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch05-st1', events=[('the Philippines becomes independent', 1946), ('Indonesia gains recognised independence', 1949), ('the French defeat at Dien Bien Phu', 1954),
                                     ('the Bandung Conference', 1955), ('Ghana becomes independent', 1957), ('the "Year of Africa"', 1960), ('Algeria becomes independent', 1962),
                                     ('Kenya becomes independent', 1963), ('Mozambique and Angola become independent', 1975), ('Zimbabwe becomes independent', 1980)])
series('ch05-st1', [('UN member states', 'members', 1945, 51, 1975, 144, 'United Nations'), ('UN member states', 'members', 1955, 76, 1965, 117, 'United Nations')], d=(1, 3))


K.st('ch05-st2', 'Indian independence and the Partition of 1947',
     terms=[('Quit India Movement', 'the mass campaign launched by the Indian National Congress in August 1942 demanding immediate British withdrawal'),
            ('Cabinet Mission', 'the 1946 British mission that proposed a federal, united India; it failed'),
            ('two-nation theory', 'the argument, associated with the Muslim League, that Hindus and Muslims were separate nations'),
            ('Direct Action Day', '16 August 1946, called by the Muslim League; it led to large-scale communal violence in Calcutta'),
            ('Mountbatten Plan', 'the June 1947 plan for partition and the transfer of power, brought forward to August 1947'),
            ('princely states', 'about 560 states ruled by Indian princes under British paramountcy, which had to accede to India or Pakistan')],
     facts=[('Who was the last Viceroy of British India?', 'Lord Mountbatten', ['Lord Curzon', 'Lord Irwin', 'Lord Wavell'], 'He arrived in March 1947.'),
            ('Who led the All-India Muslim League in the 1940s?', 'Muhammad Ali Jinnah', ['Jawaharlal Nehru', 'Maulana Azad', 'Sardar Patel'], 'He became Pakistan\'s first Governor-General.'),
            ('When did India and Pakistan become independent?', '14–15 August 1947', ['26 January 1950', '15 August 1950', '30 January 1948'], 'Pakistan marks 14 August and India 15 August.'),
            ('Which minister oversaw the integration of the princely states into India?', 'Sardar Vallabhbhai Patel', ['B. R. Ambedkar', 'Rajendra Prasad', 'Subhas Chandra Bose'], 'With V. P. Menon.'),
            ('Which British party, elected in 1945, was committed to Indian independence?', 'Labour, under Clement Attlee', ['the Conservatives under Churchill', 'the Liberals', 'the Communists'], 'Attlee announced in February 1947 that Britain would leave by June 1948.')],
     why=[('Explain why Britain decided to leave India quickly after 1945.', 'Britain was economically exhausted, the Labour government supported independence, the Indian Army and civil service were less reliable after events such as the 1946 naval mutiny, and the cost of holding India was rising.'),
          ('Explain why the Cabinet Mission Plan failed.', 'Congress and the Muslim League disagreed about the powers of the centre and the provinces, mutual distrust deepened, and the League withdrew its acceptance and called for Direct Action.'),
          ('Explain why Partition was accepted by Congress leaders in 1947.', 'After the violence of 1946–47 and the failure of interim government, many leaders believed partition was the only way to achieve a quick transfer of power and avoid civil war.'),
          ('Explain why the integration of princely states was a major challenge.', 'Hundreds of rulers had to be persuaded to accede; some, such as Hyderabad, Junagadh and Kashmir, resisted or were contested, leading to police action and conflict.')],
     contrast=[('the Indian National Congress', 'the All-India Muslim League', 'Congress claimed to represent all Indians and wanted a united India; the Muslim League under Jinnah came to demand a separate Muslim state, Pakistan.'),
               ('independence', 'Partition', 'Independence was the end of British rule; Partition was the division of British India into two states, which caused mass migration and violence.')],
     misc=[('Gandhi supported Partition.', 'Gandhi strongly opposed Partition and spent August 1947 working to stop violence in Calcutta.'),
           ('Partition created only two countries, India and Pakistan, with no further change.', 'Pakistan had two wings; East Pakistan became Bangladesh in 1971.'),
           ('British rule ended because of a single campaign.', 'Independence resulted from decades of nationalist activity, the impact of the Second World War and Britain\'s post-war weakness.')],
     cases=[('Hyderabad\'s integration', 'The Nizam of Hyderabad sought independence; in September 1948 the Indian Army carried out "Operation Polo", and the state acceded.', 'integrating princely states', 'it shows the challenges and use of force in creating the new Indian state.'),
            ('the Quit India Movement', 'Launched in August 1942, it led to the arrest of Congress leaders and widespread protests suppressed by British forces.', 'mass mobilisation', 'it showed that British rule depended on force and lacked consent.')],
     evaluate=[('The British government was mainly responsible for the Partition of India.', ['divide-and-rule policies such as separate electorates deepened divisions', 'the hurried timetable left little time to plan'], ['the Muslim League\'s demand for Pakistan and Congress\'s choices also shaped the outcome', 'communal violence in 1946–47 made a united India harder to achieve'], 'Responsibility was shared: British policy and haste mattered, but so did the decisions and failures of Indian political leaders.')],
     src=[('Speech (paraphrased)', 'At midnight on 14–15 August 1947 the new prime minister told the Constituent Assembly that India had long ago made a "tryst with destiny" and was now awakening to life and freedom. He spoke of the tasks of ending poverty, ignorance and disease and inequality of opportunity.', 'Paraphrase of Jawaharlal Nehru, speech to the Constituent Assembly, New Delhi, 14 August 1947', 'to mark independence and set out the new nation\'s goals', 'It records the vision of India\'s first prime minister at independence.', 'It is a ceremonial speech and does not address the violence of Partition then taking place.', 'India was beginning a new era of freedom with great tasks ahead.')],
     rq=[('How far did the 1946 Cabinet Mission\'s failure make Partition inevitable?', 'Why was India partitioned?', 'it is too broad and invites description', 'It evaluates a turning point in the transfer of power.', 'Use Cabinet Mission documents, Congress and League statements and two historians; compare perspectives; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch05-st2', events=[('the Indian National Congress is founded', 1885), ('the All-India Muslim League is founded', 1906), ('the Salt March', 1930),
                                     ('the Lahore Resolution', 1940), ('the Quit India Movement', 1942), ('the Cabinet Mission', 1946), ('independence and Partition', 1947),
                                     ('Gandhi is assassinated', 1948), ('Bangladesh becomes independent', 1971)])


K.st('ch05-st3', 'independence in Africa: Ghana, Kenya and the end of apartheid',
     terms=[('apartheid', 'the system of legalised racial segregation and discrimination in South Africa from 1948 to the early 1990s'),
            ('Mau Mau', 'the armed rebellion against British colonial rule in Kenya in the 1950s, mainly among the Kikuyu'),
            ('Pan-Africanism', 'the movement for the unity and solidarity of African peoples'),
            ('ANC', 'the African National Congress, founded in 1912, which led the struggle against apartheid'),
            ('Sharpeville massacre', 'the killing of 69 people by South African police at an anti-pass-law protest on 21 March 1960'),
            ('Truth and Reconciliation Commission', 'the South African body (1996–2003) that heard testimony on apartheid-era human rights violations')],
     facts=[('Which country became the first sub-Saharan African colony to gain independence from Britain, in 1957?', 'Ghana', ['Kenya', 'Nigeria', 'South Africa'], 'Formerly the Gold Coast.'),
            ('Who led Ghana to independence?', 'Kwame Nkrumah', ['Jomo Kenyatta', 'Nelson Mandela', 'Julius Nyerere'], 'His Convention People\'s Party won elections in 1951, 1954 and 1956.'),
            ('In which year did Kenya become independent?', '1963', ['1957', '1960', '1994'], 'Jomo Kenyatta became its leader.'),
            ('In which year was Nelson Mandela released from prison?', '1990', ['1964', '1976', '1994'], 'After 27 years.'),
            ('When did South Africa hold its first elections with universal suffrage?', 'April 1994', ['1948', '1961', '1990'], 'Mandela became president.')],
     why=[('Explain why Ghana achieved independence relatively peacefully.', 'It had few European settlers, a well-organised mass party under Nkrumah that used strikes and elections, and Britain was willing to transfer power to an elected government.'),
          ('Explain why Kenya\'s path to independence was violent.', 'White settlers held the best land in the highlands; land grievances fuelled the Mau Mau rebellion, which Britain suppressed with detention camps and force.'),
          ('Explain why apartheid ended in the early 1990s.', 'Internal resistance, international sanctions and isolation, economic problems, the end of the Cold War and the leadership of F. W. de Klerk and Nelson Mandela led to negotiations.'),
          ('Explain why the Sharpeville massacre was a turning point.', 'It brought international condemnation, led the government to ban the ANC and PAC, and pushed the ANC towards armed struggle.')],
     contrast=[('Ghana\'s path to independence', 'Kenya\'s path to independence', 'Ghana gained independence peacefully through mass politics and elections; Kenya\'s involved the violent Mau Mau rebellion and harsh British repression.'),
               ('segregation', 'apartheid', 'Segregation is the separation of groups; apartheid was a comprehensive legal system of segregation and white minority rule in South Africa.')],
     misc=[('Apartheid ended when Mandela was released.', 'Mandela\'s release (1990) began negotiations; apartheid laws were repealed in 1990–91 and majority rule came with the 1994 election.'),
           ('The Mau Mau rebellion mainly killed European settlers.', 'Fewer than 40 European civilians were killed; most deaths were of Kenyan Africans, including over 11,000 rebels by official figures.'),
           ('South Africa was a European colony until 1994.', 'South Africa was self-governing from 1910 and a republic from 1961; the struggle was against white minority rule, not a colonial power.')],
     cases=[('the Soweto Uprising', 'On 16 June 1976 students protested against compulsory Afrikaans teaching; police killed many, including 13-year-old Hector Pieterson.', 'resistance to apartheid', 'it brought a new generation into the struggle and drew world attention.'),
            ('the Hola Camp killings', 'In March 1959 guards beat 11 detainees to death at the Hola detention camp in Kenya.', 'colonial repression', 'the scandal increased pressure in Britain to end colonial rule in Kenya.')],
     evaluate=[('International pressure was the main reason apartheid ended.', ['sanctions and divestment damaged the economy', 'sporting and cultural boycotts isolated South Africa'], ['internal resistance by the ANC, unions and township movements made the country ungovernable', 'the end of the Cold War removed the "communist threat" argument'], 'International pressure was important, but internal resistance and political change inside South Africa were decisive.')],
     src=[('Speech (paraphrased)', 'At his trial the accused told the court that he had fought against white domination and against black domination, and that he cherished the ideal of a democratic and free society in which all persons live together in harmony with equal opportunities. He said it was an ideal for which he was prepared to die.', 'Paraphrase of Nelson Mandela, statement from the dock at the Rivonia Trial, Pretoria, 20 April 1964', 'to explain his actions and state the ANC\'s aims to the court and the world', 'It shows the values and motives of the ANC\'s leader.', 'It is a statement by the accused intended to justify his actions, not a neutral account.', 'Mandela fought for a democratic, non-racial society.')],
     rq=[('How significant were international sanctions in ending apartheid in South Africa between 1985 and 1994?', 'What was apartheid?', 'it is a definition question', 'It weighs international against internal factors.', 'Use UN resolutions, trade data, ANC statements and two historians; compare factors; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch05-st3', events=[('the ANC is founded', 1912), ('the National Party begins apartheid', 1948), ('the Mau Mau emergency is declared in Kenya', 1952),
                                     ('Ghana becomes independent', 1957), ('the Sharpeville massacre', 1960), ('Kenya becomes independent', 1963),
                                     ('Mandela is sentenced at the Rivonia Trial', 1964), ('the Soweto Uprising', 1976), ('Mandela is released', 1990), ('South Africa\'s first democratic election', 1994)])


K.st('ch05-st4', 'the legacies of colonialism: borders, economies and the Non-Aligned Movement',
     terms=[('Non-Aligned Movement', 'a group of states, founded in Belgrade in 1961, that did not formally align with either Cold War bloc'),
            ('artificial border', 'a boundary drawn by colonial powers without regard to ethnic, linguistic or geographical realities'),
            ('Berlin Conference', 'the 1884–85 conference at which European powers set rules for dividing Africa'),
            ('primary commodity dependence', 'reliance on exporting raw materials such as cocoa, copper or oil'),
            ('neo-colonialism', 'continued economic and political influence of former colonial powers over independent states'),
            ('Organisation of African Unity (OAU)', 'founded in 1963, it accepted colonial borders to avoid conflict; replaced by the African Union in 2002')],
     facts=[('Which leaders were key founders of the Non-Aligned Movement?', 'Nehru, Nasser, Tito, Sukarno and Nkrumah', ['Truman, Churchill and Stalin', 'Reagan, Thatcher and Gorbachev', 'Mao, Kim Il-sung and Ho Chi Minh only'], 'The first summit was in Belgrade in 1961.'),
            ('Which 1884–85 conference set rules for the European "Scramble for Africa"?', 'The Berlin Conference', ['the Bandung Conference', 'the Yalta Conference', 'the Potsdam Conference'], 'No Africans were present.'),
            ('Which Ghanaian leader wrote "Neo-Colonialism: The Last Stage of Imperialism" in 1965?', 'Kwame Nkrumah', ['Jomo Kenyatta', 'Julius Nyerere', 'Patrice Lumumba'], 'He argued independence was incomplete.'),
            ('In 1964 the OAU agreed that African states should do what about colonial borders?', 'Respect them', ['Redraw them by referendum', 'Abolish them', 'Let the UN redraw them'], 'To avoid wars over territory.'),
            ('Which country depends on copper for most of its export earnings, a legacy of colonial mining?', 'Zambia', ['Japan', 'Switzerland', 'Bangladesh'], 'Copper is about 70% of its exports.')],
     why=[('Explain why colonial borders have caused problems for independent states.', 'They divided some ethnic groups and joined rivals together, contributing to conflicts and secession attempts such as Biafra and disputes over territory.'),
          ('Explain why many former colonies remained dependent on primary commodities.', 'Colonial economies were organised to export raw materials and import manufactured goods, with infrastructure linking mines and plantations to ports rather than building local industry.'),
          ('Explain why newly independent states joined the Non-Aligned Movement.', 'They wanted to protect their independence, avoid being drawn into superpower conflicts and gain aid and influence from both sides.'),
          ('Explain why the OAU chose to keep colonial borders.', 'Redrawing borders could have caused endless wars, so leaders accepted existing borders as the basis of stability.')],
     contrast=[('political independence', 'economic independence', 'Political independence is self-government; economic independence means control over the economy, which many states lacked because of debt, commodity dependence and foreign ownership.'),
               ('non-alignment', 'neutrality', 'Non-alignment meant not joining either bloc while remaining active in world affairs; neutrality is a legal status of not taking part in conflicts.')],
     misc=[('All problems in former colonies are caused by colonialism.', 'Colonial legacies matter, but post-independence governance, Cold War interference and global economics also shaped outcomes.'),
           ('Non-aligned states never took sides.', 'Several leaned towards one bloc, for example receiving Soviet or US aid and arms.'),
           ('Colonial borders followed natural or ethnic boundaries.', 'Many were straight lines drawn on maps, especially in Africa.')],
     cases=[('the Nigerian Civil War (Biafra)', 'In 1967 the south-eastern region declared independence as Biafra; the war lasted until 1970 and up to a million or more people died, many from famine.', 'colonial borders and ethnic tension', 'a state created from different regions faced secession and conflict.'),
            ('the Belgrade Conference of 1961', 'Leaders from 25 countries met to found the Non-Aligned Movement, calling for peace and an end to colonialism.', 'non-alignment', 'new states sought a collective voice outside the Cold War blocs.')],
     evaluate=[('Colonial borders are the main reason for conflict in post-colonial Africa.', ['borders divided peoples and grouped rivals together', 'they led to wars such as Biafra and disputes in the Horn of Africa'], ['many conflicts stem from governance, resources and Cold War interference', 'most African states have kept their borders without inter-state war'], 'Borders contributed to some conflicts, but political, economic and external factors are usually more important.')],
     src=[('Book (paraphrased)', 'The author argued that a state in the grip of neo-colonialism is not master of its own destiny: although it has the outward signs of sovereignty, its economic system and political policy are directed from outside, often through foreign investment and aid.', 'Paraphrase of Kwame Nkrumah, Neo-Colonialism: The Last Stage of Imperialism, London, 1965', 'to warn African states about continuing foreign economic control', 'It is a leading African statesman\'s analysis of post-colonial dependence.', 'It is a political argument written during Cold War tensions and may underplay domestic causes of problems.', 'Former colonies remained controlled economically from outside.')],
     rq=[('How far has dependence on copper exports affected Zambia\'s economic development since 1964?', 'Was colonialism bad?', 'it is a vague value question', 'It investigates a specific economic legacy with data.', 'Use World Bank export data, copper price series and two studies; graph trends; evaluate sources; cite in APA.')])
series('ch05-st4', [('the world copper price', 'US$ per tonne', 2002, 1560, 2011, 8820, 'approx., World Bank'), ('the world cocoa price', 'US$ per tonne', 1977, 3800, 1992, 1100, 'approx., ICCO')], d=(1, 4))

# =============================================================================================
# ch06 Human Rights and Civil Rights Movements
# =============================================================================================
K.st('ch06-st1', 'human rights: the Universal Declaration of Human Rights and international law',
     terms=[('human rights', 'rights that belong to every person because they are human, regardless of nationality, sex, ethnicity, religion or any other status'),
            ('Universal Declaration of Human Rights (UDHR)', 'the document adopted by the UN General Assembly on 10 December 1948 setting out 30 articles of fundamental rights'),
            ('civil and political rights', 'rights such as freedom of speech, a fair trial and the right to vote'),
            ('economic, social and cultural rights', 'rights such as education, health, work and an adequate standard of living'),
            ('International Criminal Court (ICC)', 'the court in The Hague, established by the Rome Statute in 2002, that tries individuals for genocide, war crimes and crimes against humanity'),
            ('universality', 'the principle that human rights apply to everyone everywhere')],
     facts=[('On what date was the UDHR adopted?', '10 December 1948', ['24 October 1945', '26 June 1945', '1 January 1950'], '10 December is Human Rights Day.'),
            ('Who chaired the UN commission that drafted the UDHR?', 'Eleanor Roosevelt', ['Winston Churchill', 'Mahatma Gandhi', 'Dag Hammarskjöld'], 'René Cassin, P. C. Chang, Charles Malik and Hansa Mehta also contributed.'),
            ('Which Indian delegate helped change "all men are born free and equal" to "all human beings"?', 'Hansa Mehta', ['Indira Gandhi', 'Sarojini Naidu', 'Vijaya Lakshmi Pandit'], 'Article 1 now refers to all human beings.'),
            ('How many articles does the UDHR contain?', '30', ['10', '14', '100'], 'They cover civil, political, economic, social and cultural rights.'),
            ('Which two 1966 treaties, with the UDHR, make up the International Bill of Human Rights?', 'The ICCPR and the ICESCR', ['the NPT and the CTBT', 'the Paris Agreement and Kyoto Protocol', 'the Geneva and Hague Conventions'], 'They entered into force in 1976.')],
     why=[('Explain why the UDHR was adopted in 1948.', 'After the Holocaust and the war, states wanted a common standard of rights to prevent such atrocities and to show that how a state treats its people is a matter of international concern.'),
          ('Explain why the UDHR is not legally binding but still important.', 'It is a declaration, not a treaty, but it has inspired binding treaties, national constitutions and courts, and many of its principles are regarded as customary international law.'),
          ('Explain why human rights are difficult to enforce internationally.', 'States guard their sovereignty, the UN has limited enforcement powers, the Security Council veto blocks action, and some powerful states do not accept the ICC\'s jurisdiction.'),
          ('Explain why there is debate about the universality of human rights.', 'Some argue the UDHR reflects Western values; others point out that it was drafted by people from many cultures and that rights are claimed by people everywhere.')],
     contrast=[('civil and political rights', 'economic, social and cultural rights', 'Civil and political rights protect freedoms from state interference, such as free speech; economic, social and cultural rights require states to provide, such as education and health.'),
               ('a declaration', 'a treaty', 'A declaration sets out principles but is not legally binding; a treaty binds the states that ratify it.')],
     misc=[('The UDHR is a binding international treaty.', 'It is a General Assembly resolution, not a treaty; binding obligations come from later covenants and conventions.'),
           ('Human rights only concern freedom from torture and imprisonment.', 'They also include rights to education, health, work, social security and cultural life.'),
           ('All UN members voted for the UDHR in 1948.', '48 states voted in favour, none against, and 8 abstained, including the USSR bloc, South Africa and Saudi Arabia.')],
     cases=[('the International Criminal Tribunal for Rwanda', 'Set up by the UN in 1994, it convicted individuals of genocide, including the first conviction for genocide by an international court (Akayesu, 1998).', 'international criminal law', 'it showed that individuals could be held responsible for genocide.'),
            ('the European Court of Human Rights', 'Created under the 1950 European Convention on Human Rights, it hears cases against member states of the Council of Europe.', 'regional human rights enforcement', 'individuals can take their own governments to an international court.')],
     evaluate=[('The Universal Declaration of Human Rights has been effective in protecting human rights.', ['it set a global standard and inspired constitutions and treaties', 'it underpins courts, NGOs and campaigns worldwide'], ['it is not binding and is widely violated', 'enforcement depends on states and is weakened by power politics'], 'The UDHR has been highly influential in shaping law and norms, but its effectiveness depends on enforcement, which remains uneven.')],
     src=[('Speech (paraphrased)', 'The chair of the drafting commission told the General Assembly that the Declaration was not a treaty or international agreement and was not a statement of law or legal obligation, but a declaration of basic principles to serve as a common standard of achievement for all nations. She hoped it might become an international Magna Carta for all people everywhere.', 'Paraphrase of Eleanor Roosevelt, address to the UN General Assembly, Paris, 9 December 1948', 'to explain the nature and importance of the Declaration before the vote', 'It is a first-hand account of the drafters\' intentions.', 'It reflects the US and Western perspective of the time and the hopes, not the effects, of the Declaration.', 'The UDHR was a non-binding common standard that could become a global charter of rights.')],
     rq=[('How far has the International Criminal Court been effective in prosecuting crimes against humanity since 2002?', 'What are human rights?', 'it is a definition question', 'It evaluates an institution of international law using its record.', 'Use ICC case data, NGO reports and two academic analyses; consider state cooperation; evaluate sources; cite in APA.')])


K.st('ch06-st2', 'the US civil rights movement: Martin Luther King, Malcolm X and non-violent protest',
     terms=[('segregation', 'the legal or social separation of people by race, as under the Jim Crow laws in the US South'),
            ('Jim Crow laws', 'state and local laws in the southern USA enforcing racial segregation from the late 19th century to the 1960s'),
            ('civil disobedience', 'deliberately and peacefully breaking unjust laws to protest'),
            ('Black Power', 'a movement of the 1960s emphasising Black pride, self-reliance and self-defence'),
            ('NAACP', 'the National Association for the Advancement of Colored People, founded 1909, which used legal challenges'),
            ('Freedom Rides', 'the 1961 bus journeys by Black and white activists to challenge segregation in interstate travel')],
     facts=[('Which 1954 Supreme Court decision ruled segregated public schools unconstitutional?', 'Brown v. Board of Education', ['Plessy v. Ferguson', 'Roe v. Wade', 'Marbury v. Madison'], 'It overturned "separate but equal" in education.'),
            ('Whose arrest in December 1955 began the Montgomery Bus Boycott?', 'Rosa Parks', ['Coretta Scott King', 'Ella Baker', 'Fannie Lou Hamer'], 'The boycott lasted 381 days.'),
            ('In which year did Martin Luther King Jr give his "I Have a Dream" speech?', '1963', ['1955', '1965', '1968'], 'At the March on Washington, 28 August 1963.'),
            ('Which 1965 law outlawed literacy tests and other barriers to Black voting?', 'The Voting Rights Act', ['the Civil Rights Act of 1964', 'the 19th Amendment', 'the Fair Housing Act'], 'Black voter registration in the South rose sharply.'),
            ('In which year was Malcolm X assassinated?', '1965', ['1963', '1968', '1955'], 'He was killed in New York in February 1965.')],
     why=[('Explain why non-violent protest was effective for the civil rights movement.', 'It exposed the violence of segregationists on television, won sympathy across the USA and abroad, and pressured the federal government to act, as at Birmingham and Selma.'),
          ('Explain why Malcolm X criticised the strategy of non-violence.', 'He argued that Black Americans had the right to defend themselves, that integration into a racist society was not enough, and that Black pride and independence were needed.'),
          ('Explain why the federal government became more involved in civil rights in the 1960s.', 'Media coverage of violence, mass protests, Cold War concerns about the USA\'s image, and pressure from activists pushed Presidents Kennedy and Johnson to support legislation.'),
          ('Explain why the civil rights movement continued after the laws of 1964 and 1965.', 'Laws ended legal segregation but not economic inequality, housing discrimination or police violence, especially in northern cities.')],
     contrast=[('Martin Luther King Jr', 'Malcolm X', 'King advocated non-violent civil disobedience and integration; Malcolm X (before 1964) advocated Black nationalism, self-defence and separation, later moving towards broader cooperation.'),
               ('de jure segregation', 'de facto segregation', 'De jure segregation is enforced by law, as in the South; de facto segregation exists in practice through housing and economic patterns, as in many northern cities.')],
     misc=[('The civil rights movement was led only by Martin Luther King.', 'It was a mass movement involving many leaders and organisations, including the NAACP, SNCC, CORE, Ella Baker, Fannie Lou Hamer and thousands of ordinary people.'),
           ('Rosa Parks was simply a tired woman who refused to move.', 'She was an experienced NAACP activist, and her protest was part of an organised campaign.'),
           ('The Civil Rights Act of 1964 ended racial inequality in the USA.', 'It outlawed discrimination in public places and employment, but economic and social inequalities persisted.')],
     cases=[('the Birmingham campaign (1963)', 'Police used dogs and fire hoses on young protesters; images shocked the nation and pushed Kennedy to propose a civil rights bill.', 'non-violent direct action', 'deliberate campaigns exposed violence and won public support.'),
            ('the Selma to Montgomery marches (1965)', 'On "Bloody Sunday", 7 March 1965, state troopers attacked marchers on the Edmund Pettus Bridge; the Voting Rights Act followed in August.', 'protest leading to legislation', 'public outrage over violence led directly to federal law.')],
     evaluate=[('Non-violent protest was the most important factor in the success of the civil rights movement.', ['campaigns like Birmingham and Selma led directly to the 1964 and 1965 Acts', 'non-violence won national and international sympathy'], ['NAACP legal victories such as Brown v. Board were crucial', 'presidential leadership and the threat of unrest also mattered'], 'Non-violent protest was central to the legislative breakthroughs, but it worked with legal challenges, federal action and the wider political context.')],
     src=[('Letter (paraphrased)', 'Writing from prison, the minister replied to white clergymen who had called his protests unwise and untimely. He argued that people have a moral responsibility to disobey unjust laws, that waiting had almost always meant "never", and that injustice anywhere is a threat to justice everywhere.', 'Paraphrase of Martin Luther King Jr, "Letter from Birmingham Jail", 16 April 1963', 'to justify non-violent direct action and answer critics', 'It is a powerful statement of the movement\'s philosophy by its leading figure.', 'It is a persuasive argument written to answer critics and win support, not a neutral account of events.', 'Non-violent civil disobedience against unjust laws was morally necessary and urgent.')],
     rq=[('How far did television coverage of the Birmingham campaign influence the passing of the Civil Rights Act of 1964?', 'Who was Martin Luther King?', 'it is a biographical question', 'It investigates the role of the media in political change.', 'Use news footage descriptions, opinion polls, Kennedy\'s speeches and two historians; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch06-st2', events=[('the Plessy v. Ferguson ruling', 1896), ('the NAACP is founded', 1909), ('Brown v. Board of Education', 1954), ('the Montgomery Bus Boycott begins', 1955),
                                     ('the Little Rock Nine', 1957), ('the Freedom Rides', 1961), ('the March on Washington', 1963), ('the Civil Rights Act', 1964),
                                     ('the Voting Rights Act', 1965), ('Martin Luther King is assassinated', 1968)])


@R.add('ch06-st2', ('C3', 'C4'), (1, 5), 'numerical')
def black_voters(rng, slot):
    rows = [('Mississippi', 6.7, 59.8), ('Alabama', 19.3, 51.6), ('Georgia', 27.4, 52.6), ('Louisiana', 31.6, 58.9), ('South Carolina', 37.3, 51.2)]
    st, a, b = rng.choice(rows)
    ch = b - a
    if slot.d <= 3:
        return dict(stem=f'The percentage of voting-age Black residents registered to vote in {st} rose from about {a}% (1964/65) to {b}% (1967) (US Commission on Civil Rights). Calculate the increase in percentage points.',
                    answer=f'{ch:.1f} percentage points', type='numerical', marks=2, markingKey=f'{b} − {a} = {ch:.1f} percentage points (M1 A1).', gap='G3')
    st2, a2, b2 = rng.choice([r for r in rows if r[0] != st])
    return dict(stem=(f'Black voter registration (% of voting-age Black residents) before and after the Voting Rights Act: {st} {a}% → {b}%; {st2} {a2}% → {b2}% (US Commission on Civil Rights). '
                      'Calculate the percentage-point change for each state, identify which changed more, and explain the impact of the Voting Rights Act.'),
                answer=f'{st}: +{ch:.1f}; {st2}: +{b2 - a2:.1f}; larger: {st if ch > b2 - a2 else st2}', type='multi_step', marks=5,
                markingKey=f'{st} +{ch:.1f} (A1); {st2} +{b2 - a2:.1f} (A1); comparison (A1). Explanation (2): the Act banned literacy tests and sent federal examiners to register voters, '
                           'especially where registration had been lowest; but local intimidation persisted.', gap='G5')


K.st('ch06-st3', 'struggles for equality: women\'s rights, caste and Dalit movements, and Indigenous rights',
     terms=[('feminism', 'the belief in and movement for the social, political and economic equality of the sexes'),
            ('gender pay gap', 'the difference between the average earnings of men and women'),
            ('Dalit', 'the self-chosen name of communities formerly treated as "untouchable" under the caste system'),
            ('reservation', 'in India, quotas in education, jobs and legislatures for Scheduled Castes, Scheduled Tribes and other disadvantaged groups'),
            ('Indigenous peoples', 'the descendants of the original inhabitants of a land, with distinct cultures, such as the Māori, Sámi or Adivasi'),
            ('UNDRIP', 'the UN Declaration on the Rights of Indigenous Peoples, adopted in 2007'),
            ('CEDAW', 'the 1979 UN Convention on the Elimination of All Forms of Discrimination against Women')],
     facts=[('Which 1979 UN convention is often described as an international bill of rights for women?', 'CEDAW', ['the UDHR', 'UNDRIP', 'the Rome Statute'], 'It has been ratified by 189 states.'),
            ('Which Dalit leader launched the Mahad Satyagraha in 1927 to assert the right to use a public water tank?', 'B. R. Ambedkar', ['Jyotirao Phule', 'Mahatma Gandhi', 'Periyar'], 'It challenged caste exclusion.'),
            ('Which 1967 Australian referendum allowed Aboriginal people to be counted in the census and gave the Commonwealth power to make laws for them?', 'The 1967 referendum, approved by about 91% of voters', ['the 1901 Federation referendum', 'the 1999 republic referendum', 'the 2023 Voice referendum'], 'It is often misremembered as giving Aboriginal people the vote.'),
            ('Which Australian High Court case of 1992 recognised native title to land?', 'Mabo v Queensland (No 2)', ['Brown v Board', 'Roe v Wade', 'Waitangi v Crown'], 'It rejected the doctrine of terra nullius.'),
            ('In which year was UNDRIP adopted by the UN General Assembly?', '2007', ['1948', '1966', '1993'], 'Four states initially voted against, later endorsing it.')],
     why=[('Explain why legal equality has not ended discrimination against Dalits in India.', 'Although untouchability was abolished in 1950, social prejudice, economic inequality, violence and unequal access to land and education continue, and laws are not always enforced.'),
          ('Explain why the gender pay gap persists.', 'Occupational segregation, unpaid care work falling mainly on women, discrimination and fewer women in senior roles all reduce women\'s average earnings.'),
          ('Explain why land rights are central to Indigenous rights movements.', 'Land is tied to Indigenous identity, culture and livelihoods; colonisation dispossessed many communities, so restoring land rights addresses historic injustice and supports self-determination.'),
          ('Explain why international conventions such as CEDAW matter.', 'They set common standards, require states to report on progress and give activists a tool to pressure governments to change laws.')],
     contrast=[('formal equality', 'substantive equality', 'Formal equality treats everyone the same in law; substantive equality takes account of disadvantage, for example through reservations or affirmative action, to achieve equal outcomes.'),
               ('the Dalit movement', 'the women\'s movement', 'The Dalit movement challenges caste-based discrimination; the women\'s movement challenges gender discrimination – both seek equality, and Dalit women face both forms.')],
     misc=[('The 1967 Australian referendum gave Aboriginal people the right to vote.', 'Aboriginal people gained the federal vote in 1962; the referendum concerned the census and Commonwealth law-making power.'),
           ('Caste discrimination ended when the Indian Constitution came into force.', 'The Constitution abolished untouchability, but caste-based discrimination and violence continue.'),
           ('Women\'s rights movements began only in the 1960s.', 'They date back at least to the 19th century, including suffrage campaigns and earlier writers such as Mary Wollstonecraft (1792).')],
     cases=[('the Mabo decision', 'In 1992 the High Court of Australia recognised that the Meriam people held native title to the Murray Islands, overturning terra nullius.', 'Indigenous land rights', 'it changed Australian law to recognise prior Indigenous ownership.'),
            ('the Me Too movement', 'From 2017 the hashtag spread worldwide as women shared experiences of sexual harassment, leading to resignations and law reforms in several countries.', 'digital activism for women\'s rights', 'social media amplified voices and changed public debate.')],
     evaluate=[('Legal change is the most effective way to achieve equality.', ['laws such as the Indian Constitution and CEDAW establish rights and remedies', 'courts have enforced change, as in Mabo'], ['social attitudes and economic inequality persist despite laws', 'enforcement is often weak'], 'Legal change is necessary but not sufficient; lasting equality also requires social change, economic opportunity and enforcement.')],
     src=[('Book (paraphrased)', 'The author argued that caste was not just a division of labour but a division of labourers into graded, unequal groups, and that it could not be reformed from within; he called for its annihilation through the rejection of the religious ideas that sustained it.', 'Paraphrase of B. R. Ambedkar, Annihilation of Caste, Bombay, 1936', 'to challenge the caste system and its justifications; it was written as a speech that the organisers then cancelled', 'It is a foundational text of the Dalit movement by its leading thinker.', 'It is a polemical argument; it was contested by Gandhi and others who sought reform rather than abolition.', 'Caste is a system of graded inequality that must be abolished, not reformed.')],
     rq=[('How effective have reserved seats been in increasing the political representation of Scheduled Castes in India since 1952?', 'What is caste?', 'it is a definition question', 'It evaluates a policy aimed at substantive equality.', 'Use Election Commission data, two academic studies and Dalit activists\' writings; compare indicators; evaluate perspectives; cite in APA.')])
series('ch06-st3', [('the number of women MPs in the UK House of Commons', 'MPs', 1997, 120, 2024, 263, 'House of Commons Library'),
                    ('the number of women in India\'s Lok Sabha', 'MPs', 1952, 22, 2019, 78, 'Election Commission of India')], d=(1, 3))

# =============================================================================================
# ch07 Measuring Development and Inequality
# =============================================================================================
GDP_ROWS = [('the United States', 27_360, 335, 2023), ('India', 3_550, 1_429, 2023), ('China', 17_790, 1_410, 2023), ('Brazil', 2_170, 216, 2023),
            ('Nigeria', 363, 224, 2023), ('Germany', 4_460, 84.5, 2023), ('Japan', 4_210, 124.5, 2023), ('Bangladesh', 437, 173, 2023),
            ('Ethiopia', 163, 127, 2023), ('Norway', 485, 5.5, 2023), ('Kenya', 108, 55, 2023), ('Indonesia', 1_370, 278, 2023)]

K.st('ch07-st1', 'measuring development: GDP per capita, the HDI and other indicators',
     terms=[('development', 'improvement in people\'s quality of life, including income, health, education, freedom and opportunity'),
            ('GDP per capita', 'the total value of goods and services produced in a country in a year divided by its population'),
            ('purchasing power parity (PPP)', 'an adjustment of income figures to account for differences in the cost of living between countries'),
            ('Human Development Index (HDI)', 'the UNDP composite index combining life expectancy, education (expected and mean years of schooling) and GNI per capita (PPP)'),
            ('Gini coefficient', 'a measure of income inequality from 0 (perfect equality) to 1 or 100 (one person has all income)'),
            ('Multidimensional Poverty Index (MPI)', 'an index measuring poverty through deprivations in health, education and living standards'),
            ('composite indicator', 'a measure combining several indicators into a single figure')],
     facts=[('Which three dimensions are combined in the Human Development Index?', 'Health, education and standard of living', ['Wealth, military strength and trade', 'Population, area and climate', 'Happiness, religion and culture'], 'Measured by life expectancy, schooling and GNI per capita.'),
            ('Which economist, with Mahbub ul Haq, helped develop the HDI in 1990?', 'Amartya Sen', ['Milton Friedman', 'Adam Smith', 'Paul Krugman'], 'Based on the capabilities approach.'),
            ('Which country had the world\'s highest HDI in the 2023/24 report?', 'Switzerland', ['the United States', 'India', 'Brazil'], 'Norway and Iceland were close behind.'),
            ('A Gini coefficient of 0.63, as in South Africa, indicates what?', 'Very high income inequality', ['Perfect equality', 'Low inequality', 'High life expectancy'], 'South Africa is among the most unequal countries.'),
            ('Which indicator would best show access to health care?', 'Number of doctors per 1,000 people', ['GDP', 'Steel production', 'Number of cars exported'], 'Social indicators show quality of life.')],
     why=[('Explain why GDP per capita is a limited measure of development.', 'It is an average that hides inequality, ignores the informal and unpaid economy, says nothing about health, education, freedom or the environment, and is affected by exchange rates unless PPP is used.'),
          ('Explain why the HDI is considered a better measure of development than GDP per capita alone.', 'It combines income with health and education, reflecting the idea that development is about expanding people\'s capabilities, not just income.'),
          ('Explain why PPP adjustments are used to compare incomes.', 'Prices differ between countries, so a dollar buys more in India than in the USA; PPP shows what incomes can actually buy.'),
          ('Explain why two countries with similar GDP per capita can have very different HDI values.', 'Governments may spend differently on health and education, and inequality may differ, so life expectancy and schooling can vary even with similar average incomes.')],
     contrast=[('economic indicators', 'social indicators', 'Economic indicators measure income and production, such as GDP per capita; social indicators measure quality of life, such as life expectancy, literacy and infant mortality.'),
               ('GDP per capita', 'HDI', 'GDP per capita measures average economic output; HDI is a composite of health, education and income.')],
     misc=[('A high GDP per capita means everyone in a country is well off.', 'It is an average; high inequality, as in some oil-rich states, can leave many people poor.'),
           ('The HDI measures happiness.', 'It measures health, education and income; happiness is measured separately, for example in the World Happiness Report.'),
           ('Development is only about money.', 'Following Sen, development includes freedoms, health, education, political rights and environmental quality.')],
     cases=[('Kerala, India', 'Kerala has had much higher literacy and life expectancy than India\'s average despite a similar or modest income level, due to long-term public investment in health and education.', 'social development with moderate income', 'it shows that high human development is possible without very high GDP per capita.'),
            ('Equatorial Guinea', 'Oil made its GDP per capita one of the highest in Africa, yet much of the population remained poor, with low life expectancy.', 'GDP versus human development', 'high average income did not translate into broad development.')],
     evaluate=[('The HDI is the best measure of development.', ['it combines income with health and education', 'it is simple and comparable across countries'], ['it ignores inequality, freedom, gender and the environment', 'composite indices can hide important differences'], 'The HDI is more rounded than GDP per capita, but a range of indicators, including the inequality-adjusted HDI and MPI, gives a fuller picture.')],
     src=[('Book (paraphrased)', 'The author argued that development should be seen as a process of expanding the real freedoms that people enjoy, such as freedom from hunger, disease and illiteracy, and political freedom, rather than only as growth in income.', 'Paraphrase of Amartya Sen, Development as Freedom, Oxford, 1999', 'to propose a broader understanding of development', 'It is an influential work by a Nobel laureate that shaped the HDI.', 'It is a philosophical framework; freedoms are harder to measure than income.', 'Development means expanding people\'s freedoms and capabilities.')],
     rq=[('How far does Kerala\'s experience show that public spending on health and education can raise human development without high income?', 'Which country is the most developed?', 'it is a closed question', 'It tests a key idea in development theory with a real case.', 'Use NFHS and HDI data, state budget data and two studies; compare with other states; evaluate sources; cite in APA.')])
C.per_capita(K, 'ch07-st1', GDP_ROWS)
C.hdi(K, 'ch07-st1')


@R.add('ch07-st1', ('C3', 'C4'), (2, 5), 'numerical')
def quintile(rng, slot):
    rows = [('Brazil', 3.2, 57.7), ('South Africa', 2.4, 68.2), ('Norway', 9.0, 35.0), ('India', 8.1, 44.4), ('Japan', 7.5, 39.8), ('the United States', 5.2, 47.0),
            ('Ethiopia', 7.0, 41.7)]
    co, low, high = rng.choice(rows)
    r = high / low
    if slot.d <= 3:
        return dict(stem=f'In {co} the poorest 20% of the population receives about {low}% of national income and the richest 20% about {high}% (World Bank estimates). Calculate the ratio of the richest 20% to the poorest 20%.',
                    answer=f'about {r:.1f} : 1', type='numerical', marks=2, markingKey=f'{high} ÷ {low} = {r:.1f} (M1 A1).', gap='G3')
    c2, l2, h2 = rng.choice([x for x in rows if x[0] != co])
    r2 = h2 / l2
    return dict(stem=(f'Income shares (World Bank estimates): {co} – poorest 20% {low}%, richest 20% {high}%; {c2} – poorest 20% {l2}%, richest 20% {h2}%. '
                      'Calculate the 20:20 ratio for each country and explain why measures of inequality are needed alongside GDP per capita.'),
                answer=f'{co}: {r:.1f}; {c2}: {r2:.1f}', type='multi_step', marks=5,
                markingKey=f'{co} {r:.1f} (A1); {c2} {r2:.1f} (A1); comparison (A1). Explanation (2): averages hide how income is distributed; two countries with similar GDP per capita can have very different poverty levels.', gap='G5')


K.st('ch07-st2', 'global patterns of development: the Brandt line and the development gap',
     terms=[('Brandt line', 'the line on a 1980 map dividing the richer "North" from the poorer "South", from the Brandt Report'),
            ('development gap', 'the difference in levels of development between the richest and poorest countries'),
            ('Global North and Global South', 'terms for generally high-income countries and low- and middle-income countries'),
            ('newly industrialised country (NIC)', 'a country whose economy has rapidly shifted from agriculture to industry, such as South Korea or Malaysia'),
            ('World Bank income groups', 'the classification of countries as low, lower-middle, upper-middle or high income by GNI per capita'),
            ('emerging economy', 'a country experiencing rapid economic growth and industrialisation, such as India, Brazil or Indonesia')],
     facts=[('Who chaired the commission whose 1980 report introduced the North–South divide?', 'Willy Brandt', ['Gro Harlem Brundtland', 'Kofi Annan', 'Jawaharlal Nehru'], 'He was a former West German chancellor.'),
            ('Which country, south of the equator, was placed in the "North" on the Brandt line?', 'Australia (and New Zealand)', ['Brazil', 'Nigeria', 'India'], 'The line curves around them.'),
            ('Which East Asian country moved from low income in the 1960s to high income by the 1990s?', 'South Korea', ['Afghanistan', 'Haiti', 'Chad'], 'Through export-led industrialisation.'),
            ('Which World Bank group includes India as of 2024?', 'Lower-middle income', ['High income', 'Low income', 'Upper-middle income'], 'GNI per capita about US$ 2,500.'),
            ('Which region has the largest number of low-income countries?', 'Sub-Saharan Africa', ['Western Europe', 'North America', 'East Asia'], 'Most low-income countries are there.')],
     why=[('Explain why the Brandt line is now considered outdated.', 'Since 1980 countries such as China, South Korea, Singapore and parts of the Gulf have developed rapidly, so a simple North–South division no longer fits the complex pattern.'),
          ('Explain why the development gap has widened for some countries.', 'Conflict, debt, commodity dependence, weak governance and climate shocks have held back some low-income countries while others grew quickly.'),
          ('Explain why there are large development differences within countries.', 'Investment, jobs and services often concentrate in cities and core regions, while rural and peripheral areas lag behind, as between Maharashtra and Bihar in India.'),
          ('Explain why the World Bank uses income groups rather than a two-way split.', 'Development is a spectrum, and grouping countries into four categories gives a more accurate picture for policy and lending.')],
     contrast=[('the Brandt line', 'World Bank income groups', 'The Brandt line divides the world into two; World Bank groups classify countries into four income categories updated annually.'),
               ('the development gap between countries', 'the development gap within countries', 'Between countries it compares national averages; within countries it compares regions, cities and rural areas or social groups.')],
     misc=[('All countries in the Global South are poor.', 'The South includes rich economies such as Singapore and Qatar and large emerging economies such as China and Brazil.'),
           ('The development gap is getting wider for every country.', 'Many countries, especially in Asia, have narrowed the gap, while some in sub-Saharan Africa have fallen further behind.'),
           ('A country\'s place on the Brandt line never changes.', 'The line was a 1980 snapshot; countries have moved between income groups since.')],
     cases=[('South Korea', 'GDP per capita rose from under US$ 200 in 1960 to over US$ 33,000 by 2023 through export-led growth, education and state-guided industrial policy.', 'closing the development gap', 'it shows a country moving from "South" to high income within two generations.'),
            ('the Democratic Republic of the Congo', 'Despite huge mineral wealth, conflict and governance problems have kept GDP per capita among the world\'s lowest.', 'the persistent development gap', 'resources alone do not guarantee development.')],
     evaluate=[('The Brandt line is no longer useful for understanding global development.', ['NICs and emerging economies have blurred the divide', 'income groups and HDI give more nuance'], ['it still captures a broad historical and power divide in global institutions', 'many "South" countries share colonial histories and interests'], 'The Brandt line is too simple as a map of income today, but the idea of a Global South remains useful for understanding shared histories and political interests.')],
     src=[('Commission report (paraphrased)', 'The report argued that the North and the South had a mutual interest in reducing poverty and inequality: a more prosperous South would provide markets and stability for the North. It called for large transfers of resources, reform of international institutions and an end to protectionism.', 'Paraphrase of the Independent Commission on International Development Issues (chair Willy Brandt), North–South: A Programme for Survival, 1980', 'to persuade governments to act on global inequality', 'It is an influential international report with a clear analysis of global divides.', 'It reflects the economic thinking of 1980 and grouped very different countries together.', 'North and South share an interest in reducing global inequality.')],
     rq=[('How has the development gap between South Korea and Ghana changed since 1960, and why?', 'Why are some countries poor?', 'it is too broad', 'It compares two countries with similar starting points and different outcomes.', 'Use World Bank and Penn World Table data, two studies on policy; graph GDP per capita; evaluate explanations; cite in APA.')])
C.per_capita(K, 'ch07-st2', GDP_ROWS, c=('C3',), d=(1, 3))
series('ch07-st2', [('South Korea\'s GDP per capita', 'US$', 1960, 158, 2023, 33_100, 'World Bank'), ('China\'s GDP per capita', 'US$', 1990, 318, 2023, 12_600, 'World Bank'),
                    ('Ghana\'s GDP per capita', 'US$', 1960, 183, 2023, 2_260, 'World Bank')], d=(1, 4))


K.st('ch07-st3', 'the causes of uneven development: physical, historical, economic and political factors',
     terms=[('landlocked', 'having no coastline, which raises transport costs for trade'),
            ('resource curse', 'the paradox that countries rich in natural resources such as oil often have slower growth and weaker governance'),
            ('dependency theory', 'the theory that poorer countries remain underdeveloped because of exploitative economic relationships with richer countries'),
            ('Rostow\'s model', 'W. W. Rostow\'s 1960 model of five stages of economic growth, from traditional society to high mass consumption'),
            ('corruption', 'the abuse of public power for private gain'),
            ('debt crisis', 'when a country cannot repay its debts, as in Latin America and Africa in the 1980s')],
     facts=[('Which of these is a physical factor that can hinder development?', 'Being landlocked with frequent droughts', ['Corruption', 'Colonial history', 'Trade rules'], 'Physical factors include climate, relief and access to the sea.'),
            ('Which economist proposed five stages of economic growth in 1960?', 'W. W. Rostow', ['Andre Gunder Frank', 'Amartya Sen', 'Jeffrey Sachs'], 'His model is criticised as Western-centric.'),
            ('Which theorist argued that the "development of underdevelopment" resulted from dependence on core countries?', 'Andre Gunder Frank', ['W. W. Rostow', 'Adam Smith', 'Thomas Malthus'], 'A key dependency theorist.'),
            ('Which disease significantly reduces productivity in many tropical countries?', 'Malaria', ['Scurvy', 'Altitude sickness', 'Frostbite'], 'About 600,000 deaths a year, mostly in Africa.'),
            ('Which country is often cited as escaping the resource curse through good governance of diamond revenues?', 'Botswana', ['Nigeria', 'Venezuela', 'DR Congo'], 'It grew rapidly after independence.')],
     why=[('Explain why being landlocked can slow development.', 'Exports and imports must cross other countries, raising transport costs and delays and making trade dependent on neighbours\' infrastructure and politics.'),
          ('Explain why colonial history can explain uneven development.', 'Colonial economies were organised to export raw materials, infrastructure served ports, local industry was discouraged, and borders and institutions were imposed.'),
          ('Explain why conflict is a major cause of low development.', 'War destroys infrastructure, kills and displaces people, diverts spending to the military and discourages investment and trade.'),
          ('Explain why reliance on primary commodities can hinder development.', 'Commodity prices are volatile and often fall relative to manufactured goods, and raw materials add little value or employment.')],
     contrast=[('modernisation theory (Rostow)', 'dependency theory', 'Modernisation theory sees development as a series of stages all countries can pass through; dependency theory argues that global economic relations keep poorer countries dependent and underdeveloped.'),
               ('physical causes of uneven development', 'human causes', 'Physical causes include climate, disease, hazards and relief; human causes include history, trade, debt, governance and conflict.')],
     misc=[('Countries are poor because of their climate alone.', 'Climate matters, but history, institutions, trade and governance explain why countries with similar climates, such as Botswana and Zimbabwe, differ.'),
           ('Natural resources always make a country rich.', 'The resource curse shows that oil or minerals can encourage corruption, conflict and dependence.'),
           ('All countries must follow the same path to develop.', 'Countries have developed in different ways; Rostow\'s model is criticised for assuming one Western path.')],
     cases=[('Botswana\'s diamonds', 'After diamonds were discovered in 1967, Botswana used revenues for education, health and infrastructure, with low corruption; it became upper-middle income.', 'good governance and resources', 'institutions made the difference in avoiding the resource curse.'),
            ('Nigeria\'s oil', 'Oil has provided most export earnings since the 1970s, but corruption, conflict in the Niger Delta and neglect of agriculture have limited broad development.', 'the resource curse', 'resource wealth did not translate into widespread development.')],
     evaluate=[('Historical factors such as colonialism are the most important cause of uneven development today.', ['colonial economic structures and borders persist', 'dependency on commodity exports continues'], ['many former colonies such as South Korea and Singapore developed rapidly', 'governance, conflict and policy since independence matter greatly'], 'Colonial history shaped starting conditions, but post-independence choices, institutions and global economics explain much of today\'s variation.')],
     src=[('Book (paraphrased)', 'The authors argued that nations fail mainly because of "extractive" political and economic institutions that concentrate power and wealth in a narrow elite, while nations prosper when they have "inclusive" institutions that give broad groups a stake in the economy.', 'Paraphrase of Daron Acemoglu and James A. Robinson, Why Nations Fail, New York, 2012', 'to explain differences in national prosperity', 'It uses a wide range of historical cases and was influential (its authors shared the 2024 Nobel Prize in economics).', 'Critics argue it gives too little weight to geography and culture.', 'Inclusive institutions are the main cause of prosperity.')],
     rq=[('How far does governance explain the different development paths of Botswana and Zimbabwe since 1980?', 'Why is Africa poor?', 'it is a sweeping generalisation', 'It compares two neighbouring countries to test explanations.', 'Use World Bank data, corruption indices and two studies; compare factors; evaluate sources; cite in APA.')])
C.per_capita(K, 'ch07-st3', GDP_ROWS, c=('C4',), d=(4, 5))


K.st('ch07-st4', 'strategies to reduce inequality: aid, debt relief, microfinance and fair trade',
     terms=[('official development assistance (ODA)', 'government aid to promote development and welfare in low- and middle-income countries'),
            ('bilateral aid', 'aid given directly from one government to another'),
            ('multilateral aid', 'aid given through international organisations such as the World Bank or UN agencies'),
            ('tied aid', 'aid that must be spent on goods or services from the donor country'),
            ('debt relief', 'cancelling or reducing a country\'s debts, as under the HIPC Initiative from 1996'),
            ('microfinance', 'small loans, savings and insurance services for people without access to banks'),
            ('0.7% target', 'the UN target, agreed in 1970, for rich countries to give 0.7% of gross national income as aid')],
     facts=[('What share of gross national income did the UN ask rich countries to give in aid in 1970?', '0.7%', ['7%', '0.07%', '17%'], 'Only a few countries meet it.'),
            ('Which 2005 G8 summit agreed to cancel the debts of many of the poorest countries?', 'Gleneagles', ['Yalta', 'Bretton Woods', 'Kyoto'], 'It led to the Multilateral Debt Relief Initiative.'),
            ('Which 1996 initiative by the IMF and World Bank aimed to reduce the debts of the poorest countries?', 'The Heavily Indebted Poor Countries (HIPC) Initiative', ['the Marshall Plan', 'the Green Revolution', 'the Paris Agreement'], '37 countries have received relief.'),
            ('Which campaign of the late 1990s called for cancelling poor countries\' debts by 2000?', 'Jubilee 2000', ['Live Aid', 'Fridays for Future', 'Make Poverty History only'], 'It gathered about 24 million signatures.'),
            ('Which countries were among the few to exceed the 0.7% aid target in 2023?', 'Norway, Luxembourg, Sweden, Germany and Denmark', ['the USA and Japan', 'India and China', 'Brazil and Mexico'], 'OECD DAC data.')],
     why=[('Explain why tied aid may be less effective than untied aid.', 'Recipients must buy from the donor, often at higher prices and regardless of local needs, so the aid partly benefits donor companies.'),
          ('Explain why debt relief can help development.', 'Money spent on debt repayments can be redirected to health, education and infrastructure; Tanzania used savings to abolish primary school fees in 2001.'),
          ('Explain why bottom-up projects are often more sustainable than large top-down schemes.', 'They involve local communities, use appropriate technology and meet local needs, so people can maintain them.'),
          ('Explain why aid is controversial.', 'Supporters say it saves lives and builds services; critics argue it can create dependency, support corrupt governments and serve donor interests.')],
     contrast=[('top-down development', 'bottom-up development', 'Top-down projects are planned by governments or agencies, often large-scale like dams; bottom-up projects are led by local communities, often small-scale like wells.'),
               ('emergency aid', 'long-term development aid', 'Emergency aid responds to disasters with food, shelter and medicine; development aid funds long-term improvements in health, education and infrastructure.')],
     misc=[('Rich countries give most of their national income as aid.', 'Most give well under 1% of GNI; the average for OECD donors was about 0.37% in 2023.'),
           ('Debt relief simply gives money away with no conditions.', 'HIPC relief required countries to meet conditions such as poverty reduction strategies.'),
           ('Aid always reaches the poorest people.', 'Aid can be lost to corruption, administrative costs or spent on donor priorities.')],
     cases=[('Tanzania and debt relief', 'After HIPC debt relief, Tanzania abolished primary school fees in 2001; enrolment rose from about 59% to over 90% within a few years.', 'debt relief for development', 'freed resources were used for education.'),
            ('WaterAid in Ethiopia', 'WaterAid works with local partners to build hand-dug wells and train communities to maintain them.', 'bottom-up development', 'local involvement makes projects more sustainable.')],
     evaluate=[('Aid is the most effective strategy for reducing global inequality.', ['aid has funded vaccination campaigns that saved millions of lives', 'it supports health and education in the poorest countries'], ['trade, investment and remittances are much larger flows', 'aid can create dependency and be poorly targeted'], 'Aid is important for health and emergencies, but trade, investment, debt relief and good governance are more powerful long-term drivers of reducing inequality.')],
     src=[('Book (paraphrased)', 'The author argued that large aid flows to African governments had fostered dependency, encouraged corruption and slowed growth, and proposed phasing out aid over five years in favour of trade, investment and access to capital markets.', 'Paraphrase of Dambisa Moyo, Dead Aid: Why Aid Is Not Working and How There Is Another Way for Africa, London, 2009', 'to challenge the consensus in favour of aid', 'It is a provocative view from an African economist with financial experience.', 'Critics argue it focuses on government-to-government aid and ignores successes in health aid.', 'Aid has harmed African development and should be replaced by market-based finance.')],
     rq=[('How far did debt relief under the HIPC Initiative improve access to primary education in Tanzania between 2000 and 2010?', 'Does aid work?', 'it is too broad and closed', 'It evaluates a specific strategy with measurable outcomes.', 'Use UNESCO enrolment data, government budgets and two studies; compare before and after; evaluate sources; cite in APA.')])


@R.add('ch07-st4', ('C3', 'C4'), (1, 5), 'numerical')
def oda(rng, slot):
    rows = [('Norway', 520, 1.09), ('Sweden', 650, 0.91), ('Germany', 4_600, 0.79), ('the United Kingdom', 3_300, 0.58), ('Japan', 4_450, 0.44),
            ('the United States', 27_500, 0.24), ('France', 3_100, 0.48), ('Canada', 2_100, 0.38)]
    co, gni, r = rng.choice(rows)
    amt = gni * r / 100
    if slot.d <= 2:
        return dict(stem=f'{C.cap(co)} had a gross national income of about US$ {gni:,} billion and gave {r}% of GNI as aid in 2023 (approx., OECD). Calculate its aid in US$ billions.',
                    answer=f'about US$ {amt:.1f} billion', type='numerical', marks=2, markingKey=f'{r}% × {gni:,} = US$ {amt:.1f} bn (M1 A1).', gap='G3')
    tgt = gni * 0.7 / 100
    gap = tgt - amt
    return dict(stem=(f'{C.cap(co)}: GNI about US$ {gni:,} billion; aid {r}% of GNI (approx., OECD, 2023). Calculate its aid, the amount it would give at the UN 0.7% target, and the difference. '
                      + ('Evaluate whether meeting the target would be the best way for it to reduce global inequality.' if slot.d >= 4 else '')),
                answer=f'aid US$ {amt:.1f} bn; target US$ {tgt:.1f} bn; difference US$ {gap:+.1f} bn', type='multi_step', marks=4 if slot.d < 4 else 6,
                markingKey=f'Aid {r}% × {gni:,} = {amt:.1f} (A1); target 0.7% × {gni:,} = {tgt:.1f} (A1); difference {gap:+.1f} bn (A1; negative means it already exceeds the target).'
                           + (' Evaluation (3): quality and targeting of aid matter as much as quantity; trade rules, debt relief, tax justice and climate finance also matter.' if slot.d >= 4 else ''),
                gap='G5')

# =============================================================================================
# ch08 Globalisation, Trade and Interdependence
# =============================================================================================
K.st('ch08-st1', 'what globalisation is: its economic, cultural and political dimensions',
     terms=[('globalisation', 'the increasing interconnection of the world\'s economies, cultures and peoples through trade, investment, technology, migration and communication'),
            ('time–space compression', 'the feeling that the world is shrinking because faster transport and communication reduce the time it takes to connect places'),
            ('cultural globalisation', 'the spread of ideas, values, media, food and lifestyles around the world'),
            ('interdependence', 'the mutual reliance of countries on one another for goods, services, resources and security'),
            ('containerisation', 'the use of standard shipping containers from the 1950s, which greatly reduced the cost of transporting goods'),
            ('KOF Globalisation Index', 'an index measuring the economic, social and political dimensions of globalisation for each country')],
     facts=[('Who invented the modern intermodal shipping container, first used in 1956?', 'Malcolm McLean', ['Henry Ford', 'Steve Jobs', 'Thomas Edison'], 'It cut loading costs dramatically.'),
            ('Roughly what share of world GDP did trade (exports plus imports) represent in 2022?', 'About 60%', ['About 6%', 'About 100%', 'About 25%'], 'It was about 25% in 1970.'),
            ('Which event in 1991 began India\'s economic liberalisation?', 'A balance of payments crisis leading to reforms by Manmohan Singh', ['Independence', 'the Green Revolution', 'the 2008 financial crisis'], 'Tariffs and licences were reduced.'),
            ('Which Korean pop group was the first to top the US Billboard 200 album chart, in 2018?', 'BTS', ['ABBA', 'The Beatles', 'Coldplay'], 'An example of cultural globalisation from Asia.'),
            ('About how many people used the internet worldwide in 2024?', 'About 5.5 billion', ['About 550 million', 'About 55 million', 'About 8 billion'], 'ITU estimate, about two-thirds of the population.')],
     why=[('Explain why globalisation accelerated after the 1980s.', 'Containerisation and cheaper air transport, the internet, trade liberalisation, the end of the Cold War and China\'s and India\'s opening to world markets increased flows of goods, capital and information.'),
          ('Explain why globalisation can lead to cultural homogenisation.', 'Global brands, media and platforms spread similar products and values, which may weaken local languages and traditions.'),
          ('Explain why cultural globalisation is not only Westernisation.', 'Flows go in many directions: Bollywood, K-pop, Japanese anime, Nigerian Nollywood and global cuisines spread widely.'),
          ('Explain why political globalisation involves a loss of sovereignty.', 'Membership of organisations such as the WTO or EU, and international agreements, require states to follow shared rules, limiting independent decision-making.')],
     contrast=[('economic globalisation', 'cultural globalisation', 'Economic globalisation involves flows of goods, services, capital and labour; cultural globalisation involves flows of ideas, media, values and lifestyles.'),
               ('globalisation', 'glocalisation', 'Globalisation spreads products and ideas worldwide; glocalisation adapts global products to local tastes, such as McDonald\'s McAloo Tikki in India.')],
     misc=[('Globalisation is a new phenomenon of the 21st century.', 'Earlier waves include the Silk Roads, European empires and the 1870–1914 era of trade and migration.'),
           ('Globalisation affects all places equally.', 'Some places are highly connected (Singapore, London), while others remain on the margins.'),
           ('Globalisation always reduces cultural diversity.', 'It can also spread and revive cultures and create hybrid forms.')],
     cases=[('McDonald\'s in India', 'McDonald\'s opened in 1996 and adapted its menu, offering no beef and many vegetarian options such as the McAloo Tikki.', 'glocalisation', 'a global brand adapted to local cultural and religious practices.'),
            ('India\'s 1991 reforms', 'Facing a balance of payments crisis, India cut tariffs, removed many industrial licences and opened to foreign investment; growth accelerated in later decades.', 'economic globalisation', 'policy change integrated a large economy into global markets.')],
     evaluate=[('Globalisation is mainly an economic process.', ['trade, investment and supply chains are the most measurable dimensions', 'economic integration drives other changes'], ['cultural flows through media and migration are equally important', 'political cooperation and global governance shape globalisation'], 'Economic integration is central, but globalisation is multidimensional; cultural and political changes are both causes and consequences.')],
     src=[('Book (paraphrased)', 'The author argued that a combination of technological change and political events had "flattened" the world, allowing individuals and companies in places such as Bengaluru to compete and collaborate globally on equal terms with those in the West.', 'Paraphrase of Thomas L. Friedman, The World Is Flat, New York, 2005', 'to explain the effects of 21st-century globalisation for a general audience', 'It gives vivid examples of how technology connected new places.', 'Critics argue it exaggerates equality; much of the world remains unconnected or disadvantaged.', 'Technology has made the world a more level playing field.')],
     rq=[('How has the growth of the IT industry in Bengaluru since 1991 reflected economic globalisation?', 'What is globalisation?', 'it is a definition question', 'It applies the concept to a specific place and period.', 'Use NASSCOM and census data, company histories and two studies; map links; evaluate sources; cite in APA.')])
series('ch08-st1', [('world trade in goods and services', 'per cent of world GDP', 1970, 25, 2022, 63, 'World Bank'), ('global container port traffic', 'million TEU', 2000, 225, 2022, 866, 'approx., UNCTAD'),
                    ('internet users worldwide', 'billion', 2005, 1.0, 2024, 5.5, 'ITU')], d=(1, 4))


K.st('ch08-st2', 'multinational corporations and global supply chains',
     terms=[('multinational corporation (MNC)', 'a company with operations, such as factories, offices or stores, in more than one country'),
            ('foreign direct investment (FDI)', 'investment by a company in productive assets in another country'),
            ('global supply chain', 'the network of producers, suppliers and distributors in many countries involved in making and delivering a product'),
            ('outsourcing', 'contracting another company, often abroad, to carry out work previously done in-house'),
            ('offshoring', 'moving a company\'s own operations to another country'),
            ('just-in-time production', 'a system of receiving parts only when needed, reducing stock but increasing vulnerability to disruption')],
     facts=[('Which company manufactures most iPhones under contract, mainly in China?', 'Foxconn', ['Toyota', 'Nestlé', 'Unilever'], 'Taiwan-based Hon Hai Precision Industry.'),
            ('Which ship blocked the Suez Canal for six days in March 2021, disrupting global trade?', 'The Ever Given', ['the Titanic', 'the Exxon Valdez', 'the Windrush'], 'About 12% of world trade passes through Suez.'),
            ('Which Indian company, founded in 1981, became a major global IT MNC?', 'Infosys', ['Coca-Cola', 'Samsung', 'Shell'], 'Headquartered in Bengaluru.'),
            ('By revenue, which company was the world\'s largest in 2023 (Fortune Global 500)?', 'Walmart', ['Infosys', 'Ryanair', 'Tata Motors'], 'Revenue about US$ 611 billion.'),
            ('Which Taiwanese company makes most of the world\'s most advanced semiconductors?', 'TSMC', ['Intel', 'Apple', 'Huawei'], 'A key node in global supply chains.')],
     why=[('Explain why MNCs locate factories in countries such as Vietnam and Bangladesh.', 'Lower labour costs, government incentives, access to growing markets and trade agreements reduce costs and increase profits.'),
          ('Explain why global supply chains are vulnerable to disruption.', 'Production depends on many specialised suppliers in different countries and just-in-time delivery, so a single blockage, pandemic or conflict can halt production.'),
          ('Explain why host countries compete to attract MNCs.', 'MNCs bring jobs, investment, technology, skills and tax revenue, and link local firms to global markets.'),
          ('Explain why MNCs are criticised.', 'Some pay low wages, avoid tax by shifting profits, damage the environment and have great power over governments, and profits may leave the host country.')],
     contrast=[('the advantages of MNCs for host countries', 'the disadvantages', 'Advantages include jobs, investment and technology; disadvantages include low wages, profit repatriation, environmental damage and dependence.'),
               ('outsourcing', 'offshoring', 'Outsourcing contracts work to another firm; offshoring moves a company\'s own operations abroad – they often overlap.')],
     misc=[('MNCs only come from rich Western countries.', 'Many MNCs are from emerging economies, such as Tata (India), Huawei (China) and Embraer (Brazil).'),
           ('A product "made in China" is made entirely in China.', 'Most products assemble parts from many countries; the label shows only the final assembly location.'),
           ('MNCs always pay lower wages than local firms.', 'Studies often find MNCs pay more than local firms on average, though wages may still be low by global standards.')],
     cases=[('the Ever Given blockage', 'In March 2021 a container ship ran aground in the Suez Canal, holding up an estimated US$ 9.6 billion of trade a day.', 'supply chain vulnerability', 'a single incident disrupted global trade.'),
            ('Tata\'s acquisition of Jaguar Land Rover', 'In 2008 India\'s Tata Motors bought the British brands Jaguar and Land Rover from Ford.', 'MNCs from emerging economies', 'globalisation involves investment flows in many directions.')],
     evaluate=[('Multinational corporations bring more benefits than costs to host countries.', ['they create jobs and transfer technology and skills', 'they link local suppliers to global markets'], ['profits may leave the country and wages may be low', 'environmental and labour abuses, as at Rana Plaza, and tax avoidance'], 'MNCs can benefit host countries, but outcomes depend on regulation, bargaining power and how linked they are to local firms.')],
     src=[('Report (paraphrased)', 'The report found that a smartphone\'s components were sourced from dozens of suppliers in several countries, including chips from Taiwan and South Korea, displays from South Korea and Japan, and assembly in China or India, with most value captured by design, software and brand rather than assembly.', 'Paraphrase of analyses of iPhone supply chains, e.g. Xing and Detert, Asian Development Bank Institute, 2010, and later updates', 'to show how value is distributed in global supply chains', 'It uses detailed cost breakdowns based on industry data.', 'Cost estimates rely on teardown analyses and may not reflect confidential contract prices.', 'Global supply chains spread production widely, but most value goes to design and branding.')],
     rq=[('How has Apple\'s shift of some iPhone assembly from China to India since 2017 affected employment in Tamil Nadu?', 'What is an MNC?', 'it is a definition question', 'It investigates a current change in a global supply chain.', 'Use company reports, government data and news investigations; compare sources; evaluate perspectives; cite in APA.')])


@R.add('ch08-st2', ('C3', 'C4'), (1, 5), 'numerical')
def mnc_vs_gdp(rng, slot):
    firms = [('Walmart', 611), ('Amazon', 514), ('Saudi Aramco', 604), ('Apple', 394), ('Toyota', 275)]
    ctys = [('Nigeria', 363), ('Kenya', 108), ('Bangladesh', 437), ('Ethiopia', 163), ('Vietnam', 430), ('New Zealand', 250)]
    f, rev = rng.choice(firms); c, g = rng.choice(ctys)
    r = rev / g
    return dict(stem=f'In 2022–23 {f} had revenue of about US$ {rev} billion and {c} a GDP of about US$ {g} billion (approx.). Calculate the ratio of {f}\'s revenue to {c}\'s GDP'
                     + (' and explain why comparing revenue with GDP can be misleading.' if slot.d >= 3 else '.'),
                answer=f'about {r:.2f} : 1', type='numerical' if slot.d < 3 else 'multi_step', marks=2 if slot.d < 3 else 4,
                markingKey=f'{rev} ÷ {g} = {r:.2f} (M1 A1).' + (' Limitation (2): revenue is total sales, while GDP measures value added; a fair comparison uses company value added, which is much smaller; still, it indicates MNC economic power.' if slot.d >= 3 else ''),
                gap='G3')


K.st('ch08-st3', 'the winners and losers of globalisation: jobs, culture and inequality',
     terms=[('deindustrialisation', 'the decline of manufacturing industry in a region or country'),
            ('elephant curve', 'Branko Milanović\'s graph showing that global income growth from 1988 to 2008 was highest for the middle class of emerging economies and the global top 1%, and lowest for lower-middle classes in rich countries'),
            ('Rust Belt', 'the former industrial region of the north-eastern and midwestern USA affected by factory closures'),
            ('race to the bottom', 'competition between countries to attract investment by lowering wages, taxes or standards'),
            ('anti-globalisation movement', 'a movement criticising the effects of corporate globalisation, prominent at the 1999 Seattle WTO protests'),
            ('cultural erosion', 'the loss of local traditions, languages and identities under global influences')],
     facts=[('Who created the "elephant curve" of global income growth?', 'Branko Milanović', ['Thomas Piketty', 'Jeffrey Sachs', 'Joseph Stiglitz'], 'With Christoph Lakner.'),
            ('Which 1999 event saw mass protests against the WTO?', 'The Seattle ministerial conference', ['the Rio Earth Summit', 'the fall of the Berlin Wall', 'the Bandung Conference'], 'Sometimes called the "Battle of Seattle".'),
            ('About how many people did China lift out of extreme poverty between 1980 and 2020, according to the World Bank?', 'About 800 million', ['About 8 million', 'About 80 million', 'About 8 billion'], 'Linked to export-led growth.'),
            ('Which US city is often used as an example of deindustrialisation after the decline of car manufacturing?', 'Detroit', ['Miami', 'San Francisco', 'Las Vegas'], 'Its population fell from about 1.85 million in 1950 to about 640,000 in 2020.'),
            ('About how many languages are considered endangered worldwide, according to UNESCO?', 'About 40% of the world\'s roughly 7,000 languages', ['None', 'About 4', 'All of them'], 'Globalisation is one pressure.')],
     why=[('Explain why manufacturing workers in high-income countries have often lost from globalisation.', 'Factories moved to lower-cost countries, and imports competed with domestic products, leading to job losses and falling wages in industrial regions.'),
          ('Explain why the middle class in emerging economies has been a winner of globalisation.', 'Export industries, foreign investment and outsourcing created jobs and rising incomes in countries such as China, India and Vietnam.'),
          ('Explain why globalisation can increase inequality within countries.', 'Gains go to skilled workers, capital owners and connected regions, while unskilled workers and peripheral regions face competition and lose out.'),
          ('Explain why some people see globalisation as a threat to their identity.', 'Global media and brands may displace local culture, languages and traditions, and rapid change can create a sense of loss.')],
     contrast=[('winners of globalisation', 'losers of globalisation', 'Winners include emerging-economy middle classes, consumers and the global elite; losers include some manufacturing workers in rich countries and marginalised regions.'),
               ('global inequality between countries', 'inequality within countries', 'Between-country inequality has fallen as Asian economies grew; within many countries inequality has risen.')],
     misc=[('Globalisation has made all poor people poorer.', 'Extreme poverty fell from about 38% of the world population in 1990 to under 10% by 2019, partly due to trade-led growth, though gains were uneven.'),
           ('All job losses in rich countries are caused by globalisation.', 'Automation and technological change have also cut many manufacturing jobs.'),
           ('Only poor countries lose from globalisation.', 'Some groups in rich countries lose, while many in emerging economies gain.')],
     cases=[('Detroit\'s decline', 'Detroit lost much of its car industry and population after the 1960s due to competition, automation and relocation; it filed for bankruptcy in 2013.', 'losers of globalisation', 'deindustrialisation left a city with unemployment and urban decay.'),
            ('Vietnam\'s export growth', 'Since the Đổi Mới reforms of 1986, Vietnam has attracted MNCs such as Samsung; exports grew rapidly and poverty fell sharply.', 'winners of globalisation', 'integration into global markets drove growth and poverty reduction.')],
     evaluate=[('Globalisation has done more to reduce inequality than to increase it.', ['between-country inequality has fallen as Asia grew', 'extreme poverty has fallen dramatically'], ['inequality within many countries has risen', 'the top 1% captured a large share of gains'], 'Globalisation has reduced global inequality between countries but increased it within many; the overall judgement depends on which measure is used.')],
     src=[('Book (paraphrased)', 'The author showed that between 1988 and 2008 the biggest income gains went to the middle classes of emerging Asian economies and to the richest 1% of the world, while the lower-middle classes of rich countries saw little growth. He argued this helped explain political discontent in the West.', 'Paraphrase of Branko Milanović, Global Inequality: A New Approach for the Age of Globalization, Cambridge, MA, 2016', 'to analyse global income distribution and its political consequences', 'It uses household survey data from many countries.', 'Survey data under-record top incomes, and the curve depends on the start and end years chosen.', 'Globalisation\'s gains were unequally distributed between global groups.')],
     rq=[('How far has Vietnam\'s integration into global supply chains since 1986 reduced poverty?', 'Is globalisation good or bad?', 'it is a vague value question', 'It evaluates the impact of globalisation in a specific country.', 'Use World Bank poverty and trade data and two studies; graph trends; consider other factors; evaluate sources; cite in APA.')])
series('ch08-st3', [('the population of Detroit', 'people', 1950, 1_850_000, 2020, 639_000, 'US Census Bureau'),
                    ('the share of the world population in extreme poverty', 'per cent', 1990, 38, 2019, 9, 'World Bank'),
                    ('Vietnam\'s exports of goods', 'US$ billion', 2000, 14.5, 2023, 355, 'approx., General Statistics Office of Vietnam')], d=(1, 4))


K.st('ch08-st4', 'trade organisations and blocs: the WTO, the EU and ASEAN',
     terms=[('World Trade Organization (WTO)', 'the international organisation, founded in 1995, that sets and enforces rules for trade between its members'),
            ('trade bloc', 'a group of countries that reduce trade barriers among themselves, such as the EU or ASEAN'),
            ('customs union', 'a trade bloc with free trade inside and a common external tariff'),
            ('single market', 'a trade area allowing free movement of goods, services, capital and people, as in the EU'),
            ('ASEAN', 'the Association of Southeast Asian Nations, founded in 1967, with ten members'),
            ('most-favoured-nation principle', 'the WTO rule that a trade advantage given to one member must be given to all')],
     facts=[('How many members did the WTO have in 2024?', '166', ['16', '66', '193'], 'Including the EU.'),
            ('Which treaty created the European Economic Community in 1957?', 'The Treaty of Rome', ['the Treaty of Versailles', 'the Maastricht Treaty', 'the Treaty of Westphalia'], 'Six founding members.'),
            ('When did the United Kingdom leave the European Union?', '31 January 2020', ['23 June 2016', '1 January 1973', '1 January 2021'], 'The transition period ended on 31 December 2020.'),
            ('Which agreement, signed in 2020, created the world\'s largest trade bloc by population, including China and ASEAN?', 'The Regional Comprehensive Economic Partnership (RCEP)', ['NAFTA', 'Mercosur', 'the Paris Agreement'], 'India withdrew from the negotiations.'),
            ('Which country joined the WTO in 2001, a major event for world trade?', 'China', ['India', 'Brazil', 'Russia'], 'Russia joined in 2012.')],
     why=[('Explain why countries join trade blocs.', 'Removing barriers within the bloc gives access to larger markets, increases trade and investment, and strengthens bargaining power in global negotiations.'),
          ('Explain why trade blocs can disadvantage non-members.', 'Common external tariffs and preferential rules divert trade towards members, making it harder for outside producers, often from poorer countries, to compete.'),
          ('Explain why the WTO\'s Doha Round stalled.', 'Rich and developing countries disagreed, especially over agricultural subsidies in the EU and USA and access to markets for manufactured goods and services.'),
          ('Explain why the UK\'s departure from the EU affected trade.', 'Leaving the single market and customs union introduced customs checks and paperwork, raising costs for businesses trading with the EU.')],
     contrast=[('a free trade area', 'a customs union', 'A free trade area removes tariffs between members, who keep their own external tariffs; a customs union also has a common external tariff.'),
               ('the EU', 'ASEAN', 'The EU is a deep union with a single market, common institutions and (for 20 members) a single currency; ASEAN is a looser association focused on cooperation and gradual tariff reduction.')],
     misc=[('The WTO makes all trade completely free.', 'The WTO sets rules and reduces barriers through negotiation, but many tariffs and exceptions remain.'),
           ('Trade blocs always benefit all their members equally.', 'Gains vary; some regions or industries lose, and smaller members may have less influence.'),
           ('The EU is only an economic organisation.', 'It also has political institutions, a parliament, a court and common policies on the environment and human rights.')],
     cases=[('Brexit', 'The UK voted to leave the EU in June 2016 by 51.9% to 48.1% and left in January 2020; studies suggest UK–EU goods trade fell relative to trade with other countries.', 'leaving a trade bloc', 'leaving the single market raised trade costs.'),
            ('the WTO cotton dispute', 'Brazil challenged US cotton subsidies at the WTO and won in 2004–05; West African cotton producers had also complained about subsidies.', 'trade rules and fairness', 'a developing country used WTO rules to challenge a rich country\'s subsidies.')],
     evaluate=[('The WTO has been more successful than regional trade blocs in promoting free trade.', ['WTO rules cover almost all world trade and have a dispute system', 'tariffs have fallen greatly since GATT in 1947'], ['the Doha Round failed and the dispute appellate body has been paralysed since 2019', 'regional blocs such as the EU and RCEP have achieved deeper integration'], 'The WTO built the base of global trade rules, but recent progress has come mostly from regional and bilateral agreements.')],
     src=[('Treaty (paraphrased)', 'The treaty states that the Community aims to establish a common market and progressively bring together the economic policies of member states, to promote harmonious development, continuous expansion, increased stability, a rising standard of living and closer relations among its members.', 'Paraphrase of the Treaty establishing the European Economic Community (Treaty of Rome), Rome, 25 March 1957', 'to set out the legal basis and aims of the EEC', 'It is the official founding document showing the original aims.', 'It shows intentions in 1957, not how the EU developed or how members experienced it.', 'The EEC aimed at a common market and closer economic and political ties.')],
     rq=[('How did leaving the EU single market in 2021 affect UK food exports to the EU?', 'What is the EU?', 'it is a definition question', 'It investigates the effect of a trade policy change with data.', 'Use HMRC trade statistics, business surveys and two studies; compare before and after; evaluate sources; cite in APA.')])
C.trade(K, 'ch08-st4', c=('C3',), d=(1, 4))


@R.add('ch08-st4', ('C3', 'C4'), (1, 5), 'numerical')
def tariff(rng, slot):
    good, price = rng.choice([('a car imported into India', 20_000), ('a tonne of steel imported into the USA', 900), ('a pair of trainers imported into Brazil', 60),
                              ('a smartphone imported into Türkiye', 500), ('a bottle of wine imported into China', 30), ('a laptop imported into Nigeria', 800)])
    t = rng.choice([5, 10, 20, 25, 35, 50])
    new = price * (1 + t / 100)
    if slot.d <= 2:
        return dict(stem=f'The world price of {good} is US$ {price:,}. The importing country applies a {t}% tariff. What is the price after the tariff?',
                    answer=f'US$ {new:,.2f}'.replace('.00', ''), type='numerical', marks=2, markingKey=f'{price:,} × {1 + t / 100:.2f} = US$ {new:,.2f} (M1 A1).', gap='G3')
    q = rng.choice([1_000, 5_000, 20_000, 100_000])
    fall = rng.choice([10, 20, 30])
    q2 = q * (100 - fall) / 100
    rev = q2 * price * t / 100
    return dict(stem=(f'A country imports {q:,} units of {good.split(" imported")[0]} a year at a world price of US$ {price:,}. It introduces a {t}% tariff, and imports fall by {fall}%. '
                      'Calculate the new price, the new quantity imported and the tariff revenue, then explain who gains and who loses.'),
                answer=f'price US$ {new:,.2f}; imports {q2:,.0f}; revenue US$ {rev:,.0f}'.replace('.00;', ';'), type='multi_step', marks=6,
                markingKey=f'Price {price:,} × {1 + t / 100:.2f} = {new:,.2f} (A1); quantity {q:,} × {(100 - fall) / 100:.2f} = {q2:,.0f} (A1); revenue {q2:,.0f} × {price:,} × {t}% = US$ {rev:,.0f} (M1 A1). '
                           'Gains/losses (2): government gains revenue and domestic producers are protected; consumers pay more; foreign producers lose sales; risk of retaliation.', gap='G5')

# =============================================================================================
# ch09 Climate Change and Resource Management
# =============================================================================================
K.st('ch09-st1', 'climate change: the greenhouse effect, the evidence and the causes',
     terms=[('greenhouse effect', 'the natural process by which gases in the atmosphere trap heat radiated from the Earth\'s surface, keeping the planet warm'),
            ('enhanced greenhouse effect', 'the extra warming caused by increased concentrations of greenhouse gases from human activities'),
            ('greenhouse gases', 'gases such as carbon dioxide, methane, nitrous oxide and water vapour that absorb infrared radiation'),
            ('Keeling Curve', 'the record of atmospheric CO₂ measured at Mauna Loa, Hawaii, since 1958'),
            ('IPCC', 'the Intergovernmental Panel on Climate Change, which assesses climate science for governments'),
            ('carbon sink', 'a natural store that absorbs more carbon than it releases, such as forests and oceans'),
            ('feedback loop', 'a process that amplifies (positive) or reduces (negative) an initial change, such as melting ice reducing reflectivity')],
     facts=[('Roughly what was the atmospheric CO₂ concentration before the Industrial Revolution?', 'About 280 ppm', ['About 28 ppm', 'About 420 ppm', 'About 2,800 ppm'], 'It passed 420 ppm in 2023.'),
            ('By how much had global average surface temperature risen above pre-industrial levels by 2011–2020, according to the IPCC?', 'About 1.1 °C', ['About 0.1 °C', 'About 5 °C', 'About 11 °C'], 'IPCC AR6, 2021.'),
            ('Which human activity is the largest source of CO₂ emissions?', 'Burning fossil fuels for energy', ['Volcanic eruptions', 'Breathing', 'Ocean evaporation'], 'Coal, oil and gas.'),
            ('Which greenhouse gas is released in large amounts by cattle and rice paddies?', 'Methane', ['Oxygen', 'Nitrogen', 'Argon'], 'It is much more potent than CO₂ over 20 years.'),
            ('Which evidence comes from bubbles trapped in Antarctic ice?', 'Past atmospheric CO₂ levels over 800,000 years', ['Future rainfall', 'Ocean salinity today', 'Earthquake frequency'], 'Ice cores are a key proxy record.')],
     why=[('Explain why increasing CO₂ concentrations cause global warming.', 'CO₂ absorbs and re-emits infrared radiation from the Earth\'s surface, so more CO₂ traps more heat in the lower atmosphere, raising average temperatures.'),
          ('Explain why melting Arctic sea ice is a positive feedback.', 'Ice reflects most sunlight; as it melts, darker ocean absorbs more heat, causing more warming and more melting.'),
          ('Explain why scientists are confident that recent warming is caused by humans.', 'The rise in CO₂ matches fossil fuel use, the carbon has a fossil isotopic signature, natural factors such as solar activity cannot explain the trend, and models reproduce warming only with human emissions.'),
          ('Explain why deforestation contributes to climate change.', 'Trees store carbon; cutting and burning them releases CO₂ and removes a carbon sink that would otherwise absorb emissions.')],
     contrast=[('the natural greenhouse effect', 'the enhanced greenhouse effect', 'The natural effect keeps Earth about 33 °C warmer than it would be and makes life possible; the enhanced effect is the extra warming caused by human emissions.'),
               ('weather', 'climate', 'Weather is short-term atmospheric conditions; climate is the average weather over about 30 years or more.')],
     misc=[('A cold winter disproves global warming.', 'Climate change refers to long-term global averages; individual cold events still occur within a warming trend.'),
           ('The greenhouse effect is harmful in itself.', 'Without the natural greenhouse effect Earth would average about −18 °C; the problem is the enhanced effect.'),
           ('Climate change is caused mainly by the hole in the ozone layer.', 'The ozone hole is a separate problem caused by CFCs; climate change is caused mainly by greenhouse gases such as CO₂.')],
     cases=[('the Keeling Curve', 'Charles David Keeling began measuring CO₂ at Mauna Loa in 1958 at about 315 ppm; the record shows a steady rise and seasonal cycle, passing 420 ppm in 2023.', 'evidence of rising CO₂', 'continuous measurement provides clear evidence of human-caused change.'),
            ('Arctic sea-ice decline', 'September Arctic sea-ice extent has fallen by about 13% per decade since satellite records began in 1979.', 'evidence and feedback', 'it shows warming and drives a positive feedback.')],
     evaluate=[('Natural factors explain most of the climate change observed since 1950.', ['climate has changed naturally in the past, e.g. ice ages', 'volcanoes and solar cycles affect temperature'], ['solar output has not increased since 1950 while temperatures have risen', 'the IPCC concludes it is unequivocal that human influence has warmed the climate'], 'Natural factors cause variation, but the evidence overwhelmingly shows that recent warming is driven by human greenhouse gas emissions.')],
     src=[('IPCC report (paraphrased)', 'The report concluded that it is unequivocal that human influence has warmed the atmosphere, ocean and land, and that widespread and rapid changes have occurred. It estimated that global surface temperature in 2011–2020 was about 1.1 °C above 1850–1900.', 'Paraphrase of IPCC, Climate Change 2021: The Physical Science Basis, Summary for Policymakers, Geneva, 2021', 'to provide governments with an assessment of climate science', 'It summarises thousands of peer-reviewed studies and is approved by governments.', 'As a consensus summary it may be cautious, and it was published before the most recent data.', 'Humans have unequivocally warmed the climate by about 1.1 °C.')],
     rq=[('How has the length of the growing season in Punjab changed since 1970, and is this consistent with climate change?', 'Is climate change real?', 'it is a closed question with a clear scientific answer', 'It investigates local evidence of a global process.', 'Use IMD temperature data, crop calendars and two studies; graph trends; evaluate data; cite in APA.')])
C.rate_of_change(K, 'ch09-st1', [('atmospheric CO₂ at Mauna Loa', 'ppm', [(1960, 316.9), (1980, 338.8), (2000, 369.7), (2010, 389.9), (2023, 421.1)], 'NOAA'),
                                 ('global CO₂ emissions from fossil fuels', 'billion tonnes', [(1960, 9.4), (1980, 19.5), (2000, 25.5), (2010, 33.4), (2023, 37.4)], 'Global Carbon Project, approx.')])
C.footprint(K, 'ch09-st1', c=('C3',), d=(1, 4))


K.st('ch09-st2', 'the impacts of climate change on people and places',
     terms=[('sea-level rise', 'the increase in average sea level caused by thermal expansion of water and melting ice'),
            ('climate refugee', 'a person forced to move because of climate-related impacts, though the term has no formal legal status'),
            ('coral bleaching', 'the loss of colour in corals when warmer water causes them to expel the algae they depend on'),
            ('extreme weather event', 'a rare and severe event such as a heatwave, flood, drought or tropical storm'),
            ('vulnerability', 'the degree to which people or places are likely to be harmed by hazards'),
            ('glacial retreat', 'the shrinking of glaciers as melting exceeds accumulation')],
     facts=[('By roughly how much has global mean sea level risen since 1900?', 'About 20 cm', ['About 2 cm', 'About 2 m', 'About 20 m'], 'The rate is accelerating.'),
            ('Which country, mostly less than 1 m above sea level, is among the most threatened by sea-level rise?', 'The Maldives', ['Nepal', 'Switzerland', 'Bolivia'], 'Also Tuvalu, Kiribati and the Marshall Islands.'),
            ('Which reef suffered mass bleaching events in 2016, 2017, 2020, 2022 and 2024?', 'The Great Barrier Reef', ['the Red Sea reefs only', 'Lake Baikal', 'the Dead Sea'], 'Linked to marine heatwaves.'),
            ('Which 2022 disaster flooded about a third of Pakistan?', 'Monsoon floods', ['a tsunami', 'an earthquake', 'a volcanic eruption'], 'About 33 million people were affected.'),
            ('Which agreement in 2023 created a "loss and damage" fund?', 'The COP28 agreement in Dubai (fund agreed at COP27, operationalised at COP28)', ['the Kyoto Protocol', 'the Montreal Protocol', 'the Treaty of Rome'], 'It aims to help vulnerable countries.')],
     why=[('Explain why low-income countries are often more vulnerable to climate change.', 'They depend more on agriculture, have less money for defences and recovery, weaker infrastructure and health systems, and many are in hot or low-lying regions.'),
          ('Explain why glacial retreat in the Himalayas threatens water supplies.', 'Glaciers feed rivers such as the Ganges and Indus in the dry season; as they shrink, long-term flows will fall, affecting hundreds of millions of people.'),
          ('Explain why sea-level rise threatens coastal cities.', 'Higher seas increase flooding and storm surges, erode coasts and contaminate freshwater, threatening homes and infrastructure in cities such as Dhaka, Jakarta and Miami.'),
          ('Explain why climate change raises questions of justice.', 'Countries and people who contributed least to emissions, such as small island states and the poor, often suffer the worst impacts.')],
     contrast=[('environmental impacts', 'social and economic impacts', 'Environmental impacts include coral bleaching and habitat loss; social and economic impacts include crop losses, migration and damage to infrastructure.'),
               ('sudden-onset impacts', 'slow-onset impacts', 'Sudden-onset impacts are events such as floods and storms; slow-onset impacts are gradual changes such as sea-level rise and desertification.')],
     misc=[('Climate change will affect all places in the same way.', 'Impacts vary: some regions get wetter, others drier; high latitudes warm fastest; vulnerability varies with wealth.'),
           ('Climate change impacts are only in the future.', 'Impacts are already observed, including heatwaves, glacier loss and coral bleaching.'),
           ('Rising sea levels are caused only by melting sea ice.', 'Melting sea ice does not raise sea level much; thermal expansion and melting land ice (glaciers and ice sheets) do.')],
     cases=[('Pakistan floods 2022', 'Record monsoon rainfall, intensified by climate change according to attribution studies, flooded large areas, killed over 1,700 people and caused about US$ 30 billion in damage and losses.', 'extreme weather impacts', 'a country with low emissions suffered severe climate-related losses.'),
            ('Tuvalu', 'With a maximum elevation of about 4.6 m, Tuvalu faces existential threats; in 2023 it signed a treaty with Australia allowing some citizens to migrate.', 'sea-level rise and migration', 'small island states face loss of territory and forced relocation.')],
     evaluate=[('Low-income countries will suffer the most from climate change.', ['they are more dependent on agriculture and have fewer resources to adapt', 'many are in hot, low-lying or drought-prone regions'], ['rich countries also face heatwaves, wildfires and flooding, e.g. Europe 2022', 'within all countries the poorest suffer most'], 'Low-income countries are generally most vulnerable, but impacts depend on both exposure and capacity to adapt, and poor groups everywhere are at risk.')],
     src=[('Speech (paraphrased)', 'The prime minister of a Caribbean island state told world leaders that a 2 °C rise would be a death sentence for small island states, and called for reform of global finance to help vulnerable countries adapt and recover from climate disasters.', 'Paraphrase of Mia Mottley, Prime Minister of Barbados, speech at COP26, Glasgow, 1 November 2021', 'to urge leaders to act on climate change and climate finance', 'It expresses the perspective of small island states.', 'It is a persuasive speech, not a scientific report.', 'Small island states face existential risks and need finance and urgent action.')],
     rq=[('How far has sea-level rise contributed to coastal flooding in Jakarta since 1990?', 'What does climate change do?', 'it is too broad', 'It investigates a specific impact, distinguishing climate from local causes such as subsidence.', 'Use tide-gauge and subsidence data, government reports and two studies; compare causes; evaluate sources; cite in APA.')])
C.rate_of_change(K, 'ch09-st2', [('global mean sea level relative to 1993', 'mm', [(1993, 0), (2000, 20), (2010, 50), (2020, 95), (2023, 105)], 'NASA satellite data, approx.')])


K.st('ch09-st3', 'responses to climate change: mitigation, adaptation and international agreements',
     terms=[('mitigation', 'actions that reduce greenhouse gas emissions or increase carbon sinks, such as renewable energy and reforestation'),
            ('adaptation', 'actions that reduce vulnerability to climate impacts, such as flood defences, drought-resistant crops and early warning systems'),
            ('Paris Agreement', 'the 2015 agreement under which countries aim to limit warming to well below 2 °C, pursuing 1.5 °C, through nationally determined contributions'),
            ('nationally determined contribution (NDC)', 'each country\'s pledge of emission reductions under the Paris Agreement'),
            ('carbon tax', 'a tax on the carbon content of fuels to encourage lower emissions'),
            ('net zero', 'a state in which greenhouse gas emissions are balanced by removals from the atmosphere'),
            ('Kyoto Protocol', 'the 1997 agreement setting binding targets for developed countries to cut emissions')],
     facts=[('In which year was the Paris Agreement adopted?', '2015', ['1992', '1997', '2021'], 'At COP21.'),
            ('Which 1997 agreement set binding emission targets only for developed countries?', 'The Kyoto Protocol', ['the Paris Agreement', 'the Montreal Protocol', 'the Rio Declaration'], 'The USA never ratified it.'),
            ('Which principle recognises that rich and poor countries have different responsibilities for climate action?', 'Common but differentiated responsibilities', ['the polluter never pays', 'first past the post', 'the most-favoured-nation principle'], 'Agreed at Rio in 1992.'),
            ('Which country introduced one of the world\'s first carbon taxes, in 1991?', 'Sweden', ['the United States', 'China', 'Brazil'], 'Its rate is now over €100 per tonne.'),
            ('By what year has India pledged to reach net zero emissions?', '2070', ['2030', '2050', '2100'], 'Announced at COP26 in 2021.')],
     why=[('Explain why both mitigation and adaptation are needed.', 'Mitigation limits future warming, but some warming is already locked in, so adaptation is needed to cope with impacts that cannot be avoided.'),
          ('Explain why international agreements on climate change are difficult to achieve.', 'Countries differ in responsibility, wealth and vulnerability, cutting emissions has economic costs, and there is a free-rider problem when some benefit without acting.'),
          ('Explain why the Paris Agreement uses voluntary national pledges.', 'Binding targets had failed to win universal support; voluntary NDCs allowed almost all countries to join, with a review mechanism to raise ambition over time.'),
          ('Explain why a carbon tax can reduce emissions.', 'It raises the price of fossil fuels, encouraging firms and households to use energy more efficiently and switch to low-carbon alternatives.')],
     contrast=[('mitigation', 'adaptation', 'Mitigation tackles the causes by reducing emissions; adaptation responds to the effects by reducing vulnerability.'),
               ('the Kyoto Protocol', 'the Paris Agreement', 'Kyoto set binding targets for developed countries only; Paris covers almost all countries with voluntary, self-set pledges.')],
     misc=[('The Paris Agreement legally forces countries to meet their targets.', 'Countries must submit and report on NDCs, but the targets themselves are not legally binding.'),
           ('Adaptation means giving up on stopping climate change.', 'Adaptation complements mitigation; both are needed.'),
           ('Individual action is all that is needed to solve climate change.', 'Individual choices help, but systemic change in energy, transport, industry and policy is essential.')],
     cases=[('Bangladesh\'s cyclone preparedness', 'Early warning systems, cyclone shelters and volunteer networks reduced deaths from about 300,000 in 1970 and 138,000 in 1991 to a few thousand in later cyclones.', 'adaptation', 'investment in preparedness saved many lives despite continued exposure.'),
            ('Costa Rica\'s electricity', 'Since 2015 Costa Rica has generated over 98% of its electricity from renewable sources, mainly hydro, geothermal and wind.', 'mitigation', 'a middle-income country decarbonised its power sector.')],
     evaluate=[('International agreements are the most effective way to tackle climate change.', ['global problems need global cooperation', 'the Paris Agreement has shifted expectations and investment'], ['pledges are insufficient and not binding', 'national policies, technology and markets (e.g. falling solar costs) drive much of the change'], 'Agreements provide a framework and pressure, but real reductions depend on national policies, technology and finance.')],
     src=[('Agreement text (paraphrased)', 'The parties agreed to hold the increase in global average temperature to well below 2 °C above pre-industrial levels and to pursue efforts to limit it to 1.5 °C, recognising that this would significantly reduce the risks and impacts of climate change.', 'Paraphrase of the Paris Agreement, Article 2, adopted at COP21, Paris, 12 December 2015', 'to set the goal of international climate action', 'It is the agreed legal text accepted by almost all countries.', 'It sets goals but not binding national targets; it does not show whether action matches the goals.', 'Countries aim to keep warming well below 2 °C and pursue 1.5 °C.')],
     rq=[('How effective has Sweden\'s carbon tax been in reducing emissions since 1991?', 'How can we stop climate change?', 'it is very broad', 'It evaluates a specific mitigation policy with data.', 'Use Swedish emissions data, tax rates and two studies; compare with GDP growth; evaluate sources; cite in APA.')])
C.footprint(K, 'ch09-st3', c=('C3', 'C4'), d=(2, 5))


@R.add('ch09-st3', ('C3', 'C4'), (1, 5), 'numerical')
def carbon_tax(rng, slot):
    fuel, ef = rng.choice([('petrol', 2.31), ('diesel', 2.68)])  # kg CO2 per litre
    tax = rng.choice([25, 50, 100, 130])
    add = ef * tax / 1000
    if slot.d <= 2:
        return dict(stem=f'Burning one litre of {fuel} releases about {ef} kg of CO₂. With a carbon tax of US$ {tax} per tonne of CO₂, how much tax is added per litre?',
                    answer=f'about US$ {add:.3f}', type='numerical', marks=2, markingKey=f'{ef} kg = {ef / 1000} t; × {tax} = US$ {add:.3f} per litre (M1 A1).', gap='G3')
    litres = rng.choice([800, 1200, 1500, 2000])
    cut = rng.choice([5, 10, 15])
    co2 = litres * ef / 1000
    return dict(stem=(f'A household uses {litres:,} litres of {fuel} a year (about {ef} kg CO₂ per litre). A carbon tax of US$ {tax}/t CO₂ is introduced, and the household cuts its fuel use by {cut}%. '
                      'Calculate the household\'s annual emissions before the cut, its annual carbon tax after the cut, and evaluate the fairness of carbon taxes.'),
                answer=f'{co2:.2f} t CO₂; tax US$ {co2 * (1 - cut / 100) * tax:,.2f}', type='multi_step', marks=6,
                markingKey=f'{litres:,} × {ef} = {litres * ef:,.0f} kg = {co2:.2f} t (A1); after cut {co2 * (1 - cut / 100):.3f} t (M1); × {tax} = US$ {co2 * (1 - cut / 100) * tax:,.2f} (A1). '
                           'Evaluation (3): taxes are regressive for low-income households who spend more of their income on energy; revenue can be returned as dividends (as in Canada) or used to support public transport.', gap='G5')


K.st('ch09-st4', 'sustainable resource management: water, energy and the circular economy',
     terms=[('sustainable resource management', 'using resources to meet present needs without compromising the ability of future generations to meet theirs'),
            ('circular economy', 'an economic system that keeps materials in use through reuse, repair, remanufacturing and recycling, designing out waste'),
            ('linear economy', 'the "take, make, dispose" model of resource use'),
            ('water stress', 'when demand for water exceeds the available supply or poor quality restricts its use'),
            ('energy mix', 'the combination of sources used to generate a country\'s energy, such as coal, gas, nuclear, hydro, wind and solar'),
            ('renewable energy', 'energy from sources that are naturally replenished, such as solar, wind, hydro and geothermal'),
            ('virtual water', 'the water used to produce goods that are traded, such as crops or clothing')],
     facts=[('About how many litres of water are needed to make one cotton T-shirt, according to the Water Footprint Network?', 'About 2,700', ['About 27', 'About 270,000', 'About 2.7'], 'Mostly for growing cotton.'),
            ('Which source provided the largest share of new global electricity capacity in 2023?', 'Solar power', ['Coal', 'Nuclear', 'Oil'], 'Solar costs fell about 90% in a decade.'),
            ('Which country generates about 98% of its electricity from renewables, mostly hydropower?', 'Norway', ['Saudi Arabia', 'Poland', 'South Africa'], 'Its mountains and rainfall suit hydro.'),
            ('Which city faced the threat of "Day Zero", when taps would run dry, in 2018?', 'Cape Town', ['London', 'Tokyo', 'Toronto'], 'Strict restrictions cut use by about half.'),
            ('Which foundation has promoted the idea of the circular economy since 2010?', 'The Ellen MacArthur Foundation', ['the Gates Foundation', 'the Nobel Foundation', 'the Rockefeller Foundation'], 'Founded by the British sailor.')],
     why=[('Explain why water stress is increasing in many regions.', 'Population growth, urbanisation, irrigation, industrial use, pollution and climate change are increasing demand and reducing reliable supply.'),
          ('Explain why a circular economy can reduce resource use.', 'Keeping products and materials in use through repair, reuse and recycling reduces the need for new raw materials and cuts waste and emissions.'),
          ('Explain why countries are trying to diversify their energy mix.', 'Relying on one source, especially imported fossil fuels, creates risks to supply and prices; diversification improves energy security and can reduce emissions.'),
          ('Explain why renewable energy can be challenging to integrate into electricity grids.', 'Solar and wind are intermittent, so grids need storage, flexible backup and better transmission to balance supply and demand.')],
     contrast=[('a linear economy', 'a circular economy', 'A linear economy takes resources, makes products and throws them away; a circular economy keeps materials in use and designs out waste.'),
               ('renewable energy', 'non-renewable energy', 'Renewable energy comes from sources that are replenished, such as sun and wind; non-renewable energy comes from finite stocks such as coal, oil and gas.')],
     misc=[('Recycling alone creates a circular economy.', 'Recycling is the last resort; reducing, reusing, repairing and redesigning products are higher priorities.'),
           ('Renewable energy has no environmental impact.', 'Dams flood land and affect rivers, mining for battery materials has impacts, and wind farms affect landscapes and wildlife.'),
           ('Water is an unlimited resource because it is recycled by the water cycle.', 'Usable fresh water in the right place and time is limited, and aquifers can be depleted faster than they recharge.')],
     cases=[('Cape Town\'s Day Zero', 'After three years of drought, the city cut water use from about 1.2 billion litres a day in 2015 to around 500 million litres in 2018 through restrictions, pricing and campaigns.', 'water management', 'demand management avoided taps running dry.'),
            ('Singapore\'s NEWater', 'Singapore recycles treated wastewater into high-grade water, which can meet up to about 40% of its demand.', 'sustainable water supply', 'technology reduced dependence on imported water.')],
     evaluate=[('Technology is the most important solution to sustainable resource management.', ['desalination, NEWater and cheap solar power show what technology can do', 'efficiency improvements reduce resource use'], ['behaviour change and pricing, as in Cape Town, are crucial', 'governance and equitable access matter as much as technology'], 'Technology is essential, but without good governance, pricing and behaviour change it cannot ensure sustainable and fair resource use.')],
     src=[('Report (paraphrased)', 'The report argued that the world\'s economy is only about 7% circular, meaning that over 90% of materials extracted are wasted, lost or remain unavailable for reuse. It called for redesigning products and business models to keep materials in use.', 'Paraphrase of Circle Economy, Circularity Gap Report 2023, Amsterdam', 'to measure global circularity and advocate change', 'It provides a global estimate based on material flow data.', 'It is produced by an organisation that promotes the circular economy, and global material data are uncertain.', 'The global economy is mostly linear and must become more circular.')],
     rq=[('How effective were Cape Town\'s water restrictions in reducing household water use between 2015 and 2018?', 'How can we save water?', 'it is vague and has no focus', 'It evaluates a real resource management strategy with data.', 'Use City of Cape Town data, news reports and two studies; graph consumption; evaluate sources; cite in APA.')])


@R.add('ch09-st4', ('C3', 'C4'), (1, 5), 'numerical')
def energy_mix(rng, slot):
    rows = [('Germany', 515, 267), ('India', 1_950, 390), ('China', 9_400, 2_900), ('Brazil', 710, 630), ('the United Kingdom', 290, 135), ('South Africa', 230, 30),
            ('Australia', 275, 98)]
    co, tot, ren = rng.choice(rows)
    sh = ren / tot * 100
    if slot.d <= 3:
        return dict(stem=f'In 2023 {co} generated about {tot:,} TWh of electricity, of which about {ren:,} TWh came from renewable sources (approx., Ember). Calculate the renewable share.',
                    answer=f'{sh:.1f}%', type='numerical', marks=2, markingKey=f'{ren:,} ÷ {tot:,} × 100 = {sh:.1f}% (M1 A1).', gap='G3')
    c2, t2, r2 = rng.choice([r for r in rows if r[0] != co])
    s2 = r2 / t2 * 100
    return dict(stem=(f'Electricity generation, 2023 (approx., Ember): {co} {tot:,} TWh total, {ren:,} TWh renewable; {c2} {t2:,} TWh total, {r2:,} TWh renewable. '
                      'Calculate the renewable share for each and explain two factors that explain the difference.'),
                answer=f'{co}: {sh:.1f}%; {c2}: {s2:.1f}%', type='multi_step', marks=5,
                markingKey=f'{co} {sh:.1f}% (A1); {c2} {s2:.1f}% (A1); comparison (A1). Factors (2): physical resources (rivers for hydro, sun, wind), coal reserves and existing infrastructure, '
                           'government policy and investment, level of demand growth.', gap='G5')

# =============================================================================================
# ch10 Population and Migration
# =============================================================================================
K.st('ch10-st1', 'population distribution, density and change, and the demographic transition model',
     terms=[('population distribution', 'the way people are spread across an area'),
            ('population density', 'the number of people per square kilometre'),
            ('demographic transition model (DTM)', 'a model showing how birth and death rates, and so population growth, change as a country develops, in five stages'),
            ('crude birth rate', 'the number of live births per 1,000 people per year'),
            ('crude death rate', 'the number of deaths per 1,000 people per year'),
            ('natural increase', 'the birth rate minus the death rate, usually expressed per 1,000 or as a percentage'),
            ('total fertility rate', 'the average number of children a woman would have over her lifetime at current rates')],
     facts=[('In which year did the world population reach 8 billion, according to the UN?', '2022', ['2000', '2011', '2050'], 'On 15 November 2022.'),
            ('In which stage of the DTM do birth rates remain high while death rates fall rapidly?', 'Stage 2', ['Stage 1', 'Stage 4', 'Stage 5'], 'Population grows fastest.'),
            ('Which country overtook China as the world\'s most populous country in 2023?', 'India', ['the United States', 'Indonesia', 'Nigeria'], 'About 1.43 billion people.'),
            ('Which country is often used as an example of DTM stage 5, with a falling population?', 'Japan', ['Niger', 'Afghanistan', 'Nigeria'], 'Its population has fallen since about 2010.'),
            ('What total fertility rate is needed to replace a population in the long term (without migration)?', 'About 2.1', ['About 1.0', 'About 4.0', 'About 0.5'], 'Replacement-level fertility.')],
     why=[('Explain why death rates fall in stage 2 of the DTM.', 'Improvements in food supply, clean water, sanitation, vaccination and medical care reduce deaths, especially among infants and children.'),
          ('Explain why birth rates fall in stage 3 of the DTM.', 'As urbanisation, women\'s education and employment increase, children become costly rather than economic assets, contraception is available and infant mortality falls, so families have fewer children.'),
          ('Explain why the DTM may not fit all countries.', 'It was based on the experience of European countries; some countries passed through stages much faster, and factors such as HIV/AIDS, migration, war or policies like China\'s one-child policy alter the pattern.'),
          ('Explain why population density varies within countries.', 'Physical factors such as relief, climate, water and soil, and human factors such as jobs, transport and services, make some areas attractive and others hostile.')],
     contrast=[('stage 2 of the DTM', 'stage 4 of the DTM', 'In stage 2 birth rates are high and death rates fall, so population grows rapidly; in stage 4 both are low, so growth is slow or stable.'),
               ('population distribution', 'population density', 'Distribution describes where people live; density measures how many people live per unit area.')],
     misc=[('Population growth is accelerating worldwide.', 'The world growth rate peaked at about 2.1% a year in the late 1960s and is now under 1%; fertility has fallen in most countries.'),
           ('High population density always means poverty.', 'Singapore and the Netherlands are very densely populated and wealthy; Niger has low density and high poverty.'),
           ('All countries move through the DTM at the same speed.', 'South Korea passed from high to very low fertility in about 40 years, much faster than European countries.')],
     cases=[('South Korea\'s fertility decline', 'The total fertility rate fell from about 6.0 in 1960 to about 0.72 in 2023, the lowest in the world.', 'rapid demographic transition', 'economic development, urbanisation and high costs of raising children transformed population change.'),
            ('Niger', 'With a total fertility rate of about 6.7, Niger has one of the world\'s fastest-growing and youngest populations.', 'early-stage demographic transition', 'high birth rates and falling death rates produce very rapid growth.')],
     evaluate=[('The demographic transition model is still useful for understanding population change today.', ['it describes the broad pattern in most countries', 'it links population change to development'], ['it is based on European history and does not predict timing', 'it ignores migration and policy, and stage 5 was added later'], 'The DTM remains a useful framework, but it must be applied critically alongside data on migration, policy and culture.')],
     src=[('UN report (paraphrased)', 'The report projected that the world population would continue to grow, reaching a peak of about 10.3 billion in the mid-2080s, before declining slightly. More than half of the projected growth to 2050 would occur in just eight countries, five of them in Africa.', 'Paraphrase of United Nations Department of Economic and Social Affairs, World Population Prospects 2024', 'to provide population estimates and projections for planning', 'It is the standard global source, using census and survey data.', 'Projections depend on assumptions about fertility and mortality that may prove wrong.', 'World population will peak later this century, with growth concentrated in Africa.')],
     rq=[('How well does the demographic transition model describe South Korea\'s population change since 1950?', 'What is the DTM?', 'it is a definition question', 'It tests a model against a real country\'s data.', 'Use UN World Population Prospects data; plot birth and death rates; compare with the model; evaluate the model; cite in APA.')])
C.density(K, 'ch10-st1')
C.natural_increase(K, 'ch10-st1')
C.pop_change(K, 'ch10-st1')


K.st('ch10-st2', 'population structure: population pyramids, ageing and youthful populations',
     terms=[('population pyramid', 'a graph showing the age and sex structure of a population'),
            ('dependency ratio', 'the ratio of dependants (aged 0–14 and 65+) to people of working age (15–64), usually per 100'),
            ('ageing population', 'a population in which the proportion of older people is increasing'),
            ('youthful population', 'a population with a high proportion of children and young people'),
            ('demographic dividend', 'the economic growth possible when the working-age share of the population is large relative to dependants'),
            ('life expectancy', 'the average number of years a person is expected to live')],
     facts=[('What shape is the population pyramid of a country with high birth rates and a youthful population?', 'A wide base narrowing sharply towards the top', ['A narrow base and wide top', 'A rectangle', 'An hourglass'], 'Typical of Niger or Uganda.'),
            ('About what share of Japan\'s population was aged 65 or over in 2023?', 'About 29%', ['About 3%', 'About 10%', 'About 60%'], 'The highest share in the world.'),
            ('Which country\'s large working-age population is often said to offer a demographic dividend in the 2020s?', 'India', ['Japan', 'Italy', 'Germany'], 'Its median age is about 28.'),
            ('A dependency ratio of 50 means what?', '50 dependants for every 100 people of working age', ['50% of people are working', '50 workers for every dependant', 'half the population is over 65'], 'Dependants are 0–14 and 65+.'),
            ('Which country introduced the "Silver Hair" policies and robots to support elderly care?', 'Japan', ['Nigeria', 'Afghanistan', 'Bolivia'], 'Japan faces labour shortages in care.')],
     why=[('Explain why ageing populations create economic challenges.', 'Fewer workers support more retirees, raising pension and health costs, reducing the tax base and causing labour shortages.'),
          ('Explain why youthful populations create challenges.', 'Governments must provide schools, healthcare and, later, jobs for large numbers of young people; if jobs are lacking, unemployment and emigration rise.'),
          ('Explain why a demographic dividend is not automatic.', 'It requires jobs, education and healthy, skilled workers; without investment and job creation, a large working-age population can lead to unemployment.'),
          ('Explain why population pyramids are useful for planners.', 'They show how many people will need schools, jobs, housing, pensions and care in the future.')],
     contrast=[('a youthful population structure', 'an ageing population structure', 'A youthful structure has a wide base and many children, needing schools and jobs; an ageing structure has a narrow base and many older people, needing pensions and care.'),
               ('young dependants', 'elderly dependants', 'Young dependants (0–14) need education and childcare; elderly dependants (65+) need pensions, health and social care.')],
     misc=[('An ageing population is only a problem for rich countries.', 'China, Thailand and Brazil are ageing rapidly before becoming rich, which some call "growing old before growing rich".'),
           ('Older people contribute nothing to the economy.', 'Many work, volunteer, provide childcare and spend, supporting the economy.'),
           ('A high dependency ratio always means economic decline.', 'Effects depend on productivity, participation rates, migration and policy.')],
     cases=[('Japan\'s ageing society', 'With about 29% aged 65+, Japan faces labour shortages; it has raised the retirement age, encouraged automation and gradually increased foreign workers.', 'responses to ageing', 'a country adapting to a rapidly ageing population.'),
            ('Uganda\'s youthful population', 'About 45% of Ugandans are under 15; the government faces pressure to expand schooling and create jobs.', 'challenges of youth', 'a youthful structure requires heavy investment in education and employment.')],
     evaluate=[('An ageing population is a greater challenge than a youthful population.', ['pension and health costs rise while the workforce shrinks', 'it is hard to reverse'], ['youthful populations need huge investment in schools and jobs', 'unemployment among young people can cause instability'], 'Both bring serious challenges; which is greater depends on a country\'s wealth, institutions and policies.')],
     src=[('Report (paraphrased)', 'The report stated that by 2050 one in six people worldwide would be aged over 65, up from one in eleven in 2019, and that in Europe and North America the figure would be one in four. It argued that policies should support healthy ageing and lifelong work.', 'Paraphrase of United Nations, World Population Ageing 2019: Highlights', 'to inform governments about ageing trends', 'It uses UN population data and projections.', 'Projections are uncertain, and it summarises global trends rather than national details.', 'Population ageing is accelerating globally and needs policy responses.')],
     rq=[('How has Japan responded to labour shortages in elderly care since 2010?', 'Why is Japan old?', 'it is vague and informal', 'It investigates policy responses to an ageing population.', 'Use government statistics, reports on care workers and robots, and two studies; evaluate sources; cite in APA.')])
C.dependency(K, 'ch10-st2')


K.st('ch10-st3', 'migration, refugees and asylum: push and pull factors and policies',
     terms=[('asylum seeker', 'a person who has left their country and is seeking protection as a refugee, whose claim has not yet been decided'),
            ('refugee', 'a person recognised as having a well-founded fear of persecution under the 1951 Refugee Convention'),
            ('non-refoulement', 'the principle that refugees must not be returned to a country where they face serious threats'),
            ('points-based immigration system', 'a system admitting migrants according to points for skills, language and job offers, as in Canada and Australia'),
            ('internally displaced person (IDP)', 'a person forced to flee their home who stays within their own country'),
            ('economic migrant', 'a person who moves mainly to improve their income or employment')],
     facts=[('Which country hosted the largest number of refugees in the world in 2023?', 'Iran (about 3.8 million), closely followed by Türkiye', ['the United Kingdom', 'Japan', 'Brazil'], 'Mostly Afghans in Iran and Syrians in Türkiye.'),
            ('Which principle in the Refugee Convention prevents returning refugees to danger?', 'Non-refoulement', ['Sovereignty', 'Free trade', 'Subsidiarity'], 'It is part of customary international law.'),
            ('Which country introduced a points-based immigration system in 1967?', 'Canada', ['India', 'Japan', 'Egypt'], 'Australia and later the UK followed.'),
            ('In 2015, about how many asylum applications did Germany receive, mainly from Syrians?', 'About 470,000 (and about 745,000 in 2016)', ['About 4,700', 'About 47,000', 'About 47 million'], 'Angela Merkel kept the border open.'),
            ('Where is the world\'s largest refugee settlement, housing nearly a million Rohingya?', 'Cox\'s Bazar, Bangladesh', ['Dadaab, Kenya', 'Zaatari, Jordan', 'Calais, France'], 'Most Rohingya fled Myanmar in 2017.')],
     why=[('Explain why most refugees stay in neighbouring countries.', 'They flee quickly and over land, often lack money and documents to travel far, and hope to return home soon; neighbouring countries may share language and culture.'),
          ('Explain why governments use points-based immigration systems.', 'They select migrants with skills, qualifications and language ability that meet labour market needs.'),
          ('Explain why migration policy is politically controversial.', 'It involves debates about national identity, labour markets, public services, humanitarian obligations and border control.'),
          ('Explain why some migration is described as "mixed".', 'Refugees, asylum seekers and economic migrants often travel the same routes, and individuals may have several reasons for moving.')],
     contrast=[('an asylum seeker', 'a refugee', 'An asylum seeker has applied for protection and is awaiting a decision; a refugee has been recognised as needing protection.'),
               ('restrictive migration policies', 'open migration policies', 'Restrictive policies limit entry with quotas, visas and border controls; open policies, like freedom of movement within the EU, allow easier movement.')],
     misc=[('Most refugees go to Europe.', 'About 70% of refugees live in neighbouring countries; most are hosted by low- and middle-income countries.'),
           ('Asylum seekers are illegal immigrants.', 'Seeking asylum is a legal right under international law, regardless of how a person arrives.'),
           ('Migrants only move from poor to rich countries.', 'Much migration is between low- and middle-income countries, such as within Africa or to the Gulf.')],
     cases=[('the Rohingya crisis', 'In 2017 over 700,000 Rohingya fled military violence in Myanmar\'s Rakhine State to Bangladesh, where most live in camps near Cox\'s Bazar.', 'forced migration and refugees', 'a neighbouring low-income country hosts a huge refugee population.'),
            ('Germany\'s response in 2015', 'Germany accepted over a million asylum seekers in 2015–16; by 2022 more than half of those who arrived were in employment, according to IAB research.', 'refugee policy and integration', 'a host country\'s policy choices shaped both integration and political debate.')],
     evaluate=[('Rich countries should accept more refugees.', ['they have greater resources and an obligation under the Refugee Convention', 'responsibility is currently shared unequally, with poorer neighbours hosting most'], ['public opinion and integration capacity may limit numbers', 'aid to host countries near conflicts may help more people'], 'There is a strong case for fairer responsibility-sharing, through both resettlement and financial support for host countries.')],
     src=[('Speech (paraphrased)', 'The German chancellor told journalists that Germany was a strong country and that the country had managed so much already that it would manage this too, referring to the arrival of large numbers of refugees.', 'Paraphrase of Angela Merkel, summer press conference, Berlin, 31 August 2015', 'to reassure the public and justify Germany\'s open response', 'It shows the government\'s stated position at a key moment.', 'It is a political statement intended to build support; it does not show public opinion or outcomes.', 'Germany could successfully cope with the arrival of refugees.')],
     rq=[('How far have refugees who arrived in Germany in 2015–16 integrated into the labour market by 2022?', 'Are refugees good?', 'it is a vague value question', 'It investigates a measurable outcome of migration policy.', 'Use IAB employment data, government reports and two studies; compare groups; evaluate sources; cite in APA.')])
series('ch10-st3', [('the number of refugees under UNHCR mandate', 'million', 2012, 10.5, 2023, 31.6, 'UNHCR'),
                    ('the number of international migrants', 'million', 2000, 173, 2020, 281, 'UN DESA')], d=(1, 4))


K.st('ch10-st4', 'population policies: China\'s one-child policy and India\'s family planning',
     terms=[('population policy', 'a government strategy to influence population size, growth or structure'),
            ('anti-natalist policy', 'a policy that aims to reduce the birth rate'),
            ('pro-natalist policy', 'a policy that aims to increase the birth rate, such as France\'s family allowances'),
            ('one-child policy', 'China\'s policy (1980–2015) limiting most urban couples to one child'),
            ('sex ratio at birth', 'the number of male births per 100 female births; about 105 is natural'),
            ('National Family Planning Programme', 'India\'s programme, launched in 1952, the first national family planning programme in the world')],
     facts=[('When did China officially replace the one-child policy with a two-child policy?', '2015 (effective 2016)', ['1980', '2000', '2021'], 'A three-child policy followed in 2021.'),
            ('In which year did India launch the world\'s first national family planning programme?', '1952', ['1947', '1975', '2000'], 'It focused on health and contraception.'),
            ('What controversial measure was used during India\'s Emergency (1975–77)?', 'Mass sterilisation campaigns, including coercion', ['A one-child law', 'Free university education', 'A ban on marriage'], 'About 8 million sterilisations occurred in 1976–77.'),
            ('China\'s sex ratio at birth peaked at about what in the late 2000s?', 'About 118 boys per 100 girls', ['About 100 boys per 100 girls', 'About 90 boys per 100 girls', 'About 150 boys per 100 girls'], 'A natural ratio is about 105.'),
            ('Which Indian state reached below-replacement fertility in the late 1980s, mainly through education and health?', 'Kerala', ['Bihar', 'Uttar Pradesh', 'Rajasthan'], 'Its TFR is about 1.8.')],
     why=[('Explain why China introduced the one-child policy in 1980.', 'Leaders feared that rapid population growth would prevent economic modernisation and strain food and resources, so they aimed to cap the population at about 1.2 billion by 2000.'),
          ('Explain why the one-child policy led to an imbalanced sex ratio.', 'A cultural preference for sons, combined with a one-child limit, led some families to use sex-selective abortion or abandon girls.'),
          ('Explain why China relaxed the one-child policy.', 'The policy contributed to rapid ageing, a shrinking workforce and a gender imbalance, threatening economic growth and pension systems.'),
          ('Explain why education for women can reduce birth rates more effectively than coercive policies.', 'Educated women marry later, have more economic opportunities, better health knowledge and more control over family size, so fertility falls voluntarily.')],
     contrast=[('China\'s one-child policy', 'India\'s family planning approach', 'China used strict limits enforced by fines and pressure; India mostly used voluntary measures (except during the Emergency), focusing on contraception, health and incentives.'),
               ('anti-natalist policies', 'pro-natalist policies', 'Anti-natalist policies aim to reduce births, as in China after 1980; pro-natalist policies aim to raise births, as in France, Hungary and now China.')],
     misc=[('The one-child policy applied equally to everyone in China.', 'Many rural families could have a second child if the first was a girl, and ethnic minorities were often exempt.'),
           ('The one-child policy alone caused China\'s fertility decline.', 'Fertility had already fallen from about 5.8 to 2.7 in the 1970s through the "later, longer, fewer" campaign; development also reduced fertility.'),
           ('India\'s population is still growing as fast as in the 1970s.', 'India\'s total fertility rate fell to about 2.0 by 2019–21, below replacement level.')],
     cases=[('the "later, longer, fewer" campaign', 'From 1971 China encouraged later marriage, longer gaps between births and fewer children; fertility roughly halved before the one-child policy.', 'policy before the one-child policy', 'a less coercive campaign had already reduced fertility.'),
            ('Kerala\'s fertility decline', 'With high female literacy and good health care, Kerala\'s fertility fell below replacement level without coercion.', 'development-led fertility decline', 'social development can reduce birth rates voluntarily.')],
     evaluate=[('China\'s one-child policy was a success.', ['it may have prevented hundreds of millions of births and eased pressure on resources', 'it supported rapid economic growth'], ['fertility was already falling; development explains much of the decline', 'it caused human rights abuses, a gender imbalance and rapid ageing'], 'It achieved its numerical aim, but at high human and demographic cost, and similar declines were achieved elsewhere without coercion, so "success" is highly questionable.')],
     src=[('Academic article (paraphrased)', 'The authors argued that China\'s fertility had already fallen sharply in the 1970s before the one-child policy, and that the policy\'s additional effect on population size was much smaller than officially claimed, while its social costs were very large.', 'Paraphrase of Wang Feng, Yong Cai and Baochang Gu, "Population, Policy, and Politics: How Will History Judge China\'s One-Child Policy?", Population and Development Review, 2013', 'to reassess the policy\'s effects using demographic data', 'It is a peer-reviewed study by demographers, including Chinese scholars.', 'Estimating births "prevented" depends on assumptions about what would have happened without the policy.', 'The one-child policy\'s demographic effect was overstated and its costs were high.')],
     rq=[('How far did the one-child policy, rather than economic development, cause China\'s fertility decline between 1980 and 2000?', 'What was the one-child policy?', 'it is a definition question', 'It weighs policy against other causes using data.', 'Use UN and Chinese census data, two studies and compare with Thailand or South Korea; evaluate sources; cite in APA.')])
C.natural_increase(K, 'ch10-st4', c='C3', d=(2, 4))
series('ch10-st4', [('China\'s total fertility rate', 'children per woman', 1970, 5.8, 1979, 2.7, 'UN WPP'),
                    ('India\'s population', 'million', 1951, 361, 2011, 1_211, 'Census of India')], d=(1, 3))

# =============================================================================================
# ch11 Governance, Power and Citizenship
# =============================================================================================
K.st('ch11-st1', 'political systems and sovereignty: democracy, authoritarianism and the role of the United Nations',
     terms=[('sovereignty', 'the supreme authority of a state to govern itself without outside interference'),
            ('democracy', 'a system of government in which citizens choose leaders in free and fair elections, with protected rights and the rule of law'),
            ('authoritarianism', 'a system in which power is concentrated in a leader or small group not accountable to the people'),
            ('rule of law', 'the principle that everyone, including the government, is subject to and equal before the law'),
            ('separation of powers', 'the division of government into legislative, executive and judicial branches to prevent abuse of power'),
            ('Responsibility to Protect (R2P)', 'the principle, endorsed in 2005, that the international community should act when a state fails to protect its people from genocide and mass atrocities')],
     facts=[('Which 1648 treaties are often seen as establishing the modern principle of state sovereignty?', 'The Peace of Westphalia', ['the Treaty of Versailles', 'the Treaty of Rome', 'the Treaty of Tordesillas'], 'They ended the Thirty Years\' War.'),
            ('How many member states does the UN have?', '193', ['51', '100', '250'], 'South Sudan joined in 2011.'),
            ('Which UN principle, endorsed at the 2005 World Summit, concerns protecting populations from atrocities?', 'Responsibility to Protect', ['Non-alignment', 'Containment', 'Détente'], 'It was invoked for Libya in 2011.'),
            ('Which organisation publishes the annual "Freedom in the World" report?', 'Freedom House', ['the WTO', 'the IMF', 'NATO'], 'It rates political rights and civil liberties.'),
            ('Which country is the world\'s largest democracy by number of voters?', 'India', ['the United States', 'Indonesia', 'Brazil'], 'About 970 million were eligible to vote in 2024.')],
     why=[('Explain why the separation of powers protects democracy.', 'Dividing power between legislature, executive and courts allows each to check the others, preventing any one branch from abusing power.'),
          ('Explain why sovereignty can conflict with the protection of human rights.', 'States claim the right to govern without interference, but when they abuse their own people, outside intervention to protect rights challenges that sovereignty.'),
          ('Explain why some authoritarian regimes hold elections.', 'Elections can give a claim to legitimacy, identify opponents and satisfy international pressure, while results are controlled through restrictions on media and opposition.'),
          ('Explain why the UN often struggles to act in conflicts.', 'Security Council action requires agreement among the five permanent members, any of whom can veto, and the UN depends on member states for troops and funds.')],
     contrast=[('democracy', 'authoritarianism', 'In a democracy citizens choose and can remove leaders, and rights are protected; in authoritarian systems power is concentrated and opposition, media and courts are controlled.'),
               ('a presidential system', 'a parliamentary system', 'In a presidential system (USA) the president is separately elected and not part of the legislature; in a parliamentary system (UK, India) the government comes from and is accountable to parliament.')],
     misc=[('Any country that holds elections is a democracy.', 'Elections must be free and fair, with protected rights, a free press and independent courts; many authoritarian states hold elections.'),
           ('The UN is a world government that can overrule states.', 'The UN is an organisation of sovereign states; only the Security Council can make binding decisions, and enforcement depends on members.'),
           ('Sovereignty means a state can do anything within its borders.', 'International law, human rights treaties and R2P place limits on how states may treat people.')],
     cases=[('the NATO intervention in Libya (2011)', 'The Security Council authorised measures to protect civilians (Resolution 1973); NATO air strikes helped rebels overthrow Gaddafi, but the country then fell into prolonged conflict.', 'Responsibility to Protect', 'it shows both the use and the controversy of R2P.'),
            ('India\'s 2024 general election', 'About 640 million votes were cast in seven phases over six weeks, organised by the independent Election Commission.', 'democratic processes', 'it shows the scale of democratic participation in the world\'s largest democracy.')],
     evaluate=[('The United Nations is an effective protector of international peace.', ['peacekeeping missions have reduced violence in many conflicts', 'it provides a forum for diplomacy and legitimacy'], ['the veto has blocked action in Syria and Ukraine', 'it failed to prevent genocide in Rwanda and Srebrenica'], 'The UN has helped maintain peace in many cases, but its effectiveness is limited by great-power politics and dependence on members.')],
     src=[('Report (paraphrased)', 'The commission argued that state sovereignty implies responsibility, and that when a population is suffering serious harm and the state is unwilling or unable to stop it, the principle of non-intervention yields to the international responsibility to protect.', 'Paraphrase of International Commission on Intervention and State Sovereignty, The Responsibility to Protect, Ottawa, 2001', 'to reconcile sovereignty with humanitarian intervention after Rwanda and Kosovo', 'It shaped the principle later endorsed by the UN.', 'It sets out principles but critics fear powerful states may use it for their own ends.', 'Sovereignty includes a responsibility to protect people; if a state fails, others must act.')],
     rq=[('How far did the Responsibility to Protect justify the 2011 intervention in Libya?', 'What is democracy?', 'it is a definition question', 'It evaluates a principle of global governance in a real case.', 'Use UN resolutions, NATO statements, reports and two analyses; compare perspectives; evaluate sources; cite in APA.')])
C.electoral(K, 'ch11-st1', d=(3, 5))


K.st('ch11-st2', 'global governance: international organisations, NGOs and international law',
     terms=[('global governance', 'the institutions, rules and processes through which countries and other actors cooperate on global issues'),
            ('intergovernmental organisation (IGO)', 'an organisation of member states, such as the UN, WHO or WTO'),
            ('non-governmental organisation (NGO)', 'a non-profit organisation independent of government, such as Médecins Sans Frontières or Amnesty International'),
            ('international law', 'the rules and treaties that govern relations between states'),
            ('International Court of Justice (ICJ)', 'the UN court in The Hague that settles disputes between states'),
            ('soft power', 'the ability to influence others through attraction, culture and values rather than force')],
     facts=[('Which UN agency led the global campaign that eradicated smallpox by 1980?', 'The World Health Organization (WHO)', ['UNESCO', 'the IMF', 'the WTO'], 'The last natural case was in Somalia in 1977.'),
            ('Which NGO won the Nobel Peace Prize in 1999 for medical humanitarian work?', 'Médecins Sans Frontières', ['Greenpeace', 'WWF', 'the Red Cross'], 'Founded in France in 1971.'),
            ('Which court settles legal disputes between states?', 'The International Court of Justice', ['the International Criminal Court', 'the European Court of Human Rights', 'the US Supreme Court'], 'Based in the Peace Palace in The Hague.'),
            ('Which 1987 agreement to protect the ozone layer is often called the most successful environmental treaty?', 'The Montreal Protocol', ['the Kyoto Protocol', 'the Paris Agreement', 'the Rio Declaration'], 'It phased out CFCs; all UN members ratified it.'),
            ('Who coined the term "soft power"?', 'Joseph Nye', ['Henry Kissinger', 'Hans Morgenthau', 'Woodrow Wilson'], 'In 1990.')],
     why=[('Explain why global governance is needed.', 'Problems such as climate change, pandemics, trade and conflict cross borders and cannot be solved by one state alone.'),
          ('Explain why NGOs can be effective in global governance.', 'They are flexible, have expertise and local networks, can raise public awareness and pressure governments, and are seen as independent.'),
          ('Explain why the Montreal Protocol succeeded where climate agreements have struggled.', 'CFC substitutes were available and affordable, a small number of industries were involved, the science was clear, and a fund helped developing countries comply.'),
          ('Explain why international law is difficult to enforce.', 'There is no world police; enforcement depends on states\' consent, sanctions and reputation, and powerful states can ignore rulings.')],
     contrast=[('an IGO', 'an NGO', 'An IGO is made up of member states, such as the WHO; an NGO is independent of governments, such as Amnesty International.'),
               ('the ICJ', 'the ICC', 'The ICJ settles disputes between states; the ICC prosecutes individuals for genocide, war crimes and crimes against humanity.')],
     misc=[('International organisations can force states to obey them.', 'Most depend on state cooperation; only the UN Security Council can impose binding measures, and enforcement is limited.'),
           ('NGOs are always neutral and representative.', 'NGOs have their own agendas, funders and accountability issues, and many are based in rich countries.'),
           ('Global governance means a single world government.', 'It is a complex network of states, IGOs, NGOs, businesses and treaties.')],
     cases=[('smallpox eradication', 'The WHO\'s Intensified Eradication Programme (1967–1980) used surveillance and ring vaccination; smallpox was declared eradicated in 1980.', 'successful global cooperation', 'states cooperated even during the Cold War to eliminate a disease.'),
            ('the Montreal Protocol', 'Signed in 1987, it phased out CFCs; the ozone layer is projected to recover to 1980 levels around 2066 over Antarctica.', 'effective international law', 'a treaty with universal participation reversed an environmental threat.')],
     evaluate=[('NGOs are more effective than intergovernmental organisations in addressing global problems.', ['NGOs respond quickly, have local knowledge and can campaign freely', 'MSF and Amnesty have achieved significant impacts'], ['IGOs have legitimacy, resources and the ability to create binding law', 'NGOs lack enforcement power and depend on donations'], 'NGOs and IGOs have complementary strengths; the most effective responses, such as smallpox eradication, often combine both.')],
     src=[('Report (paraphrased)', 'The assessment found that the Montreal Protocol had led to the phase-out of nearly 99% of banned ozone-depleting substances, and that the ozone layer was on track to recover to 1980 values by around 2040 for most of the world, and later over the poles.', 'Paraphrase of WMO/UNEP Scientific Assessment of Ozone Depletion: 2022', 'to assess progress under the Montreal Protocol for governments', 'It is a scientific assessment by hundreds of experts.', 'It focuses on the ozone layer; projections depend on continued compliance.', 'The Montreal Protocol is working and the ozone layer is recovering.')],
     rq=[('Why was the Montreal Protocol more successful than the Kyoto Protocol in achieving its aims?', 'What is global governance?', 'it is a definition question', 'It compares two treaties to analyse what makes global governance effective.', 'Use treaty texts, emissions and CFC data and two analyses; compare factors; evaluate sources; cite in APA.')])
series('ch11-st2', [('global consumption of ozone-depleting substances', 'thousand ODP tonnes', 1989, 1_800, 2014, 30, 'approx., UNEP')], d=(1, 3))


K.st('ch11-st3', 'active citizenship: protest, the media and digital participation',
     terms=[('active citizenship', 'participating in the life of a community and society, for example by voting, volunteering, campaigning or protesting'),
            ('civil disobedience', 'deliberately and non-violently breaking a law to protest against injustice'),
            ('misinformation', 'false or misleading information spread without intent to deceive; disinformation is spread deliberately'),
            ('echo chamber', 'an environment in which people encounter only views that reinforce their own'),
            ('digital activism', 'using digital tools such as social media and petitions for political or social campaigns'),
            ('media literacy', 'the ability to access, analyse and evaluate media critically')],
     facts=[('Which 2010–12 wave of protests across the Middle East and North Africa used social media to organise?', 'The Arab Spring', ['the Velvet Revolution', 'the Prague Spring', 'the Salt March'], 'It began in Tunisia in December 2010.'),
            ('What form did the 2020–21 Indian farmers\' protest against three farm laws mainly take?', 'Farmers camped at Delhi\'s borders for about a year', ['A one-day strike', 'An online petition only', 'A court case only'], 'The laws were repealed in November 2021.'),
            ('Which 2018 movement began with Greta Thunberg striking from school?', 'Fridays for Future', ['Black Lives Matter', 'Occupy Wall Street', 'Me Too'], 'It spread to over 100 countries.'),
            ('Which movement grew globally after the killing of George Floyd in Minneapolis in May 2020?', 'Black Lives Matter', ['Extinction Rebellion', 'Solidarity', 'Chipko'], 'Protests took place in about 60 countries.'),
            ('Which press freedom organisation ranks countries in an annual index?', 'Reporters Without Borders', ['the World Bank', 'FIFA', 'OPEC'], 'The World Press Freedom Index covers 180 countries.')],
     why=[('Explain why social media has changed political participation.', 'It lets people share information instantly, organise protests and reach global audiences without traditional media, but it can also spread misinformation and enable surveillance.'),
          ('Explain why a free press is essential for active citizenship.', 'Citizens need accurate information to make decisions, and journalists hold the powerful to account by investigating wrongdoing.'),
          ('Explain why mass protests can lead to political change.', 'They show the scale of public feeling, disrupt normal life, attract media attention and pressure leaders, especially when sustained and non-violent.'),
          ('Explain why digital activism is sometimes criticised as "slacktivism".', 'Clicking "like" or signing petitions requires little effort and may not translate into sustained action or real change.')],
     contrast=[('misinformation', 'disinformation', 'Misinformation is false information spread without intent to deceive; disinformation is spread deliberately to mislead.'),
               ('traditional media', 'social media', 'Traditional media (newspapers, TV) has editors and professional standards; social media lets anyone publish instantly, with less verification.')],
     misc=[('Social media always promotes democracy.', 'It can mobilise protest but also spreads disinformation, enables surveillance and can be used by authoritarian governments.'),
           ('Protests rarely achieve anything.', 'Research by Erica Chenoweth found that non-violent campaigns succeeded about twice as often as violent ones between 1900 and 2006.'),
           ('Active citizenship means only voting.', 'It includes volunteering, campaigning, community work, informed debate and peaceful protest.')],
     cases=[('the Indian farmers\' protest (2020–21)', 'Tens of thousands of farmers, mainly from Punjab and Haryana, camped on Delhi\'s borders for about a year; in November 2021 the government repealed three farm laws.', 'sustained non-violent protest', 'prolonged mass mobilisation led to a reversal of policy.'),
            ('the Arab Spring in Tunisia', 'Protests after the self-immolation of Mohamed Bouazizi in December 2010 forced President Ben Ali to flee in January 2011; Tunisia held free elections later that year.', 'protest and the media', 'social media and satellite TV helped spread protests and topple a long-time ruler.')],
     evaluate=[('Social media has done more to strengthen democracy than to weaken it.', ['it helped organise the Arab Spring and global movements', 'it gives voice to marginalised groups'], ['disinformation and echo chambers polarise debate', 'authoritarian states use it for surveillance and propaganda'], 'Social media has empowered citizens but also created serious threats; its effect depends on regulation, media literacy and political context.')],
     src=[('Academic study (paraphrased)', 'The researchers found that between 1900 and 2006 non-violent resistance campaigns were about twice as likely to succeed as violent campaigns, partly because they attracted wider participation and caused defections among security forces.', 'Paraphrase of Erica Chenoweth and Maria J. Stephan, Why Civil Resistance Works, New York, 2011', 'to analyse the effectiveness of non-violent and violent resistance', 'It is based on a large dataset of campaigns worldwide.', 'Definitions of "success" and categorising campaigns involve judgement; more recent campaigns have been less successful.', 'Non-violent resistance is more effective than violent resistance.')],
     rq=[('How did social media contribute to the success of protests in Tunisia in 2010–11?', 'Does protest work?', 'it is a vague, closed question', 'It investigates the role of media in a specific political change.', 'Use news reports, social media data studies and two analyses; compare with satellite TV; evaluate sources; cite in APA.')])

# =============================================================================================
# ch12 Inquiry Skills and eAssessment Preparation
# =============================================================================================
K.st('ch12-st1', 'formulating a research question and planning an investigation (Criterion B)',
     terms=[('research question', 'a focused, open question that guides an investigation and can be answered with evidence'),
            ('action plan', 'a detailed plan of the steps, sources, methods and timeline for an investigation'),
            ('methodology', 'the methods used to collect and analyse information, such as surveys, interviews or document analysis'),
            ('primary research', 'collecting original data, for example through surveys, interviews or fieldwork'),
            ('ethical research', 'research that respects participants\' consent, privacy and wellbeing and acknowledges sources honestly'),
            ('reflection', 'evaluating the process and results of an investigation and how it could be improved')],
     facts=[('Which criterion in MYP Individuals and Societies assesses the research question, action plan and evaluation of the process?', 'Criterion B: Investigating', ['Criterion A', 'Criterion C', 'Criterion D'], 'B also covers using methods to collect information.'),
            ('Which is the strongest research question?', 'To what extent did the 2005 Right to Information Act reduce corruption in rural employment schemes in Rajasthan by 2015?', ['What is corruption?', 'Is India corrupt?', 'Why are laws good?'], 'It is focused, open and researchable.'),
            ('What should a researcher obtain before interviewing people?', 'Informed consent', ['Their bank details', 'Their passwords', 'A fee'], 'Participants must know how their information will be used.'),
            ('What does a good action plan include?', 'Steps, sources, methods and deadlines', ['Only the final conclusion', 'Only a title', 'Only the bibliography'], 'It makes the investigation manageable.'),
            ('Which command term asks students to give valid reasons or evidence for an answer?', 'Justify', ['State', 'Outline', 'Identify'], 'Justify the relevance of a research question.')],
     why=[('Explain why a research question should be open and focused.', 'An open question requires analysis rather than a yes/no answer, and a focused one sets clear limits of place, time and issue so it can be answered in depth.'),
          ('Explain why an investigation should use more than one research method.', 'Different methods give different kinds of evidence; combining them allows triangulation and reduces the limitations of any one method.'),
          ('Explain why researchers evaluate their process.', 'Reflecting on what worked and what did not helps assess how reliable the findings are and how future investigations could be improved.'),
          ('Explain why ethical considerations matter in research.', 'Participants must be protected from harm, their privacy respected and their consent obtained; academic honesty requires acknowledging sources.')],
     contrast=[('primary research', 'secondary research', 'Primary research collects original data, such as a survey; secondary research uses existing sources, such as reports and books.'),
               ('quantitative data', 'qualitative data', 'Quantitative data are numerical, such as statistics; qualitative data are descriptive, such as interview responses.')],
     misc=[('An action plan should never change.', 'Plans should be reviewed and adjusted as research reveals new information or problems.'),
           ('Using more sources always makes an investigation better.', 'Quality, relevance and range of sources matter more than quantity.'),
           ('A research question should be as broad as possible.', 'Broad questions lead to superficial answers; focus allows depth.')],
     cases=[('a student inquiry into Delhi\'s air pollution', 'A student refined "Why is Delhi polluted?" to "How far does crop-stubble burning in Punjab explain Delhi\'s air pollution peaks in November, 2016–2023?"', 'refining a research question', 'adding a factor, place and period made the question focused and testable.'),
            ('a community survey on plastic use', 'Students designed a questionnaire for their neighbourhood, piloted it with ten people, then revised unclear questions.', 'planning and methodology', 'piloting improved the reliability of primary data.')],
     evaluate=[('Primary research is more valuable than secondary research in an MYP investigation.', ['it produces original, specific data', 'it develops investigating skills'], ['samples are often small and unrepresentative', 'secondary sources provide context and expert analysis'], 'Both are valuable; the strongest investigations combine primary data with high-quality secondary sources.')],
     src=[('Methodology guide (paraphrased)', 'The guide advised that a pilot study – a small trial of a questionnaire or interview – helps researchers find confusing questions, estimate how long data collection will take and improve the reliability of their methods.', 'Paraphrase of a university research methods guide for social science students, 2022', 'to help students plan effective primary research', 'It gives practical, evidence-based advice.', 'It is general advice not tailored to MYP investigations.', 'Piloting improves the quality and reliability of research.')],
     rq=[('How far does crop-stubble burning in Punjab explain Delhi\'s air pollution peaks in November between 2016 and 2023?', 'Why is Delhi polluted?', 'it is too broad', 'It weighs one cause against others using measurable data.', 'Use CPCB air-quality data, NASA fire maps and two studies; compare with other sources such as traffic; evaluate; cite in APA.'),
         ('To what extent did the Delhi Metro reduce road traffic in Delhi between 2002 and 2020?', 'Is the metro good?', 'it is a vague value question', 'It evaluates an urban transport policy.', 'Use ridership data, traffic counts and two studies; evaluate; cite in APA.'),
         ('How did the 2011 Fukushima disaster affect Germany\'s energy policy?', 'What happened at Fukushima?', 'it is a descriptive question', 'It investigates how an event influenced policy in another country.', 'Use government documents, energy data and two analyses; evaluate sources; cite in APA.')])
C.sampling(K, 'ch12-st1')


K.st('ch12-st2', 'evaluating sources: origin, purpose, value and limitation (OPVL)',
     terms=[('OPVL', 'a framework for evaluating sources by their origin, purpose, value and limitation'),
            ('origin', 'who created a source, when, where and in what form'),
            ('purpose', 'why the source was created and for what audience'),
            ('value', 'how useful the source is for a specific question, given its origin and purpose'),
            ('limitation', 'what reduces the source\'s usefulness, such as bias, selectivity or lack of knowledge'),
            ('corroboration', 'checking evidence against other independent sources'),
            ('historiography', 'the study of how historians\' interpretations of the past differ and change')],
     facts=[('Which criterion includes using OPVL to analyse sources in MYP Individuals and Societies?', 'Criterion D: Thinking critically', ['Criterion A', 'Criterion B', 'Criterion C'], 'D also includes interpreting perspectives.'),
            ('A Soviet propaganda poster is most valuable for which question?', 'How the Soviet government wanted to present itself', ['How Soviet citizens actually lived', 'Exact Soviet production figures', 'What US leaders thought'], 'Purpose determines value.'),
            ('Which is a limitation of a memoir written decades after events?', 'Memory may be inaccurate or shaped by later knowledge', ['It is always a forgery', 'It cannot be cited', 'It is a secondary source only'], 'Hindsight may reshape accounts.'),
            ('What is historiography?', 'The study of how historians\' interpretations differ and change', ['The study of maps', 'A type of primary source', 'A census'], 'For example orthodox and revisionist views of the Cold War.'),
            ('What does corroboration involve?', 'Comparing a source with other independent evidence', ['Copying a source', 'Translating a source', 'Ignoring contradictory sources'], 'It tests reliability.')],
     why=[('Explain why the purpose of a source affects its value.', 'A source created to persuade, such as propaganda or a campaign speech, may select or distort information, but it is valuable for understanding the creator\'s aims and audience.'),
          ('Explain why historians\' interpretations change over time.', 'New sources become available, such as Soviet archives after 1991, new methods and questions emerge, and historians are influenced by their own context.'),
          ('Explain why a source can be valuable even if it is unreliable.', 'An unreliable source can still reveal attitudes, beliefs or propaganda techniques, which may be what the investigation is about.'),
          ('Explain why evaluating sources is essential before using them as evidence.', 'Without considering origin and purpose, a researcher may accept biased or inaccurate information and reach invalid conclusions.')],
     contrast=[('the value of a source', 'its limitation', 'Value is how a source helps answer a question; limitation is what reduces its usefulness for that question.'),
               ('an orthodox interpretation', 'a revisionist interpretation', 'An orthodox interpretation is the first widely accepted view; a revisionist interpretation challenges it, often using new evidence.')],
     misc=[('Primary sources are always more reliable than secondary sources.', 'Primary sources may be biased or limited; secondary sources may be more balanced, drawing on many primary sources.'),
           ('A biased source should never be used.', 'All sources have perspectives; biased sources are valuable for studying attitudes and must be used critically.'),
           ('OPVL is about summarising content.', 'OPVL evaluates the source\'s provenance and usefulness, not just what it says.')],
     cases=[('the opening of Soviet archives', 'After 1991 historians gained access to Soviet records, leading to new research on Stalin\'s decisions and the Cold War, such as John Lewis Gaddis\'s We Now Know (1997).', 'new sources changing interpretations', 'access to archives reshaped historiography.'),
            ('the "Hitler Diaries" forgery', 'In 1983 the German magazine Stern published diaries said to be Hitler\'s; forensic tests soon showed they were forgeries.', 'checking the authenticity of sources', 'the case shows the need to verify origin before using a source.')],
     evaluate=[('Primary sources are always more useful than secondary sources for historical inquiry.', ['they provide direct evidence from the time', 'they reveal contemporary attitudes'], ['secondary sources offer context, synthesis and expert analysis', 'primary sources can be partial, biased or forged'], 'Usefulness depends on the question; strong inquiry uses both, evaluating each critically.')],
     src=[('Photograph (described)', 'A black-and-white photograph shows a crowd of young people standing on the Berlin Wall at the Brandenburg Gate at night, some holding champagne bottles and others chipping at the concrete with hammers.', 'Photograph taken by a press photographer for an international news agency, Berlin, 10 November 1989', 'to record and report a major news event for newspapers worldwide', 'It provides visual evidence of the public mood immediately after the Wall opened.', 'It captures one moment and place selected by the photographer; it does not show the views of East German leaders or people elsewhere.', 'Berliners celebrated the opening of the Wall with joy and began to tear it down.')],
     rq=[('How have historians\' interpretations of the origins of the Cold War changed since the opening of Soviet archives in the 1990s?', 'Who started the Cold War?', 'it is a closed question', 'It focuses on historiography and the impact of new sources.', 'Read orthodox, revisionist and post-revisionist historians; compare arguments and evidence; evaluate; cite in MLA.')])
C.citation(K, 'ch12-st2')


K.st('ch12-st3', 'extended response writing: argument, evidence, counter-argument and conclusion (Criteria C and D)',
     terms=[('thesis', 'a clear statement of the main argument that answers the question'),
            ('counter-argument', 'an opposing view that the writer acknowledges and responds to'),
            ('evidence', 'specific facts, data, examples or quotations that support a point'),
            ('synthesis', 'combining ideas and evidence from different sources into a coherent argument'),
            ('judgement', 'a reasoned conclusion that weighs the arguments and answers the question'),
            ('signposting', 'words and phrases that guide the reader through an argument, such as "however", "furthermore" and "therefore"')],
     facts=[('Which command term requires weighing strengths and limitations to reach a judgement?', 'Evaluate', ['State', 'Identify', 'Outline'], 'It is assessed in Criterion D.'),
            ('What does "to what extent" require?', 'Considering the merits of an argument and reaching a judgement on how far it is valid', ['Listing facts only', 'Defining a term only', 'Describing a picture'], 'A balanced, reasoned conclusion is needed.'),
            ('Where should the main argument normally be stated in an essay?', 'In the introduction, as a thesis', ['Only in the bibliography', 'Only in the title', 'Nowhere'], 'It is then developed throughout.'),
            ('Which criterion assesses organisation, communication and referencing?', 'Criterion C: Communicating', ['Criterion A', 'Criterion B', 'Criterion D'], 'Including structure and style.'),
            ('What is the best way to include a counter-argument?', 'Present it fairly, then explain why it is weaker or how it modifies your argument', ['Ignore it', 'Mention it only in the bibliography', 'Agree with every view equally without a judgement'], 'This shows critical thinking.')],
     why=[('Explain why a strong essay includes counter-arguments.', 'Acknowledging and responding to opposing views shows understanding of complexity and strengthens the writer\'s judgement.'),
          ('Explain why specific evidence is more convincing than general statements.', 'Precise dates, figures, examples and quotations show knowledge and allow the reader to check and trust the argument.'),
          ('Explain why a conclusion should reach a clear judgement.', 'Questions such as "to what extent" or "evaluate" require a decision; a judgement shows the writer has weighed the evidence.'),
          ('Explain why planning an essay improves its quality.', 'Planning organises points logically, ensures balance and relevance and saves time in an exam.')],
     contrast=[('analysis', 'description', 'Description states what happened; analysis explains why or how and examines significance and relationships.'),
               ('a balanced essay', 'a sitting-on-the-fence essay', 'A balanced essay weighs different views and then reaches a reasoned judgement; sitting on the fence presents views without deciding.')],
     misc=[('Including as many facts as possible gets the highest marks.', 'Marks reward relevant, analysed evidence supporting an argument, not a list of facts.'),
           ('A counter-argument weakens your essay.', 'Engaging with counter-arguments shows critical thinking and makes the final judgement more convincing.'),
           ('The conclusion should introduce new evidence.', 'The conclusion should weigh the arguments already made and answer the question.')],
     cases=[('a model essay on appeasement', 'A student argued that appeasement was a reasonable policy in 1938, using rearmament statistics, then considered Churchill\'s criticisms before concluding that it was understandable but encouraged Hitler.', 'argument and counter-argument', 'the essay reached a nuanced judgement by weighing evidence.'),
            ('an eAssessment extended response', 'In an MYP eAssessment task, students had to evaluate a policy using two sources and their own knowledge, with marks for the argument, use of sources and judgement.', 'synthesis of sources and knowledge', 'high-scoring answers combine sources with outside knowledge in a clear argument.')],
     evaluate=[('A clear thesis is the most important feature of an extended response.', ['it gives the essay direction and focus', 'it shows the writer is answering the question'], ['evidence and analysis are needed to support it', 'counter-arguments and a judgement show critical thinking'], 'A clear thesis is essential, but it must be supported by evidence, analysis and engagement with other views to produce a strong response.')],
     src=[('Assessment guidance (paraphrased)', 'The guidance stated that the highest-scoring responses present a sustained, well-supported argument that consistently addresses the question, use relevant and accurate evidence, consider different perspectives and reach a well-reasoned conclusion.', 'Paraphrase of typical IB MYP Individuals and Societies eAssessment markband descriptors for extended response tasks', 'to explain to teachers and students how extended responses are assessed', 'It shows directly what examiners reward.', 'It describes standards in general terms; applying them requires examples.', 'Strong responses are sustained, supported, balanced and reach a reasoned conclusion.')],
     rq=[('To what extent was the Marshall Plan motivated by US economic self-interest rather than humanitarian concern?', 'What was the Marshall Plan?', 'it is a definition question', 'It requires weighing motives and perspectives in an extended argument.', 'Use speeches, US congressional debates, trade data and two historians; plan argument and counter-argument; cite in MLA.')])
C.graph_choice(K, 'ch12-st3')


K.st('ch12-st4', 'eAssessment practice: source engagement, investigation and extended-response tasks',
     terms=[('eAssessment', 'the on-screen examination for MYP year 5, with tasks testing all four criteria'),
            ('command term', 'a word in a question that tells you what to do, such as outline, explain, analyse or evaluate'),
            ('stimulus', 'material such as a text, map, graph, image or video provided in an exam for analysis'),
            ('markband', 'a level of performance described in the assessment criteria'),
            ('time management', 'planning how long to spend on each task according to its marks'),
            ('interdisciplinary', 'combining knowledge and methods from different subjects, such as history, geography and economics')],
     facts=[('How long is the MYP Individuals and Societies on-screen examination?', '2 hours', ['30 minutes', '5 hours', '1 day'], 'It is assessed against all four criteria.'),
            ('Which command term asks you to give a brief account or summary?', 'Outline', ['Evaluate', 'Justify', 'Discuss'], 'Outline requires main points only.'),
            ('Which command term requires considering a range of arguments and reaching a conclusion?', 'Discuss', ['State', 'Identify', 'Define'], 'Often with evidence.'),
            ('In an exam, how should time be allocated?', 'In proportion to the marks available', ['Equally to every question', 'Mostly to the first question', 'Only to the essay'], 'Roughly 1.5 minutes per mark in a 2-hour, 80-mark exam.'),
            ('Which command term asks you to break down information to bring out its structure and relationships?', 'Analyse', ['State', 'List', 'Name'], 'Analyse is a Criterion D term.')],
     why=[('Explain why understanding command terms is important in the eAssessment.', 'Each command term sets the depth and type of response required; misreading "evaluate" as "describe" leads to answers that cannot reach higher markbands.'),
          ('Explain why stimulus material should be used explicitly in answers.', 'Questions often require analysis of the source; referring to specific details shows understanding and earns marks for source engagement.'),
          ('Explain why planning is important even under time pressure.', 'A short plan ensures a clear argument, relevant evidence and balance, and prevents running out of time on extended responses.'),
          ('Explain why the eAssessment combines history, geography and economics.', 'MYP Individuals and Societies is an integrated subject, so tasks test the ability to apply concepts across disciplines to real-world issues.')],
     contrast=[('"explain"', '"evaluate"', '"Explain" requires reasons or causes; "evaluate" requires weighing strengths and limitations to reach a judgement.'),
               ('a source-based task', 'an extended-response task', 'A source-based task analyses provided material; an extended-response task requires a sustained argument using knowledge and sometimes sources.')],
     misc=[('The longest answer always earns the highest marks.', 'Marks depend on meeting the command term and criteria; focused, relevant answers score better than long, unfocused ones.'),
           ('You can ignore the sources in a source-based question if you know the topic.', 'Source-based questions require explicit use of the sources; own knowledge supports but does not replace them.'),
           ('All questions should get equal time.', 'Time should be allocated according to marks.')],
     cases=[('an eAssessment investigation task', 'Students were shown a video and data on urban flooding in Jakarta and asked to formulate a research question and outline an action plan.', 'Criterion B in the exam', 'the task tests investigating skills on an unfamiliar case.'),
            ('a source-comparison task', 'Students compared a government statement and an NGO report on a dam project, analysing origin, purpose, value and limitations.', 'Criterion D in the exam', 'the task tests evaluation of different perspectives.')],
     evaluate=[('On-screen examinations are a fair way to assess MYP Individuals and Societies.', ['they test all criteria with varied, real-world stimulus', 'they are standardised and externally moderated'], ['they test skills under time pressure rather than sustained inquiry', 'students\' typing skills and access to technology vary'], 'eAssessment offers a standardised measure of key skills, but it complements rather than replaces the sustained inquiry assessed in coursework.')],
     src=[('Data source (described)', 'A table compares four countries\' GDP per capita, life expectancy, mean years of schooling and HDI for 2022, using UNDP data. It shows that two countries with similar GDP per capita have different HDI values.', 'Table compiled from United Nations Development Programme, Human Development Report 2023/24', 'to present comparable development indicators for analysis', 'It uses an authoritative, standardised international data set.', 'Indicators are national averages that hide inequality, and data for some countries are estimates.', 'Income alone does not determine human development.')],
     rq=[('How far do differences in public health spending explain differences in life expectancy between Kerala and Uttar Pradesh?', 'Which Indian state is best?', 'it is a vague value question', 'It investigates a development issue using comparable data.', 'Use NFHS and state budget data and two studies; compare indicators; evaluate data; cite in APA.')])
C.per_capita(K, 'ch12-st4', GDP_ROWS, c=('C3',), d=(2, 4))
C.citation(K, 'ch12-st4', c='C3', d=(2, 3))
