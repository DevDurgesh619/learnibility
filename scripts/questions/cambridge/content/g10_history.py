"""Cambridge IGCSE History 0470, year 2 (grade 10): the five depth studies of Option B
(First World War; Germany 1918-45; Russia 1905-41; USA 1919-41; Second World War) plus
coursework / Paper 4 skills.

Uses the knowledge-pack builders of g9_history: Paper 1 depth-study questions (a) describe [4],
(b) explain [6], (c) 'How far' / 'How important' [10]; Paper 2-style source work; recall, chronology
and claim-checking items; plus topic data templates (election results, inflation, output, unemployment).
Sources are either well-attested words (quoted or summarised, marked as such) or labelled
'illustrative' and attributed to unnamed writers; no invented words are given to real people.
"""
from ._lib import mcq, CTX
from .g9_history import (build, S, T, packs, finalize, PROFILE, _mins, _dot, cap, low2, _kw, a_key, c_key, c_ans, _c_stem,
                         _src_intro, _src_parts, _compose_src, USE_KEY, CMP_KEY)

PROFILE = dict(PROFILE, mark_scale={'short': (2, 2), 'long': (2.5, 1.5), 'case': (2.33, 1.5)})
CHAPTERS = {}


# ============================================================== CHAPTER 1: Depth Study A, the First World War, 1914-18

w1a = T('Why the war was not over by December 1914: the Schlieffen Plan, Mons, the Marne and the race to the sea', 'schlieffen plan', 'marne', 'race to the sea')
build(w1a, {
    'enq': 'why the war was not over by Christmas 1914', 'claim': 'the Schlieffen Plan failed mainly because of Belgian and British resistance',
    'stim': ['In August 1914 German armies advanced through Belgium into France according to the Schlieffen Plan.', 'Many people in 1914 expected the war to be over by Christmas.',
             'By December 1914 a line of trenches stretched from the Channel coast to Switzerland.'],
    'terms': [
        ('Schlieffen Plan', 'Germany\'s plan to defeat France in about six weeks by attacking through Belgium, before turning against Russia'),
        ('BEF', 'the British Expeditionary Force, the small professional army sent to France in August 1914'),
        ('race to the sea', 'the series of attempts by each side in autumn 1914 to outflank the other, moving north towards the Channel coast'),
        ('mobilisation', 'calling up reserves and moving armies into position for war'),
        ('outflank', 'to go round the side of an enemy\'s line in order to attack it from the side or rear'),
        ('stalemate', 'a situation in which neither side can win or make progress'),
    ],
    'dates': [('Germany invaded Belgium', 1914, 8.04), ('the BEF fought the Battle of Mons', 1914, 8.23), ('Russia was defeated at the Battle of Tannenberg', 1914, 8.30),
              ('the First Battle of the Marne began', 1914, 9.06), ('the First Battle of Ypres began', 1914, 10.19), ('the Schlieffen Plan was first drawn up', 1905)],
    'mcq': [
        ('Why did the Schlieffen Plan send German troops through Belgium?', 'To avoid the strong French fortifications on the Franco-German border', ['Because Belgium had attacked Germany', 'Because Britain had asked Germany to', 'To reach the Russian border quickly'], '[1]'),
        ('Which battle in September 1914 stopped the German advance on Paris?', 'The Battle of the Marne', ['The Battle of the Somme', 'The Battle of Verdun', 'The Battle of Tannenberg'], 'French and British forces counter-attacked from 6 September. [1]'),
        ('Why did Moltke move troops from the west to the east in August 1914?', 'Russia mobilised faster than expected and invaded East Prussia', ['France had surrendered', 'Britain had invaded Germany', 'Austria-Hungary had asked for peace'], '[1]'),
        ('What was the first major battle fought by the BEF in 1914?', 'Mons', ['Ypres', 'Loos', 'Gallipoli'], '23 August 1914. [1]'),
    ],
    'a': [
        ('Describe the Schlieffen Plan.', 'features of the Schlieffen Plan',
         ['It was drawn up by Count Alfred von Schlieffen to avoid a war on two fronts', 'Most of the German army would attack France through Belgium', 'It aimed to encircle Paris and defeat France in about six weeks', 'Only a small force would hold off Russia, which was expected to mobilise slowly', 'After defeating France, troops would be moved east by rail to fight Russia']),
        ('What happened at the Battle of the Marne in September 1914?', 'events of the First Battle of the Marne',
         ['German armies under von Kluck turned east of Paris instead of encircling it', 'This exposed their flank to a counter-attack', 'French forces and the BEF attacked from 6 September', 'Reinforcements were rushed from Paris, some in taxis', 'The Germans retreated to the River Aisne and dug trenches']),
        ('Describe the race to the sea in autumn 1914.', 'features of the race to the sea',
         ['After the Marne, each side tried to outflank the other to the north', 'The armies moved towards the Channel coast', 'Neither side could get round the other', 'The First Battle of Ypres (October-November 1914) stopped the Germans reaching the Channel ports', 'By December trenches ran from the Channel to Switzerland']),
    ],
    'b': [
        ('Why did the Schlieffen Plan fail?',
         ['Belgian resistance, for example at the forts of Liège, delayed the German advance', 'The BEF slowed the Germans at Mons', 'Russia mobilised faster than expected, so Moltke sent troops east', 'Moltke had weakened the right wing of the attack', 'German troops were exhausted and supply lines were stretched', 'The French and British counter-attacked successfully at the Marne']),
        ('Why was the war not over by Christmas 1914?',
         ['The Schlieffen Plan failed to defeat France quickly', 'The Germans were stopped at the Marne and dug trenches', 'Neither side could outflank the other in the race to the sea', 'Defensive weapons such as machine guns and artillery gave the advantage to defenders', 'Russia\'s attack in the east meant Germany had to fight on two fronts']),
        ('Why was the Battle of the Marne important?',
         ['It stopped the German advance on Paris', 'It ended German hopes of a quick victory over France', 'It led to both sides digging trenches', 'It meant Germany would have to fight a long war on two fronts']),
    ],
    'claims': [
        ('The Schlieffen Plan was designed to defeat Russia first.', False, 'It aimed to defeat France first, in about six weeks, then turn on Russia.'),
        ('The BEF was a small professional army in 1914.', True, 'It was much smaller than the French and German armies, which relied on conscripts.'),
        ('By the end of 1914 the Germans had captured Paris.', False, 'They were stopped at the Marne in September 1914 and never reached Paris in that war.'),
    ],
    'c': [
        dict(q='‘The Schlieffen Plan failed mainly because of the resistance of the Belgians and the British.’',
             pro=['Belgian resistance at Liège delayed the German timetable', 'The BEF slowed the advance at Mons and fought at the Marne', 'British entry into the war was caused by the invasion of Belgium'],
             con=['Russia\'s rapid mobilisation forced Moltke to send troops east', 'Moltke had weakened the plan\'s right wing', 'German troops were exhausted and supply lines overstretched', 'The French army\'s counter-attack at the Marne was the decisive blow'],
             judge='Belgian and British resistance caused important delays, but the plan failed mainly because of its own flaws and the speed of Russian mobilisation, which led to defeat at the Marne'),
        dict(q='How important was the Battle of the Marne in explaining why the war was not over by Christmas 1914?',
             pro=['It stopped the advance on Paris and ended hopes of a quick German victory', 'It led directly to the digging of trenches on the Aisne'],
             con=['The race to the sea and First Ypres turned the line into a continuous front', 'Defensive firepower made attack very costly', 'War on two fronts meant neither side could concentrate forces'],
             judge='The Marne was the turning point that made a quick victory impossible, but defensive technology explains why the stalemate then lasted'),
    ],
    'src': [
        S('an order to the French army from General Joffre, 6 September 1914 (translated)', 'At the moment when the battle upon which hangs the fate of the country is about to begin, all must remember that the time for looking back is past; every effort must be concentrated on attacking and driving back the enemy.',
          'the Battle of the Marne', 'Joffre tells his soldiers that the battle will decide the fate of France and that they must attack and not retreat.',
          'To inspire French troops at the start of the counter-attack on the Marne.',
          'it is the commander\'s own order at the time', 'it was written to motivate soldiers, so it tells us about Joffre\'s intentions, not what happened in the battle',
          'That the Germans had exposed their flank by turning east of Paris.', stance=False, why='it suggests the French army itself played the decisive role'),
        S('a letter home from a British soldier who fought at Mons, August 1914 (illustrative)', 'They came on in great grey masses and we fired until our rifles were too hot to hold. We held them for a whole day before the order came to fall back.',
          'the role of the BEF in 1914', 'It suggests the BEF\'s rapid rifle fire held up the much larger German force at Mons.',
          'To tell his family about his experiences.',
          'it is an eyewitness account from a soldier who was there', 'he saw only his part of the battle and might exaggerate his unit\'s achievement',
          'That the BEF then had to retreat for two weeks before the Marne.', stance=True, why='it shows the BEF slowing the German advance'),
    ],
})

w1b = T('Why there was stalemate on the Western Front: trench warfare, Verdun and the Somme', 'stalemate on the western front', 'verdun', 'somme')
build(w1b, {
    'enq': 'the Battle of the Somme', 'claim': 'the Battle of the Somme was a failure for the British army',
    'stim': ['On 1 July 1916 the British army suffered about 57,000 casualties on the first day of the Battle of the Somme.', 'In February 1916 the German army attacked the French fortress town of Verdun.',
             'From 1915 to 1917 attacks on the Western Front rarely gained more than a few kilometres.'],
    'terms': [
        ('no man\'s land', 'the area between the opposing front-line trenches'),
        ('attrition', 'wearing down the enemy by continuous losses of men and materials'),
        ('creeping barrage', 'an artillery bombardment that moves forward just ahead of advancing infantry'),
        ('communication trench', 'a trench linking the front line with support and reserve trenches'),
        ('chlorine gas', 'a poison gas first used on a large scale by the Germans at Ypres in April 1915'),
        ('tank', 'an armoured vehicle on tracks, first used by the British on the Somme in September 1916'),
        ('shell shock', 'a mental illness caused by the stress of constant bombardment'),
    ],
    'dates': [('the Germans first used chlorine gas on a large scale at Ypres', 1915, 4), ('the German attack on Verdun began', 1916, 2), ('the Battle of the Somme began', 1916, 7),
              ('tanks were used for the first time', 1916, 9), ('the Battle of Passchendaele (Third Ypres) began', 1917, 7)],
    'mcq': [
        ('What was Falkenhayn\'s aim in attacking Verdun in 1916?', 'To “bleed France white” by drawing its army into a battle of attrition', ['To capture the Channel ports', 'To link up with the Austrian army', 'To invade Britain'], '[1]'),
        ('Why did the British attack on the Somme in July 1916?', 'To relieve pressure on the French at Verdun and break through German lines', ['To capture Paris', 'To help the Gallipoli landings', 'To end the British blockade'], '[1]'),
        ('Which weapon was most effective at defending trenches against infantry attack?', 'The machine gun', ['The bayonet', 'The cavalry sabre', 'The airship'], 'It could fire hundreds of rounds a minute. [1]'),
        ('Who commanded the British army during the Battle of the Somme?', 'Sir Douglas Haig', ['Sir John French', 'Ferdinand Foch', 'Erich von Falkenhayn'], 'Haig replaced French in December 1915. [1]'),
    ],
    'a': [
        ('Describe the trench system on the Western Front.', 'features of the trench system on the Western Front',
         ['There were front-line, support and reserve trenches', 'Communication trenches linked them', 'Trenches were dug in a zigzag pattern to limit blast and stop attackers firing along them', 'Barbed wire protected the front line', 'No man\'s land separated the two sides', 'Dugouts sheltered soldiers from shellfire']),
        ('What happened on the first day of the Battle of the Somme?', 'events of 1 July 1916 on the Somme',
         ['A week-long artillery bombardment failed to destroy the German wire and deep dugouts', 'British troops advanced at walking pace across no man\'s land', 'German machine gunners came out of their dugouts and opened fire', 'The British suffered about 57,000 casualties, including about 19,000 killed', 'Only small gains were made, mainly in the south']),
        ('Describe the Battle of Verdun.', 'features of the Battle of Verdun',
         ['The Germans attacked on 21 February 1916', 'Falkenhayn aimed to bleed the French army white', 'The French defended the town at enormous cost, supplied along the “Sacred Way”', 'The battle lasted until December 1916', 'Each side suffered more than 300,000 casualties']),
    ],
    'b': [
        ('Why was there stalemate on the Western Front from 1915 to 1917?',
         ['Machine guns, barbed wire and artillery made defence much stronger than attack', 'Trenches were well built and could be reinforced by rail faster than attackers could advance', 'Generals relied on tactics such as massed infantry attacks that suited the defenders', 'New weapons such as gas and early tanks were unreliable and did not achieve breakthrough', 'Both sides were evenly matched in men and resources']),
        ('Why did the British suffer such heavy losses on the first day of the Somme?',
         ['The bombardment did not cut the wire or destroy the deep German dugouts', 'Many shells were duds or the wrong type', 'Troops were ordered to advance slowly in lines, carrying heavy kit', 'German machine gunners had time to man their positions', 'Many soldiers were inexperienced volunteers of Kitchener\'s army']),
        ('Why was Verdun so important to the French?',
         ['It was a historic fortress town and a symbol of French national pride', 'Losing it would have damaged French morale badly', 'The French commanders insisted it must be held at all costs', 'Its loss might have opened the way for further German advances']),
    ],
    'claims': [
        ('Tanks broke the stalemate on the Western Front as soon as they were introduced in 1916.', False, 'Early tanks were slow and unreliable; they became more effective only in 1917-18, for example at Cambrai and Amiens.'),
        ('The Battle of the Somme helped relieve German pressure on Verdun.', True, 'The Germans had to move troops from Verdun to the Somme.'),
        ('Most soldiers on the Western Front spent all their time in the front-line trench.', False, 'Units rotated between front line, support, reserve and rest behind the lines.'),
    ],
    'c': [
        dict(q='‘The Battle of the Somme was a complete failure for the British army.’',
             pro=['About 57,000 British casualties on the first day, the worst in British military history', 'Only about 10 km was gained in over four months', 'The planned breakthrough never happened'],
             con=['It relieved pressure on Verdun, helping save the French army', 'German losses were also very heavy, wearing down its army (attrition)', 'The British army learned lessons in tactics such as the creeping barrage and the use of tanks'],
             judge='The Somme failed in its aim of breakthrough at terrible cost, but it achieved some strategic aims, so "complete failure" is too strong'),
        dict(q='How important was the machine gun in causing stalemate on the Western Front?',
             pro=['It made infantry attacks across open ground extremely costly', 'A few gunners could stop whole battalions'],
             con=['Artillery caused most casualties and destroyed the ground attackers had to cross', 'Barbed wire held attackers in the line of fire', 'Railways let defenders bring up reserves faster than attackers could advance', 'Tactics and generalship also mattered'],
             judge='The machine gun was crucial to the strength of defence, but stalemate resulted from a combination of defensive technologies and the limits of attacking tactics'),
    ],
    'src': [
        S('Sir Douglas Haig\'s official despatch on the Somme, December 1916 (extract)', 'Verdun had been relieved; the main German forces had been held on the Western front; and the enemy\'s strength had been very considerably worn down.',
          'the results of the Battle of the Somme', 'Haig claims the battle achieved its aims: relieving Verdun, holding German forces and wearing down the German army.',
          'To justify the battle and its huge cost to the government and the public.',
          'Haig commanded the British army and knew its aims', 'Haig had to defend his own decisions, so he stresses successes and does not mention casualties',
          'That about 420,000 British soldiers became casualties and the breakthrough never came.', stance=False, why='Haig argues the battle was a success'),
        S('a letter written by a British soldier after 1 July 1916 (illustrative)', 'We were told the wire would be cut and the Germans all dead. The wire was not cut. My platoon went over with thirty men; six of us came back.',
          'the first day of the Somme', 'It suggests the attack was a disaster because the bombardment failed and casualties were enormous.',
          'To tell his family what really happened.',
          'it is an eyewitness account from someone who took part', 'it describes only one platoon; letters were censored, so this may have been written later',
          'The strategic reasons for the battle, such as relieving Verdun.', stance=True, why='it shows the attack failing at huge cost'),
    ],
})



w1c = T('How important were other fronts? Gallipoli, the war at sea and the Eastern Front', 'other fronts', 'gallipoli', 'war at sea', 'eastern front')
build(w1c, {
    'enq': 'the importance of the other fronts', 'claim': 'the war at sea was more important than the Gallipoli campaign',
    'stim': ['In April 1915 Allied troops landed on the Gallipoli peninsula.', 'In May 1916 the British and German fleets met at the Battle of Jutland.',
             'In 1917 Germany\'s U-boats came close to starving Britain into surrender.'],
    'terms': [
        ('Gallipoli campaign', 'the failed Allied attempt in 1915 to capture the Dardanelles and knock the Ottoman Empire out of the war'),
        ('ANZAC', 'the Australian and New Zealand Army Corps, which fought at Gallipoli'),
        ('U-boat', 'a German submarine'),
        ('unrestricted submarine warfare', 'the German policy of sinking any ship, including neutral ones, in the waters around Britain'),
        ('convoy system', 'merchant ships sailing in groups protected by warships, introduced by Britain in 1917'),
        ('Battle of Jutland', 'the only major battle between the British and German surface fleets, in May-June 1916'),
    ],
    'dates': [('Russia was defeated at Tannenberg', 1914, 8), ('the Allied naval attack on the Dardanelles failed', 1915, 3), ('Allied troops landed at Gallipoli', 1915, 4), ('a U-boat sank the Lusitania', 1915, 5),
              ('the Battle of Jutland was fought', 1916, 5), ('Germany resumed unrestricted submarine warfare', 1917, 2)],
    'mcq': [
        ('Whose idea was the Gallipoli campaign?', 'Winston Churchill', ['Douglas Haig', 'David Lloyd George', 'Herbert Kitchener'], 'Churchill was First Lord of the Admiralty. [1]'),
        ('Why is the Battle of Jutland seen as a strategic British victory?', 'The German fleet stayed in port for most of the rest of the war', ['The British lost no ships', 'The German navy surrendered', 'It ended the U-boat campaign'], 'Britain lost more ships, but kept control of the North Sea. [1]'),
        ('What did the sinking of the Lusitania in 1915 do?', 'It turned American opinion against Germany', ['It brought the USA into the war immediately', 'It ended the war at sea', 'It caused Italy to leave the war'], '128 Americans died; the USA entered the war in 1917. [1]'),
        ('How did Britain defeat the U-boat threat in 1917?', 'By introducing the convoy system', ['By invading Germany', 'By building more battleships than Germany', 'By signing a treaty with Germany'], '[1]'),
    ],
    'a': [
        ('Describe what happened in the Gallipoli campaign.', 'events of the Gallipoli campaign',
         ['A naval attack on the Dardanelles in March 1915 failed when ships struck mines', 'British, French and ANZAC troops landed on 25 April 1915', 'Ottoman forces, including troops led by Mustafa Kemal, held the high ground', 'The Allies were trapped on narrow beaches and suffered from heat, disease and shortages', 'The troops were evacuated in December 1915 and January 1916']),
        ('Describe the war at sea between Britain and Germany.', 'features of the war at sea',
         ['Britain blockaded German ports to cut off food and raw materials', 'The two fleets fought at Jutland in 1916; Germany then kept its fleet in port', 'German U-boats attacked merchant ships, sinking the Lusitania in 1915', 'Germany began unrestricted submarine warfare in 1917', 'Britain introduced convoys in 1917 and the U-boat threat declined']),
    ],
    'b': [
        ('Why did the Gallipoli campaign fail?',
         ['The naval attack failed and warned the Ottomans of a landing', 'Poor planning and leadership: maps were inaccurate and commanders were slow to advance', 'Ottoman forces held the high ground and defended well', 'Disease, heat and lack of water weakened the troops', 'The Allies never sent enough men or supplies to break through']),
        ('Why was the war at sea important to the outcome of the war?',
         ['The British blockade caused severe shortages of food and materials in Germany', 'Control of the seas let Britain bring troops and supplies from its empire and the USA', 'Unrestricted submarine warfare helped bring the USA into the war', 'Convoys defeated the U-boat threat, so Britain was not starved into surrender']),
        ('Why was the Eastern Front important to the war in the west?',
         ['It forced Germany to fight on two fronts and split its forces', 'Russia\'s rapid attack in 1914 drew German troops away before the Marne', 'Russia\'s collapse in 1917-18 freed German divisions for the Spring Offensive in the west', 'The Treaty of Brest-Litovsk gave Germany land and resources in the east']),
    ],
    'claims': [
        ('The Gallipoli campaign succeeded in opening a supply route to Russia.', False, 'It failed; the Allies were evacuated without capturing the Dardanelles.'),
        ('Germany lost fewer ships than Britain at the Battle of Jutland.', True, 'Britain lost more ships and men, but the German fleet hardly left port again.'),
        ('The British blockade of Germany had little effect on German civilians.', False, 'It caused severe food shortages, for example the “turnip winter” of 1916-17.'),
    ],
    'c': [
        dict(q='‘The war at sea was more important than any other front in deciding the outcome of the First World War.’',
             pro=['The blockade caused hunger and unrest in Germany, contributing to its collapse in 1918', 'Control of the seas brought troops and supplies from the empire and the USA', 'U-boat warfare brought the USA into the war'],
             con=['The war was decided on the Western Front, where the German army was finally defeated in 1918', 'The Eastern Front tied down German forces for three years', 'Gallipoli failed and had little effect on the outcome'],
             judge='The war at sea was vital in weakening Germany over time, but the decisive defeat came on the Western Front; the two worked together'),
        dict(q='How important was the Gallipoli campaign?',
             pro=['It tied down Ottoman forces and was a bold attempt to break the stalemate', 'It shaped national identity in Australia, New Zealand and Turkey'],
             con=['It failed in all its aims and cost about a quarter of a million Allied casualties', 'It did not help Russia or weaken Germany', 'The Western Front and the blockade were far more important'],
             judge='Gallipoli was a costly failure of limited military importance, though it had lasting political and national significance'),
    ],
    'src': [
        S('a photograph of ANZAC troops on the beach at Anzac Cove, 1915 (description)', 'Soldiers are crowded on a narrow beach below steep cliffs, with stacks of supplies. Some men are swimming while others carry boxes up a path.',
          'conditions at Gallipoli', 'It suggests the Allies were confined to a narrow strip of beach overlooked by cliffs, with supplies landed under difficult conditions.',
          'To record the campaign; such photographs were used in newspapers at home.',
          'it is a photograph taken at the time', 'it may have been posed or chosen to look reassuring and does not show fighting or casualties',
          'The heavy casualties and disease suffered by the troops.', stance=None, visual=True),
        S('an extract from a modern history textbook (illustrative)', 'The blockade was a silent weapon. It did not win battles, but by 1918 Germany was hungry, its factories were short of materials and its people had lost the will to fight.',
          'the importance of the war at sea', 'It argues the British blockade did much to weaken Germany by 1918.',
          'To explain to students the role of the war at sea.',
          'it is written with hindsight and uses research on the German home front', 'it does not consider the fighting on the Western Front',
          'That the German army was defeated in battle in the Hundred Days of 1918.', stance=True, why='it suggests the war at sea had a decisive effect', kind='secondary', published=True),
    ],
})

