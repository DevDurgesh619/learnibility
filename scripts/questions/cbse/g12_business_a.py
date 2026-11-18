"""CBSE class 12 business studies (NCERT Business Studies XII, 054) families: ch01-ch04, plus `spec()`, a small
line-based parser that turns compact fact text into the dict format of g11_accountancy_kit.facts().

Line format (one fact per line; '-' lines belong to the last L, P or Q header):
    T: term | definition
    L: key | title | contrast key or -          list of points (title reads after 'the')
    - point | explanation
    P: X | Y                                    distinction
    - basis | X text | Y text
    Q: question | option; option; ... | feat key or -     scenarios (answers must be options)
    - scenario | answer | why
    F: feat key | answer | feature; feature; ...
    A: assertion | reason | code | why          Assertion-Reason
    TT: topic                                   true/false topic
    S+: true statement
    S-: false statement
    K: C4 D4 4 | case text | question => answer || question => answer
Scenarios may use {p} {p2} {p3} {his} {He} {he} {him} {f} {f2} {c} {g} (see g11_accountancy_kit.ctx).
"""
from __future__ import annotations

from g11_accountancy_kit import facts

S = 'cbse-g12-business-ch'


def spec(text: str, cat: str = 'concept', **extra) -> dict:
    d = {'cat': cat, 'terms': [], 'lists': [], 'pairs': [], 'scen': [], 'feat': {}, 'ars': [], 'cases': []}
    trues, falses, topic = [], [], None
    cur = None
    for raw in text.strip().splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('- '):
            parts = [p.strip() for p in line[2:].split(' | ')]
            cur.append(tuple(parts))
            continue
        tag, _, rest = line.partition(': ')
        parts = [p.strip() for p in rest.split(' | ')]
        if tag == 'T':
            assert len(parts) == 2, line
            d['terms'].append(tuple(parts))
        elif tag == 'L':
            cur = []
            d['lists'].append((parts[0], parts[1], cur, None if parts[2] == '-' else parts[2]))
        elif tag == 'P':
            cur = []
            d['pairs'].append((parts[0], parts[1], cur))
        elif tag == 'Q':
            cur = []
            d['scen'].append((parts[0], [o.strip() for o in parts[1].split('; ')], cur, None if parts[2] == '-' else parts[2]))
        elif tag == 'F':
            d['feat'].setdefault(parts[0], {})[parts[1]] = [x.strip() for x in parts[2].split('; ')]
        elif tag == 'A':
            assert len(parts) == 4 and parts[2] in 'abcd', line
            d['ars'].append(tuple(parts))
        elif tag == 'TT':
            topic = rest
        elif tag == 'S+':
            trues.append(rest)
        elif tag == 'S-':
            falses.append(rest)
        elif tag == 'K':
            c, dd, mk = parts[0].split()
            qa = [tuple(x.strip() for x in seg.split(' => ')) for seg in parts[2].split(' || ')]
            d['cases'].append((c, dd, int(mk), parts[1], qa))
        else:
            raise ValueError(f'bad line: {line}')
    for (q, pool, items, fk) in d['scen']:
        for it in items:
            assert len(it) == 3 and it[1] in pool, (q, it)
    for (k, t, pts, con) in d['lists']:
        for p in pts:
            assert len(p) == 2, p
    for (x, y, bs) in d['pairs']:
        for b in bs:
            assert len(b) == 3, b
    if topic:
        d['tf'] = (topic, trues, falses)
    d.update(extra)
    return d


# ================================================================ ch01 Nature and significance of management

CH01_ST1 = spec('''
T: Management | The process of getting things done with the aim of achieving goals effectively and efficiently.
T: Effectiveness | Completing the given task on time, that is, achieving the end result.
T: Efficiency | Doing the task correctly and with minimum cost, through optimum use of resources.
T: Organisational objectives | Survival, profit and growth of the organisation.
T: Social objectives | Creating benefit for society, such as using environment-friendly methods and giving employment to disadvantaged sections.
T: Personal objectives | The financial, social and higher-level needs of the people working in the organisation.
L: char | characteristics of management | -
- Goal-oriented process | Management unites the efforts of individuals to achieve the goals of the organisation.
- All-pervasive | Management is used in all organisations, economic, social or political, and at all levels.
- Multidimensional | It covers management of work, people and operations.
- Continuous process | Planning, organising, staffing, directing and controlling are performed continuously.
- Group activity | An organisation is a collection of diverse individuals working towards common goals.
- Dynamic function | Management adapts the organisation to its changing environment.
- Intangible force | It cannot be seen, but its presence is felt in the way the organisation functions.
L: imp | points of importance of management | -
- Helps in achieving group goals | It gives a common direction to individual efforts.
- Increases efficiency | It reduces costs and increases productivity through better planning and control.
- Creates a dynamic organisation | It helps people adapt to change so the organisation stays competitive.
- Helps in achieving personal objectives | Motivation and leadership help individuals meet personal goals while contributing to the organisation.
- Helps in the development of society | It provides good quality products, creates employment and adopts new technology.
Q: Which characteristic of management is highlighted? | Goal-oriented process; All-pervasive; Multidimensional; Continuous process; Group activity; Dynamic function; Intangible force | -
- {f}, a hospital in {c}, a school run by an NGO and a government office all use management to run their work. | All-pervasive | Management is needed in all types of organisations.
- The managers of {f} keep revising the menu as customers in {c} become more health-conscious. | Dynamic function | Management adapts to changes in the environment.
- {p} says the presence of good management at {f} cannot be seen but is felt in its orderly working and satisfied staff. | Intangible force | Management is felt, not seen.
- At {f}, planning, organising, staffing, directing and controlling are performed by managers every day without a break. | Continuous process | The functions are performed continuously.
- {f} brings together engineers, accountants and salespeople with different needs to achieve one target. | Group activity | Diverse individuals work together towards common goals.
- Management at {f} covers work to be done, the people who do it and the operations of production. | Multidimensional | It manages work, people and operations.
- Every activity at {f} is directed towards its target of selling 1 lakh units of {g} this year. | Goal-oriented process | Efforts are united towards stated goals.
Q: Which objective of management is being pursued? | Organisational objectives; Social objectives; Personal objectives; Efficiency objectives | -
- {f} has set a target of a 15% rise in profit and entry into two new states. | Organisational objectives | Profit and growth are organisational objectives.
- {f} uses solar power and employs people with disabilities in its {g} unit. | Social objectives | It creates benefits for society.
- {f} pays competitive salaries and offers recognition and growth to its staff. | Personal objectives | It meets the financial and higher-level needs of employees.
- {f} wants to earn enough revenue to cover its costs and stay in business in a tough market. | Organisational objectives | Survival is a basic organisational objective.
P: effectiveness | efficiency
- meaning | completing the task on time (achieving the result) | completing the task with minimum cost
- focus | end result | resources used
- concern | doing the right task | doing the task right
A: Management is a goal-oriented process. | Every organisation has a set of basic goals that management works to achieve. | a | Both true; R explains A.
A: Management is an intangible force. | Its presence can be felt in the way the organisation functions. | a | Both true; R explains A.
A: Effectiveness and efficiency are the same. | Efficiency is about doing the task with minimum cost. | d | A is false: effectiveness is about completing the task on time; efficiency is about cost. R is true.
A: Management is needed only in business organisations. | Management is all-pervasive. | d | A is false: it is needed in all organisations. R is true.
A: Management is a dynamic function. | Management has to adapt to changes in the environment. | a | Both true; R explains A.
TT: the nature of management
S+: Management is a continuous process.
S+: Management is all-pervasive.
S+: Management aims at both effectiveness and efficiency.
S+: Management is multidimensional.
S-: Management is needed only at the top level.
S-: Management is a tangible force that can be seen.
S-: Efficiency means completing a task on time regardless of cost.
S-: Management is needed only in profit-making organisations.
K: C4 D4 4 | {f}, a {g} maker in {c}, met its production target on time this year, but its costs were 20% higher than budgeted because of wastage. | Was the management effective, efficient or both? Explain. => Effective (target achieved on time) but not efficient (cost was higher than needed). || Why should a manager aim at both? => Achieving the goal is not enough; resources must be used optimally to remain competitive.
K: C4 D5 6 | {p} manages {f}, which supplies {g} across {c}. {He} sets targets that unite all departments, trains staff to adapt to online sales, and helps employees grow in their careers. The firm also runs a free skill centre for local youth. | Identify two characteristics of management in the case. => Goal-oriented process; dynamic function (also group activity). || Identify the three objectives of management being met. => Organisational (targets), personal (career growth), social (skill centre). || State two points of importance of management shown. => Helps achieve group goals; creates a dynamic organisation; helps achieve personal objectives; development of society (any two).
''')

