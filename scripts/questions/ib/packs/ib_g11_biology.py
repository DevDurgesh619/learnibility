"""IB DP Biology SL/HL (first assessment 2025), DP year 1 – ib-g11-biology.

Themes A (unity and diversity: water, nucleic acids, cells, viruses, diversity, classification, evolution,
conservation) and B (form and function: carbohydrates, lipids, proteins, membranes, organelles, specialisation,
gas exchange, transport, muscle, adaptation and niches). AHL content is marked (HL) in the curriculum.

Data-based items are parametric and compute their answers (magnification, percentage change, Simpson's
reciprocal index, specific heat, capillarity, Chargaff ratios, sequence similarity, SA:V, osmosis interpolation,
transpiration and ventilation rates, means and standard deviations). Mocks mirror HL Paper 1 (1A + 1B) and
Paper 2 (Sections A and B): see ib_biology_common.MOCK.
"""
from __future__ import annotations

import math

from _common import mcq, name, two_names, sup, CITIES  # noqa: F401
from ib_biology_common import (CONFIG, MOCK, Registry, T, CHI_CRIT, chi_assoc, data_q, dp, interp_zero,  # noqa: F401
                               make_templates, mean, mean_sd_items, nmcq, num, pct_change, pct_items, pick, sd, sf,
                               signed, simpson, table, topic)

R = Registry()
templates = make_templates(R)


def init(subject_id):
    pass


def S(key, **kw):
    topic(R, key, **kw)


# =============================================================================================
# ch01 A1.1 Water
# =============================================================================================
S('ch01-st1',
  terms=[('polar covalent bond', 'a covalent bond in which electrons are shared unequally because one atom is more electronegative, giving the atoms partial charges (δ+ and δ−)'),
         ('hydrogen bond', 'a weak intermolecular attraction between a partially positive hydrogen atom of one polar molecule and a partially negative atom (such as oxygen or nitrogen) of another'),
         ('electronegativity', 'the tendency of an atom to attract the shared electrons of a covalent bond towards itself'),
         ('dipole', 'a molecule or bond with a partial positive charge at one end and a partial negative charge at the other'),
         ('medium for life', 'the watery environment in which the chemical reactions of life take place and in which the first cells are thought to have arisen')],
  facts=[('Which atom in a water molecule carries a partial negative charge?', 'oxygen', ['hydrogen', 'both hydrogen atoms equally', 'neither, because water is non-polar'], 'Oxygen is more electronegative than hydrogen, so it pulls the shared electrons towards itself and becomes δ−.'),
         ('Which type of bond joins the hydrogen and oxygen atoms within a single water molecule?', 'polar covalent bonds', ['hydrogen bonds', 'ionic bonds', 'non-polar covalent bonds'], 'Intramolecular O–H bonds are polar covalent; hydrogen bonds are between molecules.'),
         ('What is the maximum number of hydrogen bonds that one water molecule can form with neighbouring water molecules?', 'four', ['one', 'two', 'six'], 'Two via its δ+ hydrogens and two via the two lone pairs on its δ− oxygen.'),
         ('Which feature of the water molecule, together with unequal electron sharing, makes the whole molecule polar?', 'its bent (V-shaped) geometry', ['its linear geometry', 'its overall negative charge', 'its high molecular mass'], 'The bent shape (about 104.5°) means the bond dipoles do not cancel.'),
         ('Which statement describes the strength of a single hydrogen bond?', 'It is much weaker than a covalent bond.', ['It is stronger than a covalent bond.', 'It is equal in strength to an ionic bond.', 'It is the strongest bond in biology.'], 'A hydrogen bond is about 5–10 % of the strength of a covalent bond, but there are very many of them.')],
  mc2=[('Water (Mr 18) is a liquid at 20 °C whereas methane (Mr 16) is a gas. Which statement best explains this difference?', 'Hydrogen bonds between water molecules require energy to break before water can boil.', ['Water molecules are much heavier than methane molecules.', 'The covalent bonds inside water molecules are stronger.', 'Methane molecules form hydrogen bonds with air.'], 'Methane is non-polar and has only weak intermolecular forces; water molecules are held together by many hydrogen bonds.'),
       ('Why are hydrogen bonds in water described as individually weak but collectively strong?', 'Each bond is weak, but the very large number of bonds gives considerable combined strength.', ['Hydrogen bonds become covalent when many water molecules are present.', 'Hydrogen bonds are stronger than covalent bonds in liquid water.', 'Hydrogen bonds only form in ice, where they are strong.'], 'Water contains vast numbers of hydrogen bonds that constantly break and re-form.'),
       ('Which molecule would NOT be expected to form hydrogen bonds with water?', 'methane (CH₄)', ['ammonia (NH₃)', 'glucose (C₆H₁₂O₆)', 'ethanol (C₂H₅OH)'], 'C–H bonds are almost non-polar, so methane has no δ+ H or δ− atom to bond with water.'),
       ('Why is ice less dense than liquid water at 0 °C?', 'Hydrogen bonds hold the molecules in an open lattice with larger spaces between them.', ['Ice contains trapped bubbles of air.', 'Covalent bonds lengthen when water freezes.', 'Molecules in ice have lost hydrogen atoms.'], 'In ice each molecule is fixed in a tetrahedral, hydrogen-bonded lattice that is more open than the liquid.')],
  mc3=[('A lake in Finland freezes over in winter, yet fish survive. Which explanation links this to the structure of water?', 'Ice floats because hydrogen bonds form an open lattice, and the floating ice insulates the liquid water beneath.', ['Ice sinks and protects the fish from predators.', 'Fish produce heat that prevents the lake from freezing.', 'Liquid water is less dense than ice, so it rises to the top.'], 'Floating ice insulates; the densest water (about 4 °C) collects at the bottom.'),
       ('A newly discovered molecule dissolves readily in water and contains several –OH and –NH₂ groups. What is the best explanation?', 'The groups are polar and form hydrogen bonds with water molecules.', ['The groups are non-polar and repel water.', 'The groups react covalently with water.', 'The groups make the molecule ionic.'], 'Polar –OH and –NH₂ groups are hydrophilic.'),
       ('Ammonia, hydrogen fluoride and water all have unusually high boiling points for their molecular masses. What do they have in common?', 'Hydrogen bonded to a highly electronegative atom (N, F or O).', ['An overall positive charge.', 'Ionic bonds between molecules.', 'A linear molecular shape.'], 'Hydrogen bonding requires H attached to N, O or F.')],
  why=[('Explain why a water molecule is polar.', 'Oxygen is more electronegative than hydrogen, so the shared electrons in each O–H bond are pulled towards oxygen; oxygen becomes δ− and the hydrogens δ+; because the molecule is bent, the charges do not cancel, giving a dipole.'),
       ('Explain how hydrogen bonds form between water molecules.', 'Water molecules are polar; the δ+ hydrogen atom of one molecule is attracted to a lone pair on the δ− oxygen atom of a neighbouring molecule; this electrostatic attraction is a hydrogen bond.'),
       ('Explain why ice floats on liquid water and why this matters to aquatic organisms.', 'In ice, hydrogen bonds hold each molecule in a fixed, open tetrahedral lattice, so ice is less dense than liquid water and floats; the surface ice insulates the water below, so it does not freeze solid and organisms survive the winter.'),
       ('Explain why water has a much higher boiling point than other molecules of similar size, such as methane.', 'Extensive hydrogen bonding between polar water molecules means much energy is needed to separate them into vapour; methane is non-polar with only weak intermolecular forces.'),
       ('Explain why water is described as the medium for life.', 'Most metabolic reactions occur in aqueous solution: water dissolves and transports polar and ionic substances, participates in reactions (hydrolysis, condensation, photosynthesis) and its cohesion and thermal properties support habitats; the first cells probably arose in water.')],
  contrast=[('a polar covalent bond', 'a hydrogen bond', 'A polar covalent bond is a strong intramolecular bond in which electrons are shared unequally (e.g. O–H within water); a hydrogen bond is a weak intermolecular attraction between δ+ H of one molecule and δ− O/N of another.'),
            ('hydrophilic substances', 'hydrophobic substances', 'Hydrophilic substances are polar or charged and are attracted to (dissolve in) water; hydrophobic substances are non-polar, cannot form hydrogen bonds with water and so do not dissolve, clustering together instead.')],
  misc=[('Hydrogen bonds are the bonds that hold hydrogen and oxygen together inside a water molecule.', 'Inside a water molecule the bonds are polar covalent; hydrogen bonds are weaker attractions between δ+ hydrogen of one molecule and δ− oxygen of another molecule.'),
        ('Water is polar because the molecule carries an overall negative charge.', 'Water is electrically neutral overall; it is polar because charge is unevenly distributed (δ− oxygen, δ+ hydrogens) owing to oxygen’s electronegativity and the bent shape.'),
        ('Ice is denser than liquid water because molecules in a solid are always packed more closely.', 'Water is an exception: hydrogen bonds hold molecules in an open lattice in ice, so ice is about 9 % less dense than liquid water and floats.'),
        ('Hydrogen bonds are strong bonds, which is why water is so stable.', 'Individual hydrogen bonds are weak (much weaker than covalent bonds); water’s properties arise from the very large number of hydrogen bonds acting together.')],
  cases=[('the survival of fish under the winter ice of Lake Baikal', 'Ice up to a metre thick forms at the surface and floats, insulating the liquid water below, where temperatures stay near 4 °C.', 'the effect of hydrogen bonding on the density of water', 'Hydrogen bonds fix molecules in an open lattice in ice, so ice is less dense than water, floats and insulates the habitat below.'),
         ('hydrothermal vents on the floor of the Atlantic Ocean', 'Mineral-rich water at vents provides a liquid medium in which chemical energy gradients exist, a proposed site for the origin of life.', 'water as the medium for life', 'Water dissolves the reactants (ions, small polar molecules) and allows them to collide and react, so it is a plausible medium for the first metabolism.')],
  apply=[('Predict, with a reason, whether ammonia (NH₃) can form hydrogen bonds with water molecules.', 'Yes: nitrogen is highly electronegative so N–H bonds are polar; the δ− N can attract δ+ H of water and the δ+ H of ammonia can attract δ− O of water.', 2),
         ('Ethanol (C₂H₅OH) mixes with water in all proportions but hexane (C₆H₁₄) does not. Explain this difference using molecular structure.', 'Ethanol has a polar –OH group that forms hydrogen bonds with water; hexane contains only non-polar C–H and C–C bonds, so it cannot hydrogen bond with water and is excluded.', 3),
         ('Sketch and annotate two water molecules to show the partial charges and one hydrogen bond between them. Describe what your diagram should show.', 'Each molecule bent, O labelled δ−, each H labelled δ+; a dashed line from the δ+ H of one molecule to the δ− O of the other labelled hydrogen bond.', 3)],
  evaluate=[('Hydrogen bonding is the single most important reason why water is suitable as the medium for life.', ['cohesion, adhesion, high specific heat capacity, high latent heat and the density anomaly of ice all arise from hydrogen bonding', 'hydrogen bonds with solutes allow polar molecules such as sugars and amino acids to dissolve'], ['the polarity of water (attraction to ions) explains the solubility of salts without hydrogen bonds', 'other factors such as the liquid range at Earth temperatures and the abundance of water on Earth are also essential'], 'Hydrogen bonding underlies most of water’s life-supporting properties, but polarity more generally, and planetary conditions that keep water liquid, are also required; it is the most important single molecular property rather than the only factor.')],
  extended=[('Outline the structure of a water molecule and explain how its polarity leads to hydrogen bonding and to two properties that are important for living organisms.', 'Two H atoms covalently bonded to O; bent shape about 104.5°; O more electronegative so δ−, H δ+; molecule is a dipole; δ+ H attracts δ− O of another molecule = hydrogen bond; each molecule can form up to four; property 1 e.g. cohesion allowing transpiration pull in xylem; property 2 e.g. high specific heat capacity giving thermally stable habitats; or solvent for polar/ionic substances; or ice floating.', 7)],
  )

S('ch01-st2',
  terms=[('cohesion', 'the attraction between molecules of the same substance, in water due to hydrogen bonds between water molecules'),
         ('adhesion', 'the attraction between molecules of different substances, such as water and the polar walls of xylem vessels'),
         ('capillary action', 'the movement of water up a narrow tube or through a porous material, caused by adhesion to the walls together with cohesion between water molecules'),
         ('surface tension', 'the tendency of the surface of a liquid to resist an external force, caused by cohesion between surface molecules'),
         ('solvent', 'a liquid in which other substances (solutes) dissolve to form a solution'),
         ('hydrophobic', 'describes non-polar substances that do not dissolve in water because they cannot form hydrogen bonds or ionic attractions with it')],
  facts=[('Which property of water allows a pond skater (Gerris) to walk on the surface of a pond?', 'surface tension resulting from cohesion', ['adhesion of water to the insect’s legs', 'the high specific heat capacity of water', 'the low density of ice'], 'Cohesion between surface water molecules produces surface tension that supports the insect.'),
         ('Which property of water allows a continuous column of water to be pulled up xylem vessels?', 'cohesion between water molecules', ['the high latent heat of vaporisation', 'the low viscosity of water', 'the density anomaly of water'], 'Hydrogen bonds hold the water molecules together, so tension at the leaf pulls the column upwards.'),
         ('Which substance is transported in blood plasma mainly bound to a carrier protein because it is hydrophobic?', 'cholesterol', ['glucose', 'sodium chloride', 'amino acids'], 'Cholesterol is non-polar and is carried in lipoproteins.'),
         ('Which substance in blood is transported mainly dissolved in the plasma?', 'glucose', ['oxygen', 'cholesterol', 'triglycerides'], 'Glucose is polar and highly soluble; oxygen is only slightly soluble and is carried by haemoglobin.'),
         ('What causes water to rise up a narrow glass capillary tube?', 'adhesion to the glass combined with cohesion between water molecules', ['evaporation from the top of the tube', 'the low density of water', 'osmosis into the glass'], 'Adhesion pulls water up the walls; cohesion drags the rest of the column with it.')],
  mc2=[('Sodium chloride dissolves in water. Which statement describes what happens at the molecular level?', 'The δ− oxygen of water molecules surrounds Na⁺ ions and the δ+ hydrogen surrounds Cl⁻ ions.', ['Water molecules form covalent bonds with Na and Cl atoms.', 'The δ+ hydrogen of water surrounds Na⁺ ions.', 'The ions become uncharged in solution.'], 'Opposite partial charges attract the ions and form hydration shells.'),
       ('Why is oxygen carried in blood mainly by haemoglobin rather than dissolved in plasma?', 'Oxygen is non-polar and has a low solubility in water.', ['Oxygen reacts with water to form an acid.', 'Plasma is hydrophobic.', 'Oxygen molecules are too large to dissolve.'], 'O₂ is non-polar; its solubility is far too low to meet metabolic demand.'),
       ('Water rises higher in narrow capillary tubes than in wide ones. Which explanation is correct?', 'In a narrow tube a greater proportion of the water is in contact with the walls, so adhesion supports more water per unit mass.', ['Narrow tubes contain less air resistance.', 'Cohesion only occurs in narrow tubes.', 'Water is denser in narrow tubes.'], 'Adhesive force scales with the wall circumference, the weight of the column with cross-sectional area.'),
       ('Which is an example of adhesion rather than cohesion?', 'water moving through the cellulose cell walls of a leaf', ['a water strider standing on a pond surface', 'water forming spherical droplets on a waxy leaf', 'a column of water held together in a xylem vessel'], 'Cellulose is polar; water adheres to it.')],
  mc3=[('A student places drops of water on a waxy cabbage leaf and on filter paper. On the leaf the drops bead up; on the paper they spread and soak in. Which conclusion is valid?', 'Cohesion dominates on the non-polar wax, adhesion dominates on the polar cellulose.', ['Wax is more polar than cellulose.', 'Water is hydrophobic on filter paper.', 'Adhesion dominates on the leaf.'], 'Beading shows water is more attracted to itself than to wax; spreading shows strong adhesion to cellulose.'),
       ('Lipids are absorbed from the small intestine and packaged with proteins into chylomicrons. Which property of lipids makes this packaging necessary?', 'They are hydrophobic and do not dissolve in the aqueous plasma.', ['They are too polar to cross membranes.', 'They are positively charged.', 'They react with water by hydrolysis.'], 'Non-polar lipids must be carried in particles with a hydrophilic surface.'),
       ('Soil water rises through narrow spaces between fine clay particles more than through coarse sand. Which property explains this?', 'capillary action due to adhesion and cohesion', ['high specific heat capacity', 'transparency of water', 'high latent heat of fusion'], 'Narrow spaces give stronger capillary rise.')],
  why=[('Explain how cohesion and adhesion together allow water to move up xylem vessels.', 'Evaporation from leaves creates tension; cohesion (hydrogen bonds between water molecules) transmits this tension down an unbroken column so water is pulled up; adhesion of water to the polar lignified/cellulose walls of xylem helps counter gravity and prevents the column breaking away from the walls.'),
       ('Explain why water is an excellent solvent for many biological molecules.', 'Water is polar; its δ− oxygen and δ+ hydrogens attract ions and form hydration shells; it forms hydrogen bonds with polar molecules such as glucose and amino acids, so these substances dissolve and can be transported and react.'),
       ('Explain why hydrophobic substances such as fats cluster together in water.', 'Non-polar molecules cannot form hydrogen bonds with water; water molecules hydrogen bond with each other instead and exclude the non-polar molecules, which therefore aggregate (the hydrophobic effect).'),
       ('Explain why sodium chloride and glucose are transported dissolved in blood plasma whereas cholesterol and fats are not.', 'NaCl is ionic and glucose is polar, so both are attracted to water and dissolve; cholesterol and fats are non-polar/hydrophobic, so they are carried in lipoprotein particles with a hydrophilic outer layer of phospholipids and proteins.'),
       ('Explain why surface tension is useful to some organisms.', 'Cohesion between surface water molecules produces a surface film that resists penetration; small organisms such as pond skaters can move on it and some insect larvae hang from it, giving access to a habitat at the air–water boundary.')],
  contrast=[('cohesion', 'adhesion', 'Cohesion is attraction between water molecules themselves (hydrogen bonds between water molecules); adhesion is attraction between water and a different polar or charged substance such as cellulose or glass.'),
            ('hydrophilic substances', 'hydrophobic substances', 'Hydrophilic substances are polar or ionic and dissolve in or are attracted to water; hydrophobic substances are non-polar and do not dissolve, instead clustering together.')],
  misc=[('Water moves up xylem because of adhesion alone.', 'Adhesion helps, but the main mechanism is cohesion–tension: transpiration creates tension that is transmitted down the column because water molecules are held together by cohesion.'),
        ('Oxygen dissolves easily in blood plasma, which is why we have plasma.', 'Oxygen is non-polar and poorly soluble in water; most oxygen is carried bound to haemoglobin in red blood cells.'),
        ('Water dissolves everything because it is the universal solvent.', 'Water dissolves polar and ionic substances; non-polar substances such as lipids are hydrophobic and do not dissolve.'),
        ('Cohesion is the attraction between water and the walls of a container.', 'That is adhesion; cohesion is the attraction between water molecules themselves.')],
  cases=[('the transport of water up a 100 m coast redwood (Sequoia sempervirens)', 'Water is pulled from roots to leaves through xylem, with tensions of several megapascals in the column.', 'cohesion and adhesion in water transport', 'Cohesion keeps the column continuous under tension; adhesion to xylem walls supports it, allowing water to reach great heights without a pump.'),
         ('pond skaters (Gerris lacustris) moving across the surface of a pond', 'The insects stand on the water surface without breaking it, spreading their weight on hydrophobic hairy legs.', 'surface tension', 'Cohesion between surface water molecules creates a film strong enough to support small animals.'),
         ('the transport of cholesterol in human blood as LDL and HDL particles', 'Cholesterol is packaged inside lipoproteins with phospholipid and protein coats.', 'the solvent properties of water', 'Because cholesterol is hydrophobic it cannot dissolve in plasma and must be carried in particles with a hydrophilic exterior.')],
  apply=[('Predict how the following are transported in blood plasma, giving a reason for each: glucose, oxygen, sodium chloride, cholesterol.', 'Glucose – dissolved (polar); oxygen – mostly bound to haemoglobin (non-polar, low solubility); NaCl – dissolved as Na⁺ and Cl⁻ ions (ionic); cholesterol – in lipoproteins (hydrophobic).', 4),
         ('A paper towel dipped in water draws water upwards several centimetres. Explain this observation using two properties of water.', 'Adhesion between water and the polar cellulose fibres pulls water along the fibres; cohesion between water molecules draws more water up behind = capillary action.', 2)],
  evaluate=[('The cohesion–tension theory fully explains how water reaches the tops of the tallest trees.', ['cohesion of water due to hydrogen bonding can sustain tensions large enough to lift water over 100 m', 'measured negative pressures in xylem and the narrowing of trunks during the day support the theory'], ['air bubbles (cavitation/embolism) can break the column, so additional mechanisms such as refilling and parallel vessels are needed', 'root pressure can contribute in some plants, especially at night or in spring'], 'Cohesion–tension is the main, well-supported mechanism, but a complete account must include adhesion, xylem structure that limits embolism, and minor contributions from root pressure.')],
  extended=[('Describe how the cohesive, adhesive and solvent properties of water are each significant for living organisms. Use a named example for each property.', 'Cohesion: hydrogen bonds between water molecules; allows transpiration pull in xylem / surface tension for pond skaters. Adhesion: water attracted to polar surfaces; capillary action in cell walls/xylem/soil. Solvent: polar water dissolves ions and polar molecules; e.g. glucose and amino acids transported in plasma, metabolic reactions in cytoplasm; non-polar substances such as cholesterol need carriers.', 7)],
  )

S('ch01-st3',
  terms=[('specific heat capacity', 'the energy needed to raise the temperature of 1 g (or 1 kg) of a substance by 1 °C; for water about 4.18 J g⁻¹ °C⁻¹'),
         ('latent heat of vaporisation', 'the energy required to convert a liquid into vapour without a change in temperature; for water it is very high because hydrogen bonds must be broken'),
         ('thermal conductivity', 'the ability of a substance to transfer heat energy through itself'),
         ('buoyancy', 'the upward force exerted by a fluid on an object immersed in it, which depends on the density of the fluid'),
         ('viscosity', 'the resistance of a fluid to flow; water has low viscosity compared with oils')],
  facts=[('Which property of water explains why sweating cools the body?', 'its high latent heat of vaporisation', ['its high density', 'its low specific heat capacity', 'its high surface tension'], 'Evaporation of each gram of sweat removes about 2.4 kJ of heat from the skin.'),
         ('Approximately what is the specific heat capacity of liquid water?', '4.18 J g⁻¹ °C⁻¹', ['0.418 J g⁻¹ °C⁻¹', '41.8 J g⁻¹ °C⁻¹', '2.26 J g⁻¹ °C⁻¹'], 'About 4.2 J are needed to raise 1 g of water by 1 °C.'),
         ('Compared with air, water has a much higher', 'specific heat capacity, density and thermal conductivity', ['viscosity, buoyancy and transparency to ultraviolet', 'compressibility', 'oxygen solubility'], 'Water absorbs and conducts heat far better than air and is about 800 times denser.'),
         ('Which animal is a good example of an organism whose body shape reduces the effect of water viscosity?', 'the ringed seal (Pusa hispida)', ['the black-throated loon flying in air', 'a ground-dwelling earthworm', 'a cactus'], 'Ringed seals are streamlined to swim efficiently in viscous, dense water.'),
         ('Why do large bodies of water such as oceans have relatively stable temperatures?', 'Water has a high specific heat capacity, so large energy changes produce small temperature changes.', ['Water reflects all sunlight.', 'Water has a low density.', 'Water does not conduct heat.'], 'Many hydrogen bonds must be broken to raise the temperature.')],
  mc2=[('Why does water have a high specific heat capacity?', 'Energy is used to break hydrogen bonds before molecules can move faster.', ['Water molecules are very heavy.', 'Covalent bonds in water break as it heats.', 'Water is a non-polar molecule.'], 'Absorbed energy first disrupts hydrogen bonds, so the temperature rises slowly.'),
       ('Which property of water makes it a more stable habitat than air for small organisms?', 'its high specific heat capacity', ['its low viscosity', 'its high transparency', 'its low density'], 'Water temperature changes slowly, reducing thermal stress.'),
       ('The black-throated loon (Gavia arctica) lives at the boundary between air and water. Which comparison of the two media is correct?', 'Water is denser and more viscous, so swimming requires more force than gliding in air, but buoyancy supports the body.', ['Air is more buoyant than water.', 'Air has a higher thermal conductivity than water.', 'Water is less viscous than air.'], 'Water gives more buoyancy but more drag than air.'),
       ('Why does a ringed seal need thick blubber whereas an Arctic bird such as a loon relies mainly on feathers?', 'Water conducts heat away about 25 times faster than air, so animals in water lose heat more rapidly.', ['Air has a higher specific heat capacity.', 'Feathers do not work in cold air.', 'Blubber increases density for diving.'], 'High thermal conductivity of water makes insulation critical.')],
  mc3=[('A 70 kg runner loses 500 g of sweat by evaporation during a race. Taking the latent heat of vaporisation of water as 2.4 kJ g⁻¹, how much heat is removed?', '1200 kJ', ['120 kJ', '12 000 kJ', '2.4 kJ'], 'Q = m × L = 500 g × 2.4 kJ g⁻¹ = 1200 kJ.'),
       ('Equal masses of water and ethanol are heated with the same heater for the same time. Which result is expected?', 'The ethanol shows a larger temperature rise.', ['The water shows a larger temperature rise.', 'Both show the same temperature rise.', 'The water boils first.'], 'Ethanol has a lower specific heat capacity (about 2.4 J g⁻¹ °C⁻¹) than water (4.18).'),
       ('Coastal cities such as Lisbon have smaller annual temperature ranges than inland cities at the same latitude. Which property of water best explains this?', 'high specific heat capacity', ['high surface tension', 'high viscosity', 'cohesion'], 'The ocean absorbs and releases heat slowly, moderating the climate.')],
  why=[('Explain why water has a high specific heat capacity.', 'Many hydrogen bonds between water molecules must be broken to increase the kinetic energy of the molecules; much of the energy supplied is used to break these bonds, so a lot of energy is needed per 1 °C rise.'),
       ('Explain how the high latent heat of vaporisation of water helps mammals to cool down.', 'Evaporating sweat requires a large amount of energy to break hydrogen bonds; this heat is taken from the skin and blood, so evaporation of a small mass of sweat removes a large amount of heat.'),
       ('Explain why aquatic habitats have more stable temperatures than terrestrial habitats.', 'Water has a high specific heat capacity, so it absorbs or loses a lot of energy for a small change in temperature; daily and seasonal fluctuations are therefore smaller in water.'),
       ('Explain how differences in the physical properties of air and water affect the movement of animals living in them.', 'Water is denser and more viscous than air: it provides more buoyancy (less support needed) but more drag, favouring streamlined bodies (e.g. ringed seal); air provides little buoyancy, so flying animals need lift (e.g. loon wings).'),
       ('Explain why animals living in polar waters need more insulation than those living in polar air at the same temperature.', 'Water has a much higher thermal conductivity than air, so heat is conducted away from the body faster; thick blubber reduces this heat loss.')],
  contrast=[('specific heat capacity', 'latent heat of vaporisation', 'Specific heat capacity is the energy to raise the temperature of a unit mass by 1 °C (no change of state); latent heat of vaporisation is the energy to change a unit mass of liquid to gas at constant temperature.'),
            ('water', 'air as a medium for animals', 'Water has higher density, viscosity, buoyancy, thermal conductivity and specific heat capacity than air: aquatic animals are supported but face drag and faster heat loss; animals in air need skeletal support or lift but lose heat more slowly.')],
  misc=[('Sweating cools you because the sweat itself is cold.', 'Sweat is at body temperature; cooling occurs because evaporation absorbs a large amount of heat energy (high latent heat of vaporisation) from the skin.'),
        ('Water heats up quickly because it is a good conductor of heat.', 'Water heats up slowly because of its high specific heat capacity; much energy is used to break hydrogen bonds.'),
        ('Animals in water lose heat more slowly than in air because water is a stable habitat.', 'Water has a higher thermal conductivity than air, so animals in water lose heat faster; water’s temperature is stable, but heat loss from bodies is greater.')],
  cases=[('the ringed seal (Pusa hispida) and the black-throated loon (Gavia arctica)', 'The seal is a streamlined swimmer insulated by blubber; the loon flies in air and dives in water, using feathers for insulation.', 'how the physical properties of air and water differ for organisms', 'Water’s higher density, viscosity and thermal conductivity favour streamlining and blubber in the seal, while the loon must cope with both media.'),
         ('sweating in marathon runners in hot climates', 'Runners can lose over 1 litre of sweat per hour, which evaporates from the skin.', 'the high latent heat of vaporisation of water', 'Each gram evaporated absorbs about 2.4 kJ, so evaporative cooling removes a large amount of metabolic heat.')],
  evaluate=[('The thermal properties of water are more important to living organisms than its solvent properties.', ['high specific heat capacity stabilises habitats and body temperature', 'evaporative cooling is essential for thermoregulation in many mammals and plants'], ['without water acting as a solvent, metabolism and transport could not occur at all', 'many organisms survive large temperature changes but none can survive without aqueous cytoplasm'], 'Solvent properties are more fundamental because they make metabolism possible; thermal properties are important for stability and regulation, so both matter but solvent properties are more essential.')],
  extended=[('Compare and contrast the physical properties of air and water as habitats, and explain how these properties have influenced the adaptations of a named aquatic mammal.', 'Comparisons: water denser (buoyancy), more viscous (drag), higher thermal conductivity (heat loss), higher specific heat capacity (stable temperature); both are fluids that allow movement. Named mammal e.g. ringed seal: streamlined body reduces drag; thick blubber reduces heat loss by conduction; flippers for propulsion; buoyancy reduces skeletal load.', 8)],
  )

S('ch01-st4',
  terms=[('Goldilocks zone', 'the range of distances from a star (the habitable zone) at which a planet’s surface temperature allows liquid water to exist'),
         ('carbonaceous chondrite', 'a type of primitive meteorite rich in water-bearing minerals and organic carbon, thought to have delivered water to the early Earth'),
         ('D/H ratio', 'the ratio of deuterium to ordinary hydrogen in a sample of water, used to trace the source of Earth’s water'),
         ('astrobiology', 'the scientific study of the origin, evolution and distribution of life in the universe'),
         ('extremophile', 'an organism that thrives in extreme conditions, used as a model for where life might exist on other worlds')],
  facts=[('According to the main hypothesis, how did much of Earth’s water arrive after the planet formed?', 'from collisions with asteroids (and some comets) containing water', ['by photosynthesis in the first cells', 'by condensation of hydrogen from the Sun', 'by nuclear fusion in Earth’s core'], 'The D/H ratio of carbonaceous chondrites closely matches ocean water.'),
         ('Why has Earth retained liquid water while Venus has not?', 'Earth lies at a distance from the Sun where temperatures allow water to stay liquid', ['Earth has a weaker gravitational field', 'Venus never received any water', 'Earth is closer to the Sun'], 'Earth is in the habitable (Goldilocks) zone; Venus suffered a runaway greenhouse effect.'),
         ('Which evidence is used to compare possible sources of Earth’s water?', 'the deuterium-to-hydrogen ratio of the water', ['the colour of the water', 'the pH of the water', 'the temperature of the water'], 'D/H is a chemical fingerprint of the water’s origin.'),
         ('Which moon is a target in the search for extraterrestrial life because it has a liquid water ocean beneath its icy crust?', 'Europa (Jupiter)', ['the Moon (Earth)', 'Phobos (Mars)', 'Io (Jupiter)'], 'Europa and Enceladus are thought to have subsurface liquid water oceans.')],
  mc2=[('Why is liquid water considered a requirement in the search for life elsewhere?', 'All known life uses water as the solvent for its metabolic reactions.', ['Water is the only molecule that contains hydrogen.', 'Water is needed to make planets spherical.', 'Life can only be detected through water.'], 'Life as we know it depends on aqueous chemistry.'),
       ('Comet 67P has a D/H ratio about three times that of Earth’s oceans. What does this suggest?', 'Comets similar to 67P were not the main source of Earth’s water.', ['All of Earth’s water came from 67P-type comets.', 'Earth’s water formed from the Sun.', 'Comets contain no water.'], 'A mismatch in D/H ratio argues against that source.'),
       ('Mars lies at the outer edge of the habitable zone but has no stable surface liquid water today. Which factor most explains this?', 'Its thin atmosphere and low pressure mean water freezes or sublimes.', ['It is closer to the Sun than Earth.', 'It has a thicker atmosphere than Venus.', 'Its surface is made of water ice only.'], 'Low pressure prevents stable liquid water even where temperatures allow.')],
  mc3=[('A star has a luminosity 4 times that of the Sun. The Sun’s habitable zone lies about 0.95–1.37 AU from it. Where would the habitable zone of this star lie?', 'about 1.9–2.7 AU', ['about 3.8–5.5 AU', 'about 0.48–0.69 AU', 'about 0.95–1.37 AU'], 'Distance scales with √L: √4 = 2, so 1.9–2.7 AU.'),
       ('Water vapour plumes from Saturn’s moon Enceladus contain salts, silica and simple organic molecules. Why does this make Enceladus a target for astrobiology?', 'It suggests a liquid water ocean in contact with rock, a possible energy and chemical source for life.', ['It proves life exists on Enceladus.', 'It shows Enceladus is in the Sun’s habitable zone.', 'It shows the water came from Earth.'], 'Liquid water plus energy plus chemistry are the requirements for life as we know it.')],
  why=[('Explain why the presence of liquid water is used as a guide in the search for extraterrestrial life.', 'All known life depends on water as the medium for metabolism: it dissolves reactants, allows molecules to move and react, and takes part in reactions; so planets or moons with liquid water are the most likely to support life as we know it.'),
       ('Explain why Earth has retained large amounts of liquid water.', 'Earth’s distance from the Sun gives surface temperatures between 0 and 100 °C (Goldilocks zone); its gravity and atmosphere retain water vapour, and the magnetic field reduces loss of the atmosphere to solar wind.'),
       ('Explain how the D/H ratio of water is used to test hypotheses about the origin of Earth’s water.', 'Different sources (comets, asteroids, solar nebula) have characteristic D/H ratios; if a source’s ratio matches that of ocean water it is a plausible main source; carbonaceous chondrites match closely whereas many comets have higher ratios.')],
  contrast=[('the asteroid hypothesis', 'the comet hypothesis for the origin of Earth’s water', 'The asteroid hypothesis proposes water-rich carbonaceous asteroids delivered most water, supported by their Earth-like D/H ratio; the comet hypothesis proposes icy comets, but most measured comets (e.g. 67P) have D/H ratios much higher than Earth’s oceans.')],
  misc=[('Water has always been on Earth because it formed from the same material as the planet in a hot state.', 'The early Earth was very hot and much water would have been lost; much of the present water is thought to have been delivered later by water-rich asteroids.'),
        ('If a planet has water, it must have life.', 'Liquid water is a necessary condition for life as we know it, but not a sufficient one; energy sources, suitable chemistry and time are also needed.')],
  cases=[('the Rosetta mission’s measurements of comet 67P/Churyumov–Gerasimenko', 'Rosetta found a D/H ratio of about 5.3 × 10⁻⁴, over three times that of Earth’s oceans (about 1.56 × 10⁻⁴).', 'the testing of hypotheses about the origin of Earth’s water', 'The mismatch suggests comets like 67P were not the main source, supporting the asteroid hypothesis instead.'),
         ('NASA’s Cassini mission flying through the plumes of Enceladus', 'Cassini detected water, salts, silica and organic molecules in plumes erupting from a subsurface ocean.', 'the link between water and the search for extraterrestrial life', 'Evidence of liquid water with chemical energy makes Enceladus a prime target in the search for life.')],
  sources=[('Measured D/H ratios (× 10⁻⁴): Earth’s oceans 1.56; carbonaceous chondrite meteorites 1.4–1.8; comet Hartley 2 1.61; comet 67P 5.3; comet Halley 3.1.', 'Data compiled from published spacecraft and meteorite analyses', 'Using the data, evaluate the hypothesis that comets were the main source of Earth’s water.', 'Carbonaceous chondrites (1.4–1.8) bracket the ocean value, supporting asteroids as the main source; most comets (67P 5.3, Halley 3.1 – 2 to 3.4 times higher) do not match; Hartley 2 does match, so some comets may have contributed; small sample of comets is a limitation; conclusion: asteroids more likely main source, comets minor.')],
  evaluate=[('The search for extraterrestrial life should focus only on planets and moons with liquid water.', ['all known life requires liquid water as a solvent', 'it narrows the search to the most promising targets such as Europa, Enceladus and Mars'], ['life elsewhere might use a different solvent such as liquid methane (e.g. on Titan)', 'focusing only on water could cause us to miss unfamiliar forms of life'], 'Water is a sensible first priority because it is the only solvent known to support life, but some effort should be kept for other possibilities, as our definition of life is based on a single example.')],
  extended=[('Outline the hypotheses for the origin of water on Earth, and discuss how this knowledge is used in the search for extraterrestrial life.', 'Early Earth hot – water lost/limited; water delivered by asteroids (carbonaceous chondrites) – D/H matches oceans; comets – most have higher D/H; water retained because Earth in Goldilocks zone, sufficient gravity and atmosphere; search for life targets bodies with liquid water (Mars past, Europa, Enceladus); habitable zones of exoplanets estimated from stellar luminosity; water necessary but not sufficient.', 7)],
  )


@R.add('ch01-st4', 'C3', (2, 5), 'numerical')
def habitable_zone(rng, slot):
    L = pick(rng, [0.25, 0.36, 0.49, 0.64, 1.44, 1.96, 2.25, 4.0, 6.25, 9.0])
    stars = ['Kepler-62', 'an orange dwarf star', 'a K-type star', 'an F-type star', 'Gliese 581', 'a red dwarf star', 'Tau Ceti', 'a star in the Kepler field']
    s = pick(rng, stars)
    r = math.sqrt(L)
    a, b = 0.95 * r, 1.37 * r
    d = round(rng.uniform(0.3, 3.5) * r / 1.0, 2) if slot.d >= 4 else None
    stem = (f'The habitable (Goldilocks) zone of the Sun lies between about 0.95 AU and 1.37 AU. The distance of the zone scales with the square root of a star’s luminosity. '
            f'{s} has a luminosity {L} times that of the Sun. Calculate the inner and outer limits of its habitable zone.')
    ans = f'{a:.2f} AU to {b:.2f} AU'
    key = f'√{L} = {r:.2f} (M1); inner = 0.95 × {r:.2f} = {a:.2f} AU, outer = 1.37 × {r:.2f} = {b:.2f} AU (A1).'
    if d is not None:
        inside = a <= d <= b
        stem += f' A planet orbits this star at {d} AU. Deduce whether it could have liquid surface water and state one other condition needed.'
        ans += f'; planet at {d} AU is ' + ('inside the zone – liquid water possible' if inside else 'outside the zone – liquid surface water unlikely') + '; also needs sufficient mass/gravity and an atmosphere to retain water.'
        key += f' Comparison: {d} AU is {"inside" if inside else "outside"} {a:.2f}–{b:.2f} AU (R1); other condition e.g. atmosphere/pressure, gravity to retain water (A1).'
        return num(stem, ans, key, 4)
    return num(stem, ans, key, 2)


@R.add('ch01-st4', 'C3', (1, 4), 'mcq')
def dh_ratio_mcq(rng, slot):
    src = pick(rng, [('comet 67P', 5.3), ('comet Halley', 3.1), ('comet Hyakutake', 2.9), ('comet Hale–Bopp', 3.3), ('comet 103P/Hartley 2', 1.61), ('a carbonaceous chondrite', 1.7), ('comet 46P/Wirtanen', 1.61)])
    ocean = 1.56
    ratio = src[1] / ocean
    stem = f'The D/H ratio of Earth’s ocean water is 1.56 × 10⁻⁴ and that of {src[0]} is {src[1]} × 10⁻⁴. How many times greater is the ratio for {src[0]}, and is it consistent with being a major source of Earth’s water?'
    close = abs(ratio - 1) < 0.15
    c = f'{ratio:.2f} times; {"consistent" if close else "not consistent"}'
    w = [f'{ratio:.2f} times; {"not consistent" if close else "consistent"}', f'{1 / ratio:.2f} times; {"consistent" if close else "not consistent"}', f'{src[1] - ocean:.2f} times; {"not consistent" if close else "consistent"}']
    return nmcq(rng, stem, c, w, f'{src[1]}/1.56 = {ratio:.2f}; a ratio close to 1 matches ocean water.')


# ---- data-based (ch01)
def _capillary(rng, slot):
    ds = [0.5, 1.0, 1.5, 2.0, 3.0]
    k = rng.uniform(28.5, 30.5)
    hs = [round(k / d * rng.uniform(0.96, 1.04), 1) for d in ds]
    liquid = pick(rng, ['distilled water', 'tap water', 'pond water'])
    who = name(rng)
    prods = [h * d for h, d in zip(hs, ds)]
    kk = mean(prods)
    dn = pick(rng, [0.8, 1.2, 2.5, 0.6, 4.0])
    pred = kk / dn
    pc = pct_change(hs[1], hs[0])
    intro = (f'{who} measured the height to which {liquid} rose in clean glass capillary tubes of different internal diameters at 20 °C. Each value is the mean of three readings.\n\n'
             + table(['Internal diameter / mm', 'Mean height of water / mm'], [(f'{d:.1f}', f'{h:.1f}') for d, h in zip(ds, hs)]))
    parts = [
        ('Describe the relationship between tube diameter and the height of water.', 'As diameter increases the height decreases; halving the diameter roughly doubles the height (inverse proportion).', 'Height decreases as diameter increases (A1); idea of inverse proportionality / non-linear (A1).', 2),
        ('Calculate the percentage increase in height when the diameter is reduced from 1.0 mm to 0.5 mm.', f'{pc:.0f} %', f'({hs[0]:.1f} − {hs[1]:.1f})/{hs[1]:.1f} × 100 (M1) = {pc:.0f} % (A1).', 2),
        (f'Height × diameter is approximately constant. Use the data to predict the height of water in a tube of internal diameter {dn} mm.', f'≈ {pred:.1f} mm', f'Mean of h × d ≈ {kk:.1f} mm² (M1); {kk:.1f}/{dn} = {pred:.1f} mm (A1); accept ±5 %.', 2),
        ('Explain, in terms of the properties of water, why water rises in a narrow glass tube.', 'Adhesion of polar water molecules to the polar glass pulls water up the walls; cohesion (hydrogen bonds) pulls the rest of the column up behind; rise stops when the weight of the column balances these forces.', 'Adhesion to glass (A1); cohesion between water molecules/hydrogen bonds (A1); balance with weight of column / narrower tube = less mass per unit wall contact (A1).', 3),
        ('State one variable, other than temperature, that should be controlled.', 'e.g. cleanliness/material of the tubes; type/purity of water; depth to which the tube is dipped.', 'Any one valid controlled variable (A1).', 1),
        ('Suggest how these results relate to water transport in plants.', 'Xylem vessels are narrow tubes with polar (lignified/cellulose) walls; capillary action contributes to water rise, but only by a small height, so transpiration pull is needed for tall plants.', 'Xylem as narrow tubes with adhesive walls (A1); capillarity alone only lifts water a few cm / cohesion–tension needed for tall trees (R1).', 2),
        ('Outline why each value was the mean of three readings.', 'Repeats allow anomalies to be identified and reduce the effect of random error, increasing reliability.', 'Reduce random error / identify anomalies (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch01-st2', _capillary)


SH = {'ethanol': 2.44, 'vegetable oil': 1.97, 'glycerol': 2.43, 'seawater': 3.99, 'olive oil': 1.97}


def _heating(rng, slot):
    liq = pick(rng, list(SH))
    m = pick(rng, [50, 100, 150, 200])
    Q = pick(rng, [4000, 5000, 6000, 8000, 10000])
    dtw = Q / (m * 4.18) * rng.uniform(0.97, 1.03)
    dtl = Q / (m * SH[liq]) * rng.uniform(0.97, 1.03)
    dtw, dtl = round(dtw, 1), round(dtl, 1)
    cw = Q / (m * dtw)
    cl = Q / (m * dtl)
    diff = 100 * (cw - cl) / cl
    who = name(rng)
    intro = (f'{who} supplied {Q} J of energy from an electric immersion heater to {m} g samples of water and of {liq}, each in an insulated beaker, and recorded the temperature rise.\n\n'
             + table(['Liquid', 'Mass / g', 'Energy supplied / J', 'Temperature rise / °C'], [('water', m, Q, f'{dtw:.1f}'), (liq, m, Q, f'{dtl:.1f}')]))
    parts = [
        ('State which liquid showed the greater temperature rise.', liq, f'{liq} (A1).', 1),
        ('Calculate the specific heat capacity of each liquid in J g⁻¹ °C⁻¹, using c = Q/(m ΔT).', f'water {cw:.2f}; {liq} {cl:.2f} J g⁻¹ °C⁻¹', f'Water: {Q}/({m} × {dtw:.1f}) = {cw:.2f} (A1); {liq}: {Q}/({m} × {dtl:.1f}) = {cl:.2f} (A1).', 2),
        (f'Calculate how many percent greater the specific heat capacity of water is than that of {liq}.', f'{diff:.0f} %', f'({cw:.2f} − {cl:.2f})/{cl:.2f} × 100 (M1) = {diff:.0f} % (A1).', 2),
        ('Explain why water has a high specific heat capacity.', 'Much of the energy supplied is used to break the many hydrogen bonds between water molecules rather than increasing their kinetic energy.', 'Hydrogen bonds between molecules (A1); energy used to break them before temperature rises (A1).', 2),
        ('Suggest one reason why the value obtained for water may differ from the accepted value of 4.18 J g⁻¹ °C⁻¹.', 'Heat lost to the surroundings/beaker; thermometer reading error; uneven mixing.', 'Any valid source of error linked to the direction of the difference (A1).', 1),
        ('Outline the significance of the high specific heat capacity of water for aquatic organisms.', 'Water temperature changes slowly, so aquatic habitats are thermally stable and organisms experience smaller temperature fluctuations; enzyme activity is kept relatively constant.', 'Stable habitat temperature (A1); link to reduced stress / stable enzyme activity / body temperature (A1).', 2),
        ('Suggest one improvement to the method.', 'Stir the liquid; use a lid; repeat and calculate a mean; use a digital thermometer.', 'Any one valid improvement (A1).', 1),
        ('Explain why the liquids were heated in identical containers with the same heater.', 'So that the same energy is supplied and heat losses are similar, making the comparison fair.', 'Same energy input (A1); similar heat loss/fair test (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch01-st3', _heating)


@R.add('ch01-st3', 'C3', (1, 4), 'numerical')
def sweat_calc(rng, slot):
    frames = [
        ('A cyclist in {c} evaporates {m} g of sweat during a training ride.', 'sweat'),
        ('A dog pants and evaporates {m} g of water from its respiratory surfaces in an hour on a hot day in {c}.', 'water'),
        ('A eucalyptus tree in {c} transpires {m} g of water from its leaves in one minute at midday.', 'water'),
    ]

    f, what = pick(rng, frames)
    m = pick(rng, [150, 200, 250, 300, 400, 450, 600, 750, 900])
    L = 2.4
    Q = m * L
    s = f.format(c=pick(rng, CITIES), m=m)
    if slot.d <= 2:
        stem = f'{s} The latent heat of vaporisation of water at skin or leaf temperature is about 2.4 kJ g⁻¹. Calculate the heat energy removed.'
        return num(stem, f'{Q:.0f} kJ', f'Q = m × L = {m} × 2.4 (M1) = {Q:.0f} kJ (A1).', 2)
    target = pick(rng, [1000, 1500, 2000, 2500, 3000])
    need = target / L
    stem = (f'{s} Taking the latent heat of vaporisation of water as 2.4 kJ g⁻¹, calculate the heat removed. Then calculate the mass of {what} that would need to evaporate to remove {target} kJ, '
            f'and explain why evaporation is such an effective cooling mechanism.')
    return num(stem, f'{Q:.0f} kJ; {need:.0f} g', f'{m} × 2.4 = {Q:.0f} kJ (A1); {target}/2.4 = {need:.0f} g (A1); many hydrogen bonds must be broken for each molecule to evaporate, so a lot of energy is absorbed from the surface (R1).', 3)


# =============================================================================================
# ch02 A1.2 Nucleic acids
# =============================================================================================
S('ch02-st1',
  terms=[('nucleotide', 'the monomer of a nucleic acid, made of a pentose sugar, a phosphate group and a nitrogenous base'),
         ('sugar–phosphate backbone', 'the chain of alternating pentose sugars and phosphate groups linked by covalent (phosphodiester) bonds that forms the outside of each strand of a nucleic acid'),
         ('double helix', 'the structure of DNA in which two antiparallel polynucleotide strands are wound around each other and held together by hydrogen bonds between complementary bases'),
         ('antiparallel', 'describes the two strands of DNA running in opposite directions, one 5′→3′ and the other 3′→5′'),
         ('purine', 'a nitrogenous base with a double-ring structure (adenine or guanine)'),
         ('pyrimidine', 'a nitrogenous base with a single-ring structure (cytosine, thymine or uracil)')],
  facts=[('Which components make up a single DNA nucleotide?', 'deoxyribose, a phosphate group and a nitrogenous base', ['ribose, a phosphate group and a nitrogenous base', 'deoxyribose, an amino acid and a phosphate group', 'glucose, a phosphate group and a base'], 'DNA nucleotides contain the pentose deoxyribose.'),
         ('Which bonds link adjacent nucleotides within one strand of DNA?', 'covalent bonds between the phosphate of one nucleotide and the sugar of the next', ['hydrogen bonds between bases', 'peptide bonds between bases', 'ionic bonds between phosphates'], 'Condensation forms a phosphodiester (covalent) linkage between the 3′ carbon of one sugar and the phosphate of the next.'),
         ('Which carbon atom of the pentose is the phosphate group attached to in a nucleotide?', 'carbon 5′', ['carbon 1′', 'carbon 2′', 'carbon 3′ only'], 'The base attaches at C1′, the phosphate at C5′, and the next nucleotide links to C3′.'),
         ('Which pair of bases are both purines?', 'adenine and guanine', ['cytosine and thymine', 'adenine and thymine', 'guanine and cytosine'], 'Purines (A, G) have two rings.'),
         ('Which scientists used the X-ray diffraction image produced by Rosalind Franklin to build the double-helix model of DNA in 1953?', 'James Watson and Francis Crick', ['Hershey and Chase', 'Meselson and Stahl', 'Miller and Urey'], 'Photograph 51 helped Watson and Crick deduce the helical structure.')],
  mc2=[('Why is the width of the DNA double helix constant along its length?', 'Each base pair contains one purine and one pyrimidine.', ['All four bases are the same size.', 'Both strands run in the same direction.', 'Hydrogen bonds are all the same length.'], 'A purine (two rings) always pairs with a pyrimidine (one ring).'),
       ('What is meant by the 3′ end of a DNA strand?', 'the end with a free –OH on carbon 3′ of the deoxyribose', ['the end with a free phosphate group', 'the end with three phosphate groups', 'the end with the third base'], 'The 5′ end has the free phosphate; the 3′ end has the free hydroxyl.'),
       ('Which feature of DNA structure makes it chemically stable enough to store information for long periods?', 'covalently bonded sugar–phosphate backbones with bases protected inside the helix', ['single-stranded structure', 'weak bonds within each strand', 'the presence of uracil'], 'The backbone is covalently bonded; bases are stacked inside.'),
       ('Which statement about the hydrogen bonds in DNA is correct?', 'G–C pairs form three hydrogen bonds and A–T pairs form two.', ['All base pairs form three hydrogen bonds.', 'A–T pairs form three hydrogen bonds.', 'Hydrogen bonds join the sugars to the phosphates.'], 'G–C rich DNA is therefore more thermally stable.')],
  mc3=[('A sample of DNA has a higher melting temperature than another of the same length. What is the most likely explanation?', 'It has a higher proportion of G–C base pairs.', ['It has a higher proportion of A–T base pairs.', 'It contains uracil instead of thymine.', 'It is single-stranded.'], 'Three hydrogen bonds per G–C pair require more energy to separate.'),
       ('A student’s model of DNA shows both strands with their 5′ ends at the top. What is wrong with the model?', 'The strands should be antiparallel, with one 5′ end at the top and one at the bottom.', ['The strands should be parallel.', 'The bases should be on the outside.', 'The 3′ ends should both be at the top.'], 'DNA strands are antiparallel.')],
  why=[('Explain how the structure of a nucleotide allows nucleotides to be linked into a polymer.', 'The phosphate on C5′ of one nucleotide forms a covalent bond (by condensation) with the –OH on C3′ of the sugar of the next; repeated linkage forms a sugar–phosphate backbone with bases projecting from it.'),
       ('Explain why DNA is described as a double helix with antiparallel strands.', 'Two polynucleotide strands are wound around a common axis; one runs 5′→3′ and the other 3′→5′ because complementary bases can only pair with the correct geometry when the strands run in opposite directions.'),
       ('Explain why the bases in DNA are on the inside of the double helix.', 'The bases are relatively hydrophobic and pair by hydrogen bonding with complementary bases; the hydrophilic sugar–phosphate backbone faces the aqueous environment; this also protects the coded information.'),
       ('Explain how the structure of DNA makes it suitable for storing genetic information.', 'The sequence of bases along a strand can vary without restriction and carries the information; the double helix with covalent backbones is stable; complementary base pairing allows accurate copying and repair using one strand as a template.')],
  contrast=[('purines', 'pyrimidines', 'Purines (adenine, guanine) have a double ring; pyrimidines (cytosine, thymine, uracil) have a single ring; each base pair in DNA is one purine with one pyrimidine.'),
            ('the 5′ end', 'the 3′ end of a polynucleotide strand', 'The 5′ end terminates with a phosphate attached to carbon 5′ of the sugar; the 3′ end terminates with a free hydroxyl group on carbon 3′.')],
  misc=[('In DNA the two strands are joined by covalent bonds between the bases.', 'The strands are held together by hydrogen bonds between complementary bases; covalent bonds join nucleotides within each strand.'),
        ('A nucleotide is made of a sugar, a base and an amino acid.', 'A nucleotide consists of a pentose sugar, a phosphate group and a nitrogenous base; amino acids are the monomers of proteins.'),
        ('Both strands of DNA run in the same direction.', 'The strands are antiparallel: one runs 5′→3′ and the other 3′→5′.')],
  cases=[('Rosalind Franklin’s X-ray diffraction image “Photograph 51” (1952)', 'The X-shaped pattern revealed a helix with a regular repeat and the phosphate groups on the outside.', 'how evidence was used to build the model of DNA structure', 'Watson and Crick combined this evidence with Chargaff’s ratios and model building to propose a double helix with complementary base pairs – an example of models being built from several lines of evidence.'),
         ('Watson and Crick’s early failed triple-helix model', 'Their first model had three strands with bases on the outside and was quickly rejected by Franklin.', 'the role of model building and falsification in science', 'Models are tested against data; the incorrect model was discarded and revised into the double helix consistent with all evidence.')],
  apply=[('Draw and label a single DNA nucleotide. State what each label should show.', 'Pentagon labelled deoxyribose; circle (phosphate) attached to C5′; rectangle (base) attached to C1′; covalent bonds shown as lines.', 3),
         ('Draw a simple diagram of a section of DNA showing four nucleotides in two antiparallel strands. Outline the features it must show.', 'Two strands each of two nucleotides; sugar–phosphate backbones; bases paired A–T and C–G by hydrogen bonds (dashed); strands labelled 5′ and 3′ at opposite ends.', 4)],
  evaluate=[('Watson and Crick deserve the main credit for discovering the structure of DNA.', ['they built the first model consistent with all available evidence and proposed a copying mechanism', 'their insight into complementary base pairing was original'], ['their model relied on Rosalind Franklin’s X-ray data, used without her full knowledge', 'Chargaff’s base ratios and the work of Wilkins were essential'], 'Scientific discoveries are collaborative; Watson and Crick made the decisive synthesis, but Franklin, Wilkins and Chargaff provided essential evidence, so credit should be shared.')],
  extended=[('Describe the structure of DNA, including how the two strands are held together and how the structure allows replication.', 'Nucleotides: deoxyribose, phosphate, base; covalent sugar–phosphate backbone; two strands antiparallel; double helix; bases inside; A–T (2 H bonds), G–C (3 H bonds); purine with pyrimidine; complementary pairing means each strand is a template; hydrogen bonds easily broken for separation; sequence of bases stores information.', 7)],
  )


@R.add('ch02-st1', 'C3', (1, 4), 'numerical')
def hbonds(rng, slot):
    n = pick(rng, [12, 15, 18, 20, 24, 30])
    seq = ''.join(rng.choice('ATGC') for _ in range(n))
    gc = seq.count('G') + seq.count('C')
    at = n - gc
    hb = 2 * at + 3 * gc
    frames = [f'One strand of a short DNA molecule has the base sequence 5′-{seq}-3′. Calculate the total number of hydrogen bonds holding the two strands together.',
              f'A synthetic double-stranded DNA fragment contains the strand 5′-{seq}-3′ paired with its complement. How many hydrogen bonds join the two strands?']
    if slot.d >= 3:
        pgc = 100 * gc / n
        return num(pick(rng, frames) + ' Calculate also the percentage of G–C base pairs and predict how this fragment would compare in melting temperature with a fragment of equal length containing 25 % G–C.',
                   f'{hb} hydrogen bonds; {pgc:.0f} % G–C; ' + ('higher' if pgc > 25 else 'lower or similar') + ' melting temperature',
                   f'{at} A–T pairs × 2 + {gc} G–C pairs × 3 = {hb} (M1 A1); {gc}/{n} × 100 = {pgc:.0f} % (A1); more G–C = more hydrogen bonds = higher melting temperature (R1).', 4)
    return num(pick(rng, frames), f'{hb}', f'{at} A–T pairs × 2 = {2 * at}; {gc} G–C pairs × 3 = {3 * gc} (M1); total {hb} (A1).', 2)


COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

S('ch02-st2',
  terms=[('complementary base pairing', 'the specific pairing of adenine with thymine (or uracil in RNA) and guanine with cytosine by hydrogen bonds'),
         ('base sequence', 'the order of nucleotides along a nucleic acid strand, which encodes genetic information'),
         ('genetic code', 'the set of rules by which the base sequence of mRNA is translated into the amino acid sequence of a polypeptide'),
         ('template strand', 'a strand of nucleic acid whose base sequence is used to build a complementary strand'),
         ('genome', 'the whole of the genetic information of an organism')],
  facts=[('With which base does guanine pair in DNA?', 'cytosine', ['adenine', 'thymine', 'uracil'], 'G pairs with C by three hydrogen bonds.'),
         ('How many different base sequences are possible for a DNA strand that is 10 nucleotides long?', '4¹⁰ (about 1.05 million)', ['10⁴ (10 000)', '4 × 10 (40)', '2¹⁰ (1024)'], 'Each position can be any of 4 bases: 4ⁿ sequences.'),
         ('In RNA, adenine pairs with which base?', 'uracil', ['thymine', 'guanine', 'cytosine'], 'RNA contains uracil in place of thymine.'),
         ('Which feature of nucleic acids allows an almost limitless variety of genetic information to be stored?', 'there is no restriction on the sequence of bases along a strand', ['bases pair in only one way', 'the sugar–phosphate backbone varies', 'there are twenty different bases'], 'Any base can follow any other, so 4ⁿ sequences are possible.')],
  mc2=[('Why does complementary base pairing allow DNA to be copied accurately?', 'Each base can pair with only one other base, so each strand determines the sequence of the new strand.', ['All bases can pair with any other base.', 'Base pairs are joined by strong covalent bonds.', 'The sugar–phosphate backbone specifies the sequence.'], 'A–T and G–C specificity means a strand acts as a template.'),
       ('Which explains why A pairs with T rather than with C?', 'The shapes and positions of hydrogen-bonding groups match only for A–T and G–C.', ['A and C are both pyrimidines.', 'A–C pairs would be too narrow for the helix.', 'A and T are the same size.'], 'Specific hydrogen-bonding geometry determines pairing.'),
       ('Why is a sequence of three bases (a codon) needed to code for each amino acid?', 'Sequences of one or two bases give only 4 or 16 combinations, fewer than the 20 amino acids.', ['There are three types of RNA.', 'Each amino acid has three parts.', 'DNA has three strands.'], '4³ = 64 combinations is enough for 20 amino acids.')],
  mc3=[('A DNA strand has the sequence 5′-ATGCCA-3′. Which is the complementary strand, written 5′→3′?', '5′-TGGCAT-3′', ['5′-TACGGT-3′', '5′-ATGCCA-3′', '5′-UACGGU-3′'], 'Complement is 3′-TACGGT-5′; read 5′→3′ it is TGGCAT.'),
       ('A gene sequence is 1500 base pairs long. Assuming each position can be any of the four bases, how many different sequences of this length are possible?', '4¹⁵⁰⁰', ['1500⁴', '4 × 1500', '20¹⁵⁰⁰'], '4ⁿ with n = 1500.')],
  why=[('Explain how complementary base pairing allows DNA to act as a template.', 'Because A pairs only with T and G only with C, the sequence of one strand specifies the sequence of the complementary strand; when the strands separate, free nucleotides pair with the exposed bases, rebuilding the sequence exactly.'),
       ('Explain why the diversity of possible DNA base sequences is almost limitless.', 'Any of the four bases can occur at each position, with no restriction on order, so a strand of n nucleotides has 4ⁿ possible sequences; even short genes have astronomically many possibilities.'),
       ('Explain the significance of the genetic code being universal.', 'Almost all organisms use the same codons for the same amino acids; this is evidence for common ancestry and allows genes to be transferred between species (e.g. human insulin made in bacteria).')],
  contrast=[('the base pairing of DNA', 'the base pairing between DNA and RNA', 'In DNA adenine pairs with thymine and guanine with cytosine; when RNA pairs with DNA (or RNA with RNA) adenine pairs with uracil instead of thymine.')],
  misc=[('Adenine pairs with guanine because they are both purines.', 'A purine always pairs with a pyrimidine: adenine with thymine (or uracil) and guanine with cytosine.'),
        ('The genetic code is the sequence of bases in an individual’s DNA.', 'The genetic code is the set of codon-to-amino-acid rules; the base sequence is the specific information that the code is used to read.')],
  cases=[('the production of human insulin by genetically modified Escherichia coli', 'The human insulin gene was inserted into bacteria, which produced functional human insulin.', 'the universality of the genetic code and base sequence as information', 'Bacteria read the same codons as human cells, so the human base sequence is translated into the same amino acid sequence.')],
  evaluate=[('The base sequence of DNA alone determines all the characteristics of an organism.', ['the base sequence encodes proteins and functional RNAs that build and run the organism', 'mutations that change base sequences can change characteristics'], ['environmental factors and epigenetic modifications affect gene expression', 'identical twins with the same sequence can differ in characteristics'], 'Base sequence provides the information, but the phenotype results from its interaction with gene regulation and the environment, so it does not alone determine all characteristics.')],
  extended=[('Explain how the structure of DNA allows it to store and copy an almost unlimited range of genetic information.', 'Four bases; unrestricted sequence = 4ⁿ possibilities; information in base sequence; complementary pairing A–T, G–C; strands separate and each acts as template; specific pairing ensures accurate copies; hydrogen bonds easy to break; covalent backbone stable.', 6)],
  )


@R.add('ch02-st2', 'C3', (1, 4), 'numerical')
def complement(rng, slot):
    n = pick(rng, [8, 9, 10, 12])
    seq = ''.join(rng.choice('ATGC') for _ in range(n))
    comp = ''.join(COMP[b] for b in seq)
    rc = comp[::-1]
    f = rng.randrange(3)
    if f == 0:
        stem = f'One strand of DNA has the base sequence 5′-{seq}-3′. State the base sequence of the complementary strand, written in the 3′→5′ direction.'
        return num(stem, f"3′-{comp}-5′", f'Each base replaced by its complement (A↔T, G↔C) (M1); written 3′-{comp}-5′ (A1).', 2)
    if f == 1:
        stem = f'A section of the template strand of a gene reads 5′-{seq}-3′. Write the complementary DNA strand in the 5′→3′ direction.'
        return num(stem, f"5′-{rc}-3′", f'Complement 3′-{comp}-5′ (M1); reversed to read 5′-{rc}-3′ (A1).', 2)
    rna = comp.replace('T', 'U')
    stem = f'A DNA strand reads 5′-{seq}-3′. Give the sequence of an RNA strand that would be complementary to it, written 3′→5′, and state one difference from a DNA complement.'
    return num(stem, f"3′-{rna}-5′; uracil replaces thymine", f'Complementary bases with U opposite A (M1); 3′-{rna}-5′ (A1); U instead of T (A1).', 3)


@R.add('ch02-st2', 'C3', (1, 3), 'mcq')
def complement_mcq(rng, slot):
    n = 6
    seq = ''.join(rng.choice('ATGC') for _ in range(n))
    comp = ''.join(COMP[b] for b in seq)
    rc = comp[::-1]
    stem = f'Which sequence is complementary to 5′-{seq}-3′, written 5′→3′?'
    return nmcq(rng, stem, f'5′-{rc}-3′', [f'5′-{comp}-3′', f'5′-{seq[::-1]}-3′', f'5′-{rc.replace("T", "U")}-3′', f'5′-{seq}-3′'],
                f'Complement 3′-{comp}-5′ read 5′→3′ = {rc}.')


S('ch02-st3',
  terms=[('ribose', 'the pentose sugar in RNA nucleotides, which has a hydroxyl group on carbon 2′'),
         ('deoxyribose', 'the pentose sugar in DNA nucleotides, which lacks an oxygen (has H instead of OH) on carbon 2′'),
         ('uracil', 'the pyrimidine base found in RNA in place of thymine; it pairs with adenine'),
         ('messenger RNA (mRNA)', 'a single-stranded RNA copy of a gene that carries the coded information to ribosomes for translation'),
         ('ribonucleic acid', 'a usually single-stranded nucleic acid made of ribonucleotides containing the bases A, U, G and C')],
  facts=[('Which base is found in DNA but not in RNA?', 'thymine', ['uracil', 'adenine', 'cytosine'], 'RNA has uracil instead of thymine.'),
         ('Which sugar is found in RNA?', 'ribose', ['deoxyribose', 'glucose', 'fructose'], 'Ribose has an –OH group on C2′.'),
         ('How many strands does a typical mRNA molecule have?', 'one', ['two', 'three', 'four'], 'mRNA is single-stranded; DNA is usually double-stranded.'),
         ('Which statement about the number of strands in DNA and RNA is generally correct?', 'DNA is double-stranded and RNA is single-stranded.', ['Both are double-stranded.', 'DNA is single-stranded and RNA double-stranded.', 'Both are single-stranded.'], 'Exceptions exist in some viruses.')],
  mc2=[('Why is RNA generally less stable than DNA?', 'The 2′-OH group of ribose makes the backbone more susceptible to hydrolysis.', ['RNA contains thymine.', 'RNA is double-stranded.', 'RNA has no phosphate groups.'], 'The extra hydroxyl can attack the phosphodiester bond.'),
       ('Which feature is shared by DNA and RNA?', 'nucleotides linked by covalent bonds between sugar and phosphate', ['the base thymine', 'the sugar deoxyribose', 'a double-helical structure'], 'Both are polynucleotides with sugar–phosphate backbones.'),
       ('A nucleic acid sample contains 22 % uracil. What can be concluded?', 'The sample is RNA.', ['The sample is DNA.', 'The sample contains 22 % adenine.', 'The sample is double-stranded DNA.'], 'Uracil is found only in RNA; single-stranded RNA need not follow Chargaff’s ratios.')],
  mc3=[('An analysis of a viral genome gives: A 24 %, U 31 %, G 23 %, C 22 %. What type of genome does the virus have?', 'single-stranded RNA', ['double-stranded RNA', 'double-stranded DNA', 'single-stranded DNA'], 'Uracil indicates RNA; A ≠ U indicates single-stranded.'),
       ('Short-lived mRNA molecules are useful to a cell because', 'gene expression can be switched off quickly when the mRNA is broken down', ['they store genetic information permanently', 'they replicate themselves', 'they contain thymine'], 'Instability of RNA allows rapid regulation.')],
  why=[('Explain why the differences in structure between DNA and RNA suit their different functions.', 'DNA: double-stranded, deoxyribose (more stable), thymine – suits long-term, protected storage and accurate copying; RNA: single-stranded, ribose (less stable) – suits short-lived messenger roles, can fold into shapes (tRNA, rRNA) and be broken down quickly.'),
       ('Explain how a test for the presence of uracil could distinguish DNA from RNA.', 'Uracil is found only in RNA (thymine only in DNA), so detecting uracil in hydrolysed nucleic acid shows RNA is present.')],
  contrast=[('DNA', 'RNA', 'DNA contains deoxyribose, thymine and is usually double-stranded; RNA contains ribose, uracil instead of thymine and is usually single-stranded.'),
            ('ribose', 'deoxyribose', 'Ribose has a hydroxyl group on carbon 2′; deoxyribose has a hydrogen atom there (lacking one oxygen).')],
  misc=[('RNA contains thymine and deoxyribose, just like DNA.', 'RNA contains uracil instead of thymine and ribose instead of deoxyribose.'),
        ('All RNA molecules are single linear strands with no structure.', 'RNA is single-stranded but can fold and base-pair with itself, e.g. tRNA forms a clover-leaf shape and rRNA forms part of ribosome structure.')],
  cases=[('mRNA vaccines against COVID-19', 'Lipid nanoparticles deliver mRNA coding for the spike protein; cells translate it and the mRNA is soon degraded.', 'the structural differences between RNA and DNA', 'The instability of single-stranded RNA means it does not persist or enter the nucleus, so it is translated briefly then broken down.')],
  evaluate=[('RNA, rather than DNA, was the genetic material of the first living cells.', ['RNA can both store information and catalyse reactions (ribozymes)', 'ribose is produced more easily than deoxyribose in prebiotic chemistry experiments'], ['RNA is unstable and would degrade quickly', 'there is no direct fossil evidence of an RNA world'], 'The RNA world hypothesis is strongly supported by ribozymes and modern cell biology, but direct evidence is lacking; it remains the best current hypothesis rather than an established fact.')],
  extended=[('Compare and contrast the structure of DNA and RNA.', 'Similarities: both polynucleotides; sugar–phosphate backbone; covalent bonds between nucleotides; bases A, G, C in both; complementary pairing possible. Differences: deoxyribose vs ribose; thymine vs uracil; usually double-stranded helix vs single strand; DNA longer; DNA more stable.', 6)],
  )

CHARGAFF = [('human (Homo sapiens)', 30.9, 19.9, 19.8, 29.4), ('Escherichia coli', 24.7, 26.0, 25.7, 23.6),
            ('yeast (Saccharomyces cerevisiae)', 31.3, 18.7, 17.1, 32.9), ('wheat (Triticum aestivum)', 27.3, 22.7, 22.8, 27.1),
            ('sea urchin (Strongylocentrotus)', 32.8, 17.7, 17.3, 32.1), ('chicken (Gallus gallus)', 28.0, 22.0, 21.6, 28.4),
            ('salmon (Salmo salar)', 29.7, 20.8, 20.4, 29.1), ('octopus (Octopus vulgaris)', 33.2, 17.6, 17.6, 31.6)]

S('ch02-st4',
  terms=[('bacteriophage', 'a virus that infects bacteria, such as the T2 phage used by Hershey and Chase'),
         ('radioactive isotope labelling', 'the use of a radioactive form of an element (e.g. ³²P or ³⁵S) to trace where a molecule goes in an experiment'),
         ('Chargaff’s rules', 'the observation that in double-stranded DNA the amount of adenine equals thymine and guanine equals cytosine'),
         ('tetranucleotide hypothesis', 'the early idea that DNA was a simple repeating sequence of the four bases in equal amounts, and so could not carry genetic information')],
  facts=[('Which isotope did Hershey and Chase use to label the protein coat of T2 phage?', 'sulfur-35', ['phosphorus-32', 'carbon-14', 'nitrogen-15'], 'Proteins contain sulfur (in cysteine and methionine) but DNA does not.'),
         ('Which isotope did Hershey and Chase use to label phage DNA?', 'phosphorus-32', ['sulfur-35', 'nitrogen-15', 'oxygen-18'], 'DNA contains phosphorus in its backbone; proteins contain almost none.'),
         ('In the Hershey–Chase experiment, where was most ³²P found after blending and centrifugation?', 'in the pellet containing the bacteria', ['in the supernatant with the phage coats', 'evenly divided between pellet and supernatant', 'it was destroyed by the blender'], 'Phage DNA entered the bacteria, which sediment into the pellet.'),
         ('Which observation by Chargaff disproved the tetranucleotide hypothesis?', 'base proportions differ between species', ['all four bases are present in equal amounts', 'DNA contains phosphorus', 'DNA is found in the nucleus'], 'If DNA were a simple repeat, all species would have 25 % of each base.')],
  mc2=[('Why was sulfur used to label phage protein rather than phosphorus?', 'Proteins contain sulfur but DNA does not.', ['Sulfur is less radioactive than phosphorus.', 'DNA contains sulfur but proteins do not.', 'Phosphorus damages proteins.'], 'Each label must be specific to one type of molecule.'),
       ('What was the purpose of the blender in the Hershey–Chase experiment?', 'to detach the phage coats from the outside of the bacteria', ['to break open the bacteria', 'to kill the phages', 'to mix the radioactive isotopes'], 'The empty protein coats remain attached outside until sheared off.'),
       ('Chargaff found A ≈ T and G ≈ C in many species. How did this help Watson and Crick?', 'It suggested specific pairing of A with T and G with C.', ['It showed that DNA is single-stranded.', 'It proved that DNA is the genetic material.', 'It showed the helix has three strands.'], 'Equal ratios fit complementary base pairing.')],
  mc3=[('In double-stranded DNA from a species, 18 % of the bases are guanine. What percentage are adenine?', '32 %', ['18 %', '36 %', '64 %'], 'G = C = 18 %, so A + T = 64 % and A = 32 %.'),
       ('The DNA of virus φX174 contains A 24 %, T 31 %, G 23 %, C 22 %. What does this suggest?', 'Its DNA is single-stranded.', ['Its DNA is double-stranded.', 'Its genome is RNA.', 'Its bases do not pair.'], 'A ≠ T and G ≠ C, so there is no complementary second strand.')],
  why=[('Explain how the results of the Hershey–Chase experiment showed that DNA is the genetic material of T2 phage.', '³²P-labelled DNA entered the bacteria (found in the pellet) whereas ³⁵S-labelled protein stayed outside (supernatant); new phages were produced inside the bacteria, so the material that entered – DNA – must carry the genetic instructions.'),
       ('Explain how Chargaff’s data falsified the tetranucleotide hypothesis.', 'The hypothesis predicted equal amounts (25 %) of each base in all DNA; Chargaff showed base composition varied between species (e.g. A 31 % in humans vs 25 % in E. coli), so DNA is not a simple repeat and could carry varied information.'),
       ('Explain why Hershey and Chase used two separate batches of phage.', 'Each batch carried only one label so the location of protein and DNA could be traced independently; using both labels in one batch would not distinguish which molecule produced the radioactivity measured.')],
  contrast=[('the ³²P batch', 'the ³⁵S batch in the Hershey–Chase experiment', 'In the ³²P batch the DNA was labelled and most radioactivity was found in the pellet (inside bacteria); in the ³⁵S batch the protein coat was labelled and most radioactivity remained in the supernatant (outside bacteria).')],
  misc=[('Hershey and Chase found ³⁵S inside bacteria, proving protein is the genetic material.', 'Most ³⁵S remained outside in the supernatant with the phage coats; ³²P (DNA) entered the bacteria, showing DNA is the genetic material.'),
        ('Chargaff’s rules apply to all nucleic acids.', 'The A = T and G = C ratios apply to double-stranded DNA; single-stranded DNA or RNA genomes need not follow them.')],
  cases=[('the Hershey–Chase experiment of 1952', 'T2 phages labelled with ³²P or ³⁵S infected E. coli; after blending and centrifugation, ³²P was mainly in the bacterial pellet and ³⁵S in the supernatant.', 'the use of radioactive labelling to test a hypothesis', 'Specific labels allowed the fate of DNA and protein to be traced separately, providing evidence that DNA enters the cell and carries genetic information.')],
  sources=[('Hershey and Chase reported that after blending for several minutes about 80 % of the ³⁵S was released into the supernatant, while only about 20–35 % of the ³²P was released; most ³²P remained with the bacteria, and about 30 % of it was passed on to the next generation of phages.', 'Summary of Hershey, A. D. and Chase, M. (1952) J. Gen. Physiol. 36: 39–56', 'Explain why these results were considered strong but not conclusive evidence that DNA is the genetic material.', 'Strong: most DNA entered and some ³²P appeared in progeny; most protein stayed outside. Not conclusive: about 20 % of ³⁵S remained with bacteria, so some protein may have entered; blending was incomplete; the result was for one phage only; other evidence (Avery 1944, Chargaff) was needed.')],
  evaluate=[('The Hershey–Chase experiment proved that DNA is the genetic material of all organisms.', ['labelled DNA entered bacteria and was associated with new phage production', 'the result supported earlier work by Avery, MacLeod and McCarty'], ['the experiment used only one virus, so generalising to all organisms is not justified', 'some protein contamination occurred, so the result was not absolute'], 'It provided strong evidence for one phage; acceptance for all organisms relied on the convergence of several independent lines of evidence, so “proved for all organisms” overstates it.')],
  extended=[('Describe the Hershey–Chase experiment and explain how its results, together with Chargaff’s data, contributed to understanding of the nature of the genetic material.', 'Two batches of T2 phage: ³⁵S labels protein, ³²P labels DNA; infect E. coli; blend to remove coats; centrifuge – bacteria in pellet; ³²P in pellet, ³⁵S in supernatant; DNA enters cell, directs phage production. Chargaff: base composition varies between species – falsifies tetranucleotide hypothesis – DNA can carry information; A = T, G = C – supported complementary base pairing in Watson–Crick model.', 8)],
  )


@R.add('ch02-st4', 'C3', (1, 4), 'numerical')
def chargaff_calc(rng, slot):
    sp = pick(rng, ['a species of fern', 'a marine bacterium', 'a mouse cell line', 'a sample of maize DNA', 'a deep-sea archaeon', 'the DNA of a frog', 'a plasmid from Bacillus'])
    known = pick(rng, ['A', 'G', 'C', 'T'])
    v = round(rng.uniform(14, 36), 1)
    if known in 'AT':
        a = v
        g = (100 - 2 * a) / 2
    else:
        g = v
        a = (100 - 2 * g) / 2
    vals = {'A': a, 'T': a, 'G': g, 'C': g}
    nm = {'A': 'adenine', 'T': 'thymine', 'G': 'guanine', 'C': 'cytosine'}
    stem = f'Analysis of double-stranded DNA from {sp} shows that {v} % of the bases are {nm[known]}. Calculate the percentage of each of the other three bases.'
    ans = ', '.join(f'{nm[b]} {vals[b]:.1f} %' for b in 'ATGC' if b != known)
    key = f'{nm[known]} pairs with {nm[COMP[known]]} so it is also {v} % (A1); remaining {100 - 2 * v:.1f} % shared equally by the other pair = {(100 - 2 * v) / 2:.1f} % each (A1).'
    if slot.d >= 3:
        stem += ' Explain why this calculation would not be valid for a single-stranded viral genome.'
        ans += '; in single-stranded nucleic acid bases are not paired, so A need not equal T and G need not equal C.'
        key += ' No complementary strand in a single-stranded genome so Chargaff’s equalities need not hold (R1).'
        return num(stem, ans, key, 3)
    return num(stem, ans, key, 2)


def _chargaff_dq(rng, slot):
    rows = rng.sample(CHARGAFF, 4)
    virus = rng.random() < 0.6
    data = [(r[0], r[1], r[2], r[3], r[4]) for r in rows]
    if virus:
        data.append(('bacteriophage φX174', 24.0, 23.3, 21.5, 31.2))
    who = pick(rng, data[:4])
    at = who[1] / who[4]
    gc = who[2] / who[3]
    pur = (who[1] + who[2]) / (who[3] + who[4])
    intro = ('In the late 1940s Erwin Chargaff analysed the base composition of DNA from many organisms. Some of his results (percentage of each base) are shown.\n\n'
             + table(['Source of DNA', 'A', 'G', 'C', 'T'], [(r[0], r[1], r[2], r[3], r[4]) for r in data]))
    sp_hi = max(data[:4], key=lambda r: r[2] + r[3])
    parts = [
        (f'Calculate the ratio of A to T and of G to C for {who[0]}.', f'A/T = {at:.2f}; G/C = {gc:.2f}', f'{who[1]}/{who[4]} = {at:.2f} (A1); {who[2]}/{who[3]} = {gc:.2f} (A1).', 2),
        (f'Calculate the ratio of purines to pyrimidines, (A + G)/(C + T), for {who[0]}.', f'{pur:.2f}', f'({who[1]} + {who[2]})/({who[3]} + {who[4]}) (M1) = {pur:.2f} (A1).', 2),
        ('Identify the organism in the table whose DNA has the highest proportion of G + C.', f'{sp_hi[0]} ({sp_hi[2] + sp_hi[3]:.1f} %)', f'{sp_hi[0]} (A1).', 1),
        ('Explain how these data support the model of DNA proposed by Watson and Crick.', 'A ≈ T and G ≈ C in each species, consistent with complementary base pairing of A with T and G with C in a double-stranded molecule; purine/pyrimidine ≈ 1 fits one purine pairing with one pyrimidine.', 'A ≈ T and G ≈ C (A1); complementary base pairing (R1); purine with pyrimidine / ratio ≈ 1 (R1).', 3),
        ('Explain how the data falsify the tetranucleotide hypothesis.', 'The hypothesis predicts 25 % of each base in all DNA; proportions differ markedly between species (e.g. A from about 25 % to over 30 %), so DNA is not a simple repeating unit.', 'Prediction of 25 % each (A1); observed variation between species (R1).', 2),
        ('Suggest why the ratios are not exactly 1.00.', 'Experimental/measurement error in hydrolysis and chromatography; incomplete separation of bases; impurities.', 'Any valid source of experimental error (A1).', 1),
    ]
    if virus:
        parts.insert(4, ('Deduce, with a reason, the structure of the genetic material of bacteriophage φX174.', 'Single-stranded DNA: A (24.0) ≠ T (31.2) and G ≠ C, so bases are not paired.', 'Single-stranded (A1); A ≠ T / G ≠ C so no complementary strand (R1).', 2))
    return intro, parts


data_q(R, 'ch02-st4', _chargaff_dq)


def _hershey_dq(rng, slot):
    times = [0, 1, 2, 4, 6, 8]
    s_max = rng.uniform(76, 84)
    p_max = rng.uniform(22, 32)
    inf = rng.uniform(95, 99)
    s = [round(s_max * (1 - math.exp(-t / 1.2)) * rng.uniform(0.97, 1.03), 0) if t else 0 for t in times]
    p = [round(p_max * (1 - math.exp(-t / 1.2)) * rng.uniform(0.95, 1.05), 0) if t else 0 for t in times]
    intro = ('In the Hershey–Chase experiment, E. coli infected with radioactively labelled T2 phage were agitated in a blender for different times. '
             'The percentage of each isotope released into the supernatant and the percentage of bacteria still infected were measured.\n\n'
             + table(['Blending time / min', '³⁵S released / %', '³²P released / %'], [(t, f'{a:.0f}', f'{b:.0f}') for t, a, b in zip(times, s, p)])
             + f'\n\nAfter 8 minutes {inf:.0f} % of bacteria were still infected.')
    parts = [
        ('State the percentage of ³⁵S released after 4 minutes of blending.', f'{s[3]:.0f} %', f'{s[3]:.0f} % (A1).', 1),
        ('Compare the release of ³⁵S and ³²P during blending.', f'Both rise quickly in the first 2 minutes and then level off; far more ³⁵S (about {s[-1]:.0f} %) than ³²P (about {p[-1]:.0f} %) is released.', 'Both increase then plateau (A1); ³⁵S release much greater than ³²P at each time (A1).', 2),
        ('Calculate the difference between the percentages of ³⁵S and ³²P remaining with the bacteria after 8 minutes.', f'{(100 - p[-1]) - (100 - s[-1]):.0f} percentage points', f'³²P remaining {100 - p[-1]:.0f} %, ³⁵S remaining {100 - s[-1]:.0f} % (M1); difference {(100 - p[-1]) - (100 - s[-1]):.0f} (A1).', 2),
        ('Explain why the percentage of bacteria still infected is important in interpreting the results.', 'It shows that blending did not stop infection: the genetic material had already entered the cells, so the coats removed by blending (³⁵S) were not needed for infection.', 'Blending does not prevent infection (A1); so material in the supernatant (protein) is not required (R1).', 2),
        ('Explain what the results suggest about the nature of the genetic material.', 'DNA (³²P) mostly remains with/inside the bacteria while protein (³⁵S) is mostly removed; infection continues, so DNA is the material that enters and directs phage production.', 'DNA enters cells (A1); protein stays outside (A1); DNA carries genetic information (R1).', 3),
        ('Suggest why about 20 % of ³⁵S was never released.', 'Some coats remained attached to cells even after blending / some protein entered / incomplete separation in centrifugation.', 'Any valid suggestion (A1).', 1),
        ('Explain why radioactive sulfur and phosphorus were used as labels.', 'Sulfur is found in proteins (some amino acids) but not DNA; phosphorus is in DNA (phosphate groups) but not in protein, so each label tracks one molecule.', 'S in protein only (A1); P in DNA only (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch02-st4', _hershey_dq)


# =============================================================================================
# ch03 A2.1–A2.3 Cells: origins, structure and viruses
# =============================================================================================
S('ch03-st1',
  terms=[('abiogenesis', 'the origin of life from non-living matter through natural chemical processes'),
         ('protocell', 'a self-organised, membrane-bound compartment of organic molecules proposed as a precursor of living cells'),
         ('LUCA', 'the last universal common ancestor, the most recent population of organisms from which all life on Earth descends'),
         ('RNA world hypothesis', 'the hypothesis that early life used RNA both to store genetic information and to catalyse reactions, before DNA and proteins'),
         ('ribozyme', 'an RNA molecule that acts as an enzyme, catalysing a chemical reaction')],
  facts=[('Which gases were used in the Miller–Urey experiment to simulate the early atmosphere?', 'methane, ammonia, hydrogen and water vapour', ['oxygen, nitrogen and carbon dioxide', 'oxygen and water vapour only', 'carbon dioxide and ozone'], 'A reducing atmosphere without free oxygen was assumed.'),
         ('What did the Miller–Urey experiment produce?', 'amino acids and other simple organic molecules', ['living cells', 'DNA molecules', 'proteins with enzyme activity'], 'Electrical discharges simulated lightning; amino acids formed.'),
         ('Which condition is thought to have been absent from the atmosphere of the early Earth?', 'free oxygen', ['water vapour', 'carbon dioxide', 'nitrogen'], 'Oxygen accumulated only after photosynthesis evolved.'),
         ('Where is LUCA thought most likely to have lived, according to genomic evidence?', 'around hydrothermal vents', ['in polar ice', 'in the upper atmosphere', 'in freshwater ponds rich in oxygen'], 'Genes inferred for LUCA suggest a thermophilic, anaerobic lifestyle using H₂.'),
         ('Approximately how long ago did the earliest cells appear on Earth?', 'about 3.5–4 billion years ago', ['about 500 million years ago', 'about 65 million years ago', 'about 10 billion years ago'], 'Fossil stromatolites and isotopic evidence date to about 3.5 bya or earlier.')],
  mc2=[('Why could cells not have arisen by spontaneous generation in today’s conditions?', 'Existing organisms would consume organic molecules, and free oxygen would oxidise them.', ['Modern Earth has no water.', 'Organic molecules can no longer be formed.', 'Lightning no longer occurs.'], 'Pasteur showed cells arise from pre-existing cells today.'),
       ('Why is RNA thought to have preceded DNA in early life?', 'RNA can both store information and catalyse reactions.', ['RNA is more stable than DNA.', 'RNA contains thymine.', 'RNA is double-stranded.'], 'Ribozymes allow RNA to self-replicate without proteins.'),
       ('What is the main significance of spontaneous formation of vesicles from fatty acids in water?', 'It shows how membrane-bound compartments could form without cells.', ['It shows how DNA was formed.', 'It proves life began in water.', 'It shows vesicles can replicate genes.'], 'Amphipathic molecules self-assemble into bilayers.')],
  mc3=[('In a modern repeat of the Miller–Urey experiment, oxygen was added to the gas mixture and almost no amino acids formed. What is the best interpretation?', 'Organic synthesis requires a reducing atmosphere lacking free oxygen.', ['Oxygen is needed to make amino acids.', 'Electrical sparks do not work in oxygen.', 'Amino acids can only form in water.'], 'Oxygen oxidises the intermediates.'),
       ('A protocell model consists of fatty-acid vesicles containing short RNA strands. Which property of life is it least able to show?', 'metabolism using enzymes made by the protocell', ['compartmentalisation', 'growth by taking up fatty acids', 'division into smaller vesicles'], 'Such models lack a metabolic network.')],
  why=[('Explain the main stages that must have occurred for the first cells to arise from non-living material.', 'Synthesis of simple organic molecules (e.g. amino acids, nucleotides) from inorganic compounds; assembly into polymers; development of self-replicating molecules (e.g. RNA) to allow inheritance; enclosure of these molecules in membranes to form compartments (protocells) with a separate internal chemistry.'),
       ('Explain why the Miller–Urey experiment is considered evidence for, but not proof of, abiogenesis.', 'It showed organic molecules such as amino acids can form from inorganic gases with an energy source; but it did not produce polymers, replication or cells, and the actual composition of the early atmosphere is uncertain.'),
       ('Explain why RNA is a strong candidate for the first genetic material.', 'RNA stores information in its base sequence and can catalyse reactions as ribozymes (e.g. peptide-bond formation in ribosomes), so it could replicate itself without proteins.')],
  contrast=[('the Miller–Urey hypothesis', 'the hydrothermal vent hypothesis for the origin of life', 'Miller–Urey proposes organic molecules formed in a reducing atmosphere powered by lightning; the vent hypothesis proposes they formed in deep-sea vents using chemical energy from H₂ and mineral gradients.')],
  misc=[('The Miller–Urey experiment created living cells from gases.', 'It produced only simple organic molecules such as amino acids, not polymers or cells.'),
        ('The first cells probably used DNA and proteins just like modern cells.', 'The RNA world hypothesis proposes that RNA served as both genetic material and catalyst before DNA and proteins evolved.')],
  cases=[('the Miller–Urey experiment (1953)', 'Electric sparks passed through methane, ammonia, hydrogen and water produced several amino acids within a week.', 'how conditions on early Earth may have produced organic molecules', 'It showed that, with an energy source and a reducing atmosphere, monomers needed for life form spontaneously.'),
         ('the discovery of ribozymes by Thomas Cech and Sidney Altman', 'Some RNA molecules were found to catalyse their own cutting and joining reactions.', 'the RNA world hypothesis', 'It showed that RNA can act as an enzyme as well as store information, so RNA could have been self-replicating.')],
  evaluate=[('The origin of the first cells can be explained by testable scientific hypotheses.', ['individual stages such as monomer synthesis (Miller–Urey) and vesicle formation have been reproduced in laboratories', 'ribozymes and genomic reconstruction of LUCA provide indirect evidence'], ['the actual conditions of early Earth cannot be observed directly', 'no experiment has produced a living cell from non-living matter'], 'Each stage is supported by experiments, but the whole process remains a hypothesis supported by indirect evidence; it is scientifically testable in parts but not fully explained.')],
  extended=[('Outline the conditions on the early Earth and explain how experiments have tested hypotheses about the origin of the first cells.', 'Conditions: reducing atmosphere (CH₄, NH₃, H₂, H₂O), no O₂, high UV, lightning, volcanic activity, high temperatures. Stages: monomers → polymers → self-replication → membranes. Miller–Urey produced amino acids; fatty-acid vesicles form spontaneously; ribozymes support RNA world; hydrothermal vent experiments; limitations – conditions uncertain, no cell produced.', 8)],
  )


ORGS = [('a mitochondrion', 'µm', 0.8, 3.0), ('an Escherichia coli cell', 'µm', 1.5, 3.0), ('a red blood cell', 'µm', 6.5, 8.0),
        ('a chloroplast', 'µm', 3.0, 7.0), ('a lymphocyte', 'µm', 7.0, 12.0), ('a yeast cell', 'µm', 3.0, 8.0),
        ('a nucleus', 'µm', 5.0, 10.0), ('a pollen grain', 'µm', 20.0, 50.0), ('a Paramecium', 'µm', 120.0, 250.0),
        ('a T4 bacteriophage', 'nm', 180.0, 230.0), ('an influenza virus particle', 'nm', 80.0, 120.0), ('a ribosome', 'nm', 20.0, 30.0),
        ('a palisade mesophyll cell', 'µm', 40.0, 100.0), ('a sperm cell head', 'µm', 4.0, 6.0), ('a cheek epithelial cell', 'µm', 40.0, 80.0)]


def _to_um(v, u):
    return v / 1000 if u == 'nm' else v


S('ch03-st2',
  terms=[('magnification', 'how many times larger an image is than the actual object; magnification = image size ÷ actual size'),
         ('resolution', 'the ability to distinguish two points that are close together as separate; the minimum distance at which they can be seen as separate'),
         ('cell theory', 'the theory that all living organisms are composed of cells, the cell is the smallest unit of life, and cells only arise from pre-existing cells'),
         ('scale bar', 'a line on a micrograph or drawing that represents a stated actual length, allowing sizes to be calculated'),
         ('freeze-fracture electron microscopy', 'a technique in which a frozen specimen is split along weak planes such as the middle of membranes and a replica of the surface is imaged'),
         ('cryogenic electron microscopy', 'electron microscopy of samples frozen rapidly in vitreous ice, allowing the structure of proteins to be determined at near-atomic resolution')],
  facts=[('Which unit is 1000 times smaller than a micrometre?', 'nanometre', ['millimetre', 'centimetre', 'picometre'], '1 µm = 1000 nm.'),
         ('What is the approximate maximum resolution of a light microscope?', '0.2 µm (200 nm)', ['2 nm', '0.2 nm', '20 µm'], 'Resolution is limited by the wavelength of visible light.'),
         ('Why does an electron microscope have a higher resolution than a light microscope?', 'electrons have a much shorter wavelength than light', ['electrons travel faster than light', 'the specimen is stained more strongly', 'electron microscopes use more lenses'], 'Resolution depends on wavelength.'),
         ('Which technique allows living cells to be viewed with specific proteins fluorescently labelled?', 'fluorescent stains/immunofluorescence in light microscopy', ['transmission electron microscopy', 'freeze-fracture', 'scanning electron microscopy of gold-coated cells'], 'Electron microscopy requires dead, fixed specimens in a vacuum.'),
         ('Which is a deductive conclusion of cell theory?', 'a newly discovered organism will be made of one or more cells', ['all cells contain chloroplasts', 'cells arise spontaneously from non-living matter', 'all cells are the same size'], 'Cell theory generalises from observations to predictions.')],
  mc2=[('Which observation is an exception, or a challenge, to the cell theory?', 'striated muscle fibres that contain many nuclei and are much longer than typical cells', ['a red blood cell of a frog containing a nucleus', 'an onion epidermis cell with a cell wall', 'a bacterium dividing by binary fission'], 'Muscle fibres challenge the idea of a cell as a single unit with one nucleus.'),
       ('Why is the magnification of a micrograph not a measure of how much detail is visible?', 'Detail depends on resolution; enlarging beyond the resolution limit gives a blurred image.', ['Magnification and resolution are the same thing.', 'Higher magnification always shows more detail.', 'Resolution depends only on the eyepiece.'], 'Empty magnification adds no detail.'),
       ('Why must specimens for electron microscopy be dead?', 'They are placed in a vacuum and must be fixed and stained with heavy metals.', ['Electrons kill living cells instantly but leave no damage.', 'Living cells are transparent to electrons.', 'Living cells move too fast.'], 'Vacuum and preparation methods prevent observing live cells.')],
  mc3=[('An image of a cell is 45 mm long at × 1500 magnification. What is the actual length of the cell?', '30 µm', ['3 µm', '300 µm', '67.5 µm'], '45 mm = 45 000 µm; 45 000/1500 = 30 µm.'),
       ('A scale bar 20 mm long on a micrograph represents 5 µm. What is the magnification?', '× 4000', ['× 400', '× 40 000', '× 100'], '20 mm = 20 000 µm; 20 000/5 = 4000.')],
  why=[('Explain why the resolution of an electron microscope is greater than that of a light microscope.', 'Resolution is limited by the wavelength of the radiation used; electron beams have a wavelength far shorter than visible light, so points much closer together (down to about 0.1–1 nm) can be distinguished.'),
       ('Explain how the cell theory was developed using inductive reasoning.', 'Many observations of different organisms (e.g. by Schleiden of plants and Schwann of animals) all showed cells; from these repeated observations a general theory that all organisms consist of cells was proposed, which is then tested by further observation.'),
       ('Explain why it is important to include a scale bar on a micrograph.', 'A scale bar shows the actual length represented, so sizes can be calculated even if the image is enlarged or reduced; a stated magnification becomes wrong if the image is resized.'),
       ('Explain the advantages of using fluorescent stains and immunofluorescence in light microscopy.', 'They label specific molecules (e.g. a protein with an antibody linked to a fluorescent dye), showing their location in cells; living cells can be used and several components labelled in different colours.')],
  contrast=[('magnification', 'resolution', 'Magnification is how many times larger the image is than the object; resolution is the smallest distance between two points that can still be distinguished; increasing magnification without improving resolution gives no extra detail.'),
            ('light microscopes', 'electron microscopes', 'Light microscopes use light, have resolution about 200 nm, can view living cells in colour; electron microscopes use electron beams, resolve down to about 0.1–1 nm, need dead specimens in a vacuum and give black-and-white images.')],
  misc=[('A higher magnification always shows more detail.', 'Detail depends on resolution; beyond the resolving limit, more magnification only enlarges a blurred image.'),
        ('To find the actual size of a cell, multiply the image size by the magnification.', 'Actual size = image size ÷ magnification; both lengths must be in the same units.'),
        ('Electron microscopes can be used to watch living cells divide.', 'Specimens for electron microscopy must be dead because they are fixed, stained and held in a vacuum.')],
  cases=[('Robert Hooke’s observation of cork cells in 1665', 'Hooke saw small box-like compartments in cork and named them “cells”.', 'the development of cell theory', 'His observations were among the first of many that led, by induction, to the generalisation that all organisms are made of cells.'),
         ('the use of cryogenic electron microscopy to determine the structure of the SARS-CoV-2 spike protein in 2020', 'Within weeks, cryo-EM revealed the spike protein’s shape at near-atomic resolution.', 'how developments in microscopy improve biological understanding', 'Rapid freezing preserves the native structure and the short electron wavelength gives very high resolution, supporting vaccine design.')],
  evaluate=[('Cell theory is a universal principle with no significant exceptions.', ['all organisms examined so far are made of cells, and cells arise from pre-existing cells', 'cell theory successfully predicts the structure of newly discovered organisms'], ['striated muscle fibres, aseptate fungal hyphae and giant algae such as Acetabularia do not fit the idea of a typical single-nucleus cell', 'viruses are not cellular yet show some properties of life'], 'Cell theory is robust as a general theory; apparent exceptions refine rather than overturn it, showing that scientific theories are generalisations that accommodate atypical cases.')],
  extended=[('Compare light and electron microscopy and explain how each has contributed to our understanding of cell structure.', 'Light: visible light, resolution ~200 nm, living specimens, colour stains, fluorescence, view cell divisions, nuclei, chloroplasts. Electron (TEM/SEM): electrons, resolution ~1 nm, dead specimens in vacuum, ultrastructure – membranes, ribosomes, mitochondrial cristae; freeze-fracture showed proteins spanning membranes; cryo-EM protein structure.', 8)],
  )


@R.add('ch03-st2', 'C3', (1, 5), 'numerical')
def magnification(rng, slot):
    obj, u, lo, hi = pick(rng, ORGS)
    actual = round(rng.uniform(lo, hi), 1 if u == 'µm' and hi < 20 else 0)
    if actual <= 0:
        return None
    a_um = _to_um(actual, u)
    mag = pick(rng, [400, 500, 800, 1000, 1200, 1500, 2000, 2500, 4000, 5000, 8000, 10000, 20000, 25000, 40000, 50000, 100000, 150000, 200000])
    img_mm = a_um * mag / 1000
    if not 5 <= img_mm <= 200:
        return None
    img_mm = round(img_mm, 0 if img_mm >= 20 else 1)
    f = rng.randrange(4) if slot.d >= 2 else rng.randrange(2)
    who = name(rng)
    a_real = img_mm * 1000 / mag
    out_u = 'nm' if a_real < 1 else 'µm'
    a_show = a_real * 1000 if out_u == 'nm' else a_real
    if f == 0:
        stem = f'A micrograph of {obj} has a magnification of × {mag}. The image is {sf(img_mm)} mm long. Calculate the actual length of {obj} in {out_u}.'
        return num(stem, f'{sf(a_show)} {out_u}', f'Actual size = image size ÷ magnification (M1); {sf(img_mm)} mm = {sf(img_mm * 1000)} µm; ÷ {mag} = {sf(a_show)} {out_u} (A1).', 2)
    if f == 1:
        stem = f'{who} measured the image of {obj} on a printed electron micrograph as {sf(img_mm)} mm. The actual length of {obj} is {sf(actual)} {u}. Calculate the magnification of the image.'
        return num(stem, f'× {sf(img_mm * 1000 / a_um)}', f'Magnification = image ÷ actual (M1); {sf(img_mm * 1000)} µm ÷ {sf(a_um)} µm = × {sf(img_mm * 1000 / a_um)} (A1); units must match.', 2)
    if f == 2:
        bar_um = pick(rng, [0.5, 1, 2, 5, 10, 20, 50]) if u == 'µm' else pick(rng, [50, 100, 200])
        bar_um_v = bar_um if u == 'µm' else bar_um / 1000
        bar_mm = round(bar_um_v * mag / 1000, 1)
        if not 5 <= bar_mm <= 60:
            return None
        m_real = bar_mm * 1000 / bar_um_v
        act = img_mm / bar_mm * bar_um_v
        act_show = act * 1000 if u == 'nm' else act
        stem = (f'An electron micrograph of {obj} has a scale bar labelled {bar_um} {u} that measures {bar_mm} mm. The image of {obj} is {sf(img_mm)} mm long. '
                f'(a) Calculate the magnification. (b) Calculate the actual length of {obj}.')
        return num(stem, f'(a) × {sf(m_real)}; (b) {sf(act_show)} {u}',
                   f'(a) {bar_mm} mm = {sf(bar_mm * 1000)} µm ÷ {bar_um_v} µm = × {sf(m_real)} (A1). (b) {sf(img_mm)}/{bar_mm} × {bar_um} {u} (M1) = {sf(act_show)} {u} (A1).', 3)
    # f == 3: drawing size required
    want_mag = pick(rng, [m for m in (500, 1000, 2000, 5000, 10000, 20000, 50000) if 20 <= a_um * m / 1000 <= 150] or [mag])
    draw_mm = a_um * want_mag / 1000
    stem = (f'{obj[0].upper() + obj[1:]} is {sf(actual)} {u} long. A student is asked to draw it at a magnification of × {want_mag}. Calculate how long the drawing should be in millimetres, and explain why '
            f'the magnification of a drawing should be stated or a scale bar added.')
    return num(stem, f'{sf(draw_mm)} mm', f'Image = actual × magnification (M1); {sf(a_um)} µm × {want_mag} = {sf(a_um * want_mag)} µm = {sf(draw_mm)} mm (A1); so the reader can determine real size / the image may be resized (R1).', 3)


@R.add('ch03-st2', 'C3', (1, 4), 'mcq')
def magnification_mcq(rng, slot):
    obj, u, lo, hi = pick(rng, ORGS)
    a_um = _to_um(round(rng.uniform(lo, hi), 1), u)
    mag = pick(rng, [400, 1000, 2000, 5000, 10000, 20000, 50000, 100000])
    img = a_um * mag / 1000
    if not 5 <= img <= 150:
        return None
    img = round(img)
    act = img * 1000 / mag
    show = lambda v: f'{sf(v * 1000)} nm' if v < 1 else f'{sf(v)} µm'  # noqa: E731
    stem = f'The image of {obj} in a micrograph at × {mag} is {img} mm long. What is its actual length?'
    return nmcq(rng, stem, show(act), [show(act * 10), show(act / 10), show(act * 1000), show(img / mag)],
                f'{img} mm = {img * 1000} µm; ÷ {mag} = {show(act)}.')


def _graticule(rng, slot):
    obj = pick(rng, [('guard cells', 30, 50), ('onion epidermal cells', 150, 300), ('human cheek cells', 40, 70), ('Elodea leaf cells', 40, 80), ('yeast cells', 4, 8), ('red blood cells of a frog', 18, 24)])
    objective = pick(rng, [(10, 10.0), (40, 2.5), (100, 1.0)])
    if obj[2] < 15:
        objective = (100, 1.0)
    elif obj[2] > 200:
        objective = (10, 10.0)
    elif objective[0] == 100:
        objective = (40, 2.5)
    per = objective[1]
    sizes = [rng.uniform(obj[1], obj[2]) for _ in range(6)]
    epu = [round(s / per) for s in sizes]
    if len(set(epu)) < 3 or min(epu) < 2:
        return None
    um = [e * per for e in epu]
    m, s = mean(um), sd(um)
    who = name(rng)
    intro = (f'{who} measured six {obj[0]} using an eyepiece graticule with the × {objective[0]} objective lens. A stage micrometer showed that at this magnification '
             f'one eyepiece unit (epu) = {per} µm.\n\n' + table(['Cell', '1', '2', '3', '4', '5', '6'], [['Length / epu'] + epu]))
    big = max(um)
    fov = pick(rng, [400, 450, 500]) if objective[0] == 40 else (1800 if objective[0] == 10 else 180)
    parts = [
        ('Calculate the actual length of cell 1 in µm.', f'{epu[0] * per:g} µm', f'{epu[0]} × {per} = {epu[0] * per:g} µm (A1).', 1),
        ('Calculate the mean length of the six cells.', f'{m:.1f} µm', f'Converts each to µm or mean epu × {per} (M1); {m:.1f} µm (A1).', 2),
        ('Calculate the standard deviation of the cell lengths.', f'{s:.1f} µm', f'SD (n − 1) = {s:.1f} µm (A1); accept population SD {math.sqrt(sum((x - m) ** 2 for x in um) / 6):.1f}.', 1),
        (f'The diameter of the field of view is {fov} µm. Estimate how many of the longest cells would fit across the field of view end to end.', f'{int(fov // big)}', f'{fov}/{big:g} = {fov / big:.1f} → {int(fov // big)} whole cells (A1).', 1),
        ('Explain why the eyepiece graticule must be recalibrated when the objective lens is changed.', 'The graticule is in the eyepiece, so its divisions stay the same size while the specimen image is magnified by different amounts; the actual length represented by one epu changes.', 'Graticule scale fixed / specimen magnification changes (A1); epu value changes (A1).', 2),
        ('Suggest why a sample of at least six cells was measured.', 'Cells vary in size; a larger sample gives a more representative/reliable mean and allows variation (SD) to be estimated.', 'Biological variation (A1); reliable mean / representative (A1).', 2),
        ('Calculate the magnification of a drawing in which cell 1 is drawn 60 mm long.', f'× {sf(60000 / (epu[0] * per))}', f'60 mm = 60 000 µm ÷ {epu[0] * per:g} µm (M1) = × {sf(60000 / (epu[0] * per))} (A1).', 2),
        ('Explain why a stage micrometer is needed to calibrate the eyepiece graticule.', 'The stage micrometer has divisions of known size (10 µm), so the value of each eyepiece unit can be calculated at that magnification.', 'Known scale (A1); calculation of eyepiece unit value (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch03-st2', _graticule)

S('ch03-st3',
  terms=[('prokaryote', 'an organism whose cell lacks a nucleus and membrane-bound organelles; its DNA is a naked circular loop in the cytoplasm'),
         ('nucleoid', 'the region of a prokaryotic cell where the circular DNA is located, not enclosed by a membrane'),
         ('plasmid', 'a small circle of DNA, separate from the main chromosome, found in many prokaryotes'),
         ('70S ribosome', 'the smaller type of ribosome found in prokaryotes (and mitochondria and chloroplasts)'),
         ('80S ribosome', 'the larger type of ribosome found in the cytoplasm and on the rough ER of eukaryotic cells'),
         ('compartmentalisation', 'the division of a eukaryotic cell into membrane-bound organelles so that different processes can occur in separate, optimised environments')],
  facts=[('Which structure is found in all prokaryotic cells?', '70S ribosomes', ['a nucleus', 'mitochondria', 'a cellulose cell wall'], 'Prokaryotes lack membrane-bound organelles but all have ribosomes.'),
         ('What is the main component of the cell wall of most bacteria?', 'peptidoglycan', ['cellulose', 'chitin', 'phospholipid'], 'Plants use cellulose, fungi chitin.'),
         ('Which structure is present in plant cells but absent from animal cells?', 'a cellulose cell wall', ['a nucleus', 'mitochondria', 'ribosomes'], 'Plants also have chloroplasts and a large permanent vacuole.'),
         ('Which organelle is the site of aerobic respiration in eukaryotic cells?', 'mitochondrion', ['ribosome', 'Golgi apparatus', 'lysosome'], 'Krebs cycle and oxidative phosphorylation occur in mitochondria.'),
         ('Which structure would be found in a fungal cell but not in an animal cell?', 'a cell wall made of chitin', ['centrioles', 'a nucleus', 'Golgi apparatus'], 'Fungi have chitin walls; animals have none.')],
  mc2=[('Which comparison of prokaryotic and eukaryotic cells is correct?', 'Prokaryotes have naked circular DNA; eukaryotes have linear DNA associated with histones in a nucleus.', ['Prokaryotes have 80S ribosomes; eukaryotes have 70S.', 'Both have mitochondria.', 'Prokaryotes are usually larger than eukaryotes.'], 'Key differences: nucleus, DNA form, ribosome size, organelles.'),
       ('Why is compartmentalisation an advantage to eukaryotic cells?', 'Enzymes and substrates can be concentrated and incompatible reactions kept separate.', ['It allows cells to be smaller.', 'It removes the need for ribosomes.', 'It allows DNA to be circular.'], 'E.g. hydrolytic enzymes in lysosomes are kept away from the cytoplasm.'),
       ('In an electron micrograph a cell shows a cell wall, ribosomes and a nucleoid, but no membrane-bound organelles. What is it?', 'a prokaryote', ['a plant cell', 'a fungal cell', 'an animal cell'], 'No nucleus or organelles = prokaryote.')],
  mc3=[('A micrograph shows a cell with chloroplasts, a cell wall and a large vacuole, but it also has flagella with a 9 + 2 arrangement. What is the best identification?', 'a eukaryotic photosynthetic protist such as Chlamydomonas', ['a cyanobacterium', 'a plant root cell', 'an animal sperm cell'], 'Chloroplasts and 9 + 2 flagella indicate a eukaryotic alga.'),
       ('Cells from the rough ER of pancreatic acinar cells are very abundant. What does this suggest about their function?', 'They synthesise large amounts of protein for secretion.', ['They store lipids.', 'They carry out photosynthesis.', 'They break down glucose anaerobically.'], 'Digestive enzymes are made on ribosomes of rough ER and secreted.')],
  why=[('Explain how the structure of a prokaryotic cell allows it to carry out all the functions of life.', 'Plasma membrane controls exchange; cytoplasm contains enzymes for metabolism; 70S ribosomes synthesise proteins; naked circular DNA (and plasmids) carry genes for inheritance and control; cell wall protects against bursting; some have flagella for movement and pili for attachment or DNA transfer.'),
       ('Explain why eukaryotic cells need membrane-bound organelles whereas prokaryotic cells can function without them.', 'Eukaryotic cells are much larger, with a smaller SA:V ratio; compartmentalisation allows concentrated enzymes and separate environments (e.g. low pH in lysosomes); prokaryotes are small, so diffusion distances are short and reactions can occur in the cytoplasm or on the membrane.'),
       ('Explain how electron micrographs can be used to identify the type of cell.', 'Presence or absence of a nucleus and membrane-bound organelles distinguishes eukaryotes from prokaryotes; cell wall, chloroplasts and large vacuole indicate plant; chitin wall and no chloroplasts fungus; abundant particular organelles indicate function, e.g. many mitochondria in muscle.')],
  contrast=[('prokaryotic cells', 'eukaryotic cells', 'Prokaryotic cells lack a nucleus and membrane-bound organelles, have naked circular DNA, 70S ribosomes and are usually 1–10 µm; eukaryotic cells have a nucleus containing linear DNA with histones, membrane-bound organelles, 80S ribosomes and are usually 10–100 µm.'),
            ('plant cells', 'animal cells', 'Plant cells have a cellulose cell wall, chloroplasts and a large permanent vacuole and store starch; animal cells lack walls and chloroplasts, have small temporary vacuoles, centrioles and store glycogen.'),
            ('fungal cells', 'plant cells', 'Fungal cells have walls of chitin, no chloroplasts and are heterotrophic, sometimes forming multinucleate hyphae; plant cells have cellulose walls, chloroplasts and are autotrophic.')],
  misc=[('Prokaryotic cells have no ribosomes because they have no organelles.', 'Prokaryotes do have ribosomes (70S); ribosomes are not membrane-bound, so they are present in all cells.'),
        ('Bacterial cell walls are made of cellulose like plant cell walls.', 'Bacterial walls are made of peptidoglycan (murein); cellulose walls are found in plants.'),
        ('All plant cells contain chloroplasts.', 'Only photosynthetic plant cells (e.g. mesophyll) contain chloroplasts; root cells do not.')],
  cases=[('the bacterium Escherichia coli in the human gut', 'E. coli is a rod about 2 µm long with a peptidoglycan wall, flagella, pili, a nucleoid and plasmids.', 'prokaryotic cell structure', 'It has all the functions of life without membrane-bound organelles: metabolism in the cytoplasm, protein synthesis on 70S ribosomes, DNA as a naked loop.'),
         ('pancreatic acinar cells that secrete digestive enzymes', 'Electron micrographs show extensive rough ER, many Golgi stacks and secretory vesicles.', 'the link between ultrastructure and function', 'Abundant rough ER and Golgi reflect large-scale synthesis and processing of proteins for secretion.')],
  apply=[('Draw and annotate a typical prokaryotic cell such as E. coli. List the structures that should be shown and annotate the function of each.', 'Cell wall (protection/prevents bursting); plasma membrane (controls entry/exit); cytoplasm (metabolism); nucleoid with circular DNA (genetic information); 70S ribosomes (protein synthesis); plasmid (extra genes); pili (attachment/conjugation); flagellum (movement).', 4),
         ('An electron micrograph of a cell shows a nucleus, mitochondria and a large vacuole surrounded by a thick wall, but no chloroplasts. Suggest two possible cell types and how you would distinguish them.', 'A plant root cell or a fungal cell; test the cell wall composition – cellulose (plant) or chitin (fungus); presence of starch grains or plastids suggests plant; hyphal arrangement suggests fungus.', 3)],
  evaluate=[('The distinction between prokaryotes and eukaryotes is the most fundamental division of living things.', ['the presence of a nucleus and compartmentalisation affects all aspects of cell biology', 'it is easily observed in electron micrographs'], ['molecular evidence shows archaea are as different from bacteria as from eukaryotes, giving three domains', 'some features (e.g. 70S ribosomes in mitochondria) blur the boundary'], 'The prokaryote–eukaryote distinction is a fundamental structural one, but molecular phylogeny shows the three-domain division better reflects evolutionary relationships.')],
  extended=[('Compare and contrast the structure of prokaryotic cells with that of plant and animal cells.', 'Similarities: plasma membrane, cytoplasm, ribosomes, DNA. Differences: nucleus absent in prokaryotes; naked circular DNA vs linear with histones; 70S vs 80S; no membrane-bound organelles; peptidoglycan vs cellulose wall vs none; size 1–10 µm vs 10–100 µm; plants have chloroplasts and large vacuole, animals have centrioles; plasmids in prokaryotes.', 8)],
  )

S('ch03-st4',
  terms=[('endosymbiotic theory', 'the theory that mitochondria and chloroplasts evolved from free-living prokaryotes that were engulfed by a host cell and survived inside it'),
         ('syncytium', 'a multinucleate cell or mass of cytoplasm formed by fusion of cells or by nuclear division without cell division, e.g. a striated muscle fibre'),
         ('aseptate hypha', 'a fungal hypha without cross-walls, so many nuclei share a continuous cytoplasm'),
         ('phloem sieve tube element', 'a living plant cell that lacks a nucleus and most organelles and is supported by a companion cell'),
         ('erythrocyte', 'a red blood cell, which in mammals lacks a nucleus and mitochondria when mature')],
  facts=[('Which atypical cell type contains many nuclei per cell?', 'striated muscle fibre', ['mammalian red blood cell', 'phloem sieve tube element', 'bacterium'], 'Muscle fibres form by fusion of myoblasts.'),
         ('Which type of cell loses its nucleus during development?', 'mammalian red blood cell', ['skeletal muscle fibre', 'aseptate fungal hypha', 'nerve cell'], 'Loss of the nucleus leaves more room for haemoglobin.'),
         ('Which evidence supports the endosymbiotic origin of mitochondria?', 'they have their own circular DNA and 70S ribosomes', ['they are found only in plants', 'they contain cellulose walls', 'they are made by the Golgi apparatus'], 'These are prokaryote-like features.'),
         ('How many membranes surround a mitochondrion or chloroplast?', 'two (a double membrane)', ['one', 'three', 'none'], 'The outer membrane is thought to derive from the host’s engulfing vesicle.')],
  mc2=[('Why does a mammalian red blood cell have no nucleus?', 'It gives more space for haemoglobin and a biconcave shape for gas exchange.', ['It allows the cell to divide faster.', 'It allows the cell to synthesise more proteins.', 'It allows aerobic respiration.'], 'The trade-off is a short lifespan of about 120 days.'),
       ('Mitochondria divide by a process similar to binary fission. How does this support the endosymbiotic theory?', 'Prokaryotes divide by binary fission, so mitochondria retain a prokaryotic mode of reproduction.', ['Eukaryotic cells divide by binary fission.', 'It shows mitochondria contain chlorophyll.', 'It shows mitochondria are made by the nucleus.'], 'New mitochondria arise only from existing ones.'),
       ('A phloem sieve tube element is described as atypical because it', 'lacks a nucleus but is alive and depends on a companion cell', ['has several nuclei', 'contains chloroplasts', 'is dead at maturity like xylem'], 'Sieve tube elements are living but enucleate.')],
  mc3=[('Antibiotics such as chloramphenicol that inhibit 70S ribosomes can reduce protein synthesis in human mitochondria. What does this suggest?', 'Mitochondrial ribosomes resemble prokaryotic ribosomes, supporting endosymbiosis.', ['Mitochondria contain 80S ribosomes.', 'Human cytoplasmic ribosomes are 70S.', 'Antibiotics target the nucleus.'], 'Mitochondria share features with bacteria.'),
       ('Sequencing shows the genes in chloroplast DNA most closely resemble those of cyanobacteria. What conclusion is supported?', 'Chloroplasts descended from an engulfed cyanobacterium.', ['Cyanobacteria descended from chloroplasts.', 'Chloroplasts formed from the nucleus.', 'Chloroplasts and cyanobacteria evolved independently.'], 'Molecular phylogeny places plastids within cyanobacteria.')],
  why=[('Explain the evidence that mitochondria and chloroplasts evolved by endosymbiosis.', 'They have a double membrane (inner from the prokaryote, outer from the host vesicle); their own naked circular DNA; 70S ribosomes; divide by binary fission; similar size to bacteria; their DNA sequences resemble those of α-proteobacteria and cyanobacteria respectively; antibiotics that affect bacteria affect them.'),
       ('Explain why striated muscle fibres are considered to challenge the cell theory.', 'They are very long (up to several cm) and contain many nuclei within one continuous plasma membrane, formed by fusion of many cells, so they do not fit the idea of a cell as a small unit with a single nucleus.'),
       ('Explain how the structure of aseptate fungal hyphae differs from that of typical cells.', 'Aseptate hyphae lack cross-walls, so cytoplasm and many nuclei are continuous along a long tube, rather than being divided into separate cells each with one nucleus.')],
  contrast=[('mammalian red blood cells', 'phloem sieve tube elements', 'Both lack a nucleus when mature; red blood cells are free-floating, packed with haemoglobin and lack mitochondria, whereas sieve tube elements are joined end to end through sieve plates and are supported by companion cells that carry out metabolism for them.')],
  misc=[('Mitochondria were made by the cell from its own membranes.', 'The endosymbiotic theory proposes they originated from free-living aerobic prokaryotes engulfed by an ancestral host cell.'),
        ('All living cells have exactly one nucleus.', 'Some cells have none (mature red blood cells, sieve tube elements) and some have many (striated muscle fibres, aseptate hyphae).')],
  cases=[('the work of Lynn Margulis in the 1960s', 'Margulis assembled evidence that mitochondria and chloroplasts originated as symbiotic bacteria, initially facing strong opposition.', 'the origin of eukaryotic cells by endosymbiosis', 'Her hypothesis was later strongly supported by DNA sequence data, showing how a paradigm shift occurs when evidence accumulates.'),
         ('Paulinella chromatophora, an amoeba with a recently acquired cyanobacterial endosymbiont', 'The amoeba contains photosynthetic “chromatophores” derived from a cyanobacterium about 100 million years ago.', 'endosymbiosis as an ongoing process', 'It shows a stage in which an engulfed prokaryote is becoming an organelle, as proposed for chloroplasts.')],
  evaluate=[('The endosymbiotic theory is now accepted as fact.', ['many independent lines of evidence (DNA, ribosomes, membranes, division) support it', 'phylogenetic analysis places mitochondria within α-proteobacteria'], ['the details of the host cell and sequence of events remain uncertain', 'scientific knowledge is always provisional'], 'Endosymbiosis is a well-supported theory accepted by biologists; calling it fact overstates certainty, but it is as strongly supported as any explanation in cell biology.')],
  extended=[('Outline the endosymbiotic theory and evaluate the evidence for it.', 'Host anaerobic cell engulfed aerobic prokaryote → mitochondrion, later photosynthetic prokaryote → chloroplast; not digested, mutualistic. Evidence: double membranes, circular DNA, 70S ribosomes, binary fission, size, sequence similarity, antibiotic sensitivity. Evaluation: strong convergence; but many genes transferred to nucleus; cannot observe directly; Paulinella shows process.', 8)],
  )

S('ch03-st5',
  terms=[('virus', 'a non-cellular infectious particle made of nucleic acid enclosed in a protein capsid, which can only replicate inside a host cell'),
         ('capsid', 'the protein coat of a virus, made of repeating subunits'),
         ('lytic cycle', 'a viral replication cycle in which the virus takes over the host cell, makes many new virions and bursts (lyses) the cell to release them'),
         ('lysogenic cycle', 'a viral cycle in which viral DNA is integrated into the host chromosome as a prophage and copied with it, without immediate production of virions'),
         ('prophage', 'the DNA of a bacteriophage integrated into the bacterial chromosome during the lysogenic cycle'),
         ('envelope', 'a membrane derived from the host cell surrounding the capsid of some viruses, such as influenza and HIV')],
  facts=[('Which structure is present in all viruses?', 'a protein capsid', ['a lipid envelope', 'ribosomes', 'a cell wall'], 'All viruses have nucleic acid in a capsid; only some are enveloped.'),
         ('Which type of genetic material does HIV have?', 'single-stranded RNA', ['double-stranded DNA', 'single-stranded DNA', 'protein'], 'HIV is a retrovirus using reverse transcriptase.'),
         ('Which bacteriophage is the classic example of the lysogenic cycle?', 'lambda (λ) phage', ['T4 phage', 'influenza virus', 'HIV'], 'λ integrates into the E. coli chromosome.'),
         ('Why are viruses not considered to be living cells?', 'they have no metabolism of their own and can only reproduce inside host cells', ['they contain DNA', 'they contain protein', 'they evolve'], 'Viruses lack ribosomes and enzymes for metabolism.')],
  mc2=[('Which feature is shared by viruses and cells?', 'genetic material that can mutate and evolve', ['ribosomes', 'a plasma membrane', 'cytoplasm'], 'Viruses evolve rapidly through mutation.'),
       ('Why can the lysogenic cycle be advantageous to a phage?', 'The viral genome is copied each time the host divides without killing it.', ['It makes more virions immediately.', 'It destroys host DNA.', 'It allows the phage to photosynthesise.'], 'It spreads the virus vertically while host conditions are poor.'),
       ('What is the main reason viruses evolve rapidly?', 'They have short generation times, huge population sizes and high mutation rates.', ['They have no genetic material.', 'They reproduce sexually.', 'They have large genomes.'], 'RNA viruses especially lack proofreading.')],
  mc3=[('A phage infects bacteria in a culture, but for several days no cells burst. When UV light is applied, many cells lyse. What is the best explanation?', 'The phage was in the lysogenic cycle and UV triggered a switch to the lytic cycle.', ['UV killed the bacteria directly.', 'The phage was destroyed by UV.', 'The bacteria became resistant.'], 'Stress such as UV can induce prophages.'),
       ('Viruses with RNA genomes and with DNA genomes, enveloped and non-enveloped, all infect cells. What does this diversity suggest about the origin of viruses?', 'Viruses may have arisen more than once (polyphyletic origin).', ['All viruses share one common ancestor.', 'Viruses evolved before cells.', 'Viruses are degenerate bacteria only.'], 'Structural diversity suggests multiple origins.')],
  why=[('Explain the stages of the lytic cycle of a bacteriophage such as T4.', 'Attachment to receptors on host cell; injection of viral DNA; host DNA degraded and host machinery used to replicate viral DNA and make capsid proteins; assembly of new virions; lysis of the cell by viral enzymes releases many phages.'),
       ('Explain how the lysogenic cycle differs from the lytic cycle.', 'In the lysogenic cycle viral DNA integrates into the host chromosome as a prophage and is replicated with host DNA each time the cell divides; no virions are produced and the host survives until a trigger induces entry into the lytic cycle.'),
       ('Explain why antibiotics are ineffective against viral infections.', 'Antibiotics target structures and processes of bacteria (e.g. peptidoglycan walls, 70S ribosomes); viruses lack these and use host cell machinery, so there is nothing for the antibiotic to block.')],
  contrast=[('the lytic cycle', 'the lysogenic cycle', 'In the lytic cycle the virus replicates immediately, producing many virions and killing the cell by lysis; in the lysogenic cycle the viral genome integrates as a prophage, is copied with the host chromosome and the cell is not killed until the cycle switches.'),
            ('enveloped viruses', 'non-enveloped viruses', 'Enveloped viruses (e.g. HIV, influenza) have an outer membrane derived from the host plasma membrane with viral glycoproteins; non-enveloped viruses (e.g. T4) have only a protein capsid.')],
  misc=[('Viruses are tiny bacteria.', 'Viruses are non-cellular: they lack cytoplasm, ribosomes and metabolism and can only reproduce inside host cells.'),
        ('A virus in the lysogenic cycle is inactive and harmless permanently.', 'A prophage can be induced to enter the lytic cycle, e.g. by UV or stress, killing the host and releasing virions.')],
  cases=[('the T4 bacteriophage infecting Escherichia coli', 'T4 attaches using tail fibres, injects DNA, and about 25 minutes later the cell bursts releasing 100–200 new phages.', 'the lytic cycle', 'It shows how a virus redirects host machinery to make new virions and kills the host cell by lysis.'),
         ('lambda (λ) phage in E. coli', 'λ DNA integrates at a specific site in the bacterial chromosome and can remain as a prophage for many generations.', 'the lysogenic cycle', 'The phage genome is passed on to daughter cells during binary fission until induction triggers lysis.')],
  evaluate=[('Viruses should be classified as living organisms.', ['they contain genetic material, evolve by natural selection and reproduce (inside hosts)', 'giant viruses such as mimivirus have genes for some translation-related proteins'], ['they have no metabolism, no cell structure and cannot reproduce independently', 'outside hosts they are inert particles that can even be crystallised'], 'Viruses lie at the boundary of life; by the functions of life (metabolism, homeostasis, growth) they are not living, though they share evolution with living things.')],
  extended=[('Describe the structure of viruses and compare the lytic and lysogenic cycles of bacteriophages.', 'Structure: nucleic acid (DNA or RNA), capsid of protein subunits, some enveloped, no cytoplasm or ribosomes, small (20–300 nm). Lytic: attach, inject, replicate, synthesise, assemble, lyse. Lysogenic: integrate prophage, replicated with host, induced to lytic. Comparison: both need host, attachment and injection similar; lytic kills quickly, lysogenic delays; λ vs T4.', 8)],
  )


@R.add('ch03-st5', 'C3', (1, 5), 'numerical')
def plaque_assay(rng, slot):
    dil = pick(rng, [4, 5, 6, 7, 8])
    vol = pick(rng, [0.1, 0.2, 0.5])
    plaques = rng.randint(25, 280)
    pfu = plaques / (vol * 10 ** -dil)
    phage = pick(rng, ['T4 phage', 'lambda phage', 'a phage isolated from sewage', 'a phage used in phage therapy trials', 'T7 phage'])
    stem = (f'A suspension of {phage} was diluted by a factor of 10{sup(dil)}. {vol} cm³ of the diluted suspension was spread with E. coli on an agar plate and {plaques} plaques formed. '
            f'Calculate the concentration of infective phage particles in the original suspension, in plaque-forming units (pfu) per cm³.')
    ans = f'{sf(pfu)} pfu cm⁻³'
    key = f'pfu cm⁻³ = plaques ÷ (volume × dilution) = {plaques} ÷ ({vol} × 10⁻{dil}) (M1) = {sf(pfu)} (A1).'
    if slot.d >= 4:
        burst = rng.randint(80, 220)
        stem += f' Each infected cell releases about {burst} phages per lytic cycle. Explain what a plaque is and estimate how many phages are released from 1000 infected cells.'
        ans += f'; a plaque is a clear zone where bacteria have been lysed; ≈ {burst * 1000:,} phages'.replace(',', ' ')
        key += f' Plaque = area of lysed bacteria from one original phage (R1); 1000 × {burst} = {burst * 1000} (A1).'
        return num(stem, ans, key, 4)
    return num(stem, ans, key, 2)




# =============================================================================================
# ch04 A3.1 Diversity of organisms and A3.2 Classification and cladistics
# =============================================================================================
S('ch04-st1',
  terms=[('species', 'a group of organisms with shared traits that can interbreed to produce fertile offspring (biological species concept)'),
         ('binomial nomenclature', 'the system of naming each species with two Latin words, the genus name (capital) followed by the species name (lower case), printed in italics'),
         ('morphological species concept', 'the definition of species based on shared observable physical characteristics'),
         ('variation', 'the differences in characteristics between individuals of the same species'),
         ('ring species', 'a chain of neighbouring populations that can interbreed, whose end populations cannot, making species boundaries unclear'),
         ('hybrid', 'the offspring of a cross between two different species, often infertile')],
  facts=[('In the binomial name of the lion, Panthera leo, what does each word represent?', 'Panthera is the genus and leo is the specific name.', ['Panthera is the species and leo is the genus.', 'Panthera is the family and leo is the genus.', 'Both words together name the genus.'], 'Genus first (capitalised), specific name second (lower case), both italicised or underlined when handwritten.'),
         ('Who devised the system of binomial nomenclature in the 18th century?', 'Carl Linnaeus', ['Charles Darwin', 'Gregor Mendel', 'Carl Woese'], 'Linnaeus’s Systema Naturae (1758) is the starting point for animal names.'),
         ('Why is a mule not considered a species?', 'mules are almost always infertile', ['mules cannot survive in the wild', 'mules look different from horses', 'mules have no chromosomes'], 'Horse × donkey hybrids cannot usually produce offspring.'),
         ('According to the biological species concept, what defines members of the same species?', 'they can interbreed to produce fertile offspring', ['they look identical', 'they live in the same habitat', 'they have the same number of genes'], 'Reproductive compatibility is the key criterion.')],
  mc2=[('Why does the biological species concept not apply to bacteria?', 'Bacteria reproduce asexually, so interbreeding cannot be tested.', ['Bacteria have no DNA.', 'All bacteria are the same species.', 'Bacteria are too small to be seen.'], 'The concept relies on sexual reproduction.'),
       ('Which situation creates difficulty for the morphological species concept?', 'males and females of a species that look very different (sexual dimorphism)', ['individuals that look similar and interbreed', 'a species with a binomial name', 'populations living in the same area'], 'E.g. birds of paradise; also cryptic species that look alike but do not interbreed.'),
       ('Herring gulls and lesser black-backed gulls coexist in Britain without interbreeding, yet are linked by interbreeding populations around the Arctic. This example illustrates', 'the difficulty of defining species boundaries in ring species', ['convergent evolution', 'binomial nomenclature', 'genetic drift'], 'Gradual change around the ring blurs species limits.')],
  mc3=[('Two populations of frogs look identical but their mating calls differ and they never interbreed in the wild. How should they be classified?', 'as separate species under the biological species concept', ['as the same species because they look identical', 'as hybrids', 'as one species with two varieties'], 'They are reproductively isolated cryptic species.'),
       ('Lions and tigers can produce “ligers” in captivity, but they never interbreed in the wild. Which statement is best supported?', 'They are separate species, though the boundary is not absolute.', ['They are one species.', 'Ligers prove they belong to one genus only.', 'They are ring species.'], 'Potential interbreeding in captivity shows limitations of the biological species concept.')],
  why=[('Explain why binomial nomenclature is important in biology.', 'It gives every species one unique, internationally agreed name, avoiding confusion caused by different common names in different languages or regions; the genus name also indicates relationships with similar species.'),
       ('Explain the difficulties of applying the biological species concept.', 'It cannot be applied to asexual organisms or fossils; it is hard to test interbreeding in geographically separated populations; hybrids are sometimes fertile; populations may be partly isolated (ring species), so boundaries are fuzzy.'),
       ('Explain the difference between continuous and discrete variation within a species, with an example of each.', 'Continuous variation shows a range of values with no distinct categories (e.g. human height), usually polygenic and environmental; discrete variation falls into distinct categories (e.g. ABO blood group), usually controlled by one or few genes.')],
  contrast=[('the biological species concept', 'the morphological species concept', 'The biological concept defines species by the ability to interbreed and produce fertile offspring; the morphological concept defines them by shared physical characteristics, which can be applied to fossils and asexual organisms but may mislead with dimorphism or cryptic species.'),
            ('chromosome number differences between species', 'variation within a species', 'Different species often have different chromosome numbers (e.g. chimpanzee 48, human 46), contributing to reproductive isolation; within a species chromosome number is normally constant and variation is due to differences in alleles.')],
  misc=[('Organisms that look alike must belong to the same species.', 'Cryptic species look alike but do not interbreed; species are defined by reproductive isolation in the biological concept, not only appearance.'),
        ('Scientific names are written with both words capitalised, e.g. Homo Sapiens.', 'Only the genus is capitalised: Homo sapiens, in italics.')],
  cases=[('the African forest elephant (Loxodonta cyclotis) and the African savanna elephant (Loxodonta africana)', 'Once treated as one species, DNA evidence showed little gene flow, and they were split into two species in 2021 by the IUCN.', 'the difficulty of defining species', 'The split illustrates how species definitions change with new evidence such as genetic data.'),
         ('the ring of Ensatina salamanders around the Central Valley of California', 'Neighbouring populations interbreed, but the two end populations in the south coexist without interbreeding.', 'the limitations of the biological species concept', 'Speciation is gradual, so there may be no clear point at which populations become separate species.')],
  evaluate=[('The biological species concept is the most useful way to define a species.', ['it is based on the evolutionary process of reproductive isolation that separates gene pools', 'it explains why species remain distinct when they live together'], ['it cannot be used for asexual organisms, fossils or allopatric populations', 'hybridisation with fertile offspring occurs in many plants and some animals'], 'It is the most useful concept for sexually reproducing living organisms, but biologists need several complementary concepts (morphological, phylogenetic) for other cases.')],
  extended=[('Outline the different species concepts and discuss the difficulties of deciding whether two populations are separate species.', 'Morphological: physical similarity; biological: interbreeding and fertile offspring; phylogenetic/genetic: DNA lineage. Difficulties: asexual organisms, fossils, geographic separation, hybrids (fertile or infertile), ring species, cryptic species, sexual dimorphism, gradual speciation – populations diverge continuously so no sharp line.', 8)],
  )

GENOMES = [('human (Homo sapiens)', 46, 3.1, 20000), ('chimpanzee (Pan troglodytes)', 48, 3.0, 20000), ('dog (Canis familiaris)', 78, 2.4, 19000),
           ('fruit fly (Drosophila melanogaster)', 8, 0.14, 14000), ('thale cress (Arabidopsis thaliana)', 10, 0.135, 27000),
           ('rice (Oryza sativa)', 24, 0.43, 38000), ('bread wheat (Triticum aestivum)', 42, 16.0, 107000), ('baker’s yeast (Saccharomyces cerevisiae)', 32, 0.012, 6000),
           ('Paris japonica', 40, 149.0, None), ('horse (Equus caballus)', 64, 2.5, 20000), ('donkey (Equus asinus)', 62, 2.4, 20000),
           ('nematode (Caenorhabditis elegans)', 12, 0.1, 20000)]

S('ch04-st2',
  terms=[('karyotype', 'the number and appearance of the chromosomes in a cell, arranged in homologous pairs in order of size and centromere position'),
         ('karyogram', 'an image of the chromosomes of a cell arranged in homologous pairs in decreasing order of size'),
         ('genome', 'all the genetic information (DNA) of an organism or species'),
         ('whole-genome sequencing', 'determining the complete base sequence of all the DNA of an organism'),
         ('diploid', 'a cell or organism with two sets of chromosomes (2n), one from each parent'),
         ('haploid', 'a cell with one set of chromosomes (n), as in gametes')],
  facts=[('What is the diploid chromosome number of humans?', '46', ['23', '48', '44'], 'Humans have 23 pairs.'),
         ('Which species has a diploid chromosome number of 48?', 'chimpanzee', ['human', 'fruit fly', 'domestic dog'], 'Human chromosome 2 formed from the fusion of two ancestral chromosomes.'),
         ('How large is the human genome?', 'about 3.1 billion base pairs', ['about 3.1 million base pairs', 'about 31 billion base pairs', 'about 20 000 base pairs'], 'It contains roughly 20 000 protein-coding genes.'),
         ('Which plant has one of the largest known genomes (about 149 billion base pairs)?', 'Paris japonica', ['Arabidopsis thaliana', 'rice', 'maize'], 'Genome size does not correlate with complexity.'),
         ('A karyogram is used to deduce which of the following?', 'the sex of an individual and the presence of chromosome abnormalities such as trisomy', ['the base sequence of every gene', 'the blood group of a person', 'the rate of mitosis'], 'XX/XY and an extra chromosome 21 are visible.')],
  mc2=[('Human chromosome 2 has two inactive centromere-like regions and telomere sequences near its middle. What does this suggest?', 'It formed by fusion of two ancestral chromosomes that remain separate in other great apes.', ['It is a duplicated chromosome.', 'Humans have lost a chromosome.', 'Chimpanzees have extra DNA.'], 'This explains 46 vs 48 chromosomes.'),
       ('Why is genome size a poor indicator of an organism’s complexity?', 'Genomes differ mainly in the amount of non-coding and repetitive DNA, not the number of genes.', ['All genomes are the same size.', 'Larger organisms always have more genes.', 'Genome size depends only on chromosome number.'], 'The “C-value paradox”.'),
       ('Which explains the value of whole-genome sequencing for comparing species?', 'Base sequences can be compared to measure similarity and estimate relationships.', ['It shows chromosome numbers only.', 'It gives the shape of proteins directly.', 'It reveals morphological characteristics.'], 'Sequence differences accumulate with time since divergence.')],
  mc3=[('A karyogram shows 47 chromosomes, with three copies of chromosome 21 and two X chromosomes. What is the correct interpretation?', 'a female with Down syndrome (trisomy 21)', ['a male with Down syndrome', 'a female with Turner syndrome', 'a normal female'], 'Two X = female; extra 21 = trisomy 21.'),
       ('A cell from a horse (2n = 64) and one from a donkey (2n = 62) produce gametes that fuse. What is the chromosome number of the mule?', '63', ['126', '64', '31'], '32 + 31 = 63, unpaired chromosomes cause infertility.')],
  why=[('Explain how a karyogram is prepared and what it can show.', 'Cells (e.g. lymphocytes or fetal cells) are stimulated to divide and stopped at metaphase; chromosomes are stained and photographed; homologues are paired by size, banding and centromere position; shows chromosome number, sex chromosomes and abnormalities such as trisomy.'),
       ('Explain why the number of chromosomes is a characteristic feature of a species.', 'Members of a species have the same chromosome number so homologues can pair in meiosis; differences in number disrupt pairing, making hybrids infertile and contributing to reproductive isolation.'),
       ('Explain the uses of whole-genome sequencing.', 'Comparing genomes reveals evolutionary relationships and common ancestry; identifies genes and mutations linked to disease; allows personalised medicine; helps classification and conservation genetics; has become faster and cheaper since the Human Genome Project.')],
  contrast=[('a karyotype', 'a genome', 'A karyotype describes the number and visible structure of chromosomes; a genome is the entire base sequence of the organism’s DNA.')],
  misc=[('Organisms with more chromosomes are more complex.', 'Chromosome number does not reflect complexity: dogs have 78, humans 46 and some ferns over 1000.'),
        ('The largest genomes belong to the most complex animals.', 'Some plants (e.g. Paris japonica, 149 Gb) and amoebae have far larger genomes than humans; most of the difference is non-coding DNA.')],
  cases=[('the Human Genome Project (1990–2003)', 'An international project sequenced about 3 billion base pairs and estimated about 20 000 protein-coding genes.', 'the use of whole-genome sequencing', 'It provided a reference genome for comparing individuals and species, and the cost of sequencing has since fallen from billions of dollars to a few hundred.'),
         ('the comparison of human and chimpanzee genomes', 'The genomes are about 98–99 % identical in aligned sequences; humans have 46 chromosomes and chimpanzees 48.', 'karyotype and genome comparisons between species', 'High sequence similarity shows close relationship; the fusion of two ape chromosomes into human chromosome 2 explains the difference in number.')],
  evaluate=[('Whole-genome sequencing of every newborn baby should become routine.', ['it could detect genetic diseases early and guide treatment', 'costs have fallen dramatically'], ['it raises issues of privacy, consent and possible discrimination', 'most variants are of uncertain significance and may cause anxiety'], 'Targeted screening offers clear benefits now; routine whole-genome sequencing needs strong safeguards and better interpretation of variants before it is justified.')],
  extended=[('Compare the genomes and karyotypes of different species and discuss what such comparisons reveal.', 'Chromosome numbers vary (human 46, chimp 48, dog 78); fusion of chromosome 2; genome size varies widely (yeast 12 Mb, human 3.1 Gb, Paris japonica 149 Gb) and does not correlate with complexity or gene number; sequence comparison reveals relationships and common ancestry; human–chimp 98–99 % similarity; uses in classification.', 7)],
  )


@R.add('ch04-st2', 'C3', (1, 4), 'numerical')
def gametes_hybrid(rng, slot):
    a, b = rng.sample([g for g in GENOMES if g[1] % 2 == 0], 2)
    f = rng.randrange(3)
    if f == 0:
        return num(f'The diploid number of {a[0]} is {a[1]}. State the number of chromosomes in (a) a gamete and (b) a skin cell of this organism.',
                   f'(a) {a[1] // 2}; (b) {a[1]}', f'(a) haploid n = {a[1] // 2} (A1); (b) diploid 2n = {a[1]} (A1).', 2)
    if f == 1:
        h = rng.randint(4, 40)
        return num(f'A gamete of a newly described plant species contains {h} chromosomes. State the diploid number and the number of chromosome pairs visible in a karyogram of a leaf cell.',
                   f'2n = {2 * h}; {h} pairs', f'2n = 2 × {h} = {2 * h} (A1); {h} homologous pairs (A1).', 2)
    n1 = pick(rng, [24, 28, 32, 34, 36, 38, 40])
    n2 = n1 + pick(rng, [-4, -2, 2, 4, 6])
    ha = pick(rng, ['two species of wild grass', 'two closely related species of goat', 'two species of zebra', 'two species of Iris'])
    return num(f'Hybrids can be produced between {ha} with diploid numbers {n1} and {n2}. State the chromosome number of the hybrid and explain why it is likely to be infertile.',
               f'{n1 // 2 + n2 // 2}; chromosomes cannot all pair as homologues in meiosis, so gametes are unbalanced',
               f'{n1 // 2} + {n2 // 2} = {n1 // 2 + n2 // 2} (A1); chromosomes from different species are not homologous / odd or unmatched set cannot pair in meiosis I (R1); gametes have incomplete sets (R1).', 3)


def _genome_dq(rng, slot):
    rows = rng.sample([g for g in GENOMES if g[3]], 5)
    data = [(g[0], g[1], f'{g[2]:g}', f'{g[3]:,}'.replace(',', ' ')) for g in rows]
    dens = [(g[0], g[3] / (g[2] * 1000)) for g in rows]
    hi = max(dens, key=lambda x: x[1])
    lo = min(dens, key=lambda x: x[1])
    big = max(rows, key=lambda g: g[2])
    small = min(rows, key=lambda g: g[2])
    ratio = big[2] / small[2]
    intro = ('The table shows the diploid chromosome number, haploid genome size and approximate number of protein-coding genes for several eukaryotes.\n\n'
             + table(['Species', 'Diploid number', 'Genome size / billion base pairs', 'Protein-coding genes'], data))
    parts = [
        ('Identify the species with the largest genome.', big[0], f'{big[0]} (A1).', 1),
        (f'Calculate how many times larger the genome of {big[0]} is than that of {small[0]}.', f'{ratio:.0f} times' if ratio >= 10 else f'{ratio:.1f} times', f'{big[2]:g}/{small[2]:g} (M1) = {ratio:.3g} (A1).', 2),
        ('Calculate the number of genes per million base pairs for the species with the smallest genome.', f'{small[3] / (small[2] * 1000):.0f} genes per Mb', f'{small[3]} ÷ ({small[2]:g} × 1000 Mb) (M1) = {small[3] / (small[2] * 1000):.0f} (A1).', 2),
        ('Using the data, evaluate the claim that more complex organisms have larger genomes.', f'Not supported: genome size does not follow complexity – e.g. {big[0]} has the largest genome; gene number is also not proportional to genome size; most large genomes contain much non-coding/repetitive DNA.', 'Claim not supported (A1); specific comparison from data (A1); explanation – non-coding DNA / polyploidy (R1).', 3),
        ('State whether chromosome number is correlated with genome size in these data, with a reason.', 'No clear correlation: species with similar chromosome numbers have very different genome sizes.', 'No correlation (A1) with data-based reason (R1).', 2),
        ('Suggest one reason why bread wheat has a very large genome and many genes.', 'It is hexaploid (an allopolyploid formed from three ancestral species), so it carries three complete genomes.', 'Polyploidy / three ancestral genomes (A1).', 1),
        ('Explain why genome size is measured in base pairs.', 'DNA is double-stranded, and each position on the molecule consists of a complementary base pair, so the length is counted in base pairs.', 'Double-stranded (A1); complementary pairs (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch04-st2', _genome_dq)

S('ch04-st3',
  terms=[('dichotomous key', 'an identification tool made of a series of paired, mutually exclusive descriptions, each leading to another pair or to the name of an organism'),
         ('environmental DNA (eDNA)', 'DNA shed by organisms into their surroundings (water, soil, air) that can be collected and sequenced to identify which species are present'),
         ('DNA barcoding', 'identification of species using a short, standardised gene sequence (e.g. the COI mitochondrial gene in animals) compared with a reference database'),
         ('metabarcoding', 'simultaneous identification of many species in a mixed sample by sequencing barcode regions of all the DNA it contains')],
  facts=[('Which feature makes a good couplet in a dichotomous key?', 'two mutually exclusive, observable characteristics', ['the colour of the organism only', 'characteristics that change with season', 'the size of the organism in the photograph'], 'Couplets must be unambiguous and observable.'),
         ('What is an advantage of eDNA surveys over traditional surveys?', 'species can be detected without seeing or capturing them', ['they give the exact number of individuals', 'they do not need laboratory analysis', 'they work without reference databases'], 'Rare or elusive species leave DNA traces.'),
         ('Which gene region is most commonly used for DNA barcoding of animals?', 'cytochrome c oxidase I (COI) in mitochondrial DNA', ['the insulin gene', 'ribosomal RNA of chloroplasts', 'the haemoglobin gene'], 'COI varies between species but little within them.'),
         ('How many couplets are needed in a dichotomous key to identify 8 species?', '7', ['8', '4', '16'], 'A key for n organisms needs n − 1 couplets.')],
  mc2=[('Why should a dichotomous key avoid using colour as a feature where possible?', 'Colour may vary with age, sex or season and is subjective.', ['Colour cannot be seen.', 'Colour is never inherited.', 'Keys can only use numbers.'], 'Stable, objective features are better.'),
       ('An eDNA sample from a lake contains DNA of the great crested newt, but no newts were seen. What is the most reasonable conclusion?', 'Newts are probably present in or near the lake.', ['Newts are extinct in the lake.', 'The sample must be contaminated.', 'There are exactly as many newts as DNA fragments.'], 'eDNA indicates presence but not abundance precisely; contamination is possible.'),
       ('Why can eDNA give false negatives?', 'DNA degrades in the environment, especially with warmth and UV.', ['eDNA lasts for centuries.', 'eDNA is always contaminated.', 'Reference databases include every species.'], 'Degradation and dilution reduce detection.')],
  mc3=[('A key starts: 1a “Legs present → 2”; 1b “Legs absent → Earthworm”; 2a “Six legs → 3”; 2b “Eight legs → Spider”. An animal has six legs. Where does the user go next?', 'to couplet 3', ['to Spider', 'to Earthworm', 'back to couplet 1'], 'Six legs → 2a → 3.'),
       ('Researchers sequence water from a river in Borneo and find DNA matching an otter species never recorded there. What should they do before publishing?', 'Confirm with repeat samples and controls to rule out contamination, and ideally a camera trap.', ['Publish immediately as proof.', 'Discard the result as impossible.', 'Assume the database is wrong.'], 'Verification is essential in eDNA work.')],
  why=[('Explain how a dichotomous key is used to identify an organism.', 'Starting at the first couplet, the user chooses which of two contrasting descriptions fits the specimen; each choice leads to another numbered couplet or a name; this is repeated until the organism is identified.'),
       ('Explain how environmental DNA can be used to identify species present in a habitat.', 'Water, soil or air samples are collected and filtered; DNA is extracted, specific barcode regions are amplified by PCR and sequenced; the sequences are compared with a reference database to identify the species whose DNA is present.'),
       ('Explain the advantages and limitations of eDNA compared with traditional surveys.', 'Advantages: detects rare, elusive, cryptic species; non-invasive; many species from one sample; less expertise in morphology needed. Limitations: little information on abundance, age or sex; DNA degrades or travels downstream; contamination; incomplete reference databases.')],
  contrast=[('identification using a dichotomous key', 'identification using DNA barcoding', 'Keys use observable morphological features and need an intact specimen and expertise; barcoding compares a short DNA sequence with a database and can identify fragments, eggs or eDNA, but needs laboratory work and a complete reference library.')],
  misc=[('An eDNA survey tells you exactly how many fish live in a lake.', 'eDNA mainly shows presence/absence; the amount of DNA is only a rough indicator of abundance because it depends on shedding rates, degradation and water flow.'),
        ('A dichotomous key can use as many choices as needed at each step.', 'A dichotomous key always offers exactly two contrasting choices at each step.')],
  cases=[('eDNA monitoring of great crested newts (Triturus cristatus) in ponds in England', 'Pond water samples are tested for newt DNA as an accepted alternative to night-time torch and netting surveys before development.', 'the use of eDNA in identifying species', 'Presence of the protected species is detected quickly and non-invasively from water samples.'),
         ('the use of eDNA to track invasive Asian carp in the Great Lakes', 'Carp DNA was detected beyond barriers, prompting further monitoring.', 'the benefits and limitations of eDNA', 'It gives early warning of invasions but positive results may come from boats or birds carrying DNA, not live fish.')],
  apply=[('Construct a dichotomous key to separate these four trees by their leaves: oak (simple, lobed), maple (simple, palmately lobed, opposite leaves), ash (compound, opposite leaflets), horse chestnut (compound, palmate). Describe the couplets.', '1a leaf simple → 2; 1b leaf compound → 3. 2a lobes arranged palmately (from one point) → maple; 2b lobes along the midrib → oak. 3a leaflets arranged palmately from one point → horse chestnut; 3b leaflets in pairs along a central stalk → ash.', 4),
         ('A dichotomous key is needed for 12 invertebrate species collected from leaf litter. State the number of couplets needed and suggest two features suitable for the first couplets.', '11 couplets; e.g. number of legs (6, 8, many/none); presence of segments; presence of a shell; wings present/absent.', 3)],
  evaluate=[('eDNA will soon make traditional field identification skills unnecessary.', ['eDNA can detect many species quickly and cheaply, including rare and cryptic ones', 'metabarcoding can survey whole communities from one sample'], ['eDNA gives little information on abundance, behaviour, condition or life stage', 'reference databases rely on specimens identified by trained taxonomists'], 'eDNA is a powerful complement, but field identification remains essential to validate results, build databases and study populations.')],
  extended=[('Describe how species can be identified using dichotomous keys and environmental DNA, and evaluate each method.', 'Key: paired contrasting features, n − 1 couplets, observable stable characters, specimen needed; strengths: cheap, in the field; limits: expertise, variation, life stages. eDNA: sample, filter, extract, PCR barcode, sequence, database; strengths: non-invasive, rare species, many species; limits: degradation, contamination, abundance unknown, database gaps.', 8)],
  )

S('ch04-st4',
  terms=[('taxonomy', 'the science of naming, describing and classifying organisms'),
         ('domain', 'the highest taxonomic rank; all life is classified into three domains: Archaea, Bacteria and Eukarya'),
         ('taxon', 'a group of organisms at any level of the classification hierarchy, such as a genus or family'),
         ('Archaea', 'a domain of prokaryotes distinct from bacteria in rRNA sequence, membrane lipids and cell wall composition, many of which live in extreme environments'),
         ('natural classification', 'a classification in which groups contain all the descendants of a common ancestor, reflecting evolutionary relationships')],
  facts=[('What is the correct order of taxa from highest to lowest?', 'domain, kingdom, phylum, class, order, family, genus, species', ['kingdom, domain, class, phylum, order, family, genus, species', 'domain, phylum, kingdom, class, family, order, genus, species', 'species, genus, family, order, class, phylum, kingdom, domain'], 'Mnemonic: Do Keep Ponds Clean Or Frogs Get Sick.'),
         ('Which molecule did Carl Woese compare to propose the three-domain system?', 'ribosomal RNA', ['haemoglobin', 'cytochrome c', 'chlorophyll'], 'Woese sequenced 16S rRNA in the 1970s.'),
         ('Which domain includes fungi, plants and animals?', 'Eukarya', ['Archaea', 'Bacteria', 'Protista'], 'All organisms with nucleated cells.'),
         ('Which feature distinguishes Archaea from Bacteria?', 'membrane lipids with ether linkages and no peptidoglycan in the cell wall', ['the presence of a nucleus', 'the presence of mitochondria', '80S cytoplasmic ribosomes'], 'Archaea are prokaryotes with unique biochemistry.')],
  mc2=[('Why was the five-kingdom system replaced by the three-domain system?', 'rRNA sequences showed that prokaryotes consist of two groups as different from each other as from eukaryotes.', ['Prokaryotes were found to have nuclei.', 'Viruses were discovered.', 'Fungi were found to be plants.'], 'Archaea and Bacteria are fundamentally distinct.'),
       ('Why can a traditional classification group contain organisms that are not closely related?', 'It may be based on similar features that evolved by convergent evolution.', ['It always uses DNA sequences.', 'It is based on common ancestry only.', 'It never uses morphology.'], 'E.g. “reptiles” excluding birds is not a clade.'),
       ('Which statement about a natural classification is correct?', 'It allows prediction of characteristics shared by members of a group.', ['It is based only on habitat.', 'It never changes.', 'It groups organisms by size.'], 'Shared ancestry implies shared traits.')],
  mc3=[('Organisms living in hot acidic springs have prokaryotic cells, no peptidoglycan, ether-linked membrane lipids and histone-like proteins. To which domain do they belong?', 'Archaea', ['Bacteria', 'Eukarya', 'Fungi'], 'Ether lipids and no peptidoglycan indicate Archaea.'),
       ('Genetic data show Asgard archaea share many genes with eukaryotes. What does this suggest?', 'Eukaryotes may have arisen from within the Archaea.', ['Eukaryotes evolved from Bacteria only.', 'Archaea evolved from eukaryotes.', 'Archaea and eukaryotes are unrelated.'], 'This supports a two-domain tree with eukaryotes branching from archaea.')],
  why=[('Explain the advantages of classifying organisms according to their evolutionary relationships.', 'Groups then include all descendants of a common ancestor; members share many inherited features, so characteristics of newly discovered species can be predicted; the classification reflects real evolutionary history and helps identify species.'),
       ('Explain why classification systems change over time.', 'New evidence, especially DNA and protein sequences, can reveal that existing groups do not reflect common ancestry; organisms are reclassified (e.g. the creation of domains, the move of birds into a clade with reptiles); science is self-correcting.'),
       ('Explain the evidence that led to the three-domain classification.', 'Woese compared base sequences of ribosomal RNA, which is present in all cells and evolves slowly; prokaryotes fell into two groups as different from each other as from eukaryotes; supported by differences in membrane lipids, cell walls, histones and RNA polymerase.')],
  contrast=[('Archaea', 'Bacteria', 'Both are prokaryotes; Archaea have ether-linked membrane lipids, no peptidoglycan, histones associated with DNA and introns in some genes; Bacteria have ester-linked lipids, peptidoglycan walls and no histones.'),
            ('an artificial classification', 'a natural classification', 'An artificial classification groups organisms by convenient features (e.g. habitat or flight) that may be due to convergence; a natural classification groups organisms by common ancestry so groups are clades.')],
  misc=[('Archaea are a type of bacteria because both are prokaryotes.', 'Archaea are prokaryotic but form a separate domain; their rRNA, membrane lipids and wall chemistry differ fundamentally from Bacteria and in some ways resemble eukaryotes.'),
        ('Organisms in the same order are more closely related than those in the same genus.', 'The genus is a lower, more specific taxon; members of a genus are more closely related than members of an order.')],
  cases=[('Carl Woese’s analysis of 16S ribosomal RNA (1977)', 'Methanogens had rRNA sequences very different from both bacteria and eukaryotes.', 'the three-domain system of classification', 'The data led to Archaea being recognised as a separate domain, changing the highest level of classification.'),
         ('the classification of the giant panda (Ailuropoda melanoleuca)', 'For decades it was debated whether pandas were bears or raccoons; DNA evidence placed it in the bear family, Ursidae.', 'natural classification using molecular evidence', 'Molecular data resolved a dispute that morphology alone could not, giving a classification based on common ancestry.')],
  evaluate=[('The Linnaean hierarchy of ranks is no longer useful in modern biology.', ['ranks (e.g. class, order) are arbitrary and not equivalent across groups', 'cladistics focuses on clades rather than ranks'], ['ranks provide a familiar framework for communication and teaching', 'binomial names and genera remain essential for identification and conservation'], 'Ranks remain useful as a communication tool, but classification should be based on clades revealed by molecular evidence; the hierarchy is a convention, not a natural law.')],
  extended=[('Describe the classification hierarchy and explain why the three-domain system replaced earlier classifications.', 'Domain, kingdom, phylum, class, order, family, genus, species; example (e.g. human: Eukarya, Animalia, Chordata, Mammalia, Primates, Hominidae, Homo, sapiens). Earlier two-kingdom/five-kingdom systems based on morphology; Woese rRNA: Archaea distinct; Archaea vs Bacteria lipids, walls, histones; reflects evolutionary relationships; natural classification predictive.', 8)],
  )

CYTC = {'human': 0, 'chimpanzee': 0, 'rhesus monkey': 1, 'dog': 11, 'horse': 12, 'chicken': 13, 'rattlesnake': 14, 'tuna': 21, 'yeast': 44}

S('ch04-st5',
  terms=[('clade', 'a group of organisms consisting of a common ancestor and all of its descendants'),
         ('cladogram', 'a branching diagram showing the evolutionary relationships within a clade, based on shared derived characteristics or sequence data'),
         ('node', 'a branching point on a cladogram, representing a hypothetical common ancestor'),
         ('molecular clock', 'the use of the rate at which mutations accumulate in a gene or protein to estimate the time since two lineages diverged'),
         ('parsimony', 'the principle of choosing the cladogram that requires the smallest number of evolutionary changes'),
         ('shared derived characteristic', 'a feature that evolved in the common ancestor of a clade and is found in its descendants but not in more distant relatives')],
  facts=[('What does a node on a cladogram represent?', 'a hypothetical common ancestor', ['an extinct species that has been found as a fossil', 'the present-day species', 'a mutation in a single individual'], 'Each node is a divergence point.'),
         ('Which type of evidence is now most commonly used to construct cladograms?', 'base sequences of DNA or amino acid sequences', ['size of organisms', 'habitat', 'colour'], 'Sequence data provide many characters and are less prone to convergence.'),
         ('Which principle states that the best cladogram is the one with the fewest evolutionary changes?', 'parsimony', ['falsification', 'homology', 'convergence'], 'Parsimony is used to choose between alternative trees.'),
         ('What did cladistic analysis reveal about the traditional plant family Scrophulariaceae (figworts)?', 'it was not a true clade, so many genera were moved to other families', ['it was the largest clade of plants', 'it was the first group of land plants', 'it should be merged with the animal kingdom'], 'Reclassification followed molecular evidence.')],
  mc2=[('Why are sequence differences assumed to indicate time since divergence?', 'Mutations accumulate at a roughly constant rate over time.', ['Mutations occur only during speciation.', 'Species never change after divergence.', 'Sequences are identical in all species.'], 'This is the basis of the molecular clock.'),
       ('Birds and crocodiles share a more recent common ancestor than crocodiles and lizards. What does this mean for the group “reptiles” excluding birds?', 'It is not a clade (it is paraphyletic).', ['It is a perfect clade.', 'Birds are not related to reptiles.', 'Lizards are birds.'], 'A clade must include all descendants.'),
       ('Why can cladograms based on morphology be misleading?', 'Similar structures can arise by convergent evolution in unrelated groups.', ['Morphology never varies.', 'Morphology is inherited directly from DNA in all cases.', 'Morphology is always better than DNA.'], 'Analogous structures can mislead.')],
  mc3=[('Cytochrome c of humans differs from that of horses at 12 of 104 amino acids and from that of chickens at 13. Which conclusion is best supported?', 'Humans are slightly more closely related to horses than to chickens.', ['Humans are more closely related to chickens.', 'Horses and chickens are the same species.', 'Cytochrome c is not inherited.'], 'Fewer differences indicate more recent common ancestry.'),
       ('A gene accumulates about 1 base difference per 2 million years in each lineage. Two species differ at 30 bases. Approximately when did they diverge?', '30 million years ago', ['60 million years ago', '15 million years ago', '2 million years ago'], 'Differences accumulate in both lineages: 30 ÷ 2 lineages × 2 Myr = 30 Myr.')],
  why=[('Explain how a cladogram is constructed from base sequence data.', 'Homologous sequences are aligned; the number of differences between each pair of species is counted; species with fewest differences are grouped as sharing the most recent common ancestor (node); groups are joined progressively; the most parsimonious tree is chosen.'),
       ('Explain why cladograms are regarded as hypotheses rather than proven relationships.', 'They are based on available data and assumptions (e.g. constant mutation rate, parsimony); different genes or methods can give different trees; new evidence may change them; they cannot be directly observed.'),
       ('Explain the assumptions and limitations of the molecular clock.', 'It assumes mutations accumulate at a constant rate; rates differ between genes, lineages and over time; selection can speed or slow change; it must be calibrated with fossils of known age, so estimates have uncertainty.')],
  contrast=[('a clade', 'a traditional taxonomic group', 'A clade includes a common ancestor and all its descendants, defined by shared derived features or sequences; traditional groups may be based on overall similarity and can exclude some descendants (e.g. reptiles without birds).')],
  misc=[('A cladogram shows which species evolved from which present-day species.', 'Present-day species are at the tips; a cladogram shows common ancestors (nodes), not that one living species evolved from another.'),
        ('The more similar two species look, the more closely related they must be.', 'Similar appearance can result from convergent evolution; relationships are better shown by shared derived features and sequence data.')],
  cases=[('the reclassification of the figwort family (Scrophulariaceae)', 'Analysis of chloroplast DNA sequences showed the family was not a single clade; more than half its genera were moved into other families such as Plantaginaceae.', 'how cladistics leads to reclassification', 'Classification was revised so that each family is a clade reflecting common ancestry, falsifying the earlier morphology-based grouping.'),
         ('the placement of whales within the even-toed ungulates (Cetartiodactyla)', 'DNA sequences and fossil ankle bones show whales share a common ancestor with hippopotamuses.', 'cladistics using molecular and morphological evidence', 'Sequence data revealed a relationship not obvious from body form, which fossils then confirmed.')],
  evaluate=[('Molecular data should always take priority over morphological data when constructing cladograms.', ['sequences provide thousands of characters and are less affected by convergence', 'molecular data resolved relationships such as whales with hippos'], ['DNA cannot be obtained from most fossils, so morphology is needed for extinct species', 'different genes can give conflicting trees, and horizontal gene transfer complicates analysis'], 'Molecular evidence is usually more reliable for living organisms, but the strongest cladograms combine molecular and morphological evidence, especially to include fossils.')],
  extended=[('Explain how cladograms are constructed and evaluate their use in classification.', 'Clade definition; shared derived characters; sequence alignment; count differences; parsimony; nodes = common ancestors; molecular clock for timing. Evaluation: objective, testable; reclassification (figworts, whales); limitations – convergence, rate variation, conflicting genes, hypotheses not facts.', 8)],
  )


@R.add('ch04-st5', 'C3', (1, 5), 'numerical')
def seq_diff(rng, slot):
    n = pick(rng, [18, 20, 24])
    base = [rng.choice('ATGC') for _ in range(n)]
    names_ = rng.sample(['species P', 'species Q', 'species R', 'species S'], 3)
    seqs = []
    k1 = rng.randint(1, 3)
    k2 = k1 + rng.randint(3, 6)

    def mutate(s, k):
        s = list(s)
        for i in rng.sample(range(n), k):
            s[i] = rng.choice([b for b in 'ATGC' if b != s[i]])
        return s
    a = base
    b = mutate(base, k1)
    c = mutate(base, k2)
    seqs = [''.join(a), ''.join(b), ''.join(c)]
    d_ab = sum(x != y for x, y in zip(seqs[0], seqs[1]))
    d_ac = sum(x != y for x, y in zip(seqs[0], seqs[2]))
    d_bc = sum(x != y for x, y in zip(seqs[1], seqs[2]))
    if len({d_ab, d_ac, d_bc}) < 3 or min(d_ab, d_ac, d_bc) == 0:
        return None
    lines = '\n'.join(f'{nm}: {s}' for nm, s in zip(names_, seqs))
    pairs = sorted([(d_ab, names_[0], names_[1]), (d_ac, names_[0], names_[2]), (d_bc, names_[1], names_[2])])
    close = pairs[0]
    pct = 100 * (n - pairs[0][0]) / n
    stem = f'Part of a homologous gene was sequenced in three species:\n{lines}\nCount the base differences between each pair of species and deduce which two species are most closely related.'
    ans = f'{names_[0]}–{names_[1]} {d_ab}, {names_[0]}–{names_[2]} {d_ac}, {names_[1]}–{names_[2]} {d_bc}; {close[1]} and {close[2]} most closely related'
    key = f'Differences counted correctly (A1 for all three); fewest differences = most recent common ancestor: {close[1]} and {close[2]} (R1).'
    if slot.d >= 3:
        stem += f' Calculate the percentage similarity for this pair and describe the cladogram these data support.'
        ans += f'; {pct:.1f} % similar; cladogram: {close[1]} and {close[2]} share a node, the third species branches off earlier'
        key += f' ({n} − {close[0]})/{n} × 100 = {pct:.1f} % (A1); cladogram with closest pair as sister groups (A1).'
        return num(stem, ans, key, 4)
    return num(stem, ans, key, 2)


@R.add('ch04-st5', 'C3', (2, 5), 'numerical')
def molecular_clock(rng, slot):
    rate = pick(rng, [0.5, 1, 1.5, 2, 2.5, 4])
    diffs = rng.randint(6, 60)
    gene = pick(rng, ['mitochondrial cytochrome b gene', 'nuclear rRNA gene', 'haemoglobin β-chain gene', 'COI barcode gene', 'chloroplast rbcL gene'])
    grp = pick(rng, ['two species of cichlid fish', 'two genera of lemurs', 'two species of oak', 'two species of Darwin’s finch', 'two populations of cave salamander', 'two species of baobab'])
    t = diffs / rate
    stem = (f'The {gene} of {grp} differs at {diffs} positions. Calibration with dated fossils shows that this gene accumulates differences between two lineages at {rate} per million years. '
            f'Estimate how long ago the two lineages diverged.')
    ans = f'{sf(t)} million years ago'
    key = f'Time = differences ÷ rate = {diffs} ÷ {rate} (M1) = {sf(t)} Myr (A1).'
    if slot.d >= 4:
        stem += ' State two assumptions of this estimate.'
        ans += '; assumes constant mutation rate over time and in both lineages, and accurate fossil calibration'
        key += ' Constant rate / clock-like (A1); accurate calibration / no saturation (repeated mutations at same site) (A1).'
        return num(stem, ans, key, 4)
    return num(stem, ans, key, 2)


def _cytc_dq(rng, slot):
    sp = ['chimpanzee', 'rhesus monkey', 'dog', 'horse', 'chicken', 'rattlesnake', 'tuna', 'yeast']
    pick5 = sorted(rng.sample(sp, 5), key=lambda s: CYTC[s])
    rows = [(s, CYTC[s], f'{100 * CYTC[s] / 104:.1f}') for s in pick5]
    intro = ('Cytochrome c is a protein of 104 amino acids found in the electron transport chain of all aerobic organisms. The table shows the number of amino acid differences between human cytochrome c and that of other species.\n\n'
             + table(['Species', 'Amino acid differences from human', '% difference'], [(r[0], r[1], '?' if i == len(rows) - 1 else r[2]) for i, r in enumerate(rows)]))
    last = pick5[-1]
    first = pick5[0]
    parts = [
        ('Identify the species most closely related to humans according to these data.', first, f'{first} (A1).', 1),
        (f'Calculate the percentage difference for {last}.', f'{100 * CYTC[last] / 104:.1f} %', f'{CYTC[last]}/104 × 100 (M1) = {100 * CYTC[last] / 104:.1f} % (A1).', 2),
        ('Explain why cytochrome c is useful for comparing distantly related species.', 'It is found in all aerobic organisms (universal), has an essential function so changes slowly, so differences accumulate gradually over very long times.', 'Present in all aerobic organisms (A1); slow, steady rate of change (A1).', 2),
        ('Explain how these data could be used to construct a cladogram.', 'Species with fewer differences share a more recent common ancestor and are placed on branches joined at a more recent node; the species with most differences branches off first (outgroup).', 'Fewer differences = closer (A1); nodes as common ancestors / outgroup branching first (A1).', 2),
        ('Suggest why comparing DNA base sequences may give more information than comparing amino acid sequences.', 'Because the code is degenerate, some base changes (silent mutations) do not change the amino acid; DNA also includes non-coding regions, so more differences can be detected.', 'Degenerate code / silent mutations (A1); more characters / non-coding DNA (A1).', 2),
        (f'Using a molecular clock of 1 amino acid change per 6 million years between lineages, estimate the time since humans and {pick5[2]} shared a common ancestor.', f'{CYTC[pick5[2]] * 6} million years ago', f'{CYTC[pick5[2]]} × 6 = {CYTC[pick5[2]] * 6} Myr (A1); accept with assumption of constant rate.', 1),
        ('Outline one limitation of using a single protein to deduce relationships.', 'Rates of change may vary between lineages; one protein gives few characters so trees may be unresolved or misleading; should be supported by other genes and fossils.', 'Any valid limitation (A1).', 1),
        ('Explain why the same protein can show differences between species despite having the same function.', 'Mutations that do not affect the active regions are neutral and accumulate over time; more time since divergence means more differences.', 'Neutral mutations outside key regions (A1); accumulate with time (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch04-st5', _cytc_dq)


# =============================================================================================
# ch05 A4.1 Evolution and speciation
# =============================================================================================
S('ch05-st1',
  terms=[('evolution', 'the cumulative change in the heritable characteristics of a population over time'),
         ('homologous structures', 'structures that have the same basic anatomy because they were inherited from a common ancestor, though they may have different functions'),
         ('selective breeding', 'artificial selection in which humans choose individuals with desired traits to breed, changing the characteristics of domesticated species over generations'),
         ('pentadactyl limb', 'a limb with five digits and a common bone pattern (humerus, radius and ulna, carpals, metacarpals, phalanges) found in tetrapods'),
         ('vestigial structure', 'a reduced structure that had a function in an ancestor but has little or no function in the present organism')],
  facts=[('Which is an example of homologous structures?', 'the forelimb of a bat and the flipper of a whale', ['the wing of a bat and the wing of a butterfly', 'the eye of an octopus and the eye of a human', 'the fins of a shark and the flippers of a dolphin'], 'Both have the pentadactyl bone pattern from a common ancestor.'),
         ('Which crop plants were all produced by selective breeding from wild cabbage (Brassica oleracea)?', 'broccoli, cauliflower, kale and Brussels sprouts', ['potato, tomato and aubergine', 'wheat, rice and maize', 'carrot, parsnip and celery'], 'Selection for different parts (flowers, leaves, buds) produced very different vegetables.'),
         ('What is the wild ancestor of maize?', 'teosinte', ['wild rice', 'sorghum', 'wheat'], 'Domestication in Mexico about 9000 years ago transformed the cob.'),
         ('Which type of evidence for evolution compares the order of nucleotides in genes of different species?', 'base sequence evidence', ['fossil evidence', 'homologous structures', 'selective breeding'], 'Similarity of sequences indicates common ancestry.')],
  mc2=[('Why does selective breeding provide evidence for evolution by natural selection?', 'It shows that heritable characteristics of a species can change considerably in a relatively short time when selection acts.', ['It shows humans created all species.', 'It proves that acquired characteristics are inherited.', 'It shows mutation is not needed.'], 'Large changes occur through selection of heritable variation.'),
       ('Why are similarities in base sequences strong evidence for common ancestry?', 'Sequences are copied with small changes from generation to generation, so shared sequences are inherited from a common ancestor.', ['All species need the same sequences to survive.', 'Sequences are identical in all species.', 'Sequences are acquired from the environment.'], 'Neutral or non-coding similarities are hard to explain any other way.'),
       ('Which observation about the pentadactyl limb best supports common ancestry rather than common function?', 'The same bone pattern occurs in limbs used for very different functions.', ['All limbs are used for walking.', 'Limbs of unrelated animals look similar.', 'Limbs evolved independently in each species.'], 'Divergent function with conserved structure indicates inheritance.')],
  mc3=[('In the Illinois long-term selection experiment, maize oil content rose from about 4.7 % to about 20 % over 100 generations. What is the percentage increase?', 'about 326 %', ['about 15 %', 'about 76 %', 'about 426 %'], '(20 − 4.7)/4.7 × 100 ≈ 326 %.'),
       ('Two species share a broken (non-functional) copy of the GULO gene needed to make vitamin C, with the same inactivating mutation. Which conclusion is best supported?', 'The mutation occurred in a common ancestor of both species.', ['The mutation occurred independently twice in the same way.', 'Both species need vitamin C from the gene.', 'The gene was transferred between them by viruses.'], 'Shared identical mutations indicate common descent (e.g. humans and other primates).')],
  why=[('Explain how homologous structures provide evidence for evolution.', 'Structures such as the pentadactyl limb share the same basic bone arrangement in different species despite different functions (walking, flying, swimming, grasping); this is best explained by inheritance from a common ancestor followed by adaptive radiation.'),
       ('Explain how selective breeding of domesticated animals provides evidence for evolution.', 'Domesticated breeds (e.g. dogs from wolves) differ greatly from their wild ancestors and each other; this shows that selection of heritable variation over many generations can produce large changes, analogous to natural selection.'),
       ('Explain how comparison of base sequences is used as evidence for evolution.', 'Homologous genes are compared between species; the number of differences increases with the time since species diverged; patterns of similarity match those from anatomy and fossils, supporting common ancestry.')],
  contrast=[('natural selection', 'selective breeding (artificial selection)', 'In natural selection the environment determines which variants survive and reproduce; in selective breeding humans choose which individuals breed according to desired traits; both change allele frequencies of heritable characteristics over generations.')],
  misc=[('Selective breeding creates new genes in the animals being bred.', 'Selective breeding selects among existing heritable variation (alleles); new alleles only arise by mutation.'),
        ('Homologous structures always have the same function.', 'Homologous structures share structure and origin, but often have different functions, e.g. bat wing and human arm.')],
  cases=[('the domestication of dogs from grey wolves', 'Over at least 15 000 years, selection produced breeds as different as chihuahuas and Great Danes, all of the same species.', 'selective breeding as evidence for evolution', 'Large heritable changes in a short time show how selection can change a species.'),
         ('the pentadactyl limbs of humans, bats, whales and moles', 'All have humerus, radius/ulna, carpals, metacarpals and phalanges, modified for grasping, flying, swimming and digging.', 'homologous structures as evidence for evolution', 'The shared structure despite different functions indicates descent from a common tetrapod ancestor (adaptive radiation).')],
  apply=[('Describe how you would compare the pentadactyl limbs of a frog, a bird and a human to show homology. State the bones you would identify.', 'Identify in each: one upper bone (humerus), two lower bones (radius and ulna), wrist bones (carpals), palm bones (metacarpals), digits (phalanges); note modifications: fused bones in bird wing, long digits in humans, frog radio-ulna fused.', 3)],
  evaluate=[('Base sequence data are more convincing evidence for evolution than homologous anatomical structures.', ['sequences provide many objective, quantifiable characters', 'shared non-functional sequences (pseudogenes, viral insertions) are very hard to explain without common descent'], ['homologous structures were the first strong evidence and are visible in fossils', 'both lines of evidence agree, so each strengthens the other'], 'Sequence data are more quantitative and can resolve relationships that anatomy cannot, but evidence is most convincing when molecular and anatomical data independently agree.')],
  extended=[('Outline three types of evidence for evolution, using a specific example for each.', 'Base sequences: e.g. cytochrome c or human–chimp DNA similarity; shared pseudogenes such as GULO. Selective breeding: dogs from wolves, Brassica crops, maize from teosinte – large change in short time. Homologous structures: pentadactyl limb in bat, whale, human – common ancestry. Fossils (optional): sequence of forms in rocks.', 8)],
  )


@R.add('ch05-st1', 'C3', (1, 4), 'numerical')
def breeding_gain(rng, slot):
    ctx = pick(rng, [('Mean oil content of maize kernels in a selection line', '%', 4.5, 5.0, 3.0, 4.5),
                     ('Mean milk yield of a herd of dairy cattle', 'litres per year', 2500, 3500, 1.5, 3.0),
                     ('Mean body mass of broiler chickens at 6 weeks', 'kg', 0.6, 0.9, 1.5, 3.0),
                     ('Mean grain yield of a wheat variety', 't per hectare', 1.5, 2.5, 0.8, 2.0),
                     ('Mean fleece mass of Merino sheep', 'kg', 2.5, 3.5, 0.6, 1.5)])
    label, unit, lo, hi, rlo, rhi = ctx
    a = round(rng.uniform(lo, hi), 1 if a_small(hi) else 0)
    b = round(a * (1 + rng.uniform(rlo, rhi)), 1 if a_small(hi) else 0)
    gens = pick(rng, [20, 30, 40, 50, 80, 100])
    p = pct_change(a, b)
    per = (b - a) / gens
    stem = f'{label} increased from {a:g} {unit} to {b:g} {unit} over {gens} generations of selective breeding. Calculate the percentage increase and the mean increase per generation.'
    ans = f'{p:.0f} %; {sf(per)} {unit} per generation'
    key = f'({b:g} − {a:g})/{a:g} × 100 = {p:.0f} % (A1); ({b:g} − {a:g})/{gens} = {sf(per)} {unit} per generation (A1).'
    if slot.d >= 3:
        stem += ' Explain why this provides evidence for evolution.'
        key += ' Heritable variation selected over generations changes the population’s characteristics – same principle as natural selection (R1).'
        ans += '; heritable traits changed through selection over generations'
        return num(stem, ans, key, 3)
    return num(stem, ans, key, 2)


def a_small(hi):
    return hi < 100


S('ch05-st2',
  terms=[('convergent evolution', 'the independent evolution of similar features in unrelated lineages as adaptations to similar environments or ways of life'),
         ('divergent evolution', 'the accumulation of differences between related populations, often leading to new species with different adaptations'),
         ('analogous structures', 'structures with a similar function and appearance that evolved independently and do not share a common ancestral origin'),
         ('adaptive radiation', 'the rapid divergence of an ancestral species into many species adapted to different niches')],
  facts=[('Which pair are analogous structures?', 'the wing of a bird and the wing of an insect', ['the arm of a human and the wing of a bat', 'the flipper of a whale and the leg of a horse', 'the leaf of a cactus spine and a pea tendril'], 'Bird and insect wings evolved independently.'),
         ('The streamlined shape of sharks (fish) and dolphins (mammals) is an example of', 'convergent evolution', ['divergent evolution', 'homology', 'polyploidy'], 'Similar selection pressures in water produced similar body forms.'),
         ('Which is an example of divergent evolution?', 'the pentadactyl limb modified as a bat wing and a whale flipper', ['the eyes of octopuses and humans', 'the wings of birds and bats', 'the spines of cacti and euphorbias'], 'A common ancestral structure diverged in function.'),
         ('Which pair of plants shows convergent evolution in dry habitats?', 'American cacti and African euphorbias', ['oak and beech', 'wheat and rice', 'two species of Brassica'], 'Both have succulent stems and spines but are unrelated.')],
  mc2=[('Why do analogous structures not indicate close evolutionary relationship?', 'They evolved independently in response to similar selection pressures.', ['They are inherited from a recent common ancestor.', 'They have identical genes.', 'They always have different functions.'], 'Similarity due to convergence, not ancestry.'),
       ('Which evidence would show that the eyes of an octopus and a human evolved convergently?', 'They develop from different tissues and the octopus retina lacks a blind spot.', ['Both eyes detect light.', 'Both eyes have lenses.', 'Both animals are large.'], 'Different structural details reveal independent origins.'),
       ('Which statement correctly links homologous and analogous structures to types of evolution?', 'Homologous structures result from divergent evolution; analogous structures from convergent evolution.', ['Homologous structures result from convergent evolution.', 'Both result from convergent evolution.', 'Analogous structures result from divergent evolution.'], 'Divergence modifies a shared structure; convergence produces similar ones independently.')],
  mc3=[('Thylacines (marsupials) and grey wolves (placental mammals) have remarkably similar skulls. DNA shows they last shared an ancestor about 160 million years ago. What does this illustrate?', 'convergent evolution of analogous features', ['divergent evolution from a recent ancestor', 'homologous skull structures from a recent ancestor', 'selective breeding'], 'Similar predatory niches selected similar skull shapes.'),
       ('Moles (Eurasia) and marsupial moles (Australia) both have reduced eyes, spade-like forelimbs and dense fur. Which conclusion is best supported?', 'Similar selection pressures from burrowing produced similar adaptations independently.', ['They are closely related.', 'One evolved from the other.', 'They interbreed.'], 'Classic convergence between placental and marsupial mammals.')],
  why=[('Explain how convergent evolution can produce analogous structures.', 'Unrelated species living in similar environments face similar selection pressures; individuals with variations that improve survival in that environment reproduce more; over many generations similar structures evolve independently in each lineage, e.g. streamlined bodies in sharks and dolphins.'),
       ('Explain why analogous structures can lead to errors in classification.', 'Analogous structures look similar but have different evolutionary origins; grouping organisms by them would place unrelated organisms together, so classification must use homologous features and molecular data.')],
  contrast=[('homologous structures', 'analogous structures', 'Homologous structures share the same basic structure because of common ancestry, though functions may differ; analogous structures have similar functions but different structures and origins, evolving by convergence.'),
            ('convergent evolution', 'divergent evolution', 'Convergent evolution makes unrelated lineages more similar through similar selection pressures; divergent evolution makes related lineages more different as they adapt to different environments.')],
  misc=[('Bird wings and bat wings are homologous because they both are used for flight.', 'As forelimbs they are homologous (pentadactyl limb), but as wings they are analogous: flight evolved independently, with feathers in birds and skin membranes in bats.'),
        ('Convergent evolution means two species are becoming one species.', 'Convergence produces similar features in unrelated species; they remain separate lineages and cannot interbreed.')],
  cases=[('the thylacine (Thylacinus cynocephalus) and the grey wolf (Canis lupus)', 'A marsupial and a placental mammal evolved very similar skull shapes and body form as large predators.', 'convergent evolution', 'Similar niches produced similar features despite the lineages having separated about 160 million years ago.'),
         ('the cacti of the Americas and the euphorbias of Africa', 'Both have succulent stems, spines and reduced leaves for water storage and protection in deserts.', 'analogous structures', 'Their similar forms evolved independently in response to arid conditions; flowers and DNA show they are unrelated.')],
  evaluate=[('Convergent evolution shows that evolution is predictable.', ['similar environments repeatedly produce similar solutions, e.g. streamlining, eyes, succulence', 'experiments with Anolis lizards and Lenski’s E. coli show repeated similar adaptations'], ['many lineages in similar environments evolve different solutions', 'chance events such as mutation and drift make the exact course of evolution unpredictable'], 'Convergence shows evolution is constrained and partly predictable in broad outline, but historical contingency means details cannot be predicted.')],
  extended=[('Distinguish between convergent and divergent evolution, using examples of homologous and analogous structures.', 'Divergent: common ancestor, different environments, homologous structures – pentadactyl limb in bat, whale, human. Convergent: unrelated, similar environments, analogous structures – wings of birds and insects, cacti and euphorbias, shark and dolphin shape, thylacine and wolf. Significance for classification.', 7)],
  )

S('ch05-st3',
  terms=[('speciation', 'the formation of new species by the splitting of an existing species'),
         ('reproductive isolation', 'the inability of members of two populations to interbreed and produce fertile offspring, separating their gene pools'),
         ('allopatric speciation', 'speciation that occurs when populations are separated geographically'),
         ('sympatric speciation', 'speciation that occurs within the same geographical area, through behavioural or temporal isolation or polyploidy'),
         ('behavioural isolation', 'reproductive isolation caused by differences in courtship or mating behaviour'),
         ('temporal isolation', 'reproductive isolation caused by populations breeding at different times of day or year')],
  facts=[('What is required for allopatric speciation?', 'a geographical barrier separating populations', ['polyploidy', 'living in the same habitat', 'identical selection pressures'], 'The barrier prevents gene flow.'),
         ('Which example illustrates speciation following geographical isolation?', 'chimpanzees and bonobos separated by the Congo River', ['apple maggot flies on apples and hawthorns', 'polyploid wheat', 'mule production'], 'The river prevented gene flow for about 1–2 million years.'),
         ('Two populations of crickets mature and breed in different seasons. This is', 'temporal isolation', ['geographical isolation', 'behavioural isolation', 'hybrid sterility'], 'Breeding at different times prevents interbreeding.'),
         ('Speciation by splitting requires', 'reproductive isolation followed by differential selection', ['identical environments', 'interbreeding between populations', 'no variation'], 'Isolated gene pools diverge under different selection pressures.')],
  mc2=[('Why does a geographical barrier lead to speciation?', 'It prevents gene flow, so populations accumulate different mutations and are selected differently.', ['It causes mutations directly.', 'It makes populations identical.', 'It increases interbreeding.'], 'Separated gene pools diverge until reproductive isolation is complete.'),
       ('Why does speciation require differential selection as well as isolation?', 'Different selection pressures cause the gene pools to diverge in adaptive traits.', ['Selection keeps populations identical.', 'Isolation alone always produces identical species.', 'Selection causes isolation.'], 'Drift alone may also cause divergence but slowly.'),
       ('Which mechanism of reproductive isolation can operate in sympatric speciation?', 'differences in courtship songs between groups living together', ['a mountain range between populations', 'an ocean between islands', 'a river separating two forests'], 'Behavioural isolation acts without geographical separation.')],
  mc3=[('Two populations of a fish in one lake feed at different depths and now prefer to mate with fish of their own colour. Which type of speciation is occurring?', 'sympatric speciation with behavioural isolation', ['allopatric speciation', 'polyploidy', 'artificial selection'], 'Same area; mate choice isolates gene pools (e.g. cichlids in Lake Victoria).'),
       ('Two bird populations on either side of a new mountain range differ in song after 10 000 years. When reunited they do not interbreed. What has occurred?', 'allopatric speciation', ['sympatric speciation', 'hybrid vigour', 'convergent evolution'], 'Geographical isolation led to reproductive isolation.')],
  why=[('Explain how allopatric speciation can occur.', 'A geographical barrier divides a population; gene flow stops; mutations, genetic drift and different selection pressures cause allele frequencies to diverge; eventually the populations become so different that they cannot interbreed even if they meet again (reproductive isolation).'),
       ('Explain how differences in behaviour can lead to sympatric speciation.', 'If individuals choose mates with particular courtship signals, colours or songs, gene flow between groups is reduced even in the same area; the groups diverge genetically and become reproductively isolated.'),
       ('Explain why bonobos and chimpanzees are considered separate species.', 'They were geographically isolated by the Congo River for 1–2 million years; their populations diverged in behaviour, morphology and genes; they do not interbreed in the wild.')],
  contrast=[('allopatric speciation', 'sympatric speciation', 'Allopatric speciation occurs when populations are separated by a geographical barrier; sympatric speciation occurs in the same area through behavioural, temporal or genetic (polyploidy) isolation.'),
            ('behavioural isolation', 'temporal isolation', 'Behavioural isolation results from differences in courtship or mating signals; temporal isolation results from breeding at different times of day or year.')],
  misc=[('Speciation happens when an individual suddenly gives birth to a new species.', 'Speciation is normally a gradual process in populations over many generations, though polyploidy can produce a new plant species in one or two generations.'),
        ('Any geographical barrier immediately creates new species.', 'The barrier only stops gene flow; speciation follows only after the gene pools diverge enough to cause reproductive isolation.')],
  cases=[('bonobos (Pan paniscus) and chimpanzees (Pan troglodytes)', 'Populations south of the Congo River were separated from those north of it about 1–2 million years ago.', 'allopatric speciation', 'Geographical isolation stopped gene flow and the populations diverged into two species.'),
         ('apple maggot flies (Rhagoletis pomonella)', 'Some flies switched from hawthorn to introduced apple trees; they mate on their host fruit, which ripens at different times.', 'sympatric speciation', 'Host preference and timing produce behavioural and temporal isolation within the same area.'),
         ('cichlid fish in Lake Victoria', 'Hundreds of species evolved in about 15 000 years; females choose males by colour, and populations specialise in different food.', 'reproductive isolation and speciation', 'Mate choice for colour causes behavioural isolation and rapid speciation without geographical barriers.')],
  evaluate=[('Allopatric speciation is far more common than sympatric speciation.', ['geographical isolation easily stops gene flow, as in many island and river examples', 'most well-documented speciation events involve geographical separation'], ['polyploidy is a common sympatric mechanism in plants, perhaps 15 % of plant speciation events', 'cichlids and apple maggot flies show sympatric speciation in animals'], 'Allopatric speciation is probably most common in animals, but sympatric speciation, especially by polyploidy in plants, is significant; relative frequency differs between groups.')],
  extended=[('Explain how reproductive isolation can lead to speciation, distinguishing between allopatric and sympatric speciation.', 'Speciation = split; need isolation of gene pools + differential selection; allopatric – barrier (bonobos/chimps, Congo River); sympatric – behavioural (cichlids), temporal (Rhagoletis), polyploidy; eventual inability to produce fertile offspring; gradual divergence.', 8)],
  )


def _finch_dq(rng, slot):
    yrs = [1976, 1977, 1978]
    m0 = round(rng.uniform(9.0, 9.4), 2)
    m1 = round(m0 + rng.uniform(0.4, 0.6), 2)
    m2 = round(m1 - rng.uniform(0.05, 0.2), 2)
    n0 = rng.randint(1100, 1400)
    n1 = int(n0 * rng.uniform(0.12, 0.18))
    s0 = round(rng.uniform(0.9, 1.1), 2)
    pc = pct_change(m0, m1)
    surv = 100 * n1 / n0
    intro = ('On Daphne Major in the Galápagos, Peter and Rosemary Grant measured the beak depth of medium ground finches (Geospiza fortis). A severe drought in 1977 reduced the supply of small, soft seeds; mainly large, hard seeds remained.\n\n'
             + table(['Year', 'Population', 'Mean beak depth / mm'], [(1976, n0, f'{m0:.2f}'), (1977, n1, f'{m1:.2f}'), (1978, '—', f'{m2:.2f}')])
             + f'\n\nThe standard deviation of beak depth in 1976 was {s0} mm.')
    parts = [
        ('Calculate the percentage of the 1976 population that survived to 1977.', f'{surv:.1f} %', f'{n1}/{n0} × 100 (M1) = {surv:.1f} % (A1).', 2),
        ('Calculate the percentage change in mean beak depth from 1976 to 1977.', f'{signed(pct_change(m0, m1))} %', f'({m1:.2f} − {m0:.2f})/{m0:.2f} × 100 (M1) = {signed(pc)} % (A1).', 2),
        ('Explain the change in mean beak depth between 1976 and 1977.', 'Variation in beak depth existed; during the drought only large hard seeds remained; birds with deeper beaks could crack them, survived and reproduced; so the mean beak depth of the survivors increased.', 'Variation present (A1); large seeds the selection pressure (A1); deeper-beaked birds survive (A1).', 3),
        ('Explain why the offspring produced in 1978 also had deeper beaks than the 1976 population.', 'Beak depth is heritable; survivors passed alleles for deeper beaks to their offspring, so allele frequencies changed – evolution.', 'Heritability (A1); allele frequency change between generations (A1).', 2),
        (f'The change in mean beak depth was about {abs(m1 - m0) / s0:.1f} standard deviations. Comment on the size of this change.', 'Large for one generation; shows strong directional selection.', 'Recognises a substantial shift relative to natural variation (A1).', 1),
        ('Suggest why this study is described as evolution being observed in action.', 'The change in a heritable characteristic of the population was measured over a single generation, rather than inferred from fossils.', 'Measured directly across generations / short time scale (A1).', 1),
        ('State the type of selection shown by these data.', 'directional selection', 'Directional (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch05-st3', _finch_dq)

S('ch05-st4',
  terms=[('polyploidy', 'the condition of having more than two complete sets of chromosomes in a cell'),
         ('autopolyploidy', 'polyploidy in which the extra chromosome sets come from the same species, e.g. by failure of chromosomes to separate in meiosis'),
         ('allopolyploidy', 'polyploidy arising from hybridisation between two species followed by doubling of the chromosome number'),
         ('adaptive radiation', 'the rapid evolution of many species from a common ancestor, each adapted to a different niche'),
         ('hybrid sterility', 'the inability of a hybrid between two species to produce viable gametes, usually because its chromosomes cannot pair in meiosis')],
  facts=[('Which is a classic example of adaptive radiation?', 'Darwin’s finches on the Galápagos Islands', ['the peppered moth in Britain', 'polyploid wheat', 'antibiotic resistance in bacteria'], 'About 15 species evolved from one ancestor, with beaks for different foods.'),
         ('How does polyploidy cause instant reproductive isolation?', 'polyploid individuals cannot produce fertile offspring with the parent species', ['polyploids live in different habitats', 'polyploids have fewer genes', 'polyploids cannot photosynthesise'], 'Crosses between a tetraploid and a diploid give sterile triploids.'),
         ('Which genus of plants, used as an example in the IB course, shows speciation by polyploidy with species at several different ploidy levels?', 'Persicaria (knotweeds)', ['Homo', 'Canis', 'Drosophila'], 'Persicaria species show multiple ploidy levels.'),
         ('Bread wheat is hexaploid. How many sets of chromosomes does it have?', 'six', ['two', 'three', 'four'], 'It arose from hybridisations between three ancestral species.')],
  mc2=[('Why is polyploidy much more common in plants than in animals?', 'Many plants can self-fertilise or reproduce asexually, so a single polyploid can establish a population.', ['Plants do not undergo meiosis.', 'Animals have no chromosomes.', 'Plants have smaller genomes.'], 'A new polyploid needs a compatible mate; selfing provides one.'),
       ('Why can an allopolyploid formed by chromosome doubling be fertile when the original hybrid was sterile?', 'Each chromosome now has a homologue to pair with during meiosis.', ['Doubling removes extra chromosomes.', 'Doubling makes it diploid.', 'Doubling joins the chromosomes together.'], 'Restored pairing allows balanced gametes.'),
       ('What promotes adaptive radiation on newly formed islands?', 'many vacant niches and isolation from the mainland', ['strong competition from many existing species', 'identical habitats on every island', 'continuous gene flow from the mainland'], 'Empty niches allow divergence.')],
  mc3=[('Species A (2n = 18) and species B (2n = 18) hybridise. The hybrid is sterile, but a fertile plant arises after chromosome doubling. What is its chromosome number?', '36', ['18', '9', '27'], 'Hybrid 9 + 9 = 18; doubled to 36 (allotetraploid).'),
       ('Hawaiian honeycreepers have beaks ranging from short and thick to long and curved. What process is best illustrated?', 'adaptive radiation from a common ancestor', ['convergent evolution', 'polyploidy', 'artificial selection'], 'One ancestral finch-like bird diversified into many niches.')],
  why=[('Explain how allopolyploidy can produce a new species in a short time.', 'Two species hybridise; the hybrid is sterile because chromosomes have no homologues; chromosome doubling (e.g. failure of mitosis/meiosis) gives each chromosome a partner; the allopolyploid is fertile but cannot produce fertile offspring with either parent, so it is a new reproductively isolated species.'),
       ('Explain how adaptive radiation leads to an increase in biodiversity.', 'An ancestral species reaches an area with many vacant niches; populations become isolated and specialise for different resources; differential selection and isolation cause each to become a new species, so many species arise from one.')],
  contrast=[('autopolyploidy', 'allopolyploidy', 'Autopolyploidy involves extra sets of chromosomes from the same species (e.g. through non-disjunction); allopolyploidy involves combining chromosome sets of two different species by hybridisation followed by doubling.')],
  misc=[('Polyploid plants are always weaker than diploid plants.', 'Polyploids are often larger and more vigorous (e.g. many crops such as wheat, strawberries and potatoes are polyploid).'),
        ('Adaptive radiation is the same as convergent evolution.', 'Adaptive radiation is divergence from one ancestor into many forms; convergent evolution is unrelated lineages becoming similar.')],
  cases=[('Darwin’s finches on the Galápagos Islands', 'About 15 species evolved from a single ancestral species that arrived from South America about 2 million years ago, with beaks adapted for seeds, insects, cactus and even blood.', 'adaptive radiation', 'Vacant niches on isolated islands allowed one ancestor to diversify into species with different feeding adaptations.'),
         ('the knotweed genus Persicaria', 'Closely related species carry different multiples of a basic chromosome set (for example P. hydropiper 2n = 20 and P. maculosa 2n = 44), reflecting polyploidy.', 'speciation by polyploidy', 'Doubling of chromosome sets created instant reproductive isolation and new species within the genus.')],
  evaluate=[('Polyploidy is the most important mechanism of speciation in flowering plants.', ['about a third or more of flowering-plant species are polyploid and many crops arose this way', 'polyploidy causes instant reproductive isolation'], ['many plant species arise by allopatric speciation and ecological divergence', 'most new polyploids fail to establish'], 'Polyploidy is a major and characteristic mechanism in plants, but not the only one; its importance varies between plant groups.')],
  extended=[('Explain how polyploidy and adaptive radiation each contribute to speciation, using named examples.', 'Polyploidy: non-disjunction/doubling; auto vs allo; hybrid sterile; doubling restores pairing; instant reproductive isolation; examples Persicaria, wheat, Spartina anglica. Adaptive radiation: one ancestor, many vacant niches, isolation, differential selection; Darwin’s finches, Hawaiian honeycreepers, cichlids; increases biodiversity.', 8)],
  )


@R.add('ch05-st4', 'C3', (1, 5), 'numerical')
def allopolyploid(rng, slot):
    a = pick(rng, [10, 12, 14, 16, 18, 20, 24, 28])
    b = pick(rng, [10, 12, 14, 16, 18, 20, 24, 28, 30])
    genus = pick(rng, ['Spartina', 'Tragopogon', 'Brassica', 'Primula', 'Senecio', 'Persicaria', 'Gossypium', 'Nicotiana'])
    hyb = a // 2 + b // 2
    stem = f'Two species of {genus} have diploid numbers 2n = {a} and 2n = {b}. They hybridise. State the number of chromosomes in each gamete of the parents and in the hybrid.'
    ans = f'gametes {a // 2} and {b // 2}; hybrid {hyb}'
    key = f'Gametes {a // 2} and {b // 2} (A1); hybrid {hyb} (A1).'
    if slot.d >= 3:
        stem += ' The hybrid is sterile, but after a doubling of chromosome number a fertile plant appears. State its chromosome number and explain why it is fertile and is a new species.'
        ans += f'; allopolyploid 2n = {2 * hyb}; every chromosome has a homologue so meiosis is normal; cannot form fertile offspring with either parent'
        key += f' {2 * hyb} (A1); homologues pair in meiosis (R1); crosses with parents give sterile offspring = reproductive isolation (R1).'
        return num(stem, ans, key, 5)
    return num(stem, ans, key, 2)


# =============================================================================================
# ch06 A4.2 Conservation of biodiversity
# =============================================================================================
S('ch06-st1',
  terms=[('biodiversity', 'the variety of life in all its forms, levels and combinations, including ecosystem, species and genetic diversity'),
         ('species richness', 'the number of different species present in an area'),
         ('species evenness', 'how similar the abundances of the different species in an area are'),
         ('genetic diversity', 'the variety of alleles and genes within a species or population'),
         ('ecosystem diversity', 'the variety of habitats, communities and ecological processes in an area'),
         ('Simpson’s reciprocal index', 'a measure of species diversity, D = N(N − 1)/Σn(n − 1), that takes account of both richness and evenness')],
  facts=[('Which index used in IB Biology combines species richness and evenness?', 'Simpson’s reciprocal index', ['the Lincoln index', 'the chi-squared statistic', 'the mitotic index'], 'D = N(N − 1)/Σn(n − 1).'),
         ('What is the minimum value of Simpson’s reciprocal index?', '1', ['0', '−1', '100'], 'D = 1 when only one species is present.'),
         ('Approximately how many species have been described scientifically?', 'about 2 million', ['about 20 000', 'about 200 million', 'about 2 billion'], 'Estimates of total species range from about 8 million to far more.'),
         ('Which level of biodiversity is reduced when a population loses alleles through inbreeding?', 'genetic diversity', ['ecosystem diversity', 'species richness', 'species evenness'], 'Small populations lose alleles by drift and inbreeding.')],
  mc2=[('Two woodlands each contain the same five species. In woodland X the species are equally abundant; in Y one species makes up 90 % of individuals. Which statement is correct?', 'Woodland X has the higher Simpson’s reciprocal index.', ['Woodland Y has the higher index.', 'Both have the same index.', 'Neither can be compared.'], 'Evenness raises D; dominance by one species lowers it.'),
       ('Why is genetic diversity within a species important for its survival?', 'It provides variation on which natural selection can act if conditions change.', ['It makes all individuals identical.', 'It prevents mutations.', 'It reduces the number of alleles.'], 'Low diversity increases vulnerability to disease and change.'),
       ('Why are estimates of the total number of species on Earth uncertain?', 'Many organisms, especially microbes and insects, have not been described.', ['All species have been catalogued.', 'Species numbers never change.', 'DNA cannot be used to identify species.'], 'Most species are undescribed.')],
  mc3=[('A pond sample contains 10 water beetles, 10 snails and 10 mayfly larvae. What is Simpson’s reciprocal index?', '3.2', ['3.0', '30', '0.31'], 'N = 30: 30 × 29 = 870; Σn(n − 1) = 3 × 90 = 270; D = 870/270 = 3.2.'),
       ('Simpson’s index for a coral reef fell from 8.2 to 3.1 after a bleaching event. Which is the best interpretation?', 'Diversity fell: fewer species and/or a few species now dominate.', ['Diversity increased.', 'All species went extinct.', 'Only species richness changed.'], 'Lower D means lower richness and/or evenness.')],
  why=[('Explain why biodiversity is considered at ecosystem, species and genetic levels.', 'Each level contributes differently: ecosystem diversity provides a range of habitats and processes; species diversity reflects the variety of organisms and interactions; genetic diversity within species allows adaptation; loss at any level reduces resilience.'),
       ('Explain why Simpson’s reciprocal index is more informative than species richness alone.', 'Richness counts species but ignores how individuals are distributed; the index includes evenness, so a community dominated by one species scores lower than one with equally common species, even with the same richness.')],
  contrast=[('species richness', 'species evenness', 'Species richness is the number of species present; evenness is how equally individuals are distributed among those species.')],
  misc=[('A habitat with more species always has higher biodiversity according to Simpson’s index.', 'Simpson’s index also depends on evenness; a richer community dominated by one species can have a lower index than a less rich but even community.'),
        ('Biodiversity only refers to the number of species.', 'Biodiversity includes ecosystem, species and genetic diversity.')],
  cases=[('the Amazon rainforest', 'It contains around 10 % of known species and many unique habitats, from flooded várzea to terra firme forest.', 'biodiversity at ecosystem, species and genetic levels', 'High ecosystem diversity supports enormous species richness, and each species contains genetic diversity adapted to local conditions.'),
         ('the cheetah (Acinonyx jubatus)', 'Cheetahs have very low genetic diversity, probably from a population bottleneck about 10 000 years ago.', 'the importance of genetic diversity', 'Low diversity makes the species more vulnerable to disease and reduces its ability to adapt.')],
  evaluate=[('Simpson’s reciprocal index is the best measure of the biodiversity of an area.', ['it combines richness and evenness in one number that allows comparison between sites and over time', 'it is easy to calculate from sample counts'], ['it does not measure genetic or ecosystem diversity', 'it depends on sampling method and on correct identification of species'], 'It is a useful, comparable measure of species diversity, but must be supplemented by measures of genetic and ecosystem diversity.')],
  extended=[('Describe the three levels of biodiversity and explain how species diversity can be measured and compared.', 'Ecosystem, species, genetic diversity with examples; richness and evenness; sampling (quadrats, nets); identification; Simpson’s reciprocal D = N(N − 1)/Σn(n − 1); higher D = more diverse; comparison between sites/times; limitations – sampling effort, identification.', 7)],
  )

SIMP_SITES = [('a mangrove swamp in Malaysia', ['mudskippers', 'fiddler crabs', 'mangrove snails', 'barnacles', 'polychaete worms', 'shrimps']),
              ('a meadow in the Swiss Alps', ['meadow buttercup', 'red clover', 'yarrow', 'oxeye daisy', 'ribwort plantain', 'crested dog’s-tail']),
              ('a rocky shore in Cape Town', ['limpets', 'periwinkles', 'barnacles', 'mussels', 'sea anemones', 'whelks']),
              ('leaf litter in a Costa Rican forest', ['ants', 'springtails', 'mites', 'beetles', 'woodlice', 'millipedes']),
              ('a stream in Scotland', ['mayfly nymphs', 'caddisfly larvae', 'freshwater shrimps', 'stonefly nymphs', 'water snails', 'flatworms']),
              ('a coral reef in the Red Sea', ['parrotfish', 'damselfish', 'butterflyfish', 'wrasse', 'surgeonfish', 'groupers'])]


@R.add('ch06-st1', 'C3', (1, 5), 'numerical')
def simpson_calc(rng, slot):
    site, spp = pick(rng, SIMP_SITES)
    k = 4 if slot.d <= 2 else 5 if slot.d == 3 else 6
    ns = [rng.randint(2, 40) for _ in range(k)]
    D = simpson(ns)
    data = ', '.join(f'{s} {n}' for s, n in zip(spp, ns))
    N = sum(ns)
    den = sum(n * (n - 1) for n in ns)
    stem = f'A sample from {site} contained: {data}. Calculate Simpson’s reciprocal index of diversity, D = N(N − 1)/Σn(n − 1).'
    key = f'N = {N}; N(N − 1) = {N * (N - 1)} (M1); Σn(n − 1) = {den} (M1); D = {D:.2f} (A1).'
    if slot.d >= 4:
        ns2 = [rng.randint(1, 60) for _ in range(k)]
        D2 = simpson(ns2)
        if not D2:
            return None
        stem += f' A second sample from a disturbed area nearby contained the same species in numbers {", ".join(map(str, ns2))}. Calculate D for this sample and compare the two areas.'
        ans = f'D = {D:.2f} (first) and {D2:.2f} (second); ' + ('the first area is more diverse/even' if D > D2 else 'the second area is more diverse/even')
        key += f' Second D = {D2:.2f} (A1); comparison: same richness so difference due to evenness – higher D = more even/diverse (R1).'
        return num(stem, ans, key, 5)
    return num(stem, f'D = {D:.2f}', key, 3 if slot.d >= 3 else 2)


@R.add('ch06-st1', 'C3', (1, 4), 'mcq')
def simpson_mcq(rng, slot):
    site, spp = pick(rng, SIMP_SITES)
    ns = [rng.randint(3, 25) for _ in range(3)]
    D = simpson(ns)
    N = sum(ns)
    den = sum(n * (n - 1) for n in ns)
    wrong = [f'{den / (N * (N - 1)):.2f}', f'{N * N / sum(n * n for n in ns) + 0.37:.2f}', f'{D * 2:.2f}', f'{D - 1:.2f}', f'{N / 3:.2f}']
    stem = f'A sample from {site} contained {ns[0]} {spp[0]}, {ns[1]} {spp[1]} and {ns[2]} {spp[2]}. What is Simpson’s reciprocal index, D = N(N − 1)/Σn(n − 1)?'
    return nmcq(rng, stem, f'{D:.2f}', wrong, f'N = {N}; N(N − 1) = {N * (N - 1)}; Σn(n − 1) = {den}; D = {D:.2f}.')


def _simpson_dq(rng, slot):
    site, spp = pick(rng, SIMP_SITES)
    k = 5
    a = [rng.randint(5, 30) for _ in range(k)]
    b = [rng.randint(1, 8) for _ in range(k)]
    b[rng.randrange(k)] = rng.randint(50, 90)
    Da, Db = simpson(a), simpson(b)
    if not Da or not Db:
        return None
    rows = [(s, x, y) for s, x, y in zip(spp, a, b)]
    intro = (f'Students sampled two areas of {site}: area A (undisturbed) and area B (affected by pollution). The number of individuals of each species found is shown.\n\n'
             + table(['Species', 'Area A', 'Area B'], rows))
    Na, Nb = sum(a), sum(b)
    dom = spp[b.index(max(b))]
    parts = [
        ('State the species richness of each area.', f'{k} species in each', f'{k} in each (A1).', 1),
        ('Calculate Simpson’s reciprocal index for area A.', f'{Da:.2f}', f'N = {Na}, N(N − 1) = {Na * (Na - 1)}, Σn(n − 1) = {sum(n * (n - 1) for n in a)} (M1); D = {Da:.2f} (A1).', 2),
        ('Calculate Simpson’s reciprocal index for area B.', f'{Db:.2f}', f'N = {Nb}, N(N − 1) = {Nb * (Nb - 1)}, Σn(n − 1) = {sum(n * (n - 1) for n in b)} (M1); D = {Db:.2f} (A1).', 2),
        ('Compare the diversity of the two areas and explain the difference using the data.', f'Area A is more diverse (D {Da:.2f} vs {Db:.2f}); richness is the same, but area B is dominated by {dom}, so its evenness is low.', 'Correct comparison (A1); same richness, so difference due to evenness (R1); identifies dominant species (A1).', 3),
        ('Suggest a reason for the dominance of one species in area B.', f'{dom} may be tolerant of the pollutant and benefit from reduced competition, while sensitive species decline.', 'Tolerance / reduced competition (A1).', 1),
        ('Outline how the sampling method should be designed so that the two areas can be compared fairly.', 'Same sampling method, effort, number and size of samples, random placement, same season/time; identify species consistently.', 'Two valid points (A1 A1).', 2),
        ('State one limitation of Simpson’s index as a measure of biodiversity.', 'It does not measure genetic or ecosystem diversity / sensitive to sample size / requires accurate identification.', 'Any one (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch06-st1', _simpson_dq)

S('ch06-st2',
  terms=[('mass extinction', 'a geologically short period in which a large proportion (over about 75 %) of species become extinct'),
         ('anthropogenic', 'caused by human activity'),
         ('habitat fragmentation', 'the division of a continuous habitat into smaller, isolated patches by human activities such as roads and farmland'),
         ('invasive alien species', 'a species introduced by humans outside its natural range that spreads and harms native species or ecosystems'),
         ('overexploitation', 'harvesting a species faster than its population can recover, e.g. by overfishing or hunting'),
         ('background extinction rate', 'the normal rate at which species become extinct in the absence of mass extinction events')],
  facts=[('How many mass extinction events are recognised in the fossil record?', 'five', ['two', 'ten', 'twenty'], 'Ordovician, Devonian, Permian, Triassic and Cretaceous.'),
         ('What caused the end-Cretaceous mass extinction about 66 million years ago?', 'an asteroid impact, with volcanic activity', ['human hunting', 'climate cooling caused by farming', 'an ice age caused by plants'], 'The Chicxulub impact is the main cause.'),
         ('Which is the largest current cause of biodiversity loss on land?', 'habitat destruction and land-use change', ['volcanic eruptions', 'meteorite impacts', 'natural background extinction'], 'IPBES ranks land/sea-use change first.'),
         ('Which species was driven to extinction in 1914 mainly by overhunting?', 'the passenger pigeon (Ectopistes migratorius)', ['the dodo', 'the giant panda', 'the cheetah'], 'Once billions strong, the last died in Cincinnati Zoo.'),
         ('Which human activity was the main cause of the extinction of the moa in New Zealand?', 'hunting by early Polynesian settlers', ['climate change after the last ice age', 'disease from European cattle', 'competition with rats'], 'All nine moa species disappeared within about 200 years of human arrival.')],
  mc2=[('Why is the current biodiversity crisis sometimes called the “sixth mass extinction”?', 'Extinction rates are estimated to be tens to hundreds of times the background rate, comparable with past mass extinctions.', ['Exactly five species have become extinct.', 'Five mass extinctions were caused by humans.', 'It was caused by an asteroid.'], 'Rates far exceed background levels.'),
       ('Why does habitat fragmentation reduce biodiversity even if the total area remains large?', 'Small isolated patches support smaller populations, which are more vulnerable and have less gene flow.', ['Fragments contain more resources.', 'Fragmentation increases genetic diversity.', 'Edges are better habitats for all species.'], 'Edge effects and isolation harm many species.'),
       ('Why are island species especially vulnerable to invasive predators?', 'They often evolved without such predators and lack defensive behaviours.', ['Island species are larger.', 'Islands have more predators naturally.', 'Island species reproduce rapidly.'], 'E.g. ground-nesting birds and introduced rats.')],
  mc3=[('A WWF Living Planet Index report found an average decline of 69 % in monitored vertebrate populations between 1970 and 2018. If a population had 5000 individuals in 1970, about how many would remain after such a decline?', '1550', ['3450', '3100', '690'], '5000 × (1 − 0.69) = 1550.'),
       ('A rainforest in Borneo was cleared for oil palm. Orang-utan numbers fell from 2400 to 900. What is the percentage decrease?', '62.5 %', ['37.5 %', '166.7 %', '26.7 %'], '(2400 − 900)/2400 × 100 = 62.5 %.')],
  why=[('Explain how human activities are causing a biodiversity crisis.', 'Habitat destruction and fragmentation (deforestation, agriculture, urbanisation); overexploitation (overfishing, hunting); pollution (pesticides, plastics, eutrophication); invasive alien species; climate change; together they cause extinction rates far above background rates.'),
       ('Explain why evidence for the biodiversity crisis must come from reliable surveys.', 'Population and species trends must be measured over time by repeatable methods (e.g. bird counts, camera traps, Living Planet Index); data from experts and citizen scientists must be verified; without reliable baselines declines cannot be quantified or compared.'),
       ('Explain the difference between the causes of past mass extinctions and the current crisis.', 'Past mass extinctions were caused by natural events such as asteroid impacts, massive volcanism and climate change; the current crisis is anthropogenic, caused by one species altering habitats, climate and ecosystems worldwide.')],
  contrast=[('background extinction', 'mass extinction', 'Background extinction is the continuous low rate of species loss; mass extinction is a geologically brief event in which a large proportion of species disappear, far exceeding background rates.')],
  misc=[('Extinctions only happened in the distant past, before humans.', 'Many species have gone extinct due to humans, e.g. the moa, dodo and passenger pigeon, and current rates are far above background levels.'),
        ('Planting large monoculture plantations restores biodiversity lost by deforestation.', 'Monocultures such as oil palm support far fewer species than natural forest; they replace, not restore, the original ecosystem.')],
  cases=[('the extinction of the moa (Dinornithiformes) in New Zealand', 'Nine species of large flightless birds were hunted to extinction within about 200 years of Polynesian settlement around 1300 CE.', 'human causes of extinction', 'The birds had evolved without mammalian predators and reproduced slowly, so overhunting quickly eliminated them.'),
         ('deforestation of lowland rainforest in Borneo for oil palm plantations', 'Millions of hectares of forest were converted, reducing habitat for orang-utans, hornbills and many endemic species.', 'habitat destruction as a cause of the biodiversity crisis', 'Replacement of diverse forest by monoculture removes the niches species need, causing population declines and local extinctions.')],
  evaluate=[('Habitat destruction is a greater threat to biodiversity than climate change.', ['land-use change is currently the largest driver of species loss', 'habitat loss directly removes populations and their resources'], ['climate change is accelerating and may overtake habitat loss this century', 'climate change interacts with other threats, e.g. coral bleaching'], 'Habitat destruction is the main current driver, but climate change is a growing threat and the two interact; both must be addressed.')],
  extended=[('Discuss the evidence that the Earth is experiencing a sixth mass extinction and outline its causes.', 'Five past mass extinctions (Permian, K–Pg etc.) with natural causes; current extinction rate estimated 100–1000 × background; Living Planet Index declines (~69–73 %); IUCN Red List; causes: habitat loss (oil palm in Borneo), overexploitation (moa, passenger pigeon, overfishing), invasive species, pollution, climate change; evaluation: data uncertainty, many species undescribed.', 8)],
  )

pct_items(R, 'ch06-st2', [
    ('The number of breeding pairs of a seabird on an island fell from {a} to {b} after rats were introduced.', 'pairs', 800, 4000, -0.8, -0.3, 0, 'invasive predators (rats) eat eggs and chicks of ground-nesting birds that have no defences.'),
    ('The area of mangrove forest in a coastal region decreased from {a} km² to {b} km² over 20 years.', 'km²', 150, 900, -0.6, -0.15, 0, 'clearing for shrimp farms and coastal development destroys the habitat.'),
    ('The estimated population of a large catfish in the Mekong River changed from {a} to {b} over a decade of intensive fishing.', 'individuals', 1500, 9000, -0.85, -0.4, 0, 'overexploitation removes adults faster than the population can reproduce.'),
    ('The number of insect species recorded at a monitoring site in Germany changed from {a} to {b} between 1990 and 2016.', 'species', 300, 700, -0.5, -0.2, 0, 'agricultural intensification, pesticide use and habitat loss reduce insect diversity.'),
    ('Live coral cover on a reef changed from {a} % to {b} % after a marine heatwave.', '%', 30, 60, -0.7, -0.3, 1, 'high temperatures cause coral bleaching as corals expel their algae and die.'),
])

S('ch06-st3',
  terms=[('in situ conservation', 'conservation of species in their natural habitats, for example by establishing protected areas or nature reserves'),
         ('ex situ conservation', 'conservation of species outside their natural habitats, such as in zoos, botanic gardens or seed banks'),
         ('rewilding', 'restoring an ecosystem by reintroducing missing species (e.g. top predators) and allowing natural processes to resume'),
         ('EDGE species', 'a species that is both Evolutionarily Distinct and Globally Endangered, prioritised for conservation by the EDGE of Existence programme'),
         ('seed bank', 'a facility that stores seeds under cold, dry conditions to conserve plant genetic diversity, e.g. the Svalbard Global Seed Vault')],
  facts=[('Which is an example of ex situ conservation?', 'storing seeds in the Millennium Seed Bank at Kew', ['creating a national park', 'removing invasive species from an island', 'protecting a coral reef'], 'Ex situ = outside natural habitat.'),
         ('What does the EDGE of Existence programme prioritise?', 'species that are evolutionarily distinct and globally endangered', ['species that are most attractive to tourists', 'species that are economically valuable', 'species with the largest populations'], 'Such species represent large amounts of unique evolutionary history.'),
         ('Which species is an example of an EDGE species?', 'the aye-aye (Daubentonia madagascariensis)', ['the house sparrow', 'the red fox', 'the brown rat'], 'Aye-ayes are the only living members of their family and are endangered.'),
         ('Reintroducing grey wolves into Yellowstone National Park in 1995 is an example of', 'rewilding', ['ex situ conservation', 'selective breeding', 'habitat fragmentation'], 'Restoring a top predator restored trophic cascades.')],
  mc2=[('Why is in situ conservation generally preferred to ex situ conservation?', 'Species remain in their natural ecosystem, maintaining interactions and natural selection.', ['It is always cheaper.', 'It removes all threats.', 'It allows selective breeding.'], 'Whole ecosystems are protected.'),
       ('Why might conservationists prioritise evolutionarily distinct species?', 'Their loss would remove a large amount of unique evolutionary history.', ['They have the largest populations.', 'They are always keystone species.', 'They are easy to breed in zoos.'], 'Phylogenetic diversity is irreplaceable.'),
       ('What is a limitation of seed banks?', 'Stored seeds do not evolve in response to environmental change and some seeds cannot be dried.', ['They conserve no genetic diversity.', 'Seeds cannot be stored for more than a year.', 'They are a form of in situ conservation.'], 'Recalcitrant seeds (e.g. many tropical trees) cannot be banked.')],
  mc3=[('A critically endangered frog is threatened by chytrid fungus in its rainforest habitat. Which strategy combines ex situ and in situ approaches?', 'Captive breeding in a disease-free facility followed by reintroduction once the habitat is managed.', ['Creating a national park only.', 'Storing frog seeds in a bank.', 'Removing all frogs from the wild permanently.'], 'Combination protects the population while the threat is addressed.'),
       ('Species X (ED = 20, Critically Endangered, GE = 4) and species Y (ED = 60, Vulnerable, GE = 2). Using EDGE = ln(1 + ED) + GE × ln 2, which has the higher EDGE score?', 'X', ['Y', 'They are equal', 'Cannot be determined'], 'X: ln21 + 4ln2 = 3.04 + 2.77 = 5.82; Y: ln61 + 2ln2 = 4.11 + 1.39 = 5.50.')],
  why=[('Explain the advantages and disadvantages of ex situ conservation.', 'Advantages: protection from immediate threats, captive breeding increases numbers, genetic management, research and education, seed banks store genetic diversity cheaply. Disadvantages: small populations lose genetic diversity, animals may lose natural behaviours, expensive, does not address habitat loss, reintroduction may fail.'),
       ('Explain why rewilding can restore biodiversity in an ecosystem.', 'Reintroduced keystone species such as wolves or beavers restore interactions (e.g. predation, habitat engineering) that regulate other populations; this creates trophic cascades, more varied habitats and allows natural processes to increase species diversity.'),
       ('Explain why conservation resources must be prioritised.', 'Funding and effort are limited while many species are threatened; prioritising by criteria such as evolutionary distinctiveness, threat level, keystone role or feasibility gives the greatest conservation benefit.')],
  contrast=[('in situ conservation', 'ex situ conservation', 'In situ conservation protects species within their natural habitats (e.g. reserves); ex situ conservation maintains them outside their habitats (zoos, botanic gardens, seed banks).')],
  misc=[('Zoos alone can save endangered species from extinction.', 'Zoos can maintain populations, but unless habitats are protected and threats removed, species cannot be returned to the wild; in situ conservation is essential.'),
        ('Conservation should concentrate only on large, charismatic mammals.', 'Priority should be based on criteria such as threat, evolutionary distinctiveness and ecological role; many invertebrates, plants and amphibians are vital to ecosystems.')],
  cases=[('the reintroduction of grey wolves to Yellowstone National Park in 1995', 'Wolves reduced and changed the behaviour of elk, allowing willows and aspens to regrow along rivers, which benefited beavers and songbirds.', 'rewilding', 'Restoring a top predator triggered a trophic cascade that increased biodiversity.'),
         ('the Svalbard Global Seed Vault in Norway', 'The vault stores over a million seed samples of crop varieties at −18 °C inside a mountain.', 'ex situ conservation', 'It preserves genetic diversity of crops as insurance against loss in the field, though stored seeds do not evolve.'),
         ('the EDGE of Existence programme’s work on the Chinese giant salamander', 'The salamander, among the most evolutionarily distinct amphibians, is critically endangered by overharvesting for food.', 'prioritisation of species for conservation', 'High ED and GE scores focus funding on a species whose loss would remove a unique lineage.')],
  evaluate=[('Ex situ conservation is a waste of resources that should be spent on protecting habitats.', ['without protected habitats, captive species cannot be reintroduced', 'ex situ programmes are expensive per species'], ['some species (e.g. California condor, Przewalski’s horse) survived only because of captive breeding', 'seed banks are cheap insurance for genetic diversity'], 'Both approaches are needed: habitat protection is the priority, but ex situ conservation is a vital safety net for critically endangered species.')],
  extended=[('Evaluate in situ and ex situ approaches to conserving biodiversity, with reference to named examples.', 'In situ: national parks, reserves, marine protected areas, rewilding (Yellowstone wolves), removal of invasive species; maintains interactions, large populations, evolution continues. Ex situ: zoos, captive breeding (condor), botanic gardens, seed banks (Svalbard); protects from immediate threat; loss of diversity/behaviour, cost. EDGE prioritisation. Conclusion: complementary.', 8)],
  )

IUCN = [('Least Concern', 0), ('Near Threatened', 1), ('Vulnerable', 2), ('Endangered', 3), ('Critically Endangered', 4)]


@R.add('ch06-st3', 'C3', (2, 5), 'numerical')
def edge_score(rng, slot):
    sp = pick(rng, ['the aye-aye', 'the pangolin', 'the Chinese giant salamander', 'the tuatara', 'the slender loris', 'the pygmy hippopotamus', 'the solenodon', 'the long-beaked echidna', 'the kakapo'])
    ed = round(rng.uniform(5, 80), 1)
    cat, ge = pick(rng, IUCN[1:])
    E = math.log(1 + ed) + ge * math.log(2)
    stem = (f'The EDGE score of a species is calculated as EDGE = ln(1 + ED) + GE × ln 2, where ED is the evolutionary distinctiveness (in millions of years) and GE is the IUCN threat category '
            f'(Least Concern 0, Near Threatened 1, Vulnerable 2, Endangered 3, Critically Endangered 4). {sp[0].upper() + sp[1:]} has ED = {ed} and is listed as {cat}. Calculate its EDGE score.')
    key = f'ln(1 + {ed}) = {math.log(1 + ed):.2f} (M1); {ge} × 0.693 = {ge * math.log(2):.2f}; EDGE = {E:.2f} (A1).'
    if slot.d >= 4:
        cat2, ge2 = IUCN[min(4, ge + 1)]
        E2 = math.log(1 + ed) + ge2 * math.log(2)
        stem += f' Calculate the score if it were moved to {cat2}, and explain why EDGE gives priority to evolutionarily distinct species.'
        return num(stem, f'{E:.2f}; {E2:.2f} if {cat2}', key + f' New score {E2:.2f} (A1); loss of a distinct species removes a large share of unique evolutionary history / few close relatives (R1).', 4)
    return num(stem, f'{E:.2f}', key, 2)


# =============================================================================================
# ch07 B1.1 Carbohydrates and lipids
# =============================================================================================
S('ch07-st1',
  terms=[('condensation reaction', 'a reaction in which two molecules are joined by a covalent bond with the release of a molecule of water'),
         ('hydrolysis', 'a reaction in which a covalent bond between two monomers is broken by the addition of a molecule of water'),
         ('monomer', 'a small molecule that can be joined to others of the same type to form a polymer'),
         ('polymer', 'a large molecule made of many repeating monomer units joined by covalent bonds'),
         ('covalent bond', 'a strong chemical bond formed when two atoms share a pair of electrons'),
         ('macromolecule', 'a very large molecule such as a polysaccharide, polypeptide or nucleic acid')],
  facts=[('Why can carbon form a great diversity of compounds?', 'each carbon atom can form four covalent bonds, including with other carbon atoms', ['carbon forms only ionic bonds', 'carbon has a single bonding electron', 'carbon cannot form chains'], 'Chains, branches and rings with single or double bonds are possible.'),
         ('What is released when two glucose molecules join to form maltose?', 'one molecule of water', ['one molecule of carbon dioxide', 'two molecules of water', 'one molecule of oxygen'], 'Condensation releases H₂O.'),
         ('Which type of reaction occurs during digestion of starch in the gut?', 'hydrolysis', ['condensation', 'oxidation of glucose', 'polymerisation'], 'Amylase hydrolyses glycosidic bonds using water.'),
         ('Which bond links monosaccharides in a disaccharide?', 'glycosidic bond', ['peptide bond', 'ester bond', 'phosphodiester bond'], 'Formed by condensation between –OH groups.'),
         ('Which reaction type builds polypeptides from amino acids?', 'condensation', ['hydrolysis', 'denaturation', 'oxidation'], 'Each peptide bond releases one water molecule.')],
  mc2=[('Why is energy needed to build polymers by condensation in cells?', 'Forming covalent bonds between monomers is an anabolic process requiring energy, often from ATP.', ['Water is consumed in condensation.', 'Condensation releases large amounts of energy.', 'Polymers are less stable than monomers.'], 'Anabolism uses energy; hydrolysis (catabolism) releases it.'),
       ('Which statement correctly compares condensation and hydrolysis?', 'Condensation releases water and builds polymers; hydrolysis uses water and breaks them down.', ['Both release water.', 'Hydrolysis builds polymers.', 'Condensation uses water.'], 'They are reverse reactions.'),
       ('Which molecule is NOT a polymer?', 'glucose', ['glycogen', 'cellulose', 'DNA'], 'Glucose is a monosaccharide monomer.')],
  mc3=[('How many water molecules are released when 12 glucose molecules are joined into an unbranched chain?', '11', ['12', '13', '24'], 'n − 1 bonds for a chain of n monomers.'),
       ('A polysaccharide of 500 glucose units is completely hydrolysed. How many water molecules are used?', '499', ['500', '501', '1000'], 'One water per glycosidic bond broken.')],
  why=[('Explain how the bonding properties of carbon allow the diversity of carbon compounds in living organisms.', 'Carbon has four outer electrons and forms four covalent bonds; it bonds to other carbons forming chains, branches and rings, with single or double bonds, and to H, O, N, S, P; so an almost unlimited variety of stable molecules is possible.'),
       ('Explain the relationship between condensation and hydrolysis reactions in metabolism.', 'Condensation (anabolism) joins monomers into polymers with release of water, e.g. glucose → glycogen for storage; hydrolysis (catabolism) breaks polymers into monomers using water, e.g. digestion of starch; they are reverse reactions catalysed by different enzymes.')],
  contrast=[('condensation', 'hydrolysis', 'Condensation joins two molecules by a covalent bond and releases water (building polymers); hydrolysis breaks a covalent bond by adding water (breaking polymers into monomers).'),
            ('anabolism', 'catabolism', 'Anabolism builds larger molecules from smaller ones (e.g. by condensation), requiring energy; catabolism breaks larger molecules into smaller ones (e.g. by hydrolysis), often releasing energy.')],
  misc=[('Hydrolysis releases water as large molecules are broken down.', 'Hydrolysis uses (consumes) water to break bonds; it is condensation that releases water.'),
        ('Polymers are made by joining monomers with hydrogen bonds.', 'Monomers are joined by covalent bonds formed by condensation reactions.')],
  cases=[('the digestion of starch in bread', 'Salivary and pancreatic amylase hydrolyse starch into maltose, which maltase then hydrolyses to glucose.', 'hydrolysis reactions', 'Water is added to break each glycosidic bond, converting the polymer into absorbable monomers.'),
         ('the synthesis of glycogen in liver cells after a meal', 'Glucose units are linked by condensation into branched glycogen molecules for storage.', 'condensation reactions', 'Each new glycosidic bond formed releases a molecule of water, building a polymer from monomers.')],
  evaluate=[('Carbon is the only element on which life could be based.', ['carbon forms four stable covalent bonds and long chains, giving vast molecular diversity', 'carbon compounds are stable but reactive enough at Earth temperatures'], ['silicon can also form four bonds and chains', 'we have only one example of life, so other chemistries cannot be ruled out'], 'Carbon is far better suited than alternatives such as silicon (whose compounds are less stable and less diverse in water), but with only one known example of life the claim cannot be proven.')],
  extended=[('Explain how condensation and hydrolysis reactions are involved in building and breaking down carbohydrates, proteins and lipids.', 'Condensation: glucose → disaccharide/polysaccharide (glycosidic bonds); amino acids → polypeptides (peptide bonds); glycerol + 3 fatty acids → triglyceride (ester bonds); water released; energy required. Hydrolysis: reverse, water added, digestive enzymes (amylase, protease, lipase), releases monomers.', 7)],
  )


@R.add('ch07-st1', 'C3', (1, 5), 'numerical')
def polymer_calc(rng, slot):
    n = pick(rng, [3, 4, 5, 6, 8, 10, 12, 20, 50, 100, 250])
    f = rng.randrange(3)
    if f == 0 or slot.d <= 1:
        what = pick(rng, ['glucose molecules are joined into an unbranched chain of amylose', 'amino acids are joined into a single polypeptide', 'nucleotides are joined into a single strand of RNA', 'β-glucose molecules are joined into a cellulose chain'])
        return num(f'{n} {what}. How many water molecules are released?', f'{n - 1}', f'One water per bond formed; {n} monomers in a chain form {n - 1} bonds (A1).', 1)
    C, H, O = 6 * n, 12 * n - 2 * (n - 1), 6 * n - (n - 1)
    mr = 180 * n - 18 * (n - 1)
    if f == 1:
        stem = f'Glucose has the formula C₆H₁₂O₆ (Mr = 180). Deduce the molecular formula and relative molecular mass of an unbranched chain of {n} glucose units.'
        return num(stem, f'C{C}H{H}O{O}; Mr = {mr}', f'{n} × C₆H₁₂O₆ minus {n - 1} H₂O (M1); C{C}H{H}O{O} (A1); Mr = {n} × 180 − {n - 1} × 18 = {mr} (A1).', 3)
    mass = pick(rng, [1.0, 2.0, 5.0, 10.0])
    stem = (f'A {mass:g} g sample of a polysaccharide made of {n} glucose units (Mr = {mr}) is completely hydrolysed to glucose. Calculate the mass of glucose produced and explain why it is greater than {mass:g} g.')
    g = mass * 180 * n / mr
    return num(stem, f'{g:.2f} g; water is added during hydrolysis', f'Moles of polymer = {mass:g}/{mr} (M1); glucose mass = moles × {n} × 180 = {g:.2f} g (A1); extra mass comes from the {n - 1} water molecules added per polymer (R1).', 3)


S('ch07-st2',
  terms=[('monosaccharide', 'a single sugar unit such as glucose, fructose or galactose, the monomer of carbohydrates'),
         ('disaccharide', 'a sugar formed from two monosaccharides joined by a glycosidic bond, e.g. maltose, sucrose or lactose'),
         ('polysaccharide', 'a carbohydrate polymer made of many monosaccharides joined by glycosidic bonds, e.g. starch, glycogen and cellulose'),
         ('amylopectin', 'the branched form of starch, with α-1,4 glycosidic bonds in chains and α-1,6 bonds at branch points'),
         ('cellulose', 'an unbranched polysaccharide of β-glucose in which alternate units are inverted, forming straight chains that bundle into microfibrils'),
         ('α-glucose', 'the form of glucose in which the –OH on carbon 1 is below the plane of the ring')],
  facts=[('Which polysaccharide forms plant cell walls?', 'cellulose', ['starch', 'glycogen', 'chitin'], 'Cellulose microfibrils give tensile strength.'),
         ('Which glycosidic bonds form the branches in glycogen?', 'α-1,6', ['α-1,4', 'β-1,4', 'β-1,6'], 'Chains are α-1,4; branches α-1,6.'),
         ('Which two monosaccharides form sucrose?', 'glucose and fructose', ['glucose and galactose', 'two glucose molecules', 'fructose and galactose'], 'Lactose = glucose + galactose; maltose = two glucose.'),
         ('Which is the storage polysaccharide in animals?', 'glycogen', ['starch', 'cellulose', 'sucrose'], 'Stored in liver and muscle.'),
         ('Which form of glucose makes up cellulose?', 'β-glucose', ['α-glucose', 'fructose', 'galactose'], 'β-1,4 bonds with alternate units inverted.')],
  mc2=[('Why is glucose not stored in cells as free glucose?', 'It is soluble and would lower the water potential, causing osmotic water uptake.', ['It is insoluble.', 'It cannot be respired.', 'It is too large to stay in cells.'], 'Polysaccharides are insoluble and osmotically inactive.'),
       ('Why is glycogen more highly branched than amylose?', 'Many branch ends allow rapid hydrolysis to release glucose when energy is needed.', ['Branches make glycogen soluble in water.', 'Branches allow hydrogen bonds between chains.', 'Branches make it a structural molecule.'], 'Animals need rapid glucose mobilisation.'),
       ('Which explains the high tensile strength of cellulose?', 'Straight chains lie parallel and are held by many hydrogen bonds into microfibrils.', ['Its chains are coiled into helices.', 'It is highly branched.', 'It is made of α-glucose.'], 'Alternate inverted β-glucose units allow straight chains.')],
  mc3=[('Humans cannot digest cellulose although they digest starch. Which explanation is correct?', 'Human enzymes cannot hydrolyse β-1,4 glycosidic bonds.', ['Cellulose is not made of glucose.', 'Cellulose is soluble.', 'Human enzymes cannot hydrolyse α-1,4 bonds.'], 'Enzymes are specific to the bond configuration.'),
       ('A food sample gives a blue-black colour with iodine and no change with Benedict’s reagent. Which conclusion is correct?', 'Starch is present but no reducing sugar.', ['Glucose is present.', 'Protein is present.', 'Neither starch nor sugar is present.'], 'Iodine detects starch; Benedict’s detects reducing sugars.')],
  why=[('Explain how the structure of starch makes it a suitable energy store in plants.', 'Starch is a large, insoluble polymer so it does not affect water potential; amylose is compact (helical) so much glucose is stored in small space; amylopectin is branched for faster hydrolysis; glucose is easily released by hydrolysis for respiration.'),
       ('Explain how the structure of cellulose is related to its function in plant cell walls.', 'β-glucose units with alternate units inverted form straight unbranched chains; parallel chains are held together by many hydrogen bonds forming microfibrils; microfibrils have high tensile strength, so walls resist turgor pressure and give support.'),
       ('Explain why glycogen is suited to energy storage in animals.', 'It is insoluble and compact; it is very highly branched with many ends, so enzymes can hydrolyse it rapidly to supply glucose for the high metabolic demands of animals.')],
  contrast=[('α-glucose', 'β-glucose', 'In α-glucose the –OH on carbon 1 is below the ring; in β-glucose it is above; α-glucose polymerises into starch and glycogen, β-glucose into cellulose.'),
            ('amylose', 'amylopectin', 'Amylose is unbranched with α-1,4 bonds and coils into a helix; amylopectin is branched with α-1,4 chains and α-1,6 branch points.'),
            ('glycogen', 'starch', 'Glycogen is the animal storage polysaccharide and is more highly branched; starch (amylose + amylopectin) is the plant storage polysaccharide and is less branched.')],
  misc=[('Cellulose is a storage carbohydrate in plants.', 'Cellulose is structural (cell walls); starch is the storage carbohydrate of plants.'),
        ('Starch and cellulose are both made of β-glucose.', 'Starch is made of α-glucose; cellulose is made of β-glucose.'),
        ('Glycogen is stored in plants and starch in animals.', 'Glycogen is the storage polysaccharide in animals and fungi; starch is the storage polysaccharide in plants.')],
  cases=[('cotton fibres used in textiles', 'Cotton fibres are about 90 % cellulose and are very strong and absorbent.', 'the structure–function relationship of cellulose', 'Parallel β-glucose chains hydrogen-bonded into microfibrils give high tensile strength; free –OH groups make the fibres absorbent.'),
         ('muscle glycogen stores in endurance athletes', 'Athletes “carbo-load” to raise muscle glycogen; during races glycogen is rapidly hydrolysed for respiration.', 'glycogen as an energy store', 'Highly branched glycogen provides many ends for rapid release of glucose when demand is high.')],
  apply=[('Draw the ring structures of α-glucose and β-glucose and describe the difference your drawings should show.', 'Hexagonal rings with five carbons and one oxygen, carbon 6 above the ring; in α-glucose the OH on C1 is below the ring, in β-glucose above.', 3),
         ('Describe how you would test a sample of fruit juice for reducing sugar and for starch, giving the positive results.', 'Benedict’s reagent, heat in a water bath: blue → green/yellow/orange/brick-red precipitate shows reducing sugar; iodine solution: yellow-brown → blue-black shows starch.', 3)],
  evaluate=[('Starch is a better energy store than glycogen.', ['amylose is very compact due to helical coiling, storing much glucose in little space', 'plants have low metabolic rates, so slow release is sufficient'], ['glycogen’s extensive branching releases glucose faster, suiting active animals', 'each is suited to the organism’s needs rather than one being better'], 'Neither is better in absolute terms; each is adapted to the metabolic demands of the organisms that use it.')],
  extended=[('Compare the structure and functions of starch, glycogen and cellulose.', 'Monomers: α-glucose (starch, glycogen) vs β-glucose (cellulose). Bonds: α-1,4 and α-1,6 vs β-1,4. Branching: amylose none/helix, amylopectin some, glycogen highly branched, cellulose straight chains with H bonds → microfibrils. Functions: energy storage in plants/animals, structural support in cell walls. Insoluble – no osmotic effect.', 8)],
  )


def _benedict_dq(rng, slot):
    conc = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    k = rng.uniform(1.4, 1.9)
    base = rng.uniform(8, 14)
    f = lambda c: base + (95 - base) * (1 - math.exp(-k * c))  # noqa: E731
    trans = [round(f(c), 0) for c in conc]
    unk_c = rng.uniform(0.25, 0.85)
    unk_t = round(f(unk_c), 0)
    est = None
    for (x1, y1), (x2, y2) in zip(zip(conc, trans), zip(conc[1:], trans[1:])):
        if y1 <= unk_t <= y2 and y1 != y2:
            est = x1 + (unk_t - y1) * (x2 - x1) / (y2 - y1)
    if est is None:
        return None
    juice = pick(rng, ['apple juice', 'orange juice', 'a sports drink', 'coconut water', 'honey solution diluted 1:20'])
    intro = (f'Glucose solutions of known concentration were heated with excess Benedict’s reagent for 5 minutes. The brick-red precipitate was filtered off and the percentage transmission of red light through the remaining blue filtrate was measured with a colorimeter.\n\n'
             + table(['Glucose concentration / mol dm⁻³', 'Transmission / %'], [(f'{c:.1f}', f'{t:.0f}') for c, t in zip(conc, trans)])
             + f'\n\nA sample of {juice}, treated the same way, gave {unk_t:.0f} % transmission.')
    pc = pct_change(trans[1], trans[-1])
    parts = [
        ('Describe the relationship between glucose concentration and transmission.', 'As glucose concentration increases, transmission increases; the increase is not linear and becomes smaller at higher concentrations.', 'Positive relationship (A1); non-linear / levels off (A1).', 2),
        (f'Estimate the glucose concentration of the sample ({juice}) by interpolation.', f'about {est:.2f} mol dm⁻³', f'Interpolation between the bracketing standards (M1); ≈ {est:.2f} mol dm⁻³, accept ±0.05 (A1).', 2),
        ('Calculate the percentage change in transmission between 0.2 and 1.0 mol dm⁻³.', f'{signed(pc)} %', f'({trans[-1]:.0f} − {trans[1]:.0f})/{trans[1]:.0f} × 100 (M1) = {signed(pc)} % (A1).', 2),
        ('Explain why transmission increases as glucose concentration increases.', 'Glucose reduces blue Cu²⁺ ions to brick-red Cu₂O, which is filtered off; more glucose leaves less Cu²⁺ in the filtrate, so it is paler blue, absorbs less red light and transmits more.', 'Glucose (reducing sugar) reduces Cu²⁺ to Cu₂O (A1); less blue Cu²⁺ remaining so less red light absorbed (R1).', 2),
        ('State two variables that must be controlled.', 'Volume of Benedict’s reagent and sample; temperature and time of heating; same colorimeter filter/wavelength.', 'Any two (A1 A1).', 2),
        ('Suggest why the juice might contain other sugars that this method would not detect.', 'Sucrose is a non-reducing sugar and does not react with Benedict’s reagent unless first hydrolysed with acid.', 'Sucrose non-reducing (A1).', 1),
        ('Outline the advantage of using a colorimeter rather than judging the colour by eye.', 'It gives a quantitative, objective measurement, so results are more precise and comparable.', 'Quantitative/objective (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch07-st2', _benedict_dq)

S('ch07-st3',
  terms=[('glycoprotein', 'a protein with carbohydrate chains attached, often found in the plasma membrane with the carbohydrate facing outwards'),
         ('cell recognition', 'the ability of cells to identify other cells, e.g. as self or non-self, using molecules such as glycoproteins on the cell surface'),
         ('antigen', 'a molecule, often a glycoprotein, that is recognised by the immune system and stimulates an immune response'),
         ('ABO blood group system', 'the classification of human blood by the presence or absence of A and B antigens (glycoproteins) on red blood cells'),
         ('glycocalyx', 'the carbohydrate-rich layer on the outer surface of a cell membrane formed by glycoproteins and glycolipids')],
  facts=[('Which antigens are present on the red blood cells of a person with blood group AB?', 'both A and B antigens', ['neither A nor B antigen', 'A antigen only', 'B antigen only'], 'AB has both glycoprotein modifications.'),
         ('Which blood group is called the “universal donor” for red blood cells in the ABO system?', 'O', ['AB', 'A', 'B'], 'O cells carry neither A nor B antigen.'),
         ('Where are the carbohydrate chains of membrane glycoproteins located?', 'on the outer (extracellular) surface of the membrane', ['inside the hydrophobic core', 'on the cytoplasmic surface', 'within the nucleus'], 'This allows recognition by other cells and antibodies.'),
         ('What is the difference between A and B antigens?', 'a different terminal sugar on the carbohydrate chain', ['completely different proteins', 'the presence of lipids instead of carbohydrates', 'the number of amino acids'], 'A has N-acetylgalactosamine, B has galactose added to the O (H) antigen.')],
  mc2=[('Why does a person with blood group A have anti-B antibodies in the plasma?', 'Their immune system treats B antigen as non-self.', ['B antigen is present on their cells.', 'Antibodies are made against their own A antigen.', 'They have no immune system.'], 'Antibodies are produced against antigens not present on own cells.'),
       ('Why can glycoproteins act as recognition molecules?', 'The carbohydrate chains are very varied and have specific shapes.', ['Glycoproteins are all identical.', 'They contain DNA.', 'They are found inside the nucleus.'], 'Diversity of sugar sequences gives specificity.'),
       ('What happens if group A blood is transfused into a group O recipient?', 'The recipient’s anti-A antibodies cause agglutination of the donor cells.', ['Nothing, because O is universal.', 'The donor cells destroy the recipient’s cells.', 'The blood changes to group O.'], 'O recipients have anti-A and anti-B.')],
  mc3=[('A patient’s red cells agglutinate with anti-B serum but not with anti-A serum. What is the patient’s blood group?', 'B', ['A', 'AB', 'O'], 'Reaction with anti-B only = B antigen only.'),
       ('Which group of red cells could safely be given to a patient with blood group B?', 'O or B', ['A or AB', 'AB only', 'any group'], 'B recipients have anti-A antibodies.')],
  why=[('Explain how glycoproteins are involved in cell recognition.', 'Glycoproteins in the plasma membrane carry carbohydrate chains projecting outwards; the specific sequence and shape of these chains act as markers that are recognised by complementary receptors on other cells or by antibodies, allowing self/non-self recognition and cell–cell adhesion.'),
       ('Explain the basis of the ABO blood group system.', 'Red blood cells carry glycoproteins with a carbohydrate chain (O/H antigen); allele IA adds a sugar making antigen A, IB adds a different sugar making antigen B, i lacks the enzyme; antibodies in plasma react with antigens not present on own cells, causing agglutination in incompatible transfusions.')],
  contrast=[('glycoproteins', 'glycolipids', 'Glycoproteins are proteins with attached carbohydrate chains; glycolipids are lipids with attached carbohydrate chains; both contribute to the glycocalyx and cell recognition.')],
  misc=[('Blood group O has O antigens that are recognised by all antibodies.', 'Group O red cells lack both A and B antigens (they carry only the unmodified H chain), so anti-A and anti-B do not react with them.'),
        ('Glycoproteins are found on the inner surface of the plasma membrane.', 'The carbohydrate parts face outward on the extracellular surface, where they can be recognised.')],
  cases=[('ABO blood typing before transfusion in hospitals', 'Samples are mixed with anti-A and anti-B sera; agglutination shows which antigens are present.', 'cell recognition by glycoproteins', 'Antibodies recognise specific carbohydrate antigens on red cells, so mismatched transfusion leads to agglutination and haemolysis.')],
  evaluate=[('Blood group O donors should always be used in emergencies.', ['O red cells lack A and B antigens, so they are compatible with all ABO recipients', 'it saves time when the recipient’s group is unknown'], ['O plasma contains anti-A and anti-B, so plasma products are not universal', 'O supplies are limited and Rh status must also be considered (O negative)'], 'O negative red cells are appropriate in emergencies, but group-specific blood should be used as soon as the recipient’s group is known.')],
  extended=[('Explain the role of glycoproteins in cell recognition, using the ABO blood group system as an example.', 'Glycoproteins: protein + carbohydrate, extracellular, glycocalyx; diverse sugar chains = markers; ABO: H chain; IA adds N-acetylgalactosamine, IB galactose; O none; antibodies against absent antigens; agglutination; transfusion compatibility; other roles: sperm–egg recognition, immune self/non-self, hormone receptors.', 7)],
  )

ANTIG = {'A': {'A'}, 'B': {'B'}, 'AB': {'A', 'B'}, 'O': set()}


@R.add('ch07-st3', 'C3', (1, 4), 'mcq')
def transfusion_mcq(rng, slot):
    rec = pick(rng, list(ANTIG))
    ok = [d for d in ANTIG if ANTIG[d] <= ANTIG[rec]]
    bad = [d for d in ANTIG if d not in ok]
    if not bad:
        return mcq(rng, f'A patient with blood group {rec} needs a red-cell transfusion. Which statement about ABO compatibility is correct?',
                   'Red cells of any ABO group can be given.', ['Only group AB red cells can be given.', 'Only group O red cells can be given.', 'Group A red cells will be agglutinated.'],
                   'AB has no anti-A or anti-B antibodies.')
    d = pick(rng, ok)
    stem = f'A patient with blood group {rec} needs a red-cell transfusion. Which donor group would be compatible?'
    w = [b for b in bad] + [x + ' only' for x in bad]
    return nmcq(rng, stem, d, w + ['none of the four groups'], f'Group {rec} plasma contains antibodies against ' + (' and '.join(sorted({'A', 'B'} - ANTIG[rec])) or 'neither antigen') + f'; donor {d} cells carry ' + (' and '.join(sorted(ANTIG[d])) or 'neither antigen') + '.')


@R.add('ch07-st3', 'C3', (2, 4), 'numerical')
def typing(rng, slot):
    g = pick(rng, list(ANTIG))
    who = name(rng)
    ra = 'agglutination' if 'A' in ANTIG[g] else 'no agglutination'
    rb = 'agglutination' if 'B' in ANTIG[g] else 'no agglutination'
    stem = f'{who}’s blood sample shows {ra} with anti-A serum and {rb} with anti-B serum. Deduce {who}’s blood group, state which antibodies are in the plasma, and identify which donor groups of red cells could be given.'
    abs_ = sorted({'A', 'B'} - ANTIG[g])
    ok = [d for d in ANTIG if ANTIG[d] <= ANTIG[g]]
    ans = f'Group {g}; plasma antibodies: ' + (', '.join(f'anti-{x}' for x in abs_) or 'none') + f'; compatible donors: {", ".join(ok)}'
    return num(stem, ans, f'Group {g} from agglutination pattern (A1); antibodies against antigens absent from own cells (A1); donors whose cells lack antigens recognised by recipient plasma: {", ".join(ok)} (A1).', 3)


S('ch07-st4',
  terms=[('triglyceride', 'a lipid formed by condensation of one glycerol molecule with three fatty acids, linked by ester bonds'),
         ('phospholipid', 'a lipid with a glycerol bonded to two fatty acids and a phosphate group, giving a hydrophilic head and two hydrophobic tails'),
         ('saturated fatty acid', 'a fatty acid with no carbon–carbon double bonds in its hydrocarbon chain'),
         ('unsaturated fatty acid', 'a fatty acid with one (monounsaturated) or more (polyunsaturated) carbon–carbon double bonds in its hydrocarbon chain'),
         ('cis double bond', 'a double bond in a fatty acid where the hydrogen atoms are on the same side, causing a bend in the chain'),
         ('amphipathic', 'describes a molecule that has both hydrophilic and hydrophobic regions, such as a phospholipid'),
         ('steroid', 'a lipid with a structure of four fused carbon rings, such as cholesterol, oestradiol and testosterone')],
  facts=[('How many water molecules are released when one triglyceride is formed?', 'three', ['one', 'two', 'four'], 'One per ester bond with each fatty acid.'),
         ('Which bond forms between glycerol and a fatty acid?', 'ester bond', ['glycosidic bond', 'peptide bond', 'hydrogen bond'], 'Condensation of –OH and –COOH.'),
         ('Which type of fatty acid is most common in fats that are solid at room temperature?', 'saturated', ['cis-unsaturated', 'polyunsaturated', 'omega-3'], 'Straight chains pack closely.'),
         ('Approximately how much energy does 1 g of lipid release when respired, compared with 1 g of carbohydrate?', 'about twice as much (37 kJ vs 17 kJ)', ['about the same', 'about half', 'about ten times as much'], 'Lipids are more reduced (more C–H bonds).'),
         ('Which hormone is a steroid?', 'testosterone', ['insulin', 'adrenaline', 'glucagon'], 'Steroids have four fused rings.')],
  mc2=[('Why are triglycerides suitable for long-term energy storage in adipose tissue?', 'They release twice as much energy per gram as carbohydrates and are stored without water.', ['They are soluble in water.', 'They are easily transported in plasma.', 'They are made of glucose.'], 'Compact, anhydrous, energy-dense stores.'),
       ('Why do unsaturated fats tend to be liquid at room temperature?', 'Cis double bonds create kinks that prevent close packing of chains.', ['They have higher molecular masses.', 'They contain more hydrogen.', 'They form ester bonds with water.'], 'Weaker intermolecular forces = lower melting point.'),
       ('Why do phospholipids form bilayers in water?', 'The hydrophilic heads face the water and the hydrophobic tails face each other, away from water.', ['The tails are attracted to water.', 'The heads are hydrophobic.', 'Phospholipids are soluble in water.'], 'Amphipathic molecules self-assemble.'),
       ('Why can steroid hormones pass directly through the plasma membrane?', 'They are lipids, so they dissolve in the hydrophobic core of the bilayer.', ['They are carried by channel proteins.', 'They are charged.', 'They are very large polar molecules.'], 'Then they bind intracellular receptors.')],
  mc3=[('An Arctic fox and an emperor penguin both have thick fat layers. Which function of adipose tissue is most important to them in winter?', 'thermal insulation as well as energy storage', ['buoyancy only', 'production of glucose', 'protection from UV light'], 'Fat (blubber) insulates and stores energy.'),
       ('A fatty acid has the formula C₁₇H₃₁COOH. How many C=C double bonds does it contain?', '2', ['0', '1', '3'], 'Saturated C₁₇H₃₅COOH; each double bond removes 2 H: (35 − 31)/2 = 2 (linoleic acid).')],
  why=[('Explain why lipids are more suitable than carbohydrates for long-term energy storage.', 'Lipids release about twice as much energy per gram (37 vs 17 kJ g⁻¹); they are hydrophobic and stored without water, whereas glycogen is stored hydrated; so a much smaller mass is needed; they also provide insulation and protection.'),
       ('Explain how the structure of a phospholipid allows the formation of a membrane.', 'A phospholipid has a hydrophilic phosphate head and two hydrophobic fatty-acid tails (amphipathic); in water the heads face the aqueous surroundings and the tails face inward, forming a bilayer that is a barrier to polar substances.'),
       ('Explain why saturated and unsaturated fatty acids have different melting points.', 'Saturated chains are straight and pack closely with many intermolecular attractions, so more energy is needed to melt them; cis double bonds in unsaturated chains produce kinks, preventing close packing and lowering the melting point.')],
  contrast=[('saturated fatty acids', 'unsaturated fatty acids', 'Saturated fatty acids have only single C–C bonds and straight chains, packing tightly (higher melting point); unsaturated fatty acids have one or more C=C double bonds, cis forms being kinked and having lower melting points.'),
            ('triglycerides', 'phospholipids', 'Triglycerides have three fatty acids on glycerol and are hydrophobic energy stores; phospholipids have two fatty acids and a phosphate group, are amphipathic and form membranes.'),
            ('cis fatty acids', 'trans fatty acids', 'In cis fatty acids the hydrogens are on the same side of the double bond, causing a bend; in trans fatty acids they are on opposite sides, giving a straighter chain that behaves more like a saturated fat.')],
  misc=[('Phospholipids are completely hydrophobic.', 'Phospholipids are amphipathic: a hydrophilic phosphate head and hydrophobic tails.'),
        ('Lipids are only bad for health.', 'Lipids are essential: energy stores, membranes (phospholipids, cholesterol), insulation, hormones (steroids); some are linked to disease in excess.'),
        ('Unsaturated fats contain more hydrogen than saturated fats.', 'Unsaturated fats contain fewer hydrogen atoms because double bonds replace some C–H bonds; saturated means saturated with hydrogen.')],
  cases=[('the blubber of harp seals and whales', 'Blubber can be over 10 cm thick and make up 30–50 % of body mass in some marine mammals.', 'the roles of triglycerides', 'Blubber stores energy for fasting periods and provides thermal insulation in cold water.'),
         ('the camel’s hump', 'The hump stores up to 35 kg of fat, not water.', 'lipids as energy stores', 'Fat is a compact energy store; its oxidation also produces metabolic water.')],
  evaluate=[('Lipids are a better energy store than carbohydrates for all organisms.', ['lipids store about twice as much energy per gram and are stored without water', 'they are ideal for animals that must move or fly, such as migrating birds'], ['carbohydrates can be mobilised and respired faster and can be used anaerobically', 'plants, which do not move, often store starch, and seeds use both'], 'Lipids are better for long-term, compact storage, especially in mobile animals; carbohydrates are better for rapid energy release; organisms use both.')],
  extended=[('Describe the structure of triglycerides and phospholipids and explain how these structures relate to their functions.', 'Triglyceride: glycerol + 3 fatty acids, ester bonds, condensation (3 H₂O), hydrophobic; energy storage (37 kJ/g), insulation, buoyancy. Phospholipid: glycerol + 2 fatty acids + phosphate; amphipathic; bilayer; membranes. Saturated vs unsaturated affects fluidity/melting point. Steroids (cholesterol) in membranes and hormones.', 8)],
  )


@R.add('ch07-st4', 'C3', (1, 5), 'numerical')
def energy_store(rng, slot):
    who = pick(rng, ['A bar-tailed godwit preparing to migrate from Alaska to New Zealand', 'A hibernating brown bear', 'An emperor penguin before the breeding season', 'A marathon runner', 'A ruby-throated hummingbird before crossing the Gulf of Mexico'])
    E = pick(rng, [500, 800, 1200, 2000, 5000, 15000, 50000, 200000])
    fat = E / 37
    gly = E / 17
    stem = f'{who} needs to store {E:,} kJ of energy. Calculate the mass of triglyceride and the mass of glycogen needed, given that they release 37 kJ g⁻¹ and 17 kJ g⁻¹ respectively.'.replace(',', ' ')
    ans = f'triglyceride {sf(fat)} g; glycogen {sf(gly)} g'
    key = f'{E}/37 = {sf(fat)} g (A1); {E}/17 = {sf(gly)} g (A1).'
    if slot.d >= 3:
        wet = gly * 3
        stem += ' Glycogen is stored with about 2 g of water per gram. Calculate the total stored mass for glycogen and explain the advantage of lipid storage for this animal.'
        ans += f'; glycogen + water ≈ {sf(wet)} g; lipid is about {sf(wet / fat)} times lighter, important for mobility'
        key += f' {sf(gly)} × 3 = {sf(wet)} g (A1); lipid stored anhydrous, much less mass to carry (R1).'
        return num(stem, ans, key, 4)
    return num(stem, ans, key, 2)


@R.add('ch07-st4', 'C3', (2, 4), 'numerical')
def fatty_formula(rng, slot):
    c = pick(rng, [11, 13, 15, 17, 19, 21])
    db = rng.randint(0, 4 if c >= 17 else 2)
    h = 2 * c + 1 - 2 * db
    stem = f'A fatty acid has the formula C{c}H{h}COOH. Deduce the number of carbon–carbon double bonds and state whether it is saturated, monounsaturated or polyunsaturated.'
    t = 'saturated' if db == 0 else 'monounsaturated' if db == 1 else 'polyunsaturated'
    return num(stem, f'{db}; {t}', f'Saturated formula C{c}H{2 * c + 1}COOH (M1); ({2 * c + 1} − {h})/2 = {db} double bonds (A1); {t} (A1).', 3)


FA = [('lauric acid', 12, 0, 44.2), ('myristic acid', 14, 0, 54.4), ('palmitic acid', 16, 0, 62.9), ('stearic acid', 18, 0, 69.3),
      ('arachidic acid', 20, 0, 75.5), ('oleic acid', 18, 1, 13.4), ('linoleic acid', 18, 2, -5.0), ('α-linolenic acid', 18, 3, -11.0)]


def _fa_dq(rng, slot):
    sat = [f for f in FA if f[2] == 0]
    c18 = [f for f in FA if f[1] == 18]
    rows = sorted(rng.sample(sat, 3) + [f for f in c18 if f[2] > 0], key=lambda f: (f[2], f[1]))
    st = [f for f in FA if f[0] == 'stearic acid'][0]
    if st not in rows:
        rows = sorted(rows + [st], key=lambda f: (f[2], f[1]))
    intro = ('The table shows the number of carbon atoms, the number of cis C=C double bonds and the melting point of some fatty acids.\n\n'
             + table(['Fatty acid', 'Carbon atoms', 'C=C double bonds', 'Melting point / °C'], [(f[0], f[1], f[2], f'{f[3]:.1f}') for f in rows]))
    sats = [f for f in rows if f[2] == 0]
    a, b = sats[0], sats[-1]
    per2c = (b[3] - a[3]) / ((b[1] - a[1]) / 2)
    drop = st[3] - 13.4
    pc = pct_change(st[3], 13.4)
    parts = [
        ('State the melting point of oleic acid.', '13.4 °C', '13.4 °C (A1).', 1),
        ('Describe the effect of chain length on the melting point of saturated fatty acids.', f'Melting point increases with chain length, by about {per2c:.1f} °C per two extra carbons.', 'Positive relationship (A1); quantified using data (A1).', 2),
        ('Calculate the difference in melting point between stearic acid and oleic acid.', f'{drop:.1f} °C', f'{st[3]:.1f} − 13.4 = {drop:.1f} °C (A1).', 1),
        ('Calculate the percentage decrease in melting point from stearic to oleic acid.', f'{abs(pc):.0f} %', f'({st[3]:.1f} − 13.4)/{st[3]:.1f} × 100 (M1) = {abs(pc):.0f} % (A1).', 2),
        ('Explain the effect of double bonds on melting point.', 'Cis double bonds put kinks in the chain so molecules cannot pack closely; fewer intermolecular attractions; less energy needed to separate them.', 'Kinks / bent chains (A1); looser packing, weaker attractions (A1); lower melting point (A1).', 3),
        ('Predict, with a reason, whether a fat rich in linoleic acid would be solid or liquid at 20 °C.', 'Liquid – its melting point (−5 °C) is below 20 °C.', 'Liquid with data-based reason (A1).', 1),
        ('Suggest why fish living in cold water have more polyunsaturated fatty acids in their membranes.', 'Polyunsaturated fatty acids have low melting points, keeping membranes fluid at low temperatures so membrane proteins can function.', 'Low melting point / maintain fluidity (A1); link to membrane function (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch07-st4', _fa_dq)


# =============================================================================================
# ch08 B1.2 Proteins
# =============================================================================================
S('ch08-st1',
  terms=[('amino acid', 'the monomer of proteins, with a central carbon bonded to an amine group, a carboxyl group, a hydrogen atom and a variable R group'),
         ('peptide bond', 'the covalent bond formed by condensation between the carboxyl group of one amino acid and the amine group of another'),
         ('polypeptide', 'a chain of amino acids linked by peptide bonds'),
         ('essential amino acid', 'an amino acid that cannot be synthesised by the body and must be obtained from the diet'),
         ('R group', 'the variable side chain of an amino acid, which determines its properties (e.g. polar, non-polar, charged)')],
  facts=[('How many different amino acids are coded for by the genetic code and used by ribosomes?', '20', ['4', '64', '100'], 'Twenty amino acids are encoded.'),
         ('Which groups react to form a peptide bond?', 'the carboxyl group of one amino acid and the amine group of another', ['two amine groups', 'two R groups', 'two carboxyl groups'], 'Condensation releases water.'),
         ('Where in the cell are peptide bonds formed?', 'on ribosomes', ['in the nucleus', 'in lysosomes', 'in the Golgi apparatus'], 'Translation joins amino acids.'),
         ('Why do vegans need to plan their diets to obtain all essential amino acids?', 'some plant foods are low in particular essential amino acids', ['plants contain no protein', 'essential amino acids are only in meat', 'humans can make all amino acids'], 'Combining foods (e.g. legumes and cereals) supplies all of them.')],
  mc2=[('Why is the number of possible polypeptides almost unlimited?', 'Any of 20 amino acids can occur at each position and chains vary in length.', ['There are only 20 possible proteins.', 'Peptide bonds vary in type.', 'Each protein contains every amino acid once.'], '20ⁿ sequences for a chain of n amino acids.'),
       ('Which property of an amino acid is determined by its R group?', 'whether it is polar, non-polar, acidic or basic', ['whether it can form a peptide bond', 'the number of carbon atoms in its backbone', 'whether it contains nitrogen'], 'All amino acids share the backbone; R groups differ.'),
       ('A diet that lacks one essential amino acid would most directly affect', 'the synthesis of proteins that contain that amino acid', ['the synthesis of carbohydrates', 'the absorption of fats', 'the production of DNA'], 'Translation stalls without the amino acid.')],
  mc3=[('How many different tripeptides could be made from the 20 amino acids?', '8000', ['60', '400', '1 140'], '20³ = 8000.'),
       ('A protein has two polypeptide chains of 141 and 146 amino acids. How many peptide bonds does it contain?', '285', ['287', '286', '143'], '(141 − 1) + (146 − 1) = 285.')],
  why=[('Explain how amino acids are linked to form a polypeptide.', 'On the ribosome, the carboxyl group of one amino acid reacts with the amine group of the next in a condensation reaction; a peptide bond (–CO–NH–) forms and water is released; repetition produces a chain with an N-terminus and C-terminus.'),
       ('Explain why the diversity of proteins is so great.', 'There are 20 amino acids and they can be joined in any sequence; chains vary in length from a few to thousands; 20ⁿ possible sequences; each sequence folds into a specific shape giving a specific function.'),
       ('Explain how genes determine the sequence of amino acids in a polypeptide.', 'The base sequence of a gene is transcribed into mRNA; codons (triplets) are read on ribosomes; each codon specifies one amino acid via tRNA; so the base sequence determines the amino acid sequence.')],
  contrast=[('essential amino acids', 'non-essential amino acids', 'Essential amino acids cannot be made by the body and must come from the diet; non-essential amino acids can be synthesised from other compounds.'),
            ('a dipeptide', 'a polypeptide', 'A dipeptide consists of two amino acids joined by one peptide bond; a polypeptide is a long chain of many amino acids.')],
  misc=[('Peptide bonds are formed by hydrolysis.', 'Peptide bonds are formed by condensation (water released); hydrolysis breaks them.'),
        ('All amino acids have the same R group.', 'The R group is the variable part; 20 different R groups give the different amino acids.')],
  cases=[('the dietary combination of rice and lentils in South Asian cooking (dal-bhat)', 'Rice is low in lysine and lentils are low in methionine; together they supply all essential amino acids.', 'essential amino acids', 'Combining plant proteins with different deficiencies supplies all the amino acids the body cannot make.')],
  evaluate=[('The 20 amino acids are enough to produce all the protein diversity found in living things.', ['20ⁿ possible sequences is astronomically large even for short chains', 'post-translational modifications add further diversity'], ['some organisms use additional amino acids such as selenocysteine and pyrrolysine', 'only a tiny fraction of possible sequences fold into stable, functional proteins'], 'Twenty amino acids give more than enough diversity in principle; real diversity is extended by modifications and a few rare amino acids, but limited by folding constraints.')],
  extended=[('Describe the structure of amino acids and explain how they are joined to form a huge variety of polypeptides.', 'General structure: central C, NH₂, COOH, H, R; R groups vary (20 types, polar/non-polar/charged); peptide bond by condensation on ribosomes; water released; N- and C-terminus; any sequence; 20ⁿ; genetic code determines sequence; essential vs non-essential.', 7)],
  )


@R.add('ch08-st1', 'C3', (1, 5), 'numerical')
def peptide_calc(rng, slot):
    prot = pick(rng, [('insulin', [21, 30]), ('haemoglobin', [141, 141, 146, 146]), ('a bacterial enzyme', [rng.randint(180, 420)]),
                      ('an antibody (IgG)', [214, 214, 446, 446]), ('a dimeric transcription factor', [rng.randint(80, 140)] * 2),
                      ('lysozyme', [129]), ('a spider-silk protein fragment', [rng.randint(300, 600)])])
    nm, chains = prot
    n = sum(chains)
    bonds = n - len(chains)
    f = rng.randrange(2) if slot.d >= 2 else 0
    if f == 0:
        desc = ' + '.join(map(str, chains)) if len(chains) > 1 else str(chains[0])
        stem = f'{nm[0].upper() + nm[1:]} consists of {len(chains)} polypeptide chain{"s" if len(chains) > 1 else ""} containing {desc} amino acids. Calculate the number of peptide bonds and the number of water molecules released during its synthesis.'
        return num(stem, f'{bonds} peptide bonds; {bonds} water molecules', f'Each chain of n amino acids has n − 1 bonds (M1); total {n} − {len(chains)} = {bonds} bonds, one water per bond (A1).', 2)
    L = pick(rng, [3, 4, 5, 6, 8, 10])
    poss = 20 ** L
    stem = f'Calculate how many different polypeptides of {L} amino acids could theoretically be produced from the 20 amino acids. Explain what this suggests about protein diversity.'
    return num(stem, f'20^{L} = {poss:,}'.replace(',', ' ') + '; enormous diversity even for short chains',
               f'20 choices at each of {L} positions: 20^{L} (M1) = {poss:,} (A1); diversity practically unlimited for real proteins of hundreds of amino acids (R1).'.replace(',', ' '), 3)


S('ch08-st2',
  terms=[('primary structure', 'the sequence of amino acids in a polypeptide, determined by the base sequence of a gene'),
         ('secondary structure', 'regular folding of the polypeptide backbone into α-helices or β-pleated sheets, stabilised by hydrogen bonds between C=O and N–H groups'),
         ('tertiary structure', 'the three-dimensional folding of a whole polypeptide, stabilised by interactions between R groups'),
         ('quaternary structure', 'the association of two or more polypeptide subunits (and sometimes prosthetic groups) into a functional protein'),
         ('disulfide bond', 'a covalent bond between the sulfur atoms of two cysteine R groups, which stabilises tertiary or quaternary structure'),
         ('conjugated protein', 'a protein that contains a non-polypeptide component (prosthetic group), such as the haem in haemoglobin')],
  facts=[('Which bonds stabilise α-helices and β-pleated sheets?', 'hydrogen bonds between groups of the polypeptide backbone', ['disulfide bonds between cysteines', 'peptide bonds between R groups', 'ionic bonds between phosphate groups'], 'C=O and N–H of the backbone form hydrogen bonds.'),
         ('Which amino acid forms disulfide bonds?', 'cysteine', ['glycine', 'alanine', 'lysine'], 'Cysteine has an –SH group.'),
         ('Which protein is an example of quaternary structure with a prosthetic group?', 'haemoglobin', ['collagen', 'insulin monomer', 'keratin'], 'Four subunits each with a haem group.'),
         ('Which level of structure is directly determined by the gene sequence?', 'primary structure', ['secondary structure only', 'quaternary structure only', 'the prosthetic group'], 'Higher levels follow from the primary sequence.')],
  mc2=[('Why does the tertiary structure of a globular protein cause hydrophobic R groups to be in the interior?', 'Hydrophobic R groups avoid water and cluster together in the centre, while hydrophilic groups face the aqueous surroundings.', ['Hydrophobic R groups form peptide bonds in the centre.', 'Hydrophilic R groups are repelled by water.', 'Disulfide bonds pull all hydrophobic groups inward.'], 'Hydrophobic interactions drive folding.'),
       ('Which interactions stabilise tertiary structure?', 'hydrogen bonds, ionic bonds, disulfide bonds and hydrophobic interactions between R groups', ['peptide bonds only', 'glycosidic bonds', 'phosphodiester bonds'], 'Several types of R-group interaction.'),
       ('Why can a single amino acid substitution change the function of a protein?', 'It may alter R-group interactions, changing the tertiary structure and shape.', ['It always breaks all peptide bonds.', 'It changes the genetic code.', 'It removes the quaternary structure in all proteins.'], 'E.g. sickle-cell haemoglobin.')],
  mc3=[('In sickle-cell haemoglobin, a glutamic acid (charged, polar) at position 6 of the β chain is replaced by valine (non-polar). What is the most likely effect?', 'Hydrophobic patches on the surface cause haemoglobin molecules to stick together into fibres at low oxygen.', ['The haem group is lost.', 'The protein can no longer form peptide bonds.', 'The protein becomes a fibrous structural protein.'], 'Altered surface properties cause polymerisation.'),
       ('A protein retains its function after treatment with a reducing agent that breaks disulfide bonds, but loses it after heating. What does this suggest?', 'Its shape depends mainly on non-covalent interactions such as hydrogen bonds and hydrophobic interactions.', ['Its shape depends only on disulfide bonds.', 'It has no tertiary structure.', 'Heating forms disulfide bonds.'], 'Heat disrupts weak interactions.')],
  why=[('Explain how the primary structure of a protein determines its three-dimensional shape.', 'The sequence of amino acids determines where hydrogen bonds form in the backbone (α-helices, β-sheets) and where R groups interact (hydrophobic clustering, ionic, hydrogen and disulfide bonds), so the chain folds into one specific stable conformation.'),
       ('Explain the role of hydrophobic interactions in protein folding.', 'Non-polar R groups are excluded by water, so they cluster together in the protein interior; polar and charged R groups stay on the surface interacting with water; this drives the chain into a compact globular shape.'),
       ('Explain how the quaternary structure of haemoglobin relates to its function.', 'Four polypeptide subunits (two α, two β) each hold a haem group with iron that binds O₂; interactions between subunits allow cooperative binding, so oxygen is loaded efficiently in the lungs and unloaded in tissues.')],
  contrast=[('α-helices', 'β-pleated sheets', 'In an α-helix the polypeptide coils, with hydrogen bonds between groups four amino acids apart in the same strand; in a β-pleated sheet adjacent stretches of chain lie side by side, hydrogen bonded between strands.'),
            ('tertiary structure', 'quaternary structure', 'Tertiary structure is the 3D folding of a single polypeptide; quaternary structure is the arrangement of two or more polypeptides (and prosthetic groups) in a protein.')],
  misc=[('Secondary structure is stabilised by bonds between R groups.', 'Secondary structure is stabilised by hydrogen bonds between C=O and N–H groups of the backbone; R-group interactions stabilise tertiary structure.'),
        ('All proteins have quaternary structure.', 'Only proteins made of more than one polypeptide (e.g. haemoglobin, collagen) have quaternary structure; many enzymes are single polypeptides.')],
  cases=[('sickle-cell haemoglobin (HbS)', 'A single substitution of valine for glutamic acid on the β chain causes haemoglobin to polymerise at low oxygen, distorting red cells into sickle shapes.', 'the link between primary structure and protein shape', 'One change in sequence alters R-group interactions, so the shape and behaviour of the whole protein change.'),
         ('AlphaFold’s prediction of protein structures from sequences (2020–2022)', 'An AI system predicted 3D structures of over 200 million proteins from their amino acid sequences with high accuracy.', 'how primary structure determines tertiary structure', 'Accurate prediction from sequence alone confirms that the amino acid sequence encodes the folded shape.')],
  evaluate=[('The primary structure of a protein completely determines its final shape.', ['Anfinsen showed denatured ribonuclease refolds spontaneously into its active shape', 'AI structure prediction from sequence is highly accurate'], ['many proteins need chaperones to fold correctly in cells', 'post-translational modifications and prosthetic groups also affect structure; prions can adopt alternative shapes'], 'Primary structure contains the information for folding, but the cellular environment, chaperones and modifications influence the final, functional shape.')],
  extended=[('Describe the four levels of protein structure and explain how each is stabilised.', 'Primary: sequence, peptide bonds, gene-determined. Secondary: α-helix, β-sheet, H bonds in backbone. Tertiary: 3D fold, R-group interactions – hydrophobic, H bonds, ionic, disulfide. Quaternary: multiple subunits, e.g. haemoglobin (4 subunits + haem), collagen (3 chains); conjugated vs non-conjugated. Shape determines function.', 8)],
  )

S('ch08-st3',
  terms=[('denaturation', 'a change in the three-dimensional structure of a protein, caused by breaking of the bonds that maintain it, so that it loses its biological activity'),
         ('optimum pH', 'the pH at which a protein (such as an enzyme) is most stable and active'),
         ('thermophile', 'an organism adapted to live at high temperatures, with proteins that remain stable when hot'),
         ('irreversible denaturation', 'denaturation after which the protein cannot return to its original shape, e.g. when egg albumin is cooked')],
  facts=[('Which bonds are broken first when a protein is heated and denatures?', 'hydrogen bonds and other weak interactions', ['peptide bonds', 'covalent bonds within amino acids', 'glycosidic bonds'], 'Primary structure usually survives; higher levels are lost.'),
         ('How does extreme pH cause denaturation?', 'by changing the charges on R groups, disrupting ionic and hydrogen bonds', ['by breaking peptide bonds', 'by adding amino acids', 'by forming new disulfide bonds'], 'H⁺ or OH⁻ alter ionisation of R groups.'),
         ('Which enzyme works at an optimum pH of about 2?', 'pepsin in the stomach', ['salivary amylase', 'pancreatic lipase', 'trypsin'], 'Stomach acid gives pH 1.5–2.5.'),
         ('The DNA polymerase used in PCR comes from Thermus aquaticus. Why?', 'it is stable at high temperatures that denature most proteins', ['it works best at 37 °C', 'it is denatured at 50 °C', 'it is found in humans'], 'Taq polymerase withstands 95 °C.')],
  mc2=[('Why is denaturation by boiling usually irreversible?', 'The polypeptide chains unfold and become tangled with new random interactions, so the original shape cannot re-form.', ['Peptide bonds are broken and cannot re-form.', 'The amino acids are oxidised.', 'Water is removed from the protein.'], 'Unfolded chains aggregate (e.g. cooked egg white).'),
       ('Why does a protein lose its function when denatured even though its amino acid sequence is unchanged?', 'Function depends on a specific 3D shape, which is lost.', ['Function depends only on primary structure.', 'Denaturation removes amino acids.', 'Denatured proteins become carbohydrates.'], 'Shape determines function.'),
       ('Why do proteins from thermophilic archaea not denature at 80 °C?', 'They have more ionic bonds, disulfide bonds and hydrophobic interactions stabilising their structure.', ['They have no tertiary structure.', 'They are made of different amino acids not found in other organisms.', 'Their peptide bonds are stronger.'], 'Extra stabilising interactions resist heat.')],
  mc3=[('Egg white turns from clear to opaque white when cooked. Which explanation is correct?', 'Albumin proteins denature and aggregate, scattering light.', ['Albumin is hydrolysed into amino acids.', 'Water evaporates from the albumin.', 'New peptide bonds form.'], 'Unfolded proteins clump together.'),
       ('A student adds acid to milk, and the milk forms curds. What does this show?', 'Casein proteins denature/precipitate when pH changes alter their charges.', ['Milk sugar is hydrolysed.', 'Fats are converted to protein.', 'The acid creates new amino acids.'], 'Charge changes reduce solubility.')],
  why=[('Explain how high temperature causes denaturation of a protein.', 'Increased kinetic energy makes the molecule vibrate more; weak bonds (hydrogen, ionic) and hydrophobic interactions maintaining secondary/tertiary structure break; the protein unfolds and loses its specific shape and function.'),
       ('Explain how changes in pH affect protein structure.', 'H⁺ and OH⁻ ions change the ionisation of acidic and basic R groups; this alters charges, breaking ionic bonds and hydrogen bonds between R groups; the tertiary structure changes and the protein may denature.'),
       ('Explain why most human proteins function best at about 37 °C and pH 7.4.', 'Their structures evolved to be stable in these conditions; at higher temperatures or extreme pH weak bonds are disrupted and the proteins denature; homeostasis keeps conditions near these values.')],
  contrast=[('reversible denaturation', 'irreversible denaturation', 'In reversible denaturation the protein refolds to its active shape when conditions return to normal (e.g. mild pH change); in irreversible denaturation the unfolded chains aggregate or form new bonds so the original shape cannot be regained (e.g. cooked egg).')],
  misc=[('Denaturation breaks the peptide bonds of a protein.', 'Denaturation disrupts the weaker bonds maintaining 3D shape (hydrogen, ionic, hydrophobic, sometimes disulfide); the peptide bonds of the primary structure usually remain intact.'),
        ('Enzymes are killed by high temperatures.', 'Enzymes are molecules, not living organisms; they are denatured, not killed.')],
  cases=[('Taq polymerase from Thermus aquaticus, isolated from hot springs in Yellowstone', 'The enzyme remains active after repeated heating to 95 °C in PCR.', 'resistance of proteins to denaturation', 'Extra stabilising interactions in its structure allow it to keep its shape at temperatures that denature most proteins.'),
         ('pepsin in the human stomach', 'Pepsin works best at pH about 2 and becomes inactive in the near-neutral small intestine.', 'the effect of pH on protein structure', 'Its R-group charges are suited to strong acid; at neutral pH the changed ionisation alters its shape.')],
  evaluate=[('Denaturation is always harmful to organisms.', ['loss of enzyme function at high fever temperatures can be fatal', 'heat stroke denatures cellular proteins'], ['cooking denatures food proteins, making them easier to digest', 'denaturation of pathogen proteins by stomach acid or fever helps defence'], 'Denaturation of an organism’s own proteins is harmful, but denaturation of food and pathogen proteins can be beneficial; the effect depends on whose proteins are denatured.')],
  extended=[('Explain how temperature and pH affect protein structure and function, with reference to named examples.', 'Weak bonds maintain shape; heat increases vibration, breaks H bonds/hydrophobic interactions; unfolds; loss of function; often irreversible (egg albumin); pH alters R-group ionisation, breaks ionic/H bonds; optimum pH (pepsin 2, trypsin 8); thermophile proteins (Taq) more stable; homeostasis maintains conditions.', 8)],
  )


def _denature_dq(rng, slot):
    temps = [30, 40, 50, 60, 70, 80, 90]
    tm1 = rng.uniform(52, 60)
    tm2 = rng.uniform(78, 86)
    act1 = [round(100 / (1 + math.exp((t - tm1) / 3.5)), 0) for t in temps]
    act2 = [round(100 / (1 + math.exp((t - tm2) / 3.5)), 0) for t in temps]
    p1 = pick(rng, ['a protease from cod (a cold-water fish)', 'a protease from the soil bacterium Bacillus subtilis', 'lactate dehydrogenase from rabbit muscle'])
    p2 = pick(rng, ['a protease from Thermus aquaticus', 'a homologous enzyme from the archaeon Pyrococcus furiosus', 'the same enzyme from a hot-spring bacterium'])
    h1 = interp_zero(temps, [a - 50 for a in act1])
    h2 = interp_zero(temps, [a - 50 for a in act2])
    if h1 is None or h2 is None:
        return None
    intro = (f'Samples of {p1} (enzyme X) and {p2} (enzyme Y) were held at different temperatures for 10 minutes, cooled to 25 °C and their remaining activity measured as a percentage of the untreated activity.\n\n'
             + table(['Temperature / °C', 'Enzyme X activity remaining / %', 'Enzyme Y activity remaining / %'], [(t, f'{a:.0f}', f'{b:.0f}') for t, a, b in zip(temps, act1, act2)]))
    parts = [
        ('State the activity of enzyme X remaining after treatment at 60 °C.', f'{act1[3]:.0f} %', f'{act1[3]:.0f} % (A1).', 1),
        ('Estimate the temperature at which each enzyme has lost half of its activity.', f'X ≈ {h1:.0f} °C; Y ≈ {h2:.0f} °C', f'Interpolation (M1); X {h1:.0f} °C and Y {h2:.0f} °C, accept ±2 °C (A1).', 2),
        ('Compare the effect of temperature on enzymes X and Y.', 'Both retain full activity at low temperatures and lose activity as temperature rises; Y tolerates much higher temperatures before losing activity.', 'Similarity (A1); difference with data (A1).', 2),
        ('Explain why activity was measured at 25 °C after cooling, rather than at the treatment temperature.', 'It measures only the permanent (irreversible) loss of activity due to denaturation, not the temporary effect of temperature on reaction rate.', 'Separates denaturation from effect on rate (R1).', 1),
        ('Explain the loss of activity of enzyme X at high temperatures.', 'Heat breaks hydrogen and ionic bonds/hydrophobic interactions maintaining tertiary structure; active site changes shape; substrate no longer binds; denaturation.', 'Weak bonds broken (A1); shape/active site changed (A1); irreversible denaturation (A1).', 3),
        ('Suggest how the structure of enzyme Y differs to make it more heat stable.', 'More disulfide bonds, ionic bonds (salt bridges) and hydrophobic interactions; more compact core.', 'Any valid structural difference (A1).', 1),
        ('Suggest one industrial use of enzyme Y and justify it.', 'PCR or biological washing powders/industrial processes at high temperature – remains active and reactions are faster at high temperature.', 'Use (A1) with justification (R1).', 2),
    ]
    return intro, parts


data_q(R, 'ch08-st3', _denature_dq)

S('ch08-st4',
  terms=[('fibrous protein', 'a protein with long, narrow, insoluble polypeptide chains, usually with a structural role, such as collagen or keratin'),
         ('globular protein', 'a protein with a compact, rounded, usually water-soluble shape, often with a metabolic role, such as insulin or enzymes'),
         ('collagen', 'a fibrous structural protein made of three polypeptide chains wound into a triple helix, found in skin, tendons and bone'),
         ('insulin', 'a small globular hormone of two polypeptide chains linked by disulfide bonds, which binds to receptors to lower blood glucose')],
  facts=[('Which is a fibrous protein?', 'collagen', ['insulin', 'haemoglobin', 'amylase'], 'Long triple helices give tensile strength.'),
         ('Which is a globular protein?', 'insulin', ['collagen', 'keratin', 'silk fibroin'], 'Compact, soluble hormone.'),
         ('Which amino acid occurs at every third position in collagen chains?', 'glycine', ['cysteine', 'tryptophan', 'lysine'], 'Its small R group allows tight packing of the triple helix.'),
         ('How many polypeptide chains make up a collagen molecule?', 'three', ['one', 'two', 'four'], 'A triple helix.')],
  mc2=[('Why are globular proteins usually soluble in water?', 'Hydrophilic R groups are on the outside and hydrophobic ones are buried inside.', ['They have no R groups.', 'They are made of carbohydrate.', 'Hydrophobic R groups face outward.'], 'Polar surface interacts with water.'),
       ('Why is collagen suited to its function in tendons?', 'Its triple helices bundle into fibres with high tensile strength and little stretch.', ['It is soluble and easily transported.', 'It has an active site.', 'It binds oxygen.'], 'Structure matches mechanical role.'),
       ('Why must insulin have a precise globular shape?', 'It must bind specifically to insulin receptors on target cells.', ['It must form long fibres.', 'It must be insoluble.', 'It must dissolve in lipids.'], 'Shape-dependent binding.')],
  mc3=[('Vitamin C is needed to modify proline in collagen. Sailors with scurvy had bleeding gums and poor wound healing. What is the best explanation?', 'Collagen fibres were weak because they could not be stabilised properly.', ['Insulin was not produced.', 'Haemoglobin could not bind oxygen.', 'Enzymes were denatured.'], 'Hydroxylation stabilises the triple helix.'),
       ('A new protein is long, insoluble and has a repeating sequence with little variation. What is its most likely function?', 'structural support', ['catalysing a reaction', 'acting as a hormone', 'transporting oxygen in blood'], 'Features typical of fibrous proteins.')],
  why=[('Explain how the structure of collagen is related to its function.', 'Three polypeptide chains wound in a tight triple helix; glycine every third position allows close packing; hydrogen bonds between chains; molecules cross-linked into fibrils and fibres; so collagen is strong, inelastic and insoluble, ideal for tendons, skin and bone.'),
       ('Explain how the structure of insulin relates to its function.', 'Insulin is a small globular protein of two chains held by disulfide bonds; its specific shape binds to complementary insulin receptors; it is soluble so it can travel in blood plasma from the pancreas to target cells.')],
  contrast=[('fibrous proteins', 'globular proteins', 'Fibrous proteins are long, narrow, insoluble, with repetitive sequences and structural roles (collagen, keratin); globular proteins are compact, rounded, usually soluble, with varied sequences and metabolic roles (enzymes, insulin, haemoglobin).')],
  misc=[('All proteins are enzymes.', 'Proteins have many roles: structural (collagen), hormones (insulin), transport (haemoglobin), defence (antibodies), movement (actin/myosin) as well as enzymes.'),
        ('Fibrous proteins dissolve easily in blood plasma.', 'Fibrous proteins are generally insoluble; globular proteins tend to be soluble.')],
  cases=[('scurvy in sailors on long voyages in the 18th century', 'Lack of vitamin C caused bleeding gums, reopening of old wounds and weakened tissues.', 'the structure and function of collagen', 'Vitamin C is needed to stabilise collagen; without it, collagen fibres are weak, showing the importance of structure for function.')],
  evaluate=[('Classifying proteins as fibrous or globular is a useful simplification.', ['it links shape to function in a memorable way', 'it predicts solubility and role'], ['some proteins, such as myosin, have both fibrous and globular regions', 'membrane proteins fit neither category well'], 'It is a useful first framework but must be supplemented by more detailed structural classification.')],
  extended=[('Compare the structure and function of collagen and insulin as examples of fibrous and globular proteins.', 'Collagen: 3 chains, triple helix, Gly-X-Y repeat, insoluble, H-bonded, cross-links, tensile strength, tendons/skin. Insulin: 2 chains (21 + 30), disulfide bonds, globular, soluble, specific shape, binds receptor, hormone. Both: polypeptides, primary structure determines shape, function depends on shape.', 7)],
  )


# =============================================================================================
# ch09 B2.1 Membranes and membrane transport
# =============================================================================================
S('ch09-st1',
  terms=[('fluid mosaic model', 'the model of membrane structure in which proteins are embedded in or attached to a fluid phospholipid bilayer and can move laterally'),
         ('integral protein', 'a membrane protein embedded in the hydrophobic core of the bilayer, often spanning it (transmembrane)'),
         ('peripheral protein', 'a membrane protein attached to the surface of the bilayer or to integral proteins, not embedded in the hydrophobic core'),
         ('phospholipid bilayer', 'a double layer of phospholipids with hydrophilic heads facing outwards and hydrophobic tails facing inwards, forming the basic structure of membranes'),
         ('Davson–Danielli model', 'an earlier model in which the phospholipid bilayer was sandwiched between two continuous layers of protein, later falsified')],
  facts=[('Who proposed the fluid mosaic model in 1972?', 'Singer and Nicolson', ['Davson and Danielli', 'Watson and Crick', 'Schleiden and Schwann'], 'It replaced the Davson–Danielli sandwich model.'),
         ('Approximately how thick is a plasma membrane?', 'about 7–10 nm', ['about 7–10 µm', 'about 1 mm', 'about 0.1 nm'], 'Visible as two dark lines in TEM.'),
         ('Which evidence falsified the Davson–Danielli model?', 'freeze-fracture images showing proteins embedded within the bilayer', ['the discovery of DNA', 'the fact that membranes are thin', 'the discovery of chloroplasts'], 'Proteins span the hydrophobic core.'),
         ('Which part of a phospholipid faces the cytoplasm and tissue fluid?', 'the hydrophilic phosphate head', ['the hydrophobic tails', 'the fatty acid chains', 'the ester bonds only'], 'Heads interact with water on both sides.')],
  mc2=[('Why is the bilayer a barrier to ions and polar molecules?', 'Its hydrophobic core does not allow charged or polar particles to pass easily.', ['It is completely impermeable to everything.', 'It is made of protein.', 'Its heads are hydrophobic.'], 'Small non-polar molecules pass easily; ions need proteins.'),
       ('What did the fusion of mouse and human cells (Frye and Edidin, 1970) show?', 'Membrane proteins can move laterally within the bilayer.', ['Membranes are rigid.', 'Proteins are on the surface only.', 'Cells cannot fuse.'], 'Labelled proteins mixed within 40 minutes.'),
       ('Why are integral proteins amphipathic?', 'Their hydrophobic regions lie within the bilayer core and hydrophilic regions face the aqueous surroundings.', ['They are entirely hydrophobic.', 'They are entirely hydrophilic.', 'They lack R groups.'], 'Matching the environment of each region.')],
  mc3=[('A membrane protein extracted from cells has a central stretch of 20 non-polar amino acids flanked by charged ones. What is its most likely position?', 'spanning the membrane, with the non-polar stretch in the hydrophobic core', ['entirely in the cytoplasm', 'attached only to the outer surface', 'inside the nucleus'], 'About 20 non-polar residues form one transmembrane helix.'),
       ('In a TEM image at × 2 000 000, a plasma membrane appears as two dark lines 16 mm apart from outer edge to outer edge. What is the membrane thickness?', '8 nm', ['0.8 nm', '80 nm', '8 µm'], '16 mm = 16 000 000 nm ÷ 2 000 000 = 8 nm.')],
  why=[('Explain how the properties of phospholipids lead to the formation of a bilayer.', 'Phospholipids are amphipathic; in water the hydrophilic heads associate with water and the hydrophobic tails are excluded and face each other, forming two layers; this arrangement is energetically stable and self-sealing.'),
       ('Explain the evidence that led to the replacement of the Davson–Danielli model by the fluid mosaic model.', 'Freeze-fracture EM showed proteins embedded in the bilayer; membrane proteins were found to be varied and amphipathic, so could not form continuous layers; fluorescent labelling of cell fusion showed proteins move; so the model was falsified and replaced.')],
  contrast=[('integral proteins', 'peripheral proteins', 'Integral proteins are embedded in the hydrophobic core and often span the membrane (e.g. channels, pumps); peripheral proteins are attached to the surface or to integral proteins and do not penetrate the core.'),
            ('the Davson–Danielli model', 'the fluid mosaic model', 'Davson–Danielli proposed a static bilayer sandwiched between continuous protein layers; the fluid mosaic model has proteins embedded in or attached to a fluid bilayer, able to move laterally.')],
  misc=[('In the fluid mosaic model, proteins form a continuous layer over the bilayer.', 'That was the Davson–Danielli model; in the fluid mosaic model proteins are scattered like a mosaic within and on the fluid bilayer.'),
        ('The phospholipid tails face the water on both sides of the membrane.', 'The hydrophobic tails face inward towards each other; the hydrophilic heads face the water.')],
  cases=[('freeze-fracture electron micrographs of membranes', 'Splitting frozen membranes along the middle revealed bumps (proteins) on the fracture faces.', 'the falsification of the Davson–Danielli model', 'Proteins were seen within the bilayer, not just on its surfaces, so the sandwich model had to be rejected.'),
         ('the Frye–Edidin cell fusion experiment (1970)', 'Mouse and human cells with differently labelled membrane proteins were fused; within 40 minutes the labels were intermixed.', 'the fluidity of membranes', 'Proteins diffuse laterally in the bilayer, supporting the fluid nature of the model.')],
  apply=[('Draw and label a diagram of the fluid mosaic model. List the components that should be shown.', 'Phospholipid bilayer (heads and tails labelled), integral (transmembrane) protein, peripheral protein, channel protein, glycoprotein with carbohydrate facing outward, cholesterol between phospholipids, inner/outer surfaces labelled.', 4)],
  evaluate=[('The fluid mosaic model is a complete description of membrane structure.', ['it accounts for the bilayer, embedded proteins and lateral movement, and has survived many tests', 'it explains selective permeability and membrane flexibility'], ['membranes contain lipid rafts and protein domains that are less fluid than the model implies', 'cytoskeletal attachments restrict movement of many proteins'], 'It remains the best general model, but modern evidence refines it with domains and restrictions on movement – models are simplifications that are improved over time.')],
  extended=[('Describe the fluid mosaic model of membrane structure and evaluate the evidence for it.', 'Bilayer of amphipathic phospholipids; integral and peripheral proteins; glycoproteins, glycolipids, cholesterol; fluidity, lateral movement. Evidence: freeze-fracture, Frye–Edidin, amphipathic proteins, TEM trilaminar appearance. Falsified Davson–Danielli. Limitations: rafts, cytoskeleton.', 8)],
  )

S('ch09-st2',
  terms=[('simple diffusion', 'the net passive movement of particles from a region of higher concentration to a region of lower concentration, directly through the phospholipid bilayer'),
         ('facilitated diffusion', 'passive movement of particles down a concentration gradient through specific channel or carrier proteins in a membrane'),
         ('osmosis', 'the net passive movement of water molecules across a partially permeable membrane from a region of lower solute concentration to a region of higher solute concentration'),
         ('aquaporin', 'a channel protein in the membrane that allows rapid passage of water molecules'),
         ('isotonic', 'describes a solution with the same solute concentration (osmolarity) as the cell, so there is no net movement of water'),
         ('hypertonic', 'describes a solution with a higher solute concentration than the cell, so the cell loses water by osmosis')],
  facts=[('Which substance crosses the bilayer mainly by simple diffusion?', 'oxygen', ['glucose', 'sodium ions', 'proteins'], 'Small non-polar molecules dissolve in the bilayer.'),
         ('Which protein allows rapid osmosis in kidney collecting duct cells?', 'aquaporin', ['sodium–potassium pump', 'insulin receptor', 'haemoglobin'], 'Aquaporins are water channels.'),
         ('What happens to an animal cell placed in a hypotonic solution?', 'it gains water, swells and may burst', ['it loses water and shrinks', 'nothing changes', 'it becomes plasmolysed'], 'No cell wall to resist expansion.'),
         ('What happens to a plant cell placed in a concentrated salt solution?', 'it loses water and becomes plasmolysed', ['it bursts', 'it becomes turgid', 'it gains water'], 'The membrane pulls away from the wall.'),
         ('Why are tissues for transplants kept in isotonic saline?', 'to prevent cells gaining or losing water by osmosis', ['to kill bacteria', 'to provide glucose', 'to keep the tissue frozen'], 'Isotonic solutions prevent damage.')],
  mc2=[('Why does facilitated diffusion show a maximum rate at high concentration gradients?', 'All the carrier or channel proteins become occupied.', ['The membrane becomes impermeable.', 'ATP runs out.', 'The concentration gradient reverses.'], 'Limited number of transport proteins.'),
       ('Which factor would NOT increase the rate of simple diffusion across a membrane?', 'increasing the thickness of the membrane', ['increasing the concentration gradient', 'increasing the surface area', 'increasing the temperature'], 'Thicker barriers slow diffusion.'),
       ('Why can glucose not cross the bilayer by simple diffusion at a useful rate?', 'It is a relatively large polar molecule.', ['It is non-polar.', 'It is too small.', 'It is positively charged.'], 'GLUT carriers are needed.')],
  mc3=[('Potato cylinders gained mass in 0.1 mol dm⁻³ sucrose and lost mass in 0.4 mol dm⁻³. What can be concluded?', 'The potato cells’ solute concentration is between 0.1 and 0.4 mol dm⁻³.', ['The cells are isotonic with 0.1 mol dm⁻³.', 'Sucrose entered the cells.', 'The cells are isotonic with 0.4 mol dm⁻³.'], 'Isotonic point lies between gain and loss.'),
       ('Red blood cells were placed in solutions of different NaCl concentrations. In which would they burst (haemolyse)?', 'distilled water', ['0.9 % NaCl', '2 % NaCl', '5 % NaCl'], '0.9 % is isotonic; water is hypotonic.')],
  why=[('Explain why cells placed in a hypertonic solution lose water.', 'The solution has a higher solute concentration (lower water potential) than the cytoplasm; water moves by osmosis out of the cell across the partially permeable membrane down its water potential gradient.'),
       ('Explain how the structure of channel proteins allows facilitated diffusion of specific ions.', 'Channel proteins form a hydrophilic pore through the membrane; the pore diameter and charges of lining amino acids allow only particular ions to pass; ions move down their concentration gradient without energy input.'),
       ('Explain why plant cells do not burst when placed in distilled water.', 'Water enters by osmosis and the cell swells, but the strong cellulose cell wall exerts pressure that resists further expansion; the cell becomes turgid rather than bursting.')],
  contrast=[('simple diffusion', 'facilitated diffusion', 'Both are passive and move substances down a concentration gradient; simple diffusion occurs directly through the bilayer (small non-polar molecules); facilitated diffusion uses specific channel or carrier proteins (ions, polar molecules) and can saturate.'),
            ('hypotonic solutions', 'hypertonic solutions', 'A hypotonic solution has a lower solute concentration than the cell, so water enters; a hypertonic solution has a higher solute concentration, so water leaves.')],
  misc=[('In osmosis, water moves from low water concentration to high water concentration.', 'Water moves from a region of lower solute concentration (higher water potential) to higher solute concentration (lower water potential).'),
        ('Facilitated diffusion uses ATP because proteins are involved.', 'Facilitated diffusion is passive and uses no ATP; it is active transport that uses ATP.'),
        ('Diffusion stops when the concentrations are equal because particles stop moving.', 'Particles keep moving randomly; at equilibrium there is no net movement because movement is equal in both directions.')],
  cases=[('the use of isotonic saline (0.9 % NaCl) to store donor kidneys before transplantation', 'Organs are flushed and stored in cold isotonic solution for up to 24–36 hours.', 'osmosis and isotonic solutions', 'Equal solute concentration prevents net water movement, so cells neither swell and burst nor shrink.'),
         ('aquaporins in the collecting ducts of the kidney', 'ADH causes vesicles containing aquaporins to fuse with membranes, increasing water reabsorption.', 'facilitated diffusion of water', 'More channels increase membrane permeability to water, so more water moves out of the filtrate by osmosis.')],
  evaluate=[('Osmosis is just a special case of diffusion.', ['water moves down its own concentration (water potential) gradient passively', 'the same factors (gradient, area, temperature) affect both'], ['osmosis specifically requires a partially permeable membrane that restricts solute movement', 'much water passes through aquaporins (facilitated) and its movement is driven by solute effects on water potential'], 'Osmosis is a form of passive diffusion of water, but it is distinct because it depends on a partially permeable membrane and solute effects on water potential.')],
  extended=[('Explain the mechanisms of simple diffusion, facilitated diffusion and osmosis, and outline factors affecting their rates.', 'Simple: through bilayer, non-polar, small; facilitated: channels (ions, gated) and carriers (glucose), specific, saturable; osmosis: water, partially permeable membrane, aquaporins, from low to high solute; factors: gradient, SA, distance/thickness, temperature, number of channel proteins.', 8)],
  )


def _osmosis_dq(rng, slot):
    conc = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    iso = rng.uniform(0.17, 0.33)
    tissue = pick(rng, ['potato (Solanum tuberosum)', 'sweet potato', 'carrot root', 'beetroot', 'apple'])
    k = rng.uniform(55, 75)
    pcts = [round(k * (iso - c) * rng.uniform(0.92, 1.08), 1) for c in conc]
    if len(set(x > 0 for x in pcts)) < 2:
        return None
    est = interp_zero(conc, pcts)
    if est is None:
        return None
    m0 = [round(rng.uniform(1.8, 2.4), 2) for _ in conc]
    m1 = [round(a * (1 + p / 100), 2) for a, p in zip(m0, pcts)]
    real = [100 * (b - a) / a for a, b in zip(m0, m1)]
    i = rng.randrange(len(conc))
    intro = (f'Cylinders of {tissue} were weighed, placed in sucrose solutions of different concentrations for 24 hours at 25 °C, blotted and reweighed.\n\n'
             + table(['Sucrose / mol dm⁻³', 'Initial mass / g', 'Final mass / g', '% change in mass'], [(f'{c:.1f}', f'{a:.2f}', f'{b:.2f}', '?' if j == i else f'{signed(r)}') for j, (c, a, b, r) in enumerate(zip(conc, m0, m1, real))]))
    parts = [
        (f'Calculate the percentage change in mass in {conc[i]:.1f} mol dm⁻³ sucrose.', f'{signed(real[i])} %', f'({m1[i]:.2f} − {m0[i]:.2f})/{m0[i]:.2f} × 100 (M1) = {signed(real[i])} % (A1).', 2),
        ('Explain why the results were expressed as percentage change in mass rather than change in mass.', 'The cylinders had different initial masses; percentage change allows fair comparison.', 'Different starting masses (A1).', 1),
        ('Estimate the sucrose concentration that is isotonic with the tissue.', f'≈ {est:.2f} mol dm⁻³', f'Concentration where % change = 0, by interpolation between the bracketing values (M1); ≈ {est:.2f} mol dm⁻³ (A1).', 2),
        ('Explain the change in mass in 0.5 mol dm⁻³ sucrose.', 'The solution is hypertonic to the cells (lower water potential); water leaves the cells by osmosis through the partially permeable membranes, so mass decreases.', 'Hypertonic / lower water potential outside (A1); water leaves by osmosis (A1).', 2),
        ('Suggest why the cylinders were blotted before reweighing.', 'To remove surface solution, which would add mass that was not taken up by the cells.', 'Remove surface liquid (A1).', 1),
        ('State two variables that should be controlled.', 'Temperature; time; surface area/size of cylinders; volume of solution; source of tissue.', 'Any two (A1 A1).', 2),
        ('Predict the appearance of cells from the 0.5 mol dm⁻³ solution under the microscope.', 'Plasmolysed: cytoplasm/membrane pulled away from the cell wall, small vacuole.', 'Plasmolysis described (A1).', 1),
        ('Explain why the cylinders were all cut to the same length and diameter.', 'Surface area affects the rate of osmosis, so it must be kept constant for a fair comparison.', 'Surface area affects rate (A1); controlled variable (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch09-st2', _osmosis_dq)

pct_items(R, 'ch09-st2', [
    ('A beetroot cylinder had a mass of {a} g before and {b} g after 30 minutes in a sucrose solution.', 'g', 1.5, 3.0, -0.25, 0.2, 2, 'mass gain = water entered by osmosis (solution hypotonic); mass loss = water left (hypertonic).'),
    ('The volume of a red blood cell changed from {a} µm³ to {b} µm³ when it was placed in a salt solution.', 'µm³', 85, 95, -0.35, 0.3, 0, 'water moves by osmosis into the cell if the solution is hypotonic and out of it if hypertonic.'),
    ('The length of a strip of onion epidermis tissue changed from {a} mm to {b} mm after an hour in a sugar solution.', 'mm', 30, 50, -0.12, 0.08, 1, 'cells become turgid and expand slightly in hypotonic solutions, or lose turgor and shrink in hypertonic solutions.'),
])

S('ch09-st3',
  terms=[('active transport', 'the movement of particles across a membrane against their concentration gradient using energy from ATP and specific pump proteins'),
         ('pump protein', 'a membrane protein that uses energy (usually from ATP hydrolysis) to move specific particles against their concentration gradient'),
         ('sodium–potassium pump', 'a pump protein that uses one ATP to move three Na⁺ ions out of the cell and two K⁺ ions into it'),
         ('endocytosis', 'the uptake of material into a cell by the plasma membrane folding inwards to form a vesicle'),
         ('exocytosis', 'the release of material from a cell by fusion of a vesicle with the plasma membrane'),
         ('phagocytosis', 'a type of endocytosis in which a cell engulfs large particles such as bacteria')],
  facts=[('How many sodium ions does the sodium–potassium pump move out of the cell per ATP used?', 'three', ['two', 'one', 'four'], '3 Na⁺ out, 2 K⁺ in.'),
         ('Which organelle produces most of the ATP used for active transport in root hair cells?', 'mitochondrion', ['chloroplast', 'ribosome', 'nucleus'], 'Aerobic respiration supplies ATP.'),
         ('Which process releases digestive enzymes from pancreatic cells?', 'exocytosis', ['endocytosis', 'osmosis', 'simple diffusion'], 'Secretory vesicles fuse with the membrane.'),
         ('Which property of membranes allows vesicles to form and fuse?', 'fluidity of the phospholipid bilayer', ['rigidity of the membrane', 'presence of a cell wall', 'impermeability to water'], 'The bilayer can bend and reseal.')],
  mc2=[('Why does active transport stop if a cell is treated with cyanide, a respiratory poison?', 'ATP production stops, so pumps have no energy source.', ['Cyanide blocks osmosis.', 'Cyanide makes membranes impermeable.', 'Cyanide increases diffusion.'], 'Active transport depends on ATP.'),
       ('Which distinguishes active transport from facilitated diffusion?', 'Active transport moves substances against their concentration gradient using ATP.', ['Only facilitated diffusion uses proteins.', 'Active transport is always faster.', 'Facilitated diffusion uses ATP.'], 'Both use specific proteins; only active transport needs energy.'),
       ('How does the sodium–potassium pump create a membrane potential?', 'It moves more positive charge out (3 Na⁺) than in (2 K⁺).', ['It moves negative ions out.', 'It moves equal numbers of ions each way.', 'It lets K⁺ diffuse in.'], 'Net export of one positive charge per cycle.')],
  mc3=[('Root hair cells take up nitrate ions even when the soil concentration is lower than inside the cells. Uptake stops when oxygen is removed. What does this show?', 'Nitrate is taken up by active transport, which needs ATP from aerobic respiration.', ['Nitrate enters by osmosis.', 'Nitrate enters by simple diffusion.', 'Oxygen carries nitrate into cells.'], 'Uptake against a gradient dependent on respiration.'),
       ('A neurone has 1.2 × 10⁶ sodium–potassium pumps each completing 100 cycles per second. How many K⁺ ions enter per second?', '2.4 × 10⁸', ['3.6 × 10⁸', '1.2 × 10⁸', '1.2 × 10⁶'], '1.2 × 10⁶ × 100 × 2 = 2.4 × 10⁸.')],
  why=[('Explain how the sodium–potassium pump works.', 'Three Na⁺ bind from inside; ATP is hydrolysed and the pump is phosphorylated; it changes shape, releasing Na⁺ outside; two K⁺ bind from outside; the phosphate is released and the pump returns to its original shape, releasing K⁺ inside.'),
       ('Explain how endocytosis and exocytosis depend on the fluidity of membranes.', 'Phospholipids move freely so the membrane can bend; in endocytosis it folds inward and pinches off to form a vesicle; in exocytosis a vesicle membrane fuses with the plasma membrane and becomes part of it; both require energy (ATP).')],
  contrast=[('endocytosis', 'exocytosis', 'Endocytosis takes material into the cell by infolding of the plasma membrane to form a vesicle; exocytosis releases material by fusion of a vesicle with the plasma membrane.'),
            ('active transport', 'passive transport', 'Active transport moves substances against a concentration gradient using ATP and pump proteins; passive transport (diffusion, facilitated diffusion, osmosis) moves substances down a gradient without ATP.')],
  misc=[('Active transport moves substances from high to low concentration.', 'Active transport moves substances from low to high concentration, against the gradient, using energy.'),
        ('Endocytosis does not require energy because the membrane is fluid.', 'Endocytosis and exocytosis require ATP to reshape the membrane and move vesicles, though they depend on membrane fluidity.')],
  cases=[('phagocytosis of bacteria by neutrophils', 'Neutrophils extend the membrane around bacteria and enclose them in a vesicle that fuses with lysosomes.', 'endocytosis', 'Membrane fluidity allows the engulfing of large particles, which are then digested.'),
         ('insulin secretion by β cells of the pancreas', 'Insulin is packaged in vesicles by the Golgi apparatus and released by exocytosis when blood glucose rises.', 'exocytosis', 'Vesicle fusion with the plasma membrane releases the protein outside the cell without it crossing the bilayer.')],
  evaluate=[('Active transport is the most important membrane transport mechanism in cells.', ['it creates the ion gradients needed for nerve impulses, secondary transport and osmotic control', 'it allows uptake of mineral ions against gradients'], ['most gas exchange and water movement depend on passive processes', 'active transport uses a large share of cell energy, so passive mechanisms are more economical'], 'Active transport is essential for establishing gradients, but cells depend on a combination of passive and active processes.')],
  extended=[('Compare active transport with passive transport and explain the role of the sodium–potassium pump in animal cells.', 'Active: against gradient, ATP, pump proteins, specific; passive: down gradient, no ATP, diffusion/facilitated/osmosis. Na/K pump: 3 Na⁺ out, 2 K⁺ in per ATP, phosphorylation and conformational change; maintains resting potential, controls cell volume, drives secondary active transport (e.g. Na–glucose cotransport).', 7)],
  )


@R.add('ch09-st3', 'C3', (2, 5), 'numerical')
def pump_calc(rng, slot):
    pumps = pick(rng, [5e5, 1e6, 2e6, 4e6])
    rate = pick(rng, [50, 80, 100, 150])
    secs = pick(rng, [1, 10, 60])
    cyc = pumps * rate * secs
    cell = pick(rng, ['a squid giant axon segment', 'a kidney tubule cell', 'a mammalian neurone', 'a red blood cell'])
    stem = f'{cell[0].upper() + cell[1:]} has {sf(pumps)} sodium–potassium pumps, each completing {rate} cycles per second. In {secs} s calculate the number of Na⁺ ions pumped out, the number of K⁺ ions pumped in and the number of ATP molecules used.'
    return num(stem, f'Na⁺ {sf(3 * cyc)}; K⁺ {sf(2 * cyc)}; ATP {sf(cyc)}', f'Cycles = {sf(pumps)} × {rate} × {secs} = {sf(cyc)} (M1); 3 Na⁺ out, 2 K⁺ in, 1 ATP per cycle (A1 A1).', 3)


S('ch09-st4',
  terms=[('membrane fluidity', 'the ease with which phospholipids and proteins move within a membrane, affected by temperature, fatty acid saturation and cholesterol'),
         ('cholesterol', 'a steroid found between phospholipids in animal membranes that regulates fluidity and reduces permeability to small polar molecules'),
         ('voltage-gated channel', 'an ion channel that opens or closes in response to changes in membrane potential, e.g. sodium and potassium channels in axons'),
         ('ligand-gated channel', 'an ion channel that opens when a specific chemical (ligand) binds, e.g. the nicotinic acetylcholine receptor'),
         ('homeoviscous adaptation', 'changes in membrane lipid composition, such as more unsaturated fatty acids in the cold, that maintain membrane fluidity')],
  facts=[('Which component of animal membranes acts as a fluidity buffer?', 'cholesterol', ['cellulose', 'glycogen', 'chlorophyll'], 'It restrains movement at high temperature and prevents packing at low temperature.'),
         ('Which channel opens when acetylcholine binds at a neuromuscular junction?', 'a ligand-gated (nicotinic acetylcholine) channel', ['a voltage-gated potassium channel', 'an aquaporin', 'the sodium–potassium pump'], 'Binding opens a cation channel.'),
         ('Which ion channels open in response to depolarisation of an axon membrane?', 'voltage-gated Na⁺ channels', ['ligand-gated Cl⁻ channels', 'aquaporins', 'glucose carriers'], 'Na⁺ influx generates the action potential.'),
         ('Membranes of cold-water fish contain a higher proportion of which fatty acids?', 'unsaturated fatty acids', ['saturated fatty acids', 'trans fatty acids', 'no fatty acids'], 'Kinks maintain fluidity in the cold.')],
  mc2=[('How does cholesterol reduce membrane fluidity at body temperature?', 'Its rigid rings restrict the movement of phospholipid tails.', ['It forms covalent bonds with proteins.', 'It is hydrophilic and attracts water.', 'It increases the number of double bonds.'], 'Rings interact with the upper parts of the tails.'),
       ('Why does a membrane become more permeable at high temperatures?', 'Phospholipids move more and the bilayer becomes more fluid, with gaps forming.', ['Proteins are added to the membrane.', 'Cholesterol increases.', 'Water freezes in the membrane.'], 'Increased kinetic energy disrupts packing.'),
       ('Why do gated channels allow cells to control ion movement?', 'They open only in response to a specific signal (voltage or ligand), so movement can be switched on and off.', ['They are always open.', 'They use ATP to move ions.', 'They allow all ions through.'], 'Gating gives control.')],
  mc3=[('Beetroot discs were heated at different temperatures and the red pigment leaking into water was measured. Above 50 °C leakage rose sharply. What is the best explanation?', 'Membranes become more fluid and proteins denature, so membranes lose their barrier function.', ['Pigment is made at high temperatures.', 'Cell walls dissolve.', 'The pigment is actively pumped out.'], 'Classic membrane permeability experiment.'),
       ('Bacteria grown at 10 °C have more unsaturated membrane fatty acids than those grown at 37 °C. What is the most likely reason?', 'to keep the membrane fluid at low temperature', ['to make the membrane rigid in the cold', 'to store energy', 'to increase osmosis'], 'Homeoviscous adaptation.')],
  why=[('Explain how the fatty acid composition of membranes affects their fluidity.', 'Unsaturated fatty acids have cis double bonds causing kinks; they cannot pack closely, so the membrane is more fluid; saturated fatty acids are straight, pack tightly and make membranes more viscous; organisms adjust composition to temperature.'),
       ('Explain the role of cholesterol in animal cell membranes.', 'Cholesterol fits between phospholipids; at body temperature its rigid rings restrict tail movement, reducing fluidity and permeability to small polar molecules and ions; at low temperatures it prevents tails packing tightly, so fluidity is maintained – it buffers fluidity.'),
       ('Explain the difference between voltage-gated and ligand-gated ion channels.', 'Voltage-gated channels change shape and open when the membrane potential changes (e.g. Na⁺/K⁺ channels in axons); ligand-gated channels open when a specific molecule binds to a receptor site on the channel (e.g. acetylcholine receptor at synapses).')],
  contrast=[('voltage-gated channels', 'ligand-gated channels', 'Voltage-gated channels open in response to a change in membrane potential; ligand-gated channels open when a specific signal molecule binds.')],
  misc=[('Cholesterol always makes membranes more rigid.', 'Cholesterol buffers fluidity: it reduces fluidity at higher temperatures but prevents excessive rigidity at low temperatures.'),
        ('Gated channels pump ions using ATP.', 'Gated channels allow passive facilitated diffusion when open; they do not use ATP. Pumps use ATP.')],
  cases=[('the nicotinic acetylcholine receptor at the neuromuscular junction', 'Binding of two acetylcholine molecules opens a central pore allowing Na⁺ to flow into the muscle fibre.', 'ligand-gated ion channels', 'A specific ligand changes the protein’s shape, opening the channel and depolarising the membrane.'),
         ('Antarctic icefish living at −1.9 °C', 'Their membranes contain a high proportion of polyunsaturated fatty acids.', 'adaptations that maintain membrane fluidity', 'Kinked unsaturated chains prevent membranes becoming rigid at freezing temperatures.')],
  evaluate=[('Cholesterol is harmful and should be removed from the diet completely.', ['high blood LDL cholesterol is linked to atherosclerosis and heart disease', 'reducing saturated fat and cholesterol intake lowers risk for many people'], ['cholesterol is an essential membrane component and precursor of steroid hormones and vitamin D', 'the liver synthesises most of the body’s cholesterol regardless of diet'], 'Cholesterol is essential; the concern is excessive LDL levels, so diet should limit, not eliminate, it.')],
  extended=[('Explain how membrane fluidity is controlled and why gated ion channels are important.', 'Fluidity: temperature; saturated vs unsaturated fatty acids (kinks); cholesterol buffers; homeoviscous adaptation. Importance: endocytosis, protein movement, function of membrane proteins. Gated channels: voltage-gated Na⁺/K⁺ in action potentials; ligand-gated (acetylcholine) at synapses; passive, specific, controlled opening.', 7)],
  )


def _beet_dq(rng, slot):
    temps = [20, 30, 40, 50, 60, 70, 80]
    t50 = rng.uniform(52, 60)
    absb = [round(0.05 + 0.9 / (1 + math.exp(-(t - t50) / 4)) * rng.uniform(0.95, 1.05), 2) for t in temps]
    reps = [[round(a * rng.uniform(0.9, 1.1), 2) for _ in range(3)] for a in absb]
    means = [mean(r) for r in reps]
    i = rng.randrange(2, 6)
    pc = pct_change(means[1], means[-1])
    intro = ('Beetroot discs of equal size were washed, then placed in water at different temperatures for 15 minutes. The absorbance of the water (a measure of red betalain pigment leaking from the vacuoles) was measured with a colorimeter. Three discs were used at each temperature.\n\n'
             + table(['Temperature / °C', 'Absorbance 1', 'Absorbance 2', 'Absorbance 3'], [(t, *[f'{x:.2f}' for x in r]) for t, r in zip(temps, reps)]))
    parts = [
        (f'Calculate the mean absorbance at {temps[i]} °C.', f'{means[i]:.2f}', f'({" + ".join(f"{x:.2f}" for x in reps[i])})/3 = {means[i]:.2f} (A1).', 1),
        (f'Calculate the standard deviation of the absorbance readings at {temps[i]} °C.', f'{sd(reps[i]):.3f}', f'SD (n − 1) = {sd(reps[i]):.3f} (A1); accept population SD.', 1),
        ('Calculate the percentage increase in mean absorbance between 30 °C and 80 °C.', f'{pc:.0f} %', f'Means {means[1]:.2f} and {means[-1]:.2f} (M1); ({means[-1]:.2f} − {means[1]:.2f})/{means[1]:.2f} × 100 = {pc:.0f} % (A1).', 2),
        ('Describe the trend shown by the data.', f'Little pigment leaks below about {int(t50 // 10 * 10 - 10)} °C; absorbance increases sharply between about {int(t50 // 10 * 10 - 10)} and {int(t50 // 10 * 10 + 10)} °C, then levels off.', 'Low at low temperatures (A1); steep rise at a stated range (A1).', 2),
        ('Explain the sharp increase in pigment leakage at higher temperatures.', 'Phospholipids gain kinetic energy and the bilayer becomes more fluid/disordered; membrane proteins denature, leaving gaps; the tonoplast and plasma membrane become permeable and pigment leaks out.', 'Increased fluidity (A1); protein denaturation (A1); membranes lose barrier function (A1).', 3),
        ('Explain why the discs were washed before the experiment.', 'To remove pigment released from cells cut during preparation, so only leakage during the experiment is measured.', 'Remove pigment from cut cells (A1).', 1),
        ('Suggest how the experiment could be modified to investigate the effect of ethanol on membranes.', 'Use a range of ethanol concentrations at a constant temperature; same disc size, time and volume; measure absorbance.', 'IV ethanol concentration with temperature controlled (A1); same DV method (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch09-st4', _beet_dq)


# =============================================================================================
# ch10 B2.2 Organelles and compartmentalisation; B2.3 Cell specialisation
# =============================================================================================
S('ch10-st1',
  terms=[('organelle', 'a discrete subunit of a cell that is adapted to perform a specific function'),
         ('nuclear envelope', 'the double membrane surrounding the nucleus, perforated by nuclear pores'),
         ('nuclear pore', 'a protein-lined opening in the nuclear envelope that controls movement of molecules such as mRNA between nucleus and cytoplasm'),
         ('lysosome', 'a membrane-bound vesicle containing hydrolytic enzymes at low pH, used to digest materials'),
         ('Golgi apparatus', 'a stack of flattened membrane sacs that modifies, sorts and packages proteins into vesicles'),
         ('cell fractionation', 'the separation of organelles by homogenising cells and centrifuging at increasing speeds (differential centrifugation)')],
  facts=[('Which structure is not usually considered an organelle because it is not a discrete subunit?', 'the cytoplasm', ['the nucleus', 'the mitochondrion', 'the Golgi apparatus'], 'The cytoskeleton, cell wall and cytoplasm are not counted as organelles.'),
         ('Where are proteins for secretion synthesised?', 'on ribosomes attached to the rough endoplasmic reticulum', ['on free ribosomes', 'in the nucleolus', 'in lysosomes'], 'They enter the ER lumen for processing.'),
         ('In differential centrifugation, which organelles sediment first at low speed?', 'nuclei', ['ribosomes', 'mitochondria', 'lysosomes'], 'Larger, denser organelles pellet first.'),
         ('What is the advantage of separating transcription in the nucleus from translation in the cytoplasm?', 'mRNA can be modified (e.g. intron removal) before translation', ['translation is faster in the nucleus', 'ribosomes can enter the nucleus', 'DNA can be translated directly'], 'Prokaryotes translate mRNA while it is still being transcribed.')],
  mc2=[('Why are hydrolytic enzymes kept inside lysosomes?', 'They would digest the cell’s own components if released, and they work best at the low pH inside lysosomes.', ['They are too large to leave.', 'They are made in lysosomes.', 'They only work in the cytoplasm.'], 'Compartmentalisation protects the cell.'),
       ('Why is the homogenate in cell fractionation kept ice-cold, isotonic and buffered?', 'To reduce enzyme activity, prevent osmotic damage to organelles and prevent denaturation by pH changes.', ['To speed up enzyme reactions.', 'To make organelles burst.', 'To kill bacteria.'], 'Each condition protects organelles.'),
       ('Which pathway is followed by a protein secreted by a pancreatic cell?', 'rough ER → Golgi apparatus → vesicle → plasma membrane', ['nucleus → lysosome → plasma membrane', 'Golgi → rough ER → nucleus', 'mitochondrion → Golgi → vesicle'], 'The secretory pathway.')],
  mc3=[('A cell is treated with a drug that blocks nuclear pores. Which process is most directly affected?', 'export of mRNA to the ribosomes in the cytoplasm', ['ATP synthesis in mitochondria', 'diffusion of O₂ into the cell', 'DNA replication'], 'mRNA leaves via pores.'),
       ('Mutations that prevent enzymes being tagged for delivery to lysosomes cause I-cell disease, in which undigested material accumulates. What does this show?', 'Correct targeting of proteins to compartments is essential for their function.', ['Lysosomes are not needed by cells.', 'The enzymes are made in lysosomes.', 'The nucleus digests material.'], 'Enzymes are secreted instead of reaching lysosomes.')],
  why=[('Explain the advantages of compartmentalisation in eukaryotic cells.', 'Enzymes and substrates can be concentrated in a small volume; incompatible reactions or conditions (e.g. low pH in lysosomes) are separated; damaging substances are isolated; membranes provide surfaces for enzymes and gradients (e.g. in mitochondria).'),
       ('Explain the advantage of separating the nucleus from the cytoplasm.', 'Transcription and translation are separated, so mRNA can be processed (introns removed, cap and tail added) before translation; DNA is protected from cytoplasmic enzymes and movement; gene expression can be regulated by controlling export through nuclear pores.'),
       ('Explain how organelles can be separated by cell fractionation.', 'Tissue is homogenised in cold, isotonic, buffered solution; filtered; centrifuged at increasing speeds; the densest/largest organelles (nuclei) form a pellet first, then mitochondria and chloroplasts, then lysosomes and ER, then ribosomes; each pellet can be studied.')],
  contrast=[('free ribosomes', 'ribosomes bound to rough ER', 'Free ribosomes make proteins used within the cytoplasm; ribosomes on rough ER make proteins that enter the ER for secretion, insertion in membranes or delivery to lysosomes.')],
  misc=[('Prokaryotes are inefficient because they lack a nucleus.', 'Prokaryotes are highly successful; without a nucleus they can transcribe and translate simultaneously and respond rapidly, though they cannot process mRNA in the same way.'),
        ('The Golgi apparatus makes proteins.', 'Proteins are made on ribosomes; the Golgi modifies (e.g. glycosylates), sorts and packages them.')],
  cases=[('pancreatic acinar cells secreting digestive enzymes', 'Radioactive amino acids traced by Palade appeared first in rough ER, then the Golgi, then secretory vesicles.', 'the secretory pathway and compartmentalisation', 'The sequence of organelles shows how proteins are made, processed and packaged in separate compartments.'),
         ('Tay–Sachs disease', 'A missing lysosomal enzyme (hexosaminidase A) causes lipids to accumulate in neurones.', 'the role of lysosomes', 'Lysosomes contain specific hydrolases; if one is absent, its substrate builds up and damages cells.')],
  evaluate=[('Compartmentalisation explains the success of eukaryotic cells.', ['it allows larger cells with specialised, efficient internal environments', 'it underpins multicellularity and complex regulation'], ['prokaryotes are more numerous and metabolically diverse, and thrive without it', 'compartments add energy costs for transport between them'], 'Compartmentalisation enabled eukaryotic complexity, but “success” can also be measured by abundance and diversity, where prokaryotes excel.')],
  extended=[('Explain how compartmentalisation within eukaryotic cells is related to the functions of named organelles.', 'Nucleus: separates transcription/translation, mRNA processing; RER/ribosomes: protein synthesis for secretion; Golgi: modification and packaging; lysosomes: hydrolases at low pH, isolated; mitochondria: respiration, proton gradient across inner membrane; chloroplasts; vesicles; advantages: concentration, separation, gradients.', 8)],
  )

S('ch10-st2',
  terms=[('cristae', 'the folds of the inner mitochondrial membrane, which increase the surface area for electron transport and ATP synthase'),
         ('matrix', 'the fluid inside the inner mitochondrial membrane containing enzymes of the link reaction and Krebs cycle, 70S ribosomes and DNA'),
         ('thylakoid', 'a flattened membrane sac in the chloroplast containing photosystems and ATP synthase, where light-dependent reactions occur'),
         ('granum', 'a stack of thylakoids in a chloroplast'),
         ('stroma', 'the fluid surrounding the thylakoids in a chloroplast, containing enzymes of the Calvin cycle'),
         ('intermembrane space', 'the narrow space between the inner and outer mitochondrial membranes where protons accumulate')],
  facts=[('Where in the mitochondrion is the electron transport chain located?', 'on the inner membrane (cristae)', ['in the matrix', 'on the outer membrane', 'in the intermembrane space only'], 'Proteins of the ETC and ATP synthase are embedded in cristae.'),
         ('Where does the Calvin cycle take place?', 'in the stroma', ['in the thylakoid membranes', 'in the intermembrane space', 'in the cytoplasm'], 'Rubisco is in the stroma.'),
         ('Which feature increases the surface area for light absorption in chloroplasts?', 'many thylakoids stacked into grana', ['a single outer membrane', 'a large central vacuole', 'starch grains'], 'More membrane holds more photosystems.'),
         ('Why is the intermembrane space of the mitochondrion small?', 'so a high proton concentration builds up quickly', ['to store ATP', 'to hold DNA', 'to store glucose'], 'A steep gradient drives chemiosmosis.')],
  mc2=[('Why do cells with high energy demands, such as sperm and muscle, have many mitochondria with many cristae?', 'More cristae provide more surface for the ETC and ATP synthase, producing more ATP.', ['Cristae store glucose.', 'Cristae contain chlorophyll.', 'Cristae make proteins for export.'], 'Structure–function link.'),
       ('Which shared feature of mitochondria and chloroplasts is an adaptation for chemiosmosis?', 'a membrane that encloses a small space where protons accumulate', ['a cell wall', 'a nucleus', 'a large vacuole'], 'Thylakoid lumen and intermembrane space.'),
       ('Why does the stroma contain 70S ribosomes and DNA?', 'Chloroplasts make some of their own proteins.', ['The stroma is part of the nucleus.', 'Ribosomes store starch.', 'DNA absorbs light.'], 'Also evidence for endosymbiosis.')],
  mc3=[('An electron micrograph of a mitochondrion at × 40 000 shows it as 60 mm long. What is its actual length?', '1.5 µm', ['15 µm', '0.15 µm', '2.4 µm'], '60 000 µm ÷ 40 000 = 1.5 µm.'),
       ('Mitochondria from heart muscle have more densely packed cristae than those from liver. Which prediction follows?', 'Heart mitochondria have a higher rate of oxidative phosphorylation per mitochondrion.', ['Liver mitochondria make more ATP per mitochondrion.', 'Heart mitochondria lack DNA.', 'Heart mitochondria photosynthesise.'], 'More membrane area = more ATP synthase.')],
  why=[('Explain how the structure of the mitochondrion is adapted to its function.', 'Double membrane: outer controls entry; inner folded into cristae with large surface area for ETC and ATP synthase; small intermembrane space allows a steep proton gradient; matrix contains enzymes of the link reaction and Krebs cycle; own DNA and ribosomes to make some proteins.'),
       ('Explain how the structure of the chloroplast is adapted to photosynthesis.', 'Thylakoid membranes stacked in grana give large area for photosystems and pigments; small thylakoid lumen accumulates protons for chemiosmosis; stroma contains Calvin cycle enzymes (rubisco) close to the products of light reactions; starch grains store products; own DNA and ribosomes.')],
  contrast=[('the matrix of a mitochondrion', 'the stroma of a chloroplast', 'The matrix contains enzymes of the link reaction and Krebs cycle; the stroma contains enzymes of the Calvin cycle; both are fluid compartments with DNA and 70S ribosomes.'),
            ('cristae', 'thylakoids', 'Cristae are folds of the inner mitochondrial membrane holding the ETC for respiration; thylakoids are separate internal membrane sacs of the chloroplast holding photosystems for the light-dependent reactions.')],
  misc=[('Chloroplasts are found in all plant cells and produce all their ATP.', 'Many plant cells (e.g. roots) lack chloroplasts; plant cells use mitochondria for respiratory ATP; chloroplast ATP is mainly used in the Calvin cycle.'),
        ('The outer mitochondrial membrane is folded into cristae.', 'It is the inner membrane that is folded into cristae.')],
  cases=[('flight muscle of hummingbirds', 'Mitochondria occupy about 35 % of muscle fibre volume and have very dense cristae.', 'the structure–function relationship of mitochondria', 'Extensive cristae maximise ATP production to power wingbeats of up to 80 per second.'),
         ('shade leaves compared with sun leaves', 'Chloroplasts in shade leaves have larger grana with more thylakoids.', 'the structure–function relationship of chloroplasts', 'More thylakoid membrane holds more light-harvesting pigment, capturing more of the limited light.')],
  evaluate=[('The structures of mitochondria and chloroplasts are adapted mainly for chemiosmosis.', ['both have membranes enclosing small spaces where proton gradients build up and ATP synthase is embedded', 'membrane folding/stacking maximises area for these proteins'], ['other features (matrix and stroma enzymes, DNA, ribosomes) are adapted for other stages and for self-maintenance', 'their double membranes reflect endosymbiotic origin as well as function'], 'Chemiosmosis explains many shared features, but each organelle’s structure reflects several functions and its evolutionary history.')],
  extended=[('Compare the structure of mitochondria and chloroplasts and explain how each is adapted to its function.', 'Both: double membrane, own DNA, 70S ribosomes, internal membranes with ATP synthase, proton gradients. Mitochondria: cristae, matrix (Krebs), small intermembrane space. Chloroplasts: thylakoids/grana with pigments, lumen, stroma (Calvin), starch grains. Adaptations explained.', 8)],
  )

S('ch10-st3',
  terms=[('stem cell', 'an unspecialised cell that can divide repeatedly and differentiate into specialised cell types'),
         ('differentiation', 'the process by which unspecialised cells become specialised for a particular function by expressing particular genes'),
         ('totipotent', 'describes a stem cell able to differentiate into any cell type, including extra-embryonic tissues (e.g. the zygote)'),
         ('pluripotent', 'describes a stem cell that can differentiate into any cell type of the body, but not the placenta (e.g. embryonic stem cells)'),
         ('multipotent', 'describes a stem cell able to differentiate into a limited range of related cell types (e.g. bone marrow stem cells)'),
         ('stem cell niche', 'the specific microenvironment in the body that maintains stem cells and regulates their proliferation and differentiation')],
  facts=[('Which cells are totipotent?', 'the zygote and early cells of the morula', ['bone marrow stem cells', 'neurones', 'skin cells'], 'They can form embryo and placenta.'),
         ('Where is a stem cell niche found in adult humans?', 'the bone marrow', ['the lens of the eye', 'mature red blood cells', 'the enamel of teeth'], 'Bone marrow and hair follicles contain niches.'),
         ('What causes cells with the same genome to differentiate into different types?', 'different genes are expressed in different cells', ['cells lose different genes', 'mutations occur in each cell', 'cells gain new chromosomes'], 'Gene expression determines cell type.'),
         ('Which type of stem cell is used in bone marrow transplants for leukaemia?', 'haematopoietic (blood-forming) stem cells', ['embryonic stem cells', 'neural stem cells', 'meristem cells'], 'They are multipotent.')],
  mc2=[('Why are embryonic stem cells potentially more useful in therapy than adult stem cells?', 'They are pluripotent and can form any body cell type.', ['They are always genetically identical to the patient.', 'They are multipotent.', 'They do not divide.'], 'Adult stem cells are more limited.'),
       ('Why can induced pluripotent stem cells reduce ethical concerns?', 'They are made from adult body cells, so no embryo is destroyed.', ['They are taken from embryos.', 'They are totipotent.', 'They cannot divide.'], 'Reprogramming adult cells.'),
       ('Which statement explains how stem cells contribute to tissue repair?', 'They divide to replace cells and differentiate into the needed types.', ['They fuse with damaged cells.', 'They secrete new DNA.', 'They become cancer cells.'], 'Self-renewal plus differentiation.')],
  mc3=[('A patient’s own skin cells are reprogrammed into iPS cells and differentiated into retinal cells to treat macular degeneration. What is a key advantage?', 'The cells are genetically identical to the patient, so rejection is avoided.', ['No differentiation is needed.', 'The cells are totipotent.', 'The cells can never become cancerous.'], 'Autologous cells match the immune system.'),
       ('Hair follicles contain a niche that cycles between growth and rest. Damage to the niche would most likely cause', 'loss of hair regeneration', ['more pigment', 'faster hair growth permanently', 'differentiation into neurones'], 'Stem cells need their niche.')],
  why=[('Explain how differentiation results from gene expression.', 'All body cells contain the same genes; during differentiation specific genes are switched on (transcribed) and others off, so each cell type makes particular proteins that give it its structure and function; patterns are controlled by signals and transcription factors.'),
       ('Explain the properties of stem cells that make them useful in medicine.', 'They can self-renew (divide repeatedly) and differentiate into specialised cells; so they can replace damaged tissues (e.g. bone marrow transplants, potential treatment of diabetes or Parkinson’s); pluripotent cells have the widest potential.')],
  contrast=[('totipotent stem cells', 'pluripotent stem cells', 'Totipotent cells (zygote) can form all cell types including the placenta; pluripotent cells (embryonic stem cells) can form all body cell types but not extra-embryonic tissues.'),
            ('pluripotent stem cells', 'multipotent stem cells', 'Pluripotent cells can form any body cell type; multipotent cells can only form a limited range of related types, e.g. blood cells from bone marrow stem cells.')],
  misc=[('Specialised cells contain only the genes they need.', 'Specialised cells contain the full genome; they differ in which genes are expressed.'),
        ('Adult stem cells can become any cell type.', 'Most adult stem cells are multipotent, forming only related cell types.')],
  cases=[('bone marrow transplants for leukaemia', 'Haematopoietic stem cells from a matched donor repopulate the patient’s marrow after chemotherapy.', 'the therapeutic use of stem cells', 'Multipotent donor stem cells self-renew and differentiate into all blood cell types.'),
         ('Shinya Yamanaka’s production of induced pluripotent stem cells (2006)', 'Four transcription factors reprogrammed adult mouse skin cells into pluripotent cells.', 'gene expression in differentiation', 'Switching on specific genes reversed differentiation, showing cell identity depends on gene expression.')],
  evaluate=[('The use of embryonic stem cells in research is ethically justified.', ['potential to treat serious diseases such as Parkinson’s and diabetes', 'surplus IVF embryos would otherwise be discarded'], ['destruction of embryos that some consider to have moral status', 'iPS cells offer alternatives without embryo destruction'], 'Many societies permit regulated research on surplus embryos for serious medical aims; the availability of iPS cells weakens but does not eliminate the case.')],
  extended=[('Explain the properties and types of stem cells and discuss their therapeutic uses.', 'Self-renewal, differentiation; totipotent, pluripotent, multipotent; niches (bone marrow, hair follicle); differentiation by gene expression; uses: bone marrow transplants, skin grafts, research on iPS-derived cells; issues: ethics of embryos, rejection, tumour risk.', 8)],
  )

S('ch10-st4',
  terms=[('surface area-to-volume ratio', 'the surface area of a cell or organism divided by its volume; it decreases as size increases'),
         ('type I pneumocyte', 'an extremely thin alveolar cell adapted for gas exchange by diffusion'),
         ('type II pneumocyte', 'an alveolar cell that secretes surfactant to reduce surface tension'),
         ('striated muscle fibre', 'a long multinucleate muscle cell with repeating sarcomeres, formed by fusion of many cells'),
         ('microvilli', 'finger-like projections of the plasma membrane that increase surface area for absorption')],
  facts=[('As a cube-shaped cell increases in size, what happens to its SA:V ratio?', 'it decreases', ['it increases', 'it stays the same', 'it doubles'], 'Volume grows faster than area.'),
         ('Which cell is the largest in the human body?', 'the ovum (egg cell)', ['the sperm cell', 'the red blood cell', 'the lymphocyte'], 'About 110 µm in diameter.'),
         ('Why are type I pneumocytes very thin?', 'to minimise the diffusion distance for gases', ['to store surfactant', 'to divide rapidly', 'to absorb nutrients'], 'About 0.15 µm thick.'),
         ('Why do sperm cells contain many mitochondria in their midpiece?', 'to supply ATP for the movement of the flagellum', ['to store food for the embryo', 'to make enzymes', 'to make the cell heavier'], 'Swimming requires much ATP.')],
  mc2=[('Why does a low SA:V ratio limit cell size?', 'Exchange across the surface becomes too slow to supply the larger volume’s metabolic needs.', ['Large cells cannot contain DNA.', 'Volume decreases with size.', 'Membranes cannot stretch.'], 'Rate of exchange ∝ area; demand ∝ volume.'),
       ('Why is the egg cell much larger than the sperm cell?', 'It contains food reserves and organelles for the early embryo.', ['It must swim.', 'It has more chromosomes.', 'It needs a small SA:V ratio for diffusion.'], 'Sperm is streamlined; egg stores yolk/cytoplasm.'),
       ('How do flattened or elongated shapes help large cells?', 'They increase the SA:V ratio and shorten diffusion distances.', ['They decrease SA:V ratio.', 'They reduce the amount of membrane.', 'They make cells divide less often.'], 'Shape compensates for size.')],
  mc3=[('Agar cubes of side 1 cm, 2 cm and 3 cm containing indicator are placed in acid. Which cube becomes completely coloured first, and why?', 'the 1 cm cube, because it has the highest SA:V ratio and shortest distance to the centre', ['the 3 cm cube, because it has the largest surface area', 'all at the same time', 'the 2 cm cube'], 'SA:V 6, 3 and 2 cm⁻¹.'),
       ('A spherical cell has a radius of 10 µm. What is its SA:V ratio?', '0.3 µm⁻¹', ['3 µm⁻¹', '0.1 µm⁻¹', '30 µm⁻¹'], 'SA:V of a sphere = 3/r = 0.3.')],
  why=[('Explain why cells divide rather than continuing to grow larger.', 'As size increases volume (metabolic demand) rises faster than surface area (exchange), so SA:V falls; diffusion distances to the centre increase; above a certain size the cell cannot exchange materials or remove waste quickly enough, so division keeps cells small with high SA:V.'),
       ('Explain how the structure of type I and type II pneumocytes is related to their functions.', 'Type I: extremely thin, flattened, cover most of the alveolar surface, minimising diffusion distance for gas exchange; type II: cuboidal, with many lamellar bodies that secrete surfactant, reducing surface tension so alveoli do not collapse.'),
       ('Explain how the structure of sperm and egg cells relates to their functions.', 'Sperm: small, streamlined, flagellum for swimming, many mitochondria for ATP, acrosome with enzymes to penetrate the egg, haploid nucleus; egg: large with cytoplasm and nutrients for early development, zona pellucida and cortical granules to prevent polyspermy, haploid nucleus.')],
  contrast=[('a sperm cell', 'an egg cell', 'Sperm are small, mobile, with a flagellum, mitochondria and acrosome; eggs are large, non-motile, rich in cytoplasm and nutrients with protective layers; both are haploid.'),
            ('cardiac muscle', 'striated skeletal muscle', 'Both are striated with sarcomeres; skeletal fibres are long, multinucleate and under voluntary control; cardiac muscle cells are shorter, branched, usually with one nucleus and connected by intercalated discs for coordinated contraction.')],
  misc=[('Larger cells have a larger SA:V ratio because they have more surface.', 'Larger cells have more surface area in absolute terms but a smaller SA:V ratio, because volume increases faster.'),
        ('Muscle fibres are typical cells with one nucleus each.', 'Striated muscle fibres are multinucleate, formed by fusion of many myoblasts.')],
  cases=[('red blood cells', 'Mammalian erythrocytes are biconcave discs about 7.5 µm across and lack a nucleus.', 'the relationship between cell shape, SA:V and function', 'The biconcave shape increases SA:V for rapid O₂ diffusion and lack of nucleus leaves more room for haemoglobin.'),
         ('alveolar pneumocytes in human lungs', 'Type I cells (about 0.15 µm thick) cover about 95 % of alveolar surface; type II cells secrete surfactant.', 'cell specialisation', 'Thin type I cells minimise diffusion distance; type II cells prevent alveolar collapse.')],
  evaluate=[('Surface area-to-volume ratio is the main factor limiting cell size.', ['diffusion rates depend on surface area while demand depends on volume', 'large cells (e.g. neurones, muscle fibres, eggs) have shapes or features that offset low SA:V'], ['the ability of one nucleus to control a large volume of cytoplasm also limits size', 'cytoplasmic streaming and active transport can partly overcome diffusion limits'], 'SA:V is a major constraint, but nuclear control and transport mechanisms also matter; exceptions show how cells adapt around the limit.')],
  extended=[('Explain how SA:V ratio limits cell size and describe how the structures of three named specialised cells are adapted to their functions.', 'SA:V falls with size; exchange vs demand; diffusion distance. Examples: red blood cell (biconcave, no nucleus), type I pneumocyte (thin), type II (surfactant), sperm (flagellum, mitochondria, acrosome), egg (large, nutrients), striated muscle (multinucleate, sarcomeres), cardiac muscle (branched, intercalated discs).', 8)],
  )


@R.add('ch10-st4', 'C3', (1, 5), 'numerical')
def sav(rng, slot):
    f = rng.randrange(3)
    if f == 0:
        s = pick(rng, [1, 2, 3, 4, 5, 6, 8, 10])
        u = pick(rng, ['cm', 'mm', 'µm'])
        sa, v = 6 * s * s, s ** 3
        stem = f'Calculate the surface area, volume and SA:V ratio of a cube of side {s} {u}.'
        if slot.d >= 3:
            s2 = s * 2
            stem = f'A cube-shaped model cell of side {s} {u} doubles its side length to {s2} {u}. Calculate the SA:V ratio before and after, and explain the effect on exchange of materials.'
            return num(stem, f'{sa / v:.2f} {u}⁻¹ → {6 * s2 * s2 / s2 ** 3:.2f} {u}⁻¹; ratio halves, so exchange per unit volume is slower',
                       f'SA = 6s², V = s³ (M1); {sa}/{v} = {sa / v:.2f} and {6 * s2 * s2}/{s2 ** 3} = {6 * s2 * s2 / s2 ** 3:.2f} (A1 A1); less surface per unit volume, longer diffusion distance (R1).', 4)
        return num(stem, f'SA = {sa} {u}², V = {v} {u}³, SA:V = {sa / v:.2f} {u}⁻¹', f'SA = 6 × {s}² = {sa} (A1); V = {s}³ = {v} (A1); ratio {sa / v:.2f} : 1 (A1).', 3)
    if f == 1:
        r = pick(rng, [2, 3.75, 5, 10, 25, 55])
        cell = {2: 'a yeast cell', 3.75: 'a red blood cell (treated as a sphere)', 5: 'a lymphocyte', 10: 'a hepatocyte', 25: 'a pollen grain', 55: 'a human ovum'}[r]
        sa = 4 * math.pi * r * r
        v = 4 / 3 * math.pi * r ** 3
        stem = f'Treating {cell} as a sphere of radius {r} µm, calculate its surface area, volume and SA:V ratio (SA = 4πr², V = 4/3πr³).'
        return num(stem, f'SA = {sf(sa)} µm², V = {sf(v)} µm³, SA:V = {sf(sa / v)} µm⁻¹', f'SA = {sf(sa)} µm² (A1); V = {sf(v)} µm³ (A1); SA:V = 3/r = {sf(3 / r)} µm⁻¹ (A1).', 3)
    l, w, h = pick(rng, [(10, 2, 1), (20, 4, 1), (8, 8, 1), (12, 3, 2), (6, 3, 1)])
    sa = 2 * (l * w + l * h + w * h)
    v = l * w * h
    c = round((v) ** (1 / 3), 2)
    sac = 6 * c * c
    stem = (f'A flattened cell is modelled as a cuboid {l} µm × {w} µm × {h} µm. Calculate its SA:V ratio and compare it with a cube of the same volume (side {c} µm). Explain the advantage of the flattened shape.')
    return num(stem, f'cuboid {sa / v:.2f} µm⁻¹; cube {sac / c ** 3:.2f} µm⁻¹; flattening increases SA:V and reduces diffusion distance',
               f'Cuboid SA = {sa} µm², V = {v} µm³, ratio {sa / v:.2f} (A1); cube ratio 6/{c} = {6 / c:.2f} (A1); higher SA:V / shorter distance to centre (R1).', 3)


def _agar_dq(rng, slot):
    sides = [0.5, 1.0, 1.5, 2.0, 2.5]
    rate = rng.uniform(0.045, 0.06)
    times = [round((s / 2) / rate * rng.uniform(0.95, 1.05) / 60, 1) for s in sides]
    sav_ = [6 / s for s in sides]
    j = rng.randrange(1, 4)
    intro = ('Cubes of agar containing phenolphthalein (pink in alkali) were placed in dilute hydrochloric acid. The time taken for each cube to become completely colourless was recorded.\n\n'
             + table(['Side length / cm', 'SA:V ratio / cm⁻¹', 'Time to decolourise / min'], [(f'{s:.1f}', '?' if i == j else f'{v:.1f}', f'{t:.1f}') for i, (s, v, t) in enumerate(zip(sides, sav_, times))]))
    dist = sides[-1] / 2
    rt = dist / (times[-1])
    parts = [
        (f'Calculate the SA:V ratio of the {sides[j]:.1f} cm cube.', f'{sav_[j]:.1f} cm⁻¹', f'SA = 6 × {sides[j]}² = {6 * sides[j] ** 2:.2f}; V = {sides[j] ** 3:.3f} (M1); ratio {sav_[j]:.1f} (A1).', 2),
        ('Describe the relationship between SA:V ratio and the time taken to decolourise.', 'As SA:V ratio decreases (larger cubes), time increases.', 'Inverse relationship described (A1).', 1),
        (f'Calculate the mean rate of diffusion of acid into the {sides[-1]:.1f} cm cube in cm per minute.', f'{rt:.3f} cm min⁻¹', f'Distance to centre = {dist:.2f} cm (M1); {dist:.2f}/{times[-1]:.1f} = {rt:.3f} cm min⁻¹ (A1).', 2),
        ('Explain why the larger cubes took longer to decolourise.', 'They have a smaller SA:V ratio, so less surface for acid to enter per unit volume, and a greater distance from the surface to the centre.', 'Lower SA:V (A1); longer diffusion distance (A1).', 2),
        ('Relate these results to the size of cells.', 'Cells must stay small (or flattened/folded) so that diffusion can supply the whole volume fast enough; large cells would have centres that receive materials too slowly.', 'Diffusion too slow for large volumes (A1); cells divide/have adaptations to keep SA:V high (R1).', 2),
        ('Identify two sources of error and suggest improvements.', 'Judging the colour end-point by eye – use a white tile/repeat; inaccurately cut cubes – use a template/measure with calipers; temperature/acid concentration variation – control.', 'Two errors with improvements (A1 A1).', 2),
        ('Suggest why the cubes were fully immersed and not touching the container.', 'So acid can diffuse in through all six faces and SA is as calculated.', 'All faces exposed (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch10-st4', _agar_dq)


# =============================================================================================
# ch11 B3.1 Gas exchange, B3.2 Transport, B3.3 Muscle and motility
# =============================================================================================
S('ch11-st1',
  terms=[('ventilation', 'the movement of air into and out of the lungs, maintaining concentration gradients for gas exchange'),
         ('tidal volume', 'the volume of air breathed in or out in one normal breath, about 0.5 dm³ at rest'),
         ('vital capacity', 'the maximum volume of air that can be exhaled after a maximum inhalation'),
         ('alveolus', 'a tiny air sac in the lungs where gas exchange occurs, surrounded by capillaries'),
         ('surfactant', 'a phospholipid–protein secretion from type II pneumocytes that reduces surface tension in alveoli and prevents their collapse'),
         ('inspiratory reserve volume', 'the extra volume of air that can be inhaled beyond a normal tidal inhalation')],
  facts=[('Which muscles contract during normal inspiration?', 'the diaphragm and external intercostal muscles', ['the internal intercostals and abdominal muscles', 'the diaphragm relaxes', 'the heart muscles'], 'Thorax volume increases, pressure falls.'),
         ('What happens to pressure inside the thorax during inspiration?', 'it decreases below atmospheric pressure', ['it increases', 'it stays the same', 'it equals blood pressure'], 'Air flows in down the pressure gradient.'),
         ('Which instrument is used to measure lung volumes?', 'a spirometer', ['a potometer', 'a sphygmomanometer', 'a colorimeter'], 'Spirometers record volume changes over time.'),
         ('Which feature of alveoli increases the rate of gas exchange?', 'a very large total surface area', ['a thick wall', 'few capillaries', 'a dry surface'], 'About 70 m² in human lungs.')],
  mc2=[('Why does ventilation maintain a steep concentration gradient in the alveoli?', 'It replaces air low in O₂ and high in CO₂ with fresh air.', ['It increases blood pressure.', 'It warms the air.', 'It slows blood flow.'], 'Ventilation plus blood flow keep gradients steep.'),
       ('Why do premature babies sometimes develop breathing difficulties?', 'Type II pneumocytes may not yet produce enough surfactant, so alveoli collapse.', ['They have too many alveoli.', 'Their diaphragm is too strong.', 'They have no capillaries.'], 'Surfactant is produced late in gestation.'),
       ('Which statement explains forced expiration?', 'Internal intercostals and abdominal muscles contract, reducing thorax volume further.', ['The diaphragm contracts.', 'External intercostals contract.', 'Air is drawn in.'], 'Active process during exercise.')],
  mc3=[('A student’s tidal volume is 0.5 dm³ and breathing rate 15 breaths min⁻¹. During exercise, tidal volume rises to 2.0 dm³ and rate to 30 min⁻¹. By what factor does ventilation rate increase?', '8', ['2', '4', '60'], '7.5 → 60 dm³ min⁻¹.'),
       ('Emphysema destroys alveolar walls, merging alveoli into larger spaces. Which consequence is most direct?', 'reduced surface area for gas exchange', ['increased surfactant', 'thinner diffusion barrier', 'more capillaries'], 'Fewer, larger sacs have less total area.')],
  why=[('Explain how the mechanism of ventilation causes air to enter the lungs.', 'External intercostal muscles contract, moving the ribcage up and out; the diaphragm contracts and flattens; thorax volume increases; pressure in the lungs falls below atmospheric pressure; air flows in until pressures are equal.'),
       ('Explain how the structure of alveoli is adapted for gas exchange.', 'Very large total surface area; walls of thin type I pneumocytes and capillary endothelium give short diffusion distance (about 0.5 µm); moist lining dissolves gases; dense capillary network with continuous blood flow maintains gradients; surfactant prevents collapse.'),
       ('Explain why the volume of air ventilated per minute increases during exercise.', 'Increased respiration in muscles produces more CO₂ and uses more O₂; rising CO₂/falling pH is detected by chemoreceptors; the brainstem increases rate and depth of breathing to maintain gradients and remove CO₂.')],
  contrast=[('tidal volume', 'vital capacity', 'Tidal volume is the volume exchanged in a normal breath (about 0.5 dm³); vital capacity is the maximum volume exhaled after maximum inhalation (about 4–5 dm³).'),
            ('inspiration', 'expiration at rest', 'In inspiration the diaphragm and external intercostals contract, thorax volume increases and pressure falls; in resting expiration these muscles relax, elastic recoil decreases volume and increases pressure, forcing air out.')],
  misc=[('During inspiration air is sucked in, which pushes the ribs out.', 'Muscle contraction expands the thorax first; the drop in pressure then causes air to flow in.'),
        ('Gas exchange happens in the bronchi and trachea.', 'Gas exchange occurs across the alveolar walls; the airways only conduct air.')],
  cases=[('emphysema in long-term smokers', 'Elastase from inflammatory cells breaks down elastin in alveolar walls, which merge into large air spaces.', 'the importance of alveolar structure for gas exchange', 'Reduced surface area and loss of elastic recoil lower the efficiency of gas exchange and ventilation.'),
         ('surfactant therapy for premature infants', 'Babies born before about 30 weeks are given artificial surfactant through a tube into the trachea.', 'the role of type II pneumocytes', 'Supplying surfactant lowers surface tension so alveoli stay inflated and gas exchange can occur.')],
  evaluate=[('Lung capacity is the most important factor determining athletic performance.', ['larger vital capacity allows greater ventilation at high work rates', 'some elite rowers and swimmers have exceptional lung volumes'], ['in healthy people oxygen uptake is usually limited by cardiac output and muscle capillarity, not ventilation', 'training improves heart and muscle far more than lung volume'], 'Lung capacity contributes, but cardiovascular and muscular factors usually limit aerobic performance more.')],
  extended=[('Explain the mechanism of ventilation and the adaptations of the lungs for efficient gas exchange.', 'Inspiration: diaphragm and external intercostals contract, volume up, pressure down, air in; expiration: relax, recoil, internal intercostals in forced; antagonistic muscles. Adaptations: large SA, thin pneumocytes, moist, capillaries, surfactant, ventilation maintains gradient; measured by spirometer.', 8)],
  )


@R.add('ch11-st1', 'C3', (1, 5), 'numerical')
def ventilation(rng, slot):
    who = name(rng)
    tv = round(rng.uniform(0.4, 0.65), 2)
    br = rng.randint(12, 18)
    tv2 = round(tv * rng.uniform(2.5, 4.5), 2)
    br2 = rng.randint(25, 45)
    v1, v2 = tv * br, tv2 * br2
    ctx = pick(rng, ['at rest', 'sitting reading', 'before a 400 m run'])
    if slot.d <= 2:
        return num(f'{who}’s tidal volume {ctx} was {tv} dm³ and breathing rate {br} breaths per minute. Calculate the ventilation rate.',
                   f'{v1:.2f} dm³ min⁻¹', f'Ventilation rate = tidal volume × breathing rate = {tv} × {br} (M1) = {v1:.2f} dm³ min⁻¹ (A1).', 2)
    p = pct_change(v1, v2)
    return num(f'{who}’s tidal volume {ctx} was {tv} dm³ at {br} breaths per minute. During exercise it was {tv2} dm³ at {br2} breaths per minute. Calculate the ventilation rate in each case and the percentage increase, and explain why it increases.',
               f'{v1:.2f} → {v2:.1f} dm³ min⁻¹; +{p:.0f} %; respiration in muscles increases, so more CO₂ must be removed and more O₂ supplied – rising blood CO₂ is detected by chemoreceptors, which increase breathing rate and depth', f'{v1:.2f} and {v2:.1f} dm³ min⁻¹ (A1 A1); ({v2:.1f} − {v1:.2f})/{v1:.2f} × 100 = {p:.0f} % (A1); more CO₂ from respiration detected by chemoreceptors, more O₂ needed (R1).', 4)


def _spiro_dq(rng, slot):
    tv = round(rng.uniform(0.45, 0.6), 2)
    irv = round(rng.uniform(2.3, 3.0), 2)
    erv = round(rng.uniform(1.0, 1.4), 2)
    rv = round(rng.uniform(1.1, 1.3), 2)
    br = rng.randint(12, 16)
    vc = tv + irv + erv
    tlc = vc + rv
    who = name(rng)
    intro = (f'A spirometer trace was recorded for {who}, a 17-year-old student, at rest. Values read from the trace are shown.\n\n'
             + table(['Lung volume', 'Value / dm³'], [('tidal volume', f'{tv:.2f}'), ('inspiratory reserve volume', f'{irv:.2f}'), ('expiratory reserve volume', f'{erv:.2f}'), ('residual volume (estimated)', f'{rv:.2f}')])
             + f'\n\nDuring the recording {who} took {br} breaths in one minute.')
    parts = [
        ('Calculate the vital capacity.', f'{vc:.2f} dm³', f'VC = TV + IRV + ERV = {tv:.2f} + {irv:.2f} + {erv:.2f} (M1) = {vc:.2f} dm³ (A1).', 2),
        ('Calculate the ventilation rate at rest.', f'{tv * br:.2f} dm³ min⁻¹', f'{tv:.2f} × {br} = {tv * br:.2f} dm³ min⁻¹ (A1).', 1),
        ('Calculate the total lung capacity and the percentage of it that is residual volume.', f'{tlc:.2f} dm³; {100 * rv / tlc:.0f} %', f'{vc:.2f} + {rv:.2f} = {tlc:.2f} (A1); {rv:.2f}/{tlc:.2f} × 100 = {100 * rv / tlc:.0f} % (A1).', 2),
        ('Explain why residual volume cannot be measured with a simple spirometer.', 'It is the air that remains in the lungs after maximum expiration, so it never enters or leaves the spirometer.', 'Air never exhaled (A1).', 1),
        ('Predict and explain how tidal volume and breathing rate would change during vigorous exercise.', 'Both increase; tidal volume uses part of the inspiratory and expiratory reserve volumes; to supply more O₂ and remove more CO₂ produced by respiration.', 'Both increase (A1); reserve volumes used (A1); link to respiration/CO₂ (R1).', 3),
        ('State two precautions needed when using a spirometer.', 'Sterilise the mouthpiece; use a nose clip; ensure soda lime is fresh to absorb CO₂; stop if dizzy; person must be healthy (no asthma).', 'Two valid precautions (A1 A1).', 2),
        ('Suggest why vital capacity is often lower in smokers.', 'Damage to alveolar walls (emphysema) and narrowing of airways reduces elastic recoil and the volume that can be exhaled.', 'Valid reason (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch11-st1', _spiro_dq)

S('ch11-st2',
  terms=[('stomata', 'pores in the epidermis of leaves, each surrounded by two guard cells, that allow gas exchange and control water loss'),
         ('transpiration', 'the loss of water vapour from the leaves and stems of plants, mainly through stomata'),
         ('guard cells', 'pairs of specialised epidermal cells that change shape to open and close a stoma'),
         ('spongy mesophyll', 'loosely packed leaf cells with large air spaces that allow diffusion of gases to and from photosynthesising cells'),
         ('potometer', 'apparatus for estimating the rate of transpiration by measuring water uptake by a cut shoot'),
         ('stomatal density', 'the number of stomata per unit area of leaf surface')],
  facts=[('Which cells control the opening and closing of stomata?', 'guard cells', ['palisade cells', 'xylem vessels', 'companion cells'], 'Turgor changes in guard cells open pores.'),
         ('Which factor decreases the rate of transpiration?', 'high humidity', ['high temperature', 'high wind speed', 'high light intensity'], 'Humid air reduces the water vapour gradient.'),
         ('Where are most stomata found on the leaves of typical dicotyledonous plants?', 'on the lower (abaxial) surface', ['on the upper surface', 'on the midrib only', 'on the petiole'], 'Reduces water loss from the sunlit upper surface.'),
         ('Which tissue layer of a leaf has the most chloroplasts?', 'palisade mesophyll', ['spongy mesophyll', 'epidermis', 'xylem'], 'Columnar cells just under the upper epidermis.')],
  mc2=[('Why is transpiration described as a consequence of gas exchange?', 'Stomata must open for CO₂ uptake, which allows water vapour to escape.', ['Water is needed to make CO₂.', 'Transpiration produces oxygen.', 'Stomata only allow water out.'], 'Trade-off between photosynthesis and water loss.'),
       ('Why does wind increase transpiration rate?', 'It removes water vapour from around the leaf, maintaining a steep diffusion gradient.', ['It cools the leaf.', 'It closes stomata.', 'It increases humidity.'], 'Removes the boundary layer.'),
       ('Why does a potometer only estimate transpiration rate?', 'It measures water uptake, some of which is used in photosynthesis or retained by cells.', ['It measures evaporation from the water surface.', 'It measures oxygen production.', 'It only works in darkness.'], 'Uptake ≈ but not exactly = loss.')],
  mc3=[('In a potometer the air bubble moved 45 mm in 5 minutes in a capillary of radius 0.5 mm. What is the rate of water uptake?', '7.1 mm³ min⁻¹', ['9.0 mm³ min⁻¹', '35.3 mm³ min⁻¹', '2.25 mm³ min⁻¹'], 'V = πr²d = π × 0.25 × 45 = 35.3 mm³; ÷ 5 = 7.1.'),
       ('A leaf impression shows 24 stomata in a field of view of diameter 0.4 mm. What is the stomatal density?', '191 mm⁻²', ['60 mm⁻²', '48 mm⁻²', '764 mm⁻²'], 'Area = π × 0.2² = 0.126 mm²; 24/0.126 = 191.')],
  why=[('Explain how the structure of a leaf is adapted for gas exchange.', 'Large flat surface area; thin so short diffusion distance; stomata allow CO₂ in and O₂ out; spongy mesophyll with air spaces for diffusion inside the leaf; moist cell surfaces for gases to dissolve; waxy cuticle reduces water loss.'),
       ('Explain how temperature affects the rate of transpiration.', 'Higher temperature increases the kinetic energy of water molecules, so evaporation from mesophyll cell walls and diffusion of water vapour out through stomata are faster; warm air holds more water vapour, so the gradient is steeper.'),
       ('Explain how stomatal density can be measured.', 'Apply clear nail varnish to the leaf surface, peel off with tape and mount on a slide; count stomata in several fields of view of known area at high power; calculate mean number per mm².')],
  contrast=[('palisade mesophyll', 'spongy mesophyll', 'Palisade mesophyll is tightly packed columnar cells with many chloroplasts, specialised for photosynthesis; spongy mesophyll is loosely packed with large air spaces for gas diffusion and fewer chloroplasts.')],
  misc=[('Plants transpire mainly to cool themselves down.', 'Transpiration is largely an unavoidable consequence of stomata being open for CO₂ uptake; it also helps transport water and minerals and cools leaves.'),
        ('Stomata are open at night to take in CO₂.', 'In most plants stomata close in darkness because CO₂ is not needed for photosynthesis; CAM plants are an exception.')],
  cases=[('marram grass (Ammophila arenaria) on sand dunes', 'Its leaves roll up in dry conditions with stomata in pits on the inner surface, surrounded by hairs.', 'adaptations that reduce transpiration', 'Trapped humid air reduces the water vapour gradient, so less water is lost while some gas exchange continues.'),
         ('fossil leaf stomatal density as a record of past CO₂', 'Leaves grown in high CO₂ have fewer stomata; fossil ginkgo leaves show changes matching past CO₂ levels.', 'stomatal density', 'Plants reduce stomatal density when CO₂ is high, limiting water loss while still obtaining enough CO₂.')],
  evaluate=[('Stomata are the most important adaptation for controlling water loss in plants.', ['stomata can close quickly to reduce water loss when water is scarce', 'transpiration occurs mainly through stomata'], ['the waxy cuticle prevents most water loss from the leaf surface', 'other adaptations such as leaf rolling, CAM and small leaves also reduce water loss'], 'Stomata provide the main dynamic control, but the cuticle and structural and physiological adaptations are also essential.')],
  extended=[('Explain how leaves are adapted for gas exchange and describe how the rate of transpiration can be measured and affected by abiotic factors.', 'Leaf adaptations; stomata, guard cells; potometer: cut under water, seal, bubble, rate = πr²d/t; factors: light (stomata open), temperature, humidity, wind; trade-off; stomatal density measurement by nail varnish impressions.', 8)],
  )


@R.add('ch11-st2', 'C3', (1, 5), 'numerical')
def potometer(rng, slot):
    r = pick(rng, [0.25, 0.4, 0.5, 0.75, 1.0])
    d = rng.randint(15, 120)
    t = pick(rng, [2, 4, 5, 10, 15])
    vol = math.pi * r * r * d
    rate = vol / t
    plant = pick(rng, ['a leafy shoot of Pelargonium', 'a privet shoot', 'a laurel shoot', 'a shoot of a tomato plant', 'a bean seedling'])
    cond = pick(rng, ['in still air at 20 °C', 'in front of a fan', 'under a bright lamp', 'inside a plastic bag', 'in a cool, dark room'])
    stem = f'In a bubble potometer with {plant} {cond}, the air bubble moved {d} mm in {t} minutes along a capillary tube of internal radius {r} mm. Calculate the rate of water uptake in mm³ min⁻¹.'
    key = f'V = πr²d = π × {r}² × {d} = {sf(vol)} mm³ (M1); rate = {sf(vol)}/{t} = {sf(rate)} mm³ min⁻¹ (A1).'
    if slot.d >= 4:
        area = rng.randint(40, 200)
        stem += f' The total leaf area was {area} cm². Calculate the rate per cm² of leaf and explain why it is useful to express it this way.'
        return num(stem, f'{sf(rate)} mm³ min⁻¹; {sf(rate / area)} mm³ min⁻¹ cm⁻²', key + f' {sf(rate)}/{area} = {sf(rate / area)} (A1); allows comparison between shoots of different size (R1).', 4)
    return num(stem, f'{sf(rate)} mm³ min⁻¹', key, 2)


@R.add('ch11-st2', 'C3', (1, 4), 'numerical')
def stomatal_density(rng, slot):
    diam = pick(rng, [0.3, 0.4, 0.45, 0.5])
    counts = [rng.randint(8, 45) for _ in range(5)]
    area = math.pi * (diam / 2) ** 2
    m = mean(counts)
    plant = pick(rng, ['sunflower', 'privet', 'maize', 'oleander', 'English ivy', 'tomato'])
    side = pick(rng, ['lower', 'upper'])
    stem = (f'Stomata were counted in five fields of view on a nail-varnish impression of the {side} epidermis of a {plant} leaf: {", ".join(map(str, counts))}. The diameter of the field of view was {diam} mm. '
            f'Calculate the mean stomatal density in stomata per mm².')
    return num(stem, f'{m / area:.0f} mm⁻²', f'Mean count = {m:.1f} (A1); area = π × ({diam}/2)² = {area:.3f} mm² (M1); density = {m:.1f}/{area:.3f} = {m / area:.0f} mm⁻² (A1).', 3)


def _poto_dq(rng, slot):
    conds = ['still air, 20 °C', 'fan (moving air), 20 °C', 'still air, 30 °C', 'plastic bag over shoot, 20 °C', 'dark, 20 °C']
    base = rng.uniform(20, 35)
    fac = [1.0, rng.uniform(1.8, 2.6), rng.uniform(1.4, 1.9), rng.uniform(0.25, 0.45), rng.uniform(0.15, 0.3)]
    r = 0.5
    t = 5
    ds = [[round(base * f * rng.uniform(0.92, 1.08)) for _ in range(3)] for f in fac]
    md = [mean(x) for x in ds]
    rates = [math.pi * r * r * m / t for m in md]
    k = rng.randrange(5)
    intro = (f'A bubble potometer (capillary radius {r} mm) was used to measure water uptake by a leafy shoot under different conditions. The distance moved by the bubble in {t} minutes was recorded three times for each condition.\n\n'
             + table(['Condition', 'Distance 1 / mm', 'Distance 2 / mm', 'Distance 3 / mm'], [(c, *x) for c, x in zip(conds, ds)]))
    pc = pct_change(md[0], md[1])
    parts = [
        (f'Calculate the mean distance moved for “{conds[k]}”.', f'{md[k]:.1f} mm', f'{" + ".join(map(str, ds[k]))} ÷ 3 = {md[k]:.1f} mm (A1).', 1),
        (f'Calculate the rate of water uptake for “{conds[k]}” in mm³ min⁻¹.', f'{rates[k]:.1f} mm³ min⁻¹', f'π × {r}² × {md[k]:.1f} = {math.pi * r * r * md[k]:.1f} mm³ (M1); ÷ {t} = {rates[k]:.1f} (A1).', 2),
        ('Calculate the percentage change in mean distance when the fan was switched on.', f'{signed(pc)} %', f'({md[1]:.1f} − {md[0]:.1f})/{md[0]:.1f} × 100 (M1) = {signed(pc)} % (A1).', 2),
        ('Explain the effect of moving air on the rate of transpiration.', 'Moving air removes water vapour from around the stomata, maintaining a steep water vapour gradient, so diffusion of water vapour out of the leaf is faster.', 'Removes humid air/boundary layer (A1); steeper gradient → faster diffusion (A1).', 2),
        ('Explain the results for the shoot covered with a plastic bag and the shoot in the dark.', 'Bag: humidity rises, reducing the diffusion gradient; dark: stomata close, so little water vapour escapes.', 'Bag – high humidity/low gradient (A1); dark – stomata close (A1).', 2),
        ('State two precautions needed when setting up a potometer.', 'Cut the shoot under water; ensure the apparatus is airtight/no air bubbles in xylem; dry the leaves; allow time to equilibrate.', 'Two valid precautions (A1 A1).', 2),
        ('Explain why the potometer measures water uptake rather than transpiration.', 'Some water absorbed is used in photosynthesis or to maintain turgor, so uptake is not exactly equal to water lost.', 'Water used by cells (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch11-st2', _poto_dq)

S('ch11-st3',
  terms=[('cardiac cycle', 'the sequence of events in one heartbeat, including atrial and ventricular systole and diastole'),
         ('systole', 'the phase of the cardiac cycle in which heart muscle contracts and pumps blood'),
         ('diastole', 'the phase of the cardiac cycle in which heart muscle relaxes and the chambers fill with blood'),
         ('sinoatrial node', 'the pacemaker of the heart: a group of specialised cardiac muscle cells in the right atrium that initiates each heartbeat'),
         ('tissue fluid', 'fluid that leaks out of capillaries under pressure and bathes the cells, allowing exchange of materials'),
         ('cardiac output', 'the volume of blood pumped by one ventricle per minute; stroke volume × heart rate')],
  facts=[('Which blood vessels have thick, elastic, muscular walls?', 'arteries', ['veins', 'capillaries', 'lymph vessels'], 'They withstand and smooth high pressure.'),
         ('Which vessels have valves to prevent backflow?', 'veins', ['arteries', 'capillaries', 'arterioles'], 'Low pressure in veins.'),
         ('Which structure delays the impulse between the atria and ventricles?', 'the atrioventricular node', ['the sinoatrial node', 'the bundle of His', 'the aorta'], 'The delay allows atria to empty first.'),
         ('Which valves close at the start of ventricular systole?', 'the atrioventricular valves', ['the semilunar valves', 'the valves in veins', 'no valves'], 'Ventricular pressure exceeds atrial pressure.'),
         ('What is the wall of a capillary made of?', 'a single layer of endothelial cells', ['smooth muscle and elastic tissue', 'cartilage', 'three layers of cells'], 'Short diffusion distance.')],
  mc2=[('Why does blood pressure fall as blood passes from arteries to capillaries?', 'The total cross-sectional area increases and friction with vessel walls dissipates energy.', ['Capillaries pump blood.', 'Blood is lost from the circulation.', 'Veins contract.'], 'Many narrow vessels in parallel.'),
       ('Why is the wall of the left ventricle thicker than that of the right ventricle?', 'It must generate higher pressure to pump blood around the whole body.', ['It holds a larger volume of blood.', 'It receives deoxygenated blood.', 'It pumps blood to the lungs.'], 'Systemic circulation has higher resistance.'),
       ('Why do the semilunar valves open during ventricular systole?', 'Pressure in the ventricle rises above pressure in the artery.', ['Pressure in the atria rises.', 'The SA node opens them.', 'Muscles pull them open.'], 'Valves respond to pressure differences.')],
  mc3=[('An ECG shows R waves 0.75 s apart. What is the heart rate?', '80 beats min⁻¹', ['75 beats min⁻¹', '45 beats min⁻¹', '133 beats min⁻¹'], '60 ÷ 0.75 = 80.'),
       ('Stroke volume is 70 cm³ and heart rate 72 beats min⁻¹. What is the cardiac output?', '5.04 dm³ min⁻¹', ['0.97 dm³ min⁻¹', '50.4 dm³ min⁻¹', '142 cm³ min⁻¹'], '70 × 72 = 5040 cm³ min⁻¹.')],
  why=[('Explain how tissue fluid is formed and returned to the blood.', 'At the arterial end of a capillary, hydrostatic pressure is higher than the osmotic pull of plasma proteins, so fluid is forced out through gaps; at the venous end hydrostatic pressure has fallen and water re-enters by osmosis; excess fluid drains into lymph vessels.'),
       ('Explain how the structure of arteries is related to their function.', 'Thick walls with collagen withstand high pressure; elastic fibres stretch during systole and recoil during diastole, maintaining pressure and smoothing flow; smooth muscle can constrict or dilate to regulate flow; narrow lumen maintains pressure.'),
       ('Explain how the heartbeat is initiated and coordinated.', 'The SA node (pacemaker) depolarises spontaneously, sending impulses across both atria, which contract; the AV node delays the impulse; it passes down the bundle of His and Purkinje fibres to the ventricle apex, so ventricles contract from the bottom up, after atria have emptied.'),
       ('Explain the pressure changes and valve movements during ventricular systole.', 'Ventricles contract, pressure rises above atrial pressure so AV valves close; when pressure exceeds that in the aorta/pulmonary artery, semilunar valves open and blood is ejected; as ventricles relax and pressure falls below arterial pressure, semilunar valves close.')],
  contrast=[('arteries', 'veins', 'Arteries carry blood away from the heart at high pressure, with thick muscular elastic walls and narrow lumens; veins return blood at low pressure, with thinner walls, wide lumens and valves.'),
            ('systole', 'diastole', 'Systole is contraction of heart chambers that ejects blood; diastole is relaxation during which chambers fill.')],
  misc=[('Veins always carry deoxygenated blood.', 'Veins carry blood towards the heart; the pulmonary vein carries oxygenated blood from the lungs.'),
        ('The heartbeat is started by nerve impulses from the brain.', 'Cardiac muscle is myogenic: the SA node initiates each beat; nerves and hormones only change the rate.')],
  cases=[('occlusion of a coronary artery in a heart attack', 'A blood clot on an atherosclerotic plaque blocks a coronary artery, cutting off blood to part of the heart muscle.', 'the importance of blood supply to cardiac muscle', 'Without oxygen, cardiac muscle cells cannot respire aerobically and die, reducing the heart’s ability to pump.'),
         ('artificial pacemakers', 'An electronic device delivers regular impulses to the heart when the SA node or conduction system fails.', 'the role of the SA node', 'It replaces the natural pacemaker signal that initiates each heartbeat.')],
  evaluate=[('Coronary heart disease is mainly caused by lifestyle factors.', ['smoking, high saturated fat diet, lack of exercise and obesity raise risk', 'risk falls when people change these behaviours'], ['genetic factors such as familial hypercholesterolaemia strongly affect risk', 'age and sex are non-modifiable risk factors'], 'Lifestyle factors are major modifiable contributors, but genetics and age also play substantial roles; risk results from their interaction.')],
  extended=[('Describe the events of the cardiac cycle, including pressure changes and valve movements, and explain how the heartbeat is controlled.', 'Atrial systole: AV valves open, ventricles fill. Ventricular systole: AV close, pressure rises, SL open, ejection. Diastole: SL close, filling. SA node pacemaker, AV delay, bundle of His, Purkinje fibres; myogenic; nerves/adrenaline alter rate; ECG.', 8)],
  )


@R.add('ch11-st3', 'C3', (1, 5), 'numerical')
def cardiac_output(rng, slot):
    who = name(rng)
    f = rng.randrange(2)
    if f == 0:
        rr = round(rng.uniform(0.45, 1.1), 2)
        hr = 60 / rr
        stem = f'An ECG of {who} shows that the time between successive R waves is {rr} s. Calculate the heart rate in beats per minute.'
        if slot.d >= 3:
            sv = rng.randint(60, 110)
            stem += f' The stroke volume is {sv} cm³. Calculate the cardiac output in dm³ min⁻¹.'
            return num(stem, f'{hr:.0f} beats min⁻¹; {sv * hr / 1000:.2f} dm³ min⁻¹', f'60/{rr} = {hr:.0f} (A1); {sv} × {hr:.1f} = {sv * hr:.0f} cm³ (M1) = {sv * hr / 1000:.2f} dm³ min⁻¹ (A1).', 3)
        return num(stem, f'{hr:.0f} beats min⁻¹', f'Heart rate = 60/{rr} = {hr:.0f} beats min⁻¹ (A1).', 1)
    hr1, sv1 = rng.randint(55, 80), rng.randint(60, 85)
    hr2, sv2 = rng.randint(140, 185), rng.randint(95, 130)
    co1, co2 = hr1 * sv1 / 1000, hr2 * sv2 / 1000
    stem = f'At rest {who} has a heart rate of {hr1} beats min⁻¹ and a stroke volume of {sv1} cm³. During intense exercise these become {hr2} beats min⁻¹ and {sv2} cm³. Calculate the cardiac output in each case and the factor by which it increases.'
    return num(stem, f'{co1:.2f} and {co2:.2f} dm³ min⁻¹; × {co2 / co1:.1f}', f'CO = SV × HR (M1); {co1:.2f} and {co2:.2f} dm³ min⁻¹ (A1); {co2:.2f}/{co1:.2f} = {co2 / co1:.1f} (A1).', 3)


S('ch11-st4',
  terms=[('xylem', 'plant tissue of dead, hollow, lignified vessels that transports water and mineral ions from roots to leaves'),
         ('phloem', 'plant tissue of living sieve tube elements and companion cells that transports organic compounds such as sucrose'),
         ('translocation', 'the transport of organic solutes (mainly sucrose) in phloem from sources to sinks'),
         ('source', 'a part of a plant where sugars are produced or released, such as a photosynthesising leaf'),
         ('sink', 'a part of a plant where sugars are used or stored, such as roots, fruits or growing tips'),
         ('lignin', 'a hard polymer deposited in xylem walls that strengthens them and resists collapse under tension')],
  facts=[('Which tissue transports sucrose in plants?', 'phloem', ['xylem', 'epidermis', 'cortex'], 'Translocation occurs in sieve tubes.'),
         ('Why are xylem vessels strengthened with lignin?', 'to prevent collapse under the tension of the transpiration stream', ['to store sugar', 'to allow photosynthesis', 'to make them living'], 'Low pressure inside could cause collapse.'),
         ('Which cells support sieve tube elements metabolically?', 'companion cells', ['guard cells', 'root hair cells', 'palisade cells'], 'They have many mitochondria and load sucrose.'),
         ('What drives water up the xylem in tall trees?', 'tension generated by transpiration from the leaves', ['active pumping by xylem cells', 'gravity', 'root pressure only'], 'Cohesion–tension.'),
         ('Which cells take up water and mineral ions from the soil?', 'root hair cells', ['xylem vessels', 'phloem cells', 'guard cells'], 'Large surface area.')],
  mc2=[('Why can xylem vessels conduct water efficiently?', 'They are dead, hollow tubes with no end walls or cytoplasm.', ['They contain many mitochondria.', 'They have sieve plates.', 'They pump water actively.'], 'Continuous columns of water.'),
       ('Why is phloem transport described as bidirectional?', 'Sinks can be above or below sources, so sap can move up or down.', ['Each sieve tube carries sap both ways at once.', 'Xylem and phloem swap roles.', 'Sucrose is carried only downwards.'], 'Direction depends on source–sink location.'),
       ('How is a high pressure generated in the phloem at a source?', 'Sucrose is actively loaded into sieve tubes, lowering water potential so water enters by osmosis.', ['Transpiration pulls water up.', 'Xylem pumps sucrose.', 'Sieve tubes contract.'], 'Pressure-flow mechanism.')],
  mc3=[('A radioactive tracer of ¹⁴CO₂ was given to a leaf. Labelled sucrose was detected 0.6 m away after 40 minutes. What was the rate of translocation?', '0.9 m h⁻¹', ['0.015 m h⁻¹', '24 m h⁻¹', '1.5 m h⁻¹'], '0.6 m in 40 min = 0.9 m per hour.'),
       ('A ring of bark (including phloem) is removed from a tree trunk. After some weeks the bark just above the ring swells. Why?', 'Sugars transported downwards in phloem accumulate above the cut.', ['Water accumulates because xylem is cut.', 'Roots grow above the ring.', 'Transpiration stops.'], 'Phloem is outside the xylem.')],
  why=[('Explain how the structure of xylem vessels is related to their function.', 'Dead cells with no cytoplasm and no end walls form continuous hollow tubes allowing unimpeded flow; lignified thickened walls withstand tension without collapsing; pits allow lateral movement of water; narrow diameter aids capillarity and adhesion.'),
       ('Explain the mechanism of translocation in phloem.', 'At the source, sucrose is actively loaded into companion cells/sieve tubes; water potential falls; water enters from xylem by osmosis; hydrostatic pressure rises; sap flows towards sinks where sucrose is unloaded and used/stored; water leaves, lowering pressure (pressure-flow).'),
       ('Explain how root pressure is generated.', 'Root cells actively transport mineral ions into the xylem; water potential in the xylem falls; water enters by osmosis from surrounding cells; pressure builds up and pushes water up the xylem, especially when transpiration is low.')],
  contrast=[('xylem', 'phloem', 'Xylem: dead lignified vessels, water and minerals, one direction (roots to leaves), driven by transpiration tension; phloem: living sieve tubes with companion cells, sucrose and amino acids, bidirectional from sources to sinks, driven by active loading and pressure.')],
  misc=[('Xylem vessels are living cells that pump water upwards.', 'Mature xylem vessels are dead; water is pulled up passively by transpiration (cohesion–tension).'),
        ('Phloem always carries sugar downwards from leaves to roots.', 'Phloem carries sugar from sources to sinks, which can be up (to growing shoots, fruits) or down.')],
  cases=[('aphids feeding on phloem sap', 'Aphid mouthparts (stylets) penetrate single sieve tubes; when the aphid is cut away, sap continues to exude from the stylet under pressure.', 'the pressure-flow mechanism of translocation', 'The exudation shows phloem contents are under positive pressure and allows sap to be sampled and analysed.'),
         ('ringing experiments on woody stems', 'Removing a ring of bark causes swelling above the ring as sugars accumulate.', 'the role of phloem in translocation', 'Phloem lies in the bark; cutting it stops downward transport of sugar while xylem transport continues.')],
  evaluate=[('The pressure-flow hypothesis fully explains translocation in phloem.', ['active loading at sources and osmotic pressure explain flow from source to sink', 'aphid stylet experiments confirm pressure in sieve tubes'], ['different solutes have been observed moving at different speeds in the same sieve tube', 'the role of sieve plates and possible active mechanisms along the pathway are debated'], 'Pressure flow is the best-supported explanation, but some observations suggest it may not account for all details of translocation.')],
  extended=[('Compare the structure and function of xylem and phloem and explain how water and sugars are transported in plants.', 'Xylem: dead, lignified, continuous, pits; transpiration pull, cohesion–tension, root pressure. Phloem: sieve tubes, sieve plates, companion cells; active loading, osmosis, hydrostatic pressure, source to sink; aphid evidence; bidirectional.', 8)],
  )

pct_items(R, 'ch11-st4', [
    ('The rate of sap exudation from an aphid stylet changed from {a} µl h⁻¹ to {b} µl h⁻¹ when the plant was moved from light into darkness.', 'µl h⁻¹', 0.8, 2.0, -0.6, -0.25, 2, 'less photosynthesis in the dark reduces sucrose loading at the source, so pressure and flow in the phloem fall.'),
    ('The diameter of a tree trunk changed from {a} mm at dawn to {b} mm at midday.', 'mm', 300, 600, -0.006, -0.002, 1, 'tension in the xylem during rapid transpiration pulls the walls inward, slightly shrinking the trunk.'),
    ('Xylem sap flow in a sunflower stem changed from {a} g h⁻¹ to {b} g h⁻¹ after the humidity was raised.', 'g h⁻¹', 15, 40, -0.6, -0.2, 1, 'higher humidity reduces the water vapour gradient, slowing transpiration and the transpiration pull.'),
])

S('ch11-st5',
  terms=[('sarcomere', 'the repeating contractile unit of a myofibril, between two Z lines'),
         ('sliding filament model', 'the model in which muscle contraction occurs as myosin heads pull actin filaments towards the centre of the sarcomere, shortening it without the filaments themselves shortening'),
         ('myosin', 'the thick filament protein whose heads form cross-bridges with actin and hydrolyse ATP'),
         ('actin', 'the thin filament protein with binding sites for myosin heads'),
         ('titin', 'a very large elastic protein that connects myosin to the Z line and helps muscles recoil after stretching'),
         ('antagonistic muscles', 'pairs of muscles that produce opposite movements at a joint, such as biceps and triceps')],
  facts=[('Which ion binds to troponin to expose binding sites on actin?', 'calcium ions', ['sodium ions', 'potassium ions', 'chloride ions'], 'Ca²⁺ released from the sarcoplasmic reticulum.'),
         ('Which band of the sarcomere does NOT change length during contraction?', 'the A band', ['the I band', 'the H zone', 'the sarcomere'], 'The A band is the length of the myosin filaments.'),
         ('What is the role of ATP in muscle contraction?', 'it allows myosin heads to detach from actin and re-cock', ['it binds to troponin', 'it releases calcium', 'it shortens actin filaments'], 'Hydrolysis re-energises the head.'),
         ('Which type of joint is the human elbow?', 'a synovial hinge joint', ['a fixed joint', 'a ball-and-socket joint', 'a cartilaginous joint'], 'Allows flexion and extension.')],
  mc2=[('Why does the I band shorten during contraction?', 'Actin filaments slide further over myosin, reducing the region containing actin only.', ['Actin filaments become shorter.', 'Myosin filaments shorten.', 'Z lines move apart.'], 'Filaments slide, not shorten.'),
       ('Why does rigor mortis occur after death?', 'ATP is no longer produced, so myosin heads cannot detach from actin.', ['Calcium is removed from muscle.', 'Actin is broken down.', 'Muscles relax completely.'], 'Cross-bridges remain locked.'),
       ('Why are muscles arranged in antagonistic pairs?', 'Muscles can only pull by contracting, so a second muscle is needed to reverse the movement.', ['Muscles can push and pull.', 'One muscle is always relaxed.', 'Bones contract.'], 'E.g. biceps flexes, triceps extends.')],
  mc3=[('In an electron micrograph at × 25 000, a sarcomere measures 62.5 mm. What is its actual length?', '2.5 µm', ['25 µm', '0.25 µm', '1.56 µm'], '62 500 µm ÷ 25 000 = 2.5 µm.'),
       ('A sarcomere shortens from 2.4 µm to 1.8 µm. The A band is 1.6 µm. What is the length of each half I band after contraction?', '0.1 µm', ['0.2 µm', '0.4 µm', '0.8 µm'], 'I band total = 1.8 − 1.6 = 0.2 µm, so 0.1 µm each side.')],
  why=[('Explain the sliding filament model of muscle contraction.', 'A nerve impulse causes Ca²⁺ release from the sarcoplasmic reticulum; Ca²⁺ binds troponin, moving tropomyosin off actin binding sites; myosin heads (energised by ATP hydrolysis) bind to actin forming cross-bridges; the power stroke pulls actin towards the M line; ATP binds, heads detach and re-cock; repeated cycles shorten the sarcomere.'),
       ('Explain how the structure of striated muscle fibres relates to their function.', 'Many myofibrils of repeating sarcomeres aligned so contraction is coordinated; many mitochondria supply ATP; sarcoplasmic reticulum stores and releases Ca²⁺; multinucleate fibres can be long; T tubules carry impulses inside.'),
       ('Explain why muscles need ATP both for contraction and relaxation.', 'ATP hydrolysis powers the myosin head’s change to the high-energy position; binding of ATP causes the head to detach from actin; ATP also powers active transport of Ca²⁺ back into the sarcoplasmic reticulum, allowing relaxation.')],
  contrast=[('the A band', 'the I band', 'The A band contains myosin (with overlapping actin) and stays the same length; the I band contains actin only and shortens during contraction.')],
  misc=[('During contraction the actin and myosin filaments get shorter.', 'The filaments stay the same length; they slide past each other so that the sarcomere shortens.'),
        ('Muscles can push bones as well as pull them.', 'Muscles can only contract and pull; movement in the opposite direction requires an antagonistic muscle.')],
  cases=[('the biceps and triceps at the human elbow', 'The biceps contracts to flex the elbow while the triceps relaxes; the reverse extends the arm.', 'antagonistic muscles', 'Because muscles only pull, a pair working in opposition is needed to move the forearm in both directions.'),
         ('rigor mortis used in forensic science', 'Muscles stiffen 2–6 hours after death and relax after 24–48 hours as proteins break down.', 'the role of ATP in the cross-bridge cycle', 'Without ATP, myosin heads stay bound to actin, locking muscles until the proteins degrade.')],
  evaluate=[('The sliding filament model is fully supported by evidence.', ['electron micrographs show A band length constant while I band and H zone shorten', 'X-ray diffraction and single-molecule studies show myosin power strokes'], ['the elastic role of titin and other proteins was discovered later', 'details of force generation by myosin are still being studied'], 'The core model is extremely well supported; ongoing research refines details rather than challenging it.')],
  extended=[('Describe the structure of a sarcomere and explain how muscle contraction occurs.', 'Z lines, actin (thin), myosin (thick), A band, I band, H zone, M line, titin. Impulse → Ca²⁺ from SR → troponin/tropomyosin → cross-bridges → power stroke (ADP + Pi released) → ATP detaches → hydrolysis re-cocks → sarcomere shortens; A band constant; antagonistic pairs; relaxation via Ca²⁺ pumping.', 8)],
  )


@R.add('ch11-st5', 'C3', (1, 5), 'numerical')
def sarcomere(rng, slot):
    mag = pick(rng, [10000, 15000, 20000, 25000, 30000, 40000])
    L = round(rng.uniform(2.0, 2.6), 2)
    A = 1.6
    img = round(L * mag / 1000, 1)
    if slot.d <= 2:
        stem = f'An electron micrograph of a myofibril at × {mag} shows a sarcomere {img} mm long. Calculate the actual length of the sarcomere in µm.'
        return num(stem, f'{img * 1000 / mag:.2f} µm', f'{img} mm = {img * 1000:.0f} µm (M1); ÷ {mag} = {img * 1000 / mag:.2f} µm (A1).', 2)
    L2 = round(L - rng.uniform(0.3, 0.6), 2)
    i1 = (L - A)
    i2 = (L2 - A)
    pc = pct_change(L, L2)
    stem = (f'A relaxed sarcomere is {L} µm long and its A band is {A} µm. During contraction the sarcomere shortens to {L2} µm. Calculate the percentage shortening of the sarcomere and the total length of I band before and after contraction, '
            f'and explain why the A band does not change.')
    return num(stem, f'{abs(pc):.1f} % shorter; I band {i1:.2f} → {i2:.2f} µm; A band = length of myosin, which does not shorten',
               f'({L} − {L2})/{L} × 100 = {abs(pc):.1f} % (A1); I = sarcomere − A: {i1:.2f} and {i2:.2f} µm (A1 A1); filaments slide, myosin length constant (R1).', 4)


# =============================================================================================
# ch12 B4.1 Adaptation to environment; B4.2 Ecological niches
# =============================================================================================
S('ch12-st1',
  terms=[('habitat', 'the place where a community, species, population or organism lives, described by its geographical and physical location and type of ecosystem'),
         ('adaptation', 'a heritable characteristic that increases an organism’s chance of survival and reproduction in its environment'),
         ('abiotic factor', 'a non-living physical or chemical factor in an ecosystem, such as temperature, light, water or soil pH'),
         ('xerophyte', 'a plant adapted to survive in dry conditions with little water'),
         ('halophyte', 'a plant adapted to grow in saline (salty) conditions, such as mangroves and salt-marsh plants')],
  facts=[('Which plant feature is an adaptation to sand dunes?', 'rolled leaves with sunken stomata, as in marram grass', ['large, thin leaves', 'floating leaves', 'aerial roots in water'], 'Reduces water loss in dry, windy dunes.'),
         ('Which is an adaptation of mangrove trees to waterlogged saline mud?', 'pneumatophores (aerial roots) for gas exchange', ['succulent stems storing water', 'leaves reduced to spines', 'deep tap roots to reach groundwater'], 'Mud lacks oxygen; salt is excreted by glands.'),
         ('Which abiotic factor most limits plant growth in deserts?', 'water availability', ['carbon dioxide concentration', 'oxygen concentration', 'day length'], 'Xerophytes conserve water.'),
         ('Which is an example of a habitat?', 'a mangrove swamp on the coast of Kenya', ['photosynthesis', 'a food chain', 'the niche of a species'], 'A place where organisms live.')],
  mc2=[('Why are adaptations described as heritable?', 'They are genetically determined and passed on, so they can evolve by natural selection.', ['They are learned during life.', 'They are caused by the environment directly.', 'They appear only in old organisms.'], 'Acquired changes are not adaptations in this sense.'),
       ('Why do mangrove leaves often have salt glands?', 'To excrete excess salt absorbed from seawater.', ['To absorb salt for food.', 'To photosynthesise faster.', 'To attract pollinators.'], 'Maintains water potential and prevents toxicity.'),
       ('How does a thick waxy cuticle help xerophytes?', 'It reduces water loss by evaporation from the leaf surface.', ['It increases gas exchange.', 'It absorbs water from the air.', 'It stores starch.'], 'Impermeable barrier.')],
  mc3=[('Marram grass grows on mobile sand dunes and has very deep roots and rhizomes. Which pair of abiotic factors are these adaptations most likely to address?', 'low water availability and shifting sand', ['high soil nitrogen and shade', 'flooding and low temperature', 'high humidity and still air'], 'Roots reach water; rhizomes resist burial.'),
       ('Plants on the windward side of a coastal cliff are shorter with smaller leaves than those on the sheltered side. Which is the best explanation?', 'Wind increases water loss and mechanical stress, selecting for smaller leaves and stature.', ['Wind increases photosynthesis.', 'Sheltered plants have less light.', 'Wind adds nutrients to the soil.'], 'Abiotic factors shape adaptations.')],
  why=[('Explain how marram grass is adapted to sand dunes.', 'Leaves roll up with stomata on the inner surface in pits with hairs, trapping humid air and reducing transpiration; thick cuticle on the outer surface; long roots reach deep water; rhizomes grow upward when buried by sand.'),
       ('Explain how mangroves are adapted to life in coastal saline swamps.', 'Pneumatophores (aerial roots) allow gas exchange in anaerobic mud; prop roots give stability in soft sediment; salt glands excrete salt and ultrafiltration at roots excludes it; viviparous seedlings establish quickly.'),
       ('Explain how abiotic factors determine where a species can live.', 'Each species has a range of tolerance for factors such as temperature, water, light, pH and salinity; it can only survive and reproduce where all factors are within its tolerance; so the distribution of abiotic factors limits its habitat.')],
  contrast=[('habitat', 'niche', 'A habitat is the place where an organism lives; its niche is its role in the ecosystem, including all its interactions with biotic and abiotic factors.'),
            ('xerophytes', 'halophytes', 'Xerophytes are adapted to dry conditions (conserving water); halophytes are adapted to saline conditions (excluding or excreting salt).')],
  misc=[('Animals develop adaptations during their lifetime because they need them.', 'Adaptations arise by natural selection on heritable variation over generations; individuals do not develop them in response to need.'),
        ('Abiotic factors only affect plants.', 'Abiotic factors such as temperature, water and oxygen availability affect all organisms, including animals and microbes.')],
  cases=[('marram grass (Ammophila arenaria) on European sand dunes', 'It stabilises mobile dunes, rolling its leaves in dry weather and growing up through accumulating sand.', 'adaptations to a habitat', 'Rolled leaves reduce transpiration and rhizomes allow survival of burial – heritable features suited to the abiotic conditions of dunes.'),
         ('red mangroves (Rhizophora mangle) in the Florida Everglades', 'They grow in tidal saline mud using prop roots and excluding salt at the roots.', 'adaptations to saline, anaerobic soils', 'Specialised roots and salt control allow survival where few plants can grow.')],
  evaluate=[('Abiotic factors are more important than biotic factors in determining the distribution of species.', ['abiotic factors set the limits of tolerance (e.g. temperature limits of corals)', 'biome patterns follow temperature and rainfall'], ['competition, predation and disease often limit species within physically suitable areas', 'mutualists such as pollinators are needed for many plants'], 'Abiotic factors determine where species could live (fundamental range), but biotic interactions often determine where they actually live.')],
  extended=[('Describe adaptations of named organisms to their habitats and explain how abiotic factors limit species distribution.', 'Marram grass: rolled leaves, sunken stomata, hairs, deep roots, rhizomes. Mangroves: pneumatophores, prop roots, salt glands. Range of tolerance; limiting factors; zones of stress and intolerance; biotic factors modify.', 8)],
  )

S('ch12-st2',
  terms=[('range of tolerance', 'the range of values of an abiotic factor within which a species can survive, with an optimum range in which it thrives'),
         ('transect', 'a line across a habitat along which samples are taken at intervals to study changes in distribution with an environmental gradient'),
         ('biome', 'a group of ecosystems with similar communities, shaped by similar temperature and rainfall patterns (e.g. tropical rainforest, desert, tundra)'),
         ('quadrat', 'a square frame of known area used to sample organisms in a habitat'),
         ('percentage cover', 'the percentage of the area of a quadrat occupied by a particular species'),
         ('zonation', 'the gradual change in distribution of species across a habitat in response to an environmental gradient, such as on a rocky shore')],
  facts=[('Which two abiotic factors mainly determine the distribution of terrestrial biomes?', 'temperature and rainfall', ['soil pH and wind', 'light and oxygen', 'altitude and day length'], 'Climographs plot these.'),
         ('Which biome has low rainfall and extreme temperature fluctuation?', 'hot desert', ['tropical rainforest', 'temperate deciduous forest', 'taiga'], 'Under 250 mm per year.'),
         ('Which sampling method is best to study how plant species change from the edge of a woodland into a field?', 'a belt transect', ['random quadrats in the field only', 'a single quadrat', 'capture–mark–release'], 'Transects follow gradients.'),
         ('Which biome is characterised by permafrost, low temperatures and low-growing vegetation?', 'tundra', ['savanna', 'tropical rainforest', 'temperate grassland'], 'Short growing season.')],
  mc2=[('Why are transects used rather than random quadrats when studying zonation?', 'Transects sample systematically along an environmental gradient, showing how distribution changes.', ['Random quadrats are always biased.', 'Transects need no measurements.', 'Transects only sample one species.'], 'Systematic sampling along the gradient.'),
       ('What happens to a population at the edges of its range of tolerance?', 'Individuals survive but grow and reproduce poorly (zone of physiological stress).', ['They reproduce fastest.', 'They are at their optimum.', 'They become a new species immediately.'], 'Optimum lies in the middle.'),
       ('Why do similar biomes on different continents have similar adaptations but different species?', 'Similar climates select for similar adaptations through convergent evolution.', ['The same species spread across oceans.', 'Climate does not affect organisms.', 'Different continents have identical species.'], 'E.g. cacti and euphorbias.')],
  mc3=[('A field ecologist wants to test whether light intensity limits the distribution of a fern in woodland. Which method is most appropriate?', 'measure fern percentage cover and light intensity in quadrats along a transect and test for correlation', ['count ferns in one quadrat', 'grow ferns in the dark only', 'measure rainfall across the country'], 'Correlation along a gradient.'),
       ('A climograph shows monthly temperatures 25–28 °C all year and rainfall over 200 mm every month. Which biome is it?', 'tropical rainforest', ['savanna', 'hot desert', 'temperate forest'], 'Hot and wet all year.')],
  why=[('Explain how a species’ range of tolerance determines its distribution.', 'Within the optimum range the population grows; towards the limits individuals are stressed and fewer survive or reproduce; beyond the limits they cannot survive; so the species occurs only where conditions fall within its tolerance range.'),
       ('Explain how a transect can be used to investigate the effect of an abiotic factor on the distribution of a species.', 'Lay a tape across the gradient (e.g. from shore to cliff); place quadrats at regular intervals; record abundance (percentage cover or counts) and measure the abiotic factor at each point; plot both and test for correlation (e.g. Spearman’s).'),
       ('Explain why biomes are distributed according to temperature and rainfall.', 'Temperature affects metabolic rates and growing season; rainfall affects water availability; together they determine the type of vegetation that can grow, which determines the animal communities; similar combinations produce similar biomes worldwide.')],
  contrast=[('a line transect', 'a belt transect', 'A line transect records organisms touching a line at intervals; a belt transect uses quadrats placed along the line, giving abundance data over a strip.'),
            ('tropical rainforest', 'temperate deciduous forest', 'Tropical rainforest is hot and wet all year with very high diversity and evergreen trees; temperate deciduous forest has distinct seasons with trees shedding leaves in winter and lower diversity.')],
  misc=[('The optimum range of tolerance is always at the edge of a species’ distribution.', 'The optimum is usually in the middle of the range; populations at the edges are under physiological stress.'),
        ('A correlation between light intensity and fern abundance proves that light causes the distribution.', 'Correlation does not prove causation; other factors (e.g. soil moisture) may vary with light; experiments are needed to test causation.')],
  cases=[('zonation on a rocky shore in Cape Town', 'From low to high tide line, kelp, mussels, limpets, barnacles and periwinkles occur in distinct bands.', 'the use of transects to study distribution', 'A transect up the shore reveals how tolerance of exposure and desiccation determines each species’ zone.'),
         ('coral reefs and sea temperature', 'Reef-building corals live mainly between 23 and 29 °C; above about 30 °C they bleach.', 'range of tolerance', 'Temperature outside the optimum stresses corals, limiting their distribution to warm, shallow tropical seas.')],
  evaluate=[('Transects are the most effective way to study species distribution in a habitat.', ['they reveal patterns along environmental gradients', 'they are simple and repeatable'], ['they may miss species between sampling points', 'random sampling is better for estimating population size where there is no gradient'], 'Transects are best for gradients; other methods (random quadrats, mark–recapture, eDNA) suit other questions.')],
  extended=[('Describe how the distribution of species can be investigated using transects and explain how range of tolerance and climate determine distribution.', 'Transect method: tape, quadrats at intervals, percentage cover, abiotic measurements (light meter, soil probe), correlation; range of tolerance curve (optimum, stress, intolerance); biomes by temperature and rainfall; climographs; examples.', 8)],
  )


def _transect_dq(rng, slot):
    dists = [0, 5, 10, 15, 20, 25, 30]
    spp = pick(rng, [('bracken (Pteridium aquilinum)', 'light intensity / lux', 'woodland edge into a field', lambda d: 2000 + 1300 * d, True),
                     ('sea pink (Armeria maritima)', 'soil salinity / ppt', 'cliff top inland from the sea', lambda d: max(1.0, 22 - 0.65 * d), True),
                     ('dog’s mercury (Mercurialis perennis)', 'light intensity / lux', 'open meadow into a beech wood', lambda d: max(300, 25000 - 800 * d), False),
                     ('heather (Calluna vulgaris)', 'soil pH', 'acid moorland to a limestone grassland', lambda d: 4.0 + 0.1 * d, False)])
    sp, ab, where, fx, pos = spp
    xs = [round(fx(d) * rng.uniform(0.95, 1.05), 1 if 'pH' in ab or 'ppt' in ab else -2) for d in dists]
    base = rng.uniform(55, 80)
    if pos:
        cov = [max(0, round(base - 2.2 * d + rng.uniform(-6, 6))) for d in dists[::-1]]
        cov = cov[::-1] if 'salinity' not in ab else [max(0, round(base * (1 - d / 35) + rng.uniform(-5, 5))) for d in dists]
    else:
        cov = [max(0, round(10 + 2.0 * d + rng.uniform(-5, 5))) for d in dists]
    if len(set(cov)) < 4:
        return None
    m = mean(cov)
    hi = dists[cov.index(max(cov))]
    intro = (f'A belt transect was set up from the {where}. At 5 m intervals a 1 m² quadrat was used to estimate the percentage cover of {sp}, and {ab.split(" /")[0]} was measured.\n\n'
             + table(['Distance / m', f'Percentage cover of {sp.split(" (")[0]}', ab], [(d, c, f'{x:g}') for d, c, x in zip(dists, cov, xs)]))
    parts = [
        ('State the distance at which the percentage cover was highest.', f'{hi} m', f'{hi} m (A1).', 1),
        ('Calculate the mean percentage cover along the transect.', f'{m:.1f} %', f'Sum {sum(cov)} ÷ 7 = {m:.1f} % (A1).', 1),
        (f'Describe the relationship between {ab.split(" /")[0]} and the percentage cover.', 'Percentage cover changes as the abiotic factor changes along the transect (describe direction from the table).', 'Correct direction of relationship (A1); use of data (A1).', 2),
        ('Explain why a correlation coefficient would be calculated and why it would not prove causation.', 'To quantify the strength and direction of the relationship and test its significance; other factors that vary along the transect (e.g. soil moisture, competition, grazing) could be responsible.', 'Quantify strength/significance (A1); confounding variables (A1).', 2),
        ('Outline how percentage cover is estimated.', 'Use a quadrat divided into 100 small squares (or a 10 × 10 grid); count squares more than half covered by the species; each square = 1 %.', 'Grid squares counted (A1); conversion to percentage (A1).', 2),
        ('Suggest two improvements to increase the reliability of the data.', 'Repeat the transect in parallel lines; use smaller intervals; take several readings of the abiotic factor at each point; sample at the same time of day.', 'Two valid improvements (A1 A1).', 2),
        ('Explain the distribution of the species in terms of range of tolerance.', 'Where the factor is within the species’ optimum range, it grows well and has high cover; towards the limits it is stressed and cover falls; beyond, it is absent.', 'Optimum vs stress zones linked to data (R1).', 1),
        ('Explain why a transect rather than random quadrats was used.', 'The investigation studies how distribution changes along an environmental gradient, so systematic sampling along a line is appropriate.', 'Environmental gradient (A1); systematic sampling (A1).', 2),
    ]
    return intro, parts


data_q(R, 'ch12-st2', _transect_dq)


@R.add('ch12-st2', 'C3', (1, 4), 'numerical')
def quadrat_density(rng, slot):
    sp = pick(rng, ['daisies (Bellis perennis)', 'dandelions', 'limpets', 'barnacles', 'plantains', 'buttercups'])
    q = pick(rng, [0.25, 0.5, 1.0])
    counts = [rng.randint(0, 18) for _ in range(rng.randint(6, 10))]
    area = pick(rng, [50, 100, 200, 400, 1200])
    m = mean(counts)
    dens = m / q
    stem = (f'{len(counts)} randomly placed quadrats, each {q} m², were used to sample {sp} on a {area} m² field. The counts were {", ".join(map(str, counts))}. Calculate the mean density per m² and estimate the population in the whole field.')
    return num(stem, f'{dens:.1f} per m²; about {dens * area:.0f}', f'Mean per quadrat = {m:.2f} (A1); ÷ {q} = {dens:.1f} m⁻² (A1); × {area} = {dens * area:.0f} (A1).', 3)


S('ch12-st3',
  terms=[('ecological niche', 'the role of a species in an ecosystem, including its habitat, its use of resources and all its interactions with other species and abiotic factors'),
         ('obligate anaerobe', 'an organism that can only survive in the absence of oxygen, for which oxygen is toxic'),
         ('facultative anaerobe', 'an organism that respires aerobically when oxygen is present but can switch to anaerobic respiration when it is absent'),
         ('obligate aerobe', 'an organism that requires oxygen for respiration and cannot survive without it'),
         ('mixotroph', 'an organism that can use both autotrophic and heterotrophic nutrition, such as Euglena'),
         ('saprotroph', 'a heterotroph that obtains nutrients by secreting digestive enzymes onto dead organic matter and absorbing the products')],
  facts=[('Which organism is an example of an obligate anaerobe?', 'Clostridium botulinum', ['humans', 'Saccharomyces cerevisiae', 'Euglena'], 'Grows only without oxygen.'),
         ('Which organism is a facultative anaerobe?', 'yeast (Saccharomyces cerevisiae)', ['Clostridium tetani', 'humans', 'an oak tree'], 'Respires aerobically or ferments.'),
         ('Which organism is a mixotroph?', 'Euglena gracilis', ['a mushroom', 'a lion', 'a cyanobacterium only'], 'Photosynthesises in light, ingests food in darkness.'),
         ('How do saprotrophic fungi obtain nutrition?', 'by extracellular digestion of dead organic matter and absorption', ['by photosynthesis', 'by ingesting whole prey', 'by chemosynthesis'], 'Enzymes secreted onto the substrate.'),
         ('What is the energy source for chemoautotrophic archaea at hydrothermal vents?', 'oxidation of inorganic chemicals such as hydrogen sulfide', ['sunlight', 'dead organic matter', 'ingesting other cells'], 'Chemoautotrophs fix carbon using chemical energy.')],
  mc2=[('Why can no two species occupy exactly the same niche indefinitely?', 'One would outcompete the other for the same resources (competitive exclusion).', ['They would interbreed.', 'They would become one species.', 'Niches are infinite.'], 'Gause’s principle.'),
       ('Why is oxygen toxic to obligate anaerobes?', 'They lack enzymes to detoxify reactive oxygen species formed from O₂.', ['They cannot breathe.', 'Oxygen dissolves their cell walls.', 'They photosynthesise.'], 'Lacking catalase/superoxide dismutase.'),
       ('Which statement about archaea is correct?', 'They show great metabolic diversity, including methanogens and chemoautotrophs.', ['They are all photosynthetic.', 'They are all parasites.', 'They are eukaryotes.'], 'Archaea use diverse energy sources.')],
  mc3=[('A bacterium grows throughout a tube of nutrient broth but most densely at the top where oxygen is highest. What is it most likely to be?', 'a facultative anaerobe', ['an obligate anaerobe', 'an obligate aerobe that cannot grow lower down', 'a virus'], 'Grows with or without O₂, better with it.'),
       ('Euglena kept in continuous darkness with dissolved organic nutrients survives and grows. What does this show?', 'It can switch to heterotrophic nutrition (mixotrophy).', ['It is an obligate autotroph.', 'It is a chemoautotroph.', 'It photosynthesises in the dark.'], 'Mixotrophs use both modes.')],
  why=[('Explain the difference between autotrophic and heterotrophic nutrition.', 'Autotrophs make their own organic compounds from inorganic carbon (CO₂) using energy from light (photoautotrophs) or chemical reactions (chemoautotrophs); heterotrophs obtain carbon compounds from other organisms by ingestion, absorption (saprotrophs) or parasitism.'),
       ('Explain how the niche of a species is defined.', 'The niche includes where the species lives (spatial habitat), when it is active, what it eats, its predators, competitors and parasites, and its tolerance of abiotic factors – its total role in the ecosystem.'),
       ('Explain why some organisms are obligate anaerobes and others obligate aerobes.', 'Obligate aerobes depend on oxygen as the final electron acceptor in respiration; obligate anaerobes lack the enzymes to cope with oxygen and use other metabolic pathways, so they live only in anoxic environments such as deep mud or the gut.')],
  contrast=[('obligate anaerobes', 'facultative anaerobes', 'Obligate anaerobes cannot survive in oxygen; facultative anaerobes respire aerobically when oxygen is available but can switch to anaerobic metabolism when it is absent.'),
            ('holozoic nutrition', 'saprotrophic nutrition', 'Holozoic organisms ingest food and digest it internally (e.g. animals); saprotrophs secrete enzymes onto dead matter and absorb the products externally (e.g. fungi).')],
  misc=[('All bacteria need oxygen to survive.', 'Many bacteria are facultative or obligate anaerobes; some are killed by oxygen.'),
        ('The niche of a species is the same as its habitat.', 'The habitat is where it lives; the niche is its full role, including resources used and interactions.')],
  cases=[('Euglena gracilis in ponds', 'Euglena photosynthesises using chloroplasts in light and absorbs or ingests organic matter in darkness.', 'mixotrophic nutrition', 'Using both modes allows it to survive changing light conditions.'),
         ('methanogenic archaea in the rumen of cattle', 'Archaea in the anaerobic rumen produce methane from CO₂ and hydrogen.', 'obligate anaerobic metabolism', 'They can only live in oxygen-free environments and occupy a niche in the digestive system.')],
  evaluate=[('Classifying organisms by mode of nutrition is clear-cut.', ['most organisms clearly fit autotroph or heterotroph categories', 'the categories reflect fundamental differences in metabolism'], ['mixotrophs such as Euglena and carnivorous plants use both modes', 'some parasitic plants have lost photosynthesis partly or completely'], 'The categories are useful but nutrition is a spectrum, and mixotrophs show the boundary is not clear-cut.')],
  extended=[('Describe the different modes of nutrition found in living organisms, with a named example of each.', 'Photoautotrophs (plants, cyanobacteria), chemoautotrophs (vent archaea, nitrifying bacteria), holozoic heterotrophs (animals), saprotrophs (fungi, decomposer bacteria), mixotrophs (Euglena), parasites; obligate and facultative anaerobes (Clostridium, yeast); diversity of archaea.', 8)],
  )

S('ch12-st4',
  terms=[('competitive exclusion principle', 'the principle that two species competing for exactly the same limited resources cannot coexist indefinitely; one will outcompete the other'),
         ('fundamental niche', 'the full range of conditions and resources a species could use in the absence of competitors'),
         ('realised niche', 'the actual range of conditions and resources a species uses when competitors are present'),
         ('herbivory', 'the consumption of plants or plant parts by animals'),
         ('interspecific competition', 'competition between individuals of different species for the same limited resources')],
  facts=[('Who demonstrated competitive exclusion using two Paramecium species?', 'Georgy Gause', ['Charles Darwin', 'Gregor Mendel', 'Joseph Connell'], 'P. aurelia outcompeted P. caudatum in mixed cultures.'),
         ('Which is an adaptation of plants against herbivory?', 'production of toxins such as alkaloids', ['bright flowers', 'large leaves', 'shallow roots'], 'Also spines and tough leaves.'),
         ('Which is an adaptation of predators for catching prey?', 'forward-facing eyes for binocular vision', ['camouflage to hide from predators', 'toxic skin', 'warning colouration'], 'Judging distance aids pouncing.'),
         ('What is the realised niche of a species?', 'the part of its fundamental niche it actually occupies when competitors are present', ['the niche it would occupy without competitors', 'its habitat only', 'its geographical range'], 'Competition restricts the niche.')],
  mc2=[('In Connell’s barnacle study, Chthamalus survived lower on the shore when Balanus was removed. What does this show?', 'Its realised niche is restricted by competition with Balanus.', ['Chthamalus cannot survive low on the shore.', 'Balanus helps Chthamalus.', 'Both share one niche without competition.'], 'Fundamental niche larger than realised niche.'),
       ('Why do monarch butterflies tolerate the toxins of milkweed?', 'They have evolved resistance and store the toxins as a defence against predators.', ['Milkweed has no toxins.', 'They detoxify all plants.', 'They avoid eating milkweed.'], 'Co-evolution of herbivore and plant.'),
       ('Why might two species with similar diets coexist?', 'They partition resources, e.g. feeding at different times or heights.', ['They never compete.', 'One species always dies.', 'They interbreed.'], 'Niche differentiation reduces competition.')],
  mc3=[('In Gause’s experiment, P. aurelia grew from 2 to 160 individuals per 0.5 cm³ in 8 days in pure culture. What was the mean rate of increase?', '19.75 individuals per 0.5 cm³ per day', ['20 individuals per day', '80 individuals per day', '2.5 individuals per day'], '(160 − 2)/8 = 19.75.'),
       ('Five warbler species feed in the same spruce trees in different zones of the canopy (MacArthur, 1958). What does this illustrate?', 'resource partitioning reducing competition', ['competitive exclusion', 'predation', 'mutualism'], 'Different realised niches allow coexistence.')],
  why=[('Explain the competitive exclusion principle using a named example.', 'Gause grew Paramecium aurelia and P. caudatum separately – both grew; together, competing for the same bacterial food, P. aurelia always outcompeted P. caudatum, which died out; two species cannot occupy the same niche indefinitely.'),
       ('Explain how adaptations of predators and prey result from natural selection.', 'Prey with better defences (camouflage, speed, toxins) survive and reproduce more; predators with better hunting adaptations (speed, senses, teeth) catch more prey and reproduce more; this produces an evolutionary arms race in which both improve over generations.'),
       ('Explain the difference between a fundamental and a realised niche.', 'The fundamental niche is everything a species could use without competitors; the realised niche is what it actually uses with competition; interspecific competition usually makes the realised niche smaller.')],
  contrast=[('the fundamental niche', 'the realised niche', 'The fundamental niche is the potential range of conditions and resources without competitors; the realised niche is the actual, usually smaller, range occupied in the presence of competitors.'),
            ('physical defences of plants', 'chemical defences of plants', 'Physical defences (spines, hairs, tough leaves) deter feeding mechanically; chemical defences (alkaloids, tannins, cyanogenic glycosides) make tissues toxic or unpalatable.')],
  misc=[('Competitive exclusion means competing species always fight each other.', 'Exclusion results from more efficient use of shared limited resources, not necessarily direct aggression.'),
        ('Prey adaptations evolve so that prey species are never eaten.', 'Adaptations increase the chance of survival of individuals; predation still occurs and predators also evolve.')],
  cases=[('Connell’s study of barnacles on the Isle of Cumbrae, Scotland', 'Chthamalus stellatus lived high on the shore and Balanus balanoides lower; when Balanus was removed, Chthamalus survived lower down.', 'fundamental and realised niches', 'Competition from Balanus restricted Chthamalus to a realised niche smaller than its fundamental niche.'),
         ('Gause’s Paramecium experiments (1934)', 'P. aurelia and P. caudatum both grew alone, but in mixed culture P. caudatum died out.', 'the competitive exclusion principle', 'The species with greater growth rate on the shared resource excluded the other.')],
  evaluate=[('Competition is the main factor determining the structure of ecological communities.', ['classic experiments (Gause, Connell) show competition can exclude species and restrict niches', 'resource partitioning patterns are widespread'], ['predation, disease and disturbance often keep populations below levels at which competition matters', 'mutualism and facilitation also shape communities'], 'Competition is important, especially among similar species, but communities are structured by many interacting factors.')],
  extended=[('Explain the competitive exclusion principle and describe adaptations for herbivory, predation and defence against them.', 'Gause; Connell; fundamental vs realised niche; resource partitioning (warblers). Herbivore adaptations: grinding teeth, cellulose-digesting microbes, detoxification (monarch). Plant defences: spines, toxins. Predator adaptations: speed, senses, venom; prey: camouflage, mimicry, toxins, warning colours; arms race.', 8)],
  )


def _gause_dq(rng, slot):
    days = [0, 2, 4, 6, 8, 10, 12, 14, 16]
    K1 = rng.randint(180, 220)
    K2 = rng.randint(120, 150)
    r1 = rng.uniform(0.75, 0.95)
    r2 = rng.uniform(0.6, 0.8)
    a = [round(K1 / (1 + (K1 / 2 - 1) * math.exp(-r1 * d))) for d in days]
    c = [round(K2 / (1 + (K2 / 2 - 1) * math.exp(-r2 * d))) for d in days]
    mix_a = [round(x * 0.92) for x in a]
    mix_c = [max(0, round(y * (1 - 0.075 * d))) if d > 4 else round(y * 0.9) for d, y in zip(days, c)]
    intro = ('In experiments similar to Gause’s, Paramecium aurelia and P. caudatum were grown separately and then together in tubes of nutrient medium containing bacteria as food. The number of individuals per 0.5 cm³ was recorded.\n\n'
             + table(['Day', 'P. aurelia alone', 'P. caudatum alone', 'P. aurelia (mixed)', 'P. caudatum (mixed)'], list(zip(days, a, c, mix_a, mix_c))))
    rate = (a[4] - a[0]) / 8
    pc = pct_change(c[-1], mix_c[-1]) if c[-1] else 0
    parts = [
        ('Calculate the mean rate of increase of P. aurelia alone between day 0 and day 8.', f'{rate:.1f} individuals per 0.5 cm³ per day', f'({a[4]} − {a[0]})/8 (M1) = {rate:.1f} (A1).', 2),
        ('Calculate the percentage difference between the final population of P. caudatum grown alone and in mixed culture.', f'{pc:.0f} %', f'({mix_c[-1]} − {c[-1]})/{c[-1]} × 100 (M1) = {pc:.0f} % (A1).', 2),
        ('Describe the growth of P. aurelia when grown alone.', 'Slow initial increase, then rapid (exponential) growth, then levelling off at about ' + str(K1) + ' – sigmoid curve.', 'Sigmoid shape (A1); plateau value from data (A1).', 2),
        ('Explain the results for the mixed culture.', 'Both compete for the same limited bacterial food; P. aurelia grows faster/uses food more efficiently; P. caudatum declines and is excluded – competitive exclusion.', 'Same resource / interspecific competition (A1); P. aurelia more efficient (A1); exclusion (A1).', 3),
        ('State the principle illustrated by these results.', 'Competitive exclusion: two species with the same niche cannot coexist indefinitely.', 'Competitive exclusion (A1).', 1),
        ('Suggest why P. aurelia in mixed culture reaches a slightly lower population than when grown alone.', 'Some food is consumed by P. caudatum before it is excluded.', 'Shared resource early on (A1).', 1),
        ('Outline one limitation of applying these results to natural ecosystems.', 'Laboratory conditions are uniform and simple; in nature, habitat variation allows resource partitioning, and predators/disturbance may prevent exclusion.', 'Valid limitation (A1).', 1),
    ]
    return intro, parts


data_q(R, 'ch12-st4', _gause_dq)