w1d = T('Why Germany asked for an armistice in 1918: blockade, US entry and the Ludendorff Offensive', 'germany asked for an armistice', 'ludendorff offensive', 'us entry')
build(w1d, {
    'enq': 'why Germany asked for an armistice in 1918', 'claim': 'the failure of the Ludendorff Offensive was the main reason for Germany\'s defeat',
    'stim': ['On 21 March 1918 the German army launched a huge offensive on the Western Front.', 'In April 1917 the USA declared war on Germany.', 'By the autumn of 1918 the German army was retreating along the whole Western Front.'],
    'terms': [
        ('Ludendorff Offensive', 'the German Spring Offensive of March-July 1918, designed to win the war before American troops arrived'),
        ('stormtroopers', 'specially trained German soldiers who attacked weak points and moved quickly behind enemy lines'),
        ('Hundred Days Offensive', 'the Allied counter-attacks from August to November 1918 that drove the Germans back'),
        ('Zimmermann Telegram', 'the 1917 German message proposing an alliance with Mexico against the USA, intercepted by Britain'),
        ('turnip winter', 'the winter of 1916-17, when Germans had to live largely on turnips because of food shortages'),
        ('Hindenburg Line', 'the strongly fortified German defensive line, broken by the Allies in September-October 1918'),
    ],
    'dates': [('Germany resumed unrestricted submarine warfare', 1917, 2), ('the USA declared war on Germany', 1917, 4), ('the Ludendorff Offensive began', 1918, 3),
              ('the Allies attacked at Amiens', 1918, 8), ('the Allies broke the Hindenburg Line', 1918, 9.29), ('the armistice came into effect', 1918, 11)],
    'mcq': [
        ('Why did Ludendorff launch his offensive in March 1918?', 'To win the war before large numbers of American troops arrived', ['Because Britain had surrendered', 'To help Austria-Hungary in Italy', 'Because the blockade had ended'], 'Troops were freed by Russia\'s exit from the war. [1]'),
        ('What did Ludendorff call 8 August 1918, the first day of the Battle of Amiens?', 'The “black day” of the German army', ['The day of glory', 'The turning of the tide', 'The final victory'], '[1]'),
        ('Which event in 1917 helped bring the USA into the war?', 'Germany\'s resumption of unrestricted submarine warfare', ['The Battle of the Somme', 'The Gallipoli landings', 'The Treaty of Brest-Litovsk'], 'The Zimmermann Telegram also angered Americans. [1]'),
        ('Roughly how many American troops were in France by November 1918?', 'About 2 million', ['About 20,000', 'About 200,000', 'About 20 million'], '[1]'),
    ],
    'a': [
        ('Describe the Ludendorff Offensive of 1918.', 'features of the Ludendorff Offensive',
         ['It began on 21 March 1918 with a short, intense bombardment', 'Stormtroopers broke through weak points in the Allied line', 'German forces advanced about 60 km and came within range of Paris', 'The advance outran its supplies and many soldiers stopped to loot food', 'Germany lost hundreds of thousands of its best troops and the offensive ended by July']),
        ('Describe the effects of the British blockade on Germany.', 'effects of the British blockade on Germany',
         ['Food imports were cut off, leading to severe shortages', 'Germans lived on substitutes and turnips in the winter of 1916-17', 'Hundreds of thousands of civilians died from malnutrition and disease', 'Industry was short of raw materials such as rubber and copper', 'Hunger led to strikes and protests by 1918']),
    ],
    'b': [
        ('Why did the USA enter the war in 1917?',
         ['Germany resumed unrestricted submarine warfare, sinking American ships', 'The Zimmermann Telegram proposed a German alliance with Mexico against the USA', 'American trade and loans were tied to Britain and France', 'Wilson presented the war as a fight for democracy after the Tsar fell']),
        ('Why did the Ludendorff Offensive fail?',
         ['The advance outran its supply lines and the exhausted troops could not keep going', 'Germany lost many of its best soldiers, who could not be replaced', 'The Allies created a unified command under Foch', 'American troops were arriving in large numbers', 'Hungry German soldiers stopped to loot Allied supplies']),
    ],
    'claims': [
        ('American troops arrived in France in large numbers as soon as the USA declared war in April 1917.', False, 'The US army had to be built up; large numbers arrived only in 1918.'),
        ('The Ludendorff Offensive was made possible by Russia leaving the war.', True, 'Brest-Litovsk freed German divisions from the east.'),
        ('German armies had been pushed back into Germany when the armistice was signed.', False, 'They were still in France and Belgium, which helped the stab-in-the-back myth.'),
    ],
    'c': [
        dict(q='‘The failure of the Ludendorff Offensive was the main reason why Germany asked for an armistice in 1918.’',
             pro=['Germany lost its best troops and had no reserves left', 'The failure left the army in exposed positions and destroyed morale', 'It gave the Allies the chance to counter-attack in the Hundred Days'],
             con=['The blockade had caused hunger and unrest at home', 'The arrival of US troops made German victory impossible', 'Germany\'s allies collapsed in autumn 1918', 'The Allied armies had improved tactics with tanks, aircraft and artillery'],
             judge='The failure of the offensive was the turning point, but Germany asked for an armistice because military defeat combined with the blockade, collapse of allies and the arrival of American troops'),
    ],
    'src': [
        S('a German government poster from 1917 (description)', 'The poster urges Germans to save food and avoid waste, showing a family with small portions and the words “Eat less”.',
          'the German home front', 'It shows food was scarce in Germany and the government had to ask people to eat less.',
          'To persuade civilians to cut consumption because of the blockade.',
          'it is an official source from the time', 'it is propaganda and does not show how serious the hunger really was',
          'That hundreds of thousands of civilians died from malnutrition.', stance=False, why='it suggests problems at home rather than the offensive', visual=True),
        S('the memoirs of a German officer, published in 1920 (illustrative)', 'In March we had the best army Germany ever put into the field. By July it was gone. We had nothing left to meet the Allied attack in August.',
          'the effect of the Ludendorff Offensive', 'It suggests the offensive destroyed Germany\'s best troops and left the army unable to resist the Allied counter-attack.',
          'To explain the defeat of the army, perhaps to defend its reputation.',
          'it is from an officer who fought in 1918', 'it was written after the war, possibly to blame strategy rather than the army itself',
          'The effects of the blockade on the home front.', stance=True, why='it blames the losses of the offensive for defeat'),
    ],
})

CHAPTERS[1] = [w1a, w1b, w1c, w1d]


# ============================================================== CHAPTER 2: Depth Study B, Germany 1918-45

REICH = [  # (election, total seats, NSDAP seats, NSDAP %, KPD seats)
    ('May 1928', 491, 12, 2.6, 54), ('September 1930', 577, 107, 18.3, 77), ('July 1932', 608, 230, 37.3, 89),
    ('November 1932', 584, 196, 33.1, 100), ('March 1933', 647, 288, 43.9, 81)]

g2a = T('Was the Weimar Republic doomed from the start? Constitution, Versailles and the crises of 1919-23', 'weimar republic', 'doomed from the start', 'crises of 1919-23')
build(g2a, {
    'enq': 'the problems of the Weimar Republic, 1919-23', 'claim': 'the Weimar Republic was doomed from the start',
    'stim': ['In February 1919 the newly elected National Assembly met in the town of Weimar.', 'Between 1919 and 1923 the Weimar Republic faced uprisings from both the left and the right.',
             'In 1923 Germany suffered hyperinflation.'],
    'terms': [
        ('Article 48', 'the part of the Weimar Constitution that allowed the President to rule by decree in an emergency'),
        ('proportional representation', 'an electoral system in which parties win seats in proportion to their share of the votes'),
        ('Spartacists', 'German communists, led by Rosa Luxemburg and Karl Liebknecht, who tried to seize power in January 1919'),
        ('Freikorps', 'groups of ex-soldiers who fought against left-wing revolutionaries after the war'),
        ('Kapp Putsch', 'the attempt by right-wing Freikorps to seize power in Berlin in March 1920, defeated by a general strike'),
        ('Munich Putsch', 'Hitler\'s failed attempt to seize power in Bavaria in November 1923'),
        ('hyperinflation', 'extremely rapid inflation, as in Germany in 1923 when money became almost worthless'),
    ],
    'dates': [('the Spartacist Rising took place in Berlin', 1919, 1), ('the Weimar Constitution was adopted', 1919, 8), ('the Kapp Putsch took place', 1920, 3),
              ('Walther Rathenau was assassinated', 1922, 6), ('French and Belgian troops occupied the Ruhr', 1923, 1), ('the Munich Putsch took place', 1923, 11)],
    'mcq': [
        ('How was the Kapp Putsch defeated?', 'By a general strike of Berlin workers', ['By the army', 'By the French', 'By a vote in the Reichstag'], 'The army refused to fire on the putschists. [1]'),
        ('Which feature of the Weimar Constitution often led to weak coalition governments?', 'Proportional representation', ['Article 48', 'The Bill of Rights', 'Votes for women'], 'Many small parties won seats. [1]'),
        ('How long was the Weimar President\'s term of office?', 'Seven years', ['Four years', 'Two years', 'For life'], '[1]'),
        ('What happened to Hitler after the Munich Putsch?', 'He was sentenced to five years in prison but served about nine months', ['He was executed', 'He fled to Austria', 'He was elected President'], 'He wrote Mein Kampf in Landsberg prison. [1]'),
    ],
    'a': [
        ('Describe the main features of the Weimar Constitution.', 'features of the Weimar Constitution',
         ['The President was elected every seven years and could use Article 48 in an emergency', 'The Reichstag was elected every four years by proportional representation', 'All men and women over 20 could vote', 'The Chancellor needed the support of the Reichstag', 'A Bill of Rights guaranteed freedoms such as speech and religion']),
        ('Describe the events of the Munich Putsch in 1923.', 'events of the Munich Putsch',
         ['On 8 November 1923 Hitler and the SA burst into a meeting in a Munich beer hall', 'He forced Bavarian leaders to agree to support him at gunpoint', 'The next day Hitler, Ludendorff and about 2,000 Nazis marched through Munich', 'Police opened fire and sixteen Nazis were killed', 'Hitler was arrested, tried and given a short prison sentence']),
        ('Describe the effects of hyperinflation in 1923.', 'effects of hyperinflation in 1923',
         ['Prices rose so fast that workers were paid twice a day', 'Savings became worthless, ruining the middle classes', 'People bartered goods instead of using money', 'Some people, such as debtors and those with property, gained', 'The Republic was blamed and extremists gained support']),
    ],
    'b': [
        ('Why was the Weimar Republic unpopular in its early years?',
         ['It was blamed for signing the armistice and the Treaty of Versailles (the “November Criminals”)', 'The stab-in-the-back myth claimed the army had been betrayed', 'Proportional representation produced weak coalitions', 'Many in the army, courts and civil service were hostile to democracy', 'Economic problems culminating in hyperinflation in 1923']),
        ('Why did the Weimar Republic survive the crises of 1919-23?',
         ['The army helped crush the Spartacists, and workers defeated the Kapp Putsch by a general strike', 'Extremists were divided between left and right', 'The Munich Putsch was badly planned and stopped by the police', 'Stresemann ended passive resistance and introduced a new currency in 1923', 'Many Germans still supported moderate parties such as the SPD']),
    ],
    'claims': [
        ('Women could vote in elections under the Weimar Constitution.', True, 'All men and women over 20 could vote.'),
        ('The Kapp Putsch was a left-wing rising by communists.', False, 'It was a right-wing attempt by Freikorps; the Spartacist Rising of 1919 was the communist one.'),
        ('Hyperinflation hurt every German equally.', False, 'Savers and people on fixed incomes were ruined, but those with debts or property and some businesses gained.'),
    ],
    'c': [
        dict(q='‘The Weimar Republic was doomed from the start.’',
             pro=['It was linked to defeat and the hated Treaty of Versailles', 'Proportional representation and Article 48 were weaknesses', 'It faced violent opposition from left and right', 'Elites in the army and civil service did not support it'],
             con=['It survived the crises of 1919-23', 'It recovered under Stresemann in 1924-29', 'Moderate parties won most votes in the 1920s', 'It collapsed only after the Depression of 1929'],
             judge='The Republic had serious weaknesses from the start, but its survival and recovery in the 1920s show it was not doomed; the Depression was needed to bring it down'),
        dict(q='How far was the Treaty of Versailles responsible for the problems of the Weimar Republic, 1919-23?',
             pro=['It made the Republic unpopular and led to the November Criminals myth', 'Reparations led to the Ruhr occupation and hyperinflation', 'Military restrictions created discontented ex-soldiers who joined the Freikorps'],
             con=['The constitution\'s weaknesses were home-made', 'War debts and the printing of money caused inflation', 'Left-wing revolution began before the treaty, with the Spartacists in January 1919'],
             judge='Versailles worsened every problem, but the Republic\'s difficulties also came from the war itself and from its own political weaknesses'),
    ],
    'src': [
        S('a German cartoon from 1923 (description of a typical design)', 'A woman pushes a pram piled high with banknotes, while a shopkeeper holds up a single loaf of bread.',
          'hyperinflation in 1923', 'It shows that money had become almost worthless, so huge amounts were needed to buy basic goods.',
          'To mock the government\'s handling of the economy and show the suffering caused by inflation.',
          'it reflects what many Germans experienced in 1923', 'it is exaggerated for effect and does not explain the causes',
          'That some people, such as those with debts, gained from inflation.', stance=True, why='it shows the Republic in deep economic crisis', visual=True),
        S('an extract from a modern history book (illustrative)', 'In 1923 the Republic faced invasion, economic collapse and a putsch, yet it survived. That it did so suggests its foundations were stronger than its enemies believed.',
          'the survival of the Republic', 'It argues the Republic was not doomed because it survived the worst crisis of 1923.',
          'To give a balanced interpretation of the early Republic.',
          'it is written with hindsight', 'it is one interpretation and does not discuss later weaknesses',
          'That the Republic later collapsed during the Depression.', stance=False, why='it argues the Republic had strong foundations', kind='secondary', published=True),
    ],
})

g2b = T('Recovery under Stresemann, 1924-29', 'stresemann', 'recovery')
build(g2b, {
    'enq': 'the recovery of the Weimar Republic under Stresemann', 'claim': 'the Weimar Republic recovered fully under Stresemann',
    'stim': ['Gustav Stresemann was Chancellor in 1923 and Foreign Minister from 1923 until his death in 1929.', 'The years 1924-29 are often called the “golden years” of the Weimar Republic.'],
    'terms': [
        ('Rentenmark', 'the temporary new currency introduced in November 1923 to end hyperinflation'),
        ('Dawes Plan', 'the 1924 agreement that rescheduled reparations payments and provided American loans to Germany'),
        ('Young Plan', 'the 1929 agreement that reduced the total of reparations and extended payments to 1988'),
        ('Locarno Treaties', 'the 1925 agreements in which Germany accepted its western borders'),
        ('Kellogg-Briand Pact', 'the 1928 agreement in which countries including Germany renounced war'),
        ('Bauhaus', 'the influential school of art, design and architecture founded in Weimar in 1919'),
    ],
    'dates': [('the Rentenmark was introduced', 1923, 11), ('the Dawes Plan was agreed', 1924), ('Germany signed the Locarno Treaties', 1925), ('Germany joined the League of Nations', 1926),
              ('the Young Plan was agreed', 1929, 6), ('Stresemann died', 1929, 10)],
    'mcq': [
        ('Which country provided the loans under the Dawes Plan?', 'The USA', ['Britain', 'France', 'The USSR'], '800 million gold marks were lent at first. [1]'),
        ('What did Germany agree to in the Locarno Treaties?', 'To accept its western borders with France and Belgium', ['To pay reparations in full', 'To give up the Saar permanently', 'To join NATO'], '[1]'),
        ('Which of these was a weakness of the German economy in 1924-29?', 'It depended heavily on short-term American loans', ['It had no industry', 'It had no exports', 'Prices rose every hour'], '[1]'),
        ('How did Stresemann end hyperinflation?', 'He called off passive resistance and introduced the Rentenmark', ['He printed more money', 'He refused to pay any reparations ever again', 'He joined the League of Nations'], '[1]'),
    ],
    'a': [
        ('Describe Stresemann\'s achievements in foreign policy.', 'achievements of Stresemann in foreign policy',
         ['He agreed the Dawes Plan (1924), which reduced annual reparations and brought US loans', 'He signed the Locarno Treaties (1925), improving relations with France and Britain', 'Germany joined the League of Nations in 1926 as a permanent Council member', 'Germany signed the Kellogg-Briand Pact in 1928', 'He negotiated the Young Plan (1929), reducing the reparations total']),
        ('Describe the cultural changes in Weimar Germany in the 1920s.', 'features of Weimar culture in the 1920s',
         ['Censorship was relaxed and there was more artistic freedom', 'The Bauhaus pioneered modern architecture and design', 'German cinema flourished, for example the film Metropolis (1927)', 'Cabaret and nightclubs in Berlin became famous', 'Some conservatives saw these changes as immoral and un-German']),
    ],
    'b': [
        ('Why did the German economy recover in the years 1924-29?',
         ['The Rentenmark and then the Reichsmark restored confidence in the currency', 'The Dawes Plan reduced reparations payments to a manageable level', 'American loans financed new factories, roads and housing', 'Industrial production had regained pre-war levels by 1928']),
        ('Why was the recovery of 1924-29 fragile?',
         ['It depended on short-term American loans that could be recalled', 'Farmers faced falling prices and debt', 'Unemployment never fell much below a million', 'Extremist parties still existed and many Germans remained hostile to democracy', 'Governments were short-lived coalitions']),
    ],
    'claims': [
        ('The Dawes Plan cancelled reparations altogether.', False, 'It rescheduled payments to make them manageable and provided American loans.'),
        ('Germany joined the League of Nations in 1926.', True, 'It joined after the Locarno Treaties and became a permanent member of the Council.'),
        ('The Nazis won a large share of the vote in the 1928 election.', False, 'They won only 2.6% of the vote and 12 seats.'),
    ],
    'c': [
        dict(q='‘The Weimar Republic made a full recovery under Stresemann.’',
             pro=['Hyperinflation was ended and the currency was stable', 'Industrial output recovered and living standards rose for many', 'Germany was accepted back into the international community', 'Extremist parties lost support: the Nazis won only 12 seats in 1928'],
             con=['The economy relied on American loans', 'Farmers and some of the middle class did not share in the recovery', 'Coalition governments remained unstable', 'Hindenburg, elected President in 1925, was not committed to democracy'],
             judge='The recovery was real but fragile, depending on American money and a fragile political consensus, as the Depression showed'),
    ],
    'src': [
        S('a speech by Stresemann, 1928 (summary)', 'Stresemann warned that the German economy was “dancing on a volcano”, because it depended on short-term loans from abroad that could be withdrawn.',
          'the weakness of the German economy', 'Stresemann himself warns that the recovery depended dangerously on foreign loans.',
          'To warn Germans and politicians of the risks facing the economy.',
          'Stresemann was well placed to know the real state of the economy', 'he may have wanted to encourage caution or support for his policies',
          'That the Wall Street Crash would soon lead to the recall of American loans.', stance=False, why='it shows the recovery was not secure'),
        S('a German government poster, 1927 (description of a typical design)', 'The poster shows new factories, housing and happy families under the slogan “Germany is working again”.',
          'the recovery of the economy', 'It suggests Germany\'s economy had recovered and people were prospering.',
          'To build confidence in the Republic and its economic policies.',
          'it shows how the government wanted the recovery to be seen', 'it is propaganda and ignores farmers and the unemployed',
          'That the recovery depended on American loans.', stance=True, why='it presents the recovery as complete', visual=True),
    ],
})