CH01_ST2 = spec('''
T: Science | A systematised body of knowledge that explains general truths through principles based on experimentation and with universal validity.
T: Art | The skilful and personal application of existing knowledge to achieve desired results, acquired through study, observation and experience.
T: Profession | An occupation backed by specialised knowledge and training, with entry restricted by a professional body and a code of conduct.
T: Inexact science | A science whose principles are not universally valid because they deal with human behaviour; management is called this.
T: All India Management Association (AIMA) | The professional association of managers in India, membership of which is not compulsory for managers.
L: art | features of art present in management | -
- Existence of theoretical knowledge | A body of literature on management exists for managers to learn from.
- Personalised application | Each manager applies the knowledge in a personal, unique way.
- Based on practice and creativity | Managers become more skilful through practice and creativity.
L: sci | features of science and their presence in management | -
- Systematised body of knowledge | Management has its own concepts and principles, drawn from many disciplines.
- Principles based on experimentation | Management principles come from observation and repeated experiments, but results are not exact.
- Universal validity | Management principles are not universally valid; they must be modified to suit situations.
L: prof | features of a profession and their presence in management | -
- Well-defined body of knowledge | Management is based on a systematised body of knowledge; this feature is present.
- Restricted entry | Anyone can become a manager without a degree; this feature is absent.
- Professional association | AIMA exists, but membership is not compulsory.
- Ethical code of conduct | AIMA has a code, but it is not binding on all managers.
- Service motive | The basic purpose of management is to achieve organisational goals; service motive is not central.
Q: Which feature is being described? | Existence of theoretical knowledge; Personalised application; Based on practice and creativity; Restricted entry; Professional association; Universal validity | -
- {p} has read many books on management, but applies the ideas in {his} own style while running {f}. | Personalised application | Each manager applies knowledge in a unique way.
- {p} became a better manager after years of practice and creative problem solving at {f}. | Based on practice and creativity | Skill grows with practice and creativity.
- {p} became the manager of {f} without any formal degree in management. | Restricted entry | Entry to management is not restricted, so it is not a full profession.
- Managers in India may join AIMA, but {p} manages {f} without being a member. | Professional association | Membership of the association is not compulsory.
- A principle that worked at {f} in {c} gave poor results when applied unchanged at another firm. | Universal validity | Management principles are not universally valid.
- A great deal of literature on motivation and leadership is available to {p}, a new manager at {f}. | Existence of theoretical knowledge | Management has a body of theoretical knowledge.
P: management as an art | management as a science
- basis | personal skill and creativity | systematised body of knowledge
- application | personalised to the situation | principles applied, but not exactly
- learning | practice and experience | study of principles and experimentation
A: Management is called an inexact science. | It deals with human beings whose behaviour cannot be predicted accurately. | a | Both true; R explains A.
A: Management is not a full-fledged profession. | There is no restriction on entry into management. | a | Both true; R explains A.
A: Management principles have universal validity like those of physics. | Management principles are derived from experimentation. | d | A is false; R is true.
A: Management is an art. | Managers apply their knowledge in a personalised manner. | a | Both true; R explains A.
TT: the nature of management as a science, art and profession
S+: Management has the features of art.
S+: Management is an inexact science.
S+: Entry into management is not restricted by any degree.
S-: Membership of AIMA is compulsory for all managers.
S-: Management principles are exact like those of pure sciences.
S-: Management fulfils all the features of a profession.
S-: Management cannot be learnt from books.
K: C4 D4 4 | {p} has no degree in management but has run {f} in {c} successfully for 15 years. {His} friend {p2}, who has an MBA, says that {p} is not a real manager because management is a profession like medicine. | Do you agree with {p2}? Give reasons. => No. Management does not restrict entry to degree holders, so it is not a full profession; {p} can be a manager. || Which feature of art does {p} show? => Personalised application of knowledge and skill developed through practice and creativity.
K: C4 D5 6 | A principle of motivation that worked well at {f} in {c} failed when its manager applied it unchanged in a unit in another country with a different work culture. | What does this show about management as a science? => Management is an inexact science; principles are not universally valid. || Why is this so? => Management deals with human behaviour, which varies and cannot be predicted exactly. || How should the manager have applied the principle? => By adapting it creatively to the new situation (management as an art).
''')

CH01_ST3 = spec('''
T: Top management | The senior-most executives of an organisation, such as the chairman, chief executive officer and managing director.
T: Middle management | The link between top and lower management, made up of division and department heads.
T: Supervisory management | The foremen and supervisors who directly oversee the work of operative employees.
T: Levels of management | The hierarchy of positions showing the chain of authority and responsibility in an organisation.
T: Operative employees | Workers who perform the actual production or service tasks under supervisors.
L: top | functions of top management | mid
- Integrating diverse elements | Top management coordinates the activities of different departments.
- Formulating overall objectives and strategies | It decides the goals and strategies of the organisation.
- Responsible for welfare and survival | It is accountable to the community and shareholders for the organisation's performance.
- Analysing the business environment | It studies the environment and its implications for survival.
L: mid | functions of middle management | top
- Interpreting policies framed by top management | Middle managers translate policies into departmental plans.
- Ensuring that the department has the necessary personnel | They staff their departments.
- Assigning duties and responsibilities | They allot work to supervisors.
- Motivating employees to achieve objectives | They direct and motivate people below them.
- Co-operating with other departments | They ensure smooth functioning across units.
L: low | functions of supervisory management | -
- Overseeing the efforts of the workforce | Supervisors direct the operative employees.
- Maintaining quality of output | They ensure that work meets quality standards.
- Minimising wastage of materials | They control the use of materials and time.
- Ensuring safety standards | They maintain safety on the shop floor.
- Linking management and workers | They pass on the problems of workers to middle management.
Q: Identify the level of management. | Top management; Middle management; Supervisory management; Operative level | -
- {p}, the managing director of {f}, decides to enter the {g} market in three new states. | Top management | Formulating overall objectives and strategies is a top-level function.
- {p}, the production manager of {f}, interprets the new policy and assigns duties to supervisors. | Middle management | Interpreting policies and assigning duties is a middle-level function.
- {p}, a foreman at {f}, checks the quality of {g} produced and reduces wastage on the shop floor. | Supervisory management | Maintaining quality and reducing wastage is a supervisory function.
- {p}, the CEO of {f}, studies government policy and competition to ensure the survival of the company. | Top management | Responsibility for survival and environment analysis lie with top management.
- {p}, the plant superintendent of {f}, makes sure that each department has enough staff. | Middle management | Ensuring necessary personnel is a middle-level function.
- {p}, a supervisor at {f}, passes on workers' grievances to the department head. | Supervisory management | Supervisors link workers and management.
- {p}, the marketing head of {f}, motivates the sales team to meet the targets set by the board. | Middle management | Motivating employees to achieve objectives is a middle-level function.
P: top management | supervisory management
- position | senior-most executives | lowest level of management
- main concern | objectives, strategies and survival | quality, wastage and work of operatives
- examples | chairman, CEO, managing director | foremen and supervisors
- nature of work | strategic and complex | routine and operational
A: Supervisory management directly oversees operative employees. | Supervisors interact with the actual workforce. | a | Both true; R explains A.
A: Middle management formulates the overall strategy of the organisation. | Middle managers interpret policies framed by top management. | d | A is false: strategy is formulated by top management. R is true.
A: Top management's job is complex and stressful. | It is responsible for the welfare and survival of the organisation. | a | Both true; R explains A.
A: Foremen belong to middle management. | Foremen oversee the work of operatives. | d | A is false: foremen are supervisory management. R is true.
TT: levels of management
S+: The CEO belongs to top management.
S+: Middle management is the link between top and supervisory management.
S+: Supervisors help reduce wastage of materials.
S-: Foremen are part of top management.
S-: Middle management formulates overall objectives.
S-: Supervisors decide the long-term strategy.
S-: Top management directly supervises operative workers.
K: C4 D4 4 | At {f}, the managing director {p} decided to double output. Department head {p2} prepared a departmental plan and arranged extra staff, while supervisor {p3} watched quality and wastage on the shop floor. | Identify the level of management of each person. => {p}: top; {p2}: middle; {p3}: supervisory. || State one more function of the middle level. => Assigning duties, motivating employees, co-operating with other departments (any one).
K: C4 D5 6 | Workers at {f} in {c} complain that their problems never reach the managers, and the quality of {g} has fallen. Department heads blame the board for unclear policies. | Which level is failing to link workers and management? => Supervisory management. || State two functions of that level that seem to be neglected. => Maintaining quality of output; minimising wastage; linking management and workers. || What should top management do about unclear policies? => Formulate clear objectives and policies and integrate departments.
''')

