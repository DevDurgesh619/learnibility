"""IB MYP 4 Individuals and Societies (integrated humanities) – ib-g9-social-science.

Criteria: A knowing and understanding, B investigating, C communicating, D thinking critically (MYP year 4
descriptors). Real dated events, places and attributed (paraphrased) sources; sensitive topics (empire, Partition,
migration) are summarised neutrally in the third person. Parametric generators compute answers for supply and
demand, taxes and subsidies, electoral arithmetic, trade, interest, urban and population change, energy flows in
ecosystems, yields and tourism leakage. Mocks follow the MYP 5 eAssessment shape (3 tasks, 15 items, 80 marks).
"""
from __future__ import annotations

from _common import Registry, mcq, name  # noqa: F401
import ib_myp_is_common as C

CONFIG = {'minutesPerMark': 1.5, 'mcqMinutes': 1.5}
MOCK = C.mock(4)
R = Registry()
K = C.Kit(R, 4)
STYLE = C.style(4)


def init(subject_id):
    pass


def templates(st):
    return R.build(st, STYLE)


REV_EVENTS = [('the end of the Seven Years\' War (Treaty of Paris)', 1763), ('the Stamp Act', 1765), ('the Boston Massacre', 1770),
              ('the Boston Tea Party', 1773), ('the battles of Lexington and Concord', 1775), ('the Declaration of Independence', 1776),
              ('the meeting of the Estates-General', 1789), ('the execution of Louis XVI', 1793), ('Napoleon\'s coup of 18 Brumaire', 1799),
              ('Napoleon crowned Emperor', 1804), ('the Battle of Waterloo', 1815), ('Haitian independence', 1804)]
AM_EVENTS = REV_EVENTS[:6] + [('the Proclamation of 1763', 1763), ('the Townshend Acts', 1767), ('the Coercive Acts', 1774), ('the publication of "Common Sense"', 1776), ('the British surrender at Yorktown', 1781)]
FR_EVENTS = [('the meeting of the Estates-General', 1789), ('the Flight to Varennes', 1791), ('the abolition of the monarchy', 1792), ('the execution of Louis XVI', 1793),
             ('the fall of Robespierre', 1794), ('the start of the Directory', 1795), ('Napoleon\'s coup of 18 Brumaire', 1799), ('Napoleon crowned Emperor', 1804),
             ('the Battle of Waterloo', 1815), ('the Assembly of Notables', 1787), ('the end of the Seven Years\' War (Treaty of Paris)', 1763)]

# =============================================================================================
# ch01 The Age of Revolutions
# =============================================================================================
K.st('ch01-st1', 'the causes of the American Revolution',
     terms=[('"no taxation without representation"', 'the colonists\' argument that Parliament had no right to tax them because they elected no members to it'),
            ('virtual representation', 'the British argument that MPs represented the interests of all British subjects, including colonists who could not vote for them'),
            ('Stamp Act', 'the 1765 British tax on printed materials in the colonies, such as newspapers and legal documents, repealed in 1766 after protests'),
            ('Coercive (Intolerable) Acts', 'the laws of 1774 that closed Boston harbour and restricted self-government in Massachusetts after the Boston Tea Party'),
            ('Enlightenment', 'an 18th-century intellectual movement that stressed reason, natural rights and limits on government'),
            ('Continental Congress', 'the assembly of delegates from the American colonies that coordinated resistance from 1774 and declared independence in 1776')],
     facts=[('Which war left Britain with large debts that it tried to pay partly by taxing the American colonies?', 'The Seven Years\' War (1756–1763)', ['The Hundred Years\' War', 'The Napoleonic Wars', 'The War of 1812'], 'The war doubled Britain\'s national debt.'),
            ('In which year did the Boston Tea Party take place?', '1773', ['1765', '1770', '1776'], 'Colonists dumped 342 chests of East India Company tea into Boston harbour on 16 December 1773.'),
            ('Who wrote the pamphlet "Common Sense" (January 1776) urging independence?', 'Thomas Paine', ['Thomas Jefferson', 'John Locke', 'Benjamin Franklin'], 'It sold over 100 000 copies within months.'),
            ('Which philosopher\'s idea of natural rights to "life, liberty and property" influenced the Declaration of Independence?', 'John Locke', ['Thomas Hobbes', 'Niccolò Machiavelli', 'Jean-Jacques Rousseau'], 'Jefferson adapted it to "life, liberty and the pursuit of happiness".'),
            ('Where were the first shots of the War of Independence fired in April 1775?', 'Lexington and Concord, Massachusetts', ['Yorktown, Virginia', 'Philadelphia', 'New York'], 'British troops tried to seize colonial weapons.')],
     why=[('Explain why the Stamp Act caused such strong opposition in the colonies.', 'It was the first direct tax by Parliament on the colonies, it affected influential groups (lawyers, printers, merchants), and colonists argued that only their own assemblies could tax them.'),
          ('Explain why the Boston Tea Party led to a breakdown in relations with Britain.', 'Parliament responded with the Coercive Acts, closing Boston harbour and limiting self-government; other colonies saw this as a threat to all their liberties and formed the First Continental Congress.'),
          ('Explain why Enlightenment ideas mattered to the American revolutionaries.', 'Ideas of natural rights, government by consent and the right to resist tyranny gave colonists a principled justification for rebellion beyond complaints about taxes.'),
          ('Explain why the end of the Seven Years\' War in 1763 changed relations between Britain and the colonies.', 'With the French threat gone, colonists needed British protection less, while Britain kept troops in America, banned settlement west of the Appalachians (Proclamation of 1763) and taxed the colonies to pay its debts.')],
     contrast=[('a long-term cause of the American Revolution', 'a trigger of the American Revolution', 'Long-term causes developed over years, such as colonial self-government and Enlightenment ideas; triggers were specific events, such as the Coercive Acts (1774) and the fighting at Lexington and Concord (1775).'),
               ('the colonists\' view of representation', 'the British view of representation', 'Colonists argued they could only be taxed by assemblies they elected; the British argued that Parliament virtually represented all subjects and had authority over the whole empire.')],
     misc=[('The colonists rebelled because British taxes were extremely high.', 'Colonial taxes were lower than taxes in Britain; the dispute was about who had the right to tax them, not the amount.'),
           ('All colonists supported independence.', 'Colonists were divided: Patriots, Loyalists (perhaps a fifth of the population) and many who stayed neutral.'),
           ('The Declaration of Independence gave rights to everyone in America.', 'It declared that all men are created equal, but slavery continued and women and Indigenous peoples were excluded from political rights.')],
     cases=[('the Stamp Act Congress (October 1765)', 'Delegates from nine colonies met in New York and declared that only colonial assemblies could tax the colonists; boycotts of British goods led Parliament to repeal the act in 1766.', 'colonial resistance to taxation', 'organised, cooperative protest showed that colonies could act together on principle.'),
            ('the Boston Massacre (5 March 1770)', 'British soldiers fired on a crowd, killing five colonists; Paul Revere\'s engraving spread a dramatic image of the event.', 'the role of propaganda in building opposition', 'the event was presented as British tyranny, turning opinion against the troops.')],
     evaluate=[('The American Revolution was caused mainly by taxation.', ['a series of taxes (Stamp Act, Townshend duties, Tea Act) triggered protests and boycotts', '"no taxation without representation" became the rallying cry'], ['Enlightenment ideas about rights and consent turned tax protests into a demand for independence', 'the Proclamation of 1763 and the Coercive Acts raised wider issues of liberty and self-government'], 'Taxation was the trigger and focus, but the deeper cause was a conflict over authority and rights shaped by Enlightenment ideas.')],
     src=[('Pamphlet (paraphrased)', 'The author argued that it was absurd for a continent to be permanently governed by an island. He wrote that the connection with Britain brought only injury, dragged America into Europe\'s wars, and that the time had come for separation and a republic.', 'Paraphrase of Thomas Paine, "Common Sense", Philadelphia, January 1776', 'to persuade ordinary colonists to support full independence', 'It shows the arguments that convinced many colonists in 1776 and was extremely widely read.', 'It is persuasive propaganda written by a recent immigrant to win support, not a balanced account of colonial grievances.', 'America should break away from Britain and become a republic.')],
     rq=[('How far did Thomas Paine\'s "Common Sense" change colonial attitudes towards independence in 1776?', 'Why did America become independent?', 'it is too broad to answer in depth and has no specific focus', 'It investigates the role of ideas and propaganda in causing revolution, with the pamphlet, letters and newspapers available as primary sources.', 'Read "Common Sense" (extracts) and two secondary sources; collect evidence from letters and newspapers Jan–July 1776; compare with earlier views; evaluate origin and purpose; cite in MLA.')])
C.chronology(K, 'ch01-st1', c='C3', d=(1, 3), events=AM_EVENTS)