g2c = T('Why Hitler was able to dominate Germany by 1934: Depression, elections and the consolidation of power', 'hitler was able to dominate germany', 'consolidation of power')
build(g2c, {
    'enq': 'how Hitler came to power', 'claim': 'the Depression was the main reason why Hitler became Chancellor',
    'stim': ['On 30 January 1933 President Hindenburg appointed Hitler as Chancellor.', 'Between 1928 and July 1932 the Nazis grew from 12 seats to 230 seats in the Reichstag.',
             'By August 1934 Hitler was Führer of Germany.'],
    'terms': [
        ('Reichstag Fire', 'the burning of the Reichstag building on 27 February 1933, blamed on a Dutch communist and used by Hitler to attack the communists'),
        ('Enabling Act', 'the law of March 1933 that gave Hitler the power to make laws without the Reichstag for four years'),
        ('Night of the Long Knives', 'the murder of Röhm and other SA leaders and opponents on 30 June 1934'),
        ('SA', 'the Nazi Stormtroopers or Brownshirts, led by Ernst Röhm'),
        ('Führer', 'the title Hitler took in August 1934 when he combined the posts of Chancellor and President'),
        ('Gleichschaltung', 'coordination: bringing all organisations in Germany under Nazi control'),
    ],
    'dates': [('the Wall Street Crash took place', 1929, 10), ('the Nazis won 107 seats in the Reichstag', 1930, 9), ('Hindenburg defeated Hitler in the presidential election', 1932, 4),
              ('Hitler became Chancellor', 1933, 1), ('the Enabling Act was passed', 1933, 3), ('the Night of the Long Knives took place', 1934, 6), ('Hindenburg died and Hitler became Führer', 1934, 8)],
    'mcq': [
        ('Who persuaded Hindenburg to appoint Hitler as Chancellor in January 1933?', 'Franz von Papen', ['Gustav Stresemann', 'Heinrich Brüning', 'Ernst Röhm'], 'Papen believed he could control Hitler as Vice-Chancellor. [1]'),
        ('Who was arrested for starting the Reichstag Fire?', 'Marinus van der Lubbe, a Dutch communist', ['Ernst Röhm', 'Joseph Goebbels', 'Kurt von Schleicher'], '[1]'),
        ('Why did Hitler carry out the Night of the Long Knives?', 'To remove the threat from Röhm and the SA and win the army\'s support', ['To punish the communists for the Reichstag Fire', 'To remove Hindenburg', 'To start a war with Poland'], '[1]'),
        ('What was the largest number of Reichstag seats the Nazis won in a free election?', '230, in July 1932', ['288, in 1928', '107, in 1924', '608, in 1933'], 'They won 288 in March 1933, but that election was not free. [1]'),
    ],
    'a': [
        ('Describe how Hitler became Chancellor in January 1933.', 'events leading to Hitler becoming Chancellor',
         ['The Nazis became the largest party in the Reichstag in July 1932 with 230 seats', 'Hindenburg at first refused to appoint Hitler', 'Chancellors Papen and Schleicher failed to win Reichstag support', 'Papen made a deal: Hitler as Chancellor with Papen as Vice-Chancellor', 'Hindenburg appointed Hitler on 30 January 1933, believing he could be controlled']),
        ('Describe how Hitler consolidated his power between 1933 and 1934.', 'steps by which Hitler consolidated his power in 1933-34',
         ['The Reichstag Fire was used to arrest communists and suspend civil rights', 'The Enabling Act (March 1933) let Hitler pass laws without the Reichstag', 'Trade unions were banned in May 1933', 'Other political parties were banned and Germany became a one-party state in July 1933', 'Röhm and other rivals were killed in the Night of the Long Knives', 'After Hindenburg died, Hitler became Führer and the army swore an oath to him']),
    ],
    'b': [
        ('Why did support for the Nazis increase between 1929 and 1932?',
         ['The Depression caused mass unemployment, reaching about six million in 1932', 'Weimar governments seemed unable to deal with the crisis', 'Nazi propaganda, organised by Goebbels, promised work and national revival', 'Hitler was a powerful speaker who appealed to many groups', 'Fear of communism drove the middle classes and industrialists to the Nazis']),
        ('Why was the Enabling Act important?',
         ['It allowed Hitler to make laws without the Reichstag', 'It gave a legal appearance to dictatorship', 'It allowed him to ban trade unions and other parties', 'It meant the Reichstag voted away its own power']),
        ('Why did Hitler carry out the Night of the Long Knives?',
         ['Röhm wanted the SA to take over the army, which alarmed the generals', 'Hitler needed the army\'s support to become Führer', 'The SA\'s violence embarrassed Hitler with businessmen and conservatives', 'It allowed him to remove other rivals such as Schleicher']),
    ],
    'claims': [
        ('Hitler won a majority of the votes in the election of July 1932.', False, 'The Nazis won 37.3% of the vote; they were the largest party but did not have a majority.'),
        ('Hitler became Chancellor through a political deal rather than by winning a majority.', True, 'Papen and other conservatives persuaded Hindenburg to appoint him in January 1933.'),
        ('The Night of the Long Knives was aimed mainly at the communists.', False, 'It was aimed mainly at Röhm and the leaders of the SA, as well as some conservative rivals.'),
    ],
    'c': [
        dict(q='‘The Depression was the main reason why Hitler became Chancellor in January 1933.’',
             pro=['Unemployment rose to about six million, making voters desperate', 'Nazi support rose from 2.6% in 1928 to 37.3% in July 1932', 'Weimar governments were discredited by their failure to deal with it'],
             con=['Nazi propaganda and Hitler\'s speaking skills won support', 'Fear of communism pushed industrialists and the middle class to the Nazis', 'Hitler was appointed through a backstairs deal by Papen and Hindenburg', 'Weaknesses of the Weimar system, such as Article 48, had already undermined democracy'],
             judge='The Depression created the conditions for Nazi success, but Hitler became Chancellor because conservative politicians chose to appoint him'),
        dict(q='How important was the Reichstag Fire in helping Hitler to consolidate his power?',
             pro=['It allowed him to persuade Hindenburg to issue an emergency decree suspending civil rights', 'Thousands of communists were arrested, helping the Nazis in the March 1933 election'],
             con=['The Enabling Act gave him the legal power to rule as a dictator', 'The Night of the Long Knives removed rivals within the Nazi movement', 'Hindenburg\'s death and the army oath made him Führer'],
             judge='The fire was an important first step, but the Enabling Act and the deal with the army in 1934 were more important in completing his dictatorship'),
    ],
    'src': [
        S('a Nazi election poster from 1932 (description)', 'The poster shows a crowd of grim, unemployed men and women with the caption “Our last hope: Hitler”.',
          'why Germans voted for the Nazis', 'It suggests that the unemployed saw Hitler as their only hope during the Depression.',
          'To win votes from Germans suffering in the Depression.',
          'it shows how the Nazis tried to appeal to voters in 1932', 'it is Nazi propaganda and tells us what the Nazis wanted people to think',
          'That conservative politicians played the decisive role in appointing Hitler.', stance=True, why='it links Nazi support to the Depression', visual=True),
        S('an extract from a modern history book (illustrative)', 'Hitler did not seize power; he was given it. In January 1933 a small group of conservatives around Hindenburg handed him the chancellorship, believing they could tame him.',
          'how Hitler became Chancellor', 'It argues Hitler became Chancellor because of a deal by conservative politicians, not because of the Depression alone.',
          'To challenge the idea that Hitler was swept to power by the voters.',
          'it reflects research on the events of January 1933', 'it is one interpretation that plays down Nazi electoral support',
          'That the Nazis were the largest party in the Reichstag.', stance=False, why='it argues political intrigue rather than the Depression was decisive', kind='secondary', published=True),
    ],
})