CH01_ST4 = spec('''
T: Planning | Deciding in advance what to do and how to do it.
T: Organising | Assigning duties, grouping tasks, establishing authority and allocating resources required to carry out a plan.
T: Staffing | Finding the right people for the right job.
T: Directing | Leading, influencing, motivating and supervising employees to perform the tasks assigned to them.
T: Controlling | Monitoring organisational performance towards the attainment of goals.
T: Coordination | The process by which a manager synchronises the activities of different departments; the force that binds all other functions of management.
L: coord | characteristics of coordination | -
- Coordination integrates group efforts | It gives a common focus to group effort.
- Coordination ensures unity of action | It acts as the binding force between departments.
- Coordination is a continuous process | It begins at planning and continues till controlling.
- Coordination is an all-pervasive function | It is required at all levels and in all departments.
- Coordination is the responsibility of all managers | Each manager coordinates the work of subordinates.
- Coordination is a deliberate function | It is a conscious effort by the manager.
L: need | reasons why coordination is needed | -
- Growth in size | As the organisation grows, its many employees must be made to work in harmony.
- Functional differentiation | Separate departments must be linked to work towards common goals.
- Specialisation | Specialists tend to think only of their own work and must be coordinated.
Q: Which function of management is being performed? | Planning; Organising; Staffing; Directing; Controlling | -
- {p}, the manager of {f}, decides the sales targets for next year and how they will be achieved. | Planning | Deciding in advance what to do and how.
- {p} divides the work of {f} into departments and fixes who reports to whom. | Organising | Grouping tasks and establishing authority relationships.
- {p} recruits, selects and trains new sales staff for {f}. | Staffing | Finding the right people for the right job.
- {p} motivates and guides the workers of {f} to meet their targets. | Directing | Leading and motivating employees.
- {p} compares actual output of {g} with the standard and takes corrective action. | Controlling | Monitoring performance against standards.
- {p} arranges the machines, materials and people needed for the new {g} line at {f}. | Organising | Allocating resources needed to carry out the plan.
Q: Which characteristic of coordination is highlighted? | Coordination integrates group efforts; Coordination ensures unity of action; Coordination is a continuous process; Coordination is an all-pervasive function; Coordination is the responsibility of all managers; Coordination is a deliberate function | -
- At {f}, the purchase, production and sales departments are linked so that they all work towards one target. | Coordination ensures unity of action | It binds departments into unified action.
- The CEO, department heads and supervisors of {f} all try to harmonise the work of their teams. | Coordination is the responsibility of all managers | Every manager coordinates.
- Coordination at {f} begins with planning and continues till controlling. | Coordination is a continuous process | It is needed at every stage.
- {p}, a manager at {f}, makes a conscious effort to synchronise the work of designers and marketers. | Coordination is a deliberate function | It does not happen automatically.
- Coordination is needed in every department and at every level of {f}. | Coordination is an all-pervasive function | It is needed everywhere.
A: Coordination is the essence of management. | It is needed in all functions of management. | a | Both true; R explains A.
A: Coordination is needed only at the top level. | Coordination is the responsibility of all managers. | d | A is false; R is true.
A: Coordination is a deliberate function. | It does not happen on its own; managers must work at it. | a | Both true; R explains A.
A: Specialisation increases the need for coordination. | Specialists usually feel that only they are qualified to judge their work. | a | Both true; R explains A.
A: Coordination is a separate function of management. | It is the force that binds all the other functions. | d | A is false: it is the essence of management, not a separate function. R is true.
TT: functions of management and coordination
S+: Planning is the first function of management.
S+: Coordination is the essence of management.
S+: Controlling compares actual performance with standards.
S-: Coordination is a separate function of management.
S-: Coordination is needed only in large organisations.
S-: Staffing means grouping tasks into departments.
S-: Directing means monitoring performance against standards.
K: C4 D4 4 | At {f}, the production department made 50,000 units of {g}, but the sales department could sell only 30,000 because it had planned a smaller campaign. Finance had not arranged funds for the extra raw material. | What is lacking at {f}? => Coordination among departments. || Give two reasons why it is needed here. => Functional differentiation (separate departments) and growth in size/specialisation; it ensures unity of action.
K: C4 D5 6 | {p} has just become the manager of {f} in {c}. {He} first decides targets, then groups activities, appoints people, guides them and finally checks results against targets. Throughout, {he} tries to harmonise the work of all departments. | Name in order the functions of management {p} performs. => Planning, organising, staffing, directing, controlling. || What binds these functions together? => Coordination. || State two characteristics of it shown in the case. => Continuous process; deliberate function; responsibility of all managers (any two).
''')

# ================================================================ ch02 Principles of management

CH02_ST1 = spec('''
T: Principle of management | A broad and general guideline for decision-making and behaviour of managers.
T: Universal applicability | The nature of management principles that they apply to all types of organisations, big or small, business or non-business.
T: Flexibility of principles | Management principles can be modified by the manager to suit the situation.
T: Contingent principles | The application of principles depends on the prevailing situation at a particular point of time.
T: Behavioural nature | Principles aim at influencing the behaviour of human beings.
L: nat | points describing the nature of principles of management | sig
- Universal applicability | They apply to all kinds of organisations.
- General guidelines | They guide action but do not give readymade solutions.
- Formed by practice and experimentation | They are developed after experience and research.
- Flexible | They can be modified as per the situation.
- Mainly behavioural | They aim at influencing human behaviour.
- Cause and effect relationship | They establish relationships between cause and effect.
- Contingent | Their application depends on the situation.
L: sig | points of significance of principles of management | nat
- Providing managers with useful insights into reality | They increase managers' knowledge and understanding of situations.
- Optimum utilisation of resources and effective administration | They help managers use resources well and avoid personal prejudice.
- Scientific decisions | Decisions become realistic, balanced and justifiable.
- Meeting changing environment requirements | Principles are flexible and help adapt to change.
- Fulfilling social responsibility | Principles guide managers to meet social responsibilities.
- Management training, education and research | Principles are the base of management knowledge and research.
Q: Which nature of management principles is highlighted? | Universal applicability; General guidelines; Flexible; Mainly behavioural; Contingent; Cause and effect relationship | -
- The same principle of division of work is used by {f}, a hospital and a school in {c}. | Universal applicability | Principles apply to all organisations.
- {p} modifies a principle to suit the small size of {his} {g} unit. | Flexible | Principles can be adapted.
- The principles guide {p} at {f} but do not give a ready solution to every problem. | General guidelines | They are guidelines, not rigid rules.
- {p} applies a principle differently when {f} faces a crisis than in normal times. | Contingent | Application depends on the situation.
- Principles followed at {f} are aimed at shaping how employees behave and cooperate. | Mainly behavioural | They influence human behaviour.
- {p} knows that if unity of command is broken at {f}, confusion among workers will follow. | Cause and effect relationship | Principles relate causes and effects.
A: Principles of management are flexible. | Managers can modify them according to the situation. | a | Both true; R explains A.
A: Principles of management are rigid like the principles of science. | Principles of management deal with human behaviour. | d | A is false; R is true.
A: Principles of management help in management training and research. | They are the basis of management as a discipline. | a | Both true; R explains A.
A: Principles of management give readymade solutions to all problems. | They are general guidelines. | d | A is false; R is true.
TT: principles of management
S+: Principles of management are flexible.
S+: They are general guidelines for managers.
S+: They are developed through practice and experimentation.
S-: They are rigid and cannot be modified.
S-: They apply only to business organisations.
S-: They provide readymade solutions to every problem.
S-: They are the same as techniques of management.
K: C4 D4 4 | {p}, a new manager at {f} in {c}, says that management principles are useless because they do not tell {him} exactly what to do in each situation. | Do you agree? Explain the nature of principles. => No: principles are general guidelines, flexible and contingent; they guide judgement rather than give ready solutions. || State two benefits {he} will get by following them. => Useful insights into reality, scientific decisions, optimum use of resources (any two).
''')

FAYOL = ['Division of work', 'Authority and responsibility', 'Discipline', 'Unity of command', 'Unity of direction',
         'Subordination of individual interest to general interest', 'Remuneration of employees', 'Centralisation and decentralisation',
         'Scalar chain', 'Order', 'Equity', 'Stability of tenure of personnel', 'Initiative', 'Esprit de corps']
