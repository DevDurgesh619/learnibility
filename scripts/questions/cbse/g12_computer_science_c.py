"""CBSE class 12 Computer Science (083), chapters 5-6: computer networks and data communication.

The network-design case (the board's 5-mark Section E question) is generated with computed answers:
server block = block with the most computers, star layout from it, repeaters on links over 100 m.
Also reused by Informatics Practices (065) chapter 5.
"""
from __future__ import annotations

import random

from qbank import F, mcq, num, CITIES
from g12_computer_science_kit import ST, uniq, NAMES

S = 'cbse-g12-computer-science-ch'

ORGS = ['Vidya Vikas Trust', 'Gyan Deep Academy', 'Arogya Health Services', 'Navyug Software Solutions', 'Krishi Kalyan Institute',
        'Sanjeevani Care Centre', 'Kalpana Design Studio', 'Swasthya Diagnostics', 'Pragati Logistics', 'Shiksha Sadan University',
        'Udaan Aviation Academy', 'Tarang Media House', 'Saksham Skill Centre', 'Jeevan Rekha Foundation']
BLOCKS = ['ADMIN', 'ACCOUNTS', 'HR', 'TRAINING', 'LAB', 'LIBRARY', 'RESEARCH', 'LOGISTICS', 'FINANCE', 'DESIGN', 'SALES', 'MEDIA', 'ACADEMIC', 'HOSTEL']
V_PARTS = [
    ('Which type of network (PAN, LAN, MAN or WAN) will be formed when the campus is connected to the head office in {ho}?', 'WAN, because the campus and head office are in different cities, far apart.'),
    ('Suggest the protocol or technology for making voice calls over the Internet between the campus and the head office.', 'VoIP (Voice over Internet Protocol).'),
    ('Suggest the most suitable wired medium to connect the blocks of the campus for very high-speed, interference-free data transfer.', 'Optical fibre cable.'),
    ('Which device should be installed to connect the campus network to the Internet and route data to other networks?', 'A router (with a modem from the Internet service provider).'),
    ('The company wants to prevent unauthorised access to its network from the Internet. What should be installed?', 'A firewall (hardware or software) at the point where the campus connects to the Internet.'),
    ('Which protocol should be used to transfer large files from the campus server to the head office?', 'FTP (File Transfer Protocol).'),
]


def campus(r):
    org = r.choice(ORGS)
    city, ho = r.sample(CITIES, 2)
    bl = r.sample(BLOCKS, 4)
    pcs = sorted(r.sample(range(10, 70), 3)) + [r.randint(90, 160)]
    r.shuffle(pcs)
    srv = bl[pcs.index(max(pcs))]
    pairs = [(a, b) for i, a in enumerate(bl) for b in bl[i + 1:]]
    for _ in range(100):
        dist = {p: r.choice(range(30, 300, 5)) for p in pairs}
        from_srv = {b: dist[(srv, b)] if (srv, b) in dist else dist[(b, srv)] for b in bl if b != srv}
        far = [b for b, d in from_srv.items() if d > 100]
        if 1 <= len(far) <= 2:
            break
    else:
        raise ValueError('dist')
    return org, city, ho, bl, pcs, srv, dist, from_srv, far


def campus_case(r, ho_km=None):
    org, city, ho, bl, pcs, srv, dist, from_srv, far = campus(r)
    dt = '\n'.join(f'{a} to {b}: {d} m' for (a, b), d in dist.items())
    ct = '\n'.join(f'{b}: {p}' for b, p in zip(bl, pcs))
    v = r.choice(V_PARTS)
    iv = r.choice([('Which device should be used to connect all the computers within each block?', 'A switch (an intelligent device that sends data only to the intended computer).'),
                   ('Suggest a suitable topology for connecting the computers inside each block, and the device at its centre.', 'Star topology with a switch at the centre of each block.')])
    stem = (f'{org} is setting up its campus in {city} with four blocks: {", ".join(bl)}. Its head office is in {ho}, about {r.choice([900, 1200, 1500, 1800, 2100])} km away.\n'
            f'Distances between the blocks:\n{dt}\nNumber of computers in each block:\n{ct}\n'
            f'(i) Suggest the most suitable block to house the server, with a reason.\n'
            f'(ii) Suggest a cable layout (block to block) for connecting the blocks efficiently.\n'
            f'(iii) Between which blocks should a repeater be placed, if the layout in (ii) is used and Ethernet cable is used for connections?\n'
            f'(iv) {iv[0]}\n(v) {v[0].format(ho=ho)}')
    lay = ', '.join(f'{srv}–{b}' for b in bl if b != srv)
    rep = ', '.join(f'{srv} and {b} ({from_srv[b]} m)' for b in far)
    ans = (f'(i) {srv}, because it has the maximum number of computers ({max(pcs)}); most traffic stays within the block (80:20 rule).\n'
           f'(ii) Star layout with {srv} at the centre: {lay}.\n'
           f'(iii) Between {rep}, as the distance is more than 100 m.\n(iv) {iv[1]}\n(v) {v[1]}')
    return {'stem': stem, 'answer': ans, 'key': '1 mark for each part (i)–(v); in (ii) any efficient layout centred on the server block earns the mark.', 'marks': 5}