@g2c.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g2c_seats(r, D):
    i = r.randrange(len(REICH))
    e, tot, n, pc, k = REICH[i]
    tbl = 'Reichstag election results: ' + '; '.join(f'{a}: Nazis {c} seats ({p}% of the vote), Communists {kk} seats, out of {t} seats' for a, t, c, p, kk in REICH) + '.'
    share = 100 * n / tot
    if D <= 2:
        stem = f'Study the table. {tbl} What percentage of the Reichstag seats did the Nazis hold after the election of {e}? Give your answer to one decimal place.'
        return {'stem': stem, 'answer': f'{share:.1f}%', 'key': f'{n} ÷ {tot} × 100 = {share:.1f}%. 1 mark method, 1 mark answer [2]', 'type': 'numerical', 'marks': 2, 'minutes': 3}
    j = r.choice([x for x in range(len(REICH)) if x != i])
    a, b = sorted([i, j])
    (e1, t1, n1, p1, k1), (e2, t2, n2, p2, k2) = REICH[a], REICH[b]
    stem = (f'Study the table. {tbl} (a) Calculate the change in the number of Nazi seats between {e1} and {e2}. [1] (b) Did the Nazis ever have a majority of seats? Show how you know. [2] '
            '(c) Explain why Nazi support changed so much between 1928 and 1932. [4]')
    maj = [(x[0], x[2], x[1] // 2 + 1) for x in REICH]
    ans = (f'(a) {n2 - n1:+d} seats ({n1} to {n2}). (b) No: even in March 1933 they had 288 of 647 seats, below the 324 needed for a majority. '
           '(c) The Depression caused mass unemployment; Weimar governments failed to cope; Nazi propaganda and Hitler\'s appeal won over the unemployed, farmers and the middle classes, who also feared communism.')
    key = f'(a) {n2 - n1:+d} [1] (b) No, with comparison to the majority figure, e.g. 288 < 324 of 647 [2] (c) 1 mark per reason, extra mark for development, up to [4]'
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'numerical', 'marks': 7, 'minutes': 10}

g2d = T('How effectively the Nazis controlled Germany, 1933-45: terror, propaganda and opposition', 'nazis controlled germany', 'terror, propaganda and opposition')
build(g2d, {
    'enq': 'how the Nazis controlled Germany', 'claim': 'terror was more important than propaganda in keeping the Nazis in power',
    'stim': ['In March 1933 Joseph Goebbels became Minister for Popular Enlightenment and Propaganda.', 'The Nazi police state was run by the SS under Heinrich Himmler.',
             'Opposition to the Nazis existed, but it was small and divided.'],
    'terms': [
        ('Gestapo', 'the Nazi secret state police, which used informers to find and arrest opponents'),
        ('SS', 'the Nazi organisation led by Himmler that ran the police state and the concentration camps'),
        ('concentration camp', 'a prison camp where opponents and others were held without trial, such as Dachau, opened in 1933'),
        ('propaganda', 'material designed to make people believe particular ideas, used by Goebbels to spread Nazi views'),
        ('Confessing Church', 'the Protestant church formed by Pastor Niemöller and others who opposed Nazi control of the church'),
        ('White Rose', 'the student group led by Hans and Sophie Scholl that distributed anti-Nazi leaflets in 1942-43'),
        ('Edelweiss Pirates', 'groups of young working-class Germans who rebelled against the Hitler Youth'),
    ],
    'dates': [('the first concentration camp opened at Dachau', 1933, 3), ('Nazi students burned “un-German” books', 1933, 5), ('the Concordat was signed with the Catholic Church', 1933, 7),
              ('the Berlin Olympic Games were held', 1936), ('Pastor Niemöller was arrested', 1937), ('Hans and Sophie Scholl were executed', 1943), ('the July Bomb Plot against Hitler failed', 1944)],
    'mcq': [
        ('Who led the SS?', 'Heinrich Himmler', ['Joseph Goebbels', 'Ernst Röhm', 'Hermann Göring'], '[1]'),
        ('How did the Nazis make sure Germans heard their radio broadcasts?', 'They sold cheap radios (the “People\'s Receiver”)', ['They banned newspapers completely', 'They gave every family a television', 'They closed all cinemas'], '[1]'),
        ('Who led the July Bomb Plot of 1944?', 'Claus von Stauffenberg', ['Martin Niemöller', 'Hans Scholl', 'Ernst Röhm'], 'The bomb exploded at Hitler\'s headquarters but he survived. [1]'),
        ('What was the Concordat of 1933?', 'An agreement between Hitler and the Pope that the Nazis would not interfere with the Catholic Church', ['A ban on all churches', 'A treaty with Britain', 'A law against trade unions'], 'Hitler later broke it. [1]'),
    ],
    'a': [
        ('Describe how the Nazis used terror to control Germany.', 'methods of terror used by the Nazis',
         ['The Gestapo arrested opponents, often using information from informers', 'The SS ran concentration camps where prisoners were held without trial', 'Courts were controlled by Nazi judges and the People\'s Court tried political cases', 'People could be imprisoned simply for criticising the regime', 'Fear of being reported made people keep quiet']),
        ('Describe how Goebbels used propaganda.', 'methods of Nazi propaganda',
         ['He controlled newspapers, radio and films', 'Cheap radios were sold and loudspeakers were put up in public places', 'Huge rallies were held, such as at Nuremberg', 'The 1936 Berlin Olympics were used to show off Nazi Germany', 'Censorship banned anti-Nazi books, and books were burned in 1933']),
        ('Describe the opposition to the Nazis inside Germany.', 'forms of opposition to the Nazis inside Germany',
         ['Some church leaders spoke out, such as Pastor Niemöller of the Confessing Church', 'Young people formed groups such as the Edelweiss Pirates and the Swing Youth', 'The White Rose students distributed leaflets until their arrest in 1943', 'Army officers tried to kill Hitler in the July Bomb Plot of 1944', 'Some communists and socialists worked secretly in underground groups']),
    ],
    'b': [
        ('Why was there so little opposition to the Nazis?',
         ['Terror: the Gestapo and concentration camps frightened people into silence', 'Propaganda persuaded many that Hitler was saving Germany', 'Many Germans benefited from falling unemployment and foreign policy successes', 'Opposition parties and trade unions had been banned, so there was no organisation', 'Opponents were divided, for example communists and socialists']),
        ('Why did the Nazis control the churches?',
         ['The churches had great influence over millions of Germans', 'Christian teaching on love and charity conflicted with Nazi ideas of race and violence', 'Catholics owed loyalty to the Pope, outside Germany', 'Church youth groups competed with the Hitler Youth']),
    ],
    'claims': [
        ('Every German was watched by the Gestapo all the time.', False, 'The Gestapo was relatively small and relied heavily on information from ordinary Germans.'),
        ('The White Rose was a student group that distributed anti-Nazi leaflets.', True, 'Its leaders, Hans and Sophie Scholl, were executed in 1943.'),
        ('The July Bomb Plot of 1944 succeeded in killing Hitler.', False, 'Hitler survived and about 5,000 people were later executed.'),
    ],
    'c': [
        dict(q='‘Terror was more important than propaganda in keeping the Nazis in power.’',
             pro=['The Gestapo, SS and concentration camps removed and frightened opponents', 'Fear of informers made people conform', 'Opposition parties and unions were destroyed by force'],
             con=['Propaganda persuaded many Germans to support Hitler genuinely', 'Economic recovery and falling unemployment won support', 'Foreign policy successes such as the Rhineland and the Anschluss were popular', 'Many Germans were never directly threatened by terror'],
             judge='Terror dealt with active opponents, but propaganda and real successes explain why most Germans accepted Nazi rule'),
        dict(q='How effective was opposition to the Nazis?',
             pro=['The July Bomb Plot came close to killing Hitler', 'Church protests helped stop the official T4 euthanasia programme in 1941', 'Youth groups showed that not all young people accepted Nazi ideas'],
             con=['Opposition was small, divided and easily crushed', 'Most Germans conformed or supported the regime', 'Leaders such as the Scholls and Niemöller were executed or imprisoned'],
             judge='Opposition showed great courage, but it never seriously threatened Nazi control except in 1944'),
    ],
    'src': [
        S('a Nazi poster from 1936 (description)', 'A young Hitler Youth member holds a drum, with the words “Youth serves the Führer: all ten-year-olds into the Hitler Youth”.',
          'Nazi propaganda aimed at young people', 'It shows the Nazis used propaganda to persuade young people that they owed loyalty to Hitler.',
          'To encourage all children to join the Hitler Youth.',
          'it is an official Nazi poster that shows the regime\'s aims', 'it is propaganda and shows what the Nazis wanted, not how young people felt',
          'That some young people joined rebel groups such as the Edelweiss Pirates.', stance=False, why='it shows propaganda being used to win support rather than terror', visual=True),
        S('the memoirs of a German who lived through the Nazi years, published in the 1960s (illustrative)', 'You learned to keep your mouth shut. My neighbour made a joke about Göring and was taken away. We never found out who reported him.',
          'life under the Nazi police state', 'It suggests fear of informers and the Gestapo kept ordinary people quiet.',
          'To describe the writer\'s experiences after the war.',
          'it is from someone who lived through the period', 'it was written years later and from memory; people may stress fear to excuse their own conformity',
          'That many Germans actively supported the regime.', stance=True, why='it shows terror and fear keeping people in line'),
    ],
})

g2e = T('What was it like to live in Nazi Germany? Women, youth, workers and the persecution of minorities', 'live in nazi germany', 'women, youth, workers', 'persecution of minorities')
build(g2e, {
    'enq': 'life in Nazi Germany', 'claim': 'most Germans benefited from Nazi rule',
    'stim': ['The Nazis wanted to create a “national community” (Volksgemeinschaft) of racially pure Germans.', 'In September 1935 the Nuremberg Laws took away the citizenship of German Jews.',
             'The Nazis wanted women to focus on “children, kitchen, church”.'],
    'terms': [
        ('Volksgemeinschaft', 'the Nazi idea of a “people\'s community” in which all racially pure Germans worked together'),
        ('Nuremberg Laws', 'the 1935 laws that removed German citizenship from Jews and banned marriage between Jews and non-Jews'),
        ('Kristallnacht', 'the “Night of Broken Glass”, 9-10 November 1938, when Jewish shops, homes and synagogues were attacked'),
        ('Hitler Youth', 'the Nazi youth organisation for boys; girls joined the League of German Maidens'),
        ('German Labour Front (DAF)', 'the Nazi organisation that replaced trade unions'),
        ('Strength Through Joy (KdF)', 'the Nazi organisation that provided cheap holidays and leisure activities for workers'),
        ('Lebensborn', 'the SS programme that encouraged racially “pure” women to have children'),
    ],
    'dates': [('the Nazis organised a boycott of Jewish shops', 1933, 4), ('the Nuremberg Laws were passed', 1935, 9), ('membership of the Hitler Youth was made compulsory by law', 1936, 12), ('Kristallnacht took place', 1938, 11), ('the T4 euthanasia programme began', 1939, 9)],
    'mcq': [
        ('What did the Law for the Encouragement of Marriage (1933) offer?', 'A loan to newly married couples, reduced for each child born', ['Free cars for all families', 'Higher wages for working women', 'Exemption from the Hitler Youth'], 'A quarter of the loan was cancelled for each child. [1]'),
        ('What was the Mother\'s Cross awarded for?', 'Having large numbers of children', ['Joining the army', 'Working in a factory', 'Reporting opponents to the Gestapo'], 'The gold cross was for eight or more children. [1]'),
        ('What replaced trade unions in Nazi Germany?', 'The German Labour Front (DAF)', ['The SA', 'The Reichstag', 'The Confessing Church'], '[1]'),
        ('What happened during Kristallnacht in November 1938?', 'Jewish shops, homes and synagogues were attacked across Germany', ['The Reichstag building was burned', 'Röhm was murdered', 'The Olympic Games were opened'], 'About 30,000 Jewish men were sent to concentration camps. [1]'),
    ],
    'a': [
        ('Describe Nazi policies towards women.', 'Nazi policies towards women',
         ['Women were encouraged to stay at home and focus on children, kitchen and church', 'Marriage loans were offered, reduced with each child born', 'The Mother\'s Cross was awarded to women with many children', 'Women were discouraged from careers such as law and medicine', 'Women were urged to avoid make-up and trousers']),
        ('Describe how the Nazis tried to control young people.', 'methods the Nazis used to control young people',
         ['Boys joined the Hitler Youth and girls the League of German Maidens', 'Membership became compulsory from 1936 and was enforced more strictly from 1939', 'Activities included camping, sport and military training for boys', 'The school curriculum was changed to teach Nazi ideas, including race studies', 'Teachers had to join the Nazi Teachers\' League']),
        ('Describe the persecution of Jews in Germany between 1933 and 1939.', 'stages in the persecution of Jews in Germany, 1933-39',
         ['A boycott of Jewish shops was organised in April 1933', 'Jews were dismissed from the civil service and professions', 'The Nuremberg Laws of 1935 removed citizenship and banned mixed marriages', 'During Kristallnacht in 1938 synagogues and shops were destroyed and about 30,000 Jewish men were sent to camps', 'Jewish children were expelled from schools and Jewish businesses were taken over']),
    ],
    'b': [
        ('Why did many workers support the Nazis?',
         ['Unemployment fell from about six million in 1932 to under half a million by 1938', 'Public works such as autobahns and rearmament created jobs', 'Strength Through Joy gave cheap holidays and leisure activities', 'Beauty of Labour improved conditions in some workplaces', 'There was a sense of national pride and security']),
        ('Why did the Nazis persecute minorities?',
         ['Nazi racial ideas held that Aryans were a master race and others were inferior', 'Hitler blamed Jews for Germany\'s defeat and economic problems', 'Persecution created a scapegoat that united the “national community”', 'They wanted a racially “pure” and healthy population, so disabled people, Roma and others were targeted']),
    ],
    'claims': [
        ('Unemployment in Germany fell sharply under the Nazis.', True, 'It fell from about six million in 1932 to under half a million by 1938, partly through public works, rearmament and conscription.'),
        ('Workers had more freedom under the Nazis than under the Weimar Republic.', False, 'Trade unions were banned and workers could not strike; the DAF controlled conditions.'),
        ('Women were encouraged to join the army in Nazi Germany in the 1930s.', False, 'Nazi policy encouraged women to stay at home and raise children.'),
    ],
    'c': [
        dict(q='‘Most Germans benefited from Nazi rule in the years 1933-39.’',
             pro=['Unemployment fell dramatically and many families felt secure', 'Strength Through Joy provided leisure and holidays', 'Many took pride in Germany\'s restored power'],
             con=['Workers lost trade unions and real wages were held down', 'Women lost opportunities in careers and politics', 'Jews, Roma, disabled people and others were persecuted', 'Freedom of speech and religion were destroyed'],
             judge='Many Germans who fitted the national community gained materially, but at the cost of freedom, and minorities suffered terribly'),
        dict(q='How successful were Nazi policies towards young people?',
             pro=['Millions joined the Hitler Youth and many enjoyed its activities', 'Schools taught Nazi ideas and many young people supported the regime'],
             con=['Some rebelled, for example the Edelweiss Pirates and the Swing Youth', 'Compulsion suggests voluntary membership was not enough', 'Some found the activities boring and military drill unpopular'],
             judge='Nazi youth policies were largely successful in winning young people\'s loyalty, but they never achieved total control'),
    ],
    'src': [
        S('a photograph of a Jewish shop in Berlin, 10 November 1938 (description)', 'A man walks past a Jewish-owned shop whose windows have been smashed. Broken glass lies on the pavement and passers-by look on.',
          'Kristallnacht', 'It shows that Jewish property was destroyed openly and that onlookers did nothing to stop it.',
          'To record the event; such photographs were published abroad and shocked foreign opinion.',
          'it is a photograph taken on the morning after Kristallnacht', 'it shows a single scene and does not show the violence against people',
          'That about 30,000 Jewish men were sent to concentration camps.', stance=False, why='it shows the suffering of minorities under Nazi rule', visual=True),
        S('a report by an underground group of the banned SPD, 1938 (summary)', 'The report noted that many workers grumbled about long hours and low wages, but were glad to have jobs and enjoyed the Strength Through Joy trips, and that few would risk opposing the regime.',
          'workers\' attitudes in Nazi Germany', 'It suggests workers had mixed feelings: they disliked some conditions but valued jobs and leisure.',
          'To inform the exiled SPD leadership about conditions in Germany.',
          'the reporters were secret socialist opponents of the Nazis, so they were not likely to exaggerate support for the regime', 'they gathered information secretly and may not represent all workers',
          'That trade unions had been banned and workers could not strike.', stance=True, why='it suggests many workers felt they had benefited'),
    ],
})

CHAPTERS[2] = [g2a, g2b, g2c, g2d, g2e]


# ============================================================== CHAPTER 3: Depth Study C, Russia 1905-41

FYP = [('Coal', 35.4, 64.4, 128.0), ('Steel', 4.0, 5.9, 17.7), ('Oil', 11.7, 21.4, 28.5)]  # million tonnes 1928, 1932, 1937 (official Soviet figures)

r3a = T('Why the tsarist regime collapsed in 1917: the 1905 Revolution, Nicholas II and the First World War', 'tsarist regime collapsed', '1905 revolution', 'nicholas ii')
build(r3a, {
    'enq': 'the collapse of tsarism', 'claim': 'the First World War was the main reason for the collapse of tsarism',
    'stim': ['In January 1905 troops fired on a peaceful procession of workers in St Petersburg.', 'In September 1915 Nicholas II took personal command of the Russian army.',
             'In March 1917 (February in the old Russian calendar) Nicholas II abdicated.'],
    'terms': [
        ('autocracy', 'a system in which one ruler, such as the Tsar, has complete power'),
        ('Bloody Sunday', 'the shooting of peaceful protesters outside the Winter Palace in St Petersburg in January 1905'),
        ('October Manifesto', 'the Tsar\'s 1905 promise of an elected parliament (Duma) and civil rights'),
        ('Duma', 'the Russian parliament set up after 1905, with limited powers'),
        ('Okhrana', 'the Tsar\'s secret police'),
        ('Rasputin', 'the Siberian holy man who gained influence over the Tsarina and was murdered in December 1916'),
        ('Stolypin', 'the Prime Minister from 1906 to 1911 who combined harsh repression with land reform'),
    ],
    'dates': [('Bloody Sunday took place in St Petersburg', 1905, 1), ('the Tsar issued the October Manifesto', 1905, 10), ('Stolypin was assassinated', 1911), ('Russia was defeated at Tannenberg', 1914, 8),
              ('Nicholas II took personal command of the army', 1915, 9), ('Rasputin was murdered', 1916, 12), ('Nicholas II abdicated', 1917, 3)],
    'mcq': [
        ('Who led the procession of workers on Bloody Sunday in 1905?', 'Father Gapon', ['Lenin', 'Rasputin', 'Kerensky'], '[1]'),
        ('Which war did Russia lose in 1904-05, contributing to the 1905 Revolution?', 'The Russo-Japanese War', ['The Crimean War', 'The Balkan Wars', 'The Russo-Turkish War'], 'The Russian fleet was destroyed at Tsushima. [1]'),
        ('Why was Nicholas II\'s decision to take command of the army in 1915 a mistake?', 'He was personally blamed for military defeats', ['He was a brilliant general who won too quickly', 'He left the army in Rasputin\'s command', 'He ended the war too soon'], 'It also left the government in the hands of the Tsarina and Rasputin. [1]'),
        ('What did the October Manifesto promise?', 'An elected Duma and civil rights', ['An end to the monarchy', 'Land for all peasants', 'Peace with Germany'], '[1]'),
    ],
    'a': [
        ('Describe the events of the 1905 Revolution.', 'events of the 1905 Revolution',
         ['On Bloody Sunday, troops fired on a peaceful procession led by Father Gapon', 'Strikes spread across Russia and peasants seized land', 'Sailors mutinied on the battleship Potemkin', 'The St Petersburg Soviet was set up, with Trotsky as a leader', 'The Tsar issued the October Manifesto promising a Duma']),
        ('Describe the effects of the First World War on Russia.', 'effects of the First World War on Russia',
         ['Heavy defeats, such as Tannenberg in 1914, and millions of casualties', 'Shortages of weapons, boots and supplies for the army', 'Food and fuel shortages in the cities as the railways were overwhelmed', 'Prices rose rapidly', 'The Tsar was blamed after he took command in 1915', 'Rasputin\'s influence over the Tsarina damaged the royal family\'s reputation']),
        ('Describe the events of the February Revolution of 1917.', 'events of the February Revolution of 1917',
         ['Strikes and bread riots broke out in Petrograd', 'Women marched on International Women\'s Day', 'Soldiers refused to fire on the crowds and joined them', 'The Duma set up a Provisional Committee and the Petrograd Soviet was formed', 'Nicholas II abdicated in March 1917']),
    ],
    'b': [
        ('Why did the Tsar survive the 1905 Revolution?',
         ['The October Manifesto divided the opposition, satisfying liberals', 'The army stayed loyal and crushed the revolts once troops returned from the east', 'The St Petersburg Soviet was arrested', 'Peace with Japan was made in 1905', 'Stolypin used repression and reform to restore order']),
        ('Why did the First World War weaken the Tsar\'s rule?',
         ['Defeats and huge casualties destroyed confidence in the government', 'Taking command made Nicholas personally responsible', 'Shortages of food and fuel caused hardship and strikes in the cities', 'The influence of Rasputin and the German-born Tsarina discredited the monarchy', 'The army, the Tsar\'s main support, became unreliable']),
    ],
    'claims': [
        ('The October Manifesto gave the Duma the power to make all the laws in Russia.', False, 'The Fundamental Laws of 1906 kept most power with the Tsar, who could dissolve the Duma.'),
        ('Soldiers joining the protesters was a key reason why the February Revolution succeeded.', True, 'Without the army, the Tsar could not restore order.'),
        ('The Bolsheviks led the February Revolution of 1917.', False, 'It was largely spontaneous; Lenin and most Bolshevik leaders were in exile.'),
    ],
    'c': [
        dict(q='‘The First World War was the main reason for the collapse of tsarism in 1917.’',
             pro=['Defeats and casualties discredited the regime', 'Shortages caused the bread riots and strikes of February 1917', 'The army, demoralised by the war, refused to defend the Tsar'],
             con=['Long-term problems: poverty of peasants and workers, demands for reform since 1905', 'Nicholas II\'s weak leadership and refusal to share power', 'The influence of Rasputin and the Tsarina', 'The Tsar had survived 1905 only by making promises he later took back'],
             judge='The war turned long-term discontent into revolution, but the Tsar\'s own failings and the weaknesses of autocracy explain why the war proved fatal'),
        dict(q='How important was Nicholas II\'s personal character in the collapse of tsarism?',
             pro=['He was indecisive and refused to share power with the Duma', 'He took command of the army in 1915 and was blamed for defeats', 'He allowed Rasputin and the Tsarina to influence government'],
             con=['Russia\'s economic and social problems were deep-rooted', 'The war created unbearable pressures', 'Revolutionary groups had been growing since the 1890s'],
             judge='Nicholas\'s failings made collapse more likely, but the war and long-term problems would have tested any ruler'),
    ],
    'src': [
        S('a photograph of Nicholas II blessing troops before they left for the front, 1914-15 (description)', 'The Tsar holds up an icon as kneeling soldiers bow their heads.',
          'the Tsar\'s relationship with the army', 'It presents the Tsar as the religious father of his people and leader of the army.',
          'To build loyalty to the Tsar and support for the war.',
          'it is a photograph from the time', 'it was official propaganda and does not show the army\'s shortages or defeats',
          'That by 1917 soldiers were refusing to defend the regime.', stance=None, visual=True),
        S('a report by the Okhrana, the Tsar\'s secret police, October 1916 (summary)', 'The report warned that the cost of food had risen far faster than wages and that workers in Petrograd were angry and close to revolt.',
          'conditions in Russia in 1916', 'It shows that even the Tsar\'s own police knew that wartime hardship was pushing workers towards revolution.',
          'To inform the government of the dangerous mood in Petrograd.',
          'it was written by the secret police for the government, so it had no reason to exaggerate opposition', 'it describes only Petrograd',
          'The role of Rasputin or Nicholas\'s command of the army.', stance=True, why='it links the collapse to wartime shortages', published=False),
    ],
})

r3b = T('How the Bolsheviks gained power in October 1917: the Provisional Government and Lenin', 'bolsheviks gained power', 'provisional government', 'lenin')
build(r3b, {
    'enq': 'how the Bolsheviks gained power in 1917', 'claim': 'the weakness of the Provisional Government was the main reason for the Bolshevik takeover',
    'stim': ['In April 1917 Lenin returned to Russia from exile in Switzerland.', 'On 25 October 1917 (7 November in the modern calendar) the Bolsheviks seized the Winter Palace.',
             'From March to October 1917 Russia was ruled by the Provisional Government.'],
    'terms': [
        ('Provisional Government', 'the temporary government that ruled Russia from March to October 1917'),
        ('Petrograd Soviet', 'the council of workers\' and soldiers\' deputies in the capital, which shared power with the Provisional Government'),
        ('dual power', 'the sharing of authority between the Provisional Government and the Petrograd Soviet in 1917'),
        ('April Theses', 'Lenin\'s programme of April 1917, calling for “peace, land and bread” and “all power to the soviets”'),
        ('Red Guards', 'armed groups of workers who supported the Bolsheviks'),
        ('Kornilov affair', 'the attempted military coup of August-September 1917 that strengthened the Bolsheviks'),
        ('Military Revolutionary Committee', 'the committee of the Petrograd Soviet, led by Trotsky, that organised the October Revolution'),
    ],
    'dates': [('the Provisional Government was formed', 1917, 3), ('Lenin returned to Petrograd', 1917, 4), ('the July Days protests were crushed', 1917, 7),
              ('the Kornilov affair took place', 1917, 8.5), ('the Bolsheviks seized power', 1917, 11)],
    'mcq': [
        ('Which slogan did Lenin use in the April Theses?', '“Peace, land and bread”', ['“Workers of the world, unite”', '“Socialism in one country”', '“All power to the Duma”'], '[1]'),
        ('Who became Prime Minister of the Provisional Government in July 1917?', 'Alexander Kerensky', ['Prince Lvov', 'Leon Trotsky', 'Lavr Kornilov'], '[1]'),
        ('How did the Kornilov affair help the Bolsheviks?', 'Kerensky armed the Red Guards to defend Petrograd, and the Bolsheviks gained credit', ['Kornilov joined the Bolsheviks', 'It ended the war with Germany', 'It killed Kerensky'], '[1]'),
        ('Who organised the Bolshevik seizure of power in October 1917?', 'Leon Trotsky', ['Joseph Stalin', 'Nikolai Bukharin', 'Grigory Zinoviev'], 'As head of the Military Revolutionary Committee. [1]'),
    ],
    'a': [
        ('Describe the problems faced by the Provisional Government in 1917.', 'problems faced by the Provisional Government',
         ['It shared power with the Petrograd Soviet, whose Order No. 1 controlled the soldiers', 'It continued the war, which was very unpopular', 'It delayed land reform until a Constituent Assembly met', 'Food shortages and inflation continued', 'It faced challenges from the left (July Days) and the right (Kornilov)']),
        ('Describe the events of the October Revolution.', 'events of the Bolshevik seizure of power',
         ['Trotsky\'s Military Revolutionary Committee planned the rising', 'On 24-25 October Red Guards seized key points such as bridges, railway stations and the telephone exchange', 'The cruiser Aurora fired a blank shot as a signal', 'The Winter Palace was taken with little resistance and ministers were arrested', 'Kerensky fled and the Congress of Soviets approved the new government']),
    ],
    'b': [
        ('Why did the Provisional Government become unpopular?',
         ['It kept Russia in the war, and the June offensive of 1917 failed', 'It did not give land to the peasants', 'It failed to solve shortages of food and fuel', 'It had to share power with the Soviet', 'Kerensky\'s handling of the Kornilov affair made him look weak']),
        ('Why were the Bolsheviks able to seize power in October 1917?',
         ['Lenin\'s slogans of peace, land and bread were very popular', 'The Bolsheviks gained a majority in the Petrograd Soviet by September', 'Trotsky organised the Red Guards effectively', 'The Provisional Government had little armed support left', 'The Kornilov affair had armed the Bolsheviks and discredited Kerensky']),
    ],
    'claims': [
        ('The October Revolution involved heavy fighting in Petrograd.', False, 'The seizure of power in Petrograd was achieved with little fighting; the Winter Palace was lightly defended.'),
        ('Lenin\'s return in April 1917 was helped by the German government.', True, 'Germany allowed him to travel through Germany, hoping he would take Russia out of the war.'),
        ('The Provisional Government took Russia out of the First World War.', False, 'It stayed in the war; it was the Bolsheviks who made peace at Brest-Litovsk in 1918.'),
    ],
    'c': [
        dict(q='‘The weakness of the Provisional Government was the main reason why the Bolsheviks seized power in October 1917.’',
             pro=['It stayed in the war and failed to give land or solve food shortages', 'It shared power with the Soviet', 'The Kornilov affair left it without military support'],
             con=['Lenin\'s leadership and slogans won support', 'Trotsky\'s organisation of the Red Guards made the takeover possible', 'The Bolsheviks were disciplined and determined', 'Bolsheviks controlled the Petrograd Soviet by September 1917'],
             judge='The Provisional Government\'s weakness created the opportunity, but Lenin and Trotsky\'s leadership explain why the Bolsheviks, rather than another group, took it'),
        dict(q='How important was Lenin in the Bolshevik seizure of power?',
             pro=['His April Theses gave the Bolsheviks popular slogans', 'He insisted on seizing power in October against doubters such as Zinoviev and Kamenev'],
             con=['Trotsky planned and carried out the takeover', 'The failures of the Provisional Government did much of the work', 'The Kornilov affair gave the Bolsheviks weapons and credibility'],
             judge='Lenin was vital in deciding that the Bolsheviks should take power, but Trotsky\'s organisation and the government\'s weakness were essential too'),
    ],
    'src': [
        S('a Bolshevik poster of 1917 (description of a typical design)', 'Workers, soldiers and peasants march together under red banners reading “All power to the soviets!” and “Peace, land and bread!”.',
          'Bolshevik propaganda in 1917', 'It shows the Bolsheviks appealing to workers, soldiers and peasants with simple promises.',
          'To win support for the Bolsheviks against the Provisional Government.',
          'it shows the slogans the Bolsheviks used', 'it is propaganda and does not show how far people actually supported the party',
          'That the Bolsheviks won only about a quarter of the votes in the Constituent Assembly elections.', stance=False, why='it suggests Bolshevik appeal and organisation explain their success', visual=True),
        S('the memoirs of a member of the Provisional Government, published in exile in the 1920s (illustrative)', 'By October we had no soldiers we could rely on. The garrison of Petrograd would not move. We were a government without an army.',
          'the position of the Provisional Government in October 1917', 'It suggests the Provisional Government had lost all military support and could not defend itself.',
          'To explain the fall of the government, perhaps to excuse its failure.',
          'the writer was in the government at the time', 'it was written later by someone who wanted to explain or justify defeat',
          'The role of Lenin and Trotsky.', stance=True, why='it stresses the government\'s weakness'),
    ],
})

r3c = T('How the Bolsheviks consolidated their rule: Civil War, War Communism and the NEP', 'consolidated their rule', 'civil war', 'war communism', 'nep')
build(r3c, {
    'enq': 'how the Bolsheviks kept power, 1917-24', 'claim': 'the Bolsheviks won the Civil War mainly because of the weaknesses of the Whites',
    'stim': ['In January 1918 the Bolsheviks closed down the Constituent Assembly.', 'Between 1918 and 1921 the Bolsheviks fought a civil war against the Whites.',
             'In March 1921 sailors at the Kronstadt naval base rebelled against the Bolsheviks.'],
    'terms': [
        ('Constituent Assembly', 'the elected assembly that met in January 1918 and was closed by the Bolsheviks after one day'),
        ('Cheka', 'the Bolshevik secret police set up in December 1917'),
        ('Whites', 'the opponents of the Bolsheviks in the Civil War, including former tsarist officers'),
        ('War Communism', 'the Bolshevik economic policy of 1918-21: nationalisation of industry and forced requisitioning of grain'),
        ('New Economic Policy (NEP)', 'Lenin\'s 1921 policy allowing small private businesses and private sale of surplus grain'),
        ('Nepmen', 'traders and small businessmen who profited under the NEP'),
        ('Red Terror', 'the Cheka\'s campaign of arrests and executions against opponents of the Bolsheviks'),
    ],
    'dates': [('the Cheka was set up', 1917, 12), ('the Constituent Assembly was closed', 1918, 1), ('the Treaty of Brest-Litovsk was signed', 1918, 3), ('the Tsar and his family were shot at Ekaterinburg', 1918, 7),
              ('the Kronstadt rising took place', 1921, 3.01), ('the NEP was announced', 1921, 3.15), ('Lenin died', 1924)],
    'mcq': [
        ('Who led the Red Army in the Civil War?', 'Leon Trotsky', ['Joseph Stalin', 'Admiral Kolchak', 'General Denikin'], '[1]'),
        ('Which party won the most votes in the Constituent Assembly elections of November 1917?', 'The Socialist Revolutionaries', ['The Bolsheviks', 'The Kadets', 'The Mensheviks'], 'The Bolsheviks won about a quarter of the vote. [1]'),
        ('Why did Lenin introduce the NEP in 1921?', 'War Communism had caused famine, unrest and the Kronstadt rising', ['The Whites had won the Civil War', 'Stalin demanded it', 'Britain offered a loan in return'], '[1]'),
        ('What did the Treaty of Brest-Litovsk cost Russia?', 'Large areas of land in the west, with about a third of its population', ['Its navy only', 'Siberia', 'Nothing, because Russia won'], 'Including Ukraine, Poland and the Baltic lands. [1]'),
    ],
    'a': [
        ('Describe War Communism.', 'features of War Communism',
         ['Factories and industry were nationalised', 'Grain was requisitioned from peasants by force', 'Private trade was banned', 'Food was rationed, with more for workers and soldiers', 'Strict discipline was imposed in factories']),
        ('Describe the New Economic Policy.', 'features of the New Economic Policy',
         ['Requisitioning was replaced by a tax in kind', 'Peasants could sell surplus grain for profit', 'Small businesses could be privately owned', 'Large industries, banks and foreign trade stayed under state control', 'Nepmen traders appeared and production recovered']),
        ('Describe how the Bolsheviks dealt with opposition in 1917-18.', 'methods the Bolsheviks used against opposition in 1917-18',
         ['The Cheka arrested and executed opponents', 'The Constituent Assembly was closed after one day in January 1918', 'Opposition newspapers were banned', 'Other parties, such as the Kadets, were banned', 'Peace was made at Brest-Litovsk to concentrate on enemies at home']),
    ],
    'b': [
        ('Why did the Bolsheviks win the Civil War?',
         ['Trotsky built a disciplined Red Army of about five million by 1920', 'The Reds controlled the central industrial areas and the railways', 'The Whites were divided, spread around the edges of Russia and lacked a common aim', 'Many peasants feared the Whites would bring back landlords', 'Foreign support for the Whites was limited and allowed the Reds to appear patriotic']),
        ('Why did Lenin introduce the New Economic Policy?',
         ['War Communism had caused economic collapse and famine in 1921', 'Peasants resisted requisitioning and grew less grain', 'Workers went on strike and the Kronstadt sailors rebelled', 'Lenin needed to restore production and win back support']),
    ],
    'claims': [
        ('The Bolsheviks won a majority in the Constituent Assembly elections.', False, 'The Socialist Revolutionaries won most votes; the Bolsheviks closed the Assembly in January 1918.'),
        ('Under the NEP peasants could sell surplus grain for profit.', True, 'Requisitioning was replaced by a tax, and surplus could be sold.'),
        ('The NEP was supported by every member of the Communist Party.', False, 'Many saw it as a retreat to capitalism; Lenin called it a temporary step back.'),
    ],
    'c': [
        dict(q='‘The Bolsheviks won the Civil War mainly because of the weaknesses of the Whites.’',
             pro=['The Whites were divided and had no common aims', 'Their forces were spread around the edges of Russia', 'White brutality and links to landlords lost peasant support'],
             con=['Trotsky\'s leadership created an effective Red Army', 'The Reds held the central areas, industry and railways', 'War Communism supplied the army', 'The Cheka\'s Red Terror crushed opposition behind the lines'],
             judge='White weaknesses were important, but the Reds won because they used their central position and Trotsky\'s leadership to make the most of them'),
        dict(q='How far was the NEP a success?',
             pro=['Agricultural and industrial production recovered', 'It ended the famine and the unrest of 1921', 'It helped the Bolsheviks keep power'],
             con=['Many communists saw it as a betrayal of socialism', 'Nepmen and richer peasants (kulaks) prospered, increasing inequality', 'Industry recovered more slowly than farming (the “scissors crisis”)'],
             judge='The NEP was an economic and political success in the short term, but it divided the party and was abandoned by Stalin in 1928'),
    ],
    'src': [
        S('a Bolshevik poster from the Civil War (description of a typical design)', 'A Red Army soldier stands over defeated White generals, who are shown as fat and wealthy, with landlords and foreign capitalists hiding behind them.',
          'Bolshevik propaganda in the Civil War', 'It presents the Whites as enemies of ordinary people, supported by landlords and foreigners.',
          'To win peasant and worker support for the Reds by linking the Whites with landlords and foreign powers.',
          'it shows how the Bolsheviks presented the war', 'it is propaganda and exaggerates',
          'That the Reds also used terror, such as the Cheka\'s executions.', stance=True, why='it suggests the Whites lacked popular support', visual=True),
        S('an extract from a modern history book (illustrative)', 'The Whites had brave soldiers and foreign money, but they never agreed what they were fighting for, and they never fought together. The Reds, with the railways in their hands, could move troops to whichever front was most threatened.',
          'why the Reds won the Civil War', 'It argues that White disunity and the Reds\' control of the railways and central position explain the outcome.',
          'To explain the outcome of the Civil War to readers.',
          'it is written with hindsight and draws on research', 'it does not discuss Trotsky\'s leadership or the role of terror',
          'Trotsky\'s role in building the Red Army.', stance=True, why='it stresses White weaknesses', kind='secondary', published=True),
    ],
})

r3d = T('How Stalin gained and held on to power: the leadership struggle and the purges', 'stalin gained and held on to power', 'leadership struggle', 'purges')
build(r3d, {
    'enq': 'Stalin\'s rise to power', 'claim': 'Stalin became leader mainly because of the mistakes of his rivals',
    'stim': ['When Lenin died in January 1924 there was no agreed successor.', 'By 1929 Stalin had defeated his rivals for the leadership of the USSR.',
             'In December 1934 the Leningrad party leader Sergei Kirov was murdered.'],
    'terms': [
        ('General Secretary', 'the post Stalin held from 1922, which gave him control over party appointments'),
        ('Lenin\'s Testament', 'Lenin\'s notes of 1922-23 criticising possible successors and advising that Stalin be removed as General Secretary'),
        ('Socialism in One Country', 'Stalin\'s policy of building socialism in the USSR first, rather than spreading world revolution'),
        ('Permanent Revolution', 'Trotsky\'s idea that the revolution must be spread to other countries to survive'),
        ('show trials', 'public trials of leading communists, such as Zinoviev, Kamenev and Bukharin, who confessed to invented crimes'),
        ('NKVD', 'the Soviet secret police that carried out the purges'),
        ('gulag', 'the system of labour camps where millions of prisoners were sent'),
        ('cult of personality', 'the use of propaganda to present Stalin as an all-wise, heroic leader'),
    ],
    'dates': [('Stalin became General Secretary of the Communist Party', 1922), ('Lenin died', 1924), ('Trotsky was expelled from the party', 1927), ('Trotsky was exiled from the USSR', 1929),
              ('Kirov was murdered', 1934), ('Zinoviev and Kamenev were put on trial and executed', 1936), ('Bukharin was tried and executed', 1938), ('Trotsky was murdered in Mexico', 1940)],
    'mcq': [
        ('Why was the post of General Secretary so useful to Stalin?', 'It allowed him to appoint his supporters to key positions in the party', ['It made him head of the Red Army', 'It gave him control of foreign policy', 'It made him President'], '[1]'),
        ('What did Lenin\'s Testament say about Stalin?', 'That he was too rude and should be removed as General Secretary', ['That he should become leader', 'That he was the best Marxist', 'That he should lead the Red Army'], 'The Testament was not published in the USSR. [1]'),
        ('How did Stalin mislead Trotsky over Lenin\'s funeral?', 'He gave Trotsky the wrong date, so Trotsky did not attend', ['He banned Trotsky from Moscow', 'He held the funeral in secret', 'He made Trotsky deliver the speech'], 'Trotsky\'s absence looked disrespectful. [1]'),
        ('Which senior army commander was executed in the purge of the Red Army in 1937?', 'Marshal Tukhachevsky', ['Marshal Zhukov', 'Leon Trotsky', 'Sergei Kirov'], '[1]'),
    ],
    'a': [
        ('Describe how Stalin defeated his rivals between 1924 and 1929.', 'steps by which Stalin defeated his rivals, 1924-29',
         ['He used his position as General Secretary to promote supporters', 'He allied with Zinoviev and Kamenev against Trotsky', 'Lenin\'s Testament was not published, which protected him', 'He then allied with Bukharin against Zinoviev and Kamenev', 'Trotsky was expelled in 1927 and exiled in 1929, and Bukharin was removed from the Politburo in 1929']),
        ('Describe the purges of the 1930s.', 'features of Stalin\'s purges',
         ['After Kirov\'s murder in 1934 Stalin used the NKVD to arrest suspected enemies', 'Leading communists such as Zinoviev, Kamenev and Bukharin confessed at show trials and were executed', 'The Red Army was purged, including Marshal Tukhachevsky', 'Ordinary people were denounced, arrested and sent to the gulags', 'Hundreds of thousands were executed in 1937-38 alone']),
    ],
    'b': [
        ('Why was Stalin able to become leader of the USSR by 1929?',
         ['As General Secretary he controlled appointments and built a loyal following', 'His rivals underestimated him as a dull bureaucrat', 'Trotsky was disliked and seen as arrogant, and failed to build support', 'Stalin cleverly switched alliances, using rivals against each other', 'Socialism in One Country was more popular than Permanent Revolution']),
        ('Why did Stalin carry out the purges?',
         ['To remove any possible rivals and opposition within the party', 'He was suspicious, even paranoid, about plots against him', 'To create fear so that no one would challenge him', 'To find scapegoats for economic problems', 'To provide labour for the gulags']),
    ],
    'claims': [
        ('Lenin named Stalin as his chosen successor in his Testament.', False, 'Lenin\'s Testament criticised Stalin and advised removing him as General Secretary.'),
        ('Stalin allied with different rivals at different times to defeat his opponents.', True, 'He sided with Zinoviev and Kamenev against Trotsky, then with Bukharin against them.'),
        ('The purges affected only leading members of the Communist Party.', False, 'They affected the army, officials and millions of ordinary citizens.'),
    ],
    'c': [
        dict(q='‘Stalin became leader of the USSR mainly because of the mistakes of his rivals.’',
             pro=['Trotsky failed to attend Lenin\'s funeral and did not build support in the party', 'Zinoviev and Kamenev helped to suppress Lenin\'s Testament', 'His rivals underestimated him'],
             con=['His control of party appointments as General Secretary gave him a loyal following', 'He was skilful at switching alliances', 'Socialism in One Country was a popular policy', 'He presented himself as Lenin\'s loyal follower'],
             judge='His rivals\' mistakes helped, but Stalin won mainly because he used the power of the General Secretary\'s post skilfully'),
        dict(q='How important was terror in keeping Stalin in power in the 1930s?',
             pro=['The purges removed every possible rival', 'Fear of arrest and the gulags silenced criticism'],
             con=['The cult of personality presented Stalin as a hero', 'Propaganda and censorship controlled information', 'Many genuinely supported him for industrial progress and education'],
             judge='Terror was the key method, but it worked alongside propaganda and the cult of personality'),
    ],
    'src': [
        S('Lenin\'s Testament, a note added in January 1923 (translated extract)', 'Stalin is too rude and this defect, although quite tolerable in our midst and in dealings among us Communists, becomes intolerable in a Secretary-General.',
          'Lenin\'s view of Stalin', 'Lenin criticises Stalin\'s personality and suggests he should not remain General Secretary.',
          'To advise the party leadership about his possible successors.',
          'it is Lenin\'s own judgement of Stalin', 'Lenin was ill and had recently quarrelled with Stalin',
          'That the Testament was not made public, which helped Stalin.', stance=None, published=False),
        S('a Soviet poster of the late 1930s (description of a typical design)', 'Stalin is shown standing beside Lenin, smiling, as crowds of workers and children cheer below a red banner.',
          'Stalin\'s image', 'It presents Stalin as Lenin\'s natural successor and a popular, caring leader.',
          'To build the cult of personality and link Stalin to Lenin.',
          'it shows how Stalin wanted to be seen', 'it is propaganda that hides the purges',
          'That millions were arrested and sent to the gulags.', stance=None, visual=True),
    ],
})


r3e = T("The impact of Stalin's economic policies: collectivisation and the Five-Year Plans", 'collectivisation', 'five-year plans')
build(r3e, {
    'enq': 'Stalin\'s economic policies', 'claim': 'Stalin\'s economic policies were a success',
    'stim': ['In 1928 Stalin launched the first Five-Year Plan.', 'From 1929 Soviet peasants were forced to join collective farms.',
             'In 1931 Stalin warned that the USSR was “fifty or a hundred years behind the advanced countries”.'],
    'terms': [
        ('collectivisation', 'combining small peasant farms into large state-controlled collective farms'),
        ('kolkhoz', 'a collective farm, run by peasants who shared the land and produce under state control'),
        ('kulak', 'a richer peasant; Stalin ordered the “liquidation of the kulaks as a class”'),
        ('Five-Year Plan', 'a central plan setting production targets for industry over five years'),
        ('Gosplan', 'the state planning agency that set the targets for the Five-Year Plans'),
        ('Stakhanovite', 'a worker who exceeded targets, named after the miner Alexei Stakhanov'),
        ('Magnitogorsk', 'a huge new industrial city built in the Urals during the first Five-Year Plan'),
    ],
    'dates': [('the first Five-Year Plan began', 1928), ('Stalin announced the liquidation of the kulaks', 1929), ('a devastating famine struck Ukraine and other regions', 1932),
              ('the second Five-Year Plan began', 1933), ('Alexei Stakhanov mined 102 tonnes of coal in one shift', 1935), ('the third Five-Year Plan began', 1938)],
    'mcq': [
        ('Why did Stalin want rapid industrialisation?', 'To make the USSR strong enough to defend itself against capitalist enemies', ['To join the League of Nations', 'To end communism', 'To please the kulaks'], '[1]'),
        ('How did many peasants react to collectivisation?', 'They slaughtered their animals and burned crops rather than hand them over', ['They welcomed it and joined at once', 'They moved to the USA', 'They became Nepmen'], 'Numbers of cattle and pigs roughly halved. [1]'),
        ('Which of these industries was given priority in the first Five-Year Plan?', 'Heavy industry such as coal, steel and electricity', ['Clothing and shoes', 'Toys and household goods', 'Tourism'], '[1]'),
        ('What happened in the famine of 1932-33?', 'Millions died, especially in Ukraine and Kazakhstan', ['Grain exports stopped completely', 'Collective farms were abolished', 'The kulaks took over the government'], 'Grain was still being exported. [1]'),
    ],
    'a': [
        ('Describe the process of collectivisation.', 'features of collectivisation',
         ['Small peasant farms were merged into large collective farms (kolkhozes)', 'The state took a fixed share of the grain', 'Machine Tractor Stations supplied tractors', 'Peasants who resisted were labelled kulaks and deported or killed', 'Peasants slaughtered animals in protest and production fell']),
        ('Describe the Five-Year Plans.', 'features of the Five-Year Plans',
         ['Gosplan set production targets for every industry', 'Heavy industry such as coal, steel, oil and electricity was the priority', 'New industrial cities such as Magnitogorsk were built', 'Huge projects such as the Dnieper dam and the Moscow metro were completed', 'Workers faced harsh discipline, and gulag prisoners provided forced labour']),
    ],
    'b': [
        ('Why did Stalin introduce collectivisation?',
         ['To produce more grain to feed the growing industrial cities', 'To sell grain abroad to pay for machinery', 'To bring the peasants under state control', 'To destroy the kulaks, whom he saw as capitalist enemies', 'Small, old-fashioned farms were inefficient']),
        ('Why were the Five-Year Plans able to increase industrial production so quickly?',
         ['Huge resources were directed into heavy industry', 'Propaganda and rewards, such as the Stakhanovite movement, encouraged workers', 'Harsh discipline and punishment for failing to meet targets', 'Forced labour from the gulags built many projects', 'Foreign experts and machinery were brought in']),
    ],
    'claims': [
        ('Collectivisation increased the number of farm animals in the USSR.', False, 'Peasants slaughtered their animals in protest; numbers of cattle and pigs roughly halved.'),
        ('The Five-Year Plans gave priority to heavy industry.', True, 'Coal, steel, oil and electricity were the main targets.'),
        ('Living standards for most Soviet workers rose rapidly during the first Five-Year Plan.', False, 'Consumer goods were neglected, housing was overcrowded and real wages fell in the early 1930s.'),
    ],
    'c': [
        dict(q='‘Stalin\'s economic policies were a success.’',
             pro=['Industrial output grew rapidly: coal production rose from about 35 to 128 million tonnes between 1928 and 1937', 'New industrial cities, dams and railways were built', 'The USSR was able to produce the weapons that helped defeat Germany after 1941'],
             con=['Collectivisation caused a famine in which millions died', 'Grain and livestock production fell', 'Consumer goods and housing were neglected', 'Millions of forced labourers suffered and died in the gulags'],
             judge='The policies achieved Stalin\'s aim of rapid industrialisation, but at an enormous human cost, so they were a success only by his own narrow measure'),
        dict(q='How far did collectivisation achieve its aims?',
             pro=['The state gained control over peasants and grain supplies', 'The kulaks were destroyed', 'Grain was exported to pay for industrial machinery'],
             con=['Grain production fell in the early 1930s', 'Famine killed millions', 'Livestock numbers collapsed and took years to recover'],
             judge='Collectivisation achieved Stalin\'s political aims of control, but failed to increase food production'),
    ],
    'src': [
        S('a speech by Stalin to industrial managers, February 1931 (extract)', 'We are fifty or a hundred years behind the advanced countries. We must make good this distance in ten years. Either we do it, or they will crush us.',
          'the reasons for rapid industrialisation', 'Stalin argues that the USSR must industrialise at great speed or be destroyed by its enemies.',
          'To drive managers to meet the targets of the Five-Year Plan.',
          'it is Stalin\'s own explanation of his aims', 'it was meant to inspire and pressurise, so it presents the threat in the starkest terms',
          'The human cost of the plans, such as the famine of 1932-33.', stance=None),
        S('the memoirs of a former Soviet official who fled to the West, published in 1946 (illustrative)', 'In the villages I saw empty houses and starving children. The grain had been taken to the cities and abroad. Nobody was allowed to speak of famine.',
          'the effects of collectivisation', 'It shows that collectivisation caused famine and that the government hid it.',
          'To expose the realities of Stalin\'s policies to Western readers.',
          'the writer saw events at first hand', 'he had fled the USSR and was writing against Stalin, so he may exaggerate',
          'The growth in industrial production.', stance=False, why='it shows the human cost of the policies'),
    ],
})


@r3e.add('C3', (1, 2, 3, 4, 5), 'numerical')
def r3e_output(r, D):
    name, a, b, c = r.choice(FYP)
    y1, v1, y2, v2 = r.choice([(1928, a, 1932, b), (1932, b, 1937, c), (1928, a, 1937, c)])
    pc = 100 * (v2 - v1) / v1
    fac = v2 / v1
    tbl = 'Official Soviet production figures (million tonnes): ' + ' '.join(f'{n}: 1928 {x}, 1932 {y}, 1937 {z}.' for n, x, y, z in FYP)
    if D <= 2:
        return {'stem': f'Study the figures. {tbl} Calculate the percentage increase in {name.lower()} production between {y1} and {y2}.',
                'answer': f'{pc:.0f}%', 'key': f'({v2} − {v1}) ÷ {v1} × 100 = {pc:.0f}%. 1 mark method, 1 mark answer [2]', 'type': 'numerical', 'marks': 2, 'minutes': 3}
    return {'stem': f'Study the figures. {tbl} (a) By how many times did {name.lower()} production increase between {y1} and {y2}? [2] (b) Give two reasons why a historian should treat these figures with caution. [2] '
                    '(c) Explain how the Five-Year Plans achieved such increases. [4]',
            'answer': f'(a) {v2} ÷ {v1} ≈ {fac:.1f} times. (b) They are official figures, and managers had reasons to exaggerate output to meet targets; they show quantity, not quality, and say nothing about the human cost. '
                      '(c) Resources were concentrated on heavy industry; new plants such as Magnitogorsk were built; workers were driven by targets, propaganda (Stakhanovites) and punishment; gulag labour was used.',
            'key': f'(a) {fac:.1f} times, 1 mark method, 1 mark answer [2] (b) 1 mark each reason [2] (c) 1 mark per explained point up to [4]', 'type': 'numerical', 'marks': 8, 'minutes': 12}


CHAPTERS[3] = [r3a, r3b, r3c, r3d, r3e]


# ============================================================== CHAPTER 4: Depth Study D, the USA 1919-41

US_UNEMP = [(1929, 3.2), (1930, 8.7), (1931, 15.9), (1932, 23.6), (1933, 24.9), (1934, 21.7), (1935, 20.1), (1936, 16.9), (1937, 14.3), (1938, 19.0), (1939, 17.2), (1940, 14.6), (1941, 9.9)]

u4a = T('How far the US economy boomed in the 1920s: mass production, credit and the groups left out', 'us economy boomed', 'mass production', 'groups left out')
build(u4a, {
    'enq': 'the US economy in the 1920s', 'claim': 'all Americans shared in the prosperity of the 1920s',
    'stim': ['In the 1920s the USA became the richest country in the world.', 'By the late 1920s Henry Ford\'s factories were producing a new car every few seconds.',
             'Not all Americans shared in the prosperity of the 1920s.'],
    'terms': [
        ('mass production', 'making large numbers of identical goods quickly and cheaply, for example on an assembly line'),
        ('assembly line', 'a production method in which a product moves past workers who each do one task'),
        ('hire purchase', 'buying goods by paying in instalments over time'),
        ('laissez-faire', 'the policy that the government should not interfere in the economy'),
        ('tariff', 'a tax on imported goods, such as the Fordney-McCumber tariff of 1922'),
        ('overproduction', 'producing more goods than people can afford to buy'),
        ('consumer goods', 'goods bought by households, such as radios, refrigerators and cars'),
    ],
    'dates': [('Ford introduced the moving assembly line', 1913), ('the Fordney-McCumber tariff was passed', 1922), ('Calvin Coolidge became President', 1923), ('Ford produced its 15 millionth Model T', 1927), ('Herbert Hoover became President', 1929)],
    'mcq': [
        ('Which of these was a Republican policy that helped the boom of the 1920s?', 'High tariffs on imported goods', ['Heavy taxes on the rich', 'Nationalisation of industry', 'Strict controls on banks'], '[1]'),
        ('Which group did NOT share in the prosperity of the 1920s?', 'Farmers', ['Car manufacturers', 'Electrical goods producers', 'Advertising agencies'], 'Prices fell because of overproduction and loss of European markets. [1]'),
        ('How did hire purchase help the boom?', 'It allowed people to buy goods they could not afford immediately', ['It lowered taxes on imports', 'It ended unemployment in coal mining', 'It was paid for by the government'], '[1]'),
        ('Which President said in 1925 that “the chief business of the American people is business”?', 'Calvin Coolidge', ['Woodrow Wilson', 'Franklin D. Roosevelt', 'Warren Harding'], '[1]'),
    ],
    'a': [
        ('Describe how mass production changed the car industry in the 1920s.', 'effects of mass production on the car industry',
         ['Ford\'s moving assembly line cut the time to build a Model T to about 90 minutes', 'The price of a Model T fell to under $300 by the mid-1920s', 'Car ownership rose rapidly to over 20 million by 1929', 'The car industry boosted related industries such as steel, rubber, glass and oil', 'Road building, garages and motels created new jobs']),
        ('Describe the groups that did not share in the prosperity of the 1920s.', 'groups that did not share in the prosperity of the 1920s',
         ['Farmers faced falling prices because of overproduction', 'Workers in old industries such as coal and textiles faced wage cuts and unemployment', 'Many African Americans in the South lived in poverty as sharecroppers', 'Native Americans lived on poor reservation land', 'Many new immigrants worked in low-paid jobs']),
    ],
    'b': [
        ('Why did the US economy boom in the 1920s?',
         ['The USA had gained from the First World War, supplying the Allies and taking over their markets', 'Mass production made goods cheaper', 'Hire purchase and credit allowed people to buy more', 'Republican policies of low taxes, high tariffs and laissez-faire encouraged business', 'Advertising and new industries such as cars, radios and electrical goods created demand']),
        ('Why did farmers not share in the boom?',
         ['Demand from Europe fell after the war', 'New machinery led to overproduction, so prices fell', 'Competition from Canada and Argentina', 'Tariffs led other countries to tax American food exports', 'Many farmers were in debt from buying land and machinery']),
    ],
    'claims': [
        ('The prosperity of the 1920s was shared equally by all Americans.', False, 'Farmers, workers in old industries, many African Americans and Native Americans did not share in it.'),
        ('Hire purchase allowed Americans to buy consumer goods in instalments.', True, 'It greatly increased sales of cars and electrical goods.'),
        ('The Republican governments of the 1920s regulated business closely.', False, 'They followed laissez-faire, keeping regulation and taxes low.'),
    ],
    'c': [
        dict(q='‘The most important reason for the boom of the 1920s was mass production.’',
             pro=['It made cars and consumer goods cheap enough for millions', 'The car industry stimulated steel, rubber, oil and road building'],
             con=['Credit and hire purchase increased demand', 'Republican policies encouraged business', 'The First World War had left the USA in a strong economic position', 'Advertising created new wants'],
             judge='Mass production was central, but it depended on credit, advertising and the economic advantages left by the war to create demand'),
        dict(q='How far did Americans share in the prosperity of the 1920s?',
             pro=['Many middle-class families bought cars, radios and electrical goods', 'Wages rose for many industrial workers', 'Share ownership spread'],
             con=['Farmers suffered from falling prices', 'Workers in coal and textiles faced unemployment and wage cuts', 'Many African Americans and Native Americans remained very poor', 'Wealth was concentrated among the richest Americans'],
             judge='Prosperity was real for the urban middle class but was not shared by large groups, which helps to explain the later crash'),
    ],
    'src': [
        S('an advertisement for an electric refrigerator in an American magazine, 1928 (description of a typical design)', 'A smiling housewife opens a gleaming refrigerator full of food. The text says it can be bought “for a few dollars a month”.',
          'consumer society in the 1920s', 'It shows how new consumer goods were marketed to families and how credit made them affordable.',
          'To persuade readers to buy a refrigerator on credit.',
          'it shows how goods were sold to consumers at the time', 'it is an advertisement and shows an idealised picture',
          'That many Americans, such as farmers, could not afford such goods.', stance=True, why='it presents prosperity as available to ordinary families', visual=True),
        S('a letter from a farmer in Iowa to a newspaper, 1927 (illustrative)', 'We grow more corn than ever, but we sell it for less than it costs to grow. The bank wants its money. We read about the good times in the cities, but we have never seen them.',
          'farming in the 1920s', 'It shows that farmers suffered from falling prices and debt while the cities prospered.',
          'To protest about the situation of farmers and ask for help.',
          'it is a first-hand account from a farmer', 'it is one person\'s view, written to complain',
          'The growth of new industries such as cars and electrical goods.', stance=False, why='it shows farmers did not share in the prosperity'),
    ],
})

u4b = T('How far US society changed in the 1920s: Prohibition, intolerance, immigration and the Roaring Twenties', 'us society changed', 'prohibition', 'intolerance', 'roaring twenties')
build(u4b, {
    'enq': 'American society in the 1920s', 'claim': 'the 1920s were a time of intolerance in the USA',
    'stim': ['In January 1920 Prohibition banned the manufacture and sale of alcohol in the USA.', 'The 1920s are often called the “Roaring Twenties”.',
             'In the 1920s the Ku Klux Klan claimed millions of members.'],
    'terms': [
        ('Prohibition', 'the ban on making, selling and transporting alcohol, from 1920 to 1933'),
        ('speakeasy', 'an illegal bar selling alcohol during Prohibition'),
        ('bootlegger', 'a person who made or smuggled illegal alcohol'),
        ('Red Scare', 'the fear of communists and anarchists in the USA in 1919-20'),
        ('Ku Klux Klan', 'the white supremacist organisation that attacked African Americans, Jews, Catholics and immigrants'),
        ('flapper', 'a young woman of the 1920s who challenged traditional behaviour, with short hair and skirts'),
        ('Harlem Renaissance', 'the flowering of African American art, literature and music in New York in the 1920s'),
    ],
    'dates': [('Prohibition came into force', 1920, 1), ('Sacco and Vanzetti were arrested', 1920, 5), ('the Johnson-Reed Act restricted immigration', 1924), ('the Scopes “Monkey Trial” took place', 1925),
              ('The Jazz Singer, the first full-length “talkie”, was released', 1927, 10), ('Sacco and Vanzetti were executed', 1927, 8), ('the St Valentine\'s Day Massacre took place in Chicago', 1929), ('Prohibition was ended', 1933)],
    'mcq': [
        ('Which gangster controlled much of the illegal alcohol trade in Chicago?', 'Al Capone', ['Eliot Ness', 'Bartolomeo Vanzetti', 'Henry Ford'], '[1]'),
        ('What did the Johnson-Reed (Immigration) Act of 1924 do?', 'Set quotas that favoured immigrants from northern and western Europe', ['Banned all immigration', 'Encouraged immigrants from Asia', 'Gave citizenship to all immigrants'], '[1]'),
        ('Why were Sacco and Vanzetti\'s trial seen as unfair?', 'They were Italian immigrants and anarchists, and prejudice influenced the trial', ['They were never charged', 'They were tried in Russia', 'They had confessed under torture by the FBI'], '[1]'),
        ('What was the Scopes Trial of 1925 about?', 'A teacher who broke a Tennessee law by teaching evolution', ['A bootlegger selling alcohol', 'An immigrant accused of murder', 'A Klan leader accused of violence'], '[1]'),
    ],
    'a': [
        ('Describe the problems caused by Prohibition.', 'problems caused by Prohibition',
         ['Speakeasies sold illegal alcohol in their thousands', 'Bootleggers smuggled alcohol, and moonshine could be poisonous', 'Organised crime grew, with gangsters such as Al Capone', 'Police and officials were bribed', 'Gang violence, such as the St Valentine\'s Day Massacre in 1929']),
        ('Describe the activities of the Ku Klux Klan in the 1920s.', 'activities of the Ku Klux Klan in the 1920s',
         ['It attacked African Americans, Jews, Catholics and immigrants', 'Members wore white robes and burned crosses', 'It carried out beatings and lynchings', 'It held mass marches, including in Washington in 1925', 'It had millions of members and influence in some state governments']),
        ('Describe how the lives of some women changed in the 1920s.', 'changes in the lives of some women in the 1920s',
         ['Women gained the vote in national elections in 1920', 'More women worked, for example as secretaries and shop assistants', 'Flappers wore short skirts and short hair, smoked and danced in public', 'Labour-saving devices reduced housework for some', 'Many women, especially in rural areas, saw little change']),
    ],
    'b': [
        ('Why was Prohibition introduced?',
         ['Temperance groups such as the Anti-Saloon League campaigned against alcohol', 'Many Protestants in rural areas believed alcohol was sinful', 'Alcohol was linked to crime, poverty and violence in the family', 'During the First World War, beer was linked with German brewers and grain was needed for food']),
        ('Why did intolerance increase in the USA in the 1920s?',
         ['Fear of communism after the Russian Revolution led to the Red Scare', 'Many Americans feared that immigrants threatened jobs and American values', 'Racism against African Americans was widespread, especially in the South', 'Religious fundamentalists felt threatened by modern ideas', 'The Klan exploited these fears']),
        ('Why was Prohibition ended in 1933?',
         ['It was widely ignored and could not be enforced', 'It encouraged organised crime and corruption', 'The government lost large amounts of tax revenue', 'After the Depression began, legal brewing would create jobs', 'Roosevelt promised to end it']),
    ],
    'claims': [
        ('Prohibition stopped Americans from drinking alcohol.', False, 'Alcohol was widely available in speakeasies and through bootleggers.'),
        ('Women gained the right to vote in national elections in 1920.', True, 'The 19th Amendment was ratified in 1920.'),
        ('Immigration to the USA increased because of the laws passed in the 1920s.', False, 'Quota laws in 1921 and 1924 sharply reduced immigration, especially from southern and eastern Europe.'),
    ],
    'c': [
        dict(q='‘The 1920s were a time of intolerance rather than freedom in the USA.’',
             pro=['The Red Scare and the Sacco and Vanzetti case', 'The Klan had millions of members', 'Immigration laws discriminated against southern and eastern Europeans and Asians', 'The Scopes Trial showed hostility to new ideas'],
             con=['Jazz, cinema and the Harlem Renaissance showed cultural freedom', 'Some women gained new freedoms', 'Millions ignored Prohibition', 'Consumer society gave many more choice'],
             judge='The 1920s saw both new freedoms for some urban Americans and strong intolerance towards minorities; for many groups intolerance was the stronger experience'),
        dict(q='How far did the lives of women change in the 1920s?',
             pro=['Women gained the vote in 1920', 'More women worked and some had more social freedom, such as flappers', 'Labour-saving devices reduced housework'],
             con=['Most women still did low-paid jobs and earned less than men', 'Flappers were a minority, mainly young, urban and middle class', 'Rural and poor women saw little change'],
             judge='Some women\'s lives changed significantly, but for most the changes were limited'),
    ],
    'src': [
        S('a photograph of officials pouring alcohol into a sewer, New York, 1921 (description)', 'Police and Prohibition agents watch as barrels of beer and liquor are emptied into a drain while a crowd looks on.',
          'the enforcement of Prohibition', 'It shows the authorities trying to enforce Prohibition publicly.',
          'To show that Prohibition was being enforced and to warn lawbreakers.',
          'it is a photograph taken at the time', 'it may have been staged for publicity and does not show how much alcohol escaped the law',
          'That speakeasies and bootlegging were widespread.', stance=None, visual=True),
        S('a pamphlet published by the Ku Klux Klan, 1924 (summary of a typical pamphlet)', 'The pamphlet claimed that Catholics, Jews and immigrants were a danger to “true Americanism” and called on white Protestant Americans to defend their country.',
          'Klan ideas in the 1920s', 'It shows the Klan targeted many groups as un-American.',
          'To recruit members by playing on fears of immigrants and minorities.',
          'it shows the Klan\'s own message', 'it is propaganda by an extremist organisation',
          'How many Americans opposed the Klan.', stance=True, why='it shows intolerance being spread widely'),
    ],
})

u4c = T('The causes and consequences of the Wall Street Crash', 'wall street crash')
build(u4c, {
    'enq': 'the Wall Street Crash and the Depression', 'claim': 'speculation was the main cause of the Wall Street Crash',
    'stim': ['On 24 October 1929, “Black Thursday”, nearly 13 million shares were sold on the New York Stock Exchange.', 'By 1933 about a quarter of American workers were unemployed.',
             'In the late 1920s millions of Americans bought shares, many with borrowed money.'],
    'terms': [
        ('speculation', 'buying shares in the hope of selling them quickly at a higher price'),
        ('buying on the margin', 'buying shares with a small deposit and borrowing the rest'),
        ('Black Tuesday', '29 October 1929, the worst day of the Wall Street Crash, when over 16 million shares were sold'),
        ('Hooverville', 'a shanty town of homeless people, named mockingly after President Hoover'),
        ('Bonus Army', 'the First World War veterans who marched on Washington in 1932 demanding early payment of a bonus'),
        ('Dust Bowl', 'the drought-hit area of the Great Plains in the 1930s, where soil blew away in huge dust storms'),
        ('rugged individualism', 'Hoover\'s belief that people should solve their problems through their own efforts, not government help'),
    ],
    'dates': [('share prices reached their peak', 1929, 9), ('Black Thursday', 1929, 10.24), ('Black Tuesday', 1929, 10.29), ('the Hawley-Smoot tariff was passed', 1930, 6),
              ('the Reconstruction Finance Corporation was set up', 1932, 1), ('the Bonus Army was driven out of Washington', 1932, 7)],
    'mcq': [
        ('Why did buying shares “on the margin” make the crash worse?', 'Investors had to sell when prices fell to repay their loans, pushing prices down further', ['It meant shares could never fall', 'It made shares illegal', 'It was only used by the government'], '[1]'),
        ('What percentage of American workers were unemployed in 1933?', 'About 25 per cent', ['About 3 per cent', 'About 10 per cent', 'About 50 per cent'], '[1]'),
        ('How did Hoover respond to the Bonus Army in 1932?', 'Troops were used to drive the veterans out of Washington', ['He paid the bonus at once', 'He invited them to the White House', 'He made them part of the army'], 'This badly damaged his reputation. [1]'),
        ('What was the main weakness of the American banking system in 1929?', 'There were thousands of small, independent banks with few reserves', ['Banks were all owned by the government', 'Banks were not allowed to lend money', 'There was only one bank'], '[1]'),
    ],
    'a': [
        ('Describe the events of the Wall Street Crash in October 1929.', 'events of the Wall Street Crash',
         ['Share prices began to fall in September 1929', 'On Black Thursday, 24 October, nearly 13 million shares were sold', 'Bankers tried to support prices by buying shares', 'On Black Tuesday, 29 October, over 16 million shares were sold and prices collapsed', 'Many investors, including those who had bought on the margin, were ruined']),
        ('Describe the effects of the Depression on American people.', 'effects of the Depression on American people',
         ['Unemployment reached about a quarter of the workforce by 1933', 'Thousands of banks failed and people lost their savings', 'Many families lost their homes and lived in Hoovervilles', 'Farmers were evicted when they could not repay debts; the Dust Bowl made things worse', 'People queued at soup kitchens and travelled the country looking for work']),
    ],
    'b': [
        ('Why did the Wall Street Crash happen?',
         ['Speculation had pushed share prices far above the real value of companies', 'Many shares were bought on the margin with borrowed money', 'Overproduction meant companies\' profits began to fall', 'Unequal distribution of wealth limited demand for goods', 'When confidence fell, panic selling caused prices to collapse']),
        ('Why did the Wall Street Crash lead to a depression?',
         ['Banks lost money and many collapsed, wiping out savings', 'People lost confidence and stopped spending', 'Companies cut production and laid off workers', 'Falling trade, made worse by the Hawley-Smoot tariff, hit exports', 'Unemployment reduced demand further in a vicious circle']),
        ('Why did Hoover become unpopular during the Depression?',
         ['He believed in rugged individualism and limited government help', 'He claimed recovery was close when conditions were worsening', 'His measures, such as the Reconstruction Finance Corporation, were too little, too late', 'Troops were used against the Bonus Army in 1932']),
    ],
    'claims': [
        ('The Wall Street Crash was caused only by panic on Black Thursday.', False, 'Panic was the trigger; underlying causes included speculation, buying on the margin, overproduction and weak banks.'),
        ('Thousands of American banks failed in the early 1930s.', True, 'Many small banks had lent money for speculation and collapsed.'),
        ('Hoover did nothing at all to deal with the Depression.', False, 'He set up the Reconstruction Finance Corporation and some public works, but his measures were limited.'),
    ],
    'c': [
        dict(q='‘Speculation was the main cause of the Wall Street Crash.’',
             pro=['Share prices rose far beyond the value of companies', 'Buying on the margin meant falling prices forced sales and panic'],
             con=['Overproduction meant falling profits, which undermined confidence', 'Unequal distribution of wealth limited demand', 'Weak, unregulated banks lent recklessly', 'Tariffs reduced foreign markets'],
             judge='Speculation made the crash so sudden and severe, but the underlying weaknesses of the economy explain why it happened'),
        dict(q='How far was Hoover to blame for the Depression?',
             pro=['His laissez-faire beliefs limited the government\'s response', 'The Hawley-Smoot tariff made world trade worse', 'His treatment of the Bonus Army showed he was out of touch'],
             con=['The causes of the crash lay in the 1920s boom, before he took office', 'He did take some action, such as the RFC', 'The Depression was worldwide'],
             judge='Hoover did not cause the Depression, but his limited response made it worse and longer'),
    ],
    'src': [
        S('a photograph of a Hooverville in Seattle, 1933 (description)', 'Dozens of shacks built from scrap wood, metal sheets and cardboard stand on waste ground beside the waterfront.',
          'the effects of the Depression', 'It shows that many Americans lost their homes and had to live in makeshift shanty towns.',
          'To record living conditions during the Depression.',
          'it is a photograph from the time', 'it shows one place and may have been chosen to show the worst conditions',
          'How many people lived in Hoovervilles, or that the middle class was also affected.', stance=None, visual=True),
        S('an extract from a modern history textbook (illustrative)', 'The crash did not come out of a clear sky. Farmers had been suffering for years, factories were producing more than Americans could buy, and wealth was concentrated in too few hands.',
          'the causes of the crash', 'It argues the crash resulted from long-term weaknesses in the economy, not just speculation.',
          'To explain to students the deeper causes of the crash.',
          'it is written with hindsight', 'it is a short summary and does not discuss the role of speculation',
          'The role of buying on the margin and panic selling.', stance=False, why='it stresses underlying weaknesses rather than speculation', kind='secondary', published=True),
    ],
})

u4d = T("How successful was the New Deal? Roosevelt's alphabet agencies and opposition", 'new deal', 'alphabet agencies')
build(u4d, {
    'enq': 'the New Deal', 'claim': 'the New Deal was a success',
    'stim': ['In March 1933 Franklin D. Roosevelt became President of the USA.', 'In his first Hundred Days Roosevelt passed a series of laws known as the New Deal.',
             'The New Deal faced strong opposition from both the right and the left.'],
    'terms': [
        ('New Deal', 'Roosevelt\'s programme of relief, recovery and reform to deal with the Depression'),
        ('Hundred Days', 'Roosevelt\'s first hundred days in office in 1933, when many New Deal laws were passed'),
        ('fireside chats', 'Roosevelt\'s radio talks to the American people explaining his policies'),
        ('Civilian Conservation Corps (CCC)', 'the agency that gave young men work on conservation projects such as planting trees'),
        ('Tennessee Valley Authority (TVA)', 'the agency that built dams to control floods and provide electricity in a poor region'),
        ('Agricultural Adjustment Administration (AAA)', 'the agency that paid farmers to produce less in order to raise prices'),
        ('Social Security Act', 'the 1935 law providing old-age pensions and unemployment insurance'),
    ],
    'dates': [('Roosevelt won the presidential election', 1932, 11), ('Roosevelt declared a bank holiday', 1933, 3), ('the Supreme Court ruled the NRA unconstitutional', 1935, 5), ('the Social Security Act was passed', 1935, 8),
              ('Roosevelt proposed adding judges to the Supreme Court', 1937, 2), ('a new recession hit the US economy', 1937, 9)],
    'mcq': [
        ('What was the purpose of the Emergency Banking Act of 1933?', 'To restore confidence by closing banks and reopening only sound ones', ['To abolish all banks', 'To nationalise all industry', 'To end Prohibition'], '[1]'),
        ('Which body ruled several New Deal measures unconstitutional?', 'The Supreme Court', ['The Senate', 'The Federal Reserve', 'The League of Nations'], 'For example the NRA in 1935 and the AAA in 1936. [1]'),
        ('Which critic of the New Deal proposed a “Share Our Wealth” scheme?', 'Huey Long', ['Father Coughlin', 'Dr Francis Townsend', 'Herbert Hoover'], '[1]'),
        ('What finally ended mass unemployment in the USA?', 'Rearmament and the Second World War', ['The Social Security Act', 'The AAA', 'The 1937 recession'], '[1]'),
    ],
    'a': [
        ('Describe the work of the alphabet agencies.', 'alphabet agencies and what they did',
         ['The CCC gave young men work on conservation projects', 'The TVA built dams to provide electricity and control floods', 'The AAA paid farmers to cut production to raise prices', 'The PWA and later the WPA created jobs building roads, schools and hospitals', 'The NRA set codes on wages, prices and hours']),
        ('Describe the opposition to the New Deal.', 'sources of opposition to the New Deal',
         ['Republicans and business leaders said it was too expensive and interfered with free enterprise', 'The Supreme Court ruled some measures unconstitutional', 'Huey Long argued it did not go far enough and proposed “Share Our Wealth”', 'Father Coughlin attacked Roosevelt on the radio', 'Some said it gave too much power to the federal government']),
    ],
    'b': [
        ('Why did Roosevelt win the 1932 election?',
         ['Hoover was blamed for the Depression', 'Roosevelt promised a “New Deal” and action to tackle unemployment', 'He was an energetic, confident campaigner', 'Hoover\'s treatment of the Bonus Army damaged him']),
        ('Why did the New Deal face opposition?',
         ['Businessmen disliked regulation, higher taxes and support for trade unions', 'Republicans believed it was too costly and un-American', 'The Supreme Court believed it gave the federal government too much power', 'Radicals such as Huey Long thought it did too little for the poor', 'Roosevelt\'s plan to add judges to the Supreme Court in 1937 alarmed many']),
    ],
    'claims': [
        ('The New Deal ended unemployment in the USA by 1939.', False, 'Unemployment was still about 17 per cent in 1939; rearmament and the war ended it.'),
        ('Roosevelt used radio “fireside chats” to explain his policies.', True, 'They helped restore confidence, for example in the banks in 1933.'),
        ('The Supreme Court supported every New Deal law.', False, 'It ruled the NRA and the AAA unconstitutional.'),
    ],
    'c': [
        dict(q='‘The New Deal was a success.’',
             pro=['It restored confidence in the banks and government', 'Agencies such as the CCC, PWA and WPA gave work to millions', 'The TVA transformed a poor region', 'The Social Security Act created lasting welfare reforms'],
             con=['Unemployment remained high, about 19 per cent in 1938', 'The 1937 recession showed recovery was fragile', 'African Americans and women gained less', 'The AAA helped landowners more than sharecroppers'],
             judge='The New Deal succeeded in relief and reform and restored confidence, but it did not achieve full recovery, which came only with war'),
        dict(q='How important was opposition in limiting the New Deal?',
             pro=['The Supreme Court struck down key measures', 'Business opposition limited reform', 'The failed court-packing plan of 1937 weakened Roosevelt'],
             con=['Roosevelt won landslide re-elections in 1936 and 1940', 'The Second New Deal went further despite opposition', 'Economic limits, such as the 1937 recession, were more important'],
             judge='Opposition slowed and shaped the New Deal, but Roosevelt\'s popularity meant it could not stop it'),
    ],
    'src': [
        S('Roosevelt\'s inaugural address, 4 March 1933 (extract)', 'So, first of all, let me assert my firm belief that the only thing we have to fear is fear itself.',
          'Roosevelt\'s approach to the Depression', 'Roosevelt tells Americans that panic and lack of confidence are the main danger and that they must not give in to fear.',
          'To restore public confidence at the height of the banking crisis.',
          'it is Roosevelt\'s own words at the start of his presidency', 'it is a speech intended to inspire, and says nothing about the policies themselves',
          'The measures of the Hundred Days, such as the Emergency Banking Act.', stance=None),
        S('a cartoon published in an American newspaper opposed to Roosevelt, 1935 (description of a typical design)', 'Roosevelt is shown as a doctor giving a sick Uncle Sam a huge spoonful of medicine labelled with letters such as CCC, AAA and NRA, while a large bill for the cost is pinned to the wall.',
          'opposition to the New Deal', 'The cartoonist suggests the New Deal was expensive and that its agencies were being forced on the country.',
          'To criticise the cost and scale of the New Deal.',
          'it shows how opponents viewed the New Deal at the time', 'it is from an opposition newspaper, so it is one-sided',
          'That millions found work through the agencies.', stance=False, why='it presents the New Deal as costly and doubtful', visual=True),
    ],
})


@u4d.add('C3', (1, 2, 3, 4, 5), 'numerical')
def u4d_unemp(r, D):
    tbl = 'US unemployment as a percentage of the workforce: ' + '; '.join(f'{y}: {p}%' for y, p in US_UNEMP) + '.'
    i, j = sorted(r.sample(range(len(US_UNEMP)), 2))
    (y1, p1), (y2, p2) = US_UNEMP[i], US_UNEMP[j]
    ch = round(p2 - p1, 1)
    if D <= 2:
        return {'stem': f'Study the figures. {tbl} By how many percentage points did unemployment change between {y1} and {y2}?',
                'answer': f'A {"rise" if ch > 0 else "fall"} of {abs(ch):.1f} percentage points ({p1}% to {p2}%)', 'key': f'{p2} − {p1} = {ch:+.1f} percentage points. 1 mark method, 1 mark answer [2]', 'type': 'numerical', 'marks': 2, 'minutes': 3}
    return {'stem': f'Study the figures. {tbl} (a) Identify the year when unemployment was highest. [1] (b) Calculate the change in unemployment between 1933 and 1937. [1] '
                    '(c) What happened between 1937 and 1938, and why? [2] (d) How far do these figures suggest that the New Deal was a success? [4]',
            'answer': '(a) 1933 (24.9%). (b) A fall of 10.6 percentage points (24.9% to 14.3%). (c) Unemployment rose to 19.0% in the 1937-38 recession, after Roosevelt cut government spending. '
                      '(d) They show a large fall from 1933 to 1937, suggesting success, but unemployment never fell below about 14% before the war, and fell below 10% only in 1941 with rearmament.',
            'key': '(a) 1933 [1] (b) −10.6 percentage points [1] (c) rise to 19.0%, linked to spending cuts [2] (d) 2 marks for a point supported from the figures each way, up to [4]', 'type': 'numerical', 'marks': 8, 'minutes': 12}


CHAPTERS[4] = [u4a, u4b, u4c, u4d]


# ============================================================== CHAPTER 5: Depth Study E, the Second World War 1939-c.1945

v5a = T('German successes, 1939-41: Blitzkrieg, Dunkirk and the Battle of Britain', 'german successes', 'blitzkrieg', 'dunkirk', 'battle of britain')
build(v5a, {
    'enq': 'German successes in 1939-41', 'claim': 'Blitzkrieg tactics were the main reason for German success in 1939-40',
    'stim': ['In September 1939 Germany conquered Poland in about five weeks.', 'In May and June 1940 German forces defeated France in six weeks.',
             'In the summer and autumn of 1940 the Luftwaffe tried to defeat the RAF.'],
    'terms': [
        ('Blitzkrieg', '“lightning war”, using fast attacks combining tanks, motorised infantry and aircraft to break through and encircle the enemy'),
        ('Phoney War', 'the period from September 1939 to April 1940 when there was little fighting in western Europe'),
        ('Operation Dynamo', 'the evacuation of British and French troops from Dunkirk in May-June 1940'),
        ('Maginot Line', 'the line of French fortifications along the border with Germany'),
        ('Luftwaffe', 'the German air force'),
        ('radar', 'a system using radio waves to detect aircraft, which gave the RAF early warning of attacks'),
        ('Operation Sea Lion', 'the planned German invasion of Britain, postponed in September 1940'),
    ],
    'dates': [('Germany invaded Poland', 1939, 9), ('Germany invaded Denmark and Norway', 1940, 4), ('Germany attacked the Netherlands, Belgium and France', 1940, 5.1),
              ('the Dunkirk evacuation began', 1940, 5.26), ('France signed an armistice with Germany', 1940, 6.22), ('the Blitz on London began', 1940, 9.07)],
    'mcq': [
        ('How many Allied troops were evacuated from Dunkirk?', 'About 338,000', ['About 3,000', 'About 33,000', 'About 3 million'], '[1]'),
        ('Through which region did German tanks break through in May 1940?', 'The Ardennes', ['The Maginot Line', 'The Alps', 'The Rhineland'], 'The French had thought the forest was impassable for tanks. [1]'),
        ('Why did the Luftwaffe switch to bombing London in September 1940?', 'Hitler ordered revenge after an RAF raid on Berlin', ['The RAF had been destroyed', 'London had no air defences', 'Britain had surrendered'], 'This gave the RAF time to repair its airfields. [1]'),
        ('Which aircraft were Britain\'s main fighters in the Battle of Britain?', 'Hurricanes and Spitfires', ['Lancasters and Wellingtons', 'Messerschmitts and Stukas', 'Zeros and Mustangs'], '[1]'),
    ],
    'a': [
        ('Describe Blitzkrieg tactics.', 'features of Blitzkrieg tactics',
         ['Aircraft such as Stuka dive-bombers attacked airfields, roads and defences', 'Tanks concentrated to break through at a weak point', 'Motorised infantry followed quickly to hold ground', 'Forces encircled the enemy rather than attacking head-on', 'Speed and surprise caused confusion and panic']),
        ('Describe the evacuation from Dunkirk in 1940.', 'features of the Dunkirk evacuation',
         ['British and French troops were trapped around Dunkirk after the German breakthrough', 'Hitler halted his tanks for several days', 'Operation Dynamo used naval ships and hundreds of small civilian boats', 'About 338,000 troops were rescued between 26 May and 4 June', 'Most heavy equipment was left behind']),
        ('Describe the Battle of Britain.', 'stages of the Battle of Britain',
         ['From July 1940 the Luftwaffe attacked shipping and ports in the Channel', 'In August it attacked RAF airfields and radar stations', 'The RAF was close to exhaustion by early September', 'On 7 September the Luftwaffe switched to bombing London', 'On 15 September heavy German losses showed the RAF was undefeated, and Sea Lion was postponed']),
    ],
    'b': [
        ('Why was Germany able to defeat France so quickly in 1940?',
         ['Blitzkrieg tactics combined tanks and aircraft effectively', 'The Germans attacked through the Ardennes, avoiding the Maginot Line', 'French and British tanks were spread out in support of infantry instead of concentrated', 'French commanders were slow and communications poor', 'The Allied armies moved into Belgium, leaving a gap the Germans exploited']),
        ('Why did the RAF win the Battle of Britain?',
         ['Radar gave early warning of German attacks', 'Spitfires and Hurricanes were effective fighters, and factories replaced losses quickly', 'The RAF fought over home territory, so shot-down pilots could fly again', 'The Luftwaffe switched from airfields to London in September', 'German fighters had limited fuel time over Britain']),
    ],
    'claims': [
        ('The Dunkirk evacuation was a military victory for Britain.', False, 'It rescued the army but was the result of a heavy defeat; most equipment was lost.'),
        ('Radar helped the RAF in the Battle of Britain.', True, 'The Chain Home system gave early warning so fighters could be sent where they were needed.'),
        ('The Germans broke through the Maginot Line to defeat France.', False, 'The main attack went through the Ardennes, round the north of the Maginot Line.'),
    ],
    'c': [
        dict(q='‘Blitzkrieg tactics were the main reason for German success in 1939-40.’',
             pro=['Concentrated tanks and aircraft broke through and encircled enemy forces', 'Speed caused panic and collapse in Poland and France'],
             con=['The Allies made mistakes, such as relying on the Maginot Line and moving into Belgium', 'France\'s leadership and communications were poor', 'The Nazi-Soviet Pact meant Germany had no war in the east', 'Poland was attacked from two sides'],
             judge='Blitzkrieg was very effective, but it succeeded because of Allied mistakes and the favourable position created by the Nazi-Soviet Pact'),
        dict(q='How important was the Battle of Britain?',
             pro=['It prevented a German invasion of Britain', 'Britain survived as a base for the later liberation of Europe', 'It was Hitler\'s first defeat'],
             con=['Germany was not seriously weakened', 'Hitler turned east to the USSR, where the war was decided', 'The Royal Navy might have prevented an invasion anyway'],
             judge='The Battle of Britain was very important in keeping Britain in the war, but its importance lay in what it made possible later'),
    ],
    'src': [
        S('a speech by Winston Churchill in the House of Commons, 20 August 1940 (extract)', 'Never in the field of human conflict was so much owed by so many to so few.',
          'the Battle of Britain', 'Churchill praises the RAF pilots, suggesting that the whole country owed its survival to them.',
          'To boost morale and pay tribute to the RAF at the height of the battle.',
          'it is the Prime Minister\'s own words at the time', 'it was intended to inspire and boost morale, not to analyse why the RAF was succeeding',
          'The role of radar, aircraft production or German mistakes.', stance=None),
        S('a speech by Winston Churchill in the House of Commons, 4 June 1940 (extract)', 'We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields and in the streets, we shall fight in the hills; we shall never surrender.',
          'British determination in 1940', 'Churchill tells Britain it will fight on whatever happens.',
          'To strengthen British resolve after Dunkirk and show the USA that Britain would fight on.',
          'it shows the determination of Britain\'s leader at the time', 'it was rhetoric to inspire, and earlier in the speech he warned that wars are not won by evacuations',
          'That most of the army\'s equipment had been lost in France.', stance=None),
    ],
})

v5b = T('The war on the Eastern Front: Operation Barbarossa to Stalingrad and Kursk', 'eastern front', 'barbarossa', 'stalingrad', 'kursk')
build(v5b, {
    'enq': 'the war on the Eastern Front', 'claim': 'the Battle of Stalingrad was the turning point of the war on the Eastern Front',
    'stim': ['On 22 June 1941 German forces invaded the Soviet Union in Operation Barbarossa.', 'In February 1943 the German Sixth Army surrendered at Stalingrad.',
             'In July 1943 the largest tank battle in history was fought at Kursk.'],
    'terms': [
        ('Operation Barbarossa', 'the German invasion of the USSR that began on 22 June 1941'),
        ('scorched earth', 'destroying crops, buildings and equipment when retreating so that the enemy cannot use them'),
        ('siege of Leningrad', 'the German blockade of Leningrad from 1941 to 1944, in which hundreds of thousands died'),
        ('Operation Uranus', 'the Soviet counter-attack of November 1942 that encircled the German Sixth Army at Stalingrad'),
        ('Lend-Lease', 'the US programme of supplying weapons and materials to its allies, including the USSR'),
        ('Battle of Kursk', 'the July 1943 battle in which the last major German offensive in the east was defeated'),
    ],
    'dates': [('Operation Barbarossa began', 1941, 6), ('the siege of Leningrad began', 1941, 9), ('the Soviet counter-attack before Moscow began', 1941, 12), ('the Germans attacked Stalingrad', 1942, 8),
              ('Soviet forces encircled the Sixth Army at Stalingrad', 1942, 11), ('the German Sixth Army surrendered at Stalingrad', 1943, 2), ('the Battle of Kursk was fought', 1943, 7)],
    'mcq': [
        ('Who commanded the German Sixth Army at Stalingrad?', 'Friedrich Paulus', ['Erwin Rommel', 'Heinz Guderian', 'Georgy Zhukov'], 'He surrendered on 31 January-2 February 1943. [1]'),
        ('Why did the Germans fail to capture Moscow in 1941?', 'The Soviet counter-attack and the Russian winter halted them', ['They never tried to reach it', 'Britain defended Moscow', 'Hitler ordered a retreat in June 1941'], '[1]'),
        ('How did the USSR keep producing weapons after the German invasion?', 'Factories were moved east to the Urals and beyond', ['It bought them all from Germany', 'It stopped producing weapons', 'It used only weapons from 1918'], '[1]'),
        ('Which Soviet general led the defence of Moscow and the victory at Stalingrad?', 'Georgy Zhukov', ['Leon Trotsky', 'Mikhail Tukhachevsky', 'Lavrentiy Beria'], '[1]'),
    ],
    'a': [
        ('Describe Operation Barbarossa in 1941.', 'features of Operation Barbarossa',
         ['It began on 22 June 1941 with over three million Axis troops', 'Three army groups attacked towards Leningrad, Moscow and Ukraine', 'Huge Soviet armies were encircled and millions taken prisoner', 'Leningrad was besieged from September 1941', 'The attack was halted before Moscow in December 1941']),
        ('Describe the Battle of Stalingrad.', 'stages of the Battle of Stalingrad',
         ['The German Sixth Army attacked Stalingrad in August 1942', 'Fierce street fighting took place in the ruined city', 'In November 1942 Soviet forces encircled the Germans in Operation Uranus', 'Hitler refused to allow a retreat and attempts to supply the army by air failed', 'Paulus surrendered in February 1943 and about 91,000 Germans were taken prisoner']),
    ],
    'b': [
        ('Why did Operation Barbarossa fail to defeat the USSR in 1941?',
         ['The USSR was vast and the Germans could not supply their armies over such distances', 'The Germans were not equipped for the Russian winter', 'Hitler divided his forces and delayed the attack on Moscow', 'Soviet resistance was stronger than expected and reserves from Siberia arrived', 'Scorched earth tactics denied the Germans supplies']),
        ('Why did the Soviet Union win at Stalingrad?',
         ['Soviet soldiers fought fiercely in the ruins, preventing a German victory', 'Zhukov\'s Operation Uranus encircled the Sixth Army', 'Hitler refused to let Paulus break out', 'The Luftwaffe could not supply the trapped army by air', 'Soviet industry produced more tanks and guns']),
    ],
    'claims': [
        ('Germany captured Moscow in 1941.', False, 'The Germans reached its outskirts but were driven back by the Soviet counter-attack in December 1941.'),
        ('The Battle of Kursk was the last major German offensive on the Eastern Front.', True, 'After its defeat in July 1943 the Red Army held the initiative.'),
        ('The USSR received no help from its allies during the war.', False, 'It received large quantities of supplies through Lend-Lease, including lorries and food.'),
    ],
    'c': [
        dict(q='‘The Battle of Stalingrad was the turning point of the war on the Eastern Front.’',
             pro=['A whole German army was destroyed or captured', 'It ended German advances towards the oil fields of the Caucasus', 'It was a huge boost to Soviet morale and a blow to German prestige'],
             con=['The failure before Moscow in December 1941 ended hopes of a quick victory', 'Kursk in July 1943 was the last German offensive; after it the Red Army held the initiative', 'Soviet industrial production and Lend-Lease decided the long war'],
             judge='Stalingrad was the decisive psychological and military turning point, though Moscow had already ended Blitzkrieg and Kursk confirmed the shift'),
        dict(q='How important were Hitler\'s mistakes in the German defeat on the Eastern Front?',
             pro=['He delayed the attack on Moscow in 1941', 'He refused to let the Sixth Army break out at Stalingrad', 'Brutal occupation policies turned potential allies against Germany'],
             con=['Soviet resistance and leadership improved', 'The size of the USSR and the winter', 'Soviet industrial strength and Lend-Lease'],
             judge='Hitler\'s mistakes made defeat worse, but Soviet resources and resistance were the main reasons'),
    ],
    'src': [
        S('a Soviet poster of 1942 (description of a typical design)', 'A Red Army soldier stands in front of a burning city with the words “Fight to the death! Not a step back!”',
          'Soviet resistance at Stalingrad', 'It shows the Soviet government demanding total resistance and refusing retreat.',
          'To inspire soldiers and civilians to defend Stalingrad at all costs.',
          'it shows the official Soviet message', 'it is propaganda and does not show how soldiers felt',
          'That Stalin\'s Order No. 227 of July 1942 threatened soldiers who retreated with punishment.', stance=True, why='it shows the determination that made Stalingrad a turning point', visual=True),
        S('a letter written by a German soldier trapped at Stalingrad, January 1943 (illustrative)', 'We have not had bread for days. The cold is worse than the Russians. Nobody believes any longer that help will come.',
          'German soldiers at Stalingrad', 'It shows German soldiers were starving, freezing and had lost hope.',
          'To tell his family about his situation, probably expecting to die.',
          'it is an eyewitness account from someone trapped in the city', 'it shows one soldier\'s experience; letters were censored',
          'How the Soviet counter-attack encircled the army.', stance=True, why='it shows the destruction of a German army'),
    ],
})

v5c = T('The war in the Pacific: Pearl Harbor, Midway and the atomic bombs', 'war in the pacific', 'pearl harbor', 'midway', 'atomic bombs')
build(v5c, {
    'enq': 'the war in the Pacific', 'claim': 'the atomic bombs were the main reason for Japan\'s surrender',
    'stim': ['On 7 December 1941 Japanese aircraft attacked the US Pacific Fleet at Pearl Harbor.', 'In June 1942 the US navy won a major victory at Midway.',
             'In August 1945 the USA dropped atomic bombs on Hiroshima and Nagasaki.'],
    'terms': [
        ('Pearl Harbor', 'the US naval base in Hawaii attacked by Japan on 7 December 1941'),
        ('island hopping', 'the US strategy of capturing key islands while bypassing others to advance towards Japan'),
        ('kamikaze', 'Japanese pilots who deliberately crashed their aircraft into enemy ships'),
        ('aircraft carrier', 'a warship from which aircraft take off and land, decisive in the Pacific war'),
        ('Manhattan Project', 'the secret US programme that developed the atomic bomb'),
        ('Battle of Midway', 'the June 1942 naval battle in which the USA sank four Japanese aircraft carriers'),
    ],
    'dates': [('Japan attacked Pearl Harbor', 1941, 12), ('Singapore surrendered to Japan', 1942, 2), ('the Battle of Midway was fought', 1942, 6), ('US forces landed on Iwo Jima', 1945, 2),
              ('the Battle of Okinawa began', 1945, 4), ('an atomic bomb was dropped on Hiroshima', 1945, 8.06), ('Japan formally surrendered', 1945, 9.02)],
    'mcq': [
        ('Why was the attack on Pearl Harbor not a complete success for Japan?', 'The US aircraft carriers were not in port', ['No US ships were damaged', 'The USA was already at war with Japan', 'The attack took place at night'], '[1]'),
        ('How did the USA know about the Japanese plan to attack Midway?', 'US code-breakers had broken Japanese naval codes', ['Japan announced it publicly', 'A Japanese admiral defected', 'Britain captured the plans in Singapore'], '[1]'),
        ('Which city was hit by the second atomic bomb?', 'Nagasaki', ['Tokyo', 'Osaka', 'Kyoto'], 'On 9 August 1945. [1]'),
        ('Which country declared war on Japan on 8 August 1945?', 'The USSR', ['China', 'Britain', 'Germany'], 'Soviet forces invaded Manchuria. [1]'),
    ],
    'a': [
        ('Describe the Japanese attack on Pearl Harbor.', 'features of the attack on Pearl Harbor',
         ['It was a surprise attack on Sunday 7 December 1941, without a declaration of war', 'Over 350 Japanese aircraft took off from six carriers', 'Eight US battleships were damaged or sunk', 'About 2,400 Americans were killed', 'The US aircraft carriers were at sea and escaped', 'The next day the USA declared war on Japan']),
        ('Describe the Japanese conquests in South-East Asia in 1941-42.', 'territories conquered by Japan in 1941-42',
         ['Hong Kong fell in December 1941', 'Malaya was overrun and Singapore surrendered in February 1942', 'The Philippines were captured from the USA', 'The Dutch East Indies were taken, with their oil', 'Burma was conquered, threatening India']),
    ],
    'b': [
        ('Why did Japan attack Pearl Harbor?',
         ['Japan wanted an empire in Asia with raw materials such as oil and rubber', 'The USA had imposed an oil embargo in 1941 after Japan moved into Indochina', 'Destroying the US Pacific Fleet would give Japan time to conquer South-East Asia', 'Japanese leaders hoped the USA would then accept a negotiated peace']),
        ('Why was the Battle of Midway a turning point?',
         ['Japan lost four of its aircraft carriers and many experienced pilots', 'Japan could not replace carriers as fast as the USA', 'It ended Japanese expansion in the Pacific', 'The USA took the initiative and began island hopping']),
        ('Why did the USA use atomic bombs against Japan?',
         ['To end the war quickly and avoid an invasion that could cost many American lives', 'Fighting on Iwo Jima and Okinawa showed the Japanese would resist fiercely', 'To show the USSR the power of the new weapon', 'The bomb had been developed at great cost and leaders expected to use it']),
    ],
    'claims': [
        ('The Japanese attack on Pearl Harbor destroyed all the US aircraft carriers.', False, 'The carriers were at sea and escaped, which proved vital at Midway.'),
        ('US code-breakers helped the USA win at Midway.', True, 'They learned of the Japanese plan in advance.'),
        ('Japan surrendered immediately after the bombing of Hiroshima.', False, 'Japan did not surrender until after Nagasaki and the Soviet declaration of war; the surrender was announced on 15 August.'),
    ],
    'c': [
        dict(q='‘The atomic bombs were the main reason for Japan\'s surrender in 1945.’',
             pro=['Two cities were destroyed, showing the USA could destroy Japan without invasion', 'The Emperor referred to a new and most cruel bomb in his surrender broadcast'],
             con=['Japan had already lost its navy and air force and its cities were being destroyed by conventional bombing', 'The US blockade was starving Japan', 'The Soviet declaration of war on 8 August ended hopes of Soviet mediation', 'Island hopping had brought US forces to Japan\'s doorstep'],
             judge='The bombs were the immediate trigger for surrender, but Japan was already defeated; the Soviet declaration of war was also decisive'),
        dict(q='How important was the Battle of Midway in the defeat of Japan?',
             pro=['It destroyed four carriers and ended Japanese expansion', 'It gave the USA the initiative for the rest of the war'],
             con=['US industrial strength was the underlying reason for victory', 'Island hopping and submarine warfare wore Japan down', 'The atomic bombs and Soviet entry ended the war'],
             judge='Midway was the turning point, but US industrial superiority explains why Japan could not recover from it'),
    ],
    'src': [
        S('President Roosevelt\'s speech to Congress, 8 December 1941 (extract)', 'Yesterday, December 7, 1941 — a date which will live in infamy — the United States of America was suddenly and deliberately attacked by naval and air forces of the Empire of Japan.',
          'the attack on Pearl Harbor', 'Roosevelt presents the attack as a shameful surprise attack that must be avenged.',
          'To ask Congress to declare war on Japan and unite the American people.',
          'it is the President\'s own words, the day after the attack', 'it was designed to unite Americans, so it does not discuss the reasons for Japan\'s attack, such as the oil embargo',
          'That the US carriers escaped the attack.', stance=None),
        S('an extract from a modern history book (illustrative)', 'By August 1945 Japan had no navy, its cities were burning and its people were hungry. What finally broke the will of its leaders was not one weapon but two shocks in three days: the bomb and the Soviet declaration of war.',
          'the reasons for Japan\'s surrender', 'It argues that the atomic bomb and the Soviet declaration of war together forced Japan to surrender, after it had already been defeated.',
          'To give an interpretation of why Japan surrendered.',
          'it is written with hindsight and uses evidence from both sides', 'it is one interpretation; historians still debate the importance of the bombs',
          'The scale of casualties at Hiroshima and Nagasaki.', stance=False, why='it argues the bombs were not the only decisive factor', kind='secondary', published=True),
    ],
})

v5d = T('Allied victory in Europe: D-Day, strategic bombing and the Holocaust', 'allied victory in europe', 'd-day', 'strategic bombing', 'holocaust')
build(v5d, {
    'enq': 'the Allied victory in Europe', 'claim': 'strategic bombing made a major contribution to the Allied victory in Europe',
    'stim': ['On 6 June 1944 Allied forces landed on the beaches of Normandy.', 'From 1942 British and American bombers attacked German cities and industry.',
             'When Allied troops entered the Nazi camps in 1945 they found evidence of mass murder on an enormous scale.'],
    'terms': [
        ('Operation Overlord', 'the Allied invasion of Normandy in northern France, which began on D-Day, 6 June 1944'),
        ('Operation Fortitude', 'the Allied deception plan that convinced the Germans the main invasion would come at the Pas-de-Calais'),
        ('Mulberry harbours', 'prefabricated floating harbours towed across the Channel to land supplies in Normandy'),
        ('area bombing', 'bombing a whole city area, rather than a single target, to destroy industry, housing and morale'),
        ('Combined Bomber Offensive', 'the joint campaign agreed at Casablanca in 1943 in which the USAAF bombed by day and the RAF by night'),
        ('Final Solution', 'the Nazi plan for the systematic murder of the Jews of Europe'),
        ('Einsatzgruppen', 'SS mobile killing units that shot Jews and others in the occupied USSR from 1941'),
        ('Wannsee Conference', 'the meeting of Nazi officials on 20 January 1942 that coordinated the Final Solution'),
    ],
    'dates': [('the Wannsee Conference was held', 1942, 1), ('the RAF bombing of Hamburg caused a firestorm', 1943, 7), ('Allied troops landed in Normandy on D-Day', 1944, 6),
              ('Paris was liberated', 1944, 8), ('the Battle of the Bulge began', 1944, 12), ('Soviet troops liberated Auschwitz', 1945, 1.27), ('Dresden was bombed', 1945, 2.13),
              ('Hitler committed suicide in Berlin', 1945, 4.3), ('VE Day was celebrated', 1945, 5.08)],
    'mcq': [
        ('Who was the Supreme Allied Commander for the D-Day landings?', 'Dwight D. Eisenhower', ['Bernard Montgomery', 'George Patton', 'Arthur Harris'], '[1]'),
        ('Which of these was one of the five D-Day landing beaches?', 'Omaha', ['Dunkirk', 'Calais', 'Anzio'], 'The beaches were Utah, Omaha, Gold, Juno and Sword. [1]'),
        ('Who led RAF Bomber Command from 1942 and championed area bombing?', 'Arthur Harris', ['Hugh Dowding', 'Bernard Montgomery', 'Charles Portal'], '[1]'),
        ('Which development from early 1944 allowed US bombers to attack Germany by day with fewer losses?', 'Long-range fighter escorts such as the P-51 Mustang', ['The jet engine', 'The atomic bomb', 'The Mulberry harbour'], '[1]'),
        ('Approximately how many Jews were murdered in the Holocaust?', 'About six million', ['About six hundred thousand', 'About one million', 'About twenty million'], '[1]'),
        ('Which camp was liberated by Soviet troops on 27 January 1945?', 'Auschwitz-Birkenau', ['Bergen-Belsen', 'Dachau', 'Buchenwald'], 'Belsen was liberated by British troops in April 1945. [1]'),
        ('What was the Battle of the Bulge?', 'The last major German offensive in the west, in the Ardennes', ['The Allied landing in Normandy', 'The bombing of Dresden', 'The battle for Berlin'], 'It began on 16 December 1944. [1]'),
    ],
    'a': [
        ('Describe the D-Day landings of 6 June 1944.', 'features of the D-Day landings',
         ['About 156,000 Allied troops landed on five beaches in Normandy', 'US troops landed at Utah and Omaha, British at Gold and Sword and Canadians at Juno', 'Airborne troops landed during the night to capture bridges and protect the flanks',
          'Thousands of ships and aircraft supported the landings', 'Heavy casualties were suffered at Omaha beach', 'Operation Fortitude meant German reserves were held back near Calais']),
        ('Describe the Allied strategic bombing of Germany.', 'features of the Allied bombing campaign',
         ['RAF Bomber Command carried out area bombing of cities at night', 'The USAAF attempted precision bombing of factories by day', 'The bombing of Hamburg in July 1943 created a firestorm that killed about 40,000 people',
          'From 1944 oil plants and transport were targeted', 'Dresden was destroyed in February 1945', 'About 55,000 Bomber Command aircrew were killed']),
        ('Describe the Nazi persecution and murder of the Jews during the Second World War.', 'stages of the Holocaust',
         ['Jews in occupied Poland were forced into ghettos such as Warsaw and Lodz', 'From June 1941 Einsatzgruppen shot hundreds of thousands of Jews in the USSR', 'The Wannsee Conference in January 1942 coordinated the Final Solution',
          'Death camps such as Treblinka and Auschwitz-Birkenau used gas chambers', 'About six million Jews were murdered', 'Roma, disabled people and others were also murdered']),
    ],
    'b': [
        ('Why were the D-Day landings successful?',
         ['Careful planning and training over two years', 'Operation Fortitude deceived the Germans about where the landings would be', 'The Allies had complete air superiority', 'Mulberry harbours and the PLUTO pipeline kept the armies supplied',
          'Hitler delayed releasing the panzer reserves', 'The French Resistance sabotaged railways and communications']),
        ('Why did the Allies carry out strategic bombing of Germany?',
         ['To destroy German war industry and transport', 'To break the morale of German workers', 'It was the only way Britain could hit Germany directly before an invasion was possible', 'To help the USSR by forcing Germany to divert resources to air defence',
          'To weaken the Luftwaffe before D-Day']),
        ('Why did the Nazis move from persecution to the mass murder of Jews?',
         ['Nazi racial ideology saw Jews as an enemy to be removed', 'Conquest of Poland and the USSR brought millions more Jews under Nazi control', 'The war against the USSR was seen as a war of annihilation', 'Mass shootings were considered too slow and difficult for the killers, so camps with gas chambers were built',
          'War hid the crimes from the outside world']),
    ],
    'claims': [
        ('The D-Day landings took place at the Pas-de-Calais.', False, 'They took place in Normandy; Operation Fortitude made the Germans expect an attack at the Pas-de-Calais.'),
        ('German war production rose until 1944 despite Allied bombing.', True, 'Under Albert Speer production of weapons kept rising until the second half of 1944.'),
        ('The Wannsee Conference was the start of the killing of Jews.', False, 'Mass shootings had begun in 1941; Wannsee coordinated the Final Solution across Europe.'),
        ('Soviet forces captured Berlin in 1945.', True, 'The Red Army fought its way into Berlin in April-May 1945.'),
    ],
    'c': [
        dict(q='‘D-Day was the most important reason for the defeat of Germany.’',
             pro=['It opened the second front that Stalin had demanded', 'It led to the liberation of France and the advance into Germany from the west', 'It forced Germany to fight on two major fronts at once'],
             con=['Most German forces were destroyed on the Eastern Front, for example at Stalingrad and Kursk', 'Strategic bombing damaged German industry and transport', 'US and Soviet industrial production far exceeded Germany\'s', 'Hitler\'s mistakes, such as the invasion of the USSR'],
             judge='D-Day shortened the war, but the Eastern Front destroyed most of the German army, so it was the more important factor'),
        dict(q='How far did strategic bombing contribute to the Allied victory in Europe?',
             pro=['It forced Germany to divert fighters, guns and men to air defence', 'Attacks on oil and transport in 1944-45 crippled the German war economy', 'It destroyed much of the Luftwaffe before D-Day'],
             con=['German production rose until late 1944', 'Civilian morale did not collapse', 'Losses of aircrew were very high', 'The war was mainly won on land, especially in the east'],
             judge='Bombing was not decisive on its own, but by 1944 it was a major contribution because of the attacks on oil and the diversion of German resources'),
        dict(q='How central was the persecution and murder of the Jews to the aims of the Nazi regime?',
             pro=['Antisemitism was central to Nazi ideology from the beginning', 'The killing continued even when it took trains and resources from the war effort', 'The Final Solution was organised across the whole of occupied Europe'],
             con=['Winning the war and conquering Lebensraum in the east were the regime\'s main priorities', 'Policy developed in stages and was radicalised by the war, especially the invasions of Poland and the USSR', 'The regime also persecuted and murdered other groups, such as Roma and disabled people'],
             judge='The murder of the Jews was a central aim of the regime, shown by the resources committed to it even in defeat'),
    ],
    'src': [
        S('General Eisenhower\'s Order of the Day to Allied troops, 6 June 1944 (extract)', 'You are about to embark upon the Great Crusade, toward which we have striven these many months. The eyes of the world are upon you.',
          'the D-Day landings', 'It presents D-Day as a great moral struggle that the whole world is watching.',
          'To inspire the troops on the morning of the invasion.',
          'it was written by the Supreme Commander at the time', 'it is meant to raise morale, so it says nothing about the risks or casualties',
          'The heavy casualties at Omaha beach.', stance=None),
        S('Arthur Harris, head of RAF Bomber Command, in a 1942 newsreel interview (extract)', 'The Nazis entered this war under the rather childish delusion that they were going to bomb everyone else, and nobody was going to bomb them. They sowed the wind, and now they are going to reap the whirlwind.',
          'the bombing of Germany', 'It argues the bombing of Germany is justified revenge for German bombing.',
          'To justify the bombing campaign to the British public and raise morale.',
          'it shows the view of the commander of the bombing campaign', 'Harris was defending his own campaign, so he says nothing about civilian deaths or bomber losses',
          'The bombing of Hamburg in July 1943.', stance=True, why='it shows the confidence of the commander that bombing would punish and defeat Germany'),
        S('a memorandum from Winston Churchill to his military chiefs, 28 March 1945 (extract)', 'It seems to me that the moment has come when the question of bombing of German cities simply for the sake of increasing the terror, though under other pretexts, should be reviewed.',
          'the bombing of Germany', 'It suggests Churchill had doubts about bombing cities, after Dresden, when the war was nearly won.',
          'To distance himself from area bombing as victory approached and to consider post-war Germany.',
          'it is a private memo by the Prime Minister, not propaganda', 'it was written late in the war; Churchill had supported area bombing earlier',
          'The scale of destruction at Dresden.', stance=False, why='it raises doubts about the value of bombing cities'),
        S('Richard Dimbleby, BBC radio report from Bergen-Belsen, April 1945 (extract, abridged)', 'Here over an acre of ground lay dead and dying people. You could not see which was which... This day at Belsen was the most horrible of my life.',
          'the Nazi camps', 'It shows the horror of what British troops found when they liberated Belsen.',
          'To report to the British public what the camps were like.',
          'it is an eyewitness account broadcast at the time', 'Belsen was a concentration camp; it does not show the death camps in Poland where most Jews were gassed',
          'That about six million Jews were murdered, most of them in death camps and mass shootings in the east.', stance=None),
        S('an extract from a modern history book (illustrative)', 'Bombing did not break German morale, and factories kept producing. Yet by 1944 it was forcing Germany to keep thousands of guns and fighters at home, and the attacks on oil left tanks and aircraft without fuel.',
          'the effects of strategic bombing', 'It argues bombing failed in some aims but made a significant contribution by 1944.',
          'To give a balanced interpretation of the effects of bombing.',
          'it is written with hindsight and access to German production figures', 'it is one interpretation and the extract is brief',
          'The human cost of the bombing to German civilians and Allied aircrew.', stance=True, why='it argues bombing made a significant contribution by 1944', kind='secondary', published=True),
    ],
})


# ---------------- Coursework / Paper 4 skills (uses the content packs of all depth studies)
CHAPTERS[5] = [v5a, v5b, v5c, v5d]
_P = packs(CHAPTERS)
_E = [(c, e, P) for c, P in _P for e in P.get('c', [])]
_A = [(c, x, P) for c, P in _P for x in P.get('a', [])]
_SEC = [(c, s, P) for c, P in _P for s in P.get('src', []) if s.get('kind') == 'secondary']
_PRI = [(c, s, P) for c, P in _P for s in P.get('src', []) if s.get('kind', 'primary') == 'primary']

def _qt(s):
    return s['text'] if s.get('visual') else f'“{s["text"]}”'


CW_TERMS = [
    ('enquiry question', 'a focused question that requires analysis and a judgement rather than description'),
    ('interpretation', 'a historian\'s view or argument about the past, based on evidence'),
    ('historiography', 'the study of how and why historians\' interpretations of an event have differed and changed'),
    ('bibliography', 'a list of all the sources and books used in an investigation'),
    ('referencing', 'showing exactly where evidence or a quotation comes from, for example in a footnote'),
    ('significance', 'how important an event or person was, judged by its effects at the time and later'),
    ('hindsight', 'knowledge of what happened later, which the people at the time did not have'),
    ('thesis', 'the main argument of an extended answer, stated clearly near the start'),
]
CW_KEY = ('Level 1 (1-4): general, descriptive answer with little relevant knowledge. Level 2 (5-8): some relevant knowledge, mostly narrative, with limited explanation. '
          'Level 3 (9-12): explains several factors with supporting detail but analysis is one-sided or the judgement is asserted. '
          'Level 4 (13-16): balanced, well-supported analysis of the issue with some evaluation of the relative importance of factors. '
          'Level 5 (17-20): sustained, well-organised argument with precise evidence that reaches a substantiated judgement on the question.')

v5e = T('Coursework and Paper 4 skills: framing a question, using sources and interpretations, writing an extended answer', 'coursework and paper 4 skills', 'framing a question', 'interpretations', 'extended answer')
build(v5e, {'terms': CW_TERMS})


@v5e.add('C1', (1, 2, 3), 'mcq')
def cw_bestq(r, D):
    c, e, P = r.choice(_E)
    good = e['q'] + (' How far do you agree?' if e['q'].startswith('‘') else '')
    c2, (aq, np, ps), P2 = r.choice(_A)
    ds = [aq, f'What happened during {P["enq"]}?', f'Write about {P["enq"]}.']
    opts, a = mcq(r, good, ds)
    return {'stem': f'A student is choosing an enquiry question for a coursework investigation (or a Paper 4 answer). Which of these questions is most likely to allow them to reach the highest level?',
            'options': opts, 'answer': a,
            'key': 'It requires analysis of several factors and a supported judgement; the others invite description or narrative only. [1]', 'marks': 1, 'minutes': 1}


@v5e.add('C3', (1, 2), 'mcq')
@v5e.add('C1', (1, 2, 3), 'mcq')
def cw_interp(r, D):
    c, s, P = r.choice(_SEC)
    ok = s['infer']
    ds = [x[1]['infer'] for x in r.sample([x for x in _SEC + _PRI if x[1] is not s and x[1]['infer'] != ok], 3)]
    opts, a = mcq(r, ok, ds)
    return {'stem': f'Read this interpretation, {s["prov"]}: “{s["text"]}” Which statement best summarises the historian\'s interpretation?',
            'options': opts, 'answer': a, 'key': 'Only this statement matches the argument of the extract. [1]', 'marks': 1, 'minutes': 1.5}


def _fullq(e):
    return e['q'] + (' How far do you agree?' if e['q'].startswith('‘') else '')


@v5e.add('C2', (1, 2, 3, 4), 'explain')
def cw_whyq(r, D):
    c, e, P = r.choice(_E)
    same = [x for x in _A if x[2] is P] or [x for x in _A if x[0] == c]
    c2, (aq, np, ps), P2 = r.choice(same)
    weak = r.choice([aq, f'Write everything you know about {np}.', f'What happened during {P["enq"]}?'])
    return {'stem': f'A student is choosing between two questions for an extended answer: Question 1: “{_fullq(e)}” Question 2: “{weak}” Explain why Question 1 is the better choice for a coursework or Paper 4 answer.',
            'answer': f'Question 1 asks for a judgement about {P["enq"]}, so the answer must weigh factors (for example, the point that {low2(_dot(e["pro"][0])[:-1])}, against the point that {low2(_dot(e["con"][0])[:-1])}) and reach a conclusion. Question 2 can be answered by narrative or description, so it limits the answer to the lower levels.',
            'key': '1 mark for identifying that Question 1 requires analysis / judgement; 1 mark for identifying that Question 2 invites description; up to 2 marks for explaining with reference to the topic how Question 1 allows factors to be weighed [4]',
            'type': 'explain', 'marks': 4, 'minutes': 5}


@v5e.add('C2', (2, 3, 4), 'explain')
def cw_primsec(r, D):
    c2, b, P2 = r.choice(_SEC)
    pri = [x for x in _PRI if x[2] is P2] or [x for x in _PRI if x[0] == c2]
    if not pri:
        return None
    c1, a, P1 = r.choice(pri)
    return {'stem': f'Source A: {a["prov"]}. {_qt(a)} Source B: {b["prov"]}. {_qt(b)} Explain how a historian investigating {P1["enq"]} would use Source A differently from Source B.',
            'answer': f'Source A is primary evidence from the time. Message: {a["infer"]} It must be evaluated for its purpose: {low2(a["purpose"])} Source B is a later interpretation. Argument: {b["infer"]} The historian should test this argument against evidence such as Source A, and agree with or challenge it.',
            'key': '1 mark for identifying A as contemporary evidence; 1 mark for identifying B as a later interpretation; up to 2 marks for explaining the different uses (evidence to be evaluated vs argument to be tested) with details [4]',
            'type': 'explain', 'marks': 4, 'minutes': 5}


@v5e.add('C2', (1, 2, 3, 4), 'explain')
def cw_spot(r, D):
    c, e, P = r.choice(_E)
    errs = [
        ('The answer describes events in date order without linking them to the question.', 'narrative rather than analysis; each paragraph should begin with a point that answers the question'),
        ('The conclusion says “there are arguments on both sides” but does not decide.', 'no judgement; the conclusion should state which side is stronger and why, using a criterion'),
        ('The answer quotes a historian but does not say who wrote it or test the view.', 'interpretation not referenced or evaluated; it should name the source and test it against evidence'),
        ('The answer only gives reasons that agree with the statement.', 'one-sided; it needs a developed counter-argument before the judgement'),
    ]
    k = 1 if D <= 2 else 2
    pick = r.sample(errs, k)
    return {'stem': f'A teacher writes comments on a student\'s extended answer to {e["q"]} ' + ' '.join(f'Comment {i + 1}: {x[0]}' for i, x in enumerate(pick)) +
                    f' Identify the weakness shown by {"each comment" if k > 1 else "the comment"} and explain how the student could improve the answer.',
            'answer': ' '.join(f'{i + 1}. Weakness: {x[1]}.' for i, x in enumerate(pick)) + f' For example, they could argue: {_dot(e["judge"])}',
            'key': f'For each comment: 1 mark for the weakness; 1 mark for a valid improvement linked to the question [{2 * k}]', 'type': 'explain', 'marks': 2 * k, 'minutes': _mins(2 * k)}


@v5e.add('C3', (2, 3, 4, 5), 'case')
def cw_test(r, D):
    c, s, P = r.choice(_SEC)
    es = P.get('c') or []
    if not es or s.get('stance') is None or not P.get('claim'):
        return None
    kc = _kw(P['claim'])
    sc = [len(kc & _kw(x['q'])) for x in es]
    if max(sc) < 2:
        return None
    e = es[sc.index(max(sc))]
    sup, chal = (e['pro'], e['con']) if s['stance'] else (e['con'], e['pro'])
    want = CTX.get('want_marks') or 0
    m2 = 8 if want >= 10 else (2 if want and want <= 4 else (4 if D <= 3 else 6))
    stem = (f'Read the interpretation, {s["prov"]}: “{s["text"]}” (a) What is the interpretation in the extract? [2] '
            f'(b) Use your own knowledge to explain how far this interpretation is supported by the evidence. [{m2}]')
    ans = f'(a) {s["infer"]} (b) Evidence that supports the interpretation: {_dot(sup[0])} Evidence that challenges it: {_dot(chal[0])} Judgement: {_dot(e["judge"])}'
    h = m2 // 2
    key = (f'(a) 1 mark for identifying the view; 1 mark for a supporting detail from the extract [2] (b) Up to {h} mark{"s" if h > 1 else ""} for evidence that supports and up to {h} '
           f'for evidence that challenges, each explained and linked to the extract [{m2}]')
    return {'stem': stem, 'answer': ans, 'key': key, 'type': 'case', 'marks': 2 + m2, 'minutes': _mins(2 + m2)}


@v5e.add('C3', (2, 3, 4, 5), 'short')
def cw_plan(r, D):
    c, e, P = r.choice(_E)
    n = 2 if D <= 3 else 3
    n = min(n, len(e['pro']), len(e['con']))
    return {'stem': f'You are planning a coursework investigation on the question: {e["q"]} Write a thesis statement for your answer and identify {["", "one", "two", "three"][n]} factor{"s" if n > 1 else ""} you would use to support it and {["", "one", "two", "three"][n]} you would use to challenge it.',
            'answer': f'Thesis: {_dot(e["judge"])} Support: ' + ' '.join(_dot(x) for x in e['pro'][:n]) + ' Challenge: ' + ' '.join(_dot(x) for x in e['con'][:n]),
            'key': f'1 mark for a thesis that answers the question directly; 1 mark for each relevant supporting factor and 1 for each challenging factor [{1 + 2 * n}]',
            'type': 'short', 'marks': 1 + 2 * n, 'minutes': _mins(1 + 2 * n)}


@v5e.add('C4', (3, 4, 5), 'long')
def cw_essay(r, D):
    c, e, P = r.choice(_E)
    q = _fullq(e) + ' Explain your answer.'
    lead = r.choice(['Paper 4-style extended answer (shortened practice version).', 'Extended answer practice for the depth study.', 'Write a well-organised extended answer.'])
    return {'stem': f'{lead} {q} In your answer you should consider a range of factors, use precise evidence and reach a substantiated judgement. [20]',
            'answer': c_ans(e['pro'], e['con'], e['judge']), 'key': CW_KEY + ' Indicative content: ' + c_ans(e['pro'], e['con'], e['judge']) + ' [20]',
            'type': 'long', 'marks': 20, 'minutes': 30}


@v5e.add('C4', (3, 4, 5), 'case')
def cw_sources(r, D):
    c2, b, P2 = r.choice(_SEC)
    pri = [x for x in _PRI if x[2] is P2] or [x for x in _PRI if x[0] == c2]
    if not pri:
        return None
    c1, a, P1 = r.choice(pri)
    P = P2
    es = P.get('c') or []
    if not es:
        return None
    e = r.choice(es)
    want = CTX.get('want_marks') or 0
    m = 12 if (want >= 12 or D == 5) else 8
    return {'stem': f'A student is investigating {e["q"]} They have found these two pieces of evidence. Source A: {a["prov"]}. {_qt(a)} Source B: {b["prov"]}. {_qt(b)} '
                    f'Evaluate how far each source would help the student to answer the question, and explain what other evidence they would need. [{m}]',
            'answer': f'Source A: {a["infer"]} Strength: {a["plus"]}; limitation: {a["minus"]}. Source B: {b["infer"]} Strength: {b["plus"]}; limitation: {b["minus"]}. Other evidence needed: {_dot(b["missing"])}',
            'key': (f'Level 1: describes the sources. Level 2: comments on relevance of content to the question. Level 3: evaluates both sources using provenance (author, date, purpose) and own knowledge. '
                    f'Level 4: as Level 3, with a judgement on their relative value and a precise suggestion of further evidence [{m}]'),
            'type': 'case', 'marks': m, 'minutes': _mins(m)}


CHAPTERS[5] = [v5a, v5b, v5c, v5d, v5e]
finalize(CHAPTERS)