CH02_ST2 = spec('''
T: Division of work | Fayol's principle that work is divided into small tasks, each done by a trained specialist, leading to efficient output.
T: Unity of command | Fayol's principle that an employee should receive orders from one superior only.
T: Unity of direction | Fayol's principle that each group of activities with the same objective must have one head and one plan.
T: Scalar chain | Fayol's principle that a formal line of authority runs from the highest to the lowest ranks, with a gang plank allowed for quick communication.
T: Gang plank | A direct link between two employees at the same level in different departments, allowed by Fayol for quick communication in an emergency.
T: Esprit de corps | Fayol's principle that management should promote team spirit, unity and harmony among employees.
T: Equity | Fayol's principle that managers should be kind and just to workers, with no discrimination on the basis of sex, religion, language, caste or nationality.
T: Order | Fayol's principle that there should be a place for everything and everyone, and everything and everyone should be in its place.
Q: Which of Fayol's principles is violated or applied here? | ''' + '; '.join(FAYOL) + ''' | -
- At {f}, a salesman gets instructions from both the sales manager and the finance manager, which confuses him. | Unity of command | An employee should receive orders from one superior only.
- {f} has two separate heads and plans for two units making the same {g} for the same market. | Unity of direction | One head and one plan for activities with the same objective.
- A supervisor at {f} is given responsibility for output but no authority to requisition materials. | Authority and responsibility | Authority and responsibility should be balanced.
- At {f}, workers are paid less than the minimum wage and are unhappy. | Remuneration of employees | Remuneration should be fair and give a reasonable standard of living.
- The manager of {f} keeps changing staff every few months, so no one settles into the job. | Stability of tenure of personnel | Employees should not be moved frequently.
- {p}, a manager at {f}, gives promotions only to people of {his} own region. | Equity | No discrimination; kindness and justice to all.
- Tools at {f} are scattered and workers waste time searching for them. | Order | A place for everything and everything in its place.
- The manager of {f} always says "we" instead of "I" and builds team spirit among workers. | Esprit de corps | Promotes team spirit and unity.
- Workers at {f} are encouraged to suggest new ways of packing {g}, and good suggestions are rewarded. | Initiative | Workers should be encouraged to take initiative.
- At {f}, a manager uses company funds to buy a car for {his} personal use. | Subordination of individual interest to general interest | Organisational interest must come before individual interest.
- A production worker at {f} contacts a sales worker at the same level directly in an emergency, informing their superiors. | Scalar chain | Gang plank allowed within the scalar chain for quick communication.
- At {f}, both the management and workers honour the agreed rules, and penalties are imposed judiciously. | Discipline | Obedience to rules and agreements, with fair penalties.
- {f} divides the making of {g} into small tasks, each done by a trained specialist. | Division of work | Specialisation leads to efficient output.
- Small decisions at {f} are taken by branch managers, while major policy is decided at the head office. | Centralisation and decentralisation | A balance between the two is needed.
L: fy | principles of management given by Henri Fayol | -
- Division of work | Work is divided into small tasks done by trained specialists.
- Authority and responsibility | Authority and responsibility should be in balance.
- Discipline | Obedience to rules and agreements, with good superiors and judicious penalties.
- Unity of command | Each employee receives orders from only one superior.
- Unity of direction | One head and one plan for a group of activities with the same objective.
- Subordination of individual interest to general interest | The interest of the organisation comes first.
- Remuneration of employees | Pay should be just and fair.
- Centralisation and decentralisation | A proper balance between the two is needed.
- Scalar chain | A formal line of authority from top to bottom, with a gang plank for emergencies.
- Order | People and materials should be in their proper places.
- Equity | Kindness and justice to all employees.
- Stability of tenure of personnel | Employees should be retained in their jobs.
- Initiative | Workers should be encouraged to develop and carry out plans.
- Esprit de corps | Team spirit and unity among employees.
P: unity of command | unity of direction
- meaning | an employee receives orders from one superior only | one head and one plan for a group of activities with the same objective
- aim | prevents dual subordination | prevents overlapping of activities
- implication | affects an individual employee | affects the entire organisation
- relation | concerned with the functioning of personnel | concerned with the functioning of departments
A: Unity of command prevents confusion among subordinates. | Each subordinate receives orders from only one superior. | a | Both true; R explains A.
A: Fayol allowed a gang plank in scalar chain. | A gang plank allows quick communication between employees at the same level in an emergency. | a | Both true; R explains A.
A: Unity of direction means that each employee has one boss. | Unity of direction prevents overlapping of activities. | d | A is false: that is unity of command. R is true.
A: Fayol's principle of equity calls for kindness and justice to all workers. | Equity leads to loyalty and devotion of employees. | a | Both true; R explains A.
A: Fayol said centralisation should always be complete. | Fayol favoured a balance between centralisation and decentralisation. | d | A is false; R is true.
TT: Fayol's principles of management
S+: Fayol gave fourteen principles of management.
S+: Unity of command means one subordinate, one superior.
S+: Fayol is called the father of general management.
S-: Fayol is called the father of scientific management.
S-: Unity of direction means each employee gets orders from one boss.
S-: Fayol opposed any form of decentralisation.
S-: Esprit de corps means the place for everything.
K: C4 D4 4 | At {f}, {p} receives orders from both the production head and the quality head, and the two orders often conflict. Meanwhile, two branches selling the same {g} in {c} have different plans and heads. | Identify the two principles violated. => Unity of command (dual orders) and unity of direction (two plans for the same objective). || State one consequence of each violation. => Confusion and indiscipline among workers; overlapping and wastage of resources.
K: C4 D5 6 | The new CEO of {f} in {c} ensured that workers were paid fairly, that no one was transferred frequently, that tools were kept in fixed places, and that staff were rewarded for suggestions. | Identify four of Fayol's principles followed. => Remuneration of employees; stability of tenure of personnel; order; initiative. || Explain how any one of them benefits {f}. => For example, stability of tenure reduces recruitment and training costs and builds loyalty.
''', cat='principle of Fayol')

