"""Cambridge International A Level Sociology 9699 (A2 content, grade 12).

Paper 3 Education (structured questions, including source/data items and 'evaluate' questions) and
Paper 4 Globalisation, Media and Religion (essays). Items use 9699 command words, named sociologists
and perspectives, research methods applied to these topics, simple data (percentages, rates, ratios)
and level-marked evaluation. Built with the knowledge-pack builders of the AS module (g11_sociology).
"""
from ._lib import mcq
from .g11_sociology import (T, build, classify, assemble, ctxd, fill, _pc, cap, _reg)  # noqa: F401

PROFILE = {'mark_scale': {'long': (1.5, 1.5), 'case': (1.5, 1.5)}, 'wordy': True}
CHAPTERS = {}


# ============================================================== EDUCATION (chapters 1-7)

VE = {
    'Functionalism': 'education performs vital functions for society: it passes on shared values and creates social solidarity (Durkheim), acts as a bridge from particularistic family values to universalistic values of wider society, and allocates people to roles on the basis of merit (Parsons, Davis and Moore).',
    'Marxism': 'education reproduces class inequality and legitimates it: the hidden curriculum prepares working-class pupils for subordinate jobs (Bowles and Gintis), schools act as ideological state apparatuses (Althusser), and the myth of meritocracy makes failure seem the individual’s fault.',
    'Interactionism': 'what happens inside schools matters: teachers’ labels, setting and streaming and pupils’ responses (subcultures) shape achievement through self-fulfilling prophecies (Becker, Rist, Keddie).',
    'Liberal feminism': 'education has helped reduce gender inequality through equal opportunities policies, but stereotyping, subject choice and the hidden curriculum still steer girls and boys in different directions.',
    'New Right': 'state education is inefficient and does not meet the needs of the economy; competition, parental choice and a market in schools will raise standards (Chubb and Moe), while education should transmit a shared national culture.',
}
VE_IN = dict(VE)
VE_IN['Marxism'] = 'achievement differences reflect class inequality: working-class pupils face material disadvantage and a middle-class school culture that rewards cultural capital, so schools reproduce rather than reduce inequality (Bourdieu, Bowles and Gintis).'

e1a = T('Functionalist views: socialisation, role allocation and meritocracy')
build(e1a, {
    'terms': [
        ('meritocracy', 'a system in which rewards and positions are allocated on the basis of ability and effort rather than social background', 'the best-qualified candidate getting the job regardless of class'),
        ('role allocation', 'the function of education in sifting and sorting pupils into the occupational roles that best suit their abilities', 'exams determining who enters medicine or engineering'),
        ('social solidarity', 'the sense of belonging to a society and commitment to its shared values', 'pupils learning national history and celebrating national days'),
        ('universalistic values', 'values and rules that apply equally to everyone, regardless of who they are', 'all pupils sitting the same exam marked to the same standard'),
        ('particularistic values', 'values and rules that apply only to a particular individual, often found in the family', 'parents treating a child as special because it is theirs'),
        ('specialist skills', 'the particular knowledge and skills needed for the many different jobs in a complex division of labour', 'vocational courses training pupils as electricians or nurses'),
        ('human capital', 'the knowledge, skills and qualifications of the workforce that make it productive', 'a highly educated workforce attracting investment'),
    ],
    'thinkers': [
        ('Durkheim', 'education transmits society’s shared values and creates social solidarity', 'Functionalism',
         'Durkheim argued that teaching a society’s history and values makes children feel part of something bigger; schools are “society in miniature”, teaching specialist skills and cooperation with others.',
         'Marxists argue the values transmitted are those of the ruling class, not of society as a whole.'),
        ('Parsons', 'school acts as a bridge between the family and wider society', 'Functionalism',
         'Parsons argued schools move children from particularistic family standards to universalistic standards and ascribed status to achieved status, and that school is meritocratic.',
         'Evidence of class, ethnic and gender differences in achievement suggests education is not meritocratic.'),
        ('Davis and Moore', 'education sifts and sorts people so the most able fill the most functionally important jobs', 'Functionalism',
         'Davis and Moore argued inequality is necessary to motivate the most talented to train for important roles; education is the proving ground for ability.',
         'Tumin argued it is hard to measure functional importance and that inequality prevents talent from emerging.'),
    ],
    'explain': [
        ('Explain two functions of education identified by functionalists.', 'Creating social solidarity by transmitting shared values (Durkheim); teaching specialist skills for the division of labour; acting as a bridge from particularistic to universalistic values (Parsons); role allocation on the basis of merit (Davis and Moore); developing human capital.', '2 marks for each explained function. [4]'),
        ('Explain why functionalists see education as meritocratic.', 'Everyone has an equal opportunity and is judged by the same universalistic standards; rewards (qualifications, jobs) are based on ability and effort; achieved status replaces ascribed status (Parsons).', '1 mark each developed point up to 3. [3]'),
        ('Explain one criticism of the functionalist view that education is meritocratic.', 'Evidence shows achievement varies by class, gender and ethnicity, so background matters; Marxists call meritocracy a myth that legitimates inequality; private schools and cultural capital give advantages; interactionists show labelling affects outcomes.', '1 mark identifying; 2 marks explaining with evidence. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of the functionalist view of education', ['education is not meritocratic: class, gender and ethnicity affect achievement', 'Marxists argue it transmits ruling-class values rather than shared values', 'interactionists argue it ignores what happens inside schools', 'qualifications do not always match jobs (credentialism)', 'it assumes pupils passively accept school values, ignoring anti-school subcultures']),
    ],
    'claims': [
        ('Parsons argued that school judges pupils by particularistic standards.', False, 'Parsons argued school judges pupils by universalistic standards, unlike the family.'),
        ('Durkheim saw school as “society in miniature”.', True, 'School teaches cooperation and rules that prepare pupils for life in wider society.'),
        ('Davis and Moore saw role allocation as a key function of education.', True, 'They argued education sifts and sorts pupils so the most able fill the most important jobs.'),
    ],
    'ar': ([('Functionalists see education as meritocratic.', 'they believe rewards are based on ability and effort rather than background.'),
            ('Durkheim emphasised the teaching of history.', 'shared history creates a sense of belonging and social solidarity.')],
           ['Parsons argued that education replaces achieved status with ascribed status.', 'Davis and Moore argued that inequality has no function in society.']),
    'scen': ['In {city}, every pupil sits the same national exam, and places at the best universities go to those with the highest marks.',
             'A school in {city} begins each day with an assembly about the country’s history and its national heroes.',
             'The government in {city} expands vocational colleges to train technicians for its growing electronics industry.'],
    'views': VE,
    'ctx': [('how far pupils in {city} believe that school is fair', {'young', 'meaning', 'large'}),
            ('the relationship between qualifications and occupation', {'large', 'change'})],
    'data': [dict(what='qualifications and occupation', pop='adults aged 30-40', rows=['Degree', 'Upper secondary only', 'Lower secondary or less'], cols=('Professional/managerial job', 'Routine/manual job'), cmp=True, nocount=True,
                  base=[(60, 70), (25, 40), (8, 18)], delta=[(-55, -45), (5, 15), (40, 60)], label='percentage in each type of occupation',
                  expl=['functionalists see this as role allocation: the most qualified fill the most important jobs', 'Marxists argue qualifications themselves reflect class background, so education legitimates inherited inequality',
                        'credentialism means employers demand higher qualifications for jobs'],
                  method='questionnaire', claim='education allocates people to occupations on the basis of merit',
                  counter='The data show a link between qualifications and jobs, but not whether qualifications reflect ability or class background; Bourdieu and Bowles and Gintis argue the system favours the middle class.')],
    'essays': [('Explain two functions that education performs for society according to functionalists.', 'Social solidarity and shared values (Durkheim); specialist skills; bridge between family and society (Parsons); meritocracy and role allocation (Davis and Moore); human capital.',
                'education is meritocratic',
                'Functionalists: equal opportunities, universalistic standards, achieved status (Parsons); role allocation (Davis and Moore); expansion of education and rising attainment.',
                'Marxists: myth of meritocracy (Bowles and Gintis); class, gender and ethnic gaps; cultural capital (Bourdieu); private schooling; labelling (Becker); social mobility remains limited.')],
})

e1b = T('Marxist views: correspondence theory, reproduction and legitimation')
build(e1b, {
    'terms': [
        ('correspondence principle', 'Bowles and Gintis’s idea that the relationships and structures of school mirror those of the workplace', 'obeying teachers mirrors obeying managers'),
        ('hidden curriculum', 'the unofficial norms, values and attitudes taught through the organisation and routines of school', 'punctuality, obedience and acceptance of hierarchy'),
        ('reproduction of class inequality', 'the process by which education passes class advantages and disadvantages from one generation to the next', 'middle-class children gaining the qualifications for middle-class jobs'),
        ('legitimation', 'making inequality appear fair and justified', 'the myth that failure is due to lack of effort'),
        ('myth of meritocracy', 'the Marxist idea that the belief that education is fair hides how it reproduces class inequality', 'working-class pupils blaming themselves for low grades'),
        ('ideological state apparatus', 'Althusser’s term for institutions such as education that maintain ruling-class power by spreading ideology', 'schools teaching acceptance of capitalism'),
        ('counter-school culture', 'a pupil subculture that rejects the values and rules of the school', 'Willis’s “lads” who “had a laff” and rejected school work'),
    ],
    'thinkers': [
        ('Bowles and Gintis', 'school prepares pupils for the workplace through a hidden curriculum that corresponds to work', 'Marxism',
         'Their study of 237 New York pupils found schools rewarded conformity and obedience rather than creativity; the correspondence principle and the myth of meritocracy legitimate inequality.',
         'Willis showed pupils can resist the hidden curriculum; the correspondence principle is less clear in modern, flexible workplaces.'),
        ('Althusser', 'education is the most important ideological state apparatus in capitalist society', 'Neo-Marxism',
         'Althusser argued schools reproduce labour power and the ideology that justifies capitalism.',
         'It is deterministic and ignores resistance and teachers who challenge capitalism.'),
        ('Willis', 'working-class lads’ counter-school culture prepared them for manual work', 'Neo-Marxism',
         'Willis’s study of 12 “lads” found they rejected school, valued “having a laff”, and so ended up in manual jobs; their resistance helped reproduce class inequality.',
         'The sample was small; later research found more varied working-class responses.'),
        ('Bourdieu', 'education reproduces class inequality because it values the cultural capital of the middle class', 'Neo-Marxism',
         'Bourdieu argued middle-class children’s habitus and cultural capital fit school expectations, so their success appears to be merit.',
         'Critics argue cultural capital is vague and working-class pupils can succeed.'),
    ],
    'explain': [
        ('Explain what Bowles and Gintis mean by the correspondence principle.', 'The structure of school mirrors that of work: hierarchy of head and teachers mirrors managers; extrinsic rewards (grades) mirror wages; fragmented subjects mirror fragmented work; obedience is rewarded in both.', '1 mark definition; 1 mark each developed example up to 2. [3]'),
        ('Explain two ways in which, according to Marxists, education legitimates class inequality.', 'Myth of meritocracy: success and failure are presented as fair; qualifications appear to reflect ability; failure is blamed on the individual; ideology through the curriculum presents capitalism as natural.', '2 marks for each explained way. [4]'),
        ('Explain one way in which Willis’s research challenges the correspondence principle.', 'Willis showed working-class pupils actively resisted the hidden curriculum through a counter-school culture, rather than passively accepting it; ironically their resistance still led to manual jobs.', '1 mark identifying resistance; 2 marks explaining its significance. [3]'),
    ],
    'why': [
        ('feature', 'features', 'of the hidden curriculum identified by Marxists', ['acceptance of hierarchy and authority', 'punctuality and obedience to rules', 'motivation by external rewards such as grades', 'acceptance of boring, fragmented work', 'competition between pupils']),
    ],
    'claims': [
        ('Bowles and Gintis argued that schools reward creativity and independence.', False, 'They found schools rewarded conformity and obedience, and penalised creativity.'),
        ('Marxists see the idea of meritocracy as a myth.', True, 'They argue it hides how education reproduces class inequality and legitimates it.'),
        ('Willis found that the lads accepted the school’s values.', False, 'The lads rejected school values and formed a counter-school culture.'),
    ],
    'ar': ([('Marxists argue that education reproduces class inequality.', 'middle-class pupils gain qualifications for middle-class jobs while working-class pupils are prepared for subordinate roles.'),
            ('Willis’s lads failed at school.', 'their counter-school culture rejected academic work.')],
           ['Bowles and Gintis argued school rewards those who challenge authority.', 'Althusser saw education as a repressive state apparatus.']),
    'scen': ['In a school in {city}, pupils are given merit points for being on time, wearing the correct uniform and not questioning teachers.',
             'A group of working-class boys in {city} mock pupils who work hard, skip lessons and say they will “get a job in the factory anyway”.'],
    'views': VE,
    'ctx': [('the hidden curriculum in secondary schools', {'young', 'behaviour', 'meaning'}),
            ('anti-school subcultures among working-class boys', {'young', 'hidden', 'meaning'})],
    'source': [dict(text='A researcher observed lessons in four secondary schools in {city} over a term. Pupils who sat quietly, followed instructions and handed work in on time received the highest grades for “effort”, even when their work was less original than that of pupils who questioned the teacher.',
                    method='non-participant observation', about='the hidden curriculum', finds=['quiet, obedient pupils received the highest effort grades', 'original pupils who questioned the teacher were rated lower'],
                    persp='Marxism', pview='The findings support the correspondence principle: schools reward obedience and conformity, preparing pupils to be compliant workers (Bowles and Gintis).',
                    claim='the main role of education is to reproduce a compliant workforce', pro='The source shows conformity being rewarded; Bowles and Gintis and Althusser argue education serves capitalism.',
                    con='Functionalists see education as meritocratic and teaching shared values; Willis shows pupils resist; modern workplaces require creativity; four schools may be untypical and observation may affect teachers’ behaviour.', flags={'young', 'behaviour'})],
    'essays': [('Explain two ways in which education reproduces class inequality according to Marxists.', 'Hidden curriculum and correspondence principle (Bowles and Gintis); ideology (Althusser); cultural capital (Bourdieu); myth of meritocracy; counter-school culture leading to manual work (Willis).',
                'the main function of education is to reproduce and legitimate class inequality',
                'Bowles and Gintis: correspondence principle, myth of meritocracy; Althusser: ISA; Bourdieu: cultural capital; evidence of persistent class gaps in achievement.',
                'Functionalists: meritocracy, social solidarity, role allocation; Willis: resistance; feminists: gender inequality is also reproduced; rising working-class attainment; postmodernists: education is diverse and responds to a post-Fordist economy.')],
})

e1c = T('Feminist and interactionist views of education')
build(e1c, {
    'terms': [
        ('gender stereotyping', 'expecting people to behave in particular ways because of their gender', 'assuming boys are better at physics'),
        ('hidden curriculum (gender)', 'the unofficial messages about gender roles conveyed through school organisation, teacher attention and resources', 'boys dominating classroom discussion and playground space'),
        ('labelling', 'attaching a definition to a pupil, such as “bright” or “troublemaker”, which affects how they are treated', 'a teacher seeing a pupil as “not academic”'),
        ('self-fulfilling prophecy', 'a prediction that comes true because people act on it', 'a pupil labelled weak who stops trying'),
        ('ideal pupil', 'Becker’s term for the kind of pupil teachers prefer, often based on middle-class norms of behaviour and appearance', 'a polite, neat, hard-working pupil'),
        ('patriarchal curriculum', 'a curriculum that marginalises women’s contributions and reflects male perspectives', 'history lessons focusing mainly on male leaders'),
        ('speculation', 'Hargreaves’s first stage of typing, in which teachers make guesses about pupils', 'a teacher forming an impression in the first lesson'),
    ],
    'thinkers': [
        ('Becker', 'teachers judge pupils against an image of the “ideal pupil”', 'Interactionism',
         'Becker interviewed 60 Chicago teachers and found they labelled middle-class pupils as closest to the ideal pupil and working-class pupils as furthest from it.',
         'Labelling theory can be deterministic: not all labelled pupils fulfil the prophecy.'),
        ('Hargreaves', 'teachers type pupils through stages of speculation, elaboration and stabilisation', 'Interactionism',
         'Hargreaves, Hester and Mellor showed how teachers’ initial impressions harden into fixed labels over time.',
         'It focuses on classrooms and neglects wider structures such as class and inequality.'),
        ('Spender', 'boys dominate classroom interaction and receive more teacher attention', 'Radical feminism',
         'Spender found boys talked more and teachers gave them more attention, while girls’ contributions were marginalised; the curriculum was “man-made”.',
         'Girls now outperform boys in many countries, suggesting the hidden curriculum has changed.'),
        ('Kelly', 'science is presented as a masculine subject through textbooks, examples and classroom dynamics', 'Liberal feminism',
         'Kelly argued that boys dominated science lessons and examples drew on boys’ interests, which discouraged girls.',
         'Policy initiatives have since increased girls’ participation in science.'),
    ],
    'explain': [
        ('Explain how labelling by teachers may affect pupils’ achievement.', 'Teachers label pupils (e.g. bright or troublesome) often on the basis of class, gender or ethnicity; pupils are treated accordingly (setting, attention, expectations); pupils internalise the label and a self-fulfilling prophecy results.', '1 mark each stage developed up to 3. [3]'),
        ('Explain two ways in which feminists argue education reinforces gender inequality.', 'Gendered subject choice and careers advice; hidden curriculum of teacher attention and stereotyping (Spender); patriarchal curriculum marginalising women; sexual harassment and policing of girls’ behaviour; male-dominated leadership.', '2 marks for each explained way. [4]'),
        ('Explain one criticism of interactionist explanations of educational achievement.', 'They ignore wider structural factors such as material deprivation and class inequality; labelling theory can be deterministic; pupils can reject labels (Fuller); studies are small-scale.', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which pupils may respond to negative labels', ['accepting the label and underachieving (self-fulfilling prophecy)', 'forming anti-school subcultures', 'rejecting the label and working harder to prove teachers wrong', 'withdrawing or truanting']),
    ],
    'claims': [
        ('Interactionists explain achievement mainly by material deprivation.', False, 'Interactionists focus on processes inside schools such as labelling and self-fulfilling prophecies.'),
        ('Becker found that teachers judged pupils against an ideal pupil.', True, 'The ideal pupil often matched middle-class norms.'),
        ('Liberal feminists believe gender equality in education has been fully achieved.', False, 'They recognise progress but argue stereotyping and subject choice still create inequality.'),
    ],
    'ar': ([('Labelling can lead to a self-fulfilling prophecy.', 'pupils may internalise teachers’ expectations and act in line with them.'),
            ('Feminists criticise the hidden curriculum.', 'it can transmit messages that men and boys are more important.')],
           ['Becker found teachers saw working-class pupils as closest to the ideal pupil.', 'interactionists argue labels have no effect on pupils’ self-concept.']),
    'scen': ['In a school in {city}, teachers say girls are “naturally good at languages” and boys are “natural scientists”, and careers advisers suggest nursing to girls and engineering to boys.',
             'In the first week at a new school in {city}, {person} is described by a teacher as “one to watch”; a year later {person} is in the bottom set and has stopped trying.'],
    'views': {'Interactionism': VE['Interactionism'], 'Liberal feminism': VE['Liberal feminism'],
              'Radical feminism': 'education remains patriarchal: boys dominate classrooms, the curriculum marginalises women and girls experience sexual harassment, so schools reproduce male power (Spender).',
              'Marxism': VE['Marxism']},
    'ctx': [('teacher-pupil interaction in mixed-sex classrooms', {'young', 'behaviour'}),
            ('how pupils respond to teachers’ labels', {'young', 'meaning', 'sensitive'})],
    'essays': [('Explain two ways in which teachers’ labelling may affect pupils’ education.', 'Ideal pupil (Becker); self-fulfilling prophecy (Rosenthal and Jacobson); setting and streaming based on labels; speculation-elaboration-stabilisation (Hargreaves); subcultures in response.',
                'interactionist explanations of educational achievement are more useful than structural explanations',
                'Labelling and self-fulfilling prophecy (Becker, Rist, Rosenthal and Jacobson); subcultures (Lacey); shows how inequality is produced in classrooms; allows teachers to change outcomes.',
                'Ignores material deprivation and cultural capital; deterministic; pupils resist labels (Fuller); Marxists link labels to wider class structure; small-scale studies.')],
}, VE)

e1d = T('Neoliberal and New Right views of education')
build(e1d, {
    'terms': [
        ('New Right', 'a political perspective that favours free markets, competition and a limited role for the state', 'policies giving parents a choice of school'),
        ('neoliberalism', 'an economic doctrine that the state should not provide services and that markets and competition produce efficiency', 'turning schools into competing, self-managing units'),
        ('marketisation', 'the introduction of market forces of consumer choice and competition into education', 'publishing league tables so parents can compare schools'),
        ('parentocracy', 'rule by parents: the idea that parents, as consumers, gain power over schools through choice', 'parents choosing schools based on results'),
        ('league tables', 'published rankings of schools based on exam results and other performance measures', 'a newspaper listing schools by percentage of top grades'),
        ('formula funding', 'funding schools according to the number of pupils they attract', 'a popular school receiving more money'),
        ('national culture', 'a shared set of values and history that the New Right believes education should transmit', 'a curriculum emphasising national history and language'),
    ],
    'thinkers': [
        ('Chubb and Moe', 'state schools have failed and should be replaced by a market system of competing schools', 'New Right',
         'Chubb and Moe compared state and private schools in the USA and found pupils from low-income families did about 5% better in private schools; they proposed vouchers.',
         'Critics argue private schools have advantages of selection and resources, so the comparison is unfair.'),
        ('Ball', 'marketisation creates a myth of parentocracy that favours middle-class parents', 'Neo-Marxism',
         'Ball argued choice and competition reproduce class inequality because middle-class parents have more resources to use choice.',
         'Supporters argue choice has raised standards for many schools.'),
        ('Gewirtz', 'parents differ in their ability to exercise school choice: privileged-skilled, semi-skilled and disconnected choosers', 'Neo-Marxism',
         'Gewirtz’s study of 14 London schools showed middle-class parents used economic, social and cultural capital to secure places at the best schools.',
         'It was based on London and may not apply everywhere.'),
    ],
    'explain': [
        ('Explain two features of the New Right view of education.', 'State education is inefficient and unresponsive; competition and parental choice raise standards; schools should be run like businesses; education should serve the economy; it should transmit a shared national culture.', '2 marks for each explained feature. [4]'),
        ('Explain how marketisation may reproduce class inequality in education.', 'Middle-class parents have more economic and cultural capital to use choice (Gewirtz, Ball); league tables encourage schools to select able pupils (cream-skimming) and avoid weaker ones (silt-shifting); funding follows pupils, so popular schools gain resources and unpopular ones decline.', '1 mark each developed point up to 3. [3]'),
        ('Explain one similarity and one difference between New Right and functionalist views of education.', 'Similarity: both see education as meritocratic, preparing people for work and transmitting shared values. Difference: the New Right argues state schools fail and markets are needed, while functionalists see state education as already performing these functions.', '2 marks for each explained point. [4]'),
    ],
    'why': [
        ('policy', 'policies', 'associated with the marketisation of education', ['publishing league tables', 'formula funding based on pupil numbers', 'open enrolment and parental choice', 'school inspections', 'academies and independent state-funded schools', 'competition for pupils']),
    ],
    'claims': [
        ('The New Right believes the state should run all schools centrally.', False, 'The New Right favours markets, competition and parental choice over state control.'),
        ('Gewirtz found that middle-class parents were better able to use school choice.', True, 'Privileged-skilled choosers used their capital to secure places at the best schools.'),
        ('Neoliberals argue competition between schools raises standards.', True, 'Like businesses, schools must improve to attract “customers” (parents).'),
    ],
    'ar': ([('The New Right supports parental choice.', 'it believes competition between schools will raise standards.'),
            ('Critics argue marketisation increases inequality.', 'middle-class parents have more resources to exercise choice.')],
           ['the New Right argues that the state should increase its control over schools.', 'Chubb and Moe argued that state schools perform better than private schools.']),
    'scen': ['The government in {city} publishes school league tables and allows parents to apply to any school; popular schools fill up quickly with pupils from nearby wealthy areas.',
             'A school in {city} that slips down the league tables loses pupils, and therefore funding, and has to cut teaching staff.'],
    'views': {'New Right': VE['New Right'], 'Neoliberalism': 'education should be run as a market: schools compete for pupils, parents act as consumers and the state’s role is minimal; this raises efficiency and standards.',
              'Marxism': 'marketisation reproduces class inequality behind a myth of parentocracy: middle-class parents use their capital to secure the best schools (Ball, Gewirtz).',
              'Functionalism': 'education should allocate roles meritocratically and serve the economy; competition may be functional if it raises standards, but it should not undermine equal opportunity.'},
    'ctx': [('how parents choose secondary schools in {city}', {'meaning', 'large'}),
            ('the effects of league tables on schools', {'change', 'large', 'behaviour'})],
    'data': [dict(what='school choice', pop='parents', rows=['Professional/managerial parents', 'Routine/manual parents'], cols=('2010', '2025'),
                  base=[(70, 80), (45, 55)], delta=[(0, 6), (-6, 4)], label='percentage of parents whose child got a place at their first-choice school',
                  expl=['middle-class parents have more economic, social and cultural capital to use choice (Gewirtz)', 'they can afford to move near popular schools (selection by mortgage)',
                        'schools may “cream-skim” pupils likely to boost league table results'],
                  method='official statistics', claim='parental choice benefits all parents equally',
                  counter='Most parents in both groups get a first choice; differences may reflect where families live; choice may still raise standards overall as the New Right claims.')],
    'essays': [('Explain two reasons why the New Right supports the marketisation of education.', 'Competition raises standards; parental choice and accountability; efficiency and less bureaucracy; meeting the needs of the economy; consumer power (parentocracy).',
                'marketisation has improved education for all pupils',
                'Competition and choice raise standards; league tables give accountability; rising results overall; Chubb and Moe on private-style schools.',
                'Ball and Gewirtz: middle-class advantage, myth of parentocracy; cream-skimming and silt-shifting; polarisation between schools; teaching to the test; inequality persists.')],
})

CHAPTERS[1] = [e1a, e1b, e1c, e1d]


e2a = T('Education and the economy: human capital and vocational education')
build(e2a, {
    'terms': [
        ('human capital', 'the knowledge, skills and qualifications of workers that increase their productivity', 'engineers trained at university'),
        ('vocational education', 'education and training designed to prepare people for particular jobs or occupations', 'courses in plumbing, nursing or hospitality'),
        ('credentialism', 'the growing demand by employers for qualifications, even for jobs that do not require them', 'a degree being required for an administrative job'),
        ('post-Fordism', 'a flexible system of production requiring a skilled, adaptable workforce', 'workers trained to perform several roles'),
        ('skills gap', 'a mismatch between the skills workers have and those employers need', 'a shortage of computer programmers'),
        ('knowledge economy', 'an economy in which growth depends mainly on information, skills and innovation', 'a country focused on software and research'),
        ('apprenticeship', 'a training scheme combining work with study, leading to a recognised qualification', 'a young person training as an electrician while working'),
    ],
    'thinkers': [
        ('Schultz', 'spending on education is an investment in human capital that increases economic growth', 'Functionalism',
         'Schultz argued that educated workers are more productive, so investment in education brings economic returns to individuals and societies.',
         'Critics argue qualifications may signal status rather than skills (credentialism).'),
        ('Finn', 'vocational training schemes provide cheap labour and keep unemployment figures down', 'Marxism',
         'Finn argued youth training schemes served employers and governments more than young people, offering little real skill.',
         'Supporters argue vocational routes give practical skills and progression for many young people.'),
        ('Cohen', 'vocational education teaches attitudes and values needed by employers rather than real skills', 'Marxism',
         'Cohen argued youth training aimed to create good attitudes and work discipline among working-class youth.',
         'Some schemes do lead to skilled employment.'),
        ('Collins', 'rising qualification requirements reflect credentialism rather than the real skills needed for jobs', 'Weberian theory',
         'Collins argued that groups use credentials to protect access to occupations and status, leading to qualification inflation.',
         'Some jobs genuinely require higher technical skills.'),
    ],
    'explain': [
        ('Explain two ways in which education may contribute to economic growth.', 'Developing human capital (skills and knowledge); training for specific occupations (vocational education); research and innovation; teaching work-related attitudes; role allocation of the most able to key jobs.', '2 marks for each explained way. [4]'),
        ('Explain why Marxists criticise vocational education.', 'It channels working-class pupils into low-status, low-paid routes; it teaches compliant attitudes rather than real skills (Cohen); training schemes provide cheap labour and hide unemployment (Finn); it reproduces class inequality.', '1 mark each developed point up to 3. [3]'),
        ('Explain what is meant by credentialism and one consequence of it.', 'Credentialism is the growing demand for qualifications beyond what jobs require; consequences include qualification inflation, over-education and graduates in non-graduate jobs, and disadvantage for those without credentials.', '1 mark definition; 2 marks explained consequence. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of vocational education', ['it often has lower status than academic routes', 'it may channel working-class pupils into low-paid jobs', 'training schemes may provide cheap labour rather than real skills', 'skills taught may quickly become outdated']),
    ],
    'claims': [
        ('Human capital theory sees education as an investment.', True, 'Educated workers are more productive, bringing returns to individuals and economies.'),
        ('Vocational qualifications always have higher status than academic qualifications.', False, 'In many societies vocational routes have lower status, which Marxists link to class inequality.'),
        ('Credentialism means that jobs demand fewer qualifications over time.', False, 'It means employers demand more qualifications, often beyond what the job needs.'),
    ],
    'ar': ([('Governments invest heavily in education.', 'human capital theory links education to economic growth.'),
            ('Marxists criticise vocational training schemes.', 'they argue such schemes reproduce working-class disadvantage.')],
           ['credentialism means employers demand fewer qualifications.', 'human capital theory argues education has no economic value.']),
    'scen': ['The government in {city} launches a programme of apprenticeships for 16-year-olds in construction and hospitality, while university places are expanded for top students.',
             'In {city}, many graduates are working in call centres and shops, while employers complain of a shortage of skilled technicians.'],
    'views': {'Functionalism': 'education develops human capital and allocates people to roles, so it contributes to economic growth; vocational education provides specialist skills for the division of labour.',
              'Marxism': 'education serves capitalism by producing a disciplined workforce; vocational routes channel working-class youth into low-paid work and teach compliance (Finn, Cohen).',
              'New Right': 'education should be closely tied to the needs of the economy; vocational training and competition between providers make the workforce more productive.',
              'Weberian theory': 'qualifications are used by groups to protect status and access to jobs, so rising requirements reflect credentialism rather than economic need (Collins).'},
    'ctx': [('young people’s experiences of apprenticeships', {'young', 'meaning'}),
            ('the link between education and earnings', {'large', 'change'})],
    'data': [dict(what='education and earnings', pop='workers aged 25-64', rows=['Degree', 'Vocational qualification', 'No qualifications'], cols=('2005', '2025'), nocount=True, unit='', uname='index points',
                  base=[(150, 175), (100, 115), (65, 75)], delta=[(-15, 5), (-5, 10), (-5, 5)], label='median earnings index (all workers = 100)',
                  leads=['Official earnings data for {city} (sample of {n} workers) show the following.', 'The table shows median earnings by highest qualification for {n} workers in {city}.'],
                  expl=['human capital theory: more education brings higher productivity and earnings', 'credentialism: employers use degrees to screen applicants',
                        'falling graduate premium may reflect the expansion of higher education'],
                  method='official statistics', claim='education is a good investment in human capital',
                  counter='Earnings differences may reflect class background, networks and cultural capital as well as skills; graduate premiums may fall as more people gain degrees; not all graduates get graduate jobs.')],
    'essays': [('Explain two ways in which education serves the needs of the economy.', 'Human capital and productivity (Schultz); vocational training; role allocation (Davis and Moore); hidden curriculum of work discipline (Bowles and Gintis); research and innovation.',
                'vocational education benefits young people',
                'Practical skills and qualifications; routes into skilled work; meets employers’ needs; functionalist and New Right support.',
                'Marxists: cheap labour, low status, reproduces class inequality (Finn, Cohen); credentialism; academic routes still lead to better-paid jobs; gender stereotyping in vocational courses.')],
})

e2b = T('Marketisation, privatisation and parental choice')
build(e2b, {
    'terms': [
        ('privatisation', 'the transfer of public services or assets into the hands of private companies', 'private companies running state-funded schools'),
        ('marketisation', 'introducing competition, choice and business methods into education', 'schools competing for pupils using league tables'),
        ('cream-skimming', 'schools selecting the most able pupils, who are likely to improve their results', 'a popular school admitting high-attaining applicants'),
        ('silt-shifting', 'schools avoiding or offloading pupils with learning difficulties or behaviour problems', 'excluding pupils likely to lower results'),
        ('parentocracy', 'the idea that parents, as consumers, now control education through choice', 'parents choosing schools based on league tables'),
        ('selection by mortgage', 'gaining a place at a good school by buying a house in its catchment area', 'house prices rising near successful schools'),
        ('education as a commodity', 'the idea that education is something to be bought and sold for profit', 'private tutoring and test-preparation businesses'),
    ],
    'thinkers': [
        ('Ball', 'marketisation reproduces class inequality while presenting itself as fair', 'Neo-Marxism',
         'Ball argued parentocracy is a myth: the middle class benefit most from choice, and schools focus on attracting “desirable” pupils.',
         'Defenders argue choice gives all parents more say.'),
        ('Gewirtz', 'middle-class parents are “privileged-skilled choosers” with the capital to secure the best schools', 'Neo-Marxism',
         'Gewirtz classified parents as privileged-skilled, semi-skilled and disconnected local choosers, linked to their economic and cultural capital.',
         'The typology was based on a small sample of London parents.'),
        ('Bartlett', 'marketisation leads schools to cream-skim and silt-shift', 'Neo-Marxism',
         'Bartlett argued league tables encourage schools to recruit able pupils and avoid those likely to lower results, leading to polarisation.',
         'Some schools resist these pressures and focus on inclusion.'),
        ('Ball and Youdell', 'privatisation is turning education into a commodity bought and sold for profit', 'Neo-Marxism',
         'They argued private companies increasingly provide services such as testing, buildings and management, influencing what schools do.',
         'Private involvement may bring efficiency and investment.'),
    ],
    'explain': [
        ('Explain two ways in which marketisation may benefit middle-class pupils more than working-class pupils.', 'Middle-class parents have economic capital (selection by mortgage, transport, tutoring); cultural capital to understand admissions; social capital to get information; schools cream-skim desirable pupils.', '2 marks for each explained way. [4]'),
        ('Explain what is meant by cream-skimming and silt-shifting, and why schools may do them.', 'Cream-skimming: selecting high-achieving pupils; silt-shifting: avoiding or removing low-achieving or difficult pupils. Schools do so because league tables and formula funding reward high results and popularity.', '1 mark each definition; 1 mark reason linked to league tables/funding. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why privatisation of education has increased', ['governments seek efficiency and lower costs', 'neoliberal ideas favour private provision', 'private companies see education as a source of profit', 'globalisation of education businesses', 'demand for testing, tutoring and technology services']),
    ],
    'claims': [
        ('Parentocracy means all parents have equal power to choose schools.', False, 'Ball and Gewirtz argue choice favours middle-class parents with more capital; parentocracy is a myth.'),
        ('Formula funding gives more money to schools that attract more pupils.', True, 'Funding follows pupils, so popular schools gain resources.'),
        ('Silt-shifting means schools recruit the most able pupils.', False, 'That is cream-skimming; silt-shifting means avoiding pupils likely to lower results.'),
    ],
    'ar': ([('Popular schools can become more popular.', 'formula funding gives more resources to schools that attract more pupils.'),
            ('House prices are often higher near successful schools.', 'parents buy homes in catchment areas to secure places (selection by mortgage).')],
           ['marketisation reduces competition between schools.', 'cream-skimming means schools admit pupils with behaviour problems.']),
    'scen': ['In {city}, the best-performing state schools are surrounded by expensive housing, and their intake is mostly middle-class.',
             'A private company in {city} wins a contract to run testing and management services for a group of state schools.'],
    'views': {'New Right': VE['New Right'], 'Marxism': 'marketisation and privatisation turn education into a commodity and reproduce class inequality behind a myth of parentocracy (Ball, Gewirtz).',
              'Neoliberalism': 'competition and private providers make education more efficient and responsive to parents as consumers.',
              'Functionalism': 'education should allocate pupils meritocratically; if choice and competition raise standards they are functional, but unequal access threatens equality of opportunity.'},
    'ctx': [('how parents from different social classes choose schools', {'meaning', 'large'}),
            ('the involvement of private companies in state education', {'change', 'meaning'})],
    'data': [dict(what='school intake and league table position', pop='secondary schools', rows=['Top-third schools', 'Middle-third schools', 'Bottom-third schools'], cols=('2010', '2025'), n=[60, 90, 120, 150],
                  base=[(8, 14), (18, 25), (30, 40)], delta=[(-4, 0), (-2, 3), (2, 8)], label='percentage of pupils eligible for free school meals',
                  expl=['cream-skimming by popular schools concentrates disadvantaged pupils in less popular schools (Bartlett)', 'selection by mortgage means wealthier families live near top schools',
                        'middle-class parents are privileged-skilled choosers (Gewirtz)'],
                  method='official statistics', claim='marketisation has increased polarisation between schools',
                  counter='Differences may reflect housing patterns that existed before marketisation; schools in poorer areas may still improve; free school meal eligibility is only a rough measure of disadvantage.')],
    'essays': [('Explain two effects of marketisation on schools.', 'League tables and competition; cream-skimming and silt-shifting; polarisation; teaching to the test; spending on marketing; more choice for some parents; rising results.',
                'parental choice has increased inequality in education',
                'Ball and Gewirtz: middle-class privileged-skilled choosers; selection by mortgage; cream-skimming and silt-shifting (Bartlett); polarisation.',
                'New Right: choice raises standards for all; some working-class parents use choice effectively; policies such as free transport or lotteries reduce inequality; inequality existed before marketisation.')],
})

e2c = T('Education policy, globalisation and international comparisons')
build(e2c, {
    'terms': [
        ('international league tables', 'rankings comparing pupils’ performance in different countries, such as PISA', 'a country ranked 5th in mathematics'),
        ('PISA', 'the OECD’s Programme for International Student Assessment, which tests 15-year-olds in reading, mathematics and science in many countries', 'a three-yearly comparison of national results'),
        ('policy borrowing', 'adopting education policies from other countries that appear successful', 'copying another country’s approach to teaching mathematics'),
        ('global education industry', 'multinational businesses that sell education services such as testing, technology and textbooks across countries', 'a company running exams in over 100 countries'),
        ('equality of educational opportunity', 'the principle that every child should have the same chance to succeed in education', 'free schooling for all'),
        ('compensatory education', 'policies that give extra resources to disadvantaged pupils to make up for deprivation', 'extra funding for schools in poor areas'),
    ],
    'thinkers': [
        ('Ball', 'globalisation has led to a global education policy shaped by neoliberal ideas and international comparisons', 'Neo-Marxism',
         'Ball argued governments copy policies such as testing, accountability and privatisation, often promoted by international organisations and businesses.',
         'National policies still vary greatly according to local politics and culture.'),
        ('Alexander', 'international league tables can lead to simplistic policy borrowing', 'Interactionism',
         'Alexander argued that education systems are embedded in national culture, so copying policies from high-ranking countries may not work.',
         'Comparisons can still highlight effective practices.'),
    ],
    'explain': [
        ('Explain two ways in which globalisation has influenced education policy.', 'International league tables (PISA) create pressure to raise standards; policy borrowing between countries; global education businesses; emphasis on skills for a global knowledge economy; international qualifications and student migration.', '2 marks for each explained way. [4]'),
        ('Explain one problem with using international league tables to compare education systems.', 'Tests may not reflect what is valued in each country’s curriculum; samples and translation may affect results; cultural factors such as private tutoring affect scores; they encourage teaching to the test.', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why governments pay attention to international comparisons of education', ['they link education to economic competitiveness', 'poor rankings create political pressure', 'they may identify successful policies to borrow', 'international organisations such as the OECD promote them']),
    ],
    'claims': [
        ('PISA compares the performance of 15-year-olds in different countries.', True, 'It tests reading, mathematics and science every three years.'),
        ('Policies copied from high-performing countries always succeed elsewhere.', False, 'Education systems are shaped by culture and context, so borrowed policies may not work (Alexander).'),
    ],
    'ar': ([('Many governments monitor PISA results closely.', 'they see education as important for competing in the global economy.'),
            ('Policy borrowing can be problematic.', 'policies are shaped by the culture and context of the country where they developed.')],
           ['PISA tests only university students.', 'globalisation has had no influence on education policy.']),
    'scen': ['After falling in the PISA rankings, the government of {city} introduces longer school days and more testing, copying a high-ranking East Asian system.',
             'An international company sells the same digital learning platform to schools in {city} and in forty other countries.'],
    'views': {'Functionalism': 'international comparisons help societies improve their education systems and develop human capital for the global economy.',
              'Neoliberalism': 'global competition and comparisons drive standards up; markets and accountability spread good practice.',
              'Marxism': 'globalisation spreads neoliberal policies and the profits of global education businesses, increasing inequality and turning education into a commodity (Ball).',
              'Postmodernism': 'globalisation increases diversity and choice in education but also shows there is no single best system.'},
    'ctx': [('how teachers respond to international league tables', {'meaning', 'behaviour'}),
            ('differences in attainment between countries', {'large', 'change'})],
    'data': [dict(what='international test scores', pop='15-year-olds', rows=['Country A', 'Country B', 'Country C'], cols=('2012', '2022'), unit='', uname='points', nocount=True,
                  base=[(470, 490), (500, 520), (530, 560)], delta=[(-10, 15), (-15, 5), (-20, 5)], label='mean mathematics score (international average about 480)',
                  leads=['The table shows mean scores in an international mathematics test, based on samples of about {n} pupils per country.', '{person} found these international test results (samples of around {n} pupils in each country) while researching education policy.'],
                  expl=['countries with high scores often have high status for teachers and strong cultural emphasis on education', 'private tutoring and test preparation may raise scores',
                        'policy changes such as increased testing may affect results'],
                  method='official statistics', claim='international league tables give a valid measure of the quality of education systems',
                  counter='Tests measure a narrow range of skills; samples and translation affect comparability; cultural factors outside school influence results; small score differences may not be significant.')],
    'essays': [('Explain two effects of globalisation on education.', 'Policy borrowing; international league tables and accountability; global education businesses; international students and qualifications; curriculum emphasis on global skills.',
                'international comparisons are a useful guide for education policy',
                'They highlight effective practices; motivate improvement; allow governments to judge performance against competitors.',
                'Cultural context makes borrowing problematic (Alexander); tests are narrow; encourage teaching to the test; serve neoliberal agendas (Ball).')],
}, VE)

CHAPTERS[2] = [e2a, e2b, e2c]


e3a = T('Material deprivation and educational achievement')
build(e3a, {
    'terms': [
        ('material deprivation', 'lack of money and the physical necessities of life, such as adequate housing, food and resources', 'a family unable to afford a computer or a quiet place to study'),
        ('cost of free schooling', 'the hidden costs of education, such as uniforms, trips and equipment, which burden poorer families', 'pupils missing school trips because parents cannot pay'),
        ('relative poverty', 'having an income well below the average for the society, so that people cannot afford a normal standard of living', 'a household with less than 60% of median income'),
        ('fear of debt', 'reluctance to take on loans for higher education, more common among working-class students', 'a student choosing a local course to avoid student loans'),
        ('digital divide', 'the gap between those who have access to computers and the internet and those who do not', 'pupils without home internet struggling with online homework'),
        ('overcrowded housing', 'housing with too many people for the space available, which can affect health and study', 'three children sharing one bedroom'),
    ],
    'thinkers': [
        ('Howard', 'poorer pupils have lower intakes of energy, vitamins and minerals, which affects health and concentration', 'Functionalism',
         'Howard found young people from poorer homes had poorer diets, leading to more absence and difficulty concentrating.',
         'Diet is only one factor; schools can provide meals to reduce its effects.'),
        ('Flaherty', 'money problems are a significant factor in non-attendance at school', 'Marxism',
         'Flaherty found that the cost of uniforms, trips and equipment, and fear of being bullied for looking poor, led some pupils to miss school.',
         'Free school meals and support schemes reduce some costs.'),
        ('Reay', 'working-class students are more likely to apply to local universities to reduce costs', 'Neo-Marxism',
         'Reay found working-class students chose universities close to home, limiting their options, partly because of costs and fear of debt.',
         'Cultural factors and confidence also shape choices, not only money.'),
    ],
    'explain': [
        ('Explain two ways in which material deprivation may affect educational achievement.', 'Poor diet and health lead to absence and poor concentration (Howard); overcrowded housing gives no space to study; cost of free schooling (uniforms, trips) leads to stigma and absence (Flaherty); need to work part-time; fear of debt deters higher education.', '2 marks for each explained way. [4]'),
        ('Explain one criticism of material deprivation explanations of class differences in achievement.', 'Many poor pupils succeed, so deprivation is not the only cause; cultural factors (attitudes, cultural capital) and in-school factors (labelling) matter; policies providing resources have not closed gaps.', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('effect', 'effects', 'of housing conditions on pupils’ education', ['no quiet place to do homework', 'poor health from damp or cold housing', 'disrupted schooling from moving home often', 'tiredness from overcrowding']),
    ],
    'claims': [
        ('Material deprivation can affect pupils’ health and attendance.', True, 'Poor diet and housing lead to illness and absence (Howard).'),
        ('Free state education means that poverty has no effect on achievement.', False, 'Hidden costs such as uniforms, trips and equipment still affect poorer pupils (Flaherty).'),
    ],
    'ar': ([('Pupils from poor families may miss school more often.', 'poor diet and housing can cause illness.'),
            ('Working-class students may avoid distant universities.', 'they fear the debt and costs of living away from home.')],
           ['material deprivation only affects pupils in primary schools.', 'all pupils have equal access to computers at home.']),
    'scen': ['{person}, aged 14, lives with five family members in a two-room flat in {city}, often skips breakfast and has no computer at home.',
             'A secondary school in {city} finds that pupils eligible for free meals miss more school trips and have higher absence rates.'],
    'views': VE_IN,
    'ctx': [('the effects of poverty on pupils’ achievement', {'young', 'sensitive', 'large'}),
            ('working-class students’ decisions about university', {'meaning', 'young'})],
    'data': [dict(what='poverty and achievement', pop='pupils aged 16', rows=['Pupils eligible for free school meals', 'Other pupils'], cols=('2015', '2025'),
                  base=[(35, 45), (60, 70)], delta=[(-2, 8), (-2, 5)], label='percentage achieving five good passes at age 16',
                  leads=['National data for {city} ({n} pupils) show the following results.', 'The table shows exam results for {n} pupils in {city}, by eligibility for free school meals.'],
                  expl=['material deprivation affects diet, health, housing and access to resources', 'cultural capital differences between classes (Bourdieu)',
                        'labelling and setting may disadvantage poorer pupils'],
                  method='official statistics', claim='material deprivation is the main cause of class differences in achievement',
                  counter='Free school meal eligibility is only a rough measure of class; cultural and in-school factors also matter; some poor pupils achieve highly.')],
    'essays': [('Explain two ways in which material deprivation may affect educational achievement.', 'Diet and health; housing; cost of free schooling; part-time work; fear of debt; digital divide.',
                'material factors are more important than cultural factors in explaining class differences in achievement',
                'Howard, Flaherty, Reay show effects of poverty on health, attendance and choices; gaps persist for poorer pupils; cultural deprivation theory blames the victim.',
                'Cultural capital (Bourdieu), parental attitudes (Douglas), language codes (Bernstein); in-school factors (labelling); material and cultural factors interact; some poor pupils succeed.')],
})

e3b = T('Cultural deprivation and cultural capital (Bourdieu)')
build(e3b, {
    'terms': [
        ('cultural deprivation', 'the theory that some groups lack the norms, values, skills and knowledge needed for educational success', 'claims that working-class parents place less value on education'),
        ('cultural capital', 'Bourdieu’s term for the knowledge, attitudes, values, language and tastes that give advantages in education', 'familiarity with books, museums and academic language'),
        ('habitus', 'Bourdieu’s term for the dispositions, tastes and ways of thinking learnt through socialisation in a particular class', 'feeling “at home” in a university setting'),
        ('restricted code', 'Bernstein’s term for a speech code with limited vocabulary and context-bound meanings, associated with the working class', 'short sentences assuming shared understanding'),
        ('elaborated code', 'Bernstein’s term for a speech code with a wider vocabulary and context-free meanings, associated with the middle class and used in schools', 'detailed explanations that do not depend on context'),
        ('immediate gratification', 'seeking pleasure now rather than making sacrifices for future rewards, a value cultural deprivation theorists linked to the working class', 'leaving school early to earn money'),
        ('social capital', 'the networks and contacts that provide support and information', 'parents who know teachers or university staff'),
    ],
    'thinkers': [
        ('Bourdieu', 'middle-class pupils succeed because schools value the cultural capital they acquire at home', 'Neo-Marxism',
         'Bourdieu argued economic, cultural and educational capital can be converted into each other; the middle-class habitus is treated as the norm in school.',
         'Critics say cultural capital is hard to measure and many working-class pupils succeed.'),
        ('Bernstein', 'differences in speech codes between classes affect achievement', 'Neo-Marxism',
         'Bernstein argued schools use the elaborated code, giving middle-class children an advantage; he did not see the restricted code as inferior.',
         'Critics argue the codes are over-simplified and the theory has been misused to blame working-class families.'),
        ('Douglas', 'working-class parents placed less value on education and showed less interest in their children’s progress', 'Functionalism',
         'Douglas’s longitudinal study found children whose parents showed less interest (measured by parents’ evening attendance) did less well.',
         'Blackstone and Mortimore argued working-class parents may work longer or unsocial hours and feel uncomfortable in schools.'),
        ('Sullivan', 'pupils with more cultural capital did better in exams', 'Neo-Marxism',
         'Sullivan surveyed 465 pupils on reading, TV viewing and cultural activities; those with more cultural capital, mostly middle-class, achieved better results.',
         'Cultural capital only partly explained class differences; material resources also mattered.'),
    ],
    'explain': [
        ('Explain what Bourdieu meant by cultural capital and how it affects achievement.', 'Cultural capital is the knowledge, attitudes, language and tastes of the middle class; schools value these, so middle-class pupils fit in and succeed while working-class pupils are disadvantaged; success appears to be due to merit.', '1 mark definition; 1 mark link to school values; 1 mark effect on achievement/legitimation. [3]'),
        ('Explain two criticisms of cultural deprivation theory.', 'It blames the victim and ignores material deprivation; working-class culture is different, not deficient (Keddie); working-class parents value education but face practical barriers (Blackstone and Mortimore); it ignores school factors such as labelling.', '2 marks for each explained criticism. [4]'),
    ],
    'why': [
        ('way', 'ways', 'in which middle-class parents may use cultural capital to help their children', ['reading with children and discussing ideas', 'choosing successful schools through knowledge of the system', 'visiting museums and galleries', 'using educated language that matches school expectations', 'communicating confidently with teachers']),
    ],
    'claims': [
        ('Bourdieu argued that working-class culture is inferior.', False, 'He argued schools are biased towards middle-class culture; working-class culture is not valued by schools rather than inferior.'),
        ('Bernstein linked the elaborated code to the middle class.', True, 'He argued schools use the elaborated code, advantaging middle-class pupils.'),
        ('Cultural deprivation theory has been criticised for blaming the victim.', True, 'It locates the problem in working-class families rather than in the education system or inequality.'),
    ],
    'ar': ([('Middle-class pupils often feel at home in school.', 'their habitus matches the culture that schools value.'),
            ('Keddie criticised cultural deprivation theory.', 'she argued working-class culture is different rather than deficient.')],
           ['Bernstein argued that the restricted code is the language of schools.', 'Bourdieu argued that cultural capital cannot be converted into educational success.']),
    'scen': ['{woman}’s parents in {city}, both university lecturers, take her to museums, discuss news at dinner and help her choose challenging books.',
             'A working-class pupil in {city} says she feels “out of place” in lessons where teachers use long words and refer to books she has never read.'],
    'views': VE_IN,
    'ctx': [('the influence of parents’ cultural activities on children’s achievement', {'young', 'meaning', 'large'}),
            ('working-class pupils’ experiences of a high-achieving school', {'young', 'meaning', 'sensitive'})],
    'data': [dict(what='cultural capital and achievement', pop='pupils aged 15', rows=['Pupils who read for pleasure daily', 'Pupils who never read for pleasure'], cols=('Middle-class pupils', 'Working-class pupils'), cmp=True, nocount=True,
                  base=[(70, 80), (50, 62)], delta=[(-15, -5), (-15, -5)], label='percentage achieving high grades in an English exam',
                  expl=['reading for pleasure develops vocabulary and cultural capital valued by schools (Sullivan)', 'middle-class pupils may have more economic capital (books, tutors) as well as cultural capital',
                        'teachers may label middle-class pupils more favourably'],
                  method='questionnaire', claim='cultural capital explains class differences in achievement',
                  counter='Reading helps both classes, but class differences remain even among readers, suggesting material and school factors also matter; self-reported reading may be inaccurate.')],
    'source': [dict(text='A survey of 500 sixteen-year-olds in {city} asked about reading, visits to museums and the theatre, and the newspapers they read. Pupils whose parents were graduates scored higher on these activities and achieved better exam results. However, some working-class pupils with high scores on cultural activities also achieved top grades.',
                    method='questionnaire', about='cultural capital and achievement', finds=['pupils with graduate parents scored higher on cultural activities and achieved better results', 'some working-class pupils with high cultural activity scores achieved top grades'],
                    persp='Neo-Marxism', pview='The findings support Bourdieu: cultural capital, acquired mainly in middle-class families, is rewarded by schools and helps reproduce class inequality while appearing to reflect merit.',
                    claim='cultural capital is the main reason for class differences in achievement', pro='The source links cultural activities to achievement; Bourdieu and Sullivan argue cultural capital advantages the middle class.',
                    con='Material deprivation and school factors also matter; some working-class pupils succeed; questionnaires measure activities, not deeper habitus; correlation is not causation.', flags={'young', 'large'})],
    'essays': [('Explain two ways in which cultural factors may affect educational achievement.', 'Cultural capital and habitus (Bourdieu); speech codes (Bernstein); parental interest (Douglas); attitudes and values (immediate gratification); social capital and school choice.',
                'cultural capital is the most important factor in explaining class differences in educational achievement',
                'Bourdieu and Sullivan; middle-class habitus matches school; parents use cultural and social capital in school choice (Gewirtz).',
                'Material deprivation (Howard, Flaherty); labelling and in-school factors; concept is vague and hard to measure; working-class success stories.')],
})

e3c = T('In-school factors and class: labelling and the self-fulfilling prophecy')
build(e3c, {
    'terms': [
        ('labelling', 'attaching a meaning or definition to a person, such as “bright” or “troublemaker”', 'a teacher describing a pupil as “not university material”'),
        ('self-fulfilling prophecy', 'a prediction that comes true because people act on it', 'a pupil labelled as failing who gives up'),
        ('setting', 'grouping pupils by ability for particular subjects', 'a pupil in the top set for maths but the middle set for English'),
        ('streaming', 'grouping pupils by ability for all subjects', 'a pupil placed in the “C stream” for everything'),
        ('educational triage', 'sorting pupils into those who will pass anyway, those who can be helped to pass and hopeless cases', 'extra help for pupils on the grade borderline'),
        ('ideal pupil', 'the image of the perfect pupil that teachers use to judge pupils, often based on middle-class norms', 'a polite, neat, motivated pupil'),
    ],
    'thinkers': [
        ('Rist', 'teachers separate pupils into groups based on class-related judgements from the first days of school', 'Interactionism',
         'Rist found a kindergarten teacher seated pupils at “tigers”, “cardinals” and “clowns” tables based on appearance and background; tigers (middle-class) got more attention.',
         'It was a single classroom study in the USA.'),
        ('Rosenthal and Jacobson', 'teachers’ expectations can produce a self-fulfilling prophecy in pupils’ achievement', 'Interactionism',
         'In their field experiment, randomly selected “spurters” made greater IQ gains, apparently because teachers expected more of them.',
         'Replication attempts have produced mixed results, and the study involved deception.'),
        ('Gillborn and Youdell', 'educational triage leads teachers to focus on pupils likely to raise school results', 'Neo-Marxism',
         'They argued league table pressures lead schools to ration attention, so working-class and black pupils labelled “hopeless” are neglected.',
         'Some schools target support at the most disadvantaged.'),
        ('Ball', 'banding creates differences in pupils’ attitudes and subcultures', 'Interactionism',
         'Ball’s study of Beachside Comprehensive found teachers had higher expectations of top-band (mostly middle-class) pupils; when banding was abolished, polarisation reduced but labelling continued.',
         'One school may not be typical.'),
    ],
    'explain': [
        ('Explain how setting and streaming may disadvantage working-class pupils.', 'Working-class pupils are more likely to be placed in lower sets; lower sets get less experienced teachers and lower expectations; entry to lower-tier exams limits grades; pupils may internalise labels and form anti-school subcultures (Ball, Lacey).', '1 mark each developed point up to 3. [3]'),
        ('Explain what is meant by educational triage and why it occurs.', 'Teachers sort pupils into those who will pass, those who might pass with help and those seen as hopeless, focusing resources on the middle group; it occurs because league table and target pressures reward borderline improvements (Gillborn and Youdell).', '1 mark definition; 1 mark three groups; 1 mark link to league tables/targets. [3]'),
    ],
    'why': [
        ('effect', 'effects', 'of being placed in a low stream or set', ['lower teacher expectations', 'restricted access to higher-tier exams', 'lower self-esteem and motivation', 'joining anti-school subcultures', 'self-fulfilling prophecy of underachievement']),
    ],
    'claims': [
        ('Rist found that teachers grouped pupils on the basis of measured ability only.', False, 'Grouping was based on appearance and background, linked to class.'),
        ('Educational triage can be linked to league table pressures.', True, 'Schools focus on pupils who can raise headline results.'),
        ('Labelling theory can be criticised for being deterministic.', True, 'It assumes pupils passively accept labels, but some resist them.'),
    ],
    'ar': ([('Working-class pupils are over-represented in lower sets.', 'teachers may label them as less able.'),
            ('Educational triage may increase inequality.', 'pupils labelled as hopeless receive less support.')],
           ['Rosenthal and Jacobson found that teachers’ expectations had no effect.', 'streaming means grouping pupils separately for each subject.']),
    'scen': ['A school in {city} places pupils into sets in their first week, largely on the basis of a short test and teachers’ impressions; most pupils in the bottom set are from the poorest housing estate.',
             'Under pressure to improve results in {city}, teachers give extra lessons to pupils predicted to just miss a pass, while those predicted to fail badly receive little attention.'],
    'views': {'Interactionism': VE['Interactionism'], 'Marxism': 'labelling reflects and reproduces wider class inequality: teachers’ judgements are shaped by middle-class norms, and policies such as league tables encourage triage that disadvantages working-class pupils.',
              'Functionalism': 'setting by ability is a meritocratic way of matching teaching to pupils’ abilities and allocating them to appropriate roles.'},
    'ctx': [('how teachers decide which set pupils are placed in', {'young', 'behaviour', 'meaning'}),
            ('pupils’ experiences of being in a bottom set', {'young', 'meaning', 'sensitive'})],
    'data': [dict(what='social class and setting', pop='pupils aged 12', rows=['Top set', 'Middle set', 'Bottom set'], cols=('Middle-class pupils', 'Working-class pupils'), cmp=True, dist=True,
                  base=[(40, 50), (30, 38), (15, 22)], delta=[(-25, -15), (-3, 5), (12, 22)], label='percentage of pupils placed in each mathematics set',
                  expl=['teachers may label working-class pupils as less able (Becker, Rist)', 'differences in prior attainment caused by material and cultural factors',
                        'educational triage and setting decisions reflect pressure on results'],
                  method='official statistics', claim='setting is the main reason for class differences in achievement',
                  counter='Set placement may reflect earlier attainment shaped by out-of-school factors; setting may follow rather than cause differences; some working-class pupils reach top sets.')],
    'essays': [('Explain two ways in which in-school processes may contribute to class differences in achievement.', 'Labelling and the ideal pupil (Becker); self-fulfilling prophecy (Rist, Rosenthal and Jacobson); setting and streaming (Ball); educational triage (Gillborn and Youdell); subcultures (Lacey).',
                'in-school factors are the main cause of class differences in achievement',
                'Labelling, setting and triage shape opportunities and self-concept; studies by Ball, Rist and Gillborn and Youdell; schools with similar intakes get different results.',
                'Material deprivation and cultural capital shape attainment before school; labelling is deterministic; pupils resist; Marxists stress structural causes; factors interact.')],
})

CHAPTERS[3] = [e3a, e3b, e3c]


e4a = T('Explaining the gender gap in achievement')
build(e4a, {
    'terms': [
        ('gender gap', 'the difference in educational achievement between girls and boys', 'girls outperforming boys at age 16 by 8 percentage points'),
        ('feminisation of education', 'the idea that schools have become feminised, valuing traits such as attentiveness and organisation more associated with girls', 'coursework rewarding steady, organised work'),
        ('equal opportunities policies', 'policies designed to give boys and girls the same educational chances', 'encouraging girls into science'),
        ('changing ambitions', 'the shift in girls’ aspirations away from marriage and motherhood towards careers', 'girls planning professional careers'),
        ('coursework', 'assessed work completed during a course rather than in a final exam', 'a project counting towards the final grade'),
        ('role model', 'a person whose behaviour others copy', 'female teachers and head teachers'),
    ],
    'thinkers': [
        ('Sharpe', 'girls’ priorities changed from love and marriage in the 1970s to careers and independence in the 1990s', 'Liberal feminism',
         'Sharpe’s interviews with girls showed a shift in ambitions, explaining girls’ improved achievement.',
         'Working-class girls’ ambitions may still be limited by class and economic opportunities.'),
        ('Mitsos and Browne', 'girls are more conscientious and organised, which suits coursework', 'Liberal feminism',
         'They argued girls spend more time on coursework and take more care with presentation, contributing to the gender gap.',
         'Elwood argued coursework has less influence on final grades than exams.'),
        ('Francis and Skelton', 'girls’ success reflects wider social changes such as feminism and changes in the job market', 'Liberal feminism',
         'They argued girls’ achievement is linked to changes in women’s roles, while some boys’ masculinity discourages effort.',
         'Not all girls benefit equally; class and ethnicity matter.'),
        ('Mac an Ghaill', 'the decline in traditional male jobs has produced a crisis of masculinity among working-class boys', 'Interactionism',
         'Mac an Ghaill found working-class boys who saw no prospect of skilled manual work formed macho subcultures.',
         'Some working-class boys respond by working harder.'),
    ],
    'explain': [
        ('Explain two external factors that help explain why girls now achieve better than boys in many countries.', 'Impact of feminism raising expectations; changes in the family (more female-headed households, role models); changes in women’s employment creating career incentives; changing ambitions (Sharpe).', '2 marks for each explained factor. [4]'),
        ('Explain two internal (school) factors that may explain the gender gap.', 'Equal opportunities policies; female role models among teachers; coursework and assessment styles; teacher attention and expectations; challenging stereotypes in the curriculum.', '2 marks for each explained factor. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why some boys underachieve', ['laddish subcultures see school work as feminine', 'crisis of masculinity as manual jobs decline', 'poorer literacy skills', 'boys may be over-confident and underestimate the effort needed', 'fewer male role models in primary schools']),
    ],
    'claims': [
        ('Girls outperform boys in every subject at every level in all countries.', False, 'The gap varies by subject, level, class and country; boys still do better in some subjects and countries.'),
        ('Sharpe found that girls’ ambitions had shifted towards careers.', True, 'Her 1990s interviews showed girls prioritising careers and independence.'),
        ('Equal opportunities policies may have helped girls.', True, 'They challenged stereotypes and encouraged girls into a wider range of subjects.'),
    ],
    'ar': ([('Girls’ achievement improved from the 1980s onwards.', 'feminism and changes in women’s employment raised girls’ ambitions.'),
            ('Some working-class boys underachieve.', 'the decline of traditional male jobs has reduced their motivation.')],
           ['boys outperform girls in literacy in most countries.', 'Sharpe found girls’ main ambition in the 1990s was marriage.']),
    'scen': ['In {city}, girls now outnumber boys at university by three to two, and more girls than boys achieve top grades at school.',
             'A group of 15-year-old boys in {city} say that “only geeks” revise, and that it is more important to be good at sport.'],
    'views': {'Liberal feminism': 'girls’ success reflects equal opportunities policies, changing ambitions and the impact of feminism; policies should now help both boys and girls fulfil their potential.',
              'Radical feminism': 'despite girls’ success, education remains patriarchal: girls face sexual harassment, subject stereotyping and a curriculum and leadership dominated by men.',
              'Interactionism': 'gender identities are constructed in school interaction: laddish subcultures and teacher expectations shape boys’ and girls’ attitudes to work.',
              'New Right': 'boys’ underachievement reflects the decline of the traditional family and lack of male role models; schools should provide more discipline and male teachers.'},
    'ctx': [('boys’ attitudes to school work', {'young', 'meaning'}),
            ('gender differences in exam results', {'large', 'change'})],
    'data': [dict(what='the gender gap', pop='pupils aged 16', rows=['Girls', 'Boys'], cols=('2000', '2025'),
                  base=[(50, 58), (42, 50)], delta=[(8, 16), (6, 14)], label='percentage achieving five good passes at age 16',
                  leads=['National exam data for {city} ({n} pupils) show the following.', 'The table shows exam results by gender for {n} pupils in {city}.'],
                  expl=['feminism and changing ambitions have raised girls’ motivation (Sharpe)', 'assessment styles such as coursework may favour girls’ organisation',
                        'laddish subcultures and the crisis of masculinity may hold some boys back'],
                  method='official statistics', claim='boys are underachieving in education',
                  counter='Both boys’ and girls’ results have improved; the gap may reflect girls improving faster rather than boys failing; class and ethnicity have larger effects than gender.')],
    'essays': [('Explain two reasons why girls’ achievement has improved.', 'Feminism; changes in family and employment; changing ambitions (Sharpe); equal opportunities policies; female role models; assessment changes (Mitsos and Browne).',
                'the gender gap in achievement is mainly the result of changes outside school',
                'Feminism; changing family structures; women’s employment; changing ambitions (Sharpe, Francis and Skelton).',
                'Internal factors: equal opportunities policies, role models, coursework, teacher attention; laddish subcultures inside school; class and ethnicity interact with gender.')],
})

e4b = T('Gender, subject choice and the hidden curriculum')
build(e4b, {
    'terms': [
        ('gendered subject choice', 'the tendency of boys and girls to choose different subjects', 'more girls taking languages and more boys taking physics'),
        ('gender domains', 'the tasks and activities that boys and girls see as belonging to their gender', 'girls seeing caring as their domain and boys mechanics'),
        ('gender identity', 'a person’s sense of themselves as masculine or feminine', 'a girl avoiding subjects she sees as “for boys”'),
        ('hidden curriculum', 'the unofficial messages schools give about values and behaviour, including about gender', 'boys dominating the playground'),
        ('verbal abuse', 'name-calling used to police gender and sexual identities', 'calling a boy who likes dance “gay”'),
        ('male gaze', 'the way boys and male teachers observe and judge girls, reinforcing heterosexual masculinity', 'boys rating girls’ appearance'),
    ],
    'thinkers': [
        ('Browne and Ross', 'children’s gender domains are shaped by early socialisation', 'Liberal feminism',
         'Browne and Ross found children were more confident with tasks in their own gender domain, influencing later subject choices.',
         'Gender domains may be weakening as socialisation changes.'),
        ('Kelly', 'science is seen as a boys’ subject because of textbooks, teachers and classroom dynamics', 'Liberal feminism',
         'Kelly argued boys monopolised apparatus and dominated science lessons.',
         'Girls’ participation in many sciences, such as biology, has grown.'),
        ('Connell', 'schools reinforce hegemonic masculinity through the hidden curriculum', 'Radical feminism',
         'Connell argued schools police gender through sport, discipline and peer pressure, valuing tough masculinity.',
         'Some schools actively challenge stereotypes.'),
        ('Paechter', 'pupils see subjects such as PE as masculine, which affects girls’ participation', 'Liberal feminism',
         'Paechter argued PE is associated with male competitiveness, so girls who are sporty may be labelled.',
         'Attitudes to women’s sport are changing.'),
    ],
    'explain': [
        ('Explain two reasons for gender differences in subject choice.', 'Early socialisation and gender domains (Browne and Ross); gendered subject images (Kelly); peer pressure and gender identity; careers advice and gendered job markets; single-sex schooling effects.', '2 marks for each explained reason. [4]'),
        ('Explain how the hidden curriculum may reinforce gender identities.', 'Teacher attention and discipline differ by gender; boys dominate space and discussion; verbal abuse polices masculinity and femininity; male gaze; staffing hierarchy (male heads, female classroom teachers).', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which schools could reduce gendered subject choice', ['offering female science role models', 'non-stereotyped careers advice', 'reviewing textbooks for gender bias', 'single-sex classes in some subjects', 'challenging gendered verbal abuse']),
    ],
    'claims': [
        ('Gender differences in subject choice have disappeared.', False, 'Boys still dominate some subjects (e.g. physics, computing) and girls others (e.g. languages, social sciences).'),
        ('Peer pressure can influence subject choice.', True, 'Pupils may avoid subjects that do not fit their gender identity to avoid ridicule.'),
    ],
    'ar': ([('Fewer girls than boys choose physics in many countries.', 'physics is often seen as a masculine subject.'),
            ('Gendered verbal abuse can affect pupils’ choices.', 'it polices what behaviour is acceptable for each gender.')],
           ['gender domains are fixed by biology.', 'the hidden curriculum only teaches formal subject knowledge.']),
    'scen': ['In a school in {city}, 80% of pupils taking computer science are boys, while 75% of those taking health and social care are girls.',
             'A boy in {city} who wants to study dance is teased by classmates, who say it is “for girls”.'],
    'views': {'Liberal feminism': 'gendered subject choice results from socialisation, stereotyped images and careers advice, which schools can change through equal opportunities policies.',
              'Radical feminism': 'subject choice and the hidden curriculum reflect patriarchy: schools steer girls to lower-paid caring careers and reinforce male dominance.',
              'Interactionism': 'gender identities are negotiated in interaction: peer groups and teachers label behaviour as appropriate or not, influencing choices.',
              'Functionalism': 'different subject choices may prepare boys and girls for complementary roles, although modern economies need both genders in all fields.'},
    'ctx': [('why girls avoid physics and computer science', {'young', 'meaning'}),
            ('gender differences in subject choice over time', {'large', 'change'})],
    'data': [dict(what='gender and subject choice', pop='students aged 17-18', rows=['Physics', 'Psychology', 'Computing'], cols=('Boys', 'Girls'), cmp=True, nocount=True,
                  base=[(20, 30), (10, 18), (15, 25)], delta=[(-18, -10), (10, 22), (-15, -8)], label='percentage of each gender taking the subject',
                  expl=['gender domains and early socialisation (Browne and Ross)', 'gendered subject images and stereotyping (Kelly)', 'peer pressure and gender identity'],
                  method='official statistics', claim='subject choice is still strongly shaped by gender',
                  counter='Differences may have narrowed over time; individual choice and interest also matter; the data do not show reasons for choices.')],
    'essays': [('Explain two reasons why boys and girls choose different subjects.', 'Gender domains; subject images; peer pressure and identity; careers advice; gendered labour market; teachers’ expectations.',
                'gender differences in subject choice are mainly the result of the hidden curriculum',
                'Teacher attention, subject images, peer policing, male gaze (Connell, Kelly, Paechter).',
                'Early socialisation and gender domains occur before school; labour market and family expectations; individual choice; change over time shows policies matter.')],
})

e4c = T('Masculinities, laddish subcultures and boys\' achievement')
build(e4c, {
    'terms': [
        ('laddish subculture', 'a group of boys who reject school work as feminine and value toughness, humour and popularity', 'boys who mock pupils who revise'),
        ('hegemonic masculinity', 'the dominant form of masculinity, associated with toughness, heterosexuality and power', 'boys proving themselves through sport and fighting'),
        ('crisis of masculinity', 'uncertainty about male identity as traditional male roles decline', 'working-class boys with no prospect of manual work'),
        ('macho lads', 'Mac an Ghaill’s term for working-class boys who were hostile to school and valued toughness', 'boys who see school rules as pointless'),
        ('effortless achievement', 'the image some boys cultivate of succeeding without appearing to work', 'a boy who hides his revision from friends'),
    ],
    'thinkers': [
        ('Epstein', 'working-class boys are harassed and labelled “gay” if they appear to work hard', 'Interactionism',
         'Epstein found working-class boys who worked hard were labelled “swots” or “gay”, so many avoided being seen to work.',
         'Middle-class boys may combine masculinity with achievement.'),
        ('Mac an Ghaill', 'schools produce a range of masculinities, including macho lads, academic achievers and new enterprisers', 'Interactionism',
         'Mac an Ghaill’s study of Parnell School showed boys’ masculine identities were linked to class and their response to school.',
         'One school may be untypical.'),
        ('Francis', 'laddish behaviour is a way for boys to protect their masculine status', 'Liberal feminism',
         'Francis found boys more concerned than girls about being labelled as swots, and laddishness was linked to popularity.',
         'Laddish behaviour is also found among some girls (“ladettes”).'),
    ],
    'explain': [
        ('Explain how laddish subcultures may affect boys’ achievement.', 'Laddish boys see school work as feminine and uncool; they gain status through humour, sport and rule-breaking; those who work are labelled swots; so many avoid effort and underachieve.', '1 mark each developed point up to 3. [3]'),
        ('Explain what is meant by a crisis of masculinity and how it may affect boys’ education.', 'The decline of traditional male manual jobs and the breadwinner role creates uncertainty about male identity; some working-class boys see no point in qualifications for jobs that no longer exist and form macho subcultures.', '1 mark meaning; 2 marks effect on education. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why some boys avoid being seen to work hard at school', ['fear of being labelled a swot or geek', 'working hard is seen as feminine', 'peer status depends on humour and toughness', 'fear of failure if they try and do badly']),
    ],
    'claims': [
        ('All boys reject school work.', False, 'Mac an Ghaill identified several masculinities, including academic achievers.'),
        ('Epstein found boys who worked hard could be labelled “gay”.', True, 'Homophobic abuse policed masculinity and discouraged effort.'),
    ],
    'ar': ([('Some boys avoid revising openly.', 'being seen to work hard can damage their masculine status.'),
            ('Laddish subcultures are linked to class.', 'working-class boys may see little value in qualifications for the jobs available to them.')],
           ['laddish subcultures value conscientious study.', 'Mac an Ghaill found only one type of masculinity in school.']),
    'scen': ['{man}, a 15-year-old in {city}, revises secretly at home but tells friends he “never does any work”.',
             'In a school in {city}, a group of boys gain popularity by disrupting lessons and mocking classmates who answer questions.'],
    'views': {'Interactionism': 'masculine identities are constructed and policed through peer interaction and labels such as “swot”, which affect boys’ effort and achievement.',
              'Marxism': 'laddish subcultures reflect working-class boys’ position: like Willis’s lads, their rejection of school prepares them for manual work and reproduces class inequality.',
              'Liberal feminism': 'boys’ underachievement shows how gender stereotypes harm boys as well as girls; schools should challenge narrow ideas of masculinity.',
              'New Right': 'boys’ underachievement reflects lack of discipline and male role models; schools should provide more structure and male teachers.'},
    'ctx': [('masculinity in a secondary school', {'young', 'meaning', 'behaviour'}),
            ('boys’ attitudes to revision', {'young', 'meaning'})],
    'essays': [('Explain two ways in which masculinity may affect boys’ achievement.', 'Laddish subcultures; fear of being labelled swot (Epstein, Francis); crisis of masculinity (Mac an Ghaill); effortless achievement; hegemonic masculinity and peer policing.',
                'laddish subcultures are the main reason for boys’ underachievement',
                'Epstein, Francis and Mac an Ghaill show peer pressure against effort; crisis of masculinity.',
                'Class and ethnicity have bigger effects; literacy and assessment changes; many boys achieve highly; girls’ improvement explains much of the gap; external factors such as family.')],
}, VE)

CHAPTERS[4] = [e4a, e4b, e4c]


e5a = T('Patterns of ethnic differences in achievement')
build(e5a, {
    'terms': [
        ('ethnic group', 'a group sharing a cultural identity based on factors such as language, religion, history and traditions', 'a community of migrants from the same region'),
        ('attainment gap', 'the difference in average results between groups', 'a 12-point gap between two ethnic groups'),
        ('intersectionality', 'the way ethnicity combines with class and gender to shape outcomes', 'working-class boys of one ethnic group having the lowest results'),
        ('exclusion', 'the removal of a pupil from school, temporarily or permanently, for disciplinary reasons', 'a pupil expelled for repeated disruption'),
        ('aspiration', 'hopes and ambitions for the future, such as going to university', 'parents expecting their children to become doctors'),
    ],
    'thinkers': [
        ('Modood', 'ethnic minority groups have high aspirations and many achieve well despite disadvantage', 'Interactionism',
         'Modood found many ethnic minority families valued education highly, and some groups outperformed the majority despite lower incomes.',
         'Aggregated categories can hide large differences within ethnic groups.'),
        ('Gillborn', 'black pupils are disadvantaged by the way schools assess and set them', 'Neo-Marxism',
         'Gillborn found black pupils who performed well on entry tests were later placed in lower sets and tiers, which he saw as institutional racism.',
         'Others argue class and material factors explain more of the gap.'),
        ('Archer', 'teachers see some minority pupils as “ideal” and others as “demonised”', 'Interactionism',
         'Archer found Chinese pupils were stereotyped as hard-working but “overachieving”, while black and Muslim pupils were often seen as problems.',
         'Positive stereotypes can also put pressure on pupils.'),
    ],
    'explain': [
        ('Explain why it is important to consider class and gender when studying ethnic differences in achievement.', 'Ethnicity interacts with class and gender (intersectionality); some ethnic gaps narrow or disappear when class is controlled; within each ethnic group girls often outperform boys; broad ethnic categories hide variation.', '1 mark each developed point up to 3. [3]'),
        ('Explain two reasons why official statistics on ethnicity and achievement should be treated with caution.', 'Ethnic categories are broad and hide differences (e.g. between national origins); self-classification varies; class and gender are not always controlled; changes in categories over time; small group sizes.', '2 marks for each explained reason. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why some ethnic minority groups achieve above the national average', ['high parental aspirations and support', 'strong community and supplementary schools', 'cultural value placed on education', 'positive teacher stereotypes', 'education seen as a route out of disadvantage']),
    ],
    'claims': [
        ('All ethnic minority groups underachieve compared with the majority.', False, 'Some minority groups outperform the majority, while others underachieve; patterns vary by class and gender.'),
        ('Class and gender interact with ethnicity in shaping achievement.', True, 'Intersectionality shows outcomes depend on the combination of these factors.'),
    ],
    'ar': ([('Ethnic differences in achievement vary between groups.', 'ethnic groups differ in class composition, culture and experiences of schooling.'),
            ('Some ethnic gaps narrow when class is taken into account.', 'some minority groups are more likely to be in poverty.')],
           ['all ethnic minority groups achieve below the national average.', 'gender has no effect on achievement within ethnic groups.']),
    'scen': ['Exam data from {city} show that pupils from one migrant community achieve well above the national average, while pupils from another achieve well below it.',
             'In {city}, black Caribbean boys are three times more likely to be excluded from school than the average pupil.'],
    'views': {'Interactionism': 'ethnic differences are partly created in schools through teachers’ stereotypes and labels, which shape set placements and pupils’ self-concepts (Archer, Gillborn).',
              'Functionalism': 'differences reflect cultural values and family support for education; schools should help all groups integrate into shared values (cultural deprivation view).',
              'Marxism': 'ethnic differences are bound up with class inequality: minority groups are over-represented in poverty and institutional racism helps reproduce disadvantage.'},
    'ctx': [('ethnic differences in exam results in {city}', {'large', 'change'}),
            ('minority ethnic pupils’ experiences of school', {'young', 'meaning', 'sensitive'})],
    'data': [dict(what='ethnicity and achievement', pop='pupils aged 16', rows=['Group A', 'Group B', 'Group C'], cols=('Not eligible for free meals', 'Eligible for free meals'), cmp=True, nocount=True,
                  base=[(70, 80), (50, 60), (60, 70)], delta=[(-15, -5), (-20, -10), (-15, -5)], label='percentage achieving five good passes',
                  leads=['National data for {city} ({n} pupils) show exam results by ethnic group and eligibility for free school meals.', 'The table shows results for {n} pupils in {city}, by ethnic group and poverty.'],
                  expl=['poverty reduces achievement in every ethnic group, showing the importance of class', 'cultural factors and parental aspirations differ between groups',
                        'teacher labelling and institutional racism may affect some groups more'],
                  method='official statistics', claim='class is more important than ethnicity in explaining differences in achievement',
                  counter='Differences between ethnic groups remain even within the same poverty category; broad categories hide variation; official data do not show processes inside schools.')],
    'essays': [('Explain two patterns of ethnic differences in educational achievement.', 'Some groups above and some below average; gender gaps within groups; class effects within groups; exclusion rates; differences in university entry.',
                'ethnic differences in achievement are mainly the result of social class',
                'Many minority groups are over-represented in poverty; gaps narrow when class is controlled; material deprivation affects all groups.',
                'Gaps remain within the same class; racism and labelling (Gillborn, Archer); cultural factors (Modood); gender and intersectionality.')],
})

e5b = T('External explanations: cultural, material and linguistic factors')
build(e5b, {
    'terms': [
        ('cultural deprivation', 'the theory that some groups lack the values, attitudes or skills needed for success in education', 'claims that some families do not value education'),
        ('linguistic deprivation', 'the theory that some children lack the language skills needed for school, for example if English is not their first language', 'a child struggling with exam language'),
        ('material deprivation', 'lack of money and resources that affect education, such as poor housing and diet', 'a family in overcrowded housing'),
        ('racism in wider society', 'discrimination in areas such as jobs and housing that affects minority families’ resources', 'parents denied jobs because of ethnicity'),
        ('supplementary school', 'an out-of-school-hours school run by a community, often teaching language, culture or extra subjects', 'weekend classes run by a migrant community'),
    ],
    'thinkers': [
        ('Sewell', 'the absence of fathers in some families leaves black boys vulnerable to peer pressure and street culture', 'New Right',
         'Sewell argued black boys lacked a nurturing father figure and were influenced by gangs and media images of anti-school masculinity.',
         'Critics argue this blames families and ignores racism in schools.'),
        ('Lupton', 'respect for adult authority in some families encourages good behaviour in school', 'Functionalism',
         'Lupton found that adult authority in Indian and Chinese families paralleled school authority, which helped pupils’ behaviour and achievement.',
         'This may reinforce stereotypes about particular groups.'),
        ('Gillborn and Mirza', 'material and cultural explanations cannot fully explain ethnic gaps in achievement', 'Neo-Marxism',
         'They found black pupils achieved well in some local areas at age 5 but fell behind later, suggesting school processes matter.',
         'Their data covered only some local authorities.'),
    ],
    'explain': [
        ('Explain two external factors that may lead some ethnic minority pupils to underachieve.', 'Material deprivation linked to discrimination in jobs and housing; language differences (English as an additional language); cultural deprivation claims about family structure or attitudes (Sewell); racism in wider society.', '2 marks for each explained factor. [4]'),
        ('Explain one criticism of cultural deprivation explanations of ethnic differences in achievement.', 'They blame minority families and cultures (victim-blaming); ignore material disadvantage and racism; cannot explain why some minority groups achieve highly; overlook in-school processes (Gillborn and Mirza).', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why some minority ethnic families experience material deprivation', ['discrimination in employment', 'living in areas of high unemployment', 'language barriers limiting job opportunities', 'qualifications from abroad not being recognised', 'larger family sizes in some groups']),
    ],
    'claims': [
        ('Pupils who speak English as an additional language always underachieve.', False, 'Many EAL pupils catch up and achieve well; language is not a long-term barrier for most.'),
        ('Racism in wider society can lead to material deprivation.', True, 'Discrimination in jobs and housing reduces families’ income and resources.'),
    ],
    'ar': ([('Some minority ethnic groups have higher rates of poverty.', 'they face discrimination in the labour market.'),
            ('Supplementary schools can support achievement.', 'they provide extra teaching and reinforce the value of education.')],
           ['Sewell argued that institutional racism in schools is the main cause of black boys’ underachievement.', 'language differences prevent most migrant children from ever succeeding at school.']),
    'scen': ['A family recently arrived in {city} live in a small flat; the parents, both qualified teachers in their home country, work as cleaners because their qualifications are not recognised.',
             'In {city}, a migrant community runs Saturday schools where children study mathematics and their parents’ language.'],
    'views': {'Functionalism': 'achievement reflects how far family cultures prepare children for school values; cultural deprivation can be overcome through compensatory education.',
              'New Right': 'family structure and culture explain underachievement: lack of father figures and anti-school street culture harm some boys (Sewell).',
              'Marxism': 'material deprivation, shaped by racism in the labour and housing markets, explains much underachievement; cultural explanations blame the victim.'},
    'ctx': [('the experiences of pupils learning English as an additional language', {'young', 'meaning'}),
            ('the role of supplementary schools in minority communities', {'meaning', 'behaviour'})],
    'data': [dict(what='ethnicity and income', pop='households with children', rows=['Group A', 'Group B', 'Majority group'], cols=('2010', '2025'),
                  base=[(35, 45), (20, 30), (15, 22)], delta=[(-8, 2), (-5, 3), (-4, 2)], label='percentage of households in relative poverty',
                  expl=['labour market discrimination and lower pay affect some minority groups', 'unrecognised qualifications force migrants into low-paid jobs',
                        'differences in employment rates and family size'],
                  method='official statistics', claim='material deprivation explains ethnic differences in achievement',
                  counter='Some groups with high poverty rates achieve well; in-school factors and racism also matter; poverty measures may not capture wealth or support networks.')],
    'essays': [('Explain two cultural explanations of ethnic differences in achievement.', 'Family structure (Sewell); parental attitudes and aspirations (Lupton, Modood); language; values of community; supplementary schooling.',
                'external factors are more important than internal factors in explaining ethnic differences in achievement',
                'Material deprivation, racism in wider society, language, family culture (Sewell, Lupton).',
                'Labelling and institutional racism (Gillborn, Archer); ethnocentric curriculum; gaps that open during schooling (Gillborn and Mirza); cultural explanations blame the victim.')],
})

e5c = T('Internal explanations: institutional racism, labelling and ethnocentric curriculum')
build(e5c, {
    'terms': [
        ('institutional racism', 'discrimination built into the policies and practices of organisations, whether intended or not', 'set placement systems that place disproportionate numbers of black pupils in lower sets'),
        ('ethnocentric curriculum', 'a curriculum that reflects the culture of one ethnic group, usually the majority, and marginalises others', 'history lessons ignoring the history of colonised peoples'),
        ('racialised expectations', 'teachers’ assumptions about pupils’ ability or behaviour based on ethnicity', 'expecting black pupils to be disruptive'),
        ('pupil identity', 'how teachers and others see a pupil, such as ideal, pathologised or demonised', 'a pupil seen as a hard-working “model minority”'),
        ('critical race theory', 'the view that racism is embedded in the structure of society and its institutions', 'arguing that assessment systems favour white pupils'),
        ('locked-in inequality', 'Gillborn’s idea that racial inequality is so deeply rooted that it is built into the system', 'historical disadvantage continuing across generations'),
    ],
    'thinkers': [
        ('Gillborn', 'institutional racism in assessment and setting locks in inequality for black pupils', 'Neo-Marxism',
         'Gillborn argued changes to assessment, such as moving from baseline testing to teacher assessment, coincided with black pupils being rated lower.',
         'Others argue class and family factors explain more.'),
        ('Wright', 'teachers in primary schools held stereotyped views of Asian and black pupils', 'Interactionism',
         'Wright found Asian girls were excluded from discussions and spoken to slowly, and black boys disciplined more harshly.',
         'It was a small-scale study of four schools.'),
        ('Fuller', 'black girls can reject negative labels and succeed', 'Interactionism',
         'Fuller studied black girls in a London school who worked hard to prove teachers wrong while appearing anti-school to peers.',
         'Not all pupils have the resources to resist labels.'),
        ('Coard', 'the ethnocentric curriculum damaged the self-esteem of black pupils', 'Neo-Marxism',
         'Coard argued British schools taught that white culture was superior, lowering black pupils’ self-esteem and achievement.',
         'Stone argued black pupils did not necessarily have low self-esteem.'),
    ],
    'explain': [
        ('Explain what is meant by institutional racism in education.', 'Discrimination built into the routine practices of schools, such as setting, assessment, exclusion policies or the curriculum, which disadvantages some ethnic groups even if no individual intends to discriminate.', '1 mark meaning; 1 mark built into routines/unintended; 1 mark example. [3]'),
        ('Explain two ways in which teachers’ labels may affect minority ethnic pupils.', 'Racialised expectations lead to harsher discipline and exclusion; lower set and tier placements; self-fulfilling prophecy; pupils may form subcultures or resist (Fuller); some groups positively stereotyped (Archer).', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('feature', 'features', 'of an ethnocentric curriculum', ['history focusing on the majority nation and its achievements', 'literature drawn mainly from one culture', 'religious education focusing on one faith', 'textbooks with few positive images of minorities', 'languages of minority groups not offered']),
    ],
    'claims': [
        ('Institutional racism requires individual teachers to hold racist views.', False, 'It is built into routine practices and can occur without individual intent.'),
        ('Fuller found that some black girls resisted negative labels.', True, 'They worked hard to prove teachers wrong.'),
    ],
    'ar': ([('Black pupils may be over-represented in lower sets.', 'teachers’ racialised expectations can influence set placement.'),
            ('An ethnocentric curriculum can marginalise minority pupils.', 'it gives less value to the history and culture of minority groups.')],
           ['institutional racism only occurs when individuals intend to discriminate.', 'Fuller found that all black girls accepted negative labels.']),
    'scen': ['In a school in {city}, pupils from one minority group make up 10% of the school but 30% of exclusions.',
             'The history syllabus in {city} covers the nation’s kings and wars but says almost nothing about the countries from which many pupils’ families came.'],
    'views': {'Interactionism': 'teachers’ racialised expectations and labels affect pupils’ treatment and self-concept; some pupils accept labels while others resist (Wright, Fuller).',
              'Neo-Marxism': 'critical race theorists argue racism is built into school structures such as assessment, setting and the curriculum, locking in inequality (Gillborn).',
              'Functionalism': 'schools should promote shared national values and integration; differences in outcomes reflect cultural and family factors rather than school practices.'},
    'ctx': [('teachers’ expectations of pupils from different ethnic groups', {'young', 'behaviour', 'sensitive'}),
            ('the content of the school history curriculum', {'past', 'meaning', 'media'})],
    'methods': ['questionnaire', 'unstructured interview', 'semi-structured interview', 'participant observation', 'non-participant observation', 'official statistics', 'content analysis', 'case study'],
    'data': [dict(what='exclusions by ethnicity', pop='pupils', rows=['Group A', 'Group B', 'All pupils'], cols=('2015', '2025'), unit='', uname='exclusions per 1,000 pupils', nocount=True,
                  base=[(25, 35), (8, 14), (10, 15)], delta=[(-8, 4), (-3, 2), (-3, 3)], label='permanent and fixed-term exclusions per 1,000 pupils',
                  leads=['Official data for schools in {city} (about {n}0 pupils) show exclusion rates by ethnic group.', 'The table shows exclusion rates in {city}, based on records for around {n}0 pupils.'],
                  expl=['teachers’ racialised expectations may lead to harsher discipline for some groups (Wright, Gillborn)', 'institutional racism in behaviour policies', 'material deprivation linked to behaviour difficulties'],
                  method='official statistics', claim='institutional racism explains ethnic differences in exclusions',
                  counter='Exclusion rates may also reflect differences in class and family circumstances; statistics do not show the reasons for each exclusion; rates differ between schools.')],
    'essays': [('Explain two ways in which schools may contribute to ethnic differences in achievement.', 'Labelling and racialised expectations (Wright); setting and assessment (Gillborn); ethnocentric curriculum (Coard); exclusions; pupil identities (Archer).',
                'institutional racism is the main reason for ethnic differences in achievement',
                'Gillborn: assessment and setting lock in inequality; Wright and Archer: labelling; ethnocentric curriculum; exclusion rates.',
                'External factors (poverty, family, language); some minorities achieve highly despite racism; Fuller shows resistance; class and gender interact; Sewell stresses peer culture.')],
})

CHAPTERS[5] = [e5a, e5b, e5c]


e6a = T('Teacher-pupil relationships and labelling')
build(e6a, {
    'terms': [
        ('teacher expectations', 'the beliefs teachers hold about how well pupils will do', 'expecting a pupil to gain top grades'),
        ('typing', 'the process by which teachers categorise pupils', 'seeing a pupil as a “conformist” or “deviant”'),
        ('speculation, elaboration and stabilisation', 'Hargreaves’s three stages through which teachers’ impressions of pupils become fixed labels', 'a first impression hardening into a fixed view'),
        ('negotiation', 'the process by which teachers and pupils bargain over classroom rules and behaviour', 'pupils agreeing to work if they can listen to music'),
        ('self-concept', 'a person’s view of themselves', 'a pupil seeing themselves as “clever”'),
    ],
    'thinkers': [
        ('Hargreaves', 'teachers type pupils through speculation, elaboration and stabilisation', 'Interactionism',
         'Hargreaves, Hester and Mellor showed how initial guesses about pupils are tested and become fixed labels.',
         'Pupils can change teachers’ views through their behaviour.'),
        ('Keddie', 'teachers classify pupils’ knowledge differently depending on their set', 'Interactionism',
         'Keddie found teachers accepted abstract answers from top-stream pupils but dismissed everyday knowledge from lower-stream pupils.',
         'One school may not represent others.'),
        ('Woods', 'pupils adopt different adaptations to school, such as conformity, ingratiation, ritualism, retreatism and rebellion', 'Interactionism',
         'Woods showed pupil responses are more varied than simply pro- or anti-school.',
         'The typology may oversimplify how pupils behave in different lessons.'),
    ],
    'explain': [
        ('Explain how a teacher’s initial impressions of a pupil may become a fixed label.', 'Speculation: teachers guess about a pupil from appearance and behaviour; elaboration: they test the guess; stabilisation: the label becomes fixed and shapes treatment (Hargreaves).', '1 mark for each stage explained. [3]'),
        ('Explain one strength and one limitation of interactionist studies of teacher-pupil relationships.', 'Strength: they reveal processes inside classrooms that structural theories miss and show how inequality is produced. Limitation: small-scale, may ignore wider structures; labelling may be deterministic.', '2 marks each explained point. [4]'),
    ],
    'why': [
        ('way', 'ways', 'in which teachers may communicate their expectations to pupils', ['the amount of praise or criticism given', 'the questions asked and time given to answer', 'body language and tone of voice', 'set and exam tier placement', 'the work and feedback given']),
    ],
    'claims': [
        ('Teacher-pupil relationships are always one-way, with teachers controlling pupils.', False, 'Interactionists stress negotiation: pupils influence teachers and resist labels.'),
        ('Keddie found that teachers valued knowledge differently for pupils in different streams.', True, 'Top-stream pupils’ abstract answers were valued; lower-stream pupils’ everyday knowledge was dismissed.'),
    ],
    'ar': ([('Teacher expectations can affect achievement.', 'pupils may internalise the labels teachers give them.'),
            ('Classroom rules are often negotiated.', 'pupils and teachers bargain over what behaviour is acceptable.')],
           ['Hargreaves argued labels are fixed from the first moment of contact.', 'Woods found that all pupils respond to school in the same way.']),
    'scen': ['A new teacher in {city} decides in the first lesson that {person} is “lazy”; by the end of term the teacher no longer asks {person} any questions.',
             'In a classroom in {city}, pupils agree to complete a worksheet quietly if the teacher lets them choose where to sit.'],
    'views': VE,
    'ctx': [('teacher-pupil interaction in mathematics lessons', {'young', 'behaviour'}),
            ('pupils’ views of their teachers', {'young', 'meaning'})],
    'essays': [('Explain two ways in which teacher-pupil relationships may affect achievement.', 'Labelling and self-fulfilling prophecy; typing (Hargreaves); classification of knowledge (Keddie); negotiation; pupil adaptations (Woods).',
                'teacher-pupil relationships are the most important influence on pupils’ achievement',
                'Labelling, expectations and self-fulfilling prophecy (Rist, Rosenthal and Jacobson); negotiation; Keddie.',
                'External factors such as class, cultural capital and material deprivation; pupils resist labels; structural pressures such as league tables shape teacher behaviour.')],
})

e6b = T('Setting, streaming and the organisation of learning')
build(e6b, {
    'terms': [
        ('setting', 'grouping pupils by ability separately for each subject', 'a pupil in set 1 for science and set 3 for French'),
        ('streaming', 'grouping pupils by general ability for all subjects', 'a pupil in the “B stream” for every lesson'),
        ('mixed-ability teaching', 'teaching pupils of different abilities together in the same class', 'a whole-class history lesson for all abilities'),
        ('tiering', 'entering pupils for exams with different maximum grades', 'a foundation paper capped at a middle grade'),
        ('banding', 'grouping pupils into broad ability bands', 'a school with three bands in each year'),
        ('polarisation', 'the process by which pupils move towards pro- or anti-school positions', 'top-set pupils becoming more pro-school and bottom-set pupils more anti-school'),
    ],
    'thinkers': [
        ('Lacey', 'streaming leads to differentiation and polarisation among pupils', 'Interactionism',
         'Lacey’s study of Hightown Grammar found boys in lower streams formed anti-school subcultures, while top-stream boys became more pro-school.',
         'It was a single boys’ grammar school.'),
        ('Ball', 'banding produces differences in teacher expectations and pupil attitudes', 'Interactionism',
         'At Beachside Comprehensive, Ball found top-band pupils (mostly middle-class) were encouraged towards exams, while lower bands were treated as discipline problems.',
         'When mixed-ability teaching was introduced, some differences remained.'),
        ('Douglas', 'children placed in lower streams at age 8 tend to fall further behind', 'Functionalism',
         'Douglas’s longitudinal study found that children placed in lower streams declined in IQ scores relative to those in higher streams.',
         'Other factors, such as home background, also affected progress.'),
    ],
    'explain': [
        ('Explain one advantage and one disadvantage of setting pupils by ability.', 'Advantage: teaching can be pitched at the right level for each group, stretching the most able. Disadvantage: lower sets receive lower expectations, less experienced teachers and lower exam tiers, creating self-fulfilling prophecies.', '2 marks each explained point. [4]'),
        ('Explain how streaming may lead to polarisation.', 'Pupils in top streams receive status and encouragement and become pro-school; those in bottom streams are labelled failures, lose self-esteem and form anti-school subcultures to gain status (Lacey).', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('argument', 'arguments', 'in favour of mixed-ability teaching', ['it avoids labelling pupils as failures', 'it gives all pupils access to the same curriculum', 'it reduces polarisation into pro- and anti-school groups', 'more able pupils can help others']),
    ],
    'claims': [
        ('Setting and streaming mean the same thing.', False, 'Setting groups pupils by ability in each subject; streaming groups them by general ability for all subjects.'),
        ('Lacey found that streaming led to polarisation.', True, 'Top-stream pupils became pro-school and bottom-stream pupils anti-school.'),
    ],
    'ar': ([('Pupils in lower sets may be entered for lower-tier exams.', 'teachers expect them to achieve lower grades.'),
            ('Streaming can produce anti-school subcultures.', 'pupils in lower streams are denied status in the school’s terms.')],
           ['mixed-ability teaching groups pupils by ability for all subjects.', 'Lacey found that streaming reduced differences between pupils.']),
    'scen': ['A school in {city} decides to stream pupils from age 11 on the basis of a single entrance test.',
             'In {city}, a school abolishes setting and teaches all subjects in mixed-ability classes; teachers report that lower-attaining pupils participate more.'],
    'views': VE,
    'ctx': [('the effects of setting on pupils’ self-esteem', {'young', 'meaning', 'sensitive'}),
            ('how schools decide whether to set pupils', {'meaning', 'behaviour'})],
    'data': [dict(what='setting and exam tier', pop='pupils', rows=['Top set', 'Middle set', 'Bottom set'], cols=('Middle-class pupils', 'Working-class pupils'), cmp=True, nocount=True,
                  base=[(90, 98), (55, 70), (10, 25)], delta=[(-6, 0), (-10, 0), (-10, 0)], label='percentage of pupils entered for the higher-tier exam',
                  expl=['tiering limits the grades available to lower-set pupils', 'teachers may make tier decisions influenced by labels', 'class differences in prior attainment'],
                  method='official statistics', claim='setting creates inequalities in opportunity',
                  counter='Lower-set entries may reflect genuine differences in attainment; setting may help pupils progress at their own pace; the data do not show outcomes.')],
    'essays': [('Explain two effects of setting and streaming on pupils.', 'Labelling and self-fulfilling prophecy; polarisation and subcultures (Lacey, Ball); exam tier limits; differences in teacher expectations; impact on self-esteem.',
                'setting by ability is unfair to working-class pupils',
                'Working-class pupils over-represented in lower sets; lower expectations and tiers; polarisation; Douglas, Ball, Gillborn and Youdell.',
                'Setting may suit teaching to ability; placement based on prior attainment; mixed-ability teaching has drawbacks; inequality originates outside school.')],
})

e6c = T('Pupil subcultures: pro-school and anti-school responses')
build(e6c, {
    'terms': [
        ('pupil subculture', 'a group of pupils who share similar values and behaviour patterns', 'a group of friends who all value doing well'),
        ('pro-school subculture', 'a subculture whose members accept and value the school’s goals', 'pupils who join clubs and aim for university'),
        ('anti-school subculture', 'a subculture whose members reject the school’s values and rules', 'pupils who truant and mock achievers'),
        ('differentiation', 'the process by which teachers categorise pupils according to how they perceive their ability and behaviour', 'placing pupils in different streams'),
        ('status frustration', 'a sense of failure and low status among pupils denied success by the school', 'bottom-set pupils seeking status by disrupting lessons'),
        ('conformity', 'Woods’s adaptation in which pupils accept the school’s goals and means', 'a pupil who works hard and follows rules'),
    ],
    'thinkers': [
        ('Lacey', 'differentiation by streaming produces polarisation into pro- and anti-school subcultures', 'Interactionism',
         'At Hightown Grammar, boys in low streams suffered status frustration and formed anti-school subcultures to gain status.',
         'It was a study of a single selective school.'),
        ('Willis', 'the lads’ counter-school culture prepared them for working-class jobs', 'Neo-Marxism',
         'Willis found 12 working-class “lads” rejected school as pointless, valued “having a laff” and saw conformist pupils as “ear’oles”.',
         'Small sample; later research shows more varied responses.'),
        ('Woods', 'pupils make a range of adaptations to school, not just pro- or anti-school ones', 'Interactionism',
         'Woods identified ingratiation, ritualism, retreatism and rebellion as well as conformity.',
         'Pupils may adopt different adaptations in different contexts.'),
        ('Fuller', 'pupils can reject labels while still succeeding at school', 'Interactionism',
         'Fuller’s black girls formed a subculture that valued qualifications but did not seek teachers’ approval.',
         'Not all groups have the confidence or support to resist in this way.'),
    ],
    'explain': [
        ('Explain why anti-school subcultures form.', 'Status frustration after being labelled and placed in low sets (Lacey); rejection of middle-class school values; class identity and expectations of manual work (Willis); peer pressure; laddish masculinity.', '1 mark each developed point up to 3. [3]'),
        ('Explain the difference between pro-school and anti-school subcultures, using an example of each.', 'Pro-school pupils accept school values and gain status through success (e.g. top-set pupils joining clubs); anti-school pupils reject school values and gain status by breaking rules (e.g. Willis’s lads).', '1 mark each definition; 1 mark each example. [4]'),
    ],
    'why': [
        ('adaptation', 'adaptations', 'to school identified by Woods', ['ingratiation (seeking teachers’ favour)', 'ritualism (going through the motions)', 'retreatism (daydreaming and withdrawal)', 'rebellion (rejecting school goals)', 'conformity']),
    ],
    'claims': [
        ('Willis’s lads saw conformist pupils as “ear’oles”.', True, 'They mocked pupils who conformed and valued having a laff instead.'),
        ('All pupils belong to either a pro-school or an anti-school subculture.', False, 'Woods showed a wider range of adaptations, and Fuller showed mixed responses.'),
    ],
    'ar': ([('Anti-school subcultures are more common in lower sets.', 'pupils denied status by the school seek status from peers instead.'),
            ('Willis’s lads ended up in manual jobs.', 'their counter-school culture rejected academic qualifications.')],
           ['Lacey found that streaming reduced polarisation.', 'Woods argued that pupils adopt only two types of response to school.']),
    'scen': ['A group of 14-year-olds in a bottom set in {city} skip lessons, mock classmates who do homework and say school is “a waste of time”.',
             'In a school in {city}, a group of pupils organise a debating club and revise together for exams.'],
    'views': VE,
    'ctx': [('anti-school subcultures in {city}', {'young', 'hidden', 'meaning'}),
            ('how pupils gain status among their peers', {'young', 'behaviour', 'meaning'})],
    'methods': ['participant observation', 'covert participant observation', 'non-participant observation', 'unstructured interview', 'semi-structured interview', 'questionnaire'],
    'source': [dict(text='A researcher spent a year in a school in {city}, attending lessons and spending break times with a group of Year 10 pupils. Pupils in the bottom set described school as “a joke” and gained respect from friends for answering back to teachers. Top-set pupils described their bottom-set peers as “wasting their chance”.',
                    method='participant observation', about='pupil subcultures', finds=['bottom-set pupils gained respect for answering back to teachers', 'top-set pupils described bottom-set peers as “wasting their chance”'],
                    persp='Interactionism', pview='The findings show polarisation: pupils labelled and placed in low sets suffer status frustration and form an anti-school subculture, while top-set pupils become pro-school (Lacey).',
                    claim='setting is the main cause of anti-school subcultures', pro='The source shows anti-school attitudes concentrated in the bottom set; Lacey and Ball link differentiation to polarisation.',
                    con='Willis shows class culture shapes subcultures before setting; Woods shows varied adaptations; the researcher’s presence may have changed behaviour; one school may be untypical.', flags={'young', 'behaviour'})],
    'essays': [('Explain two reasons why pupils form anti-school subcultures.', 'Status frustration (Lacey); labelling and setting; working-class culture and expectations (Willis); laddish masculinity; peer pressure.',
                'pupil subcultures are mainly a response to labelling and setting',
                'Lacey and Ball link differentiation to polarisation; labelling and status frustration.',
                'Willis: class culture and resistance; Woods’s range of adaptations; Fuller: subcultures that value success; gender and ethnicity shape subcultures; external factors.')],
})

CHAPTERS[6] = [e6a, e6b, e6c]


e7a = T('The formal curriculum, the hidden curriculum and what counts as knowledge')
build(e7a, {
    'terms': [
        ('formal curriculum', 'the subjects and content that schools officially teach and assess', 'mathematics, sciences and languages'),
        ('hidden curriculum', 'the unofficial lessons learnt through the organisation and routines of school', 'learning to wait your turn and respect authority'),
        ('stratification of knowledge', 'the ranking of some kinds of knowledge as higher status than others', 'academic subjects valued above vocational ones'),
        ('high-status knowledge', 'knowledge that is abstract, theoretical and associated with academic success and university entry', 'pure mathematics or classical literature'),
        ('national curriculum', 'a curriculum set by the state that all state schools must follow', 'compulsory subjects up to age 16'),
        ('sociology of knowledge', 'the study of how knowledge is socially produced and organised', 'asking why some subjects are compulsory'),
    ],
    'thinkers': [
        ('Young', 'what counts as valid knowledge in schools reflects the interests of powerful groups', 'Neo-Marxism',
         'Michael F.D. Young argued that high-status knowledge is abstract and written, and that the curriculum is organised to favour the middle class.',
         'Critics argue some knowledge is genuinely more powerful regardless of who defines it.'),
        ('Bernstein', 'the way knowledge is classified and framed shapes pupils’ experience of school', 'Neo-Marxism',
         'Bernstein distinguished strongly classified subjects with clear boundaries from integrated curricula, linking these to power and control.',
         'The concepts are abstract and difficult to apply empirically.'),
        ('Durkheim', 'the curriculum should transmit a shared culture and moral values', 'Functionalism',
         'Durkheim argued subjects such as history create a sense of shared identity and social solidarity.',
         'Marxists ask whose culture is transmitted.'),
    ],
    'explain': [
        ('Explain the difference between the formal curriculum and the hidden curriculum.', 'The formal curriculum is the official subjects and content taught and assessed; the hidden curriculum is the unofficial values and attitudes learnt through school routines and organisation, such as obedience and punctuality.', '1 mark each definition; 1 mark example or contrast. [3]'),
        ('Explain why some sociologists argue that the curriculum reflects the interests of powerful groups.', 'Powerful groups decide which subjects are compulsory and high-status; academic knowledge familiar to the middle class is valued above practical knowledge; the curriculum can transmit national or ruling-class ideology (Young, Bourdieu).', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('message', 'messages', 'that the hidden curriculum may teach pupils', ['accept hierarchy and authority', 'be punctual and follow rules', 'compete with others', 'boys and girls should behave differently', 'success comes from individual effort']),
    ],
    'claims': [
        ('The hidden curriculum is written down in the national curriculum.', False, 'It consists of unofficial lessons learnt through school routines, not written content.'),
        ('Some sociologists argue that academic subjects have higher status than vocational subjects.', True, 'Young argued abstract, academic knowledge is high-status and linked to power.'),
    ],
    'ar': ([('Academic subjects often have higher status than vocational subjects.', 'abstract, theoretical knowledge is valued for university entry.'),
            ('Functionalists support teaching national history.', 'shared history creates social solidarity.')],
           ['the hidden curriculum is the official list of subjects.', 'Young argued all knowledge has equal status in schools.']),
    'scen': ['The government in {city} makes coding compulsory for all pupils but removes art and drama from the core curriculum.',
             'In a school in {city}, pupils who take vocational courses are taught in a separate building and cannot study the subjects needed for university.'],
    'views': VE,
    'ctx': [('which subjects pupils see as most valuable', {'young', 'meaning', 'large'}),
            ('the hidden curriculum of school rules and routines', {'young', 'behaviour'})],
    'essays': [('Explain two features of the hidden curriculum.', 'Hierarchy and authority; punctuality and routine; competition and individualism; gender messages; acceptance of boredom; correspondence with work (Bowles and Gintis).',
                'the curriculum reflects the interests of the powerful',
                'Young: high-status knowledge favours the middle class; Marxists: ideology and hidden curriculum; ethnocentric and patriarchal curriculum; state decides content.',
                'Functionalists: curriculum transmits shared culture and skills; powerful knowledge benefits all pupils; teachers and pupils reinterpret the curriculum; content responds to the economy.')],
})

e7b = T('Ethnocentrism and power in curriculum design')
build(e7b, {
    'terms': [
        ('ethnocentrism', 'judging other cultures by the standards of one’s own and seeing one’s own culture as superior', 'a curriculum presenting colonisation as a civilising mission'),
        ('ethnocentric curriculum', 'a curriculum that reflects one culture and ignores or marginalises others', 'literature syllabuses with only majority-group authors'),
        ('multicultural education', 'education that recognises and values the cultures of all pupils', 'teaching about the festivals of several religions'),
        ('decolonising the curriculum', 'revising the curriculum to include perspectives and knowledge from formerly colonised peoples', 'adding African and Asian history to the syllabus'),
        ('cultural reproduction', 'the passing on of the dominant culture through education, reproducing inequality', 'schools rewarding the culture of the dominant group'),
    ],
    'thinkers': [
        ('Coard', 'an ethnocentric curriculum harms the self-esteem of black pupils', 'Neo-Marxism',
         'Coard argued British schools taught that white people were civilised and black people inferior, contributing to black pupils’ underachievement.',
         'Stone found black pupils did not necessarily have low self-esteem.'),
        ('Ball', 'national curricula can promote a “little Englander” view of history that ignores cultural diversity', 'Neo-Marxism',
         'Ball argued that curriculum content reflected a narrow, nationalist version of history.',
         'Curricula in many countries have since become more diverse.'),
        ('Troyna and Williams', 'schools often value the majority language and culture above those of minority pupils', 'Interactionism',
         'They argued schools gave priority to the majority language and dismissed minority languages and dialects.',
         'Many schools now offer community languages.'),
    ],
    'explain': [
        ('Explain how an ethnocentric curriculum may affect minority ethnic pupils.', 'It marginalises their history and culture, which may lower self-esteem (Coard); pupils may feel excluded and disengage; it reinforces stereotypes among all pupils; it may lead to underachievement.', '1 mark each developed point up to 3. [3]'),
        ('Explain who has the power to decide what is in the curriculum.', 'Governments set national curricula; exam boards decide syllabuses; powerful groups influence what is seen as valid knowledge; teachers and schools interpret content; international organisations and businesses increasingly influence it.', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which a curriculum could be made less ethnocentric', ['include history from different parts of the world', 'include literature by authors from minority groups', 'teach about a range of religions', 'offer community languages', 'present colonisation from the perspective of the colonised']),
    ],
    'claims': [
        ('An ethnocentric curriculum values all cultures equally.', False, 'It reflects one culture and marginalises others.'),
        ('Governments have considerable power over what is taught in state schools.', True, 'They set national curricula and approve syllabuses.'),
    ],
    'ar': ([('Some pupils may disengage from an ethnocentric curriculum.', 'they do not see their own history and culture reflected in it.'),
            ('Curriculum content can be political.', 'decisions about what to teach reflect power and values.')],
           ['an ethnocentric curriculum gives equal weight to all cultures.', 'exam boards have no influence on what pupils learn.']),
    'scen': ['A campaign group in {city} calls for the school history syllabus to include the experiences of colonised peoples and migrants.',
             'In {city}, the only language other than the national language offered at school is French, although many pupils speak Urdu, Tamil or Arabic at home.'],
    'views': {'Functionalism': 'a shared curriculum promotes social solidarity and integration into a common national culture (Durkheim).',
              'Marxism': 'the curriculum reflects the culture and interests of dominant groups and contributes to cultural reproduction and inequality.',
              'Neo-Marxism': 'critical race theorists argue an ethnocentric curriculum is part of institutional racism that disadvantages minority pupils (Gillborn, Coard).',
              'Postmodernism': 'in a diverse society there is no single valid body of knowledge; curricula should reflect many cultures and perspectives.'},
    'ctx': [('representations of different cultures in school textbooks', {'media', 'meaning', 'change'}),
            ('minority ethnic pupils’ views of the curriculum', {'young', 'meaning', 'sensitive'})],
    'methods': ['content analysis', 'questionnaire', 'unstructured interview', 'semi-structured interview', 'case study'],
    'data': [dict(what='representation in textbooks', pop='textbook images', rows=['Majority ethnic group', 'Minority ethnic groups'], cols=('2000', '2025'), complement=True, nocount=True, n=[300, 400, 500, 600],
                  base=[(80, 90), (10, 20)], delta=[(-15, -5), (5, 15)], label='percentage of people shown in history textbook images',
                  leads=['A content analysis of {n} images in history textbooks used in {city} produced the following results.', '{person} coded {n} images from history textbooks used in {city} schools.'],
                  expl=['campaigns for more diverse curricula have influenced publishers', 'policies of multicultural education', 'decolonising movements in universities and schools'],
                  method='content analysis', claim='the curriculum has become less ethnocentric', flags={'media'},
                  counter='The majority group still dominates images; numbers of images do not show how groups are represented; textbooks are only part of the curriculum.')],
    'essays': [('Explain two ways in which the curriculum may be ethnocentric.', 'History focusing on the majority nation; literature from one culture; religious education focused on one faith; language priorities; textbook images.',
                'the ethnocentric curriculum is a major cause of underachievement among minority ethnic pupils',
                'Coard: lowered self-esteem; disengagement; institutional racism (Gillborn); Troyna and Williams on language.',
                'Some minorities achieve highly despite the curriculum; Stone: self-esteem not necessarily low; class and material factors; curricula are becoming more diverse.')],
})

e7c = T('Applying research methods to the study of education')
build(e7c, {
    'research': True,
    'terms': [
        ('pupils as research subjects', 'the particular issues of researching children and young people, such as power, consent and vulnerability', 'needing parental consent to interview pupils'),
        ('gatekeeper', 'a person who controls access to a research setting, such as a head teacher', 'a head teacher deciding whether a researcher may observe lessons'),
        ('classroom observation', 'observing interaction in lessons to study processes such as labelling', 'recording how often teachers praise different pupils'),
        ('school documents', 'official records produced by schools, such as reports, policies and exclusion records', 'inspection reports and pupil records'),
        ('league table data', 'published statistics on schools’ exam results', 'percentage of pupils gaining top grades'),
        ('peer pressure in research', 'the tendency of pupils to answer in ways that impress their peers in group interviews', 'boys exaggerating anti-school attitudes in front of friends'),
    ],
    'thinkers': [
        ('Hey', 'girls’ friendships could be studied using notes passed in class', 'Liberal feminism',
         'Valerie Hey used observation and girls’ notes to study friendship groups.',
         'Notes were obtained without the consent of all writers.'),
        ('Willis', 'participant observation and interviews can reveal how pupils experience school', 'Neo-Marxism',
         'Willis combined observation, group discussions and interviews with 12 lads.',
         'Small sample and possible over-identification with the lads.'),
        ('Gillborn', 'official statistics and school records can reveal patterns of institutional racism', 'Neo-Marxism',
         'Gillborn used assessment and setting data to show how black pupils were placed lower than their test results would predict.',
         'Statistics do not show the reasons behind teachers’ decisions.'),
    ],
    'explain': [
        ('Explain two problems of using participant observation to study classrooms.', 'Gaining access through gatekeepers; adults cannot easily pass as pupils, so observation is usually overt and the Hawthorne effect is likely; teachers may change their behaviour; time-consuming; small samples.', '2 marks for each explained problem. [4]'),
        ('Explain two ethical issues in researching pupils.', 'Informed consent from pupils and parents; vulnerability and power imbalance; confidentiality and safeguarding duties; avoiding harm or distress; right to withdraw.', '2 marks for each explained issue. [4]'),
        ('Explain why official statistics on education are useful to sociologists.', 'Freely available, large-scale and regularly collected; allow comparisons of achievement by class, gender and ethnicity; show trends over time; allow evaluation of policies.', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('problem', 'problems', 'of using questionnaires with pupils', ['young pupils may not understand questions', 'pupils may answer to please teachers or impress peers', 'questionnaires given in class may not feel anonymous', 'low reading ability may affect responses']),
    ],
    'claims': [
        ('Researchers do not need permission to observe lessons.', False, 'They need access through gatekeepers such as head teachers, and consent from teachers, pupils and parents.'),
        ('Group interviews with pupils may be affected by peer pressure.', True, 'Pupils may give answers to impress friends.'),
    ],
    'ar': ([('Observation of lessons can produce the Hawthorne effect.', 'teachers and pupils know they are being watched.'),
            ('Official education statistics allow comparisons between groups.', 'they record results by gender, ethnicity and free school meal eligibility.')],
           ['covert participant observation in classrooms is easy for adult researchers.', 'pupils can always give informed consent without parents’ involvement.']),
    'scen': ['{person} plans to sit at the back of Year 9 lessons in a school in {city} for a term, counting how often teachers praise boys and girls.',
             'A researcher in {city} wants to interview 14-year-olds about bullying, using groups of five friends at a time.'],
    'views': {'Positivism': 'research on education should use reliable, quantitative methods such as official statistics and structured questionnaires to identify patterns of achievement and test hypotheses.',
              'Interpretivism': 'to understand processes such as labelling and subcultures, researchers need qualitative methods such as observation and unstructured interviews that capture meanings in classrooms.',
              'Feminism': 'research should give a voice to pupils whose experiences are overlooked, such as girls, and use sensitive, non-hierarchical methods.'},
    'ctx': [('teacher labelling in classrooms', {'young', 'behaviour', 'meaning'}),
            ('pupils’ experiences of bullying', {'young', 'sensitive', 'hidden'}),
            ('national patterns of educational achievement', {'large', 'change'}),
            ('the views of parents on school choice', {'meaning', 'large'})],
    'methods': ['questionnaire', 'structured interview', 'unstructured interview', 'semi-structured interview', 'participant observation', 'non-participant observation', 'official statistics', 'personal documents', 'longitudinal study', 'case study', 'field experiment'],
    'essays': [('Explain two reasons why sociologists might use observation to study schools.', 'To see labelling and interaction as it happens; to gain validity and verstehen; to study subcultures; to avoid relying on what teachers and pupils say.',
                'qualitative methods are the most useful for studying education',
                'Observation and interviews reveal labelling, subcultures and meanings (Willis, Ball, Lacey, Fuller); validity; interactionist preference.',
                'Official statistics show national patterns (Gillborn uses data); questionnaires reach large samples; qualitative studies are small and hard to generalise; ethical and access problems with pupils; mixed methods.')],
})
classify(e7c, [
    ('{person} uses published exam results for every school in {city} to compare achievement by gender.', 'Official statistics', 'published, secondary quantitative data.'),
    ('A researcher spends a year in a school in {city}, attending lessons and joining pupils at lunchtimes.', 'Participant observation', 'the researcher takes part in the life of the group.'),
    ('{person} hands a pre-coded questionnaire to {n} pupils in five schools in {city}.', 'Questionnaire', 'a standardised set of written questions completed by respondents.'),
    ('A sociologist has long, informal conversations with 15 teachers in {city} about how they decide which set pupils go in.', 'Unstructured interview', 'informal, in-depth conversation without a fixed schedule.'),
    ('A research team follows {n} children in {city} from age 5 to age 18, testing and interviewing them every three years.', 'Longitudinal study', 'the same sample is studied over time.'),
], ['Official statistics', 'Participant observation', 'Questionnaire', 'Unstructured interview', 'Longitudinal study', 'Field experiment'], 'Which research method is being used?', C='C3', D=(1, 2))

CHAPTERS[7] = [e7a, e7b, e7c]


# ============================================================== GLOBALISATION (chapters 8-13)

VG = {
    'Hyperglobalism': 'globalisation is a powerful, real and largely irreversible process: a borderless global economy and culture are emerging, and nation-states are losing power to global markets and corporations (Ohmae).',
    'Globalisation scepticism': 'globalisation is exaggerated: most trade and investment is still regional, nation-states remain powerful, and current levels of integration are not unprecedented (Hirst and Thompson).',
    'Transformationalism': 'globalisation is real and transforming societies, but its effects are uneven and contested; nation-states adapt and share power with global institutions rather than disappearing (Held, Giddens).',
    'Marxism': 'globalisation is the spread of capitalism worldwide: transnational corporations exploit cheap labour and resources in poorer countries, increasing global inequality (Wallerstein, Sklair).',
    'Neoliberalism': 'free trade, open markets and private enterprise spread wealth and development; globalisation benefits all countries that open their economies.',
}
VD = {
    'Modernisation theory': 'poorer countries are underdeveloped because of traditional values and institutions; they can develop by adopting Western values, investment, education and industrialisation, passing through stages of growth (Rostow, Parsons).',
    'Dependency theory': 'poorer countries are underdeveloped because they were exploited by colonialism and remain dependent on richer countries through trade, debt and TNCs; the core develops at the expense of the periphery (Frank).',
    'World-systems theory': 'the world is a single capitalist system of core, semi-periphery and periphery; countries can move between positions, but the system keeps inequality (Wallerstein).',
    'Neoliberalism': 'development comes from free markets, free trade, privatisation and reduced state spending; aid and state intervention distort markets (structural adjustment, IMF and World Bank).',
    'Post-development theory': 'the Western idea of development is itself a problem: it imposes Western values and ignores local knowledge, so communities should define their own goals (Escobar, Sachs).',
}

g8a = T('Economic, political and cultural globalisation')
build(g8a, {
    'terms': [
        ('globalisation', 'the growing interconnectedness of societies worldwide, so that events in one place affect people far away', 'a financial crisis in one country causing job losses in many others'),
        ('economic globalisation', 'the integration of national economies through trade, investment, finance and production across borders', 'a smartphone designed in one country and assembled in another'),
        ('political globalisation', 'the growth of international organisations and agreements that shape decisions beyond the nation-state', 'climate agreements negotiated by the United Nations'),
        ('cultural globalisation', 'the spread of cultural products, ideas, values and lifestyles across the world', 'the same films, music and brands being popular in many countries'),
        ('transnational corporation', 'a company that operates in many countries and organises production on a global scale', 'a car maker with factories on four continents'),
        ('global division of labour', 'the organisation of production so that different stages take place in different countries', 'clothes designed in Europe and sewn in South Asia'),
        ('interdependence', 'the situation in which countries rely on one another for goods, services and investment', 'a country depending on imported food and exported oil'),
    ],
    'thinkers': [
        ('Giddens', 'globalisation intensifies worldwide social relations so that local events are shaped by events far away', 'Transformationalism',
         'Giddens defined globalisation as the intensification of worldwide social relations linking distant localities, driven by communication technology.',
         'Critics argue globalisation is uneven and many people remain little affected.'),
        ('Ohmae', 'the nation-state is becoming irrelevant in a borderless world economy', 'Hyperglobalism',
         'Ohmae argued global markets and corporations, not governments, now drive economic life.',
         'Sceptics show states still control borders, taxation and regulation.'),
        ('Held', 'globalisation has economic, political, cultural and military dimensions that are transforming the world', 'Transformationalism',
         'Held and colleagues argued globalisation is multi-dimensional and reshapes state power rather than ending it.',
         'Hyperglobalists argue the decline of the state is more advanced.'),
        ('Ritzer', 'the principles of the fast-food restaurant are spreading to more and more sectors of society worldwide', 'Neo-Marxism',
         'Ritzer’s McDonaldisation thesis identifies efficiency, calculability, predictability and control as spreading across cultures.',
         'Critics argue local cultures adapt global products (glocalisation).'),
    ],
    'explain': [
        ('Explain the difference between economic and cultural globalisation, using an example of each.', 'Economic globalisation: integration of production, trade and finance (e.g. global supply chains); cultural globalisation: spread of cultural products and values (e.g. global music streaming and brands).', '1 mark each definition; 1 mark each example. [4]'),
        ('Explain two factors that have driven globalisation.', 'Communication technology and the internet; cheaper transport (containerisation, air travel); trade liberalisation and neoliberal policies; growth of TNCs; international organisations.', '2 marks for each explained factor. [4]'),
    ],
    'why': [
        ('example', 'examples', 'of political globalisation', ['the growth of the United Nations and its agencies', 'regional blocs such as the European Union', 'international climate agreements', 'the International Criminal Court', 'global social movements influencing governments']),
    ],
    'claims': [
        ('Globalisation only refers to economic change.', False, 'It also has political, cultural and military dimensions.'),
        ('Communication technology has been a key driver of globalisation.', True, 'The internet and satellites allow instant contact and global coordination.'),
    ],
    'ar': ([('Events in one country can affect people around the world.', 'societies have become increasingly interconnected through globalisation.'),
            ('Cultural products spread rapidly around the world.', 'digital media allow films and music to be streamed globally.')],
           ['globalisation means that all countries have become equally wealthy.', 'political globalisation refers only to trade between companies.']),
    'scen': ['A clothing company based in one country designs its products there, buys cotton from a second country, sews garments in {city} and sells them online worldwide.',
             'Young people in {city} watch the same streaming series, follow the same influencers and wear the same brands as young people in dozens of other countries.'],
    'views': VG,
    'ctx': [('how far young people in {city} feel part of a global culture', {'meaning', 'large'}),
            ('the effects of global supply chains on workers', {'meaning', 'behaviour', 'hidden'})],
    'data': [dict(what='economic globalisation', pop='countries', rows=['Trade as % of GDP: Country A', 'Trade as % of GDP: Country B', 'Trade as % of GDP: Country C'], cols=('1990', '2020'), unit='%', nocount=True, n=[3],
                  base=[(20, 35), (40, 60), (60, 80)], delta=[(10, 30), (5, 25), (-5, 15)], label='trade (exports + imports) as a percentage of GDP',
                  leads=['The table shows official data on trade for three countries studied by {person}.', 'Official statistics on trade for three countries are shown below.'],
                  expl=['trade liberalisation and neoliberal policies have opened economies', 'TNCs organise production across borders', 'cheaper transport and communication'],
                  method='official statistics', claim='economic globalisation has transformed national economies',
                  counter='Sceptics note trade is often regional rather than global; some economies were already very open; statistics do not show who benefits.')],
    'essays': [('Explain two dimensions of globalisation.', 'Economic (trade, TNCs, finance); political (international organisations, global governance); cultural (media, consumption, migration); military; environmental.',
                'globalisation is mainly an economic process',
                'Growth of trade, TNCs, global finance and supply chains; Marxists see globalisation as global capitalism; economic forces drive cultural and political change.',
                'Cultural globalisation (media, migration, McDonaldisation); political globalisation (UN, EU, global movements); transformationalists stress many dimensions; technology drives all dimensions.')],
})

g8b = T('Hyperglobalist, sceptic and transformationalist views')
build(g8b, {
    'terms': [
        ('hyperglobalism', 'the view that globalisation is a real, powerful process creating a borderless world in which nation-states are losing power', 'claims that markets now matter more than governments'),
        ('globalisation scepticism', 'the view that globalisation is exaggerated and that nation-states and regional economies remain dominant', 'pointing out that most trade is within regions'),
        ('transformationalism', 'the view that globalisation is real and significant but uneven, reshaping rather than replacing the nation-state', 'states pooling sovereignty in the EU'),
        ('borderless world', 'Ohmae’s idea that national borders are becoming irrelevant to economic activity', 'companies moving capital instantly across the world'),
        ('regionalisation', 'the concentration of trade and investment within regional blocs rather than truly global flows', 'most trade taking place within Europe, North America and East Asia'),
        ('global governance', 'the institutions and rules that regulate issues across national borders', 'the WTO, UN and international treaties'),
    ],
    'thinkers': [
        ('Ohmae', 'nation-states have become “unnatural” business units in a borderless world economy', 'Hyperglobalism',
         'Ohmae argued global consumers, TNCs and markets have made national economies and governments far less important.',
         'States still control taxation, borders and regulation, and intervened strongly in the 2008 financial crisis.'),
        ('Hirst and Thompson', 'the extent of globalisation has been exaggerated', 'Globalisation scepticism',
         'Hirst and Thompson argued the world economy was as open before 1914, most TNCs have a clear home base, and trade is concentrated in a few regions.',
         'Critics argue they underestimated new forms of digital and financial globalisation.'),
        ('Held', 'globalisation is transforming societies, but its outcomes are uncertain and uneven', 'Transformationalism',
         'Held and colleagues argued globalisation reshapes state power and creates new forms of global governance.',
         'Hyperglobalists and sceptics argue it is either more or less powerful than transformationalists claim.'),
    ],
    'explain': [
        ('Explain the difference between the hyperglobalist and sceptic views of globalisation.', 'Hyperglobalists see globalisation as real and powerful, creating a borderless world where nation-states decline (Ohmae); sceptics argue it is exaggerated, trade is regional and states remain powerful (Hirst and Thompson).', '1 mark each view; 1 mark explicit contrast. [3]'),
        ('Explain the transformationalist view of globalisation.', 'Globalisation is real and significant, but uneven and open-ended; it reshapes rather than ends state power, creating global governance; local cultures adapt global influences (Held, Giddens).', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('argument', 'arguments', 'used by sceptics to challenge claims about globalisation', ['most trade is regional rather than global', 'TNCs keep a clear national home base', 'the world economy was very open before 1914', 'nation-states still control borders, taxes and laws', 'many people remain unaffected by global culture']),
    ],
    'claims': [
        ('Sceptics argue nation-states have lost most of their power.', False, 'Sceptics argue states remain powerful; it is hyperglobalists who claim states are declining.'),
        ('Transformationalists see globalisation as uneven.', True, 'Its effects vary between countries and groups.'),
    ],
    'ar': ([('Hyperglobalists argue nation-states are declining.', 'global markets and corporations operate beyond the control of governments.'),
            ('Sceptics point to regionalisation.', 'most trade and investment takes place within regional blocs.')],
           ['transformationalists argue globalisation is a myth.', 'Ohmae argued that national borders are becoming more important to business.']),
    'scen': ['During a global financial crisis, governments around the world spend billions to rescue banks in their own countries.',
             'A large technology company in {city} pays very little tax there by recording its profits in a country with low tax rates.'],
    'views': {'Hyperglobalism': VG['Hyperglobalism'], 'Globalisation scepticism': VG['Globalisation scepticism'], 'Transformationalism': VG['Transformationalism']},
    'ctx': [('the power of national governments over large corporations', {'large', 'change', 'hidden'}),
            ('public attitudes to globalisation', {'large', 'meaning'})],
    'data': [dict(what='regional and global trade', pop='regions', rows=['Europe', 'Asia', 'North America'], cols=('2000', '2020'), nocount=True, n=[3],
                  base=[(65, 72), (48, 55), (45, 52)], delta=[(-6, 2), (0, 8), (-10, -2)], label='share of each region’s exports going to countries in the same region (%)',
                  leads=['The table shows the destination of exports for three regions, from international trade statistics.', 'International trade data show where three regions’ exports go.'],
                  expl=['sceptics point to regionalisation: much trade stays within regional blocs', 'regional trade agreements and geography encourage regional trade',
                        'hyperglobalists would note the large share traded globally'],
                  method='official statistics', claim='globalisation is exaggerated because most trade is regional',
                  counter='Global supply chains, digital trade and finance are not captured by export shares; some regions trade mainly with the rest of the world.')],
    'essays': [('Explain two arguments of globalisation sceptics.', 'Regionalisation of trade (Hirst and Thompson); TNCs have home bases; states remain powerful; historical precedent before 1914; cultural globalisation is limited.',
                'nation-states are losing their power as a result of globalisation',
                'Hyperglobalists (Ohmae): TNCs and markets beyond state control; tax avoidance; global institutions; capital mobility.',
                'Sceptics (Hirst and Thompson): states still regulate and tax; strong states in crises; transformationalists: power is reshaped not lost; nationalism and border controls are growing.')],
})

g8c = T('Time-space compression and the role of communication technology')
build(g8c, {
    'terms': [
        ('time-space compression', 'the shrinking of the world as communication and transport technologies reduce the time it takes to connect distant places', 'a video call between continents in real time'),
        ('network society', 'Castells’s term for a society organised around digital networks of information', 'global financial markets operating online 24 hours a day'),
        ('digital divide', 'unequal access to digital technologies between and within countries', 'rural areas without reliable internet'),
        ('global village', 'McLuhan’s idea that electronic media make the world feel like a single community', 'people across the world watching the same live event'),
        ('disembedding', 'Giddens’s term for the lifting out of social relations from local contexts', 'friendships maintained entirely online'),
    ],
    'thinkers': [
        ('Harvey', 'capitalism drives time-space compression to speed up production and profit', 'Marxism',
         'Harvey argued time-space compression results from capitalism’s need to reduce turnover time of capital.',
         'Others see technology and culture as independent drivers.'),
        ('Castells', 'societies are increasingly organised as networks of information flows', 'Transformationalism',
         'Castells argued power in the network society depends on control of information networks.',
         'Access to networks is very unequal (digital divide).'),
        ('McLuhan', 'electronic media turn the world into a global village', 'Hyperglobalism',
         'McLuhan argued that “the medium is the message”: new media change how people experience the world and bring them closer.',
         'Critics argue the internet can also fragment communities into “echo chambers”.'),
    ],
    'explain': [
        ('Explain what is meant by time-space compression, using an example.', 'The world seems to shrink because communication and transport technologies reduce the time needed to connect distant places, e.g. instant messaging, live global broadcasts or fast air travel.', '1 mark meaning; 1 mark technology; 1 mark example. [3]'),
        ('Explain two ways in which communication technology has contributed to globalisation.', 'Instant communication allows global business and finance; social media spreads culture and ideas; diasporas stay connected; global social movements organise online; news travels instantly.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('effect', 'effects', 'of the digital divide', ['poorer countries and groups are excluded from online economic opportunities', 'unequal access to education and information', 'reduced political voice for those offline', 'reinforcement of existing inequalities']),
    ],
    'claims': [
        ('Everyone in the world has equal access to the internet.', False, 'There is a large digital divide between and within countries.'),
        ('Time-space compression means distance matters less for communication.', True, 'Technology allows instant contact over long distances.'),
    ],
    'ar': ([('Global financial markets operate around the clock.', 'digital networks allow trading across time zones instantly.'),
            ('The digital divide can increase inequality.', 'those without internet access miss out on economic and educational opportunities.')],
           ['time-space compression means travel takes longer than in the past.', 'McLuhan argued electronic media isolate people from one another.']),
    'scen': ['A family in {city} speaks daily by video call with relatives in three other countries and sends money to them through a phone app.',
             'In a rural region near {city}, only one household in five has internet access, while in the city centre almost every home is connected.'],
    'views': VG,
    'ctx': [('how migrants use technology to keep in touch with family', {'meaning', 'behaviour'}),
            ('internet access in rural and urban areas', {'large', 'change'})],
    'data': [dict(what='internet use', pop='adults', rows=['High-income countries', 'Middle-income countries', 'Low-income countries'], cols=('2010', '2023'), nocount=True,
                  base=[(65, 75), (20, 30), (3, 8)], delta=[(15, 25), (30, 45), (15, 25)], label='percentage of adults using the internet',
                  leads=['International data (based on surveys of about {n} adults per country group) show internet use.', 'The table shows internet use from international surveys of around {n} adults in each group of countries.'],
                  expl=['falling cost of mobile phones has spread internet access', 'infrastructure investment is lower in poorer countries', 'the digital divide reflects global inequality'],
                  method='official statistics', claim='the digital divide is closing',
                  counter='The gap in percentage points between rich and poor countries remains large; access does not mean equal quality or skills; rural and gender gaps persist within countries.')],
    'essays': [('Explain two ways in which communication technology has changed social relationships.', 'Time-space compression; disembedding (Giddens); network society (Castells); transnational families; online communities; global social movements.',
                'communication technology has made the world a global village',
                'Instant global communication; shared media events; migrants maintain links; social movements organise globally (McLuhan, Castells).',
                'Digital divide; echo chambers and fragmentation; state censorship; inequality of access; local cultures remain important.')],
})

CHAPTERS[8] = [g8a, g8b, g8c]


g9a = T('Defining and measuring development')
build(g9a, {
    'terms': [
        ('development', 'a process of economic, social and political change that improves people’s living standards and life chances', 'rising incomes, better health and education'),
        ('gross national income per capita', 'the total income of a country divided by its population, used as a measure of average income', '$12,000 per person per year'),
        ('Human Development Index', 'a UN measure combining life expectancy, education and income per head', 'a country with an HDI of 0.85'),
        ('underdevelopment', 'the condition of countries with low income, poor health and limited industrialisation, which dependency theorists see as caused by exploitation', 'a country dependent on exporting one cash crop'),
        ('Sustainable Development Goals', 'UN targets agreed in 2015 to reduce poverty, inequality and environmental damage by 2030', 'a goal to end extreme poverty'),
        ('Global South', 'a term for poorer, mainly formerly colonised countries in Africa, Asia and Latin America', 'countries sometimes called developing countries'),
        ('multidimensional poverty', 'poverty measured by several deprivations, such as health, education and living standards, not income alone', 'lacking clean water, schooling and electricity'),
    ],
    'thinkers': [
        ('Sen', 'development should be seen as expanding people’s freedoms and capabilities', 'Transformationalism',
         'Amartya Sen argued development means expanding capabilities such as health, education and political freedom, not just income; this influenced the HDI.',
         'Capabilities are hard to measure and compare between cultures.'),
        ('Rostow', 'societies develop through five stages of economic growth', 'Modernisation theory',
         'Rostow’s stages run from traditional society through take-off to the age of high mass consumption.',
         'Dependency theorists argue it ignores exploitation and history.'),
        ('Escobar', 'the Western concept of development has been imposed on the Global South', 'Post-development theory',
         'Escobar argued that development discourse defined poorer countries as “backward” and justified intervention by Western experts.',
         'Critics argue many people in poorer countries do want better health, income and education.'),
    ],
    'explain': [
        ('Explain two limitations of using GNI per capita to measure development.', 'It is an average that hides inequality; it ignores non-market activity such as subsistence farming; it does not measure health, education or freedom; exchange rates distort comparisons; it ignores environmental damage.', '2 marks for each explained limitation. [4]'),
        ('Explain why the Human Development Index may be a better measure of development than income alone.', 'It combines life expectancy, education and income, so it reflects people’s quality of life and capabilities (Sen), not just economic output.', '1 mark components; 1 mark capabilities/quality of life; 1 mark contrast with income. [3]'),
    ],
    'why': [
        ('indicator', 'indicators', 'of social development', ['life expectancy', 'infant mortality rate', 'literacy rate', 'school enrolment', 'access to clean water', 'gender equality measures']),
    ],
    'claims': [
        ('GNI per capita shows how income is distributed within a country.', False, 'It is an average and hides inequality.'),
        ('The HDI combines measures of health, education and income.', True, 'It was influenced by Sen’s capabilities approach.'),
        ('Post-development theorists reject the Western idea of development.', True, 'They argue it imposes Western values and ignores local knowledge.'),
    ],
    'ar': ([('Two countries with similar GNI per capita can have different HDI scores.', 'HDI also includes health and education.'),
            ('Some sociologists criticise economic measures of development.', 'income alone does not show people’s quality of life.')],
           ['the HDI measures only economic growth.', 'GNI per capita shows the income of the poorest people.']),
    'scen': ['Country X has a higher GNI per capita than Country Y, but lower life expectancy and literacy rates.',
             'An oil-rich state near {city} has rapidly rising average income, but most of the wealth goes to a small elite.'],
    'views': VD,
    'ctx': [('living standards in rural communities in the Global South', {'meaning', 'large', 'hidden'}),
            ('changes in development indicators over thirty years', {'large', 'change'})],
    'data': [dict(what='development indicators', pop='countries', rows=['Country A', 'Country B', 'Country C'], cols=('1990', '2020'), unit='', uname='years', nocount=True, n=[3],
                  base=[(45, 55), (55, 65), (68, 75)], delta=[(8, 18), (5, 12), (2, 6)], label='life expectancy at birth (years)',
                  leads=['The table shows life expectancy in three countries, from official international data.', '{person} collected life expectancy data for three countries from international statistics.'],
                  expl=['improved health care, vaccination and clean water', 'rising incomes and education', 'aid programmes targeting disease'],
                  method='official statistics', claim='development is improving people’s lives in poorer countries',
                  counter='Gaps remain large; averages hide inequality within countries; life expectancy is one indicator only; data quality may vary.')],
    'essays': [('Explain two ways of measuring development.', 'GNI per capita; HDI; multidimensional poverty index; social indicators (literacy, infant mortality); gender development measures; happiness or well-being indices.',
                'economic measures are the best way to measure development',
                'GNI per capita is widely available, comparable and linked to resources; modernisation and neoliberal theories see growth as central.',
                'Sen’s capabilities and the HDI; inequality hidden by averages; post-development critiques; environmental costs; cultural definitions of a good life.')],
})


@g9a.add('C3', (1, 2, 3, 4, 5), 'numerical')
def g9a_gni(r, D):
    for _ in range(40):
        pa, pb = r.choice([20, 25, 40, 50, 60, 80]), r.choice([5, 8, 10, 12, 15, 30])
        ga, gb = pa * r.choice([500, 800, 1200, 2000, 3500]), pb * r.choice([6000, 9000, 15000, 25000, 40000])
        ca, cb = ga // pa, gb // pb
        if ca != cb:
            break
    d = ctxd(r)
    intro = f'Country A has a population of {pa} million and a gross national income (GNI) of ${ga:,} million. Country B has a population of {pb} million and a GNI of ${gb:,} million.'
    if D <= 1:
        ans = f'${ca:,}'
        ds = [f'${x:,}' for x in {ga, ca * 10, ca // 10 if ca // 10 else ca + 100, cb} if x != ca]
        opts, a = mcq(r, ans, ds)
        return {'stem': f'{intro} What is the GNI per capita of Country A?', 'options': opts, 'answer': a, 'key': f'${ga:,} million ÷ {pa} million = ${ca:,}. [1]', 'marks': 1}
    hi, lo = max(ca, cb), min(ca, cb)
    parts = [('Calculate the GNI per capita of each country.', f'A: {ga:,} ÷ {pa} = ${ca:,}; B: {gb:,} ÷ {pb} = ${cb:,}.', '1 mark each. [2]'),
             ('How many times greater is the higher GNI per capita than the lower? Give your answer to 1 decimal place.', f'{hi:,} ÷ {lo:,} = {hi / lo:.1f} times.', '1 mark method; 1 mark answer. [2]'),
             ('Explain one reason why GNI per capita may not give an accurate picture of living standards in these countries.', 'It is an average and hides inequality; it ignores subsistence and informal activity; it does not measure health, education or freedom; prices differ between countries.', '1 mark identifying; 1 mark explaining. [2]'),
             ('Explain how a dependency theorist might explain the difference between the two countries.', 'The poorer country may have been exploited through colonialism and remain dependent on exporting raw materials and on TNCs and debt, so wealth flows to the core (Frank).', '1 mark dependency idea; 1 mark application. [2]'),
             ('Explain how a modernisation theorist might explain the difference between the two countries.', 'The poorer country has not yet passed through the stages of growth; traditional values and lack of investment, education and technology hold it back (Rostow).', '1 mark modernisation idea; 1 mark application. [2]')]
    if D == 2:
        sel = parts[:2]
    elif D == 3:
        sel = parts[:3]
    else:
        sel = parts[:2] + [parts[2], r.choice(parts[3:])] if D == 4 else parts
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


_reg(g9a, 'C3', (1, 2, 3, 4, 5), 'numerical', g9a_gni, 'gni_pc')

g9b = T('Modernisation theory')
build(g9b, {
    'terms': [
        ('modernisation theory', 'the theory that poorer countries can develop by adopting Western values, institutions, technology and investment', 'a country building factories with Western aid'),
        ('traditional values', 'values such as fatalism, collectivism and ascribed status, which modernisation theorists saw as barriers to development', 'people accepting their position as fate'),
        ('stages of economic growth', 'Rostow’s five stages through which he believed all societies pass on the way to mass consumption', 'traditional society, preconditions, take-off, drive to maturity, mass consumption'),
        ('take-off', 'Rostow’s stage in which investment rises sharply and industry grows rapidly', 'a country experiencing rapid industrial growth'),
        ('trickle-down', 'the idea that the benefits of economic growth will eventually spread to the poor', 'new factory jobs raising incomes across a region'),
        ('Green Revolution', 'the use of new high-yield seeds, fertilisers and irrigation to increase food production in developing countries', 'India’s wheat yields rising in the 1960s'),
    ],
    'thinkers': [
        ('Rostow', 'all societies pass through five stages of economic growth', 'Modernisation theory',
         'Rostow argued Western aid and investment could help societies reach take-off and eventually high mass consumption.',
         'Frank argued underdevelopment is caused by exploitation, not traditional values.'),
        ('Parsons', 'traditional values such as particularism and ascribed status are barriers to development', 'Modernisation theory',
         'Parsons argued that development requires a shift to universalistic values, achieved status and individualism.',
         'This is ethnocentric, treating Western values as superior.'),
        ('Inkeles', 'education and mass media spread “modern” attitudes that promote development', 'Modernisation theory',
         'Inkeles argued modern people are open to new experiences, value education and plan for the future.',
         'Critics argue it blames poorer societies for their poverty.'),
    ],
    'explain': [
        ('Explain two features of modernisation theory.', 'Development is a single path following the West; traditional values are barriers; Western aid, investment and technology are needed; stages of growth (Rostow); education and media spread modern values.', '2 marks for each explained feature. [4]'),
        ('Explain two criticisms of modernisation theory.', 'It is ethnocentric, assuming Western societies are the model; it ignores colonial exploitation and dependency; aid has often benefited elites or donors; trickle-down has not happened; environmental costs of growth.', '2 marks for each explained criticism. [4]'),
    ],
    'why': [
        ('role', 'roles', 'that modernisation theorists give to the West in development', ['providing aid to fund investment', 'investment by Western companies', 'exporting technology and expertise', 'educating elites who spread modern values', 'promoting democracy and free markets']),
    ],
    'claims': [
        ('Modernisation theory argues that traditional values help development.', False, 'It sees traditional values as barriers to development.'),
        ('Rostow’s model includes a stage called take-off.', True, 'Take-off is when investment and industry grow rapidly.'),
    ],
    'ar': ([('Modernisation theorists support Western aid.', 'they believe poorer countries need capital and technology to reach take-off.'),
            ('Modernisation theory is criticised as ethnocentric.', 'it assumes Western societies are the model for all others.')],
           ['Rostow argued development begins with the age of high mass consumption.', 'modernisation theory blames colonialism for underdevelopment.']),
    'scen': ['A government near {city} invites Western companies to build factories and sends students abroad to study engineering, hoping to “catch up” with rich countries.',
             'A village near {city} receives high-yield seeds and fertiliser through an aid programme; harvests increase but poorer farmers fall into debt.'],
    'views': VD,
    'ctx': [('the effects of foreign aid on a rural community', {'meaning', 'change'}),
            ('attitudes to “modern” and “traditional” values', {'meaning', 'large'})],
    'essays': [('Explain two ways in which modernisation theorists argue that poorer countries can develop.', 'Adopting modern values; Western aid and investment; education and mass media; industrialisation; urbanisation; stages of growth.',
                'modernisation theory provides an adequate explanation of development',
                'Success of East Asian economies; role of investment, education and technology; the Green Revolution increased food output.',
                'Dependency theory (Frank): exploitation; ethnocentrism; aid benefits elites; environmental damage; post-development critique; neoliberal emphasis on markets instead of aid.')],
})

g9c = T('Dependency and world-systems theories')
build(g9c, {
    'terms': [
        ('dependency theory', 'the theory that poorer countries are underdeveloped because they have been exploited by richer countries through colonialism and unequal trade', 'a former colony exporting raw materials cheaply'),
        ('metropolis and satellite', 'Frank’s terms for rich, dominant countries and poorer countries that are exploited by them', 'a colonial power and its colony'),
        ('neo-colonialism', 'continued control of poorer countries by richer ones through economic means such as trade, debt and TNCs', 'a TNC controlling a country’s main export'),
        ('core, semi-periphery and periphery', 'Wallerstein’s three zones of the capitalist world system', 'rich industrial core, middle-income semi-periphery, poor periphery'),
        ('cash crop', 'a crop grown for export rather than for local consumption', 'cocoa or coffee grown for world markets'),
        ('unequal exchange', 'trade in which poorer countries export low-value primary goods and import high-value manufactured goods', 'exporting coffee beans and importing machinery'),
    ],
    'thinkers': [
        ('Frank', 'the development of rich countries has caused the underdevelopment of poor countries', 'Dependency theory',
         'Frank argued that the metropolis exploited satellites through colonialism and continues to do so through trade, aid and TNCs; satellites develop most when links with the metropolis are weakest.',
         'The rise of East Asian economies such as South Korea challenges the idea that dependency prevents development.'),
        ('Wallerstein', 'the world is a single capitalist world system divided into core, semi-periphery and periphery', 'World-systems theory',
         'Wallerstein argued countries can move between zones, explaining both continued inequality and the rise of some economies.',
         'Critics argue it gives too little weight to internal factors such as governance and culture.'),
        ('Baran', 'the surplus produced in poorer countries is taken by foreign capital and local elites rather than invested locally', 'Dependency theory',
         'Baran argued that economic surplus flows out of poorer countries or is consumed by elites, blocking development.',
         'Some countries have retained more surplus through state-led development.'),
    ],
    'explain': [
        ('Explain how dependency theorists explain underdevelopment.', 'Colonialism extracted resources and labour and reshaped economies around cash crops; after independence, neo-colonialism continues through unequal trade, debt, aid conditions and TNCs; surplus flows to the core (Frank, Baran).', '1 mark each developed point up to 3. [3]'),
        ('Explain one way in which world-systems theory differs from dependency theory.', 'World-systems theory includes a semi-periphery and allows countries to move between zones, explaining the rise of some economies; dependency theory sees a simpler split and argues dependency blocks development.', '1 mark each theory; 1 mark contrast. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which dependency theorists argue richer countries continue to exploit poorer countries', ['unequal terms of trade', 'debt repayments', 'aid with conditions attached', 'profits taken out by TNCs', 'brain drain of skilled workers']),
    ],
    'claims': [
        ('Dependency theory sees traditional values as the main cause of underdevelopment.', False, 'That is modernisation theory; dependency theory blames exploitation by richer countries.'),
        ('Wallerstein identified a semi-periphery.', True, 'The semi-periphery lies between the core and periphery and allows for movement between zones.'),
    ],
    'ar': ([('Dependency theorists criticise reliance on cash crops.', 'exporting primary products leaves countries vulnerable to falling world prices.'),
            ('World-systems theory can explain the rise of some economies.', 'countries can move from the periphery to the semi-periphery or core.')],
           ['Frank argued that close links with the metropolis promote development.', 'Wallerstein argued that the world is made up of separate, unconnected national economies.']),
    'scen': ['A former colony near {city} still earns 70% of its export income from coffee, whose world price has fallen by a third in five years.',
             'A country that was poor in 1960 now produces cars and electronics and has incomes close to those of Western Europe.'],
    'views': VD,
    'ctx': [('the effects of cash-crop farming on rural families', {'meaning', 'change'}),
            ('trade between rich and poor countries', {'large', 'change'})],
    'data': [dict(what='commodity dependence', pop='countries', rows=['Country A (coffee)', 'Country B (copper)', 'Country C (cocoa)'], cols=('2000', '2020'), nocount=True, n=[3],
                  base=[(55, 70), (60, 75), (45, 60)], delta=[(-10, 5), (-5, 10), (-8, 6)], label='main export as a percentage of total export earnings',
                  leads=['International trade data for three commodity-exporting countries are shown below.', 'The table shows how far three countries depend on a single export, from official trade statistics.'],
                  expl=['colonial economies were organised around cash crops and raw materials (Frank)', 'unequal exchange keeps poorer countries exporting low-value goods', 'lack of investment in manufacturing'],
                  method='official statistics', claim='poorer countries remain dependent on richer countries',
                  counter='Some countries have diversified; internal factors such as governance matter; dependence may reflect comparative advantage, as neoliberals argue.')],
    'essays': [('Explain two ways in which colonialism contributed to underdevelopment, according to dependency theorists.', 'Extraction of resources and wealth; cash-crop economies; destruction of local industries; slavery and forced labour; borders and political structures; education creating dependent elites.',
                'dependency theory explains global inequality better than modernisation theory',
                'Colonial history and continued exploitation; unequal trade, debt and TNCs; persistence of inequality despite aid (Frank, Wallerstein).',
                'Rise of East Asian “tigers” and China; internal factors such as corruption and governance; modernisation and neoliberal successes; dependency underestimates agency; world-systems theory allows mobility.')],
})

g9d = T('Neoliberal and post-development approaches')
build(g9d, {
    'terms': [
        ('neoliberalism', 'the view that development comes from free markets, free trade, privatisation and a limited role for the state', 'removing tariffs and selling state-owned companies'),
        ('structural adjustment programmes', 'conditions imposed by the IMF and World Bank on loans, such as cutting public spending and opening markets', 'a country cutting food subsidies to receive a loan'),
        ('Washington Consensus', 'the set of neoliberal policies promoted by the IMF, World Bank and US Treasury from the 1980s', 'privatisation, deregulation and trade liberalisation'),
        ('post-development theory', 'the view that the idea of development itself is a Western project that should be replaced by locally defined alternatives', 'communities rejecting large dams in favour of local projects'),
        ('grassroots development', 'development projects led by local communities rather than governments or foreign agencies', 'a women’s cooperative running a village water project'),
        ('privatisation', 'the transfer of state-owned assets and services to private ownership', 'selling a state water company'),
    ],
    'thinkers': [
        ('Sachs (Jeffrey)', 'well-targeted aid and investment can help the poorest countries escape a poverty trap', 'Modernisation theory',
         'Jeffrey Sachs argued that aid for health, education and infrastructure can enable the poorest countries to start growing.',
         'Critics argue his Millennium Villages project had mixed results.'),
        ('Escobar', 'development discourse has made the Global South appear backward and in need of Western intervention', 'Post-development theory',
         'Escobar argued that development was invented by the West after 1945 and that local cultures and knowledge should be valued.',
         'Critics say post-development offers few practical alternatives.'),
        ('Stiglitz', 'IMF structural adjustment policies often harmed the countries they were meant to help', 'Transformationalism',
         'Stiglitz, a former World Bank chief economist, argued rapid liberalisation and cuts increased poverty and instability.',
         'Neoliberals argue reforms were needed and failures reflected poor implementation.'),
    ],
    'explain': [
        ('Explain two features of the neoliberal approach to development.', 'Free markets and trade; privatisation; reduced state spending and deregulation; foreign investment; structural adjustment conditions on loans; aid seen as distorting markets.', '2 marks for each explained feature. [4]'),
        ('Explain the post-development critique of development.', 'Development is a Western idea imposed on others; it defines poorer societies as deficient; projects often harm communities and environments; local knowledge and grassroots alternatives should be valued (Escobar).', '1 mark each developed point up to 3. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of structural adjustment programmes', ['cuts to health and education harmed the poor', 'removing food subsidies raised prices', 'privatisation sold assets cheaply to foreign companies', 'opening markets exposed local industries to competition', 'debt often increased']),
    ],
    'claims': [
        ('Neoliberals argue the state should take a leading role in development.', False, 'Neoliberals favour free markets and a minimal state.'),
        ('Post-development theorists value local knowledge and grassroots alternatives.', True, 'They reject Western-defined development.'),
    ],
    'ar': ([('Structural adjustment has been widely criticised.', 'cuts to public spending often harmed the poorest groups.'),
            ('Post-development theorists criticise large-scale projects.', 'such projects often ignore local needs and damage communities.')],
           ['neoliberals argue that trade barriers promote development.', 'Escobar argued that Western development discourse empowered local cultures.']),
    'scen': ['To receive a loan, the government near {city} agrees to privatise its water company and cut food subsidies; water prices rise and protests follow.',
             'A community near {city} rejects a large dam funded by international lenders and instead builds small irrigation schemes managed by local farmers.'],
    'views': VD,
    'ctx': [('the effects of privatisation of water services', {'meaning', 'change', 'large'}),
            ('grassroots development projects led by women', {'meaning', 'behaviour'})],
    'essays': [('Explain two criticisms of the neoliberal approach to development.', 'Structural adjustment increased poverty; inequality rose; privatisation benefited foreign companies; vulnerable to market shocks; undermined public services (Stiglitz).',
                'neoliberal policies are the best route to development',
                'Free trade and investment helped growth in some countries; markets allocate resources efficiently; China and India grew after opening economies.',
                'Stiglitz and others: SAPs harmed the poor; dependency theorists: neoliberalism benefits the core; East Asian success involved strong states; post-development critique.')],
})

CHAPTERS[9] = [g9a, g9b, g9c, g9d]


# ---------------------------------------------------------------- chapter 10: global economy and inequality

def g10b_aid(r, D):
    for _ in range(40):
        ga = r.choice([300, 450, 600, 800, 1200, 1500, 2000, 2500])
        gb = r.choice([250, 400, 500, 700, 900, 1800, 3000])
        pa = r.choice([0.15, 0.2, 0.25, 0.3, 0.35, 0.5, 0.7, 0.9, 1.0])
        pb = r.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.1])
        aa, ab = round(ga * pa / 100, 3), round(gb * pb / 100, 3)
        if ga != gb and pa != pb and aa != ab and round(aa, 2) == aa and round(ab, 2) == ab:
            break
    da, db = r.choice([('Donor A', 'Donor B'), ('Country A', 'Country B'), ('Country X', 'Country Y')])
    intro = (f'{da} has a gross national income (GNI) of ${ga:,} billion and gives ${_pc(aa, 2)} billion in official development assistance (aid). '
             f'{db} has a GNI of ${gb:,} billion and gives ${_pc(ab, 2)} billion in aid. The United Nations target is for rich countries to give 0.7% of GNI in aid.')
    pa_s, pb_s = _pc(aa / ga * 100, 2), _pc(ab / gb * 100, 2)
    if D <= 1:
        ds = []
        for x in [pa * 10, pa / 10, round(aa / gb * 100, 3), pb, pa + 0.5, pa * 2]:
            v = f'{_pc(x, 3)}%'
            if v != f'{pa_s}%' and v not in ds:
                ds.append(v)
        opts, a = mcq(r, f'{pa_s}%', ds[:3])
        return {'stem': f'{intro} What percentage of its GNI does {da} give in aid?', 'options': opts, 'answer': a,
                'key': f'{_pc(aa, 2)} ÷ {ga:,} × 100 = {pa_s}%. [1]', 'marks': 1}
    meet = [x for x, p in ((da, pa), (db, pb)) if p >= 0.7]
    mtxt = ' and '.join(meet) + (' meets' if len(meet) == 1 else ' meet') + ' the target' if meet else 'Neither country meets the target'
    gap = [(x, g, p) for x, g, p in ((da, ga, pa), (db, gb, pb)) if p < 0.7]
    parts = [(f'Calculate the aid given by each country as a percentage of its GNI.', f'{da}: {_pc(aa, 2)} ÷ {ga:,} × 100 = {pa_s}%; {db}: {_pc(ab, 2)} ÷ {gb:,} × 100 = {pb_s}%.', '1 mark each correct percentage. [2]'),
             (f'State which country, if either, meets the UN target of 0.7% of GNI.', f'{mtxt}.', '1 mark. [1]')]
    if gap:
        x, g, p = gap[0]
        need, have = round(g * 0.007, 3), round(g * p / 100, 3)
        parts.append((f'Calculate how much more aid, in billions of dollars, {x} would need to give to reach the 0.7% target.',
                       f'0.7% of {g:,} = {_pc(need, 2)}; {_pc(need, 2)} − {_pc(have, 2)} = ${_pc(need - have, 2)} billion.', '1 mark for 0.7% of GNI; 1 mark for the difference. [2]'))
    parts += [('Explain one reason why dependency theorists are critical of aid.', 'Aid is often tied to buying goods from the donor, comes with conditions (structural adjustment) or loans creating debt, and serves donor political interests, keeping recipients dependent (Hayter).', '1 mark identifying; 1 mark explaining. [2]'),
              ('Explain one argument modernisation theorists use to support aid.', 'Aid provides capital, technology and expertise to fill the investment gap and help countries reach take-off (Rostow).', '1 mark identifying; 1 mark explaining. [2]'),
              ('Explain one reason why the amount of aid given may not show how far it helps the poor.', 'Aid may be lost to corruption or spent on elite projects; tied aid returns to donor firms; debt repayments may exceed aid; it may not reach the poorest.', '1 mark identifying; 1 mark explaining. [2]')]
    if D == 2:
        sel = parts[:2]
    elif D == 3:
        sel = parts[:3]
    elif D == 4:
        sel = parts[:3] + [r.choice(parts[3:])]
    else:
        sel = parts[:3] + r.sample(parts[3:], 2)
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


g10a = T('Transnational corporations and global economic power')
build(g10a, {
    'terms': [
        ('transnational corporation (TNC)', 'a company that owns or controls production in more than one country and organises its activities on a global scale', 'a clothing brand with suppliers in twenty countries'),
        ('global commodity chain', 'the network of labour and production processes that brings a product from raw materials to the consumer', 'cocoa grown in West Africa becoming chocolate sold in Europe'),
        ('export processing zone (EPZ)', 'an area in a developing country where TNCs are offered tax breaks and relaxed regulation to set up factories for export', 'garment factories in a free-trade zone'),
        ('outsourcing', 'contracting out part of the production process to other companies, often in lower-wage countries', 'a phone company using a separate supplier to assemble handsets'),
        ('race to the bottom', 'competition between countries to attract TNCs by lowering wages, taxes and regulations', 'governments weakening labour laws to keep factories'),
        ('transfer pricing', 'the pricing of goods traded between branches of the same TNC, which can be used to shift profits to low-tax countries', 'recording profits in a tax haven'),
    ],
    'thinkers': [
        ('Sklair', 'a transnational capitalist class of TNC executives, officials and professionals promotes global capitalism and consumerism', 'Marxism',
         'Sklair argued TNCs drive the culture-ideology of consumerism and are the main agents of global capitalism.',
         'Others argue states still regulate TNCs and that TNCs bring jobs and technology.'),
        ('Klein', 'global brands rely on low-paid workers in poor countries while spending heavily on marketing', 'Neo-Marxism',
         'Klein’s “No Logo” showed brands outsourcing production to sweatshops in export processing zones.',
         'Some studies find TNC jobs pay more than local alternatives.'),
        ('Bakan', 'the corporation is legally required to put shareholders’ profits first, whatever the social cost', 'Marxism',
         'Bakan argued corporations behave like “psychopaths”, ignoring harm to workers and the environment.',
         'Corporate social responsibility and regulation can limit harm.'),
    ],
    'explain': [
        ('Explain two ways in which TNCs may benefit developing countries.', 'Create jobs and pay wages higher than local alternatives; bring investment, technology and skills; build infrastructure; pay taxes; connect local suppliers to global markets.', '2 marks for each explained way. [4]'),
        ('Explain two ways in which TNCs may harm developing countries.', 'Low wages and poor conditions in sweatshops; profits repatriated to the home country; tax avoidance; environmental damage; power to influence governments; footloose firms leave when costs rise.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why TNCs locate production in developing countries', ['lower labour costs', 'tax incentives in export processing zones', 'weaker regulation of labour and the environment', 'access to raw materials', 'access to growing consumer markets']),
    ],
    'claims': [
        ('All profits made by TNCs in developing countries stay in those countries.', False, 'Much of the profit is repatriated to the TNC’s home country or shifted to tax havens.'),
        ('Some TNCs have revenues larger than the GDP of many countries.', True, 'This gives them significant economic and political power.'),
    ],
    'ar': ([('Governments compete to attract TNCs.', 'TNCs can move production to wherever costs are lowest.'),
            ('Marxists are critical of TNCs.', 'they argue TNCs exploit cheap labour in poorer countries to maximise profit.')],
           ['TNCs are banned from operating in export processing zones.', 'Sklair argued that TNCs have no influence on consumer culture.']),
    'scen': ['A global sportswear brand closes its factory in {city} and moves production to a country where wages are half as high, after the local government raised the minimum wage.',
             'A mining company owned by shareholders abroad extracts copper near {city}; the government receives low royalties, and local rivers become polluted.',
             'An electronics TNC opens an assembly plant in an export processing zone near {city}, employing 8,000 young women on short contracts.'],
    'views': {'Marxism': 'TNCs exploit cheap labour and resources in poorer countries; profits flow to owners in the core, and governments compete in a race to the bottom (Sklair, Klein).',
              'Neoliberalism': 'TNCs bring investment, jobs, technology and access to global markets; governments should remove barriers so that growth trickles down.',
              'Dependency theory': 'TNCs keep poorer countries dependent on foreign capital and low-value production, draining surplus to the core (Frank).',
              'Modernisation theory': 'TNC investment provides the capital and modern technology needed for take-off and spreads modern work values (Rostow).',
              'Transformationalism': 'TNCs are powerful global actors, but states can still bargain with and regulate them; effects vary between countries.'},
    'ctx': [('working conditions in factories supplying global brands', {'meaning', 'behaviour', 'hidden', 'sensitive'}),
            ('the size and growth of TNC investment in different countries', {'large', 'change'})],
    'data': [dict(what='foreign direct investment', pop='countries', rows=['Country A', 'Country B', 'Country C'], cols=('2005', '2020'), unit='', uname='billion dollars', nocount=True, n=[3],
                  base=[(5, 15), (20, 40), (2, 8)], delta=[(10, 30), (3, 15), (2, 6)], label='inflows of foreign direct investment by TNCs (billion dollars)',
                  leads=['The table shows official data on investment by TNCs in three developing countries.', 'Official statistics show foreign direct investment (FDI) by TNCs in three countries.'],
                  expl=['governments created export processing zones and tax incentives', 'TNCs moved production to lower-cost locations', 'some countries became less attractive as wages rose or instability grew'],
                  method='official statistics', claim='TNC investment brings development to poorer countries',
                  counter='Investment figures do not show who benefits; profits may be repatriated; jobs may be low-paid; investment may leave quickly.')],
    'essays': [('Explain two reasons why TNCs are powerful in the global economy.', 'Size of revenues; mobility (footloose); control of global commodity chains; lobbying governments; control of technology and brands; transfer pricing and tax avoidance.',
                'TNCs are more powerful than nation-states in the global economy',
                'Hyperglobalists and Marxists: TNCs’ size and mobility; race to the bottom; tax avoidance; Sklair’s transnational capitalist class.',
                'Sceptics: states regulate, tax and nationalise; TNCs depend on states for legal systems and infrastructure; China’s state control; transformationalists: power is shared.')],
})

g10b = T('Global inequality: poverty, debt and aid')
build(g10b, {
    'terms': [
        ('absolute poverty', 'lacking the minimum resources needed for physical survival, such as food, water and shelter', 'living on less than about $2 a day'),
        ('relative poverty', 'lacking the resources needed for the normal standard of living of the society one lives in', 'not being able to afford a phone or internet where most people have them'),
        ('official development assistance (aid)', 'grants and cheap loans from governments of richer countries to poorer countries', 'a donor government funding a vaccination programme'),
        ('tied aid', 'aid given on condition that the recipient buys goods or services from the donor country', 'a loan that must be spent on the donor’s engineering firms'),
        ('debt crisis', 'a situation in which poorer countries cannot repay loans and spend large shares of income on interest', 'a government spending more on debt repayments than on health'),
        ('structural adjustment programme', 'conditions attached to IMF and World Bank loans requiring cuts in public spending, privatisation and free trade', 'a country cutting food subsidies to receive a loan'),
    ],
    'thinkers': [
        ('Sachs', 'extreme poverty can be ended through large increases in well-targeted aid', 'Modernisation theory',
         'Sachs argued poor countries are stuck in a “poverty trap” and need a “big push” of aid for health, education and infrastructure.',
         'Easterly argues aid often fails because it is planned from above.'),
        ('Hayter', 'aid is a form of imperialism that benefits donors and keeps recipients dependent', 'Dependency theory',
         'Hayter argued aid and loans with conditions serve the interests of donor countries and their companies.',
         'Some aid, such as vaccination programmes, has clearly reduced death rates.'),
        ('Collier', 'the “bottom billion” are trapped by conflict, natural resources, bad governance and being landlocked', 'Neoliberalism',
         'Collier argued aid should be targeted and combined with trade and security reforms.',
         'Critics argue he underplays the role of global inequality and rich countries.'),
    ],
    'explain': [
        ('Explain the difference between absolute and relative poverty, using an example of each.', 'Absolute: lack of minimum needed for survival (e.g. insufficient food); relative: lacking what is normal in one’s society (e.g. cannot afford school trips).', '1 mark each definition; 1 mark each example. [4]'),
        ('Explain two ways in which debt may increase global inequality.', 'Interest payments transfer wealth from poor to rich countries; debt repayment reduces spending on health and education; loan conditions force cuts and privatisation; countries must export cash crops rather than food.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'made of international aid', ['tied aid benefits donor companies', 'loans create debt', 'aid can be lost to corruption', 'aid serves donors’ political interests', 'aid may create dependency', 'large projects may harm local people']),
    ],
    'claims': [
        ('Tied aid must be spent on goods from the recipient country.', False, 'Tied aid must be spent on goods or services from the donor country.'),
        ('Debt repayments can reduce spending on health and education in poorer countries.', True, 'Money spent on interest cannot be spent on public services.'),
    ],
    'ar': ([('Dependency theorists are critical of loans to poorer countries.', 'debt repayments transfer wealth from the periphery to the core.'),
            ('Structural adjustment programmes were controversial.', 'they required cuts to public spending that often hurt the poorest.')],
           ['tied aid must be spent in the recipient country.', 'absolute poverty is measured against the average living standard of a society.']),
    'scen': ['A country near {city} spends twice as much on repaying foreign loans as on health care, after borrowing heavily in the 1980s.',
             'A donor government gives a large grant to build a dam near {city}, on condition that the work is done by companies from the donor country.',
             'An international charity funds clean-water pumps in villages around {city}, run and repaired by local committees.'],
    'views': {'Modernisation theory': 'aid fills the investment gap and provides technology and expertise so that poorer countries can reach take-off (Rostow, Sachs).',
              'Dependency theory': 'aid and debt keep poorer countries dependent; tied aid and loan conditions serve donor interests and transfer wealth to the core (Hayter, Frank).',
              'Neoliberalism': 'aid distorts markets and supports inefficient governments; growth comes from free trade, private investment and reducing state spending.',
              'Post-development theory': 'aid imposes Western ideas of development; local communities should decide their own goals using local knowledge (Escobar).'},
    'ctx': [('the experiences of villagers affected by an aid project', {'meaning', 'behaviour', 'hidden'}),
            ('changes in levels of global poverty', {'large', 'change'})],
    'data': [dict(what='extreme poverty', pop='people', rows=['Sub-Saharan Africa', 'South Asia', 'East Asia and Pacific'], cols=('1990', '2019'), nocount=True, n=[3],
                  base=[(50, 58), (45, 52), (55, 62)], delta=[(-20, -10), (-40, -30), (-60, -53)], label='percentage of the population living in extreme poverty',
                  leads=['International estimates of extreme poverty in three world regions are shown below.', 'The table shows World Bank estimates of the share of people in extreme poverty.'],
                  expl=['rapid industrial growth in East Asia (especially China) lifted many out of poverty', 'debt, conflict and dependence on primary exports slowed progress in parts of Africa', 'aid and investment in health and education contributed'],
                  method='official statistics', claim='global poverty is being successfully reduced',
                  counter='Population growth means numbers in poverty may fall less than percentages; the poverty line is very low; relative inequality between rich and poor countries has grown.')],
    'essays': [('Explain two arguments for and against aid.', 'For: funds health, education and infrastructure; emergency relief; fills investment gap (Sachs). Against: tied aid; debt; corruption; dependency (Hayter); undermines local markets (Moyo).',
                'aid does more harm than good to developing countries',
                'Dependency and neoliberal critics: tied aid, debt, conditions, corruption, dependency, undermining local producers (Hayter, Moyo, Easterly).',
                'Aid has reduced child mortality and disease (Sachs); targeted and multilateral aid can work; NGOs and participatory projects; the problem is design not aid itself.')],
})
_reg(g10b, 'C3', (1, 2, 3, 4, 5), 'numerical', g10b_aid, 'aid_gni')

g10c = T('International organisations: the IMF, World Bank and WTO')
build(g10c, {
    'terms': [
        ('International Monetary Fund (IMF)', 'an international organisation that lends to countries with balance-of-payments problems and promotes financial stability', 'emergency loans to a country in a currency crisis'),
        ('World Bank', 'an international organisation that lends to developing countries for development projects and reforms', 'loans for roads, dams and education programmes'),
        ('World Trade Organization (WTO)', 'an international organisation that sets and enforces rules for trade between member countries', 'ruling on a dispute about import tariffs'),
        ('Washington Consensus', 'the set of neoliberal policies (privatisation, deregulation, free trade, spending cuts) promoted by the IMF and World Bank', 'conditions requiring privatisation of water supply'),
        ('conditionality', 'the requirement that a borrower adopts certain policies in return for a loan', 'cutting subsidies as a loan condition'),
        ('trade liberalisation', 'the removal of tariffs, quotas and other barriers to trade', 'reducing import taxes on foreign rice'),
    ],
    'thinkers': [
        ('Stiglitz', 'the IMF imposed one-size-fits-all neoliberal policies that often worsened crises in developing countries', 'Transformationalism',
         'Stiglitz, a former World Bank chief economist, argued capital-market liberalisation and austerity deepened the Asian financial crisis.',
         'Supporters argue reforms were needed to restore stability.'),
        ('Harvey', 'neoliberal institutions spread policies that restore the power of capital', 'Marxism',
         'Harvey argued that structural adjustment opened economies to TNCs and transferred public assets to private owners (accumulation by dispossession).',
         'Neoliberals argue reforms ended inefficiency and encouraged growth.'),
        ('Sachs', 'well-designed international action and aid can help end extreme poverty', 'Modernisation theory',
         'Sachs criticised harsh IMF austerity but supported international organisations funding health and infrastructure.',
         'Easterly argues top-down plans by international bodies often fail.'),
    ],
    'explain': [
        ('Explain the difference between the roles of the IMF and the WTO.', 'IMF: lends to countries facing financial crises and promotes financial stability, often with conditions; WTO: makes and enforces rules for international trade and settles trade disputes.', '1 mark each role; 1 mark contrast. [3]'),
        ('Explain two criticisms of structural adjustment programmes.', 'Spending cuts reduced health and education; removing subsidies raised food prices; privatisation benefited TNCs; free trade hurt local producers; debt continued to grow.', '2 marks for each explained criticism. [4]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'made of the World Trade Organization', ['rich countries keep farm subsidies while poor countries must open markets', 'rules on intellectual property raise medicine prices', 'powerful countries dominate negotiations', 'free trade can harm local farmers and industries']),
    ],
    'claims': [
        ('Voting power in the IMF is equal for all member countries.', False, 'Votes are weighted by financial contribution, giving rich countries most power.'),
        ('The WTO settles disputes between countries about trade.', True, 'It has a dispute settlement process.'),
    ],
    'ar': ([('Critics argue the IMF is dominated by rich countries.', 'voting power depends on the size of each country’s financial contribution.'),
            ('Structural adjustment often led to cuts in public services.', 'loan conditions required governments to reduce public spending.')],
           ['the WTO lends money to countries in financial crisis.', 'the Washington Consensus promoted nationalisation of industries.']),
    'scen': ['After a currency crisis, the government near {city} accepts an IMF loan on condition that it cuts fuel subsidies and sells the state electricity company.',
             'Farmers near {city} lose their incomes after the country removes import tariffs under a trade agreement, and cheap subsidised grain floods in from abroad.'],
    'views': {'Neoliberalism': 'the IMF, World Bank and WTO promote free markets, privatisation and fiscal discipline, which create the conditions for growth.',
              'Dependency theory': 'these organisations are dominated by core countries and impose policies that keep the periphery dependent and open to exploitation.',
              'Marxism': 'they serve global capital, opening markets to TNCs and transferring public assets to private owners (Harvey).',
              'Transformationalism': 'they are part of an emerging system of global governance that reshapes, but does not remove, state power; reform is possible (Held, Stiglitz).'},
    'ctx': [('the effects of loan conditions on public services', {'large', 'change'}),
            ('how farmers experience trade liberalisation', {'meaning', 'behaviour'})],
    'data': [dict(what='public spending under structural adjustment', pop='countries', rows=['Health', 'Education', 'Debt repayment'], cols=('Before the programme', 'After the programme'), nocount=True, n=[3],
                  base=[(8, 12), (14, 18), (15, 22)], delta=[(-4, -1), (-5, -1), (4, 10)], label='share of government spending (%)', share=True,
                  leads=['The table shows the share of government spending in a country before and after an IMF programme.', 'Official government figures for a country near {city} are shown below.'],
                  expl=['loan conditions required cuts to public spending', 'a growing share of the budget went to repaying loans', 'governments prioritised debt repayment to keep access to credit'],
                  method='official statistics', claim='structural adjustment harmed public services',
                  counter='Spending shares do not show total spending or efficiency; other factors such as recession may matter; some reforms may have reduced waste.')],
    'essays': [('Explain two roles of international organisations in the global economy.', 'IMF: crisis lending and conditionality; World Bank: development loans; WTO: trade rules and disputes; promotion of neoliberal policies; global governance.',
                'international organisations such as the IMF and WTO mainly serve the interests of rich countries',
                'Weighted votes; Washington Consensus; structural adjustment harmed the poor; WTO rules on farm subsidies and patents favour rich countries (Stiglitz, Harvey).',
                'Neoliberal view: stability and growth; emergency lending prevents collapse; WTO gives small countries a legal forum; reforms such as debt relief (HIPC); emerging powers now more influential.')],
})

CHAPTERS[10] = [g10a, g10b, g10c]


# ---------------------------------------------------------------- chapter 11: global culture, identity and migration

g11a = T('Global culture, cultural imperialism and McDonaldisation')
build(g11a, {
    'terms': [
        ('global culture', 'shared products, values, media and lifestyles found in many societies across the world', 'the same superhero films showing worldwide'),
        ('cultural imperialism', 'the domination of other cultures by the values and products of powerful (mainly Western) societies', 'local music displaced by Western pop on radio'),
        ('McDonaldisation', 'Ritzer’s term for the spread of the fast-food principles of efficiency, calculability, predictability and control', 'universities and hospitals adopting standardised procedures'),
        ('homogenisation', 'the process by which cultures become more similar', 'the same shopping malls and brands in every city'),
        ('Americanisation', 'the spread of American products, values and culture around the world', 'American fast food, films and slang in many countries'),
        ('culture-ideology of consumerism', 'Sklair’s term for the values encouraging people to define themselves through buying goods', 'advertising linking happiness to new products'),
    ],
    'thinkers': [
        ('Ritzer', 'McDonaldisation spreads efficiency, calculability, predictability and control across societies', 'Neo-Marxism',
         'Ritzer argued rationalisation creates an “iron cage” of standardised, dehumanising experiences.',
         'Glocalisation shows global brands adapting to local cultures.'),
        ('Schiller', 'Western media corporations impose their values on other cultures', 'Marxism',
         'Schiller argued American media conglomerates spread consumerist, capitalist values worldwide.',
         'Audiences interpret media actively, and non-Western media (Bollywood, K-pop) also spread globally.'),
        ('Sklair', 'TNCs spread a culture-ideology of consumerism', 'Marxism',
         'Sklair argued the transnational capitalist class promotes consumption as the meaning of life.',
         'Postmodernists argue consumers actively use goods to build identities.'),
    ],
    'explain': [
        ('Explain two features of McDonaldisation, using examples.', 'Efficiency (fast routines, e.g. drive-through); calculability (quantity over quality, e.g. portion size, exam scores); predictability (same product everywhere); control (machines and scripts replace human judgement).', '2 marks for each explained feature with example. [4]'),
        ('Explain two criticisms of the cultural imperialism thesis.', 'Audiences actively interpret media; cultural flows are multi-directional (Bollywood, K-pop, telenovelas); hybridity and glocalisation; local cultures resist and revive; it treats non-Western cultures as passive.', '2 marks for each explained criticism. [4]'),
    ],
    'why': [
        ('feature', 'features', 'of McDonaldisation identified by Ritzer', ['efficiency', 'calculability', 'predictability', 'control through non-human technology']),
    ],
    'claims': [
        ('Ritzer argued McDonaldisation increases variety and unpredictability.', False, 'He argued it increases predictability and standardisation.'),
        ('Cultural imperialism suggests powerful societies dominate other cultures.', True, 'It mainly refers to Western, especially American, influence.'),
    ],
    'ar': ([('Critics say the cultural imperialism thesis underestimates audiences.', 'people interpret and adapt global media in the light of local culture.'),
            ('Ritzer is critical of McDonaldisation.', 'he argues rationalisation can become dehumanising and irrational.')],
           ['Ritzer argued McDonaldisation applies only to restaurants.', 'cultural imperialism refers to poorer countries dominating Western culture.']),
    'scen': ['In {city}, the main shopping street now has the same coffee chains, fast-food outlets and clothing brands as cities across the world, and local cafés have closed.',
             'A hospital in {city} introduces strict time targets for each consultation and a scripted checklist for staff to follow with every patient.',
             'A survey in {city} finds that most of the top 20 films last year were made in Hollywood, but the most-streamed music was by local artists.'],
    'views': {'Marxism': 'global culture is driven by TNCs spreading consumerism and capitalist values for profit; local cultures are swamped (Sklair, Schiller).',
              'Neo-Marxism': 'rationalised, standardised culture spreads the logic of capitalism into everyday life, creating an iron cage (Ritzer).',
              'Postmodernism': 'global culture offers more choice; people mix global and local elements to create their own identities (hybridity).',
              'Transformationalism': 'cultures are changed by globalisation but not simply replaced; global products are adapted and resisted locally (glocalisation).'},
    'ctx': [('how young people in {city} view global brands', {'meaning', 'large', 'young'}),
            ('the amount of foreign content on national television', {'media', 'large', 'change'})],
    'methods': ['questionnaire', 'structured interview', 'unstructured interview', 'semi-structured interview', 'content analysis', 'case study', 'participant observation'],
    'data': [dict(what='the origin of television content', pop='channels', rows=['Domestic programmes', 'US programmes', 'Other foreign programmes'], cols=('2000', '2020'), dist=True, nocount=True, n=[3],
                  base=[(40, 50), (30, 40), (10, 20)], delta=[(5, 15), (-15, -5), (0, 5)], label='share of prime-time hours on national television (%)',
                  leads=['A content analysis of prime-time television in a country produced the results below.', 'The table shows a content analysis of prime-time schedules in a country near {city}.'],
                  expl=['local producers have grown and audiences prefer local programmes', 'quotas for domestic content', 'more content comes from non-US countries'],
                  method='content analysis', claim='cultural imperialism is declining',
                  counter='Streaming platforms may not be included; local programmes may copy US formats; ownership of channels may still be foreign.')],
    'essays': [('Explain two ways in which global culture may affect local cultures.', 'Homogenisation and Americanisation; McDonaldisation; consumerism; hybridity and glocalisation; revival of local identities as resistance.',
                'globalisation is creating a single, homogenised global culture',
                'Cultural imperialism (Schiller); McDonaldisation (Ritzer); consumerism (Sklair); dominance of US media and brands.',
                'Glocalisation and hybridity; reverse flows (Bollywood, K-pop); active audiences; resurgence of local and national identities; postmodern choice.')],
})

g11b = T('Hybrid identities and glocalisation')
build(g11b, {
    'terms': [
        ('hybridity', 'the mixing of different cultures to create new cultural forms and identities', 'Bhangra music mixing Punjabi folk and Western pop'),
        ('glocalisation', 'the adaptation of global products and ideas to fit local cultures', 'fast-food chains selling vegetarian menus in India'),
        ('cultural defence', 'the strengthening of a group’s culture in response to perceived threats from outside', 'a revival of traditional dress among a minority'),
        ('global identity', 'a sense of belonging to the world as a whole rather than one nation', 'young people describing themselves as “global citizens”'),
        ('hyphenated identity', 'an identity combining two cultural or national belongings', 'British-Pakistani or Chinese-Canadian'),
    ],
    'thinkers': [
        ('Robertson', 'globalisation and localisation happen together in the process of glocalisation', 'Transformationalism',
         'Robertson argued global products and ideas are always adapted to local cultures.',
         'Critics argue glocalisation can be a marketing strategy that still spreads global brands.'),
        ('Hall', 'identities are increasingly hybrid, fluid and formed through cultural mixing', 'Postmodernism',
         'Hall argued new “cultures of hybridity” are formed by migrants and their children.',
         'Others argue many people still hold fixed national or religious identities.'),
        ('Pieterse', 'globalisation is a process of hybridisation, not homogenisation', 'Postmodernism',
         'Pieterse described global culture as a “global mélange” of mixing cultures.',
         'Marxists argue power is unequal, so mixing is dominated by Western culture.'),
    ],
    'explain': [
        ('Explain what is meant by glocalisation, using an example.', 'The adaptation of global products, brands or ideas to local tastes and cultures, e.g. a global restaurant chain changing its menu for local religious rules.', '1 mark meaning; 1 mark development; 1 mark example. [3]'),
        ('Explain two ways in which globalisation may create hybrid identities.', 'Migration brings cultures together and second generations mix them; global media let people choose from many cultures; consumption of global goods combined with local traditions; online communities across borders.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('example', 'examples', 'of hybrid culture', ['fusion food', 'music mixing global and local styles', 'films combining Bollywood and Hollywood styles', 'mixed-language slang among young people', 'festivals celebrated across communities']),
    ],
    'claims': [
        ('Glocalisation means local cultures disappear completely.', False, 'Glocalisation means global products are adapted to local cultures.'),
        ('Second-generation migrants may develop hybrid identities.', True, 'They often combine elements of their parents’ culture with the culture of the society they grow up in.'),
    ],
    'ar': ([('Global brands often change their products for different markets.', 'glocalisation increases sales by fitting local tastes.'),
            ('Postmodernists see identity as hybrid.', 'they argue people choose and mix identities from many cultural sources.')],
           ['glocalisation means that every country adopts exactly the same products.', 'Hall argued identities are fixed at birth.']),
    'scen': ['{woman}, whose parents migrated to {city} from another continent, speaks two languages at home, follows K-pop and celebrates both her family’s festivals and local holidays.',
             'A global coffee chain in {city} offers drinks made with local spices and designs its cafés to resemble traditional tea houses.'],
    'views': {'Postmodernism': 'identities are fluid and chosen; people mix global and local influences to create hybrid identities (Hall, Pieterse).',
              'Transformationalism': 'global and local interact: global products are adapted locally, producing glocalisation rather than simple domination (Robertson).',
              'Marxism': 'glocalisation is a marketing strategy by TNCs to increase profits; hybridity still takes place on terms set by global capitalism.',
              'Interactionism': 'identity is negotiated in everyday interaction; individuals give their own meanings to cultural mixing.'},
    'ctx': [('how second-generation migrants describe their identities', {'meaning', 'young', 'sensitive'}),
            ('how global brands adapt their products in different countries', {'large', 'media'})],
    'methods': ['questionnaire', 'unstructured interview', 'semi-structured interview', 'participant observation', 'content analysis', 'case study', 'personal documents'],
    'data': [dict(what='identity among young people', pop='young people', rows=['National identity only', 'Mixed or hyphenated identity', 'Global citizen'], cols=('Parents born in the country', 'Parents born abroad'), cmp=True, dist=True, nocount=True,
                  base=[(55, 65), (20, 30), (8, 15)], delta=[(-35, -20), (20, 35), (0, 5)], label='how young people describe their identity (%)',
                  leads=['A survey of {n} young people aged 16-24 in {city} asked how they describe their identity.', '{person} surveyed {n} young people in {city} about their identities. The results are below.'],
                  expl=['children of migrants combine cultures from home and the wider society', 'global media and travel encourage global identities', 'national identity remains strong for many'],
                  method='questionnaire', claim='globalisation is producing hybrid identities',
                  counter='Most young people with parents born in the country still hold a national identity; closed questions may not capture complex identities; one city may be untypical.')],
    'essays': [('Explain two examples of glocalisation.', 'Fast-food menus adapted to local religions; global TV formats with local versions; music fusing global and local styles; global religions adapting rituals.',
                'globalisation creates hybrid identities rather than a single global culture',
                'Hall, Pieterse, Robertson: hybridity, glocalisation, diaspora cultures, reverse cultural flows.',
                'Homogenisation and cultural imperialism (Ritzer, Schiller); cultural defence and nationalism; Marxists: hybridity is commercialised; many people have little contact with global culture.')],
})

g11c = T('Migration, diaspora and transnational communities')
build(g11c, {
    'terms': [
        ('diaspora', 'a population that has spread from its original homeland but keeps a shared identity and links to it', 'communities of Indian origin across the world'),
        ('transnational community', 'a group that maintains social, economic and political ties across national borders', 'migrants sending remittances and voting in home elections'),
        ('remittances', 'money sent home by migrants to their families', 'a nurse abroad sending money monthly to parents'),
        ('push factors', 'conditions that encourage people to leave their country', 'unemployment, conflict or persecution'),
        ('pull factors', 'conditions that attract people to a new country', 'higher wages, safety or family already there'),
        ('feminisation of migration', 'the growing share of women among international migrants', 'women moving abroad as domestic and care workers'),
    ],
    'thinkers': [
        ('Castles and Miller', 'international migration has globalised, accelerated, diversified and become feminised', 'Transformationalism',
         'Castles and Miller argued we live in an “age of migration” with more complex, multi-directional flows.',
         'Sceptics point out that only a small proportion of the world’s population are international migrants.'),
        ('Cohen', 'diasporas maintain collective memory and connections to a homeland across generations', 'Postmodernism',
         'Cohen identified types of diaspora (victim, labour, trade, imperial, cultural).',
         'Some critics say the term is stretched to cover too many groups.'),
        ('Ehrenreich and Hochschild', 'women from poorer countries migrate to provide care work in richer countries, creating global care chains', 'Marxist feminism',
         'They argued care and emotional labour are transferred from poor to rich countries, leaving gaps in migrants’ own families.',
         'Migrants may gain independence and income through migration.'),
    ],
    'explain': [
        ('Explain two ways in which migrants maintain links with their country of origin.', 'Remittances; communication technology and social media; visits and return migration; voting and political involvement; religious and cultural organisations; marriage links.', '2 marks for each explained way. [4]'),
        ('Explain two effects of remittances on sending countries.', 'Raise household incomes and reduce poverty; fund education and health; bring foreign currency; create dependency and inequality between families with and without migrants; may reduce pressure for reform.', '2 marks for each explained effect. [4]'),
    ],
    'why': [
        ('push factor', 'push factors', 'leading people to migrate', ['unemployment', 'low wages', 'conflict and war', 'persecution', 'environmental disasters', 'lack of education or health care']),
    ],
    'claims': [
        ('Remittances flow from poorer countries to richer countries.', False, 'Remittances are mainly sent by migrants in richer countries back to families in poorer countries.'),
        ('A growing proportion of international migrants are women.', True, 'This is the feminisation of migration.'),
    ],
    'ar': ([('Many migrants send money home.', 'remittances support families in the country of origin.'),
            ('Diaspora communities may keep a strong sense of identity.', 'they maintain cultural, religious and family links with the homeland.')],
           ['diasporas lose all connection with their homeland after migration.', 'push factors are features of the destination country that attract migrants.']),
    'scen': ['{woman} works as a nurse in a hospital in {city}, sends half her wages to her parents abroad each month and uses video calls to help raise her children, who live with their grandmother.',
             'Members of a community originally from one country now live in {city} and five other cities; they run a shared website, fund a school in their home region and vote in its elections.'],
    'views': {'Marxism': 'migrants provide cheap, flexible labour for capitalism in richer countries, and migration drains skills from poorer countries.',
              'Marxist feminism': 'women’s migration for care work creates global care chains in which poor women’s labour is exploited to support richer families (Ehrenreich and Hochschild).',
              'Postmodernism': 'migration creates diaspora and hybrid identities; people belong to several places and choose identities (Hall, Cohen).',
              'Transformationalism': 'migration is part of a globalised, diversified pattern of movement that creates transnational communities and reshapes states (Castles and Miller).'},
    'ctx': [('the experiences of migrant care workers', {'meaning', 'sensitive', 'hidden'}),
            ('patterns of international migration over time', {'large', 'change'})],
    'data': [dict(what='remittances', pop='countries', rows=['Country A', 'Country B', 'Country C'], cols=('2010', '2022'), unit='%', nocount=True, n=[3],
                  base=[(5, 10), (15, 22), (2, 5)], delta=[(2, 6), (-3, 5), (1, 4)], label='remittances received as a percentage of GDP',
                  leads=['The table shows official data on remittances received by three countries.', 'World Bank figures on remittances received by three countries are shown below.'],
                  expl=['more people working abroad', 'digital money-transfer apps make sending money cheaper', 'economic problems at home push more people to migrate'],
                  method='official statistics', claim='migration benefits sending countries',
                  counter='Remittances do not show the social costs of separated families or the loss of skilled workers (brain drain); informal transfers are not counted.')],
    'essays': [('Explain two reasons for the growth of international migration.', 'Global inequality and push/pull factors; cheaper transport and communication; demand for labour in rich countries; conflict and climate; family reunion; diaspora networks.',
                'migration mainly benefits richer countries rather than poorer countries',
                'Brain drain; cheap labour; global care chains (Ehrenreich and Hochschild); migrants fill labour shortages; Marxist exploitation view.',
                'Remittances reduce poverty; skills and ideas return with migrants; diasporas invest in homelands; migrants gain income and independence; transformationalist view of mutual benefit.')],
})

CHAPTERS[11] = [g11a, g11b, g11c]


# ---------------------------------------------------------------- chapter 12: global crime, risk and social movements

g12a = T('Global crime: trafficking, cybercrime and green crime')
build(g12a, {
    'terms': [
        ('global crime', 'crime that crosses national borders and is organised through global networks', 'drug trafficking from producing to consuming countries'),
        ('human trafficking', 'the movement of people by force, fraud or deception for exploitation', 'people forced into labour or sex work abroad'),
        ('cybercrime', 'crime carried out using computers and the internet', 'online fraud, hacking and identity theft'),
        ('green crime', 'crime and harm against the environment and other species', 'illegal dumping of toxic waste'),
        ('global criminal economy', 'Castells’s term for the worldwide network of illegal trade worth trillions of dollars', 'arms, drugs, people and money laundering'),
        ('state crime', 'crime committed by or on behalf of governments', 'genocide or torture by state officials'),
    ],
    'thinkers': [
        ('Castells', 'a global criminal economy has emerged, linked through networks and the internet', 'Transformationalism',
         'Castells argued criminal networks use globalisation and technology to trade drugs, arms, people and money.',
         'Size estimates are uncertain because hidden crime is hard to measure.'),
        ('Glenny', 'McMafia: organised crime has globalised as markets were deregulated', 'Neoliberalism',
         'Glenny argued deregulation and the collapse of the Soviet Union created opportunities for transnational mafias.',
         'Critics argue local conditions still shape organised crime.'),
        ('Beck', 'global society produces manufactured risks such as environmental damage', 'Late modernity',
         'Beck’s risk society thesis is used by green criminologists to show how industrial harms cross borders.',
         'Marxists argue risks are unequally distributed by class and between countries.'),
        ('Taylor', 'globalisation has created criminogenic conditions by increasing inequality and insecurity', 'Marxism',
         'Taylor argued neoliberal globalisation creates greater opportunities and pressures for crime at all levels of society.',
         'Not everyone exposed to inequality turns to crime.'),
    ],
    'explain': [
        ('Explain two ways in which globalisation has created new opportunities for crime.', 'Internet allows cybercrime across borders; deregulated finance allows money laundering; cheaper transport aids trafficking; global demand for drugs; weak states in some regions.', '2 marks for each explained way. [4]'),
        ('Explain the difference between traditional and green criminology.', 'Traditional criminology studies acts that break national laws; green criminology takes a wider harm-based approach, including legal but harmful activities against the environment (White).', '1 mark each; 1 mark contrast. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why global crime is difficult to control', ['crime crosses national jurisdictions', 'differences in laws between countries', 'corruption of officials', 'criminals use encryption and the internet', 'lack of international cooperation']),
    ],
    'claims': [
        ('Green crime only includes actions that break national laws.', False, 'Green criminologists use a harm-based definition, including legal harms.'),
        ('Cybercrime can be committed against victims in other countries.', True, 'The internet allows offenders to target victims anywhere.'),
    ],
    'ar': ([('Global crime is hard to police.', 'offenders and victims are often in different countries with different laws.'),
            ('Green criminologists study legal activities.', 'they define crime by the harm caused rather than by national law.')],
           ['human trafficking always involves people who freely choose to migrate.', 'cybercrime can only be committed against people in the same country.']),
    'scen': ['Police in {city} trace a fraud ring that stole money from thousands of people online; the servers were in one country, the organisers in another and the victims in twenty more.',
             'A factory near {city} legally pours waste chemicals into a river, killing fish and harming villagers’ health downstream.',
             'Workers recruited in a village are promised jobs in {city} but have their passports taken on arrival and are forced to work without pay.'],
    'views': {'Marxism': 'global crime reflects capitalism: inequality creates pressures for crime, and the powerful (TNCs, states) commit harms that go unpunished (Taylor).',
              'Transformationalism': 'globalisation creates networks that criminals use; crime and control are reshaped across borders (Castells).',
              'Late modernity': 'global risks, including environmental harms, are manufactured by industrial society and cross borders (Beck).',
              'Functionalism': 'crime reveals weaknesses in social regulation; global crime grows where anomie and weak controls exist, and responses reaffirm shared values.'},
    'ctx': [('the experiences of victims of trafficking', {'meaning', 'sensitive', 'hidden'}),
            ('reported cybercrime in different countries', {'large', 'change'})],
    'data': [dict(what='reported cybercrime', pop='offences', rows=['Online fraud', 'Hacking', 'Identity theft'], cols=('2018', '2023'), unit='', uname='thousand offences', nocount=True, n=[3],
                  base=[(40, 60), (10, 20), (15, 25)], delta=[(20, 40), (5, 15), (-5, 10)], label='cybercrimes recorded by police in a country (thousands)',
                  leads=['Police recorded cybercrime statistics for a country near {city} are shown below.', 'The table shows cybercrimes recorded by police in one country.'],
                  expl=['more people shop and bank online', 'criminals use cheaper and more sophisticated tools', 'more victims are reporting crime'],
                  method='official statistics', claim='cybercrime is increasing rapidly',
                  counter='Most cybercrime is unreported; changes may reflect recording practices or awareness; offenders and victims may be in other countries.')],
    'essays': [('Explain two types of global crime.', 'Trafficking of drugs, arms and people; cybercrime; green crime; money laundering; state crime; terrorism.',
                'globalisation has made crime more difficult to control',
                'Castells and Glenny: global networks; cybercrime and trafficking cross borders; corruption; weak states; differences in law.',
                'International police cooperation (Interpol, Europol); surveillance technology; global agreements; much crime remains local; states still powerful.')],
})

g12b = T('Risk society and global risks (Beck)')
build(g12b, {
    'terms': [
        ('risk society', 'Beck’s term for late modern society, organised around the production and management of risks created by human activity', 'societies debating nuclear power and climate change'),
        ('manufactured risks', 'risks created by human activity, science and technology rather than nature', 'climate change, pollution and nuclear accidents'),
        ('reflexivity', 'the process by which individuals and institutions constantly monitor and reflect on risks and change their behaviour', 'people changing diets after health warnings'),
        ('boomerang effect', 'Beck’s idea that risks eventually affect those who produced them', 'pollution from factories harming wealthy areas too'),
        ('ontological insecurity', 'a feeling of uncertainty and anxiety about the world and one’s place in it', 'anxiety about climate change and job loss'),
    ],
    'thinkers': [
        ('Beck', 'late modern societies are risk societies dealing with manufactured, global risks', 'Late modernity',
         'Beck argued risks such as climate change cross borders and class lines, making society more reflexive.',
         'Critics argue the poor are still much more exposed to risks than the rich.'),
        ('Giddens', 'late modernity is a “runaway world” of global risks that individuals must reflexively manage', 'Late modernity',
         'Giddens argued people must constantly make choices about risk because tradition gives less guidance.',
         'Marxists argue he ignores structural inequality.'),
        ('Furedi', 'societies have developed a “culture of fear” in which risks are exaggerated', 'Interactionism',
         'Furedi argued the media and experts amplify fears about risks.',
         'Some risks, such as climate change, are well supported by evidence.'),
    ],
    'explain': [
        ('Explain the difference between natural and manufactured risks, using an example of each.', 'Natural risks come from nature (e.g. earthquakes, drought); manufactured risks come from human activity and technology (e.g. nuclear accidents, climate change).', '1 mark each meaning; 1 mark each example. [4]'),
        ('Explain what Beck meant by the boomerang effect.', 'Risks created by the wealthy and powerful eventually affect them too; for example, pollution or climate change returns to harm rich countries and classes, so risk cuts across class lines.', '1 mark meaning; 1 mark development; 1 mark example. [3]'),
    ],
    'why': [
        ('example', 'examples', 'of global manufactured risks', ['climate change', 'nuclear accidents', 'pandemics spread by global travel', 'financial crises', 'genetically modified food', 'cyber attacks']),
    ],
    'claims': [
        ('Beck argued that most modern risks are natural disasters.', False, 'Beck stressed manufactured risks created by human activity.'),
        ('Reflexivity means people monitor risks and change their behaviour.', True, 'It is central to Beck’s and Giddens’s accounts of late modernity.'),
    ],
    'ar': ([('Beck argued risk cuts across class lines.', 'manufactured risks such as climate change affect rich and poor alike (the boomerang effect).'),
            ('Late modern societies are reflexive.', 'people and institutions constantly assess and respond to risks.')],
           ['Beck argued modern risks affect only poorer countries.', 'manufactured risks are caused entirely by natural events.']),
    'scen': ['After a nuclear power accident in a neighbouring country, people in {city} stop buying local vegetables, demand radiation tests and protest against building a new power station.',
             'Residents of a poor district in {city} live next to a waste incinerator, while wealthier residents can afford to move away from polluted areas.'],
    'views': {'Late modernity': 'society is a risk society: manufactured global risks lead to reflexivity, as people and institutions monitor and respond to risks (Beck, Giddens).',
              'Marxism': 'risks are produced by capitalism’s pursuit of profit and fall most heavily on the poor and on poorer countries, not equally on all.',
              'Interactionism': 'risks are socially constructed; media and experts define and amplify what people fear (Furedi).',
              'Postmodernism': 'there is no single truth about risk; competing expert claims leave individuals to choose whom to believe.'},
    'ctx': [('how people perceive environmental risks', {'meaning', 'large'}),
            ('how newspapers report climate change', {'media', 'change', 'large'})],
    'methods': ['questionnaire', 'structured interview', 'unstructured interview', 'semi-structured interview', 'content analysis', 'case study', 'official statistics'],
    'data': [dict(what='concern about global risks', pop='adults', rows=['Climate change', 'Pandemics', 'Nuclear accidents'], cols=('Lowest income group', 'Highest income group'), cmp=True, nocount=True,
                  base=[(55, 70), (45, 60), (25, 40)], delta=[(5, 15), (-5, 10), (-10, 5)], label='adults “very worried” about each risk (%)',
                  leads=['A survey of {n} adults in {city} asked how worried they were about global risks.', '{person} surveyed {n} adults about risks. The results by income group are shown below.'],
                  expl=['higher-income groups have more access to information and are more reflexive', 'lower-income groups face more immediate everyday risks', 'concern about global risks cuts across income groups'],
                  method='questionnaire', claim='concern about global risks is shared across social classes, as Beck suggests',
                  counter='Concern is not the same as exposure; poorer groups may face greater actual risk; “very worried” may be interpreted differently.')],
    'essays': [('Explain two features of Beck’s risk society.', 'Manufactured risks; global risks crossing borders; reflexivity; boomerang effect; distrust of experts; individualisation.',
                'Beck’s risk society thesis explains how people respond to global risks',
                'Reflexivity and lifestyle change; environmental movements; manufactured risks such as climate change and pandemics; distrust of experts.',
                'Marxists: risk unequally distributed by class and between countries; Furedi: culture of fear; many people are not reflexive; postmodernists: no shared response.')],
})

g12c = T('Global social movements and the declining power of the nation-state')
build(g12c, {
    'terms': [
        ('new social movement', 'a movement concerned with identity, lifestyle and global issues rather than class interests, often organised through networks', 'environmental and anti-globalisation movements'),
        ('global social movement', 'a social movement that organises across national borders on global issues', 'climate strike movements in many countries'),
        ('anti-globalisation movement', 'a network of groups opposing neoliberal globalisation and the power of TNCs and international organisations', 'protests at WTO and G20 meetings'),
        ('global civil society', 'the network of NGOs, movements and activists operating across borders', 'international human rights organisations'),
        ('sovereignty', 'the supreme authority of a state to govern its own territory', 'a government making its own laws'),
        ('NGO', 'a non-governmental, not-for-profit organisation that works on social or environmental issues', 'an international charity campaigning against poverty'),
    ],
    'thinkers': [
        ('Castells', 'networked social movements use digital communication to organise outside traditional structures', 'Transformationalism',
         'Castells argued the internet allows decentralised movements to challenge powerful institutions.',
         'Online activism may be shallow (“slacktivism”).'),
        ('Klein', 'the anti-globalisation movement challenges the power of global brands and corporations', 'Neo-Marxism',
         'Klein showed how activists exposed sweatshops and corporate power.',
         'Critics argue such movements have achieved few structural changes.'),
        ('Ohmae', 'nation-states are declining in a borderless world economy', 'Hyperglobalism',
         'Ohmae argued global markets and TNCs reduce the power of governments.',
         'Sceptics show states still control borders, armies and taxes.'),
    ],
    'explain': [
        ('Explain two ways in which global social movements differ from older social movements.', 'Focus on global issues and identity rather than class; organised through networks rather than hierarchies; use the internet and social media; operate across borders; involve NGOs and diverse groups.', '2 marks for each explained difference. [4]'),
        ('Explain two reasons why the power of the nation-state may be declining.', 'TNCs and global markets beyond control; international organisations and agreements limit sovereignty; global risks need global solutions; global movements and NGOs; internet beyond state borders.', '2 marks for each explained reason. [4]'),
    ],
    'why': [
        ('method', 'methods', 'used by global social movements', ['online petitions and campaigns', 'coordinated global protests', 'boycotts of brands', 'lobbying international organisations', 'direct action', 'using social media to spread information']),
    ],
    'claims': [
        ('New social movements focus mainly on improving wages for factory workers.', False, 'They focus mainly on identity, lifestyle and global issues such as the environment and human rights.'),
        ('Social media can help movements organise across borders.', True, 'It allows rapid, low-cost coordination of global actions.'),
    ],
    'ar': ([('Global social movements can organise quickly.', 'digital communication allows activists to coordinate across borders.'),
            ('Hyperglobalists argue the nation-state is declining.', 'TNCs and global markets operate beyond the control of governments.')],
           ['new social movements always have a single leader and a strict hierarchy.', 'sceptics argue nation-states have completely lost their sovereignty.']),
    'scen': ['School students in {city} join a global climate strike organised online; on the same day, similar strikes take place in over 100 countries.',
             'Activists in {city} use social media to expose poor conditions in factories supplying a global brand, leading to a worldwide boycott.'],
    'views': {'Transformationalism': 'global movements are part of an emerging global civil society that shares power with states and international bodies (Castells, Held).',
              'Hyperglobalism': 'states are declining, so movements target global corporations and institutions directly.',
              'Globalisation scepticism': 'states remain the key decision-makers; global movements still need to persuade national governments to act.',
              'Neo-Marxism': 'movements challenge the hegemony of global capitalism and corporate power, building counter-hegemonic alternatives (Klein).',
              'Postmodernism': 'movements reflect identity and lifestyle politics; people join fluid networks rather than class-based organisations.'},
    'ctx': [('why young people join climate protests', {'meaning', 'young', 'behaviour'}),
            ('how activists use social media', {'media', 'meaning', 'large'})],
    'methods': ['questionnaire', 'unstructured interview', 'semi-structured interview', 'participant observation', 'non-participant observation', 'content analysis', 'case study'],
    'data': [dict(what='political participation', pop='young people', rows=['Signed an online petition', 'Joined a street protest', 'Voted in the last national election'], cols=('2010', '2022'), nocount=True,
                  base=[(20, 35), (5, 12), (50, 60)], delta=[(15, 30), (3, 10), (-10, 2)], label='young people aged 18-24 who reported each activity (%)',
                  leads=['A national survey of {n} young people aged 18-24 produced the results below.', '{person} compared two surveys, each of {n} young people aged 18-24.'],
                  expl=['social media makes online campaigning easy', 'global issues such as climate change mobilise young people', 'distrust of traditional politics reduces voting'],
                  method='questionnaire', claim='young people are moving from national politics to global social movements',
                  counter='Online petitions require little commitment; voting remains the most common activity; self-report may exaggerate participation.')],
    'essays': [('Explain two features of global social movements.', 'Global issues; network organisation; use of digital media; identity and lifestyle politics; direct action; links with NGOs.',
                'globalisation has reduced the power of the nation-state',
                'Hyperglobalists: TNCs, global markets, international organisations, global movements, internet; states must cooperate (climate agreements).',
                'Sceptics: states control borders, armies, taxation; strong state responses to crises; rising nationalism; transformationalists: power reshaped not lost.')],
})

CHAPTERS[12] = [g12a, g12b, g12c]


# ---------------------------------------------------------------- chapter 13: gender, globalisation and development

g13a = T('Gender and global labour: feminisation of employment')
build(g13a, {
    'terms': [
        ('feminisation of employment', 'the growing proportion of women in paid work, especially in global manufacturing and services', 'young women making up most workers in export factories'),
        ('export processing zone (EPZ)', 'an area where TNCs set up factories for export with tax breaks and weak regulation', 'garment factories employing mainly women'),
        ('global care chain', 'a series of links between people across the world based on paid or unpaid care work', 'a migrant nanny caring for children abroad while her own children are cared for by relatives'),
        ('double burden', 'the combination of paid work and unpaid domestic labour carried out by many women', 'a factory worker who also does all the housework'),
        ('informal sector', 'work that is unregulated, unprotected and often unrecorded', 'street vending and home-based piecework'),
    ],
    'thinkers': [
        ('Elson and Pearson', 'TNCs employ young women because they are seen as cheap, docile and “nimble-fingered”', 'Marxist feminism',
         'Elson and Pearson argued gender stereotypes are used to justify low pay for women in world market factories.',
         'Some women gain independence and income from factory work.'),
        ('Ehrenreich and Hochschild', 'global care chains transfer care work from poor to rich countries', 'Marxist feminism',
         'They argued migrant women do care work for richer families while their own families lose care.',
         'Migrants may gain income and autonomy.'),
        ('Kabeer', 'paid work can increase women’s bargaining power even in difficult conditions', 'Liberal feminism',
         'Kabeer’s study of Bangladeshi garment workers found work gave women greater say in household decisions.',
         'Others stress exploitation and poor conditions.'),
    ],
    'explain': [
        ('Explain two reasons why TNCs often employ young women in export factories.', 'Women can be paid less; stereotypes of “nimble fingers” and docility; less likely to be unionised; seen as temporary workers; flexible short contracts.', '2 marks for each explained reason. [4]'),
        ('Explain what is meant by a global care chain, using an example.', 'A series of links between women across countries based on care work, e.g. a woman migrates to care for a wealthy family’s children while her own children are cared for by her mother or a poorer local woman.', '1 mark meaning; 1 mark development; 1 mark example. [3]'),
    ],
    'why': [
        ('effect', 'effects', 'of factory employment on women in developing countries', ['independent income', 'greater bargaining power in the household', 'low pay and long hours', 'health problems from poor conditions', 'double burden of paid and domestic work', 'insecure contracts']),
    ],
    'claims': [
        ('Most workers in export garment factories are older men.', False, 'Most are young women.'),
        ('Paid work can increase women’s power within the household.', True, 'Kabeer found earning gave women more say in decisions.'),
    ],
    'ar': ([('Many export factories employ mainly women.', 'employers believe women can be paid less and are less likely to join unions.'),
            ('Women in paid work often face a double burden.', 'they remain responsible for most unpaid domestic labour.')],
           ['the feminisation of employment means fewer women are in paid work.', 'Elson and Pearson argued that women are paid more than men in world market factories.']),
    'scen': ['{woman}, aged 19, moved from her village to work in a garment factory near {city}; she works 60 hours a week, sends money home and now helps decide how her family spends it.',
             'A factory supplying a global fashion brand near {city} employs 3,000 women on machines, while all its supervisors and managers are men.'],
    'views': {'Marxist feminism': 'TNCs exploit women as cheap, flexible labour, using gender stereotypes to keep wages low; capitalism and patriarchy work together (Elson and Pearson).',
              'Liberal feminism': 'paid work gives women income, independence and bargaining power; improved rights and education can reduce inequality (Kabeer).',
              'Radical feminism': 'patriarchy continues in the factory: men control women as supervisors, and women still carry the double burden at home.',
              'Neoliberalism': 'factory jobs created by free trade give women opportunities and income that would not otherwise exist.'},
    'ctx': [('the experiences of women working in export factories', {'meaning', 'sensitive', 'hidden', 'behaviour'}),
            ('the changing share of women in global employment', {'large', 'change'})],
    'data': [dict(what='women’s employment', pop='workers', rows=['Garment manufacturing', 'Electronics assembly', 'Factory supervisors and managers'], cols=('1995', '2020'), nocount=True, n=[3],
                  base=[(60, 75), (45, 60), (8, 15)], delta=[(5, 15), (5, 15), (2, 8)], label='percentage of workers who are women',
                  leads=['The table shows official employment data from a country near {city} with large export factories.', 'Official data on women’s share of jobs in export industries are shown below.'],
                  expl=['TNCs prefer women as cheaper and more flexible workers', 'export industries have grown', 'managerial jobs are still dominated by men (vertical segregation)'],
                  method='official statistics', claim='globalisation has improved women’s position in the labour market',
                  counter='More jobs do not mean better pay or conditions; women remain under-represented in management; informal work is not recorded.')],
    'essays': [('Explain two ways in which globalisation has affected women’s employment.', 'Feminisation of factory work in EPZs; global care chains; growth of service work; informal sector; migration for work.',
                'globalisation has exploited rather than empowered women workers',
                'Elson and Pearson; low pay, poor conditions, factory disasters; global care chains (Ehrenreich and Hochschild); double burden; patriarchal supervision.',
                'Kabeer: increased bargaining power; independent income; delayed marriage; trade unions and campaigns improving conditions; liberal feminist view of progress.')],
})

g13b = T('Women, development and empowerment')
build(g13b, {
    'terms': [
        ('empowerment', 'the process by which people gain power and control over their own lives and choices', 'women gaining the right to own land'),
        ('Gender Inequality Index (GII)', 'a UN measure of gender inequality in health, empowerment and the labour market', 'comparing maternal mortality and women in parliament'),
        ('microfinance', 'small loans to poor people, often women, to start businesses', 'a woman borrowing to buy a sewing machine'),
        ('Women in Development (WID)', 'an approach that aimed to include women in existing development projects', 'training women in new farming techniques'),
        ('Gender and Development (GAD)', 'an approach focusing on changing unequal gender relations rather than just including women', 'projects challenging men’s control of household income'),
        ('maternal mortality', 'deaths of women from causes related to pregnancy and childbirth', 'deaths per 100,000 live births'),
    ],
    'thinkers': [
        ('Boserup', 'development projects often ignored or worsened women’s position because planners assumed men were farmers', 'Liberal feminism',
         'Boserup showed that women did much of the farming in Africa but technology and training were given to men.',
         'Later feminists argued including women was not enough; gender relations needed to change.'),
        ('Sen', 'development should be measured as the expansion of people’s freedoms and capabilities', 'Liberal feminism',
         'Sen showed that educating women reduces child mortality and fertility and increases agency.',
         'Critics argue capabilities are hard to measure.'),
        ('Yunus', 'small loans to poor women can reduce poverty and empower them', 'Neoliberalism',
         'Yunus founded the Grameen Bank, lending mainly to poor women in Bangladesh.',
         'Critics found some borrowers fell into debt and men controlled the loans.'),
    ],
    'explain': [
        ('Explain two ways in which education may empower women in developing countries.', 'Access to paid employment and income; knowledge of health and family planning reduces fertility and child mortality; greater confidence and political participation; delays early marriage.', '2 marks for each explained way. [4]'),
        ('Explain the difference between the WID and GAD approaches to development.', 'WID tried to include women in existing development projects; GAD focuses on changing the unequal power relations between men and women that cause disadvantage.', '1 mark each approach; 1 mark contrast. [3]'),
    ],
    'why': [
        ('barrier', 'barriers', 'to women’s empowerment in developing countries', ['lack of education', 'early marriage', 'lack of land and property rights', 'unpaid domestic labour', 'violence against women', 'religious or cultural norms', 'limited political representation']),
    ],
    'claims': [
        ('Microfinance loans are mainly given to large companies.', False, 'Microfinance provides small loans to poor people, often women.'),
        ('Educating girls is linked to lower child mortality.', True, 'Educated mothers have more knowledge of health and nutrition.'),
    ],
    'ar': ([('Many development agencies target women.', 'investing in women’s education and income benefits whole families.'),
            ('The GAD approach criticises WID.', 'simply including women in projects does not change unequal gender relations.')],
           ['Boserup argued that development projects had always benefited women more than men.', 'microfinance means large loans from the IMF to governments.']),
    'scen': ['A microfinance scheme near {city} lends small sums to groups of women; after five years many run small shops, but some have handed the loans to their husbands.',
             'A government near {city} introduces free secondary schooling for girls; ten years later, the average age of marriage has risen and family size has fallen.'],
    'views': {'Liberal feminism': 'education, legal rights and access to credit and jobs gradually empower women and promote development (Boserup, Sen).',
              'Radical feminism': 'development projects do not challenge patriarchy; men often control women’s loans and income, so real empowerment requires changing gender relations.',
              'Neoliberalism': 'microfinance and markets allow women to become entrepreneurs, reducing poverty through self-help (Yunus).',
              'Post-development theory': 'empowerment programmes impose Western ideas of the liberated woman; local women should define their own goals.'},
    'ctx': [('the effects of microfinance on women’s lives', {'meaning', 'behaviour', 'change'}),
            ('girls’ school enrolment across countries', {'large', 'change'})],
    'data': [dict(what='girls’ education', pop='girls', rows=['Country A', 'Country B', 'Country C'], cols=('2000', '2020'), nocount=True, n=[3],
                  base=[(20, 35), (40, 55), (60, 75)], delta=[(15, 30), (10, 25), (5, 15)], label='girls enrolled in secondary school (%)',
                  leads=['The table shows official data on girls’ secondary school enrolment in three countries.', 'UNESCO figures for girls’ secondary enrolment in three countries are shown below.'],
                  expl=['free schooling and government policy', 'development programmes targeting girls', 'changing attitudes to girls’ education and marriage'],
                  method='official statistics', claim='development is empowering women',
                  counter='Enrolment is not the same as completion or quality; education may not lead to jobs; power within households may be unchanged.')],
    'essays': [('Explain two ways in which development programmes have tried to empower women.', 'Girls’ education; microfinance; health and family planning; land rights; quotas for women in politics; GAD projects.',
                'development has improved the position of women in developing countries',
                'Rising education and literacy; lower maternal mortality; more women in paid work and politics; microfinance (Yunus); Sen and Kabeer.',
                'Patriarchy persists; exploitation in factories; men control loans; double burden; post-development and postcolonial critiques of Western models.')],
})

g13c = T('Feminist critiques of development theory')
build(g13c, {
    'terms': [
        ('androcentrism', 'the tendency to see the world from a male point of view and treat men’s experience as the norm', 'development statistics measuring only paid work'),
        ('invisible labour', 'unpaid work, mainly by women, that is not counted in measures such as GDP', 'collecting water and caring for children'),
        ('ecofeminism', 'a perspective linking the domination of women with the domination of nature', 'women leading forest protection movements'),
        ('postcolonial feminism', 'a perspective criticising Western feminism for treating women in developing countries as passive victims', 'Mohanty’s critique of “Third World woman” stereotypes'),
        ('gender blindness', 'failure to recognise how men and women are affected differently by policies', 'giving farm training only to men'),
    ],
    'thinkers': [
        ('Mohanty', 'Western feminists often portray women in the developing world as a single, passive, oppressed group', 'Postcolonial feminism',
         'Mohanty argued women’s experiences differ by class, culture and history and they actively shape their own lives.',
         'Some argue common forms of patriarchy do exist across societies.'),
        ('Shiva', 'Western development destroyed women’s traditional knowledge and harmed the environment', 'Radical feminism',
         'Shiva, an ecofeminist, argued “maldevelopment” replaced women’s sustainable practices with commercial agriculture.',
         'Critics argue she romanticises traditional life.'),
        ('Boserup', 'modernisation projects gave technology and training to men and ignored women’s farming roles', 'Liberal feminism',
         'Boserup showed development could worsen women’s status.',
         'Later feminists argued her solutions did not challenge patriarchy.'),
    ],
    'explain': [
        ('Explain two feminist criticisms of modernisation theory.', 'Gender blind: ignores women’s roles; assumes men are breadwinners; development projects gave resources to men (Boserup); GDP ignores unpaid labour; Western ideal of the family imposed.', '2 marks for each explained criticism. [4]'),
        ('Explain the postcolonial feminist criticism of Western feminism.', 'It treats women in developing countries as a single, passive victim group, ignoring diversity of class, culture and history and women’s agency (Mohanty).', '1 mark idea; 1 mark development; 1 mark sociologist or example. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'that feminists make of development theories', ['they ignore women’s unpaid labour', 'they are gender blind', 'they assume a male breadwinner', 'they treat Western women’s lives as the model', 'they ignore environmental harm affecting women']),
    ],
    'claims': [
        ('Feminists argue GDP fully measures women’s contribution to the economy.', False, 'GDP ignores most unpaid domestic and subsistence work, much of which is done by women.'),
        ('Ecofeminists link the domination of women and nature.', True, 'Shiva argues both are exploited by Western patriarchal development.'),
    ],
    'ar': ([('Feminists argue women’s work is often invisible in development statistics.', 'measures such as GDP count paid work but not unpaid domestic labour.'),
            ('Postcolonial feminists criticise some Western feminists.', 'they portray women in poorer countries as passive victims rather than active agents.')],
           ['Boserup argued that development projects gave women more resources than men.', 'ecofeminists support large-scale commercial agriculture.']),
    'scen': ['A development agency near {city} introduces tractors and training for farmers, giving them only to men, although women grow most of the food in the area.',
             'A Western charity’s advertisement shows women in a village near {city} as helpless victims, although the women run a successful savings cooperative.'],
    'views': {'Liberal feminism': 'development must include women equally in training, education and resources; projects have been gender blind (Boserup).',
              'Radical feminism': 'development is patriarchal: it extends male control over women and nature (Shiva).',
              'Postcolonial feminism': 'women in poorer countries are diverse and active; Western representations of them as victims are themselves a form of domination (Mohanty).',
              'Marxist feminism': 'development under capitalism exploits women’s paid and unpaid labour for profit.'},
    'ctx': [('how women farmers experience development projects', {'meaning', 'behaviour', 'hidden'}),
            ('how charity advertisements represent women', {'media', 'large'})],
    'methods': ['questionnaire', 'unstructured interview', 'semi-structured interview', 'participant observation', 'content analysis', 'case study'],
    'data': [dict(what='time use', pop='adults', rows=['Paid work', 'Unpaid domestic and care work', 'Collecting water and fuel'], cols=('Women', 'Men'), unit='', uname='hours', cmp=True, nocount=True,
                  base=[(3, 5), (5, 7), (1, 2)], delta=[(1, 3), (-5, -3), (-1, 0)], label='average hours per day spent on each activity',
                  leads=['A time-use diary study of {n} adults in villages near {city} produced the results below.', '{person} asked {n} adults near {city} to keep time-use diaries. The averages are shown below.'],
                  expl=['women carry most unpaid domestic labour (double burden)', 'unpaid work is invisible in GDP', 'gender roles allocate paid work to men'],
                  method='personal documents', claim='development measures ignore much of women’s work',
                  counter='Diaries may be incomplete or inaccurate; one area may be untypical; men’s informal work may also be under-recorded.')],
    'essays': [('Explain two feminist criticisms of development theory.', 'Gender blindness (Boserup); unpaid labour ignored; Western bias (Mohanty); ecofeminist critique (Shiva); male breadwinner assumption.',
                'feminist critiques have improved our understanding of development',
                'Exposed gender blindness; GAD approach; GII and gender-sensitive measures; recognition of unpaid labour; postcolonial and ecofeminist insights.',
                'Feminists disagree among themselves; ecofeminism romanticises tradition; class and global inequality may matter more (Marxists); focus on women can overlook men and children.')],
})

CHAPTERS[13] = [g13a, g13b, g13c]


# ============================================================== MEDIA (chapters 14-19)

MEDIA_M = ['questionnaire', 'structured interview', 'unstructured interview', 'semi-structured interview', 'participant observation',
           'non-participant observation', 'laboratory experiment', 'field experiment', 'content analysis', 'case study', 'official statistics']

VM = {
    'Marxism': 'the media are owned and controlled by a capitalist class who use them to spread ruling-class ideology, creating false consciousness and protecting capitalism (Miliband, Murdock and Golding).',
    'Neo-Marxism': 'media content reflects ideological hegemony: journalists from similar backgrounds share middle-class, pro-establishment assumptions, so dominant values appear as common sense (Glasgow University Media Group, Hall).',
    'Pluralism': 'power in society is spread between many competing groups; the media are diverse, respond to audience demand and reflect a range of views, so no single group controls them.',
    'Postmodernism': 'media-saturated society offers endless choice; audiences actively construct identities from media images, and reality and representation blur (Baudrillard, Strinati).',
    'Interactionism': 'media help construct social reality and labels; audiences interpret messages actively, and media reactions can amplify deviance (Cohen, Young).',
    'Liberal feminism': 'the media reinforce gender stereotypes through socialisation, but representations are improving as more women work in the media (Tuchman, Gauntlett).',
    'Radical feminism': 'the media are part of patriarchal culture: they objectify women, present male dominance as normal and serve men’s interests (Mulvey, Wolf).',
}


def g14a_cr(r, D):
    for _ in range(60):
        k = 6
        sh = sorted([r.randint(4, 32) for _ in range(k)], reverse=True)
        if sum(sh) <= 92 and len(set(sh)) == k:
            break
    else:
        sh = [28, 21, 15, 10, 7, 5]
    other = 100 - sum(sh)
    firms = r.sample(['Firm P', 'Firm Q', 'Firm R', 'Firm S', 'Firm T', 'Firm U', 'Firm V', 'Firm W'], 6)
    mkt = r.choice(['national newspaper', 'television news', 'commercial radio', 'online news', 'music streaming', 'magazine publishing'])
    d = ctxd(r)
    tab = 'Table: share of the ' + mkt + ' market (%) | ' + ' '.join(f'{f} | {s}%.' for f, s in zip(firms, sh)) + f' All other firms | {other}%.'
    intro = f'The table shows the share of the {mkt} market held by the largest companies in a country near {d["city"]}. {tab}'
    cr4, cr3 = sum(sh[:4]), sum(sh[:3])
    if D <= 1:
        ds = [f'{x}%' for x in dict.fromkeys([cr3, sum(sh[:5]), sh[0] * 4, cr4 + 10, cr4 - 10, 100 - cr4]) if x != cr4 and 0 < x <= 100][:3]
        opts, a = mcq(r, f'{cr4}%', ds)
        return {'stem': f'{intro} The four-firm concentration ratio is the combined market share of the four largest firms. What is the four-firm concentration ratio for this market?',
                'options': opts, 'answer': a, 'key': f'{" + ".join(map(str, sh[:4]))} = {cr4}%. [1]', 'marks': 1}
    conc = 'highly concentrated (an oligopoly)' if cr4 >= 60 else 'moderately concentrated' if cr4 >= 40 else 'relatively competitive'
    rel = sh[0] / sh[5]
    parts = [('Calculate the four-firm concentration ratio (the combined share of the four largest firms).', f'{" + ".join(map(str, sh[:4]))} = {cr4}%.', '1 mark method; 1 mark answer. [2]'),
             (f'Using your answer, describe how concentrated this market is. (Treat a ratio of 60% or more as highly concentrated, 40-59% as moderately concentrated and below 40% as competitive.)', f'{cr4}% means the market is {conc}.', '1 mark. [1]'),
             (f'How many times larger is the market share of {firms[0]} than that of {firms[5]}? Give your answer to 1 decimal place.', f'{sh[0]} ÷ {sh[5]} = {rel:.1f} times.', '1 mark method; 1 mark answer. [2]'),
             ('Explain how a Marxist sociologist might interpret these data.', 'Concentration of ownership gives a small capitalist class control over media content, allowing it to spread ideology and limit opposing views (Miliband, Murdock and Golding).', '1 mark Marxist idea; 1 mark application to the data. [2]'),
             ('Explain how a pluralist sociologist might respond to a Marxist interpretation of these data.', 'Many firms still compete; owners must give audiences what they want to make profits; journalists have professional independence; new media and smaller firms provide diversity.', '1 mark pluralist idea; 1 mark application. [2]'),
             ('Explain one limitation of using market share to measure media power.', 'Market share does not show influence on content or audiences; online and global media may not be counted; owners may not interfere; audiences interpret content actively.', '1 mark identifying; 1 mark explaining. [2]')]
    if D == 2:
        sel = parts[:2]
    elif D == 3:
        sel = parts[:3]
    elif D == 4:
        sel = parts[:2] + [parts[3], r.choice(parts[4:])]
    else:
        sel = parts[:3] + [parts[3], r.choice(parts[4:])]
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


g14a = T('Concentration of ownership and media conglomerates')
build(g14a, {
    'terms': [
        ('concentration of ownership', 'the process by which the ownership of media is held by fewer and fewer companies', 'a handful of firms owning most national newspapers'),
        ('media conglomerate', 'a large company that owns many different types of media and often other businesses', 'a corporation owning film studios, TV channels and streaming services'),
        ('horizontal integration', 'when a media company takes over other companies in the same type of media', 'a newspaper group buying rival newspapers'),
        ('vertical integration', 'when a media company owns all stages of production, distribution and sale', 'a film studio owning cinemas and a streaming platform'),
        ('diversification', 'when a media company expands into different types of media or other industries', 'a TV company buying a football club'),
        ('synergy', 'the cross-promotion of a product across the different media owned by one company', 'a film promoted through the owner’s TV channels, music and games'),
        ('technological convergence', 'the merging of different media into single digital platforms', 'watching TV, reading news and gaming on one smartphone'),
    ],
    'thinkers': [
        ('Bagdikian', 'a small number of corporations control most of the media, limiting diversity', 'Marxism',
         'Bagdikian showed the number of companies controlling most US media fell from 50 in 1983 to a handful by the 2000s.',
         'Pluralists point to the huge number of online sources available.'),
        ('Doyle', 'concentration of ownership reduces diversity and gives owners political influence', 'Neo-Marxism',
         'Doyle argued cross-media ownership threatens the range of viewpoints available in democratic societies.',
         'Owners may avoid interference to protect profits and credibility.'),
        ('Compaine', 'there is still plenty of competition and diversity in the media market', 'Pluralism',
         'Compaine argued concentration is exaggerated and new firms and the internet keep markets competitive.',
         'Critics note that online audiences are concentrated on a few giant platforms.'),
    ],
    'explain': [
        ('Explain the difference between horizontal and vertical integration, using an example of each.', 'Horizontal: buying companies in the same media sector (e.g. a newspaper group buying more newspapers); vertical: owning all stages of production and distribution (e.g. a studio owning cinemas and streaming).', '1 mark each definition; 1 mark each example. [4]'),
        ('Explain two consequences of the concentration of media ownership.', 'Reduced diversity of views; owners can influence content and politics; synergy and cross-promotion; homogenised content; barriers to entry for new firms; economies of scale.', '2 marks for each explained consequence. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'for the growth of media conglomerates', ['economies of scale reduce costs', 'synergy allows cross-promotion', 'digital convergence links different media', 'globalisation opens new markets', 'deregulation allows mergers', 'spreading risk across sectors']),
    ],
    'claims': [
        ('Vertical integration means a company buys its rivals in the same type of media.', False, 'That is horizontal integration; vertical integration means owning all stages from production to distribution.'),
        ('Synergy involves promoting one product across several media owned by the same company.', True, 'For example a film, its soundtrack and video game promoted together.'),
    ],
    'ar': ([('Media conglomerates use synergy.', 'owning several types of media allows them to cross-promote products.'),
            ('Some sociologists worry about concentration of ownership.', 'fewer owners may mean a narrower range of views.')],
           ['horizontal integration means owning cinemas as well as studios.', 'Bagdikian found the number of major media owners had greatly increased.']),
    'scen': ['A single company in {city} owns two national newspapers, a television channel, a radio network and the country’s most popular news website.',
             'A global entertainment corporation releases a film, then promotes it through its own TV channels, sells the soundtrack on its music label and launches a video game through its games division.'],
    'views': VM,
    'ctx': [('the views of journalists working for large media companies', {'meaning', 'hidden'}),
            ('how far news content differs between newspapers owned by the same company', {'media', 'large'})],
    'methods': MEDIA_M,
    'data': [dict(what='newspaper ownership', pop='newspapers', rows=['Company A', 'Company B', 'Company C'], cols=('2000', '2022'), nocount=True, n=[3], share=True,
                  base=[(20, 28), (15, 22), (10, 16)], delta=[(5, 12), (2, 8), (-4, 2)], label='share of national newspaper circulation (%)',
                  leads=['The table shows the share of newspaper circulation held by the three largest companies in a country near {city}.', 'Industry figures on newspaper circulation are shown below.'],
                  expl=['mergers and takeovers (horizontal integration)', 'smaller papers closed as advertising moved online', 'economies of scale favour large companies'],
                  method='official statistics', claim='media ownership is becoming more concentrated',
                  counter='Print circulation is falling; online news offers many alternative sources; ownership share does not prove control over content.')],
    'essays': [('Explain two trends in media ownership.', 'Concentration; conglomeration; horizontal and vertical integration; diversification; globalisation; technological convergence.',
                'the concentration of media ownership threatens democracy',
                'Bagdikian and Doyle: fewer owners, less diversity; owners’ political influence; Marxist instrumentalist view (Miliband); synergy produces homogenised content.',
                'Pluralists (Compaine): competition and regulation; public service broadcasting; internet and citizen journalism; owners prioritise profit not ideology; audiences active.')],
})
_reg(g14a, 'C3', (1, 2, 3, 4, 5), 'numerical', g14a_cr, 'cr4')

g14b = T('Marxist and neo-Marxist (hegemonic) approaches to media control')
build(g14b, {
    'terms': [
        ('instrumental Marxism', 'the view that owners directly use the media as tools to spread ruling-class ideology', 'a proprietor telling editors which party to support'),
        ('hegemony', 'Gramsci’s term for the dominance of ruling-class ideas achieved through consent rather than force', 'audiences accepting that free markets are “common sense”'),
        ('political economy approach', 'the view that economic factors such as profit and advertising shape media content', 'avoiding stories that upset advertisers'),
        ('false consciousness', 'a distorted view of reality that prevents the working class from seeing its exploitation', 'believing inequality is natural and fair'),
        ('ideological state apparatus', 'Althusser’s term for institutions such as the media that spread ruling-class ideology', 'TV and newspapers promoting consumerism'),
        ('bias', 'a one-sided or distorted presentation of events', 'strike reports focusing on disruption rather than workers’ grievances'),
    ],
    'thinkers': [
        ('Miliband', 'the media are used by the capitalist class to legitimate capitalism and divert attention from inequality', 'Marxism',
         'Miliband argued owners use the media to create false consciousness and present capitalism as natural.',
         'Journalists have professional independence; owners rarely intervene directly.'),
        ('Murdock and Golding', 'economic pressures such as profit and advertising narrow media content to safe, popular material', 'Marxism',
         'Their political economy approach shows how the need for profit and advertising limits critical content.',
         'Pluralists argue content reflects audience demand.'),
        ('Glasgow University Media Group', 'news reflects the middle-class, establishment views of journalists and favours the powerful', 'Neo-Marxism',
         'Their content analysis of industrial disputes showed managers framed as reasonable and strikers as disruptive.',
         'Critics argue they read their own bias into the content.'),
        ('Hall', 'media encode preferred readings that support dominant ideology, though audiences may decode them differently', 'Neo-Marxism',
         'Hall’s encoding/decoding model shows hegemonic messages can be accepted, negotiated or resisted.',
         'Pluralists deny the existence of a single dominant ideology.'),
    ],
    'explain': [
        ('Explain the difference between instrumental Marxist and neo-Marxist (hegemonic) views of media control.', 'Instrumental: owners directly control content to spread ideology (Miliband); hegemonic: journalists’ shared middle-class values produce pro-establishment content without owners’ interference (GUMG).', '1 mark each view; 1 mark explicit contrast. [3]'),
        ('Explain two ways in which media owners might influence media content.', 'Appointing editors who share their views; setting editorial policy; direct intervention in coverage; cutting budgets for investigative journalism; promoting their other businesses (synergy).', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of the Marxist view of the media', ['journalists have professional independence', 'audiences interpret messages actively', 'media content is diverse', 'owners mainly want profit, not ideology', 'regulation and public service broadcasting limit owners’ power']),
    ],
    'claims': [
        ('Neo-Marxists argue owners personally decide the content of every news story.', False, 'Neo-Marxists stress journalists’ shared values (hegemony); direct control is the instrumental Marxist view.'),
        ('The Glasgow University Media Group used content analysis of news.', True, 'They analysed TV news coverage of strikes and conflicts.'),
    ],
    'ar': ([('Neo-Marxists say media bias can occur without owners interfering.', 'journalists from similar backgrounds share establishment values.'),
            ('Murdock and Golding stress economic pressures on media.', 'the need for advertising revenue limits critical content.')],
           ['hegemony means rule by force alone.', 'the Glasgow University Media Group found that strikers were usually presented positively.']),
    'scen': ['During a dock strike in {city}, most news reports interview managers in their offices and show queues of lorries, while strikers are filmed shouting at the gates.',
             'A newspaper owner in {city} appoints a new editor who shares his views; within a year the paper stops criticising the government’s tax policy.'],
    'views': {k: VM[k] for k in ('Marxism', 'Neo-Marxism', 'Pluralism', 'Postmodernism')},
    'ctx': [('how television news reports industrial disputes', {'media', 'large'}),
            ('how journalists decide what to report', {'meaning', 'behaviour', 'hidden'})],
    'methods': MEDIA_M,
    'source': [dict(text='A content analysis of 120 television news reports about strikes in {city} found that managers were interviewed in 70% of reports and strikers in 35%. Words such as “demands” and “threats” were used for unions, while managers “offered” and “proposed”.',
                    method='content analysis', about='bias in news reporting', finds=['managers were interviewed twice as often as strikers', 'language presented unions as aggressive and managers as reasonable'],
                    persp='Neo-Marxism', pview='The findings support the Glasgow University Media Group: journalists’ shared, establishment assumptions produce news that presents the powerful as reasonable, reinforcing hegemony.',
                    claim='the news media are biased in favour of the powerful', pro='The source shows unequal access and loaded language; GUMG and Hall argue news reflects dominant ideology.',
                    con='Pluralists argue news reflects news values and audience demand; content analysis cannot show intentions or audience effects; coding is open to researcher bias; other reports may differ.', flags={'media', 'large'})],
    'essays': [('Explain two ways in which media content may reflect ruling-class ideology.', 'Owner intervention (instrumental); hegemonic assumptions of journalists (GUMG); economic pressures of advertising (Murdock and Golding); preferred readings (Hall); exclusion of radical views.',
                'the media are controlled by a ruling class in the interests of capitalism',
                'Miliband; Murdock and Golding; GUMG’s bad news studies; concentration of ownership (Bagdikian); examples of owner intervention.',
                'Pluralism: diversity, competition, professional journalism, regulation; postmodernism: fragmented audiences; Hall: audiences decode differently; new media alternatives.')],
})

g14c = T('Pluralist approaches to media ownership and control')
build(g14c, {
    'terms': [
        ('pluralism', 'the view that power in society is spread across many competing groups, and that the media reflect this diversity', 'a wide range of newspapers with different political views'),
        ('consumer sovereignty', 'the idea that audiences’ choices determine what the media produce', 'programmes with low ratings being cancelled'),
        ('public service broadcasting', 'broadcasting funded by the public and required to inform, educate and entertain all sections of society', 'a licence-fee-funded national broadcaster'),
        ('regulation', 'rules set by governments or independent bodies to control media content and ownership', 'a regulator requiring balance in TV news'),
        ('professional ethics', 'the standards of accuracy, balance and independence that journalists are expected to follow', 'checking sources before publishing a story'),
    ],
    'thinkers': [
        ('Whale', 'media owners must give audiences what they want or they lose sales and profits', 'Pluralism',
         'Whale argued that commercial pressures, not owners’ views, determine media content.',
         'Marxists argue audience demand is itself shaped by the media.'),
        ('Compaine', 'the media market remains competitive and diverse', 'Pluralism',
         'Compaine argued the internet and new entrants prevent any single company from dominating.',
         'Large platforms dominate online audiences.'),
        ('Curran', 'there is little evidence of owners directly controlling content, but commercial pressures narrow diversity', 'Neo-Marxism',
         'Curran found owners intervened at times, but pressures of profit and advertising were more important.',
         'Pluralists argue his evidence of intervention is limited to a few cases.'),
    ],
    'explain': [
        ('Explain two reasons why pluralists argue that media owners cannot control media content.', 'Audiences choose what they consume (consumer sovereignty); journalists follow professional ethics; regulation requires balance; competition between many media; owners need profits so must satisfy audiences.', '2 marks for each explained reason. [4]'),
        ('Explain one criticism of the pluralist view of the media.', 'Concentration of ownership means few owners; owners do intervene; audience demand is shaped by media and advertising; diversity is limited to mainstream views; online audiences dominated by a few platforms.', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('argument', 'arguments', 'used by pluralists to support their view of the media', ['audiences have a wide choice of media', 'journalists are professionally independent', 'regulation limits bias', 'owners must satisfy audiences to make profits', 'new media allow anyone to publish']),
    ],
    'claims': [
        ('Pluralists argue that a single ruling class controls media content.', False, 'That is the Marxist view; pluralists argue power is spread among many groups.'),
        ('Consumer sovereignty means audience choices influence media content.', True, 'Media must give audiences what they want to stay profitable.'),
    ],
    'ar': ([('Pluralists argue media content reflects audience demand.', 'commercial media must attract audiences to earn profits.'),
            ('Marxists criticise the pluralist view.', 'they argue audience tastes are shaped by advertising and ideology.')],
           ['pluralists argue regulation of the media is unnecessary because owners decide all content.', 'consumer sovereignty means that the government chooses what audiences watch.']),
    'scen': ['A TV channel in {city} cancels an expensive drama after poor ratings and replaces it with a cheaper reality show that attracts younger viewers.',
             'In {city}, readers can choose between eight national newspapers with different political positions, a public service broadcaster and thousands of online news sources.'],
    'views': {k: VM[k] for k in ('Pluralism', 'Marxism', 'Neo-Marxism', 'Postmodernism')},
    'ctx': [('how audiences choose which news sources to use', {'meaning', 'large', 'behaviour'}),
            ('the range of political views in national newspapers', {'media', 'large'})],
    'methods': MEDIA_M,
    'data': [dict(what='news sources', pop='adults', rows=['Television', 'Social media', 'Print newspapers'], cols=('2013', '2023'), nocount=True,
                  base=[(70, 80), (20, 30), (40, 50)], delta=[(-20, -10), (20, 35), (-25, -15)], label='adults using each source for news in the last week (%)',
                  leads=['A survey of {n} adults in {city} asked where they got their news.', '{person} compared two surveys of {n} adults about sources of news.'],
                  expl=['the internet and smartphones have increased choice', 'young people prefer social media', 'print newspapers have declined'],
                  method='questionnaire', claim='audiences now have more choice, as pluralists argue',
                  counter='Social media news may come from the same large organisations; algorithms limit what people see; choice of source is not the same as diversity of views.')],
    'essays': [('Explain two features of the pluralist view of the media.', 'Diversity and competition; consumer sovereignty; professional journalism; regulation and public service broadcasting; power spread between groups.',
                'the pluralist view of media ownership and control is more convincing than the Marxist view',
                'Consumer sovereignty (Whale); diversity and competition (Compaine); regulation; journalists’ independence; new media and citizen journalism.',
                'Marxists: concentration (Bagdikian), owner intervention, hegemony (GUMG), advertising pressures (Curran, Murdock and Golding); diversity is within narrow limits.')],
})

CHAPTERS[14] = [g14a, g14b, g14c]


g15a = T('News values, agenda-setting and gatekeeping')
build(g15a, {
    'terms': [
        ('news values', 'the criteria journalists use to decide whether an event is newsworthy', 'negativity, celebrity and proximity'),
        ('gatekeeping', 'the power of editors and journalists to decide which stories are included or excluded', 'an editor dropping a story about a distant flood'),
        ('agenda-setting', 'the media’s power to influence what issues the public thinks about by choosing what to cover', 'crime becoming a top public concern after weeks of coverage'),
        ('framing', 'the way the media present a story, highlighting some aspects and ignoring others', 'describing protesters as “rioters” or “campaigners”'),
        ('news diary', 'a list of planned events that journalists know will happen and can prepare to cover', 'elections, budgets and royal visits'),
        ('social construction of news', 'the idea that news is not simply a reflection of reality but is produced by organisations through selection and presentation', 'two papers reporting the same event very differently'),
    ],
    'thinkers': [
        ('Galtung and Ruge', 'journalists select stories according to news values such as negativity, elite persons and unexpectedness', 'Interactionism',
         'Galtung and Ruge identified news values that explain why some events become news.',
         'Critics argue digital news is shaped more by clicks and algorithms.'),
        ('McCombs and Shaw', 'the media set the agenda for what audiences think about', 'Pluralism',
         'McCombs and Shaw found voters’ priorities matched the issues emphasised in election coverage.',
         'Audiences may already share concerns; the direction of cause is unclear.'),
        ('Cohen and Young', 'news is manufactured through selection and presentation, not discovered', 'Interactionism',
         'Cohen and Young’s “The Manufacture of News” showed how journalists construct news.',
         'Marxists argue ideology shapes selection more than practical routines.'),
    ],
    'explain': [
        ('Explain two news values, using an example of each.', 'Negativity (disasters, crime); elite persons (celebrities, leaders); proximity (local or culturally close events); unexpectedness; personalisation; threshold (size of event).', '1 mark each news value; 1 mark each example. [4]'),
        ('Explain the difference between gatekeeping and agenda-setting.', 'Gatekeeping is the selection or rejection of stories by editors and journalists; agenda-setting is the effect of this selection on which issues the public sees as important.', '1 mark each; 1 mark contrast. [3]'),
    ],
    'why': [
        ('factor', 'factors', 'influencing which stories become news', ['news values', 'the news diary', 'cost and availability of reporters', 'deadlines and time constraints', 'owners and advertisers', 'audience interest and clicks']),
    ],
    'claims': [
        ('News is a neutral and complete reflection of all important events.', False, 'News is socially constructed through gatekeeping, news values and framing.'),
        ('Negativity is a common news value.', True, 'Bad news such as disasters and crime is more likely to be reported.'),
    ],
    'ar': ([('Stories about celebrities are often reported.', 'elite persons are an important news value.'),
            ('News is said to be socially constructed.', 'journalists select and frame events according to news values and organisational routines.')],
           ['gatekeeping means the audience chooses which stories journalists write.', 'Galtung and Ruge argued that positive, routine events are the most newsworthy.']),
    'scen': ['On the same day, a famous footballer is arrested in {city} and a report on rising child poverty is published; the footballer leads every news bulletin, and the report gets one line.',
             'After a week of front-page stories about knife crime in {city}, a poll finds that crime has become residents’ top concern, although recorded knife crime has fallen.'],
    'views': {k: VM[k] for k in ('Marxism', 'Neo-Marxism', 'Pluralism', 'Interactionism')},
    'ctx': [('how editors select stories for the front page', {'meaning', 'behaviour', 'hidden'}),
            ('which types of stories appear in newspapers', {'media', 'large'})],
    'methods': MEDIA_M,
    'data': [dict(what='news content', pop='stories', rows=['Crime and disasters', 'Celebrity and entertainment', 'Politics and economy', 'Science and development'], cols=('Newspaper X', 'Newspaper Y'), cmp=True, dist=True, nocount=True, n=[400, 500, 600, 800],
                  base=[(25, 35), (15, 25), (25, 35), (5, 10)], delta=[(-10, 0), (-12, -2), (5, 15), (2, 6)], label='share of front-page stories over one year (%)',
                  leads=['A content analysis of {n} front-page stories in two newspapers in {city} produced the results below.', '{person} carried out a content analysis of {n} front pages from two newspapers.'],
                  expl=['negativity and elite persons are strong news values', 'different papers target different audiences', 'science and development stories lack news values such as immediacy'],
                  method='content analysis', claim='news values shape what becomes news',
                  counter='Content analysis shows what is reported, not why; categories may overlap; online news may differ; audience demand may explain differences.')],
    'essays': [('Explain two factors that influence the selection of news.', 'News values (Galtung and Ruge); gatekeeping; news diary; owners and advertisers; journalists’ values; practical constraints.',
                'news is a social construction rather than an objective account of events',
                'Galtung and Ruge; gatekeeping; agenda-setting (McCombs and Shaw); framing; Cohen and Young; GUMG’s evidence of bias.',
                'Professional ethics and fact-checking; pluralists: news reflects audience demand; regulation; citizen journalism provides alternatives; some events are reported by all media.')],
})

g15b = T('Moral panics and folk devils')
build(g15b, {
    'terms': [
        ('moral panic', 'an exaggerated public and media reaction to a group or behaviour seen as a threat to society’s values', 'media outrage about youth gangs'),
        ('folk devil', 'a group defined by the media as a threat to society and blamed for social problems', 'Mods and Rockers in the 1960s'),
        ('deviancy amplification spiral', 'the process by which media reporting increases public concern, social control and the deviance itself', 'more policing leading to more recorded arrests and more stories'),
        ('moral entrepreneur', 'a person or group who campaigns to have a behaviour defined as deviant and controlled', 'a campaign group demanding bans on violent games'),
        ('sensitisation', 'the process by which media coverage makes the public and police more aware of a type of deviance', 'more reports of minor incidents after a moral panic'),
    ],
    'thinkers': [
        ('Cohen', 'media exaggeration of Mods and Rockers created folk devils and a moral panic', 'Interactionism',
         'Cohen’s “Folk Devils and Moral Panics” showed how exaggeration, prediction and symbolisation amplified deviance.',
         'McRobbie and Thornton argue moral panics are now less common because audiences are more media-literate.'),
        ('Hall', 'the 1970s moral panic about mugging diverted attention from a crisis of capitalism', 'Neo-Marxism',
         'Hall argued the media scapegoated young black men, justifying tougher control.',
         'Critics say his evidence for the crisis is limited.'),
        ('McRobbie and Thornton', 'moral panics are harder to sustain in a diverse, fragmented media world', 'Postmodernism',
         'They argued folk devils now have their own media and are defended by pressure groups.',
         'Recent panics about migrants and online harms suggest they continue.'),
        ('Young', 'police and media reaction to drug-takers amplified their deviance', 'Interactionism',
         'Young’s study of hippies showed policing strengthened their deviant identity and drug use.',
         'Hard to know how far deviance would have grown anyway.'),
    ],
    'explain': [
        ('Explain the stages of a moral panic.', 'A group or behaviour is identified as a threat; the media exaggerate and stereotype (folk devils); moral entrepreneurs demand action; authorities respond with tougher control; deviance may be amplified; the panic fades.', '1 mark for each stage up to 4. [4]'),
        ('Explain the difference between the interactionist and neo-Marxist explanations of moral panics.', 'Interactionists see moral panics as labelling and amplification through media reaction (Cohen); neo-Marxists see them as ideological, diverting attention from crises of capitalism (Hall).', '1 mark each view; 1 mark contrast. [3]'),
    ],
    'why': [
        ('function', 'functions', 'that a moral panic may serve', ['reaffirming shared values and boundaries', 'selling newspapers and attracting audiences', 'justifying tougher laws and policing', 'diverting attention from wider problems', 'uniting society against a common threat']),
    ],
    'claims': [
        ('Cohen studied the media reaction to Mods and Rockers.', True, 'His study introduced the concepts of folk devils and moral panics.'),
        ('Moral panics always reduce the deviance they target.', False, 'They can amplify deviance through labelling and stronger control.'),
    ],
    'ar': ([('Moral panics can increase deviance.', 'media labelling and tougher policing may strengthen a deviant identity.'),
            ('McRobbie and Thornton question the moral panic concept.', 'folk devils now have their own media and pressure groups to defend them.')],
           ['folk devils are the journalists who start a moral panic.', 'Hall argued the mugging panic was caused by a real rise in all crime.']),
    'scen': ['After two fights at a music festival near {city}, newspapers report a “wave of youth violence”; police double patrols, and arrests of young people for minor offences rise sharply.',
             'Following a few cases reported abroad, the media in {city} warn of a dangerous online “challenge” among children; schools send letters home, and politicians demand new laws, though no local cases are found.',
             'Newspapers in {city} describe migrants arriving by boat as a “flood” threatening jobs and culture; a campaign group calls for border closures.'],
    'views': {'Interactionism': 'the media label a group as folk devils; exaggeration and tougher control create a deviancy amplification spiral (Cohen, Young).',
              'Neo-Marxism': 'moral panics are ideological: they create scapegoats and divert attention from crises of capitalism, justifying tougher control (Hall).',
              'Functionalism': 'moral panics reaffirm shared values and the boundaries of acceptable behaviour, uniting society against a common threat.',
              'Postmodernism': 'in a fragmented media world, panics are short-lived and contested; folk devils answer back through their own media (McRobbie and Thornton).'},
    'ctx': [('how newspapers report youth crime', {'media', 'large', 'change'}),
            ('how young people labelled as a threat respond to media coverage', {'meaning', 'young', 'sensitive'})],
    'methods': MEDIA_M,
    'data': [dict(what='media coverage and public concern', pop='residents', rows=['Crime stories about young people (% of all crime stories)', 'Residents who say youth violence is a major problem (%)', 'Residents who say they avoid the town centre at night (%)'], cols=('Before the coverage', 'During the coverage'), nocount=True, n=[600, 800, 1000],
                  base=[(15, 25), (20, 30), (10, 18)], delta=[(25, 40), (20, 35), (8, 18)], label='media content and survey results in one city',
                  leads=['A study in {city} combined a content analysis of local newspapers with surveys of {n} residents, before and during a period of intense reporting of youth violence. Police figures showed little change in youth violence over the period.', '{person} studied local newspapers and surveyed {n} residents of {city}, before and during intense reporting of youth violence; recorded youth violence did not change much.'],
                  expl=['the media exaggerate the scale of the problem', 'news values such as negativity drive coverage', 'rising concern without rising offences suggests a moral panic'],
                  method='content analysis', claim='moral panics exaggerate the scale of deviance',
                  counter='Recorded offences may under-report violence; increased policing may later raise figures; articles may reflect real public concern.')],
    'essays': [('Explain two features of a moral panic.', 'Folk devils; exaggeration and distortion; prediction; moral entrepreneurs; disproportionate control response; deviancy amplification.',
                'the concept of moral panic is still useful for understanding the media today',
                'Cohen and Young; recent panics about migrants, online harms, knife crime; deviancy amplification; Hall’s ideological view.',
                'McRobbie and Thornton: fragmented media and media-literate audiences; folk devils fight back; concept is value-laden (who decides a reaction is disproportionate?); some concerns are justified.')],
})
classify(g15b, [
    ('Newspapers in {city} begin describing a group of young skateboarders as “thugs” who “terrorise” shoppers.', 'Creating folk devils', 'the media stereotype a group as a threat.'),
    ('A campaign group in {city} demands new laws to ban skateboarding in the town centre.', 'Moral entrepreneurs demanding action', 'campaigners press for the behaviour to be controlled.'),
    ('Police in {city} launch a crackdown and arrest dozens of skateboarders for minor offences.', 'Increased social control', 'authorities respond with tougher control.'),
    ('Labelled as thugs, the skateboarders in {city} become more defiant and gather in larger groups.', 'Deviancy amplification', 'the reaction increases the deviance it set out to control.'),
], ['Creating folk devils', 'Moral entrepreneurs demanding action', 'Increased social control', 'Deviancy amplification', 'Consumer sovereignty', 'Gatekeeping'], 'Which stage of a moral panic does this describe?', C='C3', D=(1, 2), name='mp_stage')

g15c = T('Media, ideology and the manufacture of consent')
build(g15c, {
    'terms': [
        ('manufacture of consent', 'Herman and Chomsky’s idea that the media produce public support for the policies of powerful elites', 'favourable coverage of a war backed by the government'),
        ('propaganda model', 'Herman and Chomsky’s model of five filters that shape news in the interests of elites', 'ownership, advertising, official sources, flak and ideology'),
        ('ideology', 'a set of ideas and beliefs that justify the interests of a particular group', 'the belief that inequality is natural'),
        ('dominant ideology', 'the ideas of the ruling class that are presented as natural and common sense', 'consumerism promoted through advertising'),
        ('flak', 'negative responses such as complaints and lawsuits used to discipline the media', 'a government attacking a broadcaster for a critical report'),
        ('primary definers', 'powerful sources, such as politicians and police, whose interpretations of events dominate news', 'police statements shaping crime reports'),
    ],
    'thinkers': [
        ('Herman and Chomsky', 'news passes through filters that make it serve elite interests', 'Marxism',
         'Their propaganda model identifies ownership, advertising, reliance on official sources, flak and anti-communism (or fear of an enemy) as filters.',
         'Critics argue it ignores journalists’ independence and critical reporting.'),
        ('Gramsci', 'the ruling class maintains power through hegemony, winning consent through culture and ideas', 'Neo-Marxism',
         'Gramsci argued the media help make ruling-class ideas seem like common sense.',
         'Pluralists argue there is no single dominant ideology.'),
        ('Hall', 'primary definers set the framework for how issues are reported', 'Neo-Marxism',
         'Hall argued reliance on official sources makes the views of the powerful dominate news.',
         'New media allow alternative sources to be heard.'),
    ],
    'explain': [
        ('Explain two filters in Herman and Chomsky’s propaganda model.', 'Ownership by large profit-seeking corporations; reliance on advertising; dependence on official sources; flak from the powerful; ideology of a common enemy.', '2 marks for each explained filter. [4]'),
        ('Explain what is meant by primary definers, using an example.', 'Powerful sources such as politicians, police and business leaders whose accounts are used first and set the frame for a story, e.g. police statements dominating coverage of a protest.', '1 mark meaning; 1 mark development; 1 mark example. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which the media may spread dominant ideology', ['presenting capitalism as natural', 'relying on official sources', 'marginalising radical views', 'promoting consumerism through advertising', 'framing protests negatively']),
    ],
    'claims': [
        ('Herman and Chomsky argued the media challenge elite interests.', False, 'They argued the media manufacture consent for elite interests.'),
        ('Reliance on official sources is one filter in the propaganda model.', True, 'Journalists depend on government and corporate sources.'),
    ],
    'ar': ([('Official sources often dominate news coverage.', 'journalists rely on politicians, police and business for regular information.'),
            ('Neo-Marxists see the media as hegemonic.', 'the media help ruling-class ideas appear as common sense.')],
           ['the propaganda model claims advertising has no influence on news.', 'Gramsci argued the ruling class rules mainly through force.']),
    'scen': ['In the run-up to a military intervention, TV news in {city} relies heavily on government and military spokespeople; anti-war groups are rarely interviewed.',
             'A newspaper in {city} drops an investigation into pollution by a car manufacturer after the company threatens to withdraw its advertising.'],
    'views': {k: VM[k] for k in ('Marxism', 'Neo-Marxism', 'Pluralism', 'Postmodernism')},
    'ctx': [('the sources quoted in news coverage of a war', {'media', 'large'}),
            ('how journalists respond to pressure from advertisers', {'meaning', 'hidden', 'sensitive'})],
    'methods': MEDIA_M,
    'data': [dict(what='news sources', pop='news reports', rows=['Government and military sources', 'Business sources', 'Campaign groups and protesters', 'Members of the public'], cols=('Television news', 'Online-only news sites'), cmp=True, dist=True, nocount=True, n=[300, 400, 500],
                  base=[(40, 50), (15, 22), (8, 14), (12, 20)], delta=[(-20, -10), (-6, 2), (8, 15), (2, 8)], label='share of sources quoted (%)',
                  leads=['A content analysis of {n} news reports about a conflict produced the results below.', '{person} analysed the sources quoted in {n} news reports about a war.'],
                  expl=['television relies on official sources as primary definers', 'online sites give more space to alternative voices', 'elite access shapes the framing of news'],
                  method='content analysis', claim='the news media manufacture consent for elite interests',
                  counter='Online sites may have their own biases; counting sources does not show how they are framed; audiences may reject official views.')],
    'essays': [('Explain two ways in which the media may manufacture consent.', 'Propaganda filters (ownership, advertising, sourcing, flak, ideology); primary definers; framing; marginalising dissent; hegemony.',
                'the media mainly serve to legitimate the interests of powerful groups',
                'Herman and Chomsky; Gramsci and hegemony; Hall’s primary definers; GUMG; examples of war and strike coverage.',
                'Pluralism: diversity and investigative journalism exposing elites (e.g. leaks and scandals); active audiences; new media and citizen journalism; regulation and public service broadcasting.')],
})

CHAPTERS[15] = [g15a, g15b, g15c]


g16a = T('Representations of gender and sexuality')
build(g16a, {
    'terms': [
        ('stereotype', 'a simplified, generalised and often negative image of a group', 'women shown mainly as homemakers in adverts'),
        ('symbolic annihilation', 'Tuchman’s term for the absence, condemnation or trivialisation of women in the media', 'few female experts interviewed on news'),
        ('male gaze', 'Mulvey’s term for the way the camera presents women as sexual objects from a heterosexual male viewpoint', 'camera lingering on a female character’s body'),
        ('beauty myth', 'Wolf’s term for the idealised standards of female beauty promoted by the media', 'airbrushed images of very thin models'),
        ('heteronormativity', 'the assumption that heterosexuality is normal and natural, reflected in media representations', 'gay characters shown only as comic sidekicks'),
        ('hegemonic masculinity', 'the dominant, idealised form of masculinity associated with strength, toughness and heterosexuality', 'action heroes who never show emotion'),
    ],
    'thinkers': [
        ('Tuchman', 'women are symbolically annihilated by the media', 'Liberal feminism',
         'Tuchman argued the media condemn, trivialise or ignore women, presenting them mainly in domestic and sexual roles.',
         'Representations have changed, with more powerful female characters.'),
        ('Mulvey', 'film presents women through a male gaze', 'Radical feminism',
         'Mulvey argued that the camera makes women objects of male pleasure.',
         'Audiences, including women, may read images differently.'),
        ('Wolf', 'the beauty myth puts pressure on women to meet impossible standards', 'Radical feminism',
         'Wolf argued idealised images undermine women’s confidence and keep them focused on appearance.',
         'Some argue women actively choose and enjoy beauty culture.'),
        ('Gauntlett', 'media now offer a wider range of gender identities from which people choose', 'Postmodernism',
         'Gauntlett argued traditional stereotypes have declined and media provide resources for constructing identity.',
         'Content analyses still find many stereotypes.'),
    ],
    'explain': [
        ('Explain two ways in which the media may stereotype women.', 'Symbolic annihilation (absence, trivialisation); domestic and caring roles; sexual objectification (male gaze); beauty myth; focus on appearance rather than achievements.', '2 marks for each explained way. [4]'),
        ('Explain one way in which media representations of masculinity have changed.', 'More emotional, caring or “metrosexual” men; fathers shown doing childcare; criticism of toxic masculinity; but hegemonic masculinity remains in action films and sport.', '1 mark identifying; 2 marks explaining with example. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'for changes in media representations of gender', ['more women working in the media', 'changing gender roles in society', 'pressure from feminist and LGBT campaigns', 'media targeting new markets', 'social media allowing self-representation']),
    ],
    'claims': [
        ('Tuchman used the term symbolic annihilation to describe the absence and trivialisation of women in the media.', True, 'It refers to women being ignored, condemned or trivialised.'),
        ('Mulvey argued the camera presents men as objects for female viewers.', False, 'Mulvey argued the camera presents women through a male gaze.'),
    ],
    'ar': ([('Feminists criticise media representations of women.', 'women are often shown in stereotyped domestic or sexualised roles.'),
            ('Postmodernists argue gender representations are more diverse today.', 'the media offer many identities from which audiences can choose.')],
           ['Wolf argued the media promote realistic and varied images of women’s bodies.', 'heteronormativity means presenting a wide range of sexualities as equally normal.']),
    'scen': ['A content analysis of adverts on television in {city} finds that women appear most often in adverts for cleaning products and cosmetics, while men appear in adverts for cars and banking.',
             'A popular streaming drama made in {city} features a female police chief, a stay-at-home father and a gay couple raising children.',
             'A men’s magazine in {city} features a male action star with a muscular body on almost every cover.'],
    'views': {k: VM[k] for k in ('Liberal feminism', 'Radical feminism', 'Postmodernism', 'Marxism')},
    'ctx': [('the roles given to men and women in television adverts', {'media', 'large'}),
            ('how teenage girls respond to images of models on social media', {'meaning', 'young', 'sensitive'})],
    'methods': MEDIA_M,
    'data': [dict(what='gender in television', pop='characters', rows=['Speaking characters who are women', 'News experts interviewed who are women', 'Directors who are women'], cols=('2005', '2022'), nocount=True, n=[3],
                  base=[(30, 38), (18, 25), (5, 10)], delta=[(3, 10), (5, 15), (3, 10)], label='percentage of women',
                  leads=['A content analysis of television in a country near {city} produced the results below.', 'Industry data and a content analysis of television programmes are shown below.'],
                  expl=['more women working in the media and changing attitudes', 'campaigns for equal representation', 'symbolic annihilation persists because women remain a minority behind the camera'],
                  method='content analysis', claim='media representations of women are improving',
                  counter='Women remain under-represented in all categories; numbers do not show the type of role; streaming and social media may differ.')],
    'essays': [('Explain two ways in which media representations of sexuality may be stereotyped.', 'Heteronormativity; LGBT characters as comic or tragic; invisibility; sexualisation; limited range; recent improvements.',
                'media representations of gender continue to reinforce traditional stereotypes',
                'Tuchman, Mulvey, Wolf; content analyses of adverts and news; beauty myth on social media; hegemonic masculinity.',
                'Gauntlett: more diverse identities; strong female leads; changing masculinities; active audiences; self-representation on social media; postmodern choice.')],
})

g16b = T('Representations of ethnicity, age and social class')
build(g16b, {
    'terms': [
        ('ethnocentrism', 'seeing the world from the viewpoint of one’s own culture and judging others by its standards', 'news focusing only on Western victims of a disaster'),
        ('Orientalism', 'Said’s term for Western representations of Eastern societies as exotic, backward or threatening', 'films showing Arab characters mainly as terrorists'),
        ('tokenism', 'including a small number of minority characters to appear diverse without real representation', 'one minority character in an otherwise white cast'),
        ('ageism', 'stereotyping and discrimination based on age', 'older people shown as confused or a burden'),
        ('underclass stereotype', 'the representation of poor people as lazy, criminal or dependent on welfare', '“benefits” reality TV programmes'),
        ('demonisation', 'presenting a group as evil or a threat to society', 'young people in hoodies described as feral'),
    ],
    'thinkers': [
        ('Said', 'Western media construct the East as the inferior, threatening “Other”', 'Neo-Marxism',
         'Said’s Orientalism showed how Western culture represented Arab and Asian societies stereotypically.',
         'Representations of minorities have become more varied.'),
        ('Van Dijk', 'news presents ethnic minorities mainly as problems or threats', 'Neo-Marxism',
         'Van Dijk’s content analysis found minorities linked to crime, conflict and immigration problems.',
         'Minority-owned and online media provide alternative representations.'),
        ('Jones', 'the media demonise the working class as “chavs”', 'Marxism',
         'Jones argued the media mock the working class, justifying inequality.',
         'Some programmes present working-class life sympathetically.'),
        ('Newman', 'media representations of the working class are rare and negative', 'Marxism',
         'Newman argued news focuses on the rich and portrays the poor as undeserving.',
         'Pluralists argue audience demand determines content.'),
    ],
    'explain': [
        ('Explain two ways in which the media may represent ethnic minorities stereotypically.', 'As a threat (crime, terrorism); as a problem (immigration); exotic or Orientalist images; tokenism; absence (symbolic annihilation); limited roles.', '2 marks for each explained way. [4]'),
        ('Explain two ways in which the media may represent young people negatively.', 'As a threat (crime, gangs, antisocial behaviour); moral panics; as lazy or irresponsible; as obsessed with technology; focus on problems rather than achievements.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('stereotype', 'stereotypes', 'of older people in the media', ['frail or dependent', 'confused or forgetful', 'grumpy or out of touch', 'a burden on society', 'absent from adverts and leading roles']),
    ],
    'claims': [
        ('Said used the term Orientalism to describe positive Western images of Eastern societies.', False, 'Orientalism describes stereotyped Western images of the East as exotic, backward or threatening.'),
        ('Some reality TV programmes present poor people as lazy or undeserving.', True, 'This reflects the underclass stereotype.'),
    ],
    'ar': ([('Ethnic minorities are often linked to crime in the news.', 'news values such as negativity and threat shape how minorities are reported.'),
            ('Older people are often absent from adverts.', 'advertisers target younger consumers with more spending power.')],
           ['tokenism means giving minority groups equal representation in the media.', 'Van Dijk found that news usually presents minorities as successful.']),
    'scen': ['A series of newspaper stories in {city} about crime uses photographs of young black men, while stories about business success use photographs of white men in suits.',
             'A popular reality TV show in {city} follows families living on benefits, using music and captions that invite viewers to laugh at them.',
             'A soap opera set in {city} introduces a 75-year-old character who runs a business, uses social media and starts a new relationship.'],
    'views': {k: VM[k] for k in ('Marxism', 'Neo-Marxism', 'Pluralism', 'Postmodernism', 'Interactionism')},
    'ctx': [('how minority ethnic groups are represented in television drama', {'media', 'large'}),
            ('how older people feel about the way the media represent them', {'meaning', 'sensitive'})],
    'methods': MEDIA_M,
    'data': [dict(what='representation of minority ethnic groups', pop='characters', rows=['Leading roles', 'Criminal roles', 'News experts'], cols=('2010', '2022'), nocount=True, n=[3],
                  base=[(6, 10), (25, 32), (5, 9)], delta=[(3, 8), (-10, -3), (2, 7)], label='percentage of characters in each type of role who are from minority ethnic groups',
                  leads=['A content analysis of prime-time television in a country where 14% of the population are from minority ethnic groups produced the results below.', '{person} carried out a content analysis of TV drama and news in a country where 14% of people are from minority ethnic groups.'],
                  expl=['minority groups are under-represented in leading and expert roles compared with 14% of the population', 'they are over-represented in criminal roles', 'diversity policies have brought some improvement'],
                  method='content analysis', claim='the media stereotype minority ethnic groups',
                  counter='Content analysis cannot show how audiences interpret roles; different channels may differ; representation is improving over time.')],
    'essays': [('Explain two ways in which the media may represent social class.', 'Underclass stereotypes (Jones); middle-class norms dominate; celebration of wealth and consumerism; working class shown as comic or criminal; absence of the working class from news.',
                'media representations of social groups are becoming more positive and diverse',
                'More diverse casts; minority-owned and online media; positive older characters; working-class dramas; postmodern diversity.',
                'Van Dijk, Said, Jones: persistent stereotypes; tokenism; moral panics about youth; ageism; Marxist ideology; under-representation behind the camera.')],
})

g16c = T('Representations of disability and stereotyping')
build(g16c, {
    'terms': [
        ('medical model of disability', 'the view that disability is a problem located in the individual’s body that needs to be cured or treated', 'news focusing on a person’s condition'),
        ('social model of disability', 'the view that people are disabled by barriers and attitudes in society rather than by their impairments', 'a lack of ramps preventing wheelchair users from entering buildings'),
        ('supercrip stereotype', 'the representation of disabled people as heroic for overcoming their impairment', 'news praising a disabled athlete as “inspirational” for ordinary activities'),
        ('pitiable stereotype', 'the representation of disabled people as objects of pity and charity', 'charity adverts showing helpless disabled children'),
        ('under-representation', 'appearing less often in the media than in the population', 'few disabled characters on prime-time television'),
    ],
    'thinkers': [
        ('Barnes', 'the media use a limited set of negative stereotypes of disabled people', 'Interactionism',
         'Barnes identified stereotypes such as pitiable, sinister, supercrip, burden and incapable of normal relationships.',
         'Representations are improving with more disabled actors and presenters.'),
        ('Shakespeare', 'disabled people are often used in film as metaphors for evil or tragedy', 'Interactionism',
         'Shakespeare argued disability is used as a plot device rather than shown as ordinary life.',
         'More recent dramas include disabled characters in everyday roles.'),
        ('Oliver', 'disability is socially created by barriers in society (the social model)', 'Marxism',
         'Oliver argued capitalism excludes people who cannot work in standard ways, creating disability.',
         'Critics argue the social model ignores the real pain of some impairments.'),
    ],
    'explain': [
        ('Explain the difference between the medical and social models of disability.', 'Medical model: disability is an individual problem of the body to be treated; social model: people are disabled by social barriers and attitudes, such as inaccessible buildings and discrimination.', '1 mark each model; 1 mark contrast. [3]'),
        ('Explain two stereotypes of disabled people identified in media research.', 'Pitiable and pathetic; sinister or evil (villains); supercrip; burden; object of curiosity; incapable of relationships (Barnes).', '2 marks for each explained stereotype. [4]'),
    ],
    'why': [
        ('effect', 'effects', 'of negative media representations of disabled people', ['reinforcing prejudice', 'lowering self-esteem', 'discrimination in employment', 'social exclusion', 'shaping policy as charity rather than rights']),
    ],
    'claims': [
        ('The social model sees disability as caused by social barriers.', True, 'It focuses on barriers and attitudes rather than individual impairment.'),
        ('Disabled people appear in the media in proportion to their numbers in the population.', False, 'Research finds they are under-represented.'),
    ],
    'ar': ([('Disabled people are often shown as objects of pity.', 'charity campaigns use images of helplessness to raise money.'),
            ('Paralympic coverage may challenge stereotypes.', 'it presents disabled people as skilled and competitive athletes.')],
           ['the supercrip stereotype shows disabled people as ordinary and unremarkable.', 'the medical model argues that society creates disability.']),
    'scen': ['A charity advert in {city} shows a disabled child alone in a dark room with sad music and the words “Without you, she has no future.”',
             'A new TV series made in {city} features a wheelchair user as the lead detective, played by a disabled actor; her disability is rarely mentioned in the plot.'],
    'views': {'Interactionism': 'media labels and stereotypes of disabled people shape how others see them and how they see themselves (Barnes).',
              'Marxism': 'disabled people are marginalised because capitalism values people mainly as productive workers (Oliver).',
              'Pluralism': 'media content reflects audience demand and commercial pressures (for example, images that raise money for charities); as attitudes change and disabled people gain a voice, representations become more diverse.',
              'Postmodernism': 'media offer a growing range of images, and disabled people use social media to represent themselves.'},
    'ctx': [('how disabled characters are represented in films', {'media', 'large'}),
            ('how disabled people feel about their representation in the media', {'meaning', 'sensitive'})],
    'methods': MEDIA_M,
    'data': [dict(what='disability on television', pop='characters', rows=['Disabled characters', 'Disabled characters played by disabled actors', 'Disabled presenters'], cols=('2010', '2022'), nocount=True, n=[3],
                  base=[(2, 5), (1, 3), (1, 2)], delta=[(2, 5), (1, 3), (1, 4)], label='percentage of all characters or presenters',
                  leads=['A content analysis of prime-time television in a country where about 18% of people are disabled produced the results below.', 'The table shows a content analysis of television in a country where around 18% of the population are disabled.'],
                  expl=['campaigns by disabled people’s organisations', 'broadcasters’ diversity targets', 'disabled people remain greatly under-represented compared with 18% of the population'],
                  method='content analysis', claim='representation of disabled people on television has improved',
                  counter='Figures remain far below 18% of the population; numbers do not show whether roles are stereotyped; online media are not included.')],
    'essays': [('Explain two stereotypes of disabled people in the media.', 'Pitiable; sinister; supercrip; burden; incapable of relationships; comic figure; medical-model focus.',
                'media representations of disabled people reinforce negative stereotypes',
                'Barnes’s stereotypes; under-representation; charity imagery; disability as plot device (Shakespeare); medical model framing.',
                'Paralympics coverage; disabled actors and presenters; social model campaigns; social media self-representation; improving but uneven.')],
})

CHAPTERS[16] = [g16a, g16b, g16c]


g17a = T('Direct effects models: hypodermic syringe and the debate on media violence')
build(g17a, {
    'terms': [
        ('hypodermic syringe model', 'the view that media messages are “injected” into a passive audience and have direct, immediate effects', 'viewers copying violence after watching a film'),
        ('imitation', 'copying behaviour seen in the media', 'children copying fighting moves from cartoons'),
        ('desensitisation', 'the process by which repeated exposure to media violence makes people less shocked by real violence', 'viewers showing little reaction to images of war'),
        ('copycat violence', 'violent acts that copy events seen in the media', 'a crime that copies a scene in a film'),
        ('catharsis', 'the idea that watching violence allows people to release aggressive feelings harmlessly', 'a viewer feeling calmer after an action film'),
        ('sensitisation', 'the idea that media violence can make audiences more aware of the harm violence causes', 'a war film making viewers more opposed to war'),
    ],
    'thinkers': [
        ('Bandura', 'children imitate aggressive behaviour they see modelled on screen', 'Positivism',
         'Bandura’s Bobo doll experiments found children who watched an adult attack a doll were more likely to copy the behaviour.',
         'The laboratory setting was artificial and the doll was designed to be hit.'),
        ('Newson', 'violent videos may have harmful effects on vulnerable children', 'Positivism',
         'Newson’s report after a high-profile child murder argued violent films should be restricted.',
         'There was no clear evidence that the offenders had watched the film blamed in the press.'),
        ('Gauntlett', 'decades of effects research have failed to prove that media violence causes real violence', 'Interactionism',
         'Gauntlett criticised effects research for treating audiences as passive and using artificial methods.',
         'Some longitudinal studies find links between viewing and aggression.'),
    ],
    'explain': [
        ('Explain two criticisms of the hypodermic syringe model.', 'Audiences are active, not passive; people interpret messages differently; artificial laboratory studies lack validity; it ignores social context (family, peers); correlation is not causation.', '2 marks for each explained criticism. [4]'),
        ('Explain the difference between desensitisation and catharsis.', 'Desensitisation: repeated exposure makes people less shocked by violence and more accepting of it; catharsis: viewing violence releases aggression harmlessly, reducing real violence.', '1 mark each; 1 mark contrast. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of laboratory experiments on media violence', ['the setting is artificial', 'short-term effects only', 'demand characteristics', 'ethical problems of exposing children to violence', 'the definition of violence is narrow']),
    ],
    'claims': [
        ('The hypodermic syringe model treats audiences as active interpreters of media.', False, 'It treats audiences as passive and directly affected.'),
        ('Bandura’s Bobo doll studies used laboratory experiments.', True, 'Children were observed in a controlled setting after watching a model.'),
    ],
    'ar': ([('Bandura’s findings are said to lack ecological validity.', 'they took place in an artificial laboratory setting.'),
            ('The hypodermic syringe model is often linked to moral panics.', 'it suggests media violence directly causes real violence.')],
           ['the catharsis model claims media violence makes viewers more aggressive.', 'Gauntlett argued effects research has proved media violence causes crime.']),
    'scen': ['After two teenagers in {city} are convicted of an assault, newspapers claim they were copying a violent video game, and politicians call for the game to be banned.',
             'A researcher in {city} shows one group of children a violent cartoon and another a calm cartoon, then observes how they play with toys for 20 minutes.'],
    'views': {'Positivism': 'media effects can be measured scientifically through experiments and correlations that show cause and effect (Bandura).',
              'Interactionism': 'audiences interpret media actively; effects depend on meanings and context, and moral panics exaggerate media effects (Gauntlett).',
              'Marxism': 'blaming the media diverts attention from structural causes of violence such as poverty and inequality.',
              'Postmodernism': 'audiences are media-literate and fragmented; there is no single effect, as people use media in many ways.'},
    'ctx': [('the effects of violent video games on children', {'behaviour', 'young', 'sensitive'}),
            ('how much violence is shown on children’s television', {'media', 'large'})],
    'methods': MEDIA_M,
    'data': [dict(what='media violence and aggression', pop='children', rows=['Hit the toy at least once', 'Played without hitting the toy'], cols=('Violent cartoon group', 'Non-violent cartoon group'), cmp=True, complement=True, nocount=True, n=[40, 60, 80],
                  base=[(55, 70), (30, 45)], delta=[(-40, -15), (15, 40)], label='children in each group (%)',
                  leads=['In a laboratory experiment in {city}, {n} children were split into two groups and observed after watching a cartoon.', '{person} carried out an experiment with {n} children aged 5-7, observing their play after a cartoon.'],
                  expl=['children may imitate behaviour they see on screen (Bandura)', 'the violent cartoon may have excited children', 'the experiment controls other variables'],
                  method='laboratory experiment', claim='media violence causes aggressive behaviour',
                  counter='Hitting a toy is not real violence; artificial setting; short-term effect only; small sample; demand characteristics; ethical concerns.')],
    'essays': [('Explain two arguments that the media cause violence.', 'Imitation (Bandura); desensitisation; copycat crimes; moral panics citing cases; longitudinal correlations.',
                'the media have a direct effect on violent behaviour',
                'Bandura’s experiments; desensitisation; copycat cases; Newson; correlational studies.',
                'Gauntlett’s critique; artificial methods; active audiences; catharsis and sensitisation; social causes of violence; moral panics exaggerate effects.')],
})

g17b = T('Limited effects models: two-step flow, uses and gratifications')
build(g17b, {
    'terms': [
        ('two-step flow model', 'the view that media messages reach people through opinion leaders who interpret them for others', 'a respected friend persuading others how to vote'),
        ('opinion leader', 'a person whose views influence how others interpret media messages', 'an influencer or community elder'),
        ('uses and gratifications model', 'the view that audiences actively use media to satisfy their own needs', 'watching a comedy to relax after work'),
        ('selective filter model', 'the view that audiences filter media through selective exposure, perception and retention', 'remembering only news that confirms one’s views'),
        ('selective exposure', 'choosing only media that fit one’s existing views and interests', 'reading only newspapers that support one’s party'),
        ('personal identity need', 'using media to compare oneself with others and form one’s identity', 'teenagers comparing themselves with characters in a drama'),
    ],
    'thinkers': [
        ('Katz and Lazarsfeld', 'media messages are filtered by opinion leaders through a two-step flow', 'Pluralism',
         'Their research on voting found personal influence was more important than direct media influence.',
         'Today, social media allow messages to reach people directly and also create new opinion leaders.'),
        ('Blumler and McQuail', 'people use the media to satisfy needs such as diversion, personal relationships, identity and surveillance', 'Pluralism',
         'Their uses and gratifications model sees the audience as active and selective.',
         'It assumes needs are freely chosen rather than shaped by the media.'),
        ('Klapper', 'audiences filter media through selective exposure, perception and retention', 'Pluralism',
         'Klapper argued the media mainly reinforce existing views rather than change them.',
         'Repeated messages over time may still shape views.'),
    ],
    'explain': [
        ('Explain the role of opinion leaders in the two-step flow model.', 'Opinion leaders consume media and interpret messages; they pass on their interpretation to others in their social network, so media influence is indirect and filtered through personal relationships.', '1 mark meaning; 1 mark process; 1 mark example. [3]'),
        ('Explain two needs that audiences satisfy through the media, according to the uses and gratifications model.', 'Diversion (escape and entertainment); personal relationships (company, shared topics); personal identity (comparing oneself); surveillance (information about the world).', '2 marks for each explained need. [4]'),
    ],
    'why': [
        ('need', 'needs', 'that audiences may meet through the media (Blumler and McQuail)', ['diversion and escape', 'personal relationships', 'personal identity', 'surveillance and information']),
    ],
    'claims': [
        ('The uses and gratifications model treats audiences as passive.', False, 'It sees audiences as active users of media.'),
        ('Klapper argued the media mainly reinforce existing attitudes.', True, 'Selective exposure, perception and retention filter messages.'),
    ],
    'ar': ([('Media messages may not change people’s views.', 'audiences select and interpret media to fit what they already believe.'),
            ('Opinion leaders influence others.', 'they interpret media messages and pass them on through personal networks.')],
           ['the two-step flow model claims messages affect everyone directly.', 'selective retention means remembering all media messages equally.']),
    'scen': ['During an election campaign in {city}, a respected local shopkeeper discusses the TV debates with customers, and many of them later vote the way he recommended.',
             'Interviews with retired people in {city} find that they watch daily soap operas because the characters feel like friends and give them something to talk about with neighbours.'],
    'views': {'Pluralism': 'audiences are active and diverse; they choose and filter media to meet their needs, so media power is limited (Blumler and McQuail, Katz and Lazarsfeld).',
              'Marxism': 'audience needs are shaped by capitalist media and advertising; “choice” takes place within the limits of dominant ideology.',
              'Interactionism': 'media meanings are negotiated in social interaction, so personal networks and opinion leaders shape interpretations.',
              'Postmodernism': 'audiences use media to construct identities in a media-saturated world with endless choice.'},
    'ctx': [('why people watch reality television', {'meaning', 'large'}),
            ('how friends influence each other’s views of news stories', {'meaning', 'behaviour'})],
    'methods': MEDIA_M,
    'data': [dict(what='reasons for using social media', pop='young people', rows=['Entertainment and escape', 'Keeping in touch with friends', 'Finding news and information', 'Comparing myself with others'], cols=('Aged 13-15', 'Aged 16-18'), cmp=True, nocount=True,
                  base=[(65, 80), (75, 88), (20, 35), (25, 40)], delta=[(-10, 5), (-8, 5), (10, 25), (-10, 5)], label='young people giving each reason (%)',
                  leads=['A survey of {n} young people in {city} asked why they use social media; respondents could give more than one reason.', '{person} surveyed {n} young people about why they use social media (more than one answer allowed).'],
                  expl=['audiences use media to meet needs such as diversion, relationships, identity and surveillance', 'older teenagers use media more for information', 'needs vary with age and life stage'],
                  method='questionnaire', claim='audiences actively use media to meet their own needs',
                  counter='Self-reported reasons may be inaccurate; closed categories limit answers; needs may themselves be shaped by media and advertising.')],
    'essays': [('Explain two features of the uses and gratifications model.', 'Active audience; needs (diversion, relationships, identity, surveillance); needs vary by age, gender, class; selective use.',
                'audiences are active rather than passive in their use of the media',
                'Uses and gratifications (Blumler and McQuail); two-step flow (Katz and Lazarsfeld); selective filter (Klapper); reception analysis (Morley); social media participation.',
                'Hypodermic syringe and cultural effects: repeated messages shape views over time; needs shaped by media; algorithms limit choice; Marxists: hegemony; moral panics show media power.')],
})

g17c = T('Cultural effects and reception analysis: active audiences')
build(g17c, {
    'terms': [
        ('cultural effects model', 'the view that repeated media messages over long periods gradually shape audiences’ values and beliefs', 'constant images of thin models shaping ideas of beauty'),
        ('reception analysis', 'the view that audiences interpret the same media text in different ways depending on their social position', 'workers and managers reading a strike report differently'),
        ('preferred reading', 'the interpretation of a text that its producers intend audiences to accept', 'a news report framing protesters as troublemakers'),
        ('negotiated reading', 'an interpretation that accepts parts of the preferred reading but adapts it', 'agreeing a strike is disruptive but sympathising with workers'),
        ('oppositional reading', 'an interpretation that rejects the preferred reading', 'seeing a pro-war report as propaganda'),
        ('drip-drip effect', 'the gradual influence of repeated media messages over time', 'repeated stereotypes slowly shaping attitudes'),
    ],
    'thinkers': [
        ('Hall', 'media texts are encoded with preferred readings but can be decoded in dominant, negotiated or oppositional ways', 'Neo-Marxism',
         'Hall’s encoding/decoding model links readings to audiences’ social positions.',
         'Critics argue it is hard to measure how audiences decode texts.'),
        ('Morley', 'different social groups interpret the same programme differently', 'Interactionism',
         'Morley’s Nationwide study found managers, students and trade unionists read the same news programme differently.',
         'Group interviews may lead people to give socially desirable answers.'),
        ('Philo', 'repeated media coverage shapes audiences’ understanding of events', 'Cultural effects theory',
         'Philo (Glasgow University Media Group) found audiences could reproduce news-style accounts of strikes and accepted many of their assumptions.',
         'Some audiences rejected the media account based on personal experience.'),
    ],
    'explain': [
        ('Explain the three types of reading identified in Hall’s encoding/decoding model.', 'Dominant (accepting the preferred reading); negotiated (accepting some of it but adapting it to one’s own situation); oppositional (rejecting the preferred reading).', '1 mark for each reading explained. [3]'),
        ('Explain the cultural effects model, using an example.', 'Media effects are long-term and cumulative: repeated messages (drip-drip) gradually shape values and attitudes, e.g. constant stereotyped images of minorities or women shaping public views.', '1 mark long-term; 1 mark repetition; 1 mark example. [3]'),
    ],
    'why': [
        ('factor', 'factors', 'that may influence how an audience interprets a media text', ['social class', 'gender', 'ethnicity', 'age', 'personal experience of the issue', 'political views', 'the group they watch with']),
    ],
    'claims': [
        ('Morley found all groups interpreted the Nationwide programme in the same way.', False, 'Different groups made dominant, negotiated or oppositional readings.'),
        ('The cultural effects model emphasises long-term, repeated media messages.', True, 'It focuses on the cumulative drip-drip effect.'),
    ],
    'ar': ([('Audiences may interpret the same programme differently.', 'their social position and experience shape how they decode media texts.'),
            ('The cultural effects model sees media power as long-term.', 'repeated messages gradually shape audiences’ values.')],
           ['an oppositional reading accepts the preferred reading of a text.', 'Morley studied audiences using a laboratory experiment with children.']),
    'scen': ['Three groups in {city} watch the same news report on a nurses’ strike: hospital managers say the strike is irresponsible, nurses say it is justified, and students accept that pay is low but think the strike is harmful.',
             'A study in {city} finds that people who watch the most television news overestimate the proportion of crimes committed by young people.'],
    'views': {'Neo-Marxism': 'media texts encode a preferred, hegemonic reading, but audiences’ class positions lead to dominant, negotiated or oppositional readings (Hall).',
              'Cultural effects theory': 'repeated media messages gradually shape audiences’ attitudes over time, reinforcing dominant ideas (Philo).',
              'Interactionism': 'audiences actively make meanings from media in social contexts; interpretations differ by group (Morley).',
              'Pluralism': 'audiences are diverse and active, so media cannot impose any single meaning on them.'},
    'ctx': [('how different social groups interpret a TV news report', {'meaning', 'large'}),
            ('long-term effects of television viewing on attitudes to crime', {'change', 'large', 'young'})],
    'methods': MEDIA_M,
    'source': [dict(text='A researcher in {city} showed a 20-minute news programme about a factory closure to five groups (managers, trade unionists, students, unemployed people and retired people), then held group discussions. Managers mostly agreed with the programme; trade unionists rejected its framing; students accepted parts of it but criticised others.',
                    method='case study', about='audience readings of the news', finds=['managers mostly accepted the programme’s view', 'trade unionists rejected its framing', 'students accepted some parts and rejected others'],
                    persp='Neo-Marxism', pview='The findings support Hall and Morley: audiences decode the same text through dominant (managers), oppositional (trade unionists) and negotiated (students) readings depending on their social position.',
                    claim='audiences are active interpreters of media messages', pro='The source shows groups decoding the programme differently, as reception analysis and Morley’s Nationwide study suggest.',
                    con='Cultural effects theorists (Philo) show repeated messages still shape understanding; group discussions may produce socially desirable or group-led answers; one programme and small groups may not be typical.', flags={'meaning', 'media'})],
    'essays': [('Explain two differences between the cultural effects model and the uses and gratifications model.', 'Cultural effects: long-term, cumulative, media shape values; uses and gratifications: audiences active, choose media to meet needs; power lies with media vs. audiences.',
                'reception analysis provides the best explanation of the relationship between the media and audiences',
                'Hall’s encoding/decoding; Morley’s Nationwide study; active audiences; social position shapes readings; supported by postmodernist and interactionist views.',
                'Cultural effects (Philo, GUMG): long-term influence; hypodermic syringe and moral panics; uses and gratifications offers an alternative active view; readings are hard to measure.')],
})

CHAPTERS[17] = [g17a, g17b, g17c]


VNM = {
    'Postmodernism': 'new media create a media-saturated, fragmented world of choice in which people construct identities and reality blurs with representation (Baudrillard).',
    'Pluralism': 'new media increase diversity and access: anyone can publish, so power is spread more widely and audiences have more choice (Jenkins, Shirky).',
    'Marxism': 'new media are owned by a few huge corporations that profit from users’ data and attention; they extend capitalist control and consumerism (Fuchs).',
    'Neo-Marxism': 'new media spread dominant ideology in new forms, though they also give some space for counter-hegemonic voices.',
    'Interactionism': 'people use new media to present and negotiate identities and relationships; meanings are created in online interaction.',
    'Radical feminism': 'new media reproduce patriarchy through online harassment, sexualised images and male-dominated technology industries.',
}

g18a = T('Defining new media: digital, interactive and networked media')
build(g18a, {
    'terms': [
        ('new media', 'screen-based, digital media that are interactive, networked and allow users to create and share content', 'social media, streaming and online games'),
        ('digitalisation', 'the conversion of all forms of information into digital code that can be stored and shared', 'music and films stored as digital files'),
        ('interactivity', 'the ability of users to respond to and shape media content', 'commenting, voting and playing online games'),
        ('convergence', 'the merging of different media and technologies into single devices or platforms', 'a smartphone used as phone, camera, TV and computer'),
        ('user-generated content', 'media content created by ordinary users rather than professional organisations', 'videos uploaded by individuals'),
        ('prosumer', 'a person who both produces and consumes media content', 'a teenager who watches videos and makes her own'),
    ],
    'thinkers': [
        ('Jenkins', 'convergence culture allows audiences to participate in creating and circulating media content', 'Pluralism',
         'Jenkins argued new media create a participatory culture in which consumers become producers.',
         'Corporations still control the main platforms.'),
        ('Boyle', 'new media are characterised by technological convergence and digitalisation', 'Pluralism',
         'Boyle argued the distinction between media producers and consumers is breaking down.',
         'Access to new media is unequal (digital divide).'),
        ('Lister', 'new media are digital, interactive, hypertextual, dispersed and virtual', 'Postmodernism',
         'Lister and colleagues identified key features distinguishing new media from old.',
         'Some argue the differences from old media are exaggerated.'),
    ],
    'explain': [
        ('Explain two features of new media, using examples.', 'Digital (information stored as code); interactive (users respond and shape content); networked (connected globally); convergent (one device for many media); user-generated content.', '2 marks for each explained feature with example. [4]'),
        ('Explain what is meant by technological convergence, using an example.', 'The merging of separate media technologies into a single digital device or platform, e.g. a smartphone that combines phone, camera, TV, radio and internet.', '1 mark meaning; 1 mark development; 1 mark example. [3]'),
    ],
    'why': [
        ('difference', 'differences', 'between new media and traditional media', ['new media are interactive', 'users can create content', 'content is available on demand', 'global networks connect users instantly', 'one device performs many functions']),
    ],
    'claims': [
        ('New media only allow one-way communication from producers to audiences.', False, 'New media are interactive and allow users to create and share content.'),
        ('A prosumer both produces and consumes media content.', True, 'User-generated content blurs the line between producers and audiences.'),
    ],
    'ar': ([('New media are described as interactive.', 'users can respond to, shape and create content.'),
            ('Convergence has changed media use.', 'one digital device can now provide many different media.')],
           ['user-generated content is produced only by large media corporations.', 'digitalisation means converting digital files back into print.']),
    'scen': ['{woman}, aged 16, in {city} watches TV series on her phone, posts her own dance videos, comments on friends’ posts and plays an online game with players in four countries.',
             'A local newspaper in {city} closes its print edition and moves online, where readers comment on stories and send in their own photos and videos.'],
    'views': VNM,
    'ctx': [('how young people use smartphones', {'behaviour', 'young', 'meaning'}),
            ('the amount of user-generated content on news websites', {'media', 'large', 'change'})],
    'methods': MEDIA_M,
    'data': [dict(what='new media use', pop='adults', rows=['Watched TV on demand', 'Posted their own content online', 'Listened to music by streaming'], cols=('Aged 16-24', 'Aged 65 and over'), cmp=True, nocount=True,
                  base=[(75, 90), (55, 70), (80, 92)], delta=[(-50, -30), (-50, -35), (-55, -35)], label='adults doing each activity in the last week (%)',
                  leads=['A national survey of {n} adults produced the results below.', '{person} analysed a survey of {n} adults in a country near {city}.'],
                  expl=['young people are “digital natives” who grew up with new media', 'older people may lack access or skills (digital divide)', 'convergence makes on-demand media easy for regular users'],
                  method='questionnaire', claim='new media use is shaped by age',
                  counter='Older people’s use is growing quickly; survey may not include people in care homes; frequency does not show the meaning of use.')],
    'essays': [('Explain two ways in which new media differ from traditional media.', 'Interactivity; digitalisation; convergence; user-generated content; networked and global; on demand.',
                'new media have transformed the relationship between media producers and audiences',
                'Prosumers and participatory culture (Jenkins); citizen journalism; user-generated content; convergence; global networks.',
                'Corporations control platforms and data (Fuchs); most content still produced professionally; digital divide; algorithms shape what users see; continuity with old media.')],
})

g18b = T('Optimistic and pessimistic views of new media')
build(g18b, {
    'terms': [
        ('neophiliacs', 'optimists who believe new media bring positive changes, such as more choice and democracy', 'claims that the internet empowers ordinary people'),
        ('cultural pessimists', 'those who believe new media have harmful effects on culture, relationships and democracy', 'claims that social media damage mental health'),
        ('digital divide', 'unequal access to new media between and within countries', 'rural and poorer households lacking broadband'),
        ('echo chamber', 'an online environment in which people encounter only views that reinforce their own', 'a news feed showing only one political view'),
        ('filter bubble', 'Pariser’s term for the personalised information that algorithms show users, limiting exposure to other views', 'search results tailored to past clicks'),
        ('cyber-utopianism', 'the belief that the internet will inevitably bring freedom and democracy', 'claims that social media will topple dictators'),
    ],
    'thinkers': [
        ('Shirky', 'new media allow people to organise collectively without traditional institutions', 'Pluralism',
         'Shirky argued the internet lowers the cost of cooperation, empowering ordinary people.',
         'Morozov argues authoritarian states also use the internet to control populations.'),
        ('Morozov', 'the internet can strengthen authoritarian control through surveillance and propaganda', 'Neo-Marxism',
         'Morozov criticised “cyber-utopianism”, showing how governments use social media to track dissidents.',
         'Online activism has helped some protest movements.'),
        ('Turkle', 'digital technology can leave people “alone together”, weakening face-to-face relationships', 'Interactionism',
         'Turkle argued constant connection reduces the depth of conversation and intimacy.',
         'Others find online contact strengthens existing relationships.'),
        ('Fuchs', 'social media corporations exploit users’ unpaid labour and data for profit', 'Marxism',
         'Fuchs argued users are the product sold to advertisers.',
         'Users gain free services and choose to participate.'),
    ],
    'explain': [
        ('Explain the difference between neophiliac and cultural pessimist views of new media.', 'Neophiliacs see new media as positive: more choice, participation, democracy and information; cultural pessimists see harm: dumbing down, surveillance, echo chambers, damaged relationships, corporate control.', '1 mark each view; 1 mark contrast. [3]'),
        ('Explain two pessimistic arguments about the effects of new media.', 'Echo chambers and filter bubbles; misinformation; cyberbullying and mental health; surveillance and loss of privacy; corporate control of data (Fuchs); digital divide; weakened relationships (Turkle).', '2 marks for each explained argument. [4]'),
    ],
    'why': [
        ('benefit', 'benefits', 'of new media claimed by neophiliacs', ['more choice of content', 'easy access to information', 'greater participation in politics', 'global communication', 'user-generated creativity', 'citizen journalism']),
    ],
    'claims': [
        ('Cultural pessimists argue new media have only positive effects.', False, 'They stress the harmful effects of new media.'),
        ('Filter bubbles may limit people’s exposure to different views.', True, 'Algorithms personalise content based on past behaviour.'),
    ],
    'ar': ([('Some sociologists worry about echo chambers.', 'people may only encounter views that reinforce their existing beliefs.'),
            ('Neophiliacs see new media as democratising.', 'anyone can publish content and take part in debate.')],
           ['Morozov argued the internet always weakens authoritarian governments.', 'Turkle argued digital technology always strengthens face-to-face relationships.']),
    'scen': ['A protest movement in {city} uses social media to organise rallies; within weeks, the government blocks several platforms and arrests activists identified from their posts.',
             'A survey in {city} finds that teenagers who spend more than five hours a day on social media are more likely to report anxiety, but also that most say social media help them stay close to friends.'],
    'views': VNM,
    'ctx': [('how social media affect young people’s friendships', {'meaning', 'young', 'sensitive'}),
            ('the spread of false news stories on social media', {'media', 'large', 'change'})],
    'methods': MEDIA_M,
    'data': [dict(what='attitudes to social media', pop='adults', rows=['Social media make it easier to take part in politics', 'Social media spread false information', 'Social media have made my relationships stronger'], cols=('2015', '2023'), nocount=True,
                  base=[(50, 60), (45, 55), (35, 45)], delta=[(-15, -5), (15, 25), (-8, 2)], label='adults who agree with each statement (%)',
                  leads=['Two surveys, each of {n} adults in {city}, asked about social media.', '{person} compared surveys of {n} adults in {city} about social media.'],
                  expl=['experience of misinformation has increased pessimism', 'growing concerns about echo chambers and surveillance', 'mixed views reflect both neophiliac and pessimist arguments'],
                  method='questionnaire', claim='people have become more pessimistic about new media',
                  counter='Attitudes may reflect media coverage rather than experience; agreement scales are crude; many still see benefits.')],
    'essays': [('Explain two arguments of neophiliacs about new media.', 'Choice and diversity; participation and democracy (Shirky); citizen journalism; global communities; access to information; creativity.',
                'new media have had a mainly negative effect on society',
                'Pessimists: echo chambers, misinformation, surveillance (Morozov), exploitation of data (Fuchs), weakened relationships (Turkle), cyberbullying, digital divide.',
                'Neophiliacs: democracy and participation (Shirky, Jenkins); access to information; global communities; support networks; effects depend on how people use media.')],
})

g18c = T('Social media, citizen journalism and digital surveillance')
build(g18c, {
    'terms': [
        ('citizen journalism', 'the collection and reporting of news by members of the public, often using phones and social media', 'a bystander filming police actions and posting them online'),
        ('digital surveillance', 'the monitoring of people’s online activity and data by states or corporations', 'governments monitoring social media for dissent'),
        ('surveillance capitalism', 'Zuboff’s term for an economic system based on collecting and selling personal data to predict and shape behaviour', 'apps tracking location to target adverts'),
        ('synopticon', 'the situation in which the many watch the few, for example the public watching the powerful through media', 'citizens filming politicians’ behaviour'),
        ('viral content', 'material that spreads rapidly across social media through sharing', 'a video viewed millions of times in a day'),
        ('fake news', 'false or misleading information presented as news', 'invented stories shared during an election'),
    ],
    'thinkers': [
        ('Zuboff', 'tech companies profit by harvesting personal data to predict and shape behaviour', 'Neo-Marxism',
         'Zuboff argued surveillance capitalism turns human experience into data for sale.',
         'Users consent to terms of service and gain free services.'),
        ('Lyon', 'we live in a surveillance society in which everyday life is constantly monitored', 'Postmodernism',
         'Lyon argued digital technologies have made surveillance routine and largely invisible.',
         'People also use technology to watch the powerful (sousveillance).'),
        ('Mathiesen', 'in the synopticon the many watch the few through the media', 'Postmodernism',
         'Mathiesen argued media allow the public to observe the powerful, complementing the panopticon.',
         'The powerful still control most surveillance.'),
        ('Foucault', 'the panopticon shows how surveillance leads people to discipline themselves', 'Postmodernism',
         'Foucault argued people who believe they may be watched regulate their own behaviour.',
         'Online, many people share information freely despite being watched.'),
    ],
    'explain': [
        ('Explain two ways in which citizen journalism may challenge traditional news media.', 'Breaks stories first; provides alternative perspectives; exposes abuses by the powerful (synopticon); bypasses gatekeepers; reaches audiences directly through social media.', '2 marks for each explained way. [4]'),
        ('Explain two problems with citizen journalism.', 'Accuracy and lack of fact-checking; fake news and manipulated images; bias and lack of context; privacy and ethics; content still filtered by platforms and algorithms.', '2 marks for each explained problem. [4]'),
    ],
    'why': [
        ('way', 'ways', 'in which states or corporations use digital surveillance', ['monitoring social media posts', 'tracking location through phones', 'collecting browsing data for advertising', 'facial recognition cameras', 'reading private messages']),
    ],
    'claims': [
        ('Citizen journalism is produced only by professional reporters.', False, 'It is produced by members of the public.'),
        ('Surveillance capitalism involves profiting from personal data.', True, 'Companies collect data to predict and influence behaviour.'),
    ],
    'ar': ([('Citizen journalists can expose abuses of power.', 'phones and social media allow ordinary people to record and share events instantly.'),
            ('Some sociologists are concerned about digital surveillance.', 'states and corporations collect large amounts of personal data.')],
           ['the synopticon means the few watch the many.', 'Zuboff argued tech companies collect data only to protect users’ privacy.']),
    'scen': ['A passer-by in {city} films police officers using force during an arrest; the video is shared millions of times and leads to an official inquiry.',
             'A free fitness app used by thousands of people in {city} records their location, sleep and heart rate, and sells the data to advertisers and insurance companies.'],
    'views': {'Neo-Marxism': 'digital platforms extend capitalist control through surveillance capitalism, turning users’ data into profit (Zuboff, Fuchs).',
              'Pluralism': 'new media spread power more widely: citizen journalism lets ordinary people challenge elites and gatekeepers, users freely choose which platforms and apps to use (trading data for free services), and regulation can protect privacy.',
              'Postmodernism': 'surveillance is everywhere and is both top-down and bottom-up; people watch and are watched (Lyon, Mathiesen).',
              'Interactionism': 'people manage their online self-presentation, aware that they may be watched, and negotiate privacy in everyday interaction.'},
    'ctx': [('how citizen journalists decide what to post', {'meaning', 'behaviour'}),
            ('the sources of video used in television news', {'media', 'large', 'change'})],
    'methods': MEDIA_M,
    'data': [dict(what='sources of breaking news video', pop='news items', rows=['Professional camera crews', 'Footage from members of the public', 'Official sources (police, government)'], cols=('2010', '2023'), dist=True, nocount=True, n=[300, 400, 500],
                  base=[(65, 75), (10, 18), (10, 18)], delta=[(-30, -15), (15, 30), (-3, 3)], label='share of video used in breaking news reports (%)',
                  leads=['A content analysis of {n} breaking news reports on television in a country near {city} produced the results below.', '{person} analysed the sources of video in {n} breaking news reports.'],
                  expl=['smartphones allow members of the public to record events', 'news organisations ask for and use viewer footage', 'cost-cutting reduces professional crews'],
                  method='content analysis', claim='citizen journalism is changing the news',
                  counter='Professional journalists still select and frame public footage (gatekeeping); content analysis cannot show audience trust; online-only news is excluded.')],
    'essays': [('Explain two examples of digital surveillance.', 'State monitoring of social media; data collection by tech companies (Zuboff); facial recognition; workplace monitoring; parental tracking apps.',
                'social media empower citizens more than they empower states and corporations',
                'Citizen journalism; synopticon (Mathiesen); online protest movements; exposure of abuses; bypassing gatekeepers (Shirky).',
                'Surveillance capitalism (Zuboff); state surveillance (Morozov, Lyon); platform control of algorithms; fake news; digital divide.')],
})

CHAPTERS[18] = [g18a, g18b, g18c]


g19a = T('Global media and cultural imperialism')
build(g19a, {
    'terms': [
        ('global media', 'media organisations, products and platforms that operate across national borders', 'a streaming service available in 190 countries'),
        ('media imperialism', 'the domination of global media by Western, especially American, corporations and content', 'Hollywood films dominating cinema screens worldwide'),
        ('contra-flow', 'media products flowing from non-Western countries to the West and elsewhere', 'Bollywood films and K-dramas watched worldwide'),
        ('localisation', 'adapting global media formats to local audiences', 'a local version of an international talent show'),
        ('global village', 'McLuhan’s idea that electronic media connect the world into a single community', 'people across the world watching a sports final live'),
    ],
    'thinkers': [
        ('Schiller', 'American media corporations spread consumerist, capitalist values worldwide', 'Marxism',
         'Schiller argued global media form part of US economic and cultural domination.',
         'Contra-flows and local production challenge this view.'),
        ('Thussu', 'global media include significant contra-flows from non-Western producers', 'Transformationalism',
         'Thussu showed Bollywood, Al Jazeera and telenovelas reaching global audiences.',
         'Contra-flows are still small compared with US media.'),
        ('McLuhan', 'electronic media create a global village', 'Hyperglobalism',
         'McLuhan argued the medium itself changes how people experience the world.',
         'Access is unequal and global media can divide as well as unite.'),
    ],
    'explain': [
        ('Explain two arguments that global media spread cultural imperialism.', 'US corporations dominate film, TV and platforms; Western values of consumerism spread; local media cannot compete; English dominates; advertising spreads global brands.', '2 marks for each explained argument. [4]'),
        ('Explain what is meant by contra-flow, using an example.', 'Media products flowing from non-Western countries to the West and other regions, challenging Western dominance, e.g. K-pop, Bollywood films or Al Jazeera.', '1 mark meaning; 1 mark development; 1 mark example. [3]'),
    ],
    'why': [
        ('example', 'examples', 'of non-Western media reaching global audiences', ['Bollywood films', 'K-pop and K-dramas', 'Latin American telenovelas', 'Nigerian Nollywood films', 'Al Jazeera news', 'Japanese anime']),
    ],
    'claims': [
        ('Contra-flow refers to Western media flowing to developing countries.', False, 'Contra-flow refers to non-Western media flowing to the West and other regions.'),
        ('Some global TV formats are adapted for local audiences.', True, 'This is localisation (glocalisation).'),
    ],
    'ar': ([('Hollywood films are shown worldwide.', 'large US media corporations have the resources to distribute globally.'),
            ('Some sociologists question media imperialism.', 'non-Western media such as Bollywood and K-pop also have global audiences.')],
           ['McLuhan argued electronic media isolate communities from one another.', 'contra-flow means local media disappear completely.']),
    'scen': ['In {city}, the five most popular TV programmes include two American dramas, a local version of an international talent show and two Korean dramas.',
             'A local film industry in {city} struggles to compete as cinemas show mainly Hollywood films, which have much bigger marketing budgets.'],
    'views': {'Marxism': 'global media spread Western capitalist values and consumerism, serving the interests of US-based corporations (Schiller).',
              'Transformationalism': 'global media are changing cultures, but flows are multi-directional and local cultures adapt global products (Thussu).',
              'Postmodernism': 'global media offer endless choice; audiences mix global and local media to create hybrid identities.',
              'Pluralism': 'media success reflects audience choice in a competitive market: Hollywood dominates where audiences prefer it, while local and non-Western producers can and do compete when they meet audience demand.'},
    'ctx': [('the origin of films shown in cinemas', {'media', 'large', 'change'}),
            ('how young people use foreign media to shape their identities', {'meaning', 'young'})],
    'methods': MEDIA_M,
    'data': [dict(what='film origin', pop='films', rows=['US films', 'Domestic films', 'Other foreign films'], cols=('2000', '2022'), dist=True, nocount=True, n=[3],
                  base=[(60, 70), (15, 25), (8, 15)], delta=[(-15, -5), (5, 12), (0, 6)], label='share of cinema box-office takings in a country (%)',
                  leads=['Box-office statistics for a country near {city} are shown below.', 'The table shows the share of cinema takings by film origin in one country.'],
                  expl=['US studios’ global distribution and marketing', 'growth of domestic production and quotas', 'contra-flows from other non-Western producers'],
                  method='official statistics', claim='media imperialism is declining',
                  counter='US films still dominate; streaming is not included; domestic films may copy Hollywood styles or be co-produced by US firms.')],
    'essays': [('Explain two ways in which global media may affect local cultures.', 'Homogenisation and Americanisation; consumerism; contra-flow; glocalisation of formats; hybrid identities.',
                'global media lead to cultural imperialism',
                'Schiller; Hollywood dominance; global platforms owned by US firms; consumerism; local media decline.',
                'Contra-flow (Thussu); localisation; active audiences; hybridity; national regulation and quotas; growth of non-Western producers.')],
})

g19b = T('The media and the public sphere')
build(g19b, {
    'terms': [
        ('public sphere', 'Habermas’s term for a space where citizens can debate public issues freely and rationally', 'eighteenth-century coffee houses where people discussed politics'),
        ('refeudalisation', 'Habermas’s term for the decline of the public sphere as commercial media turn citizens into passive consumers', 'news replaced by celebrity gossip'),
        ('infotainment', 'media content that mixes information with entertainment', 'news programmes with celebrity stories and dramatic graphics'),
        ('public service broadcasting', 'broadcasting funded publicly to inform, educate and entertain all citizens', 'a national broadcaster with balanced news'),
        ('digital public sphere', 'online spaces where citizens discuss public issues', 'political debate on social media'),
    ],
    'thinkers': [
        ('Habermas', 'commercial media have undermined the public sphere of rational debate', 'Neo-Marxism',
         'Habermas argued profit-driven media turn citizens into consumers and reduce politics to spectacle.',
         'His ideal of the historical public sphere excluded women and the poor.'),
        ('Curran', 'public service broadcasting helps sustain a democratic public sphere', 'Neo-Marxism',
         'Curran found countries with strong public service broadcasting had better-informed citizens.',
         'Critics argue public broadcasters can reflect establishment views.'),
        ('Fraser', 'there are many counter-publics, not one public sphere', 'Liberal feminism',
         'Fraser argued excluded groups such as women created their own counter-public spheres.',
         'Fragmented spheres may struggle to influence policy.'),
    ],
    'explain': [
        ('Explain what Habermas meant by the public sphere.', 'A space between private life and the state where citizens could debate public issues freely and rationally, forming public opinion, e.g. coffee houses, newspapers and pamphlets.', '1 mark meaning; 1 mark development; 1 mark example. [3]'),
        ('Explain two ways in which new media might revive the public sphere.', 'Anyone can publish and debate; access to information; online petitions and campaigns; citizen journalism; counter-publics can organise.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('threat', 'threats', 'to the public sphere', ['commercialisation and infotainment', 'concentration of ownership', 'echo chambers and filter bubbles', 'fake news', 'state censorship', 'online abuse silencing people']),
    ],
    'claims': [
        ('Habermas argued commercial media strengthened rational public debate.', False, 'He argued they weakened it (refeudalisation).'),
        ('Infotainment mixes news with entertainment.', True, 'It is linked to concerns about the decline of serious debate.'),
    ],
    'ar': ([('Habermas was concerned about commercial media.', 'profit-driven media turn citizens into passive consumers.'),
            ('Some argue social media create a new public sphere.', 'anyone can publish and debate political issues online.')],
           ['refeudalisation means the growth of rational debate.', 'Fraser argued there is only one public sphere that includes everyone equally.']),
    'scen': ['During an election in {city}, the most-watched TV news programme spends more time on candidates’ clothes and personal lives than on their policies.',
             'Residents of {city} use an online forum to debate a proposed motorway; the forum attracts thousands of comments, but many are abusive and few come from older residents.'],
    'views': {'Neo-Marxism': 'commercial media have undermined rational debate (refeudalisation), turning citizens into consumers (Habermas).',
              'Pluralism': 'diverse media and new digital spaces allow many voices to be heard, sustaining democratic debate.',
              'Postmodernism': 'there is no single public sphere, only fragmented spaces and spectacles; reality and image blur.',
              'Liberal feminism': 'excluded groups form counter-publics, and new media give them new spaces to be heard (Fraser).'},
    'ctx': [('the content of TV election coverage', {'media', 'large'}),
            ('how people take part in online political debate', {'meaning', 'behaviour'})],
    'methods': MEDIA_M,
    'data': [dict(what='election coverage', pop='news items', rows=['Policies', 'Personalities and scandals', 'Opinion polls and the “horse race”'], cols=('Public service channel', 'Commercial channel'), cmp=True, dist=True, nocount=True, n=[200, 300, 400],
                  base=[(40, 50), (20, 30), (20, 30)], delta=[(-25, -10), (8, 18), (-2, 6)], label='share of election news time (%)',
                  leads=['A content analysis of {n} election news items on two channels in a country near {city} produced the results below.', '{person} analysed {n} election news items on two TV channels.'],
                  expl=['commercial channels prefer infotainment to attract audiences', 'public service channels have a duty to inform', 'refeudalisation of the public sphere'],
                  method='content analysis', claim='commercial media weaken the public sphere',
                  counter='Viewers may use several sources; online debate is not included; time spent does not measure quality; categories overlap.')],
    'essays': [('Explain two reasons why Habermas believed the public sphere had declined.', 'Commercialisation; advertising; concentration of ownership; infotainment; public relations and spin; passive consumers.',
                'new media have created a new public sphere',
                'Online debate; citizen journalism; counter-publics (Fraser); petitions and campaigns; access to information.',
                'Echo chambers and filter bubbles; fake news; corporate control of platforms; abuse silencing voices; digital divide; Habermas: commercialisation continues.')],
})

g19c = T('Researching the media: content analysis and semiology')
build(g19c, {
    'research': True,
    'terms': [
        ('content analysis', 'a method of systematically counting and categorising the content of media texts', 'counting how often women appear as experts in news'),
        ('coding schedule', 'the list of categories a researcher uses to classify media content in a content analysis', 'categories such as “victim”, “expert” or “offender”'),
        ('thematic analysis', 'a qualitative analysis of the underlying themes and meanings in media texts', 'identifying how migrants are framed in news stories'),
        ('semiology', 'the study of signs and the meanings they convey', 'analysing what a red rose in an advert signifies'),
        ('denotation', 'the literal, obvious meaning of a sign', 'a picture of a dove shows a white bird'),
        ('connotation', 'the cultural and symbolic meanings associated with a sign', 'a dove connotes peace'),
    ],
    'thinkers': [
        ('Barthes', 'signs carry denotative and connotative meanings, and myths make ideology seem natural', 'Neo-Marxism',
         'Barthes analysed a magazine cover of a black soldier saluting the French flag as a myth supporting colonialism.',
         'Interpretations of signs are subjective.'),
        ('Glasgow University Media Group', 'systematic content analysis reveals bias in television news', 'Neo-Marxism',
         'They used content analysis and thematic analysis to study the language and images of news.',
         'Critics argue their categories reflected their own assumptions.'),
        ('Philo', 'audiences can be studied by asking them to write their own news stories', 'Cultural effects theory',
         'Philo’s news game method showed how closely audiences reproduce media accounts.',
         'Group tasks may produce artificial responses.'),
    ],
    'explain': [
        ('Explain two strengths of content analysis as a method for studying the media.', 'Quantitative, systematic and reliable (repeatable with the same coding schedule); large samples; cheap and accessible; no ethical problems with participants; can show changes over time.', '2 marks for each explained strength. [4]'),
        ('Explain the difference between denotation and connotation, using an example.', 'Denotation is the literal meaning (e.g. a picture of a red rose); connotation is the cultural meaning (e.g. love and romance).', '1 mark each; 1 mark example. [3]'),
    ],
    'why': [
        ('limitation', 'limitations', 'of content analysis', ['coding categories may reflect researcher bias', 'it does not show audience interpretations', 'counting ignores meaning and context', 'it cannot reveal producers’ intentions', 'large samples are time-consuming to code']),
    ],
    'claims': [
        ('Content analysis directly measures how audiences interpret media.', False, 'It analyses texts, not audiences’ interpretations.'),
        ('Semiology studies signs and their meanings.', True, 'It analyses denotation, connotation and myth.'),
    ],
    'ar': ([('Content analysis is seen as reliable.', 'other researchers can repeat it using the same coding schedule.'),
            ('Semiology is criticised for subjectivity.', 'different analysts may read different meanings into the same signs.')],
           ['denotation refers to the hidden cultural meaning of a sign.', 'content analysis involves interviewing audiences about their views.']),
    'scen': ['{person} records every advert shown in two hours of evening television in {city} and counts how many show women at home and how many show women at work.',
             'A researcher analyses a perfume advert from {city}, arguing that the gold colours, silk sheets and soft lighting connote luxury, desire and femininity.',
             'A research team asks groups of viewers in {city} to write their own news report on a riot, using photographs taken from real TV coverage.'],
    'views': {'Positivism': 'content analysis is useful because it is systematic, quantitative and reliable, allowing comparisons and generalisations.',
              'Interpretivism': 'counting ignores meaning; qualitative methods such as semiology and thematic analysis reveal how texts create meaning, and audience research shows interpretation.',
              'Neo-Marxism': 'research should uncover the ideology hidden in media texts, for example how signs naturalise dominant values (Barthes, GUMG).',
              'Postmodernism': 'texts have no fixed meaning; audiences create many meanings, so no method can uncover a single true reading.'},
    'ctx': [('the representation of migrants in newspapers', {'media', 'large', 'change'}),
            ('how teenagers interpret music videos', {'meaning', 'young'})],
    'methods': MEDIA_M,
    'source': [dict(text='A researcher in {city} studied 300 newspaper articles about migrants using a coding schedule. 62% of articles used words such as “flood” or “wave”; 15% quoted a migrant. A semiological analysis of the front-page photographs found migrants were usually shown in large, faceless crowds.',
                    method='content analysis', about='representations of migrants', finds=['62% of articles used words such as “flood” or “wave”', 'only 15% quoted a migrant', 'photographs showed migrants as faceless crowds'],
                    persp='Neo-Marxism', pview='The findings suggest the media construct migrants as a threat, a myth (Barthes) that diverts attention from inequality and reinforces dominant ideology.',
                    claim='content analysis is the most useful method for studying media representations', pro='The source shows content analysis produces clear, reliable, comparable figures; combined with semiology it reveals meaning.',
                    con='Coding categories may reflect the researcher’s views; counting does not reveal meaning or audience interpretation; semiology is subjective; audience research (Morley, Philo) is also needed.', flags={'media', 'large'})],
    'essays': [('Explain two strengths of semiology as a method for researching the media.', 'Reveals hidden meanings and ideology; analyses images as well as words; qualitative depth; shows how myths naturalise dominant values (Barthes).',
                'content analysis is the most effective method for researching the media',
                'Systematic, reliable, quantitative; large samples; shows patterns and changes over time; used by GUMG; no ethical problems.',
                'Coding bias; ignores meaning and context; cannot show effects; semiology and thematic analysis reveal meaning; audience research (Morley, Philo); mixed methods.')],
})
classify(g19c, [
    ('{person} counts how many times women appear as experts in 200 news reports from {city}.', 'Quantitative content analysis', 'counting and categorising media content.'),
    ('A researcher in {city} studies the colours, objects and camera angles in a car advert to uncover what they symbolise.', 'Semiology', 'analysing signs and their connotations.'),
    ('A researcher in {city} reads 50 news stories about protests to identify recurring ways in which protesters are framed.', 'Thematic analysis', 'a qualitative analysis of underlying themes and meanings.'),
    ('A team in {city} shows a news report to groups of viewers and then discusses with them how they understood it.', 'Audience reception research', 'studying how audiences interpret media texts.'),
], ['Quantitative content analysis', 'Semiology', 'Thematic analysis', 'Audience reception research', 'Laboratory experiment', 'Official statistics'], 'Which approach to researching the media is being used?', C='C3', D=(1, 2), name='media_method')

CHAPTERS[19] = [g19a, g19b, g19c]


# ============================================================== RELIGION (chapters 20-25)

REL_M = ['questionnaire', 'structured interview', 'unstructured interview', 'semi-structured interview', 'participant observation', 'covert participant observation',
         'non-participant observation', 'official statistics', 'personal documents', 'case study', 'content analysis', 'longitudinal study']

VR = {
    'Functionalism': 'religion promotes social solidarity and value consensus, helps people cope with life crises and reinforces the collective conscience (Durkheim, Malinowski, Parsons).',
    'Marxism': 'religion is ideology that legitimates class inequality and offers false comfort to the oppressed (“the opium of the people”), creating false consciousness (Marx, Lenin).',
    'Radical feminism': 'religion is patriarchal: male-dominated organisations, scriptures and rules control women and legitimate their subordination (de Beauvoir, El Saadawi).',
    'Weberian theory': 'religious ideas can bring about social change; beliefs such as the Protestant ethic shaped economic behaviour, and religion can motivate social movements (Weber).',
    'Postmodernism': 'religion has become a matter of individual choice and consumption; people pick and mix beliefs in a spiritual supermarket (Lyon, Heelas).',
    'Religious market theory': 'religion is a market: when there is competition and choice, religious organisations meet people’s needs and religiosity stays strong (Stark and Bainbridge).',
    'Neo-Marxism': 'religion can be relatively autonomous: it may support ruling-class hegemony but can also inspire resistance and liberation (Gramsci, Maduro).',
}


def g24a_att(r, D):
    for _ in range(50):
        p1, p2 = r.choice([20, 25, 30, 40, 50, 60]), None
        p2 = p1 + r.choice([2, 4, 5, 6, 8, 10])
        a1 = r.choice([2.0, 2.4, 3.0, 3.6, 4.0, 4.5, 5.0, 6.0])
        a2 = round(a1 * r.choice([0.4, 0.5, 0.6, 0.7, 0.75, 0.8]), 2)
        if round(a2, 1) == a2:
            break
    y1, y2 = r.choice([(1980, 2020), (1985, 2022), (1990, 2023), (1975, 2015)])
    d = ctxd(r)
    intro = (f'In a country near {d["city"]}, the population was {p1} million in {y1} and {p2} million in {y2}. '
             f'Average weekly attendance at religious services was {_pc(a1)} million in {y1} and {_pc(a2)} million in {y2}.')
    r1, r2 = a1 / p1 * 100, a2 / p2 * 100
    pc = (a2 - a1) / a1 * 100
    if D <= 1:
        ans = f'{_pc(r1)}%'
        ds = []
        for x in [r2, a1 / p2 * 100, r1 / 2, r1 + 5, r1 * 2]:
            v = f'{_pc(x)}%'
            if v != ans and v not in ds:
                ds.append(v)
        opts, a = mcq(r, ans, ds[:3])
        return {'stem': f'{intro} What percentage of the population attended a weekly service in {y1}?', 'options': opts, 'answer': a,
                'key': f'{_pc(a1)} ÷ {p1} × 100 = {_pc(r1)}%. [1]', 'marks': 1}
    parts = [(f'Calculate the percentage of the population attending weekly services in {y1} and in {y2}. Give your answers to 1 decimal place.',
              f'{y1}: {_pc(a1)} ÷ {p1} × 100 = {r1:.1f}%; {y2}: {_pc(a2)} ÷ {p2} × 100 = {r2:.1f}%.', '1 mark each. [2]'),
             (f'Calculate the percentage change in the number of people attending weekly services between {y1} and {y2}.',
              f'({_pc(a2)} − {_pc(a1)}) ÷ {_pc(a1)} × 100 = −{_pc(-pc)}% (a fall of {_pc(-pc)}%).', f'1 mark method; 1 mark answer (accept a fall of {_pc(-pc)}%). [2]'),
             ('Explain one reason why attendance figures may not be a valid measure of religiosity.', 'People may believe without belonging (Davie); people attend for social or family reasons; religion is practised privately or online; figures are collected differently by different organisations.', '1 mark identifying; 1 mark explaining. [2]'),
             ('Explain how a supporter of the secularisation thesis might use these data.', 'Falling attendance, especially as a share of a growing population, shows religion losing social significance (Wilson, Bruce).', '1 mark secularisation idea; 1 mark use of the data. [2]'),
             ('Explain how a critic of the secularisation thesis might respond to these data.', 'Decline in attendance may show a change in the form of religion (believing without belonging, spirituality, vicarious religion) rather than decline; religion grows elsewhere.', '1 mark criticism; 1 mark application. [2]')]
    if D == 2:
        sel = parts[:2]
    elif D == 3:
        sel = parts[:3]
    elif D == 4:
        sel = parts[:2] + [parts[2], r.choice(parts[3:])]
    else:
        sel = parts[:2] + [parts[2], parts[3], parts[4]]
    return assemble(intro, sel, 'numerical' if D <= 3 else 'multi_step')


g20a = T('Substantive, functional and social constructionist definitions of religion')
build(g20a, {
    'terms': [
        ('substantive definition of religion', 'a definition based on the content of religious belief, such as belief in God or the supernatural', 'Weber’s focus on belief in a superior power'),
        ('functional definition of religion', 'a definition based on what religion does for individuals or society, such as creating solidarity', 'Durkheim’s view of religion as uniting a moral community'),
        ('social constructionist definition of religion', 'a definition that focuses on how members of society themselves define what counts as religion', 'debates over whether a new movement is a “real” religion'),
        ('sacred', 'things set apart and forbidden, which inspire awe and reverence', 'a holy book or temple'),
        ('profane', 'ordinary, everyday things with no special significance', 'a household chair'),
        ('civil religion', 'a belief system that attaches sacred qualities to the nation and its symbols', 'reverence for the national flag and anthem'),
    ],
    'thinkers': [
        ('Durkheim', 'religion is a unified system of beliefs and practices relating to sacred things that unites believers into a moral community', 'Functionalism',
         'Durkheim defined religion functionally, through its role in creating solidarity, and by the distinction between sacred and profane.',
         'Functional definitions are very inclusive: football or nationalism could count as religion.'),
        ('Weber', 'religion is belief in a superior or supernatural power above nature', 'Weberian theory',
         'Weber’s substantive definition focuses on the content of belief.',
         'It is exclusive and may be Western-biased, excluding Buddhism and other non-theistic religions.'),
        ('Aldridge', 'definitions of religion are socially constructed and contested', 'Interactionism',
         'Aldridge showed Scientology is recognised as a religion in some countries and not in others.',
         'Constructionist definitions make generalisation difficult.'),
    ],
    'explain': [
        ('Explain the difference between substantive and functional definitions of religion.', 'Substantive: defines religion by its content, such as belief in God or the supernatural (Weber); functional: defines it by what it does, e.g. integration or coping (Durkheim, Yinger).', '1 mark each definition; 1 mark contrast. [3]'),
        ('Explain one strength and one weakness of functional definitions of religion.', 'Strength: inclusive, covers non-theistic beliefs and does not favour Western religions; weakness: too inclusive, so football or nationalism could be counted as religion.', '1 mark identifying each; 1 mark explaining each. [4]'),
    ],
    'why': [
        ('problem', 'problems', 'in defining religion', ['substantive definitions may exclude non-theistic beliefs', 'functional definitions may include non-religious activities', 'definitions differ between cultures', 'groups disagree about what counts as religion', 'definitions affect the measurement of secularisation']),
    ],
    'claims': [
        ('Weber’s definition of religion is functional.', False, 'Weber’s definition is substantive, focusing on belief in a superior or supernatural power.'),
        ('Durkheim distinguished between the sacred and the profane.', True, 'Sacred things inspire awe and are set apart from ordinary profane things.'),
    ],
    'ar': ([('Functional definitions are criticised as too inclusive.', 'activities such as supporting a football team could be counted as religion.'),
            ('Substantive definitions may be Western-biased.', 'they focus on belief in God, excluding non-theistic religions.')],
           ['social constructionist definitions are fixed and universal.', 'Durkheim defined religion only as belief in one God.']),
    'scen': ['A new movement in {city} meets weekly, follows a leader’s teachings about personal growth and holds ceremonies, but has no belief in God; the government refuses to register it as a religion.',
             'Fans of a football club in {city} gather every week, sing songs together, treat the stadium as a sacred place and mourn former players with rituals.'],
    'views': {'Functionalism': 'religion should be defined by its functions: anything that creates solidarity and shared sacred values may count (Durkheim).',
              'Weberian theory': 'religion should be defined by its content: belief in a superior or supernatural power (Weber).',
              'Interactionism': 'what counts as religion is socially constructed by the people and authorities involved (Aldridge).',
              'Postmodernism': 'in a pick-and-mix society the boundaries of religion are blurred; personal spiritual and secular beliefs mix.'},
    'ctx': [('how members of new movements define their beliefs', {'meaning', 'hidden'}),
            ('the number of people who describe themselves as religious', {'large', 'change'})],
    'methods': REL_M,
    'data': [dict(what='definitions of religion', pop='adults', rows=['Belief in God', 'Belief in a spiritual force but not God', 'Belong to a religious group', 'Practise rituals at home'], cols=('Say this makes a person religious', 'Say this applies to them'), cmp=True, nocount=True,
                  base=[(75, 85), (30, 40), (55, 65), (40, 50)], delta=[(-40, -25), (-15, -5), (-30, -15), (-20, -5)], label='adults agreeing (%)',
                  leads=['A survey of {n} adults in {city} asked what makes a person religious, and which features applied to them.', '{person} surveyed {n} adults about how they define religion.'],
                  expl=['most people use a substantive definition (belief in God)', 'definitions of religion differ between individuals', 'many people hold beliefs without belonging'],
                  method='questionnaire', claim='how religion is defined affects how religious a society appears',
                  counter='Closed questions may not capture complex views; one city may be untypical; social desirability may affect answers.')],
    'essays': [('Explain two ways of defining religion.', 'Substantive (Weber); functional (Durkheim, Yinger); social constructionist (Aldridge); inclusive and exclusive definitions.',
                'functional definitions of religion are more useful than substantive definitions',
                'Inclusive; avoid Western bias; capture civil religion and new forms; link to the role of religion in society (Durkheim).',
                'Too inclusive; substantive definitions are clearer and easier to measure (Weber); social constructionist views show definitions are contested; affect secularisation debate.')],
})

g20b = T('Measuring religiosity: belief, belonging and practice')
build(g20b, {
    'terms': [
        ('religiosity', 'the extent to which people are religious, measured by belief, belonging and practice', 'how often people pray or attend services'),
        ('religious belief', 'what people believe about God, the supernatural or the afterlife', 'belief in life after death'),
        ('religious belonging', 'membership of, or identification with, a religious organisation', 'being a registered member of a church'),
        ('religious practice', 'religious activities such as attendance, prayer and rituals', 'attending a temple weekly'),
        ('operationalisation', 'turning a concept into something that can be measured', 'measuring religiosity by counting weekly attendance'),
        ('census question on religion', 'a question in a national census about religious identity', '“What is your religion?” in a population census'),
    ],
    'thinkers': [
        ('Davie', 'many people believe without belonging', 'Postmodernism',
         'Davie argued attendance has declined faster than belief, so religion has become privatised rather than disappeared.',
         'Voas and Crockett found belief has also declined.'),
        ('Glock and Stark', 'religiosity has several dimensions, including belief, practice, experience, knowledge and consequences', 'Positivism',
         'Glock and Stark argued religiosity should be measured on several dimensions, not just attendance.',
         'Each dimension is itself difficult to measure.'),
        ('Voas and Crockett', 'belief and belonging are declining together', 'Positivism',
         'Their analysis of survey data showed each generation is less likely to believe and belong than its parents.',
         'Surveys may not capture new forms of spirituality.'),
    ],
    'explain': [
        ('Explain two problems of using attendance figures to measure religiosity.', 'People attend for non-religious reasons (social, family, school places); religious people may not attend (believing without belonging); counting methods vary; religion may be practised privately or online.', '2 marks for each explained problem. [4]'),
        ('Explain the difference between religious belief and religious belonging.', 'Belief is what people hold to be true (e.g. God, afterlife); belonging is membership of or identification with a religious organisation; one can exist without the other.', '1 mark each; 1 mark contrast. [3]'),
    ],
    'why': [
        ('way', 'ways', 'of measuring religiosity', ['attendance at services', 'membership figures', 'surveys of belief', 'census questions on religious identity', 'frequency of prayer', 'participation in rites of passage']),
    ],
    'claims': [
        ('Attendance figures are a complete measure of religiosity.', False, 'They miss private belief, online religion and people who believe without belonging.'),
        ('Davie argued many people believe without belonging.', True, 'She found belief remains higher than attendance.'),
    ],
    'ar': ([('Census figures may exaggerate religiosity.', 'people may state a religion as a cultural identity rather than active belief.'),
            ('Attendance may underestimate religiosity.', 'many people believe and pray privately without attending services.')],
           ['Glock and Stark argued religiosity has only one dimension.', 'belonging means holding private religious beliefs.']),
    'scen': ['In a census in {city}, 70% of people state a religion, but only 9% attend a religious service in a typical week.',
             '{person} interviews people in {city} who never attend services but say they pray every day and believe in an afterlife.'],
    'views': {'Positivism': 'religiosity can be measured objectively through attendance, membership and survey data, allowing comparison over time (Voas and Crockett).',
              'Interpretivism': 'religiosity is about meaning; qualitative methods are needed to understand belief and private practice.',
              'Postmodernism': 'religion has become privatised and individual: believing without belonging (Davie) and spirituality are not captured by attendance.',
              'Functionalism': 'participation in shared rituals is what matters, because religion’s function is to create solidarity.'},
    'ctx': [('how people practise religion privately', {'meaning', 'hidden', 'private'}),
            ('changes in religious attendance over time', {'large', 'change'})],
    'methods': REL_M,
    'data': [dict(what='belief, belonging and practice', pop='adults', rows=['Believe in God', 'Belong to a religious group', 'Attend services at least monthly'], cols=('1990', '2020'), nocount=True,
                  base=[(65, 75), (55, 65), (20, 30)], delta=[(-20, -10), (-25, -15), (-12, -6)], label='adults in each category (%)',
                  leads=['Two national surveys, each of {n} adults, produced the results below.', '{person} compared national surveys of {n} adults in a country near {city}.'],
                  expl=['belief has declined more slowly than practice (believing without belonging)', 'younger generations are less religious (Voas and Crockett)', 'religion has become more private'],
                  method='questionnaire', claim='believing without belonging explains the decline in attendance',
                  counter='Belief has also fallen; surveys rely on self-report; question wording may differ between years; spirituality may be missed.')],
    'essays': [('Explain two difficulties in measuring religiosity.', 'Defining religion; operationalising belief; attendance vs. belief; census identity; changing forms (online, private); reliability of counts.',
                'statistics on religious attendance are a reliable measure of religiosity',
                'Reliable, comparable figures over time; used by Bruce and Wilson; show clear decline; large samples.',
                'Davie: believing without belonging; vicarious religion; census identity; private and online religion; counting methods vary; validity problems.')],
})

g20c = T('Religion and spirituality in contemporary society')
build(g20c, {
    'terms': [
        ('spirituality', 'a personal search for meaning and inner wellbeing, often outside organised religion', 'meditation, yoga and mindfulness'),
        ('New Age', 'a diverse set of beliefs and practices focusing on self-spirituality and personal growth', 'crystal healing, astrology and alternative therapies'),
        ('spiritual revolution', 'Heelas and Woodhead’s claim that traditional religion is being replaced by holistic spirituality', 'people leaving churches for yoga classes'),
        ('privatisation of religion', 'the movement of religion from the public sphere into private life', 'personal prayer at home rather than attendance'),
        ('spiritual shopping', 'choosing beliefs and practices from many traditions to suit oneself', 'combining Buddhist meditation with Christian prayer'),
    ],
    'thinkers': [
        ('Heelas and Woodhead', 'a spiritual revolution is taking place as people move from congregational religion to holistic spirituality', 'Postmodernism',
         'Their Kendal Project found holistic spirituality growing while church attendance fell.',
         'Holistic spirituality was still small and not replacing church losses.'),
        ('Bruce', 'spirituality is a sign of secularisation, not religious revival', 'Weberian theory',
         'Bruce argued New Age beliefs are weak, individual and have little social significance.',
         'Others argue spirituality is meaningful to those who practise it.'),
        ('Lyon', 'religion has relocated to the sphere of consumption in a postmodern “Jesus in Disneyland”', 'Postmodernism',
         'Lyon argued people consume religion as part of a pick-and-mix lifestyle.',
         'Many people still belong to traditional religions.'),
    ],
    'explain': [
        ('Explain two reasons for the growth of spirituality outside organised religion.', 'Individualisation and focus on self-improvement; distrust of traditional authority; consumer culture and choice; globalisation spreading Eastern practices; wellness industry.', '2 marks for each explained reason. [4]'),
        ('Explain what Heelas and Woodhead meant by a spiritual revolution.', 'A shift from congregational religion, based on obedience to external authority, to holistic spirituality focused on inner wellbeing; found in the Kendal Project.', '1 mark meaning; 1 mark development; 1 mark evidence. [3]'),
    ],
    'why': [
        ('example', 'examples', 'of contemporary spirituality', ['yoga', 'meditation and mindfulness', 'reiki and alternative healing', 'astrology', 'spiritual retreats', 'online spiritual communities']),
    ],
    'claims': [
        ('Heelas and Woodhead found holistic spirituality had overtaken church attendance in Kendal.', False, 'Holistic spirituality grew but remained much smaller than congregational religion.'),
        ('Bruce sees spirituality as evidence of secularisation.', True, 'He argues it is individual and has little social significance.'),
    ],
    'ar': ([('Spirituality has grown in many Western societies.', 'people seek personal meaning and wellbeing rather than obeying religious authority.'),
            ('Bruce is sceptical of a spiritual revolution.', 'he argues spirituality has little social influence and cannot replace religion.')],
           ['the spiritual revolution means a rise in church attendance.', 'spirituality always requires membership of an organised religion.']),
    'scen': ['{woman}, who grew up in a religious family in {city}, no longer attends services but practises yoga, meditates daily and reads about Buddhism and astrology.',
             'A wellness centre in {city} offers mindfulness, reiki and sound healing; it is busier on Sunday mornings than the church next door.'],
    'views': {k: VR[k] for k in ('Postmodernism', 'Weberian theory', 'Functionalism', 'Marxism')},
    'ctx': [('why people take part in holistic spirituality', {'meaning', 'behaviour'}),
            ('the number of people involved in different forms of spirituality', {'large', 'change'})],
    'methods': REL_M,
    'data': [dict(what='spiritual and religious activity', pop='adults', rows=['Attend religious services weekly', 'Practise meditation or yoga weekly', 'Describe themselves as “spiritual but not religious”'], cols=('2000', '2020'), nocount=True,
                  base=[(12, 18), (3, 6), (8, 14)], delta=[(-6, -3), (4, 9), (6, 14)], label='adults (%)',
                  leads=['Surveys of {n} adults in {city} in two years produced the results below.', '{person} compared surveys of {n} adults about religion and spirituality.'],
                  expl=['individualisation and the search for self-fulfilment', 'decline of traditional religious authority', 'consumer culture and the wellness industry'],
                  method='questionnaire', claim='a spiritual revolution is taking place',
                  counter='Yoga may be exercise rather than spirituality; numbers remain smaller than religious attendance; self-description may be vague.')],
    'essays': [('Explain two features of New Age spirituality.', 'Self-spirituality; holistic wellbeing; detraditionalisation; pick and mix; individual choice; consumer-based.',
                'the growth of spirituality shows that religion is changing rather than declining',
                'Heelas and Woodhead; Davie; Lyon’s religious consumerism; postmodern pick-and-mix; growth of yoga and mindfulness.',
                'Bruce: spirituality is weak and individual, a sign of secularisation; numbers are small; Kendal Project showed limited growth; commercialised wellness may not be religious.')],
})

CHAPTERS[20] = [g20a, g20b, g20c]


g21a = T('Functionalist views: religion, integration and collective conscience (Durkheim)')
build(g21a, {
    'terms': [
        ('collective conscience', 'Durkheim’s term for the shared beliefs, values and norms that bind a society together', 'shared moral rules about right and wrong'),
        ('totemism', 'the worship of a sacred symbol (a totem) that represents a clan', 'Aboriginal clans honouring an animal emblem'),
        ('social solidarity', 'the sense of belonging and integration that binds members of society together', 'a nation mourning together after a disaster'),
        ('civil religion', 'Bellah’s term for a belief system that attaches sacred qualities to the nation', 'oaths of allegiance and national ceremonies'),
        ('life crises', 'events such as death that create stress, which religion helps people cope with (Malinowski)', 'funeral rituals comforting mourners'),
        ('functional alternative', 'something that performs the same functions as religion', 'nationalism or sport creating solidarity'),
    ],
    'thinkers': [
        ('Durkheim', 'by worshipping sacred symbols, people are really worshipping society itself', 'Functionalism',
         'Durkheim’s study of Aboriginal totemism argued religion reinforces the collective conscience and social solidarity.',
         'In diverse modern societies, religion may divide as well as unite.'),
        ('Malinowski', 'religion helps people cope with uncertainty and life crises', 'Functionalism',
         'Malinowski found Trobriand Islanders performed rituals before dangerous ocean fishing but not in the safe lagoon.',
         'Religion can also cause anxiety, for example about sin.'),
        ('Parsons', 'religion provides core values and answers ultimate questions about meaning', 'Functionalism',
         'Parsons argued religion legitimates norms and helps people make sense of suffering.',
         'Marxists argue these values benefit the ruling class.'),
        ('Bellah', 'civil religion integrates diverse societies through shared sacred national beliefs', 'Functionalism',
         'Bellah studied American civil religion, uniting people of many faiths around the nation.',
         'Civil religion may not be religion at all.'),
    ],
    'explain': [
        ('Explain two functions of religion according to functionalists.', 'Social solidarity and the collective conscience (Durkheim); coping with life crises (Malinowski); legitimating core values and answering ultimate questions (Parsons); civil religion (Bellah).', '2 marks for each explained function. [4]'),
        ('Explain what Durkheim meant by the collective conscience.', 'The shared beliefs, values and moral rules that bind society together; religious rituals reinforce it by uniting people around sacred symbols that represent society.', '1 mark meaning; 2 marks development linked to religion. [3]'),
    ],
    'why': [
        ('criticism', 'criticisms', 'of the functionalist view of religion', ['religion can cause conflict and division', 'it ignores the role of religion in inequality', 'Durkheim’s evidence on totemism is questionable', 'it does not fit diverse, multi-faith societies', 'functional alternatives can perform the same role']),
    ],
    'claims': [
        ('Malinowski found rituals were used most in safe, predictable situations.', False, 'He found rituals were used in dangerous, uncertain situations such as ocean fishing.'),
        ('Durkheim argued that worshipping sacred symbols is really worshipping society.', True, 'Sacred symbols represent the group itself.'),
    ],
    'ar': ([('Functionalists see religion as promoting solidarity.', 'shared rituals and beliefs bind members of society together.'),
            ('Critics argue the functionalist view fits small societies better.', 'modern societies contain many religions that may divide people.')],
           ['Durkheim argued religion mainly creates conflict between social classes.', 'Malinowski argued religion has no role in helping people cope with death.']),
    'scen': ['After a terrorist attack in {city}, people of many faiths and none gather in the main square, light candles, hold a minute’s silence and sing the national anthem.',
             'Fishermen in a village near {city} hold a religious ceremony before every long voyage out to sea, but not before fishing in the calm harbour.'],
    'views': {k: VR[k] for k in ('Functionalism', 'Marxism', 'Radical feminism', 'Postmodernism')},
    'ctx': [('the role of religious festivals in community life', {'meaning', 'behaviour'}),
            ('participation in national ceremonies', {'large', 'change'})],
    'methods': REL_M,
    'data': [dict(what='religion and community', pop='adults', rows=['Feel they belong to their community', 'Have helped a neighbour in the last month', 'Trust most people'], cols=('Attend services regularly', 'Never attend'), cmp=True, nocount=True,
                  base=[(65, 75), (55, 65), (45, 55)], delta=[(-20, -10), (-15, -5), (-12, -4)], label='adults agreeing (%)',
                  leads=['A survey of {n} adults in {city} compared regular attenders with those who never attend religious services.', '{person} surveyed {n} adults in {city} about religion and community.'],
                  expl=['shared worship builds social solidarity (Durkheim)', 'religious groups provide networks of mutual support', 'religion reinforces shared values'],
                  method='questionnaire', claim='religion promotes social solidarity',
                  counter='Correlation is not causation: sociable people may be more likely to attend; religion may unite insiders but exclude outsiders; self-report.')],
    'essays': [('Explain two functions of religion identified by Durkheim.', 'Social solidarity; reinforcing the collective conscience; sacred and profane; cognitive function (categories of thought); worshipping society through totems.',
                'religion acts as a force for social integration',
                'Durkheim, Malinowski, Parsons, Bellah; examples of shared rituals and civil religion; religion in times of crisis.',
                'Marxism: ideology and division; feminism: patriarchy; religious conflict and fundamentalism; multi-faith societies; secularisation reduces religion’s role; postmodernism: individual choice.')],
})

g21b = T('Marxist views: religion as ideology and the opium of the people')
build(g21b, {
    'terms': [
        ('opium of the people', 'Marx’s description of religion as a comfort that dulls the pain of exploitation without curing it', 'promises of rewards in heaven for the poor'),
        ('ideology', 'a set of ideas that justifies the interests of a powerful group', 'the belief that social positions are ordained by God'),
        ('false consciousness', 'a distorted view of reality that prevents the oppressed from seeing their exploitation', 'accepting poverty as God’s will'),
        ('alienation', 'loss of control and separation from one’s labour and true nature under capitalism', 'workers turning to religion to escape meaningless work'),
        ('divine right of kings', 'the belief that monarchs are appointed by God and must be obeyed', 'medieval kings claiming God-given authority'),
        ('liberation theology', 'a movement in the Catholic Church that used religion to fight poverty and oppression', 'priests supporting peasants in Latin America'),
    ],
    'thinkers': [
        ('Marx', 'religion is the opium of the people, an ideology that legitimates class inequality', 'Marxism',
         'Marx argued religion offers illusory happiness and disguises exploitation, producing false consciousness.',
         'Religion has sometimes inspired revolutionary change.'),
        ('Lenin', 'religion is “spiritual gin” used by the ruling class to keep the working class in its place', 'Marxism',
         'Lenin argued the ruling class uses religion to manipulate the masses.',
         'This treats believers as passive.'),
        ('Maduro', 'religion can be relatively autonomous and support the oppressed', 'Neo-Marxism',
         'Maduro argued clergy can become a source of resistance, as in liberation theology.',
         'Liberation theology declined under pressure from the Vatican.'),
        ('Halévy', 'Methodism helped prevent revolution in nineteenth-century Britain', 'Marxism',
         'Halévy argued Methodism channelled working-class discontent into religion rather than revolution.',
         'Other factors such as reform and rising wages may explain stability.'),
    ],
    'explain': [
        ('Explain two ways in which religion may act as an ideology, according to Marxists.', 'Legitimating inequality as God’s will (divine right, caste); promising rewards in the afterlife; making a virtue of suffering; offering hope of supernatural intervention; diverting attention from exploitation.', '2 marks for each explained way. [4]'),
        ('Explain one criticism of the Marxist view of religion.', 'Religion can inspire change (liberation theology, civil rights); it ignores positive functions; not all religions support the powerful; secularisation reduces religion’s ideological role.', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which religion may legitimate inequality', ['presenting inequality as God’s will', 'promising rewards in heaven', 'making a virtue of suffering', 'divine right of kings', 'teaching acceptance and obedience']),
    ],
    'claims': [
        ('Marx described religion as the opium of the people.', True, 'It dulls the pain of exploitation without removing its causes.'),
        ('Marxists argue religion always encourages revolution.', False, 'Marxists generally see religion as preventing change; neo-Marxists accept it can sometimes inspire resistance.'),
    ],
    'ar': ([('Marx saw religion as a form of ideology.', 'it legitimates inequality and creates false consciousness.'),
            ('Neo-Marxists argue religion can support the oppressed.', 'religious organisations may be relatively autonomous from the ruling class.')],
           ['Marx argued religion reveals the true causes of exploitation.', 'liberation theology supported dictatorships against the poor.']),
    'scen': ['A preacher in {city} tells poor factory workers that their suffering will be rewarded in heaven and that they should obey their employers.',
             'Priests in villages near {city} help landless farmers organise against wealthy landowners, quoting scripture to argue that God sides with the poor.'],
    'views': {'Marxism': 'religion usually acts as ideology: it legitimates class inequality and offers false comfort (“the opium of the people”); where religion is used by the poor against the rich, it shows that religion reflects the class struggle of its society, and Marx saw it as “the sigh of the oppressed creature” (Marx, Lenin).',
              'Neo-Marxism': 'religion is relatively autonomous: it can support ruling-class hegemony, but clergy may side with the oppressed and religion can inspire resistance, as in liberation theology (Maduro, Gramsci).',
              'Functionalism': 'religion integrates society around shared values; whether teaching acceptance or community action, it binds believers together and helps them cope with hardship.',
              'Weberian theory': 'religious ideas can either legitimate the existing order or motivate change; the poor may be drawn to a theodicy of disprivilege, but religious ideas and leaders can also inspire social movements.'},
    'ctx': [('the political views of religious leaders', {'meaning', 'large'}),
            ('how poor communities use religion', {'meaning', 'behaviour', 'hidden'})],
    'methods': REL_M,
    'data': [dict(what='religion and attitudes to inequality', pop='adults', rows=['Agree that inequality is “God’s will”', 'Agree that the poor will be rewarded after death', 'Support protests against poverty'], cols=('Lowest income group', 'Highest income group'), cmp=True, nocount=True,
                  base=[(30, 40), (45, 55), (40, 50)], delta=[(-15, -5), (-20, -10), (-25, -10)], label='religious adults agreeing (%)',
                  leads=['A survey of {n} religious adults in {city} asked about religion and inequality.', '{person} surveyed {n} people who attend religious services in {city}.'],
                  expl=['religion may offer comfort to the poor (opium of the people)', 'beliefs about rewards after death may reduce pressure for change', 'religion can also motivate protest'],
                  method='questionnaire', claim='religion acts as an ideology that discourages the poor from challenging inequality',
                  counter='Many poor believers support protests; survey cannot show cause; attitudes vary between religions; social desirability.')],
    'essays': [('Explain two ways in which religion may legitimate social inequality.', 'Divine right; caste and karma; rewards in the afterlife; virtue of suffering; religion supporting ruling elites.',
                'religion acts mainly as a conservative force that maintains inequality',
                'Marx, Lenin; examples such as caste, divine right, Methodism (Halévy); false consciousness; feminist view of patriarchy.',
                'Weber: Protestant ethic and change; neo-Marxists: liberation theology (Maduro); civil rights; functionalists: integration; secularisation reduces influence.')],
})

g21c = T('Weber and religion as a force for social change')
build(g21c, {
    'terms': [
        ('Protestant ethic', 'Weber’s term for the Calvinist values of hard work, discipline and self-denial that helped create capitalism', 'reinvesting profits instead of spending them'),
        ('spirit of capitalism', 'the rational pursuit of profit for its own sake, which Weber linked to the Protestant ethic', 'continuous reinvestment and careful accounting'),
        ('predestination', 'the Calvinist belief that God has already chosen who will be saved', 'believers anxiously seeking signs of salvation'),
        ('asceticism', 'self-discipline and the denial of pleasure and luxury', 'avoiding gambling, drinking and luxury'),
        ('salvation anxiety', 'the anxiety Calvinists felt because they could not know whether they were saved', 'working hard to show they were among the elect'),
        ('charismatic leadership', 'authority based on the exceptional personal qualities of a leader', 'a prophet inspiring followers to challenge tradition'),
    ],
    'thinkers': [
        ('Weber', 'Calvinist beliefs helped bring about the emergence of modern capitalism', 'Weberian theory',
         'Weber argued predestination created salvation anxiety, leading to hard work, reinvestment and the spirit of capitalism.',
         'Capitalism developed in some Catholic areas and not in some Calvinist ones (Scotland).'),
        ('Bruce', 'religion can act as a resource for social movements', 'Weberian theory',
         'Bruce studied the American civil rights movement, in which black churches provided leaders, meeting places and moral authority.',
         'Religion can also support conservative movements, as with the New Christian Right.'),
        ('Nelson', 'religion has sometimes inspired movements for justice', 'Neo-Marxism',
         'Nelson pointed to religious opposition to apartheid in South Africa and support for civil rights.',
         'Religious groups also supported apartheid.'),
    ],
    'explain': [
        ('Explain Weber’s argument about the Protestant ethic and the spirit of capitalism.', 'Calvinists believed in predestination, causing salvation anxiety; they worked hard, lived ascetically and reinvested profits as a sign of God’s favour, creating the rational spirit of capitalism.', '1 mark predestination; 1 mark anxiety; 1 mark ascetic hard work; 1 mark link to capitalism. [4]'),
        ('Explain two ways in which religion may contribute to social change.', 'Ideas motivating new behaviour (Protestant ethic); religious organisations supporting movements (civil rights, anti-apartheid); liberation theology; charismatic leaders; fundamentalist revolutions.', '2 marks for each explained way. [4]'),
    ],
    'why': [
        ('way', 'ways', 'in which religious organisations helped the civil rights movement (Bruce)', ['providing leaders such as clergy', 'offering meeting places', 'giving moral legitimacy', 'channelling dissent', 'acting as an honest broker', 'mobilising public opinion']),
    ],
    'claims': [
        ('Weber argued Calvinism was the only cause of capitalism.', False, 'Weber saw it as one important cause, alongside material factors.'),
        ('Predestination is the belief that God has already chosen who will be saved.', True, 'This led to salvation anxiety among Calvinists.'),
    ],
    'ar': ([('Weber argued religious ideas can cause social change.', 'Calvinist beliefs encouraged the hard work and reinvestment that helped create capitalism.'),
            ('Black churches helped the civil rights movement.', 'they provided leaders, meeting places and moral authority.')],
           ['Calvinists believed people could earn salvation by buying luxuries.', 'Weber argued religion is always a conservative force.']),
    'scen': ['Members of a strict religious community near {city} work long hours, avoid luxury and reinvest their profits; within two generations they own many of the region’s businesses.',
             'Religious leaders in {city} lead peaceful marches against laws that discriminate against an ethnic minority, using sermons to mobilise support.'],
    'views': {k: VR[k] for k in ('Weberian theory', 'Marxism', 'Neo-Marxism', 'Functionalism')},
    'ctx': [('the role of religious leaders in a protest movement', {'meaning', 'past', 'behaviour'}),
            ('the link between religious values and business success', {'large', 'meaning'})],
    'methods': REL_M,
    'data': [dict(what='religion and social movements', pop='activists', rows=['Attended meetings in a religious building', 'Said religion motivated their involvement', 'Recruited through a religious group'], cols=('Civil rights campaign', 'Environmental campaign'), cmp=True, nocount=True,
                  base=[(65, 80), (55, 70), (45, 60)], delta=[(-50, -35), (-40, -25), (-35, -20)], label='activists (%)',
                  leads=['A survey of {n} activists in two campaigns in {city} produced the results below.', '{person} surveyed {n} activists from two social movements.'],
                  expl=['religious organisations can be a resource for social movements (Bruce)', 'religion motivated civil rights activists', 'newer movements are more secular'],
                  method='questionnaire', claim='religion is an important force for social change',
                  counter='Correlation does not show religion caused change; movements may use churches simply as convenient spaces; samples may be unrepresentative.')],
    'essays': [('Explain two examples of religion contributing to social change.', 'Protestant ethic (Weber); civil rights (Bruce); liberation theology (Maduro); Iranian revolution; anti-apartheid.',
                'religion is a force for social change rather than stability',
                'Weber; Bruce on civil rights; liberation theology; fundamentalist revolutions; religious resistance to dictatorships.',
                'Marx: opium of the people; functionalists: integration and stability; Weber’s evidence criticised (Kautsky: capitalism came first); religion often supports existing order (New Christian Right failure).')],
})

g21d = T('Feminist views of religion and patriarchy')
build(g21d, {
    'terms': [
        ('patriarchy', 'a system of male domination over women', 'only men allowed to become priests'),
        ('religious patriarchy', 'the male domination of religious organisations, teachings and practices', 'scriptures describing women as subordinate to men'),
        ('sacred texts', 'holy writings that are often written and interpreted by men', 'stories blaming women for sin'),
        ('veiling', 'the practice of women covering their hair or face for religious reasons', 'wearing the hijab'),
        ('religious feminism', 'a perspective that seeks gender equality within religion', 'campaigns for the ordination of women'),
    ],
    'thinkers': [
        ('de Beauvoir', 'religion compensates women for their second-class status with the promise of equality in heaven', 'Radical feminism',
         'De Beauvoir argued religion is used by men to control women and give them false hope.',
         'Some women find religion empowering.'),
        ('El Saadawi', 'patriarchal interpretations of religion, rather than religion itself, oppress women', 'Radical feminism',
         'El Saadawi argued male-dominated societies reinterpreted religion to justify women’s subordination.',
         'Others see religion as a source of identity and agency for women.'),
        ('Woodhead', 'women can use religion to gain status and freedom', 'Liberal feminism',
         'Woodhead argued some women choose to wear the hijab as a symbol of liberation and use religion to gain respect.',
         'Radical feminists see this as false consciousness.'),
        ('Armstrong', 'early religions had female goddesses and priestesses before patriarchal monotheism', 'Radical feminism',
         'Armstrong argued women were marginalised as monotheistic religions developed.',
         'Historical evidence is limited.'),
    ],
    'explain': [
        ('Explain two ways in which religion may be patriarchal.', 'Male-dominated leadership and exclusion of women from priesthood; sacred texts written and interpreted by men; rules on women’s dress and sexuality; segregation in places of worship; teachings on women’s domestic roles.', '2 marks for each explained way. [4]'),
        ('Explain one argument that religion may empower women.', 'Women may choose religious practices such as the hijab as a symbol of identity and freedom (Woodhead); religious groups can give women status, networks and support; some religions now ordain women.', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('example', 'examples', 'of patriarchy in religion', ['women excluded from the priesthood', 'segregated seating in places of worship', 'male interpretation of sacred texts', 'restrictions on women’s dress', 'teachings that women should obey husbands', 'women seen as ritually impure']),
    ],
    'claims': [
        ('All feminists see religion as completely oppressive to women.', False, 'Some feminists, such as Woodhead, argue women can use religion to gain status and freedom.'),
        ('Many religions have restricted women from becoming religious leaders.', True, 'For example, women cannot become Catholic priests.'),
    ],
    'ar': ([('Feminists argue many religions are patriarchal.', 'men dominate leadership and the interpretation of sacred texts.'),
            ('Some women choose to wear the veil.', 'it can express religious identity and resistance to Western consumer culture.')],
           ['de Beauvoir argued religion gives women equal power with men on earth.', 'El Saadawi argued religion itself was created by women.']),
    'scen': ['In a place of worship in {city}, women sit separately behind a screen, cannot lead prayers and are expected to dress modestly, while all the leaders are men.',
             '{woman}, a university student in {city}, chooses to wear the hijab, saying it gives her confidence and protects her from being judged on her looks.'],
    'views': {'Radical feminism': VR['Radical feminism'], 'Liberal feminism': 'religion can change: women can gain equality within religious organisations, and some use religion to gain status and freedom (Woodhead).',
              'Functionalism': VR['Functionalism'], 'Postmodernism': VR['Postmodernism']},
    'ctx': [('women’s experiences in religious organisations', {'meaning', 'sensitive', 'hidden'}),
            ('the number of women in religious leadership', {'large', 'change'})],
    'methods': REL_M,
    'data': [dict(what='women in religious leadership', pop='religious leaders', rows=['Organisation A', 'Organisation B', 'Organisation C'], cols=('2000', '2022'), nocount=True, n=[3],
                  base=[(10, 20), (2, 6), (25, 35)], delta=[(8, 18), (0, 3), (5, 15)], label='percentage of religious leaders who are women',
                  leads=['Official figures from three religious organisations in a country near {city} are shown below.', 'The table shows official data on women leaders in three religious organisations.'],
                  expl=['campaigns by religious feminists for equality', 'some organisations now allow women leaders', 'others still exclude women from senior roles'],
                  method='official statistics', claim='religion is becoming less patriarchal',
                  counter='Women remain a minority of leaders; official figures do not show women’s power or experiences; teachings may remain patriarchal.')],
    'essays': [('Explain two feminist views of religion.', 'Radical feminist: religion as patriarchal control (de Beauvoir, El Saadawi); liberal feminist: reform and equality; Woodhead: religion can empower; Armstrong: marginalisation of women.',
                'religion is a patriarchal institution that oppresses women',
                'De Beauvoir, El Saadawi, Armstrong; male leadership; sacred texts; rules on dress and sexuality; fundamentalism and control of women.',
                'Woodhead: hijab as liberation; women ordained in some churches; women more religious than men; religious feminism; postmodern choice; interpretations differ.')],
})

CHAPTERS[21] = [g21a, g21b, g21c, g21d]


g22a = T('Churches, denominations, sects and cults')
build(g22a, {
    'terms': [
        ('church', 'a large, well-established religious organisation with a hierarchy of professional clergy, claiming a monopoly of truth and often linked to the state', 'the Catholic Church'),
        ('denomination', 'a medium-sized religious organisation that accepts society’s values, does not claim a monopoly of truth and is not linked to the state', 'Methodists'),
        ('sect', 'a small, exclusive religious group that rejects wider society, claims a monopoly of truth and often has a charismatic leader', 'Jehovah’s Witnesses in their early years'),
        ('cult', 'a loose, individualistic religious group with no sharp boundaries, offering services such as healing or self-improvement', 'astrology groups or New Age therapies'),
        ('religious pluralism', 'the existence of many different religious organisations in a society', 'churches, mosques, temples and sects in one city'),
        ('universal church', 'Troeltsch’s term for a church that includes all members of society', 'the medieval Catholic Church in Europe'),
    ],
    'thinkers': [
        ('Troeltsch', 'religious organisations can be classified as churches or sects', 'Weberian theory',
         'Troeltsch distinguished large, conservative, inclusive churches from small, radical, exclusive sects.',
         'His typology was based on Christian Europe and may not fit other societies.'),
        ('Niebuhr', 'denominations emerge from sects that have lost their radical edge', 'Weberian theory',
         'Niebuhr described denominations as “sects that have cooled down” and accepted wider society.',
         'Some sects remain sects for many generations.'),
        ('Bruce', 'religious organisations can be classified by whether they claim a monopoly of truth and how they see society', 'Weberian theory',
         'Bruce linked the move from church to denomination and cult to the growth of religious diversity and secularisation.',
         'Typologies simplify very varied groups.'),
        ('Stark and Bainbridge', 'organisations can be classified by their degree of conflict with wider society', 'Religious market theory',
         'They classified churches as low in tension and sects and cults as high in tension with society.',
         'Measuring tension is difficult.'),
    ],
    'explain': [
        ('Explain two differences between a church and a sect.', 'Size (large vs small); relationship with society (accepts vs rejects); leadership (professional hierarchy vs charismatic leader); membership (inclusive vs exclusive, demanding commitment); link with the state.', '2 marks for each explained difference. [4]'),
        ('Explain the difference between a sect and a cult.', 'A sect is exclusive, claims a monopoly of truth and demands strong commitment; a cult is loose and individualistic, tolerates other beliefs and members are more like customers.', '1 mark each; 1 mark contrast. [3]'),
    ],
    'why': [
        ('feature', 'features', 'of a sect', ['small size', 'claims a monopoly of truth', 'rejects or is hostile to wider society', 'charismatic leader', 'strong commitment from members', 'often recruits from the poor or marginalised']),
    ],
    'claims': [
        ('A denomination claims to have a monopoly of religious truth.', False, 'Denominations accept other religious organisations and do not claim a monopoly of truth.'),
        ('Sects are often led by a charismatic leader.', True, 'Authority is based on the leader’s personal qualities.'),
    ],
    'ar': ([('Denominations are sometimes called “sects that have cooled down”.', 'over time sects lose their radical edge and accept wider society (Niebuhr).'),
            ('Cults have low commitment.', 'members are individualistic and often act like customers.')],
           ['churches are usually small, exclusive groups led by a charismatic leader.', 'cults always demand that members cut all ties with wider society.']),
    'scen': ['A group of 60 people near {city} follow a leader who claims to receive messages from God; members live together, give up their possessions and avoid contact with outsiders.',
             'A religious organisation in {city} has millions of members across the country, a hierarchy of professional priests and its leader takes part in state ceremonies.',
             'People in {city} attend weekend workshops on “energy healing”; there is no membership, and many also go to their usual place of worship.'],
    'views': {k: VR[k] for k in ('Weberian theory', 'Marxism', 'Postmodernism', 'Religious market theory')},
    'ctx': [('the daily lives of members of a small sect', {'meaning', 'behaviour', 'hidden'}),
            ('membership of different types of religious organisation', {'large', 'change'})],
    'methods': REL_M,
    'data': [dict(what='religious organisation membership', pop='members', rows=['Churches', 'Denominations', 'Sects and new religious movements'], cols=('1980', '2020'), unit='', uname='thousand members', nocount=True, n=[3],
                  base=[(2500, 3200), (900, 1300), (40, 80)], delta=[(-1400, -800), (-500, -200), (30, 90)], label='membership in a country (thousands)',
                  leads=['Official membership figures for religious organisations in a country near {city} are shown below.', 'The table shows official membership figures for types of religious organisation in one country.'],
                  expl=['secularisation reduces membership of large churches', 'sects offer strong commitment and community', 'religious pluralism increases choice'],
                  method='official statistics', claim='sects are growing while churches decline',
                  counter='Sects remain very small; membership figures may be unreliable; growth from a small base looks large; many people believe without belonging.')],
    'essays': [('Explain two features of a cult.', 'Loose, individualistic; no sharp boundaries; tolerant of other beliefs; customers rather than members; services such as healing and self-improvement; short-lived.',
                'typologies of religious organisations are still useful for understanding religion today',
                'Troeltsch, Niebuhr, Wallis, Stark and Bainbridge; help compare organisations; explain changes (sect to denomination); link to secularisation debate.',
                'Based on Christian Europe; rigid categories; organisations change; globalisation and online religion; postmodern spirituality does not fit; labels such as “cult” are value-laden.')],
})
classify(g22a, [
    ('A large religious organisation in {city} has a hierarchy of professional clergy, claims to be the one true faith and is closely linked to the state.', 'Church', 'large, hierarchical, monopoly of truth, linked to the state.'),
    ('A medium-sized organisation in {city} accepts the values of wider society, tolerates other faiths and has no link with the state.', 'Denomination', 'accepts society, does not claim a monopoly of truth.'),
    ('A small group near {city} follows a charismatic leader, claims to be the only path to salvation and rejects wider society.', 'Sect', 'small, exclusive, high tension with society, monopoly of truth.'),
    ('People in {city} pay for occasional courses in meditation and crystal healing; there is no membership and they hold other beliefs too.', 'Cult', 'loose, individualistic, tolerant, customers rather than members.'),
], ['Church', 'Denomination', 'Sect', 'Cult', 'Civil religion'], 'Which type of religious organisation is described?', C='C3', D=(1, 2), name='org_type')

g22b = T("New religious movements: Wallis's typology")
build(g22b, {
    'terms': [
        ('new religious movement (NRM)', 'a religious or spiritual group of recent origin, outside the mainstream religions', 'the Unification Church or Transcendental Meditation'),
        ('world-rejecting movement', 'an NRM that is highly critical of wider society, demands strong commitment and often requires members to live apart', 'the People’s Temple'),
        ('world-accommodating movement', 'an NRM, often breaking from a mainstream church, that neither accepts nor rejects the world but focuses on religious life', 'neo-Pentecostal groups'),
        ('world-affirming movement', 'an NRM that accepts the world and offers members ways to succeed and fulfil their potential within it', 'Transcendental Meditation or Scientology'),
        ('totalitarian movement', 'a group that controls almost all aspects of members’ lives', 'a commune where the leader controls work, marriage and contact with outsiders'),
    ],
    'thinkers': [
        ('Wallis', 'NRMs can be classified as world-rejecting, world-accommodating or world-affirming according to their relationship with the world', 'Weberian theory',
         'Wallis’s typology is based on how each movement sees wider society.',
         'Some movements change over time or have features of more than one type.'),
        ('Barker', 'claims that NRMs “brainwash” members are exaggerated', 'Interactionism',
         'Barker’s study of the Unification Church (Moonies) found most recruits left within two years and joined by choice.',
         'Some groups do use manipulative techniques.'),
        ('Stark and Bainbridge', 'sects and cults offer compensators for rewards people cannot obtain', 'Religious market theory',
         'They argued the deprived join sects for compensators such as salvation, while cults offer services.',
         'Many NRM members are middle class and not deprived.'),
    ],
    'explain': [
        ('Explain two differences between world-rejecting and world-affirming new religious movements.', 'Attitude to society (hostile vs accepting); commitment (total vs part-time); lifestyle (communal and separate vs normal lives); purpose (salvation or social change vs personal success and fulfilment); recruitment (often young vs often middle-class adults).', '2 marks for each explained difference. [4]'),
        ('Explain one criticism of Wallis’s typology.', 'Movements may fit more than one category or change over time; the typology is based on beliefs rather than what members actually do; members within one movement may relate to the world differently.', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('feature', 'features', 'of world-rejecting new religious movements', ['clear notion of God', 'hostile to wider society', 'members live communally', 'strict rules and total commitment', 'charismatic leader', 'expect radical change in the world']),
    ],
    'claims': [
        ('World-affirming movements ask members to withdraw completely from society.', False, 'World-affirming movements accept society and help members succeed within it.'),
        ('Barker found that most recruits to the Moonies left within two years.', True, 'This challenges claims of brainwashing.'),
    ],
    'ar': ([('World-affirming movements often recruit successful adults.', 'they offer techniques for personal success and fulfilment in everyday life.'),
            ('Barker questioned the brainwashing thesis.', 'most people who attended Moonie workshops did not join, and many who joined later left.')],
           ['world-rejecting movements usually allow members to live ordinary lives without commitment.', 'Wallis classified movements by the number of members they have.']),
    'scen': ['A movement near {city} requires members to give up their jobs, live in a commune, cut contact with their families and prepare for the end of the world.',
             'A movement in {city} offers expensive courses promising to unlock members’ hidden potential and help them succeed at work; members keep their jobs and families.',
             'A group that broke away from a mainstream church in {city} meets for lively worship and speaking in tongues, but members live ordinary lives during the week.'],
    'views': {k: VR[k] for k in ('Weberian theory', 'Marxism', 'Postmodernism', 'Religious market theory')},
    'ctx': [('the experiences of members of a world-rejecting movement', {'meaning', 'hidden', 'sensitive', 'behaviour'}),
            ('who joins new religious movements', {'large', 'meaning'})],
    'methods': REL_M,
    'source': [dict(text='A researcher studied a new religious movement in {city} for six years, attending workshops and interviewing members and ex-members. Of 1,000 people who attended an introductory workshop, 80 joined the movement and only 40 were still members two years later. Most members were young, middle-class graduates.',
                    method='case study', about='recruitment to new religious movements', finds=['only 8% of those attending a workshop joined', 'half of those who joined had left within two years', 'most members were young, middle-class graduates'],
                    persp='Interactionism', pview='The findings support Barker: people choose to join NRMs for their own reasons and many leave, which challenges the idea that members are brainwashed.',
                    claim='people join new religious movements through free choice rather than brainwashing', pro='The source shows low recruitment and high drop-out, as Barker found with the Moonies.',
                    con='Some movements use manipulative techniques; ex-members report pressure; one movement may not be typical; the researcher’s presence may have affected behaviour; middle-class members may still be relatively deprived (Wallis).', flags={'meaning', 'hidden'})],
    'essays': [('Explain two types of new religious movement identified by Wallis.', 'World-rejecting (communal, hostile to society, e.g. People’s Temple); world-accommodating (focus on spiritual life, e.g. neo-Pentecostalism); world-affirming (personal success, e.g. TM).',
                'Wallis’s typology is the most useful way of classifying new religious movements',
                'Clear classification by relationship with the world; explains recruitment and commitment; links to deprivation and social change.',
                'Movements fit several types or change over time; Stark and Bainbridge’s alternative (sects and cults by tension); ignores members’ diverse experiences (Barker); Western bias; postmodern spirituality.')],
})
classify(g22b, [
    ('A movement near {city} requires members to live together, give up their possessions and avoid contact with outsiders.', 'World-rejecting', 'hostile to society, communal life, total commitment.'),
    ('A movement in {city} sells courses that promise to help members unlock their potential and succeed in their careers.', 'World-affirming', 'accepts the world and helps members succeed in it.'),
    ('A group that split from a mainstream church in {city} focuses on lively worship and spiritual renewal, while members keep ordinary jobs.', 'World-accommodating', 'neither accepts nor rejects the world; focuses on religious life.'),
], ['World-rejecting', 'World-affirming', 'World-accommodating', 'Universal church', 'Denomination'], 'Using Wallis’s typology, which type of new religious movement is described?', C='C3', D=(1, 2), name='wallis')

g22c = T('Explaining the growth of sects and New Age movements')
build(g22c, {
    'terms': [
        ('marginality', 'being on the edge of society, excluded from power, status or wealth', 'poor and ethnic minority groups joining sects'),
        ('relative deprivation', 'feeling deprived compared with others, even if not poor', 'middle-class people feeling spiritually empty'),
        ('social change and anomie', 'rapid change that disrupts norms and creates uncertainty, which may lead people to sects', 'urbanisation breaking up traditional communities'),
        ('compensators', 'Stark and Bainbridge’s term for supernatural promises that substitute for rewards people cannot obtain', 'a promise of salvation for the poor'),
        ('sect life cycle', 'the idea that sects either die out or become denominations as they age', 'a sect becoming a denomination in the second generation'),
        ('established sect', 'a sect that survives over generations without becoming a denomination', 'the Amish or Jehovah’s Witnesses'),
    ],
    'thinkers': [
        ('Weber', 'sects appeal to marginal groups by offering a theodicy of disprivilege', 'Weberian theory',
         'Weber argued sects explain the suffering of the disadvantaged and promise salvation.',
         'Many sect members today are middle class.'),
        ('Niebuhr', 'sects are short-lived and either die out or become denominations', 'Weberian theory',
         'Niebuhr argued the second generation lacks commitment and the sect’s puritanism fades as members become prosperous.',
         'Wilson showed some sects survive as established sects.'),
        ('Wilson', 'rapid social change and anomie encourage the growth of sects', 'Weberian theory',
         'Wilson argued disruption of norms leads people to seek certainty in sects.',
         'Some established sects survive for generations.'),
        ('Heelas', 'the New Age appeals to people seeking authenticity and self-improvement in modern society', 'Postmodernism',
         'Heelas argued the New Age offers a source of identity and success in a fragmented world.',
         'Bruce sees New Age beliefs as weak and individual.'),
    ],
    'explain': [
        ('Explain two reasons for the growth of sects.', 'Marginality and theodicy of disprivilege (Weber); relative deprivation (Wallis); social change and anomie (Wilson); compensators (Stark and Bainbridge); search for certainty and community.', '2 marks for each explained reason. [4]'),
        ('Explain Niebuhr’s view of the sect life cycle.', 'Sects are short-lived: the second generation lacks the founders’ commitment; members become prosperous and accept society; the leader dies; so sects either die out or become denominations.', '1 mark each point up to 3. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'for the growth of New Age movements', ['search for authenticity', 'focus on self-improvement and success', 'decline of traditional authority', 'consumer culture and choice', 'disillusionment with organised religion', 'globalisation spreading Eastern practices']),
    ],
    'claims': [
        ('Niebuhr argued sects usually last unchanged for many generations.', False, 'He argued sects either die out or become denominations.'),
        ('Wilson linked the growth of sects to rapid social change.', True, 'Anomie leads people to seek certainty in sects.'),
    ],
    'ar': ([('Sects often appeal to marginalised groups.', 'they offer an explanation of suffering and a promise of salvation (theodicy of disprivilege).'),
            ('The New Age appeals to some middle-class people.', 'it offers self-improvement and a sense of authenticity.')],
           ['Wilson argued that all sects become denominations within one generation.', 'compensators are material rewards such as higher wages.']),
    'scen': ['After factories near {city} close, unemployment rises sharply; within five years, several new sects attract hundreds of members from the area.',
             'Professionals in {city} pay to attend weekend retreats that combine yoga, life coaching and Buddhist meditation, saying they want to “find their true selves”.'],
    'views': {k: VR[k] for k in ('Weberian theory', 'Marxism', 'Postmodernism', 'Religious market theory')},
    'ctx': [('why people join sects', {'meaning', 'hidden'}),
            ('the growth of New Age activities', {'large', 'change'})],
    'methods': REL_M,
    'data': [dict(what='membership of sects', pop='members', rows=['Unemployed or in low-paid work', 'Recently moved to the city', 'Have a university degree'], cols=('Sect members', 'General population'), cmp=True, nocount=True,
                  base=[(35, 50), (25, 35), (15, 25)], delta=[(-25, -15), (-18, -10), (5, 15)], label='percentage in each group',
                  leads=['A survey of {n} members of sects in {city} was compared with census data for the city.', '{person} surveyed {n} sect members in {city} and compared them with the general population.'],
                  expl=['sects attract the marginalised (Weber)', 'migration and social change create anomie (Wilson)', 'graduates may be more attracted to cults and New Age movements'],
                  method='questionnaire', claim='deprivation explains why people join sects',
                  counter='Many sect members are not deprived; relative deprivation is hard to measure; sect members may not be representative; correlation is not causation.')],
    'essays': [('Explain two reasons for the growth of New Age movements.', 'Authenticity and self-spirituality (Heelas); detraditionalisation; consumer choice; postmodernity; relative deprivation of the middle class.',
                'deprivation is the main reason for the growth of sects and cults',
                'Weber’s marginality; Glock and Stark’s types of deprivation; Wallis’s relative deprivation; compensators (Stark and Bainbridge).',
                'Social change and anomie (Wilson, Bruce); postmodernity and choice (Heelas); middle-class recruitment (Barker); religious market theory; social networks.')],
})

CHAPTERS[22] = [g22a, g22b, g22c]


g23a = T('Gender and religious participation')
build(g23a, {
    'terms': [
        ('religious participation', 'taking part in religious activities such as attendance, prayer and membership', 'attending services weekly'),
        ('gendered religiosity', 'differences between men and women in religious belief and practice', 'women praying more often than men'),
        ('socialisation explanation', 'the view that women are more religious because they are socialised to be caring, obedient and nurturing', 'girls taught to be submissive and caring'),
        ('structural location', 'the idea that women’s position in society (e.g. less paid work, more caring) increases their religiosity', 'more time for church activities'),
        ('feminisation of the church', 'the growing proportion of women among religious participants and clergy', 'more women than men in church congregations'),
    ],
    'thinkers': [
        ('Miller and Hoffmann', 'women are more religious because of socialisation and lower participation in paid work', 'Liberal feminism',
         'They argued women are socialised to be passive and caring and have more time for religion.',
         'Women’s paid work has increased, but differences remain.'),
        ('Davie', 'women’s closeness to birth and death makes them more religious', 'Postmodernism',
         'Davie argued women’s involvement in childbirth and caring for the sick and dying brings them closer to ultimate questions.',
         'This risks biological determinism.'),
        ('Bruce', 'women are more likely to be involved in New Age movements because of their emphasis on healing and nurturing', 'Weberian theory',
         'Bruce linked women’s interest in the New Age to socialisation into caring roles.',
         'Men are increasingly involved in some spiritual practices.'),
        ('Brierley', 'women’s church attendance is falling faster than men’s', 'Positivism',
         'Brierley’s church census data showed declining female attendance as women’s roles changed.',
         'Women still outnumber men in most congregations.'),
    ],
    'explain': [
        ('Explain two reasons why women may be more religious than men.', 'Socialisation into caring and obedient roles; less involvement in full-time paid work; closeness to birth and death (Davie); compensation for deprivation (Glock and Stark); religion as a source of status and community; New Age emphasis on healing.', '2 marks for each explained reason. [4]'),
        ('Explain one reason why women’s religious participation may be declining.', 'Women’s increased participation in paid work leaves less time and reduces structural location argument; feminist critiques of patriarchal religion; changing gender roles (Brierley).', '1 mark identifying; 2 marks explaining. [3]'),
    ],
    'why': [
        ('reason', 'reasons', 'why women may be attracted to New Age movements', ['emphasis on healing and wellbeing', 'focus on nature and the body', 'more equal roles for women', 'socialisation into caring roles', 'seeking self-fulfilment outside patriarchal religions']),
    ],
    'claims': [
        ('Surveys usually find men are more religious than women.', False, 'Most surveys find women are more religious than men in belief and practice.'),
        ('Davie linked women’s religiosity to their closeness to birth and death.', True, 'Caring roles bring women close to ultimate questions.'),
    ],
    'ar': ([('Women often participate more in religion than men.', 'they are socialised into caring, nurturing roles that fit religious values.'),
            ('Women’s attendance has fallen in some countries.', 'more women now work full time and question patriarchal religion.')],
           ['Brierley found that women’s church attendance is rising faster than men’s.', 'the structural location explanation says women are more religious because they work longer hours.']),
    'scen': ['In a congregation in {city}, two-thirds of regular attenders are women, but all the senior leaders are men.',
             'A survey in {city} finds that women in full-time work attend religious services less often than women who are not in paid work.'],
    'views': {'Liberal feminism': 'gender differences in religiosity result from socialisation and women’s roles; as roles become more equal, differences narrow (Miller and Hoffmann).',
              'Radical feminism': VR['Radical feminism'], 'Postmodernism': VR['Postmodernism'], 'Functionalism': VR['Functionalism']},
    'ctx': [('why women and men attend religious services', {'meaning', 'large'}),
            ('gender differences in religious attendance over time', {'large', 'change'})],
    'methods': REL_M,
    'data': [dict(what='gender and religiosity', pop='adults', rows=['Pray at least weekly', 'Attend services at least monthly', 'Take part in New Age or holistic activities'], cols=('Women', 'Men'), cmp=True, nocount=True,
                  base=[(40, 55), (25, 35), (8, 14)], delta=[(-20, -10), (-12, -5), (-8, -4)], label='adults (%)',
                  leads=['A survey of {n} adults in {city} produced the results below.', '{person} surveyed {n} adults in {city} about religious practice.'],
                  expl=['socialisation of women into caring roles', 'women’s structural location and closeness to birth and death (Davie)', 'New Age emphasis on healing appeals to women'],
                  method='questionnaire', claim='women are more religious than men',
                  counter='Self-report may differ by gender; differences vary by age and religion; men may participate in other forms; one city may be untypical.')],
    'essays': [('Explain two reasons why women participate in religion more than men.', 'Socialisation; structural location; closeness to birth and death; compensation for deprivation; New Age and healing.',
                'gender differences in religious participation are mainly the result of socialisation',
                'Miller and Hoffmann; caring and obedient roles; New Age healing (Bruce); feminisation of congregations.',
                'Structural location and paid work; closeness to birth and death (Davie); deprivation (Glock and Stark); differences narrowing (Brierley); varies by religion and ethnicity.')],
})

g23b = T('Ethnicity, religion and identity')
build(g23b, {
    'terms': [
        ('cultural defence', 'the use of religion to unite a community and defend its culture against an external threat', 'religion uniting Poles against communist rule'),
        ('cultural transition', 'the use of religion to help migrants adjust to a new society', 'churches supporting new arrivals'),
        ('religious identity', 'a sense of self based on membership of a religious group', 'young people describing themselves as Muslim first'),
        ('diaspora religion', 'religion practised by communities living outside their homeland', 'Hindu temples in cities across the world'),
        ('resurgence of religion', 'a revival in religious commitment, often among minority groups', 'second-generation migrants becoming more observant'),
    ],
    'thinkers': [
        ('Bruce', 'religion is important for minority ethnic groups for cultural defence and cultural transition', 'Weberian theory',
         'Bruce argued religion offers support and a sense of identity in a hostile environment.',
         'Second and third generations may become less religious.'),
        ('Herberg', 'religion helped immigrants in the USA through cultural transition', 'Functionalism',
         'Herberg found first-generation immigrants used religion to adjust and build community.',
         'Once integrated, later generations relied less on religion.'),
        ('Modood', 'religion is a key part of identity for many minority ethnic groups', 'Interactionism',
         'Modood found religion was more important to the identity of South Asian groups than to white groups in Britain.',
         'Religious practice declined among younger people.'),
        ('Pryce', 'religion can help minority groups cope with racism and deprivation', 'Functionalism',
         'Pryce found Pentecostalism helped African-Caribbean people in Bristol adapt and gave them hope.',
         'Rastafarianism offered resistance rather than adaptation.'),
    ],
    'explain': [
        ('Explain the difference between cultural defence and cultural transition.', 'Cultural defence: religion unites a community and defends its identity against a threat (e.g. Poland); cultural transition: religion helps migrants adjust to a new society by providing support and community (Herberg).', '1 mark each; 1 mark contrast. [3]'),
        ('Explain two reasons why religion may be important for minority ethnic groups.', 'Cultural defence; cultural transition; identity and belonging; community support and networks; coping with racism and deprivation; maintaining links with the homeland.', '2 marks for each explained reason. [4]'),
    ],
    'why': [
        ('function', 'functions', 'religion may serve for migrant communities', ['providing community and support', 'maintaining cultural identity', 'helping people cope with racism', 'offering practical help such as language classes', 'keeping links with the homeland']),
    ],
    'claims': [
        ('Bruce argued that religion has no importance for minority ethnic groups.', False, 'He argued religion offers cultural defence and transition.'),
        ('Some studies find minority ethnic groups are more religious than the majority population.', True, 'Modood found religion was central to the identity of many South Asian groups.'),
    ],
    'ar': ([('Religion can help migrants adjust to a new society.', 'religious organisations provide community, support and practical help (cultural transition).'),
            ('Some second-generation migrants become more religious.', 'religion offers a clear identity in response to racism and exclusion.')],
           ['cultural defence means abandoning one’s religion to fit into a new society.', 'Herberg found later generations of immigrants relied more on religion than the first generation.']),
    'scen': ['A temple in {city} runs language classes, helps new migrants find work and holds festivals that bring the community together.',
             '{woman}, born in {city} to migrant parents, has become more religious than her parents; she says that facing racism made her proud of her faith.'],
    'views': {'Functionalism': 'religion integrates minority communities and helps migrants through cultural transition (Herberg).',
              'Marxism': 'religion may comfort minorities facing racism and deprivation but diverts them from challenging inequality.',
              'Interactionism': 'religion is a source of identity negotiated in interaction, especially in response to labelling and exclusion (Modood).',
              'Postmodernism': 'young people combine religious and other identities, choosing how far religion matters to them.'},
    'ctx': [('the role of religion in young people’s identities', {'meaning', 'young', 'sensitive'}),
            ('religious attendance among different ethnic groups', {'large'})],
    'methods': REL_M,
    'data': [dict(what='religion and identity', pop='adults', rows=['Say religion is “very important” to them', 'Attend a place of worship weekly', 'Describe religion as central to their identity'], cols=('First generation', 'Second generation'), cmp=True, nocount=True,
                  base=[(65, 80), (45, 60), (55, 70)], delta=[(-20, -5), (-25, -10), (-10, 5)], label='minority ethnic adults (%)',
                  leads=['A survey of {n} minority ethnic adults in {city} compared migrants with their children born in the country.', '{person} surveyed {n} minority ethnic adults in {city}.'],
                  expl=['cultural transition is less needed by the second generation (Herberg)', 'religion remains a source of identity, especially in response to racism (cultural defence)', 'practice declines faster than identity'],
                  method='questionnaire', claim='religion is declining among the second generation',
                  counter='Religious identity remains strong; practice may change rather than decline; different groups vary; social desirability.')],
    'essays': [('Explain two ways in which religion may help minority ethnic groups.', 'Cultural defence; cultural transition; community support; identity; coping with racism; links with homeland.',
                'religion is more important to minority ethnic groups than to the majority population',
                'Modood; Bruce’s cultural defence and transition; Herberg; Pryce; religion and identity among second generation.',
                'Religiosity declines over generations; variation between groups; some white groups are also religious; postmodern choice; secularisation affects all groups.')],
})

g23c = T('Social class and religiosity')
build(g23c, {
    'terms': [
        ('theodicy of disprivilege', 'Weber’s term for a religious explanation of the suffering of the poor and a promise of future reward', 'a sect promising salvation to the poor'),
        ('theodicy of good fortune', 'a religious justification of the privileges of the wealthy', 'the rich seeing wealth as a sign of God’s favour'),
        ('social deprivation', 'lack of status, power and prestige', 'unemployed people seeking status in a religious group'),
        ('economic deprivation', 'lack of money and material resources', 'poor people joining sects that promise rewards'),
        ('ethical deprivation', 'a feeling that society’s values are wrong', 'middle-class people joining movements that reject materialism'),
    ],
    'thinkers': [
        ('Weber', 'different classes are attracted to different religious ideas and organisations', 'Weberian theory',
         'Weber argued the poor are drawn to a theodicy of disprivilege and the wealthy to religions that justify their position.',
         'Class and religiosity patterns vary between societies.'),
        ('Glock and Stark', 'different types of deprivation lead people to different religious organisations', 'Weberian theory',
         'They identified economic, social, organismic, ethical and psychic deprivation.',
         'Deprivation is hard to measure and many deprived people are not religious.'),
        ('Marx', 'religion offers the working class false comfort and legitimates class inequality', 'Marxism',
         'Marx argued religion is the opium of the people.',
         'In many Western societies the middle class attend church more than the working class.'),
    ],
    'explain': [
        ('Explain two reasons why social class may affect religiosity.', 'The poor may seek a theodicy of disprivilege or compensators; the middle class may attend for status and respectability; class differences in education and secularism; middle-class relative deprivation and New Age.', '2 marks for each explained reason. [4]'),
        ('Explain Weber’s idea of a theodicy of disprivilege.', 'A religious explanation of why the poor suffer, promising that their suffering will be rewarded in the afterlife; this attracts the disadvantaged, especially to sects.', '1 mark meaning; 1 mark development; 1 mark link to class. [3]'),
    ],
    'why': [
        ('type', 'types', 'of deprivation identified by Glock and Stark', ['economic deprivation', 'social deprivation', 'organismic deprivation', 'ethical deprivation', 'psychic deprivation']),
    ],
    'claims': [
        ('In many Western countries, middle-class people are more likely to attend church than working-class people.', True, 'Church attendance is often linked to status and respectability.'),
        ('Weber argued that all classes are attracted to the same religious ideas.', False, 'He argued different classes are attracted to different religious ideas.'),
    ],
    'ar': ([('Sects often attract poorer people.', 'they offer a theodicy of disprivilege explaining and compensating for suffering.'),
            ('Some middle-class people join world-affirming movements.', 'they offer techniques for personal success and fulfilment.')],
           ['Glock and Stark identified only one type of deprivation.', 'a theodicy of good fortune explains the suffering of the poor.']),
    'scen': ['In a wealthy district of {city}, the established church is full every Sunday, while in a poor district nearby, small Pentecostal churches meet in rented halls.',
             'Unemployed workers in {city} join a sect that promises that the poor will inherit the earth when the current world ends.'],
    'views': {k: VR[k] for k in ('Marxism', 'Weberian theory', 'Functionalism', 'Postmodernism')},
    'ctx': [('why people in poorer areas join small churches', {'meaning', 'hidden'}),
            ('religious attendance by social class', {'large'})],
    'methods': REL_M,
    'data': [dict(what='class and religious attendance', pop='adults', rows=['Attend an established church', 'Attend a sect or Pentecostal church', 'Take part in New Age activities'], cols=('Middle class', 'Working class'), cmp=True, nocount=True,
                  base=[(18, 25), (3, 6), (6, 10)], delta=[(-12, -6), (3, 8), (-5, -2)], label='adults (%)',
                  leads=['A survey of {n} adults in {city} produced the results below.', '{person} surveyed {n} adults in {city} about religious participation by social class.'],
                  expl=['middle-class people attend established churches for status and respectability', 'sects offer a theodicy of disprivilege to the poor (Weber)', 'middle-class relative deprivation and New Age'],
                  method='questionnaire', claim='religious participation differs by social class',
                  counter='Class categories are crude; differences may reflect ethnicity or age; self-report; most people of all classes do not attend.')],
    'essays': [('Explain two ways in which social class may influence religious participation.', 'Theodicies of disprivilege and good fortune (Weber); deprivation types (Glock and Stark); middle-class respectability; New Age and relative deprivation.',
                'social class is the most important factor affecting religious participation',
                'Weber, Glock and Stark, Marx; class patterns in churches, sects and New Age; deprivation theories.',
                'Gender and ethnicity also strongly influence religiosity; age and generation (Voas and Crockett); secularisation affects all classes; global variations.')],
})

CHAPTERS[23] = [g23a, g23b, g23c]


g24a = T('Evidence for secularisation: decline in practice and institutional influence')
build(g24a, {
    'terms': [
        ('secularisation', 'the process by which religious thinking, practices and institutions lose social significance (Wilson)', 'falling church attendance and religious influence on law'),
        ('disengagement', 'the withdrawal of religious institutions from wider society and the state', 'churches losing control over education and welfare'),
        ('structural differentiation', 'Parsons’s term for the process by which specialised institutions take over functions once performed by religion', 'the state providing education and welfare'),
        ('rationalisation', 'Weber’s term for the replacement of religious and magical ways of thinking by rational, scientific ones', 'using medicine rather than prayer to cure illness'),
        ('disenchantment', 'Weber’s term for the loss of belief in magical and supernatural forces', 'natural events explained by science, not spirits'),
        ('religious diversity', 'the existence of many religious organisations, which Bruce argues undermines the plausibility of any one religion', 'many competing faiths in one city'),
    ],
    'thinkers': [
        ('Wilson', 'secularisation is the process by which religion loses its social significance', 'Weberian theory',
         'Wilson used falling church attendance and membership in Britain as key evidence.',
         'Martin argues attendance figures do not measure belief.'),
        ('Bruce', 'religious diversity, rationalisation and social fragmentation undermine religion', 'Weberian theory',
         'Bruce argued diversity makes religious beliefs less plausible and that spirituality is too weak to replace religion.',
         'Religious market theorists argue diversity increases religiosity.'),
        ('Weber', 'rationalisation and disenchantment undermine religious worldviews', 'Weberian theory',
         'Weber argued the Protestant Reformation began a process of rationalisation that led to scientific thinking.',
         'Religion persists alongside science for many people.'),
        ('Parsons', 'structural differentiation reduces the functions of religion', 'Functionalism',
         'Parsons argued that as society develops, specialised institutions take over religion’s functions.',
         'Religion may still provide meaning and identity.'),
    ],
    'explain': [
        ('Explain two types of evidence used to support the secularisation thesis.', 'Falling attendance and membership; decline in religious marriages and baptisms; reduced influence on law, education and politics (disengagement); fewer clergy; decline of belief in surveys (Voas and Crockett).', '2 marks for each explained type of evidence. [4]'),
        ('Explain what Weber meant by rationalisation and disenchantment.', 'Rationalisation: replacement of religious and magical thinking with rational, scientific thought and calculation; disenchantment: the world is no longer seen as controlled by supernatural forces.', '1 mark each; 1 mark link to secularisation. [3]'),
    ],
    'why': [
        ('cause', 'causes', 'of secularisation', ['rationalisation and science', 'structural differentiation', 'religious diversity', 'social and cultural diversity', 'individualism', 'urbanisation weakening community']),
    ],
    'claims': [
        ('Wilson defined secularisation as the growth of religion in modern society.', False, 'He defined it as the loss of social significance of religion.'),
        ('Structural differentiation means other institutions take over functions of religion.', True, 'For example, the state provides education and welfare.'),
    ],
    'ar': ([('Church attendance has fallen in many Western countries.', 'religion has lost social significance in modern societies.'),
            ('Bruce argues religious diversity weakens religion.', 'when many religions compete, none can claim to be absolutely true.')],
           ['Weber argued disenchantment increases belief in magic.', 'disengagement means religious institutions taking more control over the state.']),
    'scen': ['In {city}, religious weddings have fallen from 70% to 20% of all weddings in forty years, and most schools that were once run by churches are now run by the state.',
             'A government near {city} legalises divorce and same-sex marriage despite opposition from religious leaders, and removes religious education from the national curriculum.'],
    'views': {'Weberian theory': 'rationalisation, disenchantment and religious diversity lead to the loss of religion’s social significance (Weber, Wilson, Bruce).',
              'Functionalism': 'structural differentiation means specialised institutions take over religion’s functions, so its role becomes more limited (Parsons).',
              'Postmodernism': 'religion is not disappearing but changing: it becomes individual, private and consumer-based (Davie, Lyon).',
              'Religious market theory': VR['Religious market theory']},
    'ctx': [('changes in religious attendance over fifty years', {'large', 'change', 'past'}),
            ('how religious leaders feel about their declining influence', {'meaning', 'sensitive'})],
    'methods': REL_M,
    'data': [dict(what='religious practice', pop='couples', rows=['Religious weddings (% of weddings)', 'Children baptised or given a religious naming ceremony (%)', 'Adults attending weekly (%)'], cols=('1980', '2020'), nocount=True, n=[3],
                  base=[(55, 70), (50, 65), (12, 20)], delta=[(-40, -25), (-35, -20), (-9, -5)], label='religious practice in a country',
                  leads=['Official statistics on religious practice in a country near {city} are shown below.', 'The table shows official data on religious practice in one country.'],
                  expl=['rationalisation and individualism weaken religious practice', 'religion has lost its role in rites of passage', 'religious diversity reduces plausibility'],
                  method='official statistics', claim='secularisation is taking place',
                  counter='Practice is not the same as belief; believing without belonging; vicarious religion; religion grows in other forms and other parts of the world.')],
    'essays': [('Explain two causes of secularisation.', 'Rationalisation (Weber); structural differentiation (Parsons); religious diversity (Bruce, Berger); social and cultural diversity; individualism.',
                'secularisation is taking place in modern society',
                'Falling attendance, membership, rites of passage (Wilson, Bruce); disengagement; rationalisation; Voas and Crockett on belief.',
                'Believing without belonging and vicarious religion (Davie); religious market theory (Stark and Bainbridge); spiritual revolution; global resurgence and fundamentalism; definitions affect conclusions.')],
})
_reg(g24a, 'C3', (1, 2, 3, 4, 5), 'numerical', g24a_att, 'attendance')

g24b = T('Arguments against secularisation: believing without belonging and religious markets')
build(g24b, {
    'terms': [
        ('believing without belonging', 'Davie’s idea that many people hold religious beliefs but do not attend or belong to religious organisations', 'praying privately but never attending services'),
        ('vicarious religion', 'religion practised by an active minority on behalf of a wider population who approve of it', 'people expecting the church to be there for funerals'),
        ('religious market theory', 'the view that religion is like a market in which competition and choice increase participation', 'many churches competing for members in the USA'),
        ('compensators', 'Stark and Bainbridge’s term for supernatural promises that substitute for rewards people cannot obtain', 'a promise of eternal life'),
        ('existential security theory', 'Norris and Inglehart’s view that religiosity is highest where people feel insecure', 'high religiosity in poor, unstable societies'),
        ('cycle of renewal', 'Stark and Bainbridge’s idea that as old religions decline, new ones emerge', 'new movements growing as churches decline'),
    ],
    'thinkers': [
        ('Davie', 'religion has become privatised: people believe without belonging and practise vicarious religion', 'Postmodernism',
         'Davie argued church attendance is falling but belief and approval of religion remain widespread.',
         'Voas and Crockett show belief is falling too.'),
        ('Stark and Bainbridge', 'competition between religions increases religious participation', 'Religious market theory',
         'They argued the USA has high religiosity because of a free religious market, while state churches in Europe create low participation.',
         'Norris and Inglehart found no link between choice and participation.'),
        ('Norris and Inglehart', 'religiosity depends on existential security, not choice', 'Weberian theory',
         'They argued religion declines where people feel secure, as in wealthy, equal societies.',
         'It focuses on economic security and ignores other sources of religion.'),
        ('Casanova', 'religion is “deprivatising” and returning to public life', 'Postmodernism',
         'Casanova argued religion remains important in public debates and politics.',
         'Its influence may be limited to certain issues.'),
    ],
    'explain': [
        ('Explain what Davie meant by believing without belonging.', 'Many people hold religious beliefs but do not attend services or belong to organisations; religion has become privatised and personal, so falling attendance does not mean falling belief.', '1 mark meaning; 1 mark development; 1 mark link to secularisation. [3]'),
        ('Explain the religious market theory explanation of religiosity.', 'Religion is a market; when there is competition and choice, organisations improve their “products” and meet needs, so participation rises (USA); state monopolies reduce participation (Europe).', '1 mark each point up to 4. [4]'),
    ],
    'why': [
        ('argument', 'arguments', 'against the secularisation thesis', ['believing without belonging', 'vicarious religion', 'growth of spirituality', 'religious market theory', 'religious growth in the developing world', 'growth of fundamentalism']),
    ],
    'claims': [
        ('Stark and Bainbridge argue religious competition reduces participation.', False, 'They argue competition increases participation.'),
        ('Vicarious religion means religion practised by a minority on behalf of others.', True, 'Davie used the example of clergy and churches serving the wider population.'),
    ],
    'ar': ([('Church attendance may underestimate religiosity.', 'many people believe without belonging.'),
            ('Norris and Inglehart criticise religious market theory.', 'they find religiosity depends on existential security rather than choice.')],
           ['religious market theory argues state churches increase participation.', 'vicarious religion means everyone attends church weekly.']),
    'scen': ['In {city}, only 6% of adults attend services weekly, but 55% say they believe in God and thousands attend services after a national tragedy.',
             'In a country near {city} with many competing churches advertising lively services and youth clubs, attendance is far higher than in a neighbouring country with one state church.'],
    'views': {'Postmodernism': VR['Postmodernism'] + ' Belief is privatised: people believe without belonging (Davie).',
              'Religious market theory': VR['Religious market theory'],
              'Weberian theory': 'secularisation is real: rationalisation and diversity reduce plausibility, and private belief is weak (Bruce, Wilson).',
              'Functionalism': VR['Functionalism']},
    'ctx': [('private religious belief among people who do not attend services', {'meaning', 'private'}),
            ('religious participation in countries with different levels of competition', {'large'})],
    'methods': REL_M,
    'data': [dict(what='belief and belonging', pop='adults', rows=['Believe in God', 'Pray at least monthly', 'Attend services at least monthly'], cols=('Aged 65 and over', 'Aged 18-34'), cmp=True, nocount=True,
                  base=[(65, 75), (50, 60), (25, 35)], delta=[(-35, -20), (-30, -20), (-22, -12)], label='adults (%)',
                  leads=['A survey of {n} adults in {city} produced the results below.', '{person} surveyed {n} adults of different ages in {city}.'],
                  expl=['belief remains higher than attendance (believing without belonging)', 'each generation is less religious (Voas and Crockett)', 'religion is becoming more private'],
                  method='questionnaire', claim='believing without belonging shows religion is changing rather than declining',
                  counter='Belief is also much lower among the young; age differences may reflect life stage; self-report; questions on “God” may be understood differently.')],
    'essays': [('Explain two arguments of religious market theory.', 'Competition increases participation; demand for religion is constant; cycle of renewal; compensators; US vs Europe.',
                'religion is changing rather than declining in modern societies',
                'Davie (believing without belonging, vicarious religion); spiritual revolution (Heelas and Woodhead); religious market theory; Lyon’s Jesus in Disneyland; growth of NRMs and Pentecostalism.',
                'Bruce, Wilson: decline of belief and practice; Voas and Crockett; spirituality is weak; Norris and Inglehart: security reduces religiosity.')],
})

g24c = T('Secularisation in a global context')
build(g24c, {
    'terms': [
        ('desecularisation', 'Berger’s term for the resurgence of religion in many parts of the world', 'rapid growth of Pentecostalism in Africa and Latin America'),
        ('existential security', 'a feeling that survival is secure enough to be taken for granted', 'people in wealthy welfare states feeling secure'),
        ('Pentecostalism', 'a fast-growing form of Christianity emphasising personal experience of the Holy Spirit', 'lively worship in Latin American megachurches'),
        ('demographic growth of religion', 'the growth of religious populations through higher birth rates in poorer countries', 'religious populations growing faster than secular ones'),
        ('American exceptionalism', 'the idea that the USA is unusually religious for a rich country', 'high church attendance in the USA'),
    ],
    'thinkers': [
        ('Norris and Inglehart', 'religion declines in secure, wealthy societies but remains strong in poor, insecure ones', 'Weberian theory',
         'Their existential security theory explains why the world as a whole is becoming more religious: poorer populations are growing faster.',
         'The USA is rich but religious.'),
        ('Berger', 'the world is as religious as ever; Europe is the exception', 'Religious market theory',
         'Berger changed his view and argued desecularisation is taking place globally.',
         'Secularisation may still occur as countries develop.'),
        ('Martin', 'Pentecostalism is spreading rapidly in the developing world', 'Weberian theory',
         'Martin argued Pentecostalism encourages discipline and self-improvement, a new Protestant ethic in Latin America.',
         'Growth may slow as these societies develop.'),
        ('Davie', 'Europe’s secularism is unusual compared with the rest of the world', 'Postmodernism',
         'Davie argued there are multiple modernities: modernisation does not necessarily lead to secularisation.',
         'Some countries are becoming more secular as they develop.'),
    ],
    'explain': [
        ('Explain two reasons why religion is growing in many developing countries.', 'Existential insecurity (Norris and Inglehart); population growth; religion as a response to rapid change and urbanisation; Pentecostalism offering support and success (Martin); cultural defence; globalisation of religious movements.', '2 marks for each explained reason. [4]'),
        ('Explain Norris and Inglehart’s existential security theory.', 'Religion meets the need for security; in poor, unequal societies people feel insecure and are more religious; in wealthy, equal societies with welfare states people feel secure and religion declines.', '1 mark each point up to 3. [3]'),
    ],
    'why': [
        ('example', 'examples', 'of religious growth in a global context', ['Pentecostalism in Latin America and Africa', 'Islamic revival in parts of the Middle East and Asia', 'Hindu nationalism in India', 'Christian growth in China', 'evangelical megachurches']),
    ],
    'claims': [
        ('The world as a whole is becoming less religious because populations in religious countries are shrinking.', False, 'Populations in poorer, more religious countries are growing faster, so the world as a whole is becoming more religious.'),
        ('The USA is often seen as an exception to secularisation among rich countries.', True, 'It has high levels of attendance despite its wealth.'),
    ],
    'ar': ([('Secularisation may be mainly a European pattern.', 'religion is growing in many parts of Africa, Asia and Latin America.'),
            ('Norris and Inglehart link religiosity to insecurity.', 'religion offers comfort where survival is uncertain.')],
           ['Berger argued the whole world is rapidly secularising.', 'existential security theory says the most secure societies are the most religious.']),
    'scen': ['In a fast-growing city near {city}, new Pentecostal churches open every month, attracting migrants from rural areas with lively worship and help finding jobs.',
             'A survey compares two countries: in one, with a strong welfare state and high average incomes, 10% of adults say religion is very important; in the other, with high poverty, the figure is 85%.'],
    'views': {'Weberian theory': 'religion declines where people are secure; global religiosity reflects insecurity and population growth (Norris and Inglehart).',
              'Religious market theory': VR['Religious market theory'] + ' Europe is the exception, not the rule (Berger).',
              'Postmodernism': 'there are multiple modernities; religion takes new, global and hybrid forms rather than disappearing (Davie).',
              'Marxism': 'religion grows where poverty and inequality are greatest, offering comfort to the oppressed.'},
    'ctx': [('why rural migrants join Pentecostal churches', {'meaning', 'behaviour'}),
            ('religiosity in countries at different levels of development', {'large'})],
    'methods': REL_M,
    'data': [dict(what='religiosity across countries', pop='adults', rows=['Low-income countries', 'Middle-income countries', 'High-income countries'], cols=('Say religion is “very important”', 'Attend services weekly'), cmp=True, nocount=True, n=[3],
                  base=[(80, 90), (50, 65), (15, 30)], delta=[(-35, -20), (-30, -15), (-12, -5)], label='adults (%)',
                  leads=['International survey data for three groups of countries are shown below.', 'The table shows international survey results on religiosity.'],
                  expl=['existential insecurity in poorer countries (Norris and Inglehart)', 'secularisation in wealthy societies', 'religion provides support where welfare is weak'],
                  method='questionnaire', claim='secularisation is linked to economic development',
                  counter='Exceptions such as the USA and Gulf states; survey questions may mean different things in different cultures; averages hide variation.')],
    'essays': [('Explain two arguments that secularisation is not a global trend.', 'Desecularisation (Berger); Pentecostal growth (Martin); population growth of religious countries; fundamentalism; American exceptionalism; multiple modernities.',
                'secularisation is a Western rather than a global process',
                'Global growth of Pentecostalism, Islam, Christianity in China; existential security; demographic trends; Berger and Davie.',
                'Secularisation occurs as countries develop (South Korea, Latin America in recent years); global spread of secular values; young people less religious worldwide; religion may change form.')],
})

CHAPTERS[24] = [g24a, g24b, g24c]


g25a = T('Religious fundamentalism: causes and features')
build(g25a, {
    'terms': [
        ('fundamentalism', 'a return to the basic or fundamental principles of a religion, often in response to modern change', 'calls for strict application of sacred law'),
        ('literalism', 'interpreting sacred texts as the literal, unchanging word of God', 'reading creation stories as historical fact'),
        ('cosmopolitanism', 'an outlook that embraces diversity, tolerance and openness to change', 'accepting different lifestyles and beliefs'),
        ('resistance identity', 'Castells’s term for a defensive identity formed in reaction to globalisation', 'a group rejecting Western values to defend its traditions'),
        ('project identity', 'Castells’s term for a forward-looking identity that engages with social movements', 'feminist or environmental activism'),
        ('New Christian Right', 'a politically and morally conservative Protestant movement in the USA', 'campaigns against abortion and same-sex marriage'),
    ],
    'thinkers': [
        ('Giddens', 'fundamentalism is a reaction to the uncertainty of late modernity and globalisation', 'Late modernity',
         'Giddens argued fundamentalists seek certainty by returning to tradition, while cosmopolitanism embraces change.',
         'Fundamentalists also use modern technology and media.'),
        ('Bruce', 'fundamentalism arises when traditionalists perceive a threat to their way of life', 'Weberian theory',
         'Bruce distinguished Western fundamentalism (reacting to change within society) from developing-world fundamentalism (reacting to change imposed from outside).',
         'The term is often used negatively and inaccurately.'),
        ('Castells', 'globalisation produces resistance identities, including fundamentalism', 'Transformationalism',
         'Castells argued some groups form defensive identities against global change.',
         'Not all responses to globalisation are defensive.'),
        ('Davie', 'fundamentalism arises from modernity itself, as a reaction to it', 'Postmodernism',
         'Davie argued fundamentalism only makes sense as a response to the modern world.',
         'Fundamentalist groups vary greatly.'),
    ],
    'explain': [
        ('Explain two features of religious fundamentalism.', 'Literal reading of sacred texts; claims of absolute truth; intolerance of other views; aggressive reaction to modernity; use of modern technology; patriarchal values; “us and them” thinking; conservative morality.', '2 marks for each explained feature. [4]'),
        ('Explain the difference between fundamentalism and cosmopolitanism, according to Giddens.', 'Fundamentalism seeks certainty by returning to tradition and rejecting change; cosmopolitanism embraces modern diversity, choice and reflexivity and is tolerant of other views.', '1 mark each; 1 mark contrast. [3]'),
    ],
    'why': [
        ('cause', 'causes', 'of religious fundamentalism', ['reaction to globalisation', 'uncertainty in late modernity', 'perceived threats to traditional values', 'Western influence seen as corrupting', 'failure of secular governments', 'search for a clear identity']),
    ],
    'claims': [
        ('Fundamentalists always reject modern technology.', False, 'Many use the internet, media and modern communications to spread their message.'),
        ('Fundamentalism often involves a literal interpretation of sacred texts.', True, 'Fundamentalists treat texts as the unchanging word of God.'),
    ],
    'ar': ([('Giddens sees fundamentalism as a product of globalisation.', 'rapid change and uncertainty lead some people to seek certainty in tradition.'),
            ('Bruce distinguishes Western and developing-world fundamentalism.', 'they respond to different sources of change.')],
           ['fundamentalism always means tolerance of other religions.', 'Castells argued fundamentalism is a project identity.']),
    'scen': ['A religious movement near {city} uses social media to call for a return to “pure” traditions, opposes women working outside the home and denounces Western films and music.',
             'A conservative religious group in {city} campaigns for schools to teach the literal truth of sacred texts and to ban books it considers immoral.'],
    'views': {'Late modernity': 'fundamentalism is a defensive response to the uncertainty and choice of late modernity and globalisation (Giddens).',
              'Weberian theory': 'fundamentalism arises when traditional groups perceive threats to their values from social change (Bruce).',
              'Transformationalism': 'globalisation creates resistance identities in which some groups defend tradition against global change (Castells).',
              'Marxism': 'fundamentalism grows from poverty, inequality and the effects of global capitalism, offering the oppressed an alternative identity.'},
    'ctx': [('why young people join fundamentalist movements', {'meaning', 'young', 'sensitive', 'hidden'}),
            ('how fundamentalist groups use online media', {'media', 'large'})],
    'methods': REL_M,
    'data': [dict(what='attitudes to religion and change', pop='adults', rows=['Sacred texts should be read literally', 'Religious law should guide national law', 'Globalisation threatens our values'], cols=('Rural residents', 'Urban residents'), cmp=True, nocount=True,
                  base=[(45, 60), (35, 50), (50, 65)], delta=[(-20, -10), (-18, -8), (-15, -5)], label='adults agreeing (%)',
                  leads=['A survey of {n} adults in a country near {city} produced the results below.', '{person} analysed a survey of {n} adults in rural and urban areas.'],
                  expl=['rural areas preserve tradition and feel threatened by change', 'urban areas are more cosmopolitan (Giddens)', 'globalisation is seen as a threat to values'],
                  method='questionnaire', claim='fundamentalism is a reaction to globalisation',
                  counter='Agreement does not mean support for fundamentalist movements; urban residents also agree in large numbers; question wording; correlation is not causation.')],
    'essays': [('Explain two causes of religious fundamentalism.', 'Globalisation and uncertainty (Giddens); perceived threats (Bruce); resistance identity (Castells); failure of secular modernisation; poverty and inequality.',
                'religious fundamentalism is a response to globalisation',
                'Giddens, Castells, Bruce; examples of resistance to Western culture; use of global media; reaction to uncertainty.',
                'Fundamentalism has local political and economic causes; Western fundamentalism reacts to internal change; Davie: response to modernity generally; the term is value-laden and applied unfairly (Islamophobia).')],
})

g25b = T('Religion, globalisation and postmodernity')
build(g25b, {
    'terms': [
        ('religious consumerism', 'treating religion as a product to be chosen and consumed', 'shopping around for a church with the best music'),
        ('spiritual supermarket', 'Lyon’s image of a society in which people pick and mix beliefs from many traditions', 'combining yoga, Buddhism and Christianity'),
        ('televangelism', 'the use of television and other media to spread religious messages', 'preachers broadcasting to millions'),
        ('cyber-religion', 'religion practised or organised online', 'online prayer groups and virtual worship'),
        ('deterritorialisation', 'the separation of religion from particular places', 'a faith community connected online across countries'),
        ('religion online and online religion', 'Helland’s distinction between using the internet to communicate about religion (top-down) and practising religion online (interactive)', 'a church website versus an online prayer community'),
    ],
    'thinkers': [
        ('Lyon', 'religion has relocated to consumption in a postmodern “Jesus in Disneyland”', 'Postmodernism',
         'Lyon showed a religious festival held at Disneyland, illustrating how religion mixes with consumer culture.',
         'Bruce argues consumer religion has little social significance.'),
        ('Hervieu-Léger', 'people have become spiritual shoppers, and religion is now a matter of personal choice', 'Postmodernism',
         'Hervieu-Léger argued collective religious memory has been lost, and people construct their own beliefs.',
         'Many still inherit religion from their families.'),
        ('Helland', 'the internet has created religion online and online religion', 'Postmodernism',
         'Helland distinguished top-down religion online from more democratic online religion.',
         'Most online religious activity supplements rather than replaces offline participation.'),
        ('Nanda', 'religion and globalisation can reinforce each other, as in Hindu nationalism', 'Neo-Marxism',
         'Nanda argued India’s prosperous middle class used Hinduism to legitimate their success and nationalism.',
         'Other studies find globalisation reduces religiosity.'),
    ],
    'explain': [
        ('Explain two ways in which globalisation may affect religion.', 'Spread of religions across borders; global media and televangelism; online religion; diaspora communities; fundamentalist reactions; religious consumerism; hybrid beliefs.', '2 marks for each explained way. [4]'),
        ('Explain what Lyon meant by “Jesus in Disneyland”.', 'Religion has relocated to the sphere of consumption; people pick and mix beliefs from a spiritual supermarket, and religion blends with consumer culture and entertainment.', '1 mark meaning; 1 mark development; 1 mark example. [3]'),
    ],
    'why': [
        ('way', 'ways', 'in which the internet has changed religion', ['online worship services', 'online prayer communities', 'access to sacred texts', 'global networks of believers', 'religious leaders using social media', 'new religious movements recruiting online']),
    ],
    'claims': [
        ('Postmodernists argue religion has become a matter of personal choice.', True, 'People pick and mix beliefs in a spiritual supermarket.'),
        ('Lyon argued religion has completely disappeared in postmodern society.', False, 'He argued it has relocated to the sphere of consumption.'),
    ],
    'ar': ([('Religion is increasingly practised online.', 'the internet allows people to worship and connect with believers anywhere.'),
            ('Postmodernists describe a spiritual supermarket.', 'people choose and combine beliefs from many traditions.')],
           ['Helland argued online religion is always top-down and controlled by leaders.', 'religious consumerism means people inherit religion without any choice.']),
    'scen': ['{woman}, in {city}, joins a live-streamed prayer meeting from a church in another country, follows a Buddhist teacher on social media and attends a local mosque’s open day.',
             'A megachurch in {city} holds services with rock music and coffee shops, broadcasts worldwide online and sells branded books and clothing.'],
    'views': {k: VR[k] for k in ('Postmodernism', 'Weberian theory', 'Religious market theory', 'Marxism')},
    'ctx': [('how people use the internet for religious purposes', {'meaning', 'behaviour', 'media'}),
            ('the content of religious websites', {'media', 'large'})],
    'methods': REL_M,
    'data': [dict(what='online religious activity', pop='adults', rows=['Watched a religious service online', 'Used a prayer or meditation app', 'Followed a religious leader on social media'], cols=('2015', '2023'), nocount=True,
                  base=[(5, 10), (3, 8), (8, 14)], delta=[(10, 20), (5, 12), (5, 12)], label='adults in the last month (%)',
                  leads=['Two surveys, each of {n} adults in {city}, produced the results below.', '{person} compared surveys of {n} adults in {city} about online religious activity.'],
                  expl=['the internet allows religion to be practised anywhere', 'online religion increased during health emergencies', 'postmodern choice and religious consumerism'],
                  method='questionnaire', claim='religion is adapting to globalisation and new media',
                  counter='Online activity may supplement rather than replace attendance; most adults do not take part; self-report; growth may be temporary.')],
    'essays': [('Explain two features of religion in postmodern society.', 'Religious consumerism; spiritual supermarket; online religion; deterritorialisation; individualisation; hybrid beliefs.',
                'globalisation and postmodernity have transformed rather than weakened religion',
                'Lyon; Hervieu-Léger; online religion (Helland); global movements such as Pentecostalism; Nanda on Hindu nationalism.',
                'Bruce: consumer religion is weak, a sign of secularisation; online religion supplements offline; traditional religion still dominant for many; fundamentalist rejection of postmodernity.')],
})

g25c = T('Religion and conflict in a global society')
build(g25c, {
    'terms': [
        ('clash of civilisations', 'Huntington’s claim that future conflicts will be between civilisations defined largely by religion', 'conflict between the West and Islam'),
        ('sectarian conflict', 'conflict between groups within or between religions', 'violence between different branches of a faith'),
        ('religious nationalism', 'the fusion of religious and national identity', 'claims that a nation belongs to one religious group'),
        ('Islamophobia', 'prejudice and hostility towards Muslims', 'media stereotyping all Muslims as extremists'),
        ('ethno-religious conflict', 'conflict in which ethnic and religious identities overlap', 'conflicts where religion marks the boundary between ethnic groups'),
    ],
    'thinkers': [
        ('Huntington', 'conflicts between civilisations, defined largely by religion, will dominate global politics', 'Functionalism',
         'Huntington argued that globalisation makes religious identities more important and that the West faces conflict with other civilisations.',
         'Critics argue civilisations are not unified and most conflicts are within civilisations.'),
        ('Said', 'the clash of civilisations idea is an Orientalist stereotype that creates an “us and them” view', 'Neo-Marxism',
         'Said argued Huntington’s thesis justifies Western hostility to Islam.',
         'Supporters argue it identifies real cultural differences.'),
        ('Armstrong', 'the West’s actions, not religion itself, explain much conflict involving religion', 'Liberal feminism',
         'Armstrong argued fundamentalism is a response to Western intervention and secular modernisation.',
         'Religious ideas themselves may motivate violence.'),
        ('Jones', 'religion is rarely the only cause of conflict; it often overlaps with ethnicity, nationalism and economic interests', 'Weberian theory',
         'Jones argued Huntington ignores divisions within religions and the political causes of conflict.',
         'Religious identity can still intensify conflicts.'),
    ],
    'explain': [
        ('Explain Huntington’s clash of civilisations thesis.', 'The world is divided into civilisations based largely on religion; globalisation brings them into contact and makes religious identities stronger; future conflicts will be between civilisations, especially the West and Islam.', '1 mark each point up to 4. [4]'),
        ('Explain two criticisms of the clash of civilisations thesis.', 'Civilisations are not unified (conflict within them); exaggerates religious differences; Orientalist stereotype (Said); ignores political and economic causes; creates self-fulfilling prophecy; most religious groups coexist peacefully.', '2 marks for each explained criticism. [4]'),
    ],
    'why': [
        ('reason', 'reasons', 'why religion may be linked to conflict', ['competing claims to absolute truth', 'religion marking ethnic and national boundaries', 'political leaders using religion to mobilise support', 'resistance to Western intervention', 'competition for land and resources']),
    ],
    'claims': [
        ('Huntington argued civilisations are defined largely by religion.', True, 'He saw religion as the core of civilisational identity.'),
        ('Said strongly supported Huntington’s clash of civilisations thesis.', False, 'Said criticised it as an Orientalist stereotype.'),
    ],
    'ar': ([('Critics argue religion is rarely the only cause of conflict.', 'religious identities often overlap with ethnic, national and economic interests.'),
            ('Huntington expected more conflict between civilisations.', 'globalisation brings civilisations into contact and strengthens religious identities.')],
           ['Huntington argued religion will become irrelevant to global conflict.', 'Said argued Western images of Islam are always accurate.']),
    'scen': ['In a region near {city}, two communities with different religions fight over land and water; leaders on both sides use religious language to rally support.',
             'After a terrorist attack, some newspapers in {city} describe it as part of a “war between civilisations”, while interfaith groups hold joint vigils.'],
    'views': {'Functionalism': 'religion unites groups internally but can divide societies from one another; clashes may follow civilisational lines (Huntington).',
              'Neo-Marxism': 'the clash of civilisations is an ideology that creates enemies and justifies Western power (Said).',
              'Marxism': 'religious conflict often hides economic causes, such as competition for land, resources and power.',
              'Postmodernism': 'religious identities are fluid and hybrid; global conflict is not simply between fixed religious blocs.'},
    'ctx': [('how members of religious communities view each other in a divided city', {'meaning', 'sensitive', 'hidden'}),
            ('how newspapers report conflicts involving religion', {'media', 'large'})],
    'methods': REL_M,
    'data': [dict(what='religion in media coverage of conflict', pop='articles', rows=['Religion named as the main cause', 'Economic or political causes named', 'Interfaith cooperation mentioned'], cols=('Newspaper X', 'Newspaper Y'), cmp=True, nocount=True, n=[200, 300, 400],
                  base=[(45, 60), (25, 35), (5, 12)], delta=[(-25, -15), (10, 20), (3, 10)], label='articles mentioning each (%)',
                  leads=['A content analysis of {n} articles about a conflict in two newspapers in {city} produced the results below.', '{person} analysed {n} newspaper articles about a regional conflict.'],
                  expl=['some media frame conflict as religious (clash of civilisations)', 'others stress economic and political causes', 'news values favour conflict over cooperation'],
                  method='content analysis', claim='the media exaggerate the role of religion in conflict',
                  counter='Content analysis does not show the real causes of the conflict; categories overlap; two newspapers may not be typical.')],
    'essays': [('Explain two ways in which religion may contribute to conflict.', 'Absolute truth claims; religious nationalism; ethno-religious identity; fundamentalism; clash of civilisations; mobilisation by leaders.',
                'religion is the main cause of conflict in the global society',
                'Huntington’s clash of civilisations; fundamentalism; sectarian and ethno-religious conflicts; religious nationalism.',
                'Said, Armstrong, Jones: political, economic and ethnic causes; conflicts within civilisations; interfaith cooperation; religion as a source of peace and reconciliation; media framing exaggerates religion.')],
})

CHAPTERS[25] = [g25a, g25b, g25c]