def server_pick(r):
    org, city, ho, bl, pcs, srv, dist, from_srv, far = campus(r)
    ct = ', '.join(f'{b} {p}' for b, p in zip(bl, pcs))
    wrong = [b for b in bl if b != srv]
    return mcq(f'{org} has four blocks with these numbers of computers: {ct}. In which block should the server be placed?', srv, wrong,
               f'{srv} has the most computers, so placing the server there keeps most traffic local (80:20 rule).', r)


def repeater_pick(r):
    org, city, ho, bl, pcs, srv, dist, from_srv, far = campus(r)
    b = far[0]
    near = [x for x in bl if x != srv and x not in far]
    if not near:
        raise ValueError('near')
    d1, d2 = from_srv[b], from_srv[near[0]]
    ans = f'Between {srv} and {b}'
    wrong = [f'Between {srv} and {near[0]}', f'Inside the {srv} block only', 'No repeater is needed']
    return mcq(f'In a star layout centred on {srv}, the {srv}–{b} link is {d1} m and the {srv}–{near[0]} link is {d2} m long (Ethernet cable). Where is a repeater needed?',
               ans, wrong, f'Ethernet signals weaken beyond about 100 m; the {d1} m link needs a repeater.', r)


def mesh_count(r):
    n = r.randint(4, 12)
    t = r.randrange(3)
    if t == 0:
        a = n * (n - 1) // 2
        return {'stem': f'How many cables are needed to connect {n} computers in a fully connected mesh topology?', 'answer': str(a),
                'key': f'n(n − 1)/2 = {n} × {n - 1} / 2 = {a}.', 'distractors': [str(n * (n - 1)), str(n), str(n - 1), str(a + n)]}
    if t == 1:
        return {'stem': f'In a mesh topology of {n} computers, how many ports (network connections) does each computer need?', 'answer': str(n - 1),
                'key': f'Each node connects to the other {n - 1} nodes.', 'distractors': [str(n), str(n * (n - 1) // 2), str(n + 1), '1']}
    return {'stem': f'How many cables are needed to connect {n} computers to a central switch in a star topology?', 'answer': str(n),
            'key': f'One cable from each of the {n} computers to the switch.', 'distractors': [str(n - 1), str(n * (n - 1) // 2), str(n + 1), '1']}


TOPO_SCEN = [
    ('All computers are connected to a single backbone cable with terminators at both ends.', 'Bus'),
    ('Each computer is connected by its own cable to a central switch.', 'Star'),
    ('Every computer has a dedicated point-to-point link to every other computer.', 'Mesh'),
    ('Several star networks are connected together in a hierarchy, like branches from a root.', 'Tree'),
    ('If the central device fails, the whole network stops working, but one faulty cable affects only one computer.', 'Star'),
    ('A break in the main cable stops communication for all computers on the network.', 'Bus'),
    ('It is the most reliable layout because data can take another path if one link fails, but it needs the most cabling.', 'Mesh'),
    ('It is suitable for a school where each floor has a star network and the floors are linked to a main switch.', 'Tree'),
    ('It needs the least cable because all nodes share one line, and only one computer can transmit at a time.', 'Bus'),
    ('New computers are added easily by running one more cable to the hub or switch.', 'Star'),
]


def topo_pick(r):
    d, t = r.choice(TOPO_SCEN)
    return mcq(f'Identify the network topology: {d}', t, [x for x in ['Bus', 'Star', 'Mesh', 'Tree'] if x != t], f'This describes {t.lower()} topology.', r)


DEV_SCEN = [
    ('converts digital signals of a computer into analog signals for a telephone line and back', 'Modem'),
    ('regenerates a weak signal so that it can travel a longer distance', 'Repeater'),
    ('sends incoming data to all its ports, whatever the destination', 'Hub'),
    ('sends data only to the port of the destination computer using its MAC address', 'Switch'),
    ('forwards data packets between different networks using IP addresses', 'Router'),
    ('connects two networks that use different protocols and acts as the entry and exit point of a network', 'Gateway'),
    ('is installed in a computer to connect it to a wired network and has a unique MAC address', 'Ethernet card (NIC)'),
    ('is an 8-pin connector used at the ends of twisted-pair Ethernet cables', 'RJ45 connector'),
    ('lets a computer connect to a wireless network', 'Wi-Fi card'),
]
DEVS = [d for _, d in DEV_SCEN]


def dev_pick(r):
    d, t = r.choice(DEV_SCEN)
    wrong = r.sample([x for x in DEVS if x != t], 3)
    who = r.choice(NAMES)
    return mcq(f'{who} needs a device that {d}. Which device is it?', t, wrong, f'A {t} {d}.', r)


PROT_SCEN = [
    ('send an e-mail from a mail client to a mail server', 'SMTP'), ('download e-mails from a mail server to a personal computer', 'POP3'),
    ('upload a large set of files to a web server', 'FTP'), ('view a web page in a browser without encryption', 'HTTP'),
    ('open an online banking website securely, with data encrypted', 'HTTPS'), ('make voice calls over the Internet', 'VoIP'),
    ('log in to a remote computer and work on it as if sitting at its terminal', 'TELNET'),
    ('connect two computers directly over a serial link, as in dial-up Internet', 'PPP'),
    ('break data into packets and deliver them reliably with addresses across the Internet', 'TCP/IP'),
]
PROTS = [p for _, p in PROT_SCEN]


def prot_pick(r):
    d, t = r.choice(PROT_SCEN)
    who = r.choice(NAMES)
    return mcq(f'{who} wants to {d}. Which protocol is used?', t, r.sample([x for x in PROTS if x != t], 3), f'{t} is used to {d}.', r)


NET_SCEN = [
    ('A smartphone shares its Internet connection with a laptop on the same desk through Bluetooth.', 'PAN'),
    ('Computers in the labs and offices of a school building are connected to share a printer and files.', 'LAN'),
    ('The cable TV network that covers a whole city.', 'MAN'),
    ('A bank connects its branches in different countries to its main server.', 'WAN'),
    ('A smartwatch is connected to its owner\'s phone.', 'PAN'),
    ('The offices of a company on different floors of one building are networked.', 'LAN'),
    ('The branches of a college spread across one city are connected.', 'MAN'),
    ('The Internet, which connects networks across the world.', 'WAN'),
]


def net_pick(r):
    d, t = r.choice(NET_SCEN)
    return mcq(f'Identify the type of network: {d}', t, [x for x in ['PAN', 'LAN', 'MAN', 'WAN'] if x != t], f'{t}: matches the area covered.', r)


SITES = ['gyandeep', 'vidyavikas', 'krishikalyan', 'swasthya', 'navyugsoft', 'tarangmedia', 'udaanacademy', 'pragatilogi']
TLDS = [('in', 'India (country code)'), ('com', 'commercial'), ('org', 'organisation'), ('edu', 'educational'), ('gov.in', 'Indian government'), ('net', 'network')]


def url_parts(r):
    site = r.choice(SITES)
    tld, _ = r.choice(TLDS)
    proto = r.choice(['https', 'http'])
    path = r.choice(['admissions', 'results', 'notices', 'courses', 'events', 'downloads'])
    page = r.choice(['index.html', 'class12.html', 'fees.html', 'list.php', 'apply.html'])
    url = f'{proto}://www.{site}.{tld}/{path}/{page}'
    t = r.randrange(3)
    if t == 0:
        a = f'www.{site}.{tld}'
        return mcq(f'Identify the domain name in the URL {url}', a, [f'{proto}://www.{site}.{tld}', f'{path}/{page}', f'{site}'], f'The domain name is {a}.', r)
    if t == 1:
        a = proto.upper()
        return mcq(f'Which protocol is used to access the URL {url}?', a, [x for x in ['HTTP', 'HTTPS', 'FTP', 'SMTP'] if x != a][:3], f'The URL begins with {proto}://.', r)
    a = tld
    return mcq(f'What is the top-level domain in the URL {url}?', a, uniq([t2 for t2, _ in TLDS if t2 != tld] + [site], [a])[:3], f'The top-level domain is .{tld}.', r)


def net_compare(r):
    rows = [('Differentiate between a hub and a switch.', 'A hub broadcasts data to all ports and is not intelligent; a switch sends data only to the destination port using MAC addresses, reducing traffic.'),
            ('Differentiate between a router and a gateway.', 'A router forwards packets between networks using the same protocol; a gateway connects networks with different protocols and translates between them.'),
            ('Differentiate between star and bus topology (two points).', 'Star: each node has its own cable to a central device; one cable fault affects one node; central device failure stops all. Bus: one backbone cable; cheap; backbone fault stops the network.'),
            ('Differentiate between LAN and WAN.', 'LAN covers a small area (building/campus), high speed, privately owned; WAN covers countries or continents, lower speed, uses public/leased lines; e.g. Internet.'),
            ('Differentiate between HTML and XML.', 'HTML displays data using predefined tags; XML stores and transports data using user-defined tags; XML is case-sensitive and strict.'),
            ('Differentiate between a web browser and a web server.', 'A browser is client software that requests and displays web pages (e.g. Chrome); a web server stores websites and sends pages on request (e.g. Apache).'),
            ('Differentiate between SMTP and POP3.', 'SMTP sends (pushes) e-mail from client to server and between servers; POP3 downloads (pulls) e-mail from the server to the client.'),
            ('Differentiate between HTTP and HTTPS.', 'HTTP transfers web pages as plain text; HTTPS encrypts the data using SSL/TLS, so it is secure for banking and login pages.'),
            ('What is the role of a modem? Expand the term.', 'Modem = MOdulator–DEModulator; it converts digital data to analog signals for transmission over telephone lines and back.'),
            ('Write the full forms: (i) TCP/IP (ii) VoIP.', '(i) Transmission Control Protocol/Internet Protocol (ii) Voice over Internet Protocol.'),
            ('Write the full forms: (i) ARPANET (ii) NSFNET.', '(i) Advanced Research Projects Agency Network (ii) National Science Foundation Network.'),
            ('What is a URL? Write its parts with an example.', 'Uniform Resource Locator: the address of a resource on the web, e.g. https://www.cbse.gov.in/index.html – protocol (https), domain name, path/file name.')]
    from g12_computer_science_kit import deck
    d = deck(rows)

    def gen(rr):
        q, a = d(rr)
        return {'stem': q, 'answer': a, 'key': '2 marks: 1 mark for each correct point.', 'marks': 2}
    return gen


CH05 = [ST(S + '05-st1', 'evolution and types of networks', """
T: computer network | an interconnection of two or more computers or devices that can share data and resources
T: ARPANET | Advanced Research Projects Agency Network, the network started in 1969 by the US Department of Defense that is the forerunner of the Internet
T: NSFNET | the network started by the National Science Foundation of the USA in the mid-1980s to connect universities and research centres
T: Internet | the global network of networks that uses TCP/IP to connect millions of computers
T: PAN | Personal Area Network, a network of devices of one person within about 10 metres
T: LAN | Local Area Network, a network within a building or campus, up to about a kilometre
T: MAN | Metropolitan Area Network, a network that extends over a city
T: WAN | Wide Area Network, a network that spans states, countries or continents
Q: The first network that led to the Internet was: | ARPANET | NSFNET | ETHERNET | INTRANET
Q: ARPANET was started in the year: | 1969 | 1989 | 1957 | 1991
Q: The largest WAN in the world is: | the Internet | NSFNET | ARPANET | an intranet
Q: A network connecting a mobile phone and wireless earbuds is a: | PAN | LAN | MAN | WAN
Q: A network covering a whole city, such as a cable TV network, is a: | MAN | LAN | PAN | WAN
Q: A network covering a school campus is a: | LAN | PAN | MAN | WAN
S+: A network allows users to share resources such as printers, files and Internet connections
S+: LANs usually provide higher data transfer rates than WANs
S+: The Internet is a network of networks
S+: A WAN often uses public telephone lines, satellites or leased lines
S-: A PAN covers a whole city | A PAN covers a few metres around one person; a MAN covers a city
S-: NSFNET was the first network that led to the Internet | ARPANET (1969) was the first; NSFNET came later
S-: A LAN connects computers in different countries | A LAN is limited to a building or campus; a WAN connects countries
C: The Internet can connect computers all over the world | it is a network of networks using the common TCP/IP protocols
C: LANs are faster than WANs | the distances are short and the cables belong to the organisation
M:network: PAN | about 10 metres around a person
M:network: LAN | a building or campus
M:network: MAN | a city
M:network: WAN | countries and continents
X: C2 D2 2 | Give two advantages of networking computers. | Sharing resources (printer, Internet), sharing data and files, communication (e-mail, chat), centralised backup, cost saving (any two).
"""), ST(S + '05-st2', 'network devices', """
T: modem | a device that converts digital signals to analog signals (modulation) and analog back to digital (demodulation)
T: Ethernet card | a network interface card (NIC) fitted in a computer to connect it to a wired network; it has a unique MAC address
T: RJ45 | an eight-pin connector used at the ends of twisted-pair Ethernet cables
T: repeater | a device that regenerates and amplifies weak signals so that they can travel longer distances
T: hub | a device with many ports that broadcasts incoming data to all connected computers
T: switch | a device that forwards incoming data only to the port of the intended computer using its MAC address
T: router | a device that connects different networks and forwards data packets using IP addresses
T: gateway | a device that connects networks using different protocols and serves as the entry and exit point of a network
Q: Which device is called an intelligent hub? | Switch | Repeater | Modem | RJ45
Q: Which device is needed when a cable run is longer than about 100 metres? | Repeater | Hub | Modem | Ethernet card
Q: A MAC address is assigned to the: | network interface card | router port only | website | modem cable
Q: Which device converts digital signals into analog signals? | Modem | Switch | Hub | Repeater
Q: Which device connects a LAN to the Internet and decides the route of packets? | Router | Hub | Repeater | RJ45
Q: The MAC address is a: | 48-bit physical address | 32-bit IP address | domain name | port number
S+: A hub sends data to all computers connected to it
S+: A switch reduces unnecessary traffic by sending data only to the destination
S+: A router can connect networks that use the same protocol
S+: A gateway can translate between different protocols
S+: An Ethernet card has a unique physical address called the MAC address
S-: A hub sends data only to the destination computer | A hub broadcasts to all ports; a switch sends to the destination
S-: A repeater connects two different networks | A repeater only regenerates signals; a router or gateway connects networks
S-: RJ45 is a device that amplifies signals | RJ45 is a connector; a repeater amplifies signals
C: A switch makes a network faster than a hub | it sends each frame only to the intended port instead of every port
C: Repeaters are used in long cable runs | signals weaken (attenuate) as they travel along a cable
X: C2 D3 2 | What is the difference between a router and a switch? | A switch connects devices within one network using MAC addresses; a router connects different networks and forwards packets using IP addresses.
"""), ST(S + '05-st3', 'network topologies', """
T: topology | the arrangement of computers and other devices and the links between them in a network
T: bus topology | a layout in which all nodes are connected to a single backbone cable
T: star topology | a layout in which every node is connected to a central hub or switch
T: tree topology | a hierarchical layout formed by connecting several star networks to a bus or main switch
T: mesh topology | a layout in which each node is connected to every other node
Q: In which topology does failure of the central device stop the entire network? | Star | Mesh | Bus | Tree with redundant links
Q: Which topology needs n(n−1)/2 links for n nodes? | Mesh | Star | Bus | Tree
Q: Which topology uses terminators at both ends of the main cable? | Bus | Star | Mesh | Tree
Q: Which topology is the most reliable but the most expensive to cable? | Mesh | Bus | Star | Tree
Q: A tree topology is a combination of: | star and bus topologies | mesh and ring topologies | two meshes | bus and mesh topologies
S+: In star topology a fault in one cable affects only one node
S+: Bus topology needs less cable than star topology
S+: Mesh topology provides alternative paths for data
S+: Tree topology is suitable for networks that are spread over several floors or departments
S-: In bus topology failure of the backbone affects only one computer | A backbone failure stops the whole bus network
S-: Mesh topology needs the least cabling | Mesh needs the most cabling
S-: In star topology all computers share a single cable | Each computer has its own cable to the central device
C: Mesh topology is highly reliable | if one link fails, data can travel through another path
C: Star topology is easy to troubleshoot | each node has a separate cable, so a faulty node can be isolated easily
X: C2 D2 2 | Give one advantage and one disadvantage of star topology. | Advantage: easy to add or remove nodes, a cable fault affects one node. Disadvantage: the whole network fails if the central hub/switch fails; needs more cable than bus.
"""), ST(S + '05-st4', 'network protocols', """
T: protocol | a set of rules that governs communication between devices on a network
T: HTTP | HyperText Transfer Protocol, the protocol used to transfer web pages between a web server and a browser
T: FTP | File Transfer Protocol, used to transfer files between computers on a network
T: SMTP | Simple Mail Transfer Protocol, used to send e-mail
T: POP3 | Post Office Protocol version 3, used to download e-mail from a mail server to the user's computer
T: TELNET | a protocol for logging in to a remote computer and using it from one's own terminal
T: VoIP | Voice over Internet Protocol, a technology for making voice calls over the Internet
T: PPP | Point-to-Point Protocol, used for direct communication between two nodes over a link such as a telephone line
Q: Which protocol is used to send e-mail? | SMTP | POP3 | FTP | HTTP
Q: Which protocol encrypts web data using SSL/TLS? | HTTPS | HTTP | FTP | TELNET
Q: Which protocol is used for remote login? | TELNET | SMTP | PPP | POP3
Q: Which protocol is used to download e-mail to a local computer? | POP3 | SMTP | HTTP | VoIP
Q: Which protocol suite is the basis of the Internet? | TCP/IP | PPP | FTP | VoIP
Q: Which technology allows a phone call over a broadband connection? | VoIP | FTP | POP3 | PPP
S+: TCP breaks a message into packets and reassembles them at the destination
S+: IP is responsible for addressing and routing packets to the destination
S+: HTTPS is used for secure transactions such as online banking
S+: FTP can be used to upload files to a web server
S-: POP3 is used to send e-mail | POP3 downloads e-mail; SMTP sends it
S-: HTTP encrypts data before sending it | HTTPS encrypts; HTTP sends plain text
S-: TELNET is a secure protocol that encrypts passwords | TELNET sends data, including passwords, as plain text
C: Websites asking for passwords should use HTTPS | HTTPS encrypts the data so that it cannot be read if intercepted
C: Packets of one message may arrive in a different order | IP routes each packet independently and TCP reorders them at the destination
X: C2 D2 2 | Expand and give one use of each: (i) SMTP (ii) FTP. | (i) Simple Mail Transfer Protocol – sending e-mail (ii) File Transfer Protocol – transferring files between computers.
"""), ST(S + '05-st5', 'web services', """
T: World Wide Web | an information system of interlinked web pages and resources accessed over the Internet using browsers
T: HTML | HyperText Markup Language, used to design web pages with predefined tags
T: XML | eXtensible Markup Language, used to store and transport data with user-defined tags
T: domain name | the human-readable name of a website, such as cbse.gov.in, which is mapped to an IP address
T: URL | Uniform Resource Locator, the complete address of a resource on the web
T: web browser | a client program used to access and display web pages, such as Chrome or Firefox
T: web server | a computer or program that stores websites and delivers web pages when a browser requests them
T: DNS | Domain Name System, which translates domain names into IP addresses
Q: Who is credited with inventing the World Wide Web at CERN? | Tim Berners-Lee | Vint Cerf | Charles Babbage | Ray Tomlinson
Q: Which language uses user-defined tags? | XML | HTML | Python | SQL
Q: Which system converts a domain name into an IP address? | DNS | URL | HTTP | FTP
Q: In www.ncert.nic.in, the top-level domain is: | in | nic | www | ncert
Q: Which of the following is a web browser? | Mozilla Firefox | Apache | MySQL | Python
Q: A collection of related web pages under one domain is a: | website | web server | browser | URL
S+: HTML is used to display data while XML is used to store and transport data
S+: Every website is hosted on a web server
S+: A URL contains the protocol, the domain name and the path of the resource
S+: The Internet and the World Wide Web are not the same thing
S-: HTML tags are user-defined | HTML has predefined tags; XML tags are user-defined
S-: A web browser stores websites for others to access | A web server stores websites; a browser requests and displays them
S-: The Internet and the WWW mean the same thing | The WWW is a service that runs on the Internet
C: Users can type names instead of IP addresses to open websites | DNS translates domain names into IP addresses
C: XML is used to exchange data between different applications | its user-defined tags describe the meaning of the data
X: C2 D2 2 | Differentiate between a website and a web page. | A web page is a single document on the web; a website is a collection of related web pages under one domain name.
""")]


# ====================================================================== ch06 data communication
UNITS = ['bps', 'Kbps', 'Mbps', 'Gbps', 'Tbps']


def transfer_time(r):
    size = r.choice([2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 64, 100])
    rate = r.choice([1, 2, 4, 5, 8, 10, 16, 20, 40, 50, 80, 100])
    bits = size * 8
    t = bits / rate
    if t != int(t) and round(t, 2) != t:
        raise ValueError('ugly')
    who = r.choice(NAMES)
    ans = f'{num(t)} seconds'
    return {'stem': f'{who} downloads a {size} MB file over a link whose data transfer rate is {rate} Mbps. How long does the download take? (Take 1 byte = 8 bits, so 1 MB = 8 Mb, and ignore overheads.)',
            'answer': ans, 'key': f'Time = size in bits / rate = {size} × 8 / {rate} = {num(t)} s.', 'marks': 2,
            'distractors': uniq([f'{num(size / rate)} seconds', f'{num(t * 8)} seconds', f'{num(rate * 8 / size)} seconds', f'{num(t / 2)} seconds'], [ans])}


def unit_conv(r):
    i = r.randrange(1, 4)
    x = r.choice([2, 3, 4, 5, 8, 16])
    t = r.randrange(2)
    if t == 0:
        a = x * 1024
        ans = f'{a} {UNITS[i - 1]}'
        return mcq(f'Convert {x} {UNITS[i]} into {UNITS[i - 1]}. (Take 1 {UNITS[i]} = 1024 {UNITS[i - 1]}.)', ans,
                   [f'{x * 1000 + 24} {UNITS[i - 1]}', f'{x * 8} {UNITS[i - 1]}', f'{x * 1024 * 8} {UNITS[i - 1]}'], f'{x} × 1024 = {a}.', r)
    a = x * 1024
    ans = f'{x} {UNITS[i]}'
    return mcq(f'A link transfers data at {a} {UNITS[i - 1]}. Express this rate in {UNITS[i]}. (1 {UNITS[i]} = 1024 {UNITS[i - 1]})', ans,
               [f'{x * 8} {UNITS[i]}', f'{a // 8} {UNITS[i]}', f'{x * 1024} {UNITS[i]}'], f'{a} / 1024 = {x}.', r)


MEDIA = [
    ('carries data as pulses of light and is immune to electromagnetic interference', 'Optical fibre'),
    ('is the most common cable in LANs, with pairs of insulated copper wires twisted together', 'Twisted pair cable'),
    ('has a central copper conductor surrounded by insulation and a braided metal shield, and is used for cable TV', 'Coaxial cable'),
    ('is omnidirectional, can penetrate walls and covers 3 KHz to 1 GHz', 'Radio waves'),
    ('needs a line of sight between towers, travels in one direction and covers 1 GHz to 300 GHz', 'Microwaves'),
    ('is used in TV remotes, works over short distances and cannot pass through walls', 'Infrared'),
    ('offers the highest bandwidth among wired media and is used for undersea Internet links', 'Optical fibre'),
    ('is used for satellite communication and long-distance point-to-point links', 'Microwaves'),
    ('is cheap and flexible but has a limited range of about 100 m before signals weaken', 'Twisted pair cable'),
]
MEDIA_ALL = ['Optical fibre', 'Twisted pair cable', 'Coaxial cable', 'Radio waves', 'Microwaves', 'Infrared']


def media_pick(r):
    d, t = r.choice(MEDIA)
    return mcq(f'Identify the transmission medium that {d}.', t, r.sample([x for x in MEDIA_ALL if x != t], 3), f'{t} {d}.', r)


SW_SCEN = [
    ('A dedicated path is set up between caller and receiver before a landline telephone conversation begins.', 'Circuit switching'),
    ('An e-mail is broken into small units that travel by different routes and are reassembled at the destination.', 'Packet switching'),
    ('The full bandwidth of the path is reserved for the users even when no one is speaking.', 'Circuit switching'),
    ('No dedicated path is reserved; units of data are stored and forwarded by routers, as on the Internet.', 'Packet switching'),
    ('There is a call set-up phase before data transfer and the path is released when the call ends.', 'Circuit switching'),
    ('Each unit of data carries the destination address and may arrive out of order.', 'Packet switching'),
]


def switch_pick(r):
    d, t = r.choice(SW_SCEN)
    return mcq(f'Which switching technique is described? {d}', t, [x for x in ['Circuit switching', 'Packet switching', 'Message broadcasting', 'Bus switching'] if x != t],
               f'{t}.', r)


GEN = [('analog cellular network that carried only voice calls', '1G'), ('digital network that introduced SMS text messages (GSM/CDMA)', '2G'),
       ('generation that made mobile Internet browsing and video calls common', '3G'), ('all-IP high-speed network based on LTE, used for HD video streaming', '4G'),
       ('generation offering very high speed and very low latency, suitable for IoT and self-driving cars', '5G')]


def gen_pick(r):
    d, t = r.choice(GEN)
    return mcq(f'Which generation of mobile telecommunication is described: an {d}?' if d[0] in 'aeiou' else f'Which generation of mobile telecommunication is described: a {d}?',
               t, [x for x in ['1G', '2G', '3G', '4G', '5G'] if x != t][:3] if t != '1G' else ['2G', '3G', '4G'], f'{t}.', r)


CH06 = [ST(S + '06-st1', 'data communication', """
T: sender | the device that sends the message, such as a computer or phone
T: receiver | the device that receives the message
T: message | the data or information to be communicated, such as text, image, audio or video
T: communication medium | the path through which the message travels from sender to receiver, wired or wireless
T: bandwidth | the range of frequencies a channel can carry, measured in hertz (Hz)
T: data transfer rate | the number of bits transferred per second over a channel, measured in bps
Q: Bandwidth of a channel is measured in: | hertz (Hz) | bits per second | bytes | metres
Q: Data transfer rate is measured in: | bits per second (bps) | hertz | watts | decibels
Q: The rules that both sender and receiver follow during communication are called the: | protocol | medium | message | bandwidth
Q: Taking binary multiples (1 Kbps = 1024 bps), 1 Gbps is equal to: | 1024 Mbps | 1000 Kbps | 1024 Kbps | 8 Mbps
Q: Which is the correct order of units from smallest to largest? | bps, Kbps, Mbps, Gbps | Mbps, Kbps, Gbps, bps | Kbps, bps, Mbps, Gbps | Gbps, Mbps, Kbps, bps
S+: The five components of data communication are sender, receiver, message, communication medium and protocol
S+: A channel with higher bandwidth can carry more data per second
S+: Data transfer rate is expressed in units such as Kbps, Mbps and Gbps
S-: Bandwidth is measured in bytes per second | Bandwidth is measured in hertz; data transfer rate in bits per second
S-: A protocol is the physical path of the data | The medium is the path; a protocol is a set of rules
C: Communication between two devices needs a common protocol | both must follow the same rules to interpret the data correctly
X: C2 D2 2 | Name the components of data communication and explain any two. | Sender, receiver, message, medium, protocol; e.g. sender originates the message; protocol is the set of agreed rules.
"""), ST(S + '06-st2', 'switching techniques', """
T: switching | the technique of deciding the path through which data travels between two nodes in a network
T: circuit switching | a technique in which a dedicated physical path is set up between sender and receiver before communication and kept for the whole session
T: packet switching | a technique in which a message is broken into packets that travel independently, possibly by different routes, and are reassembled at the destination
T: packet | a small unit of data carrying the destination address and a sequence number
Q: The landline telephone system uses: | circuit switching | packet switching | message broadcasting | no switching
Q: The Internet mainly uses: | packet switching | circuit switching | analog switching | a dedicated line per user
Q: In packet switching, packets of the same message: | may travel by different routes | always travel by one fixed path | are never reordered | need a call set-up
S+: In circuit switching the path stays reserved even when no data is being sent
S+: Packet switching uses the bandwidth of links more efficiently than circuit switching
S+: In packet switching each packet carries the address of the destination
S-: Packet switching requires a dedicated path to be set up first | Circuit switching sets up a dedicated path; packet switching does not
S-: In circuit switching packets may arrive out of order | Data follows one dedicated path in order; packets may arrive out of order only in packet switching
C: Packet switching is more efficient for Internet traffic | the link is shared by many users and capacity is not wasted when one user is idle
X: C2 D3 2 | Differentiate between circuit switching and packet switching (two points). | Circuit: dedicated path set up first, reserved throughout, data in order, e.g. telephone. Packet: no dedicated path, message split into packets, different routes, reassembled, e.g. Internet.
"""), ST(S + '06-st3', 'transmission media', """
T: guided media | wired transmission media in which signals travel through a physical cable, such as twisted pair, coaxial and optical fibre
T: unguided media | wireless transmission media in which signals travel through air or space, such as radio waves, microwaves and infrared
T: twisted pair cable | a cable of pairs of insulated copper wires twisted together to reduce interference, available as UTP and STP
T: coaxial cable | a cable with a central copper conductor, insulation, a braided metal shield and an outer cover
T: optical fibre | a cable of thin glass or plastic fibres that carries data as light pulses using total internal reflection
T: microwaves | electromagnetic waves of about 1 GHz to 300 GHz that need line of sight and are unidirectional
T: infrared | electromagnetic waves of about 300 GHz to 400 THz used for short-range communication such as TV remotes
Q: Which medium is immune to electromagnetic interference? | Optical fibre | Twisted pair | Coaxial cable | Radio waves
Q: Which wireless medium cannot pass through walls and is used in remote controls? | Infrared | Radio waves | Microwaves | Satellite radio
Q: Which medium needs line-of-sight towers? | Microwaves | Radio waves | Twisted pair | Coaxial cable
Q: Which cable is used in cable TV connections? | Coaxial cable | Optical fibre | UTP | RJ45
Q: Radio waves have a frequency range of about: | 3 KHz to 1 GHz | 300 GHz to 400 THz | 1 GHz to 300 GHz | above 400 THz
Q: Which wired medium has the highest bandwidth? | Optical fibre | Coaxial cable | Twisted pair | Telephone wire
S+: Optical fibre uses the principle of total internal reflection
S+: Twisted pair cable is cheap and easy to install
S+: Radio waves are omnidirectional and can penetrate walls
S+: Satellite communication uses microwaves
S-: Infrared signals can pass through walls | Infrared cannot penetrate walls; it works within a room
S-: Optical fibre is the cheapest transmission medium | It is costly and needs skilled installation
S-: Microwaves are omnidirectional | Microwaves are unidirectional and need line of sight
C: Optical fibre is used for long-distance high-speed links | it has very high bandwidth and low signal loss and is not affected by electromagnetic interference
C: Twisted pair wires are twisted together | twisting reduces electromagnetic interference and crosstalk
M:medium: Optical fibre | light pulses through glass fibres
M:medium: Coaxial cable | cable TV connection
M:medium: Microwaves | line-of-sight towers and satellites
M:medium: Infrared | TV remote control
M:medium: Radio waves | FM broadcasts, penetrate walls
X: C2 D3 2 | Give one advantage and one disadvantage of optical fibre. | Advantage: very high bandwidth, immune to EMI, low loss, secure. Disadvantage: expensive, fragile, difficult to install and join.
"""), ST(S + '06-st4', 'mobile telecommunication technologies', """
T: 1G | the first generation of mobile networks, analog and voice-only
T: 2G | the second generation, digital networks (GSM, CDMA) that introduced SMS
T: 3G | the third generation, which made mobile Internet and video calling possible
T: 4G | the fourth generation, all-IP networks based on LTE with high data speeds
T: 5G | the fifth generation, offering very high speed, very low latency and support for many connected devices
Q: SMS was introduced with: | 2G | 1G | 4G | 5G
Q: Which generation was analog? | 1G | 2G | 3G | 4G
Q: LTE is associated with: | 4G | 2G | 1G | 3G
Q: Which generation is designed for very low latency and the Internet of Things? | 5G | 3G | 2G | 1G
S+: Each new generation of mobile technology has offered higher data speeds
S+: 2G was the first digital generation of mobile networks
S+: 5G supports a very large number of connected devices
S-: 1G networks were digital | 1G was analog; digital networks began with 2G
S-: 4G was the first generation to allow SMS | SMS came with 2G
C: 5G is suitable for self-driving cars and remote surgery | it has very low latency and very high speed
X: C2 D2 2 | Give one feature each of 3G and 4G mobile technologies. | 3G: mobile Internet browsing and video calls; 4G: LTE, all-IP, high-speed data for HD streaming.
""")]


def fams_ch05_06():
    E = {}
    E[S + '05-st1'] = [F('C2', 'D2', 'mcq', net_pick), F('C3', 'D3', 'mcq', net_pick), F('C4', 'D4', 'long', campus_case, marks=5, gap='G7'),
                       F('C2', 'D3', 'explain', net_compare(None), marks=2)]
    E[S + '05-st2'] = [F('C2', 'D2', 'mcq', dev_pick), F('C3', 'D3', 'mcq', repeater_pick), F('C3', 'D2', 'mcq', server_pick), F('C4', 'D4', 'long', campus_case, marks=5, gap='G7'),
                       F('C3', 'D3', 'explain', net_compare(None), marks=2), F('C1', 'D1', 'mcq', dev_pick), F('C4', 'D3', 'mcq', repeater_pick)]
    E[S + '05-st3'] = [F('C2', 'D2', 'mcq', topo_pick), F('C3', 'D3', 'short', mesh_count), F('C3', 'D4', 'mcq', topo_pick, gap='G5'), F('C4', 'D4', 'long', campus_case, marks=5, gap='G7'),
                       F('C1', 'D1', 'short', mesh_count), F('C2', 'D3', 'explain', net_compare(None), marks=2)]
    E[S + '05-st4'] = [F('C2', 'D2', 'mcq', prot_pick), F('C3', 'D3', 'mcq', prot_pick), F('C1', 'D1', 'mcq', prot_pick), F('C3', 'D4', 'explain', net_compare(None), marks=2, gap='G5'),
                       F('C4', 'D5', 'long', campus_case, marks=5, gap='G7')]
    E[S + '05-st5'] = [F('C2', 'D2', 'mcq', url_parts), F('C3', 'D3', 'mcq', url_parts), F('C2', 'D3', 'explain', net_compare(None), marks=2)]
    E[S + '06-st1'] = [F('C3', 'D3', 'numerical', transfer_time, marks=2), F('C2', 'D2', 'mcq', unit_conv), F('C3', 'D4', 'numerical', transfer_time, marks=2, gap='G5'),
                       F('C1', 'D1', 'mcq', unit_conv)]
    E[S + '06-st2'] = [F('C2', 'D2', 'mcq', switch_pick), F('C3', 'D3', 'mcq', switch_pick)]
    E[S + '06-st3'] = [F('C2', 'D2', 'mcq', media_pick), F('C3', 'D3', 'mcq', media_pick), F('C1', 'D1', 'mcq', media_pick), F('C4', 'D4', 'long', campus_case, marks=5, gap='G7')]
    E[S + '06-st4'] = [F('C2', 'D2', 'mcq', gen_pick), F('C4', 'D4', 'long', campus_case, marks=5, gap='G7'), F('C3', 'D3', 'mcq', gen_pick)]
    return [CH05, CH06], E