TAYLOR_T = ['Functional foremanship', 'Standardisation and simplification of work', 'Method study', 'Motion study', 'Time study', 'Fatigue study', 'Differential piece wage system']
CH02_ST3 = spec('''
T: Scientific management | Knowing exactly what you want people to do and seeing that they do it in the best and cheapest way (F.W. Taylor).
T: Science, not rule of thumb | Taylor's principle that methods of work should be developed through scientific enquiry rather than intuition or trial and error.
T: Mental revolution | A complete change in the attitude of management and workers towards each other, from competition to cooperation.
T: Functional foremanship | Taylor's technique of having eight specialist foremen, four in the planning department and four in the production department, to supervise workers.
T: Differential piece wage system | Taylor's wage plan that pays a higher rate per unit to workers who reach the standard output and a lower rate to those who do not.
T: Time study | Determining the standard time taken to perform a well-defined job.
T: Motion study | Studying the movements involved in doing a job to eliminate unnecessary ones.
T: Fatigue study | Determining the amount and frequency of rest intervals needed to complete a task.
L: tp | principles of scientific management | -
- Science, not rule of thumb | Every task should be studied scientifically to find the best method.
- Harmony, not discord | Management and workers should have a cooperative attitude (mental revolution).
- Cooperation, not individualism | Management and workers should cooperate; workers' suggestions should be welcomed.
- Development of each and every person to his or her greatest efficiency and prosperity | Workers should be scientifically selected and trained.
L: plan | specialists under the planning in-charge in functional foremanship | prod
- Route clerk | Specifies the route of production.
- Instruction card clerk | Draws up instructions for workers.
- Time and cost clerk | Prepares time and cost sheets for the job.
- Disciplinarian | Ensures discipline and enforces rules.
L: prod | specialists under the production in-charge in functional foremanship | plan
- Speed boss | Ensures that work is done at the required speed.
- Gang boss | Keeps machines and tools ready for workers.
- Repair boss | Keeps machines in working condition.
- Inspector | Checks the quality of work.
Q: Which technique of scientific management is used? | ''' + '; '.join(TAYLOR_T) + ''' | -
- {f} studies the movements of workers packing {g} and removes unnecessary ones. | Motion study | Eliminating unnecessary movements.
- {f} finds that a worker needs 20 minutes to finish one unit and sets this as the standard. | Time study | Determining the standard time for a job.
- {f} decides that workers should get a 10-minute break every two hours. | Fatigue study | Determining rest intervals.
- {f} pays ₹50 per unit to workers producing the standard 10 units a day and ₹40 per unit to those producing fewer. | Differential piece wage system | Higher rate for efficient workers.
- {f} reduces the varieties of {g} it makes from 25 to 8 and fixes standard sizes. | Standardisation and simplification of work | Eliminating unnecessary diversity and setting standards.
- {f} studies different ways of assembling {g} to find the one best way. | Method study | Finding the one best way of doing a job.
- At {f}, a worker is supervised by eight specialists, each looking after one aspect of the work. | Functional foremanship | Separation of planning and execution with specialist foremen.
Q: Which principle of scientific management is applied? | Science, not rule of thumb; Harmony, not discord; Cooperation, not individualism; Development of each and every person to his or her greatest efficiency and prosperity | -
- Instead of trial and error, {f} uses work studies to find the best way to make {g}. | Science, not rule of thumb | Scientific enquiry replaces rule of thumb.
- The management and workers of {f} treat each other as partners and share the gains of higher output. | Harmony, not discord | Mental revolution creates harmony.
- {f} rewards workers' suggestions that reduce cost and involves them in decisions. | Cooperation, not individualism | Cooperation between management and workers.
- {f} selects workers scientifically and trains them to reach their highest efficiency. | Development of each and every person to his or her greatest efficiency and prosperity | Scientific selection and training.
A: Functional foremanship violates Fayol's principle of unity of command. | Under it, a worker receives orders from eight foremen. | a | Both true; R explains A.
A: Differential piece wage system motivates efficient workers. | It pays a higher rate per unit to those who reach the standard. | a | Both true; R explains A.
A: Taylor believed in rule of thumb. | Taylor recommended scientific enquiry to find the best method. | d | A is false; R is true.
A: Mental revolution is the essence of scientific management. | It changes the attitude of both management and workers towards each other. | a | Both true; R explains A.
A: Time study determines the rest intervals during work. | Fatigue study determines the frequency of rest. | d | A is false: that is fatigue study. R is true.
TT: Taylor's scientific management
S+: Taylor is called the father of scientific management.
S+: Functional foremanship separates planning from execution.
S+: Mental revolution means a change in attitudes of workers and management.
S-: Functional foremanship has six foremen.
S-: Motion study determines the standard time for a job.
S-: Taylor favoured rule of thumb.
S-: The speed boss is under the planning in-charge.
K: C4 D4 4 | {f} pays ₹60 per unit to workers who make at least 12 units of {g} a day and ₹50 per unit to those who make fewer. {p} made 12 units and {p2} made 11 units. | Name the technique and calculate their daily wages. => Differential piece wage system; {p}: 12 × ₹60 = ₹720; {p2}: 11 × ₹50 = ₹550. || How does a difference of one unit affect wages, and why? => ₹170 difference; it rewards efficient workers and motivates others to reach the standard.
K: C4 D5 6 | At {f}, the production manager {p} finds workers make {g} in different ways, take rest whenever they like, and machines often break down. {He} wants to apply scientific management. | Suggest three techniques {he} should use, with a reason for each. => Method study (one best way), fatigue study (planned rest), functional foremanship with a repair boss (machine upkeep); also time study for standards. || Which principle should guide the relationship between {him} and the workers? => Harmony, not discord (mental revolution) and cooperation, not individualism.
''', cat='concept of scientific management')

CH02_ST4 = spec('''
T: Henri Fayol | A French mining engineer, called the father of general management, who gave fourteen principles of management.
T: F.W. Taylor | An American mechanical engineer, called the father of scientific management.
T: General theory of administration | Fayol's approach, focusing on the overall administration of the organisation from the top management's view.
T: Scientific management | Taylor's approach, focusing on productivity at the shop-floor level.
P: Fayol's principles | Taylor's scientific management
- perspective | top-level management | shop-floor level of a factory
- unity of command | strictly followed | not followed (functional foremanship)
- applicability | universal | specialised situations
- basis of formation | personal experience | observations and experimentation
- focus | improving the overall administration | increasing productivity
- personality | practitioner | scientist
- expression | general theory of administration | scientific management
Q: Whose contribution is being described? | Henri Fayol; F.W. Taylor; Both Fayol and Taylor; Neither Fayol nor Taylor | -
- {p} at {f} applies principles that are meant for the overall administration of the company from the top. | Henri Fayol | Fayol's principles take a top-level view.
- {p} at {f} applies time study and motion study on the shop floor. | F.W. Taylor | These are Taylor's techniques.
- {p} insists that each worker at {f} must have only one boss. | Henri Fayol | Unity of command is Fayol's principle.
- {p} employs eight specialist foremen to supervise the workers of {f}. | F.W. Taylor | Functional foremanship is Taylor's technique.
- {p} says that management principles at {f} should improve efficiency and reduce waste. | Both Fayol and Taylor | Both aimed at improving efficiency.
A: Fayol's principles have universal applicability. | They were formed from his personal experience as a manager. | b | Both true; R does not explain universal applicability.
A: Taylor's functional foremanship follows unity of command. | A worker gets orders from eight foremen. | d | A is false; R is true.
A: Taylor's principles were based on experimentation. | Taylor conducted experiments at the shop floor. | a | Both true; R explains A.
A: Fayol and Taylor complement each other. | Fayol focused on top management and Taylor on the shop floor. | a | Both true; R explains A.
TT: Fayol and Taylor
S+: Fayol's principles are based on personal experience.
S+: Taylor's principles are based on observation and experiment.
S+: Fayol's work is called the general theory of administration.
S-: Taylor strictly followed unity of command.
S-: Fayol's focus was the shop-floor worker.
S-: Taylor was a practitioner rather than a scientist.
S-: Fayol gave the differential piece wage system.
K: C4 D4 4 | {p} runs {f}. At the head office {he} follows unity of command and a clear scalar chain, while in the factory {he} uses time study and specialist foremen. | Whose ideas does {he} follow in each place? => Head office: Fayol; factory: Taylor. || Are the two approaches in conflict? => Partly (functional foremanship breaks unity of command) but they complement each other: one for overall administration, one for shop-floor productivity.
K: C4 D5 6 | A student says, "Fayol and Taylor said the same thing; one is enough." | Distinguish the two on three bases. => Perspective (top vs shop floor); unity of command (followed vs not); basis (experience vs experiment); focus (administration vs productivity) (any three). || Why do managers still use both? => They complement each other; Fayol's principles guide overall administration and Taylor's techniques improve operations.
''')

# ================================================================ ch03 Business environment

CH03_ST1 = spec('''
T: Business environment | The totality of all individuals, institutions and other forces that are outside the control of a business enterprise but may affect its performance.
T: Specific forces | Forces such as investors, customers, competitors and suppliers that directly affect the operations of a firm.
T: General forces | Economic, social, political, legal and technological conditions that affect all firms indirectly.
T: First mover advantage | The benefit a firm gets by identifying an opportunity early and using it before competitors.
T: Relativity | The feature that business environment differs from country to country and region to region.
L: feat | features of business environment | imp
- Totality of external forces | It is the sum of all things external to the business.
- Specific and general forces | It includes forces that affect firms directly and indirectly.
- Inter-relatedness | Different forces are closely related to one another.
- Dynamic nature | It keeps changing.
- Uncertainty | Future changes are difficult to predict.
- Complexity | It is difficult to understand the combined effect of many forces.
- Relativity | It differs from place to place.
L: imp | points of importance of business environment | feat
- It enables the firm to identify opportunities and get the first mover advantage | Early identification lets the firm use opportunities before competitors.
- It helps the firm identify threats and early warning signals | The firm can take timely action against threats.
- It helps in tapping useful resources | The firm gets finance, machines and labour from the environment.
- It helps in coping with rapid changes | Scanning the environment helps the firm adapt.
- It helps in assisting in planning and policy formulation | Understanding the environment guides future plans.
- It helps in improving performance | Firms that monitor the environment perform better.
Q: Which feature or importance of business environment is highlighted? | Dynamic nature; Inter-relatedness; Relativity; Uncertainty; Specific and general forces; It enables the firm to identify opportunities and get the first mover advantage; It helps the firm identify threats and early warning signals | -
- Demand for woollen clothes is high in Shimla but low in Chennai. | Relativity | The environment differs from region to region.
- Rising health awareness increased demand for organic food and also led the government to frame new food safety laws. | Inter-relatedness | Social and legal forces are related.
- Customer tastes for {g} have changed three times in five years. | Dynamic nature | The environment keeps changing.
- {f} could not predict that a new technology would make its product obsolete within a year. | Uncertainty | Future changes are hard to predict.
- {f} was the first to launch electric scooters in {c} after spotting rising fuel prices and gained a large market share. | It enables the firm to identify opportunities and get the first mover advantage | Early identification of an opportunity.
- On learning that a foreign brand would enter India, {f} improved its {g} and cut prices in advance. | It helps the firm identify threats and early warning signals | Timely action against a threat.
- {f} is affected both by its suppliers and by the general level of inflation in the economy. | Specific and general forces | Environment includes specific and general forces.
A: Business environment is dynamic. | It keeps changing with changes in technology, consumer tastes and government policy. | a | Both true; R explains A.
A: Business environment is within the control of the business. | Business environment consists of external forces. | d | A is false; R is true.
A: Understanding the business environment helps a firm get the first mover advantage. | It helps identify opportunities early. | a | Both true; R explains A.
A: Business environment is the same in every country. | Business environment differs from place to place. | d | A is false; R is true.
TT: business environment
S+: Business environment consists of forces outside the control of the business.
S+: Business environment is dynamic.
S+: It helps a firm identify threats early.
S-: Business environment is within the control of the firm.
S-: Business environment is the same in all countries.
S-: Business environment never changes.
S-: Only specific forces form part of the business environment.
K: C4 D4 4 | {f}, a {g} company in {c}, noticed early that young customers were shifting to online buying. It launched its own app before rivals and also prepared for a likely rise in competition from foreign firms. | Identify two points of importance of business environment in the case. => Identifying opportunities and first mover advantage; identifying threats and early warning signals. || State two features of business environment it reflects. => Dynamic nature; uncertainty (also inter-relatedness).
''', cat='concept of business environment')