K.st('ch01-st2', 'the causes of the French Revolution',
     terms=[('Ancien Régime', 'the social and political system of France before 1789, with an absolute monarchy and a society divided into three estates'),
            ('Estates-General', 'an assembly of representatives of the three estates, called by Louis XVI in 1789 for the first time since 1614'),
            ('Third Estate', 'everyone in France who was not clergy or noble – about 97% of the population, from peasants to wealthy bourgeoisie'),
            ('bourgeoisie', 'the educated, property-owning middle class, such as merchants, lawyers and officials'),
            ('taille', 'the main direct tax of the Ancien Régime, paid mainly by the Third Estate'),
            ('Tennis Court Oath', 'the pledge of 20 June 1789 by members of the National Assembly not to separate until they had given France a constitution')],
     facts=[('On which date was the Bastille stormed?', '14 July 1789', ['4 July 1776', '21 January 1793', '26 August 1789'], 'It is now France\'s national day.'),
            ('Which writer\'s pamphlet of January 1789 asked "What is the Third Estate?"', 'Emmanuel Joseph Sieyès', ['Voltaire', 'Robespierre', 'Rousseau'], 'He argued the Third Estate was the nation.'),
            ('Why did Louis XVI call the Estates-General in 1789?', 'The government was close to bankruptcy and needed new taxes', ['To declare war on Britain', 'To abolish the monarchy', 'To elect a new king'], 'Debt from wars, including support for the American Revolution, was huge.'),
            ('Which two estates were largely exempt from the taille?', 'The clergy and the nobility', ['The peasants and the clergy', 'The bourgeoisie and the nobility', 'The urban workers and the peasants'], 'Privilege meant the burden fell on the Third Estate.'),
            ('The poor harvest of 1788 caused what in early 1789?', 'A sharp rise in the price of bread', ['A fall in taxes', 'The end of feudalism', 'War with Austria'], 'Bread could take more than half a worker\'s wage.')],
     why=[('Explain why the financial crisis of the 1780s led to revolution in France.', 'The crown was nearly bankrupt after costly wars; the privileged estates blocked tax reform, forcing Louis XVI to call the Estates-General, which gave the Third Estate a stage to demand political change.'),
          ('Explain why the voting system in the Estates-General angered the Third Estate.', 'Voting was by estate, one vote each, so the clergy and nobility could always outvote the Third Estate 2–1, even though it represented about 97% of the people.'),
          ('Explain why the bourgeoisie was attracted by Enlightenment ideas.', 'Writers like Rousseau and Montesquieu argued for equality before the law, popular sovereignty and separation of powers, which justified the bourgeoisie\'s demand for political influence matching their wealth and education.'),
          ('Explain why French support for the American Revolution contributed to the French Revolution.', 'It added about a billion livres to the debt and spread ideas of liberty and representation, as French officers returned having fought for a republic.')],
     contrast=[('the First and Second Estates', 'the Third Estate', 'The First (clergy) and Second (nobility) Estates were small, privileged groups largely exempt from direct taxes; the Third Estate was the vast majority, who paid most taxes and had little political power.'),
               ('a social cause of the French Revolution', 'a financial cause of the French Revolution', 'Social causes came from the unequal estates system and resentment of privilege; financial causes came from royal debt and the failure of tax reform.')],
     misc=[('The French Revolution began because peasants wanted a republic.', 'In 1789 most people wanted reform within the monarchy; the republic came only in 1792 after war and the king\'s flight to Varennes.'),
           ('The Third Estate was made up only of poor peasants.', 'It included wealthy bourgeois merchants, lawyers and officials as well as peasants and urban workers.'),
           ('Marie Antoinette said "Let them eat cake", which caused the revolution.', 'There is no evidence she said it; the phrase appears in Rousseau\'s writing before she came to France. It reflects later propaganda, not a cause.')],
     cases=[('the Tennis Court Oath (20 June 1789)', 'Locked out of their hall, deputies of the Third Estate, calling themselves the National Assembly, swore not to separate until France had a constitution.', 'the challenge to royal authority', 'deputies claimed to represent the nation, transferring sovereignty from the king to the people.'),
            ('the storming of the Bastille (14 July 1789)', 'Parisians seeking gunpowder attacked the royal fortress and prison; its fall showed the king had lost control of Paris.', 'popular action in the Revolution', 'crowd violence forced the king to accept the National Assembly.')],
     evaluate=[('The French Revolution was caused mainly by financial problems.', ['bankruptcy forced the king to call the Estates-General', 'the privileged estates\' refusal to pay taxes exposed the system\'s unfairness'], ['long-term social resentment of privilege and Enlightenment ideas gave the crisis a revolutionary direction', 'the 1788 harvest failure and bread prices drove popular action'], 'Finance was the trigger that opened the crisis, but social inequality and new ideas explain why it became a revolution.')],
     src=[('Pamphlet (paraphrased)', 'The author asked three questions: what is the Third Estate? Everything. What has it been until now in the political order? Nothing. What does it want? To become something. He argued that the privileged orders were a burden on the nation, and that the Third Estate alone could claim to be the nation.', 'Paraphrase of Emmanuel Joseph Sieyès, "What is the Third Estate?", January 1789', 'to persuade readers that the Third Estate should have political power matching its importance', 'It shows the radical arguments circulating just before the Estates-General and was very influential.', 'It is a persuasive pamphlet by a clergyman who sided with the Third Estate; it presents the nobility entirely negatively.', 'The Third Estate is the true nation and deserves real political power.')],
     rq=[('How did bread prices in Paris contribute to popular unrest between 1788 and October 1789?', 'What was the French Revolution?', 'it is a definition question that leads only to narrative', 'It investigates an economic cause of revolutionary action with price data and accounts of the crowd.', 'Collect bread-price data from secondary sources; read accounts of the Réveillon riots and the October march on Versailles; build a timeline; correlate prices and events; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch01-st2', c='C3', d=(1, 3), events=FR_EVENTS)

K.st('ch01-st3', 'the course of the French Revolution, from the Declaration of the Rights of Man to Napoleon',
     terms=[('Declaration of the Rights of Man and of the Citizen', 'the 1789 statement of rights adopted by the National Assembly, proclaiming liberty, equality before the law and popular sovereignty'),
            ('Reign of Terror', 'the period from September 1793 to July 1794 when the Committee of Public Safety used mass arrests and executions against suspected enemies of the Revolution'),
            ('Jacobins', 'a radical political club, led by Robespierre, that dominated the Revolution in 1793–94'),
            ('Committee of Public Safety', 'the body that governed France during the Terror'),
            ('sans-culottes', 'radical working people of Paris, named for wearing trousers rather than the knee-breeches of the rich'),
            ('Napoleonic Code', 'the civil law code of 1804 that set out equality before the law and property rights across France')],
     facts=[('When was the Declaration of the Rights of Man and of the Citizen adopted?', '26 August 1789', ['14 July 1789', '4 July 1776', '21 September 1792'], 'It was adopted by the National Constituent Assembly.'),
            ('When was Louis XVI executed?', '21 January 1793', ['14 July 1789', '9 November 1799', '2 December 1804'], 'He was guillotined in Paris.'),
            ('About how many people were officially sentenced to death during the Terror?', 'About 17 000', ['About 170', 'About 1 million', 'About 2 000 000'], 'Many more died in prison or without trial.'),
            ('Who wrote the "Declaration of the Rights of Woman and of the Female Citizen" in 1791?', 'Olympe de Gouges', ['Marie Antoinette', 'Mary Wollstonecraft', 'Charlotte Corday'], 'She was executed in 1793.'),
            ('In which year did Napoleon seize power in the coup of 18 Brumaire?', '1799', ['1789', '1793', '1815'], 'He became First Consul.')],
     why=[('Explain why the Revolution became more radical between 1791 and 1793.', 'The king\'s flight to Varennes destroyed trust in him, war with Austria and Prussia from 1792 created fear of invasion and treason, and food shortages strengthened the radical sans-culottes and Jacobins.'),
          ('Explain why the Committee of Public Safety used terror.', 'It faced foreign invasion, civil war in the Vendée and economic crisis, and argued that terror was needed to defend the Republic against internal enemies.'),
          ('Explain why Robespierre fell from power in July 1794.', 'With military victories reducing the threat, many deputies feared they could be next on the guillotine; they turned against him and he was executed on 28 July 1794.'),
          ('Explain why Napoleon was able to seize power in 1799.', 'The Directory was weak, corrupt and unpopular; Napoleon was a famous, victorious general, and many wanted order and stability after a decade of upheaval.')],
     contrast=[('the constitutional monarchy of 1791', 'the Republic of 1792', 'In 1791 the king remained head of state but shared power with an elected Legislative Assembly; in 1792 the monarchy was abolished and France became a republic governed by the National Convention.'),
               ('the Terror', 'the Directory', 'The Terror (1793–94) was a period of radical, centralised emergency government and mass executions; the Directory (1795–99) was a more moderate, weaker government run by five directors.')],
     misc=[('The Declaration of the Rights of Man gave equal rights to everyone in France.', 'It proclaimed equality of "men and citizens", but women did not gain political rights and slavery in the colonies continued until 1794 (and was restored by Napoleon in 1802).'),
           ('Most victims of the Terror were nobles.', 'Nobles were a minority of those executed; most victims were peasants and workers, many in regions of rebellion such as the Vendée.'),
           ('Napoleon reversed everything the Revolution had achieved.', 'He ended political liberty, but kept equality before the law, the abolition of feudalism and careers open to talent in the Napoleonic Code.')],
     cases=[('the Women\'s March on Versailles (5–6 October 1789)', 'Thousands of Parisian women marched to Versailles over the price of bread and forced the royal family to move to Paris.', 'popular pressure in the Revolution', 'ordinary people, including women, directly shaped events and put the king under the watch of Paris.'),
            ('the Napoleonic Code (1804)', 'It established equality before the law, secular authority and property rights, but reduced women\'s rights within the family; it was spread across conquered Europe.', 'the legacy of the Revolution under Napoleon', 'some revolutionary principles were kept and exported, while political liberty was limited.')],
     evaluate=[('Napoleon betrayed the French Revolution.', ['he ended elected government and made himself emperor', 'he restored slavery in the colonies and censored the press'], ['he kept equality before the law and the abolition of feudal privileges', 'his code spread revolutionary principles across Europe'], 'He betrayed its political ideals of liberty and popular sovereignty, but preserved and spread many of its social and legal achievements.')],
     src=[('Speech to the National Convention (paraphrased)', 'The speaker argued that in a time of revolution the government needed both virtue and terror: virtue, without which terror was harmful, and terror, without which virtue was powerless. He described terror as swift, severe justice used to defend the Republic against its enemies.', 'Paraphrase of Maximilien Robespierre, speech to the National Convention, 5 February 1794', 'to justify the policies of the Committee of Public Safety to the Convention', 'It shows how the leaders of the Terror justified their actions in their own words.', 'It is a political speech designed to defend the government, so it presents terror as principled and does not show its victims\' experience.', 'Terror was a necessary form of justice to protect the Republic.')],
     rq=[('Why did the Revolution become more radical in 1792–93?', 'Was the French Revolution good?', 'it is a vague value judgement covering many years with no criteria', 'It investigates causation over a clear period, with speeches, laws and secondary interpretations available.', 'Build a timeline 1791–93; research the flight to Varennes, the war and food prices; read speeches by Robespierre and Danton; read two historians; weigh causes; evaluate sources.')])
C.chronology(K, 'ch01-st3', c='C3', d=(1, 3), events=FR_EVENTS)

K.st('ch01-st4', 'the consequences and legacy of the revolutions: liberty, equality and democracy',
     terms=[('liberalism', 'a political ideology stressing individual rights, constitutional government and the rule of law'),
            ('popular sovereignty', 'the principle that political power belongs to the people'),
            ('Congress of Vienna', 'the 1814–15 meeting of European powers that redrew the map after Napoleon and restored many monarchies'),
            ('Bill of Rights (USA)', 'the first ten amendments to the US Constitution, ratified in 1791, protecting freedoms such as speech, religion and trial by jury'),
            ('Haitian Revolution', 'the 1791–1804 uprising of enslaved people in the French colony of Saint-Domingue that created the independent state of Haiti'),
            ('Atlantic revolutions', 'the wave of revolutions between about 1775 and 1830 in North America, France, Haiti and Latin America')],
     facts=[('In which year was the US Bill of Rights ratified?', '1791', ['1776', '1787', '1865'], 'It was the first ten amendments to the Constitution.'),
            ('Who led independence movements in present-day Venezuela, Colombia, Ecuador, Peru and Bolivia?', 'Simón Bolívar', ['Toussaint Louverture', 'Giuseppe Garibaldi', 'Napoleon Bonaparte'], 'He is known as "El Libertador".'),
            ('In which year did Haiti declare independence?', '1804', ['1776', '1791', '1830'], 'It was the first state founded after a successful slave revolt.'),
            ('Which wave of revolutions spread across Europe in a single year?', 'The revolutions of 1848', ['The revolutions of 1689', 'The revolutions of 1917', 'The revolutions of 1956'], 'Uprisings occurred in France, the German states, Austria and Italy.'),
            ('The Congress of Vienna (1815) mainly aimed to…', 'restore monarchies and a balance of power after Napoleon', ['spread democracy across Europe', 'create the United Nations', 'abolish slavery worldwide'], 'Metternich of Austria was a key figure.')],
     why=[('Explain why the French Revolution influenced the rest of Europe.', 'Its ideas of liberty, equality and national sovereignty spread through pamphlets and Napoleon\'s conquests, which abolished feudal privileges and introduced the Napoleonic Code in many states.'),
          ('Explain why the revolutions of the late 18th century inspired independence in Latin America.', 'Creole elites read Enlightenment ideas, saw the American and Haitian examples, and when Napoleon invaded Spain in 1808 the authority of the Spanish crown collapsed, creating an opportunity for independence.'),
          ('Explain why the ideals of the revolutions were not applied to everyone at the time.', 'The revolutionaries were mostly property-owning men who limited voting rights by wealth and gender, and economic interests kept slavery in place in the USA and many colonies.'),
          ('Explain why the Haitian Revolution is significant in world history.', 'It was the only successful revolt by enslaved people to create a state, it challenged the idea that liberty was only for Europeans, and it influenced debates on abolition.')],
     contrast=[('the American Revolution', 'the French Revolution', 'The American Revolution was a colonial war of independence that created a federal republic but largely kept the existing social order; the French Revolution overturned an absolute monarchy and the whole system of privilege, with far more violence and radical social change.'),
               ('a short-term consequence', 'a long-term legacy', 'A short-term consequence happened soon after (e.g. war across Europe in the 1790s); a long-term legacy lasted for generations (e.g. ideas of human rights that influenced the 1948 UDHR).')],
     misc=[('The revolutions of the 18th century immediately created full democracies.', 'Voting was restricted by property and gender; universal male suffrage came later and women\'s suffrage much later.'),
           ('After 1815 the ideas of the French Revolution disappeared.', 'Monarchies were restored, but liberal and nationalist ideas revived in 1830 and 1848 and shaped the 19th century.'),
           ('The American Revolution ended slavery in the United States.', 'Slavery continued in the southern states until the 13th Amendment in 1865, although some northern states abolished it earlier.')],
     cases=[('the Haitian Revolution (1791–1804)', 'Enslaved people in Saint-Domingue rose up; under leaders such as Toussaint Louverture and Jean-Jacques Dessalines they defeated French forces and declared Haiti independent in 1804.', 'the spread of revolutionary ideals', 'enslaved people applied the language of liberty and equality to themselves, going further than the French revolutionaries.'),
            ('the revolutions of 1848', 'Uprisings across Europe demanded constitutions, national unity and wider voting rights; most were defeated within two years, but serfdom was abolished in the Austrian Empire.', 'the long-term legacy of 1789', 'liberal and nationalist ideas first spread in the 1790s continued to inspire revolution decades later.')],
     evaluate=[('The French Revolution had a greater impact on the world than the American Revolution.', ['it overturned an entire social system and spread its ideas across Europe by conquest', 'it influenced nationalism, liberalism and later revolutions everywhere'], ['the American Revolution created the first modern constitutional republic, which lasted', 'it inspired the French and Latin American revolutions'], 'Overall the French Revolution had the wider and deeper impact, but the American Revolution provided the first successful model and helped trigger the French one.')],
     src=[('Declaration of independence (paraphrased)', 'The generals declared that they had sworn to the people to renounce France for ever and to die rather than live under its rule. They proclaimed that the island would now be called Haiti, its original name, and that it would be free and independent.', 'Paraphrase of the Haitian Declaration of Independence, issued by Jean-Jacques Dessalines, Gonaïves, 1 January 1804', 'to proclaim independence and rally the people against any return of French rule and slavery', 'It is the founding document of Haiti and shows how its leaders understood their revolution.', 'As a proclamation it presents a united, defiant message and does not show divisions or the views of ordinary people.', 'Haiti is free and independent and will never again accept French rule.')],
     rq=[('How did the ideas of the French Revolution influence the Haitian Revolution between 1791 and 1804?', 'What happened after the French Revolution?', 'it is too broad – it covers the whole world and would produce a narrative', 'It investigates the transfer of ideas between revolutions and links to global interactions and rights.', 'Read the 1789 Declaration and the Haitian Declaration; read two secondary sources; compare language and aims in a table; consider differences in context; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch01-st4', c='C3', d=(1, 3), events=REV_EVENTS + [('the Congress of Vienna ends', 1815), ('the revolutions of 1848', 1848)])

# =============================================================================================
# ch02 Nationalism in Europe and India
# =============================================================================================
NAT_EVENTS = [('the founding of Young Italy by Mazzini', 1831), ('the creation of the Zollverein', 1834), ('the Frankfurt Parliament meets', 1848),
              ('Bismarck\'s "blood and iron" speech', 1862), ('the proclamation of the Kingdom of Italy', 1861), ('the Austro-Prussian War', 1866),
              ('the proclamation of the German Empire at Versailles', 1871), ('the founding of the Indian National Congress', 1885),
              ('the partition of Bengal', 1905), ('the assassination of Franz Ferdinand', 1914), ('the Salt March', 1930), ('Indian independence', 1947)]

K.st('ch02-st1', 'nationalism: nation, state, identity and national symbols',
     terms=[('nation', 'a large group of people who share a sense of common identity, often based on language, culture, history or territory'),
            ('state', 'a political unit with a defined territory, a government and sovereignty'),
            ('nation-state', 'a state whose people largely share one national identity'),
            ('nationalism', 'a belief that a nation should have its own state and that loyalty to the nation is very important'),
            ('civic nationalism', 'nationalism based on shared citizenship, values and laws rather than ethnicity'),
            ('ethnic nationalism', 'nationalism based on shared ancestry, language or culture'),
            ('imagined community', 'Benedict Anderson\'s idea (1983) that a nation is a community whose members feel connected though they will never meet most of each other')],
     facts=[('Which French writer described a nation in 1882 as "a daily plebiscite"?', 'Ernest Renan', ['Voltaire', 'Alexis de Tocqueville', 'Victor Hugo'], 'He argued a nation rests on the shared will to live together.'),
            ('"La Marseillaise", later France\'s anthem, was written in which year?', '1792', ['1789', '1815', '1871'], 'It was a war song of the Revolution.'),
            ('Which is an example of a stateless nation?', 'The Kurds', ['The Japanese', 'The French', 'The Brazilians'], 'Kurds live mainly across Türkiye, Iraq, Iran and Syria.'),
            ('Benedict Anderson argued that which invention helped nations to be "imagined"?', 'Print capitalism – mass-produced books and newspapers', ['The steam engine', 'The telephone', 'Television'], 'Shared texts in common languages linked strangers.')],
     why=[('Explain why national symbols such as flags and anthems are important to nationalism.', 'They give people a shared, emotional sign of belonging, are used in schools, ceremonies and sport, and help millions of strangers feel part of one community.'),
          ('Explain why language has often been central to nationalism.', 'A shared language allows communication, literature and newspapers that build common identity; nationalists such as the Grimm brothers collected folk tales to show a shared culture.'),
          ('Explain why nationalism can both unite and divide people.', 'It can bring people together into a state and motivate cooperation, but it can also exclude minorities who do not fit the national identity and create conflict with neighbours.'),
          ('Explain why the boundaries of nations and states often do not match.', 'Borders were drawn by wars, empires and treaties that ignored where peoples lived, so some nations are split across states and some states contain many nations.')],
     contrast=[('a nation', 'a state', 'A nation is a community of people with a shared identity; a state is a political unit with territory, government and sovereignty. A nation may exist without a state (e.g. the Kurds).'),
               ('civic nationalism', 'ethnic nationalism', 'Civic nationalism defines the nation by shared citizenship and values open to all (e.g. the French Republic\'s ideal); ethnic nationalism defines it by ancestry, language or culture, which can exclude minorities.')],
     misc=[('Nations have existed in the same form since ancient times.', 'Many historians argue that modern nations developed mainly from the late 18th century, through print, schooling and politics.'),
           ('Nationalism is always aggressive.', 'Nationalism has also driven independence from empires and democratic movements, such as in India.'),
           ('A state and a nation are the same thing.', 'A state is a political unit; a nation is a community of identity. They often overlap but are not identical.')],
     cases=[('the Kurds', 'About 30–40 million Kurds live mainly across Türkiye, Iraq, Iran and Syria; the Kurdistan Region of Iraq has had autonomy since the 1990s, but there is no Kurdish state.', 'a stateless nation', 'a strong sense of national identity does not guarantee statehood.'),
            ('the Grimm brothers\' "Children\'s and Household Tales" (1812)', 'Jacob and Wilhelm Grimm collected German folk tales partly to show a shared German culture at a time when there was no German state.', 'culture as a basis for nationalism', 'collecting language and stories helped people imagine a common nation.')],
     evaluate=[('Nationalism has done more harm than good.', ['it fuelled wars, including the First World War, and the persecution of minorities', 'ethnic nationalism has excluded and harmed people seen as outsiders'], ['it inspired movements for self-determination and freedom from empire', 'it helped build democratic states and welfare systems based on shared citizenship'], 'Nationalism has caused great harm when exclusive and aggressive, but civic and anti-colonial nationalism have also achieved freedom and democracy; its effects depend on its form.')],
     src=[('Lecture (paraphrased)', 'The speaker argued that a nation is not defined by race, language, religion or geography alone. It is a soul, a spiritual principle, made of a shared past of glory and sacrifice and a present desire to live together. A nation\'s existence is a daily plebiscite.', 'Paraphrase of Ernest Renan, lecture "What is a Nation?", Sorbonne, Paris, 1882', 'to argue that nations are based on shared will, partly in response to Germany\'s annexation of Alsace-Lorraine', 'It is a classic statement of civic nationalism by an influential thinker.', 'It was shaped by French interests: Renan wanted to argue that Alsace was French despite its German dialect.', 'A nation rests on shared memories and the will to live together, not on race or language.')],
     rq=[('How have national symbols been used in Indian Republic Day celebrations since 1950 to promote national unity?', 'What is a nation?', 'it is a definition question that leads to description', 'It analyses identity and symbols in a specific context with visual and written sources.', 'Collect official programmes, photographs and news coverage of Republic Day parades; identify symbols; analyse their meaning; compare decades; evaluate the government origin of sources; cite in APA.')])
C.chronology(K, 'ch02-st1', c='C3', d=(1, 3), events=NAT_EVENTS)

K.st('ch02-st2', 'the unification of Italy and Germany',
     terms=[('Risorgimento', 'the 19th-century movement for the political unification and "resurgence" of Italy'),
            ('Realpolitik', 'politics based on practical considerations of power rather than ideals, associated with Bismarck and Cavour'),
            ('Zollverein', 'the customs union of German states led by Prussia from 1834, which removed tariffs between members'),
            ('Expedition of the Thousand', 'Garibaldi\'s 1860 campaign with about a thousand volunteers (the Redshirts) that conquered Sicily and Naples'),
            ('Kleindeutschland', '"little Germany": a united Germany without Austria, led by Prussia'),
            ('Franco-Prussian War', 'the 1870–71 war in which Prussia and its allies defeated France, leading to the creation of the German Empire')],
     facts=[('Who founded the nationalist society Young Italy in 1831?', 'Giuseppe Mazzini', ['Count Cavour', 'Giuseppe Garibaldi', 'Victor Emmanuel II'], 'He wanted a united Italian republic.'),
            ('Where was the German Empire proclaimed on 18 January 1871?', 'The Hall of Mirrors at Versailles', ['Berlin\'s Reichstag', 'Frankfurt\'s St Paul\'s Church', 'Vienna'], 'It was a humiliation for defeated France.'),
            ('Which battle in 1866 decided the Austro-Prussian War?', 'Königgrätz (Sadowa)', ['Sedan', 'Solferino', 'Waterloo'], 'Prussia defeated Austria in seven weeks.'),
            ('Who was the first king of united Italy in 1861?', 'Victor Emmanuel II', ['Napoleon III', 'Wilhelm I', 'Charles Albert'], 'He had been king of Piedmont-Sardinia.'),
            ('Which city became the capital of Italy after its capture in 1870?', 'Rome', ['Turin', 'Florence', 'Milan'], 'French troops protecting the Pope had withdrawn.')],
     why=[('Explain why Cavour sought an alliance with France.', 'Piedmont was too weak to drive Austria out of northern Italy alone; at Plombières (1858) Napoleon III promised help in return for Nice and Savoy, and French armies helped defeat Austria in 1859.'),
          ('Explain why Bismarck fought three wars between 1864 and 1871.', 'Each war removed an obstacle to Prussian-led unification: Denmark (1864) over Schleswig-Holstein, Austria (1866) to exclude it from Germany, and France (1870–71) to bring the southern states in through shared nationalist feeling.'),
          ('Explain why the Zollverein helped German unification.', 'It linked the German states\' economies under Prussian leadership, built railways and common interests, and excluded Austria, so Prussia was seen as the natural leader.'),
          ('Explain why Garibaldi handed his conquests in southern Italy to Victor Emmanuel II.', 'Although a republican, he put unity first; meeting the king at Teano in 1860 avoided civil war and foreign intervention and allowed the south to join the new kingdom.')],
     contrast=[('the role of Mazzini', 'the role of Cavour', 'Mazzini was an idealist who spread the idea of a united, democratic Italian republic through propaganda and uprisings; Cavour was a pragmatic politician who used diplomacy and alliances to expand Piedmont under its monarchy.'),
               ('Italian unification', 'German unification', 'Italian unification relied on foreign help (France), popular volunteers (Garibaldi) and annexation of states over 1859–70; German unification was driven mainly by Prussian military power and Bismarck\'s diplomacy, completed in 1871.')],
     misc=[('Italy and Germany were unified mainly by popular revolutions.', 'The 1848 revolutions failed; unification came mainly through the diplomacy and wars of Piedmont and Prussia, though popular nationalism helped.'),
           ('Bismarck planned every step of German unification from the start.', 'Historians debate this: Bismarck was skilful at exploiting opportunities, but much depended on events and other powers\' mistakes.'),
           ('After 1861 all Italians felt Italian.', 'Most people spoke regional dialects; a politician famously remarked that having made Italy, they now had to make Italians.')],
     cases=[('the Expedition of the Thousand (1860)', 'Garibaldi landed in Sicily with about a thousand volunteers, won popular support and took Naples, then handed the south to Victor Emmanuel II.', 'popular nationalism in the Risorgimento', 'a volunteer army with local support achieved what diplomacy could not in the south.'),
            ('the Ems Telegram (1870)', 'Bismarck edited a report of a meeting between King Wilhelm and the French ambassador to make it seem insulting; France declared war.', 'Realpolitik', 'manipulating news provoked a war that united the German states against France.')],
     evaluate=[('Bismarck was the main reason for the unification of Germany.', ['his diplomacy isolated each enemy and his wars removed the obstacles', 'he manipulated events such as the Ems Telegram'], ['Prussia\'s economic strength (Zollverein, coal, railways) and army reforms made victory possible', 'nationalist feeling and the mistakes of Austria and France also mattered'], 'Bismarck was the decisive individual, but he succeeded because of Prussian economic and military power and favourable international circumstances.')],
     src=[('Speech to a parliamentary committee (paraphrased)', 'The minister-president told the Prussian budget committee that Germany did not look to Prussia\'s liberalism but to its power. The great questions of the day would not be decided by speeches and majority votes – that had been the mistake of 1848 and 1849 – but by iron and blood.', 'Paraphrase of Otto von Bismarck, speech to the Budget Committee of the Prussian Landtag, 30 September 1862', 'to persuade liberal deputies to approve army spending', 'It shows Bismarck\'s own view of how unification would be achieved, early in his career.', 'It was a speech meant to win a budget argument and caused outrage at the time; it should not be read as a full plan.', 'German unity will be achieved by military power, not liberal debate.')],
     rq=[('How important was Prussia\'s economic strength in the unification of Germany between 1834 and 1871?', 'Who was Bismarck?', 'it is a biographical question that leads to description', 'It weighs one factor against others (Bismarck, war, nationalism) with data on the Zollverein, railways and coal.', 'Collect economic data (coal, rail, Zollverein members); read two historians; compare factors in a table; build a timeline; evaluate historians\' perspectives; cite in MLA.')])
C.chronology(K, 'ch02-st2', c='C3', d=(1, 3), events=NAT_EVENTS[:7] + [('Garibaldi\'s Expedition of the Thousand', 1860), ('the capture of Rome', 1870), ('the Danish War', 1864), ('the Battle of Solferino', 1859)])

K.st('ch02-st3', 'the Indian national movement: the Congress, Gandhi and non-cooperation',
     terms=[('Indian National Congress', 'the political party founded in Bombay in 1885 that led the movement for Indian independence'),
            ('swaraj', 'self-rule; for Gandhi also self-discipline and freedom from dependence'),
            ('satyagraha', 'Gandhi\'s method of non-violent resistance, meaning "truth-force" or "holding firmly to truth"'),
            ('swadeshi', 'the movement to use Indian-made goods and boycott British goods, especially after the partition of Bengal in 1905'),
            ('Non-Cooperation Movement', 'the 1920–22 campaign of boycotting British institutions, goods and honours, called off after violence at Chauri Chaura'),
            ('Purna Swaraj', '"complete independence", declared as Congress\'s goal at Lahore in December 1929')],
     facts=[('In which year was the Indian National Congress founded?', '1885', ['1857', '1905', '1920'], 'Its first session met in Bombay.'),
            ('On which date did the Jallianwala Bagh massacre take place in Amritsar?', '13 April 1919', ['15 August 1947', '12 March 1930', '8 August 1942'], 'Troops under General Dyer fired on an unarmed crowd.'),
            ('Why did Gandhi call off the Non-Cooperation Movement in February 1922?', 'Protesters killed policemen at Chauri Chaura', ['Britain granted independence', 'Congress split into two parties', 'He was elected Prime Minister'], 'He insisted on non-violence.'),
            ('How far did Gandhi and his followers walk on the Salt March to Dandi in 1930?', 'About 385 km (240 miles)', ['About 38 km', 'About 3 850 km', 'About 15 km'], 'It lasted 24 days, 12 March–6 April 1930.'),
            ('Which movement did Gandhi launch on 8 August 1942?', 'Quit India', ['Non-Cooperation', 'Civil Disobedience', 'Swadeshi'], 'Its slogan was "Do or die".')],
     why=[('Explain why the Jallianwala Bagh massacre strengthened the national movement.', 'The shooting of hundreds of unarmed people, and the support Dyer received in Britain, convinced many moderate Indians that British rule could not be reformed; Rabindranath Tagore returned his knighthood.'),
          ('Explain why Gandhi chose salt for his campaign in 1930.', 'The salt tax affected every Indian, rich or poor, Hindu or Muslim; making salt was a simple, non-violent act anyone could do, and it attracted worldwide attention.'),
          ('Explain why Gandhi was able to turn Congress into a mass movement.', 'He used simple symbols (khadi, the spinning wheel, salt), non-violent methods ordinary people could join, and linked national demands to peasants\' and workers\' grievances, travelling widely across India.'),
          ('Explain why the partition of Bengal in 1905 led to the swadeshi movement.', 'Bengalis saw it as a "divide and rule" policy to weaken nationalism; they responded by boycotting British goods, burning foreign cloth and promoting Indian industries and schools.')],
     contrast=[('the moderates in Congress', 'the extremists in Congress', 'Moderates (e.g. Gokhale, Naoroji) used petitions and constitutional methods to seek reform within the empire; extremists (e.g. Tilak, "Lal–Bal–Pal") demanded swaraj and used mass protest and boycott.'),
               ('non-cooperation', 'civil disobedience', 'Non-cooperation (1920–22) meant refusing to work with British institutions; civil disobedience (1930–34) went further by deliberately breaking unjust laws, such as the salt law.')],
     misc=[('Gandhi alone won India\'s independence.', 'Many leaders and groups contributed – Nehru, Patel, Bose, Ambedkar, revolutionaries, peasants and workers – and Britain\'s weakness after the Second World War also mattered.'),
           ('The Congress always demanded full independence.', 'Early Congress sought reforms within British rule; complete independence (Purna Swaraj) became its official goal only in 1929.'),
           ('All Indians supported Congress.', 'The Muslim League, many princely rulers and some Dalit leaders had different aims and concerns.')],
     cases=[('the Salt March (1930)', 'Gandhi and 78 followers walked from Sabarmati to Dandi and made salt from seawater on 6 April 1930; civil disobedience spread and about 60 000 people were arrested.', 'satyagraha as a method of mass protest', 'a symbolic, non-violent act involved ordinary people and won international sympathy.'),
            ('the Champaran satyagraha (1917)', 'Gandhi supported indigo farmers in Bihar who were forced to grow indigo for European planters; an official inquiry led to reforms.', 'Gandhi\'s early methods in India', 'linking local peasant grievances to non-violent protest built mass support.')],
     evaluate=[('Non-violent protest was the most important reason why India gained independence in 1947.', ['satyagraha built a mass movement and won international sympathy', 'it made British rule morally and practically harder to sustain'], ['the Second World War weakened Britain economically and militarily', 'the 1946 naval mutiny, revolutionary movements and Bose\'s INA showed British control of the army was weakening'], 'Non-violent mass protest was central in creating a nationwide demand, but independence in 1947 also depended on Britain\'s post-war weakness and other forms of pressure.')],
     src=[('Book (paraphrased)', 'The author argued that India had not been taken by the English; Indians had given it to them by cooperating with British rule. If Indians stopped cooperating – in trade, courts, schools and government – British power would end. True swaraj meant ruling ourselves, not simply replacing English rulers with Indian ones.', 'Paraphrase of M. K. Gandhi, "Hind Swaraj" (Indian Home Rule), written in 1909 as a dialogue', 'to set out Gandhi\'s ideas on self-rule and non-cooperation for Indian readers', 'It is Gandhi\'s own early statement of the ideas behind non-cooperation and swaraj.', 'It was written before Gandhi returned to India and is a philosophical argument, not evidence of what Indians actually thought or did.', 'British rule depends on Indian cooperation; withdrawing it would bring real self-rule.')],
     rq=[('How did the Salt March change international opinion of British rule in India in 1930?', 'Who was Gandhi?', 'it is biographical and would produce a narrative', 'It investigates the impact of non-violent protest using international newspaper sources.', 'Collect reports from British, American and Indian newspapers (March–May 1930); compare perspectives in a table; read two secondary sources; evaluate origin and purpose; cite in MLA.')])
C.chronology(K, 'ch02-st3', c='C3', d=(1, 3), events=[NAT_EVENTS[7], NAT_EVENTS[8], NAT_EVENTS[10], NAT_EVENTS[11]] + [('the Jallianwala Bagh massacre', 1919), ('the Quit India Movement', 1942), ('Gandhi\'s return to India', 1915), ('the start of the Non-Cooperation Movement', 1920), ('the Lahore declaration of Purna Swaraj', 1929), ('the founding of the Muslim League', 1906)])

K.st('ch02-st4', 'nationalism as a cause of conflict and the road to 1914',
     terms=[('Pan-Slavism', 'a movement to unite or protect Slavic peoples, with Russia as their leader'),
            ('Balkan Wars', 'two wars in 1912–13 in which Balkan states fought the Ottoman Empire and then each other'),
            ('Black Hand', 'a secret Serbian nationalist society linked to the assassination of Archduke Franz Ferdinand'),
            ('revanchism', 'the desire to win back lost territory, such as French wishes to recover Alsace-Lorraine'),
            ('Weltpolitik', 'Germany\'s "world policy" under Wilhelm II to gain colonies, a navy and great-power status'),
            ('self-determination', 'the right of a people to decide their own government and form their own state')],
     facts=[('Who assassinated Archduke Franz Ferdinand in Sarajevo on 28 June 1914?', 'Gavrilo Princip', ['Kaiser Wilhelm II', 'Otto von Bismarck', 'Tsar Nicholas II'], 'He belonged to Young Bosnia, linked to the Black Hand.'),
            ('Which region did France lose to Germany in 1871 and want to recover?', 'Alsace-Lorraine', ['Bosnia', 'Schleswig', 'Savoy'], 'Its loss fuelled French revanchism.'),
            ('In which year did Austria-Hungary annex Bosnia-Herzegovina, angering Serbia?', '1908', ['1878', '1912', '1914'], 'Many Bosnians were Serbs.'),
            ('Which battleship, launched by Britain in 1906, started a new naval race with Germany?', 'HMS Dreadnought', ['HMS Victory', 'Bismarck', 'Titanic'], 'It made older battleships obsolete.')],
     why=[('Explain why the Balkans were called "the powder keg of Europe" before 1914.', 'Declining Ottoman power left competing nationalist states (Serbia, Bulgaria, Greece) and the rival ambitions of Austria-Hungary and Russia in one region, so a local crisis could ignite a great-power war.'),
          ('Explain why Serbian nationalism threatened Austria-Hungary.', 'Serbia wanted to unite South Slavs, including those inside Austria-Hungary; the multinational empire feared that if one group broke away, others would follow.'),
          ('Explain why nationalism made the great powers less willing to back down in a crisis.', 'Public opinion, the press and nationalist leagues demanded prestige and strength, so leaders feared that compromise would be seen as national humiliation.'),
          ('Explain why Russia supported Serbia.', 'As the leading Slavic and Orthodox power, Russia claimed to protect Slavs (Pan-Slavism) and wanted influence in the Balkans and access to the Straits; after backing down in 1908 it was unwilling to do so again.')],
     contrast=[('nationalism within Austria-Hungary', 'nationalism in Germany', 'In Austria-Hungary nationalism by subject peoples (Czechs, Serbs, Croats) threatened to break the empire apart; in Germany nationalism united people behind an assertive great-power policy (Weltpolitik).'),
               ('a long-term cause', 'the immediate cause of the First World War', 'Long-term causes include nationalism, alliances, militarism and imperial rivalry; the immediate cause was the assassination of Franz Ferdinand on 28 June 1914 and the July Crisis that followed.')],
     misc=[('The assassination of Franz Ferdinand alone caused the First World War.', 'It was the trigger; the war happened because of alliances, nationalism, militarism and decisions taken in the July Crisis.'),
           ('Nationalism in 1914 affected only the Balkans.', 'It shaped every great power – French revanchism, German Weltpolitik, British naval pride and Russian Pan-Slavism.'),
           ('Everyone in 1914 opposed the war.', 'Large crowds celebrated in many capitals and most socialist parties supported their governments, though some opposed the war.')],
     cases=[('the Bosnian Crisis of 1908–09', 'Austria-Hungary annexed Bosnia-Herzegovina; Serbia protested and Russia backed down after German pressure.', 'how nationalism created tension', 'Serbian and Russian resentment grew, making both less willing to compromise in 1914.'),
            ('the Balkan Wars (1912–13)', 'Balkan states drove the Ottomans out of most of Europe, then fought over the spoils; Serbia doubled in size.', 'nationalism and the road to war', 'a stronger, more confident Serbia alarmed Austria-Hungary.')],
     evaluate=[('Nationalism was the most important long-term cause of the First World War.', ['Balkan nationalism created the crisis that started the war', 'nationalist public opinion pushed governments towards confrontation'], ['the alliance system turned a local war into a European war', 'militarism and war plans such as the Schlieffen Plan made escalation rapid'], 'Nationalism was a key underlying cause and created the spark, but alliances and militarism explain why a Balkan crisis became a world war.')],
     src=[('Historian\'s book (paraphrased)', 'The historian argued that the outbreak of war in 1914 was not the fault of one power. The leaders of every major state were like sleepwalkers – watchful but unseeing – moving step by step into a catastrophe that none of them fully intended.', 'Paraphrase of Christopher Clark, "The Sleepwalkers: How Europe Went to War in 1914", 2012', 'to present a historical interpretation of the outbreak of war for historians and general readers', 'It is a major, well-researched modern interpretation using archives from many countries.', 'Other historians, such as those following Fritz Fischer, place more blame on Germany; it is one interpretation among several.', 'All the great powers shared responsibility, stumbling into a war none fully wanted.')],
     rq=[('How far did Serbian nationalism make war between Austria-Hungary and Serbia likely between 1903 and 1914?', 'Why do wars happen?', 'it is too broad and theoretical to investigate with sources', 'It focuses on one factor and one relationship over a clear period, with diplomatic documents available.', 'Build a timeline 1903–1914; read extracts of the Austrian ultimatum and Serbian reply; read two historians; analyse evidence in a table; evaluate perspectives; cite in APA.')])
C.chronology(K, 'ch02-st4', c='C3', d=(1, 3), events=[('the Congress of Berlin', 1878), ('the launch of HMS Dreadnought', 1906), ('the annexation of Bosnia', 1908), ('the First Balkan War', 1912), ('the assassination of Franz Ferdinand', 1914), ('the creation of the German Empire', 1871), ('the Franco-Russian Alliance', 1894), ('the Entente Cordiale', 1904)])

# =============================================================================================
# ch03 Imperialism and Colonial Rule
# =============================================================================================
IMP_EVENTS = [('the opening of the Suez Canal', 1869), ('the Berlin Conference opens', 1884), ('the Battle of Adwa', 1896), ('the Indian Rebellion begins', 1857),
              ('Queen Victoria proclaimed Empress of India', 1877), ('the British occupation of Egypt', 1882), ('the Boer War begins', 1899),
              ('Leopold II hands the Congo to the Belgian state', 1908), ('the partition of Bengal', 1905), ('the publication of Hobson\'s "Imperialism"', 1902)]

K.st('ch03-st1', 'the motives for imperialism: economic, political, religious and social Darwinist',
     terms=[('imperialism', 'the policy of extending a country\'s power and influence over other territories, by conquest, colonisation or economic control'),
            ('colony', 'a territory ruled by another country'),
            ('social Darwinism', 'the misuse of Darwin\'s ideas to claim that some races or nations were "fitter" than others and had a right to dominate them – an idea now rejected as racist and unscientific'),
            ('"civilising mission"', 'the claim by colonial powers that they had a duty to spread their religion, culture and institutions to colonised peoples'),
            ('protectorate', 'a territory that keeps its own ruler but is controlled by a foreign power, especially in foreign affairs'),
            ('strategic motive', 'the wish to control places important for defence, trade routes or naval bases, such as Suez or Gibraltar')],
     facts=[('Which economist argued in 1902 that imperialism was driven by the search for new places to invest surplus capital?', 'J. A. Hobson', ['Adam Smith', 'John Maynard Keynes', 'David Ricardo'], 'Lenin later developed this argument in 1917.'),
            ('Which waterway, opened in 1869, made Egypt strategically vital to Britain?', 'The Suez Canal', ['The Panama Canal', 'The Kiel Canal', 'The Grand Canal'], 'It shortened the route to India.'),
            ('Which Scottish missionary and explorer became famous in Britain for his travels in Central Africa?', 'David Livingstone', ['Cecil Rhodes', 'Henry Morton Stanley', 'Lord Lugard'], 'He linked "Christianity, commerce and civilisation".'),
            ('Which British businessman dreamed of a railway "from the Cape to Cairo"?', 'Cecil Rhodes', ['David Livingstone', 'Lord Curzon', 'Rudyard Kipling'], 'He founded the British South Africa Company.'),
            ('What new raw material from Central Africa was in high demand for bicycle and car tyres from the 1890s?', 'Rubber', ['Coal', 'Wool', 'Oil'], 'Demand led to forced labour in the Congo Free State.')],
     why=[('Explain why industrialisation increased European interest in colonies after 1870.', 'Factories needed raw materials such as cotton, rubber and palm oil, industrial nations sought protected markets for their goods and places to invest capital, and new technology (steamships, quinine, machine guns) made conquest easier.'),
          ('Explain why political rivalry between European powers encouraged imperial expansion.', 'Colonies were seen as a sign of great-power status; powers raced to claim land before rivals did, and nationalist public opinion celebrated imperial gains.'),
          ('Explain why social Darwinism was used to justify imperialism.', 'It falsely claimed that some peoples were naturally superior and destined to rule others, giving a pseudo-scientific excuse for conquest and racial hierarchy.'),
          ('Explain why religion was a motive for imperialism.', 'Missionary societies wanted to spread Christianity, and campaigners argued that colonial rule would end the slave trade and bring "civilisation"; missionaries often arrived before or alongside colonial rule.')],
     contrast=[('an economic motive for imperialism', 'a strategic motive for imperialism', 'An economic motive concerns profit – raw materials, markets and investment; a strategic motive concerns security – controlling routes, ports and bases such as Suez or Aden.'),
               ('a colony', 'a protectorate', 'A colony is ruled directly by the colonial power; a protectorate keeps its own ruler and institutions but is controlled by the foreign power, especially in defence and foreign affairs.')],
     misc=[('Imperialism was always profitable for the colonial power.', 'Some colonies cost more to govern and defend than they earned; profits went mainly to particular companies and investors.'),
           ('Social Darwinism was a scientific theory supported by Darwin\'s evidence.', 'It was a political misuse of Darwin\'s ideas, promoted by writers such as Herbert Spencer, and has no scientific basis.'),
           ('Colonised peoples accepted European rule passively.', 'There was widespread resistance – from the Battle of Adwa (1896) and the Maji Maji rising (1905–07) to the Indian rebellion of 1857.')],
     cases=[('the British occupation of Egypt (1882)', 'Britain invaded to protect the Suez Canal and the interests of European bondholders after a nationalist revolt led by Colonel Urabi.', 'strategic and economic motives', 'the canal and debts made Egypt too important to Britain to leave.'),
            ('the Congo Free State (1885–1908)', 'King Leopold II ruled the Congo as his personal property; forced labour to collect rubber led to mass deaths and mutilation, exposed by campaigners such as E. D. Morel and Roger Casement.', 'economic motives and the human cost of empire', 'the drive for profit from rubber led to extreme exploitation.')],
     evaluate=[('Economic motives were the most important reason for European imperialism after 1870.', ['industrial economies needed raw materials, markets and investment opportunities', 'companies such as Leopold\'s and Rhodes\'s drove expansion'], ['strategic rivalry and national prestige pushed powers to grab land with little economic value', 'missionary and racial ideas gave expansion public support'], 'Economic motives were central, but imperialism was driven by a combination; strategic rivalry often explains why territory with little economic value was seized.')],
     src=[('Economic study (paraphrased)', 'The author argued that imperialism did not benefit the nation as a whole. Instead it served a small group of financiers and industrialists who needed new places to invest surplus capital, while taxpayers paid for the armies and navies that protected these investments.', 'Paraphrase of J. A. Hobson, "Imperialism: A Study", London, 1902', 'to criticise imperialism and argue for social reform at home', 'It is an influential contemporary analysis by a British economist, written soon after the Boer War.', 'Hobson was a critic who wanted to show imperialism was harmful, so he emphasised economic motives and may underplay strategic and political ones.', 'Imperialism served the interests of a few investors, not the whole nation.')],
     rq=[('Why did Germany seek colonies in Africa after 1884, despite Bismarck\'s earlier reluctance?', 'Why did countries have empires?', 'it is too broad and covers all of history', 'It focuses on one power, one turning point and a range of motives with sources available.', 'Read two secondary sources; examine Bismarck\'s statements and colonial society propaganda; weigh economic, political and domestic motives in a table; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch03-st1', c='C3', d=(1, 3), events=IMP_EVENTS)

K.st('ch03-st2', 'the Scramble for Africa and the Berlin Conference of 1884–85',
     terms=[('Scramble for Africa', 'the rapid invasion, occupation and division of Africa by European powers between about 1881 and 1914'),
            ('Berlin Conference', 'the 1884–85 meeting of European powers (and the USA and Ottoman Empire), hosted by Bismarck, that set rules for claiming African territory'),
            ('effective occupation', 'the Berlin principle that a power could claim African land only if it actually controlled it'),
            ('sphere of influence', 'an area where one power claims special rights to trade and influence, recognised by rivals'),
            ('Maxim gun', 'an early machine gun, used by colonial forces with devastating effect against African armies'),
            ('arbitrary borders', 'boundaries drawn by colonial powers without regard to existing peoples, languages and states')],
     facts=[('Roughly what share of Africa was under European control in 1870?', 'About 10%', ['About 50%', 'About 90%', 'None of it'], 'By 1914 it was about 90%.'),
            ('Which two African states remained independent of European rule in 1914?', 'Ethiopia and Liberia', ['Egypt and Morocco', 'Nigeria and Ghana', 'Kenya and Sudan'], 'Ethiopia defeated Italy at Adwa in 1896.'),
            ('Who hosted the Berlin Conference?', 'Otto von Bismarck', ['Queen Victoria', 'King Leopold II', 'Napoleon III'], 'It met from November 1884 to February 1885.'),
            ('Were any African rulers invited to the Berlin Conference?', 'No', ['Yes, all of them', 'Only the Emperor of Ethiopia', 'Only the Sultan of Zanzibar'], 'Africa was divided without Africans present.'),
            ('Which Ethiopian emperor defeated the Italian army at Adwa in 1896?', 'Menelik II', ['Haile Selassie', 'Tewodros II', 'Shaka'], 'It secured Ethiopian independence.')],
     why=[('Explain why the Scramble for Africa happened so quickly after 1880.', 'Rivalry between European powers turned into a race for land; new technology (quinine, steamships, railways, the Maxim gun) made conquest possible, and the Berlin Conference set rules that encouraged rapid claims.'),
          ('Explain why Ethiopia was able to resist colonisation.', 'Menelik II modernised his army with imported rifles and artillery, united regional rulers and used diplomacy, so Ethiopia defeated Italy decisively at Adwa in 1896.'),
          ('Explain why the borders drawn during the Scramble caused long-term problems.', 'They were drawn by Europeans for their own interests, often with straight lines, splitting peoples between states and joining rivals together, which later contributed to disputes and conflicts.'),
          ('Explain why technology gave Europeans an advantage in Africa.', 'Quinine reduced deaths from malaria, steamships opened rivers, railways moved troops, and machine guns such as the Maxim gave small forces overwhelming firepower.')],
     contrast=[('direct rule', 'indirect rule', 'Under direct rule, colonial officials governed themselves (common in French colonies); under indirect rule, colonial powers governed through existing local rulers who answered to them (e.g. Lugard in northern Nigeria).'),
               ('resistance in Ethiopia', 'resistance in German East Africa', 'Ethiopia defeated an invading army at Adwa and stayed independent; the Maji Maji rising (1905–07) in German East Africa was crushed, with very heavy loss of life from fighting and famine.')],
     misc=[('The Berlin Conference divided all of Africa between the European powers.', 'It set rules for claiming territory (such as effective occupation); most borders were agreed in later treaties and conquests over the next 30 years.'),
           ('Africa had no states or governments before colonial rule.', 'Africa had many kingdoms and empires – such as Asante, the Sokoto Caliphate, Buganda and Ethiopia – with their own governments and laws.'),
           ('All of Africa was colonised without resistance.', 'Resistance was widespread – Adwa, the Anglo-Zulu War (Isandlwana, 1879), Asante, Maji Maji and many others.')],
     cases=[('the Battle of Adwa (1 March 1896)', 'Ethiopian forces under Menelik II defeated an Italian army; Italy recognised Ethiopian independence in the Treaty of Addis Ababa.', 'African resistance', 'a modernised, united African state could defeat a European invader.'),
            ('the Berlin Conference (1884–85)', 'Fourteen states agreed rules on free trade on the Congo and Niger rivers and on effective occupation, and recognised Leopold II\'s Congo Free State.', 'how the Scramble was organised', 'European powers made decisions about African land among themselves, with no African representatives.')],
     evaluate=[('The Berlin Conference was the main cause of the Scramble for Africa.', ['it set rules that triggered a race to establish effective occupation', 'it recognised claims such as the Congo Free State'], ['the Scramble had already begun, e.g. the French in Tunisia (1881) and the British in Egypt (1882)', 'deeper causes were industrial demand, rivalry and new technology'], 'The conference speeded up and organised the Scramble, but it was a product of rivalry and economic forces that had already started it.')],
     src=[('Conference document (paraphrased)', 'The powers agreed that any power which in future takes possession of a territory on the coasts of the African continent, or assumes a protectorate there, must notify the other signatory powers, and must ensure an authority sufficient to protect existing rights and freedom of trade.', 'Paraphrase of Articles 34 and 35 of the General Act of the Berlin Conference, 26 February 1885', 'to set agreed rules between European powers for claiming African territory', 'It is the official agreement and shows the principle of effective occupation in the powers\' own words.', 'It shows only the European powers\' perspective; no African voices were present, and it does not show how rules were applied on the ground.', 'Powers had to notify others and actually control territory to claim it.')],
     rq=[('Why was Ethiopia able to defeat Italy at the Battle of Adwa in 1896?', 'What happened in Africa?', 'it is far too broad, covering a continent and no time period', 'It investigates causation of a turning point in African resistance, with Ethiopian, Italian and secondary sources.', 'Read two secondary sources; collect evidence on weapons, leadership, numbers and diplomacy; compare Italian and Ethiopian accounts; evaluate perspectives; present causes in a diagram; cite in MLA.')])
C.chronology(K, 'ch03-st2', c='C3', d=(1, 3), events=IMP_EVENTS)
C.pct_change(K, 'ch03-st2', [('the share of Africa under European control', 'per cent of the continent\'s area', 1870, 10, 1914, 90, 'approx., historians\' estimates')], d=(1, 2))

K.st('ch03-st3', 'British rule in India after 1857: the Raj, the economy and resistance',
     terms=[('the Raj', 'the period of direct British Crown rule over India from 1858 to 1947'),
            ('Viceroy', 'the British monarch\'s representative who governed India'),
            ('Indian Civil Service (ICS)', 'the elite administrative service that ran British India, dominated by British officials'),
            ('separate electorates', 'a system, introduced by the Morley–Minto reforms of 1909, in which Muslims voted for their own representatives'),
            ('famine codes', 'rules issued from the 1880s for how officials should respond to famine'),
            ('princely states', 'states ruled by Indian princes under British overlordship, covering about two-fifths of the subcontinent')],
     facts=[('Which document of 1 November 1858 announced Crown rule and promised religious non-interference?', 'Queen Victoria\'s Proclamation', ['The Regulating Act', 'The Government of India Act 1935', 'The Rowlatt Act'], 'It followed the rebellion of 1857.'),
            ('In which year was Queen Victoria proclaimed Empress of India?', '1877', ['1858', '1901', '1911'], 'A great durbar was held in Delhi.'),
            ('Which Viceroy partitioned Bengal in 1905?', 'Lord Curzon', ['Lord Dalhousie', 'Lord Mountbatten', 'Lord Irwin'], 'It was reversed in 1911.'),
            ('About how much railway track had been built in India by 1900?', 'About 40 000 km', ['About 400 km', 'About 4 000 km', 'About 400 000 km'], 'It was one of the largest networks in the world.'),
            ('Which political organisation was founded in Dhaka in 1906?', 'The All-India Muslim League', ['The Indian National Congress', 'The Hindu Mahasabha', 'The Communist Party of India'], 'It sought to represent Muslim interests.')],
     why=[('Explain why the rebellion of 1857 changed the way Britain ruled India.', 'Britain ended Company rule, governed directly through a Viceroy, reorganised the army to have more British soldiers, stopped annexing princely states and promised not to interfere in religion.'),
          ('Explain why railways in British India had mixed effects.', 'They moved troops and exported raw materials to benefit British trade, but also united markets, eased famine relief in later years and helped Indians travel and organise nationally.'),
          ('Explain why there were severe famines in British India in the late 19th century.', 'Monsoon failure caused crop failure, but exports of grain, high revenue demands, slow relief and policies that favoured markets over aid turned shortages into mass deaths, as in 1876–78.'),
          ('Explain why educated Indians increasingly opposed British rule after 1880.', 'Western education spread ideas of rights and representation, yet Indians were kept out of top posts, faced racial discrimination (e.g. the Ilbert Bill controversy of 1883) and saw economic drain, so they organised politically.')],
     contrast=[('British India', 'the princely states', 'British India was governed directly by British officials; the princely states were ruled by Indian princes who accepted British overlordship and advisers.'),
               ('economic benefits claimed for British rule', 'economic criticisms of British rule', 'Supporters pointed to railways, irrigation and a unified administration; critics like Naoroji and R. C. Dutt highlighted the drain of wealth, high land revenue, deindustrialisation and famines.')],
     misc=[('India was a single colony governed in the same way everywhere.', 'About two-fifths was made up of princely states with their own rulers, and British India itself had different revenue and legal systems by province.'),
           ('Railways were built mainly to help Indian people.', 'They were planned largely for military and commercial purposes, though Indians used them extensively.'),
           ('Resistance to British rule ended after 1857.', 'Resistance continued through peasant movements, the Congress, the swadeshi movement and revolutionary groups.')],
     cases=[('the Great Famine of 1876–78', 'After monsoon failure in southern and western India, an estimated 5–10 million people died while grain continued to be exported and relief was limited.', 'the economic impact of colonial policy', 'policy choices about revenue and relief turned crop failure into catastrophe.'),
            ('the partition of Bengal (1905)', 'Lord Curzon divided Bengal into a Muslim-majority east and Hindu-majority west; mass protest and the swadeshi boycott forced its reversal in 1911.', 'resistance to colonial rule', 'a colonial decision seen as "divide and rule" provoked a mass movement.')],
     evaluate=[('British rule brought more benefits than costs to India between 1858 and 1914.', ['railways, telegraphs and irrigation canals were built', 'English education and a common administration linked the subcontinent'], ['famines killed millions and wealth was drained to Britain', 'Indians were denied political power and faced racial discrimination'], 'Most historians conclude the costs outweighed the benefits for most Indians, as infrastructure served imperial interests and growth in income per head was very low.')],
     src=[('Proclamation (paraphrased)', 'The Queen declared that she had taken over the government of India from the East India Company. She promised that no one would be favoured or disturbed because of their religious faith, that Indians would be admitted to offices of the government as far as their education and ability allowed, and that the rights of the princes would be respected.', 'Paraphrase of Queen Victoria\'s Proclamation to the Princes, Chiefs and People of India, 1 November 1858', 'to reassure Indians after the rebellion and announce direct Crown rule', 'It is the official statement of British policy after 1857 and shows the promises made.', 'It states intentions, not practice; Indians were in fact largely excluded from senior posts for decades.', 'Britain promised religious tolerance, equal access to office and respect for princes under Crown rule.')],
     rq=[('How did the partition of Bengal in 1905 change the methods of the Indian national movement?', 'Was British rule good for India?', 'it is a broad value judgement without criteria, place or period', 'It investigates the impact of a specific colonial decision on resistance, with primary sources available.', 'Read Curzon\'s statements and swadeshi pamphlets; two secondary sources; compare methods before and after 1905; timeline; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch03-st3', c='C3', d=(1, 3), events=IMP_EVENTS)

K.st('ch03-st4', 'perspectives on empire from colonisers and colonised in sources',
     terms=[('perspective', 'the viewpoint from which a person or group sees events, shaped by their position, interests and values'),
            ('Eurocentrism', 'viewing the world mainly from a European point of view and treating European experience as the norm'),
            ('postcolonial', 'relating to the period after colonial rule, and to the study of colonialism\'s lasting effects'),
            ('collaboration', 'cooperation by some colonised people with colonial rulers, for reasons such as status, profit or protection'),
            ('historiography', 'the study of how history has been written and how interpretations change over time'),
            ('agency', 'the ability of people to act and make choices that shape events')],
     facts=[('Which Nigerian novelist wrote "Things Fall Apart" (1958), showing colonialism from an Igbo perspective?', 'Chinua Achebe', ['Wole Soyinka', 'Ngũgĩ wa Thiong\'o', 'Rudyard Kipling'], 'It responded to European portrayals of Africa.'),
            ('Which British poet wrote "The White Man\'s Burden" in 1899, urging the USA to take colonies?', 'Rudyard Kipling', ['Alfred Tennyson', 'William Wordsworth', 'Joseph Conrad'], 'The poem expressed the "civilising mission".'),
            ('Whose 1835 "Minute on Education" argued for teaching Indians in English?', 'Thomas Babington Macaulay', ['Lord Curzon', 'William Bentinck', 'Robert Clive'], 'It dismissed Indian learning.'),
            ('Which Indian politician\'s 2016 book "An Era of Darkness" (published in the UK as "Inglorious Empire") criticised British rule?', 'Shashi Tharoor', ['Jawaharlal Nehru', 'Amartya Sen', 'Arundhati Roy'], 'It challenged positive views of empire.')],
     why=[('Explain why sources written by colonial officials may give a limited view of empire.', 'They were written by people with an interest in presenting rule as successful and just, often for superiors or the public at home, and they rarely recorded colonised people\'s own experiences.'),
          ('Explain why historians now try to include the perspectives of colonised peoples.', 'Earlier histories relied on colonial archives and presented Europeans as the main actors; including oral histories, local sources and literature restores the agency and experiences of colonised people.'),
          ('Explain why interpretations of empire have changed over time.', 'Decolonisation, new sources, the voices of formerly colonised peoples and changing values have led historians to question earlier, more positive accounts written in the imperial age.'),
          ('Explain why literature such as "Things Fall Apart" is useful to historians.', 'Although fiction, it shows how colonised people may have experienced change, drawing on the author\'s community memory, and it challenges stereotypes in European writing.')],
     contrast=[('the colonisers\' perspective', 'the colonised perspective', 'Colonisers often presented empire as bringing order, progress and civilisation; the colonised often experienced it as conquest, exploitation, loss of land and cultural disruption, while some groups also benefited or collaborated.'),
               ('a primary source', 'a historiographical interpretation', 'A primary source comes from the period itself (e.g. Macaulay\'s Minute, 1835); a historiographical interpretation is a later historian\'s argument about the period (e.g. Niall Ferguson\'s "Empire", 2003).')],
     misc=[('There is only one correct perspective on empire.', 'Different groups experienced empire differently; historians compare perspectives to build a fuller picture.'),
           ('Colonised peoples had no agency under colonial rule.', 'They resisted, negotiated, collaborated, adapted and shaped colonial societies in many ways.'),
           ('A source that praises empire is useless for historians.', 'It is very useful for understanding imperial attitudes and propaganda, even if it is not reliable about colonised people\'s experiences.')],
     cases=[('Macaulay\'s "Minute on Education" (1835)', 'Macaulay argued that English education would create a class of Indians "Indian in blood and colour, but English in taste" to help govern India; the government adopted English-medium education.', 'a coloniser\'s perspective', 'the source reveals the belief in European cultural superiority that shaped policy.'),
            ('Chinua Achebe\'s "Things Fall Apart" (1958)', 'The novel shows a complex Igbo society in the late 19th century before and after the arrival of missionaries and colonial government.', 'the perspective of the colonised', 'literature by a colonised people\'s writer challenges European portrayals of Africa as without history or culture.')],
     evaluate=[('Historians can only understand empire by using sources from the colonised.', ['colonial sources are biased and hide the experiences of most people', 'oral histories and local sources show agency and resistance'], ['colonial records contain vital evidence on policies, statistics and decisions', 'comparing both perspectives gives the fullest understanding'], 'Disagree: sources from the colonised are essential but not sufficient; historians need to compare colonised and colonial sources critically.')],
     src=[('Official minute (paraphrased)', 'The official argued that the government\'s funds for education should be spent on teaching English and Western science rather than Sanskrit or Arabic learning, which he dismissed as inferior. He hoped to create a class of Indians who would act as interpreters between the British and the millions they governed.', 'Paraphrase of Thomas Babington Macaulay, "Minute on Indian Education", 2 February 1835', 'to persuade the Governor-General to fund English-language education in India', 'It shows clearly the cultural attitudes that shaped colonial education policy.', 'It reflects a British official\'s assumptions of superiority; Macaulay knew no Sanskrit or Arabic, and it gives no Indian perspective.', 'English education should replace Indian learning to create a class of Indian intermediaries.')],
     rq=[('How do British and Indian accounts of the 1857 rebellion differ in the way they describe its causes?', 'What did people think about empire?', 'it is vague – which people, which empire, when?', 'It practises comparing perspectives (criterion D) on one event using accessible sources.', 'Collect two British and two Indian accounts (e.g. contemporary newspapers, V. D. Savarkar 1909, official reports); analyse each with OPVL; compare causes in a table; evaluate; cite in MLA.')])

# =============================================================================================
# ch04 Urbanisation and Urban Challenges
# =============================================================================================
URB = [('the share of the world\'s population living in urban areas', 'per cent', [(1950, 29.6), (1975, 37.7), (2000, 46.7), (2018, 55.3), (2030, 60.4), (2050, 68.4)], 'UN World Urbanization Prospects 2018; 2030 and 2050 projected'),
       ('the population of Lagos, Nigeria', 'million', [(1950, 0.33), (1970, 1.4), (1990, 4.8), (2010, 10.4), (2020, 14.4)], 'UN estimates of the urban agglomeration'),
       ('the population of Dhaka, Bangladesh', 'million', [(1950, 0.34), (1970, 1.4), (1990, 6.6), (2010, 14.7), (2020, 21.0)], 'UN estimates of the urban agglomeration')]

K.st('ch04-st1', 'urbanisation trends in HICs and LICs and the rise of megacities',
     terms=[('urbanisation', 'the increase in the proportion of a country\'s population living in towns and cities'),
            ('urban growth', 'the increase in the number of people living in urban areas, or in the area a city covers'),
            ('megacity', 'a city or urban agglomeration with more than 10 million inhabitants'),
            ('counter-urbanisation', 'the movement of people from cities to rural areas and small towns'),
            ('suburbanisation', 'the outward growth of a city as people and businesses move to the suburbs'),
            ('primate city', 'a city that is much larger than any other in its country and dominates its economy and politics, such as Lima or Bangkok')],
     facts=[('In about which year did more than half of the world\'s population first live in urban areas?', '2007', ['1950', '1980', '2030'], 'UN-DESA estimated the crossover around 2007–2008.'),
            ('How many megacities were there in 1950?', 'Two – New York and Tokyo', ['None', 'Ten', 'Thirty-three'], 'There were 33 in 2018.'),
            ('Which is the world\'s largest urban agglomeration?', 'Tokyo', ['Lagos', 'Mumbai', 'London'], 'It has about 37 million people.'),
            ('What share of the world\'s population does the UN project will be urban by 2050?', 'About 68%', ['About 30%', 'About 50%', 'About 95%'], 'World Urbanization Prospects 2018.'),
            ('In which world regions is urban growth now fastest?', 'Sub-Saharan Africa and South Asia', ['Western Europe and North America', 'Australia and New Zealand', 'Scandinavia'], 'Cities like Lagos, Kinshasa and Dhaka are growing rapidly.')],
     why=[('Explain why urbanisation is now fastest in low-income countries.', 'Many people still live in rural areas and move to cities for jobs and services, and cities also grow through high natural increase among young urban populations.'),
          ('Explain why high-income countries have slower urban growth than LICs.', 'They urbanised during industrialisation, so about 80% already live in cities; birth rates are low and some people move out to suburbs and rural areas (counter-urbanisation).'),
          ('Explain why megacities have become more common since 1950.', 'Rapid population growth and rural–urban migration in Asia, Africa and Latin America have concentrated people in a few large economic centres that attract investment, jobs and infrastructure.'),
          ('Explain why primate cities develop in some countries.', 'Power, investment, ports and services are concentrated in one city – often the former colonial capital – so it attracts most migrants and grows far larger than other cities.')],
     contrast=[('urbanisation', 'urban growth', 'Urbanisation is an increase in the proportion of people living in urban areas; urban growth is an increase in the number of urban dwellers or the area covered by cities. A city can grow without urbanisation if the rural population grows equally fast.'),
               ('urbanisation in HICs', 'urbanisation in LICs', 'In HICs urbanisation happened mainly in the 19th and early 20th centuries with industrialisation and is now slow; in LICs it is happening now, very rapidly, often faster than jobs and housing can be provided.')],
     misc=[('Most of the world\'s urban growth is happening in Europe and North America.', 'Most urban growth now happens in Asia and Africa; HIC cities grow slowly.'),
           ('Megacities are only found in rich countries.', 'Most megacities are now in Asia, Africa and Latin America – e.g. Dhaka, Lagos, Kinshasa, Mumbai, São Paulo.'),
           ('Urbanisation means the rural population is falling everywhere.', 'In many LICs the rural population is still growing in number even as the urban share rises.')],
     cases=[('Lagos, Nigeria', 'Lagos grew from about 0.3 million in 1950 to over 14 million in 2020, driven by migration from rural Nigeria and West Africa and by natural increase.', 'rapid urbanisation in an LIC', 'jobs in Nigeria\'s main port and commercial centre attract millions, faster than infrastructure can keep up.'),
            ('Tokyo, Japan', 'Tokyo became a megacity by the 1950s and is now the largest urban area at about 37 million people, though its population is beginning to age and stabilise.', 'urbanisation in an HIC', 'early industrial growth created a megacity that now faces ageing rather than rapid growth.')],
     evaluate=[('Rapid urbanisation brings more benefits than problems to low-income countries.', ['cities offer jobs, higher wages, education and health care', 'urban economies drive national growth and innovation'], ['growth often outpaces housing and services, creating informal settlements', 'congestion, pollution and inequality increase'], 'Urbanisation can drive development, but only if planning and investment in housing, transport and services keep pace; otherwise problems may outweigh benefits for the poorest.')],
     src=[('UN report (paraphrased)', 'The report stated that 55% of the world\'s population lived in urban areas in 2018 and that this share was projected to rise to 68% by 2050. Close to 90% of the increase in urban population would take place in Asia and Africa, and just three countries – India, China and Nigeria – would account for over a third of the growth.', 'Summary of United Nations DESA, "World Urbanization Prospects: The 2018 Revision"', 'to provide data and projections on urbanisation for governments and planners', 'The UN is the main global source of urban data and uses national censuses.', 'Definitions of "urban" vary between countries, and projections may change as birth rates and migration change.', 'The world is rapidly urbanising, with most future growth in Asia and Africa.')],
     rq=[('Why has the population of Dhaka grown so rapidly since 1990?', 'What is a city?', 'it is a definition question with nothing to investigate', 'It investigates the causes of rapid urban growth in a real megacity with UN data and case studies.', 'Collect UN population data; graph growth; research push factors (river erosion, flooding) and pull factors (garment industry); read two case studies; evaluate sources; cite in APA.')])
C.rate_of_change(K, 'ch04-st1', URB)
C.pct_change(K, 'ch04-st1', [('the number of megacities in the world', 'megacities', 1990, 10, 2018, 33, 'UN DESA'),
                              ('the urban population of India', 'million', 1951, 62, 2011, 377, 'Census of India')], d=(1, 3))

K.st('ch04-st2', 'push and pull factors of rural–urban migration',
     terms=[('rural–urban migration', 'the movement of people from the countryside to towns and cities'),
            ('push factor', 'a negative aspect of a place that encourages people to leave, such as unemployment, drought or conflict'),
            ('pull factor', 'a positive aspect of a place that attracts people, such as jobs, schools or health care'),
            ('intervening obstacle', 'a barrier between origin and destination, such as cost, distance or laws, that may stop people migrating'),
            ('hukou', 'China\'s household registration system, which ties access to public services to a person\'s registered place of origin'),
            ('remittance', 'money sent home by migrants to their families')],
     facts=[('About how many rural migrant workers were there in China in 2023?', 'About 300 million', ['About 3 million', 'About 30 million', 'About 1 billion'], 'China\'s National Bureau of Statistics reported about 298 million.'),
            ('Which of these is a pull factor of cities?', 'Better access to hospitals and schools', ['Drought', 'Land shortage', 'Crop failure'], 'Services attract migrants.'),
            ('Who developed a model of migration with origin, destination and intervening obstacles in 1966?', 'Everett Lee', ['Ernest Burgess', 'Walter Christaller', 'Thomas Malthus'], 'Lee\'s push–pull model.'),
            ('Which Chinese system limits migrants\' access to city schools and health care?', 'The hukou system', ['The one-child policy', 'The Belt and Road Initiative', 'The Great Leap Forward'], 'It has been gradually relaxed.')],
     why=[('Explain why the mechanisation of farming can push people to cities.', 'Machines replace farm labourers, so fewer jobs remain in rural areas and people move to cities to find work.'),
          ('Explain why migrants often move to cities even when urban jobs are insecure.', 'Average urban wages are still higher than rural incomes, there is a chance of a better job, and access to schools and health care is better; families may also diversify income through remittances.'),
          ('Explain why climate change may increase rural–urban migration.', 'Droughts, floods and rising seas damage crops and land, reducing rural livelihoods, especially in places such as coastal Bangladesh and the Sahel.'),
          ('Explain why young adults are the group most likely to migrate to cities.', 'They have fewer family ties, more years to benefit from higher wages, are more likely to be seeking education or a first job, and are more willing to take risks.')],
     contrast=[('a push factor', 'a pull factor', 'Push factors drive people away from where they live (unemployment, drought, conflict); pull factors attract them to a destination (jobs, services, family networks).'),
               ('voluntary migration', 'forced migration', 'Voluntary migration is chosen, usually for economic or family reasons; forced migration happens when people have no real choice, because of conflict, persecution or disaster.')],
     misc=[('People move to cities only because of pull factors.', 'Most migration results from a combination of push and pull factors and personal circumstances.'),
           ('Rural–urban migrants all live in slums.', 'Many find formal housing and jobs; outcomes vary greatly with skills, networks and the city.'),
           ('Migration always means moving permanently.', 'Much rural–urban migration is temporary or circular – e.g. seasonal construction work or returning home for harvests.')],
     cases=[('China\'s rural migrant workers', 'Since the 1980s, hundreds of millions have moved from inland provinces to coastal cities such as Shenzhen and Guangzhou to work in factories and construction, often leaving children with grandparents.', 'push and pull factors', 'higher factory wages pulled migrants, while limited rural income pushed them; the hukou system shaped their lives in cities.'),
            ('migration from Bangladesh\'s coastal districts to Dhaka', 'River erosion, cyclones and salinisation of farmland push many people to Dhaka, where the garment industry offers jobs.', 'environmental push factors', 'environmental change combined with urban jobs drives migration.')],
     evaluate=[('Push factors are more important than pull factors in explaining rural–urban migration.', ['rural poverty, land shortage and climate shocks force many to leave', 'environmental disasters create sudden movement'], ['cities attract migrants with higher wages and services even when rural life is stable', 'migrant networks pull family members to particular cities'], 'Both matter: push factors often explain why people leave, but pull factors and networks explain where they go; the balance differs by place and person.')],
     src=[('Survey report (paraphrased)', 'A survey of newly arrived migrants in Dhaka found that most had moved for economic reasons – especially to find work in the garment sector – but many also named river erosion, floods or loss of land as reasons for leaving their villages. Most sent part of their earnings back to their families.', 'Summary of findings of studies of migration to Dhaka by the International Organization for Migration (IOM) and Bangladeshi researchers, 2010s', 'to inform policy on migration and urban planning', 'It is based on interviews with migrants themselves and shows the mix of push and pull factors.', 'Surveys rely on what people choose to report, and a sample of new arrivals may not represent all migrants.', 'Migrants to Dhaka move mainly for work, but environmental losses also push them, and many send remittances home.')],
     rq=[('What are the main push and pull factors for families who have moved to our city in the last ten years?', 'Why do people move?', 'it is too broad and general to investigate with evidence', 'It applies the push–pull model to a local context using interviews and census data.', 'Collect census data on migration; interview ten families (with consent); code reasons as push or pull; present in a chart; compare with Lee\'s model; evaluate ethics and sampling.')])
C.pct_change(K, 'ch04-st2', [('the number of rural migrant workers in China', 'million', 2008, 225, 2023, 298, 'National Bureau of Statistics of China'),
                              ('remittances received by Bangladesh', 'US$ billion', 2010, 10.9, 2023, 21.9, 'World Bank')], d=(1, 3))

K.st('ch04-st3', 'urban challenges: informal settlements, traffic, pollution and services',
     terms=[('informal settlement', 'an area of housing built without legal permission, often lacking secure tenure, water, sanitation and services'),
            ('slum', 'an urban area of overcrowded, poor-quality housing lacking basic services'),
            ('informal economy', 'work that is not taxed, registered or protected by labour laws, such as street vending'),
            ('traffic congestion', 'when there are too many vehicles for the road space, causing slow journeys and pollution'),
            ('urban heat island', 'the effect by which cities are warmer than surrounding rural areas'),
            ('site-and-service scheme', 'a housing project in which authorities provide plots with water, sanitation and roads, and residents build their own homes')],
     facts=[('About how many people live in slums or informal settlements worldwide (UN-Habitat estimate, 2020s)?', 'Over 1 billion', ['About 10 million', 'About 100 million', 'About 5 billion'], 'Most are in Asia and Africa.'),
            ('Dharavi, one of Asia\'s largest informal settlements, is in which city?', 'Mumbai', ['Nairobi', 'Rio de Janeiro', 'Manila'], 'Up to a million people live in about 2 km².'),
            ('Kibera is an informal settlement in which city?', 'Nairobi', ['Lagos', 'Johannesburg', 'Cairo'], 'It is often described as one of Africa\'s largest.'),
            ('Which city introduced a congestion charge for central London in 2003?', 'London', ['Paris', 'Delhi', 'New York'], 'Drivers pay a daily fee to enter the zone.'),
            ('Rocinha is a large favela in which city?', 'Rio de Janeiro', ['São Paulo', 'Lima', 'Buenos Aires'], 'It lies on a steep hillside.')],
     why=[('Explain why informal settlements grow in rapidly expanding cities.', 'Migrants and low-income residents cannot afford formal housing, and governments cannot build homes and services fast enough, so people build on unused or unsafe land.'),
          ('Explain why informal settlements are often built in hazardous locations.', 'Steep slopes, floodplains, rubbish dumps and land beside railways are unwanted by formal developers, so the poorest residents settle there despite the risks of landslides and floods.'),
          ('Explain why traffic congestion is a major problem in cities such as Jakarta and Lagos.', 'Car ownership has grown faster than road and public transport capacity, cities have sprawled, and many people commute long distances to central jobs.'),
          ('Explain why informal settlements are also places of economic activity.', 'Residents run businesses such as recycling, pottery, garment work and food production; Dharavi\'s informal economy is estimated at hundreds of millions of dollars a year.')],
     contrast=[('the formal economy', 'the informal economy', 'The formal economy consists of registered, taxed jobs with contracts and legal protection; the informal economy consists of unregistered work, such as street vending, with no contracts or protection.'),
               ('slum clearance', 'slum upgrading', 'Slum clearance demolishes informal housing and relocates residents, often to the city edge; upgrading improves the existing area with water, sanitation, paths and secure tenure, keeping communities in place.')],
     misc=[('Everyone in informal settlements is unemployed.', 'Most residents work, often in the informal economy or in low-paid formal jobs; informal settlements are busy economic hubs.'),
           ('Building more roads will solve traffic congestion.', 'New roads often attract more traffic (induced demand); public transport, cycling and land-use planning are usually more effective.'),
           ('Urban problems only exist in low-income countries.', 'High-income cities also face homelessness, congestion, air pollution and unaffordable housing.')],
     cases=[('Dharavi, Mumbai', 'Up to a million people live in about 2.1 km²; thousands of small businesses recycle plastics, make leather goods and pottery, but sanitation and water are very limited.', 'the challenges and opportunities of informal settlements', 'high density and poor services coexist with a dynamic informal economy.'),
            ('air pollution in Delhi', 'In winter Delhi often records PM2.5 levels many times above WHO guidelines because of vehicle and industrial emissions, construction dust and crop burning in neighbouring states.', 'urban environmental challenges', 'multiple local and regional sources combine with weather to create severe pollution.')],
     evaluate=[('Upgrading informal settlements is better than replacing them.', ['it keeps communities, jobs and social networks in place', 'it is cheaper and improves conditions quickly, as in Rio\'s Favela-Bairro programme'], ['some sites are too hazardous to upgrade safely', 'upgrading may not provide enough space or quality housing'], 'Upgrading is usually the better approach where sites are safe, because it improves lives without destroying livelihoods; relocation should be a last resort with residents\' consent.')],
     src=[('UN-Habitat report (paraphrased)', 'The report defines a slum household as one lacking one or more of the following: improved water, improved sanitation, durable housing, sufficient living area, or security of tenure. It estimates that over a billion people live in such conditions, mostly in Asia and sub-Saharan Africa.', 'Summary of UN-Habitat, "World Cities Report" and slum indicators, 2020–2022', 'to measure urban poverty and guide policy towards the Sustainable Development Goals', 'It provides a clear, internationally agreed definition and global estimates.', 'Measuring informal settlements is difficult and estimates depend on national data quality.', 'More than a billion people live in slum conditions, defined by lack of water, sanitation, durable housing, space or tenure.')],
     rq=[('How effective has the Favela-Bairro programme been in improving living conditions in Rio de Janeiro\'s favelas since 1994?', 'Why are slums bad?', 'it is a closed, judgemental question that ignores residents\' perspectives', 'It evaluates a real urban management strategy using reports and residents\' views.', 'Read programme reports and two academic studies; compare indicators (water, sanitation, crime) before and after; find residents\' views in interviews or documentaries; evaluate sources; cite in APA.')])
C.pct_change(K, 'ch04-st3', [('the number of registered vehicles in Delhi', 'million', 2000, 3.4, 2022, 13.2, 'approx., Delhi Transport Department')], d=(1, 3))
C.density(K, 'ch04-st3', c='C3', d=(2, 3))

K.st('ch04-st4', 'planning sustainable cities, including a case study of a smart city',
     terms=[('sustainable city', 'a city designed to meet the needs of its people while reducing its environmental impact and remaining liveable for future generations'),
            ('smart city', 'a city that uses digital technology and data to manage services such as transport, energy and water more efficiently'),
            ('bus rapid transit (BRT)', 'a bus system with dedicated lanes and stations that works like a surface metro'),
            ('green infrastructure', 'parks, green roofs, street trees and wetlands that provide environmental benefits in cities'),
            ('mixed-use development', 'areas that combine housing, shops and workplaces so that people need to travel less'),
            ('Internet of Things', 'networks of sensors and devices that collect and share data, such as traffic or energy use')],
     facts=[('Which Brazilian city pioneered bus rapid transit in 1974?', 'Curitiba', ['Rio de Janeiro', 'Brasília', 'Manaus'], 'Its tube stations allow fast boarding.'),
            ('Which country launched its "Smart Nation" initiative in 2014?', 'Singapore', ['Japan', 'Germany', 'Kenya'], 'It uses sensors and data for transport and services.'),
            ('Songdo, a planned smart city, is in which country?', 'South Korea', ['China', 'India', 'the UAE'], 'It was built on reclaimed land near Incheon.'),
            ('Masdar City, begun in 2006 as a low-carbon city, is near which city?', 'Abu Dhabi', ['Dubai', 'Riyadh', 'Doha'], 'Its original zero-carbon targets were scaled back.'),
            ('Which Colombian city built cable cars (Metrocable) in 2004 to connect hillside neighbourhoods?', 'Medellín', ['Bogotá', 'Cali', 'Cartagena'], 'It reduced travel times for poorer residents.')],
     why=[('Explain why public transport is central to making cities sustainable.', 'It moves many people using less energy and space per person than cars, reducing congestion, emissions and air pollution, and gives access to jobs for people without cars.'),
          ('Explain why smart-city technology raises concerns about privacy.', 'Sensors, cameras and apps collect large amounts of data about people\'s movements and behaviour, which could be misused by governments or companies without strong safeguards.'),
          ('Explain why green infrastructure helps cities adapt to climate change.', 'Trees and green roofs cool the urban heat island, parks and wetlands absorb heavy rain and reduce flooding, and greenery improves air quality and wellbeing.'),
          ('Explain why some planned smart cities have struggled to attract residents.', 'Top-down projects such as Songdo or Masdar were expensive, sometimes far from existing jobs and communities, and built around technology rather than residents\' needs.')],
     contrast=[('a smart city', 'a sustainable city', 'A smart city uses digital technology and data to manage services; a sustainable city aims to meet people\'s needs with low environmental impact. A smart city is not automatically sustainable, and sustainable cities do not need high technology.'),
               ('top-down planning', 'bottom-up planning', 'Top-down planning is led by governments or developers, often for whole new districts; bottom-up planning involves local communities shaping changes to their own neighbourhoods.')],
     misc=[('A smart city is automatically a sustainable city.', 'Technology can improve efficiency, but sustainability also depends on reducing consumption, social equity and green space.'),
           ('Sustainable cities must be built from scratch.', 'Most sustainable change happens by retrofitting existing cities – e.g. Copenhagen\'s cycle lanes or Seoul\'s restored Cheonggyecheon stream.'),
           ('Sustainability is only about the environment.', 'Sustainable cities must also be socially fair and economically viable – affordable housing, jobs and services for all.')],
     cases=[('Curitiba, Brazil', 'Since the 1970s Curitiba has combined bus rapid transit, parks on flood-prone land and recycling schemes that exchanged waste for bus tokens or food.', 'low-cost sustainable planning', 'simple, affordable policies integrated transport, green space and social goals.'),
            ('Singapore\'s Smart Nation', 'Singapore uses electronic road pricing, sensors and open data to manage traffic, energy and water, alongside extensive green space ("City in Nature").', 'a smart city approach', 'technology and strict planning help a dense city remain efficient and liveable.')],
     evaluate=[('Smart technology is the best way to make cities sustainable.', ['data can cut energy use, manage traffic and reduce waste', 'Singapore shows the benefits of integrated technology'], ['low-tech solutions such as Curitiba\'s BRT and cycling are cheaper and proven', 'technology can be costly and raise privacy and equity concerns'], 'Technology helps, but good planning – public transport, mixed-use development, green space and community involvement – matters more than technology itself.')],
     src=[('News feature (paraphrased)', 'The reporter described Songdo as a city of glass towers, parks and pneumatic waste pipes built on reclaimed land. More than a decade after construction began, many apartments were occupied, but some residents said the city felt quiet and lacked the life of older neighbourhoods in Seoul.', 'Paraphrase of international news features on Songdo International Business District, South Korea, 2010s–2020s', 'to inform readers about a high-profile urban experiment', 'It gives an outside view and includes residents\' experiences.', 'News features may focus on striking criticisms; they do not give full data on energy use or occupancy.', 'Songdo has advanced technology and green space but some residents find it lacks community life.')],
     rq=[('How far has Curitiba\'s bus rapid transit system reduced car use since 1974?', 'Are cities sustainable?', 'it is a broad yes/no question with no place or measure', 'It evaluates a famous sustainability strategy using transport data and reports.', 'Collect data on ridership and car ownership; read two case studies and a critical article; compare with another Brazilian city; evaluate sources; cite in APA.')])

# =============================================================================================
# ch05 Ecosystems and Biomes Under Pressure
# =============================================================================================
K.st('ch05-st1', 'ecosystems: food chains, nutrient cycles and biotic and abiotic factors',
     terms=[('ecosystem', 'a community of living organisms interacting with each other and with their non-living environment'),
            ('biotic factor', 'a living part of an ecosystem, such as plants, animals, fungi and bacteria'),
            ('abiotic factor', 'a non-living part of an ecosystem, such as temperature, rainfall, sunlight and soil'),
            ('producer', 'an organism, usually a green plant, that makes its own food by photosynthesis'),
            ('decomposer', 'an organism, such as a fungus or bacterium, that breaks down dead material and returns nutrients to the soil'),
            ('trophic level', 'the position an organism occupies in a food chain'),
            ('nutrient cycle', 'the movement of nutrients between the biomass, litter and soil stores of an ecosystem')],
     facts=[('About what percentage of energy is passed on from one trophic level to the next?', 'About 10%', ['About 50%', 'About 90%', '100%'], 'Most energy is lost as heat through respiration.'),
            ('In a tropical rainforest, where are most nutrients stored?', 'In the biomass (living plants)', ['In the soil', 'In the litter', 'In the rivers'], 'Soils are poor because nutrients are recycled quickly.'),
            ('Which of these is an abiotic factor?', 'Annual rainfall', ['Fungi', 'Insects', 'Grass'], 'Abiotic means non-living.'),
            ('What is the original source of energy for almost all ecosystems?', 'The Sun', ['The soil', 'Decomposers', 'Rainfall'], 'Producers capture solar energy.')],
     why=[('Explain why food chains rarely have more than four or five trophic levels.', 'Only about 10% of energy passes to the next level; the rest is lost as heat, movement and waste, so after a few levels there is too little energy to support another population.'),
          ('Explain why tropical rainforest soils are infertile despite lush vegetation.', 'Heavy rain leaches nutrients from the soil, and dead material decomposes and is reabsorbed by plants so quickly that most nutrients are held in the biomass, not the soil.'),
          ('Explain why removing a top predator can change a whole ecosystem.', 'Prey populations grow without control, overgraze plants and alter habitats, causing a trophic cascade – as when wolves were absent from Yellowstone.'),
          ('Explain why decomposers are essential to ecosystems.', 'They break down dead organisms and waste, releasing nutrients back into the soil so producers can use them; without them nutrients would be locked in dead matter.')],
     contrast=[('a food chain', 'a food web', 'A food chain shows one feeding pathway; a food web shows many interconnected food chains in an ecosystem, giving a more realistic picture.'),
               ('biotic factors', 'abiotic factors', 'Biotic factors are living parts of an ecosystem (plants, animals, microbes); abiotic factors are non-living (climate, soil, water, light).')],
     misc=[('Energy is recycled in an ecosystem just like nutrients.', 'Nutrients are recycled, but energy flows through and is lost as heat at each level; new energy must constantly come from the Sun.'),
           ('Rainforests have very fertile soil.', 'Most rainforest soils are poor; nutrients are mainly held in the vegetation.'),
           ('Removing one species makes little difference to an ecosystem.', 'Species are interconnected; losing a keystone species can cause large changes (trophic cascades).')],
     cases=[('the reintroduction of wolves to Yellowstone National Park (1995)', 'Wolves reduced and moved elk herds; willows and aspen recovered along rivers, and beavers and songbirds returned.', 'food webs and trophic cascades', 'a top predator affected vegetation and other species through the food web.'),
            ('the nutrient cycle in the Amazon rainforest', 'Leaf litter decomposes within weeks in the hot, humid climate and nutrients are rapidly taken up by roots and fungi.', 'nutrient cycling and abiotic factors', 'warmth and moisture speed decomposition, keeping nutrients in the biomass.')],
     evaluate=[('Abiotic factors are more important than biotic factors in shaping ecosystems.', ['climate determines the global distribution of biomes', 'soil, water and sunlight limit what can live in a place'], ['keystone species such as wolves and beavers reshape habitats', 'humans, a biotic factor, now transform ecosystems everywhere'], 'Abiotic factors set the broad limits, but biotic interactions – including human activity – strongly shape how ecosystems work within those limits.')],
     src=[('National park report (paraphrased)', 'After wolves were reintroduced in 1995, the park\'s elk population declined and elk spent less time grazing along streams. Researchers recorded recovery of willow and aspen in some areas, though scientists still debate how much of this was caused by wolves and how much by drought, bears and human hunting.', 'Summary of US National Park Service information and research on wolves in Yellowstone, 2010s–2020s', 'to inform the public about wolf restoration and its ecological effects', 'It is based on long-term monitoring by park scientists.', 'It acknowledges scientific debate, so the size of the wolf effect is uncertain.', 'Wolves changed elk behaviour and helped some vegetation recover, though other factors also mattered.')],
     rq=[('How do abiotic factors (light, soil moisture and temperature) differ between the woodland edge and centre in our local park?', 'What is an ecosystem?', 'it is a definition question', 'It investigates abiotic variation with simple field measurements linked to ecosystem processes.', 'Use a transect from edge to centre; measure light, soil moisture and temperature every 5 m on three days; record; graph; relate to plant cover; evaluate equipment accuracy.')])


@R.add('ch05-st1', 'C3', (1, 5), 'numerical')
def energy_flow(rng, slot):
    eco = rng.choice([('grassland', 'grass', 'grasshoppers', 'frogs', 'snakes'), ('ocean', 'phytoplankton', 'zooplankton', 'small fish', 'tuna'),
                      ('savanna', 'grasses', 'zebras', 'lions', None), ('rainforest', 'fig trees', 'fruit bats', 'snakes', 'harpy eagles'),
                      ('tundra', 'lichens', 'caribou', 'wolves', None)])
    e0 = rng.choice([10_000, 20_000, 50_000, 100_000, 250_000])
    eff = 10 if slot.d <= 3 else rng.choice([8, 10, 12, 15])
    chain = [x for x in eco[1:] if x]
    lv = [e0]
    for _ in chain[1:]:
        lv.append(lv[-1] * eff / 100)
    if slot.d <= 2:
        return dict(stem=f'In a {eco[0]} food chain, {chain[0]} capture {e0:,} kJ of energy per m² per year. If about 10% is passed to each next level, how much energy reaches the {chain[1]}?',
                    answer=f'{e0 / 10:,.0f} kJ/m²/yr', type='numerical', marks=2,
                    markingKey=f'{e0:,} × 0.1 = {e0 / 10:,.0f} kJ (M1 A1). The other 90% is lost as heat, movement and waste.', gap='G3')
    ans = '; '.join(f'{c_}: {v:,.4g} kJ' for c_, v in zip(chain, lv))
    return dict(stem=f'A {eco[0]} food chain is: ' + ' → '.join(chain) + f'. The {chain[0]} store {e0:,} kJ of energy per m² per year and {eff}% is transferred at each step. Calculate the energy at each trophic level and explain why there are few top predators.',
                answer=ans, type='multi_step', marks=4,
                markingKey=f'Multiply by {eff / 100} at each step (M1): {ans} (A2). Explanation (R1): energy is lost at each level, so only small populations of top consumers can be supported.', gap='G3')


K.st('ch05-st2', 'global biomes: tropical rainforests, hot deserts and tundra',
     terms=[('biome', 'a large-scale ecosystem, such as tropical rainforest or tundra, defined mainly by climate and vegetation'),
            ('tropical rainforest', 'a biome near the equator with high temperatures (about 27 °C) and rainfall above 2 000 mm all year, with layered, very diverse forest'),
            ('hot desert', 'a biome receiving less than about 250 mm of rain a year, with high daytime temperatures and sparse vegetation'),
            ('tundra', 'a cold, treeless biome near the Arctic with permafrost, a short summer and low-growing plants'),
            ('permafrost', 'ground that remains frozen for at least two consecutive years'),
            ('adaptation', 'a feature that helps a plant or animal survive in its environment'),
            ('biodiversity', 'the variety of life in an area – species, genes and ecosystems')],
     facts=[('Which layer of the rainforest is formed by the tallest trees, rising above the canopy?', 'The emergent layer', ['The understorey', 'The shrub layer', 'The forest floor'], 'Emergents can exceed 50 m.'),
            ('Which is the driest non-polar desert in the world?', 'The Atacama, Chile', ['The Sahara', 'The Gobi', 'The Kalahari'], 'Some weather stations have never recorded rain.'),
            ('Tropical rainforests cover about 6% of the land surface. Roughly what share of land species do they contain?', 'More than half', ['About 1%', 'About 10%', 'Almost none'], 'They are the most biodiverse land biome.'),
            ('How long is the growing season in the Arctic tundra?', 'About 50–60 days', ['About 300 days', 'About 6 months', 'It has none'], 'Summers are short and cool.'),
            ('Which animal has long eyelashes and can close its nostrils to cope with sandstorms?', 'The dromedary camel', ['The polar bear', 'The sloth', 'The jaguar'], 'It is adapted to hot deserts.')],
     why=[('Explain why tropical rainforests have such high biodiversity.', 'Constant warmth, high rainfall and sunlight allow plants to grow all year, the layered structure creates many niches, and the biome has been stable for millions of years.'),
          ('Explain why hot deserts have a large daily temperature range.', 'Clear skies and dry air let the Sun heat the ground strongly by day and let heat escape quickly at night, so days are very hot and nights can be cold.'),
          ('Explain why tundra plants are small and grow close to the ground.', 'Low growth avoids strong, cold winds, keeps plants under insulating snow in winter and close to the warmer ground surface; permafrost also stops deep roots.'),
          ('Explain why rainforest trees have buttress roots.', 'Soils are shallow and nutrients are near the surface, so roots spread widely; large buttresses support very tall trees in shallow soil.')],
     contrast=[('the climate of a tropical rainforest', 'the climate of a hot desert', 'A rainforest is hot (about 27 °C) and wet all year (over 2 000 mm) with a small temperature range; a hot desert is hot by day, cool at night and very dry (under 250 mm), with a large daily range.'),
               ('Arctic tundra', 'Alpine tundra', 'Arctic tundra lies at high latitudes around the Arctic Ocean, with permafrost; Alpine tundra occurs above the tree line on high mountains at any latitude and often lacks permafrost.')],
     misc=[('Deserts have no life.', 'Deserts support many adapted plants and animals – cacti, acacias, camels, fennec foxes – and people such as the Tuareg.'),
           ('The rainforest is the "lungs of the Earth" and produces most of our oxygen.', 'Rainforests use much of the oxygen they produce; most atmospheric oxygen comes from ocean phytoplankton. Rainforests matter greatly for carbon storage and rainfall.'),
           ('The tundra is frozen all year.', 'The surface thaws in a short summer, creating bogs and allowing plants to flower, while the permafrost below stays frozen.')],
     cases=[('the Amazon rainforest', 'Covering about 5.5 million km² across nine countries, mostly Brazil, it holds about 10% of known species and stores vast amounts of carbon.', 'the characteristics of tropical rainforests', 'hot, wet conditions all year support layered forest and extraordinary biodiversity.'),
            ('the Alaskan tundra and the Trans-Alaska Pipeline', 'The pipeline (completed 1977) was raised on supports so that warm oil would not melt the permafrost and the caribou could pass beneath.', 'adapting human activity to the tundra', 'permafrost and wildlife shaped engineering decisions in a fragile biome.')],
     evaluate=[('Tropical rainforests are the most important biome to protect.', ['they hold the most land biodiversity and store huge amounts of carbon', 'they influence regional and global rainfall'], ['tundra permafrost stores even more carbon, which may be released as it thaws', 'deserts and grasslands support unique species and millions of people'], 'Rainforests have a strong claim because of biodiversity and carbon, but all biomes provide vital services; tundra protection is equally urgent for climate.')],
     src=[('Scientific assessment (paraphrased)', 'Permafrost soils in the Northern Hemisphere contain about 1 500 billion tonnes of carbon, roughly twice as much as is currently in the atmosphere. As the Arctic warms, thawing permafrost could release carbon dioxide and methane, adding to global warming.', 'Summary of findings in the IPCC "Special Report on the Ocean and Cryosphere in a Changing Climate", 2019', 'to inform governments of the scientific evidence on climate change in cold regions', 'It summarises peer-reviewed research agreed by scientists and governments.', 'Estimates of carbon stored and future release have wide uncertainty ranges.', 'Thawing tundra permafrost could release huge amounts of greenhouse gases.')],
     rq=[('How have the Inuit of Nunavut adapted their way of life to the tundra, and how is climate change affecting this?', 'What are biomes?', 'it is a definition question', 'It links biome characteristics with human adaptation and change, using Indigenous perspectives.', 'Read Inuit organisation reports and two secondary sources; watch an Inuit-produced documentary; record evidence in a table (traditional vs current); evaluate perspectives; cite in APA.')])
C.climate(K, 'ch05-st2', d=(1, 5))

K.st('ch05-st3', 'threats to ecosystems: deforestation, desertification and biodiversity loss',
     terms=[('deforestation', 'the clearing of forest for other land uses, such as farming, ranching, mining or roads'),
            ('desertification', 'the degradation of land in dry areas, making it more desert-like, caused by climate variation and human activities'),
            ('biodiversity loss', 'the decline in the variety of species, genes and ecosystems'),
            ('habitat fragmentation', 'the breaking up of a continuous habitat into smaller, isolated patches'),
            ('invasive species', 'a species introduced to a new area where it spreads and harms native species'),
            ('tipping point', 'a threshold beyond which an ecosystem changes rapidly and possibly irreversibly to a different state')],
     facts=[('Which activity is the largest single driver of deforestation in the Brazilian Amazon?', 'Cattle ranching', ['Logging for paper', 'Tourism', 'Urban growth'], 'Pasture occupies most cleared land.'),
            ('According to WWF\'s Living Planet Report 2024, by about how much have monitored wildlife populations declined on average since 1970?', '73%', ['7%', '27%', '97%'], 'The decline is steepest in Latin America and the Caribbean.'),
            ('Which inland sea in Central Asia shrank by about 90% after its rivers were diverted for cotton irrigation?', 'The Aral Sea', ['The Caspian Sea', 'The Dead Sea', 'Lake Baikal'], 'Soviet irrigation schemes from the 1960s diverted its rivers.'),
            ('In which year did Brazil\'s annual Amazon deforestation peak at about 27 800 km² in the 2000s?', '2004', ['1990', '2012', '2022'], 'It then fell sharply to about 4 600 km² by 2012.'),
            ('About how many species does the 2019 IPBES assessment say are threatened with extinction?', 'About 1 million', ['About 1 000', 'About 10 000', 'About 100 million'], 'Many within decades.')],
     why=[('Explain why deforestation can reduce rainfall in the Amazon.', 'Trees return large amounts of water to the air through transpiration; when forest is cleared, less moisture is recycled, so rainfall downwind falls and dry seasons lengthen.'),
          ('Explain why desertification is a problem in the Sahel.', 'Droughts combine with overgrazing, over-cultivation and cutting trees for fuel as populations grow; soil loses vegetation cover and erodes, reducing land productivity for farmers and herders.'),
          ('Explain why habitat fragmentation threatens species.', 'Small, isolated patches support smaller populations that are vulnerable to disease and inbreeding, and animals cannot move to find food, mates or new habitat as climate changes.'),
          ('Explain why biodiversity loss matters to people.', 'Ecosystems provide food, medicines, clean water, pollination, carbon storage and flood protection; losing species weakens these services and reduces resilience.')],
     contrast=[('deforestation', 'forest degradation', 'Deforestation removes forest completely and converts land to another use; degradation reduces forest quality (by selective logging or fire) while it remains forest.'),
               ('a physical cause of desertification', 'a human cause of desertification', 'Physical causes include drought and climate variability; human causes include overgrazing, over-cultivation, deforestation and poor irrigation.')],
     misc=[('Deforestation in the Amazon is mainly caused by poor farmers cutting trees for firewood.', 'Most clearing in Brazil is for large-scale cattle pasture and soy, linked to global markets and land speculation.'),
           ('Desertification means deserts are spreading naturally across the land.', 'It is land degradation in dry areas caused by a combination of climate and human use; it can occur far from existing deserts.'),
           ('Extinction is a natural process, so current biodiversity loss is not unusual.', 'Current extinction rates are estimated at tens to hundreds of times higher than the natural background rate, mainly because of human activity.')],
     cases=[('the Aral Sea', 'From the 1960s Soviet planners diverted the Amu Darya and Syr Darya to irrigate cotton; the sea shrank by about 90%, its fishing industry collapsed and salty dust storms harmed health.', 'human-caused ecosystem destruction', 'water use for one economic goal destroyed an entire aquatic ecosystem and livelihoods.'),
            ('Amazon deforestation in Brazil, 2004–2012', 'Annual clearing fell from about 27 800 km² to about 4 600 km² after satellite monitoring, new protected areas, enforcement and a soy moratorium; it rose again later.', 'the causes of deforestation and how policy affects them', 'government action and market pressure can greatly reduce clearing, but gains can be reversed.')],
     evaluate=[('Deforestation is the greatest threat to global biodiversity.', ['tropical forests hold most land species and are being cleared rapidly', 'land-use change is ranked the top driver by IPBES'], ['climate change is a growing threat to all ecosystems, including oceans and coral reefs', 'over-exploitation, pollution and invasive species also cause major losses'], 'Land-use change, including deforestation, is currently the largest driver on land, but climate change may become the greatest threat overall, and the drivers interact.')],
     src=[('Space agency data (paraphrased)', 'Brazil\'s PRODES satellite monitoring recorded about 27 800 km² of clearing in the Legal Amazon in 2004, falling to about 4 600 km² in 2012. Clearing then rose, reaching about 13 000 km² in 2021, before falling again to about 9 000 km² in 2023.', 'Summary of annual PRODES data from Brazil\'s National Institute for Space Research (INPE)', 'to provide official annual measurements of Amazon deforestation', 'It is consistent, long-term satellite data used by scientists and governments.', 'It measures clear-cutting only, not degradation by fire or selective logging; political pressure on INPE has been reported.', 'Deforestation fell sharply after 2004, rose after 2012 and fell again recently.')],
     rq=[('Why did Amazon deforestation in Brazil fall between 2004 and 2012 and then rise again?', 'Is deforestation bad?', 'it is a closed question with an obvious answer', 'It investigates change over time and the effect of policy, using INPE data and reports.', 'Download PRODES data; draw a line graph; research policies (PPCDAm, soy moratorium) and later changes; read two analyses; link causes to the trend; evaluate sources; cite in APA.')])
C.rate_of_change(K, 'ch05-st3', [('annual deforestation in the Brazilian Legal Amazon', 'km²', [(2004, 27772), (2008, 12911), (2012, 4571), (2016, 7893), (2021, 13038), (2023, 9001)], 'INPE PRODES'),
                                  ('the area of the Aral Sea', 'thousand km²', [(1960, 68), (1980, 51), (1990, 36), (2000, 25), (2010, 14)], 'approx., satellite and survey data')])

K.st('ch05-st4', 'conservation and the sustainable management of ecosystems',
     terms=[('conservation', 'the protection and careful management of ecosystems, species and natural resources'),
            ('protected area', 'an area, such as a national park, where human activity is managed to conserve nature'),
            ('payment for ecosystem services', 'a scheme that pays landowners to protect services such as forests, water or carbon storage'),
            ('REDD+', 'a UN-backed framework that pays developing countries to reduce emissions from deforestation and forest degradation'),
            ('agroforestry', 'growing trees together with crops or livestock on the same land'),
            ('rewilding', 'restoring natural processes and species, such as predators, to an area and reducing human management')],
     facts=[('Which African initiative, launched in 2007, aims to restore land across the Sahel?', 'The Great Green Wall', ['The Green Belt Movement', 'The African Union Dam', 'The Sahara Solar Project'], 'It spans about 8 000 km.'),
            ('Which country increased its forest cover from about 21% in the 1980s to over 50% today, partly through payments to landowners?', 'Costa Rica', ['Brazil', 'Indonesia', 'Madagascar'], 'Its PES scheme began in 1997.'),
            ('Which 2022 agreement set the goal of protecting 30% of land and sea by 2030 ("30 by 30")?', 'The Kunming–Montreal Global Biodiversity Framework', ['The Paris Agreement', 'The Ramsar Convention', 'CITES'], 'It was agreed at COP15.'),
            ('Which Kenyan environmentalist founded the Green Belt Movement and won the 2004 Nobel Peace Prize?', 'Wangari Maathai', ['Kofi Annan', 'Ellen Johnson Sirleaf', 'Malala Yousafzai'], 'The movement has planted tens of millions of trees.'),
            ('Which Indian national park is famous for protecting the greater one-horned rhinoceros?', 'Kaziranga', ['Ranthambore', 'Gir', 'Jim Corbett'], 'It holds about two-thirds of the world\'s population.')],
     why=[('Explain why involving local communities improves conservation.', 'Local people know the land, depend on its resources and can monitor it; if they benefit (jobs, income, rights), they support conservation rather than resisting or ignoring it.'),
          ('Explain why payments for ecosystem services can reduce deforestation.', 'They make standing forest valuable to landowners, giving an income that competes with clearing land for farming.'),
          ('Explain why "fortress conservation" has been criticised.', 'Creating parks by removing Indigenous and local people from their land caused injustice and conflict, and ignored their role in caring for ecosystems.'),
          ('Explain why protecting large connected areas is better than small isolated reserves.', 'Large, linked areas support bigger populations, allow animals to migrate and adapt to climate change, and keep ecological processes working.')],
     contrast=[('conservation', 'preservation', 'Conservation allows sustainable use of resources while protecting them; preservation aims to keep areas untouched with minimal human use.'),
               ('in-situ conservation', 'ex-situ conservation', 'In-situ conservation protects species in their natural habitat (national parks); ex-situ protects them outside it (zoos, seed banks such as the Svalbard Global Seed Vault).')],
     misc=[('Conservation means keeping people out of nature completely.', 'Many successful schemes involve sustainable use and local communities; Indigenous territories often have lower deforestation than surrounding areas.'),
           ('Planting trees anywhere always helps the environment.', 'Planting the wrong species, or trees on natural grasslands, can harm biodiversity and water supplies; restoring native ecosystems is better.'),
           ('Once a species is protected by law, it is safe.', 'Laws must be enforced and habitats protected; poaching, habitat loss and climate change continue to threaten protected species.')],
     cases=[('Costa Rica\'s payments for ecosystem services', 'Since 1997 landowners have been paid to protect or plant forest, funded partly by a fuel tax; forest cover has recovered to over half the country, supporting ecotourism.', 'sustainable ecosystem management', 'paying for the services forests provide made conservation economically worthwhile.'),
            ('the Great Green Wall', 'Launched by the African Union in 2007, it aims to restore 100 million hectares across the Sahel by 2030; progress has been uneven, with Ethiopia and Senegal among the most active.', 'large-scale restoration of degraded land', 'it shows both the ambition and the funding and coordination challenges of restoration.')],
     evaluate=[('National parks are the most effective way to protect ecosystems.', ['strict protection has saved species such as Kaziranga\'s rhinos', 'parks provide refuges and tourism income'], ['parks can exclude local people and suffer from poor enforcement ("paper parks")', 'community conservancies, PES schemes and Indigenous land rights can be as or more effective'], 'Parks are important, but they work best when combined with community involvement and wider sustainable land use outside their borders.')],
     src=[('Nobel lecture (paraphrased)', 'The speaker explained that the movement began by encouraging rural women in Kenya to plant trees to meet their needs for firewood, clean water and food. Over time, she said, they understood that environmental destruction was linked to poor governance and that protecting the environment also meant defending democracy and peace.', 'Paraphrase of Wangari Maathai, Nobel Peace Prize lecture, Oslo, 10 December 2004', 'to explain the Green Belt Movement and link environment, democracy and peace to an international audience', 'It is the founder\'s own account of the movement\'s aims and growth.', 'As a Nobel lecture it presents the movement positively and gives little detail on measured outcomes.', 'Tree planting by women met local needs and grew into a movement for democracy and peace.')],
     rq=[('How effective has Costa Rica\'s payments for ecosystem services programme been in increasing forest cover since 1997?', 'How can we save nature?', 'it is very broad and vague', 'It evaluates a specific conservation strategy with measurable outcomes.', 'Collect forest-cover data (FAO, national); read two studies on PES; consider other factors (cattle prices, tourism); graph change; evaluate sources; cite in APA.')])
C.pct_change(K, 'ch05-st4', [('Costa Rica\'s forest cover', 'per cent of land area', 1987, 21, 2021, 57, 'approx., Costa Rican government'),
                              ('the population of greater one-horned rhinos in Kaziranga', 'rhinos', 1905, 12, 2022, 2613, 'approx., Assam Forest Department')], d=(1, 4))

# =============================================================================================
# ch06 Tourism and Its Impacts
# =============================================================================================
K.st('ch06-st1', 'the growth of global tourism: causes and types of tourism',
     terms=[('mass tourism', 'large numbers of people visiting the same popular destinations, often on package holidays'),
            ('ecotourism', 'responsible travel to natural areas that conserves the environment, sustains the well-being of local people and involves education'),
            ('cultural tourism', 'travel to experience the heritage, arts and way of life of a place'),
            ('package holiday', 'a holiday in which transport, accommodation and often meals are sold together at one price'),
            ('Butler model', 'Richard Butler\'s 1980 tourist area life cycle: exploration, involvement, development, consolidation, stagnation, then decline or rejuvenation'),
            ('dark tourism', 'travel to sites associated with death or tragedy, such as battlefields or memorials')],
     facts=[('About how many international tourist arrivals were there worldwide in 2019?', 'About 1.5 billion', ['About 25 million', 'About 150 million', 'About 15 billion'], 'UN Tourism (UNWTO) recorded about 1.46 billion.'),
            ('About how many international tourist arrivals were there in 1950?', 'About 25 million', ['About 250 million', 'About 1 billion', 'About 2 million'], 'Growth since then has been huge.'),
            ('By roughly how much did international arrivals fall in 2020 because of COVID-19?', 'About 70%', ['About 7%', 'About 30%', '100%'], 'Borders closed worldwide.'),
            ('Which was the world\'s most visited country by international arrivals before the pandemic?', 'France', ['China', 'Brazil', 'Australia'], 'About 90 million arrivals in 2019.'),
            ('Which development of the 1990s greatly increased cheap air travel in Europe?', 'Budget airlines such as Ryanair and easyJet', ['The Channel Tunnel only', 'Concorde', 'Steam trains'], 'Low fares opened travel to many more people.')],
     why=[('Explain why international tourism grew so rapidly after 1950.', 'Rising incomes, paid holidays, jet aircraft and later budget airlines lowered the cost of travel, while package holidays, the internet and more open borders made trips easier to plan and book.'),
          ('Explain why tourism has grown in emerging economies such as China and India.', 'A fast-growing middle class has more disposable income and leisure time, governments have eased travel rules, and many people now travel abroad for the first time.'),
          ('Explain why the Butler model is useful for tourism planners.', 'It suggests that destinations change over time and may stagnate or decline if they become overcrowded or lose appeal, so planners can act early to rejuvenate or manage growth.'),
          ('Explain why ecotourism has become more popular.', 'Growing awareness of environmental issues, interest in wildlife and authentic experiences, and marketing by countries such as Costa Rica have attracted tourists who want responsible travel.')],
     contrast=[('mass tourism', 'ecotourism', 'Mass tourism brings large numbers of visitors to developed resorts and often has big environmental impacts; ecotourism involves small numbers in natural areas and aims to conserve the environment and benefit local people.'),
               ('domestic tourism', 'international tourism', 'Domestic tourism is travel within your own country; international tourism involves crossing a national border.')],
     misc=[('Tourism only means beach holidays.', 'Tourism includes business, cultural, adventure, medical, religious, educational and dark tourism.'),
           ('The number of tourists has grown steadily every year without interruption.', 'Growth has been interrupted by crises such as 9/11 (2001), the 2008–09 financial crisis and especially COVID-19 in 2020.'),
           ('Ecotourism always has no environmental impact.', 'Even ecotourism involves flights and visitors in fragile areas; it must be carefully managed and limited.')],
     cases=[('Benidorm, Spain', 'A fishing village in the 1950s, it became one of Europe\'s first mass-tourism resorts with high-rise hotels; it has since tried to rejuvenate its image.', 'the Butler model', 'it moved from exploration to development and consolidation, then had to rejuvenate to avoid decline.'),
            ('religious tourism to Mecca', 'Millions of Muslims visit Mecca each year for Hajj and Umrah; about 1.8 million performed Hajj in 2024.', 'types of tourism', 'pilgrimage is one of the oldest forms of travel and creates huge flows at specific times.')],
     evaluate=[('Cheap air travel is the main reason for the growth of global tourism.', ['budget airlines and jets made long-distance travel affordable', 'air arrivals dominate international tourism'], ['rising incomes and paid holidays created demand', 'the internet and easier visas made travel simpler'], 'Cheap flights were a major enabling factor, but rising incomes and leisure time created the demand that airlines responded to.')],
     src=[('UN Tourism report (paraphrased)', 'International tourist arrivals reached about 1.46 billion in 2019, the tenth consecutive year of growth. In 2020 arrivals fell by around 72% as travel restrictions spread, returning tourism to levels last seen about 30 years earlier. By 2024 arrivals had almost fully recovered to pre-pandemic levels.', 'Summary of UN Tourism (formerly UNWTO) World Tourism Barometer reports, 2020–2025', 'to provide data on global tourism trends for governments and industry', 'It is the official global source of tourism statistics, based on national data.', 'Data depend on national reporting and include only international arrivals, not domestic tourism.', 'Tourism grew strongly until 2019, collapsed in 2020 and has since recovered.')],
     rq=[('How has the type of tourist visiting Bali changed between 1990 and 2024?', 'Why do people go on holiday?', 'it is a general question without a place or period to investigate', 'It examines change in a real destination using arrivals data, reports and the Butler model.', 'Collect Indonesian statistics on arrivals by origin and purpose; read two case studies; apply the Butler model; compare decades; evaluate sources; cite in APA.')])
C.pct_change(K, 'ch06-st1', [('international tourist arrivals worldwide', 'million', 1950, 25, 2019, 1465, 'UN Tourism'),
                              ('international tourist arrivals worldwide', 'million', 2019, 1465, 2020, 407, 'UN Tourism'),
                              ('outbound trips by Chinese tourists', 'million', 2000, 10.5, 2019, 155, 'China Tourism Academy, approx.')], d=(1, 4))
C.rate_of_change(K, 'ch06-st1', [('international tourist arrivals', 'million', [(1950, 25), (1970, 166), (1990, 435), (2010, 952), (2019, 1465)], 'UN Tourism')])

K.st('ch06-st2', 'the economic, social and environmental impacts of tourism',
     terms=[('multiplier effect', 'the process by which tourist spending creates further rounds of income and jobs in the local economy'),
            ('economic leakage', 'tourist spending that leaves the destination, for example to foreign-owned hotels, airlines and imported goods'),
            ('overtourism', 'when the number of visitors exceeds what a place can manage, harming residents\' quality of life and the environment'),
            ('carrying capacity', 'the maximum number of visitors a place can support without unacceptable damage'),
            ('seasonal employment', 'jobs that are available only during the tourist season'),
            ('commodification of culture', 'turning cultural traditions into products or performances for tourists')],
     facts=[('Roughly what share of global GDP did travel and tourism contribute before the pandemic, according to the WTTC?', 'About 10%', ['About 1%', 'About 30%', 'About 50%'], 'WTTC estimated 10.3% in 2019.'),
            ('Which Thai bay, made famous by the film "The Beach", was closed from 2018 to 2022 to let coral recover?', 'Maya Bay', ['Patong Bay', 'Halong Bay', 'Ao Nang'], 'Up to 5 000 visitors a day had damaged it.'),
            ('Which city began charging day-trippers an entry fee in 2024?', 'Venice', ['Paris', 'Kyoto', 'Barcelona'], 'The fee was €5 on peak days.'),
            ('In some all-inclusive Caribbean resorts, what is a major cause of economic leakage?', 'Foreign ownership and imported food and drink', ['Local farmers selling food', 'Tourists using local buses', 'Locally owned guesthouses'], 'Much spending never reaches the local economy.')],
     why=[('Explain why the multiplier effect can spread the benefits of tourism.', 'Tourists\' spending pays hotel and restaurant workers, who spend their wages locally; businesses buy from local farmers and suppliers, so income circulates and creates further jobs.'),
          ('Explain why economic leakage reduces the benefits of tourism to low-income countries.', 'When hotels, tour operators and airlines are foreign-owned and food and equipment are imported, much of the money tourists spend flows out of the country.'),
          ('Explain why overtourism causes conflict with residents.', 'Crowds, noise, rising rents (as homes become short-term rentals) and high prices make cities like Barcelona and Venice harder to live in, while residents may see few benefits.'),
          ('Explain why tourism can damage coral reefs.', 'Divers and snorkellers touch and break coral, boats anchor on reefs, sunscreen chemicals and sewage pollute the water, and hotel construction increases sediment.')],
     contrast=[('a positive economic impact of tourism', 'a negative economic impact of tourism', 'A positive impact is job creation and foreign currency earnings; a negative impact is leakage, seasonal low-paid jobs or over-dependence on one industry.'),
               ('the multiplier effect', 'economic leakage', 'The multiplier effect keeps tourist money circulating in the local economy; leakage is money that leaves it.')],
     misc=[('Tourism always brings large economic benefits to local people.', 'Benefits depend on who owns businesses and where supplies come from; with high leakage, local people may gain little.'),
           ('Tourism only has negative effects on culture.', 'Tourism can also revive traditional crafts, festivals and languages, and fund heritage protection.'),
           ('Environmental damage from tourism happens only at the destination.', 'Flights to destinations add significantly to greenhouse gas emissions.')],
     cases=[('the Maldives', 'Tourism contributes around a quarter of GDP and most foreign earnings; resorts are on separate islands, but rising seas threaten the low-lying country.', 'dependence on tourism', 'a country can gain greatly from tourism but become vulnerable to shocks such as COVID-19 and climate change.'),
            ('overtourism in Barcelona', 'Visitor numbers grew rapidly after the 1992 Olympics; residents protested about rents and crowding, and the city restricted new hotels and short-term rentals.', 'social impacts of tourism', 'tourism growth can reduce residents\' quality of life and provoke political responses.')],
     evaluate=[('The benefits of tourism outweigh its costs for host communities.', ['it creates jobs, foreign exchange and funds for conservation and heritage', 'it can support infrastructure such as airports and roads'], ['leakage, seasonal jobs and rising costs limit local benefits', 'environmental damage and overtourism harm residents'], 'It depends on management: when local people own businesses and visitor numbers are controlled, benefits usually outweigh costs; unmanaged mass tourism can reverse this.')],
     src=[('Newspaper report (paraphrased)', 'Thousands of residents marched through central Barcelona, some spraying tourists with water pistols, to protest against mass tourism. They argued that short-term rentals had pushed up rents and that the city\'s economy depended too much on visitors. The mayor announced plans to end licences for tourist apartments by 2028.', 'Paraphrase of international news reports on protests in Barcelona, July 2024', 'to inform readers about a newsworthy protest and the city\'s response', 'It shows residents\' perspective and the political response to overtourism.', 'News reports focus on dramatic actions and may not represent the views of residents who work in tourism.', 'Residents protested that tourism raised rents and harmed the city, leading to new restrictions.')],
     rq=[('How much of the money spent by tourists in Zanzibar stays in the local economy?', 'Is tourism good?', 'it is a closed value question without criteria or a place', 'It investigates economic leakage, a key concept, in a specific destination.', 'Find reports on tourism leakage in Zanzibar (World Bank, NGOs); interview a local tour operator by video call or email; categorise spending; calculate retained %; evaluate data limits; cite in APA.')])


@R.add('ch06-st2', ('C3', 'C4'), (1, 5), 'numerical')
def leakage(rng, slot):
    place = rng.choice(['a resort in Jamaica', 'a lodge in Kenya', 'a beach hotel in Bali', 'an all-inclusive resort in the Dominican Republic', 'an eco-lodge in Costa Rica', 'a hotel in Goa'])
    spend = rng.choice([800, 1200, 1500, 2000, 2500, 3200])
    leak = rng.choice([20, 35, 45, 55, 60, 70, 80])
    kept = spend * (100 - leak) / 100
    if slot.d <= 2:
        return dict(stem=f'A tourist spends US$ {spend:,} on a holiday at {place}. If {leak}% of this leaks out of the local economy, how much stays in the destination?',
                    answer=f'US$ {kept:,.0f}', type='numerical', marks=2,
                    markingKey=f'{100 - leak}% of {spend:,} = {kept:,.0f} (M1 A1).', gap='G3')
    n = rng.choice([500, 1200, 5000, 20000])
    k2 = rng.choice([x for x in [15, 25, 30, 40] if x < leak])
    gain = spend * n * (leak - k2) / 100
    return dict(stem=(f'{n:,} tourists each spend US$ {spend:,} at {place}, where leakage is {leak}%. A new policy to buy food from local farmers and employ local managers would cut leakage to {k2}%. '
                      'Calculate the extra money that would stay in the local economy, and explain one reason why reducing leakage helps development.'),
                answer=f'US$ {gain:,.0f} more retained', type='multi_step', marks=4,
                markingKey=f'Total spending {n:,} × {spend:,} = US$ {n * spend:,} (M1); retained before {100 - leak}%, after {100 - k2}% (M1); difference {leak - k2}% = US$ {gain:,.0f} (A1). '
                           'Reason (R1): more local income creates a stronger multiplier effect – wages and purchases circulate locally, supporting jobs and services.', gap='G5')


K.st('ch06-st3', 'sustainable tourism and ecotourism',
     terms=[('sustainable tourism', 'tourism that takes full account of its current and future economic, social and environmental impacts, meeting the needs of visitors, industry, the environment and host communities'),
            ('ecotourism', 'responsible travel to natural areas that conserves the environment, sustains the well-being of local people and involves interpretation and education'),
            ('community-based tourism', 'tourism owned and managed by local communities, so they control it and keep the benefits'),
            ('visitor management', 'controlling where, when and how many visitors go to a site, through quotas, fees, permits or zoning'),
            ('"high value, low volume"', 'Bhutan\'s tourism policy of attracting fewer, higher-spending visitors to limit impacts')],
     facts=[('Which country charges visitors a Sustainable Development Fee as part of its "high value, low volume" tourism policy?', 'Bhutan', ['Thailand', 'Spain', 'Mexico'], 'The fee funds conservation and public services.'),
            ('In 2024 the Galápagos National Park entry fee for most foreign adult visitors was raised to what?', 'US$ 200', ['US$ 2', 'US$ 20', 'US$ 2 000'], 'It had been US$ 100 since 1998.'),
            ('Which Kenyan model allows Maasai landowners to earn income from wildlife tourism on their land?', 'Community conservancies', ['National parks only', 'Cattle ranching', 'Mining licences'], 'Conservancies around the Maasai Mara lease land to tourism operators.'),
            ('Which organisation defined ecotourism as responsible travel that conserves the environment and sustains local well-being?', 'The International Ecotourism Society', ['FIFA', 'OPEC', 'NATO'], 'TIES updated the definition in 2015.')],
     why=[('Explain why visitor limits can make tourism more sustainable.', 'They keep numbers within the carrying capacity, reducing erosion, crowding and disturbance to wildlife, while maintaining the quality of experience that attracts tourists.'),
          ('Explain why community-based tourism can benefit local people more than mass tourism.', 'Local people own and run the accommodation and activities, so they keep profits, decide how tourism develops and can protect their culture.'),
          ('Explain why Bhutan charges a daily fee to tourists.', 'It limits visitor numbers, raises money for health, education and conservation and avoids the environmental and cultural damage of mass tourism.'),
          ('Explain why ecotourism can still harm the environment.', 'Long-haul flights add to emissions, popular ecotourism areas can become crowded, and building lodges and roads in fragile areas causes damage.')],
     contrast=[('ecotourism', 'sustainable tourism', 'Ecotourism is a type of nature-based tourism with conservation and education goals; sustainable tourism is a wider principle that any type of tourism, including city or beach tourism, can follow.'),
               ('a visitor quota', 'an entry fee', 'A quota directly limits the number of visitors; an entry fee reduces numbers indirectly by raising cost, while also raising revenue.')],
     misc=[('Any holiday labelled "eco" is sustainable.', 'Some businesses use "greenwashing"; certification and evidence of conservation and local benefits are needed.'),
           ('Sustainable tourism means fewer jobs.', 'Well-managed sustainable tourism can create long-lasting local jobs, often higher-value ones, as in Costa Rica.'),
           ('Higher fees always reduce local benefits.', 'Fees can fund conservation and local services if revenue is shared with communities.')],
     cases=[('Costa Rica\'s ecotourism', 'With about a quarter of its land protected, Costa Rica attracts millions of nature tourists; certification (CST) rewards sustainable businesses.', 'ecotourism supporting conservation', 'protected forests became an economic asset through tourism.'),
            ('Bhutan\'s tourism policy', 'Bhutan charges a daily Sustainable Development Fee and requires most visitors to use licensed guides, limiting numbers.', '"high value, low volume" tourism', 'a small country controls tourism to protect culture and environment while earning revenue.')],
     evaluate=[('Ecotourism is the best way to protect fragile environments.', ['it gives economic value to conservation and funds parks', 'it involves and benefits local communities'], ['flights and visitors still cause impacts and can grow into mass tourism', 'income depends on tourist numbers, which can collapse in crises'], 'Ecotourism can help protect environments if strictly managed and combined with other conservation funding, but it is not a complete solution.')],
     src=[('Government policy statement (paraphrased)', 'The government announced that the daily Sustainable Development Fee would fund projects that preserve the country\'s culture and environment and improve infrastructure. The aim was to attract visitors who valued the country\'s heritage, rather than large numbers of low-spending tourists.', 'Paraphrase of statements by the Tourism Council of Bhutan on the reopening of tourism, 2022', 'to explain and justify a new tourism policy to visitors and the public', 'It states the official aims of the policy clearly.', 'It is a government statement and does not show the impacts on local businesses, some of which reported falling visitor numbers.', 'The fee funds culture and environment and aims at fewer, higher-value visitors.')],
     rq=[('How effective are community conservancies in the Maasai Mara at sharing tourism income with Maasai landowners?', 'What is ecotourism?', 'it is a definition question', 'It evaluates sustainable tourism with a focus on fairness and conservation.', 'Read conservancy reports and two academic studies; compare lease payments and wildlife data; find landowners\' views in interviews or reports; evaluate perspectives; cite in APA.')])
C.pct_change(K, 'ch06-st3', [('the number of visitors to the Galápagos Islands', 'visitors', 1990, 41000, 2023, 330000, 'approx., Galápagos National Park')], d=(1, 3))

# =============================================================================================
# ch07 Markets, Demand and Supply
# =============================================================================================
K.st('ch07-st1', 'demand and supply and the factors that determine them',
     terms=[('demand', 'the quantity of a good or service that consumers are willing and able to buy at each price over a period of time'),
            ('supply', 'the quantity of a good or service that producers are willing and able to sell at each price over a period of time'),
            ('law of demand', 'as the price of a good rises, the quantity demanded falls, other things being equal (ceteris paribus)'),
            ('law of supply', 'as the price of a good rises, the quantity supplied rises, other things being equal'),
            ('substitute', 'a good that can be used in place of another, such as tea and coffee'),
            ('complement', 'a good that is used together with another, such as printers and ink cartridges'),
            ('ceteris paribus', 'Latin for "other things being equal": assuming that only one factor changes at a time')],
     facts=[('What happens to the demand curve for a normal good when consumers\' incomes rise?', 'It shifts to the right', ['It shifts to the left', 'There is a movement along it', 'It becomes vertical'], 'More is demanded at every price.'),
            ('A fall in the price of a good itself causes which of the following?', 'A movement along the demand curve (extension of demand)', ['A rightward shift of the demand curve', 'A leftward shift of the supply curve', 'A shift of both curves'], 'Only non-price factors shift the curve.'),
            ('If the price of coffee rises, what is likely to happen to the demand for tea?', 'It increases, because tea is a substitute', ['It falls, because tea is a complement', 'It does not change', 'The supply of tea falls'], 'Consumers switch to the substitute.'),
            ('Which of these would shift the supply curve of wheat to the left?', 'A severe drought', ['A fall in fertiliser prices', 'A new high-yield seed variety', 'A government subsidy to farmers'], 'Bad weather reduces output at every price.'),
            ('Which of these is a determinant of supply rather than demand?', 'The cost of raw materials', ['Consumer tastes', 'The price of substitutes', 'Consumer income'], 'Costs of production affect how much firms are willing to supply.')],
     why=[('Explain why demand curves usually slope downwards.', 'At lower prices consumers can afford more (income effect) and the good becomes cheaper relative to substitutes (substitution effect), so quantity demanded rises.'),
          ('Explain why supply curves usually slope upwards.', 'Higher prices make production more profitable, so existing firms produce more and new firms are attracted into the market.'),
          ('Explain why an advertising campaign shifts the demand curve rather than causing a movement along it.', 'Advertising changes consumer tastes, a non-price factor, so more is demanded at every price; a movement along the curve happens only when the good\'s own price changes.'),
          ('Explain why new technology usually shifts supply to the right.', 'Technology lowers the cost of producing each unit, so firms can supply more at every price.')],
     contrast=[('a movement along the demand curve', 'a shift of the demand curve', 'A movement is caused by a change in the good\'s own price; a shift is caused by a change in a non-price factor such as income, tastes or the price of related goods.'),
               ('a substitute good', 'a complementary good', 'A rise in the price of a substitute increases demand for the other good; a rise in the price of a complement reduces demand for the other good.')],
     misc=[('An increase in price causes demand to fall.', 'A price rise causes a fall in quantity demanded (a movement along the curve); demand itself (the curve) shifts only when non-price factors change.'),
           ('Supply means the amount of a good that exists.', 'Supply is the amount producers are willing and able to sell at each price over a period, not the total stock.'),
           ('If incomes rise, demand for every good rises.', 'Demand for inferior goods, such as some cheap staple foods or bus travel, may fall as people switch to better alternatives.')],
     cases=[('avocado demand in Europe and North America', 'Health trends and social media made avocados fashionable in the 2010s; imports from Mexico and Peru grew rapidly.', 'a change in tastes shifting demand', 'a non-price factor shifted demand to the right, raising prices and output.'),
            ('Brazil\'s coffee frost of 2021', 'Frosts in Minas Gerais damaged coffee trees in July 2021, cutting future harvests; arabica prices rose to their highest level in about ten years.', 'a supply shock', 'bad weather shifted supply to the left, raising world prices.')],
     evaluate=[('Consumer income is the most important factor determining demand.', ['income sets what people are able to buy', 'rising incomes in Asia transformed demand for cars and meat'], ['tastes, the price of substitutes and population size also matter', 'for necessities, demand changes little with income'], 'Income is a key factor, but its importance depends on the good; for fashion goods tastes may dominate and for necessities price and population matter more.')],
     src=[('Market report (paraphrased)', 'The report stated that cocoa prices had more than tripled in a year because poor weather and plant disease in Côte d\'Ivoire and Ghana, which grow over half the world\'s cocoa, had reduced harvests. Chocolate makers said they would raise prices or reduce bar sizes.', 'Paraphrase of reports by the International Cocoa Organization and financial news, 2024', 'to inform traders, businesses and the public about market conditions', 'It explains a real supply shock with expert data on production.', 'It focuses on producers and businesses and says little about the effect on cocoa farmers\' incomes.', 'Bad weather and disease reduced the cocoa supply, raising prices sharply.')],
     rq=[('How did the price of cocoa change between 2022 and 2024, and what supply factors explain the change?', 'Why are things expensive?', 'it is far too broad and has no focus', 'It links demand and supply theory to a real commodity market.', 'Collect ICCO price data; read reports on weather and disease in West Africa; draw supply-and-demand diagrams; compare factors; evaluate sources; cite in APA.')])
C.supply_demand(K, 'ch07-st1', c=('C3',), d=(1, 4))
C.pct_change(K, 'ch07-st1', [('the world price of cocoa', 'US$ per tonne', 2022, 2400, 2024, 8000, 'approx., ICCO'),
                              ('avocado imports into the European Union', 'thousand tonnes', 2012, 330, 2022, 760, 'approx., Eurostat')], d=(1, 3))


K.st('ch07-st2', 'price determination: equilibrium, shortages and surpluses',
     terms=[('equilibrium price', 'the price at which quantity demanded equals quantity supplied, so the market clears'),
            ('equilibrium quantity', 'the quantity bought and sold at the equilibrium price'),
            ('excess demand (shortage)', 'when quantity demanded is greater than quantity supplied at the current price'),
            ('excess supply (surplus)', 'when quantity supplied is greater than quantity demanded at the current price'),
            ('price mechanism', 'the way changes in prices signal and ration resources, bringing markets towards equilibrium'),
            ('market', 'any arrangement that allows buyers and sellers to exchange goods, services or resources')],
     facts=[('At a price above the equilibrium, what exists in the market?', 'A surplus (excess supply)', ['A shortage', 'Equilibrium', 'Zero supply'], 'Producers want to sell more than consumers want to buy.'),
            ('If demand increases and supply stays the same, what happens to the equilibrium price and quantity?', 'Both rise', ['Both fall', 'Price rises, quantity falls', 'Price falls, quantity rises'], 'Demand shifts right along the supply curve.'),
            ('If supply increases and demand stays the same, what happens?', 'Price falls and quantity rises', ['Price rises and quantity falls', 'Both rise', 'Both fall'], 'Supply shifts right along the demand curve.'),
            ('Who described the "invisible hand" that guides markets?', 'Adam Smith', ['Karl Marx', 'John Maynard Keynes', 'Amartya Sen'], 'In The Wealth of Nations, 1776.'),
            ('What usually happens to price when there is a shortage?', 'It rises', ['It falls', 'It stays the same', 'It becomes zero'], 'Buyers compete for limited goods.')],
     why=[('Explain why a surplus causes the price to fall.', 'Sellers have unsold stock, so they cut prices to attract buyers; as price falls quantity demanded rises and quantity supplied falls until the surplus disappears.'),
          ('Explain why a shortage causes the price to rise.', 'Buyers who cannot get the good are willing to pay more, and sellers realise they can raise prices; this reduces quantity demanded and increases quantity supplied until equilibrium is reached.'),
          ('Explain how the price mechanism rations scarce goods.', 'When a good is scarce, its price rises, so only those willing and able to pay buy it, while the higher price encourages producers to supply more.'),
          ('Explain why concert tickets are often resold above face value.', 'Tickets are priced below equilibrium, creating excess demand; resellers buy them and sell at the higher price fans are willing to pay.')],
     contrast=[('a shortage', 'a surplus', 'A shortage occurs when price is below equilibrium and demand exceeds supply; a surplus occurs when price is above equilibrium and supply exceeds demand.'),
               ('the equilibrium price', 'the market price', 'The equilibrium price is where demand equals supply; the market price is the price actually charged at a given moment, which may be above or below equilibrium.')],
     misc=[('Equilibrium price is the price that is fair to everyone.', 'Equilibrium is where quantity demanded equals quantity supplied; it is not a judgement about fairness, and some people may be unable to afford it.'),
           ('Once a market reaches equilibrium it stays there forever.', 'Equilibrium changes whenever demand or supply shift, for example after a harvest failure or a change in tastes.'),
           ('A shortage means there are no goods at all.', 'A shortage means quantity demanded exceeds quantity supplied at the current price; some goods are still sold.')],
     cases=[('the 2020–21 semiconductor shortage', 'Demand for electronics rose during the COVID-19 lockdowns while factories closed; carmakers could not get chips and prices of new and used cars rose.', 'excess demand and rising prices', 'demand outstripped supply, and the price mechanism raised prices.'),
            ('the European "butter mountain"', 'In the 1980s guaranteed high prices under the EU\'s Common Agricultural Policy led farmers to produce far more butter, milk and wine than consumers bought.', 'a surplus caused by a price set above equilibrium', 'supply exceeded demand at the guaranteed price, creating stockpiles.')],
     evaluate=[('The price mechanism is the best way to allocate scarce resources.', ['prices signal scarcity and encourage efficient production', 'markets respond quickly without central planning'], ['people on low incomes may be unable to afford necessities', 'markets may fail to account for external costs such as pollution'], 'The price mechanism is efficient for most goods, but governments may need to intervene for necessities and when markets fail.')],
     src=[('Economics text (paraphrased)', 'The author argued that individuals pursuing their own interest are often led, as if by an invisible hand, to promote the interests of society more effectively than if they intended to do so. A butcher or baker, he wrote, provides our dinner not out of kindness but out of regard for their own interest.', 'Paraphrase of Adam Smith, An Inquiry into the Nature and Causes of the Wealth of Nations, London, 1776', 'to argue for free markets against heavy government regulation of trade', 'It is a founding text of economics and shows how prices coordinate decisions.', 'It was written in the 18th century before large corporations and modern environmental problems; Smith also warned about monopolies.', 'Self-interest in markets can benefit society through the invisible hand.')],
     rq=[('How did shortages of semiconductors affect new car prices in the United States between 2020 and 2022?', 'What is a market?', 'it is a definition question', 'It applies equilibrium analysis to a recent, data-rich market shock.', 'Collect price data (US Bureau of Labor Statistics); read two industry reports; draw demand and supply diagrams; consider other factors; evaluate sources; cite in APA.')])
C.supply_demand(K, 'ch07-st2', c=('C3', 'C4'), d=(1, 5))


@R.add('ch07-st2', 'C3', (1, 4), 'mcq')
def short_surplus(rng, slot):
    a = rng.choice([80, 100, 120, 150, 200]); b = rng.choice([2, 4, 5])
    c = rng.choice([10, 20]); e = rng.choice([2, 3, 4])
    p_eq = (a - c) / (b + e)
    if p_eq != int(p_eq) or p_eq <= 2:
        return None
    p_eq = int(p_eq)
    good = rng.choice(['mangoes in a Mumbai market', 'bus passes in Nairobi', 'bags of rice in Dhaka', 'concert tickets in Seoul', 'bicycles in Amsterdam', 'notebooks in Lima'])
    p = p_eq + rng.choice([-2, -1, 1, 2]) * rng.choice([1, 2])
    if p <= 0:
        return None
    qd, qs = a - b * p, c + e * p
    if qd <= 0:
        return None
    if qd > qs:
        correct = f'A shortage of {qd - qs} units'; wr = [f'A surplus of {qd - qs} units', 'Equilibrium', f'A shortage of {qd + qs} units']
    else:
        correct = f'A surplus of {qs - qd} units'; wr = [f'A shortage of {qs - qd} units', 'Equilibrium', f'A surplus of {qd + qs} units']
    return C.mcq(rng, f'For {good}, Qd = {a} − {b}P and Qs = {c} + {e}P. What exists at a price of {p}?', correct, wr,
                 f'Qd = {qd}, Qs = {qs}; equilibrium price is {p_eq}.')


K.st('ch07-st3', 'government intervention in markets through price controls, taxes and subsidies',
     terms=[('maximum price (price ceiling)', 'a legal upper limit on the price of a good, set below equilibrium to help consumers'),
            ('minimum price (price floor)', 'a legal lower limit on price, set above equilibrium to help producers or workers, such as a minimum wage'),
            ('indirect tax', 'a tax on spending on goods and services, such as VAT or an excise duty on tobacco'),
            ('subsidy', 'a payment by the government to producers to lower their costs and increase supply'),
            ('minimum support price', 'in India, a price at which the government buys crops such as wheat and rice from farmers'),
            ('rationing', 'distributing a limited supply of goods by quotas, queues or coupons rather than by price')],
     facts=[('What is the likely result of setting a maximum price below the equilibrium price?', 'A shortage', ['A surplus', 'No effect', 'A fall in demand'], 'Quantity demanded rises while quantity supplied falls.'),
            ('Which type of indirect tax is often placed on tobacco, alcohol and sugary drinks?', 'An excise duty', ['An income tax', 'A corporation tax', 'An inheritance tax'], 'These are demerit goods.'),
            ('How does a subsidy affect the supply curve?', 'It shifts supply to the right', ['It shifts supply to the left', 'It shifts demand to the left', 'It has no effect'], 'Producers\' costs fall.'),
            ('Which country introduced a soft drinks industry levy in 2018 that led many firms to cut sugar content?', 'The United Kingdom', ['Brazil', 'Japan', 'Nigeria'], 'Average sugar in taxed drinks fell sharply.'),
            ('A national minimum wage is an example of what?', 'A minimum price in the labour market', ['A maximum price', 'A subsidy', 'An indirect tax'], 'It sets a floor on the price of labour.')],
     why=[('Explain why rent controls can lead to a shortage of housing.', 'A maximum rent below equilibrium increases the number of people wanting to rent while reducing the incentive for landlords to supply or maintain homes, so demand exceeds supply.'),
          ('Explain why governments tax goods such as cigarettes.', 'The tax raises the price, reducing consumption of a harmful good, and raises revenue that can fund healthcare.'),
          ('Explain why a minimum price for crops can create a surplus.', 'At a guaranteed price above equilibrium, farmers produce more while consumers buy less, so the government must buy and store the excess, as happened with grain stocks in India.'),
          ('Explain why a subsidy on solar panels can increase their use.', 'The subsidy lowers producers\' costs, shifting supply right, so the price falls and more households and businesses buy solar panels.')],
     contrast=[('a maximum price', 'a minimum price', 'A maximum price is set below equilibrium to protect consumers and tends to cause shortages; a minimum price is set above equilibrium to protect producers and tends to cause surpluses.'),
               ('an indirect tax', 'a subsidy', 'An indirect tax raises costs and shifts supply left, raising price; a subsidy lowers costs and shifts supply right, lowering price.')],
     misc=[('The producer pays all of an indirect tax.', 'The tax burden is shared; consumers usually pay part through higher prices, depending on how responsive demand is.'),
           ('Price controls always help the people they are meant to help.', 'They can backfire: rent controls may reduce housing supply and some tenants cannot find homes; minimum prices can create waste.'),
           ('Subsidies are free for society.', 'Subsidies are paid from taxes or borrowing, so they have an opportunity cost.')],
     cases=[('India\'s minimum support price and food stocks', 'The Food Corporation of India buys wheat and rice at minimum support prices; by the 2010s stocks often far exceeded storage needs, with some grain spoiling.', 'a minimum price creating a surplus', 'a guaranteed price above market levels encouraged excess output that the state had to store.'),
            ('Venezuela\'s price controls', 'From 2003 the government set maximum prices for basic foods; by the mid-2010s shops faced severe shortages and long queues.', 'a maximum price creating a shortage', 'prices below equilibrium reduced supply and increased demand, leading to empty shelves.')],
     evaluate=[('Taxes on sugary drinks are an effective way to reduce obesity.', ['taxes raise prices and in the UK led firms to cut sugar content', 'revenue can fund school sport and health programmes'], ['consumers may switch to other unhealthy foods', 'the tax falls more heavily on low-income households'], 'Sugar taxes help reduce sugar intake, especially through reformulation, but they work best as part of a wider strategy including education and regulation.')],
     src=[('Government evaluation (paraphrased)', 'The report found that the soft drinks levy, introduced in April 2018, had led manufacturers to reduce the sugar content of many drinks before the levy started. The total sugar sold in soft drinks fell by about a third between 2015 and 2019, while sales volumes of soft drinks increased.', 'Paraphrase of Public Health England, Sugar reduction: report on progress, 2020', 'to evaluate a government policy and inform future health policy', 'It uses large-scale sales data and is produced by a public health agency.', 'As a government report it may emphasise success; it measures sugar sold rather than direct health outcomes.', 'The levy led firms to cut sugar, and sugar sold in drinks fell.')],
     rq=[('To what extent did the UK soft drinks industry levy reduce sugar consumption between 2016 and 2022?', 'Are taxes good?', 'it is a vague value question', 'It evaluates a real tax policy using measurable data.', 'Use Public Health England data and two academic studies; compare sugar per 100 ml before and after; consider other influences; evaluate sources; cite in APA.')])
C.tax_subsidy(K, 'ch07-st3')


@R.add('ch07-st3', ('C3', 'C4'), (2, 5), 'numerical')
def price_control(rng, slot):
    a = rng.choice([200, 240, 300, 360]); b = rng.choice([2, 3, 4]); c = rng.choice([0, 20, 30]); e = rng.choice([2, 3, 4])
    if (a - c) % (b + e):
        return None
    pe_ = (a - c) // (b + e); qe = a - b * pe_
    kind = rng.choice(['max', 'min'])
    good, unit = rng.choice([('rented flats in Berlin', 'flats'), ('bread in Cairo', 'thousand loaves'), ('wheat in Punjab', 'thousand tonnes'),
                             ('petrol in Lagos', 'million litres'), ('milk in the European Union', 'million litres'), ('rice in Manila', 'thousand tonnes')])
    gap = rng.choice([4, 6, 8, 10])
    if kind == 'max':
        p = pe_ - gap
        if p <= 0:
            return None
        qd, qs = a - b * p, c + e * p
        res = f'shortage of {qd - qs} {unit}'
        lab = 'maximum price'
    else:
        p = pe_ + gap
        qd, qs = a - b * p, c + e * p
        if qd <= 0:
            return None
        res = f'surplus of {qs - qd} {unit}'
        lab = 'minimum price'
    return dict(stem=(f'In the market for {good}, demand is Qd = {a} − {b}P and supply is Qs = {c} + {e}P (Q in {unit}). The government sets a {lab} of {p}. '
                      f'Calculate the equilibrium price and quantity, then the quantity demanded and supplied at the {lab}, and state the result.'),
                answer=f'Equilibrium P = {pe_}, Q = {qe}; at P = {p}: Qd = {qd}, Qs = {qs}: {res}.', type='multi_step', marks=5,
                markingKey=(f'Set {a} − {b}P = {c} + {e}P → P = {pe_} (M1 A1), Q = {qe} (A1). At {p}: Qd = {qd}, Qs = {qs} (M1); {res} (A1). '
                            + (' Accept a comment that queues or black markets may follow.' if kind == 'max' else ' Accept a comment that the government may have to buy the surplus.')),
                gap='G3')

# =============================================================================================
# ch08 Rights and Democracy
# =============================================================================================
K.st('ch08-st1', 'the struggle for the vote: the suffragette movement and universal adult franchise',
     terms=[('suffrage', 'the right to vote in public elections'),
            ('suffragist', 'a campaigner for votes for women who used peaceful, legal methods such as petitions and meetings, like Millicent Fawcett\'s NUWSS'),
            ('suffragette', 'a member of the Women\'s Social and Political Union (WSPU), founded by Emmeline Pankhurst in 1903, which used militant direct action'),
            ('universal adult franchise', 'the right of all adult citizens to vote regardless of sex, wealth, race, religion or education'),
            ('franchise', 'the right to vote, or the group of people who have that right'),
            ('Cat and Mouse Act', 'the 1913 UK law that released hunger-striking suffragettes when ill and re-arrested them when they recovered')],
     facts=[('Which was the first self-governing country to give all adult women the vote in national elections?', 'New Zealand, in 1893', ['Britain, in 1918', 'the United States, in 1920', 'France, in 1944'], 'Kate Sheppard led the campaign.'),
            ('Who founded the Women\'s Social and Political Union in 1903?', 'Emmeline Pankhurst', ['Millicent Fawcett', 'Kate Sheppard', 'Susan B. Anthony'], 'Its motto was "Deeds, not words".'),
            ('Which 1918 UK Act gave the vote to most women over 30?', 'The Representation of the People Act', ['The Great Reform Act', 'The Equal Franchise Act', 'The Cat and Mouse Act'], 'Equal voting at 21 came in 1928.'),
            ('Which amendment to the US Constitution, ratified in 1920, prohibited denying the vote on the basis of sex?', 'The 19th Amendment', ['The 13th Amendment', 'The 15th Amendment', 'The 1st Amendment'], 'Many Black women were still excluded in practice in the South until the 1965 Voting Rights Act.'),
            ('In which year did Swiss women gain the right to vote in federal elections?', '1971', ['1893', '1918', '1945'], 'One canton held out until 1990.')],
     why=[('Explain why the suffragettes turned to militant methods.', 'Decades of peaceful petitions had not persuaded Parliament, so the WSPU used direct action such as window smashing and hunger strikes to gain publicity and force the issue onto the political agenda.'),
          ('Explain why the First World War helped women gain the vote in Britain.', 'Women\'s war work in munitions, transport and nursing showed their contribution to the nation, the suffrage campaigns were paused, and the government needed to reform the franchise anyway for returning soldiers.'),
          ('Explain why universal adult franchise is seen as essential to democracy.', 'If all adults can vote, governments must answer to the whole population, not just a privileged group, and each citizen has an equal political voice.'),
          ('Explain why some women still could not vote after formal laws granted suffrage.', 'Property qualifications, literacy tests, poll taxes and racial discrimination, as in the US South, excluded many women in practice.')],
     contrast=[('suffragists', 'suffragettes', 'Suffragists (NUWSS, led by Millicent Fawcett) used peaceful, constitutional methods; suffragettes (WSPU, led by Emmeline Pankhurst) used militant direct action.'),
               ('the 1918 Representation of the People Act', 'the 1928 Equal Franchise Act', 'The 1918 Act gave the vote to women over 30 who met a property qualification and to almost all men over 21; the 1928 Act gave women the vote on equal terms with men at 21.')],
     misc=[('All women in Britain gained the vote in 1918.', 'Only women over 30 who met property qualifications (about 8.4 million) gained it in 1918; equal suffrage at 21 came in 1928.'),
           ('The suffragettes alone won women the vote.', 'Peaceful suffragist campaigning, women\'s war work and political changes after the First World War were also important.'),
           ('Universal suffrage was achieved in most countries by 1900.', 'Only New Zealand had national women\'s suffrage by 1900; many countries gave women the vote after 1945, and some much later.')],
     cases=[('Emily Wilding Davison at the 1913 Derby', 'Davison ran onto the course at Epsom and was struck by the King\'s horse; she died four days later, and her funeral drew large crowds.', 'militant suffragette tactics', 'her death brought huge publicity but historians still debate whether it was a protest or an accident.'),
            ('Kate Sheppard\'s petitions in New Zealand', 'In 1893 a petition with nearly 32,000 signatures, almost a quarter of adult women, was presented to Parliament; the Electoral Act passed later that year.', 'peaceful mass campaigning', 'a well-organised petition campaign achieved the world\'s first national women\'s suffrage.')],
     evaluate=[('Militant tactics were the main reason women gained the vote in Britain.', ['WSPU actions kept the issue in the news', 'the government could not ignore hunger strikes and protests'], ['militancy alienated some MPs and the public', 'the NUWSS had a larger membership, and war work and franchise reform in 1918 were decisive'], 'Militancy raised awareness, but peaceful campaigning and the impact of the First World War were probably more important in securing the 1918 Act.')],
     src=[('Speech (paraphrased)', 'The speaker told an American audience that she was a soldier in a civil war for women\'s rights. She argued that women had tried peaceful methods for decades without success and that only by making the situation impossible for the government would they win the vote.', 'Paraphrase of Emmeline Pankhurst, "Freedom or Death" speech, Hartford, Connecticut, 13 November 1913', 'to justify militant tactics and raise support and funds in the United States', 'It shows the WSPU leader\'s own reasoning for militancy.', 'It is a persuasive speech for fundraising and presents only the militant perspective.', 'Pankhurst argued militancy was necessary because peaceful methods had failed.')],
     rq=[('How significant was women\'s war work in the passing of the 1918 Representation of the People Act?', 'Did women get the vote?', 'it is a closed question with a simple answer', 'It weighs causes of a key change in democratic rights.', 'Read parliamentary debates (Hansard) and two historians; compare roles of war work, campaigns and politics; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch08-st1', events=[('New Zealand gives women the vote', 1893), ('the WSPU is founded', 1903), ('the Cat and Mouse Act is passed', 1913),
                                     ('women over 30 gain the vote in Britain', 1918), ('the 19th Amendment is ratified in the USA', 1920), ('the Equal Franchise Act gives UK women votes at 21', 1928),
                                     ('women vote in France for the first time', 1945), ('India holds its first general election with universal adult franchise', 1951),
                                     ('the US Voting Rights Act is passed', 1965), ('Swiss women gain the federal vote', 1971)])
C.pct_change(K, 'ch08-st1', [('the UK electorate', 'million voters', 1910, 7.7, 1918, 21.4, 'approx., UK Parliament'),
                              ('the UK electorate', 'million voters', 1918, 21.4, 1929, 28.9, 'approx., UK Parliament')], d=(1, 3))


K.st('ch08-st2', 'electoral systems and representation: first past the post and proportional representation',
     terms=[('first past the post (FPTP)', 'an electoral system in which the candidate with the most votes in each constituency wins, even without a majority'),
            ('proportional representation (PR)', 'a system in which parties win seats in proportion to their share of the vote'),
            ('constituency', 'a geographical area that elects a representative'),
            ('party list', 'a PR system in which voters choose a party and seats are filled from the party\'s ranked list of candidates'),
            ('mixed-member proportional (MMP)', 'a system combining constituency seats and list seats to make the overall result proportional, used in Germany and New Zealand'),
            ('safe seat', 'a constituency where one party has such a large majority that it is very unlikely to lose')],
     facts=[('In the 2024 UK general election, Labour won about 63% of seats with roughly what share of the vote?', 'About 34%', ['About 63%', 'About 51%', 'About 20%'], 'It won 411 of 650 seats with 33.7% of the vote.'),
            ('Which country switched from FPTP to MMP after a 1993 referendum?', 'New Zealand', ['Canada', 'India', 'the United Kingdom'], 'The first MMP election was in 1996.'),
            ('Which electoral system is used for elections to India\'s Lok Sabha?', 'First past the post', ['Party list PR', 'MMP', 'Single transferable vote'], 'India has 543 single-member constituencies.'),
            ('Which method is commonly used to allocate seats in party-list PR systems?', 'The D\'Hondt method', ['The Butler model', 'The Rostow model', 'The Lorenz curve'], 'It divides each party\'s votes by 1, 2, 3 and so on.'),
            ('In the 2015 UK election, UKIP won about 12.6% of the vote. How many seats did it win?', '1', ['82', '40', '0'], 'Its votes were spread thinly across constituencies.')],
     why=[('Explain why FPTP tends to favour large parties.', 'Winning a seat requires coming first locally, so parties with concentrated or widespread strong support win many seats, while smaller parties with support spread thinly win few.'),
          ('Explain why PR systems often produce coalition governments.', 'Because seats closely match votes and many parties win seats, a single party rarely wins a majority, so parties must form coalitions.'),
          ('Explain why supporters of FPTP value the constituency link.', 'Each area has a single representative who is accountable to local voters and can take up their concerns.'),
          ('Explain why some voters vote tactically under FPTP.', 'If their preferred party cannot win locally, they may vote for the candidate most likely to defeat the party they dislike, to avoid "wasting" their vote.')],
     contrast=[('first past the post', 'proportional representation', 'FPTP awards each seat to the local winner and often gives disproportionate results; PR allocates seats according to vote share, giving more representative but often coalition outcomes.'),
               ('a majority', 'a plurality', 'A majority is more than half of the votes; a plurality is simply more votes than any other candidate, which may be less than half.')],
     misc=[('Under FPTP a party\'s share of seats matches its share of votes.', 'FPTP often gives large seat bonuses to winning parties and few seats to smaller ones, as in the 2024 UK election.'),
           ('PR always leads to unstable governments.', 'Germany and the Nordic countries use PR and have had long periods of stable coalition government.'),
           ('A candidate must win more than half the votes to win under FPTP.', 'They only need more votes than any other candidate (a plurality).')],
     cases=[('the 2024 UK general election', 'Labour won 411 seats (63%) with 33.7% of the vote; Reform UK won 14.3% but only 5 seats.', 'disproportionality under FPTP', 'seat shares differed greatly from vote shares, renewing debate on electoral reform.'),
            ('New Zealand\'s 1993 referendum', 'After two elections in which the party with fewer votes won more seats (1978 and 1981), voters chose MMP in 1993.', 'electoral reform', 'perceived unfairness of FPTP led to a move to a more proportional system.')],
     evaluate=[('Proportional representation is fairer than first past the post.', ['seats match votes, so every vote counts more equally', 'smaller parties and minorities gain representation'], ['FPTP gives a clear local representative and usually decisive governments', 'PR can give small parties power in coalition bargaining'], 'PR is fairer in matching votes to seats, but "fairness" also includes accountability and stable government, where FPTP has strengths.')],
     src=[('Electoral reform report (paraphrased)', 'The report found that in the 2024 general election the gap between parties\' vote shares and seat shares was the largest in UK history. It argued that millions of votes had no effect on the result and called for a proportional system.', 'Paraphrase of Electoral Reform Society, report on the 2024 UK general election, 2024', 'to campaign for electoral reform by highlighting disproportional results', 'It uses official results and calculates clear measures of disproportionality.', 'It is produced by a campaign group that supports PR, so it may underplay FPTP\'s advantages.', 'The 2024 election was the most disproportional in UK history, supporting the case for PR.')],
     rq=[('How proportional were the results of UK general elections between 1997 and 2024 under first past the post?', 'Which voting system is best?', 'it is a value question without criteria', 'It uses measurable election data to evaluate representation.', 'Collect official results; calculate seat-vote gaps for each party; graph trends; read arguments for and against PR; evaluate sources; cite in APA.')])
C.electoral(K, 'ch08-st2', d=(2, 5))


@R.add('ch08-st2', 'C3', (1, 4), 'numerical')
def seat_gap(rng, slot):
    rows = [('Labour', 2024, 33.7, 411, 650), ('Reform UK', 2024, 14.3, 5, 650), ('the Liberal Democrats', 2024, 12.2, 72, 650),
            ('the Conservatives', 2019, 43.6, 365, 650), ('UKIP', 2015, 12.6, 1, 650), ('the SNP', 2015, 4.7, 56, 650),
            ('the Social Credit Party (New Zealand)', 1981, 20.7, 2, 92), ('the BJP (India)', 2019, 37.4, 303, 543), ('the BJP (India)', 2024, 36.6, 240, 543)]
    p, yr, v, s, tot = rng.choice(rows)
    sp = s / tot * 100
    diff = sp - v
    return dict(stem=f'In {yr}, {p} won {v}% of the vote and {s} of the {tot} seats. Calculate its seat share as a percentage and the difference between its seat share and vote share. State whether it was over- or under-represented.',
                answer=f'Seat share {sp:.1f}%; difference {abs(diff):.1f} percentage points; {"over" if diff > 0 else "under"}-represented.', type='numerical', marks=3,
                markingKey=f'{s}/{tot} × 100 = {sp:.1f}% (M1 A1); {sp:.1f} − {v} = {diff:+.1f} points → {"over" if diff > 0 else "under"}-represented (A1).', gap='G3')


K.st('ch08-st3', 'the making of the Indian Constitution and B. R. Ambedkar\'s role',
     terms=[('Constituent Assembly', 'the body elected in 1946 to draft India\'s Constitution; it met from December 1946 to January 1950'),
            ('Drafting Committee', 'the committee chaired by B. R. Ambedkar that prepared the text of the Constitution'),
            ('Fundamental Rights', 'rights guaranteed in Part III of the Indian Constitution, such as equality before the law and freedom of speech, enforceable in the courts'),
            ('Directive Principles of State Policy', 'guidelines in Part IV for governments to promote social and economic welfare; not enforceable in court'),
            ('Preamble', 'the introduction to the Constitution, declaring India a sovereign, democratic republic committed to justice, liberty, equality and fraternity'),
            ('untouchability', 'the caste-based practice of social exclusion of Dalits, abolished by Article 17 of the Constitution')],
     facts=[('On what date did the Constitution of India come into force?', '26 January 1950', ['15 August 1947', '26 November 1949', '2 October 1950'], '26 January is celebrated as Republic Day.'),
            ('Who chaired the Drafting Committee of the Indian Constitution?', 'B. R. Ambedkar', ['Jawaharlal Nehru', 'Rajendra Prasad', 'Sardar Patel'], 'Rajendra Prasad was President of the Constituent Assembly.'),
            ('Which article of the Constitution abolishes untouchability?', 'Article 17', ['Article 1', 'Article 370', 'Article 51A'], 'It forbids the practice in any form.'),
            ('About how long did the Constituent Assembly take to frame the Constitution?', 'Nearly three years', ['Three weeks', 'Ten years', 'Six months'], 'About 2 years, 11 months and 18 days.'),
            ('From which Indian community did Ambedkar come, which faced caste discrimination?', 'The Mahar community, classed as "untouchable" (Dalit)', ['The Brahmin community', 'The Parsi community', 'A royal family'], 'He faced discrimination at school and work.')],
     why=[('Explain why Ambedkar insisted on strong Fundamental Rights and safeguards for Dalits.', 'Having experienced caste discrimination himself, he believed that legal guarantees of equality, abolition of untouchability and reserved seats were needed to protect marginalised groups from majority domination.'),
          ('Explain why the Constitution established universal adult franchise from 1950.', 'The framers believed that political equality for all adults, regardless of literacy, caste, sex or property, was essential for a democratic republic and could drive social change.'),
          ('Explain why the Directive Principles are not enforceable in court.', 'They require resources and long-term policies, such as free education and fair wages, that a new and poor state could not immediately guarantee, so they guide rather than bind governments.'),
          ('Explain why the Constitution of India is so long.', 'It covers a large and diverse federation, sets out detailed relations between the Union and states, includes Fundamental Rights and Directive Principles, and borrowed provisions from many other constitutions.')],
     contrast=[('Fundamental Rights', 'Directive Principles of State Policy', 'Fundamental Rights are justiciable – citizens can go to court to enforce them; Directive Principles are non-justiciable guidelines for governments.'),
               ('the President of the Constituent Assembly', 'the Chair of the Drafting Committee', 'Rajendra Prasad presided over the Assembly\'s debates; Ambedkar led the committee that drafted the text.')],
     misc=[('Ambedkar wrote the whole Constitution alone.', 'He led the Drafting Committee and was its chief architect, but the text was debated and amended by the whole Constituent Assembly of about 299 members.'),
           ('India became a republic on 15 August 1947.', 'India gained independence as a dominion in 1947 and became a republic when the Constitution came into force on 26 January 1950.'),
           ('The Indian Constitution was copied from the British constitution.', 'It drew on many sources – British parliamentary government, the US Bill of Rights, the Irish Directive Principles and the Government of India Act 1935 – adapted to Indian conditions.')],
     cases=[('reservations in the Constitution', 'Seats were reserved for Scheduled Castes and Scheduled Tribes in legislatures, and the state was allowed to reserve jobs and education places for disadvantaged groups.', 'affirmative action to promote equality', 'the Constitution sought substantive, not just formal, equality.'),
            ('Ambedkar\'s final speech to the Assembly', 'On 25 November 1949 Ambedkar warned that India was entering a life of contradictions: political equality but social and economic inequality.', 'the limits of constitutional change', 'he recognised that laws alone could not end deep social inequality.')],
     evaluate=[('B. R. Ambedkar was the most important figure in the making of the Indian Constitution.', ['he chaired the Drafting Committee and steered the text through debates', 'his work ensured strong rights and abolished untouchability'], ['Nehru, Patel, Prasad and others shaped key decisions', 'the Assembly as a whole debated and amended every article'], 'Ambedkar was the chief architect of the text, but the Constitution was a collective achievement of the Assembly and national leaders.')],
     src=[('Speech (paraphrased)', 'The speaker warned the Assembly that on 26 January 1950 India would enter a life of contradictions: in politics there would be equality, with one person, one vote, one value, but in social and economic life inequality would continue. He urged that these contradictions be removed quickly or political democracy would be at risk.', 'Paraphrase of B. R. Ambedkar, speech to the Constituent Assembly, New Delhi, 25 November 1949', 'to reflect on the Constitution and warn the nation about the challenges ahead', 'It shows the chief architect\'s view of the Constitution\'s limits.', 'It is a speech at a ceremonial moment and does not provide evidence of what happened after 1950.', 'Political equality would not be enough without social and economic equality.')],
     rq=[('How effective have constitutional reservations been in increasing Dalit representation in India\'s Lok Sabha since 1952?', 'Who was Ambedkar?', 'it is a descriptive biographical question', 'It evaluates a constitutional safeguard using evidence over time.', 'Use Election Commission data and two academic studies; compare reserved and general seats; consider wider measures of inclusion; evaluate sources; cite in APA.')])
C.chronology(K, 'ch08-st3', events=[('the Government of India Act is passed', 1935), ('the Constituent Assembly first meets', 1946), ('India becomes independent', 1947),
                                     ('the Constitution is adopted by the Assembly', 1949), ('the Constitution comes into force', 1950), ('India holds its first general election', 1951),
                                     ('Ambedkar converts to Buddhism', 1956), ('Ambedkar is posthumously awarded the Bharat Ratna', 1990)])


K.st('ch08-st4', 'political participation through pressure groups, the media and civil society',
     terms=[('pressure group', 'an organisation that tries to influence government policy without standing for election'),
            ('civil society', 'organisations and groups outside government and business, such as charities, NGOs, unions and community groups'),
            ('lobbying', 'trying to persuade politicians or officials to support a particular policy'),
            ('free press', 'news media able to report without government censorship'),
            ('social movement', 'a large, loosely organised group of people working for social or political change'),
            ('petition', 'a formal written request signed by many people and sent to a government or authority')],
     facts=[('Which youth climate movement did Greta Thunberg begin with a school strike in 2018?', 'Fridays for Future', ['Extinction Rebellion', 'Greenpeace', 'Amnesty International'], 'She began striking outside the Swedish parliament.'),
            ('Which organisation, founded in 1961, campaigns for prisoners of conscience?', 'Amnesty International', ['the Red Cross', 'Oxfam', 'WWF'], 'It was founded by British lawyer Peter Benenson.'),
            ('Which Indian movement used the Right to Information as a tool to fight corruption and helped win the RTI Act of 2005?', 'The Mazdoor Kisan Shakti Sangathan (MKSS)', ['the Chipko movement', 'the Narmada Bachao Andolan', 'the Swadeshi movement'], 'It held public hearings in Rajasthan.'),
            ('In the UK, how many signatures does a parliamentary e-petition need to be considered for debate?', '100,000', ['1,000', '10,000', '1 million'], 'At 10,000 the government must respond.'),
            ('Which press freedom index is published annually by Reporters Without Borders?', 'The World Press Freedom Index', ['the Human Development Index', 'the Gini index', 'the Democracy Index'], 'It ranks 180 countries.')],
     why=[('Explain why pressure groups are important in a democracy.', 'They let citizens organise around specific issues between elections, give a voice to minorities, provide expertise to government and hold decision-makers to account.'),
          ('Explain why a free press is essential to democracy.', 'It informs citizens, exposes corruption and abuse of power, and allows debate, so voters can make informed choices and governments are accountable.'),
          ('Explain why social media has changed political participation.', 'It allows people to organise protests and campaigns quickly and cheaply and reach global audiences, but it also spreads misinformation and can create echo chambers.'),
          ('Explain why some pressure groups have more influence than others.', 'Groups with money, expert knowledge, large memberships or close links to government (insider groups) usually have more access and influence than outsider groups.')],
     contrast=[('a pressure group', 'a political party', 'A pressure group seeks to influence policy on specific issues without standing for election; a party contests elections and aims to form a government on a broad programme.'),
               ('an insider group', 'an outsider group', 'An insider group is consulted by government and works through official channels; an outsider group lacks access and uses protests and media campaigns.')],
     misc=[('Voting in elections is the only way to participate in politics.', 'Citizens also participate through petitions, protests, pressure groups, volunteering, contacting representatives and the media.'),
           ('Pressure groups are always undemocratic because nobody elects them.', 'They are part of a healthy democracy because they represent citizens\' views, though wealthy groups may have unequal influence.'),
           ('Everything shared on social media is reliable political information.', 'Social media contains misinformation; claims should be checked against reliable sources.')],
     cases=[('the Chipko movement', 'In the 1970s villagers in Uttarakhand, many of them women, hugged trees to prevent logging; in 1980 the government banned green felling in Himalayan forests of Uttar Pradesh for 15 years.', 'grassroots civil society action', 'non-violent local action changed national forest policy.'),
            ('Fridays for Future', 'Starting with one student in 2018, school climate strikes spread worldwide; on 20 September 2019 an estimated 4 million people joined global climate strikes.', 'youth political participation', 'young people without the vote influenced public debate through protest and media.')],
     evaluate=[('Pressure groups are more effective than voting in bringing about political change.', ['groups like the Chipko movement and MKSS achieved specific policy changes', 'they allow continuous participation, not just every few years'], ['elections decide who holds power and which laws pass', 'many pressure groups fail, and wealthy groups may dominate'], 'Pressure groups can be highly effective on specific issues, but they work alongside, not instead of, elections, which determine who governs.')],
     src=[('Speech (paraphrased)', 'The young speaker told world leaders at a UN summit that they had failed her generation by not acting on climate change despite clear science. She said young people were watching and would not forgive inaction.', 'Paraphrase of Greta Thunberg, speech at the UN Climate Action Summit, New York, 23 September 2019', 'to pressure world leaders to take urgent action on climate change', 'It shows how a youth activist used a global platform to influence debate.', 'It is an emotional, persuasive speech and does not set out detailed policy proposals.', 'Leaders have failed young people on climate change and must act urgently.')],
     rq=[('How did the Mazdoor Kisan Shakti Sangathan influence the passing of India\'s Right to Information Act in 2005?', 'Are protests good?', 'it is a vague value question', 'It examines how civil society influenced a real law.', 'Read accounts by MKSS founders and two academic studies; collect newspaper reports; build a timeline; evaluate perspectives; cite in MLA.')])
C.pct_change(K, 'ch08-st4', [('individual membership of the UK Labour Party', 'members', 2015, 201000, 2017, 564000, 'approx., House of Commons Library')], d=(1, 3))

# =============================================================================================
# ch09 Migration
# =============================================================================================
K.st('ch09-st1', 'types of migration: voluntary and forced, internal and international',
     terms=[('migration', 'the movement of people from one place to another to live, either permanently or for a long period'),
            ('voluntary migration', 'migration chosen freely, for example for work, study or family'),
            ('forced migration', 'migration that people are compelled to undertake because of conflict, persecution, disaster or development projects'),
            ('refugee', 'a person who has fled their country owing to a well-founded fear of persecution and is protected under the 1951 Refugee Convention'),
            ('internally displaced person (IDP)', 'a person forced to flee their home who remains within their own country\'s borders'),
            ('push factor', 'a reason that encourages people to leave a place, such as unemployment or conflict'),
            ('pull factor', 'a reason that attracts people to a place, such as jobs, safety or better services')],
     facts=[('According to UNHCR, about how many people were forcibly displaced worldwide by mid-2024?', 'About 120 million', ['About 12 million', 'About 1.2 million', 'About 1.2 billion'], 'This includes refugees, asylum seekers and IDPs.'),
            ('Which 1951 international treaty defines who is a refugee?', 'The Refugee Convention', ['the Geneva Convention on prisoners of war', 'the Paris Agreement', 'the Treaty of Versailles'], 'Its 1967 Protocol removed time and geographic limits.'),
            ('About how many international migrants were there in 2020, according to the UN?', 'About 281 million', ['About 28 million', 'About 2.8 billion', 'About 81 million'], 'About 3.6% of the world population.'),
            ('Movement from rural villages to cities within China is an example of what?', 'Internal voluntary migration', ['International forced migration', 'Refugee movement', 'Emigration'], 'Hundreds of millions of rural workers have moved to cities.'),
            ('Which theory, proposed by E. G. Ravenstein in the 1880s, set out "laws of migration"?', 'Ravenstein\'s laws of migration', ['the Butler model', 'the demographic transition model', 'Malthusian theory'], 'He noted that most migrants move short distances.')],
     why=[('Explain why most migration is internal rather than international.', 'Moving within a country is cheaper, needs no visa, and migrants share a language and culture; most people move short distances, often from rural to urban areas.'),
          ('Explain why the distinction between voluntary and forced migration is not always clear.', 'Many migrants face a mix of pressures – poverty, drought and insecurity – so a decision may be partly chosen and partly forced, as with climate-related migration.'),
          ('Explain why internally displaced people may be more vulnerable than refugees.', 'IDPs remain under their own government, which may be causing or unable to stop the conflict, and they lack the international legal protection of refugee status.'),
          ('Explain why intervening obstacles affect migration.', 'Barriers such as distance, cost, border controls and language make it harder to move, so even with strong push and pull factors people may not migrate.')],
     contrast=[('a refugee', 'an economic migrant', 'A refugee flees persecution or conflict and is protected by international law; an economic migrant moves mainly to improve their income or opportunities.'),
               ('emigration', 'immigration', 'Emigration is leaving a country to live elsewhere; immigration is arriving in a new country to live.')],
     misc=[('Most of the world\'s refugees live in rich countries in Europe and North America.', 'According to UNHCR, about 70% of refugees live in countries neighbouring their own, mostly low- and middle-income countries.'),
           ('Migrants and refugees are the same thing.', 'Refugees have fled persecution and have specific legal protection; migrant is a broader term for anyone who moves.'),
           ('Migration is mainly a modern phenomenon.', 'Humans have migrated throughout history, from early human dispersal out of Africa to the migrations of the 19th century.')],
     cases=[('rural–urban migration in China', 'From the 1980s, hundreds of millions of rural workers moved to coastal cities such as Shenzhen to work in factories, though the hukou system limited their access to urban services.', 'internal voluntary migration', 'economic pull factors drove one of the largest migrations in history.'),
            ('displacement from Syria', 'Since 2011 the war in Syria has displaced over 13 million people, about half the pre-war population; most refugees went to Türkiye, Lebanon and Jordan.', 'forced international and internal migration', 'conflict caused both refugee flows and internal displacement, mostly to neighbouring countries.')],
     evaluate=[('Push factors are more important than pull factors in explaining migration.', ['conflict and disaster force people to leave regardless of destination', 'poverty and lack of jobs drive much rural–urban migration'], ['migrants usually choose destinations with jobs, family networks and safety', 'many migrants are relatively better off and move for opportunities'], 'Both matter: push factors explain why people leave, but pull factors and networks explain where they go; their balance differs between forced and voluntary migration.')],
     src=[('UNHCR report (paraphrased)', 'The report stated that the number of forcibly displaced people had risen for twelve consecutive years, driven by conflicts in Sudan, Myanmar, Ukraine and elsewhere. It noted that low- and middle-income countries hosted around 70% of refugees.', 'Paraphrase of UNHCR, Global Trends: Forced Displacement in 2023, Geneva, 2024', 'to inform governments and the public about displacement and appeal for support', 'It is the main global source of displacement data, compiled from national and field data.', 'Numbers of IDPs are estimates in conflict zones and the agency also seeks funding, which may shape its emphasis.', 'Forced displacement keeps rising and is hosted mostly by poorer countries.')],
     rq=[('What push and pull factors explain migration from rural Bihar to Mumbai since 2000?', 'Why do people move?', 'it is too broad and has no place or time', 'It applies push–pull theory to a specific internal migration flow.', 'Use Census of India migration tables, two research papers and interview transcripts; categorise factors; map flows; evaluate sources; cite in APA.')])
C.pct_change(K, 'ch09-st1', [('the number of international migrants', 'million', 1990, 153, 2020, 281, 'UN DESA'),
                              ('the number of forcibly displaced people worldwide', 'million', 2012, 42.7, 2023, 117.3, 'UNHCR')], d=(1, 4))


@R.add('ch09-st1', 'C3', (1, 4), 'numerical')
def net_migration(rng, slot):
    place = rng.choice(['Canada', 'Australia', 'Germany', 'the United Arab Emirates', 'New Zealand', 'Singapore', 'Ireland', 'Spain'])
    imm = rng.choice([120, 250, 400, 650, 900]) * 1000
    em = rng.choice([40, 90, 150, 210, 300]) * 1000
    pop = rng.choice([5, 9, 25, 40, 83]) * 1_000_000
    net = imm - em
    rate = net / pop * 1000
    if slot.d <= 2:
        return dict(stem=f'In one year about {imm:,} people immigrated to a country such as {place} and {em:,} emigrated. Calculate net migration and state whether it is net gain or loss.',
                    answer=f'{net:+,} (net {"gain" if net > 0 else "loss"})', type='numerical', marks=2,
                    markingKey=f'Net migration = immigrants − emigrants = {imm:,} − {em:,} = {net:+,} (M1 A1).', gap='G3')
    return dict(stem=f'A country with a population of {pop:,} recorded {imm:,} immigrants and {em:,} emigrants in a year. Calculate the net migration rate per 1,000 people.',
                answer=f'{rate:+.1f} per 1,000', type='numerical', marks=3,
                markingKey=f'Net = {net:+,} (M1); ÷ {pop:,} × 1,000 (M1) = {rate:+.1f} per 1,000 (A1).', gap='G3')


K.st('ch09-st2', 'historical migrations: indentured labour, the Atlantic slave trade and the Indian diaspora',
     terms=[('Atlantic slave trade', 'the forced transport of enslaved Africans to the Americas between the 16th and 19th centuries'),
            ('triangular trade', 'the trade route linking Europe (manufactured goods), West Africa (enslaved people) and the Americas (sugar, cotton, tobacco)'),
            ('Middle Passage', 'the sea voyage across the Atlantic in which enslaved Africans were transported in brutal conditions'),
            ('indentured labour', 'a system in which workers signed contracts to work for a fixed period, usually five years, in return for passage, wages and sometimes a return ticket'),
            ('girmitiya', 'an Indian indentured labourer, from the word "agreement" (girmit)'),
            ('diaspora', 'a population living outside its ancestral homeland while keeping cultural links to it')],
     facts=[('About how many enslaved Africans were forcibly transported across the Atlantic?', 'About 12.5 million', ['About 125,000', 'About 1.2 million', 'About 125 million'], 'The Trans-Atlantic Slave Trade Database estimates about 12.5 million embarked; about 10.7 million survived the voyage.'),
            ('When did Britain abolish slavery in most of its colonies?', 'With the Slavery Abolition Act of 1833', ['In 1707', 'In 1807', 'In 1888'], 'The 1807 Act abolished the British slave trade, not slavery.'),
            ('In which year did the first ship carrying Indian indentured labourers arrive in Mauritius under the British system?', '1834', ['1757', '1857', '1947'], 'Mauritius became the largest destination.'),
            ('When was the system of Indian indentured emigration officially ended?', '1917 (finally abolished in 1920)', ['1833', '1857', '1947'], 'Campaigns in India and by figures such as Gandhi and C. F. Andrews opposed it.'),
            ('Which ship brought the first Indian indentured labourers to Fiji in 1879?', 'The Leonidas', ['the Mayflower', 'the Windrush', 'the Komagata Maru'], 'About 60,000 Indians went to Fiji.')],
     why=[('Explain why European colonial powers turned to indentured labour after the abolition of slavery.', 'Plantation owners in places such as Mauritius, Trinidad, Guyana and Fiji still needed cheap labour for sugar, so they recruited workers from India and China on fixed contracts.'),
          ('Explain why many Indians agreed to become indentured labourers.', 'Poverty, famine, debt and land loss in regions such as Bihar and Uttar Pradesh pushed people to leave, while recruiters promised wages and land, sometimes misleadingly.'),
          ('Explain why indentured labour has been described as "a new system of slavery".', 'Although workers signed contracts, many were deceived, faced harsh conditions, low pay, penalties and imprisonment for leaving, and high death rates, similar to the conditions of slavery.'),
          ('Explain why the Atlantic slave trade had long-term effects on Africa.', 'It removed millions of young people, encouraged warfare and raiding, disrupted economies and political systems, and contributed to lasting underdevelopment.')],
     contrast=[('enslavement', 'indentured labour', 'Enslaved people were owned as property for life with no rights, and their children were enslaved too; indentured labourers signed (often unfair) contracts for a fixed term and were legally free afterwards.'),
               ('the abolition of the slave trade', 'the abolition of slavery', 'Abolishing the trade (Britain 1807) banned buying and transporting enslaved people; abolishing slavery (Britain 1833) freed people already enslaved.')],
     misc=[('Indentured labourers were free workers who were treated fairly.', 'Many were recruited by deception, faced harsh discipline and criminal penalties for breaking contracts, and had high death rates.'),
           ('Enslaved Africans did not resist slavery.', 'Resistance included revolts (such as the Haitian Revolution from 1791), escape, sabotage and preserving culture.'),
           ('The Indian diaspora only began after 1947.', 'Large-scale Indian migration began in the 19th century with indentured labour to the Caribbean, Indian Ocean, Fiji and Africa.')],
     cases=[('Indian indenture in Trinidad', 'About 144,000 Indians arrived between 1845 and 1917; their descendants now form around a third of Trinidad and Tobago\'s population.', 'the creation of a diaspora', 'indentured migration created a lasting Indo-Caribbean community.'),
            ('the Haitian Revolution', 'Beginning in 1791, enslaved people in the French colony of Saint-Domingue rose up under leaders including Toussaint Louverture; Haiti declared independence in 1804.', 'resistance to slavery', 'enslaved people overthrew slavery and created the first independent Black republic.')],
     evaluate=[('Indentured labour was simply slavery under another name.', ['many labourers were deceived and faced brutal conditions and penalties', 'the system served the same plantation economies'], ['labourers had contracts, wages and a fixed term, and many chose to stay as free settlers', 'the system was eventually reformed and abolished after protest'], 'Indenture was not identical to slavery, because workers were not owned for life, but its coercion and abuses justify the description of a "new system of slavery".')],
     src=[('Historian\'s account (paraphrased)', 'The historian argued that the indenture system recreated many features of slavery: recruitment by fraud, crowded voyages, harsh plantation discipline and criminal penalties for absence from work. He concluded that it was "a new system of slavery".', 'Paraphrase of Hugh Tinker, A New System of Slavery: The Export of Indian Labour Overseas, 1830–1920, Oxford University Press, 1974', 'to analyse the indenture system using colonial archives', 'It is a detailed academic study based on extensive archival research.', 'It relies largely on official records and may give less weight to labourers\' own voices and agency.', 'Indenture reproduced many abuses of slavery.')],
     rq=[('How did Indian indentured labourers in Fiji experience working conditions between 1879 and 1916?', 'What was indenture?', 'it is a definition question', 'It focuses on lived experience using primary sources.', 'Use Totaram Sanadhya\'s memoir, colonial reports and two historians; compare perspectives; evaluate OPVL; cite in MLA.')])
C.chronology(K, 'ch09-st2', events=[('the first enslaved Africans are taken directly from Africa to the Americas', 1526), ('the Haitian Revolution begins', 1791), ('Britain abolishes the slave trade', 1807),
                                     ('the Slavery Abolition Act is passed in Britain', 1833), ('Indian indentured labourers arrive in Mauritius', 1834), ('Indian indentured labourers first reach Trinidad', 1845),
                                     ('slavery is abolished in the United States', 1865), ('the Leonidas brings indentured Indians to Fiji', 1879), ('Brazil abolishes slavery', 1888),
                                     ('Indian indentured emigration is stopped', 1917)])


@R.add('ch09-st2', 'C3', (1, 4), 'numerical')
def mortality(rng, slot):
    rows = [('enslaved Africans embarked on all slave ships', 'survived the Middle Passage', 12.5, 10.7, 'million', 'Trans-Atlantic Slave Trade Database estimates, 1501–1866'),
            ('enslaved Africans embarked on British ships', 'were landed alive in the Americas', 3.26, 2.72, 'million', 'approx., Trans-Atlantic Slave Trade Database'),
            ('enslaved Africans embarked on Portuguese and Brazilian ships', 'were landed alive in the Americas', 5.85, 4.86, 'million', 'approx., Trans-Atlantic Slave Trade Database'),
            ('enslaved Africans embarked on French ships', 'were landed alive in the Americas', 1.38, 1.12, 'million', 'approx., Trans-Atlantic Slave Trade Database')]
    a, b, x, y, unit, src = rng.choice(rows)
    p = y / x * 100
    return dict(stem=f'Of about {x} {unit} {a}, about {y} {unit} {b} ({src}). Calculate the percentage who {b}, and the percentage who did not.',
                answer=f'{p:.1f}%; {100 - p:.1f}%', type='numerical', marks=2,
                markingKey=f'{y} ÷ {x} × 100 = {p:.1f}% (M1 A1); 100 − {p:.1f} = {100 - p:.1f}%. Accept answers from rounded data.', gap='G3')


K.st('ch09-st3', 'Partition and refugee movements in the 20th century',
     terms=[('Partition', 'the division of British India in August 1947 into the independent states of India and Pakistan (including East Pakistan, later Bangladesh)'),
            ('Radcliffe Line', 'the boundary between India and Pakistan drawn by Cyril Radcliffe and announced on 17 August 1947'),
            ('communal violence', 'violence between religious or ethnic communities'),
            ('refugee camp', 'a temporary settlement providing shelter and aid for displaced people'),
            ('UNHCR', 'the United Nations High Commissioner for Refugees, created in 1950 to protect and assist refugees'),
            ('rehabilitation', 'helping displaced people rebuild their lives through housing, land, jobs and compensation')],
     facts=[('Roughly how many people were displaced by the Partition of India in 1947?', 'About 12–15 million', ['About 1 million', 'About 100 million', 'About 150,000'], 'It was one of the largest migrations in history.'),
            ('Who drew the boundary between India and Pakistan in 1947?', 'Sir Cyril Radcliffe', ['Lord Mountbatten', 'Jawaharlal Nehru', 'Muhammad Ali Jinnah'], 'He had about five weeks and had never visited India before.'),
            ('Which two provinces of British India were divided by Partition?', 'Punjab and Bengal', ['Madras and Bombay', 'Sindh and Assam', 'Bihar and Orissa'], 'Both had large Muslim and non-Muslim populations.'),
            ('Estimates of deaths in the violence of Partition range between roughly what?', '200,000 and 2 million', ['2,000 and 20,000', '20 and 200 million', 'Fewer than 1,000'], 'Precise figures are disputed.'),
            ('Which 1948 conflict created a major Palestinian refugee population?', 'The 1948 Arab–Israeli War', ['the Korean War', 'the Suez Crisis', 'the Gulf War'], 'About 700,000 Palestinians fled or were expelled; UNRWA was set up in 1949 to assist them.')],
     why=[('Explain why Partition led to such large-scale migration.', 'The new border divided mixed communities; many people feared becoming minorities in the new state, and violence and insecurity drove Hindus and Sikhs to India and Muslims to Pakistan.'),
          ('Explain why the speed of British withdrawal contributed to the violence of Partition.', 'The date was brought forward to August 1947, the border was announced only after independence, and there was little planning or security for the population movements that followed.'),
          ('Explain why refugee resettlement was a major challenge for India and Pakistan after 1947.', 'Millions arrived with few possessions, needing housing, land, jobs and compensation; both new states had limited resources and had to build camps and new towns, such as colonies in Delhi.'),
          ('Explain why oral history is important for studying Partition.', 'Official records say little about ordinary people\'s experiences; oral testimonies preserve memories of displacement, loss and survival from those who lived through it.')],
     contrast=[('refugees in 1947', 'internally displaced people today', 'Many 1947 migrants crossed the new international border and became citizens of the new state; IDPs today remain displaced within their own country without crossing a border.'),
               ('the experience of Partition in Punjab', 'the experience of Partition in Bengal', 'In Punjab migration was rapid and almost complete within months, with severe violence; in Bengal migration was more gradual and continued over decades.')],
     misc=[('Partition affected only Hindus and Muslims.', 'Sikhs, Christians and other communities were also deeply affected, especially Sikhs in Punjab.'),
           ('All refugees from Partition were quickly resettled.', 'Many lived in camps for years, and migration from East Bengal continued long after 1947.'),
           ('The number of people killed in Partition is precisely known.', 'Estimates vary widely, from about 200,000 to 2 million, because records were incomplete.')],
     cases=[('Kingsway Camp, Delhi', 'One of the largest refugee camps after Partition, housing hundreds of thousands of people from West Punjab; refugees later settled in new colonies such as Lajpat Nagar.', 'refugee resettlement', 'the camp shows how a new state had to house and rehabilitate millions of displaced people.'),
            ('the 1971 Bangladesh Liberation War', 'About 10 million refugees fled from East Pakistan to India during the conflict; most returned after Bangladesh became independent.', 'mass refugee movement', 'conflict created one of the largest refugee flows of the 20th century, with major effects on a neighbouring country.')],
     evaluate=[('The British government was mainly responsible for the suffering caused by Partition.', ['the hurried withdrawal and late announcement of the border left little planning or security', 'colonial policies had deepened communal divisions'], ['Indian political leaders also agreed to Partition and could not control local violence', 'local communal tensions and armed groups drove much of the violence'], 'Britain\'s rushed withdrawal bears significant responsibility, but the suffering also resulted from political decisions by Indian leaders and local violence; responsibility was shared.')],
     src=[('Oral history (paraphrased)', 'The interviewee, a schoolgirl in Lahore in 1947, recalled that her family left in a hurry, taking only a few belongings and expecting to return in a few weeks. She described the long journey to Amritsar and the years spent rebuilding their lives in Delhi, and said she never saw her childhood home again.', 'Paraphrase of an interview recorded by the 1947 Partition Archive, 2015', 'to preserve the memories of people who experienced Partition', 'It gives a personal, first-hand view of displacement that official records lack.', 'It was recorded nearly seventy years later, so memories may have changed; it is one individual\'s experience.', 'Families fled suddenly, expecting to return, and had to rebuild their lives.')],
     rq=[('How did the Indian government try to resettle refugees from West Punjab in Delhi between 1947 and 1955?', 'Was Partition bad?', 'it is a vague value question', 'It investigates government response and refugee experience using a range of sources.', 'Use government reports, oral histories from the 1947 Partition Archive and two historians; map new colonies; evaluate sources; cite in MLA.')])
C.chronology(K, 'ch09-st3', events=[('the Muslim League\'s Lahore Resolution', 1940), ('the Direct Action Day violence in Calcutta', 1946), ('India and Pakistan become independent', 1947),
                                     ('the 1948 Arab–Israeli War displaces Palestinians', 1948), ('UNHCR is established', 1950), ('the Refugee Convention is signed', 1951),
                                     ('refugees flee East Pakistan to India', 1971), ('the Vietnamese "boat people" crisis peaks', 1979)])


K.st('ch09-st4', 'the impacts of migration on source and host communities',
     terms=[('remittances', 'money sent home by migrants to their families'),
            ('brain drain', 'the emigration of highly skilled or educated people from a country'),
            ('brain gain', 'the benefit a country gains from returning or incoming skilled migrants'),
            ('multiculturalism', 'the presence and acceptance of several cultures within one society'),
            ('integration', 'the process by which migrants become part of the host society while keeping aspects of their own culture'),
            ('dependency ratio', 'the number of dependants (young and old) compared with the working-age population')],
     facts=[('Which country received the most remittances in the world in 2023, at about US$ 120 billion?', 'India', ['the United States', 'Germany', 'Brazil'], 'Mexico was second.'),
            ('In which country did remittances make up over a quarter of GDP in the 2020s?', 'Tajikistan (and Tonga)', ['Germany', 'Japan', 'Brazil'], 'Remittances can dominate small economies.'),
            ('Which Kerala-based migration flow has transformed the state\'s economy since the 1970s?', 'Migration to the Gulf states', ['Migration to Antarctica', 'Migration to Siberia', 'Migration to Greenland'], 'Gulf remittances fund housing, education and consumption.'),
            ('Which ship\'s arrival in 1948 symbolises post-war Caribbean migration to Britain?', 'HMT Empire Windrush', ['the Titanic', 'the Mayflower', 'the Leonidas'], 'It docked at Tilbury on 21 June 1948.'),
            ('Which term describes the loss of doctors and nurses from countries such as Zimbabwe and the Philippines to richer countries?', 'Brain drain', ['Brain gain', 'Remittances', 'Counter-urbanisation'], 'It can weaken health systems at home.')],
     why=[('Explain why remittances can benefit source countries.', 'They raise household incomes, pay for education, healthcare and housing, provide foreign currency and are often more stable than foreign aid or investment.'),
          ('Explain why migration can cause a brain drain.', 'Skilled workers educated at public expense leave for higher pay abroad, so the source country loses their skills and the return on its investment in training.'),
          ('Explain why migrants can help host countries with ageing populations.', 'Migrants are mostly of working age, so they fill labour shortages, pay taxes and help support pensions and care systems.'),
          ('Explain why migration can create tensions in host communities.', 'Rapid change may raise concerns about jobs, housing and services, and misinformation or prejudice can be exploited politically, even when evidence shows overall economic benefits.')],
     contrast=[('impacts on the source country', 'impacts on the host country', 'Source countries gain remittances but may lose workers and skills; host countries gain workers and cultural diversity but may face pressure on services and social tensions.'),
               ('brain drain', 'brain gain', 'Brain drain is the loss of skilled people through emigration; brain gain is the gain of skills through immigration or return migration.')],
     misc=[('Migrants take jobs from local people.', 'Research generally finds that migrants fill labour shortages and create demand that generates jobs; effects on local wages are usually small.'),
           ('Emigration only harms source countries.', 'Remittances, returning migrants\' skills and diaspora investment can bring significant benefits.'),
           ('Migrants are a burden on public services.', 'Studies in many countries show that working-age migrants often pay more in taxes than they use in services, though impacts vary.')],
     cases=[('Kerala and the Gulf', 'Millions of Keralites have worked in the Gulf since the 1970s; remittances have funded new houses, schools and businesses, though families face long separations.', 'impacts on a source region', 'migration brought economic gains but also social costs and dependence on Gulf economies.'),
            ('the Windrush generation', 'Caribbean migrants arriving in Britain from 1948 helped staff the NHS and transport; in 2018 it emerged that some had been wrongly denied rights or deported.', 'impacts on a host country and on migrants', 'migrants made major contributions but also faced discrimination and policy failures.')],
     evaluate=[('Migration brings more benefits than costs to source countries.', ['remittances reduce poverty and provide foreign exchange', 'diaspora networks bring investment and ideas'], ['brain drain weakens health and education systems', 'families are separated and economies can become dependent on remittances'], 'For many countries the benefits of remittances outweigh the costs, but the loss of skilled workers can be serious, especially in health care in small, poor countries.')],
     src=[('World Bank brief (paraphrased)', 'The brief reported that remittances to low- and middle-income countries reached about US$ 656 billion in 2023, more than foreign direct investment and official development assistance combined. India received the largest amount, followed by Mexico, China and the Philippines.', 'Paraphrase of World Bank / KNOMAD, Migration and Development Brief 40, June 2024', 'to inform policymakers about remittance trends', 'It is a reputable international source using central bank data.', 'Official figures exclude informal transfers, so true remittances may be higher; it gives little detail on social impacts.', 'Remittances are a major, growing financial flow to poorer countries.')],
     rq=[('How have remittances from the Gulf affected household spending in Kerala since 2000?', 'Is migration good or bad?', 'it is a vague value question', 'It investigates a measurable impact of migration on a source region.', 'Use Kerala Migration Survey data and two academic studies; analyse spending categories; consider social impacts; evaluate sources; cite in APA.')])
C.pct_change(K, 'ch09-st4', [('remittances received by India', 'US$ billion', 2010, 53.5, 2023, 120, 'World Bank'),
                              ('remittances received by Mexico', 'US$ billion', 2013, 23.4, 2023, 66.2, 'World Bank / Banco de México'),
                              ('remittances to low- and middle-income countries', 'US$ billion', 2010, 341, 2023, 656, 'World Bank')], d=(1, 4))
C.dependency(K, 'ch09-st4', c=('C3',), d=(2, 4))

# =============================================================================================
# ch10 Agriculture and Food
# =============================================================================================
K.st('ch10-st1', 'farming systems: subsistence and commercial, arable and pastoral',
     terms=[('subsistence farming', 'farming to produce food mainly for the farmer\'s own family, with little surplus to sell'),
            ('commercial farming', 'farming to produce crops or livestock for sale at a profit'),
            ('arable farming', 'growing crops such as wheat, rice or maize'),
            ('pastoral farming', 'rearing animals such as cattle, sheep or goats'),
            ('mixed farming', 'combining arable and pastoral farming on the same farm'),
            ('intensive farming', 'farming with high inputs of labour or capital per hectare to achieve high yields'),
            ('extensive farming', 'farming with low inputs per hectare over large areas, such as sheep ranching in Australia')],
     facts=[('Wet-rice cultivation in the Ganges delta is usually an example of which farming type?', 'Intensive subsistence arable farming', ['Extensive commercial pastoral farming', 'Plantation farming', 'Nomadic herding'], 'High labour inputs on small plots.'),
            ('Cattle ranching on the pampas of Argentina is an example of what?', 'Extensive commercial pastoral farming', ['Intensive subsistence arable farming', 'Shifting cultivation', 'Market gardening'], 'Large areas with few workers per hectare.'),
            ('Which farming system is used by the Maasai in Kenya and Tanzania?', 'Pastoral nomadism', ['Plantation agriculture', 'Hydroponics', 'Intensive arable farming'], 'They move herds seasonally to find pasture and water.'),
            ('A farm system has inputs, processes and outputs. Which of these is an input?', 'Fertiliser', ['Harvesting', 'Milk', 'Wheat sold at market'], 'Inputs are what goes into the farm.'),
            ('Which crop is typically grown on large commercial plantations in Assam?', 'Tea', ['Wheat', 'Potatoes', 'Barley'], 'Assam is one of the world\'s largest tea-growing regions.')],
     why=[('Explain why farming is often described as a system.', 'A farm has inputs (land, labour, seeds, fertiliser, machinery), processes (ploughing, sowing, harvesting) and outputs (crops, animals, waste), with feedback such as profits reinvested.'),
          ('Explain why physical factors influence the type of farming in an area.', 'Climate, relief and soil determine what can grow: steep, dry or cold land suits pastoral farming, while flat, fertile, well-watered land suits arable farming.'),
          ('Explain why subsistence farmers are vulnerable to drought.', 'They depend on their own harvests for food, have little savings or irrigation, and cannot easily buy food when crops fail.'),
          ('Explain why commercial farms are often larger and more mechanised than subsistence farms.', 'They aim to maximise profit, so they invest capital in machinery and land to achieve economies of scale and sell large outputs.')],
     contrast=[('intensive farming', 'extensive farming', 'Intensive farming uses high inputs on small areas for high yields per hectare; extensive farming uses low inputs over large areas with lower yields per hectare.'),
               ('subsistence farming', 'commercial farming', 'Subsistence farming produces food mainly for the family; commercial farming produces for sale and profit.')],
     misc=[('Subsistence farming is always extensive.', 'Wet-rice farming in South and East Asia is intensive subsistence farming with very high labour inputs.'),
           ('Commercial farming only happens in rich countries.', 'Commercial farms and plantations exist across the world, such as soybean farms in Brazil and tea estates in Kenya and India.'),
           ('Pastoral farming always means nomadic herding.', 'Pastoral farming includes settled dairy and beef farms as well as nomadic herding.')],
     cases=[('soybean farming in Mato Grosso, Brazil', 'Huge mechanised farms grow soybeans for export, mainly to China, making Brazil the world\'s largest soybean exporter.', 'extensive commercial arable farming', 'large capital-intensive farms produce for global markets, partly by clearing savanna and forest.'),
            ('dairy farming in the Netherlands', 'Small but highly intensive farms with high-yield cows and technology make the Netherlands a leading dairy exporter.', 'intensive commercial pastoral farming', 'capital and technology produce very high outputs from small areas.')],
     evaluate=[('Commercial farming is better than subsistence farming for developing countries.', ['it raises incomes, exports and productivity', 'it can provide jobs and foreign currency'], ['it can increase inequality, land concentration and environmental damage', 'subsistence farming supports food security and resilience for millions of families'], 'Commercial farming can drive growth, but a mix is often best, supporting smallholders to raise productivity and sell surpluses while protecting food security.')],
     src=[('FAO report (paraphrased)', 'The report estimated that there are about 608 million family farms in the world, operating around 70–80% of farmland and producing about 80% of the world\'s food in value terms. It noted that most are very small, with less than two hectares.', 'Paraphrase of Food and Agriculture Organization of the United Nations, The State of Food and Agriculture 2014', 'to highlight the importance of family farming in the International Year of Family Farming', 'It is a major international source using census data from many countries.', 'Data quality varies between countries, and the report promotes family farming, which may shape its emphasis.', 'Small family farms produce most of the world\'s food.')],
     rq=[('How has the size of soybean farms in Mato Grosso, Brazil, changed between 2000 and 2020, and why?', 'What is farming?', 'it is a definition question', 'It investigates change in a commercial farming system and its causes.', 'Use IBGE agricultural census data, satellite images and two studies; graph change; explain factors; evaluate sources; cite in APA.')])


@R.add('ch10-st1', ('C3', 'C4'), (1, 5), 'numerical')
def crop_yield(rng, slot):
    crop, place, yld = rng.choice([('rice', 'a farm in West Bengal', [2.5, 3, 3.5, 4]), ('wheat', 'a farm in Punjab', [3, 4, 4.5, 5]),
                                   ('maize', 'a smallholding in Malawi', [1.2, 1.5, 2, 2.5]), ('soybeans', 'a farm in Mato Grosso', [3, 3.2, 3.5]),
                                   ('coffee', 'a farm in Ethiopia', [0.6, 0.8, 1]), ('wheat', 'a farm in Kansas', [3, 3.5, 4])])
    ha = rng.choice([0.5, 1.5, 2, 4, 12, 40, 250])
    y = rng.choice(yld)
    out = ha * y
    if slot.d <= 2:
        return dict(stem=f'{C.cap(place)} grows {crop} on {ha} hectares with a yield of {y} tonnes per hectare. Calculate the total output.',
                    answer=f'{out:g} tonnes', type='numerical', marks=2, markingKey=f'Output = area × yield = {ha} × {y} = {out:g} t (M1 A1).', gap='G3')
    price = rng.choice([150, 220, 300, 400, 2500])
    cost = rng.choice([300, 500, 800]) * ha
    inc = out * price - cost
    if slot.d == 3:
        return dict(stem=f'{C.cap(place)} harvests {out:g} tonnes of {crop} from {ha} hectares. Calculate the yield in tonnes per hectare.',
                    answer=f'{y:g} t/ha', type='numerical', marks=2, markingKey=f'Yield = output ÷ area = {out:g} ÷ {ha} = {y:g} t/ha (M1 A1).', gap='G3')
    return dict(stem=(f'{C.cap(place)} farms {ha} hectares of {crop}, yielding {y} t/ha. It sells at US$ {price} per tonne and total costs are US$ {cost:,.0f}. '
                      'Calculate the farm\'s profit and suggest one way it could increase yields.'),
                answer=f'US$ {inc:,.0f}', type='multi_step', marks=4,
                markingKey=f'Output {ha} × {y} = {out:g} t (M1); revenue {out:g} × {price} = US$ {out * price:,.0f} (M1); profit = {out * price:,.0f} − {cost:,.0f} = US$ {inc:,.0f} (A1). '
                           'Valid method (R1), e.g. irrigation, improved seeds, fertiliser, better storage.', gap='G5')


K.st('ch10-st2', 'the Green Revolution in India: its causes, benefits and problems',
     terms=[('Green Revolution', 'the rapid increase in crop yields from the 1960s using high-yielding varieties, irrigation, fertilisers and pesticides'),
            ('high-yielding variety (HYV)', 'a crop variety bred to produce much larger harvests, such as dwarf wheat and IR8 rice'),
            ('Norman Borlaug', 'the US agronomist who developed dwarf wheat varieties in Mexico and won the 1970 Nobel Peace Prize'),
            ('M. S. Swaminathan', 'the Indian geneticist who led the introduction of HYV wheat in India in the 1960s'),
            ('tube well', 'a deep well using a pump to raise groundwater for irrigation'),
            ('minimum support price (MSP)', 'a guaranteed price at which the government buys crops such as wheat and rice from farmers')],
     facts=[('In which Indian states did the Green Revolution have its greatest early impact?', 'Punjab and Haryana', ['Kerala and Tamil Nadu', 'Assam and Meghalaya', 'Gujarat and Rajasthan'], 'They had irrigation and well-established farmers.'),
            ('Which crisis in the mid-1960s made India dependent on US food aid?', 'Two successive droughts in 1965 and 1966', ['The 1943 Bengal famine', 'The 1991 balance of payments crisis', 'The 2004 tsunami'], 'India imported millions of tonnes of wheat under PL-480.'),
            ('About how much did India\'s wheat production grow between 1965 and 1972?', 'It roughly doubled, from about 12 to 26 million tonnes', ['It fell by half', 'It rose by about 5%', 'It rose tenfold'], 'HYVs spread rapidly.'),
            ('Which rice variety, developed at the International Rice Research Institute in the Philippines in 1966, became known as "miracle rice"?', 'IR8', ['Basmati', 'Golden Rice', 'Arborio'], 'It doubled yields with irrigation and fertiliser.'),
            ('Which environmental problem has become severe in Punjab as a result of intensive irrigated agriculture?', 'Falling groundwater levels', ['Rising sea levels', 'Desertification by sand dunes', 'Volcanic activity'], 'Water tables have fallen sharply.')],
     why=[('Explain why India introduced the Green Revolution in the 1960s.', 'Droughts in 1965–66 caused food shortages and dependence on US food aid, and a fast-growing population needed more food, so the government promoted HYVs, irrigation and fertilisers to achieve self-sufficiency.'),
          ('Explain why the benefits of the Green Revolution were unequal.', 'HYVs needed irrigation, fertilisers and credit, so richer farmers in irrigated areas such as Punjab gained most, while poorer farmers and dry regions benefited less.'),
          ('Explain why the Green Revolution caused environmental problems.', 'Heavy use of fertilisers and pesticides polluted soils and water, monoculture reduced biodiversity, and tube-well irrigation lowered water tables and caused salinisation.'),
          ('Explain why the Green Revolution focused mainly on wheat and rice.', 'These were staple foods for most Indians and HYVs had been developed for them; government procurement at minimum support prices also encouraged farmers to grow them.')],
     contrast=[('traditional crop varieties', 'high-yielding varieties', 'Traditional varieties are hardier and need fewer inputs but yield less; HYVs give much higher yields but require irrigation, fertilisers and pesticides.'),
               ('the benefits of the Green Revolution', 'the problems of the Green Revolution', 'Benefits include food self-sufficiency and higher incomes; problems include inequality, debt, water depletion, soil degradation and loss of crop diversity.')],
     misc=[('The Green Revolution benefited all Indian farmers equally.', 'Gains were concentrated among larger farmers in irrigated regions; many smallholders and dry areas gained less.'),
           ('The Green Revolution increased production of all crops.', 'It mainly increased wheat and rice; pulses and coarse grains grew more slowly, and their share of farmland fell.'),
           ('The Green Revolution ended hunger in India.', 'It made India self-sufficient in grain, but malnutrition remains widespread because of poverty and unequal access to food.')],
     cases=[('Punjab\'s groundwater crisis', 'Free electricity and rice cultivation encouraged heavy pumping; the Central Ground Water Board has reported that most of Punjab\'s assessment blocks are over-exploited.', 'environmental costs of the Green Revolution', 'intensive irrigation raised yields but is depleting a vital resource.'),
            ('Borlaug\'s dwarf wheat in Mexico and India', 'Wheat varieties developed in Mexico were introduced to India and Pakistan in the mid-1960s; Pakistan\'s and India\'s wheat yields rose dramatically.', 'technology transfer', 'scientific research and international cooperation helped avert predicted famines.')],
     evaluate=[('The Green Revolution was a success for India.', ['wheat and rice production soared and India became self-sufficient in grain', 'it reduced the risk of famine and dependence on food aid'], ['benefits were unequal and many farmers fell into debt', 'it caused groundwater depletion, soil degradation and pollution'], 'It succeeded in its main aim of food self-sufficiency, but its social and environmental costs mean its success was partial and its model needs reform.')],
     src=[('Nobel lecture (paraphrased)', 'The speaker argued that the Green Revolution had won a temporary success in the war against hunger and had given humanity breathing space. He warned that unless the growth of population was brought under control, the gains would be only temporary.', 'Paraphrase of Norman Borlaug, Nobel Peace Prize lecture, Oslo, 11 December 1970', 'to explain the achievements of the Green Revolution and warn of continuing challenges', 'It is the key scientist\'s own view of the Green Revolution\'s achievements and limits.', 'Borlaug was its leading champion, so he says little about social and environmental problems.', 'The Green Revolution bought time against hunger, but population growth remained a challenge.')],
     rq=[('How has the Green Revolution affected groundwater levels in Punjab between 1970 and 2020?', 'Was the Green Revolution good?', 'it is a vague value question', 'It investigates a measurable environmental impact.', 'Use Central Ground Water Board data and two studies; graph water-table change; compare districts; evaluate sources; cite in APA.')])
C.pct_change(K, 'ch10-st2', [('India\'s wheat production', 'million tonnes', 1965, 12.3, 1972, 26.4, 'Government of India'),
                              ('India\'s food-grain production', 'million tonnes', 1966, 74, 2000, 197, 'approx., Government of India'),
                              ('wheat yield in India', 'tonnes per hectare', 1960, 0.85, 2020, 3.4, 'approx., FAO')], d=(1, 4))
C.rate_of_change(K, 'ch10-st2', [('India\'s food-grain production', 'million tonnes', [(1950, 51), (1970, 108), (1990, 176), (2010, 218), (2023, 330)], 'Government of India, approx.')])


K.st('ch10-st3', 'food security and food insecurity: causes and solutions',
     terms=[('food security', 'when all people at all times have physical and economic access to sufficient, safe and nutritious food (FAO, 1996)'),
            ('food insecurity', 'lack of regular access to enough safe and nutritious food'),
            ('famine', 'an extreme shortage of food in an area, leading to widespread hunger and deaths'),
            ('undernourishment', 'when a person\'s regular food intake is not enough to provide the energy needed for a healthy, active life'),
            ('Public Distribution System (PDS)', 'India\'s system of selling subsidised food grains through ration shops'),
            ('entitlement approach', 'Amartya Sen\'s idea that famines result from people losing the ability to obtain food, not only from a lack of food')],
     facts=[('According to the FAO, about how many people faced hunger in 2023?', 'About 733 million', ['About 73 million', 'About 7.3 billion', 'About 7 million'], 'Roughly one in eleven people.'),
            ('What are the four pillars of food security identified by the FAO?', 'Availability, access, utilisation and stability', ['Price, taste, packaging and branding', 'Wheat, rice, maize and soy', 'Land, labour, capital and enterprise'], 'Food must be available, accessible, well used and reliable over time.'),
            ('Which economist won the Nobel Prize partly for showing that the 1943 Bengal famine occurred without a major fall in food supply?', 'Amartya Sen', ['Norman Borlaug', 'Adam Smith', 'Muhammad Yunus'], 'Wages failed to keep up with rising food prices.'),
            ('Which 2013 Indian law entitles about two-thirds of the population to subsidised grain?', 'The National Food Security Act', ['The Right to Information Act', 'The Forest Rights Act', 'The Companies Act'], 'It gives 5 kg of grain per person per month.'),
            ('Which UN Sustainable Development Goal aims at "Zero Hunger" by 2030?', 'SDG 2', ['SDG 5', 'SDG 13', 'SDG 17'], 'The world is off track to meet it.')],
     why=[('Explain why food insecurity can occur even when there is enough food in a country.', 'People may lack money or land to obtain food, prices may rise faster than wages, or distribution may fail, as Amartya Sen showed for the 1943 Bengal famine.'),
          ('Explain why conflict is a major cause of food insecurity.', 'Fighting disrupts farming, destroys markets and infrastructure, displaces people and blocks aid, as in Sudan, Yemen and Gaza.'),
          ('Explain why climate change threatens food security.', 'More frequent droughts, floods and heatwaves reduce harvests, while changing rainfall and pests affect crops, hitting poor farmers hardest.'),
          ('Explain why food waste is relevant to food security.', 'About a third of food is lost or wasted globally; reducing waste would increase the food available without using more land or water.')],
     contrast=[('food availability', 'food access', 'Availability is whether enough food is produced or imported; access is whether people can afford or otherwise obtain it.'),
               ('chronic food insecurity', 'acute food insecurity', 'Chronic food insecurity is long-term inability to meet food needs; acute food insecurity is a sudden, severe shortage caused by shocks such as drought or war.')],
     misc=[('Famines are always caused by a lack of food.', 'Many famines, such as Bengal in 1943, happened when food was available but people could not afford it; politics and markets matter.'),
           ('Hunger is only a problem in poor countries.', 'Food insecurity also affects people in rich countries; millions use food banks in the UK and the US.'),
           ('Growing more food is the only solution to hunger.', 'Reducing poverty, waste and conflict, improving distribution and nutrition, and safety nets are also essential.')],
     cases=[('the 1943 Bengal famine', 'About 2–3 million people died; wartime inflation, the loss of rice imports from Burma and colonial policy priorities left many rural workers unable to buy food.', 'the entitlement approach', 'food was available, but many people lost the ability to obtain it.'),
            ('Ethiopia\'s Productive Safety Net Programme', 'Since 2005 the programme has provided food or cash to around 8 million people in exchange for public works, such as building terraces and roads.', 'a solution to chronic food insecurity', 'a safety net protects households from shocks while building local assets.')],
     evaluate=[('Poverty, rather than food shortage, is the main cause of food insecurity today.', ['the world produces enough calories for everyone', 'Sen showed famines often occur when food is available but unaffordable'], ['in conflict zones and droughts, local food shortages are real', 'climate change is reducing yields in vulnerable regions'], 'Poverty and access are the main causes globally, but conflict and climate shocks create real shortages; solutions must address both access and supply.')],
     src=[('UN report (paraphrased)', 'The report found that around 733 million people faced hunger in 2023, about one in eleven people worldwide and one in five in Africa. It concluded that the world was far off track to meet the goal of zero hunger by 2030 and identified conflict, climate extremes and economic downturns as the main drivers.', 'Paraphrase of FAO, IFAD, UNICEF, WFP and WHO, The State of Food Security and Nutrition in the World 2024', 'to monitor progress towards SDG 2 and inform policy', 'It is produced jointly by five UN agencies using global survey data.', 'Hunger estimates are modelled and less certain in conflict zones; it summarises global trends rather than local experience.', 'Hunger remains high, and conflict, climate and economic shocks are the main causes.')],
     rq=[('How effective has India\'s Public Distribution System been in reducing food insecurity in Odisha since 2013?', 'Why are people hungry?', 'it is too broad and has no focus', 'It evaluates a real food-security policy in a specific state.', 'Use National Family Health Survey data, NFSA reports and two studies; compare indicators; consider perspectives; evaluate sources; cite in APA.')])
C.pct_change(K, 'ch10-st3', [('the number of people facing hunger worldwide', 'million', 2019, 581, 2023, 733, 'FAO, SOFI 2024'),
                              ('the number of people using Trussell Trust food banks in the UK (emergency parcels)', 'million parcels', 2013, 0.9, 2023, 3.0, 'approx., Trussell Trust')], d=(1, 3))


@R.add('ch10-st3', ('C3', 'C4'), (1, 5), 'numerical')
def calories(rng, slot):
    fam = rng.choice([4, 5, 6, 7]); need = rng.choice([2100, 2200, 2300])
    kcal_kg = rng.choice([(3600, 'rice'), (3400, 'wheat flour'), (3650, 'maize')])
    days = rng.choice([7, 30])
    need_tot = fam * need * days
    kg = need_tot / kcal_kg[0]
    place = rng.choice(['Malawi', 'Bangladesh', 'Haiti', 'South Sudan', 'Nepal', 'Niger'])
    if slot.d <= 3:
        return dict(stem=f'A family of {fam} in {place} needs about {need} kcal per person per day. How many kilocalories does the family need over {days} days?',
                    answer=f'{need_tot:,} kcal', type='numerical', marks=2, markingKey=f'{fam} × {need} × {days} = {need_tot:,} kcal (M1 A1).', gap='G3')
    return dict(stem=(f'A food-aid agency calculates rations for a family of {fam} in {place} for {days} days. Each person needs {need} kcal per day and {kcal_kg[1]} provides about {kcal_kg[0]:,} kcal per kg. '
                      'Calculate how many kilograms of the staple would meet all the family\'s energy needs, and explain why this alone would not give food security.'),
                answer=f'{kg:.1f} kg', type='multi_step', marks=4,
                markingKey=f'Total need {fam} × {need} × {days} = {need_tot:,} kcal (M1); ÷ {kcal_kg[0]:,} (M1) = {kg:.1f} kg (A1). '
                           'R1: food security also needs nutritious, diverse food (protein, micronutrients), safe water and utilisation, and stable access over time.', gap='G5')

# =============================================================================================
# ch11 Money, Banking and Trade
# =============================================================================================
K.st('ch11-st1', 'the functions of money and the role of banks and credit',
     terms=[('money', 'anything generally accepted as payment for goods and services and settlement of debts'),
            ('medium of exchange', 'the function of money that allows goods to be bought and sold without barter'),
            ('store of value', 'the function of money that allows wealth to be saved for future use'),
            ('unit of account', 'the function of money as a common measure of the value of goods and services'),
            ('barter', 'exchanging goods or services directly for other goods or services without money'),
            ('credit', 'an arrangement to borrow money or obtain goods now and pay later, usually with interest'),
            ('collateral', 'an asset, such as land or a house, that a borrower pledges to a lender as security for a loan')],
     facts=[('What is the main problem with barter that money solves?', 'The need for a double coincidence of wants', ['Inflation', 'Interest rates', 'Exchange rates'], 'Each side must want what the other offers.'),
            ('Which Kenyan mobile-money service, launched in 2007, transformed access to financial services?', 'M-Pesa', ['PayPal', 'Visa', 'Alipay'], 'It lets users send money by mobile phone.'),
            ('Which bank, founded by Muhammad Yunus in Bangladesh, pioneered microcredit?', 'Grameen Bank', ['the World Bank', 'HSBC', 'the Reserve Bank of India'], 'Yunus and the bank shared the 2006 Nobel Peace Prize.'),
            ('Who controls the issue of currency notes in India?', 'The Reserve Bank of India', ['commercial banks', 'the Supreme Court', 'state governments'], 'The RBI is India\'s central bank.'),
            ('Why do banks pay interest on deposits?', 'To attract savings that they can lend to borrowers at a higher rate', ['Because the law forbids lending', 'To reduce their profits', 'To print more money'], 'The difference in rates is a source of bank profit.')],
     why=[('Explain why money is more efficient than barter.', 'Money removes the need for a double coincidence of wants, provides a common unit to compare values, is divisible and can be stored, making trade much easier.'),
          ('Explain why poor households often borrow from informal moneylenders.', 'They lack collateral, documents and nearby bank branches, so formal banks refuse them, while moneylenders lend quickly without paperwork, though at very high interest rates.'),
          ('Explain why access to credit can help people escape poverty.', 'Loans allow people to invest in tools, livestock, education or small businesses that raise their future income.'),
          ('Explain why credit can sometimes lead to a debt trap.', 'If interest rates are high or income falls, for example after a crop failure, borrowers may be unable to repay and must borrow more, so debt grows.')],
     contrast=[('formal credit', 'informal credit', 'Formal credit comes from banks and co-operatives regulated by the central bank, usually at lower interest; informal credit comes from moneylenders, traders or relatives, often at high interest and without regulation.'),
               ('a central bank', 'a commercial bank', 'A central bank, such as the Reserve Bank of India, issues currency and regulates banks; a commercial bank takes deposits and lends to households and businesses for profit.')],
     misc=[('Banks keep all the money that people deposit in their vaults.', 'Banks keep only a small fraction as reserves and lend most deposits to borrowers.'),
           ('Money has value because it is made of gold.', 'Modern money is fiat money; it has value because the government declares it legal tender and people trust it.'),
           ('Credit is always good for borrowers.', 'Credit helps when invested productively at fair rates, but high-interest debt can trap borrowers in poverty.')],
     cases=[('M-Pesa in Kenya', 'Launched by Safaricom in 2007, it reached tens of millions of users; a 2016 study in Science estimated it lifted about 2% of Kenyan households out of extreme poverty.', 'financial inclusion through technology', 'mobile money gave people without bank accounts a safe way to save and transfer money.'),
            ('Grameen Bank in Bangladesh', 'From 1976 Muhammad Yunus lent small sums to poor women in Jobra without collateral, using group lending; repayment rates were high.', 'microcredit', 'small loans without collateral allowed poor women to start businesses.')],
     evaluate=[('Microcredit is the most effective way to reduce poverty.', ['it gives poor people, especially women, access to capital without collateral', 'Grameen and others have reached millions of borrowers'], ['randomised studies found modest average effects on income', 'high interest rates and over-indebtedness have caused crises, as in Andhra Pradesh in 2010'], 'Microcredit helps some households but is not a cure-all; it works best alongside savings, insurance, education and wider development.')],
     src=[('Nobel lecture (paraphrased)', 'The speaker said that he had lent a small amount of his own money to 42 people in a village in 1976 to free them from moneylenders. He argued that poor people are creditworthy and that credit should be treated as a human right.', 'Paraphrase of Muhammad Yunus, Nobel Peace Prize lecture, Oslo, 10 December 2006', 'to explain the origins and philosophy of microcredit', 'It is the founder\'s first-hand account of how microcredit began.', 'As the founder he presents microcredit very positively and does not discuss its criticisms.', 'Poor people are creditworthy and credit can free them from moneylenders.')],
     rq=[('How has M-Pesa affected the savings of rural households in Kenya since 2007?', 'What is money?', 'it is a definition question', 'It investigates the impact of a financial innovation on development.', 'Read Suri and Jack (2016) and FinAccess survey data; compare urban and rural households; evaluate sources; cite in APA.')])
C.interest(K, 'ch11-st1')
C.exchange(K, 'ch11-st1', d=(1, 3))


K.st('ch11-st2', 'why countries trade: imports, exports and specialisation',
     terms=[('export', 'a good or service sold to another country'),
            ('import', 'a good or service bought from another country'),
            ('specialisation', 'concentrating on producing a limited range of goods or services'),
            ('absolute advantage', 'the ability of a country to produce more of a good than another country with the same resources'),
            ('comparative advantage', 'the ability to produce a good at a lower opportunity cost than another country'),
            ('balance of trade', 'the value of a country\'s exports of goods minus the value of its imports of goods'),
            ('tariff', 'a tax on imported goods')],
     facts=[('Who developed the theory of comparative advantage, using the example of England and Portugal trading cloth and wine?', 'David Ricardo', ['Adam Smith', 'Karl Marx', 'John Maynard Keynes'], 'In 1817.'),
            ('A country has a trade deficit when what happens?', 'The value of imports exceeds the value of exports', ['Exports exceed imports', 'It has no trade', 'It has a budget surplus'], 'It spends more abroad than it earns.'),
            ('Which international organisation, created in 1995, sets rules for world trade?', 'The World Trade Organization (WTO)', ['the IMF', 'UNESCO', 'NATO'], 'It replaced GATT.'),
            ('Which country was the world\'s largest exporter of goods in the 2020s?', 'China', ['India', 'Brazil', 'Nigeria'], 'It exported about US$ 3.4 trillion of goods in 2023.'),
            ('India is a major exporter of which type of service?', 'IT and software services', ['Fresh seafood only', 'Oil drilling', 'Satellite launches only'], 'Cities such as Bengaluru host major IT firms.')],
     why=[('Explain why countries specialise and trade.', 'Countries have different resources, climates and skills, so by specialising in goods they produce at a lower opportunity cost and trading, they can consume more than they could produce alone.'),
          ('Explain why trade can benefit consumers.', 'Consumers gain access to a wider choice of goods, often at lower prices, and competition from imports encourages domestic firms to improve quality.'),
          ('Explain why a country may still gain from trade even if another country is better at producing everything.', 'Gains depend on comparative, not absolute, advantage: each country benefits by specialising in what it gives up least to produce.'),
          ('Explain why governments sometimes impose tariffs.', 'Tariffs protect domestic industries and jobs from foreign competition, raise revenue and may be used in trade disputes, though they raise prices for consumers.')],
     contrast=[('absolute advantage', 'comparative advantage', 'Absolute advantage means producing more with the same resources; comparative advantage means producing at a lower opportunity cost.'),
               ('visible trade', 'invisible trade', 'Visible trade is trade in goods such as oil or rice; invisible trade is trade in services such as tourism, banking and IT.')],
     misc=[('A trade deficit always means a country is economically weak.', 'The United States has run trade deficits for decades while remaining the largest economy; deficits can reflect strong consumer demand and investment inflows.'),
           ('Trade only benefits the country with the absolute advantage.', 'Both trading partners can gain if they specialise according to comparative advantage.'),
           ('Imports always destroy domestic jobs.', 'Imports can cost jobs in some industries, but they also lower costs for businesses and consumers and support jobs in retail, logistics and export industries.')],
     cases=[('Bangladesh\'s garment industry', 'Using abundant low-cost labour, Bangladesh became the world\'s second-largest clothing exporter; garments make up over 80% of its exports.', 'specialisation based on comparative advantage', 'specialising in labour-intensive goods created millions of jobs, mainly for women, but also dependence on one industry.'),
            ('the US–China trade war', 'From 2018 the US and China imposed tariffs on hundreds of billions of dollars of each other\'s goods; studies found US consumers and firms bore most of the cost of US tariffs.', 'protectionism', 'tariffs aimed at protecting jobs raised prices and disrupted supply chains.')],
     evaluate=[('Free trade benefits all countries equally.', ['trade raises total output and gives consumers cheaper goods', 'export-led growth helped East Asian economies develop'], ['gains are unequal; some industries and workers lose', 'countries exporting raw materials may face falling prices and dependency'], 'Trade raises overall welfare, but gains are not equal; policies such as support for affected workers and diversification help spread the benefits.')],
     src=[('Economics text (paraphrased)', 'The author argued that England and Portugal would both gain if England specialised in cloth and Portugal in wine and they traded, even though Portugal could produce both goods with less labour than England.', 'Paraphrase of David Ricardo, On the Principles of Political Economy and Taxation, London, 1817', 'to argue against protectionist laws such as the Corn Laws', 'It is the founding statement of comparative advantage, explained with a clear example.', 'It is a simplified model that assumes full employment, no transport costs and no change in technology.', 'Both countries gain from specialising according to comparative advantage.')],
     rq=[('How has the growth of garment exports affected women\'s employment in Bangladesh since 1990?', 'Why do countries trade?', 'it is a general textbook question', 'It investigates the effects of specialisation in a real economy.', 'Use Bangladesh Bureau of Statistics and World Bank data, two studies and worker testimonies; graph trends; evaluate perspectives; cite in APA.')])
C.trade(K, 'ch11-st2')
C.pct_change(K, 'ch11-st2', [('Bangladesh\'s ready-made garment exports', 'US$ billion', 2000, 4.9, 2023, 47, 'approx., Export Promotion Bureau of Bangladesh'),
                              ('India\'s exports of services', 'US$ billion', 2005, 52, 2023, 340, 'approx., Reserve Bank of India')], d=(1, 4))


K.st('ch11-st3', 'fair trade and ethical consumption',
     terms=[('Fairtrade', 'a certification system guaranteeing producers a minimum price and a social premium, and requiring fair labour and environmental standards'),
            ('Fairtrade Minimum Price', 'the lowest price a buyer must pay producers for a certified product, providing a safety net when market prices fall'),
            ('Fairtrade Premium', 'an extra sum paid to producer co-operatives to invest in community or business projects'),
            ('ethical consumption', 'buying goods produced in ways that respect people, animals and the environment'),
            ('co-operative', 'a business owned and run by its members, who share the profits'),
            ('supply chain', 'the sequence of stages and businesses involved in producing and delivering a product to consumers')],
     facts=[('In which year was the first fair-trade label, Max Havelaar, launched in the Netherlands?', '1988', ['1948', '1968', '2008'], 'It was for coffee from Mexico.'),
            ('What is the Fairtrade Premium used for?', 'Community and business projects chosen by producers, such as schools or processing equipment', ['Advertising in supermarkets', 'Paying supermarket staff', 'Government taxes'], 'Producers decide democratically.'),
            ('Which product sells the most by volume under Fairtrade certification?', 'Bananas', ['Gold', 'Footballs', 'Roses'], 'Coffee and cocoa are also major Fairtrade products.'),
            ('Which 2013 factory collapse in Bangladesh, killing over 1,100 garment workers, increased pressure for ethical clothing?', 'Rana Plaza', ['Bhopal', 'Grenfell', 'Chernobyl'], 'It led to the Bangladesh Accord on building safety.'),
            ('About what share of the final price of a bar of milk chocolate typically reaches cocoa farmers?', 'About 6–7%', ['About 50%', 'About 90%', 'About 25%'], 'Most value goes to manufacturers and retailers.')],
     why=[('Explain why producers of crops like coffee need a minimum price.', 'World prices for commodities can fall sharply because of oversupply or speculation, so a guaranteed minimum protects farmers\' incomes from collapse.'),
          ('Explain why consumers may choose fair-trade products.', 'They want producers to receive a fair price and decent working conditions, and the label assures them that standards are checked.'),
          ('Explain why farmers receive only a small share of the final price of chocolate.', 'Manufacturing, branding, transport and retailing add most of the value, and powerful multinational firms have bargaining power over many small farmers.'),
          ('Explain why co-operatives help small farmers.', 'By joining together they can sell larger quantities, bargain for better prices, share equipment and access certification and credit.')],
     contrast=[('fair trade', 'free trade', 'Free trade removes barriers so prices are set by the market; fair trade aims to guarantee producers a fair price and decent conditions, even below market rates.'),
               ('ethical consumption', 'greenwashing', 'Ethical consumption is buying genuinely responsible products; greenwashing is when companies make misleading claims to appear ethical or environmentally friendly.')],
     misc=[('Fairtrade guarantees that all farmers escape poverty.', 'Studies show mixed results: Fairtrade can stabilise incomes, but many certified farmers remain poor because only part of their crop sells on Fairtrade terms.'),
           ('Fair-trade goods are always much more expensive.', 'The price difference for consumers is often small because the farmer\'s share is a small part of the final price.'),
           ('Ethical consumption is only about the environment.', 'It also covers workers\' rights, fair pay, animal welfare and community impacts.')],
     cases=[('Kuapa Kokoo in Ghana', 'A cocoa co-operative founded in 1993 with around 100,000 members; it co-owns the Divine Chocolate company and uses Fairtrade premiums for wells and schools.', 'fair trade and co-operatives', 'farmers gained a share of profits further up the supply chain.'),
            ('the Rana Plaza collapse', 'On 24 April 2013 a building housing garment factories near Dhaka collapsed, killing over 1,100 workers; global brands signed the Accord on Fire and Building Safety.', 'ethical consumption and supply chains', 'consumer and union pressure led brands to take more responsibility for working conditions.')],
     evaluate=[('Buying fair-trade products is the most effective way consumers can help producers in developing countries.', ['it guarantees minimum prices and funds community projects', 'it raises awareness of supply-chain inequality'], ['only a small share of trade is certified and benefits are uneven', 'changes in trade rules, wages and corporate practice may have bigger effects'], 'Fair trade helps some producers and raises awareness, but systemic changes in trade and corporate behaviour are needed for wider impact.')],
     src=[('Campaign report (paraphrased)', 'The report claimed that cocoa farmers in Côte d\'Ivoire and Ghana typically earned well below a living income, while chocolate companies and retailers captured most of the value of chocolate sales. It called on companies to pay higher prices and on governments to regulate supply chains.', 'Paraphrase of the Cocoa Barometer 2022, produced by a consortium of NGOs', 'to campaign for fairer pay and conditions in the cocoa industry', 'It brings together data from many studies on cocoa farmers\' incomes.', 'It is produced by campaign groups, so it emphasises problems and may give less weight to industry initiatives.', 'Cocoa farmers earn too little and most value goes to companies; reform is needed.')],
     rq=[('To what extent has Fairtrade certification increased the incomes of coffee farmers in Ethiopia since 2005?', 'Is fair trade good?', 'it is a vague value question', 'It evaluates fair trade with measurable outcomes in a real case.', 'Read two independent studies and Fairtrade reports; compare certified and uncertified farmers; consider price changes; evaluate sources; cite in APA.')])


@R.add('ch11-st3', ('C3', 'C4'), (1, 5), 'numerical')
def price_share(rng, slot):
    prod, unit, price, shares = rng.choice([
        ('a bar of chocolate', 'bar', [1.5, 2, 2.5, 3], [('cocoa farmers', 6.6), ('manufacturers', 35.2), ('retailers', 44.2), ('taxes and others', 14.0)]),
        ('a cup of coffee in a café', 'cup', [2.8, 3.2, 3.5, 4], [('coffee farmers', 1.5), ('café (staff, rent, milk)', 80), ('roasters and traders', 10.5), ('taxes', 8)]),
        ('a T-shirt', 'T-shirt', [10, 15, 20, 25], [('garment workers\' wages', 0.6), ('factory costs and profit', 12), ('brand and retailer', 72), ('transport and taxes', 15.4)]),
        ('a bunch of bananas', 'bunch', [1.2, 1.6, 2], [('plantation workers', 7), ('plantation owners', 11), ('importers and ripeners', 20), ('retailers', 42), ('shipping and taxes', 20)])])
    p = rng.choice(price)
    who, sh = shares[0]
    amt = p * sh / 100
    if slot.d <= 2:
        return dict(stem=f'{C.cap(prod)} sells for US$ {p:.2f}. If {who} receive {sh}% of the price, how much do they receive per {unit}?',
                    answer=f'US$ {amt:.3f}'.rstrip('0').rstrip('.') if amt < 0.1 else f'US$ {amt:.2f}', type='numerical', marks=2,
                    markingKey=f'{sh}% × {p:.2f} = {amt:.4f} → about US$ {amt:.2f} (M1 A1). Shares are approximate estimates from supply-chain studies.', gap='G3')
    prem = rng.choice([5, 10, 20])
    new = sh * (1 + prem / 100)
    return dict(stem=(f'Supply-chain studies suggest {who} receive about {sh}% of the US$ {p:.2f} price of {prod}. A fair-trade scheme raises the amount they receive per {unit} by {prem}%, '
                      'with the rest of the price unchanged. Calculate their new payment per unit and the new retail price, and evaluate whether this would make a large difference to consumers.'),
                answer=f'US$ {amt * (1 + prem / 100):.3f} per {unit}; new price US$ {p + amt * prem / 100:.3f}', type='multi_step', marks=5,
                markingKey=(f'Current payment {sh}% × {p:.2f} = US$ {amt:.4f} (M1); × {1 + prem / 100:.2f} = US$ {amt * (1 + prem / 100):.4f} (A1); '
                            f'extra US$ {amt * prem / 100:.4f}, so new price US$ {p + amt * prem / 100:.4f} (M1 A1). '
                            'Evaluation (R1): the price rise is tiny for consumers, but a significant gain for producers; however only part of output may sell on fair-trade terms.'),
                gap='G5')

# =============================================================================================
# ch12 Inquiry Skills
# =============================================================================================
K.st('ch12-st1', 'formulating a research question and justifying its relevance (Criterion B)',
     terms=[('research question', 'a clear, focused question that guides an investigation and can be answered with evidence in the time available'),
            ('statement of inquiry', 'in the MYP, a statement linking a key concept, related concepts and a global context that frames a unit'),
            ('action plan', 'a step-by-step plan for an investigation, including tasks, sources and a timeline'),
            ('relevance', 'why a research question matters, for example its connection to a concept, a global issue or a community'),
            ('scope', 'the limits of an investigation, such as the place, period and aspects studied'),
            ('hypothesis', 'a testable prediction about what an investigation will find')],
     facts=[('Which MYP Individuals and Societies criterion assesses formulating a research question and following an action plan?', 'Criterion B: Investigating', ['Criterion A: Knowing and understanding', 'Criterion C: Communicating', 'Criterion D: Thinking critically'], 'B covers the inquiry process.'),
            ('Which of these is the best research question?', 'How did the 2015 Gorkha earthquake affect tourism in Kathmandu between 2015 and 2019?', ['What are earthquakes?', 'Is Nepal nice?', 'Why do bad things happen?'], 'It is focused, researchable and has a place and period.'),
            ('What does "justify the relevance" of a research question mean?', 'Explain why the question is worth investigating and how it connects to concepts or global issues', ['List the sources used', 'Write the conclusion', 'Count the words in the question'], 'Relevance links the inquiry to wider significance.'),
            ('Which feature makes a research question too broad?', 'It has no limits of place, time or aspect', ['It names a specific place', 'It sets a time period', 'It uses a command term such as "to what extent"'], 'Narrow scope makes a question manageable.'),
            ('Which part of an MYP unit links a key concept, related concepts and a global context?', 'The statement of inquiry', ['The bibliography', 'The action plan', 'The reflection'], 'It frames the unit\'s inquiry.')],
     why=[('Explain why a research question should be focused.', 'A focused question can be answered in depth with the time and sources available, leading to a clearer argument and analysis.'),
          ('Explain why researchers write an action plan.', 'It organises tasks, sources and deadlines, ensures the investigation is manageable, and allows progress to be checked and adjusted.'),
          ('Explain why a good research question is open rather than closed.', 'An open question ("how", "why", "to what extent") requires analysis and evidence, while a closed question can be answered with yes/no or a single fact.'),
          ('Explain why researchers reflect on and revise their research question.', 'Early research may show that a question is too broad, lacks sources or has already been answered, so refining it improves the investigation.')],
     contrast=[('an open research question', 'a closed research question', 'An open question requires analysis and explanation; a closed question can be answered with a single fact or yes/no.'),
               ('a research question', 'a hypothesis', 'A research question asks what will be investigated; a hypothesis predicts what the answer might be and can be tested.')],
     misc=[('A broad question is better because there is more to write about.', 'Broad questions lead to superficial descriptions; focused questions allow depth and analysis.'),
           ('Once written, a research question cannot be changed.', 'Researchers often refine their question as they find sources; recording these changes shows good investigating skills.'),
           ('Justifying relevance means saying you find the topic interesting.', 'Relevance must explain the question\'s significance, for example its links to concepts, a global context or real-world issues.')],
     cases=[('a student inquiry into Mumbai\'s floods', 'A student began with "Why does it flood?" and refined it to "How did the destruction of mangroves contribute to flooding in Mumbai in July 2005?"', 'refining a research question', 'adding place, time and a specific factor made the question focused and researchable.'),
            ('a community inquiry into plastic waste', 'Students investigated how much single-use plastic their school used in a week, surveying canteens and classrooms before proposing changes.', 'relevance to the local community', 'a locally relevant question allowed primary data collection and action.')],
     evaluate=[('A good research question is the most important part of an investigation.', ['it shapes the sources, methods and argument', 'a vague question leads to a weak investigation'], ['the quality of sources and analysis also matter', 'a good question can still be undermined by poor planning'], 'A strong research question is the foundation, but an investigation also depends on effective planning, sources and critical analysis.')],
     src=[('Research guide (paraphrased)', 'The guide advised students to begin with a broad topic, read widely, and then narrow their focus to a question that is clear, focused, complex and arguable. It suggested testing a question by asking whether it can be answered with the available sources in the time allowed.', 'Paraphrase of a university library guide to developing research questions, 2023', 'to help students write effective research questions', 'It gives practical, clear criteria used by experienced researchers.', 'It is general advice for university students and is not specific to MYP Individuals and Societies.', 'Narrow a topic to a clear, focused, arguable and researchable question.')],
     rq=[('How did the 2015 Gorkha earthquake affect tourist arrivals in Nepal between 2015 and 2019?', 'What are earthquakes?', 'it is a definition question', 'It links a hazard to economic impacts using measurable data.', 'Collect Nepal Tourism Statistics; read two reports; graph arrivals; consider other factors; evaluate sources; cite in APA.'),
         ('To what extent did the Delhi Metro reduce traffic congestion in Delhi between 2002 and 2020?', 'Are trains good?', 'it is a vague value question', 'It evaluates an urban transport policy with evidence.', 'Use DMRC ridership data, traffic studies and news reports; compare before and after; evaluate; cite in APA.'),
         ('How has the Chipko movement influenced forest policy in Uttarakhand since 1973?', 'What is Chipko?', 'it is a definition question', 'It investigates the impact of a civil society movement.', 'Read accounts by activists and historians; compare policies; evaluate perspectives; cite in MLA.')])
C.sampling(K, 'ch12-st1')


K.st('ch12-st2', 'using a range of primary and secondary sources and citing them in MLA and APA format',
     terms=[('primary source', 'a source created at the time being studied or by a direct participant, such as a diary, photograph, speech or survey data you collect'),
            ('secondary source', 'a source that interprets or analyses primary sources, such as a textbook or history book'),
            ('bibliography', 'an alphabetical list of all sources used in an investigation'),
            ('in-text citation', 'a short reference in the text, such as (Sen, 1981), pointing to a full entry in the bibliography'),
            ('MLA format', 'the Modern Language Association citation style, often used in history and humanities, with author–page in-text citations'),
            ('APA format', 'the American Psychological Association style, often used in social sciences, with author–date in-text citations'),
            ('plagiarism', 'presenting someone else\'s words or ideas as your own without acknowledgement')],
     facts=[('Which of these is a primary source for studying the Partition of India?', 'A 1947 newspaper report from Lahore', ['A 2015 history textbook', 'A documentary made in 2017', 'An encyclopedia article'], 'It was created at the time.'),
            ('In APA style, which details appear in an in-text citation?', 'The author\'s surname and the year of publication', ['The title and page only', 'The publisher and city', 'The ISBN'], 'For example (Yunus, 2006).'),
            ('In MLA style, how is a book usually cited in the text?', 'By the author\'s surname and page number, e.g. (Tinker 45)', ['By the year only', 'By the title only', 'By the publisher'], 'MLA uses author–page.'),
            ('Which is the best reason to use a range of sources?', 'To compare perspectives and check the reliability of evidence', ['To make the bibliography longer', 'To avoid writing a conclusion', 'Because one source is always enough'], 'Corroboration strengthens conclusions.'),
            ('Which of these is a secondary source?', 'A historian\'s book about the Green Revolution', ['Borlaug\'s 1970 Nobel lecture', 'A 1968 photograph of a Punjab farm', 'Census data from 1971'], 'It interprets the past.')],
     why=[('Explain why researchers cite their sources.', 'Citations acknowledge others\' work, avoid plagiarism, let readers check the evidence and show the range and quality of research.'),
          ('Explain why using both primary and secondary sources strengthens an investigation.', 'Primary sources give first-hand evidence from the time, while secondary sources provide context and expert interpretation; together they allow evidence to be checked and analysed.'),
          ('Explain why websites must be checked carefully before use.', 'Anyone can publish online, so the author, date, purpose and evidence must be checked to judge reliability.'),
          ('Explain why a citation style must be used consistently.', 'Consistency makes references clear and easy to follow and shows academic honesty and accuracy.')],
     contrast=[('a primary source', 'a secondary source', 'A primary source comes from the time or a direct participant; a secondary source is a later interpretation of primary sources.'),
               ('MLA in-text citation', 'APA in-text citation', 'MLA gives the author and page number (Sen 45); APA gives the author and year (Sen, 1981).')],
     misc=[('Primary sources are always more reliable than secondary sources.', 'Primary sources can be biased or limited; secondary sources by experts may be more balanced. Reliability depends on origin and purpose.'),
           ('You only need to cite direct quotations.', 'Paraphrased ideas, data, images and statistics must also be cited.'),
           ('Wikipedia can be cited as an authoritative source in any investigation.', 'It can be a starting point, but researchers should check and cite the original sources it references.')],
     cases=[('the 1947 Partition Archive', 'Founded in 2010, the archive has recorded over 10,000 oral histories of people who lived through Partition.', 'creating primary sources', 'oral histories give voice to people missing from official records.'),
            ('Gapminder data', 'The Gapminder Foundation, founded by Hans Rosling, publishes free data on income, health and population for every country, drawing on the UN and World Bank.', 'using secondary data sets', 'reliable compiled data allows students to analyse global trends.')],
     evaluate=[('Primary sources are more valuable than secondary sources for historical investigation.', ['they provide direct evidence from the time', 'they reveal the views of participants'], ['they can be biased, incomplete or hard to interpret without context', 'secondary sources offer expert analysis of many primary sources'], 'Primary sources are essential evidence, but secondary sources provide context and interpretation; the most valuable investigations use both critically.')],
     src=[('Style guide (paraphrased)', 'The guide explained that every in-text citation must match an entry in the reference list, which should be arranged alphabetically by author surname and include the author, date, title and source so that readers can find the work.', 'Paraphrase of the Publication Manual of the American Psychological Association, 7th edition, 2020', 'to set standards for academic writing and citation', 'It is the official guide to APA style.', 'It focuses on format, not on judging the quality of sources.', 'In-text citations must match full, alphabetically ordered references.')],
     rq=[('How do primary accounts of the 1943 Bengal famine differ from official British reports?', 'What was the Bengal famine?', 'it is a descriptive question', 'It compares sources and perspectives, developing source skills.', 'Collect memoirs, newspaper reports and official documents; compare using OPVL; read two historians; cite in MLA.')])
C.citation(K, 'ch12-st2')


K.st('ch12-st3', 'thinking critically: analysing sources for origin, purpose, value and limitation (Criterion D)',
     terms=[('OPVL', 'a method for analysing sources by their origin, purpose, value and limitation'),
            ('origin', 'who created a source, when, where and in what form'),
            ('purpose', 'why a source was created and for which audience'),
            ('value', 'how a source is useful for a particular investigation'),
            ('limitation', 'what reduces a source\'s usefulness, such as bias, missing information or a narrow perspective'),
            ('corroboration', 'checking evidence by comparing it with other independent sources'),
            ('perspective', 'a particular point of view shaped by a person\'s position, experience or interests')],
     facts=[('Which MYP Individuals and Societies criterion assesses analysing sources and evaluating perspectives?', 'Criterion D: Thinking critically', ['Criterion A', 'Criterion B', 'Criterion C'], 'D covers analysis, synthesis and evaluation.'),
            ('A speech by a politician during an election campaign is most likely to be limited by what?', 'Its purpose of persuading voters, which may exaggerate', ['Its length', 'The fact that it is a primary source', 'Its date'], 'Purpose shapes content.'),
            ('Which question helps identify a source\'s purpose?', 'Why was it created and for whom?', ['How many pages does it have?', 'What colour is it?', 'Where is it stored now?'], 'Purpose concerns intent and audience.'),
            ('What does corroboration mean?', 'Checking a source against other independent evidence', ['Copying a source', 'Ignoring a source', 'Translating a source'], 'It tests reliability.'),
            ('A government report on its own policy may be limited because of what?', 'It may present the policy positively', ['It is always false', 'It cannot contain data', 'It is a secondary source'], 'Consider the creator\'s interests.')],
     why=[('Explain why the origin of a source affects its value.', 'Who created it, when and where determines what they could know: an eyewitness has direct knowledge, while someone writing later may have more perspective but less first-hand detail.'),
          ('Explain why a biased source can still be valuable.', 'A biased source reveals the attitudes and arguments of its creator, which is useful when investigating perspectives, propaganda or public opinion.'),
          ('Explain why historians compare several sources.', 'Comparing sources allows evidence to be corroborated, contradictions to be identified and a more balanced conclusion to be reached.'),
          ('Explain why the usefulness of a source depends on the question being asked.', 'A source may be very useful for one question, such as attitudes at the time, but limited for another, such as accurate statistics.')],
     contrast=[('value', 'limitation', 'Value is how a source is useful for a specific question; limitation is what reduces its usefulness, such as bias or narrow scope.'),
               ('reliability', 'usefulness', 'Reliability is how accurate and trustworthy a source is; usefulness depends on whether it helps answer the question, which even an unreliable source may do.')],
     misc=[('A primary source is always reliable because the author was there.', 'Eyewitnesses may have limited views, faulty memory or reasons to distort what happened.'),
           ('A biased source is useless.', 'Biased sources can be valuable evidence of perspectives and attitudes.'),
           ('OPVL means summarising what a source says.', 'OPVL analyses where a source comes from and why, and judges its value and limitations for a question, not just its content.')],
     cases=[('the photograph "Raising the Flag on Iwo Jima"', 'Joe Rosenthal\'s 1945 photograph showed US marines raising a second, larger flag; some later wrongly claimed it was staged, and it was widely used to promote war bonds.', 'analysing visual sources', 'a source\'s context and use can differ from what it appears to show.'),
            ('wartime posters', 'Governments in the First and Second World Wars produced posters to recruit soldiers and encourage rationing.', 'propaganda as evidence', 'posters reveal government aims and messages rather than how people actually felt.')],
     evaluate=[('Sources produced by governments are less reliable than those produced by individuals.', ['governments may present their policies positively or use propaganda', 'individual accounts can reveal hidden experiences'], ['governments often hold the most complete data, such as censuses', 'individuals may also be biased, mistaken or limited in view'], 'Reliability depends on the origin, purpose and content of each source, not simply on whether it comes from a government or an individual.')],
     src=[('Poster (described)', 'A colour poster shows a confident woman in a red-and-white headscarf flexing her arm, under the slogan "We Can Do It!". It was produced for a US company\'s factories to boost workers\' morale during the Second World War.', 'J. Howard Miller, poster for Westinghouse Electric, United States, 1943', 'to motivate factory workers and maintain production during the war', 'It shows how employers encouraged women\'s war work and how women workers were portrayed.', 'It was displayed only briefly within one company at the time; its fame as a feminist symbol dates from the 1980s, so it shows intent rather than workers\' experiences.', 'Women workers were capable and essential to the war effort.')],
     rq=[('How useful are wartime posters for understanding women\'s experiences in American factories during the Second World War?', 'What is a poster?', 'it is a definition question', 'It develops critical evaluation of sources for a historical question.', 'Collect posters, oral histories and employment data; apply OPVL; compare; reach a judgement; cite in MLA.')])
C.pct_change(K, 'ch12-st3', [('the number of women in the US labour force', 'million', 1940, 12, 1945, 18.6, 'approx., US Bureau of Labor Statistics')], d=(1, 3))


K.st('ch12-st4', 'communicating information in structured essays, reports and presentations (Criterion C)',
     terms=[('PEEL paragraph', 'a paragraph structure: Point, Evidence, Explanation, Link'),
            ('thesis statement', 'a sentence stating the main argument of an essay'),
            ('report', 'a structured document with headings that presents findings, data and recommendations'),
            ('annotation', 'a label or note added to a map, graph or image to explain features'),
            ('audience', 'the people a piece of communication is intended for'),
            ('format', 'the type of communication, such as an essay, report, poster, presentation or podcast')],
     facts=[('Which MYP Individuals and Societies criterion assesses communicating information and documenting sources?', 'Criterion C: Communicating', ['Criterion A', 'Criterion B', 'Criterion D'], 'C covers style, structure and referencing.'),
            ('Which type of graph is best for showing how a value changes over time?', 'A line graph', ['A pie chart', 'A scatter graph only', 'A Venn diagram'], 'Lines show trends.'),
            ('What should the introduction of an argumentative essay include?', 'Context and a clear thesis statement', ['Only the conclusion', 'All the evidence', 'The bibliography'], 'It sets out the argument.'),
            ('Which graph is best for showing parts of a whole, such as the share of energy sources?', 'A pie chart', ['A line graph', 'A climate graph', 'A cross-section'], 'Sectors show proportions.'),
            ('Which feature helps a reader navigate a report?', 'Clear headings and sub-headings', ['Very long paragraphs', 'No page numbers', 'Unlabelled graphs'], 'Structure aids clarity.')],
     why=[('Explain why the PEEL structure improves paragraphs.', 'It makes each paragraph focus on one point, supported by evidence, explained clearly and linked back to the question, so arguments are logical and easy to follow.'),
          ('Explain why communication should be adapted to the audience.', 'Different audiences have different knowledge and needs; language, detail and format must suit them so the message is understood.'),
          ('Explain why graphs must have titles, labels and units.', 'Without them, readers cannot tell what the data show, so the evidence cannot be interpreted or trusted.'),
          ('Explain why a conclusion should not introduce new evidence.', 'The conclusion answers the question by summarising and weighing the arguments already made; new evidence would need its own analysis.')],
     contrast=[('an essay', 'a report', 'An essay develops an argument in continuous paragraphs; a report presents findings under headings, often with data, and may include recommendations.'),
               ('describing', 'explaining', 'Describing says what something is like or what happened; explaining gives reasons or causes, showing why or how.')],
     misc=[('A longer answer always gets more marks.', 'Marks reward relevant, well-organised and supported points; padding can weaken an answer.'),
           ('A conclusion simply repeats the introduction.', 'A good conclusion weighs the arguments and gives a reasoned judgement that answers the question.'),
           ('Presentations do not need references.', 'Sources used in presentations must also be acknowledged, for example on slides and in a final reference list.')],
     cases=[('Hans Rosling\'s TED talks', 'Rosling used animated bubble charts to show changes in income and health across countries, making global data engaging for wide audiences.', 'effective data communication', 'well-chosen visuals and clear narration made complex data accessible.'),
            ('the IPCC "Summary for Policymakers"', 'IPCC assessments include a short summary in plain language with key figures, written for governments rather than scientists.', 'adapting communication to an audience', 'the same research is presented differently for different readers.')],
     evaluate=[('Visual presentations are more effective than written essays for communicating ideas in Individuals and Societies.', ['visuals make data and patterns easy to see', 'presentations can engage wide audiences'], ['essays allow detailed, nuanced argument and evaluation', 'visuals can oversimplify or mislead'], 'Each format has strengths; the most effective choice depends on the purpose and audience, and many good investigations combine both.')],
     src=[('Speech (paraphrased)', 'The speaker argued that many people hold an outdated view of the world, believing that most countries are poor and have large families. Using animated data on income and life expectancy, he showed that most countries had moved to the middle.', 'Paraphrase of Hans Rosling, TED talk "The best stats you\'ve ever seen", Monterey, California, 2006', 'to challenge misconceptions about global development using data', 'It shows a powerful way of communicating data to a general audience.', 'As a talk designed to engage, it simplifies data and focuses on positive trends.', 'The world has developed more than many people think.')],
     rq=[('How can climate data for Mumbai be presented most effectively to explain monsoon flooding risks to residents?', 'What is the monsoon?', 'it is a definition question', 'It focuses on communication choices for a real audience.', 'Collect IMD data; draw climate graphs; design an annotated map and leaflet; test with peers; evaluate; cite in APA.')])
C.graph_choice(K, 'ch12-st4')
C.citation(K, 'ch12-st4', c='C3', d=(2, 3))