DIMS = ['Economic environment', 'Social environment', 'Technological environment', 'Political environment', 'Legal environment']
CH03_ST2 = spec('''
T: Economic environment | Interest rates, inflation, disposable income, stock market indices and the value of the rupee that affect business.
T: Social environment | Customs, traditions, values, social trends and society's expectations from business.
T: Technological environment | Scientific improvements and innovations that provide new ways of producing goods and services.
T: Political environment | Political conditions, such as general stability and peace in the country and the attitude of elected government representatives towards business.
T: Legal environment | Legislation passed by Parliament, administrative orders, court judgements and decisions of commissions and agencies.
Q: Which dimension of business environment is highlighted? | ''' + '; '.join(DIMS) + ''' | -
- The Reserve Bank of India raised the repo rate, so loans for {f} became costlier. | Economic environment | Interest rates are part of the economic environment.
- Growing interest in fitness has increased demand for gyms and health food in {c}. | Social environment | Social trends are part of the social environment.
- Digital payment apps have reduced the use of cash in shops in {c}. | Technological environment | Innovations change the way business is done.
- A stable government with a pro-business attitude encouraged {f} to invest more. | Political environment | Political stability and attitude affect business.
- A new law requires {f} to print the expiry date and maximum retail price on every pack of its packaged food. | Legal environment | Legislation is part of the legal environment.
- Rising inflation reduced the purchasing power of customers of {f}. | Economic environment | Inflation is an economic factor.
- Customers now expect {f} to use eco-friendly packaging. | Social environment | Society's expectations from business are social factors.
- A court judgement banned the sale of a certain product nationwide. | Legal environment | Court judgements are legal factors.
- 3-D printing allowed {f} to make prototypes of {g} in hours instead of weeks. | Technological environment | New technology changes production.
- A peaceful general election assured foreign investors about the future of {f}. | Political environment | Peace and stability are political factors.
L: dims | dimensions of business environment | -
- Economic environment | Interest rates, inflation, disposable income and stock markets.
- Social environment | Customs, values, trends and expectations of society.
- Technological environment | Scientific improvements and innovations.
- Political environment | Political stability and the government's attitude to business.
- Legal environment | Laws, orders, court judgements and decisions of commissions.
A: An increase in the repo rate is part of the economic environment. | It changes the cost of borrowing for businesses. | a | Both true; R explains A.
A: A change in consumers' food habits is part of the technological environment. | Social trends influence demand. | d | A is false: it is social environment. R is true.
A: Court judgements are part of the legal environment. | They affect what a business may or may not do. | a | Both true; R explains A.
A: Political stability encourages investment. | Investors want an assurance about the future. | a | Both true; R explains A.
TT: the dimensions of business environment
S+: Inflation is part of the economic environment.
S+: Social trends are part of the social environment.
S+: Court judgements are part of the legal environment.
S-: Innovations are part of the political environment.
S-: Interest rates are part of the social environment.
S-: The attitude of the government is part of the technological environment.
S-: Legislation is part of the economic environment.
K: C4 D4 4 | {f} makes packaged {g} in {c}. This year: loans became costlier, customers began demanding sugar-free products, and a new law made front-of-pack nutrition labels compulsory. | Identify the dimension of business environment in each case. => Costlier loans: economic; sugar-free demand: social; labelling law: legal. || How should {f} respond to the social change? => Introduce healthier variants and communicate them to customers.
K: C4 D5 6 | {p} plans to open a chain of electric-vehicle charging stations in {c}. {He} studies fuel prices, government subsidies for EVs, battery technology and people's concern for pollution. | Identify four dimensions of environment {he} is studying, with the factor for each. => Economic (fuel prices); political (government subsidies/attitude); technological (battery technology); social (concern for pollution). || Which point of importance of business environment does this show? => Identifying opportunities and getting the first mover advantage; assisting planning.
''', cat='dimension of business environment')

CH03_ST3 = spec('''
T: Liberalisation | Freeing Indian business and industry from all unnecessary controls and restrictions.
T: Privatisation | Giving a greater role to the private sector in nation building and a reduced role to the public sector.
T: Globalisation | The integration of the various economies of the world, leading towards a global economy.
T: Disinvestment | The transfer of public sector enterprises to the private sector by selling part or all of the government's shares.
T: New Industrial Policy, 1991 | The policy announced in July 1991 that began the process of liberalisation, privatisation and globalisation in India.
T: FEMA, 1999 | The Foreign Exchange Management Act, which replaced the Foreign Exchange Regulation Act (FERA) as part of globalisation.
L: lib | measures of liberalisation under the 1991 reforms | -
- Abolishing licensing in most industries | Licences were needed only for a few industries.
- Freedom in deciding the scale of business | Firms could decide how much to produce.
- Removal of restrictions on the movement of goods and services | Trade became easier across the country.
- Freedom in fixing prices of goods and services | Prices were decided by the market.
- Reduction in tax rates and lifting of unnecessary controls | The economy was opened up.
- Simplifying procedures for imports and exports | Foreign trade became easier.
- Making it easier to attract foreign capital and technology | Foreign investment was encouraged.
L: impact | impacts of government policy changes on business and industry | -
- Increasing competition | Indian firms faced competition from multinational companies.
- More demanding customers | Customers got more choice and wanted better quality.
- Rapidly changing technological environment | Firms had to keep up with new technology.
- Necessity for change | Firms had to change policies and operations quickly.
- Need for developing human resources | Firms needed more competent and committed people.
- Market orientation | Firms began to produce what the market wanted.
- Loss of budgetary support to the public sector | Public enterprises had to become efficient to survive.
Q: Which element of the 1991 reforms is described? | Liberalisation; Privatisation; Globalisation; Demonetisation | -
- The government sold a large part of its shares in a public sector airline to a private company. | Privatisation | Disinvestment transfers ownership to the private sector.
- Industries in {c} no longer need a licence to expand production of {g}. | Liberalisation | Licensing was abolished in most industries.
- Import duties were reduced and foreign firms were allowed to invest in India more freely. | Globalisation | Integration with the world economy.
- FERA was replaced by FEMA in 1999. | Globalisation | FEMA eased foreign exchange rules for an integrated economy.
- Firms were given freedom to fix the prices of their products. | Liberalisation | Freedom in fixing prices.
- Sick public sector units were referred to the Board for Industrial and Financial Reconstruction. | Privatisation | The policy reduced the role of the public sector.
A: Liberalisation abolished licensing for most industries. | Liberalisation aimed at freeing business from unnecessary controls. | a | Both true; R explains A.
A: After 1991, Indian firms faced more competition. | Foreign firms were allowed to enter Indian markets. | a | Both true; R explains A.
A: Privatisation increases the role of the public sector. | Disinvestment transfers ownership to the private sector. | d | A is false; R is true.
A: The New Industrial Policy was announced in July 1991. | It began the process of liberalisation, privatisation and globalisation. | a | Both true; R explains A.
TT: the economic reforms of 1991
S+: The New Industrial Policy was announced in 1991.
S+: FEMA replaced FERA.
S+: Disinvestment is a part of privatisation.
S-: Licensing was made compulsory for all industries in 1991.
S-: Privatisation means a larger role for the public sector.
S-: Globalisation means isolating the economy from the world.
S-: After 1991, Indian firms faced less competition.
K: C4 D4 4 | After the 1991 reforms, {f}, which had been the only maker of {g} in India for years, suddenly faced foreign brands. Its customers began asking for better quality and more features. | Identify two impacts of the policy changes on {f}. => Increasing competition; more demanding customers. || Suggest two steps {f} should take. => Improve technology and quality; become market-oriented and develop its human resources.
K: C4 D5 6 | A student says the reforms of 1991 were only about privatisation. | Explain liberalisation, privatisation and globalisation with one measure each. => Liberalisation: abolition of licensing; privatisation: disinvestment of public sector shares; globalisation: reduction of import duties/FEMA. || State two impacts on business. => Increasing competition, more demanding customers, need for change, market orientation (any two).
''', cat='concept of economic reforms')

CH03_ST4 = spec('''
T: Demonetisation | The withdrawal of the legal tender character of certain currency notes; in India the old ₹500 and ₹1,000 notes ceased to be legal tender from 8 November 2016.
T: Legal tender | Money that must be accepted by law in payment of a debt.
T: Black money | Income on which tax has not been paid and which is kept hidden from the authorities.
T: Less-cash economy | An economy in which more payments are made through digital and banking channels and less in cash.
T: Formalisation of savings | The shift of household savings from cash into banks and other formal financial channels.
L: feat | features of demonetisation | -
- It is a tax administration measure | Cash holdings had to be deposited and could be checked against declared income.
- It is a measure to curb corruption and black money | Unaccounted cash had to be declared or became worthless.
- It aimed at creating a less-cash economy | It encouraged digital payments.
- It channelled savings into the formal financial system | Cash was deposited in banks.
- It aimed at curbing counterfeit currency | Fake notes of the old series lost their value.
L: imp | impacts of demonetisation | -
- Increase in digital transactions | Use of cards, UPI and mobile wallets rose sharply.
- Increase in bank deposits | Old notes were deposited in bank accounts.
- Short-term fall in demand for cash-based goods | Sectors depending on cash, such as real estate and small retail, were hit.
- Fall in real estate prices | Cash transactions in property declined.
- Wider tax base | More income came under the tax net.
Q: Which feature or impact of demonetisation is described? | Increase in digital transactions; Increase in bank deposits; Short-term fall in demand for cash-based goods; It is a measure to curb corruption and black money; It aimed at creating a less-cash economy | -
- Many small shops in {c} started accepting payments through UPI soon after November 2016. | Increase in digital transactions | Digital payments rose.
- Households deposited their old ₹500 and ₹1,000 notes in bank accounts. | Increase in bank deposits | Savings moved into banks.
- Sales at a cash-based wholesale market in {c} fell for a few months. | Short-term fall in demand for cash-based goods | Cash-dependent trade was hit.
- People holding large unaccounted cash had to explain its source or lose it. | It is a measure to curb corruption and black money | Black money was targeted.
- The government promoted cards and mobile wallets so that fewer payments would be made in cash. | It aimed at creating a less-cash economy | Moving towards less cash.
A: Demonetisation was announced in India on 8 November 2016. | The old ₹500 and ₹1,000 notes ceased to be legal tender. | a | Both true; R explains A.
A: Demonetisation increased digital transactions. | People had less cash to make payments. | a | Both true; R explains A.
A: Demonetisation increased the use of cash in the economy. | It aimed at creating a less-cash economy. | d | A is false; R is true.
A: Demonetisation is a tax administration measure. | Cash deposited in banks could be compared with declared incomes. | a | Both true; R explains A.
TT: demonetisation
S+: The old ₹500 and ₹1,000 notes ceased to be legal tender in November 2016.
S+: It led to an increase in digital transactions.
S+: It aimed to curb black money.
S-: It made old ₹100 notes invalid.
S-: It reduced bank deposits.
S-: It was announced in 1991.
S-: It aimed to increase the use of cash.
K: C4 D4 4 | {p} runs a {g} shop in {c} that used to accept only cash. After November 2016 {his} sales fell for a few weeks; {he} then started accepting UPI and card payments and sales recovered. | Identify two impacts of demonetisation in the case. => Short-term fall in demand for cash-based sales; increase in digital transactions. || State two features of demonetisation. => Measure to curb black money and corruption; move towards a less-cash economy; tax administration measure (any two).
''', cat='term')

# ================================================================ ch04 Planning

CH04_ST1 = spec('''
T: Planning | Deciding in advance what to do and how to do it; bridging the gap from where we are to where we want to go.
T: Primary function | Planning is called this because it lays down the base for all other functions of management.
T: Futuristic | Planning is this because it looks ahead and prepares for the future.
T: Mental exercise | Planning is this because it requires application of the mind, foresight and sound judgement.
T: Pervasive | Planning is this because it is required at all levels and in all departments.
L: imp | points of importance of planning | lim
- Planning provides direction | It states in advance how work is to be done.
- Planning reduces the risks of uncertainty | It helps managers anticipate changes.
- Planning reduces overlapping and wasteful activities | It coordinates activities of departments.
- Planning promotes innovative ideas | It requires managers to think of new ideas.
- Planning facilitates decision making | It helps choose the best alternative.
- Planning establishes standards for controlling | It gives the goals against which performance is measured.
L: lim | limitations of planning | imp
- Planning leads to rigidity | Managers may find it hard to change the plan.
- Planning may not work in a dynamic environment | The environment changes in ways the plan cannot foresee.
- Planning reduces creativity | Middle managers only carry out plans made at the top.
- Planning involves huge costs | Time and money are spent on preparing plans.
- Planning is a time-consuming process | Little time may be left for implementation.
- Planning does not guarantee success | Success depends on proper implementation too.
L: feat | features of planning | -
- Planning focuses on achieving objectives | Plans are made to achieve goals.
- Planning is a primary function of management | It precedes all other functions.
- Planning is pervasive | It is required at all levels and in all departments.
- Planning is continuous | Plans are made for a period and new plans follow.
- Planning is futuristic | It looks into the future.
- Planning involves decision making | It requires choosing among alternatives.
- Planning is a mental exercise | It requires thinking and foresight.
Q: Which importance, feature or limitation of planning is highlighted? | Planning provides direction; Planning reduces the risks of uncertainty; Planning establishes standards for controlling; Planning leads to rigidity; Planning involves huge costs; Planning does not guarantee success; Planning is continuous; Planning is pervasive | -
- {f} could not change its sales plan midway even when demand for {g} rose sharply. | Planning leads to rigidity | Fixed plans are hard to change.
- {f} spent ₹5 lakh on market research and experts while preparing its five-year plan. | Planning involves huge costs | Planning is expensive.
- Despite a detailed plan, {f} failed because its staff did not implement it properly. | Planning does not guarantee success | Success depends on implementation too.
- The plan of {f} told every department what to do, so no one was confused about the target. | Planning provides direction | It states in advance what is to be done.
- {f} kept extra stock of raw material because its plan expected a transport strike. | Planning reduces the risks of uncertainty | Managers anticipate changes.
- {f} compares actual sales with the targets in its plan. | Planning establishes standards for controlling | Plans give standards.
- As soon as one annual plan ends, {f} prepares the next. | Planning is continuous | New plans follow old ones.
- Plans are made by top, middle and supervisory managers at {f}. | Planning is pervasive | Planning is required at all levels.
A: Planning is the primary function of management. | It lays down the base for all other functions. | a | Both true; R explains A.
A: Planning guarantees success. | Plans must be implemented properly to succeed. | d | A is false; R is true.
A: Planning may lead to rigidity. | Managers may not be able to change a plan once it is made. | a | Both true; R explains A.
A: Planning is a one-time activity. | Plans are prepared for a specific period. | d | A is false: planning is continuous. R is true.
A: Planning establishes standards for controlling. | Controlling compares actual performance with planned goals. | a | Both true; R explains A.
TT: planning
S+: Planning is the primary function of management.
S+: Planning is futuristic.
S+: Planning can lead to rigidity.
S-: Planning guarantees success.
S-: Planning is needed only at the top level.
S-: Planning is a one-time activity.
S-: Planning increases uncertainty.
K: C4 D4 4 | {f} prepared a detailed three-year plan for its {g} business in {c}. Midway, a new competitor cut prices, but the managers kept following the original plan and lost market share. | Identify two limitations of planning seen here. => Planning leads to rigidity; planning may not work in a dynamic environment. || What should the managers have done? => Reviewed the premises and revised the plan (planning is continuous and must be flexible).
K: C4 D5 6 | {p}, the new manager of {f}, says, "Planning is a waste of time; we should just start working." | Give three points of importance of planning to convince {him}. => Provides direction; reduces risks of uncertainty; reduces overlapping and wasteful activities; facilitates decision making; establishes standards for control (any three). || Which limitation of planning might {p} be thinking of? Explain. => Planning is time-consuming and costly; it may lead to rigidity (any one with explanation).
''')

CH04_ST2 = spec('''
T: Planning premises | The assumptions about the future, such as forecasts of demand, prices and policies, on which plans are based.
T: Forecasting | Estimating future events on the basis of past and present data; it is the base of planning premises.
T: Alternative courses of action | The different ways in which an objective may be achieved, identified during planning.
T: Follow-up action | Monitoring the plan to ensure that it is implemented and objectives are achieved.
L: proc | steps in the planning process | -
- Setting objectives | Objectives are set for the whole organisation and each department.
- Developing premises | Assumptions about the future are made.
- Identifying alternative courses of action | Different ways to reach the objectives are found.
- Evaluating alternative courses | The pros and cons of each alternative are weighed.
- Selecting an alternative | The best plan is chosen.
- Implementing the plan | The plan is put into action.
- Follow-up action | The plan is monitored to see that it is being carried out.
Q: Which step of the planning process is described? | Setting objectives; Developing premises; Identifying alternative courses of action; Evaluating alternative courses; Selecting an alternative; Implementing the plan; Follow-up action | -
- {f} decides to increase its sales of {g} by 20% next year. | Setting objectives | Objectives are set first.
- {f} assumes that demand will grow by 8% and that there will be no new tax. | Developing premises | Assumptions about the future are made.
- {f} lists three options: open new stores, sell online, or appoint dealers. | Identifying alternative courses of action | Different ways of reaching the goal are found.
- {f} studies the cost and likely returns of each of its three options. | Evaluating alternative courses | Pros and cons are weighed.
- After study, {f} chooses to sell online. | Selecting an alternative | The best option is chosen.
- {f} hires an IT team and launches its website. | Implementing the plan | The plan is put into action.
- {f} checks every month whether online sales are on target. | Follow-up action | The plan is monitored.
A: Developing premises is the second step of the planning process. | Premises are the assumptions on which plans are based. | b | Both true; R explains what premises are, not why it is the second step.
A: Follow-up action is the last step of the planning process. | It ensures that the plan is being implemented properly. | a | Both true; R explains A.
A: Evaluating alternatives comes after selecting an alternative. | The best alternative is chosen after weighing all options. | d | A is false; R is true.
A: Planning premises should be accurate. | Plans built on wrong assumptions will fail. | a | Both true; R explains A.
TT: the planning process
S+: Setting objectives is the first step of planning.
S+: Premises are assumptions about the future.
S+: Follow-up action is the last step.
S-: Selecting an alternative comes before identifying alternatives.
S-: Premises are decided after implementing the plan.
S-: Implementing the plan is the first step.
S-: Evaluating alternatives is the last step.
K: C4 D4 4 | {f} wants to double the sales of {g} in {c}. Its managers assumed that demand would grow by 10%, listed three ways to grow, compared their costs and returns, and chose franchising. | Identify the steps of planning covered so far. => Setting objectives; developing premises; identifying alternatives; evaluating alternatives; selecting an alternative. || Name the two steps that remain and explain one. => Implementing the plan and follow-up action; follow-up checks that the plan is carried out and corrects deviations.
K: C4 D5 6 | {p}, the owner of {f}, started a new {g} line without setting targets or studying alternatives. After launch {he} never checked progress. Sales were poor. | Which steps of planning did {p} skip? => Setting objectives; developing premises; identifying and evaluating alternatives; follow-up action. || Explain how any two of them would have helped. => Objectives give direction; evaluating alternatives selects the best course; follow-up corrects deviations in time.
''', cat='term')

PLANS = ['Objective', 'Strategy', 'Policy', 'Procedure', 'Method', 'Rule', 'Programme', 'Budget']
CH04_ST3 = spec('''
T: Objective | The end result that an organisation wants to achieve, such as increasing sales by 20%.
T: Strategy | A comprehensive plan for accomplishing an organisation's objectives, considering the environment.
T: Policy | A general statement that guides thinking and channels energies towards a particular direction.
T: Procedure | The routine steps on how to carry out an activity, in chronological order.
T: Method | The prescribed way in which a task has to be performed.
T: Rule | A specific statement that tells what is to be done or not done, with no scope for discretion.
T: Programme | A detailed statement about a project that outlines objectives, policies, procedures, rules, tasks, resources and budget.
T: Budget | A statement of expected results expressed in numerical terms.
T: Single-use plan | A plan developed for a one-time event or project, such as a programme or budget.
T: Standing plan | A plan used repeatedly for situations that occur again and again, such as policies, procedures, methods and rules.
Q: Which type of plan is this? | ''' + '; '.join(PLANS) + ''' | -
- {f} aims to increase its market share in {c} by 10% in two years. | Objective | An end result to be achieved.
- {f} decides to enter the rural market with low-priced small packs of its shampoo, considering competitors' moves. | Strategy | A comprehensive plan considering the environment.
- {f} has decided that it will promote employees from within for higher posts wherever possible. | Policy | A general guide to decision making.
- At {f}, a purchase request must be approved by the department head, then by finance, before an order is placed. | Procedure | Routine steps in chronological order.
- {f} trains staff to pack {g} using a specific folding technique. | Method | The prescribed way to do a task.
- Smoking is strictly prohibited in the factory of {f}; violation leads to a fine. | Rule | A specific statement with no discretion.
- {f} prepares a detailed plan for launching a new product, with tasks, schedules, resources and costs. | Programme | A detailed plan for a project.
- {f} estimates that it will sell 50,000 units of {g} and spend ₹40 lakh on production next year. | Budget | Expected results in numbers.
- {f} has a policy of selling only for cash, with no credit to customers. | Policy | A general guideline for sales.
- Employees of {f} must wear helmets on the shop floor at all times. | Rule | No discretion is allowed.
P: policy | rule
- meaning | a general guideline for decision making | a specific statement of what is to be done or not done
- discretion | allows some discretion | allows no discretion
- penalty | no penalty for deviation | violation attracts a penalty
- flexibility | flexible | rigid
P: single-use plans | standing plans
- meaning | developed for a one-time event or project | used repeatedly for recurring situations
- examples | programmes and budgets | policies, procedures, methods and rules
- duration | for a specific period or project | for a longer period
A: A budget is a plan expressed in numerical terms. | It shows expected results in figures. | a | Both true; R explains A.
A: A rule allows managers to use discretion. | A rule is a specific statement of what must be done. | d | A is false; R is true.
A: A strategy considers the business environment. | It is a comprehensive plan for achieving objectives. | a | Both true; R explains A.
A: Procedures are steps in chronological order. | They specify the exact manner of doing a routine activity. | a | Both true; R explains A.
A: A policy is a single-use plan. | Policies guide decisions in recurring situations. | d | A is false: a policy is a standing plan. R is true.
TT: types of plans
S+: A budget is a plan expressed in numbers.
S+: A rule allows no discretion.
S+: A procedure lists steps in chronological order.
S-: A policy allows no discretion at all.
S-: A programme is a standing plan.
S-: A rule is a general guideline.
S-: Objectives are the routine steps for an activity.
K: C4 D4 4 | {f} has decided: (a) to raise sales of {g} by 25%; (b) to sell only to dealers who pay in advance; (c) that no employee may use a mobile phone on the assembly line. | Identify the type of plan in each case. => (a) Objective; (b) policy; (c) rule. || Distinguish between (b) and (c) on two bases. => Policy allows discretion, rule does not; violation of a rule attracts a penalty, deviation from a policy does not.
K: C4 D5 6 | For the launch of a new {g} brand, {f} has prepared a detailed plan of tasks, schedule and resources, with a cost estimate of ₹50 lakh. It also laid down that every order must pass through four approval steps. | Identify the types of plans in the case. => Programme (detailed launch plan); budget (₹50 lakh estimate); procedure (four approval steps). || Classify them as single-use or standing plans. => Programme and budget: single-use; procedure: standing plan.
''', cat='type of plan')

FAMILIES = {S + k: facts(v) for k, v in {
    '01-st1': CH01_ST1, '01-st2': CH01_ST2, '01-st3': CH01_ST3, '01-st4': CH01_ST4,
    '02-st1': CH02_ST1, '02-st2': CH02_ST2, '02-st3': CH02_ST3, '02-st4': CH02_ST4,
    '03-st1': CH03_ST1, '03-st2': CH03_ST2, '03-st3': CH03_ST3, '03-st4': CH03_ST4,
    '04-st1': CH04_ST1, '04-st2': CH04_ST2, '04-st3': CH04_ST3,
}.items()}
